"""BP-a-3 read-only GAP measurement: every served transaction_observed row of the window, classified.

Reads ONLY the local copies written by gap_fetch.sh (C:/dev/wk-bdprce-r1-3-data/v/, manifest.tsv).
Writes GAP_ROWS.csv into this deliverables folder and prints one summary block (GAP.json is written
from that output). The T1 rule is replicated verbatim from
data/black_diamond/scripts/silver/bd_price_update.py extract_t1_prices (lines 327-344): valid = asset_name
not null, units not null and |units| > 1e-8, market_value not null and != 0; calc_price = |market_value| /
|units|; keep 0 < calc_price < 100000; median per asset_name over all valid rows.

Classification ladder (spec 1b.3; the first that reproduces the served price within tol takes the row):
  EQUAL                          current version of the day's partition, the T1 rule
  EXPLAINED_BY_VERSION_AT_WRITE  the T1 rule over a version of the day's partition (superset of the write-time version)
  EXPLAINED_BY_MULTIDAY_WINDOW   the rule over a contiguous window of 2+ partitions containing the day, read four ways:
                                 per asset or per (asset, trade_date) (the backfill path, bd_price_update.py
                                 lines 511-518), each raw or de-duplicated by transaction_id (keep last)
  EXPLAINED_OTHER                (c1) same-day T1 rule after de-duplication by transaction_id (keep first);
                                 (c2) the JOB 2 observed-price rule (bd_price_update.py extract_observed_prices,
                                 lines 677-706: price column first, CASH excluded) on the day's own partition;
                                 (c3) the median of the price column over the day's rows excluding cash
                                 dividends (transaction_type == 'Dividend'); (c4) the T1 rule on a neighbouring
                                 trade-date partition of the window
  NOT_RECOMPUTABLE               none of the above, and the day's partition holds no valid T1 row for the asset
  UNEXPLAINED                    none of the above

Run with: python -I gap_measure.py
"""
import csv
import datetime
import os

import numpy as np
import pandas as pd

DATA = 'C:/dev/wk-bdprce-r1-3-data/'
VDIR = DATA + 'v/'
DEL = 'C:/dev/wk-bdprce-r1-3/org/missions/D8/ADVI/ADVI_BDPRCE/deliverables/0.9.0_WK_ADVI_BDPRCE~3/'
MAX_UNIT_PRICE = 100_000
WIN_START, WIN_END = datetime.date(2026, 9, 16), datetime.date(2026, 10, 13)
CLASSES = ['EQUAL', 'EXPLAINED_BY_VERSION_AT_WRITE', 'EXPLAINED_BY_MULTIDAY_WINDOW',
           'EXPLAINED_OTHER', 'UNEXPLAINED', 'NOT_RECOMPUTABLE']


def tol(p):
    return 1e-6 * max(1.0, abs(p))


def weekdays_back(end, n):
    out, d = [], end
    while len(out) < n:
        if d.weekday() < 5:
            out.append(d)
        d -= datetime.timedelta(days=1)
    return sorted(out)


WINDOW = [d.isoformat() for d in weekdays_back(WIN_END, 20)]
PRIOR = [d.isoformat() for d in weekdays_back(datetime.date.fromisoformat(WINDOW[0]) - datetime.timedelta(days=1), 20)]
REACH = PRIOR + WINDOW                      # multi-day window reach: 40 weekday dates


def read_manifest():
    rows = []
    with open(DATA + 'manifest.tsv', encoding='utf-8') as fh:
        for line in fh:
            line = line.strip('\r\n')
            if line.strip():
                rows.append(line.split('\t'))
    return rows


