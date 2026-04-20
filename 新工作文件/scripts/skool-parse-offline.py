#!/usr/bin/env python3
"""
離線解析 _skool-raw-dump.json
fix: skool 用 \xa0 (NBSP) 取代 space
"""
import datetime as dt
import json
import re
from pathlib import Path

OUT_FILE = Path.home() / "Desktop" / "Claude cowork" / "工作文件" / "素材" / "jamie-skool-weekend-letters.json"
RAW_FILE = Path.home() / "Desktop" / "Claude cowork" / "工作文件" / "素材" / "_skool-raw-dump.json"

POST_RE = re.compile(
    r'Wu chai Ing\s*\n(?P<age>[^\n]+?)\s*•\s*(?P<tag>[^\n]+)\n(?P<content>.*?)\nLike\s*\n',
    re.DOTALL
)


def parse_post(text):
    # normalize NBSP
    text = text.replace("\xa0", " ")
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
    raw = json.loads(RAW_FILE.read_text())
    jamie_posts = []
    for item in raw:
        bf = item.get("body_full") or ""
        if bf.startswith("__ERR__"):
            continue
        parsed = parse_post(bf)
        if parsed:
            parsed["url"] = item["url"]
            parsed["body_chars"] = len(parsed["body"])
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
        "notes": "Jamie 親筆 posts。週末信箱 = tag 含 '週末信箱'。其他 jamie posts 含「官方更新」「推薦」等。",
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
    print("\n--- Weekend letters (community feed) titles ---")
    for p in weekend_feed:
        print(f"  [{p['age_str']}] {p['title'][:60]} ({p['body_chars']}ch)")
    print("\n--- Other jamie posts ---")
    for p in other:
        print(f"  [{p['age_str']}] [{p['tag']}] {p['title'][:60]}")


if __name__ == "__main__":
    main()
