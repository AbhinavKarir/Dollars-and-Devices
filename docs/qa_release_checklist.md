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
- [ ] Recompute Alder Bank 2026-Q2 efficiency and recycling from the displayed inputs.
- [ ] Check Cedar Bank Q1/Q2 efficiency rate, and distinguish percentage points from percent change.
- [ ] Review the October cash ledger: 3518 + 3500 - 2626 = 4392.
- [ ] Inject a deliberate CAD 25 mismatch and confirm it produces a conspicuous failure.
- [ ] Check October groceries and dining over-budget exceptions.
- [ ] Change institution and quarter; see data update in all connected displays.
- [ ] Confirm no chart suggests actual bank performance, a verified environmental impact, or causal evidence.
- [ ] Check text contrast, navigation, and layout on narrow screens.

## Professional honesty

This is a portfolio simulation, not client engagement or production reporting. Development-method disclosure is in the README. No stakeholder approval or business-user acceptance is claimed.

## Asset controls manual acceptance (not yet executed by business users)

- [ ] Default overview shows 110 / 120 evidence-complete assets and 11 exceptions.
- [ ] Asset register lists missing receipt AST-0001 and duplicate evidence AST-0002.
- [ ] All-institution exception register includes orphan AST-9999; institution-specific views exclude unassigned evidence.
- [ ] Alder Bank filter shows 15 / 20 evidence-complete assets and five exceptions.
- [ ] CSV export includes evidence, status, proposed owner, age and next action.
- [ ] Resolved filter displays an explicit empty state; no persisted resolution is implied.
- [ ] Cost finding identifies the partial cohort: CAD 3,520 vs CAD 3,300.
- [ ] At 375 px and 200% zoom, verify headings, focus order and table access.

## Reviewer questions

1. Can you demonstrate the formula from raw fields without trusting the displayed result?
2. Is there enough context to justify the analyst recommendation?
3. Which necessary external factors are not in this dataset?
4. Would a new analyst know who must investigate the exception?
5. Are the controls auditable and repeatable?
6. Is the original visual style serving the evidence rather than distracting from it?
