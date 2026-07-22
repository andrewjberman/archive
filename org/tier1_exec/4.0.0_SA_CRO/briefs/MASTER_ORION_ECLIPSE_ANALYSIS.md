# MASTER BRIEFING — Orion Advisor Solutions + Orion Eclipse

**Author / owning agent:** `4.0.0_SA_CRO` — Chief Research Officer
**Status:** Living master briefing. Consolidates **every** Orion and Eclipse analysis in the Opal corpus.
**Date:** 2026-07-22 · **Commissioned:** Andrew-direct — colocate all research and write a master briefing
covering architecture, endpoints, methodologies.

> **HOW TO READ THIS.** A **consolidation with pointers**, not a copy — source documents stay canonical at
> their paths. Every section names its source and its evidence grade: **[HAR]** captured bodies · **[PROD]**
> code we run in production · **[LIVE]** verified against live Orion/Eclipse · **[DOC]** vendor documentation
> (public) · **[SPEC]** the vendor's own OpenAPI · **[INFERENCE]** labelled. **`[UNOBSERVED]` is not absence.**
>
> **EGRESS POSTURE:** every Orion/Eclipse finding here came from operator-supplied captures, our own
> production pulls, or **public** documentation. RCN-0002 held standing session egress and **did not use it** —
> no Orion API was called for research purposes.

---

## 1. Start here — the three-surface picture, and the thing nobody had joined up

**Orion is not one product. It is three surfaces with three different roles, and Opal's corpus reached them
from three different directions in three different months.**

| | **S1/S2 — Orion Connect** | **S3 — Eclipse** | **S4 — the Connect *product* layer** |
|---|---|---|---|
| Base | `api.cloud.orionadvisor.com` | `www.orioneclipse.com` / `api.orioneclipse.com` | same host as S1 |
| Role | Custodian aggregation + reporting; the **daily-value snapshot** | Trading / rebalancing / model overlay | **How Orion computes and configures performance** |
| Auth | JWT `Authorization: Session` (**HS512**) | JWT `Session` (**HS256**), *exchanged from* the Orion JWT, separate ID-space | same session |
| **Opal uses it** | **YES — 9 production pull Lambdas, daily** | **YES — read-only, 4 endpoint classes, daily** | **No** |
| Catalog | **No public catalog** | **Public OpenAPI 3.0.3 — 493 paths / 582 ops / 56 tags** | no public catalog |
| Our source | D3 + ADVI_ORIAPI **[PROD/LIVE]** | D3 §5 + the Eclipse catalog **[PROD/SPEC]** | **RCN-0002 [HAR+DOC]** |

**THE JOIN THIS BRIEFING MAKES.** Until now the corpus described Orion as *a feed we pull* (D3/ADVI_ORIAPI —
the ingest view) and, separately, RCN-0002 described it as *a product with a methodology* (the performance
view). **They are the same host.** We have been ingesting from Orion Connect daily for months while its
performance-methodology contract sat unexamined one path segment away.

> **Two independent confirmations that `api.cloud.orionadvisor.com` IS Orion Connect.** Orion's *public docs*
> never mention that hostname — they publish `api.orionadvisor.com` — so a docs-only pass could not resolve it
> and correctly flagged it `[NOT-RETRIEVED]`. It is settled twice over: **(a)** D3 §2 names it as the Connect
> base for our production pulls **[PROD]**; **(b)** the RCN-0002 capture shows it serving
> `/api/v1/Reporting/Scope`, `/Portfolio/*`, `/Billing/*` **[HAR]**. Same API, different hostname.

---

## 2. Corpus manifest

### 2.1 Primary specs and catalogs

