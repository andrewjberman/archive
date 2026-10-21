# FIDUPL msg 8984 -- the two reads (counts, names and numeric paging values only)

Author 2.0.0_SA_COO~P1, 2026-10-21 ~04:55Z. No account number, G number, firm label, cookie or token appears here.

## 1. Does account.txt carry a G number or rep code per account? NO column does.

Source: the landed account.txt of business day 20261019 under `fidelity/alongside/bronze/account/` (read from S3 by `lib/opal_naming.py address()`; script `acct_g_column.py`, session scratchpad). Method: for each of the 141 columns, non-blank count, distinct count, length range, numeric share, top-value share.

- Rows: **5009**, every row 141 columns wide, column 0 (the account number) 5009 distinct. The switcher's `available` for the starting G was **5204** (probe 2P, one run) and 5197 / 5197 / 5202 in the three hand captures: the file holds 195 fewer accounts than the starting G's book.
- Columns with a SMALL distinct count and non-blank on (almost) every row: col 1 (4 distinct, one value 99%), col 2 (4 distinct, 4 characters), col 9 (2), col 13 (2), col 16 (2, an 8-digit date), col 17 (1), col 26 (4), cols 28-32 (4 each), col 33 (2). Columns with 50-600 distinct: col 7 (61 distinct but only 138 non-blank), col 24 (549 distinct), col 25 (271 distinct, 761 non-blank), col 10 (523 distinct, 761 non-blank). The rest are near-unique (accounts, names, dates) or blank.
- **No column has a count near 31 (the G numbers) or 8 (the firms) on a fully populated column.** The split cannot key off account.txt alone; the switcher's per-G lists remain the account-to-G source.

## 2. The HARs (5 files in `C:/Users/Test/Downloads/`, off git): does any carry an accountList call with `start` above 0 or a `sessionCacheId`? NO.

- `accountList.json` appears in 3 of the 5 HARs, once each (16:23, 17:08, 17:23 on 2026-10-19/20). Each request carries only `length`=2000, `accountNumber` empty, `sourceCode`, `custodianCode`. Each response: 2000 rows, `available` 5197 / 5197 / 5202, `start` null, `sessionCacheId` null, `numberOfAccounts` 2000.
- The page JavaScript is in the first HAR (`unified-access-layer-v26.9.30.S217.min.js`, 200,312 bytes). Read from it, names only:
  - The UI does NOT page `accountList.json`. After the response it tests `available === -1 || available > 2000` and shows "Too many results to display. Please enter more text to narrow your search." There is no `start`, `sessionCacheId` or paging field in its request object (`length: maxResults`, `accountNumber`, `sourceCode`, `custodianCode`).
  - Other endpoints of the same app: `/ssc/accountsearch/wc/channel/service/v1/allAccountsList.json` (POST JSON body `{}`; the response has top-level `accounts`, `pageResponse.available`, `timestamp`, no `accountListResponse` wrapper) and `/ssc/accountsearch/wc/channel/accountSearch.json` (POST JSON array of `{column, operator, value}` filters; the response is `accountSearchResponse.accounts` and `.pageResponse.available`).
  - Other lists of the app page with `pageRequest.startPage` and `pageRequest.pageSize` (clientSearch/findClients.json, groupSearch/findGroups.json); `accountList.json` is not shown using them.
- So the probe's eleven forms could not have worked: the endpoint is not paged by design (a book above 2000 is "too many, narrow your search"). Why the one-character `accountNumber` answers carried no `available` is NOT explained by these reads (the probe printed no row count for them); the bundle shows `accountNumber` narrowing is a different call (`accountSearch.json`).

## What this changes

- Probe v2 (FT-s-9 REPAIR 1, in build) is amended: it also tries `allAccountsList.json` (JSON `{}`), and `accountList.json` with `pageRequest.startPage` / `pageRequest.pageSize`; the per-G book size sweep stays and is the main measurement: it says how many G numbers exceed 2000, which decides whether the pager matters at all.
