# P1 — THE MDPF CONSUMPTION MAP (the program denominator)

**What this is:** the complete, grounded enumeration of what the `/portfolios` Model Portfolios page
READS — bucket + full key, per key the fields *actually consumed*, the serving path, and the
refresh picture. It is the **write denominator** for CTO's one-process-writes-both cross-bucket
Lambda (P2/P4): *a key missing from a generator's write set is a panel that breaks on cutover.*

- **Requested by:** CTO DISPATCH 20260723T161738Z (Andrew-direct program expansion) — parked
  post-serve by COO 165038Z, bounded subset run 192559Z, **now the full deliverable** (COO 224230Z
  "back to the parked read-surface enumeration (P1)").
- **Author:** 0.4.0_DE_ClientPlatform · **audited** 2026-07-24 ~09:30–10:10Z
- **Vintage (every FE citation resolves here):** portal PROD `17256834` (tag `portal-v2.1.148`,
  explicit-SHA pin `343e7b2a`). DEV HEAD is `8602d0f7`; **the two DEV-only commits touch
  `scripts/ui-smoke.mjs` ONLY** (verified `git show --stat`), so the DEV and PROD read surfaces are
  byte-identical and this map is one vintage, not two.
- **Live-state citations:** `s3api list-objects-v2` / `head-object` on `opal-data-portal-v2`,
  `cloudfront get-distribution-config EVTSA9VEHNZVH`, `lambda get-function-configuration
  opal-assets-mdpf-portal-publisher` — all read 2026-07-24 ~09:40–10:00Z.

---

## 0. DENOMINATOR (state it first — a locus table without one cannot be assessed)

| Axis | Denominator | Method |
|---|---|---|
| Fetch surface | **10 of 10** `useQuery` hooks on the page | full-file walk of `ModelPortfolios.tsx` (2,707 lines at this vintage) + grep `useQuery\|queryKey\|queryFn`; **subtree components fetch NOTHING** (verified: zero `useQuery`/`apiRequest`/`fetch(` in `ModelPortfolios/`, `AccountDistributionChart`, `AccountDistributionMetrics`, `BenchmarkHeatmap`, `lib/pairedProvenanceRead.ts`) |
| Distinct served keys | **17 concrete keys** (10 hooks × firm parameterisation) | endpoint getters in `api/endpoints/aum.ts` + `api/portal-proxy.ts` |
| Keys in the MDPF generator's scope | **13** (see §1) | 4 non-MDPF (Yang benchmarks/peers) excluded, named explicitly |
| Live existence check | **12 of 12 in-scope keys downloaded and field-checked**; 1 in-scope key **ABSENT by design** (`json/mdpf/global/aum-metrics.json`) | `s3api get-object` per key |

**⚠ The 07-22 audit (`MDPF_3F_P1_CONSUMPTION_CONTRACT_AUDIT_20260722.md`) is SUPERSEDED as a key
list.** Since its vintage (`08c6d8b2`) the page gained **+597 lines**, a new 332-line read module
(`pairedProvenanceRead.ts`), **a 10th hook and a new key family** (`json/mdpf/{firm}/aum-metrics.json`).
Its Part-3 P5 flag list remains valid; its Part-1 inventory does not. Re-walking, not re-reading,
is what found the new key.

---

## 1. THE WRITE DENOMINATOR — every consumed object as bucket + full key

**Bucket for every row: `s3://opal-data-portal-v2`** (APPLIED-grounded, §2). Rows are the complete
set; nothing on this page reads any other bucket.

### 1a. MDPF-scoped — the generator's write set (13 keys)

