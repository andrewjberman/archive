<task_order>
  <metadata>
    <id>2.0.0_SA_COO-2026-04-01-ADHC_HISTRY-003-ae-rps-silver</id>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_to>0.6.0_AE_PartnerETL</issued_to>
    <date>2026-04-01</date>
    <status>complete</status>
    <!-- Completed 2026-04-01. 534 RPS partitions built. DS diagnostic ran successfully against silver/RPS/. -->
    <priority>urgent</priority>
    <type>data-build</type>
    <project>ADHC_HISTRY</project>
  </metadata>

  <objective>
    Build the Schwab RPS silver layer. DS is blocked on this.

    RPS = Schwab daily position snapshots. Each file reports quantity_settled per
    (account, security) for one date. The converter script already exists at
    data/black_diamond/scripts/bronze/convert_schwab_rps_to_parquet.py.
    Run it on EC2 to produce silver/RPS/ partitioned parquet.

    DS has already committed adhc_histry_005_schwab_authority_calc.py (c8db9f09)
    which reads silver/RPS/ and exits with BLOCKED if it is empty. Once silver/RPS/
    is populated, AE runs the DS script on EC2.
  </objective>

  <references>
    <ref type="converter_script">data/black_diamond/scripts/bronze/convert_schwab_rps_to_parquet.py</ref>
    <ref type="ds_diagnostic">data/black_diamond/scripts/diagnostics/adhc_histry_005_schwab_authority_calc.py (committed c8db9f09)</ref>
    <ref type="ds_to">org/tier2_senior/0.4.0_DS_ClientPlatform/task_orders/ADHC_HISTRY.002.ds-schwab-authority-injection.md</ref>
    <ref type="ec2_standard">docs/deployment/EC2_CODE_DEPLOYMENT_STANDARD.md</ref>
  </references>

  <requirements>

    <requirement id="1">
      READ convert_schwab_rps_to_parquet.py before running it. Understand:
      - What S3 input path it reads from (raw Schwab RPS files)
      - What S3 output path it writes to (should be opal-data-schwab/silver/RPS/ or similar)
      - Whether it processes all dates or a date range
      - Any dependencies (pandas, pyarrow, etc.) -- verify they are available on EC2

      Your 2026-03-31 log shows TRN silver was built (337 partitions) but RPS was NOT run.
      Confirm the RPS raw files exist in S3 before running the converter.
    </requirement>

    <requirement id="2">
      Upload convert_schwab_rps_to_parquet.py to S3 per EC2_CODE_DEPLOYMENT_STANDARD.md,
      then run on EC2 via SSM. Log the S3 output path and partition count.
    </requirement>

    <requirement id="3">
      After silver/RPS/ is built, upload the DS diagnostic script to S3 and run it on EC2:
        Script: data/black_diamond/scripts/diagnostics/adhc_histry_005_schwab_authority_calc.py
        Commit: c8db9f09

      The script reads silver/RPS/ and the account mapping parquet, then writes:
        s3://opal-data-bd/diagnostics/schwab_authority_calc.csv

      Capture the stdout summary output in your session log.
    </requirement>

    <requirement id="4">
      Report back to COO with:
      - silver/RPS/ partition count and date range covered
      - Diagnostic script stdout (injection gap summary)
      - S3 path of schwab_authority_calc.csv confirmed present

      Message COO when complete so DS can proceed to Phase 2 analysis.
    </requirement>

    <requirement id="5">
      Write a session log at:
      org/tier2_senior/0.6.0_AE_PartnerETL/logs/YYYY-MM-DD/adhc_histry_p1_rps_silver_and_diagnostic.md
    </requirement>

  </requirements>

  <acceptance_criteria>
    <criterion id="1">silver/RPS/ populated in S3 with partitioned parquet covering available RPS date range.</criterion>
    <criterion id="2">adhc_histry_005_schwab_authority_calc.py runs to completion on EC2 (no BLOCKED exit).</criterion>
    <criterion id="3">s3://opal-data-bd/diagnostics/schwab_authority_calc.csv exists.</criterion>
    <criterion id="4">COO notified with diagnostic stdout summary.</criterion>
  </acceptance_criteria>

  <constraints>
    <constraint>Follow EC2_CODE_DEPLOYMENT_STANDARD.md: upload to S3 first, EC2 pulls from S3, never inline Python in SSM.</constraint>
    <constraint>No emojis in code per CLAUDE.md.</constraint>
    <constraint>Do NOT modify the DS diagnostic script. Run it as committed (c8db9f09).</constraint>
    <constraint>Do NOT run a full gold layer rebuild -- this is diagnostic only.</constraint>
  </constraints>

  <dependencies>
    <dependency agent="0.4.0_DS_ClientPlatform" task="ADHC_HISTRY.002.ds-schwab-authority-injection" status="pending">
      DS script committed at c8db9f09. Waiting on silver/RPS/ to unblock.
    </dependency>
  </dependencies>

  <deliverables>
    <deliverable type="s3-data">silver/RPS/ partitioned parquet in opal-data-schwab</deliverable>
    <deliverable type="s3-artifact">s3://opal-data-bd/diagnostics/schwab_authority_calc.csv</deliverable>
    <deliverable type="document">Session log + COO message with diagnostic summary</deliverable>
  </deliverables>
</task_order>
