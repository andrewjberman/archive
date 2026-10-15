#!/usr/bin/env python3
"""AR360-y-AC2: the candidate composer with the price-date input put back (a mutant) must FAIL the new test file.

The mutant is written to a scratch folder OUTSIDE the product tree (<worktree>/.scratch/ar360_mutant/). The candidate
composer is copied there first, the mutant is copied over it for one bun run, and the candidate is copied back with
its sha256 verified. Prints MUTANT-FIRES only when that run FAILS; otherwise MUTANT-SURVIVES and exit 1.
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
SCRATCH = os.path.join(WT, '.scratch', 'ar360_mutant')
ANSI = re.compile(r'\x1b\[[0-9;]*m')

# (candidate text, put-back text): the three PROD sites the cell removed, restored verbatim from origin/PROD.
PUT_BACK = [
    ("  const [usd, setUsd] = useState(false)\n",
     "  const [usd, setUsd] = useState(false)\n  const [priceDate, setPriceDate] = useState('')\n"),
    ("      asOf: null,\n", "      asOf: priceDate || null,\n"),
    ("}, [onProspectReviewed, reviewed, title, preparedFor, file?.name])",
     "}, [onProspectReviewed, reviewed, title, preparedFor, priceDate, file?.name])"),
    ("{ declaredCurrency: usd, priceDate: '', referenceNotional: notional }",
     "{ declaredCurrency: usd, priceDate, referenceNotional: notional }"),
    ('          <p data-slot="prospect-price-basis" className="text-sm">Prices are the T-1 close.</p>',
     '          <label className="text-sm">Price date for share quantities\n'
     '            <input className="block rounded border p-1" type="date" value={priceDate}\n'
     '              onChange={(event) => { setPriceDate(event.target.value); changed() }} />\n'
     '          </label>'),
]


def sha256(path):
    with open(path, 'rb') as handle:
        return hashlib.sha256(handle.read()).hexdigest()


def make_mutant(text):
    for old, new in PUT_BACK:
        count = text.count(old)
        if count != 1:
            raise SystemExit('MUTANT-SURVIVES (mutant not built: anchor found %d times: %r)' % (count, old[:60]))
        text = text.replace(old, new)
    return text


def main():
    os.makedirs(SCRATCH, exist_ok=True)
    candidate_copy = os.path.join(SCRATCH, 'ProspectComposer.candidate.tsx')
    mutant_copy = os.path.join(SCRATCH, 'ProspectComposer.mutant.tsx')
    shutil.copyfile(COMPOSER, candidate_copy)
    with open(candidate_copy, encoding='utf-8') as handle:
        mutant_text = make_mutant(handle.read())
    with open(mutant_copy, 'w', encoding='utf-8', newline='') as handle:
        handle.write(mutant_text)
    candidate_sha = sha256(candidate_copy)
    mutant_sha = sha256(mutant_copy)
    if candidate_sha == mutant_sha:
        print('MUTANT-SURVIVES (mutant identical to candidate)')
        return 1
    rc = None
    try:
        shutil.copyfile(mutant_copy, COMPOSER)
        proc = subprocess.run(['bun', 'test', NEW], cwd=PORTAL, capture_output=True, text=True,
                              encoding='utf-8', errors='replace')
        rc = proc.returncode
        out = ANSI.sub('', proc.stdout + proc.stderr)
        failed = re.findall(r'^\s*(\d+) fail\s*$', out, re.M)
        n_fail = failed[-1] if failed else 'unknown'
    finally:
        shutil.copyfile(candidate_copy, COMPOSER)
        restored = sha256(COMPOSER) == candidate_sha
    if not restored:
        print('MUTANT-SURVIVES (candidate NOT restored: sha mismatch; stop and report)')
        return 1
    if rc != 0:
        print('MUTANT-FIRES (bun test rc=%s, %s failing on the mutant; candidate restored sha256 verified)' % (rc, n_fail))
        return 0
    print('MUTANT-SURVIVES (bun test rc=0 on the mutant)')
    return 1


if __name__ == '__main__':
    sys.exit(main())
