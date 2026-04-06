# DEBT_1STRUN.001 — Infrastructure Technical Debt Audit

**Agent:** 0.7.0_AE_CloudOps
**Date:** 2026-04-06
**Task Order:** DEBT_1STRUN.001.scan
**Status:** Phase 1 Complete (inventory + coverage gaps)

---

## Executive Summary

| Resource Type | In AWS | In Repo/TF | Coverage | Gap |
|--------------|--------|------------|----------|-----|
| Lambda Functions | 136 | 105 (source-map) | 77% | 31 unmapped |
| EC2 Instances | 13 | 10 (manifest services) | 62% | 8 untracked instance IDs |
| S3 Buckets | 33 | 10 (in .tf files) | 30% | 23 not in Terraform |
| DynamoDB Tables | 30 | 18 (in .tf files) | 60% | 12 not in Terraform |
| IAM Roles (Opal) | 43 | 28 (in .tf files) | 65% | 15 not in Terraform |
| TF Pipelines | 16 dirs | 14 S3 state keys | 88% | 3 dirs with no state |

**Codebase scope:** 6,610 files in `infra/aws/`, 1.87M lines, 67 MB

---

## 1. Lambda Functions — 31 Unmapped

These functions exist in AWS but have no entry in `lambda-source-map.json`.
CI drift detection, parity checks, and build tooling cannot track them.

### 1a. Trade/Recon Subsystem (10 functions) — HIGHEST PRIORITY

| Function | Runtime | Memory | Timeout |
|----------|---------|--------|---------|
| `trade-auth-handler` | python3.11 | 256MB | 30s |
| `trade-authorizer` | python3.11 | 128MB | 10s |
| `trade-dashboard-api` | python3.11 | 512MB | 60s |
| `trade-identifier-cache` | python3.11 | 256MB | 30s |
| `trade-parquet-batch-export` | python3.11 | 1024MB | 300s |
| `trade-recon-api` | python3.11 | 256MB | 60s |
| `trade-recon-auth` | python3.11 | 256MB | 30s |
| `trade-recon-authorizer` | python3.11 | 128MB | 10s |
| `trade-recon-processor` | python3.11 | 1024MB | 300s |
| `trade-submission-handler` | python3.11 | 256MB | 30s |
| `trade-workflow-handler` | python3.11 | 1024MB | 120s |

**Assessment:** Entire trade subsystem is outside Terraform management. No TF pipeline directory, no source map entries, IAM roles (`trade-recon-lambda-role`, `trade-submission-lambda-role`) not in any .tf file. Likely deployed via console or legacy scripts.

### 1b. Edge/Routing Functions (5 functions)

| Function | Runtime | Memory | Notes |
|----------|---------|--------|-------|
| `auth-validator-edge` | nodejs20.x | 128MB | CloudFront Lambda@Edge |
| `cache-control-injector` | nodejs20.x | 128MB | CloudFront origin response |
| `public-data-router` | nodejs20.x | 128MB | CloudFront viewer request |
| `tier-router-edge` | nodejs20.x | 128MB | CloudFront routing |
| `shared-advisor-router` | nodejs20.x | 128MB | CloudFront routing |

**Assessment:** CloudFront edge functions. Source exists in `infra/aws/lambda/` but not mapped. Managed by `portal-auth` TF pipeline but not registered in source-map.

### 1c. Security/Infrastructure Monitoring (4 functions)

| Function | Runtime | Memory | Notes |
|----------|---------|--------|-------|
| `access-anomaly-scanner` | python3.11 | 256MB | Security audit |
| `cost-anomaly-scanner` | python3.11 | 256MB | Cost monitoring |
| `ec2-auto-shutdown-enforcer` | python3.11 | 128MB | Has own local TF (not S3 backend) |
| `ec2-runtime-monitor` | python3.11 | 128MB | EC2 cost tracking |

**Assessment:** `ec2-auto-shutdown-enforcer` has its own TF at `infra/aws/lambda/ec2-auto-shutdown-enforcer/main.tf` with local state (not S3 backend). Others deployed ad-hoc.

### 1d. Market Overview Pipeline (3 functions)

| Function | Runtime | Notes |
|----------|---------|-------|
| `market-update-data-aggregator` | python3.12 | |
| `market-update-exporter` | python3.12 | |
| `market-update-generator` | python3.12 | |

**Assessment:** Part of market-overview TF pipeline but not in source map.

### 1e. Other Unmapped (6 functions)

| Function | Notes |
|----------|-------|
| `bd-allocation-file-checker` | Inline in `bd-pipeline/lambdas.tf` (not modularized) |
| `opal-bd-transaction-consolidator` | BD pipeline |
| `deck-generation` | Has own TF pipeline |
| `infrastructure-daily-snapshot` | Infrastructure audit |
| `opal-session-analytics` | Portal analytics |
| `opal-cloudfront-market-generator` | Market data for CloudFront |

