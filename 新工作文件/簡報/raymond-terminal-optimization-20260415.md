# 雷蒙 Claude Code 終端優化清單 for Jamie

**日期**：2026-04-15
**基底**：讀完雷蒙 7 篇 + Leo Aido 7 篇
**原則**：Jamie 是健身教練，不是工程師，超過需求不裝

---

## 摘要（一句話）

雷蒙的核心法三件事 Jamie 已經有：**CLAUDE.md + Skills + launchd 排程**。真正缺的是：**（1）三層記憶系統（MEMORY + Memory MCP + daily log）（2）Cmux 多 session 並行（3）手機遙控 Dispatch（4）Skill 自我審查機制**。其他他做的家庭自動化、Discord Bot、家庭財務 Dashboard 對 Jamie 不適用或已有替代方案（Telegram 已取代 Discord）。

---

## ✅ 立即可做（5 分內，影響最大）

### 1. CLAUDE.md 瘦身：從 400+ 行砍到 150 行
**雷蒙從 768 行砍到 120 行** — CLAUDE.md 每次對話都會載入，太長會吃掉 context 並降低表現。
Jamie 目前 CLAUDE.md 有 400+ 行，大量「2026-04-14 晚間重大更新」「LINE OA 自動回覆文案」等可以搬出去。

**做法**：
- 核心規則（≤150 行）留在 CLAUDE.md
- 領域知識（LINE OA 文案、表單 URL、價目表）搬去 `/skills/repurre-brand/references/` 或 `工作文件/背景設定/`
- 一次性決策（4/14 session 成果）只保留在 MEMORY.md

**指令**：`/claude-md-improver`（Jamie 已裝 claude-md-management plugin，可以直接跑）

---

