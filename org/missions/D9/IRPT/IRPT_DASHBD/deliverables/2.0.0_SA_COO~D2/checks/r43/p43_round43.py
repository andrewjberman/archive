"""IRPT_DASHBD round 43 (issuer 2.0.0_SA_COO~D2) -- 1.0.0_SA_CTO~DELL2's ADDENDUM 10.1 (msg 3257): re-cut DB-b-85's statement runner onto
IRPT_BCKEND's owned read IB-pr-405 (persist_inputs), so run / verify-submission / verify-persisted never touch irpt-requests directly.

Cell: DB-b-89.

Usage: python <this file> <repo_root> <criterion_id>; prints "<id> PASS" or "<id> FAIL" last.
  DB43-1-AC1  data/assets/scripts/gold/irpt_custody/e2a_real_statement.py at HEAD holds 0 direct table clients: no "irpt-requests", no
              "dynamodb", no ".get_item(", no ".query(" and no "Table(" (comment lines excluded).
  DB43-1-AC2  ~64/RUNNER_RECUT.json tests {passed > 0, failed == 0, fixture_test "<file>::<function>"} with that function defined at HEAD and
              fixture an existing file; the record's table_access_removed is true (the fixture run had no irpt-requests access).
"""
import json
import re
import sys
from pathlib import Path

SCRIPT = "data/assets/scripts/gold/irpt_custody/e2a_real_statement.py"
REC = "org/missions/D9/IRPT/IRPT_DASHBD/deliverables/0.9.0_WK_IRPT_DASHBD~64/RUNNER_RECUT.json"
BANNED = [r"irpt-requests", r"dynamodb", r"\.get_item\(", r"\.query\(", r"\bTable\("]


def main():
    root = Path(sys.argv[1] if len(sys.argv) > 1 else ".").resolve()
    cid = sys.argv[2] if len(sys.argv) > 2 else ""

    def fail(msg):
        print("FAIL: " + msg)
        print("%s FAIL" % (cid or "DB43"))
        sys.exit(1)

    if cid == "DB43-1-AC1":
        p = root / SCRIPT
        if not p.is_file():
            fail("no %s" % SCRIPT)
        code = [ln for ln in p.read_text(encoding="utf-8").splitlines() if not ln.lstrip().startswith("#")]
        hits = [(i + 1, b) for i, ln in enumerate(code) for b in BANNED if re.search(b, ln)]
        if hits:
            fail("%d direct table reference(s): %r" % (len(hits), hits[:5]))
        print("OK: 0 direct table clients in %s (%d code lines)" % (SCRIPT, len(code)))
    elif cid == "DB43-1-AC2":
        p = root / REC
        if not p.is_file():
            fail("no %s" % REC)
        r = json.loads(p.read_bytes().decode("utf-8"))
        t = r.get("tests") or {}
        m = re.fullmatch(r"([^:]+\.py)::(\w+)", str(t.get("fixture_test") or ""))
        if not isinstance(t.get("passed"), int) or t["passed"] <= 0 or t.get("failed") != 0 or not m or not (root / m.group(1)).is_file() \
                or not re.search(r"^def %s\(" % re.escape(m.group(2)), (root / m.group(1)).read_text(encoding="utf-8"), re.M):
            fail("tests %r" % t)
        if not (root / str(r.get("fixture") or "")).is_file() or r.get("table_access_removed") is not True:
            fail("fixture %r / table_access_removed %r" % (r.get("fixture"), r.get("table_access_removed")))
        print("OK: %d passed, fixture run %s with irpt-requests access removed" % (t["passed"], t["fixture_test"]))
    else:
        fail("unknown criterion %r" % cid)
    print("%s PASS" % cid)


if __name__ == "__main__":
    main()
