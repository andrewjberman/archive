# ADVI_APISCP — Scoped API Multi-Partner Routing Architecture
## Product Requirements Document

**Project Code:** `ADVI_APISCP`
**Date:** 2026-03-10
**Author:** 1.0.0_SA_CTO
**Status:** Phase 0 — Ready for COO decomposition
**Receiving Agents:** `0.4.0_DE_ClientPlatform`, `0.4.0_DT_ClientPlatform`, `0.5.0_AE_OpalETL`, `0.6.0_AE_PartnerETL`

---

## 1. Problem Statement

Partner data (Advisor Intelligence) must never leave its origin bucket (`opal-data-{firmId}`). This is a compliance and architectural invariant, not a preference.

The current implementation has two competing routing layers that are in conflict:

### Layer A — Lambda@Edge `shared-advisor-router` (correct intent, incomplete)
`infra/aws/lambda-edge/shared-advisor-router/index.mjs` v3 rewrites `/api/scoped/advisor-intelligence/*` → `/gold/*` and routes to `opal-data-bd`. This is the right model but hardcodes `opal-data-bd` as the single S3 origin — it has no per-partner routing logic.

### Layer B — `opal-data-portal-v2/json/advisor-intelligence/` (ELIMINATED)
A stale copy of partner data was being maintained at `opal-data-portal-v2/json/advisor-intelligence/` as an artifact of the pre-proxy architecture. This was detected on 2026-03-10 and permanently deleted. No writer exists for this path. This anti-pattern must never be recreated.

### Layer C — `opal-partners-data` Lambda / API Gateway (exists but disconnected)
`infra/aws/lambda/v2_portal/partners/lambdas/opal-partners-data/lambda_function.py` already implements correct multi-tenant logic: reads `X-Firm-Id` → DynamoDB lookup → correct S3 bucket. It is wired to `/api/shared/` paths (deprecated) and is currently disconnected from the active `/api/scoped/` routing.

**The gap:** The `shared-advisor-router` Lambda@Edge hardcodes `opal-data-bd` as the origin. When partner 2 onboards, their data must live in `opal-data-{firmId2}`, and the router has no mechanism to get there. We must build this now — with one partner — so the architecture is correct before we have two.

---

## 2. Compliance Rule (Non-Negotiable)

> Partner data is never copied to `opal-data-portal-v2` or any shared bucket. Each partner's data lives exclusively in `opal-data-{firmId}`. All portal reads go directly to the partner's origin bucket, optionally behind a CloudFront cache layer that is keyed per-firm. This is the ONLY acceptable pattern.

---

## 3. Current Architecture (Annotated)

```
Browser
  |
  | GET /api/scoped/advisor-intelligence/timeseries_chart.json
  |   (Authorization: Bearer {JWT})
  v
CloudFront Distribution: d2n2nzpeqf34ge.cloudfront.net (EVTSA9VEHNZVH)
  |
  | viewer-request → auth-validator-edge (Lambda@Edge v7)
  |   Verifies JWT, injects headers:
  |     X-Firm-Id    = payload.firmId      <-- KEY: firmId from JWT
  |     X-User-Email = payload.sub
  |     X-User-Tier  = payload.tier
  |     X-User-Role  = payload.role
  |
  | origin-request → shared-advisor-router (Lambda@Edge v3)
  |   Rewrites URI: /api/scoped/advisor-intelligence/* → /gold/*
  |   PROBLEM: Always routes to opal-data-bd origin (hardcoded)
  |            Does not use X-Firm-Id header
  v
S3 Origin: opal-data-bd.s3.amazonaws.com    <-- HARDCODED. Must become dynamic.
  /gold/timeseries_chart.json
  /gold/architect_leaderboard.json
  /gold/snapshots/aua_by_architect.json
  ... etc.
```

### What `auth-validator-edge` already gives us

The JWT claim `firmId` is already extracted and injected as `X-Firm-Id` on every authenticated request. For 49 Financial users, `X-Firm-Id = "bd"` (matching bucket `opal-data-bd`). This header is available to every Lambda@Edge in the `origin-request` phase.

