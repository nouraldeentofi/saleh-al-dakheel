#!/usr/bin/env python3
"""Renders the share image (og.png) and the home-screen icons with the site's own fonts.
    python3 tools/make_images.py      (needs: pip install playwright && playwright install chromium)
"""
import os
from playwright.sync_api import sync_playwright

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
IMG = os.path.join(ROOT, "src", "assets", "img")
FONTS = "file://" + os.path.join(ROOT, "src", "assets", "fonts")

FACE = f"""
@font-face{{font-family:K;src:url({FONTS}/kufam-ar-700.woff2)}}
@font-face{{font-family:A;src:url({FONTS}/alexandria-ar-400.woff2)}}
@font-face{{font-family:O;src:url({FONTS}/outfit-la-400.woff2);font-weight:400}}
@font-face{{font-family:O;src:url({FONTS}/outfit-la-600.woff2);font-weight:600}}
@font-face{{font-family:O;src:url({FONTS}/outfit-la-700.woff2);font-weight:700}}
*{{margin:0;box-sizing:border-box}}
"""

OG = f"""<html><style>{FACE}
body{{width:1200px;height:630px;background:#3D3B8E;color:#fff;font-family:A,O;position:relative;overflow:hidden}}
.rings{{position:absolute;left:290px;top:250px;width:1400px;height:1400px;margin:-700px;border-radius:50%;
 background:repeating-radial-gradient(circle,transparent 0 70px,rgba(185,183,242,.16) 70px 71.5px,transparent 71.5px 140px);
 -webkit-mask:radial-gradient(closest-side,#000 25%,transparent 100%)}}
.wrap{{position:absolute;top:150px;right:80px;width:1040px}}
h1{{font:700 104px/1.3 K,O;}}
.stop{{display:inline-block;width:24px;height:24px;border-radius:50%;background:#B9B7F2;margin-right:8px}}
.en{{font:600 40px/1.2 O;color:#DAD9FA;direction:ltr;text-align:right;margin-top:4px}}
.role{{font:400 30px/1.6 A,O;color:#D6D5F3;margin-top:34px;max-width:860px}}
.creds{{position:absolute;left:80px;bottom:72px;display:flex;gap:14px;direction:ltr}}
.creds span{{font:600 26px/1 O;padding:16px 24px;border-radius:999px;background:rgba(255,255,255,.1);border:1px solid rgba(255,255,255,.2)}}
.dots{{position:absolute;left:80px;top:150px;display:grid;grid-template-columns:repeat(6,22px);gap:12px}}
.dots i{{width:22px;height:22px;border-radius:50%;background:#B9B7F2}}
</style><body><div class="rings"></div>
<div class="dots">{''.join('<i></i>' for _ in range(18))}</div>
<div class="wrap" dir="rtl"><h1>صالح الدخيل<span class="stop"></span></h1><p class="en">Saleh Al Dakheel</p>
<p class="role">مدير مشاريع في مكتب إدارة المشاريع المؤسسي (EPMO) بوزارة الموارد البشرية والتنمية الاجتماعية</p></div>
<div class="creds"><span>PMP®</span><span>PMI-PMOCP</span></div>
</body></html>"""

ICON = f"""<html><style>{FACE}
body{{width:512px;height:512px;background:#3D3B8E;display:grid;place-items:center;overflow:hidden}}
.m{{display:inline-flex;align-items:baseline;color:#fff;font:700 250px/1 K;transform:translate(10px,-38px)}}
.m i{{display:inline-block;width:58px;height:58px;border-radius:50%;background:#B9B7F2;margin-right:18px}}
</style><body><span class="m" dir="rtl"><span>ص</span><i></i></span></body></html>"""


def main():
    with sync_playwright() as p:
        b = p.chromium.launch()
        tmp = os.path.join(IMG, "_og.html")
        open(tmp, "w", encoding="utf-8").write(OG)
        pg = b.new_page(viewport={"width": 1200, "height": 630})
        pg.goto("file://" + tmp)
        pg.wait_for_timeout(600)
        pg.screenshot(path=os.path.join(IMG, "og.png"))
        os.remove(tmp)
        tmp = os.path.join(IMG, "_icon.html")
        open(tmp, "w", encoding="utf-8").write(ICON)
        pg = b.new_page(viewport={"width": 512, "height": 512})
        pg.goto("file://" + tmp)
        pg.wait_for_timeout(400)
        big = os.path.join(IMG, "icon-512.png")
        pg.screenshot(path=big)
        os.remove(tmp)
        for size, name in ((180, "apple-touch-icon.png"), (32, "favicon-32.png")):
            q = b.new_page(viewport={"width": size, "height": size})
            q.set_content(f'<html><body style="margin:0"><img src="file://{big}" width="{size}" height="{size}"></body></html>')
            q.wait_for_timeout(200)
            q.screenshot(path=os.path.join(IMG, name))
        b.close()
    print("og.png, icon-512.png, apple-touch-icon.png, favicon-32.png written to src/assets/img")


if __name__ == "__main__":
    main()
