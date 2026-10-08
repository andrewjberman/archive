"""TO-DB-b-49 (IRPT_DASHBD round 28, DB-b-49): tie out Black Diamond's split figures (either side of the 2025-01-09 closure) against
Opal's served returns for the 2,299 closure segments. READ-ONLY: S3 GETs/LISTs only; zero vendor calls. Reuses the round-18 readers and
grading by import (tieout_e2_gross.py, which itself imports the round-17 readers): the BD gross basis (net twr + fee add-back) and Opal's
linked total_return_daily are NOT restated here.

Usage: python tieout_split_e1.py <repo_root> [--cache <pickle>]
Writes TIEOUT_SPLIT_E1.json and TIEOUT_SPLIT_E1.md beside this file. The .md is counts only.
"""
import importlib.util
import json
import pickle
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
D = HERE.parent
_spec = importlib.util.spec_from_file_location("tieout_e2_gross_r18", str(D / "0.9.0_WK_IRPT_DASHBD~13" / "tieout_e2_gross.py"))
r18 = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(r18)
r17 = r18.r17

SPLIT_PREFIX = "blackdiamond/49financial/bronze/reporting_performance/pull=split20261007/"
r17.BRONZE_PREFIX = SPLIT_PREFIX            # read_bronze reads this module global at call time
PLAN = D / "0.9.0_WK_IRPT_DASHBD~25" / "SPLIT_PULL_PLAN.json"
FULL = D / "0.9.0_WK_IRPT_DASHBD~13" / "TIEOUT_49F_BD_POPULATION_E2_GROSS.json"
TOL = r18.TOLERANCE_PP
COLUMN = "total_return_daily"


def half(acct, seg, gold, pts, bd_acct):
    """One half: {bd_return (gross), opal_return, abs_diff_pp, tied} or the same keys null with a `reason`."""
    bd = pts.get((seg["start"], seg["end"])) if isinstance(pts, dict) else None
    g = r18.grade_segment(acct, seg, r17.segment_days(gold.get(acct), seg), bd)
    out = {"range": {"start": seg["start"], "end": seg["end"]}, "bd_return": g.get("bd_gross_return"),
           "opal_return": g.get("opal_return"), "abs_diff_pp": g.get("abs_diff_pp"), "tied": None}
    if out["abs_diff_pp"] is None:
        why = g.get("why") or ""
        if why.startswith("BD_NO_RESPONSE"):
            if isinstance(pts, str):
                why = "BD_NO_RESPONSE: " + pts
            elif pts is None:
                why = "BD_NO_RESPONSE: no landed object for the bd account"
            else:
                why = "BD_NO_RESPONSE: the landed response holds no account-level point for this range"
        out["reason"] = why or "figure not readable"
        out["bd_return"] = None
    else:
        out["tied"] = out["abs_diff_pp"] <= TOL
        out["bd_net_return"] = g.get("bd_return")
        out["bd_fee_addback"] = g.get("bd_fee_addback")
    return out


