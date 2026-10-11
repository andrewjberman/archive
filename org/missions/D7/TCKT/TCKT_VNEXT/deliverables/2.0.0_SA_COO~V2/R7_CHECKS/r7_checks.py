"""TCKT_VNEXT round 7 -- the issuer's mechanical checks (2.0.0_SA_COO~V2). Run from the worktree root.

  nr-refuse   R7-nr1-AC1  an internal caller with no users PROFILE row is refused, as a failed lookup is
  nr-regress  R7-nr1-AC2  the whole ticket service test folder passes (at least 201)
  el-read     R7-el1-AC1  the empty-firm-list read's findings file has its keys and every path it cites exists

Each prints <NAME>-OK <detail> or <NAME>-FAIL <reason>; exit 0/1. Every pytest call is bounded at 110 s.
"""
import json
import re
import subprocess
import sys
from pathlib import Path

TK_DIR = Path("infra/aws/lambda/ticket_center/tests")
NR_TESTS = TK_DIR / "test_no_row_refuses.py"
NR_ROW = ["test_internal_caller_with_no_profile_row_is_refused_on_every_scoped_route",
          "test_the_refusal_is_the_failed_lookup_answer_and_names_no_ticket",
          "test_internal_caller_with_a_row_and_no_firm_list_still_reads_every_firm",
          "test_internal_caller_with_a_row_and_an_empty_firm_list_still_reads_every_firm",
          "test_clients_and_service_subjects_are_not_touched_by_the_rule"]
NR_MIN = 201  # 196 at the round-7 base plus the 5 tests of TO-R7-nr1
EL_FILE = Path("org/missions/D7/TCKT/TCKT_VNEXT/deliverables/0.9.0_WK_TCKT_VNEXT~26/EMPTY_FIRM_LIST_READ.json")
EL_KEYS = {"question", "files_read", "surfaces", "where_the_three_surfaces_disagree", "what_was_not_read", "claim"}


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


def el_read():
    if not EL_FILE.exists():
        return False, "absent: %s" % EL_FILE.as_posix()
    try:
        doc = json.loads(EL_FILE.read_text(encoding="utf-8"))
    except ValueError as e:
        return False, "not JSON: %s" % e
    if not isinstance(doc, dict) or set(doc) != EL_KEYS:
        return False, "keys differ: missing %s extra %s" % (sorted(EL_KEYS - set(doc)), sorted(set(doc) - EL_KEYS))
    files = doc["files_read"]
    if not isinstance(files, list) or not files:
        return False, "files_read is empty"
    absent = [f for f in files if not isinstance(f, str) or not Path(f.split(":")[0]).exists()]
    if absent:
        return False, "cited path(s) absent: %s" % absent[:5]
    if not isinstance(doc["surfaces"], list) or len(doc["surfaces"]) < 3:
        return False, "surfaces must list at least three readers of allowedFirmIds"
    if doc["claim"] not in ("measured", "inferred"):
        return False, "claim must be measured or inferred"
    return True, "keys=%d files_read=%d surfaces=%d" % (len(doc), len(files), len(doc["surfaces"]))


CHECKS = {
    "nr-refuse": lambda: named(NR_TESTS, NR_ROW),
    "nr-regress": lambda: regress(TK_DIR, NR_MIN),
    "el-read": el_read,
}


def main(argv):
    if len(argv) != 1 or argv[0] not in CHECKS:
        print("usage: r7_checks.py " + "|".join(sorted(CHECKS)))
        return 2
    ok, why = CHECKS[argv[0]]()
    print("%s-%s %s" % (argv[0].upper(), "OK" if ok else "FAIL", why))
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
