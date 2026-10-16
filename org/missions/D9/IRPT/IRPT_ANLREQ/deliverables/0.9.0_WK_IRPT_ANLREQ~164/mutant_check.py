#!/usr/bin/env python3
"""AR-y-367 (AC3): the one mutant that must fire.

Copies the amended driver to a scratch folder OUTSIDE the product tree (a system tempfile directory), MOVES one decision press
(the planned-button press line of the after-Submit helper) to just before the `await submit.click()` line of run(), and runs
labels_check.py's source-order check (rule (b)) against the copy. Positive control: the unmutated driver must pass the same
source-order check first.

Prints MUTANT-FIRES only when the source-order check passes on the amended driver and FAILS on the mutant (exit 0);
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

PRESS_STMT = "await item.getByRole('button', { name: plan.button, exact: true }).click()"
SUBMIT_LINE = '    await submit.click()'


def main():
    repo = lc.repo_root()
    original = os.path.join(repo, lc.DRIVER_REL)
    with open(original, encoding='utf-8') as fh:
        text = fh.read()
    lines = text.split('\n')
    press_at = [i for i, ln in enumerate(lines) if ln.strip() == PRESS_STMT]
    submit_at = [i for i, ln in enumerate(lines) if ln == SUBMIT_LINE]
    if len(press_at) != 1 or len(submit_at) != 1:
        print('MUTANT-SURVIVES mutation anchors: press line occurs %d times, submit line %d times (need 1 and 1)'
              % (len(press_at), len(submit_at)))
        return 1
    # positive control: the amended driver passes the source-order check
    reasons_orig = lc.check_order(lines)[0]
    ok_orig = not reasons_orig
    mutant = list(lines)
    moved = mutant.pop(press_at[0])
    sub = mutant.index(SUBMIT_LINE)
    mutant.insert(sub, '    ' + moved.strip())
    scratch = tempfile.mkdtemp(prefix='ar367_mutant_')
    try:
        mutant_path = os.path.join(scratch, 'fwd1_driver_mutant.mjs')
        with open(mutant_path, 'w', encoding='utf-8', newline='\n') as fh:
            fh.write('\n'.join(mutant))
        with open(mutant_path, encoding='utf-8') as fh:
            mut_lines = fh.read().split('\n')
        reasons_mut = lc.check_order(mut_lines)[0]
    finally:
        shutil.rmtree(scratch, ignore_errors=True)
    if ok_orig and reasons_mut:
        print('MUTANT-FIRES one planned press moved before the submit.click() line: the source-order check FAILS on the copy '
              '(%s); positive control PASSES on the amended driver' % reasons_mut[0])
        return 0
    print('MUTANT-SURVIVES positive control %s (%s); mutant check %s'
          % ('PASS' if ok_orig else 'FAIL', '; '.join(reasons_orig) if reasons_orig else 'no reasons',
             'FAIL' if reasons_mut else 'PASS'))
    return 1


if __name__ == '__main__':
    sys.exit(main())
