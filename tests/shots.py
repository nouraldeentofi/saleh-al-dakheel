#!/usr/bin/env python3
"""Quick screenshots: python3 tests/shots.py [width] [pages...]  (server on :8765, site at /saleh-al-dakheel/)"""
import sys, os
from playwright.sync_api import sync_playwright
BASE = "http://localhost:8765/saleh-al-dakheel/"
OUT = os.path.join(os.path.dirname(__file__), "shots")
w = int(sys.argv[1]) if len(sys.argv) > 1 else 390
pages = sys.argv[2:] or ["index.html", "en/index.html"]
with sync_playwright() as p:
    b = p.chromium.launch()
    mobile = w < 800
    ctx = b.new_context(viewport={"width": w, "height": 844 if mobile else 900}, device_scale_factor=1, is_mobile=mobile, has_touch=mobile)
    for path in pages:
        pg = ctx.new_page()
        pg.goto(BASE + path + ("?stay" if "?" not in path else ""), wait_until="networkidle")
        pg.wait_for_timeout(400)
        h = pg.evaluate("document.documentElement.scrollHeight")
        for y in range(0, h, 500):
            pg.evaluate(f"window.scrollTo(0,{y})"); pg.wait_for_timeout(90)
        pg.evaluate("window.scrollTo(0,0)"); pg.wait_for_timeout(1800)
        name = path.replace("/", "_").replace(".html", "")
        pg.screenshot(path=f"{OUT}/{name}-{w}.png", full_page=True)
        pg.close()
    b.close()
print("ok")
