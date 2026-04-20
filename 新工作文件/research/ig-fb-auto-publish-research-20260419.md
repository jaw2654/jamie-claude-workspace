# IG / FB 自動發文 2026 全景深度研究

> 日期：2026-04-19 08:46
> 背景：Jamie 04/20 21:00 IG Reel 自動發文需求 · 昨晚 Appium + instagrapi + IG Web + Business Suite 4 路全試 · 今早 Appium wireless pairing 成功但 Schedule flow 未 probe 完
> 目標：找出「Mac 完全獨立 · 不靠 iPhone 手動」的真自動發文路徑

---

## TL;DR · 給 Jamie 3 句話

1. **你要的「Mac 自動不靠 iPhone」真正答案 = Meta Business Suite 桌面網頁版**（business.facebook.com · 免費 · 瀏覽器直接排程 Reel · 75 天內 · Creator/Business 帳號可用）
2. **Setup 只要你 1 次**：IG 轉 Professional（應已是）+ 連 FB 粉專 + Mac 瀏覽器登 FB · 之後 04/20 / 04/23 / 04/25 排程全在 Mac 完成
3. **一次 setup 之後 Claude 可以用 Playwright 完全自動化 business.facebook.com 的上傳 + 排程**（不用你開瀏覽器）或你手動 1 分鐘搞定

---

## 為什麼現況複雜（速懂 3 點）

1. **IG 不歡迎自動化**：Instagram 2024 年後對 Personal 帳號鎖死 API；Web 版不支援 Reel upload；private API (instagrapi) 被 anti-bot 擋
2. **Reel 是 Pro 功能**：官方 API（Graph API）與所有排程器**只支援 Business/Creator 帳號** + 必須連 FB 粉專
3. **Appium 的限制**：iPhone UI automation 需要 iPhone 同 WiFi + Mac 實時控 · Jamie 出門 iPhone 斷就無法自動

---

## 9 條自動發 Reel 路徑 · 可行性矩陣

| # | 路徑 | 可行 | Setup 時間 | 穩定度 | 成本 | 不用 iPhone？ |
|---|------|------|------------|--------|------|---------------|
| 1 | **Meta Business Suite 桌面網頁** | ✅✅✅ | 5-10 分 | 高（官方） | 免費 | ✅ |
| 2 | **Metricool 免費方案** | ✅✅ | 10 分 | 高 | 免費（50 posts/月） | ✅ |
| 3 | **Graph API 自寫 Python** | ✅✅ | 30-60 分 | 高 | 免費 | ✅ |
| 4 | Later / Buffer / Publer 付費 | ✅ | 10 分 | 高 | $15-99/月 | ✅ |
| 5 | Appium wireless iPhone | ⚠️ | 已 setup · 20 分 probe | 中（要同 WiFi） | 免費 | ❌ iPhone 要在家 WiFi |
| 6 | instagrapi private API | ❌ | - | 低（2FA 擋） | 免費 | ✅ |
| 7 | IG Web browser automation | ❌ | - | 0（不支援 Reel） | 免費 | ✅ |
| 8 | Android Emulator + IG | ⚠️ | 1 小時 | 低（雙裝置登入 IG 風險） | 免費 | ✅ |
| 9 | iPhone App 內建 Schedule（手動） | ✅✅✅ | 60 秒/次 | 最高 | 免費 | ❌ 要 iPhone |

---

## 路徑 1 · Meta Business Suite 桌面網頁（最推）

### 做什麼
瀏覽器打開 business.facebook.com → Planner / Content → Create reel → 上傳影片 + caption + 選 04/20 21:00 → 排程

### 為什麼推
- **官方 · Meta 自家**（不會因 TOS 改動被擋）
- **免費**
- **純瀏覽器**不用寫一行 code
- **Claude 可以 Playwright 幫你全自動**（存 Jamie 瀏覽器 session · 每週自動排程）
- 75 天內皆可排程

### 前提
- IG 帳號是 Professional（Creator 或 Business 都可）· Jamie 跑 GoSky 應該已是
- 連到一個 FB Page（粉專）· 如沒有要先建一個
- Mac 瀏覽器登入 Jamie 的 FB

