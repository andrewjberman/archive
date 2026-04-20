<task_order>
  <metadata>
    <id>1.0.0_SA_CTO-2026-04-15-comp-learns-002-httpx-target</id>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_to>1.0.0_SA_CTO</issued_to><!-- CTO-execution TO per CTO direction 18:57Z: query verifiability requires CTO-level judgment; authoring is hands-on 4-6 hrs. First CTO-execution TO in this project. -->
    <date>2026-04-15</date>
    <status>staged</status><!-- Gate: PRD #1 HARNESS_FRAMEWORK ships first (needed: harness_base.py signature, query_schema.py validator). -->
    <project_code>COMP_LEARNS</project_code>
    <priority>P1 — proves loop end-to-end; blocks Phase 2 iteration</priority>
  </metadata>

  <references>
    <ref type="prd">docs/architecture/COMP_LEARNS_HTTPX_TARGET.md (PRD #2 of 5)</ref>
    <ref type="doctrine">docs/architecture/COMP_LEARNS_QUALITATIVE_FRAMEWORK.md (benchmark epistemics — 5 query dimensions + 7-step construction protocol)</ref>
    <ref type="depends">org/tier2_senior/0.4.0_DS_ClientPlatform/task_orders/COMP_LEARNS.001.ds-a-harness-framework.md (framework must ship first)</ref>
    <ref type="target_repo">github.com/encode/httpx (Python HTTP client, ~10K LOC, unfamiliar-but-tractable first target per PRD §Real modules)</ref>
  </references>

  <objective>
    Ship `comp/targets/httpx/` containing:
    - `harness.py` — ~10-line wrapper calling `comp.framework.harness_base.run_harness`
    - `queries.yaml` — **~50 ground-truth queries, hand-authored by CTO** per qualitative framework's 7-step construction protocol + 5 query dimensions
    - `answers.py` — opaque scoring hooks for queries where default comparator is insufficient
    - `_repo/` — vendored httpx clone pinned to a specific commit (`repo_pin.txt`)

    NO `compiler.py` in this TO — that's Phase 2 agent emission, not this PRD.

    Query-authoring is the load-bearing work: each query's `ground_truth_method` must cite a specific file:line in `_repo/` that can be independently re-verified.

    Time estimate per CTO: 4-6 hrs hands-on. Schedule post-ADVI_ROLLUP-rerun-validator close (~18:00 ET) so no split-attention.
  </objective>

  <scope>
    <files>
      <file action="create">comp/targets/httpx/harness.py</file>
      <file action="create">comp/targets/httpx/queries.yaml</file>
      <file action="create">comp/targets/httpx/answers.py</file>
      <file action="create">comp/targets/httpx/repo_pin.txt</file>
      <file action="vendored">comp/targets/httpx/_repo/ (via git clone + git checkout &lt;PIN_SHA&gt;)</file>
    </files>
  </scope>

  <acceptance_criteria>
    1. `_repo/` clone pinned at a recent stable httpx commit; SHA recorded in `repo_pin.txt`.
    2. `queries.yaml` contains ≥50 queries; each has `id, question, answer_kind, answer, ground_truth_method, tags`; no duplicate ids; validator from PRD #1 passes.
    3. Query tag distribution reflects the 5 dimensions from QUALITATIVE_FRAMEWORK — mix of `simple_fact`, `single_hop`, `cross_surface`, `compound_hard` (not concentrated in any single tag).
    4. Every `ground_truth_method` cites `file:line` in `_repo/` that can be manually re-verified.
    5. `harness.py` runs against a stub compiler.py (can live in CTO's working dir, not committed) and produces a valid HarnessResult.
    6. `answers.py` covers all queries whose `answer_kind` needs custom comparison (e.g., regex match, set-intersection).
    7. Session log's Compiler Tools section reproduces each `<run>` + observed-result + pass/fail vs. `<expect>` (CTO Rule 7).
    8. MCP COMPLETE to COO with commit hash + query count + tag-distribution table.
  </acceptance_criteria>

  <compiler_tools_mandate>
    <phase id="1" when="before write">
      <step>
        <run>git clone https://github.com/encode/httpx.git comp/targets/httpx/_repo &amp;&amp; cd comp/targets/httpx/_repo &amp;&amp; git log -1 --format='%H %s'</run>
        <expect>Clone succeeds; pinned commit SHA captured for repo_pin.txt.</expect>
        <if_mismatch>Retry network; if persistent, surface to COO.</if_mismatch>
      </step>
      <step>
        <run>python -c "from comp.framework.query_schema import Query, validate_queries_file; validate_queries_file('comp/targets/httpx/queries.yaml')"</run>
        <expect>After authoring, validator passes with no errors.</expect>
        <if_mismatch>Fix schema violations before commit.</if_mismatch>
      </step>
    </phase>

    <phase id="2" when="before commit">
      <step>
        <run>python -c "from comp.framework import run_harness; result = run_harness(Path('comp/targets/httpx/stub_compiler.py'), Path('comp/targets/httpx/queries.yaml'), None); print(result.query_pass_rate, result.coverage_pct)"</run>
        <expect>HarnessResult returned; pass_rate + coverage numeric; stub compiler fails most queries as expected (~0%).</expect>
        <if_mismatch>Framework contract broken; coordinate with ~A (PRD #1 owner) before commit.</if_mismatch>
      </step>
      <step>
        <run>awk -F: '{print $1}' comp/targets/httpx/queries.yaml | grep ground_truth_method | wc -l</run>
        <expect>≥50 (matches query count).</expect>
        <if_mismatch>Missing ground_truth_method on some queries — fix.</if_mismatch>
      </step>
    </phase>

    <phase id="3" when="after commit">
      <step>
        <run>Spot-check: pick 5 random queries, manually verify ground_truth_method file:line cites a real, correct answer.</run>
        <expect>5/5 spot-checks verify.</expect>
        <if_mismatch>Fix flagged queries; re-commit. Accuracy of ground_truth is load-bearing.</if_mismatch>
      </step>
    </phase>
  </compiler_tools_mandate>

  <dependencies>
    <dependency agent="0.4.0_DS_ClientPlatform~A" task="COMP_LEARNS.001" status="staged" description="framework ships first"/>
  </dependencies>

  <next>On commit: PRD #3 COMPILER_BASELINE scaffold gets templated against this target; Phase 2 iteration loop can fire once engine is built (Track B).</next>
</task_order>
