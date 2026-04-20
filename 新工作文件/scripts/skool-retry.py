#!/usr/bin/env python3
"""重試之前 len=0 的 URLs，用更長等待"""
import datetime as dt
import json
import re
import time
from pathlib import Path
from playwright.sync_api import sync_playwright
import browser_cookie3

OUT_FILE = Path.home() / "Desktop" / "Claude cowork" / "工作文件" / "素材" / "jamie-skool-weekend-letters.json"
RAW_FILE = Path.home() / "Desktop" / "Claude cowork" / "工作文件" / "素材" / "_skool-raw-dump.json"
COMMUNITY_URL = "https://www.skool.com/home-gym-3231"


def load_cookies():
    cj = browser_cookie3.chrome(domain_name="skool.com")
    out = []
    for c in cj:
        fixed = {"name": c.name, "value": c.value,
                 "domain": c.domain if c.domain.startswith(".") else "." + c.domain.lstrip("www."),
                 "path": c.path or "/", "httpOnly": False, "secure": bool(c.secure), "sameSite": "Lax"}
        if c.name in ("auth_token", "client_id"):
            fixed["domain"] = ".skool.com"
        if c.expires:
            try: fixed["expires"] = int(c.expires)
            except: pass
        out.append(fixed)
    return out


def main():
    raw = json.loads(RAW_FILE.read_text())
    missing = [x for x in raw if not x.get("body_full") or len(x["body_full"]) == 0]
    print(f"[retry] {len(missing)} urls")

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        ctx = browser.new_context(
            viewport={"width": 1440, "height": 900},
            user_agent="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36",
        )
        ctx.add_cookies(load_cookies())
        page = ctx.new_page()
        # 暖機
        page.goto(COMMUNITY_URL, wait_until="domcontentloaded", timeout=30000)
        time.sleep(6)

        for i, item in enumerate(missing, 1):
            u = item["url"]
            txt = None
            for attempt in range(4):
                try:
                    page.goto(u, wait_until="domcontentloaded", timeout=30000)
                    try:
                        page.wait_for_function(
                            "() => document.body.innerText.includes('Like') || document.body.innerText.length > 600",
                            timeout=15000
                        )
                    except Exception:
                        pass
                    time.sleep(3 + attempt)
                    t = page.inner_text("body")
                    if len(t) > 500:
                        txt = t
                        break
                    time.sleep(3)
                except Exception:
                    pass
            item["body_full"] = txt or ""
            print(f"  [{i}/{len(missing)}] len={len(txt or '')} {u[-30:]}")
            time.sleep(0.8)

        browser.close()

    # update raw
    RAW_FILE.write_text(json.dumps(raw, ensure_ascii=False, indent=2))
    print(f"[saved raw] {RAW_FILE}")


if __name__ == "__main__":
    main()
