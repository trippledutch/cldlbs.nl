#!/usr/bin/env python3
"""
ClusterTriage blog publish helper.

Usage:
    ./publish.py --list                                   # status of every slug, EN + NL
    ./publish.py <slug> [--lang en|nl]                    # publish a draft card (default lang: en)
    ./publish.py <slug> --date YYYY-MM-DD [--lang en|nl]  # publish AND set the date
    ./publish.py <slug> --sticky [--lang en|nl]           # publish AND mark as sticky/featured
    ./publish.py --sticky <slug>                          # mark sticky without publishing
    ./publish.py --unsticky <slug>                        # remove sticky flag
    ./publish.py --unpublish <slug> [--lang en|nl]        # back to draft (hide the card)
    ./publish.py --reorder [--lang en|nl]                 # rebuild card order (default: both)
    ./publish.py --sync-links [--lang en|nl]              # rebuild cross-blog link visibility
    ./publish.py --wrap-links [--lang en|nl]              # wrap unmarked cross-blog links + sync
    ./publish.py --sitemap                                # sync blog URLs into sitemap.xml
    ./publish.py --indexnow [<slug> [--lang en|nl]]        # ping IndexNow after deploy

A "slug" is a directory name under en/blog/ and/or nl/blog/, e.g.
en/blog/csv-ownership-imbalance/index.html -> slug csv-ownership-imbalance.
Slugs are discovered from the filesystem, not a hardcoded list, so a new
article directory is picked up automatically. EN and NL are independent:
a slug can be published in one language and still a draft (or nonexistent)
in the other.

REQUIRED BEFORE PUBLISHING A NEW BLOG:
  1. Write <lang>/blog/<slug>/index.html (canonical + hreflang pointing at
     clustertriage.com, not cldlbs.com)
  2. Add a blog card to <lang>/blog/index.html wrapped in DRAFT comments
     (see the DRAFT comment format used by unpublish, below)

If the blog card is missing entirely (never even added as a DRAFT), publish
will report "no card found" rather than inventing one — author the card by
hand first.

What "publish" does:
  1. Remove <meta name="robots" content="noindex,nofollow"> from the article
     file, if present (new articles are not required to have it)
  2. Uncomment the blog card in <lang>/blog/index.html

"unpublish" does the inverse. Idempotent. Safe to run multiple times.
"""
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).parent
DOMAIN = 'clustertriage.com'
STICKY_FILE = ROOT / 'sticky.txt'
SITEMAP = ROOT / 'sitemap.xml'

NOINDEX_LINE = '<meta name="robots" content="noindex,nofollow">\n'

LANGS = ('en', 'nl')

def blog_dir(lang):
    return ROOT / lang / 'blog'

def blog_index(lang):
    return blog_dir(lang) / 'index.html'

def article_file(slug, lang):
    return blog_dir(lang) / slug / 'index.html'

def url_path(slug, lang):
    return f'/{lang}/blog/{slug}/'

def listing_url_path(lang):
    return f'/{lang}/blog/'

# ----------------------------------------------------------------------------
# Slug discovery

def discover_slugs(lang):
    d = blog_dir(lang)
    if not d.exists():
        return []
    return sorted(p.parent.name for p in d.glob('*/index.html'))

def all_slugs():
    return sorted(set(discover_slugs('en')) | set(discover_slugs('nl')))

# ----------------------------------------------------------------------------
# Card / publish state in <lang>/blog/index.html

def _card_pattern(slug, lang):
    href = re.escape(url_path(slug, lang))
    return re.compile(
        r'<a class="blog-card(?: featured)?" href="' + href + r'">.*?</a>',
        re.DOTALL,
    )

def _draft_pattern(slug, lang):
    href = re.escape(url_path(slug, lang))
    return re.compile(
        r'<!-- DRAFT, not yet published\. Remove these comments to publish\.\n'
        r'(\s*<a class="blog-card(?: featured)?" href="' + href + r'">.*?</a>)\n'
        r'\s*-->',
        re.DOTALL,
    )

def card_state(slug, lang):
    """'live', 'draft', or None (no card at all) for slug in that language's listing."""
    idx = blog_index(lang)
    if not idx.exists():
        return None
    t = idx.read_text(encoding='utf-8')
    if _draft_pattern(slug, lang).search(t):
        return 'draft'
    if _card_pattern(slug, lang).search(t):
        return 'live'
    return None

