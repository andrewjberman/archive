#!/usr/bin/env python3
"""BP-b-2 -- carry-forward lookback for the residual assets, READ-ONLY.

The replay's read window starts 2026-01-01. An asset with no R1 trade inside that history cannot be
carried forward from it. This scan walks silver/transactions partitions backwards from 2025-12-31 and
records, for each residual asset, the most recent R1 trade under variant A and under variant B
(clause 5: a carry-forward carries its observation date). Partitions are fetched with
`aws s3api get-object` (a read verb) into <data>/tx_back/ (before 2026-01-01) or <data>/tx/.
Trade-date keying as in the replay: a trade dated t is taken from partition t or t+1.

Run: python lookback_scan.py --root <worktree> --data <data dir> --residual <csv> --out <csv> --floor 2020-03-06
"""
import argparse
import csv
import datetime as dt
import os
import subprocess
import sys

import pandas as pd
import pyarrow.parquet as pq

COLS = ['transaction_id', 'transaction_type', 'price', 'trade_date', 'asset_name']
AWS_SHIM = '.tools/aws'


def fetch(root, data, day, log):
    """Return the local path of partition `day`, or None when S3 has no such key (read verb only)."""
    d = day.isoformat()
    local_dir = os.path.join(data, 'tx_back' if day < dt.date(2026, 1, 1) else 'tx')
    local = os.path.join(local_dir, d + '.parquet')
    if os.path.exists(local):
        return local
    os.makedirs(local_dir, exist_ok=True)
    cmd = ['bash', os.path.join(root, AWS_SHIM), 's3api', 'get-object', '--bucket', 'opal-data-bd',
           '--key', 'silver/transactions/%s.parquet' % d, local, '--query', 'ContentLength']
    rc, err = 1, ''
    for attempt in range(3):
        try:
            res = subprocess.run(cmd, capture_output=True, text=True, timeout=180)
            rc, err = res.returncode, (res.stderr or '')
        except subprocess.TimeoutExpired:
            rc, err = 124, 'timeout'
        if rc == 0:
            break
        if 'NoSuchKey' in err:
            log.write('%s NO_PARTITION\n' % d)
            log.flush()
            return None
        log.write('%s RETRY %d rc=%s %s\n' % (d, attempt + 1, rc, err[:120].replace('\n', ' ')))
        log.flush()
    if rc != 0:
        raise RuntimeError('get-object failed for %s after 3 attempts rc=%s' % (d, rc))
    log.write('%s FETCHED\n' % d)
    log.flush()
    return local


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--root', required=True)
    ap.add_argument('--data', required=True)
    ap.add_argument('--residual', required=True)
    ap.add_argument('--out', required=True)
    ap.add_argument('--floor', default='2020-03-06')
    a = ap.parse_args()
    sys.path.insert(0, os.path.join(a.root, 'data', 'black_diamond', 'scripts', 'silver'))
    import bd_price_rule as mod  # read, not changed

    with open(a.residual, encoding='utf-8') as fh:
        names = {r['asset_name'] for r in csv.DictReader(fh)}
    pending = {'A': set(names), 'B': set(names)}
    found = {'A': {}, 'B': {}}
    floor = dt.date.fromisoformat(a.floor)
    day = dt.date(2025, 12, 31)
    scanned = 0
    cache = {}
    logp = os.path.join(a.data, 'lookback_fetch.log')
    with open(logp, 'a', encoding='utf-8') as log:
        while day >= floor and (pending['A'] or pending['B']):
            parts = []
            for t in (day, day + dt.timedelta(days=1)):
                if t not in cache:
                    p = fetch(a.root, a.data, t, log)
                    if p is None:
                        cache[t] = None
                    else:
                        tab = pq.read_table(p, columns=COLS).to_pandas()
                        tab['tdate'] = pd.to_datetime(tab['trade_date'], errors='coerce').dt.date
                        cache[t] = tab
                if cache[t] is not None:
                    parts.append(cache[t])
            scanned += 1
            for old in [k for k in cache if k > day + dt.timedelta(days=1)]:
                del cache[old]
            if parts:
                frame = pd.concat(parts, ignore_index=True)
                frame = frame[frame['tdate'] == day]
                if len(frame):
                    for var, types in (('A', mod.TRADE_TYPES_A), ('B', mod.TRADE_TYPES_B)):
                        if not pending[var]:
                            continue
                        res = mod.price_for_date(frame[COLS], day, types)
                        for asset in list(pending[var]):
                            hit = res.get(asset)
                            if hit is not None:
                                found[var][asset] = (day.isoformat(), hit['price'], len(hit['trade_ids']))
                                pending[var].discard(asset)
            day -= dt.timedelta(days=1)

    with open(a.out, 'w', encoding='utf-8', newline='') as fh:
        w = csv.writer(fh, lineterminator='\n')
        w.writerow(['asset_name', 'A_observed_date', 'A_price', 'A_distinct_trades',
                    'B_observed_date', 'B_price', 'B_distinct_trades'])
        for asset in sorted(names):
            fa = found['A'].get(asset)
            fb = found['B'].get(asset)
            w.writerow([asset,
                        fa[0] if fa else '', repr(float(fa[1])) if fa else '', fa[2] if fa else '',
                        fb[0] if fb else '', repr(float(fb[1])) if fb else '', fb[2] if fb else ''])
    print('LOOKBACK residual=%d A_resolved=%d B_resolved=%d days_scanned=%d floor=%s last_day=%s'
          % (len(names), len(found['A']), len(found['B']), scanned, a.floor, day.isoformat()))
    return 0


if __name__ == '__main__':
    sys.exit(main())
