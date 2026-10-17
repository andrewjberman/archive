# FEATURE RECEIPT -- AMGT-bt-2 (0.9.0_WK_AMGT_RESAPP~501)

## What the branch carries

- Branch: `cand/dell1/amgt-sa-model-layout-repairs` (portal repository, nested worktree `C:/dev/wk-resapp-501/portal`)
- New head commit: `847c474b` (LOCAL, not pushed)
- Base: `856fb37b` (PROD)
- Paths changed since `856fb37b`:
  - `src/pages/SecurityAnalysis/__harness__/modelLayout.harness.cjs` (new)
  - `src/pages/SecurityAnalysis/components/StatTile.tsx`
  - `src/pages/SecurityAnalysis/tabs/ModelTab.tsx`

## Pages changed

| page | route | class | gate |
|---|---|---|---|
| Security Analysis | /security-analysis | Opal-internal | internal |

## Shared files

- none

## Not carried

- `package.json`: `git diff 856fb37b HEAD -- package.json | wc -l` = 0
- `bun.lock`: `git diff 856fb37b HEAD -- bun.lock | wc -l` = 0
- `src/lib/firmAccess.ts`: `git diff 856fb37b HEAD -- src/lib/firmAccess.ts | wc -l` = 0
- `src/App.tsx`: `git diff 856fb37b HEAD -- src/App.tsx | wc -l` = 0

## How to look

- Dev build: `cd portal && bun run dev:live --port 5174`
- Page: `/security-analysis`, name RIO LN, Model tab, the Earlier version select set to October 16th, 2026.
- Hover a figure in the Model tab: its bubble now ranks at z-50 (Z_INDEX.dropdown).
- The "All figures" fold: the label column wraps long labels (whitespace-normal, break-words). Confirm the grid's horizontal scroll and the bubble over the list below the grid in a real browser.

## What the checks prove and cannot prove

- The harness `modelLayout.harness.cjs` reads class lists in a static react-dom/server render. It proves the markup carries the classes named (z-50 on the bubble, wrap classes on the label cells, overflow-x-auto on the grid scroller with no scrollbar-hiding class on its chain), that the served text is unchanged (M5 digest 8e69f1aa...), and that the existing harnesses still pass.
- It cannot prove that a tooltip is or is not covered on screen, nor that text is or is not cut off. A static render has no layout engine. The real-browser walk after the merge grades the effect.
- Repair A's z-index change addresses stacking only. The structural reading shows no stacking context traps the bubble; the walker's cover is most likely the overflow-x-auto scroller clipping the bubble below the grid. That is filed as a surprise row (see the investigation file), not fixed in this branch.
