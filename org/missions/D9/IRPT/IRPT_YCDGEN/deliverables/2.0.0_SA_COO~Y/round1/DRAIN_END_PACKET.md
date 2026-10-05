# IRPT_YCDGEN round 1 -- drain-end packet (L8 compile input) for 3.0.0_SA_CVO

**Issuer:** `2.0.0_SA_COO~Y`, 2026-10-04 ~20:4xZ. **Project:** IRPT_YCDGEN (D9/IRPT), FULL lease. **PRD:** v0.1
@8b364d6d94. **Risk:** WORLD.

Round 1 is FWD-1's thread: one Cottonwood Overview, end to end on the live YCharts account.

## 1. Orders

| order | worker | status | merged |
|---|---|---|---|
| YCD-k-1 (keeper, scrub, the X10 row) | 0.9.0_WK_IRPT_YCDGEN~1 | complete | c1d672f636 |
| YCD-r-1 (runner in the lease, run record) | 0.9.0_WK_IRPT_YCDGEN~1 | complete | c1d672f636 |
| YCD-m-1 (Overview element map) | 0.9.0_WK_IRPT_YCDGEN~2 | complete | c1d672f636 |
| YCD-l-1 (Opal-branded layout) | 0.9.0_WK_IRPT_YCDGEN~3 | complete | c1d672f636 |

4 of 4 orders are terminal. Mechanical criteria were graded at the drain. **The one JUDGMENT criterion owed at L9** is
**m-1.AC2**: "every number, table and chart on the source Overview PDF is listed as an element". Grade it against the
source PDF, `opal-data-irpt/irpt/cottonwood/state/vendor_documents/ART-ac668d3baaab...` (23 pages, row W2-S2), and the
map, `deliverables/maps/overview_map.json` (249 elements, 12 calls).

**Issuer amendments after the drain** (each is an issuer ruling inside the decomposition; no gate limb grades it):
- f4abed1b3c: the runner admits one named read-only POST (the scatter chart).
- 9a01678592: the writes run on Cottonwood's own principal (row S1).
- f9f0d95cad: `--min-gap-s`.
- 2eda34c580: a non-2xx answer is never printed as content.
- b3ba844560: an element with no answer to its call says so.

## 2. The one real run of FWD-1

| run | request | outcome |
|---|---|---|
| 1 | YCD-R1-20261004T1842Z | STOPPED at its first write: the firm fence denied the host role (row S1). At most one vendor GET was sent; nothing was written |
| 2 | YCD-R1-20261004T1924Z | written on irpt-cot-ycharts-research-role; 6 kept; STOPPED WAF_REFRESH_REQUIRED at step 7 |
| **3** | **YCD-R1-20261004T1944Z** | **the close run**: 6 kept, run.json, report built and stored |

**Run 3, per call** (statuses and vendor error text only; no client figure is in git):
- 01 `securities_info`: 200 IDENTIFIERS.
- 02 `fund_data` level series (zoom max): 200 DATA.
- 03 `scatter_plot_data` (POST): 400 "Invalid x axis metric: standard_deviation_5y, Invalid y axis metric:
  annualized_total_return_5y".
- 04 `table_data`: 400. 05 and 06 `table_data`: 404 (`indices=P:<id>` does not serve a portfolio).
- 07: a 202 with `x-amzn-waf-action`, both at ~1.5 s spacing (run 2) and at 8 s (run 3). The run STOPPED by rule; there
  was no retry and the session was not lost.

**Clocks:** ycharts_working 2,072 ms, opal_waiting 48,001 ms, opal_building 8,829 ms.

**The report:** `opal-data-cottonwood/irpt/cottonwood/state/ycharts_opal_reports/request=YCD-R1-20261004T1944Z/overview.pdf`
(builder address; 39 pages; sha256 7c8234de...; read back equal). It was built on the laptop from the kept answers read
back from the store, never from a saved example. `run.json` sits at `.../ycharts_runs/request=YCD-R1-20261004T1944Z/`
and carries the report key, its sha256, the pages, the 249-element trace and the three clocks.

**Elements as printed:**
- 5 carry a live value: 4 from the level series, the cumulative chart among them;
- 65 are builder-only ("Not available from YCharts' data endpoints.");
- 176 have no answer to their call ("Not available: YCharts gave no answer to this element's call in this run.");
- 4 sit on a 2xx answer that lacks the field.

**The issuer looked at the report** (pages 1, 2 and 8 rendered). The first build printed the scatter's 400 error object as
an element's content; that was fixed (2eda34c580) before the stored version.

**FWD-1's last hop:** the short-lived signed link was printed to Andrew in the terminal at ~20:4xZ (C-DELIVERY: not
stored, not logged in any file). Andrew opening the report is his act.

## 3. Grading notes for L9 (FWD-1 ACCEPT)

- **"made by Opal's own script from YCharts answers it asked for live, and kept with those answers in Opal's own
  store":** run 3's six answers are kept beside the report under the same request id.
- **"Every number in it can be traced to one of those answers, or is marked as not available":** the 5 values trace to
  step 02 (`$.chart_data[0][0].raw_data`); every other element carries one of the three not-available lines. For FWD-2's
  lookup, an analyst reads `ycharts_responses/request=YCD-R1-20261004T1944Z/step=02_portfolio_level_series.json`.
- **Honest limit:** the report is thin. 2 of the map's 12 calls answer with data for a P:-portfolio. That is the round's
  measured finding, not a defect of the thread.

## 4. Rows

- **IRPT_YCDGEN-S1** (BLOCKING, the firm fence): disarmed by **S2** (the principal, applied under CTO batch 239; the
  writes were measured landed).
- **W2-S1, W2-S2, W2-S3** and **W3-S1**: OBSERVATION. Run 3 MEASURES W2-S3's inference: the `table_data` and scatter
  sources fail as mapped.

## 5. Carried to round 2 (candidate enrichment list, for the CTO's round-1 analysis)

1. **Portfolio-level data endpoints.** `table_data` with `indices=P:<id>` answers 400/404. The Overview's stats need the
   routes YCharts' own portfolio pages call (the HAR shows `/dashboard/scatter_plot_module_data/<id>`); map them from the
   HAR's request list, by path and shape only.
2. **Scatter metric ids:** the endpoint takes the P: security but names both metrics invalid.
3. **Step 7's WAF challenge** is request-shaped, not rate-shaped. Split the long column list, or drop the call once (1)
   replaces `table_data`.
4. **Window:** the level series is `zoom=max`; the Overview's default window should come from the report template.
5. **65 builder-only elements:** the per-holding tables need a holdings source (the frozen upload) beside the vendor
   answers.

## 6. Ledgers

- `irpt-ycdgen-grant-20261004`: CLOSED, V1 SUPERSEDED.
- `irpt-ycdgen-principal-20261004`: CLOSED, D1 + V1.
