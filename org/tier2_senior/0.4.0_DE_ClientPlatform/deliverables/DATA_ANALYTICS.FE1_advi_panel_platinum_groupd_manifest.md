# DATA_ANALYTICS.FE1 — ADVI Dashboard PANEL → COMPONENT → PLATINUM → Group-D Threaded Manifest

**TO:** DATA_ANALYTICS.FE1 (`org/tier2_senior/0.4.0_DE_ClientPlatform/task_orders/`)
**Author:** 0.4.0_DE_ClientPlatform | **Date:** 2026-06-25 | **archetype:** TRACE
**Verify:** 3.0.0_SA_CVO (completeness + per-partner correctness) | **cc:** 0.4.0_DS_ClientPlatform
**Spine tool:** `pipescript` (advi-bd / advi-inf / advi-cot) | **FE bind:** endpoint source + `comp-transform schema-check` | **Producers:** `comp-pipescript io` + `comp-platinum reverse`

> The "ADVI dashboard" = the **AdvisorIntelligence** page (`portal/src/pages/AdvisorIntelligence/`). It is a SINGLE shared
> component tree (`_shared/{panels,tabs,components,charts}`) selected per-partner by a per-tenant `layout.ts`
> (`TenantLayoutConfig`) via `_shared/hooks/useTenantLayout.ts`. The PANELS are common; **which panels render, and which
> producer feeds them, is the per-partner divergence** — and that divergence lives in `layout.ts`. Three partners in scope:
> **49F** (`49financial`, BD pipeline, bucket `opal-data-bd`), **Inflection** (`inflection`, Orion pipeline, `opal-data-inf`),
> **Cottonwood** (`cottonwood`, BD-native pipeline, `opal-data-cot`). (`demo` exists as a 4th tenant — OUT OF SCOPE.)

---

## 0. The serving spine (identical wire path for all three partners)

```
PANEL (rendered)
  -> shared COMPONENT (_shared/tabs|panels|components)  [endpoint fn in src/api/endpoints/advisor-intelligence.ts]
    -> /api/scoped/advisor-intelligence/...  (CloudFront)
      -> shared-advisor-router Lambda@Edge (PPI-08)  [?firm=<suffix> | X-Firm-Id(JWT) -> FIRM_BUCKET_MAP]
        -> s3://opal-data-{bd|inf|cot}/platinum/...   (static JSON)   OR
        -> opal-partners-data Lambda  (PII / dynamic: clients-tab, advisor/client platinum-summary)
          <- written by the partner's Group-D publisher  (gold_dispatch.sh D_* stage)
```
- `bucketSuffix()` in `advisor-intelligence.ts:81` maps portal-canonical firmId → S3 suffix: `49financial→bd`, `inflection→inf`, `cottonwood→cot`, `demo→demo`.
- Response edge: `shared-advisor-router-response` (PPI-09) injects `Cache-Control: max-age=60` (CDNCOHT) + rewrites 4xx S3 NoSuchKey → JSON error envelope (LEDGEH, prevents SPA-HTML-at-200 cache poisoning).
- **Backend pipeline producing the platinum each partner reads:** 49F = `bd-gold-layer-pipeline` (EC2 `bd-gold-layer-runner`, `gold_dispatch.sh`); INF = `inf-gold-dispatch-ec2` (`inf-gold-layer-runner`, `orion-gold-dispatch.sh`); COT = `cot-pipeline` (`cot-exporter` EC2, `data/cot/scripts/gold/gold_dispatch.sh`).

---

## 1. Per-partner panel ENABLEMENT matrix (source: `_partners/{p}/layout.ts`)

