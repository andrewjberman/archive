# Inflection FE State of Affairs

**Author:** 0.4.0_DE_ClientPlatform
**Date:** 2026-05-05
**Matrix basis:** `docs/architecture/ADVI_INFLEC_AUDIT.md` v10 (post-chain-full)
**Portal commit baseline:** `63edaad6` (INFLFE.006 Line 210) + `72a6c1f4` (INFLFE.002) + `6fd66973` + `d52d04a0` (INFLFE.003) + `e68f54e7` (AUDIT-007 dead-code)
**Purpose:** Sprint deliverable for COO — comprehensive FE map of Inflection portal surface: pages, wirings, gaps, conditional gates, pending follow-ons.

---

## § 1 — Pages Enumerated

### Entry point routing

| File | Component | Role |
|------|-----------|------|
| `AdvisorIntelligence/index.tsx` | `AdvisorIntelligence` | Router — internal users get dropdown selector; routes `firmId=inflection` to `InflectionAdvisorIntelligence` |
| `_partners/inflection/index.tsx` | `InflectionAdvisorIntelligence` | Page shell for Inflection — tab nav, firm-level data fetches, theme |
| `_shared/hooks/useTenantLayout.ts` | `useTenantLayout(firmId)` | Pure config lookup — `firmId=inflection` → `INFLECTION_LAYOUT`; all others → `DEFAULT_LAYOUT` |

### Tabs and panels in scope for Inflection

| Tab | Enabled | Component | Notes |
|-----|---------|-----------|-------|
| PartnerAnalytics | Always visible (not a tab — inline above nav) | `_shared/components/PartnerAnalytics.tsx` | Geo-only per `allowedViewModes: ['geo']` |
| Distribution | YES | `_shared/tabs/DistributionTab.tsx` | Geo cohort only; ADV and OFC cohorts disabled |
| Books | YES | `_shared/tabs/ClientsTab.tsx` (exported as `BooksTab`) | N1→L2→L3→L4 drill hierarchy; revenueOpsSlot = `InflectionInsightsPanel` |
| Advisors | NO (`layout.ts:38`) | `_shared/tabs/AdvisorsTab.tsx` | Tab filtered from nav entirely |
| Profile | NO (`layout.ts:45`) | `_shared/AdvisorPublicProfile.tsx` | `advisorPublicProfile.enabled: false` — tab dead for Inflection |

### Components active inside BooksTab

| Component | Drill level | File |
|-----------|-------------|------|
| `InflectionInsightsPanel` | N1 revenueOpsSlot | `_partners/inflection/InflectionInsightsPanel.tsx` |
| `CanonicalBookView` | N1 firm overview (when `clientsTabData != null`) | `_shared/panels/CanonicalBookView.tsx` |
| Leaderboard section (inline) | N1 advisor list | `_shared/tabs/ClientsTab.tsx` (internal) |
| `AdvisorBookView` | L2 advisor drill | `_shared/AdvisorBookView.tsx` |
| `AdvisorBookClientDetail` | L3 client detail | `_shared/AdvisorBookClientDetail.tsx` |
| `AdvisorBookAccountModal` | L4 account modal | `_shared/AdvisorBookAccountModal.tsx` |

### Components NOT active for Inflection (GRAY)

| Component | Why disabled |
|-----------|-------------|
| `AdvisorsTab` | `tabs.advisors.enabled: false` |
| `AdvisorPublicProfile` | `panels.advisorPublicProfile.enabled: false` |
| `FeeEfficiencyPanel` | `revenueOpsPanel !== 'standard'` → `hideFeeEfficiency=true` at `ClientsTab.tsx:680` |
| `FeeRoleBreakdownPanel` | Andrew descope 2026-05-04 |
| `FeeSummaryPanel` | Andrew descope 2026-05-04 |
| `FidelityCustodianBar` | Andrew descope 2026-05-04 |

---

## § 2 — Component → S3 Artifact Wirings

### InflectionAdvisorIntelligence (page shell)

| Fetch function | S3 artifact | `?firm=` param | Purpose |
|----------------|-------------|----------------|---------|
| `getPlatinumPartnerAnalytics('quarterly', firmOverride)` | `platinum/firm/partner_analytics_quarterly.json` | `?firm=inf` | Page `generated_at` timestamp + passed to PartnerAnalytics |

