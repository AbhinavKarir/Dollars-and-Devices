"""Asset disposition rules. No UI dependencies or knowledge of the planted defect key."""
from pathlib import Path
import pandas as pd

DATA = Path(__file__).resolve().parent / 'data' / 'asset_case'
ASSET_FIELDS = {'asset_id', 'institution', 'site_type', 'device_type', 'retired_date',
                'expected_weight_kg', 'contains_data_media', 'disposal_budget_cad'}
RECEIPT_FIELDS = {'receipt_id', 'asset_id', 'vendor', 'received_date', 'weight_kg',
                  'certificate_received', 'disposal_cost_cad'}
RULES = {
    'DUPLICATE_ASSET_ID': ('High', 'IT asset manager', 'Correct duplicate asset identity before matching.'),
    'DUPLICATE_RECEIPT_ID': ('High', 'Vendor manager', 'Verify receipt identity and remove duplicate evidence.'),
    'MISSING_RECEIPT': ('High', 'IT asset manager', 'Locate the device and request collection evidence.'),
    'DUPLICATE_ASSET_RECEIPT': ('High', 'Vendor manager', 'Confirm the authoritative receipt; do not double count.'),
    'WEIGHT_MISMATCH': ('Medium', 'IT asset manager', 'Check device identity, scale measurement and source weight.'),
    'RECEIPT_BEFORE_RETIREMENT': ('High', 'IT asset manager', 'Verify retirement and collection dates against source evidence.'),
    'MISSING_CERTIFICATE': ('High', 'Information security', 'Request destruction evidence for the data-bearing device.'),
    'ORPHAN_RECEIPT': ('High', 'Vendor manager', 'Identify the asset or correct the receipt reference.'),
}
EXCEPTION_FIELDS = ['exception_id', 'record_id', 'institution', 'rule', 'severity',
                    'evidence', 'status', 'owner', 'next_action', 'age_days']


def load_asset_case(folder=DATA):
    """Read raw evidence without dropping duplicates or filtering defective records."""
    return (pd.read_csv(Path(folder) / 'asset_register.csv'),
            pd.read_csv(Path(folder) / 'recycler_receipts.csv'))