### 限制
- 不支援 Stories 排程（只 Post/Reel）
- 不支援 Collaborations 邀請（04/20 你想用 @repurre_life 協作者這功能 Business Suite **不給**）
- 不能用 IG App 內的 AI 字幕 / 特效（影片剪映剪好再上傳）

### 解決 @repurre_life Collab 問題
排程完到時間發出後 · 再進 IG App 編輯貼文加 Collaborator · 或跳過 Collab · 或在 caption 裡 @repurre_life tag（功能不同但還能觸及）

---

## 路徑 2 · Metricool 免費方案

### 做什麼
Metricool.com 註冊免費帳號 → 連 IG（需 Professional）+ FB Page → 排程 Reel

### 為什麼次推
- **介面比 Meta Business Suite 漂亮**
- 可同時管 IG + FB + Threads + YT + TikTok
- 50 posts/月 跨全平台免費

### 前提同路徑 1

### 限制
- 免費 tier 50 posts/月·你 IG + Threads 日更每月 60+篇會超
- 要看 Threads 日更是否也走 Metricool · 不走就 50 夠

---

## 路徑 3 · Graph API 自寫 Python

### 做什麼
```python
# 1. 上傳 media container
container = requests.post(f"https://graph.facebook.com/v19.0/{ig_user_id}/media", data={
    "media_type": "REELS",
    "video_url": "https://your-server.com/reel.mp4",
    "caption": caption_text,
    "access_token": token,
    "coauthor_producer_ids": "[repurre_life_id]",  # Collab 功能這條通
})
# 2. Poll until ready
# 3. Publish
requests.post(f"https://graph.facebook.com/v19.0/{ig_user_id}/media_publish", data={
    "creation_id": container.id, "access_token": token
})
```

### 優勢
- **完全自動**不用瀏覽器不用 iPhone
- **支援 Collaborators**（coauthor_producer_ids）
- 可寫成 launchd 定時排程

### 前提 + 缺點
- 需要 Developer App（developers.facebook.com）一次建 · 大概 15 分
- Access Token 60 天要 refresh（可自動化）
- Video 要 publicly accessible URL（Cloudflare R2 或 GitHub Pages）
- 一次性 setup 成本高但永久用

### 推薦用法
**長期方案 · 跟路徑 1 搭配** · 先用 Business Suite 短期 · 空時把 Graph API pipeline 寫完

---

## 路徑 4 · 付費排程器（Later / Buffer / Publer / SocialPilot）

付費（$15-99/月），不推。免費替代品（路徑 1、2）已夠。

---

## 路徑 5 · Appium wireless iPhone（昨晚 + 今早設好）

### 現狀
- Appium server + WDA + wireless pairing 全通 ✓（今早驗證）
- UI flow probe 到 step 5（home → create → REEL → video → Next x2 → caption page）✓
- **Schedule button 位置未 probe 完**（在 share sheet 需要 scroll）

### 為什麼不推
- 需要 iPhone 在家同 WiFi
- Jamie 出門 iPhone 帶走就斷
- 即使 iPhone 留家 · 家裡停電 / iPhone 關機 / WiFi 斷 · 04/20 21:00 就發不出去
- 比路徑 1 脆弱

### 繼續 iterate 價值
有 — 作為**備援**（路徑 1 如遇限制時用）· 下週有空再 probe 完 Schedule 邏輯存為 skill

---

## 路徑 6-8 · 不推原因

- **instagrapi**：2FA TOTP 被 IG 2024 anti-bot reject（昨晚試過）
- **IG Web automation**：Create menu 2024 後不給 Reel option（已確認）
- **Android Emulator**：同一 IG 帳號多裝置登入會被 IG 風控警告 / 封號

---

## 路徑 9 · iPhone App 內建 Schedule（手動 60 秒）

你已經會做 · 不多說 · fallback 永遠可用

---

## 🎯 建議執行順序