def calc_prices(df):
    """(asset_names, T1 validity mask, calc_price), row for row, per the verbatim rule."""
    mv = pd.to_numeric(df['market_value'], errors='coerce').to_numpy(dtype=float)
    un = pd.to_numeric(df['units'], errors='coerce').to_numpy(dtype=float)
    an = df['asset_name'].to_numpy(dtype=object)
    with np.errstate(divide='ignore', invalid='ignore'):
        cp = np.abs(mv) / np.abs(un)
    name_ok = np.array([(a is not None) and not (isinstance(a, float) and np.isnan(a)) for a in an], dtype=bool)
    ok = name_ok & (~np.isnan(un)) & (np.abs(un) > 1e-8) & (~np.isnan(mv)) & (mv != 0)
    ok &= (cp > 0) & (cp < MAX_UNIT_PRICE)
    return an, ok, cp


def t1_median_df(df):
    """Verbatim T1 rule on one frame; returns {asset: median over all valid rows}."""
    if df is None or len(df) == 0:
        return {}
    an, ok, cp = calc_prices(df)
    out = {}
    for a in set(an[ok]):
        out[a] = float(np.median(cp[ok & (an == a)]))
    return out


def day_structures(df):
    """Per partition:
       raw[asset]                  np.array of valid T1 prices, all rows incl. duplicates
       dl[asset] / dfst[asset]     {tid: price-or-None}, last / first occurrence wins
       raw2[(asset, td)]           np.array of valid T1 prices by trade_date (backfill path)
       dd2[(asset, td)]            {tid: price-or-None} by trade_date, last occurrence wins"""
    raw, dl, dfst, raw2, dd2 = {}, {}, {}, {}, {}
    if df is None or len(df) == 0:
        return raw, dl, dfst, raw2, dd2
    an, ok, cp = calc_prices(df)
    tids = df['transaction_id'].astype(str).to_numpy(dtype=object)
    tdates = pd.to_datetime(df['trade_date'], errors='coerce').dt.strftime('%Y-%m-%d').to_numpy(dtype=object)
    for i in range(len(df)):
        a = an[i]
        if a is None or (isinstance(a, float) and np.isnan(a)):
            continue
        val = float(cp[i]) if ok[i] else None
        dl.setdefault(a, {})[tids[i]] = val
        dfst.setdefault(a, {}).setdefault(tids[i], val)
        key = (a, tdates[i])
        dd2.setdefault(key, {})[tids[i]] = val
        if ok[i]:
            raw.setdefault(a, []).append(float(cp[i]))
            raw2.setdefault(key, []).append(float(cp[i]))
    raw = {a: np.array(v, dtype=float) for a, v in raw.items()}
    raw2 = {k: np.array(v, dtype=float) for k, v in raw2.items()}
    return raw, dl, dfst, raw2, dd2


def job2_observed(df):
    """JOB 2 rule (extract_observed_prices): observed = price if price > 0, else market_value / units when
    units != 0 and market_value != 0; CASH/Cash excluded. Returns {(asset, trade_date): {tid: observed}}."""
    px = pd.to_numeric(df['price'], errors='coerce').to_numpy(dtype=float)
    mv = pd.to_numeric(df['market_value'], errors='coerce').to_numpy(dtype=float)
    un = pd.to_numeric(df['units'], errors='coerce').to_numpy(dtype=float)
    has = (~np.isnan(px)) & (px > 0)
    calc = (~has) & (~np.isnan(mv)) & (~np.isnan(un)) & (un != 0) & (mv != 0)
    obs = np.full(len(df), np.nan)
    obs[has] = px[has]
    obs[calc] = mv[calc] / un[calc]
    an = df['asset_name'].to_numpy(dtype=object)
    tids = df['transaction_id'].astype(str).to_numpy(dtype=object)
    tdates = pd.to_datetime(df['trade_date'], errors='coerce').dt.strftime('%Y-%m-%d').to_numpy(dtype=object)
    m = {}
    for i in range(len(df)):
        a = an[i]
        if a is None or (isinstance(a, float) and np.isnan(a)) or a in ('CASH', 'Cash') or np.isnan(obs[i]):
            continue
        m.setdefault((a, tdates[i]), {})[tids[i]] = float(obs[i])
    return m


