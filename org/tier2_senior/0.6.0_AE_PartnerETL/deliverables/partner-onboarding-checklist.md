# Partner Onboarding Checklist — BD Pipeline

**Maintainer:** 0.6.0_AE_PartnerETL
**Created:** 2026-03-10
**Source:** ADVI_APISCP.001 audit findings + thread ADVI_APISCP-001 CloudFront routing analysis

---

## Overview

Each new partner firm gets its own isolated S3 bucket (`opal-data-{firmId}`). The
Lambda@Edge router constructs the origin bucket name from the `firmId` in the request
context at CloudFront time. No Lambda code changes are required to onboard a new firm —
only infrastructure and DynamoDB provisioning.

**Bucket separation rule:** Partner data NEVER goes to `opal-data-portal-v2`. That bucket
is reserved for static portal assets only.

---

## Prerequisites

Before starting, confirm with 0.7.0_AE_CloudOps:
- [ ] DT has completed the preflight discovery thread (ADVI_APISCP-001 or equivalent)
      to document the exact CloudFront OAC/OAI policy template for new buckets
- [ ] The Lambda@Edge router has been confirmed to accept the new `firmId` value
      (check `infra/aws/lambda-edge/` for any allowlist or routing table)

---

## Step 1: Create Partner S3 Bucket

**Who:** 0.6.0_AE_PartnerETL or 0.7.0_AE_CloudOps
**Terraform:** Add to `infra/aws/terraform/shared-infra/main.tf` OR create a
`infra/aws/terraform/bd-pipeline/partner-buckets.tf` module.

```hcl
resource "aws_s3_bucket" "partner_data" {
  bucket = "opal-data-${var.firm_id}"
}

resource "aws_s3_bucket_versioning" "partner_data" {
  bucket = aws_s3_bucket.partner_data.id
  versioning_configuration {
    status = "Enabled"
  }
}

resource "aws_s3_bucket_server_side_encryption_configuration" "partner_data" {
  bucket = aws_s3_bucket.partner_data.id
  rule {
    apply_server_side_encryption_by_default {
      sse_algorithm = "AES256"
    }
  }
}
```

Acceptance criteria:
- [ ] Bucket name: `opal-data-{firmId}` (e.g., `opal-data-acme-advisors`)
- [ ] Versioning: Enabled
- [ ] Server-side encryption: AES256 minimum
- [ ] Block all public access: ON

---

## Step 2: Attach CloudFront Bucket Policy

**Who:** 0.7.0_AE_CloudOps (owns CloudFront + IAM)
**REQUIRED:** Without this step, CloudFront cannot serve data from the new bucket.

S3 access is per-bucket — there is NO wildcard origin access policy covering all
`opal-data-*` buckets. Each new bucket requires its own explicit CloudFront access policy.

**Thread ADVI_APISCP-001 finding:** The exact principal format (OAC vs OAI) and the
canonical policy template must be confirmed by DT during preflight discovery. The DT will
document the policy template in their preflight thread before this step is executed.

