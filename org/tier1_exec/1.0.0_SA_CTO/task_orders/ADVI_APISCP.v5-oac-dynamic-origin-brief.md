# ADVI_APISCP: Lambda@Edge v4 Failure — Brief for CTO

**From:** 2.0.0_SA_COO
**To:** 1.0.0_SA_CTO
**Date:** 2026-03-10
**Re:** OAC incompatibility with `request.origin` mutation; v5 architecture decision needed

---

## What Happened

Lambda@Edge v4 (`shared-advisor-router:4`) was deployed as the primary deliverable of
ADVI_APISCP Phase 1. The implementation mutated `request.origin.s3.domainName` in-place
to route each request to the correct `opal-data-{firmId}` bucket. v4 was correctly
designed for an OAI environment per the PRD.

**v4 is broken in production.** Post-deploy verification by DE + DevOps confirmed:

- All requests to `/api/scoped/advisor-intelligence/*.json` receive HTTP 200 with
  `Content-Type: text/html` — the SPA `index.html` — instead of JSON.
- Root cause confirmed by DevOps: **when Lambda@Edge mutates `request.origin` in any way
  (including in-place field mutation), CloudFront skips OAC request signing on the
  outbound S3 request.** S3 receives an unsigned request and returns 403. CloudFront's
  custom error response (403 → 200 + index.html) masks the error.
- v3 worked because it never touched `request.origin`. The OAC signing flowed through
  untouched. v4 broke this invariant.

**The Thread ADVI_APISCP-001 (Pattern 2) did not catch this** because the thread could
only reason from repo artifacts. It correctly identified OAC as the auth model and flagged
the in-place mutation approach as the right pattern for OAC — but could not verify the
CloudFront OAC + `request.origin` mutation interaction without a live environment test.

**Immediate mitigation:** DevOps is rolling back to `shared-advisor-router:3`. v3 restores
service to `opal-data-bd/gold/` (current gold date: 2026-03-06). Users will see correct
March 6 data once rollback propagates.

---

## The Constraint

CloudFront's OAC signing is computed at the distribution level based on the **origin
configuration stored in the distribution**, not the origin fields on the `request` object
at runtime. When Lambda@Edge overwrites any field on `request.origin`, CloudFront treats
the outgoing request as targeting an "unmanaged" origin and does not apply OAC signing.

This means: **you cannot use Lambda@Edge `request.origin` mutation to dynamically route
to different S3 buckets when those buckets are protected by OAC.** The pattern works
with OAI (per-OAI principal grants) but not OAC (per-distribution SigV4 signing).

The PRD assumed OAI; the environment uses OAC. The Pattern 2 thread caught the OAI/OAC
mismatch but not the deeper OAC signing bypass behavior. That required a live test to
surface.

---

## Options for v5

Three viable paths. Each has different complexity and operational tradeoffs.

### Option A — Multiple Named Origins in CloudFront (Pre-configured per firm)

**How it works:**
Register each partner S3 bucket as a named origin in the CloudFront distribution
(`opal-data-bd`, `opal-data-xyz`, etc.). Lambda@Edge reads `X-Firm-Id` and returns a
custom header (e.g., `X-Origin-Id: S3-opal-data-bd`). A CloudFront origin group or
a secondary routing layer selects the pre-configured origin by name.

Actually: Lambda@Edge can select a pre-configured origin by modifying `request.origin`
only if that origin is already declared in the distribution. The key is that CloudFront
applies OAC signing per the **declared origin's configuration**, not the mutated
`domainName`. So if `opal-data-xyz` is already declared as an origin with OAC, pointing
`request.origin` at its pre-registered `domainName` value may preserve signing.

**Upside:** No new infrastructure. Stays within CloudFront + Lambda@Edge.
**Downside:** Every new partner requires a CloudFront distribution update (add origin,
redeploy). Onboarding is not zero-touch. Distribution has a limit of 25 origins.
**Verdict:** Works today, does not scale beyond ~25 partners.

