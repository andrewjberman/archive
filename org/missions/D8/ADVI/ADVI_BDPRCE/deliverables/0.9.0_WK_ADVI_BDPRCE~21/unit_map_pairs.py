"""BP-c-2 UNIT MAP (ADVI_BDPRCE round 3, AMENDMENT R1.3, third seat ~21). Read-only; ASCII only.

The pair builder is BP-c-1's (deliverables/0.9.0_WK_ADVI_BDPRCE~20/rule_probe3.py), copied, not rewritten:
served_series, nearest_earlier_pairs, trade_pairs, lot_pairs, load_manifest, checked_partition and the constants.
What is new here (order section 1.00 item 1): the pairs are taken by PRIORITY, ONE SOURCE PER ASSET:
  (1) same_date_trade: the served row against the Buy / Sale / reinvestment trades of that asset on the same date;
  (2) nearest_earlier_trade: only for an asset with no pair from (1): the served row against the asset's most
      recent earlier trade row with a computable per-unit value;
  (3) lot_extract: only for an asset with no pair from (1) or (2): the lot pairs of the lot extract.
The module's served_unit_map(pairs) takes the median per asset over the pairs of that one source.
Writes UNIT_MAP.csv (asset_name, unit, median_ratio, pairs, source) and UNIT_MAP_SUMMARY.json into --out.

Run with python -I at this file's own path, from the worktree root (PYTHONDONTWRITEBYTECODE=1):
  python -I .../0.9.0_WK_ADVI_BDPRCE~21/unit_map_pairs.py --canonical C:/dev/wk-bdprce-r3-21-data/canonical_prices.parquet \
      --dim C:/dev/wk-bdprce-r3-21-data/bd_assets_dim.parquet --manifest .../PARTITIONS3.csv \
      --silver data/black_diamond/scripts/silver --lots C:/dev/wk-bdprce-r2-7-data/lot_extract.csv --out .../~21/
"""
import io
import argparse
import bisect
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


def nearest_earlier_pairs(manifest, cache, served_price, served_assets, R):
    """AMENDMENT R1.3 second correction (section 1.0000): for each served (asset, date), ONE pair from the asset's most
    recent EARLIER trade row -- trade_date strictly before the served date, a type in TRADE_TYPES_A, a computable
    per-unit value -- searched over EVERY verified cached partition (the manifest lists all of them: tx_back and tx,
    each md5-checked before it is read). Clause 6: trade_date keys a row, never its file. Ties on the latest earlier
    trade date take the first row in partition-date order, then file order (deterministic). The same-date trades are
    a separate source (trade_pairs); a served date with no earlier cached trade gets no pair from this source.
    Returns (pairs, stats)."""
    end = pd.Timestamp(PAIR_END)
    per_asset = {}  # asset -> list of (trade_date, seq, per_unit_value)
    seq = 0
    stats = {'partitions_read': 0, 'rows_scanned': 0, 'earlier_trade_rows_on_served_assets': 0,
             'rows_without_usable_per_unit': 0}
    for key in sorted(manifest):
        day = _date.fromisoformat(key)
        path, _md5v = checked_partition(manifest, day, cache)
        t = pd.read_parquet(path, columns=COLS)
        stats['partitions_read'] += 1
        stats['rows_scanned'] += int(len(t))
        tdt = pd.to_datetime(t['trade_date'], errors='coerce')
        on_served = t['asset_name'].astype(str).isin(sorted(served_assets)) & t['transaction_type'].isin(list(R.TRADE_TYPES_A))
        sub = t.loc[on_served & (tdt < end)]
        for tdate, name, units, mv in zip(tdt[sub.index], sub['asset_name'], sub['units'], sub['market_value']):
            if pd.isna(tdate):
                continue
            stats['earlier_trade_rows_on_served_assets'] += 1
            pu = _per_unit(units, mv)
            if pu is None:
                stats['rows_without_usable_per_unit'] += 1
                continue
            per_asset.setdefault(str(name), []).append((tdate.date(), seq, pu))
            seq += 1
    for name in per_asset:
        per_asset[name].sort(key=lambda e: (e[0], e[1]))
    pairs = []
    for (d, asset), served in sorted(served_price.items(), key=lambda kv: (kv[0][0], kv[0][1])):
        entries = per_asset.get(asset)
        if not entries:
            continue
        keys = [(e[0],) for e in entries]
        pos = bisect.bisect_left(keys, (d,)) - 1  # last entry with trade_date < d
        if pos < 0:
            continue
        latest = entries[pos][0]
        first = bisect.bisect_left(keys, (latest,))  # first row of the latest earlier trade date
        pairs.append((asset, served, entries[first][2]))
    stats['assets_with_earlier_trade_in_cache'] = len({a for a, _p, _u in pairs})
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




def _cli_md5(path):
    return _md5(path)


def priority_pairs(npairs, tpairs, lpairs):
    """One source per asset, by priority (order section 1.00 item 1). Returns (chosen rows, source of each asset)."""
    order = [('same_date_trade', tpairs), ('nearest_earlier_trade', npairs), ('lot_extract', lpairs)]
    src_of = {}
    for src, pairs in order:
        for a, _s, _u in pairs:
            src_of.setdefault(a, src)
    chosen = [(a, s, u) for src, pairs in order for (a, s, u) in pairs if src_of[a] == src]
    return chosen, src_of


