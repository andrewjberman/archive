<task_order>
  <metadata>
    <id>2.0.0_SA_COO-2026-04-02-gldrst-019-ae</id>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_to>0.7.0_AE_CloudOps</issued_to>
    <date>2026-04-02</date>
    <status>superseded</status><!-- 2026-04-16: Schwab delivery must remain manual (SI2 Desktop only, no API/SFTP). Automation objective is not achievable. Manual SOP already documented in 0.6.0_AE_PartnerETL/prompt.md "Schwab Ingest" section -- 0.6.0 owns execution. Andrew confirmed 2026-04-16. -->
    <project_code>ADVI_GLDRST</project_code>
  </metadata>

  <objective>
    Automate daily Schwab RPS data retrieval, conversion, and ingestion into
    `s3://opal-data-schwab/silver/rps/`. Replace the current manual upload
    process with a scheduled pipeline. The SFTP feed stopped 2026-02-27;
    March 2026 data was manually uploaded via a workaround path.
  </objective>

  <context>
    The converter exists (`bronze/convert_schwab_rps_to_parquet.py`) and
    gold scripts already consume `silver/RPS/`. The gap is automated
    retrieval + scheduling. The delivery mechanism is unknown -- Andrew
    must clarify before implementation can begin.

    Possible mechanisms:
    - SFTP (historical, stopped working) -- needs credential refresh or new endpoint
    - API -- if Schwab provides one
    - Manual download from portal -- could be automated with Playwright
      (similar to BD exporter pattern)

    PRD: docs/architecture/GLDRST_P3_OPERATIONAL_READINESS.md (Work Stream D)
  </context>

  <scope>
    <files>
      <file action="create">Retrieval script (path TBD based on mechanism)</file>
      <file action="create">SSM document following opal-bd-realized-download.json pattern</file>
      <file action="create">EventBridge cron schedule or Lambda trigger</file>
      <file action="modify">Secrets Manager entry for Schwab credentials (if needed)</file>
    </files>
  </scope>

  <requirements>
    <requirement id="1">
      Build a retrieval script for the delivery mechanism Andrew specifies.
      The script must:
      - Fetch credentials from Secrets Manager
      - Download new RPS files to local staging
      - Upload raw files to `s3://opal-data-schwab/bronze/rps/`
      - Run `convert_schwab_rps_to_parquet.py` to produce silver partitions
      - Clean up staging
    </requirement>

    <requirement id="2">
      Create an SSM document following the `opal-bd-realized-download.json`
      pattern: fetch creds -> download -> upload to S3 -> run converter ->
      shut down instance.
    </requirement>

    <requirement id="3">
      Schedule daily execution via EventBridge cron. Target the download
      instance (not the gold runner). Run after market close (e.g., 7 PM ET).
    </requirement>

    <requirement id="4">
      No new IAM changes needed -- existing `bd-exporter-ec2-role` already
      has access to `opal-data-schwab`. Verify this before assuming.
    </requirement>
  </requirements>

  <acceptance_criteria>
    <criterion id="1">Daily Schwab RPS files appear in s3://opal-data-schwab/bronze/rps/ without manual intervention</criterion>
    <criterion id="2">silver/RPS/ partitions are current through previous business day</criterion>
    <criterion id="3">SSM document registered and tested end-to-end</criterion>
    <criterion id="4">EventBridge rule active with correct schedule</criterion>
  </acceptance_criteria>

  <constraints>
    <constraint>BLOCKED: Cannot begin until Andrew clarifies the Schwab delivery mechanism</constraint>
    <constraint>Use lowercase s3 paths: bronze/rps/ and silver/rps/ (per S3 path case consistency rule)</constraint>
    <constraint>Deploy via safe-ec2-deploy.sh per EC2 deployment protocol</constraint>
    <constraint>Do not modify the converter script -- it works correctly</constraint>
  </constraints>

  <dependencies>
    <dependency agent="Andrew" task="vendor-interface-clarification" status="blocked">
      Andrew must confirm whether Schwab RPS is available via SFTP, API, or portal download.
    </dependency>
  </dependencies>

  <deliverables>
    <deliverable type="commit">Retrieval script + SSM document</deliverable>
    <deliverable type="deploy">EventBridge cron rule + SSM document registered</deliverable>
    <deliverable type="log">Session log with end-to-end test evidence</deliverable>
  </deliverables>

  <references>
    <ref type="prd">docs/architecture/GLDRST_P3_OPERATIONAL_READINESS.md</ref>
    <ref type="source">data/black_diamond/scripts/bronze/convert_schwab_rps_to_parquet.py</ref>
    <ref type="pattern">infra/aws/ec2/bd-exporter/opal-bd-realized-download.json</ref>
  </references>
</task_order>
