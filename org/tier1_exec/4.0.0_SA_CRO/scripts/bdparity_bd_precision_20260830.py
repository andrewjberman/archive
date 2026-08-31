"""ADVI_BDPARITY BP1-4 -- BD's RETURNED PRECISION and payload shape, read from bronze bytes already pulled.

No vendor call: reads reporting_performance_<bd_id>_<q_end>.json objects copied from
s3://opal-data-assets/blackdiamond/49f/bronze/reporting_performance/<pull_date>/ into --bronze-dir.
Prints, per object: top-level keys, level.startDate (BD's inception), the literal digits of every
timeWeightedReturns.return as SENT (regex over the raw text, not the parsed float), the distinct
decimal-place counts, and every dateRangePoint's (range, return, returnAnnualized, daysHeld,
periodLength, BMV, EMV). Target-specific: the BD response schema (4.0.0_SA_CRO, 2026-08-30).
"""
import argparse
import json
import os
import re


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--bronze-dir", required=True)
    ap.add_argument("--ids", default="13477111,18927251,21089351,22596361,23221671")
    ap.add_argument("--q-end", default="2026-08-28")
    a = ap.parse_args()
    for bd_id in a.ids.split(","):
        p = os.path.join(a.bronze_dir, "reporting_performance_%s_%s.json" % (bd_id, a.q_end))
        if not os.path.exists(p):
            p = os.path.join(a.bronze_dir, "perf_%s.json" % bd_id)
        raw = open(p, encoding="utf-8").read()
        d = json.loads(raw)
        lvl = d["combinedLevels"][0]
        print("=== %s  bytes=%d  top-level keys=%s" % (bd_id, len(raw), sorted(d.keys())))
        print("  level.startDate=%s dataDate=%s nLevels=%d nRangePoints=%d"
              % (lvl.get("startDate"), d.get("dataDate"), len(d["combinedLevels"]), len(lvl["dateRangePoints"])))
        lits = re.findall(r'"timeWeightedReturns"\s*:\s*\{[^}]*?"return"\s*:\s*(-?[0-9][0-9.eE+-]*)', raw)
        decs = sorted({len(x.split(".")[1]) if "." in x and "e" not in x.lower() else -1 for x in lits})
        print("  literal 'return' digits as sent (first 6): %s" % lits[:6])
        print("  distinct decimal-place counts across %d literals: %s" % (len(lits), decs))
        for i, e in enumerate(lvl["dateRangePoints"]):
            dr = e["dateRange"]
            twr = e.get("timeWeightedReturns") or {}
            print("   [%d] %s..%s ret=%r ann=%r daysHeld=%r periodLength=%r bmv=%r emv=%r" % (
                i, str(dr.get("startDate"))[:10], str(dr.get("endDate"))[:10], twr.get("return"),
                twr.get("returnAnnualized"), twr.get("daysHeld"), twr.get("periodLength"),
                e.get("beginningMarketValue"), e.get("endingMarketValue")))


if __name__ == "__main__":
    main()
