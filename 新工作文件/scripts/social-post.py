#!/usr/bin/env python3
"""Social media posting via Playwright browser automation.
Uses Chrome cookies for authentication.
"""
import asyncio
import json
import sys
import os

async def load_cookies(context, platform):
    """Load cookies for a specific platform into browser context."""
    with open('/Users/user/.claude/secrets/social-cookies.json', 'r') as f:
        all_cookies = json.load(f)

    domain_map = {
        'instagram': '.instagram.com',
        'threads': '.facebook.com',  # threads uses FB auth
        'youtube': '.youtube.com',
        'facebook': '.facebook.com'
    }

    domain = domain_map.get(platform, '')
    # Also load google cookies for YouTube
    if platform == 'youtube':
        cookies = [c for c in all_cookies if '.youtube.com' in c['domain'] or '.google.com' in c['domain']]
    elif platform == 'threads':
        cookies = [c for c in all_cookies if '.facebook.com' in c['domain'] or '.instagram.com' in c['domain']]
    else:
        cookies = [c for c in all_cookies if domain in c['domain']]

    for c in cookies:
        try:
            cookie = {
                'name': c['name'],
                'value': c['value'],
                'domain': c['domain'],
                'path': c.get('path', '/'),
            }
            await context.add_cookies([cookie])
        except:
            pass

    return len(cookies)

async def post_threads(text):
    """Post to Threads."""
    from playwright.async_api import async_playwright

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        context = await browser.new_context()
        n = await load_cookies(context, 'threads')
        print(f"Loaded {n} cookies for Threads")

        page = await context.new_page()
        await page.goto('https://www.threads.net')
        await page.wait_for_timeout(3000)

        # Click new post button
        await page.click('[aria-label="建立"]', timeout=5000)
        await page.wait_for_timeout(1000)

        # Type the post
        await page.keyboard.type(text)
        await page.wait_for_timeout(500)

        # Click post button
        await page.click('text=發佈', timeout=5000)
        await page.wait_for_timeout(3000)

        print("Threads post sent!")
        await browser.close()

async def post_instagram(image_path, caption):
    """Post image to Instagram."""
    from playwright.async_api import async_playwright

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        context = await browser.new_context(
            viewport={'width': 390, 'height': 844},
            user_agent='Mozilla/5.0 (iPhone; CPU iPhone OS 16_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.0 Mobile/15E148 Safari/604.1'
        )
        n = await load_cookies(context, 'instagram')
        print(f"Loaded {n} cookies for Instagram")

        page = await context.new_page()
        await page.goto('https://www.instagram.com')
        await page.wait_for_timeout(3000)

        print("Instagram page loaded. Manual interaction may be needed.")
        await page.wait_for_timeout(60000)  # Wait for manual interaction

        await browser.close()

if __name__ == '__main__':
    if len(sys.argv) < 3:
        print("Usage:")
        print("  python3 social-post.py threads 'your post text'")
        print("  python3 social-post.py instagram /path/to/image.jpg 'caption'")
        sys.exit(1)

    platform = sys.argv[1]

    if platform == 'threads':
        asyncio.run(post_threads(sys.argv[2]))
    elif platform == 'instagram':
        asyncio.run(post_instagram(sys.argv[2], sys.argv[3] if len(sys.argv) > 3 else ''))
    else:
        print(f"Unknown platform: {platform}")
