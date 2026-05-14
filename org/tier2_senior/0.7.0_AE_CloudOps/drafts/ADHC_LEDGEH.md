# ADHC_LEDGEH — Lambda@Edge Defense Envelope Hardening
**PRD v0.2 — 0.7.0_AE_CloudOps — 2026-05-14 ~17:05Z**

> **v0.2 changelog (post CTO architectural ratify 16:55Z):** Option A (origin-response L@E with structured JSON error envelope) **LOCKED** per CTO Q2 ratify. Scope **NARROWED** per CTO Q3 to artifact-class (`*.json`) paths only; SPA deep-link cleanup deferred to separate ADHC candidate. CTO Q1 confirmed structurally novel — no existing primitive in codebase. CTO Q4 confirmed zero overlap with DE 0.4 `cb62f069` — clean defense-in-depth pair (DE: prevent persistence of cache poison; LEDGEH: prevent storage entirely at wire boundary). Project sister to INFGRO.004 NaN-strip pattern (FE strip + DS-side `allow_nan=False` tripwire) per CTO framing. FIRMSEP.10 Cottonwood live-ship surfaced as primary risk-window beneficiary; Cottonwood is the "why-now" anchor.

**PRD v0.1 — 0.7.0_AE_CloudOps — 2026-05-14 ~16:55Z** (architectural fork explicit; CTO review pending)

> Authored post 2026-05-14 P1 RCA: Inflection Segment Analytics Annual interval renders "Analytics data unavailable" while monthly + quarterly render partially-correctly. Root-cause chain converged on a toxic primitive at the L@E / CloudFront boundary: `custom_error_response` collapses S3 NoSuchKey / NoSuchBucket / Forbidden into the SPA HTML index payload, which React Query's `JSON.parse` swallows silently and stores as `data: null` for `staleTime` (5 min). DE 0.4 brief `e70fb243f` + DE 0.4 cache-poisoning hypothesis (filed `memory/feedback_react_query_cache_poisoning_from_deploy_window.md`) + AE 0.7 Phase 1.1 CloudWatch evidence (0 L@E errors in 8h; 0 partner_analytics requests in Andrew's 12:15-12:25Z test window) converge on this PRD as the structural defense-in-depth complement to DE 0.4's targeted FE fix `cb62f069` (drop `refetchOnMount: false` on the demonstrated-poisoning useQuery).

---

## §1 — Scope

Replace the toxic primitive — CF `custom_error_response` collapsing S3 / L@E failure into SPA HTML for artifact-class (`.json`) URLs — with a structured JSON error envelope that React Query and any other JSON consumer can parse without silent null-cache poisoning.

**In scope:**
- L@E hardening at the origin-response boundary for the `shared-advisor-router` CloudFront behavior (`/api/scoped/advisor-intelligence/*`)
- CloudFront `custom_error_response` config refinement: HTML paths preserve current SPA-deep-link behavior; JSON-artifact paths emit structured error envelope
- Empirical regression suite using today's P1 chain as the anchor: a wrong-firmId deploy reproduction must yield parseable JSON error, not HTML
- Cross-reference with DE 0.4 FE fix `cb62f069` to verify the React Query `apiRequest` error contract receives the structured envelope correctly (HTTP non-2xx + parseable JSON body → React Query `error` state, not silent `null` cache)

**Out of scope:**
- DE 0.4 FE-side cache-bust hardening (`refetchOnMount: false` removal, `staleTime: 0` on error, `queryClient.invalidateQueries` on auth) — covered under DE 0.4's own lane
- Other CloudFront distributions outside `portal-auth/cloudfront-distribution.tf` (trade-pipeline, analytics-dashboard) — each may have its own custom_error_response config; orthogonal hardening surfaces if requested
- `auth-validator-edge` viewer-request hardening (it sets X-Firm-Id; this PRD targets the origin-response / artifact-fetch boundary)
- Replacing the SPA-deep-link mechanism wholesale (separate scope; `custom_error_response` is the de facto SPA fallback today and Phase 1 of this PRD preserves it for HTML paths)

