#!/usr/bin/env python3
"""AR425-y-AC3 -- the Keep bound: the portal files changed since the AR-y-419 commit are the Ticket Center's, and only a few.

The portal worktree is resolved from this script's own location (workspace toplevel + portal). The base is the portal commit whose
message carries AR-y-419 (git log --grep). Lists the files changed since that commit (committed, working tree and untracked).
Prints KEEP-BOUND-OK files=<n> only when every changed path is under src/pages/TicketCenter/ and 3 <= n <= 6; otherwise
KEEP-BOUND-BAD <paths> (or the reason) and exit 1.
"""
import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
BOUND_PREFIX = 'src/pages/TicketCenter/'
MIN_FILES = 3
MAX_FILES = 6


def git(cwd, *args):
    proc = subprocess.run(['git'] + list(args), cwd=cwd, capture_output=True, text=True,
                          encoding='utf-8', errors='replace', timeout=120)
    if proc.returncode != 0:
        print('KEEP-BOUND-BAD git %s rc=%d: %s' % (' '.join(args), proc.returncode, proc.stderr.strip()))
        sys.exit(1)
    return proc.stdout


def main():
    workspace = git(HERE, 'rev-parse', '--show-toplevel').strip()
    portal = os.path.join(workspace, 'portal')
    base = git(portal, 'log', '--format=%H', '--grep=AR-y-419', '-1').strip()
    if not base:
        print('KEEP-BOUND-BAD no portal commit carries AR-y-419')
        sys.exit(1)
    changed = set()
    changed.update(line for line in git(portal, 'diff', '--name-only', base).splitlines() if line.strip())
    changed.update(line for line in git(portal, 'ls-files', '--others', '--exclude-standard').splitlines() if line.strip())
    paths = sorted(changed)
    bad = [p for p in paths if not p.startswith(BOUND_PREFIX)]
    if bad:
        print('KEEP-BOUND-BAD ' + ' '.join(bad))
        sys.exit(1)
    if not (MIN_FILES <= len(paths) <= MAX_FILES):
        print('KEEP-BOUND-BAD files=%d outside %d..%d' % (len(paths), MIN_FILES, MAX_FILES))
        sys.exit(1)
    print('KEEP-BOUND-OK files=%d' % len(paths))
    sys.exit(0)


if __name__ == '__main__':
    main()
