# FEATURE RECEIPT -- AMGT-bl-1 (round 105), 0.9.0_WK_AMGT_RESAPP~419

## What the branch carries

- branch: `cand/dell1/amgt-sa-currency-symbol-and-reasons` (nested portal worktree `C:/dev/wk-resapp-419/portal`)
- head commit: `051ad362d4dd1deb8c2db9725d3403d748a66f0e` (LOCAL, not pushed; the first portal commit `901f27fb70cad498ce1aae0500592b514fca4180` carries items 1 and 3, the second carries item 2)
- base: `7d5cb34daabce225bb9a2635c541f6ff3fd64e52` (PROD 7d5cb34d)
- changed paths (portal-relative, eight, all under `src/pages/SecurityAnalysis/`):
  - `src/pages/SecurityAnalysis/modelSheet.ts`
  - `src/pages/SecurityAnalysis/tabs/ModelTab.tsx`
  - `src/pages/SecurityAnalysis/types.ts`
  - `src/pages/SecurityAnalysis/components/SegmentTable.tsx`
  - `src/pages/SecurityAnalysis/__harness__/currencyAndReasons.harness.cjs`
  - `src/pages/SecurityAnalysis/__harness__/currencyFixture.PBR_US_Equity.json`
  - `src/pages/SecurityAnalysis/__harness__/currencyFixture.BATS_LN_Equity.json`
  - `src/pages/SecurityAnalysis/__harness__/currencyFixture.BATS_SEGMENT.json`

## Pages changed

| page | route | class | gate |
|---|---|---|---|
| Security Analysis | /security-analysis | Opal-internal | internal |

## Shared files

- none

## Not carried

- `package.json`: absent; `git diff 7d5cb34d HEAD -- package.json | wc -l` = 0
- `bun.lock`: absent; `git diff 7d5cb34d HEAD -- bun.lock | wc -l` = 0
- `src/lib/firmAccess.ts`: absent; `git diff 7d5cb34d HEAD -- src/lib/firmAccess.ts | wc -l` = 0
- `src/App.tsx`: absent; `git diff 7d5cb34d HEAD -- src/App.tsx | wc -l` = 0

## Harness at this head

- `CURRENCY AND REASONS HARNESS: YES (10 of 10 checks)`. C4 is now over the page's own `SegmentTable`: C4a (BATS LN served table: no `Period 4` header, the four other columns keep their figures, the sentence once), C4b (a table with no empty column: no sentence), C4c (a synthetic empty column dropped and said once). Surprise row `AMGT_RESAPP-D1-W419-S1` (its premise was the order's; the amendment corrected the location to the Thesis tab's segment table) is closed by the amendment.

## How to look

- `cd portal && bun run dev:live --port 5174`
- page: `/security-analysis`; names: `PBR US` (team Revenue prints `BRL`; the other team money rows with no served currency print no symbol), `BATS LN` (Thesis tab: the segment table has no `Period 4` column and one sentence says why), `GOOGL US` (its Key Figures dashes; not checked by the harness, which reads only the slices)
