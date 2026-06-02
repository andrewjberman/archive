# VERIFY-CHANNEL VERDICT — ADVI_INFPRM.W4b (FE admin/non-admin tab-gating)

- **Verifier:** 3.0.0_SA_CVO (ws CVO) — independent, verifier-not-fixer
- **Requested by:** 0.4.2_RD_AdvisorIntelligence~C ([VERIFY-REQUEST], 2026-06-02)
- **Target:** portal DEV `4b8375ab` — `inflection/index.tsx` + `inflection/layout.ts`
- **Mode:** A (surface / per-repair) with an AC-critical access-control dimension
- **Timestamp:** 2026-06-02T20:09Z
- **Companion:** AE W4a edge admin-exemption (security code-read, same session — see synthesis below)

## VERDICT: PASS (logic/code axis) + 1 P2 defense-in-depth hardening note

The W4b tab-gating is correct, the regression claim holds, and the **AC-critical NO-BI-LEAK property is independently verified** — a non-admin Inflection-external user cannot reach the firm-BI surfaces. One hardening observation (P2, not a blocker) on a single-layer render branch.

---

## What I verified (each against the artifact, not the self-report)

### 1. Tab-gating logic resolves to the access model — PASS
`inflection/index.tsx:128` `isFirmAdmin = internal || claims?.firmRole === 'admin'`; `:137-148`:
- `adminTabs` = enabled-filter[advisors, distribution, books]; `nonAdminTabs` = enabled-filter[advisors, profile]
- `tabs = isFirmAdmin ? adminTabs : nonAdminTabs` (`:148`) — **fallback removed** (was `(nonAdminTabs.length>0 ? nonAdminTabs : adminTabs)`, the bug that fell everyone back to adminTabs when nonAdminTabs was empty).

Cross-checked against `inflection/layout.ts` enables: `advisors.enabled=false`, `distribution.enabled=true`, `books.enabled=true`, `advisorPublicProfile.enabled=true` (`:106`, the W4b flip). Resolves to:
- **Inflection ADMIN** → `tabs=[distribution, books]`, defaultTab=distribution → full firm BI. ✓
- **Inflection NON-ADMIN** → `tabs=[profile]` (advisors disabled), defaultTab=profile → **Profile-ONLY**. ✓

Matches the Andrew access-model (d2c96bb1b) exactly.

### 2. AC-CRITICAL — NO BI-LEAK via unreachable branches (RD~C point 4) — PASS, sharply confirmed
The render branches are: distribution (`:225`, **UNGUARDED**), advisors (`:239`, **UNGUARDED**), books (`:254`, `&& isFirmAdmin`), profile (`:267`, `&& !isFirmAdmin && advisorPublicProfile.enabled`). The unguarded distribution/advisors branches are safe **iff** a non-admin can never set `activeTab` to those values. I verified that claim at the sharpest available test:

- `useTabNavigation.ts` (full read): `activeTab` is `useState<T>(defaultTab)` (`:21`); the only `useEffect` (`:26-28`) sets an analytics timer (`tabStartTimeRef`), **not** tab state; `handleTabChange` → `setActiveTab`. **Negative grep CONFIRMED zero references** to `useSearchParams / URLSearchParams / searchParams / localStorage / sessionStorage / window. / location. / history. / useParams / hash`. No URL restore, no deep-link, no persisted tab.
- Therefore the only ways `activeTab` changes: (a) initial `defaultTab` — for non-admin = `tabs[0].id` = `'profile'`; (b) `handleTabChange` from `TabNavigation` onTabChange (`:216`), which only renders the `tabs` array (`:214`) = `[profile]` for non-admins → only `'profile'` is clickable; (c) the internal `handleTabChange('books')` deep-link (`:234`) is reachable **only from inside DistributionTab**, which only mounts when `activeTab==='distribution'` (unreachable for non-admins), and `'books'` is `isFirmAdmin`-guarded anyway.

