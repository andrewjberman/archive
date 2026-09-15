#!/usr/bin/env python3
"""Builds POSN_AGGFIX.TO-A3-1's proof-of-spec instance from the committed criterion outputs.

Every output_evidence is the recorded stdout file of the criterion's invocation, read at build time (ANSI
colour codes stripped from terraform output, nothing else changed). Author: 0.9.0_WK_POSN_AGGFIX~1.
"""
import json
import re
import subprocess
from pathlib import Path

HERE = Path(__file__).resolve().parent
WS = Path(subprocess.run(['git', 'rev-parse', '--show-toplevel'], cwd=str(HERE), capture_output=True, text=True, check=True).stdout.strip())
REL = 'org/missions/D4/POSN/POSN_AGGFIX/deliverables/0.9.0_WK_POSN_AGGFIX~1/'
TO_REL = 'org/missions/D4/POSN/POSN_AGGFIX/task-orders/POSN_AGGFIX.TO-A3-1.deploy-the-producer-and-read-the-served-result.md'
OUT = HERE / 'POSN_AGGFIX.TO-A3-1.deploy-the-producer-and-read-the-served-result.proof_of_spec.json'
ANSI = re.compile(r'\x1b\[[0-9;]*m')


def git(*a):
    return subprocess.run(['git'] + list(a), cwd=str(WS), capture_output=True, text=True, encoding='utf-8', check=True).stdout.strip()


def rec(name):
    return ANSI.sub('', (HERE / name).read_text(encoding='utf-8'))


def commit_of(path):
    return git('log', '-1', '--format=%H', '--', REL + path)


to_text = (WS / TO_REL).read_text(encoding='utf-8')
crit = {}
for m in re.finditer(r'<criterion id="(A3-AC\d+)"[^>]*?(?:/>|><invocation>(.*?)</invocation><expect>(.*?)</expect></criterion>)', to_text, re.S):
    crit[m.group(1)] = (m.group(2), m.group(3))
if len(crit) != 13:
    raise SystemExit('ERROR: parsed %d of 13 criteria from the order' % len(crit))
tail = {}
for m in re.finditer(r'(?:</criterion>|/>) `(A3-AC\d+)` -- (.*?)\n', to_text):
    tail[m.group(1)] = m.group(2).strip()
H = {k: git('log', '-1', '--format=%H', '--grep', v, '--author', '0.9.0_WK_POSN_AGGFIX~1 <') for k, v in {
    'open': r'^ledger(POSN_AGGFIX.TO-A3-1', 'build': r'^build(POSN_AGGFIX.TO-A3-1', 'deploy': r'^deploy(POSN_AGGFIX.TO-A3-1',
    'recorder': r'^ci: record deploy yang-pipeline @ 84fe842e', 'close': r'^ledger-close(POSN_AGGFIX.TO-A3-1'}.items()}
for k, v in H.items():
    if not v:
        raise SystemExit('ERROR: no commit found for %s' % k)

rows = []


def row(cid, method, evidence, denominator, status='PASS', reason=None, invocation=None):
    inv, exp = crit[cid]
    r = {'criterion_id': cid, 'criterion_verbatim': ('%s EXPECT: %s' % (tail.get(cid, ''), exp)) if exp else tail[cid],
         'method': method, 'invocation': invocation or inv, 'output_evidence': evidence, 'denominator': denominator, 'status': status}
    if reason:
        r['status_reason'] = reason
    rows.append(r)


row('A3-AC1', 'command', rec('a3_ac1.out.txt'), '2 of 2 halves, one blob line each')
row('A3-AC2', 'command', rec('a3_ac2.out.txt') + '\n$ git show --stat %s\n%s' % (H['open'][:10], git('show', '--stat', '--format=%h %s', H['open'])),
    '2 of 2 ledger files (entry + sentinel) created and listed in the next commit; 8 of 8 legs opened')
row('A3-AC3', 'command', rec('a3_ac3.attempt1.out.txt') + '\n' + rec('a3_ac3.attempt2.out.txt') + '\n' + rec('a3_ac3.srcmap_restore.out.txt'),
    '1 of 1 artifact: rollback VersionId printed before the build; 1 build attempt refused on the named W19-S1 arm (probe PARSES CLEAN / declared_blobs ABSENT / rc 1) and repeated once under BAU_MANIFEST_SKIP=1; source map changed leaves 1 of 2418, non-ASCII 0 after restore (firing control CLAUDE.md 427)')
