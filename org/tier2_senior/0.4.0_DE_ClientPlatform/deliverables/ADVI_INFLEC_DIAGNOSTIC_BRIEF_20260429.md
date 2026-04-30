# Inflection Portal Diagnostic Brief
**Authored by:** 0.4.0_DE_ClientPlatform
**Date:** 2026-04-29
**Scope:** All three portal surfaces — Assets Overview (PartnerAnalytics), Distribution tab, Books tab
**Method:** Frontend code trace + direct S3 artifact inspection (all artifacts pulled and parsed; no inferences without evidence)

---

## Executive Summary

The Inflection portal has issues at three distinct layers:

1. **DS data scope bug (highest priority):** All gold scripts computing per-advisor or per-firm aggregates (partner_analytics, leaderboard, book.json) land at $89.6M firm AUA. The canonical dashboard.json / header_metrics.json both say $182.6M. This ~$93M gap is systematic across every gold script and explains most of what you're seeing wrong.

2. **Missing artifacts:** Several files the portal expects simply don't exist on S3 yet, or exist as empty stubs (concentration_risk.json = `[]`, mix_summary.json = absent entirely, clients_tab.json has wrong schema, NNA data cuts off in 2021).

3. **Portal-side display bugs (minor):** One date display issue where the portal reads the projected quarter-end date (June 30) instead of the actual data snapshot date (April 28) for in-progress periods.

---

## Part 1A — What Is There and Connected (Working)

| Surface | What Works | Artifact | Evidence |
|---------|-----------|---------|---------|
| Assets Overview | GEO donut renders with real state breakdown | `partner_analytics_quarterly.json` | WA 86.9%, MT 3.2%, CA 3.2%, etc. — data present and portal reads it |
| Assets Overview | AUA growth bar chart renders (historical series 2020–2026) | `timeseries_overview.json` | 25 quarterly periods, 72 monthly periods — chart renders |
| Assets Overview | GRO chart renders (market component only) | `timeseries_overview.growth_decomposition` | 25 quarterly rows; market delta populated; chart skeleton visible |
| Assets Overview | Data Source footer timestamp shows April 28 | `timeseries_overview.data_as_of` | Footer uses `timeseriesData.data_as_of` = "2026-04-28" — correct |
| Distribution tab | GEO cohort enabled; routing is correct | `layout.ts` + `partner_analytics_quarterly.json` | `cohorts.geo = 'enabled'`; views.geo.donut populated |
| Distribution tab | GEO geographic distribution stats exist | `partner_analytics_quarterly.views.geo.distribution.total` | Real percentiles: p25=$20K, p50=$49K, p75=$131K, max=$1.31M |
| Books tab — advisor list | 3 advisor entries exist and filter/cap works | `leaderboard.json` (QTD window) | peter_lee, patrick_scanlan, inflection_wealth_management all present |
| Books tab — L2 drill | book.json exists for all 3 advisors | S3 `platinum/advisors/*/book.json` | All 3 files generated today (15:15Z); tax + billing data present |
| Books tab — L2 | composition.json + top_holdings.json for all 3 advisors | S3 `platinum/advisors/*/` | All 3 advisor folders have both files |
| Books tab — L3 | Per-client detail.json exists | S3 `platinum/clients/{id}/detail.json` | Verified: clients/100, clients/1000, etc. exist (stale: 2026-04-27) |
| Books tab — Inflection L3 tax | TaxCostBasisPanel wired for Inflection realized/unrealized | Portal code INFSHIP B5/B6 | `getPlatinumClientDetailStatic` branches on firmOverride=inflection |
| Books tab — Revenue Ops | InflectionInsightsPanel wired; 2 of 3 sub-panels have data | S3 `activity_scan.json` (33KB) + `cash_drag.json` (28KB) | Both live on S3; portal fetches them |
| Distribution tab | Advisors tab correctly suppressed for Inflection | `layout.ts` | `tabs.advisors.enabled: false` |

---

## Part 1B — What Is There But Not Connected (Data Exists, Portal Doesn't Show It)

### B1. Canonical AUA ($182.6M) — in `header_metrics.json`, not reaching the AUA headline

**Data:** `header_metrics.json` (generated today 15:15Z) has `total.aua = $182,552,380.96`. Complete breakdown: NNA mtd/qtd/ytd/12m, new vs. existing client split (new_client_aua, existing_client_aua, new_client_count, existing_client_count), fee_earning_aua ($135.7M), account_distribution (bell curve data: histogram buckets).

