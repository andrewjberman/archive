<task_order>
  <metadata>
    <id>2.0.0_SA_COO-2026-03-18-mvp318-003-ae</id>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_to>0.6.0_AE_PartnerETL</issued_to>
    <date>2026-03-18</date>
    <status>pending</status>
    <project_code>ADVI_MVP318</project_code>
  </metadata>

  <objective>
    Run ONE FULL gold layer on bd-gold-layer-runner after DT completes Lambda deploys.
    This single run consolidates three pending workstreams: ADVI_ADVTV2.002 (architect
    attribution), ADVI_MIXV2.003 (06b AP gate + firm/advisor mix), and WS5 (MTD/QTD/YTD
    windows from script 10). The gold layer run triggers bd-portal-publisher and
    bd-portal-advisor-publisher at completion — those Lambdas MUST be on their new versions
    (WS2+WS3b) before this run completes, or the new advisor timeseries artifacts will not
    be generated.
  </objective>

  <context>
    Reference:
    - docs/architecture/ADVI_MVP318_PRD.md §WS5
    - org/tier2_senior/0.6.0_AE_PartnerETL/task_orders/ADVI_MIXV2.003.ec2-06b-deploy.md
    - org/tier2_senior/0.4.0_DT_ClientPlatform/task_orders/ADVI_ADVTV2.002.gold-layer-deploy.md
    - docs/deployment/EC2_CODE_DEPLOYMENT_STANDARD.md (repo -> S3 -> EC2 pulls, never inline scripts)

    Scripts that are deployed (already on EC2 from prior sessions per git log):
    - 08b_build_architect_attribution.py (ADVI_ADVTV2, deployed @ 72c03d2a)
    - 06b_build_client_mix_timeseries.py + insurance_accounts.json (ADVI_MIXV2.003, in_progress)

    Script that DS will commit for WS5 (pending DS ADVI_MVP318.001):
    - data/black_diamond/scripts/gold/generate_advisor_rolling_flows.py (script 10)
    - Possibly generate_partner_analytics.py (script 09) — DS will confirm

    This is a FULL mode run, not incremental. FULL is required because 00_build_accounts_dimension.py
    now ingests consultant and additional_advisor from silver transactions (08b dependency).
    Expected runtime: 60-90 min.
  </context>

  <scope>
    <files>
      <file action="upload-to-s3">data/black_diamond/scripts/gold/generate_advisor_rolling_flows.py</file>
      <file action="upload-to-s3-if-changed">data/black_diamond/scripts/gold/generate_partner_analytics.py</file>
      <file action="run-on-ec2">run_gold_layer.sh --full</file>
    </files>
  </scope>

  <requirements>
    <requirement id="1" priority="gate">
      HARD GATE: Do not run the gold layer until DT confirms bd-portal-advisor-publisher deploy is complete
      (ADVI_MVP318.002 req 3). The gold layer's final step writes pipeline-complete.json, which triggers
      both publisher Lambdas. If the old Lambda code is active at that moment, advisor timeseries artifacts
      will not be generated. DT's deploy is the gate; wait for explicit DT confirmation.
    </requirement>

    <requirement id="2">
      Wait for DS to confirm generate_advisor_rolling_flows.py (script 10) is committed to CLOUD.
      Check: git log --oneline -- data/black_diamond/scripts/gold/generate_advisor_rolling_flows.py
      If DS also committed generate_partner_analytics.py (script 09), include it in the S3 upload.
      Do not upload uncommitted code to S3.
    </requirement>

    <requirement id="3">
      Upload all DS-committed WS5 scripts to S3 per the EC2 Code Deployment Standard:
        aws s3 cp data/black_diamond/scripts/gold/generate_advisor_rolling_flows.py \
          s3://opal-data-bd/code/gold/generate_advisor_rolling_flows.py
      If script 09 also changed:
        aws s3 cp data/black_diamond/scripts/gold/generate_partner_analytics.py \
          s3://opal-data-bd/code/gold/generate_partner_analytics.py
      Do not write code directly to EC2. S3 is the artifact store; EC2 pulls from S3.
    </requirement>

    <requirement id="4">
      On bd-gold-layer-runner EC2, pull the updated WS5 scripts from S3 (SSM or SSH):
        aws s3 cp s3://opal-data-bd/code/gold/generate_advisor_rolling_flows.py \
          ~/bd-gold/data/black_diamond/scripts/gold/generate_advisor_rolling_flows.py
      (If script 09 also updated, pull it too.)
      Do NOT inline script content in SSM commands.
    </requirement>

    <requirement id="5">
      Run the FULL gold layer:
        ./run_gold_layer.sh --full
      Expected runtime: 60-90 min. Monitor for errors. If the run fails at a specific script,
      report the failure script and stdout/stderr to COO before retrying.
    </requirement>

    <requirement id="6">
      After run completes, verify three sets of acceptance criteria:

      ADVI_ADVTV2 criteria (architect attribution):
      - rel_architect_lookup.parquet contains exactly 19 named architects + Unresolved
      - No "49F House", "Unassigned", or stale architects
        aws s3 cp s3://opal-data-bd/gold/views/rel_architect_lookup.parquet /tmp/ &amp;&amp; \
        python3 -c "import pandas as pd; df=pd.read_parquet('/tmp/rel_architect_lookup.parquet'); \
          print(df['resolved_architect'].nunique(), 'architects'); print(df['resolved_architect'].unique())"

      ADVI_MIXV2 criteria (firm/advisor mix):
      - gold/firm_mix_views.json exists with &gt;=4 quarterly periods
      - gold/advisors/*/mix.json exists for at least 10 advisors
      - pct values in firm_mix_views.json sum to ~1.0 per period

      WS5 criteria (advisor timeseries artifacts from new Lambda):
      - gold/advisors/{advisor_id}/timeseries.json exists for at least one advisor
        (generated by the new Lambda after pipeline-complete.json trigger)
      - gold/advisors/{advisor_id}/mix_timeseries.json exists for at least one advisor
      NOTE: Lambda-generated artifacts only appear after pipeline-complete.json is written
      AND the Lambda runs successfully. If artifacts are missing, confirm pipeline-complete.json
      was written and check CloudWatch logs for bd-portal-advisor-publisher invocation.
    </requirement>

    <requirement id="7">
      Register the deployment in EC2_MANIFEST.json per the safe-ec2-deploy.sh protocol.
      The entry should cover the WS5 script 10 upload (and script 09 if applicable).
    </requirement>
  </requirements>

  <acceptance_criteria>
    <criterion id="1">DT bd-portal-advisor-publisher deploy confirmed before gold run starts</criterion>
    <criterion id="2">Script 10 (and 09 if changed) uploaded to S3 from committed CLOUD code</criterion>
    <criterion id="3">FULL gold layer completes without errors (all scripts 00 through 10)</criterion>
    <criterion id="4">rel_architect_lookup.parquet: 19 named architects + Unresolved</criterion>
    <criterion id="5">firm_mix_views.json present with &gt;=4 quarterly periods; pct sums ~1.0</criterion>
    <criterion id="6">Advisor timeseries and mix_timeseries JSON artifacts generated in S3</criterion>
    <criterion id="7">EC2_MANIFEST.json updated with deployment record</criterion>
  </acceptance_criteria>

  <constraints>
    <constraint>Do NOT start the gold layer run until DT confirms Lambda deploy is complete</constraint>
    <constraint>Do NOT upload uncommitted code to S3 — verify DS commit first</constraint>
    <constraint>FULL mode only — incremental mode will not backfill architect attribution</constraint>
    <constraint>Never write code directly to EC2 — repo -> S3 -> EC2 pull (EC2_CODE_DEPLOYMENT_STANDARD.md)</constraint>
    <constraint>No emojis in any SSM commands, scripts, or log output (CLAUDE.md rule 13)</constraint>
    <constraint>Export MSYS_NO_PATHCONV=1 before any AWS CLI commands with ARN or S3 paths on Git Bash</constraint>
  </constraints>

  <dependencies>
    <dependency agent="0.4.0_DT_ClientPlatform" task="ADVI_MVP318.002 req 3" status="pending">
      bd-portal-advisor-publisher deployed at WS2+WS3b version — HARD GATE for gold run
    </dependency>
    <dependency agent="0.4.0_DS_ClientPlatform" task="ADVI_MVP318.001 req 5" status="pending">
      Script 10 (and possibly 09) committed to CLOUD — gate for S3 upload
    </dependency>
  </dependencies>

  <deliverables>
    <deliverable type="verify">FULL gold layer run complete; all three acceptance criterion sets verified</deliverable>
    <deliverable type="document">Session log with verification output for all three workstreams</deliverable>
    <deliverable type="document">EC2_MANIFEST.json updated</deliverable>
  </deliverables>
</task_order>
