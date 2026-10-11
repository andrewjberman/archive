"""MDPF_STRATID round 2 -- the one real run read for FWD-2 and FWD-6 (read-only S3; writes nothing).

Reads the served Global aggregate timeseries + category view for the latest run date, and the served Cottonwood slice, then checks on
Global's last date:
  FWD-2  every Cottonwood cohort_class sma member with a value is either COUNTED under its bucket at Global (its additive by_model
         entry carries value - overlap) or NAMED in sma_additive_withheld (reason OVERLAP / OVERLAP_UNMEASURED); none is silent.
  FWD-6  every Global SMA tree member states inside_model_figure (bool) and held_out (list); each Cottonwood member with overlap > 0
         is in its row's held_out with that overlap; each additive entry carries inside_model_value.
  FWD-7  the Cottonwood slice carries unidentified_strategies {as_of, names_scanned > 0, rows of {firm_id, name, dollars, reason}}.
  TOTAL  Global opal_aggregate_aua = base_excluding_tax_aua + tax_additive_aua + sma_additive_aua on that date (within a cent), and
         Client equals the pre-deploy Client when --pre-client is given.
Prints R2-RUN-READ PASS or FAIL with the failed item named.

usage: python r2_run_read.py [--pre-client <float>]
"""
from __future__ import annotations

import argparse
import json
import sys

import boto3

B = "opal-data-assets"
COT = "gold/mdpf_revamp/cottonwood/aggregate_aua_timeseries.json"


def latest(s3, prefix):
    keys = []
    for p in s3.get_paginator("list_objects_v2").paginate(Bucket=B, Prefix=prefix):
        keys += [o["Key"] for o in p.get("Contents", []) if o["Key"].endswith(".json")]
    return sorted(keys)[-1]


def get(s3, key):
    o = s3.get_object(Bucket=B, Key=key)
    return json.loads(o["Body"].read()), o.get("VersionId"), o["LastModified"].isoformat()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--pre-client", type=float, default=None)
    a = ap.parse_args()
    s3 = boto3.client("s3")
    gk = latest(s3, "portal/gold/mdpf/global/aggregate-aua-timeseries/")
    g, gv, gm = get(s3, gk)
    cv, cvv, cvm = get(s3, gk.replace("aggregate-aua-timeseries", "category-views"))
    cot, cotv, cotm = get(s3, COT)
    print("inputs: %s v=%s %s | category-views v=%s %s | %s v=%s %s" % (gk, gv, gm, cvv, cvm, COT, cotv, cotm))
    day, i = g["dates"][-1], len(g["dates"]) - 1
    fails = []
    withheld = {(w["member_id"], w["firm_id"]): w for w in (g.get("sma_additive_withheld") or []) if w.get("date") == day}
    rows = {}
    for bucket, b in cv["nodes"]["SMA"]["children"].items():
        for m in b["members"]:
            rows[m["member_id"]] = (bucket, m)
            if "inside_model_figure" not in m or "held_out" not in m:
                fails.append("FWD-6 row %s lacks inside_model_figure/held_out" % m["member_id"])
    for mid, e in cot["by_model"].items():
        if e.get("cohort_class") != "sma" or day not in cot["dates"]:
            continue
        ci = cot["dates"].index(day)
        v = e["model_value"][ci]
        if v is None:
            continue
        ov = (e.get("overlap_model_value") or [None] * len(cot["dates"]))[ci]
        be = g["by_model"].get(mid) or {}
        counted = (be.get("model_value") or [None] * (i + 1))[i] if be.get("source_basis") == "additive" and "cottonwood" in (be.get("firms") or []) else None
        w = withheld.get((mid, "cottonwood"))
        state = "counted %.2f" % counted if counted else ""
        if w:
            state += " held_out %s %.2f" % (w["reason"], w["value"])
        if not state:
            fails.append("FWD-2 Cottonwood %s value %.2f is neither counted nor named withheld" % (mid, v))
        row = rows.get(mid, (None, {}))[1]
        if ov and ov > 0:
            ho = [h for h in row.get("held_out", []) if h.get("firm_id") == "cottonwood"]
            if not ho or abs(ho[0]["value"] - ov) > 0.01:
                fails.append("FWD-6 %s overlap %.2f not in its row's held_out" % (mid, ov))
        if counted is not None and "inside_model_value" not in be:
            fails.append("FWD-6 by_model[%s] lacks inside_model_value" % mid)
        print("  %s bucket=%s value %.2f overlap %r -> %s | row inside_model_figure=%r held_out=%r"
              % (mid, rows.get(mid, ("-",))[0], v, ov, state.strip(), row.get("inside_model_figure"), row.get("held_out")))
    ub = cot.get("unidentified_strategies")
    if not isinstance(ub, dict):
        fails.append("FWD-7 the Cottonwood slice carries no unidentified_strategies block")
    else:
        bad = [r for r in ub.get("rows", []) if set(r) < {"firm_id", "name", "dollars", "reason"}]
        if bad or not (ub.get("names_scanned") or 0) > 0:
            fails.append("FWD-7 block malformed (names_scanned %r, %d rows lacking a field)" % (ub.get("names_scanned"), len(bad)))
        # Names only, never an account id (CTO half condition 5): the list is keyed by sleeve/model name.
        print("  FWD-7 as_of %s names_scanned %s listed %d: %s" % (ub.get("as_of"), ub.get("names_scanned"), len(ub.get("rows", [])),
              [(r["name"], round(r["dollars"] or 0, 2), r["reason"]) for r in ub.get("rows", [])]))
    t = g["opal_aggregate_aua"][i]
    parts = [g.get(k, [None] * (i + 1))[i] or 0.0 for k in ("base_excluding_tax_aua", "tax_additive_aua", "sma_additive_aua")]
    if abs(t - sum(parts)) > 0.01:
        fails.append("TOTAL %.2f != base + tax + sma %.2f" % (t, sum(parts)))
    client = cv["nodes"]["Client"]["aum"]
    if a.pre_client is not None and abs(client - a.pre_client) > 0.02:
        fails.append("Client %.2f moved from %.2f" % (client, a.pre_client))
    print("day %s total %.2f = base %.2f + tax %.2f + sma %.2f | SMA %.2f | Client %.2f"
          % (day, t, parts[0], parts[1], parts[2], cv["nodes"]["SMA"]["aum"], client))
    print("R2-RUN-READ %s%s" % ("PASS" if not fails else "FAIL", "" if not fails else " -- " + "; ".join(fails)))
    return 0 if not fails else 1


if __name__ == "__main__":
    sys.exit(main())
