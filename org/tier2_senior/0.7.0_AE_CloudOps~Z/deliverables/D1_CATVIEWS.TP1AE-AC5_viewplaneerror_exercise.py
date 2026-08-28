"""TP1AE-AC5: exercise ViewPlaneError's five-peer refusal AGAINST A REAL MISMATCH.

D1_CATVIEWS.TO-P1-AE acceptance criterion 5:

    "The ViewPlaneError path EXERCISED at least once AGAINST A REAL MISMATCH and
     shown to refuse. Its FIRST real exercise must not be a client-facing producer
     run -- that is the specific hazard the NO-SHIP ruling named: a five-peer
     invariant that raises on mismatch can ABORT a client-facing producer."

WHAT THIS RUNS AGAINST, AND WHY IT IS NOT THE REPO COPY.
The subject is the DEPLOYED bytes. This script imports `mdpf_category_registry`
out of a directory extracted from the bundle downloaded from the live function
(`aws lambda get-function` -> Code.Location -> unzip), NOT from
data/mdpf/scripts/gold/. The repo copy and the deployed copy are different claims
(CLAUDE.md Rule 22a CODE layer), and only the second can abort the 13:30Z fire.

    usage:  python D1_CATVIEWS.TP1AE-AC5_viewplaneerror_exercise.py <extracted-bundle-dir>

FOUR ARMS, AND TWO OF THEM MUST *PASS*. A check that cannot pass is not a control:
if every arm refused, the exercise would be satisfied by a predicate that raises
unconditionally, which is a different defect wearing the same green tick. Arms A
and B are therefore load-bearing, not padding.

    A  exact match             -> PASSED            the predicate can pass at all
    B  1 cent, AT tolerance    -> PASSED            TOL_CENTS is real, not decorative
    C  2 cents, ONE OUTSIDE    -> REFUSED at :1079  the boundary discriminates to the cent
    D  material $1,000 break   -> REFUSED at :1079  a real break refuses

⛔ REFUSALS ARE CLASSIFIED BY SITE, NEVER BY EXCEPTION TYPE, AND THAT IS THE WHOLE
INSTRUMENT. `mdpf_category_registry` raises ViewPlaneError at FOUR distinct sites.
The first draft of this exercise set Insurance to a non-zero value and scored arms
C and D as passes -- they had refused at the INSURANCE-EXCLUSION site while the
five-peer predicate under test was never reached. Expected verdict, wrong
predicate, and `except ViewPlaneError` could not tell the difference. Insurance is
EXCLUDED FROM DISPLAY, so it must be 0.00 in the fixture for the five-peer site to
be reachable at all.

>> A TEST THAT ASSERTS ONLY THE EXCEPTION TYPE PASSES WHEN AN EARLIER GUARD FIRES
   FIRST, AND IT PASSES MOST CONVINCINGLY WHEN THE FIXTURE IS MOST BROKEN. <<

NOT A PRODUCER RUN. It writes nothing, reads no S3 key, and touches no served
artifact -- so it cannot disturb the time-of-day discriminator TP1AE-AC1 scores on
at the 2026-08-28 13:30Z scheduled fire.
"""
from __future__ import annotations

import sys

# Insurance is EXCLUDED FROM DISPLAY. A non-zero value here trips the
# insurance-exclusion refusal BEFORE the five-peer predicate is reached, and the
# exercise then measures a site it is not testing. See the docstring.
BASE_NODE_AUM = {
    "Models": 400.00,
    "SMA": 300.00,
    "Alternatives": 250.00,
    "Insurance": 0.00,
    "Client": 50.00,
}   # five peers sum to 1000.00


def classify(msg: str) -> str:
    """Which ViewPlaneError SITE refused. Type alone does not discriminate."""
    if "five-peer" in msg or "gold-plane peers sum to" in msg:
        return "FIVE-PEER(:1079)"
    if "Insurance carries" in msg:
        return "INSURANCE-EXCL"
    if "fee buckets sum to" in msg:
        return "CLIENT-C3(:1035)"
    return "OTHER-VIEWPLANE"


def main() -> int:
    if len(sys.argv) != 2:
        print(__doc__)
        return 2
    sys.path.insert(0, sys.argv[1])
    import mdpf_category_registry as R  # noqa: E402  (path set above, by design)

    tol_cents = round(R.RECON_TOLERANCE * 100)
    peers_sum = round(sum(BASE_NODE_AUM.values()), 2)
    print(f"subject     : {sys.argv[1]}")
    print(f"peers sum   : {peers_sum}   TOP_LEVEL_PEERS={R.TOP_LEVEL_PEERS}")
    print(f"TOL_CENTS   : {tol_cents}   SMA_BUCKETS={getattr(R, 'SMA_BUCKETS', 'ABSENT')}")
    print()

    def arm(tag: str, total_aua: float, expect: str) -> bool:
        try:
            R.build_category_views("cottonwood", "2026-08-27",
                                   dict(BASE_NODE_AUM), total_aua)
            site, detail = "PASSED", ""
        except R.ViewPlaneError as exc:
            site, detail = classify(str(exc)), str(exc).replace("\n", " ")[:118]
        except Exception as exc:                       # noqa: BLE001 -- any other
            site, detail = f"OTHER:{type(exc).__name__}", str(exc)[:118]
        ok = site == expect
        print(f"{'OK ' if ok else '*** MISMATCH ***'} {tag:32s} "
              f"total_aua={total_aua:<9} expect={expect:<17} got={site}")
        if detail:
            print(f"      {detail}")
        return ok

    arms = [
        arm("A exact match (NEG CONTROL)",  1000.00, "PASSED"),
        arm("B 1 cent = AT tolerance",      1000.01, "PASSED"),
        arm("C 2 cents = ONE UNIT OUTSIDE", 1000.02, "FIVE-PEER(:1079)"),
        arm("D material $1,000.00 break",   2000.00, "FIVE-PEER(:1079)"),
    ]
    print()
    print(f"ARMS {sum(arms)}/{len(arms)} as specified")
    return 0 if all(arms) else 1


if __name__ == "__main__":
    raise SystemExit(main())
