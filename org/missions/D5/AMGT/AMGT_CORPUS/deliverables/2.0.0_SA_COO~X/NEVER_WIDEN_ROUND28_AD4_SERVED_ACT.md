# AMGT_CORPUS round 28 -- never-widen pair for `CRPS-ad-4`: ONE re-derive of the 18 blocks the zero-sample sign fix (ad-2) moves, and their dossiers

COO half below, signed by the issuer `2.0.0_SA_COO~X`. The CTO half is owed by `1.0.0_SA_CTO~Z`. Round-27 analysis @`99b83b495a` s.3
item 2 ("this changes served blocks, so it carries CTO + COO never-widen halves with a serializing dry run over every key"); round-26
ruling 2 (commit each NEVER-2 sentinel after every leg close).

**Code:** CLOUD HEAD >= `c03b6cc378` (the ad-2 drain: `_resolved_sign` signs a figure by its own value when the map's sign is
UNRESOLVED only on `build_unit_map.ZERO_SAMPLE_REASON`; d7b3ac6f01). The run prints `git rev-parse HEAD` first.
`PYTHONPATH=<root>;<root>/integrations/bloomberg/research` on every leg.

**THE ORDER IS THE ACT.** gate -> (c) -> (d) -> (v), each after-read passing before the next step. There is no map leg: ad-2 moves
no map entry (dry run `map_entries 0`). One NEVER-2 entry, slug `amgt-corpus-r28-ad4`; the sentinel is committed after every leg close.

## THE SERIALIZING DRY RUN OVER EVERY KEY (`checks/round28/ad4_dryrun.py`, `evidence/r28_ad4_dryrun.txt`)
The committed builder rebuilt a TEMP map (0 entries changed); the producer's own `stage_derive` at `d45014a87e` ran against it with a
write-capturing client for **every one of 100 keys**:

`ad4 keys 100 move_blocks 18 map_entries 0 unit 0 sign 450 currency 0 value 0 case_blocks 0 top 0 other 0 errors 0 writes_per_block {1: 100}`

| transition | figures |
|---|---|
| `IS_DIV_PER_SHR` UNRESOLVED(zero sample) -> ZERO / POSITIVE | 165 / 12 |
| `EQY_DPS` UNRESOLVED(zero sample) -> ZERO / POSITIVE | 165 / 12 |
| `BEST_DPS` (forecast) UNRESOLVED(zero sample) -> ZERO / POSITIVE | 46 / 2 |
| `BEST_DIV_YLD` (forecast) UNRESOLVED(zero sample) -> ZERO / POSITIVE | 46 / 2 |

The 18 blocks: ADBE, AMD, BA, CDNS, CELH, IDXX, ISRG, MELI, MNST, NFLX, NOW, NU, QXO, SHOP CN, SNPS, SPOT, UBER, WDAY (`checks/round28/
ad4_keys.txt`). Each moves only signs (20 to 28 each); 0 value, 0 unit, 0 currency, 0 case, 0 top-level. The other 82 keys: nothing.

## PRODUCER INPUTS AND THE CODE DIFF
`767b4e8c50..c03b6cc378` (the last served act's map commit to the ad-2 drain) over `integrations/bloomberg/research/` and
`lib/research/`: 14 files changed (`evidence/r28_ad4_changed.txt`), most of them peers' (RESAPP's route files, HARVST's
`publication_gold.py`, `covered_universe.py`, `price/generation.py`, `price_axis_pull.py`). **The act's IMPORT CLOSURE** (aa-4
AMENDMENT 1; `checks/round28/ad4_closure.py` imports `model_block_pull`, `build_unit_map` and `dossier` and intersects the loaded
modules): `ad4_closure changed 14 in_closure 2`. The two are ad-2's `model_block_pull.py` and `build_unit_map.py` (the positive
control: the method finds the files the act is about). The dry run ran THIS code against every served block.

## THE DOSSIERS
A pre-act inputs read: `LEG-D-INPUTS names 18 inputs_equal_now 18` (`evidence/r28_ad4_pre_inputs.txt`). After (c), leg (d) runs
`write_one` over the 18 and writes only where the inputs changed. The count is read at leg d, never predicted. No other name is
written.

## SERVED REACH (named, not acted)
- `/thesis` computes `check_face` per request from the block's figures through the DEPLOYED `run_checks.unit_status_for` (unchanged;
  it refuses a sign containing UNRESOLVED). After (c) the 354 fiscal figures on those 18 names stop being refused: BA's DPS shows
  4.69, 5.97, 7.19, 8.22 and six 0.0 years. The values were already served; only the refusal lifts.
- The 96 forecast figures' signs reach the Model tab's E columns once `CRPS-ad-3` lands on portal DEV.
- Nothing in `lib/research/api` imports the producer, so this act does not ride AMGT_RESAPP's ag-1 redeploy (~08:30Z), and that
  redeploy does not change this act's reach.

## AFTER-STATE THE VERIFY READS (leg v)
1. Each of the 18 new blocks EQUALS its captured dry-run block, `vintage` stripped (captured again immediately before (c)); exactly 18
   new block objects in S3.
2. The dossiers: one new object per written name; changed keys within `fields.model_rows`, `inputs`, `content_sha256`, `as_of`;
   `inputs_equal_now` true on each.
3. The census over the newest block of 100 keys (`ad2_check.py`'s check-face bucket, served blocks): refused fiscal figures 364 -> 10,
   0 on the zero-sample reason. **Negative arms:** BBSE3 `CAPITAL_EXPEND` stays refused (10, unit not measured); a non-moving name's
   newest stamp (TSM) is unchanged.

## BLAST RADIUS AND ROLLBACK
- **Touches:** 18 new block stamps under `derived/model_block/<key>/`, and at most 18 new dossier objects. No overwrite, no delete, no
  map change.
- **Rollback:** revert `c03b6cc378`, then re-derive the 18 forward (the prior stamps stay).

## STOP LIMBS
1. (c) writes any block outside the 18, a block differs from its capture, or a value, unit or case moves: stop and name it.
2. (d) writes any name outside the 18: stop.
3. Any `ERROR:` or a non-zero rc: stop.

**COO HALF: SIGNED** for gate, (c) (18 blocks) and (d) (at most 18 dossiers). `2.0.0_SA_COO~X`, 2026-10-01, against
`model_block_pull.stage_derive` / `_resolved_sign` and `dossier.write_one` / `current_inputs`, at `d45014a87e` (which carries
`c03b6cc378`).
