"""BP-c-1 probe: R1.2 (bd_price_rule AMENDMENT R1.2) run over real opal-data-bd partitions, read-only.

Reads LOCAL copies downloaded with `.tools/aws s3api get-object` (READ verb only) into C:/dev/wk-bdprce-r3-13-data/.
Writes one JSON record. The only clock value is --read-at, passed in, so two runs over the same bytes are equal.

Run (from the worktree root, at this path; PYTHONDONTWRITEBYTECODE=1 keeps __pycache__ out of the tree):
  python -I org/missions/D8/ADVI/ADVI_BDPRCE/deliverables/0.9.0_WK_ADVI_BDPRCE~13/rule_probe2.py \
      --data C:/dev/wk-bdprce-r3-13-data --silver data/black_diamond/scripts/silver \
      --served org/missions/D8/ADVI/ADVI_BDPRCE/deliverables/0.9.0_WK_ADVI_BDPRCE~6/BEFORE_AFTER.csv \
      --read-at <ISO UTC> --out <path>
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
FI_CLASS = 'Fixed Income'
COUPON = 'coupon_rate'
DIM_COLS = ['asset_name', DIM_CLASS, COUPON]


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


def _ratio_of(price, units, mv):
    """price / (|market_value| / |units|), computed here independently of the module; None when not computable."""
    p, u, m = _num(price), _num(units), _num(mv)
    if p is None or u is None or m is None or p <= 0 or u == 0 or m == 0:
        return None
    return p / (abs(m) / abs(u))


def _ratio_key(v):
    return (v is None, 0.0 if v is None else v)


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
    # AMENDMENT R1.2: the Fixed Income names from the dimension's class column; the coupon never decides.
    cands, conflicting = R.par_quoted_candidates(dim, DIM_CLASS, FI_CLASS)
    coup = R.coupon_corroboration(dim, COUPON, cands)
    fi_rows_in_dim = int((dim[DIM_CLASS] == FI_CLASS).sum())

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

    def carry(asset, target):
        rows = union[(union['asset_name'] == asset)]
        dts = pd.to_datetime(rows['trade_date'], errors='coerce').dt.date
        prior = sorted(set(d for d, ty in zip(dts, rows['transaction_type'])
                           if d is not None and d < _date.fromisoformat(target)
                           and isinstance(ty, str) and ty in R.TRADE_TYPES_A))
        for d in reversed(prior):
            p = R.price_for_date(union, d.isoformat(), R.TRADE_TYPES_A, cands).get(asset)
            if p is not None:
                return R.carry_forward((p['price'], d.isoformat()))
        return None

    def row_ratios(asset, target):
        rows = union[(union['asset_name'] == asset)]
        dts = pd.to_datetime(rows['trade_date'], errors='coerce').dt.date
        out = []
        for d, ty, p, u, m in zip(dts, rows['transaction_type'], rows['price'], rows['units'], rows['market_value']):
            if d == _date.fromisoformat(target) and isinstance(ty, str) and ty in R.TRADE_TYPES_A:
                out.append({'transaction_type': ty, 'price': _num(p), 'ratio': _ratio_of(p, u, m)})
        return out

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
            'fixed_income_candidate': asset in cands,
            'coupon_present': coup.get(asset) if asset in cands else None,
            'par_scaled_ids': [] if trade is None else trade['par_scaled_ids'],
            'per_unit_left': 0 if trade is None else trade['per_unit_left'],
            'row_ratios': row_ratios(asset, t),
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

    scaled_pairs = []
    for t in TARGETS:
        for a in res[t]:
            if res[t][a]['par_scaled_ids']:
                scaled_pairs.append({'asset_name': a, 'date': t,
                                     'scaled_ids': res[t][a]['par_scaled_ids'],
                                     'coupon_present': coup.get(a, False)})
    per_unit_names = sorted(set(a for t in TARGETS for a in res[t] if res[t][a]['per_unit_left'] and a in cands))
    withheld_ratios = []
    for t in TARGETS:
        withheld_ratios.extend(census[t]['withheld_ratios'])
    withheld_ratios.sort(key=_ratio_key)
    by_reason = {}
    for t in TARGETS:
        for k, v in census[t]['withheld_by_reason'].items():
            by_reason[k] = by_reason.get(k, 0) + v
    par = {
        'class_field': "asset_super_class_bd == 'Fixed Income' (names), then the per-row ratio test: within 1 percent of 100 scaled, within 1 percent of 1 per unit left alone, else withheld; a non-Fixed-Income row within 1 percent of 100 withheld",
        'fixed_income_assets_in_dimension': len(cands),
        'fixed_income_rows_in_dimension': fi_rows_in_dim,
        'dimension_names_conflicting_excluded': sorted(conflicting),
        'assets_scaled': len(scaled_pairs),
        'scaled_rows': sum(census[t]['scaled_rows'] for t in TARGETS),
        'scaled_asset_dates': scaled_pairs,
        'coupon_corroborated_scaled_rows': sum(1 for s in scaled_pairs if s['coupon_present']),
        'withheld_disagreement': sum(census[t]['withheld_excluded'] for t in TARGETS),
        'withheld_by_reason': {k: by_reason[k] for k in sorted(by_reason)},
        'withheld_ratios': withheld_ratios,
        'per_unit_left': sum(census[t]['per_unit_left'] for t in TARGETS),
        'per_unit_left_fixed_income_names': per_unit_names,
        'unit_scale_rows_unchanged': unchanged,
        'unit_scale_rows_total': len(served),
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
