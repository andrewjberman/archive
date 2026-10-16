"""pin_c23_instance.py <worktree root> <catalog commit>: pin the MX-c-23 proof instance's produced artifacts to the commits that carried them.

regrade_c23_instance.py rewrites only the acceptance rows. The worker's first (FAIL) instance named six produced files `PENDING-THIS-COMMIT`; the proof checker
refuses that for a file committed BEFORE the instance (artifact-resolution). This script, run in the worker's worktree (so `git log` sees its commits):
  - pins every PENDING-THIS-COMMIT entry to the last commit that touched its path;
  - points the four saved c23.ACn.out entries at a3_evidence/ (the regrade run's evidence);
  - adds the landed catalog itself as a produced artifact, pinned to <catalog commit>.
It asserts that no PENDING-THIS-COMMIT remains. Nothing else in the instance changes.
"""
import json
import os
import subprocess
import sys

root, catalog_commit = sys.argv[1], sys.argv[2]
D = 'org/missions/D9/NFRA/NFRA_MCPINDEX/deliverables/0.9.0_WK_NFRA_MCPINDEX~45/'
INSTANCE = os.path.join(root, D + 'NFRA_MCPINDEX.TO-MX-c-23.assets-rows-vendor-firm-and-the-twelve-schwab-dim-rows.proof_of_spec.json')
CAT = 'infra/aws/ec2/opal-gateway/app/refs/DATA_CATALOG.yaml'
d = json.load(open(INSTANCE, encoding='utf-8'))


def last(path):
    return subprocess.run(['git', 'log', '-n', '1', '--format=%h', '--', path], capture_output=True, text=True, cwd=root).stdout.strip()


arts = []
for a in d['artifacts_produced']:
    p = a['path_or_key']
    if a['commit_or_etag'] != 'PENDING-THIS-COMMIT':
        if p != CAT:
            arts.append(a)
        continue
    a = dict(a)
    base = p.split('/')[-1]
    if base.startswith('c23.AC') and base.endswith('.out'):
        n = base[4:7]
        a['path_or_key'] = D + 'a3_evidence/c23.%s.out' % n
        a['commit_or_etag'] = last(a['path_or_key'])
        a['deploy_evidence'] = 'the saved output of c23.%s.sh on the landed final catalog (exit=0, RESULT: PASS).' % n
    else:
        a['commit_or_etag'] = last(p)
        if p.endswith('dim_asset.yaml'):
            a['deploy_evidence'] = ('one of the 12 new row files (generated); dim_asset is read by no client tool, so it keeps read_tool null and '
                                    'gap_owner NFRA_OPLGTW (ruled OUT of the finish line, CTO @33d41059d9).')
    assert a['commit_or_etag'] and a['commit_or_etag'] != 'PENDING-THIS-COMMIT', p
    arts.append(a)
arts.append({'path_or_key': CAT, 'kind': 'config_data', 'commit_or_etag': catalog_commit, 'deployed_state': 'COMMITTED-NOT-DEPLOY-SCOPE',
             'deploy_evidence': ('the final runtime catalog emitted by the issuer (emit_final.sh): md5 9519ebce3a1b92cee07a5507d1912dd3, git blob '
                                 'cf7616c08ec6b50a4676f962546ec6e732772e39; placed by place_catalog.py; shipped by MX-r-15.'),
             'artifact_covered_by': ['AC1', 'AC2', 'AC3', 'AC4']})
d['artifacts_produced'] = arts
assert not [a for a in arts if a['commit_or_etag'] == 'PENDING-THIS-COMMIT']
open(INSTANCE, 'w', encoding='utf-8', newline='\n').write(json.dumps(d, indent=2, ensure_ascii=False) + '\n')
print('pinned %d artifacts; catalog at %s' % (len(arts), catalog_commit))
