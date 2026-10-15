#!/usr/bin/env python3
"""AR361-y-AC2: the candidate composer with the as-of put back to null (a mutant) must FAIL the new test file.

The candidate composer is copied to a scratch folder OUTSIDE the product tree (<worktree>/.scratch/asof_mutant/).
The mutant is written there, copied over the composer for one bun run, and the candidate is copied back with its
sha256 verified. Prints MUTANT-FIRES only when that run FAILS; otherwise MUTANT-SURVIVES and exit 1.
"""
import hashlib
import os
import re
import shutil
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
WT = subprocess.run(['git', 'rev-parse', '--show-toplevel'], cwd=HERE, capture_output=True, text=True, check=True).stdout.strip()
PORTAL = os.path.join(WT, 'portal')
COMPOSER = os.path.join(PORTAL, 'src/pages/InvestorReporting/tabs/analysis/ProspectComposer.tsx')
NEW = 'src/pages/InvestorReporting/tabs/analysis/tests/prospect-no-price-date.test.tsx'
SCRATCH = os.path.join(WT, '.scratch', 'asof_mutant')
ANSI = re.compile(r'\x1b\[[0-9;]*m')
OLD = '      asOf: PROSPECT_AS_OF,\n'
PUT_BACK = '      asOf: null,\n'


def sha256(path):
    with open(path, 'rb') as handle:
        return hashlib.sha256(handle.read()).hexdigest()


def main():
    bun = shutil.which('bun')
    if bun is None:
        print('MUTANT-SURVIVES (bun is not on PATH; no run made)')
        return 1
    os.makedirs(SCRATCH, exist_ok=True)
    candidate_copy = os.path.join(SCRATCH, 'ProspectComposer.candidate.tsx')
    mutant_copy = os.path.join(SCRATCH, 'ProspectComposer.mutant.tsx')
    shutil.copyfile(COMPOSER, candidate_copy)
    with open(candidate_copy, encoding='utf-8', newline='') as handle:
        text = handle.read()
    # A Windows checkout (core.autocrlf) holds CRLF bytes; the anchor is matched in the file's own line ending.
    eol = '\r\n' if '\r\n' in text else '\n'
    old, put_back = OLD.replace('\n', eol), PUT_BACK.replace('\n', eol)
    count = text.count(old)
    if count != 1:
        print('MUTANT-SURVIVES (mutant not built: the as-of anchor was found %d times)' % count)
        return 1
    with open(mutant_copy, 'w', encoding='utf-8', newline='') as handle:
        handle.write(text.replace(old, put_back))
    candidate_sha = sha256(candidate_copy)
    if candidate_sha == sha256(mutant_copy):
        print('MUTANT-SURVIVES (mutant identical to candidate)')
        return 1
    rc = None
    out = ''
    try:
        shutil.copyfile(mutant_copy, COMPOSER)
        proc = subprocess.run([bun, 'test', NEW], cwd=PORTAL, capture_output=True, text=True,
                              encoding='utf-8', errors='replace', timeout=110)
        rc = proc.returncode
        out = ANSI.sub('', proc.stdout + proc.stderr)
    finally:
        shutil.copyfile(candidate_copy, COMPOSER)
        restored = sha256(COMPOSER) == candidate_sha
    if not restored:
        print('MUTANT-SURVIVES (candidate NOT restored: sha mismatch; stop and report)')
        return 1
    fails = re.findall(r'^\s*(\d+) fail\s*$', out, re.M)
    g_lines = [line.strip() for line in out.splitlines() if '(g) the header card' in line]
    if rc != 0:
        print('MUTANT-FIRES (bun test rc=%s on the mutant, %s fail; candidate restored, sha256 verified)'
              % (rc, fails[-1] if fails else 'unknown'))
        for line in g_lines:
            print('  failing line: ' + line.encode('ascii', 'replace').decode('ascii'))
        return 0
    print('MUTANT-SURVIVES (bun test rc=0 on the mutant)')
    return 1


if __name__ == '__main__':
    sys.exit(main())
