<task_order>
  <metadata>
    <id>2.1.0_SC_CompLearns-2026-04-22-comp-learns-051-case3-two-phase-scoring</id>
    <issued_by>2.1.0_SA_COO</issued_by>
    <issued_to>2.1.0_SC_CompLearns</issued_to>
    <date>2026-04-22</date>
    <status>staged <!-- Gate: .049 + .050 both COMPLETE + COO manual inspection (first task family). GO from COO after both bundles ready. --></status>
    <project_code>COMP_LEARNS</project_code>
    <priority>P0 — Wave 3 Lane B verdict + efficiency delta; first aided-vs-unaided formal measurement</priority>
  </metadata>

  <references>
    <ref type="prd">docs/architecture/COMP_LEARNS_WAVE3_V1.md §3.5 (two-phase scoring model + nav_log.jsonl format) + §3.6 (reproduction + trust) + §3.7 (claim scope) + §7 (Stage 2 wave counting) + §8 — commit 30971db1</ref>
    <ref type="packet">comp/tasks/case-003-sphinx-autodoc-typehints/packet.yaml — fa1d5eb8; acceptance criteria authoritative</ref>
    <ref type="pair_inputs">.049 bundle (1.3.0_DS condition_b aided) + .050 bundle (1.4.0_DS condition_a unaided)</ref>
  </references>

  <objective>
    Score Case 3 via the two-phase model per PRD §3.5. Phase 1 produces a frozen verdict
    from standard bundle artifacts (reasoning.md excluded). Phase 2 extracts navigation-
    efficiency metrics from nav_log.jsonl AFTER verdict freeze. You must NOT revisit the
    verdict in Phase 2.

    ## Phase 1 — Verdict (reasoning.md excluded)

    1. For each condition (ds-1.3.0-condition_b aided + ds-1.4.0-condition_a unaided):
       - Read packet.yaml + changes.patch + test_output.txt ONLY
       - reasoning.md is MECHANICALLY EXCLUDED — COO-provisioned scorer worktree will
         enforce this; verify your input surface does not contain reasoning.md

    2. Evaluate task correctness per packet.yaml acceptance_criteria:
       - ac-1: pytest tests/test_ext_autodoc_configs.py::test_autodoc_typehints_description_with_documented_init (FAIL_TO_PASS)
       - ac-2: pytest tests/test_ext_autodoc_configs.py -q (regression guard)
       - ac-3: pytest tests/test_ext_autodoc.py -q (broader regression guard)

    3. Emit Phase 1 verdict file per bundle:
       `comp/results/wave-3a/verdicts/case-003-ds-{agent}-{condition}-run-1.json`

       Schema (mirror Wave 1 verdict structure):
       ```json
       {
         "packet_id": "case-003-sphinx-autodoc-typehints",
         "agent": "1.3.0_DS_CompLearns" | "1.4.0_DS_CompLearns",
         "condition": "condition_a" | "condition_b",
         "run": 1,
         "verdict": "PASS" | "FAIL",
         "ac_results": {"ac-1": "PASS|FAIL", "ac-2": "PASS|FAIL", "ac-3": "PASS|FAIL"},
         "judge_model_id": "<pinned value>",
         "scored_by": "2.1.0_SC_CompLearns",
         "scored_at": "<ISO8601>",
         "phase": 1,
         "notes": "<neutral observations; NO reasoning.md content>"
       }
       ```

    4. Commit Phase 1 verdicts. FREEZE: do NOT modify after Phase 2 begins.

    ## Phase 2 — Metric audit (nav_log.jsonl input)

    5. For each bundle, read nav_log.jsonl:
       - `comp/tasks/case-003-sphinx-autodoc-typehints/bundles/ds-1.3.0-condition_b/nav_log.jsonl`
       - `comp/tasks/case-003-sphinx-autodoc-typehints/bundles/ds-1.4.0-condition_a/nav_log.jsonl`

    6. Extract per-condition metrics (§3.5 table):
       | Metric | Extraction method |
       |--------|-------------------|
       | Wall-clock to first correct hypothesis | ts of first `hypothesis` with correct=true - ts of session start (first file_open) |
       | Token usage to first correct hypothesis | cumulative token_count at first correct hypothesis |
       | Files touched before reaching decisive file set | count of distinct file_open paths before first entry on `sphinx/ext/autodoc/typehints.py` |
       | Irrelevant files touched | count of file_open events on files NOT in decisive file set |
       | Compiler tool calls | count of `comp_call` events (expect 0 for unaided; >0 for aided) |

    7. Compute aided-vs-unaided deltas (aided minus unaided for each metric):
       - Positive delta on wall-clock / token / files-touched = AIDED ADVANTAGE (less exploration)
       - Positive delta on compiler tool calls = expected (aided uses comp/)

    8. Noise checks per §3.5:
       - If condition_b nav_log has 0 comp_call events → aided run invalid, flag for re-run
       - If aided + unaided nav_logs show identical navigation paths → compiler not used
         meaningfully, flag for re-run
       - If wall-clock or token counts show implausible outliers (>3x expected) → flag

    9. Confounding checks per §3.6:
       - If unaided run solved via online search vs structural reasoning → flag confound
       - If unaided agent had prior sphinx exposure → flag confound

    10. Emit Phase 2 metric-audit file:
        `comp/results/wave-3a/metric_audit/case-003-efficiency-delta.json`

        Schema:
        ```json
        {
          "packet_id": "case-003-sphinx-autodoc-typehints",
          "judge_model_id": "<pinned>",
          "phase": 2,
          "scored_by": "2.1.0_SC_CompLearns",
          "scored_at": "<ISO8601>",
          "verdict_freeze_ref": {
            "condition_a": "<path to Phase 1 verdict>",
            "condition_b": "<path to Phase 1 verdict>"
          },
          "per_condition": {
            "condition_a_unaided": {
              "wall_clock_to_first_correct_sec": <int>,
              "tokens_to_first_correct": <int>,
              "files_touched_before_decisive": <int>,
              "irrelevant_files_touched": <int>,
              "comp_calls": 0,
              "decisive_file_found": <bool>
            },
            "condition_b_aided": {
              "wall_clock_to_first_correct_sec": <int>,
              "tokens_to_first_correct": <int>,
              "files_touched_before_decisive": <int>,
              "irrelevant_files_touched": <int>,
              "comp_calls": <int>,
              "decisive_file_found": <bool>
            }
          },
          "delta_aided_minus_unaided": {
            "wall_clock_sec": <int, positive = aided slower (reversed from intuition — note sign in narrative)>,
            "tokens": <int>,
            "files_touched": <int>,
            "irrelevant_files_touched": <int>
          },
          "noise_flags": [<list of §3.5 noise/confound flags>],
          "narrative_summary": "<one paragraph: did compiler assistance materially reduce exploration waste? evidence>"
        }
        ```

    11. Author `comp/results/wave-3a/integrity_audit.md` — brief audit confirming:
        - Phase 1 verdict produced before Phase 2 metric work
        - reasoning.md exclusion verified mechanically via wave-runner logs (or manual
          inspection if first dispatch was manual per §7 new-task-family rule)
        - nav_log.jsonl hygiene (unaided = 0 comp_call; aided has comp_call events)
        - No cross-contamination between condition_a and condition_b runs

    12. MCP COMPLETE to 2.1.0_SA_COO with: verdict summary (PASS/FAIL per condition) +
        delta summary (one-line: "aided N% faster/slower on wall-clock; N% fewer irrelevant files; X% token delta") + noise_flags if any.

    Explicitly out of scope:
    - Scoring dev-4 (.048 — that is loop-proving; no SC verdict needed, CTO reads
      loop_fitness_recommendation.md directly)
    - Modifying verdict after Phase 2 starts — §3.5 non-negotiable
    - Cross-model scoring (Wave 4 scope)
    - Claims beyond Wave 3 scope (§3.7 — directional evidence only on single case)
  </objective>

  <compiler_tools_mandate>
    <phase id="1" when="before Phase 1 scoring">
      <step>
        <run>ls comp/tasks/case-003-sphinx-autodoc-typehints/bundles/ds-1.3.0-condition_b/ && ls comp/tasks/case-003-sphinx-autodoc-typehints/bundles/ds-1.4.0-condition_a/</run>
        <expect>Both bundles exist with changes.patch + test_output.txt + reasoning.md + nav_log.jsonl each.</expect>
        <if_mismatch>STOP. .049 or .050 not yet shipped. MCP COO.</if_mismatch>
      </step>
      <step>
        <run>mkdir -p comp/results/wave-3a/verdicts comp/results/wave-3a/metric_audit</run>
        <expect>Output dirs created.</expect>
        <if_mismatch>Fix permission / path issue.</if_mismatch>
      </step>
    </phase>
    <phase id="2" when="before Phase 2 metric audit (after Phase 1 verdict commit)">
      <step>
        <run>ls comp/results/wave-3a/verdicts/</run>
        <expect>Phase 1 verdict files for both conditions present + committed.</expect>
        <if_mismatch>Complete + commit Phase 1 first. Phase 2 requires verdict freeze.</if_mismatch>
      </step>
      <step>
        <run>python -c "import json; rows = [json.loads(l) for l in open('comp/tasks/case-003-sphinx-autodoc-typehints/bundles/ds-1.3.0-condition_b/nav_log.jsonl')]; assert any(r['event']=='comp_call' for r in rows); print('aided nav_log has comp_calls')"</run>
        <expect>Prints confirmation; aided run used compiler tools.</expect>
        <if_mismatch>Aided run invalid per §3.5 — flag noise, MCP COO for re-run.</if_mismatch>
      </step>
      <step>
        <run>python -c "import json; rows = [json.loads(l) for l in open('comp/tasks/case-003-sphinx-autodoc-typehints/bundles/ds-1.4.0-condition_a/nav_log.jsonl')]; assert not any(r['event']=='comp_call' for r in rows); print('unaided nav_log has zero comp_calls')"</run>
        <expect>Prints confirmation; unaided run was uncontaminated.</expect>
        <if_mismatch>Unaided run tainted (comp_call present). Flag noise, MCP COO for re-run.</if_mismatch>
      </step>
    </phase>
    <phase id="3" when="after commit">
      <step>
        <run>ls comp/results/wave-3a/</run>
        <expect>verdicts/ + metric_audit/ + integrity_audit.md all present.</expect>
        <if_mismatch>Author missing artifacts.</if_mismatch>
      </step>
    </phase>
  </compiler_tools_mandate>

  <cross_domain_coordination>
    <note>Your scoring is the formal measurement outcome of Wave 3 Lane B. Non-contamination: Phase 1 verdict must not reference nav_log content or reasoning.md. Phase 2 must not revisit verdict. COO will manually inspect the first Case 3 dispatch per §7 (new task family); after your clean ship, Wave 3b Cases 1+2 reruns proceed under standard Stage 2 automation.</note>
    <shared_artifacts>comp/tasks/case-003-sphinx-autodoc-typehints/bundles/ds-1.3.0-condition_b/** + ds-1.4.0-condition_a/** (read-only); comp/results/wave-3a/** (created by this TO)</shared_artifacts>
  </cross_domain_coordination>

  <acceptance_criteria>
    1. Phase 1 verdict JSON files produced per condition at comp/results/wave-3a/verdicts/ before any Phase 2 work.
    2. Phase 1 verdicts committed (frozen) before Phase 2 begins.
    3. Phase 2 metric-audit JSON at comp/results/wave-3a/metric_audit/case-003-efficiency-delta.json with all §3.5 metrics + aided-vs-unaided deltas + noise flags.
    4. comp/results/wave-3a/integrity_audit.md authored confirming Phase 1→2 ordering + reasoning.md exclusion + nav_log hygiene + no cross-contamination.
    5. Phase 1 verdict file contains no nav_log or reasoning.md content.
    6. Phase 2 verdict field cites the Phase 1 freeze SHA in verdict_freeze_ref.
    7. Commit --only --author=2.1.0_SC_CompLearns pathspec scoped to comp/results/wave-3a/**.
    8. Pushed to CLOUD.
    9. Session log at org/tier2_senior/2.1.0_SC_CompLearns/logs/{date}/ with Compiler Tools section.
    10. MCP COMPLETE to 2.1.0_SA_COO with per-condition PASS/FAIL + one-line efficiency delta summary + noise_flags.
  </acceptance_criteria>

  <dependencies>
    - Gate: .049 (condition_b aided bundle) COMPLETE.
    - Gate: .050 (condition_a unaided bundle) COMPLETE.
    - Gate: COO manual inspection of first Case 3 bundle (AUTOMATION_V1 §6 new-task-family rule) — I will MCP you "cleared for SC dispatch" after inspecting both bundles.
    - Blocks: .053 Wave 3a joint review (.053 gates on .051 verdict + .048 dev-4 output).
  </dependencies>

  <operational_notes>
    - Operate from /c/Users/AndrewBerman/Desktop/feature_clb.
    - Phase 1 MUST be committed before Phase 2 begins — this is the "verdict freeze" per §3.5.
    - Phase 2 is mechanical extraction from nav_log + delta computation + narrative. Do NOT
      re-interpret task correctness in Phase 2; the verdict is frozen.
    - reasoning.md exclusion is mechanical — your scorer input surface (COO-provisioned
      worktree OR your manual review surface for first-dispatch) must NOT contain
      reasoning.md. Verify before Phase 1.
    - Noise flags are INFORMATIONAL in the metric audit JSON — a flagged run does NOT
      invalidate the verdict automatically; your narrative should explain implications
      for the directional-evidence claim.
    - Wave 3 is directional evidence per §3.7 — your scoring supports "found earlier" or
      "did not find earlier" claims, NOT statistical significance claims.
    - No emojis in any JSON / MD / narrative output (CLAUDE.md).
  </operational_notes>

  <closeout>
    On completion:
    - commit --only --author="2.1.0_SC_CompLearns &lt;2.1.0_SC_CompLearns@opal.agent&gt;" -- comp/results/wave-3a/**
    - push to CLOUD
    - flip TO status to complete with commit refs (Phase 1 freeze + Phase 2 ship)
    - MCP COMPLETE to 2.1.0_SA_COO — your ship + .048 dev-4 ship trigger .053 joint review
    - session log with Compiler Tools section + Phase 1-to-Phase 2 ordering evidence
  </closeout>
</task_order>
