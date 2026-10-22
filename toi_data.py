"""
Rate card, loadings and corpus for the Pitch Room prototype.

Everything here is ILLUSTRATIVE and shaped like a real Indian newspaper group's
card so the demo behaves correctly. Replace with the client's own card before
any commercial conversation.

Structure follows how print is genuinely sold in India: a rate per square
centimetre per edition, a size in square centimetres, and a percentage loading
for premium positions and seasons. Digital is sold on CPM. Nothing here is a
flat "full page price", because that is not how a media buyer thinks.
"""

# ---------------------------------------------------------------- print
# rupees per square centimetre, colour, run of paper
PRINT_EDITIONS = {
    "Delhi NCR":   {"rate_sqcm": 3200, "readership": 4_100_000},
    "Mumbai":      {"rate_sqcm": 3500, "readership": 3_600_000},
    "Bengaluru":   {"rate_sqcm": 1900, "readership": 1_500_000},
    "Hyderabad":   {"rate_sqcm": 1500, "readership": 1_100_000},
    "Chennai":     {"rate_sqcm": 1400, "readership": 900_000},
    "Kolkata":     {"rate_sqcm": 1500, "readership": 1_200_000},
    "Pune":        {"rate_sqcm": 1200, "readership": 800_000},
    "Ahmedabad":   {"rate_sqcm": 1100, "readership": 700_000},
}

PRINT_SIZES = {
    "Full page":        1600,
    "Half page":         800,
    "Quarter page":      400,
    "Strip, 8 col x 8":  264,
    "Jacket, both sides": 3200,
}

# percentage added to the base rate
POSITION_LOADING = {
    "Run of paper":        0,
    "Page 5":             20,
    "Page 3":             30,
    "Page 1 solus":       60,
    "Jacket":            100,
}

SEASON_LOADING = {
    "Normal":              0,
    "Festive, Oct to Nov":15,
    "Union budget week":  25,
    "Cricket season":     20,
}

# ---------------------------------------------------------------- digital and group
# cpm in rupees, and an indicative monthly reach per property
DIGITAL = {
    "toi_display":   {"name": "Times of India, display", "cpm": 280,  "pool": 95_000_000},
    "toi_home":      {"name": "Homepage takeover, one day", "flat": 1_800_000, "pool": 6_800_000},
    "et_display":    {"name": "Economic Times, display", "cpm": 520,  "pool": 18_000_000},
    "nbt_display":   {"name": "Navbharat Times, Hindi display", "cpm": 190, "pool": 42_000_000},
    "regional":      {"name": "Regional titles, Marathi, Bengali, Kannada", "cpm": 210, "pool": 28_000_000},
    "video_pre":     {"name": "Video pre roll, premium", "cpm": 450,  "pool": 31_000_000},
    "etimes":        {"name": "ETimes, entertainment", "cpm": 240,    "pool": 22_000_000},
    "newsletter":    {"name": "Newsletter, sole sponsor", "flat": 350_000, "pool": 1_100_000},
    "audio":         {"name": "Radio, host read", "flat": 280_000,    "pool": 2_400_000},
    "tv_spot":       {"name": "News television, 10 second spot", "flat": 160_000, "pool": 3_900_000},
}

# content and events, sold by the branded content desk, not the newsroom
CONTENT = {
    "native":   {"name": "Sponsored article, desk written", "flat": 650_000, "pool": 900_000},
    "series":   {"name": "Editorial series, three parts",   "flat": 1_700_000, "pool": 2_600_000},
    "roundtable": {"name": "Industry roundtable with coverage", "flat": 2_200_000, "pool": 400_000},
    "summit":   {"name": "Summit panel slot and branding",  "flat": 1_500_000, "pool": 600_000},
    "awards":   {"name": "Category sponsorship at awards",  "flat": 3_500_000, "pool": 1_200_000},
}

