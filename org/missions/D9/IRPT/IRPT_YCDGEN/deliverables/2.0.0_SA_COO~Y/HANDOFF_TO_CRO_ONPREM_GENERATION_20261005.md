# HANDOFF -- the YCharts report generation, end to end, for an on-premises rebuild

**From:** 2.0.0_SA_COO~Y (IRPT_BCKEND ~Y Analysis lane; IRPT_YCDGEN issuer). **To:** 4.0.0_SA_CRO. **Date:** 2026-10-05.

**Order.** Andrew-direct, 2026-10-05 ~14:3xZ (verbatim @a812d50ff1:
`org/missions/D9/IRPT/IRPT_YCDGEN/deliverables/2.0.0_SA_COO~Y/ANDREW_DIRECT_20261005T143xZ_INSOURCE_YCHARTS_GENERATION.md`)
and ~15:5xZ. Andrew asks for a text handoff "which details the whole process, any and all scripts and src paths referenced,
generations for each of the three variants referenced by path, essentially a comprehensive overview for the inputs of the
process and the current process itself ... so that the CRO should use this information to assess how to run all of this on
premises. If there is information outside of Opal Premises (e.g. holdings we don't have) then maybe there is a fast/light
mechanism to get the relevant information pieces either through some online channel or BBG. The overarching premise is
that we want to be able to do this fast and light and onsite." He also asked that it carry "as much structured data
contracts as we can possibly provide ... so we know the topography".

**Routing.** 1.0.0_SA_CTO 105307: your brief addendum comes first, then the CTO's endpoint revision (IRPT_YCDGEN PRD v0.2).

**Conventions.**
- Paths are repo-relative to `C:/Users/AndrewBerman/Desktop/ajb_workspace`.
- S3 is written `bucket/key`.
- MEASURED means read from a live answer or a HAR. EXTENDED or INFERRED means constructed or read from labels; each is
  marked where it applies.
- No figure value, ticker list, client name or credential appears here.

---

## 0. The answer in five lines

1. **YCharts generation is a remote control.** Opal sends holdings, settings and cover fields, and gets back identifiers, a
   status and a PDF link. Every analytic in the report is computed inside YCharts from YCharts' data (section 3).
2. **Each report variant has been mapped element by element** (Overview 254, Comparison 574, Multi 424 elements) to the
   data it needs. In-house, an element needs one of four things: our own input; layout or boilerplate; series math over
   price/total-return histories (Opal already computes this, in `research/layout_overview.py`); or **holding reference
   data**: fund look-through exposures, fund fundamentals and prospectus fields (section 5).
3. **The only real dependency to replace is that reference data, plus long price histories.** Opal holds part of it today
   (section 6). For the rest there are fast, light channels: Bloomberg reference fields that are served today; issuer
   files; public filings (SEC N-PORT / N-CSR / prospectus); FRED (section 7).
4. **What it costs today, measured:**
   - ~15 of every ~18 minutes is a fixed wait for YCharts' firewall window.
   - The firewall challenges the 7th request in any window.
   - The stored session is evicted whenever an Opal employee logs in to the shared account: twice today, and one job
     failed (section 8).
5. **In-house:** no session, no firewall and no vendor wait. One holdings read, one data-mart read, compute, then render (an
   Opal-branded HTML-to-PDF renderer already exists). Seconds per report, not minutes.

---

## 1. Inputs to the process

| Input | Where it comes from | Contract / path | Notes |
|---|---|---|---|
| Client holdings file (CSV or XLSX) | the portal's upload page | `docs/contracts/investor-reporting/v1/AnalysisUploadRequest.schema.json` (Appendix A) | Client data. Corrections can be applied: TICKER_NOT_FOUND, TICKER_AMBIGUOUS, ... |
| Upload result / normalized portfolio | intake Lambda (`infra/aws/lambda/investor-reporting/intake/uploads.py`, `upload_entry.py`, `parse.py`, `template_reader.py`, `security_resolution.py`, `upload_resolution.py`, `resolution_broker.py`) | `AnalysisUploadResult.schema.json`; the normalized input `irpt-normalized-portfolio.v2` (`ycharts/generate/normalized_input.py`) | Resolution runs on the resident host (`IRPT_RESIDENT_RESOLVE*` journal lines). Untracked rows are named to proxies (SGOV etc.) on the page |
| Submission: variant and comparison keys | the portal's submit | `AnalysisSubmissionRequest.schema.json` (variant `auto/overview/comparison/multicomp`), `RequestComposition.schema.json`, `ComparisonCatalogue.schema.json`; `ycharts/generate/comparison_catalogue.py`, `submission.py`, `submission_service.py`, `request_composition` | Comparison keys come from the maintained catalogue (e.g. Opal Long-Term, Opal Ultra Long-Term, IWM) |
| Report settings (7) | `ycharts/generate/recipe.py:75-89` | Section 2, call 2 | management_fee 0.003, rebalance quarterly, reinvest_dividends false, start_of_series oldest, level_as_of_type prior_close, tax_status non_qualified, benchmark ^SPXTR |
| Cover/profile fields | the advisor's profile (`frozen_worker.py:85`, `owner_reads.py`) | Section 2, call 5 | title, prepared for/by, organization, contacts, custom field, disclosure footnote |
| Held holdings data (Opal's) | DynamoDB `irpt-requests`, `irpt-jobs`; S3 composition artifacts | `HoldingsSnapshot.schema.json`, `RequestComposition.schema.json` | The research runner reads a frozen request's holdings with `runner.read_holdings` (contract 3.2) |

**Reference cases used throughout:**
- Y-5's frozen input REQ-a618aa83407689bc95193a01: 99 rows, the easy file, TIMXX named SGOV.
- Y-6's page cases: Aproxy and Bproxy (the easy file), Cproxy (Multi-Comp), Dproxy (the Stevens file), typoAccept (the typo
  file).
- The source files are in Andrew's Downloads. They are client data and are not copied into the repo.

## 2. The current production process (the served path) and its YCharts calls

**The flow:**
1. **Portal (DEV, `portal/`, port 5174):** the user uploads, corrects, picks the variant and comparisons, and submits.
2. **The routes:**
   - Upload, submit and comparisons go to the `irpt-ycharts-generate` Lambda (source `infra/aws/lambda/investor-reporting/ycharts/generate/`, entry `entry.py`).
   - History and status go to `irpt-status` (source `infra/aws/lambda/investor-reporting/ops/`: `status.py`, `owned_requests.py`, `prospect_dates.py`).
   - Holdings and directory go to `irpt-holdings` and `irpt-directory-search`.
   - The route table is `docs/contracts/investor-reporting/v1/routes.json`.
3. **The job:**
   - Acceptance writes `irpt-requests` and `irpt-jobs` (`acceptance.py`, `durable_job.py`).
   - The message goes to SQS `irpt-generation` (`infra/aws/terraform/investor-reporting/core/sqs.tf`; maxReceiveCount 5).
4. **The resident worker:**
   - It runs on EC2 `i-0167fd745ad906a66` under `irpt-analysis-resident.service`; the root is `/opt/irpt-resident/<commit>-stNN`, currently `3f29017cfc-st21`.
   - Its code is `ycharts/generate/resident_main.py`, `resident_worker.py`, `recipe.py` and `transport.py`.
   - The session lives in `ycharts/session/`: `resident_session.py`, `broker.py`, `operation_lease.py`, `deadline_transport.py`, `host_capture.py`.
   - Terraform: `infra/aws/terraform/investor-reporting/ycharts/` (`instance.tf`, `resident.tf`, `iam.tf`, `generate.tf`, `ssm.tf`).
5. **The YCharts calls** are listed in the table below. The live order is in `resident_worker.py:264-304`.
6. **Retention and certification:**
   - The vendor PDF is kept as ORIGINAL_VENDOR_PDF.
   - The extractor (`ycharts/extract/extract.py`, `certify.py`, `publication.py`, `fonts.py`) re-reads every scalar section at its page and coordinates. That gives EXTRACTION_EVIDENCE and a certified AnalysisReport (`AnalysisReport.schema.json`).
7. **The page:** `irpt-status` serves READY, and the page opens the report's sections (`StatusEnvelope`, `PublicStatusEnvelope`, `OwnedAnalysisRequest*`). Export runs through `ExportBundle` / `ExportReceipt`.

**The YCharts calls, field level** (source `recipe.py`; fixtures `ycharts/generate/fixtures/har/`, see `FIXTURE_MANIFEST.json`):

| # | Call | Request | Response (fields the code reads in **bold**) | Fixture |
|---|---|---|---|---|
| 0 | GET `/custom_pdf_reports/generate/{template_id}`: the template; also proves the session. The id follows the comparison count: 0 -> 14141822 Overview, 1 -> 14141824 Comparison, 2-5 -> 14141847 Multi (`recipe.py:138-165`) | none | **`id`** int, **`report_type`** str, **`sections`** array, `orientation` str, **`performance_disclosure_footnote`** str | templates.json MEASURED |
| 0b | GET `/securities/securities_info?securities=...` (only when an ETF comparison is picked, R:416-447) | query `securities` | list of candidate rows | none |
| 1 | POST `/model_portfolios/fixed/holdings_upload/client` (**holdings upload**) | multipart; file part `holdings` = `IRPT_HOLDINGS.csv`, text/csv; columns `Symbol,Dollars,Cost Basis Per Share,Performance Proxy`; per row `{identifier},{USD to the cent},,` (R:479-506) | **`status`** "ok", **`errors`** [], **`rows[]`** {**`security_id`**, **`display_security_id`**, **`display_name`**, **`weighting`** number}, **`weight`** "Dollars", **`upload_record_id`** int, `isExtractedHoldings` (R:513-530; the echo is checked to the cent) | upload_ok.json EXTENDED (keys MEASURED) |
| 2 | POST `/model_portfolios/fixed/` (**portfolio save**) | multipart, two JSON parts. `portfolio`: `name` (opaque "IRPT {request} r{rev} {fingerprint12}"), `upload_record_id`, the 7 settings, fixed literals (`description`, `benchmark_creation_type`, `management_fee_frequency` annually, `label` client_portfolio, `level_type`, `weight_type` Dollars, `show_*`, `uses_legacy_data`, `rebalance_cash`) and nine nulls. `items[]` from call 1's echo: `name`, `weighting`, `weight_text`, `security_id`, `display_security_id`, nulls (R:560-630) | 201 **`model_portfolio_id`** (+ `parent_folder_id`); 422 `{error_messages:[str]}` live (the fixture's `errors.management_fee[]` disagrees) | create_201.json MEASURED |
| 3 | GET `/model_portfolios/{id}/status`, then GET `/model_portfolios/fixed/{id}` (**status read-back**; ONE status GET per receive) | none | status 200, or 202 while calculating: **`{status}`** calculating/available; a 202 + `x-amzn-waf-action` is the firewall. Saved: **`portfolio.{7 settings, model_portfolio_type}`** (R:686-768) | status_ok.json EXTENDED |
| 4 | POST `/custom_pdf_reports/validate_report_securities/{template_id}` (**security check**) | JSON `{security_ids: ["P:{id}", comparison ids...], modules: null}` (R:778-806) | 200 `{}` | validate_200.json MEASURED |
| 5 | POST `/custom_pdf_reports/{template_id}` (**generation**) | JSON, 34 keys (R:809-949). Data-dependent: `security_ids`, `report_title`, `prepared_for`, `prepared_by`, `organization`, `contact_email`, `contact_phone`, `contact_url`, `custom_field`, `performance_disclosure_footnote`; inside `generationModalsState`: `coverPageInfo`, `primarySecurity`, `secondarySecurity` (Comparison), `comparisonSecurities[]` (Multi), `reportTitle`, `selectedReport` (call 0's document) | 201 **`report_url`**, `zip_url` (never fetched) | generate_201.json MEASURED |
| 6 | GET the signed `report_url` (**download**; no cookies, allow-listed hosts; `transport.py:335-382`, `session/deadline_transport.py:87-99`) | none | 200 application/pdf (`%PDF-`, `%%EOF`, size, sha256) | report.pdf EXTENDED |

**What crosses the wire:**
- Ours, going out: holdings, settings, the opaque name, comparison ids, cover fields.
- Back: identifiers, a status, URLs, the vendor's reading of our holdings (call 1), our stored settings (call 3), and the PDF.
- What the PDF echoes from our inputs: cover fields, holdings symbols and weights, comparison names, and indirectly the
  settings ("As Of: Custom", Type).
- **Every other number is computed in YCharts.**

**Code findings for the rebuild:**
- `job.py`'s older validate sends only `P:{id}` (the resident path sends the comparisons too).
- Nothing deletes the portfolios Opal creates in YCharts, so they accumulate there.
- The zip is never used.

## 3. The research path (IRPT_YCDGEN): reading YCharts' data, and Opal's own report

**Purpose (Andrew's original order, 2026-10-03):** "run the api calls, persist and categorize the response shape per api
call ... run the generation with our own custom script that uses the same endpoints but opal branded".

**Code** (`infra/aws/lambda/investor-reporting/ycharts/research/`):
- `runner.py`:
  - plans the calls from a map (`plan_calls`; `expand` over holdings);
  - enforces the call budget (`split_windows`; at most 12 requests a run, PLAN line);
  - takes the provider lease, keeps each answer, and writes the run record and the previous-run index;
  - writes a stop row on a firewall STOP;
  - read-only POSTs only.
- `keeper.py`:
  - scrubs and keeps each answer (contract C-KEEP), with its shape class (IDENTIFIERS / DATA / DOCUMENT) and sha256;
  - records `request_sha256`, and sets `changed_since_previous` to true / false / no_previous / request_changed.
- `lookup.py`: the one-command lookup of a kept call (`--firm --request --call`).
- `map_pdf.py`: builds an element map from a YCharts PDF (labels, coordinates, data rows masked; no figure values).
- `layout_overview.py`:
  - Opal's computed path: 3.4 statistics and the 4.3 six (alpha, beta, Sharpe, Sortino, monthly VaR, max drawdown), with
    a 3.5 trace;
  - the OPAL_HELD path (`load_held_rows`);
  - the Opal-branded HTML builder; `render()` produces the PDF through `render_pdf.cjs` (playwright-core / Chromium).
- `held_data.py`: the Opal-held census and `value_of` (renormalized over held holdings, with its method).
- `file_stop_row.py`: files a stop row.
- Tests: `tests/` (135 pass).

**Maps and records:**
- Maps (`org/missions/D9/IRPT/IRPT_YCDGEN/deliverables/maps/`):
  - `overview_map.json` (8 calls, 254 elements);
  - `comparison_map.json` (24 calls, 574 elements);
  - `multi_map.json` (24 calls, 424 elements);
  - `overview_coverage.json` (176 rows with class and feed);
  - `coverage_probe_map.json` and `feed_probe_map.json` (probes).
- Decompositions: `org/missions/D9/IRPT/IRPT_YCDGEN/decompositions/IRPT_YCDGEN_DECOMP*.md`. Contracts C-KEEP, C-RUN,
  C-MAP, 2.5-2.7, 3.1-3.5, 4.1-4.4 and 5.1-5.5 are defined there.
- PRD: `org/missions/D9/IRPT/IRPT_YCDGEN/prd/IRPT_YCDGEN_PRD.md` (v0.1; FWD-1 to FWD-7).
- Issuer close scripts and live-run records: `org/missions/D9/IRPT/IRPT_YCDGEN/deliverables/2.0.0_SA_COO~Y/close/`. These
  include `*_host.sh` (bundle by key and sha256, then the runner as the resident's user), `e6_render_store.py` (render,
  store and sign), and `YCD-*_host_run.txt`.
- Host tooling: `org/tier1_exec/2.0.0_SA_COO/deliverables/IRPT_MVP_Y/live_walk/`:
  - `host_read.py` (SSM), `resident_journal.py`, `job_terminal_wait.py`, `backend_join.py`, `case_trace.py`;
  - `job_status_route_read.py`, `history_route_read.py`.
- Earlier research: `docs/research/investor_reporting_ycharts_20260910/`, `..._auth_20260910/`,
  `..._cloud_20260911/`, `..._variants_20260911/`.

**YCharts' data endpoints and the answer fields read** (MEASURED: status and shape in the kept answers):

| Endpoint | Request params (names) | Answer fields read | Measured behaviour |
|---|---|---|---|
| GET `/securities/securities_info` | `securities` | `$..name`, `security_id`, `display_security_id` (a list of 1 per id) | 200 for a public ticker and for a model portfolio |
| GET `/charts/fund_data.json` | `securities`, `calcs` (`id:level,...`), `zoom`, `maxPoints`, `partner`, `startDate`, `endDate` | `$.chart_data[0][0].raw_data` ([epoch_ms, value] pairs; 23,651 points for the model portfolio, 1962 -> last close) | **ignores startDate/endDate** (row S7); 400 "no valid items" for holdings items as sent (S8) |
| GET `/charts/general_data.json` | `securities`, `metrics`, `xAxis` (`metrics` or `time`), dates | `$.chart_data[*]` | 200 for the model portfolio (xAxis=metrics); 500 for a public ticker at xAxis=time; 400 security_needed / metrics_needed for the holdings probe (S8) |
| POST `/charts/scatter_plot_data.json` | `securities`, `xAxisMetric`, `yAxisMetric` | `$.data.series[*].data[*]` {x, y, name} (point objects) | 200 for a model portfolio with documented metric ids |
| GET `/indices/table_data` | `indices`, `columns` (calc names) | `$.indicesData[0].data[?(@.calc_name==...)].calc_raw_value` | **404 for holdings' tickers and for `P:<id>`** (row S6) |
| firewall | -- | 202 + `x-amzn-waf-action` | the 7th request in a window (122 s < window <= 373 s) |

**Research store contracts:** Appendix B.

## 4. The generations of each variant, by path

**Vendor PDFs, kept as ORIGINAL_VENDOR_PDF.** All three were made from the easy file's holdings. Buckets: firm `cottonwood`;
artifacts in `opal-data-irpt`.

| Variant (template) | Request | Vendor PDF (S3 key; bytes; sha256) | VersionId | Extraction evidence (artifact) |
|---|---|---|---|---|
| 1 Overview (14141822) | REQ-777d75467393aafe6f351cc5 (Y-6 run 1, READY 05:18:26Z) | `opal-data-irpt/irpt/cottonwood/state/vendor_documents/ART-db3defc9e22639f5b2a0c20d1d1a4c88af79a49b756335930f0f00e40d9e9395/17145b000149f4bfcfce6685b807a54963071e2f323e4bed3f4ca38ba6ebbb89.pdf` (652,887 B) | `PBDPGIx4fCOBb7nJZjEmyzPmPlBGKmDK` | census ART-3ac0e440...; publication evidence ART-143ba8d2... |
| 2 Comparison (14141824) | REQ-7ea49c2d9b27957d0ea8888f | `opal-data-irpt/irpt/cottonwood/state/vendor_documents/ART-2ef3ef7d42a18bd62cd5ffddae8def8c78db3f057a2ae75cc185248eda32a093/7f8ed86e548bc6be0323224e87553cf2ce08683da0d81fc3a9219e824393f9b5.pdf` (827,312 B) | `ZG118xXXEh2pCZozNhAnF9Dw9C3UOujR` | census ART-76f2d51f...; publication evidence ART-0ec0a9f8... |
| 3 Multi-Comp (14141847) | REQ-329a56182b2668d44a28c8d7 | `opal-data-irpt/irpt/cottonwood/state/vendor_documents/ART-08ab7d1af9106539b01660f2f62de5acc7ea868556e148c5adf16f0e6188ecb5/9b59d738c23c241124e64b838d627a9afbac5165bb24f20ef41cb7044f2b5eba.pdf` (937,121 B) | `r317DqU2TxVMuwvtLV6WAI1fFQEo2lNv` | census ART-a08b0ede...; publication evidence ART-2d484cdd... |

**More vendor generations:** Y-6 today. Overview runs 1-2, Comparison runs 3-4, Multi runs 5-6. Their REQ ids and backend
timings are in `org/tier1_exec/2.0.0_SA_COO/deliverables/IRPT_MVP_Y/Y6/Y6_BACKEND_SUMMARY.md`, and each job row's
`checkpoint_pdf` names its PDF the same way. Locate any by `case_trace.py <tenant> <REQ>`.

**Opal's own generations** (`opal-data-cottonwood/irpt/cottonwood/state/`):
- `ycharts_opal_reports/request=YCD-R1-20261004T1944Z/overview.pdf`: the Opal-branded Overview of run 3 (39 pages).
- `ycharts_responses/request=<REQ>/step=NN_<call>.json`: the kept answers, every research run. Examples: YCD-R3-20261005T0219Z
  (holdings, 6 kept), YCD-R4-*, YCD-R5-E4-20261005T1215Z, WAF-PROBE-20261005T1254Z-W330.
- `ycharts_runs/request=<REQ>/run.json` and `stop_row.json`: the run records.
- `ycharts_runs/index=latest/latest_by_portfolio.json`: the previous-run index.

## 5. Each variant cross-referenced, and what each element takes in-house

Classes per element: (a) our input echoed; (b) boilerplate, layout and dates; (c) computed from series; (d) holding
reference data.

| Class | Overview (254) | Comparison (574) | Multi (424) | In-house today |
|---|---|---|---|---|
| (a) | 9 | 15 | 10 | yes |
| (b) | 51 | 61 | 167 (102 page-footer) | yes (Opal-branded renderer) |
| (c) | 30 | 103 | 86 | methods yes; series data partial (section 6) |
| (d) | 164 | 395 | 161 | partial (section 6) |

**Examples:**
- (a) p2.e05 "Port. Advisory Fee"; p14.e03 settings.
- (b) title, disclaimers, as-of dates.
- (c) p2.e04 cumulative chart; p7.e02-e08 risk table; p12.e04 holdings' annualized returns.
- (d) p2.e09 net expense ratio; p4.e32 region exposure; p6.e05 bond maturity; Comparison p17.e12 top-25 underlying holdings.

**(c) needs, per holding and per comparison key:**

| Series | Frequency | History |
|---|---|---|
| total-return level (dividends reinvested) | daily | at least 15 years + 1 month; full history, since inception, calendar years 2016-YTD |
| price-only close, plus the inception date | daily | full history |
| NAV (funds) | daily | full history |
| benchmark ^SPXTR total-return level | daily | at least 15 years |
| risk-free 3M T-bill (FRED DGS3MO) | daily | at least 15 years |

The portfolio series is buy-and-hold over our amounts from the latest common start.

**(d) needs, per holding, as a current snapshot:**
- Asset allocation: 6 sleeves, plus net stock/bond/cash.
- Equity: market-cap buckets (5), 3x3 style box, Morningstar sectors (11 + 3 super-sectors), 64 regions/countries.
- Bonds: bond sectors (6), credit quality (8), maturity buckets (16), and average credit, YTM, current yield, effective
  duration, coupon and price; bond and stock holding counts.
- Fundamentals: net and gross expense ratio, distribution and dividend yield, number of holdings, and weighted P/E, P/S,
  P/B, market cap and debt/capital, ROA, ROE.
- Holdings: each fund's top-25 constituents, with weights, prices and returns.
- Prospectus: front, deferred and redemption loads, 7- and 30-day SEC yield (subsidized and unsubsidized), waivers.

**Caveats:**
- All 1,252 placements are INFERRED from printed labels.
- Only the Overview has a coverage census; the Comparison and Multi classes are by rule.
- Methods are unstated for YCharts' risk-free rate, std-dev frequency, `drawdown_Ny` vs `max_drawdown_Ny`, and whether
  returns are net of the advisory fee. A one-time side-by-side check per variant (PRD FWD-7) settles them.

## 6. What Opal already holds

**Sources.** A read-only estate census (2026-10-05) and the round-5 Opal-held census over Y-5's 99 holdings
(`deliverables/maps/overview_coverage.json`; rows W3-S7, W2-S9).

**Bottom line.** Opal holds the right KIND of data in most families. No family covers a client portfolio's holdings: the
Bloomberg feed covers only the constituents of Opal's own four ETFs.

| # | Family | Source / storage | Cadence | Keying | Coverage, and fit for the reports |
|---|---|---|---|---|---|
| 1 | Holding characteristics and total-return history | Bloomberg Terminal (reachable only on the Terminal box): `opal-data-etfs/bbg/{as-of}/` (characteristics, history_topup, fund_daily, run_manifest); frozen 5.6-year backfill `bbg-testpull/tickers/{T}/history.csv`. Code: `integrations/bloomberg/pipeline/etf_daily_pull.py`; `data/etfs/scripts/gold/etf_positioning_gold.py:41` | daily 07:00 ET for T-1 (Windows task, `scheduled_daily_pull.cmd`) | queried by CUSIP / SEDOL / Bloomberg id; stored as "TICKER US Equity" | **Fields:** PX_LAST and daily gross total return, GICS sector / industry group, country of domicile, market cap, adjusted beta, dividend yield, fund fields (expense ratio, holdings count, duration, tracking error).<br>**Universe:** the four Opal ETFs' constituents, the funds themselves and 2 extras; history at most 5.6 years. The census matched 37 of 99 holdings (all single US stocks), the fund fields were empty for all 99, and 62 have no price series.<br>**Extension precedent:** `EXTRA_SECURITIES` + `pipeline/backfill_extra_securities_history.py` (Andrew approved, as a vendor change). |
| 2 | Fund-level sector and country allocation | Bloomberg ReferenceDataRequest on the fund ticker: `HB_INDUSTRY_SECTOR_ALLOCATION` (GICS-style), `HB_GEO_CNTRY_ALLOC`, `FUND_PCT_TOP_TEN_HOLD`, `TOTAL_NUMBER_OF_HOLDINGS_IN_PORT`. Stored at `bbg/{as-of}/constituents/` (`pipeline/etf_constituents_pull.py`), for the four Opal ETFs only | daily | fund ticker | The right shape for any ETF holding's sector and region weights. **Current-day only: Bloomberg serves no history**, so each day not captured is lost (`integrations/bloomberg/READ_HERE.md` section 4). Served without BQL |
| 3 | ETF look-through holdings | Opal ETFs: `opal-data-etfs/silver/holdings/{date}.parquet` from the Pathfinder and TrueShares issuer CSVs (~18:00 daily). About 15 rival ETFs: Excel BQL queries with dated history (`data/etfs/scripts/rivalfunds/collector_bloomberg.py`; `org/tier1_exec/4.0.0_SA_CRO~Z/deliverables/AMGT_RECONN_SOURCES_20260929/BBG_EXCEL_ACCESS_VERIFIED.md`) | daily | issuer ids / tickers | **Excel BQL is the only proven look-through route for arbitrary ETFs.** It needs Excel on the Terminal box, failed for 1 fund in 6 in testing, and is untested for mutual funds. Its daily capacity was exhausted at 07:06Z today by the rival-funds backfill. The BQL API itself is refused (an entitlement; Andrew's spend decision) |
| 4 | Benchmark index series | Bloomberg morning pull: 84 index series (equity, bond, sector, commodity, Opal custom models), PX_LAST and daily total return since 1989-12-31 (`pipeline/tplus1/src/market_indices_data_pull.ipynb`; S&P 500 = `SPX Index` at line 210). `data.pkl` goes to `opal-data-portal-v2/uploads/` (`pipeline/publish_to_portal.py:56`); DynamoDB `opal-portal-market-data` (`INDEX#<display name>` / `DAILY#date`) | daily T-1 | display name | **Fit** (more than 15 years; ^SPXTR derivable from SPX's daily total return).<br>Limits: keyed by display name; DynamoDB rounds to 2 decimals (take levels from data.pkl); a fixed universe |
| 5 | Risk-free rate | FRED DGS3MO: `opal-data-portal-v2/json/macro/yield_curve_fred.json` (`fred-data-ingestion/ingest_yield_curve_fred.py`; EventBridge 6pm ET) | daily | series id | **2 years only** (the code's lookback), so only 1y alpha/Sharpe/Sortino compute (row W2-S9).<br>Fixes already in the estate: lengthen the lookback (the FRED key is held in `opal/external-apis`); or use the Bloomberg 3M yield already in data.pkl (`json/macro/timeseries/`); or the Bloomberg 0-1Y Treasury TR index as a cash proxy |
| 6 | Prices for every Black Diamond-held security (incl. mutual funds) | Yahoo Finance: `opal-data-bd/silver/historical_prices.parquet` (date, ticker, close), feeding `silver/prices/canonical_prices.parquet`. Fetch: `data/black_diamond/scripts/silver/fetch_historical_prices_yfinance.py`; canonical build: `data/black_diamond/scripts/gold/build_canonical_prices_v2.py` | daily 14:00 UTC (scheduler Lambda starts a temporary EC2) | ticker (AI-mapped) | **The broadest price coverage in the estate**, but its match to report holdings is unmeasured.<br>Limits: about 5.8 years (from 2020-01-01); close only; mixed adjustment (the backfill is adjusted, the daily fetch is not, lines 240-247 vs 482) |
| 7 | Classifications (label-level) | DynamoDB `etf-classifications` (asset class, sub-class, sector, maturity, geography, style; `terraform/yang-pipeline/etf-classifications.tf`; new stocks weekdays 10:00 ET), `bd-securities` (AI labels incl. Cash), `trade-security-identifiers` | daily / on change | ticker | census 97, 98 and 8 of 99. **One label per holding, so no look-through shares** |
| 8 | Research price history | `bloomberg/harvest/bronze/price_history_px_last` (`integrations/bloomberg/research/price_history_pull.py`) | ad hoc | ticker | about 400 days, price only. Minor |

**Compute already in the estate:**
- IRPT Lambdas at 512-2048 MB (`infra/aws/terraform/investor-reporting/*/lambda.tf`).
- The always-on t3.medium resident EC2 host (one supervised worker on `irpt-generation`; `ycharts/resident.tf`,
  `ycharts/generate/install-resident.sh`).
- **That host already renders exports with Playwright** (`infra/aws/terraform/investor-reporting/export/main.tf:84`;
  `infra/aws/ec2/investor-reporting-export/render_export.cjs`). The report renderer can live there.
- Every Bloomberg call must run on the Terminal box: one seat, and the remote tunnel is designed but not built.

**Licensing:** Andrew cleared redistribution of Terminal data on 2026-07-10
(`org/tier0_exec/0.0.0_AB_MSTR/deliverables/NFRA_BBGMCP_PRD.md:91`). The terms for filings and financials are open
(`org/missions/D5/AMGT/AMGT_RESAPP/prd/AMGT_RESAPP_PRD.md:2153`).

## 7. What Opal does not hold, and a fast/light channel for each

**Principle.**
- The light way is a per-security cache keyed by the identifiers resolution already produces, refreshed only for the union
  of securities in live client portfolios.
- Histories are backfilled ONCE when a security first appears and appended daily after.
- Point-in-time reference fields are captured daily from the day a security first appears, since Bloomberg serves no
  history for them.
- **Vendor or online egress (EDGAR, issuer sites, a longer FRED lookback, new Bloomberg tickers) needs Andrew's
  per-use word or a standing authorization (CLAUDE.md, Agent Autonomy).** The Bloomberg quota is unmeasured; Andrew has
  called it "the binding constraint" and refused a 2,600-security pull
  (`org/tier1_exec/1.0.0_SA_CTO/deliverables/ANDREW_DIRECT_20260922_130xZ_AMGT_KEYING_RESEARCH_START_SMALL_LIST_EXCERPT_CANVASS_QUOTA.md`).

| Gap (report elements) | Fast/light channel(s) | Notes |
|---|---|---|
| **Long total-return histories for arbitrary holdings** (all (c) per-holding elements; 15-year windows) | (1) Bloomberg HistoricalDataRequest (PX_LAST plus daily total return), one-time backfill per new security through the `EXTRA_SECURITIES` / `backfill_extra_securities_history.py` precedent, then the daily top-up. (2) The Yahoo Finance pipeline Opal already runs: extend its start date and fix its adjustment convention | (1) is quota-bound and Terminal-box only. (2) is already scheduled and covers mutual funds, but needs a total-return convention and a coverage check against client holdings |
| **Benchmark** (^SPXTR) | Held: SPX Index daily total return since 1989 (family 4) | Use data.pkl levels, not the 2-decimal DynamoDB copy |
| **Risk-free 3M** (alpha, Sharpe, Sortino beyond 1y) | Lengthen the FRED lookback (key held), or the Bloomberg 3M yield in data.pkl | The lightest gap in the list |
| **Sector and country look-through** for ETF and fund holdings (Overview p3-p5 equity/region; Comparison/Multi exposures; ~200+ elements) | Bloomberg `HB_INDUSTRY_SECTOR_ALLOCATION`, `HB_GEO_CNTRY_ALLOC` per fund ticker: one refdata call per holding per day, served without BQL | GICS-style sectors versus YCharts' Morningstar sectors (a mapping or a stated deviation). Current-day only, so start capturing now. Untested on mutual-fund tickers |
| **Bond-sleeve look-through** (credit quality 8, maturity buckets 16, bond sector 6, duration, YTM, coupon; 30+ Overview elements, more in Comparison/Multi) | (a) Bloomberg fund-level duration / YTM / coupon fields (family 1 holds a duration field), the cheapest first probe. (b) SEC EDGAR N-PORT filings: complete quarterly holdings of every registered fund and ETF with each bond's maturity, coupon and type; free online; ~60-day lag; ratings not included. (c) Issuer monthly fact sheets carry credit-quality and maturity breakdowns. (d) Excel BQL holdings plus per-bond Bloomberg data, aggregated (quota-heavy) | No credit-quality or maturity-distribution field exists anywhere in the repo today. N-PORT plus Opal aggregation is the zero-vendor route for maturity, sector and coupon; credit quality needs ratings (Bloomberg per-bond, or the issuer sheets) |
| **Market-cap buckets and style box** (14+ elements) | Look-through holdings (N-PORT, issuer CSVs or Excel BQL) times per-stock market cap (Bloomberg `CUR_MKT_CAP`, held for covered stocks), with Opal-defined breakpoints. The style box needs Opal-defined value/growth scores | No Morningstar relationship exists. Either define Opal's own method, or drop or replace the style box in the Opal-branded report |
| **Fund fundamentals** (net/gross expense ratio, distribution yield, holdings count, inception date) | (a) Bloomberg fund fields, once fund tickers are on the pulled list. (b) SEC prospectus 497K / N-1A risk-return XBRL (expense ratios, loads), free online. (c) Orion Eclipse `/security` endpoints (`data/assets/vendor_api/orioneclipse/ENDPOINT_REGISTRY.json`), unverified for this | `FUND_EXPENSE_RATIO` was empty for all 99 because those were stocks; fund tickers were never pulled. No inception-date source found yet (Bloomberg `FUND_INCEPT_DT` is the natural probe) |
| **Prospectus and yields** (front/deferred/redemption loads, 7- and 30-day SEC yields subsidized/unsubsidized, waivers; Comparison/Multi tables) | SEC 497K XBRL (loads, fees, waivers); issuer daily or monthly pages (SEC yields); Bloomberg fund yield fields | SEC yields are daily and issuer-published; the light path is a nightly read for held funds |
| **Top-25 constituents of each fund holding** (Comparison/Multi holdings tables) | Issuer daily holdings CSVs (most ETF issuers publish one); N-PORT quarterly; Excel BQL (proven for ~15 rival ETFs) | Opal already runs two issuer-CSV channels (family 3) |
| **Valuation ratios; median ROA/ROE** | Per-stock Bloomberg fields (`integrations/bloomberg/research/model_block_pull.py`) over the look-through, weighted by Opal | Needs look-through first |
| **5-year beta and alpha per holding** | Compute in-house from the total-return series and the benchmark (the methods exist in `layout_overview.py`) | No data purchase needed |
| **Cash, convertible and preferred splits; money-market funds** | Classification labels (family 7) for the money-market / cash sleeve; convertibles and preferreds from N-PORT asset categories | Mutual-fund look-through is otherwise unproven |

**The YCharts residue after the build:**
- YCharts is used only for the one-time side-by-side check per variant (PRD FWD-7), then retired. A standing parity
  comparator is barred (CLAUDE.md, "NEVER stand up a shadow/build-alongside pipeline").
- The calls in section 2 stop. Opal's `irpt-generation` queue then feeds an in-house worker that reads the cache,
  computes, renders and certifies.

## 8. Measured operating facts (why on-prem)

| Fact | Measured | Where |
|---|---|---|
| Job time | 17-19 min per report; 15m07s of it parked in a fixed 900 s wait for the firewall window after one read-back (6 of 6 jobs) | `IRPT_MVP_Y/Y6/Y6_BACKEND_SUMMARY.md` |
| Firewall window | the 7th request in a window is challenged; a 7th 373 s after the first answered; 122 s challenged. The window is in (122, 373] s. The release cut to 390 s is approved (CTO batch 262), built (@f1e101d19c) and deploys after Y-6 | `IRPT_MVP_Y/WAF_WINDOW/` |
| Multi-Comp | 5 vendor requests before the read-back; the read-back is challenged and absorbed by the wait | Y6 runs 5-6 |
| Session | evicted twice (14:41Z and 14:56Z) because Opal employees share the YCharts account and a new login evicts the stored one (Andrew via MSTR 105330); run 7 ended ATTENTION SESSION_REFRESH_ALREADY_USED | Y6 run 7 |
| Data endpoints | fund_data ignores dates; table_data 404 for holdings; general_data 400 for holdings items | rows S6-S8 |
| Budgeted Overview | 8 requests = 2 windows, about 12 min of waiting for ~2 s of YCharts work | round-5 PLAN line |
| Page side | open to sections 1.4-2.0 s (60-card Overview), 10-20 s (104-card Multi) | ~D's Y-6 record |

## 9. Framing for the on-premises assessment (for the CRO; not a design)

- **Inputs are already Opal's:** the upload, normalization, resolution and holdings snapshot (section 1). Nothing there
  depends on YCharts except the vendor's echo of the upload.
- **Compute is already Opal's** for (c): `layout_overview.py`'s methods, with a trace. It needs only the series.
- **Render is already Opal's:** the HTML builder and `render_pdf.cjs`, run today on the laptop. On premises it is a
  container or Lambda image with Chromium.
- **Storage and serving are already Opal's:** the firm bucket, `irpt-jobs`/`irpt-requests`, `irpt-status`, the page and
  export.
- **The build is a data mart plus three report layouts.** The data mart holds a per-security daily series store and a
  per-security reference snapshot, refreshed on a schedule and keyed by the identifiers the resolution step already
  produces. The layouts are the three variants, from the three maps. A one-time side-by-side check per variant (FWD-7) is
  the acceptance.
- **Law the build lives under:**
  - LGIC (rule 30): new homes and names from the canon's builders.
  - No shadow pipeline or standing parity comparator: a one-time check only.
  - Vendor egress needs Andrew's per-use word.
  - Bloomberg follows `integrations/bloomberg/READ_HERE.md`.

---

## Appendix A -- Opal's v1 contracts (field trees; `docs/contracts/investor-reporting/v1/`)

Required fields are marked (req). Depth is 2; deeper structure is in each file.

#### `AnalysisUploadRequest` (docs/contracts/investor-reporting/v1/AnalysisUploadRequest.schema.json)
- `upload_token` (req): string
- `filename` (req): string
- `csv_base64`: string
- `declared_currency`: enum[USD,None]
- `price_date`: string|null
- `reference_notional`: string|null
- `supersedes_input_id`: string
- `file_base64`: string
- `file_type`: enum[csv,xlsx]
- `corrections`: array<object>
  - `finding_code` (req): enum[TICKER_NOT_FOUND,TICKER_DATA_NOT_ENTITLED,TICKER_AMBIGUOUS,TICKER_CHECK_UNAVAILABLE]
  - `from_value` (req): string
  - `to_value` (req): string

#### `AnalysisUploadResult` (docs/contracts/investor-reporting/v1/AnalysisUploadResult.schema.json)
- `upload_id` (req): string
- `state` (req): enum[NORMALIZED,NEEDS_CORRECTION,RESOLVING]
- `input_id` (req): string|null
- `input_ref`: object
  - `input_id` (req): string
  - `content_sha256` (req): string
  - `artifact_ref` (req): object
- `portfolio`: object
- `reason`: string
- `row`: integer|null
- `preview`: object
- `currency_evidence`: object
- `reconciliation`: object
- `findings`: array<object>
- `findings_total`: integer|null
- `template`: object

#### `AnalysisSubmissionRequest` (docs/contracts/investor-reporting/v1/AnalysisSubmissionRequest.schema.json)
_IRPT-MAINTAINED-SOURCE-02 51b5d63a81. Browser metadata and owned references only. Y validates exact input basis and semantics before acceptance._
- `request_id` (req): string
- `client_id` (req): string|null
- `account_ids` (req): array<string>
- `snapshot_id` (req): string|null
- `variant` (req): enum[auto,overview,comparison,multicomp]
- `comparison_keys` (req): array<string>
- `report_title` (req): string|null
- `input_id`: string
- `prepared_for` (req): string

#### `AnalysisRequest` (docs/contracts/investor-reporting/v1/AnalysisRequest.schema.json)
_GENERATED, NOT AUTHORED. Source of record: org/missions/D9/IRPT/IRPT_BCKEND/prd/IRPT_BCKEND_PRD.md @62301f71e0, CONTRACTS table row `AnalysisRequest` (producer BCKEND B5/B6/B7; consumer FNTEND; cell B5, B6, B7). Every property description quotes the table item it comes from VERBATIM between double q_
- `identity` (req): object
  - `tenant_firm_id` (req): string
  - `request_id` (req): string
  - `revision` (req): integer
  - `immutable` (req): const true
  - `ingestion_gate_revision` (req): string
  - `destination_policy_revision` (req): string
- `sender_evidence` (req): object
  - `verified` (req): enum[VERIFIED,UNVERIFIED,REJECTED]
  - `original_sender_address` (req): string
  - `verification_method` (req): enum[FORWARDING_ARRANGEMENT_HEADERS,ORIGINAL_MIME,UNKNOWN]
  - `display_from_used` (req): const false
- `message_refs` (req): array<string>
- `attachment_refs` (req): array<object>
  - `attachment_id` (req): string
  - `storage_key` (req): string
  - `sha256` (req): string
- `normalized_holdings` (req): array<object>
  - `identifier` (req): string
  - `identifier_namespace` (req): enum[TICKER,CUSIP,ISIN,CASH,MODEL,UNMATCHED]
  - `quantity` (req): object
  - `source_sheet`: string|null
  - `source_row`: integer|null
  - `source_column`: string|null
  - `source_value_verbatim` (req): string
- `variant` (req): enum[OVERVIEW,COMPARISON,MULTI,UNKNOWN]
- `comparisons` (req): array<object>
  - `position` (req): integer
  - `security_identifier` (req): string
- `settings` (req): object
  - `management_fee` (req): number
  - `rebalance`: string
  - `dividends`: boolean
  - `start`: string
  - `price`: string
  - `tax_status`: string
  - `benchmark`: string
- `findings` (req): array<object>
  - `code` (req): string
  - `detail` (req): string
  - `severity` (req): enum[INFO,UNCERTAIN,BLOCKING]
- `corrections` (req): array<object>
  - `finding_code` (req): string
  - `approved_by` (req): string
  - `from_value` (req): string
  - `to_value` (req): string
- `stage` (req): enum[RECEIVED,PARSED,NEEDS_CORRECTION,READY,SUBMITTING,GENERATED,RELEASED,FAILED]
- `release` (req): object
  - `policy_version` (req): string
  - `state` (req): enum[DRAFT,RELEASED,WITHHELD]
- `contract_version`: const "v1"

#### `RequestComposition` (docs/contracts/investor-reporting/v1/RequestComposition.schema.json)
_IRPT-MAINTAINED-SOURCE-01 at0429af3604. Admission contract for new maintained-source compositions; never retrofit authority onto historical v1 captures. Keep existing top-level spelling and registered REQUEST_COMPOSITION storage. M resolves authority and identity; Y validates input/recipe/settings a_
- `schema_version` (req): const "irpt-analysis-composition.v1"
- `browser` (req): ref:browser
- `resolved` (req): ref:resolved
  - `owner` (req): ref:owner
  - `input_ref` (req): ref:input_ref
  - `client` (req): object
  - `document`: object
  - `holdings`: object
  - `scope`: object
  - `profile` (req): ref:profile
  - `profile_provenance` (req): ref:profileProvenance
  - `comparison_catalog` (req): object
  - `source_descriptors` (req): object
  - `recipe_source_id` (req): string
  - `settings_source_id` (req): string
  - `input_owner`: ref:inputOwner
- `recipe_version` (req): string
- `settings` (req): object

#### `HoldingsSnapshot` (docs/contracts/investor-reporting/v1/HoldingsSnapshot.schema.json)
_GENERATED, NOT AUTHORED. Source of record: org/missions/D9/IRPT/IRPT_BCKEND/prd/IRPT_BCKEND_PRD.md @62301f71e0, CONTRACTS table row `HoldingsSnapshot` (producer BCKEND B12; consumer FNTEND; cell B12). Every property description quotes the table item it comes from VERBATIM between double quotes; a pr_
- `scope` (req): object
  - `resolved_scope_fingerprint` (req): string
  - `firm_id` (req): string
  - `account_ids` (req): array<string>
- `source_set_revision` (req): array<object>
  - `source` (req): string
  - `revision` (req): string
  - `completion_date` (req): string
- `clocks` (req): object
  - `business_date` (req): string
  - `as_of_timestamp` (req): string
  - `source_as_of`: array<object>
  - `custody_as_of`: string
  - `overlay_as_of`: string
- `custody_totals` (req): object
  - `unique_account_count` (req): integer
  - `unique_position_count` (req): integer
  - `total_market_value` (req): object
  - `deduplicated` (req): const true
- `nodes` (req): array<object>
  - `node_id` (req): string
  - `parent_node_id`: string|null
  - `level` (req): integer
  - `node_kind` (req): enum[ACCOUNT,SLEEVE,MODEL_WRAPPER,MODEL_LEAF,SECURITY,CASH,UNRESOLVED,CATEGORY]
  - `model_id`: object
  - `security_id`: object
  - `basis` (req): enum[OBSERVED,ASSIGNED,TARGET]
  - `amount` (req): object
  - `percentages` (req): object
  - `provenance` (req): object
  - `drill_refs`: array<object>
  - `classification`: object
  - `clocks`: object
  - `valuation_facts`: array<object>
  - `display`: object
  - `asset_class`: enum[equity,fixed_income,alternatives,structured,commodities,multi_asset,cash,other]...
  - `sub_asset_class`: string|null
  - `asset_class_basis`: enum[TABLE,NAME_ALIAS,NAME_PATTERN,TICKER_SHAPE,NONE]
  - `model_code`: string|null
  - `assigned_strategy`: object
- `coverage` (req): object
  - `nodes_resolved` (req): integer
  - `nodes_attempted` (req): integer
  - `remainder` (req): object
- `contract_version`: const "v1"
- `source_vendor_keys`: array<string>
- `attribution_holdouts`: object
  - `unassigned` (req): object
  - `assigned_without_custody`: object
  - `reconcile` (req): object
- `security_aggregates`: array<object>
  - `security_id` (req): object
  - `display`: object
  - `asset_class`: enum[equity,fixed_income,alternatives,structured,commodities,multi_asset,cash,other]...
  - `sub_asset_class`: string|null
  - `amount` (req): object
  - `weight` (req): number|null
  - `account_count` (req): integer
- `class_totals`: array<object>
  - `asset_class` (req): enum[equity,fixed_income,alternatives,structured,commodities,multi_asset,cash,other]...
- ... (19 more lines)

#### `ComparisonCatalogue` (docs/contracts/investor-reporting/v1/ComparisonCatalogue.schema.json)
_AUTHORED, cell IB-yr-242 (CTO 103038, shape B). ResolvedScope stays v1 and carries no catalogue; this is the catalogue's own closed v1 contract, served by GET /api/scoped/investor-reporting/analysis/comparisons behind the same authz guard and tenant check as the family's other scoped reads. Names co_
- `catalogue_version` (req): const "v1"
- `entries` (req): array<object>
  - `key` (req): string
  - `label` (req): string
  - `ticker` (req): string|null
  - `name_source` (req): enum[model_catalogue,etf_classifications,ticker_verbatim]

#### `StatusEnvelope` (docs/contracts/investor-reporting/v1/StatusEnvelope.schema.json)
_GENERATED, NOT AUTHORED. Source of record: org/missions/D9/IRPT/IRPT_BCKEND/prd/IRPT_BCKEND_PRD.md @62301f71e0, CONTRACTS table row `StatusEnvelope` (producer BCKEND B16; consumer FNTEND; cell B16). Every property description quotes the table item it comes from VERBATIM between double quotes; a prop_
- `operation` (req): object
  - `operation_id` (req): string
  - `operation_kind` (req): string
  - `revision` (req): string
- `state` (req): enum[QUEUED,RUNNING,READY,PARTIAL,STALE,UNAVAILABLE,NEEDS_CORRECTION,UNCERTAIN]...
- `source_dates` (req): object
  - `business_date`: string
  - `source_completion_date`: string|null
  - `as_of`: string|null
  - `date_basis`: enum[UNDATED_INPUT,PER_SECTION]
  - `prospect_analysis`: object
  - `section_dates`: array<object>
- `actions` (req): array<object>
  - `action` (req): enum[RETRY,RESUME,RESYNC,CORRECT,WAIT,NONE]
  - `safe` (req): const true
  - `description` (req): string
- `public_reason_code` (req): string
- `internal_correlation_id` (req): string
- `contract_version`: const "v1"

#### `PublicStatusEnvelope` (docs/contracts/investor-reporting/v1/PublicStatusEnvelope.schema.json)
_Public projection removes schema-marked server-only members. Internal StatusEnvelope retains the six historical obligations. IRPT-Y-DATES-01 uses explicit status-job capability negotiation._
- `operation` (req): object
  - `operation_id` (req): string
  - `operation_kind` (req): string
  - `revision` (req): string
- `state` (req): enum[QUEUED,RUNNING,READY,PARTIAL,STALE,UNAVAILABLE,NEEDS_CORRECTION,UNCERTAIN]...
- `source_dates` (req): object
  - `business_date`: string
  - `source_completion_date`: string|null
  - `as_of`: string|null
  - `date_basis`: enum[UNDATED_INPUT,PER_SECTION]
  - `prospect_analysis`: object
  - `section_dates`: array<object>
- `actions` (req): array<object>
  - `action` (req): enum[RETRY,RESUME,RESYNC,CORRECT,WAIT,NONE]
  - `safe` (req): const true
  - `description` (req): string
- `public_reason_code` (req): string
- `contract_version`: const "v1"

#### `AnalysisReport` (docs/contracts/investor-reporting/v1/AnalysisReport.schema.json)
_GENERATED, NOT AUTHORED. Source of record: org/missions/D9/IRPT/IRPT_BCKEND/prd/IRPT_BCKEND_PRD.md @62301f71e0, CONTRACTS table row `AnalysisReport` (producer BCKEND B9/B10; consumer FNTEND; cell B9, B10). Every property description quotes the table item it comes from VERBATIM between double quotes;_
- `request_ref` (req): object
  - `request_id` (req): string
  - `request_revision` (req): integer
  - `attempt_id` (req): string
  - `attempt_number` (req): integer
- `vendor_artifact` (req): object
  - `sha256` (req): string
  - `byte_length` (req): integer
  - `retrieved_at` (req): string
  - `content_type`: string
- `effective_inputs` (req): object
  - `read_back` (req): enum[READ_BACK_VERIFIED,NOT_READ_BACK]
  - `holdings_fingerprint` (req): string
  - `settings` (req): object
- `sections` (req): array<object>
  - `section_id` (req): string
  - `section_type` (req): string
  - `value`: number|string|null
  - `units` (req): string
  - `as_of_date` (req): string
  - `date_claim`: enum[SECTION,REPORT,NONE]
  - `page` (req): integer
  - `bbox`: array<number>
- `undated_sections`: array<object>
  - `section_id` (req): ref:section_id
  - `section_type` (req): ref:section_type
  - `value`: ref:value
  - `units` (req): ref:units
  - `page` (req): ref:page
  - `bbox`: ref:bbox
  - `date_claim` (req): const "NONE"
- `disclosures` (req): array<object>
  - `disclosure_id` (req): string
  - `text` (req): string
  - `source_page`: integer|null
- `extraction_coverage`: object
  - `policy_version` (req): const "source-verified-partial-v1"
  - `status` (req): enum[PARTIAL,COMPLETE_FOR_CENSUS]
  - `scope` (req): const "PINNED_CENSUS"
  - `census_sha256` (req): string
  - `counts` (req): object
  - `gaps` (req): array<object>
- `extraction_validation` (req): object
  - `status` (req): enum[CERTIFIED,UNCERTIFIED,FAILED]
  - `checks_run` (req): integer
  - `checks_failed` (req): integer
  - `notes`: string|null
- `release` (req): object
  - `released_revision` (req): string|null
  - `protected_pdf_ref`: object
- `contract_version`: const "v1"

#### `RenderPackage` (docs/contracts/investor-reporting/v1/RenderPackage.schema.json)
_GENERATED, NOT AUTHORED. Source of record: org/missions/D9/IRPT/IRPT_BCKEND/prd/IRPT_BCKEND_PRD.md @62301f71e0, CONTRACTS table row `RenderPackage` (producer FNTEND; consumer BCKEND B14; cell B14 (consumer)). Every property description quotes the table item it comes from VERBATIM between double quot_
- `supported_versions` (req): object
  - `contract_versions` (req): array<string>
  - `template_versions` (req): array<string>
- `components` (req): array<object>
  - `component_id` (req): string
  - `surface` (req): enum[SCREEN,PRINT,BOTH]
  - `deterministic` (req): const true
- `requirements` (req): object
  - `fonts` (req): array<object>
  - `assets` (req): array<object>
- `print_entry_point` (req): object
  - `module` (req): string
  - `export_name` (req): string
- `visual_fixtures` (req): array<object>
  - `fixture_id` (req): string
  - `path` (req): string
  - `sha256` (req): string
- `packaging` (req): object
  - `packaged_by` (req): const "BCKEND_B14"
  - `executed_version` (req): string
- `contract_version`: const "v1"

#### `ExportBundle` (docs/contracts/investor-reporting/v1/ExportBundle.schema.json)
_GENERATED, NOT AUTHORED. Source of record: org/missions/D9/IRPT/IRPT_BCKEND/prd/IRPT_BCKEND_PRD.md @62301f71e0, CONTRACTS table row `ExportBundle` (producer BCKEND B14; consumer B14 render; FNTEND F8 (preview -- a preview never calls the vendor again); cell B14). Every property description quotes th_
- `authorized_report_revisions` (req): array<object>
  - `report_id` (req): string
  - `revision` (req): string
  - `authorization_ref` (req): string
  - `immutable` (req): const true
  - `performance_source`: object
- `selected_sections` (req): array<string>
- `narrative_packet_ref`: object
  - `packet_id` (req): string
  - `revision` (req): string
  - `sha256` (req): string
- `analysis_report_ref`: object
  - `report_id` (req): string
  - `revision` (req): string
  - `sha256` (req): string
- `narrative_state`: enum[NOT_ATTACHED]
- `narrative_reason`: string
- `approved_assets` (req): array<object>
  - `asset_id` (req): string
  - `kind` (req): enum[LOGO,FONT,IMAGE,TEMPLATE_PART]
  - `sha256` (req): string
  - `binding` (req): string
- `versions` (req): object
  - `template_version` (req): string
  - `renderer_version` (req): string
  - `disclosure_version` (req): string
- `render_options` (req): object
  - `orientation` (req): enum[PORTRAIT,LANDSCAPE]
  - `page_size` (req): string
  - `brand_revision` (req): string
- `live_vendor_request_during_render` (req): const false
- `contract_version`: const "v1"

#### `PerformanceReport` (docs/contracts/investor-reporting/v1/PerformanceReport.schema.json)
_GENERATED, NOT AUTHORED. Source of record: org/missions/D9/IRPT/IRPT_BCKEND/prd/IRPT_BCKEND_PRD.md @62301f71e0, CONTRACTS table row `PerformanceReport` (producer BCKEND B11; consumer FNTEND; cell B11). Every property description quotes the table item it comes from VERBATIM between double quotes; a p_
- `lineage` (req): object
  - `source_system` (req): string
  - `provider` (req): enum[SMARTX,BLACK_DIAMOND,ORION,OPAL_ENGINE,OPAL_HOLDINGS,UNKNOWN]
  - `tenant_firm_id` (req): string
  - `source_revision` (req): string
  - `calculation_id`: string
  - `group_path`: array<string>
  - `node_type`: string
- `dates` (req): object
  - `requested_start` (req): string
  - `requested_end` (req): string
  - `actual_start` (req): string
  - `actual_end` (req): string
- `measurement_basis` (req): object
  - `currency` (req): string
  - `method` (req): enum[TIME_WEIGHTED,MONEY_WEIGHTED,UNKNOWN]
  - `fee_basis` (req): enum[GROSS,NET,UNKNOWN]
  - `accrual_basis` (req): enum[ACCRUAL,CASH,UNKNOWN]
  - `annualization` (req): enum[NONE,ANNUALIZED,UNKNOWN]
  - `return_units` (req): enum[DECIMAL_FRACTION,PERCENT]
- `returns` (req): object
  - `summary_returns` (req): array<object>
  - `period_returns` (req): array<object>
  - `daily_cumulative_series` (req): array<object>
  - `account_detail` (req): array<object>
- `optional_facts` (req): object
  - `benchmark`: object|null
  - `value_facts`: object|null
  - `supported` (req): boolean
- `contract_version`: const "v1"
- `retained_ref`: object
  - `report_id` (req): string
  - `revision` (req): string
  - `sha256` (req): string
  - `report_kind` (req): const "PERFORMANCE"
  - `immutable` (req): const true

#### `OwnedAnalysisRequest` (docs/contracts/investor-reporting/v1/OwnedAnalysisRequest.schema.json)
_Immutable accepted request identity, original acceptance time and, on the single-request read, the chosen comparisons' names (include=comparisons) and the frozen browser request (include=composition). Current owner and retained composition authorization are server responsibilities. No custody scope,_
- `identity` (req): object
  - `tenant_firm_id` (req): string
  - `request_id` (req): string
  - `revision` (req): integer
  - `immutable` (req): const true
  - `ingestion_gate_revision` (req): string
  - `destination_policy_revision` (req): string
- `accepted_at` (req): integer
- `comparisons`: array<object>
  - `key` (req): string
  - `label` (req): string
- `composition`: ref:AnalysisSubmissionRequest.schema.json

## Appendix B -- research store contracts (IRPT_YCDGEN)

- **Kept answer** (`schema` irpt-ycdgen-kept-v1; `.../ycharts_responses/request=<REQ>/step=NN_<call>.json`):
  - `schema`, `firm`, `request_id`, `step` int, `name` str, `call` {method, path, params};
  - `request_sha256` (round 5);
  - `kept_at` iso, `shape` IDENTIFIERS | DATA | DOCUMENT, `changed_since_previous` true | false | no_previous |
    request_changed;
  - `response` {`status` int, `content_type`, `bytes` int, `sha256`, `body_json` | `body_b64`} (scrubbed: no cookie or
    token).
- **Run record** (`schema` irpt-ycdgen-run-v1, or v2 with `holdings`; `.../ycharts_runs/request=<REQ>/run.json`):
  - `request_id`, `firm`, `portfolio`, `report_type`, `template_id`, `window` {start, end}, `status` COMPLETE | STOPPED,
    `stop_reason`, `lease`;
  - `calls[]` {`name`, `step`, `status`, `shape`, `sha256`, `request_sha256`, `changed_since_previous`, `started_at`,
    `waited_ms`, `ycharts_ms`, `key`};
  - `clocks` {`ycharts_working_ms`, `opal_waiting_ms`, `opal_building_ms`};
  - `elements[]` {`id`, `source`, `computed` (3.5 trace)};
  - `report` {`key`, `sha256`, `pages`};
  - v2 `holdings` {`source_request`, `basis`, `rows[]` {ticker, amount}}.
- **Map** (`schema` irpt-ycdgen-map-v1):
  - `report_type`, `template_id`, `source_pdf` {bucket, artifact_prefix, pages};
  - `calls[]` {`name`, `method`, `path`, `params`, `expand` {over, param, chunk, item, join}};
  - `elements[]` {`id` pN.eNN, `page`, `kind` number | table | chart | text, `label`, `note`, `claim`, and `source`. The
    `source` is BUILDER_ONLY, or {`call`, `field`, `key_index`, `column_sources`, `computed`, `columns`, `sleeve`,
    `statistic`}, or {`computed` OPAL_HELD, `group`, `field`}}.
- **Coverage row** (`overview_coverage.json`):
  - `id`, `class` HELD_DATA | OWN_SERIES | OTHER_ENDPOINT | BUILDER_ONLY;
  - `via` {`columns`, `field`, `aggregation`, `weighting`};
  - `feed` {`source` OPAL_HELD, `table`, `field`, `key`, `method`, `group`} or {`source` NOT_HELD, `reason`}.
- **Stop row** (`.../ycharts_runs/request=<REQ>/stop_row.json`): a surprise-row-shaped record of a firewall or session STOP
  (contract 2.6).
- **Previous-run index**: `{firm, portfolios: {<portfolio>: {request_id, run_key, at}}}`.
