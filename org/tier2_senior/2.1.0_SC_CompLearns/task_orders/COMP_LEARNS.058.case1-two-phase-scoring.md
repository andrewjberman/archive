<task_order>
  <metadata>
    <id>2.1.0_SC_CompLearns-2026-04-24-comp-learns-058-case1-two-phase-scoring</id>
    <issued_by>2.1.0_SA_COO</issued_by>
    <issued_to>2.1.0_SC_CompLearns</issued_to>
    <date>2026-04-24</date>
    <status>complete <!-- Phase 1 freeze: 14f6b44d; Phase 2 ship: pending --></status>
    <project_code>COMP_LEARNS</project_code>
    <priority>P0 — Wave 3b Lane B, Case 1 formal scoring verdict</priority>
  </metadata>

  <references>
    <ref type="prd">docs/architecture/COMP_LEARNS_WAVE3_V1.md §3.5 (two-phase scoring) + §3.6 (reproduction) + §3.7 (claim scope) + §7 (Stage 2 wave counting) — bd84ef10</ref>
    <ref type="prd">docs/architecture/COMP_LEARNS_WAVE3_V1.md §3.8 preflight gates (adapted for httpx)</ref>
    <ref type="packet">comp/tasks/task-001-httpx-netrc-host-authority/packet.yaml — authoritative ACs</ref>
    <ref type="pair_inputs">.054 bundle (1.4.0_DS condition_a unaided) + .055 bundle (1.2.0_DS condition_b aided)</ref>
    <ref type="wave3b_decision">COMP_LEARNS.WAVE3B-DECISION.md §3 — add confidence_note field to metric-audit JSON (non-PRD-amending)</ref>
    <ref type="precedent">.051 (Case 3 scoring) — same two-phase model; mirror that TO's discipline</ref>
  </references>

  <objective>
    Score Case 1 via the two-phase model per PRD §3.5. Phase 1 produces a frozen verdict
    from standard bundle artifacts (reasoning.md excluded). Phase 2 extracts navigation-
    efficiency metrics from nav_log.jsonl AFTER verdict freeze. Do NOT revisit verdict
    in Phase 2.

    ## Phase 1 — Verdict (reasoning.md EXCLUDED)

    1. For each condition:
       - ds-1.4.0-condition_a (unaided): comp/tasks/task-001-httpx-netrc-host-authority/bundles/ds-1.4.0-condition_a/
       - ds-1.2.0-condition_b (aided): comp/tasks/task-001-httpx-netrc-host-authority/bundles/ds-1.2.0-condition_b/
       Read ONLY: changes.patch + test_output.txt. Do NOT read reasoning.md.

    2. Evaluate task correctness per packet.yaml acceptance_criteria:
       - ac-1: pytest tests/client/test_auth.py -q -k netrc (regression baseline)
       - ac-2: pytest tests/client/test_auth.py -q -k netrc_non_standard_port (new test)
       - ac-3: pytest tests/client/test_auth.py tests/test_auth.py -q (no regressions)
       For each AC, infer PASS/FAIL from test_output.txt content (look for exit 0 evidence
       and test result lines).

    3. Emit Phase 1 verdict per condition:
       comp/results/wave-3b/verdicts/case-001-ds-1.4.0-condition_a-run-1.json
       comp/results/wave-3b/verdicts/case-001-ds-1.2.0-condition_b-run-1.json

       Schema:
       ```json
       {
         "packet_id": "task-001-httpx-netrc-host-authority",
         "agent": "1.4.0_DS_CompLearns",
         "condition": "condition_a",
         "run": 1,
         "verdict": "PASS|FAIL",
         "ac_results": {"ac-1": "PASS|FAIL", "ac-2": "PASS|FAIL", "ac-3": "PASS|FAIL"},
         "judge_model_id": "claude-sonnet-4-6",
         "scored_by": "2.1.0_SC_CompLearns",
         "scored_at": "<ISO8601>",
         "phase": 1,
         "prior_exposure_note": "<copy from bundle reasoning.md prior_exposure field>",
         "notes": "<neutral observations; NO reasoning.md content>"
       }
       ```

    4. Commit Phase 1 verdicts. FREEZE: do NOT modify after Phase 2 begins.

    ## Phase 2 — Metric audit (nav_log.jsonl input)

    5. For each bundle, read nav_log.jsonl:
       - comp/tasks/task-001-httpx-netrc-host-authority/bundles/ds-1.4.0-condition_a/nav_log.jsonl
       - comp/tasks/task-001-httpx-netrc-host-authority/bundles/ds-1.2.0-condition_b/nav_log.jsonl

    6. Extract per-condition metrics (per §3.5 table):
       - Wall-clock to first correct hypothesis: ts of first hypothesis(correct=true) minus ts of first file_open
       - Token usage to first correct hypothesis: token_count at first correct hypothesis
       - Files touched before decisive file: count of file_open events before first file_open on httpx/_utils.py
       - Irrelevant files touched: count of file_open on files NOT in {httpx/_utils.py, httpx/_client.py}
       - comp_call count: count of comp_call events (expect 0 for unaided, >0 for aided)

       Decisive file set for Case 1: httpx/_utils.py (root cause). httpx/_client.py is secondary.

    7. Compute aided-vs-unaided deltas (condition_b minus condition_a for each metric):
       - Positive wall-clock delta = aided slower
       - Positive token delta = aided more expensive

    8. Noise checks:
       - If condition_b nav_log has 0 comp_call events: flag as noise (aided run may not have used harness)
       - If aided + unaided nav_logs show identical file_open sequences: flag as possible contamination
       - If wall-clock or tokens are >3x expected: flag as implausible outlier

    9. Confound check:
       - condition_a bundle prior_exposure field says "pilot-wave-1 condition_a, separate session" — document
         in narrative. Prior separate session is not invalidating but note the directional caveat.

    10. Add confidence_note field (per CTO Wave 3b decision §3 — non-amending):
        In the metric-audit JSON, include:
        ```json
        "confidence_note": "<SC assessment: did the aided or unaided agent appear more confident at hypothesis-formation time? Read reasoning.md (Phase 2 only, after verdict freeze) to assess. Subjective OK. E.g.: 'aided agent showed higher confidence — stated correct file immediately; unaided hedged across 2 files before settling'>"
        ```

    11. Emit Phase 2 metric-audit file:
        comp/results/wave-3b/metric_audit/case-001-efficiency-delta.json

        Schema:
        ```json
        {
          "packet_id": "task-001-httpx-netrc-host-authority",
          "judge_model_id": "claude-sonnet-4-6",
          "phase": 2,
          "scored_by": "2.1.0_SC_CompLearns",
          "scored_at": "<ISO8601>",
          "verdict_freeze_ref": {
            "condition_a": "comp/results/wave-3b/verdicts/case-001-ds-1.4.0-condition_a-run-1.json",
            "condition_b": "comp/results/wave-3b/verdicts/case-001-ds-1.2.0-condition_b-run-1.json"
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
            "wall_clock_sec": <int>,
            "tokens": <int>,
            "files_touched": <int>,
            "irrelevant_files_touched": <int>
          },
          "noise_flags": [],
          "confidence_note": "<per step 10 above>",
          "narrative_summary": "<one paragraph: did compiler assistance materially reduce exploration waste on this bug-localization task? evidence>"
        }
        ```

    12. Author comp/results/wave-3b/integrity_audit.md (or append to existing if already started):
        Confirm Phase 1 verdict → commit → Phase 2 ordering. reasoning.md exclusion in Phase 1.
        nav_log hygiene (unaided = 0 comp_calls; aided has comp_calls). No cross-condition contamination.

    13. MCP COMPLETE to 2.1.0_SA_COO with:
        - condition_a verdict: PASS/FAIL
        - condition_b verdict: PASS/FAIL
        - efficiency delta one-liner (e.g. "aided N% faster/slower wall-clock; X files fewer; Y% token delta")
        - noise_flags if any

    Explicitly out of scope:
    - Case 2 scoring — that is .059
    - Revisiting Phase 1 verdict during Phase 2
    - Cross-model scoring
  </objective>

  <compiler_tools_mandate>
    <phase id="1" when="before Phase 1 scoring">
      <step>
        <run>ls comp/tasks/task-001-httpx-netrc-host-authority/bundles/ds-1.4.0-condition_a/ &amp;&amp; ls comp/tasks/task-001-httpx-netrc-host-authority/bundles/ds-1.2.0-condition_b/</run>
        <expect>Both bundle directories exist with changes.patch + test_output.txt + reasoning.md + nav_log.jsonl each</expect>
        <if_mismatch>STOP. .054 or .055 not yet shipped. MCP COO.</if_mismatch>
      </step>
      <step>
        <run>mkdir -p comp/results/wave-3b/verdicts comp/results/wave-3b/metric_audit</run>
        <expect>Output dirs created</expect>
        <if_mismatch>Fix path issue.</if_mismatch>
      </step>
    </phase>
    <phase id="2" when="before Phase 2 (after Phase 1 verdict commit)">
      <step>
        <run>ls comp/results/wave-3b/verdicts/ | grep case-001</run>
        <expect>Both case-001 verdict files present and committed</expect>
        <if_mismatch>Complete + commit Phase 1 first. Phase 2 requires verdict freeze.</if_mismatch>
      </step>
      <step>
        <run>python -c "import json; rows=[json.loads(l) for l in open('comp/tasks/task-001-httpx-netrc-host-authority/bundles/ds-1.2.0-condition_b/nav_log.jsonl')]; cc=sum(1 for r in rows if r['event']=='comp_call'); print(f'aided comp_calls: {cc}')"</run>
        <expect>aided comp_calls: 1 or more</expect>
        <if_mismatch>Flag noise (0 comp_calls in aided run). Document in metric_audit noise_flags. MCP COO before proceeding.</if_mismatch>
      </step>
    </phase>
    <phase id="3" when="after commit">
      <step>
        <run>ls comp/results/wave-3b/</run>
        <expect>verdicts/ + metric_audit/ + integrity_audit.md (or integrity_audit.md updated)</expect>
        <if_mismatch>Author missing artifacts.</if_mismatch>
      </step>
    </phase>
  </compiler_tools_mandate>

  <cross_domain_coordination>
    <note>Phase 1 verdict must not reference nav_log or reasoning.md content. Phase 2 must not revisit verdict. This TO blocks .059 only in the sense that SC is a single agent (sequential). COO will dispatch .059 after your MCP COMPLETE on .058.</note>
    <shared_artifacts>comp/results/wave-3b/integrity_audit.md (append when .059 is also done); comp/results/wave-3b/verdicts/ and metric_audit/ (created by this TO)</shared_artifacts>
  </cross_domain_coordination>

  <acceptance_criteria>
    1. Phase 1 verdict JSON files for both conditions at comp/results/wave-3b/verdicts/ before any Phase 2 work.
    2. Phase 1 verdicts committed (frozen) before Phase 2 begins.
    3. Phase 2 metric-audit JSON at comp/results/wave-3b/metric_audit/case-001-efficiency-delta.json with all §3.5 metrics + deltas + noise_flags + confidence_note.
    4. comp/results/wave-3b/integrity_audit.md started (will be appended for Case 2 in .059).
    5. Phase 1 verdict files contain no nav_log or reasoning.md content.
    6. verdict_freeze_ref in Phase 2 JSON cites the Phase 1 freeze commit sha.
    7. Commit --only --author="2.1.0_SC_CompLearns &lt;2.1.0_SC_CompLearns@opal.agent&gt;" pathspec comp/results/wave-3b/**.
    8. Pushed to CLOUD.
    9. Session log at org/tier2_senior/2.1.0_SC_CompLearns/logs/{date}/ with Compiler Tools section + Phase 1-to-Phase 2 ordering evidence.
    10. MCP COMPLETE to 2.1.0_SA_COO with per-condition PASS/FAIL + one-line efficiency delta + noise_flags.
  </acceptance_criteria>

  <dependencies>
    - Gate: .054 (condition_a bundle) COMPLETE.
    - Gate: .055 (condition_b bundle) COMPLETE.
    - Gate: COO manual inspection of bundles (first Case 1 Wave 3b dispatch per AUTOMATION_V1 §6 new-task-family rule — COO MCPs "cleared for SC dispatch" after inspecting both bundles).
    - Blocks: .059 (SC Case 2 scoring — SC is single agent; sequential).
  </dependencies>

  <operational_notes>
    - Operate from /c/Users/AndrewBerman/Desktop/feature_clb.
    - Phase 1 MUST be committed before Phase 2 begins — verdict freeze.
    - reasoning.md exclusion in Phase 1 is manual verification (not automation yet). Before Phase 1, confirm your input surface does not include reasoning.md content.
    - confidence_note is Phase 2 only (you may read reasoning.md in Phase 2 to assess confidence).
    - Prior_exposure flag (condition_a) is not invalidating — note it in verdict notes.
    - No emojis.
  </operational_notes>

  <closeout>
    - commit --only --author="2.1.0_SC_CompLearns &lt;2.1.0_SC_CompLearns@opal.agent&gt;" -- comp/results/wave-3b/**
    - push to CLOUD
    - flip TO status complete with Phase 1 freeze sha + Phase 2 ship sha
    - MCP COMPLETE to 2.1.0_SA_COO
    - session log
  </closeout>
</task_order>
