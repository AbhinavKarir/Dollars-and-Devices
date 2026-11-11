"""Reusable business-analysis calculations for the Dollars & Devices dashboard.

Raw files are fictional demonstration data. These metrics are not investment advice.
All ratios use unrounded source data; presentation handles rounding.
"""
from __future__ import annotations

import json
import math
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parent
KEYS = ["bank", "quarter"]

FINANCIAL_COLUMNS = {"bank", "quarter", "revenue", "expenses", "net_income"}
WASTE_COLUMNS = {"bank", "quarter", "desktops_kg", "atm_terminals_kg", "laptops_kg", "recycled_kg"}


def _validate(frame: pd.DataFrame, required: set[str], label: str) -> None:
    missing = required.difference(frame.columns)
    if missing:
        raise ValueError(f"{label} is missing columns: {', '.join(sorted(missing))}")
    if frame.duplicated(KEYS).any():
        raise ValueError(f"{label} has duplicate bank-quarter records.")
    if frame.empty or frame.isna().any().any():
        raise ValueError(f"{label} contains empty or missing values.")


def load_metrics(data_directory: str | Path | None = None) -> pd.DataFrame:
    """Merge the two raw datasets, validate them, and calculate all KPIs."""
    folder = Path(data_directory) if data_directory else ROOT / "data" / "raw"
    money = pd.read_csv(folder / "bank_financials.csv")
    devices = pd.read_csv(folder / "bank_ewaste.csv")
    _validate(money, FINANCIAL_COLUMNS, "Financial dataset")
    _validate(devices, WASTE_COLUMNS, "Device dataset")

    money_cols = sorted(FINANCIAL_COLUMNS.difference(KEYS))
    device_cols = sorted(WASTE_COLUMNS.difference(KEYS))
    for column in money_cols:
        money[column] = pd.to_numeric(money[column], errors="raise")
    for column in device_cols:
        devices[column] = pd.to_numeric(devices[column], errors="raise")

    if (money["revenue"] <= 0).any():
        raise ValueError("Revenue must be positive to calculate ratios.")
    if (money[money_cols] < 0).any().any() or (devices[device_cols] < 0).any().any():
        raise ValueError("All sample amounts must be non-negative.")

    merged = money.merge(devices, on=KEYS, how="outer", validate="one_to_one", indicator=True)
    if not (merged["_merge"] == "both").all():
        raise ValueError("Every bank-quarter must have both finance and device records.")
    merged = merged.drop(columns="_merge").sort_values(KEYS).reset_index(drop=True)

    merged["retired_kg"] = merged[["desktops_kg", "atm_terminals_kg", "laptops_kg"]].sum(axis=1)
    if (merged["retired_kg"] <= 0).any():
        raise ValueError("Retired device weight must be positive.")
    if (merged["recycled_kg"] > merged["retired_kg"]).any():
        raise ValueError("Recycled weight cannot exceed retired device weight.")

    merged["efficiency_ratio"] = 100 * merged["expenses"] / merged["revenue"]
    merged["net_margin"] = 100 * merged["net_income"] / merged["revenue"]
    merged["recycling_rate"] = 100 * merged["recycled_kg"] / merged["retired_kg"]
    merged["unrecycled_kg"] = merged["retired_kg"] - merged["recycled_kg"]
    merged["residual_cents"] = 100 - merged["efficiency_ratio"] - merged["net_margin"]

    for source, output in (
        ("revenue", "revenue_growth_pct"),
        ("expenses", "expense_growth_pct"),
        ("retired_kg", "retired_growth_pct"),
        ("unrecycled_kg", "unrecycled_growth_pct"),
    ):
        previous = merged.groupby("bank")[source].shift()
        merged[output] = ((merged[source] / previous) - 1) * 100
    merged["recycling_pp_change"] = merged.groupby("bank")["recycling_rate"].diff()
    merged["efficiency_pp_change"] = merged.groupby("bank")["efficiency_ratio"].diff()
    merged["margin_pp_change"] = merged.groupby("bank")["net_margin"].diff()
    merged["cost_growth_gap_pp"] = merged["expense_growth_pct"] - merged["revenue_growth_pct"]

    return merged


def load_targets(path: str | Path | None = None) -> dict:
    """Keep scorecard targets separate from analytical calculations."""
    target_path = Path(path) if path else ROOT / "config" / "targets.json"
    with target_path.open(encoding="utf-8") as handle:
        config = json.load(handle)
    for group in ("financial", "devices"):
        for entry in config[group]:
            direction, target, limit = entry["direction"], entry["target"], entry["watch_limit"]
            if direction not in {"higher", "lower"} or not all(
                isinstance(value, (int, float)) and math.isfinite(value) for value in (target, limit)
            ):
                raise ValueError("Targets require a valid direction and finite boundaries.")
            if (direction == "lower" and limit < target) or (direction == "higher" and limit > target):
                raise ValueError("Watch limit must lie on the unfavourable side of the target.")
    return config


