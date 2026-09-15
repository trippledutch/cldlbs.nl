#!/bin/sh
# Zet de inhoudshash van de gedeelde stylesheets/scripts achter de
# verwijzingen in de HTML. Zo haalt de browser een gewijzigd bestand altijd
# opnieuw op (nginx cachet /huisstijl/*.css en *.js een jaar lang als
# "immutable"), en hoeft niemand te weten dat hij hard moet verversen.
cd "$(dirname "$0")" || exit 1
css=$(md5 -q huisstijl/pagina.css | cut -c1-8)
js=$(md5 -q huisstijl/pagina.js  | cut -c1-8)
cyc=$(md5 -q huisstijl/cyclus.css | cut -c1-8)
ct=$(md5 -q huisstijl/clustertriage.css | cut -c1-8)
ct2=$(md5 -q huisstijl/clustertriage-v2.css | cut -c1-8)
storing=$(md5 -q huisstijl/storing.css | cut -c1-8)
blog=$(md5 -q huisstijl/blog.css | cut -c1-8)
fav=$(md5 -q favicon.png | cut -c1-8)
# Alle pagina's, niet een handmatige lijst: die liep eerder achter (blog en
# praktijkvoorbeelden misten een versienummer, dus een wijziging leek daar
# niet door te komen omdat de browser de oude stylesheet bleef gebruiken).
for f in $(find . -name "*.html" -not -path "./reference/*" -not -name "*antithesis-backup*"); do
  [ -f "$f" ] || continue
  perl -0pi -e "s{(huisstijl/pagina\.css)(\?v=[0-9a-f]+)?}{\$1?v=$css}g; \
                s{(huisstijl/pagina\.js)(\?v=[0-9a-f]+)?}{\$1?v=$js}g; \
                s{(huisstijl/cyclus\.css)(\?v=[0-9a-f]+)?}{\$1?v=$cyc}g; \
                s{(huisstijl/clustertriage-v2\.css)(\?v=[0-9a-f]+)?}{\$1?v=$ct2}g; \
                s{(huisstijl/clustertriage\.css)(\?v=[0-9a-f]+)?}{\$1?v=$ct}g; \
                s{(huisstijl/storing\.css)(\?v=[0-9a-f]+)?}{\$1?v=$storing}g; \
                s{(huisstijl/blog\.css)(\?v=[0-9a-f]+)?}{\$1?v=$blog}g; \
                s{(favicon\.png)(\?v=[0-9a-f]+)?}{\$1?v=$fav}g" "$f"
done
echo "favicon.png=$fav pagina.css=$css pagina.js=$js cyclus.css=$cyc clustertriage.css=$ct clustertriage-v2.css=$ct2 storing.css=$storing blog.css=$blog"
