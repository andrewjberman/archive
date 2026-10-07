# Scoping facts for the two Andrew-direct items of 2026-10-07 ~04:5xZ (price-series modal with trade markers; 30d / 90d / 365d)

Author: 2.0.0_SA_COO~RV, 2026-10-07 ~05:0xZ. For 1.0.0_SA_CTO~Z's endpoint. Facts only; no design is proposed here.

Records: `org/tier1_exec/2.0.0_SA_COO/deliverables/cooRV_ANDREW_DIRECT_20261007_045xZ_RIVALFUNDS_SECURITY_MODAL_PRICE_SERIES_WITH_TRADE_MARKERS.md`
and `..._045xZ_RIVALFUNDS_PERIODS_30D_90D_365D_EVERYWHERE.md`.

Claim grades: MEASURED = this seat ran the read this turn. CODE-READ = a read-only subagent's file read (paths and lines given),
not re-read by this seat.

## 1. The price series does not exist at the depth he asks for (MEASURED)

- `s3://opal-data-etfs/rivalfunds/etfs/gold/security_market/` holds **4** `date=` partitions, first 2026-09-29, last 2026-10-05
  (one `s3 ls` of the prefix, 04:58Z).
- `.../gold/trade_schedule/` holds **504** `date=` partitions, first 2024-10-01, last 2026-10-05 (same read).
- So trades reach back about two years and prices four days. A 30d, 90d or 365d curve needs a price history this pipeline does
  not hold.
- CODE-READ: the price table is Bloomberg `PX_LAST` per held security per run date (`enrichment_bloomberg.py` `MARKET_SCHEMA`
  :138-144, `_market_pull` :619-631); it has no multi-day range backfill; a security has a row only on dates a universe fund
  held it.
- Consequence: filling 365 days is a vendor pull. Standing rule: no external vendor call without Andrew's explicit per-use word.
  `integrations/bloomberg/` is also under his no-modify order for the daily Positioning pull. Neither is waived by these two
  messages.

## 2. A trade has a window, not a date (CODE-READ)

- `gold_trade_schedule.py` infers each trade from two consecutive holdings reports as `(window_start, window_end]`; `date`
  equals the window end and "the window is never narrowed to a finer day" (:42-43, :650-651).
- `est_price` is the issuer-implied `market_value / quantity`, not a market print; `est_notional` is the dollar figure.
- There is no percent-of-fund or bps-of-fund column for the trade itself, only `weight_before` and `weight_after`. "Percentage
  of the fund at that time" must be defined (est_notional over the fund's net assets on the window end, or the weight change).
- A marker "on the part of the curve where the purchase occurred" can be placed at the window end; for a widened window
  (`window_trading_days > 1`) the true day is unknown inside it.

## 3. The page cannot run the Market Overview modal as built (CODE-READ)

- Market Overview's modal is React + Recharts in the portal (`portal/src/components/market-performance/IndexPerformanceModal.tsx`):
  ranges 30D / 90D / 1Y / 3Y, default 1Y; a JS hover tooltip showing date and price; data from a static S3 JSON per index.
- The rivalfunds page is static HTML with **no script at all**: `render.py` refuses `<script`, `<link`, ` src=`, `@import`,
  `url(` (`_BAD_CONSTRUCTS` :2161). Its dialogs are HTML `popover` elements; its charts are inline SVG and CSS; its only hover
  text is the native `title` / SVG `<title>`.
- So "almost the same exact modal design" with a live hover tooltip is either (a) inline SVG with native title tooltips and
  CSS-only range switches, inside the no-script rule, or (b) a change to that rule. That is an endpoint decision.
- Size: the main page is 1,279,784 B against the gateway's 2,097,152 B cap, and dialogs are dropped whole above 1,950,000 B.
  171 dialogs each carrying three ranges of a daily series is a size question to settle before the cut.

## 4. The periods (CODE-READ for the period sets; MEASURED for the token census)

