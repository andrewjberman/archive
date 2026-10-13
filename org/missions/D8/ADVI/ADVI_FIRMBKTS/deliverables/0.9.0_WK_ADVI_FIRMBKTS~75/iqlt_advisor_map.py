"""Map advisor garrett_newberry to accounts via the served advisor_assignments_history
dimension (current rows), then aggregate IQLT lots of the served 2026-10-09 parquet over
those accounts. Prints counts and totals only; account ids are written to a file outside
the checkout and never printed.

Usage: python -I iqlt_advisor_map.py <assignments.parquet> <lots.parquet> <accounts_out.json>
"""
import json
import sys

import pandas as pd

ASSIGN, LOTS, OUT = sys.argv[1], sys.argv[2], sys.argv[3]
NAME = 'Garrett Newberry'
ROLES = ['architect', 'implementor', 'consultant', 'local_ops', 'additional_advisor']

asg = pd.read_parquet(ASSIGN)
cur = asg[asg['is_current'] == True].copy()  # noqa: E712
mask = pd.Series(False, index=cur.index)
for r in ROLES:
    mask |= (cur[r].astype('string') == NAME).fillna(False)
accts = set(cur.loc[mask, 'account_id'].astype(str))
print('ASSIGN_CURRENT_ACCOUNTS_FOR_ADVISOR', len(accts))
for r in ROLES:
    print('ROLE_COUNT', r, int((cur[r].astype('string') == NAME).sum()))
json.dump(sorted(accts), open(OUT, 'w'))

lots = pd.read_parquet(LOTS, columns=[
    'account_id', 'ticker', 'current_units', 'cost_basis', 'market_value',
    'accrued_gain', 'current_price', 'cost_per_unit', 'market_value_uncapped',
    'acquisition_date'])
adv = lots[lots['account_id'].astype(str).isin(accts)]
print('ADVISOR_LOTS_ALL_TICKERS', len(adv), 'accounts_with_lots', adv['account_id'].nunique())
print('ADVISOR_MV_ALL_TICKERS', round(float(adv['market_value'].sum()), 2))
iq = adv[adv['ticker'] == 'IQLT']
print('ADVISOR_IQLT_LOTS', len(iq), 'accounts', iq['account_id'].nunique())
print('ADVISOR_IQLT_UNITS', round(float(iq['current_units'].sum()), 4))
print('ADVISOR_IQLT_COST_BASIS', round(float(iq['cost_basis'].sum()), 2))
print('ADVISOR_IQLT_MARKET_VALUE', round(float(iq['market_value'].sum()), 2))
print('ADVISOR_IQLT_ACCRUED_GAIN', round(float(iq['accrued_gain'].sum()), 2))
print('ADVISOR_IQLT_MV_UNCAPPED', round(float(iq['market_value_uncapped'].sum()), 2))
print('ADVISOR_IQLT_PRICE_VALUES', sorted(iq['current_price'].dropna().unique().tolist()))
print('ADVISOR_IQLT_OLDEST_ACQ', str(iq['acquisition_date'].min()))
print('ADVISOR_IQLT_NEWEST_ACQ', str(iq['acquisition_date'].max()))
iq_out = iq.copy()
iq_out['acq'] = iq_out['acquisition_date'].dt.strftime('%Y-%m-%d')
iq_out['cost_per_unit_check'] = (iq_out['cost_basis'] / iq_out['current_units']).round(4)
iq_out['mv_per_unit_check'] = (iq_out['market_value'] / iq_out['current_units']).round(4)
iq_out.drop(columns=['account_id', 'acquisition_date']).to_csv(
    OUT.replace('.json', '_iqlt_lots.csv'), index=False)
print('IQLT_LOTS_CSV_WRITTEN', len(iq_out))
