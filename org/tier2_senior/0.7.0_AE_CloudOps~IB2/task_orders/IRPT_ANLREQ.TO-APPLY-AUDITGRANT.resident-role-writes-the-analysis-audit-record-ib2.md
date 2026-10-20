<task_order>
  <metadata>
    <id>IRPT_ANLREQ.TO-APPLY-AUDITGRANT.resident-role-writes-the-analysis-audit-record-ib2</id>
    <issued_by>2.0.0_SA_COO~Y2</issued_by>
    <issued_to>0.7.0_AE_CloudOps~IB2</issued_to>
    <date>2026-10-20</date>
    <status>staged</status>
    <project_code>IRPT_ANLREQ</project_code>
  </metadata>
<risk>WORLD</risk>
<proof_genre>DEPLOY</proof_genre>
<round>43</round>
<workstream>ZZ136</workstream>
<placeholders>NONE</placeholders>
<decomp_ref>
<decomp_doc>org/missions/D9/IRPT/IRPT_ANLREQ/decompositions/IRPT_ANLREQ_DECOMP_R40A_Y.md</decomp_doc>
<owned_cells>AR-y-477</owned_cells>
<decomp_context>Round 43, cell AR-y-477: apply the Put-only statement WriteTheAnalysisAudit and the KMS context-line extension to the inline policy irpt-ycharts-runner-resident-policy of the resident host's role irpt-ycharts-runner-role, so the packager's audit record (C-AUDIT-RECORD, AR-y-467 and AR-y-469) can be written to opal-data-irpt/irpt/&lt;firm&gt;/platinum/analysis_audit/.</decomp_context>
</decomp_ref>
<preflight>
comp-blast: DECLARED-NOT-APPLICABLE -- the blast radius is the signed pair's section 3: one Put-only statement and three entries on one KMS condition list of one inline policy of one role; no other statement, trust, bucket policy, key policy, Lambda, queue or table changes.
comp-routes: DECLARED-NOT-APPLICABLE. comp-cache: DECLARED-NOT-APPLICABLE. comp-schedule: DECLARED-NOT-APPLICABLE.
comp-iam: RUN -- this order IS an IAM change: through Terraform (scoped plan 0/1/0, safe-apply); before and after reads of the policy document and policy simulations on a sample audit key.
comp-adversary: RUN -- a plan that touches anything but the one policy (STOP); a policy diff that adds more than the one statement and the three KMS entries, or changes any other statement (STOP, nothing applied); a typed ARN or a Get/List/Delete action in the new statement (read the plan, not the claim); a prefix that names a client firm bucket instead of opal-data-irpt (STOP: the CTO refused that form once, msg 11537, withdrawn when the pinned blob was read); `terraform fmt -check` red (STOP and tell me); another IB2 act open, in particular run 7d or the r34o install (do not start); Andrew's ticket touched (forbidden). NOT seen (blind): the live policy until R0; denominator: one role policy.
</preflight>

  <objective>
    Apply the signed pair's changes and nothing else: read the live policy, plan with the resident.tf of the pinned blob, prove the plan adds exactly the one statement and the three KMS entries, apply it with safe-apply, read it back, prove by simulation that the role may now PUT (not GET, not DELETE) on a sample audit key under opal-data-irpt, close the ledger, report ONCE. If any step does not read green, STOP and say so to 2.0.0_SA_COO~Y2. THIS ORDER STARTS ONLY ON MY GO MESSAGE, which I send when run 7d is terminal and before 2.0.0_SA_COO~G2's r34o install.
  </objective>

  <context>
    Load /cloud-ops first. Signed pair: COO half org/missions/D9/IRPT/IRPT_ANLREQ/deliverables/2.0.0_SA_COO~Y2/iam_grant_audit/NEVER_WIDEN_PACKET_RESIDENT_ROLE_WRITES_ANALYSIS_AUDIT_20261020.md (`git hash-object` must print 0d1ab2373f4707c7f5757a191973ea1705b48139; commit 0f2c488b27) and the CTO half org/missions/D9/IRPT/IRPT_ANLREQ/deliverables/1.0.0_SA_CTO~DELL2/NEVER_WIDEN_RESIDENT_ROLE_WRITES_ANALYSIS_AUDIT_CTO_HALF.md (@8eba8b8ef4, CTO msg 11545; it must name the COO blob above). A different COO blob voids both halves: STOP. The packet is the plan: sections 3 (blast radius), 4 (apply protocol), 5 (rollback). Content pin: `infra/aws/terraform/investor-reporting/ycharts/resident.tf` at git blob efa98ea24952190f827ae6fe4df0f0b0f2a0a118 (`git rev-parse <the trunk commit you plan from>:infra/aws/terraform/investor-reporting/ycharts/resident.tf` must print it; it is on the trunk, drained 2ff88544d1d). Terraform root: infra/aws/terraform/investor-reporting/ycharts, resource aws_iam_role_policy.runner_resident, policy name irpt-ycharts-runner-resident-policy on role irpt-ycharts-runner-role. THE CTO'S CONDITIONS: scoped plan expects EXACTLY 0 to add, 1 to change, 0 to destroy; outside the weekday 11:30Z-14:15Z band; never alongside another IB2 act; Andrew's ticket TCK-20261017-5af976ff is not touched. The simulation key: the sample `irpt/49financial/platinum/analysis_audit/ART-<64 hex of your choice>/<64 hex>.json` in bucket opal-data-irpt (nothing is written: it is a simulation); also simulate the KMS action `kms:GenerateDataKey` on the system key with the context entry `kms:EncryptionContext:aws:s3:arn` set to `arn:aws:s3:::opal-data-irpt/irpt/49financial/platinum/analysis_audit/ART-<hex>/<hex>.json` and `kms:ViaService` set to `s3.us-east-1.amazonaws.com`.
  </context>

  <the_act>
    GO: both halves are signed AND my GO message names the trunk commit and says run 7d is terminal. Start at step 1 and go on only while each step reads green. Otherwise tell 2.0.0_SA_COO~Y2 and wait.
    1. Read both halves at HEAD; `git hash-object` of the COO half must print 0d1ab2373f4707c7f5757a191973ea1705b48139; the CTO half names it. Open the NEVER-2 ledger irpt-resident-audit-write-20261020 (legs R0 before-reads, C plan, A apply, V after-reads) and commit it; read every live worktree's org/critical_paths/.open_deploys/ FIRST (git worktree list --porcelain, then git -C <wt> ls-tree) and print the denominator: another open entry naming the ycharts Terraform stack, the role irpt-ycharts-runner-role or its policy is a STOP.
    2. R0: `aws iam get-role-policy --role-name irpt-ycharts-runner-role --policy-name irpt-ycharts-runner-resident-policy`: record the statement ids (Sid list), the length of the `kms:EncryptionContext:aws:s3:arn` list of `ReportEncryptionViaS3ForResidentFamiliesOnly` and the sha256 of the canonical (key-sorted, compact) JSON of the document; `aws iam simulate-principal-policy` for the role on `s3:PutObject` against the sample audit key: implicitDeny (the baseline); the KMS simulation: the baseline result. Any other state (the Sid already present, or an allow): STOP.
    3. C: in a throwaway worktree detached at the trunk commit that carries the pinned blob (outside the product tree; your usual way for the Terraform stacks), `terraform fmt -check resident.tf` (rc 0, else STOP and tell me), `terraform init` as the stack does, then the saved scoped plan `-target=aws_iam_role_policy.runner_resident`: `Plan: 0 to add, 1 to change, 0 to destroy`, the only changed attribute `policy`, and the policy document diff adds exactly ONE statement `WriteTheAnalysisAudit` (Effect Allow, Action exactly `s3:PutObject`, Resource exactly three `arn:aws:s3:::opal-data-irpt/irpt/<firm>/platinum/analysis_audit/*` entries: print them and CONFIRM the bucket is opal-data-irpt), adds exactly three entries to the KMS condition list (the same three prefixes), and changes or removes no other statement (print the R0 Sid list beside the planned list). Anything else: STOP, nothing applied.
    4. A: `.tools/safe-apply.sh` on the saved plan; never `aws iam put-role-policy`.
    5. V: G1 `get-role-policy`: the Sid list equals R0's plus WriteTheAnalysisAudit, every other statement except the KMS one is byte-equal to R0's (compare per Sid), and the KMS statement differs from R0's only by its condition list gaining the three prefixes. G2 the simulations: `s3:PutObject` on the sample audit key = allowed (print the matched statement id); `s3:GetObject`, `s3:GetObjectVersion` and `s3:DeleteObject` on it = implicitDeny; `s3:PutObject` on a key under another family of the same bucket unchanged from R0; the KMS simulation allowed. G3 a second plan of the same target reads `No changes`.
    6. Write org/tier2_senior/0.7.0_AE_CloudOps~IB2/deliverables/irpt_anlreq_auditgrant/A_AFTER_AUDITGRANT.txt with ONE line each, exactly: `R0 baseline implicitDeny put on the audit key`, `C plan 0 to add 1 to change 0 to destroy`, `C policy diff adds exactly WriteTheAnalysisAudit and three KMS entries`, `C bucket is opal-data-irpt`, `G1 other statements byte-equal`, `G2 put allowed get delete implicitDeny on the audit key`, `G3 replan No changes`; then the R0 Sid list, the planned Sid list, the KMS list lengths before and after and the document sha256 before and after. A line that did not hold is written `<tag> FAIL <what was read>`. Close the ledger and report ONCE to 2.0.0_SA_COO~Y2, 1.0.0_SA_CTO~DELL2 and 2.0.0_SA_COO~G2: "audit grant closed" with the lines and the output path. Report the Terraform apply to 0.0.0_AB_MSTR~DELL2 after the fact. Remove every throwaway you made.
  </the_act>

  <bounds>
    One inline policy of one role: one Put-only statement added and one condition list extended. No Get, List or Delete grant, no other statement, no trust change, no bucket or key policy, no deploy of code. Rollback: the packet's section 5 (revert the Terraform commit, scoped plan 0/1/0, safe-apply).
  </bounds>

  <paths>
    org/tier2_senior/0.7.0_AE_CloudOps~IB2/deliverables/
    org/tier2_senior/0.7.0_AE_CloudOps~IB2/logs/
    org/critical_paths/change_management/
    org/critical_paths/.open_deploys/
  </paths>

  <proof_of_spec>
