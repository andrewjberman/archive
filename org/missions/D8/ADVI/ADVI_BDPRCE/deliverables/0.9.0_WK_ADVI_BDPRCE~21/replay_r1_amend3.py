#!/usr/bin/env python3
"""BP-c-2 round 3 (third seat ~21) -- R1 replayed on AMENDMENT R1.3 with the served-unit map. READ-ONLY.

Adapted from the second seat's replay_r1_r3.py (0.9.0_WK_ADVI_BDPRCE~14, copied and adapted, not edited there), which
was adapted from round 2's replay_r1.py. What changed from the second seat (order section 1.00):
  - the module is R1.3 and EVERY module call passes served_units (the map written by unit_map_pairs.py, UNIT_MAP.csv);
  - a served row of a Fixed Income asset whose unit is unreadable (or absent from the map) is NOT_RECOMPUTABLE with the
    reason unit_unreadable (never guessed) and is counted in unit_withheld_rows; an interpolated row of such an asset
    is unresolved with the same reason;
  - unit_changed_rows: the served rows (CHANGED or NOW_CARRY_FORWARD) whose new/old price is within 1 percent of 100
    or of 0.01; the order requires 0;
  - the served set, the partitions (PARTITIONS3.csv) and the canonical object are the ones read this session;
  - BEFORE_AFTER3.csv carries the served unit and the second seat's class and price beside round 2's.

Inputs (all read-only): --canonical, --dim, --manifest (PARTITIONS3.csv), --units (UNIT_MAP.csv), --unit-summary
(UNIT_MAP_SUMMARY.json), --round2 (round 2 BEFORE_AFTER.csv), --round1 (round 1 GAP_ROWS.csv), --seat2 (the second
seat's BEFORE_AFTER2.csv). Outputs in --out: BEFORE_AFTER3.csv, ESTIMATED_ROWS3.csv, REPLAY3.json, with a two-pass
in-process determinism check. --peer-md5 takes the BEFORE_AFTER3.csv md5 of a SEPARATE process run.

Run at this file's own path with python -I, from the worktree root. ASCII only.
"""
import argparse
import bisect
import csv
import datetime as dt
import hashlib
import io
import json
import os
import statistics
import sys

import pandas as pd
import pyarrow.parquet as pq

WIN_START = dt.date(2026, 9, 16)
WIN_END = dt.date(2026, 10, 13)
TOL = 1e-6
CLASSES = ['UNCHANGED', 'CHANGED', 'NOW_CARRY_FORWARD', 'NOT_RECOMPUTABLE']
UNITS = ('per100', 'per_unit', 'unreadable')
COLS_READ = ['transaction_id', 'transaction_type', 'price', 'trade_date', 'asset_name', 'units', 'market_value']
DIM_CLASS = 'asset_super_class_bd'
FI_CLASS = 'Fixed Income'
COUPON = 'coupon_rate'
ROUND2_LIST = 'org/missions/D8/ADVI/ADVI_BDPRCE/deliverables/0.9.0_WK_ADVI_BDPRCE~6/BEFORE_AFTER.csv'
ROUND1_LIST = 'org/missions/D8/ADVI/ADVI_BDPRCE/deliverables/0.9.0_WK_ADVI_BDPRCE~3/GAP_ROWS.csv'
LIST_COLS = ['date', 'asset_name', 'served_unit', 'old_price', 'old_source', 'new_price', 'class', 'reason',
             'distinct_trades', 'excluded_by_type', 'flags', 'observation_date', 'old_price_types', 'round2_class',
             'round2_new_price', 'seat2_class', 'seat2_new_price', 'in_round2', 'round1_class', 'round1_recomputed',
             'carry_source_par_scaled', 'unit_changed']
EST_COLS = ['date', 'asset_name', 'served_unit', 'canonical_price', 'canonical_source', 'fate', 'r1_price', 'r1_basis',
            'r1_observation_date', 'reason', 'estimated_row']


def close(x, served):
    return x is not None and abs(x - served) <= TOL * max(1.0, abs(served))


def fmt(x):
    return '' if x is None else repr(float(x))


def load_module(root):
    sys.path.insert(0, os.path.join(root, 'data', 'black_diamond', 'scripts', 'silver'))
    import bd_price_rule  # noqa: E402  (read, not changed)
    if bd_price_rule.AMENDMENT != 'R1.3':
        raise SystemExit('ERROR: module amendment is %r, expected R1.3' % bd_price_rule.AMENDMENT)
    return bd_price_rule


def read_units(path):
    """UNIT_MAP.csv: {asset_name: unit}. Every unit must be in the closed set."""
    out = {}
    with open(path, encoding='utf-8', newline='') as fh:
        for r in csv.DictReader(fh):
            if r['unit'] not in UNITS:
                raise SystemExit('ERROR: unit %r for %r is not in %s' % (r['unit'], r['asset_name'], UNITS))
            if r['asset_name'] in out:
                raise SystemExit('ERROR: duplicate asset in the unit map: %r' % r['asset_name'])
            out[r['asset_name']] = r['unit']
    return out


