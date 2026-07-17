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

## 5. CTO PLAN-GATE = PASS (215011Z) -- 4 BINDING CONDITIONS on apply/go-live
Design PASS ("assume-role-is-the-boundary + fail-closed + the 22a design are exactly right"). CTO
HARD-WITHHOLDS go-live (SEV1/IAM) until APPLIED+EXERCISED evidence. The four conditions bind:

- **COND-1 -- `opal-mcp-emp-*` is now a GATED SECURITY BOUNDARY.** The gateway's `sts:AssumeRole` wildcard
  on `opal-mcp-emp-*` makes its blast radius the UNION of every role in the namespace. Compensating
  namespace INVARIANT: every `opal-mcp-emp-*` role MUST be (a) created via CTO-gated TF, (b) single-employee
  least-privilege (scoped prefixes, no write/delete), (c) trust ONLY `m365-mcp-gateway-role` + ExternalId.
  **GATE CANDIDATE (flagged):** a lint denying any `opal-mcp-emp-*` role that grants beyond a scoped prefix
  or trusts beyond the gateway. (A careless future `opal-mcp-emp-admin` would be silently gateway-assumable.)
- **COND-2 -- the RE-ID MAPPING must live OUTSIDE her prefix.** Alyssa's PII-safety rests on single-prefix
  scope; if the anonymization re-identification mapping (CELL-2 / 03_mappings) is under
  `gold/dim_taxsma_report/*`, her scoped read reaches the re-id key and defeats anonymization. **CONFIRM
  the re-id mapping is NOT under her gold prefix** -> a binding constraint on WS-3's layout.
- **COND-3 -- PII-free-by-construction rests on WS-3 anonymization ACTUALLY holding (verified, not
  asserted).** The IAM points at the anonymized gold prefix, but the read is PII-free only if WS-3's
  `dim_taxsma_report` is genuinely anonymized (no re-identifiable fields). A WS-3 gate that must clear
  before WS-6 go-live.
- **COND-4 -- 22a APPLIED+EXERCISED; CTO hard-withholds go-live.** Sequence: WS-3 gold lands -> AE applies
  TF -> evidence -> CTO go-live confirm -> WS-6. Evidence MUST carry: (a) positive simulate GetObject on a
  real gold key = allowed (one --resource-arns, isolated); (b) never-widen simulate GetObject on a
  silver/bronze key = implicitDeny (SEPARATE call); **(c) a THIRD control -- simulate `s3:ListBucket` for
  the conditioned statement WITH `--context-entries s3:prefix=blackdiamond/49f/gold/dim_taxsma_report/...`
  (a conditioned statement with NO --context-entries returns implicitDeny BYTE-IDENTICAL to a real deny, so
  the ListBucket verify FALSE-DENIES without it -- CTO catch, folds into my 22a plan);** (d) the end-to-end
  EXERCISE: gateway assumes the role, reads a gold key (OK) + a silver/bronze key (AccessDenied). DESIRED-only
  or config-read = INFERRED, non-actionable.
