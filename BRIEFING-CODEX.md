# CloudLabs · cldlbs.com — briefing voor de volgende bouwer

Geschreven 1 september 2026. Alles hieronder is besloten of onderzocht; wat nog
open staat, staat als vraag onderaan.

---

## 1. Wat CloudLabs verkoopt

Een **meting** en een **document**, geen adviesuren.

Hans Vredevoort (40 jaar Windows Server, oud-Microsoft MVP voor Failover
Clustering en Virtualisatie) meet Hyper-V-, Failover Cluster- en Azure
Local-omgevingen. Een PowerShell-verzamelscript draait vanaf de beheerserver van
de klant over WinRM naar de clusternodes, leest uitsluitend, installeert niets en
duurt ongeveer een kwartier. Het resultaat gaat via een versleutelde Proton-share
naar CloudLabs, waar er een rapport uit komt.

**Het onderscheidende zit in het rapport, niet in de meting.** Tussen meting en
document staan zes stappen, en stap 4 is een geautomatiseerde controle die het
document TEGENHOUDT. Die weigert een rapport waarin:

- een bevinding geen gemeten waarden bevat (geen getallen, nodenamen, datum)
- bij een hoog risico het actiepunt ontbreekt
- een tekst staat die in elk willekeurig rapport zou passen
- een onderdeel niet is beoordeeld en ook niet buiten scope is verklaard

Verder staan er twee dingen in die elders zelden staan: **wat gecontroleerd is en
in orde bleek**, en **wat niet gemeten kon worden, met de reden erbij**.

Rapporten in Nederlands, Engels en Duits, alle drie opgebouwd uit dezelfde
meting en niet achteraf vertaald.

### Doelgroep

Clusterbeheerders (45+, MCSE-achtergrond, lezen graag en lang) en hun
IT-managers, die de €5.000 moeten laten goedkeuren en het rapport doorgeven aan
hun directie. Nederland, en nadrukkelijk ook Duitsland — DACH is de grootste
Hyper-V/Azure Local-markt van Europa en de concurrentie is er dunner.

### Tarieven (definitief, uit de dienstbeschrijving v2.2)

| Vorm | Prijs |
|---|---|
| Jaarabonnement — basismeting + 3 kwartaalmetingen, elk met rapport en een uur bespreking | € 5.000 / jaar |
| Kwartaalabonnement — dezelfde vier metingen, per kwartaal gefactureerd | € 1.400 / kwartaal |
| Maandabonnement — quickcheck, alleen de bijgewerkte risicolijst | € 300 / maand |
| Eenmalige basismeting | € 1.500 |
| Module (draait mee in alle vier de metingen) | € 500 / module / cyclus |
| R1 — onderzoek na een storing, met RCA-document | € 1.600 / dag |
| R1 — aanvullende uren | € 200 / uur |
| Herstelwerk | € 175 / uur |

Modules: C1 (basismeting), M1 Ethernet switches, M2 Fibre Channel, M3 Storage
array, M4 Beheerkaarten/Redfish, M5 Azure control plane, M6 Azure Migrate,
M7 Prestatieketen *(in ontwikkeling)*, M8 Dataprotectie *(in ontwikkeling)*,
M9 Systeemdocumentatie, M10 Interviewbevindingen, M11 Maatwerk, R1 RCA,
M13 Identiteit/AD Tier 0, M14 Performance-baseline.

---

## 2. Beslissingen die vaststaan

1. **Alles is product.** Het uurtarief-aanbod verdwijnt. `engagement.html`
   ("Time and materials. No fixed-price theatre.", €165/uur) en
   `calculator.html` (rekent uren uit) spreken het nieuwe aanbod tegen en moeten
   weg of volledig om. Uren blijven alleen als tarief voor herstelwerk.
2. **Het woord "AI" komt nergens op de site.** De toolchain gebruikt het, maar
   de doelgroep leest "AI-gegenereerd rapport" als "onbetrouwbaar, verzonnen
   getallen, niemand verantwoordelijk". Verkoop het RESULTAAT: een rapport dat
   niet geproduceerd kán worden zolang een bevinding geen gemeten waarden
   bevat. Hans gebruikt het woord zelf nergens; volg dat.
