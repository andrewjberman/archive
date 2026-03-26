<task_order>
  <metadata>
    <id>2.0.0_SA_COO-2026-03-26-tickid-004-ds</id>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_to>0.4.0_DS_ClientPlatform</issued_to>
    <date>2026-03-26</date>
    <status>complete</status>
    <project_code>ADVI_TICKID</project_code>
  </metadata>

  <objective>
    Extend detect_new_securities.py to flag holdings where ticker=None AND no
    resolution exists in ticker_resolution.parquet. Add auto-attempt prefix matching
    against bd-securities for truncated names. Report unresolved count for pipeline
    manifest visibility.
  </objective>

  <context>
    detect_new_securities.py currently creates DynamoDB stubs (NAME::{name}) for
    tickerless holdings. After TICKID .001-.003, most tickerless holdings will be
    resolved. This enhancement makes detect_new_securities aware of the resolution
    table so it only flags truly new/unresolved securities.

    This also feeds into GLDRST .006 (pipeline manifest) — the unresolved count
    should appear in pipeline-manifest.json for operational monitoring.

    PRD: docs/architecture/ADVI_TICKID_PRD.md (section 4, Phase 4)
  </context>

  <scope>
    <files>
      <file action="modify">data/black_diamond/scripts/gold/detect_new_securities.py</file>
    </files>
  </scope>

  <requirements>
    <requirement id="1">
      After existing detection logic, add a resolution-aware check:
      1. Load ticker_resolution.parquet from S3
      2. For each holding where ticker=None:
         - If asset_name_normalized exists in resolution table: SKIP (already resolved)
         - If not: attempt prefix match against bd-securities asset_name_raw
         - If prefix match found: auto-add to resolution table output (confidence 0.95)
         - If no match: flag as UNRESOLVED
    </requirement>

    <requirement id="2">
      Print summary:
      - Total tickerless holdings
      - Already resolved (in resolution table)
      - Newly resolved (prefix match)
      - Truly unresolved (flagged for manual review)
      - Top 10 unresolved by market value
    </requirement>

    <requirement id="3">
      Graceful fallback: if ticker_resolution.parquet doesn't exist, fall back to
      current behavior (no resolution-aware filtering).
    </requirement>

    <requirement id="4">
      Session log at:
        org/tier2_senior/0.4.0_DS_ClientPlatform/logs/{date}/
          advi_tickid_004_detect_enhancement_session.md
    </requirement>
  </requirements>

  <acceptance_criteria>
    <criterion id="1">detect_new_securities.py filters out already-resolved names</criterion>
    <criterion id="2">Auto-prefix matching catches truncated BD names</criterion>
    <criterion id="3">Unresolved count printed for manifest integration</criterion>
    <criterion id="4">Graceful fallback when resolution table absent</criterion>
  </acceptance_criteria>

  <constraints>
    <constraint>Do NOT break existing DynamoDB stub creation for truly new securities</constraint>
    <constraint>Do NOT modify script 03 or any other gold script — .002 handles that</constraint>
    <constraint>No emojis in code</constraint>
  </constraints>

  <dependencies>
    <dependency agent="0.4.0_DS_ClientPlatform" task="ADVI_TICKID.001" status="required">
      ticker_resolution.parquet must exist
    </dependency>
  </dependencies>

  <deliverables>
    <deliverable type="commit">detect_new_securities.py enhancement</deliverable>
    <deliverable type="document">Session log with detection metrics</deliverable>
  </deliverables>
</task_order>