**Non-goals:**
- Refactoring `shared-advisor-router` URI-rewrite logic (working; just adding error-envelope behavior)
- Changing CloudFront cache key composition (orthogonal; covered under ADVI_FIRMSEP.06)
- Migrating from CloudFront to API Gateway (out of architectural scope for this hardening pass)

---

## §2 — Existing State

### 2.1 — The toxic primitive (CF custom_error_response global collapse)

`infra/aws/terraform/portal-auth/cloudfront-distribution.tf:623-637`:

```hcl
# --- Custom Error Responses (SPA routing — return index.html for 403/404) ---

custom_error_response {
  error_code            = 403
  response_code         = 200
  response_page_path    = "/index.html"
  error_caching_min_ttl = 0
}

custom_error_response {
  error_code            = 404
  response_code         = 200
  response_page_path    = "/index.html"
  error_caching_min_ttl = 0
}
```

**Behavior:** EVERY 403 + 404 from any cache behavior under this distribution is rewritten to `/index.html` with HTTP status `200`. This is the SPA-deep-link fallback — it works for routes like `/portal/advisor-intelligence` that the SPA owns client-side.

**Failure mode for JSON artifacts:** When `shared-advisor-router` (origin-request L@E) rewrites a request to a bucket+key that doesn't exist (e.g., wrong firm bucket from a pre-deploy URL-shape bug), CloudFront fetches from S3, receives `NoSuchKey` / `NoSuchBucket` / `403 AccessDenied` (depending on bucket policy + OAI state), and applies `custom_error_response` → returns `/index.html` content as 200. React Query's `apiRequest` receives an HTTP 200 with `Content-Type: text/html` body `<!doctype html>...` and pipes it to `JSON.parse`, which throws. React Query treats the parse error as a fetch failure and stores `data: null` under the queryKey for `staleTime` (default 5 min in this codebase).

### 2.2 — Empirical anchor (2026-05-14 P1)

| Wire-level fact | Evidence |
|---|---|
| 0 L@E errors in 8h window | AE 0.7 `.runtmp/ae07_cw_interval_compare.py` filter `?ERROR ?WARN ?failed ?denied` returned 0 matches across 8 hours |
| Quarterly: 78 successful unique requests + steady cadence | Same CW pull, `partner_analytics_quarterly` filter |
| Monthly + Annual each fire ONCE late-day, succeed | 13:07Z Annual + 15:57Z Monthly |
| Andrew test window 12:15-12:25Z: 0 partner_analytics events of ANY interval | Same CW pull, broad `partner_analytics` filter; zero matches in that window |
| Same firmId `opal-capital` flips bucket between 12:31Z (opal-data-bd) and 13:07Z+ (opal-data-inf) | Partner-switcher context-flip visible at L@E rewrite log line |

DE 0.4 cache-poisoning hypothesis (filed today, memory entry `feedback_react_query_cache_poisoning_from_deploy_window.md`):
- Pre-`17b3dad7` (~14:00-14:54Z), portal sent `?firm=49financial` / `?firm=inflection` to `shared-advisor-router`
- Real S3 buckets are `opal-data-bd` / `opal-data-inf`
- L@E constructed `opal-data-${firmParam}` → `opal-data-49financial` → NoSuchBucket → CF custom_error_response → SPA HTML → `JSON.parse('<!doctype...')` fails → React Query cached `null`
- Post-`17b3dad7` fix (`bucketSuffix(firmOverride)`) routes correctly
- But React Query cache key is `[name, granularity, firmOverride]` — doesn't include URL shape — so stale null entries from the bad-deploy window persisted for `staleTime`
- Quarterly recovered because `AuthContext.tsx:38` prefetches it at auth time post-fix; Monthly + Annual only fetch on user toggle → returned cached null at Andrew's 12:17Z test

