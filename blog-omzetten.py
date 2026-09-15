#!/usr/bin/env python3
"""CloudLabs · blog-omzetten.py

Zet de zestien artikelen in blog/ om naar de nieuwe huisstijl.

Twee dingen gebeuren tegelijk:

1. De tweetaligheid eruit. De artikelen bevatten Engels en Nederlands in
   hetzelfde bestand, verborgen met CSS. Dat is de grootste SEO-fout van de
   site: Google indexeert één pagina met twee talen door elkaar. Hier blijft
   het Nederlands staan; Engels en Duits krijgen later eigen URL's.

2. De opmaak van de nieuwe site eromheen: pagina.css plus artikel.css, dezelfde
   navigatie en voettekst als de rest, en de inhoudsopgave in de kantlijn.

De URL blijft ongewijzigd. Die zestien adressen hebben waarde opgebouwd en
mogen niet breken.

De inhoud van de artikelen wordt niet herschreven. Alleen de Engelse helft
verdwijnt en de omhulling verandert.

    python3 blog-omzetten.py <bestand>   één artikel, schrijft .nieuw ernaast
    python3 blog-omzetten.py --alles     alle zestien, ter plekke
"""
import re, sys, json, glob, html, pathlib

# Het hoofdmenu hieronder is een kopie van sync-nav.py. Draai dat script na
# elke omzetting, dan blijft het gelijk aan de rest van de site.

# ---------------------------------------------------------------- taalspannen
def strip_taal(s, houd='nl'):
    """Verwijdert <span lang="xx">...</span> van de andere taal en pelt de
    behouden taal uit zijn span. Telt de diepte, want er zitten spans in spans."""
    weg = 'en' if houd == 'nl' else 'nl'
    for taal, verwijder in ((weg, True), (houd, False)):
        uit, i = [], 0
        for m in re.finditer(r'<span lang="%s"[^>]*>' % taal, s):
            if m.start() < i:
                continue
            diepte, j = 1, m.end()
            for t in re.finditer(r'<span\b[^>]*>|</span>', s[m.end():]):
                diepte += 1 if t.group(0) != '</span>' else -1
                if diepte == 0:
                    j = m.end() + t.start()
                    break
            uit.append(s[i:m.start()])
            if not verwijder:
                uit.append(s[m.end():j])
            i = j + len('</span>')
        uit.append(s[i:])
        s = ''.join(uit)
    return s

def plat(t):
    return re.sub(r'\s+', ' ', html.unescape(re.sub(r'<[^>]+>', '', t))).strip()

def blok(s, patroon):
    """Geeft (heel, binnenkant) van het div-blok dat op `patroon` begint,
    geneste divs meegeteld."""
    m = re.search(patroon, s)
    if not m:
        return None, None
    diepte, eind = 1, len(s)
    for t in re.finditer(r'<div\b[^>]*>|</div>', s[m.end():]):
        diepte += 1 if t.group(0) != '</div>' else -1
        if diepte == 0:
            eind = m.end() + t.end()
            break
    return s[m.start():eind], s[m.end():eind - len('</div>')]

def div_blok(s, klasse):
    """Geeft de volledige <div class="klasse">...</div> terug, geneste divs
    meegeteld. Een niet-gulzige regex stopt bij de eerste </div> en pakt dus
    een geneste div verkeerd; vandaar deze diepteteller."""
    m = re.search(r'<div class="%s"[^>]*>' % klasse, s)
    if not m:
        return None, None
    diepte, eind = 1, len(s)
    for t in re.finditer(r'<div\b[^>]*>|</div>', s[m.end():]):
        diepte += 1 if t.group(0) != '</div>' else -1
        if diepte == 0:
            eind = m.end() + t.end()
            break
    return s[m.start():eind], s[m.end():eind - len('</div>')]

