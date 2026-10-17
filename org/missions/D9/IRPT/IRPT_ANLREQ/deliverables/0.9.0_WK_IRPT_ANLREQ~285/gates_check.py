#!/usr/bin/env python3
# Gates check, TO IRPT_ANLREQ.TO-AR-y-385, criterion AR385-y-AC2, AMENDMENT 1 rules. ASCII only.
# Runs the step-5 gates on cand/dell2/anlreq-prod-recut-v2 in the portal worktree:
#   typecheck (bun run typecheck) and eslint on every added or changed .ts/.tsx file (live, 0 errors);
#   the bun test DELTA: the failing test lines at the recut must EQUAL those at origin/PROD, and every
#   load error (a test file that fails to load) at the recut but not at origin/PROD must be listed in
#   r46/GATES.json new_load_errors with a cause read. The two runs are the saved outputs
#   r46/tests_recut_v2.plain.txt and r46/tests_prod_v2.plain.txt, pinned by sha256 in GATES.json.
#   --rerun-tests regenerates them (detaches origin/PROD in the portal worktree, then returns to the branch).
# Prints GATES-OK ... only when all hold; otherwise GATES-BAD <why>, exit 1.
# Control: payload_check.py against cand/dell2/anlreq-report-ref-revision-string must exit 1 (CONTROL-FIRES).
import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
import time
from collections import Counter

BASE = 'origin/PROD'
BRANCH = 'cand/dell2/anlreq-prod-recut-v2'
CONTROL_BRANCH = 'cand/dell2/anlreq-report-ref-revision-string'
TEST_DIRS = ['src/pages/TicketCenter', 'src/pages/InvestorReporting']
HERE = os.path.dirname(os.path.abspath(__file__))
R46 = os.path.join(HERE, 'r46')
PAYLOAD = os.path.join(R46, 'payload_check.py')
GATES_JSON = os.path.join(R46, 'GATES.json')
TEST_RECUT = os.path.join(R46, 'tests_recut_v2.plain.txt')
TEST_PROD = os.path.join(R46, 'tests_prod_v2.plain.txt')
ANSI = re.compile(r'\x1b\[[0-9;]*m')
TIMING = re.compile(r'\s*\[[0-9.]+m?s\]\s*$')
FRAME = re.compile(r'at .*\(([^()]*\.(?:tsx?|jsx?)):\d+:\d+\)')
WT_PORTAL = r'C:\dev\wk-irpt-anlreq-285\portal' + '\\'


def git(args, cwd):
    p = subprocess.run(['git'] + args, cwd=cwd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=120)
    return p.returncode, p.stdout.decode('utf-8', 'replace'), p.stderr.decode('utf-8', 'replace')


def bun_exe():
    exe = shutil.which('bun')
    if not exe:
        sys.exit('GATES-BAD bun not found on PATH')
    return exe


def run_bun(args, cwd, timeout):
    t0 = time.time()
    try:
        p = subprocess.run([bun_exe()] + args, cwd=cwd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                           timeout=timeout)
        rc, out = p.returncode, p.stdout.decode('utf-8', 'replace')
    except subprocess.TimeoutExpired as e:
        rc = 124
        out = (e.stdout or b'').decode('utf-8', 'replace') + '\nTIMEOUT after %ss' % timeout
    return rc, ANSI.sub('', out), round(time.time() - t0, 1)


def summary_of(text):
    # bun prints a per-file block ("1 error") earlier; the FINAL block is the last "pass" line and the four lines after it
    matches = list(re.finditer(r'^\s*(\d+) (pass|skip|fail|todo|errors?)\s*$', text, re.M))
    passes = [i for i, m in enumerate(matches) if m.group(2) == 'pass']
    summary = {}
    if passes:
        for m in matches[passes[-1]:passes[-1] + 4]:
            summary[m.group(2)] = int(m.group(1))
    ran = re.search(r'Ran (\d+) tests across (\d+) files', text)
    return {
        'passed': summary.get('pass', 0), 'skipped': summary.get('skip', 0),
        'failed': summary.get('fail', 0), 'errors': summary.get('error', 0) + summary.get('errors', 0),
        'ran': int(ran.group(1)) if ran else None, 'files': int(ran.group(2)) if ran else None,
    }


