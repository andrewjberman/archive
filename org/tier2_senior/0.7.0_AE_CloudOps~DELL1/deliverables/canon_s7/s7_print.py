"""ADHOC.canon-r11-global-axis-deploy read-only print/compare helper (0.7.0_AE_CloudOps~DELL1). Run with python -I.

  python -I s6_print.py print <label> <out.json>      the order's (a)/(d) reads: function, package object, 16 latest-date served objects,
                                                      staged gold/mdpf_revamp keys, control key, tax stores, emitter, schedule, newest manifest
  python -I s6_print.py compare <before.json> <after.json>
Prints counts and hashes only; no body is printed.
"""
from __future__ import annotations

import hashlib
import json
import sys
from datetime import datetime, timezone

import boto3

REGION = 'us-east-1'
ASSETS = 'opal-data-assets'
SCOPES = ['49financial', 'inflection', 'cottonwood', 'global']
TYPES = ['account-distribution', 'aggregate-aua-timeseries', 'aum-metrics', 'category-views']
FN = 'mdpf-gold-lambda'
EMITTER = 'opal-assets-daily-emitter'
PKG_KEY = 'portal/gold/mdpf/_code/mdpf-gold-lambda.zip'
CONTROL = ('opal-data-mdpf', 'mdpf/global/state/taxsma_control/current.json')
STORES = [
    ('opal-data-49financial', 'mdpf/49financial/state/taxsma_membership/dispositions.json'),
    ('opal-data-49financial', 'mdpf/49financial/gold/taxsma_assets/date=2026-10-16/data.parquet'),
    ('opal-data-cottonwood', 'mdpf/cottonwood/state/taxsma_membership/dispositions.json'),
    ('opal-data-cottonwood', 'mdpf/cottonwood/gold/taxsma_assets/date=2026-10-16/data.parquet'),
]

s3 = boto3.client('s3', region_name=REGION)
lam = boto3.client('lambda', region_name=REGION)


def meta(bucket: str, key: str, body: bool = False) -> dict:
    r = s3.head_object(Bucket=bucket, Key=key)
    out = {'bucket': bucket, 'key': key, 'etag': r['ETag'], 'version': r.get('VersionId'),
           'lastmod': r['LastModified'].strftime('%Y-%m-%dT%H:%M:%SZ'), 'size': r['ContentLength']}
    if body:
        out['sha256'] = hashlib.sha256(s3.get_object(Bucket=bucket, Key=key)['Body'].read()).hexdigest()
    return out


def list_keys(bucket: str, prefix: str) -> list:
    keys = []
    for page in s3.get_paginator('list_objects_v2').paginate(Bucket=bucket, Prefix=prefix):
        keys.extend(o['Key'] for o in page.get('Contents', []))
    return keys