| Source | Author / vintage | Grade | What it uniquely gives |
|---|---|---|---|
| [`docs/architecture/DATA_PLATFORM_D3_orion_eclipse_arch_spec.md`](../../../../docs/architecture/DATA_PLATFORM_D3_orion_eclipse_arch_spec.md) | `0.4.0_DS_ClientPlatform`, CTO-gated + **CVO reconcile-to-live PASS** 2026-06-24, v1.2 | **[PROD/LIVE]** | The three surfaces; the 9 daily pulls; **the snapshot pass-through thesis**; the Orion↔Eclipse join; the ~3.4% valuation lag; auth comparison; the completeness-basis addendum |
| [`docs/architecture/ADVI_ORIAPI.md`](../../../../docs/architecture/ADVI_ORIAPI.md) (793 L) | DS, HAR 2026-04-27 | **[HAR]** | **The Orion Connect API contract** — auth contract (A.1), the full query lifecycle (A.2), cohort scoping, the stored-proc back door (A.5), a Python spike (A.6), and an explicit residual-unknowns section (A.7) |
| [`data/orion/api/ECLIPSE_API_V1_ENDPOINT_CATALOG.md`](../../../../data/orion/api/ECLIPSE_API_V1_ENDPOINT_CATALOG.md) (976 L) | `0.4.0_DS_ClientPlatform~B` + `0.7.0_AE_CloudOps`, 2026-07-16 | **[SPEC]** | **The parsed 493-path Eclipse catalog**, vendor-identity-verified, with *what Opal consumes today (5 of 493)* called out |
| [`docs/research/competitive_recon/orion_20260722/ORION_TEARDOWN_20260722.md`](../../../../docs/research/competitive_recon/orion_20260722/ORION_TEARDOWN_20260722.md) | **RCN-0002**, 2026-07-22 | **[HAR+DOC]** | **The performance method contract (32 firm + 5 account options)**; `Reporting/Scope` as a calculation graph; the 118-group report vocabulary; the billing/fee engine; classification axes |
| [`docs/research/competitive_recon/orion_20260722/PLATFORM_STRUCTURE_COMPARISON_20260722.md`](../../../../docs/research/competitive_recon/orion_20260722/PLATFORM_STRUCTURE_COMPARISON_20260722.md) | **RCN-0002** | synthesis | BD × Orion — the seven invariants, the divergences, what to build |

### 2.2 Feasibility, probes and coverage

| Source | The finding |
|---|---|
| `docs/briefs/data-scientist-eclipse-ingestion-feasibility-20260514.md` | The Eclipse ingestion feasibility + the join model |
| `docs/briefs/mdpf-eclipse-inflection-model-aua-feasibility-20260518.md` | The Eclipse book and the **~3.4% valuation lag**, empirically reconciled |
| `docs/briefs/mdpf-assets-006-eclipse-inflection-model-tracking-coverage-20260518.md` | Model-tracking coverage |
| `docs/briefs/inf-pattern-e-orion-rest-capability-probe-20260515.md` | The original Orion REST capability probe |
| `docs/briefs/DATA_PLATFORM_DC_CHAR_orion_own_account_api_quality.md` | **Orion's own-account API quality characterization** |
| `docs/briefs/dc2-eclipse-authed-capture-diagnostic-plan-20260625.md`, `dc2-eclipse-offpeak-test1-harness-build-spec-20260625.md` | Eclipse authed-capture plans — the route to the write-side frontier |
| `data/inf/manual_api/README.md` + `go_nogo.md` | The Envision/ExcelReports pull reference + Phase-4 GO/NO-GO |

*(Adjacent, deliberately not folded in: the **SmartX** corpus — `mdsrc-smartx-comprehensive-endpoint-inventory`,
`smartx-rest-api-inventory`, `D4_smartx_endpoint_sweep`, etc. SmartX is the **partner** candidate for the
trade layer, not an Orion surface. It belongs in its own briefing if we ever do a TAMP comparison.)*

---

## 3. Architecture

### 3.1 S1/S2 — Orion Connect **[PROD]**

**One versioned REST API** — `api.cloud.orionadvisor.com/api/v1/{Domain}/...`. Domains observed in the RCN-0002
capture: `Portfolio`, `Reporting`, `Billing`, `Settings`, `Utility`, `Performance`, `Authorization`,
`Integrations`. **The architectural opposite of Black Diamond's ~15 services behind a gateway.**

**S2 — the per-day Assets SNAPSHOT is the reference shape.** `INF_B_00.canonical_holdings` reads market value
**directly** from Orion's per-day Assets endpoint — snapshot pass-through, no transaction reconstruction.

> **The single most important architectural point in the Orion corpus, and it is the same lesson BD taught:**
> the old reconstruct-from-transactions approach **corrupted 40.2% of rows to $0**; moving to the snapshot
> fixed it. Orion is the *proof* that snapshot methodology works cleanly when the vendor exposes a per-day
> positions endpoint. **Direct-custodian (Schwab) should target the same shape.**
> *Precision from the CVO reconcile:* the real path has a silver hop — **Orion Assets → bronze →
> `silver/api_dims/positions_mv` → INF_B_00 gold** — not "straight off the Assets endpoint."

