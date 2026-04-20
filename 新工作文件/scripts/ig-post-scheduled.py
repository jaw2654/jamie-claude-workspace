#!/usr/bin/env python3
"""IG 排程自動發文 — 一次性（fires at scheduled time via launchd）.

2026-04-16 21:00 台灣時間發 v14 代謝迷思輪播。
完整流程在 project_ig_autopost_working_20260415.md + project_ig_first_post_live_20260415.md。

用法：
    python3 ig-post-scheduled.py <js_inject_path> <caption_path> [--collab USERNAME] [--expected-date YYYY-MM-DD]
"""
import datetime as dt
import subprocess
import sys
import time
import urllib.parse
import urllib.request
from pathlib import Path

LOG = Path.home() / "Library" / "Logs" / "repurre" / "ig-post-scheduled.log"
SECRETS = Path.home() / ".claude" / "secrets" / "telegram.env"


def log(msg):
    LOG.parent.mkdir(parents=True, exist_ok=True)
    with open(LOG, "a") as f:
        f.write(f"[{dt.datetime.now().isoformat()}] {msg}\n")
    print(msg, file=sys.stderr)


def telegram(text):
    s = {}
    if SECRETS.exists():
        for line in SECRETS.read_text().splitlines():
            if "=" in line and not line.strip().startswith("#"):
                k, v = line.split("=", 1)
                s[k.strip()] = v.strip()
    token = s.get("TELEGRAM_BOT_TOKEN")
    chat = s.get("TELEGRAM_CHAT_ID")
    if not (token and chat):
        return
    data = urllib.parse.urlencode({"chat_id": chat, "text": text}).encode()
    req = urllib.request.Request(
        f"https://api.telegram.org/bot{token}/sendMessage", data=data, method="POST")
    try:
        urllib.request.urlopen(req, timeout=10)
    except Exception as e:
        log(f"telegram err: {e}")


def jxa(js_code):
    """Run JXA-style JavaScript via osascript."""
    wrapped = f'Application("Google Chrome").windows[0].activeTab.execute({{javascript: `{js_code}`}})'
    r = subprocess.run(["osascript", "-l", "JavaScript"], input=wrapped, text=True, capture_output=True, timeout=30)
    return r.stdout.strip()


def osa(applescript):
    r = subprocess.run(["osascript"], input=applescript, text=True, capture_output=True, timeout=30)
    return r.stdout.strip()


def inject_jxa_from_file(path):
    """Execute pre-built JS file in active Chrome tab (handles large payload)."""
    apple = f'set jsText to read (POSIX file "{path}") as «class utf8»\ntell application "Google Chrome" to execute active tab of front window javascript jsText'
    return osa(apple)


def click_in_dom(selector_code):
    """selector_code returns an element variable 'el'."""
    js = f"""
    (function(){{
      {selector_code}
      if (!el) return 'not_found';
      const r = el.getBoundingClientRect();
      const x = r.left + r.width/2, y = r.top + r.height/2;
      ['pointerdown','mousedown','pointerup','mouseup','click'].forEach(t =>
        el.dispatchEvent(new MouseEvent(t,{{bubbles:true,cancelable:true,view:window,clientX:x,clientY:y,button:0}})));
      return 'clicked';
    }})();
    """
    return jxa(js)


