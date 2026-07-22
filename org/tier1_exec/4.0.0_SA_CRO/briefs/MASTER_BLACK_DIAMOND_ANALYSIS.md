# MASTER BRIEFING — Black Diamond (SS&C / Advent)

**Author / owning agent:** `4.0.0_SA_CRO` — Chief Research Officer
**Status:** Living master briefing. Consolidates **every** Black Diamond analysis in the Opal corpus.
**Date:** 2026-07-22 · **Commissioned:** Andrew-direct — colocate all BD research and write a master analysis
covering architecture, endpoints, methodologies.

> **HOW TO READ THIS.** This is a **consolidation with pointers**, not a copy. Source documents stay at their
> canonical paths and remain authoritative; duplicating a 250-line spec into a second location is how a
> corrected doc later disagrees with its own copy. Every section names its source. Where sources **disagree**
> or where one **corrected** another, that is stated (§9) rather than smoothed.
>
> **EVIDENCE GRADES:** **[HAR]** captured response bodies · **[PROD]** grounded in code we run in production ·
> **[LIVE]** verified against live BD · **[DOC]** vendor documentation · **[INFERENCE]** labelled as such.
> **`[UNOBSERVED]` is not absence** — it means our captures never exercised it.

---

## 1. The single most important structural fact

**Black Diamond exposes TWO ENTIRELY SEPARATE API SURFACES, and Opal's corpus reached them from opposite
directions. Until this briefing they had never been described side by side.**

| | **Surface A — DataMining** | **Surface B — the Wealth Platform product APIs** |
|---|---|---|
| What | Persisted-query + async-execution + xlsx export, over a star schema | The APIs BD's own web app calls to render the advisor/client experience |
| Base | `*.bdreporting.com/datamining/...`, `/Api/DataMining/ExportResults/...` | ~15 domain services behind the `bd3.bdreporting.com` gateway |
| Auth | `.bd.identity` OIDC **cookie jar** + a per-run **Bearer** minted from it | Per-service short-lived JWT from `/{service}/auth/token` + `/auth/keepalive` |
| Grain | Template → levels → facts; leaf sets row grain | Resource endpoints returning nested analytic structures |
| **Opal uses it** | **YES — this is how we ingest Cottonwood today** | **No — we consume none of it** |
| Our source | D2 + D2b **[PROD/LIVE]** | RCN-0001 **[HAR]** |

**Why it matters.** Surface A is an *operational extract* API — it is how you get the book of record out.
Surface B is the *product* — performance, allocation, cost basis, activity, net worth as BD computes them for
its own screens. **A replacement effort needs Surface B's semantics (what the numbers mean) and Surface A's
mechanics (how bulk data moves).** Judging BD from either alone gives a distorted picture: Surface A looks
like a reporting warehouse; Surface B looks like an analytics engine. It is both.

---

## 2. Corpus manifest — every BD source, and what each is good for

### 2.1 Primary architecture + endpoint specs

| Source | Author / vintage | Grade | What it uniquely gives |
|---|---|---|---|
| [`docs/architecture/DATA_PLATFORM_D2_BLACK_DIAMOND_ARCH_SPEC.md`](../../../../docs/architecture/DATA_PLATFORM_D2_BLACK_DIAMOND_ARCH_SPEC.md) | `0.4.0_DS_ClientPlatform`, CTO-gated 2026-06-26 (session-locality corrected 07-08) | **[PROD/LIVE]** | The DataMining flow, auth/session model, the template/level/fact star, the 5-table catalog, **the snapshot-vs-lots-FIFO methodology thesis** |
| [`docs/briefs/data-platform-d2b-bd-rest-endpoint-catalog-20260708.md`](../../../../docs/briefs/data-platform-d2b-bd-rest-endpoint-catalog-20260708.md) | 2026-07-08 | **[LIVE]** | REST endpoint + payload catalog; **6 confirmed query types incl. the real billing type**; a-la-carte querying; a **second billing surface** at `billing.bdreporting.com` |
| [`docs/research/bd_dashboard_teardown/BD_DASHBOARD_HAR_TEARDOWN_20260721.md`](../../../../docs/research/bd_dashboard_teardown/BD_DASHBOARD_HAR_TEARDOWN_20260721.md) | **RCN-0001**, 2026-07-21 | **[HAR]** | The **product** surface: 15 services, 229 endpoints, 52 captured schemas, the performance engine, the affect vector, `firm/globalsettings` |
| [`docs/research/bd_dashboard_teardown/BD_REPLACEMENT_ROADMAP_20260721.md`](../../../../docs/research/bd_dashboard_teardown/BD_REPLACEMENT_ROADMAP_20260721.md) | **RCN-0001** | plan | Tiered replacement program (A→D), workstreams, decisions D1–D6 |
| [`docs/research/bd_dashboard_teardown/FACT_ACCOUNT_RETURN_BUILD_SPEC_20260721.md`](../../../../docs/research/bd_dashboard_teardown/FACT_ACCOUNT_RETURN_BUILD_SPEC_20260721.md) | **RCN-0001** | spec | The unifying `fact_account_return` build spec (HELD at CTO D6) |
| [`docs/architecture/COTETL_METHODOLOGY_THESIS.md`](../../../../docs/architecture/COTETL_METHODOLOGY_THESIS.md) | DS | **[PROD]** | The snapshot-first doctrine in its own right |
| [`docs/architecture/ADVI_COTETL.md`](../../../../docs/architecture/ADVI_COTETL.md) + `ADVI_COTETL_AUAFIX_PRD.md` | DS/COO | **[PROD]** | The cot ETL contract the DataMining pulls feed |

