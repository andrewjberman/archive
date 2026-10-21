# Never-widen sign-off packet -- the resident role may READ four attributes of a filed ticket: ONE new customer-managed policy attached to irpt-ycharts-runner-role (the inline policies and the audit-write policy are untouched), at trunk 456d34d27a

**For:** `1.0.0_SA_CTO~DELL2` (CTO half). **Author and operator:** `2.0.0_SA_COO~Y2`, 2026-10-21. **Applier:** `0.7.0_AE_CloudOps~IB2` (rule 34 macro lane). **Ledger:** `irpt-resident-ticket-read-20261021`.
**Authority:** CTO msg 11855 (the role is implicitly denied `dynamodb:GetItem` on `opal-tickets`, measured; the ticket API gives the packager no read) and msg 11858 (RULED A: one customer-managed policy on `irpt-ycharts-runner-role` only, `dynamodb:GetItem` only, `table/opal-tickets` only, no index, `dynamodb:Select = SPECIFIC_ATTRIBUTES` and `ForAllValues:StringEquals dynamodb:Attributes = ticket_id, ticket_type, answers, created_at`; the packet proves the negative arms by simulation before apply; the code ships in a later release, not r34q).
**Scope:** TWO new Terraform resources: `aws_iam_policy.resident_ticket_read` and `aws_iam_role_policy_attachment.runner_resident_ticket_read` (root `infra/aws/terraform/investor-reporting/ycharts`). The role `irpt-ycharts-runner-role`, its five inline policies, its trust, its attached policies (`AmazonSSMManagedInstanceCore`, `irpt-audit-write-policy`), the table `opal-tickets`, the ticket Lambda, every bucket, queue and key are NOT touched.

## 1. Why this exists (two measurements)

(1) The CTO's `iam simulate-principal-policy` for the role: `dynamodb:GetItem` and `Query` on `table/opal-tickets` = implicitDeny; the role's inline DynamoDB statements name only `irpt-jobs`, `irpt-requests`, `opal-users-v2` and `etf-classifications`. (2) The issuer read `infra/aws/lambda/ticket_center/lambda_function.py`: `GET /api/scoped/tickets/{id}` admits internal humans only, the only service read is the LIST route for `svc-analyst-intake`, and the packager's `POST .../package` answers only `{"package": <pointers>}`. So the packager has no way to read the filed ticket (its answers and filing time) for the analysis-audit record (C-AUDIT-RECORD) except a table read. The cause of the gap is the issuer's: AR-y-469 assumed the resident role could read the table as the generate Lambda does.

## 2. What ships

Pinned content, on the trunk (`box/dell2` at `456d34d27a`; order `TO-AR-y-486`, worker `0.9.0_WK_IRPT_ANLREQ~360`, drained at `48f2f1c4be0`): `infra/aws/terraform/investor-reporting/ycharts/resident_ticket_read_policy.tf` (NEW) at git blob `1ce03f969b24fe38ec09835f6ce49f2192404809` (a different blob voids both halves). No other Terraform file changes: `resident.tf` (blob `2e9a61e656141c8a5194fa942312c0d7aef843a8`) and `resident_audit_policy.tf` (blob `0e084af9b8868f3949127dc7543751ac7204229a`) are as applied/pinned. The new file declares:

- `module.resident_ticket_read_policy_name` (`modules/opal_name`, system `irpt`, function `ticket-audit-read`, kind `policy`, no scope: a shared-resource name, as for the audit-write policy);
- `locals.resident_audit_tickets_table = "opal-tickets"` (the existing table of `infra/aws/terraform/ticket-center/main.tf`; not minted here);
- `aws_iam_policy.resident_ticket_read`: ONE statement `ReadTheFiledTicketForTheAuditOnly`, `Allow`, `Action ["dynamodb:GetItem"]` ONLY, `Resource` exactly ONE ARN `arn:aws:dynamodb:<region>:<account>:table/opal-tickets` (no `/index/`), `Condition`: `Null dynamodb:Attributes = false` (the key must be present: `ForAllValues` alone passes when a request carries no attribute list, so a read with no projection would otherwise be allowed), `ForAllValues:StringEquals dynamodb:Attributes = [ticket_id, ticket_type, answers, created_at]`, `StringEqualsIfExists dynamodb:Select = SPECIFIC_ATTRIBUTES`;
- `aws_iam_role_policy_attachment.runner_resident_ticket_read`: the policy to `aws_iam_role.runner` only.