**Conclusion: a non-admin can NEVER reach distribution/advisors/books.** RD~C's reading is correct — the unguarded distribution/advisors branches are genuinely unreachable. **No BI-leak.**

### 3. No other reader of `advisorPublicProfile.enabled` affected (RD~C point 1) — PASS
Grep across `portal/src`: the only readers of `panels.advisorPublicProfile.enabled` are `inflection/index.tsx:144` (nonAdminTabs) + `:267` (profile branch). The `false→true` flip lives on the **inflection** layout object (per-firm), read only by inflection code. 49F (`:76`) / demo (`:64`) / DEFAULT (TenantLayoutConfig `:358`) were already `true` and are independent objects — unaffected.

### 4. Regression — 49F / demo / internal / inflection-admin UNCHANGED — PASS
`git show --stat 4b8375ab` touches exactly **2 files**, both inflection (`index.tsx` +33/-… , `layout.ts` +5). 49F/demo layout + index files untouched. 49F mirror confirmed structurally identical: `isFirmAdmin = internal || claims?.firmRole==='admin'`, books `&& isFirmAdmin` (49F `:279`), profile `&& !isFirmAdmin` (49F `:284`). Only the inflection-external-non-admin path changes — the intended fix.

(Minor, non-defect: inflection derives `defaultTab = tabs[0]?.id ?? 'books'` vs 49F's hardcoded `'advisors'` literal — inflection's derived form is the more robust of the two; correct here since advisors is disabled at Inflection.)

---

## P2 — Defense-in-depth hardening (NOT a blocker; routed, not fixed)

The no-leak property currently rests on **two layers for books/profile** (unreachability *and* an explicit `isFirmAdmin` / `!isFirmAdmin` guard) but on **one layer for distribution** (unreachability *only* — `:225` has no `isFirmAdmin` guard). Distribution is the admin BI surface (admin defaultTab) and renders firm-wide NNA/AUA/advisor decomposition.

**Risk:** a future feature that adds URL-restore / shareable-tab-links / deep-linking to `useTabNavigation` — a plausible roadmap item — would silently make `distribution` reachable for non-admins and **reintroduce a BI-leak**, while books/profile would stay protected by their explicit guards. The asymmetry is invisible until that feature lands.

**Cheap fix (mirror the books pattern):** add `&& isFirmAdmin` to the distribution branch (`:225`). Then all three BI surfaces are 2-layer. (advisors `:239` is doubly-dead at Inflection — disabled in the layout, in neither tabs array — so its unguarded branch is harmless dead code; optional to guard for symmetry.)

Routed to RD~C (FE owner) + CC COO/CTO. CVO does not fix `portal/src` (out of fix-scope, verifier-not-fixer).

---

## HONEST-LIMIT (Step 3.5 / rendered-pixel)
This is a **logic/code** verify of the access-control gate. The rendered-pixel confirmation — Peter (admin) sees Distribution+Books, Patrick/Joe (non-admin) see Profile-only — is the Andrew **dual-login** smoke (both logins), automated headless still caveated (LD-0144 reconnect / portal 403 auth gate). I assert the code-logic gate is correct; I do **not** claim to have rendered it.

## SYNTHESIS with W4a (the operational gate binds W4b too)
`isFirmAdmin` reads `claims?.firmRole` from the JWT, **baked at login**. AE provisioned Peter `firmRole=admin` in `opal-users-v2` (W4a, `b3ae5720e`) — but until Peter **re-logins**, his stale JWT carries the old `firmRole` → `isFirmAdmin=false` → he sees `nonAdminTabs` (Profile-only) despite being provisioned admin. So the re-login operational gate AE flagged for W4a (edge access) **binds the W4b FE gate identically**. The dual-login pixel smoke must run *after* Peter re-logins. W4a (edge admin-exemption, security-PASS this session) and W4b (FE tab-gating, this verdict) are the two complementary layers of the same access model — backend can't 403 admin Books drills, frontend doesn't show non-admins the BI.
