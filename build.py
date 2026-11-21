#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Builds Saleh Al Dakheel's site into docs/ from content.py.

    python3 build.py

Writes the Arabic pages (default, RTL) at the root of docs/, the English pages in
docs/en/, plus 404.html, robots.txt, sitemap.xml, llms.txt, llms-full.txt.
Every internal link and asset path is relative, so the site works under any
sub-path (GitHub Pages: /saleh-al-dakheel/). BASE_URL is only used for absolute
URLs that must be absolute: canonical, hreflang, og tags, JSON-LD, sitemap.
"""
import datetime
import hashlib
import html
import json
import os
import re
import shutil

from content import (CONFIG, PERSON, NAV, UI, HOME, GANTT, CAREER, CONSULTING, APPROACH,
                     CREDENTIALS, CONTACT, NOT_FOUND, KNOWS_ABOUT, OCCUPATIONS)

ROOT = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(ROOT, "src")
OUT = os.path.join(ROOT, "docs")
BASE = CONFIG["BASE_URL"].rstrip("/") + "/" if CONFIG["BASE_URL"] else ""
TODAY = datetime.date.today()
ICONS = json.load(open(os.path.join(SRC, "icons.json"), encoding="utf-8"))
LANGS = ("ar", "en")
PAGES = [slug for slug, _ in NAV]
FILE = {slug: ("index.html" if slug == "index" else slug + ".html") for slug in PAGES}

# ------------------------------------------------------------------ helpers
esc = html.escape


def icon(name, cls="ic"):
    if name == "arrow":
        cls += " ic-arrow"
    return (f'<svg class="{cls}" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.75" '
            f'stroke-linecap="round" stroke-linejoin="round" aria-hidden="true" focusable="false">{ICONS[name]}</svg>')


STOP = '<span class="stop"><span class="vh">.</span></span>'

# Latin and digit runs inside Arabic text get dir="ltr" so ranges like 2018–2024 never flip.
LTR_RUN = re.compile(r"(?:Co\.|[A-Za-z0-9@®₀-₉])(?:[A-Za-z0-9@&.,'’+%/:\-–_()®™₀-₉ ]*(?:Co\.|[A-Za-z0-9®™+%)₀-₉]))?")


def _ltr(m, O, C):
    s, tail = m.group(0), ""
    while s.count(")") > s.count("(") and s.endswith(")"):
        s, tail = s[:-1], ")" + tail
    while s.count("(") > s.count(")") and "(" in s:
        i = s.rindex("(")
        s, tail = s[:i].rstrip(), s[i:] + tail  # unbalanced "(": leave it outside
    return (O + s + C + tail) if s else tail


COUNT = re.compile(r"\[\[(\d+)(\+?)\]\]")


def count_html(m):
    n, plus = m.group(1), m.group(2)
    return (f'<span class="num" dir="ltr"><span class="count" data-to="{n}">{n}</span>'
            f'{plus}</span>')


def rich(text, lang):
    """Escape, wrap Latin runs (Arabic only), turn [[n]] into count-up numbers."""
    slots = []
    O, C, S, E = "\ue010", "\ue011", "\ue000", "\ue001"

    def hold(m):
        slots.append(count_html(m))
        return S + chr(0xE100 + len(slots) - 1) + E

    t = COUNT.sub(hold, text)
    if lang == "ar":
        t = LTR_RUN.sub(lambda m: _ltr(m, O, C), t)
    t = esc(t, quote=False)
    t = t.replace(O, '<span dir="ltr">').replace(C, "</span>")
    t = re.sub(S + "(.)" + E, lambda m: slots[ord(m.group(1)) - 0xE100], t)
    return t


def plain(text):
    """Text without the [[ ]] markup (for meta, JSON-LD, llms)."""
    return COUNT.sub(lambda m: m.group(1) + m.group(2), text)


def head_text(text, lang):
    """A title: rich text whose final full stop becomes the landing dot.
    A word joiner keeps the dot on the same line as the last word."""
    if not text.endswith("."):
        return rich(text, lang)
    return rich(text[:-1], lang) + "\u2060" + STOP


def L(d, lang):
    return d[lang] if isinstance(d, dict) else d


def ym(s):
    if s == "now":
        return TODAY.year + (TODAY.month - 1) / 12
    y, m = s.split("-")
    return int(y) + (int(m) - 1) / 12


def pct(s, a, b):
    v = (ym(s) - ym(a)) / (ym(b) - ym(a)) * 100
    return max(0.0, min(100.0, v))


def num3(i):
    return f"{i:03d}"


def asset_v(path):
    with open(path, "rb") as f:
        return hashlib.sha1(f.read()).hexdigest()[:8]


def rel(lang):
    """Prefix from a page in this language to the site root."""
    return "" if lang == "ar" else "../"


def page_href(slug, lang, from_lang):
    """Relative link to a page in `lang`, from a page in `from_lang`."""
    target = FILE[slug]
    if lang == from_lang:
        return "./" if slug == "index" else target
    if from_lang == "ar":  # ar -> en
        return "en/" if slug == "index" else "en/" + target
    return "../" if slug == "index" else "../" + target  # en -> ar


def abs_url(slug, lang):
    p = "" if slug == "index" else FILE[slug]
    return BASE + ("en/" if lang == "en" else "") + p


# ------------------------------------------------------------------ JSON-LD
def person_ld(lang):
    c = CONFIG
    img = (BASE + c["PHOTO"]) if c["PHOTO"] else (BASE + "assets/img/og.png")
    creds = []
    for v in CREDENTIALS["valid"]:
        creds.append({"@type": "EducationalOccupationalCredential", "name": v["name"]["en"],
                      "alternateName": v["name"]["ar"], "credentialCategory": "certification",
                      "recognizedBy": {"@type": "Organization", "name": v["by"]["en"], "alternateName": v["by"]["ar"]},
                      "dateCreated": v["s"], "expires": v["e"]})
    for p in CREDENTIALS["progs"]:
        creds.append({"@type": "EducationalOccupationalCredential", "name": p["name"], "credentialCategory": "certificate",
                      "recognizedBy": {"@type": "Organization", "name": p["by"]["en"], "alternateName": p["by"]["ar"]}})
    creds.append({"@type": "EducationalOccupationalCredential", "name": "BSc Chemical Engineering",
                  "alternateName": "بكالوريوس الهندسة الكيميائية", "credentialCategory": "degree",
                  "recognizedBy": {"@type": "CollegeOrUniversity", "name": "King Fahd University of Petroleum & Minerals"}})
    d = {
        "@type": "Person", "@id": BASE + "#person",
        "name": PERSON["name"][lang], "alternateName": PERSON["alternate_names"],
        "givenName": "Saleh", "familyName": "Al Dakheel",
        "jobTitle": ["Projects Manager - EPMO", "مدير مشاريع - مكتب إدارة المشاريع المؤسسي"],
        "description": plain(HOME["desc"][lang]),
        "url": BASE, "image": img,
        "address": {"@type": "PostalAddress", "addressLocality": "Riyadh", "addressCountry": "SA"},
        "homeLocation": {"@type": "Place", "name": "Riyadh, Saudi Arabia", "alternateName": "الرياض"},
        "worksFor": {"@type": "GovernmentOrganization", "name": "Ministry of Human Resources and Social Development",
                     "alternateName": ["HRSD", "وزارة الموارد البشرية والتنمية الاجتماعية", "Ministry of Human Resources and Social Development - KSA"],
                     "address": {"@type": "PostalAddress", "addressLocality": "Riyadh", "addressCountry": "SA"}},
        "alumniOf": [{"@type": "CollegeOrUniversity", "name": "King Fahd University of Petroleum & Minerals",
                      "alternateName": ["KFUPM", "جامعة الملك فهد للبترول والمعادن"]}],
        "hasOccupation": [{"@type": "Occupation", "name": n, "alternateName": alts,
                           "occupationLocation": {"@type": "City", "name": "Riyadh"}} for n, alts in OCCUPATIONS],
        "knowsAbout": KNOWS_ABOUT,
        "knowsLanguage": [{"@type": "Language", "name": "Arabic", "alternateName": "ar"},
                          {"@type": "Language", "name": "English", "alternateName": "en"}],
        "hasCredential": creds,
        "sameAs": [c["LINKEDIN"]] if c["LINKEDIN"] else [],
    }
    if c["EMAIL"]:
        d["email"] = "mailto:" + c["EMAIL"]
    if c["PHONE"]:
        d["telephone"] = c["PHONE"]
    return d


def page_ld(slug, lang, title, desc):
    url = abs_url(slug, lang)
    graph = [
        {"@type": "WebSite", "@id": BASE + "#website", "url": BASE, "name": "Saleh Al Dakheel",
         "alternateName": "صالح الدخيل", "inLanguage": ["ar", "en"], "publisher": {"@id": BASE + "#person"}},
        person_ld(lang),
        {"@type": "ProfilePage" if slug == "index" else "WebPage", "@id": url + "#page", "url": url,
         "name": title, "description": desc, "inLanguage": lang, "isPartOf": {"@id": BASE + "#website"},
         ("mainEntity" if slug == "index" else "about"): {"@id": BASE + "#person"}},
    ]
    if slug != "index":
        graph.append({"@type": "BreadcrumbList", "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": L(NAV[0][1], lang), "item": abs_url("index", lang)},
            {"@type": "ListItem", "position": 2, "name": L(dict(NAV)[slug], lang), "item": url}]})
    if slug == "contact":
        graph.append({"@type": "FAQPage", "@id": url + "#faq", "mainEntity": [
            {"@type": "Question", "name": f["q"][lang], "acceptedAnswer": {"@type": "Answer", "text": f["a"][lang]}}
            for f in CONTACT["faq"]]})
    return json.dumps({"@context": "https://schema.org", "@graph": graph}, ensure_ascii=False, separators=(",", ":"))


# ------------------------------------------------------------------ page chrome
def head(slug, lang, title, desc, versions):
    r = rel(lang)
    other = "en" if lang == "ar" else "ar"
    alt_rel = page_href(slug, other, lang)
    robots = '<meta name="robots" content="noindex">\n' if CONFIG["PREVIEW"] else ""
    links = ""
    if BASE:
        links = (f'<link rel="canonical" href="{abs_url(slug, lang)}">\n'
                 f'<link rel="alternate" hreflang="ar" href="{abs_url(slug, "ar")}">\n'
                 f'<link rel="alternate" hreflang="en" href="{abs_url(slug, "en")}">\n'
                 f'<link rel="alternate" hreflang="x-default" href="{abs_url(slug, "ar")}">\n'
                 f'<meta property="og:url" content="{abs_url(slug, lang)}">\n'
                 f'<meta property="og:image" content="{BASE}assets/img/og.png">\n'
                 f'<meta name="twitter:image" content="{BASE}assets/img/og.png">\n')
    fonts = (["kufam-ar-700", "alexandria-ar-400", "alexandria-ar-600"] if lang == "ar" else []) + ["outfit-la-400", "outfit-la-600", "outfit-la-700"]
    pre = "".join(f'<link rel="preload" href="{r}assets/fonts/{f}.woff2" as="font" type="font/woff2" crossorigin>\n' for f in fonts)
    return f"""<!doctype html>
