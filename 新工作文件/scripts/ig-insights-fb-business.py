#!/usr/bin/env python3
"""
IG Insights via business.facebook.com (uses .facebook.com cookies)

Tries to access Meta Business Suite's IG Insights page using Jamie's
existing Facebook session cookies. If session is alive, captures the
Insights overview screenshot + tries to extract structured data from
the rendered DOM.

Output:
  - 工作文件/素材/fb-business-insights-YYYY-MM-DD.json (parsed data + status)
  - 工作文件/素材/fb-business-insights-YYYY-MM-DD.png (screenshot)
  - 工作文件/素材/fb-business-insights-YYYY-MM-DD.html (full DOM for offline parse)

Note: Meta's Business Suite UI changes often. This is best-effort and
should be paired with the official Graph API path for production use.
"""
import datetime as dt
import json
import sys
from pathlib import Path

try:
    from playwright.sync_api import sync_playwright
except ImportError:
    sys.exit("Install playwright first")

COOKIES_PATH = Path("/Users/user/.claude/secrets/social-cookies.json")
OUTPUT_DIR = Path.home() / "Desktop" / "Claude cowork" / "工作文件" / "素材"

INSIGHTS_URL = "https://business.facebook.com/latest/insights/overview"


def load_facebook_cookies():
    if not COOKIES_PATH.exists():
        sys.exit(f"Cookies not found at {COOKIES_PATH}")
    all_cookies = json.loads(COOKIES_PATH.read_text())
    fb = [c for c in all_cookies if "facebook.com" in c.get("domain", "") or "instagram.com" in c.get("domain", "")]
    out = []
    for c in fb:
        fixed = {
            "name": c["name"],
            "value": c["value"],
            "domain": c.get("domain", ".facebook.com"),
            "path": c.get("path", "/"),
            "httpOnly": c.get("httpOnly", False),
            "secure": bool(c.get("secure", True)),
            "sameSite": (c.get("sameSite") or "Lax").title() if isinstance(c.get("sameSite"), str) else "Lax",
            "httpOnly": bool(c.get("httpOnly", False)),
        }
        exp = c.get("expirationDate")
        if exp:
            try:
                fixed["expires"] = int(exp)
            except (TypeError, ValueError):
                pass
        out.append(fixed)
    return out


def main():
    cookies = load_facebook_cookies()
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    today = dt.date.today().isoformat()
    json_out = OUTPUT_DIR / f"fb-business-insights-{today}.json"
    png_out = OUTPUT_DIR / f"fb-business-insights-{today}.png"
    html_out = OUTPUT_DIR / f"fb-business-insights-{today}.html"

    result = {
        "fetched_at": dt.datetime.now().isoformat(),
        "url": INSIGHTS_URL,
        "status": None,
        "final_url": None,
        "title": None,
        "screenshot": str(png_out),
        "html_dump": str(html_out),
    }

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        ctx = browser.new_context(
            user_agent="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.4 Safari/605.1.15",
            locale="zh-TW",
            viewport={"width": 1440, "height": 900},
        )
        ctx.add_cookies(cookies)
        page = ctx.new_page()

        try:
            page.goto(INSIGHTS_URL, wait_until="domcontentloaded", timeout=30_000)
            page.wait_for_timeout(5_000)  # let SPA hydrate
        except Exception as e:
            result["status"] = "navigation_error"
            result["error"] = str(e)
            json_out.write_text(json.dumps(result, ensure_ascii=False, indent=2))
            browser.close()
            print(json.dumps(result, ensure_ascii=False, indent=2))
            return

        result["final_url"] = page.url
        result["title"] = page.title()

        if "login" in page.url or "checkpoint" in page.url:
            result["status"] = "needs_login"
        else:
            result["status"] = "loaded"

        try:
            page.screenshot(path=str(png_out), full_page=True)
        except Exception as e:
            result["screenshot_error"] = str(e)

        try:
            html_out.write_text(page.content())
        except Exception as e:
            result["html_dump_error"] = str(e)

        browser.close()

    json_out.write_text(json.dumps(result, ensure_ascii=False, indent=2))
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
