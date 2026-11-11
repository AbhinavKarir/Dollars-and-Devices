"""Dollars & Devices | Business Analyst Portfolio | Start: streamlit run app.py."""
import streamlit as st
import pandas as pd
import plotly.express as px
from analytics import load_metrics, load_targets, make_scorecard, portfolio_summary, scenario
from theme import BANK_COLOURS, TEAL, SLATE, apply_theme
from evidence_views import render_kpi_workbench, render_financial_controls

st.set_page_config(page_title="Dollars & Devices | Operations Reporting", page_icon="D", layout="wide")
apply_theme()

@st.cache_data
def load_data():
    return load_metrics()

with st.sidebar:
    st.title("Dollars & Devices")
    case = st.radio("Case study", ["Operations & Device Reporting", "Cash Reconciliation Lab"])
    if case == "Cash Reconciliation Lab":
        st.caption("Separate fictional household dataset. Institution and quarter filters do not apply.")
if case == "Cash Reconciliation Lab":
    st.title("Cash Reconciliation Lab")
    render_financial_controls()
    st.stop()
try:
    df = load_data()
    targets = load_targets()
except (ValueError, KeyError, FileNotFoundError) as error:
    st.error(str(error))
    st.stop()
with st.sidebar:
    st.caption("Operations reporting scope")
    bank = st.selectbox("Institution", sorted(df.bank.unique()))
    quarters = sorted(df.loc[df.bank == bank, "quarter"].unique())
    quarter = st.selectbox("Quarter", quarters, index=len(quarters) - 1)
    st.info("Synthetic case study. Institution names are comparison labels only; figures are fictional and there is no bank affiliation.")

row = df[(df.bank == bank) & (df.quarter == quarter)].iloc[0]
history = df[df.bank == bank].sort_values("quarter")
earlier = history[history.quarter < quarter]
prev = earlier.iloc[-1] if not earlier.empty else None
current = df[df.quarter == quarter]

st.markdown('<div class="report-header"><div class="eyebrow">BUSINESS ANALYST PORTFOLIO</div>'
            '<h1>Dollars &amp; Devices</h1><p>Operations &amp; Device Reporting</p>'
            '<span class="sample-label">SYNTHETIC DATA · DEMONSTRATION ONLY</span></div>', unsafe_allow_html=True)
with st.expander("Case brief and reporting scope", expanded=False):
    st.write("Business question: can operating costs and device recovery be measured reliably? "
             "This case study compares six fictional institutional profiles across two periods, "
             "traces KPIs to source records, and links exceptions to proposed investigations. "
             "The Cash Reconciliation Lab uses a separate fictional household ledger. "
             "This is not actual bank reporting or financial advice.")

st.caption(f"FOCUS: {bank} | {quarter} | Currency: CAD millions | Devices: kilograms")
tabs = st.tabs(["Overview", "KPI Proof", "Scorecards", "Compare & Decide", "Stakeholders"])

entries = targets["financial"] + targets["devices"]
rules = {entry["metric"]: entry for entry in entries}
scores = make_scorecard(row, entries)
cost_target = rules["efficiency_ratio"]["target"]
recovery_target = rules["recycling_rate"]["target"]

def exception_summary(frame):
    ranked = frame.copy()
    ranked["priority"] = ranked.Status.map({"Off target": 0, "Watch": 1, "No baseline": 2, "On target": 4}).fillna(2)
    return ranked.sort_values("priority", kind="stable").iloc[0]

