CloudLabs huisstijl van de documentviewer
==========================================
Samengesteld 1 september 2026, voor het gelijktrekken van cldlbs.com met de
look van het bevindingenrapport.

Wat zit erin
------------
findings.css     De stylesheet van de documentviewer, ongewijzigd overgenomen
                 uit documents/docengine/html/findings.css. Dit is de bron van
                 de huisstijl: tokens, koppen, tabellen, bevindingkaarten,
                 risicochips en de A4-drukregels.
fonts.css        De @font-face-regels voor de meegeleverde fonts.
fonts/           IBM Plex Sans, Serif en Mono als woff2, zelfgehost. Zie
                 fonts/README.md voor waarom ze niet bij Google worden
                 opgehaald (druk mag niet stil terugvallen op een systeemfont)
                 en fonts/OFL.txt voor de licentie (SIL OFL 1.1; die moet
                 meereizen bij herdistributie).
stijlgids.html   Een pagina die de componenten van findings.css toont met
                 verzonnen voorbeeldinhoud. Openen in de browser naast de css;
                 ook bruikbaar als knipbron voor de site.
healthcheck.html De pagina die op cldlbs.com/healthcheck staat: dezelfde
                 huisstijl toegepast op een webpagina, met vaste kopbalk,
                 taalkeuze NL/EN/DE/ES, kort/volledig, zoom en licht/donker.
                 Zelfvoorzienend bestand; de css staat erin.
Styles.json      De gezaghebbende bron voor kleuren en vocabulaire van de
                 documentlaag (documents/Styles.json).

De drie fontrollen
------------------
Sans op de koppen en labels, Serif op de lopende tekst, Mono op meetwaarden,
codes en metaregels. Die verdeling is een besluit (27 aug 2026) en geen
toeval; zie het commentaar bovenin findings.css.

De kerntokens (lichte weergave)
-------------------------------
inkt        #0A1024     accent      #0A7E9E
grond       #FBFCFD     accentzacht #E6F2F6
oppervlak   #FFFFFF     lijn        #D3D8E0

Risicopalet (een palet voor alle oppervlakken, besluit E2, 29 jul 2026):
KRITIEK #000000 met ring #FF3B30, HOOG #E03131, MIDDEL #F76707, LAAG #1C7ED6.
Styles.json draagt deze waarden; findings.css spiegelt ze als tokens en mag
per scherm-of-drukoppervlak licht afwijken. Bij twijfel wint Styles.json.
Een thema mag de risicotokens nooit overschrijven.

Donker en druk
--------------
findings.css draagt drie standen: licht (standaard), donker (via
prefers-color-scheme en het data-theme-attribuut) en druk (A4, 22mm marge,
altijd het lichte palet, chips en accentbalken met print-color-adjust).
Wie de site herstijlt neemt die drie mee, anders valt een van de standen om.
