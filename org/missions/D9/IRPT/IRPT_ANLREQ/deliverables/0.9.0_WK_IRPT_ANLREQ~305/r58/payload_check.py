#!/usr/bin/env python3
"""AR411-y-AC1 -- payload check of the prod-based recut (TO-AR-y-411, step 3).

Prints the commit list and the file list of cand/dell2/anlreq-prod-recut-v3 against origin/PROD (in the portal
worktree of this checkout, found from this file's own location), then one line per item. Every item must read ABSENT.
A present item prints PRESENT <what> <path or sha> and the script exits 1. It ends with PAYLOAD-OK <n> commits <m> files
only when every item is ABSENT.
"""
import os
import re
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
BRANCH = 'cand/dell2/anlreq-prod-recut-v3'
BASE = 'origin/PROD'
TC_PREFIX = 'src/pages/TicketCenter/'
OLD_CONSTANTS = ('UPLOAD_MAX_TRIES', 'UPLOAD_WAIT_MS')
COMMENTARY = re.compile(r"commentary_requested['\"]?\s*(?::|=)\s*true\b")


def git(portal, args, ok_rcs=(0,)):
    proc = subprocess.run(['git', '-C', portal] + args, capture_output=True, text=True, encoding='utf-8', errors='replace')
    if proc.returncode not in ok_rcs:
        print('PAYLOAD-BAD git %s rc=%d: %s' % (' '.join(args), proc.returncode, (proc.stderr or '').strip()))
        sys.exit(1)
    return proc.returncode, proc.stdout


def main():
    top = git(HERE, ['rev-parse', '--show-toplevel'])[1].strip()
    portal = os.path.join(top, 'portal')
    _, commits = git(portal, ['log', '--reverse', '--format=%h %an %s', '%s..%s' % (BASE, BRANCH)])
    commit_lines = [c for c in commits.splitlines() if c.strip()]
    _, names = git(portal, ['diff', '--no-renames', '--name-status', BASE, BRANCH])
    name_lines = [n for n in names.splitlines() if n.strip()]
    _, paths_out = git(portal, ['diff', '--no-renames', '--name-only', BASE, BRANCH])
    paths = [p for p in paths_out.splitlines() if p.strip()]
    _, diff = git(portal, ['diff', '--no-renames', BASE, BRANCH])
    added = [ln[1:] for ln in diff.splitlines() if ln.startswith('+') and not ln.startswith('+++')]

    print('COMMITS %s..%s' % (BASE, BRANCH))
    for c in commit_lines:
        print(c)
    print('FILES %s %s' % (BASE, BRANCH))
    for n in name_lines:
        print(n)

    present = []

    outside = [p for p in paths if not p.startswith(TC_PREFIX)]
    if outside:
        present += ['PRESENT non-TicketCenter-path ' + p for p in outside]
    else:
        print('ABSENT non-TicketCenter-path (0 of %d changed paths outside %s)' % (len(paths), TC_PREFIX))

    trade = [p for p in paths if 'trade' in p.lower()]
    if trade:
        present += ['PRESENT trade-path-change ' + p for p in trade]
    else:
        print('ABSENT trade-path-change (0 of %d changed paths match trade)' % len(paths))

    flagged = [ln for ln in added if COMMENTARY.search(ln)]
    if flagged:
        present += ['PRESENT commentary-always ' + ln.strip()[:120] for ln in flagged]
    else:
        print('ABSENT commentary-always (0 added lines set commentary_requested to true)')

    # the constants are gone from every added line AND from every remaining line of the recut's src tree
    tree_hits = []
    for name in OLD_CONSTANTS:
        rc, out = git(portal, ['grep', '-n', '-F', name, BRANCH, '--', 'src'], ok_rcs=(0, 1))
        for line in out.splitlines():
            tree_hits.append(line)
    added_hits = [ln for ln in added if any(name in ln for name in OLD_CONSTANTS)]
    if tree_hits:
        present += ['PRESENT UPLOAD_MAX_TRIES-or-UPLOAD_WAIT_MS-in-tree ' + h[:160] for h in tree_hits]
    if added_hits:
        present += ['PRESENT UPLOAD_MAX_TRIES-or-UPLOAD_WAIT_MS-in-added-line ' + h.strip()[:120] for h in added_hits]
    if not tree_hits and not added_hits:
        print('ABSENT UPLOAD_MAX_TRIES (no added or remaining src line names UPLOAD_MAX_TRIES or UPLOAD_WAIT_MS)')

    for line in present:
        print(line)
    if present:
        print('PAYLOAD-BAD %d present item(s)' % len(present))
        return 1
    print('PAYLOAD-OK %d commits %d files' % (len(commit_lines), len(paths)))
    return 0


if __name__ == '__main__':
    sys.exit(main())
