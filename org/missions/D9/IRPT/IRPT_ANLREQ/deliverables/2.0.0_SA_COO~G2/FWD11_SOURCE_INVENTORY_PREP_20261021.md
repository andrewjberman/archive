# FWD-11 (parity) source inventory -- scoping input, 2026-10-21

**Claim class: INFERRED.** Compiled by a read-only research subagent for `2.0.0_SA_COO~G2` while the r34r apply waits on the gateway window. The issuer spot-checked two claims against the files (`held_data.py` line 185 reads "bond-sleeve look-through share; no Opal table holds it per holding"; `portal/src/components/ReturnVolatilityScatter.tsx` exists); line numbers below are approximate and the phrase "holds a market cap and no bucket" was not found verbatim. Nothing here is measured against a live source. It is input to the FWD-11 decomposition (PRD v0.28, FWD-11 at `prd/IRPT_ANLREQ_PRD.md` lines 125-133), to be re-read at HEAD before any cell is cut. `YR` = `infra/aws/lambda/investor-reporting/ycharts/research`.

| Kind (FWD-11) | Where it lives | Coverage | Verdict |
|---|---|---|---|
| 1 Region and country | Portfolio: `YR/held_data.py` ~42-70 maps `CNTRY_OF_DOMICILE` from `opal-data-etfs/bbg/<date>/characteristics.parquet`; models: `segment.geography` from an inline ETF mapping (yang positioning lambda); Opal ETFs: `derived_geo_allocation.parquet` | the 4 Opal ETFs' constituents plus GLD and VXX; 10 countries decided | PARTIAL: no arbitrary ETF or fund; model grain is the ETF label, not look-through |
| 2 Style box, market cap | market cap mean (`held_data.py` ~147); no style-box or cap-bucket source | portfolio only | PARTIAL (style box NOT-HELD) |
| 3 Sector | portfolio GICS (`held_data.py` ~25-40); models `segment.sector` from the `etf-classifications` registry; Opal ETFs `derived_sector_allocation` | same universe | PARTIAL: ETF and fund comparables carry only `asset_class` (`YR/opal_producer.py` ~450) |
| 4 Bond sector | `held_data.py` ~184-185: no Opal table holds it per holding | none | NOT-HELD |
| 5 Credit quality, maturity | credit quality has no rule; maturity only as model `segment.maturity` for FI ETFs; duration empty for every holding | models only | PARTIAL: no rating or maturity buckets for any comparable |
| 6 Fundamentals | dividend yield, expense ratio, market cap, holdings count only; P/E, P/B, P/S not among the 14 characteristics columns; single-stock fundamentals via the Bloomberg harvest | individual equities only | PARTIAL |
| 7 Risk/reward scatter | Opal computes std dev, Sharpe, Sortino, drawdown, alpha and beta from prices (`YR/comparables.py`); the report layout has no scatter method; the portal has `ReturnVolatilityScatter.tsx` | anything with a price series | PARTIAL: computable, not rendered in the report |
| 8 Standardized returns | periodic returns 1m to 10y (`comparables.py`, `layout_overview.py`); model series from `json/benchmarks/model_portfolio_timeseries.json` (inception 2024-04-30); month-end or quarter-end as-of not found | any ticker Yahoo or YCharts prices; models cannot have 3y, 5y, 10y | PARTIAL |
| 9 Holdings tables | portfolio `HOLDINGS_CLASSIFIED`; models `current_holdings` in `json/positioning/positioning_data.json`; Opal ETFs `gold/holding`; 13 rival funds `rivalfunds/etfs/gold/canonical_shape` | those groups only | PARTIAL: no top-holdings renderer for comparables |

## Largest gaps (for the decomposition)
1. Look-through exposure for an arbitrary ETF or mutual fund (kinds 1, 2, 3, 5): the characteristics table covers the Opal-ETF-constituent universe only, and no mutual-fund source was found (searched `data/`, `integrations/`, `infra/aws/lambda`, `lib/`).
2. Style box, bond sector, credit quality and maturity buckets have no source anywhere (kinds 2, 4, 5).
3. Fund-level P/E, P/B, P/S are not held (kind 6).
4. The model-weights extract `{as_of: {model_code: {ticker: weight}}}` of the CTO ruling is not in code.
5. The scatter and top-holdings views have no renderer.

## What this means for FWD-11's ACCEPT line
The ACCEPT line allows "a plain sentence saying why it is missing for that comparable" (FWD-12 wording). On the inventory, the first Opal parity report would fill: standardized returns (kind 8, for the portfolio and ETF comparables), sector and region for the portfolio and the Opal ETFs (kinds 1 and 3), the scatter (kind 7, new renderer on held computations), holdings for the portfolio and the models (kind 9, partly), and would say "not available for <comparable>: <reason>" for the rest until sources are bought or built. The sources the PRD's brief (O3) leaves to the CRO, and Andrew's 22Z records (recreate the YCharts packet content from data we hold; Bloomberg without limits), decide how many of the NOT-HELD kinds become buildable: that is the CTO and CRO's fold, not this note.

Not claimed: that any "HELD/PARTIAL" is current (freshness mechanisms were read from the catalogue, not measured), or that a gap is final (a miss in the searched paths is not an absence).
