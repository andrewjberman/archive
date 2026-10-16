#!/usr/bin/env python3
"""AR-y-379 (AC2): the labels, order and action check of the FWD-1 driver amended with the advisor login email option and its one fill.

Prints exactly one verdict line, with its denominator on the same line:
  LABELS-OK <n> labels, POST_ALLOWED identical, nothing before the Submit, exactly one new fill (denominator ...)  (exit 0)
  LABELS-BAD <why> (denominator ...)                                                                              (exit 1)

Rules (a) to (e) and (g) are worker 168's AR-y-374 rules, read unchanged in shape:
  (a) every line from the STEP-3 sign-in to the holdings setInputFiles is unchanged from the base 2b0a50b912; and no decision
      PRESS and no loop CALL sits between that setInputFiles and the Submit click (the listener's timeout is not a press);
  (b) in run(), the ticket-answer listener comes before submit.click(); every decision press comes after submit.click(),
      counted at its call site when it sits in answerAfterSubmit; the loop is called once, after the click, behind `if (o.decisions) {`;
  (c) the POST_ALLOWED block is byte-identical to the base 9c82e9d091 and to 2b0a50b912;
  (d) the lines of the selftest function are excluded from every scan above;
  (e) every label constant occurs in portal 0ba0cb13 (AnalysisRequestParts.tsx, TicketCenter.tsx or analysisRequest.ts).
  (g) STILL_CHECKING_TEXT occurs verbatim in portal fcbf2bce, src/pages/TicketCenter/analysisRequest.ts.
Rule (f3) is this cell's: against the merged driver c7ee06e478 the amended driver has EXACTLY ONE more .fill( token and no other
  new action token (.click( .press( .check( .selectOption( .setInputFiles( page.request), counted outside the selftest; both totals printed.
Rule (h) is this cell's: the string 'Advisor login email' occurs once in the driver, on the locator line inside run(); its one fill
  sits after the holdings upload and before the Submit click; the ADVISOR-EMAIL-NEEDED stop sits before the Submit click too.

Usage: python labels_check.py [--driver <path>] [--detail]
"""
import os
import re
import subprocess
import sys

BASE_REGION_SHA = '2b0a50b912'
BASE_ORDER_SHA = '9c82e9d091'
BASE_MERGED_SHA = 'c7ee06e478'
DRIVER_REL = 'org/missions/D9/IRPT/IRPT_ANLREQ/deliverables/0.9.0_WK_IRPT_ANLREQ~149/fwd1_driver/fwd1_driver.mjs'
PORTAL_REPO = 'C:/dev/ajb_workspace/portal'
PORTAL_SHA = '0ba0cb13'
PORTAL_FORM_SHA = 'fcbf2bce'
FORM_SOURCE = 'src/pages/TicketCenter/analysisRequest.ts'
PORTAL_SOURCES = [
    'src/pages/TicketCenter/AnalysisRequestParts.tsx',
    'src/pages/TicketCenter/TicketCenter.tsx',
    'src/pages/TicketCenter/analysisRequest.ts',
]
LABEL_CONSTANTS = [
    'PROMPT_YES', 'PROMPT_REPLACE', 'PROMPT_NO', 'PROMPT_CHECK', 'REPLACE_INPUT_PREFIX', 'FILED_AS_GIVEN_HEADING',
    'DID_YOU_MEAN_PREFIX', 'NOT_FOUND_SUFFIX', 'NO_CHOICE_LINE',
]
ACTION_TOKENS = ['.click(', '.fill(', '.press(', '.check(', '.selectOption(', '.setInputFiles(', 'page.request']
NEW_FILL_TOKEN = '.fill('
A_START = 'STEP-3 signed in through the real form'
A_END = 'setInputFiles(o.holdings)'
RUN_START = 'async function run(o) {'
RUN_END_PREFIX = 'async function readPackage('
HELPER_PREFIX = 'export async function answerAfterSubmit('
SELF_START_NAMES = ('async function selftest() {', 'function selftest() {')
MAIN_PREFIX = 'export async function main('
LISTENER_RE = re.compile(r"^    const ticketAnswer = page\.waitForResponse\(")
SUBMIT_LINE = '    await submit.click()'
LOOP_CALL_RE = re.compile(r"^\s*(const \w+ = )?await answerAfterSubmit\(page")
PRESS_RE = re.compile(r"getByRole\('button', \{ name: (PROMPT_YES|PROMPT_REPLACE|PROMPT_NO|PROMPT_CHECK|plan\.button)\b")
POST_START = 'const POST_ALLOWED = ['
STILL_RE = re.compile(r"^const STILL_CHECKING_TEXT = '(.*)'$", re.M)
ADVISOR_LABEL = 'Advisor login email'
ADVISOR_LOCATOR_LINE = "    const advisorField = page.locator('input[aria-label=\"Advisor login email\"]')"
ADVISOR_NEEDED_LINE = "    if (advisorAct.action === 'needed') throw new Error(advisorAct.why)"


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


