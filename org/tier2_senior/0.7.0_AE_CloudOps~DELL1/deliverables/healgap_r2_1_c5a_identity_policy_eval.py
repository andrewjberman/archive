"""C5a: grade the deny arms from the LIVE identity-based policy documents of
cot-rebalancer-runner-role, over the FULL carrier denominator, not just the policy edited.

Evaluation: an explicit Deny match wins outright; else an Allow match yields `allowed`;
else `implicitDeny`. Action and Resource matched with IAM glob semantics (* and ?).

DECLARED LIMITS, so the verdict is not read wider than it is:
  - identity-based policies ONLY. No bucket policy, SCP, permission boundary or session
    policy is evaluated. simulate-principal-policy would have covered some of those; it is
    denied to this box, which is why this exists (row MDPF_HEALGAP-D1-S10).
  - a matching statement carrying a Condition is REPORTED, never silently resolved.
"""
import glob
import json
import os
import re
import sys

CARRIERS_DIR = sys.argv[1]
ACTION = 's3:GetObject'


def as_list(v):
    if v is None:
        return []
    return v if isinstance(v, list) else [v]


def glob_match(pattern, value):
    rx = '^' + ''.join('.*' if c == '*' else '.' if c == '?' else re.escape(c)
                       for c in pattern) + '$'
    return re.match(rx, value) is not None


def action_match(stmt, action):
    if 'NotAction' in stmt:
        return not any(glob_match(p.lower(), action.lower()) for p in as_list(stmt['NotAction']))
    return any(glob_match(p.lower(), action.lower()) for p in as_list(stmt.get('Action')))


def resource_match(stmt, arn):
    if 'NotResource' in stmt:
        return not any(glob_match(p, arn) for p in as_list(stmt['NotResource']))
    return any(glob_match(p, arn) for p in as_list(stmt.get('Resource')))


carriers = []
for path in sorted(glob.glob(os.path.join(CARRIERS_DIR, '*.json'))):
    raw = open(path, encoding='utf-8').read().strip()
    if not raw:
        sys.exit('EMPTY CARRIER FILE %s -- a hole in the denominator, not an empty policy. STOP.' % path)
    carriers.append((os.path.basename(path)[:-5], json.loads(raw)))

print('CARRIER DENOMINATOR: %d identity-based policy document(s) on cot-rebalancer-runner-role' % len(carriers))
total_stmts = 0
for cname, doc in carriers:
    n = len(as_list(doc.get('Statement')))
    total_stmts += n
    print('  %-58s %d statement(s)' % (cname, n))
print('  TOTAL STATEMENTS SCANNED: %d' % total_stmts)
print()

ARMS = [
    ('CONTROL (C5b belongs to the issuer; here it proves the evaluator discriminates)',
     'arn:aws:s3:::opal-data-assets/blackdiamond/cottonwood/meta/2026-10-09-result.json', 'allowed'),
    ('C5a arm 1 (A2): no statement grants GetObject on any bronze/* resource',
     'arn:aws:s3:::opal-data-assets/blackdiamond/cottonwood/bronze/rebalancer_models/2026-10-09/page_000.json', 'implicitDeny'),
    ('C5a arm 1b (the ORIGINAL C5 implicit arm): the complete-stamp stays closed',
     'arn:aws:s3:::opal-data-assets/blackdiamond/cottonwood/meta/2026-10-09-complete.json', 'implicitDeny'),
    ('C5a arm 2: the 49f tree stays closed by EXPLICIT Deny',
     'arn:aws:s3:::opal-data-assets/blackdiamond/49f/meta/2026-10-09-result.json', 'explicitDeny'),
]

rows = []
for label, arn, expected in ARMS:
    allows, denies, conditioned = [], [], []
    for cname, doc in carriers:
        for stmt in as_list(doc.get('Statement')):
            if not (action_match(stmt, ACTION) and resource_match(stmt, arn)):
                continue
            tag = '%s/%s' % (cname, stmt.get('Sid') or '<no Sid>')
            if 'Condition' in stmt:
                conditioned.append(tag)
            (denies if stmt.get('Effect') == 'Deny' else allows).append(tag)
    verdict = 'explicitDeny' if denies else ('allowed' if allows else 'implicitDeny')
    ok = verdict == expected
    rows.append((label, arn, expected, verdict, ok))
    print(label)
    print('  resource : %s' % arn)
    print('  expected : %-13s observed: %-13s %s' % (expected, verdict, 'MATCH' if ok else '*** MISMATCH ***'))
    print('  Allow matches : %s' % (allows or 'none'))
    print('  Deny  matches : %s' % (denies or 'none'))
    if conditioned:
        print('  CONDITIONED (reported, not resolved) : %s' % conditioned)
    print()

verdicts = [r[3] for r in rows]
n_ok = sum(1 for r in rows if r[4])
print('RESULT: %d of %d arms match, over a %d-carrier / %d-statement denominator.'
      % (n_ok, len(rows), len(carriers), total_stmts))
print('DISCRIMINATION: verdicts across the four arms are %s -- %d distinct value(s), so a uniform'
      % (' / '.join(verdicts), len(set(verdicts))))
print('  "implicitDeny everything" or "allow everything" evaluator bug is excluded.')
print('C5a VERDICT: %s' % ('PASS' if all(r[4] for r in rows) else 'FAIL'))
sys.exit(0 if all(r[4] for r in rows) else 1)