---

## 4. Target Architecture

```
Browser
  |
  | GET /api/scoped/advisor-intelligence/timeseries_chart.json
  |   (Authorization: Bearer {JWT with firmId="bd"})
  v
CloudFront Distribution (EVTSA9VEHNZVH)
  |
  | viewer-request → auth-validator-edge (unchanged)
  |   Injects X-Firm-Id = "bd"
  |
  | origin-request → shared-advisor-router (v4 — this project)
  |   1. Reads X-Firm-Id from request headers
  |   2. Constructs S3 bucket: opal-data-{firmId}  → opal-data-bd
  |   3. Dynamically sets request.origin to that bucket
  |   4. Rewrites URI: /api/scoped/advisor-intelligence/* → /gold/*
  v
S3 Origin: opal-data-{firmId}.s3.amazonaws.com    <-- DYNAMIC per-firm
  /gold/timeseries_chart.json
  ... etc.
```

When partner 2 onboards (`firmId = "xyz"`):
- Their data pipeline writes to `opal-data-xyz/gold/`
- DynamoDB `FIRM#xyz META` record created with `s3Bucket: opal-data-xyz`
- No code changes needed — router constructs bucket from firmId automatically
- No CloudFront origin config changes needed (dynamic origin)
- No IAM changes needed (wildcard `opal-data-*` already covers it)

---

## 5. Scope of Work by Agent

### 5.1 — `0.4.0_DT_ClientPlatform` (PRIMARY OWNER, most work)

**What:** Update `shared-advisor-router` Lambda@Edge to v4 with dynamic S3 origin routing. Deploy Terraform changes.

**Files to change:**
- `infra/aws/lambda-edge/shared-advisor-router/index.mjs` — v4 logic
- CloudFront Terraform (locate and update the `opal-data-bd` S3 origin to use dynamic origin; may require new `aws_cloudfront_origin` with OAI covering `opal-data-*`)
- `infra/aws/lambda/ci/lambda-source-map.json` — update entry for `shared-advisor-router`

**Core logic for v4 `shared-advisor-router`:**
```javascript
// origin-request trigger
const firmId = request.headers['x-firm-id']?.[0]?.value;
if (!firmId) return { status: '403', body: 'Missing firm identity' };

const bucket = `opal-data-${firmId}`;
const domainName = `${bucket}.s3.us-east-1.amazonaws.com`;

// Dynamically set origin to the correct partner bucket
request.origin = {
  s3: {
    domainName,
    region: 'us-east-1',
    authMethod: 'origin-access-identity',
    path: '',
    customHeaders: {}
  }
};

// Rewrite path: /api/scoped/advisor-intelligence/* → /gold/*
request.uri = request.uri.replace('/api/scoped/advisor-intelligence/', '/gold/');
```

**CloudFront OAI requirement:** The CloudFront OAI (Origin Access Identity) must have `s3:GetObject` on `arn:aws:s3:::opal-data-*/*` — confirm current IAM allows this wildcard. If only `opal-data-bd` is granted today, expand to the wildcard.

**Deployment sequence:**
1. Update Lambda@Edge source → commit → zip → upload to S3
2. Update Lambda version in Terraform
3. `terraform plan` → verify CloudFront distribution changes
4. `terraform apply`
5. CloudFront deployment takes ~5-15 minutes to propagate globally
6. Verify: `curl -H "Authorization: Bearer {token}" https://d2n2nzpeqf34ge.cloudfront.net/api/scoped/advisor-intelligence/timeseries_chart.json | jq '.aua.data | last | .date'` → must return `2026-03-06`
7. 0-diff plan → tag → push

**Blocker to flag:** Lambda@Edge functions must be deployed to `us-east-1` and are replicated to all edge locations by CloudFront. Confirm the existing `shared-advisor-router` is deployed to `us-east-1` and wired correctly before modifying.

---

### 5.2 — `0.4.0_DE_ClientPlatform`

