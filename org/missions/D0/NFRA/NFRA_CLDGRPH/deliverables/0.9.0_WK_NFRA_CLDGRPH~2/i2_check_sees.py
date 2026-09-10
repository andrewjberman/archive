#!/usr/bin/env python3
"""I2-AC3 -- the remedy named, and the same fixture BLIND BEFORE / SEEING AFTER.

Two arms over ONE fixture:
  BEFORE : the producer bytes at the pinned pre-remedy commit (git show), loaded as a module.
  AFTER  : the producer file in THIS worktree, loaded the same way.
Both arms run the producer's OWN build_stitched_graph() and read its OWN
meta['genuine_dangling']. The only difference between the arms is the producer's bytes.

An OVER-FIRE control runs in both arms: the edge onto a node this cycle DID re-emit must
stay resolvable. A remedy that makes everything dangle would pass a naive before/after.
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import i2_fixture as F                                            # noqa: E402

REMEDY = "AWS_KEYS_MOVED"


def arm(mod, label):
    r = F.run_producer(mod, with_phantom_edge=False)
    hit = [e for e in r["dangling_sample"]
           if F.RETIRED in (e["source"], e["target"])]
    over = [e for e in r["dangling_sample"]
            if F.KEPT in (e["source"], e["target"])]
    print("  %s: genuine_dangling=%d of %d edges | dropped_ids=%s |"
          " node-absent/edge-present=%d | window edge SEEN=%s | OVER-FIRE control"
          " (edge onto the re-emitted node flagged)=%s"
          % (label, r["genuine_dangling"], r["total_edges"], r["dropped_ids"],
             len(r["node_absent_edge_present"]), bool(hit), bool(over)))
    for e in r["dangling_sample"]:
        print("      DANGLING: %s -[%s]-> %s" % (e["source"], e["edge_type"], e["target"]))
    return r, bool(hit), bool(over)


def main() -> int:
    tf = F.tree_facts()
    print("I2-AC3 -- THE REMEDY, AND THE CHECK THAT NOW SEES")
    print("  TREE          : %s (branch %s, HEAD %s)" % (tf["worktree"], tf["branch"], tf["head"]))
    print("  ENVIRONMENT   : BEFORE = producer bytes at %s (git show); AFTER = the producer"
          " file in this worktree. No S3, no network, no producer run against the live"
          " snapshot." % tf["baseline_pin"])
    print("  GRAIN         : the producer's OWN check in BOTH arms; only its bytes differ")
    print("  COVERAGE      : the SAME one fixture in both arms (1 dropped stitch node,"
          " 1 archived edge onto it, 1 archived edge onto a re-emitted node)")
    print("")
    print("REMEDY=%s" % REMEDY)
    print("WHY printed:")
    print("  1. THE EVIDENCE FROM I2-AC2. The only live read of the key set is the dangling")
    print("     filter itself, the bind at :144 is DEAD, and the only consumer of _index_aws")
    print("     outside this producer is a capture harness that calls it directly")
    print("     (g2_local_fold.sh:163) -- so moving the CHECK'S key set touches no second")
    print("     consumer, while _index_aws itself is left untouched.")
    print("  2. THE EDGE-SIDE DROP CANNOT BE MADE SAFE FROM THIS SOURCE. STORED_IN is")
    print("     droppable by its literal type because nothing else in the estate writes one")
    print("     (derive_stitch.py:155-157). The other stitch edge types -- WRITES, READS,")
    print("     ROUTES_TO, DERIVES_FROM -- collide with the AWS layer's own ARN-keyed")
    print("     READS/WRITES/ASSUMES edges carried in unchanged (module docstring :20-21),")
    print("     so a type-shaped drop would delete estate this order never touched. The")
    print("     archived edges carry no discriminator this producer can trust, and measuring")
    print("     whether one exists needs a producer run the egress hold forbids.")
    print("  3. THE CHECK IS THE GENERAL CONTROL; THE DROP IS A POINT FIX. Dropping the edge")
    print("     closes THIS window and leaves the check still answering a question about the")
    print("     moment before the collapse -- the next shrinking emission would be invisible")
    print("     again. Moving the key set makes the producer SAY the number instead of")
    print("     hiding it, which is also the only way the unmeasured magnitude ever gets")
    print("     measured: the first real run prints it.")
    print("  4. THE COST, STATED. main() returns 1 when genuine_dangling != 0, so the first")
    print("     nightly run after this lands can go ERROR where it used to print OK. That is")
    print("     the finding surfacing, not a regression -- but it is a CONSEQUENCE, not a")
    print("     side effect, and it is named here rather than discovered at 02:00Z.")
    print("")

    before_src = F.baseline_source()
    after_src = F.current_source()
    b_marker = F.REMEDY_MARKER in before_src
    a_marker = F.REMEDY_MARKER in after_src
    b_union = "| aws_keys" in before_src
    a_union = "| aws_keys" in after_src
    print("  BYTES BY CONTENT (never by ancestry): BEFORE has '%s'=%s and '| aws_keys'=%s;"
          " AFTER has '%s'=%s and '| aws_keys'=%s"
          % (F.REMEDY_MARKER, b_marker, b_union, F.REMEDY_MARKER, a_marker, a_union))
    if b_marker or not a_marker:
        print("BLOCKED: the two arms are not distinguishable by content")
        return 1

    print("")
    bmod = F.load_producer(before_src, "i2_ds_before")
    rb, b_seen, b_over = arm(bmod, "BEFORE (pinned pre-remedy bytes)")
    amod = F.load_producer(after_src, "i2_ds_after")
    ra, a_seen, a_over = arm(amod, "AFTER  (this worktree's bytes)   ")

    blind_before = (rb["genuine_dangling"] == 0
                    and len(rb["node_absent_edge_present"]) >= 1)
    seeing_after = (ra["genuine_dangling"] >= 1 and a_seen and not a_over)
    print("")
    print("CHECK_SEES_WINDOW=%s" % str(bool(blind_before and seeing_after)).lower())
    print("BLIND_BEFORE=%s (genuine_dangling=%d while %d edge(s) named a dropped node)"
          % (str(blind_before).lower(), rb["genuine_dangling"],
             len(rb["node_absent_edge_present"])))
    print("SEEING_AFTER=%s (genuine_dangling=%d, and the flagged edge IS the window edge;"
          " the re-emitted node's edge stayed resolvable, so the remedy did not over-fire)"
          % (str(seeing_after).lower(), ra["genuine_dangling"]))
    print("MAGNITUDE_ON_LIVE_SNAPSHOT=UNMEASURED (not manufactured)")
    return 0 if (blind_before and seeing_after) else 1


if __name__ == "__main__":
    sys.exit(main())
