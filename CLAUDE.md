# repurre Health Studio — Claude 工作記憶

## 🔔 2026-04-19 夜 關鍵變更（必讀 · memory 已深度存）

- **工作路徑 iCloud**：真實 cwd 在 `~/Library/Mobile Documents/com~apple~CloudDocs/claude cowork/`（小寫 claude）· Desktop 是 alias · 失效時 `ln -sf` 重建（見 memory `reference_icloud_workdir_path`）
- **週節奏 v3（04/27 起）**：一 YT 長片 / 二四日 YT Shorts+IG Reels / 三六 輪播 / 五休息 / 每天 12:00 Threads（取代舊週節奏 · 見 memory `project_weekly_cadence_v3_20260427`）
- **BSuite Reel 2 鐵律**：時間必 21:00 準 · Cover 上傳時就放（見 2 份 feedback memory）
- **瘦身 keyword**：Jamie 打「瘦身」= 清 cowork 資料夾 · 不刪只搬 `_archive/` · 清單先批准
- **CTA 全改 assessment**：`repurre-reports.pages.dev/assessment`（舊 LIFE/肩頸/1 分鐘快測/免費 全棄）
- **交易相關全停**：04/16 Jamie 指示 · pre/postmarket skill disabled · 交易日誌不再更新
- **晚報 23:00 自動**：evening-review launchd 每晚跑（不要 disable）
- **tagline**：人生下半場 · 健康過一生
- **schedule 頁面最新**：`repurre-reports.pages.dev/schedule-20260417-20260426`

**完整 handoff**：memory `project_session_20260419_night_handoff`
**MEMORY.md 索引**：每 session 必讀 📌 背景段

---

> ⚠️ **每次開新 Session 必做兩件事（最優先）：**
> 1. 讀取此檔案：`~/Desktop/Claude cowork/CLAUDE.md`（這份）
> 2. 所有資料調閱已永久授權，直接抓取不需要問 Jamie（IG/YT/行事曆/Gmail）
>
> ✅ **5 個排程已改用 macOS launchd 永久化（2026-04-14）**：
> - 不再受 Claude session 生死影響，Mac 只要是開著就會跑
> - plist 檔位於 `~/Library/LaunchAgents/com.repurre.*.plist`
> - wrapper 腳本：`~/.claude/scripts/repurre-run.sh`
> - 日誌：`~/Library/Logs/repurre/`
> - 管理指令：`launchctl list | grep repurre`（列出）/ `launchctl unload ~/Library/LaunchAgents/com.repurre.xxx.plist`（停用）
> - 手動觸發：`launchctl start com.repurre.morning-briefing`

---

## 使用者資訊

| 欄位 | 內容 |
|------|------|
| 姓名 | Jamie Wu（巫采縈）|
| 性別 | 女性 |
| 居住地 | 台北 |
| 身份 | repurre Studio 創辦人兼主教練（13坪私人工作室，12 年教學經驗）|
| 創作者 | YouTube @jamie_wu_1012 + IG @jamie_wu_1012 |
| 線上社群 | MOVE ON CREW（Skool 線上陪跑系統）|
| 工作 Email | jaw2654@gmail.com |
| 行事曆 | repurre2022@gmail.com（Google Calendar）|

### 個人背景
- 跆拳道 12 年（6-18 歲）→ 健身教練 12 年 → 創業 repurre
- 跆拳道黑帶三段、曾獲全國中等學校運動會第二名、全國運動會第四名、世錦賽國手選拔第四名
- 曾因過度減肥導致甲狀腺亢進（對發炎反應敏感）
- 2025 外派紐約擔任跆拳道教練
- 興趣：跆拳道、跳舞、網球、騎馬、跑步
- 不喝酒，愛甜點，正在學韓文
- 養貓：波米（Bomi）

---

## 🆕 2026-04-14 晚間重大更新（必讀）

