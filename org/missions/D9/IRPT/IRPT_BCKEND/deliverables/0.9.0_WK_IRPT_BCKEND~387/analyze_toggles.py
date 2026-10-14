"""Scratch (IB-pr-542 amendment): the toggle attribution arithmetic on the per-node signatures. Read only; run with python -I.

Inputs are the signature files written by cot_harness.py. A beyond-rule item is a changed classification field of a node
(base against live) that is not the signed cash-rule item (identity-patch). A toggle REMOVES an item when the toggled
run's value for that node and field equals the live value. Nothing is written to S3 or to any repository tree.
"""
import json
import sys
from collections import Counter
from pathlib import Path

sys.path.insert(0, "C:/dev/_scratch387")
import cot_harness as ch  # noqa: E402

OUT = Path("C:/dev/_scratch387/out")
TOGGLES = [
    # (short name, commit, record name, resolution, toggled_files file)
    ("account", "7ace8548905d66ef98358c384cb320f12c2683e4", "account_id", "non_closure_taken_from_head", "account"),
    ("keyed", "3f2bdda5784ec1c71eaeb78ffb218daafe517d29", "keyed_gate", "non_closure_taken_from_head", "keyed"),
    ("cusip", "01e843ce2e11be4e90e8f369f5e27c6925479398", "cusip_fallback", "hand_resolved_closure_member", "cusip"),
    ("multi", "4cc72587d6336809adbb3a46b119a304ef0a6dff", "multi_asset", "hand_resolved_closure_member", "multi"),
]
CLASS_FIELDS = ch.CLASS_FIELDS


def by_id(rows):
    return {r["id"]: r for r in rows}


def signed_item(nid, it, L, B, IDN):
    if not (it["kind"] == "cls" and it["field"] == "asset_class" and nid in IDN):
        return False
    id_ac = IDN[nid]["cls"].get("asset_class")
    b_ac = B[nid]["cls"].get("asset_class")
    l_ac = L[nid]["cls"].get("asset_class")
    return id_ac is not None and b_ac != id_ac and l_ac == id_ac


def analyze(L, B, IDN, T_by_name, toggled_files, notes_tag):
    """L, B, IDN: live, base, identity signatures (dicts by node id); T_by_name: toggled signatures by name."""
    common = [k for k in L if k in B]
    changed = {}
    for nid in sorted(common, key=str):
        items = ch.diff_items(L[nid], B[nid])
        if items:
            changed[nid] = items
    beyond_items = {}
    signed_nodes = set()
    for nid, items in changed.items():
        keep = []
        for it in items:
            if signed_item(nid, it, L, B, IDN):
                signed_nodes.add(nid)
            else:
                keep.append(it)
        if keep:
            beyond_items[nid] = keep
    for nid, items in beyond_items.items():
        for it in items:
            assert it["kind"] == "cls", ("non-classification beyond item", nid, it["kind"], it["field"])
    beyond = set(beyond_items)
    total = len(beyond)
    removed = {}
    item_removed = {}
    results = {}
    for name, commit, rec_name, resolution, _ in TOGGLES:
        T = T_by_name[name]
        rem_nodes, rem_items = set(), set()
        groups = Counter()
        largest = 0.0
        for nid, items in beyond_items.items():
            if nid not in T:
                continue
            ok_all = True
            hit = []
            for it in items:
                f = it["field"]
                if T[nid]["cls"].get(f) == L[nid]["cls"].get(f):
                    hit.append(it)
                else:
                    ok_all = False
            for it in hit:
                rem_items.add((nid, it["field"], it["label"]))
                groups[it["label"]] += 1
            if ok_all:
                rem_nodes.add(nid)
                for it in changed[nid]:
                    if it["kind"] == "num":
                        largest = max(largest, it["delta"])
        removed[name] = rem_nodes
        item_removed[name] = rem_items
        # groups count distinct nodes per label
        per_label = {}
        for nid_f_label in rem_items:
            per_label.setdefault(nid_f_label[2], set()).add(nid_f_label[0])
        results[name] = {
            "name": rec_name,
            "commit": commit,
            "revert_applied": True,
            "resolution": resolution,
            "toggled_files": sorted(toggled_files[name]),
            "removed_nodes": len(rem_nodes),
            "largest_abs_delta": round(largest, 6),
            "groups": [{"group": k, "nodes": len(v)} for k, v in sorted(per_label.items())],
        }
    # moved check: every node the toggle changed relative to base must be a beyond node (other behaviour unchanged)
    moved = {}
    for name, *_ in TOGGLES:
        T = T_by_name[name]
        mv = set()
        for nid in B:
            if nid in T and ch.diff_items(B[nid], T[nid]):
                mv.add(nid)
        moved[name] = {"moved_nodes": len(mv), "moved_outside_beyond": len(mv - beyond),
                       "node_sets_equal": set(B) == set(T)}
    union = set().union(*removed.values())
    rsum = sum(len(removed[n]) for n in removed)
    overlap = rsum - len(union)
    joint, unattr, unattr_fields = 0, 0, Counter()
    for nid in beyond - union:
        items = beyond_items[nid]
        covered = True
        for it in items:
            if not any((nid, it["field"], it["label"]) in item_removed[n] for n in removed):
                covered = False
                unattr_fields[it["label"]] += 1
        if covered:
            joint += 1
        else:
            unattr += 1
    assert rsum - overlap + joint + unattr == total, (rsum, overlap, joint, unattr, total)
    return {
        "beyond_rule_total": total,
        "signed_nodes": len(signed_nodes),
        "per_commit": [results[n] for n, *_ in TOGGLES],
        "overlap_nodes": overlap,
        "joint_nodes": joint,
        "unattributed_nodes": unattr,
        "unattributed_item_labels": dict(unattr_fields),
        "moved": moved,
        "_beyond": beyond,
        "_beyond_items": beyond_items,
        "_L": L, "_B": B, "_I": IDN,
    }


