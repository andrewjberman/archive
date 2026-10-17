# ORDER 3 (Andrew-direct): the held-day total return -- pull into a local layer, replay the rankings, publish only under the pair

**From:** `2.0.0_SA_COO~RV` (ETFS_RIVALS issuer, dell1). **To:** `0.0.3_BG_BBGTerminal` (site Z).
**Authority:** Andrew, verbatim, ~04:2xZ: "Yeah I want all those completely filled", then "now" (record
`org/tier1_exec/2.0.0_SA_COO~RV/deliverables/ANDREW_DIRECT_20261017_031xZ_RIVALFUNDS_BACKFILL_365D_NOW.md`). Ruling:
`1.0.0_SA_CTO~DELL1` msg 7291 (the TR writer cell now; "its served-rankings never-widen pair comes to me before any TR row lands
where the rankings read"). Writer: RIV-za-1, merged on box/dell1 @27ec89ad2a. No limit changes; surface C, site Z's ledger.

Script: `org/missions/D5/ETFS/ETFS_RIVALS/deliverables/2.0.0_SA_COO~RV/round32/heldtr_stage.py` (three acts; read its header).
Units: `heldtr_units_p1.json` (87,767 units, 684 securities, 2026-02-04..2026-10-12, ~175,534 points + lookups) and
`heldtr_units_p2.json` (36,166 units, 576 securities, 2025-10-13..2026-02-03, ~72,332 points) in the same folder: together the
123,933 units of `MDPF_DEMQUE/requests/ETFS_RIVALS-C1-TR-HELD-{D30,D90,D365}` (held in DEMQUE, CTO msg 7280). Keep paths short:
Windows refuses a path over 260 characters, so use the layer dirs below.

## Act 1 -- pull (spends; writes ONLY the local layer; no pair needed)

From the workspace root, at or after @27ec89ad2a:
```
python org/missions/D5/ETFS/ETFS_RIVALS/deliverables/2.0.0_SA_COO~RV/round32/heldtr_stage.py pull . C:/opal-elev/rvht1 org/missions/D5/ETFS/ETFS_RIVALS/deliverables/2.0.0_SA_COO~RV/round32/heldtr_units_p1.json 180000
python org/missions/D5/ETFS/ETFS_RIVALS/deliverables/2.0.0_SA_COO~RV/round32/heldtr_stage.py pull . C:/opal-elev/rvht1 org/missions/D5/ETFS/ETFS_RIVALS/deliverables/2.0.0_SA_COO~RV/round32/heldtr_units_p1.json 180000 --live
```
The first line is the dry run (requests nothing). Measured on dell1 for all 123,933 units: `248044 points planned (123933 units x 2
fields + 178 currency lookups)`. p1 fits what surface C has left today after rv-bf365, step 1 and the dividends; if the dry run
says REFUSED, send the line back and stop. p2 runs the same way into `C:/opal-elev/rvht2` on the next ledger day.

## Act 2 -- replay (reads only; reply with its table)

```
python org/missions/D5/ETFS/ETFS_RIVALS/deliverables/2.0.0_SA_COO~RV/round32/heldtr_stage.py replay . C:/opal-elev/rvht1 C:/opal-elev/rvht1o
```
It builds gold holding_contribution (the rankings) for the newest live day twice through overlays, without and with the layer, and
prints per fund: content hashes, rows whose contribution moved, rows whose rank_best moved, and holding-implied days A -> B.
Measured on dell1: an empty layer reads 13 of 13 funds equal; the `--control` arm (synthetic held-tr rows on 25 days) reads 0 of 13
equal, so the comparison can fail (`heldtr_replay_2026-10-16_{empty,control}.json` here). Reply with the printed table and the
json path.

## Act 3 -- publish (the SERVED act: ONLY after the issuer names both never-widen halves signed)

```
python org/missions/D5/ETFS/ETFS_RIVALS/deliverables/2.0.0_SA_COO~RV/round32/heldtr_stage.py publish . C:/opal-elev/rvht1
python org/missions/D5/ETFS/ETFS_RIVALS/deliverables/2.0.0_SA_COO~RV/round32/heldtr_stage.py publish . C:/opal-elev/rvht1 --apply
```
The first prints the write set; the second puts each object to its live uri when absent, reading each back.

### COO never-widen half (2.0.0_SA_COO~RV), for act 3

- Write set: the `gold/security_market/date=<D>/market-<capture time>-<digest>.parquet` objects in the layer, one per date of the
  part, each new (a present uri is skipped, never overwritten). Rows carry `as_of_source` "held-tr", `price_date` = D, PX_LAST and
  total return, `claim` MEASURED. Nothing else is written.
- Writers of the property: G4 `security_market` has four writers in `enrichment_bloomberg.py` -- the daily market pull (the
  report date, non-backfill), market-range and history-owed (past dates, backfill-marked), and held-tr (past dates, non-backfill).
  N = 4 writers, 4 rules read. held-tr is the only non-backfill past-date writer, so its rows outrank the backfill rows of the same
  (security, date) in `_g4_merge` and stay in `drop_backfill`'s kept set.
- What it may move, from the G4 readers in `data/etfs/scripts/rivalfunds/*.py` (census of `g4_window(`, `g4_rows(`,
  `"security_market"`: 10 non-test modules): the rankings (`gold_holding_contribution`, measured by act 2 per fund), and,
  NOT measured by act 2, `gold_trade_schedule`, `gold_buying_trend`, `gold_canonical_shape`, `price_series` (the dialog's curve on
  those dates reads the held-tr close instead of the backfill close), `gold_input_census`, `history_owed` (the units leave the owed
  set) and `dramatic_move`. Every move lands at the next publish; nothing is republished by this act.
- Both branches: a date whose object lands enters the union; a date with no answered unit lands no object and moves nothing.
- Rollback per key: removing each object is an S3 delete, Andrew's act, not given by this half (as the CTO's order-2 half C-1).
- The expected outcome is act 2's measured table, read from the producer's own build on the live inputs plus the layer; the CTO
  half names it.
