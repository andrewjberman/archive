"""code/gold/ census (MDPF_SECCLASS TO-SC-e102b, 0.7.0_AE_CloudOps~SC1). Read-only.

  python -I e102_census.py snap <out.json>          every IsLatest key under s3://opal-data-bd/code/gold/ with ETag, VersionId
  python -I e102_census.py cmp <before> <after>      MOVED / ADDED / GONE; rc 0 only when MOVED is exactly [C_06] and ADDED = GONE = 0
Pages and key counts are printed; pagination is counted client side.
"""
from __future__ import annotations

import json
import sys
from datetime import datetime, timezone

import boto3

BUCKET = 'opal-data-bd'
PREFIX = 'code/gold/'
ONLY = 'code/gold/C_06.client_mix_timeseries.py'


def snap(out: str) -> int:
    s3 = boto3.client('s3')
    keys: dict = {}
    pages = 0
    for page in s3.get_paginator('list_object_versions').paginate(Bucket=BUCKET, Prefix=PREFIX):
        pages += 1
        for v in page.get('Versions', []):
            if v['IsLatest']:
                keys[v['Key']] = {'ETag': v['ETag'].strip('"'), 'VersionId': v['VersionId'], 'Size': v['Size'],
                                  'LastModified': v['LastModified'].isoformat()}
    doc = {'taken_utc': datetime.now(timezone.utc).isoformat(), 'bucket': BUCKET, 'prefix': PREFIX,
           'pages': pages, 'total_keys': len(keys), 'keys': keys}
    with open(out, 'w', encoding='utf-8') as f:
        json.dump(doc, f, indent=1, sort_keys=True)
    print(f'census {out}: keys={len(keys)} pages={pages} taken={doc["taken_utc"]}')
    return 0


def cmp(b: str, a: str) -> int:
    B = json.load(open(b, encoding='utf-8'))['keys']
    A = json.load(open(a, encoding='utf-8'))['keys']
    moved = sorted(k for k in set(A) & set(B) if A[k]['ETag'] != B[k]['ETag'])
    added = sorted(set(A) - set(B))
    gone = sorted(set(B) - set(A))
    print(f'before={len(B)} after={len(A)} MOVED={moved} ADDED={added} GONE={gone}')
    ok = moved == [ONLY] and not added and not gone
    print('CENSUS-OK only C_06 moved' if ok else 'CENSUS-STOP something other than C_06 moved')
    return 0 if ok else 1


if __name__ == '__main__':
    if sys.argv[1] == 'snap':
        sys.exit(snap(sys.argv[2]))
    sys.exit(cmp(sys.argv[2], sys.argv[3]))