<html lang="{lang}" dir="{'rtl' if lang == 'ar' else 'ltr'}" data-page="{slug}" data-alt="{alt_rel}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{esc(title)}</title>
<meta name="description" content="{esc(desc)}">
{robots}<meta name="author" content="{esc(PERSON['name'][lang])}">
<meta name="theme-color" content="#3D3B8E">
<meta name="color-scheme" content="light">
<meta property="og:type" content="profile">
<meta property="og:site_name" content="{esc(PERSON['name'][lang])}">
<meta property="og:title" content="{esc(title)}">
<meta property="og:description" content="{esc(desc)}">
<meta property="og:locale" content="{'ar_SA' if lang == 'ar' else 'en_US'}">
<meta property="og:locale:alternate" content="{'en_US' if lang == 'ar' else 'ar_SA'}">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:image:alt" content="{esc(PERSON['name'][lang])}">
<meta property="profile:first_name" content="Saleh">
<meta property="profile:last_name" content="Al Dakheel">
<meta name="twitter:card" content="summary_large_image">
{links}<link rel="icon" href="{r}assets/img/icon.svg" type="image/svg+xml">
<link rel="icon" href="{r}assets/img/favicon-32.png" sizes="32x32" type="image/png">
<link rel="apple-touch-icon" href="{r}assets/img/apple-touch-icon.png">
{pre}<link rel="stylesheet" href="{r}assets/style.css?v={versions['css']}">
<script>(function(){{var d=document.documentElement;d.classList.add('js');try{{var p=localStorage.getItem('sd-lang');if(p&&p!==d.lang&&!/[?&]stay/.test(location.search)){{location.replace(d.getAttribute('data-alt')+location.hash);}}}}catch(e){{}}}})();</script>
<script type="application/ld+json">{page_ld(slug, lang, title, desc)}</script>
</head>
"""


def mono_html(lang, cls="mono"):
    if CONFIG["PHOTO"]:
        return (f'<span class="{cls} {cls}--photo"><img src="{rel(lang)}{CONFIG["PHOTO"]}" width="96" height="96" '
                f'alt="" decoding="async"></span>')
    return f'<span class="{cls}" aria-hidden="true"><span class="mono-in"><span class="mono-l">{PERSON["mono"][lang]}</span><i class="mono-d"></i></span></span>'


def header(slug, lang, n_sheets):
    other = "en" if lang == "ar" else "ar"
    links = "".join(
        f'<a class="nav-a" href="{page_href(s, lang, lang)}"{" aria-current=\"page\"" if s == slug else ""}>{L(t, lang)}</a>'
        for s, t in NAV)
    roll = "".join(f"<span>{num3(i)}</span>" for i in range(1, n_sheets + 1))
    return f"""<body data-page="{slug}">
<a class="skip" href="#main">{UI['skip'][lang]}</a>
<div class="progress" aria-hidden="true"><span></span></div>
<header class="hdr" id="hdr">
  <div class="pill">
    <a class="brand" href="{page_href('index', lang, lang)}">
      {mono_html(lang)}<span class="brand-n">{PERSON['name'][lang]}</span>
    </a>
    <nav class="nav" aria-label="{UI['nav_main'][lang]}">{links}</nav>
    <span class="counter" aria-hidden="true" title="{UI['sheet'][lang]}"><span class="counter-roll">{roll}</span></span>
    <a class="lang" href="{page_href(slug, other, lang)}" hreflang="{other}" lang="{other}" data-lang="{other}">{icon('lang')}<span class="lang-l">{UI['lang_to'][lang]}</span></a>
  </div>