# ---------------------------------------------------------------- de omzetting
def omzetten(pad):
    bron = pathlib.Path(pad).read_text(encoding='utf-8')
    slug = pathlib.Path(pad).stem

    hoofd = re.search(r'<main[^>]*>(.*?)</main>', bron, re.S).group(1)

    # De twee talen staan als <div lang="en"> en <div lang="nl"> naast elkaar.
    # Alleen het Nederlandse blok gaat mee.
    _, nl = blok(hoofd, r'<div lang="nl"[^>]*>')
    if nl is None:
        raise SystemExit(f'{pad}: geen <div lang="nl"> gevonden')

    # de titel staat buiten beide blokken, met spannen erin
    h1 = plat(strip_taal(re.search(r'<h1[^>]*>(.*?)</h1>', hoofd, re.S).group(1), 'nl'))

    ledes = [m.group(1).strip() for m in re.finditer(r'<p class="lede">(.*?)</p>', nl, re.S)]
    meta = re.search(r'<div class="meta">(.*?)</div>', nl, re.S)
    metatekst = plat(meta.group(1)) if meta else ''
    onderwerp = metatekst.split('\u00b7')[-1].strip() if '\u00b7' in metatekst else 'Kennisbank'

    _, toc_binnen = div_blok(nl, 'toc')
    toc_ol = re.search(r'<ol.*?</ol>', toc_binnen, re.S).group(0) if toc_binnen else ''

    # alles vanaf de eerste h2 is de tekst
    start = nl.find('<h2')
    tekst = nl[start:] if start != -1 else nl

    # gerelateerde artikelen staan buiten het taalblok en zijn zelf tweetalig
    related, _ = div_blok(hoofd, 'related')
    related = strip_taal(related, 'nl') if related else ''

    # datums en beschrijving uit de oorspronkelijke structured data
    pub = re.search(r'"datePublished"\s*:\s*"([^"]+)"', bron)
    mod = re.search(r'"dateModified"\s*:\s*"([^"]+)"', bron)
    pub = pub.group(1) if pub else '2026-01-01'
    mod = mod.group(1) if mod else pub
    beschrijving = plat(ledes[0])[:300] if ledes else h1

    # vragen voor het FAQ-schema
    vragen = []
    _, fb = div_blok(nl, 'faq-block')
    if fb:
        for st in re.split(r'<div class="faq-q"[^>]*>', fb)[1:]:
            v = plat(st.split('</div>')[0])
            rest = st.split('</div>', 1)[1] if '</div>' in st else ''
            am = re.search(r'<p[^>]*>(.*?)</p>', rest, re.S)
            a = plat(am.group(1)) if am else ''
            if v and a:
                vragen.append((v, a))

    graaf = [{
        "@type": "BreadcrumbList",
        "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "Home", "item": "https://clustertriage.com/"},
            {"@type": "ListItem", "position": 2, "name": "Blog", "item": "https://clustertriage.com/blog/"},
            {"@type": "ListItem", "position": 3, "name": h1,
             "item": f"https://clustertriage.com/blog/{slug}.html"}]
    }, {
        "@type": "BlogPosting",
        "@id": f"https://clustertriage.com/blog/{slug}.html#artikel",
        "headline": h1, "description": beschrijving,
        "inLanguage": "nl-NL", "datePublished": pub, "dateModified": mod,
        "mainEntityOfPage": f"https://clustertriage.com/blog/{slug}.html",
        "articleSection": onderwerp,
        "author": {"@type": "Person", "@id": "https://clustertriage.com/over-ons/#hans",
                   "name": "Hans Vredevoort",
                   "jobTitle": "Cluster- en virtualisatiespecialist",
                   "knowsAbout": ["Hyper-V", "Failover Clustering", "Azure Local",
                                  "Storage Spaces Direct", "Windows Server"]},
        "publisher": {"@type": "Organization", "@id": "https://clustertriage.com/#organisatie",
                      "name": "CloudLabs", "url": "https://clustertriage.com/"}
    }]
    if vragen:
        graaf.append({"@type": "FAQPage",
                      "@id": f"https://clustertriage.com/blog/{slug}.html#vragen",
                      "mainEntity": [{"@type": "Question", "name": v,
                                      "acceptedAnswer": {"@type": "Answer", "text": a}}
                                     for v, a in vragen]})
    ld = json.dumps({"@context": "https://schema.org", "@graph": graaf},
                    ensure_ascii=False, indent=2)

    lede_html = '\n        '.join(f'<p class="lede">{l}</p>' for l in ledes)
    meta_html = ' <i>&middot;</i> '.join(f'<b>{d.strip()}</b>' for d in metatekst.split('·') if d.strip())

    return TEMPLATE.format(
        slug=slug, titel=html.escape(h1), beschrijving=html.escape(beschrijving),
        ld=ld, h1=h1, ledes=lede_html, meta=meta_html,
        toc=toc_ol, tekst=tekst.strip(), related=related, onderwerp=html.escape(onderwerp))