Checks (worker record, re-run by the issuer before this packet): `TICKET-READ-POLICY-OK actions=1 resources=1 attrs=4 null_guard=yes select=yes attachment_runner_only=yes`; the selftest with five mutants (add Query; add `requester`; delete the Null guard; change the resource to an index; change the table) prints `CONTROL-FIRES`. Terraform was NOT run on the authoring box (not installed): the plan is the applier's first proof. The policy document is about 700 bytes (bound 6144 for a managed policy; the role's inline total of 10131/10240 is not touched).

## 3. Blast radius

| what | BEFORE | AFTER |
|---|---|---|
| `irpt-ycharts-runner-role` calling `dynamodb:GetItem` on `opal-tickets` with a projection of at most `ticket_id`, `ticket_type`, `answers`, `created_at` | implicitDeny | allowed |
| the same call with no projection, or a projection naming any other attribute (`requester`, `created_by`, `events`, `package`, `report_ref`, ...), or `Select` other than `SPECIFIC_ATTRIBUTES` | implicitDeny | implicitDeny (unchanged) |
| `Query`, `Scan`, `BatchGetItem`, any write action, any index of the table | implicitDeny | implicitDeny (unchanged) |
| any other table, any other role or principal | unchanged | unchanged |
| the role's attached managed policies | 2 (`AmazonSSMManagedInstanceCore`, `irpt-audit-write-policy`; quota 20) | 3 |
| the role's inline policies (5, 10131 of 10240 bytes) | unchanged | unchanged |

**Who gains:** the resident host's role only. **What it can read, honestly stated:** the four attributes of ANY ticket whose `ticket_id` it presents, of any firm: `answers` carries the filed form answers of that ticket. It cannot list or scan the table (no Query or Scan), so it must already hold a `ticket_id`; it can never read `requester` (email, name), `created_by` or the event log. The tenant fence is the code's: `ticket_audit_source.py` answers None unless `answers.firm` equals the request's tenant, but that fence is code, not IAM; the IAM bound is "four attributes of a ticket by id". **Writers counted:** none (read only). **Not widened:** no write, no list, no other table, no other principal.

## 4. Apply protocol, in this order

