# judge-compare-r3 -- CN-j-11, the intersection-and-positive-control-first comparison, round 3

Issued to `0.9.0_WK_LGIC_CANON~2` (`LGIC_CANON.TO-CN-j-11-r3`). Inputs: `judge-f.tsv` (CN-j-8), `judge-g.tsv`
(CN-j-9), `judge-h.tsv` (CN-j-10 -- unbriefed), the tree `CN_TREE_R3.md` (23 planes), `infra/logic/02_DOCTRINE.md`.
Every number below is COUNTED from the three TSVs and the tree by re-running the recount, never typed from memory.

PLANE INTERSECTION F.G.H: 23 of 23
POSITIVE CONTROL F.F: 23 of 23

ROLL-UP AGREE F.G.H: 22 of 23
ROLL-UP AGREE F.G: 22 of 23
ROLL-UP AGREE F.H: 22 of 23
ROLL-UP AGREE G.H: 23 of 23

ROLL-UP DIVERGE: 1 of 23
DIVERGE `opal-data-bd/code/` F: UNDETERMINED/R13 ; G: VIOLATES/R1 ; H: VIOLATES/R1 -- infra/logic/02_DOCTRINE.md:171

UNION REACHED: 5 of 6: R3, R8, R14, R19, R21 (NOT REACHED: R15)

## Did the unbriefed arm diverge more than the briefed pair?

The numbers say no. Judge H (unbriefed) agrees with judge G (briefed) on all 23 of 23 planes
(`ROLL-UP AGREE G.H: 23 of 23`) and disagrees with judge F (briefed) on exactly the same single plane that
judge G also disagrees with F on (`ROLL-UP AGREE F.H: 22 of 23` equals `ROLL-UP AGREE F.G: 22 of 23`, and the
one `DIVERGE` line names the same plane for both pairs). So H's agreement with the briefed pair
(22 of 23 with F, 23 of 23 with G) is at least as high as the briefed pair's agreement with each other
(F.G: 22 of 23) on both counts -- H never diverges from a briefed judge MORE than the two briefed judges
diverge from each other. If the severity-order briefing given to F and G were driving extra agreement
between them against an unbriefed H, the signature would be H as the outlier on more planes than F.G
disagree between themselves; that is not what the counts show. F is the odd one out here, not H.

What the numbers do NOT show: they do not show the arms could not have diverged on this tree, and they do not
show the briefing had no effect anywhere -- the intersection is a single tree of 23 planes with one point of
live disagreement, so a severity-order effect that only bites on rarer plane shapes (for instance a close call
between `CONFORMS` and `DECLARED-EXCEPTION`, or between `DEPARTS-RECOMMENDED` and `UNDETERMINED`) would not
necessarily surface here even if it exists in general. The one divergence present reads as a disagreement about
which RULE COORDINATE reaches the plane (does R1's legacy-code-home non-application carve out the bucket's
own firm-form name, or only the internal `code/` key structure -- `infra/logic/02_DOCTRINE.md:171,223`)
rather than a disagreement about where a verdict sits in the severity ORDER itself: F reads `UNDETERMINED`
(worst axis unmeasured, A4 compute) with the naming axis itself scored `DECLARED-EXCEPTION`, while G and H
both score the naming axis `VIOLATES`; the underlying claim in dispute is rule REACH, not rank order. So on
THIS tree, the arms did diverge exactly once, and the pattern is consistent with F reading the R1 non-application
too broadly rather than with H (unbriefed) reading severity looser than the briefed pair.
