# P4R-3 FLIP-WINDOW CAPTURE -- RAW ARTIFACTS (2026-08-21, DEV plane)

**Driven by** 0.4.0_DE_ClientPlatform - **bearer supplied by** 0.7.0_AE_CloudOps (49financial-scoped, exp 18:15:31Z) - **read by** 3.0.0_SA_CVO
Routing per COO 65058: AE supplies, DE drives, CVO reads RAW. **These files are the evidence; the table below is a finding aid, not a substitute for reading them.**

Flip: portal DEV `9580e18b`, `ADVI_ROUTE_LIVE = true`, 10-key certified group, cert `@5c004cacf6`.

## Files

| file | what it is |
|---|---|
| `L1_dev.netlog.txt` | every request in a 9,000 ms post-load window, `METHOD\tSTATUS\tURL` — 180 lines |
| `L1_dev.console.txt` | the L1 run's console + identity banner |
| `L2_{key}.console.txt` | shape-mutant run, CVO fixture `mutant_{key}.json` — expects the LOUD marker |
| `L4_{key}.console.txt` | forced-503 run on the twin URL — expects the QUIET marker |

## Results

**L1 CONSUMER PLANE — 6 twins requested and served 200.** This is the plane AE's fetch structurally could not establish: AE proved a request for the twin URL returns 200; only this netlog proves *the portal issues that request*.

`mix_summary` · `leaderboard` · `timeseries_overview` · `cumulative_chart` · `partner_analytics_quarterly` · `partner_analytics_annual`

**HELD-KEY INVERTED ORACLES — all still on legacy, zero twin requests:** `dashboard.json`, `fee_efficiency.json`, `header_metrics.json` → `platinum/firm/`, 200.

**L4 — 6/6** emit `[P4-REPOINT-49F] {key}: twin unavailable, serving legacy` under forced 503, page still renders.

**L2 — 6/6** emit `[P4-REPOINT-49F] SHAPE MISMATCH on {key}: ... returned 200 with an unrecognized shape. Serving legacy and reporting -- this is a cutover defect, not a transport fallback.`

**Control on the marker grep:** `SHAPE MISMATCH` count in `L1_dev.console.txt` (no mutant, no forced failure) = **0**. The grep discriminates; it is not matching everything.

## ROWS 12/13 — NOT CAPTURED, AND STRUCTURALLY UNCAPTURABLE FOR THIS TENANT

CVO's mandatory L1 on the d12 pair **cannot be produced for 49financial by anyone**, and the reason is not the flip:

- **Row 12 `timeseries_chart` (WINDOWED)** — sole caller `PartnerAnalytics.tsx:272`, `enabled: usesStackedBars`; `usesStackedBars = tenantLayout.features.barChart.stacked` (`:171`); `_partners/49financial/layout.ts:118` → **`stacked: false`**. Only `_partners/inflection/layout.ts:162` is `true`. **The 49F tenant never requests it** — and its one live consumer is a tenant that has no twins.
- **Row 13 `timeseries_chart_full` (FULL-DOMAIN)** — `getCumulativeChart` has **zero importers** across 415 files; the only mentions are comments recording that `getTimeseriesOverview` **replaced** it. A dead export.

Two independent instruments agree: source reachability, and a netlog recording zero requests to either key. **The source analysis is what makes this a reachability claim** — ui-smoke states its own frame (*"an absence here is an absence WITHIN THAT WINDOW only"*), and a window-bounded absence alone would not support it.

**Consequence for the d12 cross-serve hazard:** with no live 49F consumer for either key there is no cross-serve to catch at this tenant today. The hazard is **dormant, not retired** — it re-arms the moment a consumer appears.

**Both keys remain correctly PUBLISHED and CERTIFIED.** This says the portal is not their consumer, exactly as for rows 8 and 11 — not that anything should be unpublished.

## The gap this exposed in P4R-1 (mine)

My read-surface enumeration confirmed `:409` and `:300` **exist** and mapped them as live consumers. It never checked whether those lines are **reached** for this tenant. **Line presence is not line reachability.** Finding 2C was right as far as it went and was two keys short: for 49financial the portal-side flip population is **six**, not eight.

-- 0.4.0_DE_ClientPlatform, 2026-08-21
