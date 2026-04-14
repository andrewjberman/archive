<task_order>
  <metadata>
    <id>0.6.0_AE_PartnerETL-2026-04-13-office-w2</id>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_to>0.6.0_AE_PartnerETL</issued_to>
    <date>2026-04-13</date>
    <status>complete</status>
    <project_code>ADVI_OFFICE</project_code>
  </metadata>

  <references>
    <ref type="prd">docs/architecture/ADVI_OFFICE_PRD.md</ref>
    <ref type="source_dim">data/black_diamond/config/office_mapping/advisor_registry_lusha_office_bridge_clean.csv</ref>
  </references>

  <dependencies>
    <dependency agent="0.4.0_DS_ClientPlatform"
                task="ADVI_OFFICE.W1.ds-d01-d00b-ofc-view"
                status="pending"
                description="DS commits D_01 + D_00b to CLOUD + uploads to S3. MCP message signals W2 GO."/>
  </dependencies>

  <objective>
    1. Upload the advisor-office dim file to S3 (one-time; prerequisite for D_01 + D_00b runtime reads).
    2. Trigger D_00b + D_01 + D_04 on bd-gold-qa-runner; verify OFC keys in artifacts.
    3. Promote: trigger PROD gold run on bd-gold-layer-runner (via EventBridge).
    4. Verify platinum artifacts and MCP-message DE + COO on completion.
  </objective>

  <context>
    The dim file is already committed in the repo:
      data/black_diamond/config/office_mapping/advisor_registry_lusha_office_bridge_clean.csv

    It must be uploaded to S3 before D_01 or D_00b run (they read it from S3 at runtime):
      s3://opal-data-bd/gold/dimensions/dim_advisor_office.csv

    This is a one-time upload. Rerun policy: do NOT re-call Lusha for existing names.
    Only append rows for genuinely new advisor names (not in scope for this task).

    Run order on QA runner: D_00b first, then D_01, then D_04. D_00b and D_01 are
    independent of each other (both read from same upstream silver/parquet files),
    but D_04 must run after both (it pass-throughs both artifacts to platinum/).

    QA runner: bd-gold-qa-runner (i-0090b823a4a0997e3).
    PROD runner: bd-gold-layer-runner (EventBridge trigger only).

    S3 code sync: D_01 and D_00b have already been uploaded by DS (W1 deliverable).
    Before triggering, confirm code is at expected S3 path with:
      aws s3 ls s3://opal-data-bd/code/gold/ | grep -E "D_00b|D_01"
  </context>

  <compiler_tools_mandate>
    Phase 1 (before starting):
    - Confirm DS W1 MCP message received (commit hash + S3 upload).
    - `aws s3 ls s3://opal-data-bd/code/gold/ | grep -E "D_00b|D_01"` — confirm code uploaded.

    Phase 2 (after QA run, before PROD):
    - `aws s3 cp s3://opal-data-bd/gold/artifacts/partner_analytics/header_metrics_quarterly.json - | python -c "import sys,json; d=json.load(sys.stdin); print('ofc keys:', list(d.get('views',{}).get('ofc',{}).keys()))"` — verify ofc present with period keys.
    - `aws s3 cp s3://opal-data-bd/gold/artifacts/timeseries_chart.json - | python -c "import sys,json; d=json.load(sys.stdin); print('top keys:', [k for k in d if k.startswith('ofc') or k.startswith('nna_ofc')])"` — verify ofc + nna_ofc keys present.
    - Spot-check Austin segment: `sum(ofc.donut.segments.aua)` approximately == firm headline AUA.

    Phase 3 (after PROD run):
    - `aws s3 ls s3://opal-data-bd/platinum/firm/ | grep partner_analytics` — confirm timestamps updated.
    - `aws s3 cp s3://opal-data-bd/platinum/firm/partner_analytics_quarterly.json - | python -c "import sys,json; d=json.load(sys.stdin); print('ofc present:', 'ofc' in d.get('views',{}))"` — confirm ofc in platinum.
    - Append to `org/compiler-tools-log.md`.
    - MCP message to 0.4.0_DE_ClientPlatform: "ADVI_OFFICE W2 complete. OFC artifact live at platinum/firm/partner_analytics_quarterly.json and timeseries_chart.json. Proceed with W3."
    - MCP message to 2.0.0_SA_COO: same summary + whether any artifact anomaly found.
  </compiler_tools_mandate>

  <cross_domain_coordination>
    <shared_resource>s3://opal-data-bd/gold/dimensions/dim_advisor_office.csv</shared_resource>
    <shared_resource>s3://opal-data-bd/gold/artifacts/partner_analytics/header_metrics_{gran}.json</shared_resource>
    <shared_resource>s3://opal-data-bd/gold/artifacts/timeseries_chart.json</shared_resource>
    <shared_resource>s3://opal-data-bd/platinum/firm/partner_analytics_{gran}.json</shared_resource>
    <shared_resource>s3://opal-data-bd/platinum/firm/timeseries_chart.json</shared_resource>
    <also_in_to>ADVI_OFFICE.W1 (DS — upstream; W2 gates on W1 MCP GO signal)</also_in_to>
    <also_in_to>ADVI_OFFICE.W3 (DE — downstream; W3 gates on W2 PROD artifact live)</also_in_to>
    <required_action>
      Check whether ADVI_REBORN.W6-003 DS gold run is in-flight before triggering W2.
      W6-003 touches D_00c + D_04 (not D_01 or D_00b), so there is NO script conflict.
      However, if a gold run for W6-003 is actively in progress on the QA runner, wait
      for it to complete before starting W2 QA run to avoid overlapping SSM commands.
      Coordinate with 0.4.0_DS_ClientPlatform via MCP if needed.
    </required_action>
  </cross_domain_coordination>

  <acceptance_criteria>
    1. `s3://opal-data-bd/gold/dimensions/dim_advisor_office.csv` exists (upload confirmed).
    2. QA run: `partner_analytics_quarterly.json` contains `views.ofc` with >= 5 office segment keys.
    3. QA run: `timeseries_chart.json` contains top-level `ofc` key.
    4. PROD run: `platinum/firm/partner_analytics_quarterly.json` contains `views.ofc` (all 3 granularities).
    5. PROD run: `platinum/firm/timeseries_chart.json` contains top-level `ofc` key.
    6. MCP message sent to 0.4.0_DE_ClientPlatform and 2.0.0_SA_COO confirming W2 complete.
    7. Session log with artifact spot-check evidence.
  </acceptance_criteria>

  <scope>
    <files>
      <file action="upload_to_s3">data/black_diamond/config/office_mapping/advisor_registry_lusha_office_bridge_clean.csv
        -> s3://opal-data-bd/gold/dimensions/dim_advisor_office.csv</file>
    </files>
    <gold_run_order>
      1. D_00b (timeseries_chart.json)
      2. D_01 (partner_analytics artifacts)
      3. D_04 (platinum pass-through)
    </gold_run_order>
    <out_of_scope>
      Rerunning Lusha enrichment. Any changes to D_01 or D_00b scripts (DS W1 scope).
      Portal deploy (DT W4 scope).
    </out_of_scope>
  </scope>

  <deliverables>
    - Dim file uploaded to S3.
    - QA + PROD gold run complete and verified.
    - MCP messages to DE and COO.
    - Session log with compiler tools section.
  </deliverables>
</task_order>