### 📝 新體驗課 Google 表單（代替舊版 3 題表單）
- 填寫網址：https://docs.google.com/forms/d/e/1FAIpQLSdtEPcyinNocJmFpAzgzu2WTyd9o-IN71xyKLatlYEPQ5lH1g/viewform
- 編輯網址：https://docs.google.com/forms/d/1-kr5Jq3TaevBLzwQjLKfrXqrDbEH2VXgaAeqzzL8mTc/edit
- 回應試算表：https://docs.google.com/spreadsheets/d/1rqExRCzzTvPJZdbmTd7U7mmHqpZtIa8W3g-X4oEHxkM/edit
- 內容：19 題 / 6 區塊 / 篩 TA 設計（「為什麼是現在」「1 年後的自己」「每週願意固定嗎」）
- 更新腳本：`~/Desktop/Claude cowork/新工作文件/update_form.gs`（Apps Script 改 + 重跑）

### 🌐 Cloudflare Pages 新上線頁面
- **師資介紹**：https://repurre-reports.pages.dev/trainer-jamie
- **課程價目**：https://repurre-reports.pages.dev/pricing
- 源檔：`新工作文件/public/trainer-jamie.html` + `pricing.html`
- 圖片：`新工作文件/public/jamie-photo.jpg`
- 設計：米白 `#faf7f2` + 黑 + 米色 `#ede7d9` + Noto Serif TC（Quiet Luxury / 精品感）

### 💰 2026 正式價目（已同步頁面 + Canva）
| 類型 | 10 堂 | 20 堂 |
|------|------|------|
| 1 對 1 | $2,400/堂（總 $24,000）| $2,200/堂（總 $44,000）|
| 1 對 2 | $3,000/堂（總 $30,000）| $2,800/堂（總 $56,000）|
| 60 分體態深度評估（單次） | 1v1 $2,200 / 1v2 $2,800 | — |

### 🏦 匯款資訊
- 永豐銀行（807）
- 戶名：repurre studio
- 帳號：19901800449897

### 📍 地址呈現規則（隱私保護）
- 公開展示：僅「台北市大安區忠孝東路四段 233 號」
- 完整樓層 **6F-6** 只在學員預約確認後私下告知

### 📱 LINE OA（已串 Messaging API）
- Channel ID: 2009801214
- Access Token 存於 `~/.claude/secrets/line.env`（權限 600）
- 官方帳號：@repurre / displayName: repurre
- 自動回覆文案（小編身份，非 Jamie 本人）已提供 Jamie 貼到 OA Manager

### 🎨 Statusline（2026-04-14 新）
- 腳本：`~/.claude/statusline-command.sh`
- 樣式：🐱🏋️ 模型名（粗體） context 進度條（綠→黃→橘→紅）% ｜ 5H% ｜ 1W%
- 第 2 行：Git 分支* +adds/-dels Session 名稱

### 🛠 新安裝工具（2026-04-14）
- **mlx-whisper + imageio-ffmpeg**（arm64 ffmpeg 靜態）→ 影片/音訊轉譯
- **yt-dlp** → YouTube 下載
- Skill：`/transcribe`（轉譯影片/音訊為逐字稿）

### 📱 IG Bio 定稿版（2026-04-14 深夜）
```
巫采縈 Jamie
repurre Studio 創辦人 · 12 年私教

運動不是任務，是 lifestyle 🤍
陪你把訓練練成日常
不講減脂・不做折扣・不走速成

台北大安 · 1v1 / 1v2 精品私訓
👇 預約・課程・合作折扣
```
IG bio 連結：https://repurre-reports.pages.dev/links

### 💬 LINE OA 自動回覆 + GoSky IG DM（已設計文案，Jamie 貼上）

**通用自動回覆**：
```
嗨嗨！我是 repurre 小編 🤍
你的訊息已經收到囉～教練會盡快回覆你！
如果你想約體驗課，回「體驗」兩個字，我馬上幫你傳表單 👇
```

