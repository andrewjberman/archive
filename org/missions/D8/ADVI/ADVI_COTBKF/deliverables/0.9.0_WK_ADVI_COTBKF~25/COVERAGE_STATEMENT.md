# Commonwealth / Cottonwood backfill -- coverage statement (data date 2026-06-23)

## What the backfill covers, by kind of record
Each kind has its OWN date span; no one range covers them all.

- TRANSACTIONS: 1,416,497 rows, trade dates 2013-04-03 to 2026-06-22, 1,533 accounts; 1,360 rows are exact repeats of an earlier row on all 20 vendor columns, kept by design (C-SILVER: two identical lines may be two real events; see TX_REPEATS.md)
- POSITIONS: 469 positions on one day, 2026-06-23, 83 accounts (the delivery carries one snapshot)
- RETURNS: Commonwealth's own performance (returns) records, 88,654 rows, 2013-04-04 to 2026-06-23, 1,519 accounts; 14 of 1,533 transacting accounts have no performance record (the delivered performance file does not list them; ROW: ADVI_COTBKF-W23-S5)
- STATEMENTS: 7,736 account statements (PDF), dated 2025-06-30 to 2026-05-31
- TAX FORMS: 1,034 tax documents (PDF), dated 2025-02-09 to 2026-06-06 (dates read from the file name)
- CRM: NOT COVERED. The CRM zip is NOT in the backfill yet: it is held back behind the C-RESTRICTED prefix. REASON: the restricted prefix is fenced and its policy is not re-gradable from here. ROW: ADVI_COTBKF-S7, ADVI_COTBKF-W19-S1
- PRICES: NOT COVERED. Only 1,720 of the 4,634 securities traded are priced from Opal's own stores, 1,297,651 of 9,388,961 security-days covered. REASON: the price pull waits on another project's store; the bd and inf price files are barred to this project. ROW: ADVI_COTBKF-S17

## By storage table

What each table holds (counts read from the applied table) and what it does not (reason + surprise-channel row).

### silver / account_links
COVERS:
- 1,450 old Commonwealth accounts (first trade 2013-04-03 to last trade 2026-06-22), each linked or not to a later account
- 212 LINKED, 1,238 NOT_LINKED
NOT COVERED:
- 587 accounts left Commonwealth and are not linked. REASON: they left in kind with no receiving account matched. ROW: ADVI_COTBKF-W13-S1
- Chains are followed only through old accounts. REASON: 46 of 148 non-old link targets stopped trading before 2026 and their own replacements are not in this table. ROW: ADVI_COTBKF-W11-S2
- 21 near-match crosswalk accounts are not linked, awaiting a person. REASON: a mutual-fund line moved between departure and arrival, so the 80 percent bar leaves it unapplied. ROW: ADVI_COTBKF-W14-S2

### silver / coverage
COVERS:
- 5 record kinds (transactions, performance month/year/inception, positions), computed from the silver tables
- transactions 1,416,497 rows, 1,533 accounts, 2013-04-03 to 2026-06-22
NOT COVERED:
- Documents, imaging and the crosswalk are not in this table. REASON: it grades only the three silver data tables; this statement is the only account of the rest. ROW: ADVI_COTBKF-W23-S4

### silver / crosswalk
COVERS:
- 1,533 Commonwealth accounts, each MATCHED or NOT_MATCHED to a current Cottonwood account
- 439 MATCHED; NOT_MATCHED: 788 no current account holds the positions, 212 closed before current history, 37 flat, 36 ambiguous, 21 awaiting a person
NOT COVERED:
- 788 accounts have no current account holding their positions. REASON: no current account's first holdings reproduce them. ROW: ADVI_COTBKF-W10-S4
- 36 ambiguous accounts are not resolved. REASON: one-position accounts and cv-prefixed twins fit more than one account. ROW: ADVI_COTBKF-W10-S4
- 21 near-match crosswalk accounts are not linked, awaiting a person. REASON: a mutual-fund line moved between departure and arrival, so the 80 percent bar leaves it unapplied. ROW: ADVI_COTBKF-W14-S2