def is_published(slug, lang):
    return card_state(slug, lang) == 'live'

# ----------------------------------------------------------------------------
# Date helpers

MONTHS_EN = ['January', 'February', 'March', 'April', 'May', 'June',
             'July', 'August', 'September', 'October', 'November', 'December']
MONTHS_NL = ['januari', 'februari', 'maart', 'april', 'mei', 'juni',
             'juli', 'augustus', 'september', 'oktober', 'november', 'december']

def _parse_iso(date_iso):
    m = re.fullmatch(r'(\d{4})-(\d{2})-(\d{2})', date_iso or '')
    if not m:
        raise ValueError(f'Invalid date (expected YYYY-MM-DD): {date_iso!r}')
    return int(m.group(1)), int(m.group(2)), int(m.group(3))

def format_date(date_iso, lang):
    y, mo, d = _parse_iso(date_iso)
    months = MONTHS_EN if lang == 'en' else MONTHS_NL
    return f'{d} {months[mo - 1]} {y}'

def published_date(slug, lang):
    f = article_file(slug, lang)
    if not f.exists():
        return None
    m = re.search(r'"datePublished"\s*:\s*"(\d{4}-\d{2}-\d{2})"', f.read_text(encoding='utf-8'))
    return m.group(1) if m else None

def set_date(slug, lang, date_iso):
    """Overwrite the date in the article file (JSON-LD + visible byline) and
    in its listing card, for one language only."""
    _parse_iso(date_iso)
    f = article_file(slug, lang)
    if not f.exists():
        return False
    t = f.read_text(encoding='utf-8')
    human = format_date(date_iso, lang)
    t = re.sub(r'"datePublished"\s*:\s*"\d{4}-\d{2}-\d{2}"',
               f'"datePublished": "{date_iso}"', t)
    t = re.sub(r'"dateModified"\s*:\s*"\d{4}-\d{2}-\d{2}"',
               f'"dateModified": "{date_iso}"', t)
    # Visible byline: <p class="artikelmeta"><b>By/Door ...</b> <i>&middot;</i> <b>DATE</b> ...
    byline = 'By Hans Vredevoort' if lang == 'en' else 'Door Hans Vredevoort'
    t = re.sub(
        r'(<p class="artikelmeta"><b>' + re.escape(byline) + r'</b> <i>&middot;</i> <b>)'
        r'[^<]+(</b>)',
        rf'\g<1>{human}\g<2>',
        t,
    )
    f.write_text(t, encoding='utf-8')
    # Listing card date: <div class="meta">YYYY-MM-DD · X min read</div>
    idx = blog_index(lang)
    t2 = idx.read_text(encoding='utf-8')
    card_pat = re.compile(
        r'(<a class="blog-card(?: featured)?" href="' + re.escape(url_path(slug, lang)) +
        r'">.*?<div class="meta">)\d{4}-\d{2}-\d{2}( \xb7 [^<]+</div>)',
        re.DOTALL,
    )
    new2, n = card_pat.subn(rf'\g<1>{date_iso}\g<2>', t2)
    if n:
        idx.write_text(new2, encoding='utf-8')
    return True

def get_dates(slug, lang):
    """(created, published, modified) as YYYY-MM-DD strings or '-'."""
    f = article_file(slug, lang)
    if not f.exists():
        return '-', '-', '-'
    t = f.read_text(encoding='utf-8')
    pub = (re.search(r'"datePublished"\s*:\s*"([^"]+)"', t) or [None, '-'])[1]
    mod = (re.search(r'"dateModified"\s*:\s*"([^"]+)"', t) or [None, '-'])[1]
    try:
        out = subprocess.run(
            ['git', 'log', '--diff-filter=A', '--follow',
             '--format=%ad', '--date=short', '--reverse',
             '--', str(f.relative_to(ROOT))],
            capture_output=True, text=True, cwd=ROOT, check=False,
        ).stdout.strip().splitlines()
        created = out[0] if out else '-'
    except Exception:
        created = '-'
    return created, pub, mod

def _display_state(slug, lang):
    """card_state, but a 'live' card whose article file doesn't exist is a
    dead link (404), not really 'published' — call that out explicitly."""
    st = card_state(slug, lang)
    if st == 'live' and not article_file(slug, lang).exists():
        return 'BROKEN'
    return st or 'MISSING'

