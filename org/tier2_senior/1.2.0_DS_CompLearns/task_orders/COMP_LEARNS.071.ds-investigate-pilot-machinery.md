<task_order>
  <metadata>
    <id>2.1.0_SA_COO-2026-04-27-comp-learns-071-ds-investigate-pilot-machinery</id>
    <issued_by>2.1.0_SA_COO</issued_by>
    <issued_to>1.2.0_DS_CompLearns</issued_to>
    <date>2026-04-27</date>
    <status>complete</status><!-- 710c973e -- 2026-04-27 -->
    <project_code>COMP_LEARNS</project_code>
    <priority>P0 — Stage 3 ship-blocker R-DS-2 (parallel with .070/.072/.073)</priority>
  </metadata>

  <references>
    <ref type="prd">docs/architecture/COMP_LEARNS_STAGE3.md §5 — INVESTIGATE pilot machinery (R-DS-2)</ref>
    <ref type="prd_section">§5.2 — Pilot mechanics: paired C4+C1, N=8, dual-condition gate. §5.3 — Cost discipline (bounded, non-ratchet).</ref>
    <ref type="prd_context">§2 — Pre-screen triage matrix; §2.4 — Wrong|Wrong subtypes. Pilot runs after pre-screen, for pilot_eligible=true questions only.</ref>
    <ref type="runner">comp/loop/runner.py — primary implementation target</ref>
    <ref type="cvo_ruling">CVO R-DS-2 (§5) — dual-condition gate corrects V1's absolute-only rule (admitted prior-dominated + noisy questions). Pilot is non-ratchet — does NOT affect champion selection.</ref>
    <ref type="pytest_baseline">458 tests passing (comp/ --ignore=comp/targets) — do not regress</ref>
  </references>

  <objective>
    Implement INVESTIGATE pilot machinery: a non-ratchet runner mode that executes paired C4+C1 trials
    at N=8 per condition for each INVESTIGATE question with pilot_eligible=true, applies the dual-condition
    gate, and emits a pilot artifact recording the decision.

    ## Context

    Stage 3's pre-screen partitions questions into INCLUDE / SENTINEL / INVESTIGATE. INVESTIGATE questions
    with pilot_eligible=true are full-source-overload candidates — questions the compiler may recover that
    full-source prompting could not. The pilot decides their fate before primary metric scoring begins.

    The CVO V1.1 correction (paired C4+C1, N=8, dual gate) ensures that a question is promoted to INCLUDE
    only when there is BOTH a credible solvability signal (C4 ≥ 5/8) AND a positive lift signal (C4 − C1 ≥ 2
    trials). Without the C1 comparison, a question scoring 3/5 on C4 where C1 also scores 3/5 would
    (incorrectly) be promoted under V1's absolute-only rule.

    The pilot is non-ratchet: it uses the real judge but does NOT update champion.json, does NOT append
    to experiment_log.jsonl, and does NOT trigger any ratchet terminal condition. It is a one-time
    pre-dispatch decision pass.

    ## Phase 0 — Pre-implementation baseline gate

    ```bash
    python -m pytest comp/ --ignore=comp/targets -q --tb=no 2>&1 | tail -3
    # Expect: 458 passed (or more). Zero failures.
    ```

    ## Phase 1 — Runner pilot mode

    Add a `--pilot` flag (or equivalent) to `comp/bin/comp-learns-ratchet` (or a new entry-point
    `comp/bin/comp-learns-pilot`) that accepts:
    - `--target <target>` — the target identifier
    - `--questions <q01,q03,...>` — comma-separated question IDs marked pilot_eligible=true
    - `--n <int>` — number of trials per condition per question (default 8)
    - `--judge <real|mock>` — judge mode (real = ANTHROPIC_API_KEY required)
    - `--compiler-content-sha <sha>` — traceability field for pilot artifact

    The pilot runner:
    1. For each pilot_eligible question:
       a. Run N C4 trials (full two-step: background_index=True, addressing=mechanical, full compiler expansion)
       b. Run N C1 trials (unaided: background_index=False, no compiler context)
       c. Record per-trial binary pass/fail for each condition
    2. Apply the decision rule:
       - PROMOTE to INCLUDE if C4_successes >= ceil(N * 5/8) AND (C4_successes - C1_successes) >= 2
         (for N=8: C4 >= 5 AND delta >= 2)
       - DEMOTE to SENTINEL (ceiling) if C4_successes <= floor(N * 1/8)
         (for N=8: C4 <= 1)
       - DEMOTE to SENTINEL (prior-dominated) if C1_successes >= floor(N * 6/8) AND (C4_successes - C1_successes) <= 0
         (for N=8: C1 >= 6 AND C4 <= C1)
       - HOLD (INVESTIGATE — insufficient signal) otherwise
    3. Emit a pilot artifact per question and a summary artifact.

    Decision rule parameters scale with N: compute thresholds as fractions of N (5/8, 1/8, 6/8) so
    the rule generalizes if N is adjusted. Default N=8.

    ## Phase 2 — Pilot artifact schema

    Write per-question results to:
    ```
    comp/results/<target>/pilot/<run_timestamp>/pilot_<question_id>.json
    ```

    Per-question artifact:
    ```json
    {
      "schema_version": 1,
      "target": "<target>",
      "question_id": "<qID>",
      "compiler_content_sha": "<sha>",
      "n_trials": 8,
      "c4_trials": [true, false, ...],
      "c1_trials": [true, false, ...],
      "c4_successes": 5,
      "c1_successes": 2,
      "delta": 3,
      "decision": "PROMOTE | DEMOTE_CEILING | DEMOTE_PRIOR_DOMINATED | HOLD",
      "decision_rule": "c4_successes >= 5/8*N AND delta >= 2",
      "timestamp": "<ISO8601>"
    }
    ```

    Write a summary artifact:
    ```
    comp/results/<target>/pilot/<run_timestamp>/pilot_summary.json
    ```

    ```json
    {
      "schema_version": 1,
      "target": "<target>",
      "compiler_content_sha": "<sha>",
      "n_trials": 8,
      "questions": {
        "<qID>": {
          "decision": "PROMOTE",
          "c4_successes": 5,
          "c1_successes": 2,
          "delta": 3
        },
        ...
      },
      "promote_count": 1,
      "demote_ceiling_count": 0,
      "demote_prior_dominated_count": 0,
      "hold_count": 0,
      "timestamp": "<ISO8601>"
    }
    ```

    ## Phase 3 — Pre-commit gate

    ```bash
    .tools/ds-commit-gate.sh comp/loop/runner.py
    # Also gate any new bin/ entry-point if added:
    # .tools/ds-commit-gate.sh comp/bin/comp-learns-pilot
    ```

    ```bash
    python -m pytest comp/ --ignore=comp/targets -q --tb=short 2>&1 | tail -5
    # 458+ passed, 0 failed.
    ```

    Add at least one unit test for the decision-rule logic (pass mock trial arrays; verify PROMOTE /
    DEMOTE / HOLD outputs match expected). This is a new code path with non-trivial branching — a
    test is mandatory, not optional.

    ## Phase 4 — Smoke test with mock judge

    ```bash
    python comp/bin/comp-learns-ratchet click --pilot --questions q03 --n 4 --judge mock
    # or equivalent entry-point
    ls comp/results/dev-click-001/pilot/*/pilot_q03.json
    python3 -c "import json; a=json.load(open(sorted(__import__('glob').glob('comp/results/dev-click-001/pilot/*/pilot_q03.json'))[-1])); print('decision:', a['decision'], 'c4:', a['c4_successes'], 'c1:', a['c1_successes'])"
    ```

    With mock judge the pass/fail values will be deterministic or random — confirm the artifact is
    written, the decision field is one of the four valid values, and the summary is also written.

    ## Phase 5 — Commit and push

    ```bash
    git commit --only \
      --author="1.2.0_DS_CompLearns <1.2.0_DS_CompLearns@opal.agent>" \
      -m "feat(COMP_LEARNS.071): INVESTIGATE pilot machinery (R-DS-2) -- paired C4+C1 N=8 dual-gate + pilot artifact" \
      -- comp/loop/runner.py \
         comp/bin/comp-learns-ratchet
    # Include any new files (tests, new bin entry-point) in the pathspec
    git push origin CLOUD
    ```

    ## Phase 6 — MCP

    MCP 2.1.0_SA_COO with:
    - Commit sha
    - Entry-point invocation form (flag or separate binary)
    - Decision rule thresholds applied for N=8
    - Test count (must be 458+ plus new pilot tests)
    - Smoke-test artifact path + decision value observed
  </objective>

  <compiler_tools_mandate>
    <phase id="1" when="before write">
      <step>
        <run>python -m pytest comp/ --ignore=comp/targets -q --tb=no 2>&amp;1 | tail -3</run>
        <expect>458 passed (or more). Zero failures.</expect>
        <if_mismatch>STOP. Report failure count to COO before proceeding.</if_mismatch>
      </step>
    </phase>
    <phase id="2" when="before commit">
      <step>
        <run>.tools/ds-commit-gate.sh comp/loop/runner.py</run>
        <expect>All 3 checks exit 0 (py_compile + ds-precommit-check + ruff).</expect>
        <if_mismatch>STOP. Fix flagged issue.</if_mismatch>
      </step>
      <step>
        <run>python -m pytest comp/ --ignore=comp/targets -q --tb=short 2>&amp;1 | tail -5</run>
        <expect>458+ passed, 0 failed (including new pilot decision-rule tests).</expect>
        <if_mismatch>STOP. Fix regression before committing.</if_mismatch>
      </step>
    </phase>
  </compiler_tools_mandate>

  <cross_domain_coordination>
    <note>
      Parallel with .070 (sidecar), .072 (SC pre-screen), .073 (COO packet schema).
      No shared artifact writes with those TOs.
      Pilot execution (consuming this machinery) is gated on .075 (pre-screen) + .076 (CTO off-ramp),
      which identify the pilot_eligible question list. This TO delivers the machinery only.
    </note>
  </cross_domain_coordination>

  <acceptance_criteria>
    1. Pilot runner mode implemented: --pilot flag or comp/bin/comp-learns-pilot entry-point accepting --target, --questions, --n, --judge, --compiler-content-sha.
    2. Per-question pilot artifact written to comp/results/&lt;target&gt;/pilot/&lt;timestamp&gt;/pilot_&lt;qID&gt;.json with schema_version=1.
    3. pilot_summary.json written with promote/demote/hold counts.
    4. Decision rule implements dual-condition gate: PROMOTE requires C4 >= 5/8*N AND delta >= 2; DEMOTE_CEILING requires C4 <= 1/8*N; DEMOTE_PRIOR_DOMINATED requires C1 >= 6/8*N AND delta <= 0; HOLD otherwise.
    5. At least one unit test for decision-rule logic (mock trial arrays, verify output).
    6. Pilot mode does NOT write to experiment_log.jsonl, does NOT update champion.json, does NOT trigger ratchet terminal conditions.
    7. ds-commit-gate.sh exits 0 on all modified files.
    8. pytest comp/ --ignore=comp/targets passes 458+ tests, 0 failures.
    9. Smoke test confirms pilot artifact written correctly for mock run.
    10. Committed --only --author=1.2.0_DS_CompLearns. Pushed to CLOUD.
    11. MCP 2.1.0_SA_COO with commit sha + invocation form + test count.
  </acceptance_criteria>

  <dependencies>
    - No gates. Parallelizable with .070/.072/.073.
    - Pilot execution (to be dispatched after .076 CTO off-ramp ruling) gates on this TO complete.
    - .075 (sphinx pre-screen execution) does NOT require this TO.
  </dependencies>

  <operational_notes>
    - Operate from /c/Users/AndrewBerman/Desktop/feature_clb (COMP_LEARNS worktree).
    - No emojis in code or logs.
    - Pilot is non-ratchet. Do not couple it to the champion selection or ratchet state machine.
    - The N=8 default is PRD-specified. Make N configurable but default to 8.
    - Decision thresholds must be computed as fractions of N (not hardcoded for N=8).
    - ANTHROPIC_API_KEY is not needed for Phase 4 smoke test (--judge mock).
    - from __future__ import annotations required for any new gold/ or script/ file; not required for comp/loop/ or comp/bin/ files, but run pre-commit gate.
    - If the pilot runner is added as a new comp/bin/ script, include it in the ds-commit-gate.sh call.
  </operational_notes>

  <closeout>
    - flip TO status to complete with commit sha
    - git push origin CLOUD from feature_clb
    - MCP 2.1.0_SA_COO with commit sha + invocation + test count
    - session log
  </closeout>
</task_order>
