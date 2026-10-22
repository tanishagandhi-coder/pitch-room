"""
Pitch Room, a Kenja prototype.

A brief goes in. A costed media plan comes out, priced from a rate card rather
than from a language model, in English, Japanese or Hindi.

Run:  streamlit run app.py
"""

import hashlib
import json
import os
import re
from datetime import date, timedelta

import pandas as pd
import streamlit as st

import toi_data as D
from strings import STR
import i18n_extra as X
import landing
from users import ACCOUNTS

st.set_page_config(page_title="Pitch Room", page_icon="📰", layout="wide",
                   initial_sidebar_state="expanded")

MODEL = os.environ.get("PITCHROOM_MODEL", "claude-sonnet-5-5")
RED, NAVY, TEAL, GOLD, PLUM = "#E8491F", "#15110F", "#0F7B6C", "#C98A1F", "#6B3FA0"


# ------------------------------------------------------------------ languages
# Kept here so the app cannot break if toi_data is an older copy.
LANGUAGES = {
    "English": ("en", "English"), "日本語": ("ja", "Japanese"), "हिन्दी": ("hi", "Hindi"),
    "简体中文": ("zh", "Simplified Chinese"), "한국어": ("ko", "Korean"),
    "Français": ("fr", "French"), "Español": ("es", "Spanish"),
    "Deutsch": ("de", "German"), "Português": ("pt", "Portuguese"),
}

BRIEFS_I18N = {
 "ja": {
  "Japanese carmaker, India entry": "日本の自動車メーカーが、第1四半期にインド初の電気SUVを投入します。一部の愛好家を除き、インドの家庭での認知はほとんどありません。販売台数より先に信頼を得たいと考えており、外資の輸入品に見えることを経営陣が懸念しています。まず八大都市、その後に地方都市へ。",
  "Festive FMCG push": "食品メーカーが年末の祭事シーズンを狙っています。競合が多く、価格は中位帯で、テレビ広告にはすでに多額を投じています。テレビでは買えない効果を、25歳から45歳の家族層に向けて求めており、ヒンディー語圏での存在感を重視しています。",
  "Enterprise software, India": "外資系のエンタープライズソフトウェア企業が、従業員2,000名以上のインド企業の技術責任者に届きたいと考えています。商談期間は9か月。インプレッション数ではなく、質の高い商談を重視し、広告よりもソートリーダーシップを望んでいます。",
  "Japanese bank, India corridor": "日本の銀行が、インドで操業する日系メーカー向けの法人デスクをムンバイに開設します。対象は少数かつ上位層で、到達が困難です。リーチよりも、インド企業の財務部門からの信頼が重要です。",
 },
 "hi": {
  "Japanese carmaker, India entry": "एक जापानी वाहन निर्माता पहली तिमाही में भारत में अपनी पहली इलेक्ट्रिक एसयूवी ला रहा है। कुछ शौकीनों को छोड़कर भारतीय परिवारों में ब्रांड अनजान है। वे बिक्री से पहले भरोसा चाहते हैं, और बोर्ड को चिंता है कि कहीं यह विदेशी आयात न लगे। पहले आठ मेट्रो शहर, फिर टियर टू।",
  "Festive FMCG push": "एक पैकेज्ड फूड ब्रांड त्योहारी तिमाही चाहता है। श्रेणी में भीड़ है, उत्पाद मध्यम मूल्य का है, और ब्रांड पहले से टेलीविज़न पर भारी ख़र्च करता है। वे वह चाहते हैं जो टीवी का पैसा नहीं ख़रीद सकता, 25 से 45 वर्ष के परिवारों के लिए, मज़बूत हिंदी उपस्थिति के साथ।",
  "Enterprise software, India": "एक वैश्विक एंटरप्राइज़ सॉफ़्टवेयर कंपनी 2,000 से अधिक कर्मचारियों वाली भारतीय कंपनियों के तकनीकी निर्णयकर्ताओं तक पहुँचना चाहती है। बिक्री चक्र नौ महीने का है। उन्हें इम्प्रेशन नहीं, गुणवत्ता वाली बातचीत चाहिए।",
  "Japanese bank, India corridor": "एक जापानी बैंक मुंबई में कॉरपोरेट डेस्क खोल रहा है, जो भारत में काम कर रहे जापानी निर्माताओं की सेवा करेगा। दर्शक छोटे, वरिष्ठ और कठिन हैं। पहुँच से अधिक मायने रखती है भारतीय कॉरपोरेट फ़ाइनेंस टीमों की नज़र में विश्वसनीयता।",
 },
}


def briefs_for(lang):
    out = dict(D.SAMPLE_BRIEFS)
    src = BRIEFS_I18N.get(lang) or X.BRIEFS.get(lang, {})
    for k, v in src.items():
        if k in out:
            out[k] = v
    return out