def list_status():
    sticky = set(load_sticky())
    print(f'{"Slug":<48} {"Sticky":<7} {"EN":<9} {"NL":<9} {"Published":<11} {"Modified":<11}')
    print('-' * 100)
    for slug in all_slugs():
        en_state = _display_state(slug, 'en')
        nl_state = _display_state(slug, 'nl')
        lang_for_dates = 'en' if article_file(slug, 'en').exists() else 'nl'
        _, pub, mod = get_dates(slug, lang_for_dates)
        sticky_mark = '*' if slug in sticky else ''
        print(f'{slug:<48} {sticky_mark:<7} {en_state:<9} {nl_state:<9} {pub:<11} {mod:<11}')

# ----------------------------------------------------------------------------
# noindex toggling on the article file itself (optional; new articles are not
# required to carry it, so both helpers are no-ops when it's absent)

def publish_post_file(slug, lang):
    f = article_file(slug, lang)
    if not f.exists():
        return False
    t = f.read_text(encoding='utf-8')
    if 'name="robots"' not in t:
        return False
    t = re.sub(r'<meta name="robots"[^>]*>\n', '', t, count=1)
    f.write_text(t, encoding='utf-8')
    return True

def unpublish_post_file(slug, lang):
    f = article_file(slug, lang)
    if not f.exists():
        return False
    t = f.read_text(encoding='utf-8')
    if 'name="robots"' in t:
        return False
    t = re.sub(r'(<meta name="viewport"[^>]*>\n)', r'\1' + NOINDEX_LINE, t, count=1)
    f.write_text(t, encoding='utf-8')
    return True

# ----------------------------------------------------------------------------
# Card visibility in <lang>/blog/index.html

def publish_card_in_index(slug, lang):
    idx = blog_index(lang)
    t = idx.read_text(encoding='utf-8')
    m = _draft_pattern(slug, lang).search(t)
    if not m:
        return False
    idx.write_text(t[:m.start()] + m.group(1) + t[m.end():], encoding='utf-8')
    return True

def unpublish_card_in_index(slug, lang):
    idx = blog_index(lang)
    t = idx.read_text(encoding='utf-8')
    if _draft_pattern(slug, lang).search(t):
        return False  # already a draft
    m = _card_pattern(slug, lang).search(t)
    if not m:
        return False  # no card at all
    block = m.group(0)
    wrapped = (
        '<!-- DRAFT, not yet published. Remove these comments to publish.\n'
        f'{block}\n      -->'
    )
    idx.write_text(t[:m.start()] + wrapped + t[m.end():], encoding='utf-8')
    return True

# ----------------------------------------------------------------------------
# Cross-blog LINK markers inside article bodies.
#
#   inline:  <!--LINK:slug--><a href="/<lang>/blog/slug/">link text</a><!--/LINK:slug-->
#   list:    <!--LINK:slug--><li><a href="/<lang>/blog/slug/">...</a></li><!--/LINK:slug-->
#
# When the target slug is a draft (or missing) in that language, sync_links()
# hides the link:
#   - inline anchor -> plain text (strips <a> tags, keeps inner text)
#   - <li> wrapper  -> HTML comment placeholder (entire <li> removed from render)
# The markers stay in place either way, so the transition is reversible.

LINK_BLOCK_RE = re.compile(
    r'<!--LINK:(?P<slug>[a-z0-9-]+)-->(?P<body>.*?)<!--/LINK:(?P=slug)-->',
    re.DOTALL,
)
LI_BODY_RE = re.compile(r'^\s*<li>.*</li>\s*$', re.DOTALL)
LI_HIDDEN_RE = re.compile(r'^<!--draft:(?P<inner><li>.*</li>)-->$', re.DOTALL)
INLINE_BODY_RE = re.compile(r'^<a [^>]*>(?P<text>.*)</a>$', re.DOTALL)
INLINE_HIDDEN_RE = re.compile(r'^<!--draft:(?P<inner><a [^>]*>.*</a>)-->(?P<text>.*)$', re.DOTALL)


def _transform_block(slug, body, published_slugs):
    is_pub = slug in published_slugs

    m = LI_HIDDEN_RE.match(body)
    if m:
        return m.group('inner') if is_pub else body

    m = INLINE_HIDDEN_RE.match(body)
    if m:
        return m.group('inner') if is_pub else body

    if LI_BODY_RE.match(body):
        if is_pub:
            return body
        return f'<!--draft:{body.strip()}-->'

    m = INLINE_BODY_RE.match(body)
    if m:
        if is_pub:
            return body
        return f'<!--draft:{body}-->{m.group("text")}'

    return body  # unknown shape, leave untouched


