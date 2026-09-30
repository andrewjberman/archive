# AMGT_CORPUS round 23 -- never-widen pair for the SIGN re-derive (VERDICT B), then y-4's held leg (d) and leg (v)

COO half below, signed by the issuer `2.0.0_SA_COO~X`. The CTO half is owed by `1.0.0_SA_CTO~Z` ("This seat signs it", msg
27053). **Bound: not landed by 12:00Z -> A (revert) executes.** Code: CLOUD HEAD at the y-5 merge (`94301d5a9c`), which carries
`_resolved_sign` per figure (CRPS-y-5, `87aa9505f7`) and AMENDMENT 2 (`bd28136864`). The run prints `git rev-parse HEAD` first.
Evidence: `evidence/r23_y6_before.txt` (`checks/round23/y6_measure.py`, run against the y-5 code).

**THE ORDER IS THE ACT (ruling 1).** (s) the sign re-derive, then its read passes, then y-4's (d), then (v). One NEVER-2 entry: the
open `amgt-corpus-r23-unit-families` entry gains leg (s) before (d). Its legs a, b and c are already landed and proven or held.

## THE ACT
- **(s)** `python integrations/bloomberg/research/model_block_pull.py derive --no-sa-fallback --securities <3 at a time>` over the
  **50** blocks the measurement names (`BLOCK` lines in `r23_y6_before.txt`). Bronze reads only: no Bloomberg call and no SA call.
  The derive cap is 3 per call.
- Then **y-4 (d)**: `write_one` over the 93 dossier names, as the round-23 y-4 pair states.
- Then **(v)**.

## WRITER CENSUS (at `94301d5a9c`)
- `derived/model_block/<key>/` has one writer, `stage_derive`.
- The sign label comes from `_resolved_sign` (per figure, y-5).
- The unit comes from `_resolved_unit` over the committed map (`67568b59c4`, unchanged).
- `cases.base.formula` comes from `case_rule.BASE_FORMULA`, the TRUE text, kept per condition 1. The current blocks already carry
  it, so it does not move again.
- `research_dossier/` has one writer, `dossier.write_one`.

## BEFORE-STATE (read against the newest served stamps, the y-4 (c) stamps of 08:37-08:41Z)
- `y6 blocks 97 move_blocks 50 sign_changes 1569 unit_changes 0 new_sign_contradicts_value 0 served_plain_disagree 1569`.
- The 1,569 are exactly the figures whose served sign contradicts their own value: 1,568 plain and 1 convention (y5 base).

## EXPECTED OUTCOME, READ FROM THE PRODUCER'S OWN RULE
- **(s):** 50 new stamps. Per block, the sign changes equal its `BLOCK` line; the total is **1,569**, every one to the label
  `classify_sign` gives the figure's own value.
- **0 unit changes, 0 value changes, 0 case-value or formula changes, `filled_by_sa 0`.** The only other per-figure change is
  the `vintage` derivation timestamp, which is bookkeeping and is re-stamped on every derive.
- The 47 blocks that do not move are not re-derived.
- **After (s):** `y5_signs.py` over the 97 reads `plain_disagree 0 convention_disagree 0`.
- **(d)** is as the y-4 pair states: 93 puts, and the diff is `model_rows` only (units and signs in the model rows).

## AFTER-STATE THE VERIFY READS (leg v)
1. The (s) blocks against their predecessors, figure by figure: sign changes = expected, 0 unit, 0 value and 0 non-bookkeeping
   changes, `filled_by_sa 0`.
2. `y5_signs.py`: `plain_disagree 0 convention_disagree 0`.
3. The y1 census: `no_family 0 crncy 0`.
4. (d): `inputs_equal_now` True on the 93, `other_moves 0` outside `model_rows`.
5. **CTO y-4 condition 6:** one served read, the model-block route for one of the moved names, shows the new unit AND the
   corrected sign on a figure that moved.

## BLAST RADIUS AND ROLLBACK
- **Touches:** 50 new model-block stamps, then 93 dossier objects (y-4 (d)). No overwrite and no delete.
- **Rollback:** revert `87aa9505f7`'s reader change and re-derive the 50. The sampled-sign behaviour returns; forward-only.

## STOP LIMBS
1. Any block in (s) shows a unit change, a value change, a sign change other than its `BLOCK` count, a case or formula change, or
   `filled_by_sa` > 0: stop, name the figures, and do not start (d).
2. After (s), `y5_signs.py` reads `plain_disagree` > 0: stop.
3. Any `ERROR:` or a non-zero rc outside the known 3-per-call cap refusal: stop.

**COO HALF: SIGNED** for (s) (50 blocks) and the sequencing of y-4 (d) and (v) after it. `2.0.0_SA_COO~X`, 2026-09-30, against
`model_block_pull.stage_derive` and `_resolved_sign` at `94301d5a9c`. If any moves before the act, this half does not travel with it.
