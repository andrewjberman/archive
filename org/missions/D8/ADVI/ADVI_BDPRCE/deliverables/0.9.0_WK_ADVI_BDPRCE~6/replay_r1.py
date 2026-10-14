#!/usr/bin/env python3
"""BP-b-2 -- R1 replayed over the served transaction_observed rows. READ-ONLY.

Inputs are LOCAL copies fetched by the worker with read verbs only (`aws s3api get-object`):
  <data>/canonical_prices.parquet   s3://opal-data-bd/silver/prices/canonical_prices.parquet
  <data>/tx/<YYYY-MM-DD>.parquet    s3://opal-data-bd/silver/transactions/<date>.parquet, 2026-08-20..2026-10-13
The module under replay is read, not changed: data/black_diamond/scripts/silver/bd_price_rule.py.
Outputs in --out: BEFORE_AFTER.csv (one line per served row), ESTIMATED_ROWS.csv, REPLAY.json.
Nothing is written to S3 or to any product file. ASCII only.

Run:  python replay_r1.py --root <worktree> --data <data dir> --out <deliverable dir>
"""
import argparse
import csv
import datetime as dt
import glob
import hashlib
import io
import json
import os
import statistics
import sys

import pandas as pd
import pyarrow.parquet as pq

COLS = ['transaction_id', 'transaction_type', 'price', 'trade_date', 'asset_name']
TOL = 1e-6
WIN_START = dt.date(2026, 9, 16)
WIN_END = dt.date(2026, 10, 13)
READ_START = dt.date(2026, 8, 20)
CLASSES = ['UNCHANGED', 'CHANGED', 'NOW_CARRY_FORWARD', 'NOT_RECOMPUTABLE']
LIST_COLS = ['date', 'asset_name', 'old_price', 'old_source', 'new_price_A', 'new_price_B', 'class',
             'distinct_trades', 'excluded_by_type', 'flags', 'observation_date',
             'new_price_B_observation_date', 'old_price_types', 'round1_class', 'round1_recomputed',
             'file_day_price_A', 'keying_differs']
EST_COLS = ['date', 'asset_name', 'canonical_price', 'canonical_source', 'r1_A_price', 'r1_A_basis',
            'r1_A_observation_date', 'r1_B_price', 'r1_B_basis', 'r1_B_observation_date', 'estimated_row']
ROUND1_CSV = 'org/missions/D8/ADVI/ADVI_BDPRCE/deliverables/0.9.0_WK_ADVI_BDPRCE~3/GAP_ROWS.csv'


def close(x, served):
    """R1 price equals the served price within 1e-6 * max(1, |served|)."""
    return x is not None and abs(x - served) <= TOL * max(1.0, abs(served))


def fmt(x):
    return '' if x is None else repr(float(x))


def load_module(root):
    sys.path.insert(0, os.path.join(root, 'data', 'black_diamond', 'scripts', 'silver'))
    import bd_price_rule  # noqa: E402  (read, not changed)
    return bd_price_rule


def load_canonical(data):
    df = pd.read_parquet(os.path.join(data, 'canonical_prices.parquet'))
    df = df[(df['date'] >= pd.Timestamp(WIN_START)) & (df['date'] <= pd.Timestamp(WIN_END))].copy()
    df['d'] = df['date'].dt.date
    return df


def load_tx(data):
    parts = []
    for path in sorted(glob.glob(os.path.join(data, 'tx', '*.parquet'))):
        fday = dt.date.fromisoformat(os.path.basename(path)[:10])
        t = pq.read_table(path, columns=COLS).to_pandas()
        t['file_day'] = fday
        parts.append(t)
    df = pd.concat(parts, ignore_index=True)
    df['tdt'] = pd.to_datetime(df['trade_date'], errors='coerce')
    df['tdate'] = df['tdt'].dt.date
    return df


def by_tdate(df):
    out = {}
    for d, g in df.dropna(subset=['tdate']).groupby('tdate', sort=True):
        out[d] = g
    return out


def weekdays(a, b):
    n, d = 0, a
    while d <= b:
        n += 1 if d.weekday() < 5 else 0
        d += dt.timedelta(days=1)
    return n


