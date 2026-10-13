"""BP-a-3 read-only manifest: which served object versions the GAP measurement reads.

Input: the three `aws s3api list-object-versions` listings written by gap_fetch.sh (TSV: key, version id,
LastModified, IsLatest, Size). Output: manifest.tsv (kind, key, version id, LastModified, IsLatest, local name).
Kinds: daily (every version of silver/prices/<date>.parquet, window dates); tx (every version of
silver/transactions/<date>.parquet, window dates); tx_prior (the current version of the 20 weekday partitions
before the window, the multi-day window reach); canonical_latest (the current canonical object);
canonical_probe (three earlier canonical versions of 2026-10-13, to date the 1,610 count).
Reads only; writes only under C:/dev/wk-bdprce-r1-3-data/ (outside the checkout).
Run with: python -I gap_manifest.py
"""
import datetime

DATA = 'C:/dev/wk-bdprce-r1-3-data/'
PROBE_LM = ['2026-10-13T04:03:42', '2026-10-13T09:49:48', '2026-10-13T12:47:50']


def window_days(end, n=20):
    out = []
    d = end
    while len(out) < n:
        if d.weekday() < 5:
            out.append(d)
        d -= datetime.timedelta(days=1)
    return sorted(out)


def read_listing(name):
    rows = []
    with open(DATA + name, encoding='utf-8') as fh:
        for line in fh:
            line = line.strip('\r\n')
            if line.strip():
                rows.append(line.split('\t'))
    return rows


def main():
    days = window_days(datetime.date(2026, 10, 13))
    wset = {d.isoformat() for d in days}
    prior = {d.isoformat() for d in window_days(days[0] - datetime.timedelta(days=1))}
    print('window %s..%s n=%d; prior n=%d' % (days[0], days[-1], len(days), len(prior)))
    prices = read_listing('versions_silver_prices_.txt')
    txs = read_listing('versions_silver_transactions_.txt')
    canon = read_listing('versions_canonical.txt')
    out = []
    for r in prices:
        key = r[0]
        base = key.split('/')[-1]
        if key.startswith('silver/prices/') and base.endswith('.parquet') and base[:10] in wset:
            out.append(('daily', key, r[1], r[2], r[3]))
    for r in txs:
        key = r[0]
        base = key.split('/')[-1]
        if not (key.startswith('silver/transactions/') and base.endswith('.parquet')):
            continue
        if base[:10] in wset:
            out.append(('tx', key, r[1], r[2], r[3]))
        elif base[:10] in prior and r[3] == 'True':
            out.append(('tx_prior', key, r[1], r[2], r[3]))
    for r in canon:
        if r[3] == 'True':
            out.append(('canonical_latest', r[0], r[1], r[2], r[3]))
        elif any(r[2].startswith(p) for p in PROBE_LM):
            out.append(('canonical_probe', r[0], r[1], r[2], r[3]))
    lines = []
    for kind, key, vid, lm, latest in out:
        base = key.split('/')[-1]
        stem = base[:-len('.parquet')]
        local = ('%s__%s__%s.parquet' % (kind, stem, vid)).replace('/', '_')
        lines.append('\t'.join([kind, key, vid, lm, latest, local]))
    with open(DATA + 'manifest.tsv', 'w', encoding='utf-8', newline='\n') as fh:
        fh.write('\n'.join(lines) + '\n')
    counts = {}
    for row in out:
        counts[row[0]] = counts.get(row[0], 0) + 1
    print('manifest rows', len(out), counts)


if __name__ == '__main__':
    main()
