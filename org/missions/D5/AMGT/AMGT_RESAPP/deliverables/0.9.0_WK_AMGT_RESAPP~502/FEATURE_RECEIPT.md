# FEATURE RECEIPT -- AMGT-bt-3 (round 113): the shared price-currency helper trims a padded served currency code

## What the branch carries

- Branch: `cand/dell1/amgt-sa-price-currency-trim` (nested portal worktree `C:/dev/wk-resapp-502/portal`), LOCAL, not pushed.
- New head commit: `4f8299bdddcb85be245b8c1e6bfca31be5be8a2e` (subject: AMGT-bt-3 (round 113): the shared price-currency helper trims a padded served currency code).
- Base: PROD `856fb37b`.
- Every path changed since `856fb37b`:
  - `portal/src/pages/SecurityAnalysis/priceCurrency.ts`
  - `portal/src/pages/SecurityAnalysis/__harness__/priceCurrencyRule.harness.cjs`

## Pages changed

| page | route | class | gate |
|---|---|---|---|
| Security Analysis | /security-analysis | Opal-internal | internal |

## Shared files

- none

## Not carried

- `package.json`: absent; `git diff 856fb37b HEAD -- package.json | wc -l` = 0
- `bun.lock`: absent; `git diff 856fb37b HEAD -- bun.lock | wc -l` = 0
- `src/lib/firmAccess.ts`: absent; `git diff 856fb37b HEAD -- src/lib/firmAccess.ts | wc -l` = 0
- `src/App.tsx`: absent; `git diff 856fb37b HEAD -- src/App.tsx | wc -l` = 0

## How to look

- Dev build: `cd portal && bun run dev:live --port 5174`, then open `/security-analysis`.
- Names: ICT PM (PHP-priced; the header tiles and the Peers table print as before, with no visible change on live names) and GOOGL US (USD-priced; the Peers table keeps `$`).
- The padded-code case (PX_LAST currency ` PHP `) has no live name; it is exercised only by the harness R7 (`node src/pages/SecurityAnalysis/__harness__/priceCurrencyRule.harness.cjs`).
