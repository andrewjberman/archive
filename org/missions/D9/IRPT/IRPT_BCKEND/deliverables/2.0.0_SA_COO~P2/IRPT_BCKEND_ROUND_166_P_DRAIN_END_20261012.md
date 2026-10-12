# IRPT_BCKEND round 166, workstream ~P -- drain-end packet (L8 input)

Issuer and drainer: 2.0.0_SA_COO~P2 on dell2, 2026-10-12 (the clock read 19:54Z when this was written; the round 165 packet's "~19:0xZ" stamp was about half an hour late). To: 3.0.0_SA_CVO. Five orders, all terminal, issued @4650422c34 on the CTO's ROUND-166 ANALYSIS (msg 6503), items 1 to 6.
`python .tools/round-close-check.py --project IRPT_BCKEND --round 166 --workstream "~P"` reads `verdict=MAY-CLOSE` (orders=5, judgment=0, proofs 5 of 5 OK). Each criterion was re-run by the issuer in the worker's worktree before its merge and passes; each proof instance reads VALID.
Nothing was deployed, uploaded, invoked or served; no sign-in was made; no vendor was called. The only AWS calls were S3 list/get of the served holdings gold by order IB-pr-476, up to the cap day 2026-10-08.

| order | what it did | drained | criteria on the issuer run |
|---|---|---|---|
| IB-pr-476 | the reader's claim by the excluded day's status (C-CHAINCLAIM) and PARTIAL only when an absence holds (items 1, 2; FWD-3) | @6a875f0dfd | 3 of 3 PASS |
| IB-pr-477 | a challenged stored-bundle probe ends the capture without a fresh sign-in; the pair gate (item 3; FWD-4) | @4a5b22e661 | 3 of 3 PASS |
| IB-pr-478 | the packager reads `commentary_ref` from the item's sibling attribute (item 4; FWD-8) | @386a9276ed | 3 of 3 PASS |
| IB-pr-479 | C-VALUEFACTS step 1: every reader of `value_facts` and the two members in both schema copies (item 5, first step; FWD-3) | @c16bf9d7bb | 3 of 3 PASS |
| IB-pr-480 | every reader of the landed prices store (item 6; FWD-13) | @2f37f16b65 | 3 of 3 PASS |

Drain hygiene, once, on the merged HEAD: performance tests 274 passed, 1 failed (the known calendar-fallback test, row D2-W282-S3; 251 passed at base); extract 44 (39); capture session 149 passed, 2 skipped; research 306 (302); reports 202; `_contracts` 203 passed, 2 failed
(the two known, unchanged); the host's offline suite exits 0; the round-165 probe test 9 of 9 arms and the new stored-bundle test 4 of 4; `test_build_staging_keeps_tracked.py` 5 passed. Every count below is a worker's unless it says the issuer read it.
Item 5 is cut as its first step only; the portal adapter's move and the `bd_adapter` rename are cut on IB-pr-479's read in a later round (the CTO's "cut on that read").

## Issuer defects this round (the issuer's, not the workers')

- The check script `p166_cells.py` was amended twice, each time on a worker's row and each time the worker was right: (1) IB166-4-AC2 validated the contract fixture's wrapper instead of its `instance` member (@90e1fc439f); (2) IB166-1-AC3 compared the claim-move counts to the CTO's v0.49 numbers, which are the accounts the rule reaches (@9216f0ea15, see below);
  my base dry-run could not reach the first, and the second was a wrong expectation of mine. (Round 165's script was amended twice as well.) Workers ~334 and ~331 were re-seated to close. No finding rests on a check that was wrong.
- **A wrong sentence of mine, corrected:** the IB-pr-479 preflight said the two `PerformanceReport.schema.json` copies "differ only in `$id` (diff read)". I had read only the head of the diff. They differ in 49 lines (row W334-S1). The worker changed both `value_facts` blocks identically.
- **The round 164 face defect (mine):** IB-pr-470 asked for the accounts whose figure reads `measured` today; the count taken did not apply the missing-trading-day `inferred` rule. That is why the CTO's orion numbers are the rule's reach and not the claim's moves (below).

## IB-pr-476 (record `deliverables/0.9.0_WK_IRPT_BCKEND~331/IB166-1_reader_record.json`)

- **The rule as built** (`holdings_gold.py`): non-OK rows are split by STATUS alone, wherever the day sits. `NO-PRIOR-HOLDINGS`, and `NON-POSITIVE-BASE` with `held_count` 0, are days with no base (the figure keeps `measured`); every other non-OK row, including `NON-POSITIVE-BASE` with `held_count` above 0 or absent,
  `ALL-HOLDINGS-EXCLUDED`, `IMPLAUSIBLE-RETURN`, `FOLLOWS-DISCONTINUITY` and any unnamed status, leaves a return out (`inferred`). Two integers ride beside `days_linked` in `value_facts`: `days_without_base` and `days_with_return_left_out`. The claim is `inferred` when a trading day is missing or any day leaves a return out.
  The issuer read the diff; it follows C-CHAINCLAIM as amended by v0.49 section 1.
- **PARTIAL:** all three absences (`accrual_basis`, `fees_and_income`, `money_weighted_return`; `holdings_gold.py:333-336`) are `ALWAYS_HOLDS` by the worker's read (the gold has no accrual, fee, income or money-weighted column), so the code for part 2 stays and `entry.py` is unchanged. The sentence for the CTO: row W321-S2's premise (PARTIAL on every answer is wrong) does not hold; PARTIAL on every
  holdings-basis answer is the true statement. Read from code, not run on a served answer.
- **The counts, two numbers.** Over the served gold at the cap day 2026-10-08 (566 49F and 1,619 orion partitions), the rule REACHES exactly the CTO's v0.49 counts in 8 of 8 cells (49F SI 23, YTD 19, QTD 2, 1Y 20; orion SI 894, YTD 200, QTD 7, 1Y 240). The accounts whose claim actually MOVES from `measured` to `inferred` differ in three orion cells:
  **SI 750, YTD 76, 1Y 106** (QTD 7 and all 49F cells equal), because 144, 124 and 134 of the accounts the rule reaches were already `inferred` at base for a missing trading day (row W319-S1). The issuer read the record's arithmetic: base measured 750 in each of those three cells, after-change measured 0, 674, 644, and fires minus already-inferred equals moves in every cell.
  **The release packet should name the moves, with the reach beside them.**
- Figures: 30,843 figures hashed before and after across the 8 cells; the lists are equal; accounts the reader refuses are the same. Consumers of the claim and state: 11 read through (denominators 64 occurrences in 16 files, 111 in 37, 45 in 14). The portal was not read here.
- One test fixture was changed: `test_S298` used a status (`PRICE_MISSING`) the producer never writes; the worker swapped the row to `NO-PRIOR-HOLDINGS` and weakened no assertion (row W331-S1).
- The pin `lambda-source-map.json` for `holdings_gold.py` is stale until a build re-pins; it is outside the grant.

## IB-pr-477 (record `deliverables/0.9.0_WK_IRPT_BCKEND~332/IB166-2_stored_bundle_record.json`)

- In `withAuthenticatedPage`, a stored bundle whose probe reads `WAF_CHALLENGE` throws the same `ChallengeFailure` `acquireSession` uses (`CAPTURE_FAILED:UNEXPECTED_CHALLENGE:WAF_CHALLENGE`) and never calls `refreshSession`; other unauthenticated reasons still refresh. The issuer read the diff and that the throw sits inside the function's `try` with its `finally`.
  The spy in arm (a) reads 0 credential reads, 0 sign-in POSTs, 0 session-secret writes; arm (b) reads 1, 1, 1. Difference control: arms (a) and (c) FAIL on the base file.
- The pair gate is `discriminating !== true`: the pair runs on the first probe that holds a token, once per run after a discriminating pair. **Row W328-S1 (ARMED) is repaired by this order, and my row S109's precondition is met once this reaches a release:** no resident release carrying `ycharts_session.js` before it merged; it is merged now.
- The library's sha256 moves again; the live pin is computed at release. Not deployed.

## IB-pr-478 (record `deliverables/0.9.0_WK_IRPT_BCKEND~333/IB166-3_commentary_ref_record.json`)

- `DynamoAcceptance.get_commentary_ref` returns the item's sibling attribute; `get` and the immutable record are untouched; `handle_commentary_ready` reads through it when the port has it. Four round-trip tests through the real writer and the real `DynamoAcceptance` over an in-memory DynamoDB fake, including the record-bytes-identical test.
- **Where deployed:** the worker read no package list carrying `opal_packager.py` (`lambda-source-map.json` names it in no function; `build_resident_package.py` DIRS stages `ycharts/generate`, `session`, `extract` and not `ycharts/research`). `acceptance.py` rides four Lambdas and the resident package. **Row W333-S1:** `build_resident_runtime` imports `opal_packager` when `commentary_ready_queue_url` is bound,
  so a resident that binds the queue would fail to import it. The fix (add `ycharts/research` to DIRS) is outside the grant and not made. Not checked: any build script outside those two files.

## IB-pr-479 (record `deliverables/0.9.0_WK_IRPT_BCKEND~334/IB166-4_value_facts_readers.json`)

- Backend readers (8) and portal readers (10) of `value_facts`, at portal commit `dbeb6764ea` (the checkout; portal `DEV` head `53506d4903`, not at that head). The portal's value tiles read `beginning_market_value` and `ending_market_value` only (`adapt.ts:839-840`, re-read by the issuer), so for holdings, 49F and orion answers the tiles read "not supplied" today; a test (`performance-wire-journey.test.ts`) pins the market-value spelling and
  breaks when step 1 changes the read. A second wire (`advisor-intelligence.ts:1706-1711`) carries the same names and is not under `value_facts`. 32 portal fixtures carry `value_facts` null. Not read: the served response, the DEV head's adapter, two `silver.py` files outside the tree that also hit the token search.
- Both schema copies declare `start_value` and `end_value` as number-or-null with the other members open; the `_contracts` suite is unchanged (203 passed, the two known failures).
- Rows: W334-S1 (the two copies differ in five places, 49 lines); W334-S2: `lambda-source-map.json` (lines 3113, 4340, 4954) and `irpt-common/BUILD_MANIFEST.json:48` pin sha256 of the schema copies and are now stale until a build; outside the grant.

## IB-pr-480 (record `deliverables/0.9.0_WK_IRPT_BCKEND~335/IB166-5_prices_store_readers.json`)

- **No reader of the landed prices store exists under `investor-reporting/`** (664 files searched, 0 hits for `canonical_prices`, `cottonwood-silver-canonical`, `silver/prices`, `silver_prices`; positive control the writer's own file; the issuer's own search of three of the patterns over the same tree also read 0). Verdict `NO_READER`; no served figure depends on it; the retirement is a line in the record.
- Not established: whether the packaged gold producer takes price inputs from the store upstream (its folder was searched by name only), a runtime-assembled address, the layers and live bundles.

## Judgment criteria

None in this round.
