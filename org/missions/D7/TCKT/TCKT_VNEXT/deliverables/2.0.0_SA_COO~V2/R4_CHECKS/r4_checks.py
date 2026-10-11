"""TCKT_VNEXT round 4 -- the issuer's mechanical checks (2.0.0_SA_COO~V2). Run from the worktree root.

  pk-env      R4-pk1-AC1  the package door binds the packager's firms from an env list; two creator refusals carry codes
  pk-regress  R4-pk1-AC2  the whole ticket service test folder passes (at least 175)
  la-arms     R4-la1-AC1  the runner's arms-only mode sends no submission and runs the two arms
  la-regress  R4-la1-AC2  the whole runner test file passes (at least 61)
  os-mode     R4-rn2-AC1  the runner's one-step mode makes the form's four calls and at most one submission
  os-regress  R4-rn2-AC2  the whole runner test file passes (at least 68)

Each prints <NAME>-OK <detail> or <NAME>-FAIL <reason>; exit 0/1. Every pytest call is bounded at 110 s.
"""
import re
import subprocess
import sys
from pathlib import Path

PK_DIR = Path("infra/aws/lambda/ticket_center/tests")
PK_TESTS = PK_DIR / "test_package_env_firms.py"
PK_ROW = ["test_packager_with_firm_in_env_list_is_admitted_without_a_profile_row",
          "test_packager_with_firm_not_in_env_list_is_denied",
          "test_empty_or_unset_env_list_admits_nothing",
          "test_all_is_not_a_wildcard_in_the_env_list",
          "test_creator_on_completed_ticket_gets_coded_refusal",
          "test_creator_on_ticket_without_attachment_gets_coded_refusal"]
PK_MIN_PASSED = 175  # 169 at the base of TO-R4-pk1 plus its 6 tests

LA_TESTS = Path("org/missions/D7/TCKT/TCKT_VNEXT/deliverables/0.9.0_WK_TCKT_VNEXT~8/fwd1_runner/test_fwd1_runner.py")
LA_ROW = ["test_arms_only_sends_no_submission", "test_arms_only_runs_the_malformed_id_arm_and_records_400",
          "test_arms_only_runs_the_package_denial_arm", "test_arms_only_deletes_the_row_after_exp_and_exits_0",
          "test_arms_only_unexpected_arm_answer_is_a_named_failure_and_exits_1"]
LA_MIN_PASSED = 61  # 56 at the base of TO-R4-la1 plus its 5 tests

OS_ROW = ["test_one_step_creates_the_ticket_with_the_i1_source_and_never_claims",
          "test_one_step_submission_carries_ticket_id_and_the_tckt_request_id",
          "test_one_step_runs_both_arms_before_the_submission",
          "test_one_step_package_door_2xx_stops_before_the_submission",
          "test_one_step_records_as_creator_then_repeat_is_409",
          "test_one_step_sends_exactly_one_submission_even_on_timeout",
          "test_one_step_accepted_leaves_the_row_and_exits_3"]
OS_MIN_PASSED = 68  # 61 at the base of TO-R4-rn2 plus its 7 tests


def _pytest(args):
    r = subprocess.run([sys.executable, "-m", "pytest", "-q", "-p", "no:cacheprovider"] + args,
                       capture_output=True, text=True, timeout=110)
    out = re.sub(r"\x1b\[[0-9;]*m", "", r.stdout + r.stderr)
    passed = int((re.search(r"(\d+) passed", out) or [0, 0])[1])
    failed = int((re.search(r"(\d+) failed", out) or [0, 0])[1])
    errors = int((re.search(r"(\d+) error", out) or [0, 0])[1])
    return r.returncode, passed, failed, errors


def named(tests, names):
    if not tests.exists():
        return False, "absent: %s" % tests.as_posix()
    src = tests.read_text(encoding="utf-8")
    missing = [n for n in names if not re.search(r"^\s*def %s\(" % re.escape(n), src, re.M)]
    if missing:
        return False, "missing test(s): %s" % ", ".join(missing)
    rc, passed, failed, errors = _pytest([tests.as_posix(), "-k", " or ".join(names)])
    if rc != 0 or passed < len(names) or failed or errors:
        return False, "rc=%d passed=%d of %d failed=%d errors=%d" % (rc, passed, len(names), failed, errors)
    return True, "passed=%d of %d" % (passed, len(names))


def regress(target, minimum):
    rc, passed, failed, errors = _pytest([target.as_posix()])
    if rc != 0 or failed or errors or passed < minimum:
        return False, "rc=%d passed=%d (min %d) failed=%d errors=%d" % (rc, passed, minimum, failed, errors)
    return True, "passed=%d (min %d) failed=0" % (passed, minimum)


CHECKS = {
    "pk-env": lambda: named(PK_TESTS, PK_ROW),
    "pk-regress": lambda: regress(PK_DIR, PK_MIN_PASSED),
    "la-arms": lambda: named(LA_TESTS, LA_ROW),
    "la-regress": lambda: regress(LA_TESTS, LA_MIN_PASSED),
    "os-mode": lambda: named(LA_TESTS, OS_ROW),
    "os-regress": lambda: regress(LA_TESTS, OS_MIN_PASSED),
}


def main(argv):
    if len(argv) != 1 or argv[0] not in CHECKS:
        print("usage: r4_checks.py " + "|".join(sorted(CHECKS)))
        return 2
    ok, why = CHECKS[argv[0]]()
    print("%s-%s %s" % (argv[0].upper(), "OK" if ok else "FAIL", why))
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
