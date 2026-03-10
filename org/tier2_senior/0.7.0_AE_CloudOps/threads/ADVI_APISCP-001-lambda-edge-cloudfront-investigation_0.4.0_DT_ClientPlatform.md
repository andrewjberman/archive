# Thread Receipt: Lambda Edge CloudFront investigation

**Thread ID:** ADVI_APISCP-001-lambda-edge-cloudfront-investigation
**Project Serial:** ADVI_APISCP-001
**Created by:** 2.0.0_SA_COO
**Created at:** 2026-03-10T19:17:19Z
**Status:** complete
**Participants:** 0.7.0_AE_CloudOps, 0.4.0_DT_ClientPlatform

---
## 000.md

---
agent: 2.0.0_SA_COO
turn: 0
timestamp: 2026-03-10T19:17:10Z
signal: continue
---

## ADVI_APISCP-001: Lambda@Edge + CloudFront Technical Gap Investigation

I am the COO convening this Pattern 2 thread. The CTO has written PRD ADVI_APISCP proposing a v4 upgrade to `shared-advisor-router` Lambda@Edge that adds dynamic S3 origin routing per firm. The PRD includes pseudocode, but I have identified three critical assumptions that have NOT been verified against the actual infrastructure. No agent should implement until these are resolved.

**Turn order:** CloudOps (source) -> DT ClientPlatform (receiver). Three turns per agent.

---

### The three unknowns

#### Unknown 1: Lambda@Edge deployment mechanism

`infra/aws/lambda-edge/shared-advisor-router/index.mjs` and `infra/aws/lambda-edge/auth-validator-edge/index.mjs` exist in the repo, but:
- They are NOT in `lambda-source-map.json` (checked — no lambda-edge entries)
- They are NOT in any Terraform module under `infra/aws/terraform/`
- CloudFront distribution `EVTSA9VEHNZVH` is not managed by Terraform
- The deployment mechanism is completely unknown

**CloudOps: How were these Lambda@Edge functions deployed?** Look for:
- AWS CLI deploy scripts, Makefile targets, or CI scripts in or near `infra/aws/lambda-edge/`
- CloudFormation templates (separate from Terraform)
- Manual console deployment (check for package.json scripts, deploy notes, README)
- Any evidence of how auth-validator-edge reached v7 — there must be a deployment history

If you cannot find the deployment mechanism in the repo, state that clearly. That itself is a critical finding — it means DT must discover it via AWS CLI (`aws lambda list-versions-by-function`, `aws cloudfront get-distribution-config`) before implementing.

#### Unknown 2: CloudFront origin-request event shape for dynamic origin mutation

The PRD v4 pseudocode does this:

```javascript
const firmId = request.headers["x-firm-id"]?.[0]?.value;
const bucket = `opal-data-${firmId}`;
request.origin = {
  s3: {
    domainName: `${bucket}.s3.us-east-1.amazonaws.com`,
    region: "us-east-1",
    authMethod: "origin-access-identity",
    path: "",
    customHeaders: {}
  }
};
request.headers["host"] = [{ key: "Host", value: `${bucket}.s3.us-east-1.amazonaws.com` }];
```

**DT ClientPlatform: Verify this event shape.** Specifically:
1. Does `request.origin.s3` exist on origin-request events? (It should — origin-request triggers run after cache miss, before CloudFront contacts the origin)
2. Can you MUTATE `request.origin.s3.domainName` to point to a different bucket than what CloudFront is configured with?
3. Does `authMethod: "origin-access-identity"` work when the target bucket is NOT the distribution's configured origin? Or does OAI only authenticate against the configured origin?
4. Is `request.origin = { s3: { ... } }` (full replacement) correct, or must you mutate individual fields on the existing object?

Read the current v3 handler (`shared-advisor-router/index.mjs`) — it only does URI rewrite, never touches `request.origin`. Also read `auth-validator-edge/index.mjs` to confirm the X-Firm-Id header injection format.

#### Unknown 3: OAI policy scope

The S3 module (`infra/aws/multi-account/terraform/modules/s3/main.tf`, lines 131-159) shows that OAI grants are **per-bucket**:

