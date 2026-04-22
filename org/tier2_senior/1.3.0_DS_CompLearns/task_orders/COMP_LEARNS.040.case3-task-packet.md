<task_order>
  <metadata>
    <id>1.3.0_DS_CompLearns-2026-04-22-comp-learns-040-case3-task-packet</id>
    <issued_by>2.1.0_SA_COO</issued_by>
    <issued_to>1.3.0_DS_CompLearns</issued_to>
    <date>2026-04-22</date>
    <status>staged <!-- Gate: .039 CTO approval of Case 3 candidate. GO fires from COO after CTO approves. --></status>
    <project_code>COMP_LEARNS</project_code>
    <priority>P1 — required for Wave 2 formal scoring on SWE-bench Verified anchor case</priority>
  </metadata>

  <references>
    <ref type="prd">docs/architecture/COMP_LEARNS_BACKLOG_V1.md §7 (Case 3 recommendations) + §10 (TO decomposition)</ref>
    <ref type="prd">docs/architecture/COMP_LEARNS_PARALLELIZATION_V1.md §13 (task packet structure — Case 1/2 precedent)</ref>
    <ref type="existing_packets">comp/tasks/case-002-click-refactor/packet.yaml — canonical Case 2 packet template; mirror structure</ref>
    <ref type="existing_packets">comp/tasks/task-001-httpx-netrc-host-authority/packet.yaml — canonical Case 1 packet template</ref>
  </references>

  <objective>
    Author the task packet for Case 3 — a SWE-bench Verified Python case approved by CTO
    in .039. Packet goes at comp/tasks/{case3-id}/packet.yaml; {case3-id} follows the
    pattern case-003-{short-slug} where the slug reflects the underlying bug/feature.

    Explicitly in scope:

    1. Read the approved bl-sweb-*.yaml entry (landed in comp/backlog/benchmark/ via .039)
       to confirm: target repo, baseline_commit, archetype, harness_relevance rating,
       measurement_axes, SWE-bench instance_id.

    2. Clone the target repo at baseline_commit into a scratch location (NOT comp/targets/—
       use a /tmp or scratch-worktree location). Do not commit the clone. This is for
       reading the issue + test suite only.

    3. Author comp/tasks/case-003-{slug}/packet.yaml with all fields matching the Case 1/2
       pattern. Required fields (adapt from packet.yaml templates):
       - task_id, name, target, baseline_commit, archetype
       - issue_url, description (from SWE-bench instance metadata, NOT the gold patch)
       - ac_type + acceptance_criteria (derived from the failing tests in SWE-bench — at
         minimum, the test_patch tests must pass at the end of the run)
       - harness_exposure_profile, allowed_artifacts, wall_clock_max_sec, token_max
       - condition_a + condition_b descriptions (unaided + aided variants)
       - scorer_prompt_version, checklist_version (pin to current SC doctrine versions)
       - schema_version (match current)

    4. Do NOT copy SWE-bench `patch` or `test_patch` raw fields into the packet. These are
       gold data and must NOT reach DS during run. Exception: `test_patch` tests that
       define the PASS condition ARE visible to DS at run time (they are the acceptance
       criteria) — but they live in the repo's test suite, not in packet.yaml.

    5. Author any supporting fixtures the packet references:
       - comp/tasks/case-003-{slug}/gold/ folder if SC needs a local reference post-verdict
         (gold patch NOT committed here — held separately by CTO). Create the folder with a
         README.md explaining the gold-patch location convention, but no patch content.
       - comp/tasks/case-003-{slug}/ab_questions.yaml — stub allowed for Wave 2 if Archetype
         A/D case without AB component, but include the file so schema is uniform.

    6. pytest comp/ -q passes (no regressions from new packet file).

    Explicitly out of scope:
    - Authoring a new harness (comp/targets/) for the SWE-bench target repo — if that
      repo is NOT already covered by a comp/targets/ harness, flag to COO and pause. A new
      harness is a separate TO (likely .046+).
    - Running the Case 3 gold survey (that is pilot-runner scope on a future TO).
    - Modifying Case 1/2 packets.
    - Committing SWE-bench gold patches (CTO-held).

    If the approved Case 3 repo has no existing harness under comp/targets/, STOP: MCP COO
    with the gap. A harness TO precedes packet authoring in that case.
  </objective>

  <compiler_tools_mandate>
    <phase id="1" when="before write">
      <step>
        <run>comp-build && pytest comp/ -q</run>
        <expect>Clean baseline before any packet authoring.</expect>
        <if_mismatch>Rebase or fix unrelated red first.</if_mismatch>
      </step>
      <step>
        <run>cat comp/backlog/benchmark/bl-sweb-*.yaml | head -50</run>
        <expect>CTO-approved Case 3 entry present with baseline_commit + archetype + harness_relevance populated. Exactly one bl-sweb-* with status: approved.</expect>
        <if_mismatch>STOP. MCP COO — .039 has not landed or approval is missing. Do not proceed.</if_mismatch>
      </step>
      <step>
        <run>ls comp/targets/</run>
        <expect>Directory for approved Case 3 repo exists (e.g. comp/targets/requests/ if Case 3 targets requests).</expect>
        <if_mismatch>STOP. MCP COO — harness authoring precedes packet authoring; separate TO required.</if_mismatch>
      </step>
    </phase>
    <phase id="2" when="before commit">
      <step>
        <run>python -c "import yaml; p = yaml.safe_load(open('comp/tasks/case-003-{slug}/packet.yaml')); assert 'task_id' in p; assert 'baseline_commit' in p; assert 'archetype' in p; assert 'acceptance_criteria' in p; print('schema ok')"</run>
        <expect>Prints "schema ok". All required fields present.</expect>
        <if_mismatch>Fix missing fields. Do NOT commit partial packet.</if_mismatch>
      </step>
      <step>
        <run>diff &lt;(yq eval 'keys' comp/tasks/case-003-{slug}/packet.yaml) &lt;(yq eval 'keys' comp/tasks/case-002-click-refactor/packet.yaml)</run>
        <expect>Key diff is EMPTY or only adds SWE-bench-specific fields (swe_bench_id, etc.). Core schema matches Case 1/2 pattern.</expect>
        <if_mismatch>Align schema with Case 1/2 before commit. Diverging schema breaks SC hygiene and .043 wave-runner routing.</if_mismatch>
      </step>
      <step>
        <run>.tools/ds-commit-gate.sh comp/tasks/case-003-{slug}/*.yaml</run>
        <expect>Exit 0 (YAMLs parse clean).</expect>
        <if_mismatch>Fix reported issue before commit.</if_mismatch>
      </step>
      <step>
        <run>pytest comp/ -q</run>
        <expect>GREEN — new packet file does not regress anything.</expect>
        <if_mismatch>Investigate. Fix. Do not commit red.</if_mismatch>
      </step>
    </phase>
    <phase id="3" when="after commit">
      <step>
        <run>comp-build</run>
        <expect>Clean rebuild. No stale-cache warnings.</expect>
        <if_mismatch>Surface to COO.</if_mismatch>
      </step>
    </phase>
  </compiler_tools_mandate>

  <cross_domain_coordination>
    <note>.041 (Case 4 packet, 1.1.0_DS) is parallel to this TO. Both are gated on .039. Neither TO modifies the other's packet. SC (2.1.0_SC_CompLearns) observes packet structure hygiene per the extended 15-item checklist — if your packet diverges from Case 1/2 schema in a material way, SC will flag to COO before wave runner dispatches events against it. Mirror the existing pattern.</note>
    <shared_artifacts>comp/backlog/benchmark/bl-sweb-*.yaml (read-only); comp/tasks/case-003-{slug}/packet.yaml (created by this TO)</shared_artifacts>
  </cross_domain_coordination>

  <acceptance_criteria>
    1. comp/tasks/case-003-{slug}/packet.yaml exists with all required schema fields populated (matches Case 1/2 pattern).
    2. task_id, baseline_commit, archetype, harness_relevance match the CTO-approved bl-sweb-*.yaml entry exactly.
    3. acceptance_criteria section explicitly documents: "SWE-bench test_patch tests must pass" (or equivalent — the defined PASS condition).
    4. No SWE-bench `patch` or `test_patch` raw content committed.
    5. comp/tasks/case-003-{slug}/ab_questions.yaml exists (stub OK for Archetype A/D).
    6. pytest comp/ -q GREEN.
    7. Commit under --author=1.3.0_DS_CompLearns@opal.agent with --only pathspec scoped to comp/tasks/case-003-{slug}/**.
    8. Pushed to CLOUD.
    9. Session log at org/tier2_senior/1.3.0_DS_CompLearns/logs/2026-04-22/ (or actual date) with Compiler Tools section.
    10. MCP COMPLETE to 2.1.0_SA_COO with commit sha + case-003 slug chosen.
  </acceptance_criteria>

  <dependencies>
    - Gate: .039 (CTO Case 3 approval + bl-sweb-*.yaml ship). Do NOT begin until CTO posts approval evidence in bl-sweb-*.yaml status: approved.
    - Gate: harness under comp/targets/ for approved Case 3 target repo. If absent, this TO pauses and a harness TO is authored first.
    - Blocks: Wave 2 formal scoring of Case 3 (can't dispatch a run without a packet).
  </dependencies>

  <operational_notes>
    - Operate from /c/Users/AndrewBerman/Desktop/feature_clb. Confirm pwd.
    - Mirror Case 2 packet (comp/tasks/case-002-click-refactor/packet.yaml) structure closely — divergence breaks SC hygiene + wave-runner routing.
    - Clone target repo to scratch (e.g. /tmp/case-003-scratch) for reading the issue + test suite only. Do NOT commit scratch clone.
    - If you need to query SWE-bench dataset for instance metadata: use HuggingFace datasets library (installed locally) — dataset = datasets.load_dataset("SWE-bench/SWE-bench_Verified"). Field `instance_id` maps to `swe_bench_id`; `base_commit` maps to `baseline_commit`.
    - Gold patch (SWE-bench `patch` field) is CTO-held — do NOT commit it in this packet or any file.
    - No emojis.
  </operational_notes>

  <closeout>
    On completion:
    - commit with --only --author="1.3.0_DS_CompLearns &lt;1.3.0_DS_CompLearns@opal.agent&gt;" -- comp/tasks/case-003-{slug}/...
    - push to CLOUD
    - flip TO status to complete with commit ref
    - MCP COMPLETE to 2.1.0_SA_COO with sha + slug
    - session log with Compiler Tools section
  </closeout>
</task_order>
