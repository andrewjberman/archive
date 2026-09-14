"""DRIVE_YANG_GENERATORS_RECORDED_EVENTS -- POSN_ASTTAX.TO-V1-1 V1-AC11 (THIRD AMENDMENT).

WHAT THIS ACT IS, and what it deliberately is NOT. The re-cut criterion drives the
served refresh PER PRODUCER: the two generators this cell deployed are invoked
DIRECTLY, once each, in order -- yang-generate-positioning, then
yang-generate-allocation-summary -- each with the event the STATE MACHINE passed it
on the last execution that ran it, and then the pipeline's own
yang-invalidate-cloudfront with ITS recorded event. The STATE MACHINE IS NEVER
STARTED (row POSN_ASTTAX-Z-W19-S8, disarmed by the issuer as Z-S94): it consumes its
own input -- 3 of 3 objects absent -- and its write set of 28 Task states, an S3
delete and a CDN invalidation exceeds the two signed keys.

THE SIGN-OFF THIS ACT RUNS UNDER, cited by path@commit and re-read by the script:
  org/missions/D4/POSN/POSN_ASTTAX/ledger/NEVER_WIDEN_ROUND5_COO_HALF.md
  org/missions/D4/POSN/POSN_ASTTAX/ledger/NEVER_WIDEN_ROUND5_CTO_HALF.md
The COO half's R1 AMENDMENT "The act" bullet (amended ~21:1xZ) is the sign-off for
exactly this act; the CTO half's R1 AMENDMENT ~20:0xZ names "invokes, once each and
in dependency order" the producers.

THE EVENT IS RECORDED, NEVER HAND-WRITTEN. The payload sent to each function is the
RAW input STRING bytes of the LambdaFunctionScheduled event recorded in
get-execution-history of YangDataPipeline:20260911_v1-1c95bba7 -- not a re-serialised
dict. The cached history (.scratch/sfn_history.json) is re-read LIVE from Step
Functions and the two copies are compared by sha256 per event, so the GRAIN of the
claim "the recorded event" is measured rather than asserted.

BRANCH B (STOP, row, nothing further): any invoke that fails or carries a
FunctionError; a served head that does not move; the three classes not at an explicit
zero; membership differing from the pre-deploy read; ANY diff class OTHER non-empty;
allocation_summary.json differing beyond generated_at; ANY OTHER key under
json/positioning/ whose LastModified moves between the two list-objects reads. The
served keys are versioned and the prior VersionIds are printed FIRST -- they are the
restore.

Usage: timeout 1800 python org/missions/D4/POSN/POSN_ASTTAX/deliverables/0.9.0_WK_POSN_ASTTAX~19/drive_yang_generators_recorded_events.py
Exit codes: 0 = every bar met; 2 = REFUSED on a measured premise (nothing invoked);
3 = BRANCH B after an invoke (STOP, row).
"""
import datetime
import gzip
import hashlib
import json
import subprocess

import boto3
from botocore.config import Config

REGION = 'us-east-1'
ACCOUNT = '313476888478'
EXECUTION_ARN = ('arn:aws:states:%s:%s:execution:YangDataPipeline:20260911_v1-1c95bba7'
                 % (REGION, ACCOUNT))
HISTORY_CACHE = '.scratch/sfn_history.json'

SERVED_BUCKET = 'opal-data-portal-v2'
POS_KEY = 'json/positioning/positioning_data.json'
ALLOC_KEY = 'json/positioning/allocation_summary.json'
PREFIX = 'json/positioning/'
SIGNED_KEYS = (POS_KEY, ALLOC_KEY)
PRE_DEPLOY_POS_VERSION = '4Q1qjgD52FSKZ38EfHGqdKGHyJ_ktlka'

# function name -> the LambdaFunctionScheduled event id in that execution's history
RECORDED_EVENT = [
    ('yang-generate-positioning', 83),
    ('yang-generate-allocation-summary', 79),
]
CDN_FUNCTION = ('yang-invalidate-cloudfront', 155)

NEW_CLASSES = ('structured', 'commodities', 'alternatives')
MODELS = ('UST', 'ST', 'INT', 'LT', 'ULT')

HALVES = (
    'org/missions/D4/POSN/POSN_ASTTAX/ledger/NEVER_WIDEN_ROUND5_COO_HALF.md',
    'org/missions/D4/POSN/POSN_ASTTAX/ledger/NEVER_WIDEN_ROUND5_CTO_HALF.md',
)