| # | Full key | Read by (hook → getter) | Fires when | Live state (2026-07-24) |
|---|---|---|---|---|
| K1 | `json/mdpf/global/aggregate-aua-timeseries.json` | `['mdpf-aggregate-timeseries','global']` → `getMdpfAggregateAUATimeSeriesByFirm('global')` | `effectiveFirmId === 'global'` | 254,419B · 07-23T21:18:53Z · ETag `55a8b379` |
| K2 | `json/mdpf/49financial/aggregate-aua-timeseries.json` | `['mdpf-per-firm-timeseries', firmId]` → same getter | `firmId !== 'global'` | 183,004B · 07-23T21:47:06Z |
| K3 | `json/mdpf/inflection/aggregate-aua-timeseries.json` | ” | ” | 146,290B · 07-23T21:47:06Z |
| K4 | `json/mdpf/cottonwood/aggregate-aua-timeseries.json` | ” | ” | 87,262B · 07-23T21:47:07Z |
| K5 | `json/mdpf/49financial/account-distribution.json` | `['mdpf-per-firm-distribution', firmId]` → `getAccountDistributionByFirm` | `firmId !== 'global'` | 5,397B · **07-24T11:30:39Z** |
| K6 | `json/mdpf/inflection/account-distribution.json` | ” | ” | 6,878B · **07-24T11:30:39Z** |
| K7 | `json/mdpf/cottonwood/account-distribution.json` | ” | ” | 6,375B · 07-23T04:04:42Z |
| K8 | `json/mdpf/cottonwood/aum-metrics.json` | `['mdpf-per-firm-aum-metrics', firmId]` → `getAUMMetricsByFirm` | **`firmId === 'cottonwood'` ONLY** (`:528`) | 2,862B · 07-23T04:04:42Z |
| K9 | `json/mdpf/49financial/aum-metrics.json` | *(same hook, gated off today)* | **would fire on 3F-P3 widening** | **ABSENT** — see F-2 |
| K10 | `json/mdpf/inflection/aum-metrics.json` | ” | ” | **ABSENT** — see F-2 |
| K11 | `json/portfolios/aum-metrics.json` | `['aum-metrics']` → `getAUMMetrics` → `portalProxy.getAUMMetricsWithCalculations` | **ALWAYS** (no `enabled` guard — fetched on per-firm views too) | 7,234B · 07-23T20:57:17Z |
| K12 | `json/portfolios/aum-timeseries.json` | `['aum-timeseries']` → `getAUMTimeSeries` | **ALWAYS** | 289,962B · 07-23T21:26:39Z |
| K13 | `json/portfolios/account-distribution.json` | `['account-distribution']` → `getAccountDistribution` | **ALWAYS** | 7,656B · 07-23T20:57:18Z |
| K14 | `json/portfolios/non_model_assets.json` | `['non-model-assets']` → `getNonModelAssets` | **ALWAYS** | 82,101B · 07-23T19:34:57Z |

> **K11–K14 are the trap.** They sit under `portfolios/`, not `mdpf/`, they carry **no firm segment**,
> and they have **no `enabled` guard** — they are fetched on *every* view including per-firm. A
> generator scoped by the `mdpf/` prefix silently drops four keys that the Global radial, the bell
> curve, the Non-Model band and every Q-end priorLevel depend on.

### 1b. Out of MDPF scope — named so the omission is deliberate, not an oversight

| Key | Read by | Producer | Why out |
|---|---|---|---|
| `json/benchmarks/model_portfolio_benchmarks.json` | `['model-portfolio-benchmarks']`, `enabled: activeTab==='performance'` | `yang-model-portfolio-benchmarks` lambda | Yang pipeline, no AUA composition |
| `json/benchmarks/etf_returns.json` | `['etf-benchmark-returns']`, same gate | `yang-generate-etf-returns` lambda | ” |
| `json/peers/peer_performance.json` | `['peer-performance']`, `enabled: activeTab==='peers'` | `yang-generate-peer-performance` lambda | ” |

### 1c. BLAST RADIUS — keys this page shares with other pages

**The MDPF keys (K1–K10) are exclusive to this page. K11 is not.**

| Key | Other consumers |
|---|---|
| `json/portfolios/aum-metrics.json` | `FactorTilts.tsx:83` (`getAUMMetrics`) · `Attribution/tabs/SelectionTab.tsx:89` and `Positioning/tabs/HoldingsTab.tsx:564` (both via `getAUMSummary` → `portal-proxy.ts:264`, the **same URL**) |
| K12 / K13 / K14 | no other call sites found (portal-wide grep over `.ts`/`.tsx`) |

**Regenerating K11 touches four surfaces, not one.** That belongs in the gate's blast-radius line.

---

## 2. THE SERVING PATH — APPLIED, not inferred