```hcl
principals {
  type        = "AWS"
  identifiers = [var.cloudfront_oai_arn]
}
resources = ["${aws_s3_bucket.this.arn}/*"]
```

This means the OAI can only access buckets that explicitly grant it access. The PRD assumes a wildcard `opal-data-*` pattern, but the Terraform module does NOT do this.

**CloudOps: Answer these questions:**
1. Which S3 buckets currently have an OAI policy granting CloudFront access? Is it only `opal-data-bd`, or are there others?
2. When a new partner bucket (`opal-data-{firmId}`) is created, does the OAI policy get automatically applied? Or must someone explicitly add it per bucket?
3. Is there a Terraform module or script that creates partner buckets with OAI policies already attached?
4. If OAI grants are per-bucket, what is the onboarding sequence for a new firm? The PRD says "no IAM changes needed (wildcard opal-data-* already grants access)" — is this actually true?

Use tool access to search for: `cloudfront_oai` references in Terraform, OAI ARN values, S3 bucket policies on `opal-data-bd`.

---

### Self-unblock requirement (M11)

If you are uncertain about any of the three unknowns: READ the files. Search for deploy scripts. Check Terraform state references. Do NOT close this thread with "we need to check X" — check it now. You have tool access. The only acceptable unresolved items are things that require live AWS CLI queries (e.g., `aws cloudfront get-distribution-config`) which cannot be run from within this thread.

### Final turn must produce:

1. **Deployment mechanism verdict** — how Lambda@Edge is deployed, or explicit statement that it must be discovered via AWS CLI
2. **Event shape verification** — whether `request.origin.s3` dynamic mutation is supported, with any caveats
3. **OAI policy scope** — per-bucket or wildcarded, and what the onboarding sequence for new partner buckets actually requires
4. **Revised implementation guidance** — what the DT task order should say, correcting any PRD assumptions that turned out to be wrong


---

## 001.md

---
agent: 0.7.0_AE_CloudOps
turn: 1
timestamp: 2026-03-10T19:19:16Z
signal: continue
---

## Findings (source-grounded) — ADVI_APISCP Unknowns 1–3

### Unknown 1 — Lambda@Edge deployment mechanism (verdict: **NOT discoverable from current Terraform; likely manual/CLI; must be confirmed via AWS CLI**)

**What I can prove from repo context:**
- `lambda-source-map.json` explicitly does **not** include Lambda@Edge functions (no `auth-validator-edge`, no `shared-advisor-router`, etc.). This matches the PRD note.
- My search under `infra/aws/terraform/` found **no CloudFront / Lambda@Edge / OAI / OAC Terraform resources** (no `aws_cloudfront_distribution`, no `aws_cloudfront_origin_access_identity`, no `aws_cloudfront_origin_access_control` references).
- There is a historical manifest doc: `infra/aws/AWS_MANIFEST_UPDATE_2026-01-04.md` which states Lambda@Edge functions (`auth-validator-edge`, `public-data-router`, etc.) were “deployed 2026-01-04”, but it does **not** document *how* (script path, CI job, CloudFormation, etc.). It includes AWS CLI *verification* commands only.

**Conclusion:** In this repo, Lambda@Edge deploy is **not Terraform-managed** and there is **no local deploy script** discoverable in the `infra/` tree from this thread’s tool scan. Therefore DT must confirm deployment mechanism via live AWS inspection before modifying anything:
- `aws cloudfront get-distribution-config --id EVTSA9VEHNZVH`
- `aws lambda get-function --function-name shared-advisor-router --region us-east-1`
- `aws lambda list-versions-by-function --function-name shared-advisor-router --region us-east-1`

This is a hard blocker to “just implement v4” because we don’t yet know how to publish a new *versioned* Lambda@Edge and attach it to the behavior.

---

### Unknown 2 — Can origin-request mutate S3 origin dynamically? (verdict: **conceptually supported by CloudFront event model, but must be validated against the *actual* distribution config: OAC vs OAI and existing origin shape**)

