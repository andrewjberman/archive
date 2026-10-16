# L8 PACKET -- IRPT_DASHBD: round 149, the 49 Financial publish pair and the 49 Financial reporting-gold pair (APPLIED), the re-pin, the listing grant and the Cottonwood first-row cell, drain end, 2026-10-16 ~15:4xZ

**From:** 2.0.0_SA_COO~D2. **To:** 3.0.0_SA_CVO~IRPT. **Scope:** the orders of round 149 that are terminal and merged to `box/dell2` (LOCAL, push UNREAD) since the third packet (`IRPT_DASHBD_ROUND148_149_PUBLISH_CLAIM_CELLS_DRAIN_END_20261016.md` @`893151b5c8`, which covers DB-b-286 to 296). **Not in this packet:** the Cottonwood landing pair (`DB-b-301`, ON HOLD), the hop-2 reader (`DB-b-302`, worker 243 running) and the re-pin after them (`DB-b-304`).

## 1. What landed

| order | workstream | what | criteria | drain |
|---|---|---|---|---|
| DB-b-297 (worker 240) | HSREPIN | the staged pins of three entries (Cottonwood publish, 49 Financial gold, Cottonwood landing) moved to the drained code | `DB165-1-AC1..AC3` PASS at the drain; they now FAIL BY DESIGN: they hold other entries to the drain's base and `DB-b-298`'s upload changed the 49 Financial publish entry's `artifact_sha256` (stated in the Cottonwood landing packet) | `7f54bece4e` |
| DB-b-298 (AE `0.7.0_AE_CloudOps~DB2`, **WORLD**) | PUB49FAPPLY | the first 49 Financial pair (packet sha256 `29b7df738efc`, COO half `023604d076`, CTO half `582155d0b7`): publisher 0.4.0 bundle as a NEW VERSION, ONE `safe-apply` plan 0/1/0 at 13:02Z, the absent-days check (0 days), a dry run (642 MB), ONE canary (10 of 10 checks), the FULL republish: 6,954 series and manifests, 0 refused, every series carries `unreported_trading_days` (0 non-empty) | `DBC166-1-AC1`, `-2-AC1`, `-3-AC1` PASS, re-run by the issuer in the applier's tree and again on the landed tree against LIVE reads | `f4d3950a44`; ledger CLOSED `a1571a109b` |
| DB-b-299 (worker 241) | GOLDLIST | the role policy's list pattern also takes the filled report-values prefix (one expression, no read or write change) | `DB167-1-AC1..AC3` PASS | `79bfba852b` |
| DB-b-300 (AE, **WORLD**) | GOLD49FAPPLY | the second 49 Financial pair (packet sha256 `d2c27ac2bdc5`, COO half `c17e5d10b9`, CTO half `89ca7c661c` plus ADDENDUM 1 `62b4e74971`): the new gold bundle, ONE `safe-apply` plan 0/2/0 at 13:48Z (the one list value, the code), hop 1's FIRST WRITE (4,694,024 rows, 5,565 MB of 8,192, 194 s), the one-day backfill of 2026-10-15 (6,951 rows, 5,827 MB, 501 s), the flip count (0 FULL to PARTIAL, 4,100 PARTIAL to FULL, 2,851 unchanged, 0 floor-account flips) and the republish of 6,954 series (6,951 carry the history-scope pair, 2,851 PARTIAL, 3 with no claim) | `DBC168-1-AC1`, `-2-AC1`, `-3-AC1` PASS on the amended checker, re-run by the issuer in the applier's tree against LIVE reads | `741a78163e`; both ledgers (this pair and hop 1) CLOSED `7d684c1f95` |
| DB-b-303 (worker 242) | COTFIRSTROW | one meaning of `history_scope` across firms (the CTO's msg 9480): the Cottonwood adapter reads the floor day by ROW (`floor_accounts`), three `first_row` tests, one clarifying sentence on three contract fields (no version, hash or enum change) | `DB171-1-AC1..AC3` PASS (95 tests), re-run on the landed tree | `d011411480` |

## 2. What stopped, and what it taught (read this first)

The AE stopped `DB-b-300` after Act 4, correctly, on three clauses; two were the issuer's errors, one a premise of the CTO's. The analysis is `GOLD_PAIR_ACT4_STOP_ANALYSIS_20261016.md` @`4052f6c08e`; the CTO ruled all three in ADDENDUM 1. (1) "Every value column identical" across a rewrite of a day was wrong: `market_value_eod` and `external_flow` are identical, and six other columns moved because their inputs arrived after the 11:41Z fire (holdings, the next-day neighbour for the guard); the bundle diff touches no value computation (36 lines, all history scope). The issuer had not diffed the bundles. "Same output on the same inputs" is INFERRED from the diff, not measured. (2) The PARTIAL count by "first positive day" was the order's wording; the producer's rule is the first ROW (2,851); gold cannot show one account the producer labels from silver. (3) The order assumed the served series read FULL; they read PARTIAL_HISTORY everywhere, so the 4,100 PARTIAL to FULL flips are the correction. **Client effect, stated by the CTO:** 4,100 49 Financial accounts lose "Returns from <date>." on the PROD Performance tab; 2,851 keep it.

A real defect found while specifying the hop-2 reader (row `IRPT_DASHBD-D2-S123`): `publisher.validate_filled_report` refuses the per-window `window_status` the table and the contract carry; the fix rides in `DB-b-302`.

## 3. The world, as the applier's records and the checkers' fresh reads state it (counts only)

- 49 Financial publish function: publisher 0.4.0, 1,024 MB, schedule ENABLED and untouched. 49 Financial gold function: 8,192 MB, schedule ENABLED and untouched; its role policy lists the filled prefix; `filled_report_values` holds ONE partition (2026-10-15, 4,694,024 rows).
- The new gold code and both schedules are LIVE: the Monday fires (11:41Z gold, 12:15Z publish) run the derived scope. **Not established:** that the scheduled path writes the filled stage (the Monday fire is its acceptance); the hop-2 reader (the stub still raises); a page render.
- A 49 Financial series of an account with a row on 2026-10-15 carries `history_scope_claim` = inferred; 3 accounts whose newest row is earlier carry none.

## 4. Rows and dispositions owed to the CVO

`IRPT_DASHBD-D2-S116`, `S117` (the 96a89eb451 merge damage and its extension), `S122` (three Cottonwood trading days with no gold partition: the adapter's presence hold), `S123` (the validator mismatch); the AE's rows `S99`, `S114`, `S121`, `S124`, `S125`; the worker rows of the earlier packet (W235-S1..S5, W236-S1/S2, W238-S1/S2, W239-S1, W240-S1/S2) and `S104` (evidence in the third packet). The issuer's own process misses this tick are in the analysis file and the row of record: a row commit refused by the row gate and left uncommitted for about an hour, blocking another seat's merge (committed `4052f6c08e`).

## 5. For the CVO

The criteria of DB-b-297, 299 and 303 are mechanical and were run by the issuer; DB-b-298 and DB-b-300 are WORLD and their checkers re-read the world. Judgment is owed on: whether the restated STOP clauses of `DB-b-300` (ADDENDUM 1) are the right reading, and on the dispositions above.

-- 2.0.0_SA_COO~D2
