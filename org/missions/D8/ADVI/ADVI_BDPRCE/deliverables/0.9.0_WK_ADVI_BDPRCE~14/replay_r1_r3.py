#!/usr/bin/env python3
"""BP-c-2 -- R1 replayed on AMENDMENT R1.2, keyed on trade_date across ALL verified partitions. READ-ONLY.

Adapted from round 2's replay_r1.py (BP-b-2, copied, not edited) and lookback_scan.py. What changed from round 2:
  - the module is the amended one (R1.2, bd_price_rule.py): par-quoted decided per row, withheld rows counted;
  - the candidate Fixed Income set is built from silver/bd_assets_dim.parquet (asset_super_class_bd == 'Fixed Income');
  - the trade universe is EVERY verified partition (verify_partitions.py), keyed on trade_date, not a 2-day window;
  - the carry-forward looks back through the whole keyed history (no residual lookback pass);
  - a served or interpolated asset-date with any WITHHELD trade is NOT_RECOMPUTABLE (ratio_unrecognised), never priced.

Inputs (all read-only): --canonical, --dim, --manifest (PARTITIONS2.csv), --round2 (round 2 BEFORE_AFTER.csv),
--round1 (round 1 GAP_ROWS.csv). Outputs in --out: BEFORE_AFTER2.csv, ESTIMATED_ROWS2.csv, REPLAY2.json, and a
two-pass in-process determinism check. --peer-md5 takes the BEFORE_AFTER2.csv md5 of a SEPARATE process run.

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
COLS_READ = ['transaction_id', 'transaction_type', 'price', 'trade_date', 'asset_name', 'units', 'market_value']
DIM_CLASS = 'asset_super_class_bd'
FI_CLASS = 'Fixed Income'
COUPON = 'coupon_rate'
ROUND2_LIST = 'org/missions/D8/ADVI/ADVI_BDPRCE/deliverables/0.9.0_WK_ADVI_BDPRCE~6/BEFORE_AFTER.csv'
ROUND1_LIST = 'org/missions/D8/ADVI/ADVI_BDPRCE/deliverables/0.9.0_WK_ADVI_BDPRCE~3/GAP_ROWS.csv'
LIST_COLS = ['date', 'asset_name', 'old_price', 'old_source', 'new_price', 'class', 'reason', 'distinct_trades',
             'excluded_by_type', 'flags', 'observation_date', 'old_price_types', 'round2_class', 'round2_new_price',
             'in_round2', 'round1_class', 'round1_recomputed', 'carry_source_par_scaled']
EST_COLS = ['date', 'asset_name', 'canonical_price', 'canonical_source', 'fate', 'r1_price', 'r1_basis',
            'r1_observation_date', 'reason', 'estimated_row']


def close(x, served):
    return x is not None and abs(x - served) <= TOL * max(1.0, abs(served))


def fmt(x):
    return '' if x is None else repr(float(x))


def load_module(root):
    sys.path.insert(0, os.path.join(root, 'data', 'black_diamond', 'scripts', 'silver'))
    import bd_price_rule  # noqa: E402  (read, not changed)
    if bd_price_rule.AMENDMENT != 'R1.2':
        raise SystemExit('ERROR: module amendment is %r, expected R1.2' % bd_price_rule.AMENDMENT)
    return bd_price_rule


def read_partition(path, day, universe, stats):
    """Read the trade columns of one verified partition; keep the universe's rows and EVERY window-dated row.

    The window's withheld census needs every asset's rows dated in the window, served or not; the carry-forward
    and the fates need only the universe's history.
    """
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
    ap.add_argument('--out', required=True)
    ap.add_argument('--peer-md5', default='')
    ap.add_argument('--canonical-etag', default='')
    ap.add_argument('--canonical-modified', default='')
    ap.add_argument('--exclude-day', action='append', default=[],
                    help='sensitivity only: leave one partition out (the record names it)')
    a = ap.parse_args()
    mod = load_module(a.root)
    rep = {}

    # ---- the asset dimension and the par-quoted candidate set (R1.2; the coupon corroborates only) ----
    dim = pd.read_parquet(a.dim, columns=['asset_name', DIM_CLASS, COUPON])
    cands, conflicting = mod.par_quoted_candidates(dim, DIM_CLASS, FI_CLASS)
    coup = mod.coupon_corroboration(dim, COUPON, cands)
    rep['dimension'] = {'rows': int(len(dim)), 'fixed_income_rows': int((dim[DIM_CLASS] == FI_CLASS).sum()),
                        'fixed_income_names': len(cands), 'conflicting_names': sorted(conflicting),
                        'candidates_with_coupon': sum(1 for v in coup.values() if v)}

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
    interp = canon[(canon['source'] == 'linear_interpolation')].copy()
    interp_served = interp[interp['asset_name'].isin(served_assets)].sort_values(['d', 'asset_name']).copy()
    rep['interpolated_window_all_assets'] = int(len(interp))
    rep['interpolated_window_all_assets_names'] = int(interp['asset_name'].nunique())
    rep['interpolated_rows'] = int(len(interp_served))
    rep['interpolated_assets'] = int(interp_served['asset_name'].nunique())

    # ---- round 2 and round 1 lists, read for comparison only ----
    r2 = {}
    with open(os.path.join(a.root, ROUND2_LIST), encoding='utf-8') as fh:
        for r in csv.DictReader(fh):
            r2[(r['date'], r['asset_name'])] = r
    r1 = {}
    with open(os.path.join(a.root, ROUND1_LIST), encoding='utf-8') as fh:
        for r in csv.DictReader(fh):
            r1[(r['date'], r['asset_name'])] = (r['class'], r['recomputed_price'])
    cur_keys = set((d.isoformat(), a_) for d, a_ in served_keys)
    rep['served_vs_round2'] = {'round2_rows': len(r2), 'current_rows': len(cur_keys),
                               'added': sorted('%s|%s' % k for k in cur_keys - set(r2)),
                               'removed': sorted('%s|%s' % k for k in set(r2) - cur_keys),
                               'common_price_differs': sum(1 for d, a_ in served_keys
                                                           if (d.isoformat(), a_) in r2 and abs(
                                                               float(r2[(d.isoformat(), a_)]['old_price']) -
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
    if a.exclude_day:
        manifest = [r for r in manifest if r['date'] not in set(a.exclude_day)]
        rep['excluded_days_sensitivity'] = sorted(a.exclude_day)
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
                         'first': min(r['date'] for r in manifest), 'last': max(r['date'] for r in manifest)}
    rep['keying_stats'] = stats
    rep['trade_dates_in_store'] = len(all_tdates)
    rep['universe_assets'] = len(served_assets)
    rep['universe_trade_rows'] = int(len(df))
    rep['window_trade_dates_absent_from_store'] = sorted(
        (WIN_START + dt.timedelta(days=i)).isoformat() for i in range((WIN_END - WIN_START).days + 1)
        if (WIN_START + dt.timedelta(days=i)).weekday() < 5 and (WIN_START + dt.timedelta(days=i)) not in all_tdates)
    rep['floor'] = min(r['date'] for r in manifest)

    # ---- R1.2 per trade date: kept prices and withheld rows, the whole history ----
    A = mod.TRADE_TYPES_A
    groups = {d: g for d, g in df.groupby('tdate', sort=True)}
    hist = {}  # asset -> {date: [status, kept_result, withheld_result]}
    withheld_trade_rows = 0
    withheld_by_asset = {}
    for d in sorted(groups):
        g = groups[d][COLS_READ]
        kept = mod.price_for_date(g, d, A, cands)
        wh = mod.withheld_for_date(g, d, A, cands)
        for asset, v in kept.items():
            hist.setdefault(asset, {})[d] = ['KEPT', v, None]
        for asset, v in wh.items():
            prev = hist.setdefault(asset, {}).get(d)
            hist[asset][d] = ['WITHHELD', prev[1] if prev else kept.get(asset), v]
            withheld_trade_rows += sum(v['reasons'].values())
            if d >= WIN_START and d <= WIN_END:
                slot = withheld_by_asset.setdefault(asset, {'trade_rows': 0, 'ratios': set(), 'dates': set()})
                slot['trade_rows'] += sum(v['reasons'].values())
                slot['ratios'].update(round(x, 6) for x in v['ratios'] if x is not None)
                slot['dates'].add(d)
    dates_by_asset = {asset: sorted(dd) for asset, dd in hist.items()}
    rep['withheld_trade_rows_all_history'] = withheld_trade_rows

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
        recs, _ = mod._classify(g[COLS_READ].reset_index(drop=True), d, A, cands)
        for rec in recs:
            recs_by.setdefault((d, rec['asset']), []).append(rec)

    def flags_for(d, asset, served_price, kept_entry):
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
        if served_price is not None and close(1.0, served_price) and raw and close(statistics.median(raw), served_price):
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

    def old_types(d, asset, served_price):
        sub = win_groups.get((d, asset))
        if sub is None:
            return 'none'
        hit = []
        for t, grp in sub.groupby('transaction_type', sort=True):
            gp = [float(v) for v in pd.to_numeric(grp['price'], errors='coerce').dropna() if v > 0]
            if gp and close(statistics.median(gp), served_price):
                hit.append(str(t))
        return '|'.join(hit) if hit else 'none'

    def classify_served(d, asset, s):
        """Return (class, new_price, observation_date, reason, kept_entry, withheld_entry)."""
        st = hist.get(asset, {}).get(d)
        if d not in all_tdates:
            return 'NOT_RECOMPUTABLE', None, '', 'no_rows_on_date', None, None
        if st is not None and st[0] == 'WITHHELD':
            return 'NOT_RECOMPUTABLE', None, '', 'ratio_unrecognised', None, st[2]
        if st is not None and st[0] == 'KEPT':
            new = st[1]['price']
            cls = 'UNCHANGED' if close(new, s) else 'CHANGED'
            return cls, new, d.isoformat(), 'trade_median_R1_2', st[1], None
        lb = last_before(asset, d)
        if lb is None:
            return 'NOT_RECOMPUTABLE', None, '', 'no_earlier_trade', None, None
        e, ent = lb
        if ent[0] == 'WITHHELD':
            return 'NOT_RECOMPUTABLE', None, '', 'ratio_unrecognised_carry', None, ent[2]
        return 'NOW_CARRY_FORWARD', ent[1]['price'], e.isoformat(), 'carry_forward_from_%s' % e.isoformat(), ent[1], None

    def build_lists():
        rows, est = [], []
        classes = {k: 0 for k in CLASSES}
        withheld_served = 0
        withheld_direct = 0
        withheld_via_carry = 0
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
            if reason == 'ratio_unrecognised':
                withheld_served += 1
                touched.setdefault(asset, set()).add(d.isoformat())
                withheld_direct += 1
            elif reason == 'ratio_unrecognised_carry':
                withheld_served += 1
                touched.setdefault(asset, set()).add(d.isoformat())
                withheld_via_carry += 1
            if st_both(d, asset):
                both_kept_and_withheld += 1
            flags, ex_str = flags_for(d, asset, s, kept_e)
            distinct = len(kept_e['trade_ids']) if kept_e is not None else 0
            if cls in ('CHANGED', 'NOW_CARRY_FORWARD') and not close(new, s):
                moved_diff += 1
                movers.append((abs(new - s), d.isoformat(), asset, s, new, cls))
            key = (d.isoformat(), asset)
            r2row = r2.get(key)
            r1row = r1.get(key)
            if kept_e is not None and kept_e.get('par_scaled_ids'):
                par_rows.append(key)
            rows.append({'date': d.isoformat(), 'asset_name': asset, 'old_price': fmt(s), 'old_source': 'transaction_observed',
                         'new_price': fmt(new), 'class': cls, 'reason': reason, 'distinct_trades': distinct,
                         'excluded_by_type': ex_str, 'flags': flags, 'observation_date': obs,
                         'old_price_types': old_types(d, asset, s),
                         'round2_class': r2row['class'] if r2row else 'NOT_IN_ROUND2',
                         'round2_new_price': r2row['new_price_A'] if r2row else '',
                         'in_round2': 1 if r2row else 0,
                         'round1_class': r1row[0] if r1row else 'NOT_IN_ROUND1',
                         'round1_recomputed': r1row[1] if r1row else '',
                         'carry_source_par_scaled': 1 if (cls == 'NOW_CARRY_FORWARD' and kept_e is not None
                                                          and kept_e.get('par_scaled_ids')) else 0})
            if cls == 'NOW_CARRY_FORWARD' and kept_e is not None and kept_e.get('par_scaled_ids'):
                carry_par_scaled[0] += 1
        # interpolated rows of the served assets
        est_counts = {'rows': 0, 'trade_price': 0, 'last_traded_date': 0, 'unresolved': 0}
        interp_refused = {}
        interp_reasons = {}
        interp_carry_par_scaled = [0]
        for r_ in interp_served.itertuples(index=False):
            d, asset = r_.d, r_.asset_name
            st = hist.get(asset, {}).get(d)
            if st is not None and st[0] == 'WITHHELD':
                fate, rp, rb, ro, why = 'unresolved', '', '', '', 'ratio_unrecognised'
            elif st is not None and st[0] == 'KEPT':
                fate, rp, rb, ro, why = 'trade_price', fmt(st[1]['price']), 'trade', d.isoformat(), 'trade_median_R1_2'
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
            est.append({'date': d.isoformat(), 'asset_name': asset, 'canonical_price': fmt(r_.price),
                        'canonical_source': r_.source, 'fate': fate, 'r1_price': rp, 'r1_basis': rb,
                        'r1_observation_date': ro, 'reason': why, 'estimated_row': 1})
        est_counts['interp_refused'] = interp_refused
        est_counts['carry_par_scaled_served'] = carry_par_scaled[0]
        est_counts['interp_reasons'] = interp_reasons
        est_counts['carry_par_scaled_interp'] = interp_carry_par_scaled[0]
        return rows, est, classes, {'withheld_served': withheld_served, 'withheld_direct': withheld_direct,
                                    'withheld_via_carry': withheld_via_carry,
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
    with open(os.path.join(a.out, 'BEFORE_AFTER2.csv'), 'wb') as fh:
        fh.write(list_bytes)
    with open(os.path.join(a.out, 'ESTIMATED_ROWS2.csv'), 'wb') as fh:
        fh.write(est_bytes)

    # ---- past-date arm: 20 CHANGED rows, the result for the date from trades on or before that date ----
    past = []
    changed = [r_ for r_ in rows_a if r_['class'] == 'CHANGED'][:20]
    for r_ in changed:
        d = dt.date.fromisoformat(r_['date'])
        asset = r_['asset_name']
        full = hist[asset][d][1]
        frame = df[(df['asset_name'] == asset) & (df['tdate'] <= d)][COLS_READ]
        before = mod.price_for_date(frame, d, A, cands).get(asset)
        day_ids = set(mod._trade_id(v, i) for i, v in enumerate(groups[d]['transaction_id']))
        past.append({'date': r_['date'], 'asset_name': asset,
                     'equal': bool(before is not None and before['price'] == full['price'] and before['trade_ids'] == full['trade_ids']),
                     'ids_on_date_only': bool(set(full['trade_ids']) <= day_ids)})

    # ---- the four classes and the denominator ----
    c = classes_a
    served_n = len(rows_a)
    moved_n = c['CHANGED'] + c['NOW_CARRY_FORWARD']
    movers = sorted(extra_a['movers'], key=lambda x: -x[0])
    # the eight round-2 scale_100x rows, by round 2's own flag
    r2_scale = sorted(k for k, v in r2.items() if 'scale_100x' in v['flags'])
    cur_by_key = {(x['date'], x['asset_name']): x for x in rows_a}
    par_unchanged = sum(1 for k in r2_scale if k in cur_by_key and cur_by_key[k]['class'] == 'UNCHANGED')
    cf_rows = [x for x in rows_a if x['class'] == 'NOW_CARRY_FORWARD']
    tin = sum(1 for x in cf_rows if x['old_price_types'] == 'Transfer In')
    tin_any = sum(1 for x in cf_rows if 'Transfer In' in x['old_price_types'].split('|'))
    cf_with_date = sum(1 for x in cf_rows if x['observation_date'])
    # round 1's UNEXPLAINED rows, and the subset that recomputed to 1.0, each with its amended class and price
    r1_amend = {'UNEXPLAINED': {}, 'RECOMPUTED_1_0': {}}
    r1_amend_rows = []
    for k, (r1cls, r1rec) in sorted(r1.items()):
        if r1cls != 'UNEXPLAINED':
            continue
        is_one = bool(r1rec) and abs(float(r1rec) - 1.0) < 1e-9
        x = cur_by_key.get(k)
        cls_now = x['class'] if x else 'NOT_IN_SERVED_SET'
        r1_amend['UNEXPLAINED'][cls_now] = r1_amend['UNEXPLAINED'].get(cls_now, 0) + 1
        if is_one:
            r1_amend['RECOMPUTED_1_0'][cls_now] = r1_amend['RECOMPUTED_1_0'].get(cls_now, 0) + 1
        r1_amend_rows.append((k[0], k[1], cls_now, x['new_price'] if x else ''))
    rep['round1_unexplained_amended'] = r1_amend
    rep['round1_unexplained_rows'] = sum(r1_amend['UNEXPLAINED'].values())
    rep['round1_recomputed_1_0_rows'] = sum(r1_amend['RECOMPUTED_1_0'].values())

    ests = est_counts_a
    rec = {
        'order': 'BP-c-2',
        'read_at': dt.datetime.now(dt.timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ'),
        'claim': 'measured',
        'calls': [
            'aws s3api get-object --bucket opal-data-bd --key silver/prices/canonical_prices.parquet (ETag %s, LastModified %s)'
            % (a.canonical_etag, a.canonical_modified),
            'aws s3api get-object --bucket opal-data-bd --key silver/bd_assets_dim.parquet',
            'aws s3api list-objects-v2 --bucket opal-data-bd --prefix silver/transactions/ (1,929 keys: 1,928 dated partitions and _README.txt)',
            'aws s3api head-object --bucket opal-data-bd --key silver/transactions/<date>.parquet (1,928 keys, ContentLength and ETag)',
            'aws s3api get-object --bucket opal-data-bd --key silver/transactions/<date>.parquet (only for partitions whose local copy failed verification, see PARTITIONS2.csv)',
        ],
        'amendment': 'R1.2',
        'window': '%s..%s (%d weekday dates)' % (WIN_START.isoformat(), WIN_END.isoformat(), weekdays),
        'served_rows': served_n,
        'classes': {k: c[k] for k in CLASSES},
        'moved': moved_n,
        'prices_differ_from_served': extra_a['moved_diff'],
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
                         'reasons': ests['interp_reasons'], 'assets_with_ratio_refusal': len(ests['interp_refused'])},
        'lookback_keying': {
            'mode': 'trade_date_all_partitions',
            'statement': ('Keyed on trade_date across all %d verified silver/transactions partitions (%s..%s; the file '
                          'holds no key). %d trade dates in the store. Window weekdays with no trade in the store: %s. '
                          'Late-landed rows (file day after trade day): %d, of which %d lag more than one day, in all '
                          'partitions; %d and %d in the 2026 partitions. The 2026-10-14 partition is present at the read and '
                          'holds %d rows dated inside the window, keyed here (sensitivity in REPLAY2.md). Limit: a trade '
                          'dated on a day with no partition, that never landed in a later partition, is not in the store; '
                          'interpolated rows of such a day (2026-10-13) carry the last trade before it.') % (
                len(manifest), rep['floor'], rep['partitions']['last'], len(all_tdates),
                ', '.join(rep['window_trade_dates_absent_from_store']) or 'none',
                stats['late_rows_any'], stats['late_rows_gt1day'],
                stats['late_rows_2026_partitions'], stats['late_rows_2026_partitions_gt1day'],
                stats.get('partition_2026_10_14_rows_dated_in_window', 0))},
        'deterministic': bool(in_process_equal),
        'served_write': False,
        'list_file': 'BEFORE_AFTER2.csv',
        'list_sha256': list_sha,
        'list_md5': list_md5,
        'estimated_list_file': 'ESTIMATED_ROWS2.csv',
        'estimated_list_md5': hashlib.md5(est_bytes).hexdigest(),
        'peer_md5': a.peer_md5,
        'peer_md5_equal': bool(a.peer_md5) and a.peer_md5 == list_md5,
        'past_date_arm': {'sampled': len(past), 'equal': sum(1 for p in past if p['equal']),
                          'ids_on_date_only': sum(1 for p in past if p['ids_on_date_only'])},
        'definitions': {
            'withheld_rows': 'served asset-dates classed NOT_RECOMPUTABLE with reason ratio_unrecognised (direct, or a carry-forward refused because the last trade date is withheld)',
            'par_quoted_rows': 'the eight round-2 rows whose flag carried scale_100x',
            'par_withheld': 'withheld trade rows of Fixed Income assets over the window (all assets, served or not); equals withheld_fi_trade_rows',
            'withheld_assets': 'every asset with a withheld trade row on a window date; served_rows_touched counts the served asset-dates it withholds or refuses to carry',
        },
        'withheld_assets': {k: {'trade_rows': v['trade_rows'], 'ratios': sorted(v['ratios']),
                                'dates': sorted(d_.isoformat() for d_ in v['dates']),
                                'fixed_income': k in cands, 'in_served_set': k in served_assets,
                                'served_rows_touched': len(extra_a['touched'].get(k, set())),
                                'interpolated_rows_refused': ests['interp_refused'].get(k, 0)}
                            for k, v in sorted(withheld_by_asset.items())},
        'withheld_fi_trade_rows': sum(v['trade_rows'] for k, v in withheld_by_asset.items() if k in cands),
        'par_withheld': sum(v['trade_rows'] for k, v in withheld_by_asset.items() if k in cands),
        'movers_top3': [{'asset_name': m[2], 'date': m[1], 'served': m[3], 'new': m[4], 'class': m[5]}
                        for m in movers[:3]],
        'rep': rep,
    }
    with open(os.path.join(a.out, 'REPLAY2.json'), 'w', encoding='utf-8', newline='\n') as fh:
        json.dump(rec, fh, indent=1, sort_keys=True, ensure_ascii=True)
        fh.write('\n')
    print('served=%d classes=%s' % (served_n, json.dumps({k: c[k] for k in CLASSES}, sort_keys=True)))
    print('BEFORE_AFTER2 md5=%s rows=%d estimated=%d deterministic=%s peer_equal=%s'
          % (list_md5, len(rows_a), len(est_a), str(rec['deterministic']).lower(), str(rec['peer_md5_equal']).lower()))
    return 0


if __name__ == '__main__':
    sys.exit(main())
