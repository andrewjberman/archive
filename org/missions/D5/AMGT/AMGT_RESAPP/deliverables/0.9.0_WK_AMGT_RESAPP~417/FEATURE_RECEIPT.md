# FEATURE RECEIPT -- cand/dell1/amgt-sa-header-money-and-dash-reasons

Round 104, decomposition cell AMGT-bk-6. Feature of AMGT-bk-3: the Security Analysis header prints USD as `$`, and every dash tile shows its reason in visible words. Approved as Opal-internal by CTO msg 5281.

## What the branch carries

- Branch: `cand/dell1/amgt-sa-header-money-and-dash-reasons` (portal repository, LOCAL; not pushed).
- Head commit: `624e2533f665bf786e41594adba17b82c447aa7d` (author `0.9.0_WK_AMGT_RESAPP~417`), subject `AMGT-bk-3 (round 104), feature cand/dell1/amgt-sa-header-money-and-dash-reasons: ...`.
- Base: PROD `10e7664d6c4824cb88f04acf47f06264345b5b8b` (the last PROD release, cut from that commit; the branch carries only its own commit).
- Paths (4, each taken byte-for-byte from the approved candidate `3dcbb6ef`):
  - `src/pages/SecurityAnalysis/components/HeaderCards.tsx`
  - `src/pages/SecurityAnalysis/components/StatTile.tsx`
  - `src/pages/SecurityAnalysis/components/model/WhatChangedPanel.tsx`
  - `src/pages/SecurityAnalysis/__harness__/tileMoneyAndReasons.harness.cjs` (new file)

## Pages changed

| page | route | class | gate |
|---|---|---|---|
| Security Analysis | /security-analysis | Opal-internal | internal |

## Shared files

- none

## Not carried

Each path below is stated absent from the branch: `git diff 10e7664d HEAD -- <path> | wc -l` reads 0.

- AdvisorBookFeePanel: `src/pages/AdvisorIntelligence/_shared/AdvisorBookFeePanel.tsx` -- count 0 (absent). The `.test.tsx` beside it is also absent.
- The /portfolios change: the route is `src/App.tsx` (`path="/portfolios"`, line 453 at PROD) and its page is `src/pages/ModelPortfolios.tsx` -- `src/App.tsx` count 0, `src/pages/ModelPortfolios.tsx` count 0 (both absent).
- `package.json` -- count 0 (absent).
- `bun.lock` -- count 0 (absent).
- `src/lib/firmAccess.ts` -- count 0 (absent).

## How to look

From the nested portal worktree on the branch:

```
cd portal && bun run dev:live --port 5174
```

Open `/security-analysis` (internal login). Check the header money cells print `$` for USD, and the dash tiles show their reason in words. Names to check: `TSM US`, `HSBA LN`.