### 今天 Jamie 回家後（5-10 分鐘）
1. **確認 IG @jamie_wu_1012 帳號類型**（Settings → Account → Account Type）· 應該已是 Creator 或 Business · 如還是 Personal 轉
2. **確認有 FB 粉專**（facebook.com/pages）· 如沒有快速建一個 repurre Studio 粉專
3. **IG 連 FB 粉專**（IG Settings → Linked Accounts → Facebook）

### 今天之後 Claude 接手
1. Mac 瀏覽器登入 Jamie FB（她授權 or Keychain 提供）
2. 測試 business.facebook.com Planner → Create Reel → 上傳 + 排程 04/20 21:00 手動走一次驗證
3. 寫 Playwright script 自動化這個 flow · 每週 Reel 一指令排程
4. （空檔）寫 Graph API pipeline 作為長期方案

### 今晚立即（Jamie 出門期間 · 等她回來）
- Claude 繼續：
  - **把 Appium ig-reel-appium.py 的 5-step 通路存好**（昨晚 probe 成果保存）
  - **準備 Playwright Business Suite 腳本骨架**（等 Jamie 回家 login 就能跑）
  - **確認 04/20 fallback**：ig-reel-remind-20260420 launchd 20:55 推提醒 · 最差 Jamie 手動發

---

## 04/20 21:00 Reel 決策

**優先順序**

1. 🥇 Jamie 今天回家 5 分鐘 setup Business Suite（IG/FB 連結+登入）→ Claude Playwright 排程 04/20 → 完全 Mac 自動
2. 🥈 Jamie 回家 iPhone 留家 WiFi · Claude 跑完 Appium probe → 04/20 Appium 排程
3. 🥉 Jamie 回家 iPhone 手動 60 秒排程到 04/20（穩到不行但要她動手）
4. 最差 20:55 Telegram 提醒 Jamie 手動 5 分鐘發

**我的推薦**：#1 Business Suite · 後續 04/23 / 04/25 全自動 · 這週清理完 Appium 不用再撞牆

---

## 附錄 · Meta Business Suite 常見坑

1. **要有 FB 粉專** — 不能用個人 FB 排 IG
2. **IG 必須 Professional 且連到 FB 粉專** — 去 IG Settings 連一次
3. **IG 帳號受限於某些違規**時 Business Suite 會禁止 publishing（Jamie 帳號歷史乾淨應該沒事）
4. **上傳影片格式**：MP4 · 3-90 秒 · 建議 9:16 1080x1920
5. **排程最遠 75 天內** · 夠用
6. **排程後可修改 / 取消** 直到發送前

---

## 來源

- [Meta Business Suite 官方幫助 - Create and Manage Reels](https://www.facebook.com/business/help/794942355314453)
- [Instagram Graph API 2026 開發者指南](https://elfsight.com/blog/instagram-graph-api-complete-developer-guide-for-2026/)
- [Meta Creator Studio 已併入 Business Suite](https://manychat.com/blog/instagram-creator-studio-part-of-meta-business-suite/)
- [Metricool Reels 排程教學](https://metricool.com/schedule-reels-with-metricool/)
- [Metricool 免費 50 posts/月](https://metricool.com/premium-vs-free-metricool-plans/)
- [Instagram API Pricing / 免費 tier](https://www.getphyllo.com/post/instagram-api-pricing-explained-iv)
- [2026 IG 排程器 Top 12](https://postplanify.com/blog/instagram-post-scheduler-tools-2025)

---

## Claude 行動 check list · Jamie 回家後 1 次執行

- [ ] Jamie 確認 IG @jamie_wu_1012 是 Creator 或 Business
- [ ] Jamie 確認有 FB 粉專（如無建立 repurre Studio）
- [ ] Jamie IG Settings → Linked Accounts → Facebook 連一次
- [ ] Jamie Mac 瀏覽器登 FB（Safari / Chrome）
- [ ] Claude 開 business.facebook.com 走一次排程手動驗證
- [ ] Claude 寫 `~/.claude/scripts/ig-post/reel-schedule-via-business-suite.py`（Playwright）
- [ ] Claude 04/20 Reel 用此 script 排程
- [ ] Claude 排 launchd `com.repurre.ig-reel-auto-weekly` · 每週抓素材自動排
- [ ] （空檔）Claude 寫 Graph API 備援 pipeline
