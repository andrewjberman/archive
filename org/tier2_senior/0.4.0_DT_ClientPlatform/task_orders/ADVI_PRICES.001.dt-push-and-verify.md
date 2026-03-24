<task_order>
  <metadata>
    <id>2.0.0_SA_COO-2026-03-23-prices-001-dt</id>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_to>0.4.0_DT_ClientPlatform</issued_to>
    <date>2026-03-23</date>
    <status>pending</status>
    <project_code>ADVI_PRICES</project_code>
    <thread_serial>ADVI_PRICES-001</thread_serial>
    <thread_ref>org/threads/ADVI_PRICES-001-lot-valuation-reconciliation-investigati/</thread_ref>
  </metadata>

  <objective>
    QA gate and push for DS's ADVI_PRICES commits, then verify post-rerun
    reconciliation results after AE completes the gold rerun.

    This is a lightweight DT task — no Terraform or Lambda changes involved.
    The work is purely gold-layer script changes (transaction taxonomy expansion)
    and a new diagnostic script.
  </objective>

  <scope>
    <files>
      <file action="review">data/black_diamond/scripts/gold/03_build_holdings_lots.py</file>
      <file action="review">data/black_diamond/scripts/diagnostics/recon_lots_vs_allocations.py</file>
    </files>
  </scope>

  <requirements>
    <requirement id="1">
      Review DS's commits for ADVI_PRICES:
      - 03_build_holdings_lots.py: verify SELL_TYPES/CA_SELL_SUBTYPES expansion
        is additive only (no removal of existing types), and each addition has
        a rationale comment.
      - recon_lots_vs_allocations.py: verify it reads from expected S3 paths,
        handles missing data gracefully, and produces the waterfall output.
    </requirement>

    <requirement id="2">
      Push DS commits to CLOUD remote after QA review.
    </requirement>

    <requirement id="3">
      After AE completes the gold rerun and reconciliation (ADVI_PRICES.001 AE WS3):
      - Review the before/after reconciliation comparison
      - Confirm phantom account count and $ excess decreased
      - If net gap is within 1% of BD AUA, mark as acceptable
      - If net gap > 1%, flag remaining root causes to COO
    </requirement>
  </requirements>

  <acceptance_criteria>
    <criterion id="1">DS commits reviewed and pushed to CLOUD remote</criterion>
    <criterion id="2">Post-rerun reconciliation reviewed with pass/fail assessment</criterion>
  </acceptance_criteria>

  <constraints>
    <constraint>Do NOT push until DS commits are reviewed</constraint>
    <constraint>Do NOT modify the scripts — DS owns the code</constraint>
  </constraints>

  <dependencies>
    <dependency agent="0.4.0_DS_ClientPlatform" task="ADVI_PRICES.001.ds-txn-taxonomy-and-recon-diagnostic" status="pending">
      DS must commit both WS1 and WS2 before DT reviews/pushes.
    </dependency>
    <dependency agent="0.6.0_AE_PartnerETL" task="ADVI_PRICES.001.ae-recon-run-and-gold-rerun" status="pending">
      AE must complete gold rerun and reconciliation before DT does final verification.
    </dependency>
  </dependencies>

  <deliverables>
    <deliverable type="commit">Push DS commits to CLOUD remote</deliverable>
    <deliverable type="document">QA review notes + post-rerun pass/fail in session log</deliverable>
  </deliverables>
</task_order>
