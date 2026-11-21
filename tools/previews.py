#!/usr/bin/env python3
"""Builds preview-phone.png and preview-desktop.png from the running local server.
    python3 tools/previews.py   (server: /tmp/ghp/saleh-al-dakheel -> docs/, port 8765)
"""
import os
from PIL import Image, ImageDraw
from playwright.sync_api import sync_playwright

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BASE = os.environ.get("SITE", "http://localhost:8765/saleh-al-dakheel/")
TMP = "/tmp/sd-previews"
os.makedirs(TMP, exist_ok=True)

PHONE = [  # (page, element to bring to the top, open menu?)
    ("index.html", None, False),
    ("career.html", "#schedule", False),
    ("approach.html", "#own", False),
    ("en/index.html", None, False),
    ("en/consulting.html", "#clients", False),
    ("en/credentials.html", None, True),
]
DESK = [("index.html", None), ("career.html", "#schedule"), ("en/index.html", None), ("en/consulting.html", "#clients")]


def shoot(b, w, h, page, anchor, menu, out, touch):
    ctx = b.new_context(viewport={"width": w, "height": h}, device_scale_factor=2 if touch else 1, is_mobile=touch, has_touch=touch)
    pg = ctx.new_page()
    pg.goto(BASE + page + "?stay", wait_until="networkidle")
    pg.wait_for_timeout(600)
    if anchor:
        pg.evaluate(f"(() => {{ const e = document.querySelector('{anchor}'); window.scrollTo({{top: e.getBoundingClientRect().top + scrollY - 0, behavior: 'instant'}}); }})()")
        pg.wait_for_timeout(300)
        pg.evaluate("window.scrollBy({top: 1, behavior: 'instant'})")
    pg.wait_for_timeout(3600)
    if menu:
        pg.tap("#capDot")
        pg.wait_for_timeout(1400)
    pg.screenshot(path=out)
    ctx.close()


def frame_phone(img, label):
    w, h = img.size
    pad = 26
    out = Image.new("RGB", (w + pad * 2, h + pad * 2 + 70), (234, 234, 242))
    mask = Image.new("L", (w, h), 0)
    ImageDraw.Draw(mask).rounded_rectangle((0, 0, w, h), radius=64, fill=255)
    shadow = Image.new("RGB", (w, h), (205, 204, 225))
    out.paste(shadow, (pad + 6, pad + 10), mask)
    out.paste(img, (pad, pad), mask)
    d = ImageDraw.Draw(out)
    try:
        from PIL import ImageFont
        font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 30)
    except Exception:
        font = None
    d.text((pad + 8, h + pad + 18), label, fill=(28, 27, 71), font=font)
    return out


def main():
    with sync_playwright() as p:
        b = p.chromium.launch()
        phones = []
        for i, (page, anchor, menu) in enumerate(PHONE):
            f = f"{TMP}/p{i}.png"
            shoot(b, 390, 844, page, anchor, menu, f, True)
            phones.append(frame_phone(Image.open(f).convert("RGB"), ("AR  " if not page.startswith("en/") else "EN  ") + page + ("  (menu)" if menu else "")))
        desks = []
        for i, (page, anchor) in enumerate(DESK):
            f = f"{TMP}/d{i}.png"
            shoot(b, 1440, 900, page, anchor, False, f, False)
            desks.append(Image.open(f).convert("RGB"))
        b.close()
    gap = 30
    W = sum(i.size[0] for i in phones) + gap * (len(phones) + 1)
    H = max(i.size[1] for i in phones) + gap * 2
    sheet = Image.new("RGB", (W, H), (241, 241, 243))
    x = gap
    for im in phones:
        sheet.paste(im, (x, gap)); x += im.size[0] + gap
    sheet = sheet.resize((W // 2, H // 2), Image.LANCZOS)
    sheet.save(os.path.join(ROOT, "preview-phone.png"), optimize=True)
    dw, dh = 1440, 900
    D = Image.new("RGB", (dw * 2 + gap * 3, dh * 2 + gap * 3), (241, 241, 243))
    for k, im in enumerate(desks):
        D.paste(im, (gap + (k % 2) * (dw + gap), gap + (k // 2) * (dh + gap)))
    D = D.resize((D.size[0] * 2 // 3, D.size[1] * 2 // 3), Image.LANCZOS)
    D.save(os.path.join(ROOT, "preview-desktop.png"), optimize=True)
    print("preview-phone.png", sheet.size, "preview-desktop.png", D.size)


if __name__ == "__main__":
    main()
