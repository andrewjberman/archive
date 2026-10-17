# FEATURE RECEIPT -- AMGT-bu-1 (round 114, 0.9.0_WK_AMGT_RESAPP~504)

## What the branch carries

- Branch: `cand/dell1/amgt-sa-peers-subject-currency` (nested portal repository; never pushed)
- Head commit: `a3f2b7277bdb24e29cb4723de502fc0862e281f1` (LOCAL, on that branch)
- Base: `d1bed0fb` (PROD)
- Paths changed since `d1bed0fb`:
  - `src/pages/SecurityAnalysis/priceCurrency.ts`
  - `src/pages/SecurityAnalysis/tabs/PeersTab.tsx`
  - `src/pages/SecurityAnalysis/__harness__/priceCurrencyRule.harness.cjs`

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
- Page: `/security-analysis`, ICT PM, Peers tab. The subject row's Price, Mkt Cap and EV cells print the same text as before (for example `PHP 860.00`, `PHP 1.74T`, `USD 33.09B` on the synthetic padded-code overlay); on live names no visible change is expected, since no live name carries a padded code.