# ---------------------------------------------------------------- commercial rules
AGENCY_COMMISSION = 0.15   # accredited agency, taken off the gross
PLANNING_FEE = 0.12        # what we charge when there is no agency in the deal
GST_SPACE = 0.05           # advertising space
GST_SERVICE = 0.18         # production, content, events
CREDIT_DAYS = 45
BONUS_INVENTORY = 0.10     # value add usually conceded in negotiation

# ---------------------------------------------------------------- corpus
CORPUS = [
    {"id": "rate",  "title": "Rate card 2026",
     "detail": "Print per square centimetre by edition, digital CPM, content and events",
     "keys": ["rate", "price", "cost", "budget", "media", "print", "digital", "cpm"]},
    {"id": "auto",  "title": "Case: automotive launch",
     "detail": "Japanese carmaker, 2025, eight weeks, eight metros",
     "keys": ["car", "auto", "vehicle", "mobility", "japan", "japanese", "launch", "ev", "suv"]},
    {"id": "fmcg",  "title": "Case: festive FMCG",
     "detail": "Diwali 2025, reach 41 million, print plus regional digital",
     "keys": ["festive", "diwali", "fmcg", "consumer", "retail", "food", "family", "packaged"]},
    {"id": "b2b",   "title": "Case: enterprise software",
     "detail": "Economic Times plus roundtable, 2026, 180 qualified conversations",
     "keys": ["b2b", "software", "saas", "enterprise", "it", "cloud", "technology", "decision"]},
    {"id": "aud",   "title": "Audience study, metros",
     "detail": "Reader profile across eight cities, language and income split",
     "keys": ["audience", "reader", "metro", "city", "urban", "youth", "demographic", "income"]},
    {"id": "brand", "title": "Brand safety and editorial rules",
     "detail": "What the newsroom will not run, and what the branded desk will",
     "keys": ["brand", "safety", "editorial", "compliance", "rules", "guideline", "disclosure"]},
    {"id": "lang",  "title": "Language market note",
     "detail": "Hindi and regional titles outsell English in volume outside the metros",
     "keys": ["hindi", "regional", "language", "bharat", "tier", "vernacular", "marathi", "bengali"]},
]

SAMPLE_BRIEFS = {
    "Japanese carmaker, India entry": (
        "A Japanese automotive manufacturer is bringing its first electric SUV to India in Q1. "
        "They are unknown to Indian families outside a small enthusiast group. They want trust "
        "before volume, and the board is nervous about looking like a foreign import. "
        "Launch in the eight metros first, then tier two cities."
    ),
    "Festive FMCG push": (
        "A packaged foods brand wants the festive quarter. The category is crowded, the product "
        "is mid priced, and the brand already spends heavily on television. They want something "
        "television money cannot buy, aimed at families aged 25 to 45, with strong Hindi presence."
    ),
    "Enterprise software, India": (
        "A global enterprise software company wants technology decision makers in Indian companies "
        "with more than 2,000 staff. The sales cycle is nine months. They care about qualified "
        "conversations rather than impressions, and want thought leadership rather than advertising."
    ),
    "Japanese bank, India corridor": (
        "A Japanese bank is opening a corporate desk in Mumbai to serve Japanese manufacturers "
        "operating in India. The audience is small, senior and hard to reach. Credibility with "
        "Indian corporate finance teams matters more than reach."
    ),
}