**關鍵字「體驗/預約/課程」觸發 + GoSky Reels 留言 DM**：
```
嗨嗨！我是 repurre 小編 🤍
謝謝你對 Jamie 的內容有感覺！

想先慢慢認識？
🎬 Jamie 的 vlog（生活 × 訓練）
https://youtube.com/@jamie_wu_1012

🔗 完整介紹頁面（教練 / 課程 / 品牌折扣）
https://repurre-reports.pages.dev/links

已經準備好行動？直接預約 👇
📝 60 分鐘身體深度評估（$2,200）
https://docs.google.com/forms/d/e/1FAIpQLSdtEPcyinNocJmFpAzgzu2WTyd9o-IN71xyKLatlYEPQ5lH1g/viewform

有任何問題歡迎直接回我～
```

### 🚫 品牌鐵律（新增，2026-04-14）
- ❌ 禁止折扣活動（折扣學生留存率近 0%）
- ❌ 禁止主動追休眠 VIP（錯的 TA）
- ❌ 禁止追 0 轉換免費諮詢名單
- ❌ 禁止內容攻擊其他教練（「80% 教練教錯」這種不用）
- ❌ 禁止對外出現「減脂」「21 天」「速成」「瘦」字眼
- ✅ TA 篩選器 =「把運動當人生重要事」的人
- ✅ 用「陪、走、長、練」，不用「瘦、快、爆、速」

---

### 品牌定位（2026-04-14 重新梳理）

**核心信念（Jamie 原話）**
- 「健康是需要花到年以上的時間的」
- 「好好練 5 年、10 年，就是一輩子的人」
- 「不要追求速成，只在意自己有沒有做到好的動作」
- 「真實的、持續的，跟我一起走下去」
- 「不是為了減肥而健身，是為了設計下半生的系統」

**Jamie 真實 vibe**
- 超高自律 × 工作狂
- 「我不愛健身但做，因為重要」— 品牌姿態
- 紀律派、長期陪伴派、不走表演式
- 三身份：健身教練 + 美股交易員（不公開）+ 韓文 6 年（真懂韓國）

**護城河（最獨特賣點）**
- 「我跟其他教練最不一樣的地方是，很在意學生的情緒跟心態」
- 情緒 + 心態決定訓練課表調整
- 80% 教練沒做的事

**TA 理想輪廓**
- 32-43 歲（不是年齡篩選、是心態篩選）
- 核心：**有餘裕 × 有品味 × 尊重專業**（缺一不可）
- 已婚/穩定伴侶、老闆/主管/自由工作者
- 台北、買精品、常出國、養寵物
- 會打扮、穿好衣服、化妝
- 真健康意識、願意執行、不請假
- 不是「想瘦」，是「想活好」

**語氣規範**
- 陪伴式、像朋友聊天、短句優先（每句≤20 字）
- 用「你」不用「大家」
- 用「陪、走、長、練」，不用「瘦、快、爆、速」
- 講學員故事（9 年那種）> 講數字
- 承認困難（「我也不愛但做」）> 激勵口號

**視覺 / 美學**
- 穿搭 + 氣質 + 空間感，不靠露肉
- 時尚表現 > 身材表現
- 工作室質感 > 教練身材秀

**不想成為的樣子**
- 瘋狂露身材的教練 / 健身內容
- 懶惰、口是心非、一步登天
- 說到做不到
- 「減脂教練」行銷標籤

**品牌見證**
- 9 年學員案例：20→29 歲、113→83kg、體脂 34%→13%
- 2022 疫情後開工作室（4 年品牌史）
- 多位學員從 2022 上到現在

**對標帳號（Jamie 指定）**
- 沈英登（韓國健身網紅 + 體能之巔）— 第一對標
- 洋洋（紐約 YouTuber）— 生活風格對標
- 惠利、文佳煐、IU、ROSE、aespa Winter — 藝人風格參考

**AI 時代戰略**
- YT 長片是本體（故事、深度，不可被 AI 取代）
- Shorts 是切片（導流用）
- IG 貼文是日常
- Threads 是人格

**活動形式偏好**
- Jamie 最開心的是 **1 對 1 教學**
- 不是活動派 / 團體派
- 適合：輕量引流活動（限額 5 個體驗、「4 月只收 3 個新學生」）
- 不適合：大型團訓、挑戰營

