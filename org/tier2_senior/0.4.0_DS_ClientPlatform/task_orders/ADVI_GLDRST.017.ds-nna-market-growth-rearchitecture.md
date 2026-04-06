<task_order>
  <metadata>
    <id>2.0.0_SA_COO-2026-04-02-gldrst-017-ds</id>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_to>0.4.0_DS_ClientPlatform</issued_to>
    <date>2026-04-02</date>
    <status>complete</status>
    <!-- Completed 2026-04-02. Commit 7fa6947d. Script 05 decomposition: synthetic_aua + market_growth + synthetic_correction columns. -->
    <project_code>ADVI_GLDRST</project_code>
  </metadata>

  <objective>
    Rearchitect script 05 (`05_build_client_performance.py`) to decompose AUA
    changes into NNA, market growth, and synthetic correction components. Currently
    the script outputs `total_aua` and `nna` but never isolates market growth from
    RPS injection effects. With synthetic positions from scripts 02/03, the AUA
    spike on injection dates falsely appears as market growth.
  </objective>

  <context>
    Script 02 (`02_build_positions_cube.py`) writes `gold/synthetic_positions_index.parquet`
    at line 1402 with schema `{account_id, asset_name, trade_date, signed_units}` --
    one row per synthetic buy injected. This file is currently written but unconsumed.

    Approved architecture (Andrew, 2026-04-01):
    ```
    canonical_aua    = positions_cube total (with RPS injection)
    NNA              = cash transfer flows from BD transactions (existing, correct)
    synthetic_aua    = sum(synthetic_positions * canonical_prices) per date
    market_growth    = delta(canonical_aua) - NNA - delta(synthetic_aua)
    ```

    The synthetic injection appears as an "AUA Reconciliation" line item, not
    as market growth.

    PRD: docs/architecture/GLDRST_P3_OPERATIONAL_READINESS.md (Work Stream C)
  </context>

  <scope>
    <files>
      <file action="modify">data/black_diamond/scripts/gold/05_build_client_performance.py</file>
    </files>
  </scope>

  <requirements>
    <requirement id="1">
      Read `gold/synthetic_positions_index.parquet` in script 05. Join with
      `silver/prices/canonical_prices.parquet` on (asset_name, date) to compute
      `synthetic_aua` per (date, relationship_id). Handle the case where the
      file does not exist (no synthetics injected) -- default to 0.
    </requirement>

    <requirement id="2">
      Compute `market_growth` per (date, relationship_id):
      ```
      market_growth = delta(total_aua) - nna - delta(synthetic_aua)
      ```
      Where `delta(x)` is day-over-day change. First date in series has
      `market_growth = 0`.
    </requirement>

    <requirement id="3">
      Add `market_growth` and `synthetic_correction` (= delta(synthetic_aua))
      as new columns in `client_performance.parquet` output. Existing columns
      (`total_aua`, `cum_inflows`, `cum_outflows`, `nna`) remain unchanged.
    </requirement>

    <requirement id="4">
      Document the decomposition formula in the script docstring. The identity
      must hold: `delta(total_aua) = nna + market_growth + synthetic_correction`
      for every (date, relationship_id) row.
    </requirement>
  </requirements>

  <acceptance_criteria>
    <criterion id="1">client_performance.parquet contains market_growth and synthetic_correction columns</criterion>
    <criterion id="2">The identity delta(total_aua) = nna + market_growth + synthetic_correction holds for all rows (within floating point tolerance)</criterion>
    <criterion id="3">When synthetic_positions_index.parquet is absent, market_growth = delta(total_aua) - nna (graceful degradation)</criterion>
    <criterion id="4">Downstream scripts 07/08 still work (they ignore unknown columns)</criterion>
  </acceptance_criteria>

  <constraints>
    <constraint>Do NOT modify scripts 02 or 03 -- synthetic_positions_index.parquet schema is fixed</constraint>
    <constraint>Do NOT rename or remove existing columns in client_performance.parquet</constraint>
    <constraint>canonical_prices join must use the same price source as script 05's existing AUA calculation</constraint>
  </constraints>

  <dependencies>
    <dependency agent="0.6.0_AE_PartnerETL" task="gold-rebuild" status="in-progress">
      Current gold rebuild (PID 39671) must complete successfully before .017
      changes can be tested. Script 02 must have written synthetic_positions_index.parquet.
    </dependency>
  </dependencies>

  <deliverables>
    <deliverable type="commit">Modified 05_build_client_performance.py with decomposition</deliverable>
    <deliverable type="log">Session log with sample output showing the identity holds</deliverable>
  </deliverables>

  <references>
    <ref type="prd">docs/architecture/GLDRST_P3_OPERATIONAL_READINESS.md</ref>
    <ref type="source">data/black_diamond/scripts/gold/05_build_client_performance.py</ref>
    <ref type="source">data/black_diamond/scripts/gold/02_build_positions_cube.py (line 1402 -- synthetic index write)</ref>
  </references>
</task_order>
