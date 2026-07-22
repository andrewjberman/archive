# MASTER BRIEFING — SmartX (TAMP)

**Author / owning agent:** `4.0.0_SA_CRO` — Chief Research Officer
**Status:** Living master briefing. Consolidates every SmartX analysis in the Opal corpus.
**Date:** 2026-07-22 · **Commissioned:** Andrew-direct, following the BD and Orion/Eclipse masters.

> **READ THIS FIRST — SMARTX IS NOT THE SAME KIND OF ENGAGEMENT.**
> BD and Orion are **displacement** targets: incumbents whose reporting layer we intend to own. **SmartX is
> the LEVERAGE track** — a partner we intend to *buy more from*, not replace. D4 settles this (COO-settled,
> Andrew-direct): *"SmartX is the LEVERAGE track (long-term partner — BUY the model-state feed + the
> Eclipse-class plane, SELF-BUILD the medallion), NOT a supplant target."*
> **So the analytical question is different.** For BD/Orion it is *"what would we have to rebuild?"* For
> SmartX it is **"where is the buy-vs-build seam, and how controllable is the dependency?"** A teardown that
> treated SmartX as a displacement target would answer the wrong question rigorously.

> **EVIDENCE GRADES:** **[SPEC]** the CVO-passed D4 spec · **[LIVE]** live-probed against SmartX ·
> **[HAR]** captured portal session · **[PROD]** code we run · **[RULING]** an Andrew/CTO governance ruling ·
> **[INFERENCE]** fenced. **`[UNOBSERVED]` is never scored as absence.**
> **SHAPE vs DATA:** as with BD/Cottonwood and Orion/Inflection — distinguish **SmartX platform shape** from
> **Opal's own book/config data quality**. Flagged inline.

---

## 1. SmartX in one line

A **TAMP (Turnkey Asset Management Platform)** hosting Opal's model portfolios — **~5,800 accounts / ~$1.03B
AUM** at D4 vintage. **Deep on managed-account state** (model holdings, model returns at daily/weekly/monthly
cadence, risk stats, trade/rebalance events, AUM, allocation roster, and a model-management **write** plane)
and **shallow-to-absent on everything else** (no market data, no attribution, no peer universe, no factor
data, no working holdings classification).

**Crucially it is a standards stack** — OIDC/OAuth2 + REST + GraphQL. **Integrable by REST, not a scrape.**
That single fact is why the dependency is more controllable than BD's or Orion's (§7).

---

## 2. Corpus manifest

| Source | Author / vintage | Grade | What it uniquely gives |
|---|---|---|---|
| [`docs/architecture/DATA_PLATFORM_D4_smartx_endpoint_sweep.md`](../../../../docs/architecture/DATA_PLATFORM_D4_smartx_endpoint_sweep.md) | `0.6.0_AE_PartnerETL`, **CVO reconcile PASS**, CTO-canonical 2026-06-24 (v0.2) | **[SPEC/LIVE]** | The 5-surface sweep, the completeness-basis taxonomy, the partnership-slot map, the build-vs-buy boundary + dependency tradeoff, the vendor-bug list |
| `docs/briefs/mdsrc-smartx-comprehensive-endpoint-inventory-20260521.md` | 2026-05-21 | **[LIVE]** | The most complete surface map; api/3.1 exhaustion sweep + GraphQL introspection |
| `docs/briefs/smartx-rest-integration-design-20260515.md` | 2026-05-15 | **[HAR/LIVE]** | The seed: portal HAR (243 entries) + live ROPC token test; the design-of-record for retiring the EC2 scrape |
| `docs/briefs/smartx-rest-api-inventory-20260521.md` | 2026-05-21 | **[LIVE]** | The REST baseline (superseded by the comprehensive inventory) |
| `docs/briefs/mdsrc-s1-smartx-coverage-deep-dive-20260520.md` | 2026-05-20 | **[LIVE]** | Coverage depth |
| `docs/briefs/smartx-per-model-availability-matrix-20260515.md` | 2026-05-15 | **[LIVE]** | Per-model data availability |
| `docs/briefs/smartx-non-model-live-derivation-20260513.md` | 2026-05-13 | **[LIVE]** | Non-model derivation |
| `docs/briefs/mdpf-assets-{007,011,027}-*smartx*` | 2026-05-18/20 | **[LIVE]** | 49F/SmartX Phase-0 feasibility; per-account model-membership probe; coverage probe |
| `docs/briefs/yalp-mdsrc-b3-daily-smartx-direct-swap-20260521.md` | 2026-05-21 | **[PROD]** | The daily direct-swap |
| `memory/project_smartx_yaliu_account_of_record.md` | Andrew-direct 2026-07-15 / 07-17 | **[RULING]** | **The two-axis account-of-record ruling — supersedes D4 §2 (§4 below)** |

