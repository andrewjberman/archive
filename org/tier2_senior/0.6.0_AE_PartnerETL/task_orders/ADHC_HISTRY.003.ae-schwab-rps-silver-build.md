<task_order>
  <metadata>
    <id>1.0.0_SA_CTO-2026-04-01-ADHC_HISTRY-003-ae-rps-silver</id>
    <issued_by>1.0.0_SA_CTO</issued_by>
    <issued_to>0.6.0_AE_PartnerETL</issued_to>
    <date>2026-04-01</date>
    <status>complete</status>
    <!-- Completed 2026-04-01. Subsumed by ADHC_HISTRY.003.ae-rps-silver-build.md. 534 RPS partitions confirmed built. -->
    <priority>high</priority>
    <type>feature</type>
    <project>ADHC_HISTRY</project>
  </metadata>

  <objective>
    Build the Schwab silver/RPS/ layer on EC2. RPS files are Schwab's authoritative
    daily position snapshots -- settled quantity, market value, and closing price per
    (account, security) -- no FIFO reconstruction required. This is the upstream
    dependency for DS's RPS-based matching (ADHC_HISTRY.002 revised).

    Three Schwab converters exist locally and need to be committed, uploaded to S3,
    and run on EC2:
    - convert_schwab_rps_to_parquet.py  (NEW -- opal-data-schwab/silver/RPS/)
    - convert_schwab_acc_to_parquet.py  (NEW -- opal-data-schwab/silver/ACC/)
    - convert_schwab_trn_to_parquet.py  (MODIFIED -- already has silver/TRN/ in S3)

    Priority: RPS and ACC. TRN is already built (337 partitions) but the converter
    has local modifications -- commit those too.
  </objective>

  <references>
    <ref type="rps_converter">data/black_diamond/scripts/bronze/convert_schwab_rps_to_parquet.py</ref>
    <ref type="acc_converter">data/black_diamond/scripts/bronze/convert_schwab_acc_to_parquet.py</ref>
    <ref type="trn_converter">data/black_diamond/scripts/bronze/convert_schwab_trn_to_parquet.py</ref>
    <ref type="ae_session_log">org/tier2_senior/0.6.0_AE_PartnerETL/logs/2026-03-31/adhc_histry_schwab_silver_layer.md</ref>
    <ref type="ec2_standard">docs/deployment/EC2_CODE_DEPLOYMENT_STANDARD.md</ref>
    <ref type="existing_trn_silver">s3://opal-data-schwab/silver/TRN/ (337 partitions, 2026-01-16 to 2026-03-30)</ref>
  </references>

  <pre_verified_facts>
    1. All three converter scripts exist at data/black_diamond/scripts/bronze/ but are
       NOT committed to git (convert_schwab_rps_to_parquet.py and convert_schwab_acc_to_parquet.py
       are untracked; convert_schwab_trn_to_parquet.py is tracked but has uncommitted changes).

    2. silver/TRN/ already has 337 partitions in S3 from prior AE session (run locally).
       The updated TRN converter should be committed but re-running it is lower priority
       (use already_converted() idempotency check if you do run it).

    3. RPS files follow the pattern: CRS{YYYYMMDD}.RPS in opal-data-schwab/01_raw/
       and opal-data-schwab/02_anonymized/. 2024-09 through 2025-11 is Glacier (skip).
       STANDARD-class files should be in the same date range as TRN (2026-01-16 onward
       + scattered 2024 non-Glacier dates).

    4. ACC files follow: CRS{YYYYMMDD}.ACC pattern. Same Glacier constraint applies.

    5. EC2 gold runner (bd-exporter-ec2) has opal-data-schwab read/write IAM access
       (added in 2026-03-31 session).
  </pre_verified_facts>

  <requirements>

    <requirement id="1">
      Commit all three converters to CLOUD branch:
      ```
      git add data/black_diamond/scripts/bronze/convert_schwab_rps_to_parquet.py \
              data/black_diamond/scripts/bronze/convert_schwab_acc_to_parquet.py \
              data/black_diamond/scripts/bronze/convert_schwab_trn_to_parquet.py
      git commit --author="0.6.0_AE_PartnerETL &lt;0.6.0_AE_PartnerETL@opal.agent&gt;" \
          -m "feat(ADHC_HISTRY): add Schwab RPS+ACC+TRN bronze-to-silver converters"
      ```
      Do NOT push yet -- push is a separate step after the task is complete.
    </requirement>

    <requirement id="2">
      Upload the three scripts to S3 for EC2 access. Use the EC2_CODE_DEPLOYMENT_STANDARD.md
      pattern. Upload to the Schwab converter code path:
      ```
      aws s3 cp data/black_diamond/scripts/bronze/convert_schwab_rps_to_parquet.py \
                s3://opal-data-bd/code/schwab/convert_schwab_rps_to_parquet.py
      aws s3 cp data/black_diamond/scripts/bronze/convert_schwab_acc_to_parquet.py \
                s3://opal-data-bd/code/schwab/convert_schwab_acc_to_parquet.py
      aws s3 cp data/black_diamond/scripts/bronze/convert_schwab_trn_to_parquet.py \
                s3://opal-data-bd/code/schwab/convert_schwab_trn_to_parquet.py
      ```
    </requirement>

    <requirement id="3">
      Run convert_schwab_rps_to_parquet.py on EC2 via SSM. This is the priority.
      SSM command pattern (from your deployment standard):
      ```bash
      cd /tmp \
        &amp;&amp; aws s3 cp s3://opal-data-bd/code/schwab/convert_schwab_rps_to_parquet.py . \
        &amp;&amp; python3 convert_schwab_rps_to_parquet.py 2&gt;&amp;1 \
        | tee /var/log/schwab_rps_convert.log \
        &amp;&amp; aws s3 cp /var/log/schwab_rps_convert.log \
           s3://opal-data-bd/logs/schwab/rps_convert_$(date +%Y%m%d_%H%M%S).log
      ```
      Poll the SSM command to completion. Pull stdout output to verify results.
    </requirement>

    <requirement id="4">
      After RPS conversion completes, run convert_schwab_acc_to_parquet.py on EC2 via SSM
      using the same pattern. ACC is needed for the account master (taxpayer name, SSN
      cross-reference for account matching validation).
    </requirement>

    <requirement id="5">
      Report in your session log:
      - Total RPS partitions built (expected: same date range as TRN or close)
      - Sample of dates (first 3, last 3)
      - Total ACC partitions built
      - Any SKIP dates (Glacier files -- expected and fine to skip)
      - Confirm s3://opal-data-schwab/silver/RPS/ and silver/ACC/ are populated
    </requirement>

    <requirement id="6">
      Send a message to 0.4.0_DS_ClientPlatform via MCP when silver/RPS/ is confirmed built:
      ```
      send_message(
        from="0.6.0_AE_PartnerETL",
        to="0.4.0_DS_ClientPlatform",
        subject="silver/RPS/ ready -- ADHC_HISTRY.002",
        body="RPS silver layer built at s3://opal-data-schwab/silver/RPS/. N partitions from
              {first_date} to {last_date}. You can proceed with ADHC_HISTRY.002 RPS matching.
              Account mapping is at s3://opal-data-bd/gold/dimensions/schwab_bd_account_mapping.parquet."
      )
      ```
      Also notify CTO (1.0.0_SA_CTO) with the same summary.
    </requirement>

  </requirements>

  <acceptance_criteria>
    <criterion id="1">All three converters committed to CLOUD branch with correct author attribution.</criterion>
    <criterion id="2">s3://opal-data-schwab/silver/RPS/ populated with date-partitioned Parquet files.</criterion>
    <criterion id="3">s3://opal-data-schwab/silver/ACC/ populated with date-partitioned Parquet files.</criterion>
    <criterion id="4">SSM run logs saved to S3 for audit trail.</criterion>
    <criterion id="5">DS notified via MCP that silver/RPS/ is ready.</criterion>
  </acceptance_criteria>

  <constraints>
    <constraint>Never run scripts locally against production data. Upload to S3, EC2 pulls and executes.</constraint>
    <constraint>Do not restore Glacier files -- skip them (the converters already handle this with storage class check).</constraint>
    <constraint>No emojis in any code or log output per CLAUDE.md.</constraint>
    <constraint>Do not deploy any gold layer changes -- this is a silver data build only.</constraint>
    <constraint>Commit the converters but do NOT push to remote -- push comes after full task is done.</constraint>
  </constraints>

  <dependencies>
    <dependency agent="0.4.0_DS_ClientPlatform" task="ADHC_HISTRY.002" status="pending">
      DS is waiting on silver/RPS/ being available. This task (AE.003) is the upstream dependency.
      Notify DS via MCP when complete.
    </dependency>
  </dependencies>

  <deliverables>
    <deliverable type="code-commit">Three Schwab converters committed to CLOUD branch</deliverable>
    <deliverable type="s3-artifact">s3://opal-data-schwab/silver/RPS/ (daily position snapshots)</deliverable>
    <deliverable type="s3-artifact">s3://opal-data-schwab/silver/ACC/ (account master)</deliverable>
    <deliverable type="document">Session log with partition counts, date coverage, SSM command IDs</deliverable>
  </deliverables>
</task_order>
