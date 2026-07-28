# PORTAL ROUTE CANONICALITY CENSUS — non-canonical namespaces, present/active assessment

**Author:** `0.2.0_DT_PortfolioAnalytics` · **Date:** 2026-07-28 ~18:4xZ
**Directed by:** Andrew, direct at my terminal ~18:30Z —
> "api/private/ should not even exist, my understanding is we only use api/general/ and api/scoped/ on a
> canonical basis, so you should be checking these out and listing any non-canonical routes for deprecation
> if they are really still present/active"

**Canonical basis (Andrew):** `/api/general/` and `/api/scoped/` ONLY.
**Scope:** census + deprecation assessment. **No fixes, no writes, no monitors, no route changes.**

---

## METHOD + DENOMINATOR (state it, do not imply completeness)

| plane | instrument | denominator |
|---|---|---|
| APPLIED (live) | `aws cloudfront get-distribution-config EVTSA9VEHNZVH` | **24 cache behaviors + 1 default**, enumerated in full |
| SOURCE (clients) | `grep` over `portal/src` `*.ts`/`*.tsx`, **live-vs-commented classified** | all matches, hand-classified |
| BEHAVIOUR (active) | unauthenticated `curl` probe per route | **6 probes** |

**Probe semantics:** `401 LambdaGeneratedResponse` = route live, edge-auth gated. `403` = reached origin,
denied. `200` = **serving unauthenticated.**
**NOT covered:** other distributions; non-portal clients (a route with no `portal/src` client may still have
a consumer I cannot see — **"no live client" is scoped to `portal/src`, not to the world**).

---

## RESULT — 5 NON-CANONICAL ROUTE FAMILIES LIVE ON THE DISTRIBUTION

| # | behavior | origin | live probe | live clients in `portal/src` | disposition |
|---|---|---|---|---|---|
| 16 | `/json-tiered/*` | S3 portal-v2-json | **200 UNAUTH** | **0** | **DEPRECATE — priority** |
| 23 | `/api/partners` | APIGateway-portal | 401 | **0** (docstring only) | **DEPRECATE** |
| 20 | `/v1/*` | APIGateway-portal | 401 | **1** | migrate, then deprecate |
| 18 | `/api/private/portfolio*` | APIGateway-portfolio | 401 | **11** | **CANNOT deprecate yet** |
| 19 | `/api/private/*` | APIGateway-portal | 401 | **3** | **CANNOT deprecate yet** |

Canonical `/api` behaviors: **18**. Also non-canonical-by-prefix but out of Andrew's framing: `/auth/*`
(behavior 21, the login path).

---

## FINDING 1 — `/json-tiered/*` IS AN UNAUTHENTICATED TWIN OF AN AUTH-GATED CANONICAL ROUTE

**The same object, two routes, two auth postures:**
```
/json-tiered/market-overview/rsi-summary.json                200  Miss from cloudfront   <-- NO AUTH
/api/general/json-tiered/market-overview/rsi-summary.json    401  LambdaGeneratedResponse
```
The 200 returns **real data**, verified by reading the body:
`{"generated_at":"2026-07-28T13:24:40.759530Z","data_as_of":"2026-07-27","tier":1,...}`

**Mechanism:** behavior 15 (`/api/general/json-tiered/*`) carries `auth-validator-edge` + the
`public-data-router`; behavior 16 (`/json-tiered/*`) points at the **same S3 origin with neither**.

**EXPOSURE BOUNDARY — measured, 5 probes:**
```
/json-tiered/market-overview/rsi-summary.json          200
/json-tiered/market-overview/summary/all-returns.json  200
/json-tiered/market-overview/details/AAPL.json         403
/json-tiered/mdpf/global/aggregate-aua-timeseries.json 403
/json-tiered/portfolios/non_model_assets.json          403
/json-tiered/portfolios/aum-metrics.json               403
```
> **NOT A CLIENT-DATA EXPOSURE.** MDPF and portfolios keys are **403** — no AUM, holdings, or client data is
> reachable this way. Exposure is bounded to objects literally stored under a `json-tiered/` prefix, i.e.
> market-overview tier-1 summaries. **I am stating the bound because an unbounded claim here would be a
> false alarm of exactly the kind that costs credibility.**

