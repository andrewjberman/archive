# The comparison and multi maps' price pages: what exists, what round 58 is (measured 2026-10-19)

Issuer `2.0.0_SA_COO~G2`, on CTO msg 10768 ("all three maps carry price pages; measure comparison and multi now"). Method and output: `checks/price_pages_inventory_maps.py` and `PRICE_PAGES_COMPARISON_MULTI_OUTPUT_20261019.txt` (same folder): the SHIPPED Opal producer over the REAL maps, the round-57 checker's fixtures, pricing off then on. Claim: MEASURED on the code at HEAD; NOT a live run; a vendor-call count is an UPPER BOUND for price-based elements (the `key_stats` call also carries non-price rows such as Net Expense Ratio and Cash Net Allocation).

## What is measured

| | overview (round 57) | comparison | multi |
|---|---|---|---|
| map elements | 254 | 574 | 424 |
| Opal-wired elements (OWN_SERIES or OPAL_HELD) | 167 (158 + 9, from `PRICE_PAGES_INVENTORY_OUTPUT_20261019.txt`) | **0** | **0** |
| moved by turning pricing on | 9 | **0** | **0** |
| vendor-call elements (all NOT_IN_THIS_VERSION) | 22 | 351 | 144 |
| of which price-based calls (upper bound) | 15 | 45 | 50 |
| price-based, `portfolio_*` side | 15 | 26 | 23 |
| price-based, `comparison_*` side | 0 | 19 | 27 |

Reading: the comparison and multi maps were never wired to Opal data. Only the overview map was (IRPT_YCDGEN YCD-w-3 and YCD-w-5). On the other two maps, EVERYTHING but the producer's three classified elements reads NOT_IN_THIS_VERSION, price or not: 306 (comparison) and 94 (multi) non-price vendor-call elements are unwired too (exposure, fundamentals, allocation). C-V1 lifting by itself changes nothing on them.

The price-based calls on those maps: `*_risk_stats` (22 comparison, 32 multi), `*_key_stats` (10, 4), `*_level_series` (5, 6), `*_returns` (5, 4), `*_standardized_returns` (2, 3), `*_scatter` (1, 1). Pages: comparison p2, p9, p10, p11, p19; multi p2, p3, p10, p11, p12, p14, p21, p22.

## What round 58 would be (a proposal, not yet cut)

- **The `portfolio_*` side (26 comparison, 23 multi)** reuses round 57's forms: the same statistics (`total_return_*`, `std_dev_*`, `beta_*`, `alpha_*`, `sharpe_*`, `sortino_*`, `max_drawdown_*`, `cumulative_series`, `drawdown_series`, `annual_returns`) pointed at the map's elements. One map-only cell per map, after round 57 merges.
- **The `comparison_*` side (19 comparison, 27 multi)** needs a SECOND portfolio's level series: a new structure (the producer builds ONE buy-and-hold series today). What the comparison portfolio is in an Analysis Request (the swapped portfolio against the original? a model? the benchmark?) is not decided anywhere I have read. Not cut until it is.
- **`*_scatter` and `*_standardized_returns`** are new forms on any map (the overview's scatter was named out of round 57). Their own cells, if wanted.

## NOT measured

A live run of a comparison or multi report; which map Andrew's 13:43Z request used (Y2 reads it); how the resident picks a map for a request (the C-SWITCH branch); the rendered pages.
