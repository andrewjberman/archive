<task_order>
  <metadata>
    <id>2.1.0_SA_COO-2026-04-27-comp-learns-080-ds-sphinx-answer-key-schema</id>
    <issued_by>2.1.0_SA_COO</issued_by>
    <issued_to>1.1.0_DS_CompLearns</issued_to>
    <date>2026-04-27</date>
    <status>complete</status><!-- covered by .081 -- same deliverable, .081 is authoritative (flat-key schema + provenance file) -->
  </metadata>

  <references>
    <ref type="prd">docs/architecture/COMP_LEARNS_STAGE3.md §12 — Sphinx ab_answer_key.yaml schema gap (R-DS-2 P2)</ref>
    <ref type="cvo_ruling">CVO 20260427T200500Z — sphinx answer-key schema gap kept SEPARATE from grader-governance (V1.2 §11). Orthogonal task.</ref>
    <ref type="prior_ds_work">.074 sphinx question pool (9254655c) — your authoring of ab_questions.yaml + ab_answer_key.yaml under gold_answer schema</ref>
    <ref type="grader_compat">comp/bench/ — _grade_response() expects answer_type/values fields, not gold_answer/gold_source_file</ref>
    <ref type="click_format">comp/targets/click/gold/ab_answer_key.yaml — reference format using answer_type/values</ref>
    <ref type="discovery">SC .075 prescreen surfaced this gap; documented in prescreen_summary.yaml answer_key_schema_note field</ref>
  </references>

  <objective>
    Convert sphinx ab_answer_key.yaml from gold_answer/gold_source_file/gold_source_line schema to the
    answer_type/values schema expected by the standard _grade_response() function. Preserve all
    answer content; reformat schema fields only.

    ## Context

    SC's .075 prescreen execution surfaced that sphinx ab_answer_key.yaml uses a schema you authored in
    .074 that is not directly consumable by the runner's exact-match grader. The grader expects
    answer_type + values fields per click's reference format. This is an orthogonal P2 fix kept separate
    from the V1.2 grader-governance work (per CVO ruling).

    The question pool (ab_questions.yaml) is fine. Only the answer key needs schema conversion.

    ## Phase 0 — Pre-conversion review

    Read both schemas:
    ```bash
    head -30 comp/targets/click/gold/ab_answer_key.yaml      # reference: answer_type + values
    head -30 comp/targets/sphinx/gold/ab_answer_key.yaml     # current: gold_answer + gold_source_file
    ```

    Read the grader function to confirm expected schema:
    ```bash
    grep -n "answer_type\|gold_answer\|values" comp/bench/*.py | head -20
    ```

    Document the exact field names and answer_type values used by click (e.g., `exact`, `set_membership`,
    `numeric`).

    ## Phase 1 — Convert sphinx answer key

    For each entry in `comp/targets/sphinx/gold/ab_answer_key.yaml`, transform:

    **From** (current sphinx schema):
    ```yaml
    answers:
      - id: q01
        gold_answer: "register_directive"
        gold_source_file: "sphinx/util/docutils.py"
        gold_source_line: 142
        verification_note: "register_directive() at line 142 in util/docutils.py"
    ```

    **To** (click-compatible schema):
    ```yaml
    answers:
      - id: q01
        answer_type: exact
        values: ["register_directive"]
        gold_source_file: "sphinx/util/docutils.py"   # PRESERVED for audit
        gold_source_line: 142                          # PRESERVED for audit
        verification_note: "..."                       # PRESERVED for audit
    ```

    Mapping rules:
    - Single-string gold_answer → `answer_type: exact`, `values: ["<string>"]`
    - Class name pair (e.g., q05 expects "DocstringSignatureMixin, ModuleLevelDocumenter") → confirm
      whether grader supports comma-split. If yes: `answer_type: set_membership`, `values: ["DocstringSignatureMixin", "ModuleLevelDocumenter"]`. If no: keep as `exact` with the full string.
    - Numeric gold_answer (none expected for sphinx but check) → `answer_type: numeric`, `values: [<int>]`

    PRESERVE the gold_source_file, gold_source_line, verification_note fields — they are valuable
    audit metadata. The conversion adds answer_type + values; it does NOT delete provenance fields.

    ## Phase 2 — Verify grader compatibility

    For each converted answer, confirm the grader can parse it:

    ```python
    # Sketch: import the grader, run on a synthetic response that should pass
    from comp.bench import _grade_response  # or wherever it lives
    import yaml
    answers = yaml.safe_load(open('comp/targets/sphinx/gold/ab_answer_key.yaml'))['answers']
    for ans in answers:
        # Run grader against the gold answer itself; should pass
        result = _grade_response(ans['values'][0], ans)
        assert result['graded'], f"q{ans['id']} self-grade failed: {result}"
    ```

    If self-grading fails, the schema conversion is incomplete — debug and re-convert that entry.

    ## Phase 3 — YAML validation + commit

    ```bash
    python3 -c "import yaml; yaml.safe_load(open('comp/targets/sphinx/gold/ab_answer_key.yaml'))"
    ```

    Pre-commit gate:
    ```bash
    .tools/ds-commit-gate.sh comp/targets/sphinx/gold/ab_answer_key.yaml 2>&1 || echo "YAML only - py_compile not applicable"
    # Note: ds-commit-gate.sh expects .py; running on .yaml may NOOP. YAML safe_load is the relevant check.
    ```

    No pytest gate required since this is a data file change. But run pytest to confirm no regressions:
    ```bash
    python -m pytest comp/ --ignore=comp/targets -q --tb=no 2>&1 | tail -3
    # 480+ passed, 0 failed.
    ```

    ## Phase 4 — Commit and push

    ```bash
    git commit --only \
      --author="1.1.0_DS_CompLearns <1.1.0_DS_CompLearns@opal.agent>" \
      -m "fix(COMP_LEARNS.080): sphinx ab_answer_key.yaml schema -- gold_answer to answer_type/values (R-DS-2 P2)" \
      -- comp/targets/sphinx/gold/ab_answer_key.yaml
    git push origin CLOUD
    ```

    ## Phase 5 — MCP

    MCP 2.1.0_SA_COO with:
    - Commit sha
    - Conversion summary: 12 answers converted from gold_answer to answer_type/values schema
    - answer_type distribution (e.g., 10 exact + 2 set_membership)
    - Self-grading test pass count (should be 12/12)
    - Confirmation provenance fields (gold_source_file, gold_source_line, verification_note) preserved
  </objective>

  <compiler_tools_mandate>
    <phase id="1" when="before commit">
      <step>
        <run>python3 -c "import yaml; yaml.safe_load(open('comp/targets/sphinx/gold/ab_answer_key.yaml'))"</run>
        <expect>YAML loads without exception.</expect>
        <if_mismatch>STOP. Fix YAML syntax.</if_mismatch>
      </step>
      <step>
        <run>python -m pytest comp/ --ignore=comp/targets -q --tb=no 2>&amp;1 | tail -3</run>
        <expect>480+ passed, 0 failed (no regressions from data file change).</expect>
        <if_mismatch>STOP. Investigate regression.</if_mismatch>
      </step>
    </phase>
  </compiler_tools_mandate>

  <cross_domain_coordination>
    <note>
      Parallel with .077/.078/.079/.081. No dependency on V1.2 grader-governance work.
      Orthogonal P2 task per CVO ruling — kept separate from §11 governance to avoid scope creep.
      Even if sphinx is dropped under Path B target re-selection, this fix is harmless.
    </note>
  </cross_domain_coordination>

  <acceptance_criteria>
    1. comp/targets/sphinx/gold/ab_answer_key.yaml schema converted from gold_answer to answer_type + values.
    2. Provenance fields (gold_source_file, gold_source_line, verification_note) PRESERVED.
    3. 12 entries converted with correct answer_type assignment.
    4. Self-grading test confirms grader parses each entry (12/12 pass).
    5. YAML valid (yaml.safe_load passes).
    6. pytest 480+ baseline, 0 regressions.
    7. Committed --only --author=1.1.0_DS_CompLearns. Pushed to CLOUD.
    8. MCP 2.1.0_SA_COO with commit sha + conversion summary + answer_type distribution.
  </acceptance_criteria>

  <dependencies>
    - No gates. Parallel with all V1.2 governance TOs.
    - Not on Path B critical path (Path B target re-selection gates on V1.2 §10 grader-governance, not on sphinx schema).
  </dependencies>

  <operational_notes>
    - Operate from /c/Users/AndrewBerman/Desktop/feature_clb (COMP_LEARNS worktree).
    - No emojis.
    - YAML data file change only; no Python edits required.
    - If a question's gold_answer cannot be cleanly mapped to answer_type/values (edge case), document
      it in the verification_note field and use answer_type: exact as fallback. Flag such cases in MCP.
    - DO NOT alter ab_questions.yaml (the question pool itself is fine).
    - DO NOT add any V1.2 grader-governance fields to this schema; that is the .077/.078/.079 lane.
  </operational_notes>

  <closeout>
    - flip TO status to complete with commit sha
    - git push origin CLOUD from feature_clb
    - MCP 2.1.0_SA_COO with commit sha + conversion summary
    - session log
  </closeout>
</task_order>
