"""BP-c-1 probe, AMENDMENT R1.3 as corrected by order section 1.000 (2026-10-14). Read-only; ASCII only.

The served unit of every served asset is read from SERVED PAIRS (served_unit_map, pairs of asset_name,
served_price, per_unit_value):
  - served pairs: the transaction_observed rows of the SERVED canonical series for 2026-09-16..2026-10-13
    (silver/prices/canonical_prices.parquet), and, for each such (asset, date), the Buy / Sale / Dividend
    Reinvestment / Income Reinvestment rows of that asset whose trade_date is that date, read from the verified
    daily partitions (PARTITIONS2.csv; partitions dated 2026-09-16..2026-10-14 are read because clause 6 keys a
    row on its trade_date, not its file). per_unit_value = |market_value| / |units| of the trade row;
  - lot pairs: the round-2 lot extract's (current_price, |market_value| / |quantity|) as a second source.
Then R1.3 (bd_price_rule.py) runs over the real partitions for the probe dates, reading each date and the next.

Inputs: the canonical series and the asset dimension (fetched this session with `.tools/aws s3api get-object`, a READ
verb, into C:/dev/wk-bdprce-r3-20-data/; md5 checked against the object ETag), the partitions (md5 checked against
the manifest), the lot extract (sha256 checked), and the round-2 before/after list (scale_100x rows).
The only clock value is --read-at, so two runs over the same bytes are equal.

Run at this path, from the worktree root (PYTHONDONTWRITEBYTECODE=1 keeps __pycache__ out of the tree):
  python -I org/missions/D8/ADVI/ADVI_BDPRCE/deliverables/0.9.0_WK_ADVI_BDPRCE~20/rule_probe3.py \
      --canonical C:/dev/wk-bdprce-r3-20-data/canonical_prices.parquet \
      --dim C:/dev/wk-bdprce-r3-20-data/bd_assets_dim.parquet \
      --manifest org/missions/D8/ADVI/ADVI_BDPRCE/deliverables/0.9.0_WK_ADVI_BDPRCE~14/PARTITIONS2.csv \
      --silver data/black_diamond/scripts/silver \
      --lots C:/dev/wk-bdprce-r2-7-data/lot_extract.csv \
      --served org/missions/D8/ADVI/ADVI_BDPRCE/deliverables/0.9.0_WK_ADVI_BDPRCE~6/BEFORE_AFTER.csv \
      --read-at <ISO UTC> --out <path>
"""
import argparse
import csv
import hashlib
import json
import math
import os
import sys
from datetime import date as _date, timedelta

import pandas as pd

LOT_SHA256 = 'e7e618d76516c8b7977179aefb3f77ce4fc13c17fbcf1dbeb92001a6e0a2b50b'
CANON_ETAG = 'a88a7030f4506ac7e0cdb844382f9d16'   # silver/prices/canonical_prices.parquet, single part (ETag = md5)
DIM_ETAG = '45dfaab5b5756b8458c6cfae63bf9f38'     # silver/bd_assets_dim.parquet, single part (ETag = md5)
PAIR_START = _date(2026, 9, 16)
PAIR_END = _date(2026, 10, 13)
PAIR_READ_END = _date(2026, 10, 14)               # the partition after the window end (clause 6: trade_date decides)
# The probe dates: the four named in the order, plus 2026-09-16, the date of five of the eight round-2 rows.
TARGETS = ['2025-05-28', '2026-09-16', '2026-09-22', '2026-10-02', '2026-10-09']
NAMED = [
    ('MORGAN STANLEY FIN LLC 0% 05/03/2029', '2025-05-28'),
    ('BLACKROCK INC COM', '2026-09-22'),
    ('MIAMI-DADE CNTY FLA EDL FACS A 5.25% 04/01/2031', '2026-10-09'),
    ('ALLSPRING CORE BOND CIT CLASS E2', '2026-10-02'),
]
COLS = ['transaction_id', 'transaction_type', 'price', 'trade_date', 'asset_name', 'units', 'market_value']
CANON_COLS = ['date', 'asset_name', 'price', 'source']
DIM_CLASS = 'asset_super_class_bd'  # the dimension's own class column (BD dimension schema, read as data)
FI_CLASS = 'Fixed Income'
COUPON = 'coupon_rate'
DIM_COLS = ['asset_name', DIM_CLASS, COUPON]
LOT_COLS = ['asset_name', 'current_price', 'quantity', 'market_value']
CALLS = [
    'aws s3api head-object --bucket opal-data-bd --key silver/prices/canonical_prices.parquet (ETag a88a7030f4506ac7e0cdb844382f9d16)',
    'aws s3api get-object --bucket opal-data-bd --key silver/prices/canonical_prices.parquet (to C:/dev/wk-bdprce-r3-20-data/)',
    'aws s3api head-object --bucket opal-data-bd --key silver/bd_assets_dim.parquet (ETag 45dfaab5b5756b8458c6cfae63bf9f38)',
    'aws s3api get-object --bucket opal-data-bd --key silver/bd_assets_dim.parquet (to C:/dev/wk-bdprce-r3-20-data/)',
    'aws s3api get-object --bucket opal-data-bd --key silver/transactions/<date>.parquet: NOT fetched in this run; the verified local copy named by PARTITIONS2.csv is read after its md5 is checked against the manifest',
]


