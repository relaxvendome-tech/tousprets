/* Tous prêts — recherche dans les guides (hors ligne, sans service externe) */
(function () {
  var form = document.querySelector('form.search');
  var input = form && form.querySelector('input');
  var list = form && form.querySelector('.search-res');
  var data = null, results = [];
  function norm(s) { return ' ' + (s || '').toLowerCase().normalize('NFD').replace(/[\u0300-\u036f]/g, '').replace(/[^a-z0-9]+/g, ' ') + ' '; }
  function load(cb) {
    if (data) return cb();
    fetch('search-index.json').then(function (r) { return r.json(); }).then(function (j) {
      data = j.map(function (p) { p._t = norm(p.t); p._a = norm(p.t + ' ' + p.d + ' ' + p.k); return p; });
      cb();
    }).catch(function () { data = []; cb(); });
  }
  var SYN = {courant:'electricite coupure', panne:'coupure', blackout:'coupure electricite', tremblement:'seisme', incendie:'feu', flamme:'feu',
    nucleaire:'iode', radioactif:'iode nucleaire', ouragan:'cyclone', typhon:'cyclone', chaleur:'canicule', froid:'vague', neige:'froid voiture',
    chien:'animaux', chat:'animaux', bebe:'bebe', enfant:'enfants ecole', vieux:'agee', senior:'agee', handicape:'handicap', fauteuil:'handicap',
    sirene:'alerte signal', alarme:'alerte', torche:'lampe', lampe:'lampe frontale', batterie:'batterie', telephone:'recharger', boire:'eau', potable:'eau',
    manger:'aliments', nourriture:'aliments', conserve:'aliments', sac:'sac', valise:'sac', liste:'checklist', imprimer:'checklist', prix:'pas cher', gratuit:'gratuit',
    medicament:'trousse medicaments', pharmacie:'trousse', guerre:'tensions', attentat:'attaque', piratage:'cyberattaque', virus:'cyberattaque', gaz:'groupe monoxyde', co:'monoxyde'};
  function lev1(a, b) { if (Math.abs(a.length - b.length) > 1) return false; var i = 0, j = 0, e = 0;
    while (i < a.length && j < b.length) { if (a[i] === b[j]) { i++; j++; continue; } if (++e > 1) return false;
      if (a.length > b.length) i++; else if (b.length > a.length) j++; else { i++; j++; } } return e + (a.length - i) + (b.length - j) <= 1; }
  function fuzzy(w, p) { if (p._a.indexOf(' ' + w) >= 0) return 2; if (SYN[w]) { var sy = SYN[w].split(' '); if (sy.some(function (x) { return p._t.indexOf(' ' + x) >= 0; })) return 3; if (sy.some(function (x) { return p._a.indexOf(' ' + x) >= 0; })) return 1; }
    if (w.length >= 5) { if (!p._w) p._w = p._a.trim().split(' '); for (var k = 0; k < p._w.length; k++) if (lev1(w, p._w[k])) return 1; } return 0; }
  function words(q) {
    var STOP = ' de la le les du des en un une et au aux mon ma mes que quoi faire comment pour avec sur dans est il on se cas en ';
    var nq = norm(q).replace(/ tremblements? de terre /g, ' seisme ').replace(/ feux? de foret /g, ' feu foret ').replace(/ panne de courant | panne d electricite /g, ' coupure electricite ');
    return nq.trim().split(/\s+/).filter(function (w) { return w.length > 1 && STOP.indexOf(' ' + w + ' ') < 0; });
  }
  /* Score d'un enregistrement { _t: titre normalisé, _a: tout le texte normalisé, u: url } ; null = ne correspond pas */
  function score(ws, p) {
    var sc = 0, miss = 0;
    for (var i = 0; i < ws.length; i++) {
      var f = fuzzy(ws[i], p); if (!f) { miss++; continue; }
      sc += (p._t.indexOf(' ' + ws[i]) >= 0 ? 3 : f) + ((p.u || '').indexOf(ws[i]) >= 0 ? 2 : 0);
    }
    if (!sc || miss > Math.floor(ws.length / 2)) return null;
    return sc - miss;
  }
  /* API partagée avec pages.js (filtres du hub, des questions, du glossaire) */
  window.TPSearch = { norm: norm, words: words, score: score };
  if (!form || !input || !list) return;
  function find(q) {
    var ws = words(q);
    if (!ws.length) return [];
    return data.map(function (p) {
      var s = score(ws, p);
      return s === null ? null : { p: p, s: s };
    }).filter(Boolean).sort(function (a, b) { return b.s - a.s; }).slice(0, 7).map(function (x) { return x.p; });
  }
  function esc(s) { return s.replace(/[&<>"]/g, function (c) { return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]; }); }
  function render() {
    results = find(input.value);
    if (!input.value.trim()) { list.hidden = true; list.innerHTML = ''; return; }
    list.innerHTML = results.length ? results.map(function (p) {
      var u = /^[a-z0-9-]+\.html(#[\w-]*)?$/i.test(p.u || '') ? p.u : 'tous-les-guides.html';
      return '<li><a href="' + esc(u) + '"><em class="sr-cat">' + esc(p.c || '') + '</em><strong>' + esc(p.t) + '</strong><span>' + esc(p.d) + '</span></a></li>';
    }).join('') : '<li class="none">Aucun guide trouvé pour cette recherche. Essayez un mot plus simple (« eau », « radio », « coupure ») ou parcourez <a href="tous-les-guides.html">tous les guides</a>.</li>';
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
