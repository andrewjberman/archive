<task_order>
  <metadata>
    <id>IRPT_YCDGEN.TO-APPLY-st27.resident-brand-asset-release-dell2</id>
    <issued_by>2.0.0_SA_COO~G2</issued_by>
    <issued_to>0.7.0_AE_CloudOps~DELL2</issued_to>
    <date>2026-10-09</date>
    **AMENDMENT 2026-10-09 (2.0.0_SA_COO~G2, issuer):** the three criteria carry cell_refs="YCD-w-6" and a literal
<invocation>/<expect> each, read against the evidence files this order's applier already committed (0.7.0_AE_CloudOps~DELL2 msg 2260:
the prose criteria had no cell_refs and no evaluable expect). Wording and meaning unchanged. Gate limb: none graded this modification.

<status>complete</status>
    <project_code>IRPT_YCDGEN</project_code>
  </metadata>
<risk>WORLD</risk>
<proof_genre>DEPLOY</proof_genre>
<preflight>
comp-schedule: DECLARED-NOT-APPLICABLE a resident package swap on one host; no schedule, trigger or EventBridge rule is added or read
comp-iam: DECLARED-NOT-APPLICABLE no IAM change; the host role's GetObject on the artifacts prefix is the fetch (st26 D2, SSM 7f6d5a0a)
comp-adversary: DECLARED-NOT-APPLICABLE the gap was measured by row IRPT_YCDGEN-D2-S3 and the fix proved on the host by st26 V1 @ffd85b8e7c
</preflight>
<decomp_ref>
<decomp_doc>org/missions/D9/IRPT/IRPT_YCDGEN/decompositions/IRPT_YCDGEN_DECOMP_R6M.md</decomp_doc>
<owned_cells>YCD-w-6</owned_cells>
<decomp_context>The release that ships cell YCD-w-6 to the resident host as the live package (CTO~DELL2 msg 2118): st24 + the brand asset,
allow list Andrew-only. The pair is org/missions/D9/IRPT/IRPT_YCDGEN/deliverables/2.0.0_SA_COO~G2/st27_release/NEVER_WIDEN_PACKET_ST27.md.</decomp_context>
</decomp_ref>

  <objective>
    Install resident package st27 (= the running st24 + the Opal brand asset; allow list unchanged, Andrew only) on i-0167fd745ad906a66 and
    read it back. st27 STAYS LIVE: no removal leg. Scripts: org/missions/D9/IRPT/IRPT_YCDGEN/deliverables/2.0.0_SA_COO~G2/st27_release/.
  </objective>

  <context>
    The same shape as your IRPT_YCDGEN.TO-APPLY-st26 (closed 7/7 @70403dcfaa), minus svc and the F1/X1 legs. The artifacts are built and gated at
    C:/dev/irpt-release-st27/ (outside the repo; census beside them; G5 vs st24: added 2, changed 2, identical 265). Load /cloud-ops first.
  </context>

  <the_act>
    GO: the CTO half signed (relayed by 2.0.0_SA_COO~G2) AND the laptop's shell window open for this ledger (asked through
    0.0.0_AB_MSTR~DELL2 on your "ready for send (1)"). Report EVERY host send to 0.0.0_AB_MSTR~DELL2 after the fact (document, host, purpose).
    1. U2: put ec2/investor-reporting-ycharts/resident/irpt-resident-e606008994-st27.tar.gz (sha256 20916261074c356a...) and
       resident_host_install_e606008994-st27.sh (sha256 64a817c58c66ebd1...) into opal-313476888478-lambda-artifacts; both keys 404 first; read
       back by version, sha256 equal. Your VER-filled copy of install_st27.sh lives in your own deliverables (lane), as for st26.
    2. Open ledger irpt-ycdgen-st27-20261009 (legs U2 P1 D2 V1) and commit it with its sentinel.
    3. P1: host_read.py pre_read.sh. Expect st24, Andrew only, queue 0/0.
    4. D2+V1: host_read.py install_st27.sh. Expect root e606008994-st27, NRestarts 0, allow list Andrew only, load_brand resolving
       ycharts/research/brand/ in the RUNNING root with no brand env var. A fall-back or any failure: the script's own rollback (or
       remove_st27_to_st24.sh at queue 0/0), then STOP and report. On V1 PASS close the ledger and tell 2.0.0_SA_COO~G2 and
       0.0.0_AB_MSTR~DELL2 (so the laptop closes the shell window).
  </the_act>

  <bounds>
    Host i-0167fd745ad906a66 only; no IAM, Terraform, Lambda or portal change; no secret read; no vendor call.
  </bounds>

  <proof_of_spec>
Instance at `org/tier2_senior/0.7.0_AE_CloudOps~DELL2/deliverables/irpt_ycdgen_st27/IRPT_YCDGEN.TO-APPLY-st27.proof_of_spec.json`.
    <criterion id="AC1" cell_refs="YCD-w-6">Ledger irpt-ycdgen-st27-20261009 CLOSED with U2 P1 D2 V1 proven.<invocation>grep -m1 '^\*\*Status' org/critical_paths/change_management/20261009T0222Z_irpt-ycdgen-st27-20261009_deploy_completion.md</invocation><expect>^\*\*Status:\*\* CLOSED</expect></criterion>
    <criterion id="AC2" cell_refs="YCD-w-6">V1's output shows load_brand resolving the packaged path from the running e606008994-st27 root, env brand vars [].<invocation>grep -m1 'V1 brand from the RUNNING root' org/tier2_senior/0.7.0_AE_CloudOps~DELL2/deliverables/irpt_ycdgen_st27/D2_V1_INSTALL_20261009.txt</invocation><expect>e606008994-st27/ycharts/research/brand/brand\.json .*env brand vars \[\]$</expect></criterion>
    <criterion id="AC3" cell_refs="YCD-w-6">V1's output shows the allow list Andrew only.<invocation>grep -m1 'V1 allow list' org/tier2_senior/0.7.0_AE_CloudOps~DELL2/deliverables/irpt_ycdgen_st27/D2_V1_INSTALL_20261009.txt</invocation><expect>OPAL_PRODUCER_PRINCIPALS = \("andrew@opalinvest\.com",\)$</expect></criterion>
  </proof_of_spec>
</task_order>
