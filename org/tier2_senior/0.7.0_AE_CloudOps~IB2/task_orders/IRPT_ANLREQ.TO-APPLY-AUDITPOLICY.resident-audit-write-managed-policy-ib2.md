<task_order>
  <metadata>
    <id>IRPT_ANLREQ.TO-APPLY-AUDITPOLICY.resident-audit-write-managed-policy-ib2</id>
    <issued_by>2.0.0_SA_COO~Y2</issued_by>
    <issued_to>0.7.0_AE_CloudOps~IB2</issued_to>
    <date>2026-10-20</date>
    <status>complete</status><!-- flipped by issuer 2.0.0_SA_COO~Y2 2026-10-21 (round hygiene, CTO msg ~15:10Z): every criterion invocation re-run by the issuer and matched; the proof instance reads VALID rc 0 --><!-- RE-PINNED 2026-10-21 by 2.0.0_SA_COO~Y2 after run 7e (S239) and order AR-y-481: new blobs and packet hash; held until the CTO half names the new packet blob and r34p is live -->
    <project_code>IRPT_ANLREQ</project_code>
  </metadata>
<risk>WORLD</risk>
<proof_genre>DEPLOY</proof_genre>
<round>43</round>
<workstream>ZZ138</workstream>
<placeholders>NONE</placeholders>
<decomp_ref>
<decomp_doc>org/missions/D9/IRPT/IRPT_ANLREQ/decompositions/IRPT_ANLREQ_DECOMP_R40A_Y.md</decomp_doc>
<owned_cells>AR-y-479</owned_cells>
<decomp_context>Round 43, cell AR-y-479: apply ONE new customer-managed IAM policy (a Put-only statement on opal-data-irpt/irpt/&lt;firm&gt;/platinum/analysis_audit/ and a KMS statement narrowed to those prefixes) and its attachment to irpt-ycharts-runner-role, so the packager's audit record (C-AUDIT-RECORD) can be written; this replaces the inline form of AR-y-477, whose apply stopped at the 10240-byte inline cap.</decomp_context>
</decomp_ref>
<preflight>
comp-blast: DECLARED-NOT-APPLICABLE -- the blast radius is the signed pair's section 3: two new resources (one managed policy, one attachment to one role); the role's five inline policies, trust, existing attached policy, bucket policy, key policy, Lambdas, queues and tables do not change.
comp-routes: DECLARED-NOT-APPLICABLE. comp-cache: DECLARED-NOT-APPLICABLE. comp-schedule: DECLARED-NOT-APPLICABLE.
comp-iam: RUN -- this order IS an IAM change: two resources added through Terraform (scoped plan 2/0/0, safe-apply); before and after reads of the inline and attached policies and policy simulations on a sample audit key.
comp-adversary: RUN -- a plan that touches anything but the two named resources (STOP); a plan that CHANGES or destroys anything (STOP: the inline policy must not move); a policy document with more than the two statements, a Get/List/Delete action, a typed ARN, or a prefix that names a client firm bucket instead of opal-data-irpt (STOP); `terraform fmt -check` red (STOP and tell me); another IAM apply open, in particular TV2's TO-R22-DL1 or the r34o install (do not start); Andrew's ticket TCK-20261017-5af976ff or TCK-20261020-b1d61f80 touched (forbidden). NOT seen (blind): the live state until R0; denominator: one role.
</preflight>

  <objective>
    Apply the signed pair's two new resources and nothing else: read the role's live policies, plan with the two pinned files, prove the plan adds exactly the policy and its attachment, apply it with safe-apply, read it back, prove by simulation that the role may now PUT (not GET, not DELETE) on a sample audit key under opal-data-irpt, close the ledger, report ONCE. If any step does not read green, STOP and say so to 2.0.0_SA_COO~Y2. THIS ORDER STARTS ONLY ON MY GO MESSAGE, which I send after TV2's TO-R22-DL1 reports terminal (r34o and r34p are installed and closed; the GO message of 2026-10-21 supersedes this timing).
  </objective>

  <context>
    Load /cloud-ops first. Signed pair: COO half org/missions/D9/IRPT/IRPT_ANLREQ/deliverables/2.0.0_SA_COO~Y2/iam_grant_audit/NEVER_WIDEN_PACKET_RESIDENT_AUDIT_WRITE_MANAGED_POLICY_20261020.md (`git hash-object` must print 9f065fb2a59b247318d8144c754c7bd024419121; commit 8dff583d11) and the CTO half named in my GO (RE-SIGNED @d421313363 on the packet blob 9f065fb2a5, CTO msg 11679 (the first half, @0cd9cae5b0 msg 11589, named the old packet blob and is VOID); it must name that blob). A different COO blob voids both halves: STOP. The packet is the plan: sections 3 (blast radius), 4 (apply protocol), 5 (rollback). Content pins on the trunk (drained f0abc252167): `infra/aws/terraform/investor-reporting/ycharts/resident_audit_policy.tf` at git blob 0e084af9b8868f3949127dc7543751ac7204229a and `infra/aws/terraform/investor-reporting/ycharts/resident.tf` at git blob 2e9a61e656141c8a5194fa942312c0d7aef843a8 (`git rev-parse <the trunk commit you plan from>:<path>` must print each). Terraform root: infra/aws/terraform/investor-reporting/ycharts. THE CTO'S CONDITIONS: scoped plan expects EXACTLY 2 to add, 0 to change, 0 to destroy; outside the weekday 11:30Z-14:15Z band; never alongside another IB2 act or any other IAM apply; the tickets named above are not touched. The earlier order for the inline form (IRPT_ANLREQ.TO-APPLY-AUDITGRANT.resident-role-writes-the-analysis-audit-record-ib2.md) is SUPERSEDED by this one: do not run it. The simulation key: a sample `irpt/49financial/platinum/analysis_audit/ART-<64 hex of your choice>/<64 hex>.json` in bucket opal-data-irpt (nothing is written); also the KMS simulation (GenerateDataKey on the system key, context `kms:EncryptionContext:aws:s3:arn` = that object's ARN, `kms:ViaService` = `s3.us-east-1.amazonaws.com`).
  </context>

  <the_act>
    GO: both halves are signed AND my GO message names the trunk commit and says TV2's pass is terminal. Start at step 1 and go on only while each step reads green. Otherwise tell 2.0.0_SA_COO~Y2 and wait.
    1. Read both halves at HEAD; `git hash-object` of the COO half must print 9f065fb2a59b247318d8144c754c7bd024419121; the CTO half names it. Open the NEVER-2 ledger irpt-resident-audit-policy-20261020 (legs R0 before-reads, C plan, A apply, V after-reads) and commit it; read every live worktree's org/critical_paths/.open_deploys/ FIRST (git worktree list --porcelain, then git -C <wt> ls-tree) and print the denominator: another open entry naming the ycharts Terraform stack, the role irpt-ycharts-runner-role or any IAM apply is a STOP.
    2. R0: `aws iam list-role-policies` (the five inline names) with the sha256 of the canonical (key-sorted, compact) JSON of each inline policy document; `aws iam list-attached-role-policies` (AmazonSSMManagedInstanceCore expected); `aws iam get-policy` for the new policy's ARN (it is the name `module.resident_audit_policy_name` renders: take it from the plan; before the apply it must NOT exist); `aws iam simulate-principal-policy` for the role on `s3:PutObject` against the sample audit key: implicitDeny; the KMS simulation: the baseline result. Any other state: STOP.
    3. C: in a throwaway worktree detached at the trunk commit that carries the two pinned blobs (outside the product tree; your usual way for the Terraform stacks), `terraform fmt -check resident.tf resident_audit_policy.tf` (rc 0, else STOP and tell me), `terraform init` as the stack does, then the saved plan with `-target=aws_iam_policy.resident_audit_write -target=aws_iam_role_policy_attachment.runner_resident_audit_write`: `Plan: 2 to add, 0 to change, 0 to destroy`, the policy document exactly the two statements `WriteTheAnalysisAudit` (Effect Allow, Action exactly `s3:PutObject`, Resource exactly three `arn:aws:s3:::opal-data-irpt/irpt/<firm>/platinum/analysis_audit/*` entries: print them and CONFIRM the bucket is opal-data-irpt) and `AuditEncryptionViaS3ForAuditPrefixesOnly` (kms:Decrypt and kms:GenerateDataKey, the same three prefixes in the context list), the attachment targeting `irpt-ycharts-runner-role` only. Anything else: STOP, nothing applied.
    4. A: `.tools/safe-apply.sh` on the saved plan; never `aws iam create-policy`, `attach-role-policy` or `put-role-policy`.
    5. V: G1 the five inline policies' canonical sha256 equal R0's (print them side by side); `list-attached-role-policies` is R0's list plus the new policy; the new policy's default version holds exactly the two statements (compare their Sids and Actions). G2 the simulations on the sample audit key: `s3:PutObject` = allowed (print the matched policy name); `s3:GetObject`, `s3:GetObjectVersion`, `s3:DeleteObject` = implicitDeny; `s3:PutObject` on a key under another family of the same bucket unchanged from R0; the KMS simulation allowed. G3 a second plan of the same targets reads `No changes`.
    6. Write org/tier2_senior/0.7.0_AE_CloudOps~IB2/deliverables/irpt_anlreq_auditpolicy/A_AFTER_AUDITPOLICY.txt with ONE line each, exactly: `R0 baseline implicitDeny put on the audit key`, `C plan 2 to add 0 to change 0 to destroy`, `C policy is exactly the two audit statements`, `C bucket is opal-data-irpt`, `G1 inline policies unchanged`, `G2 put allowed get delete implicitDeny on the audit key`, `G3 replan No changes`; then the new policy's ARN, the R0 and V inline sha256 list and the attached lists before and after. A line that did not hold is written `<tag> FAIL <what was read>`. Close the ledger and report ONCE to 2.0.0_SA_COO~Y2, 1.0.0_SA_CTO~DELL2 and 2.0.0_SA_COO~G2: "audit policy closed" with the lines and the output path. Report the Terraform apply to 0.0.0_AB_MSTR~DELL2 after the fact. Remove every throwaway you made.
  </the_act>

  <bounds>
    Two new resources: one managed policy and its attachment to one role. No inline policy changes, no Get, List or Delete grant, no trust change, no bucket or key policy, no deploy of code. Rollback: the packet's section 5 (revert the Terraform commit, scoped plan 0/0/2, safe-apply).
  </bounds>

  <paths>
    org/tier2_senior/0.7.0_AE_CloudOps~IB2/deliverables/
    org/tier2_senior/0.7.0_AE_CloudOps~IB2/logs/
    org/critical_paths/change_management/
    org/critical_paths/.open_deploys/
  </paths>

  <proof_of_spec>
