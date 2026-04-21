<task_order>
  <metadata>
    <id>1.3.0_DS_CompLearns-2026-04-21-comp-learns-034-backlog-seed</id>
    <issued_by>2.1.0_SA_COO</issued_by>
    <issued_to>1.3.0_DS_CompLearns</issued_to>
    <date>2026-04-21</date>
    <status>complete <!-- be95f82c --></status>
    <project_code>COMP_LEARNS</project_code>
    <priority>P1 — parallel to .029/.030; no blocking dependency; unblocks .031 authoring</priority>
  </metadata>

  <references>
    <ref type="prd">docs/architecture/COMP_LEARNS_PARALLELIZATION_V1.md §13 (Benchmark backlog — acquisition and curation)</ref>
    <ref type="prereads">1.3.0_DS click pre-read (8 failure modes, logged 2026-04-21); 1.1.0_DS httpx pre-read (PR #1298 NetRC host+port cross-module bug)</ref>
    <ref type="schema">comp/backlog/ YAML schema defined in PRD §13 — 12 fields, harness_relevance_score + aided_vs_unaided_comparability are hard gates</ref>
  </references>

  <objective>
    Seed the COMP_LEARNS benchmark backlog (`comp/backlog/`) with two wave-1 entries and the schema
    definition file. This materializes §13 doctrine as concrete artifacts and gives .031 case-packet
    authoring an authoritative source to reference.

    Explicitly in scope:
    1. Create `comp/backlog/` directory with `README.md` (one paragraph: what this dir is, anti-pattern warning, how to add entries).
    2. Create `comp/backlog/backlog_schema.yaml` — canonical schema doc listing all 12 required fields, allowed values per field, and which are hard gates.
    3. Create `comp/backlog/bl-httpx-001.yaml` — Case 1 entry (httpx PR #1298 NetRC host+authority cross-module bug).
    4. Create `comp/backlog/bl-click-001.yaml` — Case 2 entry (click refactor, invariant-preservation task).

    Explicitly out of scope:
    - SWE-bench download or any external data pull — these entries are authored from pre-read context only.
    - Task packet authoring (.031 scope).
    - Any Python code.
  </objective>

  <schema>
    Per PRD §13, every backlog entry must carry these 12 fields:

    ```yaml
    backlog_id: bl-{repo}-{NNN}
    source: oss-historical          # swe-bench-verified | oss-historical | defects4j | bugsjs | synthetic
    target_repo: httpx              # repo short name matching comp/targets/<name>
    target_language: python
    baseline_commit: <sha>          # commit in target repo that is the pre-fix state; use "unknown" if not resolved
    archetype: structural_bug_localization   # structural_bug_localization | refactor_invariant_preservation | performance_regression | api_contract_change
    harness_relevance_score: high   # high | medium | low  — HARD GATE: only high enters wave-1
    expected_ds_wall_clock_min: 20  # estimate in minutes
    measurement_axes_stressed:
      - correctness
      - harness_navigation_usefulness
    acceptance_criterion_type: test_suite   # test_suite | regression_check | rubric
    aided_vs_unaided_comparability: yes     # yes | no | conditional — HARD GATE: must be yes
    notes: "..."
    ```

    Do not add fields beyond these 12. Do not omit any. If a value is genuinely unknown (e.g., exact
    baseline_commit for click refactor), use the string `"unknown"` and note why in the `notes` field.
  </schema>

  <entry_guidance>
    **bl-httpx-001 (Case 1):**
    - source: oss-historical
    - target_repo: httpx
    - archetype: structural_bug_localization
    - harness_relevance_score: high (cross-module _client.py/_utils.py; selector must navigate both)
    - measurement_axes_stressed: [correctness, harness_navigation_usefulness]
    - acceptance_criterion_type: test_suite (httpx PR #1298 had a regression test)
    - aided_vs_unaided_comparability: yes
    - notes: use your 1.1.0_DS pre-read content; PR #1298 NetRC host+port vs host+authority;
      symptom in _client.py, root cause in _utils.py; baseline_commit = commit just before PR #1298 merge

    **bl-click-001 (Case 2):**
    - source: oss-historical
    - target_repo: click
    - archetype: refactor_invariant_preservation
    - harness_relevance_score: high (8 failure modes; selector must surface decorator + group invariants)
    - measurement_axes_stressed: [correctness, harness_navigation_usefulness]
    - acceptance_criterion_type: regression_check
    - aided_vs_unaided_comparability: yes
    - notes: use your click pre-read 8 failure modes; baseline_commit = "unknown" if no specific
      OSS PR maps to this; describe the refactor invariant being tested in notes

    For baseline_commit on httpx: check the comp/targets/httpx/_repo git log for the commit
    immediately preceding the merge of PR #1298. If the repo is present, use `git log --oneline`
    to find it. If not resolvable, use `"unknown"` with a note.
  </entry_guidance>

  <acceptance_criteria>
    1. `comp/backlog/` directory exists with README.md (anti-pattern warning present).
    2. `comp/backlog/backlog_schema.yaml` present; lists all 12 fields with allowed values and hard-gate markers.
    3. `comp/backlog/bl-httpx-001.yaml` present; all 12 fields populated; harness_relevance_score=high; aided_vs_unaided_comparability=yes.
    4. `comp/backlog/bl-click-001.yaml` present; all 12 fields populated; harness_relevance_score=high; aided_vs_unaided_comparability=yes.
    5. No Python files created (YAML + Markdown only — no ds-commit-gate required).
    6. Commit with `--author="1.3.0_DS_CompLearns &lt;1.3.0_DS_CompLearns@opal.agent&gt;"`.
    7. MCP COMPLETE to 2.1.0_SA_COO with commit sha.
  </acceptance_criteria>

  <dependencies>
    - None blocking. Can execute immediately.
    - Informational input: 1.1.0_DS httpx PR #1298 pre-read (already logged 2026-04-21).
    - Informational input: your own click 8-failure-mode pre-read (already logged 2026-04-21).
    - comp/targets/httpx/_repo (for baseline_commit lookup — optional; use "unknown" if not present).
  </dependencies>

  <operational_notes>
    - Operate from feature_clb/ worktree (C:/Users/AndrewBerman/Desktop/feature_clb). Confirm pwd before first write.
    - YAML files only — no Python, no tests, no ds-commit-gate required.
    - Do not download SWE-bench or any external data. Author entries from pre-read context only.
    - Do not author task packets (.031 scope). Backlog entries are the source; packets are derived from them.
    - If comp/targets/httpx/_repo is missing or the git log is not resolvable, use baseline_commit: "unknown".
  </operational_notes>

  <closeout>
    On completion:
    - commit with `--author="1.3.0_DS_CompLearns &lt;1.3.0_DS_CompLearns@opal.agent&gt;"`
    - flip TO status to `complete` with commit ref in the status comment
    - MCP COMPLETE to 2.1.0_SA_COO with commit sha + 4-file checklist status
    - session log under `org/tier2_senior/1.3.0_DS_CompLearns/logs/2026-04-21/`
  </closeout>
</task_order>
