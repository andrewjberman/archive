# The Opal-built report's price pages: what exists, what is missing (measured 2026-10-19)

Issuer `2.0.0_SA_COO~G2`. Trigger: Andrew-direct "all holds are lifted" (`org/tier1_exec/1.0.0_SA_CTO/deliverables/ANDREW_DIRECT_20261019_144xZ_ALL_HOLDS_LIFTED.md` @93efb20243; CTO msg 10729, 10734): row 3c22, C-V1 (IRPT_YCDGEN PRD :251) lifts. Method and output: `checks/price_pages_inventory.py` and `PRICE_PAGES_INVENTORY_OUTPUT_20261019.txt` (same folder): the SHIPPED producer over the REAL `overview_map.json` (254 elements; 257 with the three classified elements the producer adds), the repository's own fixtures and made-up prices, pricing off then on. Claim: MEASURED on the code at HEAD 1855ec7d0b; NOT a live run; the comparison and multi maps are NOT measured.

## What exists (C-V1 is already half-built behind a switch)

- `opal_producer.py` has a price stage (AR-g-86, AR-g-93): `pricing` truthy runs it; absent it, every price element reads `NOT_IN_THIS_VERSION`. The resident's r34k binding has `opal_pricing_binding {"enabled": true, "tiers": ["estate","yfinance","ycharts"]}`, so the stage is on in the running resident. The benchmark is SPY and the risk-free proxy is BIL (CTO's proxies, AR-g-93), priced through the same tier chain.
- Turning pricing on moves **9 of 254** elements to VALUE: p2.e08 Periodic Return chart, p2.e13 Periodic Return table, p6.e22 Drawdown Info table, p7.e02 Alpha, p7.e03 Beta, p7.e05 Sharpe, p7.e06 Sortino, p7.e07 Max Drawdown, p7.e08 Monthly VaR. These are all `OWN_SERIES`, 1-year statistics.

## What is missing: 17 price-based elements still `NOT_IN_THIS_VERSION` with pricing on

Of 157 elements still unavailable with pricing on (65 BUILDER_ONLY static text, 70 OPAL_HELD with no rule, 22 VENDOR_SOURCED), these 17 need a price series or a statistic of one:

| page | element | what | map source now |
|---|---|---|---|
| p2 | e03 legend, e04 chart | Cumulative Return & Basic Info | VENDOR `portfolio_info`, `portfolio_level_series` |
| p2 | e07 text | Periodic Return as-of date | VENDOR `portfolio_level_series` |
| p2 | e14 number | Key Stats: YTD Total Returns | VENDOR `portfolio_snapshot_metrics` |
| p2 | e16 text, e17 chart, e18 table | Annual Return - Total | VENDOR `portfolio_level_series` |
| p2 | e11 number, e15 number | Key Stats: Beta (5Y), Alpha (5Y) | OPAL_HELD, no rule (NO_RULE) |
| p6 | e20 legend, e21 chart | Drawdown Info | VENDOR `portfolio_info`, `portfolio_level_series` |
| p7 | e04 table | Risk Info: Standard Deviation | VENDOR `portfolio_snapshot_metrics` |
| p7 | e10, e13 tables; e11, e12 charts | Risk/Reward: Return, Standard Deviation, two charts | VENDOR `portfolio_snapshot_metrics` |
| p7 | e15 chart | Benchmark level series (input to Alpha and Beta) | VENDOR `benchmark_level_series` |

## Not price pages (named so they are not swept in)

Distribution Yield (p2.e10, p8.e05), Current Yield (p8.e15), Yield to Maturity (p8.e17): dividend and bond data, FWD-10, no price tier serves them. Risk/Reward Scatter Plot (p8.e02, `portfolio_scatter_documented_ids`) and Fundamentals ROA/ROE (p8.e08, e13): vendor-specific. Stock Style, Market Classification, Region, Stock Sector charts (p3.e24-e26, p5.e34): fund look-through, not prices.

## Open scope question (to the CTO)

The map holds **no price-table element**; the CTO's list names "returns, risk, price table". A per-holding price table (ticker, last price date, source claim: estate, yfinance or ycharts) would be a NEW element, not an unlock. NOT built until the CTO says what it shows.

## NOT measured

The comparison and multi maps; a live priced request (window 5's first YCharts-tier answer is still owed); the rendered PDF of any price page (this run reads `run.json` entries, not the pixels); whether SPY/BIL price through all three tiers (the fixture serves them from the estate tier).
