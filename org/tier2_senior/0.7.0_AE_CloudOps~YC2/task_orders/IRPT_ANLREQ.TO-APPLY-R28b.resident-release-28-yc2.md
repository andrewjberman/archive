<task_order>
  <metadata>
    <id>IRPT_ANLREQ.TO-APPLY-R28b.resident-release-28-yc2</id>
    <issued_by>2.0.0_SA_COO~Y2</issued_by>
    <issued_to>0.7.0_AE_CloudOps~YC2</issued_to>
    <date>2026-10-14</date>
    <status>complete</status>
    <project_code>IRPT_ANLREQ</project_code>
  </metadata>
<risk>WORLD</risk>
<proof_genre>DEPLOY</proof_genre>
<placeholders>NONE</placeholders>
<preflight>
comp-blast: DECLARED-NOT-APPLICABLE -- the blast radius is named, per key, in the signed pair (sections 3d and 4).
comp-routes: DECLARED-NOT-APPLICABLE -- no route is added or changed. comp-cache: DECLARED-NOT-APPLICABLE. comp-schedule: DECLARED-NOT-APPLICABLE -- a resident package swap; no schedule, trigger or EventBridge rule is added or read.
comp-iam: DECLARED-NOT-APPLICABLE -- no IAM change; step 6 only READS the resident role's policy; the host fetch is by key as in st26 to st32 and r19.
comp-adversary: RUN -- by reading the release-19 order and its V1 output (TO-APPLY-R19a) against this cell; the lens: a read-back that proves the new members and says nothing about the 289 that must not move, a constant carried over from release 19, an install started before the ticket service leg closed. The order requires the whole-package comparison (298 entries) and the eight member read-backs against the build record's values, a start only on the issuer's message that L1 is closed, and a rollback whose first lines refuse before anything moves. NOT seen: the host (no ssh or SSM from the issuer) and the rollback's run on the host.
</preflight>
<decomp_ref>
<decomp_doc>org/missions/D9/IRPT/IRPT_ANLREQ/decompositions/IRPT_ANLREQ_DECOMP_R33A_Y.md</decomp_doc> round 33, workstream YX: the resident leg of release 28.
<owned_cells>AR-y-303</owned_cells>
</decomp_ref>

  <objective>
    Install the resident root 0485393f3a-r28 over the running 0485393f3a-r19 on host i-0167fd745ad906a66, and read it back. One host, one new root, three new keys. The root differs from r19 in exactly the members of the pair's section 3d (nine differing, one added, none removed: the generated bindings and the sums, the reader r19.3, portfolio, uploads, security_resolution, ops/status, resident_worker, opal_packager, and the added lib/trading_calendar.py); the capture library and wrapper are NOT moved. NO removal leg: r28 stays unless V1 fails or the issuer orders X1.
    Files: C:/dev/irpt-release-r28/ and the scripts under org/missions/D9/IRPT/IRPT_ANLREQ/deliverables/0.9.0_WK_IRPT_ANLREQ~119/r31/ and ~118/r30/.
  </objective>

  <context>Load /cloud-ops first. The same shape as IRPT_ANLREQ.TO-APPLY-R19a (read it: org/tier2_senior/0.7.0_AE_CloudOps~YC2/task_orders/IRPT_ANLREQ.TO-APPLY-R19a.resident-reader-release-yc2.md and its output under deliverables/irpt_anlreq_r19/), with these differences: the old root is r19 (not st32); the host script is the release-28 one (the build's, 17 lines changed against r19's); the scripts are the release-28 ones of AR-y-301, which print the expected values next to what they read; a read of the resident role's policy is added (step 6). You submit no request and sign in as nobody. Nothing in this order starts a job or a capture.
  Signed pair: COO half org/missions/D9/IRPT/IRPT_ANLREQ/deliverables/2.0.0_SA_COO~Y2/release28/NEVER_WIDEN_PAIR_ANLREQ_RELEASE28_FWD1_CONSOLIDATED_FOUR_LEG.md (git hash-object e9bb20d7fe2f6d610c88c4399e6a4387af5e7743) and CTO half org/missions/D9/IRPT/IRPT_ANLREQ/deliverables/1.0.0_SA_CTO~DELL2/NEVER_WIDEN_ANLREQ_RELEASE28_FWD1_CONSOLIDATED_CTO_HALF.md (@d3adae2fc8, CTO msg 7415). A different COO blob voids both halves: STOP. The pair's section 2 wrongly says the ~IB2 ledger on irpt-ycharts-generate has closed; it is OPEN, it does not touch the resident, and it is not a STOP for this order (the issuer's correction, TO-APPLY-R28a AMENDMENT 1).</context>

  <the_act>
    GO: both halves are signed. You start ONLY when (a) step 1 reads green, (b) 2.0.0_SA_COO~Y2 has MESSAGED you that legs L2 and L1 are closed (the ticket service must be at CodeSha256 C/Rt/FnSqOj7SnZC1GeoEilj8jbCKdvAUHnxYrnNZNM= first: a new packager against the old server fails every attach with a 400, row W109-S2; you read that CodeSha256 yourself, read-only, at step 1), and (c) the stored-input recount of TO-APPLY-R28a (org/tier2_senior/0.7.0_AE_CloudOps~AQ2/deliverables/irpt_anlreq_r28/R0D_RECOUNT.txt) is in the tree, read within the last 60 minutes, with turned_back 0. Otherwise tell 2.0.0_SA_COO~Y2 and wait.
    1. Read the COO half and CTO half at HEAD; `git hash-object` of the COO half must print e9bb20d7fe2f6d610c88c4399e6a4387af5e7743. `get-function opal-ticket-api` CodeSha256 must be C/Rt/FnSqOj7SnZC1GeoEilj8jbCKdvAUHnxYrnNZNM= (read only). Anything else: STOP, report.
    2. U2: put three files under ec2/investor-reporting-ycharts/resident/ in bucket opal-313476888478-lambda-artifacts, each key 404 before the put, each read back with sha256 equal; a different sha256 is a STOP (a rebuilt file is a new pair):
       - irpt-resident-0485393f3a-r28.tar.gz = C:/dev/irpt-release-r28/irpt-resident-0485393f3a-r28.tar.gz, sha256 80f4743091a10c0d82b6cba4f66ba4afb6188ece0b64b269066c5426a6335a68
       - resident_host_install_0485393f3a-r28.sh = org/missions/D9/IRPT/IRPT_ANLREQ/deliverables/0.9.0_WK_IRPT_ANLREQ~118/r30/resident_host_install_0485393f3a-r28.sh, sha256 bbead0d2b560ca49be3ab1e758d3111c22174e755771a46bce23ae3977122832
       - irpt-resident-0485393f3a-r28.package.SHA256SUMS = C:/dev/irpt-release-r28/irpt-resident-0485393f3a-r28.package.SHA256SUMS, sha256 7978dae9b299a1649fbb221098b1ea4438bf8d67f6d4ecbb8ef01fd9656f59a8
    3. Open ledger irpt-resident-r28-20261013 (the name the host script writes into its receipt; legs U2 P1 D2 V1) and commit it; read every live worktree's org/critical_paths/.open_deploys/ (git worktree list, then git -C <wt> ls-tree) first and print the denominator: another open entry naming this host or the resident root is a STOP (an open entry on irpt-ycharts-generate or on the Lambdas is printed and is not).
    4. P1: host_read.py org/missions/D9/IRPT/IRPT_ANLREQ/deliverables/0.9.0_WK_IRPT_ANLREQ~119/r31/pre_read_r28.sh (sha256 8ab1d93f07378171143f3148c38e26f5218e3832f930f0123443e036ba966ed8). Expect: the r19 root running, the r28 root ABSENT, and FIVE lines printing PASS: `P1 STOP-READ PASS`, `P1 STOP-READ-2 PASS`, `P1 STOP-READ-3 PASS`, `P1 STOP-READ-4 PASS`, `P1 STOP-READ-5 PASS`; the reader members and the worker print with the value they are wanted at. Any FAIL: install nothing, send 2.0.0_SA_COO~Y2 the output path, stop. Save the output as org/tier2_senior/0.7.0_AE_CloudOps~YC2/deliverables/irpt_anlreq_r28/P1_PRE_READ_R28.txt.
    5. D2+V1: when irpt-generation reads 0 visible and 0 in flight, host_read.py org/missions/D9/IRPT/IRPT_ANLREQ/deliverables/0.9.0_WK_IRPT_ANLREQ~119/r31/install_r28.sh (sha256 1cb64da779254dfce0f279d1ae7f1e03ec33846fcdcc907f5f7bff16f7ab2c86). Expect: running root 0485393f3a-r28, active, 0 tracebacks, polls at least 1; V1 P2 uploads.py 80ace2d376c854d6208bc0c17810e053bc538ff9e71ec5a96d8dc89629d01951 and template_reader.py a61cd0c622f8dd54864b8f2415cbe9968c0287d28087ce703073c7e392c1fc35; READER_VERSION irpt-template-reader.r19.3; `V1 P2b` printing MATCH for all eight members and no MISMATCH; `V1 P3 sha256sum -c rc=0 lines not OK: 0 of 298 checked`; the producer, reader, packager, registry-port and calendar imports OK; `V1 P4 yfinance_check.py absent from the root: yes`; host library = bindings library = a1c2880169c5f7996cc7c5880e4fe36db90f0a2c1f5a1cd01e0d1d8153544841; host wrapper = bindings wrapper; the kept library copy reads a1c28801...; the rollback root 0485393f3a-r19 still present; NO SIGN-IN line 0. Any failure: the installer's own rollback to r19 (root and receipt) has already run: read it, then STOP and report. Save the output as org/tier2_senior/0.7.0_AE_CloudOps~YC2/deliverables/irpt_anlreq_r28/D2_V1_INSTALL_R28.txt.
    6. R0e (read only, not a gate): the live policy of the resident role (ycharts/resident.tf :61 runner_resident and :127-133): does it hold dynamodb:GetItem on table/etf-classifications? Save the policy statement or the read's refusal and say which. If it does not, the registry port returns REGISTRY_UNAVAILABLE and the answer is today's; tell 2.0.0_SA_COO~Y2 in the report.
    7. Report to 2.0.0_SA_COO~Y2 that V1 is closed, with the output paths and the running root; the L3 order waits for that message. Close the ledger at V1 green. Report every host send to 0.0.0_AB_MSTR~DELL2 after the fact.
    Not in this order, and not to be run without a new word from 2.0.0_SA_COO~Y2: org/missions/D9/IRPT/IRPT_ANLREQ/deliverables/0.9.0_WK_IRPT_ANLREQ~119/r31/rollback_r28.sh (sha256 c10e05137bba54836b6cba7b2786b30e9b317aaba9bbfa839d76306ed409d377), which puts the r19 root back and exits before moving anything if the rollback root, its receipt copy or the library is missing. Rollback order for the release: this resident leg BEFORE the ticket service (a rolled-back server refuses the new packager).
  </the_act>

  <bounds>
    Host i-0167fd745ad906a66 and three new keys under ec2/investor-reporting-ycharts/resident/. No IAM, Terraform, Lambda, queue, data or portal change. No secret read. No dead letter is received, redriven or deleted. Nothing is sent to Bloomberg. No request is submitted and no sign-in is attempted.
    Rollback: the installer's own, on a failed start; afterwards the X1 script above on the issuer's word, and only AFTER the Lambda irpt-ycharts-generate has been rolled back if its leg has run (a moved Lambda stores inputs the pinned resident may refuse), and before the ticket service is rolled back.
  </bounds>

  <proof_of_spec>
