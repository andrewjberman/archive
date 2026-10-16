#!/usr/bin/env python3
"""MDPF_CANON round 11 -- grade a D4 response against the V2 never-widen pair (section 1 and the restated hard STOP).

  python grade_d4_v2.py --response <d4 response json> --baseline <dir of <scope>__<type>.json> [--against <earlier d4 response>]

Prints counts, dates and paths only (aggregates on the dated model leg are printed as a pass flag, never a value).
Exit 0 only when every arm passes. With --against, arm V10 compares this response to an earlier graded one: the two must
be identical on every body except the volatile paths. ASCII only.
"""
import argparse
import json
import os
import sys

SCOPES = ("global", "49financial", "inflection", "cottonwood")
TYPES = ("account-distribution", "aggregate-aua-timeseries", "aum-metrics", "category-views")
DATES7 = ["2026-10-07", "2026-10-08", "2026-10-09", "2026-10-12", "2026-10-13", "2026-10-14", "2026-10-15"]
VOLATILE = ("/_provenance/process_time", "/_provenance/trigger", "/_provenance/source_vintage_age_hours",
            "/generated_at", "/last_updated", "/meta/generated_at")
res = []


def vol(p):
    """a volatile path: the named ones, or any nested generated_at timestamp"""
    return p in VOLATILE or p.endswith("/generated_at")


def arm(name, ok, note=""):
    res.append(bool(ok))
    print("  %-4s %s %s" % (name, "PASS" if ok else "FAIL", note))


def load(resp_path):
    r = json.load(open(resp_path, encoding="utf-8"))
    out = {}
    for k, v in r["bodies"].items():
        p = k.split("/")
        out[(p[-3], p[-2])] = json.loads(v["body"])
    return r, out


def diffs(a, b, path="", out=None):
    out = [] if out is None else out
    if isinstance(a, dict) and isinstance(b, dict):
        for k in sorted(set(a) | set(b), key=str):
            if k not in a or k not in b:
                out.append(path + "/" + str(k))
            else:
                diffs(a[k], b[k], path + "/" + str(k), out)
    elif isinstance(a, list) and isinstance(b, list):
        if len(a) != len(b):
            out.append(path + "[len]")
        for i in range(min(len(a), len(b))):
            if json.dumps(a[i], sort_keys=True, default=str) != json.dumps(b[i], sort_keys=True, default=str):
                out.append(path + "[%d]" % i)
    elif a != b:
        out.append(path)
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--response", required=True)
    ap.add_argument("--baseline", required=True)
    ap.add_argument("--against")
    a = ap.parse_args()
    r, new = load(a.response)
    old = {(s, t): json.load(open(os.path.join(a.baseline, "%s__%s.json" % (s, t)), encoding="utf-8")) for s in SCOPES for t in TYPES}
    arm("V0", r.get("status") == "green" and r.get("errors") == [] and r.get("a4_objects_built") == 16 and len(new) == 16,
        "status=%s errors=%s built=%s bodies=%d" % (r.get("status"), r.get("errors"), r.get("a4_objects_built"), len(new)))
    c0, c1 = old[("cottonwood", "aggregate-aua-timeseries")], new[("cottonwood", "aggregate-aua-timeseries")]
    g0, g1 = old[("global", "aggregate-aua-timeseries")], new[("global", "aggregate-aua-timeseries")]
    cd, gd = c0["dates"], g0["dates"]
    arm("V1", c1["dates"] == cd and g1["dates"] == gd, "axes equal (same as-of date)")

    def delta(x, y, key, dates):
        return {d: (None if x[key][i] is None or y[key][i] is None else round(y[key][i] - x[key][i], 2)) for i, d in enumerate(dates)}
    cm, cn, cp = delta(c0, c1, "model_aua", cd), delta(c0, c1, "non_model_aua", cd), delta(c0, c1, "partner_custody_total", cd)
    Z = (0, 0.0, None)   # a date where either side is null has no delta: not a move
    moved = sorted(d for d, v in cm.items() if v not in Z)
    arm("V2", moved == DATES7, "Cottonwood model_aua moved on exactly the 7 dates: %s" % (moved == DATES7))
    arm("V3", all(cn[d] == -cm[d] for d in DATES7) and all(v in Z for d, v in cn.items() if d not in DATES7),
        "non_model_aua = -model_aua delta on the 7 dates, 0 elsewhere")
    arm("V4", all(v in (0, 0.0, None) for v in cp.values()) and c0["partner_custody_total"] == c1["partner_custody_total"],
        "Cottonwood partner_custody_total EQUAL on every date")
    gmod = {k: delta(g0, g1, k, gd) for k in ("model_aua", "opal_aggregate_aua", "base_excluding_tax_aua")}
    om = {k: delta(g0["by_model"]["other_models"], g1["by_model"]["other_models"], k, gd) for k in ("model_value", "account_count")}
    arm("V5", all(gmod[k][d] == cm[d] for k in gmod for d in DATES7) and all(gmod[k][d] in Z for k in gmod for d in gd if d not in DATES7),
        "Global model_aua, opal_aggregate_aua, base_excluding_tax_aua rise by the Cottonwood delta on the 7 dates, 0 elsewhere")
    arm("V6", all(om["model_value"][d] == cm[d] for d in DATES7) and all(om["account_count"][d] == 1 for d in DATES7)
        and all(om[k][d] in Z for k in om for d in gd if d not in DATES7),
        "Global other_models.model_value = delta, account_count +1 on the 7 dates, 0 elsewhere")
    arm("V7", g0["non_model_aua"] == g1["non_model_aua"] and g0["by_model"].keys() == g1["by_model"].keys(),
        "Global non_model_aua EQUAL; Global by_model keys unchanged (no new key)")
    # V8: no dated array cell before 2026-10-07 moves in any scope; any array aligned to the axis is checked
    bad = []
    for s in SCOPES:
        for t in TYPES:
            o, n = old[(s, t)], new[(s, t)]
            ax = o.get("dates")
            if not ax:
                continue
            for k, v in o.items():
                if isinstance(v, list) and len(v) == len(ax) and isinstance(n.get(k), list) and len(n[k]) == len(ax):
                    for i, d in enumerate(ax):
                        if d < "2026-10-07" and json.dumps(v[i], sort_keys=True, default=str) != json.dumps(n[k][i], sort_keys=True, default=str):
                            bad.append((s, t, k, d))
    arm("V8", not bad, "no axis-aligned cell before 2026-10-07 moved (%d found)" % len(bad))
    # V9: 49financial and inflection: only volatile paths and the category-views Custom members list
    odd = []
    for s in ("49financial", "inflection"):
        for t in TYPES:
            for p in diffs(old[(s, t)], new[(s, t)]):
                if vol(p) or p.startswith("/nodes/Models/children/Custom/members"):
                    continue
                odd.append((s, t, p))
    arm("V9", not odd, "49financial/inflection differ only in volatile fields and the Custom members list (%d other)" % len(odd))
    if a.against:
        _, prev = load(a.against)
        other = []
        for key in new:
            for p in diffs(prev[key], new[key]):
                if not vol(p):
                    other.append((key, p))
        arm("V10", not other and set(prev) == set(new), "identical to the earlier graded response except volatile paths (%d other)" % len(other))
    ok = all(res)
    print("D4 V2 GRADE: %d of %d arms pass -- %s" % (sum(res), len(res), "PASS" if ok else "STOP"))
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
