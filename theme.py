"""Original neon editorial theme for Dollars & Devices.

Built from CSS shapes and gradients; no third-party game artwork or brand assets.
"""
import streamlit as st

BANK_COLOURS = {
    "RBC": "#4d95ff",
    "TD": "#4ce5a2",
    "Scotiabank": "#ff687b",
    "BMO": "#27cfff",
    "CIBC": "#ef71b4",
    "National Bank": "#bfa2ff",
}

PINK = "#ff55b7"
CYAN = "#41ddff"
VIOLET = "#a28aff"
GOLD = "#ffd47c"
NAVY = "#090b23"

CSS = r"""
<style>
:root {
  --pink:#ff55b7; --cyan:#41ddff; --violet:#a28aff; --gold:#ffd47c;
  --ink:#f5f5ff; --muted:#afb4d7; --deep:#090b23; --panel:#151633;
}
html, body, [class*="css"], [data-testid="stAppViewContainer"] {font-family: "Trebuchet MS", Arial, sans-serif;}
.stApp {
    color:var(--ink);
    background:
       radial-gradient(ellipse 45% 35% at 85% 2%, rgba(255,85,183,.17), transparent 95%),
       radial-gradient(ellipse 55% 40% at 5% 25%, rgba(65,221,255,.10), transparent 95%),
       linear-gradient(155deg, #080a20 0%, #171235 55%, #08172c 100%);
}
.block-container {max-width:1330px; padding-top:1.3rem; padding-bottom:4rem;}
h1,h2,h3 {letter-spacing:-.045em !important; color:#fff !important;}
h1 {font-size:clamp(2.4rem,5vw,4.2rem)!important; font-weight:900!important;}
h2 {font-size:2rem!important; font-weight:800!important;}
h3 {font-weight:800!important;}
p, label, span {color:inherit;}
[data-testid="stSidebar"] {
   background:linear-gradient(175deg, #17132f, #0d1530 60%, #101029);
   border-right:1px solid rgba(65,221,255,.26);
}
[data-testid="stSidebar"] [data-testid="stMarkdownContainer"] p {color:#d6ddf6;}
[data-testid="stMetric"] {
   background:linear-gradient(138deg,rgba(25,27,58,.95),rgba(17,22,49,.96));
   border:1px solid rgba(65,221,255,.23); border-left:4px solid var(--cyan);
   border-radius:16px; padding:17px 19px; min-height:116px;
   box-shadow:0 8px 30px rgba(5,4,22,.23);
}
[data-testid="stMetricLabel"] {font-size:.82rem!important; color:#bfc6e3!important;}
[data-testid="stMetricValue"] {font-weight:900!important; color:white!important;}
[data-testid="stMetricDelta"] {font-weight:700!important;}
div[data-testid="stTabs"] button[role="tab"] {
   color:#d9dcf6; font-weight:700; border-radius:8px 8px 0 0; padding:10px 13px;
}
div[data-testid="stTabs"] button[aria-selected="true"] {color:var(--cyan)!important;}
div[data-testid="stVerticalBlock"] > div {scroll-margin-top:24px;}
div.stButton > button, div.stDownloadButton > button {
    color:#091024!important;
    background:linear-gradient(100deg,var(--cyan),#8cecff)!important;
    border:0!important; border-radius:11px!important; font-weight:800!important;
}
div.stButton > button:hover, div.stDownloadButton > button:hover {filter:brightness(1.12);}
[data-testid="stAlert"] {border-radius:12px;}
.neon-hero {
  position:relative; overflow:hidden; isolation:isolate;
  border:1px solid rgba(65,221,255,.4); border-radius:24px;
  padding:27px 31px 31px; margin:0 0 24px;
  background:
    radial-gradient(ellipse at 79% 25%, rgba(255,85,183,.35),transparent 28%),
    linear-gradient(105deg,rgba(10,18,47,.98) 10%,rgba(26,18,70,.98) 65%,rgba(42,24,89,.95));
  box-shadow:0 13px 50px rgba(7,6,30,.36), inset 0 0 50px rgba(65,221,255,.045);
}
.neon-hero:before {
  content:""; position:absolute; z-index:-1; right:-12%; bottom:-72%;
  width:79%; height:110%; border-radius:50%;
  background:repeating-radial-gradient(circle,rgba(255,91,186,.42) 0 1px,transparent 2px 12px);
  transform:rotate(-12deg);
}
.neon-hero:after {
  content:""; position:absolute; z-index:-1; right:5%; bottom:-110px;
  width:48%; height:240px;
  background:
    linear-gradient(transparent 48%,rgba(65,221,255,.29) 50%,transparent 52%) 0 0/100% 31px,
    linear-gradient(90deg,transparent 48%,rgba(65,221,255,.20) 50%,transparent 52%) 0 0/49px 100%;
  transform:perspective(180px) rotateX(43deg);
}
.eyebrow {text-transform:uppercase; color:var(--cyan); letter-spacing:.19em; font-size:.71rem; font-weight:900;}
.hero-title {margin:9px 0 8px; font-size:clamp(2.6rem,6.2vw,5.5rem); line-height:.93; font-weight:1000; letter-spacing:-.065em; text-transform:uppercase; color:white; text-shadow:4px 4px 0 #eb3597,7px 7px 0 #143b64;}
.hero-title span {color:var(--cyan);}
.hero-sub {max-width:670px; color:#d5d6ef; font-size:1.02rem; line-height:1.5; margin-top:19px;}
.hero-stamp {display:inline-block; background:#ffdd80; color:#25153a; padding:7px 12px; margin-top:12px; transform:rotate(-2deg); font-size:.69rem; font-weight:900; letter-spacing:.13em; box-shadow:4px 4px 0 #ff55b7;}
.section-flag {color:#91dff9; font-weight:900; font-size:.78rem; letter-spacing:.14em; text-transform:uppercase; margin:15px 0 4px;}
.comic-panel {border:1px solid rgba(175,180,219,.24); border-radius:17px; background:linear-gradient(145deg,rgba(22,26,59,.95),rgba(14,21,45,.94)); padding:20px; margin-bottom:13px; min-height:150px;}
.comic-panel.pink {border-top:4px solid #ff55b7;}
.comic-panel.blue {border-top:4px solid #41ddff;}
.comic-panel.violet {border-top:4px solid #a28aff;}
.comic-panel.gold {border-top:4px solid #ffd47c;}
.comic-panel h3 {font-size:1.27rem!important; margin:9px 0;}
.comic-panel p {color:#d5d6ef; line-height:1.55; font-size:.95rem;}
.neon-caption {color:#adb9dc; font-size:.8rem;}
.bank-stripe {display:flex; gap:6px; flex-wrap:wrap; margin:8px 0 22px;}
.bank-pill {border:1px solid rgba(255,255,255,.22); border-left:5px solid; padding:6px 10px; border-radius:8px; background:#111936; font-weight:800; font-size:.74rem;}
.dollar-shell {border:1px solid rgba(255,85,183,.3); border-radius:18px; padding:19px; background:linear-gradient(130deg,#111831,#251631);}
.cent-grid {display:grid; grid-template-columns:repeat(20,minmax(0,1fr)); gap:3px; margin-top:16px;}
.cent {height:12px; border-radius:2px;}
.cent-cost {background:#ff55b7;}
.cent-profit {background:#41ddff;}
.cent-rest {background:#725b9b;}
.cent-legend {display:flex; flex-wrap:wrap; gap:14px; font-weight:700; font-size:.81rem; margin:13px 0 0;}
.cent-legend i {display:inline-block; width:10px; height:10px; margin-right:5px; border-radius:2px;}
.score-panel {background:rgba(19,23,51,.96); border:1px solid rgba(110,126,185,.25); border-radius:14px; padding:15px 16px; margin-bottom:10px;}
.score-head {display:flex; align-items:center; justify-content:space-between; flex-wrap:wrap; gap:7px;}
.score-title {font-size:1.01rem; font-weight:900;}
.score-note {font-size:.79rem; color:#bdc6e8; margin-top:7px;}
.score-value {font-size:1.33rem; font-weight:900; color:#fff;}
.score-badge {font-size:.68rem; font-weight:900; border-radius:8px; padding:5px 7px; color:#0f1831;}
.score-badge.good {background:#6debba;}
.score-badge.watch {background:#ffcf7e;}
.score-badge.bad {background:#ff7d9b;}
.score-badge.missing {background:#b5b9d4;}
.small-print {font-size:.78rem; color:#abb9d9; line-height:1.5;}
.neon-rule {height:3px; background:linear-gradient(90deg,#ff55b7,#41ddff,transparent); margin:16px 0;}
</style>
"""


def apply_theme() -> None:
    st.markdown(CSS, unsafe_allow_html=True)
