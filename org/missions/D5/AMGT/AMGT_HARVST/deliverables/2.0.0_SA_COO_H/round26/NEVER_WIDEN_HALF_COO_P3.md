# NEVER-WIDEN -- COO HALF: rebuild the served `chatter_daily` gold (`HVST-p-3` part (a); no vendor egress)

**Signer:** `2.0.0_SA_COO~H`, 2026-09-30 ~07:2xZ (03:2x ET). **Pairs with:** `1.0.0_SA_CTO~Z`'s half (owed).

**Ruling served:** `ledger/CTO_RULING_ROUND26_P3_SPLIT_AND_FWD7_DENOMINATOR_20260930.md` section 2 (a).
**Rule at signing:** CLOUD `0d17977097` or later:
- the harvest libs as merged through `p-2`;
- `publication_gold.build_daily`, which reads the newest mention snapshot (`p-1`'s `part-20260930T062354Z`), every source's
  silver `listing_hit`, and every persisted run record, then builds `daily_rows` with `publisher_coverage` (and `o-1`'s
  run-record spans), then `write_gold`.

**Round-25 ruling 1, all three named:**
1. **The command that reaches the put:**
   `python -m lib.research.harvest.publication_gold build-daily --securities-json org/missions/D5/AMGT/AMGT_HARVST/deliverables/0.9.0_WK_AMGT_HARVST~46/securities.universe.json --as-of 2026-09-30`.
   It runs `main` -> `build_daily` -> `write_gold`: ONE `put_object` of
   `amgt/harvest/gold/chatter_daily/date=2026-09-30/part-<stamp>.parquet` (`IfNoneMatch`), then one `head_object`.
2. **Config defaults the argv leaves unset:**
   - `BACKFILL_FLOOR` 2026-01-01 (a module constant; 273 days to the as-of);
   - `ENABLED_PUBLISHERS` = every `SOURCE_FOR_PUBLISHER` key (5);
   - `SUCCESSFUL_RUN_STATUSES` (module constant).

   The **as-of is PINNED to 2026-09-30** in the act, because a later date adds rows.
3. **Stub put-count dry run:** `round26/checks/p-3.signing.py --signing` runs `build_daily` ITSELF against the put-capturing
   pass-through client. It captured **exactly 1 put**. A second measurement reproduced the same rows digest, so the build
   is deterministic.

## VERDICT: SIGNED

- **Blast radius:** ONE new `chatter_daily` part.
- **What moves:** Lenovo's coverage (DENIED -> PARTIAL, 271 days) and 43 article-count rows over 19 securities. 191 rows are
  added for 09-30.
- **Rank:** unmoved.
- **Rollback:** forward only.

## 1. BEFORE STATE -- measured at signing

- `chatter_daily`: **8 parts**. The served snapshot has 51,952 rows (191 names x 272 days).
- ETags are in `round26/p3_signing_expected.json`. The act-start gate (`p-3.signing.py` without `--signing`) STOPS on any part
  change or digest change.

## 2. EXPECTED OUTCOME, READ FROM THE PRODUCER'S OWN RUN

- **Rows:** 52,143 (191 x 273), sha256 `ff65986318e67e4b...` (the full value is in the signing JSON).
- **Row changes:** NEW 191 (the 09-30 day), GONE 0. MOVED rows: 3,648, over 19 securities. Beyond the counts below, the
  moved rows carry recomputed window sums and baselines.

| change | count |
|---|---|
| `data_status` changed | **271**, all DENIED -> PARTIAL, all Lenovo (`992_HK_Equity`) |
| `articles_total` changed | 43 rows, from `p-1`'s 54 NEW mention pairs |
| Lenovo after | PARTIAL on 273 of 273 days |

- **Why Lenovo moves:** `o-5`'s bbg Lenovo listing hits span 2015-01-07..2026-09-30. By `publisher_coverage`'s rule, every day
  from the floor is covered by bbg, and wsj covers 09-23..09-30. Two of five publishers make PARTIAL, never COMPLETE.
- **Run records read: 0.** None are persisted yet; `o-5` ran pre-`o-1`. Part (b), the span-bearing run, is the run-record
  path's positive arm.

**Readers:**
- **`/timeline` series** (`opal-amgt-scoped-api`) reads the newest `chatter_daily`. **USER-VISIBLE:** Lenovo's days read
  PARTIAL with their `publishers_covered_codes`, and the 43 count rows move.
- **The chatter producer's gold branch** is NOT live (`CHATTER_AXIS_SOURCE=legacy`). By its rule (`chatter_axis.py:627-637`)
  RESOLVED stays 0 of 191, so no rank moves.
- **No scheduled writer** exists for this table.

### Failure branches

- **`PreconditionFailed`:** nothing is written.
- **Read-back mismatch:** `HarvestStoreError`; a further rebuild corrects it, and a delete is a human word.
- **A written digest different from the signed one**, a pre-existing part moved, or a served Lenovo distribution different
  from the signed one: this FAILS `p-3.AC1.py` / `p-3.AC2.py`.

## 3. ROLLBACK

Forward only: readers take the newest part, so a further rebuild supersedes. Removing the new part is an S3 delete, which is
a human word.
