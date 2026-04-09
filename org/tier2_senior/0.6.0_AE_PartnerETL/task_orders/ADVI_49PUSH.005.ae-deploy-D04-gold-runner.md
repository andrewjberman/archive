<task_order>
  <metadata>
    <id>2.0.0_SA_COO-2026-04-08-49push-005-ae</id>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_to>0.6.0_AE_PartnerETL</issued_to>
    <date>2026-04-08</date>
    <status>pending</status>
    <project_code>ADVI_49PUSH</project_code>
    <wave>2</wave>
    <phase>P1</phase>
  </metadata>

  <objective>
    Deploy D_04.client_portal_summary.py to the bd-gold-layer-runner EC2 instance (c6i.16xlarge),
    add it to the dispatch chain, and execute a full gold run to populate the platinum/ prefix
    in opal-data-bd.
  </objective>

  <context>
    D_04 is the new platinum layer publisher written by DS in Wave 1 (ADVI_49PUSH.001).
    File: data/black_diamond/scripts/gold/D_04.client_portal_summary.py (880 lines, py_compile clean).

    It reads gold/ outputs from D_00, D_02, D_03, C_06, C_08, B_01, A_02 and writes
    ~5,300 pre-sliced JSON files to platinum/ in S3 (opal-data-bd bucket).

    Chain position: D_04 goes AFTER D_03 as the final script in CHAIN_DOWNSTREAM.
    Catalog entry: D_04|D_04.client_portal_summary.py|--upload

    PRD: docs/architecture/ADVI_49PUSH_P1_PRD.md (sections: D_04 Script Design, Dispatch Chain)
  </context>

  <requirements>
    <requirement id="1">
      py_compile gate: Run py_compile on D_04.client_portal_summary.py BEFORE uploading
      to the gold runner. This is mandatory per feedback rule (compile before upload).
    </requirement>

    <requirement id="2">
      Upload D_04 to gold runner via safe-ec2-deploy.sh or the S3 artifact path.
      Follow EC2_CODE_DEPLOYMENT_STANDARD.md (S3 artifact model).
    </requirement>

    <requirement id="3">
      Update gold_dispatch.sh:
      - Add D_04 to CHAIN_DOWNSTREAM after D_03
      - Add catalog entry: D_04|D_04.client_portal_summary.py|--upload
      - Upload updated gold_dispatch.sh to gold runner
    </requirement>

    <requirement id="4">
      Execute a full gold run (CHAIN_FULL or CHAIN_DOWNSTREAM) on bd-gold-layer-runner.
      Verify D_04 runs successfully and produces platinum/ files in S3.
    </requirement>

    <requirement id="5">
      Verify platinum/ prefix exists in opal-data-bd with expected file structure:
      - platinum/firm/dashboard.json
      - platinum/firm/mix_summary.json
      - platinum/advisors/{id}/summary.json (check at least 3 exist)
      - platinum/clients/{rel_id}/summary.json (check at least 10 exist)
      - platinum/clients/{rel_id}/mix_timeseries.json
      - platinum/clients/{rel_id}/concentration.json
      - platinum/accounts/{acct_id}/summary.json (check at least 10 exist)
    </requirement>

    <requirement id="6">
      SINGLE COMMAND DISCIPLINE: Do not run overlapping SSM commands on the gold runner.
      One command at a time. Wait for completion before issuing the next.
    </requirement>
  </requirements>

  <deliverables>
    <deliverable>D_04 deployed and running on bd-gold-layer-runner</deliverable>
    <deliverable>gold_dispatch.sh updated with D_04 in CHAIN_DOWNSTREAM</deliverable>
    <deliverable>platinum/ files verified in opal-data-bd S3</deliverable>
    <deliverable>Message to COO (2.0.0_SA_COO) confirming deploy complete + file counts</deliverable>
  </deliverables>

  <do_not>
    <rule>Do NOT run D_04 in isolation -- run the full chain so upstream gold/ inputs are fresh</rule>
    <rule>Do NOT modify D_04 code -- if it fails, report to DS (~A) for fix</rule>
    <rule>Do NOT use emojis in any SSM commands or logs</rule>
  </do_not>
</task_order>
