<?xml version="1.0" encoding="UTF-8"?>
<task_order>
  <metadata>
    <id>ADVI_INFETL.MDR</id>
    <project>ADVI_INFETL</project>
    <title>Master Data Registry — canonical Inflection pipeline data graph (all tiers, producers, consumers, schema, status)</title>
    <issued_to>0.4.0_DS_ClientPlatform~A</issued_to>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_date>2026-05-07</issued_date>
    <status>active</status>
    <priority>high</priority>
    <estimated_effort>~1.5d (compiler-aided enumeration + doc authoring)</estimated_effort>
  </metadata>

  <references>
    <ref type="andrew_directive">2026-05-07 — "we need master data registry very badly for the inflection pipeline, we need to clean that up and make sure its canonical because we cannot be having these issues of not knowing where buckets are and what is in use versus what is not. i would recommend getting in touch with DS~A because they were working on some compilers specific to inflection pipeline, and we should be using compilers more frequently with this in mind so that we can move more quickly and accurately in this subject"</ref>
    <ref type="trigger_incidents">2026-05-07 backfill audit revealed: performance writes to bronze/performance/ (NOT bronze/orion-api/{date}/performance_dim.csv as expected); representatives writes to bronze/orion-api-v2/ (NOT bronze/orion-api/); only 1 performance file exists; portal-route audit (df0b18942) found 16 gold-read violations; shared-advisor-router code drift (R3). Common root cause: no canonical registry of "where does X live + who writes it + who reads it + what's the schema."</ref>
    <ref type="ds_a_compiler_context">DS~A shipped INF support to compilers today (7ee141664) — extract_validate.py + validate_cli.py + comp-tools.yaml. INF gold validate config now supported; INF pipeline auto-detection in comp-validate. Use these as foundation.</ref>
    <ref type="related_TO">INFETL.DAILY-AUDIT (AE 0.7) — operational daily-pull matrix. Overlaps but narrower than MDR. Coordinate so MDR absorbs DAILY-AUDIT findings rather than duplicating.</ref>
    <ref type="output_target">docs/architecture/INFETL_MASTER_DATA_REGISTRY.md (NEW) + docs/architecture/inf_data_graph.yaml (NEW, machine-readable)</ref>
  </references>

  <context>
    The Inflection pipeline has accumulated multiple S3 path conventions, multiple
    bronze prefixes (bronze/orion-api/, bronze/orion-api-v2/, bronze/performance/,
    bronze/assets/, bronze/positions/, bronze/billing/), multiple silver layouts
    (silver/api_dims/, silver/transactions/), and a gold/platinum split that the
    portal-route audit (df0b18942) just flagged as having 16 violations.

    Without a canonical registry, every change risks discovering a path drift only
    when something breaks. The performance backfill blank-spot today is the latest
    example: I assumed performance wrote to bronze/orion-api/{date}/performance_dim.csv
    (matching tax/billing pattern) — actually writes to bronze/performance/{date}.parquet.
    No mechanism caught the assumption.

    This TO produces the canonical registry: every Inflection data artifact across
    bronze/silver/gold/platinum, with producer + consumers + schema + status +
    coverage. Compiler tools enumerate where humans miss.
  </context>

  <scope>
    <step>
      Compiler-aided enumeration. Use these tools to populate the registry without
      manually grep-ing 2k lines per script:

        comp-pipescript io {script} — input/output enumeration per script
        comp-pipescript deployed {script} --pipeline inf-{tier} — drift check + canonical path
        comp-blast {s3_artifact} --direction both — reverse cover (consumers + producers)
        comp-trace {s3_artifact} --direction both — full dependency chain
        comp-routes trace inflection-* — Lambda routing graph
        comp-iam service inf-* — IAM permission audit (cross-validate access patterns)
        comp-platinum reverse platinum/* — platinum consumer mapping
        comp-pii audit — PII flow audit

      Use these as the FIRST pass; manual fill-in only what compilers can't reach.
    </step>
    <step>
      Per-tier inventory. For each S3 prefix on opal-data-inf, list every distinct
      file pattern and document. Andrew direct 2026-05-07: must explicitly qualify
      single-shot vs lookback semantics + full data shape:

        - canonical_name: e.g., "performance_dim", "tax_unrealized", "transactions"
        - tier: bronze / silver / gold / platinum
        - s3_path_pattern: e.g., "bronze/performance/{date}.parquet"
        - format: csv / parquet / json

        - data_semantic_class: SINGLE_SHOT / SNAPSHOT_PER_DATE / LOOKBACK_WINDOW / EVENT_LOG
            * SINGLE_SHOT: pull once = full current state. NO historical date dimension; re-pulling overwrites.
              Examples: representatives, accounts_v2 (new_portfolio), unified_account_dim — all "current" snapshots.
              Backfill semantic: NOT meaningful — there's no historical version to recover.
            * SNAPSHOT_PER_DATE: per-date snapshot of state-as-of-that-date. Each date is independent.
              Examples: tax_unrealized, billing, assets_v2, positions_daily.
              Backfill semantic: re-pulling old date returns Orion's current view of state-as-of-that-date.
            * LOOKBACK_WINDOW: pull captures a window backward from a reference date.
              Examples: performance_dim (3y window), unified_account_dim if used with --window.
              Backfill semantic: window length matters; documented per-artifact.
            * EVENT_LOG: cumulative log of events in a date range; pulling [start, end] returns all events in that range.
              Examples: transactions (--start-date / --end-date).
              Backfill semantic: a single big pull covers the whole history; per-date "stamp" is just the run date, not the data window.

        - lookback_window: explicit window length if LOOKBACK_WINDOW class
          (e.g., performance_dim = "3y from snapshot_date")

        - data_shape:
            row_grain: account / household / transaction / advisor / firm
            column_count: approximate
            key_columns: list of primary identifier columns (account_id, household_id, etc.)
            measure_columns: list of value/numeric columns (current_value, mv, nna, etc.)
            join_keys_for_downstream: columns silver/gold builders use to join

        - partition_layout: flat / hive-partitioned / snapshot_date=
        - producer: script path or Lambda function name + canonical invocation
        - consumers: list of scripts/Lambdas/portal endpoints that read it
        - schema_pointer: schema YAML file (or inline columns + types if small)
        - rep_id_filter: which scope filter applies (INFLECTION_REP_IDS, custodian, etc.)
        - refresh_cadence: daily / monthly_eom / weekly / on-demand / never (for dead artifacts)
        - status: LIVE / DEPRECATED / NOT-IN-USE / BROKEN
        - coverage_known: date range + known gaps
        - notes: special concerns

      SAMPLE FOR PERFORMANCE (illustrative — per Andrew's direct):
        canonical_name: performance_dim
        tier: bronze
        s3_path_pattern: bronze/performance/{date}.parquet
        format: parquet
        data_semantic_class: LOOKBACK_WINDOW
        lookback_window: "3y from snapshot_date (configurable via --window)"
        data_shape:
          row_grain: account
          key_columns: [account_id, snapshot_date]
          measure_columns: [twr_value, drawdown, std_dev, beg_mv, end_mv, ...]
          join_keys_for_downstream: account_id
        partition_layout: flat
        producer: data/orion/manual_api/pull_inflection_performance_dim.py
        ...

      SAMPLE FOR TRANSACTIONS:
        canonical_name: transactions
        tier: bronze
        s3_path_pattern: bronze/orion-api/{run_date}/transactions.csv
        format: csv
        data_semantic_class: EVENT_LOG
        lookback_window: "[start_date, end_date] explicit args; default rolling 7d"
        data_shape:
          row_grain: transaction
          key_columns: [trans_id]
          measure_columns: [trans_amount]
          time_columns: [trans_date]
        partition_layout: flat-by-run-date (run_date in path; data window != run_date)
        notes: "EVENT_LOG class — bronze date is run-stamp, not data window."

      SAMPLE FOR REPRESENTATIVES:
        canonical_name: representatives
        tier: bronze
        s3_path_pattern: bronze/orion-api-v2/{date}/representatives.json
        data_semantic_class: SINGLE_SHOT
        lookback_window: N/A
        data_shape:
          row_grain: representative
          key_columns: [rep_id]
        notes: "SINGLE_SHOT — current rep registry; backfill not meaningful."
    </step>
    <step>
      Cross-validate with portal route audit (INFETL.007 / df0b18942):
        - Every platinum path the portal reads must have a registry entry
        - Every gold path the portal reads (16 violations) → flagged in registry as "TO-8 migration target"
        - shared-advisor-router routing logic → registry should capture origin-routing as a special-case data flow
    </step>
    <step>
      Populate two output files:

        docs/architecture/INFETL_MASTER_DATA_REGISTRY.md — human-readable narrative + tables grouped by tier
        docs/architecture/inf_data_graph.yaml — machine-readable canonical structure consumed by compilers (comp-tools.yaml registry can reference this)

      YAML schema (rough):

        artifacts:
          - name: performance_dim
            tier: bronze
            s3_path_pattern: bronze/performance/{date}.parquet
            format: parquet
            date_semantics: per-date
            partition_layout: flat
            producer:
              script: data/orion/manual_api/pull_inflection_performance_dim.py
              args: --upload-bronze --snapshot-date {date}
            consumers:
              - data/orion/scripts/silver/convert_orion_api_to_silver.py (--dim performance)
              - data/orion/scripts/gold/INF_C_01.canonical_nna.py
              - data/orion/scripts/gold/INF_D_08.nmec_nmnc_nna.py
            schema_pointer: docs/data/schemas/performance_dim.yaml
            rep_id_filter: INFLECTION_REP_IDS={3,6,11,12} (post-INFNNA.001)
            status: LIVE
            coverage_known: 1 file (2026-05-03) only — pre-onboarding skip-400 expected for historical
            notes: Confused with bronze/orion-api/{date}/performance_dim.csv pattern (does NOT exist there).
    </step>
    <step>
      Compiler integration. Update org/modules/graph/comp-tools.yaml to reference
      inf_data_graph.yaml as source-of-truth for compiler queries on Inflection
      pipeline. Cross-link with the BD analog if BD has a similar registry (or note
      the gap as future BD harmonization).
    </step>
    <step>
      Pre-commit gate + commit + push:
        .tools/safe-commit.sh --author "0.4.0_DS_ClientPlatform~A &lt;0.4.0_DS_ClientPlatform~A@opal.agent&gt;"
        -m "doc(ADVI_INFETL.MDR): Inflection master data registry — canonical artifact graph across bronze/silver/gold/platinum"
        -- docs/architecture/INFETL_MASTER_DATA_REGISTRY.md docs/architecture/inf_data_graph.yaml [+ comp-tools.yaml if updated]
    </step>
    <step>
      RAVC to COO: registry doc paths + counts (artifacts per tier) + gaps surfaced
      during enumeration + recommendations for cleanup tasks.
    </step>
  </scope>

  <compiler_mandate>
    <tool>comp-pipescript io — every Inflection script's I/O</tool>
    <tool>comp-pipescript deployed --pipeline inf-gold + inf-silver — drift check</tool>
    <tool>comp-blast {artifact} — reverse cover for every artifact</tool>
    <tool>comp-routes trace inflection-* — Lambda routing</tool>
    <tool>comp-iam service inf-* — IAM cross-validation</tool>
    <tool>comp-platinum reverse platinum/* — portal consumer mapping</tool>
    <tool>comp-pii audit — PII flow</tool>
  </compiler_mandate>

  <acceptance_criteria>
    <criterion id="AC1">INFETL_MASTER_DATA_REGISTRY.md landed with per-tier (bronze/silver/gold/platinum) inventory tables + narrative summary.</criterion>
    <criterion id="AC2">inf_data_graph.yaml landed in machine-readable format with all artifacts populated.</criterion>
    <criterion id="AC3">Compiler tools cited inline as enumeration sources for each section (evidence-based, not human-curated).</criterion>
    <criterion id="AC4">Status field populated for every artifact (LIVE / DEPRECATED / NOT-IN-USE / BROKEN); list of NOT-IN-USE artifacts surfaced for cleanup.</criterion>
    <criterion id="AC5">Cross-reference with INFETL.007 portal-route audit — 16 gold violations + S3-direct platinum routes captured in registry.</criterion>
    <criterion id="AC6">comp-tools.yaml updated to reference inf_data_graph.yaml as source-of-truth for INF pipeline queries.</criterion>
  </acceptance_criteria>

  <gates_dependencies>
    <upstream>None. Compiler-aided enumeration runs against current state; doesn't need to wait for any TO to ship.</upstream>
    <downstream>
      INFETL.LAMBDA-DIMS uses MDR to scope per-dim Lambda I/O contracts.
      INFETL.SHAPE-VERIFY consumes MDR as canonical shape spec.
      TO-8 (gold→platinum migration) uses MDR for tranche scoping.
      All future Inflection work cross-checks against MDR before assuming paths.
    </downstream>
  </gates_dependencies>

  <go_signal>
    <issued_at>20260507T~18:45Z</issued_at>
    <issued_by>2.0.0_SA_COO</issued_by>
    <message>GO. Andrew direct priority HIGH — "very badly" needed. Lean on compilers heavily; manual enumeration only as last resort. Coordinate with AE 0.7 INFETL.DAILY-AUDIT (operational subset). ~1.5d cumulative.</message>
  </go_signal>
</task_order>
