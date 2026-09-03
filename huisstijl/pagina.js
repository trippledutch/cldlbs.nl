/* CloudLabs · pagina.js · gedeeld door preview-home.html en triage.html.
   De verzendlogica komt van cldlbs.com/triage/: het formulier verstuurt zelf
   niets, de aanvraag vertrekt via de eigen WhatsApp of e-mail van de bezoeker. */

/* ---- van taal wisselen zonder je plek kwijt te raken ----------------------
   De NL/EN-knop gaat naar een andere pagina, dus begon je daar tot nu toe altijd
   weer bovenaan. Bij het klikken wordt onthouden waar je stond: het laatste blok
   met een id dat boven de leesregel begint, en hoe ver je daar doorheen was. De
   twee talen delen hun sectie-ids, dus meestal komt de vertaling van hetzelfde
   stuk in beeld. Bestaat dat id aan de andere kant niet, dan wordt dezelfde
   verhouding van de pagina aangehouden; dat scheelt nog altijd het hele eind
   terugscrollen.

   De aantekening geldt voor één pagina en één keer: alleen voor het adres waar
   de knop heen wees, en alleen binnen dertig seconden. Blijft die pagina uit,
   dan vervalt hij vanzelf.

   Dit blok staat bewust vooraan in het bestand. De beweging verderop meet bij
   het laden welke blokken in beeld staan, en die moeten de herstelde plek zien,
   anders komt de halve pagina alsnog omhoog geschoven. */
(function(){
  var SLEUTEL = 'cl-taalpositie', LEESREGEL = 140, GELDIG = 30000;

  function positie(){ return window.pageYOffset || document.documentElement.scrollTop || 0; }
  function speling(){
    var d = document.documentElement;
    return Math.max(0, Math.max(d.scrollHeight, document.body ? document.body.scrollHeight : 0)
                        - (window.innerHeight || d.clientHeight));
  }

  /* Het laatste blok dat boven de leesregel begint: daar kijk je naar. */
  function anker(y){
    var lees = y + LEESREGEL, beste = null, besteTop = -1;
    var els = document.querySelectorAll('#main [id]');
    for(var i = 0; i < els.length; i++){
      var el = els[i];
      if(!el.offsetParent && !el.offsetHeight) continue;
      var top = el.getBoundingClientRect().top + y;
      if(top <= lees && top >= besteTop){ beste = el; besteTop = top; }
    }
    return beste ? {id: beste.id, delta: Math.round(y - besteTop)} : null;
  }

  [].slice.call(document.querySelectorAll('.taalwissel a')).forEach(function(a){
    a.addEventListener('click', function(e){
      /* In een nieuw tabblad openen laat deze pagina staan; niets onthouden. */
      if(e.metaKey || e.ctrlKey || e.shiftKey || e.altKey || e.button) return;
      var y = positie();
      if(y < 40){ try{ sessionStorage.removeItem(SLEUTEL); }catch(err){} return; }
      var h = speling(), n = {naar: a.pathname, deel: h ? y / h : 0, tijd: Date.now()};
      var an = anker(y);
      if(an){ n.id = an.id; n.delta = an.delta; }
      try{ sessionStorage.setItem(SLEUTEL, JSON.stringify(n)); }catch(err){}
    });
  });

  var ruw = null;
  try{ ruw = sessionStorage.getItem(SLEUTEL); sessionStorage.removeItem(SLEUTEL); }catch(e){}
  if(!ruw || location.hash) return;
  var n;
  try{ n = JSON.parse(ruw); }catch(e){ return; }
  if(!n || n.naar !== location.pathname || Date.now() - n.tijd > GELDIG) return;

  var gezet = -1;
  function herstel(){
    var el = n.id ? document.getElementById(n.id) : null;
    var y = el ? el.getBoundingClientRect().top + positie() + (n.delta || 0)
               : n.deel * speling();
    y = Math.max(0, Math.min(Math.round(y), speling()));
    /* Niet zacht: de stylesheet zet scroll-behavior op smooth, en dan zou de
       pagina bij het openen zichtbaar naar beneden glijden. De bezoeker hoort
       gewoon te staan waar hij stond. */
    try{ window.scrollTo({top:y, left:0, behavior:'instant'}); }
    catch(e){ window.scrollTo(0, y); }
    gezet = positie();
  }
  herstel();

  /* Beelden en lettertypen kunnen de pagina hierna nog verschuiven, dus nog een
     keer als alles binnen is. Alleen als de pagina nog staat waar wij hem hebben
     gezet: is hij verschoven, dan heeft de bezoeker zelf gescrold en zou een
     tweede poging hem terugtrekken. Dat is erger dan een paar pixel verschil. */
  window.addEventListener('load', function(){
    if(Math.abs(positie() - gezet) <= 2) herstel();
  });
})();
/* ---- de zes domeinen -------------------------------------------------------
   Eén tabel voor de tabs onder "Waar de meting kijkt": kop, tekst, beeld en
   bijschrift. Er stonden hier twee schakelaars naast elkaar, een oude en een
   nieuwe; de oude wees nog naar de voorbeeldfoto's uit de referentiemap en won
   soms de race. Nu is er één, en die wijst naar onze eigen beelden. */
