"""Per-lot cost check for IQLT: each open lot's per-share cost against the canonical
price history within five days of its acquisition date (flag if more than 20 percent
away from every price seen in that window).

Usage: python -I iqlt_cost_check.py <canonical.parquet> <lots_csv>
Prints counts and summary only; no account identifiers.
"""
import sys

import pandas as pd

CANON, LOTS_CSV = sys.argv[1], sys.argv[2]
NAME = 'ISHARES MSCI INTL QUALITY FACTOR ETF'

can = pd.read_parquet(CANON, columns=['date', 'asset_name', 'price', 'source'])
can = can[can['asset_name'] == NAME].copy()
can['date'] = pd.to_datetime(can['date'])
can = can.dropna(subset=['price']).sort_values('date')
print('CANON_IQLT_ROWS', len(can), 'range', str(can['date'].min())[:10], str(can['date'].max())[:10])

lots = pd.read_csv(LOTS_CSV)
lots = lots[lots['current_units'] > 0].copy()
lots['acq'] = pd.to_datetime(lots['acq'])
print('OPEN_LOTS_CHECKED', len(lots))
flag_n = 0
no_window = 0
rows = []
for _, r in lots.iterrows():
    lo, hi = r['acq'] - pd.Timedelta(days=5), r['acq'] + pd.Timedelta(days=5)
    w = can[(can['date'] >= lo) & (can['date'] <= hi)]
    cpu = float(r['cost_per_unit'])
    if w.empty:
        no_window += 1
        rows.append((r['acq'].date(), round(cpu, 4), None, None, 'NO_PRICE_WINDOW'))
        continue
    pmin, pmax = float(w['price'].min()), float(w['price'].max())
    # distance from cost to the nearest price seen in the window, as a fraction of that price
    if pmin <= cpu <= pmax:
        dist = 0.0
    else:
        dist = min(abs(cpu - pmin), abs(cpu - pmax)) / min(pmin, pmax)
    flagged = dist > 0.20
    flag_n += int(flagged)
    rows.append((r['acq'].date(), round(cpu, 4), round(pmin, 4), round(pmax, 4),
                 'FLAG' if flagged else 'ok'))

print('LOTS_NO_PRICE_WINDOW', no_window)
print('LOTS_COST_FLAGGED_GT20PCT', flag_n)
print('LOTS_COST_CONSISTENT', len(lots) - flag_n - no_window)
cpu_all = lots['cost_per_unit'].astype(float)
print('COST_PER_UNIT_MIN', round(float(cpu_all.min()), 4), 'MAX', round(float(cpu_all.max()), 4),
      'UNIT_WEIGHTED', round(float(lots['cost_basis'].sum() / lots['current_units'].sum()), 4))
# acquisition-date price of the lots, for the record: canonical close on or nearest after the date
cs = can.set_index('date')['price']
def near(d):
    s = cs.loc[d - pd.Timedelta(days=5): d + pd.Timedelta(days=5)]
    return float(s.iloc[(abs(s.index - d)).argmin()]) if len(s) else None
lots['px_near_acq'] = lots['acq'].apply(near)
print('UNIT_WEIGHTED_NEAR_ACQ_PRICE', round(float((lots['px_near_acq'] * lots['current_units']).sum()
                                                  / lots['current_units'].sum()), 4))
print('CANON_ON_OR_NEAR_2023-03-14', near(pd.Timestamp('2023-03-14')))
print('CANON_ON_OR_NEAR_2024-09-24', near(pd.Timestamp('2024-09-24')))
print('CANON_ON_OR_NEAR_2025-01-13', near(pd.Timestamp('2025-01-13')))
print('CANON_ON_OR_NEAR_2026-10-09', near(pd.Timestamp('2026-10-09')))
