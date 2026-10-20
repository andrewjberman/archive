<task_order>
  <metadata>
    <id>IRPT_ANLREQ.TO-APPLY-MODELGRANT.resident-role-reads-the-model-series-and-positioning-ib2</id>
    <issued_by>2.0.0_SA_COO~G2</issued_by>
    <issued_to>0.7.0_AE_CloudOps~IB2</issued_to>
    <date>2026-10-20</date>
    <status>pending</status>
    <project_code>IRPT_ANLREQ</project_code>
  </metadata>
<risk>WORLD</risk>
<proof_genre>DEPLOY</proof_genre>
<round>60</round>
<workstream>~G</workstream>
<placeholders>NONE</placeholders>
<decomp_ref>
<decomp_doc>org/missions/D9/IRPT/IRPT_ANLREQ/decompositions/IRPT_ANLREQ_DECOMP_R60_G.md</decomp_doc>
<owned_cells>AR-g-172</owned_cells>
<decomp_context>Round 60, cell AR-g-172: apply the one-statement IAM grant (s3:GetObject on the two exact keys json/benchmarks/model_portfolio_timeseries.json and json/positioning/positioning_data.json of opal-data-portal-v2) to the inline policy of the resident host's role irpt-ycharts-runner-role, so FWD-10's comparison section can read the Opal model return series and the models' current positioning. The Terraform edit is merged (cell AR-g-172, pin 50f7c709af2).</decomp_context>
</decomp_ref>
<preflight>
comp-blast: DECLARED-NOT-APPLICABLE -- the blast radius is the signed pair's section 3: one inline-policy statement, read only, on one role, for two firm-neutral objects; one Terraform local; no other statement, trust, bucket policy, key policy, Lambda, queue or table changes.
comp-routes: DECLARED-NOT-APPLICABLE -- no route. comp-cache: DECLARED-NOT-APPLICABLE -- no cache.
comp-schedule: DECLARED-NOT-APPLICABLE -- no schedule or trigger.
comp-iam: RUN -- this order IS an IAM change: ONE statement added to aws_iam_role_policy.runner_resident through Terraform (scoped plan 0/1/0, safe-apply); before and after reads of the policy document and policy simulations on the two keys.
comp-adversary: RUN -- a plan that touches anything but the one policy (STOP); a policy diff that adds or changes more than the one statement (STOP, nothing applied); a Put/List/Delete/Version action or a wildcard in the statement (the pin's checks say none; read the plan, not the claim); an apply from a Terraform root that is not the one that declares the resource (STOP, say so); another IB2 act open on the resident role or the ycharts stack, or run 7c's window open (do not start: never two acts at once on the resident role, CTO msg 11463). NOT seen (blind): the live policy until R0; denominator: one role policy.
</preflight>

  <objective>
    Apply the one-statement IAM grant of the signed pair and nothing else: read the live policy, plan with the resident.tf of the pin, prove the plan adds exactly the one statement, apply it with safe-apply, read it back, prove by simulation that the role may now GET (not PUT) the two keys and nothing else of the bucket, read both objects with the host role, close the ledger, report ONCE. If any step does not read green, STOP and say so to 2.0.0_SA_COO~G2. THIS ORDER STARTS ONLY ON MY GO MESSAGE, and only outside run 7c's window.
  </objective>

  <context>
    Load /cloud-ops first. Signed pair: COO half org/missions/D9/IRPT/IRPT_ANLREQ/deliverables/2.0.0_SA_COO~G2/NEVER_WIDEN_PACKET_RESIDENT_ROLE_READS_MODEL_SOURCE_20261020.md (`git hash-object` must print 0834df2dd40fbcbaabfea46a3bbcefdbf7d4c937; sha256 a5200ee7915ab2bb8628995f0cb0ac345b09aabe665039b42ab8e587915b3a4f; commit a03a57da11) and the CTO half org/missions/D9/IRPT/IRPT_ANLREQ/deliverables/1.0.0_SA_CTO~DELL2/NEVER_WIDEN_RESIDENT_ROLE_READS_MODEL_SOURCE_CTO_HALF.md (signed in commit a08bb1c202, CTO msg 11463; it names the COO blob above). A different COO blob voids both halves: STOP. The packet is the plan: section 3 (blast radius), section 4 (the order of the legs), section 5 (rollback). The pin is commit 50f7c709af2 (the Terraform edit alone, merged at e408831dd8f): infra/aws/terraform/investor-reporting/ycharts/resident.tf, 16 insertions and 0 deletions: a local model_source_bucket and ONE statement ReadTheModelReturnSeriesAndPositioning (Allow, s3:GetObject, two exact object ARNs of opal-data-portal-v2). The precedent order, in the same stack and role, is your TO-APPLY-IAMGRANT (ledger irpt-resident-commentary-read-20261020): follow its legs. The two objects (measured by the issuer, read-only): both ServerSideEncryption AES256 (no KMS grant is needed), the bucket policy has no Deny; the positioning object is gzip, so a body that starts 0x1f 0x8b is expected.
  </context>

  <the_act>
    GO: both halves are signed AND my GO message names the CTO half's commit. Start at step 1 and go on only while each step reads green. Otherwise tell 2.0.0_SA_COO~G2 and wait.
    1. Read both halves at HEAD; `git hash-object` of the COO half must print 0834df2dd40fbcbaabfea46a3bbcefdbf7d4c937. Open the NEVER-2 ledger irpt-resident-model-source-read-20261020 (legs R0 before-reads, C plan, A apply, V after-reads) and commit it; read every live worktree's org/critical_paths/.open_deploys/ FIRST (git worktree list --porcelain, then git -C <wt> ls-tree) and print the denominator: another open entry naming the ycharts Terraform stack, the role irpt-ycharts-runner-role or its policy is a STOP, and so is run 7c's window being open.
    2. R0: `aws iam get-role-policy --role-name irpt-ycharts-runner-role --policy-name irpt-ycharts-runner-resident-policy`: record the statement ids (Sid list) and the sha256 of the canonical (key-sorted, compact) JSON of the document; `aws iam simulate-principal-policy` for the role on `s3:GetObject` against each of the two keys and against a third key of the bucket (json/benchmarks/other.json), and on `s3:PutObject` against the first key: all four must read implicitDeny (the baseline). Any other state (the Sid already present, or an allow): STOP.
    3. C: in a throwaway worktree detached at the pin (outside the product tree; your usual way for the Terraform stacks), `terraform fmt -check resident.tf` in the root folder (rc 0, else STOP), `terraform init` as the stack does, then the saved scoped plan `-target=aws_iam_role_policy.runner_resident`: `Plan: 0 to add, 1 to change, 0 to destroy`, the only changed attribute `policy`, and the policy document diff adds exactly ONE statement with `Sid` ReadTheModelReturnSeriesAndPositioning, Effect Allow, Action exactly `s3:GetObject`, Resource exactly the two ARNs `arn:aws:s3:::opal-data-portal-v2/json/benchmarks/model_portfolio_timeseries.json` and `arn:aws:s3:::opal-data-portal-v2/json/positioning/positioning_data.json`. Anything else in the plan, or any other changed resource: STOP, nothing applied.
    4. A: `.tools/safe-apply.sh` on the saved plan; never `aws iam put-role-policy`.
    5. V: G1 `get-role-policy`: the Sid list equals the R0 list plus ReadTheModelReturnSeriesAndPositioning, and every other statement is byte-equal to R0's (compare per Sid). G2 the simulation: `s3:GetObject` on each of the two keys = allowed (print the matched statement id); `s3:PutObject` on the first key and `s3:GetObject` on the third key = implicitDeny. G3 a second plan of the same target reads `No changes`. G4 a real get-object of each key with the host role's credentials (your probe style, in the service's environment): HTTP 200; the series body parses as JSON; the positioning body starts with the gzip magic bytes 0x1f 0x8b and decompresses to JSON.
    6. Write org/tier2_senior/0.7.0_AE_CloudOps~IB2/deliverables/irpt_anlreq_modelgrant/A_AFTER_MODELGRANT.txt with ONE line each, exactly: `R0 baseline implicitDeny on all four`, `C plan 0 to add 1 to change 0 to destroy`, `C policy diff adds exactly ReadTheModelReturnSeriesAndPositioning`, `G1 other statements byte-equal`, `G2 get allowed on two keys put and third key implicitDeny`, `G3 replan No changes`, `G4 both objects read with the host role`; then the R0 Sid list, the planned Sid list and the document sha256 before and after. A line that did not hold is written `<tag> FAIL <what was read>`. Close the ledger and report ONCE to 2.0.0_SA_COO~G2, 2.0.0_SA_COO~Y2 and 1.0.0_SA_CTO~DELL2.
  </the_act>

  <bounds>
    One inline policy of one role, one statement added, read only, two exact object keys. No Put, List, Delete or version grant, no wildcard, no other statement, no trust change, no bucket or key policy, no deploy of code, no change to any object of the bucket. The commentary-ready queue is not touched. Rollback: the packet's section 5 (revert the Terraform commit, scoped plan 0/1/0, safe-apply).
  </bounds>

  <paths>
    org/tier2_senior/0.7.0_AE_CloudOps~IB2/deliverables/
    org/tier2_senior/0.7.0_AE_CloudOps~IB2/logs/
    org/critical_paths/change_management/
    org/critical_paths/.open_deploys/
  </paths>

  <proof_of_spec>
Instance at `org/tier2_senior/0.7.0_AE_CloudOps~IB2/deliverables/irpt_anlreq_modelgrant/IRPT_ANLREQ.TO-APPLY-MODELGRANT.resident-role-reads-the-model-series-and-positioning-ib2.proof_of_spec.json`.
    <criterion id="MODG-AC1" cell_refs="AR-g-172">The record holds the seven lines, each as written (a FAIL line does not match).<invocation>grep -c -E '^(R0 baseline implicitDeny on all four|C plan 0 to add 1 to change 0 to destroy|C policy diff adds exactly ReadTheModelReturnSeriesAndPositioning|G1 other statements byte-equal|G2 get allowed on two keys put and third key implicitDeny|G3 replan No changes|G4 both objects read with the host role)$' org/tier2_senior/0.7.0_AE_CloudOps~IB2/deliverables/irpt_anlreq_modelgrant/A_AFTER_MODELGRANT.txt</invocation><expect>^7$</expect></criterion>
    <criterion id="MODG-AC2" cell_refs="AR-g-172">The ledger irpt-resident-model-source-read-20261020 is CLOSED.<invocation>grep -m1 '^\*\*Status' org/critical_paths/change_management/*irpt-resident-model-source-read-20261020_deploy_completion.md</invocation><expect>^\*\*Status:\*\* CLOSED</expect></criterion>
  </proof_of_spec>
</task_order>
# pipeline-override: an APPLY order to a tier-2 applier under a signed pair (not a worker cell); the cell AR-g-172 is the issuer's, as for TO-APPLY-IAMGRANT and TO-APPLY-R34J.
