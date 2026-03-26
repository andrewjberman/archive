<task_order>
  <metadata>
    <id>2.0.0_SA_COO-2026-03-26-gldrst-001-ds</id>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_to>0.4.0_DS_ClientPlatform</issued_to>
    <date>2026-03-26</date>
    <status>complete</status>
    <project_code>ADVI_GLDRST</project_code>
  </metadata>

  <objective>
    Extend script 06b to pre-compute quarterly/monthly/annually period views
    at L3 (relationship) level, using the same compute_period_views() function
    that already produces N1 firm and L2 advisor views. This eliminates
    deriveQuarterlyFromTimeseries() from the portal, reduces payload size
    10-50x for the quarterly bar, and ensures methodological consistency
    across all drill levels.

    Also extend script 12 to pre-compute L3 relationship composition artifacts,
    eliminating the ~3s Lambda compute in handle_books_composition().
  </objective>

  <context>
    Triggering finding: DE session log (2026-03-26) identified that N1 uses
    pre-computed quarterly views from script 06b, while L2/L3 derive them
    client-side from daily timeseries. This is fragile (L2 failed due to
    mix_timeseries.json key mismatch), wasteful (~50KB daily JSON transferred
    to extract 4 quarter-end snapshots), and methodologically inconsistent
    (publisher uses exact quarter-end positions; client-side picks nearest
    available daily data point).

    Prerequisite: lib/exclusions.py canonical exclusion stack is complete
    (commits 38faa34f, df5e8004, ae3403f5). All new artifacts will
    automatically inherit ghost + AP gate exclusions.

    Key files:
    - data/black_diamond/scripts/gold/06b_build_client_mix_timeseries.py
    - data/black_diamond/scripts/gold/12_build_composition_artifacts.py
    - data/black_diamond/scripts/gold/lib/exclusions.py
    - org/tier2_senior/0.4.0_DS_ClientPlatform/logs/2026-03-26/advi_gldrst_canonical_methodology_and_precompute.md
    - org/tier2_senior/0.4.0_DE_ClientPlatform/logs/2026-03-26/advi_mvplvl_010_l2_composition_mix_session.md
  </context>

  <scope>
    <files>
      <file action="modify">data/black_diamond/scripts/gold/06b_build_client_mix_timeseries.py</file>
      <file action="modify">data/black_diamond/scripts/gold/12_build_composition_artifacts.py</file>
    </files>
  </scope>

  <requirements>
    <!-- ============================================================ -->
    <!-- WS1: L3 Quarterly Mix Views (script 06b)                     -->
    <!-- ============================================================ -->
    <requirement id="1">
      WS1: Extend _write_relationship_json() in script 06b to also write
      a period-views artifact alongside the daily JSON.

      After accumulating daily_dict for each relationship, call:
        views = compute_period_views(daily_dict)
      and write:
        gold/client_timeseries/{relationship_id}_views.json

      Schema (must match firm_mix_views.json and advisor mix.json):
      {
        "generated_at": "ISO8601Z",
        "data_as_of": "YYYY-MM-DD",
        "relationship_id": "...",
        "views": {
          "quarterly": [FirmMixPeriodPoint...],
          "monthly": [FirmMixPeriodPoint...],
          "annually": [FirmMixPeriodPoint...]
        }
      }

      This runs inside the existing ThreadPoolExecutor write phase.
      compute_period_views() is O(n) on daily entries and takes <10ms
      per relationship. ~1,400 relationships, ~5-10KB each, ~15MB total.
    </requirement>

    <requirement id="2">
      WS1 INCREMENTAL: In incremental mode, the _views.json must be
      rebuilt from the full daily accumulator (not just the new dates).
      The existing pattern is: load existing daily JSON from S3, merge
      new dates, write back. The _views.json should be recomputed from
      the merged accumulator on every incremental run (it's cheap).
    </requirement>

    <!-- ============================================================ -->
    <!-- WS2: L3 Composition Artifacts (script 12)                    -->
    <!-- ============================================================ -->
    <requirement id="3">
      WS2: Extend script 12 to write per-relationship composition artifacts.

      After building firm and per-advisor composition, iterate over
      relationship_ids (via accounts_dimension join on holdings_lots):
        - Group holdings by relationship_id
        - Call _build_composition() for each relationship
        - Write gold/client_timeseries/{relationship_id}_composition.json

      Same schema as firm_composition.json with scope = {relationship_id}.
      This replaces the Lambda's on-the-fly handle_books_composition()
      for relationship-level queries.
    </requirement>

    <requirement id="4">
      WS2 GATE: Script 12 needs relationship_id on holdings_lots.
      Verify that holdings_lots.parquet includes relationship_id column.
      If not, join with accounts_dimension_latest.parquet (account_id ->
      relationship_id) before grouping. Document the join in the session log.
    </requirement>

    <requirement id="5">
      Write a session log at:
        org/tier2_senior/0.4.0_DS_ClientPlatform/logs/{date}/
          advi_gldrst_001_precompute_session.md

      Include:
        - WS1: number of _views.json artifacts written, sample file sizes
        - WS2: number of _composition.json artifacts written, relationship_id join method
        - Commit hashes
        - Explicit next steps for DE (portal wiring) and AE (gold rerun)
    </requirement>
  </requirements>

  <acceptance_criteria>
    <criterion id="1">WS1: gold/client_timeseries/{id}_views.json written for all relationships with same schema as firm_mix_views.json</criterion>
    <criterion id="2">WS1: incremental mode recomputes _views.json from full accumulator</criterion>
    <criterion id="3">WS2: gold/client_timeseries/{id}_composition.json written for all relationships with non-empty mix</criterion>
    <criterion id="4">Session log documents artifact counts, sizes, and next steps</criterion>
  </acceptance_criteria>

  <constraints>
    <constraint>Do NOT modify portal code (DE scope)</constraint>
    <constraint>Do NOT modify Lambda code (AE/DT scope)</constraint>
    <constraint>Do NOT write to S3 -- changes are code-only, AE runs the gold layer</constraint>
    <constraint>Use lib/exclusions.py for all exclusion logic (already wired into 06b and 12)</constraint>
    <constraint>compute_period_views() already exists -- reuse it, do not rewrite</constraint>
  </constraints>

  <dependencies>
    <dependency agent="0.4.0_DS_ClientPlatform" task="ADVI_MVPLVL.010" status="complete">
      lib/exclusions.py, ghost exclusion in 06b+12, mix_timeseries.json alias
    </dependency>
  </dependencies>

  <deliverables>
    <deliverable type="commit">Script 06b: L3 _views.json per-relationship quarterly/monthly/annually</deliverable>
    <deliverable type="commit">Script 12: L3 _composition.json per-relationship</deliverable>
    <deliverable type="document">Session log with artifact counts and next steps</deliverable>
  </deliverables>
</task_order>
