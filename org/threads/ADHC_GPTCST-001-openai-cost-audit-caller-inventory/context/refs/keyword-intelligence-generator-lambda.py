"""
Keyword Intelligence Generator
================================

Pre-computes GPT-4o-mini keyword intelligence analysis for every keyword in the
Daily Cloud TopicCloud, storing results in DynamoDB for instant portal modal loads.

Runs 2x daily at 2:50 PM and 9:50 PM ET — 20 minutes after news-trending-analysis
writes keyword-sentiments.json, 10 minutes after keyword-drilldown-generator.

Input:
  - s3://opal-data-portal-v2/json/sentiment/keyword-sentiments.json
  - opal-news-articles DynamoDB table (7-day window, same as TopicCloud)

Output:
  - opal-keyword-intelligence DynamoDB table
    PK: keyword (String, lowercase)
    SK: generated_date (String, YYYY-MM-DD)
    Attributes: full intelligence response (same schema as POST /v1/sentiment/keyword-intelligence)

Behaviour:
  - Idempotent: skips keywords already written for today (safe to re-run)
  - Continues on per-keyword errors (one bad keyword never aborts the batch)
  - OpenAI key cached at module level across warm invocations

Schedule: cron(50 14,21 * * ? *)  — 9:50 AM and 4:50 PM ET daily
"""

import json
import re
import os
from datetime import datetime, timedelta, timezone
from decimal import Decimal, InvalidOperation

import boto3
from boto3.dynamodb.conditions import Key

# ============================================================================
# CONFIGURATION
# ============================================================================

S3_BUCKET_PORTAL    = os.environ.get('S3_BUCKET_PORTAL', 'opal-data-portal-v2')
ARTICLES_TABLE      = os.environ.get('ARTICLES_TABLE', 'opal-news-articles')
INTELLIGENCE_TABLE  = os.environ.get('INTELLIGENCE_TABLE', 'opal-keyword-intelligence')
OPENAI_SECRET       = os.environ.get('OPENAI_SECRET', 'opal/openai/news-trending')
KEYWORDS_S3_KEY     = 'json/sentiment/keyword-sentiments.json'
DAYS_BACK           = 7
# Match the TopicCloud .slice(0, 20) in TopicCloud.tsx — only the visible keywords
MAX_KEYWORDS        = int(os.environ.get('MAX_KEYWORDS', '20'))

# ============================================================================
# AWS CLIENTS  (reused across warm invocations)
# ============================================================================

s3         = boto3.client('s3', region_name='us-east-1')
dynamodb   = boto3.resource('dynamodb', region_name='us-east-1')
articles_t = dynamodb.Table(ARTICLES_TABLE)
intel_t    = dynamodb.Table(INTELLIGENCE_TABLE)

# ============================================================================
# OPENAI  (optional — only used if available)
# ============================================================================

try:
    from openai import OpenAI as _OpenAI
    _OPENAI_AVAILABLE = True
except ImportError:
    _OPENAI_AVAILABLE = False
    _OpenAI = None

_OPENAI_API_KEY_CACHE = None   # cached across warm invocations


def _get_openai_api_key() -> str:
    """Fetch OpenAI key from Secrets Manager, cached at module level."""
    global _OPENAI_API_KEY_CACHE
    if _OPENAI_API_KEY_CACHE:
        return _OPENAI_API_KEY_CACHE
    try:
        sm = boto3.client('secretsmanager', region_name='us-east-1')
        resp = sm.get_secret_value(SecretId=OPENAI_SECRET)
        secret = resp.get('SecretString', '{}')
        try:
            parsed = json.loads(secret)
            key = parsed.get('api_key') or parsed.get('key') or secret
        except json.JSONDecodeError:
            key = secret
        _OPENAI_API_KEY_CACHE = key
        return key
    except Exception as e:
        print(f"[kig] Error fetching OpenAI key: {e}")
        return None


# ============================================================================
# HELPERS
# ============================================================================

def _sentiment_label(score: float) -> str:
    if score >= 0.15:  return 'Bullish'
    if score >= 0.05:  return 'Slightly Bullish'
    if score > -0.05:  return 'Neutral'
    if score > -0.15:  return 'Slightly Bearish'
    return 'Bearish'


