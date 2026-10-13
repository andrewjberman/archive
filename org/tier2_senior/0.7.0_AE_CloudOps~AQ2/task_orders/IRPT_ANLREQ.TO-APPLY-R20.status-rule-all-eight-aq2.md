<task_order>
  <metadata>
    <id>IRPT_ANLREQ.TO-APPLY-R20.status-rule-all-eight-aq2</id>
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
comp-blast: DECLARED-NOT-APPLICABLE -- the blast radius is named in the signed pair (sections 1 to 4).
comp-routes: DECLARED-NOT-APPLICABLE -- no route is added or changed. comp-cache: DECLARED-NOT-APPLICABLE. comp-schedule: DECLARED-NOT-APPLICABLE -- no schedule or trigger.
comp-iam: DECLARED-NOT-APPLICABLE -- code only; each function's role and environment are unchanged (each scoped plan says so).
comp-adversary: RUN -- by reading rows D2-S66 and D2-S69 (the live package changed under a census; a build at a pre-guard commit uploaded) against this cell; the lens: a base taken from a record, a BUILD_ONLY at a commit without the guard, a digest accepted that is not the expected one. The order requires the live read and the object-hash read at step 0, the guard check before every build, and the expected CodeSha256 before any upload. NOT seen: the functions' configuration beyond CodeSha256.
</preflight>
<decomp_ref>
<decomp_doc>org/missions/D9/IRPT/IRPT_ANLREQ/decompositions/IRPT_ANLREQ_DECOMP_R20A_Y.md</decomp_doc> round 20, workstream YR round 12: the apply of the status rule into the eight packagers.
<owned_cells>AR-y-218</owned_cells>
</decomp_ref>

  <objective>
    Release, in eight sequential scoped applies, the eight functions named in the signed pair at the EXPECTED CodeSha256 of its table: `_authz/served.py` (commit 564e60483858a3cc5c51ffea6aed0f76ff291abe) into all eight, and `ops/status.py` (commit e93258c650b369df46e22210d94add7cbb0d1749) into irpt-status only. CODE ONLY; no other member of any package moves.
  </objective>

  <context>
    Load /cloud-ops first. Signed pair: COO half org/missions/D9/IRPT/IRPT_ANLREQ/deliverables/2.0.0_SA_COO~Y2/release20/NEVER_WIDEN_PAIR_ANLREQ_RELEASE20_STATUS_RULE_ALL_EIGHT.md (git hash-object 8eccf7b90a75d4fe300892ad151b0189d47addbe) and CTO half org/missions/D9/IRPT/IRPT_ANLREQ/deliverables/1.0.0_SA_CTO~DELL2/NEVER_WIDEN_ANLREQ_RELEASE20_STATUS_RULE_ALL_EIGHT_CTO_HALF.md (@67cadd141d, CTO msg 6896). A different COO blob voids both halves: STOP. The pair is the plan: its section 2 table (live CodeSha256, S3 latest version, base commit, release patch and its git hash-object, EXPECTED CodeSha256), section 3 (build, Terraform, rollback, source map, ledger), section 5 (step 0, sequence, after-reads A1 to A5), section 6 (both branches). The release patches are under org/missions/D9/IRPT/IRPT_ANLREQ/deliverables/0.9.0_WK_IRPT_ANLREQ~61/r20/ (group A), ~64/r20/ (group B) and ~66/r20/ (irpt-status.release2.diff).
    **THE GUARD:** before the first build at each base commit, `git show <commit>:infra/aws/lambda/ci/build-and-upload.sh | grep -c BUILD_ONLY` must be at least 1 (the three bases carry it: 8 mentions). Run the digest check with `BUILD_ONLY=1`; the real upload is the same script WITHOUT it, from the same worktree, only after the digest equals the EXPECTED value. At a commit older than the guard the script uploads (row D2-S69; this lane restored the irpt-holdings key after it).
  </context>

  <the_act>
    1. Open ledger irpt-status-rule-all-eight-20261013 (legs L1 verify, L2 before sample, L3 builds, L4 plans, L5 applies, L6 after sample, L7 first hour, L8 after-reads, L9 map record) and commit it; read every live worktree's open deploy entries (git worktree list, then ls-tree) and print the denominator: another open entry naming any of the eight functions is a STOP.
    2. L1 / R0: for each of the eight: `get-function` CodeSha256 equals the table's column 2; the key's latest S3 version equals column 3 AND that object, downloaded and hashed, equals the CodeSha256. Any difference: STOP for that function and report. Check git hash-object of each release patch against the table.
    3. L2: the act-4 sampler's SAMPLE_BEFORE (pair section 5, A3), or ABSENT with the reason.
    4. For each function in the table's order (L3 to L5, one unit at a time): throwaway worktree OUTSIDE the product tree DETACHED at the base commit; guard check; apply the release patch (uncommitted); `BUILD_ONLY=1` build; the printed CodeSha256 must equal the EXPECTED value (any other: ABORT that function, nothing uploaded; report); then the same build WITHOUT BUILD_ONLY (uploads one new object version), read the object back (sha256 equal to the build); scoped plan (`Plan: 0 to add, 1 to change, 0 to destroy`, attributes last_modified, s3_object_version, source_code_hash only, environment equal; anything else: STOP the sequence, nothing applied for this unit); `.tools/safe-apply.sh` on the saved plan; never `aws lambda update-function-code`. After each unit: A1 (CodeSha256 equals EXPECTED) and A2 (the live zip differs from the previous package only in the named members); a false A1 or A2: ROLL THAT FUNCTION BACK (pair section 3, copy the column-3 version onto the key, scoped plan, safe-apply, read column 2 back), stop the sequence, file a row, tell 2.0.0_SA_COO~Y2.
    5. L6/L8: SAMPLE_AFTER and A3 (or ABSENT), A5 (the irpt-status envelope for one of the 24 codes shows a CORRECT action with words, or ABSENT with the reason). Write the file org/tier2_senior/0.7.0_AE_CloudOps~AQ2/deliverables/irpt_anlreq_r20/L8_AFTER_R20.txt with, for each function, ONE line exactly: `A1 <function> live CodeSha256 <the CodeSha256 you read>` (eight lines), then your A2 to A5 results.
    6. L7: one hour after the last unit, A4: the INTERNAL-CALLER-CLASS lines of the eight functions' log groups counted by class and outcome with the denominator (functions read, minutes, lines); no identity is read or written. Send the counts to 1.0.0_SA_CTO~DELL2 (the CTO half asks for them) and to 2.0.0_SA_COO~Y2.
    7. L9: apply the eight release diffs to the trunk map in your own worktree (only the served.py rows and irpt-status's ops/status.py row) plus each function's artifact_* and last_deployed_* record; on any conflict beyond those rows STOP. Commit, close the ledger, report once to 2.0.0_SA_COO~Y2 with the eight CodeSha256 values and the commit.
  </the_act>

  <bounds>
    Eight functions' code and eight S3 object versions (one each). No env, IAM, route, permission or Terraform change beyond the three code attributes. No request is submitted. No identity is read or written. Remove the throwaway worktrees you made when the ledger closes (git worktree remove; a recursive delete of anything else needs Andrew's word). Rollback: per function, step 4.
  </bounds>

  <proof_of_spec>
Instance at `org/tier2_senior/0.7.0_AE_CloudOps~AQ2/deliverables/irpt_anlreq_r20/IRPT_ANLREQ.TO-APPLY-R20.status-rule-all-eight-aq2.proof_of_spec.json`.
    <criterion id="R20-AC1" cell_refs="AR-y-218"><invocation>python org/missions/D9/IRPT/IRPT_ANLREQ/deliverables/2.0.0_SA_COO~Y2/checks/r20/ar20_checks.py y218-apply --root C:/dev/ajb_workspace</invocation><expect>Y218-APPLY-OK</expect></criterion>
    <criterion id="R20-AC2" cell_refs="AR-y-218">The ledger irpt-status-rule-all-eight-20261013 is CLOSED.<invocation>grep -m1 '^\*\*Status' org/critical_paths/change_management/*irpt-status-rule-all-eight-20261013_deploy_completion.md</invocation><expect>^\*\*Status:\*\* CLOSED</expect></criterion>
  </proof_of_spec>
</task_order>
# pipeline-override: an APPLY order to a tier-2 applier under a signed pair (not a worker cell); the cell AR-y-218 is the issuer's, as for TO-APPLY-R19b.
