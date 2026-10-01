# AMGT_CORPUS round 24 -- never-widen pair for the `CRPS-z-1` served act: the unit-map rebuild with the z-1 families, the re-derive of the 28 moving blocks, and the dossier refresh that consumes them

COO half below, signed by the issuer `2.0.0_SA_COO~X`. The CTO half is owed by `1.0.0_SA_CTO~Z` in its own lane
(`org/missions/D5/AMGT/AMGT_CORPUS/ledger/`). Standing rulings: 1 (a producer act finishes before its consumer starts) and 3 (every
producer input listed, reachable code diffed against the commit that built the served predecessor, new map entries read through
the consumer).

**Code:** CLOUD HEAD >= `04b89561ce`, which carries:
- z-1, the families (`d342614233`);
- z-2, the anchor reason text (`92f1403d25`);
- z-4, the slash-safe path sites (`6d6d142812`).

The run prints `git rev-parse HEAD` first. Evidence:
- `r24_m1_measure.txt`: map and block unit moves;
- `checks/round24/m2_measure.py`: per-figure unit and sign moves through the producer's own readers, plus the sign transitions.

**THE ORDER IS THE ACT (ruling 1).** (a) and (b) complete before (c), and (c) completes before (d). Each after-state read passes
before the next step begins. One NEVER-2 entry, slug `amgt-corpus-r24-unit-closures`, legs a, b, c, d and v.

## THE ACTS
- **(a) The map rebuild:** `python integrations/bloomberg/research/build_unit_map.py --population crosswalk` on the committed
  `field_map.json`, run from the shared tree with `PYTHONPATH` at the repo root. It reads S3 raw only; no vendor call.
- **(b) The commit:** `field_map.json` alone.
- **(c) The re-derive of 28 blocks:** `python integrations/bloomberg/research/model_block_pull.py derive --no-sa-fallback
  --securities <3 per call>` (the derive caps 3 per call), in Bloomberg form, over the 28 `BLOCK` lines of `m2_measure.py`:
  - 2317 TT, 6861 JP, 8035 JP, 8306 JP, 8316 JP, 8766 JP, 939 HK, 9433 JP, ICICIBC IN, TSM US;
  - ADBE, AMD, BA, CDNS, CELH, IDXX, ISRG, MELI, MNST, NFLX, NOW, NU, QXO, SHOP CN, SNPS, SPOT, UBER, WDAY.
  - Bronze reads only. No Bloomberg call, and no SA call (held off).
- **(d) The dossier refresh:** `write_one` over the 27 of the 28 that have a dossier (6861 JP has none; `read_dossier` raises
  LookupError). `write_one` writes only where `inputs` changed.

## PRODUCER INPUTS AND THE CODE DIFF (ruling 3)
The served predecessor of every one of the 28 was built at or after `94301d5a9c` (09:26Z; legs c and s of round 23). The
reachable diff `94301d5a9c..04b89561ce`, excluding tests and the map, touches 6 files:

| file | change | effect on (c) |
|---|---|---|
| `build_unit_map.py` | z-1's families F1-F6 | the map entries of (a), and nothing at derive time except `_ensure_unit_map`, which runs for a NEW name only (none of the 28) |
| `unit_anchor.py` | z-2's no-anchor reason text | the text of 12 UNRESOLVED reasons (939 HK 10, 6861 JP 1, TSM 1), through (a) |
| `model_block_pull.py` | z-4: `stage_derive` / `cmd_derive` path via `slash_safe_key`; `_model_block_keys_in_store` decodes | none on these 28; `slash_safe_key` is the identity on a slash-free key, so the object key is byte-identical |
| `pull_consumer.py`, `derive_fye_fixed.py` | z-4 path sites | not run by (c) |
| `crosswalk.py` | a marker comment | none |

The other producer inputs are unchanged since the predecessor:
- `case_rule` / `_compute_cases`: no diff; it reads the FY1 `BEST_EPS` value, never a unit.
- The per-figure sign reader `_resolved_sign`: no diff.
- `_scalar_exception`: no diff.
- Raw: `same_raw True` on all 28.

## WRITER CENSUS (3 properties, 5 writers, read at `04b89561ce`)
- `field_map.json`: `build_unit_map.main` (a); `apply_discriminated` (not run); `_ensure_unit_map` (a new name in a derive; none).
- `derived/model_block/<key>/`: `stage_derive` alone, with its SA path held off by the flag.
- `research_dossier/`: `dossier.write_one` alone.
- No working-tree scheduled task runs these producers: `amgt-induction-daily` runs a pinned copy, and `OPAL_BBGTML_daily_pull` runs
  tplus1.

