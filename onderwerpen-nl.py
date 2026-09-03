# Blok D uit het zoektermendocument. Per zoekzin een antwoord dat LETTERLIJK
# uit een bestaande pagina komt, plus de verwijzing daarheen. Niets van deze
# antwoorden is geschreven voor deze pagina; ze staan er al.
#
# (zoekzin, antwoord, bronpagina, bronnaam)
GROEPEN = [
 ("Opslag en opslagpaden", "opslag", [
  ("MPIO instellingen controleren",
   "MPIO met Round Robin op een active/passive array die sterk de voorkeur geeft aan één controller.",
   "/blog/top-10-hyper-v-cluster-issues.html", "Tien issues die we steeds vinden"),
  ("Fibre channel zoning controleren",
   "Zoning, fabricopbouw, poortstatus en padredundantie waar opslag over Fibre Channel gaat.",
   "/modules/", "De modules"),
  ("Padredundantie opslag",
   "De array zelf: firmware, pools, LUN's, hostmappings en padopbouw, naast wat de hosts aan hun kant zien.",
   "/modules/", "De modules"),
  ("Storage NIC driver verouderd",
   "Firmware-drift is onzichtbaar voor de meeste monitoring-tools, omdat de waarden in de BMC of NIC-EEPROM zitten, niet in Windows.",
   "/blog/top-10-hyper-v-cluster-issues.html", "Tien issues die we steeds vinden"),
 ]),
 ("Firmware en beheerkaarten", "firmware", [
  ("Firmware baseline cluster",
   "Oplossen: behandel firmware als configuratie. Zet een baseline (vendor solution profile van Dell, HPE of Lenovo), documenteer het in je runbook en upgrade het cluster als geheel tijdens een gepland venster.",
   "/blog/top-10-hyper-v-cluster-issues.html", "Tien issues die we steeds vinden"),
  ("iDRAC firmware versies uit de pas",
   "Hardware, firmware en BIOS-instellingen via iDRAC, iLO of XClarity; ook bruikbaar bij een node die op dat moment niet meedraait.",
   "/modules/", "De modules"),
  ("Redfish uitlezen hardware",
   "Hardware, firmware en BIOS-instellingen via iDRAC, iLO of XClarity; ook bruikbaar bij een node die op dat moment niet meedraait.",
   "/modules/", "De modules"),
 ]),
 ("Netwerk en prestaties", "netwerk", [
  ("Cluster netwerk scheiding",
   "Het cluster overweegt alleen netwerken met rol Cluster of ClusterAndClient voor intern verkeer, inclusief Live Migration.",
   "/blog/live-migration-wrong-network.html", "Live Migration over het verkeerde netwerk"),
  ("ntttcp netwerk doorvoer meten",
   "Een herhaalbare lastmeting met fio en ntttcp, alleen binnen een afgesproken onderhoudsvenster.",
   "/modules/", "De modules"),
  ("fio benchmark cluster opslag",
   "Een herhaalbare lastmeting met fio en ntttcp, alleen binnen een afgesproken onderhoudsvenster.",
   "/modules/", "De modules"),
 ]),
 ("Patchen, tijd en updates", "patchen", [
  ("CAU cluster aware updating inrichten",
   "Cluster Aware Updating heeft twee operationele modi en de keuze tussen beide is een strategische beslissing die invloed heeft op runbook, audit trail en supportbaarheid.",
   "/blog/cluster-aware-updating-runbook-audit-trail.html", "Cluster Aware Updating: runbook en audit trail"),
  ("Patchronde zonder redundantieverlies",
   "Omdat er tijdens een patchronde telkens een node uit de rotatie staat. Bij twee nodes betekent dat: \u00e9\u00e9n node draagt alles en er is geen tweede om naar uit te wijken als er in dat venster iets misgaat.",
   "/vragen/", "Veelgestelde vragen"),
  ("Time sync cluster afwijking",
   "Onder 1 seconde in steady state. Tot 5 seconden tijdens een patch-ronde of node-reboot. Boven 30 seconden is een dringend remediation-onderwerp.",
   "/blog/hyper-v-time-drift-kerberos-csv.html", "Time drift in Hyper-V clusters"),
 ]),
 ("Beveiliging, identiteit en backup", "beveiliging", [
  ("Secure Boot uitgeschakeld op host",
   "Wat hij verliest is de beveiligingsketen voor de vroege bootfase: updates voor de Windows Boot Manager, Secure Boot DB-updates, DBX-intrekkingslijst-updates en mitigaties voor toekomstige boot-niveaukwetsbaarheden van de BlackLotus-klasse (CVE-2023-24932).",
   "/blog/secure-boot-2023-certificates-hyper-v-gen2-vms.html", "Secure Boot-certificaten en Hyper-V Gen 2-VM&rsquo;s"),
  ("Generation 1 VMs migreren",
   "Bestaande VM's worden niet bijgewerkt wanneer je de host patcht, omdat hun certificaatstatus in hun eigen NVRAM zit.",
   "/blog/secure-boot-2023-certificates-hyper-v-gen2-vms.html", "Secure Boot-certificaten en Hyper-V Gen 2-VM&rsquo;s"),
  ("AD Tier 0 blootstelling",
   "Blootstelling van Tier 0 (Domain Controllers en andere kritieke identiteitsworkloads) vanaf dit cluster. Staat standaard uit en draait alleen op uw verzoek.",
   "/modules/", "De modules"),
  ("Domain controller op hetzelfde cluster",
   "Blootstelling van Tier 0 (Domain Controllers en andere kritieke identiteitsworkloads) vanaf dit cluster. Staat standaard uit en draait alleen op uw verzoek.",
   "/modules/", "De modules"),
  ("DRTM secured core server",
   "Azure Local, HCI en Storage Spaces Direct: gezondheid van pool en virtuele schijven, Network ATC-intents, Arc-connectiviteit, secured-core-status, failovermarge.",
   "/partners/", "Voor partners"),
  ("Geen backup van clustervolumes",
   "De beoordeling van backup en beheer, voorbij de aanwezigheidscontrole uit de basismeting.",
   "/modules/", "De modules"),
 ]),
 ("Azure", "azure", [
  ("Azure Arc registratie cluster",
   "Microsoft hernoemde het in november 2024 tot Azure Local en zette bestaande clusters automatisch om. Azure Arc bleef verplicht, dus er is geen onafhankelijke, niet-Azure HCI meer te koop.",
   "/blog/azure-local-vs-classic-hyper-v-cluster.html", "Klassiek Hyper-V of Azure Local?"),
  ("Azure Migrate gereedheid per VM",
   "Migratiegereedheid per virtuele machine naast wat er werkelijk draait. Alleen samen met M5.",
   "/modules/", "De modules"),
 ]),
]

# Termen uit blok D waarvoor nergens op de site of in het document van Hans
# een tekst staat. Die krijgen geen kop, want dan zou ik het antwoord zelf
# moeten verzinnen.
ZONDER_BRON = [
 "nested resiliency instellen", "resiliency achteraf wijzigen",
 "hoeveel bruikbare capaciteit bij nested mirror", "two-way mirror op twee nodes",
 "MSDSM claimt S2D disks", "jumbo frames cluster netwerk",
 "live migration CredSSP naar Kerberos", "patchronde zonder redundantieverlies",
 "VM configuratieversie verhogen", "NUMA spanning uitzetten",
 "CSV vrije ruimte te laag", "Solution Builder Extension ontbreekt",
]
