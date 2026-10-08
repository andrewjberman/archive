# ETFS_RIVALS round 26 -- drain-end packet (2.0.0_SA_COO~RV, 2026-10-08 ~01:0xZ)

One cell, RIV-rg-2: the union of round 25 reads only objects whose name carries a capture time; a date's untimed objects
are read as before, one object; the mis-dated 2026-09-29 object is named in a test. The re-cut of round 25's readers by
CTO rulings msgs 31477 and 31480 on CVO ADJUDICATION_v30 (RIV-rg-1 J1 NOT MET) and row ETFS_RIVALS-Z-S71. Issuance
14d40de902; build dff49d9123; proof 63eb3d5fe5; close edc990895b; merge 8d13655287 on site-Z CLOUD (LOCAL).
**Not deployed:** the live Lambdas are at content pin fd633ec4d2 (rounds 15 to 24 plus RIV-mr-1).

## Mechanical criteria

rg-2.AC1, rg-1.AC1, rg-1.AC2 PASS 0 failures (the order's three criteria) and rg-1.AC3 PASS, re-run by the issuer on the
branch; proof instance VALID; the check files unchanged by the worker. On merged CLOUD 0576fb051f: package suite 891
passed, 2 skipped, 0 failed; 35 of 35 check files under `round15/checks/` PASS 0 failures.

## What was built

In `gold_holding_contribution.g4_objects`, the one function every reader of the table takes its uris from: an object
takes part only when `revision.capture_time` of its name is not None; a date with no timed object returns exactly one
uri, the `revision.newest` of the date's uris; a date with both kinds returns the timed only. `gold_canonical_shape._g4_for`
on a date with no timed object is back to its pre-round-25 read (its own pick by provenance records: for 2026-09-29 the
live object, from which it joins sectors, never closes). Two product files, 24 changed lines (`gold_holding_contribution.py` 11, `gold_canonical_shape.py` 13). The package test
`test_misdated_live_object_of_2026_09_29_is_never_read` names the object, says it holds 2026-09-30's closes and cites
row Z-S71.

## The live table through the narrowed reader (issuer, read-only, FROM THE BRANCH before any merge)

| date | objects | read by the new reader | against the object the live code picks |
|---|---|---|---|
| 2026-09-29 | 2, both untimed | the import alone, `market-20260929-afcd903ad844.parquet`: 172 rows, **0 closes** | identical in every column |
| 2026-10-01 | 1 | it: 32 rows, 32 closes | identical |
| 2026-10-02 | 3, all timed | all three: 601 rows, 597 closes | identical |
| 2026-10-05, 10-06 | 1 each | each: 582 / 581 rows | identical |

The mis-dated object `market-20260929-53bc393958bd.parquet` is not opened by `g4_rows` / `g4_window` on any date.

## The real run, FROM THE BRANCH before the merge (day 2026-10-07; live inputs, local writes only)

Record `round26/real_run_2026-10-07.after_rg2.json`; `round26/before_after_tables_2026-10-07.json`.

- **holding_contribution: 0 of 6,066 rows move. buying_trend: 0 of 1,406.** (Round 25's readers moved 3,259.)
- 13 of 13 chart objects carry data identical to the served objects; 5,894 markers; 5,675,727 B.
- audit.html byte-equal to the served one. index.html 1,693,709 B, the served size; 559 characters differ, all of them
  the revision stamps of the two tables the tool rebuilds locally (read: the first difference is
  `20261007T174616Z-2c3ec5a7408d` against the local `20261008T004432Z-...`).
- `fund_sections` 0 missing of 2,247; 1 script.

## Limits

- The rule rests on a name's shape plus one named object. A FUTURE mis-dated object with a timed name would be read.
  CTO term 2 of msg 31480 is the answer and is round 27's: every close a writer adds carries its trading date and the
  reader keeps a close only where it equals the partition date.
- Why the 2026-09-29 pull is a day early was not traced. 2026-09-30 has no partition at all, so that day's closes are
  on the page only as valuation-implied points.
- `_g4_for` still joins SECTORS from the mis-dated object for the report dates that fall to that partition, as the live code
  does (which dates those are was not listed). A sector does not belong to a day; not changed.
- Worker row Z-W15-S2 (round 25) stands for round 27: a live row with no close beside a backfill row with one.

## Judgment criterion owed at L9

RIV-rg-2 J1, on this run: no table row and no chart point differs from the served page; the mis-dated object's closes
are on no chart and price no contribution.

## What waits, and on whom

- The deploy: a never-widen pair; ONE republish with `refresh_a1` true so the new readers run in the Lambda before the
  2026-10-08 11:00Z daily run depends on them; the served after-tables must read 0 moved rows. Asked of 1.0.0_SA_CTO~Z
  with the COO half.