### 1f. Test Functions (2 functions) — DELETE CANDIDATES

| Function | Notes |
|----------|-------|
| `test-yfinance-simple` | Test function, still deployed |
| `yfinance-aapl-test` | Test function, runtime=None (broken) |

---

## 2. EC2 Instances — 8 Untracked

| Instance ID | Name | Type | State | Issue |
|------------|------|------|-------|-------|
| `i-040a8cbaaaf295d95` | bd-all-historical-snapshots | r6i.4xlarge | stopped | Not in manifest |
| `i-090ae819ddc8ee5ea` | bd-snapshot-gen-v3 | r6i.4xlarge | stopped | Not in manifest |
| `i-06dfcb7dfbfa7f78b` | bd-snapshot-PRODUCTION | r6i.4xlarge | stopped | Not in manifest |
| `i-074bfc40ee049dc62` | bd-gold-detail-generator | r6i.xlarge | stopped | Service exists, instance_id=null |
| `i-05ad83c1c075de14b` | historical-prices-fetcher | t3.xlarge | stopped | Not in manifest |
| `i-0e418d2fc0b891235` | docker-builder-temp | t3.medium | stopped | Not in manifest, likely disposable |
| `i-06376c11d8b3c3443` | seeking-alpha-scraper | t3.medium | stopped | Service exists, instance_id=null |
| `i-07ebae29a16e43ed1` | seeking-alpha-scraper | t3.medium | stopped | Service exists, instance_id=null |

**Assessment:**
- 3x `bd-snapshot-*` instances (r6i.4xlarge each) appear to be legacy/one-off gold generation runs. All stopped. If no longer needed, should be terminated to avoid EBS costs.
- `docker-builder-temp` is clearly disposable.
- `historical-prices-fetcher` not tracked anywhere in manifest.
- `bd-gold-detail-generator` and `seeking-alpha-scraper` have manifest service entries but null instance IDs — need `sync-ec2-manifest.sh`.

---

## 3. S3 Buckets — 23 Not in Terraform

### 3a. Legacy/Pre-Terraform (likely console-created)

| Bucket | Purpose | Action |
|--------|---------|--------|
| `opalinvest-portal` | Portal static hosting (v1) | Active, serves portal |
| `opal-data-schwab` | Schwab data (RPS, ACC, TRN) | Active, critical |
| `opal-data-trade-submissions` | Trade form uploads | Active |
| `opal-cloudfront-logs-313476888478` | CloudFront access logs | Active |
| `opal-cloudtrail-logs-313476888478` | CloudTrail audit logs | Active |
| `opal-infrastructure-snapshots` | Infra snapshots (empty) | Likely unused |

### 3b. Legacy Code Buckets (superseded by lambda-artifacts)

| Bucket | Purpose | Action |
|--------|---------|--------|
| `opal-code-factorscanner-v2` | Old Lambda deploy zips | Superseded |
| `opal-code-smartx-v2` | Old SmartX deploy zips | Superseded |
| `opal-lambda-code-archive` | Old Lambda archive | Superseded |
| `opal-ci-staging` | CI staging artifacts | Partially active |

### 3c. Trade Subsystem (5 buckets)

| Bucket | Purpose |
|--------|---------|
| `opal-trade-form-ui` | Trade form static site |
| `opal-trade-recon-confirms` | Recon confirmations |
| `opal-trade-recon-reports` | Recon reports |
| `opal-trade-recon-requests` | Recon requests |
| `opal-trade-recon-ui` | Recon dashboard static site |

### 3d. Other

| Bucket | Purpose |
|--------|---------|
| `ajb-workflow` | Personal/workflow bucket |
| `opal-313476888478-wyncht` | HTML report hosting |
| `opal-analytics-dashboard` | Analytics static site |
| `opal-data-aaii-sentiment` | AAII sentiment data (legacy) |
| `opal-data-aaii-v2` | AAII data (duplicate?) |
| `opal-market-data-v2` | Market data (FRED, etc.) |
| `opal-market-update` | Market update data |
| `smartx-exports-ajb327-20250118` | One-time SmartX export |

---

## 4. DynamoDB Tables — 12 Not in Terraform

| Table | Likely Owner | Notes |
|-------|-------------|-------|
| `causality-generations` | causality pipeline | No TF state for causality |
| `causality-saved-analyses` | causality pipeline | No TF state for causality |
| `market-updates` | market-overview | |
| `opal-firms` | portal-auth | Core auth data |
| `opal-invitations` | portal-auth | |
| `opal-offices` | portal-auth | |
| `opal-pii-lookup` | schwab-anonymizer | PII hash lookup |
| `opal-sessions` | portal-auth | Session management |
| `trade-recon-jobs` | trade subsystem | |
| `trade-security-identifiers` | trade subsystem | |
| `trade-users` | trade subsystem | |
| `user-permissions` | portal-auth | |

