<task_order>
  <metadata>
    <id>IRPT_ANLREQ.TO-APPLY-R19a.resident-reader-release-yc2</id>
    <issued_by>2.0.0_SA_COO~Y2</issued_by>
    <issued_to>0.7.0_AE_CloudOps~YC2</issued_to>
    <date>2026-10-13</date>
    <status>pending</status>
    <project_code>IRPT_ANLREQ</project_code>
  </metadata>
<risk>WORLD</risk>
<proof_genre>DEPLOY</proof_genre>
<placeholders>NONE</placeholders>
<preflight>
comp-blast: DECLARED-NOT-APPLICABLE -- the blast radius is named, per key, in the signed pair (section 3a and 4).
comp-routes: DECLARED-NOT-APPLICABLE -- no route is added or changed. comp-cache: DECLARED-NOT-APPLICABLE. comp-schedule: DECLARED-NOT-APPLICABLE -- a resident package swap; no schedule, trigger or EventBridge rule is added or read.
comp-iam: DECLARED-NOT-APPLICABLE -- no IAM change; the host fetch is by key as in st26 to st32.
comp-adversary: RUN -- by reading the st32 apply order and its V1 output against this cell; the lens: a read-back that proves the new members and says nothing about the 294 that must not move, or a rollback that has never run. The order adds a whole-package comparison of the running root to the package's own sums and a rollback script whose first lines refuse before anything moves. NOT seen: the host (no ssh or SSM from the issuer) and the rollback's run on the host.
</preflight>
<decomp_ref>
<decomp_doc>org/missions/D9/IRPT/IRPT_ANLREQ/decompositions/IRPT_ANLREQ_DECOMP_R19A_Y.md</decomp_doc> round 8, workstream YR: the resident leg of the reader's release.
<owned_cells>AR-y-205</owned_cells>
</decomp_ref>

  <objective>
    Install the resident root 0485393f3a-r19 over the running 0485393f3a-st32 on host i-0167fd745ad906a66, and read it back. One host, one new root, three new keys. The root differs from st32 in exactly two reader members
    (intake/uploads.py, intake/template_reader.py), the generated bindings and the sums; the capture library and wrapper are NOT moved. NO removal leg: r19 stays unless V1 fails or the issuer orders X1.
    Files: C:/dev/irpt-release-r19/ and the scripts under org/missions/D9/IRPT/IRPT_ANLREQ/deliverables/2.0.0_SA_COO~Y2/release19/.
  </objective>

  <context>Load /cloud-ops first. The same shape as IRPT_YCDGEN.TO-APPLY-st32, with these differences: the host script is a 17-line copy of st32's (NEW, OLD, WANT_TAR and labels); the library is reinstalled with the SAME bytes; a second signed file (the package's own
  sums) is fetched so V1 can compare the running root with the whole package. You submit no request and sign in as nobody. Nothing in this order starts a job or a capture.
  Signed pair: COO half org/missions/D9/IRPT/IRPT_ANLREQ/deliverables/2.0.0_SA_COO~Y2/release19/NEVER_WIDEN_PAIR_ANLREQ_RELEASE19_READER_TWO_LEG.md (git hash-object 2140b9352cf527e6984106a876eccc095bd7452f) and CTO half org/missions/D9/IRPT/IRPT_ANLREQ/deliverables/1.0.0_SA_CTO~DELL2/NEVER_WIDEN_ANLREQ_RELEASE19_READER_TWO_LEG_CTO_HALF.md (@6facbbb2d3, CTO msg 6802). A different COO blob voids both halves: STOP.</context>

  <the_act>
    GO: both halves are signed. You start ONLY when (a) step 1 reads green and (b) the issuer's result of TO-READS-Y10 is in the tree, read within the last 60 minutes, with turned_back 0 (otherwise tell 2.0.0_SA_COO~Y2 and wait).
    1. Read the COO half and CTO half at HEAD; `git hash-object` of the COO half must print 2140b9352cf527e6984106a876eccc095bd7452f. Read the Lambda: `get-function irpt-ycharts-generate` CodeSha256 must be NeAB50CNXWvM5Y6nsba220QmsEiASbVbXcZVRYe4MUM= (R0b; the Lambda is IB2's, you only read it). Anything else: STOP, report.
    2. U2: put three files under ec2/investor-reporting-ycharts/resident/ in bucket opal-313476888478-lambda-artifacts, each key 404 before the put, each read back with sha256 equal; a different sha256 is a STOP (a rebuilt file is a new pair):
       - irpt-resident-0485393f3a-r19.tar.gz = C:/dev/irpt-release-r19/irpt-resident-0485393f3a-r19.tar.gz, sha256 84df6479655c07ae6000af40404e53eb056b4c403aa9134bbe9c1521317d497a
       - resident_host_install_0485393f3a-r19.sh = org/missions/D9/IRPT/IRPT_ANLREQ/deliverables/2.0.0_SA_COO~Y2/release19/resident_host_install_0485393f3a-r19.sh, sha256 8b53be1328f9ed20827e0118aee9c1b1b402d66b25d82a434275b1c83cfa57f0
       - irpt-resident-0485393f3a-r19.package.SHA256SUMS = C:/dev/irpt-release-r19/irpt-resident-0485393f3a-r19.package.SHA256SUMS, sha256 a3dea4ec9afe05db66db96e8110064e70a6ba7ea50e4d04038cdee301ddfa933
    3. Open ledger irpt-resident-r19-20261013 (legs U2 P1 D2 V1) and commit it; read every live worktree's org/critical_paths/.open_deploys/ (git worktree list, then git -C <wt> ls-tree) first and print the denominator: another open entry naming this host or the resident root is a STOP.
    4. P1: host_read.py org/missions/D9/IRPT/IRPT_ANLREQ/deliverables/2.0.0_SA_COO~Y2/release19/pre_read_r19.sh (sha256 1f18704fc80e32203a66726e77d396253c39434b65e0f3b69eab39f6a7517ee2). Expect: the st32 root running, and FIVE lines printing PASS: `P1 STOP-READ PASS`, `P1 STOP-READ-2 PASS`, `P1 STOP-READ-3 PASS`, `P1 STOP-READ-4 PASS`, `P1 STOP-READ-5 PASS`; the reader members read 47f89e0b46609c5b... and 76795b75313b0764... with 0 READER_VERSION lines. Any FAIL: install nothing, send 2.0.0_SA_COO~Y2 the output path, stop.
    5. D2+V1: when irpt-generation reads 0 visible and 0 in flight, host_read.py org/missions/D9/IRPT/IRPT_ANLREQ/deliverables/2.0.0_SA_COO~Y2/release19/install_r19.sh (sha256 4cc2b0fedec699ff078629d534a6ebb06af6d13f85c84e6e9b98344b50fbf6ab). Expect (the pair's P1 to P4): running root 0485393f3a-r19, active, 0 tracebacks, polls at least 1;
       uploads.py 176682cb1545435eec084376b3c37a578ca70d05f9ad5a376c0f2275f62b05ea and template_reader.py 83ab9b45d59065f53c640803df9fd07a0ddfcc97d89c13540c20622a6bf7bd58; READER_VERSION irpt-template-reader.r18.1;
       `V1 P3 sha256sum -c rc=0 lines not OK: 0 of 297 checked`; producer and reader import OK; host library = bindings library = a1c2880169c5f7996cc7c5880e4fe36db90f0a2c1f5a1cd01e0d1d8153544841; host wrapper = bindings wrapper;
       the kept library copy reads a1c28801...; the rollback root still present; NO SIGN-IN line 0. Any failure: the installer's own rollback to st32 (root and receipt) has already run: read it, then STOP and report.
    6. Report to 2.0.0_SA_COO~Y2 that V1 is closed, with the output path and the running root; the Lambda leg waits for that message. Close the ledger at V1 green. Report every host send to 0.0.0_AB_MSTR~DELL2 after the fact.
    Not in this order, and not to be run without a new word from 2.0.0_SA_COO~Y2: org/missions/D9/IRPT/IRPT_ANLREQ/deliverables/2.0.0_SA_COO~Y2/release19/rollback_r19.sh (sha256 2687b1a1ec14f8f5c636518632acba737482b62c0e38f8c632de32c2a4b9c2fa), which puts the st32 root back and exits before moving anything if the rollback root, its receipt copy or the st32 library is missing.
  </the_act>

  <bounds>
    Host i-0167fd745ad906a66 and three new keys under ec2/investor-reporting-ycharts/resident/. No IAM, Terraform, Lambda, queue, data or portal change. No secret read. No dead letter is received, redriven or deleted. Nothing is sent to Bloomberg. No request is submitted and no sign-in is attempted.
    Rollback: the installer's own, on a failed start; afterwards the X1 script above on the issuer's word, and only AFTER the Lambda has been rolled back if the Lambda leg has run (a moved Lambda stores inputs the pinned resident refuses).
  </bounds>

  <proof_of_spec>
Instance at `org/tier2_senior/0.7.0_AE_CloudOps~YC2/deliverables/irpt_anlreq_r19/IRPT_ANLREQ.TO-APPLY-R19a.resident-reader-release-yc2.proof_of_spec.json`.
    <criterion id="R19a-AC1" cell_refs="AR-y-205">The pre-read passed all five STOPs before anything was installed.<invocation>grep -c -E '^P1 STOP-READ(-[2345])? PASS' org/tier2_senior/0.7.0_AE_CloudOps~YC2/deliverables/irpt_anlreq_r19/P1_PRE_READ_R19.txt</invocation><expect>^5$</expect></criterion>
    <criterion id="R19a-AC2" cell_refs="AR-y-205">V1 shows the host running r19 with the whole package equal.<invocation>grep -m1 -E 'V1 P3 sha256sum -c rc=0 lines not OK: 0 of 297 checked' org/tier2_senior/0.7.0_AE_CloudOps~YC2/deliverables/irpt_anlreq_r19/D2_V1_INSTALL_R19.txt</invocation><expect>0 of 297 checked</expect></criterion>
    <criterion id="R19a-AC3" cell_refs="AR-y-205">The ledger irpt-resident-r19-20261013 is CLOSED.<invocation>grep -m1 '^\*\*Status' org/critical_paths/change_management/*irpt-resident-r19-20261013_deploy_completion.md</invocation><expect>^\*\*Status:\*\* CLOSED</expect></criterion>
  </proof_of_spec>
</task_order>
# pipeline-override: an APPLY order to a tier-2 applier under a signed pair (not a worker cell); the cell AR-y-205 is the issuer's, as for TO-APPLY-R13b.
