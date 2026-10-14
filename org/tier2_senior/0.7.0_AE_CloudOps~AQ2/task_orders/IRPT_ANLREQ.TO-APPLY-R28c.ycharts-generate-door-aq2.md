<task_order>
  <metadata>
    <id>IRPT_ANLREQ.TO-APPLY-R28c.ycharts-generate-door-aq2</id>
    <issued_by>2.0.0_SA_COO~Y2</issued_by>
    <issued_to>0.7.0_AE_CloudOps~AQ2</issued_to>
    <date>2026-10-14</date>
    <status>complete</status>
    <project_code>IRPT_ANLREQ</project_code>
  </metadata>
<risk>WORLD</risk>
<proof_genre>DEPLOY</proof_genre>
<placeholders>NONE</placeholders>
<preflight>
comp-blast: DECLARED-NOT-APPLICABLE -- the blast radius is named in the signed pair (sections 3c and 4b): a Shares file with no price date is now accepted and priced at the previous trading day, a two-account file under three header forms is now turned back, the registry evidence and the KEPT words exist (no emitter), nothing else.
comp-routes: DECLARED-NOT-APPLICABLE -- no route is added or changed. comp-cache: DECLARED-NOT-APPLICABLE. comp-schedule: DECLARED-NOT-APPLICABLE -- no schedule or trigger.
comp-iam: DECLARED-NOT-APPLICABLE -- code only; the function's role and environment are unchanged (the scoped plan says so).
comp-adversary: RUN -- by reading rows W117-S1 to S4 (a one-row staged_from does not ship the calendar; a pin move needs the sha256 move; the diff applies only with --unidiff-zero; the map's last_deployed_commit is not the live base) and the pair's wrong line about the ~IB2 ledger against this cell; the lens: a base taken from the map instead of the live package, a digest accepted that is not the expected one, an apply while another seat's ledger on the same function is open. The order requires the live read and the object-hash read at step 0, the ~IB2 ledger CLOSED before anything moves, the guard check before every build and the expected CodeSha256 before any upload. NOT seen: the function's configuration beyond CodeSha256; the Terraform state.
</preflight>
<decomp_ref>
<decomp_doc>org/missions/D9/IRPT/IRPT_ANLREQ/decompositions/IRPT_ANLREQ_DECOMP_R34A_Y.md</decomp_doc> round 34, workstream YY: the apply of release 28, leg L3.
<owned_cells>AR-y-304</owned_cells>
</decomp_ref>

  <objective>
    Release, as one scoped apply, the Lambda irpt-ycharts-generate at the EXPECTED CodeSha256 of the pair's section 3c: `template_reader.py` (r19.3), `portfolio.py`, `uploads.py`, `security_resolution.py` moved to the trunk blobs, and `trading_calendar.py` ADDED at the package root. CODE ONLY; no other member moves. Then STOP and report: the synthetic sitting is a later order.
  </objective>

  <context>
    Load /cloud-ops first. Signed pair: COO half org/missions/D9/IRPT/IRPT_ANLREQ/deliverables/2.0.0_SA_COO~Y2/release28/NEVER_WIDEN_PAIR_ANLREQ_RELEASE28_FWD1_CONSOLIDATED_FOUR_LEG.md (git hash-object e9bb20d7fe2f6d610c88c4399e6a4387af5e7743) and CTO half org/missions/D9/IRPT/IRPT_ANLREQ/deliverables/1.0.0_SA_CTO~DELL2/NEVER_WIDEN_ANLREQ_RELEASE28_FWD1_CONSOLIDATED_CTO_HALF.md (@d3adae2fc8, CTO msg 7415). A different COO blob voids both halves: STOP. The pair is the plan: section 2 (start state), section 3c (the artifact, the expected CodeSha256, the release input, the rollback), section 5 step 4 and step 5, section 6. The staged zip is the control, NOT what you upload: C:/dev/irpt-release-r28/irpt-ycharts-generate-r28.zip (sha256 ade02301039555f0f85ae8b6bb451f651b7b72bf68ea2a05288c176bef045607, 632858 bytes); the upload is the builder script's own, from the recorded input, and the staged zip must equal what it builds. Release record: org/missions/D9/IRPT/IRPT_ANLREQ/deliverables/0.9.0_WK_IRPT_ANLREQ~117/r30/IRPT_YCHARTS_GENERATE_BUILD.json (read `release_input`, `no_move_control` and the failing-id baseline).
    **The function was released by `~IB2` at 2026-10-13T22:48:27Z** (ledger 20261013T2236Z_irpt-ycg-catalogue-ultrashort-20261013, base 0c0ae5a8f5 plus the IB184-1 row diff). The pair's section 2 says that ledger has closed; at the time of the issuer's reading it was OPEN with its L6 after-read unproven (TO-APPLY-R28a AMENDMENT 1). THIS order starts only when it reads CLOSED (CTO half condition 2). If IB-pr-456 or any other change has moved the function since, the start state differs: STOP at step 2 and tell the issuer.
    **THE GUARD:** before the first build at the base commit, `git show 0c0ae5a8f5cee99e9c7fa49b8043c146fed1d05e:infra/aws/lambda/ci/build-and-upload.sh | grep -c BUILD_ONLY` must be at least 1 (it carries 8). Run the digest check with `BUILD_ONLY=1`; the real upload is the same script WITHOUT it, from the same worktree, only after the digest equals the EXPECTED value. At a commit older than the guard the script uploads (row D2-S69). The trunk-based worktree needs `git -c core.longpaths=true` on this checkout (row W115-S1).
  </context>

  <the_act>
    GO: both halves are signed. You start ONLY when (a) step 1 reads green, (b) the ledger 20261013T2236Z_irpt-ycg-catalogue-ultrashort-20261013 reads `**Status:** CLOSED` (read the file at HEAD of every live worktree that carries it and print which), and (c) 2.0.0_SA_COO~Y2 has MESSAGED you that the resident leg L4 is closed (its root reads 0485393f3a-r28 and V1 is green). Otherwise tell 2.0.0_SA_COO~Y2 and wait.
    1. Read the COO half and CTO half at HEAD; `git hash-object` of the COO half must print e9bb20d7fe2f6d610c88c4399e6a4387af5e7743. Open ledger irpt-ycg-r28-20261014 (legs L1 verify, L2 build, L3 plan, L4 apply, L5 after-reads, L6 map record) and commit it; read every live worktree's org/critical_paths/.open_deploys/ (git worktree list, then git -C <wt> ls-tree) FIRST and print the denominator: another open entry naming irpt-ycharts-generate is a STOP.
    2. R0b: `get-function irpt-ycharts-generate` CodeSha256 equals xP47NQDnZNZ8Lui1XQKUxUtTMTasR8Cj/A1sQnRDZYY=; the key investor-reporting/irpt-ycharts-generate.zip latest S3 version equals VXbWnMBmqbLWHNCsu1W8pF_HyseDHR1e AND that object, downloaded and hashed, equals the CodeSha256. Any difference: STOP and report (someone released; the issuer rebuilds, which is a new cell).
    3. Read the credential-less refusal envelope first: one invocation WITHOUT credentials, status and body sha256 (G3 before).
    4. UNIT L3. A throwaway worktree OUTSIDE the product tree DETACHED at 0c0ae5a8f5cee99e9c7fa49b8043c146fed1d05e (`git -c core.longpaths=true worktree add --detach`); guard check printed; apply, uncommitted, the diff org/missions/D9/IRPT/IRPT_ANLREQ/deliverables/0.9.0_WK_IRPT_ANLREQ~117/r30/ycharts_release_input.diff with `git apply --unidiff-zero` (`git hash-object` of the diff must print d80f656489b366d1e73a5e3a3ae39aa174f1bbab); `BUILD_ONLY=1 bash infra/aws/lambda/ci/build-and-upload.sh investor-reporting irpt-ycharts-generate`: the printed CodeSha256 must equal reAjAQOVVfD4Wui2u0UfZRt7cr9o6ioFKIwXa+8EVgc= (any other: ABORT, nothing uploaded; report); then the same build WITHOUT BUILD_ONLY (it uploads one new object version); read the object back (sha256 equals the staged zip's ade023010395...); scoped plan from infra/aws/terraform/investor-reporting/ycharts (`-target=module.irpt_ycharts_generate.aws_lambda_function.this`): `Plan: 0 to add, 1 to change, 0 to destroy`, attributes last_modified, s3_object_version, source_code_hash ONLY, environment equal (anything else: STOP, nothing applied); `.tools/safe-apply.sh` on the saved plan; never `aws lambda update-function-code`.
    5. After the apply: G1 CodeSha256 equals reAjAQOVVfD4Wui2u0UfZRt7cr9o6ioFKIwXa+8EVgc=; G2 the live zip has 105 members, and against the previous version (VXbWnMBmqbLWHNCsu1W8pF_HyseDHR1e) exactly template_reader.py, portfolio.py, uploads.py and security_resolution.py differ and trading_calendar.py is added (member-by-member sha256); G3 the credential-less refusal envelope equals the one read before (status and body sha256); G4 the function's environment variables and role are unchanged (read both before and after, compare, print equal). A false G1 to G4: ROLL BACK (pair section 3c: copy VersionId VXbWnMBmqbLWHNCsu1W8pF_HyseDHR1e onto the key, scoped plan, safe-apply, read xP47NQDn... back), STOP, file a row, tell 2.0.0_SA_COO~Y2.
    6. Write org/tier2_senior/0.7.0_AE_CloudOps~AQ2/deliverables/irpt_anlreq_r28/G_AFTER_R28c.txt with, ONE line exactly: `A1 irpt-ycharts-generate live CodeSha256 <the CodeSha256 you read>`, then your G2 to G4 results and the object VersionId uploaded.
    7. Map close commit: in your own worktree apply to the trunk map (lambda-source-map.json) the irpt-ycharts-generate entry's changes of the diff (the four pin moves with their sha256, the trading_calendar.py row AND its files[] entry, which the diff's builder run needed: rows W117-S1 and W117-S2) plus the entry's artifact_* and last_deployed_* record (new VersionId, CodeSha256, base); the IB184-1 row of the diff is already in the trunk map if ~IB2 closed its ledger, so apply only what differs; on any conflict beyond these rows STOP. Commit, close the ledger, and report ONCE to 2.0.0_SA_COO~Y2: "L3 closed" with the CodeSha256, the VersionId, the output path and the map commit. Report every Terraform apply to 0.0.0_AB_MSTR~DELL2 after the fact.
  </the_act>

  <bounds>
    One function's code and one S3 object version. No env, IAM, route, permission or Terraform change beyond the three code attributes. No request is submitted. No identity is minted, read or written. Not in this order: the synthetic sitting, the resident (closed), any other Lambda. Remove the throwaway worktree you made when the ledger closes (git worktree remove; a recursive delete of anything else needs Andrew's word). Rollback: step 5.
  </bounds>

  <proof_of_spec>