**Expected form (placeholder — use DT-verified template):**

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "AllowCloudFrontRead",
      "Effect": "Allow",
      "Principal": {
        "Service": "cloudfront.amazonaws.com"
      },
      "Action": "s3:GetObject",
      "Resource": "arn:aws:s3:::opal-data-{firmId}/*",
      "Condition": {
        "StringEquals": {
          "AWS:SourceArn": "arn:aws:cloudfront::{accountId}:distribution/{distributionId}"
        }
      }
    }
  ]
}
```

Acceptance criteria:
- [ ] CloudFront can perform `s3:GetObject` on `opal-data-{firmId}/*`
- [ ] Policy uses the DT-confirmed principal (OAC or OAI)
- [ ] No public read access granted
- [ ] 0-diff terraform plan confirmed after apply

---

## Step 3: Create FIRM#{firmId} DynamoDB Record

**Who:** 0.6.0_AE_PartnerETL or 0.7.0_AE_CloudOps
**Table:** `opal-users-v2` (DynamoDB)

Add a firm-level record that the Lambda@Edge router uses to resolve the partner's S3 bucket:

```json
{
  "PK": "FIRM#acme-advisors",
  "SK": "PROFILE",
  "firmId": "acme-advisors",
  "s3Bucket": "opal-data-acme-advisors",
  "displayName": "Acme Advisors",
  "createdAt": "2026-MM-DD",
  "active": true
}
```

Write via AWS CLI (after confirming the exact schema with 0.4.0_DE_ClientPlatform):

```bash
aws dynamodb put-item \
  --table-name opal-users-v2 \
  --item '{
    "PK": {"S": "FIRM#acme-advisors"},
    "SK": {"S": "PROFILE"},
    "firmId": {"S": "acme-advisors"},
    "s3Bucket": {"S": "opal-data-acme-advisors"},
    "displayName": {"S": "Acme Advisors"},
    "active": {"BOOL": true}
  }'
```

Acceptance criteria:
- [ ] `PK=FIRM#{firmId}` record exists in `opal-users-v2`
- [ ] `s3Bucket` field matches the bucket created in Step 1 exactly
- [ ] Router can resolve `firmId` -> `s3Bucket` (verify with a test GET)

---

## Step 4: Write Gold Output to s3://opal-data-{firmId}/gold/

**Who:** 0.6.0_AE_PartnerETL (pipeline configuration)

For the 49financial pipeline, the publisher Lambdas use:
```python
OUTPUT_BUCKET = os.environ.get('OUTPUT_BUCKET', 'opal-data-bd')
```

For a new partner, deploy a parallel publisher Lambda (or extend via environment variable)
with `OUTPUT_BUCKET=opal-data-{firmId}`. The gold/ prefix convention is **fixed** — do not
change the prefix per partner.

All JSON files consumed by the portal must follow the convention:
```
s3://opal-data-{firmId}/gold/{filename}.json
```

Examples:
```
s3://opal-data-acme-advisors/gold/architect_leaderboard.json
s3://opal-data-acme-advisors/gold/timeseries_chart.json
s3://opal-data-acme-advisors/gold/summary/header_metrics.json
```

Acceptance criteria:
- [ ] All publisher output keys begin with `gold/`
- [ ] OUTPUT_BUCKET is `opal-data-{firmId}` (not `opal-data-portal-v2`, not `opal-data-bd`)
- [ ] Cache-Control header on all put_object calls: `public, max-age=300, s-maxage=3600`

---

## Step 5: Confirm No Writes to opal-data-portal-v2

**Who:** 0.6.0_AE_PartnerETL (pre-launch audit)

Before any gold pipeline run, verify the new pipeline code:

```bash
grep -r "opal-data-portal-v2" infra/aws/lambda/bd-pipeline/{publisher-name}/
# Expected: No matches
```

The path `opal-data-portal-v2/json/advisor-intelligence/` was deleted 2026-03-10.
It must never be recreated by any partner pipeline.

Acceptance criteria:
- [ ] Zero grep matches for `opal-data-portal-v2` in any active publisher Lambda source
- [ ] Zero writes to `opal-data-portal-v2` confirmed via CloudWatch Logs after first run

---

## Step 6: No Lambda@Edge Code Changes Required

The Lambda@Edge router constructs the origin bucket name from `firmId` dynamically.
No code changes to the router are needed — only the DynamoDB FIRM# record (Step 3)
and the CloudFront bucket policy (Step 2) gate access.

**Confirm with DT** before first run: the router's `firmId` extraction logic supports
the new firm's auth context (e.g., JWT claim format, Cognito user pool association).

Acceptance criteria:
- [ ] DT confirms router will resolve new firmId correctly
- [ ] A test GET from CloudFront to `gold/architect_leaderboard.json` returns 200

---

## Post-Onboarding Verification

After first gold pipeline run for the new partner:

1. Verify S3 objects exist at `s3://opal-data-{firmId}/gold/`
2. Verify Cache-Control headers on all objects
3. Verify CloudFront serves data correctly (200 response, correct payload)
4. Confirm NO objects written to `opal-data-portal-v2/`
5. Update `pipeline_inventory.xml` `<partner_scaling_model>` with the new firm entry
6. Add the new bucket to IAM policy in `iam.tf` (restrict to `opal-data-{firmId}`)

---

## IAM Note

The bd-pipeline Lambda role currently holds a stale `s3:PutObject` permission on
`opal-data-portal-v2/*` (known issue #10 in pipeline_inventory.xml). This permission
should be removed before onboarding the second partner to maintain least-privilege hygiene.
Coordinate with 0.7.0_AE_CloudOps for the IAM cleanup.
