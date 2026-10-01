# AMGT_CORPUS round 27 -- never-widen pair for `CRPS-ac-2`: the map rebuild carrying ac-1, and ONE re-derive of BBSE3's block

COO half below, signed by the issuer `2.0.0_SA_COO~X`. The CTO half is owed by `1.0.0_SA_CTO~Z`. Round-26 analysis @`3a758833b7`
s.4 item 2 and ruling 2 (commit each NEVER-2 sentinel after every leg close); row `Z-W1-S25` ruled ACCEPT @`b239301bb1`.

**Code:** CLOUD HEAD >= `b239301bb1`, which carries ac-1 `08a2388a1b` / `72beac7438` (merged `3a7cf75c4f`). The run prints
`git rev-parse HEAD` first. `PYTHONPATH=<root>;<root>/integrations/bloomberg/research` on every leg (y-4 condition 1).

**THE ORDER IS THE ACT.** gate -> (a) -> (b) -> (c) -> (d) -> (v), each after-read passing before the next step. One NEVER-2 entry,
slug `amgt-corpus-r27-ac2`; the sentinel is committed after every leg close.

## THE SERIALIZING DRY RUN OVER EVERY KEY (`checks/round27/ac2_dryrun.py`, `evidence/r27_ac2_dryrun.txt`)
The builder rebuilt a TEMP map; the producer's own `stage_derive` ran against it with a write-capturing client for **every one of 100
keys** (raw-slash copies excluded, encoded BP/NG included). Every changed map entry and every (from, to) transition is printed:

`ac2 keys 100 move_blocks 1 map_entries 1 unit 10 sign 10 currency 0 value 0 case_blocks 0 top 0 other 0 errors 0 writes_per_block {1: 100}`

| what | change | served effect |
|---|---|---|
| map entry BBSE3 `CAPITAL_EXPEND` | per-security detail: the UNRESOLVED reason -> the ZERO-DOMINATED class (6 of 10 fiscal years exactly 0) | 10 unit texts |
| block `BBSE3_BZ_Equity` | units 10 `UNRESOLVED` -> `ZERO-DOMINATED`; signs 10 `UNRESOLVED` -> `UNRESOLVED` (reason text only) | 0 value, 0 currency, 0 case, 0 top-level |
| the other 99 keys | nothing | nothing |

The dividend keys do not move: row `Z-W1-S25`'s exemption (ruled ACCEPT) keeps EQY_DPS / IS_DIV_PER_SHR / BEST_DPS / BEST_DIV_YLD /
EQY_DVD_YLD_IND out of the class.

## PRODUCER INPUTS AND THE CODE DIFF
`29d87a966a..HEAD` (the last map commit) over `integrations/bloomberg/research/` and `lib/research/`: `build_unit_map.py` (+49/-4,
ac-1) and its new test file. Nothing else in the act's import closure moved. The dry run ran THIS code against every served block.

## THE DOSSIER
A pre-act inputs read: `INPUTS BBSE3_BZ_Equity equal_now True`. After (c), leg (d) runs `write_one` for BBSE3 only and writes only if
its inputs changed. The count is read at leg d, never predicted. No other name is written.

## SERVED REACH (named, not acted)
- `/thesis` serves the block's figures. BBSE3 `CAPITAL_EXPEND` reaches the page with the unit text
  `ZERO-DOMINATED: no magnitude: 6 of 10 fiscal years are zero` in place of the UNRESOLVED reason. The value (0.0 and the rest) is
  byte-unchanged; the sign stays UNRESOLVED.
- `modelSheet.ts` reads no unit field. `scoped_amgt.py:1261` imports only the overlay functions from `render_print`.
- **Not moved by this act:** `provenance/validate.py:32` and `render_print.py:208` mark a unit unmeasured only on the prefix
  `SEE field_map.json`, so they read BOTH `UNRESOLVED-ON-...` and `ZERO-DOMINATED...` as MEASURED. Same class before and after; off the
  served path; filed as a row.
- The census: UNRESOLVED units over 100 keys 11 -> 1 (TSM `CURR_ENTP_VAL`), ZERO-DOMINATED 0 -> 10. Neither class is measured; the
  packet prints both counts with the key count beside them.

## AFTER-STATE THE VERIFY READS (leg v)
1. (a)'s rebuilt map is byte-identical to the dry run's temp map; the element-wise diff equals the 1 entry above.
2. BBSE3's new block EQUALS its captured dry-run block, `vintage` stripped (captured again immediately before (c)).
3. The dossier: at most one new object for BBSE3; `inputs_equal_now` true.
4. The census reads UNRESOLVED 1 and ZERO-DOMINATED 10 over 100 keys, bands unchanged. **The negative arm:** TSM `CURR_ENTP_VAL`
   stays UNRESOLVED, and a dividend key (BA `EQY_DPS`) keeps its unit byte-unchanged.

## BLAST RADIUS AND ROLLBACK
- **Touches:** `field_map.json` (one commit), 1 new block stamp under `derived/model_block/BBSE3_BZ_Equity/`, and at most 1 new
  BBSE3 dossier object. No overwrite, no delete.
- **Rollback:** revert the map commit and ac-1, then re-derive BBSE3 forward (the prior stamp stays).

## STOP LIMBS
1. (a) touches an entry other than BBSE3 `CAPITAL_EXPEND`: stop and revert the map.
2. (c) writes any block other than BBSE3's, the block differs from its capture, or a value moves: stop and name it.
3. Any `ERROR:` or a non-zero rc: stop.

**COO HALF: SIGNED** for gate, (a), (b), (c) (1 block) and (d) (at most 1 dossier). `2.0.0_SA_COO~X`, 2026-10-01, against
`build_unit_map.main` / `zero_dominated_counts`, `model_block_pull.stage_derive`, and `dossier.write_one` / `current_inputs`, all at
`b239301bb1`.
