# ACTIVE_SET_V2_RECORD -- ADVI_COTBKF CB-cg-1 (round 85), worker 0.9.0_WK_ADVI_COTBKF~168

Counts only. No account key, number, name or value appears in this record; the two data files sit outside the repository.

## Headline

860 accounts are open in the 2026-10-12 snapshot under the primary definition (769 non-cash non-zero plus 91 cash-only; 139 zero-unit-only accounts excluded); 875 under the 90-day alternative; 41,826 window rows cover 3,368 securities. Reverse match: 460 crosswalk-matched, 13 near match awaiting a person, 0 account_links, 387 none (168 NEW_CLIENT_AFTER_MIGRATION, 101 MISMATCH_NO_IDENTIFIER, 91 OTHER, 27 AMBIGUOUS). Invariants against round 82: 9 of 15 match; the reverse match matches on every count; the window rows do not (41,462 on the 769 set against 42,319).

## Definition

open = at least one row in the latest Black Diamond holdings snapshot (silver/holdings, dated 2026-10-12) with units non-null and non-zero, cash-equivalent rows included; zero-unit-only and null-unit-only accounts are not open and are counted separately

| count | value |
|---|---|
| snapshot accounts (any row, 2026-10-12) | 999 |
| zero/null-unit-only accounts (excluded) | 139 |
| count_primary | 860 |
| count_769 (non-cash, non-zero, latest) | 769 |
| count_90d (non-cash, non-zero, any snapshot 2026-07-14..2026-10-12) | 875 |
| primary minus 769 (integer; set: 91) | 91 |
| primary minus 90d (integer; set: 85 primary-only, 100 90d-only) | -15 |
| cash-only accounts added over 769 | 91 |
| crosswalk-current accounts outside 769 / of them in primary | 14 / 3 |

## Files

| file | rows | sha256 | bytes |
|---|---|---|---|
| ACTIVE_COTTONWOOD_SET_V2.csv | 41826 | 5cef7ab0c9e10fe299cb757d4dba31792d069bad35f7250defa76e18773046ae | 3358913 |
| REVERSE_MATCH_V3.csv | 860 | 0783f088aecbf29e46751aa5d80239b8aa53f16484778162e34ee1c09783c66f | 37843 |

## Invariants against round 82 (expected / got / match)

| invariant | expected | got | match |
|---|---|---|---|
| accounts_769 | 769 | 769 | MATCH |
| securities_cusip | 3357 | 3361 | DIFF |
| window_rows_total | 42319 | 41462 | DIFF |
| earliest_window_start | 2013-04-08 | 2013-04-08 | MATCH |
| joined_rows | 6736 | 6850 | DIFF |
| reverse_crosswalk_matched | 457 | 457 | MATCH |
| reverse_account_links | 0 | 0 | MATCH |
| reverse_near_match | 12 | 12 | MATCH |
| reverse_none | 300 | 300 | MATCH |
| reverse_none_reasonless_before_classification | 273 | 273 | MATCH |
| reverse_none_AMBIGUOUS | 27 | 27 | MATCH |
| commonwealth_side_rows | 15894 | 18882 | DIFF |
| black_diamond_side_rows_incl_not_established | 19689 | 15730 | DIFF |
| not_established_rows | 472 | 770 | DIFF |
| windows_clipped_by_floor | 0 | 0 | MATCH |

## Reason codes (none rows)

{"NO_COMMONWEALTH_HOUSEHOLD": 0, "NEW_CLIENT_AFTER_MIGRATION": 168, "MISMATCH_NO_IDENTIFIER": 101, "OTHER": 91, "OTHER_sub": {"NO_CANDIDATE_OVERLAP": 91, "LINKED_NOT_RECORDED": 0}, "AMBIGUOUS": 27}

## Four identifiers

| cusip | rows in set | accounts |
|---|---|---|
| 35907XEW3 | 1 | 1 |
| 38150V6Q7 | 1 | 1 |
| 912796Y37 | 1 | 1 |
| 912797GE1 | 1 | 1 |

## Not established

