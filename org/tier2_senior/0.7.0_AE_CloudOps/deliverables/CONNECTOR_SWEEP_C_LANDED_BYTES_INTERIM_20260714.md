# Connector sweep — verdict (c) LANDED-BYTES, interim table (session 2026-07-14 ~08:0xZ)

**archetype:** VALIDATE
**Commission:** Andrew-direct 03:19Z (via COO relay, prior session): per believed-live ligament —
(c) landed bytes vs cadence (surfaces grounded from env vars / code, never guessed), (d) what verifies
the landing, (e) does any guard count the LANDED property or a proxy. Calendar-first (NEVER#1).
**Backbone:** re-enumerated this session (read-only script @ `CONNECTOR_SWEEP_ligament_sweep.py`):
**138 EventBridge rules (122 ENABLED / 16 DISABLED) + 7 Scheduler schedules = 145 ligaments.**
Scheduled+enabled lambda-target pairs: 111; with surface-naming env vars: 48 unique (ligament, lambda)
pairs. Mechanically listable from env alone: 6. Needs-code-grounding (bucket named, no prefix): 41.
DDB-table surfaces: queued for keyed reads. Frontier: expected last trading day = **2026-07-14**.

## Verdicted rows (cadence-aware readings, cross-bucket×prefix script noise removed)

| ligament (schedule Z) | lambda | code/env-grounded surface | landed frontier | (c) verdict |
|---|---|---|---|---|
| cot-etf-ownership-daily (10:30) | cot-etf-ownership-daily | opal-data-etfs/daily/cottonwood/ (21 obj) | 2026-07-10.json | CADENCE-CONSISTENT with the KNOWN cot freeze (source gold/canonical/holdings also frontier 07-10; the 18-day silver failure is a held, known finding — close nothing on it). Today's 10:30Z run not yet due at check time. |
| etfs-canon-fanin-daily (15:45) | etfs-canon-fanin | opal-data-etfs/daily (131 obj) | 49financial/2026-07-06.json, mtime TODAY 05:12Z | HEALTHY-WRITES. Mtime axis = this session's C9 Phase-B(a) invokes landed; partition-name axis (07-06) is the C9 content thread, separately tracked. AXIS STATED per verification law #6. |
| fear-greed-daily-update (14:30, 21:30) | opal-portal-fear-greed-fetcher | opal-data-portal-v2/json/sentiment/fear-greed-index.json | yesterday 21:3xZ write | HEALTHY (today's first run 14:30Z not yet due). |
| news-trending-analysis-daily (11:15, 21:15) | news-trending-analysis | **code-grounded** opal-data-portal-v2/json/sentiment/keyword-sentiments.json | yesterday 21:17:03Z, 155,935 B | HEALTHY on the REAL surface. **FINDING NT-1 below** — the ENV-named surface is dead config. |
| etfs-reports-monthly-run + -absence-check (1st/mo) | etfs-reports-orchestrator | opal-data-etfs/platinum/reports/ | 2026-06/etf_ownership.html (written ~07-01) | HEALTHY ON MONTHLY CADENCE (a daily-frontier tdays number is the wrong axis for a monthly ligament; next expected write 2026-08-01). |

## FINDING NT-1 (FULLY GROUNDED: orphaned endpoint + orphaned key + doc drift; NO live user impact)

`news-trending-analysis` env carries `S3_KEY=sentiment/keyword-sentiments.json`, but the DEPLOYED code
(source-map @ 903fbe9a8, deployed 2026-06-11) hardcodes `json/sentiment/keyword-sentiments.json`
(`lambda_function.py:1524`) and never reads that env var for the write. Measured:
- REAL key `json/sentiment/keyword-sentiments.json`: fresh (last write yesterday 21:17Z, 155,935 B). Fires 4/50h, 0 errors.
- LEGACY key `sentiment/keyword-sentiments.json`: EXISTS, frozen ~127 trading days (~2026-02).

**Consumer trace, grounded on DEPLOYED bytes (proxy zip downloaded via GetFunction, not repo):** the live
`opal-portal-data-proxy` carries BOTH reads — `get_keyword_sentiments()` (route `GET /v1/sentiment/keywords`)
reads the **LEGACY** key and would serve **February data with rc=200** to any caller; its sibling GPT
"why" endpoint in the same deployed zip reads the NEW key (fresh). **The live frontend is NOT affected:**
`portal-proxy.ts:1857 getKeywordSentiments()` fetches `/api/general/sentiment/keyword-sentiments.json`
(the static/S3 route onto the NEW key) — TopicCloud gets fresh data. So `/v1/sentiment/keywords` is an
ORPHANED endpoint whose only remaining function is to answer probes with 5-month-old data that looks alive.
- Doc drift: `portal/docs/architecture/PORTAL_DATA_ARCHITECTURE.md:75` claims `/v1/sentiment/keywords`
  reads the NEW path — false at the deployed proxy.
- Residual hazards: (1) any future consumer/agent wiring to the documented `/v1` endpoint inherits
  February data with no error; (2) the legacy key invites the same false-staleness read this sweep
  almost made. Cleanup candidates (BOTH out of my lane/authority): proxy endpoint fix or removal
  (DE/DT lane), legacy-key delete (human-confirmation class). ROUTED to COO as table finding, not P1.
- (e) lesson, generalized: **an env var is DESIRED-ish config, not a write receipt** — this sweep's own
  method upgraded mid-pass: env-grounded surface first, code-grounding REQUIRED whenever the env surface
  reads stale before any escalation (this row would have been a false P1 otherwise). And its mirror:
  **an rc=200 endpoint is not a fresh endpoint** — the proxy serves the frozen key without error.

## Method + queue state

- Verdict script (read-only): scratchpad `ligament_c_landed_bytes.py`; JSON at `ligament_c_verdicts.json`.
- 41 rows NEEDS-CODE-GROUNDING (env names bucket only): per-lambda source read → write-prefix extraction
  → listing. Priority order: client-data pipelines (bd/cot/inf/etfs/mdpf) → portal/news → monitors.
- DDB surfaces (news articles/trending, etfs-ownership-daily, others): keyed reads queued.
- Verdicts (d)/(e) fill alongside code-grounding (the write-verify + guard-property questions are answered
  at the same source read).
- INF-chain ligaments: read-only observation ONLY (standing hold; a freshness guard reading RED there is a
  guard WORKING).

## FINDING SA-1 (ESCALATED to COO same-turn, 081832Z): both seeking-alpha ligaments believed-live + content-dead ~4.5 months

- `seeking-alpha-news-daily` (cron 14:00Z) + `seeking-alpha-analysis-daily` (cron 21:00Z): ENABLED,
  firing 2/50h each, invocations match, **Lambda Errors metric 0** — and newest article CONTENT is
  `seeking-alpha/news/articles/2026-02-24/` (news) / manifests dead since 2026-04-13 (analysis).
- **Mechanism (CloudWatch, both lambdas, latest runs):** every Bright Data fetch → `401 Unauthorized`
  (`api.brightdata.com/request`) — dead vendor credential — caught-and-continued, so rc=0.
- **The mask:** the news coordinator still writes a well-formed `dedup_report.json` manifest DAILY —
  a fresh-looking landing that satisfies every listing check while carrying nothing. Ruling-26 specimen
  (the C5 267-byte class, at ligament scale, live for ~4.5 months).
- Vendor-held: Bright Data egress is NOT lifted; fix = Andrew's word; retire-vs-revive = above my lane.
  Blast-radius open cell: opal-data-news-av consumers (portal sentiment rides the SEPARATE
  opal-news-articles DDB chain, healthy — user impact possibly nil, unconfirmed).

## Batch-2 verdicted rows (code-grounded exact surfaces, ~08:1xZ)

| ligament | code-grounded surface | landed frontier | (c) verdict |
|---|---|---|---|
| bd-49f-{fees-,}session-daily | opal-data-bd/blackdiamond/49f/session-trigger-mode.json | TODAY 00:00:19Z | HEALTHY (trigger writes; downstream = EC2 session chain, separately owned) |
| cot-bd-session-daily | opal-data-cot/blackdiamond/cot/session-trigger-mode.json | TODAY 02:02:46Z | HEALTHY trigger; downstream cot silver freeze = the KNOWN held finding |
| etf-ownership-dashboard-daily | opal-data-etfs/platinum/etf_ownership_dashboard.json | 07-13 16:00:03Z | HEALTHY (today's 16:00Z not yet due) |
| news-api-*/news-rss-* (16 ligaments, one lambda) | opal-data-news-v2/logs/ingestion_* | TODAY 08:00:50Z | HEALTHY (log surface; article DDB keyed read queued) |
| seeking-alpha-news-daily | seeking-alpha/news/{articles,manifests} | articles 02-24 / manifest 07-13 | **SA-1 FAIL — manifest masks dead content** |
| seeking-alpha-analysis-daily | seeking-alpha/analysis/manifests/ | 2026-04-13 | **SA-1 FAIL** |
| opal-cot-value-parity-hourly | — | — | **GAP: lambda NOT in lambda-source-map.json (Rule 4)** — source-map registration queued as a finding; sibling opal-inf-value-parity maps to infra/aws/compdiff |

**Escalations: 1 (SA-1, same-turn).** NT-1 downgraded to drift on code-grounding (see above); COO PARKED
it with named triggers (081510Z). Remaining queue: ~12 reader-only probe rows ((c)=N/A-reader; their (d)/(e)
answered at their read-surface guards), DDB keyed reads, opal-inf-value-parity cfg resolution (INF domain,
read-only observation).
