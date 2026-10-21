# FIDUPL depth experiments: transactions, realized gain/loss, other Historical formats (measured 2026-10-21)

Author 2.0.0_SA_COO~P1, 2026-10-21 ~15:30Z, on Andrew-direct "keep experimenting" (CRO msg 9106, CTO msg 9111). Dates, counts and statuses only; accounts appear as sha8 of the number, no value, name or file content. One agent sign-in 15:19Z (SIGNED_IN), logout 15:27Z (`204,400`); read calls only except the five Historical create requests of part C.

## 1. Transactions: `historical-transactions` (CRO params; read-only)

- **Date format is ISO `YYYY-MM-DD`** (`MM/dd/yyyy` answers 400 with an empty error list). Body as the CRO gave: `accounts[{accountNumber, accountSource "BROK", lineOfBusiness "IWS"}]`, `timePeriodOption "custom"`, `customTimePeriodFromDate`, `customTimePeriodToDate`, `dateField "T"`, `searchBy "none"`, `cmType`, `currencyCode`, `securityId`, `transactionType` empty, `excludeCoreBrokerage false`. Answer: `{asOfTimestamp, transactions[]}`; a row carries `accountNumber`, `clientName`, `cusip`, `commissionAmount` and the other fields the endpoint map lists.
- **One call spans at most 366 days.** Any longer window is REFUSED with 400 `TXH-400` and the exact text "end date must be 366 days or less from start date, path = customTimePeriodToDate". That is a window limit, not a look-back limit: consecutive one-year windows work.
- **Floor, three accounts with activity in the last year, windows of 365 days stepped back from today:**

| window | acct 0651ed47 | acct 513ade39 | acct dc276ec7 |
|---|---|---|---|
| 2025-10-21 to 2026-10-21 | 167 | 85 | 336 |
| 2024-10-21 to 2025-10-21 | 249 | 71 | 352 |
| 2023-10-22 to 2024-10-21 | 241 | 73 | 283 |
| 2022-10-22 to 2023-10-22 | 256 | 54 | 139 |
| 2021-10-22 to 2022-10-22 | 300 | 37 | 68 |
| 2020-10-22 to 2021-10-22 | **0 (EMPTY)** | **0 (EMPTY)** | **0 (EMPTY)** |

  The earliest transaction in the 2021-10-22 window is **2021-12-08 to 2021-12-10 on all three**, and the window before is empty on all three. The floor is therefore about **2021-12 (about 4 years 10 months back)**; the same early-December date on three unrelated accounts reads as a platform start date for this login, not a rolling 5-year cap (unproven which). No response was paged or truncated at these sizes.

## 2. Realized gain/loss: `previous-sales/retrieve-realized-gain-loss/detail`

A start date 30 years back is ACCEPTED (200, no refusal). Six sampled accounts returned lots whose earliest `lotClosedDate` is 2018-07-24 (one account), 2020-11-16, 2021-10-01, 2022-06-13 (two) and 2023-03-21, and whose earliest acquisition date (`acquisitionDateFormatted`) is 2013-01-22. So realized lots and cost basis reach **back to 2018 by close date and 2013 by acquisition date** on this sample, much deeper than transactions. One account answered 500 lots of `totalCount` 915: the call pages at 500 (`offset`), so a full pull must page.

## 3. Historical export with other formats (part C of the walk question)

Standard A `PBL` (`indicatorName AN`) for 2026-06-12, 2026-05-22 and 2025-10-21, and Standard B `POS`+`PRC` (`indicatorName CN`) for 2026-06-12 and 2026-05-22: every create call was accepted (`S`) and every file finished COMPLETED WITH ERRORS with the 125-byte does-not-exist stub. **No other format or indicator reaches past the Custom floor** (positions 2026-06-15, prices 2026-06-18 on 2026-10-21). Balances (PBL) at 2026-06-12 or earlier are not served either; the walk measures its own PBL floor.

## 4. Not probed, and why

- Statements (`getDocumentsSearchResult`): its date-range parameter names are not in any record I hold; one capture or the CRO's HAR line is needed before a replay.
- Open lots: the call takes no date (current lots only).
- Standard-format on-demand export with an early transaction date: a UI walk of the export wizard; not done this session.

## 5. What lands

Nothing from this session landed. The transactions and realized-lot answers are JSON from an API, not files: landing them needs a decision on a bronze table and a replay adapter (per account, one call per 365 days for transactions, paged by 500 for lots), which is a build cell.
