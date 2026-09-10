#!/usr/bin/env python3
"""I3-AC2 -- the fold's licence stops being a COMMENT.

WHAT THE LICENCE IS. `derive_stitch.build_stitched_graph` deletes prior-cycle edges BY
TYPE. A type-shaped delete is safe only for a type nothing else in the estate writes.
Until CG-s-42 that condition lived in a prose comment: "STORED_IN is this producer's OWN
edge type (nothing else in the estate writes one)". A reader had to BELIEVE it, and a
future edit could add a type without ever testing the property the delete rests on --
which is precisely how ruling 94872's re-point onto OWNED_BY got authorized and then had
to be withdrawn.

FOUR ARMS.
  1. BEFORE -- the producer at the pre-remedy pin, resolved BY CONTENT with a positive
     control on the retrieval. Shows the licence was prose and the drop was a bare
     literal comparison.
  2. AFTER  -- the producer's OWN module loaded and its OWN function called. Shows the
     condition is now DATA and that an unlicensed type is REFUSED at runtime, not by
     convention.
  3. TESTABLE -- the falsifier RUN, not promised. `sole_written_holds` is executed on the
     registry's member (must hold) AND on a term known to have several writers (must NOT
     hold). A detector that cannot return False on the positive case is a constant wearing
     a measurement's clothes; this one returns both values in the same run.
  4. EVIDENCE -- the registry's own evidence table plus the live producer-plane census,
     each row carrying its claim kind.

BOUND. Arm 3 is a REPOSITORY sweep with the denominator it prints. It cannot see a writer
that exists only as deployed bytes, and it is a fact about TODAY: a new producer falsifies
a registry member without touching derive_stitch.py. That is why the check is re-runnable
rather than a one-time sign-off, and the bound is stated here rather than narrowed away.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import i3_fixture as F  # noqa: E402

CENSUS_CAPTURE = HERE / "i3_producer_payload_census.json"


def main() -> int:
    t = F.tree_facts()
    print("I3-AC2 -- THE FOLD'S LICENCE, MOVED OFF A COMMENT")
    print("  TREE        : %s (%s)" % (t["worktree"], t["tree_kind"]))
    print("  BRANCH/HEAD : %s @ %s" % (t["branch"], t["head"]))
    print("  BASELINE    : %s, resolved BY CONTENT (marker %s absent there, present here)"
          % (t["baseline_pin"], F.REMEDY_MARKER))
    print("  ENVIRONMENT : local worktree; the producer module is EXECUTED but no arm calls")
    print("                load_aws_layer, the only S3 reader in it. No network call.")
    print("  GRAIN       : the producer's own bytes and its own function -- not a transcript")
    print("                of them, and not the served graph.")
    print("")

    # ---- ARM 1: BEFORE -------------------------------------------------------------------
    base = F.baseline_source()
    cur = F.current_source()
    base_marker = base.count(F.REMEDY_MARKER)
    cur_marker = cur.count(F.REMEDY_MARKER)
    base_literal = base.count('edges = [e for e in edges if str(e.get("edge_type", "")) '
                              '!= "STORED_IN"]')
    print("  ARM 1 -- BEFORE (the pin's bytes, %d chars, retrieval control PASSED)" % len(base))
    print("    occurrences of %s in the baseline : %d  (0 == the condition was NOT data)"
          % (F.REMEDY_MARKER, base_marker))
    print("    the drop, as it stood -- one bare literal comparison, count=%d:" % base_literal)
    for ln in base.splitlines():
        if 'e.get("edge_type", "")) != "STORED_IN"' in ln or \
           "nothing else in the estate writes" in ln:
            print("      | %s" % ln.rstrip())
    print("    The licence was the COMMENT above that line and nothing else: no value, no")
    print("    predicate, no field a consumer could reject on.")
    print("")

    # ---- ARM 2: AFTER --------------------------------------------------------------------
    mod = F.load_producer(cur, "i3_producer_current")
    print("  ARM 2 -- AFTER (the worktree producer LOADED; its own function called)")
    print("    occurrences of %s in the worktree producer: %d" % (F.REMEDY_MARKER, cur_marker))
    print("    SOLE_WRITTEN_EDGE_TYPES  = %s" % sorted(mod.SOLE_WRITTEN_EDGE_TYPES))
    print("    PRIOR_CYCLE_DROP_REQUEST = %s" % (mod.PRIOR_CYCLE_DROP_REQUEST,))
    snap = F.prior_cycle_snapshot()
    kept_l, dropped_l, refused_l = mod.drop_prior_cycle_edges(snap, (F.SOLE,))
    kept_u, dropped_u, refused_u = mod.drop_prior_cycle_edges(snap, (F.MULTI,))
    print("    licensed request (%s)   -> dropped=%s refused=%s"
          % (F.SOLE, dropped_l, refused_l))
    print("    UNLICENSED request (%s) -> dropped=%s refused=%s  <-- the refusal is the check"
          % (F.MULTI, dropped_u, refused_u))
    checked = (dropped_l.get(F.SOLE, 0) == 2 and not refused_l
               and not dropped_u and refused_u.get(F.MULTI, 0) == 2
               and F.count(kept_u, F.MULTI) == 2 and F.count(kept_l, F.MULTI) == 2)
    print("    A CALLER CANNOT TALK THE FOLD INTO AN UNLICENSED DELETE: the request and the")
    print("    licence are separate tables and only their INTERSECTION is dropped.")
    print("")

    # ---- ARM 3: TESTABLE -----------------------------------------------------------------
    print("  ARM 3 -- THE FALSIFIER, RUN (not declared)")
    holds_pos, prod_pos, exc_pos, denom = F.sole_written_holds(F.SOLE)
    holds_neg, prod_neg, exc_neg, _ = F.sole_written_holds(F.MULTI)
    print("    DENOMINATOR: %d tracked file(s); %d READ; %d EXCLUDED above the size cap"
          % (denom["tracked"], denom["read"], denom["skipped_over_cap"]))
    print("    SUBTRACTION, not recall: every emission-shaped hit is either a PRODUCER or a")
    print("    NAMED exclusion, and both lists print in full.")
    print("    positive case  %s: sole_written=%s, producer emitter(s):" % (F.SOLE, holds_pos))
    for f, c in sorted(prod_pos.items()):
        print("        %-70s %s" % (f, c))
    print("      excluded (named, not forgotten): %d" % len(exc_pos))
    for f, c in sorted(exc_pos.items()):
        print("        excluded: %-60s %s" % (f, c))
    print("    NEGATIVE CONTROL %s: sole_written=%s, producer emitter(s):"
          % (F.MULTI, holds_neg))
    for f, c in sorted(prod_neg.items()):
        print("        %-70s %s" % (f, c))
    print("      excluded (named): %d" % len(exc_neg))
    testable = holds_pos and not holds_neg
    print("    THE CHECK RETURNS BOTH VALUES IN ONE RUN -> it can fail, so its pass means")
    print("    something. registry member holds=%s ; multi-writer term holds=%s"
          % (holds_pos, holds_neg))
    print("")

    # ---- ARM 4: EVIDENCE -----------------------------------------------------------------
    print("  ARM 4 -- EVIDENCE, each row carrying its claim kind")
    print("    SOLE_WRITERSHIP_EVIDENCE (shipped beside the registry in the producer):")
    print(json.dumps(mod.SOLE_WRITERSHIP_EVIDENCE, indent=6))
    cap = json.loads(CENSUS_CAPTURE.read_text(encoding="utf-8"))
    print("    LIVE PRODUCER PLANE (claim=%s, %d of %d payload(s) under producers/):"
          % (cap["claim"], cap["totals"]["payloads"], len(cap["payloads"])))
    for row in cap["payloads"]:
        print("      %-42s producer=%-34s STORED_IN=%-4d OWNED_BY=%d"
              % (row["local_basename"], row["producer"], row["STORED_IN"], row["OWNED_BY"]))
    print("      TOTALS STORED_IN=%d OWNED_BY=%d -- the registry admits STORED_IN and refuses"
          % (cap["totals"]["STORED_IN"], cap["totals"]["OWNED_BY"]))
    print("      OWNED_BY on exactly this evidence.")
    print("    claim kinds: `measured` = an instrument returned it in this run or in the named")
    print("    capture; `inferred` = it follows from something else; `held` = reasoned to.")
    print("    HELD, NOT MEASURED: that a conditional licence is the better branch than")
    print("    re-cutting the remedy. This run does not prefer one; see i3_branch.sh.")
    print("")

    print("=" * 78)
    print("LICENCE_WAS=COMMENT")
    print("  grounded: %s in the baseline = %d occurrence(s); the drop was one literal"
          % (F.REMEDY_MARKER, base_marker))
    print("  comparison against a string, licensed by the prose above it.")
    print("LICENCE_NOW=%s" % ("CHECKED" if checked else "UNCHANGED-REMEDY-RECUT"))
    print("  grounded: SOLE_WRITTEN_EDGE_TYPES is a frozenset the drop consults, an")
    print("  unlicensed type is REFUSED and COUNTED at runtime, and the refusal prints a")
    print("  WARN line rather than passing silently.")
    print("SOLE_WRITERSHIP_TESTABLE=%s" % ("true" if testable else "false"))
    print("  grounded: F.sole_written_holds ran on both a sole-written and a multi-written")
    print("  term this run and disagreed about them, over a printed denominator.")
    print("EVIDENCE printed")
    ok = checked and testable and base_marker == 0 and cur_marker > 0
    print("")
    print("SELF_CHECK=%s" % ("OK" if ok else "REVIEW"))
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
