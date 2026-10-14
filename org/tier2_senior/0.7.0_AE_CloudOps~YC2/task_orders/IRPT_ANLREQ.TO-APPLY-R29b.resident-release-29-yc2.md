<task_order>
  <metadata>
    <id>IRPT_ANLREQ.TO-APPLY-R29b.resident-release-29-yc2</id>
    <issued_by>2.0.0_SA_COO~Y2</issued_by>
    <issued_to>0.7.0_AE_CloudOps~YC2</issued_to>
    <date>2026-10-14</date>
    <status>pending</status>
    <project_code>IRPT_ANLREQ</project_code>
  </metadata>
<risk>WORLD</risk>
<proof_genre>DEPLOY</proof_genre>
<placeholders>NONE</placeholders>
<preflight>
comp-blast: DECLARED-NOT-APPLICABLE -- the blast radius is named, per key, in the signed pair (sections 3b and 4b): two moved code members, the bindings' package pin and the sums; nothing widens in this leg.
comp-routes: DECLARED-NOT-APPLICABLE -- no route is added or changed. comp-cache: DECLARED-NOT-APPLICABLE. comp-schedule: DECLARED-NOT-APPLICABLE -- a resident package swap; no schedule, trigger or EventBridge rule is added or read.
comp-iam: DECLARED-NOT-APPLICABLE -- no IAM change; the host fetch is by key as in release 28.
comp-adversary: RUN -- by reading the release-28 order and its V1 output (TO-APPLY-R28b, D2_V1_INSTALL_R28.txt) against this cell; the lens: a read-back that proves the new members and says nothing about the 297 that must not move, a constant carried over from release 28, an install started before the status leg closed. The order requires the whole-package comparison (298 entries) and the member read-backs against the build record's values, a start only on the issuer's message that L2 is closed, and a rollback whose first lines refuse before anything moves. NOT seen: the host (no ssh or SSM from the issuer) and the rollback's run on the host.
</preflight>
<decomp_ref>
<decomp_doc>org/missions/D9/IRPT/IRPT_ANLREQ/decompositions/IRPT_ANLREQ_DECOMP_R40A_Y.md</decomp_doc> round 40, workstream ZD: the apply of release 29, leg L4.
<owned_cells>AR-y-313</owned_cells>
</decomp_ref>

  <objective>
    Install the resident root 0485393f3a-r29 over the running 0485393f3a-r28 on host i-0167fd745ad906a66, and read it back. One host, one new root, three new keys. The root differs from r28 in exactly four of 299 members (pair section 3b): intake/uploads.py, ops/status.py, reports/resident_bindings.json (only provenance.package_pin) and SHA256SUMS; none added, none removed; the capture library and wrapper are NOT moved. NO removal leg: r29 stays unless V1 fails or the issuer orders the rollback.
    Files: C:/dev/irpt-release-r29/ and the scripts under org/missions/D9/IRPT/IRPT_ANLREQ/deliverables/0.9.0_WK_IRPT_ANLREQ~125/r39/.
  </objective>

  <context>Load /cloud-ops first. The same shape as IRPT_ANLREQ.TO-APPLY-R28b (read it: org/tier2_senior/0.7.0_AE_CloudOps~YC2/task_orders/IRPT_ANLREQ.TO-APPLY-R28b.resident-release-28-yc2.md and its output under deliverables/irpt_anlreq_r28/), with these differences: the old root is r28 (not r19); the host script is the release-29 one (its diff against release 28 is in r39/diff_host_r28_to_r29.txt); the scripts are those of AR-y-311, which print the expected values next to what they read. You submit no request and sign in as nobody. Nothing in this order starts a job or a capture.
  Signed pair: COO half org/missions/D9/IRPT/IRPT_ANLREQ/deliverables/2.0.0_SA_COO~Y2/release29/NEVER_WIDEN_PAIR_ANLREQ_RELEASE29_ORDINARY_VIEWER_AND_SHARES_WORDS_THREE_LEG.md (git hash-object 5e8b3cbd95739fe8b9172329cc671d2ef7ea1aa8) and CTO half org/missions/D9/IRPT/IRPT_ANLREQ/deliverables/1.0.0_SA_CTO~DELL2/NEVER_WIDEN_ANLREQ_RELEASE29_ORDINARY_VIEWER_AND_SHARES_WORDS_CTO_HALF.md (@abbfe49feb, CTO msg 7591). A different COO blob voids both halves: STOP. Build record: org/missions/D9/IRPT/IRPT_ANLREQ/deliverables/0.9.0_WK_IRPT_ANLREQ~125/r39/RESIDENT_BUILD.json.</context>

  <the_act>
    GO: both halves are signed. Leg L2 is CLOSED (the applier 0.7.0_AE_CloudOps~AQ2 reported it and the issuer read irpt-status live at CodeSha256 yNpw441TP5aMGYuZqkHQAPjAiQJDEPk7q8kFeDiIRIg=, 363818 bytes, 2026-10-14T12:19:40Z); the order is PENDING and this is the GO. Start at step 1 and go on when it reads green (you read that CodeSha256 yourself, read-only, at step 1). Otherwise tell 2.0.0_SA_COO~Y2 and wait.
    1. Read the COO half and CTO half at HEAD; `git hash-object` of the COO half must print 5e8b3cbd95739fe8b9172329cc671d2ef7ea1aa8. `get-function irpt-status` CodeSha256 must be yNpw441TP5aMGYuZqkHQAPjAiQJDEPk7q8kFeDiIRIg= (read only). Anything else: STOP, report.
    2. U2: put three files under ec2/investor-reporting-ycharts/resident/ in bucket opal-313476888478-lambda-artifacts, each key 404 before the put, each read back with sha256 equal; a different sha256 is a STOP (a rebuilt file is a new pair):
       - irpt-resident-0485393f3a-r29.tar.gz = C:/dev/irpt-release-r29/irpt-resident-0485393f3a-r29.tar.gz, sha256 2de2adce622f8bb9bbd5ebc071e862446b056303c0d9ffd7d41b050bd17f51a4
       - resident_host_install_0485393f3a-r29.sh = org/missions/D9/IRPT/IRPT_ANLREQ/deliverables/0.9.0_WK_IRPT_ANLREQ~125/r39/resident_host_install_0485393f3a-r29.sh, sha256 5fd383f988c825bcedd9058cc5ecaa9f0c429dcc8ac7f3acb199ada46c78e14a
       - irpt-resident-0485393f3a-r29.package.SHA256SUMS = C:/dev/irpt-release-r29/irpt-resident-0485393f3a-r29.package.SHA256SUMS, sha256 eebbf8cf794deccc65002870b26bbf5f961c61bf1751c25ba081a05ea7fbcfe0
    3. Open ledger irpt-resident-r29-20261014 (the name the host script writes into its receipt; legs U2 P1 D2 V1) and commit it; read every live worktree's org/critical_paths/.open_deploys/ (git worktree list, then git -C <wt> ls-tree) first and print the denominator: another open entry naming this host or the resident root is a STOP (an open entry on irpt-ycharts-generate or on the Lambdas is printed and is not).
    4. P1: host_read.py org/missions/D9/IRPT/IRPT_ANLREQ/deliverables/0.9.0_WK_IRPT_ANLREQ~125/r39/pre_read_r29.sh (sha256 fe35e6d43ac20cc6ac62e8ef4b6daea8da20663ee0f9b11db693f26bdc31ec86). Expect: the r28 root running, the r29 root ABSENT, and FIVE lines printing PASS: `P1 STOP-READ PASS`, `P1 STOP-READ-2 PASS`, `P1 STOP-READ-3 PASS`, `P1 STOP-READ-4 PASS`, `P1 STOP-READ-5 PASS`. Any FAIL: install nothing, send 2.0.0_SA_COO~Y2 the output path, stop. Save the output as org/tier2_senior/0.7.0_AE_CloudOps~YC2/deliverables/irpt_anlreq_r29/P1_PRE_READ_R29.txt.
    5. D2+V1: when irpt-generation reads 0 visible and 0 in flight, host_read.py org/missions/D9/IRPT/IRPT_ANLREQ/deliverables/0.9.0_WK_IRPT_ANLREQ~125/r39/install_r29.sh (sha256 0fb4fb27f36ecb4ff3fa13b4c717013645f27215fd6abca67fcca7a7c8245c0e). Expect (the script prints each wanted value beside what it reads): running root 0485393f3a-r29, active, 0 tracebacks, polls at least 1; V1 P2 uploads.py f85e8c9bb5af6ceddc6ccd513e511368447966d21f805a09306ef8f3cda81494 and template_reader.py a61cd0c622f8dd54864b8f2415cbe9968c0287d28087ce703073c7e392c1fc35; READER_VERSION irpt-template-reader.r19.3; `V1 P2b` printing MATCH for every member and no MISMATCH; `V1 P3 sha256sum -c rc=0 lines not OK: 0 of 298 checked`; the producer, reader, packager, registry-port and calendar imports OK; `V1 P4 yfinance_check.py absent from the root: yes`; host library = bindings library = a1c2880169c5f7996cc7c5880e4fe36db90f0a2c1f5a1cd01e0d1d8153544841; host wrapper = bindings wrapper; the kept library copy reads a1c28801...; the rollback root 0485393f3a-r28 still present; NO SIGN-IN line 0. Any failure: the installer's own rollback to r28 (root and receipt) has already run: read it, then STOP and report. Save the output as org/tier2_senior/0.7.0_AE_CloudOps~YC2/deliverables/irpt_anlreq_r29/D2_V1_INSTALL_R29.txt.
    6. Report to 2.0.0_SA_COO~Y2 that V1 is closed, with the output paths and the running root; the L3 order waits for that message. Close the ledger at V1 green. Report every host send to 0.0.0_AB_MSTR~DELL2 after the fact.
    Not in this order, and not to be run without a new word from 2.0.0_SA_COO~Y2: org/missions/D9/IRPT/IRPT_ANLREQ/deliverables/0.9.0_WK_IRPT_ANLREQ~125/r39/rollback_r29.sh (sha256 bef517d522994dc0b6382fbd5291db20076428138843b1b74f42e5664ad3b87a), which puts the r28 root back and exits before moving anything if the rollback root, its receipt copy or the library is missing.
  </the_act>

  <bounds>
    Host i-0167fd745ad906a66 and three new keys under ec2/investor-reporting-ycharts/resident/. No IAM, Terraform, Lambda, queue, data or portal change. No secret read. No dead letter is received, redriven or deleted. Nothing is sent to Bloomberg. No request is submitted and no sign-in is attempted.
    Rollback: the installer's own, on a failed start; afterwards the rollback script above on the issuer's word, and only AFTER the Lambda irpt-ycharts-generate has been rolled back if its leg has run (a moved Lambda stores inputs the pinned resident may refuse).
  </bounds>

  <proof_of_spec>