**What we know from repo context:**
- `shared-advisor-router` v3 (in PRD excerpt) only rewrites `request.uri` and does not touch `request.origin`.
- CloudFront distribution `EVTSA9VEHNZVH` (domain `d2n2nzpeqf34ge.cloudfront.net`) is documented in `infra/aws/AWS_MANIFEST_UPDATE_2026-01-04.md`.
- That same doc states the distribution uses **Origin Access Control (OAC)** for at least one S3 origin:
  - “Origin Access Control (OAC) created 2026-01-04 … OAC ID: `E24L6358YRRKAE` … for public data origin”.

**Why this matters:** The PRD pseudocode assumes `authMethod: "origin-access-identity"` (OAI). If the distribution is now using **OAC**, the request.origin mutation details (and required headers/signing behavior) may differ. Also, CloudFront may include an `origin` object shaped like `request.origin.s3` or `request.origin.custom` depending on the configured origin type.

**Conclusion:** The *general* Lambda@Edge origin-request event does include `request.origin` and it is commonly mutated for dynamic origin routing, but in *this* environment we must validate:
1) whether the current behavior uses an S3 origin with `request.origin.s3` present, and  
2) whether it is OAC-backed (SigV4) vs OAI-backed, because the PRD’s OAI fields may be wrong for this distribution.

This validation requires `aws cloudfront get-distribution-config` output (cannot be proven from local files).

---

### Unknown 3 — OAI/OAC policy scope across partner buckets (verdict: **per-bucket grants; PRD “wildcard opal-data-* already covers it” is not supported by our S3 module**)

**What I can prove from code:**
- The S3 bucket module policy shown in context (`.../modules/s3/main.tf` lines 131–159) grants CloudFront access **per bucket**:
  - `resources = ["${aws_s3_bucket.this.arn}/*"]`
  - i.e., you only get access to the specific bucket that attached the policy.
- Additionally, my scan did not find any Terraform in `infra/aws/terraform/` that establishes a wildcard bucket policy across `opal-data-*`.

**What I can infer safely:**
- If partner buckets are `opal-data-{firmId}`, CloudFront access will require **each bucket** to have a bucket policy allowing the CloudFront principal (OAI ARN or OAC distribution principal) to `s3:GetObject` for that bucket.
- Therefore onboarding a new partner bucket is **not** “no IAM changes needed” unless there is some separate non-Terraform automation that applies the policy at bucket creation time (not evidenced in repo).

**Conclusion:** Treat CloudFront S3 access as **per-bucket**. New partner bucket onboarding must include “attach CloudFront access policy” step (OAI or OAC depending on distribution).

---

## Revised implementation guidance (what DT task order should say differently)

1. **Add an explicit preflight step:** DT must first retrieve and paste the relevant parts of:
   - CloudFront behavior for `/api/scoped/advisor-intelligence/*`
   - Current origin type (S3 vs custom), and whether it uses **OAC** or **OAI**
   - Current Lambda@Edge association ARN + version for `shared-advisor-router`
2. **Do not assume OAI.** The PRD pseudocode uses OAI fields; our distribution is documented as using **OAC** (at least for `/api/public/*`). DT must align the v4 origin mutation to the actual origin auth model.
3. **Bucket access is per-bucket.** Partner onboarding must include adding the CloudFront access policy to `opal-data-{firmId}`. No evidence supports a wildcard `opal-data-*` policy today.

---

## Questions for DT / COO (need answers next turn to converge)

1. Does `shared-advisor-router` currently exist in AWS as a Lambda function name (like `auth-validator-edge` does), or is it named differently?
2. Is `/api/scoped/advisor-intelligence/*` currently served from an S3 origin configured as `opal-data-bd` (as PRD states), or is it still routed via some other origin?
3. Can DT run the AWS CLI queries above and paste the relevant snippets into the thread? That will let me give exact, non-speculative guidance on OAC/OAI and the correct `request.origin` mutation shape.

If DT can provide the `get-distribution-config` excerpt, I can produce a concrete “here is the exact origin object you will see and how to mutate it” recommendation in my next turn.

---

## 002.md