| Panel / tab | 49F (`49financial`) | Inflection (`inflection`) | Cottonwood (`cottonwood`) |
|---|---|---|---|
| PartnerAnalytics header | ✓ views: aua/nna/geo/adv (all) | ✓ **geo only** (`allowedViewModes:['geo']`) | ✓ aua/nna/geo (**no adv**) |
| Distribution tab | ✓ cohorts geo+adv+**ofc** | ✓ geo+adv (**ofc off**) | ✓ **geo only** (adv+ofc off) |
| Advisors tab | ✓ enabled | ✗ disabled (4 employees) | ✗ disabled (2-founder) |
| Books tab | ✓ advisorDrill, revenueOps=`standard` | ✓ advisorDrill, revenueOps=`inflection_insights` | ✗ **disabled** (v1 OUTCOME-B) |
| AdvisorPublicProfile (Profile) | ✓ | ✓ | ✗ disabled |
| Cohort-A transparency | ✓ (`getCohortASummary`) | ✗ (not wired) | ✗ |
| Inflection Insights panel | ✗ | ✓ (activity/cash-drag/concentration) | ✗ |
| Role-Composition donut | ✓ (`composition.enabled`) | ✗ | ✗ |
| GRO decomposition | ✗ | ✓ (`groDecomposition.enabled`) | ✗ |
| AUA-donut source | `gold_aua` | `partner_analytics_views` | `gold_aua` |
| Bar chart | single-series (NMNC) | **stacked** (NMNC+NMEC) | single-series (NMNC) |
| FidelityCustodianBar overlay | ✗ (BD custodian) | ✓ (`overrides/FidelityCustodianBar`) | ✗ |
| Client/account drill handler | Lambda | **static-S3** (book/detail/composition.json) | Lambda (forward-only; Books off) |

---

## 2. THE THREAD — panel → component → platinum artifact → Group-D script

Endpoint fn → S3 platinum key from `src/api/endpoints/advisor-intelligence.ts`. Producer grounded via `comp-platinum reverse` + `comp-pipescript io`.
**Producer-name divergence:** 49F & COT scripts are bare `D_0x.*`; Inflection scripts are `INF_D_0x.*` / `INF_09.*`. **For 49F & COT, `D_04.client_portal_summary.py` is the SINGLE platinum publisher** — `D_00/D_00b/D_00c/D_01/D_00f/D_02/D_03` write `gold/artifacts/*` intermediates that `D_04` republishes to `platinum/`. **Inflection fans the publish across many `INF_D_0x` scripts** (one per artifact family).

### 2.1 PartnerAnalytics header — `_shared/components/PartnerAnalytics.tsx` (always-visible)
Sub-panels: view toggle (AUA/NNA/GEO/ADV) → donut + bell-curve + quarterly metric cards + time-machine strip.

| Component query | Platinum artifact | 49F producer | INF producer | COT producer |
|---|---|---|---|---|
| `getPlatinumPartnerAnalytics(gran)` | `platinum/firm/partner_analytics_{monthly,quarterly,annual}.json` | `D_01.partner_analytics` → `D_04` | **`INF_09.generate_partner_analytics.py`** → `INF_D_04` | `D_01.partner_analytics` → `D_04` |
| `getTimeseriesOverview()` | `platinum/firm/timeseries_overview.json` | `D_00b`→`D_04::build_timeseries_overview` | `INF_D_00b.portal_timeseries` | `D_00b`→`D_04` |
| `getHeaderMetricsFresh()` | `platinum/firm/header_metrics_fresh.json` | `D_00` (D-min)* | **`INF_D_00e.fresh_header_supplement`** | `D_00`* |
| `getPlatinumInflecTimeseriesChart()` | `platinum/firm/timeseries_chart.json` | `D_00b`→`D_04` | `INF_D_00b.portal_timeseries` | `D_00b`→`D_04` |

