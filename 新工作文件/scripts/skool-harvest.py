#!/usr/bin/env python3
"""
Skool harvest:
- 硬編碼已知 43 個 post URL
- 每個 URL 都用長等待＋重試，把 body_full 存 raw
- 離線 parse
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

# 從之前 scroll 收集到的 URLs
KNOWN_URLS = [
    "https://www.skool.com/home-gym-3231/0bfacd39",
    "https://www.skool.com/home-gym-3231/1-2",
    "https://www.skool.com/home-gym-3231/11a24a33",
    "https://www.skool.com/home-gym-3231/11a24a33?p=c817284d",
    "https://www.skool.com/home-gym-3231/12-2",
    "https://www.skool.com/home-gym-3231/12-3",
    "https://www.skool.com/home-gym-3231/12-3?p=4055021e",
    "https://www.skool.com/home-gym-3231/131",
    "https://www.skool.com/home-gym-3231/2000-4",
    "https://www.skool.com/home-gym-3231/2026",
    "https://www.skool.com/home-gym-3231/2126ec4f",
    "https://www.skool.com/home-gym-3231/2126ec4f?p=eeec358a",
    "https://www.skool.com/home-gym-3231/243-25kg",
    "https://www.skool.com/home-gym-3231/28c75640",
    "https://www.skool.com/home-gym-3231/28c75640?p=9d20f5cd",
    "https://www.skool.com/home-gym-3231/3222000",
    "https://www.skool.com/home-gym-3231/33a2b2dc",
    "https://www.skool.com/home-gym-3231/4191cc3a",
    "https://www.skool.com/home-gym-3231/454-4kg",
    "https://www.skool.com/home-gym-3231/6df76c3c",
    "https://www.skool.com/home-gym-3231/82884467",
    "https://www.skool.com/home-gym-3231/82bcd6e0",
    "https://www.skool.com/home-gym-3231/82bcd6e0?p=57639a84",
    "https://www.skool.com/home-gym-3231/880f2ba2",
    "https://www.skool.com/home-gym-3231/880f2ba2?p=6d860d86",
    "https://www.skool.com/home-gym-3231/95205e57",
    "https://www.skool.com/home-gym-3231/95205e57?p=06cfbb01",
    "https://www.skool.com/home-gym-3231/9b521ac6",
    "https://www.skool.com/home-gym-3231/9b521ac6?p=ed83e3db",
    "https://www.skool.com/home-gym-3231/b6470b89",
    "https://www.skool.com/home-gym-3231/b6470b89?p=ad04a20c",
    "https://www.skool.com/home-gym-3231/bcb65c9a",
    "https://www.skool.com/home-gym-3231/e3d8ad27",
    "https://www.skool.com/home-gym-3231/e3d8ad27?p=9a14d378",
    "https://www.skool.com/home-gym-3231/e967505c",
    "https://www.skool.com/home-gym-3231/f43e1ea4",
    "https://www.skool.com/home-gym-3231/f43e1ea4?p=9db7b2cc",
    "https://www.skool.com/home-gym-3231/jamie-gpt24",
    "https://www.skool.com/home-gym-3231/jamie-gpt24?p=74b52ebf",
    "https://www.skool.com/home-gym-3231/move-on-crew",
    "https://www.skool.com/home-gym-3231/move-on-crew-2",
    "https://www.skool.com/home-gym-3231/move-on-crew?p=dccc5649",
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
    }


def fetch_with_retry(page, url, max_attempts=3):
    for attempt in range(max_attempts):
        try:
            page.goto(url, wait_until="domcontentloaded", timeout=25000)
            # 等頁面有 Like 字串或 Wu chai Ing（有回覆格式就停）
            try:
                page.wait_for_function(
                    "() => document.body.innerText.includes('Like') && document.body.innerText.length > 500",
                    timeout=12000
                )
            except Exception:
                pass
            time.sleep(2.5 + attempt)
            txt = page.inner_text("body")
            if len(txt) > 500 and ("Wu chai Ing" in txt or "MOVE ON CREW" in txt):
                return txt
        except Exception as e:
            if attempt == max_attempts - 1:
                return f"__ERR__:{e}"[:200]
    return txt if 'txt' in dir() else None


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

        # 暖機建立 session
        print("[warmup]")
        page.goto(COMMUNITY_URL, wait_until="domcontentloaded", timeout=30000)
        time.sleep(6)

        print(f"[fetching {len(KNOWN_URLS)} posts]")
        raw_dump = []
        for i, u in enumerate(KNOWN_URLS, 1):
            txt = fetch_with_retry(page, u)
            rec = {"url": u, "body_full": txt}
            raw_dump.append(rec)
            blen = len(txt) if txt and not txt.startswith("__ERR__") else 0
            print(f"  [{i}/{len(KNOWN_URLS)}] len={blen} {'ERR' if blen==0 else ''}")
            time.sleep(0.8)

        browser.close()

    RAW_FILE.write_text(json.dumps(raw_dump, ensure_ascii=False, indent=2))
    print(f"\n[saved raw] {RAW_FILE}")

    # offline parse
    jamie_posts = []
    for item in raw_dump:
        if not item.get("body_full") or item["body_full"].startswith("__ERR__"):
            continue
        parsed = parse_post(item["body_full"])
        if parsed:
            parsed["url"] = item["url"]
            jamie_posts.append(parsed)

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
        "notes": "週末信箱 tag = Jamie 親筆「letter from founder」型長文。其他 jamie posts 也保留。",
        "stats": {
            "total_jamie_authored": len(jamie_posts),
            "weekend_letters_community_feed": len(weekend_feed),
            "classroom_weekend_letters": len(classroom_weekend),
            "other_jamie": len(other),
        },
        "weekend_letters_community_feed": weekend_feed,
        "classroom_weekend_letters": classroom_weekend,
        "other_jamie_posts": other,
    }
    OUT_FILE.write_text(json.dumps(result, ensure_ascii=False, indent=2))
    print(f"[saved] {OUT_FILE}")
    print(json.dumps(result["stats"], indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
