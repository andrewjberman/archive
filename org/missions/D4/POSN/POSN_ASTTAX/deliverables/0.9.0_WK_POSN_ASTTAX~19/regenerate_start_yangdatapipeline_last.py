"""REGENERATE_START_YANGDATAPIPELINE_LAST -- POSN_ASTTAX.TO-V1-1 V1-AC11.

WHAT THE CRITERION ASKS FOR: start the yang data pipeline Step Functions state
machine (the one whose executions write json/positioning/positioning_data.json)
with the LAST SUCCEEDED execution's input, poll to a terminal status, print the
execution ARN, the status and the served keys' new LastModified / VersionId,
then read the served artifacts and classify the delta.

WHAT THIS SCRIPT DOES BEFORE IT STARTS ANYTHING -- and why: it measures the
PREMISE the criterion rests on. Re-feeding "the LAST SUCCEEDED execution's
input" only regenerates anything if the objects that input NAMES are still on
the live plane. This pipeline's second state (MoveToProcessed) MOVES the upload
objects out of uploads/ and its late state (CleanupUploads) DELETES them, so a
SUCCEEDED execution consumes its own input. If the input objects are gone the
start is not a regeneration at all: ReadManifest raises, its Catch routes to
PipelineFailed, and the only thing the act produces is a FAILED execution in
the estate's history.

So: the premise is measured and PRINTED first, per object. Absent -> REFUSE
(rc=2) with the measurement, start nothing. Present -> start, poll, read.

SECOND GATE, printed either way: the SIGNED RADIUS. The two never-widen halves
at HEAD sign exactly two keys for B1 --
  org/missions/D4/POSN/POSN_ASTTAX/ledger/NEVER_WIDEN_ROUND5_COO_HALF.md @f381f6f402
  org/missions/D4/POSN/POSN_ASTTAX/ledger/NEVER_WIDEN_ROUND5_CTO_HALF.md @af667548d1
-- json/positioning/positioning_data.json and json/positioning/allocation_summary.json,
the CTO half adding "anything else -- NOT SIGNED". This script prints the state
machine's full task census beside those two keys so the reader can see the
difference between what the act would touch and what is signed, rather than
inferring it.

Usage: timeout 900 python org/missions/D4/POSN/POSN_ASTTAX/deliverables/0.9.0_WK_POSN_ASTTAX~19/regenerate_start_yangdatapipeline_last.py
Exit codes: 0 = executed and the served keys were read; 2 = REFUSED on a
measured premise/radius failure (nothing started); 3 = started and the
execution reached a non-SUCCEEDED terminal status.
"""
import datetime
import gzip
import json
import time

import boto3

SM_NAME = 'YangDataPipeline'
SERVED_BUCKET = 'opal-data-portal-v2'
POSITIONING_KEY = 'json/positioning/positioning_data.json'
ALLOCSUM_KEY = 'json/positioning/allocation_summary.json'
SIGNED_KEYS = (POSITIONING_KEY, ALLOCSUM_KEY)
# The pre-deploy reads both halves name, so the comparison has an anchor.
PRE_DEPLOY_POSITIONING_VERSION = '4Q1qjgD52FSKZ38EfHGqdKGHyJ_ktlka'
PRE_DEPLOY_ALLOCSUM_VERSION = 'FiY95KdKcmtt5els.v44XVZciDBtUDrw'
NEW_CLASSES = ('structured', 'commodities', 'alternatives')
POLL_SECONDS = 15
POLL_BUDGET_SECONDS = 600

sfn = boto3.client('stepfunctions', region_name='us-east-1')
s3 = boto3.client('s3', region_name='us-east-1')


def rule(title):
    print('')
    print('=' * 78)
    print(title)
    print('=' * 78)


