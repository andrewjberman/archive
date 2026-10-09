"""IRPT_DASHBD round 33 (issuer 2.0.0_SA_COO~D2) -- 1.0.0_SA_CTO~DELL2's round-32 ADDENDUM 1 @78928255f6 (msg on ADJUDICATION_v17):
adopt the two W39-S1 reader fixes; measure the activity-and-lot release on the SERVED pandas 2.2.3 (a measured refusal if the served
function cannot run it); trace NEAR_ZERO_BALANCE.

Usage: python <this file> <repo_root> <criterion_id>
  DB33-1-AC1  REGRADE_FIXES_E1.json covers round 18's 9,078 graded; within (<= 0.35 pp) == `within` and >= 8,315 (round 32's
              flow-start figure, the floor the CTO set); `reader_sha256` == READER's bytes at HEAD; the fee-base writer census over the
              project tree is still exactly [READER]. Base: FAIL.
  DB33-1-AC2  every segment WITHIN in round 32's REGRADE_FLOWSTART_E2.json and OUTSIDE here is in `in_to_out` with a reason, and
              nothing else. Base: FAIL.
  DB33-2-AC1  SERVED_PANDAS_E2.json: `deployed` {function, code_sha256, last_modified, layers} with code_sha256 a non-empty string;
              `layer_pandas_version` a non-empty string read from the deployed layer; `packaged_modules` a non-empty list read from the
              deployed package; `lots_producer_packaged` == ("data/assets/scripts/gold/irpt_reporting/account_activity_lots.py" in
              packaged_modules). Base: FAIL.
  DB33-2-AC2  the branch rule, stated before the run: if lots_producer_packaged, `invoke` is present with dry_run true and a numeric
              `max_memory_used_mb`, and `verdict` is FITS (<= 2,048) or BREACH; if not, `invoke` is null and `verdict` is REFUSED with a
              non-empty `refusal`. Never an invoke without dry_run. Base: FAIL.
  DB33-3-AC1  NEAR_ZERO_E3.json: `rows` cover exactly round 31's UNEXPLAINED_CLASSES_E2.json rows with cause_class NEAR_ZERO_BALANCE
              (153 at issue), each with a non-empty sub_class; `counts` equals the tally. Base: FAIL.
  DB33-3-AC2  every sub_class is dispositioned "fixed" or "named_cause" with a non-empty cause. Base: FAIL.
Prints "<id> PASS" or "<id> FAIL" as the last line.
"""
import hashlib
import json
import re
import sys
from pathlib import Path

PROJ = "org/missions/D9/IRPT/IRPT_DASHBD/"
D = PROJ + "deliverables/"
READER = PROJ + "tieout/tieout_reader.py"
R18 = D + "0.9.0_WK_IRPT_DASHBD~13/TIEOUT_49F_BD_POPULATION_E2_GROSS.json"
R32 = D + "0.9.0_WK_IRPT_DASHBD~38/REGRADE_FLOWSTART_E2.json"
UNEX = D + "0.9.0_WK_IRPT_DASHBD~36/UNEXPLAINED_CLASSES_E2.json"
REC1 = D + "0.9.0_WK_IRPT_DASHBD~40/REGRADE_FIXES_E1.json"
REC2 = D + "0.9.0_WK_IRPT_DASHBD~41/SERVED_PANDAS_E2.json"
REC3 = D + "0.9.0_WK_IRPT_DASHBD~42/NEAR_ZERO_E3.json"
LOTS = "data/assets/scripts/gold/irpt_reporting/account_activity_lots.py"
FEE_BASE_NAMES = ("daily_mean_value", "mean_daily_value", "fee_addback_v2", "fee_base_gross", "fee_base_daily_mean")
TOL = 0.35
FLOOR = 8315
MEM = 2048


def key(s):
    seg = s.get("segment") or {}
    return (s.get("account"), seg.get("start"), seg.get("end"))


def num(v):
    return isinstance(v, (int, float)) and not isinstance(v, bool)


