#!/usr/bin/env python3
# Gates check, TO IRPT_ANLREQ.TO-AR-y-385 (criterion AR385-y-AC2). ASCII only.
# Runs the step-5 gates on cand/dell2/anlreq-prod-recut in the portal worktree:
#   typecheck (bun run typecheck), bun test on the two named folders, eslint on every
#   changed or added .ts/.tsx file. Records rc and counts in r46/GATES.json.
# Prints GATES-OK typecheck 0 tests <n> passed 0 failed eslint 0 errors only when all
# three hold; otherwise GATES-BAD <why> and exit 1.
# Control: runs payload_check.py against cand/dell2/anlreq-report-ref-revision-string
# (a DEV-cut branch carrying the Trade Request form) and prints CONTROL-FIRES when it exits 1.
import json
import os
import re
import shutil
import subprocess
import sys
import time

BASE = 'origin/PROD'
BRANCH = 'cand/dell2/anlreq-prod-recut'
CONTROL_BRANCH = 'cand/dell2/anlreq-report-ref-revision-string'
TEST_DIRS = ['src/pages/TicketCenter', 'src/pages/InvestorReporting']
HERE = os.path.dirname(os.path.abspath(__file__))
R46 = os.path.join(HERE, 'r46')
PAYLOAD = os.path.join(R46, 'payload_check.py')
ANSI = re.compile(r'\x1b\[[0-9;]*m')


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


def main():
    root = git(['rev-parse', '--show-toplevel'], HERE)[1].strip()
    portal = os.path.join(root, 'portal')
    rc, head, _ = git(['rev-parse', BRANCH], portal)
    rc2, cur, _ = git(['rev-parse', '--abbrev-ref', 'HEAD'], portal)
    head = head.strip()
    if rc != 0 or cur.strip() != BRANCH:
        print('GATES-BAD portal worktree is not on %s (on %s)' % (BRANCH, cur.strip()))
        return 1

    record = {'branch': BRANCH, 'head': head, 'base': BASE}
    bad = []

    # 1. typecheck
    rc, out, dur = run_bun(['run', 'typecheck'], portal, 480)
    errs = len(re.findall(r'error TS\d+', out))
    record['typecheck'] = {'cmd': 'bun run typecheck', 'rc': rc, 'error_TS_lines': errs, 'seconds': dur}
    if rc != 0 or errs != 0:
        bad.append('typecheck rc=%d errors=%d' % (rc, errs))

    # 2. bun test on the two folders
    rc, out, dur = run_bun(['test'] + TEST_DIRS, portal, 480)
    summary = {}
    for m in re.finditer(r'^\s*(\d+) (pass|skip|fail|todo|errors?)\s*$', out, re.M):
        summary[m.group(2)] = int(m.group(1))
    ran = re.search(r'Ran (\d+) tests across (\d+) files', out)
    passed = summary.get('pass', 0)
    failed = summary.get('fail', 0)
    errors = summary.get('error', 0) + summary.get('errors', 0)
    record['tests'] = {
        'cmd': 'bun test ' + ' '.join(TEST_DIRS), 'rc': rc, 'passed': passed, 'failed': failed,
        'skipped': summary.get('skip', 0), 'errors': errors,
        'ran': int(ran.group(1)) if ran else None, 'files': int(ran.group(2)) if ran else None,
        'seconds': dur,
    }
    if rc != 0 or failed != 0 or errors != 0 or not ran:
        bad.append('tests rc=%d failed=%d errors=%d' % (rc, failed, errors))

    # 3. eslint on changed or added ts/tsx files
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

    # control: the payload check must fire on the DEV-cut branch that carries the Trade Request form
    prc = subprocess.run([sys.executable, '-I', PAYLOAD, CONTROL_BRANCH], cwd=root,
                         stdout=subprocess.PIPE, stderr=subprocess.STDOUT, timeout=480).returncode
    control_fires = (prc == 1)
    record['control'] = {'payload_check_on': CONTROL_BRANCH, 'rc': prc, 'fires': control_fires}

    with open(os.path.join(R46, 'GATES.json'), 'w', encoding='utf-8', newline='\n') as fh:
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
    print('GATES-OK typecheck 0 tests %d passed 0 failed eslint 0 errors' % passed)
    return 0


if __name__ == '__main__':
    sys.exit(main())