with tabs[0]:
    st.header("Where to focus next")
    lead = exception_summary(scores)
    off = int((scores.Status == "Off target").sum())
    watch = int((scores.Status == "Watch").sum())
    st.caption(f"{bank} | {quarter} | {off} off target, {watch} on watch | Illustrative thresholds")
    if lead["Status"] in {"Off target", "Watch"}:
        distance_unit = "percentage points" if lead["Unit"] == "%" else lead["Unit"]
        st.subheader(f"{lead['Metric']}: {lead['Status']}")
        st.write(f"{lead['Value']:.1f}{lead['Unit']}, {abs(lead['Distance from target']):.1f} {distance_unit} "
                 f"from the {lead['Target']:.1f}{lead['Unit']} target. {lead['Why it matters']}.")
        st.write("**Next step:** Review the exceptions below, verify the inputs in KPI Proof, and use Compare & Decide to plan the investigation.")
    elif lead["Status"] != "On target":
        st.info("Some comparisons are unavailable. Review their reasons before drawing conclusions about growth.")
    else:
        st.success("All available scorecard measures are on target. Continue monitoring and verify source evidence.")

    cols = st.columns(4)
    for i, (label, metric, change) in enumerate([
        ("Efficiency", "efficiency_ratio", "efficiency_pp_change"),
        ("Net margin", "net_margin", "margin_pp_change"),
        ("Recycling", "recycling_rate", "recycling_pp_change"),
    ]):
        reason = row[change + "_reason"]
        delta = None if reason else f"{row[change]:+.1f} pp"
        cols[i].metric(label, f"{row[metric]:.1f}%", delta,
                       delta_color="inverse" if metric == "efficiency_ratio" else "normal",
                       help=(reason or "Change from the immediately preceding quarter") + ". pp = percentage points.")
    cols[3].metric("Retired mass", f"{row.retired_kg:,.0f} kg")
    st.caption("Changes compare consecutive quarters only. Missing comparisons are not zero. Hover over a metric for its comparison context.")
    exceptions = scores.loc[scores.Status != "On target", ["Metric", "Value", "Unit", "Target", "Watch limit", "Status"]]
    if not exceptions.empty:
        st.subheader("Exceptions and unavailable comparisons")
        st.dataframe(exceptions.round(2), hide_index=True, width="stretch")
    with st.expander("Combined sample portfolio and calculation illustration"):
        st.caption("Weighted ratios across all six fictional profiles; not a peer benchmark for real institutions.")
        summary = portfolio_summary(df, quarter)
        x, y, z = st.columns(3)
        x.metric("Weighted efficiency", f"{summary['efficiency_ratio']:.1f}%")
        y.metric("Weighted margin", f"{summary['net_margin']:.1f}%")
        z.metric("Weighted recycling", f"{summary['recycling_rate']:.1f}%")
        st.dataframe(pd.DataFrame({
            "Component": ["Tracked expenses", "Net income", "Unexplained arithmetic residual"],
            "Cents per CAD 1 of revenue": [row.efficiency_ratio, row.net_margin, row.residual_cents],
        }).round(2), hide_index=True, width="stretch")
        st.caption("The residual is an arithmetic illustration, not a verified accounting category or an audited bridge.")

with tabs[1]:
    render_kpi_workbench(df, bank, quarter)


def display_scorecard(frame):
    """Render an accessible four-perspective BA scorecard using illustrative thresholds."""
    for entry in frame.to_dict("records"):
        status = str(entry["Status"])
        badge = {"On target": "good", "Watch": "watch", "Off target": "bad"}.get(status, "missing")
        measure = "Unavailable" if pd.isna(entry["Value"]) else f'{entry["Value"]:.1f}{entry["Unit"]}'
        sign = "≤" if entry["Direction"] == "lower" else "≥"
        gap_unit = "pp" if entry["Unit"] == "%" else entry["Unit"]
        gap = "Comparison unavailable" if pd.isna(entry["Value"]) else f"Distance from target: {entry['Distance from target']:+.1f} {gap_unit} (actual minus target)"
        watch_rule = f"{entry['Target']:g} < value ≤ {entry['Watch limit']:g}" if entry["Direction"] == "lower" else f"{entry['Watch limit']:g} ≤ value < {entry['Target']:g}"
        st.markdown(
            '<div class="score-panel">' 
            f'<div class="eyebrow">{entry["Perspective"]}</div>'
            '<div class="score-head">'
            f'<span class="score-title">{entry["Metric"]}</span>'
            f'<span class="score-value">{measure}</span>'
            f'<span class="score-badge {badge}">{status}</span>'
            '</div>'
            f'<div class="score-note">Sample target {sign} {entry["Target"]:.1f}{entry["Unit"]} · '
            f'Watch: {watch_rule} {entry["Unit"]}<br/>{gap}<br/>{entry["Why it matters"]}</div></div>',
            unsafe_allow_html=True,
        )

with tabs[2]:
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

