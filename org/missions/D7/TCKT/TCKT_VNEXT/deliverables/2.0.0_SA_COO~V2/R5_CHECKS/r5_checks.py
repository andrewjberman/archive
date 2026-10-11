"""TCKT_VNEXT round 5 -- the issuer's mechanical checks (2.0.0_SA_COO~V2). Run from the worktree root.

  ml-digest   R5-ml1-AC1  the client mail log lines carry a digest of the recipient and never the address
  ml-regress  R5-ml1-AC2  the whole ticket service test folder passes (at least 178)
  fn-fence    R5-fn1-AC1  another firm's caller is refused on a ticket, the list and the report record
  fn-regress  R5-fn1-AC2  the whole ticket service test folder passes (at least 179)
  c6-fields   R5-c61-AC1  the commentary draft lands on the existing ticket; the ticket records who sent the final commentary
  c6-regress  R5-c61-AC2  the whole ticket service test folder passes (at least 190)
  cm2-lines   R5-cm2-AC1  the draft route does not say which ticket ids exist; the client notice list names three members
  cm2-regress R5-cm2-AC2  the whole ticket service test folder passes (at least 192)
  cm3-match   R5-cm3-AC1  a draft lands only on the ticket whose own record names that request
  cm3-regress R5-cm3-AC2  the whole ticket service test folder passes (at least 196)
  pc2-classes R5-pc2-AC1  the clamp precheck lists every ticket handler the deployed code dispatches, each with a class
  pc2-regress R5-pc2-AC2  the whole precheck test file passes (at least 21)
  ac-read     R5-ac1-AC1  the one-account read's findings file has its keys and every path it cites exists

Each prints <NAME>-OK <detail> or <NAME>-FAIL <reason>; exit 0/1. Every pytest call is bounded at 110 s.
"""
import json
import re
import subprocess
import sys
from pathlib import Path

TK_DIR = Path("infra/aws/lambda/ticket_center/tests")
ML_TESTS = TK_DIR / "test_client_mail_digest.py"
ML_ROW = ["test_sent_line_carries_the_recipient_digest_and_not_the_address",
          "test_send_failed_line_carries_the_digest_and_no_error_text_with_the_address",
          "test_digest_is_the_same_for_the_same_address_in_any_case"]
ML_MIN = 178  # 175 at the round-5 base plus the 3 tests of TO-R5-ml1
FN_TESTS = TK_DIR / "test_fence_other_firm.py"
FN_ROW = ["test_client_of_another_firm_cannot_get_the_ticket",
          "test_client_of_another_firm_does_not_see_it_in_the_list",
          "test_caller_scoped_to_another_firm_cannot_record_a_report_as_creator",
          "test_refusals_return_no_field_of_the_other_firms_ticket"]
FN_MIN = 179  # 175 at the round-5 base plus the 4 tests of TO-R5-fn1
C6_TESTS = TK_DIR / "test_commentary_same_ticket.py"
C6_ROW = ["test_commentary_service_sets_the_draft_on_the_existing_ticket",
          "test_draft_on_a_ticket_of_a_firm_off_the_list_is_refused",
          "test_draft_is_written_once",
          "test_only_the_commentary_service_may_set_the_draft",
          "test_internal_caller_records_commentary_sent_and_the_server_stamps_who_and_when",
          "test_commentary_sent_is_written_once_and_takes_no_body_field",
          "test_commentary_sent_outside_the_callers_firm_scope_is_refused"]
C6_MIN = 190  # 183 at the base of TO-R5-c61 plus its 7 tests
CM2_ROW = ["test_draft_route_gives_the_same_deny_for_a_missing_ticket_and_an_off_list_firm",
           "test_client_notice_prohibited_names_the_commentary_members_and_the_package"]
CM2_MIN = 192  # 190 at the base of TO-R5-cm2 plus its 2 tests
CM3_ROW = ["test_draft_is_accepted_only_when_the_tickets_recorded_request_id_matches",
           "test_draft_for_another_request_gets_the_one_deny",
           "test_draft_on_a_ticket_with_no_recorded_request_gets_the_one_deny",
           "test_draft_body_must_carry_a_wellformed_request_id"]
CM3_MIN = 196  # 192 at the base of TO-R5-cm3 plus its 4 tests
PC2_TESTS = Path("org/missions/D7/TCKT/TCKT_VNEXT/deliverables/0.9.0_WK_TCKT_VNEXT~13/clamp_precheck/test_clamp_precheck.py")
PC2_ROW = ["test_every_dispatched_ticket_handler_is_listed_with_a_class",
           "test_a_handler_that_calls_a_clamp_helper_is_classed_profile_scope",
           "test_the_two_commentary_handlers_are_listed_and_classed",
           "test_a_dispatched_handler_with_no_class_makes_the_exit_nonzero",
           "test_the_read27_line_and_its_table_rows_are_unchanged"]
PC2_MIN = 21  # 16 at the base of TO-R5-pc2 plus its 5 tests
AC_FILE = Path("org/missions/D7/TCKT/TCKT_VNEXT/deliverables/0.9.0_WK_TCKT_VNEXT~20/ONE_ACCOUNT_CHECK_READ.json")
AC_KEYS = {"question", "files_read", "where_an_account_is_named_in_an_uploaded_file", "can_the_door_count_accounts_today",
           "where_the_check_can_live", "what_was_not_read", "claim"}


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


def ac_read():
    if not AC_FILE.exists():
        return False, "absent: %s" % AC_FILE.as_posix()
    try:
        doc = json.loads(AC_FILE.read_text(encoding="utf-8"))
    except ValueError as e:
        return False, "not JSON: %s" % e
    if not isinstance(doc, dict) or set(doc) != AC_KEYS:
        return False, "keys differ: missing %s extra %s" % (sorted(AC_KEYS - set(doc)), sorted(set(doc) - AC_KEYS))
    files = doc["files_read"]
    if not isinstance(files, list) or not files:
        return False, "files_read is empty"
    absent = [f for f in files if not isinstance(f, str) or not Path(f.split(":")[0]).exists()]
    if absent:
        return False, "cited path(s) absent: %s" % absent[:5]
    if doc["claim"] not in ("measured", "inferred"):
        return False, "claim must be measured or inferred"
    return True, "keys=%d files_read=%d all present" % (len(doc), len(files))


CHECKS = {
    "ml-digest": lambda: named(ML_TESTS, ML_ROW),
    "ml-regress": lambda: regress(TK_DIR, ML_MIN),
    "fn-fence": lambda: named(FN_TESTS, FN_ROW),
    "fn-regress": lambda: regress(TK_DIR, FN_MIN),
    "ac-read": ac_read,
    "c6-fields": lambda: named(C6_TESTS, C6_ROW),
    "c6-regress": lambda: regress(TK_DIR, C6_MIN),
    "cm2-lines": lambda: named(C6_TESTS, CM2_ROW),
    "cm2-regress": lambda: regress(TK_DIR, CM2_MIN),
    "cm3-match": lambda: named(C6_TESTS, CM3_ROW),
    "cm3-regress": lambda: regress(TK_DIR, CM3_MIN),
    "pc2-classes": lambda: named(PC2_TESTS, PC2_ROW),
    "pc2-regress": lambda: regress(PC2_TESTS, PC2_MIN),
}


def main(argv):
    if len(argv) != 1 or argv[0] not in CHECKS:
        print("usage: r5_checks.py " + "|".join(sorted(CHECKS)))
        return 2
    ok, why = CHECKS[argv[0]]()
    print("%s-%s %s" % (argv[0].upper(), "OK" if ok else "FAIL", why))
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
