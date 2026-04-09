# DS Briefing: `ai_commentary` field for Fear & Greed Index

**From:** 0.1.1_RD_MarketPerformance
**To:** 0.1.0_DS_MarketIntelligence
**Date:** 2026-04-08
**Re:** LLM-generated contextual commentary for Fear & Greed modal

---

## Problem

The Fear & Greed modal shows 7 component scores but no narrative context. Static methodology text says things like "below average VIX indicates market complacency" regardless of whether VIX is at 15 or 35. This led to a real incident: volatility was the *highest-scoring* (least fearful) component, but at an absolute level it was still extremely elevated. The static text implied conditions were calm when they were anything but -- the other 6 components were just worse.

**We need commentary that understands absolute levels, not just relative ranking.**

## What we need

A new optional field on the `FearGreedIndex` response:

```json
{
  "current": { ... },
  "historical": [ ... ],
  "ai_commentary": [
    "Composite score of 18 indicates Extreme Fear across all 7 indicators -- no component is in positive territory.",
    "Market Volatility (VIX at 34.2) scores highest at 28, but this is misleading -- a VIX above 30 is historically extreme. It only looks 'good' because every other indicator is worse.",
    "Safe Haven Demand is the biggest drag at 8 -- bonds are massively outperforming equities over the past 20 days, a clear flight-to-safety signal."
  ]
}
```

**Requirements:**
- 3 bullets, plain English, no jargon that needs a glossary
- Must reference absolute values (VIX level, not just "below/above average")
- Must flag when the "best" component is still objectively bad
- Must flag when the "worst" component is extreme (not just relatively low)
- Must note significant period-over-period shifts (>10pt moves in 30 days)
- No generic filler like "markets are uncertain" -- every sentence should contain a specific number

## Suggested approach

Add an LLM call to the Fear & Greed data pipeline (wherever the composite + components are assembled for S3). Pass all 7 component scores + their raw values + the composite + 30d change to GPT with a prompt like:

```
You are a market analyst writing 3 concise bullet points about today's CNN Fear & Greed Index reading. Each bullet must reference specific numbers. Never describe a value as "low" or "calm" if it is objectively elevated -- always anchor to absolute levels and historical context.

Data:
- Composite: {value} ({label})
- Components: {name}: score {score}, raw {raw_value} {unit} ...
- 30D change: {change}

Write exactly 3 bullets. No markdown formatting, no bullet prefixes.
```

## Pipeline path

The field flows through:
1. Fear & Greed data assembly Lambda (generates commentary)
2. S3 JSON artifact (stores it)
3. Portal frontend (reads `ai_commentary` array, renders as numbered insights)

## Portal status

The portal already has:
- **LLM path**: Reads `ai_commentary` from the response, renders 3 numbered bullets in the modal
- **Deterministic fallback**: Client-side heuristic bullets using component scores + absolute thresholds (already live, handles the "best component is still bad" case)

When DS ships the `ai_commentary` field, it automatically takes priority over the fallback. No portal changes needed.

## Type update needed

Once live, add to `FearGreedIndex` in `portal/src/api/endpoints/sentiment.ts`:

```ts
ai_commentary?: string[];
```

This is a shared file (outside RD scope), so DE or DT should add it.
