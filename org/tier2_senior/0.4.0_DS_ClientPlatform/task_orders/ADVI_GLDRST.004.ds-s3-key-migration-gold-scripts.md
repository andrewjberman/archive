<task_order>
  <metadata>
    <id>2.0.0_SA_COO-2026-03-26-gldrst-004-ds</id>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_to>0.4.0_DS_ClientPlatform</issued_to>
    <date>2026-03-26</date>
    <status>pending</status>
    <project_code>ADVI_GLDRST</project_code>
  </metadata>

  <objective>
    Migrate all 13 gold scripts to the new S3 key layout enforcing
    medallion boundaries and organizational conventions. This is the
    core S3 restructure — every script's read/write paths change.

    The new layout organizes keys by type:
      gold/dimensions/       — dimension tables (accounts, clients, advisor assignments)
      gold/timeseries/       — daily partitioned data (positions_cube, holdings_lots)
      gold/views/            — pre-aggregated analytics tables (nna_by_*, architect_*)
      gold/artifacts/        — portal-ready JSON artifacts (firm_mix, composition, etc.)
      gold/entities/         — per-entity directories (advisors/{id}/, clients/{id}/)
      gold/validation/       — AUA certification, validation reports
      gold/meta/             — pipeline-complete.json, watermarks, manifests
  </objective>

  <context>
    Current flat layout has ~45 S3 keys scattered without consistent conventions:
    - gold/accounts_dimension_latest.parquet (dimension, should be gold/dimensions/)
    - gold/client_performance.parquet (timeseries, should be gold/timeseries/)
    - gold/views/nna_aua_by_advisor.parquet (already in views/, correct)
    - gold/firm_mix_views.json (artifact, should be gold/artifacts/)
    - gold/advisors/{id}/composition.json (entity, already correct pattern)
    - gold/pipeline-complete.json (meta, should be gold/meta/)

    Copy-then-switch migration: write to NEW paths first, verify, then
    update read paths. Old keys remain until all consumers are migrated.
    Rollback = revert read paths to old keys.

    Key files: all 13 scripts in data/black_diamond/scripts/gold/
    Reference: lib/config.py for S3_BUCKET
  </context>

  <scope>
    <files>
      <file action="create">data/black_diamond/scripts/gold/lib/s3_layout.py</file>
      <file action="modify">data/black_diamond/scripts/gold/00_build_accounts_dimension.py</file>
      <file action="modify">data/black_diamond/scripts/gold/01_build_advisor_assignments_history.py</file>
      <file action="modify">data/black_diamond/scripts/gold/02_build_positions_cube.py</file>
      <file action="modify">data/black_diamond/scripts/gold/03_build_holdings_lots.py</file>
      <file action="modify">data/black_diamond/scripts/gold/04_build_client_dimension.py</file>
      <file action="modify">data/black_diamond/scripts/gold/05_build_client_performance.py</file>
      <file action="modify">data/black_diamond/scripts/gold/05b_build_account_performance.py</file>
      <file action="modify">data/black_diamond/scripts/gold/05c_validate_aua_vs_silver.py</file>
      <file action="modify">data/black_diamond/scripts/gold/05d_write_aua_certification.py</file>
      <file action="modify">data/black_diamond/scripts/gold/06_build_client_tax_liability.py</file>
      <file action="modify">data/black_diamond/scripts/gold/06b_build_client_mix_timeseries.py</file>
      <file action="modify">data/black_diamond/scripts/gold/07_build_nna_aua_by_geography.py</file>
      <file action="modify">data/black_diamond/scripts/gold/08_build_nna_aua_by_advisor.py</file>
      <file action="modify">data/black_diamond/scripts/gold/08b_build_architect_attribution.py</file>
      <file action="modify">data/black_diamond/scripts/gold/09_generate_partner_analytics.py</file>
      <file action="modify">data/black_diamond/scripts/gold/10_generate_advisor_rolling_flows.py</file>
      <file action="modify">data/black_diamond/scripts/gold/12_build_composition_artifacts.py</file>
    </files>
  </scope>

  <requirements>
    <requirement id="1">
      Create lib/s3_layout.py — centralized S3 key registry.
      Every S3 key used by any gold script is defined here as a constant
      or function. Scripts import keys from this module instead of
      hardcoding strings. This makes future key changes a single-file edit.

      Structure:
        # Dimensions
        ACCOUNTS_DIMENSION = 'gold/dimensions/accounts_dimension_latest.parquet'
        ADVISOR_ASSIGNMENTS = 'gold/dimensions/advisor_assignments_history.parquet'
        CLIENT_DIMENSION = 'gold/dimensions/client_dimension.parquet'

        # Timeseries (partitioned)
        def positions_cube_key(date_str): return f'gold/timeseries/positions_cube/{date_str}.parquet'
        def holdings_lots_key(date_str): return f'gold/timeseries/holdings_lots/{date_str}.parquet'
        CLIENT_PERFORMANCE = 'gold/timeseries/client_performance.parquet'
        ACCOUNT_PERFORMANCE = 'gold/timeseries/account_performance.parquet'

        # Views
        NNA_AUA_BY_ADVISOR = 'gold/views/nna_aua_by_advisor.parquet'
        NNA_AUA_BY_GEOGRAPHY = 'gold/views/nna_aua_by_geography.parquet'
        ...etc

        # Artifacts (portal-ready JSON)
        FIRM_MIX_VIEWS = 'gold/artifacts/firm_mix_views.json'
        FIRM_COMPOSITION = 'gold/artifacts/firm_composition.json'
        ADVISOR_ROLLING_FLOWS = 'gold/artifacts/advisor_rolling_flows.json'
        ...etc

        # Entities
        def advisor_composition(advisor_id): return f'gold/entities/advisors/{advisor_id}/composition.json'
        def advisor_mix(advisor_id): return f'gold/entities/advisors/{advisor_id}/mix.json'
        def client_timeseries(rel_id): return f'gold/entities/clients/{rel_id}/timeseries.json'
        ...etc

        # Meta
        PIPELINE_COMPLETE = 'gold/meta/pipeline-complete.json'
        WATERMARK = 'gold/meta/client_timeseries_watermark.json'

        # Validation
        def aua_certification(date_str): return f'gold/validation/aua_certification/{date_str}.json'
    </requirement>

    <requirement id="2">
      Phase A (write-side migration): Update all script WRITE paths to new layout.
      Scripts write to NEW keys. Old keys are NOT removed yet.
      Each script also writes a COPY to the OLD key path for backward
      compatibility (dual-write) until all consumers are migrated.

      This is the safe phase — old paths still work, new paths start populating.
    </requirement>

    <requirement id="3">
      Phase B (read-side migration): Update all script READ paths to new layout.
      After a full gold rerun confirms new keys exist, switch reads to new paths.
      This phase requires coordination with .005 (Lambda) and .006 (CloudFront).

      Phase B commits should be separate from Phase A so they can be
      reverted independently (rollback = revert Phase B, old keys still exist).
    </requirement>

    <requirement id="4">
      Document the complete key migration map in the session log:
      | Old Key | New Key | Script(s) Using |
    </requirement>
  </requirements>

  <acceptance_criteria>
    <criterion id="1">lib/s3_layout.py created with all ~45 S3 keys as named constants/functions</criterion>
    <criterion id="2">Phase A: all 13 scripts dual-write to old + new paths</criterion>
    <criterion id="3">Phase B: all 13 scripts read from new paths</criterion>
    <criterion id="4">Session log contains complete key migration map</criterion>
  </acceptance_criteria>

  <constraints>
    <constraint>Do NOT delete old S3 keys — Lambdas still read from them until .005/.006</constraint>
    <constraint>Dual-write in Phase A to prevent breakage during transition</constraint>
    <constraint>Phase B requires .005 (Lambda) and .006 (CloudFront) to be ready</constraint>
    <constraint>Copy-then-switch: never remove old keys before consumers migrate</constraint>
  </constraints>

  <dependencies>
    <dependency agent="0.4.0_DS_ClientPlatform" task="ADVI_GLDRST.001" status="pending">
      Pre-compute expansion should land before migration to avoid double-moving new artifacts
    </dependency>
    <dependency agent="0.6.0_AE_PartnerETL" task="ADVI_GLDRST.002" status="pending">
      Gold rerun validates exclusion fixes before migration begins
    </dependency>
  </dependencies>

  <deliverables>
    <deliverable type="commit">lib/s3_layout.py — centralized S3 key registry</deliverable>
    <deliverable type="commit">Phase A: all scripts dual-write to old + new paths</deliverable>
    <deliverable type="commit">Phase B: all scripts read from new paths (separate commit)</deliverable>
    <deliverable type="document">Session log with complete key migration map</deliverable>
  </deliverables>
</task_order>
