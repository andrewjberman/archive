"""IB-pr-406: counts-only class/basis transitions between the base and built 49F candidate node files.
Usage: python -I class_transitions.py <scratch_dir> <out.json>   (scratch holds nodes_base_49f_49financial.json and nodes_built_49f_49financial.json)
No id, symbol or name is written: counts only.
"""
import collections
import json
import sys


def state(node):
    """'classified' for any asset class other than None/unclassified, else the value."""
    return "classified" if node.get("asset_class") not in (None, "unclassified") else str(node.get("asset_class"))


def main():
    scratch, out_path = sys.argv[1], sys.argv[2]
    with open(scratch + "/nodes_base_49f_49financial.json", encoding="utf-8") as fh:
        base = json.load(fh)
    with open(scratch + "/nodes_built_49f_49financial.json", encoding="utf-8") as fh:
        built = json.load(fh)
    trans, basis, value_moves = collections.Counter(), collections.Counter(), collections.Counter()
    disp, kinds, fields, groups = collections.Counter(), collections.Counter(), collections.Counter(), collections.Counter()
    for key, node in built.items():
        before = base[key]
        if node == before:
            continue
        smartx = node.get("node_kind") == "SECURITY" and ":asset:" in key
        if smartx:
            trans[(state(before), state(node))] += 1
            basis[(before.get("asset_class_basis"), node.get("asset_class_basis"))] += 1
            if (before.get("display") or {}).get("symbol") != (node.get("display") or {}).get("symbol"):
                disp["symbol_changed"] += 1
            if (before.get("display") or {}).get("label") != (node.get("display") or {}).get("label"):
                disp["label_changed"] += 1
            if before.get("asset_class") != node.get("asset_class"):
                value_moves[(state(before), state(node), before.get("asset_class"), node.get("asset_class"))] += 1
        else:
            kinds[node.get("node_kind")] += 1
            for field in set(node) | set(before):
                if node.get(field) != before.get(field):
                    fields[field] += 1
            groups[(node.get("node_kind"), (node.get("security_id") or {}).get("namespace"), state(before), state(node))] += 1
    out = {"smartx_class_state_transitions_base_to_built": {"%s -> %s" % k: v for k, v in trans.items()},
           "smartx_basis_transitions": {"%s -> %s" % k: v for k, v in basis.items()},
           "smartx_display": dict(disp),
           "smartx_asset_class_value_transitions": {"%s/%s: %s -> %s" % k: v for k, v in value_moves.items()},
           "non_smartx_changed_kinds": dict(kinds), "non_smartx_changed_fields": dict(fields),
           "non_smartx_changed_by_kind_ns_state": {"%s|%s|%s->%s" % k: v for k, v in groups.items()}}
    with open(out_path, "w", encoding="utf-8") as fh:
        json.dump(out, fh, indent=1, sort_keys=True)
    print(json.dumps(out, indent=1, sort_keys=True))


if __name__ == "__main__":
    main()
