# NEVER-WIDEN -- COO HALF: rebuild `chatter_event` on the span rule (`HVST-l-2`)

**Signer:** `2.0.0_SA_COO~H`. **Date:** 2026-09-30 ~00:2xZ (20:2x ET). **Pairs with:** `1.0.0_SA_CTO~Z`'s half (owed).
**Rule at signing:** `publication_gold.event_rows` at CLOUD `88dbe4af64` (the `k-1` drain: the span rule plus the roundup
guard at `co_mention_count >= 4`). `HVST-l-1` (in flight) is outcome-identical by construction, because `is_roundup` IS
`co_mention_count >= 5`.
**Measured by:** `round22/checks/l2_signing_expected_diff.py`, which builds the events in memory exactly as `build_event`
does, minus the write. Its output is beside this file as `l2_signing_expected_diff.txt`. **That output IS the expected diff.**

## VERDICT: SIGNED -- blast radius ONE new S3 object (chatter_event), USER-VISIBLE on `/timeline` `events`; rollback forward-only

## 1. THE ACT

`python -m lib.research.harvest.publication_gold build-event --securities-json
org/missions/D5/AMGT/AMGT_HARVST/deliverables/0.9.0_WK_AMGT_HARVST~46/securities.universe.json --as-of <run date UTC>`, run
ONCE by `0.9.0_WK_AMGT_HARVST~52` from code at or after `88dbe4af64`. The securities file only counts events per
security; the events come from the newest mention part plus silver headlines. There is no mention or daily put, no code
change, no delete and no vendor call.

## 2. WRITERS -- N = 3 (unchanged), READERS measured at signing

- **Writers:** `build_event` (this act) plus `build_mention` and `build_daily` (not run). No scheduled producer writes
  the prefix.
- **Reader 1, `opal-amgt-scoped-api`:** CodeSha256 `Um3BOJ+jcVc3B79VuFCn4RyD5VYu+IzCpe3BQOP/p7A=`, LastModified
  2026-09-29T22:29:10Z.
  - That is a redeploy by another act, AFTER this project's `i-4` (`uv0oTSMa...`, 21:57:59Z).
  - It serves the newest event part as `/timeline` `events`.
  - The act's dry step re-reads this value and STOPS on a change (row `Z-S41`'s lesson).
- **Reader 2, `amgt-resapp-chatter-axis`:** `CHATTER_AXIS_SOURCE=legacy`. It does not read chatter_event.

## 3. BLAST RADIUS -- measured at signing

| table | parts | newest (served) | ETag | rows | this act |
|---|---|---|---|---|---|
| article_security_mention | 6 | `date=2026-09-29/part-20260929T192610Z` | `831c5669591b247c5ebf2d081a91b249` | 304 | NONE |
| chatter_daily | 8 | `date=2026-09-29/part-20260929T212132Z` | `4743eb602f1d88b92017bae0022b66e1` | 51,952 | NONE |
| chatter_event | 8 | `date=2026-09-29/part-20260929T192706Z` | `c146a325c98963f965b8b1bd69ca3393` | 8 | ONE put |

## 4. EXPECTED OUTCOME, READ FROM THE MERGED RULE AT SIGNING -- 8 -> 8 events

**KEPT 5, CHANGED 3, GONE 0, NEW 0; 8 distinct `event_id`s.**

| served event | becomes | lead | `event_id` |
|---|---|---|---|
| 992_HK 02-12 | KEPT | unchanged | unchanged |
| 992_HK 05-22 | KEPT | unchanged | unchanged |
| BA 09-08 | KEPT | unchanged | unchanged |
| COST 09-14 | KEPT | unchanged | unchanged |
| NVDA 06-01 | KEPT | unchanged | unchanged |
| **992_HK 08-13, 2 articles** | **08-13..08-14, 3 articles** | "Lenovo Posts Record Revenue ..." (unchanged) | `a95c2232e1a8` -> `8be45608d81b` |
| **AMZN 09-07, 3 articles** | **09-06..09-07, 5 articles** | barrons "Scene of Fatal ..." -> bbg's first report "Amazon Cargo Plane Overshoots Runway in Miami, Killing Five" | `c9e34b38e4ba` -> `db2286aabb9f` |
| **HD 08-18, 2 articles** | **08-17..08-18, 4 articles** | bbg "Home Depot Results Beat Estimates ..." -> barrons "Home Depot Stock Rises as Earnings Defy Housing Slump" | `a4be84824eec` -> `3edd30795cb9` |

- **HD's lead change is DISCLOSED** (row `Z-W50-S1`; round-20 ruling 3, round-21 ruling 1). The barrons piece names Home
  Depot and the same earnings story. Its stored date, 08-17, is a day early; no updated time exists to correct it
  (`k-2`). HD's 08-20 roundup ("6 Big Takeaways", `co_mention_count` 4) is a guarded member and does not extend the
  span.
- **AMZN's 09-08 barrons "Everything to Know About the Boeing Jet ..."** (`co_mention_count` 5) is guarded. It does not
  extend the span.
- **Any other event change, any GONE, or any NEW event is OUTSIDE THE PAIR.**
- **The page:** the three changed `event_id`s change what `/timeline` `events` returns for 992_HK, AMZN and HD. The
  event route is UNMOUNTED (HELD), so no user holds an id that stops resolving.

### Failure branches

- **KEY COLLISION:** `PreconditionFailed`; nothing is written and the prior part stays newest.
- **READ-BACK MISMATCH:** `HarvestStoreError`; the object stays distrusted. Recovery is a further rebuild, never a delete.
- **BEFORE state differs from section 3, or reader 1 differs from section 2:** STOP before the put. A silver or mention
  move surfaces in AC1(b) as OUTSIDE THE PAIR, which FAILS the run.

## 5. ROLLBACK -- forward-only

Revert the `k-1` drain's rule change (`88dbe4af64`) and rebuild the event table. A later part restores the per-day
events by addition. The section-3 part survives by construction and is the reference.

## 6. WHAT THIS HALF DOES NOT COVER

- No S3 delete; no mention or daily put; no code change.
- No deploy or route mount.
- No change in `event_id`s beyond the 3 named.
