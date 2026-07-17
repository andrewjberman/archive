# WS-4 Gateway Scoped-IAM Plan (OPAL_TAXSMA_PT2) -- for CTO plan-gate

**Author:** 0.2.0_DT_PortfolioAnalytics · 2026-07-17 · **archetype:** SCRIBE (plan)
**Gate:** CTO HARD plan-gate (net-new external read into the monolith) + WS-3 gold prefix must exist
(the Rule-22a verify target). **APPLY HOLDS** for both. m365-mcp-gateway is AE infra -> DT designs, AE
applies, CTO gates. This is the plan diff for CTO to read.

## Model (Andrew-direct): per-employee scoped IAM + email->ARN + gateway assume-role
One least-privilege role per Opal employee; the gateway's AWS-surface entitlements file maps
`email -> scoped-role-ARN`; on a verified-email data-read the gateway STS-assumes that role and reads S3
under it -- the role's policy IS the boundary. Alyssa's role reaches EXACTLY the gold prefix, nothing else.

## 1. Alyssa's scoped role (NEW) -- `opal-mcp-emp-alyssa-read`
**Permissions policy** (single-prefix, PII-free-by-construction -- gold is anonymized):
```json
{ "Version": "2012-10-17", "Statement": [
  { "Sid": "ReadTaxsmaGoldOnly", "Effect": "Allow", "Action": ["s3:GetObject"],
    "Resource": ["arn:aws:s3:::opal-data-assets/blackdiamond/49f/gold/dim_taxsma_report/*"] },
  { "Sid": "ListTaxsmaGoldPrefixOnly", "Effect": "Allow", "Action": ["s3:ListBucket"],
    "Resource": ["arn:aws:s3:::opal-data-assets"],
    "Condition": { "StringLike": { "s3:prefix": ["blackdiamond/49f/gold/dim_taxsma_report/*"] } } } ] }
```
**Trust policy** (only the gateway role may assume it; ExternalId binds the specific gateway):
```json
{ "Version": "2012-10-17", "Statement": [
  { "Effect": "Allow", "Principal": { "AWS": "arn:aws:iam::313476888478:role/m365-mcp-gateway-role" },
    "Action": "sts:AssumeRole",
    "Condition": { "StringEquals": { "sts:ExternalId": "opal-mcp-taxsma-pt2" } } } ] }
```
NEVER-WIDEN: no bronze/silver, no other bucket, no write, no delete. The gold prefix is the entire reach.

## 2. Gateway side (m365-mcp-gateway-role) -- minimal additions
- Add ONE inline statement: `sts:AssumeRole` on the per-employee role ARNs ONLY (start:
  `arn:aws:iam::313476888478:role/opal-mcp-emp-*`), with the ExternalId condition. The gateway itself
  still holds ZERO opal-data-assets S3 -- it can only reach data by assuming an employee role.
- **AWS-surface entitlements file** (`aws_entitlements.json`, hot-reloaded like the existing
  `ENTITLEMENTS_PATH`): `{ "alyssa@opalinvest.com": "arn:aws:iam::313476888478:role/opal-mcp-emp-alyssa-read" }`.
  FAIL-CLOSED: no mapping for a verified email -> deny (no default role, ever).
- **New read path in the gateway** (design, not applied): a data-read tool resolves the caller's
  signature-verified email -> ARN (from the file), `sts:assume_role(RoleArn, ExternalId)`, reads the gold
  key with the temp creds, returns the record. Extends `app/entitlements.py`'s pattern (the write-class
  gate) with the AWS-surface dimension; the assume-role is the boundary, so the gateway never holds a
  standing broad grant. Alyssa's `/tax-pt2 {account}` skill drives this (WS-6).

## 3. Rule-22a live verify (CTO gate evidence -- runs BEFORE apply, gated on WS-3 gold prefix existing)
Two SEPARATE `simulate-principal-policy` calls (2+ ARNs in one call poisons held ones to implicitDeny --
a batched control is corrupted by its own presence):
```
# POSITIVE (ONE --resource-arns):
aws iam simulate-principal-policy --policy-source-arn <opal-mcp-emp-alyssa-read ARN> \
  --action-names s3:GetObject \
  --resource-arns arn:aws:s3:::opal-data-assets/blackdiamond/49f/gold/dim_taxsma_report/<a real key>
  -> EXPECT: allowed
# NEVER-WIDEN (SEPARATE invocation, a NON-gold key):
aws iam simulate-principal-policy --policy-source-arn <opal-mcp-emp-alyssa-read ARN> \
  --action-names s3:GetObject \
  --resource-arns arn:aws:s3:::opal-data-assets/blackdiamond/49f/silver/fact_taxsma_report/<a key>
  -> EXPECT: implicitDeny
```
Then EXERCISE end-to-end (behavior, not config): the gateway assumes Alyssa's role and reads a gold key
(succeeds) + a silver/bronze key (AccessDenied). comp-iam is NECESSARY-NOT-SUFFICIENT (models action, not
(action,resource)) -- the live simulate on the exact key + the assume-role exercise are the truth.

## 4. Apply sequence (all HELD)
1. WS-3 lands the gold `dim_taxsma_report` prefix (verify target). 2. CTO reads THIS plan (his gate).
3. AE applies the two roles + the gateway inline stmt + the entitlements file (Terraform; the IAM apply is
AE-executed on m365-mcp-gateway infra). 4. Rule-22a verify (both controls SEPARATE + the exercise) ->
evidence to CTO. 5. WS-6 wires Alyssa's skill. Nothing applies before CTO's plan-gate PASS.
