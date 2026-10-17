# FEATURE RECEIPT -- AMGT-bt-6 (the Model tab's last-row figure tooltips open upward)

Task order: `AMGT_RESAPP.TO-AMGT-bt-6.model-last-rows-tooltip-upward` (worker `0.9.0_WK_AMGT_RESAPP~503`).

## What the branch carries

- Branch: `cand/dell1/amgt-sa-model-tooltip-last-rows` (portal repository, nested worktree `C:/dev/wk-resapp-503/portal`).
- Head: `be136f28` (LOCAL, not pushed).
- Base: `856fb37b` (PROD).
- Paths changed since `856fb37b` (`git diff --name-only 856fb37b HEAD`):
  - `src/pages/SecurityAnalysis/components/StatTile.tsx`
  - `src/pages/SecurityAnalysis/tabs/ModelTab.tsx`
  - `src/pages/SecurityAnalysis/__harness__/modelTooltipRows.harness.cjs` (new)

What changed, in words: `FigureTooltip` takes a third placement, `above-wide` (opens upward, not capped to the anchor width). `ModelTab` passes it to the figure cells of the last `min(12, floor(N / 2))` rows of the "All figures" grid, where N is the count of grid rows that render figure cells. Every other row keeps the default `below`. `above` (the header cards) and `below` are byte-identical. No served value, figure, sentence or grid markup changes.

## Pages changed

| page | route | class | gate |
|---|---|---|---|
| Security Analysis | /security-analysis | Opal-internal | internal |

## Shared files

- none

## Not carried

- `package.json` -- `git diff 856fb37b HEAD -- package.json | wc -l` = 0
- `bun.lock` -- `git diff 856fb37b HEAD -- bun.lock | wc -l` = 0
- `src/lib/firmAccess.ts` -- `git diff 856fb37b HEAD -- src/lib/firmAccess.ts | wc -l` = 0
- `src/App.tsx` -- `git diff 856fb37b HEAD -- src/App.tsx | wc -l` = 0

## How to look

- Dev build: `cd portal && bun run dev:live --port 5174`.
- Page: `/security-analysis`, name RIO LN, Model tab, set `Earlier version` to October 16th, 2026, open the "All figures" fold.
- Hover a figure in the last 12 rows of the grid: its tooltip opens upward. Hover a figure in an earlier row: its tooltip opens downward, as before.

## What the checks prove and what they do not

- The harness `modelTooltipRows.harness.cjs` is a STRUCTURAL check on a static render (react-dom/server). It reads which class each figure tooltip carries, which fixes the direction the stylesheet opens it. It proves the class placement for the RIO LN grid and for a synthetic 6-row grid; it proves the served text is unchanged apart from class attributes.
- It does NOT prove that the scroller stops clipping. A static render has no layout engine. The real grade is the issuer's real-browser walk after the merge (`occluded-popover` on RIO LN, Model tab, Earlier version 2026-10-16).
