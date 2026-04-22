<task_order>
  <metadata>
    <id>1.1.0_DS_CompLearns-2026-04-22-comp-learns-044-comp-dev-loop</id>
    <issued_by>2.1.0_SA_COO</issued_by>
    <issued_to>1.1.0_DS_CompLearns</issued_to>
    <date>2026-04-22</date>
    <status>staged <!-- Gate: .042 (comp-preflight.py) COMPLETE. GO fires from COO after .042 ships. Ships BEFORE .043 per §13 prioritization rule. --></status>
    <project_code>COMP_LEARNS</project_code>
    <priority>P0 — Wave 2 throughput driver; per §13 priority rule, ships BEFORE .043 if resourcing tight</priority>
  </metadata>

  <references>
    <ref type="prd">docs/architecture/COMP_LEARNS_AUTOMATION_V1.md §12 (inner loop design) + §4 (micro-cycle contract) + §13 (TO decomposition + priority rule)</ref>
    <ref type="prd">docs/architecture/COMP_LEARNS_BACKLOG_V1.md §4 (dev schema) + §7 (dev seed cases, incl. dev-4 success condition)</ref>
    <ref type="produced_by_042">comp/bin/comp-preflight.py --mode dev (per-iteration validation call)</ref>
    <ref type="existing_runner">comp/bin/ — locate the `comp-learns-ratchet` runner shipped in .023; dev-loop wraps it</ref>
  </references>

  <objective>
    Implement comp/bin/comp-dev-loop.py — the inner loop for automated compiler
    development. Primary Wave 2 throughput driver. Ships BEFORE .043 per the §13
    prioritization rule: the inner loop generates real iteration data; the wave
    orchestrator is justified by that data.

    Explicitly in scope:

    1. CLI per §12:
       ```
       comp/bin/comp-dev-loop.py \
         --target {target} \
         --budget-hours {N} \
         --judge real \
         [--plateau-n {N}] \
         [--burst-n {N}] \
         [--validation-level unit|integration|full]
       ```
       Default burst-n: 3. Default plateau-n: 5. Default validation-level: unit (per iteration).

    2. Validation ladder per §12:
       - LEVEL 1 (per-iteration, ~5-30s): py_compile compiler.py + targets/{target}/compiler.py;
         targeted unit tests `pytest comp/tests/ -q -k "{target}"`. Required before logging
         ANY verdict. Level 1 FAIL → treat as DISCARD (mutation broken).
       - LEVEL 2 (KEEP candidate checkpoint, ~60-120s): full `pytest comp/ -q`. Runs before
         writing KEEP to champion.json. Level 2 FAIL on KEEP candidate → treat as DISCARD.
         TIED passing Level 2 → logged as TIED; champion unchanged.
       - LEVEL 3 (promotion checkpoint, optional, ~5 min): Level 2 + integration suite.
         Triggered only via --checkpoint flag or explicit invocation. Not per-iteration.

    3. Burst mode per §12:
       - --burst-n N: accumulate up to N iterations with Level 1 only before a Level 2
         barrier
       - Barrier triggered by: reaching N iterations OR first KEEP candidate (strongest
         candidate during burst runs Level 2)
       - Level 2 PASS → promote to champion, reset burst counter
       - Level 2 FAIL → treat as DISCARD, continue burst
       - --burst-n 1: Level 2 after every KEEP candidate (conservative)
       - --burst-n 0: Level 2 every iteration (disabled burst; slowest)

    4. Loop behavior per §12:
       a. Establish baseline (invoke `comp-learns-ratchet --once` to populate champion.json)
       b. Until budget exhausted OR plateau detected:
          - Generate compiler mutation (agent proposes change — this is the DS agent's
            work delivered as a micro-cycle bundle per §4; loop consumes it)
          - Run Level 1 validation via `comp-preflight --mode dev` + unit tests
          - Level 1 FAIL → log DISCARD, continue
          - Run `comp-learns-ratchet --once` with the mutated compiler
          - KEEP candidate:
            * Within burst window: accumulate, defer Level 2
            * At burst barrier: run Level 2 on strongest candidate
              - Level 2 PASS → update champion, log KEEP
              - Level 2 FAIL → log DISCARD
          - DISCARD or TIED → log, continue
          - Plateau (N consecutive non-KEEP across burst barriers, not individual burst
            iterations) → emit plateau signal; loop pauses; MCP COO with champion state
       c. On plateau: pause (do not exit); wait for COO signal (resume, redirect, stop)
       d. On budget exhaustion: emit summary + final champion state; exit 0

    5. experiment_log.jsonl entry format per §12:
       ```json
       {
         "iteration": int,
         "verdict": "KEEP"|"DISCARD"|"TIED",
         "primary_metric": float,
         "delta": float,
         "validation_level": "unit"|"integration"|"full",
         "level2_run": bool,
         "level2_pass": bool,
         "burst_position": int,
         "mutation_type": str,
         "intervention_tag": str,
         "compiler_sha": str,
         "baseline_commit": str,
         "wall_clock_sec": int,
         "timestamp": "ISO8601"
       }
       ```
       One line per iteration; append-only. File at comp/results/{wave_id}/experiment_log.jsonl.

    6. Kill switch per §12:
       - Check `comp/dev-loop-stop` sentinel file at each iteration start
       - If present: exit gracefully after current iteration completes; write final
         summary + champion state; emit MCP (PushNotification-equivalent via send_message)
         to COO before exit

    7. Plateau detection per §12:
       - --plateau-n default 5 consecutive non-KEEP iterations (counting through burst
         barriers, not individual burst iterations)
       - On plateau: loop pauses; MCPs COO with:
         (a) current champion state (sha + primary_metric + baseline_commit)
         (b) last N verdicts
         (c) mutation_type distribution across non-KEEPs
         (d) intervention_tag grouping of non-KEEPs
       - Resume on COO signal (configurable: resume with different strategy, redirect,
         or stop). Simplest: loop reads a file comp/dev-loop-resume.yaml written by COO;
         absent = keep waiting; present = read directives.

    8. dev-4 special success gate per BACKLOG_V1 §7 + CTO handoff:
       - dev-4 is the compiler-win seed. Its success condition is NOT a local validation
         pass alone. It requires a real primary_metric KEEP under the ratchet loop.
       - If the CLI target corresponds to dev-4 (detect via --target or by reading the
           dev_backlog entry), the loop prints a prominent notice at start: "dev-4 success
           requires primary_metric KEEP under ratchet; local validation pass is NOT
           sufficient."
       - At loop termination, if target is dev-4: print explicit summary "dev-4 run
           result: KEEP achieved=YES|NO" so COO/CTO review is unambiguous.

    9. Baseline pinning gate per BACKLOG_V1 §9 rule 7:
       - Before first iteration, read the dev_backlog entry for the target
       - If `baseline_commit` is BLANK: EXIT 1 with clear error "dev_active run requires
         committed baseline_commit in YAML; blank detected"
       - If `baseline_commit` is populated but the git working tree HEAD doesn't match
           (and is not a known branch head): log WARNING (matches CHECK 2b soft behavior)
       - This is a hard gate for unpinned active runs (rule 7 is non-negotiable)

    10. Unit tests at comp/tests/test_dev_loop.py covering:
        - Level 1 FAIL path → DISCARD logged, loop continues
        - KEEP candidate within burst: accumulates, defers Level 2
        - KEEP candidate at burst barrier: Level 2 runs; PASS promotes champion; FAIL discards
        - Plateau detection fires at N consecutive non-KEEP
        - Kill switch: sentinel file triggers graceful exit with summary written
        - Blank baseline_commit in dev_backlog → EXIT 1 at startup
        - experiment_log.jsonl schema: each entry valid JSON, all required fields present
        - dev-4 run emits special notices at start + end
        - Budget exhaustion emits summary + exit 0

    Explicitly out of scope:
    - Implementing comp-preflight (that is .042).
    - Implementing comp-wave-runner (that is .043).
    - Authoring the actual compiler mutations (that is DS-agent / downstream work).
    - comp-learns-ratchet re-implementation — this loop USES it.
    - Stage 2 eval-mode activation (dev mode is independent; .044 may ship + activate
      without .045 per §11).
    - Rich experiment-log analysis tools (deferred per §14 residual gap 5).
  </objective>

  <compiler_tools_mandate>
    <phase id="1" when="before write">
      <step>
        <run>comp-build && pytest comp/ -q</run>
        <expect>Clean baseline including .042 preflight tests green.</expect>
        <if_mismatch>Rebase / fix.</if_mismatch>
      </step>
      <step>
        <run>python comp/bin/comp-preflight.py --help</run>
        <expect>Help prints; .042 shipped.</expect>
        <if_mismatch>STOP. MCP COO — .042 prerequisite missing.</if_mismatch>
      </step>
      <step>
        <run>ls comp/bin/ | grep -i ratchet</run>
        <expect>comp-learns-ratchet runner present (shipped in .023).</expect>
        <if_mismatch>STOP. MCP COO — ratchet runner missing; hard dependency for the loop.</if_mismatch>
      </step>
    </phase>
    <phase id="2" when="before commit">
      <step>
        <run>python -m py_compile comp/bin/comp-dev-loop.py</run>
        <expect>Exit 0.</expect>
        <if_mismatch>Fix syntax.</if_mismatch>
      </step>
      <step>
        <run>.tools/ds-commit-gate.sh comp/bin/comp-dev-loop.py comp/tests/test_dev_loop.py</run>
        <expect>Exit 0.</expect>
        <if_mismatch>Fix each issue.</if_mismatch>
      </step>
      <step>
        <run>pytest comp/tests/test_dev_loop.py -v</run>
        <expect>All enumerated cases PASS.</expect>
        <if_mismatch>Debug. Do not commit partial.</if_mismatch>
      </step>
      <step>
        <run>pytest comp/ -q</run>
        <expect>Full suite GREEN.</expect>
        <if_mismatch>Fix.</if_mismatch>
      </step>
      <step>
        <run>python comp/bin/comp-dev-loop.py --target dev-httpx-001 --budget-hours 0 --judge real --burst-n 3 --dry-run 2>&1 | head -30</run>
        <expect>Prints startup validation + exits 0 without running iterations (--budget-hours 0 forces immediate exit). Validates CLI parse + dev_backlog read + baseline pinning gate logic.</expect>
        <if_mismatch>If baseline_commit for dev-httpx-001 is blank (expected if dev-1 seed hasn't shipped), the loop correctly EXIT 1 with clear error. Verify that's the actual failure mode.</if_mismatch>
      </step>
    </phase>
    <phase id="3" when="after commit">
      <step>
        <run>comp-build</run>
        <expect>Clean.</expect>
        <if_mismatch>Surface to COO.</if_mismatch>
      </step>
      <step>
        <run>pytest comp/tests/test_dev_loop.py comp/tests/test_preflight.py -v</run>
        <expect>Both GREEN — .042 + .044 integrated.</expect>
        <if_mismatch>Fix.</if_mismatch>
      </step>
    </phase>
  </compiler_tools_mandate>

  <cross_domain_coordination>
    <note>.042 (comp-preflight, 1.4.0_DS) is a hard prerequisite — this loop calls it per iteration in --mode dev. .043 (comp-wave-runner, 1.3.0_DS) is parallel — they share the result.json + experiment_log.jsonl schemas. Do NOT let schema drift; if you find a §4 or §12 ambiguity, MCP 1.3.0_DS directly (same wave 2 pod) to align on a single interpretation. Dev-mode does NOT involve SC — do not MCP SC for dev-mode bundles (category error per AUTOMATION_V1 §10).</note>
    <shared_artifacts>comp/bin/comp-preflight.py (read via subprocess); result.json schema (AUTOMATION_V1 §4, shared with .043); experiment_log.jsonl schema (§12, shared with .043); comp/dev-loop-stop (kill switch sentinel, COO-writable); comp/dev-loop-resume.yaml (plateau-resume directive, COO-writable)</shared_artifacts>
  </cross_domain_coordination>

  <acceptance_criteria>
    1. comp/bin/comp-dev-loop.py implements §12 validation ladder (Levels 1 + 2 + 3) + burst mode + plateau detection + kill switch + experiment_log.jsonl schema.
    2. --burst-n, --plateau-n, --validation-level CLI flags with documented defaults.
    3. dev-4 target emits explicit success-condition notice at start + end.
    4. Baseline pinning gate: blank baseline_commit → EXIT 1 with clear error.
    5. comp/tests/test_dev_loop.py covers all enumerated test cases; all PASS.
    6. experiment_log.jsonl entries validate against §12 schema (all required fields).
    7. pytest comp/ -q GREEN.
    8. Kill switch verified in test (sentinel file → graceful exit + summary written + MCP to COO).
    9. Commit under --author=1.1.0_DS_CompLearns@opal.agent with --only pathspec scoped to comp/bin/comp-dev-loop.py + comp/tests/test_dev_loop.py + fixtures.
    10. Pushed to CLOUD.
    11. Session log with Compiler Tools section.
    12. MCP COMPLETE to 2.1.0_SA_COO with sha. Dev mode may activate after this TO + .042 are both COMPLETE, independent of .043 + .045.
  </acceptance_criteria>

  <dependencies>
    - Gate: .042 (comp-preflight.py) COMPLETE.
    - Gate: comp-learns-ratchet runner (shipped in .023) must be callable via subprocess.
    - Parallel: .043 (shared schemas, no direct dependency).
    - Blocks: nothing formally, but: dev-mode Wave 2 throughput blocked until this ships. Per §13 priority rule, ships BEFORE .043 if resourcing tight.
  </dependencies>

  <operational_notes>
    - Operate from /c/Users/AndrewBerman/Desktop/feature_clb. Confirm pwd.
    - The DS agent's micro-cycle bundle (changes.patch + result.json) is the loop's
      INPUT per iteration — the loop does NOT itself author mutations. It consumes them.
      Agent-proposer wiring (how the DS agent is invoked per iteration) is currently
      out of scope; document the integration seam in code comments but keep the loop
      agnostic to the agent implementation for v1.
    - comp-learns-ratchet --once produces champion.json — read this between iterations
      to compare primary_metric and decide KEEP/DISCARD.
    - reasoning.md is OPTIONAL in dev-mode bundles per §4. Do NOT require it; do NOT
      reject bundles that lack it.
    - Dev-4 compiler-win: if this loop is run with --target dev-4-<slug>, the loop
      enforces the success-bar reminder. This is for COO/CTO awareness, not for auto-
      termination — the loop keeps running until budget or KEEP; the notice is cosmetic
      + unambiguous at review time.
    - No emojis in any stdout, log, or stderr.
    - Kill-switch sentinel file path (`comp/dev-loop-stop`) is a convention — add it to
      comp/.gitignore so it's never committed (it's a runtime-only file).
  </operational_notes>

  <closeout>
    On completion:
    - commit with --only --author="1.1.0_DS_CompLearns &lt;1.1.0_DS_CompLearns@opal.agent&gt;" -- comp/bin/comp-dev-loop.py comp/tests/test_dev_loop.py [fixtures] [comp/.gitignore if updated]
    - push to CLOUD
    - flip TO status to complete
    - MCP COMPLETE to 2.1.0_SA_COO with sha — dev-mode ACTIVATES on this ship (.045 gates eval mode only)
    - session log with Compiler Tools section
  </closeout>
</task_order>
