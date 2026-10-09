"""Evaluate one (action, resource) against a principal's LIVE identity-based policy documents.

WHY THIS EXISTS: `iam:SimulatePrincipalPolicy` is granted to this box's agent principal only for its
OWN ARN, so the canonical instrument is unavailable for any other role here (rows
MDPF_HEALGAP-D1-S10 / D1-S11). `iam:SimulateCustomPolicy` is absent too. Two WORLD-risk orders in one
day have needed this, so it is a committed instrument rather than an inline one-off.

Evaluation: an explicit Deny match wins outright; else an Allow match yields `allowed`; else
`implicitDeny`. Action and Resource matched with IAM glob semantics (* and ?).

IT PRINTS THE MATCHING STATEMENTS, NOT JUST A VERDICT. A bare `allowed` cannot distinguish a
least-privilege grant on one key from `s3:*` on `*`, and that difference is usually the whole question.

DECLARED LIMITS, so no verdict is read wider than it is:
  - identity-based policies ONLY. No bucket policy, SCP, permission boundary or session policy is
    evaluated. The real simulator would cover some of those.
  - a matching statement carrying a Condition is REPORTED, never silently resolved.
  - an EMPTY carrier file aborts the run: a hole in the denominator is not an empty policy.

Usage:
  python identity_policy_eval.py <carriers_dir> <action> <resource_arn> [<control_resource_arn>]
"""
from __future__ import annotations

import glob
import json
import os
import re
import sys


def as_list(v):
    if v is None:
        return []
    return v if isinstance(v, list) else [v]


def glob_match(pattern: str, value: str) -> bool:
    rx = '^' + ''.join('.*' if c == '*' else '.' if c == '?' else re.escape(c)
                       for c in pattern) + '$'
    return re.match(rx, value) is not None


def action_match(stmt, action: str) -> bool:
    if 'NotAction' in stmt:
        return not any(glob_match(p.lower(), action.lower()) for p in as_list(stmt['NotAction']))
    return any(glob_match(p.lower(), action.lower()) for p in as_list(stmt.get('Action')))


def resource_match(stmt, arn: str) -> bool:
    if 'NotResource' in stmt:
        return not any(glob_match(p, arn) for p in as_list(stmt['NotResource']))
    return any(glob_match(p, arn) for p in as_list(stmt.get('Resource')))


def load(carriers_dir: str):
    out = []
    for path in sorted(glob.glob(os.path.join(carriers_dir, '*.json'))):
        raw = open(path, encoding='utf-8').read().strip()
        if not raw:
            sys.exit('EMPTY CARRIER FILE %s -- a hole in the denominator, not an empty policy. STOP.' % path)
        out.append((os.path.basename(path)[:-5], json.loads(raw)))
    if not out:
        sys.exit('NO CARRIERS in %s -- refusing to report a verdict over nothing.' % carriers_dir)
    return out


def evaluate(carriers, action: str, arn: str):
    allows, denies, conditioned = [], [], []
    for cname, doc in carriers:
        for stmt in as_list(doc.get('Statement')):
            if not (action_match(stmt, action) and resource_match(stmt, arn)):
                continue
            tag = '%s/%s' % (cname, stmt.get('Sid') or '<no Sid>')
            if 'Condition' in stmt:
                conditioned.append(tag)
            target = denies if stmt.get('Effect') == 'Deny' else allows
            target.append((tag, as_list(stmt.get('Action')), as_list(stmt.get('Resource'))))
    verdict = 'explicitDeny' if denies else ('allowed' if allows else 'implicitDeny')
    return verdict, allows, denies, conditioned


def report(label: str, verdict: str, allows, denies, conditioned):
    print('  %s -> %s' % (label, verdict))
    for tag, acts, res in denies:
        print('     DENY  %s  Action=%s  Resource=%s' % (tag, acts, res))
    for tag, acts, res in allows:
        print('     ALLOW %s  Action=%s  Resource=%s' % (tag, acts, res))
    if not allows and not denies:
        print('     (no statement matches this action on this resource)')
    if conditioned:
        print('     CONDITIONED (reported, not resolved): %s' % conditioned)


def main() -> int:
    if len(sys.argv) < 4:
        print(__doc__)
        return 2
    carriers_dir, action, arn = sys.argv[1], sys.argv[2], sys.argv[3]
    control = sys.argv[4] if len(sys.argv) > 4 else None
    carriers = load(carriers_dir)
    total = sum(len(as_list(doc.get('Statement'))) for _, doc in carriers)
    print('CARRIERS: %d document(s), %d statement(s) -- %s'
          % (len(carriers), total, ', '.join(n for n, _ in carriers)))
    v, a, dn, c = evaluate(carriers, action, arn)
    print('ACTION: %s' % action)
    report(arn, v, a, dn, c)
    if control:
        cv, ca, cdn, cc = evaluate(carriers, action, control)
        print('  -- control resource, to show the evaluator is not answering the same way for everything --')
        report(control, cv, ca, cdn, cc)
        print('  DISCRIMINATES: %s (target %s vs control %s)' % (v != cv, v, cv))
    print('VERDICT: %s' % v)
    return 0


if __name__ == '__main__':
    sys.exit(main())