**DESIRED (comp-routes, its own header: "never a live describe-distribution"):** behavior
`/api/general/*` → origin `S3-opal-data-portal-v2-json`, edge `public-data-router` rewrites
`/api/general/` → `json/`. Uniform across all five endpoints traced.

**APPLIED (live `get-distribution-config EVTSA9VEHNZVH`, read 2026-07-24):** 24 ordered cache
behaviors enumerated in full. **There is NO `/api/general/mdpf/*` behavior on the live
distribution.** The most specific pattern matching any MDPF URL is `/api/general/*` →
`S3-opal-data-portal-v2-json` (`opal-data-portal-v2.s3.us-east-1.amazonaws.com`), edges
`auth-validator-edge` (viewer-request) / `public-data-router` (origin-request) /
`cache-control-injector` (origin-response). **The Option-C `mdpf_assets_behavior_paths` set is NOT
applied** — consistent with the S5 flip rollback (LD-0330).

**Therefore, today, every MDPF read serves from `opal-data-portal-v2`.** The
`opal-assets-mdpf-portal-publisher` writes the *same logical key names* to a **different bucket**:
live `Environment.Variables.ASSETS_BUCKET = "opal-data-assets"`, `LastModified
2026-07-23T19:28:42Z`, `CodeSha256 ZEqfKEq01ryL...`. Its 11-entry `PUBLISH_MAP` is build-alongside
and **read by nothing** until a CF flip re-points the behaviors. This corroborates 0.7.0's
deployed-artifact refutation and COO's 200556Z ownership, independently and at the CloudFront layer
rather than the Lambda layer.

**Exercise attempted and reported as inconclusive:** an unauthenticated `curl` of
`https://opalinvest.dev/api/general/mdpf/global/aggregate-aua-timeseries.json` returns **401**, and
so does a **deliberately non-existent key** — `auth-validator-edge` fires before routing, so the
response cannot discriminate a real key from a fake one. **The negative control passed, which means
the probe is uninformative, not that the key is absent.** The exercised binding on record is last
night's live-PROD DOM render (`8c751da0c` / `e6115fa66`), where the page displayed Total AUA $1.95B
— the value carried by K1 and no other key.

**Applied WRITE attribution is NOT established by this audit.** No object carries producer metadata
(`head-object` → `Metadata {}` on all four sampled keys), and source names ≥3 candidate writers per
key family (`build_aggregate_aua_timeseries.py` `JSON_PARTNER_PREFIX`; SmartX
`compute_per_firm_account_distribution.py:277`, which exists in **three** copies — `data/smartx/`,
`infra/aws/ec2/smartx-exporter/smartx-workspace/`, `infra/aws/lambda/smartx_ingestion_pipeline/`;
`build_legacy_compat_emit.py` `LEGACY_AUM_KEY/LEGACY_NM_KEY`; the `dim_mdpf_*` revamp gold scripts).
**Which process wrote a given object last night is UNDETERMINED here** — it needs CloudTrail or
runner logs. *That ambiguity is itself an argument for the one-process-writes-both design; it is not
a substitute for the answer.*

---

## 3. THE FIELD CONTRACT — fields actually consumed, verified present/absent in the live artifact

### 3a. `aggregate-aua-timeseries.json` (K1–K4) — the paired-provenance contract

Consumption is funnelled through `lib/pairedProvenanceRead.ts` (guard-enforced: direct reads of
`model_value` / `partner_custody_total` / `non_model_aua` outside that module fail
`scripts/provenance-read-guard.mjs`). Legend: ✔ present · ✖ absent · — not applicable.

