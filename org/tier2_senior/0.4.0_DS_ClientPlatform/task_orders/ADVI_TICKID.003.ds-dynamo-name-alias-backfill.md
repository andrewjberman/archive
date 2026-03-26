<task_order>
  <metadata>
    <id>2.0.0_SA_COO-2026-03-26-tickid-003-ds</id>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_to>0.4.0_DS_ClientPlatform</issued_to>
    <date>2026-03-26</date>
    <status>complete</status>
    <project_code>ADVI_TICKID</project_code>
  </metadata>

  <objective>
    Batch-update bd-securities DynamoDB items to populate name_aliases with all
    observed BD asset names for each resolved ticker. This is the belt-and-suspenders
    layer: even without the holdings enrichment (.002), the ETFClassifier's Layer 2
    (name-based lookup) will work because the DynamoDB items now contain the BD names.
  </objective>

  <context>
    The ETFClassifier's Layer 2 does a name-based scan of bd-securities looking for
    items where asset_name_raw or name_aliases match the query name. Currently only
    ~6 of 5,203 items have name_aliases populated. After this backfill, every resolved
    ticker in the resolution table will have its BD asset names in name_aliases.

    This runs independently of .002 (script 03 modification). Can run in parallel.

    PRD: docs/architecture/ADVI_TICKID_PRD.md (section 3.6)
  </context>

  <scope>
    <files>
      <file action="create">data/black_diamond/scripts/classification/backfill_name_aliases.py</file>
    </files>
  </scope>

  <requirements>
    <requirement id="1">
      Create backfill_name_aliases.py at data/black_diamond/scripts/classification/.

      For each (asset_name, resolved_ticker) pair in ticker_resolution.parquet:
      1. Look up the bd-securities item with PK = resolved_ticker (ticker-keyed items)
      2. Read existing name_aliases (may be empty list or missing)
      3. Add the BD asset_name (raw form) AND the normalized form to name_aliases
      4. Deduplicate the list
      5. BatchWriteItem / UpdateItem to persist

      Use DynamoDB UpdateExpression with SET + list_append for atomic updates.
    </requirement>

    <requirement id="2">
      Handle edge cases:
      - Ticker-keyed item doesn't exist: skip (log warning)
      - Name-keyed item exists (NAME::{name}): do NOT update — these are stubs
      - name_aliases already contains the name: skip (idempotent)
    </requirement>

    <requirement id="3">
      Validation output:
      - Count of DynamoDB items updated
      - Count of items skipped (no ticker-keyed entry)
      - Count of aliases added (total across all items)
      - ETFClassifier name_map size before and after (scan bd-securities, count items
        with non-empty name_aliases)
    </requirement>

    <requirement id="4">
      Dry-run mode: --dry-run flag that prints what would be updated without writing.
    </requirement>

    <requirement id="5">
      Session log at:
        org/tier2_senior/0.4.0_DS_ClientPlatform/logs/{date}/
          advi_tickid_003_dynamo_backfill_session.md
    </requirement>
  </requirements>

  <acceptance_criteria>
    <criterion id="1">backfill_name_aliases.py runs without errors</criterion>
    <criterion id="2">DynamoDB items updated with name_aliases containing BD asset names</criterion>
    <criterion id="3">Idempotent — re-run produces no additional changes</criterion>
    <criterion id="4">name_map size increases significantly (target: ~5K -> ~10K+)</criterion>
  </acceptance_criteria>

  <constraints>
    <constraint>Do NOT delete or modify existing DynamoDB items beyond adding name_aliases</constraint>
    <constraint>Do NOT create new DynamoDB items — only update existing ticker-keyed entries</constraint>
    <constraint>Do NOT modify NAME::-keyed stub entries</constraint>
    <constraint>Batch operations only — no individual PutItem calls (DynamoDB cost)</constraint>
    <constraint>No emojis in code</constraint>
  </constraints>

  <dependencies>
    <dependency agent="0.4.0_DS_ClientPlatform" task="ADVI_TICKID.001" status="required">
      ticker_resolution.parquet must exist
    </dependency>
  </dependencies>

  <deliverables>
    <deliverable type="commit">backfill_name_aliases.py</deliverable>
    <deliverable type="artifact">bd-securities DynamoDB items updated with name_aliases</deliverable>
    <deliverable type="document">Session log with backfill metrics</deliverable>
  </deliverables>
</task_order>
