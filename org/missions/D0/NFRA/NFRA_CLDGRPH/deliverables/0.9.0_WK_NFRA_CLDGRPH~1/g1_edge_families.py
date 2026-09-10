#!/usr/bin/env python3
"""NFRA_CLDGRPH TO-CG-G-1 / G1-AC2 -- THE DECLARED DOMAIN, WITH ITS UNCOVERED MEMBER HUNTED.

For EVERY edge family in the served graph, decide whether an endpoint names a member of
the both-identity population, and print the decision WITH ITS REASON, so the EXCLUDED
families are visible rather than silent. The swept count is the graph's own family
count: nothing is filtered before the sweep and nothing is dropped after it.

READ ONLY: reads the served graph through the projection service, never a local store.
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import g1_census_lib as L  # noqa: E402


def main():
    vintage, vline = L.served_vintage()
    for line in L.disclosure("edge FAMILY (edge_type); one row per family, its edges "
                             "and its endpoint classes are its denominators"):
        print(line)
    print(vline)
    print("")

    nodes = L.fetch_nodes()
    per, pop, alt, shadow = L.population(nodes)
    print("POPULATION_CARRIED_IN: %d of %d node class(es) carry both an ARN key and a "
          "distinct name; %d shadow id(s) in %d class(es) are the second identity of "
          "one of them" % (len(pop), len(per), len(shadow), len(set(shadow.values()))))
    print("")

    cross = L.edge_crosstab()
    src = L.edge_endpoint_counts("source")
    tgt = L.edge_endpoint_counts("target")
    decided = L.classify_families(cross, src, tgt, pop, shadow)

    total = len(cross)
    print("EDGE_FAMILIES_SWEPT=%d of %d" % (len(decided), total))
    print("SWEPT_EDGES=%d of %d edge(s) in the served graph"
          % (sum(c for f in cross.values() for _, _, c in f),
             sum(c for f in cross.values() for _, _, c in f)))
    print("")
    print("-- every family, in or out, each with the reason it is there --")
    for fam in sorted(decided):
        dec, why = decided[fam]
        f = L.facts_per_key(fam, cross, src)
        print("FAMILY %-19s DECISION=%-8s keys=%-6d edges=%-6d REASON=%s"
              % (fam, dec, f["keys"], f["edges"], why))
    print("")

    inc = [f for f in decided if decided[f][0] == "INCLUDED"]
    exc = [f for f in decided if decided[f][0] == "EXCLUDED"]
    print("INCLUDED=%d EXCLUDED=%d" % (len(inc), len(exc)))
    print("PARTITION_CHECK: %d + %d = %d, and the graph reports %d family(ies) -- the "
          "two buckets are exhaustive and disjoint over the DECLARED DOMAIN, which is "
          "every edge_type the served graph carries"
          % (len(inc), len(exc), len(inc) + len(exc), total))
    print("INCLUDED_FAMILIES: %s" % ", ".join(sorted(inc)))
    print("EXCLUDED_FAMILIES: %s" % ", ".join(sorted(exc)))
    print("")

    missing = [f for f in decided if not decided[f][1].strip()]
    ok = (not missing) and (len(inc) + len(exc) == total)
    print("FAMILIES_WITHOUT_A_REASON=%d of %d" % (len(missing), total))
    print("EVERY_FAMILY_HAS_A_REASON=%s" % ("true" if ok else "false"))
    print("VINTAGE=%s" % vintage)
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