**This is exactly the failure class the toxic primitive enables.** The pre-fix URL shape was wrong (legitimate engineering bug). The cache poisoning would have surfaced LOUD with a structured JSON error envelope; instead it surfaced SILENT and persisted across the deploy.

### 2.3 — `shared-advisor-router` origin-request L@E (current behavior)

`infra/aws/lambda-edge/shared-advisor-router/index.mjs`:
- Fires on origin-request trigger (BEFORE S3 lookup)
- Reads `X-Firm-Id` from auth-validator-edge viewer-request injection
- Branches on opal-capital staff (?firm= param) vs partner firmId (FIRM_BUCKET_MAP) vs unmapped (`opal-data-${firmId}` fallback — Cottonwood pre-onboarding sentinel)
- Mutates `request.origin.s3.domainName` + `request.headers.host` to point at the firm bucket
- Logs `Firm routing: firmId=... bucket=... uri=...` and returns the rewritten request

**Cannot see the S3 response.** Origin-request fires BEFORE the S3 fetch; origin-response fires AFTER. To intercept S3 NoSuchKey / NoSuchBucket / 403, either:
1. Add a new **origin-response L@E** (cleanest in code; new Lambda + new CF behavior wiring)
2. Refine **CloudFront `custom_error_response`** config to scope to HTML paths only (cleanest in infra; single Terraform change)

Both options are viable; tradeoffs in §3 + §7.

---

## §3 — Target Architecture

### 3.1 — Architecture (Option A LOCKED per CTO 16:55Z)

**Origin-response L@E (Option A; CTO Q2 ratify).** New Lambda `shared-advisor-router-response` at `infra/aws/lambda-edge/shared-advisor-router-response/index.mjs`. Trigger: `origin-response`. Behavior: inspect `response.status` after S3 fetch; if `response.status` is `403`/`404` AND request URI matches an artifact pattern (`/api/scoped/*` AND extension `*.json`), replace the response body with a structured JSON envelope and preserve HTTP status (404 stays 404; do NOT pin to 200) with `Content-Type: application/json` + `Cache-Control: no-cache`. CF `custom_error_response` continues to fire on HTML routes (SPA deep-link preserved).

**CTO Q2 reasoning verbatim:**
> Viewer-request L@E (shared-advisor-router) handles route/firm-bucket logic BEFORE the S3 fetch happens; it doesn't see the S3 error code. For your proposal to intercept NoSuchKey/NoSuchBucket at L@E level, you need fire-after-S3-fetch = origin-response L@E. Architecturally cleaner separation: viewer-request = request routing logic; origin-response = fetch-result transformation. Mixing them in viewer-request would mean viewer-request makes the S3 HeadObject call directly (unusual + adds latency to happy path). Cost: yes, new L@E function = additional deploy artifact + IAM + CW logs + propagation wait. But that's the right cost for clean separation.

**Option B (path-scoped CF behavior split with conditional custom_error_response) — RULED OUT.** During PRD v0.1 authoring AE 0.7 discovered that CloudFront `custom_error_response` is **distribution-level**, not behavior-level. Implementing Option B cleanly would require either (B-1) origin-response L@E handling on the HTML side — which collapses into Option A — or (B-2) splitting into a separate CF distribution, a much larger blast radius. CTO Q2 ratify on Option A confirms the architectural call independent of this discovery.

### 3.2 — Structured error envelope shape

```javascript
// Response body (Content-Type: application/json; no-cache):
{
  "error": "artifact_not_found",   // or "artifact_forbidden" for 403
  "uri": "<request.uri>",
  "bucket": "<firm-bucket-resolved-by-shared-advisor-router>",
  "firmId": "<X-Firm-Id-header-value>",
  "status": 404,
  "request_id": "<cloudfront-request-id-header>"
}
```