# read_timeout above the largest function timeout (positioning 360 s, allocation 240 s);
# max_attempts 0 so a slow synchronous invoke is NEVER silently re-fired by botocore.
LAMBDA_CFG = Config(region_name=REGION, read_timeout=420, connect_timeout=20,
                    retries={'max_attempts': 0})

s3 = boto3.client('s3', region_name=REGION)
sfn = boto3.client('stepfunctions', region_name=REGION)
lam = boto3.client('lambda', config=LAMBDA_CFG)

FAILURES = []


def rule(title):
    print('')
    print('=' * 78)
    print(title)
    print('=' * 78)


def fail(msg):
    FAILURES.append(msg)
    print('BLOCKED: %s' % msg)


def git_out(*args):
    r = subprocess.run(['git'] + list(args), capture_output=True)
    return r.stdout.decode('utf-8', 'replace').strip(), r.returncode


def head(bucket, key, version_id=None):
    """A failed retrieval returns a VALUE, never an exception the caller mistakes
    for an absence."""
    kw = {'Bucket': bucket, 'Key': key}
    if version_id:
        kw['VersionId'] = version_id
    try:
        r = s3.head_object(**kw)
        return {'present': True,
                'LastModified': r['LastModified'].astimezone(datetime.timezone.utc).isoformat(),
                'lm_epoch': r['LastModified'].timestamp(),
                'VersionId': r.get('VersionId'),
                'ContentLength': r['ContentLength'],
                'ETag': r.get('ETag')}
    except Exception as exc:
        code = getattr(exc, 'response', {}).get('Error', {}).get('Code', type(exc).__name__)
        return {'present': False, 'error': code}


def get_body(bucket, key, version_id=None):
    kw = {'Bucket': bucket, 'Key': key}
    if version_id:
        kw['VersionId'] = version_id
    r = s3.get_object(**kw)
    raw = r['Body'].read()
    body = gzip.decompress(raw) if raw[:2] == b'\x1f\x8b' else raw
    return raw, body


def list_prefix():
    out = {}
    token = None
    pages = 0
    while True:
        kw = {'Bucket': SERVED_BUCKET, 'Prefix': PREFIX}
        if token:
            kw['ContinuationToken'] = token
        r = s3.list_objects_v2(**kw)
        pages += 1
        for o in r.get('Contents', []):
            out[o['Key']] = o['LastModified'].astimezone(datetime.timezone.utc).isoformat()
        if not r.get('IsTruncated'):
            break
        token = r['NextContinuationToken']
    return out, pages


def flatten(obj, prefix=''):
    out = {}
    if isinstance(obj, dict):
        for k, v in obj.items():
            out.update(flatten(v, '%s.%s' % (prefix, k) if prefix else str(k)))
    elif isinstance(obj, list):
        for i, v in enumerate(obj):
            out.update(flatten(v, '%s[%d]' % (prefix, i)))
    else:
        out[prefix] = obj
    return out


def leaf(p):
    return p.split('.')[-1].split('[')[0]


def classify(path, old=None, new=None, kind='changed'):
    """The V1-AC4 classifier, byte-for-byte the same rules, so the served delta is
    graded by the instrument the branch rule was exercised with."""
    lf = leaf(path)
    if path == 'generated_at':
        return 'volatile-run-clock'
    for _new_class in NEW_CLASSES:
        if path == 'benchmarks.etf.%s' % _new_class:
            return 'benchmark-row/allocation-key'
        if path.startswith('benchmarks.etf.%s.' % _new_class):
            return 'benchmark-row/allocation-key'
    if lf in NEW_CLASSES:
        return 'benchmark-row/allocation-key'
    sentinel = ('unclassified', 'Unclassified', 'Unknown', 'Not classified')
    if lf in ('assetClass', 'asset_class', 'assetClassLabel', 'asset_class_label',
              'assetClassRecognized', 'asset_class_recognized'):
        return 'unrecognised-security-label'
    if kind == 'changed' and (str(old) in sentinel or str(new) in sentinel):
        return 'unrecognised-security-label'
    if lf in ('name', 'benchmarkName', 'displayName'):
        if kind == 'changed' and isinstance(old, str) and isinstance(new, str):
            return 'display-name'
        if kind == 'added':
            return 'display-name'
    return 'OTHER'


