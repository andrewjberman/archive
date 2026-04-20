<task_order>
  <metadata>
    <id>0.4.0_DS_CompLearns-2026-04-15-comp-learns-005-adversarial-queries</id>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_to>0.4.0_DS_CompLearns</issued_to>
    <date>2026-04-15</date>
    <status>deferred</status><!-- DEFERRED 2026-04-20 by 2.0.0_SA_COO~Z per CTO~Z directive. Evidence: PRD v3 `docs/architecture/COMP_LEARNS_ARCHITECTURE.md @ 8df31d86` §2 row 6 (loop/propose) re-scopes Phase 4 Goodhart-defense adversarial-query work to v0.3+. Mutation-based adversarial validation (§6.6, new TO .021) supersedes this as the v0 honesty mechanism — mutation invariance replaces adversary-generated query scaffolding for the first ratchet cycle. Re-activate only when mutation stability plateau is hit AND v0 exit criterion (§8) is cleared. Prior GO (2026-04-15 Andrew) was issued under the v1/v2 PRD that placed adversarial-query generation in Phase 4 of the pilot; v3 architectural expansion supersedes. Fork resolution: CTO~Z redline 2026-04-20T17:31Z ACK 20260420T173234Z. -->
    <project_code>COMP_LEARNS</project_code>
    <priority>P2 — Phase 4 Goodhart defense; prep work parallelizable with Phase 2 iteration</priority>
  </metadata>

  <references>
    <ref type="prd">docs/architecture/COMP_LEARNS_ADVERSARIAL_QUERIES.md (PRD #5 of 5)</ref>
    <ref type="doctrine">docs/architecture/COMP_LEARNS_QUALITATIVE_FRAMEWORK.md (6 Goodhart failure modes — adversary's target)</ref>
    <ref type="org_precedent">CTO/COO validation split — "nobody validates their own work" pattern (Rule 7 pre-flag, ADHC_ROUTER corpus-to-patch)</ref>
  </references>

  <objective>
    Phase 4 Goodhart defense. Ship the adversarial-query generation scaffolding. Primary agent iterates
    `compiler.py`; a DIFFERENT agent (adversary) generates harder queries targeting apparent gaps. Humans
    spot-check 20% of adversary-generated queries before they enter the eval set.

    **Not activated automatically.** Triggered by human decision when one of:
    - Plateau warning from PRD #4 fires 3 iterations in a row, OR
    - `query_pass_rate ≥ 85%` on current eval set, OR
    - Human judges the current compiler is exploiting simple patterns.

    Scope: scaffold only. Does NOT author adversarial queries for httpx (that's Phase 4 execution, separate future TO).
  </objective>

  <scope>
    <files>
      <file action="create">comp/framework/adversary.py</file>
      <file action="create">comp/framework/compound_query_schema.py</file>
      <file action="create">comp/framework/spot_check.py</file>
      <file action="create">comp/framework/tests/test_adversary.py</file>
      <file action="modify">comp/framework/query_schema.py (extend Query with optional `source: hand|adversary_generated|compound_hard` field)</file>
    </files>
  </scope>

  <wire_contract>
    - `adversary.py` — orchestration scaffolding: given a target + a current `results.tsv` snapshot + the
      current `queries.yaml`, produces candidate adversarial queries (via prompt to an adversary agent).
    - `compound_query_schema.py` — extends Query to cover multi-hop + cross-surface + counterfactual
      ("if I change X, what breaks"). Same yaml file, new tag values: `cross_surface_multi_hop`,
      `counterfactual`, `compound_generated`.
    - `spot_check.py` — CLI helper that samples 20% of adversary-generated queries, presents to human
      for accept/reject, writes decisions back into `queries.yaml` under `compound_generated:` section +
      logs to `adversary_log.tsv`.

    Per-target directories grow:
    - `comp/targets/{name}/queries.yaml` — extended schema (same file)
    - `comp/targets/{name}/adversary_log.tsv` — new file; columns: iteration, queries_proposed, queries_accepted, queries_rejected, rejection_reasons
  </wire_contract>

  <acceptance_criteria>
    1. `adversary.py` exposes `generate_adversarial_queries(target, results_tsv_path, current_queries_path, max_n) -> list[QueryCandidate]`. Initial implementation can stub the agent invocation with a deterministic test harness; real agent wiring is Phase 4 execution.
    2. `compound_query_schema.py` validates extended query tags + source field; back-compatible with PRD #1 schema (hand-authored queries don't need source field).
    3. `spot_check.py --target httpx --candidates /tmp/adv.yaml` produces a prompt-loop that accepts y/n/skip per query; writes decisions + appends adversary_log.tsv row.
    4. Tests ≥8 cases; pytest green.
    5. Schema back-compat: httpx's `queries.yaml` from PRD #2 still validates after schema extension.
    6. Activation criteria documented at top of `adversary.py` docstring: 3 triggers (plateau ×3, pass_rate ≥85%, human judgment).
    7. Session log's Compiler Tools section reproduces each `<run>` + observed-result + pass/fail vs. `<expect>` (CTO Rule 7).
    8. MCP COMPLETE to COO with commit hash + test output + sample adversary_log.tsv row.
  </acceptance_criteria>

  <compiler_tools_mandate>
    <phase id="1" when="before write">
      <step>
        <run>cat docs/architecture/COMP_LEARNS_QUALITATIVE_FRAMEWORK.md | grep -A 2 "Goodhart"</run>
        <expect>Confirms 6 Goodhart failure modes the adversary targets. Design must address at least the pattern-memorization mode explicitly.</expect>
        <if_mismatch>Re-read qualitative framework.</if_mismatch>
      </step>
      <step>
        <run>test -f comp/framework/query_schema.py</run>
        <expect>PRD #1 schema shipped; extension builds on top.</expect>
        <if_mismatch>Gate on PRD #1 completion.</if_mismatch>
      </step>
    </phase>

    <phase id="2" when="before commit">
      <step>
        <run>python -m pytest comp/framework/tests/test_adversary.py -v</run>
        <expect>All tests pass.</expect>
        <if_mismatch>Fix.</if_mismatch>
      </step>
      <step>
        <run>python -c "from comp.framework.compound_query_schema import validate_queries_file; validate_queries_file('comp/targets/httpx/queries.yaml')"</run>
        <expect>httpx queries.yaml still validates after schema extension (back-compat).</expect>
        <if_mismatch>Schema extension broke back-compat; fix.</if_mismatch>
      </step>
    </phase>

    <phase id="3" when="after commit">
      <step>
        <run>python -m comp.framework.spot_check --help</run>
        <expect>Usage printed.</expect>
        <if_mismatch>argparse broken.</if_mismatch>
      </step>
    </phase>
  </compiler_tools_mandate>

  <dependencies>
    <dependency agent="0.1.0_DS_CompLearns" task="COMP_LEARNS.001" status="staged" description="query_schema.py extended"/>
    <dependency agent="1.0.0_SA_CTO" task="COMP_LEARNS.002" status="staged" description="httpx queries.yaml needed for back-compat test"/>
  </dependencies>

  <next>On commit: Phase 4 activation becomes a human flip (when one of 3 triggers fires on httpx). A separate Phase 4 execution TO authors adversarial queries for httpx + runs spot-check flow.</next>
</task_order>