---
agent: 0.4.0_DT_ClientPlatform
turn: 2
timestamp: 2026-03-10T19:19:59Z
signal: continue
---

## DT Receipt + Next Actions (Unknowns 1–3)

### 1) Unknown 1 — Lambda@Edge deployment mechanism
**Receipt:** Confirmed: Lambda@Edge is **not** in `infra/aws/lambda/ci/lambda-source-map.json` and **not** in any Terraform under `infra/aws/terraform/`. Therefore, we **cannot** follow the standard Terraform Lambda deployment protocol for `shared-advisor-router`.

**Implication for my task order ADVI_APISCP.001:** I must treat Lambda@Edge deploy as a **separate, currently-unmanaged** mechanism and **discover it via live AWS inspection** before any code change is applied to CloudFront.

**Required AWS inspection (blocking):**
- `aws cloudfront get-distribution-config --id EVTSA9VEHNZVH`
- `aws lambda get-function --function-name shared-advisor-router --region us-east-1`
- `aws lambda list-versions-by-function --function-name shared-advisor-router --region us-east-1`

Until I have those outputs, I cannot safely answer:
- how to publish a new *version* for Lambda@Edge
- how the CloudFront behavior is currently associated (ARN + version)
- whether the origin is S3 and whether it’s OAI vs OAC

---

### 2) Unknown 2 — origin-request event shape + dynamic origin mutation feasibility
**What we can say from repo context alone (no AWS):**
- `shared-advisor-router` is an **origin-request** Lambda@Edge (per file header + PRD).
- `auth-validator-edge` injects `request.headers["x-firm-id"] = [{ key: "X-Firm-Id", value: payload.firmId }]` (confirmed in provided source). So the header read pattern in v4 is correct: `request.headers['x-firm-id']?.[0]?.value`.

**What we cannot safely assume (needs AWS config):**
- Whether `request.origin.s3` exists in this behavior today (depends on origin type).
- Whether the distribution uses **OAI** or **OAC** for the *advisor-intelligence scoped* origin. CloudOps notes OAC exists for at least `/api/public/*`; that makes the PRD’s `authMethod: "origin-access-identity"` assumption potentially wrong.
- Whether we must mutate `request.origin.s3.domainName` in-place vs replace `request.origin` entirely (depends on the existing origin object shape CloudFront provides for this behavior).

**DT position:** Dynamic origin mutation is *plausible* in origin-request, but I will not implement the PRD pseudocode until I see the actual `get-distribution-config` origin + cache behavior wiring.

---

### 3) Unknown 3 — OAI/OAC policy scope across partner buckets
**Receipt:** The S3 module policy is **per-bucket** (`"${aws_s3_bucket.this.arn}/*"`). There is **no evidence** of a wildcard `arn:aws:s3:::opal-data-*/*` grant in Terraform.

**Implication:** New partner onboarding **will require** adding CloudFront access policy to each `opal-data-{firmId}` bucket (whether via OAI principal ARN or OAC distribution principal), unless CloudOps can point to separate automation outside Terraform (not currently evidenced).

This means the PRD statement “no IAM changes needed” is **not currently supported**.

---

## Questions / Requests to 0.7.0_AE_CloudOps (so I can proceed)
To unblock implementation, I need CloudOps to provide (or confirm I should retrieve) these exact facts from AWS:

1) For behavior path pattern `/api/scoped/advisor-intelligence/*`:
- Which **origin ID** is used?
- Is it an **S3 origin**?
- Is it authenticated via **OAI** or **OAC**?

2) For the Lambda@Edge association on that behavior:
- The Lambda function ARN **including version** currently attached (e.g., `...:function:shared-advisor-router:3`).
- Confirmation whether we deploy by:
  - publishing a new Lambda version + updating the behavior association, or
  - some other mechanism (CloudFormation / console workflow).

If you can paste the relevant excerpt of `get-distribution-config` (Origins + CacheBehaviors entry for this path + LambdaFunctionAssociations), I can draft the exact v4 mutation code to match the real origin shape (OAC vs OAI).

---

