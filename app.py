"""
Pitch Room, a Kenja prototype.

A brief goes in. A costed, bilingual media plan comes out, priced from a real
rate card rather than from a language model.

Run locally:   streamlit run app.py
Key:           put ANTHROPIC_API_KEY in .streamlit/secrets.toml or the environment
"""

import json
import os
import re
from datetime import date, timedelta

import pandas as pd
import streamlit as st

import toi_data as D

st.set_page_config(page_title="Pitch Room", page_icon="📰", layout="wide")

MODEL = os.environ.get("PITCHROOM_MODEL", "claude-sonnet-5-5")

# --------------------------------------------------------------- styling
st.markdown("""
<style>
.block-container{padding-top:2.2rem;max-width:1400px}
h1,h2,h3{letter-spacing:-.01em}
.big{font-size:2rem;font-weight:700;line-height:1.1}
.sub{color:#6b7280;font-size:.85rem}
.kv{border:1px solid rgba(128,128,128,.25);border-radius:10px;padding:12px 14px}
.srcpill{display:inline-block;border:1px solid rgba(200,16,46,.4);background:rgba(200,16,46,.07);
         color:#C8102E;border-radius:999px;padding:2px 10px;font-size:.72rem;margin:0 5px 5px 0}
.warn{border-left:4px solid #C8102E;background:rgba(200,16,46,.06);padding:10px 14px;border-radius:8px}
.ok{border-left:4px solid #0F6B4F;background:rgba(15,107,79,.07);padding:10px 14px;border-radius:8px}
</style>
""", unsafe_allow_html=True)


# --------------------------------------------------------------- money
def inr(n):
    n = round(float(n))
    if abs(n) >= 10_000_000:
        return f"₹{n/10_000_000:,.2f} cr"
    if abs(n) >= 100_000:
        return f"₹{n/100_000:,.2f} lakh"
    return f"₹{n:,.0f}"


def inr_full(n):
    return f"₹{round(float(n)):,.0f}"


# --------------------------------------------------------------- retrieval
def retrieve(brief, enabled):
    words = set(re.split(r"[^a-z]+", brief.lower()))
    scored = []
    for c in D.CORPUS:
        if c["id"] not in enabled:
            continue
        s = sum(1 for k in c["keys"] if k in words)
        if c["id"] == "rate":
            s += 5
        if s:
            scored.append((s, c))
    scored.sort(key=lambda x: -x[0])
    return [c for _, c in scored[:4]]


# --------------------------------------------------------------- pricing
def price_print(rows, season_pct):
    out = []
    for r in rows:
        ed = D.PRINT_EDITIONS.get(r.get("edition"))
        sz = D.PRINT_SIZES.get(r.get("size"))
        if not ed or not sz:
            continue
        pos_pct = D.POSITION_LOADING.get(r.get("position", "Run of paper"), 0)
        ins = max(1, int(r.get("insertions", 1)))
        base = ed["rate_sqcm"] * sz
        loaded = base * (1 + pos_pct / 100) * (1 + season_pct / 100)
        out.append({
            "Line": f'{r["edition"]}, {r["size"]}, {r.get("position","Run of paper")}',
            "Detail": f'{sz} sq cm at {inr_full(ed["rate_sqcm"])} per sq cm',
            "Loading": f'{pos_pct + season_pct}%',
            "Qty": ins,
            "Unit": "insertion",
            "Rate": loaded,
            "Gross": loaded * ins,
            "Reach": ed["readership"] * min(ins, 3) * 0.55,
            "Why": r.get("why", ""),
            "Group": "Print",
        })
    return out


def price_digital(rows, lang="en"):
    out = []
    for r in rows:
        spec = D.DIGITAL.get(r.get("id"))
        if not spec:
            continue
        if "cpm" in spec:
            impr = max(1000, int(r.get("impressions", 1_000_000)))
            gross = impr / 1000 * spec["cpm"]
            out.append({
                "Line": D.name_for(r.get("id"), spec["name"], lang),
                "Detail": f'CPM {inr_full(spec["cpm"])}',
                "Loading": "0%",
                "Qty": impr,
                "Unit": "impressions",
                "Rate": spec["cpm"],
                "Gross": gross,
                "Reach": min(impr * 0.42, spec["pool"]),
                "Why": r.get("why", ""),
                "Group": "Digital",
            })
        else:
            units = max(1, int(r.get("units", r.get("impressions", 1) or 1)))
            if units > 50:
                units = 1
            out.append({
                "Line": D.name_for(r.get("id"), spec["name"], lang),
                "Detail": "Fixed price",
                "Loading": "0%",
                "Qty": units,
                "Unit": "unit",
                "Rate": spec["flat"],
                "Gross": spec["flat"] * units,
                "Reach": spec["pool"] * min(units, 3) * 0.6,
                "Why": r.get("why", ""),
                "Group": "Digital",
            })
    return out


