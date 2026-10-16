#!/usr/bin/env python3
"""AR-y-366 (AC3): the one mutant that must fire.

Copies the amended driver to a scratch folder OUTSIDE the product tree (a tempfile directory), changes the Replace label
constant to a misspelling ('Replce'), and runs labels_check.py's label check (rule 1 only) against the copy.
Positive control: the unmutated driver must pass the same label check first.

Prints MUTANT-FIRES only when the label check passes on the amended driver and FAILS on the mutant (exit 0);
otherwise MUTANT-SURVIVES (exit 1).
"""
import importlib.util
import os
import shutil
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
spec = importlib.util.spec_from_file_location('labels_check', os.path.join(HERE, 'labels_check.py'))
lc = importlib.util.module_from_spec(spec)
spec.loader.exec_module(lc)

ORIGINAL_LINE = "const PROMPT_REPLACE = 'Replace'"
MUTANT_LINE = "const PROMPT_REPLACE = 'Replce'"


def label_check_on(path):
    with open(path, encoding='utf-8') as fh:
        text = fh.read()
    ok, n, reasons, _details = lc.check_labels(text)
    return ok, n, reasons


def main():
    repo = lc.repo_root()
    original = os.path.join(repo, lc.DRIVER_REL)
    with open(original, encoding='utf-8') as fh:
        text = fh.read()
    if text.count(ORIGINAL_LINE) != 1:
        print('MUTANT-SURVIVES the mutation anchor occurs %d times (need 1)' % text.count(ORIGINAL_LINE))
        return 1
    scratch = tempfile.mkdtemp(prefix='ar366_mutant_')
    try:
        mutant_path = os.path.join(scratch, 'fwd1_driver_mutant.mjs')
        with open(mutant_path, 'w', encoding='utf-8', newline='\n') as fh:
            fh.write(text.replace(ORIGINAL_LINE, MUTANT_LINE, 1))
        ok_orig, n, _r0 = label_check_on(original)
        ok_mut, _n, reasons = label_check_on(mutant_path)
    finally:
        shutil.rmtree(scratch, ignore_errors=True)
    if ok_orig and not ok_mut:
        print('MUTANT-FIRES Replace label changed to Replce: label check FAILS on the copy (%s); positive control PASSES on the amended driver (%d labels)'
              % (reasons[0] if reasons else 'no reason', n))
        return 0
    print('MUTANT-SURVIVES positive control %s; mutant check %s (%d labels)'
          % ('PASS' if ok_orig else 'FAIL', 'FAIL' if not ok_mut else 'PASS', n))
    return 1


if __name__ == '__main__':
    sys.exit(main())
