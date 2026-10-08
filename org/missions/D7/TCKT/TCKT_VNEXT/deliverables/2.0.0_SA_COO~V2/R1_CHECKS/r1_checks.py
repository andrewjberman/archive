"""TCKT_VNEXT round 1 -- the issuer's mechanical checks (2.0.0_SA_COO~V2), one subcommand per criterion.

  l1-types     TV1-l1-AC1  the four existing types unchanged; analysis_request created with answers + attachment; bad bodies refused
  l1-selfclaim TV1-l1-AC2  the requester claims and completes their own ticket; a non-holder still cannot complete
  l1-report    TV1-l1-AC3  the assignee writes report_ref on an in_progress ticket with an attachment; every other caller/state refused
  p1-file      TV1-p1-AC1  the form files only on NORMALIZED, with answers + the door's input_id; NEEDS_CORRECTION shows findings, files nothing
  p1-report    TV1-p1-AC2  from a held ticket: analysis requested with the ticket's input_id, request_id written back, report opens from the ticket

Each named test below must EXIST and PASS; a missing name is a FAIL, never a skip. Each subcommand prints <TOKEN>-OK or
<TOKEN>-FAIL <reason> and exits 0 / 1. Run the l1-* subcommands from the workspace worktree root; the p1-* subcommands take
--portal <portal worktree root>.
"""
import re
import shutil
import subprocess
import sys
from pathlib import Path

L_TESTS = Path("infra/aws/lambda/ticket_center/tests/test_analysis_request.py")
P_TEST = Path("src/pages/TicketCenter/__tests__/analysis-request.test.tsx")

NAMES = {
    "l1-types": ["test_four_existing_types_unchanged", "test_analysis_request_created_with_answers_and_attachment",
                 "test_analysis_request_refuses_unknown_answer", "test_analysis_request_refuses_missing_required",
                 "test_analysis_request_refuses_bad_input_id", "test_analysis_request_refuses_missing_attachment"],
    "l1-selfclaim": ["test_requester_claims_and_completes_own_ticket", "test_non_holder_cannot_complete"],
    "l1-report": ["test_report_ref_written_by_assignee", "test_report_ref_refused_for_non_assignee",
                  "test_report_ref_refused_when_open", "test_report_ref_refused_without_attachment",
                  "test_report_ref_refuses_extra_field"],
    "p1-file": ["files only on NORMALIZED with answers and input_id", "NEEDS_CORRECTION shows findings and files nothing"],
    "p1-report": ["requests the report with the ticket input_id and writes request_id back", "opens the report from the ticket"],
}


def _pytest(names):
    if not L_TESTS.exists():
        return False, "absent: %s" % L_TESTS.as_posix()
    src = L_TESTS.read_text(encoding="utf-8")
    missing = [n for n in names if not re.search(r"^\s*def %s\(" % re.escape(n), src, re.M)]
    if missing:
        return False, "missing test(s): %s" % ", ".join(missing)
    cmd = [sys.executable, "-m", "pytest", "-q", "-p", "no:cacheprovider", L_TESTS.as_posix(), "-k", " or ".join(names)]
    r = subprocess.run(cmd, capture_output=True, text=True, timeout=170)
    out = re.sub(r"\x1b\[[0-9;]*m", "", r.stdout + r.stderr)
    passed = int((re.search(r"(\d+) passed", out) or [0, 0])[1])
    if r.returncode != 0 or passed < len(names):
        tail = [ln for ln in out.splitlines() if ln.strip()][-1:] or [""]
        return False, "rc=%d passed=%d of %d %s" % (r.returncode, passed, len(names), tail[0])
    return True, "passed=%d" % passed


def _bun(names, portal):
    root = Path(portal)
    test = root / P_TEST
    if not test.exists():
        return False, "absent: %s" % test.as_posix()
    src = test.read_text(encoding="utf-8")
    missing = [n for n in names if ("'%s'" % n) not in src and ('"%s"' % n) not in src]
    if missing:
        return False, "missing test(s): %s" % ", ".join(missing)
    bun = shutil.which("bun")
    if not bun:
        return False, "bun not on PATH"
    pattern = "|".join(re.escape(n) for n in names)
    r = subprocess.run([bun, "test", P_TEST.as_posix(), "-t", pattern], cwd=str(root), capture_output=True, text=True,
                       timeout=170)
    out = re.sub(r"\x1b\[[0-9;]*m", "", r.stdout + r.stderr)
    passed = int((re.search(r"(\d+) pass", out) or [0, 0])[1])
    failed = int((re.search(r"(\d+) fail", out) or [0, 0])[1])
    if r.returncode != 0 or failed or passed < len(names):
        return False, "rc=%d pass=%d fail=%d of %d" % (r.returncode, passed, failed, len(names))
    return True, "pass=%d" % passed


def main(argv):
    if not argv or argv[0] not in NAMES:
        print("usage: r1_checks.py {%s} [--portal <dir>]" % "|".join(NAMES))
        return 2
    sub = argv[0]
    token = "TV1-" + sub.upper().replace("-", "-")
    if sub.startswith("p1-"):
        if "--portal" not in argv:
            print("%s-FAIL --portal <dir> required" % token)
            return 1
        ok, why = _bun(NAMES[sub], argv[argv.index("--portal") + 1])
    else:
        ok, why = _pytest(NAMES[sub])
    print("%s-%s %s" % (token, "OK" if ok else "FAIL", why))
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