</header>
"""


def contact_cards(lang, where):
    c = CONFIG
    out = []
    if c["EMAIL"]:
        out.append(f"""<div class="ccard ccard--mail glass-dark" data-rv>
  <span class="ccard-ic">{icon('mail')}</span>
  <span class="ccard-k">{UI['email'][lang]}</span>
  <a class="ccard-v" href="mailto:{c['EMAIL']}" dir="ltr">{c['EMAIL']}</a>
  <span class="ccard-acts">
    <button class="chip copy" type="button" data-copy="{c['EMAIL']}"><span class="copy-a">{icon('copy')}{UI['copy'][lang]}</span><span class="copy-b" aria-hidden="true">{icon('check')}{UI['copied'][lang]}</span></button>
    <a class="chip" href="mailto:{c['EMAIL']}">{icon('mail')}{UI['write'][lang]}</a>
  </span>
  <span class="sr-live" aria-live="polite"></span>
</div>""")
    if c["LINKEDIN"]:
        out.append(f"""<a class="ccard ccard--li glass-dark" href="{c['LINKEDIN']}" target="_blank" rel="noopener" data-rv>
  <span class="ccard-ic">{icon('linkedin')}</span>
  <span class="ccard-k">{UI['linkedin'][lang]}</span>
  <span class="ccard-v" dir="ltr">linkedin.com/in/saleh-al-dakheel</span>
  <span class="ccard-go">{UI['linkedin_open'][lang]}{icon('ext', 'ic ic-sm')}</span>
</a>""")
    if c["PHONE"]:
        out.append(f"""<a class="ccard glass-dark" href="tel:{re.sub(r'[^+0-9]', '', c['PHONE'])}" data-rv>
  <span class="ccard-ic">{icon('mail')}</span><span class="ccard-k">{'الهاتف' if lang == 'ar' else 'Phone'}</span>
  <span class="ccard-v" dir="ltr">{c['PHONE']}</span></a>""")
    if c["WHATSAPP"]:
        out.append(f"""<a class="ccard glass-dark" href="https://wa.me/{c['WHATSAPP']}" target="_blank" rel="noopener" data-rv>
  <span class="ccard-ic">{icon('mail')}</span><span class="ccard-k">WhatsApp</span>
  <span class="ccard-v" dir="ltr">+{c['WHATSAPP']}</span></a>""")
    return "\n".join(out)


def footer(slug, lang):
    links = "".join(
        f'<a class="fnav-a" href="{page_href(s, lang, lang)}"{" aria-current=\"page\"" if s == slug else ""}>{L(t, lang)}</a>'
        for s, t in NAV)
    cards = "" if slug == "contact" else f'<div class="foot-cards">{contact_cards(lang, "foot")}</div>'
    return f"""<footer class="foot sheet--indigo" id="foot" data-sheet>
  <div class="ripples ripples--foot" aria-hidden="true"><i></i><i></i><i></i></div>
  <div class="wrap foot-grid{' foot-grid--slim' if slug == 'contact' else ''}">
    <div class="foot-id" data-rv>
      <p class="foot-name">{PERSON['name'][lang].rsplit(' ', 1)[0]} <span class="nw">{PERSON['name'][lang].rsplit(' ', 1)[1]}{STOP}</span></p>
      <p class="foot-role">{rich(PERSON['role'][lang], lang)}</p>
      <p class="foot-city">{icon('pin', 'ic ic-sm')}<span>{PERSON['city'][lang]}</span></p>
    </div>
    {cards}
    <nav class="fnav" aria-label="{UI['nav_foot'][lang]}">{links}</nav>
  </div>
  <div class="wrap foot-base">
    <p class="maker"><a href="{CONFIG['MAKER']}" target="_blank" rel="noopener" lang="ar" dir="rtl">تصميم وتطوير نور الدين طفي</a><span aria-hidden="true"> · </span><a href="{CONFIG['MAKER']}" target="_blank" rel="noopener" lang="en" dir="ltr">Nour Aldeen Tofi</a></p>
    <p class="copy-r"><span dir="ltr">© {TODAY.year}</span> {UI['rights'][lang]}</p>
  </div>
</footer>
"""


def menu_and_cap(slug, lang):
    other = "en" if lang == "ar" else "ar"
    items = "".join(
        f'<li style="--k:{i}"><a class="menu-a" href="{page_href(s, lang, lang)}"{" aria-current=\"page\"" if s == slug else ""}>'
        f'<span class="menu-no" dir="ltr">{num3(i + 1)}</span><span class="menu-n">{L(t, lang)}{STOP}</span></a></li>'
        for i, (s, t) in enumerate(NAV))
    mail = (f'<a class="cap-act" id="capAct" href="mailto:{CONFIG["EMAIL"]}" tabindex="-1" aria-hidden="true">'
            f'{icon("mail")}<span>{UI["email_me"][lang]}</span></a>') if CONFIG["EMAIL"] and slug != "contact" else ""
    return f"""<div class="menu" id="menu" role="dialog" aria-modal="true" aria-label="{UI['menu'][lang]}" hidden>
  <div class="menu-bg" aria-hidden="true"><div class="ripples"><i></i><i></i><i></i></div></div>
  <div class="menu-in">
    <nav aria-label="{UI['nav_menu'][lang]}"><ol class="menu-list">{items}</ol></nav>
    <div class="menu-foot">
      <a class="chip chip--light" href="{page_href(slug, other, lang)}" hreflang="{other}" lang="{other}" data-lang="{other}">{icon('lang')}{UI['lang_to'][lang]}</a>
      {f'<a class="chip chip--light" href="mailto:{CONFIG["EMAIL"]}">{icon("mail")}{UI["email"][lang]}</a>' if CONFIG['EMAIL'] else ''}
      {f'<a class="chip chip--light" href="{CONFIG["LINKEDIN"]}" target="_blank" rel="noopener">{icon("linkedin")}{UI["linkedin"][lang]}</a>' if CONFIG['LINKEDIN'] else ''}
    </div>
  </div>
</div>
<div class="cap" id="cap">
  <button class="cap-dot" id="capDot" type="button" aria-expanded="false" aria-controls="menu">
    <span class="cap-ic" aria-hidden="true"><span class="cap-dot-i"></span>{icon('x', 'ic cap-x')}</span>
    <span class="lbl"><span class="cap-l1">{UI['menu'][lang]}</span><span class="cap-l2">{UI['close'][lang]}</span></span>
  </button>
  {mail}