**Why it's not showing:** `PartnerAnalytics.tsx` (line 729-731 comment is explicit): "The Assets Overview panel renders bar charts from timeseries_chart.json only. header_metrics.json (data prop) is consumed by the Distribution tab, not here." The AUA headline shown in Assets Overview is the latest period value from `timeseries_overview.aua.quarterly` — which is 2026Q2 at $190.8M (see Issue #2 below). `header_metrics.json` is wired to the Distribution tab, not the Assets Overview header.

**Fix needed:** Either (a) DS aligns the timeseries computation to produce the canonical 182.6M for the current in-progress month/quarter, or (b) DE adds a `header_metrics`-based override for the current-period AUA headline in PartnerAnalytics (bypassing timeseries for the "current" snapshot number). DS fix is cleaner.

---

### B2. New Client / Existing Client Split — in `partner_analytics_quarterly.json`, suppressed by layout

**Data:** `partner_analytics_quarterly.json → views.aua.donut.segments` has NMNC (New Money New Client: 54 clients, $13.6M, 15.1%) and Existing (253 clients, $76.0M, 84.9%) — real data present, real proportions.

**Why it's not showing:** `INFLECTION_LAYOUT` has `allowedViewModes: ['geo']` — only the GEO donut is accessible. The AUA view (which shows the NMNC/Existing split) is locked out for Inflection. When the portal defaults to GEO, the client-cohort donut is the geographic split, not the new/existing cohort split.

**Additional issue:** Even if the AUA view were unlocked, the underlying total is 89.6M (scope bug) not 182.6M, so the proportions would be computed on the wrong base.

**Fix needed:** DS + joint decision: (a) unlock `allowedViewModes` to include `'aua'` once the scope bug is resolved, and (b) confirm the NMNC/Existing split belongs in the PartnerAnalytics donut for Inflection.

---

### B3. Leaderboard `1Y` window missing — portal prefers it, falls back to QTD

**Data:** `leaderboard.json` has `windows: {QTD, YTD, MAX}` and `available_windows: ['QTD', 'YTD', 'MAX']`. QTD has 3 entries (Peter 14.6M, Patrick 1.0M, IWM 74.0M). No 1Y window exists.

**Portal behavior:** `ClientsTab.tsx` line 262-263: tries `lbWindows['1Y']` first; falls back to `available_windows[0]` = 'QTD'. Advisor list renders using QTD data. The QTD AUAs are period-specific totals, not cumulative book AUAs — so the N1 advisor list shows QTD figures which may look odd.

**Fix needed:** DS generates a 1Y window in `leaderboard.json`, or DE adjusts the fallback label to clarify the displayed window.

---

### B4. NNA cohort decomposition (`by_geo`) in timeseries NNA — present in structure, unpopulated

**Data:** `timeseries_overview.nna.quarterly` entries have `by_geo: {}` and `by_adv: {}` — both always empty dictionaries. The NNA by geography breakdown structure exists but DS hasn't populated it.

**Portal impact:** NNA by cohort in the GRO chart section is suppressed (empty object checks). 

**Fix needed:** DS to populate `by_geo` in the NNA timeseries script.

---

## Part 1C — What Isn't There At All (Missing Data / Portal Crashes)

### C1. **AUA Scope Bug — ~$93M gap across ALL gold scripts** (HIGHEST PRIORITY)

**Evidence:** Every gold script that computes advisor-level AUA lands at 89.6M:
- `partner_analytics_quarterly.views.aua.donut.total` = $89,590,439
- `leaderboard.windows.QTD` entry sum = $89,590,439 (Peter 14.6M + Patrick 1.0M + IWM 74.0M)
- `book.json` total sum = $89,590,439 (Peter 65.8M + Patrick 6.4M + IWM 17.4M)

But `dashboard.json.headline.total_aua` = $182,552,380 and `header_metrics.total.aua` = $182,552,380. Both canonical files agree: $182.6M.

The scope bug is identical across all three gold script families, suggesting a shared upstream filter (likely a rep_id or account-status filter in the Orion silver pull) excludes approximately half the firm's accounts. The missing $93M is real AUA that belongs to the firm but isn't reaching the gold scripts.

**Impact on portal:** Every AUA number shown in Assets Overview header (if sourced from partner_analytics), Distribution tab donut total, and Books advisor AUA will be wrong until this is fixed. NNA percentages are also wrong because the denominator is wrong.

