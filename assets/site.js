// Visitor-identification tag + EU/UK consent gate.
// Lives here, not inline, because vercel.json sets script-src 'self' with no
// 'unsafe-inline' — an inline gate is silently blocked and the tag never loads.
// Config comes from <meta name="vtag-*"> so build.py stays the single source.
(function () {
  var src = meta('vtag-src'), pid = meta('vtag-pid'), ver = meta('vtag-version');
  if (!src || !pid) return;
  var EU = /^(Europe\/|Atlantic\/(Azores|Madeira|Canary|Faeroe|Reykjavik)$|Arctic\/Longyearbyen$)/;
  var KEY = 'vtag-consent';

  function meta(n) {
    var m = document.querySelector('meta[name="' + n + '"]');
    return m ? m.getAttribute('content') : '';
  }
  function load() {
    if (document.getElementById('vtag-ai-js')) return;
    var s = document.createElement('script');
    s.id = 'vtag-ai-js'; s.async = true; s.src = src;
    s.setAttribute('data-pid', pid);
    if (ver) s.setAttribute('data-version', ver);
    document.head.appendChild(s);
  }

  var tz = '';
  try { tz = Intl.DateTimeFormat().resolvedOptions().timeZone || ''; } catch (e) {}
  var stored = null;
  try { stored = localStorage.getItem(KEY); } catch (e) {}

  // ponytail: region from the browser's IANA timezone, not IP geo. A European on
  // a US VPN is missed; a traveller in Europe sees a banner unnecessarily.
  // Accepted for a zero-backend static site. Upgrade path: read Vercel's
  // x-vercel-ip-country in middleware and decide server-side.
  if (stored === 'no') return;
  if (!EU.test(tz) || stored === 'yes') { load(); return; }

  ready(function () {
    var b = document.createElement('div');
    b.className = 'consent';
    b.setAttribute('role', 'dialog');
    b.setAttribute('aria-label', 'Visitor identification consent');
    b.innerHTML = '<p>This site can identify visiting organisations so business enquiries can be followed up. It is not advertising. <a href="/privacy/">How it works</a>.</p>' +
      '<div class="consent-actions"><button type="button" data-consent="no">Decline</button>' +
      '<button type="button" data-consent="yes" class="consent-yes">Allow</button></div>';
    b.addEventListener('click', function (e) {
      var t = e.target.closest('[data-consent]');
      if (!t) return;
      try { localStorage.setItem(KEY, t.dataset.consent); } catch (err) {}
      if (t.dataset.consent === 'yes') load();
      b.remove();
    });
    document.body.appendChild(b);
  });

  function ready(fn) {
    if (document.readyState !== 'loading') fn();
    else document.addEventListener('DOMContentLoaded', fn);
  }
})();

const toggle=document.querySelector('.nav-toggle');
const links=document.querySelector('.nav-links');
if(toggle&&links){toggle.addEventListener('click',()=>{const open=links.classList.toggle('open');toggle.setAttribute('aria-expanded',String(open));});links.addEventListener('click',event=>{if(event.target.closest('a')){links.classList.remove('open');toggle.setAttribute('aria-expanded','false');}});}
// Nav dropdowns are <details>, so open/close/keyboard already work without JS.
// These handlers only add the polish browsers do not give us: one open at a time,
// close on outside click, close on Escape, and hover-to-open on real pointers.
const menus=[...document.querySelectorAll('.menu')];
if(menus.length){
  const shut=except=>menus.forEach(m=>{if(m!==except)m.open=false;});
  menus.forEach(m=>{
    m.addEventListener('toggle',()=>{if(m.open)shut(m);});
    m.addEventListener('click',e=>{if(e.target.closest('.menu-panel a'))m.open=false;});
  });
  document.addEventListener('click',e=>{if(!e.target.closest('.menu'))shut(null);});
  document.addEventListener('keydown',e=>{
    if(e.key!=='Escape')return;
    const open=menus.find(m=>m.open);
    if(open){open.open=false;open.querySelector('summary').focus();}
  });
  // Hover only where hovering is meaningful and there is room for a dropdown.
  if(window.matchMedia('(hover:hover) and (min-width:901px)').matches){
    menus.forEach(m=>{
      let t;
      m.addEventListener('mouseenter',()=>{clearTimeout(t);shut(m);m.open=true;});
      m.addEventListener('mouseleave',()=>{t=setTimeout(()=>{m.open=false;},220);});
    });
  }
}
