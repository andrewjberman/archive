<task_order>
  <metadata>
    <id>2.0.0_SA_COO-2026-04-10-profil-dt-ship</id>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_to>0.4.0_DT_ClientPlatform</issued_to>
    <date>2026-04-10</date>
    <status>staged</status>
    <project_code>ADVI_PROFIL</project_code>
  </metadata>

  <objective>
    Review, commit, and push RD's AdvisorIntelligence profile/book rewrite (5 files modified + 1 new file) from the portal DEV working tree to the portal DEV branch. All commits must use `--author=0.4.2_RD_AdvisorIntelligence <0.4.2_RD_AdvisorIntelligence@opal.agent>`. This is Wave 1 of ADVI_PROFIL and has no dependencies — it unblocks .005 (RD L3/L4 lift), .006 (cache policy), .007 (admin my-profile toggle), and .008 (frontend-dev visual test).
  </objective>

  <context>
    RD (0.4.2_RD_AdvisorIntelligence) has staged the frontend portion of ADVI_PROFIL on the portal DEV submodule working tree. Files are uncommitted and unpushed. Code is `bun run tsc -b` exit 0 and `bun run eslint` 0 errors clean on all 5 modified files. Two non-blocking `react-refresh/only-export-components` warnings on `ClientsTab.tsx` are deferred to .005.

    Files in the working tree (`portal/src/pages/AdvisorIntelligence/`):
    - NEW: `AdvisorBookView.tsx` (103 lines) — single-advisor book component, useQuery on getPlatinumAdvisorSummary, renders ConsolidatedOverviewPanel + ClientsTable, tax panel placeholder-suppressed until .003 lands.
    - MODIFIED: `AdvisorPublicProfile.tsx` — canonical ToggleGroup, HelperTip on every metric/toggle label, header "event" redesign (80x80 avatar, text-3xl/4xl font-black display name, role badges, indigo gradient), Profile/Book local toggle via internal state flip (NOT cross-tab nav), optional `showBackButton?: boolean`, removed `onNavigateToBook`.
    - MODIFIED: `AdvisorIntelligence.tsx` — Tab 3 label flips by `isInternal()` ("Books" admin vs "Profile" non-admin), `NonAdminProfileTab` helper, `claims.advisorId` fallback UI ("Advisor Identity Unavailable" centered panel), `canDrillIntoAdvisor={isFirmAdmin}` plumbed down, removed `pendingBooksAdvisorId`/`handleNavigateToBook`/`clearPendingBooksAdvisor` plumbing.
    - MODIFIED: `tabs/AdvisorsTab.tsx` — prop signature swap (`onNavigateToBook` removed, `canDrillIntoAdvisor: boolean` added), `drillHandler` computed once and threaded to 8 click surfaces, `useEffect`→`useQuery` caching fix on getFirmLeaderboard with shared `['firm-leaderboard', firmOverride]` key.
    - MODIFIED: `tabs/ClientsTab.tsx` — dead cross-tab nav code removed (`initialAdvisorId`/`onConsumeInitialAdvisorId` plumbing + consuming useEffect), `CanonicalBookView` L2 layout collapsed from FeeRoleBreakdownPanel+TaxCostBasisPanel grid to TaxCostBasisPanel full-width, removed `FeeRoleBreakdownPanel` import, exported helpers (`ConsolidatedOverviewPanel`, `TaxCostBasisPanel`, `ClientsTable`, `normalizeMixTo4Class`, `platinumToComposition`).

    Full LOC delta summary (RD briefing §6):
    - AdvisorBookView.tsx NEW +103
    - AdvisorPublicProfile.tsx ~+260/-70
    - AdvisorIntelligence.tsx ~+70/-10
    - AdvisorsTab.tsx ~+30/-30
    - ClientsTab.tsx ~+10/-25

    RD pushed at the briefing: three-commit logical split recommended (caching fix / AdvisorPublicProfile redesign / role-conditional Tab 3 + AdvisorBookView extraction) OR single bundled commit — DT's call unless Andrew overrides.
  </context>

  <compiler_tools_mandate>
    Phase 1 (before committing):
    - Read the RD briefing in full: `org/tier3_junior/0.4.2_RD_AdvisorIntelligence/deliverables/briefing_profile_book_architecture.md`
    - `cd portal && bun run tsc -b` — must exit 0
    - `cd portal && bun run eslint src/pages/AdvisorIntelligence` — must have 0 errors (2 react-refresh warnings on ClientsTab.tsx are expected and allowed; deferred to .005)
    - `comp-transform fields AdvisorIntelligence` — cross-reference rendered fields against types. No new platinum-payload fields should appear yet (.003 adds `tax_exposure` separately). Flag any surprises.
    - `comp-cache` — verify the new `['advisor-book-view', advisorId, firmOverride]` and the moved `['firm-leaderboard', firmOverride]` cache keys don't collide with anything else in the portal cache map.

    Phase 2 (commit + push):
    - Author attribution REQUIRED: `--author="0.4.2_RD_AdvisorIntelligence <0.4.2_RD_AdvisorIntelligence@opal.agent>"` on every commit. Committer = your machine user. This is non-negotiable per org agent commit protocol.
    - Portal submodule workflow: changes land on portal DEV branch inside the submodule. After pushing portal DEV, the parent workspace repo submodule pointer moves — DO NOT commit the submodule pointer update in the parent repo in this TO. Parent repo submodule pointer bumps happen on a separate RD/DE call.

    Phase 3 (after push):
    - Smoke-check: verify the remote DEV branch on the portal repo has the three (or one) new commit(s) with the correct RD author. `git log --format='%H %an %s' origin/DEV -5` inside the portal submodule.
    - No Lambda/API deploy in this TO. No CloudFront invalidation needed — portal DEV bucket pick-up is handled by whatever the current deploy cadence is.
  </compiler_tools_mandate>

  <cross_domain_coordination>
    shared_resource: `portal/src/pages/AdvisorIntelligence/tabs/ClientsTab.tsx` — touched by .001 (DT commit) and .005 (RD L3/L4 lift). Ordering: .005 waits for .001 to land. Merge conflict risk is low because .005 is additive (new files + moves) rather than overlapping edits.
    shared_resource: `portal/src/contexts/AuthContext.context.ts` — NOT touched by .001. Cast `as unknown as { advisorId?: string }` in AdvisorIntelligence.tsx:153 is expected to remain in place until .002 lands.
    last_write_owner: 0.4.2_RD_AdvisorIntelligence authored the code; 0.4.0_DT_ClientPlatform ships it.
    required_action: "Ship as soon as tsc/eslint are verified. All downstream TOs in Waves 3 and 4 are blocked on this push reaching portal DEV. Do not wait on .002 or .003 — those are parallel tracks."
  </cross_domain_coordination>

  <acceptance_criteria>
    1. All 6 files are committed to portal DEV with `--author=0.4.2_RD_AdvisorIntelligence <0.4.2_RD_AdvisorIntelligence@opal.agent>`. Commit message convention: `0.4.2_RD_AdvisorIntelligence: ADVI_PROFIL -- {subsystem}`.
    2. Commit split decision documented in the session log: single bundled commit OR three-commit logical split (caching fix / AdvisorPublicProfile redesign / role-conditional Tab 3 + AdvisorBookView). Either is acceptable per DT's call; document the rationale.
    3. `bun run tsc -b` exit 0 verified immediately before commit — DO NOT commit red TypeScript.
    4. `bun run eslint src/pages/AdvisorIntelligence` verified immediately before commit — 0 errors. The two `react-refresh/only-export-components` warnings on ClientsTab.tsx are allowed and must be explicitly called out in the session log as "deferred to ADVI_PROFIL.005 bundle."
    5. `git push origin DEV` inside the portal submodule completes successfully. Verify via `git log origin/DEV -3` showing the new commit(s) with the correct author.
    6. Parent workspace repo submodule pointer is NOT committed in this TO. A separate RD/DE/DT pass will bump the pointer when the portal DEV deploy is ready to be picked up.
    7. Session log documents: commit SHA(s), split decision rationale, tsc/eslint exit codes, and the list of react-refresh warnings that will be addressed by .005.
    8. Compiler Tools section in the session log logs the `comp-transform fields AdvisorIntelligence` and `comp-cache` results (Phase 1) plus `git log origin/DEV` verification (Phase 3).
  </acceptance_criteria>

  <scope>
    <files>
      <file action="commit">portal/src/pages/AdvisorIntelligence/AdvisorBookView.tsx (NEW)</file>
      <file action="commit">portal/src/pages/AdvisorIntelligence/AdvisorPublicProfile.tsx</file>
      <file action="commit">portal/src/pages/AdvisorIntelligence/AdvisorIntelligence.tsx</file>
      <file action="commit">portal/src/pages/AdvisorIntelligence/tabs/AdvisorsTab.tsx</file>
      <file action="commit">portal/src/pages/AdvisorIntelligence/tabs/ClientsTab.tsx</file>
    </files>
  </scope>

  <requirements>
    <requirement id="1">Author attribution: `--author=0.4.2_RD_AdvisorIntelligence <0.4.2_RD_AdvisorIntelligence@opal.agent>` on every commit. This is non-negotiable — RD wrote the code.</requirement>
    <requirement id="2">Do NOT modify any of the 6 files in this TO. Your job is commit + push, not additional code changes. If tsc/eslint fails, message the COO and request guidance — do not fix silently.</requirement>
    <requirement id="3">Do NOT bump the parent workspace repo submodule pointer in this TO. That is a separate pass.</requirement>
    <requirement id="4">Do NOT address the 2 react-refresh warnings on ClientsTab.tsx — those are bundled into .005 (RD L3/L4 lift). Document them as deferred in the session log.</requirement>
    <requirement id="5">Do NOT wait on .002 (JWT claim) or .003 (book tax_exposure). The code degrades gracefully: .001 ships immediately with placeholder fallbacks, and .002/.003 light up the missing pieces asynchronously.</requirement>
  </requirements>

  <deliverables>
    <deliverable type="commit">Portal DEV commit(s) carrying all 6 files with RD author attribution.</deliverable>
    <deliverable type="push">Portal DEV branch pushed to origin.</deliverable>
    <deliverable type="document">Session log at `org/tier2_senior/0.4.0_DT_ClientPlatform/logs/2026-04-10/advi_profil_001_ship.md` with commit SHA(s), tsc/eslint results, split rationale, react-refresh warning deferral note, and compiler tools log.</deliverable>
  </deliverables>

  <do_not>
    <rule>Do NOT commit as your own author — this is RD's code, attribution goes to RD.</rule>
    <rule>Do NOT modify any of the 6 files to "fix" the react-refresh warnings. They are deferred to .005.</rule>
    <rule>Do NOT bump the parent workspace submodule pointer.</rule>
    <rule>Do NOT invoke any Lambda, deploy Terraform, or touch AWS infrastructure. This is a portal-side only TO.</rule>
    <rule>Do NOT amend prior commits. If something goes wrong, create a NEW commit on top.</rule>
  </do_not>
</task_order>
