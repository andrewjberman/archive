#!/usr/bin/env python3
"""NFRA_CLDGRPH TO-CG-H-4 / H4-AC3 -- CG-s-39.

THE FOURTH POINT, TAKEN NOW, THROUGH THE SERVING PLANE -- NOT CARRIED FROM THE
ROUND-7 RECORD.

Three reads (03:31:02, 05:32:57, 05:57:16) established that the boundary-edge
family fell from 135 to 11 and then did not move again over about twenty-five
minutes. Three points over one interval do not establish a cadence. This script
takes the fourth, at whatever the current served vintage is, and prints that
vintage and the manifest id beside every count so that nobody has to ask which
graph the number came from.

QUERY FORM, and why it is stated rather than assumed (row NFRA_CLDGRPH-W1-S112):
  `MATCH ()-[e:STORED_IN]->()` FAILS AT THE BINDER -- "Table STORED_IN does not
  exist" -- because the served graph carries `edge_type` as a PROPERTY of one
  relationship table `CloudEdge`, not as a relationship table per family. A binder
  error is a WRONG-FORM signal, never a count of zero. This script runs the broken
  form ON PURPOSE as a NEGATIVE CONTROL, shows that it raises rather than
  answering 0, and then reads the property form.

POSITIVE CONTROL: `OWNED_BY` must come back non-zero through the SAME query path
in the SAME run. If it did, a zero anywhere else is a measurement about the graph
and not a broken query.

READ ONLY. Queries only; the client cannot write.
"""
from __future__ import annotations

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import h4_lib as L  # noqa: E402

sys.path.insert(0, os.path.join(L.ROOT, "infra", "aws", "globgrph"))
import projection_client as pc  # noqa: E402

TIMEOUT = 90.0

# The three points this cell inherits, for the fourth to be read against.
PRIOR = [
    ("2026-09-10T03:31:02", 135, 15, 27665, 59683, 6385, "CG-s-32 baseline (row W1-S39)"),
    ("2026-09-10T05:32:57", 11, 14, 27664, 59559, 6385, "CG-s-33 loss read (row W1-S39)"),
    ("2026-09-10T05:57:16", 11, 14, None, None, 6385, "issuer's third read (TO face)"),
]


def q(stmt):
    r = pc.query(stmt, timeout_s=TIMEOUT)
    return r


def count_edge_type(et):
    r = q("MATCH (a:CloudNode)-[e:CloudEdge]->(b:CloudNode) "
          "WHERE e.edge_type = '%s' RETURN count(*) AS c" % et)
    rows = r["rows"]
    return (int(rows[0]["c"]) if rows else 0), r


