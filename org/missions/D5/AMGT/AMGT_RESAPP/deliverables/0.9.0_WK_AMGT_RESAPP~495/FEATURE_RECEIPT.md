# FEATURE RECEIPT -- AMGT-br-4 (0.9.0_WK_AMGT_RESAPP~495)

## What the branch carries

- Branch: `cand/dell1/amgt-sa-peers-currency` (portal repository, cut from PROD `99d2b2a7`; never pushed).
- Head commit: `259da4c4aafd36f14b9939dbbcd86140cc2c6efe` (LOCAL; subject `AMGT-br-4: the Peers tab prints every money cell in the page name's price currency`).
- Base: `99d2b2a7` (PROD).
- Every path changed since `99d2b2a7` (`git diff --name-only 99d2b2a7 HEAD`):
  - `src/pages/SecurityAnalysis/tabs/PeersTab.tsx`
  - `src/pages/SecurityAnalysis/__harness__/peersCurrency.harness.cjs`
  - `src/pages/SecurityAnalysis/__harness__/peersCurrencyFixture.ICT_PM_peers.json`
  - `src/pages/SecurityAnalysis/__harness__/peersCurrencyFixture.ICT_PM_overlay.json`
  - `src/pages/SecurityAnalysis/__harness__/peersCurrencyFixture.GOOGL_US_peers.json`
  - `src/pages/SecurityAnalysis/__harness__/peersCurrencyFixture.GOOGL_US_overlay.json`
  - `src/pages/SecurityAnalysis/__harness__/peersCurrencyFixture.base_ratio.txt`

## Pages changed

| page | route | class | gate |
|------|-------|-------|------|
| Security Analysis | /security-analysis | Opal-internal | internal |

## Shared files

- none

## Not carried

| path | `git diff 99d2b2a7 HEAD -- <path> \| wc -l` |
|------|------|
| package.json | 0 |
| bun.lock | 0 |
| src/lib/firmAccess.ts | 0 |
| src/App.tsx | 0 |

## How to look

- Dev build: `cd portal && bun run dev:live --port 5174`.
- Page: `/security-analysis`, then the Peers tab.
- Names: ICT PM (PHP-priced; a USD figure reads `USD `, the subject row, the member row and the summary rows alike). GOOGL US is the USD-priced control (cells keep `$`).
