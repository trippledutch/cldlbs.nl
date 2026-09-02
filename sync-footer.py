#!/usr/bin/env python3
"""CloudLabs · sync-footer.py

Zet op elke pagina van de nieuwe stijl exact dezelfde voettekst.

Aanleiding: er liepen twee varianten door elkaar, en elke nieuwe pagina bracht
er weer een eigen kopie bij. De voettekst hoort op elke pagina identiek te zijn,
dus staat hij hier op één plek en wordt hij van hieruit uitgerold.

De paden zijn wortel-absoluut (/triage/ en niet ../triage/). Dat is nodig: dit
blok moet letterlijk gelijk zijn op /, /triage/, /partners/, /over-ons/ en
/praktijkvoorbeeld/, en dat kan niet met relatieve paden.

Doelgroep: elke .html die huisstijl/pagina.css laadt. Nieuwe pagina's worden
dus vanzelf meegenomen; draai het script na elke toevoeging.

    python3 sync-footer.py          toont wat er zou veranderen
    python3 sync-footer.py --schrijf  voert het uit
"""
import re, sys, pathlib

FOOTER = (
 '<footer class="footer"><div class="footer-main">'
 '<div class="footer-column"><h4>Diensten</h4>'
 '<a href="/triage/">Cluster Triage</a>'
 '<a href="/healthcheck/">De HealthCheck</a>'
 '<a href="/healthcheck/#doorloop">Van meting naar rapport</a>'
 '<a href="/services.html">Root cause analysis</a>'
 '<a href="/partners/#modules">Modules en omgevingen</a>'
 '<a href="/rapport/">Het bevindingenrapport</a></div>'
 '<div class="footer-column"><h4>Organisatie</h4>'
 '<a href="/over-ons/">Over ons</a>'
 '<a href="/method.html">Werkwijze</a>'
 '<a href="/engagement.html">Tarieven en voorwaarden</a>'
 '<a href="/partners/">Voor partners</a>'
 '<a href="/praktijkvoorbeelden.html">Praktijkvoorbeelden</a>'
 '<a href="/privacy.html">Privacyverklaring</a></div>'
 '<div class="footer-column"><h4>Kennisbank</h4>'
 '<a href="/blog/">Blog</a>'
 '<a href="/blog/top-10-hyper-v-cluster-issues.html">Storingen en oorzaken</a>'
 '<a href="/blog/cluster-witness-comparison.html">Quorum en witness</a>'
 '<a href="/blog/san-vs-s2d-vs-azure-local-hyper-v-storage.html">Opslag en Storage Spaces Direct</a>'
 '<a href="/faq.html">Veelgestelde vragen</a></div>'
 '<div class="footer-column"><h4>Contact</h4>'
 '<a href="/triage/#aanvraag">Script aanvragen</a>'
 '<a href="/rapport/">Wat u ontvangt</a>'
 '<a href="/triage/#veilig">Veiligheid en dataverwerking</a>'
 '<a href="/afspraak/">Afspraak maken</a>'
 '<a href="/contact/">Neem contact op</a></div>'
 '<div class="newsletter"><h4>Technische bevindingen per e-mail</h4>'
 '<form action="#" method="post"><label><span class="skip">E-mailadres</span>'
 '<input type="email" name="email" placeholder="naam@bedrijf.nl" autocomplete="email"></label>'
 '<button type="submit">Aanmelden</button></form>'
 '<p>Geen marketingstroom. Alleen nieuwe bevindingen en praktische uitleg.</p>'
 '<div class="social-links">'
 '<a href="https://www.linkedin.com/in/hans-vredevoort" rel="noopener" aria-label="LinkedIn">'
 '<img src="/assets/icons/linkedin.svg" alt=""></a>'
 '<a href="mailto:hans.vredevoort@cldlbs.com" aria-label="E-mail">'
 '<img src="/assets/icons/email.svg" alt=""></a>'
 '<a href="/blog/" aria-label="Blog"><img src="/assets/icons/rss.svg" alt=""></a>'
 '</div></div></div>'
 '<div class="footer-lower"><div class="footer-brand">'
 '<a class="brand" href="/preview-home.html">Cloud<span>Labs</span></a>'
 '<p>&copy; 2026 CloudLabs</p>'
 '<div class="footer-legal"><a href="/privacy.html">Privacyverklaring</a>'
 '<a href="/triage/#veilig">Beveiliging</a>'
 '<a href="/engagement.html">Algemene voorwaarden</a></div></div>'
 '<div class="footer-badges"><span class="trust-badge">LEZEND<br>GEMETEN</span>'
 '<span class="hyperv-logo"><img src="/assets/brands/hyper-v.png" alt="Microsoft Hyper-V"></span>'
 '</div></div></footer>')

# preview/ en de backup horen bij oudere ontwerpen en blijven buiten schot
OVERSLAAN = ('preview/', 'antithesis-backup')
PATROON = re.compile(r'<footer class="footer">.*?</footer>', re.S)

def paginas():
    for p in sorted(pathlib.Path('.').glob('*.html')) + sorted(pathlib.Path('.').glob('*/*.html')):
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
        m = PATROON.search(s)
        if m and m.group(0) == FOOTER:
            gelijk += 1
            continue
        nieuw = PATROON.sub(lambda _: FOOTER, s, count=1) if m else \
                s.replace('</main>', '</main>\n\n' + FOOTER + '\n', 1)
        if nieuw == s:
            print(f"  ! {p}: geen voettekst en geen </main> gevonden")
            continue
        gewijzigd += 1
        print(f"  {'bijgewerkt' if schrijf else 'zou wijzigen'}: {p}")
        if schrijf:
            p.write_text(nieuw, encoding='utf-8')
    print(f"\n  {gelijk} al gelijk, {gewijzigd} {'bijgewerkt' if schrijf else 'te wijzigen'}")
    if gewijzigd and not schrijf:
        print("  draai opnieuw met --schrijf om het door te voeren")

if __name__ == '__main__':
    main()