| Field | Consumed by | global | 49F | INF | COT |
|---|---|---|---|---|---|
| `dates[]` | every reader (the axis) | ✔ 447 | ✔ 429 | ✔ 429 | ✔ 447 |
| `by_model{}.model_value[]` | `readModelSeries` `:186` | ✔ 9 models | ✔ 7 | ✔ 7 | ✔ 5 |
| `by_model{}.account_count[]` | `readModelSeries` `:187` | ✔ | ✔ | ✔ | ✔ |
| `by_model{}.display_name` | canonical-name join `:763` | ✔ | ✔ | ✔ | ✔ |
| `by_model{}.cohort_class` | SMA fold `:760`, `:798` | ✔ | ✔ | ✔ | ✔ |
| `partner_custody_total[]` | `readFirmAggregateSeries` `:217` | **✖** | ✔ 429/429 | ✔ 429/429 | ✔ 56/447 |
| `non_model_aua[]` | `readNonModelSeries` `:233` | ✔ 423/447 | ✔ 429/429 | ✔ 423/429 | ✔ 47/447 |
| `opal_aggregate_aua[]` | Global deep-tail band `:1333` | ✔ 423/447 | **✖** | **✖** | **✖** |
| `model_aua[]` | Global deep-tail band `:1334` | ✔ 423/447 | ✔ | ✔ | ✔ |
| `account_count_total[]` | `readCountTotalSeries` `:282` (W-7) | ✔ 407/447 | ✔ 408/429 | ✔ 423/429 | ✔ **2/447** |
| `count_provenance[]` | `readCountTotalSeries` `:275` | ✔ | ✔ | ✔ | ✔ |
| `point_class[]` | `readGlobalPointClass` `:251` — **Global only by contract** | ✔ | ✖ *(by design)* | ✖ | ✖ |
| `cohort_provenance[]` | `provenanceIndex` `:108` | ✔ (per-firm-keyed) | ✔ **pre-contract shape** | ✔ **pre-contract shape** | ✔ (contract shape) |
| `as_of_last` | spine stamp `:621` | ✔ `2026-07-22` | ✔ `2026-07-22` | ✔ `2026-07-22` | ✔ `2026-07-22` |
| `meta.honest_none.total_none_dates` | Global gap suppression `:1324` | ✔ | — | — | — |
| `meta.count_coverage_end` | count-mode footer `:2245` | ✔ `2026-07-18` | ✔ `2026-07-18` | **✖** | **✖** |
| `meta.interpolation.affected_period` | band cross-check (never the source) | ✖ | ✖ | ✖ | ✔ |
| `backfill_method` | typed, not rendered at this vintage | ✖ | ✖ | ✖ | ✔ |

**Emitted but NOT consumed** (top-level): `firm_id`, `partner_name`, `as_of_first`, `n_dates`,
`source_vintage_last`, and — Global only — `inflection_non_model_aua`.

### 3b. `aum-metrics.json` per-firm (K8) — `MdpfFirmAUMMetrics`, `aum.ts:641-657`

Consumed: `total.{aum, model_aum, non_model_aum, account_count, series_start, q0..q3}` (5 read
sites), `by_model[]` (`.map`), `dates.{q0..q3}`. Live cottonwood artifact carries every one
(`total.aum 458114003.1`, `account_count 294`, `series_start "2026-07-21"`, `q0..q3` present with
`change/growth/priorLevel` all `null` — correct for a firm whose series starts 3 days ago).

### 3c. `account-distribution.json` (K5–K7, K13)

Consumed by `AccountDistributionMetrics.tsx` / `AccountDistributionChart.tsx` **as props** (they
fetch nothing): `total.account_count`, `total.median`, `total.percentiles.p*` (8 read sites),
`histogram.bin_labels[]`, `histogram.counts[]`; plus `by_model[<canonical>]` for the donut-selected
view and `?.total?.account_count` on the page (`:2240`). All present in all four live artifacts.
**`by_model` keys differ across artifacts** — `"Ultra-Short Term"` (49F) vs `"Ultra Short-Term"`
(global/portfolios) vs `"Short Term"` (COT) — reconciled client-side by
`getCanonicalModelName` (`lib/modelPortfolioColors.ts`). A generator must preserve, not normalise,
these keys unless the crosswalk moves with it.

### 3d. Legacy `portfolios/` trio (K11, K12, K14)

