#!/usr/bin/env python3
"""<PRODUCER_HARNESS_A2> -- POSN_AGGFIX.TO-A2-1 (cells AF1-s-6, AF1-s-7, AF1-s-8).

Runs yang-generate-positioning's lambda_handler (and, for --cli-upload, main() --upload) in separate
subprocesses with AWS_LAMBDA_FUNCTION_NAME set: BEFORE = lambda_function.py at the fixed anchor
605c03f81f, AFTER = the working file. The event is the RAW input string the YangDataPipeline state
machine passed to GeneratePositioning in its latest execution that ran it (get-execution-history,
read-only). A botocore wrapper passes every READ call through to the real service and CAPTURES every
S3 put/upload/delete/copy to .scratch/ WITHOUT calling the service; any other non-read call aborts the
run. Nothing is served.

Modes (one per criterion): --membership-equals-standard (A2-AC2), --compare (A2-AC3), --book-aum
(A2-AC4), --aggregate-payload (A2-AC5), --hand-rederive (A2-AC6), --fail-weights (A2-AC7),
--partial-weights (A2-AC8), --cli-upload (A2-AC13). The normal-run modes share one cached pair of runs
under .scratch/a2/runs/normal-*; every mode prints which run directory it read and whether it ran it now
or read it cached. A cached run is reused only when its source sha256 and event execution ARN still
match. --fresh re-runs and prints a determinism comparison against the previous run.

Author: 0.9.0_WK_POSN_AGGFIX~1, 2026-09-15.
"""
import argparse
import ast
import gzip
import hashlib
import io
import json
import os
import shutil
import subprocess
import sys
import time
import traceback
from pathlib import Path

HERE = Path(__file__).resolve().parent
WS = Path(subprocess.run(['git', 'rev-parse', '--show-toplevel'], cwd=str(HERE), capture_output=True,
                         text=True, check=True).stdout.strip())
PRODUCER_REL = 'infra/aws/lambda/v2_portal/yang_pipeline/positioning/yang-generate-positioning/lambda_function.py'
CLASSIFIER_REL = 'infra/aws/lambda/v2_portal/yang_pipeline/positioning/yang-generate-positioning/etf_classifications_dynamodb.py'
STANDARD_REL = 'org/standards/POSN_AGGREGATE_MODEL_SET.json'
BEFORE_COMMIT = '605c03f81f'
SCRATCH = WS / '.scratch' / 'a2'
RUNS = SCRATCH / 'runs'
STATE_MACHINE_NAME = 'YangDataPipeline'
TASK_STATE = 'GeneratePositioning'
FUNCTION_NAME = 'yang-generate-positioning'
BUCKET = 'opal-data-portal-v2'
SHARED_KEY = 'json/positioning/positioning_data.json'
AGG_KEY = 'json/positioning/opal_aggregate.json'
PLATINUM_KEY = 'platinum/mdpf/global/aum-metrics.json'
LEGACY_KEY = 'json/portfolios/aum-metrics.json'
CODES = ['UST', 'ST', 'INT', 'LT', 'ULT']
# The ULT row's names in either file: the standard's served name plus the BEFORE producer's aliases.
ULT_NAMES = {'Long-Term Aggressive', 'Long Term Aggressive', 'Ultra-Long Term', 'Ultra Long Term'}
READ_PREFIXES = ('Get', 'List', 'Head', 'Describe', 'Query', 'Scan', 'BatchGet', 'Select')
CAPTURE_OPS = {'PutObject', 'CreateMultipartUpload', 'UploadPart', 'CompleteMultipartUpload',
               'AbortMultipartUpload', 'DeleteObject', 'DeleteObjects', 'CopyObject', 'UploadPartCopy'}
# SAME INPUTS includes the process hash seed. Measured 2026-09-15 with it unpinned: two runs of the SAME
# BEFORE source differ byte-wise in portfolios.<code>.benchmark.spread.segment.{sector,geography,maturity}
# key ORDER (set iteration under hash randomization) while equal with sorted keys. Every run pins this seed.
HASH_SEED = '0'
CONTRACT_TOP = ['status', 'reason', 'generated_at', 'data_as_of', 'current_holdings', 'weights',
                'weights_source', 'members', 'left_out', 'reconciliation']
RECON_KEYS = ['five_primary_sum', 'members_sum', 'file_total_model_aum', 'gap', 'gap_explanation_ref']


def sha256_bytes(b):
    return hashlib.sha256(b).hexdigest()


def canon(obj):
    """The producer's own serialization (key order preserved) -- the byte grain the criteria name."""
    return json.dumps(obj, separators=(',', ':'))


def maybe_gunzip(b):
    return gzip.decompress(b) if b[:2] == b'\x1f\x8b' else b


# =============================================================================================
# RUNNER (inside the subprocess)
# =============================================================================================

