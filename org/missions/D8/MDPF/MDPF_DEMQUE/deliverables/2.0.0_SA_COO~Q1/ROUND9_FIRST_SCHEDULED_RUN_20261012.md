# MDPF_DEMQUE round 9 -- the first scheduled run after the tiers: 2026-10-12 22:30 ET (read 2026-10-13 ~04:2xZ by 2.0.0_SA_COO~Q1)

Instruments: `~/.opal/demque/ledger.jsonl` (device-local), `pacer.json`, `unresolved.csv`, the scheduled task's state, and
`extend_frontier.py --lag-report` at HEAD (S3 read only, frontier 2026-10-13, indexed 326). Every number below was read from one of them.

## The run

| item | measured |
|---|---|
| task `Opal MDPF_DEMQUE daily draw` | LastRunTime 10/12/2026 10:30:01 PM, LastTaskResult 0, State Ready |
| pacer | count 400, day 2026-10-12, pushback False (the cap held to the request) |
| day-2 standing id | `STANDING-T1-EXTEND-2026-10-12`, outcome DRAWN, 461,094 of 497,166 quoted cells (t-31 half condition: a SCHEDULED run, a fresh day id) |
| ADVI_COTBKF 15 funds | DRAWN, 19,474 of 23,340 cells; 7 landed (PCBIX, SGIIX, GFFFX, FOCPX, FCNTX, DISVX, DFLVX), 8 REJECTED:LOW_TRADE_AGREEMENT (VEIRX, ABNFX, PRILX, BALCX, AGTHX, NFFFX, MEIIX, VGHAX) |
| IRPT_BCKEND 878 | PARTIAL, 30,570 of 113,262 cells on day 1 (about 237 of 878 requests inside the cap, as the quote's 3-weekday plan says); finish 2026-10-14 stands |
| index | 141 stored names to 326 |

## The share classes (dell2 row IRPT_BCKEND-D2-W310-S3, answered @75df729030)

BRK-A (084670108) and BF-B (115637209) landed with the dash spelling: 125 rows each, 2026-04-14..2026-10-09, locked. BRK-B (084670702)
is in the index as `BRKB` with a 2017-01-04..2026-06-22 lock from an earlier request and has not been drawn by the 878 request yet (the day's
slice stopped at the cap); it is the one rolling name over its cycle.

## The lag report, declared against measured (CTO ADDENDUM 8)

| tier | declared cycle (trading days) | names | within | over | max lag |
|---|---|---|---|---|---|
| daily | 1 | 146 | 127 | 19 | 79 |
| rolling | 5 | 180 | 179 | 1 | 79 |

The 19 daily over names are the 14 held three-column names (lag about 77 to 78) and 5 names that landed tonight from the ADVI request with its
window ending 2026-06-22 (DISVX, DFLVX and three more): tonight's extension ran BEFORE the draw, so they first meet it at the 2026-10-13 run.
Not yet measured: whether they reach lag 0 tomorrow. The rolling cycle's first full reading is 2026-10-19, after IRPT's history has landed.

## What this does and does not show

- The pair's half condition "first SCHEDULED run read, day-2 id drawn" is met. The `freshness_basis` condition is met by CTO ADDENDUM 8.
- It does NOT show the rolling cycle: 180 rolling names landed today, none yet re-visited.
- The 8 rejected ADVI funds are an answer, not a defect: the as-traded close did not agree with the client's trades on 90 percent of dates; they stay
  unresolved with the next act `try another candidate symbol`.
