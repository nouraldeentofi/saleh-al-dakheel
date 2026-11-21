#!/usr/bin/env python3
"""Full check of the built site (part E of Nour's skill).

    cd /tmp/ghp && python3 -m http.server 8765 &     # /tmp/ghp/saleh-al-dakheel -> docs/
    python3 tests/test_site.py [--quick]

Writes tests/report.json and prints a summary. Screenshots go to tests/shots/.
"""
import json
import os
import sys
import time
from playwright.sync_api import sync_playwright

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BASE = os.environ.get("SITE", "http://localhost:8765/saleh-al-dakheel/")
AXE = open(os.environ.get("AXE", "/home/claude/tools/node_modules/axe-core/axe.min.js"), encoding="utf-8").read()
SHOTS = os.path.join(ROOT, "tests", "shots")
QUICK = "--quick" in sys.argv
os.makedirs(SHOTS, exist_ok=True)

PAGES = ["index.html", "career.html", "consulting.html", "approach.html", "credentials.html", "contact.html"]
ALL = [p for p in PAGES] + ["en/" + p for p in PAGES] + ["404.html"]
PHONES = [(320, 640), (360, 740), (390, 844), (412, 915), (430, 932)]
LAND = [(844, 390)]
TABLET = [(768, 1024)]
DESK = [(1024, 768), (1366, 768), (1440, 900)]
if QUICK:
    PHONES, DESK = [(390, 844)], [(1440, 900)]

INIT = """
window.__shifts = [];
try { new PerformanceObserver(l => { for (const e of l.getEntries()) window.__shifts.push({v: e.value, t: e.startTime, input: e.hadRecentInput,
  src: (e.sources || []).map(s => s.node ? (s.node.nodeName + '.' + (s.node.className && s.node.className.baseVal === undefined ? s.node.className : '')) : '?').slice(0, 4)}); })
  .observe({type: 'layout-shift', buffered: true}); } catch (e) {}
window.__frames = [];
"""

report = {"pages": {}, "errors": [], "summary": {}}


def url(p):
    return BASE + p + ("&" if "?" in p else "?") + "stay"


def scroll_through(pg, step=420, pause=60):
    h = pg.evaluate("document.documentElement.scrollHeight")
    y = 0
    while y < h:
        pg.evaluate(f"window.scrollTo(0,{y})")
        pg.wait_for_timeout(pause)
        y += step
        h = pg.evaluate("document.documentElement.scrollHeight")
    pg.evaluate("window.scrollTo(0, document.documentElement.scrollHeight)")
    pg.wait_for_timeout(500)


OVERFLOW_JS = """
() => {
  const vw = document.documentElement.clientWidth, out = [];
  const clipped = el => { for (let a = el.parentElement; a && a !== document.body; a = a.parentElement) {
      const s = getComputedStyle(a); if (/(hidden|clip|auto|scroll)/.test(s.overflowX + s.overflow)) return true;
      if (s.position === 'fixed') return false; } return false; };
  for (const el of document.querySelectorAll('body *')) {
    const s = getComputedStyle(el);
    if (s.display === 'none' || s.visibility === 'hidden' || el.closest('[hidden]')) continue;
    const r = el.getBoundingClientRect();
    if (!r.width) continue;
    if ((r.right > vw + 1 || r.left < -1) && !clipped(el)) out.push(el.tagName + '.' + (typeof el.className === 'string' ? el.className : '') + ' ' + Math.round(r.left) + '..' + Math.round(r.right));
  }
  return {sw: document.documentElement.scrollWidth, bw: document.body.scrollWidth, vw, out: out.slice(0, 8)};
}
"""

TARGETS_JS = """
() => {
  const bad = [];
  for (const el of document.querySelectorAll('a[href], button, [role=tab]')) {
    if (el.closest('[hidden]') || el.closest('[inert]') || el.classList.contains('skip')) continue;
    const s = getComputedStyle(el);
    if (s.display === 'none' || s.visibility === 'hidden' || +s.opacity === 0 || s.pointerEvents === 'none') continue;
    const r = el.getBoundingClientRect();
    if (!r.width || !r.height) continue;
    if (r.width < 43.5 || r.height < 43.5) bad.push((el.className || el.tagName) + ' ' + Math.round(r.width) + 'x' + Math.round(r.height) + ' "' + el.textContent.trim().slice(0, 24) + '"');
  }
  return bad;
}
"""

UNDERLINE_JS = """
() => { const bad = []; for (const el of document.querySelectorAll('a, button')) {
  const s = getComputedStyle(el); if (s.textDecorationLine !== 'none') bad.push(el.className + ':' + s.textDecorationLine); }
  return bad; }
"""

