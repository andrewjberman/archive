# Review sheet record (ADVI_COTBKF round 104, CB-da-1)

Counts and source names only. The workbook is on the desktop, outside the repository; this record carries no account number, name, security name or value.

| Measure | Count |
|---|---|
| Rows to confirm (To confirm sheet) | 107 |
| Already matched (settled) | 11 |
| Households (To confirm) | 70 |
| Strong / likely / weak | 0 / 12 / 95 |
| Competing groups among rows to confirm (rows) | 18 (42) |

## Not established

- Which candidate is right: not established. The sheet shows whether a pair passed or failed the packet's tests, and a Yes is the confirmer's word.
- Black Diamond value is the sum of the holdings market_value on the account's latest holdings date; prices were not re-derived.
- Commonwealth old account value is the total on the last date the account held a security, the date its top holdings come from; 9 of the 115 distinct Commonwealth accounts never held a security and show the last valued day instead.
- Commonwealth security names are not on the Commonwealth side: they are taken from the Black Diamond asset_name for the same CUSIP.
- The household label is the Black Diamond relationship name; the packet carries no household name, so the Commonwealth side is not grouped by household.
- Restricted CRM fields: none of tax identifier, date of birth, driver's licence or passport appears among the columns read (document index: DisplayName, ClientName, HouseholdName and the account key fields; accounts dimension: the columns named in identifies). Not copied: client city, client state, client zip and tax status on the accounts dimension.
- Account numbers appear nowhere in the visible columns: 114 Commonwealth document names carried the account number inside their text, and the number was removed from the sheet; a name-less account shows the last four characters in brackets.
- The workbook is on the desktop only and is not in git; the record carries counts and source names only.
