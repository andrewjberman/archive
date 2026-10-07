"""IRPT_DASHBD round 21 (workstream B, issuer 2.0.0_SA_COO~D2) -- 1.0.0_SA_CTO~DELL2's round-20 analysis @58f3ed0501 item E1:
`account_class_daily` and the class contribution for 49 Financial (FWD-3), built and run LOCALLY over a bounded sample. Its release
to the served gold is a separate act under its own never-widen halves; nothing here writes S3.

Usage: python <this file> <repo_root> <criterion_id>
  DB21-1-AC1  the local run's record: on every account-day, the sum of `class_return_daily` over the classes equals that
              account-day's `account_daily_return` (the account_return_daily producer's own figure for the same day) within
              1e-9; at least 50 account-days. Base: FAIL (no record).
  DB21-1-AC2  the vocabulary: every class is one of cash, fixed_income, equity, structured, alternatives, commodities,
              unclassified; every holding the classification module does not name maps to `unclassified` (never to the
              module's default), and no holding the module names is reassigned except a cash position to `cash`. Base: FAIL.
  DB21-1-AC3  the contract file org/standards/IRPT_DASHBD_ACCOUNT_CLASS_DAILY_CONTRACT.json exists; its class enum equals the
              seven values; its column list equals the record's `columns` and includes firm, account_id, method_version and
              coverage. Base: FAIL.
Prints "<id> PASS" or "<id> FAIL" as the last line.
"""
import json
import sys
from collections import defaultdict
from pathlib import Path

W = "org/missions/D9/IRPT/IRPT_DASHBD/deliverables/0.9.0_WK_IRPT_DASHBD~18/"
REC = W + "CLASS_DAILY_LOCAL_RUN.json"
CONTRACT = "org/standards/IRPT_DASHBD_ACCOUNT_CLASS_DAILY_CONTRACT.json"
CLASSES = {"cash", "fixed_income", "equity", "structured", "alternatives", "commodities", "unclassified"}
REQUIRED = {"firm", "account_id", "method_version", "coverage"}


def _load(root, rel, fail):
    p = root / rel
    if not p.is_file():
        fail("no %s" % rel)
    return json.loads(p.read_bytes().decode("utf-8"))


def main():
    root = Path(sys.argv[1] if len(sys.argv) > 1 else ".").resolve()
    cid = sys.argv[2] if len(sys.argv) > 2 else ""

    def fail(msg):
        print("FAIL: " + msg)
        print("%s FAIL" % (cid or "DB21"))
        sys.exit(1)

    if cid == "DB21-1-AC1":
        rec = _load(root, REC, fail)
        acct = {(r["account_id"], r["business_date"]): r["account_daily_return"] for r in rec.get("account_days") or []}
        sums = defaultdict(float)
        for r in rec.get("class_rows") or []:
            if r.get("class_return_daily") is not None:  # a not-measurable day carries null plus its coverage reason
                sums[(r["account_id"], r["business_date"])] += float(r["class_return_daily"])
        if len(acct) < 50:
            fail("%d account-days in the record; at least 50 are required" % len(acct))
        missing = [k for k in acct if k not in sums]
        if missing:
            fail("%d account-days carry no class rows" % len(missing))
        worst = max(abs(sums[k] - float(v)) for k, v in acct.items())
        if worst > 1e-9:
            fail("classes do not sum to the account: largest gap %.3e" % worst)
        print("OK: %d account-days; classes sum to the account's daily return, largest gap %.3e" % (len(acct), worst))
    elif cid == "DB21-1-AC2":
        rec = _load(root, REC, fail)
        bad = sorted({r["class"] for r in rec.get("class_rows") or []} - CLASSES)
        if bad:
            fail("classes outside the vocabulary: %s" % bad)
        hm = rec.get("holding_map") or []
        if not hm:
            fail("the record carries no holding_map")
        wrong = [h for h in hm
                 if (h.get("module_class") is None and not h.get("is_cash") and h.get("class") != "unclassified")
                 or (h.get("is_cash") and h.get("class") != "cash")
                 or (h.get("module_class") is not None and not h.get("is_cash") and h.get("class") != h.get("module_class"))]
        if wrong:
            fail("%d holdings mapped against the rule, e.g. %s" % (len(wrong), wrong[0]))
        un = sum(1 for h in hm if h.get("class") == "unclassified")
        print("OK: %d holdings mapped; %d unclassified kept as their own class; vocabulary within the seven" % (len(hm), un))
    elif cid == "DB21-1-AC3":
        c = _load(root, CONTRACT, fail)
        rec = _load(root, REC, fail)
        enum = set(c.get("class_enum") or [])
        if enum != CLASSES:
            fail("contract class_enum %s" % sorted(enum))
        cols = [x.get("name") if isinstance(x, dict) else x for x in c.get("columns") or []]
        if cols != list(rec.get("columns") or []):
            fail("contract columns %s differ from the record's %s" % (cols, rec.get("columns")))
        if not REQUIRED <= set(cols):
            fail("contract columns lack %s" % sorted(REQUIRED - set(cols)))
        print("OK: contract enum is the seven classes; %d columns match the produced table" % len(cols))
    else:
        fail("unknown criterion %r" % cid)
    print("%s PASS" % cid)


if __name__ == "__main__":
    main()
