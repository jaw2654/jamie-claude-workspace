#!/usr/bin/env python3
"""
Skool Classroom Fetcher v2
- 用 Playwright + skool cookies 登入 Jamie 的 Skool 社群
- 進入「週末信箱」module (d399ed55)，展開所有 posts，抓原文
- 輸出: 工作文件/素材/jamie-skool-weekend-letters.json

Usage:
  python3 skool-fetch.py              # 全流程（抓週末信箱所有 posts）
  python3 skool-fetch.py --headful    # 開視窗看
"""
import argparse
import datetime as dt
import json
import re
import sys
import time
from pathlib import Path

try:
    from playwright.sync_api import sync_playwright
except ImportError:
    sys.exit("pip3 install playwright && playwright install chromium")

COOKIES_PATH = Path("/Users/user/.claude/secrets/social-cookies.json")
OUTPUT_DIR = Path.home() / "Desktop" / "Claude cowork" / "工作文件" / "素材"
OUT_FILE = OUTPUT_DIR / "jamie-skool-weekend-letters.json"

COMMUNITY_URL = "https://www.skool.com/home-gym-3231"
WEEKEND_MODULE_URL = "https://www.skool.com/home-gym-3231/classroom/d399ed55"


def load_skool_cookies():
    all_cookies = json.loads(COOKIES_PATH.read_text())
    sk = [c for c in all_cookies if "skool" in c.get("domain", "").lower()]
    out = []
    for c in sk:
        fixed = {
            "name": c["name"],
            "value": c["value"],
            "domain": c.get("domain", ".skool.com"),
            "path": c.get("path", "/"),
            "httpOnly": c.get("httpOnly", False),
            "secure": c.get("secure", True),
            "sameSite": "Lax",
        }
        exp = c.get("expires") or c.get("expirationDate")
        if exp and exp != -1:
            try:
                fixed["expires"] = int(exp)
            except (TypeError, ValueError):
                pass
        out.append(fixed)
    return out


def harvest_post_urls_from_module(page, module_url, timeout=30000):
    """進入 module 頁，等 SPA render，抓所有 md=xxx 的 post 連結"""
    page.goto(module_url, wait_until="domcontentloaded", timeout=timeout)
    time.sleep(6)
    # 滾動幾次以確保所有 posts 載入
    for _ in range(5):
        page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
        time.sleep(1.5)
    # 抓所有 href 含 md= 的連結
    hrefs = page.eval_on_selector_all(
        "a[href*='md=']",
        "els => [...new Set(els.map(e => e.href))]"
    )
    # 濾 d399ed55 module 下的
    module_prefix = "/classroom/d399ed55"
    return [h for h in hrefs if module_prefix in h]


def extract_post_content(page, url, timeout=30000):
    """抓 classroom post 頁的原文 + 標題 + 日期"""
    rec = {"url": url, "title": None, "body": None, "date": None, "raw_text_len": 0, "error": None}
    try:
        page.goto(url, wait_until="domcontentloaded", timeout=timeout)
        time.sleep(5)  # 等 SPA render
        # 嘗試 h1 title
        title = None
        for sel in ["h1", "[class*='module-header']", "[class*='ModuleTitle']", "h2"]:
            try:
                el = page.query_selector(sel)
                if el:
                    t = el.inner_text().strip()
                    if t and len(t) > 2 and "MOVE ON CREW" not in t:
                        title = t
                        break
            except Exception:
                pass
        rec["title"] = title

        # 抓 main content
        body = None
        for sel in [
            "[class*='PostBody']",
            "[class*='ModuleContent']",
            "[class*='LessonContent']",
            "main",
            "body",
        ]:
            try:
                el = page.query_selector(sel)
                if el:
                    body = el.inner_text()
                    if body and len(body) > 100:
                        break
            except Exception:
                pass
        rec["body"] = body
        rec["raw_text_len"] = len(body or "")

        # 抓日期（Mar 12, Apr 5, etc）
        try:
            txt = page.content()
            m = re.search(
                r'(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)\s+(\d{1,2})(?:,\s+(\d{4}))?',
                txt
            )
            if m:
                rec["date"] = f"{m.group(1)} {m.group(2)}" + (f", {m.group(3)}" if m.group(3) else "")
        except Exception:
            pass
    except Exception as e:
        rec["error"] = str(e)
    return rec


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--headful", action="store_true", help="開 UI 視窗")
    parser.add_argument("--max-posts", type=int, default=25)
    args = parser.parse_args()

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    cookies = load_skool_cookies()
    print(f"[cookies] loaded {len(cookies)} skool cookies")

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=not args.headful)
        ctx = browser.new_context(
            viewport={"width": 1440, "height": 900},
            user_agent="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36",
        )
        ctx.add_cookies(cookies)
        page = ctx.new_page()

        # 登入確認
        page.goto(COMMUNITY_URL, wait_until="domcontentloaded", timeout=30000)
        time.sleep(3)
        body_txt = page.inner_text("body")[:300]
        print(f"[login check] page head: {body_txt[:150]}")

        # 到週末信箱 module 頁抓所有 post 連結
        print(f"[harvest] {WEEKEND_MODULE_URL}")
        post_urls = harvest_post_urls_from_module(page, WEEKEND_MODULE_URL)
        print(f"[harvest] found {len(post_urls)} post urls in 週末信箱 module")
        for u in post_urls[:20]:
            print(f"   - {u}")

        # 去重後抓
        post_urls = list(dict.fromkeys(post_urls))[: args.max_posts]

        results = []
        for i, u in enumerate(post_urls, 1):
            print(f"[{i}/{len(post_urls)}] {u}")
            rec = extract_post_content(page, u)
            print(f"    title: {rec.get('title')!r}  body_len: {rec['raw_text_len']}  date: {rec.get('date')}")
            results.append(rec)
            time.sleep(2)

        browser.close()

    payload = {
        "fetched_at": dt.datetime.now().isoformat(timespec="seconds"),
        "source": "skool.com/home-gym-3231 - 週末信箱 module",
        "module_id": "d399ed55",
        "count": len(results),
        "posts": results,
    }
    OUT_FILE.write_text(json.dumps(payload, ensure_ascii=False, indent=2))
    print(f"\n[saved] {OUT_FILE}  ({len(results)} posts)")


if __name__ == "__main__":
    main()
