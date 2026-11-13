# Asset reconciliation rules and evidence

All source records are synthetic. This bounded first slice implements the foundation of agreed Phases 1 and 2. The audit's four-phase roadmap informed the subsequent five-phase implementation order.

## Process

Register retirement → obtain recycler receipt → test identity, dates, weight and certificate confirmation → withhold ambiguous matches → export exceptions to proposed owners → request evidence → rerun after reviewed source corrections.

Assets retired and receipts received on or before **2026-06-30** enter the report. Every retired asset is due for evidence; no grace period applies. Receipts after cut-off are excluded. Receipts without an asset retired in scope are orphan evidence. Mass is kg; costs are CAD disposal charges only.

| Rule | Trigger | Proposed owner |
| --- | --- | --- |
| MISSING_RECEIPT | No receipt by cut-off | IT asset manager |
| DUPLICATE_ASSET_RECEIPT | More than one receipt for asset | Vendor manager |
| DUPLICATE_RECEIPT_ID | Receipt identity reused, even across assets | Vendor manager |
| DUPLICATE_ASSET_ID | Asset identity reused | IT asset manager |
| WEIGHT_MISMATCH | Absolute weight difference exceeds 0.5 kg | IT asset manager |
| RECEIPT_BEFORE_RETIREMENT | Receipt predates retirement | IT asset manager |
| MISSING_CERTIFICATE | Data-bearing device has receipt without Y confirmation | Information security |
| ORPHAN_RECEIPT | No retired asset in scope for receipt | Vendor manager |

Structural errors (missing fields, blanks, invalid dates, non-finite or negative amounts, invalid Y/N flags) stop processing with an explanation. Operational defects remain visible. All applicable receipt rules run; an asset may have multiple exceptions. Duplicate asset identities are withheld before further matching because the asset itself is ambiguous.

Evidence-complete means one unique asset, one uniquely identified receipt, and no failed evidence rule. Ambiguous receipt costs never enter the matched cohort. Asset and exception counts are distinct. These rules cannot establish physical custody, certificate authenticity or regulatory compliance.

## Deliberate defects

| Assets | Planted defect |
| --- | --- |
| AST-0001, AST-0021 | Receipt removed |
| AST-0002, AST-0022 | Additional receipt with distinct receipt ID |
| AST-0003, AST-0023 | Receipt weight increased by 5 kg |
| AST-0004, AST-0024 | Receipt date before retirement |
| AST-0005, AST-0025 | Certificate confirmation N |
| AST-9999 | Receipt references absent asset |

120 assets, ten affected assets (8.33%) and one orphan receipt produce exactly 11 exceptions, 110 evidence-complete assets and 121 raw receipt rows. The remaining assets form a clean control cohort. Tests use a separate expected-defect CSV; runtime code never reads it. Tests also introduce new missing receipts, reused IDs, overlapping rules, tolerance boundaries and cut-off changes.

## Action register limitations

Stable rule/record IDs identify exceptions. Each has evidence, severity, proposed owner, Open status and next action. Age measures days from retirement, or earliest receipt for orphan/reused receipt IDs, to cut-off; it is evidence age, not investigation age. Investigating/Resolved filters show empty states. This version does not save edits or closure evidence.

Eight-quarter expansion, refresh purchase costs, invoice reconciliation, persisted actions, certificate document validation and browser/accessibility review remain outstanding. Legacy quarterly aggregates are separate and cannot validate asset totals.
