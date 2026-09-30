# AMGT_CORPUS round 23 -- never-widen pair for `CRPS-y-4`: the unit-map rebuild, the re-derive of 97 blocks under `--no-sa-fallback`, and the dossier refresh that consumes them

COO half below, signed by the issuer `2.0.0_SA_COO~X`. The CTO half is owed by `1.0.0_SA_CTO~Z` in its own lane
(`org/missions/D5/AMGT/AMGT_CORPUS/ledger/`). Rulings: round-22 analysis rulings 1-3 @`a940eb6813`.

**Code:** CLOUD HEAD >= `a3c4775d7c`, which carries:
- y-1, the unit families (`988d0ecfc7`);
- y-2, `--no-sa-fallback` (`e727eaf6aa`);
- y-3 and its hookup (`9d4d373916`, `a3c4775d7c`).

The run prints `git rev-parse HEAD` first. Evidence: `evidence/r23_y4_before.txt` (`checks/round23/y4_measure.py` plus the flip
classification).

**THE ORDER IS THE ACT (ruling 1).** One producer finishes before its consumer starts:
- (a) and (b) complete before (c);
- (c) completes before (d);
- each step's after-state read passes before the next begins.

One NEVER-2 entry, with legs a, b, c, d and v.

## THE ACTS
- **(a) The map rebuild:** `python integrations/bloomberg/research/build_unit_map.py --population crosswalk` on the committed
  `field_map.json`, run from the shared tree. It reads S3 raw only; no vendor call.
- **(b) The commit:** `field_map.json` alone.
- **(c) The re-derive of 97 blocks:** `python integrations/bloomberg/research/model_block_pull.py derive --no-sa-fallback
  --securities <the 97>`.
  - The 97 are the 100 newest served blocks minus BP/_LN, NG/_LN and NVDA_US (below). The list is in `y4_measure.py`'s
    `BLOCK` lines, and the run passes them in Bloomberg form.
  - Bronze reads only. No Bloomberg call, and no SA call (held off).
- **(d) The dossier refresh:** `write_one` over the 93 dossier names whose block stamp (c) moved (the dossier's 95 minus BP/NG).
  `write_one` writes only where `inputs` changed.

## WRITER CENSUS (N rules read at `a3c4775d7c`)
- `field_map.json` has 3 writers:
  - `build_unit_map.main` (a);
  - `apply_discriminated` (not run);
  - `_ensure_unit_map`, which runs only for a NEW name in a derive (none in (c): every one of the 97 is already in the map's
    securities once (a) adds NVDA).
- `derived/model_block/<key>/` has one writer, `stage_derive`, with its SA path held off by the flag.
- `research_dossier/` has one writer, `dossier.write_one`.

## BEFORE-STATE (measured ~08:0xZ; `evidence/r23_y4_before.txt`)
- Served, over the newest block of 100 keys: LABEL 21,694; UNRESOLVED 9,595; POINTER 6,457. 16,052 of 37,746 are not measured.
- Every block's `filled_by_sa` is 0, and 0 figures carry `source SA_FALLBACK`.
- 98 of 100 blocks were derived from their newest raw. The 2 that read otherwise are **BP/_LN_Equity and NG/_LN_Equity**, the
  slash key form of carried row `Z-S64`. This seat's newest-raw lookup lists `security_key=BP/_LN_Equity/`, which the `/`
  may split, so the reading may be the instrument, not stale raw. **An instrument this seat does not trust is not signed over a
  value move, so both are EXCLUDED** and carried to the `Z-S64` migration.

## EXPECTED OUTCOME, READ FROM THE PRODUCERS' OWN RULES
- **(a) The map diff** (the builder into a temp copy of the committed map):
  - `entries_changed 3012 fields_touched 66 shared_changed 0 securities_added 1 [NVDA US Equity] top_level_changed 0`.
  - The 8 entries applied in round 22 are MEASURED, so the builder skips them (`already_measured`); they stay unchanged.
- **(c) The re-derive, per figure, resolving each served figure through the rebuilt map:** 97 blocks, **15,425 unit changes, and
  nothing else moves** (the same raw on all 97, and no SA figure to remove).
  - **15,068 go from unmeasured to measured.**
  - **354 go from unmeasured to unmeasured.** Only the reason text changes, or a `SEE field_map ... not yet built` pointer
    becomes an explicit reason.
  - **3 go from measured to unmeasured:** `2317 TT Equity` BEST_SALES FY1-FY3, `MILLIONS` -> `UNRESOLVED-ON-2317 TT Equity:
    unmeasured`. 2317 never had its own measurement; it served the shared scalar by inheritance. The rebuild measures it,
    cannot discriminate it, and records an exception, which the round-19 reader honours. This is the ruled rule (never claim a
    measurement not made) applied to an entry it had never reached. **Named for the CTO half to accept or refuse.**
  - After (c), the not-measured figures on the 97 blocks number 602 (from about 15,670).
- **(d) The dossier refresh:** 93 puts. The expected diff per dossier is `model_rows` units only; other fields are unchanged.
  The pack_shape re-read after round 22 read `other_moves 0`. The deployed API reads `/5` dossiers only after AMGT_RESAPP's
  redeploy, so no page moves from (d) until then.

## AFTER-STATE THE VERIFY READS (leg v)
1. (b)'s element-wise diff against the pre-image: 3,012 entries across 66 fields, 0 shared, +NVDA, 0 top-level; the 8 round-22
   entries unchanged.
2. Every block of (c) against its predecessor, figure by figure: its per-block unit-change count equals the `BLOCK` line; 0
   value changes; 0 changes other than units; `filled_by_sa 0`.
3. The y1 census over the same 100 blocks: `no_family 0`, `crncy 0`; not-measured total at or below the expected figure (BP and
   NG excluded).
4. (d): `inputs_equal_now` True on the 93, and `w1_expected_moves.py` reads `other_moves 0`.

## BLAST RADIUS AND ROLLBACK
- **Touches:** one committed file; 97 new model-block stamps; 93 new dossier objects. No overwrite and no delete.
- **Readers:** the page and the export read the newest block stamp, so about 15,068 unit labels move from UNRESOLVED/pointer to
  measured, and 3 (2317 BEST_SALES) move the other way.
- **Rollback:**
  - revert the `field_map.json` commit and re-derive the 97 with the prior map (forward-only new stamps);
  - `write_one` then refreshes the dossiers;
  - the prior stamps stay in place.

## STOP LIMBS
1. (a)/(b)'s diff differs from the stated line: stop before (c), and revert.
2. Any block in (c) shows a value change, a non-unit change, a unit-change count other than its `BLOCK` line, or `filled_by_sa`
   > 0: stop, name the figures, revert (b), and re-derive the touched blocks.
3. (d) writes any name outside the 93, or `other_moves` > 0 outside `model_rows`: stop and name it.
4. Any `ERROR:` or a non-zero rc: stop.

**COO HALF: SIGNED** for (a), (b), (c) (97 blocks) and (d) (93 dossiers). BP/_LN and NG/_LN are EXCLUDED (`Z-S64`), and NVDA
has no flip. `2.0.0_SA_COO~X`, 2026-09-30, against `build_unit_map.main` / `classify_unit`, `model_block_pull.stage_derive`
(with `sa_fallback`) and `dossier.write_one` at `a3c4775d7c`. If any moves before the act, this half does not travel with it.