(function(){
  var domeinen={
    cluster:['Elke node in dezelfde werkelijkheid','Quorum, CSV\u2019s, clusterparameters en firmware worden naast elkaar gelegd. Zo worden afwijkingen zichtbaar die per server afzonderlijk niet opvallen.','assets/triage/failover-cluster.png','CLUSTER01 \u00b7 Incidentvenster'],
    storage:['Het hele opslagpad bewezen','Van fysieke disk en cache tot pool, virtuele disk en CSV: capaciteit, fouttolerantie en status worden als \u00e9\u00e9n keten beoordeeld.','assets/triage/storage-spaces-direct.png','S2D01 \u00b7 Opslagpad'],
    network:['Host en switch naast elkaar','VLAN, RDMA, PFC en fysieke poorten worden als \u00e9\u00e9n verbinding beoordeeld, inclusief verschillen tussen nodes.','assets/triage/datacenter-network.png','DC-NET \u00b7 Redundante paden'],
    hyperv:['Configuratie die verplaatsbaar blijft','Virtuele switches, live migration, NUMA, integratieservices en hostinstellingen worden onderling vergeleken.','assets/triage/hyper-v.png','HV-PROD \u00b7 Workloads'],
    azure:['Lokaal en control plane verbonden','Registratie, Arc, Azure-resource providers en lokale nodes worden in samenhang beoordeeld.','assets/triage/azure-local.png','AZLCL01 \u00b7 Control plane'],
    distributed:['Afhankelijkheden zonder blinde vlek','Clusterrollen, witnesses, beheerinterfaces en externe afhankelijkheden worden expliciet in de conclusie betrokken.','assets/triage/distributed-systems.png','RCA \u00b7 Tijdlijn en afhankelijkheden']
  };
  var view=document.getElementById('solution-view');
  if(!view) return;
  var tabs=[].slice.call(document.querySelectorAll('[data-solution]')),
      beeld=view.querySelector('img'),
      bijschrift=view.querySelector('.solution-visual span'),
      kop=view.querySelector('h3'),
      tekst=view.querySelector('p'),
      actief=null;

  /* De zes beelden worden vooraf opgehaald; zonder dat duurt de eerste keer dat
     je een domein aanwijst zo lang als het laden van de foto. Niet tijdens het
     opbouwen van de pagina, want ze zijn samen zwaar: pas als de browser niets
     te doen heeft, of eerder als de muis de lijst nadert. */
  var opgehaald=false;
  function haalop(){
    if(opgehaald) return;
    opgehaald=true;
    Object.keys(domeinen).forEach(function(k){ (new Image()).src=domeinen[k][2]; });
  }
  var lijst=document.querySelector('.solution-tabs');
  if(lijst) lijst.addEventListener('mouseenter',haalop);
  if(window.requestIdleCallback) requestIdleCallback(haalop,{timeout:4000});
  else setTimeout(haalop,2000);

  /* Alles wisselt in dezelfde stap. Hier stond een pauze van 130 milliseconden
     waarin het beeld op onzichtbaar stond; dat was precies de vertraging die je
     voelde als je snel langs de lijst ging. */
  function toon(tab){
    var z=domeinen[tab.dataset.solution];
    if(!z || tab===actief) return;
    actief=tab;
    tabs.forEach(function(x){x.setAttribute('aria-selected',x===tab?'true':'false')});
    kop.textContent=z[0];
    tekst.textContent=z[1];
    beeld.src=z[2];
    beeld.alt=z[0];
    if(bijschrift) bijschrift.textContent=z[3];
  }

  /* Met de muis erover is genoeg; klikken en tabben blijven werken. Op een
     aanraakscherm gebeurt er niets: daar is alleen de tik een keuze. */
  var muis = window.matchMedia && matchMedia('(hover:hover)').matches;
  tabs.forEach(function(tab){
    tab.onclick=function(){ toon(tab); };
    tab.addEventListener('focus',function(){ toon(tab); });
    if(muis) tab.addEventListener('mouseenter',function(){ toon(tab); });
  });

  var eerste=tabs.filter(function(x){return x.getAttribute('aria-selected')==='true'})[0];
  if(eerste) actief=eerste;
})();
(function(){var sluit=document.getElementById('close-announcement'),melding=document.getElementById('announcement');if(sluit&&melding)sluit.onclick=function(){melding.remove();try{sessionStorage.setItem('cl-melding','1')}catch(e){}};var menu=document.getElementById('menu'),links=document.getElementById('navlinks');if(menu&&links)menu.onclick=function(){var o=links.classList.toggle('open');menu.setAttribute('aria-expanded',o?'true':'false')};var rs=[].slice.call(document.querySelectorAll('.reveal'));if(!('IntersectionObserver'in window)||matchMedia('(prefers-reduced-motion:reduce)').matches){rs.forEach(function(x){x.classList.add('in')})}else{var io=new IntersectionObserver(function(es){es.forEach(function(e){if(e.isIntersecting){e.target.classList.add('in');io.unobserve(e.target)}})},{threshold:.08});rs.forEach(function(x){io.observe(x)})}})();
/* ---- de aanvraag versturen ------------------------------------------------
   Eén op één overgenomen van cldlbs.com/triage/. Het bericht wordt hier
   opgebouwd en meegegeven aan WhatsApp of aan de mailclient van de bezoeker;
   de pagina verstuurt en bewaart zelf niets. */
(function(){
  var F = document.getElementById('triageform');
  if(!F) return;
  function bericht(){
    if(!F.reportValidity()) return null;
    var v = function(n){ return F.elements[n].value.trim(); };
    return 'Cluster Triage aanvraag'
      + '\nNaam: '     + v('voornaam') + ' ' + v('achternaam')
      + '\nBedrijf: '  + v('bedrijf')
      + '\nE-mail: '   + v('email')
      + '\nTelefoon: ' + v('telefoon')
      + '\nLand: '     + v('land')
      + '\nCluster: '  + v('cluster')
      + '\nIncident: ' + v('uren') + ' uur geleden';
  }
  var wa=document.getElementById('knop-wa'), mail=document.getElementById('knop-mail');
  if(!wa || !mail) return;
  wa.addEventListener('click', function(){
    var b = bericht(); if(b === null) return;
    window.open('https://wa.me/66991461761?text=' + encodeURIComponent(b), '_blank', 'noopener');
  });
  mail.addEventListener('click', function(){
    var b = bericht(); if(b === null) return;
    location.href = 'mailto:hans@cldlbs.com,rob@cldlbs.com?subject='
      + encodeURIComponent('Cluster Triage') + '&body=' + encodeURIComponent(b);
  });
})();

