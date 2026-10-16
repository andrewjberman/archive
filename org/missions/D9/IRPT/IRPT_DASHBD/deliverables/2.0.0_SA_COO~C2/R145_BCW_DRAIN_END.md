# IRPT_DASHBD round 145, workstream B-CW (Cottonwood) -- drain-end packet (2.0.0_SA_COO~C2, 2026-10-16)

FWD-10 for Cottonwood, the first round of this seat's new assignment (Andrew's parallelization go through the CTO's ruling `CTO_RULING_DELL2_IRPT_PARALLELIZE_WORKSTREAM_ASSIGNMENTS_20261015.md` Move 2, msg 8741). Issuance `28182f03a2`; merges `656f1392ba` (worker ~414: DB-c-22) and `a04e8b1e80` (worker ~415: DB-c-23). Decomposition `org/missions/D9/IRPT/IRPT_DASHBD/decompositions/IRPT_DASHBD_DECOMP_B-CW.md` section 14. `round-close-check.py --project IRPT_DASHBD --round 145 --workstream B-CW`: `verdict=MAY-CLOSE` (2 orders, 0 judgment criteria). `DBC145-1-AC1`, `-1-AC2`, `-2-AC1`, `-2-AC2` PASS on the workers' trees (re-run by this seat; the checker recounts every S3 figure and re-reads every cited line); `-1-AC1` and `-2-AC1` PASS on the merged tree (the bounds arms need the branch point and read FAIL after the drain, by design). Push: integrator-only (LD-0367), not re-measured this packet.

## The three facts the CTO named, measured

- **The floor, 2026-07-10:** the first date of Cottonwood `filled_report_values`. `account_return_daily` starts 2013-04-03 and `holdings_performance_daily` 2026-06-10: three starts, not one floor (row `W414-S1`).
- **Three absent days:** 2026-08-19, 2026-09-24 and 2026-09-25, absent in `filled_report_values` (3 of 68 trading days since the floor) and in `account_return_daily`.
- **The twelve-day gap:** `account_return_daily` has no partition for the 12 trading days 2026-06-23 to 2026-07-09. `holdings_performance_daily` has none absent (88 partitions to 2026-10-14); `account_dim` holds 2026-10-13 and 2026-10-14.
- **Why the floor is there is NOT established.** Black Diamond `fact_allocations` reads 0 rows on 33 of 145 partitions (22 on non-trading days, 11 on trading days 2026-06-22 to 2026-07-09), and 2026-07-10 is the first partition after the last empty one; but silver also has rows on 38 trading days inside 2026-04-25 to 2026-07-09, so the empty partitions are a candidate explanation, and the rule that starts the gold series was not read (row `W414-S2`).
- **Account histories:** 835 accounts hold on the floor day; 166 accounts of the newest partition have no floor-day row (the partial-history case); 1004 accounts in `account_dim`. `account_return_daily` carries `day_quality`: on 2026-10-14, MEASURED 827 and NOT_MEASURABLE 37.

## What the page says today (read from the code, by cited line)

| the FWD-10 ACCEPT case | verdict | what the page does |
|---|---|---|
| a partial-history account | EXPLAINED | the dashboard prints one note when `history_scope` is not FULL (`DashboardPerformance.tsx:147`); the report path (headline, chart, accounts table) has none |
| a day that could not be measured | EXPLAINED | a count and a sentence per `day_quality` state (`:141-146`) and a tooltip for the hovered day (`:160`) |
| a fallback day | NOT_REACHED | PRD addendum v0.4 ruling 17 withdrew the substitution; the contract's `return_basis` is TWR and NOT_MEASURABLE only, so the FWD-10 ACCEPT clause and C-HONESTY's fallback footnote are stale |
| a window before the news data starts | NOT_REACHED on screen | the sentence "Market history is not available before ..." prints only in the export document (`PerformanceDocument.tsx:198`); the on-screen tab reads no news state |

Coverage members with a sentence on the dashboard: 3 of 8 (`PARTIAL_HISTORY`, `FLOW_UNRECONCILED`, `SOURCE_LAG`); `MISSING_HISTORY` in the export only; none for `FULL`, `NO_LOTS`, `UNCLASSIFIED_HOLDINGS`, `FEE_RAIL_UNUSED`. The Cottonwood `account_dim` adapter assigns `FULL`, `UNCLASSIFIED_HOLDINGS` and `PARTIAL_HISTORY`, but the page does not read it. The text "Time-weighted, net of fees" is still at `MethodAndSources.tsx:25` (a comment; the rendered label is composed at lines 33 and 37), and `holdings_gold.py` now carries `TIME_WEIGHTED`/`GROSS` at line 306 where the PRD cites `:259` NET (row `W415-S1`).

**The gap this makes visible, not named by either worker:** a trading day with NO partition at all (Cottonwood's 3 absent days and the 12-day run) is not a `day_quality` state, so no counter and no sentence on the path read can say "this day could not be measured" for it; only a day that has a row can read NOT_MEASURABLE. FWD-10's "which days could not be measured" is therefore unmet for exactly the days the CTO named. This is my reading of the two records together; it is a hypothesis for the build cell to confirm on the page with a window that spans an absent day, not a measured fact.

## What the CTO's half decides

1. **Endpoint wording (his):** FWD-10's ACCEPT and C-HONESTY still name "a fallback day" (withdrawn by ruling 17), and "the news data" names a state different from the account-history start (rows `W415-S2`, `S3`). A spelling or addendum ruling, or a ruling that these two clauses are met by absence.
2. **The round-146 enrichment list (proposed, build cells, by write surface S07):** (a) a coverage reader that returns the window's absent trading days from the calendar and the gold's partitions, and a sentence that counts them where the number is; (b) the window-clipping sentence on screen (the first data date, so "where the data starts" is told for Cottonwood's 2026-07-10 and for a partial-history account's own start); (c) the sentences for the four coverage members that have none, or a ruling that they are not shown; (d) the label correction in `MethodAndSources.tsx` and the test that still pins it (`W415-S6`), and the producer reason code printed on the accounts table face (`W415-S5`); (e) a test that opens the page for a Cottonwood account and a window spanning an absent day and reads the sentence, which is the EXERCISED proof FWD-10 asks for (portal work: the cells need a portal worktree and the usual portal gates, and the client-facing question of the portal push is Andrew's).
3. **Not a B-CW cell:** the cause of the 2026-07-10 floor (the rule that starts the gold series) is the producer's, owned by `~D2`'s `account_return_daily` build; the census states what it measured.
4. **Then 49 Financial and Inflection:** the same two read cells, once the Cottonwood pattern is built (your order of work).

## Rows

`D2-S101` carries the findings and the dispositions of workers 414 and 415 (`W414-S1`, `S2`; `W415-S1` to `S6`, all INERT observations): PRD wording to the CTO (`W415-S1` to `S3`), build candidates (`W415-S4` to `S6`), questions for the build (`W414-S1`, `S2`). Nothing ARMED or BLOCKING of this round.

## Issuer's own defects this round

The worktree provisioning used the new `--sparse-add` folders from the first cut (the round 126 gap did not recur). One slip: the 414 drain loop's first attempts hit other seats' merges and a fast-lane race, so the drain landed through the background run of the same loop; no commit was lost and the branch was already merged when the foreground retry found it gone.
