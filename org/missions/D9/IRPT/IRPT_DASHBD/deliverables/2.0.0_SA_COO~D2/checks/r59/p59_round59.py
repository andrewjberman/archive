"""IRPT_DASHBD round 59 (issuer 2.0.0_SA_COO~D2) -- remedy for row IRPT_DASHBD-D2-W88-S3 (DB-b-113's measured manifest regression).

Cell: DB-b-115 the reporting-gold handler passes the firm's declared source entry to every ard.emit_day call, so the returns manifest states
the method row the entry names (2) and its three method fields, never the literal `absent`.

Usage: python <this file> <repo_root> <criterion_id>; prints "<id> PASS" or "<id> FAIL" last.
  DB59-1-AC1  every `ard.emit_day(` call in reporting-gold handler.py passes `src=`; ~90/HANDLER_SRC_FIX.json records the manifest the fixed
              handler's own call writes on a fixture: method_version == 2 and valuation_source, fee_treatment, price_basis each equal to
              the 49F custody entry's value in sources.json at HEAD, none of them `absent`; tests {passed > 0, failed == 0, new_test} with
              the new test file present at HEAD.
"""
import ast
import json
import sys
from pathlib import Path

D = "org/missions/D9/IRPT/IRPT_DASHBD/deliverables/0.9.0_WK_IRPT_DASHBD~"
HANDLER = "infra/aws/lambda/investor-reporting/reporting-gold/handler.py"
SOURCES = "data/assets/scripts/gold/irpt_reporting/sources.json"
FIELDS = ("valuation_source", "fee_treatment", "price_basis")


def main():
    root = Path(sys.argv[1] if len(sys.argv) > 1 else ".").resolve()
    cid = sys.argv[2] if len(sys.argv) > 2 else ""

    def fail(msg):
        print("FAIL: " + msg)
        print("%s FAIL" % (cid or "DB59"))
        sys.exit(1)

    if cid != "DB59-1-AC1":
        fail("unknown criterion %r" % cid)
    tree = ast.parse((root / HANDLER).read_text(encoding="utf-8"))
    calls = [n for n in ast.walk(tree) if isinstance(n, ast.Call) and isinstance(n.func, ast.Attribute) and n.func.attr == "emit_day"]
    if not calls:
        fail("no emit_day call found in the handler")
    bare = [n.lineno for n in calls if "src" not in [k.arg for k in n.keywords]]
    if bare:
        fail("emit_day call(s) without src= at line(s) %r (of %d call(s))" % (bare, len(calls)))
    p = root / (D + "90/HANDLER_SRC_FIX.json")
    if not p.is_file():
        fail("no record")
    r = json.loads(p.read_bytes().decode("utf-8"))
    src = json.loads((root / SOURCES).read_bytes().decode("utf-8"))
    entries = [v for k, v in src.items() if not k.startswith("_") and isinstance(v, dict) and v.get("method_version") == 2]
    if len(entries) != 1:
        fail("expected exactly one non-underscore sources.json entry naming method_version 2, found %d" % len(entries))
    man = r.get("manifest") or {}
    if man.get("method_version") != 2:
        fail("manifest method_version %r" % man.get("method_version"))
    for f in FIELDS:
        if man.get(f) in (None, "absent") or man.get(f) != entries[0].get(f):
            fail("manifest %s %r, the entry says %r" % (f, man.get(f), entries[0].get(f)))
    t = r.get("tests") or {}
    nt = str(t.get("new_test") or "").split("::")[0]
    if not isinstance(t.get("passed"), int) or t["passed"] <= 0 or t.get("failed") != 0 or not nt or not (root / nt).is_file():
        fail("tests %r" % t)
    print("OK: %d emit_day call(s) all pass src=; the manifest states row 2 and the entry's three method fields" % len(calls))
    print("%s PASS" % cid)


if __name__ == "__main__":
    main()
