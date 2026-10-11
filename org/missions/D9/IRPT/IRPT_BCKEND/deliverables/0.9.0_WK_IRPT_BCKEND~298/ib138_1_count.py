"""IB138-1 counting code (read only): sleeve nodes with and without a security node beneath them.

count(nodes) takes the node list of one holdings publication (the union of its parts) and returns counts only.

A SLEEVE node is recognised by its member node_kind: it is "SLEEVE" (the contract's enum member, anywhere in the tree)
or it is "CATEGORY" with an ACCOUNT as its parent (the account-level sleeve since ruling msg 102475: Models, SMAs, Client).
A security node is node_kind "SECURITY". "Beneath" is at any depth: the parent chain is walked up from each security node.
The same function reports the strict SLEEVE kind alone, and MODEL_LEAF nodes, counted the same way.
"""
import json
import sys


def count(nodes):
    parent_of = {n["node_id"]: n.get("parent_node_id") for n in nodes}
    kind_of = {n["node_id"]: n.get("node_kind") for n in nodes}
    kids_of = {}
    for n in nodes:
        kids_of.setdefault(n.get("parent_node_id"), []).append(n)
    above_a_security, above_an_actual_security = set(), set()
    for n in nodes:
        if n.get("node_kind") != "SECURITY":
            continue
        cur, seen = parent_of.get(n["node_id"]), set()
        while cur is not None and cur not in seen:
            seen.add(cur)
            above_a_security.add(cur)
            if n.get("basis") != "TARGET":
                above_an_actual_security.add(cur)
            cur = parent_of.get(cur)

    def root_of(node_id):
        cur, seen = node_id, set()
        while parent_of.get(cur) is not None and cur not in seen:
            seen.add(cur)
            cur = parent_of[cur]
        return cur

    def path_of(n):
        hp = (n.get("classification") or {}).get("hierarchy_path") or []
        return " > ".join(hp) if hp else "(no path)"

    def label(n):
        facts = (n.get("classification") or {}).get("capability_facts") or []
        mark = ("capability_fact DRILL WITHHELD" if any(str(f).startswith("DRILL WITHHELD") for f in facts)
                else "no mark in the node")
        kinds = sorted({k.get("node_kind") for k in kids_of.get(n["node_id"], [])})
        return mark + "; children: " + (",".join(kinds) if kinds else "none")

    def split(picked):
        with_sec = [n for n in picked if n["node_id"] in above_a_security]
        none = [n for n in picked if n["node_id"] not in above_a_security]
        only_target = [n for n in with_sec if n["node_id"] not in above_an_actual_security]
        labels, labels_nonzero, by_path = {}, {}, {}
        for n in none:
            labels[label(n)] = labels.get(label(n), 0) + 1
            if (n.get("amount") or {}).get("value") not in (None, 0, 0.0):
                labels_nonzero[label(n)] = labels_nonzero.get(label(n), 0) + 1
        for n in picked:
            row = by_path.setdefault(path_of(n), {"nodes": 0, "with_a_security_node_beneath": 0, "with_none": 0})
            row["nodes"] += 1
            row["with_none" if n["node_id"] not in above_a_security else "with_a_security_node_beneath"] += 1
        return {"nodes": len(picked), "with_a_security_node_beneath": len(with_sec), "with_none": len(none),
                "of_those_with_none_carrying_a_nonzero_amount": sum(
                    1 for n in none if (n.get("amount") or {}).get("value") not in (None, 0, 0.0)),
                "of_those_with_one_only_target_basis_securities": len(only_target),
                "accounts_holding_such_a_leaf": len({root_of(n["node_id"]) for n in none}),
                "labels_on_those_with_none": labels,
                "labels_on_those_with_none_and_a_nonzero_amount": labels_nonzero, "by_hierarchy_path": by_path}

    by_kind = {}
    for n in nodes:
        by_kind[n["node_kind"]] = by_kind.get(n["node_kind"], 0) + 1
    sleeves = [n for n in nodes if n.get("node_kind") == "SLEEVE"
               or (n.get("node_kind") == "CATEGORY" and kind_of.get(n.get("parent_node_id")) == "ACCOUNT")]
    return {"nodes_total": len(nodes), "nodes_by_kind": by_kind,
            "sleeves": split(sleeves),
            "strict_SLEEVE_kind": split([n for n in nodes if n.get("node_kind") == "SLEEVE"]),
            "MODEL_LEAF": split([n for n in nodes if n.get("node_kind") == "MODEL_LEAF"])}


def plant():
    """The planted snapshot: an account, a sleeve with two security nodes beneath it, a sleeve with none (5 nodes;
    the order says four, which cannot hold an account, two sleeves and two securities)."""
    def node(i, parent, kind):
        return {"node_id": i, "parent_node_id": parent, "node_kind": kind, "basis": "OBSERVED",
                "classification": {"capability_facts": []}}
    return [node("A", None, "ACCOUNT"), node("S1", "A", "SLEEVE"), node("S2", "A", "SLEEVE"),
            node("X1", "S1", "SECURITY"), node("X2", "S1", "SECURITY")]


def control():
    got = count(plant())
    s = got["sleeves"]
    planted = {"nodes_total": 5, "sleeves": 2, "sleeves_with_a_security_node_beneath": 1, "sleeves_with_none": 1,
               "accounts_holding_such_a_leaf": 1}
    read = {"nodes_total": got["nodes_total"], "sleeves": s["nodes"],
            "sleeves_with_a_security_node_beneath": s["with_a_security_node_beneath"],
            "sleeves_with_none": s["with_none"], "accounts_holding_such_a_leaf": s["accounts_holding_such_a_leaf"]}
    return planted, read


if __name__ == "__main__":
    planted, read = control()
    print(json.dumps({"planted": planted, "read": read, "equal": planted == read}, sort_keys=True))
    sys.exit(0 if planted == read else 1)
