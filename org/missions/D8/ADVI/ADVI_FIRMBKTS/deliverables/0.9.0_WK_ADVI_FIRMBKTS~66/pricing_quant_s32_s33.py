"""FB-h-7 read-only quantification, S32 and S33 (replication of product READ logic).

Inputs are local copies of SERVED S3 objects fetched with `aws s3api get-object`
into C:/dev/wk-firmbkts-66-data/ (outside the checkout). No producer script is run.
Run with: python -I pricing_quant_s32_s33.py
"""
import json
import os
import sys

import numpy as np
import pandas as pd

DATA = 'C:/dev/wk-firmbkts-66-data'
MAX_UNIT_PRICE = 100_000          # bd_price_update.py line 59
TOL = 1e-6                        # S32 threshold named in the order
TRADE_DATE = pd.Timestamp('2026-10-09')
DAILY_NAME_FMT = '{}.parquet'

os.chdir(DATA)


def t1_median(df):
    """Verbatim READ logic of extract_t1_prices (bd_price_update.py lines 327-345)."""
    valid = df[
        df['asset_name'].notna() &
        df['units'].notna() & (df['units'].abs() > 1e-8) &
        df['market_value'].notna() & (df['market_value'] != 0)
    ].copy()
    valid['calc_price'] = valid['market_value'].abs() / valid['units'].abs()
    valid = valid[(valid['calc_price'] > 0) & (valid['calc_price'] < MAX_UNIT_PRICE)]
    if valid.empty:
        return {}
    return valid.groupby('asset_name')['calc_price'].median().to_dict()


def s32():
    days = [d.strip() for d in open('last20.lf', encoding='utf-8').read().splitlines() if d.strip()]
    asset_days = 0
    changes = 0
    changed_assets = set()
    max_delta = 0.0
    missing_one_side = 0
    per_day = []
    served_check = {'compared': 0, 'equal_to_recompute': 0, 'rows_transaction_observed': 0}
    latest_day_detail = None
    canon = pd.read_parquet('latest/prices/canonical_prices.parquet')
    canon['date'] = pd.to_datetime(canon['date'])
    for d in days:
        raw = pd.read_parquet(f'latest/txn/{d}.parquet')
        a = t1_median(raw)                                              # (a) as the code does
        dedup = raw.drop_duplicates(subset=['transaction_id'], keep='first')
        b = t1_median(dedup)                                            # (b) de-duplicated
        keys = set(a) | set(b)
        day_changes = 0
        for k in keys:
            asset_days += 1
            if k in a and k in b:
                delta = abs(a[k] - b[k])
                if delta > TOL:
                    day_changes += 1
                    changed_assets.add(k)
                    max_delta = max(max_delta, delta)
                    if d == days[-1]:
                        latest_day_detail = latest_day_detail or {}
                        latest_day_detail[k] = (a[k], b[k])
            else:
                missing_one_side += 1
                day_changes += 1
                changed_assets.add(k)
        changes += day_changes
        per_day.append({'date': d, 'rows': int(len(raw)), 'distinct_tid': int(raw['transaction_id'].nunique()),
                        'assets_a': len(a), 'assets_b': len(b), 'changed': day_changes})
        # Served-value check: served canonical T1 rows for this day vs recompute (a).
        srv = canon[(canon['date'] == pd.Timestamp(d)) & (canon['source'] == 'transaction_observed')]
        served_check['rows_transaction_observed'] += int(len(srv))
        for _, r in srv.iterrows():
            if r['asset_name'] in a:
                served_check['compared'] += 1
                if abs(float(r['price']) - a[r['asset_name']]) <= 1e-6:
                    served_check['equal_to_recompute'] += 1
    # Served holdings quantity for the latest snapshot available (2026-10-09) on the same day.
    sum_x_qty = None
    qty_note = None
    if latest_day_detail is None:
        latest_day_detail = {}
    hl = pd.read_parquet('latest/holdings_lots_2026-10-09.parquet', columns=['asset_name', 'current_units'])
    qty = hl.groupby('asset_name')['current_units'].sum().abs()
    # Recompute the same-day changes for 2026-10-09 explicitly (the latest snapshot date).
    raw9 = pd.read_parquet('latest/txn/2026-10-09.parquet')
    a9 = t1_median(raw9)
    b9 = t1_median(raw9.drop_duplicates(subset=['transaction_id'], keep='first'))
    tot = 0.0
    n9 = 0
    for k in set(a9) & set(b9):
        if abs(a9[k] - b9[k]) > TOL and k in qty.index:
            tot += abs(a9[k] - b9[k]) * float(qty[k])
            n9 += 1
    sum_x_qty = round(tot, 6)
    qty_note = {'day': '2026-10-09', 'changed_assets_with_holdings': n9}
    return {
        'days': days,
        'asset_days_considered': asset_days,
        'asset_days_median_changes': changes,
        'assets_affected': len(changed_assets),
        'max_abs_price_delta': round(max_delta, 6),
        'missing_one_side': missing_one_side,
        'sum_abs_price_delta_x_qty': sum_x_qty,
        'sum_qty_note': qty_note,
        'per_day': per_day,
        'served_check': served_check,
    }