SIBLINGS_JS = """
() => {
  const groups = {'.ctile': '.ctiles', '.vc': '.vcs', '.eng-card': '.engs', '.ccard': '.ccards', '.foot-cards .ccard': '.foot-cards', '.tab': '.tablist', '.seg-b': '.seg-ctl', '.lane': '.lanes', '.names li': '.names', '.panel': '.panels', '.g-cap': '.g-caps', '.vcard': '.deck-stage'};
  const out = [];
  for (const [sel, wrap] of Object.entries(groups)) {
    document.querySelectorAll(wrap).forEach(w => {
      const items = Array.from(w.querySelectorAll(sel)).filter(e => e.offsetParent !== null);
      const rows = {};
      items.forEach(e => { const t = Math.round(e.offsetTop); (rows[t] = rows[t] || []).push(e); });
      Object.values(rows).forEach(r => { if (r.length < 2) return;
        const hs = r.map(e => e.offsetHeight); const d = Math.max(...hs) - Math.min(...hs);
        if (d > 1 && !['.ccard', '.names li'].includes(sel)) out.push(sel + ' heights differ by ' + d + 'px (' + hs.join(',') + ')');
      });
      items.forEach(e => { const r = e.getBoundingClientRect();
        e.querySelectorAll('*').forEach(c => { const cr = c.getBoundingClientRect(); if (!cr.width) return;
          if (getComputedStyle(c).position === 'absolute') return;
          if (cr.right > r.right + 1.5 || cr.left < r.left - 1.5 || cr.bottom > r.bottom + 1.5) out.push(sel + ' child ' + c.className + ' sticks out'); }); });
    });
  }
  return out.slice(0, 12);
}
"""

TYPO_JS = """
() => {
  const out = {lh: [], ls: [], fonts: {}, measure: []};
  const ar = document.documentElement.lang === 'ar';
  document.querySelectorAll('p, li, .faq-a').forEach(el => {
    if (!el.offsetParent || !el.textContent.trim()) return;
    const s = getComputedStyle(el);
    if (ar && el.closest('[lang=en]') === null) {
      const lh = parseFloat(s.lineHeight) / parseFloat(s.fontSize);
      const isHead = /(h1|h2|motto|hero-name|foot-name|menu-n|next-n|quote|dots-t|seg-t|panel-t|eng-name|ctile-n|g-cap-t|edu-s|vcard-n|names|mini|prog-n|maker|copy-r|eng-no|pno|g-label|meta|tags|steps|edu-l|chip|dots-l)/.test(el.className + ' ' + (el.parentElement ? el.parentElement.className : '') + ' ' + (el.closest('blockquote,.names,.tags,.meta,.steps,.edu-l,.mini-head,.menu-list,.fnav,.g-chips') ? 'quote' : ''));
      if (!isHead && lh < 1.69 && el.textContent.trim().length > 40) out.lh.push(el.className + ' ' + lh.toFixed(2));
    }
    if (ar && !el.closest('[lang=en],[dir=ltr]') && s.letterSpacing !== 'normal' && parseFloat(s.letterSpacing) !== 0) out.ls.push(el.className + ' ' + s.letterSpacing);
  });
  document.querySelectorAll('.lede, .points li, .faq-a, .big-p, .eng-t, .g-cap-x').forEach(el => {
    if (!el.offsetParent) return;
    const lines = Math.round(el.getBoundingClientRect().height / parseFloat(getComputedStyle(el).lineHeight));
    if (lines >= 2) out.measure.push(Math.round(el.textContent.trim().length / lines));
  });
  for (const f of ['700 20px "Kufam SD"', '400 20px "Alexandria SD"', '600 20px "Alexandria SD"', '400 20px "Outfit SD"', '600 20px "Outfit SD"', '700 20px "Outfit SD"'])
    out.fonts[f] = document.fonts.check(f, ar ? 'صالح' : 'Saleh');
  return out;
}
"""

A11Y_JS = """
() => { const bad = [];
  document.querySelectorAll('button, a[href]').forEach(el => {
    const name = (el.getAttribute('aria-label') || el.textContent || '').trim();
    if (!name && !el.querySelector('img[alt]:not([alt=""])')) bad.push('no name: ' + el.outerHTML.slice(0, 80));
    if (getComputedStyle(el).cursor !== 'pointer') bad.push('no pointer: ' + (el.className || el.tagName));
  });
  document.querySelectorAll('svg').forEach(s => { if (!s.closest('[aria-hidden=true]') && s.getAttribute('aria-hidden') !== 'true') bad.push('svg not hidden'); });
  document.querySelectorAll('img').forEach(i => { if (!i.hasAttribute('alt')) bad.push('img without alt'); });
  return bad.slice(0, 10); }
"""