TEMPLATE = '''<!doctype html>
<html lang="nl">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<!-- Omgezet naar de nieuwe huisstijl met blog-omzetten.py. De Engelse helft is
     eruit; die krijgt later een eigen URL onder /en/. De inhoud is niet
     herschreven. noindex staat aan zolang de nieuwe stijl niet live is. -->
<meta name="robots" content="noindex,nofollow">
<meta name="theme-color" content="#0A1024">
<title>{titel} &middot; CloudLabs</title>
<meta name="description" content="{beschrijving}">
<link rel="canonical" href="https://clustertriage.com/blog/{slug}.html">
<link rel="alternate" hreflang="nl" href="https://clustertriage.com/blog/{slug}.html">
<link rel="alternate" hreflang="x-default" href="https://clustertriage.com/blog/{slug}.html">
<meta property="og:type" content="article">
<meta property="og:locale" content="nl_NL">
<meta property="og:url" content="https://clustertriage.com/blog/{slug}.html">
<meta property="og:title" content="{titel}">
<meta property="og:description" content="{beschrijving}">
<link rel="icon" href="/favicon.png" type="image/png">
<link rel="stylesheet" href="/huisstijl/pagina.css">
<link rel="stylesheet" href="/huisstijl/artikel.css">

<script type="application/ld+json">
{ld}
</script>
</head>

<body>
<a class="skip" href="#main">Naar inhoud</a>

<header class="topbar">
  <nav class="nav">
    <a class="brand" href="/preview-home.html">Cloud<span>Labs</span></a>
    <div class="navlinks" id="navlinks"><a href="/triage/">Cluster Triage</a><a href="/na-een-storing/">Na een storing</a><div class="navgroep"><button type="button" class="navtop" aria-expanded="false" aria-controls="nav-de-healthcheck">De HealthCheck</button><div class="navmenu" id="nav-de-healthcheck"><a href="/healthcheck/">De HealthCheck</a><a href="/healthcheck/#doorloop">Werkwijze</a><a href="/modules/">De modules</a><a href="/rapport/">Het bevindingenrapport</a></div></div><a href="/tarieven/">Tarieven</a><div class="navgroep" data-hier="ja"><button type="button" class="navtop" aria-expanded="false" aria-controls="nav-kennisbank">Kennisbank</button><div class="navmenu" id="nav-kennisbank"><a href="/blog/" aria-current="page">Blog</a><a href="/vragen/">Veelgestelde vragen</a><a href="/praktijkvoorbeelden/">Praktijkvoorbeelden</a></div></div><a href="/over-ons/">Over ons</a></div>
    <div class="nav-actions">
      <button class="search" aria-label="Zoeken">&#8981;</button>
      <a class="btn primary" href="/triage/">Start gratis triage</a>
      <button class="menu" id="menu" aria-controls="navlinks" aria-expanded="false">Menu</button>
    </div>
  </nav>
</header>

<main id="main">
<section class="section" style="padding-bottom:70px">
  <article class="artikelpagina">

    <p class="kruimelpad"><a href="/">CloudLabs</a> / <a href="/blog/">Blog</a> / {onderwerp}</p>

    <header class="artikelkop">
      <h1>{h1}</h1>
      {ledes}
      <p class="artikelmeta">{meta}</p>
    </header>

    <div class="artikelbody">
      <nav class="toc" aria-label="Inhoud van dit artikel">
        <p class="toc-title">In dit artikel</p>
        {toc}
      </nav>

      <div class="tekst">
{tekst}
{related}
      </div>
    </div>

  </article>
</section>
</main>

<script>
(function(){{
  var menu=document.getElementById('menu'),links=document.getElementById('navlinks');
  if(menu)menu.onclick=function(){{var o=links.classList.toggle('open');menu.setAttribute('aria-expanded',o)}};
}})();
</script>
<script src="/huisstijl/pagina.js"></script>
</body>
</html>
'''

