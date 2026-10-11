# C-S82 -- the two HTTP 500s on /compare during the CVO's walk: a cause reading

**Seat:** 0.7.0_AE_CloudOps~RA1. **Order:** AMGT_RESAPP.TO-AMGT-aa-3 (issued 1e92ba6e74). **Read at:** 2026-10-11T16:12Z-16:19Z.
**Walk window:** 2026-10-11 15:34Z-15:44Z (walk files `tmp/ui-walk/20261011T153440Z/`). **Read window:** 15:30Z-15:50Z.
All times UTC. Every CloudWatch timestamp below was converted from the client's local zone to UTC before it was printed.

## Sources

- CloudWatch `get-metric-statistics`, `AWS/Lambda`, FunctionName `opal-amgt-scoped-api`: Invocations, Errors, Throttles, ConcurrentExecutions, Duration; 15:30Z-15:50Z, period 60 s; n=15 datapoints per metric (5 of the 20 minutes returned no datapoint).
- CloudWatch `get-metric-statistics`, `AWS/Lambda`, FunctionName `opal-portal-authorizer` (the HTTP API's REQUEST authorizer): Invocations, Errors, Throttles, ConcurrentExecutions, Duration; same window and period; n=15 datapoints per metric.
- CloudWatch `get-metric-statistics`, `AWS/ApiGateway`, ApiId `7k3ed8px20` (HTTP API `opal-portal-data-proxy-api`, the origin `APIGateway-portal` of distribution `EVTSA9VEHNZVH`): Count, 4xx, 5xx, Latency, IntegrationLatency; same window and period; n=15 datapoints per metric.
- CloudWatch `get-metric-statistics`, `AWS/CloudFront`, DistributionId `EVTSA9VEHNZVH`, Region Global (the distribution that answers `d2n2nzpeqf34ge.cloudfront.net`): Requests, 4xxErrorRate, 5xxErrorRate, TotalErrorRate; same window and period; n=15 datapoints per metric.
- CloudWatch Logs `filter-log-events`, log group `/aws/lambda/opal-amgt-scoped-api`, 15:30Z-15:50Z, no pattern, paginated to the end: n=1266 events (292 START, 292 END, 292 REPORT, 390 application lines); lines naming `/ROG/` or `/BA/`: n=0 (the function's lines carry no request path).
- `cloudfront get-distribution-config` EVTSA9VEHNZVH: n=30 cache behaviors read (29 path behaviors and the default); standard logging and real-time log configs read for each; origin settings read for the two API origins.
- `apigatewayv2 get-stages`, `get-routes`, `get-integration`, `get-authorizer` on `7k3ed8px20`: n=1 stage, n=119 routes; the `/compare` route's integration and authorizer read.
- `lambda get-function`, `get-account-settings` for the two functions and the account: n=2 functions, n=1 account; reserved concurrency and limits read.
- The CVO's walk `netlog.tsv`: n=1418 rows (1361 status 200, 53 status 204, 2 status 401, 2 status 500); of them n=72 are `/api/scoped/amgt/security/<ticker>/compare` rows (70 status 200, 2 status 500; ROG n=16 with 15x200 and 1x500, BA n=15 with 14x200 and 1x500). Method, status and path only, no time and no request id. The two 500s are the only 500s in the whole netlog. (The order's own count reads 70 compare calls with 68 answering 200; the file holds 72 with 70, and the ROG 15 and BA 14 answering 200 agree with the order.)
- `portal/vite.config.ts` and the installed `portal/node_modules/vite/dist/node/chunks/config.js` (proxy middleware): n=2 files read for how a proxy error is answered.

## Requests

The two failing requests, as the sources show them:

- ROG, Model tab: `GET /api/scoped/amgt/security/ROG/compare` -> 500, netlog row 766 (the first of the ROG compare rows; the rows after it answer 200). Time: not recorded by the netlog (the walk window is 15:34Z-15:44Z). Layer that logged it: none readable. Request id: none exists in any readable source.
- BA, Posture tab: `GET /api/scoped/amgt/security/BA/compare` -> 500, netlog row 1003 (the last of the BA compare rows; the rows before it answer 200). Time: not recorded by the netlog. Layer that logged it: none readable. Request id: none exists in any readable source.

Why no request id: the HTTP API stage `$default` has `AccessLogSettings` null (access logging is NOT enabled) and the function's lines carry no path; CloudFront standard logging is disabled and none of the 30 behaviors names a real-time log config. That none of the three layers keeps a per-request record is itself a finding.

## Metrics

All values are the maximum of the per-minute datapoints, over 15:30Z-15:50Z, UTC, n counted per metric.

- opal-amgt-scoped-api Throttles/Sum: max=0.0 n=15 (sum 0).
- opal-amgt-scoped-api ConcurrentExecutions/Maximum: max=10.0 n=15 (the peak is 15:36Z, with 112 invocations that minute).
- opal-amgt-scoped-api Errors/Sum: max=0.0 n=15 (sum 0). Invocations/Sum: max=112.0 n=15 (sum 291).
- opal-amgt-scoped-api Duration/Maximum: max=28472.98 ms n=15 (15:30Z 28.5 s, 15:36Z 18.5 s, 15:38Z 23.4 s, 15:41Z 22.5 s; none reaches the 29 s function timeout or the integration's 29 s).
- opal-portal-authorizer Throttles/Sum: max=0.0 n=15; ConcurrentExecutions/Maximum: max=2.0 n=15; Errors/Sum: max=0.0 n=15; Invocations/Sum: max=26.0 n=15 (sum 218).
- HTTP API 7k3ed8px20 5xx/Sum: max=0.0 n=15 (sum 0). Count/Sum: max=30.0 n=15 (sum 266). 4xx/Sum: max=3.0 n=15 (sum 6, at 15:33Z 1, 15:34Z 2, 15:43Z 3; these are 4xx, not 500).
- CloudFront EVTSA9VEHNZVH 5xxErrorRate/Maximum: max=0.0 n=15. Requests/Sum: max=59.0 n=15 (sum 405). 4xxErrorRate/Maximum: max=100.0 n=15 at 15:33Z, 15:34Z and 15:43Z, the same three minutes as the API's 4xx.

## Concurrency

- opal-amgt-scoped-api: reserved=none (`get-function` returns no `Concurrency` key, and `get-function-concurrency` returns an empty object). Timeout 29 s, memory 1769 MB.
- opal-portal-authorizer: reserved=none. Timeout 10 s, memory 256 MB.
- Account: ConcurrentExecutions limit 1000, UnreservedConcurrentExecutions 978 (22 are reserved by other functions). The two functions here draw on the unreserved pool; the peak of 10 plus 2 is 1.2 percent of it.

## Layers

- Dev-server proxy (`portal/vite.config.ts`, `/api/scoped/amgt/*` falls to the catch-all `/api` -> `https://d2n2nzpeqf34ge.cloudfront.net`, no `timeout`, no `proxyTimeout`, no `error` handler set in the config): the proxy's own log is `not readable: it goes to the dev server's console, which was not captured to any file the walk or this seat can read`. What IS readable is how the installed Vite answers a proxy error: `proxy.on("error", ...)` logs `http proxy error: <url>` and, if no header was sent, `res.writeHead(500, {"Content-Type": "text/plain"}).end()` -- a 500 with an empty body for ANY proxy failure (reset, timeout, socket hang up).
- CloudFront (`EVTSA9VEHNZVH`, behavior `/api/scoped/amgt/*` -> origin `APIGateway-portal`, viewer-request Lambda@Edge `auth-validator-edge:22`, origin read timeout 30 s): request-level logs `not readable: standard logging disabled, no real-time log config`. Metrics read: 5xxErrorRate max=0.0 over n=15 datapoints against 405 requests. CloudFront counts an origin 5xx, a Lambda@Edge error and a timeout as 5xx, so a 500 or 5xx served by this layer would not read 0.
- API Gateway (HTTP API `7k3ed8px20`, `$default` stage, route `GET /api/scoped/amgt/security/{security_key}/compare` -> AWS_PROXY integration `352l7td` to `opal-amgt-scoped-api`, 29 s integration timeout, REQUEST authorizer `portal-jwt-authorizer` -> `opal-portal-authorizer`): per-request lines `not readable: AccessLogSettings null (access logging is not enabled)`. Metrics read: 5xx max=0.0 over n=15 datapoints against a Count of 266. An authorizer failure and an integration failure both count as 5xx on this API.
- Lambda `opal-amgt-scoped-api`: Errors max=0.0 and Throttles max=0.0 over n=15; 292 START, 292 END, 292 REPORT and no error, traceback or timeout line (this confirms the order's own reading of the log group); the authorizer `opal-portal-authorizer`: Errors max=0.0, Throttles max=0.0 over n=15.

Not a layer the order named but one the route crosses: the REQUEST authorizer. It is read above and is clean.

## Cause

CAUSE: DEV-PROXY

Reasoning, by elimination with one positive mechanism, and what it does not prove:

1. Every AWS layer the request crosses reads zero 5xx over a window that contains the walk: CloudFront 5xxErrorRate 0 (405 requests), HTTP API 5xx 0 (266 requests), function and authorizer Errors 0 and Throttles 0 (291 and 218 invocations), reserved concurrency none against 978 unreserved, peak concurrency 10. A 500 that CloudFront or API Gateway had served would be counted in one of those. THROTTLED, GATEWAY-INTEGRATION, CLOUDFRONT and FUNCTION each predict a non-zero reading in a metric read here, and none is non-zero.
2. The one layer left that can answer 500 with no AWS-side record is the dev-server proxy, and its handler is read in the installed Vite: any proxy error answers 500 with an empty body. The walk saw exactly this shape: 2 of 72 compare rows in the netlog, each surrounded by 200s for the same name (ROG 15 of 16, BA 14 of 15), and no other 500 among the 1418 rows (the CVO's direct invokes answer 200).
3. What this does NOT prove: the proxy's own line (`http proxy error: /api/scoped/amgt/security/ROG/compare` with its error stack) was not read, so the underlying error (reset, timeout or socket) is not named, and the cause is established by elimination, not by observation at the proxy. The deciding source for the sub-cause is the dev server's console output for 15:34Z-15:44Z; if the walk is repeated, run the dev server with its output redirected to a file.
4. The function itself was slow in the window (a maximum of 28.5 s at 15:30Z, 23.4 s at 15:38Z and 22.5 s at 15:41Z, against a 29 s function timeout and a 30 s CloudFront origin read timeout). A response that long is a plausible trigger for a socket-level proxy error with no timeout configured on the proxy, but this reading did not observe which minute held either failing request, so it is stated as a candidate, not a finding.

A fix is not part of this order.

## Not changed

WRITES: none. Nothing was written or changed in any function, API, stage, log setting, alarm, concurrency, metric filter, distribution or log group. Reads were AWS control-plane and CloudWatch calls from the seat's own credentials plus local file reads; no test traffic was sent to the live API; no surprise row was filed.