---

## 5. IAM Roles — 15 Not in Terraform

| Role | Likely Purpose |
|------|---------------|
| `MoltbotEC2Role` | Moltbot EC2 instance (console-created) |
| `bd-merge-daily-lambda-role` | Legacy BD merge Lambda |
| `bd-pipeline-task-role` | BD pipeline tasks (legacy?) |
| `ec2-auto-shutdown-enforcer-role` | Has local TF, not S3 backend |
| `ec2-ssm-role` | Generic SSM role |
| `infrastructure-ops-lambda-role` | Infra monitoring |
| `infrastructure-snapshot-role` | Daily snapshot Lambda |
| `market-data-generator-lambda-role` | Market data |
| `market-update-lambda-role` | Market updates |
| `opal-layer3-ec2-role` | News layer3 EC2 |
| `opal-smartx-lambda-role` | Legacy SmartX |
| `portal-auth-lambda-role` | Portal auth (should be in portal-auth TF) |
| `security-sweep-dedicated-role` | Security scanning |
| `trade-recon-lambda-role` | Trade recon (no TF pipeline) |
| `trade-submission-lambda-role` | Trade submission (no TF pipeline) |

---

## 6. Terraform Pipeline Gaps

### 6a. Directories with NO S3 state backend (3)

| Directory | .tf files | Issue |
|-----------|----------|-------|
| `causality` | 1 | Local state only — never migrated to S3 |
| `seeking-alpha` | 1 | Local state only |
| `security-scanner-pipeline` | 5 | S3 key is `security-scanner/` (name mismatch) |

### 6b. S3 state key with no matching directory (1)

| State Key | Issue |
|-----------|-------|
| `lambda-layers/` | Managed by shared-infra? No dedicated TF dir |

---

## 7. Priority Remediation Recommendations

### P0 — Immediate (cost/security)

1. **Terminate disposable EC2 instances:** `docker-builder-temp`, 3x `bd-snapshot-*` (if confirmed unused). EBS costs accumulate even when stopped.
2. **Delete test Lambdas:** `test-yfinance-simple`, `yfinance-aapl-test` — dead code in production.
3. **Run `sync-ec2-manifest.sh`** to populate null instance_ids for `bd-gold-detail-generator`, `seeking-alpha-scraper`.

### P1 — Source Map Gap (CI visibility)

4. **Add 31 unmapped Lambdas to `lambda-source-map.json`** — enables parity checks and drift detection for all functions.
5. **Migrate `ec2-auto-shutdown-enforcer` TF to S3 backend** — local state is fragile.

### P2 — Terraform Coverage (infrastructure-as-code)

6. **Trade subsystem:** 10 Lambdas + 5 S3 buckets + 3 DynamoDB tables + 2 IAM roles completely outside Terraform. Needs its own pipeline directory.
7. **Causality + Seeking Alpha:** Migrate to S3 backend.
8. **Import portal-auth DynamoDB tables** (`opal-firms`, `opal-sessions`, `user-permissions`, `opal-offices`, `opal-invitations`) into portal-auth TF pipeline.
9. **Import critical S3 buckets** (`opal-data-schwab`, `opalinvest-portal`) into appropriate TF pipelines.

### P3 — Cleanup (tech debt reduction)

10. **Deduplicate S3 buckets:** `opal-data-aaii-sentiment` vs `opal-data-aaii-v2` (likely same data). `opal-market-data-v2` vs `opal-market-update`.
11. **Retire legacy code buckets:** `opal-code-factorscanner-v2`, `opal-code-smartx-v2`, `opal-lambda-code-archive` (superseded by `opal-313476888478-lambda-artifacts`).
12. **Audit stale IAM roles:** `bd-merge-daily-lambda-role`, `bd-pipeline-task-role`, `opal-smartx-lambda-role` may be unused.

---

## Methodology

- **Perceive:** `org/modules/perceive/filesystem_scanner` on `infra/aws/` (6,610 files)
- **AWS Discovery:** `aws lambda list-functions`, `aws s3 ls`, `aws dynamodb list-tables`, `aws ec2 describe-instances`, `aws iam list-roles`
- **Coverage Audit:** `org/modules/adapt/coverage_auditor` pattern — set difference between AWS live resources and repo declarations (source-map, EC2_MANIFEST, .tf files)
- **Cross-Reference:** Regex search across all .tf files for IAM role names, DynamoDB table names, S3 bucket names
