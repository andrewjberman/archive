#!/usr/bin/env python3
"""AR-y-366 (AC2): the labels check of the amended FWD-1 driver.

Prints exactly one verdict line:
  LABELS-OK <n> labels, POST_ALLOWED identical, no-decisions path unchanged   (exit 0)
  LABELS-BAD <why>                                                             (exit 1)

Checks (the cell's three rules):
  (1) every prompt label constant the driver uses occurs in the candidate source (portal commit 0ba0cb13, read with git show);
  (2) the POST_ALLOWED block is byte-identical to the base commit's block;
  (3) every line between the signed STEP-3 sign-in and the holdings setInputFiles, and every line from the Submit wait to the
      end of the file, is unchanged from the base, except lines the new option adds inside an `if (o.decisions)` guard.
      The region between the holdings setInputFiles and the Submit wait is new code and must be guarded the same way.

Usage: python labels_check.py [--driver <path>] [--detail]
"""
import difflib
import os
import re
import subprocess
import sys

BASE_SHA = '2b0a50b912'
DRIVER_REL = 'org/missions/D9/IRPT/IRPT_ANLREQ/deliverables/0.9.0_WK_IRPT_ANLREQ~149/fwd1_driver/fwd1_driver.mjs'
PORTAL_REPO = 'C:/dev/ajb_workspace/portal'
PORTAL_SHA = '0ba0cb13'
PORTAL_SOURCES = [
    'src/pages/TicketCenter/AnalysisRequestParts.tsx',
    'src/pages/TicketCenter/TicketCenter.tsx',
    'src/pages/TicketCenter/analysisRequest.ts',
]
LABEL_CONSTANTS = [
    'PROMPT_YES', 'PROMPT_REPLACE', 'PROMPT_NO', 'PROMPT_CHECK', 'REPLACE_INPUT_PREFIX', 'FILED_AS_GIVEN_HEADING',
    'DID_YOU_MEAN_PREFIX', 'NOT_FOUND_SUFFIX', 'NO_CHOICE_LINE',
]
A_START = "log('STEP-3 signed in through the real form"
A_END = "await page.locator('input[aria-label=\"Holdings file\"]').setInputFiles(o.holdings)"
B_START = "const submit = page.getByRole('button', { name: SUBMIT_LABEL, exact: true })"
POST_START = 'const POST_ALLOWED = ['
GUARD = 'if (o.decisions)'


def repo_root():
    here = os.path.dirname(os.path.abspath(__file__))
    out = subprocess.run(['git', '-C', here, 'rev-parse', '--show-toplevel'], capture_output=True, text=True)
    if out.returncode != 0:
        raise SystemExit('LABELS-BAD cannot find the worktree root (git rc=%d)' % out.returncode)
    return out.stdout.strip()


def git_show(repo, ref_path):
    out = subprocess.run(['git', '-C', repo, 'show', ref_path], capture_output=True)
    if out.returncode != 0:
        raise SystemExit('LABELS-BAD git show %s failed (rc=%d)' % (ref_path, out.returncode))
    return out.stdout.decode('utf-8')


def label_literals(driver_text):
    found = {}
    for name in LABEL_CONSTANTS:
        m = re.search(r"^const " + name + r" = '(.*)'$", driver_text, re.M)
        found[name] = m.group(1) if m else None
    return found


def check_labels(driver_text):
    """Rule (1). Returns (ok, n, reasons, details)."""
    sources = {p: git_show(PORTAL_REPO, PORTAL_SHA + ':' + p) for p in PORTAL_SOURCES}
    lits = label_literals(driver_text)
    reasons, details = [], []
    for name in LABEL_CONSTANTS:
        lit = lits[name]
        if lit is None:
            reasons.append('constant %s is missing from the driver' % name)
            continue
        hit = None
        for p in PORTAL_SOURCES:
            idx = sources[p].find(lit)
            if idx >= 0:
                line = sources[p].count('\n', 0, idx) + 1
                hit = (p, line)
                break
        if hit is None:
            reasons.append('label %s = %r occurs in no candidate source' % (name, lit))
            details.append('label %s %r NOT FOUND' % (name, lit))
        else:
            details.append('label %s %r at %s:%d (portal %s)' % (name, lit, hit[0], hit[1], PORTAL_SHA))
    return (not reasons), len(LABEL_CONSTANTS), reasons, details


