# OPAL_TAXSMA WS-4 + WS-R5 -- Gateway Scoped-IAM APPLY PLAN (ready-to-apply, for CTO + Andrew gate)

**Author:** 0.5.0_AE_OpalETL~A · 2026-07-21 · **archetype:** SCRIBE (plan-to-the-gate)
**Builds on:** DT's WS-4 design + CTO plan-gate PASS 215011Z (`org/tier2_senior/0.2.0_DT_PortfolioAnalytics/deliverables/TAXSMA_PT2_WS4_GATEWAY_IAM_PLAN_20260717.md`) + REGISTRY PRD D4 (WS-R5).
**Gate:** per-employee scoped-IAM is a SECURITY SURFACE Andrew gates (Andrew-direct 2026-07-21) + CTO plan-gate + CTO hard-withholds go-live until Rule-22a APPLIED+EXERCISED. **NOT applied.** This is the ready artifact.

## Artifacts (all committed, none applied) -- COND-1 SPLIT per CTO 005002Z
- **TF:** `infra/aws/terraform/m365-mcp-gateway/taxsma_gateway_iam.tf` -- TWO scoped roles (CTO SPLIT):
  `opal-mcp-emp-alyssa-read` (WS-4 gold read ONLY, write-free) + `opal-mcp-emp-alyssa-onboard` (WS-R5
  invoke-producer + roster-RW). Both trust = gateway role + ExternalId `opal-mcp-taxsma-pt2`; the gateway
  role gains ONE grant (assume `opal-mcp-emp-*` + ExternalId, covers both). Gateway holds ZERO opal-data-assets S3.
- **Rule-22a evidence script:** `infra/aws/terraform/m365-mcp-gateway/taxsma_rule22a_verify.sh` -- isolated
  simulates for BOTH roles (read: gold-positive + silver/bronze/write/invoke never-widen; onboard: invoke/roster
  positives + widen negatives) + the assume-role exercise. Usage: `taxsma_rule22a_verify.sh <read-arn> <onboard-arn> [<gw-arn>]`.
- **Entitlements artifact** (deploy like `ENTITLEMENTS_PATH`, hot-reloaded; FAIL-CLOSED -- no mapping => deny).
  **Under the SPLIT the map is email(+operation)->ARN, not email->ARN** (WS-6 gateway selects the role by
  operation: a read tool -> read-role, an onboard tool -> onboard-role):
  ```json
  { "alyssa@opalinvest.com": {
      "read":    "arn:aws:iam::313476888478:role/opal-mcp-emp-alyssa-read",
      "onboard": "arn:aws:iam::313476888478:role/opal-mcp-emp-alyssa-onboard" } }
  ```

## What each role grants (SPLIT -- CTO 005002Z)
| Role | Grant | WS | Scope | Never-widen |
|---|---|---|---|---|
| `-read` | `s3:GetObject` gold `dim_taxsma_report/*` | WS-4 | anonymized serve prefix ONLY | no silver/bronze/write, no invoke |
| `-read` | `s3:ListBucket` (conditioned `s3:prefix` gold) | WS-4 | list ONLY the gold prefix | other prefixes implicitDeny |
| `-onboard` | `lambda:InvokeFunction` producer ARN | WS-R5 | ONLY `opal-assets-bd49f-reporting-pull` | no other lambda, no gold read |
| `-onboard` | `s3:GetObject`+`PutObject` roster key | WS-R5 | ONLY `_ops/taxsma_roster.json` | no other key, no other prefix, no gold |

## CTO's 4 binding conditions -- status
- **COND-1 (opal-mcp-emp-* namespace invariant):** SATISFIED LITERALLY via the SPLIT (CTO decision 005002Z). Two roles: `-read` is WRITE-FREE (WS-4 gold read only); `-onboard` holds the single scoped write (WS-R5 roster-RW + producer-invoke). Both CTO-gated TF, single-purpose, trust ONLY the gateway role + ExternalId. **WS-6 implication surfaced:** the gateway must select the role BY OPERATION (email+operation->ARN entitlements, not email->ARN). CTO finalizes at apply time w/ Andrew. Gate-candidate (a lint denying any opal-mcp-emp-* role that widens) flagged.
- **COND-2 (re-id mapping NOT under her gold prefix):** OPEN -- a WS-3 layout gate (DS). The scoped read reaches everything under `gold/dim_taxsma_report/*`; if the re-id / 03_mappings key lives there, anonymization is defeated. **MUST confirm the re-id map is elsewhere before go-live.**
- **COND-3 (WS-3 anonymization actually holds -- verified not asserted):** OPEN -- the IAM is PII-free only if gold `dim_taxsma_report` is genuinely anonymized. CVO verified the Chiles gold PII-free 2026-07-18; re-confirm for the full account set before go-live.
- **COND-4 (Rule-22a APPLIED+EXERCISED; CTO hard-withholds go-live):** the verify script delivers exactly the evidence -- (a) positive GetObject gold (isolated), (b) never-widen silver/bronze (separate), (c) ListBucket WITH `--context-entries` (the conditioned-statement false-deny catch), + WS-R5 invoke/roster positives & negatives, + the assume-role EXERCISE. DESIRED-only = INFERRED.

## Apply sequence (HELD -- CTO + Andrew gate)
1. WS-3 gold prefix exists -- DONE (Chiles `account=0027265115/date=2026-07-17`).
2. CTO reads this plan + the TF (his plan-gate) + Andrew's security sign-off on the per-employee IAM.
3. AE runs `terraform plan` (m365-mcp-gateway) -> pure-add diff -> CTO reviews -> `safe-apply`.
4. AE runs `taxsma_rule22a_verify.sh <read-arn> <onboard-arn> <gateway-role-arn>` -> evidence to CTO (APPLIED+EXERCISED).
5. CONFIRM COND-2 + COND-3 (WS-3 layout + anonymization) -> CTO go-live confirm.
6. WS-6 wires Alyssa's `/tax-pt2` + `/tax-newacc` read/onboard paths through the gateway assume-role (separate).

## Notes
- WS-R5's onboarding grants make `/tax-newacc` Alyssa-operable (Phase B); until applied, onboarding is workspace-agent-run (Phase A, built).
- The gateway app's AWS-read path (resolve verified-email -> ARN -> `sts:assume_role` -> read) is WS-6 (design in DT sec 2), NOT this IAM apply.
- Deploy the IAM via Terraform on m365-mcp-gateway infra (AE-executed); `aws lambda update-function-code` etc. are irrelevant here (IAM only).