def _runner(run_dir):
    import botocore.client
    import botocore.exceptions
    import botocore.response

    run_dir = Path(run_dir)
    cfg = json.loads((run_dir / 'config.json').read_text(encoding='utf-8'))
    cap_dir = run_dir / 'captures'
    cap_dir.mkdir(parents=True, exist_ok=True)
    reads, captures, faults, counts = [], [], [], {}
    orig = botocore.client.BaseClient._make_api_call
    fault = cfg.get('fault') or {}

    def write_manifest(status, extra=None):
        doc = {'status': status, 'reads_s3': reads, 'read_call_counts': counts, 'captures': captures,
               'faults': faults}
        doc.update(extra or {})
        (run_dir / 'wrapper.json').write_text(json.dumps(doc, indent=1, default=str), encoding='utf-8')

    def patched(self, operation_name, api_params):
        svc = self.meta.service_model.service_name
        if svc == 's3' and operation_name in CAPTURE_OPS:
            body = api_params.get('Body')
            if body is not None and not isinstance(body, (bytes, bytearray)):
                body = body.read()
            body = bytes(body or b'')
            seq = len(captures) + 1
            key = str(api_params.get('Key', ''))
            fname = '%02d_%s_%s.bin' % (seq, operation_name, key.replace('/', '__'))
            (cap_dir / fname).write_bytes(body)
            meta = {k: v for k, v in api_params.items() if k != 'Body'}
            captures.append({'seq': seq, 'operation': operation_name, 'params': meta, 'body_file': fname,
                             'body_bytes': len(body), 'body_sha256': sha256_bytes(body)})
            write_manifest('RUNNING')
            resp = {'ETag': '"harness-captured"', 'VersionId': 'HARNESS-CAPTURED-NOT-SERVED',
                    'ResponseMetadata': {'HTTPStatusCode': 200}}
            if operation_name == 'CreateMultipartUpload':
                resp['UploadId'] = 'HARNESS-CAPTURED'
            return resp
        if operation_name.startswith(READ_PREFIXES):
            ck = '%s.%s' % (svc, operation_name)
            counts[ck] = counts.get(ck, 0) + 1
            key = api_params.get('Key') if svc == 's3' else None
            if svc == 's3' and operation_name == 'GetObject' and fault.get('kind') == 'fail' and key == fault.get('key'):
                faults.append({'kind': 'fail', 'key': key})
                write_manifest('RUNNING')
                raise botocore.exceptions.ClientError(
                    {'Error': {'Code': 'HarnessInjectedFailure', 'Message': 'harness: injected read failure on %s' % key}},
                    operation_name)
            resp = orig(self, operation_name, api_params)
            if svc == 's3' and operation_name == 'GetObject':
                rec = {'bucket': api_params.get('Bucket'), 'key': key, 'VersionId': resp.get('VersionId'),
                       'ContentLength': resp.get('ContentLength'), 'LastModified': str(resp.get('LastModified'))}
                if str(key).endswith('aum-metrics.json'):
                    raw = resp['Body'].read()
                    fname = 'read_%s.json' % str(key).replace('/', '__')
                    (run_dir / fname).write_bytes(raw)
                    rec['body_file'] = fname
                    served = raw
                    if fault.get('kind') == 'drop_ult' and key == fault.get('key'):
                        doc = json.loads(maybe_gunzip(raw).decode('utf-8'))
                        kept = [r for r in doc.get('by_model', []) if r.get('model_name') not in ULT_NAMES]
                        removed = [r for r in doc.get('by_model', []) if r.get('model_name') in ULT_NAMES]
                        doc['by_model'] = kept
                        served = json.dumps(doc).encode('utf-8')
                        sfname = 'served_%s.json' % str(key).replace('/', '__')
                        (run_dir / sfname).write_bytes(served)
                        rec['served_body_file'] = sfname
                        faults.append({'kind': 'drop_ult', 'key': key, 'removed_rows': removed,
                                       'rows_before': len(kept) + len(removed), 'rows_served': len(kept)})
                    resp['Body'] = botocore.response.StreamingBody(io.BytesIO(served), len(served))
                reads.append(rec)
                write_manifest('RUNNING')
            return resp
        write_manifest('ABORTED', {'aborted_on': '%s.%s' % (svc, operation_name)})
        print('HARNESS ABORT: non-read, non-captured call %s.%s' % (svc, operation_name), flush=True)
        os._exit(3)

    botocore.client.BaseClient._make_api_call = patched
    sys.dont_write_bytecode = True
    sys.path.insert(0, cfg['src_dir'])
    import importlib.util
    spec = importlib.util.spec_from_file_location('lambda_function', str(Path(cfg['src_dir']) / 'lambda_function.py'))
    mod = importlib.util.module_from_spec(spec)
    sys.modules['lambda_function'] = mod
    started = time.time()
    try:
        spec.loader.exec_module(mod)
        if cfg['kind'] == 'handler':
            event = json.loads(cfg['event_raw'])
            result = mod.lambda_handler(event, None)
            extra = {'handler_return': result}
        else:
            sys.argv = ['lambda_function.py'] + cfg['cli_argv']
            rc = mod.main()
            extra = {'main_return': rc}
        extra['module_file'] = mod.__file__
        extra['seconds'] = round(time.time() - started, 1)
        write_manifest('COMPLETED', extra)
        return 0
    except Exception:
        write_manifest('RAISED', {'traceback': traceback.format_exc(), 'module_file': getattr(mod, '__file__', None)})
        traceback.print_exc()
        return 1


# =============================================================================================
# HARNESS SIDE
# =============================================================================================

def git_show(commit, rel):
    r = subprocess.run(['git', 'show', '%s:%s' % (commit, rel)], cwd=str(WS), capture_output=True, check=True)
    if not r.stdout:
        raise SystemExit('ERROR: git show %s:%s returned empty bytes' % (commit, rel))
    return r.stdout


def before_src_dir():
    d = SCRATCH / 'src_before'
    d.mkdir(parents=True, exist_ok=True)
    for rel in (PRODUCER_REL, CLASSIFIER_REL):
        (d / Path(rel).name).write_bytes(git_show(BEFORE_COMMIT, rel))
    return d


def recorded_event():
    import boto3
    sf = boto3.client('stepfunctions', region_name='us-east-1')
    arn = None
    for page in sf.get_paginator('list_state_machines').paginate():
        for m in page['stateMachines']:
            if m['name'] == STATE_MACHINE_NAME:
                arn = m['stateMachineArn']
    if not arn:
        raise SystemExit('ERROR: state machine %s not found' % STATE_MACHINE_NAME)
    scanned = 0
    for page in sf.get_paginator('list_executions').paginate(stateMachineArn=arn):
        for ex in page['executions']:
            scanned += 1
            events = []
            for hp in sf.get_paginator('get_execution_history').paginate(executionArn=ex['executionArn'],
                                                                          includeExecutionData=True):
                events.extend(hp['events'])
            by_id = {e['id']: e for e in events}
            for e in events:
                if e['type'] != 'LambdaFunctionScheduled':
                    continue
                prev = by_id.get(e.get('previousEventId'), {})
                det = prev.get('stateEnteredEventDetails') or {}
                if prev.get('type') == 'TaskStateEntered' and det.get('name') == TASK_STATE:
                    d = e['lambdaFunctionScheduledEventDetails']
                    if (d.get('inputDetails') or {}).get('truncated'):
                        raise SystemExit('ERROR: recorded input is truncated in %s' % ex['executionArn'])
                    return {'state_machine_arn': arn, 'execution_arn': ex['executionArn'],
                            'execution_status': ex['status'], 'execution_start': str(ex['startDate']),
                            'resource': d.get('resource'), 'event_raw': d['input'],
                            'executions_scanned': scanned}
    raise SystemExit('ERROR: no execution of %s ran %s (%d scanned)' % (STATE_MACHINE_NAME, TASK_STATE, scanned))


def print_event(ev):
    e = json.loads(ev['event_raw'])
    print('EVENT execution_arn   %s (status %s, started %s; executions scanned newest-first: %d)'
          % (ev['execution_arn'], ev['execution_status'], ev['execution_start'], ev['executions_scanned']))
    print('EVENT resource        %s' % ev['resource'])
    print('EVENT model_pkl_key   %s' % e['processed']['model_pkl_key'])
    print('EVENT data_as_of_date %s' % e.get('data_as_of_date'))
    print('EVENT raw input       %d chars, sha256 %s' % (len(ev['event_raw']), sha256_bytes(ev['event_raw'].encode('utf-8'))))


