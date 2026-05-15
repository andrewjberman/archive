# TO `ADHC_LEDGEH.001` — `shared-advisor-router` artifact-path error envelope

| Field | Value |
|---|---|
| **Project** | `ADHC_LEDGEH` (Lambda@Edge Defense Envelope Hardening) |
| **Owner** | `0.7.0_AE_CloudOps` |
| **Lane** | AE / lambda-edge / portal-auth-infrastructure |
| **Status** | `pending` — dispatch GO unblocked per COO routing 17:1XZ; ready for AE 0.7 pickup |
| **Dispatch_held** | `false` — CTO canonicalize (`5362d0295`) + COO dispatch GO both received |
| **Effort** | ~3-5h actual (~1d wall budget; CTO downsize per `5362d0295` canonicalize — Option A locked, scope narrowed, FIRMSEP.04 test surface known) |
| **PRD** | `docs/architecture/ADHC_LEDGEH.md` v0.2+canonicalize (CTO `5362d0295` git mv from AE drafts preserved AE authorship trail; CTO added §11 canonicalize entry + §7.Q3 ruling on top) |

---

## Goal

Replace the toxic primitive — CF `custom_error_response` collapsing S3 NoSuchKey / NoSuchBucket / 403 into SPA HTML at HTTP 200 for artifact-class (`*.json`) paths — with a structured JSON error envelope via new origin-response L@E `shared-advisor-router-response` (Option A per PRD §3.1; CTO Q2 ratified 16:55Z).

SPA deep-link behavior on `/portal/*` and root paths MUST remain intact (HTTP 200 + `/index.html` fallback on 404; preserved because the new L@E ONLY rewrites artifact-pattern responses, and SPA paths continue to flow through CF `custom_error_response`).

---

## Pre-write Phase

Mandatory before writing code (per PRD §5):

1. `comp-routes behaviors` — enumerate all CloudFront behaviors under `portal-auth/cloudfront-distribution.tf`; identify which behaviors fire on `/api/scoped/*` artifact paths vs `/portal/*` HTML paths. Output informs Option B behavior-split scope.
2. `comp-routes trace partner_analytics_annual` — full CF → auth-validator-edge → shared-advisor-router → S3 path; identifies all consumer/producer edges on this trace.
3. `comp-iam service shared-advisor-router` — baseline IAM ops (expected: 4 ops — s3:GetObject ×3 via OAI + headers). Option A may add a sibling Lambda with distinct role; comp-iam re-run post-deploy gates as acceptance.
4. `comp-blast shared-advisor-router` — downstream consumers of the L@E. Confirm no consumer expects current HTML-collapse semantics.

Optional but recommended:
- Read `infra/aws/lambda-edge/_shared/firm-config.mjs` to confirm FIRM_BUCKET_MAP shape (for any new L@E that may reference it).
- Read `infra/aws/lambda-edge/auth-validator-edge/index.mjs` to confirm X-Firm-Id injection contract (consumed by any new origin-response L@E if Option A).

---

## Scope (Option A LOCKED per CTO Q2 ratify 16:55Z)

### Code
- New L@E at `infra/aws/lambda-edge/shared-advisor-router-response/index.mjs` (~15-20 LOC handler)
- Handler responsibilities:
  - Inspect `response.status` from CF; if `403` / `404` AND request URI matches artifact pattern (`/api/scoped/*` OR `*.json` extension), replace response body with structured JSON envelope:
    ```javascript
    {
      "error": "artifact_not_found",
      "uri": "<request.uri>",
      "bucket": "<firm-bucket-resolved-by-shared-advisor-router>",
      "firmId": "<X-Firm-Id-header>",
      "status": 404,
      "request_id": "<cloudfront-request-id-header>"
    }
    ```
  - Set `Content-Type: application/json` + `Cache-Control: no-cache` on response headers
  - Preserve HTTP status (404 stays 404; do NOT pin to 200)
  - For HTML-like paths or non-error responses: pass through unchanged