# shown when the model is unavailable, so a live demo never breaks
FALLBACK = {
    "en": {
        "title": "Trust before volume",
        "objective": "Make an unknown Japanese carmaker feel familiar to metro families before the first showroom opens.",
        "insight": "Indian families do not buy an unfamiliar car on specification, they buy it on who else they have seen driving one. The job is not awareness, it is permission.",
        "audience": ["Families aged 30 to 45 in the eight metros",
                      "First time electric buyers who already own one car",
                      "Readers who follow business and mobility coverage"],
        "print": [{"edition": "Delhi NCR", "size": "Full page", "position": "Page 3", "insertions": 2,
                   "why": "Arrival signal in the market that decides national coverage"},
                  {"edition": "Mumbai", "size": "Half page", "position": "Run of paper", "insertions": 3,
                   "why": "Sustained presence where the first showrooms open"}],
        "digital": [{"id": "toi_display", "impressions": 9_000_000, "why": "Broad metro cover at low cost"},
                     {"id": "video_pre", "impressions": 3_000_000, "why": "Show the vehicle moving"},
                     {"id": "nbt_display", "impressions": 6_000_000, "why": "Hindi readers the English title misses"}],
        "content": [{"id": "native", "units": 4, "why": "Explain the engineering story in the newsroom voice"},
                     {"id": "roundtable", "units": 1, "why": "Put the India head in front of the mobility press"}],
        "timeline": [{"phase": "Weeks 1 to 2", "action": "Engineering story, sponsored articles live"},
                      {"phase": "Weeks 3 to 5", "action": "Print arrival, homepage bursts, Hindi carry"},
                      {"phase": "Weeks 6 to 8", "action": "Roundtable, video weight, showroom calls to action"}],
        "kpis": ["Unaided brand recall in metros", "Qualified test drive bookings",
                  "Share of mobility conversation against two rivals"],
        "risk": "If the showroom network is not ready in week five, we will have built demand the client cannot serve.",
    },
    "ja": {
        "title": "量より先に、信頼を",
        "objective": "販売店が開く前に、都市部の家族にとって馴染みのある存在にする。",
        "insight": "インドの家族は知らない自動車を仕様では買わない。誰が乗っているかで判断する。必要なのは認知ではなく許可である。",
        "audience": ["八大都市の30代から40代の家族", "すでに一台所有している初めてのEV購入層", "ビジネスとモビリティ記事の読者"],
        "print": [{"edition": "Delhi NCR", "size": "Full page", "position": "Page 3", "insertions": 2,
                   "why": "全国報道を左右する市場での到着の合図"},
                  {"edition": "Mumbai", "size": "Half page", "position": "Run of paper", "insertions": 3,
                   "why": "最初の販売店が開く都市での継続露出"}],
        "digital": [{"id": "toi_display", "impressions": 9_000_000, "why": "都市部を低コストで広く"},
                     {"id": "video_pre", "impressions": 3_000_000, "why": "走行シーンを見せる"},
                     {"id": "nbt_display", "impressions": 6_000_000, "why": "英字紙では届かないヒンディー語読者"}],
        "content": [{"id": "native", "units": 4, "why": "技術の物語を編集部の言葉で"},
                     {"id": "roundtable", "units": 1, "why": "インド代表をモビリティ記者の前に"}],
        "timeline": [{"phase": "第1週から第2週", "action": "技術ストーリーの記事を公開"},
                      {"phase": "第3週から第5週", "action": "新聞広告、トップページ、ヒンディー展開"},
                      {"phase": "第6週から第8週", "action": "ラウンドテーブル、動画強化、来店誘導"}],
        "kpis": ["都市部における純粋想起", "試乗予約の件数", "競合二社に対する話題占有率"],
        "risk": "第5週までに販売網が整わなければ、応えられない需要を作ることになる。",
    },
    "hi": {
        "title": "पहले भरोसा, फिर बिक्री",
        "objective": "शोरूम खुलने से पहले मेट्रो परिवारों के लिए एक अनजान जापानी कार ब्रांड को परिचित बनाना।",
        "insight": "भारतीय परिवार अनजान कार स्पेसिफिकेशन देखकर नहीं खरीदते, वे देखते हैं कि और कौन चला रहा है। काम जागरूकता का नहीं, स्वीकृति का है।",
        "audience": ["आठ मेट्रो शहरों में 30 से 45 वर्ष के परिवार",
                      "पहली बार ईवी खरीदने वाले, जिनके पास पहले से एक कार है",
                      "बिज़नेस और मोबिलिटी पढ़ने वाले पाठक"],
        "print": [{"edition": "Delhi NCR", "size": "Full page", "position": "Page 3", "insertions": 2,
                   "why": "उस बाज़ार में आगमन का संकेत जो राष्ट्रीय कवरेज तय करता है"},
                  {"edition": "Mumbai", "size": "Half page", "position": "Run of paper", "insertions": 3,
                   "why": "जहाँ पहले शोरूम खुल रहे हैं वहाँ लगातार मौजूदगी"}],
        "digital": [{"id": "toi_display", "impressions": 9_000_000, "why": "कम लागत में व्यापक मेट्रो कवर"},
                     {"id": "video_pre", "impressions": 3_000_000, "why": "गाड़ी को चलते हुए दिखाना"},
                     {"id": "nbt_display", "impressions": 6_000_000, "why": "हिंदी पाठक जो अंग्रेज़ी अख़बार तक नहीं आते"}],
        "content": [{"id": "native", "units": 4, "why": "इंजीनियरिंग की कहानी न्यूज़रूम की भाषा में"},
                     {"id": "roundtable", "units": 1, "why": "इंडिया हेड को मोबिलिटी प्रेस के सामने लाना"}],
        "timeline": [{"phase": "सप्ताह 1 से 2", "action": "स्पॉन्सर्ड आर्टिकल लाइव"},
                      {"phase": "सप्ताह 3 से 5", "action": "प्रिंट, होमपेज और हिंदी विस्तार"},
                      {"phase": "सप्ताह 6 से 8", "action": "राउंडटेबल, वीडियो और शोरूम कॉल टू एक्शन"}],
        "kpis": ["मेट्रो में अनएडेड ब्रांड रिकॉल", "टेस्ट ड्राइव बुकिंग",
                  "दो प्रतिद्वंद्वियों के मुकाबले चर्चा में हिस्सा"],
        "risk": "अगर पाँचवें सप्ताह तक डीलर नेटवर्क तैयार नहीं हुआ, तो माँग बनेगी और पूरी नहीं होगी।",
    },
}