Route: Browser → CF → `shared-advisor-router` Lambda@Edge → `opal-data-inf` S3 bucket (via `firm=inf` bucket swap).

### PartnerAnalytics

| Fetch function | S3 artifact | `?firm=` param | Fields rendered |
|----------------|-------------|----------------|-----------------|
| `getPlatinumPartnerAnalytics(granularity, firmOverride)` | `platinum/firm/partner_analytics_quarterly.json` | `?firm=inf` | `views.geo.donut.segments`, `views.geo.distribution`, `views.geo.metrics`, top-level `periods[]`/`rows[]` |
| (internal fetch) | `platinum/firm/timeseries_overview.json` | `?firm=inf` | `aua.quarterly`, `nna.quarterly`, `growth_decomposition.quarterly`, `mix.quarterly` |

Guards: `allowedViewModes: ['geo']` → only geo-path code executed; other view modes (aua/nna/adv) dead.

### DistributionTab

| Fetch function | S3 artifact | `?firm=` param | Notes |
|----------------|-------------|----------------|-------|
| `getPlatinumPartnerAnalytics(granularity, firmOverride)` | `partner_analytics_quarterly.json` | `?firm=inf` | Snapshot mode |
| (internal) | `platinum/firm/cumulative_chart.json` | `?firm=inf` | Continuous mode — `geo` + `geo_drill` keys |
| `getPlatinumAdvisorNnaClients(advisorId, firmOverride)` | `platinum/advisors/{id}/nna_clients.json` | `?firm=inf` | RED — artifact MISSING for all 4 advisors; ADV cohort disabled so this path not hit for Inflection |

Gates: `cohorts.adv: 'disabled'` and `cohorts.ofc: 'disabled'` → only geo cohort selector rendered.

### BooksTab N1 (firm dashboard)

| Fetch function | S3 artifact / endpoint | `?firm=` param | Fields used |
|----------------|------------------------|----------------|-------------|
| `getPlatinumFirmDashboard(firmOverride)` → internally: | | | |
| └ `platinum/firm/dashboard.json` | `?firm=inf` | `split`, `headline.{total_aua, account_count, client_count, ytd.{nna,inflows,outflows}}` | |
| └ `getFirmLeaderboard(firmOverride)` | `platinum/firm/leaderboard.json` | `?firm=inf` | 4-advisor entries; `windows.{QTD,YTD,MAX}` |
| └ `platinum/firm/fee_efficiency.json` | `?firm=inf` | `setFeeEfficiencyData(null)` for Inflection (FeeEfficiency panel hidden) | |
| └ clients_tab Lambda endpoint | `/scoped/advisor-intelligence/platinum/firm/clients_tab.json` | `?firm=inf` | Inflection returns no `clients_tab.headline` → `setClientsTabData(null)` |
| `getPlatinumFirmMixSummary(firmOverride)` | `platinum/firm/mix_summary.json` | `?firm=inf` | `composition`, `mix_periods` → firm N1 CanonicalBookView mix bar |
| `getHeaderMetrics(firmOverride)` | `platinum/firm/header_metrics.json` | `?firm=inf` | `total.{fee_earning_aua, fee_earning_client_count, non_fee_earning_aua, non_fee_earning_client_count}` — Inflection fee split source |

**Critical N1 control flow for Inflection:**
```
clientsTabData === null (always for Inflection — no clients_tab.headline in dashboard.json)
  → layout.tabs.books.revenueOpsPanel === 'inflection_insights'
    → banner suppressed (INFLFE.006 Line 210 fix, 63edaad6, ClientsTab.tsx:665)
    → revenueOpsSlot renders directly = InflectionInsightsPanel
  → CanonicalBookView does NOT render (clientsTabData null)
```

**Post-D2b / v10 update:** `header_metrics.json` + `mix_summary.json` now populate Firm Overview via backfill path when `clientsTabData` is null. Wait — re-reading code: `setClientsTabData` is only set when `dash.clients_tab?.headline` exists (ClientsTab.tsx:318-336). If null, `CanonicalBookView` is not rendered regardless. The `header_metrics` total is merged into `clientsTabData.headline` when the headline IS present — it does not create a headline from scratch. So for Inflection: **CanonicalBookView is not rendered at N1.** The Firm Overview visible at N1 is `revenueOpsSlot` = InflectionInsightsPanel only.

### BooksTab L2 (advisor drill)

