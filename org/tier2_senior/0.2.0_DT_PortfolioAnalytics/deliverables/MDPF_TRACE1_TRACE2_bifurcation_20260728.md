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

---

# RESIDUALS — CLOSED (Andrew: *"finish the traces"*)

## R1 — `json/latest/manifest.json` = THE YANG-PIPELINE MANIFEST. **CLOSED.**
Producer: **`yang-generate-manifest`** Lambda (`docs/reference/yang-pipeline-lineage-map.md:70` —
*"source-verified: `MANIFEST_KEY` constant; also reads `json/latest/` prefix to enumerate artifacts"*).
Second writer: `opal_security_scanner_processor/lambda_function.py:402-410` appends a `screening_excel`
entry. Consumed off-portal too: `m365-mcp-gateway/.../opal_portal/integration.py:69`.
Bucket contents corroborate — `attribution_excel · cma_excel · data_pkl · manifest · model_pkl · peer_excel`.
It is described in-estate as *"the canonical freshness signature"* for yang.
> **NOTE: this is MY OWN pipeline** (`yang-pipeline`, DT-owned). The Benchmark tab reads the yang manifest,
> which is coherent — benchmarks are produced by `yang-model-portfolio-benchmarks`. **Not debt; correctly a
> sixth namespace, and it was simply invisible to every mdpf/portfolios-shaped search.**

## R2 — THE FROZEN PER-FIRM LEGACY KEYS. **CLOSED, and it CORROBORATES the vintage verdict.**
`data/smartx/scripts/compute_per_firm_account_distribution.py`, **dated 2026-05-29 — the exact
LastModified of the frozen keys.** Its docstring contains BOTH targets:
```
line 3   "Emits json/portfolios/{firm}/account-distribution.json for 49financial ... and inflection"
line 18  "Output keys (per DE coordination 20260529T210337Z -- aligned to DE query key):"
line 19    json/mdpf/49financial/account-distribution.json
line 20    json/mdpf/inflection/account-distribution.json
```
**The script was written to emit into `json/portfolios/{firm}/` and RE-POINTED to `json/mdpf/{firm}/` the
same day**, per DE coordination. **The frozen legacy per-firm objects are the artifacts of the pre-re-point
run — orphaned 2026-05-29 and never touched again.**
> This is the vintage verdict with a **timestamp and a cause**, not an inference: the two namespaces held the
> same per-firm shape because one was re-pointed into the other. **And the docstring's opening line still
> names the OLD target while its Output-keys section names the new one** — doc-lagging-code, the same shape
> as Trace 1's half-finished cleanup, in the file that performed the migration.

## R3 — `account_distribution.json` (UNDERSCORE) IS A STAGING CONVENTION, NOT DRIFT. **CLOSED.**
The underscore form is the **gold/staging** spelling; the hyphen form is the **served** spelling:
```
gold/mdpf_revamp/{firm}/account_distribution.json   dim_mdpf_account_distribution.py:69-73 (STAGING_PREFIX)
gold/mdpf_revamp/cottonwood/account_distribution.json  build_cottonwood_mdpf_pair.py:4,464
views/account_distribution.json                     compute_account_distribution.py:86
   vs
json/portfolios/account-distribution.json           compute_account_distribution.py:81 (PORTAL_OUTPUT_KEY)
json/mdpf/{firm}/account-distribution.json          served
```
**A deliberate layer boundary, not a typo.** ⚠ **EXCEPT** the 2026-02-19
`json/portfolios/account_distribution.json` — an **underscore key in the SERVED namespace**, predating the
convention. **Orphan; no live reference found.**

## R4 — PER-FIRM × BENCHMARK/PEERS. **CLOSED ANALYTICALLY — stronger than sampling it.**
All four tab-gated queries are **firm-invariant**: `queryKey`s carry **no firm token**
(`['model-portfolio-benchmarks']`, `['etf-benchmark-returns']`, `['peer-performance']`,
`['model-portfolio-timeseries']`) and every endpoint fn takes **no arguments**
(`portal-proxy.ts:827, 858, 890, 935`). **Selecting a firm CANNOT change these URLs**, so the unexercised
combination is provably empty rather than merely unsampled.
> **Worth flagging, not adjudicating:** this means **Benchmark and Peers render identical data regardless of
> which partner is selected**, on a page whose header carries a partner selector. Plausibly correct
> (benchmarks are model-level, not firm-level) — but it is a UX/semantics question someone should confirm,
> not a thing I can settle from the wiring.

## R5 — THE PREVIOUSLY-`UNTRACED` PRODUCERS. **NOW NAMED — but with a multiplicity warning.**
- **`json/portfolios/account-distribution.json`** ← `data/smartx/scripts/compute_account_distribution.py:81`
  (`PORTAL_OUTPUT_KEY`). **Single, clear writer.**
- **`json/portfolios/aum-metrics.json`** ← **AT LEAST THREE candidate writers**, and I am not adjudicating
  which one actually wrote the live object:
  ```
  infra/aws/lambda/smartx_ingestion_pipeline/lambda_function.py:13   "3.5 Generate AUM metrics -> json/portfolios/aum-metrics.json"
  infra/aws/lambda/opal-assets/.../opal-assets-mdpf-portal-publisher/lambda_function.py:51   PUBLISH_MAP ("portfolios","aum-metrics")
  data/mdpf/scripts/gold/dim_mdpf_aum_metrics.py:40,54   staging key + "(AE repoints json/portfolios/aum-metrics.json)"
  ```
  > **THE SOURCE-SIDE ANSWER IS A CANDIDATE LIST, NOT AN ATTRIBUTION.** Which one wrote the LIVE object is
  > still **unattributable** — CloudTrail has no data-event coverage of `portal-v2`, and the object carries
  > no producer metadata. **Naming three candidates is progress over `UNTRACED`; it is NOT the answer to
  > "who wrote this."** Read the list as a floor.
  Readers found incidentally: `infrastructure_monitor`, the smartx `ai-supervisor`(-v2), and
  `data/analysis/q1_2026_aggregate_opal_return.py:50` — **an analysis script reading a served portal key.**

## STILL OPEN (not closable from the consumption side)
- **Applied write-attribution for `portal-v2`** — structurally unavailable (no CloudTrail data events, no
  object metadata). Needs producer-side instrumentation, which is an AE/CTO decision, not a trace.
- **Single-date grounding** on artifact contents where stated; the 447-date history remains untested.
- Error/empty states and modals never exercised in the runtime capture.