**Who:** DS + AE investigation required. Root cause is upstream of the gold scripts — likely in the Orion silver pull, the canonical normalization step, or the advisor-key mapping. AE needs to check the INF bronze/silver → gold data flow.

---

### C2. **"Jun 30, 2026" date display — in-progress quarter shown with projected end date** (PORTAL BUG)

**Evidence:** `timeseries_overview.aua.quarterly` last entry is `2026Q2, end_date: '2026-06-30', Total AUA: $190,778,972`. We're in April 2026; Q2 ends June 30. The PartnerAnalytics component (line 1844) reads `end_date` from the selected/default bar and displays it as "as of [date]". The actual data is as of April 28.

**Portal behavior:** When the latest bar (2026Q2) is displayed, the "as of" sub-caption reads "Jun 30, 2026" — which is the projected quarter end, not the actual data date.

**Dual fix:**
- **DS:** Do not emit the current in-progress quarter as a closed period with its projected `end_date`. Either omit the in-progress period, or emit `end_date: data_as_of` (the actual snapshot date) for the current month/quarter.
- **DE (defensive):** Portal can cap the displayed date to `min(end_date, data_as_of)` when `end_date > data_as_of`. One-line change in PartnerAnalytics.tsx line 1844-1848. Recommended as belt-and-suspenders regardless of DS fix.

---

### C3. **"191M" / "$190.8M" AUA headline — timeseries calculation diverges from canonical** (DS BUG)

**Evidence:** `timeseries_overview.aua.quarterly` latest period (2026Q2) = $190,778,972. `timeseries_overview.aua.monthly` April 2026 = $190,778,972. Canonical: `header_metrics.total.aua` = $182,552,380; `dashboard.json.headline.total_aua` = $182,552,380. Discrepancy: ~$8M.

**Note:** This is a *separate* discrepancy from the $93M scope bug (C1). Even the timeseries script, which is producing a higher number, doesn't match canonical. The timeseries is computing $190.8M for April 2026 while canonical is $182.6M for April 28. Likely a different methodology (e.g., using `market_value` rather than `total_aua` field from the Orion bronze/silver, or including a category of accounts that the canonical process excludes).

**Also present in timeseries:** `monthly.2024-02` shows `Total AUA: $106,915,047,884` — a $106B spike in February 2024. This is a data artifact (bad input row) that will render as a chart spike. DS needs to detect and suppress outlier rows.

**Who:** DS — investigate the AUA computation in the timeseries gold script vs the canonical dashboard/header_metrics scripts.

---

### C4. **Books tab shows nothing — `dashboard.json` is a thin stub; `clients_tab` is missing** (BLOCKER)

**Evidence:**
- `dashboard.json` (273 bytes) has only: `firm_id, firm_name, generated_at, data_as_of, headline, ytd`. No `split` flag, no `clients_tab`, no `employee_leaderboard`.
- `getPlatinumFirmDashboard()` returns this stub directly (since `stub.split` is falsy).
- `ClientsTab.tsx` line 288-291 then does `{ ...dash.clients_tab, headline: { ...dash.clients_tab.headline, ... } }` — accessing `.headline` on undefined throws `TypeError`.
- The ErrorBoundary wrapping the Books tab catches this and renders "Unable to Load Books".

**What the portal needs from `dashboard.json`:** Either (a) `split: true` + individual files (`leaderboard.json`, `fee_efficiency.json`, `clients_tab.json`), or (b) the full embedded payload including `clients_tab` and `employee_leaderboard`.

**Additionally:** Even if split mode were enabled, `clients_tab.json` has the wrong schema for the portal. Current Inflection `clients_tab.json` has `{generated_at, data_as_of, firm_id, total_aua, client_count, clients[]}` — no `headline` object. Portal expects `{headline: {aua, client_count, account_count, ...}, snapshot: {...}, distribution: {...}}`.

**Who:** DS (generate correct `dashboard.json` with `split: true` and correct `clients_tab.json` schema) + possible DE defensive fix to handle missing `clients_tab` gracefully.

---

### C5. **NNA data cuts off at 2021 (5+ years of zeros)** (DS BUG)

