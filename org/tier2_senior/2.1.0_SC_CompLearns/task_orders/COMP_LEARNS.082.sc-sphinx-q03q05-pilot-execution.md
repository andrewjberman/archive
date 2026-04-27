<task_order>
  <metadata>
    <id>2.1.0_SA_COO-2026-04-27-comp-learns-082-sc-sphinx-q03q05-pilot-execution</id>
    <renumbered_from>081</renumbered_from>
    <renumber_reason>Number collision: 1.1.0_DS_CompLearns authored an independent .081 TO (ds-sphinx-answer-key-schema-fix) which absorbed .080 schema conversion at c5f5c89d. SC pilot renumbered to .082 to avoid ambiguity.</renumber_reason>
    <issued_by>2.1.0_SA_COO</issued_by>
    <issued_to>2.1.0_SC_CompLearns</issued_to>
    <date>2026-04-27</date>
    <status>pending</status>
    <project_code>COMP_LEARNS</project_code>
    <priority>P1 — V1.2 R-COO-1 narrow pilot authorization (parallel with .077/.078/.079)</priority>
  </metadata>

  <references>
    <ref type="prd">docs/architecture/COMP_LEARNS_STAGE3.md §11.4 — Sphinx q03/q05 narrow pilot (V1.2 R-COO-1 authorization)</ref>
    <ref type="prd_scope_cap">§11.4 R-COO-2 P1 binding — pilot scope strictly capped (diagnostic only, no packet, no PATH_B override, no §10 advance)</ref>
    <ref type="cvo_ruling">CVO 20260427T200500Z — q03/q05 pilot authorized under capped scope. CTO V1.2 PRD codification (95f8c0d3 + e3393b26).</ref>
    <ref type="pilot_machinery">.071 (1.2.0_DS commit 710c973e + restore 031b6599) — paired C4+C1 N=8 dual-condition gate; pilot artifact schema; 480 tests green</ref>
    <ref type="prescreen_source">comp/results/sphinx/prescreen/q03_prescreen.yaml + q05_prescreen.yaml (0bb57890) — both labeled full_source_overload_candidate, pilot_eligible=true, semantic-wrong under both regimes</ref>
    <ref type="cto_path_b">Path B target re-selection PAUSED until §11.3 grader-governance ships (.077 + .078 + .079); this pilot runs in parallel</ref>
  </references>

  <objective>
    Run the .071 paired C4+C1 N=8 pilot machinery against sphinx q03 (StandaloneHTMLBuilder — wrong base
    class) and q05 (DocstringSignatureMixin — wrong mixin name). Both are pilot_eligible
    full_source_overload_candidate from .075 prescreen. Diagnostic only — does NOT advance Stage 3
    primary case dispatch (PATH_B_MANDATORY remains binding).

    ## Context

    V1.2 R-COO-1 authorizes this narrow pilot to run in parallel with §11.3 grader-governance work.
    Both q03/q05 are clean from the grader-format question — they are genuine semantic misses (not
    grader_artifact). The pilot tests: "do q03/q05 show any C4-over-C1 lift worth preserving as a
    design signal?"

    PILOT SCOPE CAP (R-COO-2 P1 — binding):
    - The pilot does NOT morph into de facto sphinx continuation
    - The pilot does NOT trigger packet authoring
    - The pilot does NOT override PATH_B_MANDATORY (still binding from .076)
    - The pilot does NOT advance §10 ship-blocker checklist toward primary case dispatch
    - Pilot results are DIAGNOSTIC, not promotion evidence

    ## Phase 0 — Pre-run gates

    Verify pilot machinery functional:
    ```bash
    python -m pytest comp/ --ignore=comp/targets -q --tb=no -k "pilot" 2>&1 | tail -3
    # Expect: 22 pilot decision-rule tests pass.
    ```

    Verify sphinx target ready:
    ```bash
    ls comp/targets/sphinx/gold/ab_questions.yaml comp/targets/sphinx/gold/ab_answer_key.yaml
    grep "id: q03\|id: q05" comp/targets/sphinx/gold/ab_questions.yaml
    ```

    Verify .075 prescreen labels for q03/q05 both pilot_eligible=true:
    ```bash
    grep "pilot_eligible" comp/results/sphinx/prescreen/q03_prescreen.yaml
    grep "pilot_eligible" comp/results/sphinx/prescreen/q05_prescreen.yaml
    # Expect both true
    ```

    ## Phase 1 — Pilot execution

    Run .071 pilot mode for q03 + q05:

    ```bash
    python comp/bin/comp-learns-ratchet sphinx \
      --pilot \
      --questions q03,q05 \
      --judge real \
      --n 8 \
      --compiler-content-sha <sha256[:8] of comp/targets/sphinx/compiler.py>
    ```

    Compute compiler_content_sha:
    ```bash
    python3 -c "import hashlib; print(hashlib.sha256(open('comp/targets/sphinx/compiler.py','rb').read()).hexdigest()[:8])"
    ```

    Pilot execution:
    - 8 C4 trials per question (full two-step: background_index=True, addressing=mechanical, full compiler expansion)
    - 8 C1 trials per question (unaided: no compiler context)
    - 16 total trials per question = 32 trials total
    - ANTHROPIC_API_KEY required for --judge real
    - Cost: ~32 API calls cold (cache may warm if runs repeat)

    Note: V1.2 grader-governance has not shipped yet (.077 + .078 + .079 in flight). This pilot scores
    under exact-match grader. Best-effort manual semantic audit of judge responses is acceptable when
    interpreting results — note any semantic-correct-but-unparseable cases in the MCP.

    Sphinx ab_answer_key.yaml schema gap (.080 in flight): if grader fails on q03/q05 due to
    answer_type field absence, you may either (a) wait for .080 to ship and re-run, or (b) use a
    temporary local answer_type/values mapping for q03/q05 only and flag in MCP.

    ## Phase 2 — Decision rule application

    Per .071 dual-condition gate (PRD §5.2 V1.1 corrected rule):
    - PROMOTE: C4 ≥ 5/8 AND (C4 - C1) ≥ 2 → would-be-INCLUDE if Path A were viable
    - DEMOTE_CEILING: C4 ≤ 1/8 → genuine ceiling
    - DEMOTE_PRIOR_DOMINATED: C1 ≥ 6/8 AND (C4 - C1) ≤ 0 → solvable unaided
    - HOLD: otherwise → insufficient signal

    NOTE — DIAGNOSTIC INTERPRETATION (V1.2 R-COO-2):
    Per V1.2 §11.4, even a PROMOTE outcome on q03/q05 does NOT advance Stage 3 dispatch toward sphinx
    primary case. The PATH_B_MANDATORY ruling (38d00105) is preserved. PROMOTE → "design signal worth
    preserving for future Path B target similarity criteria." DEMOTE → "compiler context did not aid
    this class of structural question." Both outcomes are diagnostic.

    ## Phase 3 — Pilot artifact emission

    .071 emits per-question artifacts to:
    ```
    comp/results/sphinx/pilot/<run_timestamp>/pilot_q03.json
    comp/results/sphinx/pilot/<run_timestamp>/pilot_q05.json
    comp/results/sphinx/pilot/<run_timestamp>/pilot_summary.json
    ```

    Verify artifacts written:
    ```bash
    ls comp/results/sphinx/pilot/*/pilot_*.json
    python3 -c "import json,glob; a=json.load(open(sorted(glob.glob('comp/results/sphinx/pilot/*/pilot_summary.json'))[-1])); print(a)"
    ```

    ## Phase 4 — Diagnostic memo

    Author a brief memo at:
    ```
    comp/results/sphinx/pilot/<run_timestamp>/pilot_memo.md
    ```

    Cover:
    - q03 result: C4 successes / C1 successes / delta / decision
    - q05 result: same fields
    - Any judge response notes (especially any that look semantic-correct-but-unparseable under exact-match)
    - Diagnostic interpretation: does compiler context aid this question class?
    - Explicit confirmation: this pilot does NOT alter PATH_B_MANDATORY ruling

    ## Phase 5 — Commit and push

    ```bash
    git commit --only \
      --author="2.1.0_SC_CompLearns <2.1.0_SC_CompLearns@opal.agent>" \
      -m "score(COMP_LEARNS.081): sphinx q03/q05 narrow pilot -- diagnostic [q03_DECISION + q05_DECISION]" \
      -- comp/results/sphinx/pilot/
    git push origin CLOUD
    ```

    Replace q03_DECISION + q05_DECISION with PROMOTE / DEMOTE_CEILING / DEMOTE_PRIOR_DOMINATED / HOLD.

    ## Phase 6 — MCP

    MCP 2.1.0_SA_COO + CC 1.1.0_SA_CTO with:
    - Commit sha
    - q03 + q05 per-question results (C4 + C1 success counts, delta, decision)
    - Diagnostic interpretation (does compiler context help this question class?)
    - Any semantic-correct-but-unparseable cases noted in judge responses
    - Explicit confirmation: PATH_B_MANDATORY unchanged; pilot is diagnostic only
    - .080 schema gap status (whether you used .080 or temporary local mapping)
  </objective>

  <compiler_tools_mandate>
    <phase id="1" when="before run">
      <step>
        <run>python -m pytest comp/ --ignore=comp/targets -q --tb=no -k "pilot" 2>&amp;1 | tail -3</run>
        <expect>22 pilot decision-rule tests pass.</expect>
        <if_mismatch>STOP. Pilot machinery may have regressed; MCP COO.</if_mismatch>
      </step>
      <step>
        <run>grep "pilot_eligible" comp/results/sphinx/prescreen/q03_prescreen.yaml comp/results/sphinx/prescreen/q05_prescreen.yaml</run>
        <expect>Both q03 and q05 show pilot_eligible: true.</expect>
        <if_mismatch>STOP. Prescreen state changed; verify before running.</if_mismatch>
      </step>
    </phase>
    <phase id="2" when="after run">
      <step>
        <run>ls comp/results/sphinx/pilot/*/pilot_summary.json</run>
        <expect>pilot_summary.json present.</expect>
        <if_mismatch>Pilot artifact emission failed; investigate.</if_mismatch>
      </step>
    </phase>
  </compiler_tools_mandate>

  <cross_domain_coordination>
    <note>
      Parallel with .077/.078/.079/.080. No shared artifact writes (sphinx pilot dir is new).
      Sphinx ab_answer_key.yaml schema gap (.080 in flight): if grader fails on q03/q05, wait for .080 OR use local mapping (flag in MCP).
      Pilot result does NOT advance §10 ship-blocker. Path B target re-selection still pending §11.3 grader-governance ship.
    </note>
  </cross_domain_coordination>

  <acceptance_criteria>
    1. .071 pilot machinery confirmed functional (22 tests pass).
    2. q03 and q05 prescreen state confirmed pilot_eligible=true.
    3. Pilot run executed: 8 C4 + 8 C1 trials per question (32 total trials).
    4. Pilot artifacts written to comp/results/sphinx/pilot/&lt;timestamp&gt;/ (per-Q + summary + memo).
    5. Decision rule applied per .071 thresholds; both questions assigned PROMOTE / DEMOTE_CEILING / DEMOTE_PRIOR_DOMINATED / HOLD.
    6. Diagnostic memo authored with explicit PATH_B_MANDATORY-preserved statement.
    7. Committed --only --author=2.1.0_SC_CompLearns. Pushed to CLOUD.
    8. MCP 2.1.0_SA_COO + CC 1.1.0_SA_CTO with commit sha + per-Q results + diagnostic interpretation.
  </acceptance_criteria>

  <dependencies>
    - No gates. Parallel with .077/.078/.079/.080.
    - Pilot artifact does NOT advance Stage 3 §10 ship-blocker (per V1.2 R-COO-2 scope cap).
    - Sphinx ab_answer_key.yaml schema gap may delay if .080 not ready when running.
  </dependencies>

  <operational_notes>
    - Operate from /c/Users/AndrewBerman/Desktop/feature_clb (COMP_LEARNS worktree).
    - No emojis.
    - ANTHROPIC_API_KEY required for --judge real. Cost: ~32 API calls cold, less if cache warm.
    - This is a non-ratchet pilot. Does NOT update champion.json. Does NOT append to experiment_log.jsonl.
    - The result is DIAGNOSTIC. PATH_B_MANDATORY ruling stays binding regardless of pilot outcome.
    - Manual semantic audit of judge responses is acceptable when V1.2 dual-grader hasn't shipped (.077 in flight). Note any semantic-correct-but-unparseable observations.
  </operational_notes>

  <closeout>
    - flip TO status to complete with commit sha
    - git push origin CLOUD from feature_clb
    - MCP 2.1.0_SA_COO + CC 1.1.0_SA_CTO with diagnostic results
    - session log
  </closeout>
</task_order>