**Live integration:** `infra/aws/lambda/smartx_ingestion_pipeline` · `infra/aws/ec2/smartx-exporter` (legacy) ·
`data/smartx/scripts/*`.

---

## 3. Architecture — five surfaces

| Surface | Base | What it is | Verdict |
|---|---|---|---|
| **A — REST `api/3.1`** | `api.smartxadvisory.com/api/3.1` | The core. Envelope `{data, version, hostDetails, statusCode, requestId, timestamp}` | **The integration surface** |
| **B — performance** | `performance.smartxadvisory.com/models/performance` | Monthly returns + risk/return statistics | **The analytics core** |
| **C — GraphQL** | `graphql.smartxadvisory.com/graphql` | **NOT analytics** — a trade-restriction / compliance-flag microservice (`getFlag/listFlags`, `createFlag/batchUpdateFlags`) | **Bounded: zero portfolio data** |
| **D — legacy `api/3.0`** | `smartx.managedaccounts.io` | A 105-byte stub + model commentary | **Dropped** |
| **E — portal internal** | `portal.managedaccounts.io/ng_api/v1/mngr/*` | Portal UI plumbing | **Not a data API** |

### 3.1 Surface A — the endpoints that matter **[LIVE]**

| Endpoint | Grain | Yields |
|---|---|---|
| `models/{modelId}` | model | identity: name, **reportedModelId**, rebalanceThreshold, minimumAllocation, benchmarks[], fees[] |
| **`models/{modelId}/performance?grouping=daily\|weekly\|monthly`** | model, **multi-cadence series** | per-period `pnl{dollar,percent}` + `summary{begin/endMarketValue, transactions, fees}` — **THE daily flow-adjusted model-return source** |
| **`reportedmodels/{rmid}/holdings`** | per-symbol, snapshot | ticker, quantity, price, marketValue, **percentOfPortfolio** |
| **`reportedmodels/{rmid}/changerequesthistory`** | per-trade **event log** | tradeTimestamp, ticker, qty, activity, from/to — **the Eclipse-class trade-event read** |
| `enterprises/aum?modelid=` | model, daily series | `closingEquity` daily book value (**flow-contaminated, NOT a TWR**) |
| `enterprises/allocations?modelid=` | per-account | the allocation roster (advisor, value, openedDate) |
| `models/{id}/statistics` | model, snapshot | value, cash, exposure{long,short,net,gross} |
| `benchmarks`, `accounts`, `users`, `users/access` | — | reference + entitlement |

**Confirmed ABSENT (404, exhaustion-swept twice):** `attribution`, `risk`, `sectors`, `characteristics`,
`transactions`, `trades`, `securities`, `sleeves`, `commentary`, per-model `allocations`.
**→ No attribution / risk-decomposition / per-segment / transaction endpoint exists.** Empirically bounded,
not inferred.

### 3.2 Surface B — the analytics core **[LIVE]**

`trackedYearsForModels.{id}.months` (monthly return % + per-month benchmark) · `monthly_statistics` ·
`monthly_benchmark_statistics` · **`model.calculations`** — the risk/return suite: **deviation, alpha_spread,
cagr, sharpe, sortino, max_drawdown, skewness, kurtosis, cumulative_return**.

**NOTE:** **Date params are ignored (always full-history). Monthly cadence end-to-end. Exactly one benchmark per
model; no peer/category universe.**

---

## 4. Auth — and the material update D4 predates