</div>
"""


def scripts(lang, versions):
    return f'<script src="{rel(lang)}assets/site.js?v={versions["js"]}" defer></script>\n</body>\n</html>\n'


class Sheets:
    """Numbers the sheets of a page in order (the PDF-style page numbers)."""

    def __init__(self):
        self.n = 0

    def open(self, kind, sid, extra_cls="", stack=True, label=None, attrs=""):
        self.n += 1
        lab = f' aria-labelledby="{label}"' if label else ""
        st = " data-stack" if stack else ""
        shade = '<i class="shade" aria-hidden="true"></i>' if stack else ""
        return (f'<section class="sheet sheet--{kind} {extra_cls}" id="{sid}" data-sheet="{self.n}"{st}{lab}{attrs}>{shade}\n'
                f'<span class="pno" aria-hidden="true" dir="ltr">{num3(self.n)}</span>\n')


def sec_title(text, lang, hid, cls="h2"):
    return f'<h2 class="{cls}" id="{hid}" data-rv="h">{head_text(text, lang)}</h2>'


def next_link(slug, lang):
    i = PAGES.index(slug)
    if i + 1 >= len(PAGES):
        return ""
    nxt = PAGES[i + 1]
    return (f'<a class="next" href="{page_href(nxt, lang, lang)}" data-rv>'
            f'<span class="next-k">{UI["next"][lang]}</span>'
            f'<span class="next-n">{L(dict(NAV)[nxt], lang)}{STOP}</span>'
            f'<span class="next-no" dir="ltr">{num3(i + 2)}</span>{icon("arrow", "ic next-ic")}</a>')


def page_hero(sh, lang, h1, lead, sid="top", extra=""):
    return (sh.open("indigo", sid, "phero", stack=True, label=sid + "-h") +
            '<div class="ripples" aria-hidden="true"><i></i><i></i><i></i><i></i></div>\n'
            f'<div class="wrap phero-in">\n<h1 class="h1 page-title" id="{sid}-h" data-rv="h">{head_text(h1, lang)}</h1>\n'
            f'<p class="lede" data-rv>{rich(lead, lang)}</p>{extra}\n</div>\n</section>\n')


# ------------------------------------------------------------------ pages
def page_index(lang):
    H = HOME
    sh = Sheets()
    out = []
    # 001 hero
    motto = "".join(f'<span class="m" style="--k:{i}">{head_text(m[lang], lang)}</span>' for i, m in enumerate(H["motto"]))
    lead_dots = "".join(f'<i style="--n:{i}"></i>' for i in range(18))
    over_dots = "".join(f'<i style="--n:{i}"></i>' for i in range(82))
    out.append(sh.open("indigo", "top", "hero", label="top-h") + f"""<div class="ripples ripples--hero" aria-hidden="true"><i></i><i></i><i></i><i></i></div>
<div class="wrap hero-grid">
  <div class="hero-copy">
    <h1 class="hero-name page-title" id="top-h"><span class="hero-w">{PERSON['name'][lang].rsplit(' ', 1)[0]} <span class="nw">{PERSON['name'][lang].rsplit(' ', 1)[1]}{STOP}</span></span></h1>
    <p class="motto">{motto}</p>
    <p class="hero-role" data-rv>{rich(H['role'][lang], lang)}</p>
    <div class="hero-cta" id="heroCta" data-rv>
      <a class="btn btn--light shine" href="{page_href('career', lang, lang)}">{H['cta1'][lang]}{icon('arrow', 'ic btn-ic')}</a>
      {f'<a class="btn btn--line" href="mailto:{CONFIG["EMAIL"]}">{icon("mail")}{H["cta2"][lang]}</a>' if CONFIG['EMAIL'] else ''}
    </div>
  </div>
  <figure class="dots glass-dark" data-rv="pop">
    <figcaption class="dots-t">{head_text(H['dots_title'][lang], lang)}</figcaption>
    <div class="dots-g dots-g--lead" aria-hidden="true">{lead_dots}</div>
    <p class="dots-l"><i class="key key--solid" aria-hidden="true"></i><span>{rich(H['dots_lead'][lang], lang)}</span></p>
    <div class="dots-g dots-g--over" aria-hidden="true">{over_dots}</div>
    <p class="dots-l"><i class="key key--ring" aria-hidden="true"></i><span>{rich(H['dots_over'][lang], lang)}</span></p>
  </figure>
</div>
</section>
""")
    # 002 the job, in tabs
    tabs = H["tabs"]
    tl = "".join(
        f'<button class="tab" role="tab" type="button" id="tab-{t["id"]}" aria-controls="panel-{t["id"]}" '
        f'aria-selected="{"true" if i == 0 else "false"}" tabindex="{0 if i == 0 else -1}">{icon(t["icon"])}<span>{t["label"][lang]}</span></button>'
        for i, t in enumerate(tabs))
    panels = "".join(
        f'<div class="panel{" is-on" if i == 0 else ""}" role="tabpanel" id="panel-{t["id"]}" aria-labelledby="tab-{t["id"]}" tabindex="0"{"" if i == 0 else " inert"}>'
        f'<span class="panel-ic">{icon(t["icon"])}</span><p class="panel-t">{rich(t["text"][lang], lang)}</p></div>'
        for i, t in enumerate(tabs))
    out.append(sh.open("paper", "job", label="job-h") + f"""<div class="wrap split">
  <div class="split-a">
    {sec_title(H['job_title'][lang], lang, 'job-h')}
    <p class="lede" data-rv>{rich(H['job_lead'][lang], lang)}</p>
  </div>
  <div class="split-b tabs" data-tabs data-rv>
    <div class="tablist" role="tablist" aria-label="{H['tabs_label'][lang]}">{tl}<span class="tab-dot" aria-hidden="true"></span></div>
    <div class="panels">{panels}</div>
  </div>
</div>
</section>
""")
    # 003 mini schedule
    a, b = "2023-01", "2027-01"
    rows = ""
    for i, r in enumerate(H["path_rows"]):
        s, w = pct(r["s"], a, b), pct(r["e"], a, b) - pct(r["s"], a, b)
        rows += (f'<li class="mini-row" data-rv style="--i:{i}"><div class="mini-head"><b>{rich(r["org"][lang], lang)}</b>'
                 f'<span>{rich(r["role"][lang], lang)}</span></div>'
                 f'<div class="mini-track"><span class="mini-bar{" is-now" if r["e"] == "now" else ""}" style="--s:{s:.2f}%;--w:{w:.2f}%"></span></div>'
                 f'<span class="mini-when">{rich(r["when"][lang], lang)}</span></li>')
    years = "".join(f'<span style="--s:{pct(f"{y}-01", a, b):.2f}%">{y}</span>' for y in range(2023, 2027))
    out.append(sh.open("white", "path", label="path-h") + f"""<div class="wrap">
  {sec_title(H['path_title'][lang], lang, 'path-h')}
  <div class="mini" data-rv>
    <div class="mini-axis" aria-hidden="true">{years}</div>
    <ol class="mini-rows">{rows}</ol>
  </div>
  <a class="btn btn--ink" href="{page_href('career', lang, lang)}" data-rv>{H['path_cta'][lang]}{icon('arrow', 'ic btn-ic')}</a>
</div>
</section>
""")
    # 004 Align in numbers
    names = "".join(f'<li dir="ltr">{esc(c["name"])}</li>' for c in CONSULTING["clients"])
    out.append(sh.open("indigo", "align", label="align-h") + f"""<div class="ripples" aria-hidden="true"><i></i><i></i><i></i></div>
<div class="wrap split split--wide">
  <div class="split-a">
    {sec_title(H['align_title'][lang], lang, 'align-h')}
    <p class="big-p" data-rv>{rich(H['align_text'][lang], lang)}</p>
    <a class="btn btn--light" href="{page_href('consulting', lang, lang)}" data-rv>{H['align_cta'][lang]}{icon('arrow', 'ic btn-ic')}</a>
  </div>
  <ul class="names glass-dark" data-rv="pop">{names}</ul>
</div>
</section>
""")
    # 005 credentials
    v = CREDENTIALS["valid"]
    tiles = "".join(f"""<div class="ctile" data-rv style="--i:{i}">
  <span class="ctile-ic">{icon('award')}</span>
  <p class="ctile-n" dir="ltr">{esc(x['short']).replace('-', '\u2011')}</p>
  <p class="ctile-d">{rich(x['s_l'][lang], lang)}</p>
  <p class="ctile-by">{UI['valid_until'][lang]} {rich(x['e_l'][lang], lang)}</p>
