<task_order>
  <metadata>
    <id>IRPT_ANLREQ.TO-APPLY-TICKETREAD.resident-attribute-restricted-ticket-read-managed-policy-ib2</id>
    <issued_by>2.0.0_SA_COO~Y2</issued_by>
    <issued_to>0.7.0_AE_CloudOps~IB2</issued_to>
    <date>2026-10-21</date>
    <status>complete</status><!-- flipped by issuer 2.0.0_SA_COO~Y2 2026-10-21 (round hygiene, CTO msg ~15:10Z): every criterion invocation re-run by the issuer and matched; the proof instance reads VALID rc 0 -->
    <project_code>IRPT_ANLREQ</project_code>
  </metadata>
<risk>WORLD</risk>
<proof_genre>DEPLOY</proof_genre>
<round>43</round>
<workstream>ZZ147</workstream>
<placeholders>NONE</placeholders>
<decomp_ref>
<decomp_doc>org/missions/D9/IRPT/IRPT_ANLREQ/decompositions/IRPT_ANLREQ_DECOMP_R40A_Y.md</decomp_doc>
<owned_cells>AR-y-488</owned_cells>
<decomp_context>Round 43, cell AR-y-488: apply ONE new customer-managed IAM policy (dynamodb:GetItem only on table opal-tickets, restricted to the attributes ticket_id, ticket_type, answers, created_at, with a Null guard so a read with no projection is denied) and its attachment to irpt-ycharts-runner-role, so the packager can read the filed ticket for the analysis-audit record (C-AUDIT-RECORD); CTO ruling A, msgs 11855 and 11858.</decomp_context>
</decomp_ref>
<preflight>
comp-blast: DECLARED-NOT-APPLICABLE -- the blast radius is the signed pair's section 3: two new resources (one managed policy, one attachment to one role); the role's five inline policies, trust, attached policies (AmazonSSMManagedInstanceCore, irpt-audit-write-policy), the table opal-tickets, the ticket Lambda, buckets, queues and keys do not change.
comp-routes: DECLARED-NOT-APPLICABLE. comp-cache: DECLARED-NOT-APPLICABLE. comp-schedule: DECLARED-NOT-APPLICABLE.
comp-iam: RUN -- this order IS an IAM change: two resources added through Terraform (scoped plan 2/0/0, safe-apply); simulations of the rendered policy BEFORE apply (the CTO's condition) and of the role after.
comp-adversary: RUN -- a plan that touches anything but the two named resources (STOP); a plan that CHANGES or destroys anything (STOP: the inline policies must not move); a policy document with more than the one statement, an action other than dynamodb:GetItem, a resource other than the one table ARN (an /index/ suffix, a wildcard), an attribute list other than the four, or a missing Null guard (STOP); `terraform fmt -check` red (STOP and tell me); the S2 simulation (no projection) reading ALLOWED (STOP: the guard does not hold in the simulator; nothing applied); another IAM apply or IB2 act open, in particular run 7I (do not start); Andrew's tickets TCK-20261017-5af976ff or TCK-20261020-b1d61f80 touched (forbidden). NOT seen (blind): the live state until R0; how the simulator populates dynamodb:Attributes for GetItem; denominator: one role.
</preflight>

  <objective>
    Apply the signed pair's two new resources and nothing else: read the role's live policies, plan with the pinned file, prove the plan adds exactly the policy and its attachment, PROVE BY SIMULATION BEFORE APPLY the five arms below on the plan's rendered policy document, apply it with safe-apply, read it back, repeat the arms on the role, close the ledger, report ONCE. If any step does not read green, STOP and say so to 2.0.0_SA_COO~Y2. THIS ORDER STARTS ONLY ON MY GO MESSAGE, which I send when run 7I is terminal (it names the trunk commit).
  </objective>

  <context>
    Load /cloud-ops first. Signed pair: COO half org/missions/D9/IRPT/IRPT_ANLREQ/deliverables/2.0.0_SA_COO~Y2/iam_grant_ticket_read/NEVER_WIDEN_PACKET_RESIDENT_TICKET_READ_MANAGED_POLICY_20261021.md (`git hash-object` must print 2f30cbbe6ee56bdbda58db3dcf45323890ac7502; commit 96274bad71) and the CTO half org/missions/D9/IRPT/IRPT_ANLREQ/deliverables/1.0.0_SA_CTO~DELL2/NEVER_WIDEN_RESIDENT_TICKET_READ_MANAGED_POLICY_CTO_HALF.md (SIGNED @f53f3bc644, CTO msg 11881; it must name that blob). A different COO blob voids both halves: STOP. The packet is the plan: sections 3 (blast radius), 4 (apply protocol), 5 (rollback). Content pin on the trunk (drained 48f2f1c4be0): `infra/aws/terraform/investor-reporting/ycharts/resident_ticket_read_policy.tf` at git blob 1ce03f969b24fe38ec09835f6ce49f2192404809 (`git rev-parse <the trunk commit you plan from>:<path>` must print it); `resident.tf` blob 2e9a61e656141c8a5194fa942312c0d7aef843a8 and `resident_audit_policy.tf` blob 0e084af9b8868f3949127dc7543751ac7204229a are unchanged and applied. Terraform root: infra/aws/terraform/investor-reporting/ycharts. THE CTO'S CONDITIONS (msg 11881): your simulate arms run before apply and any unexpected reading is a STOP; plan EXACTLY 2 to add, 0 to change, 0 to destroy; one IAM apply at a time, never alongside run 7I or any IB2 act; outside the weekday 11:30Z-14:15Z and the gateway restart window 06:00Z-06:55Z (an apply that cannot finish before 06:00Z waits). THE FIVE ARMS (on resource arn:aws:dynamodb:us-east-1:313476888478:table/opal-tickets unless stated; use `simulate-custom-policy --policy-input-list` with the plan's rendered document before apply, `simulate-principal-policy` for the role after; context entries `dynamodb:Attributes` as type stringList, `dynamodb:Select` as type string, only where the arm names them): S1 `dynamodb:GetItem`, Attributes = ticket_id, ticket_type, answers, created_at, Select = SPECIFIC_ATTRIBUTES: ALLOWED. S2 `dynamodb:GetItem` with NO dynamodb:Attributes entry: IMPLICITDENY. S3 `dynamodb:GetItem`, Attributes = ticket_id, requester: IMPLICITDENY; and Attributes = ticket_id, created_by: IMPLICITDENY. S4 `dynamodb:Query` and `dynamodb:Scan` (with the allowed Attributes and Select): IMPLICITDENY; also `dynamodb:BatchGetItem` and `dynamodb:PutItem`: IMPLICITDENY. S5 `dynamodb:GetItem` with the allowed Attributes on table/opal-users-v2, and on table/opal-tickets/index/status-index: IMPLICITDENY (for the role after apply, S5 on opal-users-v2 may be allowed by the role's OTHER policies: print what the R0 baseline said for it and require the V reading to equal R0's; the new policy must not be the matched policy).
  </context>

  <the_act>
    GO: both halves are signed AND my GO message names the trunk commit and says run 7I is terminal. Start at step 1 and go on only while each step reads green. Otherwise tell 2.0.0_SA_COO~Y2 and wait.
    1. Read both halves at HEAD; `git hash-object` of the COO half must print 2f30cbbe6ee56bdbda58db3dcf45323890ac7502; the CTO half names it. Open the NEVER-2 ledger irpt-resident-ticket-read-20261021 (legs R0 before-reads, C plan, S simulations, A apply, V after-reads) and commit it; read every live worktree's org/critical_paths/.open_deploys/ FIRST (git worktree list --porcelain, then git -C <wt> ls-tree) and print the denominator: another open entry naming the ycharts Terraform stack, the role irpt-ycharts-runner-role or any IAM apply is a STOP.
    2. R0: `aws iam list-role-policies` (the five inline names) with the sha256 of the canonical (key-sorted, compact) JSON of each inline policy document; `aws iam list-attached-role-policies` (AmazonSSMManagedInstanceCore and irpt-audit-write-policy expected); `aws iam get-policy` for the new policy's ARN (the name `module.resident_ticket_read_policy_name` renders: take it from the plan; before the apply it must NOT exist); `aws iam simulate-principal-policy` for the role on the five arms: the baseline (S1 implicitDeny; print each). Any other state: STOP.
    3. C: in a throwaway worktree detached at the trunk commit that carries the pinned blob (outside the product tree; your usual way for the Terraform stacks), `terraform fmt -check resident_ticket_read_policy.tf` (rc 0, else STOP and tell me), `terraform init` as the stack does, then the saved plan with `-target=aws_iam_policy.resident_ticket_read -target=aws_iam_role_policy_attachment.runner_resident_ticket_read`: `Plan: 2 to add, 0 to change, 0 to destroy`, the policy document exactly the ONE statement `ReadTheFiledTicketForTheAuditOnly` (Effect Allow, Action exactly `dynamodb:GetItem`, Resource exactly one `arn:aws:dynamodb:us-east-1:313476888478:table/opal-tickets` with no /index/ and no wildcard, Condition exactly Null dynamodb:Attributes=false, ForAllValues:StringEquals dynamodb:Attributes = the four names, StringEqualsIfExists dynamodb:Select = SPECIFIC_ATTRIBUTES: print them), the attachment targeting `irpt-ycharts-runner-role` only. Anything else: STOP, nothing applied.
    4. S (before apply): render the planned policy document (`terraform show -json` of the saved plan) and run the five arms with `simulate-custom-policy`; print each decision beside its expectation. Any arm that differs (S2 ALLOWED above all): STOP, nothing applied, and send me the printed decisions.
    5. A: `.tools/safe-apply.sh` on the saved plan; never `aws iam create-policy`, `attach-role-policy` or `put-role-policy`.
    6. V: G1 the five inline policies' canonical sha256 equal R0's (print them side by side); `list-attached-role-policies` is R0's list plus the new policy; the new policy's default version holds exactly the one statement. G2 `simulate-principal-policy` for the role repeats the five arms (S1 allowed, matched policy = the new policy; the others as above). G3 a second plan of the same targets reads `No changes`.
    7. Write org/tier2_senior/0.7.0_AE_CloudOps~IB2/deliverables/irpt_anlreq_ticketread/A_AFTER_TICKETREAD.txt with ONE line each, exactly: `R0 baseline implicitDeny on the ticket read`, `C plan 2 to add 0 to change 0 to destroy`, `C policy is exactly the one ticket-read statement`, `S arms held before apply`, `G1 inline policies unchanged`, `G2 arms held on the role`, `G3 replan No changes`; then the new policy's ARN, the printed decision of every arm before and after, the R0 and V inline sha256 list and the attached lists before and after. A line that did not hold is written `<tag> FAIL <what was read>`. Close the ledger and report ONCE to 2.0.0_SA_COO~Y2, 1.0.0_SA_CTO~DELL2 and 2.0.0_SA_COO~G2: "ticket read policy closed" with the lines and the output path. Report the Terraform apply to 0.0.0_AB_MSTR~DELL2 after the fact. Remove every throwaway you made.
  </the_act>

  <bounds>
    Two new resources: one managed policy and its attachment to one role. No inline policy changes, no other action, table or index, no trust change, no bucket or key policy, no deploy of code. Rollback: the packet's section 5 (revert the Terraform commit, scoped plan 0/0/2, safe-apply).
  </bounds>

  <paths>
    org/tier2_senior/0.7.0_AE_CloudOps~IB2/deliverables/
    org/tier2_senior/0.7.0_AE_CloudOps~IB2/logs/
    org/critical_paths/change_management/
    org/critical_paths/.open_deploys/
  </paths>

  <proof_of_spec>
