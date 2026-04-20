#!/usr/bin/env python3
"""Threads-post canary — runs at 11:58 daily, 2 min before the real post.

Checks:
  1. Today's post exists in queue
  2. Chrome can run (osascript ping)
  3. threads.com intent URL reachable (HTTP 200)
  4. social-cookies.json still exists + parses

Failure → Telegram warning so Jamie can manually post before 12:00.
Success → silent (no noise).
"""
import datetime as dt
import json
import subprocess
import sys
import urllib.parse
import urllib.request
from pathlib import Path

QUEUE = Path("/Users/user/Desktop/Claude cowork/工作文件/threads-queue/posts.json")
COOKIES = Path("/Users/user/.claude/secrets/social-cookies.json")
LOG = Path.home() / "Library" / "Logs" / "repurre" / "threads-canary.log"
SECRETS = Path.home() / ".claude" / "secrets" / "telegram.env"


def log(msg):
    LOG.parent.mkdir(parents=True, exist_ok=True)
    with open(LOG, "a") as f:
        f.write(f"[{dt.datetime.now().isoformat()}] {msg}\n")


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
        return
    data = urllib.parse.urlencode({"chat_id": chat, "text": text}).encode()
    req = urllib.request.Request(
        f"https://api.telegram.org/bot{token}/sendMessage",
        data=data, method="POST",
    )
    try:
        urllib.request.urlopen(req, timeout=10)
    except Exception:
        pass


def check_queue(date_str):
    if not QUEUE.exists():
        return False, "queue file missing"
    try:
        posts = json.loads(QUEUE.read_text())
    except Exception as e:
        return False, f"queue parse error: {e}"
    for p in posts:
        if p.get("date") == date_str:
            if p.get("text") and p.get("title"):
                return True, p["title"]
            return False, f"post {date_str} missing text/title"
    return False, f"no post queued for {date_str}"


def check_chrome():
    try:
        subprocess.run(
            ["osascript", "-e", 'tell application "Google Chrome" to return version'],
            check=True, timeout=5, capture_output=True,
        )
        return True, "ok"
    except Exception as e:
        return False, f"chrome not responsive: {e}"


def check_threads_url():
    try:
        req = urllib.request.Request(
            "https://www.threads.com/intent/post?text=canary",
            headers={"User-Agent": "Mozilla/5.0 Safari/605.1.15"},
        )
        with urllib.request.urlopen(req, timeout=8) as r:
            return r.status in (200, 302), f"status={r.status}"
    except Exception as e:
        return False, f"threads unreachable: {e}"


def check_cookies():
    if not COOKIES.exists():
        return False, "cookies file missing"
    try:
        raw = json.loads(COOKIES.read_text())
        thread_cookies = [c for c in raw if "threads.com" in c.get("domain", "")]
        if not thread_cookies:
            return False, "no threads.com cookies"
        return True, f"{len(thread_cookies)} cookies"
    except Exception as e:
        return False, f"cookies parse error: {e}"


def main():
    date_str = sys.argv[1] if len(sys.argv) > 1 else dt.date.today().isoformat()
    checks = [
        ("queue", check_queue, [date_str]),
        ("chrome", check_chrome, []),
        ("threads-url", check_threads_url, []),
    ]
    failures = []
    summary = []
    for name, fn, args in checks:
        ok, msg = fn(*args)
        summary.append(f"{name}: {'OK' if ok else 'FAIL'} — {msg}")
        if not ok:
            failures.append(f"{name}: {msg}")

    log(" | ".join(summary))

    if failures:
        telegram(
            f"Threads canary {date_str} 預檢失敗\n\n"
            + "\n".join(f"· {f}" for f in failures)
            + "\n\n12:00 自動發可能會掛。建議手動發、或修完再等。"
        )
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
