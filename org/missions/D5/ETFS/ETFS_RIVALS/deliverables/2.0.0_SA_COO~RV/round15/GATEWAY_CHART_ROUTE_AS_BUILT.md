# The gateway chart route, as built (ETFS_RIVALS round 15, cell RIV-rt-1)

For the NFRA_OPLGTW release ask (1.0.0_SA_CTO~Z msg 30755). Read from the merged code on site-Z CLOUD @f7f2cb7c2e
(build 890c0aa948): `infra/aws/ec2/opal-gateway/app/rivalfunds_view.py` (`valid_fund`, `chart_key`,
`rivalfunds_chart`) and `infra/aws/ec2/opal-gateway/app/server.py:1116`. Not exercised on a served gateway: no
release carries it yet.

## Request

`GET /rivalfunds/<YYYY-MM-DD>/chart/<FUND>`

- `<FUND>` matches `[A-Z0-9]{1,8}` in full.
- Behind the same identity wall as `/rivalfunds/<day>` and `/rivalfunds/<day>/audit` (`server.py:203` treats every
  rivalfunds path alike). Route class `access-layer` in `tests/test_principal_cutover.py` `ROUTE_CLASS`.
- Mounted before `/rivalfunds/{day}` and after `/rivalfunds/{day}/audit`.

## What it reads

One S3 object: `<page prefix>date=<day>/charts/<FUND>.json`, the page prefix resolved by
`app/gen_rivalfunds_location.py` as for the page. No new bucket, prefix, IAM grant or resource: the object sits under
the page prefix the gateway already reads. The object is written by the publisher (cell RIV-co-1, `publish_page.py`).

## Responses

| Status | Body | When | Audit log |
|---|---|---|---|
| 200 | `application/json`, the stored bytes unchanged | the object exists and is under the size cap | `rivalfunds_view` `{day, fund, route: "chart"}` ok |
| 400 | `{"error": "bad day or fund. Use /rivalfunds/YYYY-MM-DD/chart/FUND."}` | bad day or fund | none; no S3 read |
| 401 | `{"error": "identity required"}` | no viewer | none; no S3 read |
| 404 | `{"error": "no chart for this fund and day"}` | no such object | logged |
| 502 | `{"error": "chart over the size cap"}` | the object is over the gateway's fetch cap | not read here |
| 502 | `{"error": "rivalfunds temporarily unavailable"}` | any other S3 error | logged with verdict `S3-ERROR` and the error class |

## The 200 body (the publisher's chart object)

```
{"fund", "asof", "generated_at",
 "ranges": {"R30": <first day>, "R90": <first day>, "R365": <first day>},
 "securities": {<security_key>: {
   "name", "source_words",
   "points": [[<YYYY-MM-DD>, <price>|null, <source code>], ...],
   "gaps": [{"start", "end", "reason"}],
   "markers": [{"side": "buy"|"sell", "start", "end", "span": bool, "usd", "bps", "r", "n_trades"}]}}}
```

Source codes: `m` market close, `i` holding-implied. `points` ascend by date and cover `asof - 365d .. asof`. The
publisher caps an object at 1,900,000 bytes: over it the points are thinned to weekly and the object says
`"thinned": true`; still over, the object is not written and the route answers 404 for that fund and day.

## Measured

- `rt-1.AC1.py` PASS 0 failures (6 of 6 checks), re-run by the issuer on the branch.
- `app/tests/test_rivalfunds_view.py` + `tests/test_principal_cutover.py`: 28 passed on merged CLOUD.
- The wider gateway suite reads 29 failed at the branch base and on the branch, identical lists, none a rivalfunds
  test (worker's measurement; row `ETFS_RIVALS-Z-W4-S19`). Owner: NFRA_OPLGTW.

## Order of release

Gateway release first, then the rivalfunds Lambdas. The page's one script (cell RIV-md-1) calls this route and
deploys only after it serves.
