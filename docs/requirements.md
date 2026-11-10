# Requirements and acceptance criteria | Illustrative BA artefact

This document is **not** evidence of interviews with actual company stakeholders. These user stories are developed for a simulated internal reporting initiative.

## Assumed stakeholders

- Executive sponsor: wants concise performance and risks, with verifiable figures.
- Finance partner: wants correct finance ratios and controlled reporting definitions.
- Operations lead: needs asset retirement volume, process measures and investigation questions.
- Sustainability/IT asset owner: needs evidence of tracked recoveries and disposition gaps.
- Data analyst/reporting team: wants reproducible source lineage and explicit controls.

## Prioritized backlog

| ID | Priority | Business need | User story | Acceptance criteria | Evidence |
| --- | --- | --- | --- | --- | --- |
| BA-01 | Must | Understand purpose | As a new viewer, I need a plain-language explanation before using filters. | Scope, data units and synthetic disclaimer visible on first screen. | app.py introduction |
| BA-02 | Must | Correct comparable KPIs | As a finance partner, I need efficiency and margin with controlled definitions. | Formula uses expenses/revenue and net_income/revenue; zero revenue rejected; units shown. | analytics.py; tests/test_analytics.py |
| BA-03 | Must | Traceable measures | As a reviewer, I need to recompute a KPI without trusting the chart. | For each listed measure, original fields, source file, formula, independent result and PASS/FAIL/N/A appear. | metric_audit.py; evidence_views.py |
| BA-04 | Must | Data-quality transparency | As a process owner, I need exceptions made visible. | Duplicated bank-quarter, missing values and recycled mass above retirement fail the load. | analytics.py; test suite |
| BA-05 | Must | Financial controls literacy | As an assessor, I need to see a simple cash ledger reconcile to a statement. | Opening + deposits − withdrawals = calculated close; difference shown; artificial CAD 25 mismatch flagged. | finance_controls.py; tests/test_controls.py |
| BA-06 | Must | Budget exceptions | As a budget owner, I need to see which categories exceed targets. | Monthly category actuals and budget variances shown; over-budget categories identifiable. | finance_controls.py |
| BA-07 | Should | Consistent targets | As a sponsor, I need transparent KPI rules. | Four finance and four device metrics, with sample targets stored separately in JSON and no baseline labelled N/A. | config/targets.json |
| BA-08 | Should | Comparative view | As an operations analyst, I need to identify potential investigation candidates. | Selected quarter shown; bubble size explained; no causality claimed. | app.py |
| BA-09 | Should | Sensitivity analysis | As an executive, I need to test assumptions before approving action. | Expense and recycling changes are labelled hypothetical; net income not assumed to improve. | analytics.py |
| BA-10 | Should | Stakeholder relevance | As a BA, I need questions tailored to decision-makers. | Five fictional roles display a distinct business question and engagement method. | app.py |
| BA-11 | Must | Repeatable verification | As a reviewer, I need to detect accidental calculation regressions. | Automated test suite and workflow source in GitHub; results must be observed before claiming passed CI. | tests; .github/workflows/quality.yml |
| BA-12 | Could | Narrative | As a busy viewer, I want a short summary in plain English. | Narrative generated from data without claiming unobserved causes. | analytics.py |

## Example test scenarios

**TS-01:** Select RBC 2026-Q1. The expense-to-revenue rate should be 7900 / 15000 × 100 = 52.6667% (display rounded).

**TS-02:** Select RBC 2026-Q2. Total retired device mass should be 4000 + 2800 + 3300 = 10,100 kg and recycling should be 9100 / 10100 × 100 ≈ 90.0990%.

**TS-03:** Request Q1 revenue growth. Show N/A rather than 0% or an arbitrary growth rate.

**TS-04:** Select October 2026 cash controls. Ledger closing balance should equal sample statement closing balance, CAD 4,392.

**TS-05:** Toggle the artificial CAD 25 statement error. The reconciliation should flag CAD 25, without writing to any CSV.

**TS-06:** Q2 six-institution efficiency must be total expenses ÷ total revenue, not the mean of their individual rates.

**TS-07:** If a fictional input contains more recycled mass than total retired mass, loading should fail with a clear validation message.

## Non-functional requirements

- **Integrity:** no false pass labels for missing comparatives; source amounts must remain unchanged by simulator controls.
- **Interpretability:** explanatory units, labels and methods available to nontechnical stakeholders.
- **Reproducibility:** no paid API, private keys or live external dependencies.
- **Privacy:** only fictional financial records committed; no actual personal statements.
- **Accessibility:** visible text contrast and keyboard-accessible native Streamlit controls.
- **Portability:** run with Python/Streamlit locally or in Streamlit Community Cloud once tested.

## Outstanding gaps for a real employer

Add evidence of actual requirements elicitation, SQL queries/data model, stakeholder sign-off, UAT records, and measurable real-world outcomes only after conducting those activities. Do not retroactively imply they happened in this exercise.