/* Het berichtformulier op de contactpagina. Zelfde werkwijze als de aanvraag:
   de tekst wordt opgebouwd en meegegeven aan WhatsApp of aan de mailclient van
   de bezoeker. De pagina verstuurt en bewaart zelf niets. */
(function(){
  var F = document.getElementById('contactform');
  if(!F) return;
  var wa = document.getElementById('contact-wa'), mail = document.getElementById('contact-mail');
  if(!wa || !mail) return;
  function bericht(){
    if(!F.reportValidity()) return null;
    var v = function(n){ return F.elements[n].value.trim(); };
    return 'Bericht via cldlbs.com'
      + '\nNaam: '      + v('voornaam') + ' ' + v('achternaam')
      + '\nBedrijf: '   + v('bedrijf')
      + '\nE-mail: '    + v('email')
      + '\nTelefoon: '  + (v('telefoon') || 'niet opgegeven')
      + '\nOnderwerp: ' + v('onderwerp')
      + '\n\n'          + v('bericht');
  }
  wa.addEventListener('click', function(){
    var b = bericht(); if(b === null) return;
    window.open('https://wa.me/66991461761?text=' + encodeURIComponent(b), '_blank', 'noopener');
  });
  mail.addEventListener('click', function(){
    var b = bericht(); if(b === null) return;
    location.href = 'mailto:hans.vredevoort@cldlbs.com?subject='
      + encodeURIComponent(F.elements['onderwerp'].value.trim() || 'Bericht via cldlbs.com')
      + '&body=' + encodeURIComponent(b);
  });
})();

/* Voorkeursmomenten op de afspraakpagina. Zelfde werkwijze als de andere twee
   formulieren: de pagina verstuurt en bewaart zelf niets. */
(function(){
  var F = document.getElementById('afspraakform');
  if(!F) return;
  var wa = document.getElementById('afspraak-wa'), mail = document.getElementById('afspraak-mail');
  if(!wa || !mail) return;
  function bericht(){
    if(!F.reportValidity()) return null;
    var v = function(n){ return F.elements[n].value.trim(); };
    return 'Afspraakverzoek via cldlbs.com'
      + '\nNaam: '      + v('voornaam') + ' ' + v('achternaam')
      + '\nBedrijf: '   + v('bedrijf')
      + '\nE-mail: '    + v('email')
      + '\nTelefoon: '  + (v('telefoon') || 'niet opgegeven')
      + '\nOnderwerp: ' + v('onderwerp')
      + '\nTijdzone: '  + v('tijdzone')
      + '\nMomenten: '  + v('momenten')
      + (v('toelichting') ? '\n\nOmgeving: ' + v('toelichting') : '');
  }
  wa.addEventListener('click', function(){
    var b = bericht(); if(b === null) return;
    window.open('https://wa.me/66991461761?text=' + encodeURIComponent(b), '_blank', 'noopener');
  });
  mail.addEventListener('click', function(){
    var b = bericht(); if(b === null) return;
    location.href = 'mailto:hans.vredevoort@cldlbs.com?subject='
      + encodeURIComponent('Afspraak: ' + F.elements['onderwerp'].value.trim())
      + '&body=' + encodeURIComponent(b);
  });
})();

/* De partnerbriefing op /partners/. Hier stond alleen een mailto-knop, en die
   levert een leeg bericht op waar niets in staat wat wij nodig hebben. Zelfde
   werkwijze als de andere drie formulieren: de tekst wordt hier opgebouwd en
   meegegeven aan WhatsApp of aan de mailclient van de bezoeker. De pagina
   verstuurt en bewaart zelf niets.

   Het bericht is Nederlands, ook op de Engelse pagina. Dat is bewust en gelijk
   aan de andere formulieren: het gaat naar dezelfde postbus. */
(function(){
  var F = document.getElementById('partnerform');
  if(!F) return;
  var wa = document.getElementById('partner-wa'), mail = document.getElementById('partner-mail');
  if(!wa || !mail) return;
  function bericht(){
    if(!F.reportValidity()) return null;
    var v = function(n){ return F.elements[n].value.trim(); };
    return 'Partnerbriefing aanvraag'
      + '\nNaam: '      + v('voornaam') + ' ' + v('achternaam')
      + '\nBedrijf: '   + v('bedrijf')
      + '\nE-mail: '    + v('email')
      + '\nTelefoon: '  + (v('telefoon') || 'niet opgegeven')
      + '\nOnderwerp: ' + v('onderwerp')
      + '\nClusters: '  + (v('clusters') || 'niet opgegeven')
      + (v('toelichting') ? '\n\n' + v('toelichting') : '');
  }
  wa.addEventListener('click', function(){
    var b = bericht(); if(b === null) return;
    window.open('https://wa.me/66991461761?text=' + encodeURIComponent(b), '_blank', 'noopener');
  });
  mail.addEventListener('click', function(){
    var b = bericht(); if(b === null) return;
    location.href = 'mailto:hans.vredevoort@cldlbs.com?subject='
      + encodeURIComponent('Partnerbriefing CloudLabs') + '&body=' + encodeURIComponent(b);
  });
})();

/* Vragen die openklappen zodra de muis erover gaat. Een klik zet de vraag vast,
   zodat hij open blijft als de muis weggaat; nog een klik maakt hem weer los.
   Op een apparaat zonder muis valt de zweefbeweging weg en blijft de klik over.

   Twee dingen die eerder misgingen:

   1. Openen en sluiten lazen de stand uit d.open, maar bij het sluiten stond
      die pas aan het eind van de animatie op false. Ging de muis er tijdens
      het dichtklappen weer overheen, dan zag openen() de vraag nog als open en
      deed niets, terwijl de animatie gewoon doorliep en hem alsnog sloot. De
      vraag was daarna niet meer te openen: dat was het vastlopen. Er is nu een
      eigen doelstand die meteen omslaat.

   2. De stand hing aan onfinish van de animatie. Wordt die afgebroken of loopt
      hij niet, dan bleef de vraag open staan. De tijdmeter bepaalt nu de stand
      en de animatie is alleen nog het zichtbare deel. */
