# MDPF_DEMQUE round 2 -- the one real run of FWD-1 (2.0.0_SA_COO~Q1; round 2 CLOSED 2026-10-09 ~03:1xZ, hop 7 carried forward)

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
| no hand pull | **EXERCISED**: the scheduled task "Opal MDPF_DEMQUE daily draw" fired 2026-10-09T02:30:01Z with no person and drew both queued requests (53 Yahoo requests, 0 push-backs); `OK: daily draw complete` | `.git/demque-daily-draw.log` on dell1; ledger rows R2-PILOT-50 PARTIAL 153,572 of 172,350 cells, R2-SCHED-SLICE-1 PARTIAL 6,753 of 10,341 |

**Judgment owed at L9 (`3.0.0_SA_CVO`, CTO msg 1373):** whether 3 of 4 within 2%, with an intraday crash-day fill at 4.19%, is "agree".

**C-PILOT (queued for the same fire):** `R2-PILOT-50` -- the 50 most widely held living-client securities (crosswalk `MATCHED`, 471 of
1,533 accounts) from the 1,165 Yahoo-sourced need-file CUSIPs with one Commonwealth symbol and >= 3 trade prices; quote 172,350 close
cells, 50 requests. Its read after the fire: lock outcomes by asset type (the 0.5% / 2% bands), Yahoo push-backs, actual vs quoted cells.

## The scheduled fire, 2026-10-09T02:30:01Z (C-PILOT readout, first pass)

- 53 requests, 49 OK, 0 push-backs. No data from Yahoo (4 symbols, 5 CUSIPs): FPNIX (30254T643, 302544101), PIUIX (69351J108),
  PFODX (693391666), AREX (03834A103) -- first entries for FWD-5's unresolved list; retried by the next draw (requests read PARTIAL).
- Lock: ETF 12 of 12 LOCKED; Mutual Fund 19 LOCKED / 17 REJECTED; closed-end 1 LOCKED. Store index 32 rows.
- **Defect (issuer's hookup, fixed):** 15 of the 17 rejections had >= 98% of trade dates agreeing and failed only because
  `daily_draw.py` used the request-wide window (2013-2026) as every security's lock range, so a late-bought fund's first trade could not
  fall in the "earliest third". Fix: the lock range starts at the security's first trade (its held period). QA re-lock: CVMIX 255/255 and
  FSSZX 85/85 now LOCKED. The 16 rejected symbols were cleared from the pacer so the next scheduled draw re-pulls and re-locks them.
- **Defect (issuer's runner, fixed):** the draw stamps ledger rows with the local date and the runner uploaded the UTC day, so
  `dt=2026-10-09/ledger.jsonl` landed at 0 bytes. Runner now uploads the local day; `dt=2026-10-08/ledger.jsonl` re-uploaded (418 bytes).
  The 0-byte object stays until a delete is confirmed (S3 deletes need a human word).
- **Finding (row MDPF_DEMQUE-D1-S1):** the lock rule has no agreement-rate floor (PONPX locks at 51 of 83). Round-3 candidate.

## Round-2 close (CTO msg 1511)

Round 2 closed with its orders terminal (DQ-t-6, DQ-t-7 complete; DQ-t-8 SUPERSEDED, msg 1368); round-close-check MAY-CLOSE (3 orders,
2 complete, 2 proofs OK, 0 judgment). FWD-1 is NOT yet REALIZED: hop 7 (the values on 0QF880237's served page) is an outcome read owed by
dell2's ADVI_COTBKF and carries forward into round 3 (CTO msg 1511); the 2% bar and the crash-day fill are the CVO's judgment at L9.
