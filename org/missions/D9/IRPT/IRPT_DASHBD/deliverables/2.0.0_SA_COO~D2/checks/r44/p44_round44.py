"""IRPT_DASHBD round 44 (issuer 2.0.0_SA_COO~D2) -- 1.0.0_SA_CTO~DELL2's ADDENDUM 11 (msg 3288; CVO ADJUDICATION_v25 @5f365678bf): three riders
whose host cells (DB-b-87, DB-b-89) are already complete.

Cells: DB-b-90 the realized-lot uniqueness check on the FINAL rows, after every rewrite (W62-S1); DB-b-91 a skipped lots day STATED as
"lots not computed for <date>: <reason>", never an empty table (S40); DB-b-92 verify-persisted checks the persisted object's sha256 (W64-S1).

Usage: python <this file> <repo_root> <criterion_id>; prints "<id> PASS" or "<id> FAIL" last.
  DB44-1-AC1  ~65/FINAL_ROWS_UNIQ.json tests {passed > 0, failed == 0, new_test "<file>::<function>"} with the function at HEAD, and check_site a
              function name defined in data/assets/scripts/gold/irpt_reporting/account_activity_lots.py.
  DB44-2-AC1  ~66/LOTS_NOT_COMPUTED.json tests {passed > 0, failed == 0, new_test}, listing_ignores_status true, and the handler
              infra/aws/lambda/investor-reporting/reporting-gold/handler.py carries the literal "lots not computed for".
  DB44-3-AC1  ~67/RUNNER_SHA.json tests {passed > 0, failed == 0, new_test}, and the runner
              data/assets/scripts/gold/irpt_custody/e2a_real_statement.py's verify-persisted path references "sha256".
"""
import json
import re
import sys
from pathlib import Path

D = "org/missions/D9/IRPT/IRPT_DASHBD/deliverables/0.9.0_WK_IRPT_DASHBD~"
PROD = "data/assets/scripts/gold/irpt_reporting/account_activity_lots.py"
HANDLER = "infra/aws/lambda/investor-reporting/reporting-gold/handler.py"
RUNNER = "data/assets/scripts/gold/irpt_custody/e2a_real_statement.py"


def main():
    root = Path(sys.argv[1] if len(sys.argv) > 1 else ".").resolve()
    cid = sys.argv[2] if len(sys.argv) > 2 else ""

    def fail(msg):
        print("FAIL: " + msg)
        print("%s FAIL" % (cid or "DB44"))
        sys.exit(1)

    def load(rel):
        p = root / rel
        if not p.is_file():
            fail("no %s" % rel)
        return json.loads(p.read_bytes().decode("utf-8"))

    def tests_ok(r):
        t = r.get("tests") or {}
        m = re.fullmatch(r"([^:]+\.py)::(\w+)", str(t.get("new_test") or ""))
        if not isinstance(t.get("passed"), int) or t["passed"] <= 0 or t.get("failed") != 0 or not m or not (root / m.group(1)).is_file() \
                or not re.search(r"^def %s\(" % re.escape(m.group(2)), (root / m.group(1)).read_text(encoding="utf-8"), re.M):
            fail("tests %r" % t)
        return t

    if cid == "DB44-1-AC1":
        r = load(D + "65/FINAL_ROWS_UNIQ.json")
        t = tests_ok(r)
        site = str(r.get("check_site") or "")
        if not site or not re.search(r"^def %s\(" % re.escape(site), (root / PROD).read_text(encoding="utf-8"), re.M):
            fail("check_site %r is not a function in %s" % (site, PROD))
        print("OK: final-rows uniqueness in %s(); %d passed; new test %s" % (site, t["passed"], t["new_test"]))
    elif cid == "DB44-2-AC1":
        r = load(D + "66/LOTS_NOT_COMPUTED.json")
        t = tests_ok(r)
        if r.get("listing_ignores_status") is not True or "lots not computed for" not in (root / HANDLER).read_text(encoding="utf-8"):
            fail("listing_ignores_status %r / handler statement missing" % r.get("listing_ignores_status"))
        print("OK: skipped lots days stated; listing ignores the status record; %d passed" % t["passed"])
    elif cid == "DB44-3-AC1":
        r = load(D + "67/RUNNER_SHA.json")
        t = tests_ok(r)
        src = (root / RUNNER).read_text(encoding="utf-8")
        i = src.find("verify-persisted")
        if i < 0 or "sha256" not in src[i:]:
            fail("verify-persisted path does not reference sha256")
        print("OK: verify-persisted checks sha256; %d passed" % t["passed"])
    else:
        fail("unknown criterion %r" % cid)
    print("%s PASS" % cid)


if __name__ == "__main__":
    main()
