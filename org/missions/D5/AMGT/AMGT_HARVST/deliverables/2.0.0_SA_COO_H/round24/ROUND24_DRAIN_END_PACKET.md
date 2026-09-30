# AMGT_HARVST ROUND 24 -- DRAIN-END PACKET, `2.0.0_SA_COO~H`, 2026-09-30 ~03:1xZ

| field | value |
|---|---|
| Issuance | `b1a44a82b6`: six orders over `ROUND_ANALYSIS.round23.md` @`d1ec6f4118` (decomp section 36) |
| L8-L10 route | `3.0.0_SA_CVO~Z` |
| Class | LOCAL on every drained order. No served byte and no deployed resource moved this round. |
| WORLD order | `n-4` was WITHDRAWN before dispatch (CTO ruling 1 @`5998e71f23`) |

## 1. SIX ORDERS, ALL TERMINAL

| order | FWD | deliver | drained | status | instance |
|---|---|---|---|---|---|
| `HVST-n-1` collector keeps received bytes, listing link, rank/page, run record | 1, 3 | `374b79d7c9` | `729ef39440` | complete | VALID rc=0 |
| `HVST-n-2` sa silver fields, unlabelled sa rows, query by company | 2 | `70716b383b` | `c258c87826` | complete | VALID rc=0 |
| `HVST-n-3` why the served rank holds 2 rows; gold rank diff | 7 | `173732adb7` | `49bafe8df9` | complete | VALID rc=0 |
| `HVST-n-4` flip `CHATTER_AXIS_SOURCE` to gold (WORLD) | 7 | -- | -- | **withdrawn** (AMENDMENTS 1 `89480001b4`, 2 `78425f62a7`) | not dispatched |
| `HVST-n-5` 2026-01-01 backfill plan, all covered names | 9 | `59ed1ca52e` | `6e0499ca26` | complete | VALID rc=0 |
| `HVST-n-6` `/timeline/day` profile and read-path fix | carried from DSGN_AMGTV1 r7 ruling 2 | `a333e6c1f7` | `150b717373` | complete | VALID rc=0 |

**Close run.** Script: `round24/close_run_round24.py`. Output: `round24/close_run_round24.out.txt` and `round24/rerun/`. It
ran at trunk `78425f62a7` and re-ran all 12 criterion invocations; **12 of 12 returned rc 0**. The scripts rewrote three
tracked worker outputs, and all three were restored, so the committed record is the workers'.

| check | worker | close run | why they differ |
|---|---|---|---|
| `n-1` AC1 | 195 passed | 199 passed, 1 skipped | later drains added tests |
| `n-6` AC3 | 234 passed | 239 passed | later drains added tests |
| `n-6` AC2 cold ratio, minimum | 2.32x | 2.34x | timing variation |
| `n-6` AC2 warm ratio, minimum | 45.85x | 36.95x | timing variation; the direction and order of magnitude hold |

- Body sha256: OLD == NEW on 4 of 4 days, the same four hashes as the worker.
- `n-3` reproduced: the gold branch resolves 0 of 191 and fails with `INCOMPLETE_GOLD_INPUT`.
- `n-5` reproduced: 955 page figures, 3 MEASURED, all 191 names present.

## 2. WHAT THE ROUND MEASURED OR BUILT (the CTO grades; nothing here is a grade)

| FWD | this round |
|---|---|
| **1 / 3** | **Built, not served.** The collector now keeps the publisher's received bytes beside the rebuild, with `received-sha256`, and links each article to its listing object. It records rank and page for all five publishers and writes a run record. AC3: the 126 existing objects are unchanged. **The capture runs only on `--harvest-grammar`; the scheduled `run-local.ps1` does not pass it** (row `Z-W56-S2`). CTO ruling 2 puts the flag in the scheduled run as a round-25 cell under a pair. |
| **2** | **Built, not served.** `silver_from_bronze` keeps sa's `links`, `type` and `meta`: missing fields go from 5 to 0 on the as-received articles. The 6 unlabelled sa objects are `fullArticle`, and each now yields a row. `rows_by_company_mention` makes query-by-company the mention join: Lenovo is 32 by the join against 35 by `discovered_for`, and AES, Barrick and Atlantic Power fall out. In memory, 5 of 46 served silver rows would move and 6 would be appended (46 to 52). **The served rebuild is held:** `store.silver_latest` keeps only a strictly newer `fetched_at`, so the rebuilt rows would land unread. CTO ruling 3 adds the tie-break (the later `run_stamp` wins) as a round-25 LOCAL cell, followed by the paired rebuild. |
| **7** | The served rank holds 2 rows because **188 of 191 covered names have no legacy pool link** (step table by file:line in `n3_ac1`). The producer's own gold branch **fails**: RESOLVED is 0 of 191, gold `chatter_daily` reads `no_coverage` on 5,675 of 5,730 day-reads, and all 191 read DENIED on 09-29. So the flip was withdrawn. CTO ruling 1 keeps the guard; the round-25 cell writes gold coverage from run records, and the flip is re-cut once gold resolves a gradable pair. |
| **9** | **Plan only; nothing fetched.** The collector's own `plan` covers all 191 names, Lenovo first: 23,859 listing pages. 3 of 955 page figures are MEASURED (sa `totalPages`) and 952 are the config default of 25. The sa leg is WAITS-ON-RENEWAL. |
| **5 / 6 (page half)** | Not a round-24 cell. `1.0.0_SA_CTO~Z` states in the DSGN_AMGTV1 round-8 analysis (`2c63f69a09`, ruling 4, msg 26871) that walk G met FWD-5 and FWD-6's page half, and it grades them whole in this round's HARVST analysis. |
| **`/timeline/day`** | Reading silver dominated 9 of 9 reps, at about 5.3 s deployed per day with articles. The new path reads only the publishers the keys name, 4 columns at a time, concurrently, with a cache keyed by ETag. The body is byte-equal. Locally, the minimum speedup is 2.3x cold and 37-46x warm. **Not served:** users see it only after a scoped-API redeploy under a never-widen pair, which is a follow-on WORLD seat order. |

## 3. ROWS THIS ROUND

| row | state | what it records |
|---|---|---|
| `Z-W56-S2` | ARMED | Capture runs only on `--harvest-grammar`. Ruled by CTO ruling 2 (round-25 cell). |
| `Z-W58-S1` | ARMED, disarmed by the `n-4` hold and withdrawal | The gold branch fails. |
| `Z-W59-S1`, `-S2` | INERT | The planner takes no listing size; 190 of 191 names have no `sa_symbol`. |
| `Z-W60-S1`, `-S2` | INERT | The named 992_HK day has 0 articles; the local cold ratio understates the in-region gain. |

## 4. CARRIED INTO ROUND 25 (by the CTO's rulings; not cut here)

1. Write gold `chatter_daily` coverage from run records (ruling 1).
2. Add `--harvest-grammar` to the scheduled run, under a pair (ruling 2).
3. The `silver_latest` tie-break (LOCAL), then the paired served silver rebuild (ruling 3).
4. The `/timeline/day` redeploy, a WORLD seat order under a pair.

## 5. FOR L9

All criteria this round are mechanical, so there is nothing to adjudicate at L9. The FWD grades are the CTO's at L10.

**Disposable worktrees:** `wk-hvst-r24-56` through `-60`. The branches are kept; removal waits on Andrew's go.