def main():
    cache = sys.argv[sys.argv.index("--cache") + 1] if "--cache" in sys.argv else None
    plan = json.loads(PLAN.read_bytes().decode("utf-8"))
    reqs = plan["request_list"]
    if cache and Path(cache).is_file():
        with open(cache, "rb") as f:
            n_obj, bronze, gold, n_part, n_gold_accts = pickle.load(f)
    else:
        import boto3
        from botocore.config import Config
        s3 = boto3.client("s3", region_name="us-east-1", config=Config(
            read_timeout=60, retries={"max_attempts": 8, "mode": "standard"}, max_pool_connections=32))
        n_obj, bronze = r17.read_bronze(s3, [q["bd_account"] for q in reqs])
        gold, n_part, n_gold_accts = r17.read_gold(s3, [q["account"] for q in reqs])
        if cache:
            with open(cache, "wb") as f:
                pickle.dump((n_obj, bronze, gold, n_part, n_gold_accts), f)

    full = {}
    for s in json.loads(FULL.read_bytes().decode("utf-8"))["segments"]:
        full[(s["account"], s["segment"]["start"], s["segment"]["end"])] = s.get("bd_gross_return")

    rows = []
    rc_compared = rc_within = rc_unreadable = 0
    rc_max = 0.0
    for q in reqs:
        a, bda = q["account"], str(q["bd_account"])
        pts = bronze.get(bda)
        L, R = q["ranges"]
        left = half(a, {"start": L["start"], "end": L["end"]}, gold, pts, bda)
        right = half(a, {"start": R["start"], "end": R["end"]}, gold, pts, bda)
        row = {"account": a, "left": left, "right": right}
        fg = full.get((a, L["start"], R["end"]))
        if left["bd_return"] is not None and right["bd_return"] is not None and fg is not None:
            chained = (1.0 + left["bd_return"]) * (1.0 + right["bd_return"]) - 1.0
            d = abs(chained - fg) * 100.0
            row["recompose"] = {"chained": chained, "bd_full_gross": fg, "abs_diff_pp": d, "within": d <= TOL}
            rc_compared += 1
            rc_within += 1 if d <= TOL else 0
            rc_max = max(rc_max, d)
        else:
            rc_unreadable += 1
            row["recompose"] = {"reason": "a BD half or the round-18 full-segment gross is not readable"}
        rows.append(row)

    c = {"tied_both": 0, "tied_left_only": 0, "tied_right_only": 0, "tied_neither": 0, "absent": 0}
    for r in rows:
        lt, rt = r["left"]["tied"], r["right"]["tied"]
        if lt is None or rt is None:
            c["absent"] += 1
        elif lt and rt:
            c["tied_both"] += 1
        elif lt:
            c["tied_left_only"] += 1
        elif rt:
            c["tied_right_only"] += 1
        else:
            c["tied_neither"] += 1
    n = len(rows)
    branch = "A" if c["tied_both"] > n / 2 else "B"
    left_graded = sum(1 for r in rows if r["left"]["tied"] is not None)
    right_graded = sum(1 for r in rows if r["right"]["tied"] is not None)
    left_tied = sum(1 for r in rows if r["left"]["tied"])
    right_tied = sum(1 for r in rows if r["right"]["tied"])
    rec = {"measured_by": "0.9.0_WK_IRPT_DASHBD~28", "claim": "measured", "task_order": "IRPT_DASHBD.TO-DB-b-49",
           "basis": "GROSS (BD net twr plus BD's own fee add-back, round-18 reader)", "tolerance_pp": TOL, "vendor_calls": 0,
           "column_used": COLUMN, "files_read": n_obj,
           "inputs": {"bronze_prefix": "s3://%s/%s" % (r17.BRONZE_BUCKET, SPLIT_PREFIX),
                      "served_series": "s3://%s/%sdate=<YYYY-MM-DD>/data.parquet (%d partitions; column %s)" % (
                          r17.GOLD_BUCKET, r17.GOLD_PREFIX, n_part, COLUMN),
                      "served_accounts": n_gold_accts, "plan_accounts_requested": n,
                      "round18_record": "deliverables/0.9.0_WK_IRPT_DASHBD~13/TIEOUT_49F_BD_POPULATION_E2_GROSS.json"},
           "rule": "branch A iff tied_both > 1149.5 of 2299, else B; absent = either half has no readable figure (reason named per half)",
           "counts": c, "branch": branch,
           "per_half": {"left_graded": left_graded, "left_tied": left_tied, "right_graded": right_graded, "right_tied": right_tied},
           "recompose": {"compared": rc_compared, "within_tolerance": rc_within, "not_comparable": rc_unreadable,
                         "max_abs_diff_pp": rc_max, "tolerance_pp": TOL,
                         "method": "(1+left)(1+right)-1 on BD gross halves against BD gross full-segment in the round-18 record"},
           "rows": rows}
    (HERE / "TIEOUT_SPLIT_E1.json").write_bytes((json.dumps(rec, indent=1) + "\n").encode("utf-8"))
    md = ["# TIEOUT_SPLIT_E1 -- BD split figures vs Opal served, 2,299 closure segments (counts only)", "",
          "Basis: gross (round-18 reader), tolerance %.2f pp, column %s, vendor calls 0. Landed objects read: %d." % (TOL, COLUMN, n_obj), "",
          "| count | accounts |", "|---|---|"]
    md += ["| %s | %d |" % (k, c[k]) for k in ("tied_both", "tied_left_only", "tied_right_only", "tied_neither", "absent")]
    md += ["| total | %d |" % n, "",
           "Left half graded %d, tied %d. Right half graded %d, tied %d." % (left_graded, left_tied, right_graded, right_tied), "",
           "Branch: **%s** (rule: A iff tied_both > 1,149.5 of 2,299; tied_both = %d)." % (branch, c["tied_both"]), "",
           "Recompose control: %d compared, %d within 0.35 pp, %d not comparable, max abs diff %.4f pp." % (
               rc_compared, rc_within, rc_unreadable, rc_max), ""]
    (HERE / "TIEOUT_SPLIT_E1.md").write_bytes(("\n".join(md)).encode("ascii"))
    print("OK: files %d rows %d counts %s branch %s recompose %d/%d" % (n_obj, n, c, branch, rc_within, rc_compared))


if __name__ == "__main__":
    main()
