"""IB-pr-406 replay driver: ~265's replay_publish_gate.py `run` mode, with two additions that change NO answer.
  1. canonical_lookup is memoised per process (a HIT is already cached by the canonical client; a MISS is not, and the built tree
     asks the table once per node for `CUSIP:<id>`: 115k sequential DynamoDB GetItems, 3,907 s on the first uncached run).
     Same key -> same answer within one run; the table is read-only here.
  2. the candidate nodes are written (as ~265's capturing_land does for a published candidate) BEFORE the gate sees them, so a
     REFUSED candidate is still comparable node by node.
AWS READS ONLY. Usage: python -I replay_driver_cached.py <repo_root> <tree> <scratch> <label> <firm>
"""
import json
import os
import sys


def main():
    root, tree, scratch, label, firm = sys.argv[1:6]
    sys.path.insert(0, os.path.join(root, "org", "missions", "D9", "IRPT", "IRPT_BCKEND", "deliverables", "0.9.0_WK_IRPT_BCKEND~265", "replay"))
    sys.path.insert(0, os.path.join(tree, "data", "assets", "scripts", "gold", "investor_reporting"))
    import holdings_snapshot as hs
    assert os.path.abspath(hs.__file__).startswith(os.path.abspath(tree)), "holdings_snapshot resolved outside the bundle"
    import replay_publish_gate as rp

    orig_lookup = hs._NarrowedClassifier.canonical_lookup
    memo = {}
    stats = {"calls": 0, "distinct": 0}

    def cached_lookup(self, ticker):
        stats["calls"] += 1
        if ticker not in memo:
            stats["distinct"] += 1
            memo[ticker] = orig_lookup(self, ticker)
        return memo[ticker]

    hs._NarrowedClassifier.canonical_lookup = cached_lookup

    orig_gate = hs.evaluate_publish_gate
    path = os.path.join(scratch, "nodes_%s_%s.json" % (label, firm))

    def dumping_gate(candidate, served, *a, **k):
        nodes = candidate.get("nodes") or []
        if len(nodes) > 1000 and not os.path.exists(path):
            with open(path, "w", encoding="utf-8") as fh:
                json.dump({n["node_id"]: n for n in nodes}, fh, sort_keys=True, default=str)
        return orig_gate(candidate, served, *a, **k)

    hs.evaluate_publish_gate = dumping_gate
    rp.run_mode(tree, scratch, label, [firm])
    print("lookup calls %(calls)d distinct %(distinct)d" % stats)


if __name__ == "__main__":
    main()
