# FEATURE RECEIPT -- AMGT-bs-2 (0.9.0_WK_AMGT_RESAPP~497)

## What the branch carries

- branch: `cand/dell1/amgt-sa-price-currency-rule` (LOCAL; nothing pushed)
- head: `937f15a01d123fe711bc5db175590a1c878185ca` (LOCAL)
- base: `932cea99e8cabffa7ca28d2d57aba1e923d4e591` (PROD)
- every path changed since `932cea99` (`git diff --name-only 932cea99 HEAD`):
  - `src/pages/SecurityAnalysis/__harness__/peersCurrency.harness.cjs`
  - `src/pages/SecurityAnalysis/__harness__/priceCurrencyFixture.base_table_PHP.html`
  - `src/pages/SecurityAnalysis/__harness__/priceCurrencyRule.harness.cjs`
  - `src/pages/SecurityAnalysis/components/HeaderCards.tsx`
  - `src/pages/SecurityAnalysis/priceCurrency.ts`
  - `src/pages/SecurityAnalysis/tabs/PeersTab.tsx`

## Pages changed

| page | route | class | gate |
|---|---|---|---|
| Security Analysis | /security-analysis | Opal-internal | internal |

## Shared files

- none

## Not carried

- `package.json` -- absent; `git diff 932cea99 HEAD -- package.json | wc -l` = 0
- `bun.lock` -- absent; `git diff 932cea99 HEAD -- bun.lock | wc -l` = 0
- `src/lib/firmAccess.ts` -- absent; `git diff 932cea99 HEAD -- src/lib/firmAccess.ts | wc -l` = 0
- `src/App.tsx` -- absent; `git diff 932cea99 HEAD -- src/App.tsx | wc -l` = 0

## How to look

- Dev build: `cd portal && bun run dev:live --port 5174` (port 5174 only).
- Page: `/security-analysis`.
- ICT PM (PHP-priced name): the header key-figure tiles (Price reads `PHP 860.00`; Enterprise value reads `USD` then the figure) and the Peers tab (every USD money cell reads `USD `, never `$`).
- GOOGL US (USD-priced control): the Peers tab keeps `$`; the SPCX member Price cell reads `148.07 currency not stated` (unchanged).
- Offline check: `node src/pages/SecurityAnalysis/__harness__/priceCurrencyRule.harness.cjs` (R1 to R6).
