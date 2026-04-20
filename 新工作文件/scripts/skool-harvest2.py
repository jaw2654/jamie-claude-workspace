#!/usr/bin/env python3
"""
Skool harvest v2 - 確保登入態
- 直接用 browser_cookie3 拿 live Chrome cookies（含 auth_token）
- Playwright 注入後 reload 驗證登入
- 然後逐一 fetch
"""
import datetime as dt
import json
import re
import sys
import time
from pathlib import Path

try:
    from playwright.sync_api import sync_playwright
    import browser_cookie3
except ImportError:
    sys.exit("pip3 install playwright browser_cookie3")

OUT_FILE = Path.home() / "Desktop" / "Claude cowork" / "工作文件" / "素材" / "jamie-skool-weekend-letters.json"
RAW_FILE = Path.home() / "Desktop" / "Claude cowork" / "工作文件" / "素材" / "_skool-raw-dump.json"
COMMUNITY_URL = "https://www.skool.com/home-gym-3231"

KNOWN_URLS = [
    "https://www.skool.com/home-gym-3231/0bfacd39",
    "https://www.skool.com/home-gym-3231/1-2",
    "https://www.skool.com/home-gym-3231/11a24a33",
    "https://www.skool.com/home-gym-3231/12-2",
    "https://www.skool.com/home-gym-3231/12-3",
    "https://www.skool.com/home-gym-3231/131",
    "https://www.skool.com/home-gym-3231/2000-4",
    "https://www.skool.com/home-gym-3231/2026",
    "https://www.skool.com/home-gym-3231/2126ec4f",
    "https://www.skool.com/home-gym-3231/243-25kg",
    "https://www.skool.com/home-gym-3231/28c75640",
    "https://www.skool.com/home-gym-3231/3222000",
    "https://www.skool.com/home-gym-3231/33a2b2dc",
    "https://www.skool.com/home-gym-3231/4191cc3a",
    "https://www.skool.com/home-gym-3231/454-4kg",
    "https://www.skool.com/home-gym-3231/6df76c3c",
    "https://www.skool.com/home-gym-3231/82884467",
    "https://www.skool.com/home-gym-3231/82bcd6e0",
    "https://www.skool.com/home-gym-3231/880f2ba2",
    "https://www.skool.com/home-gym-3231/95205e57",
    "https://www.skool.com/home-gym-3231/9b521ac6",
    "https://www.skool.com/home-gym-3231/b6470b89",
    "https://www.skool.com/home-gym-3231/bcb65c9a",
    "https://www.skool.com/home-gym-3231/e3d8ad27",
    "https://www.skool.com/home-gym-3231/e967505c",
    "https://www.skool.com/home-gym-3231/f43e1ea4",
    "https://www.skool.com/home-gym-3231/jamie-gpt24",
    "https://www.skool.com/home-gym-3231/move-on-crew",
    "https://www.skool.com/home-gym-3231/move-on-crew-2",
]


def load_skool_cookies_from_chrome():
    cj = browser_cookie3.chrome(domain_name="skool.com")
    out = []
    for c in cj:
        fixed = {
            "name": c.name,
            "value": c.value,
            "domain": c.domain if c.domain.startswith(".") else "." + c.domain.lstrip("www."),
            "path": c.path or "/",
            "httpOnly": False,
            "secure": bool(c.secure),
            "sameSite": "Lax",
        }
        # 關鍵 cookies 強制 domain = .skool.com
        if c.name in ("auth_token", "client_id"):
            fixed["domain"] = ".skool.com"
        if c.expires:
            try:
                fixed["expires"] = int(c.expires)
            except Exception:
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


def main():
    cookies = load_skool_cookies_from_chrome()
    print(f"[cookies] {len(cookies)} skool cookies loaded direct from Chrome")
    has_auth = any(c["name"] == "auth_token" for c in cookies)
    print(f"[cookies] auth_token present: {has_auth}")

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        ctx = browser.new_context(
            viewport={"width": 1440, "height": 900},
            user_agent="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36",
        )
        ctx.add_cookies(cookies)
        page = ctx.new_page()

        # 驗證登入狀態
        print("[check] community page...")
        page.goto(COMMUNITY_URL, wait_until="domcontentloaded", timeout=30000)
        time.sleep(5)
        head = page.inner_text("body")[:400]
        logged_in = "LOG IN" not in head.upper()[:200] and ("Community" in head or "Classroom" in head)
        print(f"[check] logged_in={logged_in}")
        print(f"[check] head: {head[:200]!r}")
        if not logged_in:
            # 多試一次 reload
            time.sleep(3)
            page.reload(wait_until="domcontentloaded", timeout=30000)
            time.sleep(5)
            head = page.inner_text("body")[:400]
            print(f"[check after reload] head: {head[:200]!r}")

        print(f"\n[fetching {len(KNOWN_URLS)} posts]")
        raw_dump = []
        for i, u in enumerate(KNOWN_URLS, 1):
            txt = None
            for attempt in range(3):
                try:
                    page.goto(u, wait_until="domcontentloaded", timeout=25000)
                    try:
                        page.wait_for_function(
                            "() => document.body.innerText.includes('Wu chai Ing') || document.body.innerText.includes('Like')",
                            timeout=10000
                        )
                    except Exception:
                        pass
                    time.sleep(2 + attempt * 1.5)
                    t = page.inner_text("body")
                    if len(t) > 800 and "LOG IN" not in t.upper()[:200]:
                        txt = t
                        break
                    if attempt < 2:
                        time.sleep(3)
                except Exception as e:
                    if attempt == 2:
                        txt = f"__ERR__:{e}"[:300]
            rec = {"url": u, "body_full": txt}
            raw_dump.append(rec)
            blen = len(txt) if txt and not txt.startswith("__ERR__") else 0
            has_jamie = (txt and "Wu chai Ing" in txt)
            print(f"  [{i}/{len(KNOWN_URLS)}] len={blen} jamie={has_jamie}")
            time.sleep(0.8)

        browser.close()

    RAW_FILE.write_text(json.dumps(raw_dump, ensure_ascii=False, indent=2))
    print(f"\n[saved raw] {RAW_FILE}")

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