**HTTP status preservation:** 404 stays 404; 403 stays 403. React Query treats non-2xx as error state regardless of body content; the envelope is consumer-friendly belt-and-suspenders but the load-bearing signal is the HTTP status itself.

**Pass-through criteria:** if `response.status < 400` OR request URI is NOT an artifact path (e.g., `/portal/*`, `/`, `/index.html`), pass through unchanged. SPA deep-link routes flow back through CF `custom_error_response` exactly as today.

### 3.3 — Empirical acceptance gate

Reproduce the 2026-05-14 P1 failure mode in a controlled test:
1. Deploy a portal commit that sends a wrong-firmId param (e.g., `?firm=49financial`)
2. Issue an artifact-class request (`/api/scoped/advisor-intelligence/platinum/firm/partner_analytics_annual.json`)
3. Expected pre-fix: HTTP 200 + `Content-Type: text/html` + `<!doctype html>` body (toxic)
4. Expected post-fix: HTTP 404 + `Content-Type: application/json` + structured envelope per §3.2; React Query enters `error` state (NOT silent null cache)

---

## §4 — Phased Plan

### Phase 1 — COMPLETE: PRD authoring + CTO architectural ratify

- PRD v0.1 authored 2026-05-14 16:55Z (Option A/B fork explicit)
- CTO architectural ratify 2026-05-14 16:55Z (Option A locked; narrow scope; zero overlap with DE 0.4)
- PRD v0.2 ship 2026-05-14 17:05Z (this revision)

### Phase 2 — Implementation + deploy (TO-001)

Single TO `ADHC_LEDGEH.001.ae-shared-advisor-router-error-envelope` (~15-20 LOC + Terraform L@E wiring + CF behavior association; ~1d wall). Ship via standard AE Lambda Deployment Protocol:
- write code → bun build → write Terraform → update lambda-source-map → safe-commit → terraform plan → terraform apply → verify 0-diff → tag (portal-auth-v{X.Y.Z+1}) → push --follow-tags
- L@E propagation wait ~15-30min post-apply before integration test
- CF distribution invalidation for affected behaviors

### Phase 3 — Validation sweep (TO-VAL)

Reproduce P1 failure mode (per §3.3). Acceptance: structured JSON error envelope reaches React Query at HTTP 404; cache state observed via React Devtools shows `error` not `null`. Cross-reference with DE 0.4 `cb62f069` to verify FE-side error handling consumes the envelope cleanly. Andrew empirical UAT on Inflection partner-demo Annual interval post-deploy.

---

## §5 — Compiler Evidence

| Tool | Use | Finding |
|---|---|---|
| `comp-routes behaviors` | Map CloudFront behaviors to L@E trigger types + custom_error_response wiring | Phase 1 mandate; informs Option A vs Option B fork scope |
| `comp-routes trace partner_analytics_annual` | Full CF → auth → S3 key path for the empirical anchor URL | Phase 1 mandate; informs blast radius |
| `comp-iam service shared-advisor-router` | Current IAM ops baseline (4 ops: s3:GetObject ×3 via OAI + headers) | Pre-write baseline; Option A may add new IAM if response-Lambda needs distinct role |
| `comp-blast shared-advisor-router` | Downstream impact of L@E change | Phase 1 mandate; identifies any consumer that expects the current HTML-collapse behavior (none expected, but verify) |
| `comp-validate` (custom config) | Synthetic empirical anchor reproduction | TO-VAL mandate |

### Compiler Tools Mandate (TO authoring template)

**Phase 1 (before writing):**
- `comp-routes behaviors` + `comp-routes trace partner_analytics_annual`
- `comp-iam service shared-advisor-router`
- `comp-blast shared-advisor-router`

**Phase 2 (before commit):**
- `bash -n` shell syntax + `bun build` validity for new L@E (Option A)
- `terraform plan` 0-diff after import / 1-diff at fix
- AE Lambda Deployment Protocol compliance (CLAUDE.md Rules 1-6)