def _to_decimal(val):
    """Convert float/int to Decimal for DynamoDB storage."""
    if isinstance(val, float):
        return Decimal(str(round(val, 6)))
    if isinstance(val, int):
        return Decimal(val)
    return val


def _convert_for_dynamo(obj):
    """Recursively convert floats to Decimal for DynamoDB put_item."""
    if isinstance(obj, dict):
        return {k: _convert_for_dynamo(v) for k, v in obj.items()}
    if isinstance(obj, list):
        return [_convert_for_dynamo(i) for i in obj]
    if isinstance(obj, float):
        return _to_decimal(obj)
    return obj


def _convert_from_dynamo(obj):
    """Recursively convert Decimal back to float when reading from DynamoDB."""
    if isinstance(obj, dict):
        return {k: _convert_from_dynamo(v) for k, v in obj.items()}
    if isinstance(obj, list):
        return [_convert_from_dynamo(i) for i in obj]
    if isinstance(obj, Decimal):
        return float(obj)
    return obj


# ============================================================================
# WEB SEARCH ENRICHMENT
# ============================================================================

def _web_search_enrich(client, keyword: str, analysis: dict, today: str) -> dict:
    """
    Run a today-focused web search to enrich the internal article analysis.

    Strategy:
      1. Use the key drivers + sentiment pattern already found to generate
         2 precise, date-anchored search queries (not generic — specific to
         the themes the article analysis identified).
      2. Run each query through OpenAI's web_search_preview tool, explicitly
         instructed to return only today's context (or very recent context
         directly relevant to the identified themes).
      3. Return a dict with 'queries' (list) and 'summary' (str) for the
         synthesis step. Returns empty dict on any failure.

    The caller is responsible for synthesis — this function only retrieves.
    """
    try:
        # --- Step 4a: generate targeted queries from what we already know ---
        driver_themes = ', '.join(
            d.get('title', '') for d in analysis.get('key_drivers', [])[:3]
        ).strip()

        # Check if a signal conflict was detected earlier
        signal_conflict = analysis.get('signal_conflict')
        has_conflict = signal_conflict and signal_conflict.get('detected')

        if has_conflict:
            query_prompt = f"""A financial intelligence analysis of the keyword "{keyword}" found CONFLICTING signals:
- Bullish articles about: {signal_conflict.get('bull_case', 'positive developments')[:150]}
- Bearish articles about: {signal_conflict.get('bear_case', 'negative developments')[:150]}
- Headline: {analysis.get('headline_summary', '')[:200]}

Generate exactly 2 web search queries that explain WHY the market reacted the way it did despite the conflicting data about "{keyword}" TODAY ({today}).
Focus on finding resolution — which side is winning and why.
Return a JSON object: {{"queries": ["query1", "query2"]}}"""
        else:
            query_prompt = f"""A financial intelligence analysis of the keyword "{keyword}" found:
- Sentiment pattern: {analysis.get('sentiment_pattern', 'unknown')}
- Key themes from articles: {driver_themes or 'general market coverage'}
- Headline: {analysis.get('headline_summary', '')[:200]}

Generate exactly 2 web search queries to find what happened with "{keyword}" TODAY ({today}).
Each query should be specific — not generic. Anchor them to TODAY and the exact themes above.
Avoid queries that would return old/historical results (no "history of", "what is", "explained").
Return a JSON object: {{"queries": ["query1", "query2"]}}"""

        q_resp = client.chat.completions.create(
            model='gpt-4o-mini',
            messages=[{'role': 'user', 'content': query_prompt}],
            response_format={'type': 'json_object'},
            temperature=0.1,
            max_tokens=150,
        )
        queries = json.loads(q_resp.choices[0].message.content).get('queries', [])[:2]
        if not queries:
            return {}

        print(f"[kig] Web search queries for '{keyword}': {queries}")

        # --- Step 4b: run each query, collect raw web context ---
        raw_results = []
        for query in queries:
            try:
                search_resp = client.responses.create(
                    model='gpt-4o-mini',
                    tools=[{'type': 'web_search_preview'}],
                    input=(
                        f"Search for news about: {query}\n\n"
                        f"TODAY is {today}. Return ONLY information from today or the last 48 hours. "
                        f"If nothing significant happened today specifically, say so briefly. "
                        f"Do not pad with background history. 3-5 sentences maximum."
                    ),
                )
                # Extract text from response output items
                for item in search_resp.output:
                    if getattr(item, 'type', None) == 'message':
                        for block in (getattr(item, 'content', None) or []):
                            text = getattr(block, 'text', None)
                            if text:
                                raw_results.append(text.strip())
                                break
            except Exception as e:
                print(f"[kig] Web search call failed for query '{query}': {e}")
                continue

        if not raw_results:
            return {}

        combined = '\n\n'.join(raw_results)
        return {'queries': queries, 'summary': combined}

    except Exception as e:
        print(f"[kig] _web_search_enrich failed for '{keyword}': {e}")
        return {}


