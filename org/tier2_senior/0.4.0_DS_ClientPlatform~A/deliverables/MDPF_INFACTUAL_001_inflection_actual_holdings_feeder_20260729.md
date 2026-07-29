# MDPF_INFACTUAL.001 — Inflection ETF actual-holdings feeder (WS-C)

**Agent:** 0.4.0_DS_ClientPlatform~A · **Date:** 2026-07-29 · **Status:** built, exercised, DORMANT (no S3 upload; activation is CTO's gate, post-fires)
**Authority:** Andrew-direct ~2144Z (@11599d60f4) + ~0016Z; TO @991a04d761; Amendment 1 ~0024Z.
**Deliverable:** `data/mdpf/scripts/feeders/wsc_inflection_held_etf.py` — PURE-ADD; zero aggregator edits.

## What it does

Replaces inflection's `model_aua x target_weight` ESTIMATE of Opal-ETF holdings with the MEASURED
position value, summed from Orion custody. Emits the convergent `partner_held_etf` artifact
(`mdpf/feeds/partner_held_etf/inflection/{date}.parquet`), column-contract-identical to the 49F
sibling (`wsd_partner_held_etf.py`). The aggregator's `read_feeder_s3` (:227-245) sweeps every firm
subdir and `build_etf_decomposition`'s override loop (:446-450) is keyed `(firm_id, ticker)`
firm-agnostically — the artifact is consumed with no aggregator change (the WS-D.2 handoff's own
design, `HANDOFF_DSA_wsd2_aggregator_wire.md:114-117`).

## Source resolution (TO §4 caveats — both settled by enumeration)

- **Caveat 1 (eclipse vs orion):** ETF holdings are a custody quantity → ORION. Confirmed the
  handoff doc's "Eclipse-positions" naming is stale: all 4 eclipse silver tables enumerated +
  schema-probed on their newest partitions — `fact_portfolios_full` (849 rows, portfolio grain),
  `fact_portfolios_simple` (837, account-map), `fact_models` (18, metadata),
  `fact_model_composition` (9, model metadata + model-level modelAUM). **Zero ticker / symbol /
  cusip / isin columns in any.** Eclipse cannot answer ticker-level holdings; Amendment 1's parity
  leg reported NOT BUILDABLE (COO carrying to Andrew); no synthesis from weights.
- **Caveat 2 (fact_assets vs fact_positions):** both exist, BOTH 2,283 partitions
  (floor **2020-04-28**, newest 2026-07-28), byte-identical on
  `(accountId, ticker, currentValue, currentShares)` at 07-28 (35,098 rows / 943 accounts each;
  `_feed=assets` vs `_feed=positions` — twin conversions of two vendor feeds).
  **PICK: `fact_assets`** (CTO-verified schema; CTO-RATIFIED 00:37Z). Twin banked as an E-pass
  curiosity by CTO.

## Population declaration (COO ruling 00:36Z — declared-PURPOSE rule)

`PURPOSE = "actual-held Opal-ETF market value, whole-custody-book population (all orion
fact_assets accounts), firm=inflection"` — declared in-module AND in the artifact's parquet file
metadata (`opal.purpose`). The 49F sibling sums the **whole Schwab RPS custody book**
(ticker-filter only, no model scoping — `wsd_partner_held_etf.py:131-155`), so both legs use the
same population class and the cross-firm decomposition compares like with like. The replacement
deliberately widens population vs the estimate (556 model accounts → 943 whole book): the honest
answer to "how much does the firm hold."

## ⚠ NAMED DISCLOSURE (CTO condition (a), 00:37Z)

Until the cutover producer's provenance block lands, the aggregate's `attribution_basis` will read
**`rps_actual:49financial,inflection`** — the legacy aggregator hardcodes the `rps_actual:` prefix
for every override firm (`mdpf_aggregate_aua.py:457`). **For inflection this label is COARSE: the
true source is `source_pipeline=orion_assets`**, carried per-row in the feeder artifact and in its
file metadata (`opal.disclosure`). Do not cite the basis string as provenance for inflection. The
honest per-firm label (`positions_actual:inflection`) is a Ruling-1-held aggregator edit, deferred
to the cutover producer spec (CTO adding to R7 provenance-block requirements).

## Measured values @ 2026-07-28 (before → after)

| Ticker | Estimate (served) | Measured (orion) | Δ | accounts |
|---|---|---|---|---|
| DIVZ | 18,382,174.73 | 18,512,156.58 | +0.71% | 581 |
| IDVZ | 17,367,784.99 | 14,155,735.71 | −18.5% | 581 |
| PFDE | 14,300,934.55 | 11,412,064.92 | −20.2% | 584 |
| PFOE | 8,215,381.40 | 6,535,547.90 | −20.4% | 584 |
| **Total** | **58,266,275.67** | **50,615,505.11** | **−13.1%** | |

**Scan denominator:** 35,098 position rows / 943 distinct accountIds, partition date=2026-07-28,
asOfDate uniformly 2026-07-28. **Predicate:** `ticker.upper().strip() == ETF` for
ETF ∈ {DIVZ, IDVZ, PFDE, PFOE}. Positive control: top custody tickers IEFA $20.3mm, DIVZ, SPYM,
IDVZ, PFDE, BIV — plausible book; zero name-based or ISIN-routed rows outside the ticker match
(ETF rows carry `isin=None`).

**Directional gate:** the briefed −1..−3% envelope was COO-retracted 00:34Z as a 49F-population
mis-import; CTO re-based the envelope 00:37Z — this measurement is the inflection baseline.
Deviation investigated before acceptance: join verified on 4 independent axes (predicate
completeness, T-0 asOfDate, 1-row-per-account×ticker grain, twin-table cross-agreement), then the
**population discriminator** (COO-gated): orion total $203,315,820.14 / 943 accounts vs inflection
model_aua $142,136,388.37 / 556 accounts, containment 549/556 matched by accountId + 7 unmatched
are synthetic `portfolio_*` ids summing to exactly $0.00 → **100% of model value inside the custody
feed. The −13.1% is real model-vs-custody drift** (DIVZ held slightly over target; the other three
~18–20% under). GATE CLEARED (COO 00:36Z).

## Acceptance evidence (all exercised 2026-07-29 00:35–00:42Z)

1. **Feeder run** rc=0, artifact 4 rows, values above, metadata verified present.
2. **attribution_basis flips**: `rps_actual:49financial;target_weight:inflection` →
   `rps_actual:49financial,inflection` on all 4 tickers + `meta.etf_attribution` (with the named
   disclosure above).
3. **`verify_wsd2_clears_identity2.py --date 2026-07-28`**: PASS (production state unchanged —
   artifact not uploaded; post-activation residuals only INCREASE, away from the identity_2 gate:
   min_public_residual 10,334,507.51 → 12,014,341.01).
4. **`mdpf_aggregate_aua.py --date 2026-07-28 --source s3 --dry-run`**: exit 0, reconciliation
   overall PASS, headline $1,783,405,733.70.
5. **FULL-AXIS diff** (local fixture with/without the artifact; fixture-parity control: local
   baseline `etf_decomposition` IDENTICAL to the s3 run): **34 differing leaf paths, every one
   named and explained** — 24 = intended per-ticker override effects (held, ownership_pct,
   held_total, public_ownership_pct, public_residual, basis × 4 tickers), 5 = basis/meta flips,
   plus `aggregate.etf_public_residual_total` +$7,650,770.56 (= exactly the estimate−measured
   delta moving from partner-held to public residual; **headline `opal_aggregate_aua` UNCHANGED**),
   `sentinel_1.today_cohort0` (same quantity; +4.9% DoD, far under the 50% threshold — no
   activation-day trip), `identity_2.min_public_residual` (up, safer),
   `source_vintage.by_feeder.partner_held_etf.inflection` ABSENT→2026-07-28, and 2 run timestamps.
   **No unexplained mover.**
6. **comp-validate**: NO CONFIG for the mdpf feeder class (neither this feeder nor the 49F sibling
   is among the 21 configured scripts) → **UNVALIDATED by that instrument, not signaled SAFE**;
   validation is the exercised chain above.

## Non-negotiables held

- **No silent target_weight fallback**: missing partition → RuntimeError, NO artifact, aggregator
  estimate path applies with honest basis. Zero/negative held → rc=1, no write.
- **No backfill from weights**: coverage floor 2020-04-28 stated; actuals only where positions exist.
- **No aggregator edit · no alarms/monitors · no schedule work · 49F leg untouched · no deploy/apply.**
- Rule 15 (`from __future__ import annotations`) ✓ · Rule 17 (business logic in a feeder, not
  silver) ✓ · commit-no-push (COO is push operator) ✓.

## Activation path (NOT tonight — CTO gate, post-fires)

(1) CTO GO → upload the 07-28 artifact (or fresher); (2) AE chain wiring adds the feeder to the
scheduled daily run (WO-4c/5 territory — a production pipeline must have a schedule); (3) basis
label edit rides the cutover producer (R7). First activated run moves cohort_0 +$7.65mm (+4.9% DoD,
under sentinel-1's 50%); identity_2 stays PASS with wider margin.