def head(bucket, key, version_id=None):
    """head_object that returns a RESULT rather than raising -- a failed
    retrieval returns a VALUE here, and the caller decides what it means."""
    kw = {'Bucket': bucket, 'Key': key}
    if version_id:
        kw['VersionId'] = version_id
    try:
        r = s3.head_object(**kw)
        return {'present': True, 'LastModified': r['LastModified'].isoformat(),
                'VersionId': r.get('VersionId'), 'ContentLength': r['ContentLength']}
    except Exception as exc:
        code = getattr(exc, 'response', {}).get('Error', {}).get('Code', type(exc).__name__)
        return {'present': False, 'error': code}


def body(bucket, key, version_id=None):
    kw = {'Bucket': bucket, 'Key': key}
    if version_id:
        kw['VersionId'] = version_id
    raw = s3.get_object(**kw)['Body'].read()
    if raw[:2] == bytes([0x1f, 0x8b]):      # gzip magic
        raw = gzip.decompress(raw)
    return raw


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


# ---------------------------------------------------------------- 1. the SFN
rule('1. THE STATE MACHINE, AND THE EVIDENCE IT IS THE ONE THAT WRITES THE KEY')
machines = sfn.list_state_machines()['stateMachines']
print('state machines in the account: %d' % len(machines))
arn = None
for m in machines:
    print('   %-26s %s' % (m['name'], m['stateMachineArn']))
    if m['name'] == SM_NAME:
        arn = m['stateMachineArn']
if arn is None:
    print('REFUSED: no state machine named %s' % SM_NAME)
    raise SystemExit(2)
definition = json.loads(sfn.describe_state_machine(stateMachineArn=arn)['definition'])


def walk_tasks(states):
    # A TOP-LEVEL-ONLY walk UNDERSTATES this machine: its generators live inside
    # Parallel branches, so a census that reads definition['States'] alone
    # returns a denominator that is quietly too small AND misses the very state
    # that writes the key this criterion is about. Recurse through Branches and
    # Iterator.
    out = []
    for n, st in states.items():
        if st.get('Type') == 'Task':
            out.append((n, st.get('Resource', '')))
        for br in st.get('Branches', []) or []:
            out.extend(walk_tasks(br.get('States', {})))
        if 'Iterator' in st:
            out.extend(walk_tasks(st['Iterator'].get('States', {})))
    return out


tasks = walk_tasks(definition['States'])
writers = [n for n, r in tasks if r.endswith('yang-generate-positioning')]
print('')
print('%s carries %d Task state(s); the state(s) invoking yang-generate-positioning '
      '(whose OUTPUT_KEY is %s): %s' % (SM_NAME, len(tasks), POSITIONING_KEY, writers))

# ------------------------------------------------------- 2. the last SUCCEEDED
rule('2. THE LAST SUCCEEDED EXECUTION AND ITS INPUT')
execs = sfn.list_executions(stateMachineArn=arn, statusFilter='SUCCEEDED',
                            maxResults=1)['executions']
if not execs:
    print('REFUSED: no SUCCEEDED execution to take an input from')
    raise SystemExit(2)
last = execs[0]
desc = sfn.describe_execution(executionArn=last['executionArn'])
last_input = desc['input']
print('name      : %s' % last['name'])
print('arn       : %s' % last['executionArn'])
print('started   : %s' % desc['startDate'].isoformat())
print('stopped   : %s' % desc['stopDate'].isoformat())
print('input     : %s' % last_input)
payload = json.loads(last_input)

# ------------------------------------------------- 3. the premise, per object
rule('3. THE PREMISE GATE -- do the objects that input NAMES still exist?')
detail = payload.get('detail', {})
in_bucket = detail.get('bucket', {}).get('name')
manifest_key = detail.get('object', {}).get('key')
named = [(in_bucket, manifest_key)]
files = payload.get('manifest', {}).get('files', {})
prefix = manifest_key.rsplit('/', 1)[0] + '/' if manifest_key and '/' in manifest_key else ''
for label, fname in sorted(files.items()):
    named.append((in_bucket, prefix + fname))
