<task_order>
  <metadata>
    <id>ADVI_ROLLUP.ASSETCLASSc</id>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_to>0.4.0_DS_ClientPlatform</issued_to>
    <date>2026-04-24</date>
    <status>complete</status><!-- Completed 2026-04-24. Commit 090d11f6 (CLOUD, pushed). S3 MATCH. Summary: _build_rps_context loads bd_assets_dim, builds is_bond_by_cusip (9,901 entries) + is_bond_by_ticker (7,744 entries) from opal_asset_class==fixed_income. _apply_rps_price_override uses vectorized lookup chain (cusip dim → ticker dim → cost_per_unit heuristic fallback with WARN). Gate clean: py_compile + ds-commit-gate exit 0. from __future__ import annotations added (DSFLOW.004 Rule 15). comp-blast: same terminal consumer set. comp-pipescript deployed: MATCH. RAVC4 to COO pending session log write. -->
    <project_code>ADVI_ROLLUP</project_code>
    <priority>P2 — CP-DS1 follow-up; quality improvement, not portal-blocking</priority>
    <origin>
      ADVI_ROLLUP dashboard standing follow-on from CP-DS1 stabilization (2026-04-17 multi-PIVOT/Gate stack): the `cost_per_unit ≤ 2.0` heuristic for stock/ETF vs cash/bond classification is a stopgap that has false-positives on low-priced stocks + false-negatives on expensive bonds. Replace with deterministic lookup via `bd_assets_dim` (ticker→asset_class) + `ticker_lookup.json` fallback. Surfaced in ADVI_ROLLUP.md blocking (2) and dashboard.
    </origin>
  </metadata>

  <references>
    <ref type="prd">docs/architecture/ADVI_ROLLUP.md (CP-DS1 section; asset_class classification discussion)</ref>
    <ref type="predecessor">ADVI_ROLLUP.CP-DS1 (closed 2026-04-21; `cost_per_unit ≤ 2.0` heuristic shipped as interim)</ref>
    <ref type="data_source">`s3://opal-data-bd/silver/bd_assets_dim/<latest>.parquet` — ticker + cusip + asset_class lookup table</ref>
    <ref type="data_source">`data/black_diamond/scripts/gold/lib/ticker_lookup.json` — curated fallback mappings</ref>
  </references>

  <objective>
    Replace the `cost_per_unit ≤ 2.0` heuristic for asset_class classification in `B_01.holdings_lots.py` (and any co-dependent scripts) with a deterministic lookup chain:

    1. **Primary:** `bd_assets_dim` join by `cusip` (preferred) or `ticker`. Pull `asset_class` directly.
    2. **Fallback:** `ticker_lookup.json` curated mappings for tickers not in dim.
    3. **Final fallback:** retain `cost_per_unit ≤ 2.0` heuristic ONLY when both lookups miss AND emit a WARN diagnostic (count per run; surface in comp-validate).

    Output: same `asset_class` field on the same output schema; populated by deterministic lookup for >95% of rows (measure + document); heuristic used for <5% with WARN log.

    **EXPLICIT SCOPE LOCK:**
    - NO B_01 rewrite; minimal surgical edit to classification logic
    - NO changes to asset_class VALUES or vocabulary (same enum — stock/etf/bond/cash/other); only the MECHANISM
    - NO changes to downstream consumers (C_02, C_05, portal)
    - NO backfill of historical partitions (runs forward from deploy; ingest-level re-run is AE's call if needed)
  </objective>

  <scope>
    <files>
      <file action="modify">data/black_diamond/scripts/gold/B_01.holdings_lots.py — replace heuristic classification block with lookup-chain</file>
      <file action="investigate">data/black_diamond/scripts/gold/B_01b.classify_new_securities.py — verify coordination; no duplicate classification</file>
      <file action="read-only">silver/bd_assets_dim (latest partition) — confirm asset_class coverage on representative sample</file>
      <file action="read-only">data/black_diamond/scripts/gold/lib/ticker_lookup.json — audit fallback coverage</file>
      <file action="modify-if-needed">data/black_diamond/scripts/gold/gold_validate_config.yaml — add heuristic-fallback-ratio WARN threshold (e.g., >5% = ERROR, >2% = WARN)</file>
    </files>
  </scope>

  <deliverables>
    <deliverable id="classification-rewrite">
      B_01 asset_class assignment uses bd_assets_dim primary + ticker_lookup fallback + heuristic only as last-resort with diagnostic counter.
    </deliverable>
    <deliverable id="coverage-metric">
      Post-run diagnostic: count rows classified by each path (dim-cusip / dim-ticker / lookup-json / heuristic). Emit as a single-line log entry + include in comp-validate output.
    </deliverable>
    <deliverable id="validator-block">
      gold_validate_config.yaml rule: heuristic-fallback-ratio > 5% = ERROR (regression); > 2% = WARN (monitor); <= 2% = PASS.
    </deliverable>
    <deliverable id="spot-check">
      Spot-check 20 rows before/after: 10 known-problematic (penny stocks, high-priced bonds) + 10 random. Document asset_class changes (none should change for correctly-classified rows; heuristic misclassifications are the value-add).
    </deliverable>
  </deliverables>

  <acceptance_criteria>
    <ac id="1">B_01 classification logic replaced per lookup chain; diff shows minimal surgical edit (one function / one block).</ac>
    <ac id="2">Heuristic-fallback-ratio on a full-chain run: <= 5% (ERROR threshold) AND documented actual % in session log.</ac>
    <ac id="3">Spot-check 20 rows: document any asset_class flips + rationale. Zero flips on rows classified correctly by old heuristic (guardrail).</ac>
    <ac id="4">No regression on downstream consumers (C_02 canonical_lots, C_05 client_tax_liability, portal) — `comp-blast B_01` post-change shows same consumer set with same asset_class distribution within 5% delta.</ac>
    <ac id="5">py_compile + ds-commit-gate.sh exit 0 pre-commit per CLAUDE.md Rule 14.</ac>
    <ac id="6">`comp-pipescript deployed B_01` MATCH post-S3-upload.</ac>
    <ac id="7">Session log Compiler Tools section reproduces every `<run>` + observed + pass/fail.</ac>
    <ac id="8">MCP COMPLETE to COO with: commit hash + heuristic-fallback-ratio % + spot-check outcome + no-regression evidence.</ac>
  </acceptance_criteria>

  <compiler_tools_mandate>
    <phase id="1" when="before write">
      <step>
        <run>comp-pipescript io B_01</run>
        <expect>READS currently includes silver/unrealized + silver/bd_assets_dim (or surface if dim is NOT a current read). If dim not a read, Phase 1 output drives scope expansion.</expect>
        <if_mismatch>If bd_assets_dim is NOT a current B_01 read, add the read in this TO; document in commit message.</if_mismatch>
      </step>
      <step>
        <run>comp-blast B_01</run>
        <expect>Downstream consumers: C_02, C_05, D_02, D_04 + portal readers. Distribution of asset_class field expected to surface.</expect>
        <if_mismatch>Document any unexpected consumer; coordinate before writing.</if_mismatch>
      </step>
      <step>
        <run>python3 -c "import pyarrow.parquet as pq; df = pq.read_table('s3://opal-data-bd/silver/bd_assets_dim/<latest>.parquet').to_pandas(); print(df['asset_class'].value_counts(); print(df['asset_class'].isna().sum(), 'null')"</run>
        <expect>Print asset_class distribution + null count in bd_assets_dim. Use to estimate primary-path coverage.</expect>
        <if_mismatch>If >20% null asset_class in dim, fallback-path coverage becomes critical; may need to expand ticker_lookup curation.</if_mismatch>
      </step>
    </phase>

    <phase id="2" when="before commit">
      <step>
        <run>python -m py_compile data/black_diamond/scripts/gold/B_01.holdings_lots.py</run>
        <expect>Exit 0.</expect>
        <if_mismatch>Fix syntax.</if_mismatch>
      </step>
      <step>
        <run>.tools/ds-commit-gate.sh data/black_diamond/scripts/gold/B_01.holdings_lots.py</run>
        <expect>Exit 0.</expect>
        <if_mismatch>Fix AST scan issues.</if_mismatch>
      </step>
    </phase>

    <phase id="3" when="after commit">
      <step>
        <run>comp-pipescript deployed B_01</run>
        <expect>MATCH.</expect>
        <if_mismatch>Re-upload.</if_mismatch>
      </step>
      <step>
        <run>comp-validate B_01 --artifact /tmp/holdings_lots_sample.parquet</run>
        <expect>Exit 0; heuristic-fallback-ratio <= 5%.</expect>
        <if_mismatch>Investigate fallback over-trigger (insufficient dim coverage or lookup curation).</if_mismatch>
      </step>
      <step>
        <run>comp-blast B_01</run>
        <expect>Same consumer set as Phase 1 (no new downstream appeared).</expect>
        <if_mismatch>Surface to COO.</if_mismatch>
      </step>
    </phase>
  </compiler_tools_mandate>

  <cross_domain_coordination>
    <shared_resource file="data/black_diamond/scripts/gold/B_01.holdings_lots.py">
      High-blast-radius file. Coordinate with any in-flight TO touching B_01. Check before writing: W4.14 INFLEC B-chain (~A) does NOT touch BD B_01 per its own scope lock.
    </shared_resource>
  </cross_domain_coordination>

  <do_not>
    <rule>Do NOT change asset_class vocabulary/values. Enum stays the same.</rule>
    <rule>Do NOT backfill historical partitions. Forward-deploy only.</rule>
    <rule>Do NOT remove heuristic path entirely — keep as final fallback with WARN.</rule>
    <rule>Do NOT rewrite B_01 broadly — minimal surgical replacement of classification block only.</rule>
  </do_not>
</task_order>
