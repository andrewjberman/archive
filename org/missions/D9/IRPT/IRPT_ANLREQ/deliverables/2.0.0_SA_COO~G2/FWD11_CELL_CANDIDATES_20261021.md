# FWD-11 (parity): candidate cells for the round after FWD-10 -- issuer's prep, 2026-10-21

**From:** `2.0.0_SA_COO~G2`. **Status:** a PROPOSAL held for the CTO's round analysis. No order is cut from it: the spec and the decomposition are the CTO's and the round's (the PRD says FWD-11 starts as soon as FWD-10 is met; FWD-10's grade waits on run 7M, the CVO's L9 and the L10 slug). **Claim class: INFERRED** from `FWD11_SOURCE_INVENTORY_PREP_20261021.md` (a research subagent's read, two claims spot-checked by the issuer) and from this seat's own reading of the producer and layout code.

## Ordering rule
Cells that Opal can fill from data it already holds and prices it already reads come first, each built the way round 60 built FWD-10: a checker file that runs the REAL producer on the REAL map over a synthetic world and computes its expected values independently, dry-run at the base (FAIL), calibrated against a reference fix and mutants, then a worker, then my merge and full-tree re-run. Where a source is NOT HELD, the report prints a plain sentence saying why (the ACCEPT line allows it); acquiring a source is a separate call, not a cell.

| id | kind (FWD-11) | what the cell produces | source it reads | held? | write set (expected) |
|---|---|---|---|---|---|
| C1 | 8 standardized returns | month-end and quarter-end as-of rows beside the periodic returns, for the portfolio, models and ETF comparables | the price paths already used by `comparables.py`; model series `json/benchmarks/model_portfolio_timeseries.json` | YES (models have no 3y/5y/10y: a sentence) | `comparables.py`, `layout_overview.py`, tests |
| C2 | 7 risk/reward scatter | a scatter of return against standard deviation for the portfolio and every comparable | the std dev and returns the section already computes | YES | `layout_overview.py` (a new method), the maps' element, tests |
| C3 | 9 holdings tables | a top-holdings table for the portfolio and for each Opal model (and the Opal ETFs); a sentence for any comparable with no holdings source | portfolio `HOLDINGS_CLASSIFIED`; models `current_holdings` in `json/positioning/positioning_data.json`; Opal ETFs `gold/holding` | PARTIAL | `model_source.py`, `comparables.py`, `layout_overview.py`, tests |
| C4 | 1, 3 region and sector | region and sector breakdown for the portfolio and the models; ETF comparables carry only an asset class, so a sentence | `held_data.py` (portfolio), `segment.geography` and `segment.sector` (models) | PARTIAL | `model_source.py`, `comparables.py`, `layout_overview.py`, tests |
| C5 | 6 fundamentals | dividend yield, expense ratio, market cap, holdings count for the portfolio and ETF comparables; P/E, P/B, P/S as a sentence | `characteristics.parquet` via `held_data.py` | PARTIAL | `comparables.py`, `layout_overview.py`, tests |
| C6 | 2, 4, 5 style box, bond sector, credit quality, maturity | one sentence per kind and comparable saying why it is missing | none held | NOT HELD | `layout_overview.py`, tests |

C3 to C6 share `comparables.py` and `layout_overview.py`; under the write-set rule they are one chain for one worker, or are split by file after the first merge. C1 and C2 touch the same two files, so the honest fan-out is 1 to 2 chains, not 6.

## Needs a call before it can be a cell
1. A source for look-through exposure of an arbitrary ETF or mutual fund (kinds 1, 2, 3, 5): the characteristics table covers the Opal-ETF-constituent universe only. A vendor field or a new held table is a CTO/CRO decision.
2. A model-weights extract `{as_of: {model_code: {ticker: weight}}}` (the CTO ruling names it; not in code).
3. Whether the scatter belongs on the Multi-Comp only or on the Comparison too.

## Live proof
Each cell's real run is one Multi-Comp filing with a typed ETF, as in run 7M, read page by page against recomputation (the existing `checks/fwd10_read.py`, `fwd10_portfolio.py`, `fwd10_etf_row.py` carry the conventions).
