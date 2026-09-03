#!/usr/bin/env python3
"""CloudLabs · sync-nav.py

Zet op elke pagina van de nieuwe stijl exact hetzelfde hoofdmenu.

Waarom dit bestaat, net als sync-footer.py: het menu stond op elke pagina
apart in de HTML. Zeven losse kopieen die bij elke nieuwe pagina uit elkaar
liepen, en waarin twee pagina's onder twee verschillende namen stonden
(nav "Wat u krijgt" tegenover voettekst "Het bevindingenrapport").

Opbouw van het menu, zeven items:

    Cluster Triage      de gratis eerste stap
    Na een storing      de hoogste intentie, iemand met een cluster dat ligt
    De HealthCheck v    het onderzoek zelf, met werkwijze, modules en rapport
    Tarieven            stond alleen in de voettekst, hoort hier
    Blog                staat los in het hoofdmenu, niet weggestopt
    Kennisbank v        vragen, praktijkvoorbeelden en onderwerpen
    Over ons            stond alleen in de voettekst, hoort hier

De naam van een pagina is hier gelijk aan de naam in de voettekst. Wijkt er
iets af, pas het dan op beide plekken aan.

    python3 sync-nav.py           toont wat er zou veranderen
    python3 sync-nav.py --schrijf voert het uit
"""
import re, sys, pathlib

# (href, label) of (label, [(href, label), ...]) voor een uitklapper.
MENU_NL = [
    ('/triage/',        'Cluster Triage'),
    ('/na-een-storing/','Na een storing'),
    ('De HealthCheck', [
        ('/healthcheck/',          'De HealthCheck'),
        ('/healthcheck/#doorloop', 'Werkwijze'),
        ('/modules/',              'De modules'),
        ('/rapport/',              'Het bevindingenrapport'),
    ]),
    ('/tarieven/',      'Tarieven'),
    ('/blog/',          'Blog'),
    ('Kennisbank', [
        ('/vragen/',               'Veelgestelde vragen'),
        ('/praktijkvoorbeelden/',  'Praktijkvoorbeelden'),
        ('/onderwerpen/',           'Onderwerpen'),
    ]),
    ('/over-ons/',      'Over ons'),
]

MENU_EN = [
    ('/en/triage/',           'Cluster Triage'),
    ('/en/after-an-incident/','After an incident'),
    ('The HealthCheck', [
        ('/en/healthcheck/',          'The HealthCheck'),
        ('/en/healthcheck/#doorloop', 'How we work'),
        ('/en/modules/',              'The modules'),
        ('/en/report/',               'The findings report'),
    ]),
    ('/en/rates/',            'Rates'),
    ('/en/blog/',             'Blog'),
    ('Knowledge base', [
        ('/en/faq/',          'FAQ'),
        ('/en/case-studies/', 'Case studies'),
        ('/en/topics/',       'Topics'),
    ]),
    ('/en/about/',            'About us'),
]


def slug(label):
    return 'nav-' + re.sub(r'[^a-z]+', '-', label.lower()).strip('-')


def bouw(menu, hier):
    """hier = het pad van de pagina zelf, voor aria-current."""
    uit = ['<div class="navlinks" id="navlinks">']
    for eerste, tweede in menu:
        if isinstance(tweede, str):                       # gewone link
            nu = ' aria-current="page"' if tweede and eerste == hier else ''
            uit.append(f'<a href="{eerste}"{nu}>{tweede}</a>')
            continue
        # uitklapper. De knop draagt geen href: de pagina zelf staat als
        # eerste regel in het uitklapmenu, zodat hij met toetsenbord en op
        # een aanraakscherm net zo goed bereikbaar is.
        id_ = slug(eerste)
        binnen = any(h.split('#')[0] == hier for h, _ in tweede)
        aan = ' data-hier="ja"' if binnen else ''
        uit.append(
            f'<div class="navgroep"{aan}>'
            f'<button type="button" class="navtop" aria-expanded="false" '
            f'aria-controls="{id_}">{eerste}</button>'
            f'<div class="navmenu" id="{id_}">'
            + ''.join(
                '<a href="%s"%s>%s</a>' % (
                    h, ' aria-current="page"' if h == hier else '', t)
                for h, t in tweede)
            + '</div></div>')
    uit.append('</div>')
    return ''.join(uit)


OVERSLAAN = ('preview/', 'antithesis-backup', 'reference/', 'referentie/',
             'huisstijl/', 'test-results/')
# Gulzig tot aan nav-actions, niet zuinig: het nieuwe menu heeft geneste
# divs voor de uitklappers, dus de eerste </div> is niet het einde. Er staat
# er per pagina maar een van nav-actions, dus dit anker is eenduidig.
PATROON = re.compile(
    r'<div class="navlinks" id="navlinks">.*</div>\s*(?=<div class="nav-actions")', re.S)


def eigen_pad(p):
    s = '/' + p.as_posix()
    return s[:-len('index.html')] if s.endswith('/index.html') else s


def paginas():
    for p in sorted(pathlib.Path('.').rglob('*.html')):
        s = p.as_posix()
        if any(x in s for x in OVERSLAAN):
            continue
        if 'huisstijl/pagina.css' in p.read_text(encoding='utf-8', errors='ignore'):
            yield p


def main():
    schrijf = '--schrijf' in sys.argv
    gelijk = gewijzigd = mist = 0
    for p in paginas():
        s = p.read_text(encoding='utf-8')
        menu = MENU_EN if p.as_posix().startswith('en/') else MENU_NL
        doel = bouw(menu, eigen_pad(p))
        m = PATROON.search(s)
        if not m:
            print(f"  ! {p}: geen navlinks-blok gevonden")
            mist += 1
            continue
        if m.group(0) == doel:
            gelijk += 1
            continue
        gewijzigd += 1
        print(f"  {'bijgewerkt' if schrijf else 'zou wijzigen'}: {p}")
        if schrijf:
            p.write_text(PATROON.sub(lambda _: doel, s, count=1), encoding='utf-8')
    print(f"\n  {gelijk} al gelijk, {gewijzigd} {'bijgewerkt' if schrijf else 'te wijzigen'}"
          + (f", {mist} zonder menu" if mist else ""))
    if gewijzigd and not schrijf:
        print("  draai opnieuw met --schrijf om het door te voeren")


if __name__ == '__main__':
    main()
