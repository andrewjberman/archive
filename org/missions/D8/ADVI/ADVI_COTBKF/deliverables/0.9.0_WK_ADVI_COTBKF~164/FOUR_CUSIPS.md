# CB-ce-1 -- four identifiers missing from the set (round 83)

Read-only. Counts, dates and reason codes only: no account key, number or value is in this record. The four
identifiers are named in `FOUR_CUSIPS.json` (keys `cusip`, in the order the task order lists them).

## Four identifiers

- Rows in the set: 0 for each of the four.
- Commonwealth trades: one account traded each (38, 2, 2 and 2 rows). That account is MATCHED in the crosswalk to a
  current account that is NOT in the 769-account active set. Active accounts that traded any of the four: 0.
- Cause, each: `former_client_only`.
- One holder (cause row 2) holds its identifier non-zero in 74 of 88 silver snapshots 2026-06-08..2026-10-12, but its
  2026-10-12 snapshot has no non-cash non-zero row, so it is not active by the set's definition.
- Additions: no active account held any of the four, so `ACTIVE_SET_ADDITIONS.csv` holds the header only (68 bytes).

## Generalization (set-wide, see not_established)

- Distinct CUSIPs traded by the 547 Commonwealth accounts of active accounts: 2760.
- Carried by the set for any active account: 2753. Missing: 7.
- Missing by cause: `window_rule_dropped_it` 4 (dividend-only; unsigned by `commonwealth_signs.py` line 63),
  `other` 3 (cash-sweep identifiers, asset type Cash). Listed in `MISSING_BY_CAUSE.csv`.
- Fixed income among the missing: 0 (CUSIP prefix 9127 or Asset_Type Fixed Income).

## Not established

- The account-key derivation was not reproduced: the salt is absent from this tree (surprise ADVI_COTBKF-D2-W164-S1).
- The active list mixes raw and token keys (surprise ADVI_COTBKF-D2-W164-S3); membership of 312 accounts is not
  checkable by key.
- BD holdings were checked by CUSIP in silver (88 of 88 files) and gold canonical (88 of 135 files; 47 carry no cusip
  column).
