---
name: weekly-integrated-report
description: |
  repurre Health Studio 每週整合週報技能。當用戶說「幫我做週報」、「本週總結」、「週報」、「幫我整合本週數據」、「本週 IG 和 YouTube 表現」時觸發。也在每週日 18:00 自動執行排程任務。

  此技能會：
  1. 整合本週 YouTube + IG 數據（WebSearch 公開數據）
  2. 讀取 Gmail 本週重要工作信件
  3. 競品分析（搜尋同類帳號本週表現）
  4. 生成黑金風格互動式 HTML 週報（8個頁籤，TA 深度版）
  5. 存入「工作文件/週報/」資料夾
  6. Telegram 推播 HTML 檔案

  每當用戶提到本週總結、週報、IG/YouTube 數據整合，都應主動使用此技能。
  自動排程：每週日 18:00 執行（cron: 0 18 * * 0）
---

# repurre 每週整合週報

## 背景

- **使用者**：Jamie Wu（巫采縈），repurre Health Studio 教練
- **IG 帳號**：@jamie_wu_1012
- **YouTube 頻道**：repurre Health Studio
- **輸出路徑**：`工作文件/週報/weekly-report-YYYY-MM-DD-v2.html`
- **工作 Email**：jaw2654@gmail.com
- **週報模板**：`工作文件/週報/週報_template_TA深度版.html`（必讀，確認格式）
- **Telegram Bot Token**：`8754872172:AAFSRJuneA12RZAbyfn38h3XDEq5uN9MPQk`
- **Telegram Chat ID**：`8708811744`

---

## 重要：週報格式規範（固定不變）

週報一律使用 **TA 深度版**格式，必須先讀取模板 `工作文件/週報/週報_template_TA深度版.html`。

### 固定色彩規範
```css
:root {
  --bg: #080808;
  --card: #111111;
  --card2: #181818;
  --border: #222;
  --gold: #c8952e;
  --gold-light: #e8b84a;
  --gold-dim: rgba(200,149,46,0.15);
  --red: #e05252;
  --green: #4caf7d;
  --blue: #5b9cf6;
  --purple: #a78bfa;
  --pink: #f472b6;
  --text: #f0ece4;
  --muted: #888;
}
```

### Tab 機制（JS onclick，非 CSS radio）
```html
<div class="tabs-wrap">
  <div class="tabs">
    <button class="tab-btn active" onclick="show(0)">📊 本週總覽 × TA</button>
    <button class="tab-btn" onclick="show(1)">📸 IG × TA 深度</button>
    <button class="tab-btn" onclick="show(2)">🎬 YouTube 分析</button>
    <button class="tab-btn" onclick="show(3)">🇰🇷 韓系體態整合</button>
    <button class="tab-btn" onclick="show(4)">👥 學員動態</button>
    <button class="tab-btn" onclick="show(5)">🎯 下週精準策略</button>
    <button class="tab-btn" onclick="show(6)">🗓 週執行計劃</button>
    <button class="tab-btn" onclick="show(7)">✈ 首爾特輯</button>
  </div>
</div>

<script>
function show(n) {
  document.querySelectorAll('.tab-panel').forEach((p,i) => {
    p.style.display = (i === n) ? 'block' : 'none';
  });
  document.querySelectorAll('.tab-btn').forEach((b,i) => {
    b.classList.toggle('active', i === n);
  });
}
</script>
```

### Header 結構（固定）
```html
<div class="header">
  <div>
    <div class="header-brand">repurre</div>
    <div class="header-sub">週報 v2 TA深度版 ｜ YYYY.MM.DD–MM.DD ｜ 本週主題</div>
  </div>
  <div class="header-pills">
    <div class="pill">IG 觸及 <strong>~數字</strong></div>
    <div class="pill">非粉絲 <strong>~XX%</strong></div>
    <div class="pill">核心 TA <strong>25–36歲女性</strong></div>
    <div class="pill">學員 <strong>X堂</strong></div>
  </div>
</div>
<div class="alert-bar">
  <span class="alert-tag">⚠ 本週特別</span>
  本週重要事項簡述...
</div>
```

---

## 8 個 Tab 內容規範

### Tab 0：📊 本週總覽 × TA

- **KPI 區**（g4 grid）：YouTube 觀看數、IG 觸及人數、IG 曝光次數、學員堂數
- **本週重大背景事件**（g3 grid）：影響策略的重要事件（市場/社會/個人）
- **TA 基本輪廓**（g2 grid）：人口統計、發現路徑、曾嘗試的方法、教練偏好
- **TA 核心痛點排行**（bar chart）

KPI 元件：
```html
<div class="kpi">
  <div class="kpi-val red">~2,500</div>
  <div class="kpi-label">YouTube 觀看數</div>
  <div class="kpi-delta flat">無新片，自然流量</div>
</div>
```

### Tab 1：📸 IG × TA 深度

- IG 本週貼文列表（每篇：類型/觸及/互動率/TA 評論）
- 非粉絲觸及比例分析
- Reels vs 靜態貼文表現對比
- TA 互動特徵分析

### Tab 2：🎬 YouTube 分析