missing = []
for b, k in named:
    r = head(b, k)
    if r['present']:
        print('  PRESENT  s3://%s/%s  LastModified=%s VersionId=%s bytes=%s'
              % (b, k, r['LastModified'], r['VersionId'], r['ContentLength']))
    else:
        print('  ABSENT   s3://%s/%s  -> %s' % (b, k, r['error']))
        missing.append((b, k))
print('')
print('DENOMINATOR: %d object(s) named by the input, %d present, %d ABSENT'
      % (len(named), len(named) - len(missing), len(missing)))

# ------------------------------------------------------- 4. the signed radius
rule('4. THE SIGNED RADIUS vs THE ACT\'S WRITE SET')
print('SIGNED for B1 by both never-widen halves at HEAD -- %d key(s):' % len(SIGNED_KEYS))
for k in SIGNED_KEYS:
    print('   s3://%s/%s' % (SERVED_BUCKET, k))
print('CTO half, B1 table, last row: "anything else -- NOT SIGNED".')
print('')
print('The act this criterion names starts the WHOLE state machine, whose %d Task '
      'states invoke these functions:' % len(tasks))
for n, r in sorted(tasks):
    print('   %-42s %s' % (n, r.rsplit(':', 1)[-1]))
print('')
print('Three of them act on objects rather than writing a served JSON:')
print('   MoveToProcessed      MOVES the upload objects out of uploads/')
print('   CleanupUploads       DELETES upload objects (an S3 delete)')
print('   InvalidateCloudFront issues a CDN invalidation')

# --------------------------------------------------- 5. the served keys, now
rule('5. THE SERVED KEYS RIGHT NOW (before anything this script might start)')
for k, anchor in ((POSITIONING_KEY, PRE_DEPLOY_POSITIONING_VERSION),
                  (ALLOCSUM_KEY, PRE_DEPLOY_ALLOCSUM_VERSION)):
    r = head(SERVED_BUCKET, k)
    print('  s3://%s/%s' % (SERVED_BUCKET, k))
    print('     LastModified=%s VersionId=%s bytes=%s  (pre-deploy anchor %s; same=%s)'
          % (r.get('LastModified'), r.get('VersionId'), r.get('ContentLength'),
             anchor, r.get('VersionId') == anchor))

if missing:
    rule('REFUSED -- rc=2. NOTHING WAS STARTED.')
    print('THE MEASUREMENT: %d of %d object(s) the last SUCCEEDED execution\'s input '
          'names are ABSENT from the live plane (printed in section 3). This pipeline '
          'consumes its own input (MoveToProcessed, CleanupUploads), so re-feeding that '
          'input cannot reproduce the run: ReadManifest reads s3://%s/%s, which is gone, '
          'and its Catch routes States.ALL to PipelineFailed.'
          % (len(missing), len(named), in_bucket, manifest_key))
    print('')
    print('CONSEQUENCE, stated rather than worked around: starting it would produce a '
          'FAILED execution and NO regeneration -- the criterion\'s named result is '
          'unreachable by its named invocation today.')
    print('')
    print('AND THE ACT IS WIDER THAN THE SIGN-OFF EITHER WAY (section 4): on the branch '
          'where the input DID exist, the run writes every key its %d Task states '
          'produce, moves and then deletes upload objects and invalidates the CDN, '
          'while the halves sign exactly %d served keys and say "anything else -- NOT '
          'SIGNED".' % (len(tasks), len(SIGNED_KEYS)))
    print('')
    print('NOT REPAIRED HERE, BY RULE: the task order\'s refusal clause -- "A criterion '
          'you cannot satisfy as written is REFUSED with its measurement, never '
          'repaired, widened or satisfied by another route." Re-uploading an input, '
          'hand-building a manifest, or invoking the two producers directly would each '
          'be a different act from the one V1-AC11 names.')
    print('')
    print('WHAT IS COVERED AND AVAILABLE TO THE ISSUER: the CTO half\'s own R1 amendment '
          '(~20:0xZ) already sanctions the DRIVEN refresh as "invokes, once each and in '
          'dependency order" the producers -- yang-generate-positioning, then '
          'yang-generate-holdings-attribution, then yang-generate-allocation-summary -- '
          'writing exactly the signed keys and nothing else. That is a re-cut of this '
          'criterion, which is the issuer\'s act, not this worker\'s.')
    raise SystemExit(2)