def diff_summary(old_obj, new_obj, title):
    fo, fn = flatten(old_obj), flatten(new_obj)
    added = sorted(set(fn) - set(fo))
    removed = sorted(set(fo) - set(fn))
    changed = sorted(k for k in set(fo) & set(fn) if fo[k] != fn[k])
    buckets = {}
    for p in added:
        buckets.setdefault(classify(p, new=fn[p], kind='added'), []).append(('ADDED', p, None, fn[p]))
    for p in removed:
        buckets.setdefault(classify(p, old=fo[p], kind='removed'), []).append(('REMOVED', p, fo[p], None))
    for p in changed:
        buckets.setdefault(classify(p, old=fo[p], new=fn[p], kind='changed'), []).append(
            ('CHANGED', p, fo[p], fn[p]))
    print('%s: prior leaf keys=%d  new leaf keys=%d  added=%d removed=%d changed=%d'
          % (title, len(fo), len(fn), len(added), len(removed), len(changed)))
    for cls in ('display-name', 'unrecognised-security-label', 'benchmark-row/allocation-key',
                'volatile-run-clock', 'OTHER'):
        print('  CLASS %-32s count=%d' % (cls, len(buckets.get(cls, []))))
    for cls in sorted(buckets):
        if cls not in ('display-name', 'unrecognised-security-label',
                       'benchmark-row/allocation-key', 'volatile-run-clock', 'OTHER'):
            print('  CLASS %-32s count=%d  (UNEXPECTED CLASS)' % (cls, len(buckets[cls])))
    other = buckets.get('OTHER', [])
    print('  OTHER = %d -> BRANCH %s' % (len(other), 'A' if not other else 'B (STOP, row)'))
    for row in other[:40]:
        print('    OTHER %s %s prior=%r new=%r' % row)
    return buckets, (fo, fn)


# ----------------------------------------------------------------------------
rule('PHASE 0 -- THE SIGN-OFF AND THE RECORDED EVENTS (provenance before any act)')
for path in HALVES:
    pin, rc = git_out('log', '-1', '--format=%H', '--', path)
    listed, rc2 = git_out('ls-tree', 'HEAD', '--', path)
    print('HALF %s @%s  present-at-HEAD=%s' % (path, pin[:10], bool(listed)))
    if not listed:
        fail('never-widen half missing at HEAD: %s' % path)
if FAILURES:
    raise SystemExit(2)

cached = json.load(open(HISTORY_CACHE, encoding='utf-8'))['events']
cache_by_id = {e['id']: e for e in cached}
print('cached history %s: %d events' % (HISTORY_CACHE, len(cached)))

live_events = None
try:
    live = []
    kw = {'executionArn': EXECUTION_ARN, 'maxResults': 1000}
    while True:
        r = sfn.get_execution_history(**kw)
        live.extend(r['events'])
        if not r.get('nextToken'):
            break
        kw['nextToken'] = r['nextToken']
    live_events = {e['id']: e for e in live}
    print('LIVE get-execution-history %s: %d events (independent re-read of the cache)'
          % (EXECUTION_ARN.split(':')[-1], len(live)))
except Exception as exc:
    print('WARN: live history re-read unavailable (%s) -- the cache stands alone' % exc)

payloads = {}
for fn_name, ev_id in RECORDED_EVENT + [CDN_FUNCTION]:
    d = cache_by_id[ev_id]['lambdaFunctionScheduledEventDetails']
    if d['resource'].split(':function:')[-1] != fn_name:
        fail('cached event %d is not %s (it is %s)' % (ev_id, fn_name, d['resource']))
        continue
    raw = d['input']
    sha = hashlib.sha256(raw.encode('utf-8')).hexdigest()
    line = 'CACHE'
    if live_events is not None:
        lraw = live_events[ev_id]['lambdaFunctionScheduledEventDetails']['input']
        lsha = hashlib.sha256(lraw.encode('utf-8')).hexdigest()
        line = 'CACHE==LIVE %s' % (sha == lsha)
        if sha != lsha:
            fail('recorded event %d differs between the cache and the live history' % ev_id)
    payloads[fn_name] = raw
    print('')
    print('RECORDED EVENT #%d -> %s   sha256=%s  [%s]  scheduled %s'
          % (ev_id, fn_name, sha[:16], line, cache_by_id[ev_id]['timestamp']))
    print(json.dumps(json.loads(raw), indent=2, sort_keys=True))
if FAILURES:
    raise SystemExit(2)

