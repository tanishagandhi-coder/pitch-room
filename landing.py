"""The product site, rendered inside the app so both look the same."""

import streamlit.components.v1 as components

LANDING = r"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>Pitch Room by Kenja</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Figtree:wght@400;500;600;700;800&family=Inter:wght@400;500;600&family=Noto+Sans+JP:wght@400;500;700&family=Noto+Sans+Devanagari:wght@400;500;700&display=swap" rel="stylesheet">
<style>
:root{
  color-scheme: light;
  --bg:#FAF7F3; --panel:#FFFFFF; --ink:#15110F; --body:#4A443F; --muted:#8A827B;
  --line:#EDE6DE; --line2:#F5F0EA;
  --orange:#E8491F; --orange-soft:#FDEFE9;
  --radius:18px;
  padding-top:env(safe-area-inset-top,0px); padding-bottom:env(safe-area-inset-bottom,0px);
  box-sizing:border-box;
}
@media (prefers-color-scheme: dark){ :root:not([data-theme="light"]){
  color-scheme: dark;
  --bg:#121110; --panel:#1B1917; --ink:#F6F2EE; --body:#C9C2BB; --muted:#8E867F;
  --line:#2A2724; --line2:#211E1C; --orange:#FF6A42; --orange-soft:#2B1711;
}}
:root[data-theme="dark"]{
  color-scheme: dark;
  --bg:#121110; --panel:#1B1917; --ink:#F6F2EE; --body:#C9C2BB; --muted:#8E867F;
  --line:#2A2724; --line2:#211E1C; --orange:#FF6A42; --orange-soft:#2B1711;
}
*{box-sizing:border-box}
html{scroll-behavior:smooth; scroll-padding-top:calc(96px + env(safe-area-inset-top,0px))}
body{margin:0;background:var(--bg);color:var(--body);
  font-family:Inter,'Noto Sans JP','Noto Sans Devanagari',system-ui,sans-serif;
  font-size:16px;line-height:1.6;-webkit-font-smoothing:antialiased}
h1,h2,h3,h4,.d{font-family:Figtree,'Noto Sans JP','Noto Sans Devanagari',system-ui,sans-serif;
  color:var(--ink);font-weight:700;letter-spacing:-.025em;line-height:1.05;margin:0}
h1{font-size:clamp(2.4rem,5.4vw,4.2rem)}
h2{font-size:clamp(1.8rem,3.4vw,2.8rem)}
h3{font-size:1.15rem;letter-spacing:-.01em}
p{margin:0 0 14px;max-width:62ch}
a{color:inherit}
.wrap{max-width:1140px;margin:0 auto;padding:0 22px}

/* floating pill nav */
.navwrap{position:relative;z-index:50;padding:14px 0 0;padding-top:calc(14px + env(safe-area-inset-top,0px))}
body::before{content:"";position:fixed;inset:0 0 auto;height:env(safe-area-inset-top,0px);background:var(--bg);z-index:60}
nav{background:var(--panel);border:1px solid var(--line);border-radius:999px;
  display:flex;align-items:center;gap:8px;padding:9px 10px 9px 18px;box-shadow:0 6px 28px rgba(20,12,6,.06)}
