#!/usr/bin/env python3
"""
Skool Community Feed Fetcher
- 進入 community 主頁（非 classroom），抓所有 post URL
- 抓 Jamie (@wu-chai-ing-3406) 本人寫的 posts 原文
- 加入到 jamie-skool-weekend-letters.json（追加模式）
"""
import datetime as dt
import json
import re
import sys
import time
from pathlib import Path

try:
    from playwright.sync_api import sync_playwright
except ImportError:
    sys.exit("pip3 install playwright")

COOKIES_PATH = Path("/Users/user/.claude/secrets/social-cookies.json")
OUT_FILE = Path.home() / "Desktop" / "Claude cowork" / "工作文件" / "素材" / "jamie-skool-weekend-letters.json"

COMMUNITY_URL = "https://www.skool.com/home-gym-3231"
JAMIE_PROFILE_URL = "https://www.skool.com/@wu-chai-ing-3406"


def load_skool_cookies():
    all_cookies = json.loads(COOKIES_PATH.read_text())
    out = []
    for c in all_cookies:
        if "skool" not in c.get("domain", "").lower():
            continue
        fixed = {
            "name": c["name"], "value": c["value"],
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


def main():
    cookies = load_skool_cookies()
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        ctx = browser.new_context(
            viewport={"width": 1440, "height": 900},
            user_agent="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36",
        )
        ctx.add_cookies(cookies)
        page = ctx.new_page()

        # 先看 Jamie profile 頁
        print(f"[step] Jamie profile {JAMIE_PROFILE_URL}")
        page.goto(JAMIE_PROFILE_URL, wait_until="domcontentloaded", timeout=30000)
        time.sleep(5)
        for _ in range(6):
            page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
            time.sleep(1.5)
        profile_text = page.inner_text("body")
        print(f"[profile text len] {len(profile_text)}")
        # 抓 /post/ 連結
        hrefs = page.eval_on_selector_all(
            "a",
            "els => [...new Set(els.map(e => e.href).filter(Boolean))]"
        )
        post_hrefs = [h for h in hrefs if "/post/" in h or "/home-gym-3231/" in h and h != COMMUNITY_URL]
        post_hrefs = [h for h in post_hrefs if "/classroom/" not in h and "/members" not in h]
        print(f"[profile] found {len(post_hrefs)} candidate post urls")
        for h in post_hrefs[:30]:
            print(f"   - {h}")

        # 同時試 community feed
        print(f"[step] community feed {COMMUNITY_URL}")
        page.goto(COMMUNITY_URL, wait_until="domcontentloaded", timeout=30000)
        time.sleep(5)
        for _ in range(10):
            page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
            time.sleep(1.2)
        feed_hrefs = page.eval_on_selector_all(
            "a",
            "els => [...new Set(els.map(e => e.href).filter(Boolean))]"
        )
        feed_posts = [h for h in feed_hrefs if "/home-gym-3231/" in h and "/classroom/" not in h and h != COMMUNITY_URL and "/members" not in h and "/calendar" not in h and "/map" not in h and "/leaderboards" not in h and "/about" not in h]
        print(f"[feed] found {len(feed_posts)} candidate post urls")
        for h in feed_posts[:40]:
            print(f"   - {h}")

        # 抓前 20 篇
        all_urls = list(dict.fromkeys(post_hrefs + feed_posts))[:25]
        print(f"\n[total to scrape] {len(all_urls)}")

        posts = []
        for i, u in enumerate(all_urls, 1):
            rec = {"url": u, "title": None, "body": None, "author": None, "date": None}
            try:
                page.goto(u, wait_until="domcontentloaded", timeout=25000)
                time.sleep(4)
                # 取 main 文字
                try:
                    body = page.query_selector("main")
                    if body:
                        rec["body"] = body.inner_text()[:4000]
                except Exception:
                    pass
                # 作者
                try:
                    txt = page.inner_text("body")
                    if "Wu chai Ing" in txt[:2000] or "Wuchai" in txt[:2000]:
                        rec["author"] = "Jamie (Wu chai Ing)"
                except Exception:
                    pass
                try:
                    h1 = page.query_selector("h1")
                    if h1:
                        rec["title"] = h1.inner_text().strip()
                except Exception:
                    pass
                m = re.search(
                    r'(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)\s+(\d{1,2})',
                    rec.get("body") or ""
                )
                if m:
                    rec["date"] = f"{m.group(1)} {m.group(2)}"
            except Exception as e:
                rec["error"] = str(e)
            print(f"[{i}/{len(all_urls)}] author={rec.get('author')} len={len(rec.get('body') or '')} title={(rec.get('title') or '')[:40]!r}")
            posts.append(rec)
            time.sleep(1.5)

        browser.close()

    # merge into existing file
    existing = {}
    if OUT_FILE.exists():
        try:
            existing = json.loads(OUT_FILE.read_text())
        except Exception:
            existing = {}
    existing.setdefault("posts", [])
    existing["community_feed_posts"] = posts
    existing["community_feed_fetched_at"] = dt.datetime.now().isoformat(timespec="seconds")
    OUT_FILE.write_text(json.dumps(existing, ensure_ascii=False, indent=2))
    print(f"\n[saved] {OUT_FILE}  (+{len(posts)} community posts)")


if __name__ == "__main__":
    main()
