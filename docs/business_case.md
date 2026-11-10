# Business case | Dollars & Devices

**Owner perspective:** Independent junior Business Analyst portfolio case study using fictional data and documented analytical assumptions.

**Business problem:** Performance reporting may show a final percentage without showing the formula, inputs, origin of data, or whether the source reconciles. A management audience needs to understand the question, trust the arithmetic, spot exceptions, and assign an investigation. This fictional case asks how an institution's operating expenses and retired IT assets can be monitored together.

**Industry-neutral capability:** Operations reporting and financial controls. A workplace version could substitute stores, sites, projects, services, or departments for the six fictional bank-labelled entities.

**Scope:** Six wholly synthetic institutional records per quarter in 2026-Q1 and Q2; plus an entirely separate fictional two-month household cash ledger to demonstrate financial literacy. No real bank financial information or personal transactions are used.

**Target job families:** Junior Business Analyst; Junior Operations Analyst; Business Performance/Reporting Analyst; entry-level Business Systems Analyst roles that value documentation, process mapping and data literacy.

## Success criteria for the prototype

- An unfamiliar reviewer understands the question and synthetic-data scope in under one minute.
- Each principal KPI can be independently recalculated from visible source numbers.
- Bad inputs are rejected, and missing historical comparisons are labelled N/A.
- The user can trace one exception to an owner, a next question, and a decision to investigate.
- A statement mismatch of CAD 25 is visibly flagged without altering the original sample records.
- No feature claims actual causal effects, real-world profitability, or verified bank sustainability performance.

These are **prototype acceptance criteria**, not validated stakeholder requirements. Stakeholders below are hypothetical roles.

## Evidence chain

1. Source files: bank financial CSV, bank device CSV, fictional cash ledger/budgets/statements.
2. Controls: schema, expected types, unique institution-period keys, unit/quantity constraints, statement reconciliation.
3. Transformations: efficiency, net margin, recycling rate, percent growth and percentage-point movements.
4. Business rules: scorecard threshold decisions, narrative notes, sensitivity assumptions.
5. Output: clear cards, calculation traces, exception register, downloadable samples, stakeholder next steps.

## Business analysis activities represented

| BA activity | Demonstration in the case | Authenticity note |
| --- | --- | --- |
| Problem definition | Explicit business question and scope | Self-defined scenario |
| Requirements analysis | Requirements matrix with business value and acceptance criteria | Hypothetical stakeholders |
| Data dictionary | Data definitions, formulas and measurement units | Synthetic source fields |
| Data quality | Validation rules and independent arithmetic checks | Tests of fictional data |
| Process mapping | As-is vs proposed-state flow | Conceptual, not an observed organizational process |
| Solution evaluation | Scenario sensitivity and exception analysis | Not predictive |
| Stakeholder engagement | Role-specific business questions | No actual interviews conducted |

## Analytical observation worth discussing

Example: Scotiabank's **synthetic** efficiency ratio rises from approximately 57.8% in Q1 to 58.2% in Q2. Expenses increase faster than revenue. That is a reason to examine expense drivers; it does **not** prove waste, misconduct or a cost-cutting opportunity.

Example: the **synthetic** October household ledger closes at CAD 4,392 and reconciles to its sample statement. Groceries exceed the sample category budget by CAD 25 and dining by CAD 32. This highlights two categories for investigation. The balance tie-out tests arithmetic and source consistency, not accuracy against a genuine third-party bank statement.

## Explicit boundaries

The prototype does not demonstrate a completed stakeholder discovery project, SQL data integration, true financial statement audit, business outcomes achieved, or deployed production controls. Those need real evidence before being claimed on a resume.

A visually distinctive presentation is welcome; it should not outrank correct data, simple language, and meaningful decisions.