def model_language(code):
    return next((v[1] for v in LANGUAGES.values() if v[0] == code), "English")


# ------------------------------------------------------------------ state
ss = st.session_state
ss.setdefault("lang", "en")
ss.setdefault("user", None)
ss.setdefault("users", {u: v[0] for u, v in ACCOUNTS.items()})
ss.setdefault("who", {u: (v[1], v[2]) for u, v in ACCOUNTS.items()})
ss.setdefault("plan", None)
ss.setdefault("history", [])
ss.setdefault("zoom", 80)
ss.setdefault("page", "what")

try:                                   # the landing button sends ?page=room
    _q = st.query_params.get("page")
    if _q in ("what", "room", "an"):
        ss.page = _q
        st.query_params.clear()
except Exception:
    pass

L = ss.lang
# labels the app needs even if strings.py is an older copy
LOCAL = {
 "nav_what": "How it works", "start": "Open the Pitch Room",
 "n_money": "Each bar is what one type of placement costs. Print is usually the tallest, which is why a small change there moves the whole budget.",
 "n_reach": "Each bar is how many people that type reaches. Compare it with the chart beside it: tall here and short there is the efficient buy.",
 "n_curve": "Reach does not build evenly. Most of it lands early, then the curve flattens as the same people see the campaign again.",
 "n_byplan": "What each plan you built would cost the advertiser, including tax.",
 "n_eff": "Cost of reaching one thousand people on each plan. Lower is better, and this is the number advertisers compare you on.",
 "n_mix": "Where the money went across every plan built in this session.",
}
LOCAL_JA = {"nav_what": "仕組み", "start": "ピッチルームを開く",
 "n_money": "各棒は掲載種別ごとの費用です。通常は新聞が最も高く、そこを少し動かすだけで全体が変わります。",
 "n_reach": "各棒は種別ごとの到達人数です。費用が低く到達が高い種別が効率の良い枠です。",
 "n_curve": "リーチは均等には積み上がりません。初期に大きく伸び、その後は緩やかになります。",
 "n_byplan": "作成した各プランの、税込の広告主負担額です。",
 "n_eff": "各プランの千人あたり単価です。低いほど良い指標です。",
 "n_mix": "このセッションで作成した全プランの費用配分です。"}
LOCAL_HI = {"nav_what": "यह कैसे काम करता है", "start": "पिच रूम खोलें",
 "n_money": "हर बार एक प्रकार के प्लेसमेंट की लागत है। प्रिंट आमतौर पर सबसे ऊँचा होता है।",
 "n_reach": "हर बार बताता है कि वह प्रकार कितने लोगों तक पहुँचता है।",
 "n_curve": "पहुँच बराबर नहीं बढ़ती। अधिकांश शुरू में मिलती है, फिर वक्र सपाट हो जाता है।",
 "n_byplan": "आपके बनाए हर प्लान की, कर सहित, विज्ञापनदाता पर लागत।",
 "n_eff": "हर प्लान में एक हज़ार लोगों तक पहुँचने की लागत। कम बेहतर है।",
 "n_mix": "इस सत्र के सभी प्लान में पैसा कहाँ गया।"}


class Labels(dict):
    """Never raises. A label we do not have falls back to English, then to itself."""
    def __missing__(self, key):
        return STR["en"].get(key, LOCAL.get(key, key.replace("_", " ")))


T = Labels(STR["en"])
T.update(LOCAL)
if L == "ja":
    T.update(LOCAL_JA)
if L == "hi":
    T.update(LOCAL_HI)
T.update(X.CORE.get(L, {}))
T.update(STR.get(L, {}))
_PROTO = getattr(D, "PROTOCOL", {"en": {}})
PROT = dict(_PROTO.get("en", {}))
PROT.update(_PROTO.get(L, {}))
_STAKE = getattr(D, "STAKEHOLDERS", {"en": []})


