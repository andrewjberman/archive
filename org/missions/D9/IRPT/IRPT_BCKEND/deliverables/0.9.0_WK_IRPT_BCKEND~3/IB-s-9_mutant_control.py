"""MUTANT CONTROL for IB-s-9.

Three claims this cell rests on, each mutated by monkeypatch in a process that edits no
production file. A passing assertion never mutated has never been tested, and the risk here is
the usual one: a chain's own replay, written by the chain's author, agrees with it.

  M1  reconcile_owned adopts the NEWEST row       -> "never the newest row" must break
  M2  the duplicate receipt check is removed      -> "a duplicate touches no vendor" must break
  M3  the WAF header rule is removed from decision -> the measured 202 must stop classifying
                                                      WAF_REFRESH_REQUIRED
  M4  a described fixture is changed without its manifest row -> the new manifest re-derivation
      must catch it. This one is here because the check it controls was ADDED to arm (h) at
      report time in response to row IRPT_BCKEND-W3-S9, and a freshness check that has only ever
      seen a fresh manifest is a constant wearing a measurement's clothes. The mutation is made
      on a COPY of the fixture directory in .scratch/; no fixture in the package is touched.

A fourth control is not here because it already SHIPS INSIDE the battery: arm (b) builds a
ResubmittingJob that re-POSTs the create on restart and shows the arm failing on it.

Run: python org/missions/D9/IRPT/IRPT_BCKEND/deliverables/0.9.0_WK_IRPT_BCKEND~3/IB-s-9_mutant_control.py
"""
import json
import os
import sys

ROOT = os.path.abspath('.')
IR = os.path.join(ROOT, 'infra', 'aws', 'lambda', 'investor-reporting')
GEN = os.path.join(IR, 'ycharts', 'generate')
for p in (os.path.join(GEN, 'tests'), GEN, os.path.join(IR, '_authz'),
          os.path.join(IR, '_authz', 'tests'), os.path.join(IR, '_gate'),
          os.path.join(IR, '_keys')):
    sys.path.insert(0, p)

import job as jobmod          # noqa: E402
import recipe                 # noqa: E402
import run_offline_suite as suite  # noqa: E402
import transport as tx        # noqa: E402

NAME, FINGERPRINT = suite.owned_name()


def newest_row_probe(label):
    collection = suite.fixture('collection.json')['body']['portfolios']
    owned = json.loads(json.dumps(collection))
    owned[0]['name'] = NAME
    result = recipe.reconcile_owned(owned, NAME, FINGERPRINT)
    newest = max(owned, key=lambda r: r['created_at'])
    return {'label': label, 'adopted': result['adopted'],
            'newest_row_id': newest['model_portfolio_id'],
            'newest_row_adopted': result['newest_row_adopted'],
            'arm_c_predicate_holds': result['adopted'] == 2332060
            and result['newest_row_adopted'] is False}


def duplicate_probe(label):
    blobs = jobmod.MemoryBlobs()
    first, _ = suite.make_job(suite.base_script(collection_owned_name=NAME), blobs=blobs)
    first_run = first.run('m-dup-1', suite.REQUEST_ID, suite.REVISION, suite.HOLDINGS,
                          'OVERVIEW', cover=suite.COVER)
    second, _ = suite.make_job(suite.base_script(collection_owned_name=NAME), blobs=blobs)
    dup = second.run('m-dup-2', suite.REQUEST_ID, suite.REVISION, suite.HOLDINGS,
                     'OVERVIEW', cover=suite.COVER)
    return {'label': label,
            'first_ok': first_run.get('ok'),
            'first_vendor_requests': len(first.tx.evidence),
            'duplicate_outcome': dup.get('outcome') or ('READY' if dup.get('ok') else dup.get('why')),
            'duplicate_vendor_requests': dup.get('vendor_requests',
                                                 len(second.tx.evidence)),
            'arm_v010_duplicate_predicate_holds':
                dup.get('outcome') == 'EXISTING_ARTIFACT_REUSED'
                and dup.get('vendor_requests') == 0}


def waf_probe(label):
    spec = suite.fixture('decision_branches.json')['WAF_REFRESH_REQUIRED']
    verdict = tx.decision(
        tx.Reply(status=spec['status'], mime=spec['content_type'],
                 body=json.dumps(spec['body']).encode(), waf_action=spec['waf_action']),
        spec['operation'])
    return {'label': label, 'decision': verdict,
            'arm_v010_waf_predicate_holds': verdict == 'WAF_REFRESH_REQUIRED'}


out = {'baseline_newest': newest_row_probe('baseline'),
       'baseline_duplicate': duplicate_probe('baseline'),
       'baseline_waf': waf_probe('baseline')}

