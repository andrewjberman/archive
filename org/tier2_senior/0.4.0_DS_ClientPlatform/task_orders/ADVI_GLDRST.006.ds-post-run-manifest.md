<task_order>
  <metadata>
    <id>2.0.0_SA_COO-2026-03-26-gldrst-006-ds</id>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_to>0.4.0_DS_ClientPlatform</issued_to>
    <date>2026-03-26</date>
    <status>staged</status>
    <project_code>ADVI_GLDRST</project_code>
  </metadata>

  <objective>
    Enhance pipeline-complete.json from a simple sentinel into a full
    post-run manifest that documents what was produced, enabling
    downstream consumers to validate data freshness and completeness.
  </objective>

  <context>
    Current pipeline-complete.json:
    {"status": "success", "mode": "incremental|full", "timestamp": "...", "run_date": "..."}

    This tells publishers "a run happened" but not what it produced.
    Publishers blindly read parquets without knowing if they're fresh.
  </context>

  <requirements>
    <requirement id="1">
      Extend run_gold_layer.sh to collect per-script outputs and write
      an enhanced manifest:

      {
        "status": "success",
        "mode": "incremental|full",
        "run_date": "YYYY-MM-DD",
        "started_at": "ISO8601Z",
        "completed_at": "ISO8601Z",
        "duration_seconds": int,
        "scripts_executed": [
          {"script": "02_build_positions_cube.py", "status": "ok", "duration_s": int,
           "outputs": ["gold/positions_cube/2026-03-26.parquet"]},
          ...
        ],
        "key_metrics": {
          "total_aua": float,
          "num_relationships": int,
          "num_accounts": int,
          "num_advisors": int,
          "data_as_of": "YYYY-MM-DD"
        },
        "exclusions_applied": {
          "ghost_accounts": int,
          "ap_gate_excluded": int
        }
      }

      Write to gold/meta/pipeline-manifest.json (new key).
      Continue writing gold/pipeline-complete.json (old key) for backward
      compatibility with publisher Lambda triggers.
    </requirement>

    <requirement id="2">
      Each gold script should write a summary line to stdout in a
      parseable format that run_gold_layer.sh can capture:
        MANIFEST: {"script": "05b", "rows": 1234567, "duration_s": 300}

      run_gold_layer.sh collects these lines and embeds them in the manifest.
    </requirement>
  </requirements>

  <acceptance_criteria>
    <criterion id="1">pipeline-manifest.json written after each gold run with per-script output inventory</criterion>
    <criterion id="2">Backward compatible: pipeline-complete.json still written (publisher trigger)</criterion>
  </acceptance_criteria>

  <constraints>
    <constraint>pipeline-complete.json must continue to be written at the same S3 key for Lambda triggers</constraint>
    <constraint>Manifest is informational — publishers do NOT gate on it (yet)</constraint>
  </constraints>

  <deliverables>
    <deliverable type="commit">run_gold_layer.sh manifest collection + write</deliverable>
    <deliverable type="commit">Per-script MANIFEST: stdout lines</deliverable>
  </deliverables>
</task_order>
