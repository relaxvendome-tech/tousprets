/* Tous prêts — bouton de partage : Web Share API, sinon copie du lien. */
(function () {
  var b = document.querySelector('.share-btn');
  if (!b) return;
  var msg = document.querySelector('.share-msg');
  var lab = b.querySelector('.share-l');
  if (!navigator.share && lab) lab.textContent = 'Copier le lien';
  function say(t) { if (msg) { msg.textContent = t; setTimeout(function () { msg.textContent = ''; }, 4000); } }
  function fallbackCopy(u) {
    var ta = document.createElement('textarea');
    ta.value = u; ta.setAttribute('readonly', ''); ta.style.position = 'fixed'; ta.style.opacity = '0';
    document.body.appendChild(ta); ta.select();
    var ok = false; try { ok = document.execCommand('copy'); } catch (e) {}
    document.body.removeChild(ta);
    say(ok ? 'Lien copié.' : 'Copiez l’adresse dans la barre du navigateur.');
  }
  b.addEventListener('click', function () {
    var c = document.querySelector('link[rel="canonical"]');
    var u = c ? c.href : location.href;
    var d = { title: document.title, url: u };
    if (navigator.share) {
      navigator.share(d).catch(function () {});
    } else if (navigator.clipboard && window.isSecureContext) {
      navigator.clipboard.writeText(u).then(function () { say('Lien copié.'); }, function () { fallbackCopy(u); });
    } else {
      fallbackCopy(u);
    }
  });
})();
