/* Tous prêts — recherche dans les guides (hors ligne, sans service externe) */
(function () {
  var form = document.querySelector('form.search');
  if (!form) return;
  var input = form.querySelector('input');
  var list = form.querySelector('.search-res');
  var data = null, results = [];
  function norm(s) { return ' ' + (s || '').toLowerCase().normalize('NFD').replace(/[\u0300-\u036f]/g, '').replace(/[^a-z0-9]+/g, ' ') + ' '; }
  function load(cb) {
    if (data) return cb();
    fetch('search-index.json').then(function (r) { return r.json(); }).then(function (j) {
      data = j.map(function (p) { p._t = norm(p.t); p._a = norm(p.t + ' ' + p.d + ' ' + p.k); return p; });
      cb();
    }).catch(function () { data = []; cb(); });
  }
  function find(q) {
    var words = norm(q).trim().split(/\s+/).filter(function (w) { return w.length > 1; });
    if (!words.length) return [];
    return data.map(function (p) {
      var score = 0;
      for (var i = 0; i < words.length; i++) {
        if (p._a.indexOf(' ' + words[i]) < 0) return null;
        score += p._t.indexOf(' ' + words[i]) >= 0 ? 3 : 1;
      }
      return { p: p, s: score };
    }).filter(Boolean).sort(function (a, b) { return b.s - a.s; }).slice(0, 7).map(function (x) { return x.p; });
  }
  function esc(s) { return s.replace(/[&<>"]/g, function (c) { return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]; }); }
  function render() {
    results = find(input.value);
    if (!input.value.trim()) { list.hidden = true; list.innerHTML = ''; return; }
    list.innerHTML = results.length ? results.map(function (p) {
      return '<li><a href="' + p.u + '"><strong>' + esc(p.t) + '</strong><span>' + esc(p.d) + '</span></a></li>';
    }).join('') : '<li class="none">Aucun guide trouvé. Essayez « eau », « radio » ou « coupure ».</li>';
    list.hidden = false;
  }
  input.addEventListener('input', function () { load(render); });
  input.addEventListener('focus', function () { if (input.value) load(render); });
  input.addEventListener('keydown', function (e) { if (e.key === 'Escape') { list.hidden = true; input.blur(); } });
  document.addEventListener('click', function (e) { if (!form.contains(e.target)) list.hidden = true; });
  form.addEventListener('submit', function (e) {
    e.preventDefault();
    load(function () { results = find(input.value); if (results[0]) location.href = results[0].u; else render(); });
  });
  var q = new URLSearchParams(location.search).get('q');
  if (q) { input.value = q; load(render); }
})();