def run(name, arm, kind, ev, fault=None, fresh=False):
    """Run (or read cached) one subprocess run. arm: BEFORE | AFTER."""
    run_dir = RUNS / name
    src_dir = before_src_dir() if arm == 'BEFORE' else (WS / PRODUCER_REL).parent
    src_sha = sha256_bytes((src_dir / 'lambda_function.py').read_bytes())
    cfg_path = run_dir / 'config.json'
    wrap_path = run_dir / 'wrapper.json'
    if run_dir.exists() and cfg_path.exists() and wrap_path.exists() and not fresh:
        cfg = json.loads(cfg_path.read_text(encoding='utf-8'))
        wrap = json.loads(wrap_path.read_text(encoding='utf-8'))
        if (cfg.get('source_sha256') == src_sha and cfg.get('execution_arn') == ev['execution_arn']
                and cfg.get('pythonhashseed') == HASH_SEED and wrap.get('status') == 'COMPLETED'):
            print('RUN %-16s %s %-7s READ CACHED %s (source sha256 %s, PYTHONHASHSEED=%s, finished %s)'
                  % (name, arm, kind, run_dir.relative_to(WS).as_posix(), src_sha[:16], HASH_SEED, cfg.get('finished_at')))
            return run_dir, cfg, wrap
    prev = None
    if run_dir.exists():
        prev = run_dir.with_name(run_dir.name + '.prev')
        if prev.exists():
            shutil.rmtree(prev)
        run_dir.rename(prev)
    run_dir.mkdir(parents=True)
    e = json.loads(ev['event_raw'])
    pkl = e['processed']['model_pkl_key']
    stem = Path(pkl).stem  # model_20260914_v1
    _, date8, version = stem.split('_', 2)
    cfg = {'arm': arm, 'kind': kind, 'src_dir': str(src_dir), 'source_sha256': src_sha,
           'source_label': ('%s@%s' % (PRODUCER_REL, BEFORE_COMMIT)) if arm == 'BEFORE' else ('%s (working file)' % PRODUCER_REL),
           'execution_arn': ev['execution_arn'], 'event_raw': ev['event_raw'], 'fault': fault or {},
           'pythonhashseed': HASH_SEED,
           'cli_argv': ['--date', date8, '--version', version, '--upload', '--output-dir', str(run_dir)],
           'started_at': time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime())}
    cfg_path.write_text(json.dumps(cfg, indent=1), encoding='utf-8')
    env = dict(os.environ)
    env.update({'AWS_LAMBDA_FUNCTION_NAME': FUNCTION_NAME, 'PYTHONDONTWRITEBYTECODE': '1', 'PYTHONIOENCODING': 'utf-8',
                'PYTHONHASHSEED': HASH_SEED})
    with open(run_dir / 'stdout.txt', 'wb') as out:
        p = subprocess.run([sys.executable, str(Path(__file__).resolve()), '--_run', str(run_dir)], cwd=str(run_dir),
                           env=env, stdout=out, stderr=subprocess.STDOUT, timeout=540)
    cfg['finished_at'] = time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime())
    cfg['rc'] = p.returncode
    cfg_path.write_text(json.dumps(cfg, indent=1), encoding='utf-8')
    wrap = json.loads(wrap_path.read_text(encoding='utf-8')) if wrap_path.exists() else {'status': 'NO-MANIFEST'}
    print('RUN %-16s %s %-7s RAN NOW -> %s rc=%d status=%s seconds=%s (source sha256 %s, AWS_LAMBDA_FUNCTION_NAME=%s, PYTHONHASHSEED=%s, fault=%s)'
          % (name, arm, kind, run_dir.relative_to(WS).as_posix(), p.returncode, wrap.get('status'), wrap.get('seconds'),
             src_sha[:16], FUNCTION_NAME, HASH_SEED, json.dumps(fault or {})))
    if wrap.get('status') != 'COMPLETED':
        tail = (run_dir / 'stdout.txt').read_text(encoding='utf-8', errors='replace').splitlines()[-30:]
        print('\n'.join('    | ' + t for t in tail))
        raise SystemExit('ERROR: run %s did not complete (%s)' % (name, wrap.get('status')))
    if prev is not None and fresh:
        determinism(prev, run_dir)
    return run_dir, cfg, wrap


def captured(run_dir, wrap, key):
    hits = [c for c in wrap['captures'] if c['params'].get('Key') == key]
    if not hits:
        return None, None
    if len(hits) > 1:
        raise SystemExit('ERROR: %d captures of %s in %s' % (len(hits), key, run_dir))
    c = hits[0]
    return c, json.loads(maybe_gunzip((run_dir / 'captures' / c['body_file']).read_bytes()).decode('utf-8'))


def aum_read(run_dir, wrap, key, served=False):
    hits = [r for r in wrap['reads_s3'] if r['key'] == key]
    if len(hits) != 1:
        raise SystemExit('ERROR: %d reads of %s in %s' % (len(hits), key, run_dir))
    r = hits[0]
    f = r.get('served_body_file') if served and r.get('served_body_file') else r['body_file']
    return r, json.loads(maybe_gunzip((run_dir / f).read_bytes()).decode('utf-8'))


def diff_paths(a, b, path='$', out=None):
    out = [] if out is None else out
    if isinstance(a, dict) and isinstance(b, dict):
        if set(a.keys()) == set(b.keys()) and list(a.keys()) != list(b.keys()):
            out.append('%s (key order differs: %s vs %s)' % (path, list(a.keys())[:4], list(b.keys())[:4]))
        for k in list(a.keys()) + [k for k in b.keys() if k not in a]:
            if k not in a or k not in b:
                out.append('%s.%s (present only in %s)' % (path, k, 'first' if k in a else 'second'))
            else:
                diff_paths(a[k], b[k], '%s.%s' % (path, k), out)
    elif isinstance(a, list) and isinstance(b, list):
        if len(a) != len(b):
            out.append('%s (list length %d vs %d)' % (path, len(a), len(b)))
        for i, (x, y) in enumerate(zip(a, b)):
            diff_paths(x, y, '%s[%d]' % (path, i), out)
    elif canon(a) != canon(b):
        out.append('%s (%s vs %s)' % (path, canon(a)[:60], canon(b)[:60]))
    return out


def shape(p):
    import re
    return re.sub(r'\[\d+\]', '[*]', p.split(' (')[0])


def print_diff_summary(label, paths, limit=12):
    shapes = {}
    for p in paths:
        shapes[shape(p)] = shapes.get(shape(p), 0) + 1
    print('%s: %d differing leaf path(s) in %d shape(s)' % (label, len(paths), len(shapes)))
    for s, n in sorted(shapes.items(), key=lambda kv: -kv[1])[:limit]:
        print('    %6d  %s' % (n, s))
    for p in paths[:limit]:
        print('    e.g. %s' % p)


def determinism(prev, cur):
    pw = json.loads((prev / 'wrapper.json').read_text(encoding='utf-8'))
    cw = json.loads((cur / 'wrapper.json').read_text(encoding='utf-8'))
    for key in sorted({c['params'].get('Key') for c in cw['captures']}):
        _, a = captured(prev, pw, key)
        _, b = captured(cur, cw, key)
        if a is None or b is None:
            print('DETERMINISM %s: present in one run only' % key)
            continue
        a = dict(a)
        b = dict(b)
        a.pop('generated_at', None)
        b.pop('generated_at', None)
        d = diff_paths(a, b)
        print('DETERMINISM %s vs previous run %s: %s' % (key, prev.name, 'EQUAL except generated_at' if not d else 'DIFFERS (%d paths)' % len(d)))
        if d:
            print_diff_summary('  determinism diff', d)


def print_captures(label, wrap):
    print('%s captured writes: %d (none sent to the service)' % (label, len(wrap['captures'])))
    for c in wrap['captures']:
        p = c['params']
        print('    #%d %s s3://%s/%s  %d bytes sha256 %s  ContentType=%s ContentEncoding=%s CacheControl=%s'
              % (c['seq'], c['operation'], p.get('Bucket'), p.get('Key'), c['body_bytes'], c['body_sha256'][:16],
                 p.get('ContentType'), p.get('ContentEncoding'), p.get('CacheControl')))


def print_same_inputs(bw, aw):
    b = {(r['bucket'], r['key']): r['VersionId'] for r in bw['reads_s3']}
    a = {(r['bucket'], r['key']): r['VersionId'] for r in aw['reads_s3']}
    common = sorted(set(a) & set(b))
    for k in common:
        print('SAME INPUT s3://%s/%s  BEFORE VersionId %s  AFTER VersionId %s  %s'
              % (k[0], k[1], b[k], a[k], 'EQUAL' if a[k] == b[k] else 'DIFFERENT'))
    for k in sorted(set(b) - set(a)):
        print('READ BY BEFORE ONLY s3://%s/%s VersionId %s' % (k[0], k[1], b[k]))
    for k in sorted(set(a) - set(b)):
        print('READ BY AFTER ONLY  s3://%s/%s VersionId %s' % (k[0], k[1], a[k]))
    print('READ CALL COUNTS BEFORE %s' % json.dumps(bw['read_call_counts'], sort_keys=True))
    print('READ CALL COUNTS AFTER  %s' % json.dumps(aw['read_call_counts'], sort_keys=True))


