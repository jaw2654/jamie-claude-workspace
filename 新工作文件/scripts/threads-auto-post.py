#!/usr/bin/env python3
"""Threads auto-poster from JSON queue.

Reads /Users/user/Library/Mobile Documents/com~apple~CloudDocs/claude cowork/新工作文件/threads-queue/posts.json,
finds today's post (or date passed as argv), then:
  1) Tries headless Playwright auto-post via threads.com web UI
  2) On any failure, opens Chrome with intent/post composer URL pre-filled
  3) Sends Telegram confirmation either way

Usage:
    python3 threads-auto-post.py             # today
    python3 threads-auto-post.py 2026-04-15  # specific date
"""
import datetime as dt
import json
import subprocess
import sys
import urllib.parse
import urllib.request
from pathlib import Path

QUEUE = Path("/Users/user/Library/Mobile Documents/com~apple~CloudDocs/claude cowork/新工作文件/threads-queue/posts.json")
COOKIES = Path("/Users/user/.claude/secrets/social-cookies.json")
LOG = Path.home() / "Library" / "Logs" / "repurre" / "threads-post.log"
SECRETS = Path.home() / ".claude" / "secrets" / "telegram.env"


def log(msg):
    LOG.parent.mkdir(parents=True, exist_ok=True)
    with open(LOG, "a") as f:
        f.write(f"[{dt.datetime.now().isoformat()}] {msg}\n")
    print(msg, file=sys.stderr)


def load_secrets():
    out = {}
    if SECRETS.exists():
        for line in SECRETS.read_text().splitlines():
            if "=" in line and not line.strip().startswith("#"):
                k, v = line.split("=", 1)
                out[k.strip()] = v.strip()
    return out


def telegram(text):
    s = load_secrets()
    token = s.get("TELEGRAM_BOT_TOKEN")
    chat = s.get("TELEGRAM_CHAT_ID")
    if not (token and chat):
        log("missing telegram secrets")
        return
    data = urllib.parse.urlencode({"chat_id": chat, "text": text}).encode()
    req = urllib.request.Request(
        f"https://api.telegram.org/bot{token}/sendMessage",
        data=data, method="POST",
    )
    try:
        urllib.request.urlopen(req, timeout=10)
    except Exception as e:
        log(f"telegram send failed: {e}")


def find_post(date_str):
    posts = json.loads(QUEUE.read_text())
    for p in posts:
        if p.get("date") == date_str:
            return p
    return None


FORBIDDEN_WORDS = ["爆", "燃脂"]
FORBIDDEN_PATTERNS = [
    "21天變身", "14天變身", "30天變身",
    "21 天變身", "14 天變身", "30 天變身",
]


def check_forbidden(text):
    hits = [w for w in FORBIDDEN_WORDS if w in text]
    hits += [p for p in FORBIDDEN_PATTERNS if p in text]
    return hits


def load_threads_cookies():
    raw = json.loads(COOKIES.read_text())
    cookies = []
    for c in raw:
        d = c.get("domain", "")
        if not any(x in d for x in ("facebook.com", "instagram.com", "threads.com")):
            continue
        fixed = {
            "name": c["name"], "value": c["value"],
            "domain": d, "path": c.get("path", "/"),
            "secure": bool(c.get("secure", True)),
            "httpOnly": bool(c.get("httpOnly", False)),
            "sameSite": (c.get("sameSite") or "Lax").title()
                        if isinstance(c.get("sameSite"), str) else "Lax",
        }
        exp = c.get("expirationDate")
        if exp:
            try:
                fixed["expires"] = int(exp)
            except Exception:
                pass
        cookies.append(fixed)
    return cookies