- `bun build` produces `index.mjs.zip` for L@E deploy (mirror existing shared-advisor-router build pipeline)

### Terraform
- New `aws_lambda_function.shared_advisor_router_response` resource in `infra/aws/terraform/portal-auth/lambda-edge.tf` (mirror existing `aws_lambda_function.shared_advisor_router` shape; `runtime = nodejs20.x`, `memory_size = 128`, `timeout = 5`)
- New `aws_lambda_function_association` (or equivalent) on the `aws_cloudfront_distribution` cache behavior for `/api/scoped/*` path pattern: `event_type = "origin-response"`, `lambda_arn = aws_lambda_function.shared_advisor_router_response.qualified_arn`
- L@E IAM role `lambda-edge-execution-role` (existing) — same role as existing L@E; no new IAM
- `aws_cloudwatch_log_group` for the new Lambda (optional but standard)

### Source-map
- New entry in `infra/aws/lambda/ci/lambda-source-map.json`:
  ```json
  "shared-advisor-router-response": {
    "source_dir": "infra/aws/lambda-edge/shared-advisor-router-response",
    "files": ["index.mjs"],
    "tf_file": "infra/aws/terraform/portal-auth/lambda-edge.tf",
    "tf_resource": "aws_lambda_function.shared_advisor_router_response",
    "artifact_s3_key": "portal-auth/shared-advisor-router-response.zip",
    "iam_role": "lambda-edge-execution-role"
  }
  ```
  Plus `last_deployed_commit` + `last_deployed_at` + `artifact_sha256` populated by `record-terraform-deploy.sh` on first deploy.

### Deploy cycle (CLAUDE.md Rules 1-6 + 11)
1. Write code + build zip via existing L@E `build-and-upload.sh`
2. Write Terraform
3. Update source-map manually OR via `record-terraform-deploy.sh`
4. `safe-commit.sh` per ADHC_OWNPTH.007 — atomic commit with new L@E + Terraform + source-map
5. `terraform plan -out=lambda-edge.tfplan` — expect new Lambda + new behavior association (1+ diff)
6. `terraform apply lambda-edge.tfplan` — verify ApplyComplete
7. Re-run `terraform plan` — verify 0-diff
8. Tag: `git tag -a portal-auth-v{X.Y.Z+1} -m "..."` per existing portal-auth tag series
9. Push with `--follow-tags`
10. **L@E propagation wait ~15-30min** before integration test

---

---

## Acceptance Criteria

Per PRD §8:

1. **Empirical P1 regression reproduction:** TO-VAL sweep (`ADHC_LEDGEH.VAL`) reproduces the 2026-05-14 P1 failure mode pre-fix on a synthetic harness or against historical CloudFront logs; confirms post-fix yields parseable JSON error envelope (Option A) or native non-2xx (Option B), NOT toxic SPA HTML at HTTP 200.
2. **SPA deep-link routes UNAFFECTED:** `/portal/advisor-intelligence/...` and root deep-links still return `/index.html` at HTTP 200 on 404 fallback. Manual UAT via browser hard-refresh on a deep-link URL.
3. **React Query consumes the error correctly:** Verified via FE devtools or integration test that `useQuery` enters `error` state on the failure path, NOT `data: null`. Cross-reference with DE 0.4 FE-side fix `cb62f069`.
4. **CloudWatch logs show normal traffic pattern post-deploy:** No error-class spike in `/aws/lambda/us-east-1.shared-advisor-router` or (Option A) the new `shared-advisor-router-response` log group.
5. **comp-iam service post-deploy:** Existing 4 ops baseline preserved; (Option A) new Lambda comp-iam shows expected ops set.
6. **`terraform plan` 0-diff after apply** — standard CLAUDE.md Rule 2 compliance.
7. **Andrew empirical UAT on Inflection partner-demo Annual interval:** Renders correctly post-deploy (validates that the toxic primitive elimination + DE 0.4 FE fix combination delivers correct behavior end-to-end).

