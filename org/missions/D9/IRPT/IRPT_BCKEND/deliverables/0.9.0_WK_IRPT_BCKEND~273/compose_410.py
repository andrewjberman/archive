"""IB-pr-410 compose step: base tree (IB-pr-402's built 49F bytes) versus the FIXED built tree (e56 + IB-pr-403 + the ticker= fact), with the
~269 build (e56 + unfixed IB-pr-403) as the negative control. Adapted from ~269's compose_406.py. Reads the gate files and node files that
~269's replay_driver_cached.py (~265's replay_publish_gate.py `run`) wrote for labels base_49f, built_49f, prior_49f, and writes
IB111-1_49f_bundle_replay.json plus an analysis file. READS ONLY. Counts, booleans and hashes only: no account id, security id, ticker or name.

Usage: python -I compose_410.py <repo_root> <built_tree> <base_tree> <prior_tree> <scratch_base> <scratch_built> <scratch_prior> <out.json> <pin> <analysis_out.json>
Verdict rule: `identical` / `expected-diff` only where the world matched the order's expectation; `FAIL` where it did not (never relabelled).
"""
import json
import os
import re
import sys


def main():
    root, built_tree, base_tree, prior_tree, sb, sn, sp, out_path, pin, ana_path = sys.argv[1:11]
    sys.path.insert(0, os.path.join(root, "org", "missions", "D9", "IRPT", "IRPT_BCKEND", "deliverables", "0.9.0_WK_IRPT_BCKEND~265", "replay"))
    sys.path.insert(0, os.path.join(built_tree, "data", "assets", "scripts", "gold", "investor_reporting"))
    import holdings_snapshot as hs
    assert os.path.abspath(hs.__file__).startswith(os.path.abspath(built_tree))
    import replay_publish_gate as rp

    def gate(scratch, lb):
        with open(os.path.join(scratch, "gate_%s.json" % lb), encoding="utf-8") as fh:
            return json.load(fh)

    def nodes(scratch, lb):
        with open(os.path.join(scratch, "nodes_%s_49financial.json" % lb), encoding="utf-8") as fh:
            return json.load(fh)

    gb, gn, gp = gate(sb, "base_49f"), gate(sn, "built_49f"), gate(sp, "prior_49f")
    ra, rb, rpri = gb["arms"]["real_49financial"], gn["arms"]["real_49financial"], gp["arms"]["real_49financial"]
    base, built, prior = nodes(sb, "base_49f"), nodes(sn, "built_49f"), nodes(sp, "prior_49f")
    pa = lambda s, lb: os.path.join(s, "nodes_%s_49financial.json" % lb)  # noqa: E731

    def classified(n):
        return n.get("asset_class") not in (None, "unclassified")

    def is_cusip(n):
        return str((n.get("security_id") or {}).get("namespace")).upper() == "CUSIP"

    def is_smartx(k, n):
        return n.get("node_kind") == "SECURITY" and ":asset:" in k

    ids_equal = base.keys() == built.keys()
    nd = rp.node_diff(pa(sb, "base_49f"), pa(sn, "built_49f"))
    cls_fields = ("asset_class", "sub_asset_class", "asset_class_basis")
    smartx = [k for k, n in built.items() if is_smartx(k, n)]
    sm = set(smartx)

    # ---- SmartX class parity, base -> built (the FIXED build) and base -> prior (the ~269 build, for the contrast)
    def transitions(cand):
        t, val, basis = {}, {}, {}
        for k in smartx:
            b, n = base[k], cand[k]
            key = ("classified" if classified(b) else "unclassified") + "->" + ("classified" if classified(n) else "unclassified")
            t[key] = t.get(key, 0) + 1
            if b.get("asset_class") != n.get("asset_class"):
                vk = "%s -> %s" % (b.get("asset_class"), n.get("asset_class"))
                val[vk] = val.get(vk, 0) + 1
            if b.get("asset_class_basis") != n.get("asset_class_basis"):
                bk = "%s -> %s" % (b.get("asset_class_basis"), n.get("asset_class_basis"))
                basis[bk] = basis.get(bk, 0) + 1
        return t, val, basis

    t_built, val_built, basis_built = transitions(built)
    t_prior, val_prior, _bp = transitions(prior)
    newly_cusip = [k for k in smartx if is_cusip(built[k]) and not is_cusip(base[k])]
    sym_gone = sum(1 for k in smartx if (base[k].get("display") or {}).get("symbol") and not (built[k].get("display") or {}).get("symbol"))
    sym_same = sum(1 for k in smartx if (base[k].get("display") or {}).get("symbol") == (built[k].get("display") or {}).get("symbol"))
    cls_changed_smartx = sum(1 for k in smartx if any(base[k].get(f) != built[k].get(f) for f in cls_fields))
    cnt = {"nodes": len(built), "smartx_security_nodes": len(smartx), "smartx_newly_cusip": len(newly_cusip),
           "smartx_class_state_base_to_built": t_built, "smartx_class_value_moves_base_to_built": val_built,
           "smartx_basis_moves_base_to_built": basis_built, "smartx_class_state_base_to_prior_269": t_prior,
           "smartx_class_value_moves_base_to_prior_269_total": sum(val_prior.values()),
           "smartx_display_symbol_present_on_base_absent_on_built": sym_gone, "smartx_display_symbol_equal_base_built": sym_same,
           "smartx_nodes_with_any_class_field_moved": cls_changed_smartx,
           "changed_nodes_smartx_security": sum(1 for k in sm if base[k] != built[k]),
           "changed_nodes_not_smartx_security": sum(1 for k in built if k not in sm and base[k] != built[k])}

    # ---- symbol miss -> CUSIP key hit, asked of the built tree's own classifier (reads only)
    _ec, clf = hs.canonical_classifier()
    memo = {}

    def look(t):
        if t not in memo:
            memo[t] = clf.canonical_lookup(t) is not None
        return memo[t]

    probe = {"cusip_nodes_newly_on_built": 0, "symbol_hit": 0, "symbol_miss": 0, "symbol_miss_cusip_key_hit": 0,
             "symbol_miss_cusip_key_miss": 0, "of_symbol_miss_cusip_hit_newly_classified": 0, "newly_classified_any": 0}
    for k in newly_cusip:
        n, b = built[k], base[k]
        probe["cusip_nodes_newly_on_built"] += 1
        if not classified(b) and classified(n):
            probe["newly_classified_any"] += 1
        sym = (n.get("display") or {}).get("symbol")
        if sym and look(sym):
            probe["symbol_hit"] += 1
            continue
        probe["symbol_miss"] += 1
        key = hs.cusip_key(n.get("security_id"))
        if key is not None and look(key):
            probe["symbol_miss_cusip_key_hit"] += 1
            if not classified(b) and classified(n):
                probe["of_symbol_miss_cusip_hit_newly_classified"] += 1
        else:
            probe["symbol_miss_cusip_key_miss"] += 1

    # ---- the gate's rule applied to (candidate, base nodes as the served stand-in), for built and for prior
    def keys(nodes_, pred):
        return {hs._gate_security_key(n) for n in nodes_.values() if n.get("node_kind") == "SECURITY" and pred(n)} - {None}

    def lost(cand):
        un = keys(cand, lambda n: n.get("asset_class") == "unclassified")
        return un & (keys(base, classified) - keys(base, lambda n: not classified(n)))

    lost_built, lost_prior = lost(built), lost(prior)
    why = {"lost_keys_built_rule_applied_to_base_nodes": len(lost_built), "lost_keys_prior_269_rule_applied_to_base_nodes": len(lost_prior),
           "built_gate_conditions": rb.get("conditions"), "prior_269_gate_conditions": rpri.get("conditions")}
    with open(ana_path, "w", encoding="utf-8") as fh:
        json.dump({"node_diff_base_vs_built": nd, "node_ids_equal": ids_equal, "counts": cnt, "probe": probe, "gate_why": why}, fh, indent=1, sort_keys=True)

    arms = []

    def gate_sig(r):
        return (r["outcome"], r["conditions"], r["listed"], r["uploaded"])

    same_gate = gate_sig(ra) == gate_sig(rb)
    arms.append({"name": "fwd14_gate_unchanged", "verdict": "identical" if same_gate else "FAIL", "negative_control": False,
                 "detail": "REAL inputs + real served index (business_date %s/%s), writes captured in memory. BASE (IB-pr-402 bytes): gate=%s conditions=%s listed=%s uploaded=%s. "
                           "BUILT (fixed): gate=%s conditions=%s listed=%s uploaded=%s. Gate code byte-identical in both members: %s. Outcome and conditions are %s."
                           % (ra["business_date"], rb["business_date"], ra["outcome"], ra["conditions"], ra["listed"], ra["uploaded"], rb["outcome"], rb["conditions"],
                              rb["listed"], rb["uploaded"], "yes" if _gate_src_equal(base_tree, built_tree) else "NO", "the same" if same_gate else "DIFFERENT")})
    fx_names = sorted(n for n in gb["arms"] if n.startswith("fx_"))
    fx_same = {nm: gb["arms"][nm] == gn["arms"].get(nm) for nm in fx_names}
    arms.append({"name": "fwd14_gate_fixture_arms_unchanged", "verdict": "identical" if all(fx_same.values()) else "FAIL", "negative_control": False,
                 "detail": "The fixture arms on each tree's real HoldingsPublication in an in-memory bucket: identical per arm = %s" % json.dumps(fx_same, sort_keys=True)})
    for nm in fx_names:
        if "mutant" in nm:
            res = gn["arms"][nm]
            arms.append({"name": "negative_control_mutant_gate_stubbed", "verdict": "expected-diff" if res["result"]["uploaded"] and res["index_moved"] else "FAIL",
                         "negative_control": True,
                         "detail": "NEGATIVE CONTROL (the gate arms discriminate): built tree with evaluate_publish_gate stubbed to PUBLISHED publishes the worse fixture candidate "
                                   "(uploaded=%s index_moved=%s); the real gate does not" % (res["result"]["uploaded"], res["index_moved"])})
    # ---- smartx_class_parity
    lost_cls = t_built.get("classified->unclassified", 0)
    arms.append({"name": "smartx_class_parity", "verdict": "identical" if lost_cls == 0 else "FAIL", "negative_control": False,
                 "detail": "SmartX model-asset SECURITY nodes (%d, same ids both trees): class state base->built %s. Nodes classified on base and unclassified on built: %d "
                           "(the ~269 build: %s, i.e. %d). display.symbol present on base and absent on built: %d; display.symbol equal on both: %d of %d. SmartX nodes with any of "
                           "asset_class/sub_asset_class/asset_class_basis moved: %d; class VALUE moves %s; basis moves %s."
                           % (len(smartx), json.dumps(t_built, sort_keys=True), lost_cls, json.dumps(t_prior, sort_keys=True), t_prior.get("classified->unclassified", 0), sym_gone,
                              sym_same, len(smartx), cls_changed_smartx, json.dumps(val_built, sort_keys=True), json.dumps(basis_built, sort_keys=True))})
    # ---- symbol_miss_cusip_fallback
    base_text = open(os.path.join(base_tree, "data", "assets", "scripts", "gold", "investor_reporting", "holdings_snapshot.py"), encoding="utf-8").read()
    built_text = open(os.path.join(built_tree, "data", "assets", "scripts", "gold", "investor_reporting", "holdings_snapshot.py"), encoding="utf-8").read()
    base_has_param = bool(re.search(r"def classify_security\([^)]*security_id", base_text))
    built_has_param = bool(re.search(r"def classify_security\([^)]*security_id", built_text))
    ok_sm = (not base_has_param) and built_has_param and probe["cusip_nodes_newly_on_built"] >= 1
    arms.append({"name": "symbol_miss_cusip_fallback", "verdict": "expected-diff" if ok_sm else "FAIL", "negative_control": False,
                 "detail": "BUILT classify_security takes security_id and asks the table for CUSIP:<id> after a symbol miss (signature on built: %s); BASE has no security_id parameter "
                           "(%s). Over the %d SmartX nodes that newly carry a CUSIP on built: symbol hit %d, symbol miss %d; of the misses, CUSIP key HIT %d, CUSIP key miss %d. "
                           "Nodes newly classified (unclassified/None on base, a class on built): %d (via the CUSIP key after a symbol miss: %d)."
                           % (built_has_param, "signature read from the base member" if not base_has_param else "UNEXPECTED: base already has it", probe["cusip_nodes_newly_on_built"],
                              probe["symbol_hit"], probe["symbol_miss"], probe["symbol_miss_cusip_key_hit"], probe["symbol_miss_cusip_key_miss"],
                              probe["newly_classified_any"], probe["of_symbol_miss_cusip_hit_newly_classified"])})
    # ---- real_49financial_nodes
    only_ok = (nd["only_in_a"] == 0 and nd["only_in_b"] == 0 and set(nd["differing_fields_on_changed_nodes"]) <= {"security_id", "classification", "asset_class",
               "sub_asset_class", "asset_class_basis", "display", "valuation_facts"})
    arms.append({"name": "real_49financial_nodes", "verdict": "expected-diff" if only_ok and ids_equal else "FAIL", "negative_control": False,
                 "detail": "Same node ids on both trees = %s (%d / %d nodes). Changed %d, unchanged %d, only in base %d, only in built %d. Differing fields on changed nodes: %s. "
                           "SmartX SECURITY nodes %d, of which %d newly carry a CUSIP security_id. Changed nodes that are not SmartX SECURITY nodes: %d. Candidate nodes sha256 base %s built %s."
                           % (ids_equal, len(base), len(built), nd["changed"], nd["same"], nd["only_in_a"], nd["only_in_b"], json.dumps(nd["differing_fields_on_changed_nodes"], sort_keys=True),
                              len(smartx), len(newly_cusip), cnt["changed_nodes_not_smartx_security"], ra["nodes_sha256"][:12], str(rb.get("nodes_sha256", ""))[:12])})
    # ---- negative control: nodes outside the two groups the order moves keep their base bytes
    custody_cusip = [k for k, n in built.items() if k not in sm and n.get("node_kind") == "SECURITY" and is_cusip(n)]
    cc = set(custody_cusip)
    untouched = [k for k in built if k not in sm and k not in cc]
    untouched_same = sum(1 for k in untouched if base.get(k) == built[k])
    nocusip_smartx = [k for k in smartx if not is_cusip(built[k])]
    nocusip_class_same = sum(1 for k in nocusip_smartx if all(base[k].get(f) == built[k].get(f) for f in cls_fields))
    arms.append({"name": "negative_control_untouched_nodes_and_no_cusip_nodes", "verdict": "expected-diff" if untouched and untouched_same == len(untouched)
                 and nocusip_class_same == len(nocusip_smartx) else "FAIL", "negative_control": True,
                 "detail": "NEGATIVE CONTROL: nodes the changes do not reach stay as on base. Nodes that are neither a SmartX model asset nor a custody SECURITY node with a CUSIP "
                           "security_id: %d of %d byte-equal to base. SmartX model-asset nodes with NO CUSIP on built: %d, of which keep identical asset_class/sub_asset_class/"
                           "asset_class_basis: %d." % (untouched_same, len(untouched), len(nocusip_smartx), nocusip_class_same)})
    # ---- e56 on custody nodes whose security_id is a CUSIP
    cc_new = sum(1 for k in custody_cusip if not classified(base[k]) and classified(built[k]))
    cc_chg = sum(1 for k in custody_cusip if base[k] != built[k])
    cc_lost = sum(1 for k in custody_cusip if classified(base[k]) and not classified(built[k]))
    arms.append({"name": "custody_cusip_nodes_e56_fallback", "verdict": "expected-diff" if cc_new >= 1 and cc_lost == 0 else "FAIL", "negative_control": False,
                 "detail": "e56 on the non-SmartX SECURITY nodes whose security_id is a CUSIP: %d such nodes, %d changed, %d NEWLY CLASSIFIED (unclassified on base, a class on built), "
                           "%d classified->unclassified." % (len(custody_cusip), cc_chg, cc_new, cc_lost)})
    # ---- negative control: the ~269 build (unfixed 403) still refuses
    pr_refused = rpri["outcome"] == "REFUSED" and rb["outcome"] != "REFUSED"
    arms.append({"name": "negative_control_269_build_unfixed_403_still_refuses", "verdict": "expected-diff" if pr_refused else "FAIL", "negative_control": True,
                 "detail": "NEGATIVE CONTROL: the ~269 build (sha256 f8bd6f66..., e56 + IB-pr-403 WITHOUT the ticker= fact) on the same real inputs: gate=%s conditions=%s listed=%s "
                           "uploaded=%s; the fixed build: gate=%s conditions=%s. The gate rule applied to the ~269 candidate names %d lost CUSIP keys, to the fixed candidate %d. "
                           "SmartX classified->unclassified on ~269: %d, on the fixed build: %d."
                           % (rpri["outcome"], rpri["conditions"], rpri["listed"], rpri["uploaded"], rb["outcome"], rb["conditions"], len(lost_prior), len(lost_built),
                              t_prior.get("classified->unclassified", 0), lost_cls)})
    doc = {"to_id": "IRPT_BCKEND.TO-IB-pr-410", "pin": pin,
           "method": "base tree = IB-pr-402's built 49F bytes (sha256 3f2e738f...), built tree = base + e56 diff + IB-pr-403 diff + the IB-pr-410 ticker= fix, prior tree = the ~269 build "
                     "(base + e56 + IB-pr-403), each extracted into its own directory outside the worktree and driven by ~265's replay_publish_gate.py `run` (python -I) through "
                     "~269's replay_driver_cached.py (memoised canonical_lookup; dumps the candidate nodes before the gate sees them). Real arms: the tree's own run_firm on the real 49F "
                     "sources and the real served index through a read-through client whose writes are captured in memory. Nothing is put anywhere.",
           "gate_files": {"base_seconds": ra["seconds"], "built_seconds": rb["seconds"], "prior_seconds": rpri["seconds"]}, "arms": arms}
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