### 3.2 S3 — Eclipse **[PROD/SPEC]**

A **separate product, separate API, separate ID-space, separate JWT**. 493 paths / 582 operations / 56 tags,
published as public OpenAPI 3.0.3 at `api.orioneclipse.com/doc/`.

Largest tags: `Models` 63 · `Trades` 44 · `Preferences` 35 · `Account` 33 · `Portfolios` 27 · `Teams` 23.
Path prefixes: `tradeorder` 103 · `modeling` 49 · `admin` 46 · `tradetool` 36 · `preference` 35.
**Eclipse's `Reports` tag is TRADE analysis, not performance** — `/report/allocations`, `/report/trades/*`.
Holdings live here too: `/holding/holdings/{id}/taxlots|transactions`.

**Both vendors keep the OMS out of the reporting platform** — BD's Rebalancer is a distinct service; Orion
makes it a distinct *product*. That convergence is why RCN-0001 scoped the rebalancer out of Wave 1.

---

## 4. Endpoints

### 4.1 The 9 daily production pulls **[PROD]** — what we actually consume

Each a Lambda on an EventBridge cron writing to `s3://opal-data-inf/bronze/orion-api(-v2)/{date}/`:

| Lambda | cron (UTC) | Output |
|---|---|---|
| `inf-api-reps` | 30 12 | representatives + household_rep_mapping |
| `inf-accounts-v2-daily` | 35 12 | new_portfolio_accounts |
| `inf-unified-account-dim-daily` | 40 12 | unified_account_dim |
| **`inf-api-assets-v2`** | 45 12 | **Portfolio Assets (the snapshot)** |
| `inf-api-positions` | 50 12 | positions |
| `inf-tax-daily` | 55 12 | tax_unrealized + tax_realized |
| `inf-billing-daily` | 35 13 | billing |
| `inf-performance-daily` | 40 13 | performance_dim (or `_SKIP.json`) |
| `inf-api-txn` | 0 13 | transactions |

Chain: bronze → `_silver_complete` sentinels → `inf-silver-aggregator` → `inf-gold-trigger` →
`inf-gold-layer-runner` EC2 (~40 `INF_*` scripts) → `gold/*` + `platinum/advisors/*` → the ADVI Inflection
tenant.

### 4.2 The Envision saved-query engine **[HAR/LIVE]** — validated end-to-end

```
GET  /api/v1/Reporting/Envision/ExcelReports                        -> list saved queries
GET  /api/v1/Reporting/Envision/ExcelReports/Verbose/{id}?expand=all -> the SAVED template (NOT runtime-ready)
POST /api/v1/Reporting/Envision/ExcelReports/{id}/Generate          -> 201 + Location (async, holds ~60s)
GET  {Location}  (= .../Run/{runId})                                -> 202 while running, 200 + CSV when done
```

> **The key gotcha, banked:** **Verbose ≠ runtime body.** Verbose returns
> `deliveryOptions/queryType/category/databaseIdList = null` and omits `entityIds`; the Generate POST must
> layer them in (`databaseIdList:[4698]`, `entityIds:[]` DB-scoped or `[3,11,12]` entity-scoped,
> `reportFormat:"Csv"`). **A saved template is not a runnable one** — structurally the same trap as BD's
> thin-envelope-vs-persisted-body (Surface A), arrived at by a different vendor.

Also: a **generic stored-procedure back door** — `POST /api/v1/Homepage/Action/DataSources/{id}` with
`configurationJson.query` = a stored-proc name. The dashboard widgets use it; the Generate path is preferred
because it wraps SPs with parameter validation. **Observed, deliberately unused.**

### 4.3 The product surface **[HAR, RCN-0002]** — 150 endpoints the app calls

`Settings` 40 · `Utility` 39 · `Reporting` 16 · `Portfolio` 10 · `Billing` 9 · `Authorization` 2 ·
`Integrations` 1 · `Performance` 1. Notables:
- **`Settings/EntityOptions/{scope}/Categories/Performance Calculator`** — the method contract (§5).
- **`Settings/Views/{Name}Dto`** (24 endpoints) — saved **grid/column definitions served from the API**.
- **`Reporting/Envision/PlaceholderHeirarchy`** (507 KB) — the report field vocabulary: **118 entity groups**.
- **`Utility/Logging/PageView/{route}`** — Orion's own telemetry; it records the app route, and I used it to
  reconstruct the walked page inventory after a truncated capture lost the page titles.

