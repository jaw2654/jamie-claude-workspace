/**
 * repurre assessment auto-responder · Google Apps Script Web App
 *
 * 功能：
 * 1. 接收 assessment 頁 POST（email + level + score）
 * 2. 根據等級 A/B/C/D 寄對應客製 email 給使用者
 * 3. 同時寄通知給 Jamie（jaw2654@gmail.com）
 * 4. Log 到 Google Sheet（可選）
 *
 * 部署步驟：
 * 1. 到 https://script.google.com 開新專案
 * 2. 貼上此整份 code
 * 3. 檔案 → 儲存，專案命名「repurre assessment autoresponder」
 * 4. 部署 → 新增部署作業 → 類型選「網頁應用程式」
 * 5. 執行身分：我（jaw2654@gmail.com）· 存取權：所有人
 * 6. 複製 Web App URL（格式 https://script.google.com/macros/s/AKfycbx.../exec）
 * 7. 貼進 assessment.html 的 ENDPOINT 常數
 */

const JAMIE_EMAIL = 'jaw2654@gmail.com';
const BRAND_FROM = 'Jamie @ repurre';
const TG_BOT_TOKEN = '8754872172:AAFSRJuneA12RZAbyfn38h3XDEq5uN9MPQk';
const TG_CHAT_ID = '8708811744';

function doPost(e) {
  try {
    // 支援兩種格式：form-urlencoded（e.parameter）和 JSON（e.postData.contents）
    // 前端用 URLSearchParams 避開 CORS preflight
    let data;
    if (e.parameter && e.parameter.email) {
      data = e.parameter;
    } else {
      data = JSON.parse(e.postData.contents);
    }
    const { email, level, score } = data;

    if (!email || !email.includes('@')) {
      return jsonResponse({ ok: false, error: 'invalid_email' });
    }

    // 1. 寄客製 email 給使用者
    const template = EMAIL_TEMPLATES[level] || EMAIL_TEMPLATES.C;
    MailApp.sendEmail({
      to: email,
      subject: template.subject,
      htmlBody: template.html,
      name: BRAND_FROM,
    });

    // 2. 通知 Jamie（走 Telegram，不走 Email）
    const ts = Utilities.formatDate(new Date(), 'Asia/Taipei', 'yyyy-MM-dd HH:mm');
    const tgText = `新 assessment 提交\n\n等級: ${level}\n總分: ${score}/50\nEmail: ${email}\n時間: ${ts}\n\n建議 24h 內親自聯絡。`;
    UrlFetchApp.fetch(`https://api.telegram.org/bot${TG_BOT_TOKEN}/sendMessage`, {
      method: 'post',
      payload: { chat_id: TG_CHAT_ID, text: tgText },
      muteHttpExceptions: true,
    });

    return jsonResponse({ ok: true });
  } catch (err) {
    return jsonResponse({ ok: false, error: String(err) });
  }
}

function doOptions() {
  return jsonResponse({ ok: true });
}

function jsonResponse(obj) {
  return ContentService
    .createTextOutput(JSON.stringify(obj))
    .setMimeType(ContentService.MimeType.JSON);
}

// ==== 4 個等級 email 模板 ====

const BASE_STYLE = `
  <div style="max-width:560px;margin:0 auto;font-family:'Noto Sans TC','PingFang TC',sans-serif;line-height:1.8;color:#2a2521;background:#ebe2cf;padding:40px 24px;">
    <div style="font-family:'Noto Serif TC',serif;font-size:24px;letter-spacing:0.02em;text-align:center;margin-bottom:8px;">
`;
const BASE_END = `
      <p style="text-align:center;color:rgba(42,37,33,0.5);font-size:13px;margin-top:40px;">jamie wu · repurre studio · 台北大安<br>est. 2014 · 十二年私教</p>
    </div>
  </div>
`;

