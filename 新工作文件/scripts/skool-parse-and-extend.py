#!/usr/bin/env python3
"""
Skool v3:
1. Scroll community feed 更深，抓更多 post URLs
2. 對每個 URL 用 page.inner_text('body')
3. 用正確 regex 解析「Wu chai Ing\n<date> • <tag>\n<title/body>」結構
4. 只保留 Jamie 本人的 post
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


POST_BODY_RE = re.compile(
    r'Wu chai Ing\s*\n(?P<age>[\w\d\s]+?)\s*•\s*(?P<tag>[^\n]+)\n(?P<content>.*?)\nLike\n',
    re.DOTALL
)


def parse_post(full_text):
    """解析 body_full，返回 dict（作者/日期/tag/title/content）"""
    m = POST_BODY_RE.search(full_text)
    if not m:
        return None
    content = m.group("content").strip()
    # 第一行是 title
    lines = content.split("\n", 1)
    title = lines[0].strip()
    body = lines[1].strip() if len(lines) > 1 else ""
    return {
        "author": "Jamie (Wu chai Ing)",
        "age_str": m.group("age").strip(),
        "tag": m.group("tag").strip(),
        "title": title,
        "body": body,
    }


def gather_post_urls(page):
    """Scroll community feed 10 次，抓所有 post URLs"""
    page.goto(COMMUNITY_URL, wait_until="domcontentloaded", timeout=30000)
    time.sleep(5)
    urls = set()
    for i in range(20):
        page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
        time.sleep(1.8)
        hrefs = page.eval_on_selector_all(
            "a[href*='/home-gym-3231/']",
            "els => els.map(e => e.href)"
        )
        for h in hrefs:
            # 排除 classroom、系統頁、members、profile
            if any(x in h for x in ["/classroom/", "/members", "/profile", "/calendar", "/map", "/leaderboards", "/about", "/-/", "skool.com/home-gym-3231?"]):
                continue
            if h == COMMUNITY_URL or h == COMMUNITY_URL + "/":
                continue
            urls.add(h)
        if i % 5 == 4:
            print(f"    [scroll {i+1}] urls collected: {len(urls)}")
    return sorted(urls)


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

        print("[step 1] gathering post URLs from community feed...")
        post_urls = gather_post_urls(page)
        print(f"[gather] got {len(post_urls)} candidate URLs")

        print(f"\n[step 2] scraping each post...")
        all_posts = []
        for i, u in enumerate(post_urls, 1):
            try:
                page.goto(u, wait_until="networkidle", timeout=25000)
                time.sleep(2.5)
                full_text = page.inner_text("body")
            except Exception as e:
                print(f"  [{i}] ERR {u} - {e}")
                continue
            parsed = parse_post(full_text)
            if not parsed:
                # 不是 Jamie 寫的，或 format 不符合
                snippet = full_text[:120].replace("\n", " | ")
                print(f"  [{i}/{len(post_urls)}] SKIP (not jamie) {u} | {snippet[:60]}")
                continue
            parsed["url"] = u
            all_posts.append(parsed)
            print(f"  [{i}/{len(post_urls)}] ✓ {parsed['age_str']} • {parsed['tag']} | {parsed['title'][:40]!r} ({len(parsed['body'])}ch)")
            time.sleep(1.2)

        browser.close()

    # 讀現有檔案 + merge
    existing = {}
    if OUT_FILE.exists():
        try:
            existing = json.loads(OUT_FILE.read_text())
        except Exception:
            pass

    # 分類：週末信箱 tag
    weekend_posts = [p for p in all_posts if "週末信箱" in p.get("tag", "")]
    other_posts = [p for p in all_posts if "週末信箱" not in p.get("tag", "")]

    result = {
        "fetched_at": dt.datetime.now().isoformat(timespec="seconds"),
        "source": "skool.com/home-gym-3231 community feed + classroom 週末信箱 module",
        "stats": {
            "total_jamie_posts": len(all_posts),
            "weekend_letters_from_community_feed": len(weekend_posts),
            "classroom_weekend_letters": len(existing.get("posts", [])),
            "other_jamie_posts": len(other_posts),
        },
        "weekend_letters_community_feed": weekend_posts,
        "classroom_weekend_letters": existing.get("posts", []),
        "other_jamie_posts": other_posts,
    }
    OUT_FILE.write_text(json.dumps(result, ensure_ascii=False, indent=2))
    print(f"\n[saved] {OUT_FILE}")
    print(f"  weekend_letters (community feed): {len(weekend_posts)}")
    print(f"  classroom_weekend_letters: {len(existing.get('posts', []))}")
    print(f"  other_jamie_posts: {len(other_posts)}")


if __name__ == "__main__":
    main()
