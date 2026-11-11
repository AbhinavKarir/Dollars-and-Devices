"""Smoke test the complete Streamlit script without opening a real browser.

Tests that all page logic can run. Visual layout still needs a manual check.
"""
from pathlib import Path
import unittest
from unittest.mock import patch
from analytics import load_targets

from streamlit.testing.v1 import AppTest


class DashboardSmokeTests(unittest.TestCase):
    def test_changed_targets_reach_overview_scorecards_and_investigation(self):
        config = load_targets()
        config["financial"][0].update(target=40, watch_limit=42)
        config["devices"][0].update(target=95, watch_limit=92)
        file_path = Path(__file__).resolve().parents[1] / "app.py"
        with patch("analytics.load_targets", return_value=config):
            app = AppTest.from_file(str(file_path), default_timeout=45).run()
        self.assertEqual(len(app.exception), 0)
        text = "\n".join(element.value for element in app.markdown)
        self.assertIn("40.0% target", text)
        self.assertIn("40 < value ≤ 42", text)
        decisions = next(frame.value for frame in app.dataframe if "Observed signal" in frame.value.columns)
        self.assertIn("illustrative limit 40%", decisions.iloc[0]["Observed signal"])
        self.assertIn("illustrative limit 95%", decisions.iloc[1]["Observed signal"])
        self.assertIn("Configured target: 95%", text)

    def test_reporting_controls_survive_filter_changes(self):
        file_path = Path(__file__).resolve().parents[1] / "app.py"
        app = AppTest.from_file(str(file_path), default_timeout=45).run()
        self.assertEqual(len(app.exception), 0)
        self.assertEqual([tab.label for tab in app.tabs], [
            "Overview", "KPI Proof", "Scorecards",
            "Compare & Decide", "Stakeholders",
        ])
        app.sidebar.selectbox[0].select("RBC")
        app.sidebar.selectbox[1].select_index(0)
        next(s for s in app.selectbox if s.label == "Choose the measure to verify").select(
            "Revenue growth quarter over quarter"
        )
        app.run()
        self.assertEqual(len(app.exception), 0)
        self.assertTrue(any(metric.value == "N/A" for metric in app.metric))
        app.slider[0].set_value(20.0).run()
        self.assertEqual(len(app.exception), 0)
        app.sidebar.radio[0].set_value("Cash Reconciliation Lab").run()
        self.assertEqual(len(app.exception), 0)
        self.assertFalse(any(s.label == "Institution" for s in app.selectbox))
        injection = next(t for t in app.toggle if t.label == "Inject an artificial CAD 25 error")
        injection.set_value(True).run()
        self.assertEqual(len(app.exception), 0)
        self.assertTrue(any("EXPECTED CONTROL FAILURE" in error.value for error in app.error))
        app.sidebar.radio[0].set_value("Operations & Device Reporting").run()
        self.assertEqual(len(app.exception), 0)

    def test_app_runs_without_exception(self):
        file_path = Path(__file__).resolve().parents[1] / "app.py"
        app = AppTest.from_file(str(file_path), default_timeout=45).run()
        self.assertEqual(
            len(app.exception), 0,
            "Streamlit execution error: " + "; ".join(str(e.message) for e in app.exception),
        )


if __name__ == "__main__":
    unittest.main()

