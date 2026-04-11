# Briefing: AdvisorIntelligence Profile / Book Architecture

**Author:** 0.4.2_RD_AdvisorIntelligence
**Date:** 2026-04-10
**Audience:** 1.0.0_SA_CTO, 2.0.0_SA_COO (for task order decomposition)
**Status:** Frontend changes shipped to working tree on `portal/DEV` submodule (staged, not committed). Awaiting backend + follow-up task orders.

---

## 1. Origin

Session started with a narrow ask: the Advisors tab on `/advisor-intelligence` didn't cache locally, forcing a refetch on every tab switch. Root cause was `AdvisorsTab.tsx` using raw `useEffect` + `useState` for its leaderboard fetch instead of `useQuery`. Fixed by converting to React Query with the same config as `DistributionTab` (`staleTime: 5 * 60 * 1000`, `refetchOnMount: false`, `refetchOnWindowFocus: false`).

That unblocked a broader UX conversation about how Profile and Book views of an advisor should relate to each other, what data scope each needs, and how admin vs non-admin experiences should differ.

---

## 2. Problem statement (as articulated by Andrew)

1. **Fee/role breakdown was duplicated.** It appeared in both the Advisors-tab Profile drilldown AND the BooksTab L2 advisor-book drill, and the Profile version was "infinitely better" (window-aware with fee buckets). The BooksTab version was noise.

2. **BooksTab landing is inherently an admin view.** Firm composition, fee efficiency scatter, advisor roster — none of that is relevant to an individual advisor looking at their own book. Non-admin advisors should never see it.

3. **Profile ↔ Book toggle needed to be instant.** Originally (before this session) there was no such toggle. My first cut in an earlier turn routed Book navigation cross-tab to BooksTab, which triggered firm-wide admin data fetches — too heavy for what should be a single-advisor view flip.

4. **Client data has different sensitivity than firm analytics.** Caching and isolation for client rosters should be considered separately from AUA/NNA analytics.

5. **Defense in depth belongs in one place.** Non-admins shouldn't be able to drill into other advisors' profiles at all — neither via Leaderboard clicks nor via crafted URLs. Per-surface permission checks scattered across components invite drift.

---

## 3. Agreed architecture

### 3.1 Tab layout (labels unchanged except Tab 3 role-conditional)

| Tab | Label | Admin (internal Opal / firm admin) | Non-admin advisor |
|-----|-------|-------------------------------------|-------------------|
| 1 | Distribution | Firm-level distribution analytics | Same |
| 2 | Advisors | Firm leaderboard + Top 3 + rolling flows. **Clickable** — drill into any advisor's Profile | Same visual content, **not clickable** — read-only competitive context |
| 3 | Books (admin) / Profile (non-admin) | Firm admin landing: composition, fee efficiency scatter, advisor roster, drill into any advisor's book | Direct render of their own `AdvisorPublicProfile` (seeded with JWT `advisorId` claim) |

Tab labels stay literal: "Books" for admins, "Profile" for non-admins. Decided after discussing alternatives (Firm Book, Book of Business, Practice, Roster) — Andrew preferred keeping the existing "Books" label rather than introducing new terminology.

### 3.2 Profile ↔ Book toggle = local view flip

The Profile/Book toggle lives **inside** `AdvisorPublicProfile` and swaps views in-place. Not a tab switch. Not a cross-tab navigation. Both views render under the same prominent header (the "event" with big avatar, name, role pills).

- **Profile view** = what `AdvisorPublicProfile` has always rendered: summary card (AUA, flows, fee section, identity), role composition donut, time-series panel
- **Book view** = new `AdvisorBookView` component. Single `useQuery` on `getPlatinumAdvisorSummary(advisorId)`. Renders composition (donut + holdings + quarterly mix) and the client roster. Caches separately (`['advisor-book-view', advisorId, firmOverride]`, 5-min stale).

First click on "Book" fetches that one advisor's summary. Subsequent toggles are instant (cache hit). Switching advisors (admin drill) evicts the per-advisor cache naturally.

### 3.3 Fee/role breakdown is Profile-only

Removed entirely from `BooksTab` admin L2 drill. The `CanonicalBookView` level='l2' layout collapsed from `FeeRoleBreakdownPanel + TaxCostBasisPanel` to tax-only (at full width, same as L4).

Rationale: the Profile version is window-aware (`feeView: 'all' | 'fee_paying' | 'no_fee'` master toggle that scopes the entire summary), assembled from the per-fee-bucket `role_breakdown` that 0.4.0_DS just shipped in commit `d3abb883` (D_00c Option 1). One authoritative surface, not two.

