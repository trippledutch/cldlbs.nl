#!/bin/sh
# Zet de inhoudshash van pagina.css en pagina.js achter de verwijzingen in de
# HTML. Zo haalt de browser een gewijzigd bestand altijd opnieuw op, en hoeft
# niemand te weten dat hij hard moet verversen.
cd "$(dirname "$0")" || exit 1
css=$(md5 -q huisstijl/pagina.css | cut -c1-8)
js=$(md5 -q huisstijl/pagina.js  | cut -c1-8)
cyc=$(md5 -q huisstijl/cyclus.css | cut -c1-8)
# Alle pagina's, niet een handmatige lijst. Die lijst liep achter: op de blog
# en de praktijkvoorbeelden stond geen versienummer, dus daar bleef de browser
# een oude stylesheet gebruiken en leek een wijziging niet door te komen.
for f in $(find . -name "*.html" -not -path "./reference/*" -not -name "*antithesis-backup*") en/about/index.html en/after-an-incident/index.html en/appointment/index.html en/blog/aligning-vms-with-storage/index.html en/blog/azure-local-documented-flaws-exit-strategy/index.html en/blog/azure-local-migration-readiness/index.html en/blog/azure-local-vs-classic-hyper-v-cluster/index.html en/blog/cluster-aware-updating-runbook-audit-trail/index.html en/blog/cluster-witness-comparison/index.html en/blog/csv-ownership-imbalance/index.html en/blog/health-check-to-patch-night/index.html en/blog/hyper-v-time-drift-kerberos-csv/index.html en/blog/index.html en/blog/live-migration-wrong-network/index.html en/blog/reporting-remediation-progress/index.html en/blog/san-vs-s2d-vs-azure-local-hyper-v-storage/index.html en/blog/secure-boot-2023-certificates-hyper-v-gen2-vms/index.html en/blog/top-10-hyper-v-cluster-issues/index.html en/blog/vmware-to-hyper-v-migration-assessment/index.html en/blog/windows-server-2025-hyper-v-cluster-features/index.html en/case-studies/index.html en/case-study/firmware-drift-and-csv-owner-imbalance/index.html en/case-study/hardware-and-rdma-for-storage-spaces-direct/index.html en/case-study/quorum-stretch-cluster-for-rolling-upgrade/index.html en/contact/index.html en/faq/index.html en/healthcheck/index.html en/index.html en/modules/index.html en/partners/index.html en/privacy/index.html en/rates/index.html en/report/index.html en/terms/index.html en/triage/index.html; do
  [ -f "$f" ] || continue
  perl -0pi -e "s{(huisstijl/pagina\.css)(\?v=[0-9a-f]+)?}{\$1?v=$css}g; \
                s{(huisstijl/pagina\.js)(\?v=[0-9a-f]+)?}{\$1?v=$js}g; \
                s{(huisstijl/cyclus\.css)(\?v=[0-9a-f]+)?}{\$1?v=$cyc}g" "$f"
done
echo "css=$css js=$js cyclus=$cyc"