GLASS_JS = """
() => {
  const parse = c => { const m = c.match(/[\\d.]+/g).map(Number); return {r: m[0], g: m[1], b: m[2], a: m[3] === undefined ? 1 : m[3]}; };
  const lum = c => { const f = v => { v /= 255; return v <= .03928 ? v / 12.92 : Math.pow((v + .055) / 1.055, 2.4); }; return .2126 * f(c.r) + .7152 * f(c.g) + .0722 * f(c.b); };
  const over = (f, b) => ({r: f.r * f.a + b.r * (1 - f.a), g: f.g * f.a + b.g * (1 - f.a), b: f.b * f.a + b.b * (1 - f.a), a: 1});
  const cr = (a, b) => { const x = lum(a), y = lum(b); return (Math.max(x, y) + .05) / (Math.min(x, y) + .05); };
  const backs = [{r: 61, g: 59, b: 142, a: 1}, {r: 241, g: 241, b: 243, a: 1}, {r: 255, g: 255, b: 255, a: 1}, {r: 28, g: 27, b: 71, a: 1}];
  const out = [];
  document.querySelectorAll('.pill, .glass-dark, .glass-light, .cap-dot, .cap-act, .vcard[data-pos="0"]').forEach(g => {
    if (!g.offsetParent && getComputedStyle(g).position !== 'fixed') return;
    const bg = parse(getComputedStyle(g).backgroundColor);
    const onIndigoOnly = g.matches('.glass-dark, .vcard');
    let min = 99, who = '';
    g.querySelectorAll('*').forEach(t => {
      if (!t.childNodes.length || ![...t.childNodes].some(n => n.nodeType === 3 && n.textContent.trim())) return;
      const s = getComputedStyle(t); if (s.visibility === 'hidden') return;
      for (let a = t; a && a !== g.parentElement; a = a.parentElement) { if (+getComputedStyle(a).opacity < .05) return; }
      if (t.closest('.counter-roll')) { const r = t.getBoundingClientRect(), c = t.closest('.counter').getBoundingClientRect(); if (r.top < c.top - 1 || r.bottom > c.bottom + 1) return; }
      let bgT = bg; for (let a = t; a && a !== g; a = a.parentElement) { const c = parse(getComputedStyle(a).backgroundColor); if (c.a > .5) { bgT = c; break; } }
      const fg = parse(s.color);
      (onIndigoOnly ? backs.slice(0, 1) : backs).forEach(b => { const v = cr(over(fg, over(bgT, b)), over(bgT, b)); if (v < min) { min = v; who = t.className || t.tagName; } });
    });
    if (min < 99) out.push({glass: g.className.split(' ')[0], min: +min.toFixed(2), who});
  });
  return out;
}
"""


def run_axe(pg):
    pg.add_script_tag(content=AXE)
    res = pg.evaluate("""async () => { const r = await axe.run(document, {runOnly: {type: 'tag', values: ['wcag2a','wcag2aa','wcag21a','wcag21aa','best-practice']}, resultTypes: ['violations']});
      return r.violations.map(v => ({id: v.id, impact: v.impact, n: v.nodes.length, t: v.nodes.slice(0,2).map(n => n.target.join(' '))})); }""")
    return res


def page_errors(pg, bucket):
    pg.on("pageerror", lambda e: bucket.append("pageerror: " + str(e)[:200]))
    pg.on("console", lambda m: bucket.append("console: " + m.text[:200]) if m.type == "error" else None)


def static_checks(b):
    """Every page × every viewport: overflow, targets, underline, siblings, errors."""
    vps = [(w, h, True) for w, h in PHONES + LAND + TABLET] + [(w, h, False) for w, h in DESK]
    for w, h, touch in vps:
        ctx = b.new_context(viewport={"width": w, "height": h}, is_mobile=touch, has_touch=touch)
        ctx.add_init_script(INIT)
        for p in ALL:
            errs = []
            pg = ctx.new_page()
            page_errors(pg, errs)
            pg.goto(url(p), wait_until="networkidle")
            pg.wait_for_timeout(300)
            scroll_through(pg, step=600 if not QUICK else 500, pause=40)
            pg.evaluate("window.scrollTo(0,0)")
            pg.wait_for_timeout(250)
            ov = pg.evaluate(OVERFLOW_JS)
            tg = pg.evaluate(TARGETS_JS)
            ul = pg.evaluate(UNDERLINE_JS)
            sib = pg.evaluate(SIBLINGS_JS)
            shifts = pg.evaluate("window.__shifts")
            key = f"{p}@{w}x{h}"
            report["pages"][key] = {"hscroll": ov["sw"] > ov["vw"] or ov["bw"] > ov["vw"], "overflow": ov["out"], "targets": tg[:6],
                                    "underline": ul[:4], "siblings": sib, "errors": errs[:5],
                                    "cls_load_scroll": round(sum(s["v"] for s in shifts), 4), "shift_src": [s["src"] for s in shifts][:4]}
            pg.close()
        ctx.close()