Instance at `org/tier2_senior/0.7.0_AE_CloudOps~YC2/deliverables/irpt_anlreq_r29/IRPT_ANLREQ.TO-APPLY-R29b.resident-release-29-yc2.proof_of_spec.json`.
    <criterion id="R29b-AC1" cell_refs="AR-y-313">The pre-read passed all five STOPs before anything was installed.<invocation>grep -c -E '^P1 STOP-READ(-[2345])? PASS' org/tier2_senior/0.7.0_AE_CloudOps~YC2/deliverables/irpt_anlreq_r29/P1_PRE_READ_R29.txt</invocation><expect>^5$</expect></criterion>
    <criterion id="R29b-AC2" cell_refs="AR-y-313">V1 shows the host running r29 with the whole package equal.<invocation>grep -m1 -E 'V1 P3 sha256sum -c rc=0 lines not OK: 0 of 298 checked' org/tier2_senior/0.7.0_AE_CloudOps~YC2/deliverables/irpt_anlreq_r29/D2_V1_INSTALL_R29.txt</invocation><expect>0 of 298 checked</expect></criterion>
    <criterion id="R29b-AC3" cell_refs="AR-y-313">The ledger irpt-resident-r29-20261014 is CLOSED.<invocation>grep -m1 '^\*\*Status' org/critical_paths/change_management/*irpt-resident-r29-20261014_deploy_completion.md</invocation><expect>^\*\*Status:\*\* CLOSED</expect></criterion>
  </proof_of_spec>
</task_order>
# pipeline-override: an APPLY order to a tier-2 applier under a signed pair (not a worker cell); the cell AR-y-313 is the issuer's, as for TO-APPLY-R28b.