def price_content(rows, lang="en"):
    out = []
    for r in rows:
        spec = D.CONTENT.get(r.get("id"))
        if not spec:
            continue
        units = max(1, int(r.get("units", 1)))
        out.append({
            "Line": D.name_for(r.get("id"), spec["name"], lang),
            "Detail": "Branded content desk",
            "Loading": "0%",
            "Qty": units,
            "Unit": "unit",
            "Rate": spec["flat"],
            "Gross": spec["flat"] * units,
            "Reach": spec["pool"] * units * 0.8,
            "Why": r.get("why", ""),
            "Group": "Content and events",
        })
    return out


def commercials(lines, agency, discount_pct, bonus_on):
    gross = sum(l["Gross"] for l in lines)
    space = sum(l["Gross"] for l in lines if l["Group"] != "Content and events")
    service = gross - space
    discount = gross * discount_pct / 100
    after_discount = gross - discount
    commission = after_discount * D.AGENCY_COMMISSION if agency else 0.0
    fee = 0.0 if agency else after_discount * D.PLANNING_FEE
    net = after_discount - commission + fee
    gst = (space / max(gross, 1)) * net * D.GST_SPACE + (service / max(gross, 1)) * net * D.GST_SERVICE
    reach = sum(l["Reach"] for l in lines)
    bonus = sum(l["Gross"] for l in lines) * D.BONUS_INVENTORY if bonus_on else 0.0
    return {
        "gross": gross, "discount": discount, "commission": commission, "fee": fee,
        "net": net, "gst": gst, "payable": net + gst, "reach": reach,
        "bonus": bonus,
        "cpm": (net / max(reach, 1)) * 1000,
    }


# --------------------------------------------------------------- model
def build_prompt(brief, sources, budget, weeks, lang_name, markets):
    menu_digital = "\n".join(f'  {k} = {v["name"]}' for k, v in D.DIGITAL.items())
    menu_content = "\n".join(f'  {k} = {v["name"]}' for k, v in D.CONTENT.items())
    return f"""You are a media strategist with twenty years inside a large Indian news group, writing a plan for an advertiser.

THE BRIEF:
{brief}

BUDGET: {inr_full(budget)} gross. LENGTH: {weeks} weeks. PRIORITY MARKETS: {", ".join(markets)}.

FROM OUR OWN FILES:
{chr(10).join('  ' + s["title"] + ': ' + s["detail"] for s in sources)}

PRINT: choose editions from {", ".join(D.PRINT_EDITIONS)}.
Sizes: {", ".join(D.PRINT_SIZES)}. Positions: {", ".join(D.POSITION_LOADING)}.

DIGITAL ids:
{menu_digital}

CONTENT AND EVENT ids:
{menu_content}

Rules you must follow:
Never state a price, a rate or a total. Quantities only, pricing is calculated separately.
Print is expensive, so keep insertions low and deliberate. Digital impressions should be in millions.
Use Hindi or regional inventory whenever the audience reaches beyond English readers, and say why.
Write every word of the output in {lang_name}.

Reply with JSON only, this exact shape:
{{"title":"short campaign name",
 "objective":"one sentence",
 "insight":"the non obvious observation this plan rests on, two sentences",
 "audience":["three short audience lines"],
 "print":[{{"edition":"","size":"","position":"","insertions":1,"why":"one line"}}],
 "digital":[{{"id":"","impressions":1000000,"why":"one line"}}],
 "content":[{{"id":"","units":1,"why":"one line"}}],
 "timeline":[{{"phase":"Weeks 1 to 2","action":"one line"}}],
 "kpis":["three measurable outcomes"],
 "risk":"one honest line about what could go wrong"}}"""


def call_model(prompt):
    key = os.environ.get("ANTHROPIC_API_KEY", "")
    if not key:
        try:                      # no secrets file at all is a normal, keyless run
            key = st.secrets.get("ANTHROPIC_API_KEY", "")
        except Exception:
            key = ""
    if not key:
        return None, "no key"
    try:
        from anthropic import Anthropic
        client = Anthropic(api_key=key)
        msg = client.messages.create(
            model=MODEL, max_tokens=2000,
            messages=[{"role": "user", "content": prompt}],
        )
        text = "".join(b.text for b in msg.content if getattr(b, "type", "") == "text")
        text = re.sub(r"^```(?:json)?|```$", "", text.strip(), flags=re.M).strip()
        return json.loads(text), None
    except Exception as e:  # a demo must never die in front of a client
        return None, str(e)[:160]


