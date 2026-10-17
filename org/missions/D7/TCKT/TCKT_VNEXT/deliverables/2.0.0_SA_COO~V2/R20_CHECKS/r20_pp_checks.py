"""TCKT_VNEXT round 20 -- the issuer's checks for cell R20-pt-4 (the PROD-based re-cut of the meeting form 12c164a0 and the outcome line 8e4f0885,
WITHOUT the Trade Request upload c05e3dda; the CTO's ruling 4e37).

  prod-diff  --portal <dir> --base <ref>   the committed diff of HEAD against the PROD base touches ONLY the five meeting files, the added lines carry no
                                           Trade Request upload code and no AnalysisPackageRow, and the new test file is present.
                                           Prints R20-PP-DIFF-OK <n files> or R20-PP-DIFF-BAD <reason>.
  prod-tests --portal <dir>                `bun test` of the two meeting test files passes with no failure. Prints R20-PP-TESTS-OK pass=<n> or R20-PP-TESTS-BAD.
  --self-test                              the diff scan on good and bad fixtures (no git, no bun). Prints R20-PP-SELFTEST-OK.
"""
import re
import shutil
import subprocess
import sys

ALLOWED = {
    "src/api/endpoints/tickets.ts",
    "src/pages/TicketCenter/MeetingRequestParts.tsx",
    "src/pages/TicketCenter/TicketCenter.tsx",
    "src/pages/TicketCenter/__tests__/meeting-request.test.tsx",
    "src/pages/TicketCenter/__tests__/meeting-outcome-visibility.test.tsx",
}
REQUIRED = {"src/pages/TicketCenter/__tests__/meeting-outcome-visibility.test.tsx",
            "src/pages/TicketCenter/MeetingRequestParts.tsx"}
FORBIDDEN_ADDED = ("TradeFormOpen", "AnalysisPackageRow", "trade-form-upload", "trade_form_upload", "TradeRequestUpload")
TESTS = ["src/pages/TicketCenter/__tests__/meeting-request.test.tsx",
         "src/pages/TicketCenter/__tests__/meeting-outcome-visibility.test.tsx"]
STRIP = re.compile(r"\x1b\[[0-9;]*m")


def diff_problem(names, added_lines):
    """names: the changed file names; added_lines: the '+' lines of the diff (without the leading plus)."""
    names = set(names)
    extra = sorted(names - ALLOWED)
    if extra:
        return "files outside the five meeting files: %s" % extra
    lacking = sorted(REQUIRED - names)
    if lacking:
        return "the re-cut lacks %s" % lacking
    for line in added_lines:
        for bad in FORBIDDEN_ADDED:
            if bad in line:
                return "an added line carries %r: %s" % (bad, line.strip()[:80])
    return None


def git(portal, *args):
    return subprocess.run(["git", "-C", str(portal)] + list(args), capture_output=True, text=True, timeout=120)


def prod_diff(portal, base):
    names = git(portal, "diff", "--name-only", base, "HEAD")
    if names.returncode != 0 or not names.stdout.strip():
        return "R20-PP-DIFF-BAD no diff against %s (rc=%d)" % (base, names.returncode)
    body = git(portal, "diff", "-U0", base, "HEAD")
    if body.returncode != 0:
        return "R20-PP-DIFF-BAD cannot read the diff"
    added = [ln[1:] for ln in body.stdout.splitlines() if ln.startswith("+") and not ln.startswith("+++")]
    why = diff_problem(names.stdout.split(), added)
    return "R20-PP-DIFF-BAD %s" % why if why else "R20-PP-DIFF-OK %d files" % len(names.stdout.split())


def prod_tests(portal):
    bun = shutil.which("bun")
    if not bun:
        return "R20-PP-TESTS-BAD bun not on PATH"
    r = subprocess.run([bun, "test"] + TESTS, cwd=str(portal), capture_output=True, text=True, timeout=170)
    out = STRIP.sub("", r.stdout + r.stderr)
    passed = int((re.search(r"(\d+) pass", out) or [0, 0])[1])
    failed = int((re.search(r"(\d+) fail", out) or [0, 0])[1])
    if r.returncode != 0 or failed or passed < 11:
        return "R20-PP-TESTS-BAD rc=%d pass=%d fail=%d" % (r.returncode, passed, failed)
    return "R20-PP-TESTS-OK pass=%d" % passed


def selftest():
    good_names = sorted(ALLOWED)
    if diff_problem(good_names, ["const x = showsMeetingOutcome(t)"]) is not None:
        return "good fixture refused"
    if diff_problem(good_names + ["src/pages/TicketCenter/__tests__/trade-form-upload.test.tsx"], []) is None:
        return "an extra file was not caught"
    if diff_problem(good_names, ["import { TradeFormOpen } from './TradeRequestParts'"]) is None:
        return "TradeFormOpen was not caught"
    if diff_problem(good_names, ["<AnalysisPackageRow ticket={t} />"]) is None:
        return "AnalysisPackageRow was not caught"
    if diff_problem(sorted(ALLOWED - REQUIRED), []) is None:
        return "a missing required file was not caught"
    return None


def main(argv):
    if argv[:1] == ["--self-test"]:
        why = selftest()
        print("R20-PP-SELFTEST-OK" if why is None else "R20-PP-SELFTEST-FAIL " + why)
        return 0 if why is None else 1
    if len(argv) >= 3 and argv[0] == "prod-tests" and argv[1] == "--portal":
        out = prod_tests(argv[2])
    elif len(argv) >= 5 and argv[0] == "prod-diff" and argv[1] == "--portal" and argv[3] == "--base":
        out = prod_diff(argv[2], argv[4])
    else:
        print("usage: r20_pp_checks.py prod-diff --portal <dir> --base <ref> | prod-tests --portal <dir> | --self-test")
        return 2
    print(out)
    return 0 if "-OK" in out else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
