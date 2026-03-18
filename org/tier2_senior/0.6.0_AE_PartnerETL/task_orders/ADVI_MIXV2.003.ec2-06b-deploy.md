<task_order>
  <metadata>
    <id>0.4.0_DS_ClientPlatform-2026-03-17-003-ae-06b-deploy</id>
    <issued_by>0.4.0_DS_ClientPlatform</issued_by>
    <issued_to>0.6.0_AE_PartnerETL</issued_to>
    <date>2026-03-17</date>
    <status>in_progress</status>
    <project_code>ADVI_MIXV2</project_code>
  </metadata>

  <objective>
    Deploy the updated 06b_build_client_mix_timeseries.py to the bd-gold-layer-runner EC2
    instance and run it. Two separate commits are being deployed: the AP gate insurance fix
    (ADVI_MIXV2.001) and the firm + advisor mix period view aggregation (ADVI_MIXV2.002).
    Full deployment instructions are in docs/briefs/devops-brief-mixv2-001.md and
    docs/briefs/devops-brief-mixv2-002.md.
  </objective>

  <scope>
    <files>
      <file action="deploy">data/black_diamond/scripts/gold/06b_build_client_mix_timeseries.py</file>
      <file action="deploy">data/black_diamond/scripts/gold/insurance_accounts.json</file>
    </files>
  </scope>

  <requirements>
    <requirement id="1">
      DEPENDENCY: Do not begin until DS confirms ADVI_MIXV2.001 and ADVI_MIXV2.002 are
      both committed to CLOUD. Read docs/briefs/devops-brief-mixv2-001.md and
      docs/briefs/devops-brief-mixv2-002.md before executing.
    </requirement>

    <requirement id="2">
      Upload both files to S3 per the EC2 Code Deployment Standard:
        s3://opal-data-bd/code/gold/06b_build_client_mix_timeseries.py
        s3://opal-data-bd/code/gold/insurance_accounts.json
      EC2 pulls from S3 — do not push directly to the instance.
    </requirement>

    <requirement id="3">
      Run 06b in incremental mode first to validate the AP gate fix:
        python3 06b_build_client_mix_timeseries.py --upload --incremental
      Verify in output that insurance accounts are no longer excluded on dates they
      were previously gated. Check S3 for updated per-relationship JSONs for the
      insurance account_ids identified in the ADVI_MIXV2.001 diagnostic.
    </requirement>

    <requirement id="4">
      If incremental validation passes, run a FULL rebuild to regenerate all relationship
      JSONs and produce the new firm_mix_views.json and per-advisor mix.json artifacts:
        python3 06b_build_client_mix_timeseries.py --upload
      Expected runtime: 30-45 min on r6i.4xlarge.
    </requirement>

    <requirement id="5">
      Verify outputs in S3:
        - gold/firm_mix_views.json exists, has views.quarterly populated with realistic values
        - gold/advisors/{advisor_id}/mix.json exists for at least 10 advisors
        - Spot-check: one advisor JSON — views.quarterly should have end_date, total_aua, per-class values
        - Spot-check: firm_mix_views.json — pct values sum to ~1.0 per period
    </requirement>

    <requirement id="6">
      Register deployment per EC2_MANIFEST.json protocol using safe-ec2-deploy.sh.
    </requirement>
  </requirements>

  <acceptance_criteria>
    <criterion id="1">gold/firm_mix_views.json present in S3 with >=4 quarterly periods</criterion>
    <criterion id="2">gold/advisors/*/mix.json present for all active advisors</criterion>
    <criterion id="3">Per-relationship JSONs for insurance accounts now include dates previously gated</criterion>
    <criterion id="4">Deployment registered in EC2_MANIFEST.json</criterion>
  </acceptance_criteria>

  <constraints>
    <constraint>Follow EC2 Code Deployment Standard: write to S3, EC2 pulls, never inline scripts in SSM</constraint>
    <constraint>Run incremental validation BEFORE full rebuild — the incremental run is the smoke test</constraint>
  </constraints>

  <dependencies>
    <dependency agent="0.4.0_DS_ClientPlatform" task="ADVI_MIXV2.001" status="pending">
      DS must commit AP gate fix before AE deploys
    </dependency>
    <dependency agent="0.4.0_DS_ClientPlatform" task="ADVI_MIXV2.002" status="pending">
      DS must commit firm/advisor aggregation before AE deploys
    </dependency>
  </dependencies>

  <deliverables>
    <deliverable type="document">EC2_MANIFEST.json updated with deploy record</deliverable>
    <deliverable type="document">Session log confirming S3 artifact presence and spot-check results</deliverable>
  </deliverables>
</task_order>