**What:** Update documentation and endpoint client code to accurately reflect the architecture. Ensure the frontend is passing `firmId` correctly and that no frontend code has any reference to the old `opal-data-portal-v2/json/advisor-intelligence` paths.

**Files to change:**
- `portal/src/api/endpoint-mapping.ts` — Update comment on line 13. Currently says:
  ```
  /api/scoped/* -> S3 origin (s3://opal-data-portal-v2/json/) via shared-advisor-router
  ```
  Correct to:
  ```
  /api/scoped/* -> S3 origin (s3://opal-data-{firmId}/gold/) via shared-advisor-router (dynamic per-firm)
  ```
- `portal/src/api/endpoints/advisor-intelligence.ts` — Audit all scoped calls. Confirm `firmId` is being sent where required. The static file calls (`timeseries_chart.json`, `clients_tab.json`) route via CloudFront and do not need `?firmId=` because the router uses `X-Firm-Id` from the JWT. Dynamic dimension calls (`/timeseries/{dimension}?firmId=`, `/snapshots/{dimension}?firmId=`) are API Gateway-backed — confirm this separation is still correct post-architecture clarification.
- `portal/src/api/endpoint-mapping.ts` — Remove any `SCOPED` category if it still references `opal-data-portal-v2`. Add explicit documentation that SCOPED = per-partner bucket, GENERAL = `opal-data-portal-v2`.

**Verification:** After DT deploys, load the AdvisorIntelligence page in dev and confirm the Network tab shows `data_as_of: 2026-03-06` in all timeseries_chart.json, clients_tab.json, and leaderboard responses.

---

### 5.3 — `0.6.0_AE_PartnerETL` (bd-pipeline owner)

**What:** Verify and document the gold output path convention. Ensure the `bd-portal-publisher` Lambda writes all output to `opal-data-bd/gold/` with no side-writes to any other bucket. Register this as a canonical invariant.

**Files to review/update:**
- `infra/aws/lambda/bd-pipeline/bd-portal-publisher/lambda_function.py` — Confirm `OUTPUT_BUCKET = 'opal-data-bd'` and all `_save_json()` calls write to `gold/` prefix. No calls to `opal-data-portal-v2`.
- `infra/aws/lambda/ci/lambda-source-map.json` — Verify `bd-portal-publisher` entry is current.
- `infra/aws/ec2/EC2_MANIFEST.json` — Verify the bd-pipeline EC2 service (bd-exporter) is registered and its output paths are documented.
- Update `pipeline_inventory.xml` to explicitly document the gold output contract:
  ```
  Output: s3://opal-data-bd/gold/{filename}.json
  Pattern: opal-data-{firmId}/gold/ for all partner pipelines
  Never: opal-data-portal-v2/ (any prefix)
  ```

**New partner onboarding checklist to write** (deliverable):
When a new partner pipeline is created, the AE must:
1. Create `opal-data-{firmId}` S3 bucket with versioning enabled
2. Create `FIRM#{firmId}` DynamoDB record in `opal-users-v2` with `s3Bucket: opal-data-{firmId}`
3. Write all gold output to `s3://opal-data-{firmId}/gold/`
4. Never write to `opal-data-portal-v2`
5. No IAM changes needed (wildcard `opal-data-*` already grants access)

---

### 5.4 — `0.5.0_AE_OpalETL` (yang/news/market pipelines)

**What:** Awareness and audit only. OpalETL pipelines (yang, news, market-overview) write to `opal-data-portal-v2` — this is correct for non-partner, general public data. No changes needed for those pipelines. However, `0.5.0_AE_OpalETL` must confirm that none of their pipelines write to any `opal-data-*` bucket pattern that could be confused with partner buckets.

**Action items:**
- Audit `yang-pipeline`, `news-pipeline`, `market-overview` publisher output paths
- Confirm all writes go to `opal-data-portal-v2/json/` or `opal-data-portal-v2/json-tiered/` exclusively
- Confirm no pipeline writes to `opal-data-bd/` or any `opal-data-{firmId}/` path
- Document this clearly in `pipeline_inventory.xml`: "Yang/News/MarketOverview pipelines write ONLY to opal-data-portal-v2. Partner pipelines write ONLY to opal-data-{firmId}. These are separate, non-overlapping patterns."

