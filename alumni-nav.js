/* =====================================================================
   IITGN Alumni — shared top bar and footer for every page on
   iitgnalumni.github.io

   HOW TO USE ON A PAGE
   Paste this one line right after the page's <body> tag:
     <script src="/alumni-nav.js"></script>
   Optional: data-footer="false" on that tag hides the shared footer
   (used on Homecoming, which is a full-screen embedded site).

   HOW TO ADD OR CHANGE A LINK
   Edit the LINKS list below. Every page picks up the change
   automatically (GitHub Pages can take a few minutes to refresh).
   ===================================================================== */
(function () {
  'use strict';

  /* ---------------- EDIT HERE ---------------- */
  var PORTAL = 'https://alumni.iitgn.ac.in/';
  var LINKS = [
    { label: 'Homecoming 2026',   href: '/homecoming2026/' },
    { label: 'MasterClass',       href: '/masterclass/' },
    { label: 'YAE Awards',        href: '/YAEA/' },
    { label: 'Alumni Collective', href: '/IITGNAC/' },
    { label: 'Newsletters & Reports', href: '/publications/' }
  ];
  var EMAIL = 'alumnirelations@iitgn.ac.in';
  /* ------------------------------------------- */

  if (window.__iitgnAlumniNav) return;           // never add it twice
  window.__iitgnAlumniNav = true;

  var me = document.currentScript;
  var showFooter = !(me && me.getAttribute('data-footer') === 'false');
  var path = location.pathname.toLowerCase();

  function isCurrent(href) {
    if (href.charAt(0) !== '/') return false;
    return path.indexOf(href.toLowerCase()) === 0;
  }
  function esc(s) {
    return String(s).replace(/[&<>"]/g, function (c) {
      return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c];
    });
  }

  /* ---------- styles (all scoped to #ia-bar / #ia-foot) ---------- */
  var css =
    '#ia-bar,#ia-foot{all:initial;display:block;box-sizing:border-box;' +
      'font-family:"Public Sans","Open Sans",Helvetica,Arial,sans-serif;' +
      '-webkit-font-smoothing:antialiased;color-scheme:light}' +
    '#ia-bar *,#ia-foot *{box-sizing:border-box;font-family:inherit;margin:0;padding:0}' +
    '#ia-bar{background:#0f2a3d;color:#dbe7ef;font-size:13px;line-height:1;position:relative;z-index:60}' +
    '#ia-bar .ia-in{max-width:1200px;margin:0 auto;padding:0 16px;height:36px;display:flex;align-items:center;gap:20px}' +
    '#ia-bar a{color:#dbe7ef;text-decoration:none;white-space:nowrap;display:inline-flex;align-items:center;height:36px;' +
      'border-bottom:2px solid transparent;transition:color .15s,border-color .15s}' +
    '#ia-bar a:hover,#ia-bar a:focus-visible{color:#fff;border-bottom-color:#b3eaf9;outline:none}' +
    '#ia-bar a.ia-home{font-weight:700;color:#fff;letter-spacing:.01em;gap:6px}' +
    '#ia-bar a.ia-home svg{width:13px;height:13px;flex:none}' +
    '#ia-bar nav{display:flex;align-items:center;gap:20px;margin-left:auto;overflow-x:auto;scrollbar-width:none;-webkit-overflow-scrolling:touch}' +
    '#ia-bar nav::-webkit-scrollbar{display:none}' +
    '#ia-bar a[aria-current="page"]{color:#fff;border-bottom-color:#b3eaf9;font-weight:600}' +
    '#ia-bar a.ia-cta{color:#0f2a3d;background:#b3eaf9;height:24px;padding:0 12px;border-radius:12px;border:0;font-weight:600}' +
    '#ia-bar a.ia-cta:hover,#ia-bar a.ia-cta:focus-visible{background:#fff;color:#0f2a3d}' +
    '@media (max-width:760px){#ia-bar .ia-in{gap:14px}#ia-bar nav{gap:16px;margin-left:0}' +
      '#ia-bar a.ia-home span.ia-long{display:none}}' +

    '#ia-foot{background:#0b1f2e;color:#9fb3c2;font-size:13px;line-height:1.5}' +
    '#ia-foot .ia-in{max-width:1200px;margin:0 auto;padding:18px 16px;display:flex;flex-wrap:wrap;align-items:center;gap:10px 24px}' +
    '#ia-foot a{color:#dbe7ef;text-decoration:none}' +
    '#ia-foot a:hover,#ia-foot a:focus-visible{color:#fff;text-decoration:underline;outline:none}' +
    '#ia-foot .ia-back{font-weight:600;color:#fff}' +
    '#ia-foot nav{display:flex;flex-wrap:wrap;gap:6px 18px}' +
    '#ia-foot .ia-end{margin-left:auto;display:flex;flex-wrap:wrap;gap:6px 18px}' +
    '@media (max-width:760px){#ia-foot .ia-end{margin-left:0}}';

  var style = document.createElement('style');
  style.id = 'ia-style';
  style.textContent = css;
  (document.head || document.documentElement).appendChild(style);

  /* ---------- top bar ---------- */
  var homeIcon = '<svg viewBox="0 0 16 16" aria-hidden="true"><path d="M10 3L5 8l5 5" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></svg>';
  var bar = document.createElement('div');
  bar.id = 'ia-bar';
  bar.innerHTML =
    '<div class="ia-in">' +
      '<a class="ia-home" href="' + PORTAL + '">' + homeIcon +
        '<span>IITGN Alumni<span class="ia-long"> Portal</span></span></a>' +
      '<nav aria-label="IITGN Alumni">' + LINKS.map(function (l) {
        return '<a href="' + esc(l.href) + '"' +
          (l.cta ? ' class="ia-cta"' : '') +
          (isCurrent(l.href) ? ' aria-current="page"' : '') +
          '>' + esc(l.label) + '</a>';
      }).join('') + '</nav>' +
    '</div>';

  function addBar() {
    if (document.body.firstChild) document.body.insertBefore(bar, document.body.firstChild);
    else document.body.appendChild(bar);
    fixFixedElements();
  }

  /* Pages whose own header (or full-screen frame) is position:fixed at the
     very top would sit over the bar. Shift them down by the bar's height,
     and let them slide back to the top as the visitor scrolls, so the
     page's own header looks and behaves exactly as before.
     This runs again once the page has finished loading, because the bar is
     added before the rest of the page (including its header) exists. */
  var fixed = [], listening = false;
  function fixFixedElements() {
    var kids = document.body.children;
    for (var i = 0; i < kids.length; i++) collect(kids[i]);
    var heads = document.querySelectorAll('header,.site-head');
    for (var j = 0; j < heads.length; j++) collect(heads[j]);
    if (!fixed.length) return;
    if (!listening) {
      listening = true;
      window.addEventListener('scroll', place, { passive: true });
      window.addEventListener('resize', place);
    }
    place();
  }
  function collect(el) {
    if (el === bar || el.tagName === 'SCRIPT' || el.tagName === 'STYLE') return;
    for (var k = 0; k < fixed.length; k++) if (fixed[k].el === el) return;
    var cs = getComputedStyle(el);
    if (cs.position !== 'fixed' || parseFloat(cs.top) !== 0) return;
    fixed.push({ el: el, fullHeight: parseFloat(cs.bottom) === 0 || el.offsetHeight >= window.innerHeight - 1 });
  }
  function place() {
    var h = bar.offsetHeight;
    var off = Math.max(0, h - (window.scrollY || window.pageYOffset || 0));
    for (var i = 0; i < fixed.length; i++) {
      var f = fixed[i];
      f.el.style.top = off + 'px';
      if (f.fullHeight) f.el.style.height = 'calc(100% - ' + off + 'px)';
    }
  }

  /* ---------- footer ---------- */
  function addFooter() {
    if (!showFooter) return;
    var foot = document.createElement('div');
    foot.id = 'ia-foot';
    foot.setAttribute('role', 'contentinfo');
    foot.innerHTML =
      '<div class="ia-in">' +
        '<a class="ia-back" href="' + PORTAL + '">&larr; Back to Alumni Portal</a>' +
        '<nav aria-label="IITGN Alumni pages">' + LINKS.map(function (l) {
          return '<a href="' + esc(l.href) + '"' + (isCurrent(l.href) ? ' aria-current="page"' : '') + '>' + esc(l.label) + '</a>';
        }).join('') + '</nav>' +
        '<span class="ia-end"><a href="mailto:' + EMAIL + '">' + EMAIL + '</a>' +
        '<a href="https://iitgn.ac.in/">iitgn.ac.in</a></span>' +
      '</div>';
    document.body.appendChild(foot);
  }

  if (document.body) addBar();
  else document.addEventListener('DOMContentLoaded', addBar);
  function whenReady() { addFooter(); fixFixedElements(); }
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', whenReady);
  else whenReady();
  window.addEventListener('load', fixFixedElements);
})();