def read_test(path):
    with open(path, 'rb') as fh:
        raw = fh.read()
    text = raw.decode('utf-8', 'replace')
    fails = [TIMING.sub('', ln.strip()) for ln in text.split('\n') if ln.strip().startswith('\u2717')]
    errs = Counter()
    lines = text.split('\n')
    for i, ln in enumerate(lines):
        if ln.startswith('error:'):
            msg = TIMING.sub('', ln)
            frame = ''
            for j in range(i + 1, min(i + 6, len(lines))):
                m = FRAME.search(lines[j])
                if m:
                    frame = m.group(1).replace(WT_PORTAL, '')
                    break
            errs[msg[:160] + ' || ' + frame] += 1
    return {'sha256': hashlib.sha256(raw).hexdigest(), 'summary': summary_of(text), 'fail_lines': fails,
            'error_blocks': errs}


def rerun_tests(portal):
    rc, cur, _ = git(['rev-parse', '--abbrev-ref', 'HEAD'], portal)
    if cur.strip() != BRANCH:
        sys.exit('GATES-BAD portal worktree is not on %s (on %s)' % (BRANCH, cur.strip()))
    rc, out, dur = run_bun(['test'] + TEST_DIRS, portal, 900)
    with open(TEST_RECUT, 'w', encoding='utf-8', newline='\n') as fh:
        fh.write(out)
    rc2, _, err = git(['checkout', '--detach', BASE], portal)
    if rc2 != 0:
        sys.exit('GATES-BAD checkout of %s failed: %s' % (BASE, err.strip()))
    try:
        rc3, out3, dur3 = run_bun(['test'] + TEST_DIRS, portal, 900)
        with open(TEST_PROD, 'w', encoding='utf-8', newline='\n') as fh:
            fh.write(out3)
    finally:
        git(['checkout', BRANCH], portal)