class Blocked(Exception):
    pass


def _md5(path):
    with open(path, 'rb') as fh:
        return hashlib.md5(fh.read()).hexdigest()


def _sha256(path):
    with open(path, 'rb') as fh:
        return hashlib.sha256(fh.read()).hexdigest()


def _num(x):
    if x is None:
        return None
    try:
        v = float(x)
    except (TypeError, ValueError):
        return None
    return v if math.isfinite(v) else None


def _per_unit(units, market_value):
    """|market_value| / |units|, computed here independently of the module; None when either is unusable or zero."""
    u = _num(units)
    m = _num(market_value)
    if u is None or m is None or u == 0 or m == 0:
        return None
    return abs(m) / abs(u)


def _ratio_of(price, units, mv):
    p = _num(price)
    pu = _per_unit(units, mv)
    if p is None or pu is None or p <= 0:
        return None
    return p / pu


def _ratio_key(v):
    return (v is None, 0.0 if v is None else v)


def _near(a, b, rel):
    return a is not None and b is not None and abs(a - b) <= rel * max(1.0, abs(b))


def _unit_changed(price, served):
    """True when price reads 100x or 1/100 of the extract's served current price, within 1 percent."""
    if price is None or served is None or served <= 0:
        return False
    return (abs(price - 100.0 * served) <= 0.01 * 100.0 * served) or (abs(price - served / 100.0) <= 0.01 * served / 100.0)


def _daterange(start, end):
    d = start
    while d <= end:
        yield d
        d = d + timedelta(days=1)


def load_manifest(path):
    """PARTITIONS2.csv: {date iso: (source_path, local_md5, verdict)}; the verified local copies."""
    out = {}
    with open(path, newline='', encoding='utf-8') as fh:
        for r in csv.DictReader(fh):
            if r.get('key', '').startswith('silver/transactions/'):
                out[r['date']] = (r['source_path'], r['local_md5'], r['verdict'])
    return out


def checked_partition(manifest, day, cache):
    """The verified local copy of one day's partition; its md5 must equal the manifest's local_md5."""
    key = day.isoformat()
    if key not in manifest:
        raise Blocked('no manifest row for partition %s' % key)
    path, want, verdict = manifest[key]
    if verdict not in ('VERIFIED_MD5', 'VERIFIED_SIZE_MULTIPART'):
        raise Blocked('partition %s is not verified: %s' % (key, verdict))
    if key not in cache:
        got = _md5(path)
        if got != want:
            raise Blocked('partition %s md5 %s != manifest %s' % (key, got, want))
        cache[key] = (path, got)
    return cache[key]


