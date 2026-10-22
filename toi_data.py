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


# ---------------------------------------------------------------- interface strings
UI = {
 "en": {"who":"Who we are reaching","runs":"How it runs","sched":"The schedule","pay":"Payable, with tax",
        "net":"Net to the publisher","reach":"Estimated reach","cpm":"Cost per thousand","bonus":"Bonus inventory given",
        "money":"Where the money goes","reachsrc":"Where the reach comes from","settle":"How the money is actually settled",
        "measure":"What we will measure","risk":"The honest risk","whyus":"Why this group and not a platform",
        "line":"Line","qty":"Qty","rate":"Rate","gross":"Gross","why":"Why","detail":"Detail","loading":"Loading",
        "over":"This plan is over the stated budget. Cut insertions or trade a premium position before it goes to the client.",
        "stale":"The plan on screen was written in another language. Press build to rewrite it.",
        "whyus_body":"Platform money buys impressions. This buys the one thing a platform cannot sell, which is the judgement of a newsroom the reader already trusts, in the language they actually read."},
 "ja": {"who":"ターゲット","runs":"進行","sched":"掲載スケジュール","pay":"税込 支払額",
        "net":"媒体社への正味額","reach":"推定リーチ","cpm":"千人あたり単価","bonus":"ボーナス枠の提供",
        "money":"費用の配分","reachsrc":"リーチの内訳","settle":"精算の流れ",
        "measure":"測定指標","risk":"想定されるリスク","whyus":"プラットフォームではなく、この媒体を選ぶ理由",
        "line":"項目","qty":"数量","rate":"単価","gross":"総額","why":"理由","detail":"内訳","loading":"割増",
        "over":"予算を超えています。出稿回数を減らすか、プレミアム位置を見直してから提案してください。",
        "stale":"画面の提案書は別の言語で作成されています。作成ボタンを押して再生成してください。",
        "whyus_body":"プラットフォームに払う費用はインプレッションを買うだけです。ここで買えるのは、読者がすでに信頼している編集部の判断を、読者が実際に読む言語で届けることです。"},
 "hi": {"who":"हम किस तक पहुँच रहे हैं","runs":"यह कैसे चलेगा","sched":"शेड्यूल","pay":"कर सहित देय",
        "net":"प्रकाशक को शुद्ध","reach":"अनुमानित पहुँच","cpm":"प्रति हज़ार लागत","bonus":"बोनस इन्वेंटरी",
        "money":"पैसा कहाँ जा रहा है","reachsrc":"पहुँच कहाँ से आ रही है","settle":"भुगतान कैसे तय होता है",
        "measure":"हम क्या मापेंगे","risk":"वास्तविक जोखिम","whyus":"प्लेटफ़ॉर्म नहीं, यह समूह क्यों",
        "line":"मद","qty":"मात्रा","rate":"दर","gross":"सकल","why":"कारण","detail":"विवरण","loading":"लोडिंग",
        "over":"यह योजना बजट से ऊपर है। क्लाइंट को भेजने से पहले इंसर्शन घटाएँ या प्रीमियम पोज़िशन बदलें।",
        "stale":"स्क्रीन पर दिख रही योजना दूसरी भाषा में बनी है। दोबारा बनाने के लिए बिल्ड दबाएँ।",
        "whyus_body":"प्लेटफ़ॉर्म का पैसा सिर्फ़ इम्प्रेशन खरीदता है। यहाँ वह मिलता है जो कोई प्लेटफ़ॉर्म नहीं बेच सकता, यानी उस न्यूज़रूम का भरोसा, उसी भाषा में जिसमें पाठक पढ़ता है।"},
}

# inventory names in each language
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
