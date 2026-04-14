<task_order>
  <metadata>
    <id>0.4.0_DE_ClientPlatform-2026-04-13-reborn-w6-004</id>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_to>0.4.0_DE_ClientPlatform</issued_to>
    <date>2026-04-13</date>
    <status>complete</status>
    <project_code>ADVI_REBORN</project_code>
  </metadata>

  <references>
    <ref type="prd">docs/architecture/ADVI_REBORN_LEADERBOARD_FEES_ROLES_FIX.md</ref>
    <ref type="prior_work">W6-003 DS (D_00c role_combination_breakdown + D_04 passthrough)</ref>
  </references>

  <dependencies>
    <dependency agent="0.4.0_DS_ClientPlatform"
                task="ADVI_REBORN.W6-003.ds-d00c-role-combination-fee-breakdown"
                status="pending"
                description="DS ships D_00c + D_04 + regenerates platinum/firm/leaderboard.json with role_combination_breakdown. MCP message signals W6-004 GO."/>
  </dependencies>

  <objective>
    Update AdvisorsTab.tsx to consume `role_combination_breakdown` from the leaderboard
    artifact and compute fee-filtered role-subset AUA correctly. Remove the unsafe
    `?? data` fallback that causes fee filters to silently revert to all-fee totals
    when a role filter is also active.
  </objective>

  <context>
    Root cause (from PRD addendum):
    - `AdvisorsTab.tsx` uses `const bucket = feeView === 'all' ? data : (data[feeView] ?? data)`.
    - When `data[feeView]` (i.e. `data.fee_paying` or `data.no_fee`) is missing from a role slice,
      the `?? data` fallback silently returns the all-fee partition — wrong result.
    - After DS W6-003, `platinum/firm/leaderboard.json` gains `role_combination_breakdown` on
      each advisor entry. Each combination key is "|".join(sorted(roles)), e.g. "architect",
      "architect|implementor", "consultant|implementor".

    Correct frontend aggregation rule (from W6-003 DS TO schema):
    ```typescript
    // For selected roles S and feeView F:
    const total = Object.entries(role_combination_breakdown)
      .filter(([key]) => key.split('|').some(r => selectedRoles.includes(r)))
      .reduce((sum, [, combo]) => sum + (combo[feeView]?.aua ?? 0), 0)
    ```
    This sums only over combinations that intersect the selected role set.
    When feeView === 'all', sum combo.aua (the combination total, not fee-partitioned).
    Each account counted once — the combination key ensures non-overlapping partition.

    Wait for DS W6-003 MCP signal before starting. Read the shipped
    `platinum/firm/leaderboard.json` Travis Penfield QTD entry to confirm
    `role_combination_breakdown` is present with at least 3 combination keys before writing code.

    Cross-domain: ADVI_OFFICE.W3 will also touch `types.ts`. Pull latest CLOUD before
    editing `types.ts` here. `AdvisorsTab.tsx` is NOT touched by any ADVI_OFFICE TO —
    safe to edit independently once W6-003 ships.
  </context>

  <compiler_tools_mandate>
    Phase 1 (before writing code — after DS W6-003 MCP signal):
    - `comp-transform schema-check AdvisorsTab` — confirm current rendered fields + type map.
    - Read Travis Penfield sample from platinum/firm/leaderboard.json:
      `aws s3 cp s3://opal-data-bd/platinum/firm/leaderboard.json - | python -c "import sys,json; d=json.load(sys.stdin); tp=[e for w in d['windows'] for e in w['entries'] if 'Travis' in e.get('name','')]; print(json.dumps(tp[0].get('role_combination_breakdown',{}), indent=2))"`

    Phase 2 (before committing):
    - Re-run `comp-transform schema-check AdvisorsTab` — confirm no new untyped fields.
    - Validate four-cell audit matrix manually:
      | Fees | Roles | Expected |
      |------|-------|----------|
      | All | all | ~427M |
      | All | Implementor off | ~394M |
      | Fee-Paying | all | ~341M |
      | Fee-Paying | Implementor off | <= 341M (NOT 394M) |
    - `bun run build` (or `bunx tsc -b`) — zero TypeScript errors.
    - `/frontend-dev` if artifact is live during the session.

    Phase 3 (after commit):
    - `comp-blast AdvisorsTab` — confirm blast radius unchanged.
    - Append to `org/compiler-tools-log.md`.
    - MCP message to 2.0.0_SA_COO: "W6-004 complete — four-cell matrix validated."
  </compiler_tools_mandate>

  <cross_domain_coordination>
    <shared_resource>portal/src/pages/AdvisorIntelligence/tabs/AdvisorsTab.tsx</shared_resource>
    <shared_resource>portal/src/pages/AdvisorIntelligence/types.ts</shared_resource>
    <also_in_to>ADVI_OFFICE.W3 (DE — will touch types.ts; NOT AdvisorsTab. Pull latest before editing types.ts here.)</also_in_to>
    <required_action>
      Do NOT start until DS W6-003 MCP GO signal received and leaderboard.json artifact
      confirmed to have role_combination_breakdown. Then edit AdvisorsTab.tsx only.
      Check `git status` before committing — do not sweep in-flight ADVI_OFFICE.W3 changes.
    </required_action>
  </cross_domain_coordination>

  <acceptance_criteria>
    1. Four-cell audit matrix correct:
       - Fees=Fee-Paying, Roles=all → ~341M (unchanged).
       - Fees=Fee-Paying, Roles=Implementor off → less than or equal to 341M (was 394M before fix).
    2. No code path falls back from `fee_paying`/`no_fee` to all-role totals.
    3. TypeScript build clean (`bun run build` zero errors).
    4. Session log records four-cell matrix values post-fix.
    5. MCP message to 2.0.0_SA_COO confirming matrix validated.
  </acceptance_criteria>

  <scope>
    <files>
      <file action="modify">portal/src/pages/AdvisorIntelligence/tabs/AdvisorsTab.tsx</file>
      <file action="modify" optional="true">portal/src/pages/AdvisorIntelligence/types.ts</file>
    </files>
    <out_of_scope>
      Backend scripts (DS W6-003 scope). DistributionTab (ADVI_OFFICE.W3 scope).
      NNA per combination (deferred per W6-003 TO out_of_scope).
    </out_of_scope>
  </scope>

  <deliverables>
    - Commit to portal DEV with DE author.
    - Session log with four-cell audit matrix + compiler tools section.
    - MCP message to 2.0.0_SA_COO.
  </deliverables>
</task_order>
