#!/usr/bin/env python3
"""CloudLabs · sync-melding.py

Zet op elke pagina van de nieuwe stijl dezelfde meldingsbalk bovenaan.

Aanleiding: de balk stond op tien van de vierenvijftig pagina's, met vier
verschillende varianten van dezelfde zin en met verwijzingen die per pagina
anders waren (#triage, #aanvraag, triage/). Wie via een blogartikel binnenkwam
zag hem niet, terwijl dat juist iemand is die nog niet weet dat de triage
bestaat.

Twee dingen horen bij elkaar en staan daarom in hetzelfde blok:

  1. een klein script vóór de balk. Dat zet een merkteken op <html> als de
     bezoeker de balk eerder heeft weggeklikt, en de opmaak verbergt hem dan.
     Het staat er vóór, zodat de balk niet eerst een tel in beeld springt.
  2. de balk zelf, met een wortel-absolute verwijzing, zodat hij op elke pagina
     naar dezelfde plek gaat.

Het wegklikken zelf en het onthouden ervan staan in huisstijl/pagina.js.

    python3 sync-melding.py            toont wat er zou veranderen
    python3 sync-melding.py --schrijf  voert het uit
"""
import re, sys, pathlib

OVERSLAAN = ('preview/', 'antithesis-backup', 'reference/', 'huisstijl/', 'test-results/')

WACHT = ('<script>try{if(sessionStorage.getItem(\'cl-melding\'))'
         'document.documentElement.setAttribute(\'data-melding\',\'weg\')}catch(e){}</script>')

MELDING = (WACHT +
 '<div class="announcement" id="announcement">'
 '<span>Cluster down? Bewaar eerst het bewijs.</span>'
 '<a href="/triage/#aanvraag">Start gratis triage &rarr;</a>'
 '<button type="button" aria-label="Sluiten" id="close-announcement">&times;</button></div>')

MELDING_EN = (WACHT +
 '<div class="announcement" id="announcement">'
 '<span>Cluster down? Secure the evidence first.</span>'
 '<a href="/en/triage/">Start free triage &rarr;</a>'
 '<button type="button" aria-label="Close" id="close-announcement">&times;</button></div>')

# De balk met het wachtscript ervoor, in welke vorm hij ook op de pagina staat.
PATROON = re.compile(
    r'(?:<script>try\{if\((?:local|session)Storage\.getItem\(\'cl-melding\'\).*?</script>)?'
    r'\s*<div class="announcement".*?</div>', re.S)

NA_SKIP = re.compile(r'<a class="skip"[^>]*>.*?</a>', re.S)
BODY = re.compile(r'<body[^>]*>')


def paginas():
    for p in sorted(pathlib.Path('.').rglob('*.html')):
        s = p.as_posix()
        if any(x in s for x in OVERSLAAN):
            continue
        if 'huisstijl/pagina.css' in p.read_text(encoding='utf-8', errors='ignore'):
            yield p


def main():
    schrijf = '--schrijf' in sys.argv
    gelijk = gewijzigd = 0
    for p in paginas():
        s = p.read_text(encoding='utf-8')
        doel = MELDING_EN if p.as_posix().startswith('en/') else MELDING

        m = PATROON.search(s)
        if m and m.group(0) == doel:
            gelijk += 1
            continue

        if m:
            nieuw = s[:m.start()] + doel + s[m.end():]
        else:
            skip = NA_SKIP.search(s)
            if skip:
                nieuw = s[:skip.end()] + doel + s[skip.end():]
            else:
                b = BODY.search(s)
                if not b:
                    print(f"  ! {p}: geen <body> gevonden")
                    continue
                nieuw = s[:b.end()] + doel + s[b.end():]

        gewijzigd += 1
        print(f"  {'bijgewerkt' if schrijf else 'zou wijzigen'}: {p}")
        if schrijf:
            p.write_text(nieuw, encoding='utf-8')

    print(f"\n  {gelijk} al gelijk, {gewijzigd} {'bijgewerkt' if schrijf else 'te wijzigen'}")
    if gewijzigd and not schrijf:
        print("  draai opnieuw met --schrijf om het door te voeren")


if __name__ == '__main__':
    main()
