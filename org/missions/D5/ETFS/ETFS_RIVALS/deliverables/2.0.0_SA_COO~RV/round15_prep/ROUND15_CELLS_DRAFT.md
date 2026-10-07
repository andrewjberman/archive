## ROUND 15 (main workstream) -- APPENDED

Source: PRD v0.18 `FWD-22`, `FWD-23`, ADDENDUM F (F.1-F.7) @6e245cbebe; five Andrew-direct records of 2026-10-07 04:5xZ-05:2xZ
(modal @ad78eef973, periods @82bb78106e, backfill/page-only/MTD @96d0ab2f4b, calendar days @69c7f24b44, script @efc0acb127);
scoping facts `deliverables/2.0.0_SA_COO~RV/round15_prep/MODAL_PRICE_SERIES_AND_PERIODS_SCOPING_FACTS.md` @d773ddba61. Author
2.0.0_SA_COO~RV; frozen; revision 1.5 of this file. Every interface below is PRESCRIBED so that a consuming cell builds against
the interface with a fixture and never against a sibling's branch: the edges are of interface, not of files.

Shared vocabulary (binding on every cell):
- **Periods:** `R30`, `R90`, `R365` -- calendar days. `asof = prev_trading_day(page_day)` (the existing CALL 3 rule); a window's
  first day is `asof - N calendar days`, its last day `asof`. `MTD`, `QTD`, `YTD` keep computing and are never displayed.
- **Chart object:** one JSON per fund per page day at `homes.page(<day>, "charts/<FUND>.json")` (opal_naming output), shape
  `{"fund", "asof", "generated_at", "ranges": {"R30": <first day>, "R90": ..., "R365": ...}, "securities": {<security_key>:
  {"name", "source_words", "points": [[<YYYY-MM-DD>, <price>|null, <source code>], ...], "gaps": [{"start", "end", "reason"}],
  "markers": [{"side": "buy"|"sell", "start", "end", "span": bool, "usd", "bps", "r", "n_trades"}]}}}`. Source codes:
  `m` market close, `i` holding-implied. `points` ascend by date and cover `asof - 365d .. asof`.
- **Route:** `GET /rivalfunds/<YYYY-MM-DD>/chart/<FUND>` on the gateway, JSON, behind the same identity wall.

Chains (M = 5; file sets disjoint across chains):

| chain | cells in order | files | risk |
|---|---|---|---|
| ~1 | RIV-pd-1, RIV-pd-2, RIV-md-1 | gold_holding_contribution.py, gold_buying_trend.py; then render.py | SERVED |
| ~2 | RIV-ps-1, RIV-tm-1, RIV-co-1 | price_series.py (new), trade_markers.py (new); then publish_page.py | SERVED |
| ~3 | RIV-bf-1 | enrichment_bloomberg.py, bbg_budget.py | WORLD |
| ~4 | RIV-rt-1 | infra/aws/ec2/opal-gateway/app/rivalfunds_view.py, server.py, their tests | WORLD |
| ~5 | RIV-pd-3 | ai_accounts.py | SERVED |

### `RIV-pd-1` -- the gold tables compute 30d / 90d / 365d as calendar days (FWD-23; F.2, F.6)
- Today `gold_holding_contribution.PERIODS = ("MTD","QTD","YTD","R30")` with R30 = the 30th NYSE trading day ending on the day
  (`period_start`, :120-128); `gold_buying_trend.PERIODS = ("YTD","R30","MTD","QTD")`, R30 likewise (`_period_starts`, :123-136).
