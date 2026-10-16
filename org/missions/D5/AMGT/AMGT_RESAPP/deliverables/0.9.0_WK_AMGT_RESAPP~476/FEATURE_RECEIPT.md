# FEATURE RECEIPT -- AMGT_RESAPP bo-1 (round 108): Security Analysis, team mark and withheld reasons

## What the branch carries

- Branch: `cand/dell1/amgt-sa-withheld-reasons` (nested portal repository, local only; never pushed)
- Head commit: `01e06415f17f5e2ea79b28548647142879cce340` (LOCAL)
- Base: `e0e69da7` (PROD, merge of `cand/dell1/amgt-sa-team-estimate-mark` into `release/20261015T223053Z`)
- Changed paths (`git diff --name-only e0e69da7 HEAD`), all under `src/pages/SecurityAnalysis/`:
  - `src/pages/SecurityAnalysis/tabs/ModelTab.tsx` -- team mark on every team P/E cell; withheld reason line under Key Figures when no P/E row; `vendorPeWithheld` removed; `withheldPeReason` imported from the new helper
  - `src/pages/SecurityAnalysis/components/model/WhatChangedPanel.tsx` -- a withheld forward BEST_PE_RATIO is not listed; the Changed tile reads the rows listed; one reason line when every changed row is dropped
  - `src/pages/SecurityAnalysis/components/model/withheldPeReason.ts` -- NEW; the helper moved out of ModelTab so the table and the panel share it
  - `src/pages/SecurityAnalysis/__harness__/withheldReasons.harness.cjs` -- NEW; 18 checks
  - `src/pages/SecurityAnalysis/__harness__/teamEstimateMark.harness.cjs` -- T5 flipped to expect the mark (the only change in this file)
  - `src/pages/SecurityAnalysis/__harness__/withheldFixture.ZURN_SW_Equity.json` -- NEW; copied byte for byte from round108_prep
  - `src/pages/SecurityAnalysis/__harness__/withheldFixture.939_HK_Equity.json` -- NEW; copied byte for byte from round108_prep
  - `src/pages/SecurityAnalysis/__harness__/withheldFixture.ICT_PM_Equity.json` -- NEW; copied byte for byte from round108_prep
  - `src/pages/SecurityAnalysis/__harness__/withheldFixture.1299_HK_Equity.json` -- NEW; copied byte for byte from round108_prep
  - `src/pages/SecurityAnalysis/__harness__/withheldFixture.ZURN_SW_compare.json` -- NEW; copied byte for byte from round108_prep

## Pages changed

| page | route | class | gate |
|---|---|---|---|
| Security Analysis | /security-analysis | Opal-internal | internal |

## Shared files

- none

## Not carried

Each path is absent from the branch; the count is `git diff e0e69da7 HEAD -- <path> | wc -l`.

- `package.json` -- 0
- `bun.lock` -- 0
- `src/lib/firmAccess.ts` -- 0
- `src/App.tsx` -- 0

## How to look

- Dev build (port 5174 only): `cd portal && bun run dev:live --port 5174`
- Page: `/security-analysis`, Model tab
- Names: `ZURN SW`, `939 HK`, `ICT PM`, `1299 HK` (no P/E row; the reason line under Key Figures; no withheld ratio in What Changed), `SHOP CN` (team text range and team estimates marked), `PBR US` (2025 range `3.6x-5x` and the 2026E and 2027E team estimates marked)
