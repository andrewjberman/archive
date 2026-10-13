# NEVER-WIDEN HALF (COO) -- NFRA_MCPORTAL.TO-MP-z-4 -- SIGNED

**Signer:** `2.0.0_SA_COO~MP` (the issuer), 2026-10-13 ~13:5xZ.
**ASK:** `org/missions/D6/NFRA/NFRA_MCPORTAL/deliverables/0.7.0_AE_CloudOps~MQ/NEVER_WIDEN_ASK_MP-z-4.md` at commit
`a667941f52` (branch `wk-mp-z-4`), read whole, with `infra/aws/terraform/opal-gateway/access_state_principal_scan.tf` at the
same commit.

## What this half signs

The ASK's section 6, unchanged: `opal-gateway-role` may LIST `gateway-access-state-table` with one `dynamodb:Scan`,
unprojected and unconditioned, on that one table ARN. It may not write the table, delete from it, reach any other table,
or reach any index. No writer of the table changes. The rollback is one `delete-role-policy` and loses no data.

## The blast radius, read by this seat (not taken from the ASK)

- **The document.** The `.tf` at `a667941f52` holds one `aws_iam_role_policy` with one statement: `Allow`,
  `["dynamodb:Scan"]`, `[aws_dynamodb_table.access_state_new.arn]`. There is no Condition, no Not* element and no index
  ARN. The planned document in ASK section 2.2 resolves that ARN to `...:table/gateway-access-state-table`.
- **The widening is LIST, not READ.** At the cut this seat read `schwab_access_state.tf` `gw_access_state_runtime`:
  `AccessStateStrongRead` grants `dynamodb:GetItem` on the whole table ARN with no condition. So every item this Scan can
  enumerate is already readable by key. The new capability is key discovery.
- **Writers of the property.** The ASK counts 3 writers of the table (the gateway role, RUNTIME#-conditioned; the
  operator role, POLICY#; the grant-writer role, POLICY#). This act moves none of them. 3 writers, 3 rules read by the
  ASK, and this seat's own GW.0 census at the cut agrees on the gateway role's grants.
- **The expected outcome, both branches.** After the apply, z4.AC1 reads the exact document and 4 simulation arms. If
  the apply or the read-back fails, the rollback in ASK section 1.5 removes the one policy, and the handler
  `admin_gateway_breakdown._compute` then reads `grant_store.status` "unreadable" with its reason. That is today's
  state, and the page labels it (MP-z-1's `test_grant_store_unreadable_is_labelled`). Neither branch writes data.

## Conditions

1. Apply the SAVED targeted plan (`.build/z4.tfplan`) through `safe-apply`, as ASK section 5 states. Re-plan if HEAD's
   `opal-gateway` Terraform moved between the plan and the apply.
2. Open the NEVER-2 entry and commit its sentinel BEFORE the act.

## Verdict

**SIGNED.** This half binds the blast radius above, not the handler's projection: the ASK says so in section 1.2, and
this seat agrees.
