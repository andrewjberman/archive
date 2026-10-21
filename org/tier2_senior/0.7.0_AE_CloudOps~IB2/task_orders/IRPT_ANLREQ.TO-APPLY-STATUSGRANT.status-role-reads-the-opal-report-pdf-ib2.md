<task_order>
  <metadata>
    <id>IRPT_ANLREQ.TO-APPLY-STATUSGRANT.status-role-reads-the-opal-report-pdf-ib2</id>
    <issued_by>2.0.0_SA_COO~Y2</issued_by>
    <issued_to>0.7.0_AE_CloudOps~IB2</issued_to>
    <date>2026-10-20</date>
    <status>complete</status><!-- flipped by issuer 2.0.0_SA_COO~Y2 2026-10-21 (round hygiene, CTO msg ~15:10Z): every criterion invocation re-run by the issuer and matched; the proof instance reads VALID rc 0 -->
    <project_code>IRPT_ANLREQ</project_code>
  </metadata>
<risk>WORLD</risk>
<proof_genre>DEPLOY</proof_genre>
<round>43</round>
<workstream>ZZ123</workstream>
<placeholders>NONE</placeholders>
<decomp_ref>
<decomp_doc>org/missions/D9/IRPT/IRPT_ANLREQ/decompositions/IRPT_ANLREQ_DECOMP_R40A_Y.md</decomp_doc>
<owned_cells>AR-y-464</owned_cells>
<decomp_context>Round 43, cell AR-y-464: apply the one-statement resource extension (s3:GetObject and s3:GetObjectVersion on the YCHARTS_OPAL_REPORT prefixes of the 3 client firms) to the inline policy irpt-status-policy of the role irpt-status-role, so the status route can read the retained Opal report PDF (run 7b stopped at R: s3:GetObjectVersion denied).</decomp_context>
</decomp_ref>
<preflight>
comp-blast: DECLARED-NOT-APPLICABLE -- the blast radius is the signed pair's section 3: three resource entries added to one statement of one inline policy of one role, read only; no other statement, trust, bucket policy, key policy, Lambda, queue or table changes.
comp-routes: DECLARED-NOT-APPLICABLE. comp-cache: DECLARED-NOT-APPLICABLE. comp-schedule: DECLARED-NOT-APPLICABLE.
comp-iam: RUN -- this order IS an IAM change: the statement's resources extended through Terraform (scoped plan 0/1/0, safe-apply); before and after reads of the policy document and policy simulations on run 7b's real PDF key.
comp-adversary: RUN -- a plan that touches anything but the one policy (STOP); a policy diff that adds more than the three resource entries or changes any other statement (STOP, nothing applied); a typed ARN or a Put/List/Delete action (read the plan, not the claim); `terraform fmt -check` red at the drained commit (STOP: whitespace re-pin is the issuer's act, as TO-APPLY-MODELGRANT showed); an apply from a Terraform root that is not the one that declares the resource (STOP); another IB2 act open, in particular 2.0.0_SA_COO~G2's resident-role apply (do not start); Andrew's ticket touched (forbidden). NOT seen (blind): the live policy until R0; denominator: one role policy.
</preflight>

  <objective>
    Apply the signed pair's one extension and nothing else: read the live policy, plan with the ops/iam.tf of the drained commit, prove the plan adds exactly the three resource entries, apply it with safe-apply, read it back, prove by simulation that `irpt-status-role` may now GET and GetObjectVersion (not PUT) on run 7b's retained Opal report PDF key, close the ledger, report ONCE. If any step does not read green, STOP and say so to 2.0.0_SA_COO~Y2. THIS ORDER STARTS ONLY ON MY GO MESSAGE.
  </objective>

  <context>
    Load /cloud-ops first. Signed pair: COO half org/missions/D9/IRPT/IRPT_ANLREQ/deliverables/2.0.0_SA_COO~Y2/iam_grant_status/NEVER_WIDEN_PACKET_STATUS_ROLE_READS_OPAL_REPORT_PDF_20261020.md (`git hash-object` must print d6011af96ef46bbfb3f90abfc5ea5a07f7efe76b; commit aaf8e74cad) and the CTO half org/missions/D9/IRPT/IRPT_ANLREQ/deliverables/1.0.0_SA_CTO~DELL2/NEVER_WIDEN_STATUS_ROLE_READS_OPAL_REPORT_PDF_CTO_HALF.md (signed @8461e95c62, CTO msg 11475; it must name the COO blob above). A different COO blob voids both halves: STOP. The packet is the plan: sections 3 (blast radius), 4 (apply protocol), 5 (rollback). Content pin: `infra/aws/terraform/investor-reporting/ops/iam.tf` at git blob 04b6c4e8a8b8ce534d14b6bdc6d851e873dcd5df (`git rev-parse <drained commit>:infra/aws/terraform/investor-reporting/ops/iam.tf` must print it); the drained commit is 9b614db42a1ebe9892f7ef7e52456f12718a510f (worker 328, order TO-AR-y-463; +7 -1 against the cut e02d849d49). Terraform root: infra/aws/terraform/investor-reporting/ops, resource aws_iam_role_policy.irpt_status, policy name irpt-status-policy on role irpt-status-role. THE CTO'S CONDITIONS: scoped plan expects EXACTLY 0 to add, 1 to change, 0 to destroy; outside the weekday 11:30Z-14:15Z band; never alongside another IB2 act (2.0.0_SA_COO~G2's resident-role apply is separate and waits for its own re-pin); Andrew's ticket TCK-20261017-5af976ff is not touched. The simulation key: the retained PDF of run 7b, exact key in `org/missions/D9/IRPT/IRPT_ANLREQ/deliverables/2.0.0_SA_COO~Y2/synthetic_residue_delete_list_supplement_run7b_20261020.json` (the entry whose key contains `/state/ycharts_opal_reports/ART-ed570a0d`), bucket opal-data-irpt.
  </context>

  <the_act>
    GO: both halves are signed AND my GO message names the drained commit. Start at step 1 and go on only while each step reads green. Otherwise tell 2.0.0_SA_COO~Y2 and wait.
    1. Read both halves at HEAD; `git hash-object` of the COO half must print d6011af96ef46bbfb3f90abfc5ea5a07f7efe76b; the blob check above must print 04b6c4e8a8b8ce534d14b6bdc6d851e873dcd5df. Open the NEVER-2 ledger irpt-status-opal-report-read-20261020 (legs R0 before-reads, C plan, A apply, V after-reads) and commit it; read every live worktree's org/critical_paths/.open_deploys/ FIRST (git worktree list --porcelain, then git -C <wt> ls-tree) and print the denominator: another open entry naming the ops Terraform stack, the role irpt-status-role or its policy is a STOP.
    2. R0: `aws iam get-role-policy --role-name irpt-status-role --policy-name irpt-status-policy`: record the statement ids (Sid list), the resources of `ReadRetainedAnalysisFamiliesUnderThePolicyPrefixesOnly` (18 expected) and the sha256 of the canonical (key-sorted, compact) JSON of the document; `aws iam simulate-principal-policy` for the role on `s3:GetObject` and `s3:GetObjectVersion` against the 7b PDF key: both must read implicitDeny (the baseline). Any other state (the family already present, or an allow): STOP.
    3. C: in a throwaway worktree detached at the drained commit (outside the product tree; your usual way for the Terraform stacks), `terraform fmt -check iam.tf` in the root folder (rc 0, else STOP and tell me: a whitespace re-pin is my act), `terraform init` as the stack does, then the saved scoped plan `-target=aws_iam_role_policy.irpt_status`: `Plan: 0 to add, 1 to change, 0 to destroy`, the only changed attribute `policy`, and the policy document diff adds exactly THREE resource entries `arn:aws:s3:::opal-data-irpt/irpt/<firm>/state/ycharts_opal_reports/*` (one per firm; print them) to that one statement, and changes or removes no other statement or resource (print the R0 Sid list beside the planned Sid list). Anything else: STOP, nothing applied.
    4. A: `.tools/safe-apply.sh` on the saved plan; never `aws iam put-role-policy`.
    5. V: G1 `get-role-policy`: the Sid list equals the R0 list, every statement other than the retained-families statement is byte-equal to R0's (compare per Sid), and that statement's resources equal R0's plus the three. G2 the simulation on the 7b PDF key: `s3:GetObject` and `s3:GetObjectVersion` = allowed (print the matched statement id), `s3:PutObject` = implicitDeny; and a key under `original_holdings` of the same firm unchanged (allowed). G3 a second plan of the same target reads `No changes`.
    6. Write org/tier2_senior/0.7.0_AE_CloudOps~IB2/deliverables/irpt_anlreq_statusgrant/A_AFTER_STATUSGRANT.txt with ONE line each, exactly: `R0 baseline implicitDeny get and getversion`, `C plan 0 to add 1 to change 0 to destroy`, `C policy diff adds exactly three ycharts_opal_reports resources`, `G1 other statements byte-equal`, `G2 get and getversion allowed put implicitDeny on ycharts_opal_reports`, `G3 replan No changes`; then the R0 Sid list, the planned Sid list and the document sha256 before and after. A line that did not hold is written `<tag> FAIL <what was read>`. Close the ledger and report ONCE to 2.0.0_SA_COO~Y2 and 1.0.0_SA_CTO~DELL2: "status grant closed" with the lines and the output path. Report the Terraform apply to 0.0.0_AB_MSTR~DELL2 after the fact. Remove every throwaway you made.
  </the_act>

  <bounds>
    One inline policy of one role, one statement's resource list extended by three read-only entries. No Put, List or Delete grant, no other statement, no trust change, no bucket or key policy, no deploy of code. Rollback: the packet's section 5 (revert the Terraform commit, scoped plan 0/1/0, safe-apply).
  </bounds>

  <paths>
    org/tier2_senior/0.7.0_AE_CloudOps~IB2/deliverables/
    org/tier2_senior/0.7.0_AE_CloudOps~IB2/logs/
    org/critical_paths/change_management/
    org/critical_paths/.open_deploys/
  </paths>

  <proof_of_spec>
