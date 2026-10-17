#!/usr/bin/env python3
"""AR389-y-AC1 -- ancestry and conflict-marker proof for the reconcile candidate branch.

Prints ANCESTRY-OK only when origin/PROD and origin/DEV are both ancestors of the branch head
(git merge-base --is-ancestor exits 0 for each) and `git grep` finds no conflict marker under src.
Otherwise prints ANCESTRY-BAD <why> and exits 1. Paths are derived from this file's location.
"""
import os
import subprocess
import sys

BR = 'cand/dell2/prod-into-dev-reconcile'
HERE = os.path.dirname(os.path.abspath(__file__))


def git(args, cwd):
    p = subprocess.run(['git'] + args, cwd=cwd, capture_output=True, text=True,
                       encoding='utf-8', errors='replace')
    return p.returncode, p.stdout, p.stderr


def bad(why):
    print('ANCESTRY-BAD ' + why)
    return 1


def main():
    rc, root, err = git(['rev-parse', '--show-toplevel'], HERE)
    if rc != 0:
        return bad('cannot derive the workspace root from %s: %s' % (HERE, err.strip()))
    portal = os.path.join(root.strip(), 'portal')
    rc_prod, _, _ = git(['merge-base', '--is-ancestor', 'origin/PROD', BR], portal)
    if rc_prod != 0:
        return bad('origin/PROD is not an ancestor of %s (rc=%d)' % (BR, rc_prod))
    rc_dev, _, _ = git(['merge-base', '--is-ancestor', 'origin/DEV', BR], portal)
    if rc_dev != 0:
        return bad('origin/DEV is not an ancestor of %s (rc=%d)' % (BR, rc_dev))
    rc_head, head, _ = git(['rev-parse', BR], portal)
    if rc_head != 0:
        return bad('cannot resolve %s' % BR)
    head = head.strip()
    rc_cnt, cnt, _ = git(['rev-list', '--count', 'origin/DEV..' + BR], portal)
    if rc_cnt != 0:
        return bad('rev-list count failed')
    rc_gg, hits, _ = git(['grep', '-n', '-E', '^(<<<<<<<|=======|>>>>>>>)', BR, '--', 'src'], portal)
    if rc_gg == 0:
        return bad('conflict markers under src at %s: %s' % (BR, hits.strip().splitlines()[0]))
    if rc_gg != 1:
        return bad('git grep failed with rc=%d' % rc_gg)
    print('ANCESTRY-OK head %s contains origin/PROD and origin/DEV, %s commits over DEV, no conflict markers'
          % (head[:12], cnt.strip()))
    return 0


if __name__ == '__main__':
    sys.exit(main())
