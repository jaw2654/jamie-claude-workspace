#!/usr/bin/env python3
"""Regenerate ig-inject-v14.js from current v14-slides/slide-*.jpg files.

Reads all slide-NN.jpg in order, base64-encodes them, and writes the inject script
that IG upload flow injects to bypass CORS on file upload.
"""
import base64
from pathlib import Path

SLIDES_DIR = Path("/Users/user/Desktop/Claude cowork/工作文件/public/v14-slides")
OUT = Path("/Users/user/Desktop/Claude cowork/工作文件/scripts/ig-inject-v14.js")

jpgs = sorted(SLIDES_DIR.glob("slide-*.jpg"))
print(f"found {len(jpgs)} slides")

data_items = []
for p in jpgs:
    b64 = base64.b64encode(p.read_bytes()).decode("ascii")
    data_items.append({"n": p.name, "b": b64})

# build inject JS — base64 inline to bypass CORS on IG composer file input
import json
data_json = json.dumps(data_items, ensure_ascii=False)

js = """(function(){
  window.__igStatus='starting';
  try {
    const input = document.querySelector('input[type="file"]');
    if (!input) { window.__igStatus='no_input'; return; }
    const data = """ + data_json + """;
    const dt = new DataTransfer();
    for (const item of data) {
      const bin = atob(item.b);
      const arr = new Uint8Array(bin.length);
      for (let i=0;i<bin.length;i++) arr[i]=bin.charCodeAt(i);
      const f = new File([arr], item.n, {type:'image/jpeg'});
      dt.items.add(f);
    }
    input.files = dt.files;
    input.dispatchEvent(new Event('change', {bubbles:true}));
    window.__igStatus = 'injected_' + data.length;
  } catch(e) {
    window.__igStatus = 'error_' + e.message;
  }
})();
"""
OUT.write_text(js)
print(f"wrote {OUT} · {OUT.stat().st_size} bytes")