## DT Proposed Revision to ADVI_APISCP.001 Task Order (so it’s implementable)
Before “modify `shared-advisor-router/index.mjs`”, add a **Preflight** section:

1. Capture current CloudFront config for `/api/scoped/advisor-intelligence/*` (origin + auth model OAI/OAC + current Lambda@Edge version ARN).
2. Capture current S3 bucket policy mechanism for `opal-data-bd` (and whether it’s OAI- or OAC-based).
3. Only then implement v4 code and deploy via the discovered mechanism.
4. Add explicit onboarding step: “attach CloudFront access policy to new `opal-data-{firmId}` bucket”.

---

## My next step (pending thread guidance)
Once CloudOps confirms whether DT should run the AWS CLI checks (and where to store the excerpts—thread vs session log), I will:
- implement v4 logic in `infra/aws/lambda-edge/shared-advisor-router/index.mjs` **locally**
- but **not deploy** until the AWS config confirms OAI vs OAC and the correct origin mutation shape.

Signal remains **continue** because the thread still needs the AWS config excerpt to converge.

---

## 003.md

---
agent: 0.7.0_AE_CloudOps
turn: 3
timestamp: 2026-03-10T19:20:22Z
signal: continue
---

## CloudOps Response — What’s Verified vs What Still Requires Live AWS

### A) Unknown 1 (Lambda@Edge deploy mechanism) — still **unknown from repo**, and here’s the concrete implication
From repo context alone, we cannot determine:
- the **Lambda function name/ARN** actually associated to the CloudFront behavior (it may not be literally `shared-advisor-router` in AWS),
- whether deploy is done via **console**, **CLI publish-version + update-distribution**, or **some legacy script outside repo**.

**Therefore the correct next action is DT running AWS CLI inspection** (or CloudOps running it if we have the right credentials in the deploy environment). There is no further repo-only work that will resolve this.

**Minimum AWS facts we need to proceed safely:**
1) CloudFront behavior for `/api/scoped/advisor-intelligence/*`:
   - `TargetOriginId`
   - `LambdaFunctionAssociations` (event type `origin-request`) including the **full ARN with version**
2) Origin definition for that `TargetOriginId`:
   - whether it is S3 REST origin (`*.s3.amazonaws.com`) vs custom origin
   - whether it uses **OAC** (OriginAccessControlId present) vs legacy **OAI** (OriginAccessIdentity present)

DT already listed the right command:
- `aws cloudfront get-distribution-config --id EVTSA9VEHNZVH`

### B) Unknown 2 (dynamic origin mutation) — guidance depends on OAC vs OAI, so PRD pseudocode must be treated as **conditional**
Repo evidence indicates **OAC exists** in this environment (at least for public data origin). That makes the PRD’s `authMethod: "origin-access-identity"` assumption **unsafe**.

**What I can state without guessing:**
- Origin-request Lambda@Edge is the correct phase for origin mutation.
- But the *exact* `request.origin` shape you must emit (and whether you must also set `Host`) depends on the existing origin type CloudFront is using for that behavior.

**Actionable constraint for DT task order revision:**
- Replace “set `authMethod: origin-access-identity`” with:
  - “mutate origin to match the distribution’s configured origin auth model (OAC vs OAI) as observed in `get-distribution-config`.”

### C) Unknown 3 (bucket access scope) — **per-bucket** is the only safe assumption today
Given the S3 module policy is per-bucket, and we have no evidence of a wildcard `opal-data-*` access grant, the PRD’s “no IAM changes needed” is **incorrect as written**.

**Revised onboarding invariant (must be added to DT/COO docs):**
- For every new `opal-data-{firmId}` bucket, you must attach a CloudFront access policy for that bucket (principal depends on OAC vs OAI).

### D) Concrete next step request (so we can converge on Turn 5)
DT: please paste into this thread (sanitized is fine) the relevant excerpts from:

1) `aws cloudfront get-distribution-config --id EVTSA9VEHNZVH`:
   - the `CacheBehaviors.Items[]` entry where `PathPattern == "/api/scoped/advisor-intelligence/*"`
   - the referenced `Origins.Items[]` entry for that behavior’s `TargetOriginId`

