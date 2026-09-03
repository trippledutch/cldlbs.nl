#!/usr/bin/env python3
"""CloudLabs · sync-thema.py

Zet op elke pagina van de nieuwe stijl de knop voor licht of donker, en het
kleine script dat de onthouden stand aanzet voordat de pagina wordt getekend.

Hans vroeg om een donkere modus (3 september 2026). De kleuren zelf staan in
huisstijl/pagina.css en het gedrag van de knop in huisstijl/pagina.js. Alleen
deze twee dingen moeten per pagina in de HTML staan:

  1. HET WACHTSCRIPT, in de <head>. Het zet de onthouden stand op <html> nog
     voordat er iets in beeld komt. Zonder dat ziet iemand die donker heeft
     gekozen bij elke paginawissel eerst een witte flits, want pagina.js staat
     onderaan de pagina en draait pas na de eerste tekening. Hetzelfde script
     zet data-js, waarop de opmaak de knop laat zien: zonder JavaScript kan de
     knop niets, dus dan hoort hij er ook niet te staan.

     Dit is dezelfde constructie als het wachtscript van de meldingsbalk in
     sync-melding.py, en om precies dezelfde reden.

  2. DE KNOP, direct na de taalwissel. Twee keuzes over hoe je de site bekijkt
     horen naast elkaar. Er staat geen woord in de knop, alleen een zon of een
     maan; aria-label draagt de naam, in de taal van de pagina.

     Die twee staan samen in <div class="nav-keuzes">, als laatste regel van
     het menu. Waarom daar en niet meer in .nav-actions staat in sync-nav.py,
     dat het menu zet; hier hoeft alleen de knop achter de taalwissel te komen
     en dat is op beide plekken hetzelfde.

Onderweg wordt ook theme-color rechtgezet. Op acht pagina's stond daar
content="var(--ink)" en dat is geen kleur: een meta-element leest de tokens van
de opmaak niet, dus de browser deed er niets mee. De waarde is #0A1024, de
kleur van de kopbalk, en die blijft in beide standen donker.

    python3 sync-thema.py            toont wat er zou veranderen
    python3 sync-thema.py --schrijf  voert het uit
"""
import re, sys, pathlib

OVERSLAAN = ('preview/', 'antithesis-backup', 'reference/', 'referentie/',
             'huisstijl/', 'test-results/')

WACHT = ("<script>(function(d){d.setAttribute('data-js','ja');try{"
         "var t=localStorage.getItem('cl-thema');"
         "if(t==='dark'||t==='light')d.setAttribute('data-theme',t)}"
         "catch(e){}})(document.documentElement)</script>")

KNOP_NL = ('<button type="button" class="themawissel" aria-pressed="false"'
           ' aria-label="Donkere modus"></button>')
KNOP_EN = ('<button type="button" class="themawissel" aria-pressed="false"'
           ' aria-label="Dark mode"></button>')

# Het wachtscript in welke vorm het er ook staat, zodat een tweede ronde niets
# verdubbelt en een gewijzigde tekst wordt overschreven.
WACHT_PATROON = re.compile(
    r"<script>\(function\(d\)\{d\.setAttribute\('data-js'.*?</script>", re.S)
KNOP_PATROON = re.compile(r'<button type="button" class="themawissel".*?</button>', re.S)

KOP_EIND = re.compile(r'</head>')
# De taalwissel heeft twee vormen, met de eigen taal als span en de andere als
# link, in beide volgordes; daarom niet een luie .*? maar de twee labels zelf,
# anders stopt de match op de eerste </span> die binnenin staat.
NA_TAALWISSEL = re.compile(
    r'(<span class="taalwissel">'
    r'(?:<a [^>]*>[A-Z]{2}</a>|<span[^>]*>[A-Z]{2}</span>)+'
    r'</span>)')
THEME_COLOR = re.compile(r'<meta name="theme-color" content="var\(--ink\)">')


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
        s = origineel = p.read_text(encoding='utf-8')
        knop = KNOP_EN if p.as_posix().startswith('en/') else KNOP_NL

        # oude versies eruit, zodat het invoegen hieronder eenduidig is
        s = WACHT_PATROON.sub('', s)
        s = KNOP_PATROON.sub('', s)
        s = THEME_COLOR.sub('<meta name="theme-color" content="#0A1024">', s)

        m = KOP_EIND.search(s)
        if not m:
            print(f"  ! {p}: geen </head> gevonden")
            mist += 1
            continue
        s = s[:m.start()] + WACHT + s[m.start():]

        m = NA_TAALWISSEL.search(s)
        if not m:
            print(f"  ! {p}: geen taalwissel gevonden")
            mist += 1
            continue
        s = s[:m.end(1)] + knop + s[m.end(1):]

        if s == origineel:
            gelijk += 1
            continue
        gewijzigd += 1
        print(f"  {'bijgewerkt' if schrijf else 'zou wijzigen'}: {p}")
        if schrijf:
            p.write_text(s, encoding='utf-8')

    print(f"\n  {gelijk} al gelijk, {gewijzigd} {'bijgewerkt' if schrijf else 'te wijzigen'}"
          + (f", {mist} overgeslagen" if mist else ""))
    if gewijzigd and not schrijf:
        print("  draai opnieuw met --schrijf om het door te voeren")


if __name__ == '__main__':
    main()