**D4 §2 (2026-06-24) records a single-credential model** — ROPC against IdentityServer, client
`smartx-managerportal-webclient`, credential **`opal7`**, one RS256 JWT (~2h) authenticating all surfaces,
rate limit ~20/min per credential (**stay ≤17/min**). That mechanism is still correct.

> ### **NOTE:** THE ACCOUNT-OF-RECORD RULING SUPERSEDES D4's SINGLE-CREDENTIAL FRAMING **[RULING]**
> **Andrew-direct 2026-07-15 and re-affirmed 2026-07-17 — after D4 was finalized.** The book is a
> **TWO-AXIS HYBRID, already deployed, both axes correct:**
>
> - **AXIS A — MODEL-DEFINITION OWNERSHIP (a catalog entitlement, NOT data access).** `opal7` (the *manager*
>   account) has `fullAccess = 11` → **owns Opal's 11 model definitions**. Enumerating the owned model book
>   requires it, and `expect_min_models >= 11` enforces exactly that. **PERMANENT, not interim.**
> - **AXIS B — ACCOUNT/CLIENT + PLATFORM DATA (runs the other way).** `opal7` has **`accountAccess = 0`** and
>   404s on `accounts/{id}/holdings` and `/activity`. **`yaliu` holds 452 `accountAccess`, those endpoints,
>   client identity, and the platform-wide `models/summary`.** `models_summary` was repointed to `yaliu`
>   (`smartx-pipeline-v1.7.0`).
>
> **"Only yaliu" means the DATA axis — never model-ownership.**
> **THE MIS-FRAME NOT TO REPEAT:** do **not** read `yaliu fullAccess = 0` as "view-only, needs a grant."
> It is a catalog-**ownership** number, not a data-access test. **There is no yaliu-fullAccess grant to
> pursue; do not draft one even if asked on the old framing — the premise is wrong.**
>
> **Consequence for D4:** its §2 *"one credential, all surfaces"* and its §3 note that `accounts` is *"empty
> for opal7"* are explained by Axis B — that emptiness is **an entitlement property, not a SmartX defect and
> not an empty book.** Any adapter must model **two credentials on two axes**, not one.

**SHAPE vs DATA:** the two-axis split is **SmartX platform shape** (entitlements are per-account and
per-axis). Which credential *we* had pointed where was **Opal config** — and it was a live defect until the
`models_summary` repoint.

---

## 5. Model identity — a build prerequisite **[LIVE]**

**Two UUID spaces. Do not confuse them.** `modelId` (used by `models/*`, `enterprises/*`, `performance`) vs
**`reportedModelId`** (used by `reportedmodels/*`, **including holdings**). Calling
`reportedmodels/{id}/holdings` with a *modelId* returns **HTTP 400**.

**The pull must chain:** `models/{modelId}` → read `.data.reportedModelId` → `reportedmodels/{rmid}/holdings`.

*(Structurally identical to Orion↔Eclipse's two ID-spaces, and to BD's internal-vs-`z`-external encodings —
**every one of the three vendors carries a dual identity space, and in all three cases it is the first thing a
naive integration gets wrong.** That is now a three-for-three invariant.)*

---

## 6. Vendor bugs and constraints — track these in any build **[LIVE]**

| # | Issue | Consequence |
|---|---|---|
| 1 | `models/{id}/statistics.returns` — **wrong-model** + dead mtd/qtd/ytd | Do not consume; use Surface B or `models/{id}/performance` |
| 2 | `reportedmodels/{rmid}/historicalperformance` — monthly and was **~14 months stale** | D4 called it dead; the 06-24 sweep found it returning data again. **Re-probe before trusting** |
| 3 | `holdings.assetType` uniformly **"equity"** (wrong for bond ETFs); `industry` = "Unknown" | **Classification must be Opal's** (ETFClassifier). This is the same moat BD and Orion own and SmartX does not |
| 4 | `holdings` is **snapshot-only** — no history endpoint | History must be **accrued** from daily snapshots going forward |
| 5 | `performance` **ignores date params** — always full-history | Window client-side; plan for payload size |
| 6 | `enterprises/aum.totalAum` **mis-scaled** | Use per-day `closingEquity`; and note it is **flow-contaminated, not a TWR** |
| 7 | Rate limit **~20/min per shared credential** | Stay ≤17/min; avoid the MDPF daily-chain window |
| 8 | **Two coexisting integration generations** — EC2 Playwright scrape + Lambda REST | Consolidate to REST; decommission the scrape after parity |