Instance at `org/tier2_senior/0.7.0_AE_CloudOps~IB2/deliverables/irpt_anlreq_auditgrant/IRPT_ANLREQ.TO-APPLY-AUDITGRANT.resident-role-writes-the-analysis-audit-record-ib2.proof_of_spec.json`.
    <criterion id="AUDG-AC1" cell_refs="AR-y-477">The record holds the seven lines, each as written (a FAIL line does not match).<invocation>grep -c -E '^(R0 baseline implicitDeny put on the audit key|C plan 0 to add 1 to change 0 to destroy|C policy diff adds exactly WriteTheAnalysisAudit and three KMS entries|C bucket is opal-data-irpt|G1 other statements byte-equal|G2 put allowed get delete implicitDeny on the audit key|G3 replan No changes)$' org/tier2_senior/0.7.0_AE_CloudOps~IB2/deliverables/irpt_anlreq_auditgrant/A_AFTER_AUDITGRANT.txt</invocation><expect>^7$</expect></criterion>
    <criterion id="AUDG-AC2" cell_refs="AR-y-477">The ledger irpt-resident-audit-write-20261020 is CLOSED.<invocation>grep -m1 '^\*\*Status' org/critical_paths/change_management/*irpt-resident-audit-write-20261020_deploy_completion.md</invocation><expect>^\*\*Status:\*\* CLOSED</expect></criterion>
  </proof_of_spec>
</task_order>
# pipeline-override: an APPLY order to a tier-2 applier under a signed pair (not a worker cell); the cell AR-y-477 is the issuer's, as for TO-APPLY-STATUSGRANT.