(function(){
  var items = [].slice.call(document.querySelectorAll('.faq-item'));
  if(!items.length) return;
  var zweeft = window.matchMedia('(hover:hover)').matches;
  var rustig = window.matchMedia('(prefers-reduced-motion:reduce)').matches;
  var soepel = 'cubic-bezier(.4,0,.2,1)';
  var UIT = 240, IN = 190;

  items.forEach(function(d){ d.doel = d.open ? 'open' : 'dicht'; });

  function stop(d){
    if(d.beweging){ d.beweging.cancel(); d.beweging = null; }
    if(d.klok){ clearTimeout(d.klok); d.klok = null; }
  }

  function openen(d){
    if(d.doel === 'open') return;
    d.doel = 'open';
    stop(d);
    d.open = true;
    var v = d.querySelector('.faq-antwoord');
    if(rustig || !v || !v.animate) return;
    d.beweging = v.animate([{height:'0px',opacity:0},
                            {height:v.scrollHeight + 'px',opacity:1}],
                           {duration:UIT, easing:soepel});
  }

  function sluiten(d){
    if(d.doel === 'dicht') return;
    d.doel = 'dicht';
    stop(d);
    var v = d.querySelector('.faq-antwoord');
    if(rustig || !v || !v.animate){ d.open = false; return; }
    d.beweging = v.animate([{height:v.scrollHeight + 'px',opacity:1},
                            {height:'0px',opacity:0}],
                           {duration:IN, easing:soepel});
    d.klok = setTimeout(function(){
      d.klok = null;
      if(d.doel === 'dicht') d.open = false;
    }, IN);
  }

  function sluitRest(behalve){
    items.forEach(function(a){
      if(a !== behalve && !a.hasAttribute('data-vast')) sluiten(a);
    });
  }

  items.forEach(function(d){
    var kop = d.querySelector('summary');
    if(!kop) return;

    kop.addEventListener('click', function(e){
      e.preventDefault();
      var vast = d.hasAttribute('data-vast');
      items.forEach(function(a){ a.removeAttribute('data-vast'); });
      items.forEach(function(a){ if(a !== d) sluiten(a); });
      if(vast){ sluiten(d); }
      else { d.setAttribute('data-vast',''); openen(d); }
    });

    if(!zweeft) return;

    /* Bewust mousemove op de vraagregel en niet mouseenter op het hele blok.
       Een openklappend antwoord duwt de vragen eronder omlaag, en dan schuift
       er een ander blok onder de stilstaande muis door. Dat vuurt mouseenter af
       zonder dat de bezoeker iets doet, waarna openen en sluiten elkaar
       afwisselen. mousemove gaat alleen af als de muis zelf beweegt. */
    kop.addEventListener('mousemove', function(){
      if(d.doel === 'open') return;
      sluitRest(d);
      openen(d);
    });
  });

  /* Sluiten bij het verlaten van de hele lijst, niet per vraag: zo blijft een
     antwoord open terwijl de muis er doorheen naar beneden gaat. */
  items[0].parentNode.addEventListener('mouseleave', function(){
    items.forEach(function(a){ if(!a.hasAttribute('data-vast')) sluiten(a); });
  });
})();

/* ---- beweging die iets betekent -----------------------------------------
   Drie stukken, alle drie gebonden aan wat er op dat moment gebeurt:
   de kopbalk die zich losmaakt van de hero zodra je scrolt, de staven die
   oplopen alsof de meting draait, en de triageregels die na elkaar binnenkomen.
   Alles slaat over bij prefers-reduced-motion, en alles staat zonder deze code
   gewoon op zijn eindstand. */
(function(){
  var rustig = window.matchMedia('(prefers-reduced-motion:reduce)').matches;
  var wortel = document.documentElement;

  /* De kopbalk is doorzichtig zolang je bovenaan een donkere hero staat, en
     wordt vast zodra er inhoud onder hem door schuift. */
  (function(){
    if(!document.querySelector('.topbar')) return;
    var eerste = document.querySelector('#main > *');
    if(eerste && eerste.classList.contains('hero')) wortel.setAttribute('data-hero','');
    var aan = null, wacht = false;
    function meet(){
      wacht = false;
      var nu = (window.pageYOffset || wortel.scrollTop) > 24;
      if(nu === aan) return;
      aan = nu;
      if(nu) wortel.setAttribute('data-gescrold',''); else wortel.removeAttribute('data-gescrold');
    }
    meet();
    window.addEventListener('scroll', function(){
      if(!wacht){ wacht = true; requestAnimationFrame(meet); }
    }, {passive:true});
  })();

  if(rustig || !window.IntersectionObserver || !document.body.animate) return;

  /* Deze twee lopen wél bij het laden, ook als ze al in beeld staan. Ze beelden
     de meting zelf uit: de staven die oplopen en de triagelijst die volloopt.
     Dat is geen opkomst van de opmaak maar de inhoud die zich opbouwt, en het
     is het enige bewegende deel boven de vouw. */
  function eenmalig(el, doe){
    var io = new IntersectionObserver(function(rijen){
      rijen.forEach(function(r){
        if(!r.isIntersecting) return;
        io.unobserve(r.target);
        doe(r.target);
      });
    }, {threshold:.25});
    io.observe(el);
  }

  /* De staven lopen op vanaf de basislijn, zwaarste eerst. */
  var staafblok = document.querySelector('.bars');
  if(staafblok) eenmalig(staafblok, function(blok){
    [].slice.call(blok.querySelectorAll('.bar')).forEach(function(staaf, n){
      staaf.animate([{transform:'scaleY(0)'},{transform:'scaleY(1)'}],
        {duration:620, delay:n*90, easing:'cubic-bezier(.22,1,.36,1)',
         fill:'backwards', composite:'replace'});
    });
  });

  /* De triageregels komen na elkaar binnen, zoals een lijst die volloopt. */
  var lijst = document.querySelector('.triage-list');
  if(lijst) eenmalig(lijst, function(blok){
    [].slice.call(blok.querySelectorAll('.triage-finding')).forEach(function(regel, n){
      regel.animate([{opacity:0, transform:'translateY(9px)'},
                     {opacity:1, transform:'none'}],
        {duration:420, delay:120 + n*95, easing:'cubic-bezier(.22,1,.36,1)', fill:'backwards'});
    });
  });
})();