def load_price_frames():
    keys = [k.strip() for k in open('price_keys.lf', encoding='utf-8').read().splitlines() if k.strip()]
    frames = []
    for k in sorted(keys):                                    # same order as B_01 load_latest_prices
        name = os.path.basename(k)
        df = pd.read_parquet(f'latest/prices/{name}')
        df['__src'] = name
        frames.append(df)
    return frames


def s33():
    frames = load_price_frames()
    prices = pd.concat(frames, ignore_index=True)
    prices['date'] = pd.to_datetime(prices['date'])
    # Exact code order: sort_values('date', ascending=False) (default kind), keep first per asset.
    latest = (prices.sort_values('date', ascending=False)
              .drop_duplicates(subset=['asset_name'], keep='first'))
    # Negative control: the same operation on the frame without the __src column must pick the same rows.
    plain = pd.concat([f.drop(columns=['__src']) for f in frames], ignore_index=True)
    plain['date'] = pd.to_datetime(plain['date'])
    plain_latest = (plain.sort_values('date', ascending=False)
                    .drop_duplicates(subset=['asset_name'], keep='first'))
    same_pick = bool(
        len(plain_latest) == len(latest) and
        (plain_latest['asset_name'].values == latest['asset_name'].values).all() and
        np.allclose(plain_latest['price'].values.astype(float), latest['price'].values.astype(float))
    )
    d_daily = prices[(prices['date'] == TRADE_DATE) & (prices['__src'] == DAILY_NAME_FMT.format('2026-10-09'))]
    d_canon = prices[(prices['date'] == TRADE_DATE) & (prices['__src'] == 'canonical_prices.parquet')]
    dup_daily = int(d_daily['asset_name'].duplicated().sum())
    dup_canon = int(d_canon['asset_name'].duplicated().sum())
    tied = sorted(set(d_daily['asset_name']) & set(d_canon['asset_name']))
    dp = d_daily.drop_duplicates('asset_name', keep='first').set_index('asset_name')
    cp = d_canon.drop_duplicates('asset_name', keep='first').set_index('asset_name')
    lw = latest.set_index('asset_name')
    win_daily = win_canon = win_other = 0
    alt_differs = 0
    max_delta = 0.0
    nondecisive = []
    for a in tied:
        wsrc = lw.loc[a, '__src']
        wdate = lw.loc[a, 'date']
        wprice = float(lw.loc[a, 'price'])
        pd_ = float(dp.loc[a, 'price'])
        pc_ = float(cp.loc[a, 'price'])
        max_delta = max(max_delta, abs(pd_ - pc_))
        if wdate != TRADE_DATE:
            win_other += 1
            nondecisive.append(a)
            continue
        if wsrc == DAILY_NAME_FMT.format('2026-10-09'):
            win_daily += 1
            other = pc_
        elif wsrc == 'canonical_prices.parquet':
            win_canon += 1
            other = pd_
        else:
            win_other += 1
            continue
        if abs(other - wprice) > 1e-9:
            alt_differs += 1
    return {
        'pandas_version': pd.__version__,
        'numpy_version': np.__version__,
        'frames': len(frames),
        'rows_total': int(len(prices)),
        'negative_control_same_pick': same_pick,
        'daily_rows_on_date': int(len(d_daily)),
        'canonical_rows_on_date': int(len(d_canon)),
        'dup_asset_rows_daily': dup_daily,
        'dup_asset_rows_canonical': dup_canon,
        'tied_assets': len(tied),
        'winner_in_daily_file': win_daily,
        'winner_in_canonical_prices': win_canon,
        'winner_other_date_or_unknown': win_other,
        'alternative_differs': alt_differs,
        'max_abs_price_delta': round(max_delta, 6),
        'nondecisive_assets': nondecisive[:50],
    }


