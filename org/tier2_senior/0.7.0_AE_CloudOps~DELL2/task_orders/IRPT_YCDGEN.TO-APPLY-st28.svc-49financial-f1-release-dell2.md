<task_order>
  <metadata>
    <id>IRPT_YCDGEN.TO-APPLY-st28.svc-49financial-f1-release-dell2</id>
    <issued_by>2.0.0_SA_COO~G2</issued_by>
    <issued_to>0.7.0_AE_CloudOps~DELL2</issued_to>
    <date>2026-10-09</date>
    <status>issued</status>
    <project_code>IRPT_YCDGEN</project_code>
  </metadata>
<risk>WORLD</risk>
<proof_genre>DEPLOY</proof_genre>
<preflight>
comp-schedule: DECLARED-NOT-APPLICABLE a resident package swap and one profile-row write; no schedule, trigger or EventBridge rule is added or read
comp-iam: DECLARED-NOT-APPLICABLE no IAM change; the host fetch is by key (st26/st27); the row write is dell2's existing DynamoDB access to opal-users-v2
comp-adversary: DECLARED-NOT-APPLICABLE ruled by 1.0.0_SA_CTO~DELL2 (msgs 2111, 2148) on the measured E5 gap (rows D2-S3, D2-S4, D2-W8-S1)
</preflight>
<decomp_ref>
<decomp_doc>org/missions/D9/IRPT/IRPT_YCDGEN/decompositions/IRPT_YCDGEN_DECOMP_R6M.md</decomp_doc>
<owned_cells>YCD-w-6</owned_cells>
<decomp_context>The seat-driven arm of FWD-1 on the live brand asset (YCD-w-6, st27): st28 adds svc to the allow list for ONE F1 run on
49financial (CTO~DELL2 msg 2148). The pair is org/missions/D9/IRPT/IRPT_YCDGEN/deliverables/2.0.0_SA_COO~G2/st28_release/NEVER_WIDEN_PACKET_F1_ST28.md.</decomp_context>
</decomp_ref>

  <objective>
    Install st28 (= the live st27 + svc on the allow list), swap svc's allowedFirmIds cottonwood -> 49financial, hand 2.0.0_SA_COO~G2 its F1
    window, then remove st28 back to st27 and swap svc back. Scripts in org/missions/D9/IRPT/IRPT_YCDGEN/deliverables/2.0.0_SA_COO~G2/st28_release/.
  </objective>

  <context>
    Same shape as your IRPT_YCDGEN.TO-APPLY-st26 (closed 7/7) plus one profile-row write. Artifacts gated at C:/dev/irpt-release-st28/
    (G5 vs the running st27: changed 2, identical 267). Load /cloud-ops first.
  </context>

  <the_act>
    GO: the CTO half signed (relayed by 2.0.0_SA_COO~G2) AND the laptop's shell window open for this ledger (dell2's standing shell access,
    if landed, replaces the ask). Report EVERY host send and the row write to 0.0.0_AB_MSTR~DELL2 after the fact.
    1. U2: put irpt-resident-b7ad601c58-st28.tar.gz (sha256 8a96f07e9510d69d...) and resident_host_install_b7ad601c58-st28.sh (sha256
       47f17df385d05c14...) into opal-313476888478-lambda-artifacts under ec2/investor-reporting-ycharts/resident/; both keys 404 first; read
       back by version, sha256 equal. Your VER-filled copy of install_st28.sh lives in your own deliverables.
    2. Open ledger irpt-ycdgen-f1-st28-20261009 (legs U2 P1 D2 V1 W1 F1 X1 V2 W2) and commit it with its sentinel.
    3. P1: host_read.py pre_read.sh. Expect st27, Andrew only, queue 0/0.
    4. D2+V1: host_read.py install_st28.sh. Expect root b7ad601c58-st28, allow list (andrew, svc), producer_for svc=OPAL, load_brand from the
       RUNNING root with no env. Any failure: the script's own rollback to st27, then STOP.
    5. W1: python swap_svc_firm.py cottonwood 49financial. Expect after: allowedFirmIds 49financial. Tell 2.0.0_SA_COO~G2 V1 and W1 are closed.
    6. X1+V2 when 2.0.0_SA_COO~G2 says F1 is done (or ends) AND irpt-generation reads 0/0: remove_st28_to_st27.sh. Expect st27, Andrew only.
    7. W2: python swap_svc_firm.py 49financial cottonwood. Close the ledger; tell 0.0.0_AB_MSTR~DELL2 X1 is reached.
  </the_act>

  <bounds>
    Host i-0167fd745ad906a66 and ONE opal-users-v2 item (svc's PROFILE row, allowedFirmIds only); no IAM, Terraform, Lambda or portal change;
    no secret read (F1 is 2.0.0_SA_COO~G2's); no vendor call.
  </bounds>

  <proof_of_spec>
Instance at `org/tier2_senior/0.7.0_AE_CloudOps~DELL2/deliverables/irpt_ycdgen_st28/IRPT_YCDGEN.TO-APPLY-st28.svc-49financial-f1-release-dell2.proof_of_spec.json`.
    <criterion id="AC1" cell_refs="YCD-w-6">The ledger irpt-ycdgen-f1-st28-20261009 is CLOSED.<invocation>grep -m1 '^\*\*Status' org/critical_paths/change_management/*irpt-ycdgen-f1-st28-20261009_deploy_completion.md</invocation><expect>^\*\*Status:\*\* CLOSED</expect></criterion>
    <criterion id="AC2" cell_refs="YCD-w-6">V2 shows the host back on st27 with the allow list Andrew only.<invocation>grep -m1 'V2 allow list' org/tier2_senior/0.7.0_AE_CloudOps~DELL2/deliverables/irpt_ycdgen_st28/X1_V2_REMOVAL_20261009.txt</invocation><expect>OPAL_PRODUCER_PRINCIPALS = \("andrew@opalinvest\.com",\)$</expect></criterion>
    <criterion id="AC3" cell_refs="YCD-w-6">W2 shows svc back on cottonwood.<invocation>grep -m1 '^after:' org/tier2_senior/0.7.0_AE_CloudOps~DELL2/deliverables/irpt_ycdgen_st28/W2_SWAP_BACK_20261009.txt</invocation><expect>'allowedFirmIds': 'cottonwood'</expect></criterion>
  </proof_of_spec>
</task_order>
