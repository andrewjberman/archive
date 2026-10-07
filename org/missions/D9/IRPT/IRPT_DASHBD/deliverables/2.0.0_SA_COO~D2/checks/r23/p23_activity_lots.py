"""IRPT_DASHBD round 23 (workstream B, issuer 2.0.0_SA_COO~D2) -- 1.0.0_SA_CTO~DELL2's round-22 analysis @a1873a8be7 item E1 (PRD
backlog B2, FWD-4): `account_activity_daily`, `account_lot_realized` and `account_lot_unrealized_daily` for 49 Financial, built and run
LOCALLY. Their release is a later packet under its own halves; nothing here writes S3.

Usage: python <this file> <repo_root> <criterion_id>
  DB23-1-AC1  the record's reconciliation for one account and one window: beginning_value + contributions - withdrawals + realized
              + unrealized_change + income == ending_value within one cent, every term present and printed. Base: FAIL.
  DB23-1-AC2  the realized-lot tie: lots_total >= 1; tied + untied == lots_total; one named reason per untied lot (untied ==
              len(untied_lots), each with a lot id and a non-empty reason). Base: FAIL.
  DB23-1-AC3  every new address and name is builder output: each `builder_output` row's `output` equals what lib/opal_naming.py
              returns for its `call` when re-run here, and the three table addresses are among them. Base: FAIL.
Prints "<id> PASS" or "<id> FAIL" as the last line.
"""
import importlib.util
import json
import sys
from pathlib import Path

W = "org/missions/D9/IRPT/IRPT_DASHBD/deliverables/0.9.0_WK_IRPT_DASHBD~20/"
REC = W + "ACTIVITY_LOTS_LOCAL_RUN.json"
TERMS = ("beginning_value", "contributions", "withdrawals", "realized", "unrealized_change", "income", "ending_value")
TABLES = ("account_activity_daily", "account_lot_realized", "account_lot_unrealized_daily")


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
        print("%s FAIL" % (cid or "DB23"))
        sys.exit(1)

    if cid == "DB23-1-AC1":
        rec = _load(root, REC, fail).get("reconciliation") or {}
        miss = [t for t in TERMS if rec.get(t) is None]
        if miss or not rec.get("account_id") or not rec.get("window"):
            fail("reconciliation lacks %s (or its account/window)" % (miss or ["account_id/window"]))
        v = {t: float(rec[t]) for t in TERMS}
        lhs = v["beginning_value"] + v["contributions"] - v["withdrawals"] + v["realized"] + v["unrealized_change"] + v["income"]
        gap = abs(lhs - v["ending_value"])
        for t in TERMS:
            print("  %-18s %18.2f" % (t, v[t]))
        if gap > 0.01:
            fail("the identity misses by %.4f (more than one cent)" % gap)
        print("OK: one account-window ties term by term within one cent (gap %.4f)" % gap)
    elif cid == "DB23-1-AC2":
        t = _load(root, REC, fail).get("lot_tie") or {}
        tot, tied, untied = t.get("lots_total"), t.get("tied"), t.get("untied")
        lots = t.get("untied_lots") or []
        if not isinstance(tot, int) or tot < 1:
            fail("lots_total %r" % tot)
        if tied is None or untied is None or tied + untied != tot:
            fail("tied %r + untied %r != lots_total %r" % (tied, untied, tot))
        bad = [x for x in lots if not x.get("lot_id") or not str(x.get("reason") or "").strip()]
        if untied != len(lots) or bad:
            fail("untied %r against %d listed lots (%d without an id or reason)" % (untied, len(lots), len(bad)))
        print("OK: %d of %d realized lots tie to their closing transaction; %d untied, each with a reason" % (tied, tot, untied))
    elif cid == "DB23-1-AC3":
        rows = _load(root, REC, fail).get("builder_output") or []
        spec = importlib.util.spec_from_file_location("opal_naming", str(root / "lib" / "opal_naming.py"))
        on = importlib.util.module_from_spec(spec)
        sys.path.insert(0, str(root / "lib"))
        spec.loader.exec_module(on)
        seen = []
        for r in rows:
            fn, args = r.get("call", {}).get("fn"), r.get("call", {}).get("args") or []
            if fn not in ("address", "name"):
                fail("builder_output row with fn %r" % fn)
            got = str(getattr(on, fn)(*args))
            if got != r.get("output"):
                fail("%s%r returns %r here; the record says %r" % (fn, tuple(args), got, r.get("output")))
            seen.append(got)
        missing = [tb for tb in TABLES if not any("/gold/%s/" % tb in s for s in seen)]
        if missing:
            fail("no builder address for %s" % missing)
        print("OK: %d builder rows re-derived; the three table addresses are builder output" % len(rows))
    else:
        fail("unknown criterion %r" % cid)
    print("%s PASS" % cid)


if __name__ == "__main__":
    main()