# ---- M1: reconciliation by RECENCY ----------------------------------------
real_reconcile = recipe.reconcile_owned


def recency_reconcile(collection, name, fingerprint):
    rows = list(collection or [])
    newest = max(rows, key=lambda r: r.get('created_at', ''), default=None)
    return {'adopted': (newest or {}).get('model_portfolio_id'), 'reason': 'NEWEST_ROW',
            'candidates': len(rows),
            'newest_row_id': (newest or {}).get('model_portfolio_id'),
            'newest_row_adopted': True, 'detail': 'MUTANT: adopted by recency'}


recipe.reconcile_owned = recency_reconcile
try:
    out['M1_reconcile_by_recency'] = newest_row_probe('M1')
finally:
    recipe.reconcile_owned = real_reconcile

# ---- M2: the duplicate receipt check removed ------------------------------
real_head = jobmod.MemoryBlobs.head
jobmod.MemoryBlobs.head = lambda self, bucket, key: None
try:
    out['M2_duplicate_check_removed'] = duplicate_probe('M2')
finally:
    jobmod.MemoryBlobs.head = real_head

# ---- M3: the WAF header rule removed --------------------------------------
real_decision = tx.decision


def bodyonly_decision(reply, operation, artifact_hosts=tx.ARTIFACT_HOSTS):
    stripped = tx.Reply(status=reply.status, mime=reply.mime, body=reply.body,
                        location=reply.location,
                        transport_uncertain=reply.transport_uncertain)
    return real_decision(stripped, operation, artifact_hosts)


tx.decision = bodyonly_decision
try:
    out['M3_waf_header_rule_removed'] = waf_probe('M3')
finally:
    tx.decision = real_decision

# ---- M4: a described fixture changed without its manifest row ---------------
# Exercised on a COPY, so the packaged fixtures and the served bytes are untouched.
import importlib.util   # noqa: E402
import shutil           # noqa: E402

_spec = importlib.util.spec_from_file_location(
    'battery_ib_s_9',
    os.path.join(ROOT, 'org', 'missions', 'D9', 'IRPT', 'IRPT_BCKEND', 'deliverables',
                 '0.9.0_WK_IRPT_BCKEND~3', 'battery_ib_s_9.py'))
battery = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(battery)


def manifest_probe(label):
    state = battery.manifest_freshness()
    return {'label': label, 'fresh': state['fresh'],
            'rows_matching': state['rows_matching'], 'rows_checked': state['rows_checked'],
            'stale_rows': state['stale_rows'],
            'disagreeing_denominators': state['disagreeing_denominators'],
            'unlisted_files': state['unlisted_files'],
            'arm_h_manifest_predicate_holds': state['fresh'] is True}


out['baseline_manifest'] = manifest_probe('baseline')

real_gen = battery.GEN
copy_root = os.path.join(ROOT, '.scratch', 'm4_generate')
if os.path.isdir(copy_root):
    shutil.rmtree(copy_root)
shutil.copytree(os.path.join(GEN, 'fixtures'), os.path.join(copy_root, 'fixtures'))
target = os.path.join(copy_root, 'fixtures', 'har', 'upload_ok.json')
with open(target, 'ab') as fh:
    fh.write(b'\n')          # one byte -- the smallest change a describer can miss
battery.GEN = copy_root
try:
    out['M4_fixture_changed_without_manifest'] = manifest_probe('M4')
finally:
    battery.GEN = real_gen
    shutil.rmtree(copy_root, ignore_errors=True)

out['verdict'] = {
    'baseline_newest_holds': out['baseline_newest']['arm_c_predicate_holds'],
    'M1_breaks_it': not out['M1_reconcile_by_recency']['arm_c_predicate_holds'],
    'baseline_duplicate_holds': out['baseline_duplicate']['arm_v010_duplicate_predicate_holds'],
    'M2_breaks_it': not out['M2_duplicate_check_removed']['arm_v010_duplicate_predicate_holds'],
    'baseline_waf_holds': out['baseline_waf']['arm_v010_waf_predicate_holds'],
    'M3_breaks_it': not out['M3_waf_header_rule_removed']['arm_v010_waf_predicate_holds'],
    'baseline_manifest_holds': out['baseline_manifest']['arm_h_manifest_predicate_holds'],
    'M4_breaks_it': not out['M4_fixture_changed_without_manifest'][
        'arm_h_manifest_predicate_holds'],
}
out['verdict']['mutants_fired_as_expected'] = all(out['verdict'].values())
print(json.dumps(out, indent=1, sort_keys=True))