/* ---- dezelfde beweging over de hele site ---------------------------------
   Blokken komen bij het in beeld schuiven één keer omhoog en aan. Binnen een
   rij lopen ze na elkaar, zodat drie kaarten naast elkaar niet als één blok
   verschijnen.

   Bewust geen IntersectionObserver maar een eigen meting op scroll. De
   waarnemer bleek bij snel doorscrollen blokken over te slaan, en dan blijft
   inhoud onzichtbaar staan. Dat risico is hier niet acceptabel: liever een
   berekening die bij elke scrollbeweging opnieuw kijkt.

   De begintoestand wordt pas gezet als deze code draait: data-beweegt op <html>
   schakelt de regels in de stylesheet in. Zonder JavaScript, of bij
   prefers-reduced-motion, staat alles gewoon zichtbaar. */
(function(){
  if(window.matchMedia('(prefers-reduced-motion:reduce)').matches) return;

  var KIES = ['.section-head','.benefit','.proof-item','.feature','.story','.topic',
              '.scope-card','.kaart','.cred','.platform-panel','.solution-view',
              '.intro-inner','.aanvraag','.faq-blok','.waarborgen','.slotregel',
              '.leesnoot','.cal-frame','.footer-column','.newsletter','.antwoord',
              '.artikelrij','.gebied','.module','.rij','.figuur','.doc','.gate'].join(',');

  var wacht = [].slice.call(document.querySelectorAll(KIES))
    .filter(function(el){ return !el.closest('.hero'); });
  if(!wacht.length) return;

  document.documentElement.setAttribute('data-beweegt','');

  /* Volgnummer binnen de eigen rij, voor het na elkaar oplopen. */
  var teller = new Map();
  wacht.forEach(function(el){
    var ouder = el.parentNode;
    var n = teller.get(ouder) || 0;
    teller.set(ouder, n + 1);
    el.classList.add('op');
    if(n) el.style.transitionDelay = Math.min(n, 5) * 70 + 'ms';
  });

  /* Wat bij het laden al in beeld staat hoort er gewoon te staan. Anders
     schuift bij elke verversing de halve pagina omhoog, en dat leest als een
     truc in plaats van als beweging die ergens over gaat.

     De beginfase eindigt bij de eerste scrollbeweging en niet na een vast
     aantal milliseconden. Een tijdgrens verliep op een trage pagina voordat de
     opmaak klaar was, waarna een blok dat gewoon in beeld stond alsnog bewoog.
     Zonder scrollen komt er ook niets nieuws in beeld, dus dit kan niet
     doorslaan naar de andere kant. */
  var beginfase = true;
  function voorbijBegin(){ beginfase = false; }

  function toon(el, meteen){
    if(meteen || beginfase) el.classList.add('meteen');
    el.classList.add('in');
    var k = wacht.indexOf(el);
    if(k > -1) wacht.splice(k, 1);
  }

  /* Twee onafhankelijke aanleidingen, want geen van beide is alleen betrouwbaar
     genoeg: een eigen meting op scroll, en daarnaast een waarnemer. Wat het
     eerst afgaat wint; toon() kan zonder bezwaar twee keer langskomen. Blijft
     een blok onzichtbaar staan, dan is de pagina stuk, en dat weegt zwaarder
     dan een dubbele controle. */
  function kijk(){
    var hoog = window.innerHeight || document.documentElement.clientHeight;
    if(!hoog) return;                       /* nog geen afmeting: later opnieuw */
    var grens = hoog * 0.94;
    wacht.slice().forEach(function(el){
      var r = el.getBoundingClientRect();
      if(r.bottom <= 0) toon(el, true);      /* al voorbijgescrold */
      else if(r.top < grens) toon(el);
    });
    if(!wacht.length){
      window.removeEventListener('scroll', kijk);
      window.removeEventListener('resize', kijk);
    }
  }

  window.addEventListener('scroll', voorbijBegin, {passive:true});
  window.addEventListener('scroll', kijk, {passive:true});
  window.addEventListener('resize', kijk);
  window.addEventListener('load', kijk);
  setTimeout(kijk, 0);
  setTimeout(kijk, 250);
  kijk();

  if(window.IntersectionObserver){
    var io = new IntersectionObserver(function(rijen){
      rijen.forEach(function(r){
        if(r.isIntersecting){ io.unobserve(r.target); toon(r.target); }
      });
    }, {threshold:0, rootMargin:'0px 0px -6% 0px'});
    wacht.slice().forEach(function(el){ io.observe(el); });
  }
})();

