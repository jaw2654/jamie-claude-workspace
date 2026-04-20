# repurre Health Studio — Claude 專案記憶

## 使用者資訊
- **姓名**：Jamie Wu（吳采盈）
- **身份**：repurre Health Studio 教練 + TopstepX 期貨交易員
- **Email（工作）**：jaw2654@gmail.com
- **行事曆**：repurre2022@gmail.com（Google Calendar）

## Telegram Bot
- **Token**：`8754872172:AAFSRJuneA12RZAbyfn38h3XDEq5uN9MPQk`
- **Chat ID**：`8708811744`
- **Bot 名稱**：Jamie studio bot
- **方式**：Claude Telegram Plugin（原生整合，不需要 daemon）

## 交易帳戶
- **平台**：TopstepX
- **帳號**：TOPX5008
- **Account ID**：20524025
- **品種**：YM 道瓊 E-mini（$5/點）
- **Tradezella**：https://app.tradezella.com/tracking/trades/a123e0c1

## 排程任務（2 個）
| 任務名稱 | Cron | 說明 |
|---------|------|------|
| morning-briefing-daily | `0 8 * * 1-5` | 週一至五 08:00 每日晨報 |
| weekly-data-report | `0 18 * * 0` | 週日 18:00 週數據報告 |

## 資料夾結構（Claude cowork/工作文件/）
```
工作文件/
├── 每日簡報/     ← 晨報 morning-briefing-YYYY-MM-DD.html
│                    盤後 evening-review-YYYY-MM-DD.html
├── 週報/         ← 週報 weekly-report-YYYY-MM-DD-v2.html
├── 交易日誌/     ← 交易日誌 trading-journal-YYYY-MM-DD.html
└── ...
```

## SSH 連線
- **筆電 IP**：192.168.10.236
- **SSH 金鑰**：已設定 key-based 認證（desktop ↔ laptop）

## Telegram 使用方式
透過 Claude Telegram Plugin 直接雙向溝通，不需要額外 daemon。
Jamie 可直接在 Telegram 傳訊息給 Claude，Claude 也可以主動推播。

## 注意事項
- Gmail MCP 只有 `create_draft`，沒有 send 功能
- 個人信箱（repurre2022@gmail.com）無授權，只能用工作帳 jaw2654@gmail.com
