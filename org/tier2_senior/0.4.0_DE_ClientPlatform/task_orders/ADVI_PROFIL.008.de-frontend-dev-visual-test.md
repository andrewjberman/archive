<task_order>
  <metadata>
    <id>2.0.0_SA_COO-2026-04-10-profil-visual-test</id>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_to>0.4.0_DE_ClientPlatform</issued_to>
    <date>2026-04-10</date>
    <status>staged</status>
    <project_code>ADVI_PROFIL</project_code>
  </metadata>

  <objective>
    Run the `/frontend-dev` plugin cycle against the AdvisorIntelligence page after .001 lands on portal DEV. Validate the header "event" redesign, the Profile/Book local toggle, the `NonAdminProfileTab` "Advisor Identity Unavailable" fallback (when .002 hasn't landed yet), and WCAG contrast on the indigo HelperTip surface. Wave 4 polish. Blocks on .001 + Andrew starting the dev server.
  </objective>

  <context>
    RD shipped the AdvisorIntelligence profile/book rewrite in .001 with `bun run tsc -b` and `bun run eslint` passing, but no browser-level visual test. The `/frontend-dev` plugin cycle is the canonical browser-side validation pass — it exercises interactive surfaces (toggles, drill clicks, hover tooltips) and flags visual/layout regressions that tsc + eslint miss.

    Scope of visual validation (from RD briefing §5.9):
    1. **Header "event" redesign** on `AdvisorPublicProfile.tsx` — 80x80 avatar tile with initials, text-3xl/4xl font-black display name, role badges, indigo gradient background. Verify layout at both admin view (with Back button) and non-admin view (with `showBackButton={false}`).
    2. **Profile/Book local toggle** — click toggle flips view in-place without a tab switch. AdvisorBookView renders ConsolidatedOverviewPanel + ClientsTable (tax panel suppressed pending .003). Verify no jank, no scroll reset, no URL change.
    3. **NonAdminProfileTab fallback** — Tab 3 as non-admin (pending .002) renders "Advisor Identity Unavailable" centered panel. Verify the fallback is visually correct (centered, icon present, message readable).
    4. **HelperTip indigo contrast** — every tooltip surface on AdvisorPublicProfile metrics and toggle labels. WCAG AA minimum (4.5:1 for text, 3:1 for UI). Use the frontend-dev plugin's built-in contrast check or an external tool (e.g., Chrome DevTools Accessibility panel).
    5. **AdvisorsTab leaderboard inertness for non-admin** — with `canDrillIntoAdvisor={false}`, all 8 click surfaces should have no cursor-pointer, no hover highlight, no click handler. Verify visually.

    Requires Andrew to start the dev server: `cd portal && /c/Users/AndrewBerman/.bun/bin/bun run dev --port 5175`. Notify Andrew via broker message when the TO starts.
  </context>

  <compiler_tools_mandate>
    Phase 1 (before starting):
    - Verify .001 has landed: `cd portal && git log origin/DEV -5` shows the 6 files from .001.
    - Send broker message to Andrew requesting the dev server be started.
    - Read `/frontend-dev` plugin documentation (if any) or recent session logs from other agents who have used it to understand the calling convention.
    - Prepare a test matrix covering the 5 scope items in §context.

    Phase 2 (during visual test):
    - Run `/frontend-dev` constitution for `AdvisorIntelligence`.
    - For each scope item, capture: a screenshot, the DOM snippet (via devtools), and a pass/fail verdict.
    - WCAG contrast: use Chrome DevTools Accessibility Panel OR the plugin's built-in check. Document the ratio for each tooltip surface.
    - If any failure is visual (not behavioral), flag to RD via broker message with screenshot + repro steps — do NOT fix frontend code in this TO.

    Phase 3 (after visual test):
    - Write a visual test report in the session log with the 5 scope items, pass/fail verdicts, screenshots (or paths to them), and the WCAG ratios.
    - If any failures are found, create a follow-up task order candidate list in the session log for RD to address in a subsequent pass.
  </compiler_tools_mandate>

  <cross_domain_coordination>
    shared_resource: Portal DEV server (started by Andrew). DE runs visual tests against it.
    shared_resource: `/frontend-dev` plugin — DE consumer only.
    last_write_owner: 0.4.0_DE_ClientPlatform (report author). RD fixes any discovered issues in follow-up TOs.
    required_action: "Send broker message to Andrew to start the dev server BEFORE running the visual test. Do not assume the server is already running."
  </cross_domain_coordination>

  <acceptance_criteria>
    1. **Dev server confirmed:** Broker message to Andrew, Andrew confirms dev server running at `http://localhost:5175`.
    2. **5 scope items tested:** Header event redesign, Profile/Book toggle, NonAdminProfileTab fallback, HelperTip contrast, AdvisorsTab non-admin inertness. Each with pass/fail verdict + evidence (screenshot or DOM snippet).
    3. **WCAG contrast results:** Every HelperTip surface has a documented contrast ratio. Minimum 4.5:1 for text; 3:1 for UI elements. Any surface below threshold flagged as a failure with the actual ratio.
    4. **Profile/Book toggle behavior:** Clicking the toggle does NOT change URL, does NOT reset scroll, does NOT unmount/remount the parent container. Verify via devtools.
    5. **NonAdminProfileTab fallback:** If test account is internal admin, use devtools to temporarily null out `claims.advisorId` or create a test user without one. Verify the fallback renders correctly.
    6. **AdvisorsTab inertness:** All 8 click surfaces (Top 3 cards, leaderboard card rows, NNA diverging bar, AUA bar chart, Growth bar chart, NNA/AUA card variants) have no pointer cursor, no hover highlight, no click handler when `canDrillIntoAdvisor={false}`. Verify all 8.
    7. **Failure triage:** Any discovered failures are documented in the session log as follow-up TO candidates with screenshot, DOM snippet, and suggested RD fix. Do NOT fix frontend code in this TO.
    8. **Visual test report:** Complete, formatted in the session log as a matrix. Includes the dev server startup time, the frontend-dev constitution run output, and the 5 scope item results.
  </acceptance_criteria>

  <scope>
    <files>
      <file action="test">portal/src/pages/AdvisorIntelligence/ (all 6 files from .001)</file>
      <file action="reference">RD briefing for expected behavior</file>
    </files>
  </scope>

  <requirements>
    <requirement id="1">Do NOT start before .001 is on portal DEV. Verify first.</requirement>
    <requirement id="2">Request dev server start from Andrew via broker message BEFORE beginning. Do not start it yourself.</requirement>
    <requirement id="3">Do NOT fix frontend code in this TO. Report failures as follow-up candidates for RD.</requirement>
    <requirement id="4">Document WCAG contrast ratios explicitly. The indigo HelperTip is a known risk area.</requirement>
    <requirement id="5">Test AdvisorsTab inertness for non-admin at ALL 8 click surfaces. Do not skip any.</requirement>
    <requirement id="6">Use devtools or a test account without an `advisorId` to exercise the NonAdminProfileTab fallback.</requirement>
  </requirements>

  <deliverables>
    <deliverable type="document">Visual test report in the session log at `org/tier2_senior/0.4.0_DE_ClientPlatform/logs/2026-04-{NN}/advi_profil_008_visual_test.md` with the 5 scope item matrix, screenshots or paths, WCAG ratios, and any follow-up TO candidates.</deliverable>
    <deliverable type="message">Broker message to Andrew requesting dev server start (sent at Phase 1).</deliverable>
    <deliverable type="message">Broker message to RD (0.4.2_RD_AdvisorIntelligence) with failure details if any are found.</deliverable>
  </deliverables>

  <do_not>
    <rule>Do NOT start the dev server yourself. Andrew starts it.</rule>
    <rule>Do NOT fix frontend code. Report failures to RD.</rule>
    <rule>Do NOT skip any of the 5 scope items. All must be tested.</rule>
    <rule>Do NOT test before .001 is on portal DEV.</rule>
    <rule>Do NOT commit anything — this TO produces a session log only.</rule>
  </do_not>
</task_order>