/* ---- de hulpkaart ---------------------------------------------------------
   Na 25 seconden schuift rechtsonder een kaart in beeld met de vraag of het
   cluster stilligt, en de knop naar het aanvraagformulier van de triage.

   Vier regels waar niet aan getornd moet worden:
   - niet op /triage/, /afspraak/ en /contact/. Daar is de bezoeker al bezig
     met precies dit en is de kaart alleen maar in de weg.
   - eenmaal open blijft open. Klikt iemand door naar een volgende pagina, dan
     staat de kaart daar meteen weer, zonder opnieuw te tellen. Hij verdwijnt
     alleen als de bezoeker hem zelf wegklikt of doorklikt.
   - eenmalig. Wie hem wegklikt of doorklikt ziet hem dertig dagen niet meer.
   - de klok loopt alleen als de pagina zichtbaar is. Een tabblad dat een half
     uur op de achtergrond staat telt niet als een halve minuut lezen.

   De teksten komen letterlijk van de site zelf: de meldingsbalk bovenaan en
   het slotblok van de praktijkvoorbeelden. */
(function(){
  var UIT=['/triage/','/afspraak/','/contact/',
           /* dezelfde drie pagina's in het Engels; die hebben andere paden en
              vielen daardoor buiten deze lijst. */
           '/en/triage/','/en/appointment/','/en/contact/'],
      SLEUTEL='cl-hulpkaart',
      STAAT='cl-hulpkaart-open',
      DAGEN=30,
      NA=25000;

  var pad=location.pathname;
  for(var i=0;i<UIT.length;i++) if(pad.indexOf(UIT[i])===0) return;

  /* Om hem te bekijken of te tonen aan iemand anders: zet ?hulpkaart=nu achter
     het adres. Dan vergeet de browser dat hij ooit is weggeklikt en staat de
     kaart er meteen. Handig, want anders blijft hij dertig dagen weg en lijkt
     het alsof hij stuk is. */
  var proef=location.search.indexOf('hulpkaart=nu')>-1;
  if(proef){ try{ localStorage.removeItem(SLEUTEL); sessionStorage.removeItem(STAAT); }catch(e){} }

  function gezien(){
    try{
      var t=parseInt(localStorage.getItem(SLEUTEL),10);
      return t && (Date.now()-t) < DAGEN*864e5;
    }catch(e){ return false; }
  }
  function onthoud(){
    try{ localStorage.setItem(SLEUTEL,String(Date.now())); sessionStorage.removeItem(STAAT); }catch(e){}
  }
  /* Haalt iemand de kaart zelf terug met het knopje, dan telt het eerdere
     wegklikken niet meer: de kaart blijft dan ook op de volgende pagina staan,
     tot hij hem opnieuw wegklikt. */
  function vergeet(){
    try{ localStorage.removeItem(SLEUTEL); }catch(e){}
  }
  /* Stond de kaart al open toen de bezoeker doorklikte, dan hoort hij op de
     volgende pagina gewoon te blijven staan. Dat onthoudt de sessie, dus na het
     sluiten van het venster telt de klok weer van voren af aan. */
  function staatOpen(){
    try{ return !!sessionStorage.getItem(STAAT); }catch(e){ return false; }
  }
  function blijfOpen(){
    try{ sessionStorage.setItem(STAAT,'1'); }catch(e){}
  }

  /* Hetzelfde formulier als op /triage/, veld voor veld. Ook hier verstuurt het
     niets zelf: de aanvraag vertrekt via de eigen WhatsApp of e-mail van de
     bezoeker, en deze pagina slaat niets op. */
  /* De kaart stond in het Nederlands op elke pagina, ook op de Engelse. De
     zinnen hieronder staan letterlijk zo op de Engelse pagina's van de site:
     de meldingsbalk ("Secure the evidence first."), het slotblok van de
     praktijkvoorbeelden ("The free Cluster Triage only reads and changes
     nothing.") en het aanvraagformulier op /en/triage/. Alleen "No, I will
     keep looking" bestond nergens; die staat in en/TE-CONTROLEREN.md.

     Het verzonden bericht blijft Nederlands, net als bij de andere drie
     formulieren: het gaat naar dezelfde postbus. */
  var EN = document.documentElement.lang === 'en';
  var T = EN ? {
    kop:'Cluster down?',
    intro:'Secure the evidence first. The free Cluster Triage only reads and changes nothing.',
    start:'Start free Cluster Triage &rarr;',
    nee:'No, I will keep looking',
    sluiten:'Close',
    knop:'Cluster down? Start the free Cluster Triage',
    voornaam:'First name', achternaam:'Last name',
    bedrijf:'Company or organisation', email:'E-mail address',
    telefoon:'Phone, with country code', land:'Country',
    cluster:'Cluster name', uren:'How many hours ago did the incident occur?',
    hint:'Send the request via both WhatsApp and e-mail, so we cannot miss it.',
    wa:'Send via WhatsApp', mail:'Also send by e-mail',
    noot:'<b>This form sends nothing by itself:</b> the request leaves through your own '+
         'WhatsApp or email. This page stores nothing.'
  } : {
    kop:'Cluster down?',
    intro:'Bewaar eerst het bewijs. De gratis Cluster Triage leest uitsluitend en verandert niets.',
    start:'Start gratis Cluster Triage &rarr;',
    nee:'Nee, ik kijk verder',
    sluiten:'Sluiten',
    knop:'Cluster down? Vraag de gratis Cluster Triage aan',
    voornaam:'Voornaam', achternaam:'Achternaam',
    bedrijf:'Bedrijf of organisatie', email:'E-mailadres',
    telefoon:'Telefoon, met landcode', land:'Land',
    cluster:'Clusternaam', uren:'Hoeveel uur geleden vond het incident plaats?',
    hint:'Verstuur de aanvraag via WhatsApp \u00e9n e-mail, dan missen wij hem niet.',
    wa:'Verstuur via WhatsApp', mail:'Verstuur ook per e-mail',
    noot:'<b>Dit formulier verstuurt niets zelf:</b> de aanvraag vertrekt via uw eigen '+
         'WhatsApp of e-mail. Deze pagina slaat niets op.'
  };

  /* Hetzelfde formulier als op de triagepagina, veld voor veld. Ook hier
     verstuurt het niets zelf: de aanvraag vertrekt via de eigen WhatsApp of
     e-mail van de bezoeker, en deze pagina slaat niets op. */
  var FORMULIER=
    '<form class="aanvraag" id="hulpform">'+
      '<div class="veldrij">'+
        '<label><span class="lbl">'+T.voornaam+'</span><input name="voornaam" autocomplete="given-name" required></label>'+
        '<label><span class="lbl">'+T.achternaam+'</span><input name="achternaam" autocomplete="family-name" required></label>'+
      '</div>'+
      '<label><span class="lbl">'+T.bedrijf+'</span><input name="bedrijf" autocomplete="organization" required></label>'+
      '<label><span class="lbl">'+T.email+'</span><input name="email" type="email" autocomplete="email" required></label>'+
      '<div class="veldrij">'+
        '<label><span class="lbl">'+T.telefoon+'</span><input name="telefoon" type="tel" autocomplete="tel" placeholder="+31 6 ..." required></label>'+
        '<label><span class="lbl">'+T.land+'</span><input name="land" autocomplete="country-name" required></label>'+
      '</div>'+
      '<label><span class="lbl">'+T.cluster+'</span><input name="cluster" required></label>'+
      '<label><span class="lbl">'+T.uren+'</span><input name="uren" type="number" min="1" max="720" placeholder="12" required></label>'+
      '<p class="verzendhint">'+T.hint+'</p>'+
      '<div class="verzendrij">'+
        '<button type="button" class="btn primary" id="hulp-wa">'+T.wa+'</button>'+
        '<button type="button" class="btn dark" id="hulp-mail">'+T.mail+'</button>'+
      '</div>'+
      '<p class="aanvraag-noot">'+T.noot+'<br>WhatsApp +66&nbsp;99&nbsp;146&nbsp;1761 &middot; hans@cldlbs.com</p>'+
    '</form>';

  var kaart=null;

  function sluit(){
    if(!kaart) return;
    onthoud();
    kaart.removeAttribute('data-open');
    document.removeEventListener('keydown',opEscape);
    setTimeout(function(){
      if(kaart&&kaart.parentNode) kaart.parentNode.removeChild(kaart);
      kaart=null;
      toonKnop();
    },320);
  }

  /* Het knopje dat overblijft. Het staat op dezelfde plek als de kaart, dus er
     is er altijd maar één van de twee te zien. */
  var knop=null;
  function toonKnop(){
    if(knop) return;
    knop=document.createElement('button');
    knop.className='hulpknop';
    knop.type='button';
    knop.setAttribute('aria-label',T.knop);
    knop.title=T.knop;
    knop.onclick=function(){ verbergKnop(); toon(true); };
    document.body.appendChild(knop);
  }
  function verbergKnop(){
    if(knop&&knop.parentNode) knop.parentNode.removeChild(knop);
    knop=null;
  }
  /* Escape sluit alleen de dichte kaart. Staat het formulier open, dan is
     iemand aan het invullen en mag één toets dat niet weggooien. */
  function opEscape(e){ if(e.key==='Escape' && kaart && !kaart.hasAttribute('data-uit')) sluit(); }

  /* Openklappen gebeurt in de kaart zelf; er wordt niet doorverwezen. De rand
     stopt met lopen zodra het formulier openstaat. */
  function klapUit(){
    if(!kaart) return;
    var knop=kaart.querySelector('.hulpkaart-uit'),
        vak=kaart.querySelector('.hulpkaart-form');
    knop.hidden=true;
    kaart.querySelector('.hulpkaart-nee').hidden=true;
    vak.hidden=false;
    kaart.setAttribute('data-uit','');
    knop.setAttribute('aria-expanded','true');
    koppelVerzenden(kaart.querySelector('#hulpform'));
    var eerste=vak.querySelector('input');
    if(eerste) eerste.focus();
  }

  /* Woordelijk dezelfde opbouw en dezelfde bestemmingen als het formulier op
     de triagepagina. */
  function koppelVerzenden(F){
    if(!F) return;
    function bericht(){
      if(!F.reportValidity()) return null;
      var v=function(n){ return F.elements[n].value.trim(); };
      return 'Cluster Triage aanvraag'
        + '\nNaam: '     + v('voornaam') + ' ' + v('achternaam')
        + '\nBedrijf: '  + v('bedrijf')
        + '\nE-mail: '   + v('email')
        + '\nTelefoon: ' + v('telefoon')
        + '\nLand: '     + v('land')
        + '\nCluster: '  + v('cluster')
        + '\nIncident: ' + v('uren') + ' uur geleden';
    }
    F.querySelector('#hulp-wa').addEventListener('click',function(){
      var b=bericht(); if(b===null) return;
      onthoud();
      window.open('https://wa.me/66991461761?text=' + encodeURIComponent(b),'_blank','noopener');
    });
    F.querySelector('#hulp-mail').addEventListener('click',function(){
      var b=bericht(); if(b===null) return;
      onthoud();
      location.href='mailto:hans@cldlbs.com,rob@cldlbs.com?subject='
        + encodeURIComponent('Cluster Triage') + '&body=' + encodeURIComponent(b);
    });
  }

  function toon(forceer){
    if(kaart) return;
    if(!forceer && gezien()) return;
    verbergKnop();
    if(forceer) vergeet();
    blijfOpen();
    kaart=document.createElement('aside');
    kaart.className='hulpkaart';
    kaart.setAttribute('role','dialog');
    kaart.setAttribute('aria-label',T.kop);
    kaart.innerHTML=
      '<button class="hulpkaart-sluit" type="button" aria-label="'+T.sluiten+'">&times;</button>'+
      '<p class="eyebrow">'+T.kop+'</p>'+
      '<p class="hulpkaart-intro">'+T.intro+'</p>'+
      '<button class="btn primary hulpkaart-uit" type="button" data-icon="script" aria-expanded="false" aria-controls="hulpkaart-form">'+T.start+'</button>'+
      '<button class="hulpkaart-nee" type="button">'+T.nee+'</button>'+
      '<div class="hulpkaart-form" id="hulpkaart-form" hidden>'+ FORMULIER +'</div>';
    document.body.appendChild(kaart);
    kaart.querySelector('.hulpkaart-sluit').onclick=sluit;
    kaart.querySelector('.hulpkaart-nee').onclick=sluit;
    kaart.querySelector('.hulpkaart-uit').onclick=klapUit;
    document.addEventListener('keydown',opEscape);
    requestAnimationFrame(function(){ requestAnimationFrame(function(){ if(kaart) kaart.setAttribute('data-open',''); }); });
  }

  /* De klok telt alleen zichtbare tijd. */
  var gelezen=0, sinds=null, tik=null;
  function start(){
    if(document.hidden||tik) return;
    sinds=Date.now();
    tik=setTimeout(function(){ tik=null; toon(); }, NA-gelezen);
  }
  function pauze(){
    if(!tik) return;
    clearTimeout(tik); tik=null;
    gelezen+=Date.now()-sinds;
  }
  if(gezien()&&!proef){
    toonKnop();
  }else if(proef||staatOpen()){
    toon(proef);
  }else{
    document.addEventListener('visibilitychange',function(){ document.hidden?pauze():start(); });
    start();
  }
})();

