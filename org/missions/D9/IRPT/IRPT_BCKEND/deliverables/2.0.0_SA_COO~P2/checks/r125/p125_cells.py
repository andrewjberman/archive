"""IRPT_BCKEND round 125 (workstream ~P, issuer 2.0.0_SA_COO~P2) -- checks of one read-only DIRECT-ACT order:
  IB125-1  IB-pr-427  Cottonwood's lagged closes graded BY ACCOUNT and by any custodian / source field (CTO msg 4786),
                      counts only, no account id in any output.

Usage: python <this file> <repo_root> <criterion_id>; prints "<id> PASS" or "<id> FAIL" last.
  IB125-1-AC1  row totals add up (own + prior + neither == moved) and the accounts are classed with no remainder:
               always_own + always_prior + mixed + no_moved_rows == accounts read. Base: FAIL (no file).
  IB125-1-AC2  every field split sums to the row totals (or its absence carries a reason), and the "neither" rows are
               split by account class and sum to the neither total. Base: FAIL (no file).
  IB125-1-AC3  the control reports the planted lagged account alone, and neither committed output carries an account id.
               Base: FAIL (no file).
"""
import json
import re
import sys
from pathlib import Path

D = "org/missions/D9/IRPT/IRPT_BCKEND/deliverables/0.9.0_WK_IRPT_BCKEND~286/"
OUT = D + "IB125-1_lag_by_account.json"
READ = D + "IB125-1_LAG_BY_ACCOUNT_READ.md"
CLASSES = ("always_own", "always_prior", "mixed", "no_moved_rows")
# Black Diamond stamps the firm-instance prefix z09 on every Cottonwood account id (sources.json, registry_key_comment).
ACCOUNT_ID = re.compile(r"\bz09[0-9A-Za-z_-]{3,}", re.IGNORECASE)


def main():
    root = Path(sys.argv[1] if len(sys.argv) > 1 else ".").resolve()
    cid = sys.argv[2] if len(sys.argv) > 2 else ""

    def fail(msg):
        print("FAIL: " + msg)
        print("%s FAIL" % (cid or "IB125"))
        sys.exit(1)

    f = root / OUT
    if not f.is_file():
        fail("no %s" % OUT)
    text = f.read_text(encoding="utf-8")
    a = json.loads(text)
    rows = a.get("rows") or {}

    def adds(r, where):
        vals = [r.get(k) for k in ("moved", "own", "prior", "neither")]
        if not all(isinstance(v, int) for v in vals) or vals[1] + vals[2] + vals[3] != vals[0]:
            fail("%s counts do not add up: %r" % (where, vals))

    if cid == "IB125-1-AC1":
        adds(rows, "rows")
        if rows["moved"] <= 0:
            fail("no moved rows")
        acc = a.get("accounts") or {}
        if not isinstance(acc.get("read"), int) or not all(isinstance(acc.get(k), int) for k in CLASSES):
            fail("accounts %r" % acc)
        if sum(acc[k] for k in CLASSES) != acc["read"]:
            fail("account classes sum to %d, %d accounts read" % (sum(acc[k] for k in CLASSES), acc["read"]))
        if not isinstance(a.get("days_graded"), int) or a["days_graded"] < 80:
            fail("days_graded %r" % a.get("days_graded"))
        by = a.get("rows_by_account_class") or {}
        for k in ("always_own", "always_prior", "mixed"):
            adds(by.get(k) or {}, "rows_by_account_class." + k)
        if sum(by[k]["moved"] for k in ("always_own", "always_prior", "mixed")) != rows["moved"]:
            fail("rows_by_account_class does not sum to the moved rows")
        print("OK: %d moved rows over %d days add up; %d accounts classed with no remainder %s" % (
            rows["moved"], a["days_graded"], acc["read"], {k: acc[k] for k in CLASSES}))
    elif cid == "IB125-1-AC2":
        adds(rows, "rows")
        fields = a.get("by_field")
        if fields is None:
            fail("no by_field")
        if not fields and not a.get("by_field_absent_reason"):
            fail("by_field is empty with no reason")
        for fld in fields:
            vals = fld.get("values") or []
            if not fld.get("field") or not vals:
                fail("field row %r" % fld.get("field"))
            for v in vals:
                adds(v, "by_field.%s" % fld["field"])
                if not isinstance(v.get("accounts"), int) or v.get("value") is None:
                    fail("by_field.%s value row lacks value or accounts" % fld["field"])
            if sum(v["moved"] for v in vals) != rows["moved"]:
                fail("by_field.%s sums to %d moved, the rows to %d" % (fld["field"], sum(v["moved"] for v in vals), rows["moved"]))
        ns = a.get("neither_by_account_class") or {}
        if not all(isinstance(ns.get(k), int) for k in ("always_own", "always_prior", "mixed")) \
                or sum(ns[k] for k in ("always_own", "always_prior", "mixed")) != rows["neither"]:
            fail("neither_by_account_class %r does not sum to %d" % (ns, rows["neither"]))
        print("OK: %d field split(s) each sum to the rows; the %d neither rows are split by account class" % (len(fields), rows["neither"]))
    elif cid == "IB125-1-AC3":
        c = a.get("control") or {}
        if c.get("planted_account_label") is None or c.get("reported") != [c.get("planted_account_label")] \
                or c.get("clean_fixture_reported") != []:
            fail("control %r" % c)
        rd = root / READ
        if not rd.is_file():
            fail("no %s" % READ)
        for name, body in ((OUT, text), (READ, rd.read_text(encoding="utf-8"))):
            m = ACCOUNT_ID.search(body)
            if m:
                fail("%s carries an account id shaped token at offset %d" % (name, m.start()))
        print("OK: the planted account is reported alone; 0 account-id tokens in the 2 committed outputs")
    else:
        fail("unknown criterion %r" % cid)
    print("%s PASS" % cid)


if __name__ == "__main__":
    main()
