"""IB-pr-417 compose step: the replay (IB117-2_49f_bundle_replay.json) and the memory record (IB117-2_49f_bundle_memory.json) of the 49F bundle
rebuilt as IB-pr-410's members + IB-pr-414's publish-gate memory fix. READS the per-run files ~265's replay_publish_gate.py `run` (through ~269's
replay_driver_cached.py) and ~276's mem_harness.py wrote in scratch directories outside the repo. Counts, booleans and hashes only: no account id,
security id, ticker or name.

Usage: python -I compose_417.py <repo_root> <fix_tree> <rp_dir> <mem_dir> <out_replay.json> <out_memory.json> <pin> <built_sha256>
  rp_dir   gate_<label>.json + nodes_<label>_49financial.json for labels base_49f (the live 404 bytes), b410_49f (IB-pr-410's members), fix_49f (this bundle)
  mem_dir  mem_<label>_49financial.json for labels fix, b404, b410 (the sequential memory runs, no memoisation); gate_<label>_49financial.json for fix, b410
Verdict rule: `identical` / `expected-diff` only where the world matched the order's expectation; `FAIL` where it did not (never relabelled).
"""
import json
import os
import sys

LIMIT = int(0.85 * 4 * 1024 ** 3)


def load(*p):
    with open(os.path.join(*p), encoding="utf-8") as fh:
        return json.load(fh)