---

## RAVC Posture

- **RAVC1:** TO authored 2026-05-14 16:55Z (this file)
- **RAVC2:** dispatch_held=true until CTO architectural ratify on Option A vs Option B fork lands (PRD v0.2)
- **RAVC3:** TO progresses on dispatch; AE 0.7 ships per Lambda Deployment Protocol
- **RAVC4:** ship evidence packet to COO (commit hash, tag, terraform plan 0-diff, comp-iam post-deploy, CW log baseline) + DE 0.4 cross-reference
- **RAVC5:** COO acceptance gates TO-VAL Phase 3 sweep + Andrew UAT

---

## Risks + Mitigations

Per PRD §9.

---

## Compliance Notes

- **CLAUDE.md Rule 1:** Terraform-only Lambda deploy — yes (no `aws lambda update-function-code`)
- **CLAUDE.md Rule 2:** Commit before apply — yes
- **CLAUDE.md Rule 3:** Dependencies in Layers — N/A (L@E does not use Layers; nodejs20.x with no external deps beyond stdlib + `_shared/firm-config.mjs`)
- **CLAUDE.md Rule 4:** Source-map registered — yes (Option A new entry; Option B no Lambda change)
- **CLAUDE.md Rule 5:** Lambda sized deliberately — yes (128MB / 5s for origin-response L@E per existing pattern)
- **CLAUDE.md Rule 6:** Tag after deploy — yes (portal-auth-v{X.Y.Z+1})
- **CLAUDE.md Rule 11:** Verify parity — yes (terraform plan 0-diff after apply)
- **CLAUDE.md Rule 14a:** safe-commit.sh per ADHC_OWNPTH.007 — yes
- **No emojis in code (CLAUDE.md "Code Quality"):** ASCII only; no Unicode above U+007F in handler or logs

---

## Cross-references

- **PRD:** `docs/architecture/ADHC_LEDGEH.md` v0.1
- **Sister TO:** `ADHC_LEDGEH.VAL.ae-empirical-regression-sweep` (Phase 3 validation; gates this TO's RAVC5 close)
- **DE 0.4 FE-side fix:** `cb62f069` (complementary; ships independently)
- **P1 brief:** `docs/briefs/inf_snapshot_segment_analytics_interval_data_gaps_20260514.md`
- **AE 0.7 Phase 1.1 evidence:** RAVC4 to COO 2026-05-14 16:39Z; CW pull scripts in `.runtmp/`
- **Related ADHC sister:** `ADHC_DRIFTD` (deploy-record hardening; v0.1 SHIPPED 2026-05-13)

---

## Versioning

- **v0.1** — 2026-05-14 ~16:55Z — initial author; staged + dispatch_held; gates on CTO Option A/B ratify
- **v0.2** — 2026-05-14 ~17:05Z — Option A locked per CTO Q2 ratify 16:55Z; Option B section stripped (path-scoped CF behavior approach ruled out due to distribution-level `custom_error_response` constraint); staged + dispatch_held=true gating now on COO per-TO dispatch GO only
- **v0.3** — 2026-05-14 ~17:20Z — CTO canonicalize at `5362d0295` (git mv from AE drafts/ to docs/architecture/ADHC_LEDGEH.md preserving AE authorship trail; CTO commit added §11 canonicalize entry + §7.Q3 ruling on top). FIRMSEP.04 test surface extension AC added per CTO Q3 ruling. Effort estimate downsized ~3-5h actual per CTO. Status flipped to `pending` (dispatch_held=false); COO per-TO dispatch GO unblocked. Sequencing per CTO `.029b → .027 → .028 → LEDGEH.001` lock — natural Wave 1+2 momentum into LEDGEH ~3-4d wall from now.