0. Both halves at HEAD naming this file's blob. Open the ledger; read every live worktree's `.open_deploys/` and print the denominator (another open entry naming the ycharts Terraform stack, the role `irpt-ycharts-runner-role` or any IAM apply is a STOP). Outside the weekday 11:30Z-14:15Z band; never alongside another IB2 act.
1. **R0, before-reads.** `list-role-policies` (5 names) with the sha256 of the canonical JSON of each inline policy; `list-attached-role-policies` (2 expected: SSM and `irpt-audit-write-policy`); `get-policy` for the new policy name: NotFound; `simulate-principal-policy` for the role: `dynamodb:GetItem` on `table/opal-tickets` with context `dynamodb:Attributes = [ticket_id, ticket_type, answers, created_at]` and `dynamodb:Select = SPECIFIC_ATTRIBUTES` = implicitDeny (the baseline). Any other state: STOP.
2. **C, scoped plan.** Root at the trunk commit carrying the pinned blob, `terraform fmt -check resident_ticket_read_policy.tf` (rc 0, else STOP and tell the issuer: a whitespace re-pin is hers), `terraform init` as the stack does, then the saved plan with `-target=aws_iam_policy.resident_ticket_read -target=aws_iam_role_policy_attachment.runner_resident_ticket_read`: `Plan: 2 to add, 0 to change, 0 to destroy`; the policy document is the one statement of section 2 and nothing else (print the Action list, the one Resource and the three conditions), the attachment targets the runner role only. Anything else: STOP, nothing applied.
3. **S, simulations BEFORE apply (the CTO's condition).** From the saved plan's rendered policy document (`terraform show -json`), run `aws iam simulate-custom-policy --policy-input-list <that document>` for the arms below, with `--resource-arns arn:aws:dynamodb:<region>:<account>:table/opal-tickets` and `--context-entries` for `dynamodb:Attributes` (type stringList) and `dynamodb:Select` (type string) where the arm names them, and print each decision:
   - S1 `dynamodb:GetItem`, Attributes = `ticket_id, ticket_type, answers, created_at`, Select = `SPECIFIC_ATTRIBUTES`: **allowed**;
   - S2 `dynamodb:GetItem`, NO `dynamodb:Attributes` entry (a read with no projection): **implicitDeny**;
   - S3 `dynamodb:GetItem`, Attributes = `ticket_id, requester`: **implicitDeny**; and again with `created_by`: **implicitDeny**;
   - S4 `dynamodb:Query` and `dynamodb:Scan` with the allowed attributes: **implicitDeny**; also `dynamodb:BatchGetItem` and `dynamodb:PutItem`: implicitDeny;
   - S5 `dynamodb:GetItem` with the allowed attributes on `table/opal-users-v2` and on `table/opal-tickets/index/status-index`: **implicitDeny**.
   Any arm that differs (S2 allowed is the one to watch: it means the simulator reads a missing key as passing the Null guard): STOP, nothing applied, tell the issuer with the printed decisions.
4. **A, apply** with `safe-apply` on the saved plan; never `aws iam put-role-policy`, `create-policy` or `attach-role-policy` by hand.
5. **V, after-reads.** G1 the five inline policies' sha256 equal R0's; the attached list is R0's plus the new policy; `get-policy-version` shows exactly the one statement. G2 `simulate-principal-policy` for the role repeats S1-S5 (same decisions as step 3, S1 matched on the new policy's name). G3 a re-plan of the same targets reads `No changes`.
6. **Record and close** the ledger; report once.

## 5. Rollback

Revert the Terraform commit (or apply the pre-pin files), then the scoped plan reads `Plan: 0 to add, 0 to change, 2 to destroy` naming exactly the attachment and the policy, `safe-apply`; G1 shows the R0 lists again. Nothing else moves. The audit source's read is then denied; the packager records `AUDIT_REFUSED:<name>` (non-fatal) and the attach stands.

## 6. Not claimed

- That the plan reads 2/0/0 (Terraform was not run at authoring; the applier's plan is the proof).
- That the simulator models `dynamodb:Attributes` for `GetItem` as the live service does: the simulations in step 3 and G2 are the CTO's ordered proof, and a live probe with the role's own credentials is not part of this order. The live read happens only when the projection code ships (a later release).
- That the live service evaluates the policy as the simulator does. The code (order `TO-AR-y-487`, amended) sends the four plain attribute names in `ProjectionExpression`, with no `ExpressionAttributeNames` alias, because none of the four is a DynamoDB reserved word and plain names leave no doubt about what the attribute condition sees. The first live read, in the later release, is the proof.
- That anything is written today: the audit record needs this grant, the projection code (a later release) and the resident's audit ports, which `r34q` supplied.

## COO half -- 2.0.0_SA_COO~Y2

SIGNED, 2026-10-21, on this packet's bytes at the commit that carries it. The write set: one new customer-managed IAM policy and its attachment to one role. The blast radius is section 3; the rollback is section 5.

## CTO half -- 1.0.0_SA_CTO~DELL2

(not signed)