</div>""" for i, x in enumerate([v[1], v[0]]))
    out.append(sh.open("paper", "creds", label="creds-h") + f"""<div class="wrap split">
  <div class="split-a">
    {sec_title(H['cred_title'][lang], lang, 'creds-h')}
    <p class="lede" data-rv>{rich(H['cred_line'][lang], lang)}</p>
    <a class="btn btn--ink" href="{page_href('credentials', lang, lang)}" data-rv>{H['cred_cta'][lang]}{icon('arrow', 'ic btn-ic')}</a>
  </div>
  <div class="split-b ctiles">{tiles}</div>
</div>
</section>
""")
    # 006 his words
    out.append(sh.open("white", "words", label="words-q") + f"""<div class="wrap">
  <figure class="quote" data-rv>
    <blockquote id="words-q"><p>{head_text(H['quote'][lang], lang)}</p></blockquote>
    <figcaption><span>{rich(H['quote_src'][lang], lang)}</span></figcaption>
  </figure>
  <a class="btn btn--ghost" href="{page_href('approach', lang, lang)}" data-rv>{H['quote_cta'][lang]}{icon('arrow', 'ic btn-ic')}</a>
</div>
</section>
""")
    return "".join(out), sh.n


def page_career(lang):
    C = CAREER
    G = GANTT
    sh = Sheets()
    out = [page_hero(sh, lang, C["h1"][lang], C["lead"][lang])]
    a, b = G["start"], G["end"]
    today = pct("now", a, b)
    years = "".join(f'<span style="--s:{pct(f"{y}-01", a, b):.2f}%">{y}</span>' for y in range(2022, 2027))
    rows = ""
    for i, r in enumerate(G["rows"]):
        s, e = pct(r["s"], a, b), pct(r["e"], a, b)
        before = ym(r["s"]) < ym(a)
        rows += (f'<button class="g-row g-row--{r["kind"]}" type="button" data-g="{r["id"]}" aria-pressed="false" aria-controls="gcap">'
                 f'<span class="g-label">{rich(r["label"][lang], lang)}</span>'
                 f'<span class="g-track" style="--today:{today:.2f}%"><span class="g-bar{" g-bar--cut" if before else ""}{" g-bar--now" if r["e"] == "now" else ""}" style="--s:{s:.2f}%;--w:{e - s:.2f}%"></span></span></button>')
    miles = "".join(f'<span class="g-mile" data-g="{m["id"]}" style="--s:{pct(m["d"], a, b):.2f}%">{"<b dir=ltr>" + str(m["n"]) + "</b>" if m["n"] > 1 else ""}</span>' for m in G["miles"])
    chips = "".join(f'<button class="chip g-chip" type="button" data-g="{m["id"]}" aria-pressed="false" aria-controls="gcap"><span>{rich(m["cap_t"][lang], lang)}</span></button>' for m in G["miles"])
    order = sorted(G["rows"] + G["miles"], key=lambda x: ym(x.get("s", x.get("d"))))
    caps = "".join(
        f'<div class="g-cap{" is-on" if j == len(order) - 1 else ""}" data-g="{x["id"]}"{"" if j == len(order) - 1 else " aria-hidden=\"true\""}>'
        f'<p class="g-cap-d">{rich(x["cap_d"][lang], lang)}</p><p class="g-cap-t">{rich(x["cap_t"][lang], lang)}</p>'
        f'<p class="g-cap-x">{rich(x["cap_x"][lang], lang)}</p></div>' for j, x in enumerate(order))
    seq = ",".join(x["id"] for x in order)
    out.append(sh.open("white", "schedule", "gsheet", label="schedule-h") + f"""<div class="wrap">
  {sec_title(C['gantt_title'][lang], lang, 'schedule-h')}
  <p class="lede" data-rv>{rich(C['gantt_lead'][lang], lang)}</p>
  <div class="gantt" data-gantt data-seq="{seq}" data-rv role="group" aria-label="{C['gantt_aria'][lang]}">
    <div class="g-axis" aria-hidden="true"><span class="g-axis-sp"></span><span class="g-axis-t" style="--today:{today:.2f}%">{years}<em class="g-today-l">{UI['today'][lang]}</em></span></div>
    <div class="g-rows">{rows}
      <div class="g-row g-row--miles" aria-hidden="true"><span class="g-label">{G['miles_label'][lang]}</span><span class="g-track" style="--today:{today:.2f}%">{miles}</span></div>
    </div>
    <div class="g-chips"><span class="g-chips-k">{G['miles_label'][lang]}</span>{chips}</div>
    <div class="g-caps glass-light" id="gcap" aria-live="off">{caps}</div>
  </div>
</div>
</section>
""")
    for r in C["roles"]:
        meta = "".join(f"<li><span>{rich(m[lang], lang)}</span></li>" for m in r["meta"])
        steps = ""
        if r.get("steps"):
            steps = '<ol class="steps">' + "".join(f'<li>{rich(s[lang], lang)}</li>' for s in r["steps"]) + "</ol>"
        pts = "".join(f'<li data-rv style="--i:{i}">{rich(p[lang], lang)}</li>' for i, p in enumerate(r["points"]))
        more = ""
        if r["more"]:
            mid = "more-" + r["id"]
            more = (f'<button class="more-btn" type="button" aria-expanded="false" aria-controls="{mid}">'
                    f'<span class="lbl"><span class="t-open">{UI["show"][lang]}</span><span class="t-close">{UI["hide"][lang]}</span></span>{icon("chev", "ic more-ic")}</button>'
                    f'<div class="more" id="{mid}"><div class="more-in"><ul class="points points--more">'
                    + "".join(f"<li>{rich(p[lang], lang)}</li>" for p in r["more"]) + "</ul></div></div>")
        note = f'<p class="role-note">{icon("cert", "ic ic-sm")}<span>{rich(r["note"][lang], lang)}</span></p>' if r.get("note") else ""
        kind = {"hrsd": "paper", "align": "white", "aramco": "paper"}[r["id"]]
        out.append(sh.open(kind, r["id"], "role", stack=not r["more"], label=r["id"] + "-h") + f"""<div class="wrap role-grid">
  <header class="role-head">
    {sec_title(r['org'][lang], lang, r['id'] + '-h', 'h2 role-org')}
    <p class="role-title" data-rv>{rich(r['title'][lang], lang)}</p>
    <ul class="meta" data-rv>{meta}</ul>
    {steps}
  </header>
  <div class="role-body">
    <ul class="points">{pts}</ul>
    {more}
    {note}
  </div>
</div>
</section>
""")
    out.append(next_sheet(sh, lang, "career"))
    return "".join(out), sh.n


def next_sheet(sh, lang, slug):
    nl = next_link(slug, lang)
    if not nl:
        return ""
    return sh.open("paper", "next", "sheet--next", stack=False) + f'<div class="wrap">{nl}</div>\n</section>\n'


def page_consulting(lang):
    C = CONSULTING
    sh = Sheets()
    out = [page_hero(sh, lang, C["h1"][lang], C["lead"][lang])]
    cards = ""
    n = len(C["clients"])
    for i, c in enumerate(C["clients"]):
        tags = "".join(f"<li><span>{rich(t[lang], lang)}</span></li>" for t in c["tags"])
        pmo = (f'<li class="tag-pmo"><i aria-hidden="true"></i>{C["pmo_tag"][lang]}</li>' if c["pmo"] else "")
        cards += f"""<li class="eng" style="--i:{i};--n:{n}">
  <article class="eng-card"><i class="shade" aria-hidden="true"></i>
    <p class="eng-no" dir="ltr">{i + 1:02d} / {n:02d}</p>
    <h3 class="eng-name" dir="ltr" lang="en">{esc(c['name'])}</h3>
    <p class="eng-t">{rich(c['text'][lang], lang)}</p>
    <ul class="tags">{tags}{pmo}</ul>
  </article>
