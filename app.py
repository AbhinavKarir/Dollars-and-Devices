"""Dollars & Devices Neon Edition | Start: streamlit run app.py."""
import streamlit as st
import pandas as pd
import plotly.express as px
from analytics import load_metrics, load_targets, make_scorecard, portfolio_summary, scenario, story_cards
from theme import BANK_COLOURS, PINK, CYAN, VIOLET, apply_theme
from evidence_views import render_kpi_workbench, render_financial_controls
from metric_audit import validate_dataset

st.set_page_config(page_title="Dollars & Devices | Neon Edition", page_icon="💿", layout="wide")
apply_theme()

@st.cache_data
def load_data():
    return load_metrics()

try:
    df = load_data()
    targets = load_targets()
except (ValueError, KeyError, FileNotFoundError) as error:
    st.error(str(error))
    st.stop()

with st.sidebar:
    st.title("💿 NEON CONTROL ROOM")
    bank = st.selectbox("Institution", sorted(df.bank.unique()))
    quarters = sorted(df.quarter.unique())
    quarter = st.selectbox("Quarter", quarters, index=len(quarters) - 1)
    st.info("All financial and device figures are FICTIONAL.")

row = df[(df.bank == bank) & (df.quarter == quarter)].iloc[0]
history = df[df.bank == bank].sort_values("quarter")
earlier = history[history.quarter < quarter]
prev = earlier.iloc[-1] if not earlier.empty else None
current = df[df.quarter == quarter]

st.markdown('<div class="neon-hero"><span class="eyebrow">BUSINESS INTELLIGENCE LAB / ISSUE 01</span><div class="hero-title">DOLLARS <span>&</span><br>DEVICES</div><div class="hero-sub">An operations and performance reporting case study. Verify metrics, trace decisions, and investigate exceptions.</div><div class="hero-stamp">SAMPLE DATA · DEMONSTRATION ONLY</div></div>', unsafe_allow_html=True)

overview_left, overview_right = st.columns([1.12, 1])
with overview_left:
    st.markdown(
        '<div class="neon-overview"><div class="eyebrow">PROJECT BRIEF / START HERE</div>'
        '<h3>Can operating costs and device recovery be measured reliably?</h3>'
        '<p>A junior Business Analyst case study that shows how fictional source records become '
        'management decisions. Compare expenses, profitability and retired technology across '
        'six invented institutional profiles and two periods. Then open KPI proof to verify the '
        'calculations and Cash controls to test a separate fictional household ledger. '
        '<b>This is not actual bank reporting or financial advice.</b></p>'
        '<div class="overview-chips"><span>Define the measure</span>'
        '<span>Check the data</span><span>Find an exception</span><span>Decide what to investigate</span>'
        '</div></div>',
        unsafe_allow_html=True
    )
with overview_right:
    st.image("assets/neon_coast.svg", width="stretch")
    st.caption("Original retro-coast illustration. Neon styling does not replace calculation evidence.")

st.caption("BUILT FOR BUSINESS ANALYSIS · Finance · Operations · Technology assets · Sustainability · Strategy")

st.caption(f"FOCUS: {bank} | {quarter} | Currency: CAD millions | Devices: kilograms")
tabs = st.tabs(["01 · Overview", "02 · KPI proof", "03 · Cash controls", "04 · Scorecards", "05 · Compare & decide", "06 · Stakeholders"])