def strip(res):
    return {k: v for k, v in res.items() if not k.startswith("_")}


def run_digest(res):
    return ch.digest_of(res["per_commit"])


def load_run(tag):
    L = by_id(ch.load_gz(OUT / ("live_%s.json.gz" % tag)))
    B = by_id(ch.load_gz(OUT / ("base_%s.json.gz" % tag)))
    IDN = by_id(ch.load_gz(OUT / ("id_%s.json.gz" % tag)))
    T = {name: by_id(ch.load_gz(OUT / ("tog_%s_%s.json.gz" % (name, tag)))) for name, *_ in TOGGLES}
    return L, B, IDN, T


def main():
    tf = {}
    for name, _, _, _, f in TOGGLES:
        tf[name] = [x for x in Path("C:/dev/_scratch387/tf_%s.txt" % {"account": "account", "keyed": "keyed", "cusip": "cusip", "multi": "multi"}[f]).read_text(encoding="utf-8").split("\n") if x]
    out = {}
    for tag in ("r1", "r2"):
        L, B, IDN, T = load_run(tag)
        res = analyze(L, B, IDN, T, tf, tag)
        out[tag] = res
        print("%s: total=%d overlap=%d joint=%d unattributed=%d digest=%s" % (
            tag, res["beyond_rule_total"], res["overlap_nodes"], res["joint_nodes"], res["unattributed_nodes"],
            run_digest(res)[:16]))
        for pc in res["per_commit"]:
            print("   ", pc["name"], "removed", pc["removed_nodes"], "largest", pc["largest_abs_delta"], pc["groups"])
        print("    moved", res["moved"])
        print("    unattributed labels", res["unattributed_item_labels"])
    r1, r2 = out["r1"], out["r2"]
    assert run_digest(r1) == run_digest(r2) and r1["per_commit"] == r2["per_commit"], "run digests differ"
    # mutant: one unchanged node's sub_asset_class set to a value that is neither live nor base, in base and every toggled run
    L, B, IDN, T = load_run("r1")
    cands = []
    for nid in sorted(B, key=str):
        if nid in r1["_beyond"] or nid not in L:
            continue
        if ch.diff_items(L[nid], B[nid]):
            continue
        if any(nid in T[n] and ch.diff_items(B[nid], T[n][nid]) for n in T):
            continue
        cands.append(nid)
    assert cands, "no unchanged node to plant the mutant on"
    m = cands[0]
    B2 = {k: json.loads(json.dumps(v)) for k, v in B.items()}
    B2[m]["cls"]["sub_asset_class"] = "__mutant__"
    T2 = {}
    for n in T:
        T2[n] = {k: json.loads(json.dumps(v)) for k, v in T[n].items()}
        T2[n][m]["cls"]["sub_asset_class"] = "__mutant__"
    mres = analyze(L, B2, IDN, T2, tf, "mutant")
    flagged = mres["unattributed_nodes"] == r1["unattributed_nodes"] + 1
    summary = {
        "r1": strip(r1), "r2": strip(r2),
        "run1_digest": run_digest(r1), "run2_digest": run_digest(r2),
        "mutant": {"planted": "sub_asset_class of one unchanged Cottonwood node set to a value neither live nor base, in the base signature and in every toggled signature (a change no single toggle removes)",
                   "beyond_rule_total_with_mutant": mres["beyond_rule_total"],
                   "unattributed_nodes_with_mutant": mres["unattributed_nodes"],
                   "flagged": flagged, "unattributed_nodes": r1["unattributed_nodes"]},
    }
    (OUT / "analysis.json").write_text(json.dumps(summary, sort_keys=True, indent=1), encoding="utf-8")
    print("mutant: total=%d unattributed=%d flagged=%s" % (mres["beyond_rule_total"], mres["unattributed_nodes"], flagged))
    print("WROTE", OUT / "analysis.json")


if __name__ == "__main__":
    main()
