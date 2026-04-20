# DESIGN.md · repurre Health Studio 品牌視覺系統

> 讓 Claude / Canva / Gamma / /cards skill 產視覺時 · 一律套這份規範 · 品牌一致性 4 週內建立記憶點

---

## 1. 品牌主題（Visual Theme）

**核心氣質**：Quiet Luxury 精品紀律派 · 不走表演式 · 不走大眾減脂教練
**情緒關鍵字**：沉著 · 陪伴 · 長線 · 真實 · 留白
**禁止氣質**：熱血 · 爆發力 · 成功學 · 打雞血 · 前後對比身材秀

**參考對標**：
- 沈英登（韓國健身網紅）· 體能之巔 · 紀律派
- 洋洋（紐約 YouTuber）· 生活風格
- 惠利 / 文佳煐 / IU / ROSE / aespa Winter · 藝人氣質參考

**絕不像的樣子**：
- 瘋狂露身材的健身教練
- 「80% 教練教錯」這種攻擊式內容
- 降價促銷 / 折扣推播
- 21 天變身 / 打卡挑戰

---

## 2. 色彩系統（Color System）

### 主色盤（Quiet Luxury）

| 用途 | HEX | RGB | 備註 |
|---|---|---|---|
| 主背景 · 米白 | `#faf7f2` | 250,247,242 | trainer-jamie.html + pricing.html 基底 |
| 品牌米色 | `#ede7d9` | 237,231,217 | hover / accent / 分隔 |
| 暖米灰（輪播 v14 背景）| `#f0ebe0` | 240,235,224 | v14 鐵律背景色 |
| 深黑 · 主字 | `#0a0a0a` | 10,10,10 | 內文、標題黑字 |
| 黑內文 | `#1a1a1a` | 26,26,26 | 細節層級 |
| 米色字（深底上）| `#f0ebe0` | 240,235,224 | v14 照片上文字 |

### 輔助色盤

| 用途 | HEX | 備註 |
|---|---|---|
| 強調淺灰 | `#d8d8d8` | 取代金色 · 報告強調色 |
| 米色字 light | `#e0d9ca` | caption body 文字 |
| 深黑 ultra | `#080808` | 週報背景 |

### 透明層規範（overlays）

- 照片 overlay（輪播 v14）：`linear-gradient(to bottom, rgba(0,0,0,0.62) 0%, 0.28 38%, 0.5 70%, 0.88 100%)`
- Caption block：`background: rgba(0,0,0,0.42); backdrop-filter: blur(14px); border-left: 2px solid #f5f5f5;`
- 高光框（highlight em）：`background: rgba(245,245,245,0.55); color: #141414; padding: 1px 3px;`

### 禁止色

- ❌ 紅 / 橘 / 黃（警示 / 熱血感）
- ❌ 粉 / 紫（甜美 / 少女感）
- ❌ 亮藍 / 亮綠（科技感）
- ❌ 純金色（太 luxury 浮誇）· 改淺灰 `#d8d8d8`

---

## 3. 字體系統（Typography）

### 主字體

- **中文**：`'Noto Serif TC'`（精品感 · Quiet Luxury）· 官方頁 + 輪播 title 用
- **中文次選**：`'Noto Sans TC', 'PingFang TC', 'Microsoft JhengHei'`（輪播 body · 報告）
- **英文 / 數字**：`-apple-system` 系 · 或 `'Fraunces'`（大數字 italic 強調）
- **打字機 / 程式碼**：`'JetBrains Mono'`（Deck v10 + 簡報打字機效果）
- **手寫襯線 italic**：`'Instrument Serif'`（.eye / .a-note 呼吸語氣）

### 字號底線（2026-04-20 Jamie 學員反映字太小 · 全放大 +30%）

| 元素 | 字號 | 用途 |
|---|---|---|
| Page title | 28px | 報告大標 |
| Hook | 24px | 輪播金句 |
| Title（輪播主文）| clamp(54px, 6.8vw, 78px) | 輪播大字 |
| Title-sm | clamp(34px, 3.8vw, 44px) | 副標 |
| Body / caption | clamp(32px, 3.6vw, 42px) | 正文 |
| Badge / lbl | 22px + padding 4-12px | 小框字 |
| Pull num（超大數字）| clamp(180px, 22vw, 280px) | 8% / 40% / 10% 類 |
| Top-bar / badge | 14px | 底部 metadata |

### 禁用樣式

- ❌ `text-shadow`（v14 鐵律禁止 · 精品感不靠 shadow）
- ❌ `font-weight: 900`（太粗不雅）· 用 700-800
- ❌ 斜體在一般內文（除了 .eye / .end-title / .pull-num）

---

## 4. 核心元件（Components）

### 4.1 輪播 v14（IG 1:1 · 本系統唯一輪播標準）

- 尺寸：1080×1080 (1:1)
- 背景：暖米灰 `#f0ebe0`
- 8 slide 結構：封面 + 6 內容 + slide 8 CTA（永遠存在）
- 照片 brightness 0.9 + contrast 1.03 + saturate 0.95
- 照片 position 65-75%（頭部上移留下半 caption 空間）
- 照片 + 黑色漸層 overlay + caption block 三明治
- 高光框（`em` 元素）1px 3px rgba(245,245,245,0.55) + color #141414
- 字體：Noto Sans TC · title 用 Fraunces italic for 數字 · .eye 用 Instrument Serif
- **絕不加 text-shadow**

### 4.2 Deck v10（16:9 簡報 · 錄影 + 教學用）

- 尺寸：1920×1080 (16:9)
- 背景：studio 照 full-bleed + dark overlay rgba(0,0,0,0.72-0.88)
- 字體：JetBrains Mono 打字機效果（技術感 · 紀律派）
- 字體色：米色 `#f0ebe0` / `#e0d9ca`
- 文字置中（利於錄影時 Jamie 眼神對準鏡頭）
- 高光框 em 同 v14

