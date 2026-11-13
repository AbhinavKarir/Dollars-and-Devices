"""Transparent calculations and financial controls for a BA case study.

A PASS proves arithmetic consistency of fictional inputs, not external validity.
"""
from __future__ import annotations

import pandas as pd
import plotly.express as px
import streamlit as st

from theme import BLUE, SLATE
from finance_controls import budget_variance, continuity_check, load_case, reconcile
from metric_audit import RECIPES, trace_metric, validate_dataset


def fmt(value, unit):
    return "Not available" if pd.isna(value) else f"{value:,.3f} {unit}"


def render_kpi_workbench(data, bank, quarter):
    st.subheader("Calculation workbench")
    st.write("Re-perform each formula from source columns. The separate SQLite test provides an independent implementation cross-check.")
    bank_rows = data.loc[data.bank == bank].sort_values("quarter")
    selected = bank_rows.loc[bank_rows.quarter == quarter].iloc[0]
    previous_rows = bank_rows.loc[bank_rows.quarter < quarter]
    previous = previous_rows.iloc[-1] if not previous_rows.empty else None
    label_to_metric = {v["title"]: k for k, v in RECIPES.items()}
    chosen = st.selectbox("Choose the measure to verify", list(label_to_metric))
    trace = trace_metric(selected, label_to_metric[chosen], previous)

    a, b, c = st.columns(3)
    a.metric("Displayed result", fmt(trace["dashboard_value"], trace["unit"]))
    b.metric("Re-performed result", fmt(trace["recomputed"], trace["unit"]))
    c.metric("Arithmetic check", trace["status"])
    st.code(trace["formula"], language="text")
    st.write("Data source:", trace["source"])
    inputs = pd.DataFrame([{"Field": k, "Original value": v} for k, v in trace["inputs"].items()])
    st.dataframe(inputs, hide_index=True, width="stretch")
    st.write("Business meaning:", trace["meaning"])
    st.write("Analyst follow-up:", trace["decision"])
    if trace["status"] == "FAIL":
        st.error("Formula mismatch. Do not use this result without correcting its source.")
    elif trace["status"] in {"N/A", "UNAVAILABLE"}:
        st.info("Comparison unavailable: " + trace["reason"] + ". No zero or growth value has been substituted.")
    else:
        st.success("Re-performed calculation matches the stored metric.")

    st.divider()
    st.subheader("Internal validation register")
    st.caption("13 control definitions applied to 12 synthetic rows. Loader integrity gates run first; these arithmetic checks do not demonstrate operational defect detection. See Asset Controls for defective source evidence.")
    checks = validate_dataset(data)
    totals = checks.Result.value_counts()
    x, y, z, w, u = st.columns(5)
    x.metric("Control definitions", checks.Check.nunique())
    y.metric("Passed", int(totals.get("PASS", 0)))
    z.metric("Failed", int(totals.get("FAIL", 0)))
    w.metric("N/A", int(totals.get("N/A", 0)))
    u.metric("Unavailable", int(totals.get("UNAVAILABLE", 0)))
    st.caption("N/A means no earlier quarter. Unavailable means a period gap or zero growth baseline; inspect the reason in the register.")
    exceptions_only = st.toggle("Show only failures and unavailable comparisons")
    subset = checks.loc[checks.Result != "PASS"] if exceptions_only else checks
    st.dataframe(subset, hide_index=True, width="stretch")
    st.download_button("Export check register", checks.to_csv(index=False),
                       file_name="validation_register.csv", mime="text/csv")


def render_financial_controls():
    st.subheader("Financial controls lab")
    st.write(
        "Can we reconcile a simple cash ledger and explain budget exceptions? "
        "This is a smaller, separate synthetic personal-finance scenario, "
        "not a record of the author's actual spending."
    )
    try:
        ledger, statements, budgets = load_case()
    except (KeyError, ValueError, FileNotFoundError) as error:
        st.error("Could not validate source files: " + str(error))
        return
    months = sorted(statements.month.unique())
    month = st.selectbox("Cash-flow month", months, index=len(months)-1)
    result = reconcile(ledger, statements, month)
    variances = budget_variance(ledger, budgets, month)
    a, b, c, d = st.columns(4)
    a.metric("Deposits", f"CAD {result['income']:,.0f}")
    b.metric("Withdrawals", f"CAD {result['expenses']:,.0f}")
    c.metric("Net cash flow", f"CAD {result['net_cash_flow']:,.0f}")
    d.metric("Closing balance", f"CAD {result['closing_calculated']:,.0f}")
    st.markdown("#### Statement reconciliation")
    st.code(
        f"Opening balance         CAD {result['opening']:,.2f}\n"
        f"+ Deposits              CAD {result['income']:,.2f}\n"
        f"- Withdrawals           CAD {result['expenses']:,.2f}\n"
        f"= Calculated closing    CAD {result['closing_calculated']:,.2f}\n"
        f"Statement closing       CAD {result['closing_statement']:,.2f}\n"
        f"Difference              CAD {result['difference']:,.2f}",
        language="text"
    )
    if result["reconciled"]:
        st.success("PASS: ledger reconciles to the fictional statement.")
    else:
        st.error("FAIL: statement and ledger do not reconcile.")

    st.markdown("#### Demonstrate exception detection")
    st.caption("This creates a temporary mismatch for demonstration; original data remains unchanged.")
    if st.toggle("Inject an artificial CAD 25 error", value=False):
        altered = reconcile(ledger, statements, month, simulated_statement_error=25.0)
        st.error(
            f"EXPECTED CONTROL FAILURE: statement {altered['closing_statement']:,.2f} "
            f"versus calculated {altered['closing_calculated']:,.2f}. "
            f"Variance CAD {altered['difference']:,.2f}."
        )
        st.write("Investigate missing transactions, duplicate postings, cut-off dates and coding errors.")

    st.markdown("#### Budget versus actual")
    display = variances.melt(id_vars="category", value_vars=["monthly_budget", "amount"],
                             var_name="measure", value_name="CAD")
    display["measure"] = display["measure"].map({"monthly_budget":"Budget", "amount":"Actual"})
    chart = px.bar(display, x="category", y="CAD", color="measure", barmode="group",
                   color_discrete_map={"Budget":SLATE, "Actual":BLUE})
    chart.update_layout(xaxis_title="", legend_title="")
    st.plotly_chart(chart, width="stretch")
    overs = variances.loc[variances.variance > 0]
    x, y, z = st.columns(3)
    x.metric("Categories over budget", len(overs))
    y.metric("Total category overspend", f"CAD {overs.variance.sum():,.2f}")
    z.metric("Opening/closing continuity", "PASS" if continuity_check(statements) else "FAIL")
    if not overs.empty:
        top = overs.iloc[0]
        st.write(
            f"Investigation candidate: {top['category']} is CAD {top['variance']:.2f} over budget. "
            "Determine whether the cause is recurring spending or an unrealistic budget."
        )
    st.dataframe(variances.round(2), hide_index=True, width="stretch")
    with st.expander("Inspect underlying fictional transactions"):
        records = ledger.loc[ledger.month == month].copy()
        records["date"] = records.date.dt.strftime("%Y-%m-%d")
        st.dataframe(records, hide_index=True, width="stretch")
        st.download_button("Download cash ledger", records.to_csv(index=False),
                           file_name="sample_cash_ledger.csv", mime="text/csv")
    st.caption("This is not double-entry accounting or assurance over a real bank statement.")

