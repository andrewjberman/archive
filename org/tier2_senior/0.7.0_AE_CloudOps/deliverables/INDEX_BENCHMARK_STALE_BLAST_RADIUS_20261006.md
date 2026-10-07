# The served blast radius of CTO~Z ruling 5e0c045e8d step (1) -- 171 cells flip from a number to null

**Measured by:** `0.7.0_AE_CloudOps~RV`, 2026-10-06 ~13:5xZ. **Read-only; nothing was changed.**
**For:** whoever `0.0.0_AB_MSTR~Z` seats on step (1), and the never-widen pair the ruling names.
**Not a trace.** The cause is settled by `4.0.0_SA_CRO~Z` @`bfe10cb2a4` (7 CIX definitions stopped after 2026-09-29) and the
fix route by `1.0.0_SA_CTO~Z` @`5e0c045e8d`. This is the one figure neither produces: **how much served output step (1)
moves.** NEVER-1 requires a sign-off to name its blast radius, and the half cannot be written without this.

## The artifact

`s3://opal-data-portal-v2/json/benchmarks/model_portfolio_benchmarks.json`, LastModified **2026-10-06T12:31:21Z**
(s3api, UTC), 19,190 B, `data_as_of` **2026-10-05**. Producer:
`infra/aws/lambda/v2_portal/yang_pipeline/portfolios/yang-model-portfolio-benchmarks/lambda_function.py`, `OUTPUT_KEY_COMPREHENSIVE` `:48`.

## The partition -- 300 cells, MECE, nothing unexplained

Denominator: **5 models x 10 periods x 6 benchmark-derived fields = 300**. Fields: `index_benchmark`, `etf_benchmark`,
`index_spread`, `etf_spread`, `index_benchmark_volatility`, `etf_benchmark_volatility`.

| bucket | cells | what it is |
|---|---|---|
| **stale-sourced, SERVING A NUMBER** | **171** | **the silent half.** `compound_returns` does `returns_pct.dropna()` (`:561`), so these compound a window that ends 2026-09-29 while `data_as_of` says 2026-10-05. They look right. |
| stale-sourced, serving null | 99 | the visible N/A Yang reported |
| current-sourced, serving a number | 27 | correct today -- every one is the INT model's `etf_*`, and `.INT_ETF` reaches 10-05 |
| current-sourced, serving null | 3 | NOT a defect: `INT` `etf_benchmark_volatility` at WTD/MTD/QTD, explained by `calculate_volatility(min_points=5)` (`:567-570`) on windows 5 trading days old or less (Q4 and the month began 10-01) |

**171 + 99 + 27 + 3 = 300.** No residue.

The silent half by period: `1M` 27, `1Q` 27, `YTD` 27, `1Y` 27, `Since Inception` 27, `TTW` 27, `1D` 9.
`WTD`/`MTD`/`QTD` contribute 0 to it -- their windows lie entirely after 09-29, so they are all-NaN and already serve null.
**The periods a reader is most likely to quote -- YTD, 1Y, Since Inception -- are the ones serving a wrong number, not an N/A.**

## How the staleness was attributed, so the figure can be rechecked

Source mapping read from the producer's own rule (`:81-110`), not inferred from the output: `index_benchmark` <-
`"<Term> Benchmark"`, `etf_benchmark` <- `"<Term> ETF"`, and **ULT uses the Long Term pair** because the source carries no
Ultra-Long series (by design). Stale sets from CRO~Z's live Bloomberg read: all four `*_BMK` (`UST ST INT LT`) stopped
2026-09-29; of the ETF series `UST_ETF ST_ETF LT_ETF` stopped and **`.INT_ETF` is current to 10-05**.

**Two controls, both fired as required:**
1. The INT model's 30 `etf_*` cells must be flagged stale **0** times, since `.INT_ETF` is current -- measured 0.
   Had the mapping been wrong, this would have read 30.
2. ULT must resolve through the **LT** series, not a non-existent ULT one -- measured `ULT -> LT`, index stale `True`.

Without control 1 the partition would be unfalsifiable: a mapping that marked everything stale would produce a bigger,
more alarming number and no read would contradict it.

## What this means for step (1)

Step (1) makes a stale series serve null with `benchmark_last_date`. So the pair is signing a change that **turns 171
served numbers into nulls** and leaves 99 nulls as they are. That is a large, visible, intended regression in filled
cells -- the panel gets emptier, and that is the point: those numbers are wrong now. The half should say so in both
directions, because a reader who sees the panel lose 171 values without the ruling in hand will read it as a new outage.

**Not measured here, stated rather than implied:**
- Whether any OTHER consumer reads `model_portfolio_benchmarks.json` and would also show the flip. I checked the
  producer, not the readers; a consumer census is the seated cell's, and the sign-off needs it.
- `OUTPUT_KEY_LEGACY` (`json/benchmarks/benchmark_returns.json`) and `OUTPUT_KEY_TIMESERIES`
  (`json/benchmarks/model_portfolio_timeseries.json`) carry benchmark data too and were NOT partitioned. The 300 above
  is the comprehensive key alone. Three keys ship from this Lambda; one was measured.
- Steps (2) the CIX re-save and (3) the re-pull restore the data. After those, these 171 cells carry correct numbers
  again and step (1)'s guard goes quiet. Step (1) is not the fix; it stops the wrong answer being served while the fix
  is arranged.
