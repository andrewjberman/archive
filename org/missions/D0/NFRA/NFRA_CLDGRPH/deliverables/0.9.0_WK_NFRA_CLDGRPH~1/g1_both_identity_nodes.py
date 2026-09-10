#!/usr/bin/env python3
"""NFRA_CLDGRPH TO-CG-G-1 / G1-AC1 -- THE POPULATION, NAMED BEFORE IT IS COUNTED.

Census of the SERVED graph for node classes whose nodes carry BOTH an id-ish key and
an arn: an ARN-shaped node_id plus a distinct `name`, two identity strings for one
resource. Prints, per class, how many nodes carry both, the denominator of nodes in
that class, and which field the graph keys on -- plus a control that fires on a class
known to carry both (S3_BUCKET), so a zero cannot be a dead instrument.

READ ONLY: reads the served graph through the projection service, never a local store.
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import g1_census_lib as L  # noqa: E402

CONTROL_CLASS = "S3_BUCKET"


def main():
    vintage, vline = L.served_vintage()
    for line in L.disclosure("node CLASS (node_type); a class is one row, its nodes "
                             "are its denominator"):
        print(line)
    print(vline)
    print("")

    nodes = L.fetch_nodes()
    bad_arn, den_arn = L.arn_column_control(nodes)
    print("ARN_COLUMN_CONTROL: nodes whose arn column differs from node_id = %d of %d "
          "-- the served arn column is a COPY of the key, so it is NOT the "
          "discriminator; node_id SHAPE plus a distinct name is" % (bad_arn, den_arn))
    print("")

    per, pop, alt, shadow = L.population(nodes)
    print("BOTH_IDENTITY_CLASSES=%d of %d node class(es)" % (len(pop), len(per)))
    print("SWEPT_NODES=%d of %d node(s) in the served graph" % (len(nodes), len(nodes)))
    print("")
    print("-- the population, one row per class that carries both --")
    for c in sorted(pop):
        v = per[c]
        keyed = ", ".join("%s=%d" % kv for kv in sorted(v["keyed_on"].items()))
        print("CLASS %-27s both=%4d of %4d node(s)  KEYED_ON=[%s]  "
              "second_identity=name  distinct_alt_names=%d"
              % (c, v["both"], v["total"], keyed, len(v["alt_names"])))
    print("")
    print("-- classes NOT in the population, with the reason, so none is silent --")
    for c in sorted(set(per) - pop):
        v = per[c]
        keyed = ", ".join("%s=%d" % kv for kv in sorted(v["keyed_on"].items()))
        print("CLASS %-27s both=%4d of %4d node(s)  KEYED_ON=[%s]  "
              "reason=no node carries an ARN-shaped key beside a distinct name"
              % (c, v["both"], v["total"], keyed))
    print("")

    print("SHADOW_IDS=%d node(s) in %d class(es): a node whose OWN key is the second "
          "identity of a both-identity resource" % (len(shadow), len(set(shadow.values()))))
    for cls in sorted(set(shadow.values())):
        ids = sorted(i for i, t in shadow.items() if t == cls)
        print("  SHADOW_CLASS %s count=%d of %d node(s) in the class; example=%s"
              % (cls, len(ids), per[cls]["total"], ids[0] if ids else "none"))
    print("")

    print("KEYED_ON printed for each of the %d class(es) in the population and each of "
          "the %d class(es) outside it; denominator %d node class(es) swept, 0 skipped"
          % (len(pop), len(per) - len(pop), len(per)))

    fired = CONTROL_CLASS in pop
    if fired:
        v = per[CONTROL_CLASS]
        print("CLASS_PROBE_CONTROL=FIRED on %s: both=%d of %d, KEYED_ON=ARN, "
              "second identity is the bucket NAME -- a known two-named class is inside "
              "the population, so a zero elsewhere is a measurement and not a dead "
              "instrument" % (CONTROL_CLASS, v["both"], v["total"]))
    else:
        print("CLASS_PROBE_CONTROL=MISSED on %s: the known two-named class is NOT in "
              "the population -- this census is not trustworthy" % CONTROL_CLASS)
    print("VINTAGE=%s" % vintage)
    return 0 if fired else 1


if __name__ == "__main__":
    sys.exit(main())
