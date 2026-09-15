#!/usr/bin/env python3
"""CloudLabs · bouw-onderwerpen.py

Bouwt /onderwerpen/ en /en/topics/ uit de lijsten in onderwerpen-nl.py en
onderwerpen-en.py.

Dit is blok D uit het zoektermendocument van 26-08-2026: de lange staart.
Punt 2 van dat document zegt hoe zo'n regel eruit hoort te zien, namelijk de
zoekzin letterlijk als kop met daaronder een kort antwoord dat op zichzelf
klopt. Dat is precies wat hier gebeurt.

Het antwoord onder elke kop is nooit voor deze pagina geschreven. Het staat
letterlijk zo op een andere pagina van de site, en dit script weigert te
bouwen als dat niet zo is. Die controle is het hele punt: zonder die controle
sluipt er vanzelf een zin in die niemand ooit heeft gezegd.

Termen zonder bron staan bewust niet op de pagina. Het document is daar zelf
duidelijk over: als er geen bevinding, geen module en geen meting achter zit,
hoort het woord er niet. Wat er nog ontbreekt staat in BLOK-D-ONTBREEKT.md.

    python3 bouw-onderwerpen.py           controleert en toont wat het wordt
    python3 bouw-onderwerpen.py --schrijf schrijft beide pagina's

Draai daarna sync-nav.py, sync-footer.py en sync-versies.py.
"""
import re, sys, json, html, pathlib, importlib.util


def laad(bestand, naam):
    spec = importlib.util.spec_from_file_location(naam, bestand)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def plat(url):
    """De tekst van een pagina, zonder opmaak, zoals een lezer hem ziet."""
    p = pathlib.Path(url.strip('/') + '/index.html')
    if not p.exists():
        p = pathlib.Path(url.lstrip('/'))
    s = p.read_text(encoding='utf-8')
    s = re.sub(r'<script.*?</script>|<style.*?</style>', '', s, flags=re.S)
    return re.sub(r'\s+', ' ', html.unescape(re.sub('<[^>]+>', ' ', s)))


def anker(t):
    return re.sub(r'[^a-z0-9]+', '-', html.unescape(t).lower()).strip('-')


def controleer(groepen):
    """Staat elk antwoord letterlijk op de pagina waar het vandaan komt?"""
    fout = []
    for _, _, items in groepen:
        for zin, antw, bron, _ in items:
            if re.sub(r'\s+', ' ', html.unescape(antw)) not in plat(bron):
                fout.append(f'{zin}  ->  {bron}')
    return fout


def bouw(t, groepen):
    alle = [x for _, _, items in groepen for x in items]
    n = len(alle)
    wegwijzer = ''.join(f'<a href="#{sl}">{naam} ({len(i)})</a>'
                        for naam, sl, i in groepen)
    blokken = ''
    for naam, sl, items in groepen:
        rijen = ''.join(
            f'<div class="vraagblok"><h2 id="{anker(z)}">{z}</h2><p>{a}</p>'
            f'<p class="waaruit"><a href="{b}">{t["uit"]}: {bn}</a></p></div>'
            for z, a, b, bn in items)
        blokken += (f'<section class="onderwerp-blok" id="{sl}">'
                    f'<p class="onderwerp-naam">{naam}</p>'
                    f'<div class="onderwerp-vragen">{rijen}</div></section>')

    ld = {"@context": "https://schema.org", "@graph": [
        {"@type": "BreadcrumbList", "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": t['thuis'], "item": t['thuisurl']},
            {"@type": "ListItem", "position": 2, "name": t['naam'], "item": t['url']}]},
        {"@type": "CollectionPage", "@id": t['url'] + "#pagina", "url": t['url'],
         "name": t['naam'], "inLanguage": t['taal'],
         "description": t['omschrijving'].format(n=n),
         "publisher": {"@id": "https://clustertriage.com/#organisatie"}},
        {"@type": "FAQPage", "@id": t['url'] + "#vragen", "mainEntity": [
            {"@type": "Question", "name": html.unescape(z),
             "acceptedAnswer": {"@type": "Answer", "text": html.unescape(a)}}
            for z, a, _, _ in alle]},
        {"@type": "ItemList", "@id": t['url'] + "#lijst", "itemListElement": [
            {"@type": "ListItem", "position": i + 1, "name": html.unescape(z),
             "url": t['url'] + "#" + anker(z)}
            for i, (z, _, _, _) in enumerate(alle)]},
    ]}

    return f'''<!DOCTYPE html>
<html lang="{t['htmltaal']}"><head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{t['titel']}</title>
<meta name="description" content="{t['omschrijving'].format(n=n)}">
<meta name="robots" content="noindex,follow">
<link rel="canonical" href="{t['url']}">
<link rel="alternate" hreflang="nl" href="https://clustertriage.com/onderwerpen/">
<link rel="alternate" hreflang="en" href="https://clustertriage.com/en/topics/">
<link rel="alternate" hreflang="x-default" href="https://clustertriage.com/onderwerpen/">
<meta property="og:title" content="{t['titel']}">
<meta property="og:type" content="website">
<meta property="og:url" content="{t['url']}">
<link rel="icon" href="/favicon.png" type="image/png">
<link rel="stylesheet" href="/huisstijl/pagina.css">
<link rel="stylesheet" href="/huisstijl/vragen.css">
<link rel="stylesheet" href="/huisstijl/onderwerpen.css">
<script type="application/ld+json">{json.dumps(ld, ensure_ascii=False, indent=1)}</script>
</head><body>
<a class="skip" href="#main">{t['naarinhoud']}</a>
<header class="topbar"><nav class="nav">
<a class="brand" href="{t['brand']}"><b>Cloud<span>Labs</span></b><small lang="en">Decades of server expertise</small></a>
<div class="navlinks" id="navlinks"><div class="nav-keuzes"><span class="taalwissel">{t['taalwissel']}</span></div></div>
<div class="nav-actions"><a class="btn primary" href="{t['knopurl']}">{t['knop']}</a>
<button class="menu" id="menu" aria-controls="navlinks" aria-expanded="false">Menu</button></div>
</nav></header>
<main id="main">
<section class="section" style="padding-bottom:70px">
  <div class="vragenpagina">

    <p class="kruimelpad" style="margin-left:var(--inspring);font-family:var(--mono);font-size:11px;letter-spacing:.1em;text-transform:uppercase;color:var(--faint)"><a href="{t['thuispad']}" style="color:var(--faint);text-decoration:none">CloudLabs</a> / {t['naam']}</p>

    <div class="vragenkop">
      <p class="eyebrow">{t['naam']}</p>
      <h1>{t['h1']}</h1>
      <p class="inleiding">{t['inleiding']}</p>
    </div>

    <nav class="wegwijzer" aria-label="{t['naam']}">{wegwijzer}</nav>

    {blokken}

  </div>
</section>
</main>
<script src="/huisstijl/pagina.js"></script>
</body></html>
'''


