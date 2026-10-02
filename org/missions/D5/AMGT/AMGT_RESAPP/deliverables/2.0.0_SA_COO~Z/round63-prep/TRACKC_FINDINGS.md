# AMGT_RESAPP track C -- timeline/day silver headline read (round 63, READ-ONLY)

Measured 2026-10-02 from this desktop (Windows, Python 3.14.7, pyarrow 24.0.0, boto3 1.43.46), fresh
process per mode, PYTHONPATH = repo root, read-only S3 GET/LIST on `opal-data-harvest`. Nothing was
written to the repo or S3; the deployed Lambda was not invoked. Raw outputs are the `*.json` files beside
this note; the scripts are `a_` .. `h_*.py`.

CAVEAT ON EVERY LOCAL TIME: this desktop's link to us-east-1 is BANDWIDTH-BOUND (single-stream GET
7.51 MB/s; 140 MB in 21.8 s = 6.4 MB/s aggregate; 64 workers gave no gain). Lambda's in-region regime is
NOT measured here. Byte counts, object counts and parity are plane-independent; wall times are local.

## 1. The code path (file:line at HEAD)

- `lib/research/api/scoped_amgt.py:4820` handler start stamps `_HANDLER_STARTED`.
- `scoped_amgt.py:4740-4763` `_timeline_article_loader`: filters the newest `article_security_mention`
  gold snapshot (`_timeline_snapshot_rows`, :4674-4684 -> `publication_gold._latest_gold_snapshot_rows_cached`)
  to security+UTC day, then `_timeline_silver_within_deadline` (:4725-4737, deadline 18.0 s at :4710, one
  persistent worker :4719-4722) -> `_timeline_silver_articles` (:4695-4702) -> `publication_gold._latest_articles_for_keys`.
- `lib/research/harvest/publication_gold.py:986-1023` `_latest_articles_for_keys`:
  1. `_silver_sources_for` (:973-983): publishers = the `<code>:` prefixes of the wanted keys.
  2. LIST, one paginated `list_objects_v2` per publisher on `<source>/harvest/silver/article/`
     (`_list_parquet_objects` :933-941; prefix from `store.table_prefix` store.py:168-172). No date
     or key narrowing: EVERY part of the publisher is listed.
  3. GET every listed part not already in `_SILVER_PART_CACHE` (:929; key (key, ETag, size)), WHOLE
     OBJECT (`_read_silver_part_projection` :963-970): `read_schema` then `read_table(columns=4)` --
     the footer is parsed twice, and column projection saves decode only, never bytes.
     Columns: `article_key, fetched_at, title, published_precision` (:926). No row-group/predicate pushdown.
  4. Concurrency: a 10-thread pool (:927, :997) on `store._default_client()` (store.py:179-181, boto3
     default pool of 10 connections).
  5. Filter: per publisher, parts in listing order, newest-wins by `store.supersedes` (store.py:363-370).
  6. Cache: per process only (`_SILVER_PART_CACHE`, `_GOLD_SNAPSHOT_CACHE` :929-930); a recycle drops it.
- Silver layout (producer `store.silver_append`, store.py:423-476): one `part-<run_stamp>.parquet` per run
  per `date=<fetched_at.date()>` partition (:446-449, :463). Write-once. Partitioned by FETCH date, not
  publication date, not key. 1 row group per part (all 19 sampled parts).
- Gold that exists (`amgt/harvest/gold/`, 11 table prefixes): `article_security_mention` carries NO title
  (`GOLD_MENTION_SCHEMA` publication_gold.py:64-89; `mention_rows` :292-317), but DOES carry each
  article's `fetched_at`, `bronze_key` and `record_hash`. `chatter_event` carries `lead_headline` for the
  lead article only. No gold table carries a headline per article.
- Bronze IS per-article (`.../bronze/article/article_hash=<sha256(article_key)>/<stamp>.json`) and the gold
  row's `bronze_key` points at it, but the title there is vendor JSON that needs the per-publisher silver
  transform (`lib/opal_data_harvest/silver_from_bronze.py`), so it is not a fit.
- The served body is whitelisted (`timeline_api.py:125-128` ARTICLE_FIELDS, `_serve_article_row`
  :143-155): an extra column on a gold row does not reach the JSON.

## 2. BA_US_Equity, 2026-09-08 -- the route's own keys

Gold snapshot `amgt/harvest/gold/article_security_mention/date=2026-10-02/part-20261002T061326Z.parquet`
(14,375 rows, 5,715 distinct article keys). Keys for BA 9/8 = 5, all distinct, across 3 publishers:
`barrons:WP-BAR-0001904706, barrons:WP-BAR-0001904458, bbg:TL11A6T9NJLS00, sa:4640843, sa:4640845`.

Cold UNMODIFIED call (`a_cold_unmodified.json`): `_latest_articles_for_keys` 20.52 s; same-process warm
re-call 0.505 s (LIST only); 5/5 rows returned; 1,884 parts cached.

Phase split, instrumented replica, cold, 10 workers (`c_phases_current.json`; parity with the unmodified
call TRUE):

