"""TO-SC-e111b read-only census helper (0.7.0_AE_CloudOps~DELL1). Run from the repo root with python -I.

  python -I e111_legp.py gold <out.json>     every IsLatest key under s3://opal-data-bd/code/gold/ with ETag and VersionId; page and key counts printed
  python -I e111_legp.py table <out.json>    etf-classifications: the 13 seeded keys present, the 9 held-out absent, first 200 sorted keys with last_updated
  python -I e111_legp.py diff <a.json> <b.json>   keys added, removed, or with a different ETag or VersionId between two gold census files
"""
from __future__ import annotations

import json
import os
import sys

REGION = 'us-east-1'
BUCKET = 'opal-data-bd'
PREFIX = 'code/gold/'
ROOT = os.getcwd()
PLAN = os.path.join(ROOT, 'org', 'missions', 'D8', 'MDPF', 'MDPF_SECCLASS', 'deliverables', '0.9.0_WK_MDPF_SECCLASS~97', 'SEED22_PLAN.json')


def gold(out: str) -> int:
    import boto3
    s3 = boto3.client('s3', region_name=REGION)
    pages, versions, markers, latest = 0, 0, 0, {}
    for page in s3.get_paginator('list_object_versions').paginate(Bucket=BUCKET, Prefix=PREFIX):
        pages += 1
        for v in page.get('Versions', []):
            versions += 1
            if v['IsLatest']:
                latest[v['Key']] = {'ETag': v['ETag'].strip('"'), 'VersionId': v['VersionId'], 'LastModified': v['LastModified'].isoformat(), 'Size': v['Size']}
        for m in page.get('DeleteMarkers', []):
            markers += 1
            if m['IsLatest']:
                latest[m['Key']] = {'DELETE_MARKER': True, 'VersionId': m['VersionId']}
    doc = {'claim': 'measured', 'bucket': BUCKET, 'prefix': PREFIX, 'pages': pages, 'versions_seen': versions, 'delete_markers_seen': markers,
           'latest_keys': len(latest), 'keys': dict(sorted(latest.items()))}
    with open(out, 'w', encoding='utf-8') as f:
        json.dump(doc, f, indent=1)
    print('GOLD-CENSUS pages=%d versions_seen=%d delete_markers_seen=%d latest_keys=%d -> %s' % (pages, versions, markers, len(latest), out))
    return 0


def table(out: str) -> int:
    import boto3
    plan = json.load(open(PLAN, encoding='utf-8'))
    seeded = [e['ticker'] for e in plan['planned']]
    held = [e['ticker'] for e in plan['seed_pending']]
    tbl = boto3.resource('dynamodb', region_name=REGION).Table('etf-classifications')
    items, pages = [], 0
    kw = {'ProjectionExpression': 'ticker, last_updated, asset_class'}
    while True:
        r = tbl.scan(**kw)
        pages += 1
        items.extend(r['Items'])
        if 'LastEvaluatedKey' not in r:
            break
        kw['ExclusiveStartKey'] = r['LastEvaluatedKey']
    keys = {i['ticker'] for i in items}
    items.sort(key=lambda i: i['ticker'])
    doc = {'claim': 'measured', 'table': 'etf-classifications', 'scan_pages': pages, 'item_count': len(items),
           'seeded_expected': len(seeded), 'seeded_present': sorted(t for t in seeded if t in keys),
           'held_expected': len(held), 'held_absent': sorted(t for t in held if t not in keys),
           'held_present': sorted(t for t in held if t in keys),
           'first200': [{'ticker': i['ticker'], 'last_updated': str(i.get('last_updated'))} for i in items[:200]]}
    with open(out, 'w', encoding='utf-8') as f:
        json.dump(doc, f, indent=1)
    print('TABLE-STATE scan_pages=%d items=%d seeded_present=%d/%d held_absent=%d/%d first200=%d -> %s' % (
        pages, len(items), len(doc['seeded_present']), len(seeded), len(doc['held_absent']), len(held), len(doc['first200']), out))
    return 0


def diff(a: str, b: str) -> int:
    ka = json.load(open(a, encoding='utf-8'))['keys']
    kb = json.load(open(b, encoding='utf-8'))['keys']
    added = sorted(set(kb) - set(ka))
    removed = sorted(set(ka) - set(kb))
    moved = sorted(k for k in set(ka) & set(kb) if (ka[k].get('ETag'), ka[k].get('VersionId')) != (kb[k].get('ETag'), kb[k].get('VersionId')))
    print('GOLD-DIFF before=%d after=%d added=%s removed=%s moved=%s' % (len(ka), len(kb), added, removed, moved))
    return 0


if __name__ == '__main__':
    a = sys.argv
    if a[1] == 'gold':
        sys.exit(gold(a[2]))
    if a[1] == 'table':
        sys.exit(table(a[2]))
    sys.exit(diff(a[2], a[3]))