def served_series(canon_path):
    """The served canonical series over the window: transaction_observed rows only.

    Returns (served_price {(date, asset): price}, served_assets frozenset, observed_rows int).
    """
    canon = pd.read_parquet(canon_path, columns=CANON_COLS)
    ts = pd.to_datetime(canon['date'], errors='coerce')
    keep = (ts >= pd.Timestamp(PAIR_START)) & (ts <= pd.Timestamp(PAIR_END)) & (canon['source'] == 'transaction_observed')
    obs = canon.loc[keep].assign(tdate=ts[keep].dt.date)
    if obs.duplicated(['tdate', 'asset_name']).any():
        raise Blocked('duplicate transaction_observed asset-date in the served window')
    served_price = {(d, str(a)): float(p) for d, a, p in zip(obs['tdate'], obs['asset_name'], obs['price'])}
    return served_price, frozenset(str(a) for a in obs['asset_name']), int(len(obs))


def trade_pairs(manifest, cache, served_price, served_assets, R):
    """Same-date trade rows of each served (asset, date), from the verified partitions. One pair per distinct
    transaction_id (first row in read order); a row with no id is its own trade. Returns (pairs, stats)."""
    pairs = []
    seen = set()
    stats = {'partitions_read': 0, 'rows_scanned': 0, 'trade_rows_on_served_asset_dates': 0,
             'trade_rows_without_usable_per_unit': 0, 'duplicate_ids_dropped': 0}
    for day in _daterange(PAIR_START, PAIR_READ_END):
        path, _md5v = checked_partition(manifest, day, cache)
        t = pd.read_parquet(path, columns=COLS)
        stats['partitions_read'] += 1
        stats['rows_scanned'] += int(len(t))
        tdt = pd.to_datetime(t['trade_date'], errors='coerce')
        sub = t.assign(tdate=tdt.dt.date)
        in_window = (tdt >= pd.Timestamp(PAIR_START)) & (tdt <= pd.Timestamp(PAIR_END))
        on_served = sub['asset_name'].astype(str).isin(sorted(served_assets)) & sub['transaction_type'].isin(list(R.TRADE_TYPES_A))
        sub = sub.loc[in_window & on_served]
        for idx, row in zip(sub.index, sub.itertuples(index=False)):
            key = (row.tdate, str(row.asset_name))
            if key not in served_price:
                continue
            stats['trade_rows_on_served_asset_dates'] += 1
            pu = _per_unit(row.units, row.market_value)
            if pu is None:
                stats['trade_rows_without_usable_per_unit'] += 1
                continue
            tid = row.transaction_id
            tid = ('row:%s:%d' % (day.isoformat(), idx)) if (tid is None or (not isinstance(tid, str) and pd.isna(tid))) else str(tid)
            dup_key = (tid, key[1], key[0])
            if dup_key in seen:
                stats['duplicate_ids_dropped'] += 1
                continue
            seen.add(dup_key)
            pairs.append((key[1], served_price[key], pu))
    return pairs, stats


def lot_pairs(lots, served_assets):
    """The lot extract's (current_price, |market_value| / |quantity|) pairs for the served assets."""
    out = []
    counts = {'lots_read': int(len(lots)), 'lots_on_served_assets': 0, 'lots_without_usable_pair': 0}
    for name, price, qty, mv in zip(lots['asset_name'], lots['current_price'], lots['quantity'], lots['market_value']):
        if not isinstance(name, str) or name not in served_assets:
            continue
        counts['lots_on_served_assets'] += 1
        p = _num(price)
        pu = _per_unit(qty, mv)
        if p is None or p <= 0 or pu is None:
            counts['lots_without_usable_pair'] += 1
            continue
        out.append((name, p, pu))
    return out, counts


