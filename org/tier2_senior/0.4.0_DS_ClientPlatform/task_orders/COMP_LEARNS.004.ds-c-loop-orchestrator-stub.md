<task_order>
  <metadata>
    <id>0.4.0_DS_ClientPlatform~C-2026-04-15-comp-learns-004-loop-orchestrator</id>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_to>0.4.0_DS_ClientPlatform~C</issued_to>
    <date>2026-04-15</date>
    <status>complete</status><!-- Shipped 2026-04-15 19:55Z. Commits: 4d17f47d (pre-flight plateau + 11 tests), 1380d44c (status flip), e657c232 (full scope: run.py rewrite + branch_guard.py + comp/bin/comp-learns-run shim, 22/22 pytest). Acceptance #5 flex ACK'd by CTO 19:52Z (shim source at comp/bin/, local .tools/ install per comp-* convention; .gitignore:170 forbids tracked .tools/ files). P0 branch-race constraint honored: Python side read-only against git. End-to-end httpx iteration deferred to post-PRD#2 ship. -->
    <evidence>
      Shipped: commits 4d17f47d (pre-flight plateau detector + 11 test cases), 1380d44c (staged→pending flip on CTO GO), e657c232 (full scope ship — run.py rewrite + branch_guard.py + comp/bin/comp-learns-run shim), 8df2ba97 (session log addendum — Track B worktree migration 23de5edf), 3ae7c3dd (DS~C session log).
      Artifacts: comp/loop/run.py, comp/loop/branch_guard.py, comp/loop/plateau.py, comp/loop/tests/ (22 test cases), comp/bin/comp-learns-run.sh.
      Validation: pytest comp/loop/ = 22/22 PASS. Acceptance #5 flex ACK'd by CTO 2026-04-15 19:52Z (shim source at comp/bin/, local .tools/ install per comp-* convention; .gitignore:170 forbids tracked .tools/ files). P0 branch-race constraint honored — Python side read-only against git.
      Deferred: end-to-end httpx iteration deferred to post-PRD#2 ship (now handled by .017 under v3 PRD).
      Session log: org/tier2_senior/0.4.0_DS_ClientPlatform/logs/2026-04-15/.
    </evidence>
    <project_code>COMP_LEARNS</project_code>
    <priority>P2 — partially subsumed by Track B engine; stubs-only until engine lands</priority>
  </metadata>

  <references>
    <ref type="prd">docs/architecture/COMP_LEARNS_LOOP_ORCHESTRATOR.md (PRD #4 of 5)</ref>
    <ref type="mandate">docs/architecture/COMP_LEARNS_OPERATIONAL_MANDATE.md (8 reqs — COO engine owns continuous-execution, state-persistence, crash-recovery, kill-switch, observability)</ref>
    <ref type="walkthrough">comp/AUTORESEARCH_WALKTHROUGH.md (COO's pre-implementation study — describes engine shape + state contract)</ref>
    <ref type="depends_framework">org/tier2_senior/0.4.0_DS_ClientPlatform/task_orders/COMP_LEARNS.001.ds-a-harness-framework.md</ref>
    <ref type="depends_engine">Track B engine ship (COO-owned, bash driver pattern per Andrew 19:01Z: "bash script that the agent can only turn off if it hits its goal")</ref>
  </references>

  <objective>
    **Stub TO — scope held narrow until COO Track B engine (bash driver) lands.**

    The bash driver subsumes PRD #4's "continuous execution" + "state persistence" + "crash recovery" surface. What remains for DS ~C after Track B ships:

    1. `comp/framework/run.py` — Python-level single-iteration entry point invoked by bash driver per iteration. Parses target arg + optional description; invokes compiler via harness; appends tsv row; writes status cache.
    2. `comp/framework/plateau.py` — pure function `detect_plateau(rows, window=5, tolerance_pct=1.0) -> bool` over tsv rows. Called by bash driver at top of each iteration.
    3. `comp/framework/branch_guard.py` — optional; asserts current git branch matches `comp-learns/{target}` or warns.
    4. `.tools/comp-learns-run` — thin shell shim calling `python -m comp.framework.run`.

    NOT in scope (owned by COO Track B engine):
    - The bash `while true` loop itself
    - Terminal-state checking (pass-rate threshold, iter cap, kill switch, wall-clock budget)
    - Kill-switch surfaces (`.halt` file, SIGTERM handler)
    - `comp-learns status {target}` observability CLI (MANDATE req #8)
    - SUMMARY.md emission at terminal state

    This TO ships the single-iteration Python side; the bash driver invokes it per iteration.
  </objective>

  <scope>
    <files>
      <file action="create">comp/framework/run.py</file>
      <file action="create">comp/framework/plateau.py</file>
      <file action="create">comp/framework/branch_guard.py</file>
      <file action="create">.tools/comp-learns-run</file>
      <file action="create">comp/framework/tests/test_plateau.py</file>
    </files>
  </scope>

  <wire_contract>
    CLI: `python -m comp.framework.run <target> [--description "..."] [--compiler-path PATH]`
    - Reads git HEAD; runs harness; appends tsv row with status `keep|discard|crash`; writes `comp/targets/{target}/state.json` cache
    - Exits 0 on successful iteration (regardless of keep/discard); exit 1 on infrastructure failure; exit 2 on crash handled as iteration failure per MANDATE req #3

    `detect_plateau(rows, window=5, tolerance_pct=1.0) -> bool` — pure function; called by bash driver per iteration.
  </wire_contract>

  <acceptance_criteria>
    1. `python -m comp.framework.run httpx --description "test"` (post-target-ship) produces a new tsv row + state.json.
    2. `detect_plateau` handles: empty tsv (False), single row (False), 5 rows within tolerance (True), 5 rows outside (False), 5 rows including one crash (count crash as non-plateau-ing).
    3. Plateau test suite ≥6 cases; pytest green.
    4. `branch_guard.py` asserts current branch matches `comp-learns/{target}` when invoked with `--strict`; warns otherwise.
    5. `.tools/comp-learns-run` PATH-available; forwards args to `python -m comp.framework.run`.
    6. Session log's Compiler Tools section reproduces each `<run>` + observed-result + pass/fail vs. `<expect>` (CTO Rule 7).
    7. MCP COMPLETE to COO with commit hash + state.json sample + plateau test output.
  </acceptance_criteria>

  <compiler_tools_mandate>
    <phase id="1" when="before write">
      <step>
        <run>test -f comp/framework/harness_base.py &amp;&amp; test -f /c/Users/AndrewBerman/Desktop/ajb_workspace/comp/bin/comp-learns-run.sh 2>&amp;1</run>
        <expect>PRD #1 shipped AND Track B bash driver shipped (second gate). If either absent, TO stays staged.</expect>
        <if_mismatch>HARD STOP — both dependencies must land first. Coordinate with ~A (PRD #1) + COO (Track B engine).</if_mismatch>
      </step>
      <step>
        <run>cat comp/AUTORESEARCH_WALKTHROUGH.md | grep -A 3 "§F.*state persistence"</run>
        <expect>Walkthrough describes state contract; Python `run.py` must honor the same contract (git log + results.tsv as source of truth; state.json is cache only).</expect>
        <if_mismatch>Re-read walkthrough before authoring.</if_mismatch>
      </step>
    </phase>

    <phase id="2" when="before commit">
      <step>
        <run>python -m pytest comp/framework/tests/test_plateau.py -v</run>
        <expect>All tests pass.</expect>
        <if_mismatch>Fix until green.</if_mismatch>
      </step>
      <step>
        <run>python -m comp.framework.run --help</run>
        <expect>Usage printed; args documented.</expect>
        <if_mismatch>argparse wiring broken.</if_mismatch>
      </step>
    </phase>

    <phase id="3" when="after commit">
      <step>
        <run>.tools/comp-learns-run --help</run>
        <expect>Shim forwards correctly.</expect>
        <if_mismatch>Shim broken; fix.</if_mismatch>
      </step>
    </phase>
  </compiler_tools_mandate>

  <dependencies>
    <dependency agent="0.4.0_DS_ClientPlatform~A" task="COMP_LEARNS.001" status="staged" description="framework signature needed"/>
    <dependency agent="2.0.0_SA_COO" task="Track B engine bash driver + CTO walkthrough ACK" status="pending" description="bash driver subsumes much of PRD #4 scope; ~C's work is the Python single-iteration half"/>
  </dependencies>

  <cross_domain_coordination>
    <shared_resource>INTERFACE contract between `comp/framework/run.py` (~C) and `comp/bin/comp-learns-run.sh` (COO Track B engine). Exit code + stdout JSON format must stay locked post-v1.</shared_resource>
    <owner_of_last_write>~C owns the Python signature; COO's bash driver consumes whatever ~C ships without demanding changes post-ship.</owner_of_last_write>
    <required_mcp>Before ~C commits any signature change post-v1, MCP COO to confirm bash driver still parses cleanly. Added per CTO audit 2026-04-15T19:15Z.</required_mcp>
  </cross_domain_coordination>

  <next>On commit: engine end-to-end (bash driver + Python iter runner + harness + compiler baseline) testable. Phase 2 real iteration on httpx can fire.</next>
</task_order>