def wrap_links(lang=None, verbose=True):
    """Walk every article file in `lang` (or both) and wrap any unmarked
    cross-blog references (<a href="/<lang>/blog/<slug>/">) that aren't
    already inside a LINK marker."""
    langs = [lang] if lang else list(LANGS)
    changed_files = 0
    for cur_lang in langs:
        slugs = set(discover_slugs(cur_lang))
        if not slugs:
            continue
        slug_alt = '|'.join(re.escape(s) for s in slugs)
        href_prefix = re.escape(f'/{cur_lang}/blog/')
        li_re = re.compile(
            r'(?P<full><li>\s*<a href="' + href_prefix + r'(?P<slug>' + slug_alt + r')/">.*?</a>\s*</li>)',
            re.DOTALL,
        )
        a_re = re.compile(
            r'(?P<full><a href="' + href_prefix + r'(?P<slug>' + slug_alt + r')/">.*?</a>)',
            re.DOTALL,
        )
        for f in sorted(blog_dir(cur_lang).glob('*/index.html')):
            self_slug = f.parent.name
            t = f.read_text(encoding='utf-8')
            original = t

            def li_repl(m):
                slug = m.group('slug')
                if slug == self_slug:
                    return m.group('full')
                start = m.start()
                preceding = t[max(0, start - 80):start]
                if f'<!--LINK:{slug}-->' in preceding and '<!--/LINK:' not in preceding.split(f'<!--LINK:{slug}-->')[-1]:
                    return m.group('full')
                return f'<!--LINK:{slug}-->{m.group("full")}<!--/LINK:{slug}-->'
            t = li_re.sub(li_repl, t)

            def a_repl(m):
                slug = m.group('slug')
                if slug == self_slug:
                    return m.group('full')
                start = m.start()
                preceding = t[max(0, start - 80):start]
                last_open = preceding.rfind(f'<!--LINK:{slug}-->')
                last_close = preceding.rfind(f'<!--/LINK:{slug}-->')
                if last_open > last_close:
                    return m.group('full')
                return f'<!--LINK:{slug}-->{m.group("full")}<!--/LINK:{slug}-->'
            t = a_re.sub(a_repl, t)

            if t != original:
                f.write_text(t, encoding='utf-8')
                changed_files += 1
                if verbose:
                    print(f'  wrapped links in: {f.relative_to(ROOT)}')
    if verbose and changed_files == 0:
        print('  no unwrapped cross-blog links found')
    return changed_files


def sync_links(lang=None, verbose=True):
    """Walk every article file in `lang` (or both) and update cross-blog
    link visibility to match current publish state, in that same language."""
    langs = [lang] if lang else list(LANGS)
    changed_files = 0
    for cur_lang in langs:
        published = {s for s in discover_slugs(cur_lang) if is_published(s, cur_lang)}
        for f in sorted(blog_dir(cur_lang).glob('*/index.html')):
            t = f.read_text(encoding='utf-8')

            def repl(m):
                new_body = _transform_block(m.group('slug'), m.group('body'), published)
                return f'<!--LINK:{m.group("slug")}-->{new_body}<!--/LINK:{m.group("slug")}-->'
            new = LINK_BLOCK_RE.sub(repl, t)
            if new != t:
                f.write_text(new, encoding='utf-8')
                changed_files += 1
                if verbose:
                    print(f'  synced links in: {f.relative_to(ROOT)}')
    if verbose and changed_files == 0:
        print('  links already in sync')
    return changed_files

# ----------------------------------------------------------------------------
# Sticky cards + reorder by date (shared across languages: sticky.txt holds
# slugs, applied to whichever language's listing has a card for that slug)

def load_sticky():
    if not STICKY_FILE.exists():
        return []
    return [
        line.strip() for line in STICKY_FILE.read_text(encoding='utf-8').splitlines()
        if line.strip() and not line.startswith('#')
    ]

def save_sticky(slugs):
    STICKY_FILE.write_text('\n'.join(slugs) + '\n' if slugs else '', encoding='utf-8')

def add_sticky(slug):
    slugs = load_sticky()
    if slug in slugs:
        return False
    slugs.append(slug)
    save_sticky(slugs)
    return True

