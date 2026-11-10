# Dollars & Devices
### Operations reporting and financial controls | Junior Business Analyst case study

**Project status:** Independent, AI-assisted, synthetic-data portfolio prototype.

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

**Synthetic RBC 2026-Q2 recovery:** 4,000 kg desktops + 2,800 kg ATM terminals + 3,300 kg laptops = 10,100 kg retired; 9,100 kg recycled ÷ 10,100 kg retired × 100 = **90.10%**. KPI proof exposes the inputs, calculation and an independent comparison against the dashboard result.

**Synthetic October cash control:** Opening balance CAD 3,518 + deposits CAD 3,500 − withdrawals CAD 2,626 = **CAD 4,392**, equal to the separately stored sample statement. A CAD 25 artificial mismatch shows how the control flags an exception. Groceries are CAD 25 over their sample budget; dining CAD 32 over. A ledger can reconcile while spending remains over budget.

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

**Formulas:** Efficiency = expenses / revenue × 100. Net margin = net income / revenue × 100. Recycling = recycled kg / retired kg × 100. Portfolio ratios divide summed numerators by summed denominators. Percentage-point movements are rate differences; percentage growth is a relative change. Cash reconciliation = opening + deposits − withdrawals − statement closing. Budget variance = actual expenses − budget.

## What this proves and what it cannot prove

Demonstrates: formulating a business problem, prototype requirements, synthetic data validation, explainable metrics, discrepancy detection, example stakeholder questions, elementary SQL joins and decision communication.

Does not prove: real banking analysis, audited financial accuracy, genuine personal financial management, actual IT sustainability, production SQL systems, stakeholder interviews, a delivered business outcome, or full accounting expertise. Two quarters of invented records do not establish a trend.

## Positioning for Canadian junior BA roles

The intended profile is **Junior Business Analyst – Operations, Performance Reporting and Controls**, not accountant, senior financial analyst or audit professional. Match this portfolio with your own genuine experience in market research, Excel-based tracking, stakeholder coordination and project/operations work.

**Suggested truthful resume bullet after testing:**  
"Developed an AI-assisted business analysis portfolio prototype with Python, pandas, Streamlit, Plotly and SQLite, demonstrating KPI definitions, synthetic data reconciliation, configurable controls, reporting, and requirements documentation."

## Deployment

Deployed on Streamlit Community Cloud from repository `AbhinavKarir/Dollars-and-Devices`, branch `main`, entrypoint `app.py`, using Python 3.11.

Live demo: https://dollars-and-devices-abhinav.streamlit.app/

Deployment checked November 10, 2026: overview loaded; KPI Proof displayed matching calculations and a validation register with 156 checks (138 PASS, 18 N/A, zero FAIL); October Cash Controls reconciled to CAD 4,392; deliberate CAD 25 mismatch correctly triggered the expected failure. The injected error was reset. These checks do not establish comprehensive mobile, accessibility or production readiness.

**Project by Abhinav Karir.** AI-assisted implementation and documentation, with transparent sample data, reproducible calculation definitions and acknowledged limits.