</li>"""
    out.append(sh.open("paper", "clients", "sheet--engs", stack=False, label="clients-h") + f"""<div class="wrap">
  {sec_title(C['list_title'][lang], lang, 'clients-h')}
  <ol class="engs">{cards}</ol>
</div>
</section>
""")
    how = "".join(f'<li class="how-i" data-rv style="--i:{i}"><span class="how-ic">{icon(h["icon"])}</span><p>{rich(h["text"][lang], lang)}</p></li>'
                  for i, h in enumerate(C["how"]))
    out.append(sh.open("white", "how", label="how-h") + f"""<div class="wrap how">
  <div class="how-a">
    {sec_title(C['how_title'][lang], lang, 'how-h')}
    <p class="lede" data-rv>{rich(C['how_lead'][lang], lang)}</p>
  </div>
  <ul class="how-list">{how}</ul>
</div>
</section>
""")
    out.append(next_sheet(sh, lang, "consulting"))
    return "".join(out), sh.n


def page_approach(lang):
    A = APPROACH
    sh = Sheets()
    out = [page_hero(sh, lang, A["h1"][lang], A["lead"][lang])]
    seg_btn = "".join(
        f'<button class="seg-b" role="tab" type="button" id="seg-{s["id"]}" aria-controls="segp-{s["id"]}" aria-selected="{"true" if i == 0 else "false"}" tabindex="{0 if i == 0 else -1}">{s["label"][lang]}</button>'
        for i, s in enumerate(A["seg"]))
    seg_p = "".join(
        f'<div class="seg-p{" is-on" if i == 0 else ""}" role="tabpanel" id="segp-{s["id"]}" aria-labelledby="seg-{s["id"]}"{"" if i == 0 else " inert"}>'
        f'<p class="seg-t">{head_text(s["text"][lang], lang)}</p></div>'
        for i, s in enumerate(A["seg"]))
    mine = "ما يخصك" if lang == "ar" else "Yours"
    theirs = "ما ليس لك" if lang == "ar" else "Not yours"
    out.append(sh.open("white", "own", label="own-h") + f"""<div class="wrap split">
  <div class="split-a">
    {sec_title(A['seg_title'][lang], lang, 'own-h')}
    <p class="lede" data-rv>{rich(A['seg_note'][lang], lang)}</p>
  </div>
  <div class="split-b seg" data-seg data-rv data-state="own">
    <div class="seg-ctl" role="tablist" aria-label="{A['seg_label'][lang]}">{seg_btn}<span class="seg-thumb" aria-hidden="true"></span></div>
    <div class="lanes" aria-hidden="true">
      <span class="lane lane--a"><em>{mine}</em></span><span class="lane lane--b"><em>{theirs}</em></span><span class="lane-dot"></span>
    </div>
    <div class="seg-stage">{seg_p}</div>
  </div>
</div>
</section>
""")
    vals = "".join(
        f'<article class="vcard" data-pos="{i}" aria-roledescription="slide" aria-label="{i + 1} / {len(A["values"])}"{"" if i == 0 else " aria-hidden=\"true\""}>'
        f'<span class="vcard-no" dir="ltr">{i + 1:02d}</span><h3 class="vcard-n">{rich(v["name"][lang], lang)}</h3>'
        f'<p class="vcard-t">{rich(v["text"][lang], lang)}</p></article>'
        for i, v in enumerate(A["values"]))
    dots = "".join(f'<i{" class=\"is-on\"" if i == 0 else ""}></i>' for i in range(len(A["values"])))
    out.append(sh.open("indigo", "values", label="values-h") + f"""<div class="ripples" aria-hidden="true"><i></i><i></i><i></i></div>
<div class="wrap split">
  <div class="split-a">
    {sec_title(A['values_title'][lang], lang, 'values-h')}
    <p class="lede" data-rv>{rich(A['belief'][lang], lang)}</p>
  </div>
  <div class="split-b deck" data-deck data-rv role="region" aria-roledescription="carousel" aria-label="{A['values_label'][lang]}">
    <div class="deck-stage">{vals}</div>
    <div class="deck-ctl">
      <button class="round" type="button" data-deck-prev aria-label="{UI['prev_card'][lang]}">{icon('arrow', 'ic flip-x')}</button>
      <span class="deck-dots" aria-hidden="true">{dots}</span>
      <button class="round" type="button" data-deck-next aria-label="{UI['next_card'][lang]}">{icon('arrow')}</button>
    </div>
  </div>
</div>
</section>
""")
    out.append(sh.open("paper", "night", label="night-h") + f"""<div class="wrap split">
  <div class="split-a">
    {sec_title(A['night_title'][lang], lang, 'night-h')}
    <p class="lede" data-rv>{rich(A['night_text'][lang], lang)}</p>
  </div>
  <figure class="split-b quote quote--card" data-rv>
    <blockquote lang="ar" dir="rtl"><p>{rich(A['night_q1']['ar'], 'ar')}</p><p class="quote-2">{rich(A['night_q2']['ar'], 'ar')}</p></blockquote>
    {'' if lang == 'ar' else f'<p class="quote-tr">{rich(A["night_q1"]["en"], "en")} {rich(A["night_q2"]["en"], "en")}</p>'}
    <figcaption><span>{rich(A['night_src'][lang], lang)}</span></figcaption>
  </figure>
</div>
</section>
""")
    out.append(sh.open("white", "pmp", label="pmp-h") + f"""<div class="wrap narrow">
  <h2 class="h2 h2--q" id="pmp-h" data-rv="h">{rich(A['pmp_title'][lang], lang)}</h2>
  <p class="lede" data-rv>{rich(A['pmp_text'][lang], lang)}</p>
</div>
</section>
""")
    out.append(sh.open("indigo", "top-talent", label="tt-h") + f"""<div class="ripples" aria-hidden="true"><i></i><i></i><i></i></div>
<div class="wrap narrow">
  <h2 class="h2 h2--giant" id="tt-h" data-rv="h">{head_text(A['top_title'][lang], lang)}</h2>
  <p class="big-p" data-rv>{rich(A['top_text'][lang], lang)}</p>
</div>
</section>
""")
    out.append(next_sheet(sh, lang, "approach"))
    return "".join(out), sh.n


def page_credentials(lang):
    C = CREDENTIALS
    sh = Sheets()
    out = [page_hero(sh, lang, C["h1"][lang], C["lead"][lang])]
    cards = ""
    for i, v in enumerate(C["valid"]):
        span = ym(v["e"]) - ym(v["s"])
        el = max(0.0, min(1.0, (ym("now") - ym(v["s"])) / span))
        cards += f"""<article class="vc" data-rv style="--i:{i}" data-s="{v['s']}" data-e="{v['e']}">
  <span class="vc-ic">{icon('award')}</span>
  <h3 class="vc-n">{rich(v['name'][lang], lang)}</h3>
  <p class="vc-by">{rich(v['by'][lang], lang)}</p>
  <p class="vc-note">{rich(v['note'][lang], lang)}</p>
  <div class="vline" style="--el:{el:.4f}" role="img" aria-label="{C['valid_from'][lang]} {v['s_l'][lang]} {C['valid_to'][lang]} {v['e_l'][lang]}">
    <span class="vline-track"><span class="vline-fill"></span><span class="vline-now"></span><span class="vline-end"></span></span>
    <span class="vline-l"><span>{rich(v['s_l'][lang], lang)}</span><span>{rich(v['e_l'][lang], lang)}</span></span>
  </div>
