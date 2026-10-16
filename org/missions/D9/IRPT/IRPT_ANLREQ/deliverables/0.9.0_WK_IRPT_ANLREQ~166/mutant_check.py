#!/usr/bin/env python3
"""AR-y-372 (AC3): the one mutant that must fire.

Copies the amended driver and its mint helper to a scratch folder OUTSIDE the product tree (a system tempfile directory),
DISABLES the planned-yes fall-through in the copy (a planned yes with no Yes button returns ok:false again, as signed), and runs
the copy's --selftest. Positive control first: the unmutated copy must pass its own --selftest.

Prints MUTANT-FIRES only when the unmutated copy passes and the mutated copy's --selftest FAILS (exit 0); otherwise
MUTANT-SURVIVES (exit 1). The failing case names are printed so the verdict can be read.
"""
import os
import shutil
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
DRIVER_NAME = 'fwd1_driver.mjs'
MINT_NAME = 'fwd1_mint.py'
DRIVER_DIR_REL = 'org/missions/D9/IRPT/IRPT_ANLREQ/deliverables/0.9.0_WK_IRPT_ANLREQ~149/fwd1_driver'
ANCHOR = "if (d.answer === 'yes' && d.fallback === FALLBACK_NO && buttons.includes(PROMPT_NO)) {"
REPLACEMENT = 'if (false) {'


def repo_root():
    out = subprocess.run(['git', '-C', HERE, 'rev-parse', '--show-toplevel'], capture_output=True, text=True)
    if out.returncode != 0:
        raise SystemExit('MUTANT-SURVIVES cannot find the worktree root (git rc=%d)' % out.returncode)
    return out.stdout.strip()


def node_bin():
    return shutil.which('node') or 'node'


def selftest(path):
    """Runs the copy's --selftest under a bound. Returns (rc, the SELFTEST line, the failing case names)."""
    try:
        out = subprocess.run([node_bin(), path, '--selftest'], capture_output=True, text=True, timeout=300)
    except subprocess.TimeoutExpired:
        return 124, 'SELFTEST timeout', []
    text = out.stdout + out.stderr
    verdict = next((ln for ln in text.splitlines() if ln.startswith('SELFTEST-')), 'SELFTEST no verdict line')
    failing = [ln[len('case FAIL '):] for ln in text.splitlines() if ln.startswith('case FAIL ')]
    return out.returncode, verdict, failing


def main():
    repo = repo_root()
    src_dir = os.path.join(repo, DRIVER_DIR_REL)
    with open(os.path.join(src_dir, DRIVER_NAME), encoding='utf-8') as fh:
        text = fh.read()
    hits = text.count(ANCHOR)
    if hits != 1:
        print('MUTANT-SURVIVES mutation anchor occurs %d times in the amended driver (need 1)' % hits)
        return 1
    mutated = text.replace(ANCHOR, REPLACEMENT)
    scratch = tempfile.mkdtemp(prefix='ar372_mutant_')
    try:
        shutil.copyfile(os.path.join(src_dir, MINT_NAME), os.path.join(scratch, MINT_NAME))
        orig_path = os.path.join(scratch, 'fwd1_driver_unmutated.mjs')
        mut_path = os.path.join(scratch, 'fwd1_driver_mutant.mjs')
        with open(orig_path, 'w', encoding='utf-8', newline='\n') as fh:
            fh.write(text)
        with open(mut_path, 'w', encoding='utf-8', newline='\n') as fh:
            fh.write(mutated)
        rc_orig, verdict_orig, fail_orig = selftest(orig_path)
        rc_mut, verdict_mut, fail_mut = selftest(mut_path)
    finally:
        shutil.rmtree(scratch, ignore_errors=True)
    if rc_orig == 0 and rc_mut != 0:
        print('MUTANT-FIRES the planned-yes fall-through disabled in a scratch copy: the copy --selftest FAILS (rc %d, %s; '
              'failing: %s); positive control PASSES (rc 0, %s)' % (rc_mut, verdict_mut, '; '.join(fail_mut)[:600], verdict_orig))
        return 0
    print('MUTANT-SURVIVES positive control rc %d (%s); mutant rc %d (%s)' % (rc_orig, verdict_orig, rc_mut, verdict_mut))
    return 1


if __name__ == '__main__':
    sys.exit(main())