- Interface: both modules' `PERIODS` gain `R90` and `R365` and keep `MTD`, `QTD`, `YTD`. `gold_holding_contribution.period_start(p,
  day)` and `gold_buying_trend._period_starts(day)[p]` return, for `R30` / `R90` / `R365`, `date(day) - 30 / 90 / 365` calendar
  days (`day` here is the as-of the stage already passes). `earliest_start` follows. A fund whose history starts after the window's
  first day keeps the existing partial rule (`period_clipped`, `price_coverage`). Each table's stage detail states, for one fund,
  the old and the new R30 window (`r30_window_was`, `r30_window_is`).
- Rulings at the cut (issuer): ONE anchor for both tables. The pure functions stay pure on the day they are handed
  (`period_start(p, d)` and `_period_starts(d)[p]` return `d - N` calendar days); `gold_buying_trend.build` hands the three
  rolling periods `gold_holding_contribution.as_of(<event day>)`, exactly as holding_contribution already does, so both tables'
  R30 / R90 / R365 start on the same day. MTD / QTD / YTD keep their present anchors and starts. `r30_window_was` and
  `r30_window_is` sit in each stage's result `detail`, each `{"fund": <id>, "start": <ISO>, "end": <ISO>}` for the first fund
  built.
- **Organic trigger:** the 07:00 ET marker publish's stale-table rebuild (`publish_page.produce_a1`).

### `RIV-pd-2` -- every switch on the page offers 30d | 90d 365d and opens on 30d; no QTD, YTD or MTD is displayed (FWD-23)
- Today `render.PERIODS = ("R30","QTD","YTD")`, `PERIOD_LABEL` names them, `_dialog_keys` covers R30 and YTD (:753), the trend
  sentence says "this year" for YTD (:1750), `_sec_dialogs` prefers the YTD trend row (:1776).
- Interface: `render.PERIODS = ("R30","R90","R365")`; `PERIOD_LABEL = {"R30": "Last 30 days", "R90": "Last 90 days", "R365":
  "Last 365 days"}`; the switch reads 30d, the dividing line, then 90d and 365d, and opens on R30. No element of the rendered
  main page or audit page carries the visible text QTD, YTD, MTD, "Quarter to date", "Year to date" or "Month to date". The
  dialog keys cover R30 and R365; the security dialog's trend row prefers R365. A period that ranks nothing for the fund greys
  and says why (unchanged rule). Rows of MTD / QTD / YTD in the context are ignored, not an error.
- Rulings at the cut (issuer): the switch's own words are short -- `render.PERIOD_SHORT = {"R30": "30d", "R90": "90d", "R365":
  "365d"}` is what each period radio's label prints (Andrew: "30d, then | 90d and 365d"); `PERIOD_LABEL` (the long names) is
  for table headings and dialog rows. The clause "the dialog keys cover R30 and R365" is WITHDRAWN (`_dialog_keys` has no
  caller); the dialog lists the three periods and its buying line is the R365 trend row.
- **Organic trigger:** the 07:00 ET marker publish.

### `RIV-pd-3` -- the AI accounts are written on the same three periods (FWD-23; F.2 last bullet)
- Today `ai_accounts` builds its facts from `("R30",5),("MTD",3),("QTD",3),("YTD",3)` (:165) and the YTD trend rows (:176-183).
- Interface: the fact pack is built from `("R30",5),("R90",3),("R365",3)` and the R365 trend rows; fact keys read
  `<fund>|R90|<bucket>` / `<fund>|R365|<bucket>`; no fact label names MTD, QTD or YTD; the prompt text names the three periods
  in plain words (last 30 / 90 / 365 days). `ai_accounts.PACK_PERIODS = ("R30","R90","R365")` is the one constant.
  The "not shown as current" rule for an older account is render's (round 14's badge) and is not this cell's.
- Rulings at the cut (issuer): a "fact label" is the fact's id and its text. Periods are named to the model in words or digits
  ("last thirty days" / "last 30 days"), consistently with the SYSTEM prompt's own number rule. `P_DIRECTION`'s "the year's
  trend" becomes "the 365-day trend".
- **Organic trigger:** the 09:00 ET sweep's AI step.

### `RIV-ps-1` -- one price series per security: market close first, holding-implied second, a gap with its reason third (FWD-22; C-MODAL-PRICE-SOURCE)
- Measured: `gold/security_market` holds 4 day partitions; `trade_schedule` 504. No module assembles a per-security daily series.
- Interface: new `rivalfunds/price_series.py`. `series(g4: DataFrame, g1: DataFrame, keys, start: date, end: date) -> {key:
  {"points": [(date, price|None, "m"|"i"|None)], "gaps": [{"start","end","reason"}], "source_words": str}}`. For each NYSE
  trading day in `[start, end]`: the G4 `px_close` of that date when present and positive (`m`); else the price implied by any
  universe fund's G1 report of that date, `market_value / quantity` with quantity > 0 (`i`; when several funds report, the
  median); else `None`. Consecutive `None` days form one gap with reason `"no market close on file and no fund reported the
  holding"`. `source_words` names in plain words which sources the series uses. No vendor call, no S3 call: pure over frames.
  `load(s, keys, start, end)` reads the two tables through the sink for the publisher.
- Rulings at the cut (issuer): a G1 row maps to a key through `gold_holding_contribution.row_keys` (the page's own key rule,
  raw-identifier alias included), never `security_id` alone. Several lots of one security in one fund's report are summed
  (market value and quantity) before the ratio. A key in neither frame returns all-None points and one gap over the range.
  Point dates are ISO strings. `load(s, keys, start, end)` returns the same dict `series` returns.
- **Organic trigger:** the publisher's chart object (RIV-co-1).

