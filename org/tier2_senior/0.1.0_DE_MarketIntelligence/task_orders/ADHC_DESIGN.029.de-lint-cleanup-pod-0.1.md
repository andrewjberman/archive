# ADHC_DESIGN.029 — Lint Cleanup: Pod 0.1 (MarketIntelligence)

**Owner:** `0.1.0_DE_MarketIntelligence`
**From:** `1.0.0_SA_CTO`
**Project:** `ADHC_DESIGN` (Phase 2 — carryover from DEBT_1STRUN)
**Depends on:** Nothing — can run concurrent with ADHC_DESIGN.026
**Priority:** Medium
**Status:** COMPLETE

---

## Background

~200 ESLint warnings remain across the portal frontend as a result of the DEBT_1STRUN scan work. Most are low-severity (unused imports, `any` types, missing dependencies in `useEffect`/`useMemo` hooks, empty catch blocks). Since DEs are already active on the tooltip unification, we're piggybacking lint cleanup onto the same work cycle.

---

## Scope — your pod's domain

Run `bun run lint` from `portal/` and fix all warnings in files under:

- `portal/src/pages/MarketPerformance/**`
- `portal/src/pages/CapitalMarketAssumptions/**`
- `portal/src/pages/CausalityEngine/**`
- `portal/src/components/market-performance/**`
- `portal/src/components/market-overview/**` (if exists)
- Any top-level shared component in `portal/src/components/` whose primary consumer is a pod 0.1 page (check via `grep -r "ComponentName" src/pages/`)

**Do NOT touch files owned by other pods** — that's covered in TO-030 (pod 0.2), .031 (pod 0.3), and .032 (pod 0.4).

---

## Deliverables

1. **Baseline measurement.** Before any edits, run:
   ```bash
   bun run lint 2>&1 | tee /tmp/lint-before-pod-0.1.txt
   grep -c "warning" /tmp/lint-before-pod-0.1.txt
   ```
   Record the total count and the per-file count for files in your domain.

2. **Fix all warnings in your domain.** Common patterns and how to resolve:

   | Warning | Fix |
   |---------|-----|
   | `'X' is defined but never used` | Delete the import/variable. If it's a type-only import, use `import type { X }` if still needed. |
   | `Unexpected any. Specify a different type` | Replace with the real type. If truly unknown, use `unknown` and narrow before use. Last resort: `// eslint-disable-next-line @typescript-eslint/no-explicit-any` with a comment explaining why. |
   | `React Hook useEffect has a missing dependency` | Add the dep. If intentionally stable (like a ref or a setter), wrap in `useCallback`/`useMemo` or add a `// eslint-disable-next-line react-hooks/exhaustive-deps` with justification. |
   | `Empty catch block` | Either log the error, re-throw, or add an intentional `// noop` comment. |
   | `Prefer const` | Change `let` to `const`. |

3. **Regression check.** After each file's fixes:
   - `bun run build` must succeed
   - Visit the affected page in `bun run dev` and confirm no functional regression
   - If a fix changes hook dependencies in a way that might affect behavior, test the hover/click/fetch path explicitly

4. **Final measurement.** After all fixes:
   ```bash
   bun run lint 2>&1 | tee /tmp/lint-after-pod-0.1.txt
   grep -c "warning" /tmp/lint-after-pod-0.1.txt
   ```
   Report delta in the commit message.

---

## Rules of engagement

- **Do not silence warnings with blanket disables.** Every `eslint-disable` you add must have a comment explaining why.
- **Do not refactor beyond fixing warnings.** If a file has a deeper code smell unrelated to lint, leave it alone — that's a separate conversation.
- **Do not move files or rename exports.** Lint fixes should be intra-file changes only.
- **If a warning is hard to fix** (e.g. requires a major refactor or touches files outside your pod), skip it and list it in your commit message as "deferred — reason: X". CTO will triage deferrals.

---

## Compiler Tool

Run `comp-tooltip summary` after your lint work to confirm no tooltip drift was introduced. This is informational — the tooltip migration itself is in .026.

## Validation

- `bun run lint` shows zero warnings in files under your pod's domain
- `bun run build` succeeds
- All affected pages render without visible regression
- Commit message includes before/after warning counts and any deferrals

Commit message: `chore(portal): pod 0.1 lint cleanup — X warnings resolved (ADHC_DESIGN.029)`

Ping `2.0.0_SA_COO` when done.
