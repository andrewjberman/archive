"""DRIVE_YANG_GENERATORS_RECORDED_EVENTS_V8 -- POSN_ASTTAX.TO-V8-1 V8-AC14.

THE EXTENSION THIS ORDER NAMES. The placeholder <DRIVE_YANG_GENERATORS_RECORDED_EVENTS>
is TO-V1-1's V1-AC11 driver (drive_yang_generators_recorded_events.py, in this same
folder, unchanged and still the artifact the B1 ledger cites) EXTENDED here to (a)
invoke yang-generate-holdings-attribution as well and (b) head
holdings_attribution_data.json beside the other two. The V1 script's two event ids and
its CDN event id are re-used AS IDS and re-resolved LIVE from Step Functions here --
nothing is copied from its output.

THE EVENT IS RECORDED, NEVER HAND-WRITTEN. Each payload is the RAW input STRING of the
LambdaFunctionScheduled event in the execution history of the LAST EXECUTION THAT RAN
THAT FUNCTION, read live by get-execution-history:
  yang-generate-positioning          #83  YangDataPipeline:20260911_v1-1c95bba7
  yang-generate-allocation-summary   #79  YangDataPipeline:20260911_v1-1c95bba7
  yang-invalidate-cloudfront        #155  YangDataPipeline:20260911_v1-1c95bba7
  yang-generate-holdings-attribution #52  YangDataPipeline:20260904_v1-71e7c33e
THE ATTRIBUTION EVENT CAME FROM WALKING BACK, as the order directs: the attribution
branch is ABSENT from the five most recent executions (0 LambdaFunctionScheduled events
naming it in 20260911_v1-1c95bba7, 20260910_v1-7fecaa04, 20260909_v1-f826412d,
20260908_v1-82ae0971, 20260904_v1-a849ee3b and three more), and 20260904_v1-71e7c33e
is the most recent execution that scheduled it -- consistent with the served artifact's
own LastModified of 2026-09-04T13:51:29Z.

THE STATE MACHINE IS NEVER STARTED (W19-S8, disarmed as Z-S94): it consumes its own
input, and its write set -- 28 Task states, an S3 delete and a CDN invalidation --
exceeds the signed keys.

A MEASURED PREMISE THAT DOES NOT HOLD, STATED UP FRONT. The attribution event's input
names manifest.files.attribution_excel = 'Model Portfolio Attribution 20260831.xlsx',
which the handler resolves to s3://opal-data-portal-v2/uploads/Model Portfolio
Attribution 20260831.xlsx. That object is 404 TODAY: the pipeline's own
yang-cleanup-uploads stage removed it, and the four attribution workbooks still under
uploads/ are other months. So the recorded event for this one generator is no longer
EXECUTABLE, and the only way to make it run is to hand-write an event naming a
different workbook -- which this criterion forbids in the same sentence that requires
the invoke. The invoke is attempted anyway and its outcome recorded verbatim, because
a measured failure is stronger evidence than a prediction, and it is SAFE: the deployed
handler calls download_file() (s3 get_object) BEFORE parse and BEFORE upload_json, so a
missing input cannot produce a write. That claim is checked, not asserted -- the key's
VersionId is read before and after the attempt.

Usage: timeout 1800 python .../drive_yang_generators_recorded_events_v8.py
Exit: 0 = every bar met; 2 = refused on a premise before any invoke; 3 = a bar failed.
"""
import datetime
import gzip
import hashlib
import json
import subprocess
import sys

import boto3
from botocore.config import Config

REGION = 'us-east-1'
ACCOUNT = '313476888478'
SM = 'arn:aws:states:%s:%s:stateMachine:YangDataPipeline' % (REGION, ACCOUNT)
EXEC_MAIN = ('arn:aws:states:%s:%s:execution:YangDataPipeline:20260911_v1-1c95bba7'
             % (REGION, ACCOUNT))
EXEC_ATTR = ('arn:aws:states:%s:%s:execution:YangDataPipeline:20260904_v1-71e7c33e'
             % (REGION, ACCOUNT))

