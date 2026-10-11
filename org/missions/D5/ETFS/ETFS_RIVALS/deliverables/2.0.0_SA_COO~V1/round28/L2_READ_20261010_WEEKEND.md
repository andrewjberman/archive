# ETFS_RIVALS round 28 -- the issuer's read of 2026-10-10 (a Saturday) and what it moves

Author 2.0.0_SA_COO~V1, 2026-10-11 ~05:0xZ, dell1. Nothing here grades; the grades are the CVO's. Every figure below
was read this tick; the source is on the line.

## Measured

| # | fact | source (read 2026-10-11 ~05:0xZ) |
|---|---|---|
| 1 | `etfs-rivalfunds-daily` is `cron(0 7 ? * MON-FRI *)` and `etfs-rivalfunds-sweep-daily` is `cron(0 9 ? * MON-FRI *)`, both America/New_York, ENABLED. Neither fires on a Saturday or a Sunday | `aws scheduler get-schedule` on each name |
| 2 | `l2_read.py 2026-10-10`: 13:00Z sweep window 12:55-13:45 has NO REPORT LINE on all 5 functions; the daily and fetch-holdings Lambdas have none in the 11:00Z window either; 0 corporate_actions objects; 0 `dramatic_move:` lines | `round28/l2_read.py 2026-10-10`, rc 0 |
| 3 | `rivalfunds/etfs/platinum/page/` holds date prefixes through `2026-10-09`; there is no `date=2026-10-10`, so `sweep_read.py` raises NoSuchKey (an absent page day, not a read failure) | S3 list, bucket opal-data-etfs |
| 4 | Silver, canonical-shape and publish-page each have a REPORT line in 10:55-11:40Z on 2026-10-10 (publish-page 144.4 s, 1,026 MB, 0 blocking findings over 5 functions) | `report_lines.py` section 1a |
| 5 | The marker `state/fetch_bloomberg/date=2026-10-09/batch-20261010T110700Z.json` was written 2026-10-10 11:07:29Z (290 bytes). The silver rule fires on an Object Created under exactly that prefix | S3 list; `aws events describe-rule rivalfunds-build-silver-bloomberg-on-marker-created` |
| 6 | The vehicle's collector leg writes that marker only on a landed batch (`scheduled_daily_pull.cmd:443`, exit 90). So the 2026-10-10 11:00Z vehicle fired and its collector leg landed | fact 5 with the .cmd line |
| 7 | `round-close-check --round 28` REFUSED: 4 of 9 J1 graded. The CVO's v1 file names `split-adjusted-series` in full and names none of the other four slugs (0 lines each), though its header says wc-1 MET, wc-2 MET | `grep -c` per slug on `ADJUDICATION_v1.dell1.md`; `round-close-check.py:383-410` matches the order id in the row text |

## What it moves

- **wi-1 and every J1 that needs the sweep or the daily Lambda cannot be read before Monday 2026-10-12 13:00Z (09:00 ET).**
  The 2026-10-10 "13:00Z sweep" the round's earlier text named did not exist by schedule (fact 1). Not a failure.
- **tc-1 J1 is gated only on the transcription** of `bbg_tplus1_20261010_*.log`. The collector leg landed (fact 6); whether
  the enrichment leg REACHED its step is exactly what the transcription shows (`tw1_j1_read.py`). Owed via relay order
  AMENDMENT 7 @9e6b96a315; no site-Z seat is live (get_live_agents 05:0xZ).
- **The page the Saturday chain touched is 2026-10-09** (fact 3 and 5), so the next `l2_read.py` page day with both a chain
  and a sweep is `2026-10-12` (windows 10:55-11:40Z and 12:55-13:45Z that Monday), read after 13:45Z.
- **wc-1 and wc-2 read UNGRADED by the checker, not by the CVO** (fact 7): the header grades both MET, no row names the
  order id. The remedy is the CVO's addendum row naming the two ids in full; the grade is the CVO's, not this seat's.
  wd-1 is a different case: the CVO HELD it (ADDENDUM 1, first page rendered with RIV-wf-1), so UNGRADED is correct.

## Not measured

- Whether the transcription's enrichment leg printed `RIVALFUNDS ENRICHMENT STEP` and an exit code other than 97.
- Whether a Terminal user was signed in at 07:00 ET on 2026-10-11 (Sunday) for the next owed date.

## Addendum 2026-10-11 ~06:0xZ -- why the Saturday enrichment leg exited 97 (measured)

| # | fact | source |
|---|---|---|
| 8 | Log line 177 reads `{"status": "SKIPPED", ..., "detail": "no non-cash securities in G1 canonical_shape at date=2026-10-09"}`; the leg exit 3 maps to 97. The collector leg before it was `status OK`, batch landed, exit 90 | `VEHICLE_LOG_20261010_1100Z.enrich.txt` at origin/box/sitez (lines 170-178 copied by ~ZV) |
| 9 | G1 `canonical_shape` for date D is first written at D+1 11:01Z, on a weekday (date=2026-10-08 first 2026-10-09 11:01:27Z; 10-07 first 10-08 11:01:24Z; 10-06 first 10-07 11:01:26Z), then rewritten ~11:08Z by the chain after the collector marker. date=2026-10-09 has 1 object, first and last 2026-10-10 11:08:26Z | S3 list, `rivalfunds/etfs/gold/canonical_shape/`, bucket opal-data-etfs |
| 10 | The daily Lambda that writes the 11:01Z object is `cron(0 7 ? * MON-FRI *)` (fact 1). On Saturday it did not fire, so no G1 for date=2026-10-09 existed at the enrichment leg's 11:07:25Z; the chain wrote it at 11:08:26Z, one minute after | facts 8, 9 and 1 |

What it moves: the 2026-10-10 run could not reach a write by construction (a weekend, with the previous trading day's G1
built only by the next weekday's Lambda). G1 for date=2026-10-09 now exists (fact 9), so the 2026-10-11 and 2026-10-12 runs,
whose default date is also 2026-10-09 (`enrichment_bloomberg.py:1259-1261`), find securities. INFERRED, not measured: that
they then run the market pull; the transcription of each date shows it. The grade stays the CVO's (ADDENDUM 8 @1e4c6bd6f2 holds
tc-1 J1 NOT MEASURED).
