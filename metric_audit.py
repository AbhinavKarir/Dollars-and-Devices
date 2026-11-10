"""Human-readable calculation trace and internal reconciliation checks.

IMPORTANT: these are repeatable arithmetic / sample-data integrity checks,
NOT external audits of the fictional institutions or their performance.
"""
from __future__ import annotations

from math import isclose
import pandas as pd

# Each recipe specifies transparent source values, formula, and unit.
RECIPES = {
    "efficiency_ratio": {
        "title": "Operating efficiency",
        "formula": "expenses / revenue * 100",
        "raw_columns": ["expenses", "revenue"],
        "source": "data/raw/bank_financials.csv",
        "unit": "%",
        "meaning": "How many cents of tracked expense correspond to one revenue dollar.",
        "decision": "If it rises, ask which cost category grew or whether revenue fell.",
    },
    "net_margin": {
        "title": "Net income margin",
        "formula": "net_income / revenue * 100",
        "raw_columns": ["net_income", "revenue"],
        "source": "data/raw/bank_financials.csv",
        "unit": "%",
        "meaning": "Net income per 100 revenue dollars.",
        "decision": "Check business mix and net income drivers; do not equate with gross margin.",
    },
    "retired_kg": {
        "title": "Total retired IT mass",
        "formula": "desktops_kg + laptops_kg + atm_terminals_kg",
        "raw_columns": ["desktops_kg", "laptops_kg", "atm_terminals_kg"],
        "source": "data/raw/bank_ewaste.csv",
        "unit": "kg",
        "meaning": "Three recorded retired-device categories added together.",
        "decision": "Ask whether device refresh cycles or asset inventory quality explain changes.",
    },
    "recycling_rate": {
        "title": "Tracked recycling rate",
        "formula": "recycled_kg / (desktops_kg + laptops_kg + atm_terminals_kg) * 100",
        "raw_columns": ["recycled_kg", "desktops_kg", "laptops_kg", "atm_terminals_kg"],
        "source": "data/raw/bank_ewaste.csv",
        "unit": "%",
        "meaning": "Share of recorded retired-device mass labelled as recycled.",
        "decision": "Confirm recycling evidence, vendor tracking, and disposition codes.",
    },
    "unrecycled_kg": {
        "title": "Not recorded as recycled",
        "formula": "retired_kg - recycled_kg",
        "raw_columns": ["desktops_kg", "laptops_kg", "atm_terminals_kg", "recycled_kg"],
        "source": "data/raw/bank_ewaste.csv",
        "unit": "kg",
        "meaning": "Mass not marked recycled, which may include other disposal pathways.",
        "decision": "Do not label all non-recycled mass as landfill without disposition data.",
    },
    "revenue_growth_pct": {
        "title": "Revenue growth quarter over quarter",
        "formula": "(revenue_current / revenue_previous - 1) * 100",
        "raw_columns": ["revenue"],
        "source": "data/raw/bank_financials.csv",
        "unit": "%",
        "meaning": "Relative movement from the previous quarter.",
        "decision": "Compare with expenses before judging operational efficiency.",
    },
    "expense_growth_pct": {
        "title": "Expense growth quarter over quarter",
        "formula": "(expenses_current / expenses_previous - 1) * 100",
        "raw_columns": ["expenses"],
        "source": "data/raw/bank_financials.csv",
        "unit": "%",
        "meaning": "Relative change in tracked operating expenses.",
        "decision": "Check whether expense growth exceeds revenue growth.",
    },
    "recycling_pp_change": {
        "title": "Recycling rate change",
        "formula": "recycling_rate_current - recycling_rate_previous",
        "raw_columns": ["recycled_kg", "desktops_kg", "laptops_kg", "atm_terminals_kg"],
        "source": "data/raw/bank_ewaste.csv",
        "unit": "percentage points",
        "meaning": "Difference of two recycling rates, not percent growth.",
        "decision": "Investigate whether any change comes from recovery or retirement-volume shifts.",
    },
}

def independent_value(row: pd.Series, metric: str, previous: pd.Series | None = None) -> float:
    """Recompute the metric with raw operands rather than copying the cached KPI value."""
    if metric == "efficiency_ratio":
        return 100 * float(row["expenses"]) / float(row["revenue"])
    if metric == "net_margin":
        return 100 * float(row["net_income"]) / float(row["revenue"])
    if metric == "retired_kg":
        return sum(float(row[key]) for key in ("desktops_kg", "laptops_kg", "atm_terminals_kg"))
    if metric == "recycling_rate":
        mass = independent_value(row, "retired_kg")
        return 100 * float(row["recycled_kg"]) / mass
    if metric == "unrecycled_kg":
        return independent_value(row, "retired_kg") - float(row["recycled_kg"])
    if metric in {"revenue_growth_pct", "expense_growth_pct"}:
        if previous is None:
            return float("nan")
        key = "revenue" if metric == "revenue_growth_pct" else "expenses"
        return 100 * (float(row[key]) / float(previous[key]) - 1)
    if metric == "recycling_pp_change":
        if previous is None:
            return float("nan")
        return independent_value(row, "recycling_rate") - independent_value(previous, "recycling_rate")
    raise KeyError(f"Unknown audit metric: {metric}")


def trace_metric(row: pd.Series, metric: str, previous: pd.Series | None = None) -> dict:
    """Explain a selected KPI from its sources and cross-check stored value."""
    recipe = RECIPES[metric]
    calculated = independent_value(row, metric, previous)
    cached = row[metric]
    both_missing = pd.isna(cached) and pd.isna(calculated)
    passed = bool(both_missing or (pd.notna(calculated) and pd.notna(cached) and
                                   isclose(float(calculated), float(cached), rel_tol=1e-9, abs_tol=1e-9)))
    inputs = {key: float(row[key]) for key in recipe["raw_columns"]}
    if previous is not None and (metric.endswith("_growth_pct") or metric.endswith("_pp_change")):
        inputs.update({"previous_" + key: float(previous[key]) for key in recipe["raw_columns"]})
    return {
        **recipe,
        "metric": metric,
        "inputs": inputs,
        "recomputed": calculated,
        "dashboard_value": cached,
        "status": "PASS" if passed else "FAIL",
        "baseline": "Available" if previous is not None else "Not available",
    }


def validate_dataset(frame: pd.DataFrame) -> pd.DataFrame:
    """Repeat selected invariants and metric checks for every institution-quarter."""
    results = []
    for bank, part in frame.groupby("bank"):
        part = part.sort_values("quarter")
        previous = None
        for _, row in part.iterrows():
            for metric in RECIPES:
                trace = trace_metric(row, metric, previous)
                results.append({
                    "Bank": bank, "Quarter": row["quarter"],
                    "Check": f"{trace['title']} formula",
                    "Result": trace["status"],
                    "Detail": "Arithmetic reconciliation" if trace["status"] == "PASS" else "Calculated result differs",
                })
            checks = {
                "Non-negative retired asset mass": row["retired_kg"] >= 0,
                "Recycled mass within total retired": 0 <= row["recycled_kg"] <= row["retired_kg"],
                "Recycling rate 0–100%": 0 <= row["recycling_rate"] <= 100,
                "Revenue denominator positive": row["revenue"] > 0,
                "Unique row per quarter": (part["quarter"] == row["quarter"]).sum() == 1,
            }
            for label, ok in checks.items():
                results.append({
                    "Bank": bank, "Quarter": row["quarter"], "Check": label,
                    "Result": "PASS" if ok else "FAIL", "Detail": "Sample-data integrity",
                })
            previous = row
    return pd.DataFrame(results)
