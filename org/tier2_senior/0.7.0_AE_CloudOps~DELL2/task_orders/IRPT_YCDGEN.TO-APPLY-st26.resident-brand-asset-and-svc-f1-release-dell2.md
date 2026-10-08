<task_order>
  <metadata>
    <id>IRPT_YCDGEN.TO-APPLY-st26.resident-brand-asset-and-svc-f1-release-dell2</id>
    <issued_by>2.0.0_SA_COO~G2</issued_by>
    <issued_to>0.7.0_AE_CloudOps~DELL2</issued_to>
    <date>2026-10-08</date>
    <status>issued</status>
    <project_code>IRPT_YCDGEN</project_code>
  </metadata>
<risk>WORLD</risk>
<proof_genre>DEPLOY</proof_genre>
<preflight>
comp-schedule: DECLARED-NOT-APPLICABLE a resident package swap on one host; no schedule, trigger or EventBridge rule is added or read
comp-iam: DECLARED-NOT-APPLICABLE no IAM change; the host role's existing GetObject on the artifacts prefix is the fetch (measured by the st25 install, SSM 959fadc3)
comp-adversary: DECLARED-NOT-APPLICABLE the gap was measured by row IRPT_YCDGEN-D2-S3 and the cell proved by YCD-w-6's instance; the CTO half grades the pair
</preflight>
<decomp_ref>
<decomp_doc>org/missions/D9/IRPT/IRPT_YCDGEN/decompositions/IRPT_YCDGEN_DECOMP_R6M.md</decomp_doc>
<owned_cells>YCD-w-6</owned_cells>
<decomp_context>The release that ships cell YCD-w-6 (drained @f9bc693920) to the resident host, with svc on the Opal allow list for ONE
seat-driven F1 run (CTO~DELL2 msg 1876). The pair is f1_st26_release/NEVER_WIDEN_PACKET_F1_ST26.md.</decomp_context>
</decomp_ref>

  <objective>
    Install resident package st26 (= the running st24 + the Opal brand asset + svc on the allow list) on i-0167fd745ad906a66, read it back,
    hand 2.0.0_SA_COO~G2 the window for its one F1 run, then install the removal (back to st24) and read it back. Every script is already
    written in org/missions/D9/IRPT/IRPT_YCDGEN/deliverables/2.0.0_SA_COO~G2/f1_st26_release/.
  </objective>

  <context>
    Row IRPT_YCDGEN-D2-S3: the host has no brand asset, so every Opal-path Overview ends LayoutRefused. Ledger irpt-ycdgen-f1-svc-20261008
    (CLOSED) is the st25 precedent: same transport, same scripts, same lessons. The artifacts are built and gated at C:/dev/irpt-release-st26/ (G5 vs st24: added 2,
    changed 3, identical 264); this order stages them. Load /cloud-ops before any AWS act.
  </context>

  <the_act>
    GO: the CTO half signed (msg relayed by 2.0.0_SA_COO~G2) AND the laptop's F1 shell window open on i-0167fd745ad906a66 (asked through
    0.0.0_AB_MSTR~DELL2). Report EVERY host send to 0.0.0_AB_MSTR~DELL2 after the fact (document, host, purpose).
    1. U2: the two files are at C:/dev/irpt-release-st26/ (outside the repo; census beside them). Put
       ec2/investor-reporting-ycharts/resident/irpt-resident-26df2c7622-st26.tar.gz (sha256 06328304b64962de...) and
       resident_host_install_26df2c7622-st26.sh (sha256 d2abe0e831656a66...) into opal-313476888478-lambda-artifacts; both keys 404 first;
       read back by version, sha256 equal. Write the script's VersionId into install_st26.sh (VER=); the fetch is by key.
    2. Open ledger irpt-ycdgen-f1-st26-20261008 (.tools/deploy_ledger.py; legs U2 P1 D2 V1 F1 X1 V2) and commit it with its sentinel.
    3. P1: host_read.py pre_read.sh. Expect st24, Andrew only, queue 0/0.
    4. D2+V1: host_read.py install_st26.sh. Expect root 26df2c7622-st26, NRestarts 0, allow list (andrew, svc), producer_for svc=OPAL and
       other=YCHARTS, and load_brand resolving ycharts/research/brand/ in the RUNNING root with no brand env var. Any failure: the script's
       own rollback, then STOP and report.
    5. Tell 2.0.0_SA_COO~G2 V1 is closed. It asks the laptop for the svc secret-reader window and runs F1 (its leg, not yours).
    6. X1+V2: when 2.0.0_SA_COO~G2 says F1 is done AND irpt-generation reads 0/0 (never before: a retained svc message retried on st24 would go
       to YCHARTS), host_read.py remove_st26_to_st24.sh. Expect st24, Andrew only. Close the ledger; tell 0.0.0_AB_MSTR~DELL2 X1 is reached.
  </the_act>

  <bounds>
    Host i-0167fd745ad906a66 only; no IAM, Terraform, Lambda or portal change; no secret read (F1 is 2.0.0_SA_COO~G2's); no vendor call.
  </bounds>

  <proof_of_spec>
    <criterion id="AC1">The ledger irpt-ycdgen-f1-st26-20261008 is CLOSED with all seven legs proven (python .tools/deploy_ledger.py check).</criterion>
    <criterion id="AC2">V1's output shows load_brand resolving the packaged path from the running st26 root.</criterion>
    <criterion id="AC3">V2's output shows the host on 409e3066d1-st24 with the allow list Andrew only.</criterion>
  </proof_of_spec>
</task_order>
