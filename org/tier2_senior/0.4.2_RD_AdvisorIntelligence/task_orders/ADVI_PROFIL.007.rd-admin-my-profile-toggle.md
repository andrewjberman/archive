<task_order>
  <metadata>
    <id>2.0.0_SA_COO-2026-04-10-profil-admin-my-profile</id>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_to>0.4.2_RD_AdvisorIntelligence</issued_to>
    <date>2026-04-10</date>
    <status>complete</status>
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

    **DECISION: SHIP.** Andrew confirmed via main chat on 2026-04-10, ~16:40 EDT, relayed by 0.4.0_DT_ClientPlatform ("yes we want the profile toggle"). All tech blockers are cleared: .001 landed (portal DEV 3e8cc3f — showBackButton prop live), .002 landed (portal DEV 65e411c + portal-auth-v1.11.7 — Claims.advisorId wired end-to-end and verified via curl for both Chase and Travis). The live test case for this TO is **travis.penfield@49financial.com** — partner-firm admin (`role=admin`, `firmId=49financial`) who is also a book-owner (`advisorId=travis_penfield`). His login flow already produces a JWT + /me response with `advisorId` populated, so the `claims.advisorId != null` gate will fire true for him on the BooksTab header.

    **Minor doc correction while here:** the first paragraph of context above says Internal Opal admin users have `firmId="OPAL"`. The actual canonical value is `firmId="opal-capital"` (verified via Chase + Travis login curl tests today and via `auth.ts:62` `if user.firmId !== 'opal-capital'`). RD should use `opal-capital` when writing any defensive firmId comparisons.

    **PAUSED 2026-04-10 ~17:05 EDT — DESIGN DECISION REQUIRED FROM ANDREW / COO**

    Re-GO'd on 2026-04-10 ~16:55 EDT by 0.4.0_DT_ClientPlatform. RD picked up the TO and did a diligence pass before writing code (ack message 20260410T223008Z). RD's analysis matched DT's pre-GO concern: **the button is structurally dormant under current auth logic.** Walking the three admin personas:

    1. **Internal Opal admin** (`isInternal=true`, `advisorId=null`) — sees BooksTab, but `claims.advisorId != null` gate fails; `auth.ts:62` makes this null by design for `firmId=opal-capital`. Button never renders.
    2. **External non-admin** (Chase, `isInternal=false`, `role=user`) — routes to `NonAdminProfileTab`, never mounts `BooksTab`. Button never rendered even if it existed.
    3. **External admin-who-is-advisor** (Travis, `isInternal=false`, `role=admin`) — `isFirmAdmin = isInternal = false`, routes to `NonAdminProfileTab`, never mounts `BooksTab`. And even if we relocated the button to `AdvisorPublicProfile` header gated on `isAdmin() && advisorId != null`, Travis ALREADY lands on his own profile via `NonAdminProfileTab` (advisorId hardwired from claims). The button would just reload the same view. Functionally pointless.

    RD's deeper insight: **the button only makes sense if the user is BROWSING SOMEONE ELSE'S profile and wants to jump back to their own.** But walking who can reach another advisor's profile:
    - **Leaderboard drill:** gated on `canDrillIntoAdvisor={isFirmAdmin}` in .001 — internal-only. Internal users have no advisorId. Dead end.
    - **BooksTab advisor drill:** only internal users see BooksTab landing. Same dead end.
    - **Direct URL:** not a real user workflow.

    **Conclusion: no user persona under current auth logic can BOTH (a) reach someone else's profile AND (b) have a non-null advisorId to jump back to.** The TO as-written ships dormant code.

    **Three paths forward (escalated to Andrew by 0.4.0_DT_ClientPlatform):**

    **(a) Broaden Leaderboard drill gate** from `isFirmAdmin` (internal-only) to `isAdmin()` (any role=admin, including partner-firm admins like Travis). Travis could then drill into other 49financial advisors from his firm's leaderboard. Once on someone else's profile, the .007 button lights up and jumps him home. This is a scope expansion — touches RD's .001 `canDrillIntoAdvisor` gating, changes AE's .004a/.004c scoping model (partner-firm admin gets wider path access), and needs an explicit security call on whether external firm admins should see other advisors' data within their firm.

    **(b) Ship .007 as dormant code** per the TO as-written. Button code lands, gate never satisfied, no visible behavior change. Latent hook for a future auth model expansion. Downside: we're shipping unexercised code paths.

    **(c) Close .007 as moot** until the broader admin-visibility auth model is designed. Zero code change now. Cleanest state but leaves the TO file dangling.

    **RD's strong lean and DT's agreement: (a) is the only path that produces a functional feature.** If Andrew wants partner-firm admins (Travis) to have firm-level visibility within their firm — and a fast jump back to their own profile from drilled views — then broaden the gate and ship .007 as it was originally conceived. If Andrew wants partner-firm admins locked to their own book identical to non-admins (Chase), then close .007 as moot and strip the BooksTab gating logic for consistency.

    While waiting on the decision, RD is proceeding with .005 (client drilldown lift) which is fully unblocked and has clear user value (Chase drilling his own book per the architectural principle).

    **RESOLUTION 2026-04-10 ~17:20 EDT — Andrew direction, relayed by 0.4.0_DT_ClientPlatform:**

    > "THE TOGGLE IS JUST THERE FOR CONVENIENCE, NOT FOR SECURITY, ITS JUST TO FLIP BETWEEN THE PAGES"

    **Interpretation:** stop treating this as a security design question. The button is a pure UX convenience — flip between firm view and own profile. The right scope-expansion is the minimal one that makes the button functional for the persona that needs it (partner-firm admins who are also advisors, like Travis Penfield).

    **Scope addition to .007 — SINGLE one-line gate change in AdvisorIntelligence.tsx (FINALIZED 2026-04-10 ~17:40 EDT after Andrew correction on .004a admin bypass semantics):**

    ```typescript
    // AdvisorIntelligence.tsx (approx line 177)
    - const isFirmAdmin = internal
    + const isFirmAdmin = internal || isAdmin()
    ```

    Where `internal = isInternal()` (firmId === 'opal-capital') and `isAdmin()` is `useAuth().isAdmin()` returning `state.user?.role === 'admin'`.

    **No two-gate split.** Earlier in the resolution thread, DT proposed splitting `isFirmAdmin` from `canDrillIntoAdvisor` to prevent dead clicks, because AE had initially picked Option 2 semantics (`isAdmin(jwt) === firmId === 'opal-capital'`) for .004a which would have 403'd Travis's drill attempts. **Andrew corrected to Option 3-simplified:**

    > "No travis should be able to click on any advisor card, or their bar in a chart element, or the leaderboard cards, and be taken to that advisors profile with full access. He is an Admin of 49. Chase however cannot do that." — Andrew, 2026-04-10 ~17:35 EDT

    AE's `.004a` Lambda@Edge helper was accordingly revised:
    ```js
    function getAllowedAdvisorIds(jwt) {
      if (jwt.role === 'admin') return null;           // bypass (Opal staff OR partner-firm admin)
      if (!jwt.advisorId) return [];                   // no identity = deny all
      return [jwt.advisorId];                          // non-admin = self only
    }
    ```

    With this, both Opal admins and partner-firm admins bypass the path-advisorId scoping check. Firm containment is handled IMPLICITLY by the existing `X-Firm-Id` injection + S3 path rewriting in `shared-advisor-router` and the firm-scoped data fetches in `opal-partners-data`. Travis hitting `/advisor/chase_bertrand/...` resolves because Chase is in 49financial; Travis hitting `/advisor/rj_advisor/...` 404s because the rewritten S3 key doesn't exist in 49financial's partition. Chase (role=user) still gets 403 on any path other than his own `advisorId`.

    **What this means for .007's frontend code:** `canDrillIntoAdvisor={isFirmAdmin}` works correctly without modification. Travis sees BooksTab, sees the leaderboard, can click any row/card/chart bar, and the backend serves his requests with full access (for same-firm advisors) or natural 404s (for cross-firm attempts, which the frontend leaderboard would not show anyway because it's already firm-scoped). No dead clicks. No split gates. No additional affordance-hiding logic. The single one-line change to `isFirmAdmin` is the entire delta for .007 outside of the button itself.

    **Persona walkthrough after this change:**

    1. **Travis** (partner-firm admin, `role=admin`, `firmId=49financial`, `advisorId=travis_penfield`): `isAdmin()=true`, `isFirmAdmin=true`, routes to `BooksTab`, sees 49financial leaderboard, `canDrillIntoAdvisor=true` makes rows clickable, `.007` "My Profile" button appears in BooksTab header because his `advisorId` is non-null. He can click any 49fin advisor row to drill into that advisor's full profile OR click the button to jump to his own profile. Back returns to BooksTab. Full firm-admin convenience.

    2. **Chase** (non-admin partner, `role=user`, `firmId=49financial`, `advisorId=chase_bertrand`): `isAdmin()=false`, `isFirmAdmin=false`, routes to `NonAdminProfileTab` which renders his own `AdvisorPublicProfile` directly. No BooksTab visibility, no leaderboard, no .007 button. He drills INTO his own book (L3/L4 per .005), but he cannot reach any other advisor's data. `.004a` backend gate enforces the same thing authoritatively — if he tries to construct a URL to another advisor, 403.

    3. **Internal Opal admin** (`firmId=opal-capital`, `role=admin`, `advisorId=null`): unchanged. `isInternal=true`, `isFirmAdmin=true`, routes to `BooksTab`, sees global leaderboard (or firm-selected), drills into any advisor. `.007` button gate `claims.advisorId != null` fails because Opal admins always have null advisorId, so the button does not render — consistent with the "they don't need a convenience shortcut because they don't have their own profile" framing.

    **Effect of the one-line change:**

    1. **Partner-firm admin (Travis Penfield, `role=admin`, `firmId=49financial`, `advisorId=travis_penfield`):** now routes to `BooksTab` on Tab 3 label "Books" (not `NonAdminProfileTab`). Sees the firm leaderboard for 49financial. The .007 button lights up on BooksTab header because his `claims.advisorId` is non-null. Clicks → renders his own `<AdvisorPublicProfile advisorId={claims.advisorId} showBackButton={true}>`. Back button returns to BooksTab firm landing.

    2. **Non-admin partner-firm user (Chase Bertrand, `role=user`, `firmId=49financial`, `advisorId=chase_bertrand`):** unchanged. `isAdmin()=false`, `isInternal()=false`, so `isFirmAdmin=false`, still routes to `NonAdminProfileTab`. Sees his own profile directly. No button shown (and none needed — he has nothing to flip to since he's already on his own profile).

    3. **Internal Opal admin:** unchanged. `isInternal()=true`, `isFirmAdmin=true`, still sees `BooksTab`. The .007 button gate `claims.advisorId != null` fails because Opal admins always have null advisorId by design (auth.ts:62). Button does not render for them. Consistent with Andrew's framing: they don't need convenience because they don't have their own advisor profile.

    **Known subtle implication (flagged but accepted per Andrew's "not security" guidance):**

    With the gate change, Travis will see the full 49financial advisor leaderboard on BooksTab. If he clicks to drill into another 49financial advisor, AE's .004a `shared-advisor-router` Lambda@Edge scoping decides whether the backend serves the data. The rule is `if !isAdmin(jwt) and path[advisorId] != jwt.advisorId: return 403`. The exact definition of `isAdmin(jwt)` in AE's Lambda matters:
    - If `isAdmin(jwt) === jwt.role === 'admin'`, Travis bypasses scoping and can view any 49financial advisor's detail
    - If `isAdmin(jwt) === jwt.firmId === 'opal-capital'`, Travis gets 403 on other advisors (only his own works)

    Andrew's "not a security concern" framing implies either behavior is acceptable for this ship. DT flagged this to AE in the .004a GO message so AE can pick consciously rather than by accident.

    **.007 deliverables updated:**
    1. Add "My Profile" button to BooksTab header (original TO spec) gated on `claims.advisorId != null`
    2. One-line gate change in `AdvisorIntelligence.tsx` to route partner-firm admins to BooksTab (new addition)
    3. Button click renders `<AdvisorPublicProfile advisorId={claims.advisorId} showBackButton={true} onBack={() => setViewMode('landing')}>` in-place
    4. Manual test coverage: log in as Travis (`travis.penfield@49financial.com` / `q1p0666`), confirm Tab 3 label = "Books", confirm leaderboard renders, confirm "My Profile" button appears in header, click it, confirm own profile renders, click back, confirm return to BooksTab landing

    **Status flipped back to `pending`** 2026-04-10 ~17:20 EDT.

    RD should complete .005 first (it's larger and fully unblocked), then pick up .007 as a small follow-up. Both ship in the same DT push pass if the timing lines up.
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
