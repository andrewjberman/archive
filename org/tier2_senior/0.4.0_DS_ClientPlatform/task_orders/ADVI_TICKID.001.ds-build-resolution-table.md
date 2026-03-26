<task_order>
  <metadata>
    <id>2.0.0_SA_COO-2026-03-26-tickid-001-ds</id>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_to>0.4.0_DS_ClientPlatform</issued_to>
    <date>2026-03-26</date>
    <status>complete</status>
    <project_code>ADVI_TICKID</project_code>
  </metadata>

  <objective>
    Build resolve_tickers.py — a ticker resolution script that maps BD asset names
    to canonical ticker symbols. Generate gold/dimensions/ticker_resolution.parquet
    with coverage metrics. This is the foundation for all subsequent TICKID phases.
  </objective>

  <context>
    ~80% of holdings_lots rows have ticker=None. The ETFClassifier's Layer 1 (ticker
    lookup in bd-securities DynamoDB) fails immediately for these. The resolution table
    solves this by mapping BD asset_name strings to canonical tickers BEFORE the
    classifier runs.

    Partial fix already deployed: commit 0c0fdb28 added asset_name_raw indexing to
    ETFClassifier, enabling Layer 2 name-based lookups. But Layer 2 has low coverage
    because most bd-securities items lack name_aliases. The resolution table provides
    structural coverage via ticker enrichment at the holdings_lots build step.

    PRD: docs/architecture/ADVI_TICKID_PRD.md (read sections 3.3, 3.4 fully)
  </context>

  <scope>
    <files>
      <file action="create">data/black_diamond/scripts/classification/resolve_tickers.py</file>
    </files>
  </scope>

  <requirements>
    <requirement id="1">
      Create resolve_tickers.py at data/black_diamond/scripts/classification/.

      Inputs:
      - Latest holdings_lots parquet from S3 (unique asset_name values where ticker is None)
      - bd-securities DynamoDB table (full scan, cached locally — use existing boto3 patterns)
      - etf_classification.py ASSET_NAME_TO_TICKER dict (import directly)

      Output:
      - gold/dimensions/ticker_resolution.parquet written to S3

      Schema (per PRD section 3.3):
      - asset_name_normalized (str, PK for join)
      - asset_name_raw (str)
      - resolved_ticker (str)
      - resolution_method (str)
      - confidence (float, 0.0-1.0)
      - last_updated (str, ISO8601)
    </requirement>

    <requirement id="2">
      Implement resolution methods in priority order (PRD section 3.3):

      1. bd_feed (confidence 1.0): ticker already in holdings_lots for this asset_name
      2. bd_securities_exact (confidence 1.0): exact match on asset_name_raw in DynamoDB
      3. bd_securities_prefix (confidence 0.95): BD truncated name is prefix of asset_name_raw
         (handle BD's ~30-char truncation)
      4. etf_classification_alias (confidence 0.95): match in ASSET_NAME_TO_TICKER dict
      5. individual_stock_pattern (confidence 0.85): "{COMPANY} INC COM" / "{COMPANY} CORP COM"
      6. mutual_fund_pattern (confidence 0.80): "{FUND NAME} {SHARE CLASS}" pattern

      Do NOT implement yahoo_search in this task order — that is a future enhancement.
      Do NOT use keyword heuristics or regex classifiers — use the structured resolution
      methods above.
    </requirement>

    <requirement id="3">
      Normalization function: lowercase, strip whitespace, collapse multiple spaces.
      Same normalization must be applied at resolve time AND at join time (script 03).
      Export normalize_asset_name() as a reusable function.
    </requirement>

    <requirement id="4">
      Script must be idempotent — safe to re-run. On re-run, regenerates the full
      resolution table (not incremental). Previous S3 artifact is overwritten.
    </requirement>

    <requirement id="5">
      Validation output (print to stdout):
      - Total unique asset names with ticker=None
      - Count and % resolved per method
      - Total resolution coverage (count and % of MV)
      - Top 20 unresolved by market value (for manual review queue)
      - Count of holdings_lots rows that would gain a ticker
    </requirement>

    <requirement id="6">
      Write a session log at:
        org/tier2_senior/0.4.0_DS_ClientPlatform/logs/{date}/
          advi_tickid_001_resolution_table_session.md

      Include: resolution coverage metrics, method breakdown, top unresolved names,
      commit hash, next steps for .002 (script 03 join).
    </requirement>
  </requirements>

  <acceptance_criteria>
    <criterion id="1">resolve_tickers.py exists and runs without errors</criterion>
    <criterion id="2">ticker_resolution.parquet written with correct schema</criterion>
    <criterion id="3">Resolution coverage > 80% of tickerless asset names</criterion>
    <criterion id="4">Top 20 unresolved list printed for manual review</criterion>
    <criterion id="5">Session log documents coverage metrics and commit hash</criterion>
  </acceptance_criteria>

  <constraints>
    <constraint>Do NOT modify script 03 — that is .002</constraint>
    <constraint>Do NOT modify detect_new_securities.py — that is .004</constraint>
    <constraint>Do NOT implement Yahoo Finance search — future enhancement</constraint>
    <constraint>Do NOT modify DynamoDB — that is .003</constraint>
    <constraint>Use current S3 key layout (not GLDRST migrated paths — .004 hasn't landed yet)</constraint>
    <constraint>No emojis in code</constraint>
  </constraints>

  <dependencies>
    <dependency agent="0.4.0_DS_ClientPlatform" task="ADVI_GLDRST.001" status="complete">
      lib/exclusions.py patterns may inform which asset_names to skip
    </dependency>
  </dependencies>

  <deliverables>
    <deliverable type="commit">resolve_tickers.py with resolution methods 1-6</deliverable>
    <deliverable type="artifact">gold/dimensions/ticker_resolution.parquet on S3</deliverable>
    <deliverable type="document">Session log with coverage metrics</deliverable>
  </deliverables>
</task_order>