def standard_maps():
    std = json.loads((WS / STANDARD_REL).read_text(encoding='utf-8'))
    primary = {m['served_name']: m['code'] for m in std['primary_models']}
    blends = {b['served_name']: {c['code']: c['share'] for c in b['constituents']} for b in std['blends']}
    return std, primary, blends


def producer_maps():
    tree = ast.parse((WS / PRODUCER_REL).read_text(encoding='utf-8'))
    found = {}
    for n in tree.body:
        if isinstance(n, ast.Assign) and len(n.targets) == 1 and isinstance(n.targets[0], ast.Name):
            if n.targets[0].id in ('AGGREGATE_PRIMARY_MODELS', 'AGGREGATE_BLEND_MODELS'):
                found[n.targets[0].id] = (ast.literal_eval(n.value), n.lineno)
    return found


def before_alias_map():
    tree = ast.parse((before_src_dir() / 'lambda_function.py').read_text(encoding='utf-8'))
    for n in ast.walk(tree):
        if isinstance(n, ast.Assign) and len(n.targets) == 1 and getattr(n.targets[0], 'id', None) == 'model_name_to_code':
            return ast.literal_eval(n.value)
    raise SystemExit('ERROR: model_name_to_code not found in the BEFORE source')


# ----------------------------------------------------------------------------------------- modes

def mode_membership():
    std, s_primary, s_blends = standard_maps()
    found = producer_maps()
    p_primary, p_line = found['AGGREGATE_PRIMARY_MODELS']
    p_blends, b_line = found['AGGREGATE_BLEND_MODELS']
    print('INSTRUMENT ast.literal_eval of the module-level assignments in %s (working file, sha256 %s)'
          % (PRODUCER_REL, sha256_bytes((WS / PRODUCER_REL).read_bytes())[:16]))
    print('STANDARD   %s version %s' % (STANDARD_REL, std['version']))
    print('PRODUCER AGGREGATE_PRIMARY_MODELS (:%d) %d entries: %s' % (p_line, len(p_primary), json.dumps(p_primary, sort_keys=True)))
    print('STANDARD primary served_name -> code  %d entries: %s' % (len(s_primary), json.dumps(s_primary, sort_keys=True)))
    print('PRODUCER AGGREGATE_BLEND_MODELS (:%d) %d entries: %s' % (b_line, len(p_blends), json.dumps(p_blends, sort_keys=True)))
    print('STANDARD blends served_name -> constituents %d entries: %s' % (len(s_blends), json.dumps(s_blends, sort_keys=True)))
    equal = p_primary == s_primary and p_blends == s_blends
    print('MEMBERSHIP EQUAL' if equal else 'MEMBERSHIP DIFFERS')
    mutated = json.loads(json.dumps(p_blends))
    first = sorted(mutated)[0]
    code = sorted(mutated[first])[0]
    mutated[first][code] = 0.4
    c_equal = p_primary == s_primary and mutated == s_blends
    print('CONTROL (in memory: %s share of %s set to 0.4 -> %s): %s'
          % (first, code, json.dumps(mutated[first], sort_keys=True), 'MEMBERSHIP EQUAL (DID NOT FIRE)' if c_equal else 'MEMBERSHIP DIFFERS'))
    return 0 if (equal and not c_equal) else 1


def normal_pair(fresh):
    ev = recorded_event()
    print_event(ev)
    b = run('normal-before', 'BEFORE', 'handler', ev, fresh=fresh)
    a = run('normal-after', 'AFTER', 'handler', ev, fresh=fresh)
    return ev, b, a


def mode_compare(fresh):
    ev, (bd, _, bw), (ad, _, aw) = normal_pair(fresh)
    print('BEFORE handler return %s' % json.dumps(bw.get('handler_return')))
    print('AFTER  handler return %s' % json.dumps(aw.get('handler_return')))
    print_captures('BEFORE', bw)
    print_captures('AFTER ', aw)
    print_same_inputs(bw, aw)
    _, B = captured(bd, bw, SHARED_KEY)
    _, A = captured(ad, aw, SHARED_KEY)
    print('SHARED FILE %s: BEFORE %s, AFTER %s' % (SHARED_KEY, 'captured' if B else 'MISSING', 'captured' if A else 'MISSING'))
    bk = list(B.get('current_holdings', {}).keys())
    ak = list(A.get('current_holdings', {}).keys())
    print('current_holdings keys BEFORE = %s' % ' '.join(bk))
    print('current_holdings keys AFTER  = %s' % ' '.join(ak))
    ok = bk == CODES + ['AGG'] and ak == CODES

    def books_identical(before, after):
        res = {}
        for code in CODES:
            x = dict(before['current_holdings'][code])
            y = dict(after['current_holdings'][code])
            x.pop('aum', None)
            y.pop('aum', None)
            res[code] = (canon(x) == canon(y), list(x.keys()), diff_paths(x, y))
        return res
    res = books_identical(B, A)
    n_ok = 0
    for code in CODES:
        same, fields, d = res[code]
        n_ok += same
        print('BOOK %s %s (fields compared: %s; holdings %d; aum BEFORE %s AFTER %s)'
              % (code, 'NON-AUM IDENTICAL' if same else 'NON-AUM DIFFERS', ','.join(fields),
                 len(A['current_holdings'][code]['holdings']), B['current_holdings'][code].get('aum'),
                 A['current_holdings'][code].get('aum')))
        if d:
            print_diff_summary('    diff', d)
    print('BOOKS NON-AUM IDENTICAL %d of %d' % (n_ok, len(CODES)))
    ok = ok and n_ok == len(CODES)
    keys = [k for k in list(B.keys()) + [k for k in A.keys() if k not in B] if k not in ('generated_at', 'current_holdings')]
    top_diff = [k for k in keys if k not in A or k not in B or canon(A[k]) != canon(B[k])]
    print('TOP-LEVEL keys compared (%d): %s' % (len(keys), ', '.join(keys)))
    print('TOP-LEVEL keys excluded: generated_at (BEFORE %s, AFTER %s), current_holdings (per book above)'
          % (B.get('generated_at'), A.get('generated_at')))
    if top_diff:
        print('TOP-LEVEL DIFFERS on: %s' % ', '.join(top_diff))
        for k in top_diff:
            if k in A and k in B:
                print_diff_summary('    diff %s' % k, diff_paths(B[k], A[k]))
    else:
        print('TOP-LEVEL IDENTICAL')
    ok = ok and not top_diff
    mutated = json.loads(json.dumps(A))
    h = mutated['current_holdings']['UST']['holdings'][0]
    old = h['weight']
    h['weight'] = round(old + 0.0001, 4)
    cres = books_identical(B, mutated)
    fired = not cres['UST'][0]
    print('CONTROL (in memory: AFTER current_holdings.UST.holdings[0] %s weight %s -> %s): BOOK UST %s -> %s'
          % (h['ticker'], old, h['weight'], 'NON-AUM DIFFERS' if fired else 'NON-AUM IDENTICAL',
             'REPORTED AS A DIFFERENCE (FIRED)' if fired else 'NOT REPORTED (DID NOT FIRE)'))
    print('VERDICT A2-AC3 %s' % ('ALL CHECKS HOLD' if (ok and fired) else 'A CHECK FAILED'))
    return 0 if (ok and fired) else 1


