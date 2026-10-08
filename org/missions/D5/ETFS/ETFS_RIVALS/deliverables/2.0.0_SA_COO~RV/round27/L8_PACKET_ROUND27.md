# ETFS_RIVALS round 27 -- task-order packet for 3.0.0_SA_CVO~RV (FWD-24, the vendor request OFF)

**Compiler:** `2.0.0_SA_COO~RV`, 2026-10-08. Issuance 21b3614f93; amendment 9c349b8d0a (a note only). Three orders, all
terminal. Nothing is deployed and nothing is written to S3 by this round so far.

| cell | order file | state | mechanical criteria, re-run by the issuer |
|---|---|---|---|
| RIV-ho-1 | `ETFS_RIVALS.TO-RIV-ho-1.the-history-owed-set-from-stored-tables-alone.md` | complete, MERGED (aca932cd3f) | ho-1.AC1 PASS 9 of 9 |
| RIV-rk-1 | `ETFS_RIVALS.TO-RIV-rk-1.the-reader-keeps-a-close-only-on-its-own-trading-date.md` | complete, MERGED (d99155c49a) | rk-1.AC1 PASS 14 of 14 |
| RIV-tw-1 | `ETFS_RIVALS.TO-RIV-tw-1.the-daily-leg-asks-for-owed-closes-request-off-by-default.md` | complete ON ITS BRANCH `wk-ETFS_RIVALS-19` @de25db03ea, NOT merged | tw-1.AC1 PASS 6 of 6, tw-1.AC2 PASS 7 of 7 (on the branch) |

On merged CLOUD (d99155c49a): suite `899 passed, 3 skipped`; check files 37 of 39 end `PASS 0 failures`; the two that
do not are tw-1.AC1 and tw-1.AC2, which grade the unmerged branch's code.

## The real runs (the artifacts J1 of each cell is graded on)

- **RIV-ho-1 J1:** `round27/history_owed_live_2026-10-08.json` -- `history_owed.owed(S3Sink, "2026-10-08")`, read-only:
  742 securities, 184,600 units, 251 dates (2025-10-08 to 2026-10-07); per security min 247, median 248, max 251;
  191 securities owe their whole window. Newest dates: 2026-10-07 742 (not pulled yet), 10-06 191, 10-05 192,
  10-02 233, 10-01 710, 09-30 742. Three sample units are in the file for a hand check against the stored tables.
- **RIV-rk-1 J1:** run FROM THE BRANCH before the merge. (i) every live `security_market` date (5 dates, 8 objects) read
  through the branch's `g4_rows`: identical in every column to the object the live code picks, no extra column.
  (ii) `real_run.py` for day 2026-10-07 against the served tables (`round27/before_after_tables_2026-10-07.rk1.json`):
  holding_contribution 0 moved of 6,066; buying_trend 0 moved of 1,406; 13 of 13 chart objects with `securities`
  data identical to the served ones; audit page byte-equal; 2,247 of 2,247 fund sections present.
  Not exercised on live data: the three new rules themselves -- the live table holds no `price_date` column, no date
  with both a timed and an untimed object that differ in descriptive fields beyond what round 26 covers, and no
  backfill row. Those are graded by the check's fixtures only.
- **RIV-tw-1 J1:** no real run exists and none is made by a seat: the real entry point is the scheduled vehicle and a
  paid vendor. The merge is a deploy to that vehicle and carries a never-widen pair (CTO ruling msg 31584); COO half
  `round27/NEVER_WIDEN_HALF_COO_R27_TW1_MERGE.md`. It lands after the 2026-10-08 11:00Z run is read; the first
  scheduled run after it is the read.

## Rows of the round

- `ETFS_RIVALS-Z-S74` (issuer, OBSERVATION): the issuance gate admitted a duplicate cell id (rk-1; also cu-1 in round
  24) and refuses the rename.
- `ETFS_RIVALS-Z-W20-S1` (worker ~20, OBSERVATION): the row-existence test for a security held only by the picked
  untimed object reads the GICS columns, name and parsekey, because provenance columns are never null.

## Stated gaps (issuer's, for the round-28 list)

- Top-up rows carry a NULL currency; the chart draws no curve for a security with no stored currency.
- The leg passes the report date as the owed window's end, so the newest day is picked up a day late.
- `HISTORY_OWED_CAP` = 5,000 units a run is the issuer's number; 184,600 units is 37 runs. Not ruled.
- Still untraced: row Z-S73, and why the 2026-09-29 pull is dated a day early.
