<task_order>
  <metadata>
    <id>2.0.0_SA_COO-2026-04-01-ADHC_HISTRY-007-ae-schwab-migration</id>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_to>0.7.0_AE_CloudOps</issued_to>
    <date>2026-04-01</date>
    <status>staged</status>
    <!-- STAGED: activate after DS commits ADHC_HISTRY.006 (converter script fix) -->
    <priority>medium</priority>
    <type>infrastructure</type>
    <project>ADHC_HISTRY</project>
  </metadata>

  <objective>
    Migrate the March 2026 Schwab RPS staging files from the workaround location
    (opal-data-bd/uploads/schwab/) to the new canonical location
    (opal-data-schwab/bronze/rps/), then clean up the staging area.
    Run this AFTER DS commits ADHC_HISTRY.006 (converter reads bronze/rps/).
  </objective>

  <references>
    <ref type="design_doc">docs/architecture/ADHC_HISTRY_schwab_bucket_design.md</ref>
    <ref type="ds_to">ADHC_HISTRY.006.ds-converter-script-fix.md (must be committed first)</ref>
  </references>

  <background>
    The opal-data-schwab bucket is NOT write-locked -- it requires --sse AES256 on all
    PutObject calls (DT finding, ADHC_HISTRY.005). EC2 role bd-exporter-ec2-role already
    has write access. The March staging files (22 RPS CSVs) were placed in
    opal-data-bd/uploads/schwab/ as a workaround. They belong in opal-data-schwab/bronze/rps/.
  </background>

  <requirements>

    <requirement id="1">
      PREREQUISITE: Confirm DS ADHC_HISTRY.006 is committed.
      `git log --oneline --author="0.4.0_DS" -3`
      Must show the converter cleanup commit before proceeding.
    </requirement>

    <requirement id="2">
      Copy March RPS files from staging to canonical location with SSE:
      ```bash
      aws s3 cp s3://opal-data-bd/uploads/schwab/ \
          s3://opal-data-schwab/bronze/rps/ \
          --recursive --sse AES256

      # Verify all 22 files copied
      aws s3 ls s3://opal-data-schwab/bronze/rps/ | wc -l
      # Expected: 22 (CRS20260302.RPS through CRS20260331.RPS)
      ```
    </requirement>

    <requirement id="3">
      Run the updated converter (from DS .006 commit) against bronze/rps/ to confirm
      it processes the March files correctly:
      - Pull DS commit from CLOUD (git pull origin CLOUD)
      - Upload updated converter script to S3 for EC2
      - Run on EC2 -- it should read bronze/rps/ and write/update silver/RPS/ partitions
      - Verify: `aws s3 ls s3://opal-data-schwab/silver/RPS/ | tail -5` -- should show
        recent March dates (20260302-20260331) at same timestamps or newer
    </requirement>

    <requirement id="4">
      Once converter verification passes, delete the workaround staging area:
      ```bash
      aws s3 rm s3://opal-data-bd/uploads/schwab/ --recursive
      # Verify empty
      aws s3 ls s3://opal-data-bd/uploads/schwab/
      # Expected: no output
      ```
    </requirement>

    <requirement id="5">
      Archive legacy prefixes (low priority, run as background job on EC2 -- large operation):
      ```bash
      # Copy 01_raw/ to _archive/01_raw/ (6214+ files, run background)
      aws s3 cp s3://opal-data-schwab/01_raw/ \
          s3://opal-data-schwab/_archive/01_raw/ \
          --recursive --sse AES256
      # Do NOT delete 01_raw/ until archive is verified complete
      ```
      This is non-blocking for the rest of the sprint. If EC2 time is constrained,
      defer to next session.
    </requirement>

    <requirement id="6">
      Write session log at:
      org/tier2_senior/0.7.0_AE_CloudOps/logs/2026-04-01/adhc_histry_schwab_migration.md

      Include: file counts copied, converter run verification, staging area deletion confirmed.
    </requirement>

    <requirement id="7">
      Message COO (2.0.0_SA_COO) when migration is complete.
    </requirement>

  </requirements>

  <acceptance_criteria>
    <criterion id="1">22 March RPS files at s3://opal-data-schwab/bronze/rps/ with SSE.</criterion>
    <criterion id="2">Updated converter runs clean against bronze/rps/ (no errors).</criterion>
    <criterion id="3">s3://opal-data-bd/uploads/schwab/ empty (staging deleted).</criterion>
    <criterion id="4">_archive/01_raw/ copy in progress or complete (non-blocking).</criterion>
  </acceptance_criteria>

  <constraints>
    <constraint>PREREQUISITE: DS .006 converter commit required before running converter step.</constraint>
    <constraint>All aws s3 cp writes to opal-data-schwab MUST include --sse AES256 or fail with 403.</constraint>
    <constraint>Do NOT delete 01_raw/ until _archive/01_raw/ is verified complete.</constraint>
    <constraint>Do NOT re-run the gold rebuild as part of this task. The current gold rebuild (.004) is separate.</constraint>
    <constraint>No emojis per CLAUDE.md.</constraint>
  </constraints>

  <dependencies>
    <dependency agent="0.4.0_DS_ClientPlatform" task="ADHC_HISTRY.006.ds-converter-script-fix" status="pending">
      Converter must read bronze/rps/ before AE runs it. Wait for DS commit.
    </dependency>
  </dependencies>

  <deliverables>
    <deliverable type="data">March RPS files migrated to canonical location. Staging area clean.</deliverable>
    <deliverable type="document">Session log with migration verification</deliverable>
  </deliverables>
</task_order>
