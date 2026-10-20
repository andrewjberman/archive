#!/usr/bin/env python3
"""AR419-y-MUTANT -- the one mutant: the catalogue effect on form open and firm choice is restored.

TicketCenter.tsx is swapped for a copy carrying a useEffect that reads the served catalogue whenever the analysis form is open
(the AR-y-419 removed chain), the new test file is run once, and the original bytes are put back with a sha256 check. Prints
MUTANT-FIRES only when test (3) of the new file is among the failures; otherwise MUTANT-SURVIVES, exit 1.
"""
import hashlib
import os
import re
import shutil
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
WORKSPACE = subprocess.run(['git', 'rev-parse', '--show-toplevel'], cwd=HERE, capture_output=True, text=True,
                           encoding='utf-8', errors='replace', timeout=120).stdout.strip()
PORTAL = os.path.join(WORKSPACE, 'portal')
TARGET = os.path.join(PORTAL, 'src', 'pages', 'TicketCenter', 'TicketCenter.tsx')
NEW_TEST = 'src/pages/TicketCenter/__tests__/models-first-paint.test.tsx'
FROM = b'const catalogueFirm = filingForm.firm.trim()'
TO = (FROM + b'\r\n  useEffect(() => {\r\n    if (!formOpen || newType !== \'analysis_request\') return\r\n'
      b'    void fetchCatalogue(catalogueFirm || undefined)\r\n  }, [formOpen, newType, catalogueFirm])')
TEST_THREE = '(3) opening the form and choosing a firm performs ZERO catalogue requests'
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
        print('MUTANT-SURVIVES not applied: the catalogue firm line occurs %d times (need 1), sha256 %s' % (count, sha_before))
        sys.exit(1)
    mutant = original.replace(FROM, TO)
    rc = None
    text = ''
    try:
        with open(TARGET, 'wb') as fh:
            fh.write(mutant)
        proc = subprocess.run([bun_path(), 'test', NEW_TEST], cwd=PORTAL, capture_output=True, text=True,
                              encoding='utf-8', errors='replace', timeout=300)
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
    failed_three = any(line.startswith('✗') and TEST_THREE in line for line in text.splitlines())
    if rc not in (None, 0) and failed_three:
        print('MUTANT-FIRES new test file rc=%s fail=%d pass=%d of %d; test (3) fails on the catalogue read at form open; restored sha256 %s'
              % (rc, n_fail, n_pass, n_fail + n_pass, sha_after))
        sys.exit(0)
    print('MUTANT-SURVIVES new test file rc=%s fail=%d pass=%d; test (3) failed=%s; restored sha256 %s'
          % (rc, n_fail, n_pass, failed_three, sha_after))
    sys.exit(1)


if __name__ == '__main__':
    main()
