# Dollars & Devices

**Technology Refresh & Asset Disposition Controls** — a synthetic Business Analyst portfolio case study.

Can we account for every retired device, and what does its disposal cost? The dashboard matches an asset register to recycler receipts, identifies missing or contradictory evidence, and routes exceptions to proposed owners.

## Current demonstration

- 120 invented assets across six fictional institutions; ten assets with deliberately defective evidence (8.33%), plus one orphan receipt.
- Eleven detected exceptions: two missing receipts, two duplicate asset receipts, two weight mismatches, two receipts before retirement, two missing destruction certificates and one orphan receipt.
- 110 assets pass the sample evidence rules. Their disposal charges total CAD 3,520 against CAD 3,300 budget: CAD 220 adverse variance. Unresolved records are excluded from this comparable cost cohort.
- Executive Overview presents finding / so what / next action. The exportable exception register includes evidence, severity, proposed owner, Open status, age and next action.

The separate **Quarterly KPI Learning Case** preserves KPI Proof, configurable scorecards, scenarios and the independent SQLite cross-check. The **Cash Reconciliation Lab** preserves the household education exercise.

## Run and verify

Python 3.11 or newer:

```sh
python -m pip install -r requirements.txt
streamlit run app.py
python -m unittest discover -s tests -v
python scripts/sql_case.py
```

[GitHub Actions](https://github.com/AbhinavKarir/Dollars-and-Devices/actions) runs the regression suite, exact expected-defect assertions and dashboard smoke tests.

## Evidence

- [Business case](docs/business_case.md)
- [Control rules and planted defects](docs/asset_controls.md)
- [Data dictionary](data/data_dictionary.csv)
- [Requirements and test traceability](docs/requirements.md)
- [Learning exercises](exercises/README.md)

The detector reads `data/asset_case/asset_register.csv` and `recycler_receipts.csv`. The separate `tests/fixtures/asset_defect_key.csv` is used only by tests. Defects remain in the input evidence.

## Limitations

All records, institutions, vendors, budgets and assignments are fictional. Evidence-complete means these sample rules pass; it does not verify physical custody, certificate authenticity or regulatory compliance. Costs cover disposal charges only. The asset sample does not roll up to legacy quarterly totals. Investigation updates are not persisted; detected exceptions start Open. No actual interviews, approvals, savings or production outcomes are claimed.

This release implements a bounded foundation of the five-phase plan. Eight-quarter financial analysis, persistent investigation updates, broader navigation redesign and browser accessibility review remain future work. Historical commits are retained.

## How this was built

This portfolio includes AI-assisted development, including this overhaul's implementation, tests and documentation. Published code, synthetic evidence, learning exercises and automated checks make the work inspectable. Passing tests establish tested behaviour; they do not establish independent mastery or real-world business validation.

Project by Abhinav Karir.
