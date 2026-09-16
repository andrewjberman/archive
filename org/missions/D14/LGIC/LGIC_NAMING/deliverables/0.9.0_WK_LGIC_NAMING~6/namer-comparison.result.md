# Result -- LGIC_NAMING.TO-LN-e-3-r3 (the namers' comparison, round 3)

**Worker:** `0.9.0_WK_LGIC_NAMING~6` · **Branch:** `wk-lgic-naming-3-6`, cut from `CLOUD` @61f64dee5e · **Cell:** `LN-e-3`

Round 2's result (`LGIC_NAMING.TO-LN-e-3-r2`) was at this path until this commit, and it is still at @ba8250b32a.
Row `LGIC_NAMING-S18` records that collision.

## Criteria

| id | invocation | deciding output | denominator | status |
|---|---|---|---|---|
| E3T-AC1 | `check_ln_r3.py e3-identical` | `VERDICT: PASS-IDENTICAL` | 18 of 18 items identical, 0 of 18 different | PASS |
| E3T-AC2 | `check_ln_r3.py e3-blind` | `VERDICT: PASS-NAMERS-UNCONFERRED` | 2 of 2 seat records: one prompt sha, 2 distinct sessions, 2 distinct folders | PASS |

## What the comparison found

- The two namers' answer files agree on all 18 items. The checker printed no `DIFFERS:` line, so no item needed a
  ruled-name line from the s.2 table of
  `org/tier1_exec/1.0.0_SA_CTO/deliverables/ROUND_ANALYSIS_LGIC_NAMING_ROUND1_20260914.md` @de52d3db04.
- Item i05 (`opal-data-cottonwood`, both namers) is marked as disclosed by row `LGIC_NAMING-S15`: the registry's
  `scopes.json` names the bucket.
- The full record is `org/missions/D14/LGIC/LGIC_NAMING/deliverables/exercises/r3/n3-compare.md`.

## Controls

- **Mutant.** Run in memory, with no tracked file edited. The AC1 mutant (B's i05 name altered) printed FAIL-DIFFERENT,
  17 of 18. The AC2 mutants (B given A's session and folder; B's prompt altered by one byte) each printed
  FAIL-NAMERS-NOT-SEPARATED. Each unmutated run printed PASS.
- **Determinism.** Two runs of each invocation were byte-identical (cmp rc=0).

## Order status

Both mechanical criteria pass by their output. The `complete` flip lands in the same commit as the proof instance,
after `proof-of-spec-check` returns rc 0.
