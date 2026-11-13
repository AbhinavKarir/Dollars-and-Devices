"""Executive reporting from reconciled transaction evidence."""
import pandas as pd
import streamlit as st
from asset_controls import load_asset_case, reconcile_assets


def render_asset_controls():
    st.markdown('<div class="report-header"><div class="eyebrow">OPERATIONS CONTROL REVIEW</div>'
                '<h1>Dollars &amp; Devices</h1><p>Technology Refresh &amp; Asset Disposition Controls</p>'
                '<span class="sample-label">SYNTHETIC DATA · DEMONSTRATION ONLY</span></div>', unsafe_allow_html=True)
    st.write('Can we account for every retired device, and what does its disposal cost? '
             'Use the exceptions to assign evidence requests before accepting disposition as complete.')
    try:
        assets, receipts = load_asset_case()
        result = reconcile_assets(assets, receipts)
    except (ValueError, KeyError, FileNotFoundError) as error:
        st.error(f'Unable to reconcile source evidence: {error}')
        return
    with st.sidebar:
        institution = st.selectbox('Disposition institution', ['All institutions', *sorted(assets.institution.unique())])
        st.caption(f"Evidence cut-off: {result['as_of']}. Orphan receipts appear under All institutions.")
    scoped = assets if institution == 'All institutions' else assets[assets.institution == institution]
    issues = result['exceptions']
    matched = result['matched']
    if institution != 'All institutions':
        issues = issues[issues.institution == institution]
        matched = matched[matched.institution == institution]
    total = scoped.asset_id.nunique()
    complete = len(matched)
    unresolved = total - complete
    overview, controls, methodology = st.tabs(['Executive Overview', 'Asset Controls & Actions', 'Data & Methodology'])
    with overview:
        st.caption(f'{institution} | Reporting cut-off {result["as_of"]} | Costs in CAD, weights in kg')
        x, y, z = st.columns(3)
        x.metric('Evidence complete', f'{complete} / {total}')
        y.metric('Assets needing review', str(unresolved))
        z.metric('Open control exceptions', str(len(issues)))
        missing = int((issues.rule == 'MISSING_RECEIPT').sum())
        security = int((issues.rule == 'MISSING_CERTIFICATE').sum())
        cost = float(matched.disposal_cost_cad.sum())
        budget = float(matched.disposal_budget_cad.sum())
        st.subheader('01 / Collection evidence needs follow-up')
        st.write(f'**Finding:** {missing} retired assets have no receipt by cut-off. '
                 '**So what:** Their recorded collection cannot be confirmed. '
                 '**Next action:** IT asset manager to locate each device and request vendor evidence.')
        st.subheader('02 / Data destruction evidence needs review')
        st.write(f'**Finding:** {security} data-bearing assets lack certificate confirmation. '
                 '**So what:** A recycler receipt alone does not demonstrate data destruction. '
                 '**Next action:** Information security to obtain and review destruction evidence.')
        st.subheader('03 / Disposal cost exceeds the sample budget')
        st.write(f'**Finding:** Evidence-complete assets show CAD {cost:,.2f} recorded cost against '
                 f'CAD {budget:,.2f} budget (variance CAD {cost-budget:+,.2f}). '
                 '**So what:** This is a partial, comparable cohort; costs on unresolved receipts are excluded. '
                 '**Next action:** Finance to verify vendor charges and reconcile unresolved items before reporting total programme cost.')
        st.info('Decision requested: assign the open evidence requests to the proposed owners and review the exception export. '
                'Evidence complete means these sample rules passed; it is not an audit opinion or proof of physical disposal.')
    with controls:
        st.header('Which records need attention?')
        status = st.selectbox('Exception status', ['All', 'Open', 'Investigating', 'Resolved'])
        visible = issues if status == 'All' else issues[issues.status == status]
        if visible.empty:
            st.info('No exceptions for this filter. Select All to review available evidence requests.')
        st.dataframe(visible, hide_index=True, width='stretch')
        st.download_button('Download exceptions CSV', visible.to_csv(index=False),
                           file_name='asset_exceptions.csv', mime='text/csv')
        st.caption('Status and owner are proposed assignments. All detected issues start Open. '
                   'This version exports the register; it does not persist investigation updates. '
                   'Age is days since retirement (or receipt for orphan/duplicate receipt identities).')
        with st.expander('Evidence-complete assets and comparable costs'):
            st.dataframe(matched, hide_index=True, width='stretch')
        with st.expander('Raw asset and receipt evidence'):
            st.dataframe(scoped, hide_index=True, width='stretch')
            st.dataframe(receipts if institution == 'All institutions' else receipts[receipts.asset_id.isin(scoped.asset_id)], hide_index=True, width='stretch')
    with methodology:
        st.write('Sources: data/asset_case/asset_register.csv and recycler_receipts.csv. '
                 'One retired asset is expected to have one receipt. Duplicate identities withhold matching. '
                 'Receipt dates must be on or after retirement and no later than cut-off. '
                 'Absolute weight difference above 0.5 kg is an exception. Data-bearing devices require certificate confirmation.')
        st.write('120 invented assets across six fictional institutions; ten assets have deliberately defective evidence '
                 '(8.33%), plus one orphan receipt. The independent expected-defect key is used only by tests. '
                 'This transaction sample does not roll up to the legacy quarterly mass totals. '
                 'Disposal costs cover only receipt charges, not refresh purchases or the full programme.')
        st.write('KPI Proof and its SQLite cross-check remain in the separate Quarterly KPI Learning Case. '
                 'Cash Reconciliation Lab remains a separate household education exercise.')
        from pathlib import Path
        dictionary = pd.read_csv(Path(__file__).resolve().parent / 'data/data_dictionary.csv')
        st.dataframe(dictionary, hide_index=True, width='stretch')
