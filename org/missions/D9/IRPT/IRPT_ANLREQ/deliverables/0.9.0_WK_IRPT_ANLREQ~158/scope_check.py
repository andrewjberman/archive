#!/usr/bin/env python3
"""AR361-y-AC3: the candidate branch touches only the composer and its test files, and no shared path.

Prints SCOPE-OK only when `git -C <portal> diff --name-only c22f4508 cand/dell2/anlreq-no-price-date-t1-asof` lists only
ProspectComposer.tsx and files under the two test folders, AND `git diff c22f4508 cand/... -- <shared paths>` is empty;
otherwise SCOPE-BAD <why> and exit 1.
"""
import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
WT = subprocess.run(['git', 'rev-parse', '--show-toplevel'], cwd=HERE, capture_output=True, text=True, check=True).stdout.strip()
PORTAL = os.path.join(WT, 'portal')
BASE = 'c22f4508'
CANDIDATE = 'cand/dell2/anlreq-no-price-date-t1-asof'
ALLOWED_EXACT = {'src/pages/InvestorReporting/tabs/analysis/ProspectComposer.tsx'}
ALLOWED_PREFIX = (
    'src/pages/InvestorReporting/tabs/analysis/tests/',
    'src/pages/InvestorReporting/__tests__/dsgn-irptv1/',
)
SHARED = [
    'src/api',
    'src/pages/TicketCenter',
    'src/pages/InvestorReporting/header',
    'src/pages/InvestorReporting/tabs/analysis/prospect.ts',
]


def git(*args):
    return subprocess.run(['git', '-C', PORTAL] + list(args), capture_output=True, text=True,
                          encoding='utf-8', errors='replace')


def main():
    names = git('diff', '--name-only', BASE, CANDIDATE)
    if names.returncode != 0:
        print('SCOPE-BAD git diff --name-only rc=%s: %s' % (names.returncode, names.stderr.strip()[:200]))
        return 1
    paths = [line.strip() for line in names.stdout.splitlines() if line.strip()]
    if not paths:
        print('SCOPE-BAD no files differ between %s and %s' % (BASE, CANDIDATE))
        return 1
    outside = [p for p in paths if p not in ALLOWED_EXACT and not p.startswith(ALLOWED_PREFIX)]
    if outside:
        print('SCOPE-BAD paths outside the grant: ' + ', '.join(outside))
        return 1
    if not any(p in ALLOWED_EXACT for p in paths):
        print('SCOPE-BAD the composer itself is not among the changed paths')
        return 1
    shared = git('diff', BASE, CANDIDATE, '--', *SHARED)
    if shared.returncode != 0:
        print('SCOPE-BAD git diff (shared paths) rc=%s: %s' % (shared.returncode, shared.stderr.strip()[:200]))
        return 1
    if shared.stdout.strip():
        touched = [line for line in shared.stdout.splitlines() if line.startswith('diff --git')]
        print('SCOPE-BAD shared paths changed: ' + '; '.join(touched[:5]))
        return 1
    print('SCOPE-OK %d paths: %s' % (len(paths), ', '.join(paths)))
    return 0


if __name__ == '__main__':
    sys.exit(main())