def mode_book_aum(fresh):
    ev, (bd, _, bw), (ad, _, aw) = normal_pair(fresh)
    _, s_primary, _ = standard_maps()
    _, B = captured(bd, bw, SHARED_KEY)
    _, A = captured(ad, aw, SHARED_KEY)
    pr, plat = aum_read(ad, aw, PLATINUM_KEY)
    lr, leg = aum_read(bd, bw, LEGACY_KEY)
    alias = before_alias_map()
    print('AFTER read  s3://%s/%s VersionId %s period %s (%d by_model rows)' % (pr['bucket'], pr['key'], pr['VersionId'], plat.get('period'), len(plat.get('by_model', []))))
    print('BEFORE read s3://%s/%s VersionId %s period %s (%d by_model rows)' % (lr['bucket'], lr['key'], lr['VersionId'], leg.get('period'), len(leg.get('by_model', []))))
    n_after = n_before = 0
    for code in CODES:
        prow = [r for r in plat['by_model'] if s_primary.get(r.get('model_name')) == code]
        lrow = [r for r in leg['by_model'] if alias.get(r.get('model_name')) == code and r.get('aum')]
        a_aum = A['current_holdings'][code].get('aum')
        b_aum = B['current_holdings'][code].get('aum')
        p_val = prow[0]['aum'] if len(prow) == 1 else None
        l_val = lrow[-1]['aum'] if lrow else None
        a_eq = len(prow) == 1 and a_aum == p_val
        b_eq = l_val is not None and b_aum == l_val
        n_after += a_eq
        n_before += b_eq
        print('BOOK %-3s AFTER aum %s | platinum row %r aum %s (VersionId %s) %s || BEFORE aum %s | legacy row %r aum %s (VersionId %s) %s'
              % (code, a_aum, prow[0]['model_name'] if prow else None, p_val, pr['VersionId'], 'EQUAL' if a_eq else 'NOT EQUAL',
                 b_aum, lrow[-1]['model_name'] if lrow else None, l_val, lr['VersionId'], 'EQUAL' if b_eq else 'NOT EQUAL'))
    print('AFTER books EQUAL to their platinum row: %d of %d' % (n_after, len(CODES)))
    print('BEFORE books EQUAL to their legacy row: %d of %d' % (n_before, len(CODES)))
    return 0 if (n_after == len(CODES) and n_before == len(CODES)) else 1


def mode_aggregate_payload(fresh):
    ev, _, (ad, _, aw) = normal_pair(fresh)
    _, s_primary, s_blends = standard_maps()
    c, P = captured(ad, aw, AGG_KEY)
    if c is None:
        print('CAPTURE %s: MISSING' % AGG_KEY)
        return 1
    pr, plat = aum_read(ad, aw, PLATINUM_KEY)
    p = c['params']
    print('CAPTURED PUT s3://%s/%s  %d bytes  ContentType=%s ContentEncoding=%s CacheControl=%s'
          % (p.get('Bucket'), p.get('Key'), c['body_bytes'], p.get('ContentType'), p.get('ContentEncoding'), p.get('CacheControl')))
    print('DECOMPRESSED PAYLOAD (holdings elided to count + first):')
    shown = json.loads(json.dumps(P))
    hs = shown['current_holdings']['AGG']['holdings']
    shown['current_holdings']['AGG']['holdings'] = ['<%d holdings; first: %s>' % (len(hs), canon(hs[0]) if hs else None)]
    print(json.dumps(shown, indent=1))
    checks = []

    def check(name, cond, detail=''):
        checks.append(bool(cond))
        print('CHECK %-58s %s%s' % (name, 'PASS' if cond else 'FAIL', ('  ' + detail) if detail else ''))
    check('put ContentType application/json', p.get('ContentType') == 'application/json', str(p.get('ContentType')))
    check('put ContentEncoding gzip', p.get('ContentEncoding') == 'gzip', str(p.get('ContentEncoding')))
    check('put CacheControl no-cache', p.get('CacheControl') == 'no-cache', str(p.get('CacheControl')))
    check('put body is gzip bytes', (ad / 'captures' / c['body_file']).read_bytes()[:2] == b'\x1f\x8b')
    check('top-level keys == contract 1.1 (10, in order)', list(P.keys()) == CONTRACT_TOP, ','.join(P.keys()))
    agg = (P.get('current_holdings') or {}).get('AGG') or {}
    check('current_holdings keys == [AGG]', list((P.get('current_holdings') or {}).keys()) == ['AGG'])
    check('current_holdings.AGG keys == holdings,total_aum', list(agg.keys()) == ['holdings', 'total_aum'])
    check('weights keys == UST ST INT LT ULT', list((P.get('weights') or {}).keys()) == CODES)
    check('weights_source keys == key,version_id,period', list((P.get('weights_source') or {}).keys()) == ['key', 'version_id', 'period'])
    m = P.get('members') or {}
    check('members keys == UST ST INT LT ULT blends', list(m.keys()) == CODES + ['blends'])
    check('members.blends entries carry model_name,aum,constituents',
          all(list(b.keys()) == ['model_name', 'aum', 'constituents'] for b in m.get('blends', [])))
    check('left_out entries carry model_name,aum', all(list(r.keys()) == ['model_name', 'aum'] for r in (P.get('left_out') or [])))
    r = P.get('reconciliation') or {}
    check('reconciliation keys == contract', list(r.keys()) == RECON_KEYS, ','.join(r.keys()))
    check('generated_at is ISO Z', isinstance(P.get('generated_at'), str) and P['generated_at'].endswith('Z') and 'T' in P['generated_at'], str(P.get('generated_at')))
    check('data_as_of == event data_as_of_date', P.get('data_as_of') == json.loads(ev['event_raw']).get('data_as_of_date'), str(P.get('data_as_of')))
    check('status OK', P.get('status') == 'OK', str(P.get('status')))
    check('reason null on OK', P.get('reason') is None)
    check('holdings non-empty', len(agg.get('holdings') or []) > 0, '%d holdings' % len(agg.get('holdings') or []))
    w = P.get('weights') or {}
    wsum = sum(w.values())
    check('weights sum to 1 within 1e-9', abs(wsum - 1.0) <= 1e-9, 'sum=%r |1-sum|=%.3e' % (wsum, abs(wsum - 1.0)))
    ms = r.get('members_sum')
    maxd = max(abs(w[k] - m[k] / ms) for k in CODES)
    for k in CODES:
        print('    weight %-3s %.15f  members[%s]/members_sum %.15f  |diff| %.3e' % (k, w[k], k, m[k] / ms, abs(w[k] - m[k] / ms)))
    check('each weight == members[code]/members_sum (max |diff| <= 1e-12)', maxd <= 1e-12, 'max |diff| %.3e over 5 of 5' % maxd)
    check('AGG.total_aum == reconciliation.members_sum', agg.get('total_aum') == ms, '%r vs %r' % (agg.get('total_aum'), ms))
    gap_re = r['file_total_model_aum'] - ms
    check('gap == file_total_model_aum - members_sum', abs(r.get('gap') - gap_re) <= 1e-6, 'gap %r recomputed %r' % (r.get('gap'), gap_re))
    check('file_total_model_aum == the read file total.model_aum', r.get('file_total_model_aum') == plat['total']['model_aum'], str(plat['total']['model_aum']))
    rows = plat.get('by_model', [])
    sum_rows = sum(x['aum'] for x in rows if x.get('model_name') in s_primary or x.get('model_name') in s_blends)
    check('members_sum == sum of primary + blend rows (within 1e-6)', abs(ms - sum_rows) <= 1e-6, 'members_sum %r rows %r' % (ms, sum_rows))
    five = sum(x['aum'] for x in rows if x.get('model_name') in s_primary)
    check('five_primary_sum == sum of the five primary rows', abs(r.get('five_primary_sum') - five) <= 1e-6, '%r vs %r' % (r.get('five_primary_sum'), five))
    check('members.blends has 2 entries', len(m.get('blends', [])) == 2, '%d' % len(m.get('blends', [])))
    for b in m.get('blends', []):
        print('    blend %r aum %r constituents %s' % (b['model_name'], b['aum'], json.dumps(b['constituents'])))
    for k in CODES:
        own = [x['aum'] for x in rows if s_primary.get(x.get('model_name')) == k][0]
        add = sum(x['aum'] * s_blends[x['model_name']].get(k, 0) for x in rows if x.get('model_name') in s_blends)
        print('    members[%-3s] %r = own row %r + blend shares %r (|diff| %.3e)' % (k, m[k], own, add, abs(m[k] - own - add)))
    exp_left = [{'model_name': x.get('model_name'), 'aum': x.get('aum')} for x in rows
                if x.get('model_name') not in s_primary and x.get('model_name') not in s_blends]
    check('left_out == every other row of the read file', P.get('left_out') == exp_left,
          '%d left out of %d rows (expected %d)' % (len(P.get('left_out') or []), len(rows), len(exp_left)))
    check('weights_source.key == platinum key', (P.get('weights_source') or {}).get('key') == PLATINUM_KEY)
    check('weights_source.version_id == VersionId the run read', (P.get('weights_source') or {}).get('version_id') == pr['VersionId'],
          'payload %s read %s' % ((P.get('weights_source') or {}).get('version_id'), pr['VersionId']))
    check('weights_source.period == the read file period', (P.get('weights_source') or {}).get('period') == plat.get('period'), str(plat.get('period')))
    check('gap_explanation_ref names the gap note', r.get('gap_explanation_ref') ==
          'org/missions/D4/POSN/POSN_AGGFIX/deliverables/0.9.0_WK_POSN_AGGFIX~1/AF1_S1_GAP_EXPLANATION.md')
    print('CHECKS PASS %d of %d' % (sum(checks), len(checks)))
    return 0 if all(checks) else 1