### 4.4 Eclipse — the 5 of 493 we consume **[PROD]**

`GET /v1/admin/Token` (JWT exchange) · `/v1/portfolio/portfolios/simple` (the **account→model assignment join
table**; carries `accountId` the full endpoint lacks) · `/v1/portfolio/portfolios` (`totalValue`,
`managedValue`, `excludedValue`, `cash`, `lastRebalancedOn`) · `/v1/modeling/models` ·
`/v1/modeling/models/{id}` (composition tree with target weights).

**The write side exists and is unused.** Rebalance generation/approval, order submission, model-assignment
writes — **this observed-but-unused write layer IS the self-build-vs-partner frontier.** Self-build is
technically visible; we only read. *(Exact write-endpoint enumeration needs a dedicated Eclipse HAR of a
rebalance action — not captured, flagged, not claimed.)*

---

## 5. Methodologies — the highest-value section

### 5.1 The performance method contract — 32 firm + 5 account options **[HAR, RCN-0002]**

Selected, verbatim (full table in the RCN-0002 teardown §3):

| Code | Name | Tenant value | Allowed |
|---|---|---|---|
| `69CALCULAT` | **Calculation Method** | **`TWR`** | **TWR / Simple / IRR** |
| `1:69GROSSO` | **Gross Of Fee** | `False` ⇒ **net** | bool |
| `69PERFAFTERTAX` | After-Tax | `False` | bool |
| `1:69ANNUAL` | **Annualization Day-Count Method** | `Days with value only` | Days with value only / All days within range |
| `69INCLUDEA` | Include Accrued Interest | `True` | bool |
| `69CLIENTPE` | Household Performance Include | `All accounts` | All / Active / With value / Registrations with value / Active registrations |
| `69TWRGAPSUPPRESS` | **TWR Day Gap Suppression** | `1` | int |
| `69USESTORE` | Use Stored Performance | `True` | bool |
| `69FEEACCRUAL` | Fee Accrual | `{enabled:false…}` | object |
| **Account scope** | `69INCLUDEI` **Include In TWR** | *Include in Performance and Activity* | Include / Exclude |

**Firm default + per-account override.** BD's `firm/globalsettings` is firm-level only — **Orion's model is
strictly richer.**

### 5.2 THE MECHANISM — the contract is callable **[HAR+DOC]**

`POST /api/v1/Reporting/Scope` carries a `performanceOption` block, and **ten of its eleven documented
parameters have an exact settings twin**: `calculationMethod`↔`69CALCULAT`, `calcGrossOfFees`↔`1:69GROSSO`,
`annualizeIncludeDaysWithoutValue`↔`1:69ANNUAL`, `includeAccruedInterest`↔`69INCLUDEA`,
`calcFirstDayPerformance`↔`69ALLOWFIR`, `calcIntraDayPerformance`↔`69ALLOWINT`,
`suppressMixedRanges`↔`69SUPPRESS`, `suppressMixedAssetLevelGroups`↔`1:69SUPPRE`, `calcAfterTax`↔`69PERFAFTERTAX`,
`annualize`↔`69ANNUALIZ`.

**The settings row IS the persisted default for a request-time parameter.** The two halves were discovered
independently from two evidence layers — a capture and a documentation page — and corroborate field-for-field.

> **What to take from it:** our `dim_return_method` is the right idea, and Orion shows the two things our v0
> lacks — **per-entity override** (firm default, account exception) and **request-time override**, so one
> stored series can be re-cut gross/net, pre/after-tax, or annualized-or-not **without a rebuild**.
>
> **`1:69ANNUAL` is our own `c01` bug, solved as a setting.** *Days with value only* vs *All days within range*
> is exactly the trading-day-vs-calendar-day annualization mismatch. **Orion did not pick a constant — they
> named the choice and let the firm ratify it.**

### 5.3 Performance as a calculation graph, not a resource **[DOC]**

