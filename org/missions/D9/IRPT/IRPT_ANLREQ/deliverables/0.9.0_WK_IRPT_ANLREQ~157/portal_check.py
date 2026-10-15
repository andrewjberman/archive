#!/usr/bin/env python3
"""AR360-y-AC1: run bun test on the new composer test file and on the three folders named by the cell.

Prints PORTAL-TESTS-OK <new passed> new, <folders passed> folders, 0 failed  only when the new file has every case
(a) to (f) passing and the folders have 0 failed; otherwise PORTAL-TESTS-BAD <why> and exit 1.
"""
import os
import re
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
WT = subprocess.run(['git', 'rev-parse', '--show-toplevel'], cwd=HERE, capture_output=True, text=True, check=True).stdout.strip()
PORTAL = os.path.join(WT, 'portal')
NEW = 'src/pages/InvestorReporting/tabs/analysis/tests/prospect-no-price-date.test.tsx'
FOLDERS = [
    'src/pages/InvestorReporting/tabs/analysis/tests',
    'src/pages/TicketCenter',
    'src/pages/InvestorReporting/__tests__/dsgn-irptv1',
]
NEW_CASES = 6
ANSI = re.compile(r'\x1b\[[0-9;]*m')


def run_bun(paths):
    proc = subprocess.run(['bun', 'test'] + paths, cwd=PORTAL, capture_output=True, text=True,
                          encoding='utf-8', errors='replace')
    out = ANSI.sub('', proc.stdout + proc.stderr)
    passed = re.findall(r'^\s*(\d+) pass\s*$', out, re.M)
    failed = re.findall(r'^\s*(\d+) fail\s*$', out, re.M)
    ran = re.findall(r'^Ran (\d+) tests? across (\d+) files?', out, re.M)
    if not passed or not failed or not ran:
        return proc.returncode, None, None, None, out
    return proc.returncode, int(passed[-1]), int(failed[-1]), ran[-1], out


def main():
    if not os.path.isfile(os.path.join(PORTAL, NEW)):
        print('PORTAL-TESTS-BAD new test file absent: ' + NEW)
        return 1
    rc, n_pass, n_fail, ran, _ = run_bun([NEW])
    if n_pass is None:
        print('PORTAL-TESTS-BAD new file: no bun summary (rc=%s)' % rc)
        return 1
    if rc != 0 or n_fail != 0 or n_pass != NEW_CASES or int(ran[0]) != NEW_CASES:
        print('PORTAL-TESTS-BAD new file: rc=%s pass=%s fail=%s ran=%s (need %d pass, 0 fail)'
              % (rc, n_pass, n_fail, ran, NEW_CASES))
        return 1
    rc2, f_pass, f_fail, f_ran, out = run_bun(FOLDERS)
    if f_pass is None:
        print('PORTAL-TESTS-BAD folders: no bun summary (rc=%s)' % rc2)
        return 1
    if rc2 != 0 or f_fail != 0:
        failing = [line for line in out.splitlines() if line.startswith('(fail)') or line.startswith('error:')][:5]
        print('PORTAL-TESTS-BAD folders: rc=%s fail=%s %s' % (rc2, f_fail, ' | '.join(failing)))
        return 1
    print('PORTAL-TESTS-OK %d new, %d folders, 0 failed' % (n_pass, f_pass))
    return 0


if __name__ == '__main__':
    sys.exit(main())
