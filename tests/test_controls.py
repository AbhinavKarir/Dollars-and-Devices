"""Tests of transparent KPI traces and fictional household controls."""
import unittest
from pathlib import Path
from tempfile import TemporaryDirectory

import pandas as pd

from analytics import load_metrics, ROOT
from metric_audit import RECIPES, trace_metric, validate_dataset
from finance_controls import load_case, reconcile, budget_variance, continuity_check


class TraceAndControlsTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.data = load_metrics()
        cls.ledger, cls.statements, cls.budgets = load_case()

    def test_kpi_proof_for_latest_quarter(self):
        r = self.data[(self.data.bank == "RBC") & (self.data.quarter == "2026-Q2")].iloc[0]
        for metric in ("efficiency_ratio", "net_margin", "retired_kg", "recycling_rate", "unrecycled_kg"):
            with self.subTest(metric=metric):
                self.assertEqual(trace_metric(r, metric)["status"], "PASS")

    def test_missing_growth_baseline_not_misrepresented(self):
        r = self.data[(self.data.bank == "RBC") & (self.data.quarter == "2026-Q1")].iloc[0]
        self.assertEqual(trace_metric(r, "revenue_growth_pct")["status"], "N/A")
        self.assertEqual(trace_metric(r, "recycling_pp_change")["status"], "N/A")

    def test_internal_register_no_arithmetic_failure(self):
        checks = validate_dataset(self.data)
        self.assertGreater(len(checks), 100)
        self.assertFalse((checks.Result == "FAIL").any())
        self.assertTrue((checks.Result == "N/A").any())

    def test_september_reconciliation(self):
        r = reconcile(self.ledger, self.statements, "2026-09")
        self.assertEqual(r["income"], 3450)
        self.assertEqual(r["expenses"], 2582)
        self.assertEqual(r["closing_calculated"], 3518)
        self.assertTrue(r["reconciled"])

    def test_october_reconciliation(self):
        r = reconcile(self.ledger, self.statements, "2026-10")
        self.assertEqual(r["income"], 3500)
        self.assertEqual(r["expenses"], 2626)
        self.assertEqual(r["closing_calculated"], 4392)
        self.assertTrue(r["reconciled"])
        self.assertTrue(continuity_check(self.statements))

    def test_error_injection_is_detected(self):
        r = reconcile(self.ledger, self.statements, "2026-10", simulated_statement_error=25)
        self.assertEqual(r["difference"], 25)
        self.assertFalse(r["reconciled"])

    def test_budget_exception_amount(self):
        rows = budget_variance(self.ledger, self.budgets, "2026-10")
        grocery = rows[rows.category == "Groceries"].iloc[0]
        dining = rows[rows.category == "Dining"].iloc[0]
        self.assertEqual(grocery["amount"], 455)
        self.assertEqual(grocery["variance"], 25)
        self.assertEqual(dining["variance"], 32)
        self.assertEqual(rows.loc[rows.variance > 0, "variance"].sum(), 57)

    def test_duplicate_transaction_is_rejected(self):
        # Intentionally damage an input file and verify the parser raises an error.
        with TemporaryDirectory() as folder:
            edited = self.ledger.copy()
            edited.loc[1, "transaction_id"] = edited.loc[0, "transaction_id"]
            edited.to_csv(Path(folder) / "transactions.csv", index=False)
            self.statements.to_csv(Path(folder) / "statements.csv", index=False)
            self.budgets.to_csv(Path(folder) / "budgets.csv", index=False)
            with self.assertRaisesRegex(ValueError, "Duplicate transaction ID"):
                load_case(folder)

    def test_zero_revenue_is_rejected(self):
        with TemporaryDirectory() as folder:
            finance = pd.read_csv(ROOT / "data" / "raw" / "bank_financials.csv")
            assets = pd.read_csv(ROOT / "data" / "raw" / "bank_ewaste.csv")
            finance.loc[0, "revenue"] = 0
            finance.to_csv(Path(folder) / "bank_financials.csv", index=False)
            assets.to_csv(Path(folder) / "bank_ewaste.csv", index=False)
            with self.assertRaisesRegex(ValueError, "Revenue must be positive"):
                load_metrics(folder)


if __name__ == "__main__":
    unittest.main()
