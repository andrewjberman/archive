<task_order>
  <metadata>
    <id>2.1.0_SA_COO-2026-04-27-comp-learns-077-ds-dual-output-grader-emission</id>
    <issued_by>2.1.0_SA_COO</issued_by>
    <issued_to>1.3.0_DS_CompLearns</issued_to>
    <date>2026-04-27</date>
    <status>pending</status>
    <project_code>COMP_LEARNS</project_code>
    <priority>P1 — V1.2 grader-governance ship-blocker (R-DS-1 P1, parallel with .078/.080/.081)</priority>
  </metadata>

  <references>
    <ref type="prd">docs/architecture/COMP_LEARNS_STAGE3.md §11.1 — Governance split; §11.3 — Implementation requirements (R-DS-1 P1)</ref>
    <ref type="prd_section">§11.2 — Why governance split, not replacement; §10 ship-blocker — V1.2 governance binding for any future primary case</ref>
    <ref type="cvo_ruling">CVO 20260427T200500Z grader-format ruling — refined Option C governance split. CTO V1.2 PRD codification (95f8c0d3 + e3393b26).</ref>
    <ref type="prior_ds_work">.070 sidecar (68f64865) — your prior runner.py + scorecard.py touch-points; this TO extends scorecard schema with dual-grader fields</ref>
    <ref type="cto_brief">org/tier1_exec/3.1.0_SA_CVO/responses/20260427T200500Z_to_1.1.0_SA_CTO_grader_format_ruling.md (CVO ruling)</ref>
  </references>

  <objective>
    Wire the runner to emit BOTH exact-match grader output AND semantic-aware grader output for every
    response. Both preserved in scorecard schema; neither overwrites the other. Disagreement flag emitted
    per response. Sidecar (§6.3) carries both per question per condition.

    ## Context

    V1.2 codifies a governance SPLIT (not replacement). Exact-match remains the primary ratchet/champion
    score (preserves Stage 1+2 ratchet history). Semantic-aware grading governs pre-screen partitioning
    + INVESTIGATE/SENTINEL triage. Disagreement rate becomes a first-class runtime metric — not a
    post-hoc audit.

    The disagreement rate makes grader-format problems detectable WITHOUT having to write closeout memos
    (CVO §1 — sphinx pre-screen forced this discovery; we don't want to repeat the discovery cycle).

    ## Phase 0 — Pre-implementation gate

    ```bash
    python -m pytest comp/ --ignore=comp/targets -q --tb=no 2>&1 | tail -3
    # Expect: 480 passed (or more). Zero failures.
    ```

    ## Phase 1 — Semantic grader implementation

    Implement a semantic-aware grader function alongside the existing exact-match grader. Place at:
    ```
    comp/bench/semantic_grader.py
    ```

    Semantic grader signature (inspired by R-SC-2 taxonomy):
    ```python
    def grade_semantic(response_text: str, gold_answer: str, answer_type: str = "exact") -> dict:
        """Return semantic grading result.

        Returns:
            {
              "graded": bool,                # pass/fail
              "label": str,                  # parseable-correct | parseable-wrong |
                                             # semantic-correct-but-unparseable |
                                             # semantic-wrong-unparseable | semantic-ambiguous
              "extracted_answer": str | None # what was extracted (if parseable) or null
            }
        ```

    Implementation strategy (DS choice):
    - Strip markdown wrappers (backticks, code fences, bold) before exact comparison
    - Apply case-insensitive comparison for class/method names
    - Detect "the answer is X" / "Answer: X" patterns and extract X
    - Fall through to exact-match if no pattern matches

    The semantic grader is BEST-EFFORT for V1.2; full R-SC-2 label assignment may require human audit
    in some cases. The goal is to catch the sphinx pattern (markdown-wrapped correct answers) automatically.

    Add unit tests at `comp/bench/tests/test_semantic_grader.py` covering:
    - Markdown-wrapped correct answer (sphinx q01/q07 pattern) → parseable-correct
    - Bare correct numeric (click q11 pattern) → parseable-correct
    - Wrong answer with prose wrapper → parseable-wrong
    - Ambiguous prose (no clear extraction) → semantic-ambiguous

    ## Phase 2 — Runner emission (comp/loop/runner.py)

    For every (question, condition) judge call, after the response arrives:
    1. Run existing exact-match grader → exact_match_result
    2. Run semantic grader → semantic_result
    3. Compute disagreement_flag = (exact_match_result.graded != semantic_result.graded)
    4. Pass both results forward to scorecard / sidecar / experiment_log writers

    Do NOT change the ratchet decision logic. The primary metric (ab_lift / champion comparison) still
    uses exact-match output. Semantic output is metadata for downstream triage and disagreement tracking.

    ## Phase 3 — Scorecard schema extension (comp/bench/scorecard.py)

    Per response, scorecard JSON gains:
    ```json
    "graders": {
      "exact_match": { "graded": true, "extracted_answer": "Builder", ... },
      "semantic": { "graded": true, "label": "parseable-correct", "extracted_answer": "Builder", ... },
      "disagreement_flag": false
    }
    ```

    Per scorecard summary, aggregate:
    ```json
    "disagreement_rate": 0.45,         // (count of disagreements) / (total responses)
    "disagreement_count": 18,
    "total_responses": 40
    ```

    ## Phase 4 — Sidecar schema extension (comp/loop/runner.py + manifest)

    Sidecar manifest.json (.070 R-DS-1 schema) gains:
    ```json
    "blob_grader_results": {
      "q01_C1": {
        "exact_match": { "graded": false, ... },
        "semantic": { "graded": true, "label": "parseable-correct", ... },
        "disagreement": true
      },
      ...
    }
    ```

    Per (q, condition) sidecar text file is unchanged (still raw delivered context). The blob_grader_results
    is metadata in the manifest, not a change to the blob format.

    ## Phase 5 — Pre-commit gate

    ```bash
    .tools/ds-commit-gate.sh comp/loop/runner.py comp/bench/scorecard.py comp/bench/semantic_grader.py
    ```

    ```bash
    python -m pytest comp/ --ignore=comp/targets -q --tb=short 2>&1 | tail -5
    # 480+ passed (baseline) plus new semantic_grader tests. 0 failures.
    ```

    ## Phase 6 — Smoke test

    Run mock judge against dev-click-001 with one iter:
    ```bash
    python comp/bin/comp-learns-ratchet click --judge mock --max-iter 1
    python3 -c "import json,glob; sc=json.load(open(sorted(glob.glob('comp/targets/click/scorecards/*.json'))[-1])); print('disagreement_rate:', sc.get('disagreement_rate'), 'graders sample:', list(sc.get('per_question_graders', {}).items())[:1] if sc.get('per_question_graders') else 'none')"
    ```

    Verify scorecard contains disagreement_rate field and per-response graders block.

    ## Phase 7 — Commit and push

    ```bash
    git commit --only \
      --author="1.3.0_DS_CompLearns <1.3.0_DS_CompLearns@opal.agent>" \
      -m "feat(COMP_LEARNS.077): dual-output grader emission (R-DS-1 P1) -- exact-match + semantic + disagreement_flag" \
      -- comp/loop/runner.py \
         comp/bench/scorecard.py \
         comp/bench/semantic_grader.py \
         comp/bench/tests/test_semantic_grader.py
    git push origin CLOUD
    ```

    ## Phase 8 — MCP

    MCP 2.1.0_SA_COO with:
    - Commit sha
    - Semantic grader implementation summary (what patterns it catches)
    - Test count (480+ baseline + new semantic_grader tests)
    - Smoke test confirms disagreement_rate field present in scorecard
    - Sample (q,c) entry from sidecar manifest with both graders' output
  </objective>

  <compiler_tools_mandate>
    <phase id="1" when="before write">
      <step>
        <run>python -m pytest comp/ --ignore=comp/targets -q --tb=no 2>&amp;1 | tail -3</run>
        <expect>480 passed (or more). Zero failures.</expect>
        <if_mismatch>STOP. MCP COO before proceeding.</if_mismatch>
      </step>
    </phase>
    <phase id="2" when="before commit">
      <step>
        <run>.tools/ds-commit-gate.sh comp/loop/runner.py comp/bench/scorecard.py comp/bench/semantic_grader.py</run>
        <expect>All 3 checks exit 0 (py_compile + ds-precommit-check + ruff) per file.</expect>
        <if_mismatch>STOP. Fix flagged issue.</if_mismatch>
      </step>
      <step>
        <run>python -m pytest comp/ --ignore=comp/targets -q --tb=short 2>&amp;1 | tail -5</run>
        <expect>480+ passed plus new semantic_grader tests. 0 failures.</expect>
        <if_mismatch>STOP. Fix regression.</if_mismatch>
      </step>
    </phase>
  </compiler_tools_mandate>

  <cross_domain_coordination>
    <note>
      Parallel with .078 (SC subtype split), .080 (DS sphinx schema), .081 (SC pilot).
      .079 (SC disagreement labels) GATES on this TO complete -- SC needs scorecard fields to emit per-Q disagreement labels.
      Path B target re-selection sub-PRD authoring (COO) gates on .077 + .078 + .079 all complete (V1.2 §10 ship-blocker).
    </note>
  </cross_domain_coordination>

  <acceptance_criteria>
    1. comp/bench/semantic_grader.py implements grade_semantic() with R-SC-2 label output.
    2. semantic_grader unit tests cover: markdown-wrapped correct, bare numeric correct, wrong-with-prose, ambiguous.
    3. comp/loop/runner.py runs both graders per response; computes disagreement_flag.
    4. Ratchet primary metric still uses exact-match output (NO change to champion selection).
    5. comp/bench/scorecard.py emits per-response graders block + summary disagreement_rate + disagreement_count + total_responses.
    6. Sidecar manifest.json (per .070 schema) gains blob_grader_results dict.
    7. ds-commit-gate.sh exits 0 on all changed files.
    8. pytest 480+ baseline + semantic_grader tests, 0 failures.
    9. Smoke test confirms disagreement_rate present in scorecard JSON.
    10. Committed --only --author=1.3.0_DS_CompLearns. Pushed to CLOUD.
    11. MCP 2.1.0_SA_COO with commit sha + grader summary + test count.
  </acceptance_criteria>

  <dependencies>
    - No gates. Parallel with .078/.080/.081.
    - .079 (SC disagreement labels) GATES on this TO.
    - V1.2 §10 ship-blocker for primary case dispatch requires .077+.078+.079 complete.
  </dependencies>

  <operational_notes>
    - Operate from /c/Users/AndrewBerman/Desktop/feature_clb (COMP_LEARNS worktree).
    - No emojis.
    - DO NOT change ratchet champion selection or primary metric computation. Exact-match grader stays primary per V1.2 §11.1.
    - Semantic grader is BEST-EFFORT; perfect R-SC-2 label assignment may require human audit. Goal is automated detection of sphinx-pattern markdown-wrapping.
    - Disagreement flag is a runtime signal, not an alarm — high disagreement rate on a target indicates "investigate grader-target fit," not "broken target."
  </operational_notes>

  <closeout>
    - flip TO status to complete with commit sha
    - git push origin CLOUD from feature_clb
    - MCP 2.1.0_SA_COO with commit sha + smoke test confirmation
    - session log
  </closeout>
</task_order>
