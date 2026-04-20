"""Screenshot carousel HTML cards to PNG files for IG upload."""
from playwright.sync_api import sync_playwright
import os

HTML = os.path.abspath(os.path.join(os.path.dirname(__file__), 'carousel-post-01-v2.html'))
OUT = os.path.join(os.path.dirname(__file__), 'carousel-output')
os.makedirs(OUT, exist_ok=True)

with sync_playwright() as p:
    browser = p.chromium.launch()
    context = browser.new_context(
        viewport={'width': 1200, 'height': 1450},
        device_scale_factor=2,
    )
    page = context.new_page()
    page.goto(f'file://{HTML}')
    page.wait_for_load_state('networkidle')

    # Force each card to render at IG exact size 1080x1350
    page.add_style_tag(content="""
        body{padding:0 !important;background:#2a2a2a !important}
        .page-hd{display:none !important}
        .grid{display:block !important;max-width:none !important;margin:0 !important;padding:0 !important}
        .card{
            width:1080px !important;height:1350px !important;
            aspect-ratio:unset !important;
            margin:0 !important;
            box-shadow:none !important;
        }
    """)
    page.wait_for_timeout(800)

    cards = page.query_selector_all('.card')
    for i, c in enumerate(cards, 1):
        c.scroll_into_view_if_needed()
        page.wait_for_timeout(200)
        c.screenshot(path=f'{OUT}/slide-{i:02d}.png')
        box = c.bounding_box()
        print(f'slide-{i:02d}.png  {int(box["width"])}x{int(box["height"])}')
    browser.close()

print(f'\n{len(cards)} PNGs saved to {OUT}/')
