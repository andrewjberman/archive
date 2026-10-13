<task_order>
  <metadata>
    <id>IRPT_ANLREQ.TO-APPLY-R19b.lambda-reader-release-ib2</id>
    <issued_by>2.0.0_SA_COO~Y2</issued_by>
    <issued_to>0.7.0_AE_CloudOps~IB2</issued_to>
    <date>2026-10-13</date>
    <status>complete</status>
    <project_code>IRPT_ANLREQ</project_code>
  </metadata>
<risk>WORLD</risk>
<proof_genre>DEPLOY</proof_genre>
<placeholders>NONE</placeholders>
<preflight>
comp-blast: DECLARED-NOT-APPLICABLE -- the blast radius is named, per key, in the signed pair (section 3b and 4).
comp-routes: DECLARED-NOT-APPLICABLE -- no route is added or changed. comp-cache: DECLARED-NOT-APPLICABLE. comp-schedule: DECLARED-NOT-APPLICABLE -- no schedule or trigger.
comp-iam: DECLARED-NOT-APPLICABLE -- code only; the function's role and environment are unchanged (the scoped plan says so).
comp-adversary: RUN -- by reading ADVI_FIRMBKTS act 4's ledger (which replaced this package on 2026-10-12) and AR-y-201's record against this cell; the lens: a build from the trunk head (its map re-pins loaders.py) or from a stale hold pin, and a package compared with another build and not with the live one. The order builds at 5d8b0390ed with the R2 patch, requires the printed CodeSha256, and compares members with the live package. NOT seen: the Lambda's configuration beyond CodeSha256, and the deployed portal bundles.
</preflight>
<decomp_ref>
<decomp_doc>org/missions/D9/IRPT/IRPT_ANLREQ/decompositions/IRPT_ANLREQ_DECOMP_R19A_Y.md</decomp_doc> round 8, workstream YR: the Lambda leg of the reader's release.
<owned_cells>AR-y-206</owned_cells>
</decomp_ref>

  <objective>
    Release irpt-ycharts-generate at CodeSha256 bNPCG2Oe1oQM/ztjggmrdDbdl83CAmUEcPnBFxlj2Rk= (package sha256 6cd3c21b639ed6840cff3b638209ab7436dd97cdc202650470f9c1171963d919, 620712 bytes, 104 members): the live package NeAB50CNXWvM5Y6nsba220QmsEiASbVbXcZVRYe4MUM= with exactly two members
    moved (uploads.py, template_reader.py), by ONE scoped safe-apply of module.irpt_ycharts_generate.aws_lambda_function.this in infra/aws/terraform/investor-reporting/ycharts. CODE ONLY.
  </objective>

  <context>
    Load /cloud-ops first. Signed pair: COO half org/missions/D9/IRPT/IRPT_ANLREQ/deliverables/2.0.0_SA_COO~Y2/release19/NEVER_WIDEN_PAIR_ANLREQ_RELEASE19_READER_TWO_LEG.md (git hash-object 2140b9352cf527e6984106a876eccc095bd7452f) and CTO half org/missions/D9/IRPT/IRPT_ANLREQ/deliverables/1.0.0_SA_CTO~DELL2/NEVER_WIDEN_ANLREQ_RELEASE19_READER_TWO_LEG_CTO_HALF.md (@6facbbb2d3, CTO msg 6802), section 3b and 5 step 2. A different COO blob voids both halves: STOP.
    START ONLY on a message from 2.0.0_SA_COO~Y2 saying the resident leg's V1 is closed green (the resident moves first; a moved Lambda stores inputs the pinned resident refuses). Any other order of the legs is a STOP.
    Records: AR-y-201 `org/missions/D9/IRPT/IRPT_ANLREQ/deliverables/0.9.0_WK_IRPT_ANLREQ~56/r19/LAMBDA_LEG_LIVE_REBASE.json` (the live and the release member manifests, the hold pins; drained @a011ddd400) and the patch
    `org/missions/D9/IRPT/IRPT_ANLREQ/deliverables/0.9.0_WK_IRPT_ANLREQ~56/r19/RELEASE_MAP_PATCH_R2.diff` (git hash-object df4d740e08c54566819a1b37942563df32f5a80e). The model for the legs is ADVI_FIRMBKTS act 4's ledger `org/critical_paths/change_management/20261012T1340Z_advi-firmbkts-fb-f-11-act4-irpt-leg-20261012_deploy_completion.md`.
  </context>

  <the_act>
    1. Open ledger irpt-ycg-r19-reader-20261013 (legs L1 verify, L2 before, L3 build, L4 plan, L5 apply, L6 after, L7 close, L8 map record) and commit it; read every live worktree's org/critical_paths/change_management open entries (git worktree list, then ls-tree) and print the denominator: another open entry naming irpt-ycharts-generate is a STOP.
    2. L1 / R0b: `get-function irpt-ycharts-generate`: CodeSha256 must read NeAB50CNXWvM5Y6nsba220QmsEiASbVbXcZVRYe4MUM=, and the S3 key investor-reporting/irpt-ycharts-generate.zip in opal-313476888478-lambda-artifacts must have latest VersionId _1MrCfPkpVkl7XDAC3NsbLhvIDvHBusc. Anything else: STOP, report (someone moved it).
    3. L2 BEFORE: if the function has a side-effect-free refusal path you can reach with an event that carries no credentials, invoke it once and record status and body sha256; if it has none, record ABSENT with the reason. Do not submit a request.
    4. L3 build: a throwaway worktree OUTSIDE the product tree, DETACHED at 5d8b0390ed (git worktree add --detach <abs-path> 5d8b0390ed); apply RELEASE_MAP_PATCH_R2.diff (git apply; check its git hash-object first), uncommitted. Run `BUILD_ONLY=1 bash infra/aws/lambda/ci/build-and-upload.sh investor-reporting irpt-ycharts-generate` there and copy the zip at once.
       The printed CodeSha256 must be bNPCG2Oe1oQM/ztjggmrdDbdl83CAmUEcPnBFxlj2Rk=; the zip's 104 member sha256 values must equal release_build.member_manifest of the AR-y-201 record, and differ from the LIVE zip's (download it) in exactly template_reader.py and uploads.py. Any other digest or member: STOP before any upload.
       Then run build-and-upload.sh WITHOUT BUILD_ONLY from the same worktree (it uploads a new object version), record the VersionId, and read the object back: sha256 equal to the build.
    5. L4 plan: scoped (`-target module.irpt_ycharts_generate.aws_lambda_function.this`) in infra/aws/terraform/investor-reporting/ycharts. Branch A: `Plan: 0 to add, 1 to change, 0 to destroy`, differing attributes last_modified, s3_object_version, source_code_hash only, environment equal. Anything else is branch B: STOP and restore nothing (nothing is applied yet; say the uploaded VersionId is unused).
    6. L5: `.tools/safe-apply.sh` on the saved plan. Never `aws lambda update-function-code`.
    7. L6 AFTER: CodeSha256 reads bNPCG2Oe1oQM/ztjggmrdDbdl83CAmUEcPnBFxlj2Rk=; download the live zip: 104 members, exactly uploads.py and template_reader.py differ from the previous package; the same refusal sample as step 3 (or ABSENT) equals the BEFORE; the function's environment keys and role equal the BEFORE read.
       The door reads D1 to D4 and C1 are ABSENT by the CTO's ruling (no caller): record them as ABSENT, and that S33 is RELEASED, NOT SHOWN LIVE.
    8. Any of 7 false: ROLL BACK AT ONCE: copy S3 version _1MrCfPkpVkl7XDAC3NsbLhvIDvHBusc onto investor-reporting/irpt-ycharts-generate.zip, scoped plan and safe-apply, read CodeSha256 NeAB50CNXWvM5Y6nsba220QmsEiASbVbXcZVRYe4MUM= back, close the ledger ROLLED_BACK, file a row, tell 2.0.0_SA_COO~Y2. The resident stays moved (the safe mixed state).
    9. L8: apply RELEASE_MAP_PATCH_R2.diff to the trunk map (infra/aws/lambda/ci/lambda-source-map.json) in your own worktree, plus the artifact_* and last_deployed_* record the deploy tooling writes; on any conflict beyond those six staged_from rows STOP. Commit, close the ledger, report once to 2.0.0_SA_COO~Y2 with the deployed CodeSha256, the VersionId and the commit.
  </the_act>

  <bounds>
    One function's code and one S3 object version. No env, IAM, route, permission or Terraform change beyond the three code attributes. No request is submitted. Remove the throwaway worktrees you made when the ledger closes (git worktree remove; a recursive delete of anything else needs Andrew's word).
    Rollback: step 8.
  </bounds>

  <proof_of_spec>
