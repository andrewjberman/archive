"""reads9_check.py -- the one mechanical check of IRPT_ANLREQ.TO-READS-Y9 (the laptop's count of stored inputs).

Usage:  python reads9_check.py [--root <repo root>]

Prints READS9-OK when the result file is complete, adds up, and holds no id, file name or address; otherwise one FAIL line per
problem and READS9-FAIL. It grades the record's FORM and arithmetic; it cannot see the table or the bucket.
"""
import json
import re
import sys
from pathlib import Path

RESULT = "org/tier2_senior/0.7.0_AE_CloudOps~ANL/deliverables/Y9_stored_input_count_r18.json"
MEMBERS = ("by_cause", "by_tenant", "inputs_by_lane", "items_scanned", "old_reader_differs", "read_at", "read_differently",
           "read_the_same", "template_inputs", "turned_back", "turned_back_with_a_report", "unreadable")
FORBIDDEN = (r"REQ-[0-9a-f]{24}", r"TCK-\d{8}-[0-9a-f]{8}", r"\.xlsx", r"\.csv", r"@", r"https?://", r"[0-9a-f]{32,}")
HASHES = ("script_blob", "new_reader_sha256", "old_reader_sha256")


def main(argv):
    root = Path(argv[argv.index("--root") + 1]) if "--root" in argv else Path(__file__).resolve().parents[9]
    problems = []
    if not (root / ".tools").is_dir():
        problems.append("root %s is not the repository root" % root)
    result = argv[argv.index("--result") + 1] if "--result" in argv else RESULT
    path = root / result
    if not path.is_file():
        problems.append("no %s" % result)
    else:
        doc = json.loads(path.read_text(encoding="utf-8"))
        count = doc.get("count") or {}
        missing = [member for member in MEMBERS if member not in count]
        for member in missing:
            problems.append("count lacks %r" % member)
        if not missing:
            unreadable = sum(count["unreadable"].values())
            if count["template_inputs"] != count["read_the_same"] + count["read_differently"] + unreadable:
                problems.append("template_inputs does not equal read_the_same + read_differently + unreadable")
            report = count["turned_back_with_a_report"]
            if report.get("with", 0) + report.get("without", 0) != count["turned_back"]:
                problems.append("with + without does not equal turned_back")
            if sum(count["inputs_by_lane"].values()) < count["template_inputs"]:
                problems.append("inputs_by_lane sums to less than template_inputs")
            print("template inputs %d: same %d, differently %d, unreadable %d; turned back %d (with a report %d)" % (
                count["template_inputs"], count["read_the_same"], count["read_differently"], unreadable, count["turned_back"],
                report.get("with", 0)))
        for key in HASHES + ("table", "bucket_how_resolved", "identity_arn_tail"):
            if not doc.get(key):
                problems.append("the result lacks %r" % key)
        if doc.get("claim") != "measured":
            problems.append("claim is not measured")
        if doc.get("writes_made") != []:
            problems.append("writes_made must be an empty list")
        body = json.dumps({key: value for key, value in doc.items() if key not in HASHES})
        for pattern in FORBIDDEN:
            if re.search(pattern, body):
                problems.append("the result holds a string matching %s (an id, a file name or an address)" % pattern)
    for problem in problems:
        print("FAIL: %s" % problem)
    print("READS9-%s" % ("FAIL" if problems else "OK"))
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
