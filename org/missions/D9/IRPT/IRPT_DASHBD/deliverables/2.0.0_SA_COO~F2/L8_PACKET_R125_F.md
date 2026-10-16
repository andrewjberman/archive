# IRPT_DASHBD round 125, workstream F-SHIP (~F2) -- the drain-end packet (FWD-5: the transactions table view model)

Issuer `2.0.0_SA_COO~F2`, 2026-10-16 ~06:0xZ. For `3.0.0_SA_CVO~IRPT`. Issuance `354d864d1a`. Decomposition
`org/missions/D9/IRPT/IRPT_DASHBD/decompositions/IRPT_DASHBD_DECOMP_R125_F.md`. fanout: 1 of 1 chains, cap 8.
Cut by the empty-tick sequence (`/next-calls IRPT_DASHBD --drive`) as FREE work around the FWD-5 block: the table's logic does not depend on the ratified words or on the contract's last details. Serves the PRD's FWD-5 and its workstream F item 3 ("The transactions table: sort, type filter, symbol search, export, virtualised").

**No judgment criterion** (one LOCAL cell, two mechanical criteria). `round-close-check.py --project IRPT_DASHBD --round 125`: `verdict=MAY-CLOSE` (6 orders, 0 judgment).

## The cell

| cell | worker | criteria | merged |
|---|---|---|---|
| `DB-f-1101` the transactions table view model | `0.9.0_WK_IRPT_DASHBD~1101` | DBF125-1-AC1 PASS (23 tests, 12 required, 8 of 8 title words), DBF125-1-AC2 PASS (the portal diff is exactly the two new files); re-run by the issuer on the worker tree | `85d5f4516c` |

The code is on the portal branch `wk-IRPT_DASHBD-1101-portal` (head `ee30038f8456b088fb2a653557b6ee606de0039d`, two commits over `origin/PROD` `a062c56e`: `tabs/reporting/transactions/transactionsView.ts`, 220 lines, and `__tests__/irpt-dashbd/transactions-view.test.ts`). Its candidate ref `cand/dell2/irpt-transactions-view` is LOCAL, not pushed, not registered.

## What it does (read by this seat, and by the worker's run)

1. **`TransactionRow`** holds the brief's 14 columns; `settle_date`, `asset_name`, `fee` and `source_txn_id` (and `symbol`, `units`, `price` for a cash line) are `null`, never zero. `TRANSACTION_COLUMNS` fixes the column order and a client-safe header each.
2. **`filterByType`, `searchBySymbol`, `sortRows`, `distinctTypes`, `exportCsv`, `visibleWindow`, `viewRows`.** The sort is stable with nulls last in both directions; the search matches the symbol and any word of the asset name by prefix; the type filter's choices are the distinct `txn_type` values in the rows (the source file names no Opal word); `viewRows` applies filter, search, sort in that order and never mutates its input.
3. **The export** quotes a comma, a quote or a line break, prints a null as an empty field, and guards a TEXT field that starts with `=`, `+`, `-` or `@` with a leading single quote (a number is never prefixed), so an opened file cannot run a formula from a symbol or a name.
4. **The window** is clamped to `[0, total]` with overscan; a total of zero or a bad row height gives `{0, 0}`.
5. **Gates:** typecheck rc=0; lint rc=1 with one error in `filing-hint.test.tsx` (outside this cell, pre-existing: row W1101-S3), 0 findings in the two new files; the InvestorReporting suite 69 failing before and after with 0 new failing names; the mutant (nulls first in descending order) fails 2 tests. No holdings helper was reused (the sort idiom lives inside React components); the idea was copied.

## Rows (all OBSERVATION, INERT)

W1101-S1 (the worktree is sparse, the row schema read at HEAD), S2 (the holdings sort is inside components), S3 (the lint error above).

## The one real run

None possible: nothing is mounted and no transactions file is served. **Thread live: n** for FWD-5.

## Open, with owners

- **Ratified (CTO round-124 analysis):** the FWD-5 words at `tran_srcde` grain. The view model's type filter will list the ratified words; `UNMAPPED` lines show as "Other" with their count (a display rule for the table component, which waits on the contract's shape).
- **Round 127** (cut next): the transaction contract with the ratified mapping and per-code flow class, then the 49 Financial producer (S103).
- **Round 126** (cut, worker `~1201` running): the ground read for Cottonwood and Inflection.
- **FWD-3 mount:** waits on `~D2`'s `class_object` 0.4.0 and `~S2`'s route member.

-- 2.0.0_SA_COO~F2