---

## 6. DynamoDB Firm Registry (Context for All Agents)

The `opal-users-v2` DynamoDB table stores firm metadata:

```
PK: FIRM#bd     SK: META
  firmId:   "bd"
  name:     "49 Financial"
  tier:     "advisor"
  s3Bucket: "opal-data-bd"
  status:   "active"
```

The `shared-advisor-router` v4 does NOT need to query DynamoDB. It constructs the bucket name from the `X-Firm-Id` header directly: `opal-data-{firmId}`. The DynamoDB record exists for the `opal-partners-data` Lambda path and for future use cases (e.g., firm-specific feature flags, branch bucket overrides). The v4 router's `opal-data-{firmId}` convention is the canonical bucket naming pattern — this must be enforced when onboarding new partners.

---

## 7. Existing Assets That Are Already Correct (Do Not Regress)

| Asset | Location | Status |
|-------|----------|--------|
| `auth-validator-edge` v7 | `infra/aws/lambda-edge/auth-validator-edge/index.mjs` | Correct — injects X-Firm-Id |
| `shared-advisor-router` v3 | `infra/aws/lambda-edge/shared-advisor-router/index.mjs` | Partially correct — needs v4 dynamic origin |
| `opal-partners-data` Lambda | `infra/aws/lambda/v2_portal/partners/lambdas/opal-partners-data/` | Correct pattern, disconnected from active routing — keep as reference |
| IAM wildcard `opal-data-*` | `partners-lambda-role` | Correct — no changes needed |
| `bd-portal-publisher` output | `opal-data-bd/gold/` | Correct |
| `opal-data-portal-v2/json/advisor-intelligence/` | DELETED 2026-03-10 | Gone — must never be recreated |

---

## 8. Risks and Constraints

| Risk | Mitigation |
|------|-----------|
| CloudFront OAI only grants access to `opal-data-bd`, not `opal-data-*` | DT confirms/expands OAI policy before applying |
| Lambda@Edge dynamic origin requires `request.origin` mutation — only valid in `origin-request` phase | `shared-advisor-router` is already an `origin-request` trigger — confirmed compatible |
| CloudFront cache will serve old responses after the Lambda@Edge update until TTL expires | Invalidate `/api/scoped/advisor-intelligence/*` path after deploy |
| New partner's firmId must exactly match bucket suffix (`opal-data-{firmId}`) | Enforce naming convention in onboarding checklist (AE deliverable) |
| `opal-data-portal-v2` stale files being recreated by any pipeline | AE confirms no pipeline writes to advisor-intelligence paths there |

---

## 9. Acceptance Criteria

1. `GET /api/scoped/advisor-intelligence/timeseries_chart.json` with a 49 Financial user JWT returns `data_as_of: 2026-03-06` (or current gold date).
2. The same request hits `opal-data-bd.s3.amazonaws.com/gold/timeseries_chart.json` — verifiable in CloudFront access logs.
3. `opal-data-portal-v2/json/advisor-intelligence/` and `opal-data-portal-v2/api/public/advisor-intelligence/` remain empty permanently. CI or a monitoring check confirms this.
4. `endpoint-mapping.ts` accurately documents the scoped routing architecture.
5. `pipeline_inventory.xml` for bd-pipeline and yang-pipeline explicitly documents the bucket separation invariant.
6. A new partner onboarding checklist exists as a deliverable from `0.6.0_AE_PartnerETL`.
7. 0-diff Terraform plan after all changes are applied.
8. All changes committed and tagged per deployment protocol.

---

## 10. Out of Scope

- Migrating existing `/api/shared/` paths (deprecated) — leave `opal-partners-data` Lambda as-is for now
- Building the second partner's actual data pipeline — this project only establishes the routing infrastructure
- Frontend UI changes — no page changes required; this is purely infrastructure and routing
