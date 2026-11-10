"""Dollars & Devices | Business Analyst Portfolio | Start: streamlit run app.py."""
import streamlit as st
import pandas as pd
import plotly.express as px
from analytics import load_metrics, load_targets, make_scorecard, portfolio_summary, scenario, story_cards
from theme import BANK_COLOURS, BLUE, TEAL, SLATE, apply_theme
from evidence_views import render_kpi_workbench, render_financial_controls

st.set_page_config(page_title="Dollars & Devices | Operations Reporting", page_icon="D", layout="wide")
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
    st.title("Dollars & Devices")
    st.caption("Reporting scope")
    bank = st.selectbox("Institution", sorted(df.bank.unique()))
    quarters = sorted(df.quarter.unique())
    quarter = st.selectbox("Quarter", quarters, index=len(quarters) - 1)
    st.info("Synthetic case study. Institution names are comparison labels only; figures are fictional and there is no bank affiliation.")

row = df[(df.bank == bank) & (df.quarter == quarter)].iloc[0]
history = df[df.bank == bank].sort_values("quarter")
earlier = history[history.quarter < quarter]
prev = earlier.iloc[-1] if not earlier.empty else None
current = df[df.quarter == quarter]

st.markdown('<div class="report-header"><div class="eyebrow">BUSINESS ANALYST PORTFOLIO</div>'
            '<h1>Dollars &amp; Devices</h1><p>Operations, performance reporting &amp; controls</p>'
            '<span class="sample-label">SYNTHETIC DATA · DEMONSTRATION ONLY</span></div>', unsafe_allow_html=True)
with st.expander("Case brief and reporting scope", expanded=False):
    st.write("Business question: can operating costs and device recovery be measured reliably? "
             "This case study compares six fictional institutional profiles across two periods, "
             "traces KPIs to source records, and links exceptions to proposed investigations. "
             "Cash Controls uses a separate fictional household ledger. "
             "This is not actual bank reporting or financial advice.")

st.caption(f"FOCUS: {bank} | {quarter} | Currency: CAD millions | Devices: kilograms")
tabs = st.tabs(["Overview", "KPI Proof", "Cash Controls", "Scorecards", "Compare & Decide", "Stakeholders"])

with tabs[0]:
    st.header("Executive summary")
    cost_signal = "above" if row.efficiency_ratio > 55 else "within"
    recovery_signal = "below" if row.recycling_rate < 85 else "at or above"
    st.write(f"{bank} reports an expense-to-revenue ratio of {row.efficiency_ratio:.1f}% "
             f"({cost_signal} the illustrative 55% limit) and a recycling rate of "
             f"{row.recycling_rate:.1f}% ({recovery_signal} the illustrative 85% target). "
             "Next: verify source calculations in KPI Proof, then review expense categories "
             "and recycler receipts with the proposed owners in Compare & Decide.")
    cols = st.columns(4)
    items = [("Efficiency ratio ↓", "efficiency_ratio", True), ("Net income margin ↑", "net_margin", False), ("Recycling rate ↑", "recycling_rate", False)]
    for i, (label, metric, inverse) in enumerate(items):
        delta = None if prev is None else f"{row[metric] - prev[metric]:+.1f} pp"
        cols[i].metric(label, f"{row[metric]:.1f}%", delta, delta_color="inverse" if inverse else "normal")
    cols[3].metric("Retired devices", f"{row.retired_kg:,.0f} kg")
    st.caption("Ratio changes are percentage points versus the previous available quarter. Lower expense ratios and higher margins/recovery rates are favourable.")
    st.subheader("Revenue allocation")
    st.dataframe(pd.DataFrame({
        "Component": ["Tracked expenses", "Net income", "Other / unreconciled"],
        "Cents per CAD 1 of revenue": [row.efficiency_ratio, row.net_margin, row.residual_cents],
    }).round(2), hide_index=True, width="stretch")
    st.caption("Arithmetic illustration only. Other / unreconciled is the residual, not a verified accounting category; this is not an audited accounting bridge.")
    st.subheader("Combined six-institution sample portfolio")
    summary = portfolio_summary(df, quarter)
    x, y, z = st.columns(3)
    x.metric("Weighted efficiency", f"{summary['efficiency_ratio']:.1f}%")
    y.metric("Weighted margin", f"{summary['net_margin']:.1f}%")
    z.metric("Weighted recycling", f"{summary['recycling_rate']:.1f}%")

    st.divider()
    st.subheader("What the sample data tells us")
    st.caption("Rules produce these observations directly from the numbers. Drivers still need investigation.")
    for entry in story_cards(row):
        st.markdown(
            '<div class="insight-panel ' + ("sustainability" if entry["accent"] == "violet" else "reporting") + '">'
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
        st.subheader("Financial performance")
        display_scorecard(make_scorecard(row, targets["financial"]))
    with b:
        st.subheader("Device recovery & sustainability")
        display_scorecard(make_scorecard(row, targets["devices"]))
    st.caption("All targets and amber bands are hypothetical and editable in config/targets.json.")
    with st.expander("See the detailed scorecard metrics"):
        st.dataframe(pd.concat([make_scorecard(row, targets["financial"]), make_scorecard(row, targets["devices"])], ignore_index=True).round(2), hide_index=True, width="stretch")

with tabs[4]:
    st.header("Operating efficiency and device recovery")
    st.caption("Compare the selected quarter against illustrative limits. Lower expense ratios and higher recovery rates are favourable.")
    fig = px.scatter(current, x="efficiency_ratio", y="recycling_rate", size="revenue", color="bank", text="bank", color_discrete_map=BANK_COLOURS, size_max=45)
    fig.update_traces(textposition="top center")
    fig.add_vline(x=55, line_dash="dash", line_color=SLATE)
    fig.add_hline(y=85, line_dash="dash", line_color=TEAL)
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
    st.caption("Adjust assumptions to estimate the sensitivity of expenses and device recovery.")
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
    graphic = px.scatter(power, x="Interest", y="Power", text="Stakeholder", color_discrete_sequence=[BLUE])
    graphic.update_traces(marker_size=17, textposition="top center")
    graphic.update_xaxes(range=[0,6])
    graphic.update_yaxes(range=[0,6])
    st.plotly_chart(graphic, width="stretch")
    st.caption("Stakeholder positions are fictional examples.")

st.divider()
st.caption("DOLLARS & DEVICES | Junior BA case study: operations reporting and controls | Synthetic data, no real-bank findings.")