def post_block(lines):
    start = None
    for i, ln in enumerate(lines):
        if ln.startswith(POST_START):
            start = i
            break
    if start is None:
        return None
    for j in range(start + 1, len(lines)):
        if lines[j] == ']':
            return lines[start:j + 1]
    return None


def find_one(lines, needle, label):
    hits = [i for i, ln in enumerate(lines) if needle in ln]
    if len(hits) != 1:
        raise ValueError('%s anchor occurs %d times (need 1)' % (label, len(hits)))
    return hits[0]


def guarded_insert(lines_added):
    """A block of added lines is allowed only when its first line is the guard and every line stays inside its indentation."""
    if not lines_added:
        return True
    first = lines_added[0]
    if GUARD not in first:
        return False
    base_indent = len(first) - len(first.lstrip(' '))
    for ln in lines_added[1:]:
        if ln.strip() == '':
            continue
        if (len(ln) - len(ln.lstrip(' '))) < base_indent:
            return False
    return True


def region_violations(base_seg, amend_seg, where):
    """Returns (violations, compared_lines) for one region."""
    out = []
    sm = difflib.SequenceMatcher(a=base_seg, b=amend_seg, autojunk=False)
    for tag, i1, i2, j1, j2 in sm.get_opcodes():
        if tag == 'equal':
            continue
        if tag in ('delete', 'replace'):
            out.append('%s: %d base line(s) removed or changed (first: %r)' % (where, i2 - i1, base_seg[i1][:70]))
            continue
        if tag == 'insert' and not guarded_insert(amend_seg[j1:j2]):
            out.append('%s: %d added line(s) outside an %s guard (first: %r)' % (where, j2 - j1, GUARD, amend_seg[j1][:70]))
    return out, len(base_seg) + len(amend_seg)


def check_unchanged(base_text, amend_text):
    """Rules (2) and (3). Returns (ok, reasons, denominator_text)."""
    bl = base_text.split('\n')
    al = amend_text.split('\n')
    reasons = []
    base_post = post_block(bl)
    amend_post = post_block(al)
    if base_post is None or amend_post is None:
        reasons.append('POST_ALLOWED block not found (base %s, amended %s)' % (base_post is not None, amend_post is not None))
    elif base_post != amend_post:
        reasons.append('POST_ALLOWED block differs from the base (%d base lines, %d amended lines)' % (len(base_post), len(amend_post)))
    try:
        ba0, ba1 = find_one(bl, A_START, 'base STEP-3'), find_one(bl, A_END, 'base setInputFiles')
        aa0, aa1 = find_one(al, A_START, 'amended STEP-3'), find_one(al, A_END, 'amended setInputFiles')
        bb = find_one(bl, B_START, 'base Submit wait')
        ab = find_one(al, B_START, 'amended Submit wait')
    except ValueError as e:
        return False, reasons + [str(e)], ''
    denom = 0
    v, n = region_violations(bl[ba0:ba1 + 1], al[aa0:aa1 + 1], 'region STEP-3..setInputFiles')
    reasons += v
    denom += n
    v, n = region_violations(bl[ba1 + 1:bb], al[aa1 + 1:ab], 'region setInputFiles..Submit wait (new code)')
    reasons += v
    denom += n
    v, n = region_violations(bl[bb:], al[ab:], 'region Submit wait..end of file')
    reasons += v
    denom += n
    return (not reasons), reasons, 'region lines compared: %d' % denom


def main(argv):
    detail = '--detail' in argv
    driver = None
    if '--driver' in argv:
        driver = argv[argv.index('--driver') + 1]
    repo = repo_root()
    if driver is None:
        driver = os.path.join(repo, DRIVER_REL)
    with open(driver, encoding='utf-8') as fh:
        amend_text = fh.read()
    base_text = git_show(repo, BASE_SHA + ':' + DRIVER_REL)
    ok1, n, r1, d1 = check_labels(amend_text)
    ok23, r23, denom = check_unchanged(base_text, amend_text)
    if detail:
        for line in d1:
            print(line)
        print('denominator: %d labels; %s' % (n, denom))
    reasons = r1 + r23
    if not reasons:
        print('LABELS-OK %d labels, POST_ALLOWED identical, no-decisions path unchanged' % n)
        return 0
    print('LABELS-BAD ' + ' | '.join(reasons) + ' (%d label constants checked; %s)' % (n, denom))
    return 1


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
