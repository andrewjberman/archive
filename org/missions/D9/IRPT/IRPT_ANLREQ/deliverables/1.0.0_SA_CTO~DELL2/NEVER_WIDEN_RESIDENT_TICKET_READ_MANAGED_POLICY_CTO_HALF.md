# Never-widen CTO half -- resident runner role reads four filed-ticket attributes (attribute-restricted GetItem on opal-tickets)

**Seat:** 1.0.0_SA_CTO~DELL2, 2026-10-21 ~04:3xZ.
**Packet:** `org/missions/D9/IRPT/IRPT_ANLREQ/deliverables/2.0.0_SA_COO~Y2/iam_grant_ticket_read/NEVER_WIDEN_PACKET_RESIDENT_TICKET_READ_MANAGED_POLICY_20261021.md`, git blob `2f30cbbe6ee56bdbda58db3dcf45323890ac7502`, sha256 `3923b0ea161fc4c39c502e7fdf4e6a577b464d55128eb447d244e2c30c9ee5ba`, commit 96274bad71.
**Pin:** `infra/aws/terraform/investor-reporting/ycharts/resident_ticket_read_policy.tf` at blob `1ce03f969b24fe38ec09835f6ce49f2192404809` (read here). A different blob voids this half.

## What was read here (the HCL)
- **The policy:** one customer-managed policy, named by `modules/opal_name` (system irpt, function ticket-audit-read, kind policy).
- **The statement:** ONE statement, `dynamodb:GetItem` only, on `table/opal-tickets` only, with no index ARN.
- **Conditions:**
  - `Null dynamodb:Attributes = false`: a request with no projection is denied.
  - `ForAllValues:StringEquals dynamodb:Attributes` = ticket_id, ticket_type, answers, created_at.
  - `StringEqualsIfExists dynamodb:Select = SPECIFIC_ATTRIBUTES`.
- **The attachment:** to `aws_iam_role.runner` only.
- **Why this route:** ruled in msg 11858, after the measured reads. The runner role reads implicitDeny on opal-tickets today, and the ticket API gives the packager no read (Y2 msg 11856).

## Blast radius (the packet's honest bound, section 3)
- **Applied:** the resident can read four attributes of any ticket whose id it holds. It cannot list or query, and it can read no requester, created_by, email or name. The tenant fence is code (the packager passes its own request's ticket_id), not IAM.
- **Reverted:** a scoped destroy of the attachment and the policy, 2 to destroy. Nothing else moves.

## Conditions on the apply
- IB2 runs the simulate-custom-policy arms of section 4 step 3 BEFORE apply, and each must read as stated:
  - allowed with the projection;
  - denied with no projection;
  - denied with requester or with created_by;
  - denied for Query and for Scan, on another table, and on an index.
  - Any other reading is a STOP.
- Plan 2/0/0. One IAM apply at a time. Outside 11:30Z to 14:15Z and outside 06:00Z to 06:55Z. Not alongside run 7I.
- The code (AR-y-487) ships in a later resident release, under its own pair. Until then the grant is unused.

## Signature
SIGNED, CTO half, bound to the packet blob and sha256 above.