**Bug 6 is the one with teeth for us:** an AUM series that is flow-contaminated is *not* a return series.
**This is the same class as our own `c01` residual-plug and our `factor` mis-naming** — a field whose name
suggests a return but which is a book value. Any consumer must know which it is holding.

---

## 7. The build-vs-buy seam — the core deliverable

| Layer | SmartX role | Decision |
|---|---|---|
| Bronze / ingest | One per-source adapter (standards OIDC + REST, parked JWT) | **BUY the feed, OWN the adapter** |
| Silver / normalize | — | **OWN** |
| Gold / model engine, cross-source joins | — | **OWN** — the platform's core IP |
| Served (platinum / ADVI / MDPF) | — | **OWN** |
| **Model / trade / rebalance (Eclipse-class)** | SmartX **is** the TAMP: trade-event read + the model-management **write** plane | **BUY / PARTNER** |
| Model performance SoR | Surface B + `models/{id}/performance` | **BUY the SoR**, own any re-derivation |

**What SmartX supplies:** model holdings/weights, model returns (daily/weekly/monthly, flow-adjusted), model
risk stats, one benchmark per model, trade/rebalance event history, model AUM, the per-account allocation
roster, and the **model-management/rebalance write plane**.

**What it does NOT supply — Opal owns or sources elsewhere:** holdings *history* (accrue), holdings
**classification** (broken — Opal ETFClassifier), **attribution** inputs, **peer/category** analytics,
**factor** data, **market** data.

### 7.1 The dependency tradeoff — stated honestly

Partnering deepens a SmartX dependency *while we are trying to reduce vendor dependency on BD/Orion.* D4's
assessment, which I endorse: **the SmartX dependency is materially more controllable**, for four reasons —

1. **Standards REST + OIDC**, not a black-box scrape or a proprietary reporting UI → portable, re-pointable,
   introspectable.
2. **We already mirror the data into our own medallion** → SmartX is a *feed*, not the system of record for
   our reporting layer.
3. **We are the client** (~$1.03B on-platform) → commercial leverage, unlike a per-seat reporting subscription.
4. **Reversibility:** the reporting/aggregation BUY is fully reversible. **Only the Eclipse-class
   trade-execution BUY is sticky** — that is the one to negotiate deliberately, with Orion Eclipse as the
   named alternative.

**Net:** BUY the model-state feed and the trade/rebalance plane; SELF-BUILD the medallion, served surfaces and
non-model custodian ingest; source the analytics gaps elsewhere.

---

## 8. SmartX alongside BD and Orion — the three-vendor picture

| | **Black Diamond** | **Orion + Eclipse** | **SmartX** |
|---|---|---|---|
| Kind | Custodian-data reporting aggregator | Custodian aggregation + reporting (+ Eclipse OMS) | **TAMP — model/trade plumbing for OUR models** |
| Our posture | **Displace** | **Displace reporting; partner/consume the trade layer** | **Partner (leverage)** |
| Scope of book | Arbitrary custodian feeds | Arbitrary custodian feeds | **Only our managed-model accounts (~5,800)** |
| Integration | Reverse-engineered, cookie+Bearer, bot-detected login | Reverse-engineered, `Session` JWT, Playwright + SMS OTP | **Standards OIDC/ROPC, headless** |
| Public API spec | **None** | **Eclipse: yes (493 paths). Connect: none** | **None** (spec-hunt: all 404) |
| Performance methodology exposed? | **Yes** — `firm/globalsettings` | **Yes, richest** — 32+5 options, callable per request | **No method contract** — returns are given, not configurable |
| Attribution | Contribution-to-parent | **Brinson** | **Absent (404)** |
| Risk statistics | `[UNOBSERVED]` | Full suite | **Full suite (Surface B)** |
| Classification | **Owns it** (SuperClass/Class/Segment) | **Owns it** (3 axes) | **Broken** — Opal must own it |
| Dual identity space | internal int ↔ `z`-external | Orion `modelId` ↔ Eclipse ID (+ STRING/INT coercion) | `modelId` ↔ `reportedModelId` |

