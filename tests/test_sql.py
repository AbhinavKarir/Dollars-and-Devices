"""Check SQL report against independent pandas calculations."""
import unittest

from analytics import load_metrics
from scripts.sql_case import sql_results


class SqlReportTests(unittest.TestCase):
    def test_join_grain(self):
        sql = sql_results()
        self.assertEqual(len(sql), 12)
        self.assertFalse(sql.duplicated(["bank", "quarter"]).any())

    def test_sql_values_match_pandas_calculation(self):
        sql = sql_results().set_index(["bank", "quarter"])
        py = load_metrics().set_index(["bank", "quarter"])
        for key in sql.index:
            for metric in ("efficiency_ratio", "net_margin", "recycling_rate", "retired_kg"):
                with self.subTest(key=key, metric=metric):
                    self.assertAlmostEqual(sql.loc[key, metric], py.loc[key, metric], places=8)


if __name__ == "__main__":
    unittest.main()