def one(lines, pred, lo, hi, what):
    hits = [i for i in range(lo, hi) if pred(lines[i])]
    if len(hits) != 1:
        raise ValueError('%s occurs %d times in run() (need 1)' % (what, len(hits)))
    return hits[0]


def run_span(lines):
    """Index span [run_s, run_e) of run() (by exact line anchors)."""
    run_s = lines.index(RUN_START)
    run_e = next(i for i in range(run_s + 1, len(lines)) if lines[i].startswith(RUN_END_PREFIX))
    return run_s, run_e


def spans(lines):
    """Index spans of run(), the answerAfterSubmit helper and the selftest function (by exact line anchors)."""
    run_s, run_e = run_span(lines)
    helper_s = next(i for i, ln in enumerate(lines) if ln.startswith(HELPER_PREFIX))
    helper_e = next(i for i in range(helper_s + 1, len(lines)) if lines[i] == '}')
    self_s = next(i for i, ln in enumerate(lines) if ln in SELF_START_NAMES)
    self_e = next(i for i in range(self_s + 1, len(lines)) if lines[i].startswith(MAIN_PREFIX))
    return run_s, run_e, helper_s, helper_e, self_s, self_e


def label_literals(driver_text):
    found = {}
    for name in LABEL_CONSTANTS:
        m = re.search(r"^const " + name + r" = '(.*)'$", driver_text, re.M)
        found[name] = m.group(1) if m else None
    return found


def check_labels(driver_text, repo):
    """Rule (e). Returns (ok, n, reasons, details)."""
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
                hit = (p, sources[p].count('\n', 0, idx) + 1)
                break
        if hit is None:
            reasons.append('label %s = %r occurs in no candidate source' % (name, lit))
        else:
            details.append('label %s %r at %s:%d' % (name, lit, hit[0], hit[1]))
    return (not reasons), len(LABEL_CONSTANTS), reasons, details


def post_block(lines):
    start = next((i for i, ln in enumerate(lines) if ln.startswith(POST_START)), None)
    if start is None:
        return None
    end = next((j for j in range(start + 1, len(lines)) if lines[j] == ']'), None)
    return None if end is None else lines[start:end + 1]


def check_post(base_order_lines, base_region_lines, lines):
    """Rule (c). Returns (reasons, lines_compared)."""
    reasons = []
    cur = post_block(lines)
    if cur is None:
        return ['POST_ALLOWED block not found in the driver'], 0
    for label, base in (('base ' + BASE_ORDER_SHA, base_order_lines), ('base ' + BASE_REGION_SHA, base_region_lines)):
        ref = post_block(base)
        if ref is None:
            reasons.append('POST_ALLOWED block not found in %s' % label)
        elif ref != cur:
            reasons.append('POST_ALLOWED block differs from %s (%d base lines, %d amended lines)' % (label, len(ref), len(cur)))
    return reasons, len(cur)


def check_order(lines):
    """Rules (a) second half, (b) and (d). Returns (reasons, stats dict)."""
    run_s, run_e, helper_s, helper_e, self_s, self_e = spans(lines)
    excluded = set(range(self_s, self_e))
    reasons = []
    run_lines = [i for i in range(run_s, run_e) if i not in excluded]
    submit = [i for i in run_lines if lines[i] == SUBMIT_LINE]
    if len(submit) != 1:
        return ['the Submit click line occurs %d times in run() (need 1)' % len(submit)], {}
    sub = submit[0]
    listen = [i for i in run_lines if LISTENER_RE.match(lines[i])]
    if len(listen) != 1 or "/api/scoped/tickets'" not in lines[listen[0]]:
        reasons.append('the ticket-answer listener line is not unique or does not name /api/scoped/tickets')
    elif not listen[0] < sub:
        reasons.append('the ticket-answer listener (line %d) comes after the Submit click (line %d)' % (listen[0] + 1, sub + 1))
    # (a) second half: between setInputFiles and the Submit click, no press and no loop call
    a_end = one(lines, lambda ln: A_END in ln, run_s, run_e, 'setInputFiles')
    for i in run_lines:
        if a_end < i < sub:
            if PRESS_RE.search(lines[i]) or LOOP_CALL_RE.match(lines[i]):
                reasons.append('a decision press or loop call sits before the Submit click (line %d)' % (i + 1))
    # (b) the loop call: once, after the click, behind if (o.decisions) {
    calls = [i for i in run_lines if LOOP_CALL_RE.match(lines[i])]
    if len(calls) != 1:
        reasons.append('the loop is called %d times in run() (need 1)' % len(calls))
    else:
        c = calls[0]
        if c <= sub:
            reasons.append('the loop call (line %d) comes before the Submit click (line %d)' % (c + 1, sub + 1))
        if lines[c - 1] != '    if (o.decisions) {':
            reasons.append('the loop call is not directly behind if (o.decisions) {')
    # (b) every decision press, counted at its call site
    presses = 0
    for i, ln in enumerate(lines):
        if i in excluded or not (PRESS_RE.search(ln) and '.click()' in ln):
            continue
        presses += 1
        if helper_s <= i < helper_e:
            pos = calls[0] if len(calls) == 1 else None
        elif run_s <= i < run_e:
            pos = i
        else:
            reasons.append('a decision press sits outside run() and the helper (line %d)' % (i + 1))
            continue
        if pos is None or pos <= sub:
            reasons.append('a decision press (line %d) is not after the Submit click (line %d)' % (i + 1, sub + 1))
    stats = {'submit_line': sub + 1, 'presses': presses, 'run_lines': len(run_lines),
             'selftest_excluded': len(excluded)}
    return reasons, stats


