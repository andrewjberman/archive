# OPAL_ANALYST TO-4d Stage 0 — News DDB census SCOPE PROPOSAL (per-option denominators)

**To:** 1.0.0_SA_CTO~Z (grammar owner; carries to Andrew via MSTR~Z) · cc 2.0.0_SA_COO~Z
**From:** 0.5.0_AE_OpalETL~Z · 2026-08-10
**Authority:** TO-4d Stage 0 (Andrew's own open-question design: *"News is the most
broad/abstract one which we will need to consider how to scope"* @6c1161075)

## The scoping problem, grounded

News differs from verticals 1-3 in TWO structural ways (comp-estate news thread: 13 chains,
10 in-scope; PORTAL_RETRIEVAL news-DDB census; all first-hand):

1. **No dedicated portal page.** News-derived data renders inside the Market Overview
   surface's components (SentimentGauge, FearGreedModal, KeywordSentimentModal,
   trending/TopicCloud, ExecutiveSummary — per comp-estate frontend legs), not on a /news
   route. The visual-first grammar has no home page to anchor on.
2. **A serving surface with NO panels at all:** catalog row 5 serves the news DDB tables
   directly through portal_lookup ddb-query — the concierge's own product surface, with
   query patterns where verticals 1-3 had panels. The grammar's `source_type: ddb` exists
   (PRD 8.1 skeleton) but every censused artifact so far anchored to a panel.

## The options, each with its denominator

| Option | Scope rule | Denominator (measured/named today) | What it misses |
|---|---|---|---|
| **A — rendered-panels only** (strict grammar fidelity) | Census only news-derived artifacts a portal panel renders | S3: json/sentiment/ 722 keys (fear-greed-index, keyword-sentiments, keyword-history-summary/{kw}, keyword-history-articles/{kw}) + json/trending/latest.json = ~723 S3 keys; 2 DDB-backed API routes (POST /v1/sentiment/keyword-intelligence; trending via data-proxy -> opal-news-trending-daily) | The concierge's OWN serving mechanism (catalog row 5 DDB queries) — the product this program exists for; also the upstream tables entirely |
| **B — catalog-serving only** (concierge-first) | Census the 4 DDB tables as artifacts; field grain = item schema; "panel" replaced by QUERY PATTERN | 4 active tables: opal-news-articles (~298k items, QUERY-by-article_date only), opal-news-trending-daily (3,428), opal-keyword-intelligence (1,772), seeking-alpha-article-urls (50,648) + 2 dormant (semantic-news-trending-daily, market-updates empty) | Every rendered sentiment/trending artifact — and it breaks the ratified visual-first grammar (no page/location/panel levels at all) |
| **C — union, two planes (RECOMMENDED)** | Visual plane per the ratified grammar for rendered news-derived artifacts (anchored on the Market Overview page, dedup pointers if that vertical is ever censused) + a labeled `ddb_sources` section (pilot residue-section pattern) for the 4 tables with query patterns + item schemas + lineage (articles -> FinBERT -> trending/keyword artifacts) | ~723 S3 keys + 4 active DDB tables (+2 dormant, state-marked) + 2 API routes | Nothing served; costs the largest Stage-1 effort (est. still < TO-4b) |

## Recommendation: **Option C**, with two scope boundaries named

- **Ownership boundary:** news OWNS news-DERIVED artifacts wherever they render (sentiment/
  trending on Market Overview); a future market-overview census points at these entries
  rather than re-censusing (dedup rule 2 across verticals).
- **Grammar mechanics:** no new level invented — the `ddb_sources` section reuses the
  ratified residue-section pattern (a labeled top-level section outside `pages`), each
  table carrying `source_type: ddb`, its sanctioned query pattern (QUERY-only discipline
  from the build stands; scans refused), item schema as fields, and item-count denominator
  with the count's own vintage.
- **Item-count honesty:** DDB counts drift daily (298,417 per PORTAL_RETRIEVAL 08-06 vs
  233,159 per the estate snapshot 07-30 for opal-news-articles) — Stage 1 stamps LIVE
  describe-table counts with their read date, never a quoted prior.

Per Andrew's design this proposal HOLDS for the scope word (his gate, not manufactured).
Stage 1 (ARTIFACT_CENSUS_NEWS.yaml + /draw) proceeds immediately on the ruling; the ruled
scope will be cited in the census header.
