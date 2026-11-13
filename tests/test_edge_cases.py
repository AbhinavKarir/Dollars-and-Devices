"""Adverse-input checks and quarter-over-quarter availability semantics."""
import unittest
from pathlib import Path
from tempfile import TemporaryDirectory
from unittest.mock import patch
import pandas as pd
from analytics import ROOT, load_metrics, load_targets, make_scorecard, story_cards
from metric_audit import trace_metric, validate_dataset
from finance_controls import load_case


class EdgeCaseTests(unittest.TestCase):
    def edited_metrics(self, modify):
        with TemporaryDirectory() as folder:
            finance = pd.read_csv(ROOT / 'data/raw/bank_financials.csv')
            devices = pd.read_csv(ROOT / 'data/raw/bank_ewaste.csv')
            modify(finance, devices)
            finance.to_csv(Path(folder) / 'bank_financials.csv', index=False)
            devices.to_csv(Path(folder) / 'bank_ewaste.csv', index=False)
            return load_metrics(folder)

    def test_gap_does_not_become_quarter_over_quarter_growth(self):
        def modify(money, devices):
            for frame in (money, devices):
                frame.loc[frame.quarter == '2026-Q2', 'quarter'] = '2026-Q3'
        data = self.edited_metrics(modify)
        current = data[(data.bank == 'Alder Bank') & (data.quarter == '2026-Q3')].iloc[0]
        previous = data[(data.bank == 'Alder Bank') & (data.quarter == '2026-Q1')].iloc[0]
        self.assertTrue(pd.isna(current.revenue_growth_pct))
        self.assertTrue(pd.isna(current.efficiency_pp_change))
        self.assertEqual(current.revenue_growth_pct_reason, 'Period gap')
        self.assertEqual(trace_metric(current, 'revenue_growth_pct', previous)['status'], 'UNAVAILABLE')
        self.assertEqual((validate_dataset(data).Result == 'UNAVAILABLE').sum(), 18)

    def test_zero_expense_baseline_is_unavailable_not_infinity(self):
        def modify(money, devices):
            money.loc[(money.bank == 'Alder Bank') & (money.quarter == '2026-Q1'), 'expenses'] = 0
        data = self.edited_metrics(modify)
        first, second = [r for _, r in data[data.bank == 'Alder Bank'].iterrows()]
        self.assertTrue(pd.isna(second.expense_growth_pct))
        self.assertEqual(second.expense_growth_pct_reason, 'Zero baseline')
        self.assertEqual(trace_metric(second, 'expense_growth_pct', first)['status'], 'UNAVAILABLE')
        scores = make_scorecard(second, load_targets()['financial'])
        self.assertEqual(scores[scores.Metric == 'Expense growth minus revenue growth'].iloc[0].Status,
                         'Unavailable: Zero baseline')

    def test_non_finite_inputs_and_malformed_quarters_are_rejected(self):
        for value in (float('inf'), float('-inf')):
            with self.subTest(value=value), self.assertRaisesRegex(ValueError, 'finite'):
                self.edited_metrics(lambda money, devices: money.__setitem__('expenses', value))
        with self.assertRaisesRegex(ValueError, 'quarters'):
            self.edited_metrics(lambda money, devices: money.loc.__setitem__((0, 'quarter'), 'Q2-2026'))

    def test_unrecycled_zero_baseline_is_unavailable(self):
        def modify(money, devices):
            mask = (devices.bank == 'Alder Bank') & (devices.quarter == '2026-Q1')
            devices.loc[mask, 'recycled_kg'] = devices.loc[mask, ['desktops_kg','atm_terminals_kg','laptops_kg']].sum(axis=1)
        data = self.edited_metrics(modify)
        second = data[(data.bank == 'Alder Bank') & (data.quarter == '2026-Q2')].iloc[0]
        self.assertTrue(pd.isna(second.unrecycled_growth_pct))
        self.assertEqual(second.unrecycled_growth_pct_reason, 'Zero baseline')

    def test_cash_non_finite_amounts_are_rejected(self):
        ledger, statements, budgets = load_case()
        with TemporaryDirectory() as folder:
            ledger['amount'] = ledger['amount'].astype(float)
            ledger.loc[0, 'amount'] = float('inf')
            ledger.to_csv(Path(folder)/'transactions.csv', index=False)
            statements.to_csv(Path(folder)/'statements.csv', index=False)
            budgets.to_csv(Path(folder)/'budgets.csv', index=False)
            with self.assertRaisesRegex(ValueError, 'finite'):
                load_case(folder)

    def test_recommendation_uses_changed_configured_target(self):
        row = load_metrics().iloc[0]
        config = load_targets()
        config['financial'][0]['target'] = 40
        self.assertIn('40%', story_cards(row, config)[-1]['body'])


if __name__ == '__main__':
    unittest.main()