def check_advisor(lines):
    """Rule (h). Returns (reasons, stats dict)."""
    run_s, run_e, _h0, _h1, self_s, self_e = spans(lines)
    reasons = []
    occ = [i for i, ln in enumerate(lines) if ADVISOR_LABEL in ln]
    if len(occ) != 1:
        return ['the string %r occurs on %d lines of the driver (need 1)' % (ADVISOR_LABEL, len(occ))], {}
    lab = occ[0]
    if not (run_s <= lab < run_e):
        return ['the string %r is not inside run()' % ADVISOR_LABEL], {}
    if lines[lab] != ADVISOR_LOCATOR_LINE:
        reasons.append('the advisor label line is not the locator line the cell names (line %d)' % (lab + 1))
    a_end = one(lines, lambda ln: A_END in ln, run_s, run_e, 'setInputFiles')
    sub = one(lines, lambda ln: ln == SUBMIT_LINE, run_s, run_e, 'Submit click')
    needed = [i for i in range(run_s, run_e) if lines[i] == ADVISOR_NEEDED_LINE]
    if len(needed) != 1 or not (a_end < needed[0] < sub):
        reasons.append('the ADVISOR-EMAIL-NEEDED stop is not one line between the holdings upload and the Submit click')
    fills = [i for i in range(lab + 1, run_e) if '.fill(' in lines[i]]
    if not fills or not lines[fills[0]].strip().startswith('await advisorField.fill(advisorAct.value)'):
        reasons.append('the first .fill( after the advisor label is not the one advisor fill')
    elif not (a_end < fills[0] < sub):
        reasons.append('the advisor fill (line %d) is not between the holdings upload and the Submit click (line %d)' % (fills[0] + 1, sub + 1))
    elif not (fills[0] < sub):
        reasons.append('the Submit click (line %d) comes before the advisor fill (line %d)' % (sub + 1, fills[0] + 1))
    stats = {'label_line': lab + 1, 'fill_line': (fills[0] + 1) if fills else None, 'submit_line': sub + 1}
    return reasons, stats


def check_region_a(base_lines, lines):
    """Rule (a) first half: the sign-in to setInputFiles region is unchanged. Returns (reasons, lines compared)."""
    try:
        bs, be = run_span(base_lines)
        bA = one(base_lines, lambda ln: A_START in ln, bs, be, 'base STEP-3')
        bB = one(base_lines, lambda ln: A_END in ln, bs, be, 'base setInputFiles')
        s, e, _h0, _h1, _s0, _s1 = spans(lines)
        aA = one(lines, lambda ln: A_START in ln, s, e, 'amended STEP-3')
        aB = one(lines, lambda ln: A_END in ln, s, e, 'amended setInputFiles')
    except (ValueError, StopIteration) as err:
        return ['region anchors: %s' % err], 0
    base_seg = base_lines[bA:bB + 1]
    amend_seg = lines[aA:aB + 1]
    if base_seg != amend_seg:
        return ['the STEP-3 to setInputFiles region differs from base %s (%d base lines, %d amended lines)'
                % (BASE_REGION_SHA, len(base_seg), len(amend_seg))], len(base_seg) + len(amend_seg)
    return [], len(amend_seg)