`POST /Reporting/Scope` = `{entity, entityIds[], asOfDate, calculations[]}`, nesting recursively via
`grouping`. **36 entity types** (Representative → Household → Registration → Account → Portfolio Group, down
to Asset, Risk Category, Moody Rating, Bond Maturity Year, Tax ID). **18 calculation types** — `performance`,
`performance-series`, `performance-breakdown`, `benchmark-performance(-series)`, `activity(-series,
-transactions)`, `cost-basis` (+ ST/LT/lots), `estimated-annual-income`, `projected-income`, `group-info`,
`group-statistic`, `benchmark-statistic`. `returnStyle` controls frequency / calendar-vs-rolling /
partial-period behaviour / cumulative / self-vs-parent context. Dates via `quickDate` or a relative-expression
grammar. **There is no `/performance/accounts/{id}`.**

**Two performance paths, and Orion says which to use:** on-demand `Scope` vs stored
`GET /v1/Reporting/BI/Performance` (`day, mtd, qtd, ytd, oneYear, threeYear, fiveYear, tenYear, inception`),
documented as **"1-2 days behind"** and recommended *only* when transactional data is unavailable. The firm
setting `69USESTORE` is its tenant-side twin.

> **Opal implication (PROPOSAL, not a fact).** Our script-per-artifact shape is BD's model — which is why
> adding one series to one chart costs a producer change, a harness change, a co-sign and a flip. We do not
> need Orion's full generality, but the shape is adoptable *at rest*: **store `fact_account_return` at the
> finest grain with the method contract attached, and make every window / rollup / gross-vs-net view a
> DERIVATION, never a separately-produced artifact.**

### 5.4 The analytics vocabulary **[HAR]**

**`Attribution` — Brinson**: `AllocationEffect`, `SelectionEffect`, `SemiNotionalEffect`, `TotalEffect`.
*Absent from the RCN-0001 spec; a different and arguably better question than BD's contribution-to-parent.*
**`Benchmark` (19)**: `Performance`, `AfterTaxPerformance`, `GrowthOf`, `Drawdown`, `Mean`, `Variance`,
`Covariance`, `StandardDeviation`, `BetaCoefficient`, `RSquared`, `JensensAlpha`, `SharpeRatio`,
`SortinoRatio`, `TreynorRatio`, `UpsideCaptureRatio`, `DownsideCaptureRatio`.
**`Allocation`**: `Level0…Level5` + `ParentLevel1` — a **6-level** reporting hierarchy.
**`Tax`**: `ShortTerm`, `LongTerm`, `Total`, `Lot`, **`TaxSavings`** + `TaxAlphaExcessBefore/AfterTaxPerformance`
— **directly relevant to OPAL_TAXSMA**.
**`Income` (14)**: yields to maturity/worst/best/next-call, modified duration, estimated annual income.
**`Trading` (11)**: model-vs-actual percent/value, `PercOutOfBalance`, tolerance bands.

### 5.5 Classification and entities **[HAR]**

