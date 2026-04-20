# Master Briefing — Post-Presentation Edit Queue

**Author:** 0.4.0_DS_ClientPlatform
**Date:** 2026-04-15
**Addressed to:** 1.0.0_SA_CTO
**Status:** For CTO decomposition into task orders
**Context:** Andrew's presentation concluded successfully. Operational freeze on tactical/alt AUA-shifting work lifts. This document rolls up every deferred edit that came out of presentation-week investigations into one place, with links to every source architecture doc DS authored over the past week.

---

## Reading guide — three layers of work

1. **Tactical ship-first** — ~1 day each, coded or near-coded, unblock on presentation thaw. Items 1, 2.
2. **Point fixes** — localized gold-script edits with single rerun to validate. Items 3, 4. Each is subsumed by a larger structural plan; ship point fix OR strategic plan, not both.
3. **Structural convergence plans** — the week's architecture work. Each eliminates an entire class of divergence by routing every consumer through one canonical table. Items 5–11.

CTO reads this top-to-bottom and picks which items need task orders *this cycle* vs. staged for the next wave. Every item has an anchor into a formal PRD or source brief — no work below is undocumented.

---

## TL;DR — master queue

| # | Work | Type | Risk | Effort | Owner | Blocker |
|---|---|---|---|---|---|---|
| 1 | Scoped-exceptions blocklist (BNP/WFC/NEWMONT, ~$24.3M phantom) | Tactical | Low | 1 day | DS | Andrew thaw |
| 2 | 3-bond tactical formalization (WP-11) | Tactical | Low | 0.5 day | DS | Ships with or after #1 |
| 3 | RFS NNA window bug — sum-of-cumulative on `nna_{ytd,max}` | Point fix | Medium | 0.5 day + rerun | DS | None |
| 4 | GEO 3-way NNA schism (subsumed by ADVI_CANNNA) | Point fix OR skip | Medium | 1 day + rerun | DS | Choose: point fix now or wait for CANNNA |
| 5 | **BDPL_ASTDIM** — silver/bd_assets pipeline stand-up | Structural | Medium | 3–5 days | AE + DS | None (critical path for 6) |
| 6 | **BDPL_CNPRCS** — canonical prices + classification refactor (WP-3 … WP-11) | Structural | Large | 2–3 weeks | DS + AE | Needs #5 + WP-3 CUSIP backfill |
| 7 | **ADVI_ROLEAUA** — role-AUA canonical convergence (6 paths → 1 atomic table) | Structural | Medium | 4 days | DS | None |
| 8 | **ADVI_CANNNA** — NNA canonical convergence (10 paths → 1 atomic table; subsumes #4) | Structural | Medium | 4 days | DS | None; pairs with #7 |
| 9 | **ADVI_SLEEVE** — sub-custody sleeve reconstruction ($35–50M silver-gold recon) | Structural | Medium | 3–4 days | DS | Phase 0 picks quantity source |
| 10 | **ADVI_FNTEND** — 20 correctness gaps across AdvisorIntelligence | Structural | Medium | ~2 weeks | RD + DE + DS | Existing pipeline |
| 11 | Cost basis panel polish — time-drift on "2020 & Earlier" bucket | Trivial FE | Nil | 10 min | DE | None |

Anything marked Tactical or Point fix can ship on DS's current queue with no architecture coordination. Structural items need CTO PRD alignment; all already have PRDs or DS plan docs authored — just need task-order decomposition.

---

## 1. Scoped-exceptions blocklist (tactical 3-bond phantom fix)

**What breaks today:** `build_canonical_prices_v2` routes BNP Paribas (CUSIP 05613L3H2) → Yahoo → BNPQF equity ADR → $107 × 215,000 face-value = **$23M phantom on a $219K real position**. Same pattern on WFC 4.15% 2029 (~$860K phantom) and NEWMONT 2.8% 2029 (~$595K phantom). Total ~$24.3M phantom firm-wide in 49F alone.

**Fix:** Persistent CUSIP-keyed blocklist (`data/black_diamond/scripts/silver/scoped_price_exceptions.json`) hard-overrides canonical prices for listed CUSIPs with `force_source='bd_txn_price'`. Orthogonal to `ticker_overrides.json` — this is a BLOCK, not a reroute.

**State:** Task order shipped, code ready, **currently on hold** per Andrew's pre-presentation AUA freeze (2026-04-14T22:15Z). Thaw unlocks immediately.

**Reference:** `org/tier2_senior/0.4.0_DS_ClientPlatform/task_orders/3-bond-phantom-scoped-exceptions.md`

---

## 2. 3-bond tactical formalization (WP-11)

Absorbs #1 into the permanent `_SCOPED_PRICE_OVERRIDES` path (`bd_price_update.py` + `inject_scoped_overrides.py::_INCEPTION_DATES`) so the fix survives the canonical-prices refactor. Scoped to land independently of BDPL_CNPRCS in case that program slips.

Inception dates + unit prices:
```python
{"asset_name": "BNP PARIBAS SA",                    "ticker": "BOND_BNP_05613L3H2",  "price": 1.02}  # 2024-10-15
{"asset_name": "WELLS FARGO & CO 4.15% 01/24/2029", "ticker": "BOND_WFC_415_2029",   "price": 0.95}  # ~2023-Q1
{"asset_name": "NEWMONT CORP 2.8% 10/01/2029",      "ticker": "BOND_NEM_28_2029",    "price": 0.87}  # ~2023-Q2
```

**Reference:** WP-11 section in `org/tier2_senior/0.4.0_DS_ClientPlatform/briefs/2026-04-14_asset_dim_and_canonical_prices_refactor.md`

---

## 3. RFS NNA window bug — sum-of-cumulative

**What's wrong:** `platinum/accounts/{id}/summary.json` and `platinum/advisors/{id}/summary.json` emit `rfs.decomposition_{ytd,max}.nna` as area-under-curve of a cumulative series. Spot-check z0820265531: `rfs.nna_max = $563.6M` where true ITD NNA = $24.98M. Travis book: `decomposition_max.nna = $4.82B` on a ~$428M book (11×). QTD coincidentally correct (most rows pre-quarter are ~0).

**Root cause:** `D_04.client_portal_summary.py::_compute_window_decomposition` (L696) and `::_compute_window_flows` nna branch (L747) do `sum(r.nna for r in slice_rows)` on an internal `nna` column that is cumulative, not delta. `cum_inflows` / `cum_outflows` in the same functions already use correct `last − pre_cutoff` pattern.

**Fix:** Replace nna-sum with `_window_nna_delta()` — same `last − pre_cutoff` as flow deltas. Two callsites in `D_04.py`. No wire-contract change, no FE edit. Verify whether `market_growth` / `synthetic_correction` have the same bug before commit.

**Note:** This is the cleanest candidate for a point-fix task order. It does NOT overlap with ADVI_CANNNA (which canonicalizes *which* NNA value is emitted, not the window-slice math). Both can ship independently.

**References:**
- `org/tier2_senior/0.4.0_DS_ClientPlatform/briefs/2026-04-15_geo_three_way_schism_and_rfs_nna_window.md` (Bug 2 section)
- DE's original report (in MCP inbox to DE, 2026-04-15T13:14Z, with bit-for-bit root-cause match)

---

## 4. GEO 3-way NNA schism — point fix OR defer to ADVI_CANNNA

**What's wrong:** Three DS aggregates on `partner_analytics_quarterly.json` for the same (period, state) disagree structurally. TX current: donut.segments[tx].value = +$637K, sum(by_city) = -$3.78M, distribution.total = -$4.75M. Up to $5M gap. Repeats across every state × period × cohort (GEO/ADV/OFC).

**Root cause:** `D_01.partner_analytics.py::build_nna_geo_view` (L1242–1429) — donut is account-grain, by_city is relationship-grain (modal state), distribution is relationship-grain (all cities). Different grains / different filter stacks / different EXCLUDE_NAMES rules.

**Two paths:**

- **Point fix (1 day):** Localized D_01 refactor — compute one atomic `(period, account, state, city, relationship)` frame, roll up three ways by sum. Historical periods regenerate on next D_01 run. Detailed in `2026-04-15_geo_three_way_schism_and_rfs_nna_window.md` Bug 1.
- **Strategic (subsumed by ADVI_CANNNA — item #8):** Every NNA aggregation in gold (including this one, plus 9 others) reads from one canonical atomic table `gold/canonical/nna_atomic/{date}.parquet`. Structurally impossible for the three D_01 rollups to disagree. 4 days total for the full convergence, versus 1 day for the point fix.

**Recommendation:** Ship ADVI_CANNNA and skip the point fix — avoids double-work on D_01 and permanently closes the whole schism class (Travis three-way, architect three-way, GEO three-way, and the 7 others we haven't found yet).

---

## 5. BDPL_ASTDIM — silver/bd_assets pipeline

**Scope:** Stand up bronze + silver ingestion for BD's `AssetDimTXNs_OpalCapital_Daily` export. Produces `silver/assets/{date}.parquet` (trade-date-partitioned, one row per txn with CUSIP + AssetID + SuperClass + Action) and `silver/bd_assets.parquet` (derived point-in-time asset dim, one row per AssetID). Mirrors the existing `silver/fees/` and `silver/transactions/` runners exactly.

**Why it blocks everything:** BDPL_CNPRCS WP-4/5/6 all require `silver/bd_assets` online as their primary join source. ADVI_CANNNA optionally consumes it for attribution key stability. Nothing structural in the canonical-prices refactor ships until this lands.

**Status:** CTO PRD complete and registered (`BDPL_ASTDIM`). Task orders already staged on DS's queue for contributor scope:
- `BDPL_ASTDIM.W2.ds-super-class-recon.md` (staged)
- `BDPL_ASTDIM.W4.ds-build-bd-assets-dim.md` (staged)

AE owns the primary pipeline stand-up (W1 ingestion, W3 backfill). DS contributes the derived silver/bd_assets builder + reconciliation.

**Reference:** `docs/architecture/BD_ASSET_DIM_PIPELINE.md` (CTO PRD, 2026-04-14)

---

## 6. BDPL_CNPRCS — canonical prices + classification refactor

**The multi-week structural program the tactical fixes (#1, #2) are buying time for.** Eleven work packages from the 2026-04-14 DS brief, already decomposed into a CTO PRD.

**Core decisions:**
- Primary price input is CUSIP, not ticker. Fixed Income / TBC assets NEVER route to Yahoo.
- BD's Asset SuperClass is authoritative for classification. DDB classifier demoted to fallback only.
- TBC (To Be Classified) → alternatives per Andrew's 2026-04-14 directive.
- Canonical prices becomes an append-only daily ledger with quality tags: `yahoo_equity | bd_txn_price | carry_forward | par_value | custodial_override | cash_par`.
- Cash becomes a first-class asset (synthetic lots from BD-txn balance replay, fixed price 1.00, folded to fixed_income at read).

**Work packages:**

| WP | Owner | Scope |
|---|---|---|
| WP-3 | AE | Backfill CUSIP into silver/transactions |
| WP-4 | DS | Enrich `gold/holdings_lots` + `positions_cube` with CUSIP + AssetID |
| WP-5 | DS + AE | Canonical prices refactor — CUSIP-primary + cash as asset + weekend/holiday ledger |
| WP-6 | DS | Classification ledger — append-only, BD-primary |
| WP-7 | DS | Phantom valuation scan (nightly diagnostic) |
| WP-8 | DS | 49F alternatives regression test (acceptance gate) |
| WP-9 | DS | CUSIP-keyed FIFO replay + phantom reclassification (uses Schwab ULN for ground truth — see §11 for ULN details) |
| WP-10 | DS | Account-ID lifecycle + cash-as-position + nightly gold↔silver reconciliation harness |
| WP-11 | DS | Scoped price overrides for phantom bonds (absorbs #2) |

**Critical path:** BDPL_ASTDIM → WP-3 → WP-4 → (WP-5, WP-6, WP-9 parallel) → WP-8. WP-7 + WP-10 parallel anywhere post WP-4.

**Staged task orders on DS queue:**
- `BDPL_CNPRCS.WP-4 … WP-9` — all staged, awaiting GO
- See item 5 above for BDPL_ASTDIM prerequisite TOs

**References:**
- `docs/architecture/BD_CANONICAL_PRICES_CLASSIFICATION_REFACTOR.md` (CTO PRD, 2026-04-14)
- `org/tier2_senior/0.4.0_DS_ClientPlatform/briefs/2026-04-14_asset_dim_and_canonical_prices_refactor.md` (DS source brief — full 400 lines with phantom scan methodology, join-key analysis, reconciliation math)

---

## 7. ADVI_ROLEAUA — role-AUA canonical convergence

**Problem:** Six independent scripts compute per-advisor / per-role AUA six different ways. Three filter stacks (EXCLUDE_NAMES on/off, ghost-exclusion on/off, AP gate on/off), three cutoff conventions (account_team snapshot vs account_performance latest vs D_01 period_pairs). Result: ~0.5% drift in Travis's architect AUA across consumers users see side-by-side. This is the architect three-way schism generalized across every role-AUA consumer.

**Six current aggregation sites:**

| # | Script | Function | Consumer |
|---|---|---|---|
| 1 | D_00c | `_build_at_role_slice` + `tagged_aua_counts` | leaderboard.json |
| 2 | D_02 | `build_advisor_books` role_breakdown (L1269) | summary.json, book.json |
| 3 | D_02 | `build_advisor_timeseries` role_ts_lookup (L1619) | timeseries.json |
| 4 | D_01 | `build_adv_view` | partner_analytics views.adv |
| 5 | D_00b | `_build_advisor_view` + adv_drill | timeseries_chart.json, cumulative_chart.json |
| 6 | C_08 | scorecard builder | advisor_fee_efficiency.json |

**Fix:** One canonical table `gold/canonical/role_aua/{date}.parquet` — one row per `(date, advisor, role)` with `aua` (equal-split), `aua_tagged_total` (pre-dedup), `aua_fee_paying`, `aua_no_fee`, `nna_txn`, `daily_inflow`, `daily_outflow`, plus reconciliation metadata. Six invariants enforced via `comp-validate` post-run. Every consumer becomes a groupby on this table; reconciliation holds by construction.

**Phased execution:** 6 phases, ~4 DS days. Phase 0 schema + tests; Phase 1 shadow artifact write in D_02 (zero reader changes, rollback trivial); Phases 2–5 cut over each of the six consumers individually with per-phase acceptance gates.

**Reference:** `docs/architecture/ROLE_AUA_CANONICAL_CONVERGENCE_PLAN.md` (DS plan doc, 2026-04-14)

---

## 8. ADVI_CANNNA — NNA canonical convergence

**Problem:** Same disease as ROLEAUA but for NNA / inflows / outflows. **Ten scripts, ~25 aggregation sites, three semantically distinct "NNA" concepts floating:**

- `nna_txn` — transaction-based, emitted by C_01 at (date, account_id) — the only physically-grounded number.
- `nna = cum_inflows − cum_outflows` — derived from C_01 running totals (D_00 / D_00b / D_00c variant).
- `period_nna = end.nna − start.nna` — period-differenced on relationship-grain cum columns (D_01 specific).

Three concepts × inconsistent dedup rules (account vs relationship vs state-city) × inconsistent EXCLUDE_NAMES filters = the Travis three-way on AdvisorPublicProfile AND the TX three-way on Snapshot-GEO-NNA AND 8 other latent schisms we haven't yet enumerated at consumer surfaces.

**Fix:** One canonical table `gold/canonical/nna_atomic/{date}.parquet` — one row per `(date, account_id)` with daily + cumulative flows, plus SCD PIT attribution keys (relationship / architect / implementor / consultant / local_ops / additional_advisor / office / state / country / city / tax_status / billable / is_excluded / is_ghost).

**Invariants** enforced via `comp-validate nna_atomic`:
1. `nna_txn == daily_inflow − daily_outflow` within $0.01 per row
2. `cum_nna == cum_inflows − cum_outflows` within $0.01 per row
3. Timeline consistency: `cum_flows[t] == cum_flows[t-1] + daily_flows[t]` per account
4. Cross-cohort additivity: `sum_{account} daily_inflow` at a date equals firm daily_inflow
5. Fee-partition preservation: `billable + non_billable == total` per (date, group)

**Consumer contract:** 12 current aggregation sites become simple groupbys on this atomic table (firm timeseries, advisor daily, geo drill, leaderboard windows, partner analytics geo/adv/ofc, client summaries, role-scoped NNA, etc.). By construction they reconcile to $0.01.

**Pairs with ROLEAUA:** Both tables emitted together in one D_02 pre-pass. Phase 1 lands the canonical writes in a single commit (both shadow artifacts, zero readers, trivial rollback).

**Phased execution:** 6 phases, ~4 DS days. Phase 1 canonical write in C_01 (shadow). Phases 2–5 cut over each consumer (D_02, D_00c, D_01, D_00b/D_00) one at a time with per-phase acceptance gates.

**Supersedes:**
- My 2026-04-15 point fix for GEO 3-way schism (item #4) — CANNNA eliminates the schism structurally across all consumers, not just D_01.
- The companion Travis three-way NNA finding.

**Reference:** `docs/architecture/ADVI_CANNNA_PLAN.md` (DS plan doc, 2026-04-15)

---

## 9. ADVI_SLEEVE — sub-custody sleeve reconstruction

**Problem:** BD sub-custody sleeve accounts (PCRA Trust, SWTC TTEE, and similar retirement vehicles) land in `silver/allocations` + `silver/unrealized` but never fire Transfer In transactions, so gold's FIFO replay never opens lots. Diagnostic case: Jones z0817905851 shows silver $2,396,510 vs gold $82,423 — $2.31M of real positions invisible at gold grain.

**Firm-wide impact:** ~$35–50M of actionable silver-gold under-reconstruction concentrated in the 403 mapped-no-RPS cohort plus ~44 gold-exceeds-silver accounts where the sleeve feed is under-reporting.

**Fix — sleeve-scoped ULN override of FIFO:**

For accounts classified as sleeves (via conservative multi-signal detection on account_type + account_registration_type + account_number prefix + portfolio_group), seed opening lots from `silver/unrealized` (ULN = BD's Unrealized Lot Network feed), then apply incremental silver/transactions on top. Not a replacement of FIFO — an opening-state override, scoped by account classification. Identical pattern to B_01's existing RPS synthetic lot injection, extended to a second feed for a different account cohort.

**Precedence stack** (for any `(account_id, asset_id)`):
1. silver/rps synthetic lot (Schwab-authoritative, covers mapped Schwab cohort)
2. silver/unrealized sleeve lot (BD-authoritative for sleeves without RPS)
3. FIFO-reconstructed lot (standard accounts with full transaction history)

**Critical open question:** Quantity source for ULN-seeded lots. silver/unrealized carries `(open_date, unit_cost, asset_id, cusip)` but **not quantity**. Three candidates:
1. Add Units column to BD's unrealized export (preferred — BD's UGL source has it; silver ingestion drops it)
2. Pull quantity from an adjacent BD feed we don't ingest (ULT = Taxable Unrealized, or positions API)
3. Apportion `account_market_value` across ULN lots by cost-basis weight (fallback; breaks on rebalanced sleeves)

Phase 0 discovery picks one.

**Phased execution:** 4 phases, ~3–4 DS days (assuming quantity path 1). Phase 0 discovery + cohort sizing; Phase 1 shadow emit (sleeve accounts only, `holdings_lots_shadow/`); Phase 2 promote + verify; Phase 3 monitor + extend detection.

**Reference:** `docs/architecture/ADVI_SLEEVE_PLAN.md` (DS plan doc, 2026-04-15)

---

## 10. ADVI_FNTEND — full-surface frontend correctness

Not DS-owned, but on the same wave. 20 identified correctness / parity gaps across AdvisorPublicProfile + AdvisorBookView + Distribution/Segment Analytics OFC surfaces. Split across 8 bundles:

- **Bundle 0** — FE-trivial sweep (pill wrapping, readonly-asset-class propagation at L3/L4, Top Holdings palette canonicalization, OFC L0 styling parity, advisor pseudonymization)
- **Bundles 1–7** — FE + DS data-contract changes (Fees-toggle scoping, Relationship Flows Summary windowing, Fee Summary team attribution, Top Gain Positions at L2/L3, Account L4 timeseries, OFC snapshot parity, Q4-2025 continuous-vs-snapshot AUA divergence investigation, Fee Efficiency role-filter)
- **AE:** single PROD D_04 rerun after ADVI_PROFAU.006 lands

**DS-relevant bundles** (all 8 FNTEND task orders staged on DS queue):
- `ADVI_FNTEND.B1.ds-fee-toggle-scoping.md`
- `ADVI_FNTEND.B2.ds-rfs-window-trio.md`
- `ADVI_FNTEND.B3.ds-fee-summary-team-attribution.md`
- `ADVI_FNTEND.B4.ds-top-gain-positions-l2.md`
- `ADVI_FNTEND.B5.ds-account-l4-timeseries.md`
- `ADVI_FNTEND.B6.ds-ofc-snapshot-parity.md`
- `ADVI_FNTEND.B7.ds-q4-aua-divergence-investigation.md`
- `ADVI_FNTEND.B8.ds-fee-efficiency-role-breakdown.md`

**Reference:** `docs/architecture/ADVI_FRONTEND_CORRECTNESS.md` (CTO PRD, 2026-04-14). Source briefing: `org/tier2_senior/0.4.2_RD_AdvisorIntelligence/briefs/2026-04-14_advi_frontend_status.md`.

**Companion:** `docs/architecture/ADVI_OFFICE_ADDENDUM.md` — OFC snapshot parity gaps (compiler-evidence-backed), 2026-04-14.

---

## 11. Cost basis panel polish — time-drift on "2020 & Earlier" bucket

**Not a data issue — forward-compat FE nit.** DE commit `ae7b377` collapses rows with `purchase_year < 2020` into one "2020 & Earlier" bucket with "≥ {current − 2020} yrs · Long" badge. Math verified correct on Travis (totals reconcile to `capital_gains_ttm = $60,311,016.46` to the penny).

**Risk:** hardcoded 2020 threshold silently stales on Jan 1 2027. Fix: parameterize `RECENT_YEARS_TO_SHOW = N`, derive both label and badge from `currentYear − N`. 10-minute FE edit.

**Secondary:** Short/Long badge on `currentYear` and `currentYear − 1` rows overstates short-term classification (those rows are mixed-term in reality). DS already emits `short_term_gain` / `long_term_gain` as separate scalars — badge could be dropped on recent years.

**Reference:** Conversation 2026-04-15 with Andrew. No formal brief.

---

## References — complete architecture doc index (DS-authored and CTO-authored, last ~10 days)

### Planning / architecture docs in `docs/architecture/`

| Doc | Date | Author | Project code |
|---|---|---|---|
| `ADVI_SLEEVE_PLAN.md` | 2026-04-15 | DS | ADVI_SLEEVE |
| `ADVI_CANNNA_PLAN.md` | 2026-04-15 | DS | ADVI_CANNNA |
| `ROLE_AUA_CANONICAL_CONVERGENCE_PLAN.md` | 2026-04-14 | DS | ADVI_ROLEAUA |
| `BD_CANONICAL_PRICES_CLASSIFICATION_REFACTOR.md` | 2026-04-14 | CTO | BDPL_CNPRCS |
| `BD_ASSET_DIM_PIPELINE.md` | 2026-04-14 | CTO | BDPL_ASTDIM |
| `ADVI_FRONTEND_CORRECTNESS.md` | 2026-04-14 | CTO | ADVI_FNTEND |
| `ADVI_OFFICE_ADDENDUM.md` | 2026-04-14 | CTO | ADVI_OFFICE |
| `ADVI_OFFICE_PRD.md` | 2026-04-13 | CTO | ADVI_OFFICE (superseded by addendum) |
| `ADVI_REBORN_LEADERBOARD_FEES_ROLES_FIX.md` | 2026-04-13 | CTO | ADVI_REBORN |
| `ADVI_HEADER_SPLIT_PRIMITIVES.md` | 2026-04-13 | CTO | ADVI_FNTEND (feeds into) |
| `DISTRIBUTION_TAB_OTHER_DEDUPE.md` | 2026-04-13 | CTO | ADVI_FNTEND (feeds into) |
| `ADVI_PROFIL_PRD.md` | 2026-04-10 | CTO | ADVI_PROFIL |

### DS source briefs in `org/tier2_senior/0.4.0_DS_ClientPlatform/briefs/`

| Brief | Date | Covers |
|---|---|---|
| `2026-04-15_post_presentation_master_summary.md` | 2026-04-15 | This document |
| `2026-04-15_geo_three_way_schism_and_rfs_nna_window.md` | 2026-04-15 | GEO schism + RFS NNA window bug (point fixes for items #3 and #4) |
| `2026-04-14_asset_dim_and_canonical_prices_refactor.md` | 2026-04-14 | BDPL_CNPRCS source brief (400 lines — full WP-1…WP-11) |
| `2026-04-06_canonical_stack_session_brief.md` | 2026-04-06 | Canonical holdings stack origin work |
| `2026-04-06_account_mapping_gap_brief.md` | 2026-04-06 | Schwab account mapping gap |

### Session logs relevant to the master queue

- `org/tier2_senior/0.4.0_DS_ClientPlatform/logs/2026-04-15/` — today's sessions (RFS spot-check, D_02 fix, post-presentation work)
- `org/tier2_senior/0.4.0_DS_ClientPlatform/logs/2026-04-14/full_session_log.md` — D_00b OFC fix + D_02 RFS decomposition fix `aa261b5b`
- `org/tier2_senior/0.4.0_DS_ClientPlatform/logs/2026-04-14/49f_alternatives_investigation_and_bdpl_cnprcs_dryrun_addendum.md`
- `org/tier2_senior/0.4.0_DS_ClientPlatform/logs/2026-04-14/evening_session_alternatives_investigation.md` — contains Schwab ULN file-ecosystem + BNP phantom trace referenced by WP-9 and ADVI_SLEEVE

### Task orders already staged on DS queue covered by this master

**Tactical / Point fix:**
- `3-bond-phantom-scoped-exceptions.md` (pending, held)

**BDPL_ASTDIM:**
- `BDPL_ASTDIM.W2.ds-super-class-recon.md` (staged)
- `BDPL_ASTDIM.W4.ds-build-bd-assets-dim.md` (staged)

**BDPL_CNPRCS:**
- `BDPL_CNPRCS.WP-4.ds-holdings-lots-cusip-enrichment.md` (staged)
- `BDPL_CNPRCS.WP-5.ds-canonical-prices-refactor.md` (staged)
- `BDPL_CNPRCS.WP-6.ds-classification-ledger.md` (staged)
- `BDPL_CNPRCS.WP-7.ds-phantom-diagnostic-nightly.md` (staged)
- `BDPL_CNPRCS.WP-8.ds-49f-alternatives-regression.md` (staged)
- `BDPL_CNPRCS.WP-9.ds-cusip-keyed-fifo-replay.md` (staged)

**ADVI_FNTEND (8 bundles):**
- `ADVI_FNTEND.B1 … B8.*.md` (all pending)

**Not yet written — CTO to author this wave:**
- `BDPL_RFSNNA.01.ds-d04-window-nna-delta-fix.md` (item #3)
- `ADVI_CANNNA.P0 … P5.*.md` (item #8, 6 phases)
- `ADVI_ROLEAUA.P0 … P5.*.md` (item #7, 6 phases)
- `ADVI_SLEEVE.P0 … P3.*.md` (item #9, 4 phases)
- `BDPL_CNPRCS.WP-10.ds-account-id-lifecycle.md` (not yet staged)
- `BDPL_CNPRCS.WP-11.ds-scoped-price-overrides.md` (formalize item #2)
- `FNTEND.cost-basis-panel-year-bucket-parameterize.md` (item #11, DE-only, trivial)
