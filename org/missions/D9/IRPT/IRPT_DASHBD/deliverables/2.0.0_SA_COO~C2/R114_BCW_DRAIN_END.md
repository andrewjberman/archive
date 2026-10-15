# IRPT_DASHBD round 114, workstream B-CW (Cottonwood) -- drain-end packet (2.0.0_SA_COO~C2, 2026-10-15)

Issuance `cf8ab92263`; checker amendment `323883217a`; merges `bea5f1de31` (worker ~401: DB-c-1, DB-c-2) and `6150170b3e` (worker ~402: DB-c-3). All LOCAL on `box/dell2`, not pushed. Decomposition
`org/missions/D9/IRPT/IRPT_DASHBD/decompositions/IRPT_DASHBD_DECOMP_B-CW.md`. `round-close-check.py --project IRPT_DASHBD --round 114 --workstream B-CW`: `verdict=MAY-CLOSE` (3 orders, 3 complete, 3 proofs ok, 0 judgment criteria).
No CTO analysis preceded this round (the ruling `CTO_RULING_DELL2_IRPT_DASHBD_FOUR_WORKSTREAMS_AT_ROUND_114_20261015.md` says the first analysis is the CTO's at this workstream's first slug). This packet is that slug's body.

## The one real run (LOCAL cells)

The three criteria re-run on the merged tree after both merges, `python -I org/missions/D9/IRPT/IRPT_DASHBD/deliverables/2.0.0_SA_COO~C2/checks/r114/p114_bcw.py . <id>`:
`DBC114-1-AC1 PASS`, `DBC114-2-AC1 PASS`, `DBC114-3-AC1 PASS`. Each criterion recounts from a fresh S3 LIST or a fresh builder call, so a PASS is a measurement of today, not of the worker's claim.

## What the round established (counts, dates, times; no client value)

1. **Landing time (DB-c-1).** The Cottonwood Black Diamond silver partition lands at 07:46 New York on each of the last 15 trading days (all 11:46 UTC, seconds 02 to 30). 15 of 15 are after 06:00 New York. The worker proposes a fire at 08:15 New York.
2. **Frontier (DB-c-1).** `holdings_performance_daily` gold ends 2026-09-25; `account_return_daily` ends 2026-06-22. Silver holds 93 partitions through 2026-10-13. The catch-up set is 13 trading days with an input and no gold: 2026-06-09 and 2026-09-28 to 2026-10-13.
3. **The packet (DB-c-2, UNSIGNED).** `deliverables/0.9.0_WK_IRPT_DASHBD~401/NEVER_WIDEN_PACKET_DB-c-2_R114.md`: schedule `irpt-cot-holdings-performance-daily`, principal `irpt-cot-holdings-performance-role` (both from `lib/opal_naming.py name()`, no refusal), 39 keys (3 per date), none present now (a fresh LIST found 0 of 39), both branches, rollback per key, nine questions for the CTO's half.
4. **No Cottonwood reader exists (DB-c-3).** No served or scheduled code reads a Cottonwood gold prefix today. `account_return_daily` has 3 readers and `holdings_performance_daily` 3, all firm-generic and resolving to the declared custody source, not Cottonwood; `account_dim` has 0 (claim inferred: five binary fixtures were not text-searched). A Cottonwood account page therefore cannot show a return from these tables yet (FWD-11).
5. **The fallback calendar's equality was not run.** `pandas_market_calendars` is absent on dell2; the test printed SKIPPED. Every trading-day answer in this round is from `NYSE/hardcoded-fallback-2010-2027`.

## What the CTO's half decides (from the packet and the reads)

- The 08:15 time against the 06:00 ET fold and `~P2`: the fold's meaning is not established here, and the 15 landings are all after 06:00.
- Whether a Cottonwood function, package and Terraform exist for the schedule to call: not established. The schedule cannot fire without one.
- The principal's grants; which AE instance applies; whether the schedule starts ENABLED; the pair (both halves signed before any apply or catch-up run).
- Whether the 2026-06-09 gap is expected (the producer reads the prior trading day; no silver exists before 2026-06-09) and whether the three partitions 2026-09-23 to 2026-09-25, whose newest object is dated 2026-09-28, were rewritten after a gold run.
- `account_return_daily` after 2026-06-22 has no input until a Commonwealth delivery or an input-contract amendment (`DB-b-201` section 7): carried, not cut.
- No Cottonwood reader (finding 4): a reader to build is a round-N enrichment for the CTO to rule on, and the contract member for it is `~D2`'s (sole contract writer).

## Rows

Disposed by `IRPT_DASHBD-D2-S49` (this seat): W401-S3 disarmed; W402-S1 closed (the issuer's checker defect, fixed in `323883217a`); W402-S3 noted. Still open: **W401-S1 ARMED, disarm owner `0.0.0_AB_MSTR`** (the fallback calendar on dell2). Carried INERT: W401-S2, W402-S2. The CVO's watermark: no round-114 B-CW row has been graded (0 judgment criteria; the round-close reviewer is `3.0.0_SA_CVO~DELL2`, present).

## Enrichment list candidates for round 115 (the CTO rules)

1. The Cottonwood reader path for the account page (finding 4), thread-breaking for FWD-11.
2. The Cottonwood function and its Terraform, so the schedule has a target (WORLD, under the pair).
3. The pair for the schedule, principal and 13-date catch-up run.
4. The package-calendar equality, once a box with `pandas_market_calendars` runs the test (or the package is installed by its owner).
