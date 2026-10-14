"""BP-c-1 probe: R1.1 (bd_price_rule AMENDMENT 1) run over real opal-data-bd partitions, read-only.

Reads LOCAL copies downloaded with `.tools/aws s3api get-object` (READ verb only) into C:/dev/wk-bdprce-r3-13-data/.
Writes one JSON record. The only clock value is --read-at, passed in, so two runs over the same bytes are equal.

Run (from the worktree root, at this path):
  python -I org/missions/D8/ADVI/ADVI_BDPRCE/deliverables/0.9.0_WK_ADVI_BDPRCE~13/rule_probe2.py \
      --data C:/dev/wk-bdprce-r3-13-data --silver data/black_diamond/scripts/silver \
      --served org/missions/D8/ADVI/ADVI_BDPRCE/deliverables/0.9.0_WK_ADVI_BDPRCE~6/BEFORE_AFTER.csv \
      --read-at 2026-10-14T01:28:00Z --out <path>
"""
import argparse
import csv
import hashlib
import json
import os
import sys
from datetime import date as _date, timedelta

import pandas as pd

TARGETS = ['2026-09-16', '2026-09-22', '2026-10-02', '2026-10-08', '2026-10-09']
NAMED = [
    ('BLACKROCK INC COM', '2026-09-22'),
    ('EXXONMOBIL HOLDINGS CORP COM SHS', '2026-10-09'),
    ('MIAMI-DADE CNTY FLA EDL FACS A 5.25% 04/01/2031', '2026-10-09'),
    ('CITIGROUP INC 5.3% 07/22/2032', '2026-09-22'),
    ('MISSOURI ST HEALTH & EDL FACS 5% 05/01/2033', '2026-10-09'),
    ('ALLSPRING CORE BOND CIT CLASS E2', '2026-10-02'),
]
COLS = ['transaction_id', 'transaction_type', 'price', 'trade_date', 'asset_name', 'units', 'market_value']
DIM_CLASS = 'asset_super_class_bd'  # the dimension's own class column (BD dimension schema, read as data)
DIM_COLS = ['asset_name', DIM_CLASS, 'coupon_rate']


def _next(d):
    return (_date.fromisoformat(d) + timedelta(days=1)).isoformat()


def _md5(path):
    with open(path, 'rb') as fh:
        return hashlib.md5(fh.read()).hexdigest()


def _num(x):
    if x is None:
        return None
    try:
        v = float(x)
    except (TypeError, ValueError):
        return None
    return None if v != v else v


def _near(a, b, rel):
    return a is not None and b is not None and abs(a - b) <= rel * max(1.0, abs(b))


def _ratio_near_100(price, units, mv):
    """True when price / (|mv| / |units|) is within 1 percent of 100 (the scale corroboration)."""
    p, u, m = _num(price), _num(units), _num(mv)
    if p is None or u is None or m is None or p <= 0 or u == 0 or m == 0:
        return False
    return abs(p / (abs(m) / abs(u)) - 100.0) <= 1.0


