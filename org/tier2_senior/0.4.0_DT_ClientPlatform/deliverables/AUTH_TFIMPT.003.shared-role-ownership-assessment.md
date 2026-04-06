# AUTH_TFIMPT.003 — Shared Role Ownership Assessment

**Agent:** 0.4.0_DT_ClientPlatform
**Date:** 2026-04-06
**Role:** `opal-portal-lambda-role`
**ARN:** `arn:aws:iam::313476888478:role/opal-portal-lambda-role`

---

## 1. Function Inventory (13 functions)

| # | Function | TF Pipeline | Category |
|---|----------|-------------|----------|
| 1 | opal-market-overview-tiered-generator | market-overview | data/market |
| 2 | opal-market-regime-classifier | market-overview | data/market |
| 3 | opal-portal-fear-greed-fetcher | market-overview | data/market |
| 4 | opal-portal-volatility-fetcher | market-overview | data/market |
| 5 | opal-portal-data-proxy | market-overview | data/portal |
| 6 | opal-trending-topics-portal-publisher | market-overview | data/news |
| 7 | opal-cloudfront-market-generator | market-overview (inferred) | data/market |
| 8 | opal-news-ai-sentiment | news-pipeline | data/news |
| 9 | opal-portal-authorizer | portal-auth | auth |
| 10 | opal-session-analytics | portal-auth (inferred) | auth |
| 11 | finbert-batch-processor | NOT_IN_TF | data/news |
| 12 | opal-infrastructure-monitor | NOT_IN_TF | ops |
| 13 | infrastructure-daily-snapshot | NOT_IN_TF | ops |

### Pipeline Distribution

| Pipeline | Count | Functions |
|----------|-------|-----------|
| **market-overview** | **7** | tiered-generator, regime-classifier, fear-greed, volatility, data-proxy, trending-publisher, cloudfront-market |
| **news-pipeline** | 1 | ai-sentiment |
| **portal-auth** | 2 | portal-authorizer, session-analytics |
| **NOT_IN_TF** | 3 | finbert, infrastructure-monitor, daily-snapshot |

**Primary user: market-overview (7/13 = 54%)**

---

## 2. Policy Inventory (12 inline policies, 0 managed)