def target_status(value: float, target: float, direction: str, watch_band: float) -> str:
    """Use three consistent thresholds; missing prior-quarter data is not a failure."""
    if pd.isna(value):
        return "No baseline"
    if direction == "lower":
        return "On target" if value <= target else "Watch" if value <= target + watch_band else "Off target"
    if direction == "higher":
        return "On target" if value >= target else "Watch" if value >= target - watch_band else "Off target"
    raise ValueError("direction must be 'higher' or 'lower'")


def make_scorecard(row: pd.Series, entries: list[dict]) -> pd.DataFrame:
    """Evaluate one bank-quarter against editable, illustrative targets."""
    output = []
    for entry in entries:
        value = row[entry["metric"]]
        output.append({
            "Perspective": entry["perspective"],
            "Metric": entry["label"],
            "Value": float(value) if pd.notna(value) else float("nan"),
            "Target": float(entry["target"]),
            "Direction": entry["direction"],
            "Status": target_status(value, entry["target"], entry["direction"], abs(entry["watch_limit"] - entry["target"])),
            "Why it matters": entry["why"],
            "Unit": entry["unit"],
        })
    return pd.DataFrame(output)


def portfolio_summary(data: pd.DataFrame, quarter: str) -> dict:
    """Weight ratios by their real denominators; never average percentages blindly."""
    part = data.loc[data["quarter"] == quarter]
    if part.empty:
        raise ValueError(f"No data found for {quarter}.")
    return {
        "revenue": float(part["revenue"].sum()),
        "efficiency_ratio": 100 * part["expenses"].sum() / part["revenue"].sum(),
        "net_margin": 100 * part["net_income"].sum() / part["revenue"].sum(),
        "recycling_rate": 100 * part["recycled_kg"].sum() / part["retired_kg"].sum(),
        "retired_kg": float(part["retired_kg"].sum()),
    }


def scenario(row: pd.Series, expense_cut_pct: float, recycling_lift_pp: float) -> dict:
    """Illustrative, non-predictive sensitivity analysis with a fixed denominator."""
    adjusted_expenses = float(row["expenses"]) * (1 - expense_cut_pct / 100)
    revised_efficiency = 100 * adjusted_expenses / float(row["revenue"])
    revised_recycling = min(100.0, float(row["recycling_rate"]) + recycling_lift_pp)
    additional_recycled = max(0.0, revised_recycling - float(row["recycling_rate"])) * float(row["retired_kg"]) / 100
    return {
        "efficiency_ratio": revised_efficiency,
        "recycling_rate": revised_recycling,
        "expense_savings": float(row["expenses"]) - adjusted_expenses,
        "additional_recycled_kg": additional_recycled,
    }


def story_cards(row: pd.Series) -> list[dict]:
    """Rule-based language: every caption refers to actual sample metrics."""
    bank, quarter = str(row["bank"]), str(row["quarter"])
    cost = float(row["efficiency_ratio"])
    margin = float(row["net_margin"])
    recycling = float(row["recycling_rate"])

    def movement(value: float, lower_is_better: bool) -> str:
        if pd.isna(value):
            return "No earlier quarter is available for comparison."
        if abs(value) < 0.05:
            return "Essentially unchanged from the previous quarter."
        trend = "rose" if value > 0 else "fell"
        effect = "favourable" if (value < 0 if lower_is_better else value > 0) else "unfavourable"
        return f"{trend.capitalize()} {abs(value):.1f} percentage points since the previous quarter ({effect})."

    if cost <= 55:
        recommendation = "Cost conversion is within the illustrative target. Investigate which operating practices can be sustained."
    else:
        recommendation = "Cost conversion is above the illustrative 55% threshold. Review expense drivers before proposing reductions."

    return [
        {
            "eyebrow": "ISSUE 01 / OPERATING EFFICIENCY",
            "headline": f"{bank}: {cost:.1f}¢ of each dollar goes to tracked expenses",
            "body": f"In {quarter}, the sample cost-to-revenue ratio is {cost:.1f}%. {movement(row['efficiency_pp_change'], True)}",
            "accent": "pink",
        },
        {
            "eyebrow": "ISSUE 02 / VALUE CREATION",
            "headline": f"Net margin lands at {margin:.1f}%",
            "body": f"Modelled net income accounts for {margin:.1f}¢ of each revenue dollar. {movement(row['margin_pp_change'], False)}",
            "accent": "blue",
        },
        {
            "eyebrow": "ISSUE 03 / DEVICE CIRCULARITY",
            "headline": f"{row['recycled_kg']:,.0f} kg recycled",
            "body": f"Of {row['retired_kg']:,.0f} kg of retired hardware, {recycling:.1f}% was labelled recycled. {movement(row['recycling_pp_change'], False)}",
            "accent": "violet",
        },
        {
            "eyebrow": "ISSUE 04 / ANALYST RECOMMENDATION",
            "headline": "What's the next question?",
            "body": recommendation + " Validate causes with operational teams before making business decisions.",
            "accent": "gold",
        },
    ]