def mode_hand_rederive(fresh):
    ev, _, (ad, _, aw) = normal_pair(fresh)
    _, P = captured(ad, aw, AGG_KEY)
    _, S = captured(ad, aw, SHARED_KEY)
    holdings = P['current_holdings']['AGG']['holdings']
    m = P['members']
    ms = P['reconciliation']['members_sum']
    print('READ AFTER captures: %s (AGG, %d holdings) and %s (five books)' % (AGG_KEY, len(holdings), SHARED_KEY))
    print('member weights: %s' % ', '.join('%s %r/%r=%.10f' % (k, m[k], ms, m[k] / ms) for k in CODES))
    top = sorted(holdings, key=lambda h: (-h['weight'], h['ticker']))[:3]
    n = 0
    for h in top:
        t = h['ticker']
        hand = 0.0
        parts = []
        for k in CODES:
            bw = [x['weight'] for x in S['current_holdings'][k]['holdings'] if x['ticker'] == t]
            if bw:
                hand += bw[0] * (m[k] / ms)
                parts.append('%s %.4f x %.10f' % (k, bw[0], m[k] / ms))
        hand4 = round(hand, 4)
        match = '%.6f' % hand4 == '%.6f' % h['weight']
        n += match
        print('HOLDING %-6s hand = sum(%s)' % (t, ' + '.join(parts)))
        print('        hand unrounded %.10f | hand at the producer\'s 4-dp rounding %.6f | producer weight %.6f | %s at 6 decimals'
              % (hand, hand4, h['weight'], 'MATCH' if match else 'NO MATCH'))
    print('HAND RE-DERIVATION MATCH %d of %d' % (n, len(top)))
    agg_set = {h['ticker'] for h in holdings}
    union = set()
    for k in CODES:
        union |= {x['ticker'] for x in S['current_holdings'][k]['holdings']}
    eq = agg_set == union
    print('TICKER SET AGG %d, union of five books %d: %s%s' % (len(agg_set), len(union), 'EQUAL' if eq else 'NOT EQUAL',
          '' if eq else ' (AGG only %s; books only %s)' % (sorted(agg_set - union), sorted(union - agg_set))))
    return 0 if (n == len(top) and eq) else 1


def fault_pair(tag, kind, ev):
    b = run('%s-before' % tag, 'BEFORE', 'handler', ev, fault={'kind': kind, 'key': LEGACY_KEY})
    a = run('%s-after' % tag, 'AFTER', 'handler', ev, fault={'kind': kind, 'key': PLATINUM_KEY})
    return b, a


def mode_fail_weights():
    ev = recorded_event()
    print_event(ev)
    (bd, _, bw), (ad, _, aw) = fault_pair('fail', 'fail', ev)
    ok = True
    for label, d, w in (('BEFORE', bd, bw), ('AFTER', ad, aw)):
        print('%s injected faults: %s' % (label, json.dumps(w['faults'])))
        warn = [ln for ln in (d / 'stdout.txt').read_text(encoding='utf-8', errors='replace').splitlines() if 'Failed to load AUM' in ln]
        print('%s producer log: %s' % (label, warn))
        print_captures(label, w)
        _, S = captured(d, w, SHARED_KEY)
        print('%s shared file top-level keys: %s' % (label, ', '.join(S.keys())))
        has_ch = 'current_holdings' in S
        print('%s shared file current_holdings key present: %s; data_date present: %s; AGG present: %s'
              % (label, has_ch, 'data_date' in S, bool(has_ch and 'AGG' in S['current_holdings'])))
        ok = ok and not has_ch and len(w['faults']) == 1
    c, P = captured(ad, aw, AGG_KEY)
    cb, _ = captured(bd, bw, AGG_KEY)
    print('BEFORE %s captured: %s' % (AGG_KEY, 'YES' if cb else 'NO (the BEFORE producer has no such key)'))
    if c is None:
        print('AFTER %s captured: NO' % AGG_KEY)
        return 1
    print('AFTER %s captured: YES, ContentType=%s ContentEncoding=%s CacheControl=%s' % (AGG_KEY, c['params'].get('ContentType'), c['params'].get('ContentEncoding'), c['params'].get('CacheControl')))
    print(json.dumps(P, indent=1))
    agg_ok = P['status'] == 'UNAVAILABLE' and P['current_holdings']['AGG']['holdings'] == [] and P['reason']
    print('AFTER aggregate status %s, holdings %s, reason non-null %s -> %s'
          % (P['status'], P['current_holdings']['AGG']['holdings'], bool(P['reason']), 'AS EXPECTED' if agg_ok else 'NOT AS EXPECTED'))
    return 0 if (ok and agg_ok) else 1


