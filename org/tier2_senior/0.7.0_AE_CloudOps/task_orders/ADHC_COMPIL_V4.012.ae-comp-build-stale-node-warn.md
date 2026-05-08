<?xml version="1.0" encoding="UTF-8"?>
<task_order>
  <metadata>
    <id>ADHC_COMPIL_V4.012</id>
    <project>ADHC_COMPIL_V4</project>
    <title>comp-build STALE_NODE_WARN — emit warning when graph-node source SHA != current-file SHA</title>
    <issued_to>0.7.0_AE_CloudOps</issued_to>
    <issued_by>1.0.0_SA_CTO</issued_by>
    <issued_date>2026-05-08</issued_date>
    <status>pending</status><!-- Authored by CTO direct per Andrew 2026-05-08 PM "full 5-item, run it" post-retrospective. PRD v0.3 addendum §13.4 TO-12. HIGH priority — biting now via INF_D_07 stale-entry case. -->
    <priority>normal</priority>
    <estimated_effort>~0.5d</estimated_effort>
  </metadata>

  <references>
    <ref type="prd">docs/architecture/ADHC_COMPIL_V4.md §13.4 TO-12 (v0.3 addendum 2026-05-08 PM)</ref>
    <ref type="retrospective">docs/architecture/ADHC_COMPIL_FULL_CORPUS_RETROSPECTIVE.md §6.4 + §7 Item B</ref>
    <ref type="anchor_incident">INF_D_07 (DS~A 2026-05-05 ADVI_INFLEC_AUDIT002_execution_closeout): "comp-pipescript io INF_D_07 -- READS: silver/accounts_dim/latest.parquet (hardcoded) -- stale graph entry; runtime uses gold/dimensions/accounts_dimension_latest.parquet"</ref>
    <ref type="second_anchor">mdlp_rvvalt_closure_catchup 2026-05-05 (DE 0.4): "AC6/AC5 comp-transform (graph build doesn't index new files before comp-build refresh)"</ref>
  </references>

  <context>
    comp-build extracts source-of-truth from filesystem at index time; comp-* tools then query the cached graph. If filesystem changes after comp-build (script edited, comp-build not re-run), tools answer from stale graph silently. INF_D_07 case: graph indexed `silver/accounts_dim/latest.parquet` but runtime had been updated to `gold/dimensions/accounts_dimension_latest.parquet`; agent had to discover via direct file read. Same class of issue across mdlp_rvvalt + others.

    Fix: emit `STALE_NODE_WARN` when current-file SHA diverges from indexed SHA; doesn't block tool output (preserves discovery utility) but signals to agent that comp-build re-run is recommended.
  </context>

  <scope>
    <step>
      <run>Read `org/modules/graph/extract_pipeline.py` + comp-build source. Locate node-metadata structure; confirm whether per-node source SHA is currently captured.</run>
      <expect>If captured: skip to step 3. If not: extend extraction to compute + store source-file SHA per node.</expect>
    </step>
    <step>
      <run>Add SHA to `.comp-graph/graph.json` per-node metadata (or equivalent index format).</run>
      <expect>SHA stored; backwards-compatible with existing graph consumers (graph readers ignore unknown fields).</expect>
    </step>
    <step>
      <run>Add SHA-check at query time: any comp-* tool that reads the graph cache calls a shared `check_node_freshness()` helper that walks node SHAs vs current filesystem; emits `STALE_NODE_WARN: <node> source SHA drift detected -- rerun comp-build` to stderr (not stdout — doesn't pollute structured output).</run>
      <expect>Existing tool stdout output unchanged; stderr-side WARN visible to agents.</expect>
    </step>
    <step>
      <run>Add CI lint mode: `comp-build --check` exits non-zero if any node SHA diverges from current filesystem.</run>
      <expect>Useful for CI gate; documented in tool help.</expect>
    </step>
    <step>
      <run>Empirical test — before TO ship, edit one indexed gold script (e.g., add a comment to D_04). Run `comp-pipescript io D_04` — expect STALE_NODE_WARN to fire. Run comp-build. Re-run comp-pipescript io D_04 — expect no WARN.</run>
      <expect>WARN fires + clears as expected; existing tool functionality unchanged.</expect>
    </step>
    <step>
      <run>Ship via safe-commit.sh; RAVC2 to CTO + COO with empirical test evidence + INF_D_07 case retro-validation.</run>
      <expect>Clean ship.</expect>
    </step>
  </scope>

  <acceptance_criteria>
    <ac id="1">comp-build records source-file SHA per indexed node in `.comp-graph/graph.json`.</ac>
    <ac id="2">Any comp-* tool emits `STALE_NODE_WARN: <node>` to stderr when current-file SHA diverges from indexed SHA. stdout unchanged.</ac>
    <ac id="3">`comp-build --check` exits non-zero (exit 2) if any node has SHA drift; exits 0 if all clean.</ac>
    <ac id="4">Empirical test: edit one indexed gold script + comp-pipescript io triggers WARN; comp-build re-run clears it.</ac>
    <ac id="5">No false positives on first build (empty .comp-graph cache → all nodes fresh).</ac>
    <ac id="6">No regression — existing tools (comp-pipescript, comp-blast, comp-trace, etc.) produce same stdout output as pre-ship.</ac>
  </acceptance_criteria>

  <compiler_tools_mandate>
    <phase id="1">Read extract_pipeline.py + graph.json structure; confirm SHA storage approach.</phase>
    <phase id="2">Pre-commit: synthetic edit + WARN-fire + comp-build-clear test cycle.</phase>
    <phase id="3">Post-commit empirical: rerun INF_D_07 case (edit script, query, observe WARN) + 1 baseline regression query (comp-pipescript io D_04 with clean cache, no WARN).</phase>
  </compiler_tools_mandate>

  <ravc>
    <expected_recipient>1.0.0_SA_CTO + 2.0.0_SA_COO (joint)</expected_recipient>
    <expected_evidence>Empirical test fire + clear cycle + 1 regression query</expected_evidence>
  </ravc>

  <out_of_scope>
    <item>Auto-rebuild on detected drift (manual rerun preserved; agent-decision point).</item>
    <item>Multi-file SHA aggregation for nodes that span multiple sources (single-file SHA per node).</item>
    <item>Partial-rebuild optimization (full comp-build still required when WARN fires).</item>
  </out_of_scope>
</task_order>
