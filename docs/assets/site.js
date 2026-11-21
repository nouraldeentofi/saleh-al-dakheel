/* Saleh Al Dakheel — behaviour. Vanilla, no dependencies.
   Sheets that stack, the live sheet counter, the landing full stops, tabs, the Gantt,
   the ownership switch, the values deck, swipe rows, the phone menu and capsule. */
(() => {
  const d = document, html = d.documentElement, W = window;
  const RTL = html.dir === 'rtl';
  const DIRX = RTL ? -1 : 1;
  const RM = W.matchMedia('(prefers-reduced-motion: reduce)');
  const reduced = () => RM.matches;
  const $ = (s, r = d) => r.querySelector(s);
  const $$ = (s, r = d) => Array.from(r.querySelectorAll(s));
  const store = {
    get(k) { try { return localStorage.getItem(k); } catch (e) { return null; } },
    set(k, v) { try { localStorage.setItem(k, v); } catch (e) { /* private mode */ } }
  };
  if (/[?&]noglass/.test(location.search)) html.classList.add('no-glass');

  /* ---------------------------------------------------------- sheets */
  const sheets = $$('[data-sheet]');
  const stacked = sheets.filter(s => s.hasAttribute('data-stack'));
  const roll = $('.counter-roll');
  const hdr = $('#hdr');
  const R = 32; // sheet overlap (the rounded top)

  function currentIndex() {
    const y = W.innerHeight * 0.42;
    let idx = 0;
    for (let i = 0; i < sheets.length; i++) {
      if (sheets[i].getBoundingClientRect().top <= y) idx = i;
    }
    return idx;
  }

  function measure() {
    const vh = W.innerHeight;
    const hs = stacked.map(s => s.offsetHeight);
    stacked.forEach((s, i) => s.style.setProperty('--stick', Math.min(0, vh - hs[i]) + 'px'));
    if (typeof pairs !== 'undefined') pairs.forEach(p => { p.h = 0; });
  }

  // pairs of [covered element, element that covers it]; the shade is a real element so only it repaints
  const pairs = [];
  stacked.forEach(s => {
    const next = sheets[sheets.indexOf(s) + 1];
    if (next) pairs.push({ el: s, next, gap: -R, target: s, shade: $(':scope > .shade', s), k: .045, o: .42 });
  });
  const engs = $$('.eng');
  engs.forEach((e, i) => {
    const card = $('.eng-card', e);
    if (engs[i + 1]) pairs.push({ el: e, next: engs[i + 1], gap: 22, target: card, shade: $('.shade', card), k: .05, o: .25 });
  });

  let lastCi = -1, ticking = false;
  function frame() {
    ticking = false;
    const vh = W.innerHeight, sy = W.scrollY;
    // read everything first ...
    const ci = roll ? currentIndex() : 0;
    const vals = reduced() ? [] : pairs.map(p => {
      const a = p.el.getBoundingClientRect().top, b = p.next.getBoundingClientRect().top, h = p.h || (p.h = p.el.offsetHeight);
      let c = ((a + h + p.gap) - b) / Math.min(h, vh);
      c = c < 0 ? 0 : c > 1 ? 1 : Math.round(c * 1000) / 1000;
      return [c, c >= 1 && b <= 0];
    });
    // ... then write
    hdr && hdr.classList.toggle('is-scrolled', sy > 24);
    vals.forEach(([c, gone], i) => {
      const p = pairs[i];
      if (p.c !== c) {
        p.c = c;
        p.target.style.scale = c ? String(1 - c * p.k) : '';
        if (p.shade) p.shade.style.opacity = c ? String(c * p.o) : '';
      }
      const cov = c > 0.02 && p.target.classList.contains('sheet');
      if (p.cov !== cov) { p.cov = cov; p.target.classList.toggle('is-covering', cov); }
      const g = gone && p.target.classList.contains('sheet');
      if (p.gone !== g) { p.gone = g; p.target.classList.toggle('is-gone', g); }
    });
    if (roll && ci !== lastCi) { lastCi = ci; roll.style.setProperty('--ci', ci); }
    if (progressFallback) progressFallback.style.setProperty('--p', Math.min(1, sy / Math.max(1, d.documentElement.scrollHeight - vh)));
  }
  const progressFallback = (W.CSS && CSS.supports && CSS.supports('animation-timeline: scroll()')) ? null : $('.progress span');
  let scrollT = null;
  function onScroll() {
    if (!ticking) { ticking = true; requestAnimationFrame(frame); }
    if (!scrollT) html.classList.add('is-scrolling');
    clearTimeout(scrollT);
    scrollT = setTimeout(() => { scrollT = null; html.classList.remove('is-scrolling'); }, 180);
  }
  W.addEventListener('scroll', onScroll, { passive: true });

  /* ---------------------------------------------------------- language: remember + keep the section */
  $$('[data-lang]').forEach(a => a.addEventListener('click', () => {
    store.set('sd-lang', a.dataset.lang);
    const s = sheets[currentIndex()];
    try { if (s && s.id && s.id !== 'top') sessionStorage.setItem('sd-anchor', JSON.stringify({ id: s.id, page: html.dataset.page })); } catch (e) { }
  }));
  function restoreAnchor() {
    try {
      const a = JSON.parse(sessionStorage.getItem('sd-anchor') || 'null');
      sessionStorage.removeItem('sd-anchor');
      if (!a || a.page !== html.dataset.page || location.hash) return;
      const el = d.getElementById(a.id);
      if (el) W.scrollTo({ top: el.getBoundingClientRect().top + W.scrollY, behavior: 'instant' });
    } catch (e) { }
  }

  /* ---------------------------------------------------------- reveal + full stops */
  const revealIO = 'IntersectionObserver' in W ? new IntersectionObserver(entries => {
    entries.forEach(e => {
      if (e.isIntersecting) { e.target.classList.add('in'); revealIO.unobserve(e.target); }
    });
  }, { rootMargin: '0px 0px -6% 0px', threshold: 0.1 }) : null;
  $$('[data-rv]').forEach(el => revealIO ? revealIO.observe(el) : el.classList.add('in'));
  const heroName = $('.hero-name');
  if (heroName) { heroName.classList.add('in'); $$('.m').forEach(m => m.classList.add('in')); }

  /* concept background: ripples spread from the section's first full stop */
  function placeRipples() {
    $$('.ripples').forEach(rp => {
      const sec = rp.parentElement;
      if (!sec || sec.classList.contains('menu-bg')) return;
      const stop = $('.stop', sec);
      if (!stop) return;
      const r = sec.getBoundingClientRect(), s = stop.getBoundingClientRect();
      const cx = s.left + s.width / 2, cy = s.top + s.height / 2;
      rp.style.setProperty('--rx', Math.round(cx - r.left) + 'px');
      rp.style.setProperty('--ry', Math.round(cy - r.top) + 'px');
    });
  }

  /* pause what is off screen */
  if ('IntersectionObserver' in W) {
    const pauseIO = new IntersectionObserver(es => es.forEach(e => e.target.classList.toggle('is-paused', !e.isIntersecting)), { rootMargin: '80px' });
    $$('.sheet, .foot').forEach(s => pauseIO.observe(s));
  }

  /* ---------------------------------------------------------- count up */
  const counts = $$('.count');
  if (counts.length && 'IntersectionObserver' in W && !reduced()) {
    const run = el => {
      el.style.inlineSize = el.getBoundingClientRect().width + 'px';  // pin the final number's width: counting never moves the words around it
      const to = +el.dataset.to, t0 = performance.now(), dur = 1300;
      const step = now => {
        const k = Math.min(1, (now - t0) / dur), v = Math.round(to * (1 - Math.pow(1 - k, 3)));
        if (el.firstChild) el.firstChild.nodeValue = v; else el.textContent = v;
        if (k < 1) requestAnimationFrame(step);
      };
      requestAnimationFrame(step);
    };
    const cIO = new IntersectionObserver(es => es.forEach(e => {
      if (e.isIntersecting) { cIO.unobserve(e.target); run(e.target); }
    }), { threshold: 0.6 });
    counts.forEach(el => cIO.observe(el));
  }

  /* ---------------------------------------------------------- tabs (the job) */
  $$('[data-tabs]').forEach(w => {
    const list = $('[role=tablist]', w), tabs = $$('[role=tab]', w), panels = $$('[role=tabpanel]', w), dot = $('.tab-dot', w);
    const place = () => {
      const t = tabs.find(x => x.getAttribute('aria-selected') === 'true') || tabs[0];
      const x = RTL ? -(list.clientWidth - (t.offsetLeft + t.offsetWidth)) : t.offsetLeft;
      dot.style.setProperty('--tx', (RTL ? x + 6 : x - 6) + 'px');
      dot.style.setProperty('--ty', (t.offsetTop - 6) + 'px');
    };
    const select = (i, focus) => {
      tabs.forEach((t, j) => { t.setAttribute('aria-selected', j === i); t.tabIndex = j === i ? 0 : -1; });
      panels.forEach((p, j) => { p.classList.toggle('is-on', j === i); p.inert = j !== i; });
      place();
      if (focus) tabs[i].focus();
    };
    tabs.forEach((t, i) => {
      t.addEventListener('click', () => select(i));
      t.addEventListener('keydown', e => {
        const n = tabs.length;
        let k = null;
        if (e.key === 'ArrowRight') k = RTL ? i - 1 : i + 1;
        if (e.key === 'ArrowLeft') k = RTL ? i + 1 : i - 1;
        if (e.key === 'Home') k = 0;
        if (e.key === 'End') k = n - 1;
        if (k !== null) { e.preventDefault(); select((k + n) % n, true); }
      });
    });
    w._place = place;
    dot.style.transition = 'none';
    place();
    requestAnimationFrame(() => requestAnimationFrame(() => { dot.style.transition = ''; html.classList.add('tabs-ready'); }));
  });

  /* ---------------------------------------------------------- Gantt (career) */
  const g = $('[data-gantt]');
  if (g) {
    const seq = g.dataset.seq.split(',');
    const capsBox = $('#gcap', g);
    let cur = seq[seq.length - 1], user = false, timer = null, visible = false;
    const select = (id, byUser) => {
      cur = id;
      $$('.g-cap', g).forEach(c => { const on = c.dataset.g === id; c.classList.toggle('is-on', on); c.setAttribute('aria-hidden', on ? 'false' : 'true'); });
      $$('button[data-g]', g).forEach(b => b.setAttribute('aria-pressed', b.dataset.g === id));
      $$('.g-mile', g).forEach(m => m.classList.toggle('is-on', m.dataset.g === id));
      if (byUser) { user = true; stop(); capsBox.setAttribute('aria-live', 'polite'); }
    };
    $$('button[data-g]', g).forEach(b => b.addEventListener('click', () => select(b.dataset.g, true)));
    const tick = () => { select(seq[(seq.indexOf(cur) + 1) % seq.length]); };
    const start = () => { if (!timer && !user && !reduced() && visible) timer = setInterval(tick, 4200); };
    const stop = () => { clearInterval(timer); timer = null; };
    select(cur);
    if ('IntersectionObserver' in W) {
      let first = true;
      new IntersectionObserver(es => es.forEach(e => {
        visible = e.isIntersecting;
        if (visible) {
          if (first && !user && !reduced()) { first = false; setTimeout(() => { if (!user && visible) { select(seq[0]); start(); } }, 2600); }
          else start();
        } else stop();
      }), { threshold: 0.35 }).observe(g);
    }
    g.addEventListener('pointerenter', e => { if (e.pointerType === 'mouse') stop(); });
    g.addEventListener('pointerleave', e => { if (e.pointerType === 'mouse') start(); });
    g.addEventListener('focusin', stop);
  }

  /* ---------------------------------------------------------- ownership | interference */
  $$('[data-seg]').forEach(w => {
    const btns = $$('[role=tab]', w), panels = $$('[role=tabpanel]', w);
    const select = (i, focus) => {
      btns.forEach((b, j) => { b.setAttribute('aria-selected', j === i); b.tabIndex = j === i ? 0 : -1; });
      panels.forEach((p, j) => { p.classList.toggle('is-on', j === i); p.inert = j !== i; });
      w.dataset.state = i === 0 ? 'own' : 'int';
      if (focus) btns[i].focus();
    };
    btns.forEach((b, i) => {
      b.addEventListener('click', () => select(i));
      b.addEventListener('keydown', e => {
        if (['ArrowLeft', 'ArrowRight', 'Home', 'End'].includes(e.key)) { e.preventDefault(); select(i === 0 ? 1 : 0, true); }
      });
    });
  });

  /* ---------------------------------------------------------- values deck */
  $$('[data-deck]').forEach(w => {
    const stage = $('.deck-stage', w), cards = $$('.vcard', w), dots = $$('.deck-dots i', w);
    let order = cards.map((_, i) => i), busy = false, timer = null, visible = false, hold = 0;
    const paint = () => {
      order.forEach((ci, pos) => {
        const c = cards[ci];
        c.dataset.pos = pos;
        c.setAttribute('aria-hidden', pos === 0 ? 'false' : 'true');
      });
      dots.forEach((dd, i) => dd.classList.toggle('is-on', i === order[0]));
    };
    const next = () => {
      if (busy) return; busy = true;
      const top = cards[order[0]];
      top.style.transform = '';
      top.classList.add('is-out');
      setTimeout(() => {
        top.classList.remove('is-out');
        order.push(order.shift());
        paint();
        busy = false;
      }, reduced() ? 0 : 460);
    };
    const prev = () => {
      if (busy) return; busy = true;
      const back = cards[order[order.length - 1]];
      back.classList.add('is-in');
      order.unshift(order.pop());
      paint();
      void back.offsetWidth;
      back.classList.remove('is-in');
      setTimeout(() => { busy = false; }, reduced() ? 0 : 460);
    };
    const userAct = fn => { hold = Date.now(); fn(); };
    $('[data-deck-next]', w).addEventListener('click', () => userAct(next));
    $('[data-deck-prev]', w).addEventListener('click', () => userAct(prev));
    // swipe
    let sx = null, sy = 0, dx = 0, dragging = false;
    stage.addEventListener('pointerdown', e => { if (busy) return; sx = e.clientX; sy = e.clientY; dx = 0; dragging = false; });
    stage.addEventListener('pointermove', e => {
      if (sx === null) return;
      dx = e.clientX - sx;
      if (!dragging && Math.abs(dx) > 8 && Math.abs(dx) > Math.abs(e.clientY - sy)) { dragging = true; try { stage.setPointerCapture(e.pointerId); } catch (err) { } }
      if (dragging) cards[order[0]].style.transform = `translateX(${dx}px) rotate(${dx / 40}deg)`;
    });
    const end = () => {
      if (sx === null) return;
      const top = cards[order[0]];
      if (dragging && dx * DIRX < -50) { userAct(next); }
      else if (dragging && dx * DIRX > 50) { top.style.transform = ''; userAct(prev); }
      else top.style.transform = '';
      sx = null; dragging = false;
    };
    stage.addEventListener('pointerup', end);
    stage.addEventListener('pointercancel', end);
    w.addEventListener('keydown', e => {
      if (e.key === 'ArrowLeft') { e.preventDefault(); userAct(RTL ? next : prev); }
      if (e.key === 'ArrowRight') { e.preventDefault(); userAct(RTL ? prev : next); }
    });
    paint();
    const auto = () => { if (visible && !reduced() && Date.now() - hold > 9000 && !w.matches(':hover') && !w.contains(d.activeElement)) next(); };
    if ('IntersectionObserver' in W) new IntersectionObserver(es => es.forEach(e => {
      visible = e.isIntersecting;
      if (visible && !timer) timer = setInterval(auto, 5200);
      if (!visible) { clearInterval(timer); timer = null; }
    }), { threshold: 0.4 }).observe(w);
  });

  /* ---------------------------------------------------------- swipe rows (phones) */
  $$('[data-swipe]').forEach(row => {
    const items = Array.from(row.children), dots = $$('i', row.nextElementSibling || d.createElement('i'));
    let t = false;
    const upd = () => {
      t = false;
      if (row.scrollWidth <= row.clientWidth + 2) { row.classList.remove('has-c'); items.forEach(i => i.classList.remove('is-c')); return; }
      const rr = row.getBoundingClientRect(), mid = rr.left + rr.width / 2;
      let best = 0, bd = Infinity;
      items.forEach((it, i) => { const r = it.getBoundingClientRect(), dd = Math.abs(r.left + r.width / 2 - mid); if (dd < bd) { bd = dd; best = i; } });
      row.classList.add('has-c');
      items.forEach((it, i) => it.classList.toggle('is-c', i === best));
      dots.forEach((dd, i) => dd.classList.toggle('is-on', i === best));
    };
    row.addEventListener('scroll', () => { if (!t) { t = true; requestAnimationFrame(upd); } }, { passive: true });
    W.addEventListener('resize', upd);
    upd();
  });

  /* ---------------------------------------------------------- details on demand (role details, FAQ) */
  $$('.more-btn, .faq-q').forEach(b => b.addEventListener('click', () => {
    const open = b.getAttribute('aria-expanded') !== 'true';
    b.setAttribute('aria-expanded', open);
    const box = d.getElementById(b.getAttribute('aria-controls'));
    if (box) box.classList.toggle('open', open);
  }));

  /* ---------------------------------------------------------- copy email */
  $$('[data-copy]').forEach(b => b.addEventListener('click', () => {
    const v = b.dataset.copy;
    const done = () => {
      b.classList.add('is-done');
      const live = b.closest('.ccard') && $('.sr-live', b.closest('.ccard'));
      if (live) live.textContent = $('.copy-b', b).textContent.trim();
      clearTimeout(b._t);
      b._t = setTimeout(() => { b.classList.remove('is-done'); if (live) live.textContent = ''; }, 2400);
    };
    const legacy = () => {
      const ta = d.createElement('textarea'); ta.value = v; ta.setAttribute('readonly', ''); ta.style.position = 'fixed'; ta.style.opacity = '0';
      d.body.appendChild(ta); ta.select(); try { d.execCommand('copy'); } catch (e) { } ta.remove(); done();
    };
    if (navigator.clipboard && W.isSecureContext) navigator.clipboard.writeText(v).then(done, legacy); else legacy();
  }));

  /* ---------------------------------------------------------- phone: capsule + full-screen menu */
  const cap = $('#cap'), dot = $('#capDot'), menu = $('#menu'), act = $('#capAct');
  let menuOpen = false;
  const outside = () => $$('body > header, body > main, body > footer, body > .skip');
  function openMenu() {
    if (menuOpen) return; menuOpen = true;
    menu.hidden = false;
    const r = dot.getBoundingClientRect();
    menu.style.setProperty('--mx', Math.round(r.left + 27) + 'px');
    menu.style.setProperty('--my', Math.round(r.top + r.height / 2) + 'px');
    const rp = $('.ripples', menu);
    if (rp) { rp.style.setProperty('--rx', Math.round(r.left + 27) + 'px'); rp.style.setProperty('--ry', Math.round(r.top + r.height / 2) + 'px'); }
    void menu.offsetWidth;
    menu.classList.add('open');
    cap.classList.add('is-open');
    dot.setAttribute('aria-expanded', 'true');
    html.classList.add('lock');
    outside().forEach(el => { el.inert = true; });
    setTimeout(() => { const a = $('.menu-a[aria-current]', menu) || $('.menu-a', menu); a && a.focus({ preventScroll: true }); }, reduced() ? 0 : 260);
    syncAct();
  }
  function closeMenu(refocus) {
    if (!menuOpen) return; menuOpen = false;
    menu.classList.remove('open');
    cap.classList.remove('is-open');
    dot.setAttribute('aria-expanded', 'false');
    html.classList.remove('lock');
    outside().forEach(el => { el.inert = false; });
    setTimeout(() => { if (!menuOpen) menu.hidden = true; }, reduced() ? 0 : 480);
    if (refocus) dot.focus({ preventScroll: true });
    syncAct();
  }
  if (dot && menu) {
    dot.addEventListener('click', () => (menuOpen ? closeMenu(true) : openMenu()));
    d.addEventListener('keydown', e => {
      if (!menuOpen) return;
      if (e.key === 'Escape') { e.preventDefault(); closeMenu(true); return; }
      if (e.key === 'Tab') {
        const f = $$('a[href], button', menu).concat(dot).filter(el => el.offsetParent !== null || el === dot);
        const i = f.indexOf(d.activeElement);
        if (e.shiftKey && (i <= 0)) { e.preventDefault(); f[f.length - 1].focus(); }
        else if (!e.shiftKey && i === f.length - 1) { e.preventDefault(); f[0].focus(); }
      }
    });
    $$('.menu-a', menu).forEach(a => a.addEventListener('click', () => { if (a.hasAttribute('aria-current')) closeMenu(false); }));
    W.matchMedia('(min-width: 1024px)').addEventListener('change', e => { if (e.matches) closeMenu(false); });
  }

  // the capsule's "Email me" appears once the hero buttons have scrolled away, and hides near the footer
  let heroGone = false, footNear = false;
  function syncAct() {
    if (!act) return;
    const show = heroGone && !footNear && !menuOpen;
    cap.classList.toggle('has-act', show);
    act.setAttribute('aria-hidden', show ? 'false' : 'true');
    act.tabIndex = show ? 0 : -1;
  }
  let actAt = Infinity;
  const actMeasure = () => {
    const t = $('#heroCta');
    actAt = t ? t.getBoundingClientRect().bottom + W.scrollY : (sheets[0] ? sheets[0].offsetHeight * 0.6 : 400);
  };
  const actCheck = () => { const g = W.scrollY > actAt; if (g !== heroGone) { heroGone = g; syncAct(); } };
  if (act && 'IntersectionObserver' in W) {
    actMeasure();
    W.addEventListener('scroll', actCheck, { passive: true });
    const foot = $('#foot');
    if (foot) new IntersectionObserver(es => es.forEach(e => { footNear = e.isIntersecting; syncAct(); }), { rootMargin: '0px 0px 0px 0px' }).observe(foot);
  }

  /* ---------------------------------------------------------- layout passes */
  function layout() {
    if (W.scrollY < 5 && typeof actMeasure === 'function') actMeasure();
    measure();
    $$('[data-tabs]').forEach(w => w._place && w._place());
    placeRipples();
    frame();
  }
  if ('ResizeObserver' in W) {
    const ro = new ResizeObserver(() => { measure(); frame(); });
    stacked.forEach(s => ro.observe(s));
  }
  let rz;
  W.addEventListener('resize', () => { clearTimeout(rz); rz = setTimeout(layout, 120); });
  layout();
  restoreAnchor();
  if (d.fonts && d.fonts.ready) d.fonts.ready.then(layout);
  W.addEventListener('load', layout);
})();