**Phase 3 (after commit):**
- Phase 3 validation sweep per §4
- L@E propagation wait verified via aws lambda get-function (Option A)
- CF distribution invalidation status

---

## §6 — TO Decomposition (COO co-sign + dispatch)

TO files at `org/tier2_senior/0.7.0_AE_CloudOps/task_orders/`.

### TO-001 (PRD-blocking — primary; Option A locked)

- **ID:** `ADHC_LEDGEH.001.ae-shared-advisor-router-error-envelope`
- **Owner:** 0.7.0_AE_CloudOps
- **Scope:**
  - New L@E `shared-advisor-router-response` at `infra/aws/lambda-edge/shared-advisor-router-response/index.mjs` (~15-20 LOC handler + bun build)
  - Handler: inspect `response.status` post S3 fetch; if `403`/`404` AND request URI matches artifact pattern (`/api/scoped/*` AND extension `*.json`), replace body with structured JSON envelope per PRD §3.2 + preserve HTTP status + `Content-Type: application/json` + `Cache-Control: no-cache`
  - SPA deep-link paths (`/portal/*`, root, etc.) pass through unchanged
  - Terraform: new `aws_lambda_function.shared_advisor_router_response` resource in `infra/aws/terraform/portal-auth/lambda-edge.tf` (mirror existing `aws_lambda_function.shared_advisor_router` shape; `runtime = nodejs20.x`, `memory_size = 128`, `timeout = 5`); new `aws_cloudfront_distribution` cache-behavior association on the `/api/scoped/*` path pattern with `event_type = "origin-response"`
  - L@E IAM role `lambda-edge-execution-role` (existing) — reuse, no new IAM
  - lambda-source-map.json entry per CLAUDE.md Rule 4
- **Acceptance:**
  - Empirical P1 reproduction yields parseable JSON error envelope at HTTP 404 (not SPA HTML at HTTP 200)
  - React Query treats response as `error` state, NOT silent `null` cache (verified via FE devtools or integration test)
  - SPA deep-link routes (`/portal/advisor-intelligence/...`) UNAFFECTED — still return `/index.html` with HTTP 200 on 404 fallback
  - CloudWatch logs (`/aws/lambda/us-east-1.shared-advisor-router-response`) show normal traffic; no error-class spike
  - `comp-iam service shared-advisor-router-response` post-deploy shows expected ops set (no IAM-permission gaps)
  - Cross-reference verified with DE 0.4 `cb62f069` FE error handling
  - `terraform plan` 0-diff post-apply
- **Effort:** ~1d wall (~15-20 LOC + Terraform + L@E propagation + CF invalidation)

### TO-VAL (validation sweep — Phase 3)

- **ID:** `ADHC_LEDGEH.VAL.ae-empirical-regression-sweep`
- **Owner:** 0.7.0_AE_CloudOps
- **Scope:** Reproduce 2026-05-14 P1 failure mode in pre-fix state on a synthetic harness (or against historical CloudFront logs if available). Confirm post-fix state yields parseable JSON error envelope at HTTP 404, NOT toxic SPA HTML at HTTP 200.
- **Acceptance:**
  - Pre-fix harness reproduces SPA HTML at HTTP 200 on artifact-class wrong-bucket request (anchors the regression)
  - Post-fix harness yields the structured envelope per §3.2 at HTTP 404
  - Andrew empirical UAT on Inflection partner-demo: Annual interval renders correctly post-deploy
- **Effort:** ~30min-1h

### Cross-domain coordination

- DE 0.4 FE-side fix `cb62f069` (drop `refetchOnMount: false` on the demonstrated-poisoning useQuery) is a **complementary** lane and is NOT a dependency for this PRD ship. Both ship independently; this PRD eliminates the toxic source primitive, DE FE fix tightens the consumer-side cache behavior.
- FIRMSEP.10 Cottonwood live-ship is the next risk window for the cache-poisoning class; this PRD landing BEFORE FIRMSEP.10 hardens that ship preemptively.
- CTO PRD review queued (4 architectural questions on the MCP I sent today 16:49Z).