with tabs[3]:
    st.header("Operating efficiency and device recovery")
    st.caption("Compare the selected quarter against illustrative limits. Lower expense ratios and higher recovery rates are favourable.")
    fig = px.scatter(current, x="efficiency_ratio", y="recycling_rate", size="revenue", color="bank", text="bank", color_discrete_map=BANK_COLOURS, size_max=45)
    fig.update_traces(textposition="top center")
    fig.add_vline(x=cost_target, line_dash="dash", line_color=SLATE)
    fig.add_hline(y=recovery_target, line_dash="dash", line_color=TEAL)
    fig.update_layout(xaxis_title="Efficiency (%) · lower is better", yaxis_title="Recycling (%) · higher is better")
    st.plotly_chart(fig, width="stretch")
    st.caption("Targets are illustrative. Bubble size indicates fictional revenue. Comparison does not establish causation.")

    st.subheader("Evidence → investigation → owner")
    above_cost = float(row["efficiency_ratio"]) > cost_target
    below_recovery = float(row["recycling_rate"]) < recovery_target
    decision_rows = [
        {
            "Observed signal": f"Expense/revenue = {row['efficiency_ratio']:.1f}% (illustrative limit {cost_target:g}%)",
            "Decision": "Investigate cost ratio" if above_cost else "Maintain monitoring",
            "Proposed owner": "Finance + Operations",
            "Evidence needed": "Expense categories, revenue mix, time period and approved definitions",
        },
        {
            "Observed signal": f"Recycling = {row['recycling_rate']:.1f}% (illustrative limit {recovery_target:g}%)",
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

    with st.expander("Full selected-quarter data"):
        st.dataframe(current.round(2), width="stretch", hide_index=True)
    st.download_button("Download sample quarter CSV", current.to_csv(index=False), file_name="sample_quarter.csv", mime="text/csv")

    st.subheader("Worked investigation: a recovery exception")
    st.caption("Illustrative training walkthrough using CIBC 2026-Q1. The hypotheses, proposed workflow and conditional outcome are hypothetical.")
    example = df.loc[(df.bank == "CIBC") & (df.quarter == "2026-Q1")]
    if not example.empty:
        case_row = example.iloc[0]
        observed = float(case_row.recycling_rate)
        status = make_scorecard(case_row, [rules["recycling_rate"]]).iloc[0]["Status"]
        st.write(f"**Observed evidence:** {case_row.recycled_kg:,.0f} kg recorded recycled / {case_row.retired_kg:,.0f} kg retired "
                 f"= {observed:.2f}%. Configured target: {recovery_target:g}%; status: {status}. "
                 f"Distance from target: {observed - recovery_target:+.2f} percentage points. The investigation is needed only when the configured target is missed.")
        st.write("**Question:** Is the apparent shortfall caused by missing evidence, reporting cut-off, classification, or genuine recovery performance?")
        st.write("**Proposed owner:** IT asset manager, supported by the sustainability lead. Request the asset register, recycler receipts, collection dates and disposition codes.")
        st.write("**Competing explanations:** A receipt arrived after the reporting cut-off; a reused device was classified separately; or material was genuinely not recovered. None is established by this dataset.")
        st.write("**Investigation steps:** Match device batches to receipts, check dates and duplicates, classify unmatched mass, then recalculate under an agreed definition. Record the evidence and unresolved exceptions.")
        st.write("**Acceptance criteria:** Every reported mass total traces to a source; duplicate batches are excluded; timing and classification rules are documented; the agreed calculation reproduces the KPI; the proposed owner records a review decision.")
        st.write("**Hypothetical outcome:** If late receipts explain the shortfall, correct the cut-off process and rerun the KPI after evidence review. If the shortfall remains, propose a vendor review. No improvement or completed business outcome is claimed.")

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

with tabs[4]:
    st.header("Who needs what information?")
    st.caption("Proposed roles and engagement approaches for this fictional case study. No actual interviews or approvals are claimed.")
    stakeholder_rows = [
        {"Proposed owner": "Finance + Operations", "Decision": "Investigate an adverse efficiency ratio", "Evidence needed": "Expense categories, revenue mix, approved KPI definitions", "Communication": "Variance briefing, then a driver review", "Acceptance": "Reproduce the ratio and agree which driver to investigate"},
        {"Proposed owner": "IT asset manager", "Decision": "Validate recorded device retirements", "Evidence needed": "Asset IDs, retirement dates, device categories", "Communication": "Asset-register walkthrough and exception log", "Acceptance": "Retired totals trace to source records"},
        {"Proposed owner": "Sustainability lead", "Decision": "Validate recovery classification", "Evidence needed": "Recycler receipts and disposition categories", "Communication": "Evidence review with IT and the vendor", "Acceptance": "Recycled mass is supported and not double counted"},
        {"Proposed owner": "Executive sponsor", "Decision": "Prioritize a bounded investigation", "Evidence needed": "Validated signal, options, uncertainty and proposed owner", "Communication": "One-page decision brief", "Acceptance": "Agree scope, owner and review date; do not assert a root cause"},
    ]
    for person in stakeholder_rows:
        with st.expander(person["Proposed owner"], expanded=person == stakeholder_rows[0]):
            for field in ("Decision", "Evidence needed", "Communication", "Acceptance"):
                st.write(f"**{field}:** {person[field]}")
    st.download_button("Download stakeholder communication plan", pd.DataFrame(stakeholder_rows).to_csv(index=False),
                       file_name="sample_stakeholder_plan.csv", mime="text/csv")

st.divider()
st.caption("DOLLARS & DEVICES | Junior BA case study | Synthetic data, no real-bank findings.")
