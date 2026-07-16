# WP2 evidence — orion positions silver backfill 07-11..15 (P0 parity, Andrew-direct)

**archetype:** CENSUS
**author:** 0.4.0_DS_ClientPlatform~B · 2026-07-16 ~07:0xZ · leg: WP2 silver half (paired with 0.7.0's bronze backfill)
**Bar (Andrew verbatim, via CTO 050304Z):** "at least July 14 if not July 15 in every single bronze and silver bucket at parity."

## The vehicle

`data/inf/scripts/silver/convert_orion_api_to_silver.py --dim positions_mv --snapshot-date {d} --upload`,
one dated invocation per day (events do not retro-fire on backfilled keys — the planned-for path, not a
discovery). Converter = the chain's own INF_API_SILVER_POSITIONS_MV step, canonical vintage; reads
`bronze/positions/{d}.jsonl.gz` (LEG-2 .jsonl.gz world — the split-brain guard at
`convert_orion_api_to_silver.py:853+` was satisfied, not exercised). Rule 17 clean by construction (the
chain's own passthrough builder; no new judgment introduced).

**Chain-safety (measured before running):** this script writes NO `silver/_silver_complete/` markers
(zero references; markers are the Lambda parquet leg's, `inf-api-positions/lambda_function.py:94`) — so
these runs could not fire `inf-silver-aggregator`, which is a CHAIN LAUNCHER (invokes `inf-gold-trigger`
`{mode:full}`). Chokepoint held v1.7.92 as the independent second layer. `bronze/` has zero S3 event
subscribers (get-bucket-notification-configuration, denominator = the whole config: 2 subscribers, neither
on bronze/).

## The census (denominator: 5 dates = the hole 2026-07-11..15)

| date | bronze in (0.7.0, true-UTC) | conversion | silver served (head-object, size @ LastModified) | mv_sum (discriminator) |
|---|---|---|---|---|
| 07-11 Sat | 06:5xZ, 2,178,581-2,187,902 B range | 34,839 rows | 1,103,494 B @ 07:02:23Z | 202,843,645.67 |
| 07-12 Sun | " | 34,839 rows | 1,104,493 B @ 07:02:46Z | 202,843,645.67 |
| 07-13 Mon | " | 34,839 rows | 1,106,039 B @ 07:02:49Z | 201,601,607.47 |
| 07-14 Tue | " | 34,839 rows | 1,108,502 B @ 07:02:53Z | 202,375,854.79 |
| 07-15 Wed | " | 34,839 rows | 1,108,780 B @ 07:02:56Z | 202,818,860.22 |

**5/5 served.** Edges bracket-verified: 07-10 present (1,182,473 B @ 07-10 13:52:58Z, the pre-outage
original) and 07-16 present (1,112,093 B @ 07-16 03:03:54Z, the release window's run-7 chain step) —
**positions_mv is CONTINUOUS 07-10..07-16.**

## The discriminator (why identical row counts are HEALTHY here, with the check that could have failed)

All 5 dates converted to exactly 34,839 rows / 936 accounts — a count that cannot fail is not a check, so
the per-date `current_value` sums were measured as the discriminating instrument: 07-11 == 07-12 **to the
cent** (Sat/Sun carrying Friday 07-10's close — the T-1 weekend shape, NEVER#1), then three DISTINCT sums
for the three trading days. Same stable book, moving prices = **true vendor vintage confirmed at the data
level**, not just at the key level. The failure this was built to catch (vendor returning today's snapshot
five times) would have shown five identical sums; it did not.

## Scope residue (named, not resolved here)

- txn/perf needed NO dated pull: run-7's `--since` default (pull_date-7) + TRAILING_DAYS=30 covered the
  hole's DATA inside the 2026-07-16 partitions; 0.7.0's window-coverage manifests at
  `bronze/{transactions,performance}/_meta/` are the evidence. Per-date KEY-parity for txn/perf 07-11..14
  is therefore not present by design — flagged to CTO with the data-parity vs key-parity distinction; the
  census re-run (CTO's acceptance instrument) adjudicates against Andrew's bar.
- WP1 (eclipse) remains open, paired on 0.7.0's producer-revive.