def remove_sticky(slug):
    slugs = load_sticky()
    if slug not in slugs:
        return False
    slugs.remove(slug)
    save_sticky(slugs)
    return True

BLOG_GRID_RE = re.compile(r'(<div class="blog-grid">)(.*?)(\n</div>)', re.DOTALL)
_SLUG_FROM_BLOCK_RE = re.compile(r'/blog/([a-z0-9-]+)/"')
_DATE_FROM_BLOCK_RE = re.compile(r'<div class="meta">(\d{4}-\d{2}-\d{2})')


def _card_block_re(lang):
    href_prefix = re.escape(f'/{lang}/blog/')
    return re.compile(
        r'(?:<!-- DRAFT, not yet published\. Remove these comments to publish\.\s*'
        r'<a class="blog-card(?: featured)?" href="' + href_prefix + r'[a-z0-9-]+/">.*?</a>\s*-->'
        r'|'
        r'<a class="blog-card(?: featured)?" href="' + href_prefix + r'[a-z0-9-]+/">.*?</a>)',
        re.DOTALL,
    )


def _apply_featured_class(block, is_sticky):
    target = 'class="blog-card featured"' if is_sticky else 'class="blog-card"'
    return re.sub(r'class="blog-card(?: featured)?"', target, block, count=1)


def reorder_cards(lang=None, verbose=True):
    """Reorder cards in <lang>/blog/index.html (or both): sticky slugs first,
    then everything else, each group sorted by date descending."""
    langs = [lang] if lang else list(LANGS)
    sticky_set = set(load_sticky())
    any_change = False
    for cur_lang in langs:
        idx = blog_index(cur_lang)
        if not idx.exists():
            continue
        t = idx.read_text(encoding='utf-8')
        m = BLOG_GRID_RE.search(t)
        if not m:
            if verbose:
                print(f'  [{cur_lang}] blog-grid section not found')
            continue
        grid_open, grid_close = m.group(1), m.group(3)

        blocks = []
        for cm in _card_block_re(cur_lang).finditer(m.group(2)):
            block = cm.group(0)
            slug_m = _SLUG_FROM_BLOCK_RE.search(block)
            date_m = _DATE_FROM_BLOCK_RE.search(block)
            if not slug_m:
                continue
            slug = slug_m.group(1)
            date = date_m.group(1) if date_m else '0000-00-00'
            block = _apply_featured_class(block, slug in sticky_set)
            blocks.append((slug, date, block))

        sticky_blocks = sorted([b for b in blocks if b[0] in sticky_set], key=lambda e: e[1], reverse=True)
        non_sticky_blocks = sorted([b for b in blocks if b[0] not in sticky_set], key=lambda e: e[1], reverse=True)
        ordered = sticky_blocks + non_sticky_blocks

        new_body = '\n' + ''.join('\n' + block + '\n' for _, _, block in ordered)
        new = t[:m.start()] + grid_open + new_body + grid_close + t[m.end():]
        if new != t:
            idx.write_text(new, encoding='utf-8')
            any_change = True
            if verbose:
                print(f'  [{cur_lang}] reordered {len(ordered)} cards ({len(sticky_blocks)} sticky + {len(non_sticky_blocks)} by date)')
        elif verbose:
            print(f'  [{cur_lang}] cards already in order')
    return any_change

# ----------------------------------------------------------------------------
# sitemap.xml

def _is_rebranded(slug, lang):
    """True if the article file's own canonical already points at
    clustertriage.com (i.e. it has been through the chrome/meta fix), so we
    don't hand not-yet-migrated old-brand pages to search engines."""
    f = article_file(slug, lang)
    if not f.exists():
        return False
    t = f.read_text(encoding='utf-8')
    m = re.search(r'<link rel="canonical" href="([^"]+)">', t)
    return bool(m and m.group(1).startswith(f'https://{DOMAIN}/'))

def _sitemap_url_line(loc, alternates, changefreq, priority):
    links = ''.join(
        f'<xhtml:link rel="alternate" hreflang="{hl}" href="{href}"/>'
        for hl, href in alternates
    )
    return f'  <url><loc>{loc}</loc>{links}<changefreq>{changefreq}</changefreq><priority>{priority}</priority></url>\n'

