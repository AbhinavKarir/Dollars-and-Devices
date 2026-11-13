"""Run with: python -m unittest discover -s tests -v"""
import unittest

from analytics import load_metrics, make_scorecard, portfolio_summary, scenario, story_cards, target_status, load_targets


class AnalyticsTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.data = load_metrics()
        cls.targets = load_targets()

    def test_expected_grain_and_completeness(self):
        self.assertEqual(len(self.data), 12)
        self.assertEqual(self.data.bank.nunique(), 6)
        self.assertEqual(self.data.quarter.nunique(), 2)
        self.assertFalse(self.data.duplicated(["bank", "quarter"]).any())

    def test_sample_alder_q1_financial_calculations(self):
        row = self.data[(self.data.bank == "Alder Bank") & (self.data.quarter == "2026-Q1")].iloc[0]
        self.assertAlmostEqual(row.efficiency_ratio, 7900 / 15000 * 100)
        self.assertAlmostEqual(row.net_margin, 4000 / 15000 * 100)

    def test_sample_alder_q2_device_calculations(self):
        row = self.data[(self.data.bank == "Alder Bank") & (self.data.quarter == "2026-Q2")].iloc[0]
        self.assertEqual(row.retired_kg, 10100)
        self.assertEqual(row.unrecycled_kg, 1000)
        self.assertAlmostEqual(row.recycling_rate, 9100 / 10100 * 100)

    def test_portfolio_ratios_use_totals(self):
        q = self.data[self.data.quarter == "2026-Q2"]
        result = portfolio_summary(self.data, "2026-Q2")
        self.assertAlmostEqual(result["efficiency_ratio"], 100 * q.expenses.sum() / q.revenue.sum())
        self.assertAlmostEqual(result["recycling_rate"], 100 * q.recycled_kg.sum() / q.retired_kg.sum())

    def test_scenario_does_not_exceed_100_percent_recycling(self):
        row = self.data.iloc[0]
        result = scenario(row, 5, 20)
        self.assertLessEqual(result["recycling_rate"], 100)
        self.assertLess(result["efficiency_ratio"], row.efficiency_ratio)

    def test_threshold_boundaries(self):
        self.assertEqual(target_status(55, 55, "lower", 2), "On target")
        self.assertEqual(target_status(56, 55, "lower", 2), "Watch")
        self.assertEqual(target_status(58, 55, "lower", 2), "Off target")
        self.assertEqual(target_status(85, 85, "higher", 3), "On target")
        self.assertEqual(target_status(83, 85, "higher", 3), "Watch")

    def test_story_and_scorecards(self):
        row = self.data[(self.data.bank == "Birch Trust") & (self.data.quarter == "2026-Q2")].iloc[0]
        stories = story_cards(row)
        self.assertEqual(len(stories), 4)
        self.assertIn("Birch Trust", stories[0]["headline"])
        self.assertEqual(len(make_scorecard(row, self.targets["financial"])), 4)
        self.assertEqual(len(make_scorecard(row, self.targets["devices"])), 4)

    def test_first_quarter_is_not_assigned_fake_growth(self):
        row = self.data[(self.data.bank == "Alder Bank") & (self.data.quarter == "2026-Q1")].iloc[0]
        scores = make_scorecard(row, self.targets["financial"])
        self.assertEqual(scores[scores.Metric == "Revenue growth QoQ"].iloc[0]["Status"], "No baseline")


if __name__ == "__main__":
    unittest.main()