# ============================================================================
# CORE INTELLIGENCE LOGIC
# (extracted verbatim from portal_data_proxy get_keyword_intelligence)
# ============================================================================

def _build_conflict_prompt_section(conflict: dict) -> str:
    """Build the conflict analysis section to inject into the GPT prompt."""
    bull_lines = []
    for a in conflict['bullish_articles'][:5]:
        score = a.get('sentiment_finbert', 0)
        bull_lines.append(f"  - {a['title']} ({score:+.2f})")
    bear_lines = []
    for a in conflict['bearish_articles'][:5]:
        score = a.get('sentiment_finbert', 0)
        bear_lines.append(f"  - {a['title']} ({score:+.2f})")

    return f"""
⚠ SIGNAL CONFLICT DETECTED
Strongly bullish articles (score > +0.4):
{chr(10).join(bull_lines)}

Strongly bearish articles (score < -0.4):
{chr(10).join(bear_lines)}

Your analysis MUST:
- Explain what the bulls are seeing vs what the bears are seeing
- Identify the specific data points driving each side
- Explain which thesis the market is pricing in and why
- Include a "signal_conflict" field in your JSON output with:
  {{ "detected": true, "bull_case": "...", "bear_case": "...", "resolution": "..." }}

"""


def _detect_signal_conflict(articles: list) -> dict:
    """
    Partition articles into strongly bullish / strongly bearish.
    If BOTH sets are non-empty, a signal conflict exists.
    Pure Python — no API call.
    """
    bullish = [a for a in articles
               if a.get('sentiment_finbert') is not None and a['sentiment_finbert'] > 0.4]
    bearish = [a for a in articles
               if a.get('sentiment_finbert') is not None and a['sentiment_finbert'] < -0.4]
    return {
        'detected': len(bullish) > 0 and len(bearish) > 0,
        'bullish_articles': bullish,
        'bearish_articles': bearish,
    }