3. **Drie talen, drie URL's.** Zie §5.
4. **Er is geen spoedlijn.** Wel: de klant downloadt de verzamelaar, draait hem
   zelf, vraagt een share aan, en dan wordt er met voorrang gekeken. Beloof
   nooit een responstijd in uren. De urgentie zit ergens anders — zie §6.
5. **De huisstijl is van Hans en wordt geërfd, niet gekopieerd.** Zie §3.

---

## 3. De huisstijl — `huisstijl/`

Hans heeft de huisstijl van de documentviewer aangeleverd. Die is doordacht tot
op de millimeter; lees de commentaren in `findings.css`, daar staat bij elke
keuze waarom.

```
huisstijl/
  findings.css     DE BRON. Ongewijzigd uit documents/docengine/html/.
                   Tokens, koppen, tabellen, bevindingkaarten, risicochips,
                   A4-drukregels. NIET AANPASSEN — Hans werkt hem bij.
  fonts.css        @font-face voor de tien zelfgehoste woff2's
  fonts/           IBM Plex Sans/Serif/Mono, latin + latin-ext, ~297 KB.
                   Zelfgehost omdat een PDF niet stil mag terugvallen op een
                   systeemfont; zie fonts/README.md. OFL.txt moet meereizen.
  Styles.json      Gezaghebbend voor kleuren en vocabulaire. Bij twijfel wint dit.
  stijlgids.html   Alle componenten met voorbeeldinhoud. Open hem.
  site.css         DOOR MIJ TOEGEVOEGD — wat een site nodig heeft en een
                   document niet: nav, knoppen, banden, kaarten, voettekst.
  omslag.css       DOOR MIJ TOEGEVOEGD — alleen de voorkant.
```

**Laadvolgorde: `fonts.css` → `findings.css` → `site.css` → `omslag.css`.**
`site.css` en `omslag.css` voegen toe, ze vervangen niets. Werkt Hans
`findings.css` bij, dan volgt de site vanzelf.

### De drie letterrollen (besluit 27 aug 2026)

- **Sans** (IBM Plex Sans) op koppen en labels
- **Serif** (IBM Plex Serif) op lopende tekst
- **Mono** (IBM Plex Mono) op meetwaarden, codes en metaregels

Mono betekent *machinewaarde*. Gebruik hem niet decoratief.

### Tokens (lichte stand)

```
--ink #0A1024   --dim #3A4255   --faint #6B7285   --rule #D3D8E0
--ground #FBFCFD  --surface #FFFFFF  --sunk #F4F6F9
--accent #0A7E9E  --accent-soft #E6F2F6
risico: KRITIEK #000000 (ring #FF3B30) · HOOG #E03131 · MIDDEL #F76707 · LAAG #1C7ED6
```

Drie standen: licht, donker (`prefers-color-scheme` + `data-theme`), en druk
(A4, 22 mm marge, altijd het lichte palet). **Alle drie moeten blijven werken.**
Een thema mag de risicotokens nooit overschrijven.

### Valkuilen in de cascade (kostte mij tijd, sla over)

- `findings.css` zet `table.tab td + td` in mono en rechts uit. Een kale
  `td.naam` verliest daarvan. Scope celregels als `table.tab td.naam`.
- `.front p` weegt even zwaar als één klasse plus één element. Een kale
  `.uitspraak` verliest. Schrijf `p.uitspraak`.
- ☀ en ☾ zitten niet in IBM Plex Mono. Gebruik letters of inline-SVG.

---

## 4. Wat er nu in de repo staat

