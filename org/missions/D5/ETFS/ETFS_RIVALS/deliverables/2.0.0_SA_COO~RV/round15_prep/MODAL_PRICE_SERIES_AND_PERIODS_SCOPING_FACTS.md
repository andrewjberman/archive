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
