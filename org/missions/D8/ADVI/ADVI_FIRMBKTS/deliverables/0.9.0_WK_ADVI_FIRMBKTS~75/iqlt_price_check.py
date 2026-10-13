"""Read-only price and custodian cross-check for IQLT on the served 2026-10-09 date.

Usage: python -I iqlt_price_check.py <silver_prices_day.parquet> <canonical.parquet>
       <silver_unrealized_day.parquet> <gn_accounts.json> <lots_iqlt_csv> <lots_parquet>
Prints prices, sources and dates, plus custodian market value for the advisor's accounts.
No account numbers are printed.
"""
import json
import sys

import pandas as pd

DAY, CANON, UNREAL, ACCTS, LOTS_CSV, LOTS = sys.argv[1:7]
NAME = 'ISHARES MSCI INTL QUALITY FACTOR ETF'

day = pd.read_parquet(DAY)
d_iq = day[day['asset_name'].astype('string').str.contains('MSCI INTL QUALITY', case=False, na=False)]
print('SILVER_PRICES_DAY_ROWS_NAME_MATCH', len(d_iq))
for _, r in d_iq.iterrows():
    print('SILVER_DAY', str(r['date'])[:10], r['ticker'], r['asset_name'], r['price'], r['source'])

can = pd.read_parquet(CANON)
can['date'] = pd.to_datetime(can['date'])
c_iq = can[can['asset_name'] == NAME].sort_values('date')
print('CANON_ROWS_FOR_IQLT', len(c_iq))
for _, r in c_iq.tail(4).iterrows():
    print('CANON_TAIL', str(r['date'])[:10], r['ticker'], r['price'], r['source'])
oct9 = c_iq[c_iq['date'] == pd.Timestamp('2026-10-09')]
print('CANON_ON_2026-10-09', [(float(x), s) for x, s in zip(oct9['price'], oct9['source'])])
# distinct prices over the last 30 days, to see whether 49.84 is a stable quote
recent = c_iq[c_iq['date'] >= pd.Timestamp('2026-09-01')]
print('CANON_SEP_OCT_PRICE_SET', sorted(set(round(float(x), 4) for x in recent['price'])))

# Near-date price history for lot acquisitions is handled in the lot script.
un = pd.read_parquet(UNREAL)
u_iq = un[(un['ticker'] == 'IQLT') | (un['asset_name'].astype('string').str.contains('MSCI INTL QUALITY', case=False, na=False))]
accts = set(json.load(open(ACCTS)))
u_adv = u_iq[u_iq['account_id'].astype(str).isin(accts)]
print('CUSTODIAN_IQLT_ROWS_ALL', len(u_iq), 'accounts', u_iq['account_id'].nunique())
print('CUSTODIAN_IQLT_ROWS_ADVISOR', len(u_adv), 'accounts', u_adv['account_id'].nunique())
print('CUSTODIAN_IQLT_MV_ADVISOR', round(float(u_adv['market_value'].sum()), 2))
print('CUSTODIAN_IQLT_MV_ALL', round(float(u_iq['market_value'].sum()), 2))
print('CUSTODIAN_IQLT_UNIT_COST_RANGE_ADVISOR',
      (round(float(u_adv['unit_cost'].min()), 4), round(float(u_adv['unit_cost'].max()), 4))
      if len(u_adv) else None)

lots = pd.read_csv(LOTS_CSV)
lot_units = float(lots['current_units'].sum())
print('LOT_UNITS_ADVISOR_OPEN_OR_ALL', round(lot_units, 4))
if len(u_adv):
    print('CUSTODIAN_MV_PER_LOT_UNIT_ADVISOR', round(float(u_adv['market_value'].sum()) / lot_units, 4))
print('LOT_MV_UNCAPPED_PER_UNIT', round(float(lots['market_value_uncapped'].sum()) / lot_units, 4)
      if 'market_value_uncapped' in lots.columns else 'col-absent')