def sitemap_urls_wanted():
    """Every URL (with its alternates) that belongs in sitemap.xml for the
    blog: the two listings, plus every rebranded, published article."""
    urls = {}
    for lang in LANGS:
        loc = f'https://{DOMAIN}{listing_url_path(lang)}'
        other = 'nl' if lang == 'en' else 'en'
        other_loc = f'https://{DOMAIN}{listing_url_path(other)}'
        urls[loc] = _sitemap_url_line(
            loc,
            [(lang, loc), (other, other_loc), ('x-default', f'https://{DOMAIN}{listing_url_path("en")}')],
            'weekly', '0.8',
        )
    for slug in all_slugs():
        alts_available = {
            lang: article_file(slug, lang).exists() and is_published(slug, lang) and _is_rebranded(slug, lang)
            for lang in LANGS
        }
        for lang in LANGS:
            if not alts_available[lang]:
                continue
            loc = f'https://{DOMAIN}{url_path(slug, lang)}'
            other = 'nl' if lang == 'en' else 'en'
            alternates = [(lang, loc)]
            if alts_available[other]:
                alternates.append((other, f'https://{DOMAIN}{url_path(slug, other)}'))
                default_href = loc if lang == 'en' else f'https://{DOMAIN}{url_path(slug, "en")}'
            else:
                default_href = loc
            alternates.append(('x-default', default_href))
            urls[loc] = _sitemap_url_line(loc, alternates, 'yearly', '0.7')
    return urls

def sync_sitemap(verbose=True):
    if not SITEMAP.exists():
        if verbose:
            print('  sitemap.xml not found, skipped')
        return False
    t = SITEMAP.read_text(encoding='utf-8')
    wanted = sitemap_urls_wanted()

    # Remove every existing /blog/ entry (listings + articles) so stale ones
    # (unpublished, un-rebranded, or renamed) don't linger, then re-add.
    existing_blog_pat = re.compile(r'  <url><loc>https://' + re.escape(DOMAIN) + r'/(?:en|nl)/blog/[^<]*</loc>.*?</url>\n')
    removed = len(existing_blog_pat.findall(t))
    t = existing_blog_pat.sub('', t)

    insertion = ''.join(wanted[loc] for loc in sorted(wanted))
    new = t.replace('</urlset>', insertion + '</urlset>')
    if new == SITEMAP.read_text(encoding='utf-8'):
        if verbose:
            print('  sitemap already in sync')
        return False
    SITEMAP.write_text(new, encoding='utf-8')
    if verbose:
        print(f'  sitemap: removed {removed} stale blog entries, wrote {len(wanted)} current ones')
    return True

# ----------------------------------------------------------------------------

def ping_indexnow(urls, verbose=True):
    """Best-effort IndexNow submission. Run AFTER deploy, since it asks
    search engines to crawl the LIVE url now. Never fatal."""
    import json, urllib.request
    urls = list(urls)
    if not urls:
        if verbose:
            print('  IndexNow: nothing to submit')
        return False
    key = None
    for p in sorted(ROOT.glob('*.txt')):
        if re.fullmatch(r'[0-9a-fA-F]{8,128}', p.stem) and p.read_text(encoding='utf-8').strip() == p.stem:
            key = p.stem
            break
    if not key:
        if verbose:
            print('  IndexNow: no key file at site root, skipped')
        return False
    data = json.dumps({
        'host': DOMAIN, 'key': key,
        'keyLocation': f'https://{DOMAIN}/{key}.txt',
        'urlList': urls,
    }).encode()
    req = urllib.request.Request(
        'https://api.indexnow.org/IndexNow', data=data,
        headers={'Content-Type': 'application/json; charset=utf-8'}, method='POST',
    )
    try:
        r = urllib.request.urlopen(req, timeout=15)
        if verbose:
            print(f'  IndexNow: {len(urls)} URL(s) submitted -> HTTP {r.status}')
        return True
    except Exception as e:
        if verbose:
            print(f'  IndexNow: ping failed ({e}); not fatal')
        return False

# ----------------------------------------------------------------------------