.logo{display:flex;align-items:center;gap:9px;font-family:Figtree,sans-serif;font-weight:700;color:var(--ink);font-size:1.02rem}
.logo i{width:26px;height:26px;border-radius:8px;background:var(--orange);display:inline-flex;
  align-items:center;justify-content:center;color:#fff;font-style:normal;font-size:.8rem;font-weight:800}
nav .links{display:flex;gap:4px;margin-left:16px}
nav .links a{text-decoration:none;color:var(--body);font-size:.88rem;padding:7px 12px;border-radius:999px}
nav .links a:hover{background:var(--line2);color:var(--ink)}
nav .sp{flex:1}
.btn{display:inline-flex;align-items:center;gap:7px;border:0;cursor:pointer;font:inherit;font-weight:600;
  font-size:.9rem;padding:11px 20px;border-radius:999px;text-decoration:none;font-family:Figtree,sans-serif}
.btn.o{background:var(--orange);color:#fff}
.btn.k{background:var(--ink);color:var(--bg)}
.btn.g{background:transparent;color:var(--ink);border:1px solid var(--line)}
.btn:hover{opacity:.92}
.iconbtn{border:1px solid var(--line);background:transparent;color:var(--body);width:36px;height:36px;
  border-radius:50%;cursor:pointer;font-size:.85rem}
@media(max-width:860px){nav .links{display:none}}

/* hero */
.hero{text-align:center;padding:72px 0 10px}
.eyebrow{display:inline-flex;align-items:center;gap:8px;background:var(--panel);border:1px solid var(--line);
  border-radius:999px;padding:6px 14px;font-size:.82rem;color:var(--body);margin-bottom:26px}
.eyebrow i{width:7px;height:7px;border-radius:50%;background:var(--orange);font-style:normal}
.hero h1{max-width:16ch;margin:0 auto}
.hero .sub{max-width:54ch;margin:20px auto 24px;font-size:1.08rem;color:var(--muted)}
.chips{display:flex;gap:9px;justify-content:center;flex-wrap:wrap;margin-bottom:28px}
.chip{background:var(--panel);border:1px solid var(--line);border-radius:999px;padding:9px 16px;font-size:.87rem}
.cta{display:flex;gap:12px;justify-content:center;align-items:center;flex-wrap:wrap}
.cta .note{font-size:.84rem;color:var(--muted);width:100%;margin-top:10px}

/* app preview */
.shot{margin:44px auto 0;max-width:980px;background:var(--panel);border:1px solid var(--line);
  border-radius:var(--radius);overflow:hidden;box-shadow:0 20px 60px rgba(20,12,6,.09)}
.shot .bar{display:flex;gap:6px;padding:12px 16px;border-bottom:1px solid var(--line2);align-items:center}
.shot .bar u{width:10px;height:10px;border-radius:50%;background:var(--line);text-decoration:none}
.shot .bar span{margin-left:12px;font-size:.76rem;color:var(--muted)}
.mock{display:grid;grid-template-columns:230px 1fr;min-height:330px}
.mock .side{border-right:1px solid var(--line2);padding:16px;background:var(--bg)}
.mock .side b{font-size:.8rem;color:var(--ink);display:block;margin-bottom:10px;font-family:Figtree,sans-serif}
.mock .fld{height:9px;border-radius:5px;background:var(--line);margin-bottom:9px}
.mock .fld.s{width:60%} .mock .fld.m{width:85%}
.mock .go{margin-top:14px;height:30px;border-radius:8px;background:var(--orange)}
.mock .main{padding:20px 22px}
.kpis{display:grid;grid-template-columns:repeat(4,1fr);gap:10px;margin-bottom:16px}
.kpi{border:1px solid var(--line2);border-radius:12px;padding:10px 12px}
.kpi b{display:block;font-family:Figtree,sans-serif;font-size:1.15rem;color:var(--ink)}
.kpi span{font-size:.64rem;letter-spacing:.07em;text-transform:uppercase;color:var(--muted)}
.rowline{display:flex;justify-content:space-between;padding:9px 0;border-bottom:1px solid var(--line2);font-size:.82rem}
.rowline b{color:var(--ink);font-weight:500}
.rowline span{color:var(--muted);font-variant-numeric:tabular-nums}

/* sections */
section{padding:86px 0}
.tag{font-size:.78rem;font-weight:600;color:var(--orange);letter-spacing:.06em;text-transform:uppercase;margin-bottom:12px}
.lede{font-size:1.05rem;color:var(--muted);max-width:60ch}
.grid3{display:grid;grid-template-columns:repeat(3,1fr);gap:16px;margin-top:34px}
.grid2{display:grid;grid-template-columns:1fr 1fr;gap:34px;align-items:center}
@media(max-width:880px){.grid3,.grid2,.mock{grid-template-columns:1fr}.mock .side{display:none}}
.card{background:var(--panel);border:1px solid var(--line);border-radius:var(--radius);padding:24px}
.card h3{margin-bottom:9px}
.card p{font-size:.93rem;color:var(--muted);margin:0}
.num{display:flex;gap:14px;align-items:flex-start;background:var(--panel);border:1px solid var(--line);
  border-radius:14px;padding:16px 18px;margin-bottom:10px;cursor:pointer;transition:border-color .18s}
.num:hover{border-color:var(--orange)}
.num.on{border-color:var(--orange);background:var(--orange-soft)}
.num i{flex:none;width:30px;height:30px;border-radius:50%;background:var(--bg);border:1px solid var(--line);
  display:flex;align-items:center;justify-content:center;font-style:normal;font-size:.8rem;font-weight:700;
  color:var(--ink);font-family:Figtree,sans-serif}
.num.on i{background:var(--orange);color:#fff;border-color:var(--orange)}
.num b{display:block;color:var(--ink);font-family:Figtree,sans-serif;font-size:1rem;margin-bottom:3px}
.num p{font-size:.88rem;margin:0;color:var(--muted)}
.panelbox{background:var(--panel);border:1px solid var(--line);border-radius:var(--radius);padding:26px;min-height:300px}
.langrow{display:flex;gap:8px;flex-wrap:wrap;margin:22px 0}
.lang{background:var(--panel);border:1px solid var(--line);border-radius:999px;padding:9px 18px;cursor:pointer;
  font:inherit;font-size:.9rem;color:var(--body)}
.lang[aria-pressed="true"]{background:var(--ink);color:var(--bg);border-color:var(--ink)}
.quote{font-family:Figtree,sans-serif;font-size:clamp(1.4rem,2.6vw,2rem);color:var(--ink);line-height:1.25;
  letter-spacing:-.02em;max-width:22ch}
.road{display:grid;grid-template-columns:repeat(4,1fr);gap:14px;margin-top:34px}
@media(max-width:880px){.road{grid-template-columns:1fr}}
.stage{background:var(--panel);border:1px solid var(--line);border-radius:14px;padding:20px;position:relative}
.stage.now{border-color:var(--orange)}
.stage u{text-decoration:none;font-size:.7rem;letter-spacing:.08em;text-transform:uppercase;color:var(--muted)}
.stage.now u{color:var(--orange)}
.stage h4{margin:8px 0 7px;font-size:1rem}
.stage p{font-size:.86rem;color:var(--muted);margin:0}
details{background:var(--panel);border:1px solid var(--line);border-radius:14px;padding:16px 20px;margin-bottom:10px}
summary{cursor:pointer;font-family:Figtree,sans-serif;font-weight:600;color:var(--ink);font-size:1rem;list-style:none}
summary::-webkit-details-marker{display:none}
summary::after{content:"+";float:right;color:var(--orange);font-weight:700}
details[open] summary::after{content:"–"}
details p{margin:12px 0 0;font-size:.93rem;color:var(--muted)}
.band{background:var(--ink);color:var(--bg);border-radius:26px;padding:56px 40px;text-align:center;margin:0 0 70px}
.band h2{color:var(--bg);max-width:20ch;margin:0 auto 14px}
.band p{color:#B9B2AB;margin:0 auto 24px;max-width:48ch}
footer{border-top:1px solid var(--line);padding:30px 0 50px;font-size:.85rem;color:var(--muted)}
.foot{display:flex;justify-content:space-between;gap:16px;flex-wrap:wrap}
</style>
</head>
<body>

<div class="navwrap"><div class="wrap"><nav>
  <span class="logo"><i>PR</i>Pitch<span style="font-weight:800">Room</span></span>
  <span class="links">
    <a href="#how">How it works</a>
    <a href="#numbers">The numbers</a>
    <a href="#languages">Languages</a>
    <a href="#method">The method</a>
    <a href="#roadmap">Where it goes</a>
  </span>
  <span class="sp"></span>
  <button class="iconbtn" id="theme" title="Light or dark">◐</button>
  <a class="btn o" href="https://pitch-room-xvut6discstzzfbhmwpjfz.streamlit.app" target="_blank" rel="noopener">Open the prototype ↗</a>
</nav></div></div>

<header class="hero"><div class="wrap">
  <span class="eyebrow"><i></i>Built for media groups, with Kenja in Tokyo</span>
  <h1 id="heroH">Every brief arrives as a costed media plan.</h1>
  <p class="sub" id="heroS">Paste what the advertiser asked for. Get the placements, the quantities, the price from your own rate card, the tax, the reach and the release order. In about twenty seconds.</p>
  <div class="chips">
    <span class="chip">Any brief in</span>
    <span class="chip">Priced from your own card</span>
    <span class="chip">English, Japanese and Hindi</span>
  </div>
  <div class="cta">
    <a class="btn k" href="https://pitch-room-xvut6discstzzfbhmwpjfz.streamlit.app" target="_blank" rel="noopener">Open the prototype ↗</a>
    <a class="btn g" href="#how">See how it works</a>
    <span class="note">A working proof of concept. Sample rate card, real arithmetic.</span>
  </div>

  <div class="shot">
    <div class="bar"><u></u><u></u><u></u><span>Pitch Room</span></div>
    <div class="mock">
      <div class="side">
        <b>The brief</b>
        <div class="fld m"></div><div class="fld"></div><div class="fld s"></div>
        <b style="margin-top:18px">Budget and length</b>
        <div class="fld"></div><div class="fld s"></div>
        <div class="go"></div>
      </div>
      <div class="main">
        <div class="kpis">
          <div class="kpi"><b>₹2.35 cr</b><span>Payable</span></div>
          <div class="kpi"><b>21.2 m</b><span>Reach</span></div>
          <div class="kpi"><b>₹1,036</b><span>Per thousand</span></div>
          <div class="kpi"><b>7</b><span>Placements</span></div>
        </div>
        <div class="rowline"><b>Delhi NCR, full page, page 3</b><span>₹1,33,12,000</span></div>
        <div class="rowline"><b>Navbharat Times, Hindi display</b><span>₹11,40,000</span></div>
        <div class="rowline"><b>Sponsored article, desk written</b><span>₹26,00,000</span></div>
        <div class="rowline"><b>Industry roundtable</b><span>₹22,00,000</span></div>
      </div>
    </div>
  </div>
</div></header>

<section id="how" style="padding-top:60px"><div class="wrap">
  <div class="tag">How it works</div>
  <h2>Four steps. Three of them run on their own.</h2>
  <p class="lede">The seller writes the brief and checks the result. Everything in between is the software.</p>
  <div class="grid2" style="margin-top:34px">
    <div>
      <div class="num on" data-s="0"><i>01</i><div><b>Paste the brief</b><p>However it arrived. An email, a call note, a one line request from a client.</p></div></div>
      <div class="num" data-s="1"><i>02</i><div><b>We read your own files</b><p>Rate card, past campaigns, audience studies. The plan is built from what the house already knows.</p></div></div>
      <div class="num" data-s="2"><i>03</i><div><b>The plan is written and priced</b><p>Placements and quantities are proposed. Every rupee is calculated from the card, never guessed.</p></div></div>
      <div class="num" data-s="3"><i>04</i><div><b>Out comes the paperwork</b><p>Schedule, money ladder, reach, cost per thousand and a release order ready to send.</p></div></div>
    </div>
    <div class="panelbox" id="stage"></div>
  </div>
</div></section>

<section id="numbers" style="background:var(--panel);border-top:1px solid var(--line);border-bottom:1px solid var(--line)">
 <div class="wrap">
  <div class="grid2">
    <div>
      <div class="tag">Why it is not a chatbot</div>
      <div class="quote">The model picks the mix. The software does the money.</div>
      <p style="margin-top:20px">A language model that states a price will eventually say forty five lakh when it means four and a half. Here it never touches a number. It proposes placements and quantities, and the code prices them from the rate card, applies the loading for a premium position, takes off the negotiated discount, deducts agency commission, adds the right tax on space and on services, and settles on a payable figure.</p>
      <p>Which means a number on screen is a number you can put in front of a client.</p>
    </div>
    <div class="card">
      <h3>How the money settles</h3>
      <div class="rowline"><b>Gross, card rate</b><span>₹3,15,22,000</span></div>
      <div class="rowline"><b>Negotiated discount, 18 percent</b><span>−₹56,73,960</span></div>
      <div class="rowline"><b>Agency commission, 15 percent</b><span>−₹38,77,206</span></div>
      <div class="rowline"><b>Net to the publisher</b><span>₹2,19,70,834</span></div>
      <div class="rowline"><b>Tax, 5 percent on space, 18 on services</b><span>₹15,38,000</span></div>
      <div class="rowline" style="border-bottom:0"><b style="color:var(--orange)">Payable</b><span style="color:var(--orange)">₹2,35,08,834</span></div>
      <p style="font-size:.8rem;color:var(--muted);margin-top:14px">Illustrative figures on a sample card. The logic is the real thing.</p>
    </div>
  </div>
 </div>
</section>

<section id="languages"><div class="wrap">
  <div class="tag">Languages</div>
  <h2>One plan, three languages, one click.</h2>
  <p class="lede">Not a translation of the output. The whole plan is written in the language, including the interface, the tables and the release order.</p>
  <div class="langrow">
    <button class="lang" data-l="en" aria-pressed="true">English</button>
    <button class="lang" data-l="ja" aria-pressed="false">日本語</button>
    <button class="lang" data-l="hi" aria-pressed="false">हिन्दी</button>
  </div>
  <div class="card" style="max-width:720px">
    <h3 id="lh">Trust before volume</h3>
    <p id="lp" style="margin-top:8px">Indian families do not buy an unfamiliar car on specification, they buy it on who else they have seen driving one. The job is not awareness, it is permission.</p>
  </div>
  <p style="margin-top:22px;color:var(--muted);font-size:.92rem">Useful twice over: for a Japanese advertiser entering India, and for Hindi speaking clients who are tired of tools that only work in English.</p>
</div></section>

<section id="method" style="background:var(--panel);border-top:1px solid var(--line);border-bottom:1px solid var(--line)">
 <div class="wrap">
  <div class="tag">The working method</div>
  <h2>Four Japanese habits, built into the proposal.</h2>
  <p class="lede">Every AI company will show you a model that writes. This is the part they cannot copy, because it is how a company behaves rather than what it builds.</p>
  <div class="grid3">
    <div class="card"><h3>根回し Nemawashi</h3><p>Everyone who can say no has been spoken to privately before the meeting. The meeting then confirms a decision rather than making one.</p></div>
    <div class="card"><h3>稟議 Ringi</h3><p>One approval sheet travels to each approver in order, and each records what they signed. Slower to start, far faster to finish.</p></div>
    <div class="card"><h3>報連相 Horenso</h3><p>A written report every week, unprompted, good news or bad. No client should have to ask how their campaign is doing.</p></div>
  </div>
  <div class="card" style="margin-top:16px">
    <h3>反省会 Hansei kai</h3>
    <p>At the end we present what did not work before what did, in writing. An agency that only reports its wins is managing the client rather than serving them.</p>
  </div>
 </div>
</section>

<section id="roadmap"><div class="wrap">
  <div class="tag">Where it goes</div>
  <h2>A proof of concept today. A line of business in a year.</h2>
  <p class="lede">The prototype proves one plan. The value is in what it becomes once it is running on real data.</p>
  <div class="road">
    <div class="stage now"><u>Now, six weeks</u><h4>The proof</h4><p>One desk, real briefs, your own rate card. One measurable number at the end: hours saved per plan.</p></div>
    <div class="stage"><u>Next</u><h4>The pitch library</h4><p>Every plan searchable. Six months in, a seller sees what was proposed to every car brand, what sold, at what discount.</p></div>
    <div class="stage"><u>Then</u><h4>Outcome feedback</h4><p>Real delivery goes back in, so the next plan is built from what actually worked, not only from the card.</p></div>
    <div class="stage"><u>Later</u><h4>The Japan desk</h4><p>Japanese brands entering India, Indian brands entering Japan, planned in both languages. Nobody else can offer this.</p></div>
  </div>
</div></section>

<section style="padding-top:0"><div class="wrap">
  <div class="tag">Questions people ask first</div>
  <h2 style="margin-bottom:28px">Short answers.</h2>
  <details open><summary>Is this selling us software?</summary><p>No. The proposal on the table is a revenue share: you take the product to your own advertisers under your brand, we build and run it. The proof of concept is a fixed fee that is credited back against the first year.</p></details>
  <details><summary>Where do the prices come from?</summary><p>A rate card held as ordinary data, not inside the model. Print is priced per square centimetre by edition with position and season loading. Digital is priced on cost per thousand. Swap in your card and every number on screen changes.</p></details>
  <details><summary>What happens to our data?</summary><p>In the prototype, nothing is stored. Each session exists in the browser and disappears when the tab closes. In production the corpus sits in your own database and never leaves it.</p></details>
  <details><summary>How long to put this on our own rate card?</summary><p>Six weeks for one department, including your card, your branding, your templates and a login for your team.</p></details>
  <details><summary>Can it replace a media planner?</summary><p>No, and it should not try. It removes the two hours of assembling and costing, so the planner spends their time on the argument, which is the part a client actually pays for.</p></details>
</div></section>

<div class="wrap"><div class="band">
  <h2>See it build a plan from a brief.</h2>
  <p>The prototype is live. Bring a real brief and watch it priced in front of you.</p>
  <a class="btn o" href="https://pitch-room-xvut6discstzzfbhmwpjfz.streamlit.app" target="_blank" rel="noopener">Open the prototype ↗</a>
</div></div>

<footer><div class="wrap foot">
  <span>Pitch Room, a Kenja prototype. Tokyo, 2026.</span>
  <span>Sample data throughout. Built for a conversation, not for production.</span>
</div></footer>

<script>
var STAGES = [
 {h:"The brief, however it arrived",
  b:["A Japanese automotive manufacturer is bringing its first electric SUV to India in Q1.",
     "They are unknown to Indian families outside a small enthusiast group.",
     "They want trust before volume. Launch in the eight metros first."],
  f:"Nothing to fill in. Paste and go."},
 {h:"What the house already knows",
  b:["Rate card 2026, nine products across print, digital, audio and events",
     "Case: automotive launch, Japanese carmaker, 2025",
     "Audience study, eight metros, language and income split",
     "Language market note, Hindi outsells English outside the metros"],
  f:"Four sources retrieved in under a second."},
 {h:"Written, then priced",
  b:["Delhi NCR, full page, page 3, two insertions",
     "Navbharat Times, Hindi display, six million impressions",
     "Sponsored article, desk written, four pieces",
     "Industry roundtable with coverage, one"],
  f:"The model chose the mix. The software priced every line."},
 {h:"The paperwork, ready to send",
  b:["Schedule with rate, quantity and loading on every line",
     "Money ladder: gross, discount, commission, tax, payable",
     "Reach, cost per thousand, and a warning if it breaks budget",
     "Release order with material deadlines and credit terms"],
  f:"Export as Markdown or a spreadsheet."}
];
function paint(i){
  var s = STAGES[i];
  document.getElementById("stage").innerHTML =
    '<div class="tag">Step 0' + (i+1) + '</div><h3 style="margin-bottom:14px">' + s.h + '</h3>' +
    s.b.map(function(x){ return '<div class="rowline"><b>' + x + '</b></div>'; }).join("") +
    '<p style="margin-top:16px;font-size:.86rem;color:var(--muted)">' + s.f + '</p>';
  var all = document.querySelectorAll(".num");
  for (var j=0;j<all.length;j++) all[j].classList.toggle("on", j === i);
}
document.querySelectorAll(".num").forEach(function(n){
  n.addEventListener("click", function(){ paint(+n.dataset.s); });
});
paint(0);

var L = {
 en:{h:"Every brief arrives as a costed media plan.",
     s:"Paste what the advertiser asked for. Get the placements, the quantities, the price from your own rate card, the tax, the reach and the release order. In about twenty seconds.",
     ch:"Trust before volume",
     cp:"Indian families do not buy an unfamiliar car on specification, they buy it on who else they have seen driving one. The job is not awareness, it is permission."},
 ja:{h:"すべての要望が、費用まで入った媒体プランになります。",
     s:"広告主からの要望を貼り付けるだけ。掲載枠、数量、自社の料金表に基づく金額、税、リーチ、発注書までそろいます。所要時間は約20秒です。",
     ch:"量より先に、信頼を",
     cp:"インドの家族は知らない自動車を仕様では買いません。誰が乗っているかで判断します。必要なのは認知ではなく、許可です。"},
 hi:{h:"हर ब्रीफ, लागत सहित मीडिया प्लान बनकर आता है।",
     s:"विज्ञापनदाता की माँग पेस्ट कीजिए। प्लेसमेंट, मात्रा, अपने रेट कार्ड से कीमत, कर, पहुँच और रिलीज़ ऑर्डर, सब मिलेगा। लगभग बीस सेकंड में।",
     ch:"पहले भरोसा, फिर बिक्री",
     cp:"भारतीय परिवार अनजान कार स्पेसिफिकेशन देखकर नहीं खरीदते, वे देखते हैं कि और कौन चला रहा है। काम जागरूकता का नहीं, स्वीकृति का है।"}
};
document.querySelectorAll(".lang").forEach(function(b){
  b.addEventListener("click", function(){
    document.querySelectorAll(".lang").forEach(function(x){ x.setAttribute("aria-pressed","false"); });
    b.setAttribute("aria-pressed","true");
    var l = L[b.dataset.l];
    document.getElementById("heroH").textContent = l.h;
    document.getElementById("heroS").textContent = l.s;
    document.getElementById("lh").textContent = l.ch;
    document.getElementById("lp").textContent = l.cp;
  });
});

document.getElementById("theme").addEventListener("click", function(){
  var cur = document.documentElement.getAttribute("data-theme");
  var dark = cur ? cur === "dark" : window.matchMedia("(prefers-color-scheme: dark)").matches;
  document.documentElement.setAttribute("data-theme", dark ? "light" : "dark");
});
</script>
</body>
</html>
"""


def render(height=5400):
    components.html(LANDING, height=height, scrolling=True)