### 飲食計算準則
- 蛋白質：體重 × 1.2 / 碳水：體重 × 1.5（約 7-8 份）/ 油脂：固定 3 份
- 1 拳頭白飯 = 4 份、55g 地瓜 = 1 份、1 手掌肉 = 3 份
- 每天至少 400g 蔬菜 + 1 份水果

### 訓練強度
- 3-6 下力竭為主要強度區間
- 訓練日確保碳水資源（1.75 個拳頭）就位
- 12 下變輕鬆時立刻加重進入 3-6 下區間

---

## Telegram Bot

| 欄位 | 內容 |
|------|------|
| Token | `8754872172:AAFSRJuneA12RZAbyfn38h3XDEq5uN9MPQk` |
| Chat ID | `8708811744` |
| 方式 | Claude Plugin（settings.json `enabledPlugins` 已啟用，啟動 `claude` 即自動載入）|
| 啟動指令 | `claude --channels plugin:telegram@claude-plugins-official` |
| ⚠️ 注意 | Python bot 已停用（`.bak`），不要重啟 |
| ⚠️ 重要 | 每次開終端必須加 `--channels` 參數，否則收不到 Telegram 訊息 |

---

## 已授權平台（Chrome 可自由讀取）

| 平台 | 網址 | 用途 |
|------|------|------|
| Gmail (jaw2654) | mail.google.com | 收件匣讀取 |
| Gmail (repurre2022) | mail.google.com | 行事曆帳號 |
| Google 試算表 | docs.google.com/spreadsheets | 薪資/數據 |
| YouTube Studio | youtube.com/@jamie_wu_1012 | 頻道數據 |
| Instagram Insights | instagram.com/accounts/insights | IG 數據 |
| MOVE ON CREW Skool | skool.com/home-gym-3231 | Jamie 健身社群 |
| LINKGOODS | linkgoods.com/jamiewu | 個人連結頁 |

---

## 排程任務（launchd · 9 個 core · 每次 session 開始必確認）

| plist | Cron | 說明 |
|-------|------|------|
| `com.repurre.morning-briefing` | `0 8 * * *` | 每天 08:00 晨報 |
| `com.repurre.threads-daily-post` | `0 12 * * *` | 每天 12:00 Threads 發文 |
| `com.repurre.threads-canary` | `58 11 * * *` | 每天 11:58 Threads precheck |
| `com.repurre.claude-watchdog` | 每 3 分 | launchd 任務健康檢查 |
| `com.repurre.evening-review` | `0 23 * * *` | 每晚 23:00 晚安回顧 |
| `com.repurre.weekly-report` | `0 18 * * 0` | 週日 18:00 週報 |
| `com.repurre.inspiration-refresh` | `0 17 * * 0` | 週日 17:00 靈感池更新 |
| `com.repurre.monthly-funnel` | `0 9 1 * *` | 每月 1 日 09:00 漏斗報告 |
| `com.repurre.salary` | `0 22 28-31 * *` | 月底 22:00 薪資結算 |

確認方式：`launchctl list | grep repurre`

---

## 報告格式規範（格式鎖死，除非 Jamie 主動要求才改）

### 晨報格式（morning-briefing）

- **格式模板**：`新工作文件/背景設定/morning-briefing-template.html`（04-12 確認版，必讀）
- **輸出路徑**：`新工作文件/每日簡報/morning-briefing-YYYY-MM-DD.html`
- **推播**：Telegram 傳文字摘要 + HTML 檔案 + 電腦開瀏覽器（不附網址）
- **背景**：`#0a0a0a`（極深黑）
- **強調色**：`#d8d8d8`（淺灰，取代金色）
- **Container**：`#141414`
- **風格**：黑白灰單色調，無彩色元素
- **Tab 機制**：CSS radio button，inputs 在 `.tabs-wrapper` 內，與 content div 為同層 siblings，使用 `#tabN:checked ~ #contentN` 選擇器
- **必須包含手機適配 CSS**（@media max-width: 600px）
- **⚠️ 固定 6 個 Tab（不可更改）**：

