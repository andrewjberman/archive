# The 480 s returns-stage dry run: what the Lambda's own REPORT lines say (IRPT_DASHBD F-SHIP, 2.0.0_SA_COO~F2, 2026-10-17 ~02:0xZ)

**Question (CTO msg 10141):** IB2's condition-4 dry run (`accounts: population`, one backfill day, stages returns, class, lots) took 480.1 s and peaked at 4,384 MB; the last scheduled fire took 298 s. Why?

**Instrument:** `filter-log-events` on `/aws/lambda/irpt-49f-reporting-gold-lambda`, pattern `REPORT RequestId`, the last 8 days, read-only (script `scratchpad/reports49f.py`; 25 REPORT lines; the denominator is every REPORT line the group holds in the window, no page cut).

## What it reads

| class | invocations (UTC) | duration | peak memory |
|---|---|---|---|
| Scheduled daily fires, 10-12 to 10-16 (11:46Z, plus 11:45Z on 10-13) | 10-12, 10-13, 10-14, 10-15, 10-16 | 217 to 318 s (10-16: 298 s) | 1,385 to 1,607 MB (10-16: 1,455 MB) |
| Two earlier runs on 10-16 (13:59Z, 14:13Z), BEFORE the transaction wiring was applied | 2 | 194.5 s and 501.4 s | 5,565 and 5,827 MB |
| Today's apply runs (01:26 to 01:28Z): dry run, time-trigger, first write, range | 4 | 0.6 to 20.1 s | 255 to 379 MB |
| IB2's returns-stage dry run (01:38Z, the 480 s read) | 1 | 480.1 s | 4,384 MB |

## Reading

1. **The 480 s run is the population path, not the daily path.** Its profile (480 s, 4.4 GB) matches the 10-16 14:13Z run (501 s, 5.8 GB), which was taken BEFORE any transaction code was on the function. The daily fire's profile is about 300 s at about 1.4 GB. A population read of every account is a larger job than the fire's daily read, so 298 s is not the right yardstick for it.
2. **The transaction wiring is not the cause:** the transaction stage was not in the run's stage list (returns, class, lots), and the stage's own full-range run took 20 s.
3. **Monday's fire:** the daily path adds one transaction stage of about 1 s per day on top of about 300 s, so the expected fire is near 300 s at about 1.5 GB, far from the 720 s trigger. The first scheduled fire's REPORT line is the measurement that decides it.

## Not established

What payload the two 10-16 runs carried (the REPORT lines do not hold it; I infer `population` from the profile). Whether the daily fire's return stage and the population dry run read the same code path beyond that. The first fire with the transaction stage has not happened (Monday 2026-10-19, 11:41Z schedule).

-- 2.0.0_SA_COO~F2
