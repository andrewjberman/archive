# AMGT_HARVST -- ROUND 48 DRAIN-END PACKET (L8 input), `2.0.0_SA_COO~H`, 2026-10-06 ~06:4xZ

**Round:** the round-47 analysis enrichment list (`ledger/ROUND_ANALYSIS.round47.md` @acc5c6e750). Decomposition section 61, issued
@986cef910c. **Class: LOCAL + SERVED** (au-3 is a served gold write under a never-widen pair).

## 1. The cells

| cell | result | evidence |
|---|---|---|
| `HVST-au-1` | **COMPLETE.** Worker ~96 @0e52b3639b + @d4adadab63. `Collector.upload` catches `subprocess.TimeoutExpired`, and `drive()` records `upload_timeout` as a transport-class stop (STOP + TRANSIENT). Past the budget it writes the stop to the checkpoint and prints SUMMARY. AC1 4/4. | task order record face; `test_au1_upload_timeout.py` |
| `HVST-au-2` | **COMPLETE.** Worker ~97 @5235d0ba0f + @079559d648. A would-be `listing_empty_200` on a name with `previously_stored > 0` reads `soft_block`, which is outside `SUCCESSFUL_RUN_STATUSES` and outside `STOP_STATUSES`. AC1 5/5; the mutant fails. | task order record face; `test_au2_soft_block.py` |
| landing | **LANDED @093da8e2b8** (15 files, dropped 0, foreign 0). The collector suite reads **665 passed, 3 skipped**; research harvest 355 passed. Both AC2 reds were the issuer's, and the issuer repaired them: the as-1 plants pinned 191 after at-5 (@2148adb922; at-5 had landed without the suite), and the ae4 stop-set pin gains `upload_timeout`. | rows Z-W96-S1/S2, Z-W97-S1 |
| `HVST-au-3` | **DONE: served gold rebuild #6** (item 3, asked by COO~Z msg 29872) under COO @e512987397 + CTO @0b26f965af; NEVER-2 entry opened and CLOSED. **Mention** `part-20261006T060121Z`: 33,665 rows. **Daily** `part-20261006T062025Z`: 59,148 rows. VERIFY holds on the written parts; no rollback. | `round48/au-3.act_20261006T052751Z.json`; `NEVER_WIDEN_HALF_COO_GOLD_REBUILD6.md` |

**au-3, the numbers:**
- **mention:** gone 0; added 2,623; changed 5,363, all class (c) hash-only; unexplained 0.
- **url:** on 31,919 rows, missing 0; `url == article_url(silver)` on every row. By publisher: barrons 712/712, bbg 5,102/5,102,
  sa 26,041/26,041, ft 30/930, wsj 34/880. Stored links only; no host was fetched.
- **daily:** gone 0; changed 28,070 by added mention plus 558 past-day coverage-only (d); OTHER 0.
- Dry run 1 broke the rebuild-#5 rule on classes (c) and (d). The pair accepted both, bounded, before the write.

**Item 4 (the resume)** is not a cell. It waits on Andrew (Z-S89; CTO @69ce080222). Every collection leg is STOPPED: concluded of
191 sa 9, barrons 130, bbg 104, wsj 154, ft 0; DECLARED SET EMPTY.

## 2. For the CVO

- **To grade:**
  - FWD-4 links: the url now on served mention rows (RESAPP reads it);
  - au-1 and au-2 (plants);
  - au-3 against its signed rule.
- **Still a qualified wait:** the collection outcomes (FWD-1, 3, 7, 9, 10, 11, 13, 14, 15), on Andrew's hand-solve and the SA account.
- **Surprise rows this round:** Z-W96-S1, Z-W96-S2, Z-W97-S1. All are INERT, and the issuer repaired them at the landing.

Push: read at send time.
