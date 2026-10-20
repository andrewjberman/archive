"""Read-only census of every vendor silver table: catalogued rows (gateway DATA_CATALOG) plus named live extras.
Per prefix: object count, parquet count, partition count, first/newest partition, newest LastModified,
and the column schema of the newest-partition parquet (footer read only)."""
import json
import re
import sys
import boto3
import yaml
import pyarrow.fs as pafs
import pyarrow.parquet as pq

CAT = sys.argv[1]
OUT = sys.argv[2]
V = ('orion/', 'eclipse/', 'smartx/', 'schwab/', 'blackdiamond/', 'commonwealth/')
d = yaml.safe_load(open(CAT, encoding='ascii'))
targets = []
for sec, v in d.items():
    if isinstance(v, list):
        for r in v:
            if isinstance(r, dict) and r.get('prefix') and r.get('bucket') and r.get('table') and not r.get('retired'):
                p, a = str(r['prefix']), str(r.get('address') or '')
                if p.startswith(V) or a.startswith(V):
                    targets.append({'src': 'catalog', 'bucket': r['bucket'], 'prefix': p, 'address': a or None, 'table': r['table']})
EXTRA = [('opal-data-bd', 'silver/' + t + '/') for t in ('assets', 'prices', 'realized', 'transactions_enriched')] + \
        [('opal-data-inf', 'silver/' + t + '/') for t in ('accounts_dim', 'api_dims', 'assets_v2', 'eclipse', 'meta',
                                                          'orion-rest/transactions', 'orion-rest/performance_weekly',
                                                          'performance', 'performance_dim', 'prices', 'transactions')]
for b, p in EXTRA:
    targets.append({'src': 'live-extra', 'bucket': b, 'prefix': p, 'address': None, 'table': p.rstrip('/').split('/')[-1]})

s3 = boto3.client('s3')
fs = pafs.S3FileSystem(region='us-east-1')
DP = re.compile(r'(?:^|/)(?:date=)?(\d{4}-\d{2}-\d{2})(?:/|\.parquet$)')
for t in targets:
    n = npq = 0
    newest_lm = None
    parts = {}
    for page in s3.get_paginator('list_objects_v2').paginate(Bucket=t['bucket'], Prefix=t['prefix']):
        for o in page.get('Contents', []):
            n += 1
            k = o['Key']
            if newest_lm is None or o['LastModified'] > newest_lm:
                newest_lm = o['LastModified']
            if k.endswith('.parquet'):
                npq += 1
                m = DP.search(k[len(t['prefix']):])
                if m:
                    parts.setdefault(m.group(1), []).append(k)
    t.update({'objects': n, 'parquet': npq, 'partitions': len(parts),
              'first_partition': min(parts) if parts else None, 'newest_partition': max(parts) if parts else None,
              'newest_modified_utc': newest_lm.astimezone().astimezone(__import__('datetime').timezone.utc).isoformat() if newest_lm else None})
    key = None
    if parts:
        key = sorted(parts[max(parts)])[-1]
    elif npq:
        for page in s3.get_paginator('list_objects_v2').paginate(Bucket=t['bucket'], Prefix=t['prefix']):
            ks = [o['Key'] for o in page.get('Contents', []) if o['Key'].endswith('.parquet')]
            if ks:
                key = ks[-1]
                break
    t['schema_key'] = key
    if key:
        try:
            with fs.open_input_file('%s/%s' % (t['bucket'], key)) as f:
                pf = pq.ParquetFile(f)
                t['rows'] = pf.metadata.num_rows
                t['columns'] = ['%s:%s' % (fld.name, fld.type) for fld in pf.schema_arrow]
        except Exception as e:
            t['schema_error'] = '%s: %s' % (type(e).__name__, str(e)[:200])
    print('OK:', t['bucket'], t['prefix'], n, t['newest_partition'], file=sys.stderr, flush=True)
json.dump(targets, open(OUT, 'w', encoding='utf-8'), indent=1, default=str)
print('census rows:', len(targets))