### 4.3 報告 HTML（晨報 / 晚報 / 週報 / 月漏斗）

- 黑白灰單色調 · 無彩色元素
- 背景：`#080808`（週報）或 `#0a0a0a`（晨報）
- 強調色：`#d8d8d8`（取代金色）
- Container：`#141414`
- 必含手機適配 CSS（@media max-width: 600px-768px）
- Tab 機制：
  - 晨報：CSS radio button（input in tabs-wrapper · 同層 sibling 結構）
  - 週報：JavaScript `function show(n)` + onclick

### 4.4 cover 頁（網站）

- `trainer-jamie.html` / `pricing.html` · 米白 + 黑 + Noto Serif TC
- 地址隱私：僅露「台北市大安區忠孝東路四段 233 號」· 6F-6 只在預約確認後私下告知
- 禁止折扣 / 優惠 / 免費試課字眼

---

## 5. 排版原則（Layout）

- **留白**：寧可少不可擠 · padding 48-72px / 10-15%
- **對齊**：中軸對齊 > 左對齊 > 右對齊（精品感中軸為主）
- **邊距**：照片 full-bleed 時沒邊距 · 文字區 10-15% padding
- **Grid**：輪播 1:1 單圖 · 報告 2-3 col grid · deck 16:9 中央集中
- **line-height**：1.4-1.5（呼吸感）· 中文不低於 1.4

---

## 6. 深度與質感（Depth & Texture）

- **陰影**：禁用 `box-shadow` 雜色 · 用 border `1px solid rgba(0,0,0,0.08)` 做分隔
- **邊框圓角**：2-4px 極小 · 不走卡片膨脹風
- **blur**：caption block `backdrop-filter: blur(14px)` 是 v14 唯一 blur 用途
- **梯度**：只在照片 overlay · 文字區不加 gradient

---

## 7. Do's & Don'ts

### Do

- ✅ 中軸對齊 · 留白 · Noto Serif TC
- ✅ 用「陪、走、長、練」· 不用「瘦、快、爆、速」
- ✅ 照片選穿搭 / 氣質 / 空間感
- ✅ 學員故事（9 年那位、52 歲、43 歲案例）「能力 / 生活 / 選擇」對比
- ✅ 招牌詞「代償歸零」「選擇的能力」每篇至少 1 個
- ✅ CTA 永遠二選一：檢測 `repurre-reports.pages.dev/assessment` 或 19 題體驗表單
- ✅ 影片發布一律 21:00 台灣時間（Threads 12:00 例外）

### Don't

- ❌ 瘦 / 減脂 / 速成 / 21 天 / 爆 / 燃脂（一律禁用）
- ❌ 折扣 / 免費諮詢 / 降價
- ❌ 攻擊其他教練 / 「80% 教練教錯」
- ❌ 身材 BA 對比（2026-04-27 週至 2026-05-10 週）· 用能力對比代替
- ❌ 「網紅式打 call」「姊妹們一起」
- ❌ text-shadow / box-shadow 雜色 / 卡片膨脹

---

## 8. 品牌招牌詞（Signature Words）

**主招牌詞**：**代償歸零**（how 層 · 方法）
**副招牌詞**：**選擇的能力** / **選擇權**（why 層 · 動機）
**品牌公式**：代償歸零 × 選擇的能力 = repurre
**Tagline**：**人生下半場 · 健康過一生**

**語氣關鍵詞**：
- 用：陪、走、長、練、撐、設計、底層、下半場
- 不用：瘦、快、爆、速、撕、狠、拼

**句式範例**：
- 「你現在練的不是肌肉 · 是 50 歲的選擇權」
- 「70 歲能跳舞的人 · 35 歲就開始準備了」
- 「不是為了變壯 · 是為了不失去做這些事的能力」

---

## 9. 適用場景（Where to Apply）

| 場景 | 套用 | 工具 |
|---|---|---|
| IG 輪播 v14 | 完整（色 + 字 + 照片規範）| carousel-build skill |
| IG Reels caption | 語氣 + 招牌詞 + CTA 規則 | content-write skill |
| Threads 每日 | 語氣 + 招牌詞 + 句式 | threads-auto-post.py |
| YT 長片 thumbnail | 色 + 字（Noto Serif TC）| /cards skill（未來）|
| YT 長片 description | 語氣 + 招牌詞 + CTA | content-write skill |
| 晨報 / 週報 / 晚報 HTML | 色（黑白灰）+ 手機 CSS | morning-briefing / weekly-report / evening-review |
| Cloudflare 網站 | 色（米白 + 黑）+ Noto Serif TC | trainer-jamie.html + pricing.html |
| XHS 圖文 | 9 張 + caption · 語氣 + 招牌詞 | 未來 xhs-auto-post.py |
| Canva / Gamma | 色盤 + 字體 + 招牌詞 | Canva MCP + Gamma MCP |

---

## 10. Review 與版本（Versioning）

- **v1 · 2026-04-20** · 初版 · 基於 CLAUDE.md + 輪播 v14 + 報告格式 + Jamie 4/20 feedback（字放大 / BA 規則 / CTA 二選一）整合
- 修改：Jamie feedback → 更新此檔 → 同步 memory（`project_design_md_v1_20260420`）
- 所有視覺產出 skill（carousel-build / content-write / /cards）自動 load 此檔為 style guide

**此檔是單一真相來源**。當 skill SKILL.md 跟此檔衝突時 · 以此檔為準。Skill 作者應在其 SKILL.md 加「Load DESIGN.md from `/Users/user/Library/Mobile Documents/com~apple~CloudDocs/claude cowork/DESIGN.md` first」。
