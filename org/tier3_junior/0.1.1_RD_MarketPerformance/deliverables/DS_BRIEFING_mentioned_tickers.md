# DS Briefing: `mentioned_tickers` field for Trending Topics

**From:** 0.1.1_RD_MarketPerformance
**To:** 0.1.0_DS_MarketIntelligence
**Date:** 2026-04-08
**Re:** New field request for Layer 3 trending topic narratives

---

## What we need

A new optional field on each trending topic narrative:

```
mentioned_tickers: string[]   // e.g. ["AMZN"], ["NVDA", "MSFT"], []
```

**Max 3 tickers per topic.** Only include tickers that are a primary subject of the narrative -- not every stock mentioned in passing across 12 articles. If a topic is macro ("Fed rate pause", "bond yields stabilize"), return an empty array. Do not force a ticker onto every topic.

## Where it goes

The field should be added to each bullish/bearish narrative object in the Layer 3 curation output, alongside the existing fields:

```json
{
  "topic": "Amazon cloud revenue surprises to the upside",
  "context": "- AWS revenue grew 19% YoY...\n- ...",
  "article_count": 8,
  "sentiment_bull_bear": 0.42,
  "top_sources": ["Reuters", "Bloomberg"],
  "image_url": "https://...",
  "mentioned_tickers": ["AMZN"]     // <-- new field
}
```

## Extraction approach

This should come from the GPT curation prompt in `semantic-news-layer3-curation`. The model already reads every article and synthesizes the narrative -- just ask it to also return the 0-3 most relevant tickers in the structured output. No separate NER pass needed.

Suggested addition to the curation prompt's output schema:

```
"mentioned_tickers": {
  "type": "array",
  "items": { "type": "string" },
  "description": "0-3 stock tickers (e.g. AMZN, NVDA) that are primary subjects of this narrative. Empty array for macro/sector topics.",
  "maxItems": 3
}
```

## Portal pipeline

The field flows through:
1. `semantic-news-layer3-curation` Lambda (generates it)
2. DynamoDB `opal-news-trending-daily` table (stores it)
3. `semantic-trending-topics-portal-publisher` Lambda (passes it through to S3 JSON)
4. Portal frontend (reads it)

Step 3 already does `parsed.get('image_url', '')` -- just add `parsed.get('mentioned_tickers', [])` in the same block.

Step 4 is already wired: the portal reads `mentioned_tickers` dynamically and renders ticker bubbles on the trend cards and in the drilldown modal header. No portal changes needed once the data is live.

## Why

The trending topic cards on Market Overview currently show: topic name, article count, sentiment arrow. Adding a ticker bubble (e.g. `AMZN`) gives immediate context about what stock is moving without reading the headline. The drilldown modal also shows up to 3 tickers in the upper right. Both are already coded and waiting for the data.

## Type update needed

Once the field is live, `TrendingTopic` in `portal/src/api/endpoints/market.ts` should get:

```ts
mentioned_tickers?: string[];
```

This is a shared file (outside RD scope), so DE or DT should add it. The portal currently reads the field via dynamic access so it will work before the type is updated, but the type should be formalized.
