# AMGT-bh-4 -- first full weekday after the S3-client build, `/aws/lambda/opal-amgt-scoped-api`

Order: AMGT_RESAPP.TO-AMGT-bh-4.read-the-first-weekday-of-the-s3-client-build-from-the-function-log (round 101, decomposition s.109).
Worker: 0.9.0_WK_AMGT_RESAPP~400. Read only. The function was not invoked; no other AWS call was made beyond the Logs Insights queries and the one configuration read.
Window read by the round-99 method: 2026-10-12T12:40:00Z to 2026-10-13T12:40:00Z. Every query returned Complete; none Failed, Cancelled or Timed out.

## Window

WINDOW 2026-10-12T12:40:00Z to 2026-10-13T12:40:00Z (UTC, 24 h; the end was fixed before the reads began; the reads ran from 2026-10-13T12:44Z)
FUNCTION CodeSha256 42z0tn68TZjuk8awBclnMii0k+FX2Pw2bw7iN9Xitz0= LastModified 2026-10-12T04:18:21.000+0000 (read at 2026-10-13T12:44:06Z, after the window end; State Active, LastUpdateStatus Successful, Timeout 29 s, MemorySize 1769 MB)
LastModified before the window start: the function's code did not change inside the window, because the one read at 12:44Z shows the last change at 04:18:21Z, before 12:40Z.
The order gives the build as applied 2026-10-12T04:17:52Z; the function reads LastModified 04:18:21Z, 29 s later. Both precede the window; the difference is recorded, not used.

## Counts

- INVOCATIONS n=625 | round 99 window n=32528 | not a rate: the window's own total, not comparable as a count
- OVER 20 s n=1 | round 99 n=53 | per 1,000 invocations: 1.60 (round 99: 1.63)
- ATTRIBUTED n=0 | round 99 n=0 | per 1,000: 0.00 (round 99: 0.00)
- UNATTRIBUTED n=1 | round 99 n=53 | per 1,000: 1.60 (round 99: 1.63)
- COLD n=1 | round 99 n=12 | per 1,000: 1.60 (round 99: 0.37)
- POOL-FULL n=0 | round 99 n=49 | per 1,000: 0.00 (round 99: 1.51)
- NO POOL-FULL n=1 | round 99 n=4 | per 1,000: 1.60 (round 99: 0.12)

Context, not one of the seven: cold starts among all 625 invocations of the window n=6 (round 99: n=210; per 1,000: 9.60 against 6.46). Invocations over all of the window carrying the 'Connection pool is full' warning n=0 (round 99 window: n=582 invocations, so the query returns the warning where it exists).

Why, from the numbers: the window is not a comparable day. It holds 625 invocations against 32,528 in the round-99 window, and its REPORT lines stop twice. The last REPORT line before the first gap is 2026-10-12T05:38:03Z; the next is 2026-10-12T12:30:43Z. The last REPORT line before the second gap is 2026-10-12T13:06:42Z; the next is 2026-10-13T12:30:43Z, one invocation, which is the only REPORT line of the final hour of the window. Both gaps hold zero REPORT lines. The one over-20 s invocation (request id d6d9ce24-c675-45de-8389-b74317dbb3bc, START 2026-10-12T12:41:11.742Z, duration 20,049.86 ms, cold with init 686.71 ms, max memory 385 MB) has only START, END and REPORT lines: no warning and no application line, so it carries no pool-full evidence. The zero pool-full count is not a query-syntax zero: the same query, run on the round-99 window, returns 582 invocations and 3,341 lines. With 625 invocations, one over-20 s invocation is a rate of 1.60 per 1,000, which cannot be told apart from round 99's 1.63; the other rates rest on counts of 0, 1 or 6 and show no comparison.
What these numbers do NOT show: why the log group holds no REPORT lines for those hours. Either no invocation reached the function or the log delivery lost them; the logs cannot separate the two, and the API gateway log was not read. Whether anyone used the scoped API in the silent hours. Whether the one over-20 s run has any link to the build, which precedes the window by 8 hours, or to the Monday snapshot write. The cause of the slow run. A route or a security key for it. A rate from one event is one event.

## Routes

ROUTE none attributable | reason: the one over-20 s invocation (request id d6d9ce24-c675-45de-8389-b74317dbb3bc) has 3 log lines, START, END and REPORT; none of them contains a route path, a security key or `route=`. No route was inferred from the duration or the hour.

## Names

NAME none attributable | reason: the same 3 log lines name no security key. No name is attributed to the one over-20 s invocation.

## Beside

Each MINUTE line counts the over-20 s invocations whose REPORT line (event time, equal to START plus the duration) falls in that UTC minute, and the REPORT count of that minute over the whole window (stats count(*) by bin(1m); 16 non-empty minutes in the window).

MINUTE 2026-10-12 12:41 UTC | over20=1 | invocations=2

The window's invocations per minute: median 48 across the 16 non-empty minutes (min 1 at 2026-10-13 12:30 UTC, max 63 at 2026-10-12 13:00 UTC). The minute holding the over-20 s run is a quiet one of 2 invocations, against that median of 48.

## Sources

- REPORT lines in the window, `stats count(*)` on `@type = "REPORT"`, log group /aws/lambda/opal-amgt-scoped-api | n=625
- Over-20 s REPORT list, `filter @type = "REPORT" and @duration > 20000`, with request id, duration and init duration | n=1
- Cold among the over-20 s, `filter @type = "REPORT" and @duration > 20000 and @initDuration > 0` | n=1
- Cold among all invocations in the window (context only), `filter @type = "REPORT" and @initDuration > 0` | n=6
- Every log line of the one over-20 s request id, `filter @requestId = "d6d9ce24-c675-45de-8389-b74317dbb3bc"` | n=3
- Invocations over the window carrying the warning, `filter @message like /Connection pool is full/ | stats count_distinct(@requestId)`; zero matching records | n=0
- Positive control, the same warning query over the round-99 window 2026-10-10T23:29:21Z to 2026-10-11T23:29:21Z: 582 invocations, 3,341 lines | n=582
- Positive control, REPORT count over the round-99 window, by hour (22 hour bins) | n=32528
- REPORT count by minute over the window, 16 non-empty minutes | n=625
- REPORT count by hour from 2026-10-11T12:00Z to 2026-10-13T12:40Z, the silence evidence | n=34871
- All-event count by hour from 2026-10-12T04:00Z to 13:30Z, the silence evidence (hours 04, 05, 12 and 13) | n=17270
- Function configuration, `get_function_configuration` for opal-amgt-scoped-api, one read at 2026-10-13T12:44:06Z | n=1

## Surfaces

READ: CloudWatch Logs Insights on the function's own log group /aws/lambda/opal-amgt-scoped-api (REPORT, START, END, INIT and application lines)
READ: Lambda function configuration of opal-amgt-scoped-api (CodeSha256, LastModified, State, LastUpdateStatus, Timeout, MemorySize), one read
NOT READ: the API gateway's own access log for the scoped API (outside this order's bounds; no call made)
NOT READ: the function URL's access log, the S3 request log of the endpoint and the client's side (outside this order's bounds; none called)

## Not changed

WRITES: none. No invoke, no deploy, no store write, no schedule, no bun, npm or pip install, no Bloomberg call, no S3 delete. The reading names no client, firm or account.
