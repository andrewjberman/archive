#!/usr/bin/env python3
"""AR410-y-AC3 -- the candidate moves only the wait loop, its texts and its two call sites.

Prints SCOPE-OK only when git diff --name-only f70745362d8b cand/dell2/anlreq-upload-resolving-backoff lists at least one
path and only src/pages/TicketCenter/analysisRequest.ts, src/pages/TicketCenter/TicketCenter.tsx and paths under
src/pages/TicketCenter/__tests__/; otherwise SCOPE-BAD <why>, exit 1.
"""
import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
WT = os.path.abspath(os.path.join(HERE, *([os.pardir] * 7)))
PORTAL = os.path.join(WT, 'portal')
BASE = 'f70745362d8baa34d78c50b8246a5f98ba7c8862'
BRANCH = 'cand/dell2/anlreq-upload-resolving-backoff'
ALLOWED_FILES = {
    'src/pages/TicketCenter/analysisRequest.ts',
    'src/pages/TicketCenter/TicketCenter.tsx',
}
ALLOWED_PREFIX = 'src/pages/TicketCenter/__tests__/'


def bad(why):
    print('SCOPE-BAD ' + why)
    sys.exit(1)


def main():
    proc = subprocess.run(['git', '-C', PORTAL, 'diff', '--name-only', BASE, BRANCH],
                          capture_output=True, text=True, timeout=120)
    if proc.returncode != 0:
        bad('git diff rc=%s: %s' % (proc.returncode, (proc.stderr or '').strip()[:200]))
    paths = [line.strip() for line in proc.stdout.splitlines() if line.strip()]
    if not paths:
        bad('git diff lists no path for ' + BRANCH)
    outside = [p for p in paths if p not in ALLOWED_FILES and not p.startswith(ALLOWED_PREFIX)]
    if outside:
        bad('outside the grant: ' + ', '.join(outside))
    print('SCOPE-OK %d paths: %s' % (len(paths), ', '.join(sorted(paths))))
    sys.exit(0)


if __name__ == '__main__':
    main()
