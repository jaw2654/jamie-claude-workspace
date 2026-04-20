#!/usr/bin/env python3
"""
Skool Community Feed Fetcher v2
- 更長等待 + 更廣 selector，用 inner_text body 而非 main
- 過濾出 Jamie 作者的 posts
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

# 從上輪輸出手動挑出可能的 post slug（非 classroom / 非系統頁）
CANDIDATE_POSTS = [
    "https://www.skool.com/home-gym-3231/bcb65c9a",
    "https://www.skool.com/home-gym-3231/move-on-crew",
    "https://www.skool.com/home-gym-3231/move-on-crew?p=dccc5649",
    "https://www.skool.com/home-gym-3231/3222000",
    "https://www.skool.com/home-gym-3231/f43e1ea4",
    "https://www.skool.com/home-gym-3231/f43e1ea4?p=9db7b2cc",
    "https://www.skool.com/home-gym-3231/1-2",
    "https://www.skool.com/home-gym-3231/12-3",
    "https://www.skool.com/home-gym-3231/12-3?p=4055021e",
    "https://www.skool.com/home-gym-3231/2000-4",
    "https://www.skool.com/home-gym-3231/2026",
    "https://www.skool.com/home-gym-3231/e967505c",
    "https://www.skool.com/home-gym-3231/4191cc3a",
    "https://www.skool.com/home-gym-3231/6df76c3c",
    "https://www.skool.com/home-gym-3231/2126ec4f",
    "https://www.skool.com/home-gym-3231/2126ec4f?p=eeec358a",
    "https://www.skool.com/home-gym-3231/12-2",
    "https://www.skool.com/home-gym-3231/95205e57",
    "https://www.skool.com/home-gym-3231/95205e57?p=06cfbb01",
    "https://www.skool.com/home-gym-3231/e3d8ad27",
    "https://www.skool.com/home-gym-3231/e3d8ad27?p=9a14d378",
    "https://www.skool.com/home-gym-3231/b6470b89",
    "https://www.skool.com/home-gym-3231/b6470b89?p=ad04a20c",
    "https://www.skool.com/home-gym-3231/28c75640",
    "https://www.skool.com/home-gym-3231/28c75640?p=9d20f5cd",
    "https://www.skool.com/home-gym-3231/454-4kg",
    "https://www.skool.com/home-gym-3231/0bfacd39",
    "https://www.skool.com/home-gym-3231/11a24a33",
    "https://www.skool.com/home-gym-3231/11a24a33?p=c817284d",
    "https://www.skool.com/home-gym-3231/82bcd6e0",
    "https://www.skool.com/home-gym-3231/82bcd6e0?p=57639a84",
    "https://www.skool.com/home-gym-3231/880f2ba2",
    "https://www.skool.com/home-gym-3231/880f2ba2?p=6d860d86",
    "https://www.skool.com/home-gym-3231/9b521ac6",
    "https://www.skool.com/home-gym-3231/9b521ac6?p=ed83e3db",
    "https://www.skool.com/home-gym-3231/33a2b2dc",
]


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
        # 先暖機一次建立 session
        page.goto(COMMUNITY_URL, wait_until="domcontentloaded", timeout=30000)
        time.sleep(4)

        posts = []
        for i, u in enumerate(CANDIDATE_POSTS, 1):
            rec = {"url": u, "author": None, "title": None, "date": None, "body": None, "is_jamie": False}
            try:
                page.goto(u, wait_until="networkidle", timeout=30000)
                time.sleep(3)
                full_text = page.inner_text("body")
                rec["body_full"] = full_text
                # 判斷是否 Jamie
                if "Wu chai Ing" in full_text or "Wuchai" in full_text:
                    rec["author"] = "Jamie"
                    rec["is_jamie"] = True
                else:
                    # 找「某某人」pattern
                    m = re.search(r'^([A-Z][A-Za-z\s]{2,40})\s*\n\s*(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)', full_text, re.MULTILINE)
                    if m:
                        rec["author"] = m.group(1).strip()
                # h1 title
                try:
                    h1s = page.query_selector_all("h1, h2")
                    for h in h1s:
                        t = h.inner_text().strip()
                        if t and "MOVE ON CREW" not in t and len(t) > 3:
                            rec["title"] = t
                            break
                except Exception:
                    pass
                m = re.search(r'(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)\s+(\d{1,2})', full_text)
                if m:
                    rec["date"] = f"{m.group(1)} {m.group(2)}"
                # 抓 post 本文——去掉 navbar 雜訊
                # 找 "Wu chai Ing\n<date>" 後面 到 "Like" 或留言區前的段落
                mm = re.search(
                    r'Wu chai Ing\s*\n(?:.*?\n)?\s*(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)\s+\d+.*?\n(.*?)(?:\n(?:Like|Reply|Add comment|Comment)|\Z)',
                    full_text, re.DOTALL
                )
                if mm:
                    rec["body"] = mm.group(1).strip()[:5000]
            except Exception as e:
                rec["error"] = str(e)
            print(f"[{i}/{len(CANDIDATE_POSTS)}] jamie={rec['is_jamie']} date={rec.get('date')} title={(rec.get('title') or '')[:50]!r} body_len={len(rec.get('body') or '')}")
            posts.append(rec)
            time.sleep(1.5)

        browser.close()

    # merge
    existing = {}
    if OUT_FILE.exists():
        try:
            existing = json.loads(OUT_FILE.read_text())
        except Exception:
            pass
    existing["community_feed_v2_fetched_at"] = dt.datetime.now().isoformat(timespec="seconds")
    existing["community_feed_v2"] = posts
    jamie_only = [p for p in posts if p.get("is_jamie")]
    existing["jamie_community_posts"] = jamie_only
    OUT_FILE.write_text(json.dumps(existing, ensure_ascii=False, indent=2))
    print(f"\n[saved] {OUT_FILE}")
    print(f"[stats] total={len(posts)} jamie_authored={len(jamie_only)}")


if __name__ == "__main__":
    main()
