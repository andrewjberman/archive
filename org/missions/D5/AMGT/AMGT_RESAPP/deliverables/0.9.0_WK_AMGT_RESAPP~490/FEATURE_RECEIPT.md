# FEATURE RECEIPT -- AMGT-bp-4 (round 109): money display

## What the branch carries

- Branch: `cand/dell1/amgt-sa-money-display` (nested portal worktree `C:/dev/wk-resapp-490/portal`), cut from PROD `15bc21b3`.
- Head commit: `aba098da` (full `aba098daee5c42c9f0fdb65bfaf4366ce8ca39d7`), LOCAL only, not pushed. Earlier commit on the branch: `94c30e22` (harness, fixtures and base files recorded from the unedited page).
- Base: `15bc21b3`.
- Changed paths (`git diff --name-only 15bc21b3 HEAD`, 7 files):
  - `src/pages/SecurityAnalysis/__harness__/moneyDisplay.harness.cjs`
  - `src/pages/SecurityAnalysis/__harness__/moneyFixture.GOOGL_US.json`
  - `src/pages/SecurityAnalysis/__harness__/moneyFixture.ICT_PM.json`
  - `src/pages/SecurityAnalysis/__harness__/moneyFixture.base_outputs.json`
  - `src/pages/SecurityAnalysis/__harness__/moneyFixture.base_tiles.json`
  - `src/pages/SecurityAnalysis/components/HeaderCards.tsx`
  - `src/pages/SecurityAnalysis/components/StatTile.tsx`

What the feature does (display only; no served value, figure or existing sentence changes):

1. A minus sign leads the whole money figure: `-$63.90B`, `-EUR 63.90B`, `-PHP 63.90B`, `-$12.50` (was `$-63.90B` and so on). Positive and non-money formats print as before.
2. A USD figure prints `USD ` and the amount when the name's price currency is not USD (ICT PM: `USD 33.11B` beside `PHP 860.00`). `$` is kept where the price currency is USD or none is served.

## Pages changed

| page | route | class | gate |
|---|---|---|---|
| Security Analysis | /security-analysis | Opal-internal | internal |

No other page is changed.

## Shared files

- none

## Not carried

Each path is absent from the branch; the count is `git diff 15bc21b3 HEAD -- <path> | wc -l`, measured at `aba098da`.

- `package.json`: 0
- `bun.lock`: 0
- `src/lib/firmAccess.ts`: 0
- `src/App.tsx`: 0

## How to look

- Dev build: `cd portal && bun run dev:live --port 5174` (on the candidate branch).
- Page: `/security-analysis`, names `ICT PM` and `GOOGL US`.
- Header tiles: GOOGL US NET DEBT reads `-$63.90B`; ICT PM ENTERPRISE VALUE reads `USD 33.11B` beside PRICE `PHP 860.00`; GOOGL US MARKET CAP and ENTERPRISE VALUE still read `$`.
- Harness: `node src/pages/SecurityAnalysis/__harness__/moneyDisplay.harness.cjs` (YES, 24 of 24 checks at `aba098da`).