row('A3-AC4', 'command', rec('a3_ac4.out.txt'), '1 of 1 planned address, 0 add 1 change 0 destroy')
row('A3-AC5', 'command', rec('a3_ac5.attempt1.out.txt'), '1 of 1 apply run; 1 changed of 1 planned; 0 HALT_ACK re-runs (the gate listed no inbox, row POSN_AGGFIX-Z-W1-S11)')
row('A3-AC6', 'command', rec('a3_ac6.out.txt'), 'N/A -- boolean: No changes on the 1 targeted module')
row('A3-AC7', 'live_read', rec('a3_ac7.out.txt'), '1 of 1 function: CodeSha256 equal to the 1 uploaded artifact sha256; LastModified 22:09:30Z after the apply started 22:08:49Z')
row('A3-AC8', 'live_read', rec('a3_ac8.out.txt'),
    '1 generator invoke and 1 invalidation invoke on 1 execution (0 RUNNING); 2 heads + 1 platinum head before and after; listing 3 keys before, 4 after; other keys under json/positioning/ unchanged 2 of 2')
row('A3-AC9', 'live_read', rec('a3_ac9.out.txt'),
    'books NON-AUM IDENTICAL 5 of 5; book aum EQUAL 5 of 5; top-level keys compared 5 of 5 identical; weights 5 of 5; served delta 7 of 7 paths permitted; other keys moved 0 of 2; checks 8 of 8; controls 2 of 2 behaved')
row('A3-AC10', 'live_read', rec('a3_ac10.out.txt'), 'out maps 30 of 30 tickers identical; extra maps 30 of 30 identical; conflicts prior 0 new 0, difference 0')
row('A3-AC11', 'command', rec('a3_ac11.out.txt') + '\n' + rec('a3_ac11.srcmap_restore.out.txt') + '\n' + rec('a3_ac11.changelog_by_hand.out.txt')
    + '\n$ git show --stat %s\n%s' % (H['deploy'][:10], git('show', '--stat', '--format=%h %s', H['deploy'])),
    '1 of 28 source-map rows stamped (3 of 2418 leaves changed); 1 follow-up commit restoring pure ASCII (non-ASCII 0, 0 leaf differences of 2418); 1 CHANGELOG entry by hand (entries 46 -> 47)')
row('A3-AC12', 'command', rec('a3_ac12.out.txt'), '8 of 8 legs closed with evidence; 1 of 1 sentinel removed; entry + sentinel removal in 1 commit')
rows.append({'criterion_id': 'A3-AC13', 'criterion_verbatim': tail['A3-AC13'], 'method': 'manual_read_with_citation',
             'invocation': 'JUDGMENT -- no invocation; graded at L9 by 3.0.0_SA_CVO~Z', 'judgment': True,
             'output_evidence': (HERE / 'a3_ac13.readings.txt').read_text(encoding='utf-8'),
             'denominator': 'N/A -- judgment criterion; the readings cite 7 of 7 served delta paths and 2 of 2 conflicts lists',
             'status': 'UNVERIFIABLE-BY-INSTRUMENT',
             'status_reason': 'judgment="true": graded by 3.0.0_SA_CVO~Z at L9; the substitute oracle is that L9 adjudication over the recorded readings (a3_ac9.out.txt, a3_ac10.out.txt). No verdict is offered.'})

outs = ['a3_ac1.out.txt', 'a3_ac2.out.txt', 'a3_ac3.attempt1.out.txt', 'a3_ac3.attempt2.out.txt', 'a3_ac3.srcmap_restore.out.txt', 'a3_ac4.out.txt',
        'a3_ac5.attempt1.out.txt', 'a3_ac6.out.txt', 'a3_ac7.out.txt', 'a3_ac8.out.txt', 'a3_ac9.out.txt', 'a3_ac10.out.txt', 'a3_ac11.out.txt',
        'a3_ac11.srcmap_restore.out.txt', 'a3_ac11.changelog_by_hand.out.txt']
cover = {'a3_ac1': ['A3-AC1'], 'a3_ac2': ['A3-AC2'], 'a3_ac3': ['A3-AC3'], 'a3_ac4': ['A3-AC4'], 'a3_ac5': ['A3-AC5'], 'a3_ac6': ['A3-AC6'],
         'a3_ac7': ['A3-AC7'], 'a3_ac8': ['A3-AC8'], 'a3_ac9': ['A3-AC9'], 'a3_ac10': ['A3-AC10'], 'a3_ac11': ['A3-AC11']}