def do_print(label: str, out: str) -> int:
    d = {'label': label, 'at': datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ'), 'claim': 'measured'}
    cfg = lam.get_function_configuration(FunctionName=FN)
    d['function'] = {'CodeSha256': cfg['CodeSha256'], 'LastModified': cfg['LastModified'], 'LastUpdateStatus': cfg.get('LastUpdateStatus'),
                     'MDPF_GOLD_COMMIT': cfg['Environment']['Variables'].get('MDPF_GOLD_COMMIT'), 'MemorySize': cfg['MemorySize'],
                     'Timeout': cfg['Timeout'], 'env_keys': sorted(cfg['Environment']['Variables'])}
    d['env_sha256'] = hashlib.sha256(json.dumps(cfg['Environment']['Variables'], sort_keys=True).encode()).hexdigest()
    ecfg = lam.get_function_configuration(FunctionName=EMITTER)
    d['emitter'] = {'CodeSha256': ecfg['CodeSha256'], 'LastModified': ecfg['LastModified']}
    d['package_object'] = meta(ASSETS, PKG_KEY)
    served, dens = [], {}
    for sc in SCOPES:
        for ty in TYPES:
            pre = 'portal/gold/mdpf/%s/%s/' % (sc, ty)
            ks = sorted(k for k in list_keys(ASSETS, pre) if k.endswith('.json'))
            dens[pre] = len(ks)
            served.append(meta(ASSETS, ks[-1], body=True))
    d['served'] = served
    d['served_denominators'] = dens
    staged = [meta(ASSETS, k) for k in sorted(list_keys(ASSETS, 'gold/mdpf_revamp/'))]
    d['state_keys'] = staged
    d['staged_denominator'] = len(staged)
    d['control_key'] = meta(CONTROL[0], CONTROL[1], body=True)
    d['tax_stores'] = [meta(b, k) for b, k in STORES]
    scd = boto3.client('scheduler', region_name=REGION).get_schedule(Name='mdpf-scheduled-floor', GroupName='default')
    d['schedule'] = {'expr': scd['ScheduleExpression'], 'group': 'default', 'input': scd['Target']['Input'], 'state': scd['State']}
    mks = sorted(k for k in list_keys(ASSETS, 'portal/gold/mdpf/_manifests/') if k.endswith('.json'))
    d['manifest_key'] = mks[-1]
    d['manifest_count'] = len(mks)
    run = json.loads(s3.get_object(Bucket=ASSETS, Key=mks[-1])['Body'].read()).get('run', {})
    d['manifest_run'] = {k: run.get(k) for k in ('data_as_of', 'expected_frontier', 'a4_objects_built', 'a4_expected', 'code', 'trigger')}
    d['workbook_snapshots'] = {}
    for tier in ('bronze', 'silver'):
        ks = list_keys(ASSETS, 'gateway/global/%s/taxsma_workbook/' % tier)
        d['workbook_snapshots'][tier] = {'count': len(ks)}
    with open(out, 'w', encoding='utf-8') as f:
        json.dump(d, f, indent=1)
    print('PRINT %s at %s: CodeSha256=%s commit=%s pkgVersion=%s served=%d staged=%d control=%s stores=%d emitter=%s manifest=%s -> %s' % (
        label, d['at'], d['function']['CodeSha256'], d['function']['MDPF_GOLD_COMMIT'], d['package_object']['version'], len(served), len(staged),
        d['control_key']['version'][:8], len(d['tax_stores']), d['emitter']['CodeSha256'][:10], d['manifest_key'], out))
    return 0


def _idx(rows: list) -> dict:
    return {(r['bucket'], r['key']): (r['version'], r['etag'], r.get('sha256')) for r in rows}


def compare(a: str, b: str) -> int:
    x = json.load(open(a, encoding='utf-8'))
    y = json.load(open(b, encoding='utf-8'))
    for name in ('served', 'state_keys', 'tax_stores'):
        ia, ib = _idx(x[name]), _idx(y[name])
        changed = sorted(k[1] for k in set(ia) & set(ib) if ia[k] != ib[k])
        print('== %s: before %d after %d same keys %s unchanged %d changed %d %s' % (
            name, len(ia), len(ib), set(ia) == set(ib), len(set(ia) & set(ib)) - len(changed), len(changed), changed[:5]))
        if set(ia) != set(ib):
            print('   added', sorted(k[1] for k in set(ib) - set(ia))[:5], 'removed', sorted(k[1] for k in set(ia) - set(ib))[:5])
    ca, cb = x['control_key'], y['control_key']
    print('== control: unchanged %s' % ((ca['version'], ca['etag']) == (cb['version'], cb['etag'])))
    print('emitter equal %s | manifest key equal %s | schedule input equal %s' % (
        x['emitter'] == y['emitter'], x['manifest_key'] == y['manifest_key'], x['schedule'] == y['schedule']))
    print('workbook counts', {t: (x['workbook_snapshots'][t]['count'], y['workbook_snapshots'][t]['count']) for t in x['workbook_snapshots']})
    print('function', x['function']['CodeSha256'][:12], '->', y['function']['CodeSha256'][:12], '| commit', x['function']['MDPF_GOLD_COMMIT'][:10], '->', y['function']['MDPF_GOLD_COMMIT'][:10])
    return 0


if __name__ == '__main__':
    a = sys.argv
    sys.exit(do_print(a[2], a[3]) if a[1] == 'print' else compare(a[2], a[3]))
