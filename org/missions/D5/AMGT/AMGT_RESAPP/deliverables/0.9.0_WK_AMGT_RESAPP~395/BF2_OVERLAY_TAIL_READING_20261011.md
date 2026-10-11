# AMGT-bf-2 -- overlay tail reading, `/aws/lambda/opal-amgt-scoped-api`, last 24 hours

Order: AMGT_RESAPP.TO-AMGT-bf-2.read-the-overlay-tail-over-20-seconds-over-a-day-of-real-traffic (round 99, decomposition s.107).
Worker: 0.9.0_WK_AMGT_RESAPP~395. Read only. The function was not invoked; no other AWS call was made.

## Window

WINDOW 2026-10-10T23:29:21Z to 2026-10-11T23:29:21Z (UTC, 24 h; the end was fixed at the moment the read started, 2026-10-11T23:29:21Z)
FUNCTION CodeSha256 mbGRmy1Hnh7M6Gtt9LchHPmt17lYS/oyCl6s10lJO+w= LastModified 2026-10-11T22:15:23.000+0000 (read at 2026-10-11T23:29:38Z, 17 s after the window end; Version $LATEST, State Active, LastUpdateStatus Successful, Timeout 29 s, MemorySize 1769 MB)

## Counts

- INVOCATIONS n=32528
- OVER 20 s n=53
- ATTRIBUTED n=0
- UNATTRIBUTED n=53
- COLD n=12
- POOL-FULL n=49
- NO POOL-FULL n=4

Over-20 s invocations are 53 of 32,528 (0.16%). The cut's probe read a different window (31,878 REPORT lines, 53 over 20 s, 202 cold); this window holds the same 53 over-20 s invocations.

Why, from the numbers: 49 of the 53 (92%) carry a "Connection pool is full" warning, 277 warning lines in all, median 6 per invocation. 12 of the 53 (23%) are cold starts, with init 612 to 713 ms, against 210 cold starts among all 32,528 invocations (0.6%). Median duration is 24.9 s (min 20.9 s, max 29.0 s); one of the 53 ended at the 29 s timeout (Status: timeout). Cold over-20 s runs have a median of 25.6 s, warm ones 24.0 s. The first pool-full warning is logged 19.9 to 25.9 s after START (median 22.4 s), and 2.5 to 4.0 s before the invocation ends (median 2.7 s); in 47 of the 49 it comes after 20 s from START. The 53 over-20 s invocations fall in 49 distinct minutes, which hold a median of 23 REPORT lines each (1 to 162): this is a count of invocations ending in the minute, not instantaneous concurrency. 47 of the 53 REPORT lines precede the function's LastModified (22:15:23Z); the earliest over-20 s is at 09:45:52Z.

What these numbers do NOT show: no line of any over-20 s invocation names a route or a security key, so which endpoint or name ran slow is unknown; the warnings show the connection pool full near the end of a run, not what filled it, and the order of events is not a cause; the duration is the function's own REPORT figure, not the client's latency, since the gateway and client sides were not read; the in-minute counts are REPORT completions, not concurrency; a single 24-hour window; nothing here links the slow runs to the redeploy, since 47 of them ran before the last LastModified.

## Routes

ROUTE none attributable | reason: none of the 436 log lines of the 53 over-20 s invocations contains `/api/scoped/amgt/`, `_Equity` or `route=`; the lines are START, END, REPORT and the pool-full WARNING only, so all 53 are UNATTRIBUTED. No route was inferred from duration or hour.

## Names

NAME none attributable | reason: the same 436 lines name no security key (`<TICKER>_<EXCH>_Equity`), so no name is attributed to any of the 53 invocations.

## Beside

Each MINUTE line counts the over-20 s invocations whose REPORT line (log-event time, equal to START plus the duration) falls in that UTC minute, and the REPORT count of that minute over the whole window (stats count(*) by bin(1m); minutes without a REPORT line are absent from that query, and all 49 minutes carry one).

