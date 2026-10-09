# Round-82 PREP, three API items (CTO~DELL1 round-81 analysis @284169f039, section 3 items 3, 4a, 4b): grounding notes

Fork of `2.0.0_SA_COO~R1`, 2026-10-09 ~06:5xZ. Not cut, not issued. Read only: GET-shaped invokes of the live function `aAkcp2l1`, S3
list/get, local in-process reads. No store write, no deploy, no vendor call.

## Item 3 -- UNVGY's served no-forecast reason

- **Code:** `lib/research/api/scoped_amgt.py` `read_model` (`:5132`), the branch at `:5174-5187`. With no forecast figures it takes a
  WHOLE-BLOCK unresolved reason (a `SCOPE_FORECAST` entry with no `fiscal_period`); failing that and with a block present, it serves the
  literal `"raw stamp {stamp} carries no bestdata.json (pulled before C-MODEL-FORECASTS)"`.
- **Why UNVGY is wrong:** its block's forecast unresolved entries are ALL per-period (`reason 'no BEST_PERIOD_END_DATE for this period'`,
  FY1-FY3 x the BEST_* mnemonics; evidence `AMGT_CORPUS/.../r41_c4_unvgy_forecast_reason_20261009.txt`), so it falls through; the stamp
  DOES carry bestdata.json (Bloomberg returned 5 of 17 fields, not BEST_PERIOD_END_DATE).
- **Live today:** `/security/UNVGY_US_Equity/thesis` 200, `forecast_reason` = `raw stamp 20261008T131353Z carries no bestdata.json (pulled before C-MODEL-FORECASTS)`.
- **Change:** between the whole-block arm and the stamp arm, when per-period `SCOPE_FORECAST` entries exist, serve one sentence built
  from them -- the most common per-period reason with the periods it covers (e.g. "Bloomberg returned no period end date for FY1, FY2
  and FY3, so no forecast figure is served"). The stamp sentence stays only for a block with no forecast unresolved entry at all.
- **Files:** `scoped_amgt.py` (that branch); a new test `lib/research/api/tests/test_forecast_reason_per_period.py`.

## Item 4b -- a relevance (mention) field on feed items

- **Code:** `scoped_amgt.py` `read_feed` (`:5355`), served on `/security/<key>/overlay` as `feed` (`read_security_overlay`, `:3527`).
  Items are built at `:5410-5421` from gold `article_security_mention` rows; `most_discussed_basis` is the literal ABSENT text (`:5376`).
- **The field already exists in the rows:** every gold row carries `mention_count` (AMD: 463 of 463 rows, one row per article); the
  "In the news" card already serves it as `mentions` (`lib/research/api/top_band.py:115`, `_count`, most-discussed first).
- **Live today:** AMD 22 items, BA 75, NVDA 117 -- 0 carry `mentions`; basis "ABSENT -- harvested news carries no discussion count ...".
- **Change:** each item carries `mentions` (`top_band._count(row.get("mention_count"))`, reused, not re-written); `most_discussed_basis`
  names the measured basis ("gold article_security_mention mention_count"). ORDER stays newest first (the page ranks; C-PRESENTATION-ONLY
  leaves ranking choice to the page, which now has a served field to rank by). Note: sampled AMD counts are mostly 1, a weak signal.
- **Files:** `scoped_amgt.py` (`read_feed` only); a test in `lib/research/api/tests/` (new file).

## Item 4a -- a per-day price series on the timeline route

- **Route:** `/security/<key>/timeline` -> `scoped_amgt.py:6728` calls `lib/research/harvest/timeline_api.py` `get_timeline` (`:289`),
  which takes injected loaders; `word_cloud_builder` (`:6734`) is the precedent for an optional added block.
- **Where per-day prices are STORED:** S3 `opal-data-harvest/bloomberg/harvest/bronze/price_history_px_last/date=<as_of>/{year_pull.json,
  daily_30d.json}` (writer `integrations/bloomberg/research/price_series_persist.py`, `address()`-built; schema `price_px_last_series_v1`,
  `series: {"AMD US": [[date, px], ...]}`). 5 objects today: one year pull (2025-08-28..2026-10-02, 95 tickers, AMD 276 points) and four
  `daily_30d` (10-02, 10-05, 10-06, 10-07). Merge rule: `load_history` (`:131`) -- per ticker by date, the LATER object wins a date.
  NOTHING is fetched from a vendor.
- **Reader gap:** `load_history` lives under `integrations/`, OUTSIDE the function's packaged closure (`lib.research`,
  `lib.opal_data_harvest`, `lib.opal_naming`, `lib.trading_calendar`), so the function cannot import it. A small reader is needed under
  `lib/research/price/` (same address via `opal_naming`, same merge rule, read only).
- **Grant:** the role's inline policy already allows `bloomberg/harvest/bronze/*` (live read 06:5xZ) -- NO IAM change.
- **Live today:** AMD timeline 200, keys `events, floor_date, marker_kinds_absent, markers, security_key, series, word_cloud`; no price.
- **Change:** new `lib/research/price/history_read.py` (`price_points(security_key, start, end)` -> `[{date, close}]` ascending, the
  security_key mapped to the Bloomberg ticker by the crosswalk's own form, e.g. `AMD_US_Equity` -> `AMD US`); `get_timeline` gains an
  optional `price_loader` and serves `price_series`, `price_series_source` (the object keys read) and `price_series_reason` when empty
  (never an invented point); the ONE wiring line `price_loader=...` at `scoped_amgt.py:6728` is a HOOKUP for the issuer at the merge (C10).
- **Files:** new `lib/research/price/history_read.py` + test; `lib/research/harvest/timeline_api.py` + its test; hookup `scoped_amgt.py:6728`.

## Write sets

Items 3 and 4b both edit `scoped_amgt.py` -> ONE cell (two branches, one file). Item 4a touches `timeline_api.py` and a new
`lib/research/price/` module; its one `scoped_amgt.py` line is the merge's hookup, so it is a SEPARATE cell, disjoint from the first.
All three serve only through a redeploy (WORLD), like ee-6; 4a needs no IAM line.

## Checks -- `checks/r82_unvgy.py`, `r82_feed.py`, `r82_timeline.py` (+ helper `_r82_call.py`), dry-run at the base

- r82_unvgy AC1, deployed and local: U1 PASS, U2 FAIL, U3 FAIL; `R82 UNVGY AC1 SERVED: NO`, exit 1 -- FAIL as expected.
- r82_feed AC1, deployed and local: F1 PASS (AMD 22, BA 75 items), F2 FAIL (0 carry mentions), F3 FAIL (ABSENT); NO -- FAIL as expected.
- r82_timeline AC1, deployed and local: T1 PASS (281 chatter days), T2 FAIL (no price_series), T3 FAIL; NO -- FAIL as expected.

## Open

1. Item 3's sentence: which per-period reasons to quote when they differ across mnemonics (today UNVGY's are uniform).
2. Item 4a's ticker map: whether to read the Bloomberg form from the crosswalk or strip `_Equity` (the crosswalk is the estate's rule).
3. Item 4c (the print PDF's "date not stored with this figure" said once, `render_pack.py:486`) was not in this fork's scope.

-- fork of 2.0.0_SA_COO~R1
