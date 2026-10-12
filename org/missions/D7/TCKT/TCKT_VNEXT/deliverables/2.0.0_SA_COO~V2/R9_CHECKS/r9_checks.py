"""TCKT_VNEXT round 9 -- the issuer's mechanical checks (2.0.0_SA_COO~V2). Run from the worktree root.

  st-active   R9-st1-AC1  an internal caller whose PROFILE row is not status 'active' is refused, as a failed lookup is
  st-regress  R9-st1-AC2  the whole ticket service test folder passes (at least 206)
  ct-count    (applier)   the count file has its totals, they sum, and it holds no address

Each prints <NAME>-OK <detail> or <NAME>-FAIL <reason>; exit 0/1. Every pytest call is bounded at 110 s.
"""
import json
import re
import subprocess
import sys
from pathlib import Path

TK_DIR = Path("infra/aws/lambda/ticket_center/tests")
ST_TESTS = TK_DIR / "test_status_active.py"
ST_ROW = ["test_internal_caller_with_a_disabled_row_is_refused_on_every_scoped_route",
          "test_a_row_with_no_status_or_an_unseen_status_is_refused",
          "test_the_refusal_is_the_failed_lookup_answer_and_its_log_line_carries_no_address",
          "test_an_active_row_keeps_every_firm_list_behaviour",
          "test_clients_and_service_subjects_are_not_touched_by_the_status_rule"]
ST_MIN = 206  # 201 at the round-9 base plus the 5 tests of TO-R9-st1
CT_FILE = Path("org/tier2_senior/0.7.0_AE_CloudOps~TV2/deliverables/r9_ct1/ACTIVE_INTERNAL_ROWS_BY_DOMAIN_20261012.json")
CT_KEYS = {"active_internal_rows", "on_an_opal_domain", "on_a_non_opal_domain"}


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


def ct_count():
    if not CT_FILE.exists():
        return False, "absent: %s" % CT_FILE.as_posix()
    raw = CT_FILE.read_text(encoding="utf-8")
    if "@" in raw:
        return False, "the file holds an address"
    try:
        doc = json.loads(raw)
    except ValueError as e:
        return False, "not JSON: %s" % e
    t = doc.get("totals") or {}
    if not CT_KEYS <= set(t):
        return False, "totals missing %s" % sorted(CT_KEYS - set(t))
    if t["active_internal_rows"] != t["on_an_opal_domain"] + t["on_a_non_opal_domain"]:
        return False, "the two domain counts do not sum to active_internal_rows"
    if not isinstance(doc.get("opal_domains_used"), list) or not doc["opal_domains_used"]:
        return False, "opal_domains_used must list the domains counted as Opal's"
    return True, "active_internal=%d opal=%d non_opal=%d" % (
        t["active_internal_rows"], t["on_an_opal_domain"], t["on_a_non_opal_domain"])


CHECKS = {
    "st-active": lambda: named(ST_TESTS, ST_ROW),
    "st-regress": lambda: regress(TK_DIR, ST_MIN),
    "ct-count": ct_count,
}


def main(argv):
    if len(argv) != 1 or argv[0] not in CHECKS:
        print("usage: r9_checks.py " + "|".join(sorted(CHECKS)))
        return 2
    ok, why = CHECKS[argv[0]]()
    print("%s-%s %s" % (argv[0].upper(), "OK" if ok else "FAIL", why))
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
