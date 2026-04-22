<task_order>
  <metadata>
    <id>1.1.0_DS_CompLearns-2026-04-22-comp-learns-041-case4-task-packet</id>
    <issued_by>2.1.0_SA_COO</issued_by>
    <issued_to>1.1.0_DS_CompLearns</issued_to>
    <date>2026-04-22</date>
    <status>complete <!-- Phase0 commit: 6706f333 (bl-httpx-002 baseline resolved). Packet commit: ecfdbd4e (case-004 authored). Pushed to CLOUD 2026-04-22. --></status>
    <project_code>COMP_LEARNS</project_code>
    <priority>P1 — Case 4 covers Archetype D (cross-module diagnosis), highest harness leverage for aided-vs-unaided</priority>
  </metadata>

  <references>
    <ref type="prd">docs/architecture/COMP_LEARNS_BACKLOG_V1.md §5 (Archetype D definition) + §7 (Case 4 recommendation — OSS historical, httpx or requests) + §10</ref>
    <ref type="prd">docs/architecture/COMP_LEARNS_PARALLELIZATION_V1.md §13 (task packet structure)</ref>
    <ref type="existing_packets">comp/tasks/task-001-httpx-netrc-host-authority/packet.yaml — Case 1 (Archetype A on httpx) — closest precedent for OSS historical pattern</ref>
    <ref type="existing_packets">comp/tasks/case-002-click-refactor/packet.yaml — alternate structural template</ref>
  </references>

  <objective>
    Author the task packet for Case 4 — an OSS historical cross-module diagnosis bug
    authored by CTO in .039 (bl-*.yaml entry in comp/backlog/benchmark/). Target is httpx
    or requests per BACKLOG_V1 §7.

    Explicitly in scope:

    1. Read the CTO-authored bl-*.yaml entry to confirm: target repo, baseline_commit,
       archetype (should be D — Cross-Module Failure Diagnosis), issue_url, measurement_axes,
       harness_relevance, harness_gap.

    2. Confirm harness coverage: if target is httpx, comp/targets/httpx/ already exists.
       If target is requests, comp/targets/requests/ must exist — if not, STOP and MCP COO
       (harness authoring precedes packet authoring).

    3. Read the source PR / issue at issue_url in a scratch clone of the target repo at
       baseline_commit. Identify:
       - The failing test(s) that exercise the bug (these become the PASS condition)
       - The root-cause module(s) vs. symptom module(s) (Archetype D requires the bug be
         diagnosable only via cross-module edge traversal — confirm this is true)
       - Any reasoning-quality audit hooks (post-verdict reasoning.md assessment lens)

    4. Author comp/tasks/case-004-{slug}/packet.yaml:
       - task_id, name, target, baseline_commit, archetype=D
       - issue_url, description (neutral — describes the symptom, NOT the fix)
       - ac_type = test_suite + reasoning quality score (post-verdict audit)
       - acceptance_criteria: failing test(s) must PASS at end of run; DS must NOT be
         told which modules to edit (cross-module diagnosis is the test)
       - harness_exposure_profile, allowed_artifacts, wall_clock_max_sec, token_max
       - condition_a (unaided) + condition_b (aided) descriptions
       - scorer_prompt_version, checklist_version, schema_version pinned
       - measurement_axes: reasoning_quality primary, aided-vs-unaided differentiation primary

    5. Author fixtures at comp/tasks/case-004-{slug}/:
       - ab_questions.yaml — Archetype D benefits from reasoning-quality AB questions; if
         CTO's bl-*.yaml includes harness_gap notes, seed 3-5 AB questions about the
         cross-module edge traversal. Otherwise stub with empty questions: [].
       - README.md describing the case (neutral, symptom-only framing).

    6. Do NOT commit gold patch (the real fix PR merged into the repo upstream). Reference
       via issue_url / gold_patch_url in the bl-*.yaml entry (CTO-held).

    7. pytest comp/ -q passes.

    Explicitly out of scope:
    - Authoring harness for a new target repo (separate TO if needed).
    - Running the Case 4 gold survey.
    - Modifying Case 1/2 packets.
    - Writing the fix patch (DS agents diagnose during run; they do not author the fix in the packet).
  </objective>

  <compiler_tools_mandate>
    <phase id="1" when="before write">
      <step>
        <run>comp-build && pytest comp/ -q</run>
        <expect>Clean baseline.</expect>
        <if_mismatch>Rebase / fix unrelated red first.</if_mismatch>
      </step>
      <step>
        <run>cat comp/backlog/benchmark/bl-*.yaml | grep -A2 "archetype: D"</run>
        <expect>At least one bl-*.yaml with archetype: D and status: approved (the CTO Case 4 entry from .039).</expect>
        <if_mismatch>STOP. MCP COO — .039 has not landed.</if_mismatch>
      </step>
      <step>
        <run>ls comp/targets/{target}/</run>
        <expect>Harness exists for the Case 4 target (comp/targets/httpx/ or comp/targets/requests/). Substitute {target} with the actual bl-*.yaml target field.</expect>
        <if_mismatch>STOP. MCP COO — harness authoring precedes packet. Separate TO required.</if_mismatch>
      </step>
    </phase>
    <phase id="2" when="before commit">
      <step>
        <run>python -c "import yaml; p = yaml.safe_load(open('comp/tasks/case-004-{slug}/packet.yaml')); assert p['archetype'] == 'D'; assert 'acceptance_criteria' in p; assert 'reasoning_quality' in p.get('measurement_axes', []); print('schema ok')"</run>
        <expect>Prints "schema ok". Archetype D + reasoning_quality axis confirmed.</expect>
        <if_mismatch>Fix packet before commit.</if_mismatch>
      </step>
      <step>
        <run>diff &lt;(yq eval 'keys' comp/tasks/case-004-{slug}/packet.yaml) &lt;(yq eval 'keys' comp/tasks/task-001-httpx-netrc-host-authority/packet.yaml)</run>
        <expect>Key set matches Case 1 pattern (Archetype A on OSS historical). Any additions are Archetype-D-specific (reasoning_audit_prompt, etc.).</expect>
        <if_mismatch>Align to Case 1 pattern.</if_mismatch>
      </step>
      <step>
        <run>.tools/ds-commit-gate.sh comp/tasks/case-004-{slug}/*.yaml</run>
        <expect>Exit 0.</expect>
        <if_mismatch>Fix before commit.</if_mismatch>
      </step>
      <step>
        <run>pytest comp/ -q</run>
        <expect>GREEN.</expect>
        <if_mismatch>Investigate. Fix.</if_mismatch>
      </step>
      <step>
        <run>grep -r "patch:" comp/tasks/case-004-{slug}/ 2>/dev/null || echo "CLEAN"</run>
        <expect>CLEAN — no patch content accidentally committed. Gold fix is CTO-held, not in packet.</expect>
        <if_mismatch>Remove patch content. Re-verify.</if_mismatch>
      </step>
    </phase>
    <phase id="3" when="after commit">
      <step>
        <run>comp-build</run>
        <expect>Clean rebuild.</expect>
        <if_mismatch>Surface to COO.</if_mismatch>
      </step>
    </phase>
  </compiler_tools_mandate>

  <cross_domain_coordination>
    <note>.040 (Case 3 packet, 1.3.0_DS) is parallel. Neither TO touches the other's packet. SC observes packet structure hygiene. If your Archetype D framing materially differs from Case 1's OSS-historical pattern (different ac_type, different axes emphasis), flag to COO — schema drift breaks wave-runner routing.</note>
    <shared_artifacts>comp/backlog/benchmark/bl-*.yaml Case 4 entry (read-only); comp/tasks/case-004-{slug}/** (created by this TO)</shared_artifacts>
  </cross_domain_coordination>

  <acceptance_criteria>
    1. comp/tasks/case-004-{slug}/packet.yaml authored with archetype=D + all required schema fields.
    2. acceptance_criteria explicitly cites the failing test(s) that pass at run end.
    3. measurement_axes includes reasoning_quality as primary.
    4. ac_type = test_suite + reasoning quality (post-verdict audit).
    5. No gold patch content committed anywhere in comp/tasks/case-004-{slug}/.
    6. pytest comp/ -q GREEN.
    7. Commit under --author=1.1.0_DS_CompLearns@opal.agent with --only pathspec scoped to comp/tasks/case-004-{slug}/**.
    8. Pushed to CLOUD.
    9. Session log with Compiler Tools section.
    10. MCP COMPLETE to 2.1.0_SA_COO with commit sha + case-004 slug.
  </acceptance_criteria>

  <dependencies>
    - Gate: .039 — CTO authors bl-*.yaml Case 4 entry. Do NOT begin until that ships.
    - Gate: harness at comp/targets/{target}/ exists.
    - Blocks: Wave 2 formal scoring of Case 4.
  </dependencies>

  <operational_notes>
    - Operate from /c/Users/AndrewBerman/Desktop/feature_clb. Confirm pwd.
    - Archetype D requires that diagnosis be cross-module — verify the bug cannot be
      localized by reading one file. If the CTO's bl-*.yaml is ambiguous on this, MCP
      CTO for confirmation before authoring.
    - Mirror Case 1 packet structure (OSS historical on httpx is closest precedent).
    - The AB questions in ab_questions.yaml (if populated) should probe cross-module
      reasoning — "which module owns X?" "how does edge A→B resolve?" — not test-pass
      questions.
    - Scratch clone of target repo at baseline_commit for issue reading only; do NOT commit.
    - Gold patch URL goes in the bl-*.yaml entry (CTO's file), not the packet.
    - No emojis.
  </operational_notes>

  <closeout>
    On completion:
    - commit with --only --author="1.1.0_DS_CompLearns &lt;1.1.0_DS_CompLearns@opal.agent&gt;" -- comp/tasks/case-004-{slug}/...
    - push to CLOUD
    - flip TO status to complete
    - MCP COMPLETE to 2.1.0_SA_COO with sha + slug
    - session log with Compiler Tools section
  </closeout>
</task_order>
