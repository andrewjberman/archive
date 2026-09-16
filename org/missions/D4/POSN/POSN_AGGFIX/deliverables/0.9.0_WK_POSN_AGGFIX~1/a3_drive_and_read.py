#!/usr/bin/env python3
"""<DRIVE_AND_READ_A3> -- POSN_AGGFIX.TO-A3-1 (cell AF1-s-10).

Default mode (A3-AC8): ONE driven run on the recorded events. Prints the heads of the shared file and the
Opal-only key and the full listing of json/positioning/ FIRST; then invokes yang-generate-positioning ONCE
with the raw input the YangDataPipeline state machine passed GeneratePositioning in its latest execution
that ran it, and yang-invalidate-cloudfront ONCE with its recorded input from the SAME execution (never a
hand-written event, never the state machine); then the same heads and listing again. The invoke client
has retries disabled so a timeout can never become a second invoke, and a state file refuses a second
drive. The prior and new VersionIds persist in a3_drive_state.json beside this script.

--read-only-compare (A3-AC9): prior vs new shared file as PARSED JSON (dict key order ignored, list order
compared; the never-widen halves' ADDENDA on row W1-S7), each book's aum against its own platinum row at
the VersionId the run read, the Opal-only payload checks, and the Branch A / Branch B line.

--satellites-reader (A3-AC10): build_satellites_characteristics.yang_index imported by path and run on the
prior and the new shared file.

Nothing in the two read modes writes to any service. Author: 0.9.0_WK_POSN_AGGFIX~1, 2026-09-15.
"""
import argparse
import base64
import copy
import datetime as dt
import gzip
import hashlib
import importlib.util
import json
import re
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
WS = Path(subprocess.run(['git', 'rev-parse', '--show-toplevel'], cwd=str(HERE), capture_output=True,
                         text=True, check=True).stdout.strip())
STATE = HERE / 'a3_drive_state.json'
REGION = 'us-east-1'
BUCKET = 'opal-data-portal-v2'
PREFIX = 'json/positioning/'
SHARED_KEY = 'json/positioning/positioning_data.json'
AGG_KEY = 'json/positioning/opal_aggregate.json'
PLATINUM_KEY = 'platinum/mdpf/global/aum-metrics.json'
STATE_MACHINE_NAME = 'YangDataPipeline'
GEN_STATE, GEN_FN = 'GeneratePositioning', 'yang-generate-positioning'
INV_STATE, INV_FN = 'InvalidateCloudFront', 'yang-invalidate-cloudfront'
CODES = ['UST', 'ST', 'INT', 'LT', 'ULT']
STANDARD_REL = 'org/standards/POSN_AGGREGATE_MODEL_SET.json'
SATELLITES_REL = 'data/assets/scripts/gold/build_satellites_characteristics.py'
PERMITTED = [
    (re.compile(r'^\$\.generated_at \(value\)'), 'generated_at'),
    (re.compile(r'^\$\.current_holdings\.AGG \(present only in prior\)$'), 'current_holdings.AGG removed'),
    (re.compile(r'^\$\.current_holdings\.(UST|ST|INT|LT|ULT)\.aum \(value\)'), 'book aum'),
]


def out(s=''):
    sys.stdout.write(str(s).encode('ascii', 'backslashreplace').decode('ascii') + '\n')
    sys.stdout.flush()


