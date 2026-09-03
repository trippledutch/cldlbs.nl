#!/usr/bin/env python3
"""CloudLabs · sync-versies.py

Zet achter elke verwijzing naar een eigen stylesheet of script de vingerafdruk
van de inhoud, als ?v=<eerste acht tekens van de md5>.

Waarom: een bezoeker die er eerder was heeft pagina.css al in zijn browser
staan. Verandert dat bestand, dan haalt hij het niet opnieuw op, tenzij de
naam verandert. Dat is precies wat de ?v= doet. Stond die stempel op een oude
waarde, dan zag hij nieuwe HTML met oude opmaak, en dat is erger dan geen
stempel.

Tot nu toe werd de waarde met de hand bijgehouden, en hij was daardoor
afgedwaald: de pagina's zeiden 3d9c39cc waar het bestand c1dce568 was.

    python3 sync-versies.py           toont wat er zou veranderen
    python3 sync-versies.py --schrijf voert het uit

Draai dit als laatste, na sync-nav.py en sync-footer.py.
"""
import re, sys, hashlib, pathlib

OVERSLAAN = ('preview/', 'antithesis-backup', 'reference/', 'referentie/',
             'test-results/')
# alleen eigen bestanden; een ?v= achter iets van buiten heeft geen zin
PATROON = re.compile(r'(?P<pad>/?huisstijl/[a-z0-9-]+\.(?:css|js))(?:\?v=[0-9a-f]+)?')

vingerafdrukken = {}


def vinger(pad):
    sleutel = pad.lstrip('/')
    if sleutel not in vingerafdrukken:
        b = pathlib.Path(sleutel)
        vingerafdrukken[sleutel] = (
            hashlib.md5(b.read_bytes()).hexdigest()[:8] if b.exists() else None)
    return vingerafdrukken[sleutel]


def main():
    schrijf = '--schrijf' in sys.argv
    gelijk = gewijzigd = 0
    ontbreekt = set()

    def vervang(m):
        v = vinger(m.group('pad'))
        if v is None:
            ontbreekt.add(m.group('pad'))
            return m.group(0)
        return f"{m.group('pad')}?v={v}"

    for p in sorted(pathlib.Path('.').rglob('*.html')):
        if any(x in p.as_posix() for x in OVERSLAAN):
            continue
        s = p.read_text(encoding='utf-8')
        nieuw = PATROON.sub(vervang, s)
        if nieuw == s:
            gelijk += 1
            continue
        gewijzigd += 1
        print(f"  {'bijgewerkt' if schrijf else 'zou wijzigen'}: {p}")
        if schrijf:
            p.write_text(nieuw, encoding='utf-8')

    for pad, v in sorted(vingerafdrukken.items()):
        if v:
            print(f"  {pad}  ->  ?v={v}")
    for o in sorted(ontbreekt):
        print(f"  ! {o} bestaat niet, stempel ongemoeid gelaten")
    print(f"\n  {gelijk} al gelijk, {gewijzigd} {'bijgewerkt' if schrijf else 'te wijzigen'}")
    if gewijzigd and not schrijf:
        print("  draai opnieuw met --schrijf om het door te voeren")


if __name__ == '__main__':
    main()
