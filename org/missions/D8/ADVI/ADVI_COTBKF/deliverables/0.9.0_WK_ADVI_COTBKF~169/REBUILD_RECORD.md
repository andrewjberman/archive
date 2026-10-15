# REBUILD_RECORD -- ADVI_COTBKF CB-ch-1 (round 86), worker 0.9.0_WK_ADVI_COTBKF~169

Counts, dates, codes and hashes only. No account number, name or value appears here; the two rebuilt files sit outside the repository at C:/dev/_cotbkf_rebuild_20261015/.

## Result (final run, from the committed script blob edbddd5fe38712b1f0c3dc3f22389394c0729414, commit b65e3ecdbd)

| file | rows rebuilt | rows pinned | sha256 rebuilt | equal to pin |
|---|---|---|---|---|
| ACTIVE_COTTONWOOD_SET_V2.csv | 41825 | 41826 | d5999835cfb3d6bc344444c348e51a176b18b45d9cfea1664eba2fe172b1ff67 | no |
| REVERSE_MATCH_V3.csv | 860 | 860 | 0783f088aecbf29e46751aa5d80239b8aa53f16484778162e34ee1c09783c66f | yes |

## Repairs (six: three after the first report, then three under amendment 1)

1. Commit 8cd4c0a81f: the type is read as stored (164 rows of a trailing-space key were refused).
2. Commit 9f617f4fd9: the candidate id is read before its description (near 0 to 13, AMBIGUOUS 0 to 27).
3. Commit 68ffc04bc9: a pair held on both sides emits one joined row (62,754 to 41,808 rows).
4. Commit 501c066bdb: a row with no CUSIP is keyed by (ticker, name) and carries the key ticker.
5. Commit 0b88fd292f: a joined row ends where the Black Diamond side ends.
6. Commit b65e3ecdbd: a null Symbol reads as None; the stored Symbol has no nulls, so this changed no pinned ticker.

## Diff (final run, order-independent multiset)

41793 rows equal; 33 pinned-only; 32 rebuilt-only. The 25 paired rows differ on ticker only (held_to: 0). The pinned file has 737 rows with ticker text None; the rebuild has 714.

## Order is not deterministic

The window-file row order depends on PYTHONHASHSEED: three runs of the committed script gave three sha256 values. The sort key has no tie-break. The pinned file orders its 61 tied groups by held_to (61 of 61) and by window_basis (61 of 61). Not applied: the cap is reached. Surprise row ADVI_COTBKF-D1-W169-S4.

## Reverse match (equal to pin)

crosswalk_matched 460; near_match_waiting_on_a_person 13; none 387 (NEW_CLIENT_AFTER_MIGRATION 168, MISMATCH_NO_IDENTIFIER 101, OTHER 91 with NO_CANDIDATE_OVERLAP 91, AMBIGUOUS 27); account_links 0.

## Definition (equal to record)

snapshot accounts 999; zero-unit-only 139; primary 860; count_769 769; count_90d 875; primary minus 769 = 91; primary minus 90d = -15; cash-only added 91.

## Sources read (listing denominators in REBUILD_RECORD.json)

silver holdings 88 of 90 listed read; gold holdings 135 of 137 listed read; Commonwealth transactions 14 of 14 parts read (1,416,497 rows); crosswalk.csv and account_links.csv read whole.
