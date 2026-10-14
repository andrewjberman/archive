<task_order>
  <metadata>
    <id>IRPT_ANLREQ.TO-APPLY-R29a.status-words-aq2</id>
    <issued_by>2.0.0_SA_COO~Y2</issued_by>
    <issued_to>0.7.0_AE_CloudOps~AQ2</issued_to>
    <date>2026-10-14</date>
    <status>pending</status>
    <project_code>IRPT_ANLREQ</project_code>
  </metadata>
<risk>WORLD</risk>
<proof_genre>DEPLOY</proof_genre>
<placeholders>NONE</placeholders>
<preflight>
comp-blast: DECLARED-NOT-APPLICABLE -- the blast radius is named in the signed pair (sections 3a and 4b): one word entry in the status envelope; nothing widens in this leg.
comp-routes: DECLARED-NOT-APPLICABLE -- no route is added or changed. comp-cache: DECLARED-NOT-APPLICABLE. comp-schedule: DECLARED-NOT-APPLICABLE -- no schedule or trigger.
comp-iam: DECLARED-NOT-APPLICABLE -- code only; the function's role and environment are unchanged (the scoped plan says so).
comp-adversary: RUN -- by reading rows W116-S1 and W123-S1 (the map's last_deployed_commit does not rebuild the live zip), D2-S66 and D2-S69 (the live package changed under a census; a build at a pre-guard commit uploaded) against this cell; the lens: a base taken from a record, a BUILD_ONLY at a commit without the guard, a digest accepted that is not the expected one, a plan that changes more than the three code attributes. The order requires the live read and the object-hash read at step 2, the guard check before every build, and the expected CodeSha256 before any upload. NOT seen: the function's configuration beyond CodeSha256; the Terraform state.
</preflight>
<decomp_ref>
<decomp_doc>org/missions/D9/IRPT/IRPT_ANLREQ/decompositions/IRPT_ANLREQ_DECOMP_R40A_Y.md</decomp_doc> round 40, workstream ZD: the apply of release 29, leg L2.
<owned_cells>AR-y-312</owned_cells>
</decomp_ref>

  <objective>
    Release `irpt-status` (leg L2 of the signed release-29 pair) at the EXPECTED CodeSha256 of its section 3a: `ops/status.py` with ONE added key in `CORRECTION_WORDS`, `SHARES_PRICE_SOURCE_NOT_COMPOSED`. CODE ONLY; no other member of the package moves. Then STOP and report to 2.0.0_SA_COO~Y2: the resident (L4) and `irpt-ycharts-generate` (L3) are NOT in this order.
  </objective>

  <context>
    Load /cloud-ops first. Signed pair: COO half org/missions/D9/IRPT/IRPT_ANLREQ/deliverables/2.0.0_SA_COO~Y2/release29/NEVER_WIDEN_PAIR_ANLREQ_RELEASE29_ORDINARY_VIEWER_AND_SHARES_WORDS_THREE_LEG.md (git hash-object 5e8b3cbd95739fe8b9172329cc671d2ef7ea1aa8) and CTO half org/missions/D9/IRPT/IRPT_ANLREQ/deliverables/1.0.0_SA_CTO~DELL2/NEVER_WIDEN_ANLREQ_RELEASE29_ORDINARY_VIEWER_AND_SHARES_WORDS_CTO_HALF.md (@abbfe49feb, CTO msg 7591). A different COO blob voids both halves: STOP. The pair is the plan: section 2 (start state), 3a (the artifact, the expected CodeSha256, the rollback), 5 step 0 and step 1, section 6. The staged zip is the control, NOT what you upload: C:/dev/irpt-release-r29/irpt-status-r29.zip (sha256 c8da70e38d533f968c198b99aa41d000f8c089024310f93babc9057838884488, 363818 bytes); the upload is the builder script's own (it sets the object metadata the Terraform source_code_hash reads), from the recorded input, and the staged zip must equal what it builds. Build record: org/missions/D9/IRPT/IRPT_ANLREQ/deliverables/0.9.0_WK_IRPT_ANLREQ~123/r39/IRPT_STATUS_BUILD.json (read `release_input`, `no_move_control`, `rollback`).
    **THE GUARD:** before the first build at the base commit, `git show d39886e4aa3cfcb68c05b9abda3600f418cae873:infra/aws/lambda/ci/build-and-upload.sh | grep -c BUILD_ONLY` must be at least 1 (it carries 8). Run the digest check with `BUILD_ONLY=1`; the real upload is the same script WITHOUT it, from the same worktree, only after the digest equals the EXPECTED value. At a commit older than the guard the script uploads (row D2-S69). The worktree needs `git -c core.longpaths=true` on this checkout (row W115-S1). Use a private TMPDIR (a new empty folder outside the repository) for every build: the builder's zip temp path is one fixed name per function (row W123-S2).
    **Row W123-S1 (ARMED, yours to disarm):** the map's `last_deployed_commit` for `irpt-status` does not reproduce the live zip; step 7 re-pins it in the map close commit.
    **What this leg releases (pair section 4b):** the words a person sees for a Shares file; no one gains or loses any ability.
  </context>

  <the_act>
    GO: both halves are signed. The c449 delete order (TO-DELETE-C449) is PARKED by the issuer after your STOP (msg 7592: an explicit IAM deny; the route is asked of 1.0.0_SA_CTO~DELL2); it does not hold this order. Start at step 1 and go on when it reads green. Otherwise tell 2.0.0_SA_COO~Y2 and wait.
    1. Read the COO half and CTO half at HEAD; `git hash-object` of the COO half must print 5e8b3cbd95739fe8b9172329cc671d2ef7ea1aa8. Open ledger irpt-status-r29-20261014 (legs L1 verify, L2 build, L3 plan, L4 apply, L5 after-reads, L6 map record) and commit it; read every live worktree's org/critical_paths/.open_deploys/ (git worktree list, then git -C <wt> ls-tree) FIRST and print the denominator: another open entry naming irpt-status is a STOP (an open entry on the resident or on irpt-ycharts-generate is printed in the denominator and does not stop L2).
    2. R0b: `get-function irpt-status` CodeSha256 equals MIVrDbv+/w8ioVB24xS97gnETVbNRCroDiY+Ne5osbA=; the key investor-reporting/irpt-status.zip latest S3 version equals V_g2PtX08Ktkbo5XYohrB5pHDFctjzZE AND that object, downloaded and hashed, equals the CodeSha256. Any difference: STOP and report (someone released; the issuer rebuilds, which is a new cell).
    3. Read the credential-less refusal envelope first: one invocation WITHOUT credentials, status and body sha256 (S3 before).
    4. A throwaway worktree OUTSIDE the product tree DETACHED at d39886e4aa3cfcb68c05b9abda3600f418cae873 (`git -c core.longpaths=true worktree add --detach`); guard check printed; apply, uncommitted, the diff org/missions/D9/IRPT/IRPT_ANLREQ/deliverables/0.9.0_WK_IRPT_ANLREQ~123/r39/status_release_map_repin.diff (`git hash-object` must print 33b9de7137bafc7df8e903265f997102ba567b9a); `TMPDIR=<private> BUILD_ONLY=1 bash infra/aws/lambda/ci/build-and-upload.sh investor-reporting irpt-status`: the printed CodeSha256 must equal yNpw441TP5aMGYuZqkHQAPjAiQJDEPk7q8kFeDiIRIg= (any other: ABORT the unit, nothing uploaded; report); then the same build WITHOUT BUILD_ONLY (it uploads one new object version); read the object back (sha256 equals the staged zip's c8da70e38d53...).
    5. Scoped plan from infra/aws/terraform/investor-reporting/ops (`-target=module.irpt_status.aws_lambda_function.this`): `Plan: 0 to add, 1 to change, 0 to destroy`, attributes last_modified, s3_object_version, source_code_hash ONLY, environment equal (anything else: STOP, nothing applied); `.tools/safe-apply.sh` on the saved plan; never `aws lambda update-function-code`.
    6. After the apply: S1 CodeSha256 equals yNpw441TP5aMGYuZqkHQAPjAiQJDEPk7q8kFeDiIRIg=; S2 the live zip has 49 members and differs from the previous version (V_g2PtX08Ktkbo5XYohrB5pHDFctjzZE) only in status.py (member-by-member sha256); S3 the credential-less refusal envelope equals the one read before (status and body sha256). A false S1 to S3: ROLL BACK (pair section 3a: copy VersionId V_g2PtX08Ktkbo5XYohrB5pHDFctjzZE onto the key, scoped plan, safe-apply, read MIVrDbv+... back), STOP, file a row, tell 2.0.0_SA_COO~Y2. Write org/tier2_senior/0.7.0_AE_CloudOps~AQ2/deliverables/irpt_anlreq_r29/A_AFTER_R29a.txt with, ONE line exactly: `A1 irpt-status live CodeSha256 <the CodeSha256 you read>`, then your S2, S3 results and the object VersionId uploaded.
    7. Map record: in your own worktree apply the status.py row of the diff to the trunk map (lambda-source-map.json) plus the function's artifact_* and last_deployed_* record (the new VersionId, CodeSha256, commit); on any conflict beyond those rows STOP. Commit, close the ledger, and report ONCE to 2.0.0_SA_COO~Y2: "L2 closed" with the CodeSha256, the VersionId, the output path and the map commit. Report the Terraform apply to 0.0.0_AB_MSTR~DELL2 after the fact.
  </the_act>

  <bounds>
    One function's code and one S3 object version. No env, IAM, route, permission or Terraform change beyond the three code attributes. No request is submitted. No identity is minted, read or written. Not in this order: the resident (L4), irpt-ycharts-generate (L3), the sitting. Remove the throwaway worktree you made when the ledger closes (git worktree remove; a recursive delete of anything else needs Andrew's word). Rollback: step 6.
  </bounds>

  <proof_of_spec>
Instance at `org/tier2_senior/0.7.0_AE_CloudOps~AQ2/deliverables/irpt_anlreq_r29/IRPT_ANLREQ.TO-APPLY-R29a.status-words-aq2.proof_of_spec.json`.
    <criterion id="R29a-AC1" cell_refs="AR-y-312">The function reads the expected CodeSha256 after the apply.<invocation>grep -c -E '^A1 irpt-status live CodeSha256 yNpw441TP5aMGYuZqkHQAPjAiQJDEPk7q8kFeDiIRIg=$' org/tier2_senior/0.7.0_AE_CloudOps~AQ2/deliverables/irpt_anlreq_r29/A_AFTER_R29a.txt</invocation><expect>^1$</expect></criterion>
    <criterion id="R29a-AC2" cell_refs="AR-y-312">The ledger irpt-status-r29-20261014 is CLOSED.<invocation>grep -m1 '^\*\*Status' org/critical_paths/change_management/*irpt-status-r29-20261014_deploy_completion.md</invocation><expect>^\*\*Status:\*\* CLOSED</expect></criterion>
  </proof_of_spec>
</task_order>
# pipeline-override: an APPLY order to a tier-2 applier under a signed pair (not a worker cell); the cell AR-y-312 is the issuer's, as for TO-APPLY-R28a.