def post_via_chrome_applescript(text):
    """Post via Chrome + JS injection（2026-04-15 最終版）.

    經實測驗證可行的流程：
      1. 開 Chrome 到 /intent/post?text=<urlencoded>（Threads SPA 會自動 fill composer）
      2. 等 8 秒讓 composer mount + 文字注入 React state
      3. 透過 Chrome 的 execute javascript 注入一段 JS：
         - 驗證 contenteditable 內有文字
         - 找到「發佈」按鈕（role=button + innerText=='發佈' 或 'Post'）
         - 檢查 aria-disabled/disabled 狀態
         - .click()
      4. 等 5 秒，用 JS 再讀一次 URL / 狀態確認發佈成功

    依賴：
      - Chrome → View → Developer → Allow JavaScript from Apple Events（已開）
      - 首次執行會跳 macOS Automation 授權（Chrome + osascript），點一次允許之後永久

    比舊版好在：不用模擬 keyboard，不怕 focus 錯、不怕 Cmd+Enter 被 SPA 擋。
    """
    import time, json as _json

    # Step 1: 開 Chrome 到 intent URL
    encoded = urllib.parse.quote(text)
    url = f"https://www.threads.com/intent/post?text={encoded}"
    try:
        subprocess.run(
            ["osascript"],
            input=f'tell application "Google Chrome"\nactivate\nopen location "{url}"\nend tell',
            text=True, check=True, timeout=15,
        )
        log("chrome opened intent URL")
    except Exception as e:
        return False, f"open_failed: {e}"

    # Step 2: 等 composer mount + auto-fill
    # 2026-04-20 patch: 8s 太短 button 沒 render · real-post 也改 12s（dry-run 也是 12s）
    time.sleep(12)

    # Step 3: JXA precheck — 驗證 composer 有文字 + 按鈕可點
    # 2026-04-20 patch: 鎖 dialog scope + 繁簡英 button text 都吃 + 原生 button tag 也找
    jxa_precheck = '''
    const chrome = Application("Google Chrome");
    const tab = chrome.windows[0].activeTab;
    const js = `
      (function(){
        const dialogs = [...document.querySelectorAll('[role="dialog"]')];
        const target = dialogs.find(d => {
          const ed = d.querySelector('[contenteditable="true"]');
          return ed && (ed.innerText||'').length >= 10;
        }) || document;
        const ed = target.querySelector('[contenteditable="true"]');
        const btns = [...target.querySelectorAll('[role="button"], button')];
        const pub = btns.find(b => {
          const t = (b.innerText||'').trim();
          return t === '發佈' || t === '發布' || t === 'Post' || t === 'Share';
        });
        return JSON.stringify({
          hasEditor: !!ed,
          editorLen: ed ? (ed.innerText||'').length : 0,
          hasButton: !!pub,
          btnDisabled: pub ? (pub.getAttribute('aria-disabled')||pub.getAttribute('disabled')||'no') : 'n/a',
          url: location.href.slice(0,80)
        });
      })();
    `;
    tab.execute({javascript: js});
    '''
    try:
        pre = subprocess.run(
            ["osascript", "-l", "JavaScript"],
            input=jxa_precheck, text=True, check=True, timeout=15, capture_output=True,
        ).stdout.strip()
        log(f"precheck={pre}")
        pre_data = _json.loads(pre)
        if not pre_data.get("hasEditor"):
            return False, "no_editor_found"
        if not pre_data.get("hasButton"):
            return False, "no_publish_button"
        if pre_data.get("editorLen", 0) < 10:
            return False, f"editor_too_short: len={pre_data.get('editorLen')}"
        if pre_data.get("btnDisabled") not in ("no", "false"):
            return False, f"button_disabled: {pre_data.get('btnDisabled')}"
    except Exception as e:
        return False, f"precheck_failed: {e}"

    # Step 4: JXA click 發佈
    # 關鍵修復（2026-04-15 實測）：
    # 1. Threads composer 頁面有兩個 [role="dialog"] 疊著：0 號有我們的文字、1 號空白。
    #    必須鎖定 editorLen >= 10 的那個 dialog，才不會點到空的。
    # 2. Meta 會擋純 .click()，必須 dispatch 完整 pointer event 序列
    #    (pointerdown → mousedown → pointerup → mouseup → click) 才模擬真人觸發。
    jxa_click = '''
    const chrome = Application("Google Chrome");
    const tab = chrome.windows[0].activeTab;
    const js = `
      (function(){
        const dialogs = [...document.querySelectorAll('[role="dialog"]')];
        const target = dialogs.find(d => {
          const ed = d.querySelector('[contenteditable="true"]');
          return ed && (ed.innerText||'').length >= 10;
        });
        if (!target) return 'no_target_dialog';
        const btns = [...target.querySelectorAll('[role="button"], button')];
        const pub = btns.find(b => {
          const t = (b.innerText||'').trim();
          return t === '發佈' || t === '發布' || t === 'Post' || t === 'Share';
        });
        if (!pub) return 'no_button';
        const rect = pub.getBoundingClientRect();
        const x = rect.left + rect.width/2;
        const y = rect.top + rect.height/2;
        ['pointerdown','mousedown','pointerup','mouseup','click'].forEach(type => {
          pub.dispatchEvent(new MouseEvent(type, {bubbles:true, cancelable:true, view:window, clientX:x, clientY:y, button:0}));
        });
        return 'clicked_pointer';
      })();
    `;
    tab.execute({javascript: js});
    '''
    try:
        click_result = subprocess.run(
            ["osascript", "-l", "JavaScript"],
            input=jxa_click, text=True, check=True, timeout=10, capture_output=True,
        ).stdout.strip()
        log(f"click result={click_result}")
    except Exception as e:
        return False, f"click_failed: {e}"

    # Step 5: 等發佈完成 + 驗證 URL 已跳離 intent/post
    time.sleep(6)
    try:
        result = subprocess.run(
            ["osascript"],
            input='tell application "Google Chrome" to return URL of active tab of front window',
            text=True, check=True, timeout=5, capture_output=True,
        )
        final_url = result.stdout.strip()
        log(f"final_url={final_url[:120]}")
    except Exception as e:
        return False, f"final_check_failed: {e}"

    if "intent/post" in final_url:
        return False, f"still_on_composer_after_click: {final_url[:80]}"

    return True, f"posted (url={final_url[:60]})"


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    flags = [a for a in sys.argv[1:] if a.startswith("--")]
    dry = "--dry" in flags
    date_str = args[0] if args else dt.date.today().isoformat()
    post = find_post(date_str)
    if not post:
        log(f"no post queued for {date_str}")
        return 0

    log(f"target: {date_str} | {post['title']}{' [DRY]' if dry else ''}")
    text = post["text"]

    force = "--force" in flags
    hits = check_forbidden(text)
    if hits and not force:
        log(f"ABORT forbidden words: {hits}")
        telegram(
            f"Threads {date_str}「{post['title']}」已擋下：文案含禁用詞 {', '.join(hits)}。\n"
            f"修 queue 檔再跑，或加 --force 強制發。\n\n{text}"
        )
        return 1
    if hits and force:
        log(f"force-post with forbidden words: {hits}")
    if dry:
        # Dry mode: 只做 step 1-3 precheck，不 click 發佈
        import time, json as _json, subprocess as _sp
        encoded = urllib.parse.quote(text)
        url = f"https://www.threads.com/intent/post?text={encoded}"
        _sp.run(["osascript"], input=f'tell application "Google Chrome"\nactivate\nopen location "{url}"\nend tell', text=True, check=True, timeout=15)
        log("chrome opened (dry)")
        time.sleep(12)
        # 用 JXA (JavaScript for Automation) 走 osascript -l JavaScript，避免雙重 escaping
        # 2026-04-20 patch: 鎖定 composer dialog + 支援「發佈/發布/Post/Share」四種 button 文字
        jxa = '''
        const chrome = Application("Google Chrome");
        const tab = chrome.windows[0].activeTab;
        const js = `
          (function(){
            const dialogs = [...document.querySelectorAll('[role="dialog"]')];
            const target = dialogs.find(d => {
              const ed = d.querySelector('[contenteditable="true"]');
              return ed && (ed.innerText||'').length >= 10;
            }) || document;
            const ed = target.querySelector('[contenteditable="true"]');
            const btns = [...target.querySelectorAll('[role="button"], button')];
            const pub = btns.find(b => {
              const t = (b.innerText||'').trim();
              return t === '發佈' || t === '發布' || t === 'Post' || t === 'Share';
            });
            return JSON.stringify({
              hasEditor: !!ed,
              editorLen: ed ? (ed.innerText||'').length : 0,
              editorHead: ed ? (ed.innerText||'').slice(0,50) : '',
              hasButton: !!pub,
              btnText: pub ? (pub.innerText||'').trim() : 'n/a',
              btnDisabled: pub ? (pub.getAttribute('aria-disabled')||pub.getAttribute('disabled')||'no') : 'n/a',
              dialogCount: dialogs.length,
              allBtnTexts: btns.slice(0,15).map(b=>(b.innerText||'').trim()).filter(Boolean)
            });
          })();
        `;
        tab.execute({javascript: js});
        '''
        pre = _sp.run(
            ["osascript", "-l", "JavaScript"],
            input=jxa, text=True, check=True, timeout=15, capture_output=True,
        ).stdout.strip()
        log(f"DRY precheck={pre}")
        print(pre)
        # 清掉 composer 避免誤送
        _sp.run(
            ["osascript"],
            input='tell application "Google Chrome" to set URL of active tab of front window to "about:blank"',
            text=True, timeout=5,
        )
        return 0
    success, status = post_via_chrome_applescript(text)

    if success:
        log(f"OK auto-posted: {status}")
        telegram(f"Threads 已自動發 {date_str} {post['title']}\n\n{text}")
    else:
        log(f"auto-post failed ({status}), Chrome 應已開撰寫頁 等你手動發")
        telegram(
            f"Threads 自動發失敗 ({status}) {date_str} {post['title']}\n\n"
            f"Chrome 撰寫頁應已開 文字預填 你按發佈即可\n\n{text}"
        )
    return 0


if __name__ == "__main__":
    sys.exit(main())