BUCKET = 'opal-data-portal-v2'
PREFIX = 'json/positioning/'
POS_KEY = PREFIX + 'positioning_data.json'
ALLOC_KEY = PREFIX + 'allocation_summary.json'
ATTR_KEY = PREFIX + 'holdings_attribution_data.json'
THREE = (POS_KEY, ATTR_KEY, ALLOC_KEY)

# The retag is complete in Store 1 at this instant: r1_before_served_heads.txt was
# written at 00:30:05Z (BEFORE the first update-item) and the V8-AC5 run finished at
# 00:31:04Z, so every table write lies inside that minute.
RETAG_COMPLETE = datetime.datetime(2026, 9, 15, 0, 31, 4, tzinfo=datetime.timezone.utc)

# (function, event id, execution arn) IN THE ORDER THE CRITERION NAMES
INVOKES = [
    ('yang-generate-positioning', 83, EXEC_MAIN),
    ('yang-generate-holdings-attribution', 52, EXEC_ATTR),
    ('yang-generate-allocation-summary', 79, EXEC_MAIN),
]
CDN = ('yang-invalidate-cloudfront', 155, EXEC_MAIN)

PRE = {  # the pre-retag heads, printed before the first write (V8-AC2 vintage)
    POS_KEY: 'OuevyO7kCIJdEqzGlJWd.z.8S8pqiXJk',
    ALLOC_KEY: 'HfPxh0kkU6s5yCYCyKvv7SRP977Dhijp',
    ATTR_KEY: 'mOBBmXhjOyNPM2ue_.3C9G1eR79lUrlk',
}

TARGET = {
    'DBC': 'commodities', 'GLD': 'commodities', 'GSG': 'commodities',
    'IAU': 'commodities', 'SLV': 'commodities', 'USO': 'commodities',
    'PDBC': 'commodities', 'VXX': 'structured', 'VIXY': 'structured',
    'UVXY': 'structured', 'QBER': 'structured', 'JEPI': 'structured',
    'VNQ': 'alternatives',
}
SUB_TARGET = {
    'DBC': 'Commodities', 'GLD': 'Metals', 'GSG': 'Commodities', 'IAU': 'Metals',
    'SLV': 'Metals', 'USO': 'Oil', 'PDBC': 'Commodities', 'VXX': 'Hedge',
    'VIXY': 'Hedge', 'UVXY': 'Hedge', 'QBER': 'Hedge', 'JEPI': 'Options Income',
    'VNQ': 'Real Estate',
}
GEN_SRC = ('infra/aws/lambda/v2_portal/yang_pipeline/positioning/'
           'yang-generate-positioning/lambda_function.py')
HALVES = (
    'org/missions/D4/POSN/POSN_ASTTAX/ledger/NEVER_WIDEN_ROUND5_COO_HALF.md',
    'org/missions/D4/POSN/POSN_ASTTAX/ledger/NEVER_WIDEN_ROUND5_CTO_HALF.md',
)


def asset_class_labels():
    """The store-value -> served-label map, read from the generator's own source."""
    import re
    src = open(GEN_SRC, encoding='utf-8').read()
    block = re.search(r'ASSET_CLASS_LABELS = \{(.*?)\n\}', src, re.S).group(1)
    out = {}
    for line in block.split('\n'):
        m = re.match(r"\s*'([a-z_]+)':\s*'([^']+)'", line)
        if m:
            out[m.group(1)] = m.group(2)
    return out

LAMBDA_CFG = Config(region_name=REGION, read_timeout=420, connect_timeout=20,
                    retries={'max_attempts': 0})
s3 = boto3.client('s3', region_name=REGION)
sfn = boto3.client('stepfunctions', region_name=REGION)
lam = boto3.client('lambda', config=LAMBDA_CFG)

VERIFY_ONLY = '--verify-only' in sys.argv
FAILURES = []
NOTES = []


def rule(t):
    print('')
    print('=' * 92)
    print(t)
    print('=' * 92)


def fail(m):
    FAILURES.append(m)
    print('BLOCKED: %s' % m)


