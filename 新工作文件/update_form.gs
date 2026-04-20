// ============================================================
// repurre 體驗評估表單｜更新版（加匯款 + 1v1/1v2 + 地址）
// ============================================================
// 執行方式：
// 1. 開啟 https://script.google.com/
// 2. 編輯區貼上這整段程式（Cmd+A 全選 → Cmd+V）
// 3. 按 ▷ 執行 updateRepurreForm
// ============================================================

var FORM_ID = '1-kr5Jq3TaevBLzwQjLKfrXqrDbEH2VXgaAeqzzL8mTc';

function updateRepurreForm() {
  var form = FormApp.openById(FORM_ID);

  // 清空所有現有題目
  var items = form.getItems();
  for (var i = items.length - 1; i >= 0; i--) {
    form.deleteItem(items[i]);
  }

  // 更新標題 + 說明
  form.setTitle('repurre｜60 分鐘身體深度評估預約');

  form.setDescription(
    '嗨，歡迎來到 repurre 🤍\n\n' +
    '這不是一般的「試試看體驗課」。\n' +
    '這是一次 60 分鐘、一對一（或一對二）的身體深度對話。\n\n' +
    '在 repurre，我們相信：\n' +
    '身體不是一個要「管理」的物件，\n' +
    '而是一個需要被「理解」的夥伴。\n\n' +
    '━━━━━━━━━━━━━━━\n\n' +
    '這 60 分鐘，教練會幫你看見：\n' +
    '• 你的身體現在在哪個位置\n' +
    '• 為什麼你容易累、容易痠、動作卡卡\n' +
    '• 你的姿勢、肌力、柔軟度之間的關係\n' +
    '• 飲食和訓練要怎麼配合你的生活\n' +
    '• 未來 6-12 個月，身體可以怎麼走\n\n' +
    '60 分鐘後，你會帶走：\n' +
    '✦ 一份專屬於你的身體現況藍圖\n' +
    '✦ 客製化訓練方向 × 飲食建議 × 下一步課表規劃\n\n' +
    '━━━━━━━━━━━━━━━\n\n' +
    '【費用】\n' +
    '✦ 一對一：NT$ 2,200 / 60 分鐘\n' +
    '✦ 一對二：NT$ 2,800 / 60 分鐘（兩人共用一堂）\n\n' +
    '【匯款資訊】\n' +
    '銀行：永豐銀行（807）\n' +
    '戶名：repurre studio\n' +
    '帳號：19901800449897\n\n' +
    '※ 請在填寫表單前完成匯款，表單最後欄位請填你匯款帳號的「後 5 碼」以利對帳。\n\n' +
    '━━━━━━━━━━━━━━━\n\n' +
    '「健康是以年為單位的事。」\n\n' +
    '如果你是正在認真思考「運動該怎麼走長」的人，\n' +
    '這個評估會是一個很好的起點。\n\n' +
    '如果你還在找「一個月暴瘦 5 公斤、14 天翹臀」之類的方案——\n' +
    '這個評估可能不適合你，\n' +
    '歡迎把時間留給更適合你的教練 🙏\n\n' +
    '━━━━━━━━━━━━━━━\n\n' +
    '填完表單，教練會親自看你寫的每一題，\n' +
    '1-3 個工作天內小編會透過 LINE 或 Email 回你確認時間 🤍'
  );

  form.setCollectEmail(true);

  // ========== 區塊 1：基本資料 ==========
  form.addPageBreakItem().setTitle('① 基本資料');

  form.addTextItem().setTitle('你的名字').setRequired(true);
  form.addDateItem().setTitle('生日').setIncludesYear(true).setRequired(true);
  form.addTextItem().setTitle('手機號碼').setRequired(true);
  form.addTextItem().setTitle('LINE ID').setRequired(true);
  form.addTextItem().setTitle('Instagram 帳號')
    .setHelpText('（例：@jamie_wu_1012，沒有 IG 請填「無」）')
    .setRequired(true);

  form.addMultipleChoiceItem()
    .setTitle('年齡區間')
    .setChoiceValues(['20-29', '30-39', '40-49', '50+'])
    .setRequired(true);

  // ========== 區塊 2：要預約哪種 ==========
  form.addPageBreakItem().setTitle('② 預約方案');

  form.addMultipleChoiceItem()
    .setTitle('你想預約的方案？')
    .setChoiceValues([
      '一對一 NT$ 2,200 / 60 分鐘',
      '一對二 NT$ 2,800 / 60 分鐘（兩人共用一堂）'
    ])
    .setRequired(true);

  form.addTextItem()
    .setTitle('如果是一對二，另一位的名字是？（選填，一對一請填「無」）');

  // ========== 區塊 3：目前的狀態 ==========
  form.addPageBreakItem().setTitle('③ 目前的狀態');

  form.addMultipleChoiceItem()
    .setTitle('你目前的運動頻率？')
    .setChoiceValues([
      '完全沒有運動',
      '偶爾運動（每月 1-3 次）',
      '有固定但不夠（每週 1 次）',
      '每週 2-3 次以上',
      '每天都會動'
    ])
    .setRequired(true);

  form.addMultipleChoiceItem()
    .setTitle('過去有沒有找過教練上 1 對 1 課程？')
    .setChoiceValues([
      '沒有，這是我第一次考慮',
      '有過一次短期（1-3 個月）',
      '有過長期（半年以上）',
      '現在或過去有固定教練'
    ])
    .setRequired(true);

  form.addCheckboxItem()
    .setTitle('目前最在意的身體狀況或體態問題？（可複選）')
    .setChoiceValues([
      '圓肩、駝背、脖子前傾',
      '骨盆前後傾、腰痠',
      '腹直肌分離（產後）',
      '全身肌力不足、爬樓梯會喘',
      '體態鬆散、衣服不合身',
      '過度疲勞、睡不好',
      '體重、體脂',
      '慢性疼痛或運動傷害',
      '更年期相關身體變化'
    ])
    .showOtherOption(true)
    .setRequired(true);

  // ========== 區塊 4：關於你（篩 TA 核心） ==========
  form.addPageBreakItem().setTitle('④ 關於你');

  form.addParagraphTextItem()
    .setTitle('你為什麼「現在」想認真看待自己的身體？')
    .setHelpText('不用寫得完美，寫你真實的想法就好 🤍')
    .setRequired(true);

  form.addParagraphTextItem()
    .setTitle('你希望 1 年後的自己，是什麼樣子？')
    .setRequired(true);

  form.addMultipleChoiceItem()
    .setTitle('你願意把運動當成「每週固定要做的事」嗎？')
    .setChoiceValues([
      '可以，我願意至少每週 1 次、每次 1 小時',
      '可以，但一週 1 次我不確定能堅持',
      '我還在想，先試試看再說',
      '暫時沒辦法，只想先評估一次看看'
    ])
    .setRequired(true);

  // ========== 區塊 5：實務 ==========
  form.addPageBreakItem().setTitle('⑤ 實務');

  form.addCheckboxItem()
    .setTitle('你希望的課程時段？（可複選）')
    .setChoiceValues([
      '平日早上（9-12）',
      '平日下午（13-17）',
      '平日晚上（18-21）',
      '週末白天',
      '週末晚上'
    ])
    .setRequired(true);

  form.addMultipleChoiceItem()
    .setTitle('你住在哪一帶？')
    .setChoiceValues([
      '大安 / 信義 / 松山',
      '中山 / 北投',
      '內湖 / 南港',
      '板橋 / 新店 / 永和',
      '桃園 / 新北其他區',
      '其他縣市',
      '海外'
    ])
    .setRequired(true);

  form.addCheckboxItem()
    .setTitle('你是怎麼認識 repurre 的？（可複選）')
    .setChoiceValues([
      'Instagram',
      'YouTube',
      '朋友推薦',
      'Google 搜尋',
      'Threads',
      'Netflix、文章或其他媒體'
    ])
    .showOtherOption(true)
    .setRequired(true);

  // ========== 區塊 6：匯款 + 最後 ==========
  form.addPageBreakItem().setTitle('⑥ 匯款確認');

  form.addSectionHeaderItem()
    .setTitle('匯款資訊再次提醒')
    .setHelpText(
      '銀行：永豐銀行（807）\n' +
      '戶名：repurre studio\n' +
      '帳號：19901800449897\n\n' +
      '請確認匯款後再送出表單。'
    );

  form.addTextItem()
    .setTitle('請填入你匯款帳號的「後 5 碼」')
    .setHelpText('用來對帳（範例：若帳號為 0123456789，請填 56789）')
    .setRequired(true);

  form.addParagraphTextItem()
    .setTitle('有沒有什麼想讓教練知道的？')
    .setHelpText('例如：身體舊傷、特殊目標、時間限制、生理期狀況等（選填）');

  // 設定送出後的確認訊息（含地址）
  form.setConfirmationMessage(
    '收到了，謝謝你 🤍\n\n' +
    '教練會親自看你寫的每一題，\n' +
    '1-3 個工作天內小編會透過 LINE 或 Email 回你確認時間。\n\n' +
    '━━━━━━━━━━━━━━━\n\n' +
    '📍 repurre Studio\n' +
    '台北市大安區忠孝東路四段 233 號\n\n' +
    '（確認預約後小編會私訊你完整樓層 + 路線）\n\n' +
    '━━━━━━━━━━━━━━━\n\n' +
    '在回覆之前，可以做的 3 件事：\n\n' +
    '1. 追蹤 @jamie_wu_1012 看最近在拍的內容\n' +
    '2. 看一下工作室空間的精選限動\n' +
    '3. 先記下自己最在意的 1-2 個身體狀況，評估那天直接跟教練聊\n\n' +
    'repurre 見 🤍'
  );

  Logger.log('✅ 表單已更新');
  Logger.log('📝 編輯網址：' + form.getEditUrl());
  Logger.log('📤 填寫網址：' + form.getPublishedUrl());
}