### `RIV-tm-1` -- a fund's trades in a security as sized markers (FWD-22; C-TRADE-MARKER)
- Measured: `trade_schedule` (G5) carries `action`, `window_start`, `window_end`, `window_trading_days`, `est_notional`; no
  share-of-fund column for the trade itself.
- Interface: new `rivalfunds/trade_markers.py`. `markers(g5_rows, fund_mv_by_date: {date: float}) -> [{"side", "start", "end",
  "span", "usd", "bps", "r", "n_trades"}]` per (fund, security): `side` = `buy` for entry / add, `sell` for trim / exit; `usd`
  = abs(`est_notional`); `bps` = `usd / fund_mv_by_date[window_end] * 10000` (the fund's total reported market value on the
  window end; absent -> `bps` None and `r` = R_MIN); `r` = the marker radius: `R_MIN` (3.0) at 20 bps or less, `R_MAX` (12.0) at
  500 bps or more, linear in bps between; `span` = `window_trading_days > 1`; trades of one side sharing one window are ONE
  marker with `n_trades` counted and `usd` / `bps` summed. A REFUSED window yields no marker. `words(marker) -> str` reads
  "Bought" / "Sold", the date or "between <start> and <end>", the dollar value, the basis points of the fund, and the count.
- Rulings at the cut (issuer): `g5_rows` is a list of row dicts (or a DataFrame, converted); `fund_mv_by_date` is keyed by
  `datetime.date`. The fund's total reported market value includes its cash lines (it is the report's total). A refused window
  has no G5 rows, so "no marker" is: empty rows in, `[]` out. `words()` prints dollars as `$26,000` and dates as ISO.
- **Organic trigger:** the publisher's chart object (RIV-co-1).

### `RIV-co-1` -- the publisher writes one chart object per fund beside the page, with its size line (FWD-22; F.5 items 1 and 4)
- Interface: `publish_page` writes `homes.page(day, "charts/<FUND>.json")` for every fund of the page, in the shape of the shared
  vocabulary, covering exactly the securities whose dialog on the rendered page carries that fund's section
  (`publish_page.dialog_fund_keys(html) -> {fund: [security_key, ...]}`, exported by THIS cell from a regex over the rendered HTML:
  `data-sec-dialog="<key>"` blocks and their `<section data-fund=...>` children; no render.py edit). Built from
  `price_series.load` and `trade_markers.markers`. `CHART_MAX_BYTES = 1_900_000` per object: over it, the 365-day points are
  thinned to weekly (and the object says `"thinned": true`); still over -> the object is not written and the stage prints `FAIL:
  chart object over cap for <FUND>`. The manifest gains `charts: {<FUND>: {"uri", "bytes", "securities", "markers",
  "thinned"}}`. The day's page publishes whether or not a chart object fails. Write once per revision, like audit.html.
