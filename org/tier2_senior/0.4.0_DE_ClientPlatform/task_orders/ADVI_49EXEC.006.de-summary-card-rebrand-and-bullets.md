<task_order>
  <metadata>
    <id>ADVI_49EXEC.006</id>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_to>0.4.0_DE_ClientPlatform</issued_to>
    <date>2026-04-15</date>
    <status>staged</status><!-- Can parallelize with DS/DT against stub artifact bullets:[] per PRD §11 -->
    <project_code>ADVI_49EXEC</project_code>
    <priority>P1 (FE surface; ships against stub initially, real artifact lands when TO 2 ships)</priority>
  </metadata>

  <references>
    <ref type="prd">docs/architecture/ADVI_49EXEC.md §2 (surface change) + §3 (schema) + §7 TO 6</ref>
    <ref type="file">portal/src/pages/AdvisorIntelligence/AdvisorPublicProfile.tsx (SummaryCard at L267-end, title at L351)</ref>
    <ref type="file">portal/src/lib/api/types.ts (add AdvisorExecSummary type)</ref>
  </references>

  <objective>
    1. Rename `SummaryCard` panel title `"Summary"` → `"Executive Summary"` (L351 per PRD).
    2. Add new `<ExecutiveSummaryBullets />` component as the first child of `<PanelContent>` (above the existing Hero + tiles, line ~355). Renders 4-6 bullets per PRD §3 schema; each bullet = icon + headline + one-line detail.
    3. New React Query hook `useAdvisorExecSummary(advisorId, firmOverride)` colocated with existing `useQuery` calls in SummaryCard. Fetches `/api/scoped/advisor-intelligence/platinum/advisors/{id}/exec_summary.json`.
    4. Empty/loading: skeleton (4 placeholder rows) on loading; empty-array (NO error banner) on 404. The 404 case is "first night this advisor exists, no insights yet" — must not throw.
    5. Add new TS type `AdvisorExecSummary` to `portal/src/lib/api/types.ts` per PRD §3 schema.
    6. Existing Hero/AUA/flows/fee tiles push down (no other layout change in v1).

    **Stub-first development per PRD §11:** Ship FE against `bullets: []` empty array fixture (renders empty-state path) so DS/DT TO 1/2/4/7 don't gate FE. Real artifact lands when TO 2 ships and nightly produces.

    Out of scope v1: Refresh button, per-bullet click-through (`cta_path` field exists in schema for v1.5), user-level dismiss/customization.
  </objective>

  <scope>
    <files>
      <file action="modify">portal/src/pages/AdvisorIntelligence/AdvisorPublicProfile.tsx</file>
      <file action="modify">portal/src/lib/api/types.ts</file>
      <file action="create">portal/src/components/ExecutiveSummaryBullets.tsx (or inline if SummaryCard convention)</file>
      <file action="create">portal/.frontend-dev/testing/exec_summary_panel.json (constitution per PRD acceptance #6)</file>
    </files>
  </scope>

  <wire_contract>
    Endpoint: GET `/api/scoped/advisor-intelligence/platinum/advisors/{id}/exec_summary.json`. Type: `AdvisorExecSummary` (matches PRD §3 schema). Query key: `['advisor-exec-summary', advisorId, firmOverride]`. Fallbacks: skeleton on loading, empty-no-banner on 404.
  </wire_contract>

  <acceptance_criteria>
    1. Panel title renders "Executive Summary".
    2. Bullets render in order; up to 6, floor of 4 (some advisors will legitimately have <4 triggered slots — empty-state acceptable per PRD §3).
    3. Skeleton on loading, empty-no-banner on 404 (verified by intentionally fetching nonexistent advisor).
    4. New TS type `AdvisorExecSummary` in types.ts matches PRD §3 schema exactly.
    5. New query key `['advisor-exec-summary', advisorId, firmOverride]` does not collide with existing keys.
    6. `/frontend-dev` constitution `exec_summary_panel.json` ships with 4-6-bullet acceptance; passes 5/5 iterations against stub artifact AND (post-TO 2 deploy) against live nightly artifact.
    7. Session log Compiler Tools section reproduces every `<run>` + observed + pass/fail.
    8. MCP COMPLETE to COO with commit hash, screenshot evidence of: skeleton state, empty state, populated state (with stub).
  </acceptance_criteria>

  <compiler_tools_mandate>
    <phase id="1" when="before write — auto-rule">
      <step>
        <run>comp-cache collisions</run>
        <expect>New key `['advisor-exec-summary', advisorId, firmOverride]` does not collide with existing keys.</expect>
        <if_mismatch>Pick non-colliding key; document.</if_mismatch>
      </step>
      <step>
        <run>comp-transform schema-check AdvisorPublicProfile --feature exec</run>
        <expect>No UNUSED fields named `exec_summary*` slipped in. Confirms clean type addition.</expect>
        <if_mismatch>Investigate.</if_mismatch>
      </step>
    </phase>
    <phase id="2" when="before commit">
      <step>
        <run>comp-transform fields AdvisorPublicProfile</run>
        <expect>New bullets render every type field declared in AdvisorExecSummary.</expect>
        <if_mismatch>Add missing render or narrow type.</if_mismatch>
      </step>
      <step>
        <run>cd portal &amp;&amp; bunx tsc -b</run>
        <expect>TypeScript build clean.</expect>
        <if_mismatch>Fix.</if_mismatch>
      </step>
    </phase>
    <phase id="3" when="after merge">
      <step>
        <run>/frontend-dev exec_summary_panel.json</run>
        <expect>5/5 iterations PASS against stub artifact (empty bullets array → empty-no-banner; 4-bullet stub → 4 bullets render; 6-bullet stub → 6 bullets render with icons).</expect>
        <if_mismatch>Iterate constitution + component until PASS.</if_mismatch>
      </step>
    </phase>
  </compiler_tools_mandate>

  <cross_domain_coordination>
    - Reads `platinum/advisors/{id}/exec_summary.json` produced by TO 2 (DS).
    - Schema contract: PRD §3.
    - Stub-first development (`bullets: []`) decouples FE from DS/DT timing.
  </cross_domain_coordination>

  <dependencies>
    <none/><!-- Stub-first; real artifact landing is followup verification, not blocker -->
  </dependencies>

  <next>
    TO 6 close → final FE verification rerun after TO 2 ships first nightly artifact (5/5 PASS against live data).
  </next>
</task_order>
