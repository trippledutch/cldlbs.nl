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
 # Volgorde en naamgeving gelijk aan het hoofdmenu, zie sync-nav.py.
 '<a href="/na-een-storing/">Na een storing</a>'
 '<a href="/healthcheck/">De HealthCheck</a>'
 '<a href="/modules/">De modules</a>'
 '<a href="/rapport/">Het bevindingenrapport</a></div>'
 '<div class="footer-column"><h4>Organisatie</h4>'
 '<a href="/over-ons/">Over ons</a>'
 '<a href="/healthcheck/#doorloop">Werkwijze</a>'
 '<a href="/tarieven/">Tarieven</a>'
 # De privacyverklaring stond hier én onderin bij de juridische regel.
 # Twee keer dezelfde link in één voettekst; hij hoort onderin thuis.
 '<a href="/partners/">Voor partners</a></div>'
 '<div class="footer-column"><h4>Kennisbank</h4>'
 '<a href="/blog/">Blog</a>'
 # Praktijkvoorbeelden stond onder Organisatie. Het zijn casussen, geen
 # bedrijfsinformatie; ze horen bij de kennisbank naast de blog en de FAQ.
 '<a href="/praktijkvoorbeelden/">Praktijkvoorbeelden</a>'
 '<a href="/blog/top-10-hyper-v-cluster-issues.html">Storingen en oorzaken</a>'
 '<a href="/blog/cluster-witness-comparison.html">Quorum en witness</a>'
 '<a href="/blog/san-vs-s2d-vs-azure-local-hyper-v-storage.html">Opslag en Storage Spaces Direct</a>'
 '<a href="/vragen/">Veelgestelde vragen</a>'
 '<a href="/onderwerpen/">Onderwerpen</a></div>'
 '<div class="footer-column"><h4>Contact</h4>'
 '<a href="/triage/#aanvraag">Gratis script aanvragen</a>'
 # Veiligheid en dataverwerking wees naar /triage/#veilig, en die staat onderin
 # al als Beveiliging. Tweemaal dezelfde bestemming, en het is bovendien geen
 # manier om contact op te nemen.
 '<a href="/afspraak/#agenda">Afspraak maken</a>'
 '<a href="/contact/#bericht">Neem contact op</a></div>'
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
 # Eén regel onder het merk die zegt waar de metingen aan gedaan worden en in
 # welke talen het rapport komt. De talen staan hier gelijk aan de partner-
 # pagina en de FAQ; de taal wordt bij de intake vastgelegd en geldt voor de
 # hele opdracht.
 '<p class="footer-tagline">Onafhankelijke metingen aan Hyper-V, Failover Cluster '
 'en Azure Local omgevingen. Rapporten in het Nederlands, Engels, Duits, '
 'Spaans en Frans.</p>'
 '<p>&copy; 2026 CloudLabs</p>'
 '<div class="footer-legal"><a href="/privacy/">Privacyverklaring</a>'
 '<a href="/triage/#veilig">Beveiliging</a>'
 '<a href="/voorwaarden/">Algemene voorwaarden</a>'
 # De knop die de cookiebalk terughaalt. Op de oude site stond hij
 # rechtsboven in de kopbalk; daar is geen ruimte meer, want die is op
 # 360 breed al tot op de pixel verdeeld. Hier staat hij naast de
 # verklaring die uitlegt waar de vraag over gaat. Zie sync-cookies.py.
 '<button type="button" class="cookiebalk-open">Cookievoorkeuren</button></div></div>'
 # Twee rijen merken. Boven de platformen die gemeten worden, eronder de
 # serverhardware waarop ze draaien. Azure Stack HCI is sinds november 2024
 # hernoemd naar Azure Local; de tegel staat er onder de oude naam bij omdat
 # veel beheerders hun cluster nog zo kennen, en draagt daarom hetzelfde
 # icoon. Herkomst en voorwaarden van elk merkbestand, ook van de drie
 # hardwaremerken: assets/brands/HERKOMST.txt.
 '<div class="footer-badges">'
 '<div class="merkrij">'
 '<span class="merk-logo"><img src="/assets/brands/azure-local.svg" alt=""><b>Azure Local</b></span>'
 '<span class="merk-logo"><img src="/assets/brands/azure-local.svg" alt=""><b>Azure Stack HCI</b></span>'
 '<span class="hyperv-logo"><img src="/assets/brands/hyper-v.png" alt="Microsoft Hyper-V"></span>'
 '</div>'
 '<div class="merkrij">'
 '<span class="hardware-logo"><img src="/assets/brands/dell.svg" alt="Dell Technologies"></span>'
 '<span class="hardware-logo"><img src="/assets/brands/hpe.svg" alt="Hewlett Packard Enterprise"></span>'
 '<span class="hardware-logo"><img src="/assets/brands/lenovo.svg" alt="Lenovo"></span>'
 '</div>'
 '</div></div></footer>')