2) If possible, also paste:
   - `aws lambda get-function --function-name <NAME_FROM_ASSOCIATION> --region us-east-1` (just the `Configuration.FunctionArn` and `Runtime` is enough)
   - `aws lambda list-versions-by-function --function-name <NAME> --region us-east-1` (to confirm current versioning pattern)

Once we have those, I can give **exact** v4 implementation guidance:
- whether to mutate `request.origin.s3.domainName` in-place vs replace `request.origin`,
- whether `Host` header must be set,
- and what bucket policy principal format is required for new partner buckets (OAC vs OAI).

---

## 004.md

---
agent: 0.4.0_DT_ClientPlatform
turn: 4
timestamp: 2026-03-10T19:20:42Z
signal: continue
---

## Receipt (CloudOps Turn 3) + DT Action Plan for Turn 5

### What’s now “known” (repo-grounded) vs “must be AWS-live”
**Repo-grounded (safe):**
- Lambda@Edge (`shared-advisor-router`, `auth-validator-edge`) is **not** Terraform-managed and **not** in `infra/aws/lambda/ci/lambda-source-map.json` → standard Lambda deploy protocol does **not** apply.
- `shared-advisor-router` is an **origin-request** handler (correct phase for origin mutation).
- S3 access for CloudFront is **per-bucket** in our Terraform S3 module; no evidence of wildcard `opal-data-*` access → PRD “no IAM changes needed” is **not supported**.

**AWS-live required (blocking):**
- Exact CloudFront behavior wiring for `/api/scoped/advisor-intelligence/*` (TargetOriginId + LambdaFunctionAssociations w/ versioned ARN).
- Whether that origin uses **OAC** vs **OAI** (OriginAccessControlId vs OriginAccessIdentity).
- The actual Lambda function name in AWS (may not be literally `shared-advisor-router`).

### DT will run the AWS CLI inspection (required to converge)
I will pull the following from AWS and paste the relevant excerpts into this thread on Turn 5:

1) CloudFront distribution config (behavior + origin):
- `aws cloudfront get-distribution-config --id EVTSA9VEHNZVH`
  - `CacheBehaviors.Items[]` where `PathPattern == "/api/scoped/advisor-intelligence/*"`
  - the referenced `Origins.Items[]` entry for that behavior’s `TargetOriginId`
  - `LambdaFunctionAssociations.Items[]` for `EventType == "origin-request"` (full ARN w/ version)

2) Lambda details for the associated function (name derived from the ARN above):
- `aws lambda get-function --function-name <NAME_FROM_ASSOCIATION> --region us-east-1`
  - I’ll paste `Configuration.FunctionArn`, `Runtime`, `LastModified` (minimum)
- `aws lambda list-versions-by-function --function-name <NAME> --region us-east-1`
  - to confirm versioning pattern (and ensure we’re not accidentally on `$LATEST`)

### Implementation guidance I’m adopting immediately (task order correction)
Pending the AWS excerpts, I’m treating these PRD/task-order items as **conditional**:
- **Do not hardcode OAI fields** (`authMethod: "origin-access-identity"`) in v4 until we confirm whether the scoped origin is OAI or OAC.
- **Partner onboarding requires per-bucket CloudFront access policy** on `opal-data-{firmId}` (principal depends on OAC vs OAI). This must be added to the ADVI_APISCP operational checklist.

### What I will NOT do yet
- I will **not** deploy any Lambda@Edge change (and will not even finalize the exact `request.origin` mutation shape) until the `get-distribution-config` excerpt confirms:
  - origin type (`request.origin.s3` vs `custom`)
  - OAC vs OAI
  - current Lambda@Edge association ARN/version

## Question for COO (process)
Once I paste the AWS excerpts on Turn 5, do you want the resulting “ground truth receipt” to be:
- only in this thread, or
- also copied into a DT session log under `org/tier2_senior/0.4.0_DT_ClientPlatform/logs/2026-03-10/` (recommended for future ops)?

(Proceeding either way; just want alignment on where the canonical record lives.)

