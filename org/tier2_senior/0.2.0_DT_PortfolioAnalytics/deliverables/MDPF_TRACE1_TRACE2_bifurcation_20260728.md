# TRACE 1 + TRACE 2 — the `aum-metrics` bifurcation and the two-namespace split

**Author:** `0.2.0_DT_PortfolioAnalytics` · **Date:** 2026-07-28
**Directed by:** Andrew ~19:15Z via CTO 191648Z. **The deliverable is the LOGIC, not the inventory.**
**Scope:** trace only. No writes, no fixes, no promote.

---

## DENOMINATOR + PREDICATE (stated before the findings, per the binding method)

**METHOD: enumerate from the RENDER, work backwards.** Two instruments, different blind spots, counts
reported separately.

| instrument | denominator | predicate | blind to |
|---|---|---|---|
| RUNTIME capture, deployed PROD | **22 distinct `/api` requests** over **7 exercised contexts** | any URL the browser requested (a 401 still proves the request) | anything unexercised; a fetch gated behind a successful response |
| SOURCE trace (imports, not patterns) | **12 query sites** in `ModelPortfolios.tsx` + sub-components | resolved endpoint→URL literal | runtime-composed URLs |
| S3 listing | full `json/portfolios/` + `json/mdpf/` | — | — |

**Contexts exercised (named, not implied):** `load:global:AUA`, `tab:global:Benchmark`, `tab:global:Peers`,
`tab:global:AUA`, `firm:49financial:AUA`, `firm:inflection:AUA`, `firm:cottonwood:AUA`.
**NOT exercised:** per-firm × Benchmark/Peers combinations; error/empty states; any modal.

**UNION = 23.** Runtime found 22; SOURCE adds 1 the runtime never fired
(`/api/general/benchmarks/model_portfolio_timeseries.json`, `ReturnVolatilityScatter.tsx:334`).
**Runtime found 1 that BOTH source traces missed** — see the sixth namespace below.

---

## SIX NAMESPACES, NOT TWO

| namespace | keys | notes |
|---|---|---|
| REVAMP `json/mdpf/` | 8 | `global` + 3 firms |
| LEGACY `json/portfolios/` | 4 | all fired on **initial Global load** |
| `json/benchmarks/` | 2 (+1 source-only) | Benchmark tab only |
| `json/peers/` | 1 | Peers tab only |
| **`json/latest/`** | **1** | **`/api/general/json/latest/manifest.json`, Benchmark tab. NEW — invisible to every source-side pattern used today** |
| `/api/scoped/advisor-intelligence/` | 6 | `?firm=bd`, fires on Global load |

> **The count went 4 → 5 → 8 → 22/23 today. EVERY correction came from widening the METHOD, never from
> looking harder with the same one.** `json/latest/` was found only by completing the lazy-tab runtime
> capture — the step that was nearly skipped as a formality.

---

# TRACE 1 — `aum-metrics.json`: one key, two consumers, two shapes

## THE LOGIC, RECOVERED — a demo stopgap that outlived its occasion, and a half-finished cleanup

```
portal-proxy.ts:277  getAUMSummary()                 -> /api/general/portfolios/aum-metrics.json  as AUMSummary
portal-proxy.ts:358  getAUMMetricsWithCalculations() -> /api/general/portfolios/aum-metrics.json  as AUMMetricsResponse
aum.ts:696           getAUMMetricsByFirm()           -> /api/general/mdpf/{firm}/aum-metrics.json  (3rd consumer, other namespace)
```

**`getAUMSummary`'s own docstring is the confession** (`portal-proxy.ts:264-271`):
> `🚧 DEMO MODE: Using public endpoint (no auth) for demo purposes`
> `TODO: Revert to private endpoint for production:  Path: /api/private/portfolios/aum-summary.json`
> `Path: /api/general/portfolios/aum-metrics.json (using metrics as fallback)`

**MEASURED: `aum-summary.json` DOES NOT EXIST.** `head-object` empty; the full `json/portfolios/` listing
carries `account-distribution.json`, `account_distribution.json` *(2026-02-19, a second spelling)*,
`aum-metrics.json`, `aum-timeseries.json`, `latest.json`, `manifest.json`, `metrics.json`,
`non_model_assets.json`, `non_model_assets_preview.json`, `summary.json`, `timeseries.json` — **no
`aum-summary.json`.**

> **So the "fallback" has no original to fall back FROM.** The intended artifact was never produced (or was
> retired), someone pointed the summary consumer at the metrics key to make a demo work, and **the stopgap
> became the architecture.**