rule('PHASE 0b -- THE PREMISE THE RECORDED EVENT NAMES, MEASURED PER OBJECT')
premise_keys = []
ev83 = json.loads(payloads['yang-generate-positioning'])
for k in ('data_pkl_key', 'model_pkl_key'):
    premise_keys.append(ev83['processed'][k])
absent = 0
for k in premise_keys:
    h = head(SERVED_BUCKET, k)
    print('  input s3://%s/%s -> %s' % (SERVED_BUCKET, k, json.dumps(h)))
    if not h['present']:
        absent += 1
print('  PRESENT %d of %d named input objects (the state-machine replay was 0 of 3;'
      ' the PROCESSED keys the generator event names are a different set)'
      % (len(premise_keys) - absent, len(premise_keys)))
if absent:
    fail('%d of %d recorded-event input objects absent' % (absent, len(premise_keys)))
    raise SystemExit(2)

rule('PHASE 1 -- BASELINE BEFORE THE INVOKES (the prior VersionIds ARE the restore)')
pre = {}
for k in SIGNED_KEYS:
    pre[k] = head(SERVED_BUCKET, k)
    print('  BEFORE %s -> %s' % (k, json.dumps(pre[k])))
print('  pre-deploy anchor VersionId for %s: %s (matches current: %s)'
      % (POS_KEY, PRE_DEPLOY_POS_VERSION, pre[POS_KEY].get('VersionId') == PRE_DEPLOY_POS_VERSION))

base_list, pages = list_prefix()
print('')
print('  list-objects-v2 s3://%s/%s  DENOMINATOR: %d key(s), %d page(s) -- the second'
      ' control baseline' % (SERVED_BUCKET, PREFIX, len(base_list), pages))
for k in sorted(base_list):
    print('    %s  %s' % (base_list[k], k))

_, pre_pos_body = get_body(SERVED_BUCKET, POS_KEY, PRE_DEPLOY_POS_VERSION)
pre_pos = json.loads(pre_pos_body)
pre_alloc_raw, pre_alloc_body = get_body(SERVED_BUCKET, ALLOC_KEY, pre[ALLOC_KEY]['VersionId'])
pre_alloc = json.loads(pre_alloc_body)
print('')
print('  pre-deploy %s VersionId %s: %d inflated bytes, generated_at %s'
      % (POS_KEY, PRE_DEPLOY_POS_VERSION, len(pre_pos_body), pre_pos.get('generated_at')))
print('  prior %s VersionId %s: %d stored bytes / %d inflated, generated_at %s'
      % (ALLOC_KEY, pre[ALLOC_KEY]['VersionId'], len(pre_alloc_raw), len(pre_alloc_body),
         pre_alloc.get('generated_at')))

rule('PHASE 2 -- THE INVOKES: the two generators this cell deployed, DIRECTLY, in order')
for fn_name, ev_id in RECORDED_EVENT:
    t0 = datetime.datetime.now(datetime.timezone.utc)
    resp = lam.invoke(FunctionName=fn_name, InvocationType='RequestResponse',
                      Payload=payloads[fn_name].encode('utf-8'))
    body = resp['Payload'].read().decode('utf-8', 'replace')
    t1 = datetime.datetime.now(datetime.timezone.utc)
    ferr = resp.get('FunctionError')
    print('')
    print('INVOKE %s  event #%d  StatusCode=%s  FunctionError=%s  elapsed=%.1fs'
          % (fn_name, ev_id, resp['StatusCode'], ferr if ferr else 'NONE',
             (t1 - t0).total_seconds()))
    print('  response body: %s' % body[:2000])
    if resp['StatusCode'] != 200 or ferr:
        fail('%s invoke did not return a clean 200 (StatusCode=%s FunctionError=%s)'
             % (fn_name, resp['StatusCode'], ferr))
if FAILURES:
    print('')
    print('BRANCH B -- STOP. Nothing further is invoked; the CDN step is NOT run.')
    raise SystemExit(3)

rule('PHASE 3 -- BOTH HEADS MOVED (the artifact, never the invoke rc)')
post = {}
for k in SIGNED_KEYS:
    post[k] = head(SERVED_BUCKET, k)
    moved = (post[k]['present'] and pre[k]['present']
             and post[k]['VersionId'] != pre[k]['VersionId']
             and post[k]['lm_epoch'] > pre[k]['lm_epoch'])
    print('  AFTER  %s -> %s' % (k, json.dumps(post[k])))
    print('         moved=%s  (%s -> %s ; VersionId %s -> %s)'
          % (moved, pre[k].get('LastModified'), post[k].get('LastModified'),
             pre[k].get('VersionId'), post[k].get('VersionId')))
    if not moved:
        fail('%s head did not move after the invoke' % k)

