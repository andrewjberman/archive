<task_order>
  <metadata>
    <id>1.1.0_DS_CompLearns-2026-04-21-comp-learns-023-comp-learns-ratchet-runner</id>
    <issued_by>1.1.0_SA_CTO</issued_by>
    <issued_to>1.1.0_DS_CompLearns</issued_to>
    <date>2026-04-21</date>
    <status>complete <!-- 41225ed9 --></status>
    <evidence>
      Shipped: commit 41225ed9 — comp-learns-ratchet Python runner (Layer B) (COMP_LEARNS.023).
      Artifacts: comp/bin/comp-learns-ratchet (105 lines, executable, shebang #!/usr/bin/env python3), comp/loop/runner.py (352 lines: RunnerConfig, ExitCode enum, run()/do_status()/do_halt(), judge instantiation, plateau/budget/halt/SIGTERM terminal conditions, _print_summary()), comp/bin/comp-learns-run.sh (DEPRECATED header added per AC#10), comp/loop/tests/test_runner_cli.py (129 lines: CLI dispatch, --judge required, exit codes), comp/loop/tests/test_runner_resume.py (71 lines: --resume semantics, next_iter(), start_iter calculation), comp/loop/tests/test_runner_terminal_conditions.py (plateau detection, halt, budget, threshold, fork).
      Validation: AC#1 comp/bin/comp-learns-ratchet committed executable with shebang PASS. AC#2 --judge required: no-flag invocation exits 2 with usage naming --judge mock|real (test_runner_cli.py) PASS. AC#3 mock smoke --judge mock --max-iter 3 completes, appends 3 entries, exits 10 (MAX_ITER) PASS. AC#4 threshold exit exits 0 THRESHOLD_REACHED (test_runner_terminal_conditions.py) PASS. AC#5 plateau detection: fixture with 5 tied same-sha entries exits 12 PLATEAU (test_runner_terminal_conditions.py) PASS. AC#6 halt: .halt file before run exits 13 before first iterate() call PASS. AC#7 --resume with existing 8-entry log runs iters 9+10 only (test_runner_resume.py) PASS. AC#8 grep comp/loop/runner.py: zero refs to comp.framework.run / results.tsv / comp-learns-run.sh / behavioral pass rate PASS. AC#9 pytest test_runner_terminal_conditions.py test_runner_resume.py test_runner_cli.py green (35 tests) PASS. AC#10 DEPRECATED header in comp/bin/comp-learns-run.sh PASS. AC#11 _print_summary() emits six-field summary on every exit path (champion sha/pm/f1/loc + elapsed + iters + judge mode) PASS. AC#12 ds-commit-gate.sh passed on all .py files PASS.
      Session log: org/tier2_senior/1.1.0_DS_CompLearns/logs/2026-04-21/.
    </evidence>
    <project_code>COMP_LEARNS</project_code>
    <priority>P0 — critical path; Phase 1 exit condition; blocks .024/.025/.026/.027/.028</priority>
  </metadata>

  <references>
    <ref type="prd">docs/architecture/COMP_LEARNS_RUNTIME_V1.md §3 (Layer B), §4 (terminal conditions), §10 (status views), §13 (phase 1 exit)</ref>
    <ref type="precedent">comp/bin/comp-learns-run.sh (bash driver — Layer C, to be deprecated in .028; read for kill-switch contract only, do NOT port semantics)</ref>
    <ref type="engine">comp/loop/ratchet.py::iterate() (Layer A — unchanged; runner calls this)</ref>
  </references>

  <objective>
    Ship `comp/bin/comp-learns-ratchet` — the authoritative Python orchestrator around `ratchet.iterate()`. Multi-iteration, ratchet-native terminal conditions, explicit `--judge mock|real`, resume/halt/status. After this TO merges, operators run ratchet sequences through this binary and never through the bash driver.

    Explicitly in scope:
    1. New Python entry point `comp/bin/comp-learns-ratchet` (executable, shebang `#!/usr/bin/env python3`).
    2. Companion module `comp/loop/runner.py` holding the orchestration logic (runner thin, logic testable).
    3. Ratchet-native terminal conditions per PRD §4 — no behavioral pass-rate, no TSV plateau.
    4. `--resume` (pick up from latest experiment-log iter + champion state), `--halt` (write `.halt` marker), `--status` (derived view per §10 — stub acceptable at this TO, full impl lands in .026).
    5. One-paragraph human summary on exit, derived from artifacts only.
    6. Unit tests for terminal-condition evaluation, resume semantics, and CLI arg parsing.

    Explicitly out of scope (handled in later TOs):
    - provenance fields (`judge_mode`, `benchmark_honest`, compare explainability) — .024/.025
    - selector tie rendering — .026
    - legacy-loop removal — .028
    - real-judge proving sequence — .027
  </objective>

  <scope>
    <files>
      <file action="create">comp/bin/comp-learns-ratchet</file>
      <file action="create">comp/loop/runner.py</file>
      <file action="create">comp/loop/tests/test_runner_terminal_conditions.py</file>
      <file action="create">comp/loop/tests/test_runner_resume.py</file>
      <file action="create">comp/loop/tests/test_runner_cli.py</file>
      <file action="modify">comp/bin/comp-learns-run.sh (prepend DEPRECATED header; no functional change)</file>
    </files>
  </scope>

  <wire_contract>
    **CLI contract** (PRD §3 Layer B):
    ```
    comp-learns-ratchet <target> --judge mock|real [--max-iter N] [--budget-sec N] [--threshold F] [--plateau-k N] [--resume]
    comp-learns-ratchet <target> --status
    comp-learns-ratchet <target> --halt
    ```
    - `--judge` is REQUIRED (no default). Missing → exit 2 with usage message. Rationale: prevents silent demo runs.
    - `--max-iter` default 20. `--budget-sec` default 43200 (12h). `--threshold` default 1.30 (httpx). `--plateau-k` default 5.
    - `<target>` resolves to `comp/targets/<target>/`. Unknown target → exit 2.

    **Runner loop shape** (pseudocode, owns nothing beyond orchestration):
    ```python
    def run(target: str, cfg: RunnerConfig) -> ExitCode:
        ctx = resolve_target_context(target)  # paths, compiler fn, judge instance
        start_iter = next_iter_number(ctx.experiment_log_path) if cfg.resume else 1
        t0 = time.monotonic()
        for i in range(start_iter, cfg.max_iter + 1):
            if halt_requested(ctx.halt_path): return ExitCode.HALTED
            if budget_exceeded(t0, cfg.budget_sec): return ExitCode.BUDGET
            result = ratchet.iterate(..., iter_num=i, judge=ctx.judge)
            if result.primary_metric >= cfg.threshold: return ExitCode.THRESHOLD_REACHED
            if at_plateau(ctx.experiment_log_path, cfg.plateau_k): return ExitCode.PLATEAU
            if result.verdict == Verdict.FORKED: return ExitCode.FORK
        return ExitCode.MAX_ITER
    ```

    **Terminal conditions** (ratchet-native, PRD §4):
    - `primary_metric >= threshold` — check AFTER iterate() returns, before loop increments
    - plateau: last `plateau_k` experiment-log verdicts ∈ {tied, discarded} with no KEEP in window AND no champion-sha change in window. Read from `experiment_log.jsonl`, NOT from any TSV.
    - `--max-iter` — loop boundary
    - `--budget-sec` — wall-clock since runner start
    - `.halt` file at `comp/targets/<target>/.halt` — polled at top of each iter
    - `Verdict.FORKED` returned by iterate() → halt, exit with fork code

    **Forbidden terminal conditions** (must NOT be reachable in this runner):
    - behavioral pass-rate threshold
    - anything reading `results.tsv`
    - anything calling `comp.framework.run`

    **Exit codes**:
    ```
    0 = THRESHOLD_REACHED (success)
    1 = runner error (bug / IO)
    2 = usage error (missing --judge, unknown target, etc.)
    10 = MAX_ITER
    11 = BUDGET
    12 = PLATEAU
    13 = HALTED
    14 = FORK (SelectorGameDetected)
    ```

    **Resume semantics**:
    - `--resume` reads `experiment_log.jsonl`, finds max `iter`, starts at max+1
    - if log is empty or missing → error "nothing to resume" (exit 2)
    - champion state is whatever `champion.json` says; runner does not touch it

    **Halt semantics**:
    - `comp-learns-ratchet <target> --halt` writes `comp/targets/<target>/.halt` (contents: ISO8601 timestamp)
    - any running `comp-learns-ratchet <target>` process detects it at top of next iter and exits 13
    - SIGTERM to the runner process also exits 13 cleanly (signal handler)
    - `.halt` is NOT auto-cleared; operator removes it before next resume

    **Status (stub for this TO; full impl in .026)**:
    - `--status` prints: target, current champion (sha + primary_metric + structural_f1 + compiler_loc), last 3 experiment-log entries, iter count
    - full tie-rendering + cache-provenance + judge_mode block deferred to .026
    - mark the stub with `# TODO(.026): expand per RUNTIME_V1.md §10`

    **Summary on exit**:
    ```
    [comp-learns-ratchet httpx] exit=THRESHOLD_REACHED at iter=12
      champion: sha=13254d0 primary_metric=1.3012 structural_f1=0.5800 loc=31
      elapsed: 00:42:18  iters: 12  judge: real
      artifacts: comp/targets/httpx/{champion.json, experiment_log.jsonl, scorecards/}
    ```
    Paragraph is derived from artifacts only. No separate state system.
  </wire_contract>

  <acceptance_criteria>
    1. **Entry point executable**: `chmod +x comp/bin/comp-learns-ratchet` committed; shebang `#!/usr/bin/env python3`; `.tools/` PATH or explicit `comp/bin/` invocation both work.
    2. **--judge required**: `comp-learns-ratchet httpx` (no `--judge`) exits 2 with usage message naming `--judge mock|real`.
    3. **Mock smoke**: `comp-learns-ratchet httpx --judge mock --max-iter 3` completes, appends 3 new entries to `experiment_log.jsonl`, updates (or leaves stable) `champion.json`, exits 10 (MAX_ITER).
    4. **Threshold exit**: with a compiler known to clear threshold in ≤2 iters (use existing `13254d0` champion + a mock judge gold-aware wrapper), `--threshold 1.20 --max-iter 5` exits 0 with THRESHOLD_REACHED.
    5. **Plateau detection**: construct a test fixture experiment log with last 5 entries all `tied` + same champion_sha; runner invoked with `--resume --plateau-k 5` exits 12 (PLATEAU) without running a new iteration.
    6. **Halt**: touch `.halt` before running → runner exits 13 before first iterate() call. During a run, `comp-learns-ratchet httpx --halt` from another process causes next iter boundary to exit 13.
    7. **Resume**: with existing httpx log (8 entries), `--resume --max-iter 10` runs iters 9 and 10 only (2 new entries appended).
    8. **No legacy surface reached**: grep in `comp/loop/runner.py` finds zero references to `comp.framework.run`, `results.tsv`, `comp-learns-run.sh`, or `behavioral pass rate`.
    9. **Tests pass**: `pytest comp/loop/tests/test_runner_terminal_conditions.py comp/loop/tests/test_runner_resume.py comp/loop/tests/test_runner_cli.py -q` green.
    10. **DEPRECATED header on bash driver**: first 10 lines of `comp/bin/comp-learns-run.sh` contain `# DEPRECATED: use comp-learns-ratchet (comp/bin/comp-learns-ratchet). Scheduled for removal in COMP_LEARNS.028.` — no other changes to the bash file in this TO.
    11. **Summary paragraph**: stdout on every exit includes the six-field summary in the wire contract above, derived from reading `champion.json` + tail of `experiment_log.jsonl` (no internal state file consulted).
    12. **Pre-commit gate**: `.tools/ds-commit-gate.sh` passes on every new `.py` file before commit (CLAUDE.md rule 14).
  </acceptance_criteria>

  <dependencies>
    - None (this TO unblocks all of Phase 2+)
    - Does NOT require any changes to `comp/loop/ratchet.py::iterate()` — Layer A is unchanged
  </dependencies>

  <operational_notes>
    - Runner must be pure Python, no bash. Windows git-bash execution works via the shebang.
    - `comp/loop/runner.py::run()` should be importable and callable from tests without invoking the CLI — CLI is a thin `argparse` → `run()` wrapper.
    - Logging: stdout only; no log files created by the runner. iterate() handles its own artifact writes.
    - Do not add a `state.json` cache in this TO. Resume reads the experiment log directly. (PRD §10: "If `state.json` exists, it is a cache, never load-bearing.")
    - Judge instantiation: `--judge mock` → `comp.bench.judges.mock.MockJudge` (or existing gold-aware variant for smoke), `--judge real` → `comp.bench.judges.anthropic.AnthropicJudge`. Missing credentials on `real` → exit 1 with clear error.
  </operational_notes>

  <closeout>
    On completion:
    - commit with `--author="1.1.0_DS_CompLearns <1.1.0_DS_CompLearns@opal.agent>"`
    - MCP COMPLETE to 1.1.0_SA_CTO + 2.1.0_SA_COO with commit sha + AC checklist status
    - session log under `org/tier2_senior/1.1.0_DS_CompLearns/logs/2026-04-{DD}/`
    - flip TO status to `complete` with commit ref in the status comment
  </closeout>
</task_order>
