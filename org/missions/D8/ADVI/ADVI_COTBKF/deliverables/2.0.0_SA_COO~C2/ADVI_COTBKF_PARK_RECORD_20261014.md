# ADVI_COTBKF -- PARK RECORD, written by 2.0.0_SA_COO~C2 on dell2, 2026-10-14T01:00Z

**Parked by:** `1.0.0_SA_CTO~DELL2`, round-86 analysis `org/tier1_exec/1.0.0_SA_CTO/deliverables/CTO_ROUND_ANALYSIS_ADVI_COTBKF_ROUND_86_PARK_20261014.md` @5288c61f29 (msg 7376), on the CVO's slug (`REMEDIATION_v51.md` @239f84375d, CB85cg1-AC3 PASS), under the dell2 pivot direction O4 ("ONE active-set + reverse-match cell, then PARK"). No round 87. The register's PARKED row is carried by `0.0.0_AB_MSTR~DELL2`.
**Un-park condition (the CTO's):** Andrew's word, or the ARD route to a page being applied (which carries the UNVERIFIED label's pair and the price correction).

## What the project leaves

| item | value | where |
|---|---|---|
| Active set | **860 accounts**, 3,368 securities, 41,826 window rows; sha256 `5cef7ab0c9e10fe299cb757d4dba31792d069bad35f7250defa76e18773046ae` | `org/missions/D8/ADVI/ADVI_COTBKF/deliverables/2.0.0_SA_COO~C2/ACTIVE_COTTONWOOD_SET_V2.csv` @4d427d3bbb |
| Reverse match | 860 rows: 460 matched, 13 near, 387 none, each with a reason; sha256 `0783f088aecbf29e46751aa5d80239b8aa53f16484778162e34ee1c09783c66f` | `.../REVERSE_MATCH_V3.csv` @4d427d3bbb |
| Definition (the CTO's, msgs 7343, 7364) | open at Black Diamond on the latest snapshot (2026-10-12), cash included. 999 accounts appear; **139 have only zero or null units and are EXCLUDED** (they hold nothing to price; any past holdings come through their Commonwealth predecessor where matched). 91 of the 860 are cash-only accounts added over the round-82 definition (769); the 90-day alternative was 875 (85 only in the new set, 100 only in the 90-day set) | `ACTIVE_SET_V2_RECORD.json` (worker ~168, merged bd08ff5eb4) |
| Keys | raw account ids on both sides, one key space (Andrew-direct 2026-10-09; the round-82 tokens' salt is lost) | all 860 reverse-match keys are 11-character raw ids |
| Scan test | `data/assets/scripts/silver/tests/test_cotbkf_no_account_ids.py`: 871 files, 0 hits, 4 of 4 named files exempt by path and sha256; a wrong pin on either new file fails (measured) | @4d427d3bbb, @92ab57aedf |
| The round-82 pair | `ACTIVE_COTTONWOOD_SET.csv`, `REVERSE_MATCH.csv` stay in the tree as a record, superseded by V2/V3, still exempt by their pins | @ec617572b8 |
| Rule for dell1 | former clients are excluded from every draw | the CTO's carry to MDPF_DEMQUE |

## Named gaps, with their owners

1. **The round-85 build scripts are LOST; V2/V3 cannot be reproduced.** They were uncommitted scratch in worker ~168's worktree (my order said run outputs go in `.scratch`, never committed); I removed the worktree after the merge. A disk search finds none and the harness keeps no subagent transcript. The files are intact and hashed (above); dell1 consumes the files, not the scripts (CTO ruling A, msg 7380). **Owner:** the first cell of any un-park, which rewrites the scripts from `ACTIVE_SET_V2_RECORD.json`, commits them, re-runs them and compares both hashes. Lesson row: `D2-S137`. Same class: round 82's window script (`W168-S2`).
2. **The round-82 window counts differ from the rebuild on the same 769 accounts** (window rows 42,319 vs 41,462): 6 of 15 aggregates DIFF, named in `ADVI_COTBKF_ROUND_85_DRAIN_END_20261014.md`; the CTO called them expected under the new definition; the CVO graded round 85 PASS. Not explained further.
3. **`month_grades` Year and InceptionToDate columns (10 of 19) were not measured** for the `porting_verdict` change; deferred with the label's apply (CTO msg 7360).
4. **The price errors (APH, CTVA, HON) in the minted tables are a PARKED defect.** The ARD route reaches no page (`route_not_live`, round 82; row `D2-S135`, the CTO's disarm of `D2-W155-S1`). Preconditions on that route ever going live: the UNVERIFIED label's never-widen pair and apply (the label is built, counted and tested locally, 61 tests; the COO half is a DRAFT, `deliverables/0.9.0_WK_ADVI_COTBKF~165/NEVER_WIDEN_R83_PORTING_VERDICT_COO_HALF.md`), and the correction of those prices (cause not established: the first stage off 1.0 is the store row against the cached vendor Close).
5. **The 15-fund quote call `XB-20261012T024430Z-8522` sat unread for 45 hours** in this seat's `read/` folder (moved, never opened by me), until the dell1 manager's ask (msg 7366). Acked 2026-10-14T00:25:49Z; receiving side closed SERVED at 00:28:29Z on the CTO's ruling (msg 7371): round 80 CB-cb-2, 7 of 15 funds landed, 8 REJECTED `LOW_TRADE_AGREEMENT`. Status HALF-CLOSED (to only): dell1 closes its `from` side.

## ARMED rows at the park (the tool reads 10; the disarm clock is the CVO's)

`comp-surprise --project ADVI_COTBKF`: 10 armed, 0 open, 0 defects. **Mine to disarm:** `D2-W50-S1`, `-S2`, `-S3` (disarmed in words by row `D2-S39`, the clock not advanced), `D2-W66-S1` (the producer's closed vocabularies hold no value for FWD-3's method; the rows carry NULL), `D2-W155-S1` (the CTO's disarm, row `D2-S135`; the clock not advanced), `D2-W159-S1` (the store holds two `asset_name` values under one ticker; fixed in the four readers by round 83, same fact as `W158-S2`), `D2-W168-S2` (gap 2). **The CTO's:** `D2-S60`, `D2-S92`, `D2-W158-S2`. The disarm rows I filed are `D2-S134` (void, per the CVO), `S135`, `S136`; none advances a clock. These ride the park to `0.0.0_AB_MSTR~DELL2` and the CVO; this seat stands down and cannot disarm them.

## The rounds (this lane's, 2026-10-13/14)

Round 80 (3 cells, issued late: the previous session ended before the spawn), 81 (3), 82 (3, plus a fourth drafted but refused by the one-issuer-per-round gate), 83 (3), 84 (1), 85 (1). The CVO graded rounds 80 to 85. Two criteria FAILED: CB82cd1-AC3 (273 of 300 none rows carried no reason; repaired by rounds 84 and 85) and CB83ce1-AC3 (the salt lost, so the tokens could not be re-derived; repaired by round 85's one key space); the others read PASS to this seat's knowledge (round 85: CB85cg1-AC3 PASS, REMEDIATION_v51). Defects of mine, in the rows or the messages: the status-flip wording (W158-S4, W160-S2), the AC1 pytest command that could not collect (W166-S1, AMENDMENT 1), the missing month_grades read grant (W165-S2, AMENDMENT 1), the salted-token claim I made about the round-82 files (corrected in `ADVI_COTBKF_ROUND_82_DRAIN_END_20261013.md` and the CTO message of 20:48Z), my disarm row `D2-S134` whose premise was wrong, and the lost scripts above.

## Leftovers

- Worker branches: all 14 branches of rounds 80 to 85 (wk-ADVI_COTBKF-155 to -168) are merged and removed; one older branch `wk-ADVI_COTBKF-96` is UNMERGED (one commit, `fd47dde9c0`, row `D2-W96-S1`, absent from the base channel; its diff rewrites the channel file, so it was NOT merged). The CTO or the next COO decides: salvage the row or delete the branch.
- Outside the repository: `C:/dev/_cotbkf_active_set_20261013/` holds the round-82 pair, `REVERSE_MATCH_V2.csv` (round 84, superseded, not committed), and the V2/V3 files (committed copies exist). Empty directories `C:/dev/wk-cotbkf-161` and `C:/dev/wk-cotbkf-80` remain (device busy / left by earlier seats).
- This lane's cron `712bf657` (`/canonical-drive` 60m) is deleted at the stand-down; the inbox watcher dies with the session.
