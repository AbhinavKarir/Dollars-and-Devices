"""Fictional personal cash-flow case: recording, budget analysis, and reconciliation.

For BA financial-literacy demonstration only. This is not a double-entry
accounting system, nor a view of the portfolio owner's actual finances.
"""
from __future__ import annotations

from pathlib import Path
from math import isfinite

import pandas as pd

ROOT = Path(__file__).resolve().parent / "data" / "finance_case"
CATEGORIES = {"Housing", "Groceries", "Transport", "Utilities", "Subscriptions",
              "Dining", "Health", "Shopping"}


def load_case(directory: str | Path | None = None):
    """Load and validate a miniature cash ledger, statement, and budget."""
    location = Path(directory) if directory is not None else ROOT
    ledger = pd.read_csv(location / "transactions.csv")
    statements = pd.read_csv(location / "statements.csv")
    budgets = pd.read_csv(location / "budgets.csv")

    for label, frame, columns in (
        ("Transactions", ledger, {"transaction_id", "date", "description", "category", "direction", "amount", "month"}),
        ("Statements", statements, {"month", "opening_balance", "statement_closing_balance"}),
        ("Budgets", budgets, {"category", "monthly_budget"}),
    ):
        missing = columns - set(frame.columns)
        if missing:
            raise ValueError(f"{label} missing: {sorted(missing)}")
        if frame.empty or frame[list(columns)].isna().any().any():
            raise ValueError(f"{label} is empty or has missing required values.")
    if ledger.transaction_id.duplicated().any():
        raise ValueError("Duplicate transaction ID: every entry must have a unique identifier.")
    if statements.month.duplicated().any() or budgets.category.duplicated().any():
        raise ValueError("Duplicate month or budget category.")
    if not set(ledger.direction).issubset({"in", "out"}):
        raise ValueError("direction must be 'in' or 'out'.")
    if not set(ledger.loc[ledger.direction == "out", "category"]).issubset(CATEGORIES):
        raise ValueError("Unrecognized expense category.")
    if not (ledger.loc[ledger.direction == "in", "category"] == "Income").all():
        raise ValueError("Incoming cash must be categorized as Income.")
    if not set(ledger.loc[ledger.direction == "out", "category"]).issubset(set(budgets.category)):
        raise ValueError("Every expense category needs an approved budget line.")
    if set(budgets.category) != CATEGORIES:
        raise ValueError("The sample budget categories do not match the expected categories.")

    ledger["date"] = pd.to_datetime(ledger.date, errors="raise")
    if not (ledger["date"].dt.strftime("%Y-%m") == ledger["month"]).all():
        raise ValueError("One or more transaction months disagree with transaction dates.")
    ledger["amount"] = pd.to_numeric(ledger["amount"], errors="raise")
    budgets["monthly_budget"] = pd.to_numeric(budgets["monthly_budget"], errors="raise")
    for key in ("opening_balance", "statement_closing_balance"):
        statements[key] = pd.to_numeric(statements[key], errors="raise")
    if not all(series.map(isfinite).all() for series in (
        ledger["amount"], budgets["monthly_budget"], statements["opening_balance"], statements["statement_closing_balance"]
    )):
        raise ValueError("All cash-control amounts must be finite numbers.")
    if (ledger.amount <= 0).any() or (budgets.monthly_budget < 0).any():
        raise ValueError("Amounts must be positive; budgets cannot be negative.")
    if set(ledger.month) != set(statements.month):
        raise ValueError("Every transaction month needs a statement, and vice versa.")
    return ledger.sort_values(["date", "transaction_id"]).reset_index(drop=True), statements.sort_values("month"), budgets


def reconcile(ledger: pd.DataFrame, statements: pd.DataFrame, month: str,
              simulated_statement_error: float = 0.0) -> dict:
    """Compare independently stated closing balance with a calculated cash movement."""
    one_month = ledger.loc[ledger.month == month]
    statement = statements.loc[statements.month == month]
    if len(statement) != 1:
        raise ValueError(f"No unique statement for {month}.")
    opening = float(statement.iloc[0].opening_balance)
    recorded_closing = float(statement.iloc[0].statement_closing_balance) + simulated_statement_error
    incoming = float(one_month.loc[one_month.direction == "in", "amount"].sum())
    outgoing = float(one_month.loc[one_month.direction == "out", "amount"].sum())
    expected = opening + incoming - outgoing
    difference = round(recorded_closing - expected, 2)
    net = incoming - outgoing
    return {
        "month": month,
        "opening": opening,
        "income": incoming,
        "expenses": outgoing,
        "net_cash_flow": net,
        "closing_calculated": expected,
        "closing_statement": recorded_closing,
        "difference": difference,
        "reconciled": abs(difference) < 0.005,
        "cash_surplus_rate": (100 * net / incoming) if incoming else float("nan"),
        "transaction_count": int(len(one_month)),
    }


def budget_variance(ledger: pd.DataFrame, budgets: pd.DataFrame, month: str) -> pd.DataFrame:
    """Positive variance means overspending; negative means under budget."""
    one = ledger.loc[(ledger.month == month) & (ledger.direction == "out")]
    actual = one.groupby("category", as_index=False)["amount"].sum()
    summary = budgets.merge(actual, on="category", how="left", validate="one_to_one")
    summary["amount"] = summary.amount.fillna(0.0)
    summary["variance"] = summary["amount"] - summary["monthly_budget"]
    summary["utilization_pct"] = summary.apply(
        lambda r: 100 * r["amount"] / r["monthly_budget"] if r["monthly_budget"] > 0
        else float("nan"), axis=1
    )
    summary["status"] = summary["variance"].apply(lambda x: "Over budget" if x > 0 else "Within budget")
    return summary.sort_values("variance", ascending=False).reset_index(drop=True)


def continuity_check(statements: pd.DataFrame) -> bool:
    """Prior closing must equal the next opening in chronological sequence."""
    statement_rows = statements.sort_values("month").reset_index(drop=True)
    for i in range(1, len(statement_rows)):
        if abs(float(statement_rows.loc[i, "opening_balance"])
               - float(statement_rows.loc[i - 1, "statement_closing_balance"])) > 0.005:
            return False
    return True