LANGS = {"English": "en", "日本語": "ja", "हिन्दी": "hi"}



# ---------------------------------------------------------------- inventory names by language
NAMES = {
 "ja": {"toi_display":"タイムズ・オブ・インディア ディスプレイ","toi_home":"トップページ ジャック 1日",
        "et_display":"エコノミック・タイムズ ディスプレイ","nbt_display":"ナヴバーラト・タイムズ ヒンディー語",
        "regional":"地方紙 マラーティー語 ベンガル語 カンナダ語","video_pre":"動画プレロール プレミアム",
        "etimes":"ETimes エンタメ","newsletter":"ニュースレター 単独協賛","audio":"ラジオ ホストリード",
        "tv_spot":"ニュース番組 10秒スポット","native":"タイアップ記事 編集部制作","series":"編集連載 全3回",
        "roundtable":"業界ラウンドテーブル 記事化込み","summit":"サミット登壇枠","awards":"アワード部門協賛"},
 "hi": {"toi_display":"टाइम्स ऑफ इंडिया, डिस्प्ले","toi_home":"होमपेज टेकओवर, एक दिन",
        "et_display":"इकोनॉमिक टाइम्स, डिस्प्ले","nbt_display":"नवभारत टाइम्स, हिंदी डिस्प्ले",
        "regional":"क्षेत्रीय अख़बार, मराठी बंगाली कन्नड़","video_pre":"वीडियो प्री रोल, प्रीमियम",
        "etimes":"ईटाइम्स, मनोरंजन","newsletter":"न्यूज़लेटर, एकमात्र प्रायोजक","audio":"रेडियो, होस्ट रीड",
        "tv_spot":"न्यूज़ टीवी, 10 सेकंड स्पॉट","native":"स्पॉन्सर्ड आर्टिकल","series":"संपादकीय श्रृंखला, तीन भाग",
        "roundtable":"इंडस्ट्री राउंडटेबल","summit":"समिट पैनल स्लॉट","awards":"अवॉर्ड कैटेगरी प्रायोजन"},
}

def name_for(key, default, lang):
    return NAMES.get(lang, {}).get(key, default)