def hover_focus_underline(b):
    ctx = b.new_context(viewport={"width": 1440, "height": 900})
    bad, hover_stick = [], []
    for p in ["index.html", "career.html", "contact.html", "en/approach.html"]:
        pg = ctx.new_page()
        pg.goto(url(p), wait_until="networkidle")
        scroll_through(pg, 700, 30)
        n = pg.evaluate("document.querySelectorAll('a[href], button').length")
        for i in range(n):
            loc = pg.locator("a[href], button").nth(i)
            try:
                if not loc.is_visible():
                    continue
                loc.hover(timeout=600)
                d1 = loc.evaluate("e => getComputedStyle(e).textDecorationLine")
                loc.focus()
                d2 = loc.evaluate("e => getComputedStyle(e).textDecorationLine")
                if d1 != "none" or d2 != "none":
                    bad.append(f"{p} #{i} {d1}/{d2}")
            except Exception:
                pass
        pg.close()
    ctx.close()
    report["summary"]["underline_hover_focus"] = bad[:10] or "none"


def a11y(b):
    out = {}
    for (w, h, touch) in [(390, 844, True), (1440, 900, False)]:
        ctx = b.new_context(viewport={"width": w, "height": h}, is_mobile=touch, has_touch=touch)
        for p in ALL:
            pg = ctx.new_page()
            pg.goto(url(p), wait_until="networkidle")
            scroll_through(pg, 500, 50)
            pg.wait_for_timeout(1200)
            pg.evaluate("window.scrollTo(0,0)")
            pg.wait_for_timeout(600)
            v = run_axe(pg)
            extra = pg.evaluate(A11Y_JS)
            typo = pg.evaluate(TYPO_JS)
            glass = pg.evaluate(GLASS_JS)
            out[f"{p}@{w}"] = {"axe": v, "extra": extra, "typo": typo, "glass": glass}
            pg.close()
        ctx.close()
    report["a11y"] = out