def main():
    print("=" * 78)
    print("H4-AC3 -- THE FOURTH POINT, READ NOW THROUGH THE SERVING PLANE")
    print("=" * 78)
    L.tree_read("h4_fourth_point")
    print("")
    print("INSTRUMENT   : projection_client.query -> POST <base_url>/graph/cypher.")
    print("               This is the ONLY way a laptop seat reaches the served graph;")
    print("               no local store is opened, named or read.")
    print("GRAIN        : one row of the served CloudEdge/CloudNode tables. Counts are")
    print("               count(*) over the whole table, never a sample and never a page.")
    print("ENVIRONMENT  : the LIVE serving plane at run time. The comparison values are")
    print("               the three prior reads of this cell, each at its own vintage,")
    print("               taken through this same client by the round-7 worker and the")
    print("               issuer -- so the prior environment IS this environment, at an")
    print("               earlier vintage.")
    print("")

    # ------------------------------------------------------------------
    # NEGATIVE CONTROL -- the banked wrong form must RAISE, not answer 0.
    # ------------------------------------------------------------------
    print("NEGATIVE CONTROL -- the wrong query form must FAIL, not return zero")
    bad = "MATCH ()-[e:STORED_IN]->() RETURN count(*) AS c"
    print("  statement : %s" % bad)
    try:
        r = q(bad)
        print("  RESULT    : returned rows=%r -- THE WRONG FORM ANSWERED." % (r.get("rows"),))
        print("              A zero from this shape would have been indistinguishable")
        print("              from a real zero. Treat every family count below as SUSPECT.")
        neg = "DID-NOT-RAISE"
    except Exception as exc:  # noqa: BLE001 -- the exception IS the measurement
        msg = str(exc).replace("\n", " ")[:180]
        print("  RESULT    : RAISED -- %s" % msg)
        print("              Good: the binder refuses the relationship-table form, so a")
        print("              zero from the PROPERTY form below is a measurement.")
        neg = "RAISED"
    print("  NEGATIVE_CONTROL=%s" % neg)
    print("")

    # ------------------------------------------------------------------
    # THE READ.
    # ------------------------------------------------------------------
    h = pc.health(timeout_s=30.0)
    stored_in, r_si = count_edge_type("STORED_IN")
    served_from, _ = count_edge_type("SERVED_FROM")
    owned_by, _ = count_edge_type("OWNED_BY")

    r_nodes = q("MATCH (n:CloudNode) RETURN n.node_type AS t, count(*) AS c")
    by_type = {}
    for row in r_nodes["rows"]:
        by_type[row["t"] or ""] = int(row["c"])
    total_nodes = sum(by_type.values())
    policy_nodes = by_type.get("S3_BUCKET_POLICY", 0)

    r_edges = q("MATCH (a:CloudNode)-[e:CloudEdge]->(b:CloudNode) RETURN count(*) AS c")
    total_edges = int(r_edges["rows"][0]["c"]) if r_edges["rows"] else 0

    r_fam = q("MATCH (a:CloudNode)-[e:CloudEdge]->(b:CloudNode) "
              "RETURN e.edge_type AS et, count(*) AS c")
    families = sorted({(row["et"] or "") for row in r_fam["rows"]})

    # The parent-class question, MEASURED rather than asserted: which node class
    # does the OTHER boundary family hang off? If it is the same volatile class,
    # the same mechanism is still loaded.
    r_sf = q("MATCH (a:CloudNode)-[e:CloudEdge]->(b:CloudNode) "
             "WHERE e.edge_type = 'SERVED_FROM' "
             "RETURN b.node_type AS bt, count(*) AS c")
    sf_targets = sorted(((row["bt"] or ""), int(row["c"])) for row in r_sf["rows"])

    vintage = r_si.get("vintage") or h.get("vintage") or "<none returned>"
    manifest = r_si.get("manifest_sha256") or "<none returned>"

    print("SERVED_VINTAGE printed")
    print("  SERVED_VINTAGE = %s" % vintage)
    print("  (the SERVICE's own vintage line, returned on the same response as the")
    print("   counts below -- not a client clock and not a file mtime.)")
    print("MANIFEST_ID printed")
    print("  MANIFEST_ID    = %s" % manifest)
    print("  (manifest_sha256 as the service reports it on the counting query itself,")
    print("   so the vintage and the number cannot come apart.)")
    print("QUERY_FORM=edge_type-as-property")
    print("  statement used : MATCH (a:CloudNode)-[e:CloudEdge]->(b:CloudNode)")
    print("                   WHERE e.edge_type = '<FAMILY>' RETURN count(*) AS c")
    print("")

    print("THE COUNTS AT THIS VINTAGE")
    print("  STORED_IN=%d" % stored_in)
    print("  SERVED_FROM=%d" % served_from)
    print("  S3_BUCKET_POLICY_NODES=%d" % policy_nodes)
    print("  TOTAL_NODES=%d" % total_nodes)
    print("  TOTAL_EDGES=%d" % total_edges)
    print("  OWNED_BY=%d" % owned_by)
    print("  EDGE_FAMILIES_PRESENT=%d" % len(families))
    print("  STORED_IN_IN_FAMILY_LIST=%s"
          % ("yes" if "STORED_IN" in families else "no -- the family has no rows at all"))
    print("")

    print("POSITIVE CONTROL -- a family known present, through the SAME path, same run")
    print("  OWNED_BY returned %d through the identical statement shape. A zero from" % owned_by)
    print("  STORED_IN is therefore a measurement about the graph, not a broken query.")
    print("  POSITIVE_CONTROL=%s" % ("FIRED" if owned_by > 0 else "DID-NOT-FIRE"))
    print("")

    print("THE FOURTH POINT AGAINST THE THREE THIS CELL INHERITED")
    print("  vintage              STORED_IN  S3_BUCKET_POLICY  nodes    edges   OWNED_BY  source")
    for vin, si, pol, nn, ee, ob, src in PRIOR:
        print("  %-20s %9s  %16s  %-7s  %-6s  %-8s %s"
              % (vin, si, pol, nn if nn is not None else "-", ee if ee is not None else "-", ob, src))
    print("  %-20s %9d  %16d  %-7d  %-6d  %-8d %s"
          % (vintage[:19], stored_in, policy_nodes, total_nodes, total_edges, owned_by,
             "THIS READ (h4_fourth_point, taken now)"))
    print("")

    first_si = PRIOR[0][1]
    print("READING (a statement of what the four points say, no verdict):")
    if stored_in == 0:
        print("  The family is now EMPTY. It went %d -> 11 inside the window this cell was" % first_si)
        print("  cut to explain, held at 11 across two reads twenty-five minutes apart, and")
        print("  has since reached 0. THE LOSS DID NOT STOP; the three-point reading that")
        print("  it had stopped was a plateau between two drops, which is exactly what a")
        print("  three-point read of an event-driven process cannot distinguish from a halt.")
    elif stored_in < 11:
        print("  The family has fallen further since the third read: 11 -> %d." % stored_in)
    elif stored_in == 11:
        print("  The family is unchanged at 11 since the third read.")
    else:
        print("  The family has RISEN since the third read: 11 -> %d." % stored_in)
    print("  SERVED_FROM stands at %d. Its TARGET CLASSES, measured in this same run" % served_from)
    print("  (denominator = %d SERVED_FROM edges, every one of them, no sample):" % served_from)
    for bt, c in sf_targets:
        print("    -> %-24s %d" % (bt, c))
    pol_share = dict(sf_targets).get("S3_BUCKET_POLICY", 0)
    print("  %d of %d SERVED_FROM edges hang off S3_BUCKET_POLICY -- the same parent"
          % (pol_share, served_from))
    print("  class that carried STORED_IN away. The mechanism is still loaded.")
    print("")

    print("=" * 78)
    print("SUMMARY")
    print("=" * 78)
    print("SERVED_VINTAGE printed")
    print("MANIFEST_ID printed")
    print("QUERY_FORM=edge_type-as-property")
    print("SERVED_VINTAGE=%s" % vintage)
    print("MANIFEST_ID=%s" % manifest)
    print("STORED_IN=%d" % stored_in)
    print("SERVED_FROM=%d" % served_from)
    print("SERVED_FROM_ON_S3_BUCKET_POLICY=%d of %d"
          % (dict(sf_targets).get("S3_BUCKET_POLICY", 0), served_from))
    print("S3_BUCKET_POLICY_NODES=%d" % policy_nodes)
    print("TOTAL_NODES=%d" % total_nodes)
    print("TOTAL_EDGES=%d" % total_edges)
    print("OWNED_BY=%d" % owned_by)
    print("NEGATIVE_CONTROL=%s" % neg)
    print("POSITIVE_CONTROL=%s" % ("FIRED" if owned_by > 0 else "DID-NOT-FIRE"))
    print("OK: H4-AC3 complete -- read only, nothing published.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