| Key | Consumed fields | Live shape |
|---|---|---|
| K11 `aum-metrics.json` | `total.{q0,q1,q2}` (`.change/.growth/.priorLevel`), `total.account_count`, `by_model[]` (`.find`), `dates.{q0..q3}`, `last_updated` | ✔ all present; `period 2026-07-22`, `last_updated 2026-07-23T20:55:19Z` |
| K12 `aum-timeseries.json` | `aggregate[].{period, aum}` (Q-end priorLevels `:1616-1618`, graceful-degrade trend source), `by_model{}` | ✔ `aggregate` n=447, last `{period 2026-07-22, aum 1637144180.01, account_count 7830}`; `by_model` 5 keys |
| K14 `non_model_assets.json` | `latest.non_model_aum` (`:978`), `time_series[].{period, non_model_aum}` (roll-forward `getNonModelAumForDate` `:344-362`) | ✔ present; **`latest.date 2026-07-20`** vs `as_of_last 2026-07-22` on K1–K4 — a 2-day axis offset between the two families, **inside** the page's own `spineIsStale` >3-day divergence guard (`:1013-1018`), so it renders no notice today. **Recorded as a cadence observation, not a staleness finding** — no trading-calendar verdict is asserted here. |

---

## 4. PERIOD-END AND SELECTOR FEATURES — per feature, own key vs client-derived