rule('PHASE 4 -- THE SERVED positioning_data.json, READ AND GRADED')
_, new_pos_body = get_body(SERVED_BUCKET, POS_KEY, post[POS_KEY]['VersionId'])
new_pos = json.loads(new_pos_body)
print('  served VersionId %s: %d inflated bytes, generated_at %s, data_as_of %s, models %s'
      % (post[POS_KEY]['VersionId'], len(new_pos_body), new_pos.get('generated_at'),
         new_pos.get('data_as_of'), sorted(new_pos.get('portfolios', {}))))

print('')
print('  (a) THE FIVE-CLASS ALLOCATION KEYS AT AN EXPLICIT ZERO -- 60 leaf keys expected')
zero_paths = []
for m in MODELS:
    p = new_pos['portfolios'][m]
    for c in NEW_CLASSES:
        zero_paths.append(('portfolios.%s.allocation.%s' % (m, c), p['allocation'].get(c, '<MISSING>')))
        zero_paths.append(('portfolios.%s.benchmark.allocation.%s' % (m, c),
                           p['benchmark']['allocation'].get(c, '<MISSING>')))
        zero_paths.append(('portfolios.%s.benchmark.spread.allocation.%s' % (m, c),
                           p['benchmark']['spread']['allocation'].get(c, '<MISSING>')))
        zero_paths.append(('portfolios.%s.delta.%s' % (m, c), p['delta'].get(c, '<MISSING>')))
present = [p for p in zero_paths if p[1] != '<MISSING>']
zeros = [p for p in present if p[1] == 0 or p[1] == 0.0]
print('      leaf keys present: %d of %d expected' % (len(present), len(zero_paths)))
print('      of those, value 0 or 0.0: %d of %d' % (len(zeros), len(present)))
for path, val in zero_paths:
    if val == '<MISSING>' or not (val == 0 or val == 0.0):
        print('      NOT-ZERO-OR-MISSING %s = %r' % (path, val))
if len(present) != 60 or len(zeros) != 60:
    fail('the five-class zero keys read %d present / %d zero, expected 60 / 60'
         % (len(present), len(zeros)))

print('')
print('  (b) benchmarks.etf ROWS FOR THE THREE CLASSES, VERBATIM')
etf = new_pos.get('benchmarks', {}).get('etf', {})
print('      benchmarks.etf key denominator: %d -> %s' % (len(etf), sorted(etf)))
for c in NEW_CLASSES:
    row = etf.get(c)
    print('      benchmarks.etf.%s = %s' % (c, json.dumps(row, sort_keys=True)))
    if not isinstance(row, dict) or row.get('ticker') is not None or row.get('label') != 'no benchmark':
        fail('benchmarks.etf.%s is not a labelled-zero row (ticker null, label "no benchmark")' % c)

print('')
print('  (c) MEMBERSHIP -- tickers per model vs the pre-deploy read (VersionId %s)'
      % PRE_DEPLOY_POS_VERSION)
for m in MODELS:
    tb = [h['ticker'] for h in pre_pos['portfolios'][m]['holdings']]
    tn = [h['ticker'] for h in new_pos['portfolios'][m]['holdings']]
    same = tb == tn
    print('      %-4s pre=%d new=%d identical=%s' % (m, len(tb), len(tn), same))
    if not same:
        fail('membership changed for model %s' % m)

print('')
print('  (d) THE PAYLOAD DIFF, CLASSIFIED (pre-deploy served bytes vs the served bytes now)')
buckets, _ = diff_summary(pre_pos, new_pos, '      positioning_data.json')
if buckets.get('OTHER'):
    fail('positioning_data.json diff carries %d OTHER row(s)' % len(buckets['OTHER']))

rule('PHASE 5 -- THE CONTROL: allocation_summary.json byte-identical except generated_at')
_, new_alloc_body = get_body(SERVED_BUCKET, ALLOC_KEY, post[ALLOC_KEY]['VersionId'])
new_alloc = json.loads(new_alloc_body)
fa, fn2 = flatten(pre_alloc), flatten(new_alloc)
a = sorted(set(fn2) - set(fa))
r = sorted(set(fa) - set(fn2))
c = sorted(k for k in set(fa) & set(fn2) if fa[k] != fn2[k])
print('  prior leaf keys=%d  new leaf keys=%d  added=%d removed=%d changed=%d'
      % (len(fa), len(fn2), len(a), len(r), len(c)))
