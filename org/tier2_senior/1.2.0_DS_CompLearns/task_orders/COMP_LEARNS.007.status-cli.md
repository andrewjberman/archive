<task_order>
  <metadata>
    <id>1.2.0_DS_CompLearns-2026-04-15-comp-learns-007-status-cli</id>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_to>1.2.0_DS_CompLearns</issued_to>
    <date>2026-04-15</date>
    <status>staged</status><!-- Parallel with #003; flips pending when ~B closes #003. -->
    <project_code>COMP_LEARNS</project_code>
    <priority>P1 — MANDATE req #8 observability</priority>
  </metadata>

  <references>
    <ref type="mandate">docs/architecture/COMP_LEARNS_OPERATIONAL_MANDATE.md (Requirement 8: "comp-learns status httpx")</ref>
    <ref type="engine">comp/bin/comp-learns-run.sh — writes state.json + tsv to `worktrees/comp-learns-{target}/comp/targets/{target}/`</ref>
    <ref type="framework">comp/framework/run.py — state.json schema authoritative</ref>
    <ref type="walkthrough">comp/AUTORESEARCH_WALKTHROUGH.md §F Req #8 — `comp-learns status` + state.json cache</ref>
  </references>

  <objective>
    Ship `comp-learns status {target}` CLI + install shim. Sub-10s response per mandate req #8.

    Reads (in priority order):
    1. `worktrees/comp-learns-{target}/comp/targets/{target}/state.json` — cache of current iter metrics
    2. `worktrees/comp-learns-{target}/comp/targets/{target}/results.tsv` — authoritative history (via results_schema)
    3. `worktrees/comp-learns-{target}/comp/targets/{target}/.driver.lock` — driver PID presence
    4. `worktrees/comp-learns-{target}/comp/targets/{target}/.halt` — paused flag
    5. `worktrees/comp-learns-{target}/comp/targets/{target}/SUMMARY.md` — terminal state if present

    Outputs:
    - `state`: active | paused | terminated
    - `iter`: current iteration number (from tsv row count, authoritative)
    - `seconds_since_last_commit`: derived from state.json.last_update_unix vs now
    - `last_3_statuses`: last 3 tsv rows' status field (keep/discard/crash)
    - `plateau_warning`: detect_plateau() result on last 5 keep rows
    - `branch`: resolved from git -C {worktree} rev-parse --abbrev-ref HEAD
    - `driver_pid`: read from state.json

    Human-readable default + `--json` flag for machine-readable.
  </objective>

  <scope>
    <files>
      <file action="create">comp/framework/status.py (the CLI implementation)</file>
      <file action="create">comp/bin/comp-learns-status (install shim)</file>
      <file action="create">comp/framework/tests/test_status.py</file>
    </files>
  </scope>

  <wire_contract>
    CLI: `comp-learns-status {target} [--json]`
    Default human output (≤15 lines):
    ```
    target: httpx
    state: active
    iter: 27
    seconds_since_last_commit: 42
    last_3_statuses: keep, keep, discard
    plateau_warning: false
    branch: comp-learns/httpx
    driver_pid: 408320
    ```
    `--json` output: same fields + types as a JSON object for piping.

    Exit codes: 0 (found + readable), 2 (target dir absent), 3 (state malformed).
  </wire_contract>

  <acceptance_criteria>
    1. `comp-learns-status _stub` produces valid output against the stub target state artifacts.
    2. Sub-10s response (wall-clock `time` shows <10s).
    3. `--json` flag produces parseable JSON (pytest validates schema).
    4. `active` / `paused` / `terminated` state derivation per rules: driver PID alive → active; .halt file present → paused; SUMMARY.md present + PID dead → terminated.
    5. Tests ≥6 cases; pytest green.
    6. Install shim at `comp/bin/comp-learns-status` (tracked); user copies to `.tools/` per ~C's pattern.
    7. Session log Compiler Tools section per CTO Rule 7.
    8. MCP COMPLETE to COO with commit hash + sample output on stub.
  </acceptance_criteria>

  <compiler_tools_mandate>
    <phase id="1" when="before write">
      <step>
        <run>cat comp/framework/run.py | grep -A 15 "write_state_cache"</run>
        <expect>state.json schema visible; fields: target, iter, commit, query_pass_rate, coverage_pct, mean_latency_ms, lines_of_code, status, plateau_warning, description, timestamp.</expect>
        <if_mismatch>~C's run.py schema drifted; reconcile before writing status.py.</if_mismatch>
      </step>
      <step>
        <run>cat comp/framework/results_schema.py | grep -A 5 COLUMNS</run>
        <expect>~A's columns tuple authoritative for tsv parsing.</expect>
        <if_mismatch>Reconcile.</if_mismatch>
      </step>
    </phase>

    <phase id="2" when="before commit">
      <step>
        <run>python -m pytest comp/framework/tests/test_status.py -v</run>
        <expect>All tests pass.</expect>
        <if_mismatch>Fix until green.</if_mismatch>
      </step>
      <step>
        <run>time comp-learns-status _stub</run>
        <expect>Exit 0; &lt;10s wall-clock (real &lt; 10.000s in time output).</expect>
        <if_mismatch>Optimize.</if_mismatch>
      </step>
    </phase>

    <phase id="3" when="after commit">
      <step>
        <run>comp-learns-status _stub --json | python -c "import json,sys; json.load(sys.stdin); print('ok')"</run>
        <expect>"ok" — JSON parses cleanly.</expect>
        <if_mismatch>Fix schema.</if_mismatch>
      </step>
    </phase>
  </compiler_tools_mandate>

  <dependencies>
    <dependency agent="1.1.0_DS_CompLearns" task="COMP_LEARNS.001" status="complete"/>
    <dependency agent="1.3.0_DS_CompLearns" task="COMP_LEARNS.004" status="complete" description="state.json + run.py schema authoritative"/>
  </dependencies>

  <next>On commit: operator can answer "what is target X doing?" in sub-10s per mandate req #8 — closes the last observability requirement.</next>
</task_order>