def main():
    root = Path(sys.argv[1] if len(sys.argv) > 1 else ".").resolve()
    cid = sys.argv[2] if len(sys.argv) > 2 else ""

    def fail(msg):
        print("FAIL: " + msg)
        print("%s FAIL" % (cid or "DB33"))
        sys.exit(1)

    def load(rel):
        p = root / rel
        if not p.is_file():
            fail("no %s" % rel)
        return json.loads(p.read_bytes().decode("utf-8"))

    if cid in ("DB33-1-AC1", "DB33-1-AC2"):
        graded = {key(s) for s in load(R18)["segments"] if s["verdict"] in ("WITHIN", "OUTSIDE")}
        r = load(REC1)
        segs = r.get("segments") or []
        if {key(s) for s in segs} != graded or len(segs) != 9078 or [s for s in segs if not num(s.get("abs_diff_pp"))]:
            fail("%d segments; equal to round 18's 9,078 graded with numeric abs_diff_pp: %s" % (len(segs), {key(s) for s in segs} == graded))
        rp = root / READER
        if not rp.is_file() or r.get("reader_sha256") != hashlib.sha256(rp.read_bytes()).hexdigest():
            fail("reader_sha256 differs from %s at HEAD" % READER)
        if cid == "DB33-1-AC1":
            w = sum(1 for s in segs if s["abs_diff_pp"] <= TOL)
            if r.get("within") != w or w < FLOOR:
                fail("within %r, the tally %d, floor %d" % (r.get("within"), w, FLOOR))
            pat = re.compile(r"^\s*def\s+(%s)\s*\(" % "|".join(FEE_BASE_NAMES), re.M)
            files = sorted(p for p in (root / PROJ).rglob("*.py") if "__pycache__" not in p.parts)
            writers = [p.relative_to(root).as_posix() for p in files if pat.search(p.read_bytes().decode("utf-8", "replace"))]
            if writers != [READER]:
                fail("fee-base writer census over %d .py: %r" % (len(files), writers))
            print("OK: 9,078 re-graded with both fixes: within %d (>= %d); writer census 1 of %d; sha matches HEAD" % (w, FLOOR, len(files)))
        else:
            prev = {key(s): s for s in load(R32)["segments"]}
            want = {key(s) for s in segs if s["abs_diff_pp"] > TOL and prev[key(s)]["abs_diff_pp"] <= TOL}
            got = r.get("in_to_out") or []
            if {key(x) for x in got} != want or len(got) != len(want) or [x for x in got if not str(x.get("reason") or "").strip()]:
                fail("in_to_out %d vs %d from the records, every one with a reason" % (len(got), len(want)))
            print("OK: %d IN->OUT against round 32's flow-start re-grade, every one named" % len(want))
    elif cid in ("DB33-2-AC1", "DB33-2-AC2"):
        r = load(REC2)
        dep = r.get("deployed") or {}
        mods = r.get("packaged_modules")
        if cid == "DB33-2-AC1":
            if not str(dep.get("code_sha256") or "").strip() or not dep.get("function") or not str(r.get("layer_pandas_version") or "").strip():
                fail("deployed %r / layer_pandas_version %r incomplete" % (dep, r.get("layer_pandas_version")))
            if not isinstance(mods, list) or not mods:
                fail("packaged_modules %r must be the non-empty list read from the deployed package" % mods)
            if r.get("lots_producer_packaged") is not (LOTS in mods):
                fail("lots_producer_packaged %r but %s in packaged_modules is %s" % (r.get("lots_producer_packaged"), LOTS, LOTS in mods))
            print("OK: deployed %s sha %s; layer pandas %s; %d modules; lots producer packaged: %s" % (
                dep["function"], dep["code_sha256"][:12], r["layer_pandas_version"], len(mods), r["lots_producer_packaged"]))
        else:
            inv = r.get("invoke")
            if r.get("lots_producer_packaged") is True:
                if not isinstance(inv, dict) or inv.get("dry_run") is not True or not num(inv.get("max_memory_used_mb")):
                    fail("lots producer packaged: invoke must be a dry_run with numeric max_memory_used_mb, got %r" % inv)
                want = "FITS" if inv["max_memory_used_mb"] <= MEM else "BREACH"
                if r.get("verdict") != want:
                    fail("verdict %r, the peak %s gives %s" % (r.get("verdict"), inv["max_memory_used_mb"], want))
                print("OK: served dry_run peak %s MB -> %s" % (inv["max_memory_used_mb"], want))
            else:
                if inv is not None or r.get("verdict") != "REFUSED" or not str(r.get("refusal") or "").strip():
                    fail("lots producer not packaged: invoke must be null and verdict REFUSED with a refusal; got invoke %r verdict %r" % (
                        inv, r.get("verdict")))
                print("OK: REFUSED (measured): %s" % r["refusal"][:160])
    elif cid in ("DB33-3-AC1", "DB33-3-AC2"):
        pop = {key(x) for x in load(UNEX)["rows"] if x.get("cause_class") == "NEAR_ZERO_BALANCE"}
        r = load(REC3)
        rows = r.get("rows") or []
        if {key(x) for x in rows} != pop or len(rows) != len(pop) or [x for x in rows if not str(x.get("sub_class") or "").strip()]:
            fail("%d rows; equal to the %d NEAR_ZERO_BALANCE rows, each with a sub_class" % (len(rows), len(pop)))
        tally = {}
        for x in rows:
            tally[x["sub_class"]] = tally.get(x["sub_class"], 0) + 1
        if (r.get("counts") or {}) != tally:
            fail("counts %r, the tally %r" % (r.get("counts"), tally))
        if cid == "DB33-3-AC1":
            print("OK: %d of %d NEAR_ZERO_BALANCE traced: %s" % (len(rows), len(pop), tally))
        else:
            disp = r.get("dispositions") or {}
            bad = [k for k in tally if (disp.get(k) or {}).get("disposition") not in ("fixed", "named_cause")
                   or not str((disp.get(k) or {}).get("cause") or "").strip()]
            if bad:
                fail("sub-classes without disposition and cause: %r" % bad)
            print("OK: every sub-class dispositioned: %s" % {k: disp[k]["disposition"] for k in tally})
    else:
        fail("unknown criterion %r" % cid)
    print("%s PASS" % cid)


if __name__ == "__main__":
    main()
