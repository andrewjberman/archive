# DATA_ANALYTICS — SERVER-SIDE Group-D → Group-A LINEAGE MANIFEST (49F / BD)

**TO:** DATA_ANALYTICS (server-side companion to FE1) | **Author:** 0.4.0_DE_ClientPlatform | **Date:** 2026-06-25
**archetype:** TRACE | **Partner:** 49 Financial (`49financial`, BD pipeline, `opal-data-bd`) — **v0.1 (49F first; COT then INF to follow, successively)**
**Pairs with:** `DATA_ANALYTICS.FE1_advi_panel_platinum_groupd_manifest.md` (panel→D). Together = the complete `panel → platinum → D → C → B → A → Schwab-raw` vertical.
**Spine tool:** `comp-pipescript io` (per-script READS `<-` edge map) + `pipescript advi-bd`. Rail-grounded, not raw grep.

> **Direction:** FE1 threads frontend-DOWN and STOPS at the D-tier publisher (the served-artifact waist). This doc picks up
> THERE and threads the gold internal lineage UPSTREAM: `D-publisher → C-tier (canonical analytics) → B-tier (holdings/lots/gains)
> → A-tier (dimensions) → Schwab-raw silver`. Layered: §1–2 = the script-to-script SPINE; §3 = FIELD-level detail on the three
> headline numbers (`total_aua` / `nna` / `tax_liability`); §4 = the rebuild-relevance tags (the value-parity census substrate
> CTO's G2 rider needs). No silent Unknown — every edge is a grounded `comp-pipescript io` read or an explicit `(external/silver)` leaf.

---

## 0. The 49F gold tiers (28 scripts; the contract waist is D, the leaves are A→silver)

| Tier | Role | Scripts |
|---|---|---|
| **D** (publishers) | emit the served `platinum/*` + `gold/artifacts/*` | D_00, D_00b, D_00c, D_00f, D_01, D_02, D_03, **D_04 (sole platinum publisher)** |
| **C** (canonical analytics) | performance / NNA / tax / mix / attribution / fee | C_00, C_01(+b/c), C_02, C_03, C_05, C_06, C_07, C_08 |
| **B** (holdings/lots/gains) | positions→holdings→lots→gains | B_00, **B_01 (FIFO — rebuild-EXCISE)**, B_02 (custodian lots), B_03 |
| **A** (dimensions) | accounts / advisor / fee / positions-cube / client | A_00, A_01, A_02, A_03, A_04 |
| **silver/raw** | the leaves (bronze→silver) | `schwab/silver/{rld,uln,ult}`, `silver/{allocations,prices/canonical_prices(S_00),transactions,realized,unrealized}` |

---

## 1. Per-D-publisher upstream closure (the script-spine, transitive to A→silver)

Each row = a served D-publisher → its FULL transitive upstream (grounded `comp-pipescript io` edges). `→` reads downward.

| D-publisher | C-tier reached | B-tier reached | A-tier reached | silver/raw leaves |
|---|---|---|---|---|
| **D_04** client_portal_summary | C_01, C_02, C_03, C_06, C_07, C_08 | B_00, B_02, **B_01** | A_00, A_03, A_04 | (via B/C) + `leaderboard.prior_week` |
| **D_00** portal_aggregates | C_02, C_03, C_05, C_07 | (via C) B_03→B_00/B_02 | A_00, A_02, A_04 | nna_aua views, snapshots (silver) |
| **D_00b** portal_timeseries | C_01, C_02, C_03, C_07 | **B_01** (holdings_lots) | A_00, A_04 | role_aua, dim_advisor_office |
| **D_00c** portal_leaderboard | C_01, C_03, C_07, C_08 | (via C) | A_01, A_02, A_04 | advisor_fee_detail (silver) |
| **D_00f** advisor_nna_canonical | C_07 | (via C_01 chain) | A_00 | — |
| **D_01** partner_analytics | C_01, C_02, C_03, C_07 | (via C) | A_00, A_04 | nna_aua views, role_aua |
| **D_02** advisor_client_detail | C_01, C_03, C_05, C_07, C_08 | **B_01** (holdings_lots) | A_00→A_01, A_02, A_04 | entities (silver) |
| **D_03** composition_artifacts | C_02, C_03, C_06, C_07 | **B_01** (holdings_lots) | A_04 | firm_composition (silver) |

**Read:** every served 49F artifact resolves through the C-tier analytics into the B-tier holdings/lots/gains and the A-tier dimensions, bottoming out at Schwab silver. `D_04` is the widest (27 inputs); `D_00f` the narrowest (advisor NNA only).

## 2. Tier reference — each script's direct upstream (grounded `<-` edges)

**A-tier (dimensions — the silver/bronze boundary):**
| Script | Produces | Direct upstream |
|---|---|---|
| A_00 accounts_dimension | `gold/dimensions/accounts_dimension_latest.parquet` | silver (BD accounts dim) |
| A_01 advisor_assignments | `gold/dimensions/advisor_assignments_history.parquet` | A_00 + silver (assignments) |
| A_02 fee_rate_history | `gold/dimensions/fee_rate_history.parquet` | **silver (BD Fees feed — N1 non-custodian)** |
| A_03 positions_cube | `gold/timeseries/positions_cube/` | silver/allocations + `silver/prices/canonical_prices`(S_00) + silver/{realized,unrealized} |
| A_04 client_dimension | `gold/dimensions/client_dimension.parquet` | **A_00 (household roll-up — N2 point)** |

**B-tier (holdings/lots/gains):**
| Script | Produces | Direct upstream |
|---|---|---|
| B_00 canonical_holdings | `gold/canonical/holdings/` | A_00, A_03, S_00, silver/{realized,unrealized}, **B_02** |
| **B_01 holdings_lots (FIFO)** | `gold/timeseries/holdings_lots/` | A_00, A_03, S_00, silver/unrealized, bd_assets_dim, ticker_resolution |
| B_02 canonical_lots | `gold/canonical/lots_{realized,unrealized}/` | A_00, B_00, S_00, **`schwab/silver/{rld,uln,ult}` (custodian-DIRECT)**, silver/realized |
| B_03 account_gains | `gold/canonical/account_gains/` | B_00, B_02 (holdings+lots), **silver/transactions (TRN)** |

**C-tier (canonical analytics):**
| Script | Produces | Direct upstream |
|---|---|---|
| C_00 canonical_performance | `gold/canonical/performance/` | A_00, B_03 |
| C_01 canonical_nna | `gold/canonical/nna/` | A_00, B_03, C_02, silver/nna |
| C_02 client_performance | `gold/timeseries/client_performance.parquet` | A_00, B_03, B_00/B_02, C_00, A_03 |
| C_03 account_performance | `gold/timeseries/account_performance.parquet` | A_00, B_03, C_02 |
| C_05 client_tax_liability | `gold/views/client_tax_liability.parquet` | A_00, **B_02 (lots_unrealized)** + **B_01 (holdings_lots FIFO)** |
| C_06 client_mix_timeseries | `gold/views/mix_daily_summary.json` | A_00, C_02, C_03, C_07, B_00/B_02 |
| C_07 advisor_attribution | `gold/views/account_team.parquet`, `rel_architect_lookup` | A_00, C_03 |
| C_08 advisor_fee_efficiency | `gold/artifacts/advisor_fee_efficiency.json` | C_07, A_01, **A_02 (fee_rate)**, C_01, silver/advisor_fee_detail |

## 3. FIELD-level lineage — the three headline numbers

### 3.1 `total_aua` (header_metrics / partner_analytics / clients_tab headline)
```
platinum total_aua  (D_04::build_firm_dashboard / D_00 header_metrics)
  <- C_02/C_03  client/account_performance . ending_mv (AUA per account/client, scoped by A_00 tax/relationship)
    <- B_00/B_02 canonical_holdings . market_value
      <- A_03 positions_cube . (qty x price)
        <- silver/allocations (positions) + silver/prices/canonical_prices [S_00]
```
A-scope: `A_00 accounts_dimension` (which accounts count) + `A_04 client_dimension` (household roll-up for client-level AUA).

### 3.2 `nna` (canonical NNA — advisor_nna_canonical / timeseries / leaderboard)
```
platinum nna  (D_00f advisor_nna_canonical / D_00b timeseries)
  <- C_01 canonical_nna . nna  (inflow/outflow classification + residual cross-check)
    <- B_03 account_gains  (dAUA = Growth + NNA decomposition)
      <- silver/transactions [TRN]  (the flow events)  +  B_00/B_02 holdings deltas
```
A-scope: `A_00` (account set) + `C_07 advisor_attribution` (whose NNA — advisor/team rollup).

### 3.3 `tax_liability` (client_tax_liability — TaxCostBasisPanel / L3 client drill)
```
platinum tax  (D_00 / D_02 <- C_05 client_tax_liability)
  <- C_05 . {realized, unrealized, ST/LT cost_basis, gain_loss}
    <- B_02 canonical_lots . lots_unrealized  [<- schwab/silver/uln + ult]   (custodian-DIRECT)
    <- B_02 canonical_lots . lots_realized     [<- schwab/silver/rld]         (custodian-DIRECT)
    <- B_01 holdings_lots (FIFO)  *** rebuild-EXCISE dependency (see §4) ***
```
A-scope: `A_00` (tax_status per account).

## 4. REBUILD-RELEVANCE TAGS — the value-parity census substrate (CTO G2 rider)

CTO's G2 ruling: excising B_01-FIFO + B_00-reconcile requires a VALUE-PARITY census — every served field whose lineage passes through a FIFO-derived or reconcile-adjusted node must reproduce its value Schwab-native. This lineage flags the exact targets:

| Tag | Served lineage carrying it | Census target |
|---|---|---|
| **B_01-FIFO** (excise) | `tax_liability` (via C_05); holdings-lots reads in **D_00b, D_02, D_03** (HOLDINGS_LOTS_PREFIX) | every field these emit that derives from `holdings_lots` must re-derive from B_02 custodian lots (ULN/RLD) at PARITY before B_01 is cut |
| **B_00-reconcile** (excise) | all AUA/holdings-derived fields (`total_aua`, mix, composition) via C_02/C_06 ← B_00 | B_00 currently reconciles BD↔Schwab + reads B_02; rebuild collapses to "read RPS/B_02 direct" — parity-check the holdings `market_value` |
| **N1 fee** (retain) | fee fields via C_08 ← **A_02** ← silver BD-fees | A_02/C_08 unchanged (CTO: RETAIN bd-fees feed); not a parity risk, a retained dependency |
| **N2 household** (Andrew-deferred) | `client_count` + client-level AUA via **A_04 ← A_00** household roll-up | the grouping logic in A_04 is the N2 sovereign item; partial-lock — do not re-derive until Andrew rules |
| **custodian-DIRECT (already present)** | B_02 ← `schwab/silver/{rld,uln,ult}` | the Schwab-direct lot path EXISTS today — the rebuild promotes it to primary + retires B_01; lowers parity risk for lots |

## 5. Completeness attestation (no silent Unknown)
All 8 D-publishers threaded to their transitive A-tier + silver leaves (§1), every script's direct upstream grounded via `comp-pipescript io` `<-` edges (§2), field-lineage on the 3 headline numbers (§3), rebuild-excise/retain/deferred dependencies tagged (§4). `(external/silver)` leaves are explicit, not gaps. Rail-grounded (comp-pipescript io + pipescript advi-bd), not raw grep.

## NEXT (successive, per Andrew)
- **v0.2 — Cottonwood** (BD-native, `data/cot/scripts/gold`): same D→A backtrack; expect the same `D_04`-publisher shape but the reduced essential set (D_00/D_00b/D_01/D_04) + the COT custodian-direct-snapshot methodology (ADVI_COTETL).
- **v1.0 — Inflection** (Orion, `data/inf/scripts/gold`): the ~20 `INF_D_0x` fan-out backtracked through the INF C/B/A tiers to Orion-raw; distinct shape (not the Schwab-raw target).
