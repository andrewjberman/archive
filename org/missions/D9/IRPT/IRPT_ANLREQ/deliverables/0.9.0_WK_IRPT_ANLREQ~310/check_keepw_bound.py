#!/usr/bin/env python3
"""AR428-y-AC3 -- the Keep-words bound: the portal files changed since the AR-y-425 commit are the Ticket Center's, and 2 to 6 in number.

The portal worktree is resolved from this script's own location (workspace toplevel + portal). The base is the portal commit whose
subject opens with the AR-y-425 Keep restoration (anchored on the subject). Lists the files changed since it (committed, working
tree and untracked). Prints KEEPW-BOUND-OK files=<n> only when every changed path is under src/pages/TicketCenter/ and 2 <= n <= 6;
otherwise KEEPW-BOUND-BAD <paths> (or the reason) and exit 1.
"""
import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
BOUND_PREFIX = 'src/pages/TicketCenter/'
MIN_FILES = 2
MAX_FILES = 6
BASE_SUBJECT = '^feat(TicketCenter): C-FILING-HINT Keep path restored'


def git(cwd, *args):
    proc = subprocess.run(['git'] + list(args), cwd=cwd, capture_output=True, text=True,
                          encoding='utf-8', errors='replace', timeout=120)
    if proc.returncode != 0:
        print('KEEPW-BOUND-BAD git %s rc=%d: %s' % (' '.join(args), proc.returncode, proc.stderr.strip()))
        sys.exit(1)
    return proc.stdout


def main():
    workspace = git(HERE, 'rev-parse', '--show-toplevel').strip()
    portal = os.path.join(workspace, 'portal')
    base = git(portal, 'log', '--format=%H', '--grep=' + BASE_SUBJECT, '-1').strip()
    if not base:
        print('KEEPW-BOUND-BAD no portal commit carries the AR-y-425 subject')
        sys.exit(1)
    changed = set()
    changed.update(line for line in git(portal, 'diff', '--name-only', base).splitlines() if line.strip())
    changed.update(line for line in git(portal, 'ls-files', '--others', '--exclude-standard').splitlines() if line.strip())
    paths = sorted(changed)
    bad = [p for p in paths if not p.startswith(BOUND_PREFIX)]
    if bad:
        print('KEEPW-BOUND-BAD ' + ' '.join(bad))
        sys.exit(1)
    if not (MIN_FILES <= len(paths) <= MAX_FILES):
        print('KEEPW-BOUND-BAD files=%d outside %d..%d' % (len(paths), MIN_FILES, MAX_FILES))
        sys.exit(1)
    print('KEEPW-BOUND-OK files=%d' % len(paths))
    sys.exit(0)


if __name__ == '__main__':
    main()