with tabs[0]:
    st.header("Executive pulse")
    cols = st.columns(4)
    items = [("Efficiency ratio ↓", "efficiency_ratio", True), ("Net income margin ↑", "net_margin", False), ("Recycling rate ↑", "recycling_rate", False)]
    for i, (label, metric, inverse) in enumerate(items):
        delta = None if prev is None else f"{row[metric] - prev[metric]:+.1f} pp"
        cols[i].metric(label, f"{row[metric]:.1f}%", delta, delta_color="inverse" if inverse else "normal")
    cols[3].metric("Retired devices", f"{row.retired_kg:,.0f} kg")
    st.subheader("The 100-cent dollar breakdown")
    cost = max(0, min(100, round(float(row.efficiency_ratio))))
    profit = max(0, min(100-cost, round(float(row.net_margin))))
    tiles = '<i class="cent cent-cost"></i>' * cost + '<i class="cent cent-profit"></i>' * profit + '<i class="cent cent-rest"></i>' * (100-cost-profit)
    st.markdown('<div class="dollar-shell"><div class="eyebrow">ONE REVENUE DOLLAR / 100 SQUARES</div><div class="cent-grid">' + tiles + '</div></div>', unsafe_allow_html=True)
    st.caption(f"Expense {row.efficiency_ratio:.1f} cents | Net income {row.net_margin:.1f} cents | Other / unreconciled {row.residual_cents:.1f} cents. Illustrative, not an audited accounting bridge.")
    st.subheader("Combined six-institution sample portfolio")
    summary = portfolio_summary(df, quarter)
    x, y, z = st.columns(3)
    x.metric("Weighted efficiency", f"{summary['efficiency_ratio']:.1f}%")
    y.metric("Weighted margin", f"{summary['net_margin']:.1f}%")
    z.metric("Weighted recycling", f"{summary['recycling_rate']:.1f}%")

    st.divider()
    st.subheader("What the sample data tells us")
    st.caption("Rules produce these observations directly from the numbers. Drivers still need investigation.")
    for entry in story_cards(row)[:3]:
        st.markdown(
            '<div class="comic-panel ' + entry["accent"] + '">'
            '<div class="eyebrow">' + entry["eyebrow"] + '</div>'
            '<h3>' + entry["headline"] + '</h3><p>' + entry["body"] + '</p></div>',
            unsafe_allow_html=True
        )


with tabs[1]:
    render_kpi_workbench(df, bank, quarter)

with tabs[2]:
    render_financial_controls()


def display_scorecard(frame):
    """Render an accessible four-perspective BA scorecard using illustrative thresholds."""
    for entry in frame.to_dict("records"):
        status = str(entry["Status"])
        badge = {"On target": "good", "Watch": "watch", "Off target": "bad"}.get(status, "missing")
        measure = "No baseline" if pd.isna(entry["Value"]) else f'{entry["Value"]:.1f}{entry["Unit"]}'
        sign = "≤" if entry["Direction"] == "lower" else "≥"
        st.markdown(
            '<div class="score-panel">'
            f'<div class="eyebrow">{entry["Perspective"]}</div>'
            '<div class="score-head">'
            f'<span class="score-title">{entry["Metric"]}</span>'
            f'<span class="score-value">{measure}</span>'
            f'<span class="score-badge {badge}">{status}</span>'
            '</div>'
            f'<div class="score-note">Sample target {sign} {entry["Target"]:.1f}{entry["Unit"]} · '
            f'{entry["Why it matters"]}</div></div>',
            unsafe_allow_html=True,
        )

with tabs[3]:
    st.header("Balanced scorecards")
    a, b = st.columns(2)
    with a:
        st.subheader("💵 Money scorecard")
        display_scorecard(make_scorecard(row, targets["financial"]))
    with b:
        st.subheader("♻️ Devices scorecard")
        display_scorecard(make_scorecard(row, targets["devices"]))
    st.caption("All targets and amber bands are hypothetical and editable in config/targets.json.")
    with st.expander("See the detailed scorecard metrics"):
        st.dataframe(pd.concat([make_scorecard(row, targets["financial"]), make_scorecard(row, targets["devices"])], ignore_index=True).round(2), hide_index=True, width="stretch")

