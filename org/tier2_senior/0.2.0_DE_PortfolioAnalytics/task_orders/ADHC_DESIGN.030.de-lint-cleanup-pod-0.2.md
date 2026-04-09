# ADHC_DESIGN.030 — Lint Cleanup: Pod 0.2 (PortfolioAnalytics)

**Owner:** `0.2.0_DE_PortfolioAnalytics`
**From:** `1.0.0_SA_CTO`
**Project:** `ADHC_DESIGN` (Phase 2 — carryover from DEBT_1STRUN)
**Depends on:** Nothing — can run concurrent with ADHC_DESIGN.027
**Priority:** Medium
**Status:** PENDING

---

## Background

~200 ESLint warnings remain across the portal frontend as a result of the DEBT_1STRUN scan. Piggybacking cleanup onto the active DE work cycle while tooltip migration is in flight.

---

## Scope — your pod's domain

Run `bun run lint` from `portal/` and fix all warnings in files under:

- `portal/src/pages/Positioning/**`
- `portal/src/pages/Attribution/**`
- `portal/src/pages/FactorTilts/**`
- `portal/src/pages/Valuation/**`
- `portal/src/pages/Macroeconomics/**`
- `portal/src/pages/Correlation/**`
- Any top-level shared component in `portal/src/components/` whose primary consumer is a pod 0.2 page (check via `grep -r "ComponentName" src/pages/`)

**Do NOT touch files owned by other pods** — that's TO-029 (pod 0.1), .031 (pod 0.3), .032 (pod 0.4).

---

## Deliverables

1. **Baseline measurement:**
   ```bash
   bun run lint 2>&1 | tee /tmp/lint-before-pod-0.2.txt
   grep -c "warning" /tmp/lint-before-pod-0.2.txt
   ```
   Record total + per-file counts for your domain.

2. **Fix all warnings in your domain.** Common patterns:

   | Warning | Fix |
   |---------|-----|
   | `'X' is defined but never used` | Delete the import/variable. Use `import type { X }` if only needed as a type. |
   | `Unexpected any. Specify a different type` | Replace with real type. `unknown` + narrowing if truly unknown. Last resort: disable with comment. |
   | `React Hook useEffect has a missing dependency` | Add the dep. If intentionally stable, wrap in `useCallback`/`useMemo` or disable with justification. |
   | `Empty catch block` | Log, re-throw, or `// noop` comment. |
   | `Prefer const` | Change `let` to `const`. |

3. **Regression check.** After each file:
   - `bun run build` succeeds
   - Visit the page in `bun run dev` — no functional regression
   - If hook dep changes could affect behavior (fetch timing, re-render loops), test the affected path

4. **Final measurement:**
   ```bash
   bun run lint 2>&1 | tee /tmp/lint-after-pod-0.2.txt
   grep -c "warning" /tmp/lint-after-pod-0.2.txt
   ```
   Report delta in commit message.

---

## Rules of engagement

- No blanket `eslint-disable`. Every disable gets a comment explaining why.
- No refactoring beyond lint fixes. Deeper smells are a separate conversation.
- No file moves or export renames.
- If a warning requires cross-pod changes, defer and list it in the commit message.

---

## Validation

- `bun run lint` shows zero warnings in files under your pod's domain
- `bun run build` succeeds
- All pod 0.2 pages render without regression

Commit message: `chore(portal): pod 0.2 lint cleanup — X warnings resolved (ADHC_DESIGN.030)`

Ping `1.0.0_SA_CTO` when done.
