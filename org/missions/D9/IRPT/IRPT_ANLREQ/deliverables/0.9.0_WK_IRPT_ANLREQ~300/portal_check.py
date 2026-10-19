#!/usr/bin/env python3
"""AR410-y-AC1 -- bun test on the new test file, and on the folder src/pages/TicketCenter, in the portal worktree.

Prints PORTAL-TESTS-OK <new passed> new, <folder passed> folder, 0 failed only when the new file has exactly the
EXPECTED_NEW cases and all pass, and the folder has no failure; otherwise PORTAL-TESTS-BAD <why>, exit 1.
The worktree is derived from this file's location (seven levels up), never hardcoded.
"""
import os
import re
import shutil
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
WT = os.path.abspath(os.path.join(HERE, *([os.pardir] * 7)))
PORTAL = os.path.join(WT, 'portal')
NEW_TEST = 'src/pages/TicketCenter/__tests__/upload-resolving-backoff.test.tsx'
FOLDER = 'src/pages/TicketCenter'
EXPECTED_NEW = 7
ANSI = re.compile(r'\x1b\[[0-9;]*m')


def bun_path():
    found = shutil.which('bun')
    if found:
        return found
    return 'bun'


def run_bun(target):
    try:
        proc = subprocess.run([bun_path(), 'test', target], cwd=PORTAL, capture_output=True, text=True, timeout=300)
    except subprocess.TimeoutExpired:
        return None, None, None
    text = ANSI.sub('', (proc.stdout or '') + (proc.stderr or ''))
    passes = re.findall(r'^\s*(\d+) pass\s*$', text, re.MULTILINE)
    fails = re.findall(r'^\s*(\d+) fail\s*$', text, re.MULTILINE)
    if not passes or not fails:
        return proc.returncode, None, None
    return proc.returncode, int(passes[-1]), int(fails[-1])


def bad(why):
    print('PORTAL-TESTS-BAD ' + why)
    sys.exit(1)


def main():
    if not os.path.isfile(os.path.join(PORTAL, NEW_TEST)):
        bad('new test file absent in ' + PORTAL)
    rc_new, new_pass, new_fail = run_bun(NEW_TEST)
    if rc_new is None:
        bad('bun test timed out on the new file')
    if new_pass is None:
        bad('no pass/fail summary for the new file, rc=%s' % rc_new)
    if rc_new != 0 or new_fail != 0:
        bad('new file: rc=%s, %s fail' % (rc_new, new_fail))
    if new_pass != EXPECTED_NEW:
        bad('new file: %s pass, expected %s cases' % (new_pass, EXPECTED_NEW))
    rc_f, f_pass, f_fail = run_bun(FOLDER)
    if rc_f is None:
        bad('bun test timed out on the folder')
    if f_pass is None:
        bad('no pass/fail summary for the folder, rc=%s' % rc_f)
    if rc_f != 0 or f_fail != 0:
        bad('folder: rc=%s, %s fail' % (rc_f, f_fail))
    print('PORTAL-TESTS-OK %d new, %d folder, 0 failed' % (new_pass, f_pass))
    sys.exit(0)


if __name__ == '__main__':
    main()
