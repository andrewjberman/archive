# REBUILD_RECORD -- ADVI_COTBKF CB-ch-1 (round 86), worker 0.9.0_WK_ADVI_COTBKF~169

Counts, dates, codes and hashes only. No account number, name or value appears here; the two rebuilt files sit outside the repository at C:/dev/_cotbkf_rebuild_20261015/.

## Result

| file | rows rebuilt | rows pinned | sha256 rebuilt | equal to pin |
|---|---|---|---|---|
| ACTIVE_COTTONWOOD_SET_V2.csv | 41808 | 41826 | ccd2f969803884695f6d6b597e3d48e77a4a01812634dfdf97e1c98bb3f07d5d | no |
| REVERSE_MATCH_V3.csv | 860 | 860 | 0783f088aecbf29e46751aa5d80239b8aa53f16484778162e34ee1c09783c66f | yes |

The script was run from its committed blob 867a2cf1daa21dc46432d523cf8cc29beca1b990 (commit 68ffc04bc9).

## Repairs (three; the cap)

1. Commit 8cd4c0a81f: the type was stripped before lookup, refusing 164 rows of the trailing-space key csltfee.
2. Commit 9f617f4fd9: the candidate id is read before its description; near match 0 to 13, AMBIGUOUS 0 to 27.
3. Commit 68ffc04bc9: a pair held on both sides emits one joined row and no side window; 62,754 rows became 41,808.

## Why V2 is not equal

Of the 41,808 rebuilt rows, 41,487 match a pinned row exactly. 339 pinned rows have no match and 321 rebuilt rows have no match. The paired differences are ticker (285) and held_to (48). The file is not edited to match and no further repair is made.

## Reverse match (equal to pin)

crosswalk_matched 460, near_match_waiting_on_a_person 13, none 387 (NEW_CLIENT_AFTER_MIGRATION 168, MISMATCH_NO_IDENTIFIER 101, OTHER 91 with NO_CANDIDATE_OVERLAP 91, AMBIGUOUS 27), account_links 0.

## Definition (equal to record)

snapshot accounts 999; zero-unit-only 139; primary 860; count_769 769; count_90d 875; primary minus 769 = 91; primary minus 90d = -15; cash-only added 91.

## Sources read (see REBUILD_RECORD.json for the listing denominators)

silver holdings 88 of 90 listed read; gold holdings 135 of 137 listed read; Commonwealth transactions 14 of 14 parts read (1,416,497 rows); crosswalk.csv and account_links.csv read whole.
