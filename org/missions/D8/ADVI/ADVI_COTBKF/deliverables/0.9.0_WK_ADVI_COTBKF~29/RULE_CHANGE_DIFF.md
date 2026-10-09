# Rule change diff (CB-m-2): the ONE signing table against the applied tables

Before = the applied silver table read from S3; after = the same script re-run locally on the same cached inputs, nothing applied. Rows compared by key.

## crosswalk (key commonwealth_account; compared: status, rule, current_account, score)

- rows (distinct keys over both sides): 1533 (before 1533, after 1533)
- rows changed: 65; changed field lines: 161
- MATCHED before: 439; after: 471

Class counts, status (before -> after):

- MATCHED: 439 -> 471
- NOT_MATCHED: 1094 -> 1062

Class counts, rule (MATCHED) (before -> after):

- R2-in-kind-transfer: 439 -> 471

Class counts, reason_code (NOT_MATCHED) (before -> after):

- AMBIGUOUS: 36 -> 38
- AWAITING_PERSON: 21 -> 22
- CLOSED_BEFORE_CURRENT_HISTORY: 212 -> 188
- NO_CURRENT_ACCOUNT_HOLDS_POSITIONS: 788 -> 770
- NO_SECURITY_POSITIONS: 37 -> 44

Changed field lines by reason:

- current_account moves with the status change NOT_MATCHED -> MATCHED: 32
- match gained: NOT_MATCHED -> MATCHED: 32
- rule moves with the status change NOT_MATCHED -> MATCHED: 32
- score moves with the status change NOT_MATCHED -> MATCHED: 32
- still NOT_MATCHED, score changed: 33

Not counted as changes (the order compares only the fields above), rows whose value differs:

- reason_code: 66
- positions_compared: 76
- positions_matched: 36
- holdings_basis: 67

Changed rows (account, field, before -> after):

- acct#03b1818c, status, NOT_MATCHED -> MATCHED
- acct#03b1818c, rule,  -> R2-in-kind-transfer
- acct#03b1818c, current_account,  -> z0926757511
- acct#03b1818c, score,  -> 0.966700
- acct#a56947be, score,  -> 0.483900
- acct#afff21b7, score,  -> 0.000000
- acct#fe3aa89f, status, NOT_MATCHED -> MATCHED
- acct#fe3aa89f, rule,  -> R2-in-kind-transfer
- acct#fe3aa89f, current_account,  -> z0926704991
- acct#fe3aa89f, score,  -> 1.000000
- acct#c35ddef3, status, NOT_MATCHED -> MATCHED
- acct#c35ddef3, rule,  -> R2-in-kind-transfer
- acct#c35ddef3, current_account,  -> z0926704451
- acct#c35ddef3, score,  -> 1.000000
- acct#7c2950f8, score,  -> 0.000000
- acct#3514364a, score,  -> 0.000000
- acct#487a177f, status, NOT_MATCHED -> MATCHED
- acct#487a177f, rule,  -> R2-in-kind-transfer
- acct#487a177f, current_account,  -> z0926725281
- acct#487a177f, score,  -> 1.000000
- acct#5446c1d7, status, NOT_MATCHED -> MATCHED
- acct#5446c1d7, rule,  -> R2-in-kind-transfer
- acct#5446c1d7, current_account,  -> z0926652341
- acct#5446c1d7, score,  -> 1.000000
- acct#0d10c089, status, NOT_MATCHED -> MATCHED
- acct#0d10c089, rule,  -> R2-in-kind-transfer
- acct#0d10c089, current_account,  -> z0926652331
- acct#0d10c089, score,  -> 1.000000
- acct#bd6094c0, status, NOT_MATCHED -> MATCHED
- acct#bd6094c0, rule,  -> R2-in-kind-transfer
- acct#bd6094c0, current_account,  -> z0926768821
- acct#bd6094c0, score,  -> 1.000000
- acct#6b93dd15, score,  -> 0.000000
- acct#8179a706, score,  -> 0.750000
- acct#1665d973, status, NOT_MATCHED -> MATCHED
- acct#1665d973, rule,  -> R2-in-kind-transfer
- acct#1665d973, current_account,  -> z0926725221
- acct#1665d973, score,  -> 1.000000
- acct#77c2edca, status, NOT_MATCHED -> MATCHED
- acct#77c2edca, rule,  -> R2-in-kind-transfer
- ... 121 more in rule_change_rows.csv

## account_links (key old_account; compared: status, new_account)

- rows (distinct keys over both sides): 1450 (before 1450, after 1450)
- rows changed: 2; changed field lines: 4
- LINKED before: 212; after: 212

Class counts, status (before -> after):

- LINKED: 212 -> 212
- NOT_LINKED: 1238 -> 1238

Class counts, reason (NOT_LINKED) (before -> after):

- LEFT_COMMONWEALTH: 587 -> 588
- ambiguous: 14 -> 14
- below threshold: 91 -> 90
- closed to cash: 495 -> 544
- no in-kind receiver: 51 -> 2

Changed field lines by reason:

- match gained: NOT_LINKED -> LINKED: 1
- match lost: LINKED -> NOT_LINKED: 1
- new_account moves with the status change LINKED -> NOT_LINKED: 1
- new_account moves with the status change NOT_LINKED -> LINKED: 1

Not counted as changes (the order compares only the fields above), rows whose value differs:

- reason: 52
- end_positions: 87
- matched: 1
- score: 52

Changed rows (account, field, before -> after):

- acct#e1e2dacb, status, NOT_LINKED -> LINKED
- acct#e1e2dacb, new_account,  -> acct#f6464238
- acct#d6187d4b, status, LINKED -> NOT_LINKED
- acct#d6187d4b, new_account, acct#8f547eb0 -> 

