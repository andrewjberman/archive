<task_order>
  <metadata>
    <id>0.4.0_DS_ClientPlatform-2026-04-14-office-w9a</id>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_to>0.4.0_DS_ClientPlatform</issued_to>
    <date>2026-04-14</date>
    <status>complete</status>
    <project_code>ADVI_OFFICE</project_code>
  </metadata>

  <references>
    <ref type="prd">docs/architecture/ADVI_OFFICE_ADDENDUM.md</ref>
    <ref type="diagnosis">DE message 20260414T163020Z — getPlatinumCumulativeChart reads cumulative_chart.json, ofc key missing</ref>
  </references>

  <objective>
    Add ofc and nna_ofc keys to platinum/firm/cumulative_chart.json so the OFC
    Continuous AUA chart renders in the portal. 10-line addition to D_04.
  </objective>

  <context>
    Root cause (confirmed by COO code read):
    D_04.client_portal_summary.py build_cumulative_chart() (line 1519) reads
    timeseries_chart.json and extracts geo/adv/nna_geo/nna_adv explicitly.
    It does NOT extract ofc or nna_ofc. The data exists in timeseries_chart.json
    (ofc.data: 2,291 rows, 10 offices — confirmed by DS W5 verification).

    The portal's getPlatinumCumulativeChart() reads platinum/firm/cumulative_chart.json.
    Once ofc is present, data?.ofc resolves and the stacked area chart renders
    automatically — no portal code changes needed (DE already wired it).

    No DT portal deploy needed after this change — pure data-side fix.
  </context>

  <scope>
    <file>data/black_diamond/scripts/gold/D_04.client_portal_summary.py</file>
    <change>
      In build_cumulative_chart() at the top-level views extraction block
      (currently lines ~1542-1572), add alongside geo/adv/nna_geo/nna_adv:

        ofc = ts_chart.get('ofc', {})
        nna_ofc = ts_chart.get('nna_ofc', {})

      And in the chart dict:

        'ofc': {
            'description': ofc.get('description', ''),
            'categories': ofc.get('categories', []),
            'data': _weekly_downsample(ofc.get('data', [])),
        },
        'nna_ofc': {
            'description': nna_ofc.get('description', ''),
            'categories': nna_ofc.get('categories', []),
            'data': _weekly_downsample(nna_ofc.get('data', [])),
        },

      Follow the exact same pattern as geo/adv (lines 1553-1572).
      No other changes needed — _weekly_downsample handles the data correctly.
    </change>
  </scope>

  <compiler_tools_mandate>
    <phase name="before_write">
      Set context: printf "SERIAL=0.4.0_DS_ClientPlatform\nTO_ID=ADVI_OFFICE.W9a\n" > .comp-graph/.agent_context
      <run>comp-pipescript io D_04.client_portal_summary.py</run>
      <expect>cumulative_chart.json in WRITES list; timeseries_chart.json in READS list</expect>
    </phase>
    <phase name="before_commit">
      <run>py_compile data/black_diamond/scripts/gold/D_04.client_portal_summary.py</run>
      <expect>No syntax errors</expect>
    </phase>
    <phase name="after_s3_upload">
      Spot-check: python -c "import boto3,json; d=json.loads(boto3.client('s3').get_object(Bucket='opal-data-bd',Key='code/gold/D_04.client_portal_summary.py')['Body'].read()); print('ok')" (confirm ETag)
    </phase>
  </compiler_tools_mandate>

  <cross_domain_coordination>
    <shared_resource>s3://opal-data-bd/platinum/firm/cumulative_chart.json</shared_resource>
    <also_in_to>ADVI_OFFICE.W9b (AE — runs D_04 after this commit)</also_in_to>
    <required_action>
      After committing and uploading to S3, MCP-message 0.6.0_AE_PartnerETL
      with subject "W9a complete — D_04 ready for W9b run" and include the S3 ETag.
      Also MCP-message 2.0.0_SA_COO.
    </required_action>
  </cross_domain_coordination>

  <acceptance_criteria>
    1. D_04.client_portal_summary.py build_cumulative_chart() emits ofc and nna_ofc keys.
    2. py_compile passes (no syntax errors).
    3. D_04 uploaded to S3 — ETag confirmed.
    4. MCP messages to AE 0.6.0 (W9b GO) and COO.
    5. Session log with compiler tools section.
  </acceptance_criteria>

  <deliverables>
    - D_04.client_portal_summary.py modified and committed to CLOUD.
    - D_04 uploaded to s3://opal-data-bd/code/gold/D_04.client_portal_summary.py.
    - MCP to 0.6.0_AE_PartnerETL (W9b GO) and 2.0.0_SA_COO.
    - Session log.
  </deliverables>
</task_order>