def publish(slug, lang='en', date=None, sticky=False):
    if not article_file(slug, lang).exists():
        print(f'No article file for {lang}/blog/{slug}/ — write it first.')
        return 1
    print(f'Publishing {slug} ({lang})...')
    if date:
        try:
            _parse_iso(date)
        except ValueError as e:
            print(f'  ERROR: {e}')
            return 1
        set_date(slug, lang, date)
        print(f'  dates set to {date}:      yes (article + card)')
    r1 = publish_post_file(slug, lang)
    print(f'  noindex removed:       {"yes" if r1 else "not present"}')
    r2 = publish_card_in_index(slug, lang)
    if not r2 and card_state(slug, lang) is None:
        print('  card un-hidden:        FAILED — no card found in the listing, not even as DRAFT. Add one by hand first.')
        return 1
    print(f'  card un-hidden:        {"yes" if r2 else "already visible"}')
    if sticky:
        r5 = add_sticky(slug)
        print(f'  marked sticky:         {"yes" if r5 else "already sticky"}')
    print('  syncing cross-blog links:')
    sync_links(lang)
    print('  reordering blog cards:')
    reorder_cards(lang)
    print('Done. Commit and push to publish live.')
    return 0

def unpublish(slug, lang='en'):
    print(f'Unpublishing {slug} ({lang})...')
    r1 = unpublish_post_file(slug, lang)
    print(f'  noindex added:         {"yes" if r1 else "already present or no article file"}')
    r2 = unpublish_card_in_index(slug, lang)
    print(f'  card hidden:           {"yes" if r2 else "already hidden or no card"}')
    print('  syncing cross-blog links:')
    sync_links(lang)
    print('  reordering blog cards:')
    reorder_cards(lang)
    print('Done.')
    return 0

# ----------------------------------------------------------------------------

def _lang_arg(args, default='en'):
    if '--lang' in args:
        idx = args.index('--lang')
        if idx + 1 < len(args) and args[idx + 1] in LANGS:
            return args[idx + 1]
    return default

def main():
    args = sys.argv[1:]
    if not args or args[0] in ('-h', '--help'):
        print(__doc__)
        return 0
    if args[0] == '--list':
        list_status()
        return 0
    if args[0] == '--sync-links':
        lang = _lang_arg(args, default=None)
        print(f'Syncing cross-blog links ({lang or "both languages"}):')
        sync_links(lang)
        return 0
    if args[0] == '--wrap-links':
        lang = _lang_arg(args, default=None)
        print(f'Wrapping unmarked cross-blog links ({lang or "both languages"}):')
        wrap_links(lang)
        print('Syncing cross-blog links:')
        sync_links(lang)
        return 0
    if args[0] == '--sitemap':
        print('Syncing blog URLs into sitemap.xml:')
        sync_sitemap()
        return 0
    if args[0] == '--indexnow':
        if len(args) >= 2 and not args[1].startswith('--'):
            lang = _lang_arg(args, default='en')
            urls = [f'https://{DOMAIN}{url_path(args[1], lang)}']
        else:
            urls = re.findall(r'<loc>([^<]+)</loc>', SITEMAP.read_text(encoding='utf-8')) if SITEMAP.exists() else []
        print('Submitting to IndexNow:')
        ping_indexnow(urls)
        return 0
    if args[0] == '--reorder':
        lang = _lang_arg(args, default=None)
        print(f'Reordering blog cards ({lang or "both languages"}):')
        reorder_cards(lang)
        return 0
    if args[0] == '--sticky' and len(args) >= 2:
        slug = args[1]
        r = add_sticky(slug)
        print(f'sticky:                {"added" if r else "already sticky"}')
        reorder_cards()
        return 0
    if args[0] == '--unsticky':
        if len(args) < 2:
            print('Usage: ./publish.py --unsticky <slug>')
            return 1
        slug = args[1]
        r = remove_sticky(slug)
        print(f'sticky:                {"removed" if r else "not sticky"}')
        reorder_cards()
        return 0
    if args[0] == '--unpublish':
        if len(args) < 2:
            print('Usage: ./publish.py --unpublish <slug> [--lang en|nl]')
            return 1
        return unpublish(args[1], lang=_lang_arg(args))
    # publish <slug> [--date YYYY-MM-DD] [--sticky] [--lang en|nl]
    slug = args[0]
    date = None
    sticky = '--sticky' in args
    lang = _lang_arg(args)
    if '--date' in args:
        idx = args.index('--date')
        if idx + 1 >= len(args):
            print('Usage: ./publish.py <slug> --date YYYY-MM-DD [--sticky] [--lang en|nl]')
            return 1
        date = args[idx + 1]
    return publish(slug, lang=lang, date=date, sticky=sticky)

if __name__ == '__main__':
    sys.exit(main())