def compute_keyword_intelligence(keyword: str, kw_metadata: dict) -> dict:
    """
    Run the full article-fetch + GPT analysis for one keyword.
    Returns the payload dict (NOT a cors_response wrapper) or raises on failure.

    kw_metadata: the entry from keyword-sentiments.json for this keyword
                 (has sentiment, count, bullish, bearish, neutral)
    """
    keyword_lower = keyword.lower().strip()
    avg_sentiment  = float(kw_metadata.get('sentiment', 0))
    bullish_count  = int(kw_metadata.get('bullish', 0))
    bearish_count  = int(kw_metadata.get('bearish', 0))
    neutral_count  = int(kw_metadata.get('neutral', 0))

    # ------------------------------------------------------------------
    # Step 1: Fetch matching articles
    #
    # Fast path — use pre-fetched cluster articles if the keyword-sentiments
    # entry already has them (cluster-based topics from embed_and_cluster_topics).
    # Regex scan path is kept for legacy single-word keyword entries that have
    # no pre-fetched articles.
    # ------------------------------------------------------------------
    all_articles = []
    by_date = {}

    prefetched = kw_metadata.get('articles', [])

    if prefetched:
        # --- Cluster / fast path: articles come from the trending report ---
        print(f"[kig] Using {len(prefetched)} pre-fetched articles for '{keyword}'")
        for a in prefetched:
            sentiment_raw = a.get('sentiment_finbert')
            sentiment_val = None
            if sentiment_raw is not None:
                try:
                    f = float(sentiment_raw)
                    if f != 0.0:
                        sentiment_val = f
                except (ValueError, TypeError):
                    pass

            pub = a.get('published', '')
            # Derive date bucket for by_date (YYYY-MM-DD prefix of ISO timestamp)
            date_bucket = pub[:10] if pub else datetime.now(timezone.utc).strftime('%Y-%m-%d')

            all_articles.append({
                'title':             a.get('title', ''),
                'source':            a.get('source', ''),
                'url':               a.get('url', ''),
                'published':         pub,
                'sentiment_finbert': round(sentiment_val, 4) if sentiment_val is not None else None,
                'summary':           a.get('summary', ''),
                '_date':             date_bucket,
            })
            if sentiment_val is not None:
                by_date.setdefault(date_bucket, []).append(sentiment_val)

    else:
        # --- Legacy path: regex scan against DynamoDB opal-news-articles ---
        kw_pattern = re.compile(r'\b' + re.escape(keyword_lower) + r'\b')

        for days_ago in range(DAYS_BACK):
            check_date = (datetime.now(timezone.utc) - timedelta(days=days_ago)).strftime('%Y-%m-%d')
            day_sentiments = []

            try:
                resp = articles_t.query(
                    KeyConditionExpression=Key('article_date').eq(check_date),
                    ProjectionExpression='title, sentiment_finbert, #src, #u, published, summary',
                    ExpressionAttributeNames={'#u': 'url', '#src': 'source'}
                )
                day_articles = resp.get('Items', [])
                while 'LastEvaluatedKey' in resp:
                    resp = articles_t.query(
                        KeyConditionExpression=Key('article_date').eq(check_date),
                        ProjectionExpression='title, sentiment_finbert, #src, #u, published, summary',
                        ExpressionAttributeNames={'#u': 'url', '#src': 'source'},
                        ExclusiveStartKey=resp['LastEvaluatedKey']
                    )
                    day_articles.extend(resp.get('Items', []))
            except Exception as e:
                print(f"[kig] DynamoDB error for {check_date}: {e}")
                day_articles = []

            for article in day_articles:
                title = (article.get('title') or '').lower()
                if not kw_pattern.search(title):
                    continue

                sentiment_raw = article.get('sentiment_finbert')
                sentiment_val = None
                if sentiment_raw is not None:
                    try:
                        f = float(sentiment_raw)
                        if f != 0.0:
                            sentiment_val = f
                            day_sentiments.append(f)
                    except (ValueError, TypeError):
                        pass

                all_articles.append({
                    'title':             article.get('title') or '',
                    'source':            article.get('source') or '',
                    'url':               article.get('url') or '',
                    'published':         article.get('published') or check_date,
                    'sentiment_finbert': round(sentiment_val, 4) if sentiment_val is not None else None,
                    'summary':           article.get('summary') or '',
                    '_date':             check_date,
                })

            by_date[check_date] = day_sentiments

    all_articles.sort(key=lambda a: a.get('published', ''), reverse=True)
    article_count = len(all_articles)

    # ------------------------------------------------------------------
    # Step 2: Build daily breakdown oldest → newest
    # ------------------------------------------------------------------
    daily_breakdown = []
    for days_ago in range(DAYS_BACK - 1, -1, -1):
        date_str = (datetime.now(timezone.utc) - timedelta(days=days_ago)).strftime('%Y-%m-%d')
        sentiments = by_date.get(date_str, [])
        daily_breakdown.append({
            'date':          date_str,
            'article_count': len(sentiments),
            'avg_sentiment': round(sum(sentiments) / len(sentiments), 4) if sentiments else None,
        })

    # ------------------------------------------------------------------
    # Fallback: no matching articles
    # ------------------------------------------------------------------
    if article_count == 0:
        return {
            'keyword':             keyword,
            'sentiment_score':     avg_sentiment,
            'sentiment_label':     _sentiment_label(avg_sentiment),
            'sentiment_pattern':   'low_confidence',
            'pattern_explanation': 'No matching articles found in the 7-day window.',
            'headline_summary':    (
                f'Insufficient data to analyze sentiment for "{keyword}" in the current '
                f'7-day window.'
            ),
            'key_drivers':         [],
            'counterarguments':    'Insufficient article coverage to identify counterarguments.',
            'confidence':          'low',
            'confidence_reason':   'No matching articles found.',
            'article_count':       0,
            'articles':            [],
            'generated_at':        datetime.utcnow().isoformat() + 'Z',
        }

    # ------------------------------------------------------------------
    # Step 2b: Detect signal conflict (divergent bullish/bearish articles)
    # ------------------------------------------------------------------
    conflict = _detect_signal_conflict(all_articles)

    # ------------------------------------------------------------------
    # Step 3: GPT-4o-mini analysis
    # ------------------------------------------------------------------
    if not _OPENAI_AVAILABLE:
        raise RuntimeError('OpenAI package not available in Lambda environment')

    api_key = _get_openai_api_key()
    if not api_key:
        raise RuntimeError('OpenAI API key not available from Secrets Manager')

    article_lines = []
    for a in all_articles[:40]:
        score_str = f"{a['sentiment_finbert']:+.2f}" if a.get('sentiment_finbert') is not None else 'N/A'
        pub = (a.get('published') or '')[:10]
        summary_snippet = (a.get('summary') or '')[:300]
        line = f"{a['title']} | {a.get('source','?')} | {pub} | {score_str}"
        if summary_snippet:
            line += f" | {summary_snippet}"
        article_lines.append(line)

    trend_lines = [
        f"{d['date']}: {d['article_count']} articles, avg {d['avg_sentiment']:+.3f}"
        for d in daily_breakdown
        if d['article_count'] > 0 and d['avg_sentiment'] is not None
    ]

    prompt = f"""You are a financial intelligence analyst summarizing market news sentiment for a portfolio manager.

KEYWORD: {keyword}
SENTIMENT SCORE: {avg_sentiment:+.3f}  (scale: -1.0 bearish → +1.0 bullish)
ARTICLE BREAKDOWN: {bullish_count} bullish / {bearish_count} bearish / {neutral_count} neutral (of {article_count} total matching articles)

DAILY TREND (oldest → newest):
{chr(10).join(trend_lines) if trend_lines else 'No daily trend data available'}

ARTICLES (title | source | date | finbert_score | summary_excerpt):
{chr(10).join(article_lines)}

{''.join(_build_conflict_prompt_section(conflict)) if conflict['detected'] else ''}Analyze the sentiment for this keyword and return a JSON object with EXACTLY these fields:
{{
  "headline_summary": "2-3 sentence executive summary of WHY this keyword has this sentiment score, grounded in the articles above",
  "sentiment_pattern": "<breakout_driven | high_frequency_moderate | contrarian | low_confidence>",
  "pattern_explanation": "1-2 sentences describing the character of coverage",
  "key_drivers": [
    {{
      "type": "<BREAKOUT | TRENDING | HEADWIND>",
      "title": "Short label 3-6 words",
      "description": "2-3 sentences with specific evidence from the articles above",
      "article_count": <integer>,
      "avg_sentiment_estimate": <float -1.0 to 1.0>,
      "recency_label": "<today | 1-2 days ago | 3-5 days ago | ongoing | fading>"
    }}
  ],
  "counterarguments": "2-3 sentences on the opposing case grounded in the article data",
  "confidence": "<high | medium | low>",
  "confidence_reason": "1 sentence on confidence based on article count and source quality"{'''
  ,
  "signal_conflict": {{
    "detected": true,
    "bull_case": "2-3 sentences explaining what bullish articles are seeing",
    "bear_case": "2-3 sentences explaining what bearish articles are seeing",
    "resolution": "2-3 sentences on which thesis the market is pricing in and why"
  }}''' if conflict['detected'] else ''}
}}

Definitions:
- BREAKOUT: 1-3 articles with |score| > 0.4 that disproportionately drive the average
- TRENDING: Many articles over multiple days with consistent moderate sentiment
- HEADWIND: Countervailing articles opposing the dominant direction
- breakout_driven: Score dominated by 1-3 extreme articles
- high_frequency_moderate: Broad, consistent coverage across many articles and days
- contrarian: High count but roughly split bullish/bearish
- low_confidence: Fewer than 5 articles or very mixed/weak signals

Rules:
- Include 2-4 key_drivers
- Be specific: reference actual article titles, themes, or sources from the data
- Do not fabricate events not in the article data
- If bullish overall, counterarguments should surface the bearish risk; vice versa"""

    client = _OpenAI(api_key=api_key)
    gpt_response = client.chat.completions.create(
        model='gpt-4o-mini',
        messages=[{'role': 'user', 'content': prompt}],
        response_format={'type': 'json_object'},
        temperature=0.2,
        max_tokens=1600,
    )
    analysis = json.loads(gpt_response.choices[0].message.content)

    # ------------------------------------------------------------------
    # Step 4: Web search enrichment — today-focused context only
    #
    # We use what the initial article analysis identified (key drivers,
    # sentiment pattern) to build precise, date-anchored queries.
    # The web search is prompted to return ONLY today's context, or
    # recent context directly relevant to the themes we already found.
    # Results are then synthesised back into the analysis via a second
    # GPT pass — updating, not replacing, what the articles told us.
    # ------------------------------------------------------------------
    today = datetime.now(timezone.utc).strftime('%Y-%m-%d')
    web_enriched = False
    web_queries_used = []

    web_context = _web_search_enrich(client, keyword, analysis, today)
    if web_context:
        web_enriched = True
        # Capture the queries for auditability
        web_queries_used = web_context.get('queries', [])
        web_text = web_context.get('summary', '')

        if web_text:
            synthesis_prompt = f"""You previously analysed "{keyword}" from a 7-day internal article database.
Now you have today's ({today}) live web context. Update the analysis to incorporate it.

ORIGINAL ANALYSIS (from internal articles):
Sentiment pattern : {analysis.get('sentiment_pattern')}
Headline summary  : {analysis.get('headline_summary')}
Key drivers       : {json.dumps(analysis.get('key_drivers', []), indent=2)}
Counterarguments  : {analysis.get('counterarguments')}
Confidence        : {analysis.get('confidence')} — {analysis.get('confidence_reason')}
Signal conflict   : {json.dumps(analysis.get('signal_conflict')) if analysis.get('signal_conflict') else 'None'}

TODAY'S WEB CONTEXT ({today}):
{web_text}

Rules for updating:
- Only change a field if the web context adds meaningfully new information for TODAY.
- Do NOT introduce historical context from the web that is older than 3 days unless it
  directly explains something happening today (e.g. an ongoing trial, a multi-day earnings run).
- Do NOT dilute or contradict well-supported findings from the article data without clear
  evidence from the web context.
- If the web context confirms the article analysis, say so in headline_summary — it raises confidence.
- If the web context reveals a significant development today NOT in the articles, incorporate it
  as a new key_driver with recency_label "today".
- Keep the same JSON schema with the same field names.
- If "signal_conflict" is present in the original analysis, preserve it in your output.
- Add a "web_context_note" field (1 sentence) describing what today's web search added or confirmed.

Return the complete updated JSON object with all original fields."""

            synth_response = client.chat.completions.create(
                model='gpt-4o-mini',
                messages=[{'role': 'user', 'content': synthesis_prompt}],
                response_format={'type': 'json_object'},
                temperature=0.2,
                max_tokens=1400,
            )
            enriched = json.loads(synth_response.choices[0].message.content)
            # Merge — keep all original fields, overwrite with enriched where present
            analysis.update(enriched)

    clean_articles = [{k: v for k, v in a.items() if k not in ('_date', 'summary')} for a in all_articles[:50]]

    result = {
        'keyword':             keyword,
        'sentiment_score':     avg_sentiment,
        'sentiment_label':     _sentiment_label(avg_sentiment),
        'sentiment_pattern':   analysis.get('sentiment_pattern', 'low_confidence'),
        'pattern_explanation': analysis.get('pattern_explanation', ''),
        'headline_summary':    analysis.get('headline_summary', ''),
        'key_drivers':         analysis.get('key_drivers', []),
        'counterarguments':    analysis.get('counterarguments', ''),
        'confidence':          analysis.get('confidence', 'medium'),
        'confidence_reason':   analysis.get('confidence_reason', ''),
        'web_context_note':    analysis.get('web_context_note', ''),
        'web_enriched':        web_enriched,
        'web_queries':         web_queries_used,
        'article_count':       article_count,
        'articles':            clean_articles,
        'generated_at':        datetime.utcnow().isoformat() + 'Z',
    }

    # Only include signal_conflict when detected (avoids noise for non-conflict keywords)
    signal_conflict_output = analysis.get('signal_conflict')
    if signal_conflict_output and signal_conflict_output.get('detected'):
        result['signal_conflict'] = signal_conflict_output

    return result


