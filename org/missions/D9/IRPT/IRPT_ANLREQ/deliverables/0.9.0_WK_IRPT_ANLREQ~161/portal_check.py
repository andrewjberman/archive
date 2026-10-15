"""AR364-y-AC1: run bun test on the new gate test file and on the TicketCenter folder, in the portal worktree.

Prints PORTAL-TESTS-OK <new passed> new, <folder passed> folder, 0 failed only when the new file passes all its cases
(a) to (f) and the folder has 0 failed; otherwise PORTAL-TESTS-BAD <why>, exit 1.
"""
import re
import shutil
import subprocess
import sys

PORTAL = 'C:/dev/wk-irpt-anlreq-161/portal'
NEW_FILE = 'src/pages/TicketCenter/__tests__/filing-tree-gate.test.tsx'
FOLDER = 'src/pages/TicketCenter'
NEW_CASES = 6
ANSI = re.compile(r'\x1b\[[0-9;]*[A-Za-z]')


def bun_test(target):
    bun = shutil.which('bun')
    if bun is None:
        return None, 'bun not on PATH'
    try:
        r = subprocess.run([bun, 'test', target], cwd=PORTAL, capture_output=True, timeout=120)
    except subprocess.TimeoutExpired:
        return None, 'bun test timed out (120 s) on ' + target
    text = ANSI.sub('', (r.stdout + r.stderr).decode('utf-8', 'replace'))
    p = re.findall(r'^\s*(\d+) pass\s*$', text, re.M)
    f = re.findall(r'^\s*(\d+) fail\s*$', text, re.M)
    if not p or not f:
        return None, 'no pass/fail summary on ' + target + ' (rc=' + str(r.returncode) + ')'
    return {'rc': r.returncode, 'pass': int(p[-1]), 'fail': int(f[-1])}, None


def main():
    new, why = bun_test(NEW_FILE)
    if why:
        print('PORTAL-TESTS-BAD ' + why)
        return 1
    if new['rc'] != 0 or new['fail'] != 0 or new['pass'] != NEW_CASES:
        print('PORTAL-TESTS-BAD new file: rc=%d pass=%d fail=%d (need pass=%d fail=0 rc=0)'
              % (new['rc'], new['pass'], new['fail'], NEW_CASES))
        return 1
    folder, why = bun_test(FOLDER)
    if why:
        print('PORTAL-TESTS-BAD ' + why)
        return 1
    if folder['rc'] != 0 or folder['fail'] != 0:
        print('PORTAL-TESTS-BAD folder: rc=%d fail=%d' % (folder['rc'], folder['fail']))
        return 1
    print('PORTAL-TESTS-OK %d new, %d folder, 0 failed' % (new['pass'], folder['pass']))
    return 0


if __name__ == '__main__':
    sys.exit(main())
