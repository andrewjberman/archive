#!/usr/bin/env python3
"""I2-AC1 -- the node-absent/edge-present window, DEMONSTRATED on the PRE-REMEDY producer.

WHAT THIS RUNS: the producer source at the pinned pre-remedy commit, loaded as a module and
driven through its OWN build_stitched_graph() over a fixture. The verdict number is the
producer's own meta["genuine_dangling"] -- not a re-implementation of its predicate.

WHY A PIN AND NOT THE WORKTREE FILE: this criterion is graded AFTER the remedy lands in the
same file. Read from the worktree it would grade the remedy, not the baseline. Pinning the
pre-remedy bytes keeps this arm a BASELINE at every later grading, and the pin is resolved
BY CONTENT below, with a control, rather than by any ancestry test.
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import i2_fixture as F                                            # noqa: E402

OUT = Path(__file__).resolve().parent / "i2_window.baseline.json"


def main() -> int:
    tf = F.tree_facts()
    print("I2-AC1 -- THE BLIND WINDOW, ON THE PRE-REMEDY PRODUCER")
    print("  TREE          : %s (branch %s, HEAD %s)" % (tf["worktree"], tf["branch"], tf["head"]))
    print("  ENVIRONMENT   : producer bytes pinned at %s via git show; no S3, no network, no"
          " producer run against the live snapshot" % tf["baseline_pin"])
    print("  GRAIN         : the producer's OWN build_stitched_graph() and its OWN"
          " meta['genuine_dangling']; only the 3 input loaders are replaced")
    print("  COVERAGE      : ONE synthetic fixture, 3 stitch/AWS nodes and 2-3 archived edges."
          " It certifies the SHAPE of the window, not its MAGNITUDE on the live snapshot.")

    src = F.baseline_source()
    # CONTENT control on the pin (the tree clause): pre-remedy bytes carry the union that
    # keeps a dropped id alive and do NOT carry this order's marker.
    has_union = "| aws_keys" in src
    has_marker = F.REMEDY_MARKER in src
    print("  PIN_BY_CONTENT: baseline_bytes=%d chars, contains '| aws_keys'=%s,"
          " contains '%s'=%s (expected True/False)"
          % (len(src), has_union, F.REMEDY_MARKER, has_marker))
    if not has_union or has_marker:
        print("BLOCKED: the pinned bytes are not the pre-remedy producer")
        return 1

    mod = F.load_producer(src, "i2_derive_stitch_baseline")

    # ---- arm A: the window itself, nothing else in the fixture -------------------------
    a = F.run_producer(mod, with_phantom_edge=False)
    dropped = a["dropped_ids"]
    naep = a["node_absent_edge_present"]
    window_built = (F.RETIRED in dropped
                    and a["collapsed"]["prior_cycle_not_reemitted"] >= 1
                    and len(naep) >= 1)
    print("")
    print("  ARM A (window): dropped_stitch_ids=%s of %d stitch ids in the snapshot"
          " | prior_cycle_not_reemitted=%d"
          % (dropped, 2, a["collapsed"]["prior_cycle_not_reemitted"]))
    for e in naep:
        print("    NODE-ABSENT/EDGE-PRESENT: %s -[%s]-> %s"
              % (e["source"], e["edge_type"], e["target"]))
    print("  ARM A producer verdict: genuine_dangling=%d of %d edges in the artifact"
          % (a["genuine_dangling"], a["total_edges"]))

    # ---- arm B: negative control -- an endpoint in NEITHER key set must be SEEN --------
    b = F.run_producer(mod, with_phantom_edge=True)
    control_hit = [e for e in b["dangling_sample"] if F.PHANTOM in (e["source"], e["target"])]
    print("  ARM B (control): one extra archived edge onto %s, an id in NEITHER the snapshot"
          " NOR this cycle's emission" % F.PHANTOM)
    print("  ARM B producer verdict: genuine_dangling=%d of %d edges -- the check is ALIVE"
          " on this fixture, so arm A's 0 is blindness and not a dead instrument"
          % (b["genuine_dangling"], b["total_edges"]))

    payload = {
        "criterion": "I2-AC1", "claim_kind": "measured",
        "tree": tf,
        "arm_a": {k: a[k] for k in ("genuine_dangling", "collapsed", "total_nodes",
                                    "total_edges", "dropped_ids",
                                    "node_absent_edge_present", "node_ids")},
        "arm_b": {"genuine_dangling": b["genuine_dangling"],
                  "dangling_sample": b["dangling_sample"],
                  "total_edges": b["total_edges"]},
        "denominator_note": "1 fixture; 2 archived stitch nodes; 2 (arm A) / 3 (arm B)"
                            " archived edges. MAGNITUDE ON THE LIVE SNAPSHOT: UNMEASURED"
                            " (a producer run is forbidden by the egress hold).",
    }
    OUT.write_text(F.jdump(payload) + "\n", encoding="utf-8")

    ok_clean = (a["genuine_dangling"] == 0)
    ok_control = (b["genuine_dangling"] >= 1 and len(control_hit) >= 1)
    print("")
    print("WINDOW_BUILT=%s" % str(window_built).lower())
    print("CHECK_SAYS_CLEAN_WHILE_BLIND=%s" % str(bool(ok_clean and window_built)).lower())
    print("  the producer printed the equivalent of 'OK: genuine (non-wildcard) dangling"
          " edges = 0' while %d edge(s) named a node it had just dropped" % len(naep))
    print("BASELINE_CAPTURED=%s (%s)" % (str(OUT.exists()).lower(), OUT.name))
    print("NODE_ABSENT_EDGE_PRESENT=%d of %d edges in the arm-A artifact" % (len(naep),
                                                                            a["total_edges"]))
    print("MAGNITUDE_ON_LIVE_SNAPSHOT=UNMEASURED (not manufactured; see row W1-S44)")
    print("NEGATIVE_CONTROL=%s" % ("FIRED" if ok_control else "DID-NOT-FIRE"))
    return 0 if (window_built and ok_clean and ok_control and OUT.exists()) else 1


if __name__ == "__main__":
    sys.exit(main())