def css():
    z = ss.zoom
    st.markdown(f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Bricolage+Grotesque:opsz,wght@12..96,500;12..96,700;12..96,800&family=Inter+Tight:wght@400;500;600&family=Noto+Sans+JP:wght@400;500;700&family=Noto+Sans+Devanagari:wght@400;500;700&display=swap');
html {{ zoom: {z}%; }}
html, body, .stApp, button, input, textarea, select, .stMarkdown, [data-testid="stWidgetLabel"],
[data-testid="stMarkdownContainer"], .stRadio, .stSelectbox, .stSlider, .stTabs {{
  font-family: 'Inter Tight','Noto Sans JP','Noto Sans Devanagari',system-ui,sans-serif !important; }}
/* never touch the icon fonts, or the eye on the password box prints as a word */
span[data-testid="stIconMaterial"], .material-icons, .material-symbols-rounded,
[class*="material-symbols"], [data-testid*="Icon"] {{ font-family: 'Material Symbols Rounded' !important; }}
h1,h2,h3,.disp {{ font-family: 'Bricolage Grotesque','Noto Sans JP','Noto Sans Devanagari',system-ui,sans-serif !important;
  font-weight: 700 !important; letter-spacing: -.025em; }}
header[data-testid="stHeader"] {{ background: transparent; height: 0; }}
.block-container {{ padding-top: 4.2rem; padding-bottom: 3rem; max-width: 1380px; }}
[data-testid="stToolbar"], [data-testid="stStatusWidget"], [data-testid="manage-app-button"],
.stAppDeployButton, #MainMenu, footer, [data-testid="stDecoration"] {{ display: none !important; }}
[data-testid="stSidebar"] {{ min-width: 360px !important; max-width: 360px !important; }}
[data-testid="stSidebar"] .block-container {{ padding-top: 1.2rem; }}
.topline {{ display:flex; align-items:center; gap:10px; font-size:.82rem; color:#6B7280; }}
.badge {{ display:inline-block; font-size:.66rem; letter-spacing:.06em; padding:2px 9px;
  border-radius:999px; border:1px solid; }}
[data-testid="stSidebar"] {{ background: linear-gradient(180deg,#FFFFFF 0%,#FAF7F3 100%); border-right:1px solid #EDE6DE; }}
[data-testid="stMetricValue"] {{ font-family:'Bricolage Grotesque',sans-serif !important; font-weight:400 !important; }}
[data-testid="stMetricLabel"] p {{ text-transform:uppercase; letter-spacing:.05em; font-size:.68rem !important; color:#6B7280; }}
.disp {{ font-size:2.1rem; line-height:1.12; color:#16202C; margin:.1rem 0 .3rem; }}
.lede {{ color:#5B6472; font-size:1rem; margin-bottom:.6rem; }}
.card {{ border:1px solid #EDE6DE; border-left:5px solid {RED}; border-radius:12px;
  padding:14px 16px; background:#fff; height:100%; }}
.card.n {{ border-left-color:{NAVY}; }} .card.t {{ border-left-color:{TEAL}; }}
.card.g {{ border-left-color:{GOLD}; }} .card.p {{ border-left-color:{PLUM}; }}
.card h4 {{ margin:0 0 6px; font-size:.95rem; color:#16202C; font-weight:600; }}
.card p {{ margin:0; font-size:.86rem; color:#5B6472; }}
.pill {{ display:inline-block; border-radius:999px; padding:3px 11px; font-size:.72rem;
  margin:0 6px 6px 0; border:1px solid; }}
.warn {{ border-left:5px solid {RED}; background:#FDEEF0; padding:11px 15px; border-radius:10px; color:#16202C; }}
.good {{ border-left:5px solid {TEAL}; background:#E8F5F1; padding:11px 15px; border-radius:10px; color:#16202C; }}
.step {{ display:flex; gap:12px; align-items:flex-start; margin-bottom:10px; }}
.step b {{ flex:none; width:26px; height:26px; border-radius:50%; background:{RED}; color:#fff;
  display:flex; align-items:center; justify-content:center; font-size:.8rem; }}
.stTabs [data-baseweb="tab-list"] {{ gap:4px; }}
.stTabs [data-baseweb="tab"] {{ padding:6px 14px; border-radius:8px 8px 0 0; }}
hr {{ margin:.8rem 0; }}
</style>""", unsafe_allow_html=True)


css()


# ------------------------------------------------------------------ helpers
def inr(n):
    n = round(float(n))
    if abs(n) >= 10_000_000:
        return f"₹{n/10_000_000:,.2f} cr"
    if abs(n) >= 100_000:
        return f"₹{n/100_000:,.2f} lakh"
    return f"₹{n:,.0f}"


def inr_full(n):
    return f"₹{round(float(n)):,.0f}"


def h(txt):
    st.markdown(f'<div class="disp">{txt}</div>', unsafe_allow_html=True)


def sidebar_shell():
    """Always present, so the left panel never disappears between pages."""
    with st.sidebar:
        st.markdown(f"### {T['app']}")
        st.caption(T["tagline"])
        labels = [T["nav_what"], T["nav_room"], T["nav_an"]]
        keys = ["what", "room", "an"]
        choice = st.radio("nav", labels, index=keys.index(ss.page),
                          label_visibility="collapsed", key="navside")
        picked = keys[labels.index(choice)]
        if picked != ss.page:
            ss.page = picked
            st.rerun()
        st.divider()


def topbar():
    c = st.columns([4, 3, 2])
    with c[0]:
        st.markdown(f'**{T["app"]}**  <span style="color:#8A8F98;font-size:.8rem">{T["tagline"]}</span>',
                    unsafe_allow_html=True)
    with c[1]:
        names = list(LANGUAGES)
        cur = next((n for n, v in LANGUAGES.items() if v[0] == ss.lang), "English")
        choice = st.selectbox(T["lang_label"], names, index=names.index(cur),
                              label_visibility="collapsed", key="langpick")
        new = LANGUAGES[choice][0]
        if new != ss.lang:
            ss.lang = new
            st.rerun()
    with c[2]:
        if ss.user:
            nm, side = ss.who.get(ss.user, (ss.user, "Guest"))
            col = NAVY if side == "Kenja" else TEAL
            st.markdown(f'<div style="text-align:right;font-size:.8rem;color:#6B7280">{T["signedin"]} '
                        f'<b>{nm}</b> <span class="badge" style="border-color:{col};color:{col}">{side}</span></div>',
                        unsafe_allow_html=True)
            if st.button(T["signout"], use_container_width=True):
                ss.user = None
                st.rerun()
    st.divider()


# ------------------------------------------------------------------ auth
def auth_page():
    h(T["auth_h"])
    st.markdown(f'<div class="lede">{T["auth_s"]}</div>', unsafe_allow_html=True)
    a, b = st.columns([1, 1.1])
    with a:
        ti, tu = st.tabs([T["tab_in"], T["tab_up"]])
        with ti:
            with st.form("in"):
                u = st.text_input(T["user"])
                p = st.text_input(T["pwd"], type="password")
                if st.form_submit_button(T["btn_in"], type="primary", use_container_width=True):
                    hp = hashlib.sha256(p.encode()).hexdigest()
                    if ss.users.get(u.strip().lower()) == hp:
                        ss.user = u.strip().lower()
                        st.rerun()
                    else:
                        st.error(T["err_user"])
            st.caption(T["kenja_note"])
        with tu:
            with st.form("up"):
                u = st.text_input(T["user"], key="nu")
                p1 = st.text_input(T["pwd"], type="password", key="np1")
                p2 = st.text_input(T["pwd2"], type="password", key="np2")
                if st.form_submit_button(T["btn_up"], type="primary", use_container_width=True):
                    u = u.strip()
                    if not u or u in ss.users:
                        st.error(T["err_exists"])
                    elif len(p1) < 6:
                        st.error(T["err_short"])
                    elif p1 != p2:
                        st.error(T["err_match"])
                    else:
                        ss.users[u] = hashlib.sha256(p1.encode()).hexdigest()
                        ss.who[u] = (u, "Guest")
                        ss.user = u
                        st.rerun()
        st.caption(T["note_auth"])
    with b:
        for k, cls in [("w1", ""), ("w3", "n"), ("w4", "t")]:
            st.markdown(f'<div class="card {cls}"><h4>{T[k+"_h"]}</h4><p>{T[k+"_b"]}</p></div>',
                        unsafe_allow_html=True)
            st.write("")


# ------------------------------------------------------------------ explainer
def what_page():
    """The same product site people see on the web, inside the app."""
    st.markdown("<style>.block-container{padding-left:0;padding-right:0;max-width:100%}</style>",
                unsafe_allow_html=True)
    if st.button(T["start"], type="primary", use_container_width=True, key="open_top"):
        ss.page = "room"
        st.rerun()
    landing.render(height=5600)
    if st.button(T["start"], type="primary", use_container_width=True, key="open_bottom"):
        ss.page = "room"
        st.rerun()


# ------------------------------------------------------------------ retrieval, pricing
def retrieve(brief, enabled):
    words = set(re.split(r"[^a-z]+", brief.lower()))
    scored = []
    for c in D.CORPUS:
        if c["id"] not in enabled:
            continue
        s = sum(1 for k in c["keys"] if k in words) + (5 if c["id"] == "rate" else 0)
        if s:
            scored.append((s, c))
    scored.sort(key=lambda x: -x[0])
    return [c for _, c in scored[:4]]


def price_print(rows, season_pct):
    out = []
    for r in rows:
        ed, sz = D.PRINT_EDITIONS.get(r.get("edition")), D.PRINT_SIZES.get(r.get("size"))
        if not ed or not sz:
            continue
        pos = D.POSITION_LOADING.get(r.get("position", "Run of paper"), 0)
        ins = max(1, int(r.get("insertions", 1)))
        rate = ed["rate_sqcm"] * sz * (1 + pos / 100) * (1 + season_pct / 100)
        out.append({"Line": f'{r["edition"]}, {r["size"]}, {r.get("position","Run of paper")}',
                    "Detail": f'{sz} sq cm', "Loading": f"{pos + season_pct}%", "Qty": ins,
                    "Unit": "insertion", "Rate": rate, "Gross": rate * ins,
                    "Reach": ed["readership"] * min(ins, 3) * 0.55,
                    "Why": r.get("why", ""), "Group": "Print"})
    return out


def price_digital(rows, lang):
    out = []
    for r in rows:
        spec = D.DIGITAL.get(r.get("id"))
        if not spec:
            continue
        nm = D.name_for(r.get("id"), spec["name"], lang)
        if "cpm" in spec:
            impr = max(1000, int(r.get("impressions", 1_000_000)))
            out.append({"Line": nm, "Detail": f'CPM {inr_full(spec["cpm"])}', "Loading": "0%",
                        "Qty": impr, "Unit": "impressions", "Rate": spec["cpm"],
                        "Gross": impr / 1000 * spec["cpm"],
                        "Reach": min(impr * 0.42, spec["pool"]),
                        "Why": r.get("why", ""), "Group": "Digital"})
        else:
            u = max(1, int(r.get("units", 1) or 1))
            u = 1 if u > 50 else u
            out.append({"Line": nm, "Detail": "Fixed", "Loading": "0%", "Qty": u, "Unit": "unit",
                        "Rate": spec["flat"], "Gross": spec["flat"] * u,
                        "Reach": spec["pool"] * min(u, 3) * 0.6,
                        "Why": r.get("why", ""), "Group": "Digital"})
    return out


def price_content(rows, lang):
    out = []
    for r in rows:
        spec = D.CONTENT.get(r.get("id"))
        if not spec:
            continue
        u = max(1, int(r.get("units", 1)))
        out.append({"Line": D.name_for(r.get("id"), spec["name"], lang), "Detail": "Branded desk",
                    "Loading": "0%", "Qty": u, "Unit": "unit", "Rate": spec["flat"],
                    "Gross": spec["flat"] * u, "Reach": spec["pool"] * u * 0.8,
                    "Why": r.get("why", ""), "Group": "Content and events"})
    return out


def commercials(lines, agency, disc, bonus_on):
    gross = sum(l["Gross"] for l in lines) or 1
    space = sum(l["Gross"] for l in lines if l["Group"] != "Content and events")
    service = gross - space
    disc_amt = gross * disc / 100
    after = gross - disc_amt
    comm = after * D.AGENCY_COMMISSION if agency else 0.0
    fee = 0.0 if agency else after * D.PLANNING_FEE
    net = after - comm + fee
    gst = (space / gross) * net * D.GST_SPACE + (service / gross) * net * D.GST_SERVICE
    reach = sum(l["Reach"] for l in lines)
    return {"gross": gross, "discount": disc_amt, "commission": comm, "fee": fee, "net": net,
            "gst": gst, "payable": net + gst, "reach": reach,
            "bonus": gross * D.BONUS_INVENTORY if bonus_on else 0.0,
            "cpm": (net / max(reach, 1)) * 1000}


def build_prompt(brief, sources, budget, weeks, lang_name, markets):
    return f"""You are a media strategist with twenty years inside a large Indian news group, writing a plan for an advertiser.

THE BRIEF:
{brief}

BUDGET: {inr_full(budget)} gross. LENGTH: {weeks} weeks. PRIORITY MARKETS: {", ".join(markets)}.

FROM OUR OWN FILES:
{chr(10).join('  ' + s["title"] + ': ' + s["detail"] for s in sources)}

PRINT editions: {", ".join(D.PRINT_EDITIONS)}
Sizes: {", ".join(D.PRINT_SIZES)}. Positions: {", ".join(D.POSITION_LOADING)}.
DIGITAL ids: {", ".join(D.DIGITAL)}
CONTENT ids: {", ".join(D.CONTENT)}

Never state a price or a total. Quantities only.
Print is expensive, keep insertions deliberate. Digital impressions in millions.
Use Hindi and regional inventory when the audience reaches past English readers.
Write every word in {lang_name}.

Reply with JSON only:
{{"title":"short campaign name","objective":"one sentence","insight":"two sentences",
 "audience":["three lines"],
 "print":[{{"edition":"","size":"","position":"","insertions":1,"why":""}}],
 "digital":[{{"id":"","impressions":1000000,"why":""}}],
 "content":[{{"id":"","units":1,"why":""}}],
 "timeline":[{{"phase":"","action":""}}],
 "kpis":["three outcomes"],"risk":"one line"}}"""


def call_model(prompt):
    key = os.environ.get("ANTHROPIC_API_KEY", "")
    if not key:
        try:
            key = st.secrets.get("ANTHROPIC_API_KEY", "")
        except Exception:
            key = ""
    if not key:
        return None, "nokey"
    try:
        from anthropic import Anthropic
        msg = Anthropic(api_key=key).messages.create(
            model=MODEL, max_tokens=2000, messages=[{"role": "user", "content": prompt}])
        txt = "".join(b.text for b in msg.content if getattr(b, "type", "") == "text")
        return json.loads(re.sub(r"^```(?:json)?|```$", "", txt.strip(), flags=re.M).strip()), None
    except Exception as e:
        return None, str(e)[:120]


# ------------------------------------------------------------------ pitch room
def room_page():
    with st.sidebar:
        briefs = briefs_for(L)
        pick = st.selectbox(T["sb_brief_from"], list(briefs))
        brief = st.text_area(T["sb_brief"], briefs[pick], height=150, key="brief_" + L)
        budget = st.select_slider(T["sb_budget"],
                                  options=[25_000_000, 50_000_000, 75_000_000, 100_000_000, 150_000_000],
                                  value=50_000_000, format_func=inr)
        weeks = st.slider(T["sb_weeks"], 2, 16, 8, step=2)
        markets = st.multiselect(T["sb_markets"], list(D.PRINT_EDITIONS),
                                 default=["Delhi NCR", "Mumbai", "Bengaluru"])
        season = st.selectbox(T["sb_season"], list(D.SEASON_LOADING))
        st.divider()
        st.caption(T["sb_comm"])
        agency = st.toggle(T["sb_agency"], value=True)
        disc = st.slider(T["sb_disc"], 0, 45, 18)
        bonus = st.toggle(T["sb_bonus"], value=True)
        start = st.date_input(T["sb_start"], value=date.today() + timedelta(days=21))
        st.divider()
        st.caption(T["sb_corpus"])
        enabled = [c["id"] for c in D.CORPUS if st.checkbox(c["title"], True, key="c_" + c["id"])]
        st.divider()
        label = T["sb_again"] if ss.plan else T["sb_build"]
        go = st.button(label, type="primary", use_container_width=True)
        if ss.plan and st.button(T["sb_clear"], use_container_width=True):
            ss.plan = None
            st.rerun()
        st.select_slider(T["sb_zoom"], options=[70, 80, 90, 100], key="zoom")

    if go:
        sources = retrieve(brief, enabled)
        with st.status(T["st_work"], expanded=True) as s:
            st.write(T["st_read"])
            st.write(T["st_ret"].format(n=len(sources)))
            st.write(T["st_draft"])
            data, err = call_model(build_prompt(
                brief, sources, budget, weeks,
                model_language(L), markets or ["Delhi NCR"]))
            off = data is None
            if off:
                data = D.FALLBACK.get(L, D.FALLBACK["en"])
                st.write(T["st_nokey"] if err == "nokey" else T["st_fail"])
            st.write(T["st_price"])
            s.update(label=T["st_done"], state="complete", expanded=False)
        ss.plan = {"data": data, "sources": sources, "offline": off, "lang": L,
                   "weeks": weeks, "start": start, "budget": budget}

    if not ss.plan:
        h(T["e_h"])
        st.markdown(f'<div class="lede">{T["e_s"]}</div>', unsafe_allow_html=True)
        c = st.columns(3)
        for col, n, k, cls in zip(c, "123", ["e1", "e2", "e3"], ["", "n", "t"]):
            with col:
                st.markdown(f'<div class="card {cls}"><div class="step"><b>{n}</b>'
                            f'<div><p>{T[k]}</p></div></div></div>', unsafe_allow_html=True)
        st.caption(T["e_time"])
        return

    plan = ss.plan
    if plan["offline"] and plan["lang"] != L:
        plan["data"], plan["lang"] = D.FALLBACK.get(L, D.FALLBACK["en"]), L
    d = plan["data"]
    lines = (price_print(d.get("print", []), D.SEASON_LOADING[season])
             + price_digital(d.get("digital", []), L)
             + price_content(d.get("content", []), L))
    c = commercials(lines, agency, disc, bonus)
    df = pd.DataFrame(lines)

    if ss.history[-1:] == [] or ss.history[-1].get("key") != (d.get("title"), round(c["payable"])):
        ss.history.append({"key": (d.get("title"), round(c["payable"])), "title": d.get("title", ""),
                           "payable": c["payable"], "reach": c["reach"], "cpm": c["cpm"],
                           "lang": L, "when": pd.Timestamp.now().strftime("%H:%M"),
                           "mix": df.groupby("Group")["Gross"].sum().to_dict()})

    if plan["offline"]:
        st.markdown(f'<div class="warn">{T["offline"]}</div>', unsafe_allow_html=True)
    elif plan["lang"] != L:
        st.info(T["stale"])

    h(d.get("title", ""))
    st.markdown(f'<div class="lede">{d.get("objective","")}</div>', unsafe_allow_html=True)
    st.markdown("".join(
        f'<span class="pill" style="border-color:{RED};color:{RED};background:#FDEEF0">{s["title"]}</span>'
        for s in plan["sources"]), unsafe_allow_html=True)

    m = st.columns(5)
    gap = (c["payable"] / plan["budget"] - 1) * 100
    m[0].metric(T["pay"], inr(c["payable"]), f'{gap:+.0f}% {T["vs"]}')
    m[1].metric(T["net"], inr(c["net"]))
    m[2].metric(T["reach"], f'{c["reach"]/1_000_000:.1f} m')
    m[3].metric(T["cpm"], inr_full(c["cpm"]))
    m[4].metric(T["bonus"], inr(c["bonus"]))
    if gap > 5:
        st.markdown(f'<div class="warn">{T["over"]}</div>', unsafe_allow_html=True)
    elif gap < -20:
        st.markdown(f'<div class="good">{T["under"]}</div>', unsafe_allow_html=True)

    P = PROT
    t1, t2, t3, t4, t5, t6 = st.tabs([T["t_plan"], T["t_num"], T["t_ro"], T["t_arg"],
                                      P["tab"], T["t_exp"]])

    with t1:
        st.markdown(f"**{d.get('insight','')}**")
        a, b = st.columns(2)
        with a:
            st.markdown("##### " + T["who"])
            for x in d.get("audience", []):
                st.markdown(f"- {x}")
        with b:
            st.markdown("##### " + T["runs"])
            for t in d.get("timeline", []):
                st.markdown(f"**{t.get('phase','')}**  {t.get('action','')}")
        st.markdown("##### " + T["sched"])
        show = df[["Line", "Detail", "Loading", "Qty", "Rate", "Gross", "Why"]].copy()
        show["Rate"] = show["Rate"].map(inr_full)
        show["Gross"] = show["Gross"].map(inr_full)
        show["Qty"] = show["Qty"].map(lambda x: f"{x:,.0f}")
        show.columns = [T["line"], T["detail"], T["loading"], T["qty"], T["rate"], T["gross"], T["why"]]
        st.dataframe(show, use_container_width=True, hide_index=True)

    with t2:
        a, b = st.columns(2)
        with a:
            st.markdown("##### " + T["money"])
            g = df.groupby("Group")["Gross"].sum().reset_index()
            g.columns = [T["group"], T["gross"]]
            st.bar_chart(g, x=T["group"], y=T["gross"], color=RED, height=250)
            st.caption(T["n_money"])
        with b:
            st.markdown("##### " + T["reachsrc"])
            r = df.groupby("Group")["Reach"].sum().reset_index()
            r.columns = [T["group"], T["reach"]]
            st.bar_chart(r, x=T["group"], y=T["reach"], color=NAVY, height=250)
            st.caption(T["n_reach"])
        st.markdown("##### " + T["curve"])
        wk = plan["weeks"]
        curve = pd.DataFrame({T["week"]: list(range(1, wk + 1)),
                              T["reach"]: [c["reach"] * (1 - pow(2.718, -2.2 * i / wk)) for i in range(1, wk + 1)]})
        st.area_chart(curve, x=T["week"], y=T["reach"], color=TEAL, height=240)
        st.caption(T["n_curve"])
        st.markdown("##### " + T["settle"])
        ladder = pd.DataFrame([
            [T["gross"], c["gross"]], [f'{T["sb_disc"]} {disc}', -c["discount"]],
            [T["sb_agency"] if agency else "Planning fee", -c["commission"] if agency else c["fee"]],
            [T["net"], c["net"]], ["GST", c["gst"]], [T["pay"], c["payable"]]],
            columns=[T["step"], T["amount"]])
        ladder[T["amount"]] = ladder[T["amount"]].map(inr_full)
        st.dataframe(ladder, use_container_width=True, hide_index=True)

    with t3:
        ro = f"RO/{date.today().strftime('%Y%m')}/{abs(hash(d.get('title','x'))) % 9000 + 1000}"
        st.markdown(f"##### {T['ro_h']} {ro}")
        st.write(f'{T["ro_mat"]}: {(plan["start"] - timedelta(days=7)).strftime("%d %b %Y")}')
        rod = df[["Group", "Line", "Qty", "Unit", "Gross"]].copy()
        rod["Gross"] = rod["Gross"].map(inr_full)
        rod.columns = [T["group"], T["line"], T["qty"], "Unit", T["gross"]]
        st.dataframe(rod, use_container_width=True, hide_index=True)
        st.markdown(f'<div class="good">{T["ro_terms"].format(x=inr_full(c["payable"]), d=D.CREDIT_DAYS)}</div>',
                    unsafe_allow_html=True)

    with t4:
        st.markdown("##### " + T["measure"])
        for k in d.get("kpis", []):
            st.markdown(f"- {k}")
        st.markdown("##### " + T["risk"])
        st.write(d.get("risk", ""))
        st.markdown("##### " + T["whyus"])
        st.write(T["whyus_b"])

    with t5:
        st.caption(P["intro"])
        st.markdown("##### " + P["nema_h"])
        st.write(P["nema_s"])
        st.dataframe(pd.DataFrame(_STAKE.get(L, _STAKE.get("en", [])),
                                  columns=[P["who"], P["cares"], P["ask"], P["when"]]),
                     use_container_width=True, hide_index=True)
        st.markdown("##### " + P["ringi_h"])
        st.write(P["ringi_s"])
        st.dataframe(pd.DataFrame([(i + 1, r[0], r[2], "") for i, r in enumerate(_STAKE.get(L, _STAKE.get("en", [])))],
                                  columns=["#", P["who"], P["ask"], "承認"]),
                     use_container_width=True, hide_index=True)
        st.markdown("##### " + P["horen_h"])
        st.write(P["horen_s"])
        s0, wk = plan["start"], plan["weeks"]
        cal = [(s0 - timedelta(days=7), T["ro_mat"], "Both"), (s0, "Live", "Publisher")]
        for i in range(1, wk):
            cal.append((s0 + timedelta(weeks=i),
                        "Mid campaign review" if i == wk // 2 else "Written report, unprompted", "Us"))
        cal.append((s0 + timedelta(weeks=wk), "Campaign ends", "Publisher"))
        cal.append((s0 + timedelta(weeks=wk + 2), P["hansei_h"], "Us"))
        st.dataframe(pd.DataFrame([(x[0].strftime("%d %b %Y"), x[1], x[2]) for x in cal],
                                  columns=[P["date"], P["what"], P["owner"]]),
                     use_container_width=True, hide_index=True)
        st.markdown("##### " + P["hansei_h"])
        st.write(P["hansei_s"])
        st.markdown("##### " + P["commit_h"])
        for x in P["commits"]:
            st.markdown(f"- {x}")

    with t6:
        md = [f"# {d.get('title','')}", "", d.get("objective", ""), "", d.get("insight", ""), "",
              f'| {T["line"]} | {T["qty"]} | {T["rate"]} | {T["gross"]} |', "| --- | --- | --- | --- |"]
        for l in lines:
            md.append(f'| {l["Line"]} | {l["Qty"]:,.0f} | {inr_full(l["Rate"])} | {inr_full(l["Gross"])} |')
        md += ["", f'**{T["pay"]} {inr_full(c["payable"])} · {T["reach"]} {c["reach"]/1_000_000:.1f} m '
                   f'· {T["cpm"]} {inr_full(c["cpm"])}**', "", T["risk"], d.get("risk", "")]
        md = "\n".join(md)
        st.code(md, language="markdown")
        a, b = st.columns(2)
        a.download_button(T["dl_md"], md, file_name="plan.md", use_container_width=True)
        b.download_button(T["dl_csv"], df.to_csv(index=False), file_name="schedule.csv",
                          use_container_width=True)


# ------------------------------------------------------------------ analytics
def analytics_page():
    h(T["an_h"])
    hist = ss.history
    if not hist:
        st.markdown(f'<div class="lede">{T["an_empty"]}</div>', unsafe_allow_html=True)
        return
    hd = pd.DataFrame(hist)
    m = st.columns(4)
    m[0].metric(T["an_plans"], len(hd))
    m[1].metric(T["an_value"], inr(hd["payable"].sum()))
    m[2].metric(T["an_avgcpm"], inr_full(hd["cpm"].mean()))
    m[3].metric(T["an_reach"], f'{hd["reach"].sum()/1_000_000:.1f} m')
    a, b = st.columns(2)
    with a:
        st.markdown("##### " + T["an_byplan"])
        v = hd[["title", "payable"]].copy()
        v.columns = [T["an_title"], T["pay"]]
        st.bar_chart(v, x=T["an_title"], y=T["pay"], color=RED, height=260)
        st.caption(T["n_byplan"])
    with b:
        st.markdown("##### " + T["an_eff"])
        e = hd[["title", "cpm"]].copy()
        e.columns = [T["an_title"], T["cpm"]]
        st.bar_chart(e, x=T["an_title"], y=T["cpm"], color=GOLD, height=260)
        st.caption(T["n_eff"])
    st.markdown("##### " + T["an_mix"])
    mix = {}
    for row in hist:
        for k, v in row["mix"].items():
            mix[k] = mix.get(k, 0) + v
    mx = pd.DataFrame({T["group"]: list(mix), T["gross"]: list(mix.values())})
    st.bar_chart(mx, x=T["group"], y=T["gross"], color=TEAL, height=240)
    st.caption(T["n_mix"])
    st.markdown("##### " + T["an_hist"])
    show = hd[["when", "title", "lang", "payable", "reach", "cpm"]].copy()
    show["payable"] = show["payable"].map(inr_full)
    show["reach"] = show["reach"].map(lambda x: f"{x/1_000_000:.1f} m")
    show["cpm"] = show["cpm"].map(inr_full)
    show.columns = [T["an_when"], T["an_title"], T["an_lang"], T["pay"], T["reach"], T["cpm"]]
    st.dataframe(show, use_container_width=True, hide_index=True)


# ------------------------------------------------------------------ run
topbar()
if not ss.user:
    auth_page()
else:
    sidebar_shell()
    if ss.page == "what":
        what_page()
    elif ss.page == "room":
        room_page()
    else:
        analytics_page()
