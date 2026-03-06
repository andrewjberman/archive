# Task Order: ADVI_AUAVAR.002 — Execute AUA Gap Decomposition Diagnostic on EC2 — 0.4.0_DT_ClientPlatform

```xml
<task_order>
  <metadata>
    <id>ADVI_AUAVAR.002-DT.execute-aua-gap-diagnostic</id>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_to>0.4.0_DT_ClientPlatform</issued_to>
    <date>2026-03-06</date>
    <status>pending</status>
    <priority>HIGH — AUAVAR Phase 1 EC2 execution. Blocked until ADVI_AUAVAR.001-DS completes.</priority>
    <thread>ADVI_AUAVAR-001-aua-gap-segment-decomposition-bd-allocat</thread>
    <project>ADVI_AUAVAR</project>
  </metadata>

  <!-- ================================================================ -->
  <!-- SECTION 1 — CONTEXT                                               -->
  <!-- ================================================================ -->
  <background id="1" title="Context">
    Thread ADVI_AUAVAR-001 is complete. DS is writing diag_aua_gap_decomposition.py
    (ADVI_AUAVAR.001-DS). Once committed, DT executes it on EC2 (i-01003b035d2988dfb)
    using the S3 artifact model + SSM send-command pattern.

    Anchor date: D = 2026-03-02.

    The diagnostic resolves two things in one run:
      1) Gold-vs-gold reconciliation: client_performance total vs positions_cube x prices total
         (explains the $1.236B vs $1.552B discrepancy from Phase 1 investigation)
      2) BD-vs-gold segment decomposition: account coverage, household integrity, residual
         (the ~$55M gap waterfall)

    Output is a JSON artifact that DS interprets and COO converts into the AUAVAR memo.
  </background>

  <!-- ================================================================ -->
  <!-- SECTION 2 — WHAT TO DO                                           -->
  <!-- ================================================================ -->
  <objective>
    Execute diag_aua_gap_decomposition.py on EC2 for D=2026-03-02.
    Upload the JSON output and stdout to S3. Report S3 artifact paths to COO/DS.
  </objective>

  <requirements>

    <requirement id="1">
      PRE-FLIGHT: confirm DS task order is complete.
        - data/black_diamond/scripts/diagnostics/diag_aua_gap_decomposition.py is committed.
        - docs/briefs/devops-brief-auavar-gap-decomposition-ec2-run.md exists.
      Do not proceed until both files are committed.
    </requirement>

    <requirement id="2">
      PUSH DS's commits then upload the script to S3:

      git push origin CLOUD

      aws s3 cp data/black_diamond/scripts/diagnostics/diag_aua_gap_decomposition.py \
        s3://opal-data-bd/diagnostics/diag_aua_gap_decomposition.py
    </requirement>

    <requirement id="3">
      EXECUTE on EC2 via SSM send-command using the file://.tmp_ssm_params.json pattern.

      Write .tmp_ssm_params.json:
        {
          "commands": [
            "aws s3 cp s3://opal-data-bd/diagnostics/diag_aua_gap_decomposition.py /tmp/diag_aua_gap_decomposition.py",
            "python /tmp/diag_aua_gap_decomposition.py 2>&1 | tee /tmp/aua_gap_stdout.txt",
            "aws s3 cp /tmp/aua_gap_stdout.txt s3://opal-data-bd/diagnostics/aua_gap_decomposition_2026-03-02_stdout.txt"
          ]
        }

      Then:
        export MSYS_NO_PATHCONV=1
        aws ssm send-command \
          --document-name "AWS-RunShellScript" \
          --instance-ids i-01003b035d2988dfb \
          --parameters file://.tmp_ssm_params.json \
          --output text

      EC2 instance: bd-gold-layer-runner (i-01003b035d2988dfb)
      Expected runtime: ~5-10 min (single date, no multi-partition transaction scan)

      The script writes its own JSON output to S3:
        s3://opal-data-bd/diagnostics/aua_gap_decomposition_2026-03-02.json

      DT only needs to capture stdout (above) and confirm JSON exists.
    </requirement>

    <requirement id="4">
      POST-RUN DATA AVAILABILITY CHECK:
      The script attempts to load positions_cube/2026-03-02.parquet. If it flags
      positions_cube_missing=true in the JSON, report this to DS/COO before considering
      the run complete. A fallback run for D=2026-03-03 or D=2026-03-04 may be needed.
    </requirement>

    <requirement id="5">
      REPORT and LOG after execution:
        - Confirm S3 artifacts are present:
            s3://opal-data-bd/diagnostics/aua_gap_decomposition_2026-03-02.json
            s3://opal-data-bd/diagnostics/aua_gap_decomposition_2026-03-02_stdout.txt
        - Print the top-level "totals" block from the JSON (aws s3 cp to /tmp, cat)
        - Note the SSM command ID

      Write DT execution log at:
        org/tier2_senior/0.4.0_DT_ClientPlatform/logs/2026-03-XX/auavar_aua_gap_diagnostic_ec2.md

      Commit log with DT authorship:
        git commit --author="0.4.0_DT_ClientPlatform &lt;0.4.0_DT_ClientPlatform@opal.agent&gt;" \
          -m "0.4.0_DT_ClientPlatform: ADVI_AUAVAR -- AUA gap diagnostic executed, S3 artifact published"
    </requirement>

  </requirements>

  <acceptance_criteria>
    <criterion id="1">
      s3://opal-data-bd/diagnostics/aua_gap_decomposition_2026-03-02.json exists and
      contains all required top-level keys: run_metadata, totals, coverage, segments,
      top_account_residuals, diagnostics.
    </criterion>
    <criterion id="2">
      s3://opal-data-bd/diagnostics/aua_gap_decomposition_2026-03-02_stdout.txt exists.
    </criterion>
    <criterion id="3">
      DT execution log committed with SSM command ID and S3 artifact confirmation.
      If positions_cube was missing, this is noted explicitly in the log.
    </criterion>
    <criterion id="4">
      No gold/ or silver/ production files modified.
    </criterion>
  </acceptance_criteria>

  <constraints>
    <constraint>
      EC2_CODE_DEPLOYMENT_STANDARD.md applies. S3 artifact model only. No inline Python in SSM.
    </constraint>
    <constraint>
      Use export MSYS_NO_PATHCONV=1 before aws ssm send-command to prevent MSYS path mangling.
    </constraint>
    <constraint>
      Do not rerun or modify the diagnostic script without DS/COO approval. If the script errors,
      capture the full stdout and report before any retry.
    </constraint>
    <constraint>
      Commit with DT authorship. Push after execution log is written.
    </constraint>
  </constraints>

  <dependencies>
    <dependency agent="0.4.0_DS_ClientPlatform"
                task="ADVI_AUAVAR.001-DS (write script + DT brief)"
                status="blocking"
                note="DT cannot execute until DS commits diag_aua_gap_decomposition.py and DT brief."/>
  </dependencies>

  <deliverables>
    <deliverable type="s3">s3://opal-data-bd/diagnostics/aua_gap_decomposition_2026-03-02.json</deliverable>
    <deliverable type="s3">s3://opal-data-bd/diagnostics/aua_gap_decomposition_2026-03-02_stdout.txt</deliverable>
    <deliverable type="commit">DT execution log with S3 artifact confirmation</deliverable>
  </deliverables>

</task_order>
```