def interactions(b):
    """Touch context: nav, menu, language, tabs, gantt, seg, deck, swipe, copy, details; nothing jumps."""
    res = {}
    ctx = b.new_context(viewport={"width": 390, "height": 844}, is_mobile=True, has_touch=True)
    ctx.add_init_script(INIT)
    ctx.grant_permissions(["clipboard-read", "clipboard-write"])
    pg = ctx.new_page()
    errs = []
    page_errors(pg, errs)

    # menu: open, every link navigates, close with the same button, Esc
    nav_ok = []
    for i, p in enumerate(PAGES):
        pg.goto(url("index.html"), wait_until="networkidle")
        pg.tap("#capDot")
        pg.wait_for_timeout(700)
        opened = pg.evaluate("document.querySelector('#menu').classList.contains('open') && document.documentElement.classList.contains('lock')")
        pg.locator(".menu-a").nth(i).tap()
        pg.wait_for_timeout(700)
        nav_ok.append((p, opened, pg.url.split("/")[-1].split("?")[0] or "index.html"))
    res["menu_nav"] = nav_ok
    pg.goto(url("career.html"), wait_until="networkidle")
    pg.tap("#capDot"); pg.wait_for_timeout(600)
    pg.tap("#capDot"); pg.wait_for_timeout(700)
    res["menu_close_button"] = pg.evaluate("document.querySelector('#menu').hidden && !document.documentElement.classList.contains('lock')")
    pg.tap("#capDot"); pg.wait_for_timeout(600)
    pg.keyboard.press("Escape"); pg.wait_for_timeout(700)
    res["menu_close_esc"] = pg.evaluate("document.querySelector('#menu').hidden")

    # language: toggle, remembered, returns to the same section
    pg.goto(url("career.html"), wait_until="networkidle")
    pg.evaluate("document.getElementById('align').scrollIntoView({behavior:'instant'})")
    pg.wait_for_timeout(500)
    pg.tap(".pill .lang")
    pg.wait_for_load_state("networkidle"); pg.wait_for_timeout(600)
    res["lang_switch_url"] = pg.url.replace(BASE, "")
    res["lang_switch_section"] = pg.evaluate("(() => { const r = document.getElementById('align').getBoundingClientRect(); return Math.round(r.top) })()")
    pg.goto(BASE + "approach.html", wait_until="networkidle")  # no ?stay: remembered English should redirect
    pg.wait_for_timeout(400)
    res["lang_remembered"] = pg.url.replace(BASE, "")
    pg.tap(".pill .lang"); pg.wait_for_load_state("networkidle"); pg.wait_for_timeout(300)
    res["lang_back"] = pg.url.replace(BASE, "")

    # nothing jumps: operate every switching block on the home page and record positions + layout shifts
    pg.goto(url("index.html"), wait_until="networkidle")
    scroll_through(pg, 500, 40)
    pg.evaluate("window.scrollTo({top: 0, behavior: 'instant'})"); pg.wait_for_timeout(200)
    pg.evaluate("window.scrollTo({top: document.querySelector('#job .tabs').getBoundingClientRect().top + scrollY - 200, behavior: 'instant'})")
    pg.wait_for_timeout(800)
    pg.evaluate("window.__shifts = []")
    POS = "(() => [Math.round(scrollY), document.documentElement.scrollHeight, Math.round(document.querySelector('.panels').offsetHeight), Math.round(document.querySelector('#path').getBoundingClientRect().top)])()"
    before = pg.evaluate(POS)
    tabs = pg.locator("[role=tab]")
    for i in [1, 2, 3, 0, 3, 2, 1, 1, 3]:
        tabs.nth(i).tap(); pg.wait_for_timeout(60)
    pg.wait_for_timeout(700)
    after = pg.evaluate(POS)
    res["tabs_fast_final"] = pg.evaluate("(() => { const t = [...document.querySelectorAll('.tabs [role=tab]')]; const i = t.findIndex(x => x.getAttribute('aria-selected') === 'true'); const p = [...document.querySelectorAll('.tabs .panel')].findIndex(x => x.classList.contains('is-on')); return [i, p, document.querySelectorAll('.tabs .panel.is-on').length] })()")
    res["tabs_positions"] = [before, after]
    res["tabs_shift"] = round(sum(s["v"] for s in pg.evaluate("window.__shifts")), 4)

    # career: gantt rows, chips, auto cycle
    pg.goto(url("career.html"), wait_until="networkidle")
    pg.evaluate("document.querySelector('.gantt').scrollIntoView({block:'center', behavior:'instant'})")
    pg.wait_for_timeout(300)
    pg.evaluate("window.__shifts = []")
    pos0 = pg.evaluate("Math.round(document.querySelector('#hrsd').getBoundingClientRect().top + scrollY)")
    c0 = pg.evaluate("document.querySelector('.g-cap.is-on').dataset.g")
    pg.wait_for_timeout(7200)
    c1 = pg.evaluate("document.querySelector('.g-cap.is-on').dataset.g")
    res["gantt_auto_cycles"] = c0 != c1
    rows = pg.locator("button.g-row")
    for i in range(rows.count()):
        rows.nth(i).tap(); pg.wait_for_timeout(120)
    chips = pg.locator(".g-chip")
    for i in range(chips.count()):
        chips.nth(i).tap(); pg.wait_for_timeout(120)
    pg.wait_for_timeout(600)
    res["gantt_final"] = pg.evaluate("[document.querySelectorAll('.g-cap.is-on').length, document.querySelector('.g-cap.is-on').dataset.g, document.querySelector('.g-chip[aria-pressed=true]').dataset.g]")
    pos1 = pg.evaluate("Math.round(document.querySelector('#hrsd').getBoundingClientRect().top + scrollY)")
    res["gantt_positions"] = [pos0, pos1]
    res["gantt_shift"] = round(sum(s["v"] for s in pg.evaluate("window.__shifts")), 4)

    # career: details on demand (allowed to grow) and the button stays put
    pg.evaluate("document.querySelector('#align .more-btn').scrollIntoView({block:'center', behavior:'instant'})")
    pg.wait_for_timeout(500)
    y0 = pg.evaluate("Math.round(document.querySelector('#align .more-btn').getBoundingClientRect().top)")
    pg.tap("#align .more-btn"); pg.wait_for_timeout(800)
    y1 = pg.evaluate("Math.round(document.querySelector('#align .more-btn').getBoundingClientRect().top)")
    res["details_button_stays"] = [y0, y1, pg.evaluate("document.querySelector('#more-align').classList.contains('open')")]

    # approach: segmented switch + deck (buttons, auto, swipe)
    pg.goto(url("approach.html"), wait_until="networkidle")
    pg.evaluate("document.querySelector('.seg').scrollIntoView({block:'center', behavior:'instant'})")
    pg.wait_for_timeout(700)
    pg.evaluate("window.__shifts = []")
    p0 = pg.evaluate("Math.round(document.querySelector('#values').getBoundingClientRect().top + scrollY)")
    for i in [1, 0, 1, 1, 0, 1]:
        pg.locator(".seg-b").nth(i).tap(); pg.wait_for_timeout(50)
    pg.wait_for_timeout(900)
    res["seg_final"] = pg.evaluate("[document.querySelector('.seg').dataset.state, document.querySelector('.seg-p.is-on').id]")
    p1 = pg.evaluate("Math.round(document.querySelector('#values').getBoundingClientRect().top + scrollY)")
    res["seg_positions"] = [p0, p1]
    pg.evaluate("document.querySelector('.deck').scrollIntoView({block:'center', behavior:'instant'})")
    pg.wait_for_timeout(600)
    top0 = pg.evaluate("document.querySelector('.vcard[data-pos=\"0\"] .vcard-n').textContent")
    pg.wait_for_timeout(15500)  # auto turn waits 9 s after any touch, then every 5.2 s
    top1 = pg.evaluate("document.querySelector('.vcard[data-pos=\"0\"] .vcard-n').textContent")
    res["deck_auto"] = top0 != top1
    for _ in range(5):
        pg.locator("[data-deck-next]").tap(); pg.wait_for_timeout(40)
    pg.wait_for_timeout(900)
    res["deck_fast_state"] = pg.evaluate("[document.querySelectorAll('.vcard[data-pos=\"0\"]').length, document.querySelectorAll('.vcard[aria-hidden=false]').length, document.querySelectorAll('.vcard.is-out, .vcard.is-in').length]")
    # swipe with touch-like pointer events
    t_before = pg.evaluate("document.querySelector('.vcard[data-pos=\"0\"] .vcard-n').textContent")
    box = pg.locator(".deck-stage").bounding_box()
    cx, cy = box["x"] + box["width"] / 2, box["y"] + box["height"] / 3
    pg.evaluate(f"""(() => {{ const s = document.querySelector('.deck-stage');
      const ev = (t, x) => s.dispatchEvent(new PointerEvent(t, {{bubbles: true, clientX: x, clientY: {cy}, pointerId: 7, pointerType: 'touch', isPrimary: true}}));
      ev('pointerdown', {cx}); for (let i = 1; i <= 8; i++) ev('pointermove', {cx} + i * 18); ev('pointerup', {cx} + 144); }})()""")
    pg.wait_for_timeout(900)
    res["deck_swipe_changes"] = t_before != pg.evaluate("document.querySelector('.vcard[data-pos=\"0\"] .vcard-n').textContent")
    p2 = pg.evaluate("Math.round(document.querySelector('#night').getBoundingClientRect().top + scrollY)")
    res["deck_positions_night"] = p2
    res["approach_shift"] = round(sum(s["v"] for s in pg.evaluate("window.__shifts")), 4)

    # credentials: swipe row on phones
    pg.goto(url("credentials.html"), wait_until="networkidle")
    pg.evaluate("document.querySelector('.vcs').scrollIntoView({block:'center', behavior:'instant'})")
    pg.wait_for_timeout(600)
    pg.evaluate("document.querySelector('.vcs').scrollBy({left: -400 * (document.dir === 'rtl' ? 1 : -1)})")
    pg.wait_for_timeout(700)
    res["swipe_row"] = pg.evaluate("[document.querySelector('.vcs').classList.contains('has-c'), [...document.querySelectorAll('.vcs .vc')].findIndex(e => e.classList.contains('is-c')), [...document.querySelectorAll('.sdots i')].findIndex(e => e.classList.contains('is-on'))]")

    # contact: copy email, FAQ open
    pg.goto(url("contact.html"), wait_until="networkidle")
    pg.wait_for_timeout(500)
    pg.evaluate("window.__shifts = []")
    pg.tap(".copy")
    pg.wait_for_timeout(300)
    res["copy"] = [pg.evaluate("document.querySelector('.copy').classList.contains('is-done')"),
                   pg.evaluate("navigator.clipboard.readText().catch(() => 'n/a')")]
    res["copy_shift"] = round(sum(s["v"] for s in pg.evaluate("window.__shifts")), 4)
    pg.locator(".faq-q").first.tap(); pg.wait_for_timeout(700)
    res["faq_open"] = pg.evaluate("document.querySelector('.faq-q').getAttribute('aria-expanded') === 'true' && document.getElementById('faq-0').classList.contains('open')")

    # hover never sticks on touch
    pg.goto(url("index.html"), wait_until="networkidle")
    pg.wait_for_timeout(400)
    res["cap_at_top"] = pg.evaluate("document.getElementById('cap').classList.contains('has-act')")
    res["hover_media_on_touch"] = pg.evaluate("matchMedia('(hover: hover)').matches")
    pg.evaluate("document.querySelector('.ctile').scrollIntoView({block:'center', behavior:'instant'})")
    pg.wait_for_timeout(1500)
    pg.locator(".ctile").first.tap(); pg.wait_for_timeout(500)
    res["tile_after_tap_transform"] = pg.evaluate("getComputedStyle(document.querySelector('.ctile')).transform")

    # capsule action: appears after the hero buttons, hides near the footer
    pg.evaluate("window.scrollTo(0, innerHeight * 1.6)"); pg.wait_for_timeout(600)
    res["cap_after_hero"] = pg.evaluate("document.getElementById('cap').classList.contains('has-act')")
    pg.evaluate("window.scrollTo(0, document.documentElement.scrollHeight)"); pg.wait_for_timeout(700)
    res["cap_at_footer"] = pg.evaluate("document.getElementById('cap').classList.contains('has-act')")
    res["errors"] = errs[:8]
    ctx.close()
    report["interactions"] = res