**Bestaande site (root):** `index.html`, `services.html`, `method.html`,
`findings.html`, `engagement.html`, `about.html`, `book.html`, `faq.html`,
`cases.html`, `calculator.html`, `partners.html`, `blog.html` + 16 blogs.
Donkerblauw (#0a1024), cyaan accent, rasteroverlay en CRT-scanlines, genummerde
tabs (01 Home, 02 Blog). **Die stijl moet weg** — hij leest als sci-fi-dashboard
en niet als een bedrijf dat meetrapporten levert.

**Door mij toegevoegd, niet gecommit:**
- `huisstijl/` — zie §3
- `preview/index.html` — homepage-proef, `noindex`
- `preview-home.html` — oudere proef, mag weg

**Draaiende server tijdens ontwikkeling:** `python3 -m http.server 8000` in de
repo-root. De preview staat op `/preview/index.html`.

### Bekende fouten in de bestaande site

- `favicon.png` is **1,4 MB**. Moet ~5 KB zijn.
- `partners.html` staat op `noindex` en niet in de sitemap, terwijl het de
  sterkste pagina van de site is. Moet indexeerbaar worden.
- `cases.html` heeft nul interne links maar staat wél in de sitemap.
- Alle `lastmod` in `sitemap.xml` staan op 2026-05-15.
- `search-index.json` is 319 KB en wordt client-side opgehaald.
- Structured data: alleen `ProfessionalService` op de home.

---

## 5. Taalarchitectuur — de grootste SEO-fout

**Nu:** beide talen staan in hetzelfde bestand op dezelfde URL en worden met CSS
verborgen:

```css
html[data-lang="en"] [lang="nl"]{display:none}
html[data-lang="nl"] [lang="en"]{display:none}
```

Gevolgen: Google indexeert één pagina met twee talen door elkaar; `<title>` en
`<meta description>` zijn maar in één taal; de hreflang wijst `en`, `nl` én
`x-default` naar dezelfde URL en doet dus niets; Duits kan er niet bij.

**Moet worden:** `/` (NL), `/en/`, `/de/` — echte bestanden, eigen `<title>`,
eigen `<h1>`, eigen meta, en hreflang die naar elkáár wijst.

> Let op: `huisstijl/healthcheck.html` van Hans gebruikt wél de
> CSS-taalwissel (NL/EN/DE/ES). Voor een **document** is dat prima — dat staat
> op noindex. Voor de **site** niet. Zelfde visuele systeem, andere
> taalarchitectuur.

Site- en rapporttalen gelijk houden op **drie** (NL/EN/DE). De ES in de viewer
is een UI-taal, geen rapporttaal; geen Spaans verkeer trekken naar een product
dat geen Spaans rapport levert.

### Build-stap

De site moet statische HTML blijven (snel, geen framework-risico, en zowel
Google als de AI-crawlers lezen server-side HTML het best). Maar 7 pagina-typen
× 3 talen × ~40 onderwerppagina's is niet met de hand te onderhouden — nu staat
in elk van de 28 bestanden dezelfde nav, cookiebanner, analytics en footer
overgetypt.

Dus: **content in Markdown/YAML per taal + templates → gegenereerde HTML in de
repo → deployen zoals nu.** Eleventy ligt voor de hand; de repo heeft al een
halve generator in Python (`publish.py`, 887 regels: publiceren, sitemap,
JSON-LD, cross-links, sticky, IndexNow).

**Eén basis-URL als variabele.** Canonical, `og:url`, hreflang, sitemap en
robots.txt komen daaruit. Hans wil `cldlbs.nl` als staging naast `cldlbs.com`;
nu zou hij 30 bestanden met de hand moeten nalopen. Met een build krijgt een
staging-build vanzelf `noindex` en eigen canonicals.

**Hosting: nginx, eigen server.** 301-redirects zijn dus gewoon mogelijk. De 16
blog-URL's hebben opgebouwde waarde en mogen niet breken.

---

## 6. Paginastructuur (uit het zoektermendocument van Hans)

Hans heeft 125 zoekzinnen in drie talen geordend naar **intentie**, niet naar
modulenaam. Blokken A t/m G. Vertaling naar pagina's, per taal:

| Pagina | Bedient | Nu |
|---|---|---|
| Home | positionering + het verschil | bestaat, moet om |
| **HealthCheck** (het product) | blok B — koopintentie | verspreid over 3 pagina's |
| **Modules** | blok F | alleen op partners.html |
| **Na een storing** (R1/RCA) | blok A + C — hoogste betalingsbereidheid | 3 regels op services.html |
| **Het rapport** | bewijs, ankerpunt voor AI-antwoorden | findings.html komt in de buurt |
| **Partners** | blok E | bestaat, staat op noindex |
| **Vragen** (elk een eigen kop + FAQPage-schema) | blok G | faq.html, één blok |
| **Onderwerpen** — ~40 bevinding-uitleggen | blok D — de lange staart | 16 blogs |
| Over Hans | autoriteit | bestaat, is goed |

**De 324 bevindingen zijn het grootste bezit.** Niemand anders heeft 324
uitgeschreven, bewijsbare bevindingen over Hyper-V/S2D/Azure Local. Maar maak er
géén 324 dunne pagina's van — dat is een spamsignaal. Kies de **40 beste**,
600–900 woorden elk, met een echte gemeten waarde erin.

### De spoedpagina — de enige goede vondst uit dit traject

Blok A is "cluster ligt eruit": iemand met een storing, nu. Er is geen piket, dus
beloof geen responstijd. **De urgentie ligt bij het bewijs, niet bij CloudLabs:**

> Clusterlogboeken rollen door en gebeurteniskanalen lopen vol. Wie 48 uur
> wacht, heeft geen storing meer om te onderzoeken maar een rapport vol gaten.

Dus: **"Draai de verzamelaar nu. Niet omdat wij nu kijken, maar omdat het bewijs
er nu nog is."** Dat is 100% eerlijk, vereist niemand aan de kant van CloudLabs,
en geeft de man om 3 uur 's nachts één handeling. Stappen: download (statisch
bestand, werkt altijd) → draaien (leest alleen, toont eerst het plan, één
ja/nee-vraag) → share aanvragen (formulier) → wij kijken met voorrang.

