#!/usr/bin/env python3
"""
IG Insights Fetcher (cookies-based, no Meta App needed)

Uses the Instagram session cookies already exported to /Users/user/.claude/secrets/social-cookies.json
to read Jamie's profile stats + recent post performance via browser automation.

Output: 工作文件/素材/ig-insights-YYYY-MM-DD.json
Consumed by: weekly-report skill

If cookies are stale (IG shows login page), re-export from Chrome.

Usage:
    python3 ig-insights-fetch.py [--username jamie_wu_1012] [--posts 20]
"""
import argparse
import datetime as dt
import json
import re
import sys
from pathlib import Path

try:
    from playwright.sync_api import sync_playwright
except ImportError:
    sys.exit("Install playwright first: pip3 install playwright")

COOKIES_PATH = Path("/Users/user/.claude/secrets/social-cookies.json")
OUTPUT_DIR = Path.home() / "Desktop" / "Claude cowork" / "工作文件" / "素材"


def load_ig_cookies():
    if not COOKIES_PATH.exists():
        sys.exit(f"Cookies not found at {COOKIES_PATH}. Re-export from Chrome.")
    all_cookies = json.loads(COOKIES_PATH.read_text())
    ig = [c for c in all_cookies if "instagram.com" in c.get("domain", "")]
    if not ig:
        sys.exit("No instagram.com cookies in file.")
    out = []
    for c in ig:
        fixed = {
            "name": c["name"],
            "value": c["value"],
            "domain": c.get("domain", ".instagram.com"),
            "path": c.get("path", "/"),
            "httpOnly": c.get("httpOnly", False),
            "secure": c.get("secure", True),
            "sameSite": c.get("sameSite", "Lax").title() if isinstance(c.get("sameSite"), str) else "Lax",
        }
        if "expirationDate" in c:
            fixed["expires"] = int(c["expirationDate"])
        out.append(fixed)
    return out


def parse_number(txt):
    if not txt:
        return None
    t = txt.replace(",", "").strip()
    m = re.match(r"([\d.]+)\s*([KMB萬])?", t)
    if not m:
        return None
    n = float(m.group(1))
    suf = m.group(2)
    return int(n * {"K": 1_000, "M": 1_000_000, "B": 1_000_000_000, "萬": 10_000, None: 1}.get(suf, 1))


def fetch(username, n_posts):
    cookies = load_ig_cookies()
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        ctx = browser.new_context(
            user_agent="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.4 Safari/605.1.15",
            locale="zh-TW",
        )
        ctx.add_cookies(cookies)
        page = ctx.new_page()
        url = f"https://www.instagram.com/{username}/"
        page.goto(url, wait_until="networkidle", timeout=30_000)

        if "accounts/login" in page.url:
            browser.close()
            sys.exit("Session expired. Re-export cookies from Chrome.")

        result = {
            "fetched_at": dt.datetime.now().isoformat(),
            "username": username,
            "url": url,
        }

        try:
            header_txt = page.locator("header").inner_text(timeout=5_000)
        except Exception:
            header_txt = ""
        result["header_raw"] = header_txt

        m_posts = re.search(r"([\d.,]+\s*[KM萬]?)\s*(?:posts|篇貼文|貼文)", header_txt)
        m_follow = re.search(r"([\d.,]+\s*[KM萬]?)\s*(?:followers|位?粉絲|名粉絲)", header_txt)
        m_following = re.search(r"([\d.,]+\s*[KM萬]?)\s*(?:following|追蹤中|追蹤)", header_txt)
        result["posts_count"] = parse_number(m_posts.group(1)) if m_posts else None
        result["followers"] = parse_number(m_follow.group(1)) if m_follow else None
        result["following"] = parse_number(m_following.group(1)) if m_following else None

        post_hrefs = page.evaluate(
            """() => Array.from(document.querySelectorAll("a[href*='/p/'], a[href*='/reel/']"))
                     .map(a => a.getAttribute('href'))
                     .filter((v, i, a) => v && a.indexOf(v) === i)"""
        )
        posts = [{"url": f"https://www.instagram.com{h}" if h.startswith("/") else h}
                 for h in post_hrefs[:n_posts]]
        result["recent_posts"] = posts

        browser.close()
        return result


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--username", default="jamie_wu_1012")
    ap.add_argument("--posts", type=int, default=20)
    args = ap.parse_args()

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    data = fetch(args.username, args.posts)

    today = dt.date.today().isoformat()
    out_path = OUTPUT_DIR / f"ig-insights-{today}.json"
    out_path.write_text(json.dumps(data, ensure_ascii=False, indent=2))
    print(f"saved: {out_path}")
    print(f"followers: {data.get('followers')}")
    print(f"posts: {data.get('posts_count')}")
    print(f"recent posts captured: {len(data.get('recent_posts', []))}")


if __name__ == "__main__":
    main()
