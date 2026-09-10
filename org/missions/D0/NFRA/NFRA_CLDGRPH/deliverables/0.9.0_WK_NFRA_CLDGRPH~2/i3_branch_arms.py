#!/usr/bin/env python3
"""I3-AC3 arms -- the branch TAKEN is MOVE THE LICENCE, and here is the proof.

THE BRANCH. The cell offered two: move the licence (make the drop conditional on
sole-writership) or re-cut the remedy (leave the licence alone). BOTH ARE PASSES. This
order took **LICENCE_MOVED**, and says so before it shows anything, because a run that
does not say which branch it took is the one thing that cannot pass.

WHY THIS BRANCH, STATED AS HELD AND NOT AS MEASURED. Re-cutting the remedy leaves the
unconditional delete in place for the NEXT type someone wants to retire; moving the
licence makes the property the delete rests on checkable for every type, including
STORED_IN itself, whose sole-writership is a fact about today rather than a property of
the term. That is a judgement, not a measurement, and the alternative branch remains open.

SIX ARMS, EACH A PASS/FAIL, RUN AGAINST THE PRODUCER'S OWN BYTES.
  1  the licensed type is still dropped -- behaviour for STORED_IN is unchanged
  2  a multi-writer type SURVIVES a request to drop it
  3  the refusal is COUNTED and printed, never silent
  4  a bystander type is untouched in both arms
  5  the SHIPPED request reproduces the baseline's kept-set EXACTLY (no regression):
     the baseline arm evals the pre-remedy expression LIFTED VERBATIM from the pin's bytes
  6  NEGATIVE CONTROL -- the withdrawn remedy, applied to the baseline expression, DOES
     delete the other producer's edges. Without arm 6, arm 2's survival is vacuous: a
     harness that cannot observe a deletion cannot certify its absence.

ENVIRONMENT: local worktree; the producer module is executed, `load_aws_layer` is never
called, and no arm touches AWS, an image, a task or a topic.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import i3_fixture as F  # noqa: E402

BASELINE_DROP_RE = re.compile(
    r'^\s*edges = \[e for e in edges if str\(e\.get\("edge_type", ""\)\) != "STORED_IN"\]\s*$',
    re.M)


def baseline_drop_expr(src: str) -> str:
    m = BASELINE_DROP_RE.search(src)
    if not m:
        raise RuntimeError("ERROR: baseline drop expression not found in the pin's bytes")
    return m.group(0).strip()


def run_expr(expr: str, edges: list) -> list:
    ns = {"edges": list(edges), "str": str}
    exec(compile(expr, "<baseline-bytes>", "exec"), ns)
    return ns["edges"]


def main() -> int:
    t = F.tree_facts()
    print("I3-AC3 -- THE BRANCH TAKEN, AND ITS PROOF")
    print("  TREE        : %s (%s)" % (t["worktree"], t["tree_kind"]))
    print("  BRANCH/HEAD : %s @ %s" % (t["branch"], t["head"]))
    print("  BASELINE    : %s -- the pre-remedy producer, resolved BY CONTENT" % t["baseline_pin"])
    print("  ENVIRONMENT : local worktree, fixture edges only; no S3, no task, no publish.")
    print("  GRAIN       : the producer's OWN drop function and the pin's OWN drop")
    print("                expression, both executed. Neither arm is a transcript.")
    print("  HARNESS     : 5 fixture edges -- 2 %s (this producer's), 2 %s (graphuni-storage's"
          % (F.SOLE, F.MULTI))
    print("                shape, copied from its payload), 1 %s bystander." % F.BYSTANDER)
    print("")

    base_src = F.baseline_source()
    cur_src = F.current_source()
    mod = F.load_producer(cur_src, "i3_producer_branch")
    expr = baseline_drop_expr(base_src)
    print("  THE PIN'S OWN DROP EXPRESSION, LIFTED VERBATIM:")
    print("    %s" % expr)
    print("")

    snap = F.prior_cycle_snapshot()
    n_sole, n_multi, n_by = (F.count(snap, F.SOLE), F.count(snap, F.MULTI),
                             F.count(snap, F.BYSTANDER))
    print("  FIXTURE IN : %s=%d %s=%d %s=%d (total %d edges)"
          % (F.SOLE, n_sole, F.MULTI, n_multi, F.BYSTANDER, n_by, len(snap)))

    kept_ship, dropped_ship, refused_ship = mod.drop_prior_cycle_edges(
        snap, mod.PRIOR_CYCLE_DROP_REQUEST)
    kept_ask, dropped_ask, refused_ask = mod.drop_prior_cycle_edges(snap, (F.MULTI,))
    kept_both, dropped_both, refused_both = mod.drop_prior_cycle_edges(
        snap, (F.SOLE, F.MULTI))
    kept_base = run_expr(expr, snap)
    kept_neg = run_expr(expr.replace('"STORED_IN"', '"OWNED_BY"'), snap)

    arms = []

    a1 = F.count(kept_ship, F.SOLE) == 0 and dropped_ship.get(F.SOLE) == n_sole
    arms.append(("1 licensed type still dropped",
                 a1, "%s kept=%d dropped=%s" % (F.SOLE, F.count(kept_ship, F.SOLE),
                                                dropped_ship)))

    a2 = F.count(kept_ask, F.MULTI) == n_multi and F.count(kept_both, F.MULTI) == n_multi
    arms.append(("2 multi-writer type SURVIVES a drop request",
                 a2, "%s kept=%d of %d when explicitly requested; kept=%d when requested"
                 " ALONGSIDE the licensed type"
                 % (F.MULTI, F.count(kept_ask, F.MULTI), n_multi,
                    F.count(kept_both, F.MULTI))))

    a3 = refused_ask.get(F.MULTI) == n_multi and refused_both.get(F.MULTI) == n_multi
    arms.append(("3 the refusal is COUNTED, not silent",
                 a3, "refused=%s / %s" % (refused_ask, refused_both)))

    a4 = all(F.count(k, F.BYSTANDER) == n_by
             for k in (kept_ship, kept_ask, kept_both, kept_base))
    arms.append(("4 bystander type untouched in every arm",
                 a4, "%s kept=%d in all four kept-sets" % (F.BYSTANDER, n_by)))

    a5 = [id(e) for e in kept_ship] == [id(e) for e in kept_base]
    arms.append(("5 shipped request == the pin's kept-set, element for element",
                 a5, "len(new)=%d len(baseline)=%d identical_objects=%s"
                 % (len(kept_ship), len(kept_base), a5)))

    neg_deleted = n_multi - F.count(kept_neg, F.MULTI)
    a6 = neg_deleted == n_multi and n_multi > 0
    arms.append(("6 NEGATIVE CONTROL: the withdrawn re-point DOES delete them",
                 a6, "re-pointing the pin's own expression onto %s deleted %d of %d"
                 % (F.MULTI, neg_deleted, n_multi)))

    print("")
    print("  ARMS:")
    for name, ok, detail in arms:
        print("    %-8s %s" % ("PASS" if ok else "FAIL", name))
        print("             %s" % detail)
    passed = sum(1 for _, ok, _ in arms if ok)

    print("")
    print("  WHAT ARM 6 MEANS. The CTO's withdrawal @2fa5bf1670 said a future cut 'changes")
    print("  the remedy or MOVES THE FOLD'S LICENCE FIRST, and may not assume the licence")
    print("  travels with the re-point.' Arm 6 is that assumption, executed: the pin's own")
    print("  expression re-pointed onto %s removes %d of %d of graphuni-storage's edges."
          % (F.MULTI, neg_deleted, n_multi))
    print("  Arm 2 is the same request through the moved licence, and nothing is removed.")
    print("")

    print("=" * 78)
    print("BRANCH=LICENCE_MOVED")
    print("  The drop is now conditional on the term being sole-written. The alternative")
    print("  branch (REMEDY_RECUT) is NOT taken and stays open; this face does not prefer")
    print("  one, and the preference above is labelled HELD.")
    print("MULTI_WRITER_TERM_SURVIVES=%s" % str(a2).lower())
    print("SOLE_WRITTEN_TERM_DROPPED=%s" % str(a1).lower())
    print("FIXTURE_ARMS=%d of %d" % (passed, len(arms)))
    print("NEGATIVE_CONTROL=%s" % ("FIRED" if a6 else "DID-NOT-FIRE"))
    print("")
    print("  DENOMINATOR: %d arms declared, %d executed, %d PASS. Every arm's deciding"
          % (len(arms), len(arms), passed))
    print("  number is printed beside it; none is a summary of another.")
    ok = passed == len(arms)
    print("SELF_CHECK=%s" % ("OK" if ok else "REVIEW"))
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
