"""Read-only trace of IQLT lots from the served 2026-10-09 holdings_lots parquet.

Usage: python -I iqlt_lots_read.py <parquet> <accounts_json_or_dash>
Prints aggregates and a per-lot table without client or account identifiers.
"""
import json
import sys

import pandas as pd

path = sys.argv[1]
df = pd.read_parquet(path)
by_ticker = df[df['ticker'] == 'IQLT']
by_name = df[df['asset_name'].astype('string').str.contains('MSCI INTL QUALITY', case=False, na=False)]
print('TOTAL_ROWS', len(df))
print('IQLT_BY_TICKER_ROWS', len(by_ticker), 'accounts', by_ticker['account_id'].nunique())
print('IQLT_BY_ASSETNAME_ROWS', len(by_name), 'accounts', by_name['account_id'].nunique())
print('ASSET_NAMES_FOR_IQLT', sorted(by_ticker['asset_name'].dropna().unique().tolist()))
print('TICKER_NULL_ON_NAME_MATCH', int(by_name['ticker'].isna().sum()))
print('IQLT_OPEN_ROWS', int(by_ticker['is_open'].fillna(False).sum()))
print('PRICE_QUALITY', by_ticker['price_quality'].value_counts(dropna=False).to_dict())
print('CURRENT_PRICE_UNIQUE', sorted(by_ticker['current_price'].dropna().unique().tolist())[:10])
print('IQLT_UNITS', round(float(by_ticker['current_units'].sum()), 4))
print('IQLT_COST_BASIS', round(float(by_ticker['cost_basis'].sum()), 2))
print('IQLT_MARKET_VALUE', round(float(by_ticker['market_value'].sum()), 2))
print('IQLT_ACCRUED_GAIN', round(float(by_ticker['accrued_gain'].sum()), 2))
print('IQLT_MV_UNCAPPED', round(float(by_ticker['market_value_uncapped'].sum()), 2))
print('ACQ_DATE_MIN', str(by_ticker['acquisition_date'].min()))
print('ACQ_DATE_MAX', str(by_ticker['acquisition_date'].max()))

if len(sys.argv) > 2 and sys.argv[2] != '-':
    accts = set(json.load(open(sys.argv[2])))
    sub = by_ticker[by_ticker['account_id'].isin(accts)]
    print('ADVISOR_ACCOUNTS_IN_MAP', len(accts))
    print('ADVISOR_IQLT_ROWS', len(sub), 'accounts', sub['account_id'].nunique())
    print('ADVISOR_IQLT_UNITS', round(float(sub['current_units'].sum()), 4))
    print('ADVISOR_IQLT_COST_BASIS', round(float(sub['cost_basis'].sum()), 2))
    print('ADVISOR_IQLT_MARKET_VALUE', round(float(sub['market_value'].sum()), 2))
    print('ADVISOR_IQLT_ACCRUED_GAIN', round(float(sub['accrued_gain'].sum()), 2))
    print('ADVISOR_IQLT_OLDEST_ACQ', str(sub['acquisition_date'].min()))

cols = ['acquisition_date', 'current_units', 'cost_per_unit', 'cost_basis',
        'current_price', 'market_value', 'accrued_gain', 'price_quality']
view = by_ticker[cols].copy()
view['acquisition_date'] = view['acquisition_date'].dt.strftime('%Y-%m-%d')
view['per_share_cost_check'] = (view['cost_basis'] / view['current_units']).round(4)
view['per_share_mv_check'] = (view['market_value'] / view['current_units']).round(4)
view.to_csv(sys.argv[3] if len(sys.argv) > 3 else '/dev/null', index=False)
print('PER_LOT_CSV_WRITTEN', len(view))