**Geen publieke upload-knop.** Proton Drive kent geen blinde file request; een
map met editor-rechten laat iedereen met de link ook zien, downloaden en
verwijderen wat er al staat. Eén vaste droplink = klant A kan de clusterinventaris
van klant B downloaden. De share wordt per klant klaargezet, zoals Hans het al doet.

---

## 7. De vormgeving — vijf afgekeurde versies

**Dit is het waardevolste deel van deze briefing. Lees het voor je iets tekent.**

De opdrachtgever heeft vijf richtingen afgekeurd. De redenen zijn bruikbaar:

**1. Documentstijl** — één kolom van 52rem, serif, geen contrast, precies de
huisstijl van het rapport.
→ *"te simpel, niet professioneel"*. Terecht: het was een memo op een scherm.
Geen schaal, geen ritme, geen visuele instap.

**2. Banden** — volle stroken met wisselende gronden, grotere koppen, kaarten,
prijskaarten, screenshots van de rapporten.
→ *"ziet er goedkoop uit"*. De screenshots waren de zwakke plek: schermafdrukken
van Word-documenten, korrelig en op een telefoon onleesbaar.

**3. Levende componenten** — de bevindingkaart live gerenderd met `findings.css`
in plaats van een screenshot, cyclusfiguur en RiskTrend als getekende SVG, hero
met diepte.
→ De componenten zelf werkten goed. Maar: *"de navigatie springt naar ankers op
dezelfde pagina, dat is geen site"*. Terecht.

**4. Deeltjesveld** (naar het model van tenable.com) — bijna zwart, canvas met
~300 driftende knooppunten, verbindingen die ontstaan en verdoven, drie pulsen,
parallax op de muis, lopende meetregel, oplopende tellers.
→ *"te AI-achtig, voelt niet betrouwbaar"*. **Dit is de scherpste kritiek van het
hele traject.** Een zwevend puntennetwerk met blauwe gloed is het cliché van
AI-gegenereerde en crypto-landingspagina's, en het verwijst nergens naar. Dat is
dodelijk voor een bedrijf waarvan de belofte luidt dat een tekst die in élk
willekeurig rapport zou passen wordt geweigerd.

