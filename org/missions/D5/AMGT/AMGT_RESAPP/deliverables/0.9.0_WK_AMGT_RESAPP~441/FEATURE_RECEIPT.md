# FEATURE RECEIPT -- AMGT-bm-1 (AMGT_RESAPP round 106)

Feature: the Security Analysis Model tab prints the price behind a historical P/E, gives every All-figures dash its reason, and shows a withheld forward P/E's served reason.

## What the branch carries

- Branch: `cand/dell1/amgt-sa-pe-basis-and-reasons` (portal repository, nested worktree `C:/dev/wk-resapp-441/portal`)
- Head commit: `9a1adc6e35834f1e5060dc3e9a677f4aff8cbb36` (LOCAL, not pushed)
- Base: PROD `7db035e4`
- Changed paths (`git diff --name-status 7db035e4 HEAD`):
  - `A src/pages/SecurityAnalysis/__harness__/basisAndReasons.harness.cjs`
  - `A src/pages/SecurityAnalysis/__harness__/basisFixture.GOOGL_US_Equity.json`
  - `A src/pages/SecurityAnalysis/__harness__/basisFixture.PBR_US_Equity.json`
  - `M src/pages/SecurityAnalysis/tabs/ModelTab.tsx`
  - `M src/pages/SecurityAnalysis/types.ts`

## Pages changed

| page | route | class | gate |
|---|---|---|---|
| Security Analysis | /security-analysis | Opal-internal | internal |

## Shared files

- none

## Not carried

Each path absent from the branch, with the count of its diff against the base (`git diff 7db035e4 HEAD -- <path> | wc -l`):

- `package.json`: 0
- `bun.lock`: 0
- `src/lib/firmAccess.ts`: 0
- `src/App.tsx`: 0

## How to look

- Dev build: `cd portal && bun run dev:live --port 5174`
- Page: `/security-analysis`, then the Model tab
- Names: `GOOGL US` (historical P/E price line under the 2025 P/E), `PBR US` (team P/E row), `ISP IM`
