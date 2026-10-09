"""TO-DB-b-59 (IRPT_DASHBD round 31, DB-b-59, E3): the FLOW_TIMING compounded misses graded both ways -- every external flow at the START of
its day (invested for the day) vs at the END (not invested). Neither is adopted. READ-ONLY: S3 GETs/LISTs of the served gold only; zero
vendor calls; no write but the local record.

Population: round 30's compounded record, abs_diff_pp > 0.35 and reason == FLOW_TIMING. BD's gross is the record's bd_gross_return.
Opal's re-link is round 17's link_alt_flow (imported, not restated): START r = V_t/(V_t-1 + F_t) - 1; END r = (V_t - F_t)/V_t-1 - 1;
the segment's first day keeps its served return under both.

Usage: python flow_timing_e3.py <repo_root> [--cache <pickle>]
"""
import importlib.util
import json
import pickle
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
D = HERE.parent
R17_PATH = D / "0.9.0_WK_IRPT_DASHBD~12" / "tieout_e2.py"
_spec = importlib.util.spec_from_file_location("tieout_e2_r17", str(R17_PATH))
r17 = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(r17)
COMP_REL = "org/missions/D9/IRPT/IRPT_DASHBD/deliverables/0.9.0_WK_IRPT_DASHBD~34/TIEOUT_COMPOUND_E1.json"
TOL = 0.35


def key(s):
    return (s["account"], s["segment"]["start"], s["segment"]["end"])


def grade(seg_row, days):
    gross = seg_row["bd_gross_return"]
    start = r17.link_alt_flow(days, "START")
    end = r17.link_alt_flow(days, "END")
    a, b = abs(gross - start) * 100.0, abs(gross - end) * 100.0
    return {"account": seg_row["account"], "segment": seg_row["segment"], "abs_diff_pp_flow_start": a,
            "abs_diff_pp_flow_end": b, "swing_pp": b - a}


def main():
    root = Path(sys.argv[1]).resolve()
    cache = sys.argv[sys.argv.index("--cache") + 1] if "--cache" in sys.argv else None
    comp = json.loads((root / COMP_REL).read_bytes().decode("utf-8"))
    pop = [s for s in comp["segments"] if s["abs_diff_pp"] > TOL and s.get("reason") == "FLOW_TIMING"]
    accts = sorted({s["account"] for s in pop})
    if cache and Path(cache).is_file():
        with open(cache, "rb") as f:
            gold, n_part, n_gold = pickle.load(f)
    else:
        import boto3
        from botocore.config import Config
        s3 = boto3.client("s3", region_name="us-east-1", config=Config(
            read_timeout=60, retries={"max_attempts": 8, "mode": "standard"}, max_pool_connections=32))
        gold, n_part, n_gold = r17.read_gold(s3, accts)
        if cache:
            with open(cache, "wb") as f:
                pickle.dump((gold, n_part, n_gold), f)
    rows, served_vs_end = [], 0
    for s in pop:
        days = r17.segment_days(gold.get(s["account"]), s["segment"])
        if not days or len(days) != s["opal_days"]:
            raise SystemExit("ERROR: served days for a population segment differ from the record (%s)" % (s["segment"],))
        if abs(r17.link([d["r"] for d in days]) - s["opal_return"]) > 1e-9:
            raise SystemExit("ERROR: served link differs from the record's opal_return")
        rows.append(grade(s, days))
        if abs(r17.link_alt_flow(days, "END") - s["opal_return"]) > 1e-9:
            served_vs_end += 1
    ws = sum(1 for x in rows if x["abs_diff_pp_flow_start"] <= TOL)
    we = sum(1 for x in rows if x["abs_diff_pp_flow_end"] <= TOL)
    sw = sorted(x["swing_pp"] for x in rows)
    n = len(sw)
    dist = {"min": sw[0], "p25": sw[n // 4], "median": sw[n // 2], "p75": sw[(3 * n) // 4], "max": sw[-1],
            "negative_end_closer": sum(1 for v in sw if v < 0), "zero": sum(1 for v in sw if v == 0),
            "positive_start_closer": sum(1 for v in sw if v > 0)}
    rec = {"measured_by": "0.9.0_WK_IRPT_DASHBD~37", "claim": "measured", "task_order": "IRPT_DASHBD.TO-DB-b-59",
           "tolerance_pp": TOL, "vendor_calls": 0, "population": n,
           "rows": rows, "within_flow_start": ws, "within_flow_end": we, "adopted": None, "swing_distribution_pp": dist,
           "end_relink_differs_from_served_link": served_vs_end,
           "method": "For each compounded segment with abs_diff_pp > 0.35 and reason FLOW_TIMING, Opal's linked return is recomputed from the "
                     "served gold (market_value_eod, external_flow) by round 17's link_alt_flow under START (r = V_t/(V_t-1 + F_t) - 1) and "
                     "END (r = (V_t - F_t)/V_t-1 - 1); the first in-segment day keeps its served return. Each is compared with the record's "
                     "bd_gross_return (compounded gross). abs_diff_pp_flow_X = |bd_gross - opal_X| * 100; swing_pp = end - start. "
                     "within_* count abs_diff <= 0.35. No convention is adopted.",
           "files_read": {"compound_record": COMP_REL, "reader": "org/missions/D9/IRPT/IRPT_DASHBD/deliverables/0.9.0_WK_IRPT_DASHBD~12/tieout_e2.py",
                          "served_series": "s3://%s/%sdate=<YYYY-MM-DD>/data.parquet (%d partitions; market_value_eod, external_flow, total_return_daily)" % (
                              r17.GOLD_BUCKET, r17.GOLD_PREFIX, n_part), "served_accounts_in_series": n_gold,
                          "population_accounts": len(accts)}}
    (HERE / "FLOW_TIMING_E3.json").write_bytes((json.dumps(rec, indent=1) + "\n").encode("utf-8"))
    md = ["# FLOW_TIMING_E3 (IRPT_DASHBD round 31, TO-DB-b-59) -- counts only", "",
          "Population: %d compounded misses (abs_diff_pp > 0.35, reason FLOW_TIMING)." % n,
          "Within 0.35 pp with each external flow at the START of its day: %d of %d." % (ws, n),
          "Within 0.35 pp with each external flow at the END of its day: %d of %d." % (we, n),
          "Adopted convention: none (null). The counts go to the CTO.", "",
          "Swing (end minus start, pp): min %.4f, p25 %.4f, median %.4f, p75 %.4f, max %.4f." % (
              dist["min"], dist["p25"], dist["median"], dist["p75"], dist["max"]),
          "Rows where START is closer to BD: %d; END closer: %d; equal: %d." % (
              dist["positive_start_closer"], dist["negative_end_closer"], dist["zero"]),
          "Rows where the END re-link differs from the served link: %d of %d." % (served_vs_end, n), "",
          "Method and per-segment rows: FLOW_TIMING_E3.json.", ""]
    (HERE / "FLOW_TIMING_E3.md").write_bytes("\n".join(md).encode("utf-8"))
    print("OK: population %d within_start %d within_end %d end_vs_served_differs %d" % (n, ws, we, served_vs_end))
    print(json.dumps(dist, indent=1))


if __name__ == "__main__":
    main()