def price_ex_dividend(df):
    """{asset: np.array of price-column values > 0 over rows whose transaction_type is not 'Dividend'}."""
    out = {}
    if df is None or len(df) == 0:
        return out
    px = pd.to_numeric(df['price'], errors='coerce').to_numpy(dtype=float)
    an = df['asset_name'].to_numpy(dtype=object)
    tt = df['transaction_type'].to_numpy(dtype=object)
    for i in range(len(df)):
        a = an[i]
        if a is None or (isinstance(a, float) and np.isnan(a)) or tt[i] == 'Dividend':
            continue
        if not np.isnan(px[i]) and px[i] > 0:
            out.setdefault(a, []).append(px[i])
    return {a: np.array(v, dtype=float) for a, v in out.items()}


def med_raw(STR, days, asset):
    parts = [STR[x][0][asset] for x in days if x in STR and asset in STR[x][0]]
    if not parts:
        return None
    return float(np.median(np.concatenate(parts)))


def med_dedup(STR, days, asset):
    m = {}
    for x in days:
        if x in STR and asset in STR[x][1]:
            m.update(STR[x][1][asset])
    vals = [v for v in m.values() if v is not None]
    if not vals:
        return None
    return float(np.median(np.array(vals, dtype=float)))


def med_date_raw(STR, days, asset, d):
    parts = [STR[x][3][(asset, d)] for x in days if x in STR and (asset, d) in STR[x][3]]
    if not parts:
        return None
    return float(np.median(np.concatenate(parts)))


def med_date_dedup(STR, days, asset, d):
    m = {}
    for x in days:
        if x in STR and (asset, d) in STR[x][4]:
            m.update(STR[x][4][(asset, d)])
    vals = [v for v in m.values() if v is not None]
    if not vals:
        return None
    return float(np.median(np.array(vals, dtype=float)))


