"""Smoke test the complete Streamlit script without opening a real browser.

Tests that all page logic can run. Visual layout still needs a manual check.
"""
from pathlib import Path
import unittest

from streamlit.testing.v1 import AppTest


class DashboardSmokeTests(unittest.TestCase):
    def test_app_runs_without_exception(self):
        file_path = Path(__file__).resolve().parents[1] / "app.py"
        app = AppTest.from_file(str(file_path), default_timeout=45).run()
        self.assertEqual(
            len(app.exception), 0,
            "Streamlit execution error: " + "; ".join(str(e.message) for e in app.exception),
        )


if __name__ == "__main__":
    unittest.main()