## EXPECTED OUTCOME, READ FROM THE PRODUCERS' OWN RULES
- **(a) The map diff** (the builder into a temp copy): 84 entries across 10 fields (`BEST_BPS BEST_DIV_YLD BEST_DPS BEST_SALES
  BS_CASH_NEAR_CASH_ITEM BS_TOTAL_LIABILITIES CURR_ENTP_VAL EQY_DPS IS_DIV_PER_SHR SALES_REV_TURN`); 0 shared, 0 top-level, 0
  securities added.
- **(c) Per figure, each served figure resolved through the rebuilt map by the producer's own readers:** 28 blocks.
  - **565 unit changes:**
    - 553 go from unmeasured to measured, equal to z-1's projection;
    - 12 go from UNRESOLVED to UNRESOLVED (reason text: 939 HK 10, 6861 JP 1, TSM 1);
    - **0 go from measured to anything else.**
  - **115 sign changes, on the 11 non-US blocks only:**
    - 103 go from UNRESOLVED to POSITIVE, and 0 contradict their own value;
    - 12 go from UNRESOLVED to UNRESOLVED (reason text).
    - A sign on these names was forced UNRESOLVED while its unit was; it now resolves per figure (y-5's reader).
  - **0 value changes, and 0 case-text changes** (no case input moved).
  - Not-measured figures on the 98 non-excluded blocks go from 602 to 49.
- **(d) The dossier refresh:** 27 puts. The expected diff per dossier is units and signs in `model_rows` and the block stamp in
  `inputs`; other fields are unchanged.

## AFTER-STATE THE VERIFY READS (leg v)
1. (b)'s element-wise diff against the pre-image: 84 entries across the 10 fields named; 0 shared; 0 top-level.
2. Every block of (c) against its predecessor, figure by figure:
   - its per-block unit and sign counts equal its `m2` line;
   - 0 value changes, 0 case changes, and `filled_by_sa 0`;
   - `new_sign_contradicts_value 0`.
3. The z1 census over the same blocks reads `remaining 49`.
4. (d): 27 writes, `inputs_equal_now` True on the 27, and `other_moves 0` outside `model_rows`.
5. **The served read:** the deployed `opal-amgt-scoped-api` `/thesis` for 8306 JP serves one figure that moved to measured in
   (c), named from leg c's figure diff, with the new stamp's label; no older stamp of 8306 carries that label.

## BLAST RADIUS AND ROLLBACK
- **Touches:** one committed file; 28 new model-block stamps; 27 new dossier objects. No overwrite and no delete.
- **Readers:** the page and the export read the newest block stamp. 553 unit labels move from UNRESOLVED to measured, 103 sign
  labels move from UNRESOLVED to POSITIVE, and 24 labels change reason text only. **None moves from measured to another value.**
- **Rollback:**
  - revert the `field_map.json` commit and re-derive the 28 with the prior map (forward-only new stamps);
  - `write_one` then refreshes the 27;
  - the prior stamps stay in place.

## STOP LIMBS
1. (a)/(b)'s diff differs from the stated line: stop before (c), and revert.
2. Any block in (c) shows any of the following: stop, name the figures, revert (b), and re-derive the touched blocks.
   - a value change or a case change;
   - a unit or sign count other than its `m2` line;
   - a measured-to-other unit;
   - a sign contradicting its value;
   - `filled_by_sa` > 0.
3. (d) writes any name outside the 27, or `other_moves` > 0 outside `model_rows`: stop and name it.
4. Any `ERROR:` or a non-zero rc: stop.

**COO HALF: SIGNED** for (a), (b), (c) (28 blocks) and (d) (27 dossiers). BP/_LN and NG/_LN are EXCLUDED (`Z-S64`, and their
objects move only in round 25). `2.0.0_SA_COO~X`, 2026-09-30, against `build_unit_map.main` / `build_entries` /
`unit_from_basis_zero`, `model_block_pull.stage_derive` (with `sa_fallback`), `_resolved_unit` / `_resolved_sign`, and
`dossier.write_one`, all at `04b89561ce`. If any of these moves before the act, this half does not travel with it.