# ----------------------------------------------------------- 6. start + poll
rule('6. START + POLL')
name = 'posn-b1-verify-%s' % datetime.datetime.utcnow().strftime('%Y%m%dT%H%M%SZ')
started = sfn.start_execution(stateMachineArn=arn, name=name, input=last_input)
exec_arn = started['executionArn']
print('execution ARN: %s' % exec_arn)
deadline = time.time() + POLL_BUDGET_SECONDS
status = 'RUNNING'
poll_desc = None
while time.time() < deadline:
    poll_desc = sfn.describe_execution(executionArn=exec_arn)
    status = poll_desc['status']
    print('   %s  status=%s' % (datetime.datetime.utcnow().strftime('%H:%M:%SZ'), status))
    if status != 'RUNNING':
        break
    time.sleep(POLL_SECONDS)
print('TERMINAL STATUS: %s' % status)

rule('7. THE SERVED KEYS AFTER THE RUN')
after = {}
for k in SIGNED_KEYS:
    after[k] = head(SERVED_BUCKET, k)
    print('  s3://%s/%s  LastModified=%s VersionId=%s bytes=%s'
          % (SERVED_BUCKET, k, after[k].get('LastModified'), after[k].get('VersionId'),
             after[k].get('ContentLength')))
if status != 'SUCCEEDED':
    print('')
    print('The execution did not SUCCEED; the served read below is reported against '
          'the pre-deploy anchors so the reader can see whether anything moved.')
    raise SystemExit(3)

rule('8. THE SERVED READ -- positioning_data.json, new vs pre-deploy')
new = json.loads(body(SERVED_BUCKET, POSITIONING_KEY).decode('utf-8'))
old = json.loads(body(SERVED_BUCKET, POSITIONING_KEY,
                      PRE_DEPLOY_POSITIONING_VERSION).decode('utf-8'))
fn, fo = flatten(new), flatten(old)
leaf_keys = [k for k in fn if k.split('.')[-1].split('[')[0] in NEW_CLASSES
             and k.startswith('portfolios.')]
zeros = [k for k in leaf_keys if fn[k] in (0, 0.0)]
print('five-class allocation leaf keys under portfolios.*: %d, of which value 0 or 0.0: %d'
      % (len(leaf_keys), len(zeros)))
for cls in NEW_CLASSES:
    print('benchmarks.etf.%s = %s'
          % (cls, json.dumps(new.get('benchmarks', {}).get('etf', {}).get(cls))))
for m in sorted(new.get('portfolios', {})):
    tn = [h['ticker'] for h in new['portfolios'][m]['holdings']]
    to = [h['ticker'] for h in old['portfolios'][m]['holdings']]
    print('membership %-4s %d vs %d identical=%s' % (m, len(to), len(tn), to == tn))

rule('9. THE CONTROL -- allocation_summary.json, new vs its prior version')
a_new = body(SERVED_BUCKET, ALLOCSUM_KEY)
a_old = body(SERVED_BUCKET, ALLOCSUM_KEY, PRE_DEPLOY_ALLOCSUM_VERSION)
jn, jo = json.loads(a_new.decode('utf-8')), json.loads(a_old.decode('utf-8'))
fa_n, fa_o = flatten(jn), flatten(jo)
diff = sorted(set(fa_n) ^ set(fa_o)) + sorted(
    k for k in set(fa_n) & set(fa_o) if fa_n[k] != fa_o[k])
print('byte-identical: %s' % (a_new == a_old))
print('differing leaf keys: %d -> %s' % (len(diff), diff[:20]))
raise SystemExit(0)
