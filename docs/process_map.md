# Current and target process | Conceptual simulation

This is a **designed example**, not an observed workflow at a bank or company.

## Before: weak reporting process

~~~mermaid
flowchart TD
A[Finance and IT files arrive] --> B[Analyst copies values into spreadsheet]
B --> C[Charts and KPI cards]
C --> D[Presentation to stakeholders]
D --> E{Can the figures be traced?}
E -->|No| F[Manual rework and clarification]
E -->|Yes| G[Discussion]
~~~

Weaknesses: inconsistent KPI definitions, manually copied numbers, missing checks, undocumented denominator and unclear exception ownership.

## After: prototype process

~~~mermaid
flowchart TD
A[Raw synthetic financial and asset files] --> B[Validate schema units and unique keys]
B --> C{Valid data?}
C -->|No| D[Stop and display source exception]
C -->|Yes| E[Calculate documented KPIs]
E --> F[Independently recompute and compare]
F --> G{Arithmetic matches?}
G -->|No| H[Flag discrepancy and investigate]
G -->|Yes| I[Show performance and target exceptions]
I --> J[Stakeholder interprets context]
J --> K[Assign investigation and next action]
~~~

## Example handoff and decision

Operations notices increasing retired-device mass. IT asset management checks the source inventory and refresh schedule. The sustainability lead checks recycler evidence. The finance partner validates whether related expense movements share a time period. The BA documents the next question, owner and follow-up decision, instead of asserting causality from a scatter plot.

## Future-state evaluation criteria

- KPI explanation and raw source are recoverable within two clicks.
- Invalid or unmatched source records cannot silently populate executive charts.
- Unavailable comparisons have a distinct N/A state.
- Every hypothetical target is clearly labelled as a prototype assumption.
- All discrepancy examples have a visible expected-versus-actual comparison.
