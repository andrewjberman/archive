# AMGT_CORPUS round 17 -- never-widen pair for Hitachi 6501 JP's model-block pull (cell CRPS-s-1's exercising act)

COO half below, signed by the issuer `2.0.0_SA_COO~X`. The CTO half is owed by `1.0.0_SA_CTO~Z` in its own lane
(`org/missions/D5/AMGT/AMGT_CORPUS/ledger/`). Ruling it implements: round-16 analysis s.2 ruling 4 and s.4 cell 1 @`61ed59c609`
("if the admission is missing, the fix goes through the same scripted Bloomberg pull (R-21); a served write is its own pair");
AMGT_RESAPP `ROUND_ANALYSIS.round49.md` ruling 4.

## THE ACT -- ONE NAME, THE EXISTING SCRIPT, FROM A CLEAN CHECKOUT
1. Run from a detached worktree at CLOUD HEAD, NOT the shared tree, because the derive stage writes the repo file
   `integrations/bloomberg/research/field_map.json`. In the shared tree that file carries another seat's UNCOMMITTED edit (+1187 /
   -134 lines; not this seat's, not touched).
   - `python integrations/bloomberg/research/model_block_pull.py pull --securities "6501 JP Equity"`
   - `python integrations/bloomberg/research/model_block_pull.py derive --securities "6501 JP Equity"`
2. Commit that worktree's `field_map.json` delta (Hitachi's entries only) and merge it into CLOUD.
3. A change entry opens before step 1 and closes on the after-state reads.
- The census that found the gap: `deliverables/0.9.0_WK_AMGT_CORPUS~1/MODEL_BLOCK_CENSUS_ROUND17.json` (merged `01682baecd`):
  95 of 96 present, `6501_JP_Equity` absent, and the producer admits no new registration without a named ticker.
- The act's precedent: the rr-1 ledger `20260925T2156Z_amgt-rr-1-five-no-block-names_deploy_completion.md`.

## VENDOR AUTHORITY
Andrew R-21 `b390c36444` (all vendors, through a script). The pull makes Bloomberg DAPI calls:
- one ReferenceData header request;
- one HistoricalData request;
- three ReferenceData forecast requests (`BEST_FPERIOD_OVERRIDE` 1FY/2FY/3FY).

The derive may call `sa_forecast_fallback.py` (Seeking Alpha) for each forecast cell Bloomberg leaves empty. Every call is
scripted. `bloomberg_health` read `ok: true` (127.0.0.1:8194) at signing.

## WRITER CENSUS
- **Raw:** `bloomberg/harvest/bronze/{refdata,histdata,bestdata}/security_key=6501_JP_Equity/<stamp>.json`, written by
  `stage_pull`. Fresh stamps; never an existing key.
- **Derived:** `derived/model_block/6501_JP_Equity/<stamp>/model_block.json`, written by `stage_derive`, fresh stamp.
- **Unit map:** `integrations/bloomberg/research/field_map.json`, via `build_unit_map.py`'s additive merge, which never
  overwrites a MEASURED entry, and only when the map has no entry for the security.
- N = 1 producer for each surface: `model_block_pull.py` at CLOUD HEAD.

## BEFORE-STATE (measured 2026-09-29 ~23:3xZ)
- The bronze `refdata`, `histdata` and `bestdata` tables each hold 0 objects under `security_key=6501_JP_Equity`.
- `derived/model_block/6501_JP_Equity/` holds 0 objects.
- CLOUD HEAD `field_map.json` has no `6501` entry.
- The crosswalk record is `6501_JP_Equity` (`bloomberg_security` `6501 JP Equity`, HITACHI LTD).

## EXPECTED OUTCOME, READ FROM THE PRODUCER'S OWN RULE -- both branches
- **Branch 1 -- Bloomberg answers (the terminal is up):**
  - 3 raw puts, then 1 derived `model_block.json` under a fresh stamp, whose figures carry `{value, unit, sign, basis, vintage,
    source}`.
  - Closed fiscal years only; groups not yet closed go to `unresolved`.
  - Forecast cells are sourced `BBG`, or `SA_FALLBACK` where Bloomberg left a cell empty.
  - `field_map.json` gains Hitachi's field entries; no existing entry moves.
  - Served effect: AMGT_RESAPP's export and `/thesis` model read Hitachi's block, and the deployed export stops refusing the
    name. For the other 95 names, nothing is written.
- **Branch 2 -- a request fails or returns field errors:**
  - The raw lands exactly as returned, which is the point of C-RAW-BEFORE-DERIVED.
  - The derive either records what is `unresolved` or refuses. No partial block is served under a failed stage; a derive that
    refuses writes nothing.
  - Stop limb 2.

## AFTER-STATE THE VERIFY READS
1. bronze: 1 object in each of the 3 tables for `6501_JP_Equity`; derived: 1 `model_block.json`.
2. `model_block.json` names at least one closed fiscal year, and every figure carries its six fields.
3. The `field_map.json` diff against CLOUD HEAD adds only Hitachi keys (0 changed, 0 removed).
4. The CRPS-s-1 census re-run reads `present 96 absent 0`.

## BLAST RADIUS AND ROLLBACK
- **Touches:** 3 bronze objects, 1 derived object, and the unit-map file (additive). No delete, no overwrite.
- **Rollback:**
  - revert the `field_map.json` commit;
  - the derived object is write-once, and a reader picks the newest stamp.
  - Un-serving it needs a delete, which is Andrew's act. The exposure is one name gaining a model block it lacked, which is the
    ratified direction.

## STOP LIMBS
1. `bloomberg_health` is not ok, or the pull reports a session error: stop. The terminal sign-in is `READ_HERE.md` section 2 and
   needs Andrew's MFA.
2. Any stage exits non-zero, or derive refuses: stop. Nothing is committed; the raw stays as evidence.
3. The `field_map.json` diff touches any non-Hitachi key: stop and discard the worktree's edit.

**COO HALF: SIGNED.** `2.0.0_SA_COO~X`, 2026-09-29, against CLOUD HEAD at signing (`01682baecd` or later with
`integrations/bloomberg/research/` unchanged).