- 本週上傳影片（若有）：標題、觀看數、觀看時長、TA 輪廓
- 頻道總體數據：訂閱數趨勢
- IG vs YouTube TA 差異分析

### Tab 3：🇰🇷 韓系體態整合

搜尋：
```
"韓國藝人 身材管理 운동 YYYY-MM" OR "K-pop idol fitness diet 2026"
"韓國 健身 트렌드 YYYY" OR "K-fitness trend"
```

- 韓國藝人身材管理方式（5-6 位，附 Jamie 教練專業評語）
- 韓國健身文化 vs 台灣差異
- 可借鑒的內容策略

藝人卡格式：
```html
<div class="celeb-card">
  <div class="celeb-name">藝人名稱</div>
  <span class="celeb-badge badge-ok">✅ 可借鑒</span>
  <div class="celeb-method">管理方式：...</div>
  <div class="celeb-comment">Jamie 評語：從運動科學角度...</div>
</div>
```

### Tab 4：👥 學員動態

從 Google Calendar 統計本週課堂數：
- 各學員上課次數
- Dana 代課情況
- 新客諮詢/體驗課情況
- 學員進度更新

### Tab 5：🎯 下週精準策略

基於本週數據的具體建議：
- 內容策略（幾篇 Reels / 幾篇靜態 / 主題方向）
- 招生策略（TA 痛點切入點）
- 課程安排建議

action-row 格式：
```html
<div class="action-row">
  <div class="action-num">1</div>
  <div class="action-text">
    <div class="action-title">行動標題</div>
    <div class="action-desc">具體說明...</div>
  </div>
</div>
```

### Tab 6：🗓 週執行計劃

下週 7 天 calendar grid：
```html
<div class="calendar">
  <div class="day-card">
    <div class="day-header">Mon</div>
    <div class="day-date">04/13</div>
    <span class="day-tag reels">Reels</span>
    <div class="day-desc">首爾健身文化開箱...</div>
  </div>
  <!-- 週二至週日 -->
</div>
```

### Tab 7：✈ 首爾特輯（或本週特殊主題）

若本週有特殊主題（首爾行程、重大活動、特殊挑戰）則顯示相關內容。
平常週可改為「本季策略展望」或「月度回顧」。

```html
<div class="seoul-card">
  <div class="seoul-title">🇰🇷 首爾特輯標題</div>
  <div class="seoul-body">內容詳述...</div>
</div>
```

---

## 步驟一：讀取週報模板

**必須先執行**：
```
Read 工作文件/週報/週報_template_TA深度版.html
```
確認最新格式後再生成本週週報。

---

## 步驟二：收集本週數據

**計算本週日期範圍**：上週一至本週日（YYYY.MM.DD–MM.DD）

**IG 數據（WebSearch）：**
```
"@jamie_wu_1012 Instagram 本週" OR "repurre Health Studio IG"
```
估算：觸及率、互動率、新增粉絲、非粉絲觸及%

**YouTube 數據（WebSearch）：**
```
"repurre Health Studio YouTube 本週"
```
訂閱數、本週上傳影片表現

**Gmail 本週重要信件：**
```
gmail_search_messages: jaw2654@gmail.com, newer_than:7d, is:important
```

**競品分析（WebSearch）：**
```
"台灣女性健身教練 Instagram 本週" OR "fitness coach Taiwan 2026"
```

**行事曆本週課堂數：**
```
gcal_list_events: repurre2022@gmail.com, 本週一至週日
```

---

## 步驟三：生成 HTML 週報

基於模板格式，填入本週實際數據，生成完整 HTML。

**命名規則**：`weekly-report-YYYY-MM-DD-v2.html`（日期為本週日）

---

## 步驟四：Telegram 推播 HTML 檔案

```bash
python3 -c "
import subprocess, json
from datetime import datetime

TOKEN = '8754872172:AAFSRJuneA12RZAbyfn38h3XDEq5uN9MPQk'
CHAT_ID = '8708811744'
DATE = 'YYYY-MM-DD'  # 替換本週日日期
html_path = f'/Users/user/Desktop/Claude cowork/工作文件/週報/weekly-report-{DATE}-v2.html'

result = subprocess.run([
    'curl', '-s', '-X', 'POST',
    f'https://api.telegram.org/bot{TOKEN}/sendDocument',
    '-F', f'chat_id={CHAT_ID}',
    '-F', f'document=@{html_path}',
    '-F', f'caption=📊 repurre 週報 {DATE}\n點擊開啟完整互動週報（8個分頁）'
], capture_output=True, text=True)

r = json.loads(result.stdout)
print('✅ Telegram 推播成功' if r.get('ok') else f'❌ 錯誤：{r}')
"
```

---

## 問題處理

| 情況 | 處理方式 |
|------|----------|
| IG 無公開數據 | 根據歷史數據估算，標注「估計值」|
| YouTube 查不到本週數據 | 顯示「本週無新片上傳」|
| Gmail 無重要信件 | 顯示「本週無重要工作信件」|
| 模板讀取失敗 | 使用 CLAUDE.md 中的格式規範生成 |
| Telegram 推播失敗 | 改傳文字摘要 fallback |
