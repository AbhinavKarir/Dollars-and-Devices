"""Verify documented baseline policy and configured performance boundaries."""
import json
import unittest
from pathlib import Path
from tempfile import TemporaryDirectory

from analytics import load_metrics, load_targets, make_scorecard
from metric_audit import trace_metric, validate_dataset


class GovernanceTests(unittest.TestCase):
    def test_na_results_are_only_first_quarter_growth_checks(self):
        data = load_metrics()
        register = validate_dataset(data)
        self.assertEqual(register.Result.value_counts().to_dict(), {"PASS": 138, "N/A": 18})
        missing = register[register.Result == "N/A"]
        self.assertEqual(set(missing.Quarter), {"2026-Q1"})
        self.assertEqual(set(missing.Check), {
            "Revenue growth quarter over quarter formula",
            "Expense growth quarter over quarter formula", "Recycling rate change formula",
        })
        self.assertTrue((missing.groupby("Bank").size() == 3).all())

    def test_unexpected_missing_current_and_growth_values_fail(self):
        data = load_metrics()
        first = data[data.bank == "RBC"].iloc[0].copy()
        first["revenue"] = first["efficiency_ratio"] = float("nan")
        self.assertEqual(trace_metric(first, "efficiency_ratio")["status"], "FAIL")
        previous, current = [r.copy() for _, r in data[data.bank == "RBC"].iterrows()]
        current["revenue"] = current["revenue_growth_pct"] = float("nan")
        self.assertEqual(trace_metric(current, "revenue_growth_pct", previous)["status"], "FAIL")

    def test_all_configured_scorecard_boundaries(self):
        targets = load_targets()
        for entry in targets["financial"] + targets["devices"]:
            sign = 1 if entry["direction"] == "lower" else -1
            for value, expected in ((entry["target"], "On target"),
                                    (entry["watch_limit"], "Watch"),
                                    (entry["watch_limit"] + sign * .01, "Off target"),
                                    (float("nan"), "No baseline")):
                with self.subTest(metric=entry["metric"], value=value):
                    score = make_scorecard({entry["metric"]: value}, [entry])
                    self.assertEqual(score.iloc[0]["Status"], expected)

    def test_reversed_watch_boundary_is_rejected(self):
        config = load_targets()
        config["financial"][0]["watch_limit"] = 54
        with TemporaryDirectory() as folder:
            path = Path(folder) / "targets.json"
            path.write_text(json.dumps(config), encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "unfavourable"):
                load_targets(path)


if __name__ == "__main__":
    unittest.main()