def build(args, R):
    dates_read = sorted(set(d for t in TARGETS for d in (t, _next(t))))
    sources = {}
    frames = []
    for d in dates_read:
        p = os.path.join(args.data, 'tx_%s.parquet' % d)
        sources['silver/transactions/%s.parquet' % d] = _md5(p)
        frames.append(pd.read_parquet(p, columns=COLS))
    union = pd.concat(frames, ignore_index=True)

    dimp = os.path.join(args.data, 'bd_assets_dim.parquet')
    sources['silver/bd_assets_dim.parquet'] = _md5(dimp)
    dim = pd.read_parquet(dimp, columns=DIM_COLS)
    cands, conflicting = R.par_quoted_candidates(dim, DIM_CLASS, 'coupon_rate', 'Fixed Income')
    qualifies = (dim['asset_super_class_bd'] == 'Fixed Income') & dim['coupon_rate'].notna()
    fi_any = set(str(n) for n in dim.loc[(dim['asset_super_class_bd'] == 'Fixed Income') & dim['asset_name'].notna(), 'asset_name'])

    # Served 100x rows and the round-2 values, from the round-2 before/after list (read-only, committed record).
    served = []
    round2 = {}
    with open(args.served, newline='', encoding='utf-8') as fh:
        for r in csv.DictReader(fh):
            round2.setdefault((r['date'], r['asset_name']), r)
            if 'scale_100x' in r['flags']:
                served.append(r)

    res = {}
    wh = {}
    census = {}
    for t in TARGETS:
        res[t] = R.price_for_date(union, t, R.TRADE_TYPES_A, cands)
        wh[t] = R.withheld_for_date(union, t, R.TRADE_TYPES_A, cands)
        census[t] = R.exclusion_census(union, t, R.TRADE_TYPES_A, cands)

    # Types seen: every raw row whose trade_date is a target date (both partitions of each target read).
    tdates = pd.to_datetime(union['trade_date'], errors='coerce').dt.date.astype(object)
    on_target = union[tdates.isin([_date.fromisoformat(t) for t in TARGETS])]
    types = {}
    for v in on_target['transaction_type']:
        k = v if isinstance(v, str) else 'null'
        types[k] = types.get(k, 0) + 1
    types_seen = {k: types[k] for k in sorted(types)}

    # Fixed-income assets the candidate rule leaves unscaled whose ratio is near 100 (reported, never scaled).
    fi_unscaled_near100 = set()
    for _, r in on_target.iterrows():
        name = r['asset_name']
        if not isinstance(name, str) or name not in fi_any or name in cands:
            continue
        if r['transaction_type'] in R.TRADE_TYPES_A and _ratio_near_100(r['price'], r['units'], r['market_value']):
            fi_unscaled_near100.add(name)

    def carry(asset, target):
        rows = union[(union['asset_name'] == asset)]
        dts = pd.to_datetime(rows['trade_date'], errors='coerce').dt.date
        prior = sorted(set(d for d, ty in zip(dts, rows['transaction_type'])
                           if d is not None and d < _date.fromisoformat(target)
                           and isinstance(ty, str) and ty in R.TRADE_TYPES_A))
        for d in reversed(prior):
            p = R.price_for_date(union, d.isoformat(), R.TRADE_TYPES_A, cands).get(asset)
            if p is not None:
                cf = R.carry_forward((p['price'], d.isoformat()))
                return cf
        return None

    # Assets: the named set plus the eight round-2 scale_100x rows (deduplicated, in order).
    keys = []
    for k in NAMED + [(r['asset_name'], r['date']) for r in served]:
        if k not in keys:
            keys.append(k)
    entries = []
    served_keys = set((r['asset_name'], r['date']) for r in served)
    unchanged = 0
    for asset, t in keys:
        if t not in TARGETS:
            raise SystemExit('asset date outside the probe dates: %s %s' % (asset, t))
        trade = res[t].get(asset)
        w = wh[t].get(asset)
        if trade is not None:
            kind = 'trade'
        elif w is not None:
            kind = 'withheld'
        else:
            kind = 'absent'
        e = {
            'asset_name': asset,
            'date': t,
            'price': None if trade is None else trade['price'],
            'kind': kind,
            'distinct_trade_ids': [] if trade is None else trade['trade_ids'],
            'par_quoted_candidate': asset in cands,
            'par_scaled_ids': [] if trade is None else trade['par_scaled_ids'],
        }
        if w is not None:
            e['withheld'] = w
        if kind == 'absent':
            e['carry_forward'] = carry(asset, t)
        r2 = round2.get((t, asset))
        e['round2'] = None if r2 is None else {
            'old_price': _num(r2['old_price']), 'new_price_A': _num(r2['new_price_A']),
            'new_price_B': _num(r2['new_price_B']), 'distinct_trades': r2['distinct_trades']}
        if (asset, t) in served_keys:
            served_price = _num(r2['old_price'])
            eq = trade is not None and _near(trade['price'], served_price, 1e-6)
            e['served_price'] = served_price
            e['equal_to_served'] = bool(eq)
            unchanged += 1 if eq else 0
        entries.append(e)

    assets_scaled = sum(1 for t in TARGETS for a in res[t] if res[t][a]['par_scaled_ids'])
    par = {
        'class_field': "asset_super_class_bd == 'Fixed Income' and coupon_rate not null",
        'candidates_in_dimension': len(cands),
        'candidate_rows_in_dimension': int(qualifies.sum()),
        'dimension_names_conflicting_excluded': sorted(conflicting),
        'assets_scaled': assets_scaled,
        'withheld_disagreement': sum(census[t]['withheld_by_reason'].get('ratio_near_1', 0) for t in TARGETS),
        'withheld_ratio_unrecognised': sum(census[t]['withheld_by_reason'].get('ratio_unrecognised', 0) for t in TARGETS),
        'unit_scale_rows_unchanged': unchanged,
        'unit_scale_rows_total': len(served),
        'fixed_income_unscaled_with_ratio_near_100': sorted(fi_unscaled_near100),
    }
    return {
        'order': 'BP-c-1',
        'read_at': args.read_at,
        'claim': 'measured',
        'calls': ['.tools/aws s3api get-object --bucket opal-data-bd --key silver/transactions/%s.parquet' % d
                  for d in dates_read] + [
                  '.tools/aws s3api get-object --bucket opal-data-bd --key silver/bd_assets_dim.parquet'],
        'amendment': R.AMENDMENT,
        'deterministic': None,
        'reinvestment_in': ('Dividend Reinvestment' in R.TRADE_TYPES_A and 'Income Reinvestment' in R.TRADE_TYPES_A),
        'transfer_in_out': ('Transfer In' not in R.TRADE_TYPES_A),
        'par_quoted': par,
        'types_seen': types_seen,
        'census': {t: census[t] for t in TARGETS},
        'sources_md5': sources,
        'assets': entries,
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--data', required=True)
    ap.add_argument('--silver', required=True)
    ap.add_argument('--served', required=True)
    ap.add_argument('--read-at', required=True)
    ap.add_argument('--out', required=True)
    args = ap.parse_args()
    sys.path.insert(0, os.path.abspath(args.silver))
    import bd_price_rule as R  # noqa: E402

    first = json.dumps(build(args, R), indent=1, sort_keys=True)
    second = json.dumps(build(args, R), indent=1, sort_keys=True)
    rec = json.loads(first)
    rec['deterministic'] = bool(first == second)
    text = json.dumps(rec, indent=1, sort_keys=True) + '\n'
    with open(args.out, 'w', encoding='utf-8', newline='\n') as fh:
        fh.write(text)
    print('PROBE2 wrote %s deterministic=%s assets=%d' % (args.out, rec['deterministic'], len(rec['assets'])))
    return 0


if __name__ == '__main__':
    sys.exit(main())
