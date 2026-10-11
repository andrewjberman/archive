<task_order>
  <metadata>
    <id>IRPT_YCDGEN.TO-APPLY-st32.the-capture-diagnosis-release-dell2</id>
    <issued_by>2.0.0_SA_COO~G2</issued_by>
    <issued_to>0.7.0_AE_CloudOps~YC2</issued_to>
    <date>2026-10-11</date>
    <status>pending</status>
    <project_code>IRPT_YCDGEN</project_code>
  </metadata>
<risk>WORLD</risk>
<proof_genre>DEPLOY</proof_genre>
<preflight>
comp-schedule: DECLARED-NOT-APPLICABLE -- a resident package swap; no schedule, trigger or EventBridge rule is added or read
comp-iam: DECLARED-NOT-APPLICABLE -- no IAM change; the host fetch is by key as in st26-st31
comp-adversary: RUN -- package gate PASS in whole-tree mode against the running st31 (added 3, removed 0, changed 17, identical 277); the 17 changed and 3 added members are listed and read in st32_release/CENSUS_ST32_AGAINST_ST31_20261011.md; NOT seen: any exercised path on the host, host_capture.py and lib/opal_naming.py line by line, and the rollback's library step, which has never run
</preflight>
<decomp_ref>
<decomp_doc>org/missions/D9/IRPT/IRPT_YCDGEN/decompositions/IRPT_YCDGEN_DECOMP_R13.md</decomp_doc>
<owned_cells>YCD-d-13</owned_cells>
<decomp_context>The capture-diagnosis release. Pair: org/missions/D9/IRPT/IRPT_YCDGEN/deliverables/2.0.0_SA_COO~G2/st32_release/NEVER_WIDEN_PACKET_ST32.md (COO half) and the CTO half, at the hashes named in the_act.</decomp_context>
</decomp_ref>

  <objective>
    Install the resident root 0485393f3a-st32 over the running 19b02b2971-st31 on host i-0167fd745ad906a66, and read it back.
    One host, one new root, ONE HOST FILE (the capture library), one restart. NO removal leg: st32 stays unless V1 fails or
    the issuer orders X1. Scripts: org/missions/D9/IRPT/IRPT_YCDGEN/deliverables/2.0.0_SA_COO~G2/st32_release/. Artifacts:
    C:/dev/irpt-release-st32/.
  </objective>

  <context>Load /cloud-ops first. The same shape as TO-APPLY-st31, with one difference: the installer also replaces
  /opt/investor-reporting-ycharts/ycharts_session.js and keeps the old file beside it. You submit no request and sign in as
  nobody. No binding is added. The first sign-in after this release is a later act on the CTO's word; nothing in this order
  starts a job or a capture.</context>

  <the_act>
    GO: both halves are signed: COO half at packet blob 57f962a8b3 (@1e356e0f3d) and CTO half blob 6d3c6df8f5 (@b511482612, CTO msg 5268), with two conditions; condition 1 is steps 3 and 4 below, condition 2 is not yours. Report every host send to 0.0.0_AB_MSTR~DELL2 after the fact.
    1. U2: put the tar 0485393f3a-st32.tar.gz (sha256 e59596e4d731a89c0349dd28d36d34eaafa4d1237e43e36a598bd40b36a34f1e) as
       ec2/investor-reporting-ycharts/resident/irpt-resident-0485393f3a-st32.tar.gz, and
       resident_host_install_0485393f3a-st32.sh (sha256 05b0cfba8b8948a6573ef9e4b3a1d538939ebf4d54a3761af797c77712878adf) under
       the same prefix. Each key must be 404 before the put; read each back, sha256 equal. A different sha256 is a STOP:
       a rebuilt tar is a new pair.
    2. Open ledger irpt-resident-st32-20261011 (legs U2 P1 D2 V1) and commit it.
    3. P1: host_read.py pre_read.sh. Expect st31 running. THREE STOPS, each must print PASS: `P1 STOP-READ PASS` (the unit
       carries no IRPT_ANALYSIS_READY_QUEUE_URL), `P1 STOP-READ-2 PASS` (the host library is st31's,
       857d90b81960d69a7a6700be6fffe33d86628694aef95f8cfb64aca7a82cb839), `P1 STOP-READ-3 PASS` (the kept-copy path does
       not already exist). On any FAIL, install nothing, send 2.0.0_SA_COO~G2 the output path, and stop.
    4. D2+V1: when irpt-generation reads 0 visible and 0 in flight, host_read.py install_st32.sh. Expect: running root
       0485393f3a-st32, active, 0 tracebacks; allow list `("andrew@opalinvest.com",)`; producer_for svc = YCHARTS;
       host library = bindings library = a1c2880169c5f7996cc7c5880e4fe36db90f0a2c1f5a1cd01e0d1d8153544841; host wrapper =
       bindings wrapper; `V1 old library kept for rollback` prints 857d90b81960d69a7a6700be6fffe33d86628694aef95f8cfb64aca7a82cb839;
       cause_claim measured occurrences 1; the NO SIGN-IN line reads 0 journal lines and 0 children; packager key 0; both
       queue binding counts 0; the running process environment count 0. Any failure: the installer's own rollback to st31
       (root, receipt AND library), then STOP and report. A capture, eviction or session-refresh line in V1 is a failure.
    5. Tell 2.0.0_SA_COO~G2 that V1 is closed, with the output path. Close the ledger at V1 green.
    Not in this order, and not to be run without a new word from 2.0.0_SA_COO~G2: remove_st32_to_st31.sh (X1 + V2). If it
    is ever ordered and it cannot find the kept library at st31's sha256 it exits before moving anything: report that.
  </the_act>

  <bounds>
    Host i-0167fd745ad906a66 and two new keys under ec2/investor-reporting-ycharts/resident/. No IAM, Terraform, Lambda,
    queue, data or portal change. No secret read. No dead letter is received, redriven or deleted. Nothing is sent to
    Bloomberg. No request is submitted and no sign-in is attempted.
  </bounds>

  <proof_of_spec>
Instance at `org/tier2_senior/0.7.0_AE_CloudOps~YC2/deliverables/irpt_ycdgen_st32/IRPT_YCDGEN.TO-APPLY-st32.the-capture-diagnosis-release-dell2.proof_of_spec.json`.
    <criterion id="AC1" cell_refs="YCD-d-13">The pre-read passed all three STOPs before anything was installed.<invocation>grep -c -E '^P1 STOP-READ(-[23])? PASS' org/tier2_senior/0.7.0_AE_CloudOps~YC2/deliverables/irpt_ycdgen_st32/P1_PRE_READ_20261011.txt</invocation><expect>^3$</expect></criterion>
    <criterion id="AC2" cell_refs="YCD-d-13">V1 shows the host running st32.<invocation>grep -m1 'V1 running root' org/tier2_senior/0.7.0_AE_CloudOps~YC2/deliverables/irpt_ycdgen_st32/D2_V1_INSTALL_20261011.txt</invocation><expect>0485393f3a-st32 active=active</expect></criterion>
    <criterion id="AC3" cell_refs="YCD-d-13">The ledger irpt-resident-st32-20261011 is CLOSED.<invocation>grep -m1 '^\*\*Status' org/critical_paths/change_management/*irpt-resident-st32-20261011_deploy_completion.md</invocation><expect>^\*\*Status:\*\* CLOSED</expect></criterion>
  </proof_of_spec>
</task_order>