# ============================================================================
# MAIN BATCH PROCESSOR
# ============================================================================

def process_all_keywords(today: str) -> dict:
    """
    Load keyword-sentiments.json, compute GPT intelligence for every keyword,
    write each result to opal-keyword-intelligence DynamoDB.

    Skips keywords already written for today (idempotent).
    Continues on per-keyword errors.
    """
    stats = {
        'total': 0,
        'written': 0,
        'skipped_existing': 0,
        'errors': 0,
    }

    # Load keywords from S3
    print(f"[kig] Loading keywords from s3://{S3_BUCKET_PORTAL}/{KEYWORDS_S3_KEY}")
    try:
        resp = s3.get_object(Bucket=S3_BUCKET_PORTAL, Key=KEYWORDS_S3_KEY)
        kw_data = json.loads(resp['Body'].read().decode('utf-8'))
        keywords = kw_data.get('keywords', [])
    except Exception as e:
        raise RuntimeError(f"Failed to load keyword-sentiments.json: {e}")

    keywords = keywords[:MAX_KEYWORDS]
    print(f"[kig] {len(keywords)} keywords to process for {today} (MAX_KEYWORDS={MAX_KEYWORDS})")
    stats['total'] = len(keywords)

    for kw_entry in keywords:
        keyword = (kw_entry.get('keyword') or '').strip().lower()
        if not keyword:
            continue

        # Idempotency check — skip if already written for today
        try:
            existing = intel_t.get_item(
                Key={'keyword': keyword, 'generated_date': today},
                ProjectionExpression='keyword'
            )
            if 'Item' in existing:
                print(f"[kig] SKIP (exists): {keyword}")
                stats['skipped_existing'] += 1
                continue
        except Exception as e:
            print(f"[kig] Warning: idempotency check failed for {keyword}: {e}")
            # Proceed anyway — worst case we overwrite with fresh data

        # Compute intelligence
        try:
            payload = compute_keyword_intelligence(keyword, kw_entry)
        except Exception as e:
            print(f"[kig] ERROR computing {keyword}: {e}")
            stats['errors'] += 1
            continue

        # Write to DynamoDB
        try:
            item = _convert_for_dynamo(payload)
            item['keyword']        = keyword
            item['generated_date'] = today
            intel_t.put_item(Item=item)
            print(f"[kig] OK: {keyword} ({payload.get('article_count', 0)} articles, "
                  f"confidence={payload.get('confidence', '?')})")
            stats['written'] += 1
        except Exception as e:
            print(f"[kig] ERROR writing DynamoDB for {keyword}: {e}")
            stats['errors'] += 1

    return stats