artifacts = [
    {'path_or_key': 'infra/aws/lambda/v2_portal/yang_pipeline/positioning/yang-generate-positioning/lambda_function.py', 'kind': 'script',
     'commit_or_etag': '166ca71b8558bd71ab72ce92e258951f01fc7634', 'deployed_state': 'DEPLOYED-VERIFIED',
     'deploy_evidence': 'These bytes are the running code of yang-generate-positioning (module.generate_positioning.aws_lambda_function.this): safe-apply 0 added 1 changed 0 destroyed; targeted re-plan No changes; get-function-configuration CodeSha256 riByGXEfWXdFTEavKGG0nFRj/k4JUAjIiVKfm06Tdgk= == artifact sha256, LastModified 2026-09-15T22:09:30Z. Source: lambda_function.py @166ca71b85 (the one commit on the function directory since dbe34de7b0).',
     'artifact_covered_by': ['A3-AC4', 'A3-AC5', 'A3-AC6', 'A3-AC7']},
    {'path_or_key': 's3://opal-313476888478-lambda-artifacts/yang-pipeline/yang-generate-positioning.zip', 'kind': 's3_object',
     'commit_or_etag': 'RKnw3YkTo8okvldCf3vrTbDtWejlJjzs', 'deployed_state': 'DEPLOYED-VERIFIED',
     'deploy_evidence': 'head-object after the build: VersionId RKnw3YkTo8okvldCf3vrTbDtWejlJjzs, 36447 bytes, content-sha256 riByGXEfWXdFTEavKGG0nFRj/k4JUAjIiVKfm06Tdgk=; rollback VersionId LCmMHmpdHvv0P3FB76_anxuuors0CIlr.',
     'artifact_covered_by': ['A3-AC3', 'A3-AC7']},
    {'path_or_key': 's3://opal-data-portal-v2/json/positioning/positioning_data.json', 'kind': 's3_object',
     'commit_or_etag': 'dFjRdciig4Y.4DBiK_F0eyHtn1.YBCOC', 'deployed_state': 'DEPLOYED-VERIFIED',
     'deploy_evidence': 'prior VersionId aJ7nhwRKko3H_AMRzsNvvwkf1NiO9aou (LastModified 2026-09-15T11:06:20Z) -> new VersionId dFjRdciig4Y.4DBiK_F0eyHtn1.YBCOC (LastModified 2026-09-15T22:12:23Z); parsed compare BRANCH A.',
     'artifact_covered_by': ['A3-AC8', 'A3-AC9', 'A3-AC10']},
    {'path_or_key': 's3://opal-data-portal-v2/json/positioning/opal_aggregate.json', 'kind': 's3_object',
     'commit_or_etag': 'M8FOApCmYnAQB_3946XGOHSeqEzcL2j.', 'deployed_state': 'DEPLOYED-VERIFIED',
     'deploy_evidence': 'ABSENT (404) before; VersionId M8FOApCmYnAQB_3946XGOHSeqEzcL2j. after (LastModified 2026-09-15T22:12:23Z, 3906 bytes gzip); status OK, weights sum 1.0, each weight == members/members_sum.',
     'artifact_covered_by': ['A3-AC8', 'A3-AC9']},
    {'path_or_key': 'infra/aws/lambda/ci/lambda-source-map.json', 'kind': 'config_data', 'commit_or_etag': H['deploy'], 'deployed_state': 'COMMITTED-NOT-DEPLOY-SCOPE',
     'deploy_evidence': 'recorder commit %s stamped yang-generate-positioning only; follow-up %s restores pure ASCII with the recorder values.' % (H['recorder'][:10], H['deploy'][:10]),
     'artifact_covered_by': ['A3-AC3', 'A3-AC11']},
    {'path_or_key': 'infra/aws/terraform/yang-pipeline/CHANGELOG.json', 'kind': 'config_data', 'commit_or_etag': H['deploy'], 'deployed_state': 'COMMITTED-NOT-DEPLOY-SCOPE',
     'deploy_evidence': 'entry untagged-84fe842e written by hand in the helper shape (the helper cannot run on this device, POSN_ASTTAX W23-S4).', 'artifact_covered_by': ['A3-AC11']},
    {'path_or_key': 'org/critical_paths/change_management/20260915T2156Z_posn-aggfix-r1-producer_deploy_completion.md', 'kind': 'doc', 'commit_or_etag': H['close'],
     'deployed_state': 'COMMITTED-NOT-DEPLOY-SCOPE', 'deploy_evidence': 'opened @%s, closed @%s with 8 of 8 legs and the sentinel removed.' % (H['open'][:10], H['close'][:10]),
     'artifact_covered_by': ['A3-AC2', 'A3-AC12']},
    {'path_or_key': REL + 'a3_drive_and_read.py', 'kind': 'test', 'commit_or_etag': commit_of('a3_drive_and_read.py'), 'deployed_state': 'COMMITTED-NOT-DEPLOY-SCOPE',
     'deploy_evidence': "The order's DRIVE_AND_READ_A3: a local driver, never deployed; the drive mode invoked the two functions once each, the read modes write nothing.",
     'artifact_covered_by': ['A3-AC8', 'A3-AC9', 'A3-AC10']},
    {'path_or_key': REL + 'a3_drive_state.json', 'kind': 'doc', 'commit_or_etag': commit_of('a3_drive_state.json'), 'deployed_state': 'COMMITTED-NOT-DEPLOY-SCOPE',
     'deploy_evidence': 'The prior, new and aggregate VersionIds and the before/after listings the read modes use; TO-B3-1 reads them.', 'artifact_covered_by': ['A3-AC8', 'A3-AC9', 'A3-AC10']},
]
for o in outs:
    artifacts.append({'path_or_key': REL + o, 'kind': 'doc', 'commit_or_etag': commit_of(o), 'deployed_state': 'COMMITTED-NOT-DEPLOY-SCOPE',
                      'deploy_evidence': "Recorded evidence: stdout of the criterion's invocation with its rc; nothing deployed.",
                      'artifact_covered_by': cover[o.split('.')[0]]})