Instance at `org/tier2_senior/0.7.0_AE_CloudOps~YC2/deliverables/irpt_anlreq_r28/IRPT_ANLREQ.TO-APPLY-R28b.resident-release-28-yc2.proof_of_spec.json`.
    <criterion id="R28b-AC1" cell_refs="AR-y-303">The pre-read passed all five STOPs before anything was installed.<invocation>grep -c -E '^P1 STOP-READ(-[2345])? PASS' org/tier2_senior/0.7.0_AE_CloudOps~YC2/deliverables/irpt_anlreq_r28/P1_PRE_READ_R28.txt</invocation><expect>^5$</expect></criterion>
    <criterion id="R28b-AC2" cell_refs="AR-y-303">V1 shows the host running r28 with the whole package equal.<invocation>grep -m1 -E 'V1 P3 sha256sum -c rc=0 lines not OK: 0 of 298 checked' org/tier2_senior/0.7.0_AE_CloudOps~YC2/deliverables/irpt_anlreq_r28/D2_V1_INSTALL_R28.txt</invocation><expect>0 of 298 checked</expect></criterion>
    <criterion id="R28b-AC3" cell_refs="AR-y-303">The ledger irpt-resident-r28-20261013 is CLOSED.<invocation>grep -m1 '^\*\*Status' org/critical_paths/change_management/*irpt-resident-r28-20261013_deploy_completion.md</invocation><expect>^\*\*Status:\*\* CLOSED</expect></criterion>
  </proof_of_spec>
</task_order>
# pipeline-override: an APPLY order to a tier-2 applier under a signed pair (not a worker cell); the cell AR-y-303 is the issuer's, as for TO-APPLY-R19a.
