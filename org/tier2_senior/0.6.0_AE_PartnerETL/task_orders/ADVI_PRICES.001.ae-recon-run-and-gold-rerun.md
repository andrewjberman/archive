<task_order>
  <metadata>
    <id>2.0.0_SA_COO-2026-03-23-prices-001-ae</id>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_to>0.6.0_AE_PartnerETL</issued_to>
    <date>2026-03-23</date>
    <status>complete</status>
    <project_code>ADVI_PRICES</project_code>
    <thread_serial>ADVI_PRICES-001</thread_serial>
    <thread_ref>org/threads/ADVI_PRICES-001-lot-valuation-reconciliation-investigati/</thread_ref>
  </metadata>

  <objective>
    Two workstreams after DS delivers the taxonomy expansion and diagnostic script:

    WS1: Upload DS's updated 03_build_holdings_lots.py and recon_lots_vs_allocations.py
    to S3, then run a FULL gold layer rerun to produce corrected holdings_lots with
    expanded exit type recognition.

    WS2: Run the reconciliation diagnostic against the new holdings_lots output and
    compare to the 2026-03-19 baseline. Quantify how much of the $91M phantom excess
    was resolved by the taxonomy expansion.
  </objective>

  <scope>
    <files>
      <file action="upload-to-s3">data/black_diamond/scripts/gold/03_build_holdings_lots.py</file>
      <file action="upload-to-s3">data/black_diamond/scripts/diagnostics/recon_lots_vs_allocations.py</file>
      <file action="run-on-ec2">run_gold_layer.sh (full mode)</file>
      <file action="run-on-ec2">recon_lots_vs_allocations.py</file>
    </files>
  </scope>

  <requirements>
    <requirement id="1">
      WS1 — Upload updated scripts to S3 and run full gold layer.

      PRE-FLIGHT: Verify DS commits are on CLOUD and the expanded SELL_TYPES
      are present in 03_build_holdings_lots.py.

      Upload sequence:
        aws s3 sync data/black_diamond/scripts/gold/ s3://opal-data-bd/code/gold/
        aws s3 cp data/black_diamond/scripts/diagnostics/recon_lots_vs_allocations.py \
          s3://opal-data-bd/code/diagnostics/recon_lots_vs_allocations.py

      Run: bash run_gold_layer.sh full
      Monitor to completion. Record wall time and any errors.
    </requirement>

    <requirement id="2">
      WS2 — Post-rerun reconciliation.

      After the full gold rerun completes and holdings_lots/{date}.parquet is written:
        python3 recon_lots_vs_allocations.py --date {date}

      Compare to baseline (2026-03-19):
        - Phantom accounts: was 269 (+$91M). What is it now?
        - Missing lots: was 156 (-$28M). Expected unchanged.
        - Net gap: was +$25.6M (+1.6%). What is it now?

      Save comparison output to session log.
    </requirement>
  </requirements>

  <acceptance_criteria>
    <criterion id="1">Full gold rerun completes without errors</criterion>
    <criterion id="2">Post-rerun reconciliation shows reduced phantom count and $ excess vs baseline</criterion>
    <criterion id="3">Results documented in session log with before/after comparison</criterion>
  </acceptance_criteria>

  <constraints>
    <constraint>Do NOT run until DS WS1 and WS2 commits are on CLOUD</constraint>
    <constraint>Follow safe-ec2-deploy.sh for any code uploads if EC2_MANIFEST applies</constraint>
    <constraint>No emojis in code or log output (CLAUDE.md rule 13)</constraint>
  </constraints>

  <dependencies>
    <dependency agent="0.4.0_DS_ClientPlatform" task="ADVI_PRICES.001.ds-txn-taxonomy-and-recon-diagnostic" status="pending">
      DS must commit expanded SELL_TYPES and recon_lots_vs_allocations.py before AE runs.
    </dependency>
  </dependencies>

  <deliverables>
    <deliverable type="deploy">Updated 03_build_holdings_lots.py deployed to EC2 via S3</deliverable>
    <deliverable type="verify">Full gold rerun completed + reconciliation comparison</deliverable>
    <deliverable type="document">Session log with before/after reconciliation waterfall</deliverable>
  </deliverables>
</task_order>
