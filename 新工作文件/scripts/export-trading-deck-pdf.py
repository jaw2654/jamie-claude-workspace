"""Export trading live deck HTML → PDF 6 pages 16:9"""
from playwright.sync_api import sync_playwright
from pathlib import Path

HTML = Path("/Users/user/Desktop/Claude cowork/工作文件/public/trading-live-deck.html").resolve()
OUT_PDF = Path("/Users/user/Desktop/Claude cowork/工作文件/public/trading-live-deck.pdf")

with sync_playwright() as p:
    browser = p.chromium.launch()
    ctx = browser.new_context(viewport={"width": 1920, "height": 1080})
    page = ctx.new_page()
    page.goto(f"file://{HTML}")
    page.wait_for_load_state("networkidle")
    page.wait_for_timeout(1500)
    page.pdf(
        path=str(OUT_PDF),
        width="1920px",
        height="1080px",
        print_background=True,
        margin={"top": "0", "right": "0", "bottom": "0", "left": "0"},
    )
    browser.close()
print(f"PDF → {OUT_PDF}")
