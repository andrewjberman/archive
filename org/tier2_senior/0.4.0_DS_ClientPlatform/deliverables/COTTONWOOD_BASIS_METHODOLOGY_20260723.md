# COTTONWOOD BASIS METHODOLOGY — the two-source overlay, recorded

**Authority:** Andrew-direct 2026-07-23 ~134xZ (via COO 134545Z, verbatim): *"We're pulling the
models from their 'rebalance' domain, and overlaying 'datamining' holdings for values."*
**Author:** 0.4.0_DS_ClientPlatform. **Referenced from:** every cottonwood-basis-bearing artifact's
`meta` (pair, distribution, Global spine, radial). **Grounding vintage:** @HEAD 2026-07-23 (line
citations below at their committing revisions).

## The structure (grounded, Rule 22)

Cottonwood AUM is a **TWO-SOURCE OVERLAY**, never a single feed:

1. **MODEL MEMBERSHIP — the BD REBALANCE domain** (which accounts belong to which models):
   - Bronze: the daily Rebalancer pull — `rebalancer_models` (the 60-model roster),
     `rebalancer_model_detail` (definitions + blend trees + createdAt), `rebalancer_accounts`
     (the 911-account book with per-account `strategyName`).
   - Silver: `rebalancer_schemas.SILVER_FEED` (`data/assets/scripts/silver/rebalancer_schemas.py:49-53`
     @`1351c74d9`) maps that domain to `fact_model_roster` / `fact_model_definition` +
     `fact_model_blend` / `fact_model_assignment`.
   - Gold: `build_dim_model_portfolio.build()` resolves membership — assignment
     `strategy_name` → roster model (`data/assets/scripts/gold/build_dim_model_portfolio.py:219-224`
     @`8a7208a70` lineage), blend-decomposed to the archetypal ladder via `decompose()`
     (`:152-180`), +1 count per leaf / dollars split by weight (`:251-252`).

2. **DOLLAR VALUES — the BD DATAMINING domain, overlaid** (what each account is worth):
   - Bronze: the DataMining `HOLDINGS_DAILY_{date}.xlsx` export → monolith
     `blackdiamond/cottonwood/silver/fact_holdings` (raw vendor headers preserved).
   - The overlay: `build_dim_model_portfolio.account_values()`
     (`build_dim_model_portfolio.py:132-146`) sums `Market Value` per `AccountID` from
     `fact_holdings` (`HOLDINGS_PREFIX` `:59`); `build()` joins values onto membership at
     `:216,:236-240`.

3. **THE JOIN:** Rebalancer `externalId` == DataMining `AccountID` — string equality, both
   z09-prefixed, NO int coercion (CRO join spec, banked 211136Z 07-22; exercised 296/296).

**Every downstream cottonwood artifact inherits this overlay:** the G8 pair
(`build_cottonwood_mdpf_pair.build_units` wires `bdmp.account_values` + assignment), the trend
slice (reads the dim), the interpolated band (same two sources + the labeled fuzzy overlay), the
Global fold + radial (consume those artifacts).

## Why two dates ride every artifact (the TWO-DATES law, direct consequence)

Because the sources are two DIFFERENT feeds with different cadences, `date=` (assignment/pull
date, Rebalancer) and `value_date` (dollars as-of, DataMining holdings) are carried separately on
every row/artifact — conflating them would present one domain's vintage as the other's.

## Methodology notes bound to this basis

- **fee_scope = model**: only Rebalancer-modeled AUA enters the fee basis (vs 49F full-book).
- **The band's fuzzy overlay** (historical only): assignment history is reconstructed by
  basket-matching against Rebalancer target definitions, labeled `interpolated_estimate`,
  match-epsilon-suppressed (measured valley 0.10) — because **the Rebalancer domain is
  live-state-only and DataMining assignment history is CURRENT-STAMPED** (CRO verdict 042824Z):
  real historical VALUES exist; real historical MEMBERSHIP does not. The two-source split is
  exactly why the band's custody cohort can be measured while its model cohort is estimated.
- **Basis reference in artifacts:** `partners_basis.cottonwood = "bd-rebalancer-models +
  bd-datamining-values"` (the self-describing short form) + the structured
  `meta.cottonwood_basis` block {model_source, value_source, join, methodology} pointing here.

**The prior label `bd-datamining-holdings` named only the VALUE source — corrected 2026-07-23 per
Andrew's directive; this document is the standing record.**
