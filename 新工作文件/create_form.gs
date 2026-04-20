// ============================================================
// repurre｜60 分鐘身體深度評估預約表單｜一鍵產生器
// ============================================================
// 使用方式：
// 1. 開啟 https://script.google.com/
// 2. 左上角「新增專案」
// 3. 把整份程式碼貼進去（蓋掉原本的）
// 4. 按上方執行鈕 ▷（第一次會要你授權）
// 5. 執行完會在你的 Drive 裡出現新表單 + 試算表
// 6. 執行完在 Logs 會印出表單連結 + 試算表連結
// ============================================================

function createRepurreForm() {
  // 建立表單
  var form = FormApp.create('repurre｜60 分鐘身體深度評估預約');

  form.setDescription(
    '嗨，歡迎來到 repurre 🤍\n\n' +
    '這不是一般的「試試看體驗課」。\n' +
    '這是一次 60 分鐘、一對一的身體深度對話。\n\n' +
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
    '完整評估後你會帶走:\n' +
    '✦ 你專屬的體態報告 PDF（可以一直留著）\n' +
    '✦ 30 天個人化實踐清單\n' +
    '✦ 一週內 LINE 優先問答（課後還能繼續問）\n\n' +
    '━━━━━━━━━━━━━━━\n\n' +
    '✦ 費用：NT$ 2,200\n' +
    '✦ 地點：repurre Health Studio（台北市）\n' +
    '✦ 時長：60 分鐘\n\n' +
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

  // 設定收 Email（個人 Gmail 不支援 setRequireLogin 和 setLimitOneResponsePerUser，所以拿掉）
  form.setCollectEmail(true);

  // ========== 區塊 1：基本資料 ==========
  form.addPageBreakItem().setTitle('① 基本資料');

  form.addTextItem().setTitle('你的名字').setRequired(true);
  form.addTextItem().setTitle('LINE ID（選填，方便之後聯絡）');
  form.addTextItem().setTitle('手機號碼').setRequired(true);

  form.addMultipleChoiceItem()
    .setTitle('年齡')
    .setChoiceValues(['20-29', '30-39', '40-49', '50+'])
    .setRequired(true);

  // ========== 區塊 2：目前的狀態 ==========
  form.addPageBreakItem().setTitle('② 目前的狀態');

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

  // ========== 區塊 3：關於你（篩 TA 核心） ==========
  form.addPageBreakItem().setTitle('③ 關於你');

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

  // ========== 區塊 4：實務 ==========
  form.addPageBreakItem().setTitle('④ 實務');

  form.addCheckboxItem()
    .setTitle('你希望的課程時段？（可複選）')
    .setChoiceValues([
      '平日早上（9-12）',
      '平日下午（13-17）',
      '平日晚上（18-21）',
      '週末白天',
      '週末晚上',
      '線上（海外、外地、或出差多）'
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

  // ========== 區塊 5：最後 ==========
  form.addPageBreakItem().setTitle('⑤ 最後');

  form.addParagraphTextItem()
    .setTitle('有沒有什麼想讓教練知道的？')
    .setHelpText('例如：身體舊傷、特殊目標、時間限制、生理期狀況等（選填）');

  // 設定送出後的確認訊息
  form.setConfirmationMessage(
    '收到了，謝謝你 🤍\n\n' +
    '教練會親自看你寫的每一題，\n' +
    '1-3 個工作天內小編會透過 LINE 或 Email 回你確認時間。\n\n' +
    '━━━━━━━━━━━━━━━\n\n' +
    '在回覆之前，可以做的 3 件事：\n\n' +
    '1. 追蹤 @jamie_wu_1012 看最近在拍的內容\n' +
    '2. 看一下工作室空間的精選限動\n' +
    '3. 先記下自己最在意的 1-2 個身體狀況，評估那天直接跟教練聊\n\n' +
    'repurre 見 🤍'
  );

  // 建立回應試算表
  var ss = SpreadsheetApp.create('repurre 體驗評估回應 - ' +
    Utilities.formatDate(new Date(), 'Asia/Taipei', 'yyyyMMdd'));
  form.setDestination(FormApp.DestinationType.SPREADSHEET, ss.getId());

  // 印出連結
  Logger.log('✅ 表單已建立');
  Logger.log('📝 表單編輯網址：' + form.getEditUrl());
  Logger.log('📤 表單填寫網址（給學生看的）：' + form.getPublishedUrl());
  Logger.log('📊 回應試算表網址：' + ss.getUrl());
}