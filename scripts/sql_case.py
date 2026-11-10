"""Reproducible SQLite cross-check for two synthetic CSV datasets.

Run: python scripts/sql_case.py
Demonstrates a two-key JOIN and ratio calculations independent of pandas.
This is a local in-memory database, not a production SQL connection.
"""
from __future__ import annotations

import sqlite3
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parent.parent

SQL = """
SELECT
    f.bank,
    f.quarter,
    f.revenue,
    f.expenses,
    f.net_income,
    (100.0 * f.expenses / f.revenue) AS efficiency_ratio,
    (100.0 * f.net_income / f.revenue) AS net_margin,
    (e.desktops_kg + e.laptops_kg + e.atm_terminals_kg) AS retired_kg,
    (100.0 * e.recycled_kg / (e.desktops_kg + e.laptops_kg + e.atm_terminals_kg)) AS recycling_rate
FROM finance f
INNER JOIN ewaste e ON f.bank = e.bank AND f.quarter = e.quarter
ORDER BY f.bank, f.quarter
"""


def sql_results(root: Path = ROOT) -> pd.DataFrame:
    finance = pd.read_csv(root / "data" / "raw" / "bank_financials.csv")
    ewaste = pd.read_csv(root / "data" / "raw" / "bank_ewaste.csv")
    with sqlite3.connect(":memory:") as conn:
        finance.to_sql("finance", conn, index=False)
        ewaste.to_sql("ewaste", conn, index=False)
        return pd.read_sql_query(SQL, conn)


if __name__ == "__main__":
    rows = sql_results()
    print("Rows returned:", len(rows))
    print(rows[["bank", "quarter", "efficiency_ratio", "recycling_rate"]].round(2).to_string(index=False))
