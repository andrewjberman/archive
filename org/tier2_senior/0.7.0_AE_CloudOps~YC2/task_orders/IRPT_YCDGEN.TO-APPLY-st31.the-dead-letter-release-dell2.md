<task_order>
  <metadata>
    <id>IRPT_YCDGEN.TO-APPLY-st31.the-dead-letter-release-dell2</id>
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
comp-adversary: RUN -- package gate PASS in whole-tree mode against the running st30 (added 0, removed 0, changed 21, identical 273); the 21 moved members are listed and read in st31_release/CENSUS_ST31_AGAINST_ST30_20261011.md; NOT seen: any exercised path on the host, and three of four response-schema diffs line by line
</preflight>
<decomp_ref>
<decomp_doc>org/missions/D9/IRPT/IRPT_YCDGEN/decompositions/IRPT_YCDGEN_DECOMP_R12.md</decomp_doc>
<owned_cells>YCD-a-12</owned_cells>
<decomp_context>The dead-letter release. Pair: org/missions/D9/IRPT/IRPT_YCDGEN/deliverables/2.0.0_SA_COO~G2/st31_release/NEVER_WIDEN_PACKET_ST31.md (COO half) and the CTO half, at the hashes named in the_act.</decomp_context>
</decomp_ref>

  <objective>
    Install the resident root 19b02b2971-st31 over the running 37210c771a-st30 on host i-0167fd745ad906a66, and read it back.
    One host, one new root, one restart. NO removal leg: st31 stays unless V1 fails or the issuer orders X1. Scripts:
    org/missions/D9/IRPT/IRPT_YCDGEN/deliverables/2.0.0_SA_COO~G2/st31_release/. Artifacts: C:/dev/irpt-release-st31/.
  </objective>

  <context>Load /cloud-ops first. The same shape as TO-APPLY-st30. You submit no request and sign in as nobody. No binding is
  added. The vendor session is failing on this host (CTO msg 4917): nothing in this order starts a job.</context>

  <the_act>
    GO: both halves are signed at packet blob 8d68f341d2 @a61d835162 (COO half) and CTO half @bb5f7303b7, whose condition 1 is MET on st31_release/CONDITION1_PORTAL_READERS_AT_PROD_20261011.md @5643d0e811 (CTO msg 5016). Report every host send to 0.0.0_AB_MSTR~DELL2 after the fact.
    1. U2: put the tar 19b02b2971-st31.tar.gz (sha256 00532ad07e3e250b4a136b32585f4244ca25c6bf7108c850dc1af600118c4b99) as
       ec2/investor-reporting-ycharts/resident/irpt-resident-19b02b2971-st31.tar.gz, and
       resident_host_install_19b02b2971-st31.sh (sha256 40207530c2c2b547d4502bea56260291be2752160321ffa8dae6985e1c410c64) under
       the same prefix. Each key must be 404 before the put; read each back, sha256 equal. A different sha256 is a STOP:
       a rebuilt tar is a new pair.
    2. Open ledger irpt-resident-st31-20261011 (legs U2 P1 D2 V1) and commit it.
    3. P1: host_read.py pre_read.sh. Expect st30 running. THE STOP: the output must print `P1 STOP-READ PASS`. On
       `P1 STOP-READ FAIL`, install nothing, send 2.0.0_SA_COO~G2 the output path, and stop.
    4. D2+V1: when irpt-generation reads 0 visible and 0 in flight, host_read.py install_st31.sh. Expect: running root
       19b02b2971-st31, active, 0 tracebacks; allow list `("andrew@opalinvest.com",)`; producer_for svc = YCHARTS;
       `GENERATE_MAX_RECEIVES = 5`; READ_BACK_RELEASE_VISIBILITY_S = 390; ticket_package occurrences 0; both queue binding
       counts 0; the running process environment count 0. Any failure: the installer's own rollback to st30, then STOP
       and report.
    5. Tell 2.0.0_SA_COO~G2 that V1 is closed, with the output path. Close the ledger at V1 green.
    Not in this order, and not to be run without a new word from 2.0.0_SA_COO~G2: remove_st31_to_st30.sh (X1 + V2).
  </the_act>

  <bounds>
    Host i-0167fd745ad906a66 and two new keys under ec2/investor-reporting-ycharts/resident/. No IAM, Terraform, Lambda,
    queue, data or portal change. No secret read. No dead letter is received, redriven or deleted. Nothing is sent to
    Bloomberg. No request is submitted and no sign-in is attempted.
  </bounds>

  <proof_of_spec>
Instance at `org/tier2_senior/0.7.0_AE_CloudOps~YC2/deliverables/irpt_ycdgen_st31/IRPT_YCDGEN.TO-APPLY-st31.the-dead-letter-release-dell2.proof_of_spec.json`.
    <criterion id="AC1" cell_refs="YCD-a-12">The pre-read passed the STOP before anything was installed.<invocation>grep -c 'P1 STOP-READ PASS' org/tier2_senior/0.7.0_AE_CloudOps~YC2/deliverables/irpt_ycdgen_st31/P1_PRE_READ_20261011.txt</invocation><expect>^1$</expect></criterion>
    <criterion id="AC2" cell_refs="YCD-a-12">V1 shows the host running st31.<invocation>grep -m1 'V1 running root' org/tier2_senior/0.7.0_AE_CloudOps~YC2/deliverables/irpt_ycdgen_st31/D2_V1_INSTALL_20261011.txt</invocation><expect>19b02b2971-st31 active=active</expect></criterion>
    <criterion id="AC3" cell_refs="YCD-a-12">The ledger irpt-resident-st31-20261011 is CLOSED.<invocation>grep -m1 '^\*\*Status' org/critical_paths/change_management/*irpt-resident-st31-20261011_deploy_completion.md</invocation><expect>^\*\*Status:\*\* CLOSED</expect></criterion>
  </proof_of_spec>
</task_order>
