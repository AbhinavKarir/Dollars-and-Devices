"""Restrained executive reporting theme; original branding, no corporate assets."""
import plotly.io as pio
import streamlit as st

NAVY = "#142D4E"
BLUE = "#2459B8"
TEAL = "#087F78"
SLATE = "#64748B"
# Institution accents are used only in the cross-institution comparison chart.
BANK_COLOURS = {
    "RBC": "#2459B8", "TD": "#287348", "Scotiabank": "#B7353C",
    "BMO": "#167A9C", "CIBC": "#84334E", "National Bank": "#77558B",
}

CSS = r"""
<style>
.stApp {background:#F4F6FA; color:#172B45; font-family:"Segoe UI",Arial,sans-serif;}
.block-container {max-width:1320px; padding-top:2rem; padding-bottom:3rem;}
h1,h2,h3 {color:#142D4E; letter-spacing:-.02em;}
h1 {font-size:2rem!important; font-weight:700!important;}
h2 {font-size:1.5rem!important; font-weight:650!important;}
h3 {font-size:1.15rem!important; font-weight:650!important;}
[data-testid="stSidebar"] {background:#EAF0F7; border-right:1px solid #CFD9E6;}
[data-testid="stMetric"] {background:#FFFFFF; border:1px solid #D6DFEA; border-top:3px solid #2459B8; border-radius:8px; padding:18px 20px; min-height:120px;}
[data-testid="stMetricLabel"] {color:#465A72; font-size:.85rem;}
[data-testid="stMetricValue"] {color:#142D4E; font-variant-numeric:tabular-nums; font-weight:650;}
[data-testid="stTabs"] [role="tablist"] {gap:4px; border-bottom:1px solid #CFD9E6; overflow-x:auto;}
[data-testid="stTabs"] button[role="tab"] {color:#465A72; padding:10px 14px; white-space:nowrap;}
[data-testid="stTabs"] button[aria-selected="true"] {color:#2459B8; font-weight:650;}
[data-testid="stTabs"] [data-baseweb="tab-highlight"] {background:#2459B8;}
.stButton > button, .stDownloadButton > button {background:#2459B8; color:white; border:1px solid #2459B8; border-radius:4px; font-weight:600;}
.stButton > button:hover, .stDownloadButton > button:hover {background:#173E86; color:white; border-color:#173E86;}
button:focus-visible, a:focus-visible {outline:3px solid #087F78!important; outline-offset:3px;}
.report-header {border-bottom:2px solid #142D4E; padding:0 0 18px; margin-bottom:16px;}
.report-header h1 {margin:4px 0; padding:0;}
.report-header p {color:#465A72; margin:4px 0 12px;}
.eyebrow {color:#52657A; text-transform:uppercase; letter-spacing:.09em; font-size:.72rem; font-weight:650;}
.sample-label {display:inline-block; color:#334E6E; background:#E6EDF7; padding:5px 8px; border-radius:3px; font-size:.72rem; font-weight:600;}
.insight-panel {background:white; border:1px solid #D6DFEA; border-left:3px solid #2459B8; border-radius:4px; padding:16px 20px; margin-bottom:12px;}
.insight-panel.sustainability {border-left-color:#087F78;}
.insight-panel h3 {margin:6px 0;}
.insight-panel p {color:#465A72; line-height:1.6; margin-bottom:0;}
.score-panel {background:white; border:1px solid #D6DFEA; border-radius:4px; padding:16px; margin-bottom:10px;}
.score-head {display:flex; align-items:center; justify-content:space-between; flex-wrap:wrap; gap:8px; margin-top:6px;}
.score-title {font-weight:600;}
.score-value {color:#142D4E; font-size:1.3rem; font-weight:650; font-variant-numeric:tabular-nums;}
.score-note {font-size:.82rem; color:#465A72; margin-top:8px; line-height:1.5;}
.score-badge {font-size:.75rem; font-weight:650; border-radius:3px; padding:4px 8px;}
.score-badge.good {color:#075B50; background:#DCF1EB;}
.score-badge.watch {color:#785000; background:#FFF0CC;}
.score-badge.bad {color:#9B2632; background:#FBE6E8;}
.score-badge.missing {color:#465A72; background:#EAF0F7;}
@media(max-width:750px) {
 .block-container {padding-top:1rem; padding-left:1rem; padding-right:1rem;}
 .report-header h1 {font-size:1.7rem!important;}
 .insight-panel {padding:14px;}
 [data-testid="stMetric"] {padding:14px 16px;}
}
</style>
"""


def apply_theme() -> None:
    """Use one light chart template and CSS palette across every reporting tab."""
    pio.templates["executive"] = pio.templates["plotly_white"]
    pio.templates["executive"].layout.update(
        font=dict(family="Segoe UI, Arial, sans-serif", color=NAVY, size=13),
        paper_bgcolor="#FFFFFF", plot_bgcolor="#FFFFFF",
        colorway=[BLUE, TEAL, SLATE],
        xaxis=dict(gridcolor="#E4EAF2", zerolinecolor="#CFD9E6", automargin=True),
        yaxis=dict(gridcolor="#E4EAF2", zerolinecolor="#CFD9E6", automargin=True),
        margin=dict(l=30, r=30, t=45, b=40),
        legend=dict(orientation="h", y=-0.2),
    )
    pio.templates.default = "executive"
    st.markdown(CSS, unsafe_allow_html=True)