- Today's periods: `gold_buying_trend` computes YTD / R30 / MTD / QTD; the security dialog's keys cover R30 and YTD.
- 90d and 365d are new calculations in the gold tables, not relabels. 365d contribution needs 365 days of prices: the same gap
  as section 1.
- Token census over `data/etfs/scripts/rivalfunds/*.py` and its tests for YTD / QTD / MTD / R30 / R90 / R365: 166 occurrences
  in 27 files (this seat's Grep; 5 product files, 22 test files). The AI accounts also name periods (`ai_accounts.py`, 6).
- He named QTD and YTD only. MTD is not named.

## 5. The size budget against `C-PAGE-CAP` (MEASURED 2026-10-07 ~05:1xZ on the served 2026-10-06 index.html, batch rv-publish-1006r14)

- Page 1,279,784 B. Its dialogs block is 446,080 B: **423** security dialogs holding **671** fund sections, of which **365**
  carry a buying line (a fund traded the security), in **276** dialogs. (The 171 in section 3 was the AUDIT page's dialog count,
  the wrong object for this budget; corrected here.)
- `C-PAGE-CAP` asks for 20% headroom under `DIALOG_SOFT_CAP` (1,950,000 B): a ceiling of 1,560,000 B. Room left under it:
  **280,216 B** -- 662 B per dialog, 417 B per fund section, 767 B per traded fund section.
- Under the cap itself (no headroom): 670,216 B -- 1,584 B per dialog.
- Not measured: the bytes of one real curve. An inline SVG path of n points costs roughly 10 to 12 B a point before markers
  (an estimate, not a measurement); three ranges at 21 / 63 / 52 (weekly) points is on the order of 1,500 B a curve. On that
  estimate one curve per dialog does not fit under the 20% ceiling and barely fits under the cap with nothing else added.
- Also unruled by Andrew at this writing: the day unit of 30d / 90d / 365d (trading or calendar); the CTO recommends calendar
  (msg 30607) and has carded it to him.

## 6. The existing Bloomberg route the backfill derives from (CODE-READ by this seat, 2026-10-07 ~05:2xZ; Andrew-direct record `cooRV_ANDREW_DIRECT_20261007_051xZ_RIVALFUNDS_BBG_BACKFILL_YES_PAGE_ONLY_HIDE_MTD.md` @96d0ab2f4b)

- What exists: `enrichment_bloomberg.py` stage `pull-enrichment`, mode `market` (`_market_pull`, :600). For a PAST date it
  already sends a `HistoricalDataRequest` (`_blp_historical_data`, :290, through `integrations/bloomberg/mcp/blp_client`) for
  `MARKET_HIST_FIELDS`, start = end = that one date, in batches of 50 securities (`DEFAULT_BATCH`, :93), and writes the
  `gold/security_market/date=<D>` partition with its marker. `plan-market` is the offline plan of the same.
- So the backfill is this mode over a date RANGE instead of one date: the same client call already takes `start` and `end`.
  Nothing under `integrations/bloomberg/` needs to change (his no-modify order stands). `READ_HERE.md` section 4 states that a
  historical request returns a full `PX_LAST` series.
- The securities: the page's 423 dialog securities on 2026-10-06 (MEASURED from the served index); the set a fund held at
  any time in the range is larger and is not counted here.
- THE HAZARD (from `bbg_budget.py`'s own header): on 2026-10-05 about 175k rows of ad hoc backfill exhausted the Terminal's
  daily capacity and blocked the 07:00 ET production pulls. `bbg_budget.json`: ceiling 150,000 rows a day, production reserve
  30,000. `check_backfill` guards the HOLDINGS collector only; the market pull does not call it, and whether historical
  price points draw on the same capacity meter is NOT known to this seat.
- Size of the pull, an estimate: 423 securities x about 252 trading days = about 107,000 price points for one year (more if
  the unit is trading days: 365 of them reach back about 17 months).
- Therefore: the backfill is a WORLD cell with its own budget guard, run AFTER the day's 11:00Z vehicle run and never before
  it, split across days if the estimate does not fit under ceiling less reserve.