- Rulings at the cut (issuer): `dialog_fund_keys(html)` and `CHART_MAX_BYTES` live in `publish_page` (this cell's file) and the
  cap is read at call time. A fund of the page with no dialog section gets NO object and no manifest entry. In the manifest
  `securities` and `markers` are counts. Thinning keeps the last trading day of each ISO week and every day that carries a
  marker's start or end. A fund whose object is refused has the manifest entry `{"uri": null, "bytes": <over-cap bytes>,
  "refused": true}`. `fund_mv_by_date` is the sum of `market_value` over the fund's G1 report of that date.
- **Organic trigger:** the 07:00 ET marker publish.

### `RIV-bf-1` -- an ad hoc Bloomberg close-price backfill over a date range, on the existing market route, under a row budget (FWD-22; F.5 card 2 answer; WORLD)
- Andrew-direct @96d0ab2f4b: "Yes for the rivalfunds funds only ... an ad hoc backfill for the selected funds that uses the
  existing BBG route"; @69c7f24b44: about 365 calendar days. Existing route: `enrichment_bloomberg` mode `market` already sends a
  one-day `HistoricalDataRequest` for a past date (`_market_pull`, `_blp_historical_data`).
- Interface: new mode `market-range` of stage `pull-enrichment`: event `{"mode": "market-range", "start", "end", "securities":
  [...], "batch_id", "sink", "max_points": int, "dry_run": bool}`. It plans `len(securities) x trading days in [start, end]`
  points; `dry_run` returns the plan and spends nothing; if the plan exceeds `max_points`, or exceeds `bbg_budget`'s
  `ceiling - reserve - spent(today)`, it REFUSES before any request, naming the points left. Otherwise ONE historical request
  per batch of 50 securities over `[start, end]` for `px_close`'s field only; it writes one `gold/security_market/date=<D>`
  object per date that has rows (never overwriting an existing object of that date: a date already holding a `market-*.parquet`
  is skipped and counted), each row `as_of_source = "backfill"`; it records the points in the `bbg_budget` ledger with mode
  `market-range`; a tripped session stops the run with what landed stated. No file under `integrations/` changes. The live
  run is the ISSUER's act under a never-widen pair, after the day's 07:00 ET vehicle run; the worker makes NO Bloomberg call.
- Rulings at the cut (issuer): a refusal is `status == "REFUSED"` (the module's own word). The result carries `plan: {"points",
  "securities", "trading_days", "batches"}`; a refusal's detail names the planned points and the points left, where "left" is
  the smaller of `max_points` and the budget remainder. Skipped dates are returned as `skipped_dates` (a list). The ledger
  records the points REQUESTED (securities x trading days of the range), since that is what the vendor was asked for. The
  budget read is a new `bbg_budget.check_points(points, today=None) -> None | detail` beside `check_backfill` (unchanged).
  A tripped session returns `FAILED` naming the dates that landed.
- **Organic trigger:** none (ad hoc by Andrew's word); the negative arm is the daily `market` mode, unchanged.

### `RIV-rt-1` -- the gateway serves a fund's chart object (FWD-22; F.5 item 2; WORLD, released by NFRA_OPLGTW)
- Today `rivalfunds_view` serves `/rivalfunds/<day>` and `/rivalfunds/<day>/audit` (2 MB cap, audit log, identity wall).
- Interface: `rivalfunds_view.chart_key(day, fund)` (the page prefix + `date=<day>/charts/<FUND>.json`; `fund` must match
  `^[A-Z0-9]{1,8}$`) and handler `rivalfunds_chart` for `/rivalfunds/{day}/chart/{fund}`: 200 `application/json` with the
  object's bytes; bad day or bad fund -> 400; no object -> 404 JSON `{"error": "no chart for this fund and day"}`; over the cap
  -> the page's own over-cap refusal; every call audit-logged with `{"day", "fund", "route": "chart"}`. The route is declared
  in `ROUTE_CLASS` as `access-layer` and mounted in `server.py` by this cell.
- Rulings at the cut (issuer): CORRECTION -- the over-cap refusal is the page's own (502, `rivalfunds_view.py` `_serve_day`),
  not a 413. No viewer -> 401 as the other routes. The 200 and the 404 are audit-logged; a 400 and a 401 are not, as today.
  The `server.py` Route and the `ROUTE_CLASS` line are THIS cell's (the lane refuses the issuer's commit there: round 13
  AMENDMENT 1), so both files are in its paths.
- **Organic trigger:** a signed-in click on a security modal after RIV-md-1 is served.

### `RIV-md-1` -- the security modal draws the price curve with the fund's trade markers, by the page's ONE script (FWD-22; F.7)
- Interface: each `<section data-fund=...>` of a security dialog gains a chart frame `<div class=rf-chart data-chart-fund="<FUND>"
  data-chart-key="<security_key>">` holding a three-way range switch (30d first, then 90d, 365d), a words line (`data-chart-status`)
  and the fund's trade list in words (from the context's trades; present with or without the script). The page carries EXACTLY
  ONE inline `<script>` block with no `src`; `_BAD_CONSTRUCTS` admits that one block and still refuses every other script,
  `src=`, `<link`, `@import`, `url(`; `render.script_count(html) -> int`. The script: on a dialog opening, fetches
  `/rivalfunds/<page day>/chart/<FUND>` (same origin, once per fund, cached), draws an inline-SVG curve of the chosen range
  from `points`, breaks the line at gaps and prints each gap's reason, draws each marker as a hollow circle of radius `r` at
  its end date (green buy, red sell; a `span` marker also draws a bar over its window), shows price + date on pointing at any
  part of the curve and the marker's words on a marker, prints `source_words`. On a failed or missing object the status line
  reads "Chart could not load" and the trade list stays. `data-history=none` and HISTORY_NONE leave the dialog.
  The script lands on the SERVED page only after the chart route serves (issuer's sequencing at the deploy).
- Rulings at the cut (issuer): the script is emitted unconditionally by `render_page`; the route-before-script order is the
  issuer's deploy sequence, not a flag. The AUDIT page gets no chart frame and no script, and `validate_audit` /
  `validate_fund` still refuse any script. `data-chart-fund` carries the fund ticker exactly as the route takes it. The range
  switch is three buttons `<button data-chart-range="R30|R90|R365">` reading 30d, 90d, 365d, R30 marked current. The trade
  list is one line per trade from `trade_markers.words` when that module is importable, else the page's own trade words; a
  fund with no trade in the security lists none and says "No trades in the last 365 days".
- **Organic trigger:** opening a security modal from a fund's section on the live page.
