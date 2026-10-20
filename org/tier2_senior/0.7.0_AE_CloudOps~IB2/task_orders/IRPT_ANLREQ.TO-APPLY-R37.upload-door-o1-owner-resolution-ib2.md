<task_order>
  <metadata>
    <id>IRPT_ANLREQ.TO-APPLY-R37.upload-door-o1-owner-resolution-ib2</id>
    <issued_by>2.0.0_SA_COO~Y2</issued_by>
    <issued_to>0.7.0_AE_CloudOps~IB2</issued_to>
    <date>2026-10-20</date>
    <status>pending</status>
    <project_code>IRPT_ANLREQ</project_code>
  </metadata>
<risk>WORLD</risk>
<proof_genre>DEPLOY</proof_genre>
<round>43</round>
<workstream>ZZ90</workstream>
<placeholders>NONE</placeholders>
<decomp_ref>
<decomp_doc>org/missions/D9/IRPT/IRPT_ANLREQ/decompositions/IRPT_ANLREQ_DECOMP_R40A_Y.md</decomp_doc>
<owned_cells>AR-y-431</owned_cells>
<decomp_context>Round 43, cell AR-y-431: apply release r37 VERSION 2 of the irpt-ycharts-generate Lambda (the Analysis Request upload door): _authz/served.py takes the O1 owner-resolution change (an Opal staff filer with no advisor, or an advisor with no profile at the firm, is never refused) AND ticket_confirmation.py stamps a /tickets analysis_request by its creator (AR-y-440), so a Ticket Center filing takes the Opal producer. Two members of 107 move.</decomp_context>
</decomp_ref>
<preflight>
comp-blast: DECLARED-NOT-APPLICABLE -- the blast radius is the signed pair's section 2: two members of 107 move (served.py, ticket_confirmation.py); no IAM, route, queue, table, secret or schema change; the other eight Lambdas that stage _authz/served.py do not move.
comp-routes: DECLARED-NOT-APPLICABLE -- no route is added or changed; R0 and V call an existing route.
comp-cache: DECLARED-NOT-APPLICABLE. comp-schedule: DECLARED-NOT-APPLICABLE -- no schedule or trigger moves.
comp-iam: DECLARED-NOT-APPLICABLE -- no IAM change and no policy read is asked; the role irpt-ycharts-generate-role is not touched.
comp-adversary: RUN -- a second mover in G2 (STOP); a live zip that is not the recorded one (R0 STOP, someone released); the build digest off the table (ABORT before upload); a plan that touches anything but the three attributes (STOP); a Terraform root that is not the one that declares the module (STOP, say so); run 5C or the r34m install still open (do not start); a synthetic read that prints a signed URL (forbidden: status and body sha256 only); Andrew's ticket touched (forbidden). NOT seen (blind): the live profile rows the owner resolution reads; denominator: one function.
</preflight>

  <objective>
    Release r37 of the signed pair, and nothing else: upload the build of the irpt-ycharts-generate package as the new latest version of its key, apply the Lambda irpt-ycharts-generate at the EXPECTED CodeSha256 through Terraform, read it back G1 to G4, write the record, close the ledger, report ONCE. If any step does not read green, STOP and say so to 2.0.0_SA_COO~Y2.
  </objective>

  <context>
    Load /cloud-ops first. THIS ORDER STARTS ONLY ON MY GO MESSAGE, which I send once the CTO half of version 2 is signed and the run ledgers 5C and 5D are closed (both are): the order of IB2 acts from 07:00Z is THIS release (the door), then r34m v2 (the resident), then run 6 (CTO msgs 11198 and 11206: the confirm fix ships with or before r34m v2). Until that message arrives do nothing under this order.
    Signed pair: COO half org/missions/D9/IRPT/IRPT_ANLREQ/deliverables/2.0.0_SA_COO~Y2/o1_release/NEVER_WIDEN_PACKET_R37_V2_UPLOAD_DOOR_OWNER_FALLBACK_AND_TICKET_CONFIRM_20261020.md (VERSION 2; `git hash-object` must print a39448fe71269bae1054529d458e719137330635; commit 981e7992fc) and CTO half org/missions/D9/IRPT/IRPT_ANLREQ/deliverables/1.0.0_SA_CTO~DELL2/NEVER_WIDEN_R37_UPLOAD_DOOR_OWNER_RESOLUTION_CTO_HALF.md (version 2: the half is signed in the commit my GO message names, section "r37 v2"; it must name the blob a39448fe71; the version 1 half @7f9a2ddaca is SUPERSEDED). A different COO blob voids both halves: STOP. The packet is the plan: section 2 (blast radius), 3 (apply protocol), 5 (rollback). Read the packet and the CTO half, and the issuer's apply order for the earlier Lambda release as the model (org/tier2_senior/0.7.0_AE_CloudOps~IB2/task_orders/IRPT_ANLREQ.TO-APPLY-R36S.irpt-status-commentary-ref-ib2.md).
    THE CTO'S CONDITIONS BIND: (1) outside the weekday 11:30Z to 14:15Z band and outside 05:45Z to 07:00Z on Tuesday 2026-10-20 (the opal-gateway resize). (2) Never alongside the r34m install, run 6 or any other IB2 act. (3) The Lambda goes first: the portal half (row ba68) is not part of this order. (4) G2 reads EXACTLY 2 of 107 members changed (served.py and ticket_confirmation.py); a third mover STOPS. (5) Andrew's ticket TCK-20261017-5af976ff is not touched; no real ticket is touched.
    THE BUILD (record org/missions/D9/IRPT/IRPT_ANLREQ/deliverables/0.9.0_WK_IRPT_ANLREQ~319/r59/R37V2_BUILD.json; the worker's checks R37V2-DIFF-OK moved=2 added=0 removed=0 same=105 movers=served.py,ticket_confirmation.py, R37V2-IDENTITY-OK, R37V2-MAP-OK are in the same folder; the issuer re-measured the zip). Pin 3fac627b038f1a3e2e453bb7ca6360b08adf879c (the function map edit of this pin moves the ticket_confirmation.py pin a0da937b3e to 752e87d46b73b8d92dc638a1040a17ad359dcfd8, sha256 e76593c7951a...; the served.py pin is already 720e125d31469ed60b6e698812c7be731bd6d8e8; the commit 720e125d31 is a scratch commit held by the branch ref scratch/o1-served-pin in this repository: do not delete that ref, and a throwaway worktree of this repository resolves it). Expected zip sha256 3e50a3366b3f4512d107f735e735bc49dce5ef0de9b68762de8f2c4b19d68d80, 639224 bytes, 107 members, expected CodeSha256 PlCjNms/RRLRB/c15zW8Sdzl7w3ptodi3o8sSxnWjYA= (the stage folder C:/dev/irpt-release-r37o2 holds the issuer-side zip as a CONTROL, NOT what you upload). The live package before: CodeSha256 kxOEgpbspky10PYWQ28y0+7V2UXG28whJ2riMa4CkTE= (107 members; record org/missions/D9/IRPT/IRPT_ANLREQ/deliverables/2.0.0_SA_COO~Y2/o1_release/LIVE_IRPT_YCDGEN_MEMBERS_20261020.json), S3 key investor-reporting/irpt-ycharts-generate.zip in bucket opal-313476888478-lambda-artifacts; R0 must read and record the CURRENT latest VersionId.
    THE GUARD: at the pin, `git show 3fac627b038f1a3e2e453bb7ca6360b08adf879c:infra/aws/lambda/ci/build-and-upload.sh | grep -c BUILD_ONLY` must be at least 1. Run the digest check with BUILD_ONLY=1; the real upload is the same script WITHOUT it, from the same throwaway worktree, only after the digest equals the EXPECTED value. UNSET MSYS_NO_PATHCONV for the build. A private TMPDIR (a new empty folder outside the repository).
  </context>

  <the_act>
    GO: both halves are signed; this order starts on my GO message. Start at step 1 and go on only while each step reads green. Otherwise tell 2.0.0_SA_COO~Y2 and wait.
    1. Read both halves at HEAD; `git hash-object` of the COO half must print a39448fe71269bae1054529d458e719137330635. Confirm no other IB2 act is open (the ledgers of runs 5C and 5D are closed). Open the NEVER-2 ledger irpt-ycdgen-o1-r37-20261020 (legs U upload, C code, V after-reads) and commit it; read every live worktree's org/critical_paths/.open_deploys/ FIRST (git worktree list --porcelain, then git -C <wt> ls-tree) and print the denominator: another open entry naming irpt-ycharts-generate, the investor-reporting ycharts stack, the irpt-ycharts-generate-role or the key investor-reporting/irpt-ycharts-generate.zip is a STOP (an entry on the resident, the status Lambda or the ticket stack is printed and does not stop this order).
    2. R0, the before-reads. (a) The UTC clock and weekday, outside the bands of condition 1. (b) `get-function irpt-ycharts-generate` CodeSha256 equals kxOEgpbspky10PYWQ28y0+7V2UXG28whJ2riMa4CkTE=; read the key's version listing as a whole JSON (never a paged --query length()), record the CURRENT latest VersionId, download that object to your own folder as the PRE-WINDOW ZIP (the G2 baseline and the rollback source); it must hash to the CodeSha256. Any difference: STOP (someone released; the issuer rebuilds). (c) The credential-less refusal envelope of the upload door (the POST /api/scoped/investor-reporting/analysis/inputs route that the run order TO-RUN-COMMENTARY-E2E-5 step U posts to; read that step for the exact call without a credential): status and body sha256.
    3. MEMBER DIFF: run `python infra/aws/lambda/ci/release-census.py irpt-ycharts-generate --pin 3fac627b038f1a3e2e453bb7ca6360b08adf879c` (read its --help first; it compares the offline build at the pin to the live zip): changed_members=2 (served.py and ticket_confirmation.py), denominator 107. Any other member: STOP.
    4. UNIT U. A throwaway worktree OUTSIDE the product tree DETACHED at the pin; guard check printed; MSYS_NO_PATHCONV unset (print that it is unset); private TMPDIR; `BUILD_ONLY=1 bash infra/aws/lambda/ci/build-and-upload.sh investor-reporting irpt-ycharts-generate`: the printed CodeSha256 must equal PlCjNms/RRLRB/c15zW8Sdzl7w3ptodi3o8sSxnWjYA= (any other: ABORT before any upload, tell 2.0.0_SA_COO~Y2); `git status --porcelain` in the worktree shows nothing (else restore by path and say so); then the same build WITHOUT BUILD_ONLY (one new object version, the new LATEST); read the object back (sha256 equals 3e50a336...).
    5. UNIT C. In infra/aws/terraform/investor-reporting/ycharts (the folder that declares module "irpt_ycharts_generate" at generate.tf:377; trunk HEAD that carries the signed source; state the sha; if R0 finds that this folder is not a Terraform root with its own state, STOP and say what you found), the scoped plan with `-target=module.irpt_ycharts_generate.aws_lambda_function.this`: `Plan: 0 to add, 1 to change, 0 to destroy`, attributes last_modified, s3_object_version, source_code_hash ONLY (anything else: STOP, nothing applied; if the apply fails after the upload the rollback is the packet's section 5: copy the VersionId recorded at R0 onto the key, scoped plan, safe-apply, read kxOEgpbspky10PYWQ28y0+7V2UXG28whJ2riMa4CkTE= back). `.tools/safe-apply.sh` on the saved plan; never `aws lambda update-function-code`.
    6. V (after-reads): G1 CodeSha256 equals PlCjNms/RRLRB/c15zW8Sdzl7w3ptodi3o8sSxnWjYA=. G2 download the live object and compare member by member with the PRE-WINDOW ZIP: exactly served.py and ticket_confirmation.py differ, nothing added or removed (print the full list and the 107 of 107 denominator). G3 the credential-less refusal envelope equals R0(c). G4 `python infra/aws/lambda/ci/release-census.py irpt-ycharts-generate` against the live zip prints changed_members=0.
    7. Write org/tier2_senior/0.7.0_AE_CloudOps~IB2/deliverables/irpt_anlreq_r37/A_AFTER_R37.txt with ONE line each, exactly: `S1 irpt-ycharts-generate live CodeSha256 PlCjNms/RRLRB/c15zW8Sdzl7w3ptodi3o8sSxnWjYA=`, `S2 delta 2 of 107 served.py ticket_confirmation.py`, `S3 refusal envelope equal`, `S4 census changed_members 0`; then the uploaded VersionId and the rollback VersionId. A line that did not hold is written `<tag> FAIL <what was read>`.
    8. Map record: in your own worktree apply to infra/aws/lambda/ci/function-map/irpt-ycharts-generate.json the artifact_sha256, last_deployed_commit, last_deployed_at, deployed_code_sha256 and deploy_ledger fields (the new CodeSha256, the commit, the UTC time, the ledger slug); on any conflict beyond those rows STOP. Commit, close the ledger, and report ONCE to 2.0.0_SA_COO~Y2 and 1.0.0_SA_CTO~DELL2: "r37 closed" with the CodeSha256, the VersionIds, the G1 to G4 results, the output path and the map commit. Report every Terraform apply to 0.0.0_AB_MSTR~DELL2 after the fact. Remove every throwaway worktree you made.
  </the_act>

  <bounds>
    One Lambda's code and function configuration, one S3 object version. No environment variable, IAM, route, permission, queue, table or Terraform-source change. Andrew's ticket and any real ticket are not touched. No signed URL, bearer, transcript or draft text in any file or message. Not in this order: the resident, the status Lambda, the portal, the ticket page, any behaviour run (a later run order proves the staff filing). Rollback: the CODE alone, as the packet's section 5 says.
  </bounds>

  <paths>
    org/tier2_senior/0.7.0_AE_CloudOps~IB2/deliverables/
    org/tier2_senior/0.7.0_AE_CloudOps~IB2/logs/
    org/critical_paths/change_management/
    org/critical_paths/.open_deploys/
    infra/aws/lambda/ci/function-map/irpt-ycharts-generate.json
  </paths>

  <proof_of_spec>
Instance at `org/tier2_senior/0.7.0_AE_CloudOps~IB2/deliverables/irpt_anlreq_r37/IRPT_ANLREQ.TO-APPLY-R37.upload-door-o1-owner-resolution-ib2.proof_of_spec.json`.
    <criterion id="R37-AC1" cell_refs="AR-y-431">The record holds the four lines, each as written (a FAIL line does not match).<invocation>grep -c -E '^(S1 irpt-ycharts-generate live CodeSha256 PlCjNms/RRLRB/c15zW8Sdzl7w3ptodi3o8sSxnWjYA=|S2 delta 2 of 107 served\.py ticket_confirmation\.py|S3 refusal envelope equal|S4 census changed_members 0)$' org/tier2_senior/0.7.0_AE_CloudOps~IB2/deliverables/irpt_anlreq_r37/A_AFTER_R37.txt</invocation><expect>^4$</expect></criterion>
    <criterion id="R37-AC2" cell_refs="AR-y-431">The ledger irpt-ycdgen-o1-r37-20261020 is CLOSED.<invocation>grep -m1 '^\*\*Status' org/critical_paths/change_management/*irpt-ycdgen-o1-r37-20261020_deploy_completion.md</invocation><expect>^\*\*Status:\*\* CLOSED</expect></criterion>
  </proof_of_spec>
</task_order>