| Tab | 內容 |
|-----|------|
| ☑️ 每日流程 | 今日行程（Google Calendar）+ Daily Checklist 合併在同一 Tab |
| 📧 Gmail | 讀取真實收件匣未讀信件；若無則顯示「目前收件匣無未讀重要信件」|
| 🌍 世界大事 | 美股行情（道瓊/S&P/NASDAQ）+ 當日最新國際新聞 3–5 則，每則必附真實出處 URL |
| 💪 全球健身話題 | 全球健身趨勢 + 台灣競品觀察，每則附出處 URL |
| 📱 K-pop 運動飲食保養 | K-pop 藝人訓練法 + 韓星飲食策略 + 韓國保養時尚趨勢，每則附出處 URL |
| 🎬 影片內容建議 | 長影片 YouTube 選題（含 HOOK + 4 段承接鋪合）+ 短影片 Reels/Shorts（含 HOOK + 3 段承接）|

- ⚠️ **所有新聞必須附真實出處 URL，禁止捏造**
- **輸出路徑**：`新工作文件/每日簡報/morning-briefing-YYYY-MM-DD.html`
- **Telegram**：傳送 HTML 檔案（sendDocument），讓手機用瀏覽器開啟

### 週報格式（weekly-integrated-report）

- **背景**：`#080808`（極深黑）
- **強調色**：`#d8d8d8`（淺灰，取代金色；CSS 變數 `--gold` 改為此值）
- **風格**：黑白灰單色調，無彩色元素（red/green/blue/purple/pink 一律換為灰階）
- **Tab 機制**：JavaScript（`function show(n)` + `onclick="show(n)"`）
- **8 個 Tab**：

| Tab | 內容 |
|-----|------|
| 📊 本週總覽 × TA | KPI 總覽、TA 輪廓、本週重大背景 |
| 📸 IG × TA 深度 | 觸及/非粉絲%/各貼文表現 |
| 🎬 YouTube 分析 | 觀看數、訂閱變化、影片表現 |
| 🇰🇷 韓系體態整合 | 韓國健身/時尚/藝人趨勢 |
| 👥 學員動態 | 課堂數、學員反饋、新客開發 |
| 🎯 下週精準策略 | 基於本週數據的內容策略建議 |
| 🗓 週執行計劃 | 下週具體排程（IG/YT 發文計劃）|
| ✈ 首爾特輯 | 韓國市場/文化相關更新（或該週主題）|

- **格式模板**：`新工作文件/週報/週報_template_TA深度版.html`（必讀）
- **輸出路徑**：`新工作文件/週報/weekly-report-YYYY-MM-DD-v2.html`
- **推播**：Telegram 傳 HTML 檔案 + 電腦開瀏覽器
- **必須包含手機適配 CSS**（@media max-width: 768px）

---

## 資料夾結構

```
Claude cowork/                  ← iCloud 路徑 claude cowork (小寫 c)
├── CLAUDE.md                   ← 此檔案（每次開 session 必讀）
├── week-20260420-all-in-one.md ← 本週內容 pack
├── shorts-thumbs/              ← YT Shorts 縮圖
└── 新工作文件/                  ← 主工作夾
    ├── public/                 ← Cloudflare Pages 部署源（唯一）
    ├── content-pack/           ← 每週內容包 (week-YYYYMMDD/)
    ├── content-plan/           ← 月主題池
    ├── scripts/                ← 自動化腳本 (ig-post / social-post / yt-api-upload 等)
    ├── email/                  ← 425 warm list + CSV
    ├── research/               ← 市場研究快照
    ├── 背景設定/               ← 4 份分冊 + 報告模板
    ├── 每日簡報/               ← morning-briefing-YYYY-MM-DD.html
    ├── 每日晚安回顧/           ← evening-review
    ├── 週報/                   ← weekly-report-YYYY-MM-DD-v2.html
    ├── 簡報/                   ← deck v10 + 歷史筆記
    ├── 素材/                   ← 照片 / 影片
    ├── 薪資/                   ← 薪資 Excel
    ├── transcripts/            ← 逐字稿
    ├── browser-profile/        ← Playwright profile (BSuite 自動化)
    ├── course-kb/              ← 課程知識庫
    └── threads-queue/posts.json ← Threads 發文佇列
```

