/* CloudLabs · pagina.js · gedeeld door preview-home.html en triage.html.
   De verzendlogica komt van cldlbs.com/triage/: het formulier verstuurt zelf
   niets, de aanvraag vertrekt via de eigen WhatsApp of e-mail van de bezoeker. */
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
(function(){var sluit=document.getElementById('close-announcement'),melding=document.getElementById('announcement');if(sluit&&melding)sluit.onclick=function(){melding.remove()};var menu=document.getElementById('menu'),links=document.getElementById('navlinks');if(menu&&links)menu.onclick=function(){var o=links.classList.toggle('open');menu.setAttribute('aria-expanded',o?'true':'false')};var rs=[].slice.call(document.querySelectorAll('.reveal'));if(!('IntersectionObserver'in window)||matchMedia('(prefers-reduced-motion:reduce)').matches){rs.forEach(function(x){x.classList.add('in')})}else{var io=new IntersectionObserver(function(es){es.forEach(function(e){if(e.isIntersecting){e.target.classList.add('in');io.unobserve(e.target)}})},{threshold:.08});rs.forEach(function(x){io.observe(x)})}var c=document.getElementById('carousel'),vo=document.getElementById('next'),te=document.getElementById('prev');if(c&&vo&&te){vo.onclick=function(){c.scrollBy({left:c.clientWidth*.65,behavior:'smooth'})};te.onclick=function(){c.scrollBy({left:-c.clientWidth*.65,behavior:'smooth'})}}})();
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
