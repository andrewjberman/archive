# OG-pm-2 -- the latency cause read (2026-10-05 and 2026-09-30, UTC)

**Finding: MIX.** No slowdown of the routes that existed at OG-p-1.

## Instrument
ALB access logs (`access_logs.s3.enabled=true`, `s3://opal-data-security/waf-logs/alb-opal-gateway/`), field `target_processing_time`, the same quantity as CloudWatch `TargetResponseTime`. Caller identity for the one steady caller comes from the gateway audit lake (`opal-mcp-audit`), which carries no latency. Reads only; the probes are in `probes/`.

Cannot see: requests the ALB answers itself (903 of 4,231 rows on 10-05; 1,573 of 4,083 on 09-30); the MCP tool inside `POST /mcp`; any principal beyond IP and User-Agent; requests with no target response (2 on 10-05, 81 on 09-30; counted, latency null); health checks; bodies and secrets. The log order-statistic p95 reads 0.9358 s against CloudWatch's 0.9473 s on 10-05.

## Coverage (log forwarded rows against ALB RequestCount, CloudWatch read for the same UTC day)
| day | covered | ALB RequestCount | timed | ALB SampleCount | CloudWatch p95 |
|---|---|---|---|---|---|
| 2026-10-05 | 3,328 | 3,328 | 3,326 | 3,326 | 0.9473 s |
| 2026-09-30 | 2,510 | 2,510 | 2,429 | 2,429 | 0.5446 s |

## Routes (top by requests; full tables in `PM2_CAUSE.json`; `*` = existed at OG-p-1)
2026-10-05 (34 routes):
| route | requests | p95 s |
|---|---|---|
| GET /hx/teams/chats | 1,440 | 1.018 |
| GET /ms/site_children * | 1,261 | 0.524 |
| POST /mcp * | 224 | 0.0767 |
| GET /hx/teams/chats/{id}/messages | 87 | 0.902 |
| GET /mcp * | 79 | 0.0262 |
| POST /token * | 40 | 0.396 |
| GET /.well-known/oauth-authorization-server * | 36 | 0.0013 |
| POST /mcp/ * | 21 | 0.025 |

2026-09-30 (18 routes):
| route | requests | p95 s |
|---|---|---|
| GET /ms/site_children * | 1,247 | 0.581 |
| POST /mcp * | 963 | 0.109 |
| GET /mcp * | 165 | 0.124 |
| POST /token * | 58 | 0.553 |
| GET /.well-known/oauth-authorization-server * | 38 | 0.0014 |

The at_ogp1 set is the route set of the Gateway source at `7bd89b5d71` (the commit OG-p-1 AC1 digest-compared the host against, 50 of 50), with the ALB rules from OGP1-AC3 (row Z-W27-S4).

## Hypothesis (i): yes
`GET /hx/teams/chats`, audit label `teamsassist` (tool `hx_teams`), `Python-urllib/3.12`, 60 requests every hour, 24 of 24 hours on 10-05, p95 1.018 s. First seen 2026-10-02T19:18Z (OG-rl-3's release day); 1,440 a day from 10-03. It is 1,380 of the 1,972 requests in the 23 hours other than 02Z: 70.0 % of the quiet-hour traffic, and 90.1 % of all requests on routes added since OG-p-1.

## The deciding numbers
| 10-05 vs 09-30 | 10-05 | 09-30 |
|---|---|---|
| routes at OG-p-1, all requests, p95 | 0.5147 s (1,727 timed) | 0.538 s (2,424) |
| routes at OG-p-1, hours other than 02Z, p95 | 0.2896 s | 0.3082 s |
| POST /mcp p95 | 0.0767 s | 0.1088 s |
| POST /token p95 | 0.396 s | 0.5525 s |
| GET /ms/site_children p95 | 0.524 s | 0.581 s |
| routes added since OG-p-1, p95 | 1.0142 s (1,599) | 0.003 s (5) |

The routes that existed at OG-p-1 read below the 0.6642 s cap and at or below their 09-30 values, route by route. The day's 0.9473 s comes from routes added since, led by the steady poller. This is MIX; it is not SLOWDOWN. The ruling on the cap is the CTO's (R17).

## Context (read-only, same instruments)
10-01 0.599, 10-02 0.899, 10-03 1.655, 10-04 0.961, 10-05 0.947 (CloudWatch). The poller's own p95 was 1.85 s on 10-03 (row Z-W27-S5).

writes: 0.
