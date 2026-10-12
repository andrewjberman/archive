"""runc173_check.py -- the one mechanical check of IRPT_ANLREQ.TO-RUN-C173 (the one read-only run of the internal-callers census script).

Usage:  python runc173_check.py [--root <repo root>]

Prints RUNC173-OK when the result file is complete, adds up, and holds no address; otherwise one FAIL line per problem and RUNC173-FAIL.
It grades the record's FORM and arithmetic; it cannot see the users table.
"""
import json
import re
import sys
from pathlib import Path

RESULT = "org/tier2_senior/0.7.0_AE_CloudOps~AR2/deliverables/C173_INTERNAL_CALLERS_CENSUS.json"
PART_A = ("table", "items_scanned", "profile_rows", "internal_rows", "internal_active", "internal_by_firmId_userType_status",
          "external_rows", "unreadable_rows", "denominator_check")
FORBIDDEN = (r"@", r"https?://")


def main(argv):
    root = Path(argv[argv.index("--root") + 1]) if "--root" in argv else Path(__file__).resolve().parents[9]
    problems = []
    if not (root / ".tools").is_dir():
        problems.append("root %s is not the repository root" % root)
    path = root / RESULT
    if not path.is_file():
        problems.append("no %s" % RESULT)
    else:
        doc = json.loads(path.read_text(encoding="utf-8"))
        count = (doc.get("count") or {}).get("part_a") or {}
        for member in PART_A:
            if member not in count:
                problems.append("part_a lacks %r" % member)
        if not [p for p in problems if p.startswith("part_a")]:
            by_key = sum(row.get("rows", 0) for row in count["internal_by_firmId_userType_status"])
            if by_key != count["internal_rows"]:
                problems.append("the status table sums to %d, not internal_rows %d" % (by_key, count["internal_rows"]))
            if count["internal_rows"] + count["external_rows"] + count["unreadable_rows"] != count["profile_rows"]:
                problems.append("internal + external + unreadable does not equal profile_rows")
            if count["denominator_check"] is not True:
                problems.append("the script's own denominator check is not true")
            active_rows = sum(r.get("rows", 0) for r in count["internal_by_firmId_userType_status"] if r.get("status") == "active")
            if active_rows != count["internal_active"]:
                problems.append("rows with status active (%d) differ from internal_active (%d)" % (active_rows, count["internal_active"]))
            print("internal rows %d, exactly active %d, not active %d, unreadable %d" % (
                count["internal_rows"], count["internal_active"], count["internal_rows"] - count["internal_active"], count["unreadable_rows"]))
        for key in ("read_at", "script_blob", "identity_arn_tail"):
            if not doc.get(key):
                problems.append("the result lacks %r" % key)
        if (doc.get("count") or {}).get("part_b", {}).get("part_b") != "NOT_AVAILABLE":
            problems.append("part_b must read NOT_AVAILABLE (no log line carries the caller); never a number")
        if doc.get("claim") != "measured":
            problems.append("claim is not measured")
        if doc.get("writes_made") != []:
            problems.append("writes_made must be an empty list")
        body = json.dumps(doc)
        for pattern in FORBIDDEN:
            if re.search(pattern, body):
                problems.append("the result holds a string matching %s (an address or a link)" % pattern)
    for problem in problems:
        print("FAIL: %s" % problem)
    print("RUNC173-%s" % ("FAIL" if problems else "OK"))
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
