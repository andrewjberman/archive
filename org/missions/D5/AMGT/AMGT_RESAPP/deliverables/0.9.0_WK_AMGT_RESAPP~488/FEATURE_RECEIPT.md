# FEATURE RECEIPT -- AMGT_RESAPP bp-1 (`AMGT-bp-1`, round 109)

Feature: a changed figure whose value is a list no longer crashes the Security Analysis Model tab (RIO LN).
Issued to: `0.9.0_WK_AMGT_RESAPP~488`, issued by `2.0.0_SA_COO~R1`.

## What the branch carries

- Branch: `cand/dell1/amgt-sa-changed-list-value` (nested portal checkout, never pushed)
- Head commit: `d060d119b95880029453f00582caea0f66ee3699` (LOCAL, on the branch). Commits since base: `bfd4ec6d` harness, fixtures and base files; `25afc84c` the list-value fix; `01c53022` AMENDMENT 1 (date-row length, sign-first money); `d060d119` harness docblock.
- Base: `15bc21b304d4b0a150a9cdd0c1b75251f0b8c2a8` (PROD `15bc21b3`)
- Changed paths (7, all under `portal/`):
  - `src/pages/SecurityAnalysis/components/model/WhatChangedPanel.tsx`
  - `src/pages/SecurityAnalysis/__harness__/changedListValue.harness.cjs`
  - `src/pages/SecurityAnalysis/__harness__/changedListFixture.RIO_LN_compare.json`
  - `src/pages/SecurityAnalysis/__harness__/changedListFixture.RIO_LN_Equity.json`
  - `src/pages/SecurityAnalysis/__harness__/changedListFixture.base_row.json`
  - `src/pages/SecurityAnalysis/__harness__/changedListFixture.base_zurn.sha256`
  - `src/pages/SecurityAnalysis/__harness__/changedListFixture.base_money.json`

## Pages changed

| page | route | class | gate |
|---|---|---|---|
| Security Analysis | /security-analysis | Opal-internal | internal |

## Shared files

- none

## Not carried

Each path absent from the branch: `git diff 15bc21b3 HEAD -- <path> | wc -l` reads 0.

- `package.json`: 0
- `bun.lock`: 0
- `src/lib/firmAccess.ts`: 0
- `src/App.tsx`: 0

## How to look

- Dev build: `cd portal && bun run dev:live --port 5174`
- Page: `/security-analysis`, name `RIO LN`, its Model tab; the What changed panel lists the header figure `ERN_ANN_DT_AND_PER` (earnings dates), which before this branch threw and blanked the page.