| Fetch function | S3 / API path | `?firm=` param | Mapping notes |
|----------------|---------------|----------------|---------------|
| `getPlatinumAdvisorSummary(advisorId, firmOverride)` | API GW → opal-partners-data Lambda → `platinum/advisors/{id}/summary.json` in `opal-data-inf` | `firmOverride='inf'` → Lambda uses `LAMBDA_FIRM_ID['inf'] = 'inflection'` | Maps `plat.book`, `plat.mix`, `plat.concentration`, `plat.fee_summary`, `plat.mix_periods` to `AdvisorBookResponse` shape |

Sentinel: `warnOnInflectionAdvisorDrift(r)` checks `book`, `mix`, `fee_summary` keys present (INFLFE.002 `72a6c1f4`).

Also fetches (via `useQuery` inside `AdvisorBookView`):
- `getPlatinumAdvisorTimeseries(advisorId, firmOverride)` → `platinum/advisors/{id}/timeseries.json` — GRAY (sole consumer `AdvisorPublicProfile` disabled; 404-tolerant guard returns `{ data: [] }` from INFLFE.003 Cell 7 fix, `d52d04a0`)
- `getAdvisorExecSummary(advisorId, firmOverride)` → `platinum/advisors/{id}/exec_summary.json` — check if rendered; 404-tolerant

### BooksTab L3 (client detail — Inflection static path)

| Fetch function | S3 artifact | `?firm=` param | Guard |
|----------------|-------------|----------------|-------|
| `getPlatinumClientDetailStatic(clientKey, firmOverride)` | `platinum/clients/{hhId}/detail.json` | `?firm=inf` | Gate: `isInflectionFirm = firmOverride === 'inf' \|\| firmOverride === 'inflection'` at `ClientsTab.tsx:400` |

Sentinel: `warnOnInflectionClientDrift(r)` checks `relationship_id`, `detail.total_aua`, `detail.accounts[]`, `detail.tax.realized`, `detail.tax.unrealized` (INFLFE.002 `72a6c1f4`).

Note: Standard 49F path uses Lambda `getPlatinumClientSummary` → opal-partners-data. Inflection uses direct S3 static JSON (AUDIT-004 `fc88893a`).

### BooksTab L4 (account modal)

| Fetch function | S3 artifact | `?firm=` param |
|----------------|-------------|----------------|
| `getPlatinumAccountSummary(accountId, firmOverride)` | `platinum/accounts/{accountId}/summary.json` | `?firm=inf` |

### InflectionInsightsPanel (Revenue Ops revenueOpsSlot)

| Fetch function | S3 artifact | React Query key | Guards |
|----------------|-------------|-----------------|--------|
| `getInflectionActivityScan(firmOverride)` | `platinum/firm/activity_scan.json?firm=inf` | `['inflection-activity-scan', firmOverride]` | `allAuaZero = data.every(r => r.aua === 0)` → "Awaiting data"; `data.length === 0` → "No data yet" |
| `getInflectionCashDrag(firmOverride)` | `platinum/firm/cash_drag.json?firm=inf` | `['inflection-cash-drag', firmOverride]` | `allCashAuaZero = data.every(r => r.cash_aua === 0)` → "Awaiting data"; `data.length === 0` → "No data yet" |
| `getInflectionConcentrationRisk(firmOverride)` | `platinum/firm/concentration_risk.json?firm=inf` | `['inflection-concentration-risk', firmOverride]` | `data.length === 0` → "No data yet" (no all-zero guard needed — HHI non-zero by definition) |

Route: Browser → CF → `shared-advisor-router` Lambda@Edge (origin-request) → S3 `opal-data-inf` **directly**. Does NOT go through `opal-partners-data` Lambda. CF path: `/api/scoped/advisor-intelligence/platinum/firm/{activity_scan,cash_drag,concentration_risk}.json`.

Sentinels (INFLFE.002): `warnOnInflectionActivityShape` (checks array + `aua` key), `warnOnInflectionCashDragShape` (checks `cash_aua` key), `warnOnInflectionConcentrationShape` (checks `hhi` key) — all `console.warn` only, no crash.

STALE_TIME: 5 minutes. `refetchOnWindowFocus: false`. `retry: 1`.

---

## § 3 — Known Gaps per Surface (matrix v10 state)

### YELLOW — FE or surface-ambiguity issues (3 cells)

