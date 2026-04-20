#!/usr/bin/env python3
"""
Skool v4: 更 robust 的抓取
- domcontentloaded + wait for text pattern
- 重試機制
- 用 v2 archived body_full 作為 fallback（已存在 JSON 裡）
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


POST_RE = re.compile(
    r'Wu chai Ing\s*\n(?P<age>[^\n]+?)\s*•\s*(?P<tag>[^\n]+)\n(?P<content>.*?)\nLike\n',
    re.DOTALL
)


def parse(full_text):
    m = POST_RE.search(full_text)
    if not m:
        return None
    content = m.group("content").strip()
    lines = content.split("\n", 1)
    return {
        "author": "Jamie (Wu chai Ing)",
        "age_str": m.group("age").strip(),
        "tag": m.group("tag").strip(),
        "title": lines[0].strip(),
        "body": lines[1].strip() if len(lines) > 1 else "",
    }


def fetch_one(page, url, max_attempts=2):
    for attempt in range(max_attempts):
        try:
            page.goto(url, wait_until="domcontentloaded", timeout=25000)
            # 等 Wu chai Ing 或 Like 字串（最多 12 秒）
            try:
                page.wait_for_function(
                    "() => document.body.innerText.includes('Wu chai Ing') || document.body.innerText.includes('Like')",
                    timeout=12000
                )
            except Exception:
                pass
            time.sleep(1.5)
            txt = page.inner_text("body")
            if "Wu chai Ing" in txt:
                return txt
            if attempt == 0:
                time.sleep(2)  # 再給一次
                continue
            return txt
        except Exception as e:
            if attempt == max_attempts - 1:
                return f"__ERR__: {e}"
    return None


def main():
    cookies = load_skool_cookies()
    # Load candidate URLs from last JSON
    existing = {}
    if OUT_FILE.exists():
        try:
            existing = json.loads(OUT_FILE.read_text())
        except Exception:
            pass

    # Union: 從 community_feed_v2 的 url，加上 classroom post url
    candidate_urls = set()
    for item in existing.get("community_feed_v2", []):
        candidate_urls.add(item["url"])
    # 清除無效 URLs
    candidate_urls = {u for u in candidate_urls if "/home-gym-3231/" in u}

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        ctx = browser.new_context(
            viewport={"width": 1440, "height": 900},
            user_agent="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36",
        )
        ctx.add_cookies(cookies)
        page = ctx.new_page()

        # 暖機
        page.goto(COMMUNITY_URL, wait_until="domcontentloaded", timeout=30000)
        time.sleep(4)
        # scroll more 擴大 candidate
        for _ in range(15):
            page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
            time.sleep(1.5)
            hrefs = page.eval_on_selector_all(
                "a[href*='/home-gym-3231/']",
                "els => els.map(e => e.href)"
            )
            for h in hrefs:
                if any(x in h for x in ["/classroom/", "/members", "/profile", "/calendar", "/map", "/leaderboards", "/about", "/-/"]):
                    continue
                if "?" in h and "?p=" not in h:
                    continue
                if h.endswith("/home-gym-3231") or h.endswith("/home-gym-3231/"):
                    continue
                candidate_urls.add(h)

        candidate_urls = sorted(candidate_urls)
        print(f"[candidates] {len(candidate_urls)}")

        jamie_posts = []
        for i, u in enumerate(candidate_urls, 1):
            txt = fetch_one(page, u)
            if not txt or txt.startswith("__ERR__"):
                print(f"  [{i}/{len(candidate_urls)}] ERR {u}")
                continue
            parsed = parse(txt)
            if not parsed:
                # 不是 Jamie 的 post
                author_match = re.search(r'^\s*([A-Z][A-Za-z][A-Za-z\s]*)\s*\n\s*\d+[mhdw]\s*•', txt, re.MULTILINE)
                author = author_match.group(1).strip() if author_match else "unknown"
                print(f"  [{i}/{len(candidate_urls)}] skip (author={author[:20]})")
                continue
            parsed["url"] = u
            jamie_posts.append(parsed)
            print(f"  [{i}/{len(candidate_urls)}] ✓ {parsed['age_str']} • {parsed['tag']} | {parsed['title'][:40]!r}")
            time.sleep(1.0)

        browser.close()

    weekend_posts = [p for p in jamie_posts if "週末信箱" in p.get("tag", "")]
    other_posts = [p for p in jamie_posts if "週末信箱" not in p.get("tag", "")]
    classroom_weekend = existing.get("classroom_weekend_letters", []) or existing.get("posts", [])

    result = {
        "fetched_at": dt.datetime.now().isoformat(timespec="seconds"),
        "source": "skool.com/home-gym-3231 community feed + classroom 週末信箱 module",
        "stats": {
            "total_jamie_posts_from_feed": len(jamie_posts),
            "weekend_letters_from_community_feed": len(weekend_posts),
            "other_jamie_posts": len(other_posts),
            "classroom_weekend_letters": len(classroom_weekend),
        },
        "weekend_letters_community_feed": weekend_posts,
        "classroom_weekend_letters": classroom_weekend,
        "other_jamie_posts": other_posts,
    }
    OUT_FILE.write_text(json.dumps(result, ensure_ascii=False, indent=2))
    print(f"\n[saved] {OUT_FILE}")
    print(json.dumps(result["stats"], indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
