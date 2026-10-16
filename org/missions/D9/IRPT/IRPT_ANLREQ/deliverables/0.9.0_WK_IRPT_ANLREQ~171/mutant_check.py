#!/usr/bin/env python3
"""AR-y-379 (AC3, the one mutant that fails): the amended driver with validateAdvisorEmail made to admit a real-domain address.

Copies the amended driver (and its mint helper, which the selftest reads) to a scratch folder in the system temp directory,
OUTSIDE the product tree, and runs the copy's own --selftest. Two runs:
  1. the unmutated copy (the positive control): must PASS, prints POSITIVE-CONTROL PASSES;
  2. the mutated copy: the domain check is replaced by `if (false) return`, so a real-domain address is admitted.
Prints MUTANT-FIRES only when the mutated copy's selftest FAILS (exit 0); otherwise MUTANT-SURVIVES (exit 1).
No browser, no mint, no network: the selftest is offline and the mutant never reaches run() (its cases are plan-only or refused).

Usage: python mutant_check.py
"""
import os
import shutil
import subprocess
import sys
import tempfile

DRIVER_REL = 'org/missions/D9/IRPT/IRPT_ANLREQ/deliverables/0.9.0_WK_IRPT_ANLREQ~149/fwd1_driver/fwd1_driver.mjs'
MINT_REL = 'org/missions/D9/IRPT/IRPT_ANLREQ/deliverables/0.9.0_WK_IRPT_ANLREQ~149/fwd1_driver/fwd1_mint.py'
ANCHOR = 'if (domain !== ADVISOR_EMAIL_DOMAIN) return'
MUTANT = 'if (false) return'
SELFTEST_TIMEOUT = 240


def repo_root():
    here = os.path.dirname(os.path.abspath(__file__))
    out = subprocess.run(['git', '-C', here, 'rev-parse', '--show-toplevel'], capture_output=True, text=True)
    if out.returncode != 0:
        raise SystemExit('MUTANT-SURVIVES cannot find the worktree root (git rc=%d)' % out.returncode)
    return out.stdout.strip()


def selftest(path):
    """Runs the copy's --selftest at its own path; returns (rc, the verdict line, the case FAIL lines, the case count)."""
    node = shutil.which('node')
    if node is None:
        raise SystemExit('MUTANT-SURVIVES node is not on PATH; no selftest was run')
    run = subprocess.run([node, path, '--selftest'], capture_output=True, text=True, timeout=SELFTEST_TIMEOUT)
    lines = (run.stdout or '').splitlines()
    verdict = [ln for ln in lines if ln.startswith('SELFTEST-OK') or ln.startswith('SELFTEST-BAD')]
    fails = [ln for ln in lines if ln.startswith('case FAIL')]
    cases = [ln for ln in lines if ln.startswith('case PASS') or ln.startswith('case FAIL')]
    return run.returncode, (verdict[-1] if verdict else 'NO-VERDICT'), fails, len(cases)


def main():
    repo = repo_root()
    src = os.path.join(repo, DRIVER_REL)
    mint = os.path.join(repo, MINT_REL)
    with open(src, encoding='utf-8') as fh:
        text = fh.read()
    if text.count(ANCHOR) != 1:
        print('MUTANT-SURVIVES the mutation anchor occurs %d times in the amended driver (need 1); no mutant was run' % text.count(ANCHOR))
        return 1
    scratch = tempfile.mkdtemp(prefix='ar379_mutant_')
    try:
        base_copy = os.path.join(scratch, 'base', 'fwd1_driver.mjs')
        mut_copy = os.path.join(scratch, 'mutant', 'fwd1_driver.mjs')
        for sub in ('base', 'mutant'):
            os.makedirs(os.path.join(scratch, sub))
            shutil.copyfile(mint, os.path.join(scratch, sub, 'fwd1_mint.py'))
        with open(base_copy, 'w', encoding='utf-8', newline='\n') as fh:
            fh.write(text)
        with open(mut_copy, 'w', encoding='utf-8', newline='\n') as fh:
            fh.write(text.replace(ANCHOR, MUTANT, 1))
        rc_b, verdict_b, fails_b, n_b = selftest(base_copy)
        if rc_b != 0 or not verdict_b.startswith('SELFTEST-OK'):
            print('POSITIVE-CONTROL FAILS the unmutated copy: rc=%d %s (%d cases); no verdict on the mutant' % (rc_b, verdict_b, n_b))
            return 1
        print('POSITIVE-CONTROL PASSES the unmutated copy: rc=%d %s (%d of %d cases)' % (rc_b, verdict_b, n_b - len(fails_b), n_b))
        rc_m, verdict_m, fails_m, n_m = selftest(mut_copy)
        if rc_m != 0 and fails_m:
            print('MUTANT-FIRES domain check replaced by `if (false) return` in a scratch copy: the copy --selftest FAILS (rc=%d, %s; '
                  '%d of %d cases FAIL under the mutant)' % (rc_m, verdict_m, len(fails_m), n_m))
            return 0
        print('MUTANT-SURVIVES the copy --selftest passed under the mutant (rc=%d, %s)' % (rc_m, verdict_m))
        return 1
    finally:
        shutil.rmtree(scratch, ignore_errors=True)


if __name__ == '__main__':
    sys.exit(main())