> **THE THREE-VENDOR OBSERVATION.** SmartX is the only one of the three that **does not expose a performance
> method contract.** BD publishes `firm/globalsettings`; Orion publishes a 32-option contract *and makes it
> callable per request*. SmartX simply returns numbers. **For a partner whose returns we may serve to clients,
> "what method produced this?" has no queryable answer** — which is a real diligence gap, not a bug.
> It also means SmartX **cannot** serve as a methodology reference the way BD does for defensibility; it can
> only be a *value* oracle for the model slice.
>
> **And SmartX is the only one already on our target ingest pattern** — standards REST, parked JWT, headless.
> D4's point stands: it is *the model for the Schwab/BD/Orion ingest we are trying to reach.*

---

## 9. Completeness basis — what "we know SmartX" means

D4's per-surface taxonomy is the model other vendor specs should copy:

| Surface | Basis | Can we fully know it? |
|---|---|---|
| **C — GraphQL** | **PROVABLY COMPLETE** — schema introspection returns the whole schema by construction | **YES** — "compliance-flags only, zero analytics" is a *provable* bound |
| **A — REST api/3.1** | **Best-effort, empirically bounded** — exhaustion-swept twice (05-21, 06-24); no vendor spec, so a 404 means *absent as-of-date*, not *cannot exist* | **NO** |
| **B — performance** | **Observed** (HAR + spot-checks; not exhaustion-swept) | NO |

**No vendor API spec exists** — a live spec-hunt probed `/swagger*`, `/openapi.json`, `/v3/api-docs`,
`/api-docs`, `/.well-known/*` across both hosts: **all 404**. The only published definition is OIDC discovery
(auth-only).

**And the surface drifts.** Between 05-21 and 06-24 the live model roster went **7 → 11** (new Opal Global
total-return + Dividend Income), `accounts` went from empty to populated, and `historicalperformance` began
returning data. **The re-probe was warranted, and any build must re-probe at build time.**

---

## 10. Open items

1. **The Eclipse-class BUY-vs-BUILD final call** — SmartX (this brief) vs Orion Eclipse (D3) vs self-build.
   **A product + commercial decision, not an engineering estimate.** D3 and D4 jointly inform it and neither
   resolves it.
2. **Holdings classification ownership** — SmartX's `assetType` is broken, so Opal's ETFClassifier is
   load-bearing. Same moat both other vendors own.
3. **SmartX bucket placement vs firm separation** — SmartX model data lands in **`opal-data-bd`**
   (BD-domain-colocated by use-case) and MDPF consumes it there. When the engine generalizes per-firm, that
   placement collides with the **bd/cot/inf never-cross-firm rule**. **Flagged in D4 as a D5 must-address and
   still open.** *This is the one item here with a compliance edge, and it is ours, not SmartX's.*
4. **Legacy EC2 exporter decommission** — after REST parity.
5. **Multi-firm SmartX onboarding** — generalization is a platform requirement.
6. **No method contract (new, from this brief)** — if SmartX returns are ever served to clients as Opal
   numbers, we should ask SmartX to state their return methodology in writing, since the API will not.

---

## 11. Cross-reference

[`MASTER_BLACK_DIAMOND_ANALYSIS.md`](MASTER_BLACK_DIAMOND_ANALYSIS.md) ·
[`MASTER_ORION_ECLIPSE_ANALYSIS.md`](MASTER_ORION_ECLIPSE_ANALYSIS.md) ·
[`SURFACE_RECONCILIATION_TEST_20260722.md`](SURFACE_RECONCILIATION_TEST_20260722.md) ·
BD × Orion synthesis: [`../../../../docs/research/competitive_recon/orion_20260722/PLATFORM_STRUCTURE_COMPARISON_20260722.md`](../../../../docs/research/competitive_recon/orion_20260722/PLATFORM_STRUCTURE_COMPARISON_20260722.md) ·
Engagement index: [`../RECON_REGISTER.md`](../RECON_REGISTER.md)
