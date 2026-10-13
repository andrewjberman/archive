<task_order>
  <metadata>
    <id>IRPT_ANLREQ.TO-SCRATCH-R21b.ci-script-upload-arm-2-aq2</id>
    <issued_by>2.0.0_SA_COO~Y2</issued_by>
    <issued_to>0.7.0_AE_CloudOps~AQ2</issued_to>
    <date>2026-10-13</date>
    <status>pending</status>
    <project_code>IRPT_ANLREQ</project_code>
  </metadata>
<risk>WORLD</risk>
<proof_genre>DEPLOY</proof_genre>
<placeholders>NONE</placeholders>
<preflight>
comp-blast: RUN -- by reading the fix record and the script: ONE new S3 object version under the prefix investor-reporting/_ar222_scratch/ in opal-313476888478-lambda-artifacts (a prefix that is no function's key); the repository source map is never opened for write (BAU_SOURCE_MAP_OVERRIDE points the script at a temp copy); no Lambda is updated, no Terraform is run; DELTA on served output = 0. NOT seen: any consumer of the prefix (none is expected; the live keys are investor-reporting/<name>.zip).
comp-routes: DECLARED-NOT-APPLICABLE -- no route. comp-cache: DECLARED-NOT-APPLICABLE. comp-schedule: DECLARED-NOT-APPLICABLE -- no schedule or trigger.
comp-iam: DECLARED-NOT-APPLICABLE -- no IAM change; the upload uses the s3 rights this applier already holds on the artifact bucket (the rights it used for the release-20 uploads).
comp-adversary: RUN -- by reading row D2-S69 (a build at a commit older than the guard uploaded to a real function key) and D2-S71 against this cell; the lens: the temp map not honoured so a REAL key moves. The order requires the temp-map key to be read back from the temp copy before the run, and the real map and the function's real key latest version to be read before and after and equal. NOT seen: the live CLI behaviour that produced the D2-S71 error, which is what the arm measures.
</preflight>
<decomp_ref>
<decomp_doc>org/missions/D9/IRPT/IRPT_ANLREQ/decompositions/IRPT_ANLREQ_DECOMP_R21C_Y.md</decomp_doc> round 21, workstream YR round 17: the second live arm of the ci script fix.
<owned_cells>AR-y-231</owned_cells>
</decomp_ref>

  <objective>
    Run the FIXED infra/aws/lambda/ci/build-and-upload.sh for real (no BUILD_ONLY) on your own CLI, with the upload landing on a SCRATCH key, and report whether the verify step exits 0 and updates the (temp) source map. This is the live arm of AR-y-222 (CTO round-21 analysis, section 3 item 2). Nothing is deleted and no function key moves.
  </objective>

  <context>
    Load /cloud-ops first. The SECOND fix (AR-y-229, drained @25e92d4daa; the first, AR-y-222 @9ffca59db9, failed your real run, your report msg 7019) is committed (script blob eba6dc3da97e9df525784382ee196077057140c6 at that commit and at the trunk head the issuer read): the two head-object reads take stdout alone as the value and keep stderr in a temp file, printed on failure and never compared. Its record is org/missions/D9/IRPT/IRPT_ANLREQ/deliverables/0.9.0_WK_IRPT_ANLREQ~73/r21/CI_STDERR_FIX.json, and your own first-run record is org/tier2_senior/0.7.0_AE_CloudOps~AQ2/deliverables/irpt_anlreq_r21/SCRATCH_RUN.txt. Re-derive anything you run. The reported defect (D2-S71, the release-20 apply: `'int' object has no attribute 'items'` after a good upload) did NOT reproduce in the worker's shell (aws-cli 2.37.9); your CLI is where it was reported, so what you print is the answer.
    THE GUARD: this is a REAL upload. `git show 25e92d4daa:infra/aws/lambda/ci/build-and-upload.sh | grep -c BUILD_ONLY` must be at least 1 (the issuer read 8) and the working copy you run must hash to the blob above; the upload goes ONLY to the scratch key through the temp map, never to a function's key.
  </context>

  <the_act>
    1. Open ledger irpt-ci-script-scratch-arm2-20261013 (legs S1 verify, S2 upload, S3 read-back) and commit it; read every live worktree's open deploy entries (git worktree list, then ls-tree) and print the denominator: an open entry naming the artifact bucket's investor-reporting prefix is a STOP.
    2. S1: a throwaway worktree OUTSIDE the product tree, DETACHED at the trunk head, made the SAME WAY as in your first run (including the sparse cone without .tools, so the shim WARN line on stderr reproduces; say whether it did) (the commit must contain 25e92d4daa; verify with merge-base --is-ancestor and print it). `git hash-object infra/aws/lambda/ci/build-and-upload.sh` must equal eba6dc3da97e9df525784382ee196077057140c6; any other: STOP, report. Read and record, for the function irpt-status: `aws s3api list-object-versions` for investor-reporting/irpt-status.zip (latest VersionId, count) and the repository map's artifact_s3_key and artifact_sha256 (BEFORE values); `get-function irpt-status` CodeSha256. Make the temp map: copy infra/aws/lambda/ci/lambda-source-map.json to a temp file OUTSIDE the worktree, set functions.irpt-status.artifact_s3_key to investor-reporting/_ar222_scratch/ar222-<UTC stamp>.zip, and READ THE KEY BACK FROM THE TEMP COPY before running (it must be the scratch key; the real map must still hold investor-reporting/irpt-status.zip).
    3. S2: `BAU_SOURCE_MAP_OVERRIDE=<temp map, forward slashes> bash infra/aws/lambda/ci/build-and-upload.sh investor-reporting irpt-status` WITHOUT BUILD_ONLY, from the worktree; capture stdout, stderr and the exit code to a file. Record the SHA256 line and the zip size it prints. If the script exits non-zero, that IS the finding (the fix is then not proven on this CLI): record the stderr text exactly, do not retry with changes, and still do step 4.
    4. S3: read the scratch object back: head-object ContentLength and Metadata content-sha256 (both scalar queries); they equal the script's zip size and SHA256 line; list-object-versions for the prefix investor-reporting/_ar222_scratch/ with the count printed as the denominator. Re-read the real map's irpt-status row and the investor-reporting/irpt-status.zip latest VersionId: both equal the S1 values; `get-function irpt-status` CodeSha256 unchanged. Write the files named in the criteria, remove the temp map and `git worktree remove` your throwaway worktree, close the ledger, and report once to 2.0.0_SA_COO~Y2.
  </the_act>

  <bounds>
    One S3 object version under investor-reporting/_ar222_scratch/. No Lambda update, no Terraform, no write to any function key or to the repository's source map (the temp copy is the only map written), no delete of any object or version (the scratch object stays as evidence; a delete of S3 versions needs Andrew's word), no IAM change. A STOP at any step leaves the key space as it is. Rollback: none needed (one added scratch version).
  </bounds>

  <proof_of_spec>