# --------------------------------------------------------------- sidebar
with st.sidebar:
    st.markdown("### Pitch Room")
    st.caption("Kenja prototype. Rates illustrative.")

    lang_label = st.radio("Output language", list(D.LANGS), horizontal=True)
    lang = D.LANGS[lang_label]

    st.divider()
    pick = st.selectbox("Start from a brief", list(D.SAMPLE_BRIEFS))
    brief = st.text_area("The brief", D.SAMPLE_BRIEFS[pick], height=180)

    budget = st.select_slider(
        "Gross budget",
        options=[25_000_000, 50_000_000, 75_000_000, 100_000_000, 150_000_000],
        value=50_000_000, format_func=inr)
    weeks = st.slider("Campaign length, weeks", 2, 16, 8, step=2)
    markets = st.multiselect("Priority markets", list(D.PRINT_EDITIONS),
                             default=["Delhi NCR", "Mumbai", "Bengaluru"])
    season = st.selectbox("Season loading", list(D.SEASON_LOADING))

    st.divider()
    st.caption("Commercials")
    agency = st.toggle("Accredited agency on the deal, 15 percent commission", value=True)
    discount = st.slider("Negotiated discount on gross, percent", 0, 45, 18)
    bonus = st.toggle("Concede 10 percent bonus inventory", value=True)

    st.divider()
    st.caption("Corpus")
    enabled = [c["id"] for c in D.CORPUS if st.checkbox(c["title"], True, key="c_" + c["id"])]

    go = st.button("Build the plan", type="primary", use_container_width=True)


# --------------------------------------------------------------- run
if "plan" not in st.session_state:
    st.session_state.plan = None

if go:
    sources = retrieve(brief, enabled)
    with st.status("Working", expanded=True) as status:
        st.write("Reading the brief")
        st.write(f"Retrieved {len(sources)} sources: " + ", ".join(s["title"] for s in sources))
        st.write("Drafting the plan")
        data, err = call_model(build_prompt(brief, sources, budget, weeks, lang_label, markets or ["Delhi NCR"]))
        offline = data is None
        if offline:
            data = D.FALLBACK[lang]
            st.write("Running without a key, showing the saved example" if err == "no key" else f"Model unavailable ({err}), using the saved example")
        st.write("Pricing from the rate card")
        status.update(label="Done", state="complete", expanded=False)
    st.session_state.plan = {"data": data, "sources": sources, "offline": offline, "lang": lang}

plan = st.session_state.plan

if not plan:
    st.markdown('<div class="big">Nothing built yet</div>', unsafe_allow_html=True)
    st.write("Set the brief on the left and press build. A costed plan appears in about twenty seconds.")
    st.stop()

d = plan["data"]
# the saved example exists in every language, so follow the picker immediately
if plan["offline"] and plan["lang"] != lang:
    d = D.FALLBACK[lang]
    plan["data"], plan["lang"] = d, lang

U = D.UI[lang]
lines = (price_print(d.get("print", []), D.SEASON_LOADING[season])
         + price_digital(d.get("digital", []), lang)
         + price_content(d.get("content", []), lang))
c = commercials(lines, agency, discount, bonus)
df = pd.DataFrame(lines)

if plan["offline"]:
    st.markdown('<div class="warn">Showing the saved example. Everything here works except freshly written copy, which needs an API key.</div>',
                unsafe_allow_html=True)

if not plan["offline"] and plan["lang"] != lang:
    st.info(D.UI[lang]["stale"])
st.markdown(f'<div class="big">{d.get("title","")}</div>', unsafe_allow_html=True)
st.write(d.get("objective", ""))
st.markdown("".join(f'<span class="srcpill">{s["title"]}</span>' for s in plan["sources"]),
            unsafe_allow_html=True)

over = c["payable"] > budget * 1.05
m = st.columns(5)
m[0].metric(U["pay"], inr(c["payable"]), f'{(c["payable"]/budget-1)*100:+.0f}% against budget')
m[1].metric(U["net"], inr(c["net"]))
m[2].metric(U["reach"], f'{c["reach"]/1_000_000:.1f} m')
m[3].metric(U["cpm"], inr_full(c["cpm"]))
m[4].metric(U["bonus"], inr(c["bonus"]))
if over:
    st.markdown(f'<div class="warn">{U["over"]}</div>', unsafe_allow_html=True)

t1, t2, t3, t4, t5 = st.tabs(["The plan", "The numbers", "Release order", "The argument", "Export"])

