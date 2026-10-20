<task_order>
  <metadata>
    <id>IRPT_ANLREQ.TO-APPLY-IAMGRANT.resident-role-reads-the-analysis-commentary-draft-ib2</id>
    <issued_by>2.0.0_SA_COO~Y2</issued_by>
    <issued_to>0.7.0_AE_CloudOps~IB2</issued_to>
    <date>2026-10-20</date>
    <status>pending</status>
    <project_code>IRPT_ANLREQ</project_code>
  </metadata>
<risk>WORLD</risk>
<proof_genre>DEPLOY</proof_genre>
<round>43</round>
<workstream>ZZ106</workstream>
<placeholders>NONE</placeholders>
<decomp_ref>
<decomp_doc>org/missions/D9/IRPT/IRPT_ANLREQ/decompositions/IRPT_ANLREQ_DECOMP_R40A_Y.md</decomp_doc>
<owned_cells>AR-y-447</owned_cells>
<decomp_context>Round 43, cell AR-y-447: apply the one-statement IAM grant (s3:GetObject and s3:GetObjectVersion on the ANALYSIS_COMMENTARY prefixes of the 3 client firms) to the inline policy of the resident host's role irpt-ycharts-runner-role, so the packager can read the commentary draft (probe B: head 403, get AccessDenied).</decomp_context>
</decomp_ref>
<preflight>
comp-blast: DECLARED-NOT-APPLICABLE -- the blast radius is the signed pair's section 3: one inline-policy statement, read only, on one role; no other statement, trust, bucket policy, key policy, Lambda, queue or table changes.
comp-routes: DECLARED-NOT-APPLICABLE. comp-cache: DECLARED-NOT-APPLICABLE. comp-schedule: DECLARED-NOT-APPLICABLE.
comp-iam: RUN -- this order IS an IAM change: ONE statement added to aws_iam_role_policy.runner_resident through Terraform (scoped plan 0/1/0, safe-apply); before and after reads of the policy document and policy simulations on the real run-6 keys.
comp-adversary: RUN -- a plan that touches anything but the one policy (STOP); a policy diff that adds or changes more than the one statement (STOP, nothing applied); a typed ARN or a Put/List/Delete action in the statement (the pin's checks say none; read the plan, not the claim); an apply from a Terraform root that is not the one that declares the resource (STOP, say so); another IB2 act open (do not start); Andrew's ticket touched (forbidden). NOT seen (blind): the live policy until R0; denominator: one role policy.
</preflight>

  <objective>
    Apply the one-statement IAM grant of the signed pair and nothing else: read the live policy, plan with the resident.tf of the pin, prove the plan adds exactly the one statement, apply it with safe-apply, read it back, prove by simulation that the role may now GET (not PUT) under analysis_commentaries on a real run-6 key, close the ledger, report ONCE. If any step does not read green, STOP and say so to 2.0.0_SA_COO~Y2. THIS ORDER STARTS ONLY ON MY GO MESSAGE (the CTO half must be signed and named there).
  </objective>

  <context>
    Load /cloud-ops first. Signed pair: COO half org/missions/D9/IRPT/IRPT_ANLREQ/deliverables/2.0.0_SA_COO~Y2/iam_grant/NEVER_WIDEN_PACKET_RESIDENT_ROLE_READS_COMMENTARY_DRAFT_20261020.md (`git hash-object` must print 43229821996608413194f6d19413a411d1c315d8; commit 2ce835d0ba) and the CTO half org/missions/D9/IRPT/IRPT_ANLREQ/deliverables/1.0.0_SA_CTO~DELL2/NEVER_WIDEN_RESIDENT_ROLE_READS_COMMENTARY_DRAFT_CTO_HALF.md (signed in commit c72cacf8531, CTO msg 11287; it must name the COO blob above). A different COO blob voids both halves: STOP. The packet is the plan: sections 3 (blast radius), 4 (apply protocol), 5 (rollback). Pin 430cd08b2aac7ef74dd31ba78a856032a0343ad3 (the Terraform edit of infra/aws/terraform/investor-reporting/ycharts/resident.tf: 21 insertions, 0 deletions; merged bb3c5906b25). Terraform root: infra/aws/terraform/investor-reporting/ycharts, resource aws_iam_role_policy.runner_resident, policy name irpt-ycharts-runner-resident-policy on role irpt-ycharts-runner-role. THE CTO'S CONDITIONS: scoped plan expects EXACTLY 0 to add, 1 to change, 0 to destroy; outside the weekday 11:30Z-14:15Z band; never alongside another IB2 act; Andrew's ticket TCK-20261017-5af976ff is not touched. The simulation keys: take the key of run 6's leftover commentary draft from org/tier2_senior/0.7.0_AE_CloudOps~IB2/deliverables/irpt_anlreq_commentary_e2e6/state_e2e6.json (leftover_blob_keys, the entry under analysis_commentaries/), bucket opal-data-irpt.
  </context>

  <the_act>
    GO: both halves are signed AND my GO message names the CTO half's commit. Start at step 1 and go on only while each step reads green. Otherwise tell 2.0.0_SA_COO~Y2 and wait.
    1. Read both halves at HEAD; `git hash-object` of the COO half must print 43229821996608413194f6d19413a411d1c315d8. Open the NEVER-2 ledger irpt-resident-commentary-read-20261020 (legs R0 before-reads, C plan, A apply, V after-reads) and commit it; read every live worktree's org/critical_paths/.open_deploys/ FIRST (git worktree list --porcelain, then git -C <wt> ls-tree) and print the denominator: another open entry naming the ycharts Terraform stack, the role irpt-ycharts-runner-role or its policy is a STOP.
    2. R0: `aws iam get-role-policy --role-name irpt-ycharts-runner-role --policy-name irpt-ycharts-runner-resident-policy`: record the statement ids (Sid list) and the sha256 of the canonical (key-sorted, compact) JSON of the document; `aws iam simulate-principal-policy` for the role on `s3:GetObject` and `s3:PutObject` against the run-6 commentary key: both must read implicitDeny (the baseline). Any other state (the Sid already present, or an allow): STOP.
    3. C: in a throwaway worktree detached at the pin (outside the product tree; your usual way for the Terraform stacks), `terraform fmt -check resident.tf` in the root folder (rc 0, else STOP), `terraform init` as the stack does, then the saved scoped plan `-target=aws_iam_role_policy.runner_resident`: `Plan: 0 to add, 1 to change, 0 to destroy`, the only changed attribute `policy`, and the policy document diff adds exactly ONE statement with `Sid` ReadTheAnalysisCommentaryDraft, Effect Allow, Action exactly `s3:GetObject` and `s3:GetObjectVersion`, Resource exactly three `arn:aws:s3:::opal-data-irpt/irpt/<firm>/state/analysis_commentaries/*` entries (print them), and changes or removes no other statement (print the R0 Sid list beside the planned Sid list). Anything else: STOP, nothing applied.
    4. A: `.tools/safe-apply.sh` on the saved plan; never `aws iam put-role-policy`.
    5. V: G1 `get-role-policy`: the Sid list equals the R0 list plus ReadTheAnalysisCommentaryDraft, and every other statement is byte-equal to R0's (compare per Sid). G2 the simulation on the run-6 commentary key: `s3:GetObject` = allowed (print the matched statement id), `s3:PutObject` = implicitDeny; and `s3:PutObject` on a run-6 `ycharts_opal_reports` key unchanged (allowed). G3 a second plan of the same target reads `No changes`.
    6. Write org/tier2_senior/0.7.0_AE_CloudOps~IB2/deliverables/irpt_anlreq_iamgrant/A_AFTER_IAMGRANT.txt with ONE line each, exactly: `R0 baseline implicitDeny get and put`, `C plan 0 to add 1 to change 0 to destroy`, `C policy diff adds exactly ReadTheAnalysisCommentaryDraft`, `G1 other statements byte-equal`, `G2 get allowed put implicitDeny on analysis_commentaries`, `G3 replan No changes`; then the R0 Sid list, the planned Sid list and the document sha256 before and after. A line that did not hold is written `<tag> FAIL <what was read>`. Close the ledger and report ONCE to 2.0.0_SA_COO~Y2 and 1.0.0_SA_CTO~DELL2: "iam grant closed" with the lines and the output path. Report the Terraform apply to 0.0.0_AB_MSTR~DELL2 after the fact. Remove every throwaway you made.
  </the_act>

  <bounds>
    One inline policy of one role, one statement added, read only. No Put, List or Delete grant, no other statement, no trust change, no bucket or key policy, no deploy of code. The commentary-ready queue is not touched. Rollback: the packet's section 5 (revert the Terraform commit, scoped plan 0/1/0, safe-apply).
  </bounds>

  <paths>
    org/tier2_senior/0.7.0_AE_CloudOps~IB2/deliverables/
    org/tier2_senior/0.7.0_AE_CloudOps~IB2/logs/
    org/critical_paths/change_management/
    org/critical_paths/.open_deploys/
  </paths>

  <proof_of_spec>
Instance at `org/tier2_senior/0.7.0_AE_CloudOps~IB2/deliverables/irpt_anlreq_iamgrant/IRPT_ANLREQ.TO-APPLY-IAMGRANT.resident-role-reads-the-analysis-commentary-draft-ib2.proof_of_spec.json`.
    <criterion id="IAMG-AC1" cell_refs="AR-y-447">The record holds the six lines, each as written (a FAIL line does not match).<invocation>grep -c -E '^(R0 baseline implicitDeny get and put|C plan 0 to add 1 to change 0 to destroy|C policy diff adds exactly ReadTheAnalysisCommentaryDraft|G1 other statements byte-equal|G2 get allowed put implicitDeny on analysis_commentaries|G3 replan No changes)$' org/tier2_senior/0.7.0_AE_CloudOps~IB2/deliverables/irpt_anlreq_iamgrant/A_AFTER_IAMGRANT.txt</invocation><expect>^6$</expect></criterion>
    <criterion id="IAMG-AC2" cell_refs="AR-y-447">The ledger irpt-resident-commentary-read-20261020 is CLOSED.<invocation>grep -m1 '^\*\*Status' org/critical_paths/change_management/*irpt-resident-commentary-read-20261020_deploy_completion.md</invocation><expect>^\*\*Status:\*\* CLOSED</expect></criterion>
  </proof_of_spec>
</task_order>
# pipeline-override: an APPLY order to a tier-2 applier under a signed pair (not a worker cell); the cell AR-y-447 is the issuer's, as for TO-APPLY-R37 and TO-APPLY-R34M.
