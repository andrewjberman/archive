<task_order>
  <metadata>
    <id>IRPT_YCDGEN.TO-APPLY-sr3.served-read-window-8-section-census-dell2</id>
    <issued_by>2.0.0_SA_COO~G2</issued_by>
    <issued_to>0.7.0_AE_CloudOps~YC2</issued_to>
    <date>2026-10-11</date>
    <status>complete</status>
    <project_code>IRPT_YCDGEN</project_code>
  </metadata>
<risk>WORLD</risk>
<proof_genre>DEPLOY</proof_genre>
<preflight>
comp-schedule: DECLARED-NOT-APPLICABLE -- two conditional row writes; no schedule, trigger or EventBridge rule is added or read
comp-iam: DECLARED-NOT-APPLICABLE -- no IAM change on dell2; the secret resource-policy ADD/REMOVE is the laptop executor's leg, routed by MSTR
comp-adversary: RUN -- CTO msg 3309; the same blast radius as st28 W1/W2 with no host send; the after-read STOP rule and the 30-minute bound are in the pair
</preflight>
<decomp_ref>
<decomp_doc>org/missions/D9/IRPT/IRPT_YCDGEN/decompositions/IRPT_YCDGEN_DECOMP_R7.md</decomp_doc>
<owned_cells>YCD-a-7</owned_cells>
<decomp_context>FWD-1's served read of REQ-5e4149d2. Pair: org/missions/D9/IRPT/IRPT_YCDGEN/deliverables/2.0.0_SA_COO~G2/r7/NEVER_WIDEN_PACKET_SERVED_READ_WINDOW.md.</decomp_context>
</decomp_ref>

  <objective>
    Two conditional writes on svc's PROFILE row, around one read-only owner read by 2.0.0_SA_COO~G2:
    W1 cottonwood -> 49financial, then W2 49financial -> cottonwood. Script:
    org/missions/D9/IRPT/IRPT_YCDGEN/deliverables/2.0.0_SA_COO~G2/st29_release/swap_svc_firm.py.
  </objective>

  <the_act>
    WINDOW 8 (issuer 2.0.0_SA_COO~G2, 2026-10-11): the same act as IRPT_YCDGEN.TO-APPLY-sr1 window 6, for the SECTION CENSUS
    of round 8 cell YCD-c-8 (CTO round-8 analysis @fe73849335 section 3 item 3): ONE read of REQ-5e4149d2's analysis-report
    sections. Blast radius and bounds are unchanged: ONE opal-users-v2 item. Save outputs as W1_SWAP_OUT_WINDOW8.txt and
    W2_SWAP_BACK_WINDOW8.txt in your deliverables folder. State the continuity claim on allowedFirmIds, not on updatedAt.
    START CONDITION: do NOT begin on receipt. Begin on 2.0.0_SA_COO~G2's GO naming this order, sent when the laptop secret
    ADD for window 8 is put.
    GO: the CTO half signed in the packet.
    1. Open ledger irpt-ycdgen-served-read-w8 (legs W1 S+ R W2 S-) and commit it.
    2. W1: python swap_svc_firm.py cottonwood 49financial, saving the output. Note the time T0. Tell 2.0.0_SA_COO~G2 that W1 is
       closed.
    3. W2: at 2.0.0_SA_COO~G2's "R done", or at T0 + 30 minutes, whichever comes first:
       python swap_svc_firm.py 49financial cottonwood, saving the output.
    4. After-read: svc's row reads cottonwood. Close the ledger once S- is confirmed by MSTR. If the after-read is not as expected:
       STOP, restore, and report to 1.0.0_SA_CTO~DELL2.
  </the_act>

  <bounds>ONE opal-users-v2 item (svc's allowedFirmIds). No host send, no IAM, and no secret read.</bounds>

  <proof_of_spec>
Instance at `org/tier2_senior/0.7.0_AE_CloudOps~YC2/deliverables/irpt_ycdgen_sr1/IRPT_YCDGEN.TO-APPLY-sr3.served-read-window-8-section-census-dell2.proof_of_spec.json`.
    <criterion id="AC1" cell_refs="YCD-a-7">The ledger irpt-ycdgen-served-read-w8 is CLOSED.<invocation>grep -m1 '^\*\*Status' org/critical_paths/change_management/*irpt-ycdgen-served-read-w8_deploy_completion.md</invocation><expect>^\*\*Status:\*\* CLOSED</expect></criterion>
    <criterion id="AC2" cell_refs="YCD-a-7">W2 shows svc back on cottonwood.<invocation>grep -m1 '^after:' org/tier2_senior/0.7.0_AE_CloudOps~YC2/deliverables/irpt_ycdgen_sr1/W2_SWAP_BACK_WINDOW8.txt</invocation><expect>'allowedFirmIds': 'cottonwood'</expect></criterion>
  </proof_of_spec>
</task_order>