### 3.4 Defense in depth — single choke point

Under this architecture, an advisor can only ever reach their own profile via Tab 3 (which is hard-wired to their JWT `advisorId`). Tab 2 (Leaderboard) renders the same firm-wide data for everyone but strips all click affordances for non-admins. No cross-tab navigation paths. No click handlers to audit per surface.

Frontend enforcement is cosmetic — the actual defense must live server-side (see §5.2).

---

## 4. What's implemented (this session)

All changes in `portal/src/pages/AdvisorIntelligence/` under submodule `DEV` branch. Staged in working tree, **not committed, not pushed**.

### 4.1 New file

- **`AdvisorBookView.tsx`** (103 lines) — single-advisor book component. `useQuery` on `getPlatinumAdvisorSummary(advisorId, firmOverride)`, keyed independently. Renders `ConsolidatedOverviewPanel` + `ClientsTable`. Tax panel placeholder-suppressed until DS adds book-level tax to the payload. `onClientClick` is a no-op stub (see §5.3).

### 4.2 Modified files

- **`AdvisorPublicProfile.tsx`**
  - Added canonical `ToggleGroup` (matches `AdvisorsTab` exactly: `bg-white/5 rounded-lg p-1`, `px-3 py-1.5 text-xs`)
  - Added `Tip` / `ToggleLabel` helpers wrapping `HelperTip` (indigo canonical)
  - Added `HelpCircle` tooltips to every metric label in the SummaryCard (Total AUA, Accounts, Clients, New Clients, Inflows, Outflows, NNA, AUA Growth, Fee-Earning AUA, Non-Fee AUA, Avg Fee Rate, Active Since, Roles) and every toggle label (Fees, Window, Metric, Mode, View)
  - Added `helpText` props to the 3 `PanelHeader`s (Summary, Role Composition, Time Series)
  - Redesigned header as an "event": 80×80 avatar tile with initials, `text-3xl md:text-4xl font-black` display name, role badges, indigo gradient background. "Back to Advisors" moved to a dedicated top-of-panel button with `ArrowLeft`
  - Added Profile/Book toggle on the right side of the header event (`User` + `BookOpen` icons)
  - Book view renders `<AdvisorBookView>` inline via local state flip — no cross-tab navigation
  - Added optional `showBackButton?: boolean` prop (default true) so the component can render as a top-level tab without a nonsensical Back button
  - Removed `onNavigateToBook` prop and its dead handler

- **`AdvisorIntelligence.tsx`**
  - Tab 3 label flips between "Books" (admin) and "Profile" (non-admin) based on `isInternal()`
  - Tab 3 body renders `BooksTab` for admins, new `NonAdminProfileTab` helper for non-admins
  - `NonAdminProfileTab` fetches the firm leaderboard (shared cache key with `AdvisorsTab`, so no duplicate fetch), resolves the current advisor's entry, and renders `<AdvisorPublicProfile showBackButton={false}>`
  - Non-admin claim read: `(claims as { advisorId?: string })?.advisorId ?? null`. Currently always null — see §5.1
  - Missing-claim fallback UI: centered Panel with icon + "Advisor Identity Unavailable" heading + contact-support message
  - Passes `canDrillIntoAdvisor={isFirmAdmin}` down to `AdvisorsTab`
  - Removed all cross-tab nav plumbing (`pendingBooksAdvisorId` state, `handleNavigateToBook`, `clearPendingBooksAdvisor`)

- **`tabs/AdvisorsTab.tsx`**
  - Prop signature change: `onNavigateToBook` removed, `canDrillIntoAdvisor: boolean` added
  - `drillHandler = canDrillIntoAdvisor ? handleAdvisorClick : undefined` computed once and passed to all 8 downstream click surfaces (Top 3 cards, leaderboard card rows, NNA diverging bar, AUA bar chart, Growth bar chart, and the NNA/AUA card variants)
  - Every leaderboard surface already gates `cursor-pointer` and hover styles on whether `onAdvisorClick` is defined — passing `undefined` makes the entire leaderboard inert for non-admins with zero per-component changes
  - Drill branch `if (selectedAdvisorId && employeeData && canDrillIntoAdvisor)` — belt and suspenders
  - Removed stale `ChartWindowOption` import (was unused after earlier refactor)
  - Initial caching fix from session start: `useEffect`→`useQuery` on `getFirmLeaderboard`, shared `['firm-leaderboard', firmOverride]` key with `NonAdminProfileTab`

