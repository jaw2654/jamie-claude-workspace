#!/usr/bin/env python3
"""
Skool final: 一步到位
1. Scroll community feed 抓所有 post urls
2. 每個 URL 都 goto + 等待 + 抓 body text，存 raw
3. 離線 regex parse
4. 加上 classroom 週末信箱
5. 輸出乾淨 JSON
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
RAW_FILE = Path.home() / "Desktop" / "Claude cowork" / "工作文件" / "素材" / "_skool-raw-dump.json"
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


def parse_post(text):
    m = POST_RE.search(text)
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
        "body_chars": len((lines[1] if len(lines) > 1 else "")),
    }


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

        # 暖機 + 滾動收集
        print("[step 1] scrolling community feed for URLs...")
        page.goto(COMMUNITY_URL, wait_until="domcontentloaded", timeout=30000)
        time.sleep(5)
        urls = set()
        for i in range(25):
            page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
            time.sleep(1.6)
            hrefs = page.eval_on_selector_all(
                "a[href*='/home-gym-3231/']",
                "els => els.map(e => e.href)"
            )
            for h in hrefs:
                if any(x in h for x in ["/classroom", "/members", "/profile", "/calendar", "/map", "/leaderboards", "/about", "/-/"]):
                    continue
                if h.rstrip("/") == COMMUNITY_URL:
                    continue
                urls.add(h)
        urls = sorted(urls)
        print(f"[collected] {len(urls)} URLs")

        # 暴力抓每個 URL 的 body text
        print(f"\n[step 2] fetching each post (networkidle + wait)...")
        raw_dump = []
        for i, u in enumerate(urls, 1):
            rec = {"url": u, "body_full": None, "error": None}
            try:
                page.goto(u, wait_until="domcontentloaded", timeout=30000)
                # 等到頁面有 "Wu chai Ing" 字串（或 timeout 15s）
                try:
                    page.wait_for_function(
                        "() => document.body.innerText.length > 400",
                        timeout=15000
                    )
                except Exception:
                    pass
                time.sleep(2.5)
                rec["body_full"] = page.inner_text("body")
            except Exception as e:
                rec["error"] = str(e)[:200]
            print(f"  [{i}/{len(urls)}] len={len(rec.get('body_full') or '')} err={rec.get('error')}")
            raw_dump.append(rec)
            time.sleep(0.8)

        browser.close()

    # 存 raw
    RAW_FILE.write_text(json.dumps(raw_dump, ensure_ascii=False, indent=2))
    print(f"\n[saved raw] {RAW_FILE}")

    # 離線 parse
    jamie_posts = []
    for item in raw_dump:
        if not item.get("body_full"):
            continue
        parsed = parse_post(item["body_full"])
        if parsed:
            parsed["url"] = item["url"]
            jamie_posts.append(parsed)

    # 讀 existing classroom posts
    existing = {}
    if OUT_FILE.exists():
        try:
            existing = json.loads(OUT_FILE.read_text())
        except Exception:
            pass

    classroom_weekend = existing.get("classroom_weekend_letters", [])
    weekend_feed = [p for p in jamie_posts if "週末信箱" in p.get("tag", "")]
    other = [p for p in jamie_posts if "週末信箱" not in p.get("tag", "")]

    result = {
        "fetched_at": dt.datetime.now().isoformat(timespec="seconds"),
        "source": "skool.com/home-gym-3231",
        "notes": "週末信箱 = tag 含 '週末信箱' 的 Jamie 親筆 post。其他 jamie posts 也保留（其他 tag 如「推薦」「閒聊」）。",
        "stats": {
            "total_jamie_authored": len(jamie_posts),
            "weekend_letters_community": len(weekend_feed),
            "classroom_weekend_letters": len(classroom_weekend),
            "other_jamie": len(other),
        },
        "weekend_letters_community": weekend_feed,
        "classroom_weekend_letters": classroom_weekend,
        "other_jamie_posts": other,
    }
    OUT_FILE.write_text(json.dumps(result, ensure_ascii=False, indent=2))
    print(f"[saved] {OUT_FILE}")
    print(json.dumps(result["stats"], indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