Instance at `org/tier2_senior/0.7.0_AE_CloudOps~IB2/deliverables/irpt_anlreq_ticketread/IRPT_ANLREQ.TO-APPLY-TICKETREAD.resident-attribute-restricted-ticket-read-managed-policy-ib2.proof_of_spec.json`.
    <criterion id="TKRD-AC1" cell_refs="AR-y-488">The record holds the seven lines, each as written (a FAIL line does not match).<invocation>grep -c -E '^(R0 baseline implicitDeny on the ticket read|C plan 2 to add 0 to change 0 to destroy|C policy is exactly the one ticket-read statement|S arms held before apply|G1 inline policies unchanged|G2 arms held on the role|G3 replan No changes)$' org/tier2_senior/0.7.0_AE_CloudOps~IB2/deliverables/irpt_anlreq_ticketread/A_AFTER_TICKETREAD.txt</invocation><expect>^7$</expect></criterion>
    <criterion id="TKRD-AC2" cell_refs="AR-y-488">The ledger irpt-resident-ticket-read-20261021 is CLOSED.<invocation>grep -m1 '^\*\*Status' org/critical_paths/change_management/*irpt-resident-ticket-read-20261021_deploy_completion.md</invocation><expect>^\*\*Status:\*\* CLOSED</expect></criterion>
  </proof_of_spec>
</task_order>
# pipeline-override: an APPLY order to a tier-2 applier under a signed pair (not a worker cell); the cell AR-y-488 is the issuer's, as for TO-APPLY-AUDITPOLICY.
