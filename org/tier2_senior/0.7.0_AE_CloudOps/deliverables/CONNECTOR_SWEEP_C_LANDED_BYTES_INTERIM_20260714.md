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

## DDB-surface rows (queued keyed reads -- verdicted 2026-07-14 ~18:5xZ session)

| DDB surface | writer ligament | (c) verdict | (d)/(e) notes |
|---|---|---|---|
| opal-etfs-ownership-daily | etfs-canon-fanin (15:45Z) | HEALTHY -- CLOSED BY TODAY'S C9 cond-3 verify: 12/12 slices true-vintage, exactly one 12-write burst/day at 15:45Z (CW metric, 07-11..14), ingested_utc ties | (d) CW invoke log + write-capacity metric + row stamps; (e) the C9 tripwire class reads the ROW (the landed property), not a proxy |
| opal-assets-daily-aua | opal-assets-daily-emitter (17:15Z) | WRITER CADENCE-HEALTHY / CONTENT PINNED-BY-HOLD: daily fires (07-13+07-14 both 17:15Z, rows_written=28, rc clean) re-emit the FROZEN mdpf platinum 07-10 vintage -- the held INF/mdpf chain's shadow, BY DESIGN; close nothing on it. Row semantics are self-documenting (staleness=99 SENTINEL shared by contract with the 14 mdpf-cohort alarms; vintage_state/coverage_state are the unambiguous read) | (d) emitter OK-line carries partition_key+rows_written; (e) the row ITSELF carries the staleness measure + sentinel -- a guard reading the landed property by construction |
| opal-news-articles | news ingest chain | SAMPLE-LIVE (item ingested 2026-07-12T08:00Z observed); NEWEST-ITEM read OPEN -- needs the table's key/GSI schema for an efficient newest query (full scan disproportionate); the chain's S3 surfaces already verdicted HEALTHY (NT-1 row) | (d)/(e) fill with the newest-item read |

## FINDING CF-1: comp-freshness `ddb` mode reads FALSE-EMPTY on populated tables (2/2 tested)

`comp-freshness ddb opal-assets-daily-aua` and `... opal-news-articles` both printed
`WARN / NOTE: No items found with PK prefix ''` -- while direct scans return items on BOTH tables.
The instrument's default PK-prefix mechanism does not fit either table's key shape, and the
resulting verdict is BYTE-INDISTINGUISHABLE from a genuinely empty table (verification law #5:
no channel for "I don't know" -- not-knowing renders as a WARN that looks measured). Same family
as the CLAUDE.md NEVER#1 comp-freshness caveat (missing freshness_basis falls back silently).
ROUTED to COO for tool-owner routing: these two tables need per-table config entries (real PK
pattern + freshness_basis trading-day-frontier where applicable), and the empty-read should say
CONFIG-MISS, not WARN-empty.

## Priority code-grounding batch 2 (2026-07-14 ~18:5xZ)

| ligament | lambda | (c)/(d)/(e) verdict |
|---|---|---|
| gldinc-ss4c-canary-daily (06:30Z) | gldinc-ss4c-canary | HEALTHY + GUARD-POSITIVE: fired 2/50h (cadence-exact); pure reader/asserter on the LIVE gold/_state/load_flows cache (no S3 writes; CW metrics out); (e) FOUR bound alarms (absence/break/weekly-absence/weekly-divergence) ALL OK -- the canary is itself the guard, and its absence is alarmed. Nothing to fix. |
| etfs-canon-fanin-daily | etfs-canon-fanin | CLOSED (C9 + DDB row above). |
| opal-assets-daily-emitter-daily | opal-assets-daily-emitter | CLOSED (DDB row above). |
| mdpf-daily-refresh-trigger | mdpf-daily-trigger | OBSERVED-HELD BY DESIGN: event-pattern on the Door-6 sentinel key; fired 0/50h == the hold HOLDING. Read-only observation per the standing INF hold; a zero here is the healthy reading. |
| inf-silver-chain-bronze-complete | inf-silver-chain | OBSERVED-CONSISTENT-WITH-KNOWN-STATE: fired 2/50h -- the parquet bronze producer still runs (17a ongoing, known) and its bronze-complete events drive the silver chain. Read-only observation ONLY per the hold; no verdict beyond consistency. |

## FINDING ES-1 (GROUNDED): exec-summary-generator source tree DELETED from the repo 2026-04-27 by an unrelated log commit; deployed lambda now unrebuildable; source-map lists 15 phantom files

- git: commit 64b6b9d65 (2026-04-27, subject "log(COMP_LEARNS.session13)...") deleted the ENTIRE
  infra/aws/lambda/exec-summary-generator/ source set (lambda_function.py 455 lines, config.py,
  metrics.py, platinum_reader.py, validator.py, 6 prompt files, exec_summary/ package ~484 lines).
  `git ls-files` on the dir: ZERO tracked files today; only __pycache__ remains on disk.
- Consequence: the DEPLOYED lambda cannot be rebuilt from the repo (Rule-10-class violation state),
  and the source-map row still lists all 15 files -- map drift, files[] is a phantom census.
- The ligament (exec-summary-trigger, EVENT-pattern, opal-data-bd env) fired 0/50h -- whether the
  0 is a dead upstream (platinum write pattern never matching) or dormant-by-design needs the
  TRIGGER pattern read against bd platinum write cadence; NOT settled here.
- Same sweep-deletion family as c36710809/fbdb335b4 (a broad pathspec in an unrelated commit) --
  the class the 2026-07-14 safe-commit fix now guards against for pycache; SOURCE deletions
  swept into log commits remain possible and this one went unnoticed for 11 weeks.
- ROUTED to COO: restore-vs-decommission is an ownership call (ADVI_49EXEC lineage). Recovery is
  mechanical if wanted: `git checkout 64b6b9d65~1 -- infra/aws/lambda/exec-summary-generator/`
  then verify vs the DEPLOYED CodeSha256 before any motion.
