# ADVI Full-Surface Frontend Status Investigation

**Author:** 0.4.2_RD_AdvisorIntelligence
**Date:** 2026-04-14
**Addressed to:** 1.0.0_SA_CTO
**Status:** Proposal — awaiting CTO decomposition into task orders

---

## Items by Surface

### Distribution / Segment Analytics

| # | Item | Status | Root cause |
|---|---|---|---|
| D1 | Q4 2025 Continuous AUA ≠ Snapshot / Header | Data — unknown | `cumulative_chart.json` (D_01 timeseries) vs `partner_analytics.json` (snapshot + header). Two independent AUA aggregations. Needs DS reconciliation — mapping issue or asof/point-picking glitch. |
| D2 | Snapshot-OFC-AUA L1 drill: no time machine lookback | FE + DS | `OfcAdvisorListPanel` (`DistributionTab:3071`) has no per-period strip. `NnaQuarterlyStrip` (`:3165`) is NNA-only. Need DS to expose per-office-per-period AUA; FE wires a time-machine row mirroring L0. |
| D3 | Snapshot-OFC-NNA: no bell curve (L0 + L1) | FE + DS likely | `nna_ofc` exists on continuous but snapshot bell-curve for OFC-NNA not populating. Verify DS emits nna distribution bins under `views.ofc` (and L1 per-advisor bins); FE to render. |
| D4 | "No advisor data for Austin" on L1 drill | DS | `officeSegment.advisors[]` empty (`DistributionTab:3086`). Needs DS to populate `advisors[]` on every OFC donut segment. |
| D5 | Continuous-ADV drill: pseudonymize sub-category labels (added 2026-04-14 per Andrew) | FE trivial | `DistributionTab.tsx` `ContinuousChartView` when `cohort === 'adv' && isDrilled` — `getCategoryDisplayName` falls through to `formatArchitectLabel` which renders real client names / account numbers. Change to `Client N` ordinal labels (Other preserved). Helper `pseudonymizeChildLabel` swapped at `:1295, :1308, :1445, :2022, :2180, :2249`. Forced — independent of `canSeeCleartext()`. |

### Advisors / AdvisorPublicProfile (public)

| # | Item | Status | Root cause |
|---|---|---|---|
| A1 | Clients / New Clients do not respond to Fees toggle in Summary | DS + FE | Summary reads `entry.client_count` / `entry.new_clients` raw; only AUA/flows are fee-bucketed via `entry.fee_breakdown`. DS to add `client_count` / `new_clients` / `account_count` under each of `fee_breakdown.{fee_paying,no_fee}`; FE swaps on `feeView`. |
| A2 | Role Composition donut does not respond to Fees toggle | DS + FE | `RoleDonut` reads `entry.role_breakdown[role].{aua,nna,client/account_count}`. `types.ts` already anticipates a fee-partition sub-bucket on `role_breakdown` (`:1527`). DS to populate `role_breakdown[role].{fee_paying,no_fee}`; FE picks the bucket matching `feeView`. |
| A3 | Lifetime Activity must match Summary canonical numbers | DS + FE | Currently uses `*_canonical` period-diffs — explicit note "Fee filter not applied to lifetime activity chart" (`:1105`). Reconcile: DS emits fee-bucketed lifetime timeseries OR FE scales chart by the same fee bucket Summary uses. Exact reconciliation logic is for CTO to specify. |

### Advisor "Private" / Book view

| # | Item | Status | Root cause |
|---|---|---|---|
| B1 | Capital Gains TTM + Cost Basis by Year not populating | AE (open) | Fields shipped in DS D_04 tax_exposure, PROD D_04 artifact pre-dates DS commit. Needs PROD gold re-run. Already flagged 2026-04-14. |
| B2 | Clients panel "No Fee" bubble wraps two lines | FE trivial | `ClientsTable.tsx:77` — add `whitespace-nowrap` to the pill span + widen cell. |
| B3 | Add NNA column with QTD/YTD/Max toggle to Clients table | DS + FE | `AdvisorClient` needs `nna_{qtd,ytd,max}` (plus inflows/outflows for consistency with flow panels). FE adds column + shared window toggle. |
| B4 | Client L1 drill — Asset Mix must be non-clickable | FE trivial | `AdvisorBookClientDetail` passes no `readonlyAssetClass` to `CanonicalBookView` (L3 call). L2 sets it; L3 + L4 do not. Pass `readonlyAssetClass` at both call sites. |
| B5 | Fee Summary: clarify Client Fee vs Advisor share + team split; rename "Wtd Avg Fee" | DS + FE | `FeeSummaryPanel:35` labels aggregate as "Wtd Avg Fee" (misreads as this advisor's fee). Needs DS per-account: `client_total_fee`, and a `team_attribution[]` array of `{advisor_id, display_name, fee_share_bps, fee_share_pct}` with the profile advisor first. FE renders rollup + split. |
| B6 | Cost Basis & Top Gain Positions connected at L3 | DS + FE | `AdvisorBookView.tsx:282` passes `topGainPositions: []`. Needs DS to surface `top_gain_positions` at L2 and L3 (L3 has the type already — `clientDetail.tax.top_gain_positions`), then FE passes through. |
| B7 | Replace "AUA Change Decomposition (Trailing 90d)" with "Relationship Flows Summary" (QTD/YTD/Max toggle, default QTD) | DS + FE | `AuaDecompositionPanel` (`AdvisorBookClientDetail:42`) hardcoded 90d from `decomposition_90d`. Needs DS to ship `decomposition_{qtd,ytd,max}` + matching nna/inflows/outflows per window; FE renames, re-skins, adds toggle. |
| B8 | Accounts table Inflows/Outflows/NNA shared with RFS toggle | DS + FE | `AccountsTable` currently renders `cum_inflows` / `cum_outflows` / `nna` (lifetime-ish). Needs per-account `{inflows,outflows,nna}_{qtd,ytd,max}`; FE binds columns to the RFS window. |
| B9 | Account L1 drill — time series history (M/Q/Y snapshot lookbacks) | DS + FE | `PlatinumAccountSummary` lacks a timeseries. DS adds account-level inception-to-date timeseries (AUA + NNA). FE adds chart + M/Q/Y interval toggle mirroring Lifetime Activity pattern. |
| B10 | Account L1 drill — Asset Mix not clickable | FE trivial | Same as B4 at L4 call site (`AdvisorBookAccountDetail` → `CanonicalBookView`). |

### Global

| # | Item | Status | Root cause |
|---|---|---|---|
| G1 | Top Holdings bars colored by asset class (equity blue / FI green / alts orange), matching Assets Overview canonical | FE verify | `ConsolidatedOverviewPanel` already does `colorFor(item.asset_class)` via `mixPieColor` (`chartColors MIX_PIE`). Need to (a) confirm `MIX_PIE` matches the Assets Overview canonical palette for equity/FI/alts, (b) audit every other "Top Holdings" surface to use the same helper (no hardcoded PALETTE colors). |

---

## Suggested Sequencing

1. Trivial FE sweep (B2, B4, B10, G1) — single small RD TO, no dependency.
2. DS TOs for bundles 1, 2, 6 in parallel (independent data surfaces); DS TO for bundle 7 (investigation) in parallel.
3. Bundle 3, 4, 5 DS TOs can follow bundle 2 to reuse the window/fee vocabulary.
4. FE TOs per bundle behind each DS ship.