- Round-82 window segmentation: its script is not committed and its output keys are salted tokens, so no committed rule reproduces its window counts. Rebuilt from the stated rule (held = non-zero units; a Commonwealth window opens at the first non-zero running balance and closes on the trade that returns it to zero; a Black Diamond window is a run of consecutive gold keys with a non-zero row; a joined row is one (account, CUSIP) pair held on both sides). The rebuild gives 41,462 rows on the 769 set against 42,319 (DIFF); see invariants.
- Definition of open: units non-null and non-zero, any kind. 139 accounts have only zero or null units rows and carry no market value on any row; they are excluded and counted in zero_unit_only_accounts. The alternative of any row of any kind gives 999 accounts.
- Cash-equivalent flag: the 47 no-snapshot gold keys (2026-04-22..2026-06-07) carry no cash_equivalent column, so the flag is not established for 107,511 gold rows; those rows are kept as windows (cash included). The 47 keys also carry no cusip; their CUSIP comes from a one-CUSIP-per-asset_name map where the name is unique, else the row is not_established (834 window rows in the set are not_established, keyed by ticker and name, cusip blank).
- Joined windows: a joined row is one (account, CUSIP) pair with a Commonwealth window and a Black Diamond window; 6,886 such pairs. The overlap-tested variant gives 6,699 on the 769 set (round-82 invariant 6,736). The round-82 join rule is not recoverable from committed material.
- The 2012-01-01 floor never binds: the Commonwealth transactions begin 2013-04-03 and the Black Diamond gold keys begin 2026-04-22; windows_clipped_by_floor is 0.
- Commonwealth predecessor chain: account_links LINKED edges (old to new) are followed transitively from each crosswalk-matched Commonwealth account; 550 Commonwealth accounts belong to the set chains (547 for the 769 set; the 769 control gives former_client_accounts 986, the round-82 figure).
- account_key is the raw Black Diamond account_id of the current account for every row, including the Commonwealth-side windows of its chain; the Commonwealth account numbers are carried only in the reverse match predecessor_key column of the outside file.
- predecessor_key for a near match is the Commonwealth account that waits on a person. One Black Diamond id is a candidate of two AWAITING_PERSON rows; its predecessor_key cell carries both keys separated by a semicolon (one row, not a single key).
- none reason codes: NO_COMMONWEALTH_HOUSEHOLD is 0 because no household identifier exists on the Black Diamond side of an unmatched account (crosswalk.csv has no household column; account_links client_line joins to no Black Diamond key). NEW_CLIENT_AFTER_MIGRATION uses the partition test as the list defines it (first date any row appears in gold or silver holdings, on or after 2026-06-23); round 84 used window starts because its keys were tokens.
- MISMATCH_NO_IDENTIFIER is a CUSIP-overlap candidate test on the 2026-10-12 snapshot (any non-zero row, cash-equivalent CUSIPs included), with the candidate a Commonwealth account holding a pre-migration transaction in that CUSIP. Candidate sets run from 1 to 751 Commonwealth accounts, so the test does not discriminate between accounts; it records that a shared CUSIP exists and that no key join exists, not that a match was attempted and failed.
- four_identifiers: each identifier has one row in the set file. In the 2026-10-12 snapshot 38150V6Q7 has one row with zero units and the other three have no row; they are held in history only.
- former_client_accounts counts Commonwealth accounts with history outside the set chains (counts only). securities_only_former_clients is 1,703 by this rule (Commonwealth share-moving CUSIPs of former accounts not held by any set window); the round-82 figure 1,699 was on the round-82 windows and is not reproduced.
- Reason codes on the 273 rows of the 769 set, by the same tests: NEW_CLIENT_AFTER_MIGRATION 145 (round 84: 152), MISMATCH_NO_IDENTIFIER 96 (round 84: 89), OTHER 32 (round 84: 32), NO_COMMONWEALTH_HOUSEHOLD 0 (round 84: 0). The change is the measured partition test in place of the window-start test.
- Snapshot counts: the 769 reproduce only with non-zero units (non-cash, negative units included): the rule "units above zero" gives 766. The 90-day alternative 875 reproduces with non-zero, non-cash rows on snapshots dated 2026-07-14..2026-10-12 (1 day either side gives the same count).
- Crosswalk-current accounts outside the 769: 14, all present in the 2026-10-12 snapshot. 3 are in the set (non-zero cash rows); the other 11 have only zero or null units rows and are excluded with the zero-unit-only accounts.

## Sources

- s3://opal-data-cot/silver/holdings/ : one list-objects-v2 (auto-paginated) = 88 dated parquet keys, 2026-06-08..2026-10-12, one key per date; all 88 read (90-day alternative); the latest 2026-10-12 read for the primary definition; columns account_id, units, cusip, cash_equivalent
- s3://opal-data-cot/gold/canonical/holdings/ : one list-objects-v2 = 135 dated parquet keys, 2026-04-22..2026-10-12; all 135 read for the per-security windows and the first-appearance partition test; 47 keys (2026-04-22..2026-06-07) carry no cusip and no cash_equivalent column
- s3://opal-data-assets/commonwealth/cottonwood/silver/transactions/date=2026-06-23/ : list-objects-v2 = 14 parquet parts; all 14 read, 1,416,497 rows, 1,533 accounts; columns Account_Number, Cusip, Symbol, Quantity, Trade_Date, Transaction_Type, source_line
- s3://opal-data-assets/commonwealth/cottonwood/silver/crosswalk/date=2026-06-23/crosswalk.csv : get-object, 1,533 rows (471 MATCHED, 1,062 NOT_MATCHED; 22 AWAITING_PERSON and 38 AMBIGUOUS in reason_code)
- s3://opal-data-assets/commonwealth/cottonwood/silver/account_links/date=2026-06-23/account_links.csv : get-object, 1,450 rows (212 LINKED)
- data/assets/scripts/silver/commonwealth_signs.py (worktree HEAD 70616e8c1b): the one signed-quantity rule; 61 transaction types, 0 unsigned-with-quantity types
- org/missions/D8/ADVI/ADVI_COTBKF/deliverables/0.9.0_WK_ADVI_COTBKF~167/NONE_REASON_LIST.md and NONE_REASONS_RECORD.json: the closed list, its tests in order, migration date M = 2026-06-23 (reused unchanged)
- org/missions/D8/ADVI/ADVI_COTBKF/deliverables/0.9.0_WK_ADVI_COTBKF~161/ACTIVE_SET_RECORD.json and the round-82 files in C:/dev/_cotbkf_active_set_20261013/ (sha256 checked): the invariants
- not read: the restricted CRM prefix, any vendor or Black Diamond API, the Commonwealth silver positions table, any S3 write or delete; C:/dev/_cotbkf_private_evidence_20261009/ not opened
