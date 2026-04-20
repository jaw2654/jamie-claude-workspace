// Cloudflare Pages advanced mode Worker
// Routes /api/assessment to email handler, everything else → static assets

export default {
  async fetch(request, env, ctx) {
    const url = new URL(request.url);

    if (url.pathname === '/api/assessment') {
      return handleAssessment(request, env);
    }

    return env.ASSETS.fetch(request);
  },
};

async function handleAssessment(request, env) {
  // CORS preflight
  if (request.method === 'OPTIONS') {
    return new Response(null, {
      headers: corsHeaders(),
    });
  }

  if (request.method !== 'POST') {
    return json({ ok: false, error: 'method_not_allowed' }, 405);
  }

  try {
    const body = await request.json();
    const { email, level, score } = body;

    if (!email || !email.includes('@')) {
      return json({ ok: false, error: 'invalid_email' }, 400);
    }

    const lvl = (level || 'C').toUpperCase();
    const template = TEMPLATES[lvl] || TEMPLATES.C;

    // 1. Send to user via MailChannels (Cloudflare's free email relay)
    const userEmail = {
      personalizations: [{ to: [{ email }] }],
      from: {
        email: 'hello@repurre-reports.pages.dev',
        name: 'Jamie @ repurre',
      },
      reply_to: { email: 'jaw2654@gmail.com', name: 'Jamie Wu' },
      subject: template.subject,
      content: [{ type: 'text/html', value: template.html }],
    };

    const userRes = await fetch('https://api.mailchannels.net/tx/v1/send', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(userEmail),
    });

    const userOk = userRes.ok;

    // 2. Also notify Jamie via Telegram
    try {
      const token = '8754872172:AAFSRJuneA12RZAbyfn38h3XDEq5uN9MPQk';
      const chatId = '8708811744';
      const ts = new Date().toLocaleString('zh-TW', { timeZone: 'Asia/Taipei' });
      const msg = `📋 新 assessment 提交\n\n等級: ${lvl}\n總分: ${score || '?'} / 50\nEmail: ${email}\n時間: ${ts}\n自動信: ${userOk ? '✓ 已寄' : '✗ 失敗'}`;
      await fetch(`https://api.telegram.org/bot${token}/sendMessage`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ chat_id: chatId, text: msg }),
      });
    } catch (e) {
      // ignore
    }

    if (!userOk) {
      const errText = await userRes.text();
      return json({ ok: false, error: 'email_send_failed', detail: errText }, 500);
    }

    return json({ ok: true });
  } catch (err) {
    return json({ ok: false, error: 'server_error', message: String(err) }, 500);
  }
}

function json(obj, status = 200) {
  return new Response(JSON.stringify(obj), {
    status,
    headers: { 'Content-Type': 'application/json', ...corsHeaders() },
  });
}

function corsHeaders() {
  return {
    'Access-Control-Allow-Origin': '*',
    'Access-Control-Allow-Methods': 'POST, OPTIONS',
    'Access-Control-Allow-Headers': 'Content-Type',
  };
}

// ==== Email Templates ====

const FORM_URL =
  'https://docs.google.com/forms/d/e/1FAIpQLSdtEPcyinNocJmFpAzgzu2WTyd9o-IN71xyKLatlYEPQ5lH1g/viewform';

function baseHtml(level, title, body, cta) {
  return `<!doctype html>
<html><body style="margin:0;padding:0;background:#ebe2cf;font-family:'Noto Sans TC','PingFang TC',sans-serif;color:#2a2521;">
<div style="max-width:560px;margin:0 auto;padding:40px 24px;">
  <p style="text-align:center;font-family:'Times New Roman',serif;font-style:italic;font-size:15px;color:rgba(42,37,33,0.6);letter-spacing:0.1em;margin:0 0 20px;">a note from jamie</p>
  <p style="text-align:center;font-family:'Times New Roman',serif;font-style:italic;font-size:96px;color:#2a2521;margin:0;line-height:1;">${level}</p>
  <p style="text-align:center;color:rgba(42,37,33,0.5);font-size:13px;letter-spacing:0.15em;text-transform:uppercase;margin:4px 0 32px;">妳的等級</p>
  <p style="font-size:22px;font-weight:700;line-height:1.5;margin:0 0 20px;">${title}</p>
  <div style="font-size:15.5px;line-height:1.85;color:rgba(42,37,33,0.82);">${body}</div>
  <div style="background:#2a2521;color:#ebe2cf;padding:22px 24px;border-radius:3px;margin:32px 0;">
    ${cta}
  </div>
  <p style="text-align:center;margin:28px 0;">
    <a href="${FORM_URL}" style="display:inline-block;padding:16px 32px;background:#2a2521;color:#ebe2cf;text-decoration:none;border-radius:2px;font-weight:700;letter-spacing:0.02em;">預約 60 分鐘深度評估 →</a>
  </p>
  <p style="text-align:center;color:rgba(42,37,33,0.5);font-family:'Times New Roman',serif;font-style:italic;font-size:14px;margin-top:48px;padding-top:24px;border-top:1px solid rgba(42,37,33,0.14);">jamie wu · repurre studio · 台北大安<br>est. 2014 · 十二年私教</p>
</div>
</body></html>`;
}

