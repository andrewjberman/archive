# AMGT-au-6 -- where the Lead Panel's time goes, before and after (worker 0.9.0_WK_AMGT_RESAPP~236)

Instrument: `profile9.py` (cProfile + a wrapper on botocore's `_make_api_call`) and `profile_table.py` (one FRESH process per route: one cold call, one warm call, boto calls by operation). Both run the LOCAL handler against the live stores from this device, so absolute ms are network-latency-bound (about 150-250 ms per boto call here); the CALL COUNTS are the device-neutral figure. BEFORE = a `git archive` of the issuance commit; AFTER = this worktree.

## 1. Per-phase table, BEFORE (cProfile, one cold call each; "in boto" = time inside botocore calls, the rest of the wall is Python)

| route | wall | etf-classifications GetItem (serial, one per ranked row) | model-block header ListObjectsV2 + GetObject (one pair per unnamed name) | crosswalk, pointers, Query | decode + compute in Python |
|---|---|---|---|---|---|
| rankings/trending/price (default) | 26.1 s | 94 calls, 16.6 s | 23-27 lists 8.7 s + 25 GETs 3.2 s | 5 pointer GetItems 0.4-4.8 s, 2 Query 0.6 s | under 0.6 s (25.5 s of 26.1 s is inside botocore) |
| timeseries/collected/chatter?days=30 | 52.3 s | 289 calls, 61.6 s summed over 8 threads | 57 lists 19.0 s + 52 GETs 6.0 s | 2 Query 0.7 s | 0.17 s own time in `read_monthly_chatter` |

Cause, in order of cost: (1) the classification table is read ONE GetItem PER RANKED NAME, serially in `_join_classification`, and the chatter route repeats that three times over (`_display_names`, `_classifications`, and the `TRENDING/PRICE` ranking it reads for `places_moved`); (2) every unnamed name costs a model-block S3 listing and GET (`_model_block_name`), again three times in the chatter route; (3) the generation pointer walk and the prior-generation read for `places_moved`; (4) a fresh `boto3.resource("dynamodb")` per call. NOTHING was cached across requests, so a warm call cost the same as a cold one (rows below: warm == cold). Decode and compute are not the cost.

## 2. The fix (all inside `lib/research/api/`; no store write, no new producer, no new S3/DynamoDB read path)

| change | rule | effect |
|---|---|---|
| `served_cache.py` (new) | version-keyed or TTL memo, deep-copied on read, a failed read is never stored | the holder for the four below |
| `read_generation_rows` | keyed on the generation partition (carries `generation_id`) AND the pointer's `row_count`; no expiry | a committed generation is read once per container |
| `read_generation_pointer` | TTL 60 s per (axis, date), a day with no pointer yet is held too | the backward walk is one pass per minute |
| `_classification_for_ticker` | TTL 300 s per bare ticker (per security for a trailing-slash root); READ_FAILED never held | 94-110 serial GetItems per request become 0 when warm |
| `_join_classification` | the distinct misses are read in parallel (8 workers), as `monthly_chatter._classifications` already did | cold: 94 serial reads become 8-wide |
| `_model_block_name` | TTL 300 s per security_key, only a completed read (SERVED or ABSENT) | 23-57 list+GET pairs per request become 0 when warm |
| `_dynamodb()` | one resource per container, built under a lock | removes a resource build per call and the concurrent-build race the new threads would meet |

Staleness bound, stated: a newly committed generation is visible within 60 s; an edit to a classification row or a model-block name within 300 s. A committed generation's rows can never be stale (the key carries its identity).

## 3. BEFORE / AFTER, per route (fresh process per route; calls = GetItem/ListObjectsV2/GetObject/Query)

BEFORE (issuance commit):

| route | cold ms | cold calls (Get/List/GetObj/Query) | warm ms | warm calls |
|---|---|---|---|---|
| lead-panel_timeseries_collected_chatter_days30 [200] | 52184 | 289/58/53/2 | 44209 | 289/57/49/2 |
| lead-panel_timeseries_collected_chatter_days90 [200] | 55605 | 289/58/53/2 | 63805 | 289/57/49/2 |
| lead-panel_timeseries_collected_chatter_days365 [200] | 29732 | 289/58/53/2 | 44359 | 289/57/49/2 |
| lead-panel_rankings_trending_price_default | 19428 | 99/25/25/2 | 21093 | 99/24/24/2 |
| lead-panel_rankings_trending_price_days90 | 23365 | 109/25/25/1 | 59303 | 109/24/24/1 |
| lead-panel_rankings_trending_price_days365 | 62603 | 110/25/25/1 | 23391 | 110/24/24/1 |
| lead-panel_rankings_breakout_price_default | 19726 | 99/25/25/2 | 17081 | 99/24/24/2 |
| lead-panel_rankings_breakout_price_days90 | 18346 | 109/25/25/1 | 17924 | 109/24/24/1 |
| lead-panel_rankings_breakout_price_days365 | 19924 | 110/25/25/1 | 17465 | 110/24/24/1 |

(The three chatter rows above were re-measured after the first table run read 500 on the bare archive, which lacked `org/standards`; the six ranking rows are from the first run, all status 200.)

AFTER (this worktree):

| route | cold ms | cold calls (Get/List/GetObj/Query) | warm ms | warm calls |
|---|---|---|---|---|
| lead-panel_timeseries_collected_chatter_days30 | 18584 | 102/34/29/2 | 933 | 0/8/0/0 |
| lead-panel_timeseries_collected_chatter_days90 | 7841 | 102/34/29/2 | 969 | 0/8/0/0 |
| lead-panel_timeseries_collected_chatter_days365 | 9314 | 102/34/29/2 | 917 | 0/8/0/0 |
| lead-panel_rankings_trending_price_default | 5275 | 99/27/25/2 | 277 | 0/2/0/0 |
| lead-panel_rankings_trending_price_days90 | 6188 | 109/26/25/1 | 257 | 0/1/0/0 |
| lead-panel_rankings_trending_price_days365 | 29362 | 110/27/26/1 | 353 | 0/1/0/0 |
| lead-panel_rankings_breakout_price_default | 5512 | 99/27/25/2 | 307 | 0/2/0/0 |
| lead-panel_rankings_breakout_price_days90 | 5543 | 109/26/25/1 | 150 | 0/1/0/0 |
| lead-panel_rankings_breakout_price_days365 | 5092 | 110/27/26/1 | 146 | 0/1/0/0 |

Read the table by column: WARM is what a user sees after the container has served one Lead Panel read. WARM before 17-64 s (the "almost a minute" Andrew reported) against after 0.15-0.97 s; the residue is 1-8 S3 listings per request (the covered-universe listing, which is read fresh by its own contract, and the gold-snapshot listings that pick the newest object). COLD (first call of a fresh container) before 18-62 s against after 5-29 s locally: still network-bound at about 100 parallel classification GetItems and about 25 model-block reads; the cold-container remainder is the one row filed this cell (a stored per-name roster would remove it, and is a new producer, so it is not built here).

AC1 (the checker, bar 6000 ms, warm, local): see the proof instance; AC2: `after_equal.py` prints EQUAL 9 of 9.