Instance at `org/tier2_senior/0.7.0_AE_CloudOps~IB2/deliverables/irpt_anlreq_statusgrant/IRPT_ANLREQ.TO-APPLY-STATUSGRANT.status-role-reads-the-opal-report-pdf-ib2.proof_of_spec.json`.
    <criterion id="STG-AC1" cell_refs="AR-y-464">The record holds the six lines, each as written (a FAIL line does not match).<invocation>grep -c -E '^(R0 baseline implicitDeny get and getversion|C plan 0 to add 1 to change 0 to destroy|C policy diff adds exactly three ycharts_opal_reports resources|G1 other statements byte-equal|G2 get and getversion allowed put implicitDeny on ycharts_opal_reports|G3 replan No changes)$' org/tier2_senior/0.7.0_AE_CloudOps~IB2/deliverables/irpt_anlreq_statusgrant/A_AFTER_STATUSGRANT.txt</invocation><expect>^6$</expect></criterion>
    <criterion id="STG-AC2" cell_refs="AR-y-464">The ledger irpt-status-opal-report-read-20261020 is CLOSED.<invocation>grep -m1 '^\*\*Status' org/critical_paths/change_management/*irpt-status-opal-report-read-20261020_deploy_completion.md</invocation><expect>^\*\*Status:\*\* CLOSED</expect></criterion>
  </proof_of_spec>
</task_order>
# pipeline-override: an APPLY order to a tier-2 applier under a signed pair (not a worker cell); the cell AR-y-464 is the issuer's, as for TO-APPLY-IAMGRANT.
