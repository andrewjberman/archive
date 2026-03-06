# Task Order: ADVI_NNAVAR.002 — Execute NNA Gap Decomposition Suites on EC2 — 0.4.0_DT_ClientPlatform

```xml
<task_order>
  <metadata>
    <id>ADVI_NNAVAR.002-DT.execute-gap-decomposition-suites</id>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_to>0.4.0_DT_ClientPlatform</issued_to>
    <date>2026-03-06</date>
    <status>pending</status>
    <priority>HIGH — NNAVAR Phase 1 EC2 execution. Blocked until ADVI_NNAVAR.001-DS completes.</priority>
    <thread>ADVI_NNAVAR-001-nna-gap-decomposition-param-grid-analysi</thread>
    <project>ADVI_NNAVAR</project>
  </metadata>

  <!-- ================================================================ -->
  <!-- SECTION 1 — CONTEXT                                               -->
  <!-- ================================================================ -->
  <background id="1" title="Context">
    Thread ADVI_NNAVAR-001 is complete. DS is writing diag_nnavar_gap_decomposition.py
    (ADVI_NNAVAR.001-DS). Once committed, DT executes all 6 suites on EC2
    (i-01003b035d2988dfb, bd-gold-layer-runner) using the S3 artifact model + SSM.

    This is the same EC2/SSM execution pattern used for:
      - diag_acat_inkind_scan_v3.py  (Phase 2)
      - diag_acat_param_grid.py v2   (gold baseline run, ~7 min, 2026-03-05)

    The diagnostic isolates each rule's NNA impact without touching any production gold artifacts.
  </background>

  <!-- ================================================================ -->
  <!-- SECTION 2 — WHAT TO DO                                           -->
  <!-- ================================================================ -->
  <objective>
    Execute diag_nnavar_gap_decomposition.py on EC2 for each suite (baseline through coverage),
    one suite at a time, publishing S3 artifacts after each run. Capture stdout per suite.
    Report S3 artifact paths to COO/DS after each suite completes.
  </objective>

  <requirements>

    <requirement id="1">
      PRE-FLIGHT: confirm DS task order is complete.
        - data/black_diamond/scripts/diagnostics/diag_nnavar_gap_decomposition.py is committed.
        - docs/briefs/devops-brief-nnavar-gap-decomposition-ec2-run.md exists.
      Do not proceed until both files are committed.
    </requirement>

    <requirement id="2">
      PUSH DS's commits before uploading the script to S3.

      git push origin CLOUD

      Then upload the diagnostic script to S3:
        aws s3 cp data/black_diamond/scripts/diagnostics/diag_nnavar_gap_decomposition.py \
          s3://opal-data-bd/scripts/diagnostics/diag_nnavar_gap_decomposition.py
    </requirement>

    <requirement id="3">
      EXECUTE SUITES in recommended order (suite-per-invocation via SSM):

      Recommended order: baseline -> exclusions -> dedup -> caps -> timing -> coverage

      For each suite, use the file://.tmp_ssm_params.json pattern (avoids MSYS path mangling):

      Example for --suite exclusions:
        Write .tmp_ssm_params.json:
          {
            "commands": [
              "aws s3 cp s3://opal-data-bd/scripts/diagnostics/diag_nnavar_gap_decomposition.py /tmp/diag_nnavar_gap_decomposition.py",
              "python /tmp/diag_nnavar_gap_decomposition.py --suite exclusions --run-date 20260306 2>&1 | tee /tmp/nnavar_exclusions_stdout.txt",
              "aws s3 cp /tmp/nnavar_exclusions_stdout.txt s3://opal-data-bd/diagnostics/nnavar/20260306/exclusions/stdout.txt"
            ]
          }
        Then:
          aws ssm send-command \
            --document-name "AWS-RunShellScript" \
            --instance-ids i-01003b035d2988dfb \
            --parameters file://.tmp_ssm_params.json \
            --output text

      IMPORTANT:
        - COO/DS review summary.csv after each suite before proceeding to the next.
          If a dominant driver is found early, COO may stop the sequence.
        - If a suite errors, capture the error output and report to DS before retrying.
        - Do not run multiple suites concurrently unless COO explicitly requests.

      Expected runtime per suite:
        baseline    ~1-3 min
        exclusions  ~8-12 min
        dedup       ~10-15 min
        caps        ~8-15 min
        timing      ~2-6 min
        coverage    ~2-6 min
    </requirement>

    <requirement id="4">
      REPORT after each suite: post the following to your session log:
        - Suite name
        - SSM command ID (for auditability)
        - S3 artifact paths written (summary.csv, variants written)
        - Pearson r and total_gap from summary.csv for each variant (copy-paste from CSV)
        - Wall-clock runtime

      After all suites complete, write a single DT execution log at:
        org/tier2_senior/0.4.0_DT_ClientPlatform/logs/2026-03-XX/nnavar_gap_decomposition_ec2.md

      Commit log with DT authorship:
        git commit --author="0.4.0_DT_ClientPlatform &lt;0.4.0_DT_ClientPlatform@opal.agent&gt;" \
          -m "0.4.0_DT_ClientPlatform: ADVI_NNAVAR -- gap decomposition suites executed, S3 artifacts published"
    </requirement>

  </requirements>

  <acceptance_criteria>
    <criterion id="1">
      All 6 suites executed (or execution halted by COO after a decisive early result).
      summary.csv present at s3://opal-data-bd/diagnostics/nnavar/{run_date}/{suite}/summary.csv
      for each completed suite.
    </criterion>
    <criterion id="2">
      stdout captured for each suite at:
        s3://opal-data-bd/diagnostics/nnavar/{run_date}/{suite}/stdout.txt
    </criterion>
    <criterion id="3">
      DT execution log committed with S3 artifact paths and per-variant Pearson r + total_gap.
    </criterion>
    <criterion id="4">
      No gold/ or silver/ production files modified.
    </criterion>
  </acceptance_criteria>

  <constraints>
    <constraint>
      EC2_CODE_DEPLOYMENT_STANDARD.md applies. S3 artifact model only. No inline Python in SSM commands.
    </constraint>
    <constraint>
      Suite-per-invocation: one SSM command per suite, not --suite all, unless COO requests batch run.
    </constraint>
    <constraint>
      If EC2 instance OOMs (memory exhausted), do NOT attempt fixes. Report to DS/COO with
      the full error output before any retry.
    </constraint>
    <constraint>
      Commit with DT authorship. Push after all suites complete.
    </constraint>
  </constraints>

  <dependencies>
    <dependency agent="0.4.0_DS_ClientPlatform"
                task="ADVI_NNAVAR.001-DS (write script + DT brief)"
                status="blocking"
                note="DT cannot execute until DS commits diag_nnavar_gap_decomposition.py and DT brief."/>
  </dependencies>

  <deliverables>
    <deliverable type="s3">s3://opal-data-bd/diagnostics/nnavar/{run_date}/*/summary.csv (one per suite)</deliverable>
    <deliverable type="s3">s3://opal-data-bd/diagnostics/nnavar/{run_date}/*/stdout.txt (one per suite)</deliverable>
    <deliverable type="s3">s3://opal-data-bd/diagnostics/nnavar/{run_date}/*/*/metrics.json (one per variant)</deliverable>
    <deliverable type="commit">DT execution log with S3 paths and metrics summary</deliverable>
  </deliverables>

</task_order>
```