### 2.2 Operational findings worth knowing before you design anything

| Source | The finding |
|---|---|
| `docs/briefs/bd-unrealized-export-500k-row-cap-finding-20260709.md` | **A hard export row cap** — bulk extraction is not unbounded |
| `docs/briefs/bd-account-type-filter-semantics-decision-20260709.md` | Account-type filter semantics — a classification trap |
| `docs/briefs/cot-bd-table-endpoint-crossref-20260608.md` | Table ↔ endpoint cross-reference |
| `docs/briefs/cot-bd-pipeline-deepdive-medallion-port-plan-20260608.md` | Medallion port plan for the cot BD pipeline |
| `bd-49f-ec2-scrape-to-datamining-api-migration-20260625.md` | **The migration from UI scraping to the DataMining API** — why the API path exists |
| `bd-49f-durable-auto-auth-cv-login-otp-relay-20260625.md`, `bd-49f-auto-login-durable-hardening-audit-20260702.md`, `cot-durable-auto-auth-parallel-of-bd-49f-20260625.md` | The durable auto-auth / OTP-relay story — the hardest operational problem in the whole integration |
| `bd-silver-schema-drift-rca-2026-01-27.md` | Schema drift RCA — the vendor changes shapes under you |
| `bd-49f-allocations-retry-net-design-20260630.md` | Allocations retry/net design |
| `gldinc-bd-gold-loader-shape-nondeterminism-census-20260611.md` | Loader shape non-determinism |

*(Also present and deliberately not folded in: BD **cost/rightsizing** briefs — `nfra-costaws-r3-*`,
`nfra-costred-r2-*`, `bd-gold-rightsize-analysis-*`, `bd-gold-memory-diagnostic-*`. These are Opal
infrastructure economics, not BD platform analysis.)*

---

## 3. Architecture

### 3.1 Surface B — the product (RCN-0001, **[HAR]**)

**~15 domain backends behind a gateway** (`bd3.bdreporting.com`), each reached with a per-service short-lived
JWT minted at `/{service}/auth/token`, with `/auth/keepalive` heartbeats. Real-time rides **SignalR**.

`portfolioreporting` (THE analytics engine) · `networth` · `account-api` · `portfolio-api` ·
`relationship` (CRM) · `schema-api` (**classification + benchmarks + targets** — the reference-data moat) ·
`billing` · `user-api` · `firm-api` · `ix` (Investor Experience) · `timeline` · `docs` ·
`rebalancer` · `datamanagement` · `broadcast/alerts/bulk/platform`.

**The separability is the strategic gift:** the client-visible analytics can be replaced without touching CRM,
the rebalancer, or the portal.

### 3.2 Surface A — DataMining (D2, **[PROD]**)

A **persisted-query + async-execution + export-download** API:

```
GET  /datamining/auth/token                       (Cookie jar) -> {access_token}   # opaque, short-lived
POST /datamining/request/v1/run  {template,asOfDate}  (Bearer)  -> {templateId(runId), resultGuid}
GET  /datamining/request/v1/run/{runId}/status        (Bearer)  -> {statusMessage, isComplete}   # poll
GET  /Api/DataMining/ExportResults/{resultGuid}   (Cookie jar)  -> xlsx bytes
```