\* `header_metrics_fresh` is an Inflection-origin pattern (`INF_D_00e`, ADHC_BPMVH D-min). 49F/COT header headline falls back to canonical `header_metrics.json` (`D_00`→`D_04`) when fresh is absent — **flag: confirm `header_metrics_fresh.json` presence on bd/cot with DS** (graceful-degrade exists, but verify it's intended-absent vs a gap).

### 2.2 Distribution tab — `_shared/tabs/DistributionTab.tsx` (default tab)
Snapshot/Continuous toggle; metric AUA/NNA/CLA; GEO/ADV cohort selector → donut + bell curve.

| Component query | Platinum artifact | 49F | INF | COT |
|---|---|---|---|---|
| `getPlatinumPartnerAnalytics` (snapshot donut) | `partner_analytics_{gran}.json` | `D_01`→`D_04` | `INF_09`→`INF_D_04` | `D_01`→`D_04` |
| `getTimeseriesOverview` | `timeseries_overview.json` | `D_00b`→`D_04` | `INF_D_00b` | `D_00b`→`D_04` |
| `getPlatinumCumulativeChart` (continuous) | `platinum/firm/cumulative_chart.json` | `D_04::build_cumulative_chart` | **`INF_D_00d.cumulative_chart`** | `D_04::build_cumulative_chart` |
| `getAdvisorNnaCanonical` (continuous NNA / drill) | `platinum/firm/advisor_nna_canonical.json` | `D_00f.advisor_nna_canonical`→`D_04` | `INF_D_00f.advisor_nna_canonical` | **GAP — no `D_00f` in `data/cot/scripts/gold/`** ⚠ |
| `getPlatinumAdvisorNnaClients` (ADV-NNA client drill) | `platinum/advisors/{id}/nna_clients.json` | `D_02`→`D_04` | `INF_D_02.advisor_client_detail` | (adv disabled — not consumed) |
| `getPlatinumAdvisorSummary` (drill parent) | `advisor/{id}/platinum-summary` (Lambda) / INF static `book.json`+`composition.json` | `D_02`/`D_04` | `INF_D_02`+`INF_D_03` (static) | (adv disabled) |

⚠ **COT divergence/gap:** COT Distribution is GEO-only (adv off) and COT gold has **no `D_00f.advisor_nna_canonical`** — `getAdvisorNnaCanonical(cottonwood)` would 404 → empty. Acceptable IF continuous-NNA is not surfaced for COT v1 (Distribution is geo-centric); **flag to DS/CVO to confirm intended-absent.**

### 2.3 Advisors tab — `_shared/tabs/AdvisorsTab.tsx` + `_shared/components/AdvisorAnalytics.tsx`  (**49F ONLY**)
TOP-3 + Rolling Flows (LineChart) + Leaderboard table.

| Component query | Platinum artifact | 49F producer | INF / COT |
|---|---|---|---|
| `getFirmLeaderboard()` | `platinum/firm/leaderboard.json` | `D_00c`→`D_04::build_firm_dashboard` | tab disabled both |
| `getPlatinumAdvisorTimeseries(id)` | `platinum/advisors/{id}/timeseries.json` | `D_04` | n/a |
| `getAdvisorMixViews(id)` | `advisors/{id}/mix-views` (Lambda) ← `platinum/advisors/{id}/mix.json` | `D_04` | n/a |
| `getAdvisorNnaCanonical()` | `platinum/firm/advisor_nna_canonical.json` | `D_00f`→`D_04` | n/a |

### 2.4 Books tab — `_shared/tabs/ClientsTab.tsx` + `_shared/AdvisorBookView.tsx`  (**49F + Inflection; COT disabled**)
Sub-panels (`_shared/panels`): ConsolidatedOverviewPanel, TaxCostBasisPanel, FeeEfficiencyPanel/FeeSummaryPanel, ClientListPanel, CanonicalBookView → drills to ClientDetail → Account.

| Component query | Platinum artifact | 49F producer | INF producer |
|---|---|---|---|
| `getPlatinumFirmDashboard()` (split: leaderboard+fee_efficiency+clients-tab) | `platinum/firm/dashboard.json` (+`leaderboard.json`,`fee_efficiency.json`, clients-tab Lambda) | `D_04::build_firm_dashboard`; fee_eff via `D_00c` | `INF_D_00`/`INF_D_00c`→`INF_D_04` |
| `getPlatinumFirmMixSummary()` | `platinum/firm/mix_summary.json` | `D_04` | **`INF_D_02d.firm_mix_summary`** |
| `getHeaderMetrics()` | `platinum/firm/header_metrics.json` | `D_00`→`D_04` | `INF_D_00`→`INF_D_04` |
| `getClientDirectory()` | `platinum/firm/client_directory.json` | `D_04` | **`INF_D_02c.client_directory`** |
| `getPlatinumAdvisorSummary(id)` (book drill) | Lambda `platinum-summary` / **INF static** `advisors/{id}/book.json`+`composition.json` | `D_02`+`D_03`→`D_04` (Lambda) | **`INF_D_02.advisor_client_detail`(book) + `INF_D_03.composition_artifacts`(composition)** |
| `getPlatinumClientSummary` / `getPlatinumClientDetailStatic(hh)` | Lambda / **INF static** `clients/{hh}/{detail,composition,top_holdings,timeseries}.json` | `D_04` (Lambda) | `INF_D_02`(detail)+`INF_D_03`(composition)+`INF_D_05.client_top_holdings`+`INF_D_06.client_timeseries`+`INF_D_04b.client_publishers` |
| `getPlatinumAccountSummary(acct)` | `platinum/accounts/{acct}/summary.json` | `D_04` | `INF_D_04` |
| `getPlatinumAccountTimeseriesStatic(hh,acct)` | `platinum/clients/{hh}/accounts/{acct}/timeseries.json` | (Lambda handler) | **`INF_D_09.account_timeseries`** (INF-only artifact) |

### 2.5 AdvisorPublicProfile — `_shared/AdvisorPublicProfile.tsx`  (**49F + Inflection; COT disabled**)
| Component query | Platinum artifact | 49F | INF |
|---|---|---|---|
| `getPlatinumAdvisorDrilldownSummary(id)` | `advisor/{id}/platinum-summary` (Lambda; PII) ← `platinum/advisors/{id}/summary.json` | `D_04` | `INF_D_04` |
| `getAdvisorExecSummary(id)` | `platinum/advisors/{id}/exec_summary.json` | `D_04` (ADVI_49EXEC.006 batch) | INF batch |
| `getAdvisorNnaCanonical()` | `platinum/firm/advisor_nna_canonical.json` | `D_00f`→`D_04` | `INF_D_00f` |
| `getPlatinumAdvisorTimeseries(id)` | `platinum/advisors/{id}/timeseries.json` | `D_04` | `INF_D_04` |
| Role-Composition donut | (from advisor summary `role_breakdown`) | `D_02`→`D_04` (49F roles) | suppressed (`composition.enabled=false`) |

### 2.6 Cohort-A transparency — `_partners/49financial/index.tsx`  (**49F ONLY**)
| Component query | Platinum artifact | Producer |
|---|---|---|
| `getCohortASummary()` | `platinum/firm/cohort_a_summary.json` | `D_04` (ADVI_STAUDT). *(COT emits `gold/platinum/firm/cohort_a_summary.json` per cot-pipeline served list but the panel is not wired for COT.)* |

### 2.7 Inflection Insights panel — `_partners/inflection/InflectionInsightsPanel.tsx`  (**Inflection ONLY**, revenueOps=`inflection_insights`)
| Component query | Platinum artifact | Producer |
|---|---|---|
| `getInflectionActivityScan(window)` | `platinum/firm/activity_scan_{qtd,ytd,1y,max}.json` | **`INF_D_05.activity_scan`** |
| `getInflectionCashDrag(window)` | `platinum/firm/cash_drag_{qtd,ytd,1y,max}.json` | **`INF_D_06.cash_drag`** |
| `getInflectionFirmConcentrations()` | `platinum/firm/firm_concentrations.json` | **`INF_D_07a.firm_concentrations`** |
| FidelityCustodianBar overlay | (static layout config; no fetch) | n/a |

---

## 3. Per-partner producer summary (portal-load-bearing Group-D scripts)

**49F (`data/black_diamond/scripts/gold/`)** — load-bearing: `D_00`, `D_00b`, `D_00c`, `D_00f`, `D_01`, `D_02`, `D_03`, **`D_04` (sole platinum publisher)**. Every firm/advisor/client platinum key is republished by `D_04`; upstream `D_0x` write `gold/artifacts/*` intermediates.

**Inflection (`data/inf/scripts/gold/`)** — load-bearing (fan-out publishers): `INF_09.generate_partner_analytics`, `INF_D_00`, `INF_D_00b`, `INF_D_00c`(+GRO), `INF_D_00d`, `INF_D_00e`, `INF_D_00f`, `INF_D_02`, `INF_D_02b`, `INF_D_02c`, `INF_D_02d`, `INF_D_03`, `INF_D_04`, `INF_D_04b`, `INF_D_05`(+activity_scan, client_top_holdings), `INF_D_06`(+cash_drag, client_timeseries), `INF_D_07a`, `INF_D_08`, `INF_D_09`. **INF is the richest surface** (Insights panel + per-account timeseries + GRO are INF-unique).

**Cottonwood (`data/cot/scripts/gold/`)** — load-bearing for v1: `D_00`, `D_00b`, `D_01`, **`D_04` (sole platinum publisher)** — feeding **only** PartnerAnalytics (aua/nna/geo) + Distribution(geo). `D_00c`(leaderboard), `D_02`(advisor/client detail), `D_03`(composition) run but are **frontend-unconsumed for COT v1** (Advisors/Books tabs disabled) → **agnostic-drop candidates for the lean rebuild** until COT advisor dimension materializes (ADVI_PRTORG §5-A.1 REVISIT-LATER). COT has **no `D_00f.advisor_nna_canonical`**.

---

## 4. Convergence notes for 0.4.0_DS (portal-contract reconciliation)

The portal contract = exactly the platinum keys §2 lists, per partner. FE-down (this manifest) ⇄ DS gold-up (A1) + Schwab-raw-native D-tier field-requirements must reconcile:

1. **No panel needs a field no Group-D produces** — every §2 query resolves to a named producer EXCEPT the two flagged gaps (4a, 4b). Confirm those with DS.
2. **Group-D output with no panel consumer = agnostic-drop candidate** for the canonize-gold lean rebuild:
   - **COT:** `D_00c` leaderboard, `D_02` advisor/client detail, `D_03` composition — produced, not consumed (Books/Advisors off). Essential-vs-agnostic = AGNOSTIC for COT v1.
   - COT `gold/platinum/firm/cohort_a_summary.json` + `cash_coverage_summary.json` (D_04) — served, panel-unwired.
3. **GAP 4a (COT):** `getAdvisorNnaCanonical(cottonwood)` → no `D_00f` producer in COT tree → 404/empty. Intended (geo-only v1) or a needed emit? → **DS/CVO ruling.**
4. **GAP 4b (49F/COT header_fresh):** `header_metrics_fresh.json` is an INF-origin (`INF_D_00e`) pattern; confirm 49F/COT headline-tile fresh-AUA is intended-canonical-fallback vs a missing `D_00e`-equivalent emit. (Graceful-degrade present; not a render break.)
5. **Producer-name divergence is load-bearing for the rebuild:** 49F/COT funnel ALL platinum through `D_04`; INF fans across `INF_D_0x`. The canonize-gold rebuild's essential-script set differs in SHAPE per partner — a single `D_04` for BD-native vs ~20 publishers for INF.

---

## 5. Completeness attestation (AC4 — no silent Unknown)

Every visible ADVI panel enumerated (§2.1–2.7); every panel matched to its `_shared`/`_partner` component; every component query threaded to its platinum key + Group-D producer. **Two producer gaps explicitly flagged** (4a COT advisor_nna_canonical; 4b header_metrics_fresh on bd/cot) — flagged, not omitted. `demo` tenant noted out-of-scope. Per-partner enablement (§1) and producer divergence (§3) surfaced. Rail-grounded: `pipescript` (spine), `comp-platinum reverse` + `comp-pipescript io` (producers), `comp-transform schema-check` (PartnerAnalytics/DistributionTab — clean, no MISSING), endpoint source for FE bind.