with tabs[4]:
    st.header("Lean & Green performance quadrant")
    st.caption("When the numbers collide, decisions begin.")
    fig = px.scatter(current, x="efficiency_ratio", y="recycling_rate", size="revenue", color="bank", text="bank", color_discrete_map=BANK_COLOURS, size_max=45)
    fig.update_traces(textposition="top center")
    fig.add_vline(x=55, line_dash="dash", line_color=PINK)
    fig.add_hline(y=85, line_dash="dash", line_color=CYAN)
    fig.update_layout(xaxis_title="Efficiency (%) · lower is better", yaxis_title="Recycling (%) · higher is better")
    st.plotly_chart(fig, width="stretch")
    st.caption("Targets are illustrative. Bubble size indicates fictional revenue. Comparison does not establish causation.")

    st.subheader("Evidence → investigation → owner")
    above_cost = float(row["efficiency_ratio"]) > 55
    below_recovery = float(row["recycling_rate"]) < 85
    decision_rows = [
        {
            "Observed signal": f"Expense/revenue = {row['efficiency_ratio']:.1f}% (illustrative limit 55%)",
            "Decision": "Investigate cost ratio" if above_cost else "Maintain monitoring",
            "Proposed owner": "Finance + Operations",
            "Evidence needed": "Expense categories, revenue mix, time period and approved definitions",
        },
        {
            "Observed signal": f"Recycling = {row['recycling_rate']:.1f}% (illustrative limit 85%)",
            "Decision": "Investigate recovery evidence" if below_recovery else "Validate recorded recovery",
            "Proposed owner": "IT asset lead + Sustainability",
            "Evidence needed": "Asset register, recycler receipts, disposition categories",
        },
    ]
    st.dataframe(pd.DataFrame(decision_rows), hide_index=True, width="stretch")
    st.caption(
        "Suggested owners are hypothetical. These records justify asking questions, "
        "not asserting operational root causes."
    )
    with st.expander("External drivers this model does NOT measure"):
        st.markdown(
            "Inflation, business or lending mix, interest rates, institutional scale, seasonal effects, "
            "device replacement policy, recycling vendor contracts and differences in disclosure methods "
            "could change how comparable the figures are. The synthetic dataset does not contain "
            "these explanatory variables. A real BA would document them and check with business owners."
        )

    st.dataframe(current.round(2), width="stretch", hide_index=True)
    st.download_button("Download sample quarter CSV", current.to_csv(index=False), file_name="sample_quarter.csv", mime="text/csv")

    st.divider()
    st.header("Scenario sensitivity")
    st.caption("Know the score before you make the move.")
    a, b = st.columns(2)
    reduction = a.slider("Expense reduction (%)", 0.0, 20.0, 5.0, 0.5)
    recycling = b.slider("Recycling uplift (percentage points)", 0.0, 20.0, 5.0, 0.5)
    s = scenario(row, reduction, recycling)
    a, b, c, d = st.columns(4)
    a.metric("New efficiency", f"{s['efficiency_ratio']:.1f}%")
    b.metric("New recycling", f"{s['recycling_rate']:.1f}%")
    c.metric("Modelled expense saving", f"CAD {s['expense_savings']:,.1f}M")
    d.metric("Additional recycled", f"{s['additional_recycled_kg']:,.0f} kg")
    st.warning("Sensitivity only, not a forecast. Revenue and retired mass are fixed. Savings do not automatically change net income.")

with tabs[5]:
    st.header("Stakeholder lens")
    people = {
        "Finance director": ("How can we improve expense conversion?", "efficiency_ratio", "Financial KPI review"),
        "Operations manager": ("What is driving device retirements?", "retired_kg", "Operations workshop"),
        "Sustainability lead": ("Is the recovery rate improving?", "recycling_rate", "Vendor evidence review"),
        "IT asset manager": ("Which device types need attention?", "laptops_kg", "IT asset inventory"),
        "Executive sponsor": ("Where should leadership invest attention?", "net_margin", "Executive briefing")
    }
    role = st.selectbox("Select stakeholder", list(people))
    question, metric, meeting = people[role]
    st.write("**Business question:** " + question)
    st.write("**Engagement approach:** " + meeting)
    st.metric(metric.replace("_", " ").title(), f"{row[metric]:,.1f}")
    power = pd.DataFrame({"Stakeholder":list(people), "Power":[5,4,4,3,5], "Interest":[5,4,5,4,4]})
    graphic = px.scatter(power, x="Interest", y="Power", text="Stakeholder", color_discrete_sequence=[PINK])
    graphic.update_traces(marker_size=17, textposition="top center")
    graphic.update_xaxes(range=[0,6])
    graphic.update_yaxes(range=[0,6])
    st.plotly_chart(graphic, width="stretch")
    st.caption("Stakeholder positions are fictional examples.")

st.divider()
st.caption("DOLLARS & DEVICES | Junior BA case study: operations reporting and controls | Synthetic data, no real-bank findings.")
with st.expander("A small retro easter egg"):
    st.caption("You forget a thousand things every day. Make sure this is not one of em.")
