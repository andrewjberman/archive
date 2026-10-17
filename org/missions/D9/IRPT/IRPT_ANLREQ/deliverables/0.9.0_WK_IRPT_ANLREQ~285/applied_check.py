#!/usr/bin/env python3
# Applied check, TO IRPT_ANLREQ.TO-AR-y-385 (criterion AR385-y-AC3). ASCII only.
# Prints APPLIED-OK <a> applied <l> left out only when: every one of the nine candidates is in
# exactly one of applied / left_out of r46/PROD_RECUT_CANDIDATE.json; every applied candidate's
# own commits appear as (cherry picked from commit <sha>) lines in git log origin/PROD..branch;
# every left-out candidate carries a reason. Otherwise APPLIED-BAD <why>, exit 1.
import json
import os
import re
import subprocess
import sys

BASE = 'origin/PROD'
BRANCH = 'cand/dell2/anlreq-prod-recut-v2'
NINE = [
    'anlreq-filing-notice',
    'anlreq-ticket-commentary-pdf-reader',
    'asof-date-only-no-invented-clock',
    'irpt-fwd10-partial-history-sentence',
    'irpt-series-mirror-contract-031',
    'tckt-meeting-form-prod-recut',
    'anlreq-advisor-login-email',
    'ticket-hop-failure-read-dev',
    'anlreq-report-ref-revision-string',
]
HERE = os.path.dirname(os.path.abspath(__file__))
REC = os.path.join(HERE, 'r46', 'PROD_RECUT_CANDIDATE.json')
CMT = os.path.join(HERE, 'r46', 'CANDIDATE_COMMITS.json')


def bad(why):
    print('APPLIED-BAD ' + why)
    sys.exit(1)


def git(args, cwd):
    p = subprocess.run(['git'] + args, cwd=cwd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=120)
    if p.returncode != 0:
        bad('git %s rc=%d %s' % (' '.join(args), p.returncode, p.stderr.decode('utf-8', 'replace').strip()))
    return p.stdout.decode('utf-8', 'replace')


def main():
    root = git(['rev-parse', '--show-toplevel'], HERE).strip()
    portal = os.path.join(root, 'portal')
    try:
        rec = json.load(open(REC, encoding='utf-8'))
        cmt = json.load(open(CMT, encoding='utf-8'))
    except (OSError, ValueError) as e:
        bad('cannot read record: %s' % e)

    applied = rec.get('applied', [])
    left_out = rec.get('left_out', [])
    names_applied = [a.get('candidate') for a in applied]
    names_left = [x.get('candidate') for x in left_out]
    for n in NINE:
        k = names_applied.count(n) + names_left.count(n)
        if k != 1:
            bad('candidate %s is in %d of applied/left_out (need exactly 1)' % (n, k))
    extra = sorted(set(names_applied + names_left) - set(NINE))
    if extra:
        bad('names outside the nine candidates: %s' % ', '.join(extra))

    # own commits of each applied candidate: the record must equal CANDIDATE_COMMITS.json
    own_by_name = {c['branch'].replace('cand/dell2/', ''): c['own_commits'] for c in cmt['candidates']}
    body = git(['log', '--format=%B%x1e', '%s..%s' % (BASE, BRANCH)], portal)
    trailers = set(re.findall(r'\(cherry picked from commit ([0-9a-f]{40})\)', body))
    checked = 0
    for a in applied:
        n = a['candidate']
        own = own_by_name.get(n)
        if own is None:
            bad('applied candidate %s has no own commits in CANDIDATE_COMMITS.json' % n)
        if a.get('own_commits') != own:
            bad('applied %s own_commits differ from CANDIDATE_COMMITS.json' % n)
        for sha in own:
            if sha not in trailers:
                bad('applied %s own commit %s has no cherry-pick trailer on %s' % (n, sha, BRANCH))
            checked += 1
        picks = a.get('cherry_picks', {})
        for sha in own:
            if picks.get(sha) is None:
                bad('applied %s has no cherry-pick sha recorded for %s' % (n, sha))
    for x in left_out:
        if not str(x.get('reason', '')).strip():
            bad('left-out candidate %s carries no reason' % x.get('candidate'))
        for c in x.get('own_commits', []):
            if c.get('sha') in trailers:
                bad('left-out candidate %s commit %s is on the recut' % (x.get('candidate'), c.get('sha')))

    # the lint commit is a step-3 addition, recorded separately; its trailer must be present
    lint = rec.get('lint_fix', {}).get('original_commit')
    if lint and lint not in trailers:
        bad('lint-fix commit %s has no trailer on %s' % (lint, BRANCH))

    print('APPLIED-OK %d applied %d left out (%d own commits checked)' % (len(applied), len(left_out), checked))
    return 0


if __name__ == '__main__':
    sys.exit(main())