### silver / document_index
COVERS:
- 11,119 documents of 6 types, each with its own dates: ADVS 165 (2016-02-25 to 2022-12-15); CLNT 932 (2025-06-24 to 2026-06-18); NCSD 1,239 (2016-02-25 to 2026-04-17); REPR 13 (2025-10-10 to 2026-05-28); STMT 7,736 (2025-06-30 to 2026-05-31); TXRP 1,034 (2025-02-09 to 2026-06-06)
- all 11,119 listed and present; 3 archives; 985 distinct accounts
NOT COVERED:
- 1,544 of 11,119 documents carry no account. REASON: the NCSD, ADVS and REPR listings (and 127 CLNT) carry no account number. ROW: ADVI_COTBKF-W23-S3
- 10,085 documents have no page count. REASON: the vendor listing gives none (REPR carries a literal W). ROW: ADVI_COTBKF-W9-S1
- 3,383 documents are dated from the file name, not a listing date. REASON: TXRP and the other types carry no per-document date. ROW: ADVI_COTBKF-W9-S1
- The CRM zip is NOT in the backfill yet: it is held back behind the C-RESTRICTED prefix. REASON: the restricted prefix is fenced and its policy is not re-gradable from here. ROW: ADVI_COTBKF-S7, ADVI_COTBKF-W19-S1

### silver / documents
COVERS:
- 11,119 PDFs written at their target keys, apply ledger documents.parquet: 11,119 VERIFIED of 11,119 rows
- 1,795,905,639 bytes
NOT COVERED:
- Nothing from the CRM zip is in this table. REASON: the restricted prefix is fenced and its policy is not re-gradable from here. ROW: ADVI_COTBKF-S7, ADVI_COTBKF-W19-S1
- 1,544 PDFs carry no account in the ledger. REASON: the NCSD, ADVS and REPR listings (and 127 CLNT) carry no account number. ROW: ADVI_COTBKF-W23-S3

### silver / performance
COVERS:
- 80,709 month, 6,425 year and 1,520 inception rows, 1,519 distinct accounts at inception, 2013-04-04 to 2026-06-23
NOT COVERED:
- 14 of 1,533 transacting accounts have no performance record. REASON: the delivered performance file does not list them. ROW: ADVI_COTBKF-W23-S5

### silver / positions
COVERS:
- 469 positions on one day (2026-06-23), 83 accounts
NOT COVERED:
- Positions on any other day; 1,450 of 1,533 accounts. REASON: the delivery carries one positions snapshot, so earlier holdings are rebuilt from transactions. ROW: ADVI_COTBKF-W23-S2
- Prices: only 1,720 of the 4,634 securities traded are priced from Opal's own stores, 1,297,651 of 9,388,961 security-days covered. REASON: the price pull waits on another project's store; the bd and inf price files are barred to this project. ROW: ADVI_COTBKF-S17

### silver / transactions
COVERS:
- 1,416,497 rows, 1,533 accounts, 4,634 distinct securities (CUSIP), trade dates 2013-04-03 to 2026-06-22
NOT COVERED:
- No single account spans 2013 to 2026; the longest is 10.4 years. REASON: the 2013-2017 history sits under different account numbers. ROW: ADVI_COTBKF-S2
- The applied row count 1,416,497 differs from the 1,415,137 an earlier row reported. REASON: an earlier row said exact duplicates were dropped; the applied table holds the full count. ROW: ADVI_COTBKF-W23-S1
- Prices: only 1,720 of the 4,634 securities traded are priced from Opal's own stores, 1,297,651 of 9,388,961 security-days covered. REASON: the price pull waits on another project's store; the bd and inf price files are barred to this project. ROW: ADVI_COTBKF-S17

### bronze / imaging
COVERS:
- 3 zips, 3,171,626,456 bytes, 24,489 PDFs listed in the document index archives
NOT COVERED:
- The CRM zip is NOT in the backfill yet: it is held back behind the C-RESTRICTED prefix. REASON: the restricted prefix is fenced and its policy is not re-gradable from here. ROW: ADVI_COTBKF-S7, ADVI_COTBKF-W19-S1

### bronze / manifest
COVERS:
- delivery commonwealth/cottonwood, data date 2026-06-23, received 2026-10-06; 4 shipped files, 24,546 members
NOT COVERED:
- The CRM zip is NOT in the backfill yet: it is held back behind the C-RESTRICTED prefix. REASON: the restricted prefix is fenced and its policy is not re-gradable from here. ROW: ADVI_COTBKF-S7, ADVI_COTBKF-W19-S1

### bronze / portfolio_accounting
COVERS:
- 1 zip, 23,833,956 bytes, holding the transactions, performance and positions files
NOT COVERED:
- Nothing beyond the three files of that one zip. REASON: the delivery carries one portfolio-accounting zip for all three. ROW: ADVI_COTBKF-S1

