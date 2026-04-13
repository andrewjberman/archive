# ADHC_DESIGN.032 — Lint Cleanup: Pod 0.4 (ClientPlatform)

**Owner:** `0.4.0_DE_ClientPlatform`
**From:** `1.0.0_SA_CTO`
**Project:** `ADHC_DESIGN` (Phase 2 — carryover from DEBT_1STRUN)
**Depends on:** Nothing — can run concurrent with tooltip work (.025/.028)
**Priority:** Medium
**Status:** COMPLETE (with follow-up — see ADHC_DESIGN.033 below)
<!-- portal DEV f3274f3 2026-04-13. Pod-0.4 lint count 23 -> 16 warnings.
     Cleared 5 react-hooks/rules-of-hooks violations (real bugs: useMemo/
     useCallback below early returns in AdvisorsTab + FeeEfficiencyPanel)
     plus 1 unused-imports auto-fix.
     Remaining 16 warnings = 15 react-hooks/set-state-in-effect + 1
     react-hooks/refs. All on intentional state-resync effects (cohort
     changes resetting drill state, etc.) — perf hints, not bugs. Each
     needs an effect-restructure with regression risk; deferred to a
     dedicated effect-refactor pass. Tracked as ADHC_DESIGN.033 (TBD). -->


---

## Background

~200 ESLint warnings remain across the portal frontend from DEBT_1STRUN. Each DE pod is doing lint cleanup in their own domain concurrently with the tooltip unification work.

Pod 0.4 likely has the largest lint surface (AdvisorIntelligence has the most active development and therefore accumulated the most drift). Plan accordingly.

---

## Scope — your pod's domain

Run `bun run lint` from `portal/` and fix all warnings in files under:

- `portal/src/pages/AdvisorIntelligence/**` (all of it — tabs, components, ClientDetail, panels)
- `portal/src/pages/ModelPortfolios.tsx` and related files
- `portal/src/pages/Books/**` (if exists) — Books is your domain too
- `portal/src/components/AccountDistributionChart.tsx` (pod 0.4 primary consumer)
- `portal/src/components/ReturnVolatilityScatter.tsx` (pod 0.4 primary consumer)
- Any other shared component primarily consumed by pod 0.4 pages
- `portal/src/components/DataTooltip.tsx` (created in TO-025 — your ownership)

**Do NOT touch files owned by other pods** — that's TO-029/.030/.031.

---

## Deliverables

1. **Baseline:**
   ```bash
   bun run lint 2>&1 | tee /tmp/lint-before-pod-0.4.txt
   grep -c "warning" /tmp/lint-before-pod-0.4.txt
   ```
   Record total + per-file counts. Pod 0.4 likely has the highest density; expect the biggest delta.

2. **Fix all warnings in your domain.** Standard playbook:

   | Warning | Fix |
   |---------|-----|
   | `'X' is defined but never used` | Delete. Use `import type { X }` if only used as a type. |
   | `Unexpected any` | Real type. `unknown` + narrowing. Disable with comment as last resort. |
   | `React Hook missing dependency` | Add the dep. For stable refs/setters, wrap in `useCallback`/`useMemo` or disable with justification. |
   | `Empty catch block` | Log, re-throw, or `// noop`. |
   | `Prefer const` | Change `let` to `const`. |

3. **Pod-specific gotchas.**

   AdvisorIntelligence tabs have a lot of `useEffect`/`useMemo` chains around fetch + transform + derive. Hook dependency warnings in these files are the **most dangerous to blindly fix** — wrong dep arrays can cause infinite re-fetch loops or stale data. For every hook dep fix in ADVI:
   - Read the useEffect body and understand what it depends on
   - If the warning suggests a dep that would cause a refetch loop, wrap the offending value in `useMemo` / `useCallback` at its source instead of adding it to the dep array
   - Test the affected tab in `bun run dev` — watch DevTools Network tab for runaway requests
   - If in doubt, document the decision in a comment above the hook

   The ClientsTab, AdvisorsTab, and DistributionTab in particular have fetch chains that depend on selectedFirm/selectedAdvisor/selectedClient state — fix those carefully.

4. **Regression check.** After each file:
   - `bun run build` succeeds
   - Visit the ADVI pages, ModelPortfolios, Books — no visible regression, no console errors
   - Watch the Network tab for any new runaway refetch behavior after hook dep changes

5. **Final measurement:**
   ```bash
   bun run lint 2>&1 | tee /tmp/lint-after-pod-0.4.txt
   grep -c "warning" /tmp/lint-after-pod-0.4.txt
   ```

---

## Rules of engagement

- No blanket `eslint-disable`. Every disable gets a comment with a justification.
- No refactoring beyond lint fixes — if a file smells bad, leave it and raise it separately.
- No file moves or export renames.
- Hook dep fixes in ADVI files require extra scrutiny — wrong fixes break the whole dashboard. If unsure, defer and flag it to CTO.
- If a warning requires cross-pod changes, defer and list in commit message.

---

## Compiler Tool

Run `comp-tooltip summary` after your lint work to confirm no tooltip drift was introduced. The tooltip migration itself is in .025/.028.

## Validation

- `bun run lint` shows zero warnings in files under your pod's domain
- `bun run build` succeeds
- ADVI dashboard fully functional — all tabs render, fetches complete once (no infinite loops), selectors update cleanly
- ModelPortfolios renders without regression
- Commit message includes before/after warning counts + any deferrals

Commit message: `chore(portal): pod 0.4 lint cleanup — X warnings resolved (ADHC_DESIGN.032)`

Ping `2.0.0_SA_COO` when done.
