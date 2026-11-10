"""Smoke test the complete Streamlit script without opening a real browser.

Tests that all page logic can run. Visual layout still needs a manual check.
"""
from pathlib import Path
import unittest

from streamlit.testing.v1 import AppTest


class DashboardSmokeTests(unittest.TestCase):
    def test_reporting_controls_survive_filter_changes(self):
        file_path = Path(__file__).resolve().parents[1] / "app.py"
        app = AppTest.from_file(str(file_path), default_timeout=45).run()
        self.assertEqual(len(app.exception), 0)
        self.assertEqual([tab.label for tab in app.tabs], [
            "Overview", "KPI Proof", "Cash Controls", "Scorecards",
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
        injection = next(t for t in app.toggle if t.label == "Inject an artificial CAD 25 error")
        injection.set_value(True).run()
        self.assertEqual(len(app.exception), 0)
        self.assertTrue(any("EXPECTED CONTROL FAILURE" in error.value for error in app.error))
        app.slider[0].set_value(20.0).run()
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
