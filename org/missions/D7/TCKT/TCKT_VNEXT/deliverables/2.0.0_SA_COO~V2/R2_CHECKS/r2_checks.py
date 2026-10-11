"""TCKT_VNEXT round 2 -- the issuer's mechanical checks (2.0.0_SA_COO~V2). Run from the worktree root.

  rn-submit-id  R2-rn1-AC1  the runner polls the id the submission answered, or the firm's request list; never a value it sent
  rn-stage      R2-rn1-AC2  the runner reads the contract field `stage`, bounded, and records a terminal stage as a result
  rn-ticket     R2-rn1-AC3  the runner records a REQ id on the ticket and opens the report from the ticket's report_ref
  rr-shape      R2-rr1-AC1  the report route stores a well-formed REQ id and refuses a malformed one with a typed code
  ts-guard      R2-ts1-AC1  by default no ticket_center test can reach a real SES send or a real users-table read
  pg-open       R2-pg1-AC1  (needs --portal <dir>) the ticket's Open report reads the finished report; a stated waiting state
  pg-existing   R2-pg1-AC2  (needs --portal <dir>) the existing TicketCenter analysis-request tests still pass
  tc-regress    R2-rr1-AC2 / R2-ts1-AC2  the whole ticket_center/tests directory passes (at least MIN_PASSED, 0 failed)

Each prints <NAME>-OK <detail> or <NAME>-FAIL <reason>; exit 0/1. Every pytest call is bounded at 110 s.
"""
import re
import subprocess
import sys
from pathlib import Path

TC_TESTS = Path("infra/aws/lambda/ticket_center/tests")
RUNNER_TESTS = Path("org/missions/D7/TCKT/TCKT_VNEXT/deliverables/0.9.0_WK_TCKT_VNEXT~8/fwd1_runner/test_fwd1_runner.py")
MIN_PASSED = 147  # the directory's count at the round-2 base (box/dell2, 2026-10-11), read by this check

NAMED = {
    "rn-submit-id": (RUNNER_TESTS, ["test_polls_id_from_submit_answer", "test_falls_back_to_request_list_when_answer_has_no_id",
                                    "test_never_polls_the_sent_token", "test_ambiguous_request_list_is_a_named_failure"]),
    "rn-stage": (RUNNER_TESTS, ["test_reads_stage_field_until_generated", "test_failed_stage_is_recorded_not_retried",
                                "test_poll_budget_is_bounded", "test_refusal_envelope_is_not_a_read"]),
    "rn-ticket": (RUNNER_TESTS, ["test_records_req_id_on_ticket", "test_opens_report_from_ticket_report_ref",
                                 "test_never_records_a_non_req_id"]),
    "rr-shape": (TC_TESTS / "test_report_ref_shape.py", ["test_well_formed_request_id_stored", "test_malformed_request_id_refused_typed",
                                                         "test_sent_token_shape_refused", "test_refusal_writes_nothing"]),
    "ts-guard": (TC_TESTS / "test_no_real_aws.py", ["test_ses_send_is_guarded_by_default", "test_users_table_read_is_guarded_by_default",
                                                    "test_a_test_can_still_install_its_own_stub"]),
}


def _run(args):
    r = subprocess.run([sys.executable, "-m", "pytest", "-q", "-p", "no:cacheprovider"] + args,
                       capture_output=True, text=True, timeout=110)
    out = re.sub(r"\x1b\[[0-9;]*m", "", r.stdout + r.stderr)
    passed = int((re.search(r"(\d+) passed", out) or [0, 0])[1])
    failed = int((re.search(r"(\d+) failed", out) or [0, 0])[1])
    errors = int((re.search(r"(\d+) error", out) or [0, 0])[1])
    return r.returncode, passed, failed, errors


def named(key):
    path, names = NAMED[key]
    if not path.exists():
        return False, "absent: %s" % path.as_posix()
    src = path.read_text(encoding="utf-8")
    missing = [n for n in names if not re.search(r"^\s*def %s\(" % re.escape(n), src, re.M)]
    if missing:
        return False, "missing test(s): %s" % ", ".join(missing)
    rc, passed, failed, errors = _run([path.as_posix(), "-k", " or ".join(names)])
    if rc != 0 or passed < len(names) or failed or errors:
        return False, "rc=%d passed=%d of %d failed=%d errors=%d" % (rc, passed, len(names), failed, errors)
    return True, "passed=%d of %d" % (passed, len(names))


def regress():
    rc, passed, failed, errors = _run([TC_TESTS.as_posix()])
    if rc != 0 or failed or errors or passed < MIN_PASSED:
        return False, "rc=%d passed=%d (min %d) failed=%d errors=%d" % (rc, passed, MIN_PASSED, failed, errors)
    return True, "passed=%d (min %d) failed=0" % (passed, MIN_PASSED)


PG_NEW = "src/pages/TicketCenter/__tests__/open-report.test.tsx"
PG_OLD = "src/pages/TicketCenter/__tests__/analysis-request.test.tsx"
PG_NAMES = ["open report reads the finished report, not the request record",
            "a report not yet generated shows a stated waiting state",
            "a request record is never presented as the report"]


def bun(portal, rel, names):
    import shutil
    root = Path(portal)
    f = root / rel
    if not f.exists():
        return False, "absent: %s" % rel
    src = f.read_text(encoding="utf-8")
    missing = [n for n in names if n not in src]
    if missing:
        return False, "missing test(s): %s" % "; ".join(missing)
    exe = shutil.which("bun")
    if not exe:
        return False, "bun not on PATH"
    r = subprocess.run([exe, "test", rel], cwd=str(root), capture_output=True, text=True, timeout=110)
    out = re.sub(r"\[[0-9;]*m", "", r.stdout + r.stderr)
    passed = int((re.search(r"(\d+) pass", out) or [0, 0])[1])
    failed = int((re.search(r"(\d+) fail", out) or [0, 0])[1])
    if r.returncode != 0 or failed or passed < max(1, len(names)):
        return False, "rc=%d pass=%d fail=%d" % (r.returncode, passed, failed)
    return True, "pass=%d fail=0" % passed


def main(argv):
    if argv and argv[0] in ("pg-open", "pg-existing"):
        if len(argv) != 3 or argv[1] != "--portal":
            print("%s-FAIL --portal <dir> required" % argv[0].upper())
            return 1
        ok, why = bun(argv[2], PG_NEW, PG_NAMES) if argv[0] == "pg-open" else bun(argv[2], PG_OLD, [])
        print("%s-%s %s" % (argv[0].upper(), "OK" if ok else "FAIL", why))
        return 0 if ok else 1
    if len(argv) != 1 or (argv[0] not in NAMED and argv[0] != "tc-regress"):
        print("usage: r2_checks.py {%s|tc-regress}" % "|".join(sorted(NAMED)))
        return 2
    ok, why = regress() if argv[0] == "tc-regress" else named(argv[0])
    print("%s-%s %s" % (argv[0].upper(), "OK" if ok else "FAIL", why))
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
