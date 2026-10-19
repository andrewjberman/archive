#!/usr/bin/env python3
"""AR416-y-AC3 -- the O2 write bound: every file the portal candidate changes since origin/DEV sits inside the
Ticket Center folder or is the client signature file src/api/endpoints/investor-reporting.ts.

The portal worktree is resolved from this script's own location (workspace toplevel + portal), never a typed path.
Prints O2-BOUND-OK files=<n> only when every changed path is in bound; otherwise O2-BOUND-BAD <paths> and exit 1.
"""
import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
BOUND_PREFIX = 'src/pages/TicketCenter/'
BOUND_FILE = 'src/api/endpoints/investor-reporting.ts'


def git(cwd, *args):
    proc = subprocess.run(['git'] + list(args), cwd=cwd, capture_output=True, text=True, timeout=120)
    if proc.returncode != 0:
        print('O2-BOUND-BAD git %s rc=%d: %s' % (' '.join(args), proc.returncode, proc.stderr.strip()))
        sys.exit(1)
    return proc.stdout


def main():
    workspace = git(HERE, 'rev-parse', '--show-toplevel').strip()
    portal = os.path.join(workspace, 'portal')
    base = git(portal, 'merge-base', 'HEAD', 'origin/DEV').strip()
    changed = set()
    changed.update(line for line in git(portal, 'diff', '--name-only', base).splitlines() if line.strip())
    changed.update(line for line in git(portal, 'ls-files', '--others', '--exclude-standard').splitlines()
                   if line.strip())
    paths = sorted(changed)
    bad = [p for p in paths if not (p.startswith(BOUND_PREFIX) or p == BOUND_FILE)]
    if bad:
        print('O2-BOUND-BAD ' + ' '.join(bad))
        sys.exit(1)
    print('O2-BOUND-OK files=%d' % len(paths))
    sys.exit(0)


if __name__ == '__main__':
    main()
