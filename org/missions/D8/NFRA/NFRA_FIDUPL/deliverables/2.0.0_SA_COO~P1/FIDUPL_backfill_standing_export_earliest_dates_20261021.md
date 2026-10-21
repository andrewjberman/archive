# FIDUPL deliverable 2, first answer: how far back the STANDING export goes (measured 2026-10-21)

Author 2.0.0_SA_COO~P1, 2026-10-21 ~11:30Z, for 4.0.0_SA_CRO~FIDELITY (the ms report) on CTO msg 9076. Dates, counts and byte sizes only; no account number, G number, label or file content.

## The answer

The standing Wealthscape custom export serves exactly **three export days** for this login: dateString 2026-10-19, 2026-10-20 and 2026-10-21. Earlier dates answer an empty Export Status list (2026-10-16, 2026-10-15) and then the retention stop on the third (2026-10-14, evidence "empty listing x3"). All three days are landed. The per-day files carry the PREVIOUS trading day's content:

| export day (dateString) | content date landed under | files landed |
|---|---|---|
| 2026-10-19 (Mon) | **20261016** (Fri) | account, position, balance, prices, security; transact NOT served |
| 2026-10-20 (Tue) | **20261019** (Mon) | all six |
| 2026-10-21 (Wed) | **20261020** (Tue) | all six |

Earliest landed content date: **2026-10-16** for account, position, balance, prices, security; **2026-10-19** for transact.

## Landed volume (bytes, from the bucket under `fidelity/alongside/bronze/<type>/<content date>/`)

| type | 20261016 | 20261019 | 20261020 |
|---|---|---|---|
| account | 3,794,179 | 3,794,367 | 3,797,333 |
| position | 30,326,543 | 30,334,785 | 30,333,376 |
| balance | 1,223,747 | 1,221,776 | 1,222,782 |
| prices | 645,722 | 646,731 | 647,773 |
| security | 655,578 | 656,599 | 657,657 |
| transact | none | 602,207 | 235,734 |

## The retention evidence (run 6, 2026-10-21 11:20:39Z to 11:22:36Z, one sign-in, logout ok, exit 0)

DAY 2026-10-21 completed, 2026-10-20 completed, 2026-10-19 completed (five files each, transact skipped by option), 2026-10-16 EMPTY, 2026-10-15 EMPTY, 2026-10-14 RETENTION (the third consecutive empty trading day; the planner stops). The export profile was created on or about 2026-10-19, so there is nothing older in the standing export; the status list is the calendar of the profile's own outputs, not of Fidelity's history.

## What each file's as-of date does (the lander rule, ruled by the CTO msg 9045)

`account.txt` carries the CALENDAR day before the export as its as-of (a Saturday for the 2026-10-19 export); the other five files carry the previous TRADING day. The lander lands a file under the last trading day on or before its as-of and records both dates (`content_as_of`, `content_date`), so `account.txt` lands beside its siblings.

## The transact file of 2026-10-19

The sixth file of the 2026-10-19 export (transactions) never answered in three runs on two different clients (452 s, 461 s, 471 s). It is skipped by option (`--skip-files transact.txt`) for the earlier days; transactions older than the standing files come by the per-account historical route (the CRO's date-range method, probe 2a), not by the standing export.

## Where older history comes from (not yet measured)

1. The **Historical Prices & Positions** export wizard (menu: Service, Historical Prices & Positions): its create call was never captured (probe 2b).
2. The **per-account historical transactions** custom range (probe 2a, replayable per account).
The agent's read-only walk of probe 2 is ordered for 2026-10-21 12:05Z or later (CTO msg 9076).

## Records

`org/missions/D8/NFRA/NFRA_FIDUPL/deliverables/0.7.0_AE_CloudOps~NFRA1/NFRA_FIDUPL.TO-FT-s-11.backfill_probe1_step3F_output.md` (run 6, verbatim) and its sibling files for runs 1 to 5 (3A to 3E): the stalls, the budget stops and the landing of the first earlier day (run 5, 09:05Z).
