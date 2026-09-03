# Blok D · wat er nog ontbreekt

Blok D uit het zoektermendocument van 26-08-2026 telt tweeëndertig termen.
Eenentwintig staan op `/onderwerpen/` en `/en/topics/`, elk met een antwoord
dat letterlijk uit een bestaande pagina komt.

Voor de elf hieronder staat nergens iets. Niet op de site, niet in de zestien
blogartikelen, niet in de drie praktijkvoorbeelden en niet in de HealthCheck-
brochure. Ze zijn daarom weggelaten in plaats van ingevuld, want het document
zegt dat zelf: *"als er geen bevinding, geen module en geen meting achter zit,
hoort het woord niet in de lijst."*

## Wat er per term nodig is

Punt 4 van het document geeft de vorm: **wat het is, waarom het risico geeft
en wat de meting laat zien.** Drie tot vijf zinnen per term is genoeg. Daarmee
komt de term op `/onderwerpen/` en, waar het een hele vraag is, ook op
`/vragen/`.

### Storage Spaces Direct · resiliency (vier termen in één keer)

Dit is met afstand de grootste winst per alinea. Eén stuk over resiliency in
S2D dekt vier blok-D-termen én de vijftiende vraag van blok G, die nu als
enige van die vijftien ontbreekt.

| Term | De vraag die beantwoord moet worden |
|---|---|
| nested resiliency instellen | Wat is nested resiliency en hoe wordt het ingesteld? |
| wanneer heb ik nested resiliency nodig | *(blok G)* Bij welk aantal nodes en welk risico is het nodig? |
| hoeveel bruikbare capaciteit bij nested mirror | Wat houdt u netto over van de ruwe capaciteit? |
| two-way mirror op twee nodes | Wat gebeurt er bij uitval van één node, en waarom is dat anders dan bij drie nodes? |
| resiliency achteraf wijzigen | Kan het resiliency-type na aanmaak nog worden gewijzigd, en zo nee, wat dan? |

### Netwerk

| Term | De vraag |
|---|---|
| jumbo frames cluster netwerk | Wanneer zetten wij jumbo frames aan, en wat gaat er mis als host en switch niet overeenkomen? |
| live migration CredSSP naar Kerberos | Waarom is CredSSP de verkeerde keuze, en wat is er nodig om naar Kerberos over te stappen? |

### Opslagpaden

| Term | De vraag |
|---|---|
| MSDSM claimt S2D disks | Wanneer gebeurt dit, waaraan herkent u het en wat is het gevolg? |
| CSV vrije ruimte te laag | Vanaf welke vrije ruimte wordt het een bevinding, en wat gaat er stuk? |

### Virtuele machines

| Term | De vraag |
|---|---|
| VM configuratieversie verhogen | Wanneer is verhogen nodig, en wat verliest u erdoor? |
| NUMA spanning uitzetten | Wanneer zetten wij dit uit, en wat is het effect op de prestaties? |

### Azure Local

| Term | De vraag |
|---|---|
| Solution Builder Extension ontbreekt | Wat is de SBE, en wat betekent het als hij ontbreekt of achterloopt? |

## Hoe het erin komt

De teksten gaan in `onderwerpen-nl.py` en `onderwerpen-en.py`, met per term de
pagina waar de volledige uitleg staat. Daarna:

    python3 bouw-onderwerpen.py --schrijf
    python3 sync-nav.py --schrijf
    python3 sync-footer.py --schrijf
    python3 sync-versies.py --schrijf

`bouw-onderwerpen.py` weigert te bouwen als een antwoord niet letterlijk op de
opgegeven bronpagina staat. Zet de tekst dus eerst op die pagina.
