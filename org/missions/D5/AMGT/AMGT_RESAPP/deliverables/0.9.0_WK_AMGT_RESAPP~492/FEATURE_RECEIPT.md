# FEATURE RECEIPT -- AMGT-bq-1 (round 110): the What Changed detail as text, and the USD money code

## What the branch carries

- Branch: `cand/dell1/amgt-sa-changed-list-value` (nested portal worktree `C:/dev/wk-resapp-492/portal`), the bp-1 candidate.
- New head commit: `bc0a5cd9` (full `bc0a5cd911f1d50b59b22a13af0c90239c3fd165`), LOCAL only, not pushed.
- Previous head: `d060d119` (full `d060d119b95880029453f00582caea0f66ee3699`).
- Base: `15bc21b3` (full `15bc21b304d4b0a150a9cdd0c1b75251f0b8c2a8`, PROD).
- Changed paths since the previous head (`git diff --name-only d060d119 HEAD`, 4 files):
  - `src/pages/SecurityAnalysis/__harness__/changedListFixture.ICT_PM_compare.json`
  - `src/pages/SecurityAnalysis/__harness__/changedListFixture.ICT_PM_header.json`
  - `src/pages/SecurityAnalysis/__harness__/changedListValue.harness.cjs`
  - `src/pages/SecurityAnalysis/components/model/WhatChangedPanel.tsx`
- Changed paths since the base (`git diff --name-only 15bc21b3 HEAD`, 9 files):
  - `src/pages/SecurityAnalysis/__harness__/changedListFixture.ICT_PM_compare.json`
  - `src/pages/SecurityAnalysis/__harness__/changedListFixture.ICT_PM_header.json`
  - `src/pages/SecurityAnalysis/__harness__/changedListFixture.RIO_LN_Equity.json`
  - `src/pages/SecurityAnalysis/__harness__/changedListFixture.RIO_LN_compare.json`
  - `src/pages/SecurityAnalysis/__harness__/changedListFixture.base_money.json`
  - `src/pages/SecurityAnalysis/__harness__/changedListFixture.base_row.json`
  - `src/pages/SecurityAnalysis/__harness__/changedListFixture.base_zurn.sha256`
  - `src/pages/SecurityAnalysis/__harness__/changedListValue.harness.cjs`
  - `src/pages/SecurityAnalysis/components/model/WhatChangedPanel.tsx`

What the feature does (display only; no served value, figure or existing sentence changes):

1. The expanded "Full figures" detail of a changed row never prints raw JSON. The earnings-dates list prints its newest five entries as `<announcement_date> (<period>)` joined by `; `, then `; <n> entries in all`. Any other list prints `<n> entries`; an object prints `key: value` pairs. The visible row text is unchanged.
2. A money figure served in USD on a name whose PX_LAST price currency is another code prints `USD ` and the amount (before, after and change cells; ICT PM enterprise value reads `USD 33.11B`). `$` is kept where the price currency is USD or none is served.
3. A negative header money figure prints its sign first (`-USD 33.09B`).

## Pages changed

| page | route | class | gate |
|---|---|---|---|
| Security Analysis | /security-analysis | Opal-internal | internal |

No other page is changed.

## Shared files

- none

## Not carried

Each path is absent from the branch; the count is `git diff 15bc21b3 HEAD -- <path> | wc -l`, measured at `bc0a5cd9`.

- `package.json`: 0
- `bun.lock`: 0
- `src/lib/firmAccess.ts`: 0
- `src/App.tsx`: 0

## How to look

- Dev build: `cd portal && bun run dev:live --port 5174` (on the candidate branch).
- Page: `/security-analysis`, Model tab, What Changed. Names `RIO LN` (expand the earnings-dates row: the detail prints the newest five dates, then the count) and `ICT PM` (the enterprise-value row prints `USD 33.11B` and `USD 33.09B` beside PRICE `PHP 860.00`).
- Harness: `node src/pages/SecurityAnalysis/__harness__/changedListValue.harness.cjs` (YES, 16 of 16 checks at `bc0a5cd9`).
