# Task Order: ACAT In-Kind NNA — Cloud Testing and Production Design — 0.4.0_DS_ClientPlatform

```xml
<task_order>
  <metadata>
    <id>2.0.0_SA_COO-2026-03-05-acat-inkind-nna-testing</id>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_to>0.4.0_DS_ClientPlatform</issued_to>
    <date>2026-03-05</date>
    <status>complete</status>
    <priority>HIGH — CEO-directed. Addresses $106M inflow gap vs Schwab TOA.</priority>
    <completion_date>2026-03-05</completion_date>
  </metadata>

  <context>
    Three diagnostic scripts were written this session to investigate ACAT in-kind NNA
    undercount (diag_acat_inkind_scan.py, v2, v3). v3 is the most refined implementation,
    using a 30-day onboarding window per account with FIFO netting:

      acat_estimate = gross_buys - total_nna_in - total_sells  (clipped to 0)

    These scripts are untracked and have not been committed. Running them locally crashes
    the machine — full silver/transactions history is too large for a local environment.
    ALL execution must happen in the cloud on the BD EC2 instance.

    CEO has approved this investigation. The goal is to thoroughly test the methodology,
    understand results at full scale, and determine the best path to production integration
    in script 05. This is NOT a "run once and ship" task — testing and design quality matter.
  </context>

  <objective>
    Commit the ACAT diagnostic scripts, run the full-history scan on EC2 (via S3 artifact
    model), analyze the output thoroughly, stress-test the methodology against known edge
    cases, and produce a design recommendation for how to integrate the 30-day onboarding
    FIFO logic into script 05 as a production NNA supplement.
  </objective>

  <requirements>

    <!-- ================================================================ -->
    <!-- STEP 1 — Commit the scripts                                      -->
    <!-- ================================================================ -->
    <requirement id="1">
      Commit all three diagnostic scripts to CLOUD. They are currently untracked at:
        data/black_diamond/scripts/diagnostics/diag_acat_inkind_scan.py
        data/black_diamond/scripts/diagnostics/diag_acat_inkind_scan_v2.py
        data/black_diamond/scripts/diagnostics/diag_acat_inkind_scan_v3.py

      Commit with DS authorship:
        git add data/black_diamond/scripts/diagnostics/diag_acat_inkind_scan*.py
        git commit --author="0.4.0_DS_ClientPlatform &lt;0.4.0_DS_ClientPlatform@opal.agent&gt;" \
          -m "0.4.0_DS_ClientPlatform: add ACAT in-kind NNA diagnostic scripts v1/v2/v3"

      DO NOT push — DT handles all pushes.
    </requirement>

    <!-- ================================================================ -->
    <!-- STEP 2 — Write a DT brief for EC2 execution                     -->
    <!-- ================================================================ -->
    <requirement id="2">
      Write a brief for 0.4.0_DT_ClientPlatform at:
        docs/briefs/devops-brief-acat-inkind-nna-ec2-run.md

      The brief must specify:
        - Script to run: diag_acat_inkind_scan_v3.py (v3 is the production-candidate version)
        - EC2 target: the BD gold layer runner instance (same instance that runs run_gold_layer.sh)
        - S3 artifact path to upload to: s3://opal-data-bd/scripts/diagnostics/diag_acat_inkind_scan_v3.py
        - Run command on EC2 (after pulling from S3):
            python /tmp/diag_acat_inkind_scan_v3.py 2>&1 | tee /tmp/acat_scan_v3_output.txt
        - Output capture: upload stdout to s3://opal-data-bd/diagnostics/acat_scan_v3_output.txt
          so DS can read results without SSH access
        - AWS CLI to download the output:
            aws s3 cp s3://opal-data-bd/diagnostics/acat_scan_v3_output.txt - | cat
        - Context: script loads ALL silver/transactions partitions (full history).
          Memory requirement is substantial. If the instance OOMs, DT should note that
          and DS will refactor to a chunked/streaming approach.
        - No Terraform changes needed — this is a one-off diagnostic run, not a pipeline deploy.
        - Follow EC2_CODE_DEPLOYMENT_STANDARD.md: code goes repo -> S3 -> EC2, never inline in SSM.

      Commit the brief with DS authorship. Signal DT via session log (DT reads DS logs on startup).
    </requirement>

    <!-- ================================================================ -->
    <!-- STEP 3 — Analyze output after DT runs v3                        -->
    <!-- ================================================================ -->
    <requirement id="3">
      After DT runs the scan and the output is in S3, read it and document findings in a
      session log. The analysis MUST cover:

      3a. Gap closure headline:
        - What % of the 13-month $106M inflow gap is recovered by the ACAT estimate?
        - Month-by-month: which months improve most, which overshoot?
        - Does the adjustment cause any month's gap to FLIP sign (over-adjustment)?

      3b. Volume sanity checks:
        - Total accounts flagged vs total onboarded accounts (what % are ACAT arrivals?)
        - Distribution of acat_estimate values: are there outliers that inflate the total?
        - Cross-check against the known zero-inflow relationships (408 relationships,
          $77M AUA documented in 2026-02-27 session). Do they dominate the ACAT flagged set?

      3c. Edge case audit — examine the top 25 accounts by ACAT estimate:
        - Do the top accounts look like genuine ACAT transfers (diverse asset names,
          non-model ETFs like Fidelity Contra Pool, mutual funds)?
        - Or do they look like model rebalances that slipped through (only standard
          firm ETFs, coordinated buy dates across many accounts)?
        - For any suspicious top-25 account: pull the raw transactions and verify
          the FIFO arithmetic manually.

      3d. BURST_THRESHOLD sensitivity:
        - v3 uses BURST_THRESHOLD=3 (minimum 3 buys in window). Test with 2 and 5.
        - Quantify how much the total ACAT estimate changes. A stable estimate across
          thresholds (2 to 5) indicates the signal is robust. Wild swings indicate
          the threshold is doing heavy lifting and the underlying signal is noisy.

      3e. Onboarding window sensitivity:
        - v3 uses 30 days. Also test with 14 days and 45 days.
        - Rationale: ACAT advisors who move fast (< 2 weeks) may fall through a 30-day
          window; advisors who take their time (> 30 days) may be missed.
        - Does 14 vs 45 days change the total materially? If yes, document which
          population is responsible for the difference.
    </requirement>

    <!-- ================================================================ -->
    <!-- STEP 4 — Production design brief                                 -->
    <!-- ================================================================ -->
    <requirement id="4">
      After completing the analysis, write a production design brief at:
        docs/briefs/data-scientist-acat-inkind-nna-production-design.md

      The brief must answer:

      4a. RECOMMENDED APPROACH (choose one, justify):
        Option A — Supplemental inflow credit in script 05:
          After load_flows_from_transactions(), run the onboarding-window FIFO scan,
          compute acat_estimate per account, and add a synthetic 'ACAT_INKIND' inflow
          row to the flows DataFrame for each qualifying account.
          Pro: flows into all downstream scripts (09, 10) automatically.
          Con: synthetic rows require careful labeling to remain distinguishable from
          real transactions. Cumulative flow figures will reflect the adjustment.

        Option B — Post-hoc adjustment at the output layer (script 09):
          Generate the ACAT estimate separately and add it as an additive correction
          to the inflow totals in header_metrics.json / timeseries_chart.json.
          Pro: does not alter the raw flow records; adjustment is explicit and auditable.
          Con: must be replicated in script 10 (advisor_rolling_flows) and any future
          scripts that consume client_performance.parquet. Maintenance burden grows.

        Option C — Separate ACAT inflow file:
          Write a new script (e.g., 05c_estimate_acat_inkind.py) that produces
          a parquet of ACAT-estimated inflows per account per onboarding month.
          Scripts 09 and 10 optionally merge this in.
          Pro: cleanly separable from main NNA pipeline; easy to disable if wrong.
          Con: adds a pipeline dependency; run_gold_layer.sh needs updating.

      4b. RECOMMENDED PARAMETER VALUES (based on sensitivity testing in step 3):
        - ONBOARDING_DAYS: 30 (or justify different value)
        - BURST_THRESHOLD: 3 (or justify different value)
        - Any additional guards to add

      4c. FALSE POSITIVE RISK ASSESSMENT:
        - What is the probability that the ACAT estimate includes genuine investment
          decisions that should NOT count as NNA? Quantify if possible.
        - Propose one or two additional guard conditions that would reduce false positives
          without material impact on gap closure.

      4d. SCHWAB RECONCILIATION TARGET:
        - After implementing the recommended approach, what adjusted 13-month NNA
          figure do we expect vs Schwab's $354.7M?
        - Is over-adjustment a risk? (Our adjusted inflows > Schwab TOA In for any month?)
        - Note: Schwab's NNA includes FDIC sweeps which we already exclude. Our adjusted
          figure does not need to match Schwab exactly — it needs to be directionally
          consistent and remove the sign reversals.

      4e. REBUILD SEQUENCE (if Option A or C):
        - Which scripts need to run after the new ACAT logic is live?
        - What full-history rebuild does this require?
        - Estimate runtime impact (reference existing timing from run_gold_layer.sh logs).
    </requirement>

  </requirements>

  <acceptance_criteria>
    <criterion id="1">diag_acat_inkind_scan_v1/v2/v3.py committed to CLOUD under DS authorship.</criterion>
    <criterion id="2">DT brief written at docs/briefs/devops-brief-acat-inkind-nna-ec2-run.md with complete S3/EC2 instructions.</criterion>
    <criterion id="3">v3 scan output captured to s3://opal-data-bd/diagnostics/acat_scan_v3_output.txt by DT.</criterion>
    <criterion id="4">Session log documents gap closure headline, volume sanity checks, top-25 account audit, and both sensitivity tests (threshold + window).</criterion>
    <criterion id="5">Production design brief at docs/briefs/data-scientist-acat-inkind-nna-production-design.md with recommended approach, parameter values, false positive assessment, and rebuild sequence.</criterion>
    <criterion id="6">No changes made to script 05 or any production gold layer script during this task. Testing only — implementation follows after COO reviews the design brief.</criterion>
  </acceptance_criteria>

  <constraints>
    <constraint>
      DO NOT run any diagnostic script locally. The silver/transactions dataset is too large
      for local execution and will crash the machine. All execution happens on EC2 via the
      S3 artifact model (EC2_CODE_DEPLOYMENT_STANDARD.md). Write the DT brief and wait for
      cloud output before doing any analysis.
    </constraint>
    <constraint>
      DO NOT modify script 05, 09, 10, or any production gold layer script during this task.
      This is a testing and design phase. The implementation task order will be issued separately
      after COO and CEO review the design brief.
    </constraint>
    <constraint>
      DS cannot push or deploy to AWS. Write the DT brief and commit locally.
      DT handles S3 upload, EC2 execution, and output capture.
      DT handles pushing CLOUD after DS commits.
    </constraint>
    <constraint>
      The design brief (Step 4) is the primary deliverable for CEO review. It must be
      self-contained — a reader with no prior context should be able to understand the
      problem, the methodology, and the recommendation without reading the diagnostic scripts.
    </constraint>
    <constraint>
      Follow the canonical NNA exclusion logic (JNL - LONG/SHORT, TRF BTWN SCH ACCTS,
      TO SEP ACCT MGR, TRANSFER FUNDS TO SCHWAB BANK) from the 2026-03-05 canonical_nna_logic.md
      session. v3 already includes these exclusions in its nna_mask. Do not revert them.
    </constraint>
  </constraints>

  <dependencies>
    <dependency agent="0.4.0_DT_ClientPlatform" task="EC2 run of diag_acat_inkind_scan_v3.py"
                status="pending" note="DS writes brief (Step 2); DT executes; DS reads S3 output (Step 3)"/>
  </dependencies>

  <deliverables>
    <deliverable type="commit">diag_acat_inkind_scan_v1/v2/v3.py committed to data/black_diamond/scripts/diagnostics/</deliverable>
    <deliverable type="document">docs/briefs/devops-brief-acat-inkind-nna-ec2-run.md — DT execution instructions</deliverable>
    <deliverable type="document">Session log with full analysis of v3 output (gap closure, sanity checks, sensitivity tests)</deliverable>
    <deliverable type="document">docs/briefs/data-scientist-acat-inkind-nna-production-design.md — production implementation recommendation</deliverable>
  </deliverables>
</task_order>
```
