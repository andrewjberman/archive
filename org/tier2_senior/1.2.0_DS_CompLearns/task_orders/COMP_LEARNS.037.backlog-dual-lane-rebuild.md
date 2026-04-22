<task_order>
  <metadata>
    <id>1.2.0_DS_CompLearns-2026-04-22-comp-learns-037-backlog-dual-lane-rebuild</id>
    <issued_by>2.1.0_SA_COO</issued_by>
    <issued_to>1.2.0_DS_CompLearns</issued_to>
    <date>2026-04-22</date>
    <status>complete <!-- commit 9fd69bce pushed CLOUD 2026-04-22 by 1.2.0_DS_CompLearns --></status>
    <project_code>COMP_LEARNS</project_code>
    <priority>P0 — foundation TO for Wave 2 backlog work; .038/.039/.040/.041 all depend on this schema landing</priority>
  </metadata>

  <references>
    <ref type="prd">docs/architecture/COMP_LEARNS_BACKLOG_V1.md §3 (benchmark schema) + §4 (dev schema) + §5 (archetypes) + §8 (BACKLOG.md index) + §10 (TO decomposition)</ref>
    <ref type="existing_entries">comp/backlog/bl-httpx-001.yaml + comp/backlog/bl-click-001.yaml (both currently at repo root of comp/backlog/; migrate to comp/backlog/benchmark/ with `lane: benchmark` field added)</ref>
    <ref type="handoff_log">org/tier1_exec/1.1.0_SA_CTO/logs/2026-04-22/session13_wave2_prd_handoff.md (commit 8b09bda5) — CTO authoritative handoff</ref>
  </references>

  <objective>
    Rebuild comp/backlog/ with a dual-lane directory structure per BACKLOG_V1 §2. The current
    flat layout (bl-httpx-001.yaml + bl-click-001.yaml at comp/backlog/ root) becomes two
    lanes: benchmark/ (strict schema, formal scoring) and dev/ (relaxed schema, rapid iteration).

    Explicitly in scope:

    1. Create directories:
       - comp/backlog/benchmark/
       - comp/backlog/dev/

    2. Migrate existing entries to benchmark/ lane with schema update:
       - mv comp/backlog/bl-httpx-001.yaml comp/backlog/benchmark/bl-httpx-001.yaml
       - mv comp/backlog/bl-click-001.yaml comp/backlog/benchmark/bl-click-001.yaml
       - Add `lane: benchmark` field to each (required by §3)
       - Verify all §3 required fields present (case_id, name, lane, target, language,
         baseline_commit, source, archetype, measurement_axes, harness_relevance,
         aided_unaided_safe, expected_ds_minutes, ac_type, status, notes). If any field
         is missing in the current YAML, ADD IT with a best-effort value and flag in
         notes that the value was back-filled during .037 migration — do not invent
         baseline_commits; if genuinely absent, use status: candidate.

    3. Author comp/backlog/BACKLOG.md — the unified index across both lanes. Table format
       per §8:

       ```markdown
       | case_id | name | target | lane | archetype | harness_relevance | status |
       |---------|------|--------|------|-----------|-------------------|--------|
       | bl-httpx-001 | ... | encode/httpx | benchmark | A | 4 | active |
       | bl-click-001 | ... | pallets/click | benchmark | B | 4 | active |
       ```

       BACKLOG.md header must reference BACKLOG_V1 PRD and note that new entries are added
       by CTO (.039) + COO (.038). Do not author entries for dev/ in this TO — that is
       CTO's lane in .039.

    4. Remove the old backlog schema file if it references the flat layout:
       - comp/backlog/README.md (currently stale — re-author to reference dual-lane)
       - comp/backlog/backlog_schema.yaml (if it exists and describes flat layout, migrate
         or delete; BACKLOG_V1 §3 + §4 are authoritative going forward)

    Explicitly out of scope:
    - Authoring new benchmark or dev entries — CTO (.039) + COO (.038) do that.
    - Populating dev/ directory with entries (leave empty with a .gitkeep or README stub).
    - Modifying comp/targets/* or comp/tasks/* — backlog reorg does not touch those.
    - Running any gold survey or pilot run.
  </objective>

  <compiler_tools_mandate>
    <phase id="1" when="before write">
      <step>
        <run>comp-build</run>
        <expect>Rebuild succeeds. No warnings about stale cache.</expect>
        <if_mismatch>Surface to COO — likely concurrent edit. Do not proceed with backlog migration until clean.</if_mismatch>
      </step>
      <step>
        <run>pytest comp/ -q</run>
        <expect>All existing tests PASS. Baseline before any file move.</expect>
        <if_mismatch>Rebase on current CLOUD before proceeding. Fix any unrelated red before touching backlog.</if_mismatch>
      </step>
    </phase>
    <phase id="2" when="before commit">
      <step>
        <run>ls comp/backlog/benchmark/ comp/backlog/dev/</run>
        <expect>benchmark/ contains bl-httpx-001.yaml + bl-click-001.yaml; dev/ exists (empty or stub).</expect>
        <if_mismatch>STOP. Structure must match §2 lane layout before commit.</if_mismatch>
      </step>
      <step>
        <run>python -c "import yaml; [print(k, yaml.safe_load(open(f'comp/backlog/benchmark/bl-{t}-001.yaml'))['lane']) for t in ['httpx','click']]"</run>
        <expect>Both prints "benchmark" — confirms lane field added.</expect>
        <if_mismatch>STOP. Add `lane: benchmark` to any missing entry. Re-run.</if_mismatch>
      </step>
      <step>
        <run>pytest comp/ -q</run>
        <expect>All tests PASS. No regressions from file moves.</expect>
        <if_mismatch>Investigate — a test likely imported comp/backlog/*.yaml by path. Fix the test reference or restore layout.</if_mismatch>
      </step>
      <step>
        <run>.tools/ds-commit-gate.sh comp/backlog/benchmark/bl-httpx-001.yaml comp/backlog/benchmark/bl-click-001.yaml</run>
        <expect>Exit 0 (YAMLs are stdlib-parseable; gate is not Python-specific but runs clean).</expect>
        <if_mismatch>Fix reported issue before commit.</if_mismatch>
      </step>
    </phase>
    <phase id="3" when="after commit">
      <step>
        <run>comp-build</run>
        <expect>Rebuild succeeds post-commit. No stale-cache warnings.</expect>
        <if_mismatch>Surface to COO — likely concurrent commit during your write.</if_mismatch>
      </step>
      <step>
        <run>cat comp/backlog/BACKLOG.md | head -20</run>
        <expect>Index table is populated with both bl-httpx-001 + bl-click-001 rows, lane column = benchmark.</expect>
        <if_mismatch>Re-author BACKLOG.md in a follow-up commit; do not leave stale.</if_mismatch>
      </step>
    </phase>
  </compiler_tools_mandate>

  <cross_domain_coordination>
    <note>.038 (COO, SWE-bench candidates) writes new files under comp/backlog/benchmark/ (bl-sweb-*.yaml) AFTER this TO completes. .039 (CTO, Case 4 + dev seeds) writes new files under both comp/backlog/benchmark/ (bl-*.yaml for Case 4) and comp/backlog/dev/ (dev-1..4 entries) AFTER this TO completes. Neither .038 nor .039 modifies bl-httpx-001 or bl-click-001. BACKLOG.md index will be appended to by .038 and .039 — append-only, no rewrite. This TO's author (1.2.0_DS) owns the initial structure + index format; subsequent TOs append rows.</note>
    <shared_artifacts>comp/backlog/BACKLOG.md (append-only after this TO)</shared_artifacts>
  </cross_domain_coordination>

  <acceptance_criteria>
    1. comp/backlog/benchmark/ directory exists; bl-httpx-001.yaml + bl-click-001.yaml inside, each with `lane: benchmark` field set.
    2. comp/backlog/dev/ directory exists (empty or with .gitkeep/README stub).
    3. comp/backlog/BACKLOG.md authored per §8 format — index table with both benchmark entries populated; header references BACKLOG_V1 PRD.
    4. comp/backlog/README.md re-authored (or deleted) — must NOT describe the flat pre-pilot layout.
    5. pytest comp/ -q GREEN (no regressions).
    6. All moves committed under --author=1.2.0_DS_CompLearns@opal.agent with --only pathspec limiting to comp/backlog/** files.
    7. Pushed to CLOUD.
    8. Session log at org/tier2_senior/1.2.0_DS_CompLearns/logs/2026-04-22/ with Compiler Tools section documenting comp-build + pytest runs.
    9. MCP COMPLETE to 2.1.0_SA_COO with commit sha — this unblocks .038 (SWE-bench candidates) and .039 (CTO dev seeds).
  </acceptance_criteria>

  <dependencies>
    - No blocking upstream. Execute immediately on GO receipt.
    - Blocks: .038 (COO-authored SWE-bench candidates land in benchmark/); .039 (CTO Case 4 + dev seeds land in both lanes).
    - Pilot wave 1 entries (bl-httpx-001, bl-click-001) already have baseline_commits locked — migration is field-additive, not field-rewriting.
  </dependencies>

  <operational_notes>
    - Operate from /c/Users/AndrewBerman/Desktop/feature_clb (COMP_LEARNS worktree). Confirm pwd before any edit.
    - Single commit is preferred. If you must split, keep each commit scoped to comp/backlog/** via `git commit --only -- comp/backlog/...`.
    - BACKLOG_V1 PRD is authoritative on schema fields. If a current YAML lacks a required field per §3 that cannot be recovered, mark status: candidate and flag in notes for CTO review at .039.
    - Do NOT invent baseline_commits. Both entries already have real commits pinned (f80cf4b0... for click).
    - If comp/backlog/backlog_schema.yaml exists and is redundant with BACKLOG_V1 PRD, delete it and note the deletion in commit message.
  </operational_notes>

  <closeout>
    On completion:
    - commit with --only --author="1.2.0_DS_CompLearns &lt;1.2.0_DS_CompLearns@opal.agent&gt;" -- comp/backlog/... files only
    - push to CLOUD
    - flip TO status to complete with commit ref in the XML comment
    - MCP COMPLETE to 2.1.0_SA_COO with commit sha — this authorizes .038 + .039 to begin
    - session log under org/tier2_senior/1.2.0_DS_CompLearns/logs/2026-04-22/ with Compiler Tools section
  </closeout>
</task_order>
