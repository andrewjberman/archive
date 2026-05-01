<task_order>
  <metadata>
    <id>ADHC_ORNDSP.001.ae-orion-dispatch-skip-existing</id>
    <issued_by>1.0.0_SA_CTO</issued_by>
    <issued_to>0.7.0_AE_CloudOps</issued_to>
    <date>2026-04-30</date>
    <status>complete</status><!-- 0.7.0_AE_CloudOps 2026-05-01: --skip-existing flag shipped commit 46ee0ca51. S3 marker at gold/artifacts/{SCRIPT_ID}/{RUN_DATE}. bash -n PASS, smoke AC1-AC5 verified. S3 MATCH e50b303ad0f4c0a4e5c2e3f5b187611f. -->
    <project_code>ADHC_ORNDSP</project_code>
    <theme>operational ergonomics</theme>
    <effort>0.5 weeks</effort>
    <priority>standing-low</priority>
    <gates_on>none</gates_on>
    <optional>true</optional>
  </metadata>

  <context>
    During the 2026-04-29 W4.14 B-chain SSM dispatch, the operator passed
    `--skip-existing` to orion-gold-dispatch.sh. This flag does not exist.
    The dispatch exited 1 immediately. Root cause: no idempotent re-run or
    backfill-guard flag exists in the dispatch tool.

    CTO flagged this as a useful ergonomic gap to close (2026-04-30 RULING
    message). Currently `--run-date` was added for date override; this TO
    adds a complementary skip-if-artifact-exists guard so backfill and
    idempotent re-runs are safe to dispatch.
  </context>

  <objective>
    Add `--skip-existing` flag to orion-gold-dispatch.sh. When set, each
    script in the chain checks whether its expected S3 artifact already
    exists before running. If the artifact exists and is dated >= RUN_DATE,
    the script is skipped with an INFO line. If missing or stale, it runs
    normally.

    This prevents re-computing and re-uploading outputs that already settled,
    making backfill + idempotent re-runs safe to dispatch.
  </objective>

  <scope>
    - Add `--skip-existing` boolean flag (default: off; current behavior unchanged)
    - Per-script artifact check: each CATALOG entry needs an artifact key pattern
      OR the flag works by checking S3 for a dated partition under
      `s3://opal-data-inf/gold/artifacts/` keyed by script ID + RUN_DATE
    - SKIP line format: `SKIP: {id} -- artifact exists for {RUN_DATE}`
    - Non-zero exit from artifact check must not affect chain exit code
    - Works with --bg, --from, --chain partial, --single
    - Help text updated; BG re-invoke forwards the flag
    - Syntax-clean (bash -n) before commit
  </scope>

  <acceptance_criteria>
    1. `--skip-existing` with a pre-existing artifact for RUN_DATE: script
       is skipped, INFO/SKIP line printed, chain continues to next script.
    2. `--skip-existing` with no artifact: script runs normally.
    3. Without `--skip-existing`: behavior is identical to today (no artifact check).
    4. `--bg --skip-existing` works (flag forwarded in BG re-invoke args).
    5. bash -n passes; smoke test passes.
  </acceptance_criteria>

  <do_not>
    <rule>Do NOT add artifact key patterns to the CATALOG hereditoc without
    confirming the S3 path pattern with DS first — paths may have changed.</rule>
    <rule>Do NOT change exit codes of any existing modes.</rule>
    <rule>Do NOT start before resolving the owned-paths lane classification
    for orion-gold-dispatch.sh (ADHC_ORNDSP.001 will have the same lane
    violation as the --run-date commit if the file stays in POD4 lane).</rule>
  </do_not>

  <deliverables>
    <deliverable type="code">data/orion/scripts/gold/orion-gold-dispatch.sh with --skip-existing</deliverable>
    <deliverable type="s3">Upload to s3://opal-data-inf/code/gold/orion-gold-dispatch.sh</deliverable>
    <deliverable type="ravc">RAVC to CTO with: AC1-AC5 smoke test outputs</deliverable>
  </deliverables>

  <notes>
    - Companion to ADHC_ORNDSP: --run-date flag shipped 2026-04-30 (same session,
      pending commit unblock via COO lane-violation ruling)
    - Lane classification of orion-gold-dispatch.sh must be resolved before
      either flag commit lands (AE agent blocked by POD4 owned-paths gate)
  </notes>
</task_order>
