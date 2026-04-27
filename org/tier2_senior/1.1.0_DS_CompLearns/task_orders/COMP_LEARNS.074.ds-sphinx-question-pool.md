<task_order>
  <metadata>
    <id>2.1.0_SA_COO-2026-04-27-comp-learns-074-ds-sphinx-question-pool</id>
    <issued_by>2.1.0_SA_COO</issued_by>
    <issued_to>1.1.0_DS_CompLearns</issued_to>
    <date>2026-04-27</date>
    <status>complete</status>
    <project_code>COMP_LEARNS</project_code>
    <priority>P0 — Stage 3 prerequisite: sphinx pre-screen cannot run without question pool (parallel with .070/.071/.072/.073)</priority>
  </metadata>

  <references>
    <ref type="prd">docs/architecture/COMP_LEARNS_STAGE3.md §7 — Target selection: sphinx Path A default</ref>
    <ref type="prd_section">§2 — Pre-screen triage matrix; §7.1 — Sphinx selection rationale (65k LOC, cross-module API, extension hooks far from fix sites)</ref>
    <ref type="sphinx_target">comp/targets/sphinx/ — compiler v0 (imports-only), repo_pin=36367765, ab_questions.yaml currently empty</ref>
    <ref type="sphinx_harness">.046 sphinx harness v0 (1.2.0_DS, Wave 3b) — harness setup validated; runner wired</ref>
    <ref type="click_question_format">comp/targets/click/gold/ab_questions.yaml + ab_answer_key.yaml — reference format for question pool structure</ref>
    <ref type="pre_screen_consumer">.075 (SC sphinx pre-screen execution) gates on this TO; .076 (CTO off-ramp gate) gates on .075</ref>
  </references>

  <objective>
    Author the sphinx candidate question pool: populate comp/targets/sphinx/gold/ab_questions.yaml and
    ab_answer_key.yaml with >= 10 questions that give the Stage 3 pre-screen meaningful room to partition
    into INCLUDE / SENTINEL / INVESTIGATE.

    ## Context

    The sphinx target has a compiler v0 (imports-only) and an empty question bank. Stage 3's pre-screen
    requires a candidate question pool before SC can run zero-shot and full-source scoring. The questions
    must be authored with the Stage 3 measurement objective in mind: questions where the parametric prior
    MIGHT dominate (so the pre-screen can detect SENTINEL cases honestly) AND questions where cross-module
    structural navigation is the difference-maker (INCLUDE cases). The goal is a pool that the pre-screen
    can legitimately partition — not a pool optimized for high INCLUDE count.

    ## Phase 0 — Pre-authoring review

    Read the sphinx target's repo structure to understand the codebase:
    ```bash
    ls comp/targets/sphinx/_repo/
    # Note: repo is at the pinned commit 36367765
    ```

    Read the current compiler v0:
    ```bash
    cat comp/targets/sphinx/compiler.py
    ```

    Read the click question format as reference:
    ```bash
    cat comp/targets/click/gold/ab_questions.yaml
    cat comp/targets/click/gold/ab_answer_key.yaml
    ```

    Note: sphinx is a documentation generator with extension/plugin API. Key architectural
    areas that produce measurement-room questions:
    - Extension loading and configuration (complex cross-module setup chain)
    - Directive class hierarchy (directives registered via add_directive; resolution path non-trivial)
    - Builder/environment relationship (inheritance and protocol implementation)
    - Domain registration and object description (cross-module role/directive registration)
    - Autodoc extension (introspection + docstring extraction pipeline)

    ## Phase 1 — Author >= 10 candidate questions

    Author questions following these constraints:

    **Measurement-room constraint (most important):**
    Each question must have a PLAUSIBLE ANSWER that a smart ML model might give without looking at the
    code (pre-training parametric knowledge), AND a CORRECT ANSWER that requires inspecting the specific
    sphinx codebase at the pinned commit. If the parametric answer IS the correct answer for a typical
    sphinx version, the question will land in SENTINEL. That is acceptable — the pre-screen is supposed
    to find those.

    **Coverage constraint:**
    Include questions across at least 3 of the following types:
    1. Cross-module inheritance chain questions (e.g., "what class does X inherit from" — where the
       answer is non-obvious from docs alone)
    2. Method resolution questions (e.g., "which class first defines method Y in the sphinx.ext.X
       hierarchy")
    3. Configuration/attribute source questions (e.g., "where is attribute Z first assigned in the
       builder setup chain")
    4. Registration mechanism questions (e.g., "how does directive D get registered — what call, in
       which module, invoked from where")
    5. Extension hook questions (e.g., "what event does extension E connect to, and in which file")

    **Answer quality constraint:**
    - Answers must be definitively verifiable from the pinned commit source code
    - Each answer must be a short, specific string (a class name, method name, module path, or
      one-line description) — NOT a multi-sentence explanation
    - Avoid questions where the "correct" answer is trivially in the sphinx documentation or
      widely cited in Stack Overflow (high prior-dominance risk)

    **Format (match click style):**
    ab_questions.yaml:
    ```yaml
    questions:
      - id: q01
        text: "<question text>"
        expected_answer_type: class_name | method_name | module_path | attribute_value | registration_call
        difficulty: low | medium | high
        cross_module: true | false
        note: "<optional: why this question has measurement room>"
      - id: q02
        ...
    ```

    ab_answer_key.yaml:
    ```yaml
    answers:
      - id: q01
        gold_answer: "<exact expected answer string>"
        gold_source_file: "<path/relative/to/sphinx/root>"
        gold_source_line: <line number>
        verification_note: "<one-line: how to verify from source>"
      - id: q02
        ...
    ```

    Aim for:
    - >= 5 cross_module: true questions (these are the Stage 3 measurement core)
    - >= 3 high-difficulty questions (test the pre-screen's ability to find INCLUDE cases)
    - >= 2 low-difficulty or well-documented questions (test the pre-screen's ability to find SENTINEL)

    ## Phase 2 — Verification pass

    For each question, verify the gold answer against the pinned commit source:
    ```bash
    cd comp/targets/sphinx/_repo
    git checkout 36367765  # or verify already at this commit
    # Search the source to confirm each gold answer
    grep -rn "<gold_answer>" --include="*.py" | head -5
    ```

    All gold answers must be verifiable from source. Any question where you cannot confirm the gold
    answer from the pinned commit must be dropped or revised.

    ## Phase 3 — Pre-commit gate

    No Python files are modified. No ds-commit-gate.sh required. Verify YAML is well-formed:
    ```bash
    python3 -c "import yaml; yaml.safe_load(open('comp/targets/sphinx/gold/ab_questions.yaml'))"
    python3 -c "import yaml; yaml.safe_load(open('comp/targets/sphinx/gold/ab_answer_key.yaml'))"
    ```
    Both must load without error.

    ## Phase 4 — Commit and push

    ```bash
    git add comp/targets/sphinx/gold/ab_questions.yaml \
            comp/targets/sphinx/gold/ab_answer_key.yaml
    git commit --only \
      --author="1.1.0_DS_CompLearns <1.1.0_DS_CompLearns@opal.agent>" \
      -m "feat(COMP_LEARNS.074): sphinx question pool -- N questions, cross-module focus (Stage 3 pre-screen input)" \
      -- comp/targets/sphinx/gold/ab_questions.yaml \
         comp/targets/sphinx/gold/ab_answer_key.yaml
    git push origin CLOUD
    ```

    Replace N in the commit message with the actual question count.

    ## Phase 5 — MCP

    MCP 2.1.0_SA_COO with:
    - Commit sha
    - Question count (total + cross_module count + difficulty breakdown)
    - Coverage types covered (from the 5 types in Phase 1)
    - Any questions where measurement room was uncertain (flag for pre-screen to watch)
    - YAML validation confirmed (both files load without error)
  </objective>

  <compiler_tools_mandate>
    <note>This TO modifies YAML files only. Run python3 yaml.safe_load validation before commit.
    No ds-commit-gate.sh required (no Python source changes).</note>
  </compiler_tools_mandate>

  <cross_domain_coordination>
    <note>
      Parallel with .070/.071/.072/.073.
      .075 (SC sphinx pre-screen execution) gates on this TO complete.
      SC will run zero-shot + full-source scoring for each question authored here.
      Do NOT pre-score or pre-triage questions in this TO — that is SC's work in .075.
    </note>
  </cross_domain_coordination>

  <acceptance_criteria>
    1. comp/targets/sphinx/gold/ab_questions.yaml populated with >= 10 questions (IDs q01-qNN).
    2. comp/targets/sphinx/gold/ab_answer_key.yaml populated with gold answers for all questions.
    3. Each answer verified from pinned commit source (36367765).
    4. >= 5 cross_module: true questions.
    5. Coverage spans >= 3 of the 5 question types listed in Phase 1.
    6. YAML valid (python3 yaml.safe_load passes for both files).
    7. Committed --only --author=1.1.0_DS_CompLearns. Pushed to CLOUD.
    8. MCP 2.1.0_SA_COO with commit sha + question count + coverage breakdown.
  </acceptance_criteria>

  <dependencies>
    - No gates. Parallelizable with .070/.071/.072/.073.
    - .075 (sphinx pre-screen execution) gates on this TO complete.
  </dependencies>

  <operational_notes>
    - Operate from /c/Users/AndrewBerman/Desktop/feature_clb (COMP_LEARNS worktree).
    - No emojis.
    - DO NOT pre-triage or predict INCLUDE/SENTINEL/INVESTIGATE in this TO — that is SC's job in .075.
    - DO NOT modify compiler.py or runner.py — this TO is question authoring only.
    - The sphinx repo is at comp/targets/sphinx/_repo/ at the pinned commit. Verify you are at the
      pinned commit before searching source.
    - If the _repo directory is empty or the pinned commit is not checked out, check the runner config
      or .046 harness setup for how the repo is provisioned.
    - aim for measurability, not difficulty. Questions that look hard but are in sphinx's README are
      SENTINEL; questions that look easy but require following a 3-hop import chain are INCLUDE.
      Write a mix of both deliberately.
  </operational_notes>

  <closeout>
    - flip TO status to complete with commit sha
    - git push origin CLOUD from feature_clb
    - MCP 2.1.0_SA_COO with commit sha + question count + coverage breakdown
    - session log
  </closeout>
</task_order>