Instance at `org/tier2_senior/0.7.0_AE_CloudOps~AQ2/deliverables/irpt_anlreq_r28/IRPT_ANLREQ.TO-APPLY-R28c.ycharts-generate-door-aq2.proof_of_spec.json`.
    <criterion id="R28c-AC1" cell_refs="AR-y-304">The function reads the expected CodeSha256 after the apply.<invocation>grep -c -E '^A1 irpt-ycharts-generate live CodeSha256 reAjAQOVVfD4Wui2u0UfZRt7cr9o6ioFKIwXa\+8EVgc=$' org/tier2_senior/0.7.0_AE_CloudOps~AQ2/deliverables/irpt_anlreq_r28/G_AFTER_R28c.txt</invocation><expect>^1$</expect></criterion>
    <criterion id="R28c-AC2" cell_refs="AR-y-304">The ledger irpt-ycg-r28-20261014 is CLOSED.<invocation>grep -m1 '^\*\*Status' org/critical_paths/change_management/*irpt-ycg-r28-20261014_deploy_completion.md</invocation><expect>^\*\*Status:\*\* CLOSED</expect></criterion>
  </proof_of_spec>
</task_order>
# pipeline-override: an APPLY order to a tier-2 applier under a signed pair (not a worker cell); the cell AR-y-304 is the issuer's, as for TO-APPLY-R28a.
