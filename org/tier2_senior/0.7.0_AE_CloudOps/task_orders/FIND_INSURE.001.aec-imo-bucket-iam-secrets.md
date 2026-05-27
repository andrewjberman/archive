# FIND_INSURE.001 — opal-data-imo bucket + IAM + secrets wiring

**Project:** [FIND_INSURE](../../../projects/FIND_INSURE.json)
**PRD:** `docs/architecture/FIND_INSURE.md` §3.1, §3.3, §4 Phase 0 deliverable 1+2
**Pod:** 0.7.0_AE_CloudOps
**Lane:** AE base
**Author:** 2.0.0_SA_COO 2026-05-27T~15:50Z
**Status:** pending — GO via [DRIVE] MCP this cycle
**Sizing:** ~1-2h wall

<status>pending</status>

---

## Objective

Provision `s3://opal-data-imo` bucket via Terraform with documented medallion prefix conventions; provision Lambda execution IAM role for FIND_INSURE.* functions; wire `find-insure/bright-data/api-key` (existing per Andrew) + `find-insure/lusha-ai/api-key` (confirm/create) Secrets Manager entries into role access.

Parallel-feasible against ADVI_DEMOV1.012 Fire 1 monitoring window — infra-class, mechanical, low-touch on the .012 critical path.

## Acceptance criteria

- **AC1.** Terraform applied 0-diff with `aws_s3_bucket.opal_data_imo` provisioned; same account, same region as existing opal-data-* buckets; default-encryption + versioning enabled; bucket policy documented in module README.
- **AC2.** README at `infra/aws/terraform/opal-data-imo/README.md` (or module-attached) documents the bronze/silver/gold/serving prefix conventions per PRD §3.2; empty marker objects `corp/.keep` + `serving/.keep` placed.
- **AC3.** IAM execution role `find-insure-lambda-role` provisioned: read/write to `s3://opal-data-imo/*`; read from Secrets Manager paths `find-insure/bright-data/*` + `find-insure/lusha-ai/*`; CloudWatch Logs write; standard Lambda assume-role trust.
- **AC4.** Secrets Manager: `find-insure/bright-data/api-key` confirmed accessible by role (existing per Andrew); `find-insure/lusha-ai/api-key` either confirmed (if Andrew/IT has provisioned) OR explicit PRD §11 blocking item 3 routed to Andrew (do NOT block AC1-AC3 on AC4 lusha — bright-data alone is enough for Phase 1).
- **AC5.** Lambda source-map: register the IAM role + bucket in any source-map files that gate CI drift detection. No code Lambdas yet (Phase 0 only provisions; Phase 1 lands actual functions).
- **AC6.** Standard CLAUDE.md discipline: Terraform-only deploy + safe-apply checkpoint + tag `find-insure-v0.1.0` post-0-diff + `record-terraform-deploy.sh`.

## RAVC2 deliverable

`[RAVC2-Request] FIND_INSURE.001 — bucket + IAM + secrets` to ws COO with: terraform apply 0-diff confirmation, bucket ARN + ARN, IAM role ARN, secrets-access verification (aws secretsmanager get-secret-value via role-assume probe OR cite-existing test), tag commit hash. AE 0.7 CC ws CTO (PRD architect).

## Notes

- Bright Data secret pre-existing per Andrew direct (PRD §3.3) — confirm path naming + permission only; do NOT recreate.
- LushaAI secret status flagged in FIND_INSURE.json blocking #3 — if not present, surface as RAVC2 finding + route to Andrew via [SYNC] MCP; do NOT block bucket+IAM ship.
- comp-iam service check after iam.tf edit; comp-iam gaps after apply.
- Parallel to ADVI_DEMOV1.012 Fire 1 monitoring acceptable per /work cron + /allocation cap-status (6 of 16; AE 0.7 has parallel capacity for low-touch infra during monitoring window).

— ws COO 2026-05-27T15:50Z
