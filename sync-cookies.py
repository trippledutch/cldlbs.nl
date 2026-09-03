#!/usr/bin/env python3
"""CloudLabs · sync-cookies.py

Zet op elke pagina van de nieuwe stijl de meting en de toestemmingsvraag.

Aanleiding: de oude site had allebei en de nieuwe geen van beide. Op de oude
site stond Google Analytics met Consent Mode in de <head>, een balk onderaan
die toestemming vroeg en een knop om die keuze te herzien. Bij de overstap naar
de mappenstructuur is dat blok niet meegekomen, dus was er van de nieuwe site
geen enkel bezoekcijfer.

Twee dingen horen bij elkaar en gaan daarom in één script:

  1. de meting in de <head>, met alles op denied. De tag draait dan wel maar
     slaat niets op: geen cookie, geen verkeer naar Google. Dat is de stand
     waarin iemand binnenkomt en het is ook de stand waarin hij blijft als hij
     weigert. Er hoeft dus nooit iets ongedaan gemaakt te worden.
  2. de balk onderaan, die de vraag stelt. Zonder die balk zou de meting nooit
     aangaan, en zonder de meting zou de balk nergens over gaan.

Het antwoord onthouden en de meting aanzetten staan in huisstijl/pagina.js.
De opmaak staat in huisstijl/pagina.css. De knop om de keuze te herzien staat
in de juridische regel van de voettekst en komt uit sync-footer.py.

De meting staat vlak voor </head>, dus na het scriptje dat de thema-stand zet.
Dat scriptje moet als eerste draaien, anders staat de pagina een tel in de
verkeerde stand; de meting heeft die haast niet en hangt bovendien aan async.

    python3 sync-cookies.py            toont wat er zou veranderen
    python3 sync-cookies.py --schrijf  voert het uit

Draai hierna sync-versies.py, zoals na elke wijziging aan pagina.css of
pagina.js.
"""
import re, sys, pathlib

OVERSLAAN = ('preview/', 'antithesis-backup', 'reference/', 'referentie/',
             'huisstijl/', 'test-results/')

METING = (
 # Geen padnaam in de opmerking. sync-versies.py zoekt naar huisstijl/*.js
 # en zet er een ?v= achter, ook in een opmerking, en dan staat er een
 # vingerafdruk in een zin.
 '<!-- Google tag (gtag.js) met Consent Mode v2. Alles staat op denied; het '
 'paginascript zet analytics_storage om zodra de bezoeker akkoord gaat. De '
 'drie advertentiesoorten blijven altijd geweigerd. -->'
 '<script async src="https://www.googletagmanager.com/gtag/js?id=G-BETH09PH6C"></script>'
 '<script>window.dataLayer=window.dataLayer||[];'
 'function gtag(){dataLayer.push(arguments)}'
 "gtag('consent','default',{ad_storage:'denied',ad_user_data:'denied',"
 "ad_personalization:'denied',analytics_storage:'denied',"
 "functionality_storage:'granted',security_storage:'granted',wait_for_update:500});"
 "gtag('js',new Date());"
 "gtag('config','G-BETH09PH6C',{anonymize_ip:true})</script>")

# De tekst is die van de oude site, woord voor woord. Er is één zin bij: de
# verwijzing naar de privacyverklaring, want daar staat de tabel met welke
# cookie wat doet en hoe lang hij blijft.
BALK = (
 '<div class="cookiebalk" id="cookiebalk" role="dialog" aria-live="polite" aria-label="Cookies">'
 '<div class="cookiebalk-inner">'
 '<p>Wij gebruiken Google Analytics om te zien hoe bezoekers deze site '
 'gebruiken. Analytische cookies worden alleen geplaatst als u akkoord gaat. '
 'Wat er precies wordt vastgelegd staat in de '
 '<a href="/privacy/">privacyverklaring</a>.</p>'
 '<div class="cookiebalk-knoppen">'
 '<button type="button" class="btn primary" id="cookie-ja">Accepteer analytics</button>'
 '<button type="button" class="btn ghost" id="cookie-nee">Weigeren</button>'
 '</div></div></div>')

BALK_EN = (
 '<div class="cookiebalk" id="cookiebalk" role="dialog" aria-live="polite" aria-label="Cookies">'
 '<div class="cookiebalk-inner">'
 '<p>We use Google Analytics to understand how visitors use this site. '
 'Analytics cookies are only set if you accept. What exactly is recorded is '
 'in the <a href="/en/privacy/">privacy statement</a>.</p>'
 '<div class="cookiebalk-knoppen">'
 '<button type="button" class="btn primary" id="cookie-ja">Accept analytics</button>'
 '<button type="button" class="btn ghost" id="cookie-nee">Decline</button>'
 '</div></div></div>')

# De meting zoals hij er in welke vorm ook staat, met of zonder de opmerking.
PATROON_METING = re.compile(
    r'(?:<!--\s*Google tag.*?-->)?\s*'
    r'<script async src="https://www\.googletagmanager\.com/gtag/js\?id=[^"]*"></script>\s*'
    r'<script>\s*window\.dataLayer.*?</script>', re.S)

PATROON_BALK = re.compile(r'<div class="cookiebalk"[^>]*>.*?</div></div></div>', re.S)

HEAD = re.compile(r'</head>')
# De balk komt vlak voor pagina.js te staan. Dat script leest hem uit, dus hij
# moet er dan al zijn; een balk erna zou pas bij de volgende pagina werken.
VOOR_SCRIPT = re.compile(r'<script src="(?:\.\./|/)?huisstijl/pagina\.js')


def paginas():
    for p in sorted(pathlib.Path('.').rglob('*.html')):
        if any(x in p.as_posix() for x in OVERSLAAN):
            continue
        if 'huisstijl/pagina.css' in p.read_text(encoding='utf-8', errors='ignore'):
            yield p


def main():
    schrijf = '--schrijf' in sys.argv
    gelijk = gewijzigd = 0
    for p in paginas():
        s = origineel = p.read_text(encoding='utf-8')
        doel = BALK_EN if p.as_posix().startswith('en/') else BALK

        m = PATROON_METING.search(s)
        if m:
            if m.group(0) != METING:
                s = s[:m.start()] + METING + s[m.end():]
        else:
            h = HEAD.search(s)
            if not h:
                print(f"  ! {p}: geen </head> gevonden")
                continue
            s = s[:h.start()] + METING + s[h.start():]

        b = PATROON_BALK.search(s)
        if b:
            if b.group(0) != doel:
                s = s[:b.start()] + doel + s[b.end():]
        else:
            v = VOOR_SCRIPT.search(s)
            if not v:
                print(f"  ! {p}: pagina.js niet gevonden, balk overgeslagen")
                continue
            s = s[:v.start()] + doel + s[v.start():]

        if s == origineel:
            gelijk += 1
            continue

        gewijzigd += 1
        print(f"  {'bijgewerkt' if schrijf else 'zou wijzigen'}: {p}")
        if schrijf:
            p.write_text(s, encoding='utf-8')

    print(f"\n  {gelijk} al gelijk, {gewijzigd} {'bijgewerkt' if schrijf else 'te wijzigen'}")
    if gewijzigd and not schrijf:
        print("  draai opnieuw met --schrijf om het door te voeren")


if __name__ == '__main__':
    main()
