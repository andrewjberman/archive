<task_order>
  <metadata>
    <id>2.1.0_SC_CompLearns-2026-04-24-comp-learns-059-case2-two-phase-scoring</id>
    <issued_by>2.1.0_SA_COO</issued_by>
    <issued_to>2.1.0_SC_CompLearns</issued_to>
    <date>2026-04-24</date>
    <status>complete <!-- Phase 1 freeze: 290bd61f; Phase 2 ship: 2d2337fb; pushed CLOUD --></status>
    <project_code>COMP_LEARNS</project_code>
    <priority>P0 — Wave 3b Lane B, Case 2 formal scoring verdict</priority>
  </metadata>

  <references>
    <ref type="prd">docs/architecture/COMP_LEARNS_WAVE3_V1.md §3.5 + §3.6 + §3.7 + §7 — bd84ef10</ref>
    <ref type="packet">comp/tasks/case-002-click-refactor/packet.yaml — authoritative ACs</ref>
    <ref type="pair_inputs">.056 bundle (1.3.0_DS condition_a unaided) + .057 bundle (1.4.0_DS condition_b aided)</ref>
    <ref type="wave3b_decision">COMP_LEARNS.WAVE3B-DECISION.md §3 — confidence_note field required</ref>
    <ref type="precedent">.058 (Case 1 scoring this wave) — same model; append to wave-3b artifacts</ref>
  </references>

  <objective>
    Score Case 2 via the two-phase model. Same discipline as .058 / .051. Sequenced after
    .058 MCP COMPLETE lands to COO (single SC agent — sequential).

    ## Phase 1 — Verdict (reasoning.md EXCLUDED)

    1. For each condition:
       - ds-1.3.0-condition_a (unaided): comp/tasks/case-002-click-refactor/bundles/ds-1.3.0-condition_a/
       - ds-1.4.0-condition_b (aided): comp/tasks/case-002-click-refactor/bundles/ds-1.4.0-condition_b/
       Read ONLY: changes.patch + test_output.txt.

    2. Evaluate task correctness per packet.yaml acceptance_criteria:
       - ac-1: pytest tests/ -q (no regressions)
       - ac-2: pytest tests/ -q -k 'group or nested or subcommand' (_protected_args + nested)
       - ac-3: pytest tests/ -q -k 'option or param or decorator' (decorator accumulation)
       - ac-4: pytest tests/ -q -k 'invoke or result_callback or chain' (invoke_without_command + result_callback)
       - ac-5: pytest tests/ -q -k 'help or version or eager' (eager param ordering)
       Infer PASS/FAIL from test_output.txt.

    3. Emit Phase 1 verdict per condition:
       comp/results/wave-3b/verdicts/case-002-ds-1.3.0-condition_a-run-1.json
       comp/results/wave-3b/verdicts/case-002-ds-1.4.0-condition_b-run-1.json

       Schema (mirror case-001 verdicts from .058):
       ```json
       {
         "packet_id": "case-002-click-refactor",
         "agent": "1.3.0_DS_CompLearns",
         "condition": "condition_a",
         "run": 1,
         "verdict": "PASS|FAIL",
         "ac_results": {"ac-1":"PASS|FAIL","ac-2":"PASS|FAIL","ac-3":"PASS|FAIL","ac-4":"PASS|FAIL","ac-5":"PASS|FAIL"},
         "judge_model_id": "claude-sonnet-4-6",
         "scored_by": "2.1.0_SC_CompLearns",
         "scored_at": "<ISO8601>",
         "phase": 1,
         "prior_exposure_note": "<copy from bundle reasoning.md prior_exposure field>",
         "notes": "<neutral observations; NO reasoning.md content>"
       }
       ```

    4. Commit Phase 1 verdicts. FREEZE before Phase 2.

    ## Phase 2 — Metric audit (nav_log.jsonl input)

    5. For each bundle, read nav_log.jsonl:
       - comp/tasks/case-002-click-refactor/bundles/ds-1.3.0-condition_a/nav_log.jsonl
       - comp/tasks/case-002-click-refactor/bundles/ds-1.4.0-condition_b/nav_log.jsonl

    6. Extract per-condition metrics:
       - Wall-clock to first correct hypothesis
       - Token usage to first correct hypothesis
       - Files touched before decisive file (decisive file set: src/click/core.py + src/click/decorators.py)
       - Irrelevant files touched (not in decisive set)
       - comp_call count (0 for unaided; >0 for aided)

    7. Compute deltas (condition_b minus condition_a).

    8. Noise checks (same as .058):
       - 0 comp_calls in condition_b → flag
       - Identical nav_log sequences → flag
       - >3x implausible wall-clock/token → flag

    9. Confound check:
       - condition_a (1.3.0_DS) prior_exposure = "pilot-wave-1 case-002, separate session" — document.

    10. Add confidence_note field (per CTO Wave 3b decision):
        Read reasoning.md in Phase 2 (after verdict freeze) to assess aided vs unaided agent
        confidence at hypothesis formation. Subjective assessment from reasoning.md is acceptable.

    11. Emit Phase 2 metric-audit file:
        comp/results/wave-3b/metric_audit/case-002-efficiency-delta.json
        (same schema as case-001-efficiency-delta.json, adapted for Case 2 fields)

    12. Append to comp/results/wave-3b/integrity_audit.md:
        Add Case 2 section: Phase 1→2 ordering confirmed, reasoning.md exclusion in Phase 1,
        nav_log hygiene, no cross-condition contamination.

    13. MCP COMPLETE to 2.1.0_SA_COO with:
        - Case 2 verdict per condition (PASS/FAIL)
        - Efficiency delta one-liner
        - noise_flags if any
        - Brief note on whether aided vs unaided showed any confidence difference (from confidence_note)

    Explicitly out of scope:
    - Case 1 scoring — already done in .058
    - Revisiting Phase 1 verdict in Phase 2
  </objective>

  <compiler_tools_mandate>
    <phase id="1" when="before Phase 1 scoring">
      <step>
        <run>ls comp/tasks/case-002-click-refactor/bundles/ds-1.3.0-condition_a/ &amp;&amp; ls comp/tasks/case-002-click-refactor/bundles/ds-1.4.0-condition_b/</run>
        <expect>Both bundle directories exist with changes.patch + test_output.txt + reasoning.md + nav_log.jsonl</expect>
        <if_mismatch>STOP. .056 or .057 not yet shipped. MCP COO.</if_mismatch>
      </step>
    </phase>
    <phase id="2" when="before Phase 2 (after Phase 1 commit)">
      <step>
        <run>ls comp/results/wave-3b/verdicts/ | grep case-002</run>
        <expect>Both case-002 verdict files present and committed</expect>
        <if_mismatch>Complete + commit Phase 1 first.</if_mismatch>
      </step>
      <step>
        <run>python -c "import json; rows=[json.loads(l) for l in open('comp/tasks/case-002-click-refactor/bundles/ds-1.4.0-condition_b/nav_log.jsonl')]; cc=sum(1 for r in rows if r['event']=='comp_call'); print(f'aided comp_calls: {cc}')"</run>
        <expect>aided comp_calls: 1 or more</expect>
        <if_mismatch>Flag noise. Document in noise_flags. MCP COO before proceeding.</if_mismatch>
      </step>
    </phase>
    <phase id="3" when="after commit">
      <step>
        <run>ls comp/results/wave-3b/</run>
        <expect>verdicts/ (4 files total: 2 from .058 + 2 from .059) + metric_audit/ (2 files) + integrity_audit.md</expect>
        <if_mismatch>Author missing artifacts.</if_mismatch>
      </step>
    </phase>
  </compiler_tools_mandate>

  <cross_domain_coordination>
    <note>Sequenced after .058 (Case 1 scoring) MCP COMPLETE. Both wave-3b scoring TOs share comp/results/wave-3b/ directory. Append to integrity_audit.md (do not overwrite .058 Case 1 section). Both TOs use the same result dirs — path discipline is by filename prefix (case-001- vs case-002-).</note>
    <shared_artifacts>comp/results/wave-3b/ (shared with .058; append to integrity_audit.md)</shared_artifacts>
  </cross_domain_coordination>

  <acceptance_criteria>
    1. Phase 1 verdict files for both Case 2 conditions committed before Phase 2.
    2. Phase 2 metric-audit JSON at comp/results/wave-3b/metric_audit/case-002-efficiency-delta.json.
    3. integrity_audit.md has Case 2 section appended.
    4. confidence_note field present in case-002 metric-audit JSON.
    5. Phase 1 verdict files contain no reasoning.md content.
    6. Commit --only --author="2.1.0_SC_CompLearns &lt;2.1.0_SC_CompLearns@opal.agent&gt;" -- comp/results/wave-3b/verdicts/case-002-* comp/results/wave-3b/metric_audit/case-002-* comp/results/wave-3b/integrity_audit.md.
    7. Pushed to CLOUD.
    8. Session log with Compiler Tools section.
    9. MCP COMPLETE to 2.1.0_SA_COO.
  </acceptance_criteria>

  <dependencies>
    - Gate: .056 (condition_a bundle) COMPLETE.
    - Gate: .057 (condition_b bundle) COMPLETE.
    - Gate: COO bundle inspection clearance (same §6 new-task-family rule — COO MCPs cleared before dispatch).
    - Sequenced after .058 MCP COMPLETE (single SC agent).
  </dependencies>

  <operational_notes>
    - Operate from /c/Users/AndrewBerman/Desktop/feature_clb.
    - Phase 1 MUST be committed before Phase 2.
    - reasoning.md excluded in Phase 1; may be read in Phase 2 for confidence_note only.
    - Prior_exposure for 1.3.0_DS condition_a is noted, not invalidating.
    - No emojis.
  </operational_notes>

  <closeout>
    - commit --only --author="2.1.0_SC_CompLearns &lt;2.1.0_SC_CompLearns@opal.agent&gt;" -- comp/results/wave-3b/verdicts/case-002-* comp/results/wave-3b/metric_audit/case-002-* comp/results/wave-3b/integrity_audit.md
    - push to CLOUD
    - flip TO status complete
    - MCP COMPLETE to 2.1.0_SA_COO
    - session log
  </closeout>
</task_order>