</article>"""
    dots = "".join("<i></i>" for _ in C["valid"])
    out.append(sh.open("paper", "valid", label="valid-h") + f"""<div class="wrap">
  {sec_title(C['valid_title'][lang], lang, 'valid-h')}
  <p class="lede" data-rv>{rich(C['valid_lead'][lang], lang)}</p>
  <div class="swipe vcs" data-swipe role="region" aria-label="{C['valid_label'][lang]}" tabindex="0">{cards}</div>
  <div class="sdots" aria-hidden="true">{dots}</div>
</div>
</section>
""")
    progs = "".join(f"""<li class="prog" data-rv style="--i:{i}">
  <span class="prog-d">{rich(p['d'][lang], lang)}</span>
  <span class="prog-n" dir="ltr" lang="en">{esc(p['name'])}</span>
  <span class="prog-by">{rich(p['by'][lang], lang)}</span>
</li>""" for i, p in enumerate(C["progs"]))
    out.append(sh.open("white", "programmes", label="prog-h") + f"""<div class="wrap">
  {sec_title(C['prog_title'][lang], lang, 'prog-h')}
  <ol class="progs">{progs}</ol>
</div>
</section>
""")
    langs = "".join(f"<li>{l[lang]}</li>" for l in C["langs"])
    out.append(sh.open("indigo", "education", label="edu-h") + f"""<div class="ripples" aria-hidden="true"><i></i><i></i><i></i></div>
<div class="wrap split">
  <div class="split-a">
    {sec_title(C['edu_title'][lang], lang, 'edu-h')}
  </div>
  <div class="split-b edu glass-dark" data-rv="pop">
    <span class="edu-ic">{icon('grad')}</span>
    <p class="edu-s">{rich(C['edu_school'][lang], lang)}</p>
    <p class="edu-d">{rich(C['edu_degree'][lang], lang)}</p>
    <p class="edu-w">{rich(C['edu_when'][lang], lang)}</p>
    <p class="edu-a">{rich(C['edu_act'][lang], lang)}</p>
    <div class="edu-l"><span>{C['lang_title'][lang]}</span><ul>{langs}</ul></div>
  </div>
</div>
</section>
""")
    out.append(next_sheet(sh, lang, "credentials"))
    return "".join(out), sh.n


def page_contact(lang):
    C = CONTACT
    sh = Sheets()
    city = (f'<div class="ccard ccard--city glass-dark" data-rv><span class="ccard-ic">{icon("pin")}</span>'
            f'<span class="ccard-k">{UI["city"][lang]}</span><span class="ccard-v">{PERSON["city"][lang]}</span></div>')
    extra = (f'<div class="contact-mono" data-rv="pop">{mono_html(lang, "mono mono--xl")}</div>'
             f'<div class="ccards">{contact_cards(lang, "page")}{city}</div>')
    out = [page_hero(sh, lang, C["h1"][lang], C["lead"][lang], extra=extra)]
    faq = ""
    for i, f in enumerate(C["faq"]):
        fid = f"faq-{i}"
        faq += f"""<div class="faq-i" data-rv style="--i:{i}">
  <h3 class="faq-h"><button class="faq-q" type="button" aria-expanded="false" aria-controls="{fid}"><span>{rich(f['q'][lang], lang)}</span><span class="faq-pm" aria-hidden="true"></span></button></h3>
  <div class="more" id="{fid}"><div class="more-in"><p class="faq-a">{rich(f['a'][lang], lang)}</p></div></div>
</div>"""
    out.append(sh.open("paper", "faq", label="faq-h", stack=False) + f"""<div class="wrap narrow">
  {sec_title(C['faq_title'][lang], lang, 'faq-h')}
  <div class="faq">{faq}</div>