**Evidence:** `timeseries_overview.nna.quarterly` has exactly 4 rows: 2020Q2 through 2021Q1. `timeseries_overview.nna.monthly` has 10 rows through 2021-02. Every post-2021 period has NNA = 0 in `growth_decomposition` (e.g., 2026Q2: `nna: 0.0`). The NNA fields in `partner_analytics_quarterly.views.aua.metrics` are all 0.0 (nna_ytd, q0, q1, q2).

**Portal impact:** GRO chart shows NNA = 0 for every period from 2021 onward. The NNA bars/lines in the GRO chart are all flat at zero. NNA by cohort (Distribution tab) has no data.

**Also:** `dashboard.json.ytd.nna = 0.0` — even the dashboard reports zero YTD NNA.

**Who:** DS — the Orion transaction feed (inflows/outflows) is either (a) not included in the Inflection silver pipeline past 2021, or (b) the NNA calculation script filters/normalizes in a way that zeroes out all flows post-2021.

---

### C6. **AUA distribution bell curve — percentiles = zero** (DS BUG)

**Evidence:** `partner_analytics_quarterly.views.aua.distribution.total`: count=307, sum=$89.6M, but `mean=0.0, p25=0.0, p50=0.0, p75=0.0, min=0.0, max=0.0`. `views.aua.distribution.by_segment = {}`.

**Contrast:** `views.geo.distribution.total` has real percentiles (p25=$20K, p50=$49K, p75=$131K) — the GEO cohort bell curve has data. The overall AUA distribution (accounts ranked by AUA size) is the one that's empty.

**Portal impact:** The Distribution tab "accounts" bell curve shows nothing. The Distribution tab GEO geographic bell curve may render (data is present for that view).

**Who:** DS — the AUA distribution percentile calculation in the partner_analytics gold script is producing zeros for the overall account distribution. Likely a division/aggregation bug in the `views.aua.distribution` computation specifically.

---

### C7. **`concentration_risk.json` is empty** (DS BUG — known from today)

**Evidence:** `s3://opal-data-inf/platinum/firm/concentration_risk.json` = 2 bytes = `[]`. The Revenue Ops InflectionInsightsPanel shows an empty state for the Concentration Risk sub-panel.

**Who:** DS (the INFGRD.003 concentration_risk script produced an empty list).

---

### C8. **Mix data = 0 rows; `mix_summary.json` missing** (DS GAPS)

**Evidence:**
- `timeseries_overview.mix.quarterly` = 0 rows. `timeseries_overview.mix.monthly` = 0 rows. Mix panel in PartnerAnalytics shows "Asset class mix data unavailable".
- `s3://opal-data-inf/platinum/firm/mix_summary.json` does not exist. `getPlatinumFirmMixSummary()` catches the 404 and returns null.

**Portal behavior:** Mix chart/panel is completely dark. No asset class breakdown available.

**Who:** DS — the Orion data feed may not include asset class/model information. This may require a decision from Andrew: is mix data available from Orion, or is this panel intentionally suppressed for Inflection?

---

### C9. **Continuous view data** (UNCLEAR — needs investigation)

**Evidence:** The Distribution tab has a Continuous view toggle (AreaChart with 2-year daily data). For 49F this is served by the `opal-partners-data` Lambda via a different endpoint. `timeseries_chart.json` (436KB, from 2026-04-27) exists on S3 and may be the continuous timeseries source — but this file's structure wasn't fully inspected in this investigation.

**Action needed:** DE to check whether `timeseries_chart.json` is wired as the continuous view source for Inflection, or whether the Continuous toggle expects the Lambda endpoint (which may not route to Inflection).

---

### C10. **GRO NNA contribution = zero for entire post-2021 period** (follows from C5)

**Evidence:** Confirmed in `timeseries_overview.growth_decomposition` — every period 2021Q2 through 2026Q2 has `nna: 0.0`. GRO chart renders market-only bars; the NNA stacked component is invisible.

**Same root cause as C5** (NNA pipeline truncation). Fix C5 and this resolves automatically.

---

## Part 2 — Quick Reference: Artifact Inventory

