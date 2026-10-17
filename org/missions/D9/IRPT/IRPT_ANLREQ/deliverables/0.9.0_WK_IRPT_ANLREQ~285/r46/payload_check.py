#!/usr/bin/env python3
# Payload check, TO IRPT_ANLREQ.TO-AR-y-385 (criterion AR385-y-AC1). ASCII only.
# Usage: payload_check.py [branch]   (default: cand/dell2/anlreq-prod-recut)
# Prints the recut's commit list, its file list against origin/PROD, then one line
# per excluded item: ABSENT when the recut does not carry it, PRESENT when it does.
# Exit 0 and a final PAYLOAD-OK line only when every excluded item reads ABSENT.
import os
import subprocess
import sys

BASE = 'origin/PROD'
DEFAULT_BRANCH = 'cand/dell2/anlreq-prod-recut'

# excluded commits (sha, label); patch ids are computed here and checked against the record
EXCLUDED = [
    ('c05e3ddaa1ce97ecb98fe26d5f592dd01fbf0e2a', 'Trade Request form', '7e175bc14aeab08b1db182dd7a3ad50829b05229'),
    ('8e4f088522685acf223c1054cb5e896df613cbeb', 'meeting-outcome visibility', 'd0762b7150240b32b46d2e701932b297d04f175e'),
    ('12c164a0732db6b040df78a0a5d820e9fb220a96', 'original meeting-and-trade commit', '9950b74eac14324f6e061418a6716d7f31ac6a19'),
    ('406345bce120cdec5d9b7a0cef00bd7b80b680e9', 'commentary-always commit', '48aae7ade8e35ee9697ad5a9eaedcde581b6c2cf'),
]
# 7f6c698d is a merge (commentary-always merge): it is covered by its second parent 406345bce1 above

HERE = os.path.dirname(os.path.abspath(__file__))
PRESENT = []


