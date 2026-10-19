#!/usr/bin/env python3
"""AR411-y-AC2 -- gates check of the prod-based recut (TO-AR-y-411, step 4).

Reads r58/GATES.json, re-runs the new test file in the portal worktree of this checkout (found from this file's own
location) and runs the control: origin/PROD's analysisRequest.ts is swapped in for the backoff file, the new test run
must FAIL (CONTROL-FIRES), and the backoff file is restored with a sha256 check.
Prints GATES-OK typecheck 0 eslint 0 new-tests <n> passed failing-lines-equal-PROD <k> new-load-errors <e> explained
only when typecheck and eslint hold, the new cases pass, the failing test lines equal origin/PROD's, every new load
error is explained in GATES.json and the control fires; otherwise GATES-BAD <why>, exit 1.
"""
import hashlib
import json
import os
import re
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
NEW_TEST = 'src/pages/TicketCenter/__tests__/upload-resolving-backoff.test.tsx'
TARGET = 'src/pages/TicketCenter/analysisRequest.ts'
ANSI = re.compile(r'\x1b\[[0-9;]*m')


def bad(why):
    print('GATES-BAD ' + why)
    sys.exit(1)


def git_bytes(portal, args):
    proc = subprocess.run(['git', '-C', portal] + args, capture_output=True)
    if proc.returncode != 0:
        bad('git %s rc=%d' % (' '.join(args), proc.returncode))
    return proc.stdout


def sha256(data):
    return hashlib.sha256(data).hexdigest()


def run_new_tests(portal):
    proc = subprocess.run(['bun', 'test', NEW_TEST], cwd=portal, capture_output=True, text=True, encoding='utf-8',
                          errors='replace', timeout=300)
    text = ANSI.sub('', (proc.stdout or '') + (proc.stderr or ''))
    passed = re.findall(r'^\s*(\d+) pass\s*$', text, re.MULTILINE)
    failed = re.findall(r'^\s*(\d+) fail\s*$', text, re.MULTILINE)
    return proc.returncode, (int(passed[-1]) if passed else None), (int(failed[-1]) if failed else None)


def main():
    with open(os.path.join(HERE, 'GATES.json'), 'r', encoding='utf-8') as fh:
        gates = json.load(fh)
    top = subprocess.run(['git', '-C', HERE, 'rev-parse', '--show-toplevel'], capture_output=True, text=True).stdout.strip()
    if not top:
        bad('cannot find the workspace worktree from this file')
    portal = os.path.join(top, 'portal')

    head = git_bytes(portal, ['rev-parse', 'HEAD']).decode('ascii').strip()
    if head != gates.get('head'):
        bad('portal HEAD %s is not the recorded head %s' % (head, gates.get('head')))

    if gates['typecheck']['rc'] != 0 or gates['typecheck']['ts_error_lines'] != 0:
        bad('typecheck not clean in GATES.json')
    if gates['eslint']['rc'] != 0 or gates['eslint']['errors'] != 0:
        bad('eslint not clean in GATES.json')

    tests = gates['tests']
    recut_fail = tests['recut']['failing_lines']
    prod_fail = tests['prod']['failing_lines']
    if sorted(recut_fail) != sorted(prod_fail):
        bad('failing test lines at the recut (%d) differ from origin/PROD (%d)' % (len(recut_fail), len(prod_fail)))

    new_load = gates.get('new_load_errors', 0)
    explained = gates.get('load_errors_explained', [])
    if new_load != len(explained):
        bad('new load errors %d, explained %d' % (new_load, len(explained)))

    # the new cases pass, re-run now on the recut
    rc, npass, nfail = run_new_tests(portal)
    want = gates['new_tests']['cases']
    if npass is None or nfail is None:
        bad('no pass/fail summary from the new test run rc=%d' % rc)
    if nfail != 0 or npass != want or rc != 0:
        bad('new test run rc=%d pass=%d fail=%d, expected %d pass 0 fail' % (rc, npass, nfail, want))

    # the control: origin/PROD's analysisRequest.ts swapped in must make the new test run FAIL
    target = os.path.join(portal, *TARGET.split('/'))
    with open(target, 'rb') as fh:
        original = fh.read()
    sha_before = sha256(original)
    prod_version = git_bytes(portal, ['show', 'origin/PROD:' + TARGET])
    if sha256(prod_version) == sha_before:
        bad('control invalid: origin/PROD version equals the backoff file')
    crc = cpass = cfail = None
    try:
        with open(target, 'wb') as fh:
            fh.write(prod_version)
        crc, cpass, cfail = run_new_tests(portal)
    finally:
        with open(target, 'wb') as fh:
            fh.write(original)
    with open(target, 'rb') as fh:
        sha_after = sha256(fh.read())
    if sha_after != sha_before:
        bad('restore failed: sha256 %s before, %s after' % (sha_before, sha_after))
    if crc == 0:
        bad('CONTROL-SURVIVES: the new test run passed with origin/PROD analysisRequest.ts (rc=0)')
    print('CONTROL-FIRES origin/PROD analysisRequest.ts swapped in: rc=%s pass=%s fail=%s; restored, sha256 %s'
          % (crc, cpass, cfail, sha_after))

    print('GATES-OK typecheck 0 eslint 0 new-tests %d passed failing-lines-equal-PROD %d new-load-errors %d explained'
          % (npass, len(prod_fail), new_load))
    return 0


if __name__ == '__main__':
    sys.exit(main())
