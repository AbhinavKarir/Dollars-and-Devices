# Verification and recruiter review checklist

This checklist separates code-level tests from visual and business acceptance. Do not claim readiness until the required checks are observed.

## Automated checks

- [ ] Python modules compile without syntax errors.
- [ ] All regression and cash reconciliation tests pass.
- [ ] In-memory SQLite output matches pandas calculations.
- [ ] Synthetic source schema and duplicate/denominator rules are enforced.
- [ ] First-quarter comparisons appear as unavailable rather than invented growth.

## Manual walkthrough

- [ ] Open first screen and understand the fictional business case within 60 seconds.
- [ ] Recompute RBC 2026-Q2 efficiency and recycling from the displayed inputs.
- [ ] Check Scotiabank Q1/Q2 efficiency rate, and distinguish percentage points from percent change.
- [ ] Review the October cash ledger: 3518 + 3500 - 2626 = 4392.
- [ ] Inject a deliberate CAD 25 mismatch and confirm it produces a conspicuous failure.
- [ ] Check October groceries and dining over-budget exceptions.
- [ ] Change institution and quarter; see data update in all connected displays.
- [ ] Confirm no chart suggests actual bank performance, a verified environmental impact, or causal evidence.
- [ ] Check text contrast, navigation, and layout on narrow screens.

## Professional honesty

This is an independent portfolio simulation with AI-assisted code. It is not real client engagement, audited bank finance, genuine personal finance, or a production dashboard. Discuss the assumptions and answer questions directly, especially where real stakeholder approval is still needed.

## Reviewer questions

1. Can you demonstrate the formula from raw fields without trusting the displayed result?
2. Is there enough context to justify the analyst recommendation?
3. Which necessary external factors are not in this dataset?
4. Would a new analyst know who must investigate the exception?
5. Are the controls auditable and repeatable?
6. Is the original visual style serving the evidence rather than distracting from it?