### iCloud 同步

- iCloud 路徑：`~/Library/Mobile Documents/com~apple~CloudDocs/Claude cowork/`
- 每次更新 CLAUDE.md 或報告後，同步到 iCloud

### Cloudflare Pages 部署（背景自動，不推播網址）

- 平台：Cloudflare Pages（已從 Vercel 切換）
- 專案名：repurre-reports
- 公開網址：https://repurre-reports.pages.dev
- 每次報告生成後：複製到 `public/` → `wrangler pages deploy 新工作文件/public/ --project-name repurre-reports`
- Telegram 推播**不附網址**，Jamie 需要分享時自己去拿
- 舊 Vercel 網址（備用）：https://public-ten-mauve.vercel.app

---

## 輸出方式（固定規則）

| 報告 | 輸出 | 時間 |
|------|------|------|
| 晨報 | Telegram 推播 HTML + 文字摘要 + 電腦開啟瀏覽器 | 每日 08:00 |
| 晚報 | Telegram 原生訊息 | 每日 23:00 |
| 週報 | Telegram 推播 HTML + 電腦開啟瀏覽器 | 週日 18:00 |
| 薪資 | Excel 存檔 | 月底 22:00 |
| Threads | 自動發文 | 每日 12:00 |

⚠️ **禁止寄 Email**——所有報告改為 Telegram sendDocument 推播，不使用 Gmail。
⚠️ **Cloudflare 背景部署**——每次報告生成後自動部署到 Cloudflare Pages（公開可分享），但 Telegram 推播不附網址。

---

## 終端環境設定（已完成，勿重複安裝）

### 01 終端優化
- `CLAUDE_CODE_NO_FLICKER=1`（差分渲染，防閃爍）
- `CLAUDE_CODE_SCROLL_SPEED=3`（滾輪速度）
- `cc` alias：`cd ~/Desktop/Claude\ cowork && claude --channels plugin:telegram@claude-plugins-official`
- 設定位置：`~/.zshrc`

### 02 外部編輯器
- 編輯器：CotEditor（Mac App Store 免費）
- CLI wrapper：`~/.local/bin/cot-editor`（cot --wait wrapper）
- 環境變數：`EDITOR='cot-editor'`（在 `~/.zshrc`）
- 使用方式：Claude Code 中按 `Ctrl+G` 開啟

### 03 安全刪除
- `rm` alias 為 `trash`（移到垃圾桶，可還原）
- `rm!` 為 `/bin/rm`（真正刪除，慎用）
- 20 條危險指令黑名單（在 `~/.claude/settings.json` 的 `permissions.deny`）
- 包含：rm -rf、sudo、git reset --hard、git push --force 等

### 04 MCP 工具
| MCP Server | 用途 |
|------------|------|
| Firecrawl | 網頁爬取/搜尋 |
| Filesystem | 檔案系統存取（Desktop/Documents/Downloads/iCloud） |
| Playwright | 瀏覽器自動化 |
| Cloudflare | Cloudflare Pages 靜態部署 + 觀測 |

### 05 部署工具
| 工具 | 狀態 | 適用場景 |
|------|------|----------|
| Cloudflare Pages | **主力**（repurre-reports） | 晨報/週報/schedule 頁 HTML |
| Zeabur | Plugin 已安裝（zeabur@zeabur） | 有後端/資料庫的專案 |
| Vercel | 備用（public-ten-mauve） | 舊部署，已切換至 Cloudflare |

### 06 權限模式
- 模式：`bypassPermissions`（全自動，不逐步確認）
- 設定位置：`~/.claude/settings.json`

### 07 Plugins
| Plugin | 用途 |
|--------|------|
| telegram@claude-plugins-official | Telegram Bot 推播 |
| context7@claude-plugins-official | 文件查詢 |
| claude-md-management@claude-plugins-official | CLAUDE.md 管理 |
| hookify@claude-plugins-official | Hook 管理 |
| zeabur@zeabur | Zeabur 部署 |