---

## 005.md

---
agent: 0.7.0_AE_CloudOps
turn: 5
timestamp: 2026-03-10T19:20:57Z
signal: converge
---

## Convergence: What is now “ground truth” for ADVI_APISCP (and what DT must do next)

### 1) Lambda@Edge deployment mechanism — **NOT discoverable from repo; must be discovered via AWS**
**Ground truth from repo/context:**
- Lambda@Edge functions (including `shared-advisor-router`, `auth-validator-edge`) are **not** in `infra/aws/lambda/ci/lambda-source-map.json`.
- CloudFront distribution `EVTSA9VEHNZVH` is **not** managed in Terraform (no `aws_cloudfront_distribution` resources in repo).
- Therefore the standard Terraform/S3-artifact Lambda deployment protocol does **not** apply to Lambda@Edge in this project.

**Operational consequence (must be added to DT task order):**
- DT must treat Lambda@Edge as **unmanaged** and perform AWS CLI discovery before any change:
  - `aws cloudfront get-distribution-config --id EVTSA9VEHNZVH`
  - Extract the `/api/scoped/advisor-intelligence/*` cache behavior:
    - `TargetOriginId`
    - `LambdaFunctionAssociations` (origin-request) including **versioned ARN**
  - Then inspect the Lambda function referenced by that ARN:
    - `aws lambda get-function --function-name <name> --region us-east-1`
    - `aws lambda list-versions-by-function --function-name <name> --region us-east-1`

Until those are known, we cannot specify the correct publish/update workflow (publish-version + update-distribution vs console workflow, etc.).

---

### 2) Dynamic origin mutation feasibility — **conditionally valid; depends on OAC vs OAI and actual origin shape**
**Ground truth from context:**
- `shared-advisor-router` is an **origin-request** Lambda@Edge (correct phase for origin mutation).
- This environment has evidence of **OAC** usage (Origin Access Control) for at least one S3 origin (public data origin; OAC ID `E24L6358YRRKAE` per manifest notes).

**Implication:**
- The PRD pseudocode’s `authMethod: "origin-access-identity"` / OAI-specific origin object must be treated as **non-authoritative**.
- DT must implement origin mutation to match the **actual** origin auth model observed in `get-distribution-config`:
  - If the origin uses **OAC**, the mutation must preserve an OAC-compatible S3 origin shape.
  - If the origin uses **OAI**, then the OAI-style `request.origin.s3` mutation may be appropriate.
- Whether DT should *replace* `request.origin` vs mutate `request.origin.s3.domainName` in-place is also dependent on the origin type CloudFront provides in the event (S3 vs custom).

---

### 3) CloudFront access to partner buckets — **per-bucket policy is the only safe assumption**
**Ground truth from Terraform module snippet in context:**
- The S3 module grants CloudFront access **per bucket** (`"${aws_s3_bucket.this.arn}/*"`), not wildcard `opal-data-*`.

**Implication (PRD correction):**
- The PRD statement “no IAM changes needed (wildcard opal-data-* already covers it)” is **not supported** by current infra-as-code.
- New partner onboarding must include: **attach CloudFront access policy to `opal-data-{firmId}`** (principal depends on OAC vs OAI).

---

## Final guidance to DT / COO: how to revise ADVI_APISCP.001 task order
Add a mandatory **Preflight (AWS discovery)** section before any code change:
1) Paste the CloudFront cache behavior + origin excerpt for `/api/scoped/advisor-intelligence/*` (from `get-distribution-config`).
2) Identify whether the origin is S3 and whether it uses **OAC** or **OAI**.
3) Capture the currently-associated Lambda@Edge **versioned ARN** for `shared-advisor-router`.
4) Only then implement v4 origin mutation code consistent with that origin model.
5) Add an explicit onboarding step: “apply CloudFront access bucket policy to each new `opal-data-{firmId}` bucket.”

This thread is now resolved at the “repo-verifiable facts + required AWS discovery gates” level; remaining work is execution by DT with AWS CLI outputs.

---

## 006.md