**5. Technische tekening** (huidige `preview/index.html`) — licht, millimeter-
papier, SVG-schema van cluster AZLCL01: vier nodes met echte namen en
firmwareversies, twee switches, een array, en de afwijking op N03 gemarkeerd met
`F01 HOOG` in rood.
→ *"ik weet het niet"*. Geen diagnose meer; vermoeidheid na vijf rondes.

### Wat hieruit te leren valt

- **Specificiteit wekt vertrouwen, decoratie niet.** Echte nodenamen,
  firmwareversies en datums werken; abstracte visuals werken niet.
- **Er is geen goed beeldmateriaal.** Rapport-screenshots zijn afgekeurd
  ("niet goed"). Stockfoto's van racks zijn niet hun hardware. Oxide werkt omdat
  daar een dure productrender staat; CloudLabs heeft niets fotogenieks.
  *Overweeg dit als eerste te laten maken:* een 3D-render of fotoshoot van de
  gedrukte rapporten. Dat deblokkeert meer dan welke CSS ook.
- **Vraag: hoe ziet de CloudLabs Studio eruit?** Runecast — de directe
  concurrent — gebruikt screenshots van hun eigen interface als hero, en dat
  werkt. Het bezwaar gold schermafdrukken van een Wórd-document. Een echt
  scherm leest heel anders. Als de Studio een toonbare interface heeft, is dat
  het beste beeldmateriaal dat er is.

### Onderzochte referenties