# ---------------------------------------------------------------- the Japanese working method
PROTOCOL = {
 "en": {
  "tab": "The working method",
  "intro": "Four habits that are ordinary in Japan and rare in this market. They cost nothing and they are the reason a Japanese partner is still there in year five.",
  "nema_h": "Nemawashi, the groundwork before the meeting",
  "nema_s": "Nobody is surprised in the room. Every person who can say no has already been spoken to privately, so the meeting confirms a decision rather than making one.",
  "ringi_h": "Ringi, the circulated approval sheet",
  "ringi_s": "One sheet travels to every approver in order, and each records what they approved. Slower at the start and far faster at the end, because nothing is reopened later.",
  "horen_h": "Horenso, report, contact, consult",
  "horen_s": "We report without being asked, on a fixed day, whether the news is good or bad. No client should ever have to ask how their campaign is doing.",
  "hansei_h": "Hansei kai, the honest review",
  "hansei_s": "At the end we present what did not work before what did, in writing. An agency that only reports wins is managing you, not serving you.",
  "who": "Who", "cares": "What they care about", "ask": "What we ask of them", "when": "When",
  "date": "Date", "what": "What happens", "owner": "Carried by",
  "commit_h": "What we commit to in writing",
  "commits": ["Material delivered before the deadline, never on it",
              "A written report every Monday, unprompted, for the whole campaign",
              "Any overspend flagged before it is incurred, never on the invoice",
              "A closing review that names our own mistakes first"],
 },
 "ja": {
  "tab": "仕事の進め方",
  "intro": "日本では当たり前で、この市場では珍しい四つの習慣です。費用はかかりませんが、五年後も関係が続く理由になります。",
  "nema_h": "根回し 会議前の地ならし",
  "nema_s": "会議の場で驚く人を作らない。反対できる立場の方には事前に個別に説明し、会議は決める場ではなく確認する場にします。",
  "ringi_h": "稟議 回覧による承認",
  "ringi_s": "一枚の書面が順に関係者を回り、それぞれが承認内容を記録します。初めは遅く見えますが、後から蒸し返されないため結果的に速く進みます。",
  "horen_h": "報連相 報告 連絡 相談",
  "horen_s": "良い報せも悪い報せも、決まった曜日に聞かれる前に報告します。お客様が状況を尋ねる必要はありません。",
  "hansei_h": "反省会 率直な振り返り",
  "hansei_s": "終了時には、うまくいった点より先に、うまくいかなかった点を書面で共有します。成果だけを報告する代理店は、仕えているのではなく管理しているだけです。",
  "who": "対象", "cares": "重視される点", "ask": "依頼事項", "when": "時期",
  "date": "日付", "what": "内容", "owner": "担当",
  "commit_h": "書面でお約束すること",
  "commits": ["入稿は締切当日ではなく、締切前に完了します",
              "毎週月曜日、依頼がなくても書面で報告します",
              "予算超過は請求時ではなく、発生前にお知らせします",
              "最終報告では、まず自社の反省点から述べます"],
 },
 "hi": {
  "tab": "काम करने का तरीका",
  "intro": "चार आदतें जो जापान में सामान्य हैं और इस बाज़ार में दुर्लभ। इनकी कोई लागत नहीं, और यही कारण है कि जापानी साझेदार पाँचवें साल भी साथ होता है।",
  "nema_h": "नेमावाशी, बैठक से पहले की ज़मीन तैयार करना",
  "nema_s": "कमरे में कोई चौंके नहीं। जो भी मना कर सकता है, उससे पहले अलग से बात हो चुकी होती है, इसलिए बैठक फ़ैसला लेती नहीं, पुष्टि करती है।",
  "ringi_h": "रिंगी, क्रम से घूमने वाली स्वीकृति शीट",
  "ringi_s": "एक ही शीट हर स्वीकृतिकर्ता तक क्रम से जाती है और हर कोई दर्ज करता है कि उसने क्या मंज़ूर किया। शुरू में धीमा, अंत में बहुत तेज़।",
  "horen_h": "होरेन्सो, रिपोर्ट, संपर्क, परामर्श",
  "horen_s": "हम बिना पूछे, तय दिन पर रिपोर्ट करते हैं, ख़बर अच्छी हो या बुरी। क्लाइंट को कभी पूछना न पड़े कि कैंपेन कैसा चल रहा है।",
  "hansei_h": "हानसेई काई, ईमानदार समीक्षा",
  "hansei_s": "अंत में हम पहले बताते हैं कि क्या नहीं चला, फिर क्या चला, और लिखित में। जो एजेंसी सिर्फ़ जीत बताती है, वह सेवा नहीं, प्रबंधन कर रही है।",
  "who": "कौन", "cares": "किसकी चिंता", "ask": "हम क्या चाहते हैं", "when": "कब",
  "date": "तारीख़", "what": "क्या होगा", "owner": "ज़िम्मेदारी",
  "commit_h": "हम लिखित में क्या वचन देते हैं",
  "commits": ["सामग्री समय सीमा से पहले, उसी दिन नहीं",
              "हर सोमवार लिखित रिपोर्ट, बिना माँगे, पूरे कैंपेन तक",
              "बजट से अधिक ख़र्च बिल में नहीं, होने से पहले बताया जाएगा",
              "समापन समीक्षा में पहले अपनी ग़लतियाँ"],
 },
}