- **`tabs/ClientsTab.tsx`** (BooksTab)
  - Removed `initialAdvisorId` / `onConsumeInitialAdvisorId` prop plumbing (dead code from the earlier cross-tab nav attempt)
  - Removed the `useEffect` that consumed `initialAdvisorId`
  - Removed `feeSummaryByRole` from the `CanonicalBookView` L2 call site and from the type signature
  - `CanonicalBookView` L2 layout collapsed from `<FeeRoleBreakdownPanel + TaxCostBasisPanel>` grid to `<TaxCostBasisPanel>` full-width
  - Removed unused `FeeRoleBreakdownPanel` import
  - Exported (for `AdvisorBookView` consumption): `ConsolidatedOverviewPanel`, `TaxCostBasisPanel`, `ClientsTable`, `normalizeMixTo4Class`, `platinumToComposition`

### 4.3 Verification

- `bun run tsc -b` → exit 0
- `bun run eslint` on all 5 edited files → 0 errors
- 2 react-refresh/only-export-components warnings on `ClientsTab.tsx` (non-blocking, HMR fast-refresh concern only) — see §5.6
- No browser/Playwright visual testing yet — `/frontend-dev` plugin cycle pending on Andrew kicking off the dev server

---

## 5. What's NOT done — task order candidates

### 5.1 [BLOCKER, DT] JWT `advisorId` claim

**Problem:** `portal/src/contexts/AuthContext.context.ts` defines `Claims` with only `firmId: string | null` and `userType: 'Dev' | null`. No `advisorId` field.

**Impact:** Non-admin Tab 3 ("Profile") renders the "Advisor Identity Unavailable" placeholder at runtime. All the frontend infrastructure is wired and typed for when the claim lands — the path auto-activates the moment `claims.advisorId` becomes non-null.

**Needed:** DT (0.4.0_DT_ClientPlatform and/or 0.7.0_AE_CloudOps) to plumb an `advisorId` claim into the JWT issued by `auth-validator-edge` / login Lambda. This is a multi-layer change: token issuance, token validation, `Claims` interface update in the frontend, and a mapping of user → advisor at the auth source (likely in `portal-auth` pipeline).

**Acceptance:** `const { claims } = useAuth(); claims.advisorId` resolves to the authenticated user's advisor id on non-admin accounts. Remove the `as unknown as { advisorId?: string }` cast in `AdvisorIntelligence.tsx:153` once `Claims` is updated.

### 5.2 [BLOCKER, DT/AE] Server-side advisor scoping

**Problem:** Frontend gating is cosmetic. A non-admin user with network devtools can today call any of these endpoints with any advisor id:
- `getPlatinumAdvisorSummary(advisorId, firmOverride)`
- `getPlatinumAdvisorDrilldownSummary(advisorId, firmOverride)`
- `getPlatinumAdvisorTimeseries(advisorId, firmOverride)`

**Impact:** The "defense in depth" value of the single-choke-point architecture is null until this is enforced server-side.

**Needed:** Lambda@Edge (likely `shared-advisor-router` v9+) must check that non-admin JWTs can only request their own `advisorId` on these paths. Admins continue to bypass the check. Spec:

```
if !isAdmin(jwt) and pathAdvisorId(request) != jwt.advisorId:
    return 403
```

Endpoints to cover (path templates):
- `/api/scoped/partners/books/advisor/{advisorId}/platinum-summary`
- `platinum/advisors/{advisorId}/summary.json` (via Lambda, not S3-direct)
- `platinum/advisors/{advisorId}/timeseries.json` (via Lambda, not S3-direct)

**Acceptance:** Crafted curl from a non-admin JWT to another advisor's id returns 403. Admin request unaffected. Integration test covering both cases.

### 5.3 [RD] L3/L4 client drilldown inside `AdvisorBookView`

**Problem:** `AdvisorBookView.tsx` renders the clients table but `onClientClick` is a no-op. A user (admin or non-admin) viewing their own Book view cannot drill into a specific client.

**Impact:** Feature-gap. Current workaround: admin can use the BooksTab admin landing to reach client detail (L3) and account detail (L4). Non-admin has no path to client detail at all.

**Needed:** Lift `ClientsTab.tsx`'s L3 and L4 rendering logic (lines ~480-660 approximately) into reusable components. Likely two new files:
- `AdvisorBookClientDetail.tsx` (L3)
- `AdvisorBookAccountDetail.tsx` (L4)

