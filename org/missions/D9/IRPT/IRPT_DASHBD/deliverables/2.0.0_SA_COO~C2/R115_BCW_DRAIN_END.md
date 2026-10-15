# IRPT_DASHBD round 115, workstream B-CW (Cottonwood) -- drain-end packet (2.0.0_SA_COO~C2, 2026-10-15)

Issuance `463b62f4da`; order and checker amendments `ae4457aa64`, `51c4f2bfeb`; merge `8f83241ac1` (worker ~403: DB-c-4, DB-c-5). All LOCAL on `box/dell2`, not pushed. Decomposition
`org/missions/D9/IRPT/IRPT_DASHBD/decompositions/IRPT_DASHBD_DECOMP_B-CW.md` section 2. Answers `CTO_ROUND_ANALYSIS_IRPT_DASHBD_B-CW_ROUND_115_20261015.md` @d514312c6d.
`round-close-check.py --project IRPT_DASHBD --round 115 --workstream B-CW`: `verdict=MAY-CLOSE` (2 orders, 0 judgment criteria).

## The one real run (LOCAL cells)

On the merged tree: `DBC115-1-AC1 PASS`, `DBC115-2-AC1 PASS`, each recounting from a fresh S3 LIST or builder call. DB-c-6 (the ask to `~D2`, `6f953f389d`) was acked by `~D2` (msg 7951); the Cottonwood reader is cut in `~D2`'s next issuance.

## What the round established (counts, dates, instants; no client value)

1. **What wrote Cottonwood's gold (DB-c-4): AD_HOC, claim inferred.** No Lambda or scheduled job in the repo names the Cottonwood source (the two producer functions fire the other two declared channels). The gold manifests carry schema 1.1; HEAD emits 1.2. So the schedule needs a BUILT function (`irpt-cot-holdings-performance-lambda` from the builder), and a HEAD-built one writes 1.2 beside 1.1 (row W403-S2, the CTO's). No run log was read, so a job outside the repo is not excluded.
2. **2026-06-09 cannot be computed.** Its prior trading day, 2026-06-08, has no silver partition (silver starts 2026-06-09) and the source declares no gap link, so the producer's rule returns ABSENT. The pair packet excludes it with that reason (12 dates, 2026-09-28 to 2026-10-13, 36 keys; a fresh LIST found 0 of 36 present).
3. **The 2026-09-23 to 09-25 silver was not rewritten.** Each partition holds one object with one version, first written 2026-09-28 (the bucket is versioned, no delete markers); the gold for those dates was written 2026-09-29 after it (09-25 has three gold versions, all 2026-09-29). The earlier "newest object dated 09-28" oddity is a first write.
4. **The pair packet (DB-c-5, UNSIGNED, 20,524 characters, eight headings).** Function BUILD; schedule `irpt-cot-holdings-performance-daily` at `cron(15 8 ? * MON-FRI *)` America/New_York with the input-frontier hold; principal `irpt-cot-holdings-performance-role` writing only the two gold tables and reading the Black Diamond silver prefix and its own daily gold prefix; the catch-up first and the schedule created ENABLED only after its after-read. Path: `deliverables/0.9.0_WK_IRPT_DASHBD~403/NEVER_WIDEN_PACKET_DB-c-5_R115.md`.
5. **The calendar item is closed.** `exchange_calendars` was installed on dell2; `test_nyse_fallback_equals_package.py` reads 18 of 18 years equal (row D2-S50).
6. **Commonwealth silver (relayed, partition date verified).** `4.0.0_SA_CRO~DELL1` (via MSTR, msg 7972): the newest data date is 2026-06-22 (the `date=2026-06-23` partition), one ClientDelivery package, no later delivery found, contracts not read. This seat's fresh LIST: each Commonwealth Cottonwood silver table holds exactly one partition, `date=2026-06-23`. `account_return_daily` cannot resume from this source; dell1's CTO has not answered.

## What the CTO's half decides

- The principal's grants (the two-prefix read, write-only on the two gold tables) against the bucket policy, which this lane does not read; who applies (an AE lane `0.0.0_AB_MSTR~DELL2` names; none is free and live now); the schema 1.1 versus 1.2 question (W403-S2); whether the schedule starts disabled until the catch-up's after-read (as ruled); the Andrew word the rollback deletes need; both halves sign before any apply.
- `account_return_daily` after 2026-06-22: a Commonwealth delivery, an input-contract amendment or another source is the CTO's and Andrew's to rule.

## Rows

Dispositioned by `IRPT_DASHBD-D2-S53` (this seat). Still ARMED, owner `1.0.0_SA_CTO`: **W403-S4** (the list grant; ruled in the packet, awaits the sign-off) and **W403-S2** (schema 1.1 versus 1.2). INERT: W403-S1, W403-S3, and from round 114 W401-S2 and W402-S2. Disarmed: W401-S1 (`D2-S50`), W401-S3 (`D2-S49`). The CVO's watermark: no round-115 B-CW row has been graded (0 judgment criteria; the round-close reviewer `3.0.0_SA_CVO~DELL2` is present).

## Enrichment list candidates for round 116 (the CTO rules)

1. The pair itself: both halves signed on `NEVER_WIDEN_PACKET_DB-c-5_R115.md`, the AE applier named, then the function build cell (WORLD, under the pair), the principal, the 12-date catch-up and its after-read, then the schedule created ENABLED.
2. The schema 1.1 versus 1.2 ruling before the function is built (W403-S2).
3. The Cottonwood reader, `~D2`'s next issuance; B-CW re-checks that the gold the reader names is the gold the pair produces.