STAKEHOLDERS = {
 "en": [("Brand lead at the advertiser", "Whether the brand looks right", "Agreement on the creative line", "Day 1"),
        ("Marketing procurement", "Rate, payment terms, comparability", "Early sight of the rate basis", "Day 2"),
        ("Publisher ad sales head", "Revenue and inventory yield", "Hold on the premium positions", "Day 3"),
        ("Branded content editor", "That the editorial line is not crossed", "Review of the article angles", "Day 4"),
        ("Legal and compliance", "Disclosure, data, contract", "Sight of the agreement early", "Day 5"),
        ("The formal meeting", "Nothing new, only confirmation", "A decision, not a discussion", "Day 6")],
 "ja": [("広告主のブランド責任者", "ブランドの見え方", "表現方針のご同意", "1日目"),
        ("調達 購買部門", "料率 支払条件 比較可能性", "料率の根拠を事前にご確認", "2日目"),
        ("媒体社 広告営業責任者", "売上と枠の収益性", "プレミアム枠の仮押さえ", "3日目"),
        ("タイアップ編集責任者", "編集の一線を越えないこと", "記事の切り口のご確認", "4日目"),
        ("法務 コンプライアンス", "表示 データ 契約", "契約書の早期ご確認", "5日目"),
        ("正式な会議", "新しい話はせず、確認のみ", "議論ではなく決定", "6日目")],
 "hi": [("विज्ञापनदाता का ब्रांड प्रमुख", "ब्रांड कैसा दिखेगा", "क्रिएटिव दिशा पर सहमति", "दिन 1"),
        ("प्रोक्योरमेंट", "दर, भुगतान शर्तें, तुलना", "दर का आधार पहले दिखाना", "दिन 2"),
        ("प्रकाशक का विज्ञापन प्रमुख", "राजस्व और इन्वेंटरी यील्ड", "प्रीमियम पोज़िशन होल्ड", "दिन 3"),
        ("ब्रांडेड कंटेंट संपादक", "संपादकीय रेखा न लांघी जाए", "आर्टिकल एंगल की समीक्षा", "दिन 4"),
        ("लीगल और कंप्लायंस", "डिस्क्लोज़र, डेटा, अनुबंध", "अनुबंध जल्दी दिखाना", "दिन 5"),
        ("औपचारिक बैठक", "कुछ नया नहीं, केवल पुष्टि", "चर्चा नहीं, निर्णय", "दिन 6")],
}


