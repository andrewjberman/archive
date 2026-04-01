<task_order>
  <metadata>
    <id>2.0.0_SA_COO-2026-04-01-ADHC_HISTRY-006-ds-converter-fix</id>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_to>0.4.0_DS_ClientPlatform</issued_to>
    <date>2026-04-01</date>
    <status>pending</status>
    <priority>medium</priority>
    <type>cleanup</type>
    <project>ADHC_HISTRY</project>
  </metadata>

  <objective>
    Update the Schwab RPS converter script to use the new bronze/rps/ prefix as its
    primary source, remove the March staging workaround script, and clean up dead code.
    This is a 3-file change. Does NOT block the gold rebuild in progress.
  </objective>

  <references>
    <ref type="design_doc">docs/architecture/ADHC_HISTRY_schwab_bucket_design.md</ref>
    <ref type="converter">data/black_diamond/scripts/bronze/convert_schwab_rps_to_parquet.py</ref>
    <ref type="workaround_script">data/black_diamond/scripts/bronze/convert_rps_march_staging.py</ref>
  </references>

  <background>
    DT (ADHC_HISTRY.005) found that the opal-data-schwab bucket is NOT write-locked.
    The policy requires ServerSideEncryption: AES256 on all PutObject calls. The
    convert_schwab_rps_to_parquet.py converter already handles this correctly (line 168).
    The issue was callers using AWS CLI without --sse AES256.

    The design calls for new RPS files to land in bronze/rps/ going forward, with
    the converter reading bronze/rps/ first (new data) and 01_raw/ as fallback (historical).
    The March staging workaround script is now dead code.
  </background>

  <requirements>

    <requirement id="1">
      Read convert_schwab_rps_to_parquet.py completely. Locate the SRC_PREFIXES constant
      or wherever source prefixes are defined.

      Change the source prefix list to read bronze/rps/ first:
      ```python
      # Before (or equivalent)
      SRC_PREFIXES = ['01_raw/', '02_anonymized/']

      # After
      SRC_PREFIXES = ['bronze/rps/', '01_raw/']  # bronze/rps/ first (new data), 01_raw/ historical fallback
      ```

      Verify the converter handles both prefixes with SSE-AES256 on output (line 168 per DT).
      If the SSE kwarg is missing anywhere in the write path, add `ServerSideEncryption='AES256'`.
    </requirement>

    <requirement id="2">
      Delete convert_rps_march_staging.py. This script was a one-off workaround that
      patched the converter to read from opal-data-bd/uploads/schwab/. With the new
      routing design, it is dead code.

      Verify no other script imports or references convert_rps_march_staging.py before deleting.
    </requirement>

    <requirement id="3">
      Commit both changes (converter update + deletion) with author attribution:
      ```
      git commit --author="0.4.0_DS_ClientPlatform <0.4.0_DS_ClientPlatform@opal.agent>" \
          -m "cleanup(ADHC_HISTRY): converter reads bronze/rps/ first, delete march staging workaround"
      ```
      Do NOT push. AE will push after completing the file migration (.007).
    </requirement>

    <requirement id="4">
      Write a brief session log update (append to today's existing log or create new):
      org/tier2_senior/0.4.0_DS_ClientPlatform/logs/2026-04-01/adhc_histry_converter_cleanup.md

      Note: commit hash, what changed, and that the March staging files in
      opal-data-bd/uploads/schwab/ are still there pending AE migration.
    </requirement>

    <requirement id="5">
      Message COO when committed with the commit hash.
    </requirement>

  </requirements>

  <acceptance_criteria>
    <criterion id="1">convert_schwab_rps_to_parquet.py reads bronze/rps/ before 01_raw/.</criterion>
    <criterion id="2">All write paths in the converter include ServerSideEncryption='AES256'.</criterion>
    <criterion id="3">convert_rps_march_staging.py deleted from the repo.</criterion>
    <criterion id="4">Changes committed on CLOUD, not pushed.</criterion>
  </acceptance_criteria>

  <constraints>
    <constraint>Do NOT change silver/RPS/ output prefix -- gold scripts depend on it.</constraint>
    <constraint>Do NOT delete 01_raw/ files -- historical archive, AE handles archival separately.</constraint>
    <constraint>This is a non-blocking cleanup. Do not delay ADHC_HISTRY Phase 2 gold rebuild for this.</constraint>
    <constraint>No emojis per CLAUDE.md.</constraint>
  </constraints>

  <dependencies>
    <dependency agent="0.4.0_DT_ClientPlatform" task="ADHC_HISTRY.005" status="complete">
      Design doc confirms the converter change needed. SSE requirement and prefix structure verified.
    </dependency>
  </dependencies>

  <deliverables>
    <deliverable type="code-commit">convert_schwab_rps_to_parquet.py updated + convert_rps_march_staging.py deleted</deliverable>
    <deliverable type="message">COO commit hash notification</deliverable>
  </deliverables>
</task_order>