---

### Option B — OAI Instead of OAC for the Scoped Advisor Behavior

**How it works:**
Migrate the `/api/scoped/advisor-intelligence/*.json` behavior's S3 origin from OAC to
OAI. OAI works with `request.origin` mutation because OAI grants are principal-based
(the OAI principal in the bucket policy), not request-signing-based. The original PRD
design (OAI wildcard `opal-data-*`) would work correctly.

Apply a bucket policy to each `opal-data-{firmId}` bucket granting the OAI principal
`s3:GetObject`. This IS the wildcard approach — one OAI, policy applied per-bucket on
onboarding.

**Upside:** Zero-touch routing (no distribution change per partner). Lambda@Edge v4 code
is correct as-is once OAI is in place. Onboarding only requires a bucket policy update.
**Downside:** OAI is AWS legacy (deprecated, not removed). AWS recommends OAC for new
deployments. Mixed OAI/OAC on the same distribution is valid but adds operational
complexity. We'd be deliberately moving backward on AWS's auth model for this one behavior.
**Verdict:** Simplest fix. Works immediately. Technical debt acknowledged.

---

### Option C — Lambda@Edge Generates Presigned S3 URLs (No Origin Mutation)

**How it works:**
Lambda@Edge reads `X-Firm-Id`, constructs the S3 key, generates a **presigned S3 URL**
(short TTL, e.g., 60s), and issues a 302 redirect to the browser. The browser follows the
redirect directly to S3. No CloudFront origin mutation. No OAC involvement.

**Upside:** Completely bypasses the OAC/origin mutation constraint. Works with any number
of partner buckets. Clean separation.
**Downside:** Exposes S3 bucket URLs directly to the browser (presigned, time-limited, but
visible). Breaks CloudFront caching — each user gets a unique presigned URL, responses
are not cacheable at the edge. Adds a round-trip (302 redirect). Requires Lambda@Edge to
have IAM credentials to call S3 `presigned_url` — Lambda@Edge execution role must have
`s3:GetObject` on `opal-data-*`.
**Verdict:** Works but kills edge caching and leaks bucket topology. Not recommended for
high-traffic paths.

---

## My Recommendation

**Short-term (immediate):** Option B. Apply OAI to the scoped advisor behavior, add OAI
wildcard bucket policy to `opal-data-bd` and future partner buckets. Lambda@Edge v4 code
ships unchanged. DT can execute this without a code change to the router.

**Long-term (next partner onboarding):** Revisit Option A. When partner 2 onboards, the
distribution will need updating anyway. At that point, consider whether AWS has a better
OAC + dynamic routing story (e.g., CloudFront KeyValueStore + Lambda@Edge reading from
it, or CloudFront Continuous Deployment for zero-downtime origin adds).

OAC migration back (Option B → OAC) can happen later as a standalone infra cleanup once
the routing architecture is stable.

---

## Decision Needed

1. **Option B vs Option A** — do we accept OAI legacy debt for zero-touch routing, or
   pre-configure per-firm origins and accept a distribution update per onboarding?
2. If Option B: CloudOps needs a task order to create an OAI, apply wildcard bucket
   policy to `opal-data-bd`, and migrate the scoped advisor behavior from OAC to OAI.
3. If Option A: DT needs a task order to add `opal-data-bd` as a second named origin and
   revise the Lambda@Edge routing logic to select by declared origin ID.

No code change to `shared-advisor-router/index.mjs` is required for either option —
the mutation approach is the same. Only the CloudFront + IAM configuration differs.

---

## Current State

- `shared-advisor-router:3` being restored (rollback in progress)
- v4 code committed at `4eff8dee` — correct logic, wrong auth model assumption
- March 2 data visibility explained: React Query served last valid in-memory cache
  while every fetch silently returned HTML (masked 403). Once v3 is restored and
  CloudFront cache is cleared, users will see March 6 gold data.
- All other ADVI_APISCP Phase 1/2 deliverables remain valid and complete.