| Cell | Surface | Root cause | FE vs upstream | Matrix row | Next action |
|------|---------|-----------|----------------|-----------|-------------|
| `composition.json` per-advisor — asset mix not visible at L3 client detail | ADV drill / L2 | Surface ambiguity: `composition.json` is an L2 advisor artifact; L3 client detail renders per-client mix (separate artifact `platinum/clients/{id}/detail.json`). FE code for L2 advisor `CanonicalBookView` likely does render composition — Andrew's observation was at L3. Need clarification. | Surface-ambiguity (not a code bug) | § Surface 6 | DE: disambiguate via RD Playwright — click L2 advisor drill, check if asset mix donut renders there; separately check L3 |
| `top_holdings.json` per-advisor — not visible at L3; 3/4 stale; joe_brandenburg MISSING | ADV drill / L2+L3 | Data issue: `top_holdings.json` is L2 advisor artifact (last updated 2026-04-28, 6 days stale). joe_brandenburg artifact MISSING entirely (INF_I_D02b catalog gap). L3 client top holdings = separate per-client artifact (missing). | Data gap (DS/AE upstream for freshness + joe_brandenburg add) + surface-ambiguity | § Surface 6 | DS/AE: INF_I_D02b catalog add + stale republish; DE: confirm L2 vs L3 render surface |
| L3 client detail — asset mix / time machine snapshot / top holdings absent | BooksTab L3 | Per-client platinum artifact (`platinum/clients/{hhId}/detail.json`) lacks mix, timeseries, and top_holdings sections. Cost basis ✓, tax ✓, fee summary ✓, accounts[] ✓ — but 3 panel sections empty. FE code is wired for these fields (mapping correct per INFLFE.002 sentinel pass); data is not emitted. | Upstream data gap — DS/AE AUDIT-009 scope | § Surface 4 BooksTab L3 | DS/AE: per-client mix + timeseries + holdings publishers (AUDIT-009) |

### RED — Data missing / wrong (3 cells)

| Cell | Surface | Root cause | Owner | Matrix row | Next action |
|------|---------|-----------|-------|-----------|-------------|
| Leaderboard `period_start_aua` null on MAX window → phantom `aua_growth_pct` (+4213% Peter, +7522% Patrick) | BooksTab N1 leaderboard | `INF_B_00.latest_accounts_v2_key()` L162-172 returns `keys[-1]` (latest partition) for every `snap_date_str` — rep_bucket reflects today's advisor attribution, not historical point-in-time. Fix: `accounts_v2_key_for_date(snap_date_str)`. | DS~D (ADVI_RPBKTPI scope) | § Surface 4 | RPBKTPI TO — no FE code change needed; FE correctly renders null as "N/A" |
| Leaderboard `lifecycle_aua` all zero across 4 advisors (NMNC/NMEC/existing decomposition = $0) | BooksTab N1 leaderboard | Upstream publisher gap — lifecycle_aua per-advisor decomposition not populated at Inflection advisor grain. | DS / AE | § Surface 4 | DS/AE investigation — no FE code change needed |
| `joe_brandenburg/top_holdings.json` MISSING from S3 | ADV drill | joe_brandenburg rep_id resolution not in INF_I catalog; catalog add + AE rerun needed. | AE 0.6.1 / AE 0.7 + DS~B (INF_I_D02b) | § Surface 6 | INF_I_D02b catalog add + AE SSM dispatch |

### RED-(c) / RED-INVESTIGATE — Scope-deferred upstream dims (Surface 7, 4 cells)

These are not FE bugs. Listed for completeness.

| Cell | Status | Blocker |
|------|--------|---------|
| Tax dim silver | Scope-deferred per `def351cb4` | HISTBF.005/.006 backlog |
| Billing dim silver | Scope-deferred per `def351cb4` | Same |
| Cost-basis `includeCostBasis=true` flag flip | Scope-deferred per `def351cb4` | Single query-param flip on Orion API calls |
| Reporting/Scope endpoint family (HAR 7) | RED-INVESTIGATE | Books-tab HAR capture needed |

### GRAY — Out of scope (14 cells)

Per `layout.ts` + Andrew descope rulings. Full list in `docs/architecture/ADVI_INFLEC_AUDIT.md § Out-of-Scope`.

---

## § 4 — FE Conditional Gates (full enumeration)

### `useTenantLayout(firmId)` — layout config map