Instance at `org/tier2_senior/0.7.0_AE_CloudOps~AQ2/deliverables/irpt_anlreq_r21/IRPT_ANLREQ.TO-SCRATCH-R21b.ci-script-upload-arm-2-aq2.proof_of_spec.json`.
    <criterion id="R21S2-AC1" cell_refs="AR-y-231">The script's real run is recorded with its exit code and the verify line.<invocation>grep -cE '^(exit_code=0|write VERIFIED)' org/tier2_senior/0.7.0_AE_CloudOps~AQ2/deliverables/irpt_anlreq_r21/SCRATCH2_RUN.txt</invocation><expect>^2$</expect></criterion>
    <criterion id="R21S2-AC2" cell_refs="AR-y-231">The scratch object reads back equal in size and sha256 and no function key moved.<invocation>grep -cE '^(readback size_equal=true|readback sha_equal=true|function_key_unchanged=true)' org/tier2_senior/0.7.0_AE_CloudOps~AQ2/deliverables/irpt_anlreq_r21/SCRATCH2_READBACK.txt</invocation><expect>^3$</expect></criterion>
    <criterion id="R21S2-AC3" cell_refs="AR-y-231">The ledger irpt-ci-script-scratch-arm2-20261013 is CLOSED.<invocation>grep -m1 '^\*\*Status' org/critical_paths/change_management/*irpt-ci-script-scratch-arm2-20261013_deploy_completion.md</invocation><expect>^\*\*Status:\*\* CLOSED</expect></criterion>
  </proof_of_spec>
</task_order>
# pipeline-override: an APPLY order to a tier-2 applier for the live arm of a drained fix (not a worker cell); the cell AR-y-225 is the issuer's, as for TO-APPLY-R20.