---

## §7 — Open Questions (post v0.2 CTO ratify)

**RESOLVED (CTO ratify 16:55Z):**

- **Q1 (originally: Option A vs Option B fork):** Option A locked.
- **Q2 (originally: existing CF/L@E split primitive):** Structurally novel; no existing primitive to reuse.
- **Q3 (originally: narrow vs broader SPA-deep-link cleanup):** Narrow scope locked; SPA-deep-link cleanup deferred to separate ADHC candidate if surfaces.
- **Q4 (originally: overlap with DE 0.4 `cb62f069`):** Zero overlap; clean defense-in-depth pair.

**STILL OPEN (TO-001 dispatch-time decisions):**

1. **Artifact-pattern matching.** Scope by path glob (`/api/scoped/*`) AND extension (`*.json`)? Or just path glob? CTO narrow-scope directive favors AND-of-path-AND-extension; cleanest signal that body is JSON-consumer-intended. Lean: AND.

2. **Defense-in-depth `apiRequest` FE contract.** Should DE 0.4 add a Content-Type assertion to `apiRequest` (throw on `text/html` without `error` envelope field)? FE-lane change; **flag to DE 0.4 as a separate follow-on, not scope-into-LEDGEH**. DE 0.4 will decide independently.

3. **CI integration test for the new behavior.** ADVI_FIRMSEP.04 already has a CI integration test for `shared-advisor-router` firm-routing. Extend that test to cover the new error-envelope behavior, or add a new test under `infra/aws/lambda-edge/_tests/shared-advisor-router-response/`? Lean: extend existing FIRMSEP.04 test surface.

---

## §8 — Acceptance Criteria (project-level)

1. **Toxic primitive eliminated for artifact-class paths.** No path under `/api/scoped/*` returns HTTP 200 + `Content-Type: text/html` on S3 NoSuchKey / NoSuchBucket / 403.
2. **SPA deep-link routes unaffected.** `/portal/*` and root deep-links still return `/index.html` at HTTP 200 on 404 fallback.
3. **React Query consumes the error correctly.** Verified via FE devtools or integration test that `useQuery` enters `error` state on the failure path, NOT `data: null`.
4. **Empirical P1 regression.** TO-VAL sweep reproduces the 2026-05-14 P1 failure mode pre-fix (anchor verified) and confirms post-fix state.
5. **No regression on CloudWatch error class.** Post-deploy CloudWatch log group `/aws/lambda/us-east-1.shared-advisor-router*` shows normal traffic pattern; no error-class spike.
6. **AE Lambda Deployment Protocol compliance.** CLAUDE.md Rules 1-6 + 7-12 (if EC2 component surfaces, which it should not for this PRD): Terraform-only deploy, commit-before-apply, dependencies in Layers (none for L@E here), source-map registered (Option A), Lambda sized appropriately (memory + timeout — L@E max 128MB + 5s for origin-response), tagged after deploy.
7. **Documentation:** AE 0.7 session log captures the PRD-author + TO-ship chain; cross-references DE 0.4 cache-poisoning memory entry as the empirical seed.

---

## §9 — Risks + Mitigations

