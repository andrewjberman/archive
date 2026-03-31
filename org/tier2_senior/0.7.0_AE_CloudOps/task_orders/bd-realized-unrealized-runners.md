<task_order>
  <metadata>
    <id>1.0.0_SA_CTO-2026-03-30-bd-realized-unrealized-runners</id>
    <issued_by>1.0.0_SA_CTO</issued_by>
    <issued_to>0.7.0_AE_CloudOps</issued_to>
    <date>2026-03-30</date>
    <status>complete</status> <!-- Verified 2026-03-30: bd-v2.20.0 deployed, manual test passed, EventBridge rules live (21:25+21:32 UTC Mon-Fri). AE confirmed via inbox message. -->
  </metadata>

  <objective>
    Set up daily BD realized and unrealized capital gains report runners following
    the exact same pattern as the existing bd-allocations pipeline. BD has two new
    report templates configured: "Realized" and "Unrealized". These need bronze
    ingestion (XLSX download from BD portal to S3), silver conversion (XLSX to daily
    parquet partitions), and the S3 folder structure to support both.
  </objective>

  <scope>
    <files>
      <!-- S3 folder structure (create via aws s3 cp of empty marker or first test file) -->
      <file action="create">s3://opal-data-bd/forwardfill_v2/realized/</file>
      <file action="create">s3://opal-data-bd/forwardfill_v2/unrealized/</file>
      <file action="create">s3://opal-data-bd/silver/realized/</file>
      <file action="create">s3://opal-data-bd/silver/unrealized/</file>

      <!-- Silver merge script extension -->
      <file action="modify">data/black_diamond/scripts/silver/merge-daily-incremental.py</file>

      <!-- SSM documents (new, one per report type) -->
      <file action="create">infra/aws/ssm/opal-bd-realized-download.json</file>
      <file action="create">infra/aws/ssm/opal-bd-unrealized-download.json</file>

      <!-- Trigger Lambdas (new, one per report type) -->
      <file action="create">infra/aws/lambda/bd-pipeline/bd-realized-trigger/lambda_function.py</file>
      <file action="create">infra/aws/lambda/bd-pipeline/bd-unrealized-trigger/lambda_function.py</file>

      <!-- EventBridge rules -->
      <file action="modify">infra/aws/terraform/bd-pipeline/eventbridge.tf</file>

      <!-- Terraform for new Lambdas + SSM -->
      <file action="modify">infra/aws/terraform/bd-pipeline/main.tf</file>

      <!-- Source map -->
      <file action="modify">infra/aws/lambda/ci/lambda-source-map.json</file>

      <!-- EC2 manifest if new instance needed -->
      <file action="modify">infra/aws/ec2/EC2_MANIFEST.json</file>
    </files>
  </scope>

  <requirements>
    <requirement id="1">
      Create canonical S3 folder structure:
      - Bronze: `s3://opal-data-bd/forwardfill_v2/realized/REALIZED_YYYY-MM-DD.xlsx`
      - Bronze: `s3://opal-data-bd/forwardfill_v2/unrealized/UNREALIZED_YYYY-MM-DD.xlsx`
      - Silver: `s3://opal-data-bd/silver/realized/YYYY-MM-DD.parquet`
      - Silver: `s3://opal-data-bd/silver/unrealized/YYYY-MM-DD.parquet`
      - Manifests: `s3://opal-data-bd/silver/incremental_realized_manifest.json`
      - Manifests: `s3://opal-data-bd/silver/incremental_unrealized_manifest.json`
    </requirement>

    <requirement id="2">
      Extend `merge-daily-incremental.py` with `--realized` and `--unrealized` flags
      following the exact pattern of `--allocations`. Each flag:
      - Lists new XLSX files in the corresponding forwardfill_v2/ prefix
      - Converts XLSX to parquet with snake_case column normalization
      - Saves daily partitions to silver/{report_type}/YYYY-MM-DD.parquet
      - Tracks processed files in the report-type-specific manifest
      - Dedup keys: realized uses (account_id, asset_name, trade_date, unit_cost),
        unrealized uses (account_id, asset_name) as it is a daily snapshot
    </requirement>

    <requirement id="3">
      Create SSM documents for each report type, patterned after
      `opal-bd-allocation-download`. Steps: fetch BD credentials from Secrets Manager
      (`opal/bd/credentials`), download from BD portal using the template name
      ("Realized" / "Unrealized"), upload XLSX to bronze S3 prefix, run
      merge-daily-incremental.py with the appropriate flag.
    </requirement>

    <requirement id="4">
      Create trigger Lambdas patterned after `bd-allocation-trigger`. Each Lambda:
      starts the bd-allocations EC2 instance (reuse i-0800437d1dbb0b5cc, same BD
      credentials and IAM role), sends the corresponding SSM document, returns.
      The EC2 instance is already configured with bd-exporter-ec2-role which has
      S3 read/write to opal-data-bd/ and Secrets Manager access.
    </requirement>

    <requirement id="5">
      Add EventBridge rules in `eventbridge.tf` for daily weekday execution.
      Schedule AFTER the existing allocation trigger (21:48 UTC):
      - Unrealized: ~21:55 UTC (daily snapshot, runs first)
      - Realized: ~22:02 UTC (incremental, runs second)
      Stagger to avoid concurrent SSM commands on the same EC2 instance.
    </requirement>

    <requirement id="6">
      Register both new Lambdas in `lambda-source-map.json`. Add both SSM
      document names to the bd-daily-trigger-lambda-role IAM policy so the
      trigger Lambdas can dispatch them.
    </requirement>

    <requirement id="7">
      Deploy via standard Terraform flow: commit -> plan -> apply -> 0-diff ->
      record-terraform-deploy.sh -> tag -> push --follow-tags. This is a
      bd-pipeline Terraform change.
    </requirement>
  </requirements>

  <acceptance_criteria>
    <criterion id="1">Both trigger Lambdas exist and can be invoked manually (test invocation returns success)</criterion>
    <criterion id="2">SSM documents execute successfully on bd-allocations EC2 instance</criterion>
    <criterion id="3">After one manual trigger cycle, XLSX files appear in forwardfill_v2/realized/ and forwardfill_v2/unrealized/</criterion>
    <criterion id="4">After merge script runs, parquet files appear in silver/realized/ and silver/unrealized/</criterion>
    <criterion id="5">EventBridge rules are ENABLED and fire on weekday schedule</criterion>
    <criterion id="6">lambda-source-map.json updated, 0-diff Terraform plan achieved</criterion>
    <criterion id="7">bd-pipeline tagged with next version</criterion>
  </acceptance_criteria>

  <constraints>
    <constraint>Reuse the existing bd-allocations EC2 instance (i-0800437d1dbb0b5cc) -- do NOT create a new instance. Same BD credentials, same IAM role.</constraint>
    <constraint>Stagger EventBridge schedules to prevent concurrent SSM commands on the same instance.</constraint>
    <constraint>Follow LAMBDA_DEPLOYMENT_PROTOCOL.md and TERRAFORM_PIPELINE_STRATEGY.md for all deploy steps.</constraint>
    <constraint>The BD report template names are exactly "Realized" and "Unrealized" -- confirm with the BD TypeScript downloader how template names map to download parameters.</constraint>
    <constraint>Unrealized is a daily SNAPSHOT (full replacement each day). Realized is INCREMENTAL (each day adds that day's sells). The merge script must handle both patterns -- unrealized overwrites by (account_id, asset_name), realized appends by (account_id, asset_name, trade_date).</constraint>
    <constraint>No emojis in any code per CLAUDE.md.</constraint>
  </constraints>

  <dependencies>
    <dependency agent="0.4.0_DS_ClientPlatform" task="bd_realized_agg.parquet compaction" status="complete">DS already built the one-time backfill compaction. This task order creates the STEADY-STATE pipeline that replaces the backfill.</dependency>
  </dependencies>

  <deliverables>
    <deliverable type="commit">merge-daily-incremental.py with --realized and --unrealized flags</deliverable>
    <deliverable type="commit">SSM documents for both report types</deliverable>
    <deliverable type="commit">Trigger Lambdas for both report types</deliverable>
    <deliverable type="commit">EventBridge rules in bd-pipeline Terraform</deliverable>
    <deliverable type="commit">lambda-source-map.json updated</deliverable>
    <deliverable type="deploy">bd-pipeline Terraform apply + 0-diff + tag</deliverable>
  </deliverables>
</task_order>