for k in c:
    print('    CHANGED %s  prior=%r new=%r' % (k, fa[k], fn2[k]))
for k in a[:20]:
    print('    ADDED %s = %r' % (k, fn2[k]))
for k in r[:20]:
    print('    REMOVED %s = %r' % (k, fa[k]))
only_clock = (not a and not r and c == ['generated_at'])
print('  byte-identical except generated_at: %s  (inflated bytes %d -> %d)'
      % (only_clock, len(pre_alloc_body), len(new_alloc_body)))
print('  WHY THIS IS THE CONTROL: no holding carries structured/commodities/alternatives'
      ' today, so the new BENCHMARK_ALLOCATIONS rows are code-level and must NOT move the'
      ' served bytes.')
if not only_clock:
    fail('allocation_summary.json differs beyond generated_at')

rule('PHASE 6 -- THE SECOND CONTROL: no OTHER key under json/positioning/ moved')
after_list, pages2 = list_prefix()
print('  list-objects-v2 again  DENOMINATOR: %d key(s), %d page(s)' % (len(after_list), pages2))
moved_other = []
for k in sorted(set(base_list) | set(after_list)):
    b = base_list.get(k)
    n = after_list.get(k)
    state = 'UNCHANGED'
    if b is None:
        state = 'APPEARED'
    elif n is None:
        state = 'VANISHED'
    elif b != n:
        state = 'MOVED'
    flag = 'SIGNED' if k in SIGNED_KEYS else 'other'
    print('    %-9s %-6s %s  %s -> %s' % (state, flag, k, b, n))
    if state != 'UNCHANGED' and k not in SIGNED_KEYS:
        moved_other.append((k, state, b, n))
print('  keys under the prefix that are NOT the two signed keys and MOVED: %d of %d'
      % (len(moved_other), len(after_list)))
if moved_other:
    fail('%d non-signed key(s) under %s moved -- Branch B' % (len(moved_other), PREFIX))

if FAILURES:
    print('')
    print('BRANCH B -- STOP. The CDN invalidation is NOT run.')
    raise SystemExit(3)

rule('PHASE 7 -- THE CDN: the pipeline\'s own invalidation step, its recorded event')
fn_name, ev_id = CDN_FUNCTION
resp = lam.invoke(FunctionName=fn_name, InvocationType='RequestResponse',
                  Payload=payloads[fn_name].encode('utf-8'))
body = resp['Payload'].read().decode('utf-8', 'replace')
ferr = resp.get('FunctionError')
print('INVOKE %s  event #%d  StatusCode=%s  FunctionError=%s'
      % (fn_name, ev_id, resp['StatusCode'], ferr if ferr else 'NONE'))
print('  response body: %s' % body[:2000])
if resp['StatusCode'] != 200 or ferr:
    fail('%s invoke did not return a clean 200' % fn_name)
else:
    try:
        parsed = json.loads(body)
        for inv in parsed.get('invalidations', []):
            print('  DISTRIBUTION %s  Invalidation Id %s  Status %s%s'
                  % (inv.get('distribution_id'), inv.get('invalidation_id'),
                     inv.get('status'), '  ERROR=%s' % inv['error'] if 'error' in inv else ''))
            if 'error' in inv:
                fail('CloudFront invalidation failed on %s' % inv.get('distribution_id'))
    except ValueError:
        fail('%s response body is not JSON' % fn_name)

rule('VERDICT')
print('served keys AFTER the driven refresh:')
for k in SIGNED_KEYS:
    print('  %s  LastModified %s  VersionId %s  %s bytes'
          % (k, post[k]['LastModified'], post[k]['VersionId'], post[k]['ContentLength']))
print('restore (the prior object versions, printed before the act):')
for k in SIGNED_KEYS:
    print('  %s  VersionId %s' % (k, pre[k]['VersionId']))
if FAILURES:
    print('')
    print('BRANCH B -- %d blocking observation(s):' % len(FAILURES))
    for f in FAILURES:
        print('  - %s' % f)
    raise SystemExit(3)
print('')
print('OK: BRANCH A -- every clause of V1-AC11 met on the ARTIFACT.')
raise SystemExit(0)