# preview/ en de backup horen bij oudere ontwerpen en blijven buiten schot.
# en/ hoort er WEL bij, maar met de Engelse voettekst hieronder. Anders lopen
# de twee talen uit elkaar, en dat is precies waar dit script voor bestaat.
OVERSLAAN = ('preview/', 'antithesis-backup', 'reference/', 'huisstijl/', 'test-results/')
PATROON = re.compile(r'<footer class="footer">.*?</footer>', re.S)

# De Engelse voettekst. Dezelfde opbouw en dezelfde volgorde als de
# Nederlandse hierboven; alleen de labels zijn vertaald. Elke link wijst nog
# naar een Nederlandse pagina en zegt dat ook met hreflang="nl", want die
# pagina's zijn de enige die er zijn.
FOOTER_EN = (
    '<footer class="footer"><div class="footer-main"><div class="footer-column"><h4>Services</h4><a href="/en/triage/">Cluster Triage</a><a href="/en/after-an-incident/">After an incident</a><a href="/en/healthcheck/">The HealthCheck</a><a href="/en/modules/">The modules</a><a href="/en/report/">The findings report</a></div><div class="footer-column"><h4>Organisation</h4><a href="/en/about/">About us</a><a href="/en/healthcheck/#doorloop">How we work</a><a href="/en/rates/">Rates</a><a href="/en/partners/">For partners</a></div><div class="footer-column"><h4>Knowledge base</h4><a href="/en/blog/">Blog</a><a href="/en/case-studies/">Case studies</a><a href="/en/blog/top-10-hyper-v-cluster-issues/">Failures and causes</a><a href="/en/blog/cluster-witness-comparison/">Quorum and witness</a><a href="/en/blog/san-vs-s2d-vs-azure-local-hyper-v-storage/">Storage and Storage Spaces Direct</a><a href="/en/faq/">FAQ</a><a href="/en/topics/">Topics</a></div><div class="footer-column"><h4>Contact</h4><a href="/en/triage/#aanvraag">Request the free script</a><a href="/en/appointment/#agenda">Book a call</a><a href="/en/contact/#bericht">Get in touch</a></div><div class="newsletter"><h4>Technical findings by email</h4><form action="#" method="post"><label><span class="skip">Email address</span><input type="email" name="email" placeholder="name@company.com" autocomplete="email"></label><button type="submit">Subscribe</button></form><p>No marketing stream. Only new findings and practical explanation.</p><div class="social-links"><a href="https://www.linkedin.com/in/hans-vredevoort" rel="noopener" aria-label="LinkedIn"><img src="/assets/icons/linkedin.svg" alt=""></a><a href="mailto:hans.vredevoort@cldlbs.com" aria-label="Email"><img src="/assets/icons/email.svg" alt=""></a><a href="/en/blog/" aria-label="Blog"><img src="/assets/icons/rss.svg" alt=""></a></div></div></div><div class="footer-lower"><div class="footer-brand"><a class="brand" href="/en/">Cloud<span>Labs</span></a><p class="footer-tagline">Independent measurements of Hyper-V, Failover Cluster and Azure Local environments. Reports in Dutch, English, German, Spanish and French.</p><p>&copy; 2026 CloudLabs</p><div class="footer-legal"><a href="/en/privacy/">Privacy statement</a><a href="/en/triage/#veilig">Security</a><a href="/en/terms/">Terms of engagement</a><button type="button" class="cookiebalk-open">Cookie preferences</button></div></div><div class="footer-badges"><div class="merkrij"><span class="merk-logo"><img src="/assets/brands/azure-local.svg" alt=""><b>Azure Local</b></span><span class="merk-logo"><img src="/assets/brands/azure-local.svg" alt=""><b>Azure Stack HCI</b></span><span class="hyperv-logo"><img src="/assets/brands/hyper-v.png" alt="Microsoft Hyper-V"></span></div><div class="merkrij"><span class="hardware-logo"><img src="/assets/brands/dell.svg" alt="Dell Technologies"></span><span class="hardware-logo"><img src="/assets/brands/hpe.svg" alt="Hewlett Packard Enterprise"></span><span class="hardware-logo"><img src="/assets/brands/lenovo.svg" alt="Lenovo"></span></div></div></div></footer>'
)

def paginas():
    # Alle niveaus, niet drie. De Engelse praktijkvoorbeelden staan vier mappen
    # diep (en/case-study/<naam>/index.html) en bleven daardoor achter met een
    # oude voettekst.
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
        doel = FOOTER_EN if p.as_posix().startswith('en/') else FOOTER
        m = PATROON.search(s)
        if m and m.group(0) == doel:
            gelijk += 1
            continue
        nieuw = PATROON.sub(lambda _: doel, s, count=1) if m else \
                s.replace('</main>', '</main>\n\n' + doel + '\n', 1)
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
