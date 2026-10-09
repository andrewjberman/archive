"""IRPT_DASHBD round 51 (issuer 2.0.0_SA_COO~D2) -- laptop 4.0.0_SA_CRO via 0.0.0_AB_MSTR~DELL2 (msg 3555): no naming-registry row is owed;
address('irpt', firm, 'gold', 'account_activity_daily', '_status', 'lots_not_computed.json') builds the lots status key and grades CONFORMANT,
so the handler builds the key with address() instead of typing the suffix (rule 30).

Usage: python <this file> <repo_root> <criterion_id>; prints "<id> PASS" or "<id> FAIL" last.
  DB51-1-AC1  the reporting-gold handler carries no typed "_status/lots_not_computed.json" string literal, and calls address( with '_status'
              and 'lots_not_computed.json' arguments; ~79/STATUS_KEY_ADDRESS.json tests {passed > 0, failed == 0, new_test} with the
              function at HEAD and key_equal_before_after true.
"""
import json
import re
import sys
from pathlib import Path

HANDLER = "infra/aws/lambda/investor-reporting/reporting-gold/handler.py"
REC = "org/missions/D9/IRPT/IRPT_DASHBD/deliverables/0.9.0_WK_IRPT_DASHBD~79/STATUS_KEY_ADDRESS.json"


def main():
    root = Path(sys.argv[1] if len(sys.argv) > 1 else ".").resolve()
    cid = sys.argv[2] if len(sys.argv) > 2 else ""

    def fail(msg):
        print("FAIL: " + msg)
        print("%s FAIL" % (cid or "DB51"))
        sys.exit(1)

    if cid != "DB51-1-AC1":
        fail("unknown criterion %r" % cid)
    h = (root / HANDLER).read_text(encoding="utf-8")
    if re.search(r"""["']_status/lots_not_computed\.json["']""", h):
        fail("the handler still types the status suffix")
    if not re.search(r"address\([^)]*['\"]_status['\"][^)]*['\"]lots_not_computed\.json['\"]", h, re.S):
        fail("no address(..., '_status', 'lots_not_computed.json') call in the handler")
    p = root / REC
    if not p.is_file():
        fail("no %s" % REC)
    r = json.loads(p.read_bytes().decode("utf-8"))
    t = r.get("tests") or {}
    m = re.fullmatch(r"([^:]+\.py)::(\w+)", str(t.get("new_test") or ""))
    if not isinstance(t.get("passed"), int) or t["passed"] <= 0 or t.get("failed") != 0 or not m or not (root / m.group(1)).is_file() \
            or not re.search(r"^\s*def %s\(" % re.escape(m.group(2)), (root / m.group(1)).read_text(encoding="utf-8"), re.M):
        fail("tests %r" % t)
    if r.get("key_equal_before_after") is not True:
        fail("key_equal_before_after %r" % r.get("key_equal_before_after"))
    print("OK: status key built by address(); key unchanged; %d passed" % t["passed"])
    print("%s PASS" % cid)


if __name__ == "__main__":
    main()