def main():
    args = sys.argv[1:]
    if len(args) < 2:
        log("usage: ig-post-scheduled.py <js_inject> <caption_path> [--collab USER] [--expected-date DATE]")
        return 1

    js_inject = args[0]
    caption_path = args[1]
    collab = None
    expected_date = None
    i = 2
    while i < len(args):
        if args[i] == "--collab":
            collab = args[i + 1]; i += 2
        elif args[i] == "--expected-date":
            expected_date = args[i + 1]; i += 2
        else:
            i += 1

    if expected_date:
        today = dt.date.today().isoformat()
        if today != expected_date:
            log(f"date mismatch: today={today} expected={expected_date} — skipping")
            telegram(f"IG 排程跳過 (日期不對: {today} ≠ {expected_date})")
            return 0

    log(f"START ig post: js={js_inject} caption={caption_path} collab={collab}")
    telegram(f"IG 排程開始 · v14 代謝迷思輪播")

    # Step 1: navigate IG
    osa('tell application "Google Chrome"\nactivate\nset URL of active tab of front window to "https://www.instagram.com/"\nend tell')
    time.sleep(6)

    # Step 2: click 新貼文 SVG
    click_in_dom("""
      const svg = document.querySelector('svg[aria-label="新貼文"]');
      if (!svg) { var el = null; return; }
      var el = svg;
      for (let i=0;i<6;i++){ el = el.parentElement; if (!el) break; if (el.tagName==='A'||el.getAttribute('role')==='button') break; }
    """)
    time.sleep(2)

    # Step 3: click 貼文
    click_in_dom("""
      var el = [...document.querySelectorAll('a,div,span')].find(e => (e.innerText||'').trim() === '貼文');
    """)
    time.sleep(4)

    # Step 4: inject 7 files
    inject_jxa_from_file(js_inject)
    time.sleep(10)
    status = jxa('JSON.stringify({status:window.__igStatus,heading:(document.querySelector("[role=dialog] [role=heading]")||{}).innerText||""})')
    log(f"after inject: {status}")
    # v14 可為 7 或 8 張 (cover+7 or cover+6+CTA), 檢查 injected_ 開頭即可
    if "injected_" not in status:
        telegram(f"IG FAIL at inject: {status}")
        return 1

    # Step 5: 下一步 x 2 (crop → filter → caption)
    for step in ("crop", "filter"):
        click_in_dom("""
          var el = [...document.querySelectorAll('div[role=\"button\"],button')].find(e => (e.innerText||'').trim() === '下一步');
        """)
        time.sleep(3)
        log(f"advanced past {step}")

    # Step 6: paste caption
    caption_text = Path(caption_path).read_text()
    subprocess.run(["pbcopy"], input=caption_text.encode(), timeout=5)
    click_in_dom("""
      var el = document.querySelector('[contenteditable=true]');
      if (el) el.focus();
    """)
    time.sleep(1)
    osa("""
    tell application "Google Chrome" to activate
    delay 0.5
    tell application "System Events"
        tell process "Google Chrome" to set frontmost to true
        delay 0.3
        keystroke "v" using {command down}
    end tell
    """)
    time.sleep(3)
    clen = jxa('document.querySelector("[contenteditable=true]")?.innerText?.length || 0')
    log(f"caption pasted len={clen}")
    if int(clen or 0) < 100:
        telegram(f"IG FAIL caption only {clen} chars")
        return 1

    # Step 7: Add collaborator (best effort)
    if collab:
        click_in_dom(f"""
          var el = [...document.querySelectorAll('input[type=text]')].find(i => i.placeholder === '新增協作者');
          if (el) el.focus();
        """)
        time.sleep(0.8)
        osa(f"""
        tell application "System Events"
            tell process "Google Chrome" to set frontmost to true
            delay 0.3
            keystroke "{collab}"
        end tell
        """)
        time.sleep(4)
        # Click the result row (avoid 完成 text - target the first div[role=button] matching but NOT literal 完成)
        click_in_dom(f"""
          const rows = [...document.querySelectorAll('div[role=button]')].filter(e => {{
            const t = (e.innerText||'').trim();
            return t.startsWith('{collab}') && t.length < 60;
          }});
          var el = rows[0] || null;
        """)
        time.sleep(2)
        collab_status = jxa(f'document.body.innerText.includes("{collab}") ? "found" : "missing"')
        log(f"collab after click: {collab_status}")

    # Step 8: click 分享 (last one)
    click_in_dom("""
      const btns = [...document.querySelectorAll('div[role=\"button\"]')].filter(e => (e.innerText||'').trim() === '分享');
      var el = btns.length ? btns[btns.length-1] : null;
    """)
    time.sleep(28)

    # Verify
    heading = jxa('(document.querySelector("[role=dialog] [role=heading]")||{}).innerText || ""')
    log(f"final heading: {heading}")
    if "已分享" in heading or "已分享" in jxa('document.body.innerText'):
        telegram(f"IG 發文成功 ✓ v14 代謝迷思輪播 · 協作={collab or '(無)'}")
        return 0
    else:
        telegram(f"IG 可能失敗 · heading={heading[:60]}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