Instance at `org/tier2_senior/0.7.0_AE_CloudOps~IB2/deliverables/irpt_anlreq_r19/IRPT_ANLREQ.TO-APPLY-R19b.lambda-reader-release-ib2.proof_of_spec.json`.
    <criterion id="R19b-AC1" cell_refs="AR-y-206">The build printed the expected CodeSha256 before any upload.<invocation>grep -c 'bNPCG2Oe1oQM/ztjggmrdDbdl83CAmUEcPnBFxlj2Rk=' org/tier2_senior/0.7.0_AE_CloudOps~IB2/deliverables/irpt_anlreq_r19/L3_BUILD_R19.txt</invocation><expect>^[1-9]</expect></criterion>
    <criterion id="R19b-AC2" cell_refs="AR-y-206">The live function reads the expected CodeSha256 after the apply.<invocation>grep -m1 'live CodeSha256 bNPCG2Oe1oQM/ztjggmrdDbdl83CAmUEcPnBFxlj2Rk=' org/tier2_senior/0.7.0_AE_CloudOps~IB2/deliverables/irpt_anlreq_r19/L6_AFTER_R19.txt</invocation><expect>live CodeSha256 bNPCG2Oe</expect></criterion>
    <criterion id="R19b-AC3" cell_refs="AR-y-206">The ledger irpt-ycg-r19-reader-20261013 is CLOSED.<invocation>grep -m1 '^\*\*Status' org/critical_paths/change_management/*irpt-ycg-r19-reader-20261013_deploy_completion.md</invocation><expect>^\*\*Status:\*\* CLOSED</expect></criterion>
  </proof_of_spec>
</task_order>
# pipeline-override: an APPLY order to a tier-2 applier under a signed pair (not a worker cell); the cell AR-y-206 is the issuer's, as for TO-APPLY-R13b.