def mode_partial_weights():
    ev = recorded_event()
    print_event(ev)
    (bd, _, bw), (ad, _, aw) = fault_pair('partial', 'drop_ult', ev)
    _, s_primary, _ = standard_maps()
    alias = before_alias_map()
    ok = True
    for label, d, w, key, names in (('BEFORE', bd, bw, LEGACY_KEY, alias), ('AFTER', ad, aw, PLATINUM_KEY, s_primary)):
        f = w['faults'][0]
        print('%s served %s with the ULT row removed: rows %d -> %d, removed %s'
              % (label, key, f['rows_before'], f['rows_served'], json.dumps(f['removed_rows'])))
        r, served = aum_read(d, w, key, served=True)
        _, S = captured(d, w, SHARED_KEY)
        print('%s shared file current_holdings keys: %s' % (label, ' '.join(S.get('current_holdings', {}).keys())))
        for code in CODES:
            got = S['current_holdings'][code]['aum']
            rows = [x['aum'] for x in served['by_model'] if names.get(x.get('model_name')) == code and x.get('aum')]
            exp = rows[-1] if rows else 0
            good = got == exp
            ok = ok and good and (code != 'ULT' or got == 0)
            print('    %s BOOK %-3s aum %s  expected %s (%s)  %s' % (label, code, got, exp,
                  'row in the served file, VersionId %s' % r['VersionId'] if rows else 'no row -> .get(code, 0)', 'OK' if good else 'NOT OK'))
    c, P = captured(ad, aw, AGG_KEY)
    cb, _ = captured(bd, bw, AGG_KEY)
    print('BEFORE %s captured: %s' % (AGG_KEY, 'YES' if cb else 'NO (the BEFORE producer has no such key)'))
    _, B = captured(bd, bw, SHARED_KEY)
    if 'AGG' in B.get('current_holdings', {}):
        agg = B['current_holdings']['AGG']
        print('BEFORE shared file AGG: %d holdings, total_aum %s (served over the four rows present)' % (len(agg['holdings']), agg['total_aum']))
    if c is None:
        print('AFTER %s captured: NO' % AGG_KEY)
        return 1
    shown = json.loads(json.dumps(P))
    print('AFTER %s captured: YES' % AGG_KEY)
    print(json.dumps(shown, indent=1))
    agg_ok = P['status'] == 'UNAVAILABLE' and P['current_holdings']['AGG']['holdings'] == [] and 'ULT' in (P['reason'] or '')
    print('AFTER aggregate status %s, reason %r names ULT: %s -> %s'
          % (P['status'], P['reason'], 'ULT' in (P['reason'] or ''), 'AS EXPECTED' if agg_ok else 'NOT AS EXPECTED'))
    return 0 if (ok and agg_ok) else 1


def compare_payloads(label, x, y):
    x = dict(x)
    y = dict(y)
    gx = x.pop('generated_at', None)
    gy = y.pop('generated_at', None)
    d = diff_paths(x, y)
    print('%s: generated_at %s vs %s (excluded); %s' % (label, gx, gy, 'EQUAL in every other field' if not d else 'DIFFERS'))
    if d:
        print_diff_summary('    diff', d)
    return not d


AGG_EQUAL_FIELDS = ['status', 'weights', 'weights_source', 'members', 'left_out', 'reconciliation']


def path_of(p):
    return p.split(' (')[0]


def amendment1_excluded(p):
    """A2-AC13 AMENDMENT 1: current_holdings AGG and the five book aum values are outside the compared set."""
    q = path_of(p)
    if q == '$.current_holdings.AGG' or q.startswith('$.current_holdings.AGG.') or q.startswith('$.current_holdings.AGG['):
        return True
    return q in ['$.current_holdings.%s.aum' % c for c in CODES]


def cli_vs_handler_path_set(label, cli, handler):
    """The shared file's CLI-versus-handler difference, as a path set with the AMENDMENT 1 exclusion applied."""
    x = dict(cli)
    y = dict(handler)
    gx = x.pop('generated_at', None)
    gy = y.pop('generated_at', None)
    d = diff_paths(x, y)
    kept = [p for p in d if not amendment1_excluded(p)]
    excl = [p for p in d if amendment1_excluded(p)]
    kept_set = sorted({path_of(p) for p in kept})
    print('%s: generated_at %s vs %s (excluded); %d differing leaf path(s): %d excluded by AMENDMENT 1 '
          '(current_holdings AGG, the five book aum), %d compared (%d distinct paths)'
          % (label, gx, gy, len(d), len(excl), len(kept), len(kept_set)))
    print_diff_summary('    compared', kept, limit=50)
    if excl:
        print_diff_summary('    excluded', excl, limit=50)
    for p in kept_set:
        print('    path %s' % p)
    return kept_set


def agg_fields_equal(label, X, H, show=True):
    """opal_aggregate.json CLI vs handler over the AMENDMENT 1 fields; the verdict is value equality."""
    rows = []
    for f in AGG_EQUAL_FIELDS:
        present = f in X and f in H
        rows.append((f, present and X[f] == H[f], present and canon(X[f]) == canon(H[f]),
                     canon(X.get(f))[:110], canon(H.get(f))[:110]))
    xa = (X.get('current_holdings') or {}).get('AGG') or {}
    ha = (H.get('current_holdings') or {}).get('AGG') or {}
    present = 'total_aum' in xa and 'total_aum' in ha
    rows.append(('current_holdings.AGG.total_aum', present and xa['total_aum'] == ha['total_aum'],
                 present and canon(xa['total_aum']) == canon(ha['total_aum']), canon(xa.get('total_aum')), canon(ha.get('total_aum'))))
    tx = [(h.get('ticker'), h.get('weight')) for h in xa.get('holdings') or []]
    th = [(h.get('ticker'), h.get('weight')) for h in ha.get('holdings') or []]
    multiset_eq = len(tx) > 0 and len(tx) == len(th) and sorted(tx, key=canon) == sorted(th, key=canon)
    rows.append(('current_holdings.AGG.holdings[*] (ticker, weight)', multiset_eq, tx == th,
                 '%d holdings, first %s' % (len(tx), canon(tx[:3])), '%d holdings, first %s' % (len(th), canon(th[:3]))))
    ok = all(r[1] for r in rows)
    if show:
        for f, eq, beq, xs, hs in rows:
            print('    %s FIELD %-50s %s (serialized bytes %s)  cli=%s  handler=%s'
                  % (label, f, 'EQUAL' if eq else 'NOT EQUAL', 'equal' if beq else 'differ', xs, hs))
    print('%s: %d of %d fields EQUAL -> %s' % (label, sum(1 for r in rows if r[1]), len(rows), 'ALL EQUAL' if ok else 'NOT ALL EQUAL'))
    return ok