def read_partition(path, day, universe, stats):
    """Read the trade columns of one verified partition; keep the universe's rows and EVERY window-dated row."""
    names = pq.read_schema(path).names
    want = [c for c in COLS_READ if c in names]
    if 'units' not in names or 'market_value' not in names:
        stats['partitions_missing_units_or_mv'] += 1
    t = pq.read_table(path, columns=want).to_pandas()
    for c in COLS_READ:
        if c not in t.columns:
            t[c] = None
    tdt = pd.to_datetime(t['trade_date'], errors='coerce')
    stats['rows_total'] += len(t)
    stats['trade_date_unparsed'] += int(tdt.isna().sum())
    lag = (pd.Timestamp(day) - tdt).dt.days
    stats['late_rows_any'] += int((lag > 0).sum())
    stats['late_rows_gt1day'] += int((lag > 1).sum())
    if day.year == 2026:
        stats['late_rows_2026_partitions'] += int((lag > 0).sum())
        stats['late_rows_2026_partitions_gt1day'] += int((lag > 1).sum())
    t['tdate'] = tdt.dt.date
    t['file_day'] = day
    t = t[t['tdate'].notna()]
    tdates = set(t['tdate'].unique())
    in_window = (t['tdate'] >= WIN_START) & (t['tdate'] <= WIN_END)
    if day == dt.date(2026, 10, 14):
        stats['partition_2026_10_14_rows_dated_in_window'] = int(in_window.sum())
        stats['partition_2026_10_14_rows_dated_before_window_end'] = int((t['tdate'] <= WIN_END).sum())
    t = t[in_window | t['asset_name'].isin(universe)]
    return t, tdates


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--root', required=True)
    ap.add_argument('--canonical', required=True)
    ap.add_argument('--dim', required=True)
    ap.add_argument('--manifest', required=True)
    ap.add_argument('--units', required=True)
    ap.add_argument('--unit-summary', required=True)
    ap.add_argument('--seat2', required=True)
    ap.add_argument('--out', required=True)
    ap.add_argument('--peer-md5', default='')
    ap.add_argument('--canonical-etag', default='')
    ap.add_argument('--canonical-modified', default='')
    a = ap.parse_args()
    mod = load_module(a.root)
    rep = {}

    # ---- the served-unit map (AMENDMENT R1.3 clause 1; written by unit_map_pairs.py) ----
    units = read_units(a.units)
    with open(a.units, 'rb') as fh:
        units_sha = hashlib.sha256(fh.read()).hexdigest()
    with open(a.unit_summary, encoding='utf-8') as fh:
        unit_summary = json.load(fh)
    if unit_summary.get('unit_map_sha256') != units_sha:
        raise SystemExit('ERROR: UNIT_MAP.csv sha256 differs from UNIT_MAP_SUMMARY.json')

    # ---- the asset dimension and the par-quoted candidate set (R1.2; the coupon corroborates only) ----
    dim = pd.read_parquet(a.dim, columns=['asset_name', DIM_CLASS, COUPON])
    cands, conflicting = mod.par_quoted_candidates(dim, DIM_CLASS, FI_CLASS)
    coup = mod.coupon_corroboration(dim, COUPON, cands)
    rep['dimension'] = {'rows': int(len(dim)), 'fixed_income_rows': int((dim[DIM_CLASS] == FI_CLASS).sum()),
                        'fixed_income_names': len(cands), 'conflicting_names': sorted(conflicting),
                        'candidates_with_coupon': sum(1 for v in coup.values() if v)}

    def unit_of(asset):
        return units.get(asset, 'unreadable')

    # ---- the served set, re-read ----
    canon = pd.read_parquet(a.canonical)
    canon = canon[(canon['date'] >= pd.Timestamp(WIN_START)) & (canon['date'] <= pd.Timestamp(WIN_END))].copy()
    canon['d'] = canon['date'].dt.date
    served = canon[canon['source'] == 'transaction_observed'].sort_values(['d', 'asset_name']).copy()
    assert len(served) == len(set(zip(served['d'], served['asset_name']))), 'duplicate served asset-date'
    served_keys = list(zip(served['d'], served['asset_name']))
    served_price = {(d, a_): float(p) for d, a_, p in zip(served['d'], served['asset_name'], served['price'])}
    served_assets = set(served['asset_name'])
    weekdays = sum(1 for i in range((WIN_END - WIN_START).days + 1)
                   if (WIN_START + dt.timedelta(days=i)).weekday() < 5)
    rep['window_rows_all_sources'] = int(len(canon))
    rep['window_calendar_dates'] = int(canon['d'].nunique())
    rep['window_source_counts'] = {k: int(v) for k, v in canon['source'].value_counts().items()}
    rep['weekdays'] = weekdays
    rep['served_assets'] = len(served_assets)
    interp = canon[(canon['source'] == 'linear_interpolation')].copy()
    interp_served = interp[interp['asset_name'].isin(served_assets)].sort_values(['d', 'asset_name']).copy()
    rep['interpolated_window_all_assets'] = int(len(interp))
    rep['interpolated_window_all_assets_names'] = int(interp['asset_name'].nunique())
    rep['interpolated_rows'] = int(len(interp_served))
    rep['interpolated_assets'] = int(interp_served['asset_name'].nunique())
    unit_missing = sorted(a_ for a_ in served_assets if a_ not in units)
    rep['served_assets_absent_from_unit_map'] = unit_missing
    served_units_counts = {'assets': len(served_assets),
                           'per100': sum(1 for a_ in served_assets if unit_of(a_) == 'per100'),
                           'per_unit': sum(1 for a_ in served_assets if unit_of(a_) == 'per_unit'),
                           'unreadable': sum(1 for a_ in served_assets if unit_of(a_) == 'unreadable')}
    if served_units_counts['per100'] + served_units_counts['per_unit'] + served_units_counts['unreadable'] != \
            served_units_counts['assets']:
        raise SystemExit('ERROR: served_units classes do not sum to assets')

    # ---- round 2, the second seat and round 1 lists, read for comparison only ----
    r2 = {}
    with open(os.path.join(a.root, ROUND2_LIST), encoding='utf-8') as fh:
        for r in csv.DictReader(fh):
            r2[(r['date'], r['asset_name'])] = r
    s2 = {}
    with open(a.seat2, encoding='utf-8') as fh:
        for r in csv.DictReader(fh):
            s2[(r['date'], r['asset_name'])] = r
    r1 = {}
    with open(os.path.join(a.root, ROUND1_LIST), encoding='utf-8') as fh:
        for r in csv.DictReader(fh):
            r1[(r['date'], r['asset_name'])] = (r['class'], r['recomputed_price'])
    cur_keys = set((d.isoformat(), a_) for d, a_ in served_keys)
    rep['served_vs_round2'] = {'round2_rows': len(r2), 'current_rows': len(cur_keys),
                               'added': len(cur_keys - set(r2)), 'removed': len(set(r2) - cur_keys),
                               'common_price_differs': sum(1 for d, a_ in served_keys
                                                           if (d.isoformat(), a_) in r2 and abs(
                                                               float(r2[(d.isoformat(), a_)]['old_price']) -
                                                               served_price[(d, a_)]) > 0)}
    rep['served_vs_seat2'] = {'seat2_rows': len(s2), 'current_rows': len(cur_keys),
                              'added': sorted('%s|%s' % k for k in cur_keys - set(s2)),
                              'removed': sorted('%s|%s' % k for k in set(s2) - cur_keys),
                              'common_price_differs': sum(1 for d, a_ in served_keys
                                                          if (d.isoformat(), a_) in s2 and abs(
                                                              float(s2[(d.isoformat(), a_)]['old_price']) -
                                                              served_price[(d, a_)]) > 0)}

    # ---- every verified partition, keyed on trade_date ----
    manifest = []
    with open(a.manifest, encoding='utf-8') as fh:
        for r in csv.DictReader(fh):
            manifest.append(r)
    ok_verdicts = ('VERIFIED_MD5', 'VERIFIED_SIZE_MULTIPART')
    bad = [r['key'] for r in manifest if r['verdict'] not in ok_verdicts]
    if bad:
        raise SystemExit('ERROR: unverified partitions in manifest: %d' % len(bad))
    stats = {'rows_total': 0, 'trade_date_unparsed': 0, 'late_rows_any': 0, 'late_rows_gt1day': 0,
             'late_rows_2026_partitions': 0, 'late_rows_2026_partitions_gt1day': 0,
             'partitions_missing_units_or_mv': 0}
    frames, all_tdates = [], set()
    for r in sorted(manifest, key=lambda x: x['date']):
        day = dt.date.fromisoformat(r['date'])
        t, tds = read_partition(r['source_path'], day, served_assets, stats)
        all_tdates |= tds
        frames.append(t)
    df = pd.concat(frames, ignore_index=True)
    rep['partitions'] = {'verified': len(manifest), 'verdicts': sorted(set(r['verdict'] for r in manifest)),
                         'first': min(r['date'] for r in manifest), 'last': max(r['date'] for r in manifest),
                         'manifest_file': 'PARTITIONS3.csv'}
    rep['keying_stats'] = stats
    rep['trade_dates_in_store'] = len(all_tdates)
    rep['universe_assets'] = len(served_assets)
    rep['universe_trade_rows'] = int(len(df))
    rep['window_trade_dates_absent_from_store'] = sorted(
        (WIN_START + dt.timedelta(days=i)).isoformat() for i in range((WIN_END - WIN_START).days + 1)
        if (WIN_START + dt.timedelta(days=i)).weekday() < 5 and (WIN_START + dt.timedelta(days=i)) not in all_tdates)
    rep['floor'] = min(r['date'] for r in manifest)

    # ---- R1.3 per trade date: kept prices and withheld rows, the whole history ----
    A = mod.TRADE_TYPES_A
    groups = {d: g for d, g in df.groupby('tdate', sort=True)}
    hist = {}  # asset -> {date: [status, kept_result, withheld_result]}
    withheld_trade_rows = 0
    withheld_unit_trade_rows = 0
    withheld_by_asset = {}
    for d in sorted(groups):
        g = groups[d][COLS_READ]
        kept = mod.price_for_date(g, d, A, cands, served_units=units)
        wh = mod.withheld_for_date(g, d, A, cands, served_units=units)
        for asset, v in kept.items():
            hist.setdefault(asset, {})[d] = ['KEPT', v, None]
        for asset, v in wh.items():
            prev = hist.setdefault(asset, {}).get(d)
            hist[asset][d] = ['WITHHELD', prev[1] if prev else kept.get(asset), v]
            withheld_trade_rows += sum(v['reasons'].values())
            withheld_unit_trade_rows += v['reasons'].get('unit_unreadable', 0)
            if d >= WIN_START and d <= WIN_END:
                slot = withheld_by_asset.setdefault(asset, {'trade_rows': 0, 'ratios': set(), 'dates': set(),
                                                            'unit_unreadable_rows': 0})
                slot['trade_rows'] += sum(v['reasons'].values())
                slot['unit_unreadable_rows'] += v['reasons'].get('unit_unreadable', 0)
                slot['ratios'].update(round(x, 6) for x in v['ratios'] if x is not None)
                slot['dates'].add(d)
    dates_by_asset = {asset: sorted(dd) for asset, dd in hist.items()}
    rep['withheld_trade_rows_all_history'] = withheld_trade_rows
    rep['withheld_unit_unreadable_trade_rows_all_history'] = withheld_unit_trade_rows

    def last_before(asset, d):
        """The latest trade date strictly before d with any qualifying or withheld row for the asset."""
        ds = dates_by_asset.get(asset, [])
        i = bisect.bisect_left(ds, d) - 1
        if i < 0:
            return None
        e = ds[i]
        return e, hist[asset][e]

    # ---- window records and flags (the module's own per-row records, window dates only) ----
    win = df[(df['tdate'] >= WIN_START) & (df['tdate'] <= WIN_END)]
    win_groups = {k: v for k, v in win.groupby(['tdate', 'asset_name'], sort=True)}
    win_dates = {d: groups[d] for d in sorted(groups) if WIN_START <= d <= WIN_END}
    recs_by = {}
    for d, g in win_dates.items():
        recs, _ = mod._classify(g[COLS_READ].reset_index(drop=True), d, A, cands, units)
        for rec in recs:
            recs_by.setdefault((d, rec['asset']), []).append(rec)

    def flags_for(d, asset, served_p, kept_entry):
        recs = recs_by.get((d, asset), [])
        ex = {}
        for r_ in recs:
            key = r_['excluded'] if r_['excluded'] is not None else ('NO_PRICE' if r_['no_price'] else None)
            if key is not None:
                ex[key] = ex.get(key, 0) + 1
        fl = []
        sub = win_groups.get((d, asset))
        raw = []
        if sub is not None:
            raw = [float(v) for v in pd.to_numeric(sub['price'], errors='coerce').dropna() if v > 0]
        if served_p is not None and close(1.0, served_p) and raw and close(statistics.median(raw), served_p):
            fl.append('dividend_dominated')
        if kept_entry is not None:
            kept_rows = [r_['price'] for r_ in recs if r_['kept']]
            if kept_rows and abs(statistics.median(kept_rows) - kept_entry['price']) > TOL * max(1.0, kept_entry['price']):
                fl.append('repeat_weighted')
            if any(r_['scaled'] for r_ in recs if r_['kept']):
                fl.append('scale_100x')
        fl.append('estimated_row=0')
        wh_recs = [r_ for r_ in recs if r_['withheld'] is not None]
        if wh_recs:
            ratios = sorted(round(r_['ratio'], 6) if r_['ratio'] is not None else None for r_ in wh_recs
                            if r_['ratio'] is not None)
            fl.append('withheld:%s:ratio=%s' % (wh_recs[0]['withheld'], '/'.join('%g' % x for x in ratios) or 'none'))
        ex_str = ';'.join('%s:%d' % (k, ex[k]) for k in sorted(ex))
        return '|'.join(fl), ex_str

    def old_types(d, asset, served_p):
        sub = win_groups.get((d, asset))
        if sub is None:
            return 'none'
        hit = []
        for t, grp in sub.groupby('transaction_type', sort=True):
            gp = [float(v) for v in pd.to_numeric(grp['price'], errors='coerce').dropna() if v > 0]
            if gp and close(statistics.median(gp), served_p):
                hit.append(str(t))
        return '|'.join(hit) if hit else 'none'

    def is_unit_withheld(asset):
        """AMENDMENT R1.3 clause 2: a Fixed Income asset whose unit is unreadable (or absent) is never priced."""
        return asset in cands and unit_of(asset) == 'unreadable'

    def classify_served(d, asset, s):
        """Return (class, new_price, observation_date, reason, kept_entry, withheld_entry)."""
        if is_unit_withheld(asset):
            return 'NOT_RECOMPUTABLE', None, '', 'unit_unreadable', None, None
        st = hist.get(asset, {}).get(d)
        if d not in all_tdates:
            return 'NOT_RECOMPUTABLE', None, '', 'no_rows_on_date', None, None
        if st is not None and st[0] == 'WITHHELD':
            return 'NOT_RECOMPUTABLE', None, '', 'ratio_unrecognised', None, st[2]
        if st is not None and st[0] == 'KEPT':
            new = st[1]['price']
            cls = 'UNCHANGED' if close(new, s) else 'CHANGED'
            return cls, new, d.isoformat(), 'trade_median_R1_3', st[1], None
        lb = last_before(asset, d)
        if lb is None:
            return 'NOT_RECOMPUTABLE', None, '', 'no_earlier_trade', None, None
        e, ent = lb
        if ent[0] == 'WITHHELD':
            return 'NOT_RECOMPUTABLE', None, '', 'ratio_unrecognised_carry', None, ent[2]
        return 'NOW_CARRY_FORWARD', ent[1]['price'], e.isoformat(), 'carry_forward_from_%s' % e.isoformat(), ent[1], None

    def unit_changed(new, old):
        """AMENDMENT R1.3 clause 3: the ratio new/old within 1 percent of 100 or of 0.01."""
        if new is None or old is None or old <= 0:
            return False
        ratio = new / old
        return abs(ratio - 100.0) <= 0.01 * 100.0 or abs(ratio - 0.01) <= 0.01 * 0.01

    def build_lists():
        rows, est = [], []
        classes = {k: 0 for k in CLASSES}
        withheld_served = 0
        withheld_direct = 0
        withheld_via_carry = 0
        unit_withheld = 0
        unit_withheld_assets = {}
        unit_changed_rows = []
        both_kept_and_withheld = 0
        touched = {}
        movers = []
        moved_diff = 0
        par_rows = []
        carry_par_scaled = [0]
        for d, asset in served_keys:
            s = served_price[(d, asset)]
            cls, new, obs, reason, kept_e, wh_e = classify_served(d, asset, s)
            classes[cls] += 1
            if reason == 'unit_unreadable':
                unit_withheld += 1
                unit_withheld_assets.setdefault(asset, 0)
                unit_withheld_assets[asset] += 1
            elif reason == 'ratio_unrecognised':
                withheld_served += 1
                touched.setdefault(asset, set()).add(d.isoformat())
                withheld_direct += 1
            elif reason == 'ratio_unrecognised_carry':
                withheld_served += 1
                touched.setdefault(asset, set()).add(d.isoformat())
                withheld_via_carry += 1
            if cls in ('CHANGED', 'NOW_CARRY_FORWARD') and unit_changed(new, s):
                unit_changed_rows.append('%s|%s' % (d.isoformat(), asset))
            if st_both(d, asset):
                both_kept_and_withheld += 1
            flags, ex_str = flags_for(d, asset, s, kept_e)
            distinct = len(kept_e['trade_ids']) if kept_e is not None else 0
            if cls in ('CHANGED', 'NOW_CARRY_FORWARD') and not close(new, s):
                moved_diff += 1
                movers.append((abs(new - s), d.isoformat(), asset, s, new, cls, reason))
            key = (d.isoformat(), asset)
            r2row = r2.get(key)
            r1row = r1.get(key)
            s2row = s2.get(key)
            if kept_e is not None and kept_e.get('par_scaled_ids'):
                par_rows.append(key)
            rows.append({'date': d.isoformat(), 'asset_name': asset, 'served_unit': unit_of(asset),
                         'old_price': fmt(s), 'old_source': 'transaction_observed',
                         'new_price': fmt(new), 'class': cls, 'reason': reason, 'distinct_trades': distinct,
                         'excluded_by_type': ex_str, 'flags': flags, 'observation_date': obs,
                         'old_price_types': old_types(d, asset, s),
                         'round2_class': r2row['class'] if r2row else 'NOT_IN_ROUND2',
                         'round2_new_price': r2row['new_price_A'] if r2row else '',
                         'seat2_class': s2row['class'] if s2row else 'NOT_IN_SEAT2',
                         'seat2_new_price': s2row['new_price'] if s2row else '',
                         'in_round2': 1 if r2row else 0,
                         'round1_class': r1row[0] if r1row else 'NOT_IN_ROUND1',
                         'round1_recomputed': r1row[1] if r1row else '',
                         'carry_source_par_scaled': 1 if (cls == 'NOW_CARRY_FORWARD' and kept_e is not None
                                                          and kept_e.get('par_scaled_ids')) else 0,
                         'unit_changed': 1 if (cls in ('CHANGED', 'NOW_CARRY_FORWARD') and unit_changed(new, s)) else 0})
            if cls == 'NOW_CARRY_FORWARD' and kept_e is not None and kept_e.get('par_scaled_ids'):
                carry_par_scaled[0] += 1
        # interpolated rows of the served assets
        est_counts = {'rows': 0, 'trade_price': 0, 'last_traded_date': 0, 'unresolved': 0}
        interp_refused = {}
        interp_reasons = {}
        interp_unit_withheld = 0
        interp_carry_par_scaled = [0]
        for r_ in interp_served.itertuples(index=False):
            d, asset = r_.d, r_.asset_name
            st = hist.get(asset, {}).get(d)
            if is_unit_withheld(asset):
                fate, rp, rb, ro, why = 'unresolved', '', '', '', 'unit_unreadable'
                interp_unit_withheld += 1
            elif st is not None and st[0] == 'WITHHELD':
                fate, rp, rb, ro, why = 'unresolved', '', '', '', 'ratio_unrecognised'
            elif st is not None and st[0] == 'KEPT':
                fate, rp, rb, ro, why = 'trade_price', fmt(st[1]['price']), 'trade', d.isoformat(), 'trade_median_R1_3'
            else:
                # no trade on the date (ruling clause 5): the carry-forward applies, WITH its observation date
                lb = last_before(asset, d)
                no_rows = '' if d in all_tdates else '_no_store_rows_on_date'
                if lb is None:
                    fate, rp, rb, ro, why = 'unresolved', '', '', '', 'no_earlier_trade'
                elif lb[1][0] == 'WITHHELD':
                    fate, rp, rb, ro, why = 'unresolved', '', '', '', 'ratio_unrecognised_carry'
                else:
                    fate, rp, rb, ro, why = ('last_traded_date', fmt(lb[1][1]['price']), 'last_traded', lb[0].isoformat(),
                                             'carry_forward' + no_rows)
                    if lb[1][1].get('par_scaled_ids'):
                        interp_carry_par_scaled[0] += 1
            if why.startswith('ratio_unrecognised'):
                interp_refused[asset] = interp_refused.get(asset, 0) + 1
            interp_reasons[why] = interp_reasons.get(why, 0) + 1
            est_counts['rows'] += 1
            est_counts[fate] += 1
            est.append({'date': d.isoformat(), 'asset_name': asset, 'served_unit': unit_of(asset),
                        'canonical_price': fmt(r_.price), 'canonical_source': r_.source, 'fate': fate, 'r1_price': rp,
                        'r1_basis': rb, 'r1_observation_date': ro, 'reason': why, 'estimated_row': 1})
        est_counts['interp_refused'] = interp_refused
        est_counts['interp_unit_withheld'] = interp_unit_withheld
        est_counts['carry_par_scaled_served'] = carry_par_scaled[0]
        est_counts['interp_reasons'] = interp_reasons
        est_counts['carry_par_scaled_interp'] = interp_carry_par_scaled[0]
        return rows, est, classes, {'withheld_served': withheld_served, 'withheld_direct': withheld_direct,
                                    'withheld_via_carry': withheld_via_carry,
                                    'unit_withheld': unit_withheld, 'unit_withheld_assets': unit_withheld_assets,
                                    'unit_changed_rows': unit_changed_rows,
                                    'both_kept_and_withheld': both_kept_and_withheld, 'touched': touched,
                                    'movers': movers, 'moved_diff': moved_diff, 'par_rows': par_rows}, est_counts

    def st_both(d, asset):
        st = hist.get(asset, {}).get(d)
        return bool(st is not None and st[0] == 'WITHHELD' and st[1] is not None)

    rows_a, est_a, classes_a, extra_a, est_counts_a = build_lists()
    rows_b, est_b, classes_b, extra_b, est_counts_b = build_lists()  # second in-process pass
    in_process_equal = (rows_a == rows_b) and (est_a == est_b) and (classes_a == classes_b)

    def dump(rows_, cols):
        buf = io.StringIO()
        w = csv.DictWriter(buf, fieldnames=cols, lineterminator='\n')
        w.writeheader()
        for x in rows_:
            w.writerow(x)
        return buf.getvalue().encode('utf-8')

    list_bytes = dump(rows_a, LIST_COLS)
    est_bytes = dump(est_a, EST_COLS)
    list_md5 = hashlib.md5(list_bytes).hexdigest()
    list_sha = hashlib.sha256(list_bytes).hexdigest()
    os.makedirs(a.out, exist_ok=True)
    with open(os.path.join(a.out, 'BEFORE_AFTER3.csv'), 'wb') as fh:
        fh.write(list_bytes)
    with open(os.path.join(a.out, 'ESTIMATED_ROWS3.csv'), 'wb') as fh:
        fh.write(est_bytes)

    # ---- past-date arm: 20 CHANGED rows, the result for the date from trades on or before that date ----
    past = []
    changed = [r_ for r_ in rows_a if r_['class'] == 'CHANGED'][:20]
    for r_ in changed:
        d = dt.date.fromisoformat(r_['date'])
        asset = r_['asset_name']
        full = hist[asset][d][1]
        frame = df[(df['asset_name'] == asset) & (df['tdate'] <= d)][COLS_READ]
        before = mod.price_for_date(frame, d, A, cands, served_units=units).get(asset)
        day_ids = set(mod._trade_id(v, i) for i, v in enumerate(groups[d]['transaction_id']))
        past.append({'date': r_['date'], 'asset_name': asset,
                     'equal': bool(before is not None and before['price'] == full['price'] and before['trade_ids'] == full['trade_ids']),
                     'ids_on_date_only': bool(set(full['trade_ids']) <= day_ids)})

    # ---- the four classes and the denominator ----
    c = classes_a
    served_n = len(rows_a)
    moved_n = c['CHANGED'] + c['NOW_CARRY_FORWARD']
    movers = sorted(extra_a['movers'], key=lambda x: -x[0])
    r2_scale = sorted(k for k, v in r2.items() if 'scale_100x' in v['flags'])
    cur_by_key = {(x['date'], x['asset_name']): x for x in rows_a}
    par_unchanged = sum(1 for k in r2_scale if k in cur_by_key and cur_by_key[k]['class'] == 'UNCHANGED')
    cf_rows = [x for x in rows_a if x['class'] == 'NOW_CARRY_FORWARD']
    tin = sum(1 for x in cf_rows if x['old_price_types'] == 'Transfer In')
    tin_any = sum(1 for x in cf_rows if 'Transfer In' in x['old_price_types'].split('|'))
    cf_with_date = sum(1 for x in cf_rows if x['observation_date'])
    # round 1's UNEXPLAINED rows, and the subset that recomputed to 1.0, each with its amended class and price
    r1_amend = {'UNEXPLAINED': {}, 'RECOMPUTED_1_0': {}}
    for k, (r1cls, r1rec) in sorted(r1.items()):
        if r1cls != 'UNEXPLAINED':
            continue
        is_one = bool(r1rec) and abs(float(r1rec) - 1.0) < 1e-9
        x = cur_by_key.get(k)
        cls_now = x['class'] if x else 'NOT_IN_SERVED_SET'
        r1_amend['UNEXPLAINED'][cls_now] = r1_amend['UNEXPLAINED'].get(cls_now, 0) + 1
        if is_one:
            r1_amend['RECOMPUTED_1_0'][cls_now] = r1_amend['RECOMPUTED_1_0'].get(cls_now, 0) + 1
    rep['round1_unexplained_amended'] = r1_amend
    rep['round1_unexplained_rows'] = sum(r1_amend['UNEXPLAINED'].values())
    rep['round1_recomputed_1_0_rows'] = sum(r1_amend['RECOMPUTED_1_0'].values())

    # the named case: MORGAN STANLEY FIN LLC 0% 05/03/2029 on 2026-10-05, and its interpolated rows
    morgan = 'MORGAN STANLEY FIN LLC 0% 05/03/2029'
    m_row = cur_by_key.get(('2026-10-05', morgan))
    m_est = [x for x in est_a if x['asset_name'] == morgan]
    m_fates = {}
    m_prices = {}
    for x in m_est:
        m_fates[x['fate']] = m_fates.get(x['fate'], 0) + 1
        k_ = (x['r1_price'], x['r1_observation_date'])
        m_prices[k_] = m_prices.get(k_, 0) + 1
    rep['named_case_morgan'] = {
        'asset_name': morgan, 'served_unit': unit_of(morgan), 'fixed_income': morgan in cands,
        'served_2026_10_05': m_row['old_price'] if m_row else None,
        'row_2026_10_05': {k: m_row[k] for k in ('new_price', 'class', 'reason', 'observation_date', 'old_price_types')}
        if m_row else None,
        'interpolated_rows': len(m_est), 'interpolated_fates': {k: m_fates[k] for k in sorted(m_fates)},
        'interpolated_carry_prices': [{'r1_price': k_[0], 'r1_observation_date': k_[1], 'rows': m_prices[k_]}
                                      for k_ in sorted(m_prices, key=lambda z: (str(z[1]), str(z[0])))],
    }
    morgan_hist = []
    for d_ in sorted(hist.get(morgan, {})):
        st_ = hist[morgan][d_]
        morgan_hist.append({'date': d_.isoformat(), 'status': st_[0],
                            'kept_price': None if st_[1] is None else st_[1]['price'],
                            'withheld': None if st_[2] is None else st_[2]['reasons']})
    rep['named_case_morgan']['trade_dates_with_qualifying_or_withheld_rows'] = morgan_hist

    ests = est_counts_a
    rec = {
        'order': 'BP-c-2',
        'read_at': dt.datetime.now(dt.timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ'),
        'claim': 'measured',
        'calls': [
            'aws s3api head-object --bucket opal-data-bd --key silver/prices/canonical_prices.parquet (ETag %s, LastModified %s)'
            % (a.canonical_etag, a.canonical_modified),
            'aws s3api get-object --bucket opal-data-bd --key silver/prices/canonical_prices.parquet (to C:/dev/wk-bdprce-r3-21-data/, md5 equal to the ETag)',
            'aws s3api get-object --bucket opal-data-bd --key silver/bd_assets_dim.parquet (to C:/dev/wk-bdprce-r3-21-data/, md5 equal to the ETag)',
            'aws s3api list-objects-v2 --bucket opal-data-bd --prefix silver/transactions/ (1,929 keys: 1,928 dated partitions and _README.txt)',
            'aws s3api head-object --bucket opal-data-bd --key silver/transactions/<date>.parquet (1,928 keys: ContentLength and ETag)',
            'aws s3api get-object --bucket opal-data-bd --key silver/transactions/<date>.parquet (4 partitions whose cached copy failed verification or was missing: 2026-10-02, 2026-10-08, 2026-10-11, 2026-10-14)',
        ],
        'amendment': 'R1.3',
        'window': '%s..%s (%d weekday dates)' % (WIN_START.isoformat(), WIN_END.isoformat(), weekdays),
        'served_rows': served_n,
        'classes': {k: c[k] for k in CLASSES},
        'moved': moved_n,
        'prices_differ_from_served': extra_a['moved_diff'],
        'served_units': served_units_counts,
        'unit_map_file': 'UNIT_MAP.csv',
        'unit_map_sha256': units_sha,
        'unit_map_summary_file': 'UNIT_MAP_SUMMARY.json',
        'unit_changed_rows': len(extra_a['unit_changed_rows']),
        'unit_changed_row_keys': extra_a['unit_changed_rows'],
        'unit_withheld_rows': extra_a['unit_withheld'],
        'unit_withheld_assets': {k: extra_a['unit_withheld_assets'][k] for k in sorted(extra_a['unit_withheld_assets'])},
        'unit_withheld_trade_rows_window': sum(v['unit_unreadable_rows'] for v in withheld_by_asset.values()),
        'unit_withheld_trade_rows_all_history': withheld_unit_trade_rows,
        'par_quoted_rows': len(r2_scale),
        'par_rows_unchanged': par_unchanged,
        'withheld_rows': extra_a['withheld_served'],
        'withheld_rows_direct': extra_a['withheld_direct'],
        'withheld_rows_via_carry_refusal': extra_a['withheld_via_carry'],
        'withheld_trade_rows_keyed_history': withheld_trade_rows,
        'withheld_nonfi_trade_rows': sum(v['trade_rows'] for k, v in withheld_by_asset.items() if k not in cands),
        'withheld_assets_count': len(withheld_by_asset),
        'withheld_assets_in_served_set': sum(1 for k in withheld_by_asset if k in served_assets),
        'both_kept_and_withheld_served_rows': extra_a['both_kept_and_withheld'],
        'transfer_in_carry_forwards': tin,
        'transfer_in_any_carry_forwards': tin_any,
        'carry_forwards_with_date': cf_with_date,
        'carry_forwards_from_par_scaled_trade': sum(1 for x in cf_rows if x['carry_source_par_scaled'] == '1'),
        'interpolated_carry_from_par_scaled_trade': ests['carry_par_scaled_interp'],
        'interpolated': {'rows': ests['rows'], 'with_trade_price': ests['trade_price'],
                         'with_last_traded_date': ests['last_traded_date'], 'unresolved': ests['unresolved'],
                         'unit_withheld': ests['interp_unit_withheld'],
                         'reasons': ests['interp_reasons'], 'assets_with_ratio_refusal': len(ests['interp_refused'])},
        'lookback_keying': {
            'mode': 'trade_date_all_partitions',
            'statement': ('Keyed on trade_date across all %d verified silver/transactions partitions (%s..%s; the file '
                          'holds no key; 1,926 by md5 and 2 by size against a multipart ETag, see PARTITIONS3.csv). '
                          '%d trade dates in the store. Window weekdays with no trade in the store: %s. '
                          'Late-landed rows (file day after trade day): %d, of which %d lag more than one day, in all '
                          'partitions; %d and %d in the 2026 partitions. The 2026-10-14 partition is present at the read and '
                          'holds %d rows dated inside the window, keyed here. Limit: a trade dated on a day with no '
                          'partition, that never landed in a later partition, is not in the store; interpolated rows of '
                          'such a day (2026-10-13) carry the last trade before it.') % (
                len(manifest), rep['floor'], rep['partitions']['last'], len(all_tdates),
                ', '.join(rep['window_trade_dates_absent_from_store']) or 'none',
                stats['late_rows_any'], stats['late_rows_gt1day'],
                stats['late_rows_2026_partitions'], stats['late_rows_2026_partitions_gt1day'],
                stats.get('partition_2026_10_14_rows_dated_in_window', 0))},
        'deterministic': bool(in_process_equal),
        'served_write': False,
        'list_file': 'BEFORE_AFTER3.csv',
        'list_sha256': list_sha,
        'list_md5': list_md5,
        'estimated_list_file': 'ESTIMATED_ROWS3.csv',
        'estimated_list_md5': hashlib.md5(est_bytes).hexdigest(),
        'peer_md5': a.peer_md5,
        'peer_md5_equal': bool(a.peer_md5) and a.peer_md5 == list_md5,
        'past_date_arm': {'sampled': len(past), 'equal': sum(1 for p in past if p['equal']),
                          'ids_on_date_only': sum(1 for p in past if p['ids_on_date_only'])},
        'definitions': {
            'withheld_rows': 'served asset-dates classed NOT_RECOMPUTABLE with reason ratio_unrecognised (direct, or a carry-forward refused because the last trade date is withheld)',
            'unit_withheld_rows': 'served asset-dates of a Fixed Income asset whose served unit is unreadable (or absent from the map): NOT_RECOMPUTABLE, reason unit_unreadable, never priced',
            'unit_changed_rows': 'served rows CHANGED or NOW_CARRY_FORWARD whose new/old price is within 1 percent of 100 or of 0.01; must be 0',
            'par_quoted_rows': 'the eight round-2 rows whose flag carried scale_100x',
            'par_withheld': 'withheld trade rows of Fixed Income assets over the window (all assets, served or not); equals withheld_fi_trade_rows',
            'withheld_assets': 'every asset with a withheld trade row on a window date; served_rows_touched counts the served asset-dates it withholds or refuses to carry',
        },
        'withheld_assets': {k: {'trade_rows': v['trade_rows'], 'unit_unreadable_rows': v['unit_unreadable_rows'],
                                'ratios': sorted(v['ratios']),
                                'dates': sorted(d_.isoformat() for d_ in v['dates']),
                                'served_unit': unit_of(k),
                                'fixed_income': k in cands, 'in_served_set': k in served_assets,
                                'served_rows_touched': len(extra_a['touched'].get(k, set())),
                                'unit_withheld_served_rows': extra_a['unit_withheld_assets'].get(k, 0),
                                'interpolated_rows_refused': ests['interp_refused'].get(k, 0)}
                            for k, v in sorted(withheld_by_asset.items())},
        'withheld_fi_trade_rows': sum(v['trade_rows'] for k, v in withheld_by_asset.items() if k in cands),
        'par_withheld': sum(v['trade_rows'] for k, v in withheld_by_asset.items() if k in cands),
        'movers_top3': [{'asset_name': m[2], 'date': m[1], 'served': m[3], 'new': m[4], 'class': m[5], 'reason': m[6],
                         'move_percent': round(100.0 * (m[4] - m[3]) / m[3], 4)}
                        for m in movers[:3]],
        'rep': rep,
    }
    with open(os.path.join(a.out, 'REPLAY3.json'), 'w', encoding='utf-8', newline='\n') as fh:
        json.dump(rec, fh, indent=1, sort_keys=True, ensure_ascii=True)
        fh.write('\n')
    print('served=%d classes=%s' % (served_n, json.dumps({k: c[k] for k in CLASSES}, sort_keys=True)))
    print('BEFORE_AFTER3 md5=%s rows=%d estimated=%d deterministic=%s peer_equal=%s unit_changed=%d unit_withheld=%d'
          % (list_md5, len(rows_a), len(est_a), str(rec['deterministic']).lower(),
             str(rec['peer_md5_equal']).lower(), rec['unit_changed_rows'], rec['unit_withheld_rows']))
    return 0


if __name__ == '__main__':
    sys.exit(main())