**The two-credential split is load-bearing:** catalog/template ops and run-execution authorize via the
**Bearer**; the binary export authorizes via the **cookie jar**.

**A run does not stream rows** — it materializes a server-side result identified by `resultGuid`, which the
export endpoint serves as xlsx (`Sheet1` = data, `Timestamps` = the canonical as-of metadata sheet).

> **Operational trap worth carrying into any design:** BD sets `statusMessage='Error'` **with
> `isComplete=False`** on a failed run — polling `isComplete` alone hangs for the full timeout. **An error
> state that is not a completion state is a design others will reproduce by accident.**

### 3.3 The dimensional spine — and how the two surfaces agree

Surface A exposes the star top-to-leaf **[PROD]**:

```
Team -> Relationship -> [Portfolio Group] -> Portfolio -> Account -> Holding -> Tax Lot
```

Surface B independently shows **Relationship → Portfolio → Account** with holdings and lots beneath **[HAR]**.
**Two independent reads of the same book of record agree** — D2 simply sees more of it, because the query API
exposes `Team` at the top and `Tax Lot` at the leaf, which the product screens do not surface as levels.
**This is the entity model to replicate.**

---

## 4. Endpoints

### 4.1 Surface A — the 5 (of 6) query types we run **[PROD]**

| Table | qt | Levels | Dims | Measures | Leaf grain | Key measures |
|---|---|---|---|---|---|---|
| holdings | 1 | server-side | — | — | Account × Holding (snapshot) | Market Value, Units (Ending MV, `activityOptionId=1`) |
| transactions | 2 | 5 | 63 | 5 | Transaction | Units, MV, Transaction Fee, Income, Account Fee |
| realized | 3 | 8 | 209 | 7 | Tax Lot (closed) | Cost Basis, Proceeds, ST/LT G/L, Total G/L |
| unrealized | 4 | 8 | 208 | 11 | Tax Lot (open) | Cost Basis, Amortization, MV, ST/LT G/L |
| allocations | 5 | 4 + alloc levels | 62 | 1 | Account (rollup) | Market Value |
| **billing** | **6** | — | — | — | — | **D2b: a real billing query type exists** — the first-pass "no billing type" verdict was **wrong** |

**Thin envelope vs persisted body — the key architectural fact.** Local template JSONs carry only
`{templateId, queryTypeId, dateRangeType, startDate, endDate, name, comment}`. **The full dimension/level/fact
selection lives SERVER-SIDE** and materializes only at runtime via `GET /datamining/request/v1/template/{id}`.
You refine a query by **re-persisting the template, not by changing code** — the data shape stays a contract.

### 4.2 Surface B — the analytics engine **[HAR]**

`portfolioreporting/api/`:
- **`performance/performancePeriod`** — `beginningMarketValue`, `endingMarketValue`, `netGains`,
  `netAdditions`, `fees`, `income`, **`timeWeightedReturns{return, returnAnnualized,
  contributionOfReturnToParent, contributionOfReturnToTotal}`**, **`moneyWeightedReturns{return}`**,
  `benchmarks[]{benchmarkId, return, difference}`, `daysHeld`, `periodLength`,
  **`performingBmv/Emv` vs `positionOnlyBmv/Emv`**. Nested Portfolio→Class→Segment→Asset.
- **`performance/performanceSeries`** — the daily arrays behind the chart, incl. cumulative benchmark series.
- **`activitySummary/star`** (+`/chart`, `/transactionDetails`) — the return "GL": contributions, withdrawals,
  netAdditions, fees, feeRebates, expenses, gainLoss, costBasisRgl, marketRgl, marketUgl, appreciation,
  storedAdditions/Withdrawals/Income, netContributions, contraContributions, intraPortfolioFlows.
- `allocation` (+ `/target` with tolerance bands) · `costBasis` (realized/unrealized × ST/LT, unit cost,
  amortization, paydown factor) · `income/fixed` + `income/projected` · `capitalmarkets` (benchmark library
  across 75 named ranges) · `transactions/star` · `alternativeInvestments` (IRR).
- `networth/api/balancesheet` — assets vs liabilities incl. held-away.
- `schema-api/*` — SuperClass/Class/Segment, benchmarks, targets **(bodies not captured — the moat)**.

