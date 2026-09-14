# Result -- LGIC_NAMING.TO-LN-e-3-r2 (the namers' comparison, round 2)

**Worker:** `0.9.0_WK_LGIC_NAMING~6` · **Branch:** `wk-lgic-naming-2-6`, cut from `CLOUD` @866f250fec · **Cell:** `LN-e-3`

## Criteria

| id | invocation | deciding output | denominator | status |
|---|---|---|---|---|
| E3R-AC1 | `check_ln_r2.py e3-identical` | `VERDICT: FAIL-DIFFERENT` | 15 of 18 identical, 3 of 18 different | FAIL |
| E3R-AC2 | `check_ln_r2.py e3-blind` | `VERDICT: PASS-NAMERS-UNCONFERRED` | 2 of 2 seat records: one prompt sha, 2 distinct sessions, 2 distinct folders | PASS |

## What the comparison found

- The namers differ on i03, i10 and i11. On all three, namer A (e1) wrote the ruled name from the s.2 table of
  `org/tier1_exec/1.0.0_SA_CTO/deliverables/ROUND_ANALYSIS_LGIC_NAMING_ROUND1_20260914.md` (table @de52d3db04, file
  @2706014705). Namer B (e2) wrote none of the three. Each of B's three names repeats the system token inside the
  function slot.
- The namers agree on i05 and i15, and both of those are disclosed by row `LGIC_NAMING-S15`: the briefing contains
  their ruled names.
- The full record is `org/missions/D14/LGIC/LGIC_NAMING/deliverables/exercises/r2/n3-compare.md`.

## Order status

The order stays `pending`. E3R-AC1 printed FAIL, and the order allows the `complete` flip only when every mechanical
criterion passes by its output. The order also says a difference is FWD-1's evidence, not a defect to fix, so the
FAIL is recorded as the round's measurement. It is not fixed and not re-run.

## Controls

- **Mutant.** Run in memory, with no tracked file edited. The AC1 positive control (B's file replaced by a copy of
  A's) printed PASS-IDENTICAL, 18 of 18. The AC2 mutant (B given A's session and folder) printed
  FAIL-NAMERS-NOT-SEPARATED.
- **Determinism.** Two runs of each invocation were byte-identical.