| firmId value | Layout returned | Location |
|-------------|----------------|----------|
| `'inflection'` | `INFLECTION_LAYOUT` | `_partners/inflection/layout.ts` |
| anything else (`'bd'`, unknown) | `DEFAULT_LAYOUT` | `_shared/types/TenantLayoutConfig.ts` |

Called in: `InflectionAdvisorIntelligence` (inflection/index.tsx), `BooksTab` (ClientsTab.tsx:119), `AdvisorsTab`, `AdvisorBookView`.

### INFLECTION_LAYOUT flags and their FE effects

| Flag | Value | FE effect | Location |
|------|-------|-----------|----------|
| `tabs.partnerAnalytics.defaultViewMode` | `'geo'` | PartnerAnalytics mounts in geo view by default | `layout.ts:19` |
| `tabs.partnerAnalytics.allowedViewModes` | `['geo']` | View-mode toggle (AUA/NNA/ADV/GEO selector) hidden; non-geo donut/bell paths dead | `layout.ts:20` |
| `tabs.distribution.cohorts.geo` | `'enabled'` | Geo cohort selector visible in DistributionTab | `layout.ts:27` |
| `tabs.distribution.cohorts.adv` | `'disabled'` | ADV cohort tab not rendered; `getPlatinumAdvisorNnaClients` not called | `layout.ts:27` |
| `tabs.distribution.cohorts.ofc` | `'disabled'` | OFC cohort tab not rendered | `layout.ts:27` |
| `tabs.books.advisorDrill.enabled` | `true` | Advisor name rows are clickable → L2 drill | `layout.ts:35` |
| `tabs.books.revenueOpsPanel` | `'inflection_insights'` | (1) Banner suppressed (`ClientsTab.tsx:665`); (2) `hideFeeEfficiency=true` (`ClientsTab.tsx:680`); (3) `revenueOpsSlot` renders directly | `layout.ts:36` |
| `tabs.advisors.enabled` | `false` | Advisors tab filtered from `adminTabs[]` and `nonAdminTabs[]` → not rendered | `layout.ts:38` |
| `panels.advisorList.maxEntries` | `4` | Leaderboard entries sliced to `capped.slice(0, 4)` at `ClientsTab.tsx:290` | `layout.ts:42` |
| `panels.advisorList.allowedAdvisorKeys` | `['inflection_wealth_management','peter_lee','patrick_scanlan','joe_brandenburg']` | Leaderboard entries filtered by `allowedAdvisorKeys.includes(e.advisor_id)` at `ClientsTab.tsx:288` | `layout.ts:43` |
| `panels.advisorPublicProfile.enabled` | `false` | Profile tab filtered out; `active_since` consumer dead; `getPlatinumAdvisorTimeseries` consumer dead | `layout.ts:45` |

### Inflection-specific code gates (not in layout.ts)

| Gate | Location | Effect |
|------|----------|--------|
| `firmOverride = internal ? FIRM_ID : undefined` where `FIRM_ID = 'inf'` | `inflection/index.tsx:154` | Internal users send `?firm=inf` on all S3 fetch calls; external Inflection users rely on `X-Firm-Id` JWT claim (Lambda@Edge passthrough) |
| `isInflectionFirm = firmOverride === 'inf' \|\| firmOverride === 'inflection'` | `ClientsTab.tsx:400` | Routes L3 to `getPlatinumClientDetailStatic` (static S3 JSON) instead of `getPlatinumClientSummary` (Lambda BD-shape) |
| `layout.tabs.books.revenueOpsPanel !== 'inflection_insights'` (banner gate) | `ClientsTab.tsx:665` | Suppresses "historical backfill" banner for Inflection (INFLFE.006 Line 210 fix `63edaad6`) |
| `layout.tabs.books.revenueOpsPanel !== 'standard'` (fee efficiency gate) | `ClientsTab.tsx:680` | Passes `hideFeeEfficiency=true` to CanonicalBookView → FeeEfficiencyPanel not rendered |
| `revenueOpsPanel === 'standard'` role chip gate | AdvisorBookView (INFSHIP Phase 3 Bug 3 fix) | Role chips gated on standard layout; Inflection `role_breakdown: {}` empty + chip render suppressed |

### Default layout differences (49F vs Inflection)

