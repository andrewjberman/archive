# FEATURE RECEIPT -- AMGT_RESAPP bt-1 (earnings dates in the long form)

## What the branch carries

- Branch: `cand/dell1/amgt-sa-earnings-long-dates` (nested portal repository `C:/dev/wk-resapp-500/portal`)
- Head commit: `c4e4f96af33ed086e5e36cc90274667400dfc0fe` (LOCAL, not pushed)
- Base: `856fb37b` (PROD)
- Every path changed since `856fb37b`:
  - `src/pages/SecurityAnalysis/components/model/WhatChangedPanel.tsx`
  - `src/pages/SecurityAnalysis/__harness__/earningsLongDates.harness.cjs` (new)
  - `src/pages/SecurityAnalysis/__harness__/changedListValue.harness.cjs`
  - `src/pages/SecurityAnalysis/__harness__/changedObjectCells.harness.cjs`
  - `src/pages/SecurityAnalysis/__harness__/changedObjectFixture.base_rio_row.txt`

## Pages changed

| page | route | class | gate |
| --- | --- | --- | --- |
| Security Analysis | /security-analysis | Opal-internal | internal |

## Shared files

- none

## Not carried

- `package.json`: absent; `git diff 856fb37b HEAD -- package.json | wc -l` = 0
- `bun.lock`: absent; `git diff 856fb37b HEAD -- bun.lock | wc -l` = 0
- `src/lib/firmAccess.ts`: absent; `git diff 856fb37b HEAD -- src/lib/firmAccess.ts | wc -l` = 0
- `src/App.tsx`: absent; `git diff 856fb37b HEAD -- src/App.tsx | wc -l` = 0

## How to look

- Dev build: `cd portal && bun run dev:live --port 5174`
- Page: `/security-analysis`, names RIO LN and ICT PM, Model tab, What Changed, the earnings row (older version pairs). The visible Before and After cells and the expanded "Full figures" detail print announcement dates as "October 13th, 2026 (2026:Q3), 135 entries" and so on.
