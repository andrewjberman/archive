# FEATURE RECEIPT -- AMGT-br-1 (AMGT_RESAPP round 111): an object-valued What Changed cell renders as readable text

Serial: 0.9.0_WK_AMGT_RESAPP~493. Cell: AMGT-br-1. Nested portal worktree: `C:/dev/wk-resapp-493/portal`.

## What the branch carries

- Branch: `cand/dell1/amgt-sa-changed-object-cells` (nested portal repository, cut from PROD `99d2b2a7`; never pushed).
- New head commit: `164c9fd58da4a5fae9ebb3d1ee5aa984c918886f` (LOCAL, `git log -1` in the nested worktree).
- Base: `99d2b2a7` (PROD).
- Every path changed since `99d2b2a7` (`git diff --name-only 99d2b2a7 HEAD`):
  - `src/pages/SecurityAnalysis/components/model/WhatChangedPanel.tsx`
  - `src/pages/SecurityAnalysis/__harness__/changedObjectCells.harness.cjs`
  - `src/pages/SecurityAnalysis/__harness__/changedObjectFixture.base_digests.json`
  - `src/pages/SecurityAnalysis/__harness__/changedObjectFixture.base_rio_row.txt`

## Pages changed

| page | route | class | gate |
|---|---|---|---|
| Security Analysis | /security-analysis | Opal-internal | internal |

## Shared files

- none

## Not carried

- `package.json`: `git diff 99d2b2a7 HEAD -- package.json | wc -l` = 0
- `bun.lock`: `git diff 99d2b2a7 HEAD -- bun.lock | wc -l` = 0
- `src/lib/firmAccess.ts`: `git diff 99d2b2a7 HEAD -- src/lib/firmAccess.ts | wc -l` = 0
- `src/App.tsx`: `git diff 99d2b2a7 HEAD -- src/App.tsx | wc -l` = 0

## How to look

- `cd portal && bun run dev:live --port 5174`
- Open `/security-analysis` on RIO LN and ICT PM, Model tab, What Changed. Both names are controls: their rows print exactly as on PROD (RIO LN earnings-dates row: "<announcement_date> (<period>), <n> entries").
- The object-valued cell is exercised by the harness on a synthetic compare, not by live data: `node src/pages/SecurityAnalysis/__harness__/changedObjectCells.harness.cjs` (from the portal root) prints `CHANGED OBJECT CELLS HARNESS: YES (6 of 6 checks)`.
