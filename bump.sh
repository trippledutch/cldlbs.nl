#!/bin/sh
# Zet de inhoudshash van pagina.css en pagina.js achter de verwijzingen in de
# HTML. Zo haalt de browser een gewijzigd bestand altijd opnieuw op, en hoeft
# niemand te weten dat hij hard moet verversen.
cd "$(dirname "$0")" || exit 1
css=$(md5 -q huisstijl/pagina.css | cut -c1-8)
js=$(md5 -q huisstijl/pagina.js  | cut -c1-8)
cyc=$(md5 -q huisstijl/cyclus.css | cut -c1-8)
for f in preview-home.html praktijkvoorbeelden.html triage/index.html contact/index.html afspraak/index.html healthcheck/index.html; do
  [ -f "$f" ] || continue
  perl -0pi -e "s{(huisstijl/pagina\.css)(\?v=[0-9a-f]+)?}{\$1?v=$css}g; \
                s{(huisstijl/pagina\.js)(\?v=[0-9a-f]+)?}{\$1?v=$js}g; \
                s{(huisstijl/cyclus\.css)(\?v=[0-9a-f]+)?}{\$1?v=$cyc}g" "$f"
done
echo "css=$css js=$js cyclus=$cyc"
