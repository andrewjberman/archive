# OPAL_ANALYST TO-4d Stage 1 — News census complete findings (/draw)

**To:** 0.0.0_AB_MSTR~Z · cc 2.0.0_SA_COO~Z
**From:** 0.5.0_AE_OpalETL~Z · 2026-08-10
**Census:** `ARTIFACT_CENSUS_NEWS.yaml` @ddd918d8c (vertical 4, completes the four-vertical baseline)
**Scope authority:** Q7 = Option C union, Andrew-direct ("C on this call", record @1624238b3); Stage-0 proposal @a263a0ad6. ALL evidence first-hand (COO discipline flag honored).

```
NEWS VERTICAL — served news-derived artifacts, two planes per the Q7 Option-C ruling

1. The build plane — how news becomes served artifacts (S3 plane + DDB plane, one chain)

   INGEST                 ENRICH                  CURATE/AGGREGATE            SERVED STORE
   ──────                 ──────                  ────────────────            ────────────
  ┌──────────────────┐   articles    ┌─────────────────────┐   scored rows
  │ news-ingestion-  │ ────────────► │ finbert-batch-      │ ─────────────┐
  │ scheduler        │  NewsAPI+RSS  │ processor →         │  writeback   │
  │ (crons ENABLED)  │  ~350-585/day │ opal-news-ai-       │  in-place    │
  ├──────────────────┤               │ sentiment (FinBERT) │              ▼
  │ seeking-alpha    │   articles    │ (crons ENABLED)     │   ┌─────────────────────────┐
  │ news+analysis    │ ────────────► └─────────────────────┘   │ DDB opal-news-articles  │
  │ chains (crons    │  daily 14:00Z/21:00Z                    │ 303,603 items LIVE      │
  │ ENABLED; dedup   │                                         │ 2026-08-10; QUERY by    │
  │ ledger 50,648)   │                                         │ article_date ONLY       │
  └──────────────────┘                                         └────────────┬────────────┘
                                                                7-day window│reads
                                            ┌───────────────────────────────┤
                                            ▼                               ▼
                              ┌──────────────────────┐        ┌──────────────────────────┐
                              │ news-trending-       │        │ opal-news-layer3-        │
                              │ analysis (Layer 2,   │ ──────►│ curation (GPT-4o)        │
                              │ cron ENABLED         │ report │ → DDB opal-news-         │
                              │ 11:15/21:15Z)        │        │ trending-daily 4,537     │
                              └──────────┬───────────┘        │ LIVE; 20 items/day       │
                                         │ writes S3          └──────────┬───────────────┘
                                         ▼                               │ writes S3 (1s apart,
   ┌─────────────────────────────────────────────────┐                   │ producer INFERRED)
   │ S3 opal-data-portal-v2 (SERVED, all live today) │◄──────────────────┘
   │  json/sentiment/keyword-sentiments.json 21:16Z  │
   │  json/trending/latest.json            21:17Z    │   ┌── SEPARATE feed ──┐
   │  json/sentiment/fear-greed-index.json 14:30Z ◄──┼── │ opal-portal-fear- │
   │                                                 │   │ greed-fetcher     │
   │  FROZEN residue (04-07, producer cron DISABLED):│   │ (CNN API, cron    │
   │  keyword-history-summary/{kw}   360 keys        │   │ 14:30/21:30Z)     │
   │  keyword-history-articles/{kw}  360 keys        │   └───────────────────┘
   └─────────────────────────────────────────────────┘
   DEAD LEG: keyword-intelligence-generator (cron DISABLED, chained after the frozen
   drilldown) → DDB opal-keyword-intelligence 2,892 items LIVE but EMPTY for every
   currently-trending keyword (exercised 2/2 → 0 items; newest item seen 2026-02-23)

2. The query plane — how a portal user reaches news-derived data (/market, the default route)

    YOU (portal, "/" → /market "Market Overview")
        │
        ├─► Panel "Trending Topics" (ExecutiveSummary.tsx:264)
        │      GET /api/general/trending/latest.json (15-min cache)
        │      ◄── 10 bullish + 10 bearish GPT topics, per-topic article rows
        │      click topic → modal renders from the SAME artifact (no 2nd fetch)
        │
        ├─► Panel "Daily Cloud" (SentimentGauge.tsx:130, TopicCloud)
        │      GET /api/general/sentiment/keyword-sentiments.json (30-min refetch)
        │      ◄── 44 ranked keywords, FinBERT-colored, sized by count
        │      click keyword → KeywordSentimentModal
        │          POST /v1/sentiment/keyword-intelligence {keyword}
        │          ◄── ✗ EMPTY for today's keywords (dead leg above) — the one
        │              broken user path in the vertical, exercised live
        │
        └─► Panel "Fear & Greed" (SentimentGauge.tsx:169, gauge)
               GET /api/general/sentiment/fear-greed-index.json (5-min refetch)
               ◄── value 65.71 "greed" + 7 components + 249-day history
               click gauge → FearGreedModal (same artifact, 2nd queryKey — smell)

    CONCIERGE plane (catalog row 5 — the panel-less serving surface, Q7 Plane 2):
    portal_lookup.py ddb-query {table} {hash-value}   QUERY-only, scans refused
        opal-news-articles        by article_date    opal-news-trending-daily  by date
        opal-keyword-intelligence by keyword (+GSI)  seeking-alpha-article-urls by run_date

   ANSWER back in your terminal: "585 articles ingested today, FinBERT-scored;
   20 GPT topics curated 21:17Z; the gauge reads 65.71 greed as of 14:30Z —
   and the keyword drilldown modal is serving EMPTY intelligence."

  The Q7 "two planes, one census" model is exact and deliberate:
  ┌─────────────────────────┬──────────────────────────────────────────────────┐
  │  Visual plane (grammar) │  ddb_sources plane (residue-section pattern)     │
  ├─────────────────────────┼──────────────────────────────────────────────────┤
  │ page→location→panel→    │ table→query_pattern→item_schema→lineage          │
  │  artifact→field         │  (query patterns stand in for panels)            │
  │ anchored /market        │ anchored portal_lookup catalog row 5             │
  │ 3 canonical S3 types    │ 4 active tables + 2 dormant, state-marked        │
  │ vintage per artifact    │ item counts LIVE-stamped 2026-08-10, never quoted│
  │ news OWNS these rows    │ future market-overview census POINTS here        │
  └─────────────────────────┴──────────────────────────────────────────────────┘
```

