<task_order>
  <metadata>
    <id>2.0.0_SA_COO-2026-03-26-mvplvl-010-ae</id>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_to>0.6.0_AE_PartnerETL</issued_to>
    <date>2026-03-26</date>
    <status>complete</status>
    <!-- CTO audit 2026-03-26: Gold rerun subsumed by ADVI_GLDRST.002 (same scope, broader). No separate MVPLVL rerun needed. -->
    <project_code>ADVI_MVPLVL</project_code>
  </metadata>

  <objective>
    Deploy DS's ghost exclusion + mix_timeseries fixes to S3, then run a FULL
    gold layer rebuild to regenerate all parquets and portal artifacts.

    UPDATED 2026-03-26: DS expanded scope beyond the original 06+06b to include
    5 scripts and a new shared library. Script 05b (account_performance) is now
    changed and it only runs in FULL mode. A full gold rerun is required.

    Changes across 4 commits (9bca5ff6, 38faa34f, df5e8004, ae3403f5):
    - lib/exclusions.py: new shared module (ghost account loading + insurance AP gate)
    - Script 05: deduped to use lib/exclusions.py (zero behavior change)
    - Script 05b: ghost account exclusion added (closes ~$7.4M Books vs Advisors gap)
    - Script 06: ghost account exclusion added
    - Script 06b: ghost exclusion + mix_timeseries.json alias + insurance AP gate
    - Script 12: ghost exclusion + insurance AP gate (180d for insurance vs 45d standard)
  </objective>

  <context>
    DS session: org/tier2_senior/0.4.0_DS_ClientPlatform/logs/2026-03-26/
      advi_mvplvl_010_l2_mix_tax_diagnostic.md

    DS commits on CLOUD:
    - 9bca5ff6: WS2+WS3 (mix_timeseries alias + script 06 ghost exclusion)
    - 38faa34f: lib/exclusions.py + dedup scripts 05+06 (zero behavior change)
    - df5e8004: Script 05b ghost exclusion (primary fix for Books vs Advisors gap)
    - ae3403f5: Scripts 06b+12 ghost exclusion + shared insurance AP gate

    S3 deploy target: s3://opal-data-bd/code/gold/
    EC2 runner: bd-gold-layer-runner (i-01003b035d2988dfb, r6i.xlarge)
  </context>

  <scope>
    <files>
      <file action="upload-to-s3">data/black_diamond/scripts/gold/lib/exclusions.py</file>
      <file action="upload-to-s3">data/black_diamond/scripts/gold/05_build_client_performance.py</file>
      <file action="upload-to-s3">data/black_diamond/scripts/gold/05b_build_account_performance.py</file>
      <file action="upload-to-s3">data/black_diamond/scripts/gold/06_build_client_tax_liability.py</file>
      <file action="upload-to-s3">data/black_diamond/scripts/gold/06b_build_client_mix_timeseries.py</file>
      <file action="upload-to-s3">data/black_diamond/scripts/gold/12_build_composition_artifacts.py</file>
      <file action="run-on-ec2">run_gold_layer.sh full</file>
    </files>
  </scope>

  <requirements>
    <requirement id="1">
      Verify DS commits are on CLOUD:
        git log --oneline -5 -- data/black_diamond/scripts/gold/lib/exclusions.py
        git log --oneline -5 -- data/black_diamond/scripts/gold/05b_build_account_performance.py
      Expect commits ae3403f5, df5e8004, 38faa34f, 9bca5ff6 in recent history.
    </requirement>

    <requirement id="2">
      Deploy ALL gold scripts (including lib/) to S3:
        aws s3 sync data/black_diamond/scripts/gold/ s3://opal-data-bd/code/gold/ \
          --delete --exclude '*.parquet' --exclude 'archive/*' --exclude '__pycache__/*'
      Verify lib/exclusions.py is uploaded (new file).
    </requirement>

    <requirement id="3">
      Run FULL gold layer on bd-gold-layer-runner via SSM.
      FULL mode is required because script 05b only runs in full mode (excluded
      from incremental script list). The 05b ghost exclusion is the primary fix
      for the $7.4M Books-vs-Advisors AUA gap.
      Verify pipeline completes successfully (sentinel written).
    </requirement>

    <requirement id="4">
      Post-run verification:

      Step 4a: Verify mix_timeseries.json aliases exist:
        aws s3 ls s3://opal-data-bd/gold/advisors/ --recursive | grep mix_timeseries.json
      Should see 20 mix_timeseries.json files (one per advisor).

      Step 4b: Verify ghost accounts excluded from tax liability:
        Check gold runner log for exclusion messages from scripts 05b, 06, 06b, 12.

      Step 4c: Verify 05b account_performance.parquet regenerated:
        aws s3 ls s3://opal-data-bd/gold/account_performance.parquet
      Timestamp should reflect the new full run.
    </requirement>
  </requirements>

  <acceptance_criteria>
    <criterion id="1">DS commits verified on CLOUD before deploy</criterion>
    <criterion id="2">Gold scripts synced to S3 (code/gold/)</criterion>
    <criterion id="3">FULL gold run completes (sentinel written)</criterion>
    <criterion id="4">20 mix_timeseries.json files exist on S3</criterion>
    <criterion id="5">Ghost exclusion logged in run output from scripts 05b, 06, 06b, 12</criterion>
    <criterion id="6">account_performance.parquet regenerated with updated timestamp</criterion>
  </acceptance_criteria>

  <constraints>
    <constraint>Wait for DS commits to land on CLOUD before deploying</constraint>
    <constraint>Use FULL mode -- 05b only runs in full mode and is the primary fix</constraint>
    <constraint>Do NOT modify Lambda or Terraform -- this is S3-only</constraint>
  </constraints>

  <dependencies>
    <dependency agent="0.4.0_DS_ClientPlatform" task="ADVI_MVPLVL.010" status="complete">
      DS committed script fixes locally. Must be on CLOUD before AE deploys.
    </dependency>
  </dependencies>

  <deliverables>
    <deliverable type="deploy">Gold scripts deployed to S3, full gold run complete</deliverable>
    <deliverable type="document">Session log with SSM command IDs and verification output</deliverable>
  </deliverables>
</task_order>