def run(args, cwd, stdin=None):
    p = subprocess.run(['git'] + args, cwd=cwd, input=stdin, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    return p.returncode, p.stdout.decode('utf-8', 'replace'), p.stderr.decode('utf-8', 'replace')


def git(args, cwd):
    rc, out, err = run(args, cwd)
    if rc != 0:
        sys.stderr.write('ERROR: git %s rc=%d %s\n' % (' '.join(args), rc, err.strip()))
        sys.exit(2)
    return out


def patch_id(sha, cwd):
    diff = subprocess.run(['git', 'show', '--format=', '--no-color', sha], cwd=cwd,
                          stdout=subprocess.PIPE, stderr=subprocess.PIPE).stdout
    p = subprocess.run(['git', 'patch-id', '--stable'], cwd=cwd, input=diff,
                       stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    line = p.stdout.decode('utf-8', 'replace').strip()
    return line.split()[0] if line else None


def body_lines(sha, cwd):
    out = git(['show', '--format=', '--no-color', sha], cwd)
    keep = []
    for ln in out.splitlines():
        if ln.startswith('+++') or ln.startswith('---'):
            continue
        if ln.startswith('+') or ln.startswith('-'):
            keep.append(ln)
    return sorted(keep)


def present(msg):
    PRESENT.append(msg)
    print('PRESENT ' + msg)


def main():
    branch = sys.argv[1] if len(sys.argv) > 1 else DEFAULT_BRANCH
    root = git(['rev-parse', '--show-toplevel'], HERE).strip()
    portal = os.path.join(root, 'portal')
    print('payload check of %s against %s (repo %s)' % (branch, BASE, portal))

    commits_out = git(['log', '--reverse', '--format=%h %an %s', '%s..%s' % (BASE, branch)], portal)
    commits = [ln for ln in commits_out.splitlines() if ln.strip()]
    commit_shas = git(['rev-list', '--reverse', '--no-merges', '%s..%s' % (BASE, branch)], portal).split()
    print('== COMMITS (%d) git log --reverse --format=%%h %%an %%s %s..%s' % (len(commits), BASE, branch))
    for ln in commits:
        print(ln)

    diff_out = git(['diff', '--name-status', BASE, branch], portal)
    entries = [ln.split('\t') for ln in diff_out.splitlines() if ln.strip()]
    print('== FILES (%d) git diff --name-status %s %s' % (len(entries), BASE, branch))
    for ln in diff_out.splitlines():
        if ln.strip():
            print(ln)
    changed_paths = [p for e in entries for p in e[1:]]

    tree_branch = set(git(['ls-tree', '-r', '--name-only', branch], portal).splitlines())
    tree_base = set(git(['ls-tree', '-r', '--name-only', BASE], portal).splitlines())
    new_in_tree = sorted(tree_branch - tree_base)

    # 1. Trade Request form component
    hit = [p for p in changed_paths if os.path.basename(p) == 'TradeRequestParts.tsx']
    if hit:
        for p in hit:
            present('TradeRequestParts.tsx %s' % p)
    else:
        print('ABSENT TradeRequestParts.tsx (no diff entry vs %s)' % BASE)

    # 2. trade-request tests: new trade-named files under src/ (a file already on PROD is not new)
    trade_new = [p for p in new_in_tree if p.startswith('src/') and 'trade' in p.lower()]
    trade_modified = [p for p in changed_paths if p.startswith('src/') and 'trade' in p.lower()
                      and p in tree_base]
    for p in trade_new:
        present('trade-request tests %s' % p)
    for p in trade_modified:
        print('NOTE trade-named file already on PROD, touched by recut: %s' % p)
    if not trade_new:
        print('ABSENT trade-request tests (no new trade-named path under src/)')

    # 3. meeting-outcome visibility: paths, and MeetingOutcome-named new files, and added lines
    mo_paths = [p for p in new_in_tree if 'meeting-outcome-visibility' in p.lower()
                or 'meetingoutcome' in os.path.basename(p).lower()]
    for p in mo_paths:
        present('meeting-outcome-visibility path %s' % p)
    cur = None
    mo_lines = []
    for ln in git(['diff', '-U0', '--no-color', BASE, branch], portal).splitlines():
        if ln.startswith('+++ b/'):
            cur = ln[6:]
        elif ln.startswith('+') and not ln.startswith('+++') and 'MeetingOutcome' in ln:
            mo_lines.append('%s: %s' % (cur, ln[1:][:80]))
    for m in mo_lines:
        present('meeting-outcome-visibility added line %s' % m)
    if not mo_paths and not mo_lines:
        print('ABSENT meeting-outcome-visibility (no path, no MeetingOutcome-named new file, no added MeetingOutcome line)')

    # 4. commentary-always: show the commentary_requested lines at the recut and at PROD
    show_files = ['src/pages/TicketCenter/analysisRequest.ts',
                  'src/pages/InvestorReporting/contracts/wire/AnalysisSubmissionRequest.ts']
    for f in show_files:
        for ref, label in ((branch, 'recut'), (BASE, 'PROD')):
            rc, out, _ = run(['show', '%s:%s' % (ref, f)], portal)
            lines = []
            if rc == 0:
                for i, ln in enumerate(out.splitlines(), 1):
                    if 'commentary_requested' in ln:
                        lines.append('%d: %s' % (i, ln.strip()))
            print('  SHOW %s %s commentary_requested lines: %s' % (label, f, '; '.join(lines) if lines else '(none)'))
    rc, out, _ = run(['grep', '-n', '-E', 'commentary_requested[[:space:]]*[:=][[:space:]]*true', branch, '--', 'src'], portal)
    if rc == 0 and out.strip():
        for ln in out.splitlines():
            present('commentary-always constant true on the wire %s' % ln[:160])
    elif rc == 1:
        print('ABSENT commentary-always (no commentary_requested constant true anywhere under src/ at the recut)')
    else:
        sys.stderr.write('ERROR: git grep rc=%d\n' % rc)
        sys.exit(2)

    # 5. excluded patch ids against every recut commit
    for sha, label, rec_pid in EXCLUDED:
        pid = patch_id(sha, portal)
        if pid != rec_pid:
            sys.stderr.write('ERROR: patch-id of %s is %s, record says %s\n' % (sha, pid, rec_pid))
            sys.exit(2)
        hits = [c for c in commit_shas if patch_id(c, portal) == pid]
        if hits:
            for h in hits:
                present('patch-id %s (%s, %s) equals recut commit %s' % (sha, pid[:12], label, h))
        else:
            print('ABSENT patch-id %s (%s, %s) against %d commits' % (sha, pid[:12], label, len(commit_shas)))

    # 6. excluded body (the +/- lines of the whole commit), so a re-based copy is not missed
    for sha, label, _ in EXCLUDED:
        ex = body_lines(sha, portal)
        hits = [c for c in commit_shas if body_lines(c, portal) == ex]
        if hits:
            for h in hits:
                present('body of %s (%s) identical to recut commit %s' % (sha, label, h))
        else:
            print('ABSENT body %s (%s) against %d commits' % (sha, label, len(commit_shas)))

    if PRESENT:
        print('PAYLOAD-BAD %d present items' % len(PRESENT))
        return 1
    print('PAYLOAD-OK %d commits %d files' % (len(commit_shas), len(entries)))
    return 0


if __name__ == '__main__':
    sys.exit(main())
