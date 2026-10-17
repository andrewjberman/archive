# FEATURE RECEIPT -- AMGT_RESAPP bu-2 (round 114), 0.9.0_WK_AMGT_RESAPP~505

## What the branch carries

- Branch: `cand/dell1/amgt-sa-page-dates-long-form` (nested portal repository, LOCAL, not pushed)
- Head commit: `9a8ef5e451` (AMGT_RESAPP bu-2: every date the Security Analysis page prints from a served ISO day passes through the house long-date helper)
- Base: PROD `d1bed0fb`
- Paths changed since `d1bed0fb` (`git diff --name-only d1bed0fb HEAD`):
  - `src/pages/SecurityAnalysis/__harness__/dateRule.harness.cjs`
  - `src/pages/SecurityAnalysis/__harness__/dateRuleFixture.ICT_PM_compare_scalar_date.json`
  - `src/pages/SecurityAnalysis/__harness__/dateRuleFixture.base_rio_visible.json`
  - `src/pages/SecurityAnalysis/__harness__/dateSites.fixture.json`
  - `src/pages/SecurityAnalysis/components/AiFillBlock.tsx`
  - `src/pages/SecurityAnalysis/components/ChatterBubbles.tsx`
  - `src/pages/SecurityAnalysis/components/CheckFaceBadge.tsx`
  - `src/pages/SecurityAnalysis/components/DossierSections.tsx`
  - `src/pages/SecurityAnalysis/components/HeaderBrief.tsx`
  - `src/pages/SecurityAnalysis/components/HeaderCards.tsx`
  - `src/pages/SecurityAnalysis/components/InputProvenance.tsx`
  - `src/pages/SecurityAnalysis/components/PriceBars.tsx`
  - `src/pages/SecurityAnalysis/components/RankedChart.tsx`
  - `src/pages/SecurityAnalysis/components/RankedList.tsx`
  - `src/pages/SecurityAnalysis/components/SegmentBreakdown.tsx`
  - `src/pages/SecurityAnalysis/components/SegmentTable.tsx`
  - `src/pages/SecurityAnalysis/components/TimelinePanel.tsx`
  - `src/pages/SecurityAnalysis/components/TimelineWordCloud.tsx`
  - `src/pages/SecurityAnalysis/components/model/WhatChangedPanel.tsx`
  - `src/pages/SecurityAnalysis/tabs/ExecManagementTab.tsx`
  - `src/pages/SecurityAnalysis/tabs/PostureTab.tsx`

## Pages changed

| page | route | class | gate |
|---|---|---|---|
| Security Analysis | /security-analysis | Opal-internal | internal |

## Shared files

- none

## Not carried

- `package.json`: absent; `git diff d1bed0fb HEAD -- package.json | wc -l` = 0
- `bun.lock`: absent; `git diff d1bed0fb HEAD -- bun.lock | wc -l` = 0
- `src/lib/firmAccess.ts`: absent; `git diff d1bed0fb HEAD -- src/lib/firmAccess.ts | wc -l` = 0
- `src/App.tsx`: absent; `git diff d1bed0fb HEAD -- src/App.tsx | wc -l` = 0

## How to look

- Dev build: `cd portal && bun run dev:live --port 5174`
- Page: `/security-analysis`, names: ICT PM (Model tab, What Changed, older version pairs, the "Date of the issuer's next expected earnings report" row, which reads "November 6th, 2026" and "November 11th, 2026" where PROD read "2026-11-06" and "2026-11-11"); RIO LN as the control (unchanged).
- Harness: `cd portal && node src/pages/SecurityAnalysis/__harness__/dateRule.harness.cjs` (DATE RULE HARNESS: YES 7 of 7 checks).
