"""IRPT_DASHBD round 45 (issuer 2.0.0_SA_COO~D2) -- 1.0.0_SA_CTO~DELL2's ADDENDUM 11.1 item 1 (msg 3362, @43bbe32935): the statement runner
accepts the seat-authored selection FILE (ADDENDUM 9.2); no seat mints account_set_id through selection-create.

Usage: python <this file> <repo_root> <criterion_id>; prints "<id> PASS" or "<id> FAIL" last.
  DB45-1-AC1  ~68/SELECTION_FILE.json has tests {passed > 0, failed == 0, new_test "<file>::<function>"} with the function at HEAD;
              deterministic is a bool; if true, derivation_site names a "<file>::<function>" at HEAD (the API's own sel_ derivation);
              if false, the runner data/assets/scripts/gold/irpt_custody/e2a_real_statement.py carries the literal "selection_source".
"""
import json
import re
import sys
from pathlib import Path

REC = "org/missions/D9/IRPT/IRPT_DASHBD/deliverables/0.9.0_WK_IRPT_DASHBD~68/SELECTION_FILE.json"
RUNNER = "data/assets/scripts/gold/irpt_custody/e2a_real_statement.py"


def main():
    root = Path(sys.argv[1] if len(sys.argv) > 1 else ".").resolve()
    cid = sys.argv[2] if len(sys.argv) > 2 else ""

    def fail(msg):
        print("FAIL: " + msg)
        print("%s FAIL" % (cid or "DB45"))
        sys.exit(1)

    def site_ok(s):
        m = re.fullmatch(r"([^:]+\.py)::(\w+)", str(s or ""))
        return bool(m) and (root / m.group(1)).is_file() and bool(
            re.search(r"^\s*def %s\(" % re.escape(m.group(2)), (root / m.group(1)).read_text(encoding="utf-8"), re.M))

    if cid != "DB45-1-AC1":
        fail("unknown criterion %r" % cid)
    p = root / REC
    if not p.is_file():
        fail("no %s" % REC)
    r = json.loads(p.read_bytes().decode("utf-8"))
    t = r.get("tests") or {}
    if not isinstance(t.get("passed"), int) or t["passed"] <= 0 or t.get("failed") != 0 or not site_ok(t.get("new_test")):
        fail("tests %r" % t)
    det = r.get("deterministic")
    if not isinstance(det, bool):
        fail("deterministic %r is not a bool" % det)
    if det and not site_ok(r.get("derivation_site")):
        fail("deterministic but derivation_site %r is not a function at HEAD" % r.get("derivation_site"))
    if not det and "selection_source" not in (root / RUNNER).read_text(encoding="utf-8"):
        fail("not deterministic, and the runner does not record selection_source")
    print("OK: runner accepts the selection file; deterministic=%s; %d passed" % (det, t["passed"]))
    print("%s PASS" % cid)


if __name__ == "__main__":
    main()
