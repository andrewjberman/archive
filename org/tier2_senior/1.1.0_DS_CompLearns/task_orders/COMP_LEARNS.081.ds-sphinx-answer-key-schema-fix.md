<task_order>
  <metadata>
    <id>2.1.0_SA_COO-2026-04-27-comp-learns-081-ds-sphinx-answer-key-schema-fix</id>
    <issued_by>2.1.0_SA_COO</issued_by>
    <issued_to>1.1.0_DS_CompLearns</issued_to>
    <date>2026-04-27</date>
    <status>pending</status>
    <project_code>COMP_LEARNS</project_code>
    <priority>P2 — orthogonal to grader-governance; required before any sphinx scoring; parallel with .077/.078/.079/.080</priority>
  </metadata>

  <references>
    <ref type="prd">docs/architecture/COMP_LEARNS_STAGE3.md §12: "Sphinx ab_answer_key.yaml schema gap — gold_answer/gold_source_file schema incompatible with _grade_response(); DS schema-conversion task (R-DS-2 P2)"</ref>
    <ref type="finding">.075 SC prescreen run_prescreen.py — custom grader required because load_answer_key() returns gold_answer schema incompatible with _grade_response()</ref>
    <ref type="gold_dir">comp/targets/sphinx/gold/ab_answer_key.yaml — current incompatible schema (gold_answer / gold_source_file)</ref>
    <ref type="grader">comp/bench/ab.py _grade_response() — requires answer_type + values/value/tolerance fields per click schema</ref>
    <ref type="precedent">comp/targets/click/gold/ab_answer_key.yaml — correct schema reference (pool, answer_type, values/value/tolerance)</ref>
    <ref type="validator">comp/bench/ab_answer_key_validator.py — raises RatchetPoolOpenEndedRejected if answer_type is not {enumerable, set_membership, numeric}</ref>
  </references>

  <objective>
    Convert comp/targets/sphinx/gold/ab_answer_key.yaml from the gold_answer/gold_source_file
    schema to the standard answer_type/values schema required by _grade_response() and the
    ratchet runner. Under the current schema, ALL sphinx questions grade False in the standard
    runner (load_answer_key returns a list under 'answers' key; _grade_response gets an empty
    entry dict and falls through to return False).

    ## Context

    The sphinx answer key was authored in .074 (1.1.0_DS_CompLearns) using a narrative schema
    (gold_answer, gold_source_file, gold_source_line, verification_note). This schema is human-
    readable but not machine-gradeable. The SC prescreen (.075) detected this gap and wrote a
    custom grader. For primary scoring to work, the canonical schema is required.

    ## Phase 0 — Read existing files

    Read comp/targets/sphinx/gold/ab_answer_key.yaml (current schema).
    Read comp/targets/click/gold/ab_answer_key.yaml (reference schema).
    Read comp/bench/ab.py load_answer_key() to understand what structure _grade_response() expects.

    ## Phase 1 — Determine answer_type for each question

    The 12 sphinx questions span three answer types. Assign answer_type per question:

    | QID | Gold answer | answer_type | values / value field |
    |-----|-------------|-------------|----------------------|
    | q01 | register_directive | enumerable | values: [register_directive] |
    | q02 | directives.register_directive | enumerable | values: [directives.register_directive] |
    | q03 | StandaloneHTMLBuilder | enumerable | values: [StandaloneHTMLBuilder] |
    | q04 | ClassDocumenter | enumerable | values: [ClassDocumenter] |
    | q05 | DocstringSignatureMixin, ModuleLevelDocumenter | set_membership | values: [DocstringSignatureMixin, ModuleLevelDocumenter] |
    | q06 | none | enumerable | values: [none] |
    | q07 | I18nBuilder | enumerable | values: [I18nBuilder] |
    | q08 | doctree-resolved | enumerable | values: [doctree-resolved] |
    | q09 | doctree-read | enumerable | values: [doctree-read] |
    | q10 | Directive | enumerable | values: [Directive] |
    | q11 | setup | enumerable | values: [setup] |
    | q12 | BaseAdmonition | enumerable | values: [BaseAdmonition] |

    NOTE on enumerable vs set_membership:
    - enumerable: answer must exactly equal one value (case/whitespace normalized)
    - set_membership: answer parsed as comma-delimited set, must equal gold set unordered
    - q05 is set_membership (two base classes; order may vary)
    - All others are enumerable (single expected value)

    NOTE on grader case-sensitivity: _grade_response enumerable branch uses
    text.lower().strip() in values (lowercased). Verify your values match the gold lowercased.
    For class names and function names: exact canonical case in values is preserved; grader
    normalizes both sides to lowercase for comparison.

    ## Phase 2 — Rewrite ab_answer_key.yaml

    Rewrite in the canonical flat-key format (matching click precedent):

    ```yaml
    # COMP_LEARNS sphinx A/B answer key
    # Target: sphinx-doc/sphinx, pinned commit 36367765fe780f962bba861bf368a765380bbc68
    # Authored: 2026-04-27 by 1.1.0_DS_CompLearns under COMP_LEARNS.074 (original) /
    #           COMP_LEARNS.081 (schema conversion)
    # Gold-before-code: all answers hand-verified from source at pinned commit.
    # Schema: canonical answer_type/values per _grade_response() contract.

    q01:
      pool: ratchet_critical
      answer_type: enumerable
      values:
        - "register_directive"

    q02:
      pool: ratchet_critical
      answer_type: enumerable
      values:
        - "directives.register_directive"

    ... (all 12 questions)
    ```

    Keep the gold_source_file and verification_note information in a separate companion file:
    comp/targets/sphinx/gold/ab_answer_key_provenance.yaml (new file). This preserves the
    source-verification audit trail without polluting the grader-facing schema.

    ## Phase 3 — Validate with ab_answer_key_validator.py

    ```bash
    cd /c/Users/AndrewBerman/Desktop/feature_clb
    python3 -c "
    import yaml
    from pathlib import Path
    ak = yaml.safe_load(Path('comp/targets/sphinx/gold/ab_answer_key.yaml').read_text())
    print('keys:', list(ak.keys())[:5])
    print('q01:', ak.get('q01'))
    print('q05:', ak.get('q05'))
    "
    ```
    Confirm: top-level keys are q01-q12, each has answer_type and values.

    If ab_answer_key_validator.py exists and accepts a target argument:
    ```bash
    python3 comp/bench/ab_answer_key_validator.py sphinx
    ```

    Also verify _grade_response works for a sphinx question:
    ```bash
    python3 -c "
    from comp.bench.ab import _grade_response, load_answer_key
    from pathlib import Path
    ak = load_answer_key(Path('comp/targets/sphinx/gold/ab_answer_key.yaml'))
    print('q01 entry:', ak.get('q01'))
    print('grade test:', _grade_response('register_directive', ak['q01']))  # should be True
    print('grade test2:', _grade_response('Register_Directive', ak['q01'])) # should be True (normalized)
    print('grade test3:', _grade_response('wrong_answer', ak['q01']))       # should be False
    "
    ```

    ## Phase 4 — Commit and push

    ```bash
    git add comp/targets/sphinx/gold/ab_answer_key.yaml \
            comp/targets/sphinx/gold/ab_answer_key_provenance.yaml
    git commit --only \
      --author="1.1.0_DS_CompLearns <1.1.0_DS_CompLearns@opal.agent>" \
      -m "fix(COMP_LEARNS.081): sphinx ab_answer_key schema conversion -- gold_answer->answer_type/values (R-DS-2 P2)" \
      -- comp/targets/sphinx/gold/ab_answer_key.yaml \
         comp/targets/sphinx/gold/ab_answer_key_provenance.yaml
    git push origin CLOUD
    ```

    ## Phase 5 — MCP

    MCP 2.1.0_SA_COO with:
    - Commit sha
    - Confirmation that _grade_response() returns True for all 12 correct answers
    - Confirmation that q05 (set_membership) parses correctly for "DocstringSignatureMixin,
      ModuleLevelDocumenter" and "ModuleLevelDocumenter, DocstringSignatureMixin" (order-
      independent)
    - Whether any answer_type assignment deviated from the TO spec (flag for SC review if so)
  </objective>

  <compiler_tools_mandate>
    <note>YAML file edit only (no Python changes). ds-commit-gate.sh not required.
    However, run the python3 validation commands in Phase 3 to verify grader compatibility
    before committing — a silent schema mismatch would cause all sphinx questions to grade False.</note>
  </compiler_tools_mandate>

  <cross_domain_coordination>
    <note>
      Parallel with .077/.078/.079/.080 — no shared artifacts.
      SC (.075 prescreen) used a custom grader to work around this gap. After this TO,
      the prescreen run_prescreen.py script should be updated to use load_answer_key() +
      _grade_response() for consistency (minor follow-on; not a gate for this TO).
      If Path B activates, this fix is moot for sphinx primary scoring — but sphinx may
      serve as a shakedown target later, so the fix is still warranted.
    </note>
  </cross_domain_coordination>

  <acceptance_criteria>
    1. ab_answer_key.yaml rewritten in canonical flat-key schema (q01-q12 top-level keys).
    2. Each entry has pool, answer_type, values (or value+tolerance for numeric).
    3. q05 assigned set_membership with two values.
    4. All others assigned enumerable with single value.
    5. _grade_response() returns True for all 12 correct gold answers (verified in Phase 3).
    6. ab_answer_key_provenance.yaml created with source audit trail.
    7. Committed --only --author=1.1.0_DS_CompLearns. Pushed CLOUD.
    8. MCP 2.1.0_SA_COO with validation confirmation.
  </acceptance_criteria>

  <dependencies>
    - No upstream gate. Can start immediately.
    - Independent of .077/.078/.079/.080.
  </dependencies>

  <operational_notes>
    - Operate from /c/Users/AndrewBerman/Desktop/feature_clb (COMP_LEARNS worktree).
    - No emojis.
    - The values list in enumerable entries is case-preserved but grader normalizes to lowercase
      for comparison. Use exact canonical case from gold_answer as the values entry.
    - Do NOT change the question text in ab_questions.yaml — only the answer key changes.
    - If ab_answer_key_validator.py raises RatchetPoolOpenEndedRejected: review the answer_type
      assignment; the validator requires {enumerable, set_membership, numeric} for ratchet_critical.
  </operational_notes>

  <closeout>
    - flip TO status to complete with commit sha
    - git push origin CLOUD
    - MCP 2.1.0_SA_COO
    - session log
  </closeout>
</task_order>