**Why it is still a real finding:** the canonical twin **requires auth for the identical bytes**. Either the
auth on behavior 15 is unnecessary, or behavior 16 is a bypass of it — **both cannot be right**, and nothing
in `portal/src` calls the bare form. A route with **zero clients and a weaker auth posture than its own
canonical twin** is the cleanest possible deprecation candidate.
*(The app fetches these via `publicApiRequest` on the CANONICAL path, suggesting the data is intended
public — which would make behavior 15's auth the anomaly rather than 16's absence. **That is an architecture
call, not mine.** Either way one of the two routes should not exist.)*

## FINDING 2 — `/api/partners` IS ORPHANED, AND ITS CANONICAL TWIN ALREADY EXISTS
Behavior 23 `/api/partners` is live (401). Its only appearance in `portal/src` is a **docstring**
(`api/endpoints/advisor-intelligence.ts:8`, `GET /api/partners - List partners`). **Canonical
`/api/scoped/partners/*` exists as behavior 22.** Deprecate 23; confirm no non-portal consumer first.

## FINDING 3 — `/api/private/` IS **NOT** DEAD, AND I CORRECTED MYSELF ON THIS
> ⚠ **I initially reported to Andrew that `/api/private/` appeared commented-out. That was WRONG** — it came
> from reading only the MDPF-adjacent call sites, which ARE commented. A full classified sweep found
> **14 LIVE (uncommented) call sites.** Recording the correction because the wrong version would have
> licensed deleting a live feature's backend.

**LIVE — Portfolio Management, 11 sites** (`api/endpoints/portfolio.ts`, `portfolio-optimization.ts`):
`/api/private/portfolio/{parse-pickle,autosave,optimization-autosave,export-and-submit,exports,versions,funds}`,
`/api/private/portfolio-management`.
**LIVE — 1 site:** `portal-proxy.ts:296` `/api/private/portfolios/aum-flows.json`.

**ALREADY MIGRATED (commented, evidence of a deliberate prior migration):**
`/api/private/portfolios/{aum-summary,aum-timeseries,aum-metrics,account-distribution}.json` → now served
from `/api/general/`. `portal-proxy.ts:356-357` states the rationale verbatim:
> `// prior DEMO comment + TODO to move to /api/private/ removed — the general`
> `// endpoint is now auth-gated at CF layer, equivalent protection to /api/private/.`

**So the `/api/private/` → `/api/general/` migration is REAL, PRECEDENTED, and PARTIALLY COMPLETE.** What
remains is Portfolio Management, which is a distinct feature with its own API Gateway origin
(`APIGateway-portfolio`, behavior 18) — **a larger migration than the MDPF one, not a cleanup.**

## FINDING 4 — `/v1/*` HAS EXACTLY ONE CLIENT
`portal/src/api/endpoints/sentiment.ts:798` → `/v1/sentiment/keyword-intelligence`. Live (401). Single
call site; migration to `/api/scoped/` looks cheap but I have not costed the backend side.

---

## RECOMMENDED DEPRECATION ORDER (recommendation only — routing is CTO's)

1. **`/json-tiered/*` (16)** — zero clients, weakest auth posture, resolves an auth inconsistency. **Confirm
   no non-portal consumer**, then remove.
2. **`/api/partners` (23)** — zero clients, canonical twin already live.
3. **`/v1/*` (20)** — one client; migrate `sentiment.ts:798` to `/api/scoped/`, then remove.
4. **`/api/private/*` + `/api/private/portfolio*` (19, 18)** — **NOT a cleanup.** Requires migrating the
   Portfolio Management feature (12 of 14 call sites) off `APIGateway-portfolio`. **Its own project.** The
   MDPF-side migration is already done and is the working precedent.

## RESIDUAL / WHAT THIS DOES NOT ESTABLISH
- **"Zero live clients" is scoped to `portal/src`.** A non-portal consumer (script, integration, another
  app) would be invisible here. **Confirm before removing any behavior** — a removed route with an unknown
  consumer is an outage.
- Behavior **ORDER** is precedence-bearing on CloudFront; I enumerated but did **not** analyse whether
  removing one changes which behavior a path falls through to. **That analysis is required before any
  removal** and I have not done it.
- I did not probe `/auth/*` or the default `/*`.
- **6 probes total.** Not a sweep of every key under any namespace.
