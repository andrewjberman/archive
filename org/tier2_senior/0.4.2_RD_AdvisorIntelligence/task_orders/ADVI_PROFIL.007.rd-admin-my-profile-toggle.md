<task_order>
  <metadata>
    <id>2.0.0_SA_COO-2026-04-10-profil-admin-my-profile</id>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_to>0.4.2_RD_AdvisorIntelligence</issued_to>
    <date>2026-04-10</date>
    <status>staged</status>
    <project_code>ADVI_PROFIL</project_code>
  </metadata>

  <objective>
    Add an optional "My Profile" button to the `BooksTab` header (Tab 3 admin landing) that, when clicked, renders the admin's own `AdvisorPublicProfile` inline with `showBackButton={true}`. The button only appears when `claims.advisorId` is non-null — i.e., when the admin user is also an advisor (external firm-admin who is also a book-owner). Wave 4 polish. Blocked on .002 (JWT advisorId claim).
  </objective>

  <context>
    RD briefing §5.5: Deferred during design. Internal Opal admin users do not have an `advisorId` and never need this. External firm-admin users who are also advisors benefit from a shortcut from the firm BooksTab landing directly to their own Profile without having to navigate the leaderboard drill chain.

    UX: A button in the `BooksTab` header (where the firm overview panels live) labeled "My Profile" or similar. Clicking it swaps the BooksTab body out and renders `<AdvisorPublicProfile advisorId={claims.advisorId} showBackButton={true} onBack={() => setViewMode('landing')}>` in-place. The back button returns to the BooksTab landing. Not a tab switch, not a cross-tab nav.

    The `showBackButton={true}` prop was explicitly added to `AdvisorPublicProfile.tsx` in .001 precisely for this use case — the non-admin Tab 3 path uses `showBackButton={false}` because the admin user has a tab bar to navigate, whereas the admin My Profile shortcut needs a back path.

    Claim gate: the button MUST only render when `claims.advisorId` is non-null. Internal Opal admin users (firmId="OPAL", no advisor mapping) will never see the button. Admin users with an advisor identity (rare but valid) see the shortcut.

    Low priority. This is polish, not a blocker for any other workstream.
  </context>

  <compiler_tools_mandate>
    Phase 1 (before writing):
    - Verify .002 has landed (`portal-auth-v1.11.{N}` deployed + AuthContext.context.ts Claims interface updated with `advisorId`).
    - Verify .001 has landed (AdvisorPublicProfile.tsx has `showBackButton?: boolean` prop).
    - Read `portal/src/pages/AdvisorIntelligence/tabs/ClientsTab.tsx` (BooksTab) header region to find the right insertion point for the button.
    - Read `AdvisorPublicProfile.tsx` to confirm `showBackButton` + `onBack` props work as expected.

    Phase 2 (during implementation):
    - Add a local state hook in BooksTab: `const [viewMode, setViewMode] = useState<'landing' | 'my-profile'>('landing')`.
    - Add the button in the header, gated on `claims.advisorId != null`. Use existing button styles (match the canonical ToggleGroup or button variants already in the page).
    - When `viewMode === 'my-profile'`, render `<AdvisorPublicProfile advisorId={claims.advisorId} showBackButton={true} onBack={() => setViewMode('landing')}>` in place of the BooksTab landing content.
    - When `viewMode === 'landing'`, render the existing BooksTab landing unchanged.

    Phase 3 (after implementation):
    - `bun run tsc -b` exit 0
    - `bun run eslint` clean
    - `comp-transform fields ClientsTab` — verify the added conditional render is picked up and no other fields are affected.
    - Manual test: log in as an admin user WITH an advisor identity (Andrew provides test account), confirm the button appears. Log in as an internal Opal admin (no advisor), confirm the button is absent.
    - RD does NOT push. Hand off to DT.
  </compiler_tools_mandate>

  <cross_domain_coordination>
    shared_resource: `portal/src/contexts/AuthContext.context.ts` — reads `claims.advisorId` (added in .002).
    shared_resource: `AdvisorPublicProfile.tsx` — uses `showBackButton={true}` + `onBack` (added in .001).
    shared_resource: `tabs/ClientsTab.tsx` (BooksTab) — .005 may also touch this file for the L3/L4 extract. Ordering: .007 can run in parallel with .005 as long as .001 has landed. If a merge conflict arises, .005 typically wins (it's the larger refactor); .007 rebases on top.
    last_write_owner: 0.4.2_RD_AdvisorIntelligence.
    required_action: "Wait for .002 + .001. Can run in parallel with .005 (merge conflict risk is low because .007 only touches the header region)."
  </cross_domain_coordination>

  <acceptance_criteria>
    1. **Button visibility:** Appears only when `claims.advisorId != null`. Admin user without advisor identity never sees it.
    2. **Button behavior:** Clicking swaps BooksTab body to render own AdvisorPublicProfile with `showBackButton={true}`. Back button returns to BooksTab landing.
    3. **Not a tab switch:** No navigation to Profile tab. No URL change. Pure local state flip inside BooksTab.
    4. **Existing BooksTab landing unchanged** when `viewMode === 'landing'`.
    5. **tsc + eslint clean.**
    6. **Manual test:** Admin-with-advisor sees button, internal Opal admin does not. Logged in session log with the test account identifiers (redacted).
    7. **Session log:** Documents the button location, the state hook, the test matrix, and the Compiler Tools section.
    8. **Handoff to DT:** Broker message for commit+push.
  </acceptance_criteria>

  <scope>
    <files>
      <file action="modify">portal/src/pages/AdvisorIntelligence/tabs/ClientsTab.tsx (BooksTab header + conditional render)</file>
      <file action="reference">portal/src/pages/AdvisorIntelligence/AdvisorPublicProfile.tsx</file>
      <file action="reference">portal/src/contexts/AuthContext.context.ts</file>
    </files>
  </scope>

  <requirements>
    <requirement id="1">Do NOT start until .002 is fully deployed and .001 is on portal DEV.</requirement>
    <requirement id="2">Button MUST be gated on `claims.advisorId != null`. Do not render for internal Opal admins.</requirement>
    <requirement id="3">Use existing button/toggle styles. Do not introduce new design system components.</requirement>
    <requirement id="4">Do NOT commit or push. Hand off to DT.</requirement>
    <requirement id="5">Low priority — safe to defer if higher-priority ADVI_PROFIL or ADVI_49PUSH work appears.</requirement>
  </requirements>

  <deliverables>
    <deliverable type="code">ClientsTab.tsx modified in the working tree, staged for DT commit+push.</deliverable>
    <deliverable type="document">Session log at `org/tier2_senior/0.4.2_RD_AdvisorIntelligence/logs/2026-04-{NN}/advi_profil_007_admin_my_profile.md`.</deliverable>
    <deliverable type="message">Broker message to 0.4.0_DT_ClientPlatform.</deliverable>
  </deliverables>

  <do_not>
    <rule>Do NOT start before .002 lands.</rule>
    <rule>Do NOT make this a tab switch or URL change. Local state only.</rule>
    <rule>Do NOT render the button for internal Opal admins.</rule>
    <rule>Do NOT commit or push.</rule>
  </do_not>
</task_order>