### 08 自訂 Skills
| Skill | 路徑 | 用途 |
|-------|------|------|
| /morning-briefing | `~/.claude/skills/morning-briefing/` | 每日晨報 |
| /evening-review | `~/.claude/skills/evening-review/` | 每晚回顧 |
| /weekly-report | `~/.claude/skills/weekly-report/` | 週報 |
| /content-write | `~/.claude/skills/content-write/` | 內容包產稿 |
| /content-voice | `~/.claude/skills/content-voice/` | 品牌語氣校稿 |
| /carousel-build | `~/.claude/skills/carousel-build/` | v14 輪播產出 |
| /inspiration-refresh | `~/.claude/skills/inspiration-refresh/` | 週日靈感池更新 |
| /subtitle-ai | `~/.claude/skills/subtitle-ai/` | 字幕產 SRT |
| /transcribe | `~/.claude/skills/transcribe/` | 影片/音訊逐字稿 |
| /yt-vlog-pipeline | `~/.claude/skills/yt-vlog-pipeline/` | YT Vlog 上傳一條龍 |
| /publish-verify | `~/.claude/skills/publish-verify/` | 發佈後 curl 驗證 |
| /monthly-funnel | `~/.claude/skills/monthly-funnel/` | 每月漏斗報告 |
| /skill-creator | `~/.claude/skills/skill-creator/` | 建立/優化 skill |

### 09 語音輸入（Wispr Flow）
- **App**：Wispr Flow（https://wisprflow.ai）
- **登入**：Google OAuth — jaw2654@gmail.com
- **語言**：Auto Detect / Chinese (Traditional)
- **使用方式**：按住熱鍵說話 → 自動轉文字到任何 App 的輸入框
- **Jamie 偏好**：講話比打字快，可以用語音跟 Claude 溝通

### 10 社群發文（Browser Use）
- **方式**：Playwright 瀏覽器自動化 + Chrome cookies
- **Cookies 路徑**：`/tmp/social-cookies.json`（從 Chrome 匯出）
- **腳本路徑**：`新工作文件/scripts/social-post.py`
- **支援平台**：Threads / IG / YouTube
- **使用方式**：Jamie 說「發 Threads：（內容）」→ 自動發文
- **Cookie 匯出指令**：`python3 -c "import browser_cookie3, json; ..."`（需重新匯出時執行）
- **⚠️ 注意**：Chrome 清 cookies 或登出後需重新匯出

### 09 Claude.ai MCP（自動連線）
Google Calendar、Gmail、Canva、Notion、Gamma、Miro

### 參考來源
- [雷蒙 Claude Code Starter Kit](https://github.com/Raymondhou0917/claude-code-resources/tree/master/starter-kit)
- [AI 操控軟體的五種方式](https://raymondhouch.com/lifehacker/digital-workflow/how-ai-controls-software-api-cli-mcp-browser-use/)
- [Zeabur vs Cloudflare 部署指南](https://raymondhouch.com/lifehacker/digital-workflow/zeabur-cloudflare-deploy-guide/)
- [Agent Skills 官方規範](https://agentskills.io/home)

---

## 工具注意事項

- Gmail MCP：**只用來讀取 inbox 真實信件**，不寄 Email、不建草稿
- 搜尋 Gmail 時用：`in:inbox is:unread newer_than:3d`（排除草稿和自動信）
- 若 Gmail inbox 無未讀信件，Tab 顯示「目前收件匣無未讀重要信件」
- 所有新聞必須有真實出處 URL，禁止捏造
- 所有市場調查、名人、藝人、idol、世界新聞內容必須符合真實性，做不到寧可不寫
- 內容產出必須符合 TA 需求（35-45 成熟女性，見品牌定位），產出有價值的內容
- Telegram 推播：用 `sendDocument` 傳送 HTML 檔案（讓手機用瀏覽器開啟）
- **電腦開啟報告一律用 Safari 開 Cloudflare Pages 公開網址**，不開本地檔案
- 晨報：`open -a Safari https://repurre-reports.pages.dev/morning-briefing-YYYY-MM-DD.html`
- 週報：`open -a Safari https://repurre-reports.pages.dev/weekly-report-YYYY-MM-DD-v2.html`