def motion(b):
    """Screens at load, +1 s, +3 s and three scroll positions; reduced motion keeps everything visible."""
    from PIL import Image, ImageChops
    out = {}
    for (w, h, touch) in [(390, 844, True), (1440, 900, False)]:
        for lang in ["", "en/"]:
            ctx = b.new_context(viewport={"width": w, "height": h}, is_mobile=touch, has_touch=touch)
            pg = ctx.new_page()
            pg.goto(url(lang + "index.html"), wait_until="commit")
            pg.wait_for_timeout(120)
            names = []
            for t in [0, 1000, 3000]:
                if t:
                    pg.wait_for_timeout(t - (1000 if t == 3000 else 0))
                f = f"{SHOTS}/motion-{w}{lang.strip('/') or 'ar'}-t{t}.png"
                pg.screenshot(path=f); names.append(f)
            for k, y in enumerate([0.9, 2.2, 3.6]):
                pg.evaluate(f"window.scrollTo(0, innerHeight * {y})"); pg.wait_for_timeout(900)
                f = f"{SHOTS}/motion-{w}{lang.strip('/') or 'ar'}-s{k}.png"
                pg.screenshot(path=f); names.append(f)
            diffs = []
            for a, c in zip(names[:2], names[1:3]):
                d = ImageChops.difference(Image.open(a).convert("RGB"), Image.open(c).convert("RGB")).getbbox()
                diffs.append(bool(d))
            # at rest: two frames 1.5 s apart at the hero still differ (ripples, dots, shine)
            pg.evaluate("window.scrollTo(0,0)"); pg.wait_for_timeout(1500)
            pg.screenshot(path="/tmp/r1.png"); pg.wait_for_timeout(1500); pg.screenshot(path="/tmp/r2.png")
            rest = bool(ImageChops.difference(Image.open("/tmp/r1.png").convert("RGB"), Image.open("/tmp/r2.png").convert("RGB")).getbbox())
            out[f"{w}{lang or 'ar'}"] = {"entrance_changes": diffs, "alive_at_rest": rest}
            ctx.close()
    # reduced motion
    rm = {}
    for (w, h, touch) in [(390, 844, True), (1440, 900, False)]:
        ctx = b.new_context(viewport={"width": w, "height": h}, is_mobile=touch, has_touch=touch, reduced_motion="reduce")
        for p in ["index.html", "approach.html", "en/career.html"]:
            pg = ctx.new_page()
            pg.goto(url(p), wait_until="networkidle")
            scroll_through(pg, 500, 80)
            pg.wait_for_timeout(600)
            hidden = pg.evaluate("[...document.querySelectorAll('[data-rv], .stop')].filter(e => { const s = getComputedStyle(e); const b = e.classList.contains('stop') ? getComputedStyle(e, '::before') : s; return +b.opacity < .99 && e.offsetParent; }).length")
            rm[f"{p}@{w}"] = hidden
            pg.close()
        pg = ctx.new_page(); pg.goto(url("index.html"), wait_until="networkidle"); pg.wait_for_timeout(800)
        pg.screenshot(path=f"{SHOTS}/reduced-{w}.png"); pg.close()
        ctx.close()
    out["reduced_motion_hidden_elements"] = rm
    report["motion"] = out