def mode_cli_upload(fresh):
    import copy
    ev = recorded_event()
    print_event(ev)
    e = json.loads(ev['event_raw'])
    head = subprocess.run(['git', 'rev-parse', '--short=10', 'HEAD'], cwd=str(WS), capture_output=True, text=True).stdout.strip()
    head_bytes = subprocess.run(['git', 'show', 'HEAD:' + PRODUCER_REL], cwd=str(WS), capture_output=True).stdout
    work_bytes = (WS / PRODUCER_REL).read_bytes()
    at_head = len(head_bytes) > 0 and head_bytes == work_bytes
    print('AFTER SOURCE = HEAD %s: working %s sha256 %s, git show HEAD sha256 %s (%d bytes) -> %s'
          % (head, PRODUCER_REL, sha256_bytes(work_bytes)[:16], sha256_bytes(head_bytes)[:16], len(head_bytes), at_head))
    (ad, _, aw) = run('normal-after', 'AFTER', 'handler', ev, fresh=False)
    (cd, ccfg, cw) = run('cli-after', 'AFTER', 'cli', ev, fresh=fresh)
    print('CLI argv: %s (AWS_LAMBDA_FUNCTION_NAME=%s set by the harness, as for the handler runs)' % (' '.join(ccfg['cli_argv']), FUNCTION_NAME))
    pkl_reads = [r for r in cw['reads_s3'] if r['key'].startswith('benchmarks/model_')]
    hreads = [r for r in aw['reads_s3'] if r['key'] == e['processed']['model_pkl_key']]
    print('MODEL PKL: event %s (handler VersionId %s); CLI read %s'
          % (e['processed']['model_pkl_key'], hreads[0]['VersionId'] if hreads else None,
             ', '.join('%s VersionId %s' % (r['key'], r['VersionId']) for r in pkl_reads)))
    same_pkl = len(pkl_reads) == 1 and bool(hreads) and pkl_reads[0]['key'] == hreads[0]['key'] and pkl_reads[0]['VersionId'] == hreads[0]['VersionId']
    print('MODEL PKL SAME AS THE HANDLER RUN: %s' % same_pkl)
    print('CLI main() return: %s' % cw.get('main_return'))
    print_captures('CLI AFTER', cw)
    keys = [c['params'].get('Key') for c in cw['captures']]
    two = sorted(keys) == sorted([SHARED_KEY, AGG_KEY]) and len(keys) == 2
    print('EXACTLY TWO PUTS %s AND %s: %s' % (SHARED_KEY, AGG_KEY, two))
    ok = at_head and same_pkl and two and cw.get('main_return') == 0
    payloads = {}
    for key in (SHARED_KEY, AGG_KEY):
        c, X = captured(cd, cw, key)
        _, H = captured(ad, aw, key)
        if c is None or H is None:
            print('CAPTURE MISSING %s: cli %s handler %s' % (key, c is not None, H is not None))
            ok = False
            continue
        p = c['params']
        shape_ok = (p.get('ContentType'), p.get('ContentEncoding'), p.get('CacheControl')) == ('application/json', 'gzip', 'no-cache')
        print('PUT SHAPE %s: ContentType=%s ContentEncoding=%s CacheControl=%s -> %s'
              % (key, p.get('ContentType'), p.get('ContentEncoding'), p.get('CacheControl'), 'OK' if shape_ok else 'NOT OK'))
        ok = ok and shape_ok
        payloads[key] = (X, H)
    # The shared file: the CLI-versus-handler difference path set at the BEFORE anchor and at HEAD.
    (bd, _, bw) = run('normal-before', 'BEFORE', 'handler', ev, fresh=False)
    (cbd, _, cbw) = run('cli-before', 'BEFORE', 'cli', ev, fresh=fresh)
    print_captures('CLI BEFORE', cbw)
    _, XB = captured(cbd, cbw, SHARED_KEY)
    _, HB = captured(bd, bw, SHARED_KEY)
    same_set = False
    if XB is None or HB is None or SHARED_KEY not in payloads:
        print('SHARED FILE CAPTURE MISSING: cli-before %s normal-before %s head pair %s' % (XB is not None, HB is not None, SHARED_KEY in payloads))
        ok = False
    else:
        kb = cli_vs_handler_path_set('SHARED %s CLI vs handler at BEFORE %s' % (SHARED_KEY, BEFORE_COMMIT), XB, HB)
        kh = cli_vs_handler_path_set('SHARED %s CLI vs handler at HEAD %s' % (SHARED_KEY, head), *payloads[SHARED_KEY])
        only_head = sorted(set(kh) - set(kb))
        only_base = sorted(set(kb) - set(kh))
        for q in only_head:
            print('    only at HEAD: %s' % q)
        for q in only_base:
            print('    only at %s: %s' % (BEFORE_COMMIT, q))
        same_set = len(kh) > 0 and not only_head and not only_base
        print('PATH SET at %s: %d; at HEAD: %d; only at HEAD (NEW): %d; only at %s: %d'
              % (BEFORE_COMMIT, len(kb), len(kh), len(only_head), BEFORE_COMMIT, len(only_base)))
        print('SHARED FILE CLI-vs-HANDLER DIFFERENCE PATH SET SAME AT %s AND AT HEAD (apart from current_holdings AGG and the five book aum): %s'
              % (BEFORE_COMMIT, same_set))
        injected = set(kh) | {'$.control.injected_path'}
        print('CONTROL one path injected into the HEAD set in memory: same=%s -> %s'
              % (injected == set(kb), 'REPORTED AS A DIFFERENCE (FIRED)' if injected != set(kb) else 'NOT REPORTED (DID NOT FIRE)'))
    ok = ok and same_set
    agg_ok = False
    if AGG_KEY in payloads:
        X, H = payloads[AGG_KEY]
        print('AGGREGATE %s CLI vs handler at HEAD %s: generated_at %s vs %s (not compared)' % (AGG_KEY, head, X.get('generated_at'), H.get('generated_at')))
        agg_ok = agg_fields_equal('AGG', X, H)
        XM = copy.deepcopy(X)
        if XM.get('current_holdings', {}).get('AGG', {}).get('holdings'):
            XM['current_holdings']['AGG']['holdings'][0]['weight'] = XM['current_holdings']['AGG']['holdings'][0]['weight'] + 0.0001
            fired = not agg_fields_equal('CONTROL (first AGG holding weight +0.0001 in the CLI copy, in memory)', XM, H, show=False)
            print('CONTROL aggregate field check -> %s' % ('REPORTED AS A DIFFERENCE (FIRED)' if fired else 'NOT REPORTED (DID NOT FIRE)'))
    ok = ok and agg_ok
    print('VERDICT A2-AC13 %s' % ('ALL CHECKS HOLD' if ok else 'A CHECK FAILED'))
    return 0 if ok else 1


def main():
    if len(sys.argv) == 3 and sys.argv[1] == '--_run':
        return _runner(sys.argv[2])
    ap = argparse.ArgumentParser(description=__doc__.split('\n')[0])
    g = ap.add_mutually_exclusive_group(required=True)
    for flag in ('--membership-equals-standard', '--compare', '--book-aum', '--aggregate-payload', '--hand-rederive',
                 '--fail-weights', '--partial-weights', '--cli-upload'):
        g.add_argument(flag, action='store_true')
    ap.add_argument('--fresh', action='store_true', help='re-run the cached normal runs and print a determinism comparison')
    a = ap.parse_args()
    print('HARNESS %s at workspace %s (HEAD %s); BEFORE anchor %s; captures under %s; nothing is served'
          % (Path(__file__).name, WS.as_posix(),
             subprocess.run(['git', 'rev-parse', '--short=10', 'HEAD'], cwd=str(WS), capture_output=True, text=True).stdout.strip(),
             BEFORE_COMMIT, RUNS.relative_to(WS).as_posix()))
    if a.membership_equals_standard:
        return mode_membership()
    if a.compare:
        return mode_compare(a.fresh)
    if a.book_aum:
        return mode_book_aum(a.fresh)
    if a.aggregate_payload:
        return mode_aggregate_payload(a.fresh)
    if a.hand_rederive:
        return mode_hand_rederive(a.fresh)
    if a.fail_weights:
        return mode_fail_weights()
    if a.partial_weights:
        return mode_partial_weights()
    return mode_cli_upload(a.fresh)


if __name__ == '__main__':
    sys.exit(main())
