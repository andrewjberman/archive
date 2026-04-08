# Trending Topics: Bullet Point + Truncation Investigation
**Date:** 2026-04-08
**Agent:** 0.1.1_RD_MarketPerformance
**Requested by:** Andrew Berman (for COO routing)

---

## Executive Summary

Three issues reported with Trending Topics. All three trace to the same root cause: **the GPT prompt in Layer 3 curation generates prose paragraphs, not bullet points.** The portal rendering code is correctly written to handle bullets -- but it never receives them.

---

## Issue 1: Modal Does Not Show 3 Bullet Points

**Expected:** Clicking into a topic's drilldown modal shows 3 concise bullet points of analysis.
**Actual:** Shows a prose paragraph truncated to 2 visible lines.

**Root cause:** The `ContextBullets` component (`ExecutiveSummary.tsx:898-917`) splits `context` on `\n` and strips `- ` or `* ` prefixes. When the split produces <= 1 element (which it always does because the context has **zero newlines**), it falls back to a `<p>` tag with `line-clamp-2` (CSS 2-line truncation).

**Evidence from production S3 data** (`s3://opal-data-portal-v2/json/trending/latest.json`):
- Every `context` field is a 900-1200 char prose paragraph
- Zero newlines (`\n` count = 0 for all topics)
- Zero bullet-formatted lines (`- ` or `* ` prefix count = 0)

## Issue 2: Content Gets Truncated

**Expected:** Full analysis visible.
**Actual:** Only 2 lines visible in both the modal header and hero card.

**Root cause:** Because `ContextBullets` falls into the single-paragraph path (line 908), it renders:
```html
<p class="line-clamp-2">...900+ char paragraph...</p>
```
`line-clamp-2` is a CSS property that hard-truncates to 2 visible lines. This is the **fallback behavior** -- bullets would not be truncated this way (each bullet gets `line-clamp-1` independently, and up to 3 are shown).

## Issue 3: Preview Card Should Show First Bullet

**Expected:** `HeroTrendCard` (the #1 bullish and #1 bearish preview) shows the first bullet point.
**Actual:** Shows truncated prose.

**Root cause:** `HeroTrendCard` (line 851-896) renders `ContextBullets` with `limit={1}` (line 881), which would correctly show only the first bullet. But since the context has no newlines, the split produces 1 element = the entire paragraph, and it falls back to `<p class="line-clamp-2">`.

---

## Data Pipeline Trace

```
GPT prompt (prose)                          <-- ROOT CAUSE
  |
  v
news_layer3_curation Lambda                 (line 1346-1364)
  - Prompt: "150-200 word analysis"
  - No instruction to format as bullets
  - Output: single prose paragraph
  |
  v
DynamoDB: opal-news-trending-daily          (field: 'analysis')
  |
  v
trending-topics-portal-publisher Lambda     (line 169)
  - Maps: analysis -> context
  - No transformation or reformatting
  |
  v
S3: opal-data-portal-v2/json/trending/latest.json
  |
  v
Portal: ExecutiveSummary.tsx
  - ContextBullets splits on \n
  - Always gets 1 element (no newlines in data)
  - Always falls back to <p> with line-clamp-2
```

### Key File Paths

| Component | File | Line |
|-----------|------|------|
| GPT analysis prompt | `infra/aws/lambda/news_layer3_curation/lambda_function.py` | 1346-1364 |
| DynamoDB write | `infra/aws/lambda/news_layer3_curation/lambda_function.py` | 1493 |
| Publisher mapping (analysis -> context) | `infra/aws/lambda/v2_portal/01_market_overview/lambdas/trending-topics-portal-publisher/lambda_function.py` | 169 |
| ContextBullets renderer | `portal/src/components/market-performance/ExecutiveSummary.tsx` | 898-917 |
| HeroTrendCard (preview, limit=1) | `portal/src/components/market-performance/ExecutiveSummary.tsx` | 881 |
| DrilldownModal header (limit=default 3) | `portal/src/components/market-performance/ExecutiveSummary.tsx` | 720 |

---

## Recommended Fix (for COO to authorize)

**Option A: Fix the prompt (upstream, preferred)**
Change the GPT prompt in `news_layer3_curation` (line 1346-1364) to request 3 bullet points instead of a prose paragraph:

```
"analysis": "3 concise bullet points (each 1-2 sentences) explaining the {sentiment_direction} market implications. Format as:\n- Bullet 1\n- Bullet 2\n- Bullet 3\nFocus on affected sectors, potential price movements, and investment considerations."
```

This is the cleanest fix because:
- The portal rendering code already handles this format correctly
- No portal changes needed
- All downstream consumers (modal, hero card, regular cards) immediately work
- Next Lambda deployment + pipeline run populates correct format

**Option B: Fix in the publisher (midstream)**
Add a post-processing step in `trending-topics-portal-publisher` (line 169) that calls a small LLM or regex to reformat prose into 3 bullets. More complex, more fragile.

**Option C: Fix in the portal (downstream, band-aid)**
Remove `line-clamp-2` from the fallback `<p>` in `ContextBullets` and increase visible lines. This doesn't solve the "3 discrete bullet points" requirement -- just shows more of the paragraph.

**Recommendation:** Option A. Single line change in the prompt. DS owns `news_layer3_curation`. Requires a Terraform deploy of the Lambda after commit.

---

## Notes

- `image_url` field is also `MISSING` on all topics in production. This was added by MKOV_TRENDS.003 (DS task) but the publisher at line 169 does not map it from DynamoDB. Separate issue, flagging for awareness.