const EMAIL_TEMPLATES = {
  A: {
    subject: '妳的身體自測結果：A 等級 · repurre',
    html: BASE_STYLE + `身體自測結果</div>
      <p style="text-align:center;font-family:Georgia,serif;font-style:italic;font-size:72px;color:#2a2521;margin:20px 0 4px;">A</p>
      <p style="text-align:center;color:rgba(42,37,33,0.5);font-size:13px;margin-bottom:32px;">妳的等級</p>
      <p style="font-weight:700;font-size:18px;margin-bottom:16px;">基礎很好，可以開始進階了。</p>
      <p>妳的底子扎實。這個階段應該做的是：</p>
      <ul>
        <li>增加訓練強度（重量 / 組數）</li>
        <li>嘗試更複合的動作（槓鈴硬舉、引體向上）</li>
        <li>把訓練規劃得更系統化</li>
      </ul>
      <p style="margin-top:24px;">妳需要的是方向跟計畫，不是從零開始。大部分 30+ 女生做不到 A 等級——這個層級的調整反而只有教練才看得出來。</p>
      <p style="margin-top:24px;padding:18px 22px;background:#2a2521;color:#ebe2cf;border-radius:3px;">
        <strong>60 分鐘深度評估</strong>可以精準找出：動作模式的微小代償、左右失衡、最該優先解的限制因素。A 等級的人進步會卡在「看不到的細節」——這是教練的價值所在。
      </p>
      <p style="text-align:center;margin-top:28px;"><a href="https://docs.google.com/forms/d/e/1FAIpQLSdtEPcyinNocJmFpAzgzu2WTyd9o-IN71xyKLatlYEPQ5lH1g/viewform" style="display:inline-block;padding:14px 28px;background:#2a2521;color:#ebe2cf;text-decoration:none;border-radius:2px;font-weight:700;">預約 60 分鐘深度評估 →</a></p>
    ` + BASE_END,
  },
  B: {
    subject: '妳的身體自測結果：B 等級 · repurre',
    html: BASE_STYLE + `身體自測結果</div>
      <p style="text-align:center;font-family:Georgia,serif;font-style:italic;font-size:72px;color:#2a2521;margin:20px 0 4px;">B</p>
      <p style="text-align:center;color:rgba(42,37,33,0.5);font-size:13px;margin-bottom:32px;">妳的等級</p>
      <p style="font-weight:700;font-size:18px;margin-bottom:16px;">有底子，但某些面向明顯弱。</p>
      <p>妳有一定基礎，但 10 項裡通常有 3-5 項拖後腿。可能是：</p>
      <ul>
        <li>活動度不足（肩胛 / 髖 / 踝）</li>
        <li>核心穩定度弱</li>
        <li>單邊不平衡（左右差異）</li>
      </ul>
      <p style="margin-top:24px;">重點是：找到弱項優先補，訓練效率會差很多。亂練反而會讓強的更強、弱的更弱，最後容易卡關或受傷。</p>
      <p style="margin-top:24px;padding:18px 22px;background:#2a2521;color:#ebe2cf;border-radius:3px;">
        <strong>60 分鐘深度評估</strong>可以精準找出妳的弱項 + 給妳接下來 3 個月的訓練優先順序。不需要砍掉重練——只需要把時間花在對的地方。
      </p>
      <p style="text-align:center;margin-top:28px;"><a href="https://docs.google.com/forms/d/e/1FAIpQLSdtEPcyinNocJmFpAzgzu2WTyd9o-IN71xyKLatlYEPQ5lH1g/viewform" style="display:inline-block;padding:14px 28px;background:#2a2521;color:#ebe2cf;text-decoration:none;border-radius:2px;font-weight:700;">預約 60 分鐘深度評估 →</a></p>
    ` + BASE_END,
  },
  C: {
    subject: '妳的身體自測結果：C 等級 · repurre',
    html: BASE_STYLE + `身體自測結果</div>
      <p style="text-align:center;font-family:Georgia,serif;font-style:italic;font-size:72px;color:#2a2521;margin:20px 0 4px;">C</p>
      <p style="text-align:center;color:rgba(42,37,33,0.5);font-size:13px;margin-bottom:32px;">妳的等級</p>
      <p style="font-weight:700;font-size:18px;margin-bottom:16px;">身體在提醒妳：該系統性重建了。</p>
      <p>不是因為老了——是太久沒有好好練。這個階段最怕的是「自己亂練」：</p>
      <ul>
        <li>網路教學一堆，但每個人身體狀況不一樣</li>
        <li>適合別人的動作不一定適合妳</li>
        <li>用錯方式會讓代償更嚴重，甚至受傷</li>
      </ul>
      <p style="margin-top:24px;">C 等級最該做的事就是找教練做一次完整評估。先知道自己「不能做什麼」比先做什麼重要得多。</p>
      <p style="margin-top:24px;padding:18px 22px;background:#2a2521;color:#ebe2cf;border-radius:3px;">
        <strong>60 分鐘深度評估</strong>會幫妳畫出起跑線：<br>· 哪些動作現在可以做<br>· 哪些要先避開<br>· 第一個月應該專注什麼<br><br>安全比快速更重要。
      </p>
      <p style="text-align:center;margin-top:28px;"><a href="https://docs.google.com/forms/d/e/1FAIpQLSdtEPcyinNocJmFpAzgzu2WTyd9o-IN71xyKLatlYEPQ5lH1g/viewform" style="display:inline-block;padding:14px 28px;background:#2a2521;color:#ebe2cf;text-decoration:none;border-radius:2px;font-weight:700;">預約 60 分鐘深度評估 →</a></p>
    ` + BASE_END,
  },
  D: {
    subject: '妳的身體自測結果：D 等級 · repurre',
    html: BASE_STYLE + `身體自測結果</div>
      <p style="text-align:center;font-family:Georgia,serif;font-style:italic;font-size:72px;color:#2a2521;margin:20px 0 4px;">D</p>
      <p style="text-align:center;color:rgba(42,37,33,0.5);font-size:13px;margin-bottom:32px;">妳的等級</p>
      <p style="font-weight:700;font-size:18px;margin-bottom:16px;">行動力正在流失，但現在開始永遠不會太晚。</p>
      <p>每拖一年，要花的力氣就多一倍。但好消息是：</p>
      <ul>
        <li>只要開始練、有人帶，3 個月就會有明顯差別</li>
        <li>妳不用怕起點低——我帶過的學員很多人從這裡開始</li>
        <li>重點不是妳現在在哪，是妳願不願意動</li>
      </ul>
      <p style="margin-top:24px;">D 等級不是壞事，是數據。妳現在知道自己需要專業的協助，這比大部分還在假裝沒問題的人強。</p>
      <p style="margin-top:24px;padding:18px 22px;background:#2a2521;color:#ebe2cf;border-radius:3px;">
        <strong>60 分鐘深度評估</strong>會幫妳從零規劃：<br>· 找出最安全的起點<br>· 給妳可以持續 6 個月的計畫<br>· 建立可追蹤的進度指標
      </p>
      <p style="text-align:center;margin-top:28px;"><a href="https://docs.google.com/forms/d/e/1FAIpQLSdtEPcyinNocJmFpAzgzu2WTyd9o-IN71xyKLatlYEPQ5lH1g/viewform" style="display:inline-block;padding:14px 28px;background:#2a2521;color:#ebe2cf;text-decoration:none;border-radius:2px;font-weight:700;">預約 60 分鐘深度評估 →</a></p>
    ` + BASE_END,
  },
};
