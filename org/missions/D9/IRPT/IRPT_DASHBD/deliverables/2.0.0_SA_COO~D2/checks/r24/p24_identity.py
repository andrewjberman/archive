"""IRPT_DASHBD round 24 (workstream B, issuer 2.0.0_SA_COO~D2) -- 1.0.0_SA_CTO~DELL2's round-23 analysis @9f285400cf: E1 diagnoses the
activity-identity gaps of round 23 (row W20-S2), E2 fixes the named cause and re-grades. LOCAL: no S3 write.

The round-23 record `deliverables/0.9.0_WK_IRPT_DASHBD~20/ACTIVITY_LOTS_LOCAL_RUN.json` carries `window_identity`: 91 accounts graded,
52 within one cent, and `accounts_above_one_cent` (39 rows: account_id, gap). This checker re-reads it as the denominator.

Usage: python <this file> <repo_root> <criterion_id>
  DB24-1-AC1  the largest gap's window term by term: account_id is the round-23 account with the largest |gap|; all seven terms carry
              a value, a row_count and their source rows (non-empty where the value is non-zero); the cause is named with the rows
              that show it. Base: FAIL.
  DB24-1-AC2  the transaction-type census: at least one row; each type carries row_count, sign (+, - or UNSIGNED), maps_to_term
              (a term or null) and moves_value; `unmapped_value_movers` lists exactly the types that move value and map to no term.
              Base: FAIL.
  DB24-1-AC3  the 39 gaps classed: the set of accounts equals round 23's 39; tolerance == 0.05 (stated in the order before the run);
              ROUNDING only where |gap| <= tolerance; every MISSING-TERM row names its type or cause; counts per class printed.
              Base: FAIL.
  DB24-2-AC1  the re-grade over the same 91 accounts: graded == 91; passed + failed == graded; one failure row per failure, each with
              a class. Base: FAIL.
  DB24-2-AC2  one named window with a non-zero realized gain AND a non-zero contribution or withdrawal ties within one cent, every
              term printed. Base: FAIL.
  DB24-2-AC3  the producer's tests pass (at least 23, naming identity). Base: PASS at the cut (23 tests); the fix must keep it.
Prints "<id> PASS" or "<id> FAIL" as the last line.
"""
import json
import re
import subprocess
import sys
from pathlib import Path

P = "org/missions/D9/IRPT/IRPT_DASHBD/deliverables/"
R23 = P + "0.9.0_WK_IRPT_DASHBD~20/ACTIVITY_LOTS_LOCAL_RUN.json"
W = P + "0.9.0_WK_IRPT_DASHBD~21/"
E1 = W + "GAP_DIAGNOSIS_E1.json"
E2 = W + "IDENTITY_REGRADE_E2.json"
TESTS = "data/assets/scripts/gold/irpt_reporting/tests/test_account_activity_lots.py"
TERMS = ("beginning_value", "contributions", "withdrawals", "realized", "unrealized_change", "income", "ending_value")
TOL = 0.05


def _load(root, rel, fail):
    p = root / rel
    if not p.is_file():
        fail("no %s" % rel)
    return json.loads(p.read_bytes().decode("utf-8"))


def _r23(root, fail):
    w = _load(root, R23, fail).get("window_identity") or {}
    rows = w.get("accounts_above_one_cent") or []
    return w, {r["account_id"]: float(r["gap"]) for r in rows}