def now():
    return dt.datetime.now(dt.timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')


def sha(b):
    return hashlib.sha256(b).hexdigest()


def gunzip(b):
    return gzip.decompress(b) if b[:2] == b'\x1f\x8b' else b


def clients():
    import boto3
    return boto3.client('s3', region_name=REGION), boto3.client('stepfunctions', region_name=REGION)


def load_state():
    return json.loads(STATE.read_text(encoding='utf-8')) if STATE.exists() else {}


def save_state(st):
    STATE.write_text(json.dumps(st, indent=2, ensure_ascii=True) + '\n', encoding='ascii', newline='\n')


# ------------------------------------------------------------------------------------------ reads

def head(s3, key):
    from botocore.exceptions import ClientError
    try:
        h = s3.head_object(Bucket=BUCKET, Key=key)
    except ClientError as e:
        if e.response.get('Error', {}).get('Code') in ('404', 'NoSuchKey', 'NotFound'):
            return None
        raise
    return {'VersionId': h.get('VersionId'), 'LastModified': h['LastModified'].astimezone(dt.timezone.utc).isoformat(),
            'ContentLength': h.get('ContentLength'), 'ContentEncoding': h.get('ContentEncoding'),
            'ContentType': h.get('ContentType'), 'CacheControl': h.get('CacheControl')}


def listing(s3):
    rows = {}
    for page in s3.get_paginator('list_objects_v2').paginate(Bucket=BUCKET, Prefix=PREFIX):
        for o in page.get('Contents', []):
            rows[o['Key']] = {'LastModified': o['LastModified'].astimezone(dt.timezone.utc).isoformat(), 'Size': o['Size']}
    return rows


def print_heads_and_listing(s3, label):
    hs = {}
    for key in (SHARED_KEY, AGG_KEY, PLATINUM_KEY):
        h = head(s3, key)
        hs[key] = h
        if h is None:
            out('%s HEAD %s ABSENT (404)' % (label, key))
        else:
            out('%s HEAD %s VersionId %s LastModified %s ContentLength %s ContentEncoding %s'
                % (label, key, h['VersionId'], h['LastModified'], h['ContentLength'], h['ContentEncoding']))
    ls = listing(s3)
    out('%s LIST s3://%s/%s  %d key(s) (list_objects_v2, paginated, counted client-side)' % (label, BUCKET, PREFIX, len(ls)))
    for k in sorted(ls):
        out('%s     %-60s LastModified %s Size %d' % (label, k, ls[k]['LastModified'], ls[k]['Size']))
    return hs, ls


def recorded_events(sf):
    """The latest execution that ran GeneratePositioning, with BOTH recorded Lambda inputs from it."""
    arn = None
    for page in sf.get_paginator('list_state_machines').paginate():
        for m in page['stateMachines']:
            if m['name'] == STATE_MACHINE_NAME:
                arn = m['stateMachineArn']
    if not arn:
        raise SystemExit('ERROR: state machine %s not found' % STATE_MACHINE_NAME)
    running = []
    for page in sf.get_paginator('list_executions').paginate(stateMachineArn=arn, statusFilter='RUNNING'):
        running.extend(e['executionArn'] for e in page['executions'])
    out('STATE MACHINE %s RUNNING executions: %d %s' % (STATE_MACHINE_NAME, len(running), running))
    scanned = 0
    for page in sf.get_paginator('list_executions').paginate(stateMachineArn=arn):
        for ex in page['executions']:
            scanned += 1
            events = []
            for hp in sf.get_paginator('get_execution_history').paginate(executionArn=ex['executionArn'], includeExecutionData=True):
                events.extend(hp['events'])
            by_id = {e['id']: e for e in events}
            found = {}
            for e in events:
                if e['type'] != 'LambdaFunctionScheduled':
                    continue
                prev = by_id.get(e.get('previousEventId'), {})
                name = (prev.get('stateEnteredEventDetails') or {}).get('name')
                if prev.get('type') == 'TaskStateEntered' and name in (GEN_STATE, INV_STATE) and name not in found:
                    d = e['lambdaFunctionScheduledEventDetails']
                    if (d.get('inputDetails') or {}).get('truncated'):
                        raise SystemExit('ERROR: recorded %s input is truncated in %s' % (name, ex['executionArn']))
                    found[name] = {'resource': d.get('resource'), 'input': d['input'], 'event_id': e['id']}
            if GEN_STATE in found:
                if INV_STATE not in found:
                    raise SystemExit('ERROR: %s ran %s but has no recorded %s input' % (ex['executionArn'], GEN_STATE, INV_STATE))
                return {'execution_arn': ex['executionArn'], 'execution_status': ex['status'],
                        'execution_start': str(ex['startDate']), 'executions_scanned': scanned,
                        'running': running, 'events': found}
    raise SystemExit('ERROR: no execution of %s ran %s (%d scanned)' % (STATE_MACHINE_NAME, GEN_STATE, scanned))


def get_json(s3, key, version_id):
    o = s3.get_object(Bucket=BUCKET, Key=key, VersionId=version_id)
    raw = o['Body'].read()
    if o.get('VersionId') != version_id:
        raise SystemExit('ERROR: asked %s VersionId %s, got %s' % (key, version_id, o.get('VersionId')))
    return json.loads(gunzip(raw).decode('utf-8')), len(raw), sha(raw)


# ------------------------------------------------------------------------------------------ drive

def mode_drive():
    import boto3
    from botocore.config import Config
    st = load_state()
    if st.get('generator_invoked_at'):
        out('REFUSED: %s records a generator invoke at %s; this driver invokes once.' % (STATE.name, st['generator_invoked_at']))
        return 2
    s3, sf = clients()
    lam = boto3.client('lambda', region_name=REGION,
                       config=Config(read_timeout=900, connect_timeout=30, retries={'total_max_attempts': 1, 'mode': 'standard'}))
    out('DRIVER a3_drive_and_read.py at %s (HEAD %s) %s' % (WS.as_posix(), subprocess.run(
        ['git', 'rev-parse', '--short=10', 'HEAD'], cwd=str(WS), capture_output=True, text=True).stdout.strip(), now()))
    out('== BEFORE ==')
    hb, lb = print_heads_and_listing(s3, 'BEFORE')
    ev = recorded_events(sf)
    if ev['running']:
        out('REFUSED: an execution of %s is RUNNING; a concurrent writer would confound the served read.' % STATE_MACHINE_NAME)
        return 2
    gen, inv = ev['events'][GEN_STATE], ev['events'][INV_STATE]
    out('EVENT execution_arn %s (status %s, started %s; executions scanned newest-first: %d)'
        % (ev['execution_arn'], ev['execution_status'], ev['execution_start'], ev['executions_scanned']))
    for label, e in ((GEN_STATE, gen), (INV_STATE, inv)):
        out('EVENT %-20s resource %s history event %s raw input %d chars sha256 %s'
            % (label, e['resource'], e['event_id'], len(e['input']), sha(e['input'].encode('utf-8'))))
    out('EVENT %s input: %s' % (INV_STATE, inv['input']))
    gcfg = lam.get_function_configuration(FunctionName=GEN_FN)
    out('DEPLOYED %s CodeSha256 %s LastModified %s (the bytes this invoke runs)' % (GEN_FN, gcfg['CodeSha256'], gcfg['LastModified']))
    st.update({'to_id': 'POSN_AGGFIX.TO-A3-1', 'author': '0.9.0_WK_POSN_AGGFIX~1', 'execution_arn': ev['execution_arn'],
               'generator_input_sha256': sha(gen['input'].encode('utf-8')), 'invalidation_input_sha256': sha(inv['input'].encode('utf-8')),
               'generator_code_sha256': gcfg['CodeSha256'], 'before': {'heads': hb, 'listing': lb},
               'generator_invoked_at': now()})
    save_state(st)
    out('== INVOKE %s (RequestResponse, retries disabled) %s ==' % (GEN_FN, st['generator_invoked_at']))
    r = lam.invoke(FunctionName=GEN_FN, InvocationType='RequestResponse', LogType='Tail', Payload=gen['input'].encode('utf-8'))
    payload = r['Payload'].read().decode('utf-8')
    out('INVOKE %s StatusCode %s FunctionError %s ExecutedVersion %s' % (GEN_FN, r.get('StatusCode'), r.get('FunctionError', 'none'), r.get('ExecutedVersion')))
    out('INVOKE %s response payload: %s' % (GEN_FN, payload))
    out('INVOKE %s log tail:' % GEN_FN)
    for line in base64.b64decode(r.get('LogResult', '')).decode('utf-8', 'replace').splitlines():
        out('    ' + line)
    st['generator_result'] = {'StatusCode': r.get('StatusCode'), 'FunctionError': r.get('FunctionError'), 'payload': payload}
    save_state(st)
    if r.get('FunctionError'):
        out('STOP: the generator returned FunctionError; the invalidation is NOT invoked.')
        return 1
    st['invalidation_invoked_at'] = now()
    save_state(st)
    out('== INVOKE %s (RequestResponse, retries disabled) %s ==' % (INV_FN, st['invalidation_invoked_at']))
    r2 = lam.invoke(FunctionName=INV_FN, InvocationType='RequestResponse', LogType='Tail', Payload=inv['input'].encode('utf-8'))
    p2 = r2['Payload'].read().decode('utf-8')
    out('INVOKE %s StatusCode %s FunctionError %s' % (INV_FN, r2.get('StatusCode'), r2.get('FunctionError', 'none')))
    out('INVOKE %s response payload: %s' % (INV_FN, p2))
    st['invalidation_result'] = {'StatusCode': r2.get('StatusCode'), 'FunctionError': r2.get('FunctionError'), 'payload': p2}
    save_state(st)
    out('== AFTER ==')
    ha, la = print_heads_and_listing(s3, 'AFTER ')
    st['after'] = {'heads': ha, 'listing': la}
    prior = (hb.get(SHARED_KEY) or {}).get('VersionId')
    new = (ha.get(SHARED_KEY) or {}).get('VersionId')
    st['shared_prior_version_id'], st['shared_new_version_id'] = prior, new
    st['agg_version_id'] = (ha.get(AGG_KEY) or {}).get('VersionId')
    save_state(st)
    moved = prior != new
    out('SHARED FILE VersionId prior %s new %s -> %s' % (prior, new, 'MOVED' if moved else 'NOT MOVED'))
    out('OPAL-ONLY KEY before %s after %s' % ('ABSENT' if hb.get(AGG_KEY) is None else 'PRESENT ' + hb[AGG_KEY]['VersionId'],
                                              'ABSENT' if ha.get(AGG_KEY) is None else 'PRESENT ' + ha[AGG_KEY]['VersionId']))
    others = sorted((set(lb) | set(la)) - {SHARED_KEY, AGG_KEY})
    changed = [k for k in others if lb.get(k) != la.get(k)]
    for k in others:
        out('OTHER %-60s before %s after %s %s' % (k, (lb.get(k) or {}).get('LastModified', 'ABSENT'),
                                                  (la.get(k) or {}).get('LastModified', 'ABSENT'), 'MOVED' if k in changed else 'unchanged'))
    out('OTHER KEYS UNDER %s UNCHANGED: %d of %d%s' % (PREFIX, len(others) - len(changed), len(others),
                                                     '' if not changed else '  MOVED: ' + ', '.join(changed)))
    st['other_keys_moved'] = changed
    st['other_keys_count'] = len(others)
    save_state(st)
    ok = moved and ha.get(AGG_KEY) is not None and not changed
    out('A3-AC8 %s' % ('ALL CHECKS HOLD' if ok else 'A CHECK FAILED -- BRANCH B TRIGGER'))
    return 0 if ok else 1


# ---------------------------------------------------------------------------------------- compare

def vdiff(a, b, path='$', acc=None, order=None):
    """Parsed-value difference: dict key ORDER ignored (counted separately), list order compared."""
    acc = [] if acc is None else acc
    if isinstance(a, dict) and isinstance(b, dict):
        if order is not None and set(a) == set(b) and list(a) != list(b):
            order.append(path)
        for k in list(a) + [k for k in b if k not in a]:
            if k not in b:
                acc.append('%s.%s (present only in prior)' % (path, k))
            elif k not in a:
                acc.append('%s.%s (present only in new)' % (path, k))
            else:
                vdiff(a[k], b[k], '%s.%s' % (path, k), acc, order)
    elif isinstance(a, list) and isinstance(b, list):
        if len(a) != len(b):
            acc.append('%s (value: list length %d vs %d)' % (path, len(a), len(b)))
        for i, (x, y) in enumerate(zip(a, b)):
            vdiff(x, y, '%s[%d]' % (path, i), acc, order)
    elif type(a) is not type(b) or a != b:
        acc.append('%s (value) %s -> %s' % (path, json.dumps(a)[:80], json.dumps(b)[:80]))
    return acc


def classify(paths):
    rows = []
    for p in paths:
        hit = [name for rx, name in PERMITTED if rx.search(p)]
        rows.append((p, hit[0] if hit else None))
    return rows


def book_non_aum(prior, new, code):
    x = dict(prior['current_holdings'][code])
    y = dict(new['current_holdings'][code])
    x.pop('aum', None)
    y.pop('aum', None)
    return vdiff(x, y, '$.current_holdings.%s' % code), sorted(set(x) | set(y))


def mode_compare():
    st = load_state()
    prior_v, new_v, agg_v = st.get('shared_prior_version_id'), st.get('shared_new_version_id'), st.get('agg_version_id')
    if not (prior_v and new_v and agg_v):
        out('ERROR: %s lacks the prior/new/aggregate VersionIds (run the drive first)' % STATE.name)
        return 2
    s3, _ = clients()
    P, pn, ps = get_json(s3, SHARED_KEY, prior_v)
    N, nn, ns = get_json(s3, SHARED_KEY, new_v)
    A, an, as_ = get_json(s3, AGG_KEY, agg_v)
    out('READ %s prior VersionId %s (%d bytes stored, sha256 %s)' % (SHARED_KEY, prior_v, pn, ps[:16]))
    out('READ %s new   VersionId %s (%d bytes stored, sha256 %s)' % (SHARED_KEY, new_v, nn, ns[:16]))
    out('READ %s       VersionId %s (%d bytes stored, sha256 %s)' % (AGG_KEY, agg_v, an, as_[:16]))
    out('COMPARE GRAIN: parsed JSON values, dict key order ignored, list order compared (never-widen ADDENDA, row W1-S7)')
    pk, nk = list(P.get('current_holdings', {})), list(N.get('current_holdings', {}))
    out('current_holdings keys prior = %s' % ' '.join(pk))
    out('current_holdings keys new = %s' % ' '.join(nk))
    checks = [pk == CODES + ['AGG'], nk == CODES]
    n_books = 0
    for code in CODES:
        d, fields = book_non_aum(P, N, code)
        n_books += not d
        out('BOOK %s %s (fields compared: %s; holdings prior %d new %d; aum prior %s new %s)'
            % (code, 'NON-AUM IDENTICAL' if not d else 'NON-AUM DIFFERS', ','.join(f for f in fields if f != 'aum'),
               len(P['current_holdings'][code].get('holdings') or []), len(N['current_holdings'][code].get('holdings') or []),
               P['current_holdings'][code].get('aum'), N['current_holdings'][code].get('aum')))
        for p in d[:20]:
            out('    ' + p)
    out('BOOKS NON-AUM IDENTICAL %d of %d' % (n_books, len(CODES)))
    checks.append(n_books == len(CODES))
    # each book's aum against its own platinum row at the VersionId the run read
    ws = A.get('weights_source') or {}
    plat_v = ws.get('version_id')
    std = json.loads((WS / STANDARD_REL).read_text(encoding='utf-8'))
    primary = {m['served_name']: m['code'] for m in std['primary_models']}
    plat_head_before = ((st.get('before') or {}).get('heads') or {}).get(PLATINUM_KEY) or {}
    plat_head_after = ((st.get('after') or {}).get('heads') or {}).get(PLATINUM_KEY) or {}
    out('PLATINUM VersionId the run read (opal_aggregate.json weights_source.version_id) %s period %s; head before the drive %s, after %s'
        % (plat_v, ws.get('period'), plat_head_before.get('VersionId'), plat_head_after.get('VersionId')))
    o = s3.get_object(Bucket=BUCKET, Key=PLATINUM_KEY, VersionId=plat_v)
    plat = json.loads(gunzip(o['Body'].read()).decode('utf-8'))
    n_aum = 0
    for code in CODES:
        rows = [r for r in plat.get('by_model', []) if primary.get(r.get('model_name')) == code]
        val = rows[0]['aum'] if len(rows) == 1 else None
        eq = len(rows) == 1 and N['current_holdings'][code].get('aum') == val
        n_aum += eq
        out('BOOK %-3s new aum %r | platinum row %r aum %r (VersionId %s) %s'
            % (code, N['current_holdings'][code].get('aum'), rows[0]['model_name'] if rows else None, val, plat_v, 'EQUAL' if eq else 'NOT EQUAL'))
    out('BOOK AUM EQUAL TO ITS OWN ROW %d of %d' % (n_aum, len(CODES)))
    checks.append(n_aum == len(CODES))
    keys = [k for k in list(P) + [k for k in N if k not in P] if k not in ('generated_at', 'current_holdings')]
    top = {k: vdiff(P.get(k, '<ABSENT>'), N.get(k, '<ABSENT>'), '$.' + k) if (k in P and k in N) else ['$.%s (present only in %s)' % (k, 'prior' if k in P else 'new')] for k in keys}
    bad = [k for k in keys if top[k]]
    out('TOP-LEVEL keys compared (%d): %s' % (len(keys), ', '.join(keys)))
    out('TOP-LEVEL keys excluded: generated_at (prior %s, new %s), current_holdings (per book above)' % (P.get('generated_at'), N.get('generated_at')))
    out('TOP-LEVEL IDENTICAL' if not bad else 'TOP-LEVEL DIFFERS on: %s' % ', '.join(bad))
    for k in bad:
        for p in top[k][:20]:
            out('    ' + p)
    checks.append(not bad)
    # the Opal-only payload
    w = A.get('weights') or {}
    m = A.get('members') or {}
    ms = (A.get('reconciliation') or {}).get('members_sum')
    wsum = sum(w.values()) if w else float('nan')
    out('OPAL_AGGREGATE status %s reason %r data_as_of %s generated_at %s holdings %d total_aum %r'
        % (A.get('status'), A.get('reason'), A.get('data_as_of'), A.get('generated_at'),
           len(((A.get('current_holdings') or {}).get('AGG') or {}).get('holdings') or []),
           ((A.get('current_holdings') or {}).get('AGG') or {}).get('total_aum')))
    out('OPAL_AGGREGATE weights_source %s' % json.dumps(ws))
    out('OPAL_AGGREGATE weights sum %r |1-sum| %.3e %s' % (wsum, abs(wsum - 1.0), 'WITHIN 1e-9' if abs(wsum - 1.0) <= 1e-9 else 'OUTSIDE 1e-9'))
    maxd = 0.0
    for k in CODES:
        d = abs(w[k] - m[k] / ms)
        maxd = max(maxd, d)
        out('    weight %-3s %.15f  members[%s]/members_sum %.15f  |diff| %.3e' % (k, w[k], k, m[k] / ms, d))
    out('OPAL_AGGREGATE each weight == members[code]/members_sum: max |diff| %.3e over %d of %d (tolerance 1e-12)' % (maxd, len(CODES), len(CODES)))
    checks += [A.get('status') == 'OK', abs(wsum - 1.0) <= 1e-9, maxd <= 1e-12]
    # the whole served delta, classified against the four permitted classes
    order = []
    delta = vdiff(P, N, '$', None, order)
    rows = classify(delta)
    out('SERVED DELTA (shared file, parsed values): %d path(s); dicts whose key order alone differs: %d (not a difference)' % (len(rows), len(order)))
    agg_rows = [p for p, c in rows if c == 'current_holdings.AGG removed']
    for p, c in rows:
        out('    %-12s %s%s' % ('PERMITTED' if c else 'NOT PERMITTED', p, ('  [' + c + ']') if c else ''))
    not_permitted = [p for p, c in rows if not c]
    moved = st.get('other_keys_moved') or []
    out('OTHER KEYS UNDER %s MOVED (from the drive): %d of %s' % (PREFIX, len(moved), st.get('other_keys_count')))
    out('NEW KEY %s present VersionId %s status %s' % (AGG_KEY, agg_v, A.get('status')))
    # controls
    c1 = copy.deepcopy(N)
    h0 = c1['current_holdings']['UST']['holdings'][0]
    h0['weight'] = h0['weight'] + 0.0001
    cd, _ = book_non_aum(P, c1, 'UST')
    c1_np = [p for p, c in classify(vdiff(P, c1)) if not c]
    out('CONTROL 1 (in memory: new UST holdings[0] %s weight +0.0001): BOOK UST %s; classifier NOT PERMITTED paths %d -> %s'
        % (h0.get('ticker'), 'NON-AUM DIFFERS' if cd else 'NON-AUM IDENTICAL', len(c1_np), 'FIRED' if (cd and c1_np) else 'DID NOT FIRE'))
    c2 = copy.deepcopy(N)
    c2['current_holdings']['UST'] = dict(reversed(list(c2['current_holdings']['UST'].items())))
    c2_d = vdiff(N, c2)
    out('CONTROL 2 (in memory: key order of new current_holdings.UST reversed): value paths %d -> %s'
        % (len(c2_d), 'KEY ORDER IGNORED' if not c2_d else 'KEY ORDER READ AS A DIFFERENCE'))
    controls_ok = bool(cd and c1_np) and not c2_d
    branch_a = all(checks) and not not_permitted and not moved and len(agg_rows) == 1
    out('CHECKS HOLD %d of %d; NOT PERMITTED served paths %d; other keys moved %d; controls %s'
        % (sum(bool(c) for c in checks), len(checks), len(not_permitted), len(moved), 'FIRED AS EXPECTED' if controls_ok else 'DID NOT BEHAVE'))
    out('BRANCH A' if branch_a else 'BRANCH B')
    return 0 if (branch_a and controls_ok) else 1


# ------------------------------------------------------------------------------------- satellites

def mode_satellites():
    st = load_state()
    prior_v, new_v = st.get('shared_prior_version_id'), st.get('shared_new_version_id')
    if not (prior_v and new_v):
        out('ERROR: %s lacks the prior/new VersionIds (run the drive first)' % STATE.name)
        return 2
    path = WS / SATELLITES_REL
    spec = importlib.util.spec_from_file_location('build_satellites_characteristics', str(path))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    blob = subprocess.run(['git', 'rev-parse', 'HEAD:' + SATELLITES_REL], cwd=str(WS), capture_output=True, text=True).stdout.strip()
    out('IMPORTED %s by path (sha256 %s, HEAD blob %s); yang_index at line %d'
        % (SATELLITES_REL, sha(path.read_bytes())[:16], blob[:12], mod.yang_index.__code__.co_firstlineno))
    s3, _ = clients()
    P, _, _ = get_json(s3, SHARED_KEY, prior_v)
    N, _, _ = get_json(s3, SHARED_KEY, new_v)
    po, pc, pe = mod.yang_index(P)
    no, nc, ne = mod.yang_index(N)
    out('PRIOR VersionId %s: current_holdings books %s; out tickers %d; extra tickers %d; conflicts %d %s'
        % (prior_v, list(P.get('current_holdings', {})), len(po), len(pe), len(pc), pc))
    out('NEW   VersionId %s: current_holdings books %s; out tickers %d; extra tickers %d; conflicts %d %s'
        % (new_v, list(N.get('current_holdings', {})), len(no), len(ne), len(nc), nc))
    out_same, extra_same = po == no, pe == ne
    out('OUT MAPS %s (ticker count prior %d new %d)' % ('IDENTICAL' if out_same else 'DIFFER', len(po), len(no)))
    if not out_same:
        for t in sorted(set(po) | set(no)):
            if po.get(t) != no.get(t):
                out('    out differs %s: prior %s new %s' % (t, json.dumps(po.get(t))[:120], json.dumps(no.get(t))[:120]))
    out('EXTRA MAPS %s (ticker count prior %d new %d)' % ('IDENTICAL' if extra_same else 'DIFFER', len(pe), len(ne)))
    if not extra_same:
        for t in sorted(set(pe) | set(ne)):
            if pe.get(t) != ne.get(t):
                out('    extra differs %s: prior %s new %s' % (t, json.dumps(pe.get(t)), json.dumps(ne.get(t))))
    only_p, only_n = [t for t in pc if t not in nc], [t for t in nc if t not in pc]
    out('CONFLICTS prior %s' % json.dumps(pc))
    out('CONFLICTS new   %s' % json.dumps(nc))
    out('CONFLICTS DIFFERENCE: only in prior %d %s; only in new %d %s%s'
        % (len(only_p), json.dumps(only_p), len(only_n), json.dumps(only_n), '  (EMPTY DIFFERENCE)' if not (only_p or only_n) else ''))
    for t in only_p:
        rows = []
        for book, b in (P.get('current_holdings') or {}).items():
            for r in (b.get('holdings') if isinstance(b, dict) else b) or []:
                if (r.get('ticker') or '').strip().upper() == t:
                    keep = {f: mod._clean(r.get(f)) for f in mod.SCALAR_FIELDS}
                    keep['returns'] = {k: mod._clean(v) for k, v in (r.get('returns') or {}).items()}
                    rows.append((book, keep))
        first = rows[0][1] if rows else {}
        for book, keep in rows:
            diffs = sorted(k for k in set(first) | set(keep) if first.get(k) != keep.get(k))
            out('    prior conflict %s book %-3s differs from first occurrence (%s) on: %s' % (t, book, rows[0][0], diffs or 'nothing'))
    return 0 if (out_same and extra_same) else 1


def main():
    ap = argparse.ArgumentParser(description=__doc__.split('\n')[0])
    g = ap.add_mutually_exclusive_group()
    g.add_argument('--read-only-compare', action='store_true')
    g.add_argument('--satellites-reader', action='store_true')
    a = ap.parse_args()
    if a.read_only_compare:
        return mode_compare()
    if a.satellites_reader:
        return mode_satellites()
    return mode_drive()


if __name__ == '__main__':
    sys.exit(main())
