#!/usr/bin/env python3
"""AR410-y-AC2 -- the one mutant: the wait loop in analysisRequest.ts stops after four waits.

The changed file is swapped for the mutant, one bun run of the new test file is made, and the original bytes are put back
with a sha256 check. Prints MUTANT-FIRES only when that run FAILS; otherwise MUTANT-SURVIVES, exit 1.
"""
import hashlib
import os
import re
import shutil
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
WT = os.path.abspath(os.path.join(HERE, *([os.pardir] * 7)))
PORTAL = os.path.join(WT, 'portal')
TARGET = os.path.join(PORTAL, 'src', 'pages', 'TicketCenter', 'analysisRequest.ts')
NEW_TEST = 'src/pages/TicketCenter/__tests__/upload-resolving-backoff.test.tsx'
# the loop condition, as shipped: re-post while RESOLVING and the total wait is not yet reached
FROM = b'resolving(result) && waitedMs < UPLOAD_MAX_TOTAL_WAIT_MS;'
# the mutant: re-post while RESOLVING and fewer than four waits have been made
TO = b'resolving(result) && attempt <= 4;'
ANSI = re.compile(r'\x1b\[[0-9;]*m')


def sha256(data):
    return hashlib.sha256(data).hexdigest()


def bun_path():
    found = shutil.which('bun')
    return found if found else 'bun'


def main():
    with open(TARGET, 'rb') as fh:
        original = fh.read()
    sha_before = sha256(original)
    count = original.count(FROM)
    if count != 1:
        print('MUTANT-SURVIVES not applied: the loop condition occurs %d times (need 1), sha256 %s' % (count, sha_before))
        sys.exit(1)
    mutant = original.replace(FROM, TO)
    rc = None
    text = ''
    try:
        with open(TARGET, 'wb') as fh:
            fh.write(mutant)
        proc = subprocess.run([bun_path(), 'test', NEW_TEST], cwd=PORTAL, capture_output=True, text=True, timeout=300)
        rc = proc.returncode
        text = ANSI.sub('', (proc.stdout or '') + (proc.stderr or ''))
    finally:
        with open(TARGET, 'wb') as fh:
            fh.write(original)
    with open(TARGET, 'rb') as fh:
        sha_after = sha256(fh.read())
    if sha_after != sha_before:
        print('MUTANT-SURVIVES restore failed: sha256 %s before, %s after' % (sha_before, sha_after))
        sys.exit(1)
    fails = re.findall(r'^\s*(\d+) fail\s*$', text, re.MULTILINE)
    passes = re.findall(r'^\s*(\d+) pass\s*$', text, re.MULTILINE)
    n_fail = int(fails[-1]) if fails else 0
    n_pass = int(passes[-1]) if passes else 0
    total = n_fail + n_pass
    if rc is not None and rc != 0 and n_fail > 0:
        print('MUTANT-FIRES new test file rc=%s fail=%d of %d on the four-wait mutant; restored sha256 %s'
              % (rc, n_fail, total, sha_after))
        sys.exit(0)
    print('MUTANT-SURVIVES new test file rc=%s fail=%d of %d on the four-wait mutant; restored sha256 %s'
          % (rc, n_fail, total, sha_after))
    sys.exit(1)


if __name__ == '__main__':
    main()
