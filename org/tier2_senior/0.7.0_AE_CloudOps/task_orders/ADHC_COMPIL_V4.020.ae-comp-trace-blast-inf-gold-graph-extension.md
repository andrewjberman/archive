<?xml version="1.0" encoding="UTF-8"?>
<task_order>
  <metadata>
    <id>ADHC_COMPIL_V4.020</id>
    <project>ADHC_COMPIL_V4</project>
    <title>comp-trace/blast cross-layer graph extension — inject INF gold script nodes + promote D_04 hardcoded platinum-write strings to s3:platinum/* graph nodes</title>
    <issued_to>0.7.0_AE_CloudOps</issued_to>
    <issued_by>1.0.0_SA_CTO</issued_by>
    <issued_date>2026-05-08</issued_date>
    <status>complete</status><!-- Closed 2026-05-08T~PM by AE 0.7.0. Architectural seam identified: extract_s3.py gold-extraction loop was BD-only (data/black_diamond/scripts/gold/) + comp-pipescript inject was a separate step that got wiped on every comp-build rebuild. Fix: (a) duplicated the gold-extraction loop in extract_s3.py for INF gold dir (data/orion/scripts/gold/INF_*.py) — script-level + function-level nodes + CALLS edges + builder/function S3 writes; (b) added _inject_full_pipeline_into_graph() helper in trace_graph.build_graph that calls inject_pipeline_edges for both BD and INF gold DAGs in-process with optional _graph param (avoids cache-write race). Empirical: 1250→1772 nodes (+42%); 1047→1344 edges (+28%); 36 INF gold scripts + 428 INF function nodes registered; 22 s3:platinum/* nodes (BD D_04 platinum writes). All 4 OPS Cat 2 cases flip FAIL→PASS. BD regression-clean (multi-match output unchanged; build_employee_leaderboard blast enriched 7→13 from platinum injection). Tier reclassification: comp-trace + comp-blast moved A in comp-tools-segment-scope.md + comp-tools.yaml. RAVC1 latitude not exercised (additive code, no extractor refactor). -->
    <priority>high</priority>
    <estimated_effort>~1-1.5d (graph-extractor refactor risk; RAVC1 if scope expands)</estimated_effort>
  </metadata>

  <references>
    <ref type="prd">docs/architecture/ADHC_COMPIL_V4.md (V4 family)</ref>
    <ref type="ops_briefing">AE 0.7 OPS triage briefing 20260508T~PM Cat 2 (Cross-layer graph coverage gaps; Tier reclassification finding)</ref>
    <ref type="ops_matrix">docs/architecture/ADHC_COMPIL_V4_017_TEST_MATRIX.md</ref>
    <ref type="prior_to">ADHC_COMPIL_V4.008 added inf-manual-api/* to comp-pipescript pipeline_dag but did NOT inject INF gold nodes into comp-trace/blast cross-layer graph</ref>
  </references>

  <context>
    Architectural finding from OPS empirical run: comp-trace/blast cross-layer graph (`.comp-graph/graph.json`) contains BD gold + Lambda + Component + Endpoint + EventBridge + S3 nodes — but NOT INF gold scripts as first-class nodes. Empirical: `grep '"id":\s*"gold:INF_'` against `.comp-graph/graph.json` returns 0 matches. So `comp-trace INF_D_04 --direction both` returns "No nodes matching"; `comp-blast _build_aua_view` returns "No nodes matching"; `comp-blast inf-gold-trigger` returns "No downstream consumers" (Lambda in graph but downstream INF gold consumers empty).

    Compounded second issue: `comp-trace platinum/firm/leaderboard.json` returns "No nodes matching" — `s3:platinum/*` nodes don't exist in graph at all. D_04 writes platinum keys via `[HARDCODED]` strings but the writes aren't promoted to S3_ARTIFACT graph nodes.

    This empirically reclassified `comp-trace` + `comp-blast` from Tier A (cross-segment) to Tier B (segment-aware) per V4.017 segment-scope finding. The architectural goal: bring them back to Tier A by extending the graph extractor.
  </context>

  <scope>
    <step>
      <run>Read `org/modules/graph/extract_pipeline.py` + `extract_*` family — locate where BD gold nodes get injected into the cross-layer graph (vs the per-pipeline DAG used by comp-pipescript). The two graph populations are distinct; identify the injection seam for cross-layer.</run>
      <expect>Clear understanding of (a) which extractor populates `.comp-graph/graph.json` cross-layer graph vs (b) which extractors populate comp-pipescript per-pipeline DAGs. Determine if extension is additive or requires refactor.</expect>
      <if_mismatch>If the cross-layer extractor is structurally separate from per-pipeline + a refactor is required: RAVC1 to CTO with scope finding; CTO may split this TO or expand budget.</if_mismatch>
    </step>
    <step>
      <run>**Part 1 (INF gold node injection):** extend cross-layer graph extractor to register INF gold scripts (`data/orion/scripts/gold/INF_*.py`) as `gold:INF_*` nodes alongside BD `gold:*` nodes. Reuse the AST extraction pattern from V4.008.</run>
      <expect>Post-extension: `grep '"id":\s*"gold:INF_"' .comp-graph/graph.json` returns ≥30 matches (current 36 INF gold scripts per V4.008 + manual_api ship).</expect>
    </step>
    <step>
      <run>**Part 2 (s3:platinum/* node promotion):** D_04 writes platinum keys via hardcoded strings; extend extractor to detect these `[HARDCODED]` write patterns and promote them to `s3:platinum/*` graph nodes with proper write edges from D_04.</run>
      <expect>Post-extension: `comp-trace platinum/firm/leaderboard.json` returns nodes (D_04 as writer + downstream consumers).</expect>
    </step>
    <step>
      <run>Empirical regression: re-run V4.017 OPS test matrix Cat 2 cases (2.1 + 2.2 + 2.3 + 2.4). All should now PASS instead of "No nodes matching".</run>
      <expect>4/4 OPS Cat 2 cases flip FAIL → PASS.</expect>
    </step>
    <step>
      <run>Update segment-scope reference card + comp-tools.yaml: `comp-trace` + `comp-blast` move back to Tier A (cross-segment). Update test-matrix doc to reflect post-fix Tier classification.</run>
      <expect>Documentation reflects empirical post-fix scope.</expect>
    </step>
    <step>
      <run>Ship via safe-commit.sh; RAVC2 to CTO + COO with full evidence + Tier reclassification doc updates.</run>
      <expect>Clean ship.</expect>
    </step>
  </scope>

  <acceptance_criteria>
    <ac id="1">`gold:INF_*` nodes injected into cross-layer graph; ≥30 INF gold script nodes exist post-build.</ac>
    <ac id="2">`s3:platinum/*` nodes injected via D_04 hardcoded-string detection; ≥1 platinum key has writer+consumer edges.</ac>
    <ac id="3">OPS Cat 2 cases (2.1/2.2/2.3/2.4) all flip FAIL → PASS empirically.</ac>
    <ac id="4">comp-trace + comp-blast move back to Tier A per segment-scope reference card + comp-tools.yaml metadata.</ac>
    <ac id="5">BD case regression-clean: `comp-trace D_04` + `comp-blast bd-gold-trigger` produce same output as pre-ship.</ac>
    <ac id="6">comp-pipescript per-pipeline DAG behavior unchanged (this TO targets cross-layer graph; comp-pipescript already covers per-pipeline correctly).</ac>
  </acceptance_criteria>

  <compiler_tools_mandate>
    <phase id="1">Read extract_pipeline.py + cross-layer extractor; identify injection seam.</phase>
    <phase id="2">Pre-commit: 6-cell test matrix (4 OPS Cat 2 + 2 BD regression).</phase>
    <phase id="3">Post-commit: rerun V4.017 OPS Cat 2 test cases; append to compiler-tools-log.md.</phase>
  </compiler_tools_mandate>

  <ravc>
    <expected_recipient>1.0.0_SA_CTO + 2.0.0_SA_COO (joint)</expected_recipient>
    <expected_evidence>Pre/post grep of `.comp-graph/graph.json` + 4 Cat 2 test case re-runs + 2 BD regression cases + Tier reclassification doc updates</expected_evidence>
  </ravc>

  <out_of_scope>
    <item>Inflection silver/bronze gold extension (separate scope; manual_api already shipped V4.008).</item>
    <item>Lambda/EventBridge cross-layer edges (V4.005 comp-events scope).</item>
    <item>Generic platinum-write detection beyond D_04 hardcoded strings (D_04 is the dominant case; generalize if other scripts surface).</item>
  </out_of_scope>
</task_order>