/* Uitklappers in het hoofdmenu.
   Met de muis doet CSS het werk via :hover, en met de tab-toets via
   :focus-within. Dit script is er voor het derde geval: een aanraakscherm,
   waar hover niet bestaat. Een tik op de knop klapt uit, Escape of een tik
   ernaast klapt weer dicht. Boven 1100 heeft dat zin; daaronder staat het
   uitgeklapte menu toch al helemaal open, dus doet de knop niets. */
(function(){
  var knoppen = [].slice.call(document.querySelectorAll('.navtop'));
  if(!knoppen.length) return;
  function dicht(behalve){
    knoppen.forEach(function(k){
      if(k !== behalve) k.setAttribute('aria-expanded','false');
    });
  }
  knoppen.forEach(function(k){
    k.addEventListener('click', function(e){
      if(window.matchMedia('(max-width:1100px)').matches) return;
      e.stopPropagation();
      var open = k.getAttribute('aria-expanded') === 'true';
      dicht(k);
      k.setAttribute('aria-expanded', open ? 'false' : 'true');
    });
  });
  document.addEventListener('click', function(e){
    if(!e.target.closest || !e.target.closest('.navgroep')) dicht(null);
  });
  document.addEventListener('keydown', function(e){
    if(e.key !== 'Escape') return;
    var open = document.querySelector('.navtop[aria-expanded="true"]');
    if(open){ dicht(null); open.focus(); }
  });
})();

