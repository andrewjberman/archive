<task_order>
  <metadata>
    <id>IRPT_ANLREQ.TO-APPLY-R37.irpt-status-two-pdf-routes-ib2</id>
    <issued_by>2.0.0_SA_COO~Y2</issued_by>
    <issued_to>0.7.0_AE_CloudOps~IB2</issued_to>
    <date>2026-10-20</date>
    <status>complete</status><!-- flipped by issuer 2.0.0_SA_COO~Y2 2026-10-21 (round hygiene): every criterion invocation re-run by the issuer and matched; the proof instance reads VALID rc 0 -->
    <project_code>IRPT_ANLREQ</project_code>
  </metadata>
<risk>WORLD</risk>
<proof_genre>DEPLOY</proof_genre>
<round>43</round>
<workstream>ZZ134</workstream>
<placeholders>NONE</placeholders>
<decomp_ref>
<decomp_doc>org/missions/D9/IRPT/IRPT_ANLREQ/decompositions/IRPT_ANLREQ_DECOMP_R40A_Y.md</decomp_doc>
<owned_cells>AR-y-475</owned_cells>
<decomp_context>Round 43, cell AR-y-475: release r37 of the irpt-status Lambda (owned_report.py: the commentary route binds by logical id and signs the PDF's own sha256; the Overview route resolves the retained Opal PDF through the artifact binding) so the two report PDFs open from a ticket.</decomp_context>
</decomp_ref>
<preflight>
comp-blast: DECLARED-NOT-APPLICABLE -- the blast radius is the signed pair's section 2: one member of 49 moves (owned_report.py); no IAM, route, queue, table, secret or schema change.
comp-routes: DECLARED-NOT-APPLICABLE -- no route is added or changed; R0 and V call existing routes.
comp-cache: DECLARED-NOT-APPLICABLE. comp-schedule: DECLARED-NOT-APPLICABLE -- no schedule or trigger moves.
comp-iam: DECLARED-NOT-APPLICABLE -- no IAM change; the role's read of the Opal report family was applied earlier (ledger irpt-status-opal-report-read-20261020, CLOSED).
comp-adversary: RUN -- a second mover in the member diff (STOP); a live zip that is not the recorded one (R0 STOP, someone released); the build digest off the table (ABORT before upload); a plan that touches anything but the three attributes (STOP); `terraform fmt` or a gate red (STOP and tell me); a synthetic read that prints a signed URL (forbidden: status and body sha256 only); another IB2 act open, in particular the resident release of 2.0.0_SA_COO~G2 (do not start); Andrew's ticket touched (forbidden).
</preflight>

  <objective>
    Release r37 of the signed pair, and nothing else: upload the build of the irpt-status package as the new latest version of its key, apply the Lambda irpt-status at the EXPECTED CodeSha256 through Terraform, read it back G1 to G6, write the record, close the ledger, report ONCE. If any step does not read green, STOP and say so to 2.0.0_SA_COO~Y2. THIS ORDER STARTS ONLY ON MY GO MESSAGE (the CTO half must be signed and named there). Andrew is waiting on run 7d, which follows this order: work straight through, but never weaken a check.
  </objective>

  <context>
    Load /cloud-ops first. Signed pair: COO half org/missions/D9/IRPT/IRPT_ANLREQ/deliverables/2.0.0_SA_COO~Y2/irpt_status_release/NEVER_WIDEN_PACKET_R37_STATUS_TWO_PDF_ROUTES_20261020.md (`git hash-object` must print f0a152fd55f44e83b93fa0f4bb0f35c306846ddf; commit c54998e269) and the CTO half named in my GO (it must name that blob). A different COO blob voids both halves: STOP. The packet is the plan: sections 2 (blast radius), 3 (apply protocol), 4 (rollback). Model: the earlier order for the same function, org/tier2_senior/0.7.0_AE_CloudOps~IB2/task_orders/IRPT_ANLREQ.TO-APPLY-R36S.irpt-status-commentary-ref-ib2.md (read its steps 2 to 8; the commands are the same, the expected values below replace its).
    THE BUILD (record org/missions/D9/IRPT/IRPT_ANLREQ/deliverables/0.9.0_WK_IRPT_ANLREQ~348/r51/R37_BUILD.json; the issuer's check `python -I org/missions/D9/IRPT/IRPT_ANLREQ/deliverables/0.9.0_WK_IRPT_ANLREQ~348/r51/live_diff.py org/missions/D9/IRPT/IRPT_ANLREQ/deliverables/0.9.0_WK_IRPT_ANLREQ~348/r51/R37_BUILD.json org/missions/D9/IRPT/IRPT_ANLREQ/deliverables/2.0.0_SA_COO~Y2/irpt_status_release/LIVE_IRPT_STATUS_MEMBERS_20261020.json` printed LIVE-DIFF-OK moved=1 added=0 removed=0 same=48 mover=owned_report.py). Pin 474f174e89407c62cec422870cb63cb47eff2e43 (trunk, box/dell2; no map edit). Expected zip sha256 078474759a814617259902ce8811e9dc5b7fc0d6cca263598547e508245f1321, 369411 bytes, 49 members, expected CodeSha256 B4R0dZqBRhclmQLOiBHp3Ft/wNbMomNZhUflCCRfEyE= (the stage folder C:/dev/irpt-release-r37 holds the worker's zip as a CONTROL, NOT what you upload). The live package before: CodeSha256 274dl2bCd2VC3OcX4Uqc4AMbWep65B97F1+CVNoKfMc= (LastModified 2026-10-17T16:41:08Z, 368788 bytes), S3 key investor-reporting/irpt-status.zip in bucket opal-313476888478-lambda-artifacts; R0 must read and record the CURRENT latest VersionId.
    THE GUARD: at the pin, `git show 474f174e89407c62cec422870cb63cb47eff2e43:infra/aws/lambda/ci/build-and-upload.sh | grep -c BUILD_ONLY` must be at least 1. Run the digest check with BUILD_ONLY=1; the real upload is the same script WITHOUT it, from the same throwaway worktree, only after the digest equals the EXPECTED value. UNSET MSYS_NO_PATHCONV for the build. A private TMPDIR (a new empty folder outside the repository).
  </context>

  <the_act>
    GO: both halves are signed AND my GO message names the CTO half's commit. Start at step 1 and go on only while each step reads green. Otherwise tell 2.0.0_SA_COO~Y2 and wait.
    1. Read both halves at HEAD; `git hash-object` of the COO half must print f0a152fd55f44e83b93fa0f4bb0f35c306846ddf. Open the NEVER-2 ledger irpt-status-r37-20261020 (legs U upload, C code, V after-reads) and commit it; read every live worktree's org/critical_paths/.open_deploys/ FIRST (git worktree list --porcelain, then git -C <wt> ls-tree) and print the denominator: another open entry naming irpt-status, the investor-reporting ops stack, the irpt-status role or the key investor-reporting/irpt-status.zip is a STOP (an entry on the resident, the commentary draft store or the ticket stack is printed and does not stop this order).
    2. R0, the before-reads: (a) `get-function irpt-status` CodeSha256 equals 274dl2bCd2VC3OcX4Uqc4AMbWep65B97F1+CVNoKfMc=; read the key's version listing as a whole JSON (never a paged --query length()), record the CURRENT latest VersionId, download that object to your own folder as the PRE-WINDOW ZIP (the G2 baseline and the rollback source); it must hash to the CodeSha256. Any difference: STOP. (b) The credential-less refusal envelope of the status route: status and body sha256. (c) ONE retained READY report read as a synthetic internal viewer if one can be minted by the method of TO-EXERCISE-R28b (every minted row removed after its exp and read ABSENT), else `NOT MADE <why>`: status and body sha256. (d) G5 SUBJECT: look for ONE synthetic request whose item carries a retained artifact the routes could open; if none (expected: the earlier runs' rows were deleted), G5 is NOT MADE and is reported so.
    3. MEMBER DIFF: `python infra/aws/lambda/ci/release-census.py irpt-status --pin 474f174e89407c62cec422870cb63cb47eff2e43` (read its --help first): changed_members=1 (owned_report.py), denominator 49. Any other member: STOP.
    4. UNIT U. A throwaway worktree OUTSIDE the product tree DETACHED at the pin; guard check printed; MSYS_NO_PATHCONV unset (print that it is unset); private TMPDIR; `BUILD_ONLY=1 bash infra/aws/lambda/ci/build-and-upload.sh investor-reporting irpt-status`: the printed CodeSha256 must equal B4R0dZqBRhclmQLOiBHp3Ft/wNbMomNZhUflCCRfEyE= (any other: ABORT before any upload, tell 2.0.0_SA_COO~Y2); `git status --porcelain` in the worktree shows nothing; then the same build WITHOUT BUILD_ONLY (one new object version, the new LATEST); read the object back (sha256 equals 078474759a81...).
    5. UNIT C. In infra/aws/terraform/investor-reporting/ops (trunk HEAD that carries the signed source; state the sha), `terraform fmt -check` on the files the root holds (rc 0, else STOP and tell me), then the scoped plan with `-target=module.irpt_status.aws_lambda_function.this`: `Plan: 0 to add, 1 to change, 0 to destroy`, attributes last_modified, s3_object_version, source_code_hash ONLY (anything else: STOP, nothing applied; if the apply fails after the upload the rollback is the packet's section 4: copy the VersionId recorded at R0 onto the key, scoped plan, safe-apply, read 274dl2bCd2VC3OcX4Uqc4AMbWep65B97F1+CVNoKfMc= back). `.tools/safe-apply.sh` on the saved plan; never `aws lambda update-function-code`.
    6. V (after-reads): G1 CodeSha256 equals B4R0dZqBRhclmQLOiBHp3Ft/wNbMomNZhUflCCRfEyE=. G2 download the live object and compare member by member with the PRE-WINDOW ZIP: exactly owned_report.py differs, nothing added or removed (print the full list and the 49 of 49 denominator). G3 the credential-less refusal envelope equals R0(b). G4 the READY report read of R0(c), if made, returns the same status and a BYTE-IDENTICAL body (sha256 equal). G5 per R0(d): made or `NOT MADE <why>`. G6 `python infra/aws/lambda/ci/release-census.py irpt-status` against the live zip prints changed_members=0.
    7. Write org/tier2_senior/0.7.0_AE_CloudOps~IB2/deliverables/irpt_anlreq_r37/A_AFTER_R37.txt with ONE line each, exactly: `S1 irpt-status live CodeSha256 B4R0dZqBRhclmQLOiBHp3Ft/wNbMomNZhUflCCRfEyE=`, `S2 delta 1 of 49 owned_report.py`, `S3 refusal envelope equal`, `S4 ready report read byte-identical` (or `S4 NOT MADE <why>`), `S5 PDF routes read NOT MADE <why>` (or the made line), `S6 census changed_members 0`; then the uploaded VersionId and the rollback VersionId. A line that did not hold is written `<tag> FAIL <what was read>`. Close the ledger and report ONCE to 2.0.0_SA_COO~Y2 and 1.0.0_SA_CTO~DELL2: "r37 closed" with the CodeSha256, the VersionIds, the G1 to G6 results, the output path. Report the Terraform apply to 0.0.0_AB_MSTR~DELL2 after the fact. Remove every throwaway worktree you made.
  </the_act>

  <bounds>
    One Lambda's code and function configuration, one S3 object version. No environment variable, IAM, route, permission, queue, table or Terraform-source change. Synthetic viewer rows are removed after exp. Andrew's ticket and any real ticket are not touched. No signed URL, bearer, transcript or draft text in any file or message. Not in this order: the resident, the commentary draft store, the portal, the ticket page. Rollback: the CODE alone, as the packet's section 4 says.
  </bounds>

  <paths>
    org/tier2_senior/0.7.0_AE_CloudOps~IB2/deliverables/
    org/tier2_senior/0.7.0_AE_CloudOps~IB2/logs/
    org/critical_paths/change_management/
    org/critical_paths/.open_deploys/
    infra/aws/lambda/ci/function-map/irpt-status.json
  </paths>

  <proof_of_spec>
Instance at `org/tier2_senior/0.7.0_AE_CloudOps~IB2/deliverables/irpt_anlreq_r37/IRPT_ANLREQ.TO-APPLY-R37.irpt-status-two-pdf-routes-ib2.proof_of_spec.json`.
    <criterion id="R37-AC1" cell_refs="AR-y-475">The record holds the six lines, each as written (a FAIL line does not match; NOT MADE lines are admitted for S4 and S5 only).<invocation>grep -c -E '^(S1 irpt-status live CodeSha256 B4R0dZqBRhclmQLOiBHp3Ft/wNbMomNZhUflCCRfEyE=|S2 delta 1 of 49 owned_report.py|S3 refusal envelope equal|S4 (ready report read byte-identical|NOT MADE .+)|S5 (PDF routes read NOT MADE .+|PDF routes read .+)|S6 census changed_members 0)$' org/tier2_senior/0.7.0_AE_CloudOps~IB2/deliverables/irpt_anlreq_r37/A_AFTER_R37.txt</invocation><expect>^6$</expect></criterion>
    <criterion id="R37-AC2" cell_refs="AR-y-475">The ledger irpt-status-r37-20261020 is CLOSED.<invocation>grep -m1 '^\*\*Status' org/critical_paths/change_management/*irpt-status-r37-20261020_deploy_completion.md</invocation><expect>^\*\*Status:\*\* CLOSED</expect></criterion>
  </proof_of_spec>
</task_order>
# pipeline-override: an APPLY order to a tier-2 applier under a signed pair (not a worker cell); the cell AR-y-475 is the issuer's, as for TO-APPLY-R36S.