---

## 5. Methodologies — how BD actually computes

### 5.1 The method contract, exposed verbatim **[HAR]**

`request/api/firm/globalsettings` returns:
`performanceReturnCalc: NetOfFees` · `marketValueCalc: Accrued` · `defaultAccrualMethod: Account365` ·
`returnType: Annualized` · `benchmarkType: ClassSpecific` · `managementFeeOption: GainLoss` ·
`defaultDateRange: QuarterToDate` · `defaultTaxLotMethod: FIFO`.

**This is `dim_return_method`, written down by the incumbent.** It is the basis of Andrew's defensibility
steer (2026-07-21): *"I like the BD approach because its defensible to refer to."* Standing consequence — the
**METHOD-vs-NUMBERS split**: method aligns to BD because it is defensible to refer to; **numbers are always
computed and validated on our own data.** BD is a reference and a parity oracle, never a source of figures.

### 5.2 The transaction "affect vector" — the cash-flow taxonomy **[HAR]**

Every transaction carries signed affects:
`externalFlow / incomeAffect / cashAffect / unitAffect / advisorFeeAffect / accrualAffect`, plus
`transactionReportingType` and a `fileCode` encoding the tuple — e.g. `Cash Withdrawal (-1,0,0,0,0,-1)`.

**This is the exact taxonomy `2.0.0_SA_COO~A` independently reconstructed by hand** from Schwab `sb_cd`
descriptions. Two independent derivations converging is the strongest signal in the whole BD corpus, and it
makes BD's crosswalk a ready-made **parity oracle** for our own classifier.

### 5.3 Snapshot-first vs lots-FIFO — the doctrine **[PROD]**

BD exposes **both** accounting views:
- **Snapshot** (qt1): canonical position value per account/holding/day, delivered directly. *This IS the book
  of record value.*
- **Lot-level** (qt3/qt4): tax-lot-grained — `Open Date`, `Unit Cost`, `Inherited Date`, `Is Wash Sale`, with
  BD computing cost basis, proceeds and ST/LT G/L **at the lot**. The lot-relief method (FIFO/avg/spec-ID) is
  resolved **inside BD**; we consume resolved rows and do not re-run relief.

> **THE DOCTRINE, and it was learned the hard way: read daily value from the SNAPSHOT; do not reverse-engineer
> it from the transaction/lots chain.** Wiring Cottonwood through 49F's lots-FIFO value path
> **corrupted 40.2% of rows to $0** and froze served AUA until the 2026-06-22 re-wire. A snapshot legitimately
> has **no lot lineage** — an empty lots chain there is *correct, not a defect*.
>
> **Andrew's forward direction:** use BD `Assets_Dim` (qt1) as the daily-value mechanism directly, and once
> proven on cot, retrofit 49F to snapshot-native going forward — keeping reverse-engineering only for 49F's
> pre-snapshot history.

**This is the most valuable single idea in the BD corpus** and it generalises: D3 shows Orion's per-day Assets
snapshot is the same shape and the same win.

### 5.4 What a replacement must own, hardest first **[PROD]**

1. **Custodian feed ingestion + reconciliation** — multi-custodian normalization + break resolution. Hardest.
2. **Tax-lot accounting** — lot relief, wash sales, cost basis across corporate actions.
3. **The dimensional book of record** — the Team→…→TaxLot star. A modeling task; our silver/gold already
   materializes a comparable star.
4. **The query/export surface** — the thinnest layer.

**The snapshot-first thesis means we do NOT need (2) to own daily VALUE** — only to own gains and tax detail.

---

## 6. Auth — and a correction the corpus made to itself

- **Root credential = the `.bd.identity` OIDC session cookie jar**, captured by an interactive Playwright
  login on the exporter EC2 and stored in Secrets Manager (`blackdiamond/cot/session`).
- **The FULL jar is required for `v1/run`** — `.bd.identity` alone suffices for catalog/template GETs, but
  run-execution needs the antiforgery + idsrv session cookies.
- **The Bearer is minted per-run** and is opaque and short-lived. Mint fresh; do not cache off-box.
- **Session TTL is SHORT (~30–60 min effective)** — the `cf_bm` bot-management cookie plus idsrv idle gates
  the practical window, **not** the longer nominal `expires_at`.
- **Firm isolation is structural:** per-partner secret, bucket and firm-id, with the bronze runner failing
  closed if a firm-id is set without its own bucket.

