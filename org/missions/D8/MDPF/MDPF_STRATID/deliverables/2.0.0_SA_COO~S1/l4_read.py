"""MDPF_STRATID R1 ledger L4 read (FWD-1): the first SCHEDULED mdpf-gold-lambda run after D2.

Usage: python l4_read.py <pre_dir> <post_dir>
  Each dir holds 12 files named <scope>__<view>.json, scope in global/49financial/inflection/cottonwood,
  view in aggregate-aua-timeseries/category-views/aum-metrics. pre = the 2026-10-07 run-date objects
  (version ids in PREFIRE_SNAPSHOT_20261009.md); post = the run date the fire writes.

Checks (pair NEVER_WIDEN_PAIR_R1_GLOBAL_PFDE_FOLD.md sections 4-6, CTO~DELL1 msg 1575):
  A  per-firm history: every per-date figure on every date pre carries is equal in post, ignoring the two
     admitted keys. Any moved figure prints STOP.
  B  per-firm admitted keys: sma_additive_aua all None, sma_additive_withheld == [].
  C  Global: SMA > ETF Strategies > PFDE == Cottonwood served PFDE on the post date; sma_additive_aua on that
     date == it (overlap 0) or PFDE is named in sma_additive_withheld (overlap unmeasured branch).
  D  Global Client == sum of the per-firm Client nodes on the post date (the sleeve does not enter Client).
"""
import json
import os
import sys

FIRMS = ("49financial", "inflection", "cottonwood")
ADMITTED = {"sma_additive_aua", "sma_additive_withheld"}
SKIP = {"_provenance", "meta", "source_vintage_last", "as_of_last", "n_dates", "dates"} | ADMITTED
TOL = 0.005


def load(d, scope, view):
    with open(os.path.join(d, "%s__%s.json" % (scope, view)), encoding="utf-8") as f:
        return json.load(f)


def history_diffs(pre, post):
    pos = {d: i for i, d in enumerate(post["dates"])}
    diffs = []

    def cmp(name, a, b):
        for i, d in enumerate(pre["dates"]):
            j = pos.get(d)
            if j is None:
                diffs.append((name, d, "date absent in post"))
            elif a[i] != b[j]:
                diffs.append((name, d, "%r -> %r" % (a[i], b[j])))

    for k, v in pre.items():
        if k in SKIP or not isinstance(v, list) or len(v) != len(pre["dates"]):
            continue
        cmp(k, v, post.get(k) or [None] * len(post["dates"]))
    for m, mv in (pre.get("by_model") or {}).items():
        pm = (post.get("by_model") or {}).get(m) or {}
        for k, v in mv.items():
            if isinstance(v, list) and len(v) == len(pre["dates"]):
                cmp("by_model.%s.%s" % (m, k), v, pm.get(k) or [None] * len(post["dates"]))
    return diffs


def find_member(node, member_id, path=()):
    if isinstance(node, dict):
        if node.get("member_id") == member_id:
            yield path, node
        for k, v in node.items():
            yield from find_member(v, member_id, path + (k,))
    elif isinstance(node, list):
        for x in node:
            yield from find_member(x, member_id, path)


def main(pre_dir, post_dir):
    ok = True
    for f in FIRMS:
        d = history_diffs(load(pre_dir, f, "aggregate-aua-timeseries"), load(post_dir, f, "aggregate-aua-timeseries"))
        print("A %s history: %d moved figure(s)%s" % (f, len(d), " -- STOP" if d else ""))
        for x in d[:10]:
            print("    ", x)
        ok &= not d
        p = load(post_dir, f, "aggregate-aua-timeseries")
        b = all(v is None for v in (p.get("sma_additive_aua") or [0])) and p.get("sma_additive_withheld") == []
        print("B %s admitted keys: %s" % (f, "OK" if b else "FAIL (sma_additive_aua=%r..., withheld=%r)"
              % ((p.get("sma_additive_aua") or [])[-1:], p.get("sma_additive_withheld"))))
        ok &= b

    gts = load(post_dir, "global", "aggregate-aua-timeseries")
    cts = load(post_dir, "cottonwood", "aggregate-aua-timeseries")
    gcv = load(post_dir, "global", "category-views")
    day = gts["dates"][-1]
    cot_pfde = cts["by_model"]["pfde"]["model_value"][cts["dates"].index(day)]
    hits = [(p, n) for p, n in find_member(gcv["nodes"], "pfde") if "SMA" in " ".join(p) or "ETF" in " ".join(p)]
    g_pfde = hits[0][1].get("aum") if hits else None
    add = (gts.get("sma_additive_aua") or [None])[-1]
    withheld = gts.get("sma_additive_withheld")
    print("C day=%s cottonwood PFDE=%r global PFDE node=%r at %s; sma_additive_aua=%r; withheld=%r"
          % (day, cot_pfde, g_pfde, hits[0][0] if hits else None, add, withheld))
    measured = g_pfde is not None and cot_pfde is not None and abs(g_pfde - cot_pfde) < TOL and add is not None \
        and abs(add - cot_pfde) < TOL
    unmeasured = add in (None, 0, 0.0) and "pfde" in json.dumps(withheld or []).lower()
    print("C branch: %s" % ("OVERLAP-MEASURED OK" if measured else "OVERLAP-UNMEASURED OK" if unmeasured else "FAIL"))
    ok &= measured or unmeasured

    i = len(gts["dates"]) - 1
    base, tax = gts["base_excluding_tax_aua"][i], gts["tax_additive_aua"][i] or 0
    total = gts["opal_aggregate_aua"][i]
    delta = total - (base + tax)
    dd = abs(delta - (add or 0)) < TOL
    print("D1 total delta: opal_aggregate_aua=%.2f - (base %.2f + tax %.2f) = %.2f vs sma_additive_aua %r: %s"
          % (total, base, tax, delta, add, "OK" if dd else "FAIL"))
    nodes = gcv["nodes"]
    in_client = [p for p, _ in find_member(nodes.get("Client", {}), "pfde")]
    view_sum = sum(v.get("aum") or 0 for v in nodes.values())
    dc = not in_client and abs(view_sum - gcv["sums"]["total_aua"]) < 0.05
    print("D2 Client: PFDE under Client %d time(s); view-plane node sum %.2f vs total_aua %.2f: %s"
          " (proxy: the sleeve lands under SMA, not Client; a counterfactual Client figure needs the pre-D2 pin)"
          % (len(in_client), view_sum, gcv["sums"]["total_aua"], "OK" if dc else "FAIL"))
    ok &= dd and dc
    print("L4-VERDICT %s" % ("PASS" if ok else "FAIL"))
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1], sys.argv[2]))
