"""AR332-y-AC1 -- the portal test gate of TO-AR-y-332 (0.9.0_WK_IRPT_ANLREQ~140).

Runs `bun test` in the candidate portal worktree on three targets: the new test file, the whole
src/pages/TicketCenter folder, and the whole src/pages/InvestorReporting folder. The failing NAMES of the
InvestorReporting run are compared with the failing names recorded from a clean origin/PROD worktree
(r41/baseline_ir_failures.json).

Prints PORTAL-TESTS-OK ... only when the new file has cases (a) to (f) all passing, TicketCenter has 0 failed,
and every failing InvestorReporting name is in the baseline (a baseline name that now passes is fine).
Otherwise prints PORTAL-TESTS-BAD <why> and exits 1.
"""
import json
import os
import shutil
import subprocess
import sys
import tempfile
import xml.etree.ElementTree as ET

WT = 'C:/dev/wk-irpt-anlreq-140'
PORTAL = WT + '/portal'
DELIV = WT + '/org/missions/D9/IRPT/IRPT_ANLREQ/deliverables/0.9.0_WK_IRPT_ANLREQ~140'
BASELINE = DELIV + '/r41/baseline_ir_failures.json'
NEW_FILE = 'src/pages/TicketCenter/__tests__/commentary-pdf-reader.test.tsx'
TICKET_DIR = 'src/pages/TicketCenter'
IR_DIR = 'src/pages/InvestorReporting'
CASES = ['(a)', '(b)', '(c)', '(d)', '(e)', '(f)']


def bad(why):
    print('PORTAL-TESTS-BAD ' + why)
    sys.exit(1)


def run_junit(target, outdir, label):
    """Run bun test on one target; return (cases, rc) where cases is a list of (classname, name, failed)."""
    bun = shutil.which('bun')
    if bun is None:
        bad('bun is not on PATH')
    out = os.path.join(outdir, label + '.junit.xml')
    try:
        run = subprocess.run(
            [bun, 'test', target, '--reporter=junit', '--reporter-outfile=' + out],
            cwd=PORTAL, capture_output=True, text=True, timeout=900,
        )
    except subprocess.TimeoutExpired:
        bad(label + ': bun test timed out (900 s)')
    if not os.path.exists(out):
        bad(label + ': bun test wrote no junit file (rc=%s)' % run.returncode)
    root = ET.parse(out).getroot()
    cases = []
    for case in root.iter('testcase'):
        failed = case.find('failure') is not None or case.find('error') is not None
        cases.append((case.get('classname', ''), case.get('name', ''), failed))
    return cases, run.returncode


def main():
    with open(BASELINE, 'r', encoding='utf-8') as fh:
        baseline = json.load(fh)
    baseline_names = set(entry['name'] for entry in baseline['failing'])

    outdir = tempfile.mkdtemp(prefix='portal_check_', dir=WT + '/.scratch')
    new_cases, _ = run_junit(NEW_FILE, outdir, 'new_file')
    tc_cases, _ = run_junit(TICKET_DIR, outdir, 'ticketcenter')
    ir_cases, _ = run_junit(IR_DIR, outdir, 'investor_reporting')

    # (1) the new file: six cases, one per letter (a) to (f), each passing
    if len(new_cases) != 6:
        bad('new file ran %d cases, expected 6' % len(new_cases))
    for letter in CASES:
        hits = [c for c in new_cases if c[1].startswith(letter + ' ')]
        if len(hits) != 1:
            bad('case %s not found exactly once (%d)' % (letter, len(hits)))
        if hits[0][2]:
            bad('case %s FAILS: %s' % (letter, hits[0][1][:90]))
    new_passed = sum(1 for c in new_cases if not c[2])

    # (2) TicketCenter: 0 failed
    tc_failed = [c for c in tc_cases if c[2]]
    if tc_failed:
        bad('TicketCenter has %d failing case(s): %s' % (len(tc_failed), tc_failed[0][1][:90]))
    tc_passed = sum(1 for c in tc_cases if not c[2])

    # (3) InvestorReporting: every failing name is in the baseline
    ir_failing = [c for c in ir_cases if c[2]]
    ir_failing_names = set(c[1] for c in ir_failing)
    new_names = sorted(n for n in ir_failing_names if n not in baseline_names)
    if new_names:
        bad('InvestorReporting failing name(s) NOT in the baseline: ' + ' | '.join(n[:80] for n in new_names))

    print('PORTAL-TESTS-OK %d new, %d TicketCenter 0 failed, %d IR failing (all in the baseline)' % (
        new_passed, tc_passed, len(ir_failing)))
    sys.exit(0)


if __name__ == '__main__':
    main()
