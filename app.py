"""Dollars & Devices Neon Edition | Start: streamlit run app.py."""
import streamlit as st
import pandas as pd
import plotly.express as px
from analytics import load_metrics, load_targets, make_scorecard, portfolio_summary, scenario, story_cards
from theme import BANK_COLOURS, PINK, CYAN, VIOLET, apply_theme

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

st.markdown('<div class="neon-hero"><span class="eyebrow">BUSINESS INTELLIGENCE LAB / ISSUE 01</span><div class="hero-title">DOLLARS <span>&</span><br>DEVICES</div><div class="hero-sub">The cost of doing business. The cost of retiring tech. A neon executive analytics case study for better decisions.</div><div class="hero-stamp">SAMPLE DATA · DEMONSTRATION ONLY</div></div>', unsafe_allow_html=True)
st.caption(f"FOCUS: {bank} | {quarter} | Currency: CAD millions | Devices: kilograms")
tabs = st.tabs(["📡 Executive pulse", "📰 Story Mode", "🎛️ Scorecards", "📈 Benchmark", "🧪 Scenarios", "👥 Stakeholders", "📚 Analyst guide"])

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

with tabs[1]:
    st.header("The Neon Newsroom")
    st.caption("Rule-based sample-data headlines. No invented drivers or AI guesses.")
    for item in story_cards(row):
        st.markdown('<div class="comic-panel ' + item["accent"] + '"><div class="eyebrow">' + item["eyebrow"] + '</div><h3>' + item["headline"] + '</h3><p>' + item["body"] + '</p></div>', unsafe_allow_html=True)
    trend = history.melt(id_vars="quarter", value_vars=["efficiency_ratio", "net_margin", "recycling_rate"], var_name="metric", value_name="rate")
    st.plotly_chart(px.line(trend, x="quarter", y="rate", color="metric", markers=True, color_discrete_sequence=[PINK, CYAN, VIOLET]), use_container_width=True)

with tabs[2]:
    st.header("Balanced scorecards")
    a, b = st.columns(2)
    with a:
        st.subheader("💵 Money scorecard")
        st.dataframe(make_scorecard(row, targets["financial"])[["Perspective","Metric","Value","Target","Status","Why it matters"]].round(2), hide_index=True, use_container_width=True)
    with b:
        st.subheader("♻️ Devices scorecard")
        st.dataframe(make_scorecard(row, targets["devices"])[["Perspective","Metric","Value","Target","Status","Why it matters"]].round(2), hide_index=True, use_container_width=True)
    st.caption("All targets and amber bands are hypothetical and editable in config/targets.json.")

with tabs[3]:
    st.header("Lean & Green performance quadrant")
    fig = px.scatter(current, x="efficiency_ratio", y="recycling_rate", size="revenue", color="bank", text="bank", color_discrete_map=BANK_COLOURS, size_max=45)
    fig.update_traces(textposition="top center")
    fig.add_vline(x=55, line_dash="dash", line_color=PINK)
    fig.add_hline(y=85, line_dash="dash", line_color=CYAN)
    fig.update_layout(xaxis_title="Efficiency (%) · lower is better", yaxis_title="Recycling (%) · higher is better")
    st.plotly_chart(fig, use_container_width=True)
    st.caption("Targets are illustrative. Bubble size indicates fictional revenue. Comparison does not establish causation.")
    st.dataframe(current.round(2), use_container_width=True, hide_index=True)
    st.download_button("Download sample quarter CSV", current.to_csv(index=False), file_name="sample_quarter.csv", mime="text/csv")

with tabs[4]:
    st.header("What-if scenario lab")
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
    st.plotly_chart(graphic, use_container_width=True)
    st.caption("Stakeholder positions are fictional examples.")

with tabs[6]:
    st.header("BA interview guide")
    st.write("**Problem:** Bring financial efficiency and responsible IT asset retirement into one decision-ready view.")
    st.write("**Process:** discovery → validation → KPIs → benchmarking → stakeholder review → recommendation.")
    st.markdown("**Formulas:** Efficiency = expenses / revenue × 100. Margin = net income / revenue × 100. Recycling = recycled kg / retired kg × 100.")
    st.write("**Rate changes:** 85% to 88% is +3 percentage points, NOT 3% growth.")
    st.write("**Aggregation:** Divide portfolio totals rather than averaging standalone percentages.")
    st.write("**Limits:** Fictional numbers, two quarters, and hypothetical targets. No causal or investment conclusions.")
    st.write("**Reuse:** Replace banks with locations, departments, suppliers, or products and validate KPIs with domain experts.")
    st.code("streamlit run app.py", language="bash")

st.divider()
st.caption("DOLLARS & DEVICES · NEON EDITION | Original BA portfolio case study | Fictional data only")
