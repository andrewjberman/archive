# IRPT_YCDGEN round 4 -- drain-end packet (L8 compile input) for 3.0.0_SA_CVO

**Issuer:** `2.0.0_SA_COO~Y`, 2026-10-05 ~07:1xZ. **Round 4:** the CTO's round-3 analysis @033795b666, sections 2-3 (E1-E6),
issued in ONE issuance @f867ec3bca. **Risk:** WORLD.

## 1. Orders

| order | worker | merged | mechanical (re-run on the merged tree) |
|---|---|---|---|
| YCD-r-4 (call budget; keeper point objects) | ~1 @7f0d395090 | 0a439396d1 | r-4.AC1 PASS (16), r-4.AC2 PASS (2) |
| YCD-o-4 (held-data feed census; probe map) | ~2 @aeaf356634 | c6a2cbb058 | o-4.AC1 PASS (158 of 158 fed, all YCHARTS_SECURITY), o-4.AC2 PASS (6 requests for 99 holdings) |
| YCD-l-4 (the six statistics) | ~3 @869f31f05c | 57b511a031 | l-4.AC1 PASS (7) |
| YCD-m-4 (map label rule; 50 rows) | ~4 @c73a8fae30 | c3b266a60a | m-4.AC1 PASS (4), m-4.AC2 PASS (comparison 574, multi 423) |

4 of 4 orders are terminal (@0bdc75c6c2), and the research suite reads 104 passed. Two channel append conflicts were
resolved as base plus both appendices: every json block parses and every id is unique.

**Issuer rulings** are recorded in each order's drain note:
- r-4's two record choices are accepted.
- W2-S6 is accepted.
- W3-S5 is accepted.
- W3-S6: the conventions are confirmed (sample moments, Jensen x 12, Sortino about 0, interpolated 5th percentile, level-series inputs).
- W4-S5 and W4-S6 are accepted.

**JUDGMENT criterion owed at L9:** m-4.AC3, the re-grade of m-3.AC2 against the two PDFs: every row listed, labels read right,
no figure value.

## 2. The live close (issuer, inside the lease, solo gate clear each time)

| window | runs (request) | outcome |
|---|---|---|
| 1, 05:56Z and 06:08Z | A `YCD-R4-20261005T0552Z-A` (--end 2026-09-30), B `-B` (--end 2026-10-02); `close/measure_map_r4.json`, 6 calls each, 660 s apart | Both kept 5 answers and stopped at call 6, the AAPL `general_data` price probe (HTTP 500, BACKOFF). There was **no firewall challenge** in either run. `portfolio_level_series` was byte-identical in A and B (B reads `false`), as was `portfolio_info`. The AAPL `securities_info` probe answered 200 with a `security_id` |
| 2, 06:20Z | C `YCD-R4-20261005T0620Z-C`: `deliverables/maps/feed_probe_map.json` over Y-5's 99 holdings, 6 requests | **6 of 6 requests answered HTTP 400.** `general_data` returned `security_needed` and `metrics_needed`; `fund_data` returned "no valid items" (row **S8**) |
| 2, 06:32Z | D and E (`-D`, `-E`): `close/e5_dated_level_map_r4.json`, the level series without zoom, --start 2025-10-01, --end 09-30 then 10-02 | Byte-identical (E reads `false`). **`fund_data` ignores startDate and endDate**: 23,651 points through 2026-10-02 in every form (row **S7**) |
| 3, 07:07Z (~D's freed slot between Y-6 runs 2 and 3) | F `YCD-R4-20261005T0700Z-F` (`close/e5_zoom_5y_map_r4.json`: portfolio_info + portfolio_level_series_zoom at zoom=5y), then G `-G` 10 s later (`close/e5_zoom_max_map_r4.json`: the same two call names, zoom=max); 2 requests each | Both COMPLETE, all 200. **G reads `changed_since_previous: true` on `portfolio_level_series_zoom`** (F's answer `04f9de536ee8..`, G's `539579bbaee2..`, which is also run A's zoom=max answer) **and `false` on `portfolio_info`** (`df70928da81c..` in both) |

**What it measured:**
1. **E5's `--end` driver is false** (S7). The CTO's E5 premise (analysis :28-30) does not hold for this endpoint. The false
   arm is measured twice (B against A, E against D). **The true arm is realized by a lever that does change the answer under
   one call name** (window 3): zoom=5y, then zoom=max. This is the issuer's substitute for the `--end` driver, and S7 records it.
   The organic next-close run remains the ordinary check.
2. **E1's feed does not answer yet** (S8).
   - The holdings' ticker items are refused. The expand join puts ',' after an item that already ends ',,', and a ticker
     may not be the YCharts id.
   - The region and maturity column ids are not `general_data` metrics.
   - `securities_info` resolves a public ticker to its `security_id`.
   - No HELD_DATA element is fed. So **E6 is not rendered**: it would equal run 3's Overview, which is already stored and
     approved (FWD-1; Andrew's open of it is still not on record).
3. **The budget holds at 6 requests a window with 660 s between windows.** Five windows ran without a challenge, at 6, 6,
   6, 1 + 1 and 2 + 2 requests. The window length below 660 s is unmeasured. At 6 requests per ~11 minutes, a 26-call Overview
   needs 5 windows (about 45 minutes), and that bears on FWD-6.

## 3. Rows

- **S7** (E5's driver) and **S8** (E1's live probe): OBSERVATION, INERT, the issuer's.
- W2-S6, W3-S5, W3-S6, W4-S5 and W4-S6: ruled at the drain.

## 4. Carried to round 5 (candidates for the CTO's round-4 analysis)

1. **The feed's request form.**
   - Resolve each holding through `/securities/securities_info` to its `security_id`.
   - Fix the expand join (no extra separator).
   - Validate the metric ids on one public security inside the budget before a holdings run.
   - Split the region and maturity ids, or source them elsewhere.
2. **The six statistics' inputs:** wire a benchmark series kept by the run and a risk-free series Opal holds, per element (W3-S6).
3. **The budget's real cost to FWD-6:** measure the window length below 660 s (one probe pair), then design the Overview's
   calls to the fewest windows.
4. **A non-2xx answer's shape label.** The keeper labels a 400 JSON body DATA and a 400 text body IDENTIFIERS. The layout
   already reads non-2xx as not answered, so this is a label fix, not a data risk.
5. **E6** once (1) feeds.
