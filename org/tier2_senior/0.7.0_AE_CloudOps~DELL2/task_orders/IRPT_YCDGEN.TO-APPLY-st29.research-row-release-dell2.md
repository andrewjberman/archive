<task_order>
  <metadata>
    <id>IRPT_YCDGEN.TO-APPLY-st29.research-row-release-dell2</id>
    <issued_by>2.0.0_SA_COO~G2</issued_by>
    <issued_to>0.7.0_AE_CloudOps~DELL2</issued_to>
    <date>2026-10-09</date>
    <status>complete</status>
    <project_code>IRPT_YCDGEN</project_code>
  </metadata>
<risk>WORLD</risk>
<proof_genre>DEPLOY</proof_genre>
<preflight>
comp-schedule: DECLARED-NOT-APPLICABLE -- a resident package swap; no schedule, trigger or EventBridge rule is added or read
comp-iam: DECLARED-NOT-APPLICABLE -- no IAM change; round 7's roles were applied under TO-APPLY-r7 @0617cb243d; the host fetch is by key as in st26-st28
comp-adversary: RUN -- the RetentionRefused cause was read from the st28 tar (research row firms ['cottonwood']); gate PASS against the running st28 (changed 2, identical 267)
</preflight>
<decomp_ref>
<decomp_doc>org/missions/D9/IRPT/IRPT_YCDGEN/decompositions/IRPT_YCDGEN_DECOMP_R7.md</decomp_doc>
<owned_cells>YCD-a-7</owned_cells>
<decomp_context>The release of YCD-a-7's registry row to the resident host, and the F1 re-run. Pair: org/missions/D9/IRPT/IRPT_YCDGEN/deliverables/2.0.0_SA_COO~G2/st29_release/NEVER_WIDEN_PACKET_ST29.md.</decomp_context>
</decomp_ref>

  <objective>
    Install st29 (st28 plus the round-7 research row) on the resident host, hand 2.0.0_SA_COO~G2 its F1 re-run, then remove st29
    straight to st27 and swap svc back to cottonwood. This supersedes TO-APPLY-st28's X1, V2 and W2. Scripts are in
    org/missions/D9/IRPT/IRPT_YCDGEN/deliverables/2.0.0_SA_COO~G2/st29_release/; artifacts are at C:/dev/irpt-release-st29/.
  </objective>

  <context>Load /cloud-ops first. Same shape as TO-APPLY-st28. The CTO's hard bound is 13:09:10Z (msg 3063).</context>

  <the_act>
    GO: the CTO half signed in the packet. Report every host send to 0.0.0_AB_MSTR~DELL2 after the fact.
    1. U2: put the tar (sha256 3bf984a8f752dfbf...) and resident_host_install_f0ff4f1653-st29.sh (sha256 9ea64ae53fd81aca...) under
       ec2/investor-reporting-ycharts/resident/. Each key must be 404 before the put; read each back by version, sha equal.
    2. Open ledger irpt-ycdgen-f1-st29-20261009 (legs U2 P1 D2 V1 F1 X1 V2 W2) and commit it.
    3. P1: host_read.py pre_read.sh. Expect st28 running and the st27 root present.
    4. D2+V1: when irpt-generation reads 0/0, host_read.py install_st29.sh. Expect root f0ff4f1653-st29, producer_for svc=OPAL, and
       the packaged research row firms = 3. Any failure: the script's own rollback to st28, then STOP.
    5. Tell 2.0.0_SA_COO~G2 that V1 is closed.
    6. X1+V2 at the EARLIER of my "F1 done" or 13:09:10Z, at 0/0: remove_st29_to_st27.sh. Expect st27, with Andrew only.
    7. W2: python swap_svc_firm.py 49financial cottonwood. Close this ledger, and close irpt-ycdgen-f1-st28-20261009 as SUPERSEDED by
       this X1/W2. Tell 0.0.0_AB_MSTR~DELL2 that X1 is reached.
  </the_act>

  <bounds>
    Host i-0167fd745ad906a66 and ONE opal-users-v2 item (svc's PROFILE allowedFirmIds, W2 only). No IAM, Terraform, Lambda or
    portal change, and no secret read.
  </bounds>

  <proof_of_spec>
Instance at `org/tier2_senior/0.7.0_AE_CloudOps~DELL2/deliverables/irpt_ycdgen_st29/IRPT_YCDGEN.TO-APPLY-st29.research-row-release-dell2.proof_of_spec.json`.
    <criterion id="AC1" cell_refs="YCD-a-7">The ledger irpt-ycdgen-f1-st29-20261009 is CLOSED.<invocation>grep -m1 '^\*\*Status' org/critical_paths/change_management/*irpt-ycdgen-f1-st29-20261009_deploy_completion.md</invocation><expect>^\*\*Status:\*\* CLOSED</expect></criterion>
    <criterion id="AC2" cell_refs="YCD-a-7">V2 shows the host back on st27 with the allow list Andrew only.<invocation>grep -m1 'V2 allow list' org/tier2_senior/0.7.0_AE_CloudOps~DELL2/deliverables/irpt_ycdgen_st29/X1_V2_REMOVAL_20261009.txt</invocation><expect>OPAL_PRODUCER_PRINCIPALS = \("andrew@opalinvest\.com",\)$</expect></criterion>
    <criterion id="AC3" cell_refs="YCD-a-7">W2 shows svc back on cottonwood.<invocation>grep -m1 '^after:' org/tier2_senior/0.7.0_AE_CloudOps~DELL2/deliverables/irpt_ycdgen_st29/W2_SWAP_BACK_20261009.txt</invocation><expect>'allowedFirmIds': 'cottonwood'</expect></criterion>
  </proof_of_spec>
</task_order>