def main():
    root = Path(sys.argv[1] if len(sys.argv) > 1 else ".").resolve()
    cid = sys.argv[2] if len(sys.argv) > 2 else ""

    def fail(msg):
        print("FAIL: " + msg)
        print("%s FAIL" % (cid or "DB24"))
        sys.exit(1)

    if cid == "DB24-1-AC1":
        _, gaps = _r23(root, fail)
        biggest = max(gaps, key=lambda a: abs(gaps[a]))
        b = _load(root, E1, fail).get("largest_gap_window") or {}
        if b.get("account_id") != biggest:
            fail("largest_gap_window is %r; round 23's largest |gap| is %s (%.2f)" % (b.get("account_id"), biggest, gaps[biggest]))
        terms = b.get("terms") or {}
        for t in TERMS:
            x = terms.get(t) or {}
            if x.get("value") is None or not isinstance(x.get("row_count"), int):
                fail("term %s lacks value or row_count" % t)
            if float(x["value"]) != 0 and not x.get("source_rows"):
                fail("term %s is non-zero with no source rows" % t)
            print("  %-18s %18.2f  rows %d" % (t, float(x["value"]), x["row_count"]))
        if not str(b.get("cause") or "").strip() or not b.get("evidence_rows"):
            fail("the cause or its evidence rows are missing")
        print("OK: %s window read term by term; cause: %s" % (biggest, str(b["cause"])[:160]))
    elif cid == "DB24-1-AC2":
        rec = _load(root, E1, fail)
        census = rec.get("type_census") or []
        if not census:
            fail("empty type_census")
        bad = [c for c in census if not isinstance(c.get("row_count"), int) or c.get("sign") not in ("+", "-", "UNSIGNED")
               or "maps_to_term" not in c or not isinstance(c.get("moves_value"), bool)]
        if bad:
            fail("%d census rows lack row_count, sign, maps_to_term or moves_value" % len(bad))
        want = sorted(c["type"] for c in census if c["moves_value"] and c.get("maps_to_term") is None)
        if sorted(rec.get("unmapped_value_movers") or []) != want:
            fail("unmapped_value_movers %r, re-derived %r" % (rec.get("unmapped_value_movers"), want))
        uns = sum(1 for c in census if c["sign"] == "UNSIGNED")
        print("OK: %d types censused (%d UNSIGNED); %d move value and map to no term: %s" % (len(census), uns, len(want), want))
    elif cid == "DB24-1-AC3":
        _, gaps = _r23(root, fail)
        g = _load(root, E1, fail).get("gap_classes") or {}
        if float(g.get("tolerance", -1)) != TOL:
            fail("tolerance %r; the order states %s" % (g.get("tolerance"), TOL))
        rows = g.get("rows") or []
        got = {r.get("account_id") for r in rows}
        if got != set(gaps) or len(rows) != len(gaps):
            fail("%d classed rows against round 23's %d gaps" % (len(rows), len(gaps)))
        wrong = [r for r in rows if r.get("class") not in ("ROUNDING", "MISSING-TERM")
                 or (r["class"] == "ROUNDING" and abs(gaps[r["account_id"]]) > TOL)
                 or (r["class"] == "MISSING-TERM" and not str(r.get("cause") or "").strip())]
        if wrong:
            fail("%d rows classed against the rule, e.g. %s" % (len(wrong), wrong[0]))
        n = {c: sum(1 for r in rows if r["class"] == c) for c in ("ROUNDING", "MISSING-TERM")}
        print("OK: %d gaps classed: ROUNDING %d, MISSING-TERM %d (tolerance %s)" % (len(rows), n["ROUNDING"], n["MISSING-TERM"], TOL))
    elif cid == "DB24-2-AC1":
        w, _ = _r23(root, fail)
        r = _load(root, E2, fail).get("regrade") or {}
        fails = r.get("failures") or []
        if r.get("graded") != w.get("accounts_graded") or r.get("passed", -1) + r.get("failed", -1) != r.get("graded"):
            fail("graded %r (round 23: %r), passed %r, failed %r" % (r.get("graded"), w.get("accounts_graded"), r.get("passed"), r.get("failed")))
        if len(fails) != r.get("failed") or [f for f in fails if not f.get("class")]:
            fail("%d failure rows for failed=%r, or a failure without a class" % (len(fails), r.get("failed")))
        print("OK: re-grade over %d accounts: %d pass, %d fail (classes: %s)" % (
            r["graded"], r["passed"], r["failed"], sorted({f["class"] for f in fails})))
    elif cid == "DB24-2-AC2":
        x = _load(root, E2, fail).get("exercise") or {}
        miss = [t for t in TERMS if x.get(t) is None]
        if miss or not x.get("account_id") or not x.get("window"):
            fail("exercise lacks %s" % (miss or ["account_id/window"]))
        v = {t: float(x[t]) for t in TERMS}
        if v["realized"] == 0 or (v["contributions"] == 0 and v["withdrawals"] == 0):
            fail("the named window does not exercise realized AND a contribution or withdrawal")
        gap = abs(v["beginning_value"] + v["contributions"] - v["withdrawals"] + v["realized"] + v["unrealized_change"]
                  + v["income"] - v["ending_value"])
        for t in TERMS:
            print("  %-18s %18.2f" % (t, v[t]))
        if gap > 0.01:
            fail("the identity misses by %.4f" % gap)
        print("OK: %s %s ties within one cent (gap %.4f) with realized and a flow both non-zero" % (x["account_id"], x["window"], gap))
    elif cid == "DB24-2-AC3":
        t = root / TESTS
        if not t.is_file() or "identity" not in t.read_bytes().decode("utf-8"):
            fail("no tests naming identity at %s" % TESTS)
        rr = subprocess.run([sys.executable, "-m", "pytest", "-q", "-p", "no:cacheprovider", str(t)], cwd=str(root),
                            capture_output=True, text=True, timeout=110)
        out = re.sub(r"\x1b\[[0-9;]*m", "", (rr.stdout or "") + (rr.stderr or ""))
        m = re.search(r"(\d+) passed", out)
        if rr.returncode or not m or int(m.group(1)) < 23:
            fail("pytest: %s" % out[-300:])
        print("OK: %s producer tests passed" % m.group(1))
    else:
        fail("unknown criterion %r" % cid)
    print("%s PASS" % cid)


if __name__ == "__main__":
    main()
