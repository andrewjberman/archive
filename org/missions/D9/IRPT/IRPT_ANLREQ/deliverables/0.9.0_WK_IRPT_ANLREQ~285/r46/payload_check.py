#!/usr/bin/env python3
# Payload check, TO IRPT_ANLREQ.TO-AR-y-385, criterion AR385-y-AC1, AMENDMENT 1 rules. ASCII only.
# Usage: payload_check.py [branch]   (default: cand/dell2/anlreq-prod-recut-v2)
# Prints the recut's commit list, its file list against origin/PROD, then one line per
# excluded item: ABSENT when the recut does not carry it, PRESENT when it does.
# Exit 0 and a final PAYLOAD-OK line only when every excluded item reads ABSENT or ONLY-8b35.
import os
import subprocess
import sys

BASE = 'origin/PROD'
DEFAULT_BRANCH = 'cand/dell2/anlreq-prod-recut-v2'

# the approved tckt-meeting-form-prod-recut (AMENDMENT 1: its meeting-form content is IN the set)
MEETING_8B35 = {
    'e5c8e07569aa090b29b7a31c363f68246ce41821',
    '4e1e35bfa0826bbf07971b4cc0bad76ff79edc9d',
}

# excluded commits (sha, label, recorded patch id). 7f6c698d is a merge: its second parent
# 406345bce1 is the excluded commit, and 7f6c698d itself is checked by ancestry below.
EXCLUDED = [
    ('c05e3ddaa1ce97ecb98fe26d5f592dd01fbf0e2a', 'Trade Request form',
     '7e175bc14aeab08b1db182dd7a3ad50829b05229'),
    ('406345bce120cdec5d9b7a0cef00bd7b80b680e9', 'commentary-always commit (second parent of 7f6c698d)',
     '48aae7ade8e35ee9697ad5a9eaedcde581b6c2cf'),
]
EXCLUDED_MERGES = [
    ('7f6c698d429cffeb5990265ed35d20a46e6735e3', 'commentary-always merge'),
]

# informational only (AMENDMENT 1: NOT excluded): reported, never counted as PRESENT
INFO = [
    ('12c164a0732db6b040df78a0a5d820e9fb220a96', 'original meeting-and-trade commit',
     '9950b74eac14324f6e061418a6716d7f31ac6a19'),
    ('8e4f088522685acf223c1054cb5e896df613cbeb', 'meeting-outcome visibility',
     'd0762b7150240b32b46d2e701932b297d04f175e'),
]

HERE = os.path.dirname(os.path.abspath(__file__))
PRESENT = []