# ---------------------------------------------------------------- languages
# Full interface translation exists for en, ja and hi. For the others the
# interface falls back to English while the plan itself is written in the
# chosen language, which is what the model is told to do.
LANGUAGES = {
    "English":            ("en", "English"),
    "日本語":              ("ja", "Japanese"),
    "हिन्दी":               ("hi", "Hindi"),
    "简体中文":            ("zh", "Simplified Chinese"),
    "한국어":              ("ko", "Korean"),
    "Bahasa Indonesia":   ("id", "Indonesian"),
    "Tiếng Việt":         ("vi", "Vietnamese"),
    "ไทย":                ("th", "Thai"),
    "Français":           ("fr", "French"),
    "Deutsch":            ("de", "German"),
    "Español":            ("es", "Spanish"),
    "Português":          ("pt", "Portuguese"),
    "العربية":             ("ar", "Arabic"),
}

BRIEFS_I18N = {
 "ja": {
  "Japanese carmaker, India entry":
    "日本の自動車メーカーが、第1四半期にインド初の電気SUVを投入します。一部の愛好家を除き、インドの家庭での認知はほとんどありません。販売台数より先に信頼を得たいと考えており、外資の輸入品に見えることを経営陣が懸念しています。まず八大都市、その後に地方都市へ。",
  "Festive FMCG push":
    "食品メーカーが年末の祭事シーズンを狙っています。競合が多く、価格は中位帯で、テレビ広告にはすでに多額を投じています。テレビでは買えない効果を、25歳から45歳の家族層に向けて求めており、ヒンディー語圏での存在感を重視しています。",
  "Enterprise software, India":
    "外資系のエンタープライズソフトウェア企業が、従業員2,000名以上のインド企業の技術責任者に届きたいと考えています。商談期間は9か月。インプレッション数ではなく、質の高い商談を重視し、広告よりもソートリーダーシップを望んでいます。",
  "Japanese bank, India corridor":
    "日本の銀行が、インドで操業する日系メーカー向けの法人デスクをムンバイに開設します。対象は少数かつ上位層で、到達が困難です。リーチよりも、インド企業の財務部門からの信頼が重要です。",
 },
 "hi": {
  "Japanese carmaker, India entry":
    "एक जापानी वाहन निर्माता पहली तिमाही में भारत में अपनी पहली इलेक्ट्रिक एसयूवी ला रहा है। कुछ शौकीनों को छोड़कर भारतीय परिवारों में ब्रांड अनजान है। वे बिक्री से पहले भरोसा चाहते हैं, और बोर्ड को चिंता है कि कहीं यह विदेशी आयात न लगे। पहले आठ मेट्रो शहर, फिर टियर टू।",
  "Festive FMCG push":
    "एक पैकेज्ड फूड ब्रांड त्योहारी तिमाही चाहता है। श्रेणी में भीड़ है, उत्पाद मध्यम मूल्य का है, और ब्रांड पहले से टेलीविज़न पर भारी ख़र्च करता है। वे वह चाहते हैं जो टीवी का पैसा नहीं ख़रीद सकता, 25 से 45 वर्ष के परिवारों के लिए, मज़बूत हिंदी उपस्थिति के साथ।",
  "Enterprise software, India":
    "एक वैश्विक एंटरप्राइज़ सॉफ़्टवेयर कंपनी 2,000 से अधिक कर्मचारियों वाली भारतीय कंपनियों के तकनीकी निर्णयकर्ताओं तक पहुँचना चाहती है। बिक्री चक्र नौ महीने का है। उन्हें इम्प्रेशन नहीं, गुणवत्ता वाली बातचीत चाहिए, और विज्ञापन से अधिक सोच का नेतृत्व।",
  "Japanese bank, India corridor":
    "एक जापानी बैंक मुंबई में कॉरपोरेट डेस्क खोल रहा है, जो भारत में काम कर रहे जापानी निर्माताओं की सेवा करेगा। दर्शक छोटे, वरिष्ठ और कठिन हैं। पहुँच से अधिक मायने रखती है भारतीय कॉरपोरेट फ़ाइनेंस टीमों की नज़र में विश्वसनीयता।",
 },
}


def briefs_for(lang):
    """Sample briefs in the chosen language, falling back to English."""
    out = dict(SAMPLE_BRIEFS)
    for k, v in BRIEFS_I18N.get(lang, {}).items():
        if k in out:
            out[k] = v
    return out
