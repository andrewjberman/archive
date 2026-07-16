# Casebook G→C MAP DRAFT — the seed→monolith correspondence record, for CTO fold + sign

**TO:** OPAL_GLDRNS.A4 L4 | **Author:** 0.4.0_DS_ClientPlatform~A | 2026-07-16 ~18:0xZ
**Status: DRAFT — awaiting CTO fold into `docs/architecture/OPAL_RUNNERS_CANONICAL_FORM_CASEBOOK.md`**
(casebook is CTO-lane per the owned-paths gate; the WAVE3_SPEC precedent — lane drafts, CTO folds).
**The TO's own words for this leg:** *"Map the G→C correspondence explicitly in L0's casebook entry
set — the record, not tribal memory, carries which seed script became which C unit."* G-numbers below
are read from each seed script's OWN header (grep of `data/canonical/schwab/gold/`, 2026-07-16), not
asserted from memory; the two unnumbered headers are flagged as such.

---

## THE G→C MAP (seed `data/canonical/schwab/gold/` → monolith `data/assets/scripts/gold/runners_49f/`)

| G | seed script | monolith unit | status @ 2026-07-16 | port notes |
|---|---|---|---|---|
| G2 | build_gold_account_gains.py (header self-labels "gold-B"; G2 per the build plan + the landed core's citation) | **C_00.account_gains** | **PORTED** (A4 L1, 64c7fa7dd) | daily-atomic re-grain; NNA legs IMPORTED from C_03's core (never copied); F-AMT amount/direction oracle |
| G3 | build_gold_canonical_lots.py | **B_00.lots** | rides the lots disposition legs (B_01/B_01b/B_02, per Entry-5 footer) | union fact_uln+fact_rld; no FIFO anywhere |
| G4 | build_gold_account_performance.py | **C_01.account_performance** | **PORTED THIS LEG** (A4 L4) | see "the union-all caveat, resolved" below |
| G5 | build_gold_client_performance.py | **C_02.client_performance** | **PORTED** (A4 L2, M1 gates in code) | returns re-computed on summed bmv, never averaged |
| G6 | build_gold_canonical_nna.py | **C_03.nna** | **PORTED + LIVE** (first-live 07-16 09:52Z) | daily-atomic first-class; windowed = pure projection (grain law) |
| — | build_gold_holdings.py (header UNNUMBERED, self-labels "Gold-B", the old-B_00 equivalent) | **NO UNIT — COLLAPSES TO READS** | per Entry 5 R3 + the plan's B-group ruling | positions are READ (fact_rps + dim_position); the reconcile instinct survives ONLY as C_04's flags-never-patches guard |
| G7 | build_gold_client_tax_liability.py | C_05.tax_liability | Wave-4 | real 1099-DIV + ULT actuals |
| G8 | build_gold_realized_gains.py | C_06.realized_gains | Wave-4 | RLW is 0824-only today; 0833 vintage set confirmed at build |
| G9 | build_gold_firm_composition.py | C_07.composition | Wave-4 | dim_asset classes, no regex banks |
| G10 | build_gold_portal_aggregates.py | D-group publishers | Wave-5 | PARALLEL-NOT-SERVING until the parity streak |
| G11 | build_gold_advisor_attribution.py | C_08.advisor_attribution | Wave-4 (gates on D1 bridge proof) | bd-bridge flags stay |
| G12 | build_gold_advisor_fee_efficiency.py | C_09.advisor_fee_efficiency | Wave-4 | |
| G13 | build_gold_partner_analytics.py (header self-labels G13) | C_10.partner_analytics | Wave-4 | **fix the stale docstring-vs-code billable-gate drift AT PORT** (plan's named cell) |
| G14 | build_gold_advisor_split_reconciliation.py (header cites G13 as its INPUT; G14 per the plan) | C_11.split_reconciliation | Wave-4 | "money not accounted for" |
| n/a | — (no seed lineage) | **C_04.recon_guard** | **BUILT + LIVE** (Wave-2) | the NEW pure guard; replaces the legacy load-bearing reconciliation layer |

## THE PRICE-MATRIX RETIREMENTS (the d1ff2dfb0 L4 duty, verbatim anchor acabb3553)

**Andrew-direct 2026-07-16 ~14:1xZ (recorded @ acabb3553):** *"any kind of transaction-based pricing
framework is deprecated"*; the canonical-prices schema *"only mattered because we had to reprice based
on transactions"* and is *"unnecessary"* on daily RPS-snapshot holdings.

- **No seed G-script is price-matrix-purposed — MEASURED, denominator stated:** `comp-grep
  "canonical_prices" data/canonical/schwab/` = 0 matches in 0 files, 41 files scanned (2026-07-16).
  There is nothing in the seed to deprecate-not-port; the mapping above is retirement-free.
- The price-matrix class in the estate is **legacy-only**: `build_canonical_prices_v2.py`
  (data/black_diamond/scripts/gold/ — retires in place with the legacy chain) and the **M4
  canonical-prices promotion leg, RETIRED-WITH-REPLACEMENT** (M4-supersede committed for CTO
  @ a04bcbcd4; replacement = the L3 `pct_priced` STATEMENT-price-coverage spec lines, still queued).
- Transactions remain **FLOWS-ONLY** (the F-AMT chain — conformant); in-kind valuation is
  row-price-else-statement-closing-price (the statement's own prices, never a rebuilt matrix).

## THE G4/G5 UNION-ALL CAVEAT — RESOLVED AT PORT (the incrementality contract's named bite)

The plan flagged it verbatim: the seed's G4/G5 *"union ALL account_gains partitions for cumulative
returns — at port these re-shape to incremental-with-carried-state (running cumulatives keyed off
yesterday's row) ... NEVER an unbounded union that grows forever."* The C_01 port lands exactly that:
each partition = `data.parquet` (today's window rows; absent day ABSENT) + `state.parquet` (the
carried ledger — per-account geometric factor, O(accounts) forever); zero-BMV days link NEUTRAL and
are counted, dormancy carries without factor reset, and the runner REFUSES on a continuity gap
(latest prior partition must equal the gains window's own prev_date). C_02 needed no re-shape — its
caveat share lives in C_01's contract (stated in the landed L2 core).

## THE trn_nna DISPOSITION (CTO ruling 165108Z, folded at L4 — the /49-schwab-conv survivor)

The NNA Layer-B classification (the retiring bronze converter
`convert_schwab_trn_to_nna_silver.py`) is judgment-bearing — Rule-17 GOLD-TIER — and now derives
gold-side: `lib/schwab_trn_nna_gold.py` (classifier rules + txn-key hash MOVED verbatim,
byte-compatible) consumed by `lib/schwab_flows.load_schwab_flows_by_date(source='monolith')` from
monolith `schwab/08242234/silver/dim_transaction` (purpose=model_portfolios → 0824,
purpose-resolved, NO default). Parity: measured PASS two tiers within-master (partition row-for-row
on 3 real deliveries; full-seam window 07-01..07-15 to the cent, 0/10 dates mismatched). Named
divergences on full history, both honest: 58 legacy-only partitions are ALL pre-feed-floor
(<2024-07-08, the Entry-1 residue on Andrew's desk); 12 monolith-only partitions are deliveries the
legacy OneDrive chain MISSED (11 in 2026-01 + 2026-04-30) — the monolith path recovers them. Flip
default rides the bd-exporter-ec2-role IAM grant (measured implicitDeny on the exact monolith key;
positive control allowed, run in isolation).

---

*(This map supersedes the "next entries" expectations only where stated; per-script R1–R5 entries
still land WITH each Wave-4 port per the plan.)*