| Site | Wat het is | Wat je eraan hebt |
|---|---|---|
| [oxide.computer](https://oxide.computer/) | rack-scale hardware | Schermvullende productrender, kop klein en linksonder, mono-annotaties (`FIG. 1`), echte dropdown-navigatie. Mooiste referentie, maar leunt volledig op een duur beeld. |
| [tenable.com](https://www.tenable.com/) | scant infra, rapporteert — zelfde categorie | Lost "niets fotogenieks" op met een abstract gegenereerd beeld. **Wij hebben dit geprobeerd en het werd afgekeurd als te AI-achtig.** |
| [runecast.com](https://www.runecast.com/) | directe concurrent (config-audits + rapportage, nu Dynatrace) | Wit, zakelijk, **UI-screenshots als hero**. |
| [uptimeinstitute.com](https://uptimeinstitute.com/) | dé autoriteit: 4.000+ datacenters, 120+ landen, heeft zelfs een dienst "Data Center Healthcheck" | Middelmatige site met carrousels. **In deze markt komt gezag niet van webdesign.** |
| [rachfahl.de](https://www.rachfahl.de/) | scherpste concurrent (DE, Hyper-V/S2D/Azure Local, MVP sinds 2010) | Wit/blauw, teamfoto's, MVP-badges. Geen prijzen, geen rapportvoorbeelden. |
| [inspark.nl](https://www.inspark.nl) | waar Hans vroeger werkte, Microsoft Country Partner of the Year NL | Niet kopiëren: hun bewijs is institutioneel (Rijksmuseum, LUMC, 14 logo's). Met een lege logocarrousel lees je als een klein bedrijf dat zich groter voordoet. |

### Wat CloudLabs heeft dat de concurrenten niet hebben

Rachfahl, XCES en Tovey noemen **geen van drieën een bedrag**. CloudLabs kan de
hele prijsladder op de pagina zetten. Datzelfde geldt voor de moduletabel met
statuskolom, inclusief de voetnoot:

> *"In ontwikkeling betekent nog niet leverbaar; daar verkopen wij niet op vooruit."*

Dat is de zeldzaamste zin op een B2B-site. Publiceer die tabel ongewijzigd.

---

## 8. Wat te bouwen

**Fase 1 — fundering (onafhankelijk van de vormgeving):**
1. Build-stap met één basis-URL als variabele
2. Drie taal-directories met echte hreflang; 301-redirects voor de 16 blog-URL's
3. `favicon.png` terugbrengen naar ~5 KB
4. `partners.html` van `noindex` af en in de sitemap
5. `engagement.html` en `calculator.html` verwijderen of ombouwen

**Fase 2 — de kernpagina's, NL eerst** (de teksten van Hans zijn af, zie
`huisstijl/healthcheck.html`): Home, HealthCheck, Het rapport, Modules,
Na een storing, Tarieven, Vragen.

**Fase 3 — EN en DE**, geschreven en niet vertaald. Blok G verschilt per taal in
formulering: *"woran erkenne ich"* is een andere zin dan *"hoe weet ik"* en trekt
ander verkeer.

**Fase 4 — de lange staart:** ~40 onderwerppagina's uit de bevindingen, ~2 per
week. Dit is de motor en het stopt nooit.

**Fase 5 — autoriteit:** Hans' MVP-verleden, hyper-v.nu, conferenties,
gastartikelen. In een niche als deze wint een naam het van domeinautoriteit.

Realistisch: dit is een spel van 6–12 maanden. "cluster ligt eruit" wordt in
Nederland misschien twintig keer per maand getypt. De winst zit in de optelsom
van de lange staart, in AI-antwoorden die de pagina citeren, en in het
partnerkanaal.

### Niet doen

- Geen React/shadcn. shadcn is React + Tailwind + Radix, werkt niet met platte
  HTML, en zou CloudLabs bovendien op elke andere SaaS-startup laten lijken.
- Geen carrousels, nieuwsbrieven of case-sliders. Die moeten wekelijks gevoed
  worden en CloudLabs is met z'n tweeën; een stilstaande carrousel is erger dan
  geen carrousel.
- Geen stockfotografie. Geen mensen achter laptops, geen serverracks met blauwe
  lampjes.
- Geen algemene termen ("cloud", "IT-beheer", "digitale transformatie"). Hans:
  *"als er geen bevinding, geen module en geen meting achter zit, hoort het
  woord niet in de lijst."*
- `findings.css` niet aanpassen. Hans werkt hem bij; de site erft.

---

## 9. Open vragen

1. **Is het eerste kijken na een storing gratis?** Hans zou hierop terugkomen.
   Bepaalt de tekst op de spoedpagina. Advies: gratis en kort, als binnenkomer;
   het onderzoek erna is waar het geld zit.
2. **Heeft de CloudLabs Studio een toonbare interface?** Zie §7. Dit is de
   goedkoopste route naar bruikbaar beeldmateriaal.
3. **Verschil van inzicht tussen Hans en Laurens over de uitstraling?** Hans
   heeft in `findings.css` een doordachte, sobere huisstijl vastgelegd; versie 1
   was precies dat, en werd te simpel bevonden. Dat verschil is met CSS niet op
   te lossen en moet eerst besproken.
4. **InSpark als partnerklant?** Zij beheren Rijksmuseum, Gemeente Amsterdam en
   LUMC, draaien daar Hyper-V/Azure Local, en hebben niemand die een
   324-bevindingenmeting doet. Hans kent de organisatie van binnenuit. Dat is
   blok E uit het zoektermendocument (*white label cluster assessment*,
   *rapport onder eigen merk*) — extra reden om `partners.html` zichtbaar te maken.

---

## 10. Bronbestanden

- `huisstijl/healthcheck.html` — de dienstbeschrijving v2.2 van Hans, 13
  hoofdstukken, vier talen. **De teksten hieruit zijn af en mogen letterlijk de
  site op.**
- `huisstijl/stijlgids.html` — alle componenten met voorbeeldinhoud
- `huisstijl/Styles.json` — kleuren, vocabulaire, risicolabels in drie talen
- Zoektermendocument van Hans (PDF, 125 zinnen × 3 talen, blokken A–G)
- `preview/index.html` — versie 5, met commentaren waarom elke keuze zo is