MINUTE 2026-10-11 09:45 UTC | over20=1 | invocations=3
MINUTE 2026-10-11 10:57 UTC | over20=1 | invocations=2
MINUTE 2026-10-11 11:10 UTC | over20=1 | invocations=3
MINUTE 2026-10-11 12:05 UTC | over20=2 | invocations=8
MINUTE 2026-10-11 12:07 UTC | over20=1 | invocations=1
MINUTE 2026-10-11 12:09 UTC | over20=1 | invocations=10
MINUTE 2026-10-11 12:12 UTC | over20=1 | invocations=9
MINUTE 2026-10-11 12:43 UTC | over20=1 | invocations=21
MINUTE 2026-10-11 12:48 UTC | over20=1 | invocations=18
MINUTE 2026-10-11 12:49 UTC | over20=1 | invocations=36
MINUTE 2026-10-11 12:50 UTC | over20=1 | invocations=32
MINUTE 2026-10-11 13:22 UTC | over20=1 | invocations=9
MINUTE 2026-10-11 13:47 UTC | over20=1 | invocations=4
MINUTE 2026-10-11 13:48 UTC | over20=1 | invocations=15
MINUTE 2026-10-11 13:55 UTC | over20=1 | invocations=34
MINUTE 2026-10-11 13:56 UTC | over20=1 | invocations=77
MINUTE 2026-10-11 14:31 UTC | over20=1 | invocations=9
MINUTE 2026-10-11 14:58 UTC | over20=2 | invocations=31
MINUTE 2026-10-11 15:07 UTC | over20=1 | invocations=53
MINUTE 2026-10-11 15:26 UTC | over20=1 | invocations=162
MINUTE 2026-10-11 15:27 UTC | over20=1 | invocations=117
MINUTE 2026-10-11 15:30 UTC | over20=1 | invocations=13
MINUTE 2026-10-11 15:39 UTC | over20=1 | invocations=9
MINUTE 2026-10-11 15:41 UTC | over20=1 | invocations=13
MINUTE 2026-10-11 15:59 UTC | over20=1 | invocations=7
MINUTE 2026-10-11 16:42 UTC | over20=1 | invocations=23
MINUTE 2026-10-11 17:39 UTC | over20=1 | invocations=24
MINUTE 2026-10-11 18:04 UTC | over20=1 | invocations=41
MINUTE 2026-10-11 18:05 UTC | over20=1 | invocations=138
MINUTE 2026-10-11 18:36 UTC | over20=1 | invocations=2
MINUTE 2026-10-11 19:06 UTC | over20=1 | invocations=12
MINUTE 2026-10-11 19:24 UTC | over20=1 | invocations=12
MINUTE 2026-10-11 19:53 UTC | over20=1 | invocations=20
MINUTE 2026-10-11 20:21 UTC | over20=1 | invocations=117
MINUTE 2026-10-11 20:22 UTC | over20=1 | invocations=20
MINUTE 2026-10-11 20:36 UTC | over20=1 | invocations=105
MINUTE 2026-10-11 20:45 UTC | over20=1 | invocations=105
MINUTE 2026-10-11 20:48 UTC | over20=1 | invocations=25
MINUTE 2026-10-11 20:49 UTC | over20=1 | invocations=160
MINUTE 2026-10-11 21:08 UTC | over20=1 | invocations=72
MINUTE 2026-10-11 21:32 UTC | over20=1 | invocations=14
MINUTE 2026-10-11 21:36 UTC | over20=1 | invocations=10
MINUTE 2026-10-11 21:44 UTC | over20=1 | invocations=51
MINUTE 2026-10-11 21:45 UTC | over20=1 | invocations=64
MINUTE 2026-10-11 22:08 UTC | over20=1 | invocations=149
MINUTE 2026-10-11 22:18 UTC | over20=1 | invocations=41
MINUTE 2026-10-11 22:19 UTC | over20=2 | invocations=137
MINUTE 2026-10-11 22:20 UTC | over20=2 | invocations=109
MINUTE 2026-10-11 22:33 UTC | over20=1 | invocations=70

Across the 49 minutes the invocations per minute have a median of 23 (min 1, max 162). The whole window's median minute among the 540 minutes that hold any REPORT line is 31.5 invocations (max 390).

## Sources

- REPORT lines in the window, `stats count(*)` on `@type = "REPORT"`, log group /aws/lambda/opal-amgt-scoped-api | n=32528
- Over-20 s REPORT list, `@type = "REPORT" and @duration > 20000`, sorted by time, with request id, duration and init duration | n=53
- Cold among the over-20 s, `@initDuration > 0` | n=12
- Cold among all invocations (context only), `@initDuration > 0` | n=210
- Every log line of the 53 request ids, `filter @requestId in [...]` (START, END, REPORT, pool-full WARNING) | n=436
- REPORT count by `bin(1m)` over the window (540 non-empty minutes) | n=32528
- Function configuration, `get_function_configuration` for opal-amgt-scoped-api | n=1

## Surfaces

READ: CloudWatch Logs Insights on the function's own log group /aws/lambda/opal-amgt-scoped-api (REPORT, START, END and application lines)
READ: Lambda function configuration of opal-amgt-scoped-api (CodeSha256, LastModified, Version, Timeout, MemorySize, State)
NOT READ: the API gateway's own access log for the scoped API (not in this order's bounds; no call made)
NOT READ: the function URL's access log, the S3 request log of the endpoint named in the warning, and the client's side (browser timing); none in this order's bounds, none called

## Not changed

WRITES: none. No invoke, no deploy, no store write, no schedule, no bun, npm or pip install, no Bloomberg call, no S3 delete. The reading names no client, firm or account.