def build(args, R, manifest):
    cache = {}
    # ---- the asset dimension (md5 checked against its ETag) ----
    dim_md5 = _md5(args.dim)
    if dim_md5 != DIM_ETAG:
        raise Blocked('dimension md5 %s != ETag %s' % (dim_md5, DIM_ETAG))
    dim = pd.read_parquet(args.dim, columns=DIM_COLS)
    cands, conflicting = R.par_quoted_candidates(dim, DIM_CLASS, FI_CLASS)
    coup = R.coupon_corroboration(dim, COUPON, cands)
    fi_rows_in_dim = int((dim[DIM_CLASS] == FI_CLASS).sum())

    # ---- the served series and the served unit of every served asset (AMENDMENT R1.3 clause 1, section 1.000) ----
    served_price, served_assets, observed_rows = served_series(args.canonical)
    tpairs, tstats = trade_pairs(manifest, cache, served_price, served_assets, R)
    lots = pd.read_csv(args.lots, usecols=LOT_COLS)
    lpairs, lstats = lot_pairs(lots, served_assets)
    rows = [(a, p, u) for a, p, u in tpairs] + [(a, p, u) for a, p, u in lpairs]
    rows += [(a, None, None) for a in sorted(served_assets)]  # every served asset is present; no pair -> unreadable
    pair_frame = pd.DataFrame(rows, columns=['asset_name', 'served_price', 'per_unit_value'])
    unit_map = R.served_unit_map(pair_frame)
    served_units = {name: unit for name, (unit, _ratio) in unit_map.items()}
    units_count = {'assets': len(served_units),
                   'per100': sum(1 for u in served_units.values() if u == 'per100'),
                   'per_unit': sum(1 for u in served_units.values() if u == 'per_unit'),
                   'unreadable': sum(1 for u in served_units.values() if u == 'unreadable')}
    assets_with_trade_pair = len({a for a, _p, _u in tpairs})
    assets_with_lot_pair = len({a for a, _p, _u in lpairs})

    # The lot extract's served current price (median per asset): the reference for unit_changed (as round 3 built it).
    lot_price = lots.groupby('asset_name')['current_price'].median().to_dict()
    lot_skips = {
        'lots': int(len(lots)),
        'zero_or_missing_qty_or_mv': int(((lots['quantity'].fillna(0) == 0) | lots['quantity'].isna()
                                          | (lots['market_value'].fillna(0) == 0) | lots['market_value'].isna()).sum()),
        'missing_or_non_positive_price': int((lots['current_price'].isna() | (lots['current_price'] <= 0)).sum()),
    }

    # ---- the round-2 scale_100x rows and their round-2 values (read-only, committed record) ----
    served = []
    round2 = {}
    with open(args.served, newline='', encoding='utf-8') as fh:
        for r in csv.DictReader(fh):
            round2.setdefault((r['date'], r['asset_name']), r)
            if 'scale_100x' in r['flags']:
                served.append(r)

    # ---- the probe partitions: each target date and the next (verified copies) ----
    dates_read = sorted(set(d for t in TARGETS for d in (_date.fromisoformat(t), _date.fromisoformat(t) + timedelta(days=1))))
    sources = {'canonical_prices.parquet md5': _md5(args.canonical), 'bd_assets_dim.parquet md5': dim_md5,
               'lot_extract.csv sha256': _sha256(args.lots)}
    frames = []
    for d in dates_read:
        path, md5v = checked_partition(manifest, d, cache)
        sources['silver/transactions/%s.parquet md5' % d.isoformat()] = md5v
        frames.append(pd.read_parquet(path, columns=COLS))
    union = pd.concat(frames, ignore_index=True)

    res = {}
    wh = {}
    census = {}
    for t in TARGETS:
        res[t] = R.price_for_date(union, t, R.TRADE_TYPES_A, cands, served_units=served_units)
        wh[t] = R.withheld_for_date(union, t, R.TRADE_TYPES_A, cands, served_units=served_units)
        census[t] = R.exclusion_census(union, t, R.TRADE_TYPES_A, cands, served_units=served_units)

    # Types seen: every raw row whose trade_date is a target date (both partitions of each target read).
    tdates = pd.to_datetime(union['trade_date'], errors='coerce').dt.date.astype(object)
    on_target = union[tdates.isin([_date.fromisoformat(t) for t in TARGETS])]
    types = {}
    for v in on_target['transaction_type']:
        k = v if isinstance(v, str) else 'null'
        types[k] = types.get(k, 0) + 1
    types_seen = {k: types[k] for k in sorted(types)}

    def carry(asset, target):
        rows_a = union[(union['asset_name'] == asset)]
        dts = pd.to_datetime(rows_a['trade_date'], errors='coerce').dt.date
        prior = sorted(set(d for d, ty in zip(dts, rows_a['transaction_type'])
                           if d is not None and d < _date.fromisoformat(target)
                           and isinstance(ty, str) and ty in R.TRADE_TYPES_A))
        for d in reversed(prior):
            p = R.price_for_date(union, d.isoformat(), R.TRADE_TYPES_A, cands, served_units=served_units).get(asset)
            if p is not None:
                return R.carry_forward((p['price'], d.isoformat()))
        return None

    def row_ratios(asset, target):
        rows_a = union[(union['asset_name'] == asset)]
        dts = pd.to_datetime(rows_a['trade_date'], errors='coerce').dt.date
        out = []
        for d, ty, p, u, m in zip(dts, rows_a['transaction_type'], rows_a['price'], rows_a['units'], rows_a['market_value']):
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
    unit_changed = 0
    for asset, t in keys:
        if t not in TARGETS:
            raise Blocked('asset date outside the probe dates: %s %s' % (asset, t))
        trade = res[t].get(asset)
        w = wh[t].get(asset)
        carried = None if trade is not None or w is not None else carry(asset, t)
        if trade is not None:
            kind = 'trade'
        elif w is not None:
            kind = 'withheld'
        elif carried is not None:
            kind = 'carry'
        else:
            kind = 'absent'
        lp = lot_price.get(asset)
        lp = None if lp is None or lp != lp else float(lp)
        umap = unit_map.get(asset)
        e = {
            'asset_name': asset,
            'date': t,
            'price': None if trade is None else trade['price'],
            'kind': kind,
            'distinct_trade_ids': [] if trade is None else trade['trade_ids'],
            'served_unit': served_units.get(asset, 'unreadable'),
            'served_ratio_median': None if umap is None else umap[1],
            'canonical_served_price_on_date': served_price.get((_date.fromisoformat(t), asset)),
            'extract_current_price_median': lp,
            'fixed_income_candidate': asset in cands,
            'coupon_present': coup.get(asset) if asset in cands else None,
            'par_scaled_ids': [] if trade is None else trade['par_scaled_ids'],
            'par_as_executed_ids': [] if trade is None else trade['par_as_executed_ids'],
            'converted_ids': [] if trade is None else trade['converted_ids'],
            'per_unit_left': 0 if trade is None else trade['per_unit_left'],
            'row_ratios': row_ratios(asset, t),
        }
        if w is not None:
            e['withheld'] = w
        if carried is not None:
            e['carry_forward'] = carried
        if trade is not None or carried is not None:
            if _unit_changed(e['price'] if trade is not None else carried['price'], lp):
                unit_changed += 1
        r2 = round2.get((t, asset))
        e['round2'] = None if r2 is None else {
            'old_price': _num(r2['old_price']), 'new_price_A': _num(r2['new_price_A']),
            'new_price_B': _num(r2['new_price_B']), 'distinct_trades': r2['distinct_trades']}
        if (asset, t) in served_keys:
            served_price_r2 = _num(r2['old_price'])
            eq = trade is not None and _near(trade['price'], served_price_r2, 1e-6)
            e['served_price'] = served_price_r2
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
    withheld_ratios = []
    for t in TARGETS:
        withheld_ratios.extend(census[t]['withheld_ratios'])
    withheld_ratios.sort(key=_ratio_key)
    by_reason = {}
    for t in TARGETS:
        for k, v in census[t]['withheld_by_reason'].items():
            by_reason[k] = by_reason.get(k, 0) + v
    par = {
        'class_field': "asset_super_class_bd == 'Fixed Income' (names), then the per-row ratio test read in the asset's served unit: per100 -> as executed (ratio 100) or x100 (ratio 1), per_unit -> R1.2 (ratio 100 divided by 100, ratio 1 left alone), unreadable or absent -> withheld unit_unreadable",
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
        'par_as_executed': sum(census[t]['par_as_executed'] for t in TARGETS),
        'converted_to_per100': sum(census[t]['converted_to_per100'] for t in TARGETS),
        'unit_unreadable_rows': sum(census[t]['unit_unreadable_rows'] for t in TARGETS),
        'unit_scale_rows_unchanged': unchanged,
        'unit_scale_rows_total': len(served),
    }
    return {
        'order': 'BP-c-1',
        'read_at': args.read_at,
        'claim': 'measured',
        'calls': list(CALLS),
        'amendment': R.AMENDMENT,
        'deterministic': None,
        'reinvestment_in': ('Dividend Reinvestment' in R.TRADE_TYPES_A and 'Income Reinvestment' in R.TRADE_TYPES_A),
        'transfer_in_out': ('Transfer In' not in R.TRADE_TYPES_A),
        'extract_sha256': sources['lot_extract.csv sha256'],
        'units_source': ('two sources, one median per asset (served_unit_map, section 1.000): (1) the served canonical series '
                         'silver/prices/canonical_prices.parquet (md5 %s), its source transaction_observed rows for '
                         '2026-09-16..2026-10-13 (%d rows, %d assets), each paired with the same-date Buy, Sale, Dividend '
                         'Reinvestment and Income Reinvestment rows of that asset (per_unit_value = |market_value| / |units|, '
                         'read from the verified daily partitions, trade_date keyed); (2) the lot extract lots (current_price, '
                         '|market_value| / |quantity|) of the served assets. Bands: 10 percent of 100 -> per100, 10 percent of 1 -> per_unit.'
                         % (sources['canonical_prices.parquet md5'], observed_rows, len(served_assets))),
        'served_units': units_count,
        'served_pairs': {'trade_pairs': len(tpairs), 'lot_pairs': len(lpairs),
                         'assets_with_trade_pair': assets_with_trade_pair, 'assets_with_lot_pair': assets_with_lot_pair,
                         'assets_with_no_pair': units_count['assets'] - len(
                             {a for a, _p, _u in tpairs} | {a for a, _p, _u in lpairs}),
                         'trade_scan': tstats, 'lot_scan': lstats},
        'lot_skips': lot_skips,
        'unit_changed_assets': unit_changed,
        'par_quoted': par,
        'types_seen': types_seen,
        'census': {t: census[t] for t in TARGETS},
        'sources': sources,
        'assets': entries,
    }


