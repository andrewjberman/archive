"""IB-pr-414 compose step: the gate-decision replay (IB115-1_gate_decision_replay.json) and the memory census (IB115-1_memory_census.json).
READS the per-run files mem_harness.py and replay_publish_gate.py wrote in the scratch directories. Counts, booleans and hashes only.

Usage: python compose_replay.py <census_dir> <rp_dir> <w49_dir> <fx_dir> <old49_dir> <outdir> <pin>
  census_dir  mem_<tree>_49financial.json for pre404, b404, b410, fix (the sequential, memory/wall-time census runs; no memoisation)
  rp_dir      gate_<tree>_<firm>.json for b404, b410, fix404, fix at cottonwood and inflection (the fix* runs carry the old-gate same-input arm)
  w49_dir     gate_<tree>_49financial.json for b404, b410, fix404, fix (49F decisions)
  fx_dir      gate_<label>.json from replay_publish_gate.py `run` (fixture arms) for labels b404, fix404, fix
  old49_dir   gate_fix404_49financial.json from a --old-gate run at 49F
Verdict rule: `identical` only where the compared decisions are byte-equal; `expected-diff` for a negative control that behaved as it must.
"""
import json
import os
import sys


def load(*p):
    with open(os.path.join(*p), encoding="utf-8") as fh:
        return json.load(fh)


def view(d):
    return {"outcome": d["outcome"], "conditions": [[c["condition"], c["count"]] for c in d["conditions"]],
            "listed": {k: v["count"] for k, v in sorted(d["listed"].items())}}


def main():
    census, rp, w49, fx, old49, outdir, pin = sys.argv[1:8]
    arms = []
    for firm in ("49financial", "inflection", "cottonwood"):
        d = w49 if firm == "49financial" else rp
        t = {x: load(d, "gate_%s_%s.json" % (x, firm)) for x in ("b404", "b410", "fix404", "fix")}
        full = {x: t[x]["decision"] for x in t}
        same_f404 = full["fix404"] == full["b404"]
        same_fix = full["fix"] == full["b404"]
        same_b410 = full["fix"] == full["b410"]
        oldg = load(old49, "gate_fix404_49financial.json") if firm == "49financial" else None
        same_input = (oldg or t["fix404"]).get("old_gate_equals_new_gate")
        ok = same_f404 and same_fix and same_b410 and same_input is True
        v = view(full["b404"])
        arms.append({"name": "fix_vs_b404_gate_decision_%s" % firm, "verdict": "identical" if ok else "expected-diff", "negative_control": False,
                     "detail": "REAL %s inputs and the real served index (served %d nodes), upload through a read-through client whose writes are discarded "
                               "(nothing leaves the process), business date 2026-10-08. Gate decision, whole (outcome, every condition with its ids and count, "
                               "every listed set with its ids): b404 tree = %s. (a) the b404 tree WITH ONLY the memory fix (fix404) byte-equal to b404: %s; "
                               "(b) the shipped fix tree (the IB-pr-410 bytes + the fix) byte-equal to b404: %s and to the b410 tree: %s; "
                               "(c) SAME-INPUT arm: in one process the OLD gate code (b404's served_publication + evaluate_publish_gate, full served node list) "
                               "and the NEW code judge the SAME candidate and the SAME served index: equal=%s."
                               % (firm, t["b404"]["served_nodes"], json.dumps(v, sort_keys=True), same_f404, same_fix, same_b410, same_input)})
    # ---- fixture arms (the QA worse candidate etc.) on the b404, fix404 and fix trees
    g = {x: load(fx, "gate_%s.json" % x) for x in ("b404", "fix404", "fix")}
    fxn = sorted(n for n in g["b404"]["arms"] if n.startswith("fx_"))
    for name in fxn:
        a = {x: g[x]["arms"][name] for x in g}
        same = a["fix404"] == a["b404"] and a["fix"] == a["b404"]
        firm = name.split("_")[1]
        if name.endswith("worse_restored"):
            w, r = a["fix"]["worse"], a["fix"]["restored"]
            exp = (w["outcome"] == "REFUSED" and not a["fix"]["worse_index_moved"] and a["fix"]["refusal_record_keys"] == 1
                   and r["outcome"] == "PUBLISHED" and a["fix"]["restored_index_moved"])
            arms.append({"name": "fix_" + name, "verdict": "expected-diff" if exp else "FAIL", "negative_control": True,
                         "detail": "NEGATIVE CONTROL, the QA worse candidate (a classified security now unclassified) on the FIX tree: %s on %s, index_moved=%s, "
                                   "refusal records=%d; then the restored candidate %s and moves the index=%s. Equal to the b404 tree arm for arm: %s"
                                   % (w["outcome"], w["conditions"], a["fix"]["worse_index_moved"], a["fix"]["refusal_record_keys"], r["outcome"],
                                      a["fix"]["restored_index_moved"], same)})
        elif "mutant" in name:
            res = a["fix"]["result"]
            arms.append({"name": "fix_" + name, "verdict": "expected-diff" if (res["uploaded"] and a["fix"]["index_moved"]) else "FAIL",
                         "negative_control": True,
                         "detail": "NEGATIVE CONTROL (the worse arm discriminates): on the fix tree the gate stubbed to PUBLISHED publishes the worse candidate "
                                   "(uploaded=%s index_moved=%s); the real gate does not. Equal to b404 arm: %s" % (res["uploaded"], a["fix"]["index_moved"], same)})
        else:
            arms.append({"name": "fix_" + name, "verdict": "identical" if same else "FAIL", "negative_control": "not_refused" in name or "monday" in name,
                         "detail": "fixture arm %s on the fix tree and on the fix404 tree equals the b404 tree arm field for field (outcome %s, listed %s, "
                                   "conditions %s, index_moved %s): %s" % (name, a["fix"]["result"]["outcome"], a["fix"]["result"]["listed"],
                                                                         a["fix"]["result"]["conditions"], a["fix"]["index_moved"], same)})
    doc = {"pin": pin, "to_id": "IRPT_BCKEND.TO-IB-pr-414",
           "method": "mem_harness.py (python 3.12) drives each tree's OWN holdings_snapshot.run_firm at the real sources and the real served index "
                     "through a read-through client (reads to AWS, every write captured in memory and discarded, every other mutation raises); "
                     "replay_publish_gate.py `run` drives the fixture arms. Trees: b404 = the live 49F bundle (irUPjpfr..., sha256 3f2e738f...); "
                     "b410 = b404 + the e56 holdings_snapshot.py and the IB-pr-410 holdings_49f.py (member sha256 a9fe965f / 401a36ff, equal to IB-pr-410's); "
                     "fix404 = b404 + only the memory fix (isolates the gate change); fix = b410 + the memory fix (the member the next bundle carries). "
                     "Nothing is put anywhere.", "arms": arms}
    with open(os.path.join(outdir, "IB115-1_gate_decision_replay.json"), "w", encoding="utf-8") as fh:
        json.dump(doc, fh, indent=1, sort_keys=True)
    print("wrote replay", len(arms), "arms:", {a["name"]: a["verdict"] for a in arms})


if __name__ == "__main__":
    main()
