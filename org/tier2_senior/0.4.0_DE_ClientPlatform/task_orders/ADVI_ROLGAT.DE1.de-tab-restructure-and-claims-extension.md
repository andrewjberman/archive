<task_order>
  <metadata>
    <id>0.4.0_DE_ClientPlatform-2026-04-17-advi-rolgat-de1</id>
    <issued_by>0.4.0_DE_ClientPlatform</issued_by>
    <issued_to>0.4.0_DE_ClientPlatform</issued_to>
    <date>2026-04-17</date>
    <status>complete</status>
    <project_code>ADVI_ROLGAT</project_code>
  </metadata>

  <objective>
    Restructure `AdvisorIntelligence.tsx` so that non-admin users see only `Advisors | Profile` tabs (admins retain `Distribution | Advisors | Books`). Every non-admin advisor role gets the Profile/Book toggle; Book content differs by payload (implementor = overview only, consultant/local_ops/architect = full book, architect + drill). Extend `Claims` with `advisorRole` and add 4 helper methods (`canSeeClientList`, `canDrillToClient`, `canDrillToAccount`, `canDrillIntoOtherAdvisor`) that RD1 depends on. Extend `devBypass` with a role picker so any of the 4 roles can be simulated locally without a live JWT.
  </objective>

  <context>
    PRD: `docs/architecture/ADVI_ROLGAT_PRD.md` r2 (2026-04-17) — sections 2, 5a, 5b, 5c. READ r2 — supersedes r1. Andrew resolved the three open questions: 4-role enum (no additional_advisor), local_ops = RCU Implementor + Local Ops SL populated only, architects DO NOT cross-advisor-drill.

    Current shape (reference):
    - `portal/src/contexts/AuthContext.context.ts` — Claims interface. Today: `{ firmId, userType, advisorId, firmRole }`.
    - `portal/src/contexts/AuthContext.tsx` — provider. Has `isInternal`, `isAdmin`, `isDev`, `hasAccess`, `canAccessFirm`, `canSeeCleartext`.
    - `portal/src/pages/AdvisorIntelligence/AdvisorIntelligence.tsx` — L175 computes `isFirmAdmin = internal || claims?.firmRole === 'admin'`. L225–270 renders 3-tab nav + tab3 flip. You restructure both.
    - `portal/src/pages/AdvisorIntelligence/components/PartnerAnalytics.tsx` — always-visible today. Stays visible for all non-admin users (L0 applies to everyone authenticated).

    Dependency: DT1 emits `advisorRole` claim. Can develop against `devBypass` initially; final pass must verify live JWT end-to-end.

    Frontend simplification from r2: PartnerAnalytics is visible to ALL authenticated users (no more hide-for-local_ops logic). Profile/Book toggle is visible to ALL non-admin advisor roles. Book content differences come from the BACKEND payload strip (DT1), not frontend logic — if `clients` array is absent, ClientListPanel just doesn't render (already guarded with `?.`).

    Cross-advisor drill (leaderboard advisor-card click) is ADMIN-ONLY. Architects do NOT drill into other advisors. Set `canDrillIntoAdvisor` on AdvisorsTab to `isFirmAdmin`, not `isFirmAdmin || architect`.
  </context>

  <compiler_tools_mandate>
    Phase 1 — before writing (note: this TO adds new values to a TypeScript union type AND adds new role-based routing, so the schema-check + ternary-audit pair from TO_PROTOCOL §SPECIAL CASE applies):
      <run>comp-transform schema-check AdvisorIntelligence --feature advisorRole</run>
      <expect>0 feature-relevant WARN entries before you start (no pre-existing advisorRole fields rendered). Baseline.</expect>
      <if_mismatch>If advisorRole already appears as UNUSED somewhere, verify it's not a stub from a prior session.</if_mismatch>

      <run>comp-transform ternary-audit AdvisorIntelligence</run>
      <expect>Capture current set of role-branching ternaries. After Phase 2 re-run must show 0 gaps on your new advisorRole ternaries.</expect>
      <if_mismatch>Document pre-existing gaps — they are not yours to fix.</if_mismatch>

      <run>comp-blast component:portal/src/pages/AdvisorIntelligence/AdvisorIntelligence.tsx</run>
      <expect>Downstream consumers of this component (App.tsx route). Snapshot the number.</expect>
      <if_mismatch>n/a — orientation only.</if_mismatch>

      <run>comp-transform schema-check PartnerAnalytics</run>
      <expect>Pre-existing MISSING `period` field at L454 — NOT your scope, leave alone. Do not introduce new MISSING.</expect>
      <if_mismatch>If you break PartnerAnalytics (unrelated to advisorRole), revert.</if_mismatch>

    Phase 2 — before committing:
      <run>comp-transform schema-check AdvisorIntelligence --feature advisorRole</run>
      <expect>0 WARN on advisorRole-prefixed fields. All new role helpers referenced in code are present in Claims type.</expect>
      <if_mismatch>Fix before commit. UNUSED advisorRole = routing ternary missing a branch per TO_PROTOCOL §SPECIAL CASE.</if_mismatch>

      <run>comp-transform ternary-audit AdvisorIntelligence</run>
      <expect>0 new gaps introduced by your changes. Pre-existing gaps unchanged.</expect>
      <if_mismatch>Each new gap = a role where the ternary silently falls to the wrong else. Fix all before commit.</if_mismatch>

      <run>bunx tsc -b</run>
      <expect>Exit 0, no type errors.</expect>
      <if_mismatch>Fix types. Likely culprit: forgetting `null` in the advisorRole union somewhere.</if_mismatch>

      <run>bun run build</run>
      <expect>Exit 0.</expect>
      <if_mismatch>Fix before commit.</if_mismatch>

    Phase 3 — after committing:
      <run>comp-blast component:portal/src/pages/AdvisorIntelligence/AdvisorIntelligence.tsx</run>
      <expect>Unchanged from Phase 1.</expect>
      <if_mismatch>Flag to 0.4.0_DE (self) / RD1.</if_mismatch>

      <run>/frontend-dev advi_role_architect</run>
      <expect>PASS in ≤ 2 iterations. Uses devBypass('architect'). Constitution shipped by RD1 — if RD1 has not landed yet, run a minimal stub constitution (`advi_role_de1_smoke.json`) asserting the tab layout flip only. RD1's five role constitutions come in a later pass.</expect>
      <if_mismatch>Iterate. If 5 iterations without PASS, flag via MCP.</if_mismatch>
  </compiler_tools_mandate>

  <cross_domain_coordination>
    shared_resource: `portal/src/pages/AdvisorIntelligence/types.ts`
    also_in_to: ADVI_ROLGAT.RD1
    last_write_owner: 0.4.0_DE (DE1 first, RD1 rebases)
    required_action: DE1 commits any types.ts changes before RD1 starts. RD1 MCPs DE1 if types.ts additions are needed mid-stream.

    shared_resource: `portal/src/contexts/AuthContext.tsx` + `portal/src/contexts/AuthContext.context.ts`
    also_in_to: (none — DT1 explicitly excluded from editing these files)
    last_write_owner: 0.4.0_DE
    required_action: DE1 owns these files end-to-end. If DT1 emits a different enum than PRD §2, DE1 is responsible for reconciling (and MCP'ing DT to fix upstream).

    shared_resource: JWT claim shape / DynamoDB partner table schema
    also_in_to: ADVI_ROLGAT.DT1
    last_write_owner: 0.4.0_DT
    required_action: DE1 reads DT1's emitted claim shape before merging. Do not deploy the portal until the JWT from `/auth/me` actually carries `advisorRole` in dev — otherwise the devBypass path ships untested against real claims.
  </cross_domain_coordination>

  <acceptance_criteria>
    1. `Claims` interface (AuthContext.context.ts) includes `advisorRole: AdvisorRole | null` with `AdvisorRole` exported. Exact union: `'architect' | 'consultant' | 'local_ops' | 'implementor'` (4 values, no additional_advisor).
    2. `AuthContextType` adds `advisorRole: () => AdvisorRole | null`, `canSeeClientList: () => boolean`, `canDrillToClient: () => boolean`, `canDrillToAccount: () => boolean`, `canDrillIntoOtherAdvisor: () => boolean`. Admin-bypass short-circuits each to true when `isAdmin()` or `isInternal()`.
    3. `parseClaims` parses `advisorRole`. Unknown values → null. String 'null' → null. Cover all four enum values + null.
    4. `devBypass` accepts optional `advisorRole` and `firmRole` args. Default unchanged (admin).
    5. AdvisorIntelligence.tsx: when `isFirmAdmin` is false, `TabNavigation` renders only `Advisors` and `Profile` (Distribution removed). When `isFirmAdmin` is true, unchanged.
    6. Profile tab (non-admin): render Profile/Book toggle for ALL advisor roles (no per-role hiding). Book path renders `AdvisorBookView`. Backend payload strip determines Book content — your job is only to mount the component.
    7. PartnerAnalytics header visible for ALL non-admin users (no advisorRole-based hiding).
    8. Leaderboard `canDrillIntoAdvisor` prop wired to `canDrillIntoOtherAdvisor()` helper (admin-only). Architects cannot drill into other advisor cards.
    9. `comp-transform schema-check AdvisorIntelligence --feature advisorRole`: 0 feature-relevant WARN.
    10. `comp-transform ternary-audit AdvisorIntelligence`: 0 new gaps.
    11. `bun run build` exits 0.
    12. `/frontend-dev advi_role_de1_smoke` PASS — constitution asserts 5 cases: admin (3 tabs), implementor/consultant/local_ops/architect (2 tabs each).
    13. Session log with Compiler Tools table.
    14. MCP COMPLETE to 0.4.2_RD citing commit hash + helper signatures.
  </acceptance_criteria>

  <scope>
    <files>
      <file action="modify">portal/src/contexts/AuthContext.context.ts</file>
      <file action="modify">portal/src/contexts/AuthContext.tsx</file>
      <file action="modify">portal/src/pages/AdvisorIntelligence/AdvisorIntelligence.tsx</file>
      <file action="modify">portal/src/pages/AdvisorIntelligence/components/PartnerAnalytics.tsx</file>
      <file action="modify">portal/src/pages/AdvisorIntelligence/types.ts</file>
      <file action="create">portal/.frontend-dev/testing/advi_role_de1_smoke.json</file>
      <file action="reference">docs/architecture/ADVI_ROLGAT_PRD.md</file>
    </files>
  </scope>

  <requirements>
    <requirement id="1">Claims type extension per PRD §5b. Export `AdvisorRole` as its own type for RD1 to import. Four values only.</requirement>
    <requirement id="2">Four new helper methods on AuthContextType per PRD §5b (advisorRole, canSeeClientList, canDrillToClient, canDrillToAccount, canDrillIntoOtherAdvisor — the last explicitly admin-only). Admin bypass short-circuits.</requirement>
    <requirement id="3">parseClaims handles all four enum values + null. Unknown string → null. Do NOT default to permissive.</requirement>
    <requirement id="4">devBypass(advisorRole?, firmRole?) accepts role params. When advisorRole is provided without firmRole, auto-set firmRole='user' and role='user' to simulate a partner-firm advisor.</requirement>
    <requirement id="5">AdvisorIntelligence.tsx: non-admin tab list = `[{id:'advisors',label:'Advisors'},{id:'profile',label:'Profile'}]`. Admin unchanged. Default activeTab = 'advisors' for non-admin.</requirement>
    <requirement id="6">Non-admin Profile tab: always render Profile/Book toggle (no per-role hiding). Profile = AdvisorPublicProfile. Book = AdvisorBookView.</requirement>
    <requirement id="7">PartnerAnalytics visible for all non-admin (and admin). No advisorRole-based gating of the header.</requirement>
    <requirement id="8">AdvisorsTab `canDrillIntoAdvisor` prop wired to `canDrillIntoOtherAdvisor()` (admin-only). Not `|| architect`.</requirement>
    <requirement id="9">AdvisorBookView replaces inline `isInternal() || claims?.firmRole === 'admin'` with `auth.canDrillToAccount()`. Do the helper swap only — RD1 owns the downstream component gating (ClientsTable onClick, AdvisorBookClientDetail account-row click, etc.).</requirement>
    <requirement id="10">Ship minimal self-test constitution `advi_role_de1_smoke.json` that toggles devBypass between admin and each of the 4 non-admin roles (5 test cases total) and asserts visible tab count + names. RD1 ships the full drill-state matrix later.</requirement>
  </requirements>

  <deliverables>
    <deliverable type="commit">portal DEV commit: Claims type + helpers + devBypass role picker + AdvisorIntelligence tab restructure + PartnerAnalytics gate + self-test constitution.</deliverable>
    <deliverable type="document">Session log at `org/tier2_senior/0.4.0_DE_ClientPlatform/logs/{YYYY-MM-DD}/advi_rolgat_de1.md` with Compiler Tools table and MCP dispatch/completion notes.</deliverable>
    <deliverable type="document">MCP COMPLETE to RD1 citing the Claims type commit hash + AdvisorRole enum shape + list of helpers RD1 can call from AuthContext.</deliverable>
  </deliverables>

  <do_not>
    <rule>Do NOT change admin tab layout. Distribution/Advisors/Books stays pixel-identical.</rule>
    <rule>Do NOT default null advisorRole to anything permissive. Null = most restrictive (same as local_ops).</rule>
    <rule>Do NOT remove the existing `canAccessFirm` / `hasAccess` / `canSeeCleartext` helpers. Additive only.</rule>
    <rule>Do NOT edit AdvisorBookView, AdvisorBookClientDetail, AdvisorBookAccountModal, ClientsTable drill-click logic — that is RD1's scope. You only touch the helper function they'll consume.</rule>
    <rule>Do NOT ship without `/frontend-dev advi_role_de1_smoke` PASS. Cosmetic-only gating breaks silently when the ternary misses a branch.</rule>
    <rule>Do NOT commit to portal PROD. DEV only. DT pushes after all wave commits are locally verified.</rule>
  </do_not>
</task_order>
