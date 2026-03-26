<task_order>
  <metadata>
    <id>2.0.0_SA_COO-2026-03-26-gldrst-002-ae</id>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_to>0.6.0_AE_PartnerETL</issued_to>
    <date>2026-03-26</date>
    <status>pending</status>
    <project_code>ADVI_GLDRST</project_code>
  </metadata>

  <objective>
    Full gold layer rerun to apply the canonical exclusion unification
    (lib/exclusions.py) committed on 2026-03-26. This regenerates all
    downstream parquets and portal artifacts with consistent ghost account
    exclusion, populates mix_timeseries.json aliases, and validates that
    the Books tab and Advisors tab AUA now match.
  </objective>

  <context>
    Five commits landed on CLOUD on 2026-03-26 that require a gold rerun:

    1. 9bca5ff6: mix_timeseries.json alias in 06b + ghost exclusion in 06
    2. 38faa34f: lib/exclusions.py creation + dedup scripts 05+06
    3. df5e8004: Ghost exclusion added to script 05b (fixes ~$7.4M discrepancy)
    4. ae3403f5: Ghost exclusion added to 06b+12, shared insurance AP gate
    5. 16c3139e: DFAC classified as equity / US Small Cap / active

    Expected impact:
    - account_performance.parquet: SUM(total_aua) drops by ~$7.4M (ghost accounts removed)
    - book.json per advisor: summary.total_aua now matches architect_leaderboard.json
    - mix_timeseries.json: 20 new alias files created under gold/advisors/{id}/
    - firm_composition.json + advisor composition.json: ~$7.4M reduction (ghost + insurance AP gate)
    - DFAC holdings reclassified from "Other" to "Equity" in all mix/composition artifacts
  </context>

  <requirements>
    <requirement id="1">
      Pull latest CLOUD to EC2 gold runner instance.
      Verify commits 9bca5ff6 through 16c3139e are present.
    </requirement>

    <requirement id="2">
      Execute FULL gold layer run (not incremental):
        ./run_gold_layer.sh full

      Full run is required because:
      - Script 05b needs to reprocess ALL positions_cube partitions with ghost exclusion
      - Script 06b needs to regenerate ALL per-advisor mix.json + mix_timeseries.json aliases
      - Script 12 needs to regenerate ALL composition artifacts with ghost + insurance AP gate
    </requirement>

    <requirement id="3">
      Post-run validation:
      (a) Cross-validate 05 vs 05b: the built-in cross_validate_vs_client_performance()
          should pass within 0.1% tolerance (was failing before due to ghost mismatch)
      (b) Verify mix_timeseries.json aliases exist:
          aws s3 ls s3://opal-data-bd/gold/advisors/ --recursive | grep mix_timeseries.json
          Expected: 20 files (one per advisor)
      (c) Spot-check one advisor:
          Compare book.json summary.total_aua vs architect_leaderboard.json for the same advisor
          Delta should be < 0.01%
      (d) Verify DFAC classification:
          Download any composition.json, confirm DFAC appears under "equity" asset class
    </requirement>

    <requirement id="4">
      Write a session log at:
        org/tier2_senior/0.6.0_AE_PartnerETL/logs/{date}/
          advi_gldrst_002_gold_rerun_session.md

      Include: run duration, instance type, before/after AUA comparison,
      cross-validation result, mix_timeseries.json alias count, DFAC verification.
    </requirement>
  </requirements>

  <acceptance_criteria>
    <criterion id="1">Full gold layer run completes without errors</criterion>
    <criterion id="2">05b cross_validate_vs_client_performance passes within 0.1%</criterion>
    <criterion id="3">20 mix_timeseries.json alias files exist on S3</criterion>
    <criterion id="4">book.json and architect_leaderboard.json AUA match within 0.01% for spot-checked advisor</criterion>
  </acceptance_criteria>

  <constraints>
    <constraint>Use FULL mode (not incremental) -- ghost exclusion must reprocess all historical partitions</constraint>
    <constraint>Do NOT modify code -- all changes are already committed on CLOUD</constraint>
    <constraint>Prefer c5.4xlarge or larger for full run (r6i.xlarge is too slow for full 05b reprocessing)</constraint>
  </constraints>

  <dependencies>
    <dependency agent="0.4.0_DS_ClientPlatform" task="ADVI_MVPLVL.010" status="complete">
      lib/exclusions.py + all script fixes committed
    </dependency>
  </dependencies>

  <deliverables>
    <deliverable type="artifact">Regenerated gold parquets + portal JSON artifacts on S3</deliverable>
    <deliverable type="document">Session log with validation results</deliverable>
  </deliverables>
</task_order>
