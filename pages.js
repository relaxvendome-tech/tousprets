/* Tous prêts — fonctions des pages outils (v6) : test « Suis-je prêt ? », filtre de « Tous les guides »,
   filtre des questions-réponses et du glossaire, checklist à cocher et à imprimer.
   Aucune ressource externe. La normalisation et les synonymes viennent de search.js (window.TPSearch). */
(function () {
  'use strict';
  var $ = function (s, r) { return (r || document).querySelector(s); };
  var $$ = function (s, r) { return [].slice.call((r || document).querySelectorAll(s)); };

  /* Recherche partagée : search.js (chargé avant, en defer) expose TPSearch ; repli minimal sinon. */
  function S() {
    if (window.TPSearch) return window.TPSearch;
    var norm = function (s) { return ' ' + (s || '').toLowerCase().normalize('NFD').replace(/[̀-ͯ]/g, '').replace(/[^a-z0-9]+/g, ' ') + ' '; };
    return { norm: norm, words: function (q) { return norm(q).trim().split(/\s+/).filter(function (w) { return w.length > 1; }); },
      score: function (ws, p) { return ws.every(function (w) { return p._a.indexOf(' ' + w) >= 0; }) ? 1 : null; } };
  }
  function rec(title, all, url) { var n = S().norm; return { _t: n(title), _a: n(all), u: url || '' }; }
  function plural(n, one, many) { return n + ' ' + (n > 1 ? many : one); }

  /* ---------- 1. Test « Suis-je prêt ? » : une question à la fois ---------- */
  function diag() {
    var form = $('#diag'); if (!form) return;
    var fs = $$('.dq', form), n = fs.length, cur = 0;
    var top = $('.dg-top', form), bar = $('.dg-bar', form), count = $('#dg-count'), err = $('#dg-err');
    var nav = $('.dg-nav', form), prev = $('#dg-prev'), next = $('#dg-next'), res = $('#dres');
    form.classList.add('dg-js'); top.hidden = false; nav.hidden = false;
    function val(f) { var c = $('input:checked', f); return c ? +c.value : null; }
    function show(i, focus) {
      cur = i; err.hidden = true; res.hidden = true; form.hidden = false;
      fs.forEach(function (f, k) { f.hidden = k !== i; });
      count.textContent = 'Question ' + (i + 1) + ' sur ' + n;
      bar.setAttribute('aria-valuenow', i + 1);
      bar.firstElementChild.style.width = Math.round((i + 1) / n * 100) + '%';
      prev.disabled = i === 0;
      next.textContent = i === n - 1 ? 'Voir mon résultat' : 'Suivant';
      if (focus) { $('legend', fs[i]).focus({ preventScroll: true }); var r = top.getBoundingClientRect(); if (r.top < 0 || r.top > innerHeight * 0.6) top.scrollIntoView({ block: 'start' }); }
    }
    function esc(s) { return String(s).replace(/[&<>"]/g, function (c) { return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]; }); }
    function result() {
      var tot = 0, miss = [];
      fs.forEach(function (f, k) { var v = val(f); tot += v; if (v < 2) miss.push([v, k, f]); });
      var r = tot / (n * 2);
      var lvl = r >= 0.8 ? ['Bien préparé', 'Très bien préparé. Pensez à vérifier votre kit deux fois par an.']
        : r >= 0.5 ? ['En bonne voie', 'Bonne base. Quelques actions simples vous mettront à l\'abri.']
        : ['Premiers pas', 'Vous démarrez : chaque petit pas compte, commencez par l\'action n° 1.'];
      miss.sort(function (a, b) { return a[0] - b[0] || a[1] - b[1]; });
      var acts = miss.slice(0, 3).map(function (m) {
        return '<li><a href="' + esc(m[2].dataset.link) + '.html">' + esc(m[2].dataset.act) + '</a> <span class="dres-why">(réponse « ' + (m[0] ? 'en partie' : 'non') + ' »)</span></li>';
      }).join('');
      res.innerHTML = '<h3 class="dres-t" tabindex="-1">Votre niveau : ' + lvl[0] + '</h3><p><strong>' + lvl[1] + '</strong></p>' +
        (acts ? '<p>' + (miss.length === 1 ? 'Votre prochaine action :' : 'Vos ' + Math.min(3, miss.length) + ' prochaines actions :') + '</p><ol class="dres-acts">' + acts + '</ol>'
          : '<p>Rien ne manque à l\'essentiel. Gardez votre kit à jour.</p>') +
        '<p class="dres-cta"><a class="btn" href="checklist-kit-urgence-72h.html">Ouvrir la checklist à imprimer</a> <a class="btn btn-2" href="./">Cocher ma liste dans l\'appli</a></p>' +
        '<p class="dres-again"><button type="button" class="linkbtn" id="dg-edit">Modifier mes réponses</button><button type="button" class="linkbtn" id="dg-restart">Recommencer le test</button></p>';
      form.hidden = true; res.hidden = false;
      $('.dres-t', res).focus({ preventScroll: true }); res.scrollIntoView({ block: 'start' });
      $('#dg-edit').addEventListener('click', function () { show(n - 1, true); });
      $('#dg-restart').addEventListener('click', function () { $$('input', form).forEach(function (i) { i.checked = false; }); show(0, true); });
    }
    function go() {
      if (val(fs[cur]) === null) {
        err.textContent = 'Choisissez une réponse (oui, en partie ou non) pour continuer.'; err.hidden = false;
        $('input', fs[cur]).focus(); return;
      }
      if (cur < n - 1) show(cur + 1, true); else result();
    }
    form.addEventListener('submit', function (e) { e.preventDefault(); go(); });
    prev.addEventListener('click', function () { if (cur > 0) show(cur - 1, true); });
    form.addEventListener('change', function () { err.hidden = true; });
    show(0, false);
  }

  /* ---------- 2. Tous les guides : recherche + puces ---------- */
  function hub() {
    var box = $('#gfilter'); if (!box) return;
    box.hidden = false;
    var input = $('#gq'), out = $('#gf-n'), empty = $('.gf-empty', box);
    var cards = $$('a.gcard[data-u]'), secs = $$('main section[id]').filter(function (s) { return $('a.gcard[data-u]', s); });
    var f = { u: '', p: '' }, extra = {};
    var recs = cards.map(function (c) {
      var t = $('strong', c).textContent, d = $('.gcard-b > span', c).textContent;
      return { c: c, r: rec(t, t + ' ' + d + ' ' + c.getAttribute('href').replace(/[-.]/g, ' '), c.getAttribute('href')) };
    });
    /* enrichit avec les questions des guides (search-index.json), si disponible (pas en file://) */
    fetch('search-index.json').then(function (r) { return r.json(); }).then(function (j) {
      j.forEach(function (p) { extra[p.u] = (p.d || '') + ' ' + (p.k || ''); });
      recs.forEach(function (x) { var e = extra[x.c.getAttribute('href')]; if (e) { x.r._a += S().norm(e); x.r._w = null; } });
      if (input.value) run();
    }).catch(function () {});
    function run() {
      var ws = S().words(input.value), shown = 0;
      recs.forEach(function (x) {
        var ok = (!f.u || x.c.dataset.u === f.u) && (!f.p || (' ' + x.c.dataset.p + ' ').indexOf(' ' + f.p + ' ') >= 0) &&
          (!ws.length || S().score(ws, x.r) !== null);
        x.c.hidden = !ok; if (ok) shown++;
      });
      secs.forEach(function (s) { s.hidden = !$$('a.gcard[data-u]', s).some(function (c) { return !c.hidden; }); });
      out.textContent = shown === cards.length ? plural(shown, 'guide', 'guides') : plural(shown, 'guide affiché', 'guides affichés') + ' sur ' + cards.length;
      empty.hidden = shown > 0;
      $('.gf-clear', box).hidden = !(input.value.trim() || f.u || f.p);
    }
    $$('.chip', box).forEach(function (b) {
      b.addEventListener('click', function () {
        f[b.dataset.f] = b.dataset.v;
        $$('.chip[data-f="' + b.dataset.f + '"]', box).forEach(function (o) { o.setAttribute('aria-pressed', o === b ? 'true' : 'false'); });
        run();
      });
    });
    input.addEventListener('input', run);
    $('.gf-form', box).addEventListener('submit', function (e) { e.preventDefault(); run(); });
    input.addEventListener('keydown', function (e) { if (e.key === 'Escape' && input.value) { input.value = ''; run(); } });
    $$('.gf-reset, .gf-clear', box).forEach(function (r) {
      r.addEventListener('click', function () {
        input.value = ''; f = { u: '', p: '' };
        $$('.chip', box).forEach(function (o) { o.setAttribute('aria-pressed', o.dataset.v ? 'false' : 'true'); });
        run(); input.focus();
      });
    });
    var q = new URLSearchParams(location.search).get('q');
    if (q) { input.value = q; var hq = $('form.search input'); if (hq) hq.value = ''; }
    run();
  }

  /* ---------- 3 et 4. Filtre de liste générique (questions-réponses, glossaire) ---------- */
  function listFilter(o) {
    var input = $(o.input); if (!input) return;
    var wrap = input.closest('[hidden]'); if (wrap) wrap.hidden = false;
    var out = $(o.count), empty = $(o.empty), items = o.items();
    items.forEach(function (it) { it.r = rec(it.title, it.text); });
    function run() {
      var ws = S().words(input.value), shown = 0;
      items.forEach(function (it) {
        var ok = !ws.length || S().score(ws, it.r) !== null;
        it.els.forEach(function (e) { e.hidden = !ok; }); if (ok) shown++;
        if (o.open && it.els[0].tagName === 'DETAILS') it.els[0].open = !!ws.length && ok && shown <= 3;
      });
      o.groups().forEach(function (g) { g.hidden = !o.visible(g); });
      out.textContent = !ws.length ? plural(items.length, o.unit[0], o.unit[1]) : plural(shown, o.unit[0], o.unit[1]) + ' sur ' + items.length;
      empty.hidden = shown > 0;
    }
    input.addEventListener('input', run);
    input.addEventListener('keydown', function (e) { if (e.key === 'Escape' && input.value) { input.value = ''; run(); } });
    var rs = $(o.reset); if (rs) rs.addEventListener('click', function () { input.value = ''; run(); input.focus(); });
    run();
  }
  function qa() {
    if (!$('#qaq')) return;
    listFilter({ input: '#qaq', count: '#qa-n', empty: '.qa-empty', reset: '.qa-reset', unit: ['question', 'questions'], open: true,
      items: function () { return $$('main section[id] .faq > details').map(function (d) { var s = $('summary', d).textContent; return { title: s, text: d.textContent, els: [d] }; }); },
      groups: function () { return $$('main section[id]').filter(function (s) { return $('.faq > details', s); }); },
      visible: function (g) { return $$('.faq > details', g).some(function (d) { return !d.hidden; }); } });
  }
  function gloss() {
    if (!$('#glq')) return;
    listFilter({ input: '#glq', count: '#gl-n', empty: '.gl-empty', reset: '.gl-reset', unit: ['terme', 'termes'],
      items: function () {
        return $$('main section[id] dl > dt').map(function (dt) {
          var els = [dt], n = dt.nextElementSibling; while (n && n.tagName === 'DD') { els.push(n); n = n.nextElementSibling; }
          return { title: dt.textContent, text: els.map(function (e) { return e.textContent; }).join(' '), els: els };
        });
      },
      groups: function () { return $$('main section[id]').filter(function (s) { return $('dl > dt', s); }); },
      visible: function (g) { return $$('dl > dt', g).some(function (d) { return !d.hidden; }); } });
    /* lettre ciblée par la barre alphabétique : si elle est masquée par un filtre, on efface le filtre */
    $$('.gl-az a').forEach(function (a) {
      a.addEventListener('click', function () {
        var t = document.getElementById(a.getAttribute('href').slice(1)); var i = $('#glq');
        if (t && t.hidden && i) { i.value = ''; i.dispatchEvent(new Event('input')); }
      });
    });
  }

  /* ---------- 5. Checklist à cocher, imprimer et partager ---------- */
  function checklist() {
    var tools = $('#ck-tools'); if (!tools) return;
    var KEY = 'tp_print_checklist_v1', state = {};
    try { state = JSON.parse(localStorage.getItem(KEY) || '{}') || {}; } catch (e) { state = {}; }
    if (typeof state !== 'object' || Array.isArray(state)) state = {};
    var lis = $$('#checklist ul.check > li'), boxes = [];
    lis.forEach(function (li, i) {
      var k = S().norm(li.textContent).trim().slice(0, 80);
      var id = 'ck-' + (i + 1);
      var cb = document.createElement('input'); cb.type = 'checkbox'; cb.className = 'ck'; cb.id = id; cb.checked = !!state[k];
      var lab = document.createElement('label'); lab.htmlFor = id;
      while (li.firstChild) lab.appendChild(li.firstChild);
      li.appendChild(cb); li.appendChild(lab); li.classList.add('ck-li');
      cb.addEventListener('change', function () { if (cb.checked) state[k] = 1; else delete state[k]; save(); prog(); });
      boxes.push(cb);
    });
    $$('#checklist ul.check').forEach(function (u) { u.classList.add('ck-live'); });
    function save() { try { localStorage.setItem(KEY, JSON.stringify(state)); } catch (e) {} }
    var bar = $('.dg-bar', tools), n = $('#ck-n');
    function prog() {
      var d = boxes.filter(function (b) { return b.checked; }).length, t = boxes.length;
      n.textContent = d + ' élément' + (d > 1 ? 's' : '') + ' coché' + (d > 1 ? 's' : '') + ' sur ' + t + (d === t ? ' : votre kit est complet.' : '');
      bar.setAttribute('aria-valuenow', d); bar.setAttribute('aria-valuemax', t);
      bar.firstElementChild.style.width = (t ? Math.round(d / t * 100) : 0) + '%';
    }
    $$('[hidden]', tools).forEach(function (e) { if (!e.classList.contains('share-msg')) e.hidden = false; });
    $('#ck-print').addEventListener('click', function () { window.print(); });
    $('#ck-reset').addEventListener('click', function () {
      if (!boxes.some(function (b) { return b.checked; })) return;
      if (!confirm('Décocher toutes les cases de cette checklist ?')) return;
      boxes.forEach(function (b) { b.checked = false; }); state = {}; save(); prog();
    });
    prog();
  }

  function init() { diag(); hub(); qa(); gloss(); checklist(); }
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', init); else init();
})();
