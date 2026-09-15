/* CloudLabs · shared script · v0.4.9 */
(function(){
  /* Mobile nav overflow fade */
  var navEl  = document.querySelector('nav.tabs');
  var navWrap = navEl && navEl.closest('.nav-wrap');
  if(navEl && navWrap){
    var checkOverflow = function(){
      navWrap.classList.toggle('has-overflow', navEl.scrollWidth > navEl.clientWidth);
    };
    checkOverflow();
    navEl.addEventListener('scroll', checkOverflow);
    window.addEventListener('resize', checkOverflow);
  }
  var html = document.documentElement;

  /* Language toggle */
  var setLang = function(l){
    html.setAttribute('data-lang', l);
    document.querySelectorAll('.lang-toggle button').forEach(function(b){
      b.setAttribute('aria-pressed', b.dataset.setLang === l ? 'true' : 'false');
    });
    try{ localStorage.setItem('cl_lang', l); }catch(e){}
  };
  document.querySelectorAll('.lang-toggle button').forEach(function(b){
    b.addEventListener('click', function(){ setLang(b.dataset.setLang); });
  });
  try{
    var saved = localStorage.getItem('cl_lang');
    if(saved === 'nl' || saved === 'en'){
      setLang(saved);
    } else {
      /* Auto-detect from browser language if no stored preference */
      var browserLang = (navigator.language || navigator.userLanguage || '').toLowerCase();
      if(browserLang === 'nl' || browserLang.indexOf('nl-') === 0){
        setLang('nl');
      }
    }
  }catch(e){}

  /* Findings switcher (only on findings page) */
  var cards = document.querySelectorAll('.finding-card[data-finding]');
  if(cards.length){
    var pills = document.querySelectorAll('.pill-btn[data-finding]');
    var prev  = document.getElementById('finding-prev');
    var next  = document.getElementById('finding-next');
    var order = Array.from(pills).map(function(p){ return p.dataset.finding; });
    var idx   = 0;
    var show  = function(i){
      idx = (i + order.length) % order.length;
      var id = order[idx];
      cards.forEach(function(c){ c.classList.toggle('active', c.dataset.finding === id); });
      pills.forEach(function(p){ p.setAttribute('aria-current', p.dataset.finding === id ? 'true' : 'false'); });
      if(prev) prev.disabled = idx === 0;
      if(next) next.disabled = idx === order.length - 1;
    };
    pills.forEach(function(p, i){ p.addEventListener('click', function(){ show(i); }); });
    if(prev) prev.addEventListener('click', function(){ show(idx - 1); });
    if(next) next.addEventListener('click', function(){ show(idx + 1); });
    show(0);
  }

  /* Book form mailto (only on book page) */
  var send = document.getElementById('send-mail');
  if(send){
    send.addEventListener('click', function(){
      var v = function(id){ return (document.getElementById(id) || {}).value || ''; };
      var lang = html.getAttribute('data-lang');
      var subj = lang === 'nl'
        ? 'CloudLabs intake aanvraag · ' + v('f-svc')
        : 'CloudLabs intake request · ' + v('f-svc');
      var body = lang === 'nl'
        ? 'Naam: ' + v('f-name') + '\nOrganisatie: ' + v('f-org') + '\nE-mail: ' + v('f-email') + '\nDienst: ' + v('f-svc') + '\nRichtblok: ' + v('f-block') + '\n\nToelichting:\n' + v('f-notes') + '\n'
        : 'Name: ' + v('f-name') + '\nOrganisation: ' + v('f-org') + '\nEmail: ' + v('f-email') + '\nService: ' + v('f-svc') + '\nIndicative block: ' + v('f-block') + '\n\nNotes:\n' + v('f-notes') + '\n';
      location.href = 'mailto:hans@vredevoort.com?subject=' + encodeURIComponent(subj) + '&body=' + encodeURIComponent(body);
    });
  }

  /* ── Stagger index assignment ─────────────────────────────── */
  document.querySelectorAll('.anim-stagger').forEach(function(parent){
    Array.from(parent.children).forEach(function(child, i){
      child.style.setProperty('--i', i);
    });
  });

  /* ── Scroll animations ────────────────────────────────────── */
  if('IntersectionObserver' in window){
    var observer = new IntersectionObserver(function(entries){
      entries.forEach(function(entry){
        if(entry.isIntersecting){
          entry.target.classList.add('is-visible');
          observer.unobserve(entry.target);
        }
      });
    }, {threshold: 0.12, rootMargin: '0px 0px -40px 0px'});

    document.querySelectorAll('.anim-fade, .anim-stagger').forEach(function(el){
      observer.observe(el);
    });
  } else {
    /* Fallback: show everything immediately */
    document.querySelectorAll('.anim-fade, .anim-stagger').forEach(function(el){
      el.classList.add('is-visible');
    });
  }

  /* Stat counter animation */
  function animateCounter(el, target, suffix, duration){
    var start = 0;
    var step  = Math.ceil(target / (duration / 16));
    var timer = setInterval(function(){
      start = Math.min(start + step, target);
      el.textContent = start + suffix;
      if(start >= target) clearInterval(timer);
    }, 16);
  }

  var statsObserver = new IntersectionObserver(function(entries){
    entries.forEach(function(entry){
      if(!entry.isIntersecting) return;
      var el = entry.target;
      var raw   = el.dataset.count;
      var suffix = el.dataset.suffix || '';
      animateCounter(el, parseInt(raw, 10), suffix, 900);
      statsObserver.unobserve(el);
    });
  }, {threshold: 0.5});

  document.querySelectorAll('[data-count]').forEach(function(el){
    statsObserver.observe(el);
  });
  /* ── End scroll animations ─────────────────────────────────── */

  /* Cookie consent */
  var KEY     = 'cl_consent';
  var banner  = document.getElementById('consentBanner');
  var reopen  = document.getElementById('consentReopen');
  var accept  = document.getElementById('consentAccept');
  var decline = document.getElementById('consentDecline');

  if(banner){
    function showBanner(){ banner.classList.add('show'); }
    function hideBanner(){ banner.classList.remove('show'); }
    function update(state){
      if(typeof gtag !== 'undefined'){
        gtag('consent', 'update', {
          analytics_storage: state,
          ad_storage: 'denied',
          ad_user_data: 'denied',
          ad_personalization: 'denied'
        });
      }
      try{ localStorage.setItem(KEY, state); }catch(e){}
      hideBanner();
    }
    var savedConsent = null;
    try{ savedConsent = localStorage.getItem(KEY); }catch(e){}
    if(savedConsent === 'granted'){ update('granted'); hideBanner(); }
    else if(savedConsent === 'denied'){ hideBanner(); }
    else{ showBanner(); }
    if(accept)  accept.addEventListener('click',  function(){ update('granted'); });
    if(decline) decline.addEventListener('click', function(){ update('denied');  });
    if(reopen)  reopen.addEventListener('click',  function(){ showBanner(); });
  }

  /* Copy-to-clipboard buttons on code blocks (blog articles) */
  document.querySelectorAll('.article pre').forEach(function(pre){
    var code = pre.querySelector('code');
    if(!code) return;
    var wrap = document.createElement('div');
    wrap.className = 'code-block';
    pre.parentNode.insertBefore(wrap, pre);
    wrap.appendChild(pre);
    var btn = document.createElement('button');
    btn.type = 'button';
    btn.className = 'copy-btn';
    btn.setAttribute('aria-label', 'Copy code');
    btn.innerHTML = '<span class="copy-label">Copy</span>';
    btn.addEventListener('click', function(){
      var text = code.textContent;
      var done = function(){
        btn.classList.add('copied');
        btn.querySelector('.copy-label').textContent = 'Copied';
        setTimeout(function(){
          btn.classList.remove('copied');
          btn.querySelector('.copy-label').textContent = 'Copy';
        }, 1500);
      };
      if(navigator.clipboard && navigator.clipboard.writeText){
        navigator.clipboard.writeText(text).then(done).catch(function(){});
      } else {
        var ta = document.createElement('textarea');
        ta.value = text; ta.setAttribute('readonly','');
        ta.style.position='absolute'; ta.style.left='-9999px';
        document.body.appendChild(ta); ta.select();
        try{ document.execCommand('copy'); done(); }catch(e){}
        document.body.removeChild(ta);
      }
    });
    wrap.appendChild(btn);
  });

  /* Build the sticky TOC sidebar from the in-document TOC when a blog does
     not ship one of its own. On desktop the CSS hides the inline TOC and shows
     this sidebar; on mobile the inline TOC shows and this stays hidden. */
  (function(){
    var article = document.querySelector('.article');
    if(!article || article.querySelector('.article-toc-sticky')) return;
    var tocs = article.querySelectorAll('.toc');
    if(!tocs.length) return;
    var aside = document.createElement('aside');
    aside.className = 'article-toc-sticky';
    aside.setAttribute('aria-label', 'On this page');
    aside.innerHTML = '<div class="toc-title"><span lang="en">In this article</span><span lang="nl">In dit artikel</span></div>';
    tocs.forEach(function(toc){
      var ol = toc.querySelector('ol');
      if(!ol) return;
      var clone = ol.cloneNode(true);
      var langEl = toc.closest('[lang]');
      if(langEl) clone.setAttribute('lang', langEl.getAttribute('lang'));
      aside.appendChild(clone);
    });
    article.insertBefore(aside, article.firstChild);
  })();

  /* Scrollspy on sticky TOC sidebar (blog articles, desktop) */
  var stickyToc = document.querySelector('.article-toc-sticky');
  if(stickyToc && 'IntersectionObserver' in window){
    var headings = document.querySelectorAll('.article h2[id]');
    if(headings.length){
      var spyObs = new IntersectionObserver(function(entries){
        entries.forEach(function(entry){
          if(entry.isIntersecting){
            var id = entry.target.id;
            stickyToc.querySelectorAll('a').forEach(function(a){
              a.classList.toggle('active', a.getAttribute('href') === '#' + id);
            });
          }
        });
      }, { rootMargin: '-12% 0px -78% 0px', threshold: 0 });
      headings.forEach(function(h){ spyObs.observe(h); });
    }
  }

  /* Full-text search (topbar) */
  (function(){
    var topRight = document.querySelector('.top-right');
    if(!topRight) return;
    var isBlog = /\/blog\//.test(location.pathname);
    var base = isBlog ? '../' : '';
    var doc = document.documentElement;

    var btn = document.createElement('button');
    btn.className = 'search-btn'; btn.id = 'searchOpen'; btn.setAttribute('aria-label','Search');
    btn.innerHTML = '<svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><circle cx="11" cy="11" r="7"></circle><line x1="21" y1="21" x2="16.65" y2="16.65"></line></svg>';
    topRight.insertBefore(btn, topRight.firstChild);

    var ov = document.createElement('div');
    ov.className = 'search-overlay'; ov.hidden = true;
    ov.innerHTML = '<div class="search-panel" role="dialog" aria-modal="true" aria-label="Search"><input id="searchInput" type="search" autocomplete="off" spellcheck="false"><div class="search-results"></div></div>';
    document.body.appendChild(ov);
    var input = ov.querySelector('#searchInput'), results = ov.querySelector('.search-results');

    var idx = null, loading = false, queue = [];
    function load(cb){
      if(idx){ cb(); return; }
      queue.push(cb);
      if(loading) return; loading = true;
      fetch(base + 'search-index.json').then(function(r){ return r.json(); })
        .then(function(d){ idx = d; queue.forEach(function(f){ f(); }); queue = []; })
        .catch(function(){ results.innerHTML = '<div class="sr-empty">Search unavailable</div>'; });
    }
    function nlOn(){ return doc.getAttribute('data-lang') === 'nl'; }
    function open(){
      ov.hidden = false; document.body.style.overflow = 'hidden';
      input.placeholder = nlOn() ? 'Zoeken op de site...' : 'Search the site...';
      input.value = ''; results.innerHTML = ''; input.focus(); load(function(){});
    }
    function close(){ ov.hidden = true; document.body.style.overflow = ''; }
    btn.addEventListener('click', open);
    ov.addEventListener('click', function(e){ if(e.target === ov) close(); });
    document.addEventListener('keydown', function(e){
      if(e.key === 'Escape' && !ov.hidden){ close(); return; }
      if(ov.hidden && (e.key === '/' || ((e.metaKey||e.ctrlKey) && (e.key === 'k' || e.key === 'K')))){
        var tag = (e.target.tagName || '').toLowerCase();
        if(tag !== 'input' && tag !== 'textarea'){ e.preventDefault(); open(); }
      }
    });
    function esc(s){ return String(s).replace(/[&<>]/g, function(c){ return {'&':'&amp;','<':'&lt;','>':'&gt;'}[c]; }); }
    function snippet(text, terms){
      var low = text.toLowerCase(), i = low.indexOf(terms[0]);
      if(i < 0) i = 0;
      var start = Math.max(0, i - 40);
      return (start > 0 ? '…' : '') + esc(text.slice(start, start + 150)) + '…';
    }
    function render(q){
      var terms = q.toLowerCase().split(/\s+/).filter(Boolean);
      if(!terms.length){ results.innerHTML = ''; return; }
      var nl = nlOn(), hits = [];
      idx.forEach(function(e){
        var hay = (e.te + ' ' + e.tn + ' ' + e.s + ' ' + e.x).toLowerCase();
        if(terms.every(function(t){ return hay.indexOf(t) >= 0; })){
          var title = (nl ? e.tn : e.te) || e.te, tl = title.toLowerCase(), score = 0;
          terms.forEach(function(t){ if(tl.indexOf(t) >= 0) score += 3; });
          hits.push({ e: e, title: title, score: score });
        }
      });
      hits.sort(function(a,b){ return b.score - a.score; });
      if(!hits.length){ results.innerHTML = '<div class="sr-empty">' + (nl ? 'Geen resultaten' : 'No results') + '</div>'; return; }
      var qs = encodeURIComponent(q);
      results.innerHTML = hits.slice(0,8).map(function(h){
        var u = base + h.e.u, hash = '', hi = u.indexOf('#');
        if(hi >= 0){ hash = u.slice(hi); u = u.slice(0, hi); }
        u += (u.indexOf('?') >= 0 ? '&' : '?') + 'q=' + qs + hash;
        return '<a class="sr-item" href="' + u + '"><span class="sr-title">' + esc(h.title) + '</span>'
          + (h.e.s ? '<span class="sr-sec">' + esc(h.e.s) + '</span>' : '')
          + '<span class="sr-snip">' + snippet(h.e.x, terms) + '</span></a>';
      }).join('');
    }
    input.addEventListener('input', function(){ load(function(){ render(input.value.trim()); }); });
  })();

  /* Highlight the search term after arriving from a search result (?q=) */
  (function(){
    var q;
    try{ q = new URLSearchParams(location.search).get('q'); }catch(e){ return; }
    if(!q) return;
    var terms = q.toLowerCase().split(/\s+/).filter(Boolean);
    if(!terms.length) return;
    var root = document.getElementById('main-content') || document.querySelector('.article') || document.body;
    var re = new RegExp('(' + terms.map(function(t){ return t.replace(/[.*+?^${}()|[\]\\]/g, '\\$&'); }).join('|') + ')', 'gi');
    function hidden(node){
      for(var el = node.parentElement; el && el !== root.parentNode; el = el.parentElement){
        var s = getComputedStyle(el);
        if(s.display === 'none' || s.visibility === 'hidden') return true;
      }
      return false;
    }
    var walker = document.createTreeWalker(root, NodeFilter.SHOW_TEXT, {
      acceptNode: function(n){
        if(!n.nodeValue || !n.nodeValue.trim()) return NodeFilter.FILTER_REJECT;
        var tag = n.parentNode && n.parentNode.nodeName;
        if(tag === 'SCRIPT' || tag === 'STYLE' || tag === 'MARK') return NodeFilter.FILTER_REJECT;
        re.lastIndex = 0;
        return re.test(n.nodeValue) ? NodeFilter.FILTER_ACCEPT : NodeFilter.FILTER_REJECT;
      }
    });
    var targets = [];
    while(walker.nextNode()) targets.push(walker.currentNode);
    var firstVisible = null;
    targets.forEach(function(node){
      var vis = !hidden(node), txt = node.nodeValue, frag = document.createDocumentFragment(), last = 0, m;
      re.lastIndex = 0;
      while((m = re.exec(txt))){
        if(m.index > last) frag.appendChild(document.createTextNode(txt.slice(last, m.index)));
        var mk = document.createElement('mark');
        mk.className = 'search-hl';
        mk.textContent = m[0];
        frag.appendChild(mk);
        if(!firstVisible && vis) firstVisible = mk;
        last = m.index + m[0].length;
        if(m.index === re.lastIndex) re.lastIndex++;
      }
      if(last < txt.length) frag.appendChild(document.createTextNode(txt.slice(last)));
      node.parentNode.replaceChild(frag, node);
    });
    if(firstVisible){
      setTimeout(function(){ firstVisible.scrollIntoView({ behavior: 'smooth', block: 'center' }); }, 60);
    }
    try{
      var u = new URL(location.href); u.searchParams.delete('q');
      history.replaceState(null, '', u.pathname + u.search + u.hash);
    }catch(e){}
  })();
})();