def run_once(args, R):
    manifest = load_manifest(args.manifest)
    return build(args, R, manifest)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--canonical', required=True)
    ap.add_argument('--dim', required=True)
    ap.add_argument('--manifest', required=True)
    ap.add_argument('--silver', required=True)
    ap.add_argument('--lots', required=True)
    ap.add_argument('--served', required=True)
    ap.add_argument('--read-at', required=True)
    ap.add_argument('--out', required=True)
    args = ap.parse_args()
    canon_md5 = _md5(args.canonical)
    if canon_md5 != CANON_ETAG:
        print('PROBE3 BLOCKED canonical md5 %s != ETag %s' % (canon_md5, CANON_ETAG))
        return 1
    got = _sha256(args.lots)
    if got != LOT_SHA256:
        print('PROBE3 BLOCKED lot extract sha256 %s != %s' % (got, LOT_SHA256))
        return 1
    sys.path.insert(0, os.path.abspath(args.silver))
    import bd_price_rule as R  # noqa: E402
    if R.AMENDMENT != 'R1.3':
        print('PROBE3 BLOCKED module amendment %s' % R.AMENDMENT)
        return 1
    try:
        first = json.dumps(run_once(args, R), indent=1, sort_keys=True)
        second = json.dumps(run_once(args, R), indent=1, sort_keys=True)
    except Blocked as exc:
        print('PROBE3 BLOCKED %s' % exc)
        return 1
    rec = json.loads(first)
    rec['deterministic'] = bool(first == second)
    rec['determinism_md5'] = {'run1': hashlib.md5(first.encode('ascii')).hexdigest(),
                              'run2': hashlib.md5(second.encode('ascii')).hexdigest()}
    text = json.dumps(rec, indent=1, sort_keys=True) + '\n'
    with open(args.out, 'w', encoding='ascii', newline='\n') as fh:
        fh.write(text)
    print('PROBE3 wrote %s deterministic=%s assets=%d served=%s'
          % (args.out, rec['deterministic'], len(rec['assets']), json.dumps(rec['served_units'], sort_keys=True)))
    return 0


if __name__ == '__main__':
    sys.exit(main())
