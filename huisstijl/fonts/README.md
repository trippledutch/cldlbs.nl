# IBM Plex — statische WOFF2-faces, lokaal meegeleverd

De website gebruikt lokale, statische IBM Plex WOFF2-bestanden. De fonts worden
niet bij Google Fonts opgehaald en er worden geen variable-fontbestanden gebruikt.

Dat is een bewuste productiekeuze. De Google Fonts-versie van IBM Plex kan als
variable font worden geleverd: één bestand dekt dan meerdere gewichten. Bij de
HTML-naar-PDF-productie met headless Chrome bleek zo'n variable font stil te
kunnen worden geweigerd wanneer het als data-URI was ingebakken. Chrome gaf geen
bruikbare foutmelding en viel terug op een systeemfont. Het document werd dus wel
gemaakt, maar zag er niet meer exact uit zoals bedoeld.

De statische faces uit IBM's eigen repository laden wel betrouwbaar. Daarom geldt
voor CloudLabs / ClusterTriage:

- gebruik statische WOFF2-faces per gewicht;
- host die bestanden lokaal in deze map;
- geen Google Fonts-runtime-afhankelijkheid;
- geen variable IBM Plex voor productie-output;
- bij zelfstandige HTML/PDF-output mogen dezelfde statische faces als base64
  data-URI in het document worden ingebakken.

## Bron

De bestanden komen uit IBM's officiële Plex-repository, uit de `complete/woff2`
map van de betreffende familie. De bronstructuur is onder andere:

```
https://raw.githubusercontent.com/IBM/plex/master/packages/
plex-<sans|serif|mono>/fonts/complete/woff2/IBMPlex<Sans|Serif|Mono>-<gewicht>.woff2
```

De site gebruikt momenteel onder andere:

```
IBMPlexSans-400.woff2
IBMPlexSans-500.woff2
IBMPlexSans-600.woff2
IBMPlexMono-400.woff2
```

Voor de bestaande visuele stijl zijn ook statische Plex Serif-faces aanwezig.
Alle families blijven dus statisch; de keuze Sans / Serif / Mono is een
ontwerpkeuze en staat los van het technische probleem met variable fonts.

## Website versus PDF

Voor de website worden de WOFF2-bestanden als gewone lokale assets geserveerd.
Dat maakt browsercaching mogelijk en houdt de HTML klein.

Voor een zelfstandige rapport-HTML die ook zonder netwerk identiek moet renderen,
kunnen de statische WOFF2-faces rechtstreeks als base64 data-URI in de pagina
worden ingebakken. Daarmee heeft de printgang geen internetverbinding of lokaal
geïnstalleerd IBM Plex nodig.

## Controle van PDF-output

Een correcte HTML-pagina op het scherm is geen bewijs dat de juiste fonts in de
PDF terecht zijn gekomen. De betrouwbare controle is de fonttabel van de
uiteindelijke PDF zelf. De productiecontrole moet daarom verifiëren dat de
verwachte IBM Plex-faces als `/BaseFont` voorkomen en mag niet vertrouwen op een
lokaal geïnstalleerde fontfamilie.

## Licentie

IBM Plex valt onder de SIL Open Font License 1.1. Zie `OFL.txt`. De licentie moet
met de fonts meereizen. De Reserved Font Name-regels uit de licentie blijven van
toepassing.

## Bijwerken

Nieuwe of vervangende fontbestanden uitsluitend uit IBM's officiële
Plex-repository halen. Houd bestandsnaam, gewicht en `@font-face`-declaratie één
op één bij elkaar. Voeg geen Google Fonts variable font toe als vervanging voor
meerdere statische gewichten.
