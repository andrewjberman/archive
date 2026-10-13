# NONE_REASON_LIST -- round 84, cell CB-cf-1, worker 0.9.0_WK_ADVI_COTBKF~167

Written and committed BEFORE any classification read. It is the closed list for the `reason` of each `none` row.

## Population and columns

- File: `org/missions/D8/ADVI/ADVI_COTBKF/deliverables/2.0.0_SA_COO~C2/REVERSE_MATCH.csv` (header `account_key,predecessor_key,match_basis,reason`, 769 rows, sha256 20fb38333542b23beab5a61316cf9acdc0119dbf0be85b55fe150ec191c09a64).
- Population to classify: the rows whose `predecessor_key` is `none` AND whose `reason` is `none`. That is 273 rows. CORRECTION (before any classification read; surprise row ADVI_COTBKF-D2-W167-S1): a `reason` = `none` filter alone matches 730 rows, 457 of them `crosswalk_matched` rows that stay untouched. The 300 `predecessor_key` = `none` rows hold 273 with reason `none` and 27 with reason `AMBIGUOUS` (the 27 stay unchanged).
- Keys reused as they stand: `account_key`, `predecessor_key`, `match_basis`, `reason`. No re-derivation of the 769.
- Commonwealth-side keys are the salted tokens the record uses. A candidate Commonwealth account (test 3) is counted in that same token space. If the salt is unavailable to this worker, the candidate counts are recorded `not_established`.

## Migration date

M = 2026-06-23. Reason: the Commonwealth transactions table has its last Trade_Date on 2026-06-22 (ACTIVE_SET_RECORD.json, sources). 2026-06-23 is the first date after the last Commonwealth record, and it is the partition the record reads (`date=2026-06-23/`). The Black Diamond starts (gold canonical 2026-04-22, silver holdings 2026-06-08) are record starts, not the migration date.

## Tests, in order (the FIRST test passed assigns the code; an account that passes none is OTHER)

1. `NO_COMMONWEALTH_HOUSEHOLD`
   - Test: a household join exists in the data read (a column of `silver/crosswalk/date=2026-06-23/crosswalk.csv` or `silver/account_links/date=2026-06-23/account_links.csv` holding a household identifier shared by two or more Commonwealth accounts), AND no Commonwealth account carrying the account's household identifier has any row in `silver/transactions/date=2026-06-23/`.
   - If neither file carries a household column, the test cannot be passed. The code is then assigned to no row, and the record states that no household join exists.
2. `NEW_CLIENT_AFTER_MIGRATION`
   - Test: the earliest partition date in which the Black Diamond `account_id` appears in `gold/canonical/holdings` (dated 2026-04-22 onward) or `silver/holdings` (dated 2026-06-08 onward) is on or after M = 2026-06-23.
3. `MISMATCH_NO_IDENTIFIER`
   - Test: a candidate Commonwealth account exists, AND no row of crosswalk.csv or account_links.csv joins that candidate to this account.
   - Candidate: a Commonwealth account with at least one transaction row dated before M whose Cusip is also held by the account in the `silver/holdings` snapshot dated 2026-10-12.
   - Identifiers that would settle it: holder name, tax identifier, account title. These are counted absent if no column of the files read carries them. The header read records which are absent.
4. `OTHER`, with a sub-code of at most 3 words from this closed list only:
   - `NO_CANDIDATE_OVERLAP`: no candidate exists under test 3. The account has no shared holding with any pre-migration Commonwealth account.
   - `LINKED_NOT_RECORDED`: a candidate exists and a crosswalk or account_links row joins it to the account, yet the reverse match left `predecessor_key` = `none`. This is an anomaly, recorded and not repaired.

## Rules

- No code is invented beyond this list. A row that fits no test and no sub-code above is a surprise row, not a new code.
- Rows outside the 273 (including the 27 `AMBIGUOUS` rows and every matched or near row) are not touched.
- No account key, number or value appears in this list or in any record derived from it.
