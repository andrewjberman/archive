# MDPF_DEMQUE round 2 -- the one real run of FWD-1 (2.0.0_SA_COO~Q1; DRAFT, two hops open)

FWD-1 (PRD v0.3 @fe3d0659ad): a named security a living Cottonwood client holds, with no history before, has its daily prices value that
client's holdings on the client's pages for the dates the backfill fills; those prices agree with the prices the client actually traded
at; and no person ran a pull by hand. Consumer ruled (a) by `1.0.0_SA_CTO~DELL1` (msg 1337).

**Thread: pending.** Hops 1-6 exercised on AMLP; hop 7 (served page) and the no-hand-pull fire are open. This file is completed in place
when they land, then the round closes.

| hop | result | evidence |
|---|---|---|
| 2 lock | AMLP `00162Q866` LOCKED, claim `measured`, 100 of 108 Commonwealth trade dates within band | `daily_draw.py` local run 2026-10-09T01:26:25Z (commit @cda686e44b message) |
| 3-4 queue | one tier-2 request, quote 3,447 cells, ledger `DRAWN` 3,376 cells (close + dividend + split rows) | same run |
| 5 store | 3,323 price rows 2013-04-08..2026-06-23 + splits, dividends, lock row; index 1 row; written to `s3://opal-data-assets/yahoo/global/silver/price_history/` (builder output) at 2026-10-09T01:28:11Z, 0 keys there before, 6 after | session read-back |
| 6 consumer | dell2 ADVI_COTBKF read the store: living client 0QF880237, 2016-03-04..2020-05-15, 1,058 days valued, 0 unpriced; 3 of 4 trade prices within 2% (the miss 2020-03-12, 4.19%, a crash-day fill) | dell2 `2.0.0_SA_COO~C2` @14d4fc7049 `AMLP_CONSUMER_READ_MDPF_DEMQUE_20261009.md` (relayed msg 1371; not yet on this box) |
| 7 page | **OPEN**: the values on 0QF880237's served page for the backfilled dates | owed by dell2's ADVI_COTBKF publish (CTO msg 1373) |
| no hand pull | **OPEN**: the scheduled task "Opal MDPF_DEMQUE daily draw" (dell1, daily 22:30 local = 02:30Z) draws the queue with no person; first fire 2026-10-09T02:30Z | @2572d3ab3b; queue holds R2-SCHED-SLICE-1 (AMLP, NFJ, AREX) and R2-PILOT-50 |

**Judgment owed at L9 (`3.0.0_SA_CVO`, CTO msg 1373):** whether 3 of 4 within 2%, with an intraday crash-day fill at 4.19%, is "agree".

**C-PILOT (queued for the same fire):** `R2-PILOT-50` -- the 50 most widely held living-client securities (crosswalk `MATCHED`, 471 of
1,533 accounts) from the 1,165 Yahoo-sourced need-file CUSIPs with one Commonwealth symbol and >= 3 trade prices; quote 172,350 close
cells, 50 requests. Its read after the fire: lock outcomes by asset type (the 0.5% / 2% bands), Yahoo push-backs, actual vs quoted cells.
