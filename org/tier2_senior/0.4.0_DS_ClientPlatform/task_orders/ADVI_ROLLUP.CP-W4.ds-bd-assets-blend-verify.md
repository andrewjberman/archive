<task_order>
  <metadata>
    <id>ADVI_ROLLUP.CP-W4</id>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_to>0.4.0_DS_ClientPlatform</issued_to>
    <date>2026-04-17</date>
    <status>complete</status>
    <project_code>ADVI_ROLLUP</project_code>
    <priority>P0 — gates CP-AE1 backfill join correctness</priority>
    <supersedes>BDPL_ASTDIM.W4.ds-build-bd-assets-dim.md</supersedes>
  </metadata>

  <context>
    AE compacted silver/bd_assets.parquet (3.19M rows) as part of BDPL_ASTDIM W5-W6.
    CTO flagged at W4 issue time: unclear whether the AE-compacted file applied the
    BD-first / ETFClassifier-fallback blend rule (D3 from the PRD). If the blend was not
    applied, the CUSIP → asset_class mapping downstream will be wrong.

    CP-AE1 (AE) will join silver/transactions on asset_id → cusip using this file.
    If bd_assets.parquet has bad super_class data, it doesn't block the CUSIP join —
    but must be confirmed before DS uses it as a classification source in CP-DS1.
  </context>

  <objective>
    Inspect the live silver/bd_assets.parquet for blend-rule presence.
    Fast verification — sample the file, check super_class source provenance.
    Two outcomes:
      (a) Blend applied: document + signal AE they can proceed with full backfill.
      (b) Blend NOT applied: rebuild via build_bd_assets_dim.py with BD-first/ETFClassifier-fallback,
          atomically replace S3 object, re-verify. Coordinate with AE before overwriting
          if AE's backfill is in flight.
  </objective>

  <tasks>
    1. Read silver/bd_assets.parquet (sample 10k rows or full schema).
       Check: does a `super_class_source` or equivalent provenance column exist?
       If yes: count BD-wins vs ETFClassifier-fallback vs both-null.
       If no column: sample super_class values and cross-reference against
       known BD super_class vocab (from W2 recon doc) to infer whether blend was applied.
    2. Determine: blend applied (go to step 4) or not applied (go to step 3).
    3. If rebuild needed:
       - Run build_bd_assets_dim.py with BD-first/ETFClassifier-fallback blend rule.
       - Verify: row count >= 10,000, asset_id zero duplicates, super_class >= 95% non-null.
       - Upload to s3://opal-data-bd/silver/bd_assets.parquet (atomic replace).
       - Coordinate with AE: hold CP-AE1 backfill until upload is confirmed.
    4. Commit blend recon log to data/black_diamond/scripts/diagnostics/output/bd_assets_blend_verify_{YYYY-MM-DD}.json.
       Fields: total_rows, bd_wins, etfclassifier_fallback, both_null, blend_applied (bool), rebuild_performed (bool).
  </tasks>

  <acceptance_criteria>
    1. silver/bd_assets.parquet confirmed: asset_id zero duplicates, super_class >= 95% non-null.
    2. Blend recon log committed with bd_wins + etfclassifier_fallback + both_null counts.
    3. If rebuild performed: build_bd_assets_dim.py committed + S3 upload confirmed.
    4. AE signaled (MCP) that CP-W4 is COMPLETE and they can proceed with full backfill.
    5. MCP COMPLETE to COO with blend status, row count, and any rebuild performed.
  </acceptance_criteria>

  <compiler_tools_mandate>
    Phase 1 (before any write):
      comp-pipescript io build_bd_assets_dim.py (if rebuild path taken) — confirm I/O.
      comp-blast silver/bd_assets — confirm downstream consumers before atomic replace.
    Phase 2 (if rebuild):
      python -m py_compile build_bd_assets_dim.py.
      comp-validate silver/bd_assets.parquet after upload.
  </compiler_tools_mandate>

  <dependencies>
    None — silver/bd_assets.parquet exists (W7 complete). Proceed immediately.
  </dependencies>

  <next>
    CP-W4 COMPLETE signals AE (CP-AE1) to proceed with full historical backfill.
  </next>
</task_order>