INDEX_KOP = '''<!doctype html>
<html lang="nl">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<!-- Gegenereerd met blog-omzetten.py --index. Niet met de hand bijwerken:
     draai het script opnieuw nadat er een artikel bij komt. -->
<meta name="robots" content="noindex,nofollow">
<meta name="theme-color" content="#0A1024">
<title>Blog &middot; Hyper-V, Failover Clustering en Azure Local &middot; CloudLabs</title>
<meta name="description" content="Uitleg bij bevindingen die wij in Hyper-V-, Failover Cluster- en Azure Local-omgevingen terugzien: quorum en witness, CSV-eigenaarschap, RDMA, firmware, migraties en patchrondes.">
<link rel="canonical" href="https://clustertriage.com/blog/">
<link rel="alternate" hreflang="nl" href="https://clustertriage.com/blog/">
<link rel="alternate" hreflang="x-default" href="https://clustertriage.com/blog/">
<meta property="og:type" content="website">
<meta property="og:locale" content="nl_NL">
<meta property="og:url" content="https://clustertriage.com/blog/">
<meta property="og:title" content="Blog &middot; CloudLabs">
<meta property="og:description" content="Uitleg bij de bevindingen die wij in clusters terugzien.">
<link rel="icon" href="/favicon.png" type="image/png">
<link rel="stylesheet" href="/huisstijl/pagina.css">
<link rel="stylesheet" href="/huisstijl/artikel.css">

<script type="application/ld+json">
{ld}
</script>
</head>

<body>
<a class="skip" href="#main">Naar inhoud</a>

<header class="topbar">
  <nav class="nav">
    <a class="brand" href="/preview-home.html">Cloud<span>Labs</span></a>
    <div class="navlinks" id="navlinks"><a href="/triage/">Cluster Triage</a><a href="/na-een-storing/">Na een storing</a><div class="navgroep"><button type="button" class="navtop" aria-expanded="false" aria-controls="nav-de-healthcheck">De HealthCheck</button><div class="navmenu" id="nav-de-healthcheck"><a href="/healthcheck/">De HealthCheck</a><a href="/healthcheck/#doorloop">Werkwijze</a><a href="/modules/">De modules</a><a href="/rapport/">Het bevindingenrapport</a></div></div><a href="/tarieven/">Tarieven</a><div class="navgroep" data-hier="ja"><button type="button" class="navtop" aria-expanded="false" aria-controls="nav-kennisbank">Kennisbank</button><div class="navmenu" id="nav-kennisbank"><a href="/blog/" aria-current="page">Blog</a><a href="/vragen/">Veelgestelde vragen</a><a href="/praktijkvoorbeelden/">Praktijkvoorbeelden</a></div></div><a href="/over-ons/">Over ons</a></div>
    <div class="nav-actions">
      <button class="search" aria-label="Zoeken">&#8981;</button>
      <a class="btn primary" href="/triage/">Start gratis triage</a>
      <button class="menu" id="menu" aria-controls="navlinks" aria-expanded="false">Menu</button>
    </div>
  </nav>
</header>

<main id="main">
<section class="section" style="padding-bottom:80px">
  <div class="inner">
    <p class="kruimelpad"><a href="/">CloudLabs</a> / Blog</p>
    <h1 style="font-family:var(--serif);font-weight:400;font-size:clamp(34px,5vw,58px);line-height:1.05;letter-spacing:-.022em;margin:0 0 26px;max-width:17ch">Wat wij in clusters terugzien</h1>
    <p style="font-family:var(--serif);font-size:21px;line-height:1.55;color:var(--dim);max-width:820px;margin:0 0 14px">Deze artikelen komen uit de bevindingencatalogus. Elk stuk behandelt iets dat wij in echte omgevingen tegenkomen, met de gemeten waarden erbij en de handeling die erop volgt.</p>
    <p style="font-family:var(--serif);font-size:18px;line-height:1.7;color:var(--dim);max-width:820px;margin:0 0 50px">Geen nieuwsberichten en geen productaankondigingen. Uitleg waar een clusterbeheerder de volgende patchronde iets aan heeft.</p>

    <div class="artikellijst">
{rijen}
    </div>
  </div>
</section>
</main>

<script>
(function(){{
  var menu=document.getElementById('menu'),links=document.getElementById('navlinks');
  if(menu)menu.onclick=function(){{var o=links.classList.toggle('open');menu.setAttribute('aria-expanded',o)}};
}})();
</script>
<script src="/huisstijl/pagina.js"></script>
</body>
</html>
'''

