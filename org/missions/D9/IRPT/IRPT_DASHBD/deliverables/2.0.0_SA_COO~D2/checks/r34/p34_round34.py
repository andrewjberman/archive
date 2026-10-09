"""IRPT_DASHBD round 34 (issuer 2.0.0_SA_COO~D2) -- 1.0.0_SA_CTO~DELL2's round-33 ADDENDUM 2 @47c849d75b (msg 2116) on ADJUDICATION_v18:
repair the two callers round 32's promotion broke and re-run the near-zero fix without its shim (row S36); measure the activity-and-lot
release's lots peak on the pandas 2.2.3 kit; trace FLOW_TIMING_AFTER_FEE_BASE (116).

Usage: python <this file> <repo_root> <criterion_id>
  DB34-1-AC1  pytest passes on BOTH caller tests -- ~39/test_large_flow_e3.py and ~35/test_crossover_e1.py (the latter has a test whose
              name contains "caller"); neither caller nor ~42/near_zero_e3.py assigns `mean_daily_value` on a module (no shim); the
              fee-base writer census over the project tree is still exactly [READER]. Base: FAIL.
  DB34-1-AC2  NEAR_ZERO_SHIMFREE_E1.json: `shim_applied` is false; `rows` cover exactly the 153 NEAR_ZERO_BALANCE rows of round 31's
              UNEXPLAINED_CLASSES_E2.json; `counts` equals the tally; `fixed_within` (rows of the fixed classes within 0.35 pp) and
              `tieout_within_total` are integers; `reader_sha256` == READER's bytes at HEAD. Base: FAIL.
  DB34-2-AC1  KIT_PEAK_E2.json: `runtime` read from the run's own process has pandas "2.2.3", numpy "1.26.4", pyarrow "14.0.2" and a
              python 3.12.x; `population_count` >= 7,000 and `accounts_run` equal to it; `lots_stage_completed` true; `batch_size` equals
              the lots producer's DEFAULT_BATCH_SIZE at HEAD. Base: FAIL.
  DB34-2-AC2  `lots_peak_mb` numeric; `verdict` == FITS iff lots_peak_mb <= 2,048 else BREACH (stated here before the run); the 3.0.6
              reference (`reference_3_0_6_peak_mb`) is printed beside it. Base: FAIL.
  DB34-3-AC1  FLOW_TIMING_FEE_E3.json: `rows` cover exactly the 116 FLOW_TIMING_AFTER_FEE_BASE rows of round 31's record, each with a
              non-empty sub_class and a numeric `abs_diff_pp_now` (under the reader of record); `counts` equals the tally; `within_now`
              equals the count of rows with abs_diff_pp_now <= 0.35. Base: FAIL.
  DB34-3-AC2  every sub_class is dispositioned "fixed", "named_cause" or "resolved_by_reader" with a non-empty cause. Base: FAIL.
Prints "<id> PASS" or "<id> FAIL" as the last line.
"""
import hashlib
import json
import re
import subprocess
import sys
from pathlib import Path

PROJ = "org/missions/D9/IRPT/IRPT_DASHBD/"
D = PROJ + "deliverables/"
READER = PROJ + "tieout/tieout_reader.py"
UNEX = D + "0.9.0_WK_IRPT_DASHBD~36/UNEXPLAINED_CLASSES_E2.json"
T39 = D + "0.9.0_WK_IRPT_DASHBD~39/test_large_flow_e3.py"
T35 = D + "0.9.0_WK_IRPT_DASHBD~35/test_crossover_e1.py"
CALLERS = (D + "0.9.0_WK_IRPT_DASHBD~39/large_flow_e3.py", D + "0.9.0_WK_IRPT_DASHBD~35/crossover_e1.py",
           D + "0.9.0_WK_IRPT_DASHBD~42/near_zero_e3.py")