def s33_asof():
    """Sensitivity (inferred): the same selection on the file set as it stood at the 2026-10-09 run,
    i.e. daily files dated <= 2026-10-09 and canonical rows dated <= 2026-10-09 (current canonical
    object, filtered; its historical versions were not replayed)."""
    frames = []
    for f in load_price_frames():
        f = f[f['date'].astype('datetime64[ns]') <= TRADE_DATE] if f['__src'].iloc[0] == 'canonical_prices.parquet' else f
        if f['__src'].iloc[0] != 'canonical_prices.parquet' and pd.to_datetime(f['date']).max() > TRADE_DATE:
            continue
        frames.append(f)
    prices = pd.concat(frames, ignore_index=True)
    prices['date'] = pd.to_datetime(prices['date'])
    latest = (prices.sort_values('date', ascending=False)
              .drop_duplicates(subset=['asset_name'], keep='first'))
    d_daily = prices[(prices['date'] == TRADE_DATE) & (prices['__src'] == '2026-10-09.parquet')]
    d_canon = prices[(prices['date'] == TRADE_DATE) & (prices['__src'] == 'canonical_prices.parquet')]
    tied = sorted(set(d_daily['asset_name']) & set(d_canon['asset_name']))
    dp = d_daily.drop_duplicates('asset_name', keep='first').set_index('asset_name')
    cp = d_canon.drop_duplicates('asset_name', keep='first').set_index('asset_name')
    lw = latest.set_index('asset_name')
    win_daily = win_canon = other_date = alt = 0
    max_delta = 0.0
    for a in tied:
        wsrc, wdate, wprice = lw.loc[a, '__src'], lw.loc[a, 'date'], float(lw.loc[a, 'price'])
        pd_, pc_ = float(dp.loc[a, 'price']), float(cp.loc[a, 'price'])
        max_delta = max(max_delta, abs(pd_ - pc_))
        if wdate != TRADE_DATE:
            other_date += 1
            continue
        if wsrc == '2026-10-09.parquet':
            win_daily += 1
            other = pc_
        else:
            win_canon += 1
            other = pd_
        if abs(other - wprice) > 1e-9:
            alt += 1
    return {'tied_assets': len(tied), 'winner_in_daily_file': win_daily,
            'winner_in_canonical_prices': win_canon, 'winner_other_date': other_date,
            'alternative_differs': alt, 'max_abs_price_delta': round(max_delta, 6),
            'frames_used': len(frames)}


if __name__ == '__main__':
    which = sys.argv[1] if len(sys.argv) > 1 else 'both'
    out = {}
    if which in ('s32', 'both'):
        out['s32'] = s32()
    if which in ('s33', 'both'):
        out['s33'] = s33()
    if which == 's33asof':
        out['s33_asof_2026_10_09'] = s33_asof()
    print(json.dumps(out, indent=2, default=str))
