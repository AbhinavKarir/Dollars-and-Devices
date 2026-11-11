# Dollars & Devices
### Operations reporting and financial controls | Junior Business Analyst case study

**Project status:** Synthetic-data business analysis portfolio prototype.

**[Open the live dashboard](https://dollars-and-devices-abhinav.streamlit.app/)**

> A manager should be able to answer three questions about any KPI: where did the number come from, how was it calculated, and what decision can it actually support?

This project was designed to demonstrate business analysis skills useful beyond banking: defining KPIs, validating information, documenting requirements, reconciling a small cash ledger, interpreting budget variance, examining operational risks, and communicating recommendations. It uses fictional institution-labelled finance and e-waste records plus a separate synthetic personal cash-flow exercise. No figures are genuine company performance or private user information.

## What the dashboard does

| Screen | Business question | Demonstrated skill |
| --- | --- | --- |
| Overview | What changed, and where should we investigate? | KPI definitions, evidence-led narrative, weighted portfolio ratios |
| KPI proof | Can we independently reproduce the result? | Raw inputs, formulas, source lineage and validation register |
| Cash controls | Does the ledger reconcile, and what is over budget? | Financial literacy, reconciliation, variance analysis and exception detection |
| Scorecards | Which illustrative targets are missed? | Configurable business rules and missing-baseline handling |
| Compare & decide | Which profiles need investigation? | Cross-comparison and sensitivity assumptions |
| Stakeholders | Who needs which question answered? | Stakeholder segmentation, process and decision framing |

The executive reporting interface uses navy, white and royal blue, with teal for sustainability. Institution accents appear only in comparison charts. There are no corporate logos. KPI evidence and sample-data limitations remain visible.

## Try it

Requires Python 3.11 or newer. From the project directory:

    python -m pip install -r requirements.txt
    streamlit run app.py

Verify calculations:

    python -m unittest discover -s tests -v
    python scripts/sql_case.py

A GitHub Actions workflow file also describes compile and unit-test checks. **Check the Actions tab for a real result before calling CI successful.**

## Worked examples

**Synthetic RBC 2026-Q2 recovery:** 4,000 kg desktops + 2,800 kg ATM terminals + 3,300 kg laptops = 10,100 kg retired; 9,100 kg recycled Ã· 10,100 kg retired Ã— 100 = **90.10%**. KPI proof exposes the inputs, calculation and an independent comparison against the dashboard result.

**Synthetic October cash control:** Opening balance CAD 3,518 + deposits CAD 3,500 âˆ’ withdrawals CAD 2,626 = **CAD 4,392**, equal to the separately stored sample statement. A CAD 25 artificial mismatch shows how the control flags an exception. Groceries are CAD 25 over their sample budget; dining CAD 32 over. A ledger can reconcile while spending remains over budget.

## Business analysis artefacts

- [Business case and boundaries](docs/business_case.md)
- [Prioritized requirements and acceptance criteria](docs/requirements.md)
- [Conceptual before/after process map](docs/process_map.md)
- [Sample analytical observations](docs/analyst_notes.md)

These are authored portfolio case-study artefacts, **not** records of actual stakeholder interviews, real organizational sign-off or client UAT.

## Files and evidence

| File | Role |
| --- | --- |
| app.py | Streamlit UI, filters, executive and decision views |
| analytics.py | Base dataset validation and financial/e-waste calculations |
| metric_audit.py | Independently recalculates KPIs and prepares a data-quality register |
| finance_controls.py | Reads separate cash ledger, statements and budgets; performs reconciliation |
| evidence_views.py | Makes arithmetic and reconciliation evidence visible in the app |
| config/targets.json | Hypothetical finance and IT-device operating thresholds |
| scripts/sql_case.py | SQLite in-memory join and independent KPI calculation example |
| tests/ | Automated regression and financial-controls tests |
| .github/workflows/quality.yml | CI workflow definition |
| data/raw/ | Invented institution finance and device records |
| data/finance_case/ | Invented household cash transactions, statements and budgets |

## Calculation definitions

Calculations use unrounded inputs. Financial source amounts are CAD millions; cash-control amounts are CAD; device mass is kilograms. Display rounding does not change the underlying calculation.

| Measure | Calculation | Output |
| --- | --- | --- |
| Operating efficiency | `expenses / revenue * 100` | % |
| Net income margin | `net_income / revenue * 100` | % |
| Retired device mass | `desktops_kg + laptops_kg + atm_terminals_kg` | kg |
| Recycling rate | `recycled_kg / retired_kg * 100` | % |
| Unrecycled mass | `retired_kg - recycled_kg` | kg, not necessarily landfill |
| Revenue growth | `(current_revenue / previous_revenue - 1) * 100` | % |
| Expense growth | `(current_expenses / previous_expenses - 1) * 100` | % |
| Recycling rate change | `current_rate - previous_rate` | percentage points |
| Portfolio ratio | `sum(numerator) / sum(denominator) * 100` | %, weighted by denominator |
| Calculated cash closing | `opening + deposits - withdrawals` | CAD |
| Reconciliation difference | `statement_closing - calculated_closing` | CAD, rounded to cents |
| Budget variance | `actual_expenses - budget` | CAD, positive means over budget |

Growth requires a previous observation and a nonzero prior denominator. The current sample contains consecutive quarters; the implementation compares previous available observations and does not enforce a complete quarterly calendar. A future gap must be investigated before describing its change as quarter-over-quarter.

## Data Governance & Lineage

### Sources and transformation path

All records are invented portfolio data. Institution names are labels, not evidence of actual institutional performance. The portfolio maintainer manages the sample files and rule definitions; business owners mentioned in the case study are proposed roles, not actual approvers.

| Source | Grain and lineage | Consumer |
| --- | --- | --- |
| `data/raw/bank_financials.csv` | One institution-quarter; revenue, expenses and net income | `analytics.load_metrics` validates inputs, joins devices on `bank, quarter`, then calculates finance KPIs |
| `data/raw/bank_ewaste.csv` | One institution-quarter; retired categories and recycled mass | Same one-to-one join, followed by device KPIs and comparisons |
| `data/finance_case/transactions.csv` | One transaction ID, with date, month, direction, category and amount | `finance_controls.load_case`, cash reconciliation and budget aggregation |
| `data/finance_case/statements.csv` | One month with opening and separately stored sample closing balance | Closing-balance reconciliation and continuity check |
| `data/finance_case/budgets.csv` | One category with a monthly budget | Category actual-versus-budget comparison |
| `config/targets.json` | Illustrative targets, explicit watch limits and formula tolerances | Scorecards and KPI formula checks |

`metric_audit.py` independently recalculates selected KPIs from raw operands. KPI Proof shows source fields, formulas, computed values and PASS/FAIL/N/A results. `scripts/sql_case.py` provides an additional SQLite join/calculation example. Historical `data/processed/` files are learning outputs and are not inputs to the current application. Learning scripts live in [`exercises/`](exercises/).

### Thirteen checks producing 156 results

The current validation register evaluates **13 check definitions for each of 12 institution-quarter rows**, producing **156 results**, not 156 distinct rules. Input-loader checks and separate cash-control tests are additional controls outside this count.

| Check group | Definitions applied per row | Expected result |
| --- | --- | --- |
| Formula reconciliation (8) | Efficiency, net margin, retired mass, recycling rate, unrecycled mass, revenue growth, expense growth, recycling-rate change | Independently calculated value matches the dashboard within configured absolute/relative tolerance, both `1e-9` |
| Integrity (5) | Non-negative retired mass; recycled mass between zero and retired mass; recycling rate between 0 and 100%; positive revenue; unique institution-quarter | PASS when the condition holds; otherwise FAIL |

For the checked-in sample, the expected totals are **138 PASS, 18 N/A, 0 FAIL**. The 18 N/A results are exactly **6 institutions × 3 baseline-dependent formulas** in **2026-Q1**: revenue growth, expense growth and recycling-rate change. Q1 has no earlier observation. Those values remain missing rather than being invented as zero. Q2 has a baseline and all eight formulas are checked. Unexpected missing formula values are FAIL, not N/A. Counts change when records or check definitions change.

### Thresholds and exception handling

Business performance and data validity have different meanings:

- **On target / Watch / Off target:** illustrative performance classifications. `target`, `direction` and `watch_limit` define the boundaries explicitly in the configuration. For efficiency, `<=55%` is On target, `>55%` through `57%` is Watch, and `>57%` is Off target. For recycling, `>=85%` is On target, `82%` through `<85%` is Watch, and `<82%` is Off target. Boundary equality belongs to Watch at the watch limit. These are case-study assumptions, not bank-approved limits.
- **PASS / FAIL / N/A:** formula or integrity results. Formula comparison uses the configured numeric tolerances; integrity conditions are exact comparisons. No baseline is an expected limitation, not a performance failure.
- **Cash controls:** reconciliation compares statement closing with calculated closing, rounded to cents; a nonzero cent difference fails. The artificial CAD 25 mismatch is a deliberate test. Continuity compares adjacent statement balances with a CAD 0.005 tolerance. These cash checks are separate from the 156-result KPI register.

The input loader rejects missing columns/values, duplicate keys, non-numeric amounts, invalid sample signs, nonpositive ratio denominators and unmatched finance/device records before the dashboard renders. For a later FAIL, inspect the source row and join keys, reproduce the formula, correct the source or code with evidence, and rerun tests before relying on the affected KPI. Off-target performance calls for investigation of business drivers rather than editing data to make it pass. The prototype displays validation results but does not implement an enterprise quarantine, approval or incident-management workflow.

Missing-baseline handling does not cover every possible data issue. Calendar gaps, zero prior growth denominators, external source verification and production access controls require further work before production use. Changes to sample data or thresholds should be reviewed through a versioned Git change and the automated checks rerun.

## What this proves and what it cannot prove

Demonstrates: formulating a business problem, prototype requirements, synthetic data validation, explainable metrics, discrepancy detection, example stakeholder questions, elementary SQL joins and decision communication.

Does not prove: real banking analysis, audited financial accuracy, genuine personal financial management, actual IT sustainability, production SQL systems, stakeholder interviews, a delivered business outcome, or full accounting expertise. Two quarters of invented records do not establish a trend.

## Positioning for Canadian junior BA roles

The intended profile is **Junior Business Analyst â€“ Operations, Performance Reporting and Controls**, not accountant, senior financial analyst or audit professional. Match this portfolio with your own genuine experience in market research, Excel-based tracking, stakeholder coordination and project/operations work.

**Example resume bullet (only claim work you can personally demonstrate):**  
"Developed a business analysis portfolio prototype with Python, pandas, Streamlit, Plotly and SQLite to demonstrate KPI definitions, synthetic data reconciliation, reporting controls and requirements documentation."

## Deployment

Deployed on Streamlit Community Cloud from repository `AbhinavKarir/Dollars-and-Devices`, branch `main`, entrypoint `app.py`, using Python 3.11.

Live demo: https://dollars-and-devices-abhinav.streamlit.app/

Deployment checked November 10, 2026: overview loaded; KPI Proof displayed matching calculations and a validation register with 156 checks (138 PASS, 18 N/A, zero FAIL); October Cash Controls reconciled to CAD 4,392; deliberate CAD 25 mismatch correctly triggered the expected failure. The injected error was reset. These checks do not establish comprehensive mobile, accessibility or production readiness.

**Project by Abhinav Karir.** Synthetic datasets, reproducible calculations, and automated tests are published for review.

