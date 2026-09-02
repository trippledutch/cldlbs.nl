# IBM Plex, meegeleverd en niet opgehaald

Zestien woff2-bestanden, latin en latin-ext, samen ongeveer 297 KB. Ze staan hier
omdat het rapport ze niet mag ophalen op het moment dat het gedrukt wordt.

## Waarom niet van Google Fonts

Gemeten op 27 augustus 2026, op het bevindingenrapport dat al bij een klant lag:

```
faces in de geleverde pdf   IBMPlexMono-Regular, IBMPlexSerif-SemiBold,
                            IBMPlexMono-Medium, Helvetica
IBM Plex Sans               ONTBREEKT
```

De lopende tekst - het grootste deel van het rapport - was teruggevallen op de
systeemletter. Het reproduceert, dus het was geen mislukte download op een
ongelukkig moment. Op dezelfde machine:

```
fc-match "IBM Plex Sans"    -> Verdana
fc-match "IBM Plex Serif"   -> Times New Roman
fc-match "IBM Plex Mono"    -> Andale Mono
```

Niets van Plex staat lokaal geinstalleerd. De pagina haalde de faces bij Google
Fonts, en waar dat niet lukt kiest de browser stil iets anders. Er komt gewoon
een pdf uit die er anders uitziet dan het scherm, en niemand ziet het.

Dat is precies het gedrag dat de docx-route NIET heeft:
check_pdf_font_guarantee weigert liever te converteren dan een stil verminderd
document af te leveren. Meeleveren geeft de html-route dezelfde eigenschap langs
een andere weg - er valt niets terug te vallen, dus de vraag komt niet op.

Een klant heeft bovendien niet altijd internet op de machine waar het rapport
wordt gedrukt, en dat is juist de situatie waarin de knop moet werken.

## Waarom latin EN latin-ext

Google splitst per tekenset en levert er 32. Cyrillisch, Grieks en Vietnamees
hebben wij niet nodig. Latin-ext wel: die draagt onder meer de Poolse, Tsjechische
en Hongaarse tekens, en die komen voor in nodenamen en klantnamen. Alleen latin
zou ongeveer 150 KB schelen en een Poolse naam laten terugvallen - Hans koos
297 KB op 27 aug 2026.

## Licentie

SIL Open Font License 1.1, zie OFL.txt. Herdistributie is toegestaan; de licentie
moet meereizen en dat is wat dat bestand hier doet. Reserved Font Name "Plex":
een gewijzigde versie mag niet meer zo heten.

## Bijwerken

De bestanden komen uit de css die Google Fonts teruggeeft voor de families en
gewichten die findings.css noemt. Verandert die lijst, dan verandert deze map
mee - en dan moet de @font-face-blok in findings.css opnieuw gegenereerd worden,
want de unicode-range hoort bij het bestand.
