/* nav.js — navigation v4 de tousprets.fr (menu mobile, sous-menu « Outils pratiques »). Sans dépendance. */
(function () {
  'use strict';
  var nav = document.getElementById('mainnav');
  var toggle = document.querySelector('.nav-toggle');
  if (!nav || !toggle) return;
  var closeBtn = nav.querySelector('.mn-close');
  var subBtn = nav.querySelector('.mn-btn');
  var sub = subBtn ? document.getElementById(subBtn.getAttribute('aria-controls')) : null;
  var mq = window.matchMedia('(max-width: 900px)');
  var backdrop = null;
  var hoverTimer = null;
  var hoverOpened = false;

  function focusables() {
    return Array.prototype.filter.call(
      nav.querySelectorAll('a[href], button:not([disabled])'),
      function (el) { return el.offsetParent !== null; }
    );
  }

  /* ---------- Tiroir mobile ---------- */
  function isOpen() { return nav.classList.contains('is-open'); }

  function openMenu() {
    nav.classList.add('is-open');
    toggle.setAttribute('aria-expanded', 'true');
    nav.setAttribute('role', 'dialog');
    nav.setAttribute('aria-modal', 'true');
    document.documentElement.classList.add('mn-lock');
    backdrop = document.createElement('div');
    backdrop.className = 'mn-backdrop';
    backdrop.addEventListener('click', function () { closeMenu(true); });
    nav.parentNode.insertBefore(backdrop, nav);
    var cur = nav.querySelector('[aria-current]');
    if (cur && cur.classList.contains('mn-sa')) setSub(true);
    (closeBtn || focusables()[0]).focus();
  }

  function closeMenu(returnFocus) {
    if (!isOpen()) return;
    nav.classList.remove('is-open');
    toggle.setAttribute('aria-expanded', 'false');
    nav.removeAttribute('role');
    nav.removeAttribute('aria-modal');
    document.documentElement.classList.remove('mn-lock');
    if (backdrop) { backdrop.remove(); backdrop = null; }
    if (returnFocus) toggle.focus();
  }

  toggle.addEventListener('click', function () { isOpen() ? closeMenu(true) : openMenu(); });
  if (closeBtn) closeBtn.addEventListener('click', function () { closeMenu(true); });

  nav.addEventListener('keydown', function (e) {
    if (!isOpen() || e.key !== 'Tab') return;
    var f = focusables();
    if (!f.length) return;
    var first = f[0], last = f[f.length - 1];
    if (e.shiftKey && document.activeElement === first) { e.preventDefault(); last.focus(); }
    else if (!e.shiftKey && document.activeElement === last) { e.preventDefault(); first.focus(); }
  });

  function onMq() { if (!mq.matches) closeMenu(false); setSub(false); }
  if (mq.addEventListener) mq.addEventListener('change', onMq); else if (mq.addListener) mq.addListener(onMq);

  /* ---------- Sous-menu « Outils pratiques » ---------- */
  function subOpen() { return subBtn && subBtn.getAttribute('aria-expanded') === 'true'; }
  function setSub(open) { if (subBtn) subBtn.setAttribute('aria-expanded', open ? 'true' : 'false'); }
  function subLinks() { return sub ? Array.prototype.slice.call(sub.querySelectorAll('a')) : []; }

  if (subBtn && sub) {
    subBtn.addEventListener('click', function () {
      if (hoverOpened) { hoverOpened = false; setSub(true); return; }
      setSub(!subOpen());
    });
    subBtn.addEventListener('keydown', function (e) {
      if (mq.matches) return;
      if (e.key === 'ArrowDown') { e.preventDefault(); setSub(true); subLinks()[0].focus(); }
      else if (e.key === 'ArrowUp') { e.preventDefault(); setSub(true); var l = subLinks(); l[l.length - 1].focus(); }
    });
    sub.addEventListener('keydown', function (e) {
      if (mq.matches) return;
      var l = subLinks(), i = l.indexOf(document.activeElement);
      if (e.key === 'ArrowDown') { e.preventDefault(); l[(i + 1) % l.length].focus(); }
      else if (e.key === 'ArrowUp') { e.preventDefault(); l[(i - 1 + l.length) % l.length].focus(); }
      else if (e.key === 'Home') { e.preventDefault(); l[0].focus(); }
      else if (e.key === 'End') { e.preventDefault(); l[l.length - 1].focus(); }
    });
    var li = subBtn.parentNode;
    li.addEventListener('pointerenter', function (e) {
      if (e.pointerType !== 'mouse' || mq.matches) return;
      clearTimeout(hoverTimer);
      if (!subOpen()) { hoverOpened = true; setSub(true); }
    });
    li.addEventListener('pointerleave', function (e) {
      if (e.pointerType !== 'mouse' || mq.matches) return;
      clearTimeout(hoverTimer);
      hoverOpened = false;
      hoverTimer = setTimeout(function () { if (!li.contains(document.activeElement)) setSub(false); }, 250);
    });
    li.addEventListener('focusout', function (e) {
      if (mq.matches) return;
      if (!li.contains(e.relatedTarget)) setSub(false);
    });
  }

  /* ---------- Échap et clic extérieur ---------- */
  document.addEventListener('keydown', function (e) {
    if (e.key !== 'Escape' && e.key !== 'Esc') return;
    if (subOpen() && !mq.matches) {
      var inSub = sub && sub.contains(document.activeElement);
      setSub(false);
      if (inSub) subBtn.focus();
    } else if (isOpen()) {
      closeMenu(true);
    }
  });
  document.addEventListener('click', function (e) {
    if (isOpen() && !nav.contains(e.target) && !toggle.contains(e.target)) closeMenu(false);
    if (!mq.matches && subOpen() && subBtn && !subBtn.parentNode.contains(e.target)) setSub(false);
  });
})();
