"""TCKT_VNEXT round 20 -- the issuer's checks for cell R20-pt-5 (the meeting outcome line readable on the Ticket Center board: row TCKT_VNEXT-D2-S59,
the CTO's ruling msg 10423).

  pf-diff  --portal <dir> --base <ref>   the committed diff of HEAD against the base touches ONLY MeetingRequestParts.tsx and the new contrast test, and
                                         no added line carries Trade Request upload code. Prints R20-PF-DIFF-OK <n files> or R20-PF-DIFF-BAD <reason>.
  pf-tests --portal <dir>                the new contrast test file exists and `bun test` of it plus the two meeting test files passes with no failure.
                                         Prints R20-PF-TESTS-OK pass=<n> or R20-PF-TESTS-BAD <reason>.
  --self-test                            the diff scan on good and bad fixtures (no git, no bun). Prints R20-PF-SELFTEST-OK.
"""
import re
import shutil
import subprocess
import sys
from pathlib import Path

PARTS = "src/pages/TicketCenter/MeetingRequestParts.tsx"
NEWTEST = "src/pages/TicketCenter/__tests__/meeting-outcome-contrast.test.tsx"
ALLOWED = {PARTS, NEWTEST}
FORBIDDEN_ADDED = ("TradeFormOpen", "trade-form-upload", "TradeRequestUpload", "AnalysisPackageRow")
TESTS = [NEWTEST,
         "src/pages/TicketCenter/__tests__/meeting-outcome-visibility.test.tsx",
         "src/pages/TicketCenter/__tests__/meeting-request.test.tsx"]
STRIP = re.compile(r"\x1b\[[0-9;]*m")


def diff_problem(names, added_lines):
    names = set(names)
    extra = sorted(names - ALLOWED)
    if extra:
        return "files outside the two allowed: %s" % extra
    lacking = sorted(ALLOWED - names)
    if lacking:
        return "the fix lacks %s" % lacking
    for line in added_lines:
        for bad in FORBIDDEN_ADDED:
            if bad in line:
                return "an added line carries %r" % bad
    return None


def git(portal, *args):
    return subprocess.run(["git", "-C", str(portal)] + list(args), capture_output=True, text=True, timeout=120)


def pf_diff(portal, base):
    names = git(portal, "diff", "--name-only", base, "HEAD")
    if names.returncode != 0 or not names.stdout.strip():
        return "R20-PF-DIFF-BAD no diff against %s (rc=%d)" % (base, names.returncode)
    body = git(portal, "diff", "-U0", base, "HEAD")
    added = [ln[1:] for ln in body.stdout.splitlines() if ln.startswith("+") and not ln.startswith("+++")]
    why = diff_problem(names.stdout.split(), added)
    return "R20-PF-DIFF-BAD %s" % why if why else "R20-PF-DIFF-OK %d files" % len(names.stdout.split())


def pf_tests(portal):
    if not (Path(portal) / NEWTEST).exists():
        return "R20-PF-TESTS-BAD the contrast test file is absent: %s" % NEWTEST
    bun = shutil.which("bun")
    if not bun:
        return "R20-PF-TESTS-BAD bun not on PATH"
    r = subprocess.run([bun, "test"] + TESTS, cwd=str(portal), capture_output=True, text=True, timeout=170)
    out = STRIP.sub("", r.stdout + r.stderr)
    passed = int((re.search(r"(\d+) pass", out) or [0, 0])[1])
    failed = int((re.search(r"(\d+) fail", out) or [0, 0])[1])
    if r.returncode != 0 or failed or passed < 26:
        return "R20-PF-TESTS-BAD rc=%d pass=%d fail=%d (the two meeting files carry 24 and the new file at least 2)" % (r.returncode, passed, failed)
    return "R20-PF-TESTS-OK pass=%d" % passed


def selftest():
    ok = sorted(ALLOWED)
    if diff_problem(ok, ["className={`text-xs font-medium text-white/80`}"]) is not None:
        return "good fixture refused"
    if diff_problem(ok + ["src/pages/TicketCenter/TicketCenter.tsx"], []) is None:
        return "an extra file was not caught"
    if diff_problem([PARTS], []) is None:
        return "a missing test file was not caught"
    if diff_problem(ok, ["import { TradeFormOpen } from './x'"]) is None:
        return "TradeFormOpen was not caught"
    return None


def main(argv):
    if argv[:1] == ["--self-test"]:
        why = selftest()
        print("R20-PF-SELFTEST-OK" if why is None else "R20-PF-SELFTEST-FAIL " + why)
        return 0 if why is None else 1
    if len(argv) >= 3 and argv[0] == "pf-tests" and argv[1] == "--portal":
        out = pf_tests(argv[2])
    elif len(argv) >= 5 and argv[0] == "pf-diff" and argv[1] == "--portal" and argv[3] == "--base":
        out = pf_diff(argv[2], argv[4])
    else:
        print("usage: r20_pf_checks.py pf-diff --portal <dir> --base <ref> | pf-tests --portal <dir> | --self-test")
        return 2
    print(out)
    return 0 if "-OK" in out else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