| phase | wall | thread-summed (10 workers) |
|---|---|---|
| LIST (3 prefixes, 4 pages, 1,884 objects) | 0.62 s | -- |
| fetch phase (GET + decode, pooled) | 21.78 s | -- |
|   S3 GET incl. body read | -- | 197.9 s (time-to-first-byte 162.6 s); median 87 ms/GET, p90 160 ms |
|   `read_schema` (footer parse #1) | -- | 4.1 s |
|   projected `read_table` (footer #2 + decode) | -- | 8.9 s |
|   `to_pylist` | -- | 0.4 s |
| filter (newest-wins over 8,080 rows) | 0.002 s | -- |
| total | 22.41 s | -- |

GET is 94% of worker time, decode 6%, filter ~0. Locally the GET time is the link's bandwidth (see caveat).

## 3. Bytes read vs bytes needed

- Read: 1,884 objects, 139,991,714 bytes (barrons 48 / bbg 624 / sa 1,212 parts), 8,080 rows decoded.
- Needed: 5 rows; their key+title+precision+timestamp = 482 bytes = 3.4e-6 of the bytes read.
- Inside a part, the 4 needed columns are 0.17%-4.2% of column-chunk bytes (19 sampled parts,
  `b_layout.json`); footers are 10.8-122.5 KB per part (22-101 columns per schema), which is 40-70% of a
  small part. A footer+column ranged read (`c_phases_ranged.json`) still read 97.95 MB in 2,692 requests
  (-30% bytes, +43% requests); local wall 14.3 s.
- Partition skew: 2,052 of ~2,373 silver article parts sit in the `date=2026-10-01` fetch-date partition
  (bbg 588, sa 1,086, wsj 301, ft 77; a bulk re-harvest, inferred). 13,300 of 14,375 mention rows point into `date=2026-10-01`.

Can the rows be located without whole-publisher silver? YES, through the gold row itself, measured:
- `date=` partition == UTC date of `fetched_at`: 8,701 / 8,701 silver rows (all 5 publishers, 2,373 parts).
- gold mention `fetched_at` == newest silver `fetched_at`: 5,715 / 5,715 keys (0 stale, 0 absent).
- holding part's `run_stamp` within [-1 s, +1 s] of `fetched_at`: 5,394 / 5,715 keys (94.4%); 321 keys have
  a later stamp (+23 s up to +19 days: re-silvered bronze). 592 / 11,635 (security, day) groups hold at
  least one guaranteed window miss.
- 8,691 / 8,696 keys live in exactly one part; 5 in two.
- `record_hash` (store.py:330-334) covers every non-lineage field, title and published_precision included.
- Partition pruning ALONE does not generalise: over all 11,635 (security, day) groups the pruned read is
  p50 1,106 parts vs 1,212 today (`f_pointer_dist.json`). It only helps days fetched before 10-01 (BA 9/8:
  102 parts, 16 MB, 4.1 s local).

## 4. Options measured

A. PRODUCER: carry `title` + `published_precision` on every `article_security_mention` row
   (`GOLD_MENTION_SCHEMA` publication_gold.py:64-89 +2 fields; `mention_rows` :292-317 +2 keys;
   `build_mention` already holds the silver row, so no added producer read). Route
   (`scoped_amgt.py:4755-4761`) reads the headline off `mine`; it keeps the silver path only for a snapshot
   without the column. Size ~15 lines + tests. Measured in memory: snapshot 1,278,356 -> 1,531,803 bytes
   (+20%), decode 0.53 -> 0.44 s local, 5,715/5,715 titles non-null, precision values {instant}. The cold
   route then makes ZERO silver reads; it already reads this snapshot. MOVES SERVED OUTPUT: a gold rebuild,
   and the headline becomes "silver as of the gold build" instead of "silver at request time" (measured
   delta today 0/5,715). Needs a never-widen pair, the producer lane (AMGT_HARVST owns publication_gold.py
   and GOLD_MENTION_SCHEMA), and 2 deploys (freeze).

B. ROUTE-ONLY pointer read: for each key use the gold row's (`fetched_at`, `record_hash`): read the
   `date=` partition's parts stamped within +-2 s; fall back to that partition's later parts on a miss;
   ALWAYS also read every part with LastModified >= the snapshot's build stamp (newest-wins guard);
   apply `store.supersedes`. Simulated cold (`h_option_b.json`): parity with the unmodified reader 29/29
   groups (BA 9/8, 20 seeded-random, 3 largest, 5 guaranteed window misses); local wall median 1.67 s;
   BA 9/8 66 parts / 15.3 MB / 2.28 s; window-miss groups 3.8-5.2 s (134-308 fallback parts). One run hit
   a 21.4 s LIST stall (23.0 s wall), cause not established. Size ~60-70 lines in publication_gold.py + ~5 in
   scoped_amgt.py + a parity test. Served output UNCHANGED by construction (DELTA 0) -> no never-widen pair;
   one Lambda deploy (freeze). Tail: the after-build set grows until the next gold build (builds/day: 1, 1,
   1, then none 09-25..09-28, then 3, 2, 4, 1), and window-miss keys can fall back onto a 1,000+-part partition.

C. MECHANICAL: workers 10 -> 32-64 with botocore `max_pool_connections` (publication_gold.py:927, :995),
   parse the footer once (:968-970), optionally footer+column ranged GETs. ~5-40 lines, served output
   unchanged. Local: 64 workers 22.0 s (no gain, bandwidth-bound), ranged 14.3 s. Lambda effect UNMEASURED
   (inferred: helps only if Lambda is latency-bound). Cost stays linear in total silver parts.

## 5. Recommendation

A. It is the smallest change that removes the silver read from the request entirely (O(1), no cache, no
deadline race), and the producer already holds the title at build time. Its cost is governance (producer
lane, never-widen pair, rebuild, deploy under the freeze), not code. If the producer change cannot land
this round, B is the route-only stopgap with measured parity and no served-output move.
