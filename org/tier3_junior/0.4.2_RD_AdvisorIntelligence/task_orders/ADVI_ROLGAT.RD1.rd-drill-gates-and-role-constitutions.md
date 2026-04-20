<task_order>
  <metadata>
    <id>0.4.0_DE_ClientPlatform-2026-04-17-advi-rolgat-rd1</id>
    <issued_by>0.4.0_DE_ClientPlatform</issued_by>
    <issued_to>0.4.2_RD_AdvisorIntelligence</issued_to>
    <date>2026-04-17</date>
    <status>complete</status>
    <project_code>ADVI_ROLGAT</project_code>
  </metadata>

  <objective>
    Gate drill surfaces in AdvisorBookView / ClientDetail / AccountModal / ClientsTable by `advisorRole`, using the AuthContext helpers DE1 lands first. Ship four per-role `/frontend-dev` constitutions covering implementor / consultant / local_ops / architect. Implementor Book renders overview only (backend strips client/cost-basis fields — frontend auto-hides panels via existing `?.` guards). Consultant and local_ops see full book but ClientsTable rows non-clickable. Architect sees full drill.
  </objective>

  <context>
    PRD: `docs/architecture/ADVI_ROLGAT_PRD.md` r2 (2026-04-17) — sections 2, 5a, 7a. READ r2 — supersedes r1. Andrew resolved the three open questions: 4-role enum (no additional_advisor), local_ops = RCU Implementor + Local Ops SL populated only, architects DO NOT cross-advisor-drill.

    Dependency: ADVI_ROLGAT.DE1 must land first. It ships:
    - `AdvisorRole` type export (4 values)
    - `advisorRole`, `canSeeClientList`, `canDrillToClient`, `canDrillToAccount`, `canDrillIntoOtherAdvisor` helpers on `useAuth()`
    - Claims.advisorRole field
    - `devBypass(advisorRole?, firmRole?)` extended signature

    Import helpers from `useAuth()`. DO NOT add your own role checks against `claims?.advisorRole` directly in components — that duplicates logic DE1 centralized.

    Current call sites that hard-code the old gate (`isInternal() || claims?.firmRole === 'admin'`):
    - `portal/src/pages/AdvisorIntelligence/AdvisorBookView.tsx` L72 — DE1 swaps this to `canDrillToAccount()`. You do NOT touch L72 — DE1 does. You touch everything else (ClientsTable row onClick, account-row click in ClientDetail, any other drill-state gate inside panels/). Grep first: `grep -rn "firmRole === 'admin'" portal/src/pages/AdvisorIntelligence/` and make sure nothing outside DE1's scope remains.

    Visual states RD1 owns (matches PRD §5a):
    - implementor: Book renders Overview panel only. ClientListPanel absent because backend stripped `clients` array. Cost-basis/tax/income panels absent because backend stripped those fields. Frontend does NOT need a separate "is implementor" check — use the existing `?.` guards already present in the book view. If your read of the component finds any panel NOT guarded, add the guard.
    - consultant / local_ops: Book = Overview + ClientListPanel + cost-basis panels. ClientsTable rows NON-clickable (no cursor-pointer, no onClick, no hover). Small Accounts By Role panel visible. Account drill hidden.
    - architect: ClientsTable rows clickable → ClientDetail opens. Account row clickable → AccountModal opens. Same as admin today.

    Frontend-dev constitutions live in `portal/.frontend-dev/testing/*.json`. Existing examples: `clients_panel.json`, `role_breakdown_small_accts.json`, `fee_summary_window.json`.
  </context>

  <compiler_tools_mandate>
    Phase 1 — before writing:
      <run>comp-transform schema-check AdvisorBookView</run>
      <expect>Baseline. Capture rendered_fields, no new MISSING will appear since you're adding role gating, not data fields.</expect>
      <if_mismatch>n/a orientation.</if_mismatch>

      <run>comp-transform fields AdvisorBookView</run>
      <expect>Inventory of rendered data fields. Role gating should not change this list.</expect>
      <if_mismatch>n/a orientation.</if_mismatch>

      <run>git log --oneline -5 portal/src/contexts/AuthContext.context.ts</run>
      <expect>Most recent commit should be from 0.4.0_DE_ClientPlatform landing DE1 (Claims.advisorRole + helpers). If not, DO NOT START — wait for DE1 MCP COMPLETE.</expect>
      <if_mismatch>Stop and MCP 0.4.0_DE asking for DE1 commit hash.</if_mismatch>

    Phase 2 — before committing:
      <run>comp-transform schema-check AdvisorBookView</run>
      <expect>Rendered fields unchanged from Phase 1 (you did not add data fields). 0 MISSING.</expect>
      <if_mismatch>Fix before commit.</if_mismatch>

      <run>comp-transform ternary-audit AdvisorBookView</run>
      <expect>0 gaps introduced by your role ternaries.</expect>
      <if_mismatch>Each gap = a role where the drill silently shows the wrong surface. Fix all before commit.</if_mismatch>

      <run>bun run build</run>
      <expect>Exit 0.</expect>
      <if_mismatch>Fix types.</if_mismatch>

    Phase 3 — after committing:
      <run>/frontend-dev advi_role_implementor</run>
      <expect>PASS. Profile/Book toggle visible. Book view = Overview panel only. ClientListPanel NOT rendered (backend stripped `clients`). Cost-basis / tax / income panels NOT rendered.</expect>
      <if_mismatch>If ClientListPanel appears when backend strips, the panel's visibility guard is wrong — add `?.` guard on `clients?.length`.</if_mismatch>

      <run>/frontend-dev advi_role_consultant</run>
      <expect>PASS. Profile/Book toggle visible. Book = Overview + ClientListPanel + cost-basis. ClientsTable rows NOT clickable (no cursor-pointer, no hover), Small Accounts by Role panel visible, account drill absent.</expect>
      <if_mismatch>Iterate until PASS, ≤ 5 iterations.</if_mismatch>

      <run>/frontend-dev advi_role_local_ops</run>
      <expect>PASS — identical surface to consultant.</expect>
      <if_mismatch>Iterate.</if_mismatch>

      <run>/frontend-dev advi_role_architect</run>
      <expect>PASS. Full drill: ClientsTable → ClientDetail → AccountModal. All three surfaces reachable and interactive. Advisors-tab leaderboard cards NOT clickable (cross-advisor drill is admin-only).</expect>
      <if_mismatch>Iterate.</if_mismatch>
  </compiler_tools_mandate>

  <cross_domain_coordination>
    shared_resource: `portal/src/pages/AdvisorIntelligence/types.ts`
    also_in_to: ADVI_ROLGAT.DE1
    last_write_owner: 0.4.0_DE (landed first)
    required_action: Rebase onto DE1's commit before starting. If you need a new type for a role-gated prop, MCP 0.4.0_DE and wait for a types.ts commit — do NOT add to types.ts from RD1.

    shared_resource: `portal/.frontend-dev/testing/advi_role_de1_smoke.json`
    also_in_to: ADVI_ROLGAT.DE1
    last_write_owner: 0.4.0_DE
    required_action: DE1's smoke constitution covers tab layout only. Your five role constitutions cover drill state. No overlap — DE1's file stays.
  </cross_domain_coordination>

  <acceptance_criteria>
    1. Every remaining hardcoded `isInternal() || claims?.firmRole === 'admin'` inside AdvisorIntelligence/ components replaced with `canDrillToAccount()` or `canDrillToClient()` from useAuth. No grep hits for the old pattern remain. Confirm: `grep -rn "firmRole === 'admin'" portal/src/pages/AdvisorIntelligence/` returns 0 lines.
    2. ClientsTable row `onClick` (and the row's `cursor-pointer` / hover visual) is conditional on `canDrillToClient()`. When false: no click handler, no hover effect, no cursor change. Small Accounts By Role panel still renders regardless.
    3. AdvisorBookClientDetail account-row click conditional on `canDrillToAccount()`. When false: no click, no hover.
    4. AdvisorBookAccountModal never opens for a role without `canDrillToAccount()`. Even if the modal is reached by URL manipulation (out of scope to block fully; backend tier gate is the real stop), the UI does not expose the trigger.
    5. Four `/frontend-dev` constitutions shipped: `advi_role_implementor.json`, `advi_role_consultant.json`, `advi_role_local_ops.json`, `advi_role_architect.json`. Each simulates devBypass with that role and asserts the visible surface per PRD §7a.
    6. All four constitutions PASS in ≤ 5 iterations each (document iteration counts in session log).
    7. `comp-transform schema-check AdvisorBookView` clean; `comp-transform ternary-audit AdvisorBookView` 0 new gaps.
    8. `bun run build` exits 0.
    9. Session log with Compiler Tools table.
    10. page_inventory.xml update if any new constitution file counts as a rendered artifact (follow existing convention — constitutions are test artifacts, likely not inventoried).
    11. MCP COMPLETE to 0.4.0_DE_ClientPlatform citing commit hash + five PASS lines + iteration counts.
  </acceptance_criteria>

  <scope>
    <files>
      <file action="modify">portal/src/pages/AdvisorIntelligence/AdvisorBookView.tsx</file>
      <file action="modify">portal/src/pages/AdvisorIntelligence/AdvisorBookClientDetail.tsx</file>
      <file action="modify">portal/src/pages/AdvisorIntelligence/AdvisorBookAccountModal.tsx</file>
      <file action="modify">portal/src/pages/AdvisorIntelligence/panels/ClientsTable.tsx</file>
      <file action="modify">portal/src/pages/AdvisorIntelligence/AdvisorPublicProfile.tsx</file>
      <file action="create">portal/.frontend-dev/testing/advi_role_implementor.json</file>
      <file action="create">portal/.frontend-dev/testing/advi_role_consultant.json</file>
      <file action="create">portal/.frontend-dev/testing/advi_role_local_ops.json</file>
      <file action="create">portal/.frontend-dev/testing/advi_role_architect.json</file>
      <file action="reference">docs/architecture/ADVI_ROLGAT_PRD.md</file>
    </files>
  </scope>

  <requirements>
    <requirement id="1">Replace every `isInternal() || claims?.firmRole === 'admin'` inside AdvisorIntelligence/ components with the appropriate canDrill helper. Grep-clean after commit.</requirement>
    <requirement id="2">ClientsTable: row-level gate as described. Non-clickable rows must still render all data (name, AUA, small-accts col, red row accent when small_account_count > 0). Only interactivity is removed.</requirement>
    <requirement id="3">AdvisorBookClientDetail: account row gate. If !canDrillToAccount(), render rows static, no chevron/click hint.</requirement>
    <requirement id="4">AdvisorPublicProfile: when used as the direct Profile surface for local_ops/additional_advisor (no Profile/Book toggle available per DE1), ensure no book-drill CTA is visible. Should already be clean — verify.</requirement>
    <requirement id="5">Four role constitutions using devBypass. Each asserts (a) Profile/Book toggle visible (always true for all 4 under r2), (b) presence/absence of ClientListPanel + cost-basis panels, (c) whether ClientsTable row click is interactive, (d) whether account drill is interactive, (e) leaderboard cross-advisor drill NOT interactive (all 4 non-admin roles).</requirement>
    <requirement id="6">Follow existing constitution schema (see `portal/.frontend-dev/testing/clients_panel.json` for reference). Use ACTIONABLE_FIXES block.</requirement>
  </requirements>

  <deliverables>
    <deliverable type="commit">portal DEV commit: drill gates across 5 files + 5 role constitutions.</deliverable>
    <deliverable type="document">Session log at `org/tier3_junior/0.4.2_RD_AdvisorIntelligence/logs/{YYYY-MM-DD}/advi_rolgat_rd1.md` with Compiler Tools table + five PASS rows + iteration counts.</deliverable>
    <deliverable type="document">MCP COMPLETE to 0.4.0_DE_ClientPlatform with commit hash and PASS matrix.</deliverable>
  </deliverables>

  <do_not>
    <rule>Do NOT duplicate role logic in components. Use `useAuth()` helpers. If a helper is missing, MCP DE1 — do not inline the check.</rule>
    <rule>Do NOT start until DE1 is COMPLETE. The Claims type + helpers are a hard dependency.</rule>
    <rule>Do NOT skip any of the five constitutions. The matrix is the whole point — five roles, four surfaces.</rule>
    <rule>Do NOT commit to portal PROD. DEV only.</rule>
    <rule>Do NOT ship if any of the five /frontend-dev runs fails after 5 iterations. MCP DE1 with ACTIONABLE_FIXES dump instead.</rule>
  </do_not>
</task_order>