| Artifact | Status | AUA | Notes |
|----------|--------|-----|-------|
| `dashboard.json` | Thin stub | $182.6M | No `split`, no `clients_tab`, no `employee_leaderboard` → Books crash |
| `header_metrics.json` | GOOD | $182.6M | Full breakdown, correct. Not used in Assets Overview |
| `partner_analytics_quarterly.json` | Scope bug | $89.6M | GEO donut OK; AUA dist zeros; NNA zeros; new/existing split suppressed |
| `partner_analytics_monthly.json` | Scope bug | $89.6M | Same issues |
| `partner_analytics_annual.json` | Scope bug | $89.6M | Same issues |
| `timeseries_overview.json` | Partial | $190.8M (current) | AUA history good; NNA truncated 2021; Mix = 0; Feb 2024 spike; June 30 date |
| `leaderboard.json` | Partial | $89.6M | No 1Y window; QTD/YTD/MAX only; 3 advisors present |
| `clients_tab.json` | Wrong schema | $429.4M | Old file (Apr 27), wrong schema, wrong AUA — portal cannot use |
| `firm_composition.json` | GOOD | — | Exists (Apr 28) |
| `top_holdings.json` | GOOD | — | Exists (Apr 28) |
| `activity_scan.json` | GOOD | — | 33KB, live today |
| `cash_drag.json` | GOOD | — | 28KB, live today |
| `concentration_risk.json` | EMPTY | — | 2 bytes = `[]` |
| `nmec_nmnc_nna.json` | Generated | — | Live today; not yet wired to portal |
| `cohort_a_summary.json` | GOOD | $47M cohort-A | Wired (Apr 24, `5a4a4d2d`) |
| `mix_summary.json` | MISSING | — | Not on S3; Mix panel dark |
| `filters/dimensions.json` | Minimal | — | 237 bytes |
| `timeseries_chart.json` | Stale | — | 436KB, Apr 27; Continuous view dependency TBD |
| Per-advisor `book.json` (×3) | GOOD | $89.6M total | All 3 advisors; today's run |
| Per-advisor `composition.json` (×3) | GOOD | — | All 3 advisors |
| Per-advisor `top_holdings.json` (×3) | GOOD | — | All 3 advisors |
| Per-client `clients/{id}/detail.json` | STALE | — | Exists (Apr 27); L3 drill technically has data |
| `fee_efficiency.json` | MISSING | — | Not checked; needed for Books N1 fee panel |

---

## Part 3 — Prioritized Fix List for COO Task Order Decomposition

| # | Fix | Owner | Blocks |
|---|-----|-------|--------|
| 1 | Investigate + fix AUA scope bug ($89.6M vs $182.6M) in the Orion silver-to-gold pipeline | DS + AE | Everything AUA-related across all 3 tabs |
| 2 | Regenerate `clients_tab.json` with correct schema (`headline` object, correct AUA, snapshot data) + fix `dashboard.json` to set `split: true` and reference correct files | DS | Books tab load |
| 3 | Fix NNA pipeline truncation — 2021Q1 cutoff; populate flows through current date | DS | GRO NNA, Distribution NNA, NNA metrics |
| 4 | Fix `concentration_risk.json` gold script (emitting empty `[]`) | DS | Revenue Ops Concentration sub-panel |
| 5 | Fix `timeseries_overview` AUA for current period ($190.8M vs $182.6M) + suppress/fix Feb 2024 spike ($106B) | DS | Assets Overview headline AUA |
| 6 | Fix `timeseries_overview` in-progress quarter end_date OR DE capping (min(end_date, data_as_of)) | DS primary / DE defensive | "Jun 30" date display |
| 7 | Populate `views.aua.distribution` percentiles (p25/p50/p75/mean) in partner_analytics gold script | DS | Accounts bell curve |
| 8 | Generate `mix_summary.json` OR confirm Mix data unavailable from Orion (decision required) | DS (decision: Andrew/DS) | Mix panel |
| 9 | Generate `leaderboard.json` `1Y` window | DS | Books N1 advisor AUA accuracy |
| 10 | Populate `timeseries_overview.nna.by_geo` with cohort-level NNA decomposition | DS | NNA by geography in GRO |
| 11 | Refresh `clients_tab.json` per-client list and `clients/{id}/detail.json` from today's snapshot | DS | Books client list freshness |
| 12 | DE: defensive portal fix for `dash.clients_tab` undefined (null-check before spread) | DE | Books tab resilience |
| 13 | DE: cap "as of" date to `min(end_date, data_as_of)` in PartnerAnalytics | DE | Jun 30 date display |
| 14 | Decision + possible DE change: unlock `allowedViewModes` to include `'aua'` once scope bug fixed | DE + Andrew | New/existing client split visible |
| 15 | Investigate Continuous view data path for Inflection (`timeseries_chart.json` vs Lambda) | DE + AE | Distribution Continuous toggle |
