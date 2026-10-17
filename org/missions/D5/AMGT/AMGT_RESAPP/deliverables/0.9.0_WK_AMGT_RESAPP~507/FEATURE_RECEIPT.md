# FEATURE RECEIPT -- AMGT_RESAPP AMGT-bu-4 (model-grid-scroll-cue)

Issued to `0.9.0_WK_AMGT_RESAPP~507` by `2.0.0_SA_COO~R1`, round 114, decomposition s.123.

## What the branch carries

- Branch: `cand/dell1/amgt-sa-model-grid-scroll-cue` (nested portal worktree `C:/dev/wk-resapp-507/portal`), LOCAL, never pushed.
- Base: PROD `d1bed0fb`.
- Head commit: `9fb741c14f04b7e946b5eea308118eb67a001002` (subject: `AMGT_RESAPP AMGT-bu-4: the All figures grid shows that it scrolls sideways`).
- Paths changed since `d1bed0fb` (`git diff --name-only d1bed0fb HEAD`):
  - `src/pages/SecurityAnalysis/tabs/ModelTab.tsx` (2 insertions: the cue line and the scroller line with its new classes; 1 deletion: the old scroller line; see `git diff d1bed0fb HEAD`)
  - `src/pages/SecurityAnalysis/__harness__/gridScrollCue.harness.cjs` (new, 271 lines)

## Pages changed

| page | route | class | gate |
|---|---|---|---|
| Security Analysis | /security-analysis | Opal-internal | internal |

## Shared files

- none

## Not carried

Each path absent from the branch; the count is `git diff d1bed0fb HEAD -- <path> | wc -l`, measured at head `9fb741c1`.

- `package.json`: 0
- `bun.lock`: 0
- `src/lib/firmAccess.ts`: 0
- `src/App.tsx`: 0

## How to look

- Dev build: `cd portal && bun run dev:live --port 5174`
- Page: `/security-analysis`, the RIO LN security, the Model tab, open the `All figures` fold.
- What to see: the caption `Scroll sideways to see every year.` directly above the grid, and a visible navy horizontal scrollbar thumb on the grid's bottom edge when the fold is open.
- The saved value of every figure is unchanged; only the caption and the scrollbar paint are new.

## What the checks prove and what they cannot

- The harness `gridScrollCue.harness.cjs` is a STATIC render (`react-dom/server`, RIO LN fixture). It proves the markup: one cue element inside the closed fold before the grid table (S1), the scroller's thumb class is not transparent and no scrollbar-hiding class is present (S2), the served text is unchanged apart from the cue sentence (S3), and the fold holds the cue (S5).
- It cannot prove that the thumb paints, that it is visible in a browser, or where the caption lands on screen. There is no layout engine or pixels in a static render. The grade is the issuer's real-browser screenshot read after the merge.
- Cascade caution for that read: `src/index.css` section 6 (`SCROLLBAR STYLING`) is UNLAYERED, and Tailwind v4 emits utilities in a cascade layer, so an unlayered `::-webkit-scrollbar-thumb { background: transparent }` can win over the arbitrary thumb utility regardless of specificity. The branch does not edit `src/index.css` (the order forbids it), so the thumb colour may not paint. This is recorded as a surprise row for the issuer.
- S4 (the round-113 `modelTooltipRows.harness.cjs` still reading `YES (9 of 9 checks)`) does NOT hold on this branch: its B5 digests the whole served Model tab text, and the cue sentence adds 65 characters to it. Its B1 to B4 and the B3 placement controls pass. See the surprise row in `org/missions/D5/AMGT/AMGT_RESAPP/surprise-channel/investigations/INVESTIGATION_v1.md`.