def main():
    rerun = '--rerun-tests' in sys.argv
    root = git(['rev-parse', '--show-toplevel'], HERE)[1].strip()
    portal = os.path.join(root, 'portal')
    rc, head, _ = git(['rev-parse', BRANCH], portal)
    rc2, cur, _ = git(['rev-parse', '--abbrev-ref', 'HEAD'], portal)
    head = head.strip()
    if rc != 0 or cur.strip() != BRANCH:
        print('GATES-BAD portal worktree is not on %s (on %s)' % (BRANCH, cur.strip()))
        return 1
    if rerun:
        rerun_tests(portal)

    record = {'branch': BRANCH, 'head': head, 'base': BASE}
    bad = []

    # 1. typecheck (live)
    rc, out, dur = run_bun(['run', 'typecheck'], portal, 480)
    errs = len(re.findall(r'error TS\d+', out))
    record['typecheck'] = {'cmd': 'bun run typecheck', 'rc': rc, 'error_TS_lines': errs, 'seconds': dur}
    if rc != 0 or errs != 0:
        bad.append('typecheck rc=%d errors=%d' % (rc, errs))

    # 2. eslint (live) on every added, modified or renamed ts/tsx file of the recut
    rc, names, _ = git(['diff', '--name-only', '--diff-filter=AMR', BASE, BRANCH], portal)
    files = [f for f in names.splitlines() if re.search(r'\.(ts|tsx)$', f)]
    try:
        p = subprocess.run([bun_exe(), 'x', 'eslint'] + files, cwd=portal, stdout=subprocess.PIPE,
                           stderr=subprocess.STDOUT, timeout=480)
        erc, eout = p.returncode, ANSI.sub('', p.stdout.decode('utf-8', 'replace'))
    except subprocess.TimeoutExpired:
        erc, eout = 124, 'TIMEOUT'
    m = re.search(r'(\d+) errors?, (\d+) warnings?', eout)
    eerr = int(m.group(1)) if m else 0
    ewarn = int(m.group(2)) if m else 0
    record['eslint'] = {'cmd': 'bun x eslint <%d changed ts/tsx files>' % len(files), 'rc': erc,
                        'errors': eerr, 'warnings': ewarn, 'files': len(files)}
    if erc != 0 or eerr != 0:
        bad.append('eslint rc=%d errors=%d' % (erc, eerr))

    # 3. the bun test delta against origin/PROD (saved outputs, pinned by sha256)
    rt = read_test(TEST_RECUT)
    rp = read_test(TEST_PROD)
    fl_r, fl_p = Counter(rt['fail_lines']), Counter(rp['fail_lines'])
    fail_equal = fl_r == fl_p
    if not fail_equal:
        bad.append('failing test lines differ from origin/PROD: recut-only %d, prod-only %d' % (
            sum((fl_r - fl_p).values()), sum((fl_p - fl_r).values())))
    new_errs = sorted(k for k in rt['error_blocks'] if k not in rp['error_blocks'])
    gaps = {}
    with open(GATES_JSON, encoding='utf-8') as fh:
        prev = json.load(fh)
    causes = {(c['message'] + ' || ' + c['file']): c['cause'] for c in prev.get('new_load_errors', [])}
    unexplained = [k for k in new_errs if not str(causes.get(k, '')).strip()]
    if unexplained:
        bad.append('%d new load error(s) without a cause in GATES.json' % len(unexplained))
    if rt['summary']['failed'] != rp['summary']['failed'] or rt['summary']['errors'] != rp['summary']['errors']:
        bad.append('summary fail/errors differ from origin/PROD')
    # the sparse-worktree load errors that both sides carry, by class (recorded, not gated)
    for k, v in rp['error_blocks'].items():
        cls = k.split(' || ')[0][:90]
        gaps[cls] = gaps.get(cls, 0) + v
    record['tests'] = {
        'cmd': 'bun test ' + ' '.join(TEST_DIRS),
        'recut': {'file': os.path.basename(TEST_RECUT), 'sha256': rt['sha256'], **rt['summary']},
        'origin_PROD_same_worktree': {'file': os.path.basename(TEST_PROD), 'sha256': rp['sha256'], **rp['summary']},
        'failing_lines_recut': sum(fl_r.values()), 'failing_lines_prod': sum(fl_p.values()),
        'failing_lines_equal_to_prod': fail_equal,
        'load_error_blocks_recut': sum(rt['error_blocks'].values()),
        'load_error_blocks_prod': sum(rp['error_blocks'].values()),
        'new_load_errors_count': len(new_errs),
        'load_error_classes_on_both': sorted(gaps.items(), key=lambda kv: -kv[1]),
    }
    # the causes are read by hand and kept at the top level of GATES.json; a new error without one is GATES-BAD
    record['new_load_errors'] = [{'message': k.split(' || ')[0], 'file': k.split(' || ')[1],
                                  'cause': causes.get(k, '')} for k in new_errs]
    record['control'] = {}

    # 4. control: the payload check must fire on the DEV-cut branch that carries the Trade Request form
    prc = subprocess.run([sys.executable, '-I', PAYLOAD, CONTROL_BRANCH], cwd=root,
                         stdout=subprocess.PIPE, stderr=subprocess.STDOUT, timeout=480).returncode
    control_fires = (prc == 1)
    record['control'] = {'payload_check_on': CONTROL_BRANCH, 'rc': prc, 'fires': control_fires}

    with open(GATES_JSON, 'w', encoding='utf-8', newline='\n') as fh:
        json.dump(record, fh, indent=2)
        fh.write('\n')

    if control_fires:
        print('CONTROL-FIRES payload_check.py rc=%d against %s' % (prc, CONTROL_BRANCH))
    else:
        print('CONTROL-SILENT payload_check.py rc=%d against %s (expected 1)' % (prc, CONTROL_BRANCH))
        bad.append('control silent')

    if bad:
        print('GATES-BAD ' + '; '.join(bad))
        return 1
    print('GATES-OK typecheck 0 tests %d passed failing-lines-equal-PROD %d new-load-errors %d explained '
          'eslint 0 errors' % (rt['summary']['passed'], sum(fl_r.values()), len(new_errs)))
    return 0


if __name__ == '__main__':
    sys.exit(main())