NL = dict(
    naam='Onderwerpen', taal='nl-NL', htmltaal='nl',
    url='https://clustertriage.com/onderwerpen/', thuis='Home', thuisurl='https://clustertriage.com/',
    thuispad='/', brand='/preview-home.html', knopurl='/triage/', knop='Start gratis triage',
    naarinhoud='Naar inhoud', uit='Uitgewerkt in',
    taalwissel='<span aria-current="true">NL</span><a href="/en/topics/" hreflang="en" lang="en">EN</a>',
    titel='Onderwerpen &middot; wat wij meten en waar het staat &middot; CloudLabs',
    omschrijving='{n} onderwerpen uit Hyper-V, Failover Cluster en Azure Local omgevingen, van MPIO en Fibre Channel zoning tot Secure Boot en Azure Arc. Elk met een kort antwoord en de pagina waar het is uitgewerkt.',
    h1='Wat wij tegenkomen, en waar het is uitgewerkt',
    inleiding='Dit zijn onderwerpen die in Hyper-V, Failover Cluster en Azure Local omgevingen terugkomen. Elk antwoord hieronder staat letterlijk zo in het artikel of op de pagina waarnaar de regel eronder verwijst. Zoekt u iets dat er niet bij staat, stel de vraag dan gerust.')

EN = dict(
    naam='Topics', taal='en-GB', htmltaal='en',
    url='https://clustertriage.com/en/topics/', thuis='Home', thuisurl='https://clustertriage.com/en/',
    thuispad='/en/', brand='/en/', knopurl='/en/triage/', knop='Start free triage',
    naarinhoud='Skip to content', uit='Explained in',
    taalwissel='<a href="/onderwerpen/" hreflang="nl" lang="nl">NL</a><span aria-current="true">EN</span>',
    titel='Topics &middot; what we measure and where it sits &middot; CloudLabs',
    omschrijving='{n} topics from Hyper-V, Failover Cluster and Azure Local environments, from MPIO and Fibre Channel zoning to Secure Boot and Azure Arc. Each with a short answer and the page where it is worked out.',
    h1='What we run into, and where it is worked out',
    inleiding='These are topics that keep coming back in Hyper-V, Failover Cluster and Azure Local environments. Every answer below appears word for word in the article or on the page the line underneath points to. If you are looking for something that is not here, ask.')


def main():
    schrijf = '--schrijf' in sys.argv
    hier = pathlib.Path(__file__).parent
    werk = [(NL, hier / 'onderwerpen-nl.py', 'onderwerpen/index.html'),
            (EN, hier / 'onderwerpen-en.py', 'en/topics/index.html')]
    stuk = 0
    for t, lijst, doel in werk:
        groepen = laad(lijst, lijst.stem.replace('-', '_')).GROEPEN
        fout = controleer(groepen)
        n = sum(len(i) for _, _, i in groepen)
        if fout:
            stuk += len(fout)
            print(f'  {doel}: {len(fout)} antwoorden staan NIET letterlijk in hun bron')
            for f in fout:
                print('     ', f)
            continue
        print(f'  {doel}: {n} onderwerpen, alle antwoorden letterlijk in de bron')
        if schrijf:
            pathlib.Path(doel).parent.mkdir(parents=True, exist_ok=True)
            pathlib.Path(doel).write_text(bouw(t, groepen), encoding='utf-8')
            print(f'     geschreven')
    if stuk:
        print('\n  niets geschreven; herstel eerst de citaten')
        sys.exit(1)
    if not schrijf:
        print('\n  draai opnieuw met --schrijf om de pagina\'s weg te schrijven')


if __name__ == '__main__':
    main()