### 2. 啟用 Memory MCP（三層記憶的第二層：知識圖譜）
**雷蒙設計**：MEMORY.md（短期）+ memory.json（知識圖譜）+ daily/*.md（時序）
Jamie 現在只有 MEMORY.md（`~/.claude/projects/.../memory/`），少了知識圖譜那層，無法回答「Jamie 用過哪些相似的 IG 對標帳號？」這種關聯性問題。

**指令**：
```bash
claude mcp add memory -- npx -y @modelcontextprotocol/server-memory
```

**為什麼適合她**：品牌/學員/對標帳號之間有大量關聯，圖譜比純 markdown 更能把握「沈英登 ↔ 洋洋 ↔ WO5」這種比較。

---

### 3. 建立 `/insight` 週反省 Skill
**雷蒙每週自動跑 `/insight`** — AI 分析過去一週的所有 session，找出重複摩擦點，優化 CLAUDE.md 與 Skills。

**做法**：新增 `~/.claude/skills/insight/SKILL.md`
- 觸發：週日夜間跑（可以搭進 weekly-integrated-report launchd）
- 內容：掃 `~/.claude/projects/*/memory/` 的 daily logs，找出重複被問的事 → 建議新 Skill 或修 CLAUDE.md

**回報**：Telegram 推摘要即可。**讓系統自己升級自己**，這是雷蒙說的「第三週系統自我演化」。

---

### 4. 開啟 macOS 系統通知
**雷蒙說這是 Claude Code「最被忽視的功能」** — 下完指令去泡咖啡，跳通知再回來看。
Jamie 現在 Telegram 已經做這件事，但當她人在電腦前時，系統通知比切 app 快。

**做法**：`~/.claude/settings.json` 加 `"notifyOnComplete": true`（或查官方最新鍵名）

---

## 🟡 今週可做（1-2 小時，有明顯增益）

### 5. 裝 Cmux（多 session 並行）
**雷蒙核心配置** — 左側垂直側邊欄分主題、右側同時並排 3-4 個 session，每個跑不同任務。

**適用情境（Jamie 的真實場景）**：
- Session 1：寫 IG 貼文 / Threads
- Session 2：跑晨報 / 週報
- Session 3：改 pricing.html / trainer-jamie.html
- Session 4：讀 Gmail / Tradesea

Jamie 用 Mac Mini M4，記憶體沒問題，Cmux 比單一終端機多開好管理。

**指令**：[Cmux 官方網站](https://cmux.sh)（Mac 版免費）

**取捨**：⚠️ 學習曲線 30 分鐘。如果她喜歡「一次專注一件事」（像雷蒙老婆），可以跳過。但她是工作狂 × 雙身份（健身 + 交易），並行需求高，**推薦試**。

---

### 6. Dispatch 手機遙控（Cowork 手機 App）
**雷蒙 4 月用 Cowork Dispatch** — 在外面用手機 App 下指令給家裡的電腦。
Jamie 去紐約 / 首爾出差時超有用。她現在在外只有 Telegram 能「聊」，但沒法「下任務」叫 Claude 跑晨報、抓數據、改網頁。

**做法**：
1. 手機裝 Claude 手機 App（Cowork 版）
2. 配對 Mac Mini（需要 Mac 保持開機 + 不休眠）
3. Mac 系統設定 → 電池 → 關閉自動休眠

**取捨**：⚠️ 需要 Mac 不休眠 24/7（電費小）。**推薦裝**——出國時是救命工具。

---

### 7. Skill 品質保證：skill-creator v2.0（4 個 eval agents）
**雷蒙做了個 meta 設計**：reviewer / grader / comparator / analyzer 四個子代理人，每次建新 Skill 自動跑品質檢查。
Jamie 已有 7+ skills，品質沒統一審查機制。

**做法**：擴充現有 `~/.claude/skills/skill-creator/`，加 `references/eval-agents.md` 定義 4 個審查角度。

**取捨**：⚠️ 對 Jamie 稍重，可以簡化為「每次建新 skill 後，跑一次 `/codex` 給第二意見」（Jamie 已有 codex skill）。

---

### 8. Subagent + Worktree 並行探索
**雷蒙用 Subagent 做「三件事一起跑最後彙整」** — 例如同時抓 IG / YT / 競品三個資料源後合併。
Jamie 現在週報是單線性跑，如果用 subagent 並行 IG + YT + Skool，時間可以從 10 分鐘壓到 3 分鐘。

**做法**：現有 `/weekly-report` skill 裡改寫 — 呼叫 3 個 subagent 並行抓數據，主 agent 等結果再整合。

**取捨**：⚠️ 週報已經每週跑一次，時間壓縮不是急需。**可以但不急**。

---

## ⏳ 以後再說（大於 3 小時或不急）

### 9. Obsidian 當「人看的文件」中樞（取代 CotEditor？）
**雷蒙組合 = 桌面 App + Obsidian + 終端機**
Obsidian 的 wikilinks 串連所有筆記、手機 / iPad / Mac 同步比 CotEditor 強。
Jamie 現在用 CotEditor 開單檔，沒有全局筆記網路。

**⚠️ 看她需要**：如果她只是偶爾編 HTML，CotEditor 夠用。如果她想把品牌內容、學員 CRM、課程腳本都存下來互相 link，Obsidian 是升級路徑（免費）。

---

### 10. iMessage 串接 Claude Code
**雷蒙寫過用 iMessage 讓家人也能用 AI 助理**。
Jamie 一個人經營品牌，沒有家人要一起用，**Telegram 已經完全取代這個需求**，❌ 不建議裝。

---

### 11. Discord Bot（Kairos）
雷蒙的「主動推送」核心，但 **Jamie 已有 launchd + Telegram plugin 的完整替代方案**，❌ 不必重做。

---

### 12. Home Assistant / 智能家庭
雷蒙的副產品。Jamie 住工作室，13 坪，沒智慧家庭設備，❌ 不適用。

---

### 13. 家庭財務 Dashboard
雷蒙整合股票 + 記帳 + 訂閱。Jamie 的交易日誌已經是這個定位（甚至更專業），❌ 已滿足。

---

### 14. Gemini 配圖生成工作流
**雷蒙用 Gemini 生 2K 教學配圖**。Jamie 有 Canva MCP + Canva brand kit，**視覺走 Quiet Luxury 精品感**，Gemini 生的風格不符合。❌ 不建議。

---

### 15. Bot Watchdog（crontab 每 15 分檢查 Bot 存活）
雷蒙的 Discord Bot 需要。Jamie 的 launchd 已有失敗重試機制（KeepAlive），❌ 不必另做。

---

### 16. 截圖合成工具（screenshot-composite）
雷蒙做了品牌浮水印工具。Jamie 如果要做品牌統一的截圖（例如學員見證），**⚠️ 看需要**——她的 Cloudflare 頁面截圖目前沒有浮水印需求。

---

## 📋 Jamie vs 雷蒙 差距一覽表

| 項目 | 雷蒙 | Jamie | 差距 |
|---|---|---|---|
| CLAUDE.md 行數 | 120 | 400+ | ❌ 太長，需瘦身 |
| 記憶系統 | 三層（MEMORY + MCP + daily） | 單層（MEMORY.md） | ❌ 缺 Memory MCP |
| 排程方式 | cron + Mac mini 24/7 | launchd ✓ | ✅ 一樣穩 |
| 推播通道 | Discord Bot | Telegram Plugin | ✅ 同等 |
| 多 session | Cmux | 單終端 | ❌ 缺 Cmux |
| 手機遙控 | Dispatch | Telegram 單向 | ⚠️ 部分缺 |
| Skills 數量 | 25 | 7 | ⚠️ 自然成長中 |
| Skill QA | 4 eval agents | 無 | ⚠️ 可輕量化版 |
| 自我演化 | /insight 週跑 | 無 | ❌ 最該補 |
| 知識分層 | Skills + references 拆分 | 大部分塞 CLAUDE.md | ❌ 需重整 |
| 外部編輯器 | Obsidian | CotEditor | ⚠️ 看需求 |
| MCP 工具數 | 19 | 8 | ✅ 沒必要追平 |

---

## 🎯 最終建議：3 件事本週做

1. **今晚（15 分）**：`/claude-md-improver` 砍 CLAUDE.md + 裝 Memory MCP
2. **這週找 1 小時**：裝 Cmux、跑一次試試多 session 並行
3. **週末**：寫 `/insight` skill，讓系統每週自己反省 + 升級

其他項目（Obsidian / Dispatch / Subagent）等這三個做完、跑順，再決定要不要追加。

**核心精神（雷蒙原話）**：
> AI 不需要記住所有細節，但需要知道去哪裡找。
> 最好的 Skill 是你自己長出來的，不是別人打包好的。

Jamie 已經比雷蒙說的 80% 的人走得更遠，剩下的是**知識分層**（CLAUDE.md 瘦身）和**系統自我演化**（/insight）兩步。