> **A CORRECTION THE CORPUS MADE TO ITSELF, and it is the model for how these records should behave.**
> D2 originally stated the BD session was **IP-bound** to the exporter box. On 2026-07-08 an off-box test
> proved **querying is NOT IP-bound** — `auth/token`, `template/{id}` and template-list all return 200 off-box
> with a valid session, and there is **zero IP-checking code** in either script. The original claim was *"a
> confounded inference from a single 2026-06-09 incident (its own memory flagged 'suspected own-goal, never
> confirmed')"*, conflated with the real short-TTL constraint. **What is genuinely on-box is the interactive
> LOGIN** — it has real bot detection (`cf_bm`) and needs a browser context.
> **The lesson generalises: an operational constraint that everyone repeats is not thereby verified.**

---

## 7. Known operational limits — design against these

- **Export row cap** — a hard ceiling on unrealized exports; bulk extraction is bounded (`bd-unrealized-export-500k-row-cap-finding-20260709.md`).
- **`statusMessage='Error'` with `isComplete=False`** — an error that is not a completion (§3.2).
- **qt5 relationship MV double-counts rep-split rows (~2×)** — silver/gold **must** dedup before any
  relationship rollup. A known dedup requirement, **not** a BD defect to replicate.
- **Snapshot tables return the END-date snapshot regardless of window width** — so a 14-day window is a
  holiday-gap floor, not a restatement lookback. For transactions/realized the window *is* BD's ~14d
  restatement lookback. **The same parameter means two different things depending on the table.**
- **Schema drift is real** (`bd-silver-schema-drift-rca-2026-01-27.md`) and surfaces as a 400 or a shape change.
- **A second billing surface exists** at `billing.bdreporting.com`, distinct from the DataMining billing query
  type (D2b §6).

---

## 8. Completeness basis — what "we know BD" actually means

**BD publishes no developer API catalog.** Both surfaces are **reverse-engineered, vendor-unsupported**. Per
D2 §14's framing, BD is **bounded-complete**, never catalog-complete:

- **Surface A:** bounded by the templates we persist + the live-enriched template dump. `holdings` (qt1) is
  **envelope-only locally** — its full selection lives server-side and the catalog row is **PENDING a live
  on-box dump**.
- **Surface B:** bounded by what the 2026-07-21 walk exercised — 1,136 API calls / 229 endpoints / 52 captured
  schemas, with **5 endpoint families explicitly `[BODY-NOT-CAPTURED]`** (classification tree, benchmark
  library, security master, rebalancer models, billing config).

**A UI redesign breaks the pulls.** That is a re-investigation, not a ticket.

---

## 9. Where sources disagree, and what is still open

**Corrections already absorbed** (recorded, not silently overwritten): session IP-binding **falsified** 07-08
(§6); "no billing query type exists" **falsified** 07-08 (§4.1).

**Open:**
1. **qt1 holdings full catalog** — needs the on-box live-enriched template dump (D2 §7). *The one gap in the
   Surface-A catalog.*
2. **The 5 `[BODY-NOT-CAPTURED]` families** on Surface B — the classification tree and benchmark library are
   **the moat**, and we have their endpoint names but not their schemas.
3. **`fact_account_return` remains HELD** at CTO's D6 registration, post-MDPF-flip. Open at Andrew: D1
   (Account365 method pin), D2 (classification build-vs-license).
4. **Surface A × Surface B reconciliation is UNTESTED** — nobody has verified that a value read via
   DataMining qt1 equals the same account's value on `performancePeriod` for the same date. **They should
   agree; that is an assumption, not a measurement.** Cheap to test and worth doing before we treat BD as a
   parity oracle for `fact_account_return`.

---

## 10. Cross-reference

**Orion/Eclipse:** [`MASTER_ORION_ECLIPSE_ANALYSIS.md`](MASTER_ORION_ECLIPSE_ANALYSIS.md).
**The BD × Orion structural synthesis** — the seven invariants both vendors arrived at independently:
[`docs/research/competitive_recon/orion_20260722/PLATFORM_STRUCTURE_COMPARISON_20260722.md`](../../../../docs/research/competitive_recon/orion_20260722/PLATFORM_STRUCTURE_COMPARISON_20260722.md).
**Engagement index:** [`../RECON_REGISTER.md`](../RECON_REGISTER.md) — RCN-0001.
