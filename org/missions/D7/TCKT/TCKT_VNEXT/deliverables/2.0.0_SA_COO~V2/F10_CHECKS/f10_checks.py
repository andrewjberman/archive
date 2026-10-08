"""TCKT_VNEXT workstream F10 (FWD-6, PRD ADDENDUM 1) -- the issuer's mechanical checks (2.0.0_SA_COO~V2).

  f10-principal  F10-AC1  svc-commentary creates an analysis_request and nothing else; every other action denies it
  f10-fields     F10-AC2  draft_commentary + report_request_id are type data, stored for svc-commentary only, validated, kept out of the DL notice
  f10-security   F10-AC3  the 2026-08-12 finding stays closed on the write path: identity from the token never the body; no context denies
  f10-household  F10-l2-AC1  household optional for svc-commentary ONLY, declared as type data; humans still must answer; no placeholder stored
  f10-regress    F10-l2-AC2  the whole ticket_center tests directory passes (every pre-existing file, every F10 test)

Each named test must EXIST and PASS; a missing name is a FAIL, never a skip. Prints <TOKEN>-OK or <TOKEN>-FAIL <reason>,
exits 0 / 1. Run from the worktree root.
"""
import re
import subprocess
import sys
from pathlib import Path

TESTS = Path("infra/aws/lambda/ticket_center/tests/test_commentary_write.py")
TESTS_DIR = Path("infra/aws/lambda/ticket_center/tests")

NAMES = {
    "f10-principal": ["test_svc_commentary_creates_analysis_request", "test_svc_commentary_refused_other_types",
                      "test_svc_commentary_denied_every_other_action", "test_unknown_service_subject_still_unresolvable"],
    "f10-fields": ["test_draft_and_report_request_id_stored", "test_draft_fields_refused_for_internal_human",
                   "test_draft_status_must_be_draft", "test_draft_text_over_limit_refused", "test_draft_unknown_key_refused",
                   "test_draft_not_in_dl_notice", "test_draft_fields_declared_in_type_definition"],
    "f10-household": ["test_svc_commentary_household_optional", "test_human_household_still_required",
                      "test_household_optional_declared_in_type_definition", "test_svc_commentary_household_absent_stores_no_placeholder"],
    "f10-security": ["test_created_by_is_token_subject_not_body", "test_body_asserted_identity_ignored_on_create",
                     "test_no_authorizer_context_denied", "test_firm_outside_allowed_refused_for_svc_commentary"],
    "f10-package-auth": ["test_package_written_by_named_principal", "test_package_principal_empty_refuses_everyone",
                         "test_package_refused_for_humans_and_svc_commentary", "test_package_principal_read_from_type_definition"],
    "f10-package-rules": ["test_package_refused_other_type", "test_package_refused_completed_ticket", "test_package_refused_firm_mismatch",
                          "test_package_second_write_needs_prior_attached_at", "test_package_refuses_extra_or_empty_field",
                          "test_package_not_in_dl_notice"],
}
PACKAGE_TESTS = Path("infra/aws/lambda/ticket_center/tests/test_package_route.py")


def _pytest(names, tests=TESTS):
    TESTS = tests
    if not TESTS.exists():
        return False, "absent: %s" % TESTS.as_posix()
    src = TESTS.read_text(encoding="utf-8")
    missing = [n for n in names if not re.search(r"^\s*def %s\(" % re.escape(n), src, re.M)]
    if missing:
        return False, "missing test(s): %s" % ", ".join(missing)
    cmd = [sys.executable, "-m", "pytest", "-q", "-p", "no:cacheprovider", TESTS.as_posix(), "-k", " or ".join(names)]
    r = subprocess.run(cmd, capture_output=True, text=True, timeout=170)
    out = re.sub(r"\x1b\[[0-9;]*m", "", r.stdout + r.stderr)
    passed = int((re.search(r"(\d+) passed", out) or [0, 0])[1])
    if r.returncode != 0 or passed < len(names):
        tail = [ln for ln in out.splitlines() if ln.strip()][-1:] or [""]
        return False, "rc=%d passed=%d of %d %s" % (r.returncode, passed, len(names), tail[0])
    return True, "passed=%d" % passed


def _regress():
    cmd = [sys.executable, "-m", "pytest", "-q", "-p", "no:cacheprovider", TESTS_DIR.as_posix()]
    r = subprocess.run(cmd, capture_output=True, text=True, timeout=170)
    out = re.sub(r"\x1b\[[0-9;]*m", "", r.stdout + r.stderr)
    passed = int((re.search(r"(\d+) passed", out) or [0, 0])[1])
    failed = int((re.search(r"(\d+) failed", out) or [0, 0])[1])
    if r.returncode != 0 or failed or passed < 104:
        return False, "rc=%d passed=%d failed=%d (floor 104)" % (r.returncode, passed, failed)
    return True, "passed=%d failed=0" % passed


def main(argv):
    subs = list(NAMES) + ["f10-regress"]
    if not argv or argv[0] not in subs:
        print("usage: f10_checks.py {%s}" % "|".join(subs))
        return 2
    sub = argv[0]
    token = sub.upper()
    if sub == "f10-regress":
        ok, why = _regress()
    else:
        ok, why = _pytest(NAMES[sub], PACKAGE_TESTS if sub.startswith("f10-package") else TESTS)
    print("%s-%s %s" % (token, "OK" if ok else "FAIL", why))
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
