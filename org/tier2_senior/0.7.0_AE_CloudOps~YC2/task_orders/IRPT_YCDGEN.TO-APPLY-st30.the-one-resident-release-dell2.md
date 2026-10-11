<task_order>
  <metadata>
    <id>IRPT_YCDGEN.TO-APPLY-st30.the-one-resident-release-dell2</id>
    <issued_by>2.0.0_SA_COO~G2</issued_by>
    <issued_to>0.7.0_AE_CloudOps~YC2</issued_to>
    <date>2026-10-11</date>
    <status>complete</status>
    <project_code>IRPT_YCDGEN</project_code>
  </metadata>
<risk>WORLD</risk>
<proof_genre>DEPLOY</proof_genre>
<preflight>
comp-schedule: DECLARED-NOT-APPLICABLE -- a resident package swap; no schedule, trigger or EventBridge rule is added or read
comp-iam: DECLARED-NOT-APPLICABLE -- no IAM change; the host fetch is by key as in st26-st29
comp-adversary: RUN -- package gate PASS against the running st27 (added 25, removed 0, changed 61, identical 208); census parts 1 and 2 read every loadable diff; 0 of 294 members under performance/
</preflight>
<decomp_ref>
<decomp_doc>org/missions/D9/IRPT/IRPT_YCDGEN/decompositions/IRPT_YCDGEN_DECOMP_R10.md</decomp_doc>
<owned_cells>YCD-d-10</owned_cells>
<decomp_context>The one resident release. Pair: org/missions/D9/IRPT/IRPT_YCDGEN/deliverables/2.0.0_SA_COO~G2/st30_release/NEVER_WIDEN_PACKET_ST30.md (COO half) and org/missions/D9/IRPT/IRPT_YCDGEN/deliverables/1.0.0_SA_CTO~DELL2/NEVER_WIDEN_RESIDENT_ST30_CTO_HALF.md (CTO half), at the hashes named in the_act.</decomp_context>
</decomp_ref>

  <objective>
    Install the resident root 37210c771a-st30 over the running e606008994-st27 on host i-0167fd745ad906a66, and read it back.
    One host, one new root, one restart. There is NO removal leg in this order: st30 stays unless V1 fails or the issuer
    orders X1. Scripts: org/missions/D9/IRPT/IRPT_YCDGEN/deliverables/2.0.0_SA_COO~G2/st30_release/. Artifacts:
    C:/dev/irpt-release-st30/.
  </objective>

  <context>Load /cloud-ops first. Same shape as TO-APPLY-st29's legs U2, P1, D2, V1, without its F1, X1, W2. You submit no
  request and sign in as nobody. The svc profile is not touched.</context>

  <the_act>
    GO: both halves are signed at packet blob f81df64584 @b0c75d2f04 (COO half) and CTO half @e2346b95f8 (CTO msg 4690). Report every host send to 0.0.0_AB_MSTR~DELL2 after the fact.
    1. U2: put the tar 37210c771a-st30.tar.gz (sha256 e5a6b6251b0e5e971cf73d785770965d4c2f407a6b4d79286508b50a853da241) as
       ec2/investor-reporting-ycharts/resident/irpt-resident-37210c771a-st30.tar.gz, and
       resident_host_install_37210c771a-st30.sh (sha256 dd85725806894839bd46fc66d990ba195f966862015a2983bb7bbbef0964b969) under
       the same prefix. Each key must be 404 before the put; read each back, sha256 equal. A different sha256 is a STOP:
       a rebuilt tar is a new pair.
    2. Open ledger irpt-resident-st30-20261011 (legs U2 P1 D2 V1) and commit it.
    3. P1: host_read.py pre_read.sh. Expect st27 running. THE STOP: the output must print `P1 STOP-READ PASS`
       (IRPT_ANALYSIS_READY_QUEUE_URL reads 0 in the unit Environment, the running process and the unit files). On
       `P1 STOP-READ FAIL`, install nothing, send 2.0.0_SA_COO~G2 the output path, and stop.
    4. D2+V1: when irpt-generation reads 0 visible and 0 in flight, host_read.py install_st30.sh. Expect: running root
       37210c771a-st30, active, 0 tracebacks; allow list `("andrew@opalinvest.com",)`; producer_for svc = YCHARTS;
       packaged research row firms = 3; request schema names ticket_id; READ_BACK_RELEASE_VISIBILITY_S = 390; both queue
       binding counts 0; the running process environment count 0. Any failure: the installer's own rollback to st27,
       then STOP and report.
    5. Tell 2.0.0_SA_COO~G2 that V1 is closed, with the output path. Close the ledger at V1 green.
    Not in this order, and not to be run without a new word from 2.0.0_SA_COO~G2: remove_st30_to_st27.sh (X1 + V2).
  </the_act>

  <bounds>
    Host i-0167fd745ad906a66 and two new keys under ec2/investor-reporting-ycharts/resident/. No IAM, Terraform, Lambda,
    queue, data or portal change. No secret read. No dead letter is received, redriven or deleted. Nothing is sent to
    Bloomberg. No request is submitted.
  </bounds>

  <proof_of_spec>
Instance at `org/tier2_senior/0.7.0_AE_CloudOps~YC2/deliverables/irpt_ycdgen_st30/IRPT_YCDGEN.TO-APPLY-st30.the-one-resident-release-dell2.proof_of_spec.json`.
    <criterion id="AC1" cell_refs="YCD-d-10">The pre-read passed the STOP before anything was installed.<invocation>grep -c 'P1 STOP-READ PASS' org/tier2_senior/0.7.0_AE_CloudOps~YC2/deliverables/irpt_ycdgen_st30/P1_PRE_READ_20261011.txt</invocation><expect>^1$</expect></criterion>
    <criterion id="AC2" cell_refs="YCD-d-10">V1 shows the host running st30.<invocation>grep -m1 'V1 running root' org/tier2_senior/0.7.0_AE_CloudOps~YC2/deliverables/irpt_ycdgen_st30/D2_V1_INSTALL_20261011.txt</invocation><expect>37210c771a-st30 active=active</expect></criterion>
    <criterion id="AC3" cell_refs="YCD-d-10">The ledger irpt-resident-st30-20261011 is CLOSED.<invocation>grep -m1 '^\*\*Status' org/critical_paths/change_management/*irpt-resident-st30-20261011_deploy_completion.md</invocation><expect>^\*\*Status:\*\* CLOSED</expect></criterion>
  </proof_of_spec>
</task_order>