## Findings (complete, zero elision)

**F1 — FROZEN drilldown chain, exercised on the live user path (the load-bearing finding).**
Both keyword-history families (720 of the 722 sentiment keys) are frozen — LastModified
range 2026-01-05..2026-04-07 (COMPLETE listings, rail-checked) — and
`opal-keyword-intelligence` holds ZERO items for currently-trending keywords ('fund
commentaries', 'cyclospora salad fears' → 0 items each; newest item seen `generated_date`
2026-02-23). Mechanism (INFERRED, cron facts per comp-estate): the drilldown generator and
intelligence generator crons are DISABLED, documented as "chained after trending-analysis" —
the chain evidently does not fire. Net user impact: **KeywordSentimentModal opens EMPTY for
every keyword a user can actually click today.** Per the moratorium + TRIGGER_LAYER doctrine
this lands as a FINDING routed to owners — no monitor built, no fix dispatched (portal-lane
+ pipeline-lane, not mine).

**F2 — The history families are also ORPHANED at HEAD.** `getKeywordSentimentHistorySummary/
Articles` (sentiment.ts:614+) have ZERO component callers (first-hand grep over src/).
comp-estate's frontend claim ("consumed by KeywordSentimentModal.tsx") is STALE at HEAD —
the modal fetches keyword-intelligence only. So even un-freezing the producer would today
serve 720 keys nobody renders.

**F3 — Trending is served from S3-static, not DDB-via-proxy; the in-code producer comment
is stale.** ExecutiveSummary fetches `getTrendingTopicsStatic` → `/api/general/trending/
latest.json`; the comment at ExecutiveSummary.tsx:105 names `opal-trending-topics-portal-
publisher` as the writer, but that lambda's crons are ALL DISABLED — while latest.json was
written 1s after the layer3 DDB rows (21:17:19Z DDB / 21:17:20Z S3). Producer = the
trending-analysis/layer3 chain (INFERRED from timing; not source-confirmed — I did not read
the lambda source). comp-estate's "trending.ts reads opal-news-trending-daily" frontend leg
is likewise stale at HEAD.

**F4 — Fourth vintage-regime variant.** trending/latest.json carries THREE vintage stamps
(`generated_at` + `data_as_of` + `date`); the sentiment artifacts stamp `generated_at` only.
Extends the TO-4b/4c registry finding (data_as_of / provenance-block / as_of → + this).

**F5 — Dead endpoint definitions over absent keys.** `articles.json` and `aaii-history.json`
are fetched by defined endpoint fns (one zero-caller, one commented-out caller) but ABSENT
from the COMPLETE 722-key walk — dead code over dead keys, banked as portal-lane smell.

**F6 — Count-drift honesty (the ruling's own boundary, exercised).** Live describe-table
2026-08-10: articles 303,603 (vs 298,417 quoted 08-06, 233,159 quoted 07-30), trending
4,537, intelligence 2,892, SA-urls 50,648 (exactly the 08-06 prior — unmoved),
semantic 113 + market-updates 1 (dormant). SA-urls recent-partition probes (08-08..10,
news+analysis suffixes) returned 0 items — key-format/recency question BANKED, not
adjudicated.

**Smells banked (portal-lane, untouched under exclusivity):** duplicate fear-greed fetch
under two queryKeys; stale producer comment (F3); dead endpoints (F5); silent fallback
data on fear-greed fetch error (sentiment.ts:125-134 fabricates value 50 "Fallback data").

## Five-rule self-score: 5/5

1. **Untitled panels carry component names** — KeywordSentimentModal + FearGreedModal rows. PASS
2. **Dedup pointers, never re-census** — FearGreedModal → canonical "Fear & Greed"; ddb
   intelligence row → canonical ddb_sources; non-news panels on /market excluded with the
   ownership boundary stated in the page comment. PASS
3. **Denominator before rows** — 722-key + 1-key COMPLETE walks + 6 DDB tables stated in
   header; every ddb-query result carries the tool's own DENOMINATOR line. PASS
4. **Vintage with every figure** — every retrieval row stamps bytes + vintage + read date;
   DDB counts stamped LIVE 2026-08-10 per the ruling's binding boundary. PASS
5. **Evidence per row, first-hand** — portal_lookup COMPLETE reads + component file:line
   read by the census author; zero subagent evidence. PASS

## Program state

Vertical 4 of 4 complete — the four-vertical baseline (MP @0c1dae3da, Pod-2 @49cb88ead,
Macro @5efce36b7, News @ddd918d8c) is DONE pending COO validation + Andrew review. Next
per the plan: Andrew's semantic pass + DATA_CATALOG v0.2 (Steps 3-6, not my dispatch to
assume).
