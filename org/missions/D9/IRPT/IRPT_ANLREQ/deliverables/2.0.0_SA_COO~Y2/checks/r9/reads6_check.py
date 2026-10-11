"""reads6_check.py -- the one mechanical check of IRPT_ANLREQ.TO-READS-Y6 (the laptop's job-row reads and ticket-id count).

Usage:  python reads6_check.py [--root <repo root>]

Prints READS6-OK when the result file is complete and consistent; otherwise one FAIL line per problem and READS6-FAIL.
It grades the record's FORM and arithmetic; it cannot see the tables. The default root is this file's repository root.
"""
import json
import re
import sys
from pathlib import Path

RESULT = "org/tier2_senior/0.7.0_AE_CloudOps~ANL/deliverables/Y6_job_rows_and_ticket_id_count.json"


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
        rows = doc.get("job_rows") or {}
        states = rows.get("states") or {}
        if rows.get("of") != 14 or len(states) != 14 or any(not re.fullmatch(r"REQ-[0-9a-f]{24}", k) for k in states):
            problems.append("job_rows.states does not hold exactly the 14 request ids")
        ready = sorted(k for k, v in states.items() if v == "READY")
        if rows.get("ready_count") != len(ready):
            problems.append("ready_count %r does not equal the %d ids whose state reads READY" % (rows.get("ready_count"), len(ready)))
        first = rows.get("first_ready")
        if (first is None) != (not ready) or (first is not None and states.get(first) != "READY"):
            problems.append("first_ready is not consistent with the states")
        count = doc.get("ticket_id_count") or {}
        parts = [count.get(k) for k in ("with_ticket_id", "without_ticket_id", "unreadable")]
        if any(not isinstance(x, int) for x in parts) or not isinstance(count.get("accepted_scanned"), int) \
                or sum(parts) != count.get("accepted_scanned"):
            problems.append("ticket_id_count parts do not add up to accepted_scanned")
        if doc.get("claim") != "measured":
            problems.append("claim is not measured")
        print("job rows read READY: %d of 14; ticket_id count %s of %s without" % (len(ready), count.get("without_ticket_id"),
                                                                                    count.get("accepted_scanned")))
    for problem in problems:
        print("FAIL: %s" % problem)
    print("READS6-%s" % ("FAIL" if problems else "OK"))
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