def main():
    root, fix_tree, rp, mem, out_replay, out_mem, pin, built = sys.argv[1:9]
    sys.path.insert(0, os.path.join(fix_tree, "data", "assets", "scripts", "gold", "investor_reporting"))
    import holdings_snapshot as hs
    assert os.path.abspath(hs.__file__).startswith(os.path.abspath(fix_tree))
    gb, g410, gfx = (load(rp, "gate_%s_49f.json" % x) for x in ("base", "b410", "fix"))
    ra, r4, rf = gb["arms"]["real_49financial"], g410["arms"]["real_49financial"], gfx["arms"]["real_49financial"]
    for nm, r in (("base", ra), ("b410", r4), ("fix", rf)):
        if "error" in r:
            raise SystemExit("run %s errored: %s" % (nm, r["error"]))
    nb, n4, nf = (load(rp, "nodes_%s_49f_49financial.json" % x) for x in ("base", "b410", "fix"))
    mf, m404, m410 = (load(mem, "mem_%s_49financial.json" % x) for x in ("fix", "b404", "b410"))
    for nm, m in (("fix", mf), ("b404", m404), ("b410", m410)):
        if "error" in m:
            raise SystemExit("memory run %s errored: %s" % (nm, m["error"]))

    def sig(r):
        return (r["outcome"], r["conditions"], r["listed"], r["uploaded"], r["refused"])

    def classified(n):
        return n.get("asset_class") not in (None, "unclassified")

    arms = []
    # ---- fwd14_gate_vs_b410
    same_sig = sig(rf) == sig(r4)
    fx_names = sorted(n for n in gfx["arms"] if n.startswith("fx_"))
    fx_same = {nm: gfx["arms"][nm] == g410["arms"].get(nm) for nm in fx_names}
    d_fix = load(mem, "gate_fix_49financial.json")
    d_410 = load(mem, "gate_b410_49financial.json")
    full_same = d_fix["decision"] == d_410["decision"]
    ok = same_sig and all(fx_same.values()) and full_same and rf["nodes_sha256"] == r4["nodes_sha256"]
    arms.append({"name": "fwd14_gate_vs_b410", "verdict": "identical" if ok else "FAIL", "negative_control": False,
                 "detail": "REAL 49financial inputs and the real served index, upload through a read-through client whose writes are discarded (nothing leaves the process). "
                           "Replay run (business_date %s/%s): b410 tree (IB-pr-410 members) gate=%s conditions=%s listed=%s uploaded=%s; this bundle gate=%s conditions=%s listed=%s "
                           "uploaded=%s; equal=%s. Whole decision from the memory runs (outcome, every condition with its count, every listed set; served node count %s vs %s): "
                           "byte-equal=%s. Fixture arms (%d, on each tree's real HoldingsPublication in an in-memory bucket) equal arm for arm: %s. Candidate nodes sha256 equal: %s."
                           % (r4["business_date"], rf["business_date"], r4["outcome"], r4["conditions"], r4["listed"], r4["uploaded"], rf["outcome"], rf["conditions"],
                              rf["listed"], rf["uploaded"], same_sig, d_410.get("served_nodes"), d_fix.get("served_nodes"), full_same, len(fx_names),
                              json.dumps(fx_same, sort_keys=True), rf["nodes_sha256"] == r4["nodes_sha256"])})
    # ---- smartx_class_parity (base = the live 404 bytes -> this bundle; also this bundle vs b410)
    ids_equal = nb.keys() == nf.keys() == n4.keys()
    smartx = [k for k, n in nf.items() if n.get("node_kind") == "SECURITY" and ":asset:" in k]
    cls_fields = ("asset_class", "sub_asset_class", "asset_class_basis")
    t = {}
    for k in smartx:
        key = ("classified" if classified(nb[k]) else "unclassified") + "->" + ("classified" if classified(nf[k]) else "unclassified")
        t[key] = t.get(key, 0) + 1
    lost = t.get("classified->unclassified", 0)
    moved_vs_410 = sum(1 for k in smartx if any(n4[k].get(f) != nf[k].get(f) for f in cls_fields))
    sym_eq = sum(1 for k in smartx if (nb[k].get("display") or {}).get("symbol") == (nf[k].get("display") or {}).get("symbol"))
    arms.append({"name": "smartx_class_parity", "verdict": "identical" if ids_equal and lost == 0 and moved_vs_410 == 0 else "FAIL", "negative_control": False,
                 "detail": "SmartX model-asset SECURITY nodes (%d; same node ids on the live-404, b410 and this tree = %s, %d nodes): class state live-404 -> this bundle %s; "
                           "classified -> unclassified: %d. Nodes with any of asset_class/sub_asset_class/asset_class_basis different between this bundle and the b410 tree: %d. "
                           "display.symbol equal live-404 vs this bundle: %d of %d."
                           % (len(smartx), ids_equal, len(nf), json.dumps(t, sort_keys=True), lost, moved_vs_410, sym_eq, len(smartx))})
    # ---- every candidate node equals the b410 tree's (the memory fix is gate code only)
    diff_nodes = sum(1 for k in nf if n4.get(k) != nf[k])
    arms.append({"name": "real_49financial_nodes_vs_b410", "verdict": "identical" if diff_nodes == 0 and ids_equal else "FAIL", "negative_control": False,
                 "detail": "Candidate nodes of this bundle vs the b410 tree: %d nodes, %d differ (the memory fix changes the publish-gate code, not the node build). "
                           "Versus the live 404 bytes: changed %d, byte-equal %d (the served change IB-pr-410 already counted)."
                           % (len(nf), diff_nodes, sum(1 for k in nf if nb.get(k) != nf[k]), sum(1 for k in nf if nb.get(k) == nf[k]))})
    # ---- negative controls
    pk = lambda m: m["peak_wset_bytes"] or m["sampled_peak_rss_bytes"]  # noqa: E731
    neg_ok = pk(m404) > pk(mf) and pk(m410) > pk(mf) and pk(mf) < LIMIT <= max(pk(m404), pk(m410))
    arms.append({"name": "negative_control_served_node_list_form_peaks_above_fix", "verdict": "expected-diff" if neg_ok else "FAIL", "negative_control": True,
                 "detail": "NEGATIVE CONTROL, one harness (mem_harness.py, run_firm on the real 49F inputs, writes captured in memory, run sequentially and alone, no memoisation): "
                           "the live 404 bundle (served publication held as a node-dict list) peaks at %d B and the b410 tree (same gate form) at %d B; this bundle (keyed sets) at %d B. "
                           "The limit is %d B (0.85 x 4 GiB); the served-node list form peaks above this bundle in both trees and above the limit in %d of 2."
                           % (pk(m404), pk(m410), pk(mf), LIMIT, sum(1 for m in (m404, m410) if pk(m) >= LIMIT))})
    for nm in fx_names:
        if "mutant" in nm:
            res = gfx["arms"][nm]
            arms.append({"name": "negative_control_mutant_gate_stubbed", "verdict": "expected-diff" if res["result"]["uploaded"] and res["index_moved"] else "FAIL",
                         "negative_control": True,
                         "detail": "NEGATIVE CONTROL (the gate arms discriminate): this bundle with evaluate_publish_gate stubbed to PUBLISHED publishes the worse fixture candidate "
                                   "(uploaded=%s index_moved=%s); the real gate does not." % (res["result"]["uploaded"], res["index_moved"])})
    doc = {"to_id": "IRPT_BCKEND.TO-IB-pr-417", "pin": pin, "built_sha256": built,
           "method": "live 404 tree = the live 49F bundle (version irUPjpfrDLoM2zhnhunbBtIG9fP275kI, sha256 3f2e738f...); b410 tree = live + the e56 holdings_snapshot.py diff + IB-pr-403 and IB-pr-410 "
                     "holdings_49f.py diffs (member sha256 a9fe965f / 401a36ff, IB-pr-410's); this bundle = b410 + the holdings_snapshot.py diff of 3f2bdda578. Each extracted into its own "
                     "directory outside the worktree; replay arms by ~265's replay_publish_gate.py `run` through ~269's replay_driver_cached.py; memory and whole-decision arms by ~276's "
                     "mem_harness.py. Real inputs, real served index, writes captured in memory. Nothing is put anywhere.", "arms": arms}
    with open(out_replay, "w", encoding="utf-8") as fh:
        json.dump(doc, fh, indent=1, sort_keys=True)
    mem_doc = {"peak_rss_bytes": int(pk(mf)), "wall_time_s": mf["seconds"], "cpu_time_s": mf["cpu_time_s"], "table_lookups": mf["table_lookups"],
               "harness": "mem_harness.py (~276; python %s) drives the BUILT bundle's own holdings_snapshot.run_firm('49financial', as_of %s) on the real sources and the real served index "
                          "through a read-through client: every put captured in memory and discarded, every other mutation raises (upload disabled: no byte leaves the process). "
                          "peak_rss_bytes = the OS peak working set (psutil peak_wset), sampler cross-check %d B. Run sequentially and alone, no memoisation. built sha256 %s."
                          % (mf["python"], mf["as_of"], mf["sampled_peak_rss_bytes"], built),
               "inputs_date": mf["business_date"], "limit_bytes": LIMIT,
               "controls": {"live_404_bundle": {"peak_rss_bytes": int(pk(m404)), "wall_time_s": m404["seconds"], "table_lookups": m404["table_lookups"]},
                            "b410_members": {"peak_rss_bytes": int(pk(m410)), "wall_time_s": m410["seconds"], "table_lookups": m410["table_lookups"]}},
               "gate_outcome": mf.get("outcome"), "node_count": mf.get("node_count")}
    with open(out_mem, "w", encoding="utf-8") as fh:
        json.dump(mem_doc, fh, indent=1, sort_keys=True)
    print("wrote", out_replay, len(arms), "arms:", {a["name"]: a["verdict"] for a in arms})
    print("wrote", out_mem, {k: mem_doc[k] for k in ("peak_rss_bytes", "wall_time_s", "cpu_time_s", "table_lookups", "inputs_date")})


if __name__ == "__main__":
    main()