REC1 = D + "0.9.0_WK_IRPT_DASHBD~43/NEAR_ZERO_SHIMFREE_E1.json"
REC2 = D + "0.9.0_WK_IRPT_DASHBD~44/KIT_PEAK_E2.json"
REC3 = D + "0.9.0_WK_IRPT_DASHBD~45/FLOW_TIMING_FEE_E3.json"
LOTS = "data/assets/scripts/gold/irpt_reporting/account_activity_lots.py"
FEE_BASE_NAMES = ("daily_mean_value", "mean_daily_value", "fee_addback_v2", "fee_base_gross", "fee_base_daily_mean")
TOL = 0.35
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
        print("%s FAIL" % (cid or "DB34"))
        sys.exit(1)

    def load(rel):
        p = root / rel
        if not p.is_file():
            fail("no %s" % rel)
        return json.loads(p.read_bytes().decode("utf-8"))

    def pop_of(cls):
        return {key(x) for x in load(UNEX)["rows"] if x.get("cause_class") == cls}

    if cid == "DB34-1-AC1":
        t35 = (root / T35).read_bytes().decode("utf-8") if (root / T35).is_file() else ""
        if not re.search(r"^def test_\w*caller\w*\(", t35, re.M):
            fail("no test whose name contains 'caller' in %s" % T35)
        for t in (T39, T35):
            rr = subprocess.run([sys.executable, "-m", "pytest", "-q", "-p", "no:cacheprovider", str(root / t)], cwd=str(root),
                                capture_output=True, text=True, timeout=600)
            out = re.sub(r"\x1b\[[0-9;]*m", "", (rr.stdout or "") + (rr.stderr or ""))
            if rr.returncode or not re.search(r"\d+ passed", out) or re.search(r"\d+ failed", out):
                fail("pytest %s: %s" % (t, out[-300:]))
        shim = re.compile(r"\.\s*mean_daily_value\s*=")
        shimmed = [c for c in CALLERS if (root / c).is_file() and shim.search((root / c).read_bytes().decode("utf-8"))]
        if shimmed:
            fail("a module-level mean_daily_value assignment (shim) remains in %r" % shimmed)
        pat = re.compile(r"^\s*def\s+(%s)\s*\(" % "|".join(FEE_BASE_NAMES), re.M)
        files = sorted(p for p in (root / PROJ).rglob("*.py") if "__pycache__" not in p.parts)
        writers = [p.relative_to(root).as_posix() for p in files if pat.search(p.read_bytes().decode("utf-8", "replace"))]
        if writers != [READER]:
            fail("fee-base writer census over %d .py: %r" % (len(files), writers))
        print("OK: both caller tests pass; no shim in %d caller(s); writer census 1 of %d" % (len(CALLERS), len(files)))
    elif cid == "DB34-1-AC2":
        r = load(REC1)
        pop = pop_of("NEAR_ZERO_BALANCE")
        rows = r.get("rows") or []
        if r.get("shim_applied") is not False:
            fail("shim_applied %r (must be false)" % r.get("shim_applied"))
        if {key(x) for x in rows} != pop or len(rows) != len(pop) or [x for x in rows if not str(x.get("sub_class") or "").strip()]:
            fail("%d rows; equal to the %d NEAR_ZERO_BALANCE rows, each with a sub_class" % (len(rows), len(pop)))
        tally = {}
        for x in rows:
            tally[x["sub_class"]] = tally.get(x["sub_class"], 0) + 1
        if (r.get("counts") or {}) != tally:
            fail("counts %r, the tally %r" % (r.get("counts"), tally))
        if not isinstance(r.get("fixed_within"), int) or not isinstance(r.get("tieout_within_total"), int):
            fail("fixed_within %r / tieout_within_total %r must be integers" % (r.get("fixed_within"), r.get("tieout_within_total")))
        if r.get("reader_sha256") != hashlib.sha256((root / READER).read_bytes()).hexdigest():
            fail("reader_sha256 differs from %s at HEAD" % READER)
        print("OK: shim-free re-run of 153: fixed classes within %d; tie-out within total %d; counts %s" % (
            r["fixed_within"], r["tieout_within_total"], tally))
    elif cid in ("DB34-2-AC1", "DB34-2-AC2"):
        r = load(REC2)
        if cid == "DB34-2-AC1":
            rt = r.get("runtime") or {}
            if rt.get("pandas") != "2.2.3" or rt.get("numpy") != "1.26.4" or rt.get("pyarrow") != "14.0.2" \
                    or not str(rt.get("python") or "").startswith("3.12."):
                fail("runtime %r is not python 3.12 / pandas 2.2.3 / numpy 1.26.4 / pyarrow 14.0.2" % rt)
            pop, run = r.get("population_count"), r.get("accounts_run")
            if not isinstance(pop, int) or pop < 7000 or run != pop or r.get("lots_stage_completed") is not True:
                fail("population %r, accounts_run %r, lots_stage_completed %r" % (pop, run, r.get("lots_stage_completed")))
            m = re.search(rb"^DEFAULT_BATCH_SIZE\s*=\s*(\d+)", (root / LOTS).read_bytes(), re.M)
            if not m or r.get("batch_size") != int(m.group(1)):
                fail("batch_size %r, DEFAULT_BATCH_SIZE at HEAD %r" % (r.get("batch_size"), m and int(m.group(1))))
            print("OK: python %s pandas %s numpy %s pyarrow %s; %d accounts at batch %s; lots completed" % (
                rt["python"], rt["pandas"], rt["numpy"], rt["pyarrow"], pop, r["batch_size"]))
        else:
            pk = r.get("lots_peak_mb")
            if not num(pk):
                fail("lots_peak_mb %r" % pk)
            want = "FITS" if pk <= MEM else "BREACH"
            if r.get("verdict") != want:
                fail("verdict %r, the peak %s gives %s" % (r.get("verdict"), pk, want))
            print("OK: lots peak on pandas 2.2.3 = %.1f MB -> %s (3.0.6 reference %s MB; limit %d MB)" % (
                pk, want, r.get("reference_3_0_6_peak_mb"), MEM))
    elif cid in ("DB34-3-AC1", "DB34-3-AC2"):
        pop = pop_of("FLOW_TIMING_AFTER_FEE_BASE")
        r = load(REC3)
        rows = r.get("rows") or []
        if {key(x) for x in rows} != pop or len(rows) != len(pop) \
                or [x for x in rows if not str(x.get("sub_class") or "").strip() or not num(x.get("abs_diff_pp_now"))]:
            fail("%d rows; equal to the %d FLOW_TIMING_AFTER_FEE_BASE rows, each with sub_class and numeric abs_diff_pp_now" % (len(rows), len(pop)))
        tally = {}
        for x in rows:
            tally[x["sub_class"]] = tally.get(x["sub_class"], 0) + 1
        if (r.get("counts") or {}) != tally:
            fail("counts %r, the tally %r" % (r.get("counts"), tally))
        if cid == "DB34-3-AC1":
            w = sum(1 for x in rows if x["abs_diff_pp_now"] <= TOL)
            if r.get("within_now") != w:
                fail("within_now %r, the tally %d" % (r.get("within_now"), w))
            print("OK: %d of %d traced; %d within now under the reader; %s" % (len(rows), len(pop), w, tally))
        else:
            disp = r.get("dispositions") or {}
            bad = [k for k in tally if (disp.get(k) or {}).get("disposition") not in ("fixed", "named_cause", "resolved_by_reader")
                   or not str((disp.get(k) or {}).get("cause") or "").strip()]
            if bad:
                fail("sub-classes without disposition and cause: %r" % bad)
            print("OK: every sub-class dispositioned: %s" % {k: disp[k]["disposition"] for k in tally})
    else:
        fail("unknown criterion %r" % cid)
    print("%s PASS" % cid)


if __name__ == "__main__":
    main()