def index_bouwen():
    """Leest de omgezette artikelen en zet er een overzicht van. Herhaalbaar:
    komt er een artikel bij, dan draai je dit opnieuw."""
    posts = []
    for f in sorted(glob.glob('blog/*.html')):
        if f.endswith('index.html'):
            continue
        s = pathlib.Path(f).read_text(encoding='utf-8')
        slug = pathlib.Path(f).stem
        h1 = plat(re.search(r'<h1>(.*?)</h1>', s, re.S).group(1))
        lm = re.search(r'<p class="lede">(.*?)</p>', s, re.S)
        lede = plat(lm.group(1)) if lm else ''
        mm = re.search(r'<p class="artikelmeta">(.*?)</p>', s, re.S)
        delen = [plat(x) for x in re.findall(r'<b>(.*?)</b>', mm.group(1), re.S)] if mm else []
        datum = delen[1] if len(delen) > 1 else ''
        leestijd = delen[2] if len(delen) > 2 else ''
        onderwerp = delen[3] if len(delen) > 3 else 'Kennisbank'
        iso = re.search(r'"datePublished"\s*:\s*"([^"]+)"', s)
        posts.append({'slug': slug, 'h1': h1, 'lede': lede, 'datum': datum,
                      'leestijd': leestijd, 'onderwerp': onderwerp,
                      'iso': iso.group(1) if iso else '2026-01-01'})
    posts.sort(key=lambda p: p['iso'], reverse=True)

    rijen = []
    for p in posts:
        kort = p['lede'] if len(p['lede']) <= 190 else p['lede'][:187].rsplit(' ', 1)[0] + '...'
        rijen.append(
            f'      <a class="artikelrij" href="/blog/{p["slug"]}.html">\n'
            f'        <div class="rij-meta"><b>{html.escape(p["onderwerp"])}</b>'
            f'{html.escape(p["datum"])}<br>{html.escape(p["leestijd"])}</div>\n'
            f'        <div><h2>{html.escape(p["h1"])}</h2><p>{html.escape(kort)}</p></div>\n'
            f'      </a>')

    ld = json.dumps({"@context": "https://schema.org", "@graph": [
        {"@type": "BreadcrumbList", "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "Home", "item": "https://clustertriage.com/"},
            {"@type": "ListItem", "position": 2, "name": "Blog", "item": "https://clustertriage.com/blog/"}]},
        {"@type": "Blog", "@id": "https://clustertriage.com/blog/#blog",
         "name": "CloudLabs Blog", "inLanguage": "nl-NL",
         "description": "Uitleg bij bevindingen uit Hyper-V-, Failover Cluster- en Azure Local-metingen.",
         "publisher": {"@type": "Organization", "@id": "https://clustertriage.com/#organisatie",
                       "name": "CloudLabs", "url": "https://clustertriage.com/"},
         "blogPost": [{"@type": "BlogPosting", "headline": p['h1'],
                       "url": f"https://clustertriage.com/blog/{p['slug']}.html",
                       "datePublished": p['iso'], "articleSection": p['onderwerp'],
                       "author": {"@type": "Person", "name": "Hans Vredevoort"}} for p in posts]}]},
        ensure_ascii=False, indent=2)

    pathlib.Path('blog/index.html').write_text(
        INDEX_KOP.format(ld=ld, rijen='\n'.join(rijen)), encoding='utf-8')
    print(f"  blog/index.html gebouwd met {len(posts)} artikelen")


def main():
    if '--index' in sys.argv:
        index_bouwen()
    elif '--alles' in sys.argv:
        for f in sorted(glob.glob('blog/*.html')):
            if f.endswith('index.html'):
                continue
            pathlib.Path(f).write_text(omzetten(f), encoding='utf-8')
            print(f"  omgezet: {f}")
    elif len(sys.argv) > 1:
        uit = sys.argv[1] + '.nieuw'
        pathlib.Path(uit).write_text(omzetten(sys.argv[1]), encoding='utf-8')
        print(f"  geschreven: {uit}")
    else:
        print(__doc__)

if __name__ == '__main__':
    main()
