# NEVER-WIDEN HALF (COO) -- OG-ap-12: grant `sqs:ChangeMessageVisibility` on the silver DLQ, then re-deploy the schwab per-family drain

Signer: 2.0.0_SA_COO~O, 2026-10-12 ~12:5xZ. Cause: row NFRA_OPLGTW-Z-S97. OG-ap-11 AC2 FAILED on the real 12:15Z
sweep and was rolled back under its A2 (@aebec97ee4).

## The act

1. **The policy edit.** `infra/aws/terraform/opal-assets/silver.tf`, resource `aws_iam_policy.silver_dlq_access` (live
   name `opal-assets-silver-dlq-access`): add ONE action, `sqs:ChangeMessageVisibility`, to the statement
   `SilverDlqSendAndDrain`. The Resource stays `aws_sqs_queue.silver_dlq.arn`, the one queue.
2. **The re-deploy.** Re-deploy the schwab converter at the OG-ap-11 build (its `ap11_build.json` `code_sha256`), by
   the OG-ap-11 path: `safe-apply -target`, ledger, read-back.
3. **The grade.** Grade on the NEXT scheduled 12:15Z schwab sweep, with the same two synthetics and the same `ap11.AC2`.

## Blast radius

- **One policy, 1 to 7 roles.** The policy is attached to 7 live roles (`list-entities-for-policy` read 2026-10-12
  12:5xZ): etf, smartx, orion, schwab, bd49finsurance, eclipse, blackdiamond. All 7 gain the action on the ONE queue.
- **What the action can do.** It acts only on a message the caller already RECEIVED, through its receipt handle.
  Every one of these roles already holds `sqs:DeleteMessage` on the same queue, so it is strictly weaker than a grant
  they hold.
- **The other 6 roles.** Their deployed code never calls the action (only `schwab_runtime.py` `drain_dlq` does, at
  HEAD), so their behaviour does not move.
- **What does not move.** No other queue, no S3, no Lambda other than schwab.

## The plan bar

- The policy edit is a targeted plan, read at rc=0: `1 to change` (the policy document), 0 add, 0 destroy. Any other
  row is a STOP.
- The schwab leg reads 1 to change: the code fields plus `OPAL_BUILD_COMMIT`.

## Rollback, per key

- **Policy:** revert the one action by the same targeted apply.
- **Schwab:** redeploy `prior_code_sha256` and the prior pin (exactly as OG-ap-11's A2 rollback).

## Window

Apply outside [09:15,11:35)Z, [12:00,12:50)Z and [21:15,23:35)Z.

## Owed by the issuer at the cut

- `comp-iam` run on the ACTION, not declared.
- A `simulate-principal-policy` on schwab-role for `sqs:ChangeMessageVisibility` on the DLQ ARN: DENY before, ALLOW
  after.