def run(args, cwd):
    p = subprocess.run(['git'] + args, cwd=cwd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
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


def is_ancestor(sha, branch, cwd):
    rc, _, _ = run(['merge-base', '--is-ancestor', sha, branch], cwd)
    return rc == 0


def source_of(sha, cwd):
    # a recut commit is a cherry-pick: its -x trailer names the candidate commit it copies
    # the LAST such trailer is this recut commit's own -x line (an earlier one may come from the copied message)
    msg = git(['log', '-1', '--format=%B', sha], cwd)
    found = sha
    for ln in msg.splitlines():
        ln = ln.strip()
        if ln.startswith('(cherry picked from commit ') and ln.endswith(')'):
            found = ln[len('(cherry picked from commit '):-1].strip()
    return found


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
    for p in hit:
        present('TradeRequestParts.tsx %s' % p)
    if not hit:
        print('ABSENT TradeRequestParts.tsx (no diff entry vs %s; on %s: %s)' % (
            BASE, BASE, 'yes, untouched' if 'src/pages/TicketCenter/TradeRequestParts.tsx' in tree_base else 'no'))

    # 2. trade-request tests: NEW trade-named paths under src/ (a file already on PROD is not new)
    trade_new = [p for p in new_in_tree if p.startswith('src/') and 'trade' in p.lower()]
    for p in trade_new:
        present('trade-request tests %s' % p)
    if not trade_new:
        trade_base = [p for p in tree_base if p.startswith('src/') and 'trade' in p.lower()]
        print('ABSENT trade-request tests (no new trade-named path under src/; trade-named files already on %s: %d)'
              % (BASE, len(trade_base)))

    # 3. trade-path-change (AMENDMENT 1): the recut modifies NO path matching trade, whether or not it was on PROD
    trade_changed = [p for p in changed_paths if 'trade' in p.lower()]
    for p in trade_changed:
        present('trade-path-change %s' % p)
    if not trade_changed:
        print('ABSENT trade-path-change (no diff entry vs %s matches trade, case-insensitive)' % BASE)

    # 4. meeting-outcome visibility (AMENDMENT 1): every meeting path is owned by the two 8b35 commits only
    # the recut commits, mapped to the candidate commit each one copies (the -x trailer)
    source = {c: source_of(c, portal) for c in commit_shas}
    meet_paths = [p for p in changed_paths if 'meeting' in p.lower()]
    for p in meet_paths:
        touching = git(['rev-list', '--no-merges', '%s..%s' % (BASE, branch), '--', p], portal).split()
        srcs = [source.get(c, c) for c in touching]
        foreign = [s for s in srcs if s not in MEETING_8B35]
        if foreign:
            present('meeting-outcome-visibility path %s touched by non-8b35 commits %s' % (
                p, ' '.join(s[:8] for s in foreign)))
        else:
            print('ONLY-8b35 meeting-outcome-visibility path %s touched only by 8b35 commits %s' % (
                p, ' '.join(s[:8] for s in srcs) if srcs else '(no recut commit)'))
    if not meet_paths:
        print('ABSENT meeting-outcome-visibility (no diff entry vs %s matches meeting)' % BASE)
    # the outcome-line content (MeetingOutcome) is introduced by 8b35 commits only
    n_non8b = 0
    for c in commit_shas:
        if source[c] in MEETING_8B35:
            continue
        n_non8b += 1
        rc, out, _ = run(['show', '--format=', '--no-color', '-U0', c], portal)
        added = [ln for ln in out.splitlines()
                 if ln.startswith('+') and not ln.startswith('+++') and 'MeetingOutcome' in ln]
        for ln in added:
            present('meeting-outcome content %s in non-8b35 commit %s' % (ln[1:][:80].strip(), c[:8]))
    print('ONLY-8b35 meeting-outcome content: MeetingOutcome added lines in %d non-8b35 recut commits checked' % n_non8b)

    # 5. commentary-always: the wire line at the recut and at PROD, and no constant true anywhere under src/
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
    rc, out, _ = run(['grep', '-n', '-E', 'commentary_requested[[:space:]]*[:=][[:space:]]*true', branch, '--', 'src'],
                     portal)
    if rc == 0 and out.strip():
        for ln in out.splitlines():
            present('commentary-always constant true on the wire %s' % ln[:160])
    elif rc == 1:
        print('ABSENT commentary-always (no commentary_requested constant true under src/ at the recut)')
    else:
        sys.stderr.write('ERROR: git grep rc=%d\n' % rc)
        sys.exit(2)

    # 6. excluded items: ancestry, patch id and body against every recut commit
    # the recut's OWN commits are origin/PROD..branch; a commit on the base is not a recut commit
    own_all = set(git(['rev-list', '%s..%s' % (BASE, branch)], portal).split())
    for sha, label in EXCLUDED_MERGES:
        if sha in own_all:
            present('own commit merge %s (%s)' % (sha[:8], label))
        else:
            print('ABSENT own commit merge %s (%s) in %s..%s' % (sha[:8], label, BASE, branch))
    for sha, label, rec_pid in EXCLUDED:
        if sha in own_all:
            present('own commit %s (%s)' % (sha[:8], label))
        else:
            print('ABSENT own commit %s (%s) in %s..%s' % (sha[:8], label, BASE, branch))
        if is_ancestor(sha, BASE, portal):
            print('INFO %s (%s) is an ancestor of %s (on the base; the recut carries no copy of it)' % (
                sha[:8], label, BASE))
        pid = patch_id(sha, portal)
        if pid != rec_pid:
            sys.stderr.write('ERROR: patch-id of %s is %s, record says %s\n' % (sha, pid, rec_pid))
            sys.exit(2)
        hits = [c for c in commit_shas if patch_id(c, portal) == pid]
        if hits:
            for h in hits:
                present('patch-id %s (%s, %s) equals recut commit %s' % (sha[:8], pid[:12], label, h[:8]))
        else:
            print('ABSENT patch-id %s (%s, %s) against %d commits' % (sha[:8], pid[:12], label, len(commit_shas)))
        ex = body_lines(sha, portal)
        bhits = [c for c in commit_shas if body_lines(c, portal) == ex]
        if bhits:
            for h in bhits:
                present('body of %s (%s) identical to recut commit %s' % (sha[:8], label, h[:8]))
        else:
            print('ABSENT body %s (%s) against %d commits' % (sha[:8], label, len(commit_shas)))

    # 7. informational: the two commits AMENDMENT 1 keeps IN the set, with the patch-id relation read
    for sha, label, rec_pid in INFO:
        pid = patch_id(sha, portal)
        hits = [c for c in commit_shas if patch_id(c, portal) == pid]
        print('INFO not excluded (AMENDMENT 1) %s (%s) patch-id %s equals recut commits: %s' % (
            sha[:8], label, pid[:12] if pid else None, ' '.join(h[:8] for h in hits) if hits else '(none)'))

    if PRESENT:
        print('PAYLOAD-BAD %d present items' % len(PRESENT))
        return 1
    print('PAYLOAD-OK %d commits %d files' % (len(commit_shas), len(entries)))
    return 0


if __name__ == '__main__':
    sys.exit(main())