| Flag | DEFAULT_LAYOUT (49F) | INFLECTION_LAYOUT |
|------|----------------------|-------------------|
| `tabs.advisors.enabled` | `true` | `false` |
| `tabs.distribution.cohorts.adv` | `'enabled'` | `'disabled'` |
| `tabs.distribution.cohorts.ofc` | `'enabled'` | `'disabled'` |
| `tabs.books.revenueOpsPanel` | `'standard'` (FeeEfficiencyPanel) | `'inflection_insights'` (InflectionInsightsPanel) |
| `panels.advisorList.maxEntries` | `Infinity` | `4` |
| `panels.advisorList.allowedAdvisorKeys` | `[]` (no filter) | `[4 named keys]` |
| `panels.advisorPublicProfile.enabled` | `true` | `false` |

---

## § 5 — Pending FE Follow-ons

### Line 211 — AUA strip update (D2b chain; ETA 20:10-20:30Z)

**What's changing:** DS~C canonical_holdings re-fire + AE 0.7 `_orion_api_silver_lib.py` stale-at-S3 fix → `dashboard.json#headline.total_aua` updates from $182.55M → ~$199M. Downstream cascade also updates per-advisor leaderboard data, potentially `header_metrics.json` AUA total, and InflectionInsightsPanel source data.

**FE code assessment — no changes expected.** FE handles dynamic values. All AUA fields rendered via `formatCurrency()` with no hardcoded values. No FE code change needed for the strip update.

**Post-D2b cascade diagnostic plan:**

| Scenario | Trigger | FE behavior | RD capture target | FE action needed |
|----------|---------|-------------|-------------------|-----------------|
| A: `period_start_aua` still null post-chain (RPBKTPI not fixed) | D2b re-fire does not touch accounts_v2 join | Phantom `aua_growth_pct` persists (+4213% Peter). `groNa` guard at leaderboard → shows "N/A" for nulls. No crash. | Leaderboard cards for all 4 advisors — confirm GRO% column values. Confirm `groNa` renders "N/A" correctly when null. | None — RPBKTPI is DS~D scope |
| B: `period_start_aua` populated on QTD/YTD post-chain (partial RPBKTPI progress) | New leaderboard window entries have non-null period_start_aua | `aua_growth_pct` renders real percentages. QTD/YTD windows show corrected growth. MAX may still show null. | Leaderboard QTD vs MAX window comparison. Confirm period selector renders correct numbers per window. | None — FE already handles mixed null/non-null correctly |
| C: `lifecycle_aua` flips non-zero per-advisor | Chain updates advisor-grain lifecycle decomposition | Role decomposition in L2 `AdvisorBookView` lifecycle section renders non-zero NMNC/NMEC/existing. Leaderboard role donut may populate. | L2 Peter Lee drill → lifecycle/role donut section. Leaderboard N1 role decomposition per advisor card. | None — FE handles non-zero values correctly |
| D: Headline AUA updates to ~$199M | D2b canonical_holdings + silver lib fix refreshes all downstream artifacts | N1 leaderboard total, PartnerAnalytics geo donut center, per-advisor L2 totals all update. `header_metrics.json#total.aua` updates. | PartnerAnalytics panel — center AUA value. N1 leaderboard sum across 4 advisors. L2 Peter Lee / Patrick / Joe individual totals. | None — formatCurrency handles any value |
| E: InflectionInsightsPanel regression (INFLFE.003 allAuaZero re-fires) | New chain emits zero-AUA rows (unlikely — AUDIT-002 confirmed non-zero) | INFLFE.003 guard triggers → "Awaiting data" shown instead of table. | Revenue Ops all 3 sub-panels — confirm `awaiting_data_count=0` and rows render. | None expected; if triggered = DS upstream regression, not FE bug |

**RD consolidated Playwright sweep — explicit capture targets for D2b RAVC5:**

| Capture | Target element | Pass criterion |
|---------|---------------|---------------|
| `d2b_01_n1_headline.png` | N1 Firm Overview / leaderboard AUA total | Total ≠ $182M (updated) |
| `d2b_02_leaderboard_cards.png` | All 4 advisor cards — GRO% column | No phantom >1000% values (if RPBKTPI fixed); OR "N/A" renders cleanly (if still null) |
| `d2b_03_lifecycle_decomp.png` | Leaderboard advisor card lifecycle NMNC/NMEC/existing section | Non-zero values if upstream fixed; $0 if not (no crash either way) |
| `d2b_04_revenue_ops.png` | InflectionInsightsPanel all 3 sub-panels | awaiting_data_count=0; rows visible; no regression |
| `d2b_05_l2_peter_drill.png` | L2 Peter Lee drill — top-level AUA | Updated from $161M if chain reruns per-advisor data |
| `d2b_06_partner_analytics.png` | PartnerAnalytics geo donut center | Updated AUA value |
| `d2b_07_distribution_snapshot.png` | DistributionTab snapshot mode | Renders correctly (regression check) |

