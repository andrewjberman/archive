#!/usr/bin/env python3
"""AR361-y-AC1: both test files report 0 fail, and the new file runs its 7 cases (a) to (g).

Runs `bun test` on the new test file and on the s55 component-wiring file, in <worktree>/portal.
Prints `ASOF-TESTS-OK <n> passed, 0 failed` only when both files report 0 fail and the new file runs
exactly the cases (a) to (g); otherwise `ASOF-TESTS-BAD <why>` and exit 1.
"""
import os
import re
import shutil
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
WT = subprocess.run(['git', 'rev-parse', '--show-toplevel'], cwd=HERE, capture_output=True, text=True, check=True).stdout.strip()
PORTAL = os.path.join(WT, 'portal')
NEW = 'src/pages/InvestorReporting/tabs/analysis/tests/prospect-no-price-date.test.tsx'
S55 = 'src/pages/InvestorReporting/__tests__/dsgn-irptv1/s55.component-wiring.test.tsx'
CASES = list('abcdefg')
ANSI = re.compile(r'\x1b\[[0-9;]*m')


def bad(why):
    print('ASOF-TESTS-BAD ' + why)
    return 1


def run_file(bun, rel):
    proc = subprocess.run([bun, 'test', rel], cwd=PORTAL, capture_output=True, text=True,
                          encoding='utf-8', errors='replace', timeout=110)
    out = ANSI.sub('', proc.stdout + proc.stderr)
    passes = re.findall(r'^\s*(\d+) pass\s*$', out, re.M)
    fails = re.findall(r'^\s*(\d+) fail\s*$', out, re.M)
    ran = re.findall(r'Ran (\d+) tests? across', out)
    return proc.returncode, passes, fails, ran


def main():
    bun = shutil.which('bun')
    if bun is None:
        return bad('bun is not on PATH')
    for rel in (NEW, S55):
        if not os.path.isfile(os.path.join(PORTAL, rel)):
            return bad('test file absent: ' + rel)
    with open(os.path.join(PORTAL, NEW), encoding='utf-8') as handle:
        names = re.findall(r"^\s*test\('\((\w)\) ", handle.read(), re.M)
    if names != CASES:
        return bad('the new file declares cases %s, not (a) to (g)' % ''.join(names))
    total = 0
    for rel in (NEW, S55):
        rc, passes, fails, ran = run_file(bun, rel)
        if not passes or not fails:
            return bad('no pass/fail summary from bun for ' + rel + ' (rc=%s)' % rc)
        n_pass, n_fail = int(passes[-1]), int(fails[-1])
        if n_fail != 0 or rc != 0:
            return bad('%s reports %d fail (rc=%s)' % (rel, n_fail, rc))
        if rel == NEW and (not ran or int(ran[-1]) != len(CASES) or n_pass != len(CASES)):
            return bad('the new file ran %s cases with %d pass, not 7' % (ran[-1] if ran else '?', n_pass))
        total += n_pass
    print('ASOF-TESTS-OK %d passed, 0 failed' % total)
    return 0


if __name__ == '__main__':
    sys.exit(main())
