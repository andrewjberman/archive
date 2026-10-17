# FEATURE RECEIPT -- AMGT-br-3 (0.9.0_WK_AMGT_RESAPP~494)

The P/E not shown footer names the missing figure in plain words, never a vendor mnemonic.

## What the branch carries

- Branch: `cand/dell1/amgt-sa-pe-footer-words` (portal repo, nested worktree `C:/dev/wk-resapp-494/portal`)
- New head commit: `3eb64c263ade1093c0d18b5b4df241e655ac68da` (LOCAL, not pushed)
- Base: `99d2b2a7` (PROD)
- Every path changed since `99d2b2a7`:
  - `src/pages/SecurityAnalysis/__harness__/peFooterWords.harness.cjs`
  - `src/pages/SecurityAnalysis/tabs/ModelTab.tsx`

## Pages changed

| page | route | class | gate |
| --- | --- | --- | --- |
| Security Analysis | /security-analysis | Opal-internal | internal |

## Shared files

- none

## Not carried

- `package.json` -- absent; `git diff 99d2b2a7 HEAD -- package.json | wc -l` = 0
- `bun.lock` -- absent; `git diff 99d2b2a7 HEAD -- bun.lock | wc -l` = 0
- `src/lib/firmAccess.ts` -- absent; `git diff 99d2b2a7 HEAD -- src/lib/firmAccess.ts | wc -l` = 0
- `src/App.tsx` -- absent; `git diff 99d2b2a7 HEAD -- src/App.tsx | wc -l` = 0

## How to look

- `cd portal && bun run dev:live --port 5174`
- Open `/security-analysis`, the names RIO LN and ICT PM, the Model tab, and the Key Figures footer `P/E not shown: ...` (shown when the table has no P/E row).
- Before the change the footer read `price / reported EPS (IS_EPS), FY2025, ...`; after it reads `price / reported earnings per share, FY2025, ...`.
- The harness `src/pages/SecurityAnalysis/__harness__/peFooterWords.harness.cjs` renders the five served variants (GBp/USD, absent input, EPS not positive, price not positive, currency not stated) and proves each prints no mnemonic.

## Mnemonic census

Question: every source of a string the footer can print, and every vendor-mnemonic-shaped token each can contain. Read at the worktree, `99d2b2a7` plus the branch's own commit for the portal side.

Sources that build a reason and can reach the footer (lib, `lib/research/api/scoped_amgt.py`):

| # | file:line | string | mnemonic tokens |
| --- | --- | --- | --- |
| 1 | lib/research/api/scoped_amgt.py:2754 | `an input is absent (PX_LAST or IS_EPS)` | PX_LAST, IS_EPS |
| 2 | lib/research/api/scoped_amgt.py:2756 | `reported EPS (IS_EPS) is not positive` | IS_EPS |
| 3 | lib/research/api/scoped_amgt.py:2758 | `the fiscal-year price (PX_LAST) is not positive` | PX_LAST |
| 4 | lib/research/api/scoped_amgt.py:2760 | `the currency of the price or of reported EPS is not stated` | none |
| 5 | lib/research/api/scoped_amgt.py:2762 | `the price is in {ccy} and reported EPS in {ccy}, and a ratio of different currencies is not shown` | none |
| 6 | lib/research/api/scoped_amgt.py:2764 | wrapper `price / reported EPS (IS_EPS), FY{year}, is not shown: {why}` (historical, `fiscal_unresolved`) | IS_EPS |
| 7 | lib/research/api/scoped_amgt.py:2806 | estimate year `the price is in {ccy} and consensus EPS in {ccy}, ...` (`forecast_withheld`, wired at :5760 and :5816) | none |
| 8 | lib/research/api/scoped_amgt.py:5803-5807 | `fiscal_unresolved` passthrough of the stored model-block `unresolved` rows (scope fiscal_year_line_item) plus `pe_withheld`; the stored text is produced outside this worktree (see the gap below) | not measured at source |

Portal readers on the footer path (`portal/src/pages/SecurityAnalysis/`):

| # | file:line | role |
| --- | --- | --- |
| 9 | tabs/ModelTab.tsx:197-199 | `fiscalPeReason` reads the `fiscal_unresolved` PE_RATIO reason (historical source) |
| 10 | components/model/withheldPeReason.ts:6-12 | reads the `forecast_withheld` BEST_PE_RATIO reason (estimate source) |
| 11 | tabs/ModelTab.tsx:617-618 | footer call site; each reason now passes through `plainPeReason` before it is printed |

Read, not on the footer path:

- lib/research/api/scoped_amgt.py:2742 -- `price / reported EPS (IS_EPS), FY{year}` is `basis.definition` on served rows, never a reason.
- lib/research/api/scoped_amgt.py:1164-1187 -- `_plain_no_block_reasons` acts only on a covered name with no model block, which carries no `fiscal_unresolved`.
- tabs/ModelTab.tsx:652 and :672 -- the P/E row's forecast dash prints `withheldPeReason` raw. Its reason is site 7 (no token). Not wrapped: the cell scopes the change to the footer.
- tabs/ModelTab.tsx:684-686 -- the literal `P/E not shown: ` and the `; ` join carry no token.

Denominator: 8 lib sites (sites 1-8) and 3 portal sites (9-11) read on the footer path; 3 non-footer sites read.

Token set found in every string that can reach the footer: `IS_EPS`, `PX_LAST`. The table names both (`reported earnings per share`, `share price`). No token was found that the table does not name, so no table row was added.

Gap, reported and not closed: the producer of the stored `unresolved` rows (site 8) is named by `lib/research/checkface/scopes.py` as `integrations/bloomberg/research/model_block_pull.py` lines 392-426. That path is absent from this worktree (`Glob` returned no file). The stored model blocks that are present, `lib/research/posture/data/model_block/*.json`, carry no reason value with an underscore token (0 hits). The producer's own text is unmeasured.
