<task_order>
  <metadata>
    <id>2.0.0_SA_COO-2026-03-26-tickid-002-ds</id>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_to>0.4.0_DS_ClientPlatform</issued_to>
    <date>2026-03-26</date>
    <status>complete</status>
    <project_code>ADVI_TICKID</project_code>
  </metadata>

  <objective>
    Modify script 03 (build_holdings_lots.py) to join with ticker_resolution.parquet,
    enriching holdings_lots with resolved tickers. After this change, downstream scripts
    (05, 05b, 06, 06b, 12) receive holdings with tickers populated for >95% of positions.
  </objective>

  <context>
    Phase 1 (.001) produced gold/dimensions/ticker_resolution.parquet with mappings from
    BD asset names to canonical tickers. This task order wires that table into the gold
    layer pipeline by joining it at the holdings_lots build step.

    The join is a simple left merge on normalized asset_name. COALESCE(raw_ticker,
    resolved_ticker) ensures BD-provided tickers take precedence.

    No downstream script changes needed — they already consume holdings_lots.ticker.

    PRD: docs/architecture/ADVI_TICKID_PRD.md (section 3.5)
  </context>

  <scope>
    <files>
      <file action="modify">data/black_diamond/scripts/gold/03_build_holdings_lots.py</file>
    </files>
  </scope>

  <requirements>
    <requirement id="1">
      After FIFO reconstruction builds the lots DataFrame, add the resolution join:

      1. Read ticker_resolution.parquet from S3 (gold/dimensions/)
      2. Normalize lots['asset_name'] using the same normalize_asset_name() from
         resolve_tickers.py (import it or duplicate the 3-line function)
      3. Left merge on asset_name_normalized
      4. COALESCE: lots['ticker'] = lots['ticker'].fillna(lots['resolved_ticker'])
      5. Drop the join columns (asset_name_normalized, resolved_ticker)

      The join adds <1s overhead (~5K resolution rows).
    </requirement>

    <requirement id="2">
      Graceful fallback: if ticker_resolution.parquet does not exist on S3,
      print a warning and continue without enrichment. Do NOT fail the gold run.
    </requirement>

    <requirement id="3">
      Validation output (print to stdout):
      - Count of lots rows before enrichment with ticker != None
      - Count after enrichment with ticker != None
      - Delta (new tickers added)
      - % coverage after enrichment
    </requirement>

    <requirement id="4">
      Write a session log at:
        org/tier2_senior/0.4.0_DS_ClientPlatform/logs/{date}/
          advi_tickid_002_holdings_enrichment_session.md

      Include: before/after ticker coverage, commit hash, note that gold rerun
      needed to populate enriched holdings (subsumed by GLDRST .009 if committed first).
    </requirement>
  </requirements>

  <acceptance_criteria>
    <criterion id="1">Script 03 joins with ticker_resolution.parquet</criterion>
    <criterion id="2">COALESCE preserves BD-provided tickers (no overwrites)</criterion>
    <criterion id="3">Graceful fallback when resolution table doesn't exist</criterion>
    <criterion id="4">Ticker coverage after enrichment > 95%</criterion>
  </acceptance_criteria>

  <constraints>
    <constraint>Do NOT modify any downstream scripts (05, 05b, 06, 06b, 12)</constraint>
    <constraint>Do NOT write to S3 — code-only change, AE runs gold layer</constraint>
    <constraint>MUST commit before GLDRST .009 gold rerun — .009 will generate enriched holdings</constraint>
    <constraint>No emojis in code</constraint>
  </constraints>

  <dependencies>
    <dependency agent="0.4.0_DS_ClientPlatform" task="ADVI_TICKID.001" status="required">
      ticker_resolution.parquet must exist on S3
    </dependency>
  </dependencies>

  <deliverables>
    <deliverable type="commit">Script 03 modification with resolution table join</deliverable>
    <deliverable type="document">Session log with coverage metrics</deliverable>
  </deliverables>
</task_order>
