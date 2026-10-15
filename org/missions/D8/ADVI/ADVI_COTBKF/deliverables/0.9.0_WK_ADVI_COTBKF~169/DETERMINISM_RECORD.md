# DETERMINISM_RECORD -- ADVI_COTBKF CB-ci-6 (round 87), worker 0.9.0_WK_ADVI_COTBKF~169

Counts, dates, codes and hashes only. No account number, name or value appears here; the window files sit outside the repository at C:/dev/_cotbkf_rebuild_20261015/seed0, seed1 and seed2.

## Change

One change to cotbkf_active_set_v2.py (commit 925acb1946, blob 3e1c727a2838be89573914fc769258379c04deda): the window rows are sorted by the total key (account_key, source_side, cusip, held_from, held_to, window_basis, ticker). The ticker is the seventh element because eight pinned groups share the six fields and differ only by ticker. The pinned order does not follow ticker in seven of those eight, which is stated as residual; it is not chased.

## Runs (the committed script, three hash seeds)

| seed | V2 sha256 | V3 sha256 |
|---|---|---|
| 0 | a266c8fbf5c348d57b0f93adae76c365512dc3b766335760a449b841d8f120a3 | 0783f088aecbf29e46751aa5d80239b8aa53f16484778162e34ee1c09783c66f |
| 1 | a266c8fbf5c348d57b0f93adae76c365512dc3b766335760a449b841d8f120a3 | 0783f088aecbf29e46751aa5d80239b8aa53f16484778162e34ee1c09783c66f |
| 2 | a266c8fbf5c348d57b0f93adae76c365512dc3b766335760a449b841d8f120a3 | 0783f088aecbf29e46751aa5d80239b8aa53f16484778162e34ee1c09783c66f |

Deterministic: true (one V2 hash, one V3 hash across the three seeds). V3 equals its pin. V2 does not equal its pin.

## Residual against the V2 pin (counts only)

41793 rows equal as a multiset; 33 pinned-only (commonwealth 23, black_diamond 9, both 1); 32 rebuilt-only (commonwealth 21, black_diamond 8, both 3). The 25 paired rows differ on ticker only (held_to: none). Not explained to a rule; stated, not repaired.
