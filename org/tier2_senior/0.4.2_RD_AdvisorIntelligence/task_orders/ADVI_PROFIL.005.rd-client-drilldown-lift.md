<task_order>
  <metadata>
    <id>2.0.0_SA_COO-2026-04-10-profil-l3l4-lift</id>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_to>0.4.2_RD_AdvisorIntelligence</issued_to>
    <date>2026-04-10</date>
    <status>staged</status>
    <project_code>ADVI_PROFIL</project_code>
  </metadata>

  <objective>
    Lift the L3 (client detail) and L4 (account detail) rendering out of `portal/src/pages/AdvisorIntelligence/tabs/ClientsTab.tsx` (lines ~480-660) into two new reusable components — `AdvisorBookClientDetail.tsx` (L3) and `AdvisorBookAccountDetail.tsx` (L4) — and wire them into `AdvisorBookView.tsx` (the new file from .001) with its own internal `selectedClientKey` / `selectedAccountId` state. Convert existing `useEffect` + `useState` fetches at both drill levels to `useQuery` during the lift (same pattern as the .001 AdvisorsTab caching fix). Each drill level gets its own per-id cache key, 5-min stale. Bundle the §5.6 react-refresh warning cleanup: move pure helpers (`normalizeMixTo4Class`, `platinumToComposition`) to `portal/src/pages/AdvisorIntelligence/lib/composition.ts`, move panel components to a `panels/` subfolder. Wave 3.
  </objective>

  <context>
    RD's .001 shipped `AdvisorBookView.tsx` with `onClientClick` as a no-op stub. Admin users viewing their own Book via the new Profile→Book toggle cannot drill into a specific client — the workaround is to use the BooksTab admin landing, which is the old path. Non-admin users (once .002 lands) have no path to client detail at all.

    Current L3/L4 code lives in `ClientsTab.tsx` and is tangled with the admin BooksTab state machine. The lift must decouple the rendering from the specific data source (admin `AdvisorBookResponse` vs single-advisor `PlatinumAdvisorSummary`) and accept normalized props. Expected signatures:
    ```
    <AdvisorBookClientDetail
      clientKey={string}
      clientData={NormalizedClient}
      onAccountClick={(accountId: string) => void}
      onBack={() => void}
    />
    <AdvisorBookAccountDetail
      accountId={string}
      accountData={NormalizedAccount}
      onBack={() => void}
    />
    ```
    The parent (`AdvisorBookView` or `ClientsTab`) owns the state and fetches; the detail components are pure renderers.

    React-refresh warnings from .001 on `ClientsTab.tsx`: ESLint `react-refresh/only-export-components` flags the file because it now exports 5 helpers (`ConsolidatedOverviewPanel`, `TaxCostBasisPanel`, `ClientsTable`, `normalizeMixTo4Class`, `platinumToComposition`) alongside the `BooksTab` component. Fix: move the pure helpers to `lib/composition.ts`, move the panel components to `panels/` (own files), leave `ClientsTab` as a single-component file. This also keeps the code clean for future maintenance.

    Cache policy: default to 5-min stale on the per-id keys (matching existing page policy). If Andrew/COO picks option (b) or (c) in .006, those keys will be updated in a follow-up one-line change per key. Do not wait on .006 — ship with 5-min stale and update after.

    Client data fetching: the existing `ClientsTab` L3/L4 fetches use bespoke `useEffect`+`useState` patterns. Convert to `useQuery` with proper error/loading states. If the existing fetch functions live in `portal/src/api/` or similar, reuse them as-is; do not rewrite the API layer.
  </context>

  <compiler_tools_mandate>
    Phase 1 (before writing):
    - Verify .001 has landed: check `portal` submodule DEV branch `git log origin/DEV -5`; confirm the 6 files from .001 are present.
    - `comp-transform fields ClientsTab` — capture the full rendered field set for L3 and L4, so the lift preserves identical output.
    - `comp-cache` — list all current cache keys under `portal/src/pages/AdvisorIntelligence/`. The new per-id keys (`['advisor-book-client', advisorId, clientKey]`, `['advisor-book-account', advisorId, accountId]`) must not collide.
    - `Grep` for every call site of `normalizeMixTo4Class` and `platinumToComposition` across the portal. The move to `lib/composition.ts` requires updating all importers.
    - Read the full L3/L4 block in `ClientsTab.tsx` (lines ~480-660) to understand the current data shape expectations and the exact rendering hierarchy.

    Phase 2 (during implementation):
    - Create `portal/src/pages/AdvisorIntelligence/lib/composition.ts` with `normalizeMixTo4Class` and `platinumToComposition` — pure, no React imports.
    - Create `portal/src/pages/AdvisorIntelligence/panels/` subfolder. Move `ConsolidatedOverviewPanel`, `TaxCostBasisPanel`, `ClientsTable` into their own files under `panels/`. Update all importers.
    - Create `portal/src/pages/AdvisorIntelligence/AdvisorBookClientDetail.tsx` and `AdvisorBookAccountDetail.tsx` as pure renderers.
    - Update `AdvisorBookView.tsx` to own the `selectedClientKey` / `selectedAccountId` state, fetch per-id via `useQuery`, and render the drill chain.
    - Update `ClientsTab.tsx` (the admin BooksTab path) to use the new extracted components too, not the inline L3/L4 code. Admin and non-admin paths converge on the same rendering components but keep distinct data fetches.
    - Convert L3 and L4 `useEffect`+`useState` fetches to `useQuery`. Preserve existing error/loading UX — any new Suspense boundaries must match existing patterns.

    Phase 3 (after implementation):
    - `bun run tsc -b` exit 0
    - `bun run eslint src/pages/AdvisorIntelligence` — 0 errors, 0 react-refresh warnings (the lift resolves them)
    - `comp-transform fields AdvisorIntelligence` — verify the rendered field set is unchanged (same fields, now rendered by extracted components)
    - `comp-cache` — verify the new per-id cache keys are present and don't collide
    - `comp-blast ClientsTab` — verify no dead imports remain after the extraction
    - RD does NOT push — this TO ships changes to the portal DEV working tree. DT picks up the commit+push in a follow-up (or bundled with .001 if .005 lands quickly enough to be in the same DT pass — unlikely given the dependency chain).
  </compiler_tools_mandate>

  <cross_domain_coordination>
    shared_resource: `portal/src/pages/AdvisorIntelligence/tabs/ClientsTab.tsx` — .001 (DT commit), .005 (RD L3/L4 lift). Ordering: .005 blocks on .001. Merge conflict risk is low because .001 commits and .005 is additive (extract to new files, update imports).
    shared_resource: `portal/src/pages/AdvisorIntelligence/AdvisorBookView.tsx` — .001 (NEW file), .005 (extends with drill state). Same owner (RD), no conflict.
    shared_resource: The cache key `['advisor-book-view', advisorId, firmOverride]` from .001. The new `['advisor-book-client', advisorId, clientKey]` and `['advisor-book-account', advisorId, accountId]` must be distinct.
    last_write_owner: 0.4.2_RD_AdvisorIntelligence for all code. DT ships separately.
    required_action: "Wait for .001 to land on portal DEV. Then proceed with the lift. Cache policy (5-min stale) is a placeholder — if .006 changes the policy, that's a one-line follow-up per cache key."
  </cross_domain_coordination>

  <acceptance_criteria>
    1. **Files created:** `AdvisorBookClientDetail.tsx`, `AdvisorBookAccountDetail.tsx`, `lib/composition.ts`, and a `panels/` subfolder with `ConsolidatedOverviewPanel.tsx`, `TaxCostBasisPanel.tsx`, `ClientsTable.tsx`.
    2. **ClientsTab.tsx cleanup:** L3 and L4 inline rendering removed (~300 lines deleted). Uses the new extracted components. Exports removed (no more 5-helper export set). React-refresh warnings gone.
    3. **AdvisorBookView drill state:** Owns `selectedClientKey` / `selectedAccountId` state. `onClientClick` is wired (no longer a no-op). Renders `AdvisorBookView` → `AdvisorBookClientDetail` → `AdvisorBookAccountDetail` navigation chain.
    4. **Per-id cache keys:** `['advisor-book-client', advisorId, clientKey]` and `['advisor-book-account', advisorId, accountId]`, both 5-min stale, no collisions with existing keys.
    5. **useQuery conversion:** All L3/L4 fetches use `useQuery`, not `useEffect`+`useState`. Error states handled. Loading states match existing page UX.
    6. **tsc + eslint clean:** `bun run tsc -b` exit 0. `bun run eslint src/pages/AdvisorIntelligence` 0 errors, 0 react-refresh warnings.
    7. **comp-transform fields unchanged:** The rendered field set for L3 and L4 is byte-identical pre/post lift. Verified via `comp-transform fields AdvisorIntelligence` before and after.
    8. **Admin and non-admin both drill:** Admin user from BooksTab can drill L2→L3→L4 (unchanged UX). Non-admin user from Tab 3 Profile→Book can drill into their own clients via the new AdvisorBookView path. Both use the same rendering components.
    9. **Navigation back preserves scroll:** Back from L4 to L3 and from L3 to Book view preserves parent scroll position (use react-router or browser history — whichever matches existing AdvisorsTab drill pattern).
    10. **Session log:** Documents the extracted file list, the cache key spec, the useQuery conversion diff summary (LOC), the comp-transform before/after, and the Compiler Tools section.
    11. **Working tree handoff:** RD does NOT commit or push. RD sends a broker message to 0.4.0_DT_ClientPlatform announcing the working tree is ready for a commit+push pass (similar to the .001 handoff).
  </acceptance_criteria>

  <scope>
    <files>
      <file action="create">portal/src/pages/AdvisorIntelligence/AdvisorBookClientDetail.tsx</file>
      <file action="create">portal/src/pages/AdvisorIntelligence/AdvisorBookAccountDetail.tsx</file>
      <file action="create">portal/src/pages/AdvisorIntelligence/lib/composition.ts</file>
      <file action="create">portal/src/pages/AdvisorIntelligence/panels/ConsolidatedOverviewPanel.tsx</file>
      <file action="create">portal/src/pages/AdvisorIntelligence/panels/TaxCostBasisPanel.tsx</file>
      <file action="create">portal/src/pages/AdvisorIntelligence/panels/ClientsTable.tsx</file>
      <file action="modify">portal/src/pages/AdvisorIntelligence/AdvisorBookView.tsx</file>
      <file action="modify">portal/src/pages/AdvisorIntelligence/tabs/ClientsTab.tsx</file>
      <file action="update_imports">Any other file importing `normalizeMixTo4Class`, `platinumToComposition`, or the three panel components from ClientsTab</file>
    </files>
  </scope>

  <requirements>
    <requirement id="1">Do NOT start until .001 is committed + pushed on portal DEV. Verify via `git log origin/DEV -5` inside the portal submodule.</requirement>
    <requirement id="2">Preserve the rendered field set byte-for-byte. The lift is a refactor, not a feature change. `comp-transform fields AdvisorIntelligence` must match pre/post. Any diff is a regression.</requirement>
    <requirement id="3">Convert useEffect+useState fetches to useQuery. Do not leave any raw useEffect fetches in the extracted components.</requirement>
    <requirement id="4">Ship with 5-min stale cache keys as a placeholder. If .006 changes the policy, the follow-up is a one-line edit per key. Do not block on .006 — that's a separate decision.</requirement>
    <requirement id="5">Do NOT commit or push. RD hands the working tree off to DT via broker message, same pattern as .001.</requirement>
    <requirement id="6">Fix the react-refresh warnings — do not leave them deferred further. The lift's primary side benefit is resolving these.</requirement>
    <requirement id="7">Admin BooksTab and non-admin Profile→Book both converge on the same rendering components. Do NOT duplicate the rendering logic across two code paths.</requirement>
    <requirement id="8">Handle the "no client selected" / "no account selected" empty states explicitly. Do not render undefined or blank.</requirement>
    <requirement id="9">If you discover that the existing L3/L4 fetches use PII-sensitive fields that should not be cached (.007 decision is likely option b or c for client detail), still ship with 5-min stale — .006 will update.</requirement>
  </requirements>

  <deliverables>
    <deliverable type="code">9 files created or modified in the portal DEV working tree, staged for commit under RD author.</deliverable>
    <deliverable type="document">Session log at `org/tier2_senior/0.4.2_RD_AdvisorIntelligence/logs/2026-04-{NN}/advi_profil_005_l3l4_lift.md` with the extracted file list, cache key spec, useQuery conversion LOC summary, comp-transform before/after, and Compiler Tools section.</deliverable>
    <deliverable type="message">Broker message to 0.4.0_DT_ClientPlatform announcing working tree is ready for commit+push, same pattern as .001.</deliverable>
  </deliverables>

  <do_not>
    <rule>Do NOT start before .001 is committed and pushed on portal DEV.</rule>
    <rule>Do NOT change the rendered field set. The lift is a pure refactor.</rule>
    <rule>Do NOT commit or push. Hand off to DT via broker message.</rule>
    <rule>Do NOT leave useEffect+useState fetches in the extracted components. Full useQuery conversion.</rule>
    <rule>Do NOT block on .006 cache policy decision. Ship with 5-min stale placeholder.</rule>
    <rule>Do NOT duplicate rendering logic between admin BooksTab and non-admin Profile→Book paths. One set of extracted components serves both.</rule>
  </do_not>
</task_order>