const TEMPLATES = {
  A: {
    subject: '妳的身體自測結果 · A 等級 · repurre',
    html: baseHtml(
      'A',
      '基礎很好，可以開始進階了。',
      `<p>妳的底子扎實。這個階段應該做的是：</p>
       <ul style="padding-left:20px;line-height:1.85;">
         <li>增加訓練強度（重量 / 組數）</li>
         <li>嘗試更複合的動作（槓鈴硬舉、引體向上）</li>
         <li>把訓練規劃得更系統化</li>
       </ul>
       <p style="margin-top:20px;">妳需要的是方向跟計畫，不是從零開始。大部分 30+ 女生做不到 A 等級——這個層級的調整反而只有教練才看得出來。</p>`,
      `<p style="margin:0;line-height:1.75;"><strong style="background:rgba(235,226,207,0.15);padding:2px 6px;border-radius:2px;">60 分鐘深度評估</strong>會看得更仔細：動作模式的微小代償、左右失衡、最該優先解的限制因素。A 等級的進步會卡在「看不到的細節」——這是教練的價值所在。</p>`,
    ),
  },
  B: {
    subject: '妳的身體自測結果 · B 等級 · repurre',
    html: baseHtml(
      'B',
      '有底子，但某些面向明顯弱。',
      `<p>妳有一定基礎，但 10 項裡通常有 3-5 項拖後腿。可能是：</p>
       <ul style="padding-left:20px;line-height:1.85;">
         <li>活動度不足（肩胛 / 髖 / 踝）</li>
         <li>核心穩定度弱</li>
         <li>單邊不平衡（左右差異）</li>
       </ul>
       <p style="margin-top:20px;">重點是：找到弱項優先補，訓練效率會差很多。亂練反而會讓強的更強、弱的更弱，最後容易卡關或受傷。</p>`,
      `<p style="margin:0;line-height:1.75;"><strong style="background:rgba(235,226,207,0.15);padding:2px 6px;border-radius:2px;">60 分鐘深度評估</strong>可以精準找出妳的弱項 + 給妳接下來 3 個月的訓練優先順序。不需要砍掉重練——只需要把時間花在對的地方。</p>`,
    ),
  },
  C: {
    subject: '妳的身體自測結果 · C 等級 · repurre',
    html: baseHtml(
      'C',
      '身體在提醒妳：該系統性重建了。',
      `<p>不是因為老了——是太久沒有好好練。這個階段最怕的是「自己亂練」：</p>
       <ul style="padding-left:20px;line-height:1.85;">
         <li>網路教學一堆，但每個人身體狀況不一樣</li>
         <li>適合別人的動作不一定適合妳</li>
         <li>用錯方式會讓代償更嚴重，甚至受傷</li>
       </ul>
       <p style="margin-top:20px;">C 等級最該做的事就是找教練做一次完整評估。先知道自己「不能做什麼」比先做什麼重要得多。</p>`,
      `<p style="margin:0 0 10px;line-height:1.75;"><strong style="background:rgba(235,226,207,0.15);padding:2px 6px;border-radius:2px;">60 分鐘深度評估</strong>會幫妳畫出起跑線：</p>
       <p style="margin:0;line-height:1.85;">· 哪些動作現在可以做<br>· 哪些要先避開<br>· 第一個月應該專注什麼</p>
       <p style="margin:12px 0 0;">安全比快速更重要。</p>`,
    ),
  },
  D: {
    subject: '妳的身體自測結果 · D 等級 · repurre',
    html: baseHtml(
      'D',
      '行動力正在流失，但現在開始永遠不會太晚。',
      `<p>每拖一年，要花的力氣就多一倍。但好消息是：</p>
       <ul style="padding-left:20px;line-height:1.85;">
         <li>只要開始練、有人帶，3 個月就會有明顯差別</li>
         <li>妳不用怕起點低——我帶過的學員很多人從這裡開始</li>
         <li>重點不是妳現在在哪，是妳願不願意動</li>
       </ul>
       <p style="margin-top:20px;">D 等級不是壞事，是數據。妳現在知道自己需要專業的協助，這比大部分還在假裝沒問題的人強。</p>`,
      `<p style="margin:0 0 10px;line-height:1.75;"><strong style="background:rgba(235,226,207,0.15);padding:2px 6px;border-radius:2px;">60 分鐘深度評估</strong>會幫妳從零規劃：</p>
       <p style="margin:0;line-height:1.85;">· 找出最安全的起點<br>· 給妳可以持續 6 個月的計畫<br>· 建立可追蹤的進度指標</p>`,
    ),
  },
};