| Policy | Actions | Resources | Used By |
|--------|---------|-----------|---------|
| opal-portal-s3-read | s3:Get/Put/Delete/List | 8 buckets (smartx, portal-data, portal-v2, news-v2, market-data-v2, aaii-sentiment, bd) | All data functions |
| opal-portal-dynamodb | dynamodb CRUD | 5 tables (market-data, news-articles, data-smartx, trending-daily, keyword-intelligence) | Market + news functions |
| opal-portal-logs | logs:Create/Put | /aws/lambda/* (us-east-2) | All functions |
| opal-portal-secrets | secretsmanager:Get | opal/smartx/config, opal/external-apis | data-proxy, fetchers |
| opal-sessions-dynamodb | dynamodb full CRUD | opal-sessions table | session-analytics, authorizer |
| opal-sessions-secrets | secretsmanager:Get | opal/auth/jwt-public-key | authorizer |
| SecretsManagerAccess | secretsmanager:Get | opal/* (broad wildcard) | Multiple |
| opal-cloudfront-invalidation | cloudfront:CreateInvalidation | distribution EVTSA9VEHNZVH | market generators |
| opal-bedrock-invoke | bedrock:InvokeModel | stability.stable-image-* | trending-image-generator |
| opal-infrastructure-monitor | CloudWatch, logs, lambda:List, ec2:Describe, ce:GetCost, ses:Send, events:List | * (broad) | infrastructure-monitor |
| lambda-invoke-finbert | lambda:Invoke | opal-news-ai-sentiment | finbert-batch-processor |
| EC2SnapshotPermissions | ec2:CreateImage/DescribeImages/CreateTags | EC2 instances/images/snapshots | daily-snapshot |

### Policy Categorization

| Category | Policies | Functions Needing Them |
|----------|----------|----------------------|
| **Data access (S3+DynamoDB)** | s3-read, dynamodb, secrets | All 7 market-overview + news + data-proxy |
| **Auth** | sessions-dynamodb, sessions-secrets | authorizer, session-analytics (2 functions) |
| **Ops/monitoring** | infrastructure-monitor, EC2Snapshot | infrastructure-monitor, daily-snapshot (2 functions) |
| **AI/ML** | bedrock-invoke, lambda-invoke-finbert | trending-image, finbert-batch (2 functions) |
| **CloudFront** | cloudfront-invalidation | market generators |
| **Logging** | logs | All functions |
| **Broad secrets** | SecretsManagerAccess | Unclear (overlaps with portal-secrets + sessions-secrets) |

---

## 3. Recommendation: Option B — shared-infra owns the role

### Why NOT Option A (portal-auth):
- portal-auth only uses 2 of 13 functions (authorizer + session-analytics)
- portal-auth deploys infrequently (last: v1.6.0 today, before that: v1.5.0 on 2026-03-16)
- An auth deploy that breaks the role would affect all 13 functions including market-overview and news

### Why NOT Option C (per-pipeline split):
- 12 inline policies would need to be duplicated/split across 4+ roles
- S3 access (8 buckets) is genuinely shared — most functions need the same buckets
- Additional IAM roles increase TF complexity for marginal security benefit
- The 3 NOT_IN_TF functions would need to be onboarded first

### Why Option B (shared-infra):
- **shared-infra already manages this role partially** — `EC2SnapshotPermissions` is attached via shared-infra/main.tf:318
- shared-infra is the natural home for cross-pipeline resources (S3 buckets, layers, shared roles)
- shared-infra deploys rarely and deliberately — low blast radius from accidental changes
- The role predates Terraform; shared-infra's pattern is "import legacy shared resources"
- If a pipeline needs a function-specific permission in the future, it adds an inline policy via `aws_iam_role_policy` referencing the role by ARN — no ownership conflict

### Caveat: market-overview is the heavyweight user
If the role were split in the future (Option C), market-overview would get the largest piece (7 functions). But for the import-only step, shared-infra is the right owner because it's the least-frequently-deployed pipeline and already has the precedent.

---

## 4. Migration Plan

### Pre-migration checks
1. `terraform state list` in shared-infra — confirm role is NOT already imported
2. `aws iam get-role --role-name opal-portal-lambda-role` — capture full role document
3. Snapshot all 12 inline policies (done above)

### Step 1: Import into shared-infra
```hcl
# shared-infra/iam.tf

resource "aws_iam_role" "portal_lambda" {
  name = "opal-portal-lambda-role"
  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Effect    = "Allow"
      Principal = { Service = "lambda.amazonaws.com" }
      Action    = "sts:AssumeRole"
    }]
  })
}
```

```bash
export MSYS_NO_PATHCONV=1
.tools/terraform.exe -chdir=infra/aws/terraform/shared-infra import aws_iam_role.portal_lambda opal-portal-lambda-role
```

### Step 2: Import all 12 inline policies
```hcl
# One aws_iam_role_policy per inline policy
resource "aws_iam_role_policy" "portal_s3_read" {
  name   = "opal-portal-s3-read"
  role   = aws_iam_role.portal_lambda.name
  policy = jsonencode({ ... })  # from captured policy document
}
# ... repeat for all 12
```

```bash
# Import each: terraform import aws_iam_role_policy.portal_s3_read opal-portal-lambda-role:opal-portal-s3-read
# ... repeat for all 12
```

### Step 3: Verify 0-diff
```bash
.tools/terraform.exe -chdir=infra/aws/terraform/shared-infra plan
# Must show "No changes"
```

### Step 4: Update other pipelines
- portal-auth/iam.tf: Change data source to reference shared-infra output or ARN directly (already does ARN)
- market-overview/main.tf: Already references by ARN — no change needed
- news-pipeline/variables.tf: Already has ARN default — no change needed

### Step 5: Remove portal-auth data source
```hcl
# portal-auth/iam.tf — REMOVE this block:
# data "aws_iam_role" "portal_lambda" {
#   name = "opal-portal-lambda-role"
# }
```

### Rollback
If 0-diff fails after import:
```bash
.tools/terraform.exe -chdir=infra/aws/terraform/shared-infra state rm aws_iam_role.portal_lambda
# ... state rm each aws_iam_role_policy
```
This removes TF tracking without affecting the actual AWS role.

---

## 5. Drift / Orphaned Permissions

| Policy | Issue |
|--------|-------|
| `SecretsManagerAccess` | Overlaps with `opal-portal-secrets` + `opal-sessions-secrets`. Grants `opal/*` wildcard which is broader than needed. Candidate for removal after confirming all secrets paths are covered by the specific policies. |
| `opal-portal-logs` | Scoped to us-east-2 only. Functions in us-east-1 get logs from the Lambda service role's default CloudWatch permissions. This policy may be vestigial. |
| `opal-portal-s3-read` | Named "s3-read" but grants Put+Delete too. Misleading name. |
| `EC2SnapshotPermissions` | Only used by `infrastructure-daily-snapshot` (NOT_IN_TF). Could be moved to a dedicated role when that function is onboarded. |
| `opal-bedrock-invoke` | Only used by trending-image-generator (NOT_IN_TF). Same. |

---

## Summary

**Recommendation:** Import `opal-portal-lambda-role` + all 12 inline policies into **shared-infra** pipeline.
**Rationale:** shared-infra already partially manages it, deploys rarely (low blast radius), and owns the shared-resource pattern.
**Effort:** ~2 hours (13 imports, HCL scaffolding, 0-diff verification).
**Risk:** Low — import is a read-only TF operation; rollback is `state rm`.
