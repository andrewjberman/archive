# Exact-name 1:1 review list (ADVI_COTBKF round 87, CB-ci-5)

A candidate list for a person to confirm. Not a link: tier REVIEW, nothing consumes it. No name, name token,
hash of a name or account number is in this file; the link ids resolve only through the key outside the repository.

| Measure | Count |
|---|---|
| Exact-name pairs | 28 |
| 1:1 pairs (on the list) | 14 |
| Pairs whose Commonwealth account hits 2+ active accounts | 9 |
| Pairs whose active account is hit by 2+ Commonwealth accounts | 5 |
| Pairs whose active account is a new client (not in the 219) | 4 |
| List rows in the 219 reachable | 13 of 14 |
| Corroborations 0 / 1 / 2 / 3 | 0 / 5 / 9 / 0 |
| Rows already claimed in the served crosswalk | 0 |

Denominators: 1062 unmatched Commonwealth, 387 unmatched active (168 new clients), 219 reachable.

## Not established

- Commonwealth registration class: no class column in transactions and no class key among the 21 document_index listing_fields keys; same_registration_class is null on every row. The research's 18 class corroborations are not reproduced from the named tables.
- transactions Position_Type (CASH, MARGIN) is a per-line position type, not a registration class; not used.
- Positions file not read (outside the grant): holdings as it left are the transaction rebuild (holdings_as_left), not the 2026-06-23 positions.
- Exact name only: recall is low (research control: 93 of 462 already-matched pairs agree on exact name), so absence from the list says nothing about a pair.
- Two real clients sharing one name are not separable by name; no wrong-1:1 control was run on matched pairs.
- STOP_TOKENS is a judgement; a different stop list moves the hit count.
- Document name fields: DisplayName, ClientName, HouseholdName only; DocumentName, DocName and ReportName are document titles and are not used.
- Black Diamond name fields: account_name and account_display_name only.
- already_claimed is measured against the served crosswalk only.
- No tax id or date of birth on either readable side; the restricted CRM prefix and zip were not read.
