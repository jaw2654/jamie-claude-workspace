#!/usr/bin/env python3
"""
IG Posts Deep Fetcher
Visits each IG post URL with Playwright + cookies, extracts:
  caption, date, is_reel, likes/views if visible
Output: 工作文件/素材/ig-posts-deep-YYYY-MM-DD.json
"""
import argparse
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
OUTPUT_DIR = Path.home() / "Desktop" / "Claude cowork" / "工作文件" / "素材"


def load_ig_cookies():
    all_cookies = json.loads(COOKIES_PATH.read_text())
    ig = [c for c in all_cookies if "instagram.com" in c.get("domain", "")]
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
        exp = c.get("expirationDate")
        if exp is not None:
            try:
                fixed["expires"] = int(exp)
            except (TypeError, ValueError):
                pass
        out.append(fixed)
    return out


def extract_post(page, url):
    rec = {"url": url, "shortcode": None, "is_reel": "/reel/" in url, "caption": None,
           "date_iso": None, "likes": None, "views": None, "comments": None, "media_type": None,
           "author": None, "raw_snippet": None}
    m = re.search(r"/(reel|p)/([^/]+)/", url)
    if m:
        rec["shortcode"] = m.group(2)
    try:
        page.goto(url, wait_until="domcontentloaded", timeout=45_000)
    except Exception as e:
        rec["error"] = f"goto: {e}"
        return rec
    if "accounts/login" in page.url:
        rec["error"] = "login_required"
        return rec

    # Wait briefly for dynamic content
    try:
        page.wait_for_selector("article, main", timeout=10_000)
    except Exception:
        pass
    time.sleep(2)

    # 1) Try meta description (often contains likes/comments + caption for posts)
    try:
        meta_desc = page.locator('meta[name="description"]').get_attribute("content", timeout=3_000)
    except Exception:
        meta_desc = None
    try:
        og_desc = page.locator('meta[property="og:description"]').get_attribute("content", timeout=3_000)
    except Exception:
        og_desc = None
    try:
        og_title = page.locator('meta[property="og:title"]').get_attribute("content", timeout=3_000)
    except Exception:
        og_title = None

    rec["raw_snippet"] = {"meta_desc": meta_desc, "og_desc": og_desc, "og_title": og_title}

    # Parse likes/comments from meta description
    text_sources = " | ".join(x for x in [meta_desc, og_desc, og_title] if x)
    if text_sources:
        # Pattern: "123 likes, 4 comments" / "1,234 次讚" / "觀看"
        m_like = re.search(r"([\d,\.]+[KM萬]?)\s*(?:likes?|次讚|人說這讚|個讚)", text_sources, re.IGNORECASE)
        m_com = re.search(r"([\d,\.]+[KM萬]?)\s*(?:comments?|則留言|留言)", text_sources, re.IGNORECASE)
        m_view = re.search(r"([\d,\.]+[KM萬]?)\s*(?:views?|次觀看|觀看次數)", text_sources, re.IGNORECASE)
        if m_like:
            rec["likes"] = m_like.group(1)
        if m_com:
            rec["comments"] = m_com.group(1)
        if m_view:
            rec["views"] = m_view.group(1)

    # 2) Extract caption from meta desc (IG usually embeds the caption after a colon)
    # Format example: "Jamie Wu on October 15, 2025: "caption text""
    if meta_desc:
        m_cap = re.search(r':\s*"(.+?)"\s*$', meta_desc, re.DOTALL)
        if m_cap:
            rec["caption"] = m_cap.group(1).strip()
        m_date = re.search(r"(?:on\s+|在\s*)((?:January|February|March|April|May|June|July|August|September|October|November|December)\s+\d+,?\s+\d{4}|\d{4}年\d+月\d+日|\d{4}-\d{1,2}-\d{1,2})", meta_desc)
        if m_date:
            rec["date_iso"] = m_date.group(1)

    # 3) Fallback: read caption from page DOM
    if not rec["caption"]:
        try:
            # IG often puts caption in h1 or article > div > ul > li first
            caption_el = page.locator("article h1").first
            if caption_el.count() > 0:
                rec["caption"] = caption_el.inner_text(timeout=3_000)
        except Exception:
            pass

    # 4) time datetime
    try:
        t = page.locator("time").first.get_attribute("datetime", timeout=3_000)
        if t:
            rec["date_iso"] = t
    except Exception:
        pass

    # 5) media type detection
    try:
        has_video = page.locator("video").count() > 0
        has_carousel = page.locator('[aria-label*="carousel" i], [aria-label*="輪播" i], button[aria-label*="Next" i]').count() > 0
        if rec["is_reel"] or has_video:
            rec["media_type"] = "reel/video"
        elif has_carousel:
            rec["media_type"] = "carousel"
        else:
            rec["media_type"] = "image"
    except Exception:
        pass

    return rec


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--input", default=str(OUTPUT_DIR / "ig-insights-2026-04-15.json"))
    ap.add_argument("--out", default=str(OUTPUT_DIR / f"ig-posts-deep-{dt.date.today()}.json"))
    ap.add_argument("--limit", type=int, default=50)
    args = ap.parse_args()

    src = json.loads(Path(args.input).read_text())
    urls = [p["url"] for p in src.get("recent_posts", [])][: args.limit]
    print(f"[+] {len(urls)} URLs to fetch")

    cookies = load_ig_cookies()
    results = []

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        ctx = browser.new_context(
            user_agent="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.4 Safari/605.1.15",
            locale="zh-TW",
            viewport={"width": 1280, "height": 900},
        )
        ctx.add_cookies(cookies)
        page = ctx.new_page()

        # Also try to grab more posts from the profile page via scroll
        try:
            page.goto("https://www.instagram.com/jamie_wu_1012/", wait_until="domcontentloaded", timeout=30_000)
            time.sleep(3)
            # scroll
            for _ in range(6):
                page.mouse.wheel(0, 2000)
                time.sleep(1.5)
            post_hrefs = page.evaluate(
                """() => Array.from(document.querySelectorAll("a[href*='/p/'], a[href*='/reel/']"))
                         .map(a => a.getAttribute('href'))
                         .filter((v, i, a) => v && a.indexOf(v) === i)"""
            )
            discovered = []
            for h in post_hrefs:
                full = f"https://www.instagram.com{h}" if h.startswith("/") else h
                if "jamie_wu_1012" in full and full not in urls and full not in discovered:
                    discovered.append(full)
            print(f"[+] scroll discovered {len(discovered)} additional posts")
            urls = (urls + discovered)[: args.limit]
        except Exception as e:
            print(f"[!] profile scroll failed: {e}")

        print(f"[+] final urls: {len(urls)}")

        for i, u in enumerate(urls, 1):
            print(f"  [{i}/{len(urls)}] {u}")
            try:
                r = extract_post(page, u)
                results.append(r)
            except Exception as e:
                results.append({"url": u, "error": str(e)})
            time.sleep(1.5)

        browser.close()

    Path(args.out).write_text(json.dumps({
        "fetched_at": dt.datetime.now().isoformat(),
        "count": len(results),
        "posts": results,
    }, ensure_ascii=False, indent=2))
    print(f"[+] saved: {args.out}")


if __name__ == "__main__":
    main()
