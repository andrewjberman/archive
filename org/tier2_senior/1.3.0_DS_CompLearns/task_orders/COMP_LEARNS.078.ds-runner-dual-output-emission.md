<task_order>
  <metadata>
    <id>2.1.0_SA_COO-2026-04-27-comp-learns-078-ds-runner-dual-output-emission</id>
    <issued_by>2.1.0_SA_COO</issued_by>
    <issued_to>1.3.0_DS_CompLearns</issued_to>
    <date>2026-04-27</date>
    <status>pending</status>
    <project_code>COMP_LEARNS</project_code>
    <priority>P1 — V1.2 grader-governance ship-blocker (§11.3 R-DS-1 P1); parallel with .077/.079/.080/.081</priority>
  </metadata>

  <references>
    <ref type="prd">docs/architecture/COMP_LEARNS_STAGE3.md §11.1 governance split + §11.3 DS implementation requirements (R-DS-1 P1)</ref>
    <ref type="runner">comp/loop/runner.py — run_pilot(), _run_n_trials(); existing single-output grader path</ref>
    <ref type="ab">comp/bench/ab.py — _grade_response(), run() — exact-match grader location</ref>
    <ref type="rsc2">comp/results/r_sc_2_semantic_labels.md — R-SC-2 label taxonomy consumed by semantic-aware grader</ref>
    <ref type="precedent">comp/results/dev-click-001/scoring_regime_honesty_note.md — exact-match float() failure mode documented</ref>
  </references>

  <objective>
    Implement V1.2 §11.3 grader-governance split in the runner: every judge response now
    yields BOTH exact-match grader output AND semantic-aware grader output. Neither
    overwrites the other. Disagreement flag emitted per response.

    ## Context

    The sphinx pre-screen (.075) revealed that the current exact-match grader masks
    `semantic-correct-but-unparseable` responses as incorrect, producing a false
    Wrong|Wrong signal across 8 of 12 sphinx questions. The grader_artifact pattern is
    target-independent and will recur on every new target unless the runner emits
    sufficient data to distinguish it at runtime.

    V1.2 §11.1 governance split: exact-match remains primary ratchet/champion metric;
    semantic-aware governs pre-screen triage. The runner must emit both so SC can classify
    triage decisions without ad hoc response auditing.

    ## Phase 0 — Read and understand existing grader

    Read the existing _grade_response() in comp/bench/ab.py.
    Understand: float() for numeric, set-split for set_membership, enum match for enumerable.
    The exact-match grader result is currently the only output; semantic-aware is absent.

    ## Phase 1 — Implement semantic-aware secondary grader

    Add a `_semantic_grade_response(response_text: str, entry: dict) -> str` function
    in comp/bench/ab.py returning an R-SC-2 label string:
    - `parseable-correct` — exact-match pass
    - `parseable-wrong` — extracted value present but wrong
    - `semantic-correct-but-unparseable` — correct value present in prose but grader failed
    - `semantic-wrong-unparseable` — grader failed AND prose is semantically wrong
    - `semantic-ambiguous` — cannot determine

    Implementation guidance:
    - For numeric questions: after float() ValueError, apply regex extraction of first
      number from prose (e.g., re.search(r'\b(\d+(?:\.\d+)?)\b', text)). If extracted number
      matches gold → semantic-correct-but-unparseable. If extracted but wrong → semantic-
      wrong-unparseable. If no number found → semantic-ambiguous.
    - For set_membership questions: after set-mismatch, check if gold values appear as
      substrings in prose (case-insensitive). If ALL gold values found in prose → semantic-
      correct-but-unparseable. If SOME → semantic-wrong-unparseable. If none → semantic-
      wrong-unparseable.
    - For enumerable questions: after enum-miss, check if the correct enum value appears
      as a word in prose. If found → semantic-correct-but-unparseable. Else → semantic-
      wrong-unparseable.
    - For answer_type='class_name' or 'registration_call' or 'attribute_value' (sphinx-
      schema types): check substring match of gold_answer in response prose. If match →
      semantic-correct-but-unparseable. Else → semantic-wrong-unparseable.

    This is a heuristic grader, not a perfect judge. The output is for triage guidance,
    not champion selection. Err on the side of semantic-ambiguous when uncertain.

    ## Phase 2 — Dual-output emission in _run_n_trials

    Update comp/loop/runner.py _run_n_trials() to capture both:
    ```python
    exact_pass = _grade_response(resp.text, answer_entry)
    semantic_label = _semantic_grade_response(resp.text, answer_entry)
    disagreement = (exact_pass and semantic_label != 'parseable-correct') or \
                   (not exact_pass and semantic_label == 'parseable-correct')
    ```

    Return an extended structure per trial:
    ```python
    {"exact_pass": bool, "semantic_label": str, "disagreement": bool, "response_text": str}
    ```

    The existing callers of _run_n_trials() that expect list[bool] must be updated to
    handle the new dict structure. run_pilot() is the primary consumer — update pilot
    artifact output to include both grader outputs.

    For the standard ratchet run (not pilot), the primary metric continues to use
    exact_pass. The semantic_label and disagreement_flag are emitted to a sidecar
    per-response, not into the champion scorecard top-level.

    ## Phase 3 — Scorecard and sidecar schema update

    Update comp/bench/scorecard.py to add per-run disagreement summary:
    ```json
    "grader_governance": {
      "exact_match_correct": N,
      "semantic_aware_correct": N,
      "disagreement_count": N,
      "disagreement_rate": 0.NN,
      "schema_version": 1
    }
    ```

    The `grader_governance` block is emitted in the scorecard alongside existing fields.
    It does NOT replace ab_lift, primary_metric, or any existing champion-selection field.

    For the delivered-context sidecar (§6.3, .070), add per question per condition:
    ```json
    "grader_governance": {
      "exact_pass": bool,
      "semantic_label": "...",
      "disagreement": bool
    }
    ```

    ## Phase 4 — Tests

    Add or update tests in comp/bench/tests/ covering:
    1. _semantic_grade_response for each answer_type with semantic-correct-but-unparseable
       cases (verbatim from R-SC-1 evidence: q11 click response should label correctly)
    2. disagreement flag logic (exact_pass=False + semantic_label=parseable-correct → disagreement=True)
    3. grader_governance scorecard block structure

    Run ds-commit-gate.sh on all modified Python files before committing.

    ## Phase 5 — Commit and push

    ```bash
    cd /c/Users/AndrewBerman/Desktop/feature_clb
    .tools/ds-commit-gate.sh comp/bench/ab.py comp/loop/runner.py comp/bench/scorecard.py
    git add comp/bench/ab.py comp/loop/runner.py comp/bench/scorecard.py comp/bench/tests/
    git commit --only \
      --author="1.3.0_DS_CompLearns <1.3.0_DS_CompLearns@opal.agent>" \
      -m "feat(COMP_LEARNS.078): V1.2 grader-governance dual-output -- semantic-aware secondary grader + disagreement rate emission" \
      -- comp/bench/ab.py comp/loop/runner.py comp/bench/scorecard.py comp/bench/tests/
    git push origin CLOUD
    ```

    ## Phase 6 — MCP

    MCP 2.1.0_SA_COO with:
    - Commit sha
    - Confirmation that exact-match primary metric path is unchanged (primary ratchet/champion
      selection uses exact_pass only)
    - Semantic-aware grader answer_type coverage (which types handled)
    - Test count and coverage
    - Any schema decisions that deviate from the TO spec (flag for CTO if so)

    CC 1.1.0_SA_CTO with same content.
  </objective>

  <compiler_tools_mandate>
    <note>Python source changes. Run ds-commit-gate.sh on all edited Python files before commit.
    Gate: python -m py_compile + ds-precommit-check.py + ruff check --target-version py39.
    All three must exit 0. No emojis in code.</note>
  </compiler_tools_mandate>

  <cross_domain_coordination>
    <note>
      Parallel with .077/.079/.080/.081.
      .079 (SC disagreement emission) reads the output format defined here — coordinate if format
      changes are needed. MCP SC if dual-output structure changes from TO spec.
      .070 (sidecar) was authored by 1.3.0_DS — update sidecar schema in the same commit if feasible.
    </note>
  </cross_domain_coordination>

  <acceptance_criteria>
    1. _semantic_grade_response() implemented in comp/bench/ab.py returning R-SC-2 label string.
    2. _run_n_trials() updated to emit both exact_pass and semantic_label per trial.
    3. disagreement flag logic correct per §11.1 governance split definition.
    4. grader_governance block added to scorecard schema.
    5. Exact-match primary metric path unchanged — champion selection uses exact_pass only.
    6. Tests added for semantic grader + disagreement flag.
    7. ds-commit-gate.sh passed on all edited Python files.
    8. Committed --only --author=1.3.0_DS_CompLearns. Pushed CLOUD.
    9. MCP 2.1.0_SA_COO + CC 1.1.0_SA_CTO.
  </acceptance_criteria>

  <dependencies>
    - No upstream gate. Can start immediately.
    - .079 (SC disagreement emission) depends on this TO completing first.
    - .077 (sphinx pilot) is parallel and does not gate or depend on this TO.
  </dependencies>

  <operational_notes>
    - Operate from /c/Users/AndrewBerman/Desktop/feature_clb (COMP_LEARNS worktree).
    - No emojis in code or logs.
    - The semantic-aware grader is heuristic. Document the heuristic explicitly in the function
      docstring so future maintainers understand the precision limits.
    - Do NOT change the primary metric formula or champion selection logic. The governance
      split is additive, not a replacement.
    - from __future__ import annotations on all modified files (PEP-604 compatibility).
  </operational_notes>

  <closeout>
    - flip TO status to complete with commit sha
    - git push origin CLOUD from feature_clb
    - MCP 2.1.0_SA_COO + CC 1.1.0_SA_CTO
    - session log
  </closeout>
</task_order>
