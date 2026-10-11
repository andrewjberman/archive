"""AMGT_RESAPP round-92 PREP -- W372-S3: the block of a located period stops at another period's label.

  PYTHONPATH=<repo root> python r92_block_bound.py            (no network, no AWS: synthetic excerpts)

`_period_blocks` gives each LOCATED label a block from its own label to the NEXT LOCATED label (by text position) or the excerpt's end.
The last located period's block therefore runs to the excerpt's end, and a figure that the filing states for a DIFFERENT period (a year
the point set never names, so it is never located) verifies for it. Round 91's worker measured it on a synthetic excerpt; the real
excerpts hold only because a table label happens to bound the block.

    S1 point 2025 = 18.08 against "... 2025 ... In 2024 revenue was 18.08 billion": the figure is 2024's, the point is refused.
    S2 control: point 2025 = 21.05 against the same text (its own period's figure, stated before the other year) still verifies.
    S3 control: both periods as points, 2025 = 21.05 and 2024 = 18.08, both verify.
    S4 the bound is a different YEAR token, not distance: 2025 = 21.05 stated 4,000 characters after its label, with no other year token
       between, still verifies (a bound by distance would refuse it).
    S5 a figure after a different year token in a TABLE row is refused the same way: `2025` header line, then a row, then a line
       `2026`, then 77.5: the point 2025 = 77.5 is refused.
Verdict: R92 BLOCK BOUND: YES|NO (exit 0|1). At the base (2026-10-11) S1 and S5 FAIL, S2-S4 PASS.
"""
import sys

from lib.research.filings import analyze

PROSE = ("Results of operations for 2025 were driven by cloud revenue. Revenue was 21.05 billion for the year. "
         "In 2024 revenue was 18.08 billion, an increase of 16 percent.")


def say(ok, label, detail=""):
    print("%s %s%s" % ("PASS" if ok else "FAIL", label, ("  [" + detail + "]") if detail else ""))
    return ok


def run(text, points):
    kept, held = analyze._apply_point_verification([dict(p) for p in points], text, [], anchor=0)
    return {k["period"]: k for k in kept}, {h["period"]: h for h in held}


def main():
    results = []
    kept, held = run(PROSE, [{"period": "2025", "value": 18.08}])
    results.append(say("2025" not in kept and "2025" in held, "S1 a figure stated for a different year is refused for the last located period",
                       "kept %s" % sorted(kept)))
    kept, held = run(PROSE, [{"period": "2025", "value": 21.05}])
    results.append(say("2025" in kept, "S2 control: the period's own figure, stated before the other year, still verifies"))
    kept, held = run(PROSE, [{"period": "2025", "value": 21.05}, {"period": "2024", "value": 18.08}])
    results.append(say("2025" in kept and "2024" in kept, "S3 control: both periods as points both verify", "kept %s" % sorted(kept)))
    far = "Results for 2025 follow. " + ("Operating commentary continues without a date. " * 90) + "Revenue was 21.05 billion."
    kept, held = run(far, [{"period": "2025", "value": 21.05}])
    results.append(say("2025" in kept, "S4 the bound is a different year token, not distance", "text %d chars" % len(far)))
    table = "Year ended December 31,\n2025\nRevenue\n41.2\n2026\nRevenue\n77.5\n"
    kept, held = run(table, [{"period": "2025", "value": 77.5}])
    results.append(say("2025" not in kept and "2025" in held, "S5 a figure after a different year token in a table row is refused",
                       "kept %s" % sorted(kept)))
    print("   arms passed %d of %d" % (sum(1 for r in results if r), len(results)))
    ok = all(results)
    print("R92 BLOCK BOUND: %s" % ("YES" if ok else "NO"))
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
