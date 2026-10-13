# FEATURE_RECEIPT -- Security Analysis feature branch (AMGT_RESAPP bj-9, round 103)

Issued to 0.9.0_WK_AMGT_RESAPP~410 by 2.0.0_SA_COO~R1. Approval and promote are NOT part of this receipt.

## What the branch carries

- Branch: `feature/amgt-security-analysis-v1` in the nested portal repository, commit `e80be8ce0272c85bc291ba4688f49bfc430e5a12` (LOCAL, not pushed).
- Base: `15c9754975` (portal PROD).
- DEV source: `origin/DEV` at `4d601023` (fetched this run). The order was cut against `c1d36723`; DEV has moved since.
- Page files: 17 (all under `src/pages/SecurityAnalysis/`, 1 added and 16 modified, taken whole with `git checkout origin/DEV -- src/pages/SecurityAnalysis`; no hand edit).
- Shared files: 0.

## Pages changed

| page | route | class | gate |
|---|---|---|---|
| Security Analysis | /security-analysis | Opal-internal | internal |

The route and its gate already exist on PROD (`src/App.tsx`: `<ProtectedRoute requireInternal>` at the two `/security-analysis` routes), so no route file is changed. No other page is changed.

## Shared files

- none (0 shared files: typecheck rc 0 with no error naming a file outside `src/pages/SecurityAnalysis/`).

## Not carried

Each path below is absent from the branch: `git diff 15c9754975 e80be8ce0272c85bc291ba4688f49bfc430e5a12 -- <path> | wc -l` is 0 for every row. The PROD-to-DEV delta is given so the exclusion can be read against a real change.

| not carried | path | branch diff lines (base..HEAD) | PROD..origin/DEV diff lines |
|---|---|---|---|
| AdvisorBookFeePanel | `src/pages/AdvisorIntelligence/_shared/AdvisorBookFeePanel.tsx` | 0 | 325 |
| AdvisorBookFeePanel test | `src/pages/AdvisorIntelligence/_shared/AdvisorBookFeePanel.test.tsx` | 0 | 91 (absent on PROD, added on DEV) |
| /portfolios change | `src/pages/ModelPortfolios.tsx` | 0 | 105 |
| dependency manifest | `package.json` | 0 | 21 |
| lockfile | `bun.lock` | 0 | 82 |
| partner pages list | `src/lib/firmAccess.ts` | 0 | 0 (DEV has not changed it since PROD; excluded by the order's rule regardless) |
