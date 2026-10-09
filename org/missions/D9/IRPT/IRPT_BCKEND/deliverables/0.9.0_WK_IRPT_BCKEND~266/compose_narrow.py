"""IB-pr-402 compose step: reads the per-firm gate files that ~265's replay_publish_gate.py `run` mode wrote for the NARROW tree
(label narrow_<short>) and the LIVE tree (label live_<short>), and writes IB103-2_narrow_bundle_replay.json.

Usage: python -I compose_narrow.py <repo_root> <scratch_dir> <out.json> <pin>
Reuses ~265's node_diff and pub_view; the verdict rules are ~265's real_arm / fx rules, one pair of trees per firm.
Counts, booleans and hashes only: no account id, no security id, no name.
"""
import json
import os
import sys

SHORT = {"49financial": "49f", "inflection": "inf", "cottonwood": "cot"}


def main():
    root, scratch, out_path, pin = sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4]
    sys.path.insert(0, os.path.join(root, "org", "missions", "D9", "IRPT", "IRPT_BCKEND", "deliverables",
                                    "0.9.0_WK_IRPT_BCKEND~265", "replay"))
    import replay_publish_gate as rp

    def load(lb):
        with open(os.path.join(scratch, "gate_%s.json" % lb), encoding="utf-8") as fh:
            return json.load(fh)

    arms = []
    hashes = {}
    for firm in sorted(SHORT):
        s = SHORT[firm]
        b, lv = load("narrow_" + s), load("live_" + s)
        hashes[firm] = {"narrow_holdings_snapshot_sha256": b["holdings_snapshot_sha256"],
                        "live_holdings_snapshot_sha256": lv["holdings_snapshot_sha256"]}
        ba, la = b["arms"]["real_" + firm], lv["arms"]["real_" + firm]
        name = "real_%s_live_vs_built" % firm
        if "error" in ba or "error" in la:
            arms.append({"name": name, "verdict": "expected-diff", "negative_control": False,
                         "detail": "NOT REPLAYED: built=%r live=%r" % (ba.get("error"), la.get("error"))})
        else:
            nd = rp.node_diff(os.path.join(scratch, "nodes_live_%s_%s.json" % (s, firm)),
                              os.path.join(scratch, "nodes_narrow_%s_%s.json" % (s, firm)))
            same_nodes = ba["nodes_sha256"] == la["nodes_sha256"]
            same_stable = ba["stable_body_sha256"] == la["stable_body_sha256"]
            ok = ba["outcome"] == "PUBLISHED" and ba["uploaded"] and not ba["conditions"]
            ident = ok and la["uploaded"] and same_nodes and same_stable and nd["changed"] == 0 \
                and nd["only_in_a"] == 0 and nd["only_in_b"] == 0
            arms.append({"name": name, "verdict": "identical" if ident else "expected-diff", "negative_control": False,
                         "detail": "REAL inputs + real served index, writes captured in memory. NARROW tree (live bundle + holdings_snapshot.py moved by "
                                   "9af6811b61 + ce6e2a218e) versus the LIVE bundle. NARROW gate=%s conditions=%s listed=%s%s; live gate=%s. "
                                   "Candidate nodes identical=%s (sha256 %s/%s); stable body (all but clocks and source_set_revision) identical=%s; "
                                   "whole revision identical=%s (clocks identical=%s, source_set_revision identical=%s); puts %d/%d; nodes %s/%s; "
                                   "accounts %s/%s; business_date %s/%s. Node diff live->narrow: %s"
                                   % (ba["outcome"], ba["conditions"], ba["listed"], "" if ok else " ** NARROW DID NOT PUBLISH **",
                                      la["outcome"], same_nodes, la["nodes_sha256"][:12], ba["nodes_sha256"][:12], same_stable,
                                      ba["revision"] == la["revision"], ba["clocks_sha256"] == la["clocks_sha256"],
                                      ba["source_set_revision_sha256"] == la["source_set_revision_sha256"], la["put_count"], ba["put_count"],
                                      la["node_count"], ba["node_count"], la["unique_account_count"], ba["unique_account_count"],
                                      la["business_date"], ba["business_date"], json.dumps(nd, sort_keys=True))})
        for nm in sorted(n for n in b["arms"] if n.startswith("fx_")):
            ba2, la2 = b["arms"][nm], lv["arms"].get(nm)
            if "mutant" in nm:
                wr = b["arms"]["fx_%s_worse_restored" % firm]
                res = ba2["result"]
                stub_ok = bool(res["uploaded"] and ba2["index_moved"])
                arms.append({"name": nm, "verdict": "expected-diff" if stub_ok else "FAIL", "negative_control": True,
                             "detail": "NEGATIVE CONTROL (the worse arm discriminates): the SAME worse candidate with evaluate_publish_gate stubbed to "
                                       "PUBLISHED publishes and moves the index (uploaded=%s index_moved=%s); with the real gate the narrow tree %s it "
                                       "(index_moved=%s)" % (res["uploaded"], ba2["index_moved"], wr["worse"]["outcome"], wr["worse_index_moved"])})
                continue
            if nm.endswith("worse_restored"):
                w, r, lw, lr = ba2["worse"], ba2["restored"], la2["worse"], la2["restored"]
                exp = (w["outcome"] == "REFUSED" and not ba2["worse_index_moved"] and ba2["refusal_record_keys"] == 1
                       and r["outcome"] == "PUBLISHED" and ba2["restored_index_moved"])
                live_publishes_worse = bool(lw["uploaded"] and la2["worse_index_moved"])
                arms.append({"name": nm, "verdict": "expected-diff" if exp and live_publishes_worse else "FAIL", "negative_control": False,
                             "detail": "QA table, one run. NARROW: worse arm %s on %s, index_moved=%s, refusal records=%d, then restored arm %s "
                                       "index_moved=%s. LIVE (no gate): worse arm uploaded=%s index_moved=%s (the worse candidate IS published), "
                                       "restored uploaded=%s index_moved=%s"
                                       % (w["outcome"], w["conditions"], ba2["worse_index_moved"], ba2["refusal_record_keys"], r["outcome"],
                                          ba2["restored_index_moved"], lw["uploaded"], la2["worse_index_moved"], lr["uploaded"],
                                          la2["restored_index_moved"])})
                continue
            res, lres = ba2["result"], la2["result"]
            want = {"all_unknown_loses_account": "account_lost_not_refused", "closed_account_not_refused": "closed_accounts_not_refused",
                    "monday_not_stale": None}
            key = [k for k in want if nm.endswith(k)][0]
            exp = res["outcome"] == "PUBLISHED" and ba2["index_moved"] and (want[key] is None or res["listed"].get(want[key]) == 1)
            same_pub = rp.pub_view(res) == rp.pub_view(lres) and ba2["index_moved"] == la2["index_moved"]
            title = {"all_unknown_loses_account": "an all-UNKNOWN firm loses an account: PUBLISHED and listed",
                     "closed_account_not_refused": "NEGATIVE CONTROL: an account the source records TERMINATED is listed, never refused",
                     "monday_not_stale": "NEGATIVE CONTROL: a Monday candidate is not stale against Friday's served frontier"}[key]
            arms.append({"name": nm, "verdict": "identical" if same_pub and exp else "expected-diff", "negative_control": key != "all_unknown_loses_account",
                         "detail": "%s. NARROW %s index_moved=%s listed=%s conditions=%s%s; LIVE (no gate) uploaded=%s index_moved=%s; the landed revision is %s"
                                   % (title, res["outcome"], ba2["index_moved"], res["listed"], res["conditions"], "" if exp else " ** UNEXPECTED **",
                                      lres["uploaded"], la2["index_moved"], "identical in both trees" if same_pub else "different")})
    doc = {"to_id": "IRPT_BCKEND.TO-IB-pr-402", "pin": pin, "holdings_snapshot_hashes": hashes,
           "method": "each bundle tree (narrow, live) extracted into its own directory and driven by ~265's replay_publish_gate.py `run` (python -I): "
                     "real arms = the tree's own run_firm on the real sources and the real served index through a read-through client whose writes are "
                     "captured in memory (every other mutation raises); fixture arms = an in-memory versioned bucket under the tree's real "
                     "HoldingsPublication. Nothing is put anywhere. as_of_timestamp (a datetime.now() clock) is excluded from the stable body.",
           "arms": arms}
    with open(out_path, "w", encoding="utf-8") as fh:
        json.dump(doc, fh, indent=1, sort_keys=True)
    print("wrote", out_path, len(arms), "arms")


if __name__ == "__main__":
    main()
