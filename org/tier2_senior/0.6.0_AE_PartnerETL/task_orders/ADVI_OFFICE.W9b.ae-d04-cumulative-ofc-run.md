<task_order>
  <metadata>
    <id>0.6.0_AE_PartnerETL-2026-04-14-office-w9b</id>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_to>0.6.0_AE_PartnerETL</issued_to>
    <date>2026-04-14</date>
    <status>staged</status>
    <project_code>ADVI_OFFICE</project_code>
  </metadata>

  <references>
    <ref type="prd">docs/architecture/ADVI_OFFICE_ADDENDUM.md</ref>
  </references>

  <dependencies>
    <dependency agent="0.4.0_DS_ClientPlatform"
                task="ADVI_OFFICE.W9a.ds-cumulative-chart-ofc-key"
                status="pending"
                description="DS commits D_04 change + uploads to S3. MCP GO signal triggers W9b."/>
  </dependencies>

  <objective>
    Run D_04 on QA runner to regenerate platinum/firm/cumulative_chart.json with
    the new ofc and nna_ofc keys. Verify OFC continuous AUA is live in the artifact.
    No portal deploy needed — frontend already handles data?.ofc once key exists.
  </objective>

  <context>
    D_04 is a pass-through/aggregation script. All upstream artifacts are already
    in S3 from today's QA run (D_00b, D_01, D_02, D_03 outputs present).
    Only D_04 needs to re-run to regenerate cumulative_chart.json.

    D_04 run time: ~10-15 minutes (20,476 platinum files). No heavy compute.
    QA runner: bd-gold-qa-runner (i-0090b823a4a0997e3, AutoShutdown=disabled).

    Wait for DS W9a MCP GO signal before starting.
  </context>

  <scope>
    Run D_04 only (not full --group D). Use SSM dispatch:
      aws ssm send-command ... --parameters 'commands=["cd /home/ec2-user/bd-gold && python D_04.client_portal_summary.py --upload"]'

    Verify: aws s3 cp s3://opal-data-bd/platinum/firm/cumulative_chart.json - |
      python -c "import sys,json; d=json.load(sys.stdin); print('ofc cats:', d.get('ofc',{}).get('categories','MISSING')); print('nna_ofc cats:', d.get('nna_ofc',{}).get('categories','MISSING'))"

    Expected: ofc.categories = ['Austin', 'Dallas', 'Los Angeles', ...] (10 offices)
              nna_ofc.categories = same 10 offices
  </scope>

  <compiler_tools_mandate>
    <phase name="before_run">
      Set context: printf "SERIAL=0.6.0_AE_PartnerETL\nTO_ID=ADVI_OFFICE.W9b\n" > .comp-graph/.agent_context
      <run>comp-pipescript deployed D_04.client_portal_summary.py</run>
      <expect>MATCH — DS W9a ETag on S3 must match before running</expect>
      <if_mismatch>Do not run. Contact DS to re-upload.</if_mismatch>
    </phase>
    <phase name="after_run">
      Spot-check cumulative_chart.json ofc + nna_ofc keys (commands above).
      Append to org/compiler-tools-log.md.
      MCP to 2.0.0_SA_COO: "W9b complete — cumulative_chart.json has ofc + nna_ofc. OFC continuous AUA live."
    </phase>
  </compiler_tools_mandate>

  <cross_domain_coordination>
    <shared_resource>s3://opal-data-bd/platinum/firm/cumulative_chart.json</shared_resource>
    <required_action>No concurrent D_04 runs. Confirm QA runner is idle before dispatching.</required_action>
  </cross_domain_coordination>

  <acceptance_criteria>
    1. D_04 run exits 0 on QA runner.
    2. platinum/firm/cumulative_chart.json contains ofc.categories with 10 offices.
    3. platinum/firm/cumulative_chart.json contains nna_ofc.categories with 10 offices.
    4. MCP to 2.0.0_SA_COO confirming W9b complete.
    5. Session log with compiler tools section.
  </acceptance_criteria>

  <deliverables>
    - D_04 QA run complete and verified.
    - cumulative_chart.json ofc + nna_ofc confirmed live.
    - MCP to COO.
    - Session log.
  </deliverables>
</task_order>