inst = {
    'schema_version': '1.0', 'to_id': 'POSN_AGGFIX.TO-A3-1', 'firm': 'FABRIC', 'phase': 'BUILD-GENERAL',
    'decomp_ref': {'doc': 'org/missions/D4/POSN/POSN_AGGFIX/decompositions/POSN_AGGFIX_DECOMP.md', 'vintage_commit': git('rev-parse', '605c03f81f'), 'to_ref': TO_REL},
    'spec_ref': {'doc': 'org/missions/D4/POSN/POSN_AGGFIX/prd/POSN_AGGFIX_PRD.md', 'group': 'OTHER', 'vintage_commit': git('rev-parse', 'cbd85e5cff')},
    'assignee': '0.9.0_WK_POSN_AGGFIX~1',
    'artifacts_produced': artifacts,
    'acceptance': rows,
    'controls': {
        'mutant': {
            'description': 'A3-AC9 CONTROL 1: one new UST holding weight raised by 0.0001 in memory; A3-AC9 CONTROL 2: the key order of new current_holdings.UST reversed in memory (the parsed compare must ignore it); A3-AC3 and A3-AC11 detector firing control CLAUDE.md.',
            'expected': 'CONTROL 1 reported as BOOK UST NON-AUM DIFFERS and one NOT PERMITTED path; CONTROL 2 zero value paths; CLAUDE.md a non-zero non-ASCII count.',
            'observed': "A3-AC9 'CONTROL 1 ... BOOK UST NON-AUM DIFFERS; classifier NOT PERMITTED paths 1 -> FIRED'; 'CONTROL 2 ... value paths 0 -> KEY ORDER IGNORED'; A3-AC3/A3-AC11 'DETECTOR FIRING CONTROL CLAUDE.md nonascii 427'.",
            'status': 'FIRED-AS-EXPECTED'},
        'determinism': {
            'method': 'N/A: the order drives exactly ONE served run and forbids a second (the driver refuses a second drive from its state file). The read modes are re-runnable read-only on fixed VersionIds.',
            'observed': 'One drive at 2026-09-15T22:12:14Z; A3-AC9 and A3-AC10 read the fixed VersionIds aJ7nhwRKko3H_AMRzsNvvwkf1NiO9aou and dFjRdciig4Y.4DBiK_F0eyHtn1.YBCOC. Per-process key order of benchmark.spread.segment is the known nondeterminism (row W1-S7); the parsed compare counted 11 key-order-only dicts and read them as no difference.',
            'status': 'N/A-WITH-REASON'}},
    'declared_exclusions': [
        {'item': 'The YangDataPipeline state machine was not started.', 'reason': 'The order: the generator and the invalidation are invoked directly on the recorded events.'},
        {'item': 'yang-time-machine and rollback-protocol.sh were not invoked, and the residual they leave (a restore to an execution before the change re-serves AGG and July aum) is not addressed.',
         'reason': 'Both halves and the order: row POSN_AGGFIX-Z-S2 carries it to the round analysis.'},
        {'item': "The main() --upload write site was not exercised.", 'reason': 'A manual CLI path the order names as not invoked (row W1-S4; TO-A2-1 A2-AC13).'},
        {'item': 'No Branch B rollback was run.', 'reason': 'A3-AC9 printed BRANCH A: 7 of 7 served delta paths permitted, 0 other keys moved, opal_aggregate status OK.'},
        {'item': "The halt gate's issuer-inbox census and HALT_ACK re-run were not performed.", 'reason': 'The gate listed no inbox and passed on the first run (row POSN_AGGFIX-Z-W1-S11).'},
        {'item': 'The CloudFront invalidation on distribution E2LPCXXBLDGWXY did not happen.', 'reason': 'The distribution does not exist; the recorded execution got the same error (row POSN_AGGFIX-Z-W1-S12). Which distribution serves the portal was not measured.'},
        {'item': 'record-terraform-deploy.sh was not edited; its CHANGELOG helper did not run.', 'reason': 'Environment-only workaround per OPERATING FACT 3; the entry is written by hand as A3-AC11 names.'},
        {'item': 'build-and-upload.sh ran under BAU_MANIFEST_SKIP=1.', 'reason': 'A3-AC3 names this repeat when the manifest gate refuses on the W19-S1 arm; the probe read PARSES CLEAN / declared_blobs ABSENT / rc 1.'},
    ],
    'surprises': [
        'POSN_AGGFIX-Z-W1-S11: the halt gate passed A3-AC5 without listing the issuer inbox, so OPERATING FACT 2 had nothing to act on (OBSERVATION, INERT).',
        'POSN_AGGFIX-Z-W1-S12: yang-invalidate-cloudfront invalidates only one of its two distributions; E2LPCXXBLDGWXY is NoSuchDistribution in this run and in the recorded execution (OBSERVATION, INERT).',
    ],
    'session_log': ('L7 worker 0.9.0_WK_POSN_AGGFIX~1 on POSN_AGGFIX.TO-A3-1 (cell AF1-s-10; round 1, slot ~1, third order), worktree /c/tmp/wk-aggfix-1-1 branch wk-posn_aggfix-1-1, '
                    '2026-09-15 ~21:55-22:3xZ. Bar: branch wk-posn_aggfix-1-1, TREE-OK; fast-forwarded fc5369a093 -> SITEZ 33dad02f79. The order was read whole at that HEAD. Halves read and cited: '
                    'ledger/NEVER_WIDEN_ROUND1_PRODUCER_COO_HALF.md @02c0bb8d91 and ledger/NEVER_WIDEN_ROUND1_PRODUCER_CTO_HALF.md @10d61c774f. Commits: open %s, build %s, recorder %s, deploy record %s, ledger close %s. '
                    'Clock note: the driver stamps local UTC; the generator log shows its uploads at 22:12:22Z while the driver printed the invalidation start at 22:12:21Z, a ~1 s box-vs-Lambda clock offset; the invokes are synchronous and ran in order. '
                    'Push state: LOCAL, not pushed.') % (H['open'][:10], H['build'][:10], H['recorder'][:10], H['deploy'][:10], H['close'][:10]),
    'compiler_tools': [
        {'tool': 'terraform (WinGet install on PATH) via .tools/safe-apply.sh', 'invocation': 'init; plan -target=module.generate_positioning -out; safe-apply apply <plan>; plan -target', 'result': '0/1/0 plan, apply complete, No changes'},
        {'tool': 'infra/aws/lambda/ci/build-and-upload.sh and record-terraform-deploy.sh', 'invocation': 'as the order names them', 'result': 'artifact uploaded and verified; source map row stamped'},
        {'tool': '.tools/aws (s3api head-object, lambda get-function-configuration)', 'invocation': 'A3-AC3, A3-AC7', 'result': 'VersionIds and CodeSha256'},
        {'tool': 'boto3 (box credentials) in a3_drive_and_read.py', 'invocation': 'stepfunctions list/get_execution_history; lambda invoke (retries disabled); s3 head/list/get_object by VersionId', 'result': 'one driven run; parsed compares'},
        {'tool': '.tools/deploy_ledger.py', 'invocation': 'open, close-leg L1..L8, close', 'result': 'entry opened and closed'},
        {'tool': '.tools/proof-of-spec-check.py (the worktree copy)', 'invocation': 'python .tools/proof-of-spec-check.py <instance> A3-AC1,...,A3-AC13', 'result': 'the verdict is its exit code'},
    ],
}
OUT.write_text(json.dumps(inst, indent=2, ensure_ascii=True) + '\n', encoding='ascii', newline='\n')
print('WROTE %s: %d acceptance rows, %d artifacts, %d surprises' % (OUT.name, len(rows), len(artifacts), len(inst['surprises'])))