### Line 212 — Per-client publishers gap (AUDIT-009 scope; no FE action)

Andrew 2026-05-05 confirmed L3 client detail renders cost basis ✓, tax ✓, fee summary ✓ — but missing: asset mix donut, time machine snapshot lookback, top holdings panel. These 3 missing sections are tracked as AUDIT-009 DS/AE publisher scope. FE code is pre-wired for these sections (mapping exists in `getPlatinumClientDetailStatic` adapter at `endpoints/advisor-intelligence.ts:884`); no FE code change needed until publishers ship the data.

**FE is complete at L3.** When DS/AE AUDIT-009 ships:
1. `detail.mix` → will populate asset mix donut via existing `compositionData` useMemo (`ClientsTab.tsx:435-440`)
2. `detail.mix_periods` → will populate time machine quarterly bar via existing `l3QuarterlyMix` (`ClientsTab.tsx:442`)
3. `detail.top_holdings` → unclear if currently in static adapter output; may need DE wiring pass post-AUDIT-009 data landing

### Tech-debt GRAY cell audit (bandwidth item)

The 14 GRAY cells in the matrix include:
- `radial_12m` — **CLEANED** (AUDIT-007 `e68f54e7` removed `RadialSegment`, `RadialData`, `radial_12m` field from `types.ts` + comment from `advisor-intelligence.ts`)
- `active_since` — sole consumer `AdvisorPublicProfile` disabled for Inflection; data null post-S7SUMFIX. **No code to remove** — `active_since` renders in `AdvisorPublicProfile.tsx` which IS the standard 49F path. Cannot delete.
- `FeeEfficiencyPanel`, `FeeRoleBreakdownPanel`, `FeeSummaryPanel` — standard 49F panels; code must remain for DEFAULT_LAYOUT path. No dead-code removal possible for Inflection descope.
- ADV/OFC cohort code in `DistributionTab.tsx` — gated by `cohorts.adv: 'disabled'`; code is structural (used for 49F); no removal.

**Conclusion:** `radial_12m` was the only true dead-code candidate across all 14 GRAY cells. Already cleaned. No further tech-debt cleanup warranted without an explicit AUDIT-008+ pass.

---

## Summary Scorecard (v10 baseline)

| Status | Count | Surfaces |
|--------|-------|---------|
| GREEN | ~32 | Page header (4), PartnerAnalytics (8), DistributionTab (4), BooksTab N1+L2+L4 (13+), ADV drill (5), InflectionInsightsPanel (3) |
| GREEN-by-design | 1 | PartnerAnalytics `views.geo` flat shape (no q1/q2/q3 nesting) |
| YELLOW | 3 | L2 composition ambiguity; L2/L3 top_holdings; L3 client detail missing fields |
| RED | 3 | Leaderboard period_start_aua (RPBKTPI); lifecycle_aua zero; joe_brandenburg top_holdings MISSING |
| RED-(c/b/investigate) | 5 | Surface 7 upstream dims (scope-deferred) |
| GRAY | 14 | Out-of-scope per layout.ts + Andrew descope |

**FE completion assessment:** FE code is complete and correct for all GREEN + GREEN-by-design cells. All 3 YELLOW cells trace to data-layer gaps or surface ambiguity (not FE bugs). All 3 RED cells are DS~D / DS~B / AE upstream scope. No FE code changes are pending or required to unblock any RED cell.

**Portal commits included in this baseline:**

| Commit | TO | Change |
|--------|-----|--------|
| `63edaad6` | INFLFE.006 | Line 210 banner suppression |
| `72a6c1f4` | INFLFE.002 | Envelope contract sentinels (3 components) |
| `6fd66973` | INFLFE.003 | Cells 1-3 allAuaZero defensive render |
| `d52d04a0` | INFLFE.003 | Cell 7 timeseries 404-tolerant |
| `e68f54e7` (pending submodule bump) | AUDIT-007 | radial_12m dead-code removal |