def main():
    man = read_manifest()
    kinds = {}
    for row in man:
        kinds[row[0]] = kinds.get(row[0], 0) + 1
    print('manifest rows by kind', kinds)

    # ---- served rows: canonical object, latest version
    canon = [m for m in man if m[0] == 'canonical_latest'][0]
    c = pd.read_parquet(VDIR + canon[5], columns=['date', 'asset_name', 'ticker', 'price', 'source'])
    c['date'] = pd.to_datetime(c['date']).dt.normalize()
    cw = c[(c['date'] >= pd.Timestamp(WIN_START)) & (c['date'] <= pd.Timestamp(WIN_END))]
    served = cw[cw['source'] == 'transaction_observed'].copy().reset_index(drop=True)
    served['d'] = served['date'].dt.strftime('%Y-%m-%d')
    print('canonical latest', canon[2], canon[1][:8], 'window rows', len(cw), 'sources',
          cw['source'].value_counts().to_dict())
    print('served_rows (transaction_observed, window) =', len(served))
    print('served per date', served.groupby('d').size().to_dict())

    # ---- partitions: every version of each window date (version test); current version of each reach date
    tx_versions = {}
    for kind, key, vid, lm, latest, loc in man:
        if kind == 'tx':
            tx_versions.setdefault(key.split('/')[-1][:10], []).append((lm, vid, latest, loc))
    current = {}
    for d in REACH:
        if d in tx_versions:
            cands = [t for t in tx_versions[d] if t[2] == 'True']
            if cands:
                current[d] = cands[0]
    for kind, key, vid, lm, latest, loc in man:
        if kind == 'tx_prior':
            current[key.split('/')[-1][:10]] = (lm, vid, latest, loc)
    print('reach dates', len(REACH), 'with a current partition', len(current),
          'missing', [d for d in REACH if d not in current])

    RAW_DF, OWN, STR, J2, XD = {}, {}, {}, {}, {}
    for d in REACH:
        if d in current:
            df = pd.read_parquet(VDIR + current[d][3])
            RAW_DF[d] = df
            OWN[d] = t1_median_df(df)
            STR[d] = day_structures(df)
            J2[d] = job2_observed(df)
            XD[d] = price_ex_dividend(df)
    own_first = {d: t1_median_df(RAW_DF[d].drop_duplicates(subset=['transaction_id'], keep='first')) for d in RAW_DF}
    print('current partition rows:', {d: len(RAW_DF[d]) for d in sorted(RAW_DF)})

    version_med = {}
    for d in WINDOW:
        for lm, vid, latest, loc in tx_versions.get(d, []):
            version_med[(d, vid)] = t1_median_df(pd.read_parquet(VDIR + loc))
    print('versions read for the version test:', len(version_med))

    rows_out = []
    cls = {k: 0 for k in CLASSES}
    causes = {}
    span_hist, variant_hist = {}, {}
    overlap_j2_in_b = 0
    for _, r in served.iterrows():
        d, a, p = r['d'], r['asset_name'], float(r['price'])
        own = OWN.get(d, {}).get(a)
        own_s = '' if own is None else own
        if own is not None and abs(own - p) <= tol(p):
            cls['EQUAL'] += 1
            rows_out.append([d, a, p, own, 'EQUAL', 'current:%s' % current[d][1][:8]])
            continue
        # (a) version at write: the T1 rule on every version of the day's partition (superset of write-time)
        hit_a = None
        for lm, vid, latest, loc in tx_versions.get(d, []):
            v = version_med.get((d, vid), {}).get(a)
            if v is not None and abs(v - p) <= tol(p):
                hit_a = (lm, vid)
                break
        if hit_a is not None:
            cls['EXPLAINED_BY_VERSION_AT_WRITE'] += 1
            rows_out.append([d, a, p, own_s, 'EXPLAINED_BY_VERSION_AT_WRITE', 'version:%s@%s' % (hit_a[1][:8], hit_a[0])])
            continue
        # (b) multi-day window containing d (2+ partitions of REACH)
        i = REACH.index(d)
        best = None
        for s_ in range(0, i + 1):
            for e_ in range(i, len(REACH)):
                if e_ == s_:
                    continue
                days = REACH[s_:e_ + 1]
                hit = []
                for label, m in (('asset-raw', med_raw(STR, days, a)),
                                 ('asset-dedup', med_dedup(STR, days, a)),
                                 ('date-raw', med_date_raw(STR, days, a, d)),
                                 ('date-dedup', med_date_dedup(STR, days, a, d))):
                    if m is not None and abs(m - p) <= tol(p):
                        hit.append(label)
                if hit:
                    key = (e_ - s_, s_)
                    if best is None or key < best[0]:
                        best = (key, days[0], days[-1], '+'.join(hit))
        if best is not None:
            cls['EXPLAINED_BY_MULTIDAY_WINDOW'] += 1
            span_hist[best[0][0] + 1] = span_hist.get(best[0][0] + 1, 0) + 1
            variant_hist[best[3]] = variant_hist.get(best[3], 0) + 1
            if d in J2 and (a, d) in J2[d]:
                vals = list(J2[d][(a, d)].values())
                if vals and abs(float(np.median(vals)) - p) <= tol(p):
                    overlap_j2_in_b += 1
            rows_out.append([d, a, p, own_s, 'EXPLAINED_BY_MULTIDAY_WINDOW',
                             'window:%s..%s:%s' % (best[1], best[2], best[3])])
            continue
        # (c1) same-day T1 rule after de-duplication by transaction_id (keep first)
        of = own_first.get(d, {}).get(a)
        if of is not None and abs(of - p) <= tol(p):
            cls['EXPLAINED_OTHER'] += 1
            causes.setdefault('c1_same_day_transaction_id_dedup_keep_first', []).append((d, a))
            rows_out.append([d, a, p, own_s, 'EXPLAINED_OTHER', 'c1:dedup_day:%s' % d])
            continue
        # (c2) JOB 2 observed-price rule on the day's own partition
        vals2 = list(J2.get(d, {}).get((a, d), {}).values())
        if vals2 and abs(float(np.median(np.array(vals2, dtype=float))) - p) <= tol(p):
            cls['EXPLAINED_OTHER'] += 1
            causes.setdefault('c2_job2_observed_price_rule_own_day', []).append((d, a))
            rows_out.append([d, a, p, own_s, 'EXPLAINED_OTHER', 'c2:job2_own_day:%s' % d])
            continue
        # (c3) median of the price column over the day's rows excluding cash dividends
        xs = XD.get(d, {}).get(a)
        if xs is not None and len(xs) and abs(float(np.median(xs)) - p) <= tol(p):
            cls['EXPLAINED_OTHER'] += 1
            causes.setdefault('c3_price_column_median_excluding_cash_dividends', []).append((d, a))
            rows_out.append([d, a, p, own_s, 'EXPLAINED_OTHER', 'c3:price_ex_dividend:%s' % d])
            continue
        # (c4) T1 rule on a neighbouring trade-date partition of the window
        shift = None
        for x in REACH:
            if x == d or x not in OWN:
                continue
            mx = OWN[x].get(a)
            if mx is not None and abs(mx - p) <= tol(p):
                shift = (x, 'raw')
                break
            mxf = own_first[x].get(a) if x in own_first else None
            if mxf is not None and abs(mxf - p) <= tol(p):
                shift = (x, 'dedup')
                break
        if shift is not None:
            cls['EXPLAINED_OTHER'] += 1
            causes.setdefault('c4_neighbouring_trade_date_partition', []).append((d, a, shift[0]))
            rows_out.append([d, a, p, own_s, 'EXPLAINED_OTHER', 'c4:partition:%s:%s' % (shift[0], shift[1])])
            continue
        if own is None:
            cls['NOT_RECOMPUTABLE'] += 1
            rows_out.append([d, a, p, '', 'NOT_RECOMPUTABLE', 'partition:%s:no_valid_row' % d])
        else:
            cls['UNEXPLAINED'] += 1
            rows_out.append([d, a, p, own, 'UNEXPLAINED', 'none'])

    total = sum(cls.values())
    print('CLASSES', cls)
    print('sum of classes', total, 'served_rows', len(served), 'partition check', total == len(served))
    print('EXPLAINED_OTHER causes', {k: len(v) for k, v in causes.items()})
    print('multi-day minimal window span (partitions) histogram', dict(sorted(span_hist.items())))
    print('multi-day minimal-window variant histogram', dict(sorted(variant_hist.items())))
    print('multi-day rows also reproduced by the own-day JOB 2 rule (overlap, not reassigned)', overlap_j2_in_b)

    unexp = [r for r in rows_out if r[4] == 'UNEXPLAINED']
    rec = []
    for r in unexp:
        dab = abs(r[2] - r[3])
        rec.append((dab, dab / max(1.0, abs(r[3])), r))
    rec.sort(key=lambda t: -t[0])
    print('UNEXPLAINED rows', len(unexp))
    for dab, drel, r in rec[:6]:
        print('  %s %s served=%.6f recomputed=%.6f abs=%.6f rel=%.6f' % (r[0], r[1], r[2], r[3], dab, drel))
    if rec:
        print('UNEXPLAINED max abs diff %.6f ; max rel diff %.6f' % (max(t[0] for t in rec), max(t[1] for t in rec)))
    print('UNEXPLAINED by date', {k: v for k, v in sorted(
        {d: sum(1 for r in unexp if r[0] == d) for d in set(r[0] for r in unexp)}.items())})

    with open(DEL + 'GAP_ROWS.csv', 'w', encoding='utf-8', newline='') as fh:
        w = csv.writer(fh, lineterminator='\n')
        w.writerow(['date', 'asset_name', 'served_price', 'recomputed_price', 'class', 'evidence_ref'])
        for r in rows_out:
            rc = '' if r[3] in ('', None) else '%.10g' % r[3]
            w.writerow([r[0], r[1], '%.10g' % r[2], rc, r[4], r[5]])
    print('GAP_ROWS.csv bytes', os.path.getsize(DEL + 'GAP_ROWS.csv'), 'rows', len(rows_out))
    print('CAUSE_ROWS', {k: len(v) for k, v in causes.items()})


if __name__ == '__main__':
    main()
