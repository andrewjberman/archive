"""IB-pr-406 compose step: base tree (IB-pr-402's built 49F bytes) versus built tree (+ e56 CUSIP fallback + IB-pr-403 SmartX CUSIP ids).
Reads the gate files and node files that replay_driver_cached.py / ~265's replay_publish_gate.py `run` wrote (labels base_49f, built_49f),
and writes IB107-1_49f_bundle_replay.json. READS ONLY (the built tree's own canonical classifier scan). Counts, booleans and hashes only:
no account id, no security id, no ticker, no name is written.

Usage: python -I compose_406.py <repo_root> <built_tree> <base_tree> <scratch> <out.json> <pin> <analysis_out.json>
Verdict rule: `identical` / `expected-diff` only where the world matched the order's expectation; `FAIL` where it did not (never relabelled).
"""
import json
import os
import re
import sys


def main():
    root, built_tree, base_tree, scratch, out_path, pin, ana_path = sys.argv[1:8]
    sys.path.insert(0, os.path.join(root, "org", "missions", "D9", "IRPT", "IRPT_BCKEND", "deliverables", "0.9.0_WK_IRPT_BCKEND~265", "replay"))
    sys.path.insert(0, os.path.join(built_tree, "data", "assets", "scripts", "gold", "investor_reporting"))
    import holdings_snapshot as hs
    assert os.path.abspath(hs.__file__).startswith(os.path.abspath(built_tree))
    import replay_publish_gate as rp

    def gate(lb):
        with open(os.path.join(scratch, "gate_%s.json" % lb), encoding="utf-8") as fh:
            return json.load(fh)

    gb, gn = gate("base_49f"), gate("built_49f")
    ra, rb = gb["arms"]["real_49financial"], gn["arms"]["real_49financial"]
    with open(os.path.join(scratch, "nodes_base_49f_49financial.json"), encoding="utf-8") as fh:
        base = json.load(fh)
    with open(os.path.join(scratch, "nodes_built_49f_49financial.json"), encoding="utf-8") as fh:
        built = json.load(fh)

    # ---- node-level census (counts only)
    ids_equal = base.keys() == built.keys()
    nd = rp.node_diff(os.path.join(scratch, "nodes_base_49f_49financial.json"), os.path.join(scratch, "nodes_built_49f_49financial.json"))
    cls_fields = ("asset_class", "sub_asset_class", "asset_class_basis")
    smartx = [k for k, n in built.items() if n.get("node_kind") == "SECURITY" and ":asset:" in k]
    cnt = {"nodes": len(built), "security_nodes": sum(1 for n in built.values() if n.get("node_kind") == "SECURITY"),
           "smartx_security_nodes": len(smartx), "smartx_newly_cusip": 0, "smartx_no_cusip_source_unchanged_id": 0,
           "smartx_cusip_ambiguous_listed": 0, "newly_classified": 0, "classification_changed_other": 0,
           "changed_nodes_not_smartx_security": 0, "changed_nodes_smartx_security": 0,
           "smartx_cusip_node_class_unchanged": 0}
    changed_ids = [k for k in base.keys() & built.keys() if base[k] != built[k]]
    for k in changed_ids:
        if k not in set(smartx):
            cnt["changed_nodes_not_smartx_security"] += 1
        else:
            cnt["changed_nodes_smartx_security"] += 1
    sm = set(smartx)
    for k in smartx:
        n, b = built[k], base.get(k) or {}
        ns = str((n.get("security_id") or {}).get("namespace")).upper()
        bs = str((b.get("security_id") or {}).get("namespace")).upper()
        facts = json.dumps(n.get("classification") or {})
        if ns == "CUSIP" and bs != "CUSIP":
            cnt["smartx_newly_cusip"] += 1
            if any(n.get(f) != b.get(f) for f in cls_fields):
                was = b.get("asset_class") in (None, "unclassified")
                now = n.get("asset_class") not in (None, "unclassified")
                if was and now:
                    cnt["newly_classified"] += 1
                else:
                    cnt["classification_changed_other"] += 1
            else:
                cnt["smartx_cusip_node_class_unchanged"] += 1
        elif ns != "CUSIP":
            if "no CUSIP in source" in facts:
                cnt["smartx_no_cusip_source_unchanged_id"] += 1
            if "no unique CUSIP" in facts:
                cnt["smartx_cusip_ambiguous_listed"] += 1

    # ---- symbol miss -> CUSIP key hit, asked of the built tree's own classifier (reads only)
    _ec, clf = hs.canonical_classifier()
    memo = {}

    def look(t):
        if t not in memo:
            memo[t] = clf.canonical_lookup(t) is not None
        return memo[t]

    probe = {"cusip_nodes_newly_on_built": 0, "symbol_hit": 0, "symbol_miss": 0, "symbol_miss_cusip_key_hit": 0, "symbol_miss_cusip_key_miss": 0,
             "of_symbol_miss_cusip_hit_newly_classified": 0}
    for k in smartx:
        n, b = built[k], base.get(k) or {}
        if str((n.get("security_id") or {}).get("namespace")).upper() != "CUSIP" or str((b.get("security_id") or {}).get("namespace")).upper() == "CUSIP":
            continue
        probe["cusip_nodes_newly_on_built"] += 1
        sym = (n.get("display") or {}).get("symbol")
        if look(sym):
            probe["symbol_hit"] += 1
            continue
        probe["symbol_miss"] += 1
        key = hs.cusip_key(n.get("security_id"))
        if key is not None and look(key):
            probe["symbol_miss_cusip_key_hit"] += 1
            if b.get("asset_class") in (None, "unclassified") and n.get("asset_class") not in (None, "unclassified"):
                probe["of_symbol_miss_cusip_hit_newly_classified"] += 1
        else:
            probe["symbol_miss_cusip_key_miss"] += 1

    # ---- why the gate refuses: the gate's own rule applied to (built candidate, base nodes as the served stand-in)
    def unclassified_keys(nodes):
        return {hs._gate_security_key(n) for n in nodes.values() if n.get("node_kind") == "SECURITY" and n.get("asset_class") == "unclassified"} - {None}

    def placed_keys(nodes):
        return {hs._gate_security_key(n) for n in nodes.values() if n.get("node_kind") == "SECURITY" and n.get("asset_class") not in (None, "unclassified")} - {None}

    def unplaced_keys(nodes):
        return {hs._gate_security_key(n) for n in nodes.values() if n.get("node_kind") == "SECURITY" and n.get("asset_class") in (None, "unclassified")} - {None}

    now_un = unclassified_keys(built)
    lost = now_un & (placed_keys(base) - unplaced_keys(base))
    lost_in_smartx = {hs._gate_security_key(built[k]) for k in smartx} & lost
    lost_also_nonsmartx_classified_on_built = {hs._gate_security_key(n) for k, n in built.items() if n.get("node_kind") == "SECURITY" and k not in sm
                                               and n.get("asset_class") not in (None, "unclassified")} & lost
    why = {"lost_keys_rule_applied_to_base_nodes": len(lost), "gate_reported_conditions": rb.get("conditions"),
           "lost_keys_carried_by_a_smartx_model_asset_node": len(lost_in_smartx),
           "lost_keys_also_classified_on_a_non_smartx_node_of_the_built_candidate": len(lost_also_nonsmartx_classified_on_built),
           "built_unclassified_keys": len(now_un), "base_unclassified_keys": len(unclassified_keys(base)),
           "base_placed_keys": len(placed_keys(base)),
           "lost_keys_cusip_namespace": sum(1 for k in lost if k.startswith("CUSIP:"))}
    with open(ana_path, "w", encoding="utf-8") as fh:
        json.dump({"node_diff": nd, "node_ids_equal": ids_equal, "counts": cnt, "probe": probe, "gate_why": why}, fh, indent=1, sort_keys=True)

    arms = []
    # ---- fwd14_gate_unchanged
    same_gate = (ra["outcome"] == rb["outcome"] and ra["conditions"] == rb["conditions"] and ra["listed"] == rb["listed"]
                 and ra["uploaded"] == rb["uploaded"])
    fx_names = sorted(n for n in gb["arms"] if n.startswith("fx_"))
    fx_same = {}
    for nm in fx_names:
        fa, fb = gb["arms"][nm], gn["arms"].get(nm)
        fx_same[nm] = fa == fb
    arms.append({"name": "fwd14_gate_unchanged", "verdict": "identical" if same_gate else "FAIL", "negative_control": False,
                 "detail": "REAL inputs + real served index (business_date %s/%s), writes captured in memory. BASE (IB-pr-402 bytes): gate=%s conditions=%s listed=%s "
                           "uploaded=%s. BUILT: gate=%s conditions=%s listed=%s uploaded=%s. The gate CODE is unchanged (evaluate_publish_gate is byte-identical in both "
                           "members: %s); its OUTCOME on the real candidate is %s. %s"
                           % (ra["business_date"], rb["business_date"], ra["outcome"], ra["conditions"], ra["listed"], ra["uploaded"], rb["outcome"],
                              rb["conditions"], rb["listed"], rb["uploaded"],
                              "yes" if _gate_src_equal(base_tree, built_tree) else "NO",
                              "the same" if same_gate else "DIFFERENT -- the order expected the same",
                              "" if same_gate else "Mechanism (measured, counts only): %s" % json.dumps(why, sort_keys=True))})
    arms.append({"name": "fwd14_gate_fixture_arms_unchanged", "verdict": "identical" if all(fx_same.values()) else "FAIL", "negative_control": False,
                 "detail": "The six fixture arms (worse_restored, all_unknown_loses_account, closed_account_not_refused, monday_not_stale, mutant_gate_stubbed) run "
                           "on each tree's real HoldingsPublication in an in-memory bucket: identical per arm = %s" % json.dumps(fx_same, sort_keys=True)})
    for nm in fx_names:
        if "mutant" in nm:
            res = gn["arms"][nm]
            arms.append({"name": "negative_control_mutant_gate_stubbed", "verdict": "expected-diff" if res["result"]["uploaded"] and res["index_moved"] else "FAIL",
                         "negative_control": True,
                         "detail": "NEGATIVE CONTROL (the gate arms discriminate): built tree with evaluate_publish_gate stubbed to PUBLISHED publishes the worse "
                                   "fixture candidate (uploaded=%s index_moved=%s); the real gate does not" % (res["result"]["uploaded"], res["index_moved"])})
    # ---- symbol_miss_cusip_fallback
    base_text = open(os.path.join(base_tree, "data", "assets", "scripts", "gold", "investor_reporting", "holdings_snapshot.py"), encoding="utf-8").read()
    base_has_param = bool(re.search(r"def classify_security\([^)]*security_id", base_text))
    ok_sm = probe["symbol_miss_cusip_key_hit"] >= 1 and not base_has_param
    arms.append({"name": "symbol_miss_cusip_fallback", "verdict": "expected-diff" if ok_sm else "FAIL", "negative_control": False,
                 "detail": "BUILT classify_security takes security_id and asks the table for CUSIP:<id> after a symbol miss; BASE classify_security has no security_id "
                           "parameter (%s). Over the %d SmartX nodes that newly carry a CUSIP on built: symbol hit %d, symbol miss %d; of the misses, CUSIP key HIT %d, "
                           "CUSIP key miss %d. Nodes NEWLY CLASSIFIED (unclassified/None on base, a class on built): %d of %d. Classification changed another way: %d. "
                           "CUSIP node whose class did not move: %d. (A node with no symbol reaches the CUSIP key directly: canonical_lookup('') is None.)"
                           % ("signature read from the base member" if not base_has_param else "UNEXPECTED: base already has it", probe["cusip_nodes_newly_on_built"],
                              probe["symbol_hit"], probe["symbol_miss"], probe["symbol_miss_cusip_key_hit"], probe["symbol_miss_cusip_key_miss"],
                              cnt["newly_classified"], cnt["smartx_newly_cusip"], cnt["classification_changed_other"], cnt["smartx_cusip_node_class_unchanged"])})
    # ---- real_49financial_nodes
    only_ok = (nd["only_in_a"] == 0 and nd["only_in_b"] == 0 and set(nd["differing_fields_on_changed_nodes"]) <= {"security_id", "classification", "asset_class",
               "sub_asset_class", "asset_class_basis", "display", "valuation_facts"})
    arms.append({"name": "real_49financial_nodes", "verdict": "expected-diff" if only_ok and ids_equal else "FAIL", "negative_control": False,
                 "detail": "Same node ids on both trees = %s (%d / %d nodes). Changed %d, unchanged %d, only in base %d, only in built %d. Differing fields on changed nodes: %s. "
                           "SmartX SECURITY nodes %d: %d newly carry a CUSIP security_id, %d keep the source id with 'no CUSIP in source' listed, %d ambiguous. Changed nodes "
                           "that are not SmartX SECURITY nodes: %d. Candidate nodes sha256 base %s built %s."
                           % (ids_equal, len(base), len(built), nd["changed"], nd["same"], nd["only_in_a"], nd["only_in_b"],
                              json.dumps(nd["differing_fields_on_changed_nodes"], sort_keys=True), cnt["smartx_security_nodes"], cnt["smartx_newly_cusip"],
                              cnt["smartx_no_cusip_source_unchanged_id"], cnt["smartx_cusip_ambiguous_listed"], cnt["changed_nodes_not_smartx_security"],
                              ra["nodes_sha256"][:12], "see analysis (candidate not landed: REFUSED)" if rb.get("outcome") == "REFUSED" else rb.get("nodes_sha256", "")[:12])})
    # ---- negative control: nodes outside the two groups the order moves keep their base bytes
    def is_cusip(n):
        return str((n.get("security_id") or {}).get("namespace")).upper() == "CUSIP"
    custody_cusip = [k for k, n in built.items() if k not in sm and n.get("node_kind") == "SECURITY" and is_cusip(n)]
    cc = set(custody_cusip)
    untouched = [k for k in built if k not in sm and k not in cc]
    untouched_same = sum(1 for k in untouched if base.get(k) == built[k])
    nocusip_smartx = [k for k in smartx if not is_cusip(built[k])]
    nocusip_class_same = sum(1 for k in nocusip_smartx if all(base[k].get(f) == built[k].get(f) for f in cls_fields))
    arms.append({"name": "negative_control_untouched_nodes_and_no_cusip_nodes", "verdict": "expected-diff" if untouched and untouched_same == len(untouched)
                 and nocusip_class_same == len(nocusip_smartx) else "FAIL", "negative_control": True,
                 "detail": "NEGATIVE CONTROL: nodes the two changes do not reach stay as on base. Nodes that are neither a SmartX model asset nor a custody SECURITY node "
                           "with a CUSIP security_id: %d of %d byte-equal to base. SmartX model-asset nodes with NO CUSIP on built (source id kept, 'no CUSIP in source' "
                           "listed): %d, of which keep identical asset_class/sub_asset_class/asset_class_basis: %d (their classification facts gain the listing line; "
                           "that is the only difference)." % (untouched_same, len(untouched), len(nocusip_smartx), nocusip_class_same)})
    # ---- e56 on custody nodes whose security_id is a CUSIP (what the order wanted from the fallback)
    cc_new = sum(1 for k in custody_cusip if base[k].get("asset_class") in (None, "unclassified") and built[k].get("asset_class") not in (None, "unclassified"))
    cc_chg = sum(1 for k in custody_cusip if base[k] != built[k])
    cc_lost = sum(1 for k in custody_cusip if base[k].get("asset_class") not in (None, "unclassified") and built[k].get("asset_class") in (None, "unclassified"))
    arms.append({"name": "custody_cusip_nodes_e56_fallback", "verdict": "expected-diff" if cc_new >= 1 and cc_lost == 0 else "FAIL", "negative_control": False,
                 "detail": "e56 on the non-SmartX SECURITY nodes whose security_id is a CUSIP: %d such nodes, %d changed, %d NEWLY CLASSIFIED (unclassified on base, a class on "
                           "built), %d classified->unclassified. (Same node ids on both trees; only classification fields differ on these.)"
                           % (len(custody_cusip), cc_chg, cc_new, cc_lost)})
    # ---- IB-pr-403's effect on the SmartX model-asset nodes' classification (the order expects none)
    trans = {}
    for k in smartx:
        if is_cusip(built[k]) and not is_cusip(base[k]):
            a = "classified" if base[k].get("asset_class") not in (None, "unclassified") else "unclassified"
            b2 = "classified" if built[k].get("asset_class") not in (None, "unclassified") else "unclassified"
            trans[a + "->" + b2] = trans.get(a + "->" + b2, 0) + 1
    sym_gone = sum(1 for k in smartx if is_cusip(built[k]) and not is_cusip(base[k]) and not (built[k].get("display") or {}).get("symbol")
                   and (base[k].get("display") or {}).get("symbol"))
    arms.append({"name": "smartx_model_asset_classification_moves", "verdict": "FAIL" if trans.get("classified->unclassified") else "expected-diff", "negative_control": False,
                 "detail": "The %d SmartX model-asset nodes that newly carry a CUSIP: class state base->built %s. display.symbol present on base and ABSENT on built: %d "
                           "(fill_display takes `symbol` from a TICKER-namespaced security_id or a ticker= fact; a CUSIP security_id gives it neither, so classify_security "
                           "then asks the table with no ticker, the CUSIP key misses, and the bd-securities fallback answers by name). The order expects no loss here."
                           % (cnt["smartx_newly_cusip"], json.dumps(trans, sort_keys=True), sym_gone)})
    doc = {"to_id": "IRPT_BCKEND.TO-IB-pr-406", "pin": pin,
           "method": "base tree = IB-pr-402's built 49F bytes (sha256 3f2e738f...), built tree = base + e56 diff + IB-pr-403 diff, each extracted into its own directory outside "
                     "the worktree and driven by ~265's replay_publish_gate.py `run` (python -I) through replay_driver_cached.py (memoised canonical_lookup; dumps the candidate "
                     "nodes before the gate sees them). Real arms: the tree's own run_firm on the real 49F sources and the real served index through a read-through client whose "
                     "writes are captured in memory. Nothing is put anywhere.",
           "gate_files": {"base_seconds": ra["seconds"], "built_seconds": rb["seconds"]}, "arms": arms}
    with open(out_path, "w", encoding="utf-8") as fh:
        json.dump(doc, fh, indent=1, sort_keys=True)
    print("wrote", out_path, len(arms), "arms:", {a["name"]: a["verdict"] for a in arms})


def _gate_src_equal(base_tree, built_tree):
    p = os.path.join("data", "assets", "scripts", "gold", "investor_reporting", "holdings_snapshot.py")
    def body(t):
        s = open(os.path.join(t, p), encoding="utf-8").read()
        i = s.index("def evaluate_publish_gate")
        return s[i:s.index("def write_refusal_record", i)]
    return body(base_tree) == body(built_tree)


if __name__ == "__main__":
    main()