def build_map(args, R, manifest):
    cache = {}
    canon_md5 = _md5(args.canonical)
    if canon_md5 != CANON_ETAG:
        raise Blocked('canonical md5 %s != ETag %s' % (canon_md5, CANON_ETAG))
    dim_md5 = _md5(args.dim)
    if dim_md5 != DIM_ETAG:
        raise Blocked('dimension md5 %s != ETag %s' % (dim_md5, DIM_ETAG))
    lot_sha = _sha256(args.lots)
    if lot_sha != LOT_SHA256:
        raise Blocked('lot extract sha256 %s != %s' % (lot_sha, LOT_SHA256))
    served_price, served_assets, observed_rows = served_series(args.canonical)
    npairs, nstats = nearest_earlier_pairs(manifest, cache, served_price, served_assets, R)
    tpairs, tstats = trade_pairs(manifest, cache, served_price, served_assets, R)
    lots = pd.read_csv(args.lots, usecols=LOT_COLS)
    lpairs, lstats = lot_pairs(lots, served_assets)
    chosen, src_of = priority_pairs(npairs, tpairs, lpairs)
    rows = list(chosen) + [(a, None, None) for a in sorted(served_assets)]  # every served asset present
    pair_frame = pd.DataFrame(rows, columns=['asset_name', 'served_price', 'per_unit_value'])
    unit_map = R.served_unit_map(pair_frame)
    used = {}
    for a, _s, _u in chosen:
        used[a] = used.get(a, 0) + 1
    table = []
    for a in sorted(unit_map):
        unit, ratio = unit_map[a]
        table.append({'asset_name': a, 'unit': unit, 'median_ratio': '' if ratio is None else repr(float(ratio)),
                      'pairs': used.get(a, 0), 'source': src_of.get(a, 'none')})
    counts = {'assets': len(table),
              'per100': sum(1 for t in table if t['unit'] == 'per100'),
              'per_unit': sum(1 for t in table if t['unit'] == 'per_unit'),
              'unreadable': sum(1 for t in table if t['unit'] == 'unreadable')}
    by_source = {'same_date_trade': 0, 'nearest_earlier_trade': 0, 'lot_extract': 0, 'none': 0}
    for t in table:
        by_source[t['source']] += 1
    unreadable_by_source = {}
    for t in table:
        if t['unit'] == 'unreadable':
            unreadable_by_source[t['source']] = unreadable_by_source.get(t['source'], 0) + 1
    summary = {
        'amendment': R.AMENDMENT,
        'served_units': counts,
        'assets_by_source': by_source,
        'unreadable_by_source': unreadable_by_source,
        'per100_assets': [t['asset_name'] for t in table if t['unit'] == 'per100'],
        'pairs_chosen': {'same_date_trade': sum(1 for a, _s, _u in chosen if src_of[a] == 'same_date_trade'),
                         'nearest_earlier_trade': sum(1 for a, _s, _u in chosen if src_of[a] == 'nearest_earlier_trade'),
                         'lot_extract': sum(1 for a, _s, _u in chosen if src_of[a] == 'lot_extract')},
        'pairs_available': {'nearest_earlier_trade': len(npairs), 'same_date_trade': len(tpairs), 'lot_extract': len(lpairs)},
        'served_observed_rows': observed_rows,
        'nearest_scan': nstats, 'trade_scan': tstats, 'lot_scan': lstats,
    }
    return table, summary


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--canonical', required=True)
    ap.add_argument('--dim', required=True)
    ap.add_argument('--manifest', required=True)
    ap.add_argument('--silver', required=True)
    ap.add_argument('--lots', required=True)
    ap.add_argument('--out', required=True)
    args = ap.parse_args()
    sys.path.insert(0, os.path.abspath(args.silver))
    import bd_price_rule as R  # noqa: E402  (read, not changed)
    if R.AMENDMENT != 'R1.3':
        print('UNITMAP BLOCKED module amendment %s' % R.AMENDMENT)
        return 1
    manifest = load_manifest(args.manifest)
    try:
        table, summary = build_map(args, R, manifest)
    except Blocked as exc:
        print('UNITMAP BLOCKED %s' % exc)
        return 1
    buf = io.StringIO()
    w = csv.DictWriter(buf, fieldnames=['asset_name', 'unit', 'median_ratio', 'pairs', 'source'], lineterminator='\n')
    w.writeheader()
    for t in table:
        w.writerow(t)
    data = buf.getvalue().encode('utf-8')
    with open(os.path.join(args.out, 'UNIT_MAP.csv'), 'wb') as fh:
        fh.write(data)
    summary['unit_map_sha256'] = hashlib.sha256(data).hexdigest()
    summary['unit_map_rows'] = len(table)
    with open(os.path.join(args.out, 'UNIT_MAP_SUMMARY.json'), 'w', encoding='utf-8', newline='\n') as fh:
        json.dump(summary, fh, indent=1, sort_keys=True, ensure_ascii=True)
        fh.write('\n')
    print('UNITMAP wrote %s rows=%d served_units=%s sha256=%s'
          % (os.path.join(args.out, 'UNIT_MAP.csv'), len(table), json.dumps(summary['served_units'], sort_keys=True),
             summary['unit_map_sha256']))
    print('UNITMAP by_source=%s pairs_chosen=%s' % (json.dumps(summary['assets_by_source'], sort_keys=True),
                                                    json.dumps(summary['pairs_chosen'], sort_keys=True)))
    return 0


if __name__ == '__main__':
    sys.exit(main())