CTO asked this explicitly ("these may derive client-side from the timeseries or read their own keys
— SAY WHICH, per feature, from the code").

| Feature | Own key? | Read path |
|---|---|---|
| **Monthly / Quarterly period selector** | **NO — pure UI state** | `periodView` `useState<'monthly'\|'quarterly'>` `:539`; no fetch, no `enabled` coupling |
| **Period-end bar selection** | **NO — 100% client-derived** | `filterToEndOfPeriod` `:1998-2046`: groups the daily series by `YYYY-MM` / `YYYY-Q`, then picks **the last date in each group with a REAL value for the ACTIVE metric** (`:2034-2041` — value → `p.aum != null`; count → any active model's `account_count != null`). Not exact-calendar-end, not `latest<=target`. **No synthesis: data stays None, this is render-aggregation only.** |
| **Value / Count trend toggle** | **NO — UI state**, but it **re-keys the anchor** | `trendMetricType` `:540`; drives which anchor field the tooltip reads (below) |
| **Tooltip "Total"** (the Andrew-flagged defect) | **NO — rides a synthetic row field** | `anchoredTotal = rowPayload['total_aua']` `:1151`, set at `:2067-2070` and `:2288`: **per-firm → `aggregateItem.aum` (= served `partner_custody_total`); Global → `null`, so the tooltip falls back to the bucket sum.** That per-firm-only scoping IS the v2.1.148 P1 fix — Global's aggregate is model-only, so anchoring it there dropped ~$420M of non-model. |
| **Tooltip "Total Holdings"** (count mode) | **NO — synthetic row field** | `anchoredCount = rowPayload['count_total']` `:1154`, set `:2072-2075` from `readCountTotalSeries` → **served `account_count_total[]`**, the producer count. Never a client re-sum (guard-enforced; a client sum dips to 0 on count-exempt dates where the producer honestly bridges). |
| **Q0–Q2 quarterly growth tiles** | **PARTIAL — served key + FE override** | `change`/`growth` SERVED from K11 `total.qN`; **`priorLevel` FE-OVERRIDDEN** at `:1616-1618` via `trendEnterpriseAt` = `getTrendAumForDate(K12.aggregate, Q)` + `getNonModelAumForDate(K14.time_series, Q)` — an FE-composed enterprise level per quarter |
| **Rolling window** | **NO — client-derived** | per-firm = rolling 1 year from the latest date; Global = since-inception. This is the boundary Andrew read as a data floor on Inflection (07-22 addendum finding: data extends 8.5 months further back than the rendered window) |
| **MTD / YTD selectors** | **DO NOT EXIST** on this page | grep of the period machinery returns only `monthly`/`quarterly` + `q0..q3`. Reported as absent rather than silently omitted. |

**Net: no period-end feature reads a key of its own.** Every one derives from K1–K4 / K11 / K12 /
K14. A generator that changes the daily grain changes every period-end number on the page.

---

## 5. FINDINGS

**F-1 — SCHEMA ASYMMETRY between the Global slice and the per-firm slices, and it has already shipped
one client-visible defect.** Global carries `opal_aggregate_aua` + `model_aua` and **no**
`partner_custody_total`; per-firm carries `partner_custody_total` + `model_aua` and **no**
`opal_aggregate_aua`. The two families name their total differently. v2.1.147 anchored the tooltip
Total on `partner_custody_total` — correct per-firm, **absent at Global** — so the live Global
tooltip read ~$1.53B beside rows composing ~$1.95B until `343e7b2a` scoped the anchor per-firm-only.
**This is the single highest-value thing for the generator to fix or to make explicit.** A shared
component over two slices that disagree on the name of "the total" will keep producing this defect.

**F-2 — `aum-metrics.json` exists for cottonwood ONLY; the hook is gated to match.** K8 present;
K9/K10 (49F/INF) and a global equivalent are **ABSENT from S3**, and `:528` gates the hook to
`effectiveFirmId === 'cottonwood'`. **The gate and the data agree today** — this is not a live
defect. But 3F-P3 widens that predicate, and **widening it before DS produces K9/K10 renders an
empty panel for 49F/INF** (the wrapper returns `null` on a miss, so it degrades rather than throws).
The generator's write set must land K9/K10 **before or with** the predicate change.

**F-3 — `cohort_provenance` on 49F and INF is the PRE-CONTRACT date-less schema, so both firms have
NO working provenance channel today.** Live entries read `{"model":"SmartX","custody":"Schwab"}`
(49F) and `{"model":"Eclipse","custody":"Orion"}` (INF) — **source names, not `PointClass` enums,
and no `date` key**. `provenanceIndex` `:118` rejects any date-less entry and degrades the **whole**
channel to predates-contract → every point reads `measured` → **no interpolation band can ever
render for 49F or INF**. Cottonwood carries the contract shape
(`{date, custody, model, non_model}`); Global carries the per-firm-keyed shape
(`{date, 49financial, inflection, cottonwood}`) and correctly supplies `point_class[]` alongside.
**The FE handles this safely and loudly (console warn) — it is a PRODUCER gap, not an FE defect**,
and it is invisible on screen precisely because the fail-safe is well-built.

**F-4 — Cottonwood emits a `non_model` provenance slot that no reader consumes.** `readNonModelSeries`
`:230` rides the **`custody`** slot by design (module docstring). The producer emitting a distinct
`non_model` slot means producer and consumer disagree about which channel labels the non-model band.
Harmless today (custody is present); **a divergent-intent flag for the generator contract**, not a
live defect.

**F-5 — Two orphan keys: published, byte-identical to a live key, read by nothing.**
(a) `json/mdpf/aggregate-aua-timeseries.json` (no firm segment, 254,419B, ETag `55a8b379`) is
**byte-identical to K1** and its only accessor, `getMdpfAggregateAUATimeSeries` (`portal-proxy.ts:492`),
has **zero call sites** portal-wide. (b) `json/mdpf/global/account-distribution.json` (7,656B, ETag
`14d668ef`) is **byte-identical to K13** and is not read — the Global view calls
`getAccountDistribution()` → `portfolios/account-distribution.json`. Both are duplicate writes.
`aum.ts:444`'s stale comment on the (a) function is the same comment that misled the 07-23
platinum-overwrite dispatch. **Recommendation: the generator writes ONE of each pair and the other
is retired — but the retirement is a CTO call, since an unread key is cheap and a wrong deletion is not.**

**F-6 — `meta.count_coverage_end` is present on global + 49F, absent on INF + COT.** Read at `:2245`
through an optional-chained cast, so absence degrades silently rather than throwing. Per-firm
inconsistency in a field the count-mode footer renders — the generator should emit it uniformly or
the FE should state the absent case.

**F-7 — INSTRUMENT: `comp-platinum page ModelPortfolios` composes the WRONG BUCKET for the
`/api/general/*` behavior.** It reports `cloudfront: /api/general/* -> S3-opal-data-bd (firm-routed
via X-Firm-Id)` for `json/portfolios/account-distribution.json`. **The live distribution binds that
behavior to `S3-opal-data-portal-v2-json`.** The tool's `--firm` default (`FIRM: bd -> bucket
opal-data-bd`) is being applied to a behavior that is not firm-routed. Verified with a control:
`list-objects-v2 --bucket opal-data-bd --prefix json/portfolios/` returns **empty Contents**, while
the identical call against `opal-data-portal-v2` returns the key. *(First attempt used
`--query KeyCount`, which returned `None` for BOTH buckets — the positive control failed, so the
instrument was rebuilt on `Contents[]` before any verdict was recorded. A bare `None` on the target
would have read as proof of absence.)* **Coverage: 2 of 10 fetches traced.** This is worse than the
07-22 finding (a mis-read URL); a composed bucket that names another firm's tree is the class the
firm-separation gates exist to catch. **Do not quote comp-platinum bucket columns for this page.**

**F-8 — INSTRUMENT: `comp-transform fields ModelPortfolios` returns 7 field paths; §3 of this
document enumerates ≥45 consumed paths** (the tool misses every mdpf / per-firm / benchmark / peer hook), and `schema-check` returns
`[WARN] types-resolution: no types.ts found` — the types live in `portal-proxy.ts` / `endpoints/aum.ts`.
**Unchanged from 07-22; the gap persists across two audits.** This audit's denominator comes from the
full-file walk, not from the tool. Recorded so nobody sizes coverage off the tool's 7.

---

## 6. WHAT THE GATE NEEDS (for CTO's P2/P4 one-process-writes-both Lambda)

1. **The write set is §1a: 13 keys, of which K9/K10 do not yet exist.** Any generator scoped by the
   `mdpf/` prefix drops K11–K14 and breaks the Global radial, the bell curve, the Non-Model band and
   every Q-end priorLevel.
2. **The consumed bucket is `opal-data-portal-v2` and the CF behaviors are NOT flipped** (§2). A
   write to `opal-data-assets` alone is green-and-unread. Two-write means *both*, or the flip lands
   in the same gate.
3. **K11 has three other consumer pages** (§1c) — the blast radius is not one surface.
4. **F-1 is a design question the Lambda should settle, not inherit:** one total-field name across
   Global and per-firm, or an explicit documented asymmetry. It has already cost one client-visible
   defect.
5. **Applied write-attribution for the current keys is UNDETERMINED** (§2). Before a new writer takes
   these keys, the existing writer must be identified and stopped, or two processes will race the
   same key.
6. **F-3 means 49F/INF provenance is a producer gap** — the band cannot render for them regardless of
   FE work.

---

## 7. COMPILER TOOLS (mandate reproduction)

| Run | Expected | Observed | Verdict |
|---|---|---|---|
| `comp-cache collisions` | shared keys + type mismatches | 105/105 useQuery call-sites captured, 0 unparseable, 14 shared keys, **0 type mismatches** (none on this page) | PASS |
| `comp-transform schema-check ModelPortfolios` | rendered-field inventory, MISSING flagged | `[WARN] types-resolution: no types.ts found` | **TOOL GAP — F-8** |
| `comp-transform fields ModelPortfolios` | every data-bound field as denominator | 7 paths (`distributionData`, `metricsData` only) | **TOOL GAP — F-8**; denominator taken from full-file walk |
| `comp-platinum page ModelPortfolios` | full-stack artifact→component map | 2 of 10 fetches; **wrong bucket** on the traced behavior | **TOOL DEFECT — F-7** |
| `comp-routes behaviors` / `trace` ×5 | endpoint → behavior → key | uniform `/api/general/*` → `opal-data-portal-v2`, rewrite `/api/general/` → `json/` | PASS (DESIRED plane; APPLIED confirmed separately §2) |
| `comp-grep` (json/mdpf, json/portfolios producers) | producer candidates | ≥3 candidate writers per key family, 3 copies of the SmartX distribution script | PASS — feeds §2's UNDETERMINED verdict |
| live `cloudfront get-distribution-config EVTSA9VEHNZVH` | APPLIED behavior→origin | 24 behaviors; **no `/api/general/mdpf/*`**; `/api/general/*` → portal-v2 | PASS (Rule 22a applied limb) |
| live `lambda get-function-configuration opal-assets-mdpf-portal-publisher` | APPLIED target bucket | `ASSETS_BUCKET=opal-data-assets` | PASS |
| live `s3api get-object` ×12 + `head-object` ×4 | key existence + field presence | 12/12 in-scope keys retrieved and field-checked | PASS |

**Read-only TO honoured: zero FE modifications.** `git -C portal status --porcelain` shows **no
tracked modification** (untracked scratch dirs pre-date this audit and are not mine).
