# morning-briefing Skill 規範（2026-04-13 更新版）
# ⚠️ 此為正確格式，每次做晨報必須以此為準
# ⚠️ 不可更改 Tab 結構，不可新增或刪除 Tab

## 基本資訊

- **使用者**：Jamie Wu（巫采縈），repurre Health Studio 教練
- **行事曆**：calendarId = `repurre2022@gmail.com`
- **工作信箱**：jaw2654@gmail.com
- **輸出路徑**：`工作文件/每日簡報/morning-briefing-YYYY-MM-DD.html`
- **Telegram Token**：`8754872172:AAFSRJuneA12RZAbyfn38h3XDEk5uN9MPQk`
- **Telegram Chat ID**：`8708811744`

---

## 最重要原則

- ❌ 禁止捏造新聞、數據、URL
- ❌ 禁止修改 Tab 結構（固定 6 個 Tab，不可增減）
- ❌ 禁止發 Email（改為 Telegram sendDocument）
- ✅ 所有新聞必須附真實出處 URL
- ✅ 搜不到就寫「今日無相關新聞」
- ✅ Gmail 無未讀就寫「目前收件匣無未讀重要信件」

---

## HTML 設計規範（固定不變）

```
body background:       #0a0a0a
card/container:        #141414
border:                #1e1e1e / #222
text primary:          #e0e0e0 / #ffffff
text secondary:        #888 / #aaa
accent (active tab):   #ffffff
Tab 機制：CSS radio button（不用 JavaScript）
手機適配：必須包含 @media max-width: 600px
```

---

## 固定 6 個 Tab（此結構鎖死，不可更改）

| # | Tab Label | 內容 |
|---|-----------|------|
| 1 | ☑️ 每日流程 | Google Calendar 今日行程 + Daily Checklist（11 項 checkbox）|
| 2 | 📧 Gmail | 讀取真實收件匣未讀信件；無則顯示「目前收件匣無未讀重要信件」|
| 3 | 🌍 世界大事 | 美股行情（道瓊/S&P/NASDAQ）+ 國際新聞 3–5 則（必附真實 URL）|
| 4 | 💪 全球健身話題 | 全球健身趨勢 2–3 則 + 台灣競品觀察 1–2 則（附 URL）|
| 5 | 📱 K-pop 運動飲食保養 | K-pop 藝人訓練法 + 韓星飲食策略 + 韓國保養時尚（附 URL）|
| 6 | 🎬 影片內容建議 | 長影片 YouTube（HOOK+承接鋪合 4 段）+ 短影片 Reels（HOOK+承接鋪合 3 段）|

---

## Tab 1 Checklist（固定 11 項）

1. 起床・喝水 500ml（06:30）
2. 閱讀晨報・確認今日行程（07:00）
3. 自主訓練（07:30）
4. 準備課程內容・場地整理（08:30）
5. 上午課程（根據行事曆填入時間）
6. 午餐・休息
7. 內容創作時間（拍攝/剪輯/企劃）（15:00）
8. IG 貼文/限動更新（17:00）
9. 晚間課程（根據行事曆填入時間）
10. 回覆訊息・明日備課（21:00）
11. 放鬆・睡前閱讀（22:30）

---

## Tab 6 影片內容建議格式（固定結構）

### 長影片 YouTube
```
video-type: 📺 長影片 YOUTUBE
video-title: 【具體標題，含反差感或學習點】
hook-box:
  hook-label: 🎣 HOOK（開頭 5 秒）
  hook-text: 「30 字以內開場台詞，帶出好奇心或反差感」
flow-items（4 段）:
  A 開場: 建立衝擊感（vlog 畫面/反差數據/個人經歷）
  B 核心內容: 具體比較或教學，2–3 個例子
  C 科學解析: 教練角度破解迷思或專業觀點
  D 帶走訊息+CTA: 1–3 個可執行重點 + 明確 CTA
```

### 短影片 Reels / Shorts
```
video-type: ⚡ 短影片 REELS / SHORTS
video-title: 【直接衝擊，15 字內】
hook-box:
  hook-label: 🎣 HOOK（開頭 3 秒）
  hook-text: 「15 字以內直接破題台詞」
flow-items（3 段）:
  1 揭曉: 快速說明是什麼（10–15 秒）
  2 展示: 快節奏 2–3 場景（各 3–5 秒）
  3 結論+CTA: 一句帶走 + 留言互動
```

---

## 資料收集（並行執行）

1. `gcal_list_events`（repurre2022@gmail.com，今日）
2. WebSearch：美股昨日收盤
3. WebSearch：世界新聞 today YYYY-MM-DD
4. WebSearch：全球健身趨勢 + 台灣競品
5. WebSearch（3 個）：K-pop 運動 / K-pop 飲食 / 韓國保養時尚
6. `gmail_search_messages`（jaw2654@gmail.com，`in:inbox is:unread newer_than:3d`）

---

## 輸出流程

### A. 存檔
```
工作文件/每日簡報/morning-briefing-YYYY-MM-DD.html
```

### B. Telegram sendDocument
```bash
ACTUAL_DATE="YYYY-MM-DD"
curl -s -X POST \
  "https://api.telegram.org/bot8754872172:AAFSRJuneA12RZAbyfn38h3XDEk5uN9MPQk/sendDocument" \
  -F "chat_id=8708811744" \
  -F "document=@/Users/user/Desktop/Claude cowork/工作文件/每日簡報/morning-briefing-${ACTUAL_DATE}.html" \
  -F "caption=☀️ repurre 晨報 ${ACTUAL_DATE}"
```

如失敗，改傳文字摘要 fallback。

---

## 問題處理

| 情況 | 處理方式 |
|------|----------|
| 市場休市 | 標記「休市」，顯示最近交易日數據 |
| 新聞找不到 | 寫「今日無相關新聞」，不捏造 |
| Gmail 無未讀 | 顯示「目前收件匣無未讀重要信件」|
| Telegram 失敗 | 改傳文字摘要 |
