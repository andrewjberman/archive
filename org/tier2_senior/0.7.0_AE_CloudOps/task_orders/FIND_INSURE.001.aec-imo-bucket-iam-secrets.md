# FIND_INSURE.001 — opal-data-imo bucket + IAM + secrets wiring

**Project:** [FIND_INSURE](../../../projects/FIND_INSURE.json)
**PRD:** `docs/architecture/FIND_INSURE.md` v0.3 §3 + §4 Phase 0; ws CTO `0719c576f` 2026-05-27 v0.3 absorption of ws CVO arch-brief `8fb6f7d94`
**Pod:** 0.7.0_AE_CloudOps
**Lane:** AE base
**Author:** 2.0.0_SA_COO 2026-05-27T~15:50Z; v0.3 AC expansion 2026-05-27T~16:30Z
**Status:** pending — GO held on .012 Fire 1 RAVC2-Accept per CVO ADDITIVE-2 timing gate (unchanged across v0.2→v0.3)
**Sizing:** ~2-3h wall (expanded from ~1-2h per v0.3 scope additions)

<status>complete</status>

---

## Amendment 2026-05-27T~16:30Z (v0.3 architectural absorption per CTO `0719c576f` + CVO brief `8fb6f7d94`)

Per ws CTO v0.3 absorption of ws CVO architectural brief:
- **7 root prefixes** (not 4): `corp/` + `serving/` + `code/` + `config/` + `telemetry/` + `qa/` + `archives/` per inf-pipeline canonical
- **SSE-S3 + versioning Enabled + Public-Access-Block all-true + SKIP CORS** mirror inf-pipeline `s3.tf`
- **8-rule lifecycle policy** for cost discipline (specifics per PRD v0.3 §3.x or CVO brief §3)
- **IAM least-privilege detail**: delete-restrict on `gold/silver/serving/config/code` (structurally protected); delete-allowed on `bronze/* + telemetry/* + qa/*` only
- **Secrets Manager namespace pre-allocation**: `find-insure/bright-data/*` + `find-insure/lusha-ai/*` + `find-insure/job-board/*` (Phase 2 Part B HAR-endpoint reservation per CVO §5.2)

Lusha key already routed via CTO `[SYNC HANDOFF]` to AE 0.7 (your scope to provision under `find-insure/lusha-ai/api-key` per CTO MCP).

## Objective

Provision `s3://opal-data-imo` bucket via Terraform with 7-prefix layout + SSE-S3 + versioning + PAB + 8-rule lifecycle; provision `find-insure-lambda-role` IAM execution role with least-privilege per CVO §5.1 (delete-restricted); wire 3-namespace Secrets Manager access (bright-data + lusha-ai + job-board reserved).

Parallel-feasible against ADVI_DEMOV1.012 Fire 1 monitoring window — but timing-held per CVO ADDITIVE-2 until post-.012-RAVC2-Accept (~post-19:00Z).

## Acceptance criteria

- **AC1.** Terraform applied 0-diff with `aws_s3_bucket.opal_data_imo` provisioned; same account + region as existing opal-data-* buckets; **SSE-S3 + versioning Enabled + Public-Access-Block all-true + SKIP CORS** per CVO brief §3 inf-pipeline mirror. **8-rule lifecycle policy** per PRD v0.3 §3 / CVO brief §4 cost-discipline set. Bucket policy documented in module README.
- **AC2.** README at `infra/aws/terraform/opal-data-imo/README.md` documents the **7 root prefixes** per PRD v0.3: `corp/` (per-IMO medallion) + `serving/` (consolidated tables) + `code/` (HIGH Phase 0; Lambda artifacts) + `config/` (HIGH Phase 0; centralized) + `telemetry/` (MEDIUM Phase 0; pipeline-run logs) + `qa/` (MEDIUM Phase 0; QA artifacts) + `archives/` (LOW Phase 0; cold storage). Marker objects `corp/.keep` + `serving/.keep` + `code/.keep` + `config/.keep` + `telemetry/.keep` + `qa/.keep` + `archives/.keep` placed.
- **AC3.** IAM execution role `find-insure-lambda-role` provisioned per CVO brief §5.1 least-privilege:
  - **S3 read/write** to `s3://opal-data-imo/*`
  - **S3 delete RESTRICTED** to `bronze/* + telemetry/* + qa/*` only (gold/silver/serving/config/code structurally protected from delete at role level — anti-defect per CVO §5.1)
  - **Secrets Manager read** from 3 namespaces: `find-insure/bright-data/*` + `find-insure/lusha-ai/*` + `find-insure/job-board/*` (job-board reserved for Phase 2 Part B HAR-endpoint credentials per CVO §5.2)
  - **CloudWatch Logs write** for Lambda execution
  - **EventBridge** (per PRD v0.3 §3.x orchestration sketch)
  - Standard Lambda assume-role trust policy
- **AC4.** Secrets Manager namespace verification:
  - `find-insure/bright-data/api-key` confirmed accessible by role (existing per Andrew direct PRD §3.3)
  - `find-insure/lusha-ai/api-key` provisioned per CTO `[SYNC HANDOFF]` direct routing (key + tagging + EnvVar contract spec received from CTO MCP)
  - `find-insure/job-board/*` namespace reserved (no key required at Phase 0; reservation only — actual keys land at Phase 2 Part B HAR-staged-attack)
- **AC5.** Lambda source-map: register the IAM role + bucket in `infra/aws/lambda/ci/lambda-source-map.json` per CLAUDE.md Rule 4. No code Lambdas yet (Phase 1 lands actual functions); placeholder structural entries acceptable.
- **AC6.** Standard CLAUDE.md discipline: Terraform-only deploy (Rule 1) + safe-apply checkpoint (Rule 18) + tag `find-insure-v0.1.0` post-0-diff + `record-terraform-deploy.sh` integration. comp-iam service + comp-iam gaps after apply.

## RAVC2 deliverable

`[RAVC2-Request] FIND_INSURE.001 — bucket + IAM + secrets` to ws COO with: terraform apply 0-diff confirmation, bucket ARN + ARN, IAM role ARN, secrets-access verification (aws secretsmanager get-secret-value via role-assume probe OR cite-existing test), tag commit hash. AE 0.7 CC ws CTO (PRD architect).

## Notes

- Bright Data secret pre-existing per Andrew direct (PRD §3.3) — confirm path naming + permission only; do NOT recreate.
- LushaAI secret status flagged in FIND_INSURE.json blocking #3 — if not present, surface as RAVC2 finding + route to Andrew via [SYNC] MCP; do NOT block bucket+IAM ship.
- comp-iam service check after iam.tf edit; comp-iam gaps after apply.
- Parallel to ADVI_DEMOV1.012 Fire 1 monitoring acceptable per /work cron + /allocation cap-status (6 of 16; AE 0.7 has parallel capacity for low-touch infra during monitoring window).

— ws COO 2026-05-27T15:50Z