**AND THE CLEANUP WAS DONE — TO THE SIBLING ONLY.** `getAUMMetricsWithCalculations` had its identical DEMO
comment deliberately retired (`:355-358`, `NFRA_GRAPHS.D7-FIX.T3`: *"prior DEMO comment + TODO to move to
/api/private/ removed — the general endpoint is now auth-gated at CF layer, equivalent protection"*).
**`getAUMSummary`, 80 lines above, still carries the stale DEMO/TODO text.** A partial cleanup that fixed one
function and missed its twin — **the same shape as the 4-vs-5 and the codeMap: right method, incomplete
application.**

## STRUCTURAL COMPATIBILITY — IT SILENTLY MIS-READS (answering CTO's exact question)

`AUMSummary` (`:199`) declares 5 fields. Checked against the **live served payload**:

| declared | present in payload? |
|---|---|
| `period` | PRESENT |
| `total_aum` | **ABSENT** → `undefined` at runtime (payload has `total.aum`) |
| `total_accounts` | **ABSENT** → `undefined` (payload has `total.account_count`) |
| `by_asset_class` | **ABSENT** → `undefined` |
| `by_model` | PRESENT |

Served top-level keys: `period, last_updated, dates, total, by_model, meta`.
**`AUMSummary` is NOT a subset of `AUMMetricsResponse`. Three of five fields do not exist.** `apiRequest<T>`
is a compile-time cast with no runtime validation, so this is **a contract lie that TypeScript reports as
type-safe.**

**INERT TODAY, AND INERT IS NOT ABSENT:** both consumers (`SelectionTab.tsx:89`, `HoldingsTab.tsx:564`) read
**only `by_model`**, via their own inline type. Nothing reads the three phantom fields. **A future consumer
reading `data.total_aum` gets `undefined`, and the type says that is fine.**

## THE LIVE DEFECT THIS TRACE SURFACED (reported separately 192305Z)
Both consumers key an AUM-weighting map through a hardcoded `codeMap` that **hits 1 of 7** — served names
carry hyphens (`Short-Term`), map keys use spaces (`Short Term`). `allPortfolios = ['UST','ST','INT','LTC','LTA']`;
only `INT` resolves → **AGG weights Intermediate 100%, the other four 0%** on Attribution + Positioning.
**The equal-weighting fallback is disarmed by the single partial hit** (`hasAUM = totalAUM > 0`).
**NOT rendered — no visual claim made.** DE's lane. Not MDPF.

---

# TRACE 2 — three types in both namespaces: SCOPE-based or VINTAGE-based?

## FALSIFICATION TEST, STATED BEFORE THE ANSWER
- **SCOPE-based** would predict: legacy holds ONLY global shapes, REVAMP holds ONLY per-firm — a live
  partition, to be preserved.
- **VINTAGE-based** would predict: **both** namespaces carry the **same shapes**, differing in currency and
  coverage — debt, to be retired.

## MEASURED
```
LEGACY  json/portfolios/49financial/account-distribution.json   2026-05-29   1642 B
        json/portfolios/inflection/account-distribution.json    2026-05-29   2115 B
        (no cottonwood, no global subdir)

REVAMP  json/mdpf/{49financial, cottonwood, global, inflection}/   current
        json/mdpf/aggregate-aua-timeseries.json                    2026-07-27 15:10:34Z (scope-less)
```

**VERDICT: VINTAGE.** The legacy namespace carries the **same per-firm partition** the REVAMP namespace
does — it is not global-only. It is **frozen at 2026-05-29**, covers **2 firms instead of 4 scopes**, and was
superseded rather than partitioned away from. **The scope-based hypothesis is falsified by the presence of
`json/portfolios/{firm}/` at all.**

> **CTO's working assumption was vintage and it survives the test — but note it survives on evidence that
> would have falsified it, not on agreement.** Had `json/portfolios/{firm}/` been absent, I would be
> reporting the opposite.

**Remediation implication (his framing): retire, do not preserve.**

## A DETAIL THAT MATTERS FOR THE PUBLISHER
`json/mdpf/aggregate-aua-timeseries.json` (the **scope-less** key, CTO-ruled = `global`) carries
LastModified **2026-07-27 15:10:34Z** — **the ~1500Z clobber signature.** So the legacy producer writes into
the **REVAMP** namespace too, at the scope-less key. It is now covered by AE's `json/mdpf/*` deny.

## PRODUCTION HALF — ROUTED, NOT RECONSTRUCTED
Per CTO's instruction I do **not** reconstruct emitters. Identified where source names them:
- `json/portfolios/{non_model_assets,aum-timeseries}.json` ← `build_legacy_compat_emit.py` (Stage 3.5)
- `json/mdpf/*` REVAMP artifacts ← `build_aggregate_aua_timeseries.py` / `dim_mdpf_*`
- **`json/portfolios/{aum-metrics,account-distribution}.json` → `UNTRACED`.** I have not established their
  writer, and **CloudTrail cannot name a `portal-v2` writer at all** (no data-event coverage — C-4), so this
  may be structurally unattributable from the consumption side. **Reporting UNTRACED rather than inferring.**
- `json/portfolios/{49financial,inflection}/account-distribution.json` → **UNTRACED**, frozen 2026-05-29.

---

## RESIDUALS
- **Per-firm × Benchmark/Peers not exercised.** A firm-scoped benchmark fetch would not appear here.
- **`json/latest/manifest.json` not traced** — found at the buzzer, producer and purpose unknown.
- **`account_distribution.json` (underscore, 2026-02-19)** sits beside `account-distribution.json` (hyphen).
  Two spellings, one concept. Not traced.
- Single-date grounding on artifact contents where stated; the 447-date history remains untested.
