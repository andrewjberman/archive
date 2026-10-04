# AMGT_CORPUS round 35 -- never-widen pair for `CRPS-ak-4`: the unit-map rebuild for the 52, one re-derive of each served block, and the re-pin to the commit carrying the map

**Authority:** round-34 analysis @`83cd052a9c`, ruling 2 and s.3 item 1: "the map write is the served move, so it takes a pair".
Decomposition v35.0 @`17a5893472`.

**Code:** CLOUD at or after `1ed823496d`. It carries:
- CRPS-ak-1 @`7c43d48775`: the families for the 52;
- CRPS-ak-2 @`61c58e31bc`: the explicit interpreter in the re-pin script;
- CRPS-ak-3 @`a5a561d96b`: the dry-run repair;
- the Z-W1-S30 disarm @`1ed823496d`: CRNCY_ADJ_MKT_CAP's basis reads millions.

## TIMING: the served legs run AFTER the 2026-10-04 13:00Z scheduled fire is read

1. The scheduled task derives with its pinned checkout's own `field_map.json`, currently pin `a864e82a5c`, whose map has no family
   for the 52. A map write and re-derive before 13:00Z would be undone at 13:00Z: that fire would re-derive every block with
   pointer units again. That is served churn.
2. A re-pin before 13:00Z would make the acceptance fire run new code, so a failure there could not be attributed to the
   round-34 producer the CVO graded.

So legs m, d and r run together after FWD-22's acceptance read, and the acceptance stays on the pin it was graded on.

## THE SERIALIZING DRY RUN OVER EVERY KEY (`checks/round35/ak4_dryrun.py` -> `evidence/r35_ak4_dryrun.txt`)

It runs in memory: `build_unit_map`'s own `resolve_population(crosswalk)`, `load_raw_for_key`, `prepare_header` and
`build_entries` (remeasure=False, the additive merge), compared with the committed `field_map.json`. It wrote nothing; the
committed map was unchanged after it.

- **Population:** 237 crosswalk keys, 100 with raw landed.
- **The 52 over 100 names:** 4,398 MEASURED, 802 UNRESOLVED. Of the UNRESOLVED, 656 are "no value returned for this mnemonic",
  23 are ZERO-DOMINATED (10/10 or 11/11 fiscal years zero) and the rest are named magnitude non-discriminations. Every
  UNRESOLVED carries its reason.
- **Base entries:** 6,600 compared, 0 units moved in substance. Two base texts change, and neither is a unit. They are
  UNRESOLVED-to-UNRESOLVED re-samples with the same reason and a new sampled magnitude from the 10-03 raw:
  - TSM `CURR_ENTP_VAL` 71,993,494 -> 75,714,013;
  - RKT `SI_PERCENT_EQUITY_FLOAT` 0.005699 -> 0.005701.
- **The would-be map:** 118 fields (66 committed + 52), 100 securities (unchanged).

## THE ACT, IN ORDER (one NEVER-2 entry, slug `amgt-corpus-r35-ak4`)

0. **Gate.**
   - The 13:00Z fire has been read: its closing line and the refresh line.
   - Re-run `ak4_dryrun.py` on the post-fire raw. It must again show base units moved 0 in substance, with the 52's counts
     printed.
   - `schedule_induction.ps1 -Plan -Commit <m>` prints `PLAN python ...\Python311\python.exe (source: live-task)`. STOP on
     anything else.
1. **(m) Map write:** `PYTHONPATH=. python integrations/bloomberg/research/build_unit_map.py --population crosswalk`. Commit
   `field_map.json` alone as commit `<m>`.
2. **(d) Re-derive:** one `stage_derive(s3, security, raw_stamp=<newest raw>, sa_fallback=False)` per registered name (96). Each
   writes a NEW write-once `derived/model_block/<key>/<stamp>/model_block.json`.
3. **(r) Re-pin:** `schedule_induction.ps1 -Register -Commit <m>`, then `-Status`.
4. **(v) Verify:**
   - the newest block of all 96 names is the re-derive's stamp;
   - the count of the 52's figures carrying the pointer unit "SEE field_map.json" reads 0. Each figure carries a measured unit,
     or the name sits in `unresolved` with its reason;
   - BA's Model tab is looked at (version newest; no pointer or raw-list text);
   - the task reads Start In `<m>`, Python311, 13:00Z.

## EXPECTED OUTCOME, READ FROM THE PRODUCERS' RULES (every branch)

- **Writers of the served block:** one function, `stage_derive`, reached by `cmd_derive`, `cmd_admit`, `cmd_refresh` and this
  leg's loop.
- **The unit a figure carries:** `_resolved_unit` reads it from `field_map.json`, with the per-security exception path. N = 2
  rules read.
- **Branch A (map written, all 96 derive):** the 52's figures carry MEASURED units, roughly 4,398 entries of 5,200 over 100
  names. The rest are UNRESOLVED with their reason. The 66 base fields' units are unchanged, and no value moves (the same raw
  is re-derived).
- **Branch B (a name fails to derive):** it keeps its 13:00Z block, the failure is listed, and the other names proceed.
- **Branch C (the plan names a non-Python311 interpreter, or the script refuses):** STOP before (r). The map and blocks stand,
  and the old pin's next fire would re-derive pointer units, so roll (m) and (d) back in the same session (below).

## BLAST RADIUS AND ROLLBACK (per key)

| what | may touch | rollback |
|---|---|---|
| `integrations/bloomberg/research/field_map.json` | +52 field entries; 2 base UNRESOLVED texts re-sampled; 0 base units | revert commit `<m>` |
| `derived/model_block/<key>/<stamp>/model_block.json` | up to 96 NEW write-once keys, each becoming the served newest | forward: re-derive from the same raw with the reverted map (mints a newer block with the prior units); exact restore by deleting the new objects needs Andrew's word |
| Scheduled Task `amgt-induction-daily` | its Start In (pin `<m>`), interpreter Python311 (unchanged), trigger unchanged | `-Register -Commit a864e82a5c` |

Never touched: any raw/bronze object, any Bloomberg call (the re-derive reads landed raw only), any Seeking Alpha call
(`sa_fallback=False`), any portal file, any other firm.

**COO HALF: SIGNED** by `2.0.0_SA_COO~X`, 2026-10-04 ~02:0xZ, for legs 0, m, d, r and v, covering branches A, B and C. The legs
run after the 13:00Z acceptance read.

**CTO HALF:** owed by `1.0.0_SA_CTO~Z`.
