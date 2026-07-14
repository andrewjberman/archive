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

## FINDING NT-1 (declarative drift + stale-orphan hazard; NOT an outage)

`news-trending-analysis` env carries `S3_KEY=sentiment/keyword-sentiments.json`, but the DEPLOYED code
(source-map @ 903fbe9a8, deployed 2026-06-11) hardcodes `json/sentiment/keyword-sentiments.json`
(`lambda_function.py:1524`) and never reads that env var for the write. Measured:
- REAL key `json/sentiment/keyword-sentiments.json`: fresh (last write yesterday 21:17Z, 155,935 B). Fires 4/50h, 0 errors.
- LEGACY key `sentiment/keyword-sentiments.json`: EXISTS, frozen ~127 trading days (~2026-02). **A stale
  record says something false with authority** — any consumer still reading the old path consumes
  February data with no error. Portal consumption path check queued (comp-cache/comp-transform) before
  any cleanup ask; the delete itself is human-confirmation class regardless.
- (e) lesson, generalized: **an env var is DESIRED-ish config, not a write receipt** — this sweep's own
  method upgraded mid-pass: env-grounded surface first, code-grounding REQUIRED whenever the env surface
  reads stale before any escalation (this row would have been a false P1 otherwise).

## Method + queue state

- Verdict script (read-only): scratchpad `ligament_c_landed_bytes.py`; JSON at `ligament_c_verdicts.json`.
- 41 rows NEEDS-CODE-GROUNDING (env names bucket only): per-lambda source read → write-prefix extraction
  → listing. Priority order: client-data pipelines (bd/cot/inf/etfs/mdpf) → portal/news → monitors.
- DDB surfaces (news articles/trending, etfs-ownership-daily, others): keyed reads queued.
- Verdicts (d)/(e) fill alongside code-grounding (the write-verify + guard-property questions are answered
  at the same source read).
- INF-chain ligaments: read-only observation ONLY (standing hold; a freshness guard reading RED there is a
  guard WORKING).

**Escalations so far: none** — the one candidate (NT-1) downgraded to drift on code-grounding.
