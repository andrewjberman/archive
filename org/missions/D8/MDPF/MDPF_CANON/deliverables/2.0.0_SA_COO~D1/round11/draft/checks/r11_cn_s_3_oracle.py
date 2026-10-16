#!/usr/bin/env python3
"""MDPF_CANON round 11 cell CN-s-3 (the Cottonwood Trend, CRO spec base) -- DRAFT reference oracle, 2.0.0_SA_COO~D1, 2026-10-16. Not issued.

The CRO spec (org/tier1_exec/4.0.0_SA_CRO/deliverables/MDPF_CANON_COTTONWOOD_AUM_TREND_UPGRADE_SPEC_20261015.md @21caa664be) states a rule per group
and a month-end oracle. This script derives the groups from the SERVED Cottonwood object by that rule and grades them against the spec, so any
implementation of the cell (portal or producer) has one independent answer to match. It reads a local copy of the served object (the issuer
downloads it first; this script reads no S3):

  python r11_cn_s_3_oracle.py oracle --object <cottonwood aggregate-aua-timeseries .json>

Arms (O5 is a control: the pre-fix rule must fail the oracle, so the oracle can fail):
  O1 the window starts at the first total-bearing date (2026-06-09) and holds 89 rows on the 2026-10-14 object
  O2 the five primary lines + Custom + Other sum to the Total on every window row (within $0.005), no negative group
  O3 the month-end oracle at the five period ends (+-$0.05M per cell)
  O4 the 12 absent model-leg dates take the last measured model leg, are listed carried, and keep their measured Total
  O5 control: Other taken as the served non_model_aua (today's drawing) misses the 2026-06-30 oracle (non_model_aua is None before 2026-07-20)

The oracle is for the object BEFORE CN-s-1 (Muni still in Other). After CN-s-1 Custom rises and Other falls by the Opal_Muni_Income account on
every date it holds a value; the order re-bases O3 then.   ASCII only.
"""
import json
import sys

PRIMARY = (("UST", "opal_ultra_short_term"), ("ST", "opal_short_term"), ("INT", "opal_intermediate"),
           ("LT", "opal_long_term_conservative"), ("ULT", "opal_long_term_aggressive"))
# spec oracle, $M: period end -> UST, ST, INT, LT, ULT, Custom, Other, Total
ORACLE = (
    ("2026-06-30", 0.0, 0.0, 4.2, 1.0, 0.0, 0.0, 431.4, 436.7),
    ("2026-07-31", 1.4, 16.3, 74.9, 31.3, 1.1, 6.2, 338.8, 470.1),
    ("2026-08-31", 18.5, 18.4, 80.3, 59.5, 1.1, 15.0, 283.7, 476.5),
    ("2026-09-30", 18.2, 21.2, 81.4, 56.7, 1.0, 24.0, 338.8, 541.3),
    ("2026-10-14", 18.2, 22.0, 82.0, 56.6, 1.4, 24.8, 348.6, 553.7),
)
M = 1_000_000.0


def num(x):
    return x if isinstance(x, (int, float)) and not isinstance(x, bool) else None


def derive(d, other_rule="total_minus_model"):
    dates, total, maua = d["dates"], d["partner_custody_total"], d["model_aua"]
    nm = d["non_model_aua"]
    legs = {k: d["by_model"][key]["model_value"] for k, key in PRIMARY}
    first = next(i for i, t in enumerate(total) if num(t) is not None)
    rows, last, carried = [], None, []
    for i in range(first, len(dates)):
        t = num(total[i])
        if t is None:
            continue
        # The model leg is ABSENT on a date when model_aua is None (the 12 exceptions). Where model_aua is present, a primary model with no
        # value is a model with no accounts yet: the spec oracle prints it as 0.0 (UST, ST, ULT at 2026-06-30), so it reads 0.0 here.
        have = num(maua[i]) is not None
        if have:
            leg = {k: (num(legs[k][i]) or 0.0) for k, _ in PRIMARY}
            leg["model_aua"] = maua[i]
            last = leg
            is_carried = False
        else:
            if last is None:
                continue
            leg, is_carried = last, True
            carried.append(dates[i])
        five = sum(leg[k] for k, _ in PRIMARY)
        custom = leg["model_aua"] - five
        other = (t - leg["model_aua"]) if other_rule == "total_minus_model" else num(nm[i])
        rows.append({"date": dates[i], "total": t, "prim": {k: leg[k] for k, _ in PRIMARY}, "custom": custom, "other": other, "carried": is_carried})
    return rows, carried


def at(rows, end):
    cand = [r for r in rows if r["date"] <= end]
    return cand[-1] if cand else None


def cells(r):
    return [r["prim"][k] / M for k, _ in PRIMARY] + [r["custom"] / M, (r["other"] or 0.0) / M, r["total"] / M]


def oracle(path):
    d = json.load(open(path, encoding="utf-8"))
    rows, carried = derive(d)
    arms = []
    arms.append(("O1 window", bool(rows) and rows[0]["date"] == "2026-06-09" and len(rows) == 89, "%s rows from %s" % (len(rows), rows[0]["date"] if rows else None)))
    bad = [r["date"] for r in rows if abs(sum(r["prim"].values()) + r["custom"] + r["other"] - r["total"]) > 0.005 or min(list(r["prim"].values()) + [r["custom"], r["other"]]) < -0.005]
    arms.append(("O2 exact partition, no negative group", not bad, "offending %s" % bad[:5]))
    miss = []
    for end, *want in ORACLE:
        r = at(rows, end)
        got = cells(r) if r else None
        if not got or any(abs(g - w) > 0.05 for g, w in zip(got, want)):
            miss.append((end, [round(x, 2) for x in got] if got else None, want))
    arms.append(("O3 month-end oracle", not miss, "misses %s" % miss[:2]))
    exc = sorted((d.get("meta", {}).get("channel_participation", {}).get("exceptions") or {}).keys())
    ok4 = exc == sorted(carried) and len(exc) == 12 and all(at(rows, x)["total"] == d["partner_custody_total"][d["dates"].index(x)] for x in exc)
    arms.append(("O4 12 carried dates, measured Total kept", ok4, "exceptions %d carried %d" % (len(exc), len(carried))))
    rows_c, _ = derive(d, "served_non_model")
    r630 = at(rows_c, "2026-06-30")
    wrong = r630 is None or abs((r630["other"] or 0.0) / M - 431.4) > 0.05
    arms.append(("O5 control: the served non_model_aua rule misses the oracle", wrong, "Other at 2026-06-30 = %s" % (None if r630 is None else r630["other"])))
    k = 0
    for name, ok, detail in arms:
        k += 1 if ok else 0
        print("  %s %s%s" % ("PASS" if ok else "FAIL", name, "" if ok else "  -- " + str(detail)[:240]))
    print("ROUND 11 CN-S-3 ORACLE: %d of %d arms" % (k, len(arms)))
    return 0 if k == len(arms) else 1


if __name__ == "__main__":
    if len(sys.argv) >= 4 and sys.argv[1] == "oracle" and sys.argv[2] == "--object":
        sys.exit(oracle(sys.argv[3]))
    print(__doc__)
    sys.exit(2)