def reconcile_assets(assets, receipts, as_of='2026-06-30', weight_tolerance_kg=0.5):
    """Reconcile evidence available by cut-off; ambiguous identities never count as matched.

    Structural errors stop processing. Valid but contradictory evidence becomes an exception.
    Weight differences strictly greater than the absolute kg tolerance fail. All retired
    assets are due at the cut-off (no grace period). Age starts at retirement/receipt,
    not an invented investigation date. Financial totals use unambiguous receipts only.
    """
    import math
    if not math.isfinite(weight_tolerance_kg) or weight_tolerance_kg < 0:
        raise ValueError('Weight tolerance must be finite and nonnegative')
    a, r = assets.copy(), receipts.copy()
    cutoff = pd.Timestamp(as_of)
    if pd.isna(cutoff):
        raise ValueError('A reporting cut-off is required')
    for frame, fields, date_field, numeric_fields, flag in [
        (a, ASSET_FIELDS, 'retired_date', ['expected_weight_kg', 'disposal_budget_cad'], 'contains_data_media'),
        (r, RECEIPT_FIELDS, 'received_date', ['weight_kg', 'disposal_cost_cad'], 'certificate_received'),
    ]:
        if not fields.issubset(frame.columns):
            raise ValueError(f'Missing fields: {sorted(fields - set(frame.columns))}')
        if frame[list(fields)].isna().any().any():
            raise ValueError('Required evidence fields cannot be null')
        for field in fields - set(numeric_fields) - {date_field}:
            if frame[field].astype(str).str.strip().eq('').any():
                raise ValueError(f'Blank field: {field}')
        frame[date_field] = pd.to_datetime(frame[date_field], format='%Y-%m-%d', errors='raise')
        if not frame[flag].isin(['Y', 'N']).all():
            raise ValueError(f'{flag} must be Y or N')
        for field in numeric_fields:
            frame[field] = pd.to_numeric(frame[field], errors='raise')
            if not frame[field].map(math.isfinite).all() or (frame[field] < 0).any():
                raise ValueError(f'{field} must be finite and nonnegative')
    a = a[a.retired_date <= cutoff]
    r = r[r.received_date <= cutoff]
    issues = []

    def issue(record, institution, rule, evidence, date):
        severity, owner, action = RULES[rule]
        issues.append(dict(exception_id=f'{rule}:{record}', record_id=record,
                           institution=institution, rule=rule, severity=severity,
                           evidence=evidence, status='Open', owner=owner,
                           next_action=action, age_days=max(0, (cutoff - date).days)))

    duplicate_receipt_ids = set(r.loc[r.receipt_id.duplicated(False), 'receipt_id'])
    for receipt_id in sorted(duplicate_receipt_ids):
        rows = r[r.receipt_id == receipt_id]
        issue(receipt_id, 'Unassigned', 'DUPLICATE_RECEIPT_ID',
              f'{len(rows)} rows share receipt ID; asset references: {sorted(rows.asset_id.unique())}', rows.received_date.min())
    matched = []
    for asset_id, group in a.groupby('asset_id', sort=True):
        asset = group.iloc[0]
        found = r[r.asset_id == asset_id]
        before = len(issues)
        if len(group) != 1:
            issue(asset_id, asset.institution, 'DUPLICATE_ASSET_ID',
                  f'{len(group)} asset rows', asset.retired_date)
            continue
        if found.empty:
            issue(asset_id, asset.institution, 'MISSING_RECEIPT', 'No receipt by cut-off', asset.retired_date)
            continue
        if len(found) > 1:
            issue(asset_id, asset.institution, 'DUPLICATE_ASSET_RECEIPT',
                  f'{len(found)} receipt rows; match withheld', asset.retired_date)
        # Evaluate all candidate receipts; report each rule once per asset.
        if ((found.weight_kg - asset.expected_weight_kg).abs() > weight_tolerance_kg).any():
            issue(asset_id, asset.institution, 'WEIGHT_MISMATCH',
                  f'Expected {asset.expected_weight_kg:g} kg; received {found.weight_kg.tolist()} kg', asset.retired_date)
        if (found.received_date < asset.retired_date).any():
            issue(asset_id, asset.institution, 'RECEIPT_BEFORE_RETIREMENT',
                  'Receipt predates recorded retirement', asset.retired_date)
        if asset.contains_data_media == 'Y' and found.certificate_received.ne('Y').any():
            issue(asset_id, asset.institution, 'MISSING_CERTIFICATE',
                  'Data-bearing asset lacks certificate confirmation', asset.retired_date)
        if len(issues) == before and not found.receipt_id.isin(duplicate_receipt_ids).any():
            matched.append(dict(asset_id=asset_id, institution=asset.institution,
                                disposal_budget_cad=asset.disposal_budget_cad,
                                disposal_cost_cad=found.iloc[0].disposal_cost_cad))
    for asset_id, group in r[~r.asset_id.isin(a.asset_id)].groupby('asset_id', sort=True):
        issue(asset_id, 'Unassigned', 'ORPHAN_RECEIPT',
              f'{len(group)} receipts reference no retired asset in scope', group.received_date.min())
    exceptions = pd.DataFrame(issues, columns=EXCEPTION_FIELDS).sort_values(
        ['severity', 'rule', 'record_id'], kind='stable').reset_index(drop=True)
    matched = pd.DataFrame(matched, columns=['asset_id', 'institution', 'disposal_budget_cad', 'disposal_cost_cad'])
    return {'exceptions': exceptions, 'matched': matched, 'asset_count': a.asset_id.nunique(),
            'receipt_count': len(r), 'as_of': cutoff.date().isoformat()}