def action_counts(lines):
    """Rule (f3): the action tokens outside the selftest function (the selftest span is excluded the same way in both files)."""
    _run_s, _run_e, _h0, _h1, self_s, self_e = spans(lines)
    counts = {t: 0 for t in ACTION_TOKENS}
    for i, ln in enumerate(lines):
        if self_s <= i < self_e:
            continue
        for t in ACTION_TOKENS:
            counts[t] += ln.count(t)
    return counts


def check_actions(base_lines, lines):
    """Rule (f3). Returns (reasons, base counts, amended counts)."""
    base = action_counts(base_lines)
    cur = action_counts(lines)
    reasons = []
    if cur[NEW_FILL_TOKEN] != base[NEW_FILL_TOKEN] + 1:
        reasons.append('%s occurs %d times in the amended driver outside selftest, base %s has %d (need exactly one more)'
                       % (NEW_FILL_TOKEN, cur[NEW_FILL_TOKEN], BASE_MERGED_SHA, base[NEW_FILL_TOKEN]))
    for t in ACTION_TOKENS:
        if t != NEW_FILL_TOKEN and cur[t] != base[t]:
            reasons.append('%s occurs %d times in the amended driver outside selftest, base %s has %d (need equal)'
                           % (t, cur[t], BASE_MERGED_SHA, base[t]))
    return reasons, base, cur


def check_still(driver_text, repo):
    """Rule (g). Returns (reasons, line in the form source or None, the constant text or None)."""
    m = STILL_RE.search(driver_text)
    if m is None:
        return ['the constant STILL_CHECKING_TEXT is missing from the driver'], None, None
    text = m.group(1)
    src = git_show(PORTAL_REPO, PORTAL_FORM_SHA + ':' + FORM_SOURCE)
    idx = src.find(text)
    if idx < 0:
        return ['STILL_CHECKING_TEXT occurs in no form source at portal %s' % PORTAL_FORM_SHA], None, text
    return [], src.count('\n', 0, idx) + 1, text


def main(argv):
    detail = '--detail' in argv
    driver = argv[argv.index('--driver') + 1] if '--driver' in argv else None
    repo = repo_root()
    if driver is None:
        driver = os.path.join(repo, DRIVER_REL)
    with open(driver, encoding='utf-8') as fh:
        text = fh.read()
    lines = text.split('\n')
    base_region = git_show(repo, BASE_REGION_SHA + ':' + DRIVER_REL).split('\n')
    base_order = git_show(repo, BASE_ORDER_SHA + ':' + DRIVER_REL).split('\n')
    base_merged = git_show(repo, BASE_MERGED_SHA + ':' + DRIVER_REL).split('\n')
    reasons = []
    ok_e, n, r_e, d_e = check_labels(text, repo)
    reasons += r_e
    r_a, n_a = check_region_a(base_region, lines)
    reasons += r_a
    r_c, n_c = check_post(base_order, base_region, lines)
    reasons += r_c
    r_b, stats = check_order(lines)
    reasons += r_b
    r_h, adv = check_advisor(lines)
    reasons += r_h
    r_f, base_counts, cur_counts = check_actions(base_merged, lines)
    reasons += r_f
    r_g, still_line, still_text = check_still(text, repo)
    reasons += r_g
    denom = ('%d labels; %d region lines compared (a); POST_ALLOWED %d lines (c); %d presses and %d run() lines ordered (b); '
             '%d selftest lines excluded (d); advisor label on line %s, its fill on line %s, Submit on line %s (h); '
             '%s base %s %d, amended %d (f3, one more fill, others equal); '
             'STILL_CHECKING_TEXT at form source %s line %s (g)'
             % (n, n_a, n_c, stats.get('presses', 0), stats.get('run_lines', 0), stats.get('selftest_excluded', 0),
                adv.get('label_line'), adv.get('fill_line'), adv.get('submit_line'),
                NEW_FILL_TOKEN, BASE_MERGED_SHA, base_counts[NEW_FILL_TOKEN], cur_counts[NEW_FILL_TOKEN],
                PORTAL_FORM_SHA, still_line))
    if detail:
        for line in d_e:
            print(line)
        print('action tokens base %s: %s' % (BASE_MERGED_SHA, ', '.join('%s %d' % (t, base_counts[t]) for t in ACTION_TOKENS)))
        print('action tokens amended: %s' % ', '.join('%s %d' % (t, cur_counts[t]) for t in ACTION_TOKENS))
    if not reasons:
        print('LABELS-OK %d labels, POST_ALLOWED identical, nothing before the Submit, exactly one new fill (denominator: %s)'
              % (n, denom))
        return 0
    print('LABELS-BAD ' + ' | '.join(reasons) + ' (denominator: %s)' % denom)
    return 1


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