def glass_fallback(b):
    ctx = b.new_context(viewport={"width": 390, "height": 844}, is_mobile=True, has_touch=True)
    pg = ctx.new_page()
    pg.goto(BASE + "index.html?stay&noglass", wait_until="networkidle")
    scroll_through(pg, 500, 40)
    pg.evaluate("window.scrollTo(0,0)"); pg.wait_for_timeout(1500)
    pg.screenshot(path=f"{SHOTS}/noglass-390.png")
    report["glass_fallback"] = pg.evaluate(GLASS_JS)
    ctx.close()


def smoothness(b):
    out = {}
    for p in ["index.html", "career.html", "consulting.html"]:
        ctx = b.new_context(viewport={"width": 390, "height": 844}, is_mobile=True, has_touch=True)
        pg = ctx.new_page()
        pg.goto(url(p), wait_until="networkidle")
        cdp = ctx.new_cdp_session(pg)
        cdp.send("Emulation.setCPUThrottlingRate", {"rate": 4})
        pg.wait_for_timeout(500)
        pg.evaluate("""() => { window.__ft = []; let last = performance.now(); const f = now => { window.__ft.push(now - last); last = now; if (!window.__stopf) requestAnimationFrame(f); }; requestAnimationFrame(f); }""")
        h = pg.evaluate("document.documentElement.scrollHeight")
        y = 0
        t0 = time.time()
        while y < h:
            pg.mouse.wheel(0, 120)
            y += 120
            pg.wait_for_timeout(16)
        pg.wait_for_timeout(400)
        ft = pg.evaluate("window.__stopf = true, window.__ft")
        ft = ft[2:]
        if ft:
            ft_sorted = sorted(ft)
            out[p] = {"frames": len(ft), "avg_fps": round(1000 / (sum(ft) / len(ft)), 1),
                      "p95_ms": round(ft_sorted[int(len(ft) * .95) - 1], 1), "long_frames_pct": round(100 * sum(1 for x in ft if x > 50) / len(ft), 1),
                      "seconds": round(time.time() - t0, 1)}
        ctx.close()
    report["smoothness_4x_cpu_390"] = out