# ============================================================================
# LAMBDA HANDLER
# ============================================================================

def lambda_handler(event, context):
    print("=" * 70)
    print("KEYWORD INTELLIGENCE GENERATOR")
    print("=" * 70)
    today = datetime.now(timezone.utc).strftime('%Y-%m-%d')
    print(f"Date: {today}")

    if not _OPENAI_AVAILABLE:
        return {
            'statusCode': 500,
            'body': json.dumps({'error': 'OpenAI package not available — rebuild zip with Linux wheels'})
        }

    try:
        stats = process_all_keywords(today)
    except Exception as e:
        print(f"[kig] FATAL: {e}")
        import traceback
        traceback.print_exc()
        return {
            'statusCode': 500,
            'body': json.dumps({'error': str(e)})
        }

    print()
    print("=" * 70)
    print(f"COMPLETE: {stats['written']} written, "
          f"{stats['skipped_existing']} skipped, "
          f"{stats['errors']} errors / {stats['total']} total")
    print("=" * 70)

    return {
        'statusCode': 200,
        'body': json.dumps({
            'message': 'Keyword intelligence generation complete',
            'date': today,
            'stats': stats,
        })
    }


if __name__ == '__main__':
    result = lambda_handler({}, None)
    print(json.dumps(json.loads(result['body']), indent=2))
