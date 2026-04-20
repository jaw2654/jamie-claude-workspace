"""Screenshot v12 carousel HTML → 7 PNGs (1080×1350 for IG)."""
from playwright.sync_api import sync_playwright
from pathlib import Path

HTML = Path("/Users/user/Desktop/Claude cowork/工作文件/public/carousel-v12-lift-first.html").resolve()
OUT = Path("/Users/user/Desktop/Claude cowork/工作文件/public/v12-slides")
OUT.mkdir(parents=True, exist_ok=True)

with sync_playwright() as p:
    browser = p.chromium.launch()
    ctx = browser.new_context(viewport={"width": 1200, "height": 1450}, device_scale_factor=2)
    page = ctx.new_page()
    page.goto(f"file://{HTML}")
    page.wait_for_load_state("networkidle")
    # 強制每張卡片為 1080×1350（IG 規格）
    page.add_style_tag(content="""
      body{padding:0 !important;background:#0a0a0a !important}
      .page-hd{display:none !important}
      .row{display:block !important;max-width:none !important;margin:0 !important;padding:0 !important;gap:0 !important}
      .card{
        width:1080px !important;height:1350px !important;
        aspect-ratio:unset !important;
        margin:0 !important;box-shadow:none !important;border-radius:0 !important;
      }
    """)
    page.wait_for_timeout(1200)
    cards = page.query_selector_all(".card")
    for i, c in enumerate(cards, 1):
        c.scroll_into_view_if_needed()
        page.wait_for_timeout(200)
        c.screenshot(path=str(OUT / f"slide-{i:02d}.png"))
        box = c.bounding_box()
        print(f"slide-{i:02d}.png  {int(box['width'])}x{int(box['height'])}")
    browser.close()
print(f"\n{len(cards)} PNGs → {OUT}/")