Wire them into `AdvisorBookView` with its own internal `selectedClientKey` / `selectedAccountId` state. Both paths should fetch only the specific client/account data (no firm-wide calls). Each drill level needs its own React Query key scoped by the ids.

**Scope:** ~300 lines moved, plus a separate useQuery per level. Existing ClientsTab L3/L4 currently uses `useEffect`+`useState` fetches that should be converted to `useQuery` during the lift (same pattern as the AdvisorsTab caching fix).

**Acceptance:** From `AdvisorBookView` (i.e., from Profile→Book toggle), clicking a client row renders client detail inline, clicking an account renders account detail inline. Navigation back preserves parent scroll position. Cache keys are per-id, 5-min stale.

### 5.4 [DS] Book-level tax exposure in `PlatinumAdvisorSummary`

**Problem:** `AdvisorBookView` hides the tax panel because `PlatinumAdvisorSummary` (from `getPlatinumAdvisorSummary`) doesn't carry book-level `tax_exposure`. Today that data only lives on the admin path's `AdvisorBookResponse` (used by ClientsTab's L2 drill).

**Needed:** DS (0.4.0_DS_ClientPlatform) to add a `tax_exposure` field to the platinum advisor summary payload with the same shape as the existing `AdvisorBookResponse.tax_exposure`:
```ts
tax_exposure: {
  taxable: number
  taxable_pct: number
  tax_deferred: number
  tax_deferred_pct: number
  tax_free: number
  tax_free_pct: number
  capital_gains_ttm?: number
}
```

**Frontend follow-up (trivial):** In `AdvisorBookView.tsx`, replace `const tax = null` with the live value and the `{tax && <TaxCostBasisPanel>}` render lights up.

### 5.5 [RD, optional] Admin "My Profile" toggle on Tab 3

**Problem:** Deferred during design. Internal Opal admins don't have an `advisorId`, so they'd never need this. External firm-admin users who are themselves advisors would benefit from a shortcut from BooksTab landing → their own profile.

**Scope:** Small — add a button/toggle in `BooksTab` header that renders `<AdvisorPublicProfile advisorId={claims.advisorId} showBackButton={true} onBack={backToLanding}>` when clicked. Only surface the button when `claims.advisorId` is non-null (i.e., the admin is also an advisor).

**Blocked on:** §5.1 JWT claim.

**Priority:** Low — doesn't affect the primary advisor experience.

### 5.6 [RD] React-refresh lint warnings on `ClientsTab.tsx`

**Problem:** `ClientsTab.tsx` now exports 5 helpers (`ConsolidatedOverviewPanel`, `TaxCostBasisPanel`, `ClientsTable`, `normalizeMixTo4Class`, `platinumToComposition`) alongside the `BooksTab` component. ESLint `react-refresh/only-export-components` flags this — warnings, not errors, but it degrades HMR fast-refresh in dev.

**Fix:** Move the two pure helpers (`normalizeMixTo4Class`, `platinumToComposition`) to a new file like `portal/src/pages/AdvisorIntelligence/lib/composition.ts`. The three panel components (`ConsolidatedOverviewPanel`, `TaxCostBasisPanel`, `ClientsTable`) can either stay in `ClientsTab.tsx` (still warns because of co-located helpers) or be lifted to their own files (cleanest). Lifting to `panels/` subfolder is preferable if §5.3 lands, because L3/L4 extraction will want them as siblings anyway.

**Priority:** Cosmetic, but bundle with §5.3 work.

### 5.7 [RD] Client data caching policy decision

**Status:** Currently using `staleTime: 5 * 60 * 1000`, `gcTime` default (5 min), to match the rest of the page. Andrew raised "different caching policy for client data" during design but didn't commit to a specific value.

**Options to decide:**
1. **Match existing** (current state) — 5-min stale, default gc. Fast toggles, data persists across advisor switches within 5 min.
2. **PII-sensitive** — `staleTime: 30_000`, `gcTime: 0`. Instant eviction on unmount, refetch on every reopen. Safer if someone walks past an unlocked laptop.
3. **Split level** — advisor-level book 5 min stale (§4.1 current); client-detail (L3, when §5.3 lands) `gcTime: 0`. Two policies, sharper at the more sensitive level.

**Needed:** Andrew or COO decision. I can flip the values in one line each.

### 5.8 [DT] Commit + push

**Status:** All 5 modified files and 1 new file are in the portal submodule working tree on `DEV`, staged for author `0.4.2_RD_AdvisorIntelligence`. RD cannot push.

**Needed:** 0.4.0_DT_ClientPlatform to review, commit under RD author attribution, and push to portal `DEV`. The commits should be split logically:

1. `0.4.2_RD_AdvisorIntelligence: AdvisorsTab -- fix leaderboard caching via useQuery`
2. `0.4.2_RD_AdvisorIntelligence: AdvisorPublicProfile -- canonical toggles + HelperTip surface + header event redesign`
3. `0.4.2_RD_AdvisorIntelligence: AdvisorIntelligence -- role-conditional Tab 3 + Profile/Book local toggle + AdvisorBookView extraction`

Or single bundled commit — DT's call.

### 5.9 [Andrew / DE] Visual testing

**Needed:** `/frontend-dev` plugin cycle on the new header event, Profile/Book toggle, and `NonAdminProfileTab` placeholder. Requires Andrew to start the dev server (`cd portal && bun run dev --port 5175`) and run the frontend-dev constitution for `AdvisorIntelligence`. WCAG check on the indigo HelperTip contrast is worth verifying.

---

## 6. Files touched (full list)

| File | Status | LOC delta approx |
|------|--------|------------------|
| `portal/src/pages/AdvisorIntelligence/AdvisorBookView.tsx` | NEW | +103 |
| `portal/src/pages/AdvisorIntelligence/AdvisorPublicProfile.tsx` | MODIFIED | ~+260 / ~-70 |
| `portal/src/pages/AdvisorIntelligence/AdvisorIntelligence.tsx` | MODIFIED | ~+70 / ~-10 |
| `portal/src/pages/AdvisorIntelligence/tabs/AdvisorsTab.tsx` | MODIFIED | ~+30 / ~-30 (incl. earlier caching fix) |
| `portal/src/pages/AdvisorIntelligence/tabs/ClientsTab.tsx` | MODIFIED | ~+10 / ~-25 |

All edits stay within `portal/src/pages/AdvisorIntelligence/` — inside RD commit scope.

---

## 7. Recommended task order sequencing

**Wave 1 — unblock the non-admin path (parallelizable):**
- `ADVI_*.dt-jwt-advisor-claim` → §5.1
- `ADVI_*.ds-book-tax-exposure` → §5.4
- `ADVI_*.dt-ship-profile-book-rewrite` → §5.8 (no dependencies, can ship immediately)

**Wave 2 — defense in depth (blocks on §5.1):**
- `ADVI_*.ae-advisor-scoping-enforcement` → §5.2

**Wave 3 — feature completion (blocks on §5.8):**
- `ADVI_*.rd-client-drilldown-lift` → §5.3 + §5.6 bundled
- `ADVI_*.rd-client-cache-policy-decision` → §5.7 (just needs Andrew decision, then one-line change)

**Wave 4 — polish:**
- `ADVI_*.rd-admin-my-profile-toggle` → §5.5 (blocked on §5.1, not urgent)
- `ADVI_*.de-frontend-dev-visual-test` → §5.9

---

## 8. Open questions for Andrew / COO

1. **Client data caching policy** — §5.7. Need a commitment to option 1, 2, or 3.
2. **L3/L4 drill-down scope** — §5.3. Should non-admin advisors be able to drill into their own client detail from the Book view? Assumed yes, but worth confirming. If no, §5.3 is admin-only and the scope shrinks.
3. **Admin "My Profile" toggle priority** — §5.5. Cut entirely, or follow-up after JWT claim lands?
4. **Commit bundling** — one commit or three-way split for §5.8?

---

## 9. Compiler tools used

Per TO gate, the tools I ran during this work:

| Tool | Purpose | Result |
|------|---------|--------|
| `Grep` / `Read` | Locate existing toggle patterns, HelperTip usage, fetch sites in `AdvisorsTab`, `ClientsTab`, `AdvisorPublicProfile` | Direct hit on each — no phantom deps |
| (`comp-transform schema-check`) | Would normally run for field rendering audit | **Not run this session.** Reason: changes are structural (prop plumbing, component extraction, toggle unification) rather than new data-field rendering. Existing fields already covered by previous audits; no new fields were consumed from the platinum payload. Worth running during §5.3 lift when L3/L4 fields touch new rendering paths. |

Will log this session in `logs/2026-04-10/` at commit time, including the compiler-tools line for `org/compiler-tools-log.md`.