/* De scankaart in de hero loopt zijn bevindingen langs.
   De staven groeien vanaf de basislijn zodra de kaart in beeld komt, daarna
   licht er telkens een op en staat de bijbehorende bevinding eronder. Er zit
   geen knop bij: hij loopt vanzelf, hij stopt zodra u weg scrolt, en met de
   muis op een staaf springt hij naar die staaf. Bij prefers-reduced-motion
   staan de staven er meteen en blijft de eerste bevinding staan. */
(function(){
  var kaart = document.querySelector('.scan-card[data-doorloop]');
  if(!kaart) return;
  var staven = [].slice.call(kaart.querySelectorAll('.bar')),
      velden = [].slice.call(kaart.querySelectorAll('.scan-signaal')),
      veld   = kaart.querySelector('.scan-veld'),
      teller = kaart.querySelector('.scan-teller'),
      rustig = matchMedia('(prefers-reduced-motion:reduce)').matches,
      nu = 0, klok = null, gegroeid = false;
  if(!velden.length) return;
  if(veld) veld.setAttribute('data-js','');

  function twee(n){ return (n < 10 ? '0' : '') + n; }

  function toon(i){
    nu = i;
    staven.forEach(function(s, k){
      if(k === i) s.setAttribute('data-actief',''); else s.removeAttribute('data-actief');
    });
    velden.forEach(function(v, k){
      if(k === i) v.setAttribute('data-actief',''); else v.removeAttribute('data-actief');
    });
    if(teller) teller.textContent = twee(i + 1) + ' / ' + twee(velden.length);
  }

  function loop(){
    stop();
    if(rustig) return;
    klok = setInterval(function(){ toon((nu + 1) % velden.length); }, 2900);
  }
  function stop(){ clearInterval(klok); klok = null; }

  function groei(){
    if(gegroeid) return;
    gegroeid = true;
    if(rustig){
      staven.forEach(function(s){ s.setAttribute('data-op',''); });
      kaart.setAttribute('data-loopt','');
      toon(0);
      return;
    }
    staven.forEach(function(s, k){
      setTimeout(function(){ s.setAttribute('data-op',''); }, 90 + k * 150);
    });
    setTimeout(function(){
      kaart.setAttribute('data-loopt','');
      toon(0);
      loop();
    }, 150 * staven.length + 640);
  }

  staven.forEach(function(s, k){
    s.addEventListener('mouseenter', function(){
      if(!gegroeid) return;
      toon(k);
      loop();
    });
  });

  if(!('IntersectionObserver' in window)){ groei(); return; }
  new IntersectionObserver(function(items){
    items.forEach(function(it){
      if(it.isIntersecting){ groei(); if(gegroeid && klok === null) loop(); }
      else stop();
    });
  }, {threshold:.25}).observe(kaart);
})();