def build(mod, data, round1, lookback):
    canon = load_canonical(data)
    served = canon[canon['source'] == 'transaction_observed'].copy().sort_values(['d', 'asset_name'])
    served_rows = len(served)
    served_keys = set(zip(served['d'], served['asset_name']))
    assert len(served_keys) == served_rows, 'duplicate served asset-date'

    tx = load_tx(data)
    groups = by_tdate(tx)
    fd_groups = {d: g[g['file_day'] == d] for d, g in groups.items()}
    A, B = mod.TRADE_TYPES_A, mod.TRADE_TYPES_B
    resA = {d: mod.price_for_date(g[COLS], d, A) for d, g in groups.items()}
    resB = {d: mod.price_for_date(g[COLS], d, B) for d, g in groups.items()}
    resA_fd = {d: mod.price_for_date(g[COLS], d, A) for d, g in fd_groups.items()}
    tdates = sorted(groups)

    # Seam: rows whose trade_date sits in a partition other than the trade date's own file.
    in_win = (tx['tdt'] >= pd.Timestamp(WIN_START)) & (tx['tdt'] <= pd.Timestamp(WIN_END))
    seam_rows = int(((tx['tdate'] != tx['file_day']) & in_win).sum())

    def last_obs(res, asset, d):
        # Latest R1 trade strictly before d: from the loaded partitions (trade_date keyed), and from the
        # lookback scan (lookback_scan.py) for residual assets. The later observation date wins.
        cand = None
        for e in reversed([x for x in tdates if x < d]):
            hit = res.get(e, {}).get(asset)
            if hit is not None:
                cand = (e, hit['price'])
                break
        var = 'A' if res is resA else 'B'
        lb = lookback.get(asset, {}).get(var)
        if lb is not None and (cand is None or lb[0] > cand[0]):
            cand = (lb[0], lb[1])
        if cand is None:
            return None
        return mod.carry_forward((cand[1], cand[0]))

    excl_cache = {}

    def day_index(d):
        if d in excl_cache:
            return excl_cache[d]
        g = groups.get(d)
        ex, by_asset = {}, {}
        if g is not None:
            recs, _ = mod._classify(g[COLS].reset_index(drop=True), d, A)
            for r in recs:
                key = r['excluded'] if r['excluded'] is not None else ('NO_PRICE' if r['no_price'] else None)
                if key is not None:
                    ex.setdefault(r['asset'], {})
                    ex[r['asset']][key] = ex[r['asset']].get(key, 0) + 1
            for asset, s in g.groupby('asset_name', sort=True):
                by_asset[asset] = s
        excl_cache[d] = (ex, by_asset)
        return excl_cache[d]

    rows, sums = [], {c: 0 for c in CLASSES}
    flags_n = {'dividend_dominated': 0, 'repeat_weighted': 0, 'estimated_row': 0, 'scale_100x': 0}
    old_types_count, nontrade_old, nontrade_old_B = {}, 0, 0
    keying_diff = 0
    b_changed = 0
    a_changed_detail = {'CHANGED': 0, 'NOW_CARRY_FORWARD': 0, 'cf_equals_served': 0}
    not_rec_no_cf = 0

    for r in served.itertuples(index=False):
        d, a, s = r.d, r.asset_name, float(r.price)
        ex, by_asset = day_index(d)
        day_rows = len(groups[d]) if d in groups else 0
        A_hit = resA.get(d, {}).get(a)
        B_hit = resB.get(d, {}).get(a)
        cfA = None if A_hit is not None else last_obs(resA, a, d)

        if day_rows == 0:
            cls = 'NOT_RECOMPUTABLE'
        elif A_hit is not None:
            cls = 'UNCHANGED' if close(A_hit['price'], s) else 'CHANGED'
        elif cfA is not None:
            cls = 'NOW_CARRY_FORWARD'
        else:
            cls = 'NOT_RECOMPUTABLE'
        sums[cls] += 1
        if cls == 'NOT_RECOMPUTABLE' and day_rows > 0 and A_hit is None:
            not_rec_no_cf += 1

        if cls == 'NOT_RECOMPUTABLE':
            new_a, obs_a = None, ''
        elif A_hit is not None:
            new_a, obs_a = A_hit['price'], d.isoformat()
        else:
            new_a, obs_a = cfA['price'], cfA['observed_date']

        if B_hit is not None:
            new_b, obs_b = B_hit['price'], d.isoformat()
        else:
            cfB = last_obs(resB, a, d) if day_rows > 0 else None
            new_b, obs_b = (cfB['price'], cfB['observed_date']) if cfB else (None, '')
        if new_b is not None and not close(new_b, s):
            b_changed += 1

        if cls == 'CHANGED':
            a_changed_detail['CHANGED'] += 1
        if cls == 'NOW_CARRY_FORWARD':
            a_changed_detail['NOW_CARRY_FORWARD'] += 1
            if close(new_a, s):
                a_changed_detail['cf_equals_served'] += 1

        dist = len(A_hit['trade_ids']) if A_hit is not None else 0
        exs = ex.get(a, {})
        ex_str = ';'.join('%s:%d' % (k, exs[k]) for k in sorted(exs))

        # old_price_types: per row-type group, the raw median of the price column over this asset-date.
        sub = by_asset.get(a)
        types_hit = []
        all_prices = []
        if sub is not None:
            pr = pd.to_numeric(sub['price'], errors='coerce')
            all_prices = [float(v) for v in pr.dropna() if v > 0]
            for t, grp in sub.groupby('transaction_type', sort=True):
                gp = pd.to_numeric(grp['price'], errors='coerce').dropna()
                gp = [float(v) for v in gp if v > 0]
                if gp and close(statistics.median(gp), s):
                    types_hit.append(str(t))
        old_types = '|'.join(types_hit) if types_hit else 'none'
        old_types_count[old_types] = old_types_count.get(old_types, 0) + 1
        if cls in ('CHANGED', 'NOW_CARRY_FORWARD'):
            if not types_hit or not any(t in A for t in types_hit):
                nontrade_old += 1
                if new_b is not None and B_hit is not None:
                    nontrade_old_B += 1

        # flags
        flags = []
        if close(1.0, s) and all_prices and close(statistics.median(all_prices), s):
            flags.append('dividend_dominated')
        if A_hit is not None and sub is not None:
            a_rawv = pd.to_numeric(sub.loc[sub['transaction_type'].isin(list(A)), 'price'], errors='coerce').dropna()
            a_raw = [float(v) for v in a_rawv if v > 0]
            if a_raw and abs(statistics.median(a_raw) - A_hit['price']) > TOL * max(1.0, abs(A_hit['price'])):
                flags.append('repeat_weighted')
        flags.append('estimated_row=0')
        # Unit scale: the executed price of a bond trade is quoted per 100 of par; a served unit price is per 1.
        if new_a is not None and s:
            ratio = new_a / s
            if abs(ratio - 100.0) <= 1e-3 * 100.0 or abs(ratio - 0.01) <= 1e-3 * 0.01:
                flags.append('scale_100x')
        for f in flags:
            if f in flags_n:
                flags_n[f] += 1

        fd_hit = resA_fd.get(d, {}).get(a)
        fd_price = fd_hit['price'] if fd_hit is not None else None
        differs = (fd_price is None) != (A_hit is None) or (
            A_hit is not None and fd_price is not None and abs(fd_price - A_hit['price']) > 0)
        keying_diff += 1 if differs else 0

        r1 = round1.get((d.isoformat(), a))
        rows.append({
            'date': d.isoformat(), 'asset_name': a, 'old_price': fmt(s), 'old_source': 'transaction_observed',
            'new_price_A': fmt(new_a), 'new_price_B': fmt(new_b), 'class': cls,
            'distinct_trades': dist, 'excluded_by_type': ex_str, 'flags': '|'.join(flags),
            'observation_date': obs_a, 'new_price_B_observation_date': obs_b,
            'old_price_types': old_types,
            'round1_class': r1[0] if r1 else 'NOT_IN_ROUND1',
            'round1_recomputed': r1[1] if r1 else '',
            'file_day_price_A': fmt(fd_price), 'keying_differs': 1 if differs else 0,
        })

    # Estimated rows: canonical linear_interpolation / carry_forward rows of assets with a served row.
    served_assets = set(served['asset_name'])
    est_src = canon[canon['source'].isin(['linear_interpolation', 'carry_forward']) &
                    canon['asset_name'].isin(served_assets)].sort_values(['d', 'asset_name'])
    est_rows = []
    for r in est_src.itertuples(index=False):
        d, a = r.d, r.asset_name
        A_hit, B_hit = resA.get(d, {}).get(a), resB.get(d, {}).get(a)
        if A_hit is not None:
            ra, ba, oa = A_hit['price'], 'trade', d.isoformat()
        else:
            cf = last_obs(resA, a, d)
            ra, ba, oa = (cf['price'], 'last_traded', cf['observed_date']) if cf else (None, 'no_earlier_trade_in_read_range', '')
        if B_hit is not None:
            rb, bb, ob = B_hit['price'], 'trade', d.isoformat()
        else:
            cf = last_obs(resB, a, d)
            rb, bb, ob = (cf['price'], 'last_traded', cf['observed_date']) if cf else (None, 'no_earlier_trade_in_read_range', '')
        est_rows.append({'date': d.isoformat(), 'asset_name': a, 'canonical_price': fmt(r.price),
                         'canonical_source': r.source, 'r1_A_price': fmt(ra), 'r1_A_basis': ba,
                         'r1_A_observation_date': oa, 'r1_B_price': fmt(rb), 'r1_B_basis': bb,
                         'r1_B_observation_date': ob, 'estimated_row': 1})

    # Past-date arm: 20 CHANGED rows; the result for date d from only trades on or before d equals the full result.
    past = []
    for row in [x for x in rows if x['class'] == 'CHANGED'][:20]:
        d = dt.date.fromisoformat(row['date'])
        a = row['asset_name']
        full = resA[d][a]
        before_frame = tx[tx['tdt'] <= pd.Timestamp(d)][COLS]
        before = mod.price_for_date(before_frame, d, A).get(a)
        day_ids = {mod._trade_id(v, i) for i, v in enumerate(groups[d]['transaction_id'])}
        past.append({'date': row['date'], 'asset_name': a,
                     'equal_on_or_before_frame': bool(before is not None and before['price'] == full['price']
                                                      and before['trade_ids'] == full['trade_ids']),
                     'trade_ids_on_date_only': bool(set(full['trade_ids']) <= day_ids)})

    def dump(rows_, cols):
        buf = io.StringIO()
        w = csv.DictWriter(buf, fieldnames=cols, lineterminator='\n')
        w.writeheader()
        for x in rows_:
            w.writerow(x)
        return buf.getvalue().encode('utf-8')

    summary = {
        'served_rows': served_rows,
        'window_weekdays': weekdays(WIN_START, WIN_END),
        'classes': sums,
        'a_changed_detail': a_changed_detail,
        'b_changed': b_changed,
        'keying_differs': keying_diff,
        'seam_rows_in_window': seam_rows,
        'flags': flags_n,
        'old_price_types_counts': old_types_count,
        'nontrade_old_source_changed_rows': nontrade_old,
        'nontrade_old_source_changed_rows_priced_by_B': nontrade_old_B,
        'not_recomputable_without_earlier_trade': not_rec_no_cf,
        'estimated_rows_listed': len(est_rows),
        'past_date_arm': {'sampled': len(past),
                          'equal': sum(1 for p in past if p['equal_on_or_before_frame']),
                          'trade_ids_on_date_only': sum(1 for p in past if p['trade_ids_on_date_only'])},
        'tx_dates_read': len(tdates),
    }
    return dump(rows, LIST_COLS), dump(est_rows, EST_COLS), summary


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--root', required=True)
    ap.add_argument('--data', required=True)
    ap.add_argument('--out', required=True)
    ap.add_argument('--lookback', default='')
    a = ap.parse_args()
    mod = load_module(a.root)

    round1 = {}
    with open(os.path.join(a.root, ROUND1_CSV), encoding='utf-8') as fh:
        for r in csv.DictReader(fh):
            round1[(r['date'], r['asset_name'])] = (r['class'], r['recomputed_price'])

    read_at = dt.datetime.now(dt.timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')
    lookback = {}
    if a.lookback:
        with open(a.lookback, encoding='utf-8') as fh:
            for r in csv.DictReader(fh):
                ent = {}
                if r['A_observed_date']:
                    ent['A'] = (dt.date.fromisoformat(r['A_observed_date']), float(r['A_price']))
                if r['B_observed_date']:
                    ent['B'] = (dt.date.fromisoformat(r['B_observed_date']), float(r['B_price']))
                lookback[r['asset_name']] = ent
    lookback_meta = {}
    if a.lookback:
        with open(a.lookback, 'rb') as fh:
            raw = fh.read()
        lookback_meta = {'file': os.path.basename(a.lookback), 'sha256': hashlib.sha256(raw).hexdigest(),
                         'assets': len(lookback), 'A_resolved': sum(1 for v in lookback.values() if 'A' in v),
                         'B_resolved': sum(1 for v in lookback.values() if 'B' in v),
                         'floor': '2020-03-06'}
    list_a, est_a, summ_a = build(mod, a.data, round1, lookback)
    list_b, est_b, summ_b = build(mod, a.data, round1, lookback)  # second in-process pass
    deterministic = (list_a == list_b) and (est_a == est_b) and (summ_a == summ_b)

    os.makedirs(a.out, exist_ok=True)
    with open(os.path.join(a.out, 'BEFORE_AFTER.csv'), 'wb') as fh:
        fh.write(list_a)
    with open(os.path.join(a.out, 'ESTIMATED_ROWS.csv'), 'wb') as fh:
        fh.write(est_a)

    c = summ_a['classes']
    assert sum(c.values()) == summ_a['served_rows'], 'class partition does not sum to served_rows'
    rec = {
        'order': 'BP-b-2',
        'read_at': read_at,
        'claim': 'measured',
        'calls': [
            'aws s3api get-object --bucket opal-data-bd --key silver/prices/canonical_prices.parquet',
            'aws s3api head-object --bucket opal-data-bd --key silver/prices/canonical_prices.parquet',
            'aws s3api list-objects-v2 --bucket opal-data-bd --prefix silver/transactions/ (1,928 keys; denominator of the key set)',
            'aws s3api get-object --bucket opal-data-bd --key silver/transactions/<date>.parquet (286 keys, 2026-01-01..2026-10-13; 50 NoSuchKey, see lookback)',
            'aws s3api get-object --bucket opal-data-bd --key silver/transactions/<date>.parquet (lookback_scan.py: 2,127 days, 2020-03-06..2025-12-31; 618 NoSuchKey)',
        ],
        'window': '2026-09-16..2026-10-13 (%d weekday dates)' % summ_a['window_weekdays'],
        'served_rows': summ_a['served_rows'],
        'classes': c,
        'variants': {
            'A_trades_only': {'changed': c['CHANGED'] + c['NOW_CARRY_FORWARD'],
                              'CHANGED': c['CHANGED'], 'NOW_CARRY_FORWARD': c['NOW_CARRY_FORWARD'],
                              'carry_forward_equals_served': summ_a['a_changed_detail']['cf_equals_served']},
            'B_plus_reinvestment': {'changed': summ_a['b_changed']},
        },
        'no_trade_policy': 'carry the last observed R1 price with its observation date; interpolation banned',
        'estimated_rows_listed': summ_a['estimated_rows_listed'],
        'dividend_dominated': summ_a['flags']['dividend_dominated'],
        'scale_100x': summ_a['flags']['scale_100x'],
        'repeat_weighted': summ_a['flags']['repeat_weighted'],
        'file_day_vs_trade_date_differs': summ_a['keying_differs'],
        'seam_rows_in_window': summ_a['seam_rows_in_window'],
        'deterministic': deterministic,
        'served_write': False,
        'list_file': 'BEFORE_AFTER.csv',
        'estimated_list_file': 'ESTIMATED_ROWS.csv',
        'old_price_types_counts': summ_a['old_price_types_counts'],
        'nontrade_old_source_changed_rows': summ_a['nontrade_old_source_changed_rows'],
        'nontrade_old_source_changed_rows_priced_by_B': summ_a['nontrade_old_source_changed_rows_priced_by_B'],
        'not_recomputable_without_earlier_trade': summ_a['not_recomputable_without_earlier_trade'],
        'past_date_arm': summ_a['past_date_arm'],
        'tx_dates_read': summ_a['tx_dates_read'],
        'BEFORE_AFTER_sha256': hashlib.sha256(list_a).hexdigest(),
        'BEFORE_AFTER_md5': hashlib.md5(list_a).hexdigest(),
        'ESTIMATED_ROWS_md5': hashlib.md5(est_a).hexdigest(),
        'lookback_source': lookback_meta,
    }
    with open(os.path.join(a.out, 'REPLAY.json'), 'w', encoding='utf-8', newline='\n') as fh:
        json.dump(rec, fh, indent=1, sort_keys=True)
        fh.write('\n')

    print('served=%d classes=%s' % (summ_a['served_rows'], json.dumps(c, sort_keys=True)))
    print('BEFORE_AFTER md5=%s rows=%d estimated=%d deterministic=%s'
          % (rec['BEFORE_AFTER_md5'], len(list_a.splitlines()) - 1, len(est_a.splitlines()) - 1,
             str(deterministic).lower()))
    return 0


if __name__ == '__main__':
    sys.exit(main())