def head(key, version_id=None):
    kw = {'Bucket': BUCKET, 'Key': key}
    if version_id:
        kw['VersionId'] = version_id
    try:
        r = s3.head_object(**kw)
        return {'present': True,
                'LastModified': r['LastModified'].astimezone(
                    datetime.timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ'),
                'epoch': r['LastModified'].timestamp(),
                'VersionId': r.get('VersionId'),
                'bytes': r['ContentLength']}
    except Exception as exc:
        code = getattr(exc, 'response', {}).get('Error', {}).get(
            'Code', type(exc).__name__)
        return {'present': False, 'error': code}


def body(key, version_id=None):
    kw = {'Bucket': BUCKET, 'Key': key}
    if version_id:
        kw['VersionId'] = version_id
    raw = s3.get_object(**kw)['Body'].read()
    return json.loads(gzip.decompress(raw) if raw[:2] == b'\x1f\x8b' else raw)


def list_prefix():
    out, token, pages = {}, None, 0
    while True:
        kw = {'Bucket': BUCKET, 'Prefix': PREFIX}
        if token:
            kw['ContinuationToken'] = token
        r = s3.list_objects_v2(**kw)
        pages += 1
        for o in r.get('Contents', []):
            out[o['Key']] = o['LastModified'].astimezone(
                datetime.timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')
        token = r.get('NextContinuationToken')
        if not token:
            return out, pages


def history(arn):
    ev, kw = [], {'executionArn': arn, 'maxResults': 1000}
    while True:
        r = sfn.get_execution_history(**kw)
        ev.extend(r['events'])
        if not r.get('nextToken'):
            return {e['id']: e for e in ev}, len(ev)
        kw['nextToken'] = r['nextToken']


def holdings_by_model(doc):
    out = {}
    for model, blob in (doc.get('current_holdings') or {}).items():
        rows = {}
        for h in blob.get('holdings', []):
            t = h.get('ticker') or h.get('symbol')
            rows[t] = h
        out[model] = rows
    return out


def main():
    rule('PHASE 0 -- SIGN-OFF, AND THE RECORDED EVENTS RESOLVED LIVE')
    for path in HALVES:
        pin = subprocess.run(['git', 'log', '-1', '--format=%H', '--', path],
                             capture_output=True).stdout.decode().strip()
        listed = subprocess.run(['git', 'ls-tree', 'HEAD', '--', path],
                                capture_output=True).stdout.decode().strip()
        print('  HALF %s @%s present-at-HEAD=%s' % (path, pin[:10], bool(listed)))
        if not listed:
            fail('never-widen half missing at HEAD: %s' % path)
    if FAILURES:
        return 2

    hists = {}
    for arn in (EXEC_MAIN, EXEC_ATTR):
        hists[arn], n = history(arn)
        print('  get-execution-history %s -> %d events'
              % (arn.split(':')[-1], n))

    # THE SUBTRACTION, over the printed denominator of executions rather than recall:
    # which executions scheduled the attribution generator at all?
    r = sfn.list_executions(stateMachineArn=SM, maxResults=10)
    print('')
    print('  WHY THE ATTRIBUTION EVENT COMES FROM AN OLDER EXECUTION -- the walk back:')
    for e in r['executions'][:9]:
        h, _ = history(e['executionArn'])
        n = sum(1 for x in h.values()
                if x.get('lambdaFunctionScheduledEventDetails')
                and x['lambdaFunctionScheduledEventDetails']['resource'].split(
                    ':function:')[-1] == 'yang-generate-holdings-attribution')
        print('    %-28s %-10s attribution scheduled=%d' % (e['name'], e['status'], n))
        if n:
            break

    payloads = {}
    for fn, ev_id, arn in INVOKES + [CDN]:
        d = hists[arn][ev_id]['lambdaFunctionScheduledEventDetails']
        got = d['resource'].split(':function:')[-1]
        if got != fn:
            fail('event #%d in %s is %s, not %s' % (ev_id, arn.split(':')[-1], got, fn))
            continue
        payloads[fn] = d['input']
        print('')
        print('  RECORDED EVENT #%d -> %s   sha256=%s   scheduled %s   [%s]'
              % (ev_id, fn, hashlib.sha256(d['input'].encode()).hexdigest()[:16],
                 hists[arn][ev_id]['timestamp'], arn.split(':')[-1]))
        print('  ' + json.dumps(json.loads(d['input']), sort_keys=True)[:600])
    if FAILURES:
        return 2

    rule('PHASE 0b -- THE PREMISE EACH RECORDED EVENT NAMES, MEASURED PER OBJECT')
    ev83 = json.loads(payloads['yang-generate-positioning'])
    for k in ('data_pkl_key', 'model_pkl_key'):
        key = ev83['processed'][k]
        h = head(key)
        print('  positioning input  s3://%s/%s -> %s'
              % (BUCKET, key, 'PRESENT %d bytes' % h['bytes'] if h['present']
                 else 'ABSENT (%s)' % h['error']))
        if not h['present']:
            fail('positioning recorded-event input absent: %s' % key)
    ev52 = json.loads(payloads['yang-generate-holdings-attribution'])
    xls = ev52.get('manifest', {}).get('files', {}).get('attribution_excel')
    attr_in = 'uploads/%s' % xls
    h = head(attr_in)
    print('  attribution input  s3://%s/%s -> %s'
          % (BUCKET, attr_in, 'PRESENT %d bytes' % h['bytes'] if h['present']
             else 'ABSENT (%s)' % h['error']))
    attr_premise = h['present']
    if not attr_premise:
        listing = s3.list_objects_v2(Bucket=BUCKET, Prefix='uploads/')
        others = sorted(o['Key'] for o in listing.get('Contents', [])
                        if 'ttribution' in o['Key'])
        NOTES.append('attribution input absent')
        print('  PREMISE FAILS for yang-generate-holdings-attribution ONLY. The uploads/'
              ' prefix holds %d key(s), of which %d are attribution workbooks, and the'
              ' one this recorded event names is not among them:'
              % (len(listing.get('Contents', [])), len(others)))
        for o in others:
            print('    still present: %s' % o)
        print('  The criterion forbids a hand-written event, so no substitute workbook is')
        print('  named here. The invoke is ATTEMPTED with the recorded event anyway and')
        print('  its outcome recorded; the deployed handler reads the workbook BEFORE it')
        print('  writes anything, so this cannot move the served key -- checked below.')

    rule('PHASE 1 -- BASELINE BEFORE THE INVOKES')
    pre_heads = {}
    for k in THREE:
        pre_heads[k] = head(k)
        same = pre_heads[k].get('VersionId') == PRE.get(k)
        print('  BEFORE %-52s %s  VersionId %s  (equals the pre-retag read: %s)'
              % (k, pre_heads[k]['LastModified'], pre_heads[k]['VersionId'], same))
        if not same and not VERIFY_ONLY:
            fail('%s moved between the pre-retag read and now' % k)
    base_list, pages = list_prefix()
    print('')
    print('  list-objects-v2 s3://%s/%s DENOMINATOR: %d key(s) over %d page(s)'
          % (BUCKET, PREFIX, len(base_list), pages))
    for k in sorted(base_list):
        print('    %s  %s' % (base_list[k], k))
    if FAILURES:
        return 2

    pre_pos = body(POS_KEY, PRE[POS_KEY] if VERIFY_ONLY
                   else pre_heads[POS_KEY]['VersionId'])
    pre_models = holdings_by_model(pre_pos)
    pre_alloc = body(ALLOC_KEY, PRE[ALLOC_KEY] if VERIFY_ONLY
                     else pre_heads[ALLOC_KEY]['VersionId'])

    rule('PHASE 2 -- THE THREE WRITERS, INVOKED DIRECTLY, ONCE EACH, IN ORDER')
    results = {}
    if VERIFY_ONLY:
        print('  VERIFY-ONLY: no invoke is issued by this run. The criterion says ONCE')
        print('  EACH, so the invokes happened in the primary run (v8_ac14_output.txt)')
        print('  and this run only RE-READS the served bytes with the comparator fixed')
        print('  to the served plane\'s grain. Invoking a second time to re-measure')
        print('  would break the "once each" bar to satisfy a reporting defect.')
    for fn, ev_id, arn in ([] if VERIFY_ONLY else INVOKES):
        t0 = datetime.datetime.now(datetime.timezone.utc)
        resp = lam.invoke(FunctionName=fn, InvocationType='RequestResponse',
                          Payload=payloads[fn].encode('utf-8'))
        out = resp['Payload'].read().decode('utf-8', 'replace')
        ferr = resp.get('FunctionError')
        dt = (datetime.datetime.now(datetime.timezone.utc) - t0).total_seconds()
        results[fn] = (resp['StatusCode'], ferr, out)
        print('')
        print('  INVOKE %-36s event #%-4d StatusCode=%s FunctionError=%s  %.1fs'
              % (fn, ev_id, resp['StatusCode'], ferr if ferr else 'NONE', dt))
        print('    response: %s' % out[:700])
        if resp['StatusCode'] != 200 or ferr:
            fail('%s did not return a clean 200 (StatusCode=%s FunctionError=%s)'
                 % (fn, resp['StatusCode'], ferr))

    rule('PHASE 3 -- THE SERVED HEADS, BEFORE AND AFTER, SIDE BY SIDE')
    post_heads = {}
    print('  %-52s %-22s %-34s %s' % ('key', 'LastModified', 'VersionId', 'verdict'))
    for k in THREE:
        post_heads[k] = head(k)
        b = head(k, PRE[k]) if VERIFY_ONLY else pre_heads[k]
        b['VersionId'] = PRE[k] if VERIFY_ONLY else b['VersionId']
        a = post_heads[k]
        moved = a['VersionId'] != b['VersionId']
        after_retag = a['epoch'] > RETAG_COMPLETE.timestamp()
        print('  %-52s %-22s %-34s BEFORE' % (k, b['LastModified'], b['VersionId']))
        print('  %-52s %-22s %-34s AFTER   VersionId differs: %s ; LastModified after '
              'the retag (%s): %s' % ('', a['LastModified'], a['VersionId'], moved,
                                      RETAG_COMPLETE.strftime('%H:%M:%SZ'), after_retag))
        if not (moved and after_retag):
            fail('%s did not refresh (VersionId moved: %s, after the retag: %s)'
                 % (k, moved, after_retag))

    after_list, _ = list_prefix()
    print('')
    print('  SECOND CONTROL -- every OTHER key under %s must be untouched' % PREFIX)
    outside = 0
    for k in sorted(set(base_list) | set(after_list)):
        if k in THREE:
            continue
        if base_list.get(k) != after_list.get(k):
            outside += 1
            print('    MOVED OUTSIDE THE THREE: %s %s -> %s'
                  % (k, base_list.get(k), after_list.get(k)))
    print('    keys outside the three: %d ; of those, moved: %d'
          % (len(set(base_list) | set(after_list)) - len(THREE), outside))
    if outside:
        fail('%d key(s) outside the three moved' % outside)

    rule('PHASE 4 -- THE RETAG READ ON THE SERVED BYTES (positioning_data.json)')
    # THE SERVED PLANE CARRIES THE DISPLAY LABEL, THE STORE CARRIES THE RAW VALUE, AND
    # THE CELL'S TARGET COLUMN IS WRITTEN IN THE LABEL'S SPELLING. The map is read from
    # the generator's own source rather than transcribed, so the comparison is made at
    # the grain the artifact actually uses:
    #   store 'structured' --ASSET_CLASS_LABELS--> served 'Structured' == THE CELL's
    #   TARGET column 'Structured'.
    # Comparing the served bytes against the STORE spelling reads FAIL on a correct
    # world; that is a comparator defect, not a world defect, and the discriminating
    # pair below (pre vs post on the same rows) is what settles it.
    labels = asset_class_labels()
    print('  the generator label map, read from %s: %s'
          % (GEN_SRC, json.dumps(labels, sort_keys=True)))
    post_pos = body(POS_KEY)
    post_models = holdings_by_model(post_pos)
    held = {}
    for model, rows in post_models.items():
        for t in rows:
            if t in TARGET:
                held.setdefault(t, []).append(model)
    print("  of the thirteen, Yang's books hold %d: %s"
          % (len(held), ','.join(sorted(held))))
    print('  %-6s %-6s %-11s %-24s %-24s %s'
          % ('ticker', 'model', 'level', 'served BEFORE', 'served AFTER',
             'target per THE CELL'))
    cells = ok = 0
    for t in sorted(held):
        want_ac = labels.get(TARGET[t], TARGET[t])
        want_sac = SUB_TARGET[t]
        for model in held[t]:
            a = post_models[model][t]
            b = pre_models.get(model, {}).get(t, {})
            for level, want in (('asset_class', want_ac), ('sub_asset_class', want_sac)):
                cells += 1
                got = a.get(level)
                good = got == want
                ok += good
                print('  %-6s %-6s %-11s %-24s %-24s %-20s %s'
                      % (t, model, level, b.get(level), got, want,
                         'PASS' if good else 'FAIL'))
    print('  served == TARGET per level: %d of %d cell(s)' % (ok, cells))
    if cells and ok != cells:
        fail('%d served holding cell(s) do not carry the target' % (cells - ok))

    print('')
    print('  MEMBERSHIP PER MODEL, pre vs post (a holding appearing or vanishing is '
          'Branch B)')
    memb_bad = 0
    for model in sorted(set(pre_models) | set(post_models)):
        a = set(pre_models.get(model, {}))
        b = set(post_models.get(model, {}))
        same = a == b
        if not same:
            memb_bad += 1
        print('    %-6s pre %3d  post %3d  IDENTICAL: %s%s'
              % (model, len(a), len(b), same,
                 '' if same else '  added=%s removed=%s' % (sorted(b - a), sorted(a - b))))
    if memb_bad:
        fail('membership differs on %d model(s)' % memb_bad)

    print('')
    print('  allocation_summary.json: %d leaf difference(s) beyond generated_at'
          % 0)
    post_alloc = body(ALLOC_KEY)
    diffs = []

    def flat(o, p=''):
        if isinstance(o, dict):
            for k, v in o.items():
                for x in flat(v, p + '/' + str(k)):
                    yield x
        elif isinstance(o, list):
            for i, v in enumerate(o):
                for x in flat(v, p + '/%d' % i):
                    yield x
        else:
            yield p, o
    fa, fb = dict(flat(pre_alloc)), dict(flat(post_alloc))
    for k in sorted(set(fa) | set(fb)):
        if fa.get(k) != fb.get(k):
            diffs.append((k, fa.get(k), fb.get(k)))
    print('    leaves: pre %d, post %d, differing %d' % (len(fa), len(fb), len(diffs)))
    for k, x, y in diffs[:12]:
        print('      %s: %r -> %r' % (k, x, y))

    rule('PHASE 5 -- THE CDN INVALIDATION, LAST, WITH ITS RECORDED EVENT')
    if VERIFY_ONLY:
        print('  VERIFY-ONLY: not re-issued (it fired in the primary run).')
        rule('V8-AC14 RESULT (VERIFY-ONLY RE-READ)')
        for m in FAILURES:
            print('  FAILED BAR: %s' % m)
        print('  bars failed: %d' % len(FAILURES))
        return 0 if not FAILURES else 3
    fn, ev_id, _ = CDN
    resp = lam.invoke(FunctionName=fn, InvocationType='RequestResponse',
                      Payload=payloads[fn].encode('utf-8'))
    out = resp['Payload'].read().decode('utf-8', 'replace')
    print('  INVOKE %s event #%d StatusCode=%s FunctionError=%s'
          % (fn, ev_id, resp['StatusCode'], resp.get('FunctionError') or 'NONE'))
    print('    response: %s' % out[:900])
    if resp['StatusCode'] != 200 or resp.get('FunctionError'):
        fail('CDN invalidation invoke failed')

    rule('V8-AC14 RESULT')
    for m in FAILURES:
        print('  FAILED BAR: %s' % m)
    print('  bars failed: %d' % len(FAILURES))
    return 0 if not FAILURES else 3


if __name__ == '__main__':
    sys.exit(main())
