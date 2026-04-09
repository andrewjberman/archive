# ADHC_DESIGN.031 — Lint Cleanup: Pod 0.3 (TradingOperations)

**Owner:** `0.3.0_DE_TradingOperations`
**From:** `1.0.0_SA_CTO`
**Project:** `ADHC_DESIGN` (Phase 2 — carryover from DEBT_1STRUN)
**Depends on:** Nothing
**Priority:** Medium
**Status:** PENDING

---

## Background

~200 ESLint warnings remain across the portal frontend from DEBT_1STRUN. Every DE pod is doing lint cleanup in their own domain concurrently.

Pod 0.3 has no files in the tooltip migration scope (no data tooltips flagged in the unification report), so this TO is your only ADHC_DESIGN phase 2 deliverable.

---

## Scope — your pod's domain

Run `bun run lint` from `portal/` and fix all warnings in files under:

- `portal/src/pages/PortfolioManagement/**`
- `portal/src/pages/TradeSubmission/**` (if exists)
- `portal/src/pages/DataRefresh/**`
- `portal/src/pages/SecurityScanner/**`
- `portal/src/pages/Trade/**` (if exists)
- Any top-level shared component in `portal/src/components/` whose primary consumer is a pod 0.3 page (check via `grep -r "ComponentName" src/pages/`)

**Do NOT touch files owned by other pods.**

---

## Deliverables

1. **Baseline:**
   ```bash
   bun run lint 2>&1 | tee /tmp/lint-before-pod-0.3.txt
   grep -c "warning" /tmp/lint-before-pod-0.3.txt
   ```

2. **Fix all warnings in your domain.** Same playbook as the other pod lint TOs:

   | Warning | Fix |
   |---------|-----|
   | `'X' is defined but never used` | Delete. Use `import type { X }` if still needed. |
   | `Unexpected any` | Real type. `unknown` + narrowing. Last resort: disable with comment. |
   | `React Hook missing dependency` | Add dep or wrap in `useCallback`/`useMemo`. Disable with justification if stable. |
   | `Empty catch block` | Log, re-throw, or `// noop`. |
   | `Prefer const` | Change `let` to `const`. |

3. **Regression check.** After each file:
   - `bun run build` succeeds
   - Visit the page in `bun run dev` — no functional regression
   - For trade submission / portfolio management pages specifically, double-check that any form validation or API fetch hooks behave correctly after dep array changes (those pages have more stateful logic than most)

4. **Final measurement:**
   ```bash
   bun run lint 2>&1 | tee /tmp/lint-after-pod-0.3.txt
   grep -c "warning" /tmp/lint-after-pod-0.3.txt
   ```

---

## Rules of engagement

- No blanket `eslint-disable`. Every disable gets a comment.
- No refactoring beyond lint fixes.
- No file moves or export renames.
- If a warning requires cross-pod changes, defer and list in commit message.

---

## Validation

- `bun run lint` shows zero warnings in files under your pod's domain
- `bun run build` succeeds
- All pod 0.3 pages render + function without regression (especially form/submission flows)

Commit message: `chore(portal): pod 0.3 lint cleanup — X warnings resolved (ADHC_DESIGN.031)`

Ping `1.0.0_SA_CTO` when done.