with t1:
    st.markdown(f'**{d.get("insight","")}**')
    st.write("")
    cc = st.columns(2)
    with cc[0]:
        st.markdown("##### " + U["who"])
        for a in d.get("audience", []):
            st.markdown(f"- {a}")
    with cc[1]:
        st.markdown("##### " + U["runs"])
        for t in d.get("timeline", []):
            st.markdown(f"**{t.get('phase','')}**  {t.get('action','')}")
    st.markdown("##### " + U["sched"])
    show = df[["Line", "Detail", "Loading", "Qty", "Rate", "Gross", "Why"]].copy()
    show.columns = [U["line"], U["detail"], U["loading"], U["qty"], U["rate"], U["gross"], U["why"]]
    show[U["rate"]] = show[U["rate"]].map(inr_full)
    show[U["gross"]] = show[U["gross"]].map(inr_full)
    show[U["qty"]] = show[U["qty"]].map(lambda x: f"{x:,.0f}")
    st.dataframe(show, use_container_width=True, hide_index=True)

with t2:
    a, b = st.columns([1, 1])
    with a:
        st.markdown("##### " + U["money"])
        bygroup = df.groupby("Group")["Gross"].sum().reset_index()
        st.bar_chart(bygroup, x="Group", y="Gross", color="#C8102E", height=260)
    with b:
        st.markdown("##### " + U["reachsrc"])
        byreach = df.groupby("Group")["Reach"].sum().reset_index()
        st.bar_chart(byreach, x="Group", y="Reach", color="#1B2A4A", height=260)
    st.markdown("##### " + U["settle"])
    ladder = pd.DataFrame([
        ["Gross, card rate", c["gross"]],
        [f"Negotiated discount, {discount} percent", -c["discount"]],
        ["Agency commission, 15 percent" if agency else "Planning fee, 12 percent",
         -c["commission"] if agency else c["fee"]],
        ["Net", c["net"]],
        ["GST", c["gst"]],
        ["Payable by the advertiser", c["payable"]],
    ], columns=["Step", "Amount"])
    ladder["Amount"] = ladder["Amount"].map(inr_full)
    st.dataframe(ladder, use_container_width=True, hide_index=True)
    st.caption("Space carries 5 percent GST, content and events carry 18 percent. "
               f"Credit period {D.CREDIT_DAYS} days from the release order.")

with t3:
    ro = f"RO/{date.today().strftime('%Y%m')}/{abs(hash(d.get('title','x'))) % 9000 + 1000}"
    st.markdown(f"##### Release order {ro}")
    st.write(f"Material deadline: {(date.today()+timedelta(days=7)).strftime('%d %B %Y')} for print, "
             f"{(date.today()+timedelta(days=4)).strftime('%d %B %Y')} for digital.")
    ro_df = df[["Group", "Line", "Qty", "Unit", "Gross"]].copy()
    ro_df["Gross"] = ro_df["Gross"].map(inr_full)
    st.dataframe(ro_df, use_container_width=True, hide_index=True)
    st.markdown(f'<div class="ok">Net payable {inr_full(c["payable"])} including tax. '
                f'Credit {D.CREDIT_DAYS} days. Cancellation, 14 days notice for print, 7 for digital.</div>',
                unsafe_allow_html=True)

with t4:
    st.markdown("##### " + U["measure"])
    for k in d.get("kpis", []):
        st.markdown(f"- {k}")
    st.markdown("##### " + U["risk"])
    st.write(d.get("risk", ""))
    st.markdown("##### " + U["whyus"])
    st.write(U["whyus_body"])

with t5:
    md = [f"# {d.get('title','')}", "", d.get("objective", ""), "", "## Insight", d.get("insight", ""), "",
          "## Schedule", "", "| Line | Qty | Rate | Gross |", "| --- | --- | --- | --- |"]
    for l in lines:
        md.append(f'| {l["Line"]} | {l["Qty"]:,.0f} {l["Unit"]} | {inr_full(l["Rate"])} | {inr_full(l["Gross"])} |')
    md += ["", f'**Net {inr_full(c["net"])}, payable with tax {inr_full(c["payable"])}, '
               f'reach {c["reach"]/1_000_000:.1f} million, CPM {inr_full(c["cpm"])}**', "",
           "## Risk", d.get("risk", ""), "", "_Prototype. Rates illustrative._"]
    md = "\n".join(md)
    st.code(md, language="markdown")
    st.download_button("Download Markdown", md, file_name="media_plan.md", use_container_width=True)
    st.download_button("Download the schedule as CSV", df.to_csv(index=False),
                       file_name="schedule.csv", use_container_width=True)