def main():
    t = time.time()
    with sync_playwright() as p:
        b = p.chromium.launch()
        static_checks(b); print("static checks done", round(time.time() - t), flush=True)
        hover_focus_underline(b); print("hover/focus done", round(time.time() - t))
        a11y(b); print("a11y done", round(time.time() - t))
        interactions(b); print("interactions done", round(time.time() - t))
        motion(b); print("motion done", round(time.time() - t))
        glass_fallback(b)
        smoothness(b); print("smoothness done", round(time.time() - t))
        b.close()
    P = report["pages"]
    s = report["summary"]
    s["page_viewports_checked"] = len(P)
    s["hscroll"] = [k for k, v in P.items() if v["hscroll"] or v["overflow"]]
    s["small_targets"] = {k: v["targets"] for k, v in P.items() if v["targets"]}
    s["underline_rest"] = [k for k, v in P.items() if v["underline"]]
    s["siblings"] = {k: v["siblings"] for k, v in P.items() if v["siblings"]}
    s["js_errors"] = {k: v["errors"] for k, v in P.items() if v["errors"]}
    s["cls_total_load_scroll"] = round(sum(v["cls_load_scroll"] for v in P.values()), 4)
    s["cls_pages"] = {k: (v["cls_load_scroll"], v["shift_src"]) for k, v in P.items() if v["cls_load_scroll"] > 0}
    ax = report.get("a11y", {})
    s["axe_serious_critical"] = {k: [x for x in v["axe"] if x["impact"] in ("serious", "critical")] for k, v in ax.items() if any(x["impact"] in ("serious", "critical") for x in v["axe"])}
    s["axe_all_ids"] = sorted({x["id"] + ":" + str(x["impact"]) for v in ax.values() for x in v["axe"]})
    s["a11y_extra"] = {k: v["extra"] for k, v in ax.items() if v["extra"]}
    s["typo_lh"] = {k: v["typo"]["lh"] for k, v in ax.items() if v["typo"]["lh"]}
    s["typo_ls"] = {k: v["typo"]["ls"] for k, v in ax.items() if v["typo"]["ls"]}
    s["fonts_loaded"] = {k: v["typo"]["fonts"] for k, v in ax.items() if not all(v["typo"]["fonts"].values())} or "all"
    meas = [m for k, v in ax.items() if k.endswith("@1440") for m in v["typo"]["measure"]]
    s["desktop_chars_per_line"] = [min(meas), max(meas), round(sum(meas) / len(meas))] if meas else None
    s["glass_min_contrast"] = sorted({(g["glass"], g["min"]) for v in ax.values() for g in v["glass"]}, key=lambda x: x[1])[:6]
    with open(os.path.join(ROOT, "tests", "report.json"), "w", encoding="utf-8") as f:
        json.dump(report, f, ensure_ascii=False, indent=1)
    print(json.dumps(s, ensure_ascii=False, indent=1)[:9000])
    print(json.dumps(report.get("interactions"), ensure_ascii=False)[:3000])
    print(json.dumps(report.get("motion"), ensure_ascii=False)[:1500])
    print(json.dumps(report.get("glass_fallback"), ensure_ascii=False)[:600])
    print(json.dumps(report.get("smoothness_4x_cpu_390"), ensure_ascii=False))
    print("took", round(time.time() - t), "s")


if __name__ == "__main__":
    main()
