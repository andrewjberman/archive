"""AR364-y-AC2: the one mutant. The hint gate is put back to proxyableFindings (the AR-y-363 text, the candidate a168015b),
swapped into the portal file for ONE bun run of the new test file, and restored with a sha256 check.

Prints MUTANT-FIRES only when that run FAILS; otherwise MUTANT-SURVIVES, exit 1.
"""
import hashlib
import re
import shutil
import subprocess
import sys

PORTAL = 'C:/dev/wk-irpt-anlreq-161/portal'
TARGET = 'src/pages/TicketCenter/analysisRequest.ts'
NEW_FILE = 'src/pages/TicketCenter/__tests__/filing-tree-gate.test.tsx'
BASE = 'a168015b'
NEW_CASES = 6
ANSI = re.compile(r'\x1b\[[0-9;]*[A-Za-z]')


def sha(b):
    return hashlib.sha256(b).hexdigest()


def git_show_base():
    r = subprocess.run(['git', '-C', PORTAL, 'show', BASE + ':' + TARGET], capture_output=True, timeout=60)
    if r.returncode != 0:
        raise SystemExit('MUTANT-SURVIVES git show base failed rc=%d' % r.returncode)
    return r.stdout


def main():
    path = PORTAL + '/' + TARGET
    with open(path, 'rb') as fh:
        orig = fh.read()
    sha0 = sha(orig)
    mutant = git_show_base()
    # positive control: the mutant really is the proxyableFindings gate, and it differs from the working file
    if b'proxyableFindings(findings)' not in mutant or mutant == orig:
        print('MUTANT-SURVIVES positive control failed: the swapped text is not the proxyableFindings gate')
        return 1
    bun = shutil.which('bun')
    if bun is None:
        print('MUTANT-SURVIVES bun not on PATH')
        return 1
    try:
        with open(path, 'wb') as fh:
            fh.write(mutant)
        try:
            r = subprocess.run([bun, 'test', NEW_FILE], cwd=PORTAL, capture_output=True, timeout=120)
            rc = r.returncode
            text = ANSI.sub('', (r.stdout + r.stderr).decode('utf-8', 'replace'))
        except subprocess.TimeoutExpired:
            rc, text = 124, ''
    finally:
        with open(path, 'wb') as fh:
            fh.write(orig)
    with open(path, 'rb') as fh:
        restored = sha(fh.read())
    if restored != sha0:
        print('MUTANT-RESTORE-FAILED sha256 %s != %s' % (restored, sha0))
        return 2
    fails = re.findall(r'^\s*(\d+) fail\s*$', text, re.M)
    n_fail = int(fails[-1]) if fails else -1
    failed_lines = [ln for ln in text.splitlines() if '\u2717' in ln]
    labels = sorted(set(re.findall(r'>\s*\((\w)\)', ''.join(failed_lines))))
    if rc != 0 and n_fail >= 1:
        print('MUTANT-FIRES %d of %d cases fail under the proxyableFindings gate (rc=%d; failing: %s); portal file restored, sha256 %s'
              % (n_fail, NEW_CASES, rc, ','.join(labels) or 'see run', restored[:12]))
        return 0
    print('MUTANT-SURVIVES rc=%d fail=%d (rc=124 is a timeout); portal file restored, sha256 %s' % (rc, n_fail, restored[:12]))
    return 1


if __name__ == '__main__':
    sys.exit(main())
