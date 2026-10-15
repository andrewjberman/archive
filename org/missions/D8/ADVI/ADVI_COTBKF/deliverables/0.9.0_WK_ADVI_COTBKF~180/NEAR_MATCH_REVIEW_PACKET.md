# Near-match review packet (ADVI_COTBKF round 90, CB-cl-3)

A page for the person who confirms. The packet lists candidate links, one row per distinct pair of a Commonwealth account and a Black Diamond account. A candidate is not a link: it passed or failed the rule's tests, and that is all it says. The packet cannot say which candidate is right.

The R4 route (a Commonwealth account's name reaches one Black Diamond household, then the holdings fingerprint inside it) and the exact-name route are the two sources. A pair found by both is one row.

## What the columns mean

| Column | Meaning |
|---|---|
| link_id | a 12-character id; it resolves to its two accounts only through the key kept outside the repository |
| routes | R4, NAME, or R4+NAME (both routes found the pair) |
| r4_tier | DETERMINISTIC (rests on the fingerprint, not a candidate to confirm) or CANDIDATE; blank for name-only pairs |
| r4_household_via | how the household was reached: the account name, or the client line |
| r4_window_ok | whether the dates fall inside the derived window |
| r4_fingerprint_band | the holdings fingerprint score as a band (<0.5, 0.5-0.8, >=0.8); never the number |
| name_corroborations | 0 to 3: how many of date window, registration class and holdings agree on the name pair |
| in_219 | the Black Diamond account is one of the 219 reachable unmatched active accounts |
| bd_account_state | unmatched_active, new_client, near_match_waiting (already waiting on a person), or other |
| competing_pairs | how many other pairs in this packet share either account: a conflict a person must see |

## Counts

| Measure | Count |
|---|---|
| Distinct pairs (rows) | 118 |
| Routes R4 / NAME / R4+NAME | 104 / 8 / 6 |
| R4 tier DETERMINISTIC / CANDIDATE / blank | 11 / 99 / 8 |
| To confirm (rows not DETERMINISTIC) | 107 |
| Among the 219 reachable unmatched active accounts | 102 |
| With a competing pair | 44 |
| R4 rows / name rows / overlap | 110 / 14 / 6 |
| Rows the packet's checks could not resolve | 0 |

No link here is applied; a link applies only on a person's word; Andrew names who confirms.

The file has 119 lines, a header and 118 rows.

