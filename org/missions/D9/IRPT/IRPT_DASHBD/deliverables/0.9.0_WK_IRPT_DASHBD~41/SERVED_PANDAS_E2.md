# SERVED_PANDAS_E2 -- the activity-and-lot release on the served runtime (TO-DB-b-64)

Counts only. Read 2026-10-09T01:27:16Z with the .tools/aws shim; reads only, ZERO invokes.

| Item | Value |
|---|---|
| Function | irpt-49f-reporting-gold-lambda (us-east-1), 2,048 MB, 900 s, python3.12 |
| Code sha256 | Mex71Y5gk9RYE9q885knj3Ph12xV2Y9eVqMl3uJ1Z44= |
| Last modified | 2026-10-03T16:57:43Z |
| Layer | irpt-performance-native-layer:1 |
| Layer pandas | 2.2.3 (numpy 1.26.4, pyarrow 14.0.2) |
| Deployed package | 16 members, 5 .py |
| Packaged .py | handler.py; lib/opal_naming.py; lib/trading_calendar.py; data/assets/scripts/lib/stream_parquet.py; data/assets/scripts/gold/irpt_reporting/account_return_daily.py |
| Lots producer packaged | NO (account_activity_lots.py absent) |
| Branch taken | not packaged: no invoke |
| Invokes made | 0 |
| Verdict | REFUSED |

The deployed bytes agree with the declared package in lambda-source-map.json: the served function holds the daily-return
producer only, so it cannot run the lots stage as served.

| Runtime | Lots peak (MB) | Limit (MB) |
|---|---|---|
| pandas 3.0.6 (dell2, batch 1000) | <= 1,763 | 2,048 |
| pandas 2.3.3 | measured in an earlier round; figure not in this order, not restated | 2,048 |
| pandas 2.2.3 (served) | not measured: REFUSED, producer not packaged | 2,048 |

Next step per the order: a 2.2.3 kit request, routed by the issuer.