**Three independent axes** — `ProductCategories` 5 · `RiskCategories` 20 (Morningstar-style) ·
`ProductClasses` **1,168** — plus `69AUTOASSE Auto Asset Classification`. *(BD uses one strict
SuperClass→Class→Segment tree. Orion's axes model is more flexible and costs no more to build.)*

**Entity hierarchy: Client → Registration → Account**, each account carrying `custodian`, `managementStyle`,
`isActive`, **`inBalance`**, **`lastReconciledEffectiveDate`**, `lastPositionDate`. **Reconciliation state is a
queryable account property, not an ETL-internal log line.**

### 5.6 The Orion ↔ Eclipse join, and the ~3.4% lag **[PROD/LIVE]**

Two ID-spaces stitched by two keys:
1. **Account value — by ID with coercion.** Eclipse `accountId` is a **STRING**; Orion `account.id` is an
   **INT**. `int(eclipse.accountId) == orion.account.id`. *(The type gotcha caught the first pass.)*
2. **Model — by NAME**, via a materialized 9-ID map. **Not by the live list endpoint** — `/v1/modeling/models`
   returns **NULL `name` for 8 of 9** models, so the name map must be a **materialized constant**. *(Same
   class as Orion `Trading/Models` returning `items: null` on list.)*

**The lag:** Orion `currentValue` is custody-settled EOD; Eclipse is rebalance-day intraday. Measured
**−$3.37M / −3.4%**, i.e. **96.6% reconciliation**.

> **This is structural, not a defect: accept and document, do not "fix."** Treat **Eclipse as the rebalance-day
> model source of truth** and **Orion as the settled custody value**. They are different valuation moments.

---

## 6. Auth **[PROD/LIVE, with [DOC] where noted]**

- **Orion Connect:** `Authorization: Session <jwt>` — **literal `Session ` prefix, NOT `Bearer`; a Bearer send
  silently 401s.** HS512, `~10h` TTL, payload `{A_C (database/firm), A_UD, A_ED, CID, exp, iss:"orion",
  aud:"session.orion"}`. **No auth cookies** — all observed cookies are analytics.
- **Required headers on every call:** `App: OrionConnect`, `AppPath: <UI route>`, `BrowserSessionId: <UUID>`,
  and `Origin/Referer` matching the host (Orion validates them against the session CSRF). **This is more than
  the public docs disclose** — a docs-only implementation would fail on the header contract.
- **Acquisition:** headless Playwright sign-in on the `inf-exporter` EC2 captures the header → S3 + Secrets
  Manager; daily 08:00 ET cron. **SMS 2FA** via the `inf-otp-relay` function-URL; a persisted "remember this
  device" cookie makes steady-state runs OTP-free (~30–90d).
- **Download exception:** the result-fetch URL also accepts `?Authorization=<jwt>` as a **query param**, with
  no `Session ` prefix.
- **Eclipse:** exchange the Orion JWT — `GET https://www.orioneclipse.com/v1/admin/Token` with
  `Authorization: Session <orion_jwt>` → `{eclipse_access_token, orion_access_token}`. **HS256** (Orion is
  HS512), `exp` is a **float** (Orion's is int), separate `firmId` and a **distinct user id**.
- **[DOC] — the public/partner path we do not use:** `GET|POST /api/v1/security/token` supports **Basic** and
  **OAuth2 authorization-code**; access token 10h, refresh token **375 days, one-time-use, one active per
  client_id**; **`Authorization: Impersonate` with `Entity: 4|5`** for advisor-acts-as-client. Credentials are
  **request-only**. *This is the supported route if we ever want vendor-sanctioned access instead of a
  browser-captured session.*

---

## 7. Known limits and traps

- **Server-side `$filter` / `modelId` / `modelAggId` are SILENTLY IGNORED** on `Portfolio/Accounts` →
  client-side filtering required. **A filter that returns 200 and ignores you is worse than one that errors.**
- **`Trading/Models` list returns `items: null`** — composition needs `/{id}` detail.
- **`/v1/modeling/models` list returns NULL `name` for 8/9** — hence the materialized name map (§5.6).
- **Result caps:** `$top` hard cap **100,000**; Data Queries cap at **20 minutes or 1,000,000 rows**. Docs
  discourage `$skip`/`$top` (*"not formally implemented into the endpoints themselves"*) and recommend
  ID-first fetch then **50,000-row chunks, 4 parallel requests**. **[DOC]**
- **Rate limits unobserved and unpublished** — unknown at scale; production cadence stays conservative.
- **Eclipse provisioning fragility** — a `422 "No Firm is Associated with the user"` gap once required an
  admin to add the user. **Single point of failure: the pipeline goes dark if Andrew is de-listed.** The
  Eclipse-admin contact should be recorded; a dedicated service user is cleaner than the acts-as-Andrew posture.
- **Reverse-engineered and vendor-unsupported (S1/S2/S4):** a UI redesign breaks the pulls — re-investigation,
  not a ticket.

---

## 8. Completeness — and a correction the corpus made to itself

**Per D3 §14, Orion+Eclipse are `bounded-complete`, never catalog-complete.** Only a file-feed custodian
(Schwab) is catalog-complete; reverse-engineered API vendors have **an expansion frontier**, and the unified
engine must treat them that way.

> **THE CORRECTION, and it is exemplary.** D3 originally carried *"Orion and Eclipse publish no developer API
> catalog"* — a statement lifted from an `ADVI_ORIAPI.md` §1 remark about **Orion Connect** and applied to
> **Eclipse**. On 2026-07-16 it was **falsified for Eclipse**: Orion Eclipse publishes a full public **OpenAPI
> 3.0.3 catalog, 493 paths**, vendor-identity-verified (TLS, spec self-ID, authenticated spot-check
> byte-identical). **The amendment was written in place, with its scope explicitly bounded** — *verified for
> Eclipse only; whether Orion Connect publishes an equivalent is not yet verified either way, so the original
> statement stands for Connect pending its own check.*
>
> **RCN-0002 has now discharged that pending check for Connect: no public OpenAPI exists** — `/api/help`,
> `/swagger/v1/swagger.json` 404; `/api/index.html` is login-gated (**not authenticated**). *But the guide
> corpus at `developers.orionadvisor.com/guides/` is effectively public and carries real endpoint paths, JSON
> bodies and field names* — so "no catalog" was true, while "no documentation" was **not**.
>
> **The generalisable error: a premise true of one product carried onto a sibling because they share a brand.**

**Still `[NOT-RETRIEVED]`:** a complete endpoint census for Connect (RCN-0002 §4 is *a floor, not a census*) ·
`performance-breakdown`'s output shape · Eclipse **v2** (proven to exist by one guide URL; no spec) · Eclipse
`components.schemas` is **empty (0)**, so the spec alone gives no field-level models · Orion's
**transaction-level flow classification** — BD's affect vector remains our reference taxonomy.

---

## 9. Displacement verdict

| Layer | Displaceable? | How |
|---|---|---|
| Orion reporting (Envision saved-query) | **YES** | We already serve ADVI/MDPF off our own gold; the report engine adds nothing we don't rebuild |
| Orion custodian-aggregation (Assets snapshot, accounts, tax, billing) | **LOW–MEDIUM (consume)** | The cleanest surface we integrate; direct-custodian is the eventual owned path, Orion's snapshot is the interim **and the reference shape** |
| **Eclipse trade/rebalance** | **PARTNERSHIP, not self-build** | Consume read-side assignments/composition; **do not self-build active rebalancing in Phase 2** |

**Orion is the best-shape firm we integrate** — snapshot pass-through, clean REST, a thin transform. The
reporting/aggregation displacement is mostly *consolidation of what we already run cleanly*. The genuinely new
work is the owned trade/rebalance **decision** (a product choice, not an engineering estimate) and
generalizing per-day-snapshot ingest to direct-custodian.

---

## 10. Open items

1. **The Connect *product* surface has never been ingested** — we pull dimensions and a `performance_dim`, but
   the **method contract** (§5.1) and `Reporting/Scope` (§5.3) are unused. **We could be reading Orion's own
   performance under a declared methodology instead of only a precomputed `performance_dim`.** Worth a scoping
   conversation; it is not a build request.
2. **`Reporting/Scope` vs our `performance_dim` has never been reconciled.** Same question as BD Surface A × B:
   *do the two agree?* Assumed, not measured.
3. **Eclipse write-side enumeration** — needs a dedicated HAR of a rebalance action (`dc2-eclipse-*` briefs
   plan it). The build-vs-buy frontier.
4. **The Eclipse book is a GROWING SERIES, not a pin** — 0518: 842 portfolios/$199.7M, Opal slice 399/$93.6M;
   06-23 live: 855/$204.0M, Opal slice **467/$122.5M** (+68 / +$28.9M). **Andrew-corroborated as real
   migration**, not drift. Opal's share went ~47% → ~60% in ~5 weeks. **Model Opal-advised-AUA-off-inf as a
   time series, never a fixed figure.**
5. **Eclipse-admin contact unrecorded** (§7) — a live single point of failure.
6. **Brinson attribution + after-tax/tax-alpha** — new capabilities surfaced by RCN-0002, **proposals only**,
   requiring CTO scoping; after-tax should be scoped with OPAL_TAXSMA rather than invented separately.

---

## 11. Cross-reference

**Black Diamond:** [`MASTER_BLACK_DIAMOND_ANALYSIS.md`](MASTER_BLACK_DIAMOND_ANALYSIS.md).
**BD × Orion synthesis** (seven invariants):
[`docs/research/competitive_recon/orion_20260722/PLATFORM_STRUCTURE_COMPARISON_20260722.md`](../../../../docs/research/competitive_recon/orion_20260722/PLATFORM_STRUCTURE_COMPARISON_20260722.md).
**Engagement index:** [`../RECON_REGISTER.md`](../RECON_REGISTER.md) — RCN-0002.
