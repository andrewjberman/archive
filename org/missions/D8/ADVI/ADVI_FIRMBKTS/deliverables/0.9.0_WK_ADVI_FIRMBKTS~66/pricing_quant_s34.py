"""FB-h-7 S34: version comparison of the served objects for trade dates 2026-08-20..23.

Reads the local copies fetched by fetch_versions.sh (S3 get-object --version-id) and the
version manifest ver_manifest.tsv (from list-object-versions). Read-only.
Run with: python -I pricing_quant_s34.py
"""
import hashlib
import io
import json
import os

import pandas as pd

DATA = 'C:/dev/wk-firmbkts-66-data'
os.chdir(DATA)

KEYS = []
for d in ['2026-08-20', '2026-08-21', '2026-08-22', '2026-08-23']:
    for p in ['silver/transactions', 'silver/prices', 'gold/canonical/account_gains']:
        KEYS.append(f'{p}/{d}.parquet')


def content_hash(path):
    """Two hashes: raw bytes, and the decoded table content (row hashes, column names, dtypes)."""
    raw = open(path, 'rb').read()
    sha_bytes = hashlib.sha256(raw).hexdigest()
    df = pd.read_parquet(io.BytesIO(raw))
    rowh = pd.util.hash_pandas_object(df, index=False).values.tobytes()
    meta = json.dumps([list(map(str, df.columns)), list(map(str, df.dtypes))]).encode()
    sha_content = hashlib.sha256(rowh + meta).hexdigest()
    return sha_bytes, sha_content, int(len(df))


def main():
    versions = {}
    for line in open('ver_manifest.tsv', encoding='utf-8').read().splitlines():
        key, vid, lm, loc = line.split('\t')
        sb, sc, n = content_hash(loc)
        versions.setdefault(key, []).append({'lm': lm, 'vid': vid, 'bytes': sb, 'content': sc, 'rows': n})
    out = {'objects': [], 'versions_fetched': sum(len(v) for v in versions.values())}
    changed_cal = changed_bytes = changed_alt = 0
    for key in KEYS:
        vs = sorted(versions.get(key, []), key=lambda v: v['lm'])
        base = [v for v in vs if v['lm'][:10] >= '2026-08-24']
        base = base[0] if base else None
        after_cal = [v for v in vs if v['lm'][:10] >= '2026-09-03']
        after_alt = [v for v in vs if v['lm'] >= '2026-09-02T00:00:00']
        def differs(group, field):
            if base is None:
                return None
            return any(v[field] != base[field] for v in group)
        rec = {
            'key': key,
            'versions_total': len(vs),
            'versions_before_0823': sum(1 for v in vs if v['lm'][:10] < '2026-08-24'),
            'base_version_lm': base['lm'] if base else None,
            'versions_after_0902_calendar': len(after_cal),
            'changed_calendar_content': differs(after_cal, 'content'),
            'changed_calendar_bytes': differs(after_cal, 'bytes'),
            'changed_instant_content': differs(after_alt, 'content'),
            'versions_after_0902_instant': len(after_alt),
        }
        out['objects'].append(rec)
        if rec['changed_calendar_content']:
            changed_cal += 1
        if rec['changed_calendar_bytes']:
            changed_bytes += 1
        if rec['changed_instant_content']:
            changed_alt += 1
    out['summary'] = {'objects_compared': len(KEYS), 'changed_calendar_content': changed_cal,
                      'changed_calendar_bytes': changed_bytes, 'changed_instant_content': changed_alt}
    print(json.dumps(out, indent=2))


if __name__ == '__main__':
    main()