</div>
</section>
""")
    return "".join(out), sh.n


PAGE_FUN = {"index": page_index, "career": page_career, "consulting": page_consulting,
            "approach": page_approach, "credentials": page_credentials, "contact": page_contact}
META = {"index": HOME, "career": CAREER, "consulting": CONSULTING, "approach": APPROACH,
        "credentials": CREDENTIALS, "contact": CONTACT}


def build_page(slug, lang, versions):
    body, n = PAGE_FUN[slug](lang)
    m = META[slug]
    title, desc = plain(m["title"][lang]), plain(m["desc"][lang])
    return (head(slug, lang, title, desc, versions) + header(slug, lang, n + 1) +
            f'<main id="main" tabindex="-1">\n{body}</main>\n' + footer(slug, lang) +
            menu_and_cap(slug, lang) + scripts(lang, versions))


def build_404(versions):
    lang = "ar"
    N = NOT_FOUND
    from urllib.parse import urlparse
    base = f'<base href="{urlparse(BASE).path or "/"}">\n' if BASE else ""
    h = head("index", lang, N["title"][lang], N["lead"][lang], versions)
    h = h.replace('<meta charset="utf-8">\n', '<meta charset="utf-8">\n' + base, 1)
    h = re.sub(r'<link rel="(canonical|alternate)"[^>]*>\n', "", h)
    h = re.sub(r'<meta property="og:url"[^>]*>\n', "", h)
    h = h.replace('<meta name="robots" content="noindex">\n', "")
    h = h.replace("<meta name=\"author\"", '<meta name="robots" content="noindex">\n<meta name="author"', 1)
    h = h.replace("location.replace(", "void(")  # never redirect a 404
    sh = Sheets()
    links = "".join(f'<a class="chip chip--light" href="{page_href(s, lang, lang)}">{L(t, lang)}</a>' for s, t in NAV)
    extra = (f'<p class="lede" lang="en" dir="ltr">{N["h1"]["en"]} {N["lead"]["en"]}</p>'
             f'<div class="hero-cta"><a class="btn btn--light" href="./">{N["cta"][lang]}{icon("arrow", "ic btn-ic")}</a>'
             f'<a class="btn btn--line" href="en/" lang="en">{N["cta"]["en"]}</a></div><div class="chips404">{links}</div>')
    body = page_hero(sh, lang, N["h1"][lang], N["lead"][lang], extra=extra)
    return (h + header("index", lang, 1).replace(' aria-current="page"', "") + f'<main id="main" tabindex="-1">\n{body}</main>\n'
            + footer("404", lang) + menu_and_cap("index", lang).replace(' aria-current="page"', "") + scripts(lang, versions))


# ------------------------------------------------------------------ text files
def robots_txt():
    bots = ["GPTBot", "OAI-SearchBot", "ChatGPT-User", "ClaudeBot", "Claude-User", "Claude-SearchBot", "anthropic-ai",
            "PerplexityBot", "Perplexity-User", "Google-Extended", "Googlebot", "Bingbot", "Applebot", "Applebot-Extended",
            "DuckDuckBot", "YandexBot", "CCBot", "Meta-ExternalAgent"]
    s = "# Saleh Al Dakheel — personal site. Search engines and AI assistants are welcome.\n"
    s += "".join(f"User-agent: {b}\nAllow: /\n\n" for b in bots)
    s += "User-agent: *\nAllow: /\n"
    if BASE:
        s += f"\nSitemap: {BASE}sitemap.xml\n"
    return s


def sitemap_xml():
    if not BASE:
        return None
    rows = []
    for slug in PAGES:
        for lang in LANGS:
            alts = "".join(f'<xhtml:link rel="alternate" hreflang="{l}" href="{abs_url(slug, l)}"/>' for l in LANGS)
            alts += f'<xhtml:link rel="alternate" hreflang="x-default" href="{abs_url(slug, "ar")}"/>'
            rows.append(f"<url><loc>{abs_url(slug, lang)}</loc><lastmod>{TODAY.isoformat()}</lastmod>{alts}</url>")
    return ('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" '
            'xmlns:xhtml="http://www.w3.org/1999/xhtml">\n' + "\n".join(rows) + "\n</urlset>\n")


def llms_txt():
    b = BASE or ""
    lines = [
        "# Saleh Al Dakheel (صالح الدخيل)",
        "",
        "> Projects Manager in the Enterprise Project Management Office (EPMO) of Saudi Arabia's Ministry of Human Resources and Social Development (HRSD), Riyadh, since July 2026. Leads 18 active projects and oversees the enablement of 82 in the Sakhaa Program. PMP (Sep 2025) and PMI-PMOCP (May 2026). Previously Assistant Consultant and Consultant at Align Consulting (Dammam) and corrosion engineering trainee at Saudi Aramco. BSc Chemical Engineering, KFUPM (2018–2024).",
        "",
        "Arabic name: صالح الدخيل. Other spellings: Saleh Al-Dakheel, Saleh Aldakheel, Saleh H. Aldakheel.",
        "",
        "## Pages (Arabic, default)",
    ]
    for slug, t in NAV:
        lines.append(f"- [{t['ar']}]({b}{'' if slug == 'index' else FILE[slug]}): {plain(META[slug]['desc']['ar'])}")
    lines += ["", "## Pages (English)"]
    for slug, t in NAV:
        lines.append(f"- [{t['en']}]({b}en/{'' if slug == 'index' else FILE[slug]}): {plain(META[slug]['desc']['en'])}")
    lines += ["", "## Contact"]
    if CONFIG["EMAIL"]:
        lines.append(f"- Email: {CONFIG['EMAIL']}")
    if CONFIG["LINKEDIN"]:
        lines.append(f"- LinkedIn: {CONFIG['LINKEDIN']}")
    lines += ["", "## Optional", f"- [Full text of the site]({b}llms-full.txt)", ""]
    return "\n".join(lines)


def llms_full_txt():
    out = []
    for lang in ("en", "ar"):
        p = lambda d: plain(d[lang])
        out += [f"# {p(PERSON['name'])}", "", p(PERSON["role"]) + ".", p(PERSON["city"]), ""]
        out += ["## " + p(dict(NAV)["index"]), " ".join(p(m) for m in HOME["motto"]), p(HOME["job_lead"])]
        out += ["- " + p(t["label"]) + ": " + p(t["text"]) for t in HOME["tabs"]]
        out += [p(HOME["align_text"]), p(HOME["quote"]) + " (" + p(HOME["quote_src"]) + ")", ""]
        out += ["## " + p(dict(NAV)["career"]), p(CAREER["lead"]), ""]
        for r in CAREER["roles"]:
            out.append("### " + p(r["org"]).rstrip(".") + ": " + p(r["title"]))
            out.append(" | ".join(p(m) for m in r["meta"]))
            for s in r.get("steps", []):
                out.append("- " + p(s))
            out += ["- " + p(x) for x in r["points"] + r["more"]]
            if r.get("note"):
                out.append(p(r["note"]))
            out.append("")
        out += ["### " + p(GANTT["miles_label"])]
        out += ["- " + p(m["cap_t"]) + " — " + p(m["cap_d"]) + ". " + p(m["cap_x"]) for m in GANTT["miles"]]
        out += ["", "## " + p(dict(NAV)["consulting"]), p(CONSULTING["lead"]), ""]
        for c in CONSULTING["clients"]:
            out.append(f"- {c['name']}: {p(c['text'])}")
        out += ["", "### " + p(CONSULTING["how_title"]).rstrip(".")]
        out += ["- " + p(h["text"]) for h in CONSULTING["how"]]
        out += ["", "## " + p(dict(NAV)["approach"]), p(APPROACH["lead"])]
        out += ["- " + p(s["label"]) + ": " + p(s["text"]) for s in APPROACH["seg"]]
        out += [p(APPROACH["seg_note"]), ""]
        out += ["- " + p(v["name"]) + ": " + p(v["text"]) for v in APPROACH["values"]]
        out += [p(APPROACH["belief"]), "", p(APPROACH["night_title"]), p(APPROACH["night_text"]),
                p(APPROACH["night_q1"]) + " " + p(APPROACH["night_q2"]), "", p(APPROACH["pmp_title"]), p(APPROACH["pmp_text"]),
                "", p(APPROACH["top_text"]), ""]
        out += ["## " + p(dict(NAV)["credentials"])]
        out += [f"- {v['name']['en']} — {p(v['by'])} — {p(v['s_l'])} to {p(v['e_l'])}" if lang == "en" else
                f"- {v['name']['en']} — {p(v['by'])} — {p(v['s_l'])} إلى {p(v['e_l'])}" for v in CREDENTIALS["valid"]]
        out += [f"- {x['name']} — {p(x['by'])} — {p(x['d'])}" for x in CREDENTIALS["progs"]]
        out += [f"- {p(CREDENTIALS['edu_degree'])} — {p(CREDENTIALS['edu_school'])} — {p(CREDENTIALS['edu_when'])}. {p(CREDENTIALS['edu_act'])}",
                "- " + p(CREDENTIALS["lang_title"]) + ": " + ", ".join(p(x) for x in CREDENTIALS["langs"]), ""]
        out += ["## " + p(CONTACT["faq_title"]).rstrip(".")]
        for f in CONTACT["faq"]:
            out += ["Q: " + p(f["q"]), "A: " + p(f["a"]), ""]
        out += ["---", ""]
    return "\n".join(out)


# ------------------------------------------------------------------ main
def main():
    if os.path.isdir(OUT):
        shutil.rmtree(OUT)
    os.makedirs(os.path.join(OUT, "en"))
    shutil.copytree(os.path.join(SRC, "assets"), os.path.join(OUT, "assets"))
    versions = {"css": asset_v(os.path.join(SRC, "assets", "style.css")),
                "js": asset_v(os.path.join(SRC, "assets", "site.js"))}
    for slug in PAGES:
        for lang in LANGS:
            path = os.path.join(OUT, FILE[slug]) if lang == "ar" else os.path.join(OUT, "en", FILE[slug])
            with open(path, "w", encoding="utf-8") as f:
                f.write(build_page(slug, lang, versions))
    with open(os.path.join(OUT, "404.html"), "w", encoding="utf-8") as f:
        f.write(build_404(versions))
    files = {"robots.txt": robots_txt(), "sitemap.xml": sitemap_xml(), "llms.txt": llms_txt(),
             "llms-full.txt": llms_full_txt(), ".nojekyll": ""}
    if CONFIG["DOMAIN"]:
        files["CNAME"] = CONFIG["DOMAIN"] + "\n"
    for name, text in files.items():
        if text is None:
            continue
        with open(os.path.join(OUT, name), "w", encoding="utf-8") as f:
            f.write(text)
    n = sum(len(fs) for _, _, fs in os.walk(OUT))
    print(f"built {len(PAGES) * 2} pages + 404 into docs/ ({n} files), BASE_URL={BASE or '(empty)'}, PREVIEW={CONFIG['PREVIEW']}")


if __name__ == "__main__":
    main()