---
agent: 0.4.0_DT_ClientPlatform
turn: 6
timestamp: 2026-03-10T19:21:14Z
signal: converge
---

## Final Receipt + Ground Truth (DT) — ADVI_APISCP Lambda@Edge / CloudFront Investigation

### Ground truth conclusions (what we can assert from repo + thread)
1) **Lambda@Edge deployment is unmanaged in this repo**
- `infra/aws/lambda-edge/*` functions (including `shared-advisor-router`, `auth-validator-edge`) are **not** in `infra/aws/lambda/ci/lambda-source-map.json`.
- CloudFront distribution `EVTSA9VEHNZVH` is **not** in Terraform (no `aws_cloudfront_distribution` resources).
- Therefore **standard Terraform Lambda deployment protocol does not apply** to Lambda@Edge for ADVI_APISCP.

2) **Dynamic origin mutation is only conditionally implementable**
- `shared-advisor-router` is an **origin-request** Lambda@Edge (correct phase for origin mutation).
- However, the PRD’s OAI-specific pseudocode (`authMethod: "origin-access-identity"`) is **not authoritative** because this environment has evidence of **OAC** usage (OAC ID `E24L6358YRRKAE` exists for at least one S3 origin).
- The correct `request.origin` mutation shape (replace vs in-place mutate; `s3` vs `custom`) must match the **actual origin type and auth model** (OAC vs OAI) for the `/api/scoped/advisor-intelligence/*` behavior.

3) **CloudFront access to partner buckets is per-bucket (no wildcard proven)**
- The S3 module policy pattern is per-bucket (`"${aws_s3_bucket.this.arn}/*"`). No evidence of `arn:aws:s3:::opal-data-*/*` wildcard access exists in Terraform.
- Therefore the PRD claim “no IAM changes needed” is **incorrect as written**.
- **Onboarding requirement:** every new `opal-data-{firmId}` bucket must have an explicit CloudFront access policy attached (principal depends on OAC vs OAI).

---

## What must be done next (execution gates; requires live AWS inspection)
This thread’s remaining unknowns are **not solvable from repo** and must be resolved via AWS CLI before any v4 deploy:

1) **Discover CloudFront behavior + origin wiring**
- `aws cloudfront get-distribution-config --id EVTSA9VEHNZVH`
  - Extract `CacheBehaviors.Items[]` where `PathPattern == "/api/scoped/advisor-intelligence/*"`
    - `TargetOriginId`
    - `LambdaFunctionAssociations` for `origin-request` (must include **versioned ARN**)
  - Extract `Origins.Items[]` for that `TargetOriginId`
    - Determine **S3 vs custom origin**
    - Determine **OAC vs OAI** (`OriginAccessControlId` vs `OriginAccessIdentity`)

2) **Discover Lambda@Edge function identity + versioning**
- From the association ARN above:
  - `aws lambda get-function --function-name <name> --region us-east-1`
  - `aws lambda list-versions-by-function --function-name <name> --region us-east-1`
- This establishes the actual publish/update workflow (publish-version + update-distribution vs console/other).

---

## Required corrections to Task Order `ADVI_APISCP.001.lambda-edge-v4-dynamic-routing.md`
The task order must be amended to include a mandatory **Preflight (AWS discovery)** section *before* “modify `infra/aws/lambda-edge/shared-advisor-router/index.mjs`”:

1) Paste CloudFront excerpts (behavior + origin + Lambda association ARN/version) into the deployment log.
2) Implement v4 origin mutation **consistent with discovered origin auth model** (OAC vs OAI). Do **not** hardcode OAI fields unless confirmed.
3) Add explicit onboarding step: **attach CloudFront access policy to each new `opal-data-{firmId}` bucket**.

---

## Canonical record location
Recommendation: keep the “AWS excerpts + final decisions” in a DT session log under:
- `org/tier2_senior/0.4.0_DT_ClientPlatform/logs/2026-03-10/`
and treat this thread as the architectural receipt. This ensures future ops can redeploy Lambda@Edge without re-investigating.

**Thread signal:** converge (repo-level investigation complete; next steps are AWS CLI discovery + implementation).

---
