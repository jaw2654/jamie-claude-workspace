// ============================================================
// repurre 體驗評估表單 · 精簡 5 題版（2026-04-20 Jamie 指示降門檻）
// ============================================================
// 舊 19 題版本：update_form.gs.bak-19q-20260420 · 體驗課前一週用
// 此版：第一道漏斗 · 5 題 · 減 friction
//
// 執行方式：
// 1. 開啟 https://script.google.com/
// 2. 編輯區貼上這整段程式（Cmd+A 全選 → Cmd+V）
// 3. 按 ▷ 執行 updateRepurreForm5Q
// ============================================================

var FORM_ID = '1-kr5Jq3TaevBLzwQjLKfrXqrDbEH2VXgaAeqzzL8mTc';

function updateRepurreForm5Q() {
  var form = FormApp.openById(FORM_ID);

  // 清空所有現有題目
  var items = form.getItems();
  for (var i = items.length - 1; i >= 0; i--) {
    form.deleteItem(items[i]);
  }

  // 標題 + 簡短說明
  form.setTitle('repurre｜60 分鐘身體深度評估預約');
  form.setDescription(
    '嗨，我是 Jamie 🤍\n\n' +
    '這不是一般的體驗課。這是一次 60 分鐘、1 對 1 的身體深度對話。\n\n' +
    '60 分鐘後，你會帶走：\n' +
    '• 身體現況藍圖\n' +
    '• 客製化訓練方向 × 飲食建議\n' +
    '• 未來 6-12 個月身體可以怎麼走\n\n' +
    '只問你 5 題 · 2 分鐘填完。'
  );

  // Q1 姓名
  form.addTextItem()
      .setTitle('姓名')
      .setRequired(true);

  // Q2 為什麼是現在
  form.addParagraphTextItem()
      .setTitle('為什麼是現在想來？')
      .setHelpText('不用完美答案 · 就講你此刻的真實想法。')
      .setRequired(true);

  // Q3 1 年後的自己
  form.addParagraphTextItem()
      .setTitle('1 年後你想變成什麼樣子？')
      .setHelpText('可以是身體、生活、能力、或任何你在意的面向。')
      .setRequired(true);

  // Q4 每週願意固定嗎
  var q4 = form.addMultipleChoiceItem();
  q4.setTitle('你每週願意固定來 2-3 次訓練嗎？')
    .setChoices([
      q4.createChoice('願意 · 我已經準備好把訓練放進行事曆'),
      q4.createChoice('願意 · 但需要 Jamie 幫我看時間怎麼排'),
      q4.createChoice('想先做 1 次體態評估再決定')
    ])
    .setRequired(true);

  // Q5 聯絡方式
  form.addTextItem()
      .setTitle('LINE ID 或手機號碼')
      .setHelpText('Jamie 會在 24 小時內 LINE 或電話回覆你預約時段。')
      .setRequired(true);

  Logger.log('✓ 5 題版表單更新完成');
  Logger.log('URL: ' + form.getPublishedUrl());
}
