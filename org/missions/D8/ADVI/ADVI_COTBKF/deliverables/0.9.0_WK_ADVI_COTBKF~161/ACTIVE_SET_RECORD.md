# CB-cd-1 -- active Cottonwood set and reverse match (round 82)

Read-only. Counts only: no account key, number, name or value is in this record. The two data files sit outside the
repository at `C:/dev/_cotbkf_active_set_20261013/` (account keys must not enter the tree).

## Definition (written before the count)

- Primary: holds a non-cash position with non-zero units in the latest Black Diamond holdings snapshot, dated 2026-10-12.
  The snapshot lists 999 accounts; 769 of them hold such a position.
- Alternative 1: holds such a position in any snapshot dated in the last 90 days (2026-07-15..2026-10-12, 63 dated snapshots): 875 accounts. Differs from primary by 106.
- Alternative 2: its Commonwealth chain has any transaction dated in the last 90 days: 0 accounts. Differs from primary by 769. The Commonwealth transactions end 2026-06-22, so this set is empty.

## Files

| file | rows | bytes | sha256 |
|---|---|---|---|
| ACTIVE_COTTONWOOD_SET.csv | 42319 | 3868045 | eb9dd0c3f6def67eab31c1b931e7fe66ad07ef37e2600908733da0a154afebfc |
| REVERSE_MATCH.csv | 769 | 77473 | 20fb38333542b23beab5a61316cf9acdc0119dbf0be85b55fe150ec191c09a64 |

## Active set

- Active accounts 769; securities 3357; window rows 42319; earliest window start 2013-04-08.
- Windows clipped by the 2012-01-01 floor: 0. Windows joined across a predecessor link: 6736.
- Former-client Commonwealth accounts (history, no position in the primary set): 986. Securities held only by former clients: 1699.

## Reverse match (current accounts 769)

- crosswalk_matched 457; account_links 0 (links join Commonwealth accounts only; see surprise ADVI_COTBKF-D2-W161-S3);
  near_match_waiting_on_a_person 12; none 300. The four classes sum to 769; rows in file 769.
- Of the 300 none accounts, 27 carry an AMBIGUOUS crosswalk reason and the rest carry none.

## Surprise rows filed (dell2, ADVI_COTBKF-W161)

- ADVI_COTBKF-D2-W161-S1 near_matches.csv absent (21 vs 22)
- ADVI_COTBKF-D2-W161-S2 Commonwealth identifiers are raw, not acct# tokens
- ADVI_COTBKF-D2-W161-S3 account_links class is empty by construction
- ADVI_COTBKF-D2-W161-S4 Commonwealth transactions end 2026-06-22
- ADVI_COTBKF-D2-W161-S5 gold canonical schema is not BD-only by column

Not established: see the `not_established` list in `ACTIVE_SET_RECORD.json`.
