#!/usr/bin/env python3
"""Webapp Testing helper — Playwright 真瀏覽器驗最新貼文

Usage:
    verify-post.py threads @jamie_wu_1012 "肩頸越動越痠"
    verify-post.py ig @jamie_wu_1012 "代償歸零"
    verify-post.py xhs <xhs_user_handle> "<keyword>"
"""
import asyncio
import sys
import time
import os
import browser_cookie3
from playwright.async_api import async_playwright


PLATFORM_CONFIG = {
    "threads": {
        "cookie_domain": ".threads.com",
        "url_template": "https://www.threads.com/{handle}",
        "article_selector": "div[data-pressable-container='true'], div[role='article'], article, a[href*='/post/']",
    },
    "ig": {
        "cookie_domain": ".instagram.com",
        "url_template": "https://www.instagram.com/{handle_clean}/",
        "article_selector": "article",
    },
    "xhs": {
        "cookie_domain": ".xiaohongshu.com",
        "url_template": "https://www.xiaohongshu.com/user/profile/{handle_clean}",
        "article_selector": "section.note-item, div.note-item, a.cover",
    },
}


def load_cookies(domain):
    jar = browser_cookie3.chrome(domain_name=domain)
    cookies = []
    for c in jar:
        cookies.append({
            "name": c.name,
            "value": c.value,
            "domain": c.domain,
            "path": c.path or "/",
            "expires": int(c.expires) if c.expires else -1,
            "httpOnly": bool(getattr(c, "_rest", {}).get("HttpOnly", False)) if hasattr(c, "_rest") else False,
            "secure": bool(c.secure),
            "sameSite": "Lax",
        })
    return cookies


async def verify(platform, handle, keyword):
    cfg = PLATFORM_CONFIG.get(platform)
    if not cfg:
        return {"ok": False, "reason": f"unknown_platform: {platform}"}

    handle_clean = handle.lstrip("@")
    url = cfg["url_template"].format(handle=handle, handle_clean=handle_clean)

    try:
        cookies = load_cookies(cfg["cookie_domain"])
    except Exception as e:
        return {"ok": False, "reason": f"cookie_load_failed: {e}"}

    async with async_playwright() as p:
        b = await p.chromium.launch(headless=True)
        ctx = await b.new_context(
            user_agent="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Safari/605.1.15",
        )
        await ctx.add_cookies(cookies)
        pg = await ctx.new_page()
        try:
            await pg.goto(url, wait_until="networkidle", timeout=30000)
        except Exception as e:
            await b.close()
            return {"ok": False, "reason": f"goto_failed: {e}", "url": url}

        await pg.wait_for_timeout(5000)

        try:
            articles = await pg.evaluate(
                "(sel) => [...document.querySelectorAll(sel)].slice(0, 3).map(e => (e.innerText || '').slice(0, 500))",
                cfg["article_selector"],
            )
        except Exception as e:
            await b.close()
            return {"ok": False, "reason": f"dom_read_failed: {e}", "url": url}

        # Screenshot for failure analysis
        ts = int(time.time())
        screenshot_path = f"/tmp/webapp-verify-{platform}-{ts}.png"
        try:
            await pg.screenshot(path=screenshot_path, full_page=False)
        except Exception:
            screenshot_path = None

        await b.close()

        if not articles:
            return {"ok": False, "reason": "no_articles_found", "url": url, "screenshot": screenshot_path}

        latest = articles[0] or ""
        if keyword in latest:
            return {"ok": True, "url": url, "latest_head": latest[:80], "screenshot": None}
        else:
            return {
                "ok": False,
                "reason": "keyword_not_in_latest",
                "url": url,
                "latest_head": latest[:200],
                "screenshot": screenshot_path,
            }


def main():
    if len(sys.argv) < 4:
        print("usage: verify-post.py <platform> <handle> <keyword>", file=sys.stderr)
        sys.exit(2)
    platform, handle, keyword = sys.argv[1], sys.argv[2], sys.argv[3]
    result = asyncio.run(verify(platform, handle, keyword))
    import json
    print(json.dumps(result, ensure_ascii=False))
    sys.exit(0 if result.get("ok") else 1)


if __name__ == "__main__":
    main()