| Risk | Mitigation |
|---|---|
| Option A: L@E origin-response adds latency on every artifact response | L@E p99 measured <50ms for trivial handlers; negligible vs S3 fetch wall (~50-200ms typical); can be measured + dropped if Andrew rejects |
| Option B: splitting CF behavior breaks an existing cache-key partition | comp-routes behaviors pre-write inspection enumerates all path patterns; FIRMSEP.06 cache-key partitioning audit informs the split |
| New L@E mis-handles request methods (OPTIONS preflight, HEAD) | Mirror `shared-advisor-router` OPTIONS pass-through pattern; integration test in FIRMSEP.04 surface |
| `custom_error_response` removal accidentally exposes raw S3 error XML to the FE | React Query treats HTTP status as the load-bearing signal; XML body in 404 is acceptable (FE doesn't parse it); if needed, Option A's structured envelope replaces the body entirely |
| Deploy-window cache poisoning STILL possible on non-artifact routes | Out of scope for this PRD; banked as separate ADHC candidate if surfaces |
| L@E versioning + propagation wait introduces deploy-time friction | Standard AE protocol; ~15-30min wait is well-understood; Andrew sign-off after wait verified |
| CTO architectural ratify delay blocks ship | Architectural question is bounded (Option A vs Option B); CTO turnaround typically same-day per recent ADHC arc; PRD v0.2 ships post-ratify in 1-2h author-cycle |

---

## §10 — Cross-references

- **DE 0.4 cache-poisoning memory entry:** `memory/feedback_react_query_cache_poisoning_from_deploy_window.md` (filed 2026-05-14)
- **DE 0.4 FE-side fix:** `cb62f069` (drop `refetchOnMount: false` on the demonstrated-poisoning useQuery; targeted complement to this PRD's structural fix)
- **P1 brief:** `docs/briefs/inf_snapshot_segment_analytics_interval_data_gaps_20260514.md` (DE 0.4 brief `e70fb243f`)
- **AE 0.7 Phase 1.1 CloudWatch evidence packet:** RAVC4 to COO 2026-05-14 16:39Z; CW pull scripts in `.runtmp/ae07_cw_*.py`
- **DS~A Phase 1.3 ship-side probe:** `org/tier2_senior/0.4.0_DS_ClientPlatform/logs/2026-05-14/DS_A_session3_p1_partner_analytics_annual_ship_lineage_probe.md`
- **COO RATIFY message:** 20260514T165217Z `RATIFY ADHC_LEDGEH proposal — strong defense-in-depth + general-purpose; author PRD + initial TO`
- **AE 0.7 architectural review request:** MCP to CTO 2026-05-14 16:49Z with 4 architectural questions
- **Related projects:**
  - `ADVI_FIRMSEP.04` (CI integration test for shared-advisor-router firm-routing) — extension surface
  - `ADVI_FIRMSEP.06` (conditional cache-key partitioning) — orthogonal cache hardening
  - `ADVI_FIRMSEP.10` (Cottonwood onboarding live-ship) — primary risk-window beneficiary
  - `ADVI_SHARED.006` (4-layer firmId canonicalization; DE 0.4 ship `8b71292f`) — same deploy-window cluster
  - `ADHC_DRIFTD` (sibling deploy-record hardening; v0.1 SHIPPED 2026-05-13) — closest architectural sister project
- **CLAUDE.md:** Rules 1 + 6 (Terraform-only, deliberate sizing); Rule 11 (verify parity); applicable to L@E deploy under standard protocol

---

## §11 — Versioning

- **v0.1** — 2026-05-14 ~16:55Z — initial ship; Option A / Option B architectural fork explicit in §3.1 + §7.Q1; PRD-authoring lane: 0.7.0_AE_CloudOps. CTO architectural ratify queued (CC'd on proposal MCP 16:49Z). COO ratify received 16:52Z; project code locked as `ADHC_LEDGEH`.
- **v0.2** — 2026-05-14 ~17:05Z — post CTO architectural ratify (msg 16:55Z): Option A (origin-response L@E with structured JSON error envelope) **LOCKED**; scope **NARROWED** per Q3 to artifact-class (`/api/scoped/*` AND `*.json`) paths; CTO Q1 confirmed structurally novel; CTO Q4 confirmed zero overlap with DE 0.4 `cb62f069` (defense-in-depth pair). Option B discovery (CF custom_error_response is distribution-level, not behavior-level) documented as rule-out reasoning. PRD-authoring lane: 0.7.0_AE_CloudOps. Phase 2 dispatch (TO-001) unblocked.
