<task_order>
  <metadata>
    <id>1.3.0_DS_CompLearns-2026-04-22-comp-learns-043-comp-wave-runner</id>
    <issued_by>2.1.0_SA_COO</issued_by>
    <issued_to>1.3.0_DS_CompLearns</issued_to>
    <date>2026-04-22</date>
    <status>staged <!-- Gate: .042 (comp-preflight.py) COMPLETE. GO fires from COO after .042 ships. --></status>
    <project_code>COMP_LEARNS</project_code>
    <priority>P1 — wave orchestrator for Stage 2 eval-mode activation; secondary to .044 per §13 prioritization rule</priority>
  </metadata>

  <references>
    <ref type="prd">docs/architecture/COMP_LEARNS_AUTOMATION_V1.md §7 (loop function design) + §8 (scorer worktree provisioning) + §9 (comparison-domain drift) + §10 (eval-mode invariants) + §13 (TO decomposition)</ref>
    <ref type="wave1_data">comp/results/pilot-wave-1/ — dry-run target; wave-runner must reconstruct this event sequence from manifests</ref>
    <ref type="produced_by_042">comp/bin/comp-preflight.py + diagnostic JSON schema (§5) — contract this TO consumes</ref>
  </references>

  <objective>
    Implement comp/bin/comp-wave-runner.py — the mixed-mode wave orchestrator. Handles
    one full wave config (N tasks × M conditions × K agents), exits at the end. Not a
    long-running daemon.

    Explicitly in scope:

    1. CLI per §7:
       ```
       comp-wave-runner --wave-config <wave.yaml> [--dry-run]
       ```
       Non-dry: executes the wave end to end. Dry-run: validates config + dispatches
       nothing; prints the event sequence the runner would fire and the per-event mode
       routing.

    2. Wave config schema per §7 (YAML):
       ```yaml
       wave_id: str
       mode: dev | eval | mixed
       tasks:
         - task_id: str
           conditions: [a, b]
           mode: dev | eval  # optional; inherits wave-level mode if absent
       agents: [str, ...]
       scorer: str  # used in eval only; ignored in dev
       gate: human | policy | audit_sampled
       preflight_tool: str  # path to comp-preflight.py
       doctrine_version: str
       worktree_root: str
       output_dir: str
       ```

    3. Startup validation:
       - All task packets exist at comp/tasks/{task_id}/packet.yaml
       - All agents are reachable on the MCP broker (get_live_agents)
       - Eval-mode tasks: scorer agent is live (if mode has any eval event)
       - Dev-mode tasks: scorer field is ignored
       - preflight_tool path resolves + is executable

    4. Dependency order enforcement per §7:
       - condition_a events complete BEFORE condition_b for same (task × agent)
       - Within condition_a: agents run in parallel per task
       - Across tasks: all tasks parallel (no shared state)
       - Cross-mode independence: dev + eval tasks in the same wave do not gate each other

    5. Per-event loop:
       a. Dispatch GO to DS via MCP (include mode + condition + task_id + worktree + bundle output path in GO body)
       b. Wait for DS "bundle delivered" MCP (event-driven via inbox-watch, NOT polling)
       c. Run `comp-preflight --task {id} --bundle-path {path} --condition {a|b} --mode {dev|eval}`
       d. Parse preflight JSON:
          - EXIT 0 + dev mode: process result.json; log KEEP/DISCARD/TIED to experiment_log.jsonl
          - EXIT 0 + eval mode: provision fresh SC worktree (§8); copy packet + bundle (diff + test_output.txt, NOT reasoning.md); send scoring request to SC
          - EXIT 1: pause event; MCP COO with failure JSON; halt wave-level progression OR mark this (task × agent × condition) as failed depending on wave config
       e. Eval-mode only: wait for SC verdict MCP; record to comp/results/{wave_id}/verdicts/{task}-{agent}-{condition}-run-{N}.json
       f. Comparison-domain check per §9: actual_manifest_hash == expected_manifests[task][condition]; mismatch flags the verdict file with comparison_domain_flag: true

    6. Scorer worktree provisioning (eval only, §8):
       ```
       WORKTREE=worktrees/comp-learns/{task_id}/scorer-run-{N}
       git worktree add $WORKTREE {baseline_commit}
       cp {bundle}/refactor.patch $WORKTREE/input/
       cp {bundle}/test_output.txt $WORKTREE/input/
       cp comp/tasks/{task}/packet.yaml $WORKTREE/input/
       # reasoning.md NOT copied — mechanically enforced; reject if already present
       cd $WORKTREE && git status --short  # must be empty
       ```
       Cleanup post-verdict: `git worktree remove $WORKTREE --force`. Log path to
       comp/results/{wave_id}/worktree_audit.log.

    7. Comparison-domain drift per §9:
       - At wave startup: compute expected_manifest_hash for every eval-mode (task × condition) cell
       - Persist to comp/results/{wave_id}/expected_manifests.json
       - After each eval verdict: verify actual matches expected; flag but do not halt

    8. Wave finalization:
       - Eval events done: trigger SC integrity audit request (MCP to scorer with audit request)
       - Dev events done: emit dev summary = (KEEPs count, DISCARDs count, champion state, plateau count)
       - Write comp/results/{wave_id}/run_summary.json with per-event status + comparison-domain flags

    9. Unit tests at comp/tests/test_wave_runner.py covering:
       - Wave config validation (missing task packet → startup fail; invalid mode → fail)
       - Dev-mode-only wave (no scorer involvement; no worktree provisioning)
       - Eval-mode-only wave with a stub SC (verdict mock)
       - Mixed-mode wave: dev + eval events coexist; per-task mode overrides respected
       - Preflight EXIT 1 halts the offending event and MCPs COO
       - Dependency order: condition_a before condition_b; cross-task parallel
       - Comparison-domain flag fires on manifest mismatch (synthetic test)
       - --dry-run prints event sequence and exits 0 without dispatching

    10. Dry-run verification against wave 1 data:
        - Construct a wave-1.yaml config that describes the pilot wave 1 events
          (2 tasks × 2 conditions × agents from pilot-wave-1/)
        - `comp-wave-runner --wave-config wave-1.yaml --dry-run` must print the actual
          event sequence that ran in pilot-wave-1 (reconstructed from the existing
          verdicts/ + bundles/ + integrity_audit.md)
        - This is the "verified against wave 1 data" gate from §7 + §11

    Explicitly out of scope:
    - Implementing comp-preflight.py (that is .042).
    - Implementing comp-dev-loop.py (that is .044; wave-runner may REFERENCE it via
      subprocess or leave dev-mode execution to a separate runner — align on the simpler
      design: wave-runner processes result.json directly in dev mode, does NOT subshell
      into comp-dev-loop.py).
    - Authoring the actual wave-2.yaml config for Wave 2 (COO writes that during .045
      activation review).
    - Running SC — wave-runner requests; SC executes; wave-runner records the return.
    - Multi-scorer pool (deferred to v2 per §14).

    Prioritization note: If resourcing is tight, .044 (dev loop) ships BEFORE this TO.
    Do not start .043 until .042 is COMPLETE; confirm .044 status with COO before starting.
  </objective>

  <compiler_tools_mandate>
    <phase id="1" when="before write">
      <step>
        <run>comp-build && pytest comp/ -q</run>
        <expect>Clean baseline including .042's comp-preflight tests green.</expect>
        <if_mismatch>Rebase or fix. Do not proceed on a red baseline.</if_mismatch>
      </step>
      <step>
        <run>python comp/bin/comp-preflight.py --help</run>
        <expect>CLI help prints; confirms .042 shipped and API is the expected contract.</expect>
        <if_mismatch>STOP. MCP COO — .042 not yet shipped. This TO is gated on it.</if_mismatch>
      </step>
      <step>
        <run>ls comp/results/pilot-wave-1/</run>
        <expect>pilot-wave-1/ exists with verdicts/, bundles/, integrity_audit.md — needed for dry-run gate.</expect>
        <if_mismatch>Investigate; pilot wave 1 data is a hard ref.</if_mismatch>
      </step>
    </phase>
    <phase id="2" when="before commit">
      <step>
        <run>python -m py_compile comp/bin/comp-wave-runner.py</run>
        <expect>Exit 0.</expect>
        <if_mismatch>Fix syntax.</if_mismatch>
      </step>
      <step>
        <run>.tools/ds-commit-gate.sh comp/bin/comp-wave-runner.py comp/tests/test_wave_runner.py</run>
        <expect>Exit 0.</expect>
        <if_mismatch>Fix each flagged issue.</if_mismatch>
      </step>
      <step>
        <run>pytest comp/tests/test_wave_runner.py -v</run>
        <expect>All tests PASS — all enumerated cases including dry-run, mixed-mode, preflight-fail halt.</expect>
        <if_mismatch>Debug + fix. Do not commit partial.</if_mismatch>
      </step>
      <step>
        <run>pytest comp/ -q</run>
        <expect>Full suite GREEN.</expect>
        <if_mismatch>Fix.</if_mismatch>
      </step>
      <step>
        <run>python comp/bin/comp-wave-runner.py --wave-config comp/tests/fixtures/wave-1-replay.yaml --dry-run</run>
        <expect>Prints event sequence that matches pilot-wave-1 order (2 tasks × 2 conditions × agents). Exit 0.</expect>
        <if_mismatch>Adjust config or runner logic until dry-run reconstructs wave 1 accurately. This is the §11 gate.</if_mismatch>
      </step>
    </phase>
    <phase id="3" when="after commit">
      <step>
        <run>comp-build</run>
        <expect>Clean.</expect>
        <if_mismatch>Surface to COO.</if_mismatch>
      </step>
      <step>
        <run>pytest comp/tests/test_wave_runner.py comp/tests/test_preflight.py -v</run>
        <expect>Both GREEN. Confirms .042 + .043 integrated cleanly.</expect>
        <if_mismatch>Fix.</if_mismatch>
      </step>
    </phase>
  </compiler_tools_mandate>

  <cross_domain_coordination>
    <note>.042 (comp-preflight, 1.4.0_DS) is a hard prerequisite — this TO calls comp-preflight.py via subprocess and parses its JSON output. Any CLI contract change from .042 breaks this TO. .044 (comp-dev-loop, 1.1.0_DS) is parallel — they share the result.json + experiment_log.jsonl schemas. Do NOT write the wave runner to subshell into comp-dev-loop; instead, wave-runner processes result.json directly in dev mode (simpler; fewer moving parts). If you need to coordinate schema changes with .044, MCP 1.1.0_DS directly (same wave 2 DS pod).</note>
    <shared_artifacts>comp/bin/comp-preflight.py (read via subprocess); result.json schema (AUTOMATION_V1 §4, shared with .044); experiment_log.jsonl schema (§12, shared with .044); comp/tests/fixtures/preflight/ (read only, for reusable test data)</shared_artifacts>
  </cross_domain_coordination>

  <acceptance_criteria>
    1. comp/bin/comp-wave-runner.py implements §7 wave config schema + §7 loop behavior + §8 worktree provisioning + §9 manifest drift check + §10 invariant preservation.
    2. --dry-run mode prints event sequence + mode routing without dispatching; exits 0 on valid config.
    3. comp/tests/test_wave_runner.py covers all enumerated test cases; all PASS.
    4. Dry-run against wave-1-replay.yaml reconstructs the pilot wave 1 event sequence accurately (this is the §11 gate).
    5. reasoning.md mechanically excluded from scorer worktree provisioning (tested).
    6. Comparison-domain flag logic tested (synthetic manifest mismatch).
    7. pytest comp/ -q GREEN end-to-end.
    8. Commit under --author=1.3.0_DS_CompLearns@opal.agent with --only pathspec scoped to comp/bin/comp-wave-runner.py + comp/tests/test_wave_runner.py + comp/tests/fixtures/... (if added).
    9. Pushed to CLOUD.
    10. Session log with Compiler Tools section documenting every mandate run.
    11. MCP COMPLETE to 2.1.0_SA_COO with commit sha.
  </acceptance_criteria>

  <dependencies>
    - Gate: .042 (comp-preflight.py) COMPLETE and merged to CLOUD.
    - Parallel: .044 (comp-dev-loop.py) — no direct dependency, shared schemas only.
    - Blocks: .045 (Stage 2 eval-mode activation review dry-runs this runner).
  </dependencies>

  <operational_notes>
    - Operate from /c/Users/AndrewBerman/Desktop/feature_clb. Confirm pwd.
    - Event-driven waiting: use the MCP broker's inbox notification path (not polling).
      Reference: .tools/inbox-watch behavior — wave-runner internally spawns or subscribes.
      If the broker doesn't expose a Python API for subscription, fall back to reading
      inbox filesystem path at org/mcp/inbox/{agent_serial}/ with brief sleeps — this is
      acceptable for v1 so long as it's documented.
    - Mechanical reasoning.md exclusion: when provisioning scorer worktree, NEVER copy
      reasoning.md even if present in bundle. Test this.
    - Wave-level manifest reference: expected_manifests.json is append-only; if a run
      encounters a new (task × condition) cell not in expected, log as new anchor, do
      NOT fail the wave.
    - Dry-run must be fully offline — no MCP dispatches, no git worktree commands — just
      config validation + event sequence print.
    - No emojis anywhere.
  </operational_notes>

  <closeout>
    On completion:
    - commit with --only --author="1.3.0_DS_CompLearns &lt;1.3.0_DS_CompLearns@opal.agent&gt;" -- comp/bin/comp-wave-runner.py comp/tests/test_wave_runner.py [fixtures]
    - push to CLOUD
    - flip TO status to complete
    - MCP COMPLETE to 2.1.0_SA_COO with sha
    - session log with Compiler Tools section
  </closeout>
</task_order>
