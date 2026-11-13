"""Independent expected defects, clean cohort, boundaries and altered source evidence."""
from pathlib import Path
import unittest
import pandas as pd
from asset_controls import load_asset_case, reconcile_assets


class AssetControlTests(unittest.TestCase):
    def setUp(self):
        self.assets, self.receipts = load_asset_case()

    def test_exact_documented_defects_and_cost_cohort(self):
        result = reconcile_assets(self.assets, self.receipts)
        key = pd.read_csv(Path(__file__).parent / 'fixtures/asset_defect_key.csv')
        actual = result['exceptions']
        self.assertEqual(set(zip(actual.record_id, actual.rule)), set(zip(key.record_id, key.rule)))
        self.assertEqual(len(actual), len(key))
        self.assertEqual(len(actual.exception_id.unique()), 11)
        self.assertEqual(result['asset_count'], 120)
        self.assertEqual(len(result['matched']), 110)
        self.assertEqual(result['matched'].disposal_cost_cad.sum(), 3520)
        self.assertEqual(result['matched'].disposal_budget_cad.sum(), 3300)
        self.assertTrue(actual.status.eq('Open').all())
        self.assertTrue(actual[['owner', 'next_action', 'evidence']].notna().all().all())
        self.assertTrue(actual.loc[actual.rule != 'ORPHAN_RECEIPT','age_days'].eq(81).all())
        self.assertEqual(actual.loc[actual.rule == 'ORPHAN_RECEIPT','age_days'].tolist(),[71])

    def test_clean_evidence_then_new_missing_receipt(self):
        assets = self.assets.iloc[40:].copy()
        receipts = self.receipts[self.receipts.asset_id.isin(assets.asset_id)].copy()
        self.assertTrue(reconcile_assets(assets, receipts)['exceptions'].empty)
        result = reconcile_assets(assets, receipts.iloc[1:])
        self.assertEqual(result['exceptions'][['record_id','rule']].values.tolist(),
                         [['AST-0041','MISSING_RECEIPT']])
        self.assertEqual(len(result['matched']), 79)

    def test_tolerance_cutoff_and_non_data_device(self):
        a = self.assets.iloc[[40]].copy()
        r = self.receipts[self.receipts.asset_id == a.iloc[0].asset_id].copy()
        r['weight_kg'] = a.iloc[0].expected_weight_kg + .5
        r['certificate_received'] = 'N'
        a['contains_data_media'] = 'N'
        self.assertTrue(reconcile_assets(a, r)['exceptions'].empty)
        r['weight_kg'] += .001
        self.assertEqual(reconcile_assets(a,r)['exceptions'].rule.tolist(), ['WEIGHT_MISMATCH'])
        r['received_date'] = '2026-07-01'
        self.assertEqual(reconcile_assets(a,r)['exceptions'].rule.tolist(), ['MISSING_RECEIPT'])
        a['retired_date'] = '2026-07-02'
        self.assertEqual(reconcile_assets(a,r)['asset_count'], 0)

    def test_ambiguous_ids_and_multiple_rules_are_not_matched(self):
        a = self.assets.iloc[[40]].copy()
        r = self.receipts[self.receipts.asset_id == a.iloc[0].asset_id].copy()
        doubled = pd.concat([r,r],ignore_index=True)
        result = reconcile_assets(a, doubled)
        self.assertEqual(set(result['exceptions'].rule), {'DUPLICATE_RECEIPT_ID','DUPLICATE_ASSET_RECEIPT'})
        self.assertTrue(result['matched'].empty)
        result = reconcile_assets(pd.concat([a,a]),r)
        self.assertEqual(result['exceptions'].rule.tolist(), ['DUPLICATE_ASSET_ID'])
        self.assertTrue(result['matched'].empty)
        r['weight_kg'] = 100
        r['certificate_received'] = 'N'
        r['received_date'] = '2026-04-01'
        self.assertEqual(set(reconcile_assets(a,r)['exceptions'].rule),
                         {'WEIGHT_MISMATCH','MISSING_CERTIFICATE','RECEIPT_BEFORE_RETIREMENT'})

    def test_structural_invalid_inputs_are_explained(self):
        for value in [float('inf'), -1, float('nan')]:
            a = self.assets.copy()
            a['expected_weight_kg'] = a.expected_weight_kg.astype(float)
            a.loc[0,'expected_weight_kg'] = value
            with self.assertRaises(ValueError): reconcile_assets(a,self.receipts)
        with self.assertRaisesRegex(ValueError,'Missing fields'):
            reconcile_assets(self.assets.drop(columns='asset_id'),self.receipts)

    def test_every_source_column_has_dictionary_entry(self):
        root = Path(__file__).resolve().parents[1]
        dictionary = pd.read_csv(root/'data/data_dictionary.csv')
        documented = set(zip(dictionary.dataset,dictionary.column))
        for path in (root/'data').rglob('*.csv'):
            if path.name == 'data_dictionary.csv': continue
            for field in pd.read_csv(path,nrows=0).columns:
                self.assertIn((path.relative_to(root).as_posix(),field),documented)


class AssetDashboardTests(unittest.TestCase):
    def test_default_overview_and_exception_filters(self):
        from streamlit.testing.v1 import AppTest
        app = AppTest.from_file(str(Path(__file__).resolve().parents[1]/'app.py'),default_timeout=45).run()
        self.assertEqual(len(app.exception),0)
        self.assertEqual(app.tabs[0].label,'Executive Overview')
        self.assertEqual(app.metric[0].value,'110 / 120')
        register = next(d.value for d in app.dataframe if 'exception_id' in d.value.columns)
        self.assertEqual(len(register),11)
        app.sidebar.selectbox[0].select('Alder Bank').run()
        self.assertEqual(len(app.exception),0)
        self.assertEqual(app.metric[0].value,'15 / 20')
        next(s for s in app.selectbox if s.label=='Exception status').select('Resolved').run()
        self.assertTrue(any('No exceptions for this filter' in i.value for i in app.info))