Instance at `org/tier2_senior/0.7.0_AE_CloudOps~IB2/deliverables/irpt_anlreq_auditpolicy/IRPT_ANLREQ.TO-APPLY-AUDITPOLICY.resident-audit-write-managed-policy-ib2.proof_of_spec.json`.
    <criterion id="AUDP-AC1" cell_refs="AR-y-479">The record holds the seven lines, each as written (a FAIL line does not match).<invocation>grep -c -E '^(R0 baseline implicitDeny put on the audit key|C plan 2 to add 0 to change 0 to destroy|C policy is exactly the two audit statements|C bucket is opal-data-irpt|G1 inline policies unchanged|G2 put allowed get delete implicitDeny on the audit key|G3 replan No changes)$' org/tier2_senior/0.7.0_AE_CloudOps~IB2/deliverables/irpt_anlreq_auditpolicy/A_AFTER_AUDITPOLICY.txt</invocation><expect>^7$</expect></criterion>
    <criterion id="AUDP-AC2" cell_refs="AR-y-479">The ledger irpt-resident-audit-policy-20261020 is CLOSED.<invocation>grep -m1 '^\*\*Status' org/critical_paths/change_management/*irpt-resident-audit-policy-20261020_deploy_completion.md</invocation><expect>^\*\*Status:\*\* CLOSED</expect></criterion>
  </proof_of_spec>
</task_order>
# pipeline-override: an APPLY order to a tier-2 applier under a signed pair (not a worker cell); the cell AR-y-479 is the issuer's, as for TO-APPLY-STATUSGRANT.
