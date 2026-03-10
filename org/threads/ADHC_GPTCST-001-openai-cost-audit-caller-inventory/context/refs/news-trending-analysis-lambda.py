"""
News Trending Analysis Lambda - V2 (Refactored)
================================================

Sophisticated trending topic detection with:
- Exponential time decay (λ=0.05, ~14 day half-life)
- Multi-word phrase extraction
- NLTK + Finance stopwords (500+ words)
- Pattern-based phrase filtering (catches infinite variations)
- Sentiment scoring

Input: DynamoDB opal-news-articles (last 7 days)
Output: S3 opal-data-news-av/trending_reports/latest.json

Triggered: Daily at ~5:00 PM ET (after final ingestion at 4:45 PM)

Author: Dashboard Engineer
Date: 2025-12-01 (Refactored with modular filtering)
"""

import boto3
import json
from collections import defaultdict
from datetime import datetime, timedelta, timezone
import re
from typing import List, Dict
from html.parser import HTMLParser
from html import unescape
import math
from decimal import Decimal
import os

# OpenAI SDK for GPT validation
try:
    from openai import OpenAI
    OPENAI_AVAILABLE = True
except ImportError:
    print("WARN: OpenAI SDK not installed - GPT validation disabled")
    OPENAI_AVAILABLE = False
    OpenAI = None

# Import our modular stopwords and filters
from stopwords import (
    ALL_STOPWORDS, SENTIMENT_ONLY_KEYWORDS, MANUAL_INCLUSION_LIST,
    KEYWORD_ALIASES, FILTERED_PHRASES,
    is_blocked_source, is_clickbait_headline  # NEW: Source/headline filtering
)
from phrase_filters import filter_keyword, should_filter_phrase
from text_cleaner import clean_article_text, clean_title, clean_summary

# HDBSCAN for embedding-based clustering
try:
    import numpy as np
    import hdbscan
    HDBSCAN_AVAILABLE = True
except Exception as _hdbscan_err:
    HDBSCAN_AVAILABLE = False
    print(f"WARN: hdbscan/numpy not available -- will fall back to keyword clustering ({type(_hdbscan_err).__name__}: {_hdbscan_err})")

# AWS clients
dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
s3_client = boto3.client('s3', region_name='us-east-1')
secrets_client = boto3.client('secretsmanager', region_name='us-east-1')

# GPT Configuration
# API Key: News_Trending (dedicated key for this Lambda)
OPENAI_SECRET_NAME = os.environ.get('OPENAI_SECRET_NAME', 'opal/openai/news-trending')
GPT_MODEL = "gpt-4o"  # Upgraded from mini for better keyword validation

# Configuration
ARTICLES_TABLE = 'opal-news-articles'
S3_BUCKET = 'opal-data-news-v2'
S3_BUCKET_PORTAL = 'opal-data-portal-v2'  # TopicCloud word cloud output
DAYS_BACK = 7
TOP_N_TOPICS = 100  # Increased from 50 to widen bullish topic pool (2026-01-18)
DECAY_LAMBDA = 0.05  # Half-life ~14 days

# Dynamic stopwords file in S3 (learned from GPT validation)
DYNAMIC_STOPWORDS_KEY = 'config/dynamic_stopwords.json'


# ============================================================================
# GPT VALIDATION FUNCTIONS
# ============================================================================

def get_secret(secret_name: str) -> str:
    """Get secret value from AWS Secrets Manager"""
    try:
        response = secrets_client.get_secret_value(SecretId=secret_name)
        secret = response.get('SecretString', '{}')
        # Handle both raw string and JSON format
        try:
            parsed = json.loads(secret)
            return parsed.get('api_key') or parsed.get('key') or secret
        except json.JSONDecodeError:
            return secret
    except Exception as e:
        print(f"ERROR: Error getting secret {secret_name}: {e}")
        return None


def load_dynamic_stopwords() -> set:
    """Load dynamically learned stopwords from S3"""
    try:
        response = s3_client.get_object(Bucket=S3_BUCKET_PORTAL, Key=DYNAMIC_STOPWORDS_KEY)
        data = json.loads(response['Body'].read().decode('utf-8'))
        stopwords = set(data.get('stopwords', []))
        print(f"OK: Loaded {len(stopwords)} dynamic stopwords from S3")
        return stopwords
    except s3_client.exceptions.NoSuchKey:
        print("OK: No dynamic stopwords file found - starting fresh")
        return set()
    except Exception as e:
        print(f"WARN: Error loading dynamic stopwords: {e}")
        return set()


def save_dynamic_stopwords(stopwords: set):
    """Save dynamically learned stopwords to S3"""
    try:
        data = {
            'stopwords': sorted(list(stopwords)),
            'updated_at': datetime.now(timezone.utc).isoformat(),
            'count': len(stopwords)
        }
        s3_client.put_object(
            Bucket=S3_BUCKET_PORTAL,
            Key=DYNAMIC_STOPWORDS_KEY,
            Body=json.dumps(data, indent=2),
            ContentType='application/json'
        )
        print(f"OK: Saved {len(stopwords)} dynamic stopwords to S3")
    except Exception as e:
        print(f"ERROR: Error saving dynamic stopwords: {e}")


def gpt_validate_keywords(keywords: List[Dict]) -> List[Dict]:
    """
    Use GPT-4o-mini to validate keywords and filter out junk/noise.

    Returns filtered keyword list and updates dynamic stopwords.
    """
    if not OPENAI_AVAILABLE:
        print("WARN: OpenAI not available - skipping GPT validation")
        return keywords

    if not keywords:
        return keywords

    # Get API key
    api_key = get_secret(OPENAI_SECRET_NAME)
    if not api_key:
        print("WARN: No OpenAI API key - skipping GPT validation")
        return keywords

    try:
        client = OpenAI(api_key=api_key)

        # Extract just keyword names for validation
        keyword_names = [k['keyword'] for k in keywords]

        prompt = f"""You are a financial news analyst validating keywords for a portfolio manager word cloud.

REMOVE these categories of JUNK:

1. MEANINGLESS FRAGMENTS:
   - "the end", "the start", "the biggest", "the first", "the new"
   - "as part", "as part of", "first time", "questions"
   - ANY phrase starting with "the" + vague word

2. NEWS/ARTICLE BOILERPLATE:
   - "bbc world service", "five minute news", "news bulletin"
   - "drug boat", "york city"

3. META-CONTEXT (not actual topics):
   - "presents at", "presented at", "speaking at" (event boilerplate)
   - "prediction", "predicts", "could soar" (speculation boilerplate)
   - "investor day", "earnings call", "conference call" (event types, not topics)
   - "ubs global technology", "goldman conference" (conference names)

4. SPORTS CONTENT (absolute rejection - this is a financial portal, not a sports site):
   - Any NFL/NBA/MLB/NHL/NCAA keyword: "nfl", "nba", "mlb", "nhl", "ncaa"
   - Sports team names: "texans", "cowboys", "patriots", "chiefs", "steelers", "ravens",
     "eagles", "packers", "49ers", "bengals", "bills", "broncos", "colts", "titans",
     "falcons", "saints", "panthers", "buccaneers", "bears", "lions", "vikings",
     "seahawks", "rams", "chargers", "raiders", "jaguars", "browns", "commanders",
     "giants", "jets", "dolphins", "cardinals", "lakers", "celtics", "knicks",
     "yankees", "dodgers", "mets", "red sox", "cubs", "braves"
   - Sports terms: "free agency", "free agent", "trade deadline", "draft pick",
     "quarterback", "wide receiver", "running back", "franchise tag", "salary cap",
     "nfl trade", "nfl draft", "nfl free agency", "player trade", "roster move",
     "transfer portal", "march madness", "super bowl", "world series",
     "playoff", "postseason", "halftime", "regular season", "season opener"
   - Sports personalities: "tyreek hill", "patrick mahomes", "travis kelce",
     "lamar jackson", "josh allen", and other athlete names

KEEP these market-relevant keywords (DO NOT flag):
- People/policies: "trump", "fed", "tariffs", "powell"
- Countries/regions: "china", "russia", "ukraine"
- Sectors/assets: "ai stocks", "crypto", "bitcoin", "tech stocks"
- Events: "black friday", "cyber monday", "rate cut"
- Companies: "nvidia", "tesla", "apple"
- Economics: "inflation", "jobs report", "gdp"

Keywords to validate:
{json.dumps(keyword_names, indent=2)}

Return JSON:
{{
  "junk_keywords": ["keyword1", "keyword2"],
  "reason": "Brief explanation"
}}

Flag garbage, meta-context, and ALL sports content. Keep actual market topics."""

        response = client.chat.completions.create(
            model=GPT_MODEL,
            messages=[{"role": "user", "content": prompt}],
            response_format={"type": "json_object"},
            temperature=0.1,  # Low temp for consistency
            max_tokens=500
        )

        result = json.loads(response.choices[0].message.content)
        junk_keywords = set(k.lower() for k in result.get('junk_keywords', []))

        if junk_keywords:
            print(f"\nGPT: identified {len(junk_keywords)} junk keywords: {junk_keywords}")
            print(f"   Reason: {result.get('reason', 'N/A')}")

            # Filter out junk keywords
            filtered = [k for k in keywords if k['keyword'].lower() not in junk_keywords]

            # Update dynamic stopwords
            dynamic_stopwords = load_dynamic_stopwords()
            new_stopwords = junk_keywords - dynamic_stopwords
            if new_stopwords:
                print(f"   Adding {len(new_stopwords)} new stopwords: {new_stopwords}")
                dynamic_stopwords.update(junk_keywords)
                save_dynamic_stopwords(dynamic_stopwords)

            print(f"   Filtered: {len(keywords)} -> {len(filtered)} keywords")
            return filtered
        else:
            print("OK: GPT validation passed - all keywords look good")
            return keywords

    except Exception as e:
        print(f"WARN: GPT validation error (continuing without): {e}")
        return keywords


# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

class HTMLStripper(HTMLParser):
    """Strip HTML tags from text"""
    def __init__(self):
        super().__init__()
        self.reset()
        self.strict = False
        self.convert_charrefs = True
        self.text = []

    def handle_data(self, d):
        self.text.append(d)

    def get_data(self):
        return ''.join(self.text)


def strip_html(html_text: str) -> str:
    """Remove HTML tags and decode entities"""
    if not html_text:
        return ''
    text = unescape(html_text)
    stripper = HTMLStripper()
    stripper.feed(text)
    clean_text = stripper.get_data()
    clean_text = re.sub(r'\s+', ' ', clean_text).strip()
    return clean_text


def strip_boilerplate(text: str) -> str:
    """Remove common article boilerplate patterns before analysis"""
    boilerplate_patterns = [
        r'The post .* appeared first on .*',
        r'Originally published .*',
        r'Click here to .*',
        r'Read more:.*',
        r'See also:.*',
        r'Related:.*',
        r'Subscribe to .*',
        r'Sign up for .*',
        r'\(PRNewswire\).*',
        r'\(Business Wire\).*',
        r'\(Globe Newswire\).*',
        r'-- \w+ \d+, \d{4}',  # Date patterns
        r'Continue reading.*',
        r'For more information.*',
    ]

    cleaned = text
    for pattern in boilerplate_patterns:
        cleaned = re.sub(pattern, '', cleaned, flags=re.IGNORECASE)

    return cleaned.strip()


def calculate_time_decay(published_at: str, decay_lambda: float = DECAY_LAMBDA) -> float:
    """
    Calculate exponential time decay score: e^(-λ × days_ago)
    Returns 0.0-1.0 where recent = higher score
    """
    try:
        if published_at.endswith('Z'):
            published_dt = datetime.fromisoformat(published_at.replace('Z', '+00:00'))
        else:
            published_dt = datetime.fromisoformat(published_at)

        now = datetime.now(timezone.utc)
        if published_dt.tzinfo is None:
            published_dt = published_dt.replace(tzinfo=timezone.utc)

        days_ago = (now - published_dt).total_seconds() / 86400
        days_ago = max(0, days_ago)

        decay_score = math.exp(-decay_lambda * days_ago)
        return decay_score
    except Exception:
        return 0.5  # Default for unparseable dates


def extract_keywords(text: str) -> List[str]:
    """Extract meaningful keywords from text (uses stopword filtering)"""
    text = text.lower()
    words = re.findall(r'\b[a-z]{3,}\b', text)
    # Filter using our modular system
    keywords = [w for w in words if filter_keyword(w, is_phrase=False)]
    return keywords


def extract_phrases(text: str) -> List[str]:
    """Extract meaningful 2-3 word phrases (uses pattern filtering)"""
    text = text.lower()
    words = re.findall(r'\b[a-z]+\b', text)

    phrases = []
    for i in range(len(words) - 1):
        # 2-word phrases
        phrase = f"{words[i]} {words[i+1]}"
        # Use pattern filtering instead of explicit checks
        if not should_filter_phrase(phrase):
            phrases.append(phrase)

        # 3-word phrases
        if i < len(words) - 2:
            phrase3 = f"{words[i]} {words[i+1]} {words[i+2]}"
            if not should_filter_phrase(phrase3):
                phrases.append(phrase3)

    return phrases


def calculate_sentiment_fallback(text: str) -> Dict[str, float]:
    """
    FALLBACK sentiment calculation using keyword matching
    Only used when FinBERT score is missing from article

    NOTE: This is a backup method. Primary sentiment comes from FinBERT
    (ProsusAI/finbert transformer scored by opal-news-ai-sentiment Lambda)
    """
    text_lower = text.lower()

    # Simple positive/negative word lists
    positive_words = {'gain', 'gains', 'surge', 'surges', 'rally', 'rallies',
                      'jump', 'jumps', 'soar', 'soars', 'beat', 'beats',
                      'strong', 'bullish', 'optimistic', 'growth', 'profit'}
    negative_words = {'loss', 'losses', 'drop', 'drops', 'fall', 'falls',
                      'plunge', 'plunges', 'crash', 'crashes', 'decline',
                      'weak', 'bearish', 'pessimistic', 'recession', 'fear'}

    words = set(re.findall(r'\b[a-z]+\b', text_lower))

    pos_count = len(words & positive_words)
    neg_count = len(words & negative_words)
    total = pos_count + neg_count

    if total == 0:
        sentiment = 0.0
    else:
        sentiment = (pos_count - neg_count) / total

    return {
        'overall': sentiment,
        'bullish_bearish': sentiment,
        'confidence_fear': 0.0,
        'positive_negative': sentiment,
        'risk_appetite': 0.0,
        'legal_risk': 0.0,
        'emotional_intensity': min(1.0, total / 5)
    }


def get_article_sentiment(article: Dict, text: str) -> float:
    """
    Get sentiment score for article, prioritizing FinBERT

    Priority:
    1. sentiment_finbert (from FinBERT transformer) - PRIMARY
       - 0.0 scores are treated as "no meaningful sentiment" and EXCLUDED
       - Only non-zero FinBERT scores (-1.0 to 1.0) are used
    2. If FinBERT is 0.0 or missing, return None (excluded from sentiment aggregation)

    Returns:
        sentiment score from -1.0 (bearish) to +1.0 (bullish)
        OR None if no meaningful sentiment detected (0.0 FinBERT or missing)

    Note: FinBERT returns 0.0 when it cannot extract meaningful sentiment from text.
    These articles should not contribute to sentiment analysis as they add noise.
    """
    # Check if article has FinBERT score (added by opal-news-ai-sentiment Lambda)
    sentiment_finbert = article.get('sentiment_finbert')

    if sentiment_finbert is not None:
        # Convert Decimal to float if needed
        try:
            finbert_score = float(sentiment_finbert)
            # Validate range AND exclude 0.0 scores (no meaningful sentiment)
            if -1.0 <= finbert_score <= 1.0 and finbert_score != 0.0:
                return finbert_score
            # 0.0 means FinBERT couldn't detect sentiment - return None
            elif finbert_score == 0.0:
                return None
        except (ValueError, TypeError):
            pass

    # No FinBERT score or invalid - return None (exclude from sentiment analysis)
    # We don't fallback to keyword matching as FinBERT is more accurate
    return None


def calculate_quality_score(article: Dict) -> float:
    """Calculate source quality score"""
    source = article.get('source', '').lower()

    quality_map = {
        'financial times': 100, 'ft ': 100, 'bloomberg': 100,
        'wall street journal': 100, 'wsj': 100, 'reuters': 95,
        'cnbc': 90, 'economist': 95, 'barrons': 90,
        'yahoo finance': 85, 'marketwatch': 85,
        'seeking alpha': 80, 'benzinga': 75,
        'coindesk': 75, 'cointelegraph': 70,
    }

    for key, score in quality_map.items():
        if key in source:
            return float(score)

    return 50.0  # Default


def decimal_to_float(obj):
    """Convert Decimal to float for JSON serialization"""
    if isinstance(obj, Decimal):
        return float(obj)
    elif isinstance(obj, dict):
        return {k: decimal_to_float(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [decimal_to_float(i) for i in obj]
    return obj


# ============================================================================
# MAIN ANALYSIS FUNCTIONS
# ============================================================================

def load_articles_from_dynamodb(days: int = DAYS_BACK) -> List[Dict]:
    """Load articles from DynamoDB for the past N days"""
    print(f"Loading {days} days of articles from DynamoDB...")

    table = dynamodb.Table(ARTICLES_TABLE)
    articles = []

    for days_ago in range(days):
        date_str = (datetime.now() - timedelta(days=days_ago)).strftime('%Y-%m-%d')

        try:
            response = table.query(
                KeyConditionExpression='article_date = :date',
                ExpressionAttributeValues={':date': date_str}
            )

            day_articles = response.get('Items', [])
            articles.extend(day_articles)

            # Handle pagination
            while 'LastEvaluatedKey' in response:
                response = table.query(
                    KeyConditionExpression='article_date = :date',
                    ExpressionAttributeValues={':date': date_str},
                    ExclusiveStartKey=response['LastEvaluatedKey']
                )
                articles.extend(response.get('Items', []))

            print(f"  {date_str}: {len(day_articles)} articles")

        except Exception as e:
            print(f"  {date_str}: Error - {e}")

    # Convert Decimals to floats
    articles = [decimal_to_float(a) for a in articles]

    print(f"OK: Loaded {len(articles)} total articles\n")
    return articles


def _merge_plural_forms(keyword_data: dict) -> dict:
    """
    Post-accumulation merge: fold simple plural forms into their singular.

    Only merges when BOTH the plural and singular appear in keyword_data, so
    it never invents a singular that wasn't already being tracked.  Handles:
      - word + s   → word   (tariffs → tariff, chips → chip)
      - word + es  → word   (indices → index NOT handled; too irregular)
      - word + ies → word+y (currencies → currency)

    Multi-word phrases are never touched — only single tokens.
    Words already handled by KEYWORD_ALIASES are already merged at ingestion
    time; this catches anything that slipped through.
    """
    kw_set = set(keyword_data.keys())
    to_merge = {}  # plural_key → singular_key

    for kw in list(kw_set):
        if ' ' in kw:
            continue  # skip phrases

        kw_lower = kw.lower()

        # -ies → -y  (e.g. currencies → currency)
        if kw_lower.endswith('ies') and len(kw_lower) > 4:
            candidate = kw_lower[:-3] + 'y'
            if candidate in kw_set:
                to_merge[kw] = candidate
                continue

        # -es → base  (e.g. watches → watch) — only if base is ≥3 chars
        if kw_lower.endswith('es') and len(kw_lower) > 4:
            candidate = kw_lower[:-2]
            if candidate in kw_set and len(candidate) >= 3:
                to_merge[kw] = candidate
                continue

        # -s → base  (e.g. tariffs → tariff, chips → chip)
        if kw_lower.endswith('s') and len(kw_lower) > 3:
            candidate = kw_lower[:-1]
            if candidate in kw_set and len(candidate) >= 3:
                to_merge[kw] = candidate

    if not to_merge:
        return keyword_data

    merged = dict(keyword_data)
    for plural, singular in to_merge.items():
        if plural not in merged or singular not in merged:
            continue
        merged[singular]['articles'].extend(merged[plural]['articles'])
        merged[singular]['sentiment_scores'].extend(merged[plural]['sentiment_scores'])
        merged[singular]['positive_articles'].extend(merged[plural]['positive_articles'])
        merged[singular]['negative_articles'].extend(merged[plural]['negative_articles'])
        merged[singular]['neutral_articles'].extend(merged[plural]['neutral_articles'])
        merged[singular]['time_decay_scores'].extend(merged[plural]['time_decay_scores'])
        merged[singular]['quality_scores'].extend(merged[plural]['quality_scores'])
        del merged[plural]
        print(f"MERGE: plural '{plural}' -> '{singular}' "
              f"({len(merged[singular]['articles'])} combined articles)")

    return merged


def detect_trending_topics(articles: List[Dict], top_n: int = TOP_N_TOPICS) -> List[Dict]:
    """Detect trending topics with time-decay scoring and pattern-based filtering"""
    print(f"Detecting trending topics from {len(articles)} articles...")

    keyword_data = defaultdict(lambda: {
        'articles': [],
        'sentiment_scores': [],
        'positive_articles': [],  # Track positive sentiment articles
        'negative_articles': [],  # Track negative sentiment articles
        'neutral_articles': [],   # Track neutral sentiment articles
        'time_decay_scores': [],
        'quality_scores': []
    })

    all_phrases = set()
    blocked_source_count = 0
    clickbait_count = 0

    for article in articles:
        title = clean_title(article.get('title', ''))
        summary = clean_summary(article.get('summary', ''))
        source = article.get('source', '') or article.get('newsapi_source_name', '')

        # FILTER 1: Block low-quality sources (Motley Fool, InvestorPlace, etc.)
        if is_blocked_source(source):
            blocked_source_count += 1
            continue

        # FILTER 2: Block clickbait headlines ("This stock could soar...", etc.)
        if is_clickbait_headline(title):
            clickbait_count += 1
            continue

        text = f"{title} {summary}"

        # Calculate scores - use published_date (DynamoDB field name)
        time_decay = calculate_time_decay(article.get('published_date', ''))
        quality = calculate_quality_score(article)

        # Get sentiment - uses FinBERT only, returns None if 0.0 or missing
        sentiment_score = get_article_sentiment(article, text)

        # Store in article (None means no meaningful sentiment)
        article['time_decay_score'] = time_decay
        article['quality_score'] = quality
        article['sentiment_overall'] = sentiment_score
        article['sentiment_bullish_bearish'] = sentiment_score
        article['has_meaningful_sentiment'] = sentiment_score is not None

        # Extract keywords and phrases (already filtered by extract_* functions)
        keywords = extract_keywords(text)
        phrases = extract_phrases(text)
        all_phrases.update(phrases)

        # Track keyword occurrences
        for kw in set(keywords + phrases):
            # Skip filtered phrases (e.g., "of ai", "in the")
            if kw in FILTERED_PHRASES:
                continue

            # Apply keyword aliases (e.g., "donald trump" -> "trump")
            kw_normalized = KEYWORD_ALIASES.get(kw, kw)

            keyword_data[kw_normalized]['articles'].append(article)

            # Track sentiment distribution by category
            if sentiment_score is not None:
                keyword_data[kw_normalized]['sentiment_scores'].append(sentiment_score)

                # Categorize article by sentiment (FIX: Track actual distribution)
                if sentiment_score >= BULLISH_THRESHOLD:
                    keyword_data[kw_normalized]['positive_articles'].append(article)
                elif sentiment_score <= BEARISH_THRESHOLD:
                    keyword_data[kw_normalized]['negative_articles'].append(article)
                else:
                    keyword_data[kw_normalized]['neutral_articles'].append(article)

            keyword_data[kw_normalized]['time_decay_scores'].append(time_decay)
            keyword_data[kw_normalized]['quality_scores'].append(quality)

    # Build component words to exclude (if phrase exists, skip its words)
    component_words = set()
    for phrase in all_phrases:
        component_words.update(phrase.split())

    # Merge plural forms into singular (e.g. "tariffs" → "tariff") so both
    # don't appear as separate entries in the word cloud
    keyword_data = _merge_plural_forms(keyword_data)

    # Calculate trending scores
    trending_topics = []

    for keyword, data in keyword_data.items():
        mention_count = len(data['articles'])

        # Minimum mentions threshold
        is_manual = keyword.lower() in MANUAL_INCLUSION_LIST
        min_mentions = 1 if is_manual else 3

        if mention_count < min_mentions:
            continue

        # Skip component words (unless it's a phrase itself or manual)
        is_phrase = ' ' in keyword
        if not is_phrase and keyword in component_words and not is_manual:
            continue

        # Skip sentiment-only keywords (unless manual)
        if keyword.lower() in SENTIMENT_ONLY_KEYWORDS and not is_manual:
            continue

        # Calculate weighted trending score
        trending_score = sum(
            td * (q / 100) * (1.5 if is_phrase else 1.0)
            for td, q in zip(data['time_decay_scores'], data['quality_scores'])
        )

        # Calculate averages - sentiment may be empty if all articles had 0.0 FinBERT
        sentiment_scores = data['sentiment_scores']
        if sentiment_scores:
            avg_sentiment = sum(sentiment_scores) / len(sentiment_scores)
            sentiment_article_count = len(sentiment_scores)

            # FIX: Calculate actual label distribution counts
            positive_count = len(data['positive_articles'])
            negative_count = len(data['negative_articles'])
            neutral_count = len(data['neutral_articles'])
        else:
            avg_sentiment = None  # No meaningful sentiment for this topic
            sentiment_article_count = 0
            positive_count = 0
            negative_count = 0
            neutral_count = 0

        avg_quality = sum(data['quality_scores']) / len(data['quality_scores'])
        avg_time_decay = sum(data['time_decay_scores']) / len(data['time_decay_scores'])

        # DEBUG: Log Nvidia specifically to verify fix
        if keyword.lower() == 'nvidia':
            print(f"\n{'='*80}")
            print(f"DEBUG: Nvidia Sentiment Analysis (FIX VERIFICATION)")
            print(f"{'='*80}")
            print(f"   Total articles mentioning Nvidia: {mention_count}")
            print(f"   Articles with meaningful sentiment: {sentiment_article_count}")
            print(f"   Positive articles: {positive_count}")
            print(f"   Negative articles: {negative_count}")
            print(f"   Neutral articles: {neutral_count}")
            print(f"   Distribution check: {positive_count + negative_count + neutral_count} = {sentiment_article_count}")
            print(f"   Average sentiment score: {avg_sentiment:.4f}")
            print(f"   Sample sentiment scores (first 10): {sentiment_scores[:10]}")
            print(f"{'='*80}\n")

        # Get top articles by quality (up to 50 for drilldown scrolling)
        sample_articles = sorted(
            data['articles'],
            key=lambda a: a.get('quality_score', 0),
            reverse=True
        )[:50]

        trending_topics.append({
            'keyword': keyword,
            'mention_count': mention_count,
            'trending_score': round(trending_score, 3),
            'avg_sentiment': round(avg_sentiment, 4) if avg_sentiment is not None else None,
            'sentiment_article_count': sentiment_article_count,  # How many articles had meaningful FinBERT
            'positive_count': positive_count,    # FIX: Actual positive article count
            'negative_count': negative_count,    # FIX: Actual negative article count
            'neutral_count': neutral_count,      # FIX: Actual neutral article count
            'avg_quality': round(avg_quality, 1),
            'avg_time_decay': round(avg_time_decay, 3),
            'is_phrase': is_phrase,
            'sample_articles': [
                {
                    'title': a.get('title', ''),
                    'source': a.get('source', ''),
                    'url': a.get('url', ''),
                    'published_at': a.get('published_date', ''),  # DynamoDB field is published_date
                    'sentiment': a.get('sentiment_bullish_bearish'),  # None if no meaningful sentiment
                    'has_sentiment': a.get('has_meaningful_sentiment', False)
                }
                for a in sample_articles
            ]
        })

    # Sort by trending score
    trending_topics.sort(key=lambda x: x['trending_score'], reverse=True)

    # Log filtering stats
    if blocked_source_count > 0 or clickbait_count > 0:
        print(f"SKIP: Filtered out: {blocked_source_count} blocked sources, {clickbait_count} clickbait headlines")
    print(f"OK: Found {len(trending_topics)} trending topics (returning top {top_n})\n")
    return trending_topics[:top_n]


def extract_cluster_label(articles: List[Dict]) -> str:
    """
    Pick the best single-word or phrase label for a cluster.

    Counts how many articles in the cluster contain each keyword/phrase
    (TF-style: 1 per article regardless of frequency within it).  Returns
    the most common term, preferring phrases over single words via the
    existing 1.5× phrase bonus.  Falls back to the highest-quality article's
    first title keyword if nothing survives filtering.
    """
    from collections import Counter
    keyword_counts = Counter()

    for article in articles:
        title = clean_title(article.get('title', ''))
        summary = clean_summary(article.get('summary', ''))
        text = f"{title} {summary}"

        seen = set()
        for term in extract_keywords(text) + extract_phrases(text):
            normalized = KEYWORD_ALIASES.get(term, term)
            if normalized not in FILTERED_PHRASES and normalized not in seen:
                # Weight phrases 1.5× to prefer multi-word labels
                keyword_counts[normalized] += 1.5 if ' ' in normalized else 1.0
                seen.add(normalized)

    if keyword_counts:
        return keyword_counts.most_common(1)[0][0]

    # Fallback: first keyword from the highest-quality article title
    best = max(articles, key=lambda a: a.get('quality_score', 0))
    words = extract_keywords(clean_title(best.get('title', '')))
    return words[0] if words else 'unknown'


def _gpt_label_clusters(topics: List[Dict], client) -> Dict[int, str]:
    """
    Use GPT-4o-mini to generate precise 1-3 word labels for a batch of clusters.

    Sends one request with all cluster IDs + their top-3 article titles.
    Returns {cluster_id: label}. Falls back to extract_cluster_label() if this
    returns {} or is missing an entry.
    """
    if not topics or not OPENAI_AVAILABLE:
        return {}

    lines = []
    for t in topics:
        cid = t.get('cluster_id')
        if cid is None:
            continue
        titles = [
            a.get('title', '')[:100]
            for a in t.get('sample_articles', [])[:3]
            if a.get('title')
        ]
        if not titles:
            continue
        lines.append(f'{cid}: {" | ".join(titles)}')

    if not lines:
        return {}

    prompt_body = '\n'.join(lines)

    try:
        response = client.chat.completions.create(
            model='gpt-4o-mini',
            messages=[
                {
                    'role': 'system',
                    'content': (
                        'You are labeling clusters of financial news articles for a word cloud. '
                        'For each cluster ID and its article titles, return a specific 1-3 word '
                        'lowercase label capturing the core story. '
                        'Prefer precise terms (e.g. "nvidia earnings", "fed rate cut", '
                        '"china tariffs") over generic ones (e.g. "market", "news", "stocks"). '
                        'Respond ONLY with valid JSON: {"0": "label", "1": "label", ...}'
                    ),
                },
                {
                    'role': 'user',
                    'content': f'Label these news clusters:\n\n{prompt_body}',
                },
            ],
            max_tokens=1500,
            temperature=0.0,
            response_format={'type': 'json_object'},
        )
        raw = json.loads(response.choices[0].message.content)
        result = {int(k): str(v).strip().lower()[:60]
                  for k, v in raw.items() if str(k).lstrip('-').isdigit()}
        print(f'[embed_and_cluster] GPT labeled {len(result)}/{len(topics)} clusters')
        return result
    except Exception as e:
        print(f'[embed_and_cluster] GPT labeling failed ({type(e).__name__}: {e}) -- using keyword fallback')
        return {}


def embed_and_cluster_topics(articles: List[Dict], top_n: int = TOP_N_TOPICS) -> List[Dict]:
    """
    Embedding-based replacement for detect_trending_topics().

    Same input  : articles list from DynamoDB (with FinBERT scores pre-populated)
    Same output : trending_topics list — identical schema consumed by Layer 3

    Steps:
      1. Per-article filters + scoring  (same logic as keyword version)
      2. Batch embed via OpenAI text-embedding-3-small (dimensions=256)
      3. HDBSCAN cluster (min_cluster_size=5, leaf method)
      4. Aggregate cluster-level scores; initial label via extract_cluster_label()
      5. Pairwise cosine similarities across ALL clusters
      5b. Deterministic dedup: drop weaker of each pair with sim > 0.65
      6. GPT-4o-mini batch labeling of top-N surviving clusters
    """
    if not HDBSCAN_AVAILABLE:
        print("WARN: Falling back to keyword-based detect_trending_topics()")
        return detect_trending_topics(articles, top_n), []

    print(f"[embed_and_cluster] Starting with {len(articles)} articles...")

    # ------------------------------------------------------------------
    # Step 1: Per-article filter + scoring (mirrors detect_trending_topics)
    # ------------------------------------------------------------------
    filtered = []
    blocked_source_count = 0
    clickbait_count = 0

    for article in articles:
        title = clean_title(article.get('title', ''))
        summary = clean_summary(article.get('summary', ''))
        source = article.get('source', '') or article.get('newsapi_source_name', '')

        if is_blocked_source(source):
            blocked_source_count += 1
            continue
        if is_clickbait_headline(title):
            clickbait_count += 1
            continue

        text = f"{title} {summary}"

        time_decay = calculate_time_decay(article.get('published_date', ''))
        quality = calculate_quality_score(article)
        sentiment = get_article_sentiment(article, text)

        article['time_decay_score'] = time_decay
        article['quality_score'] = quality
        article['sentiment_overall'] = sentiment
        article['sentiment_bullish_bearish'] = sentiment
        article['has_meaningful_sentiment'] = sentiment is not None
        article['_embed_text'] = text

        filtered.append(article)

    print(f"[embed_and_cluster] After filters: {len(filtered)} articles "
          f"(blocked={blocked_source_count}, clickbait={clickbait_count})")

    if not filtered:
        return [], []

    # ------------------------------------------------------------------
    # Step 2: Batch embed via OpenAI
    # ------------------------------------------------------------------
    api_key = get_secret(OPENAI_SECRET_NAME)
    if not api_key:
        print("WARN: No OpenAI key -- falling back to keyword clustering")
        return detect_trending_topics(articles, top_n), []

    client = OpenAI(api_key=api_key)
    texts = [a['_embed_text'][:8000] for a in filtered]   # ~2K token cap per article

    all_embeddings = []
    batch_size = 500
    for i in range(0, len(texts), batch_size):
        batch = texts[i:i + batch_size]
        response = client.embeddings.create(
            model="text-embedding-3-small",
            input=batch,
            dimensions=256,   # Reduced from 1536 — sufficient for news clustering
        )
        # Preserve input order (API doesn't guarantee it)
        sorted_data = sorted(response.data, key=lambda x: x.index)
        all_embeddings.extend([item.embedding for item in sorted_data])
        print(f"[embed_and_cluster] Embedded batch {i // batch_size + 1}/{math.ceil(len(texts)/batch_size)}: {len(batch)} articles")

    embeddings_matrix = np.array(all_embeddings, dtype=np.float32)
    print(f"[embed_and_cluster] Embeddings matrix: {embeddings_matrix.shape}")

    # ------------------------------------------------------------------
    # Step 3: HDBSCAN cluster
    # ------------------------------------------------------------------
    clusterer = hdbscan.HDBSCAN(
        min_cluster_size=5,
        min_samples=1,
        cluster_selection_method='leaf',
        metric='euclidean',
        core_dist_n_jobs=-1,      # use all available CPUs
    )
    labels = clusterer.fit_predict(embeddings_matrix)

    n_clusters = len(set(labels)) - (1 if -1 in labels else 0)
    noise_count = int(np.sum(labels == -1))
    print(f"[embed_and_cluster] Clusters: {n_clusters}, "
          f"Noise: {noise_count} ({100 * noise_count / len(labels):.1f}%)")

    # ------------------------------------------------------------------
    # Step 4: Build trending_topics from clusters
    # ------------------------------------------------------------------
    from collections import defaultdict as _defaultdict
    cluster_buckets: dict = _defaultdict(list)
    for article, label in zip(filtered, labels):
        if label != -1:
            cluster_buckets[int(label)].append(article)

    trending_topics = []

    for cluster_id, c_arts in cluster_buckets.items():
        sentiments = [
            a['sentiment_bullish_bearish']
            for a in c_arts
            if a.get('has_meaningful_sentiment')
        ]
        if sentiments:
            avg_sentiment = sum(sentiments) / len(sentiments)
            positive_count = sum(1 for s in sentiments if s >= BULLISH_THRESHOLD)
            negative_count = sum(1 for s in sentiments if s <= BEARISH_THRESHOLD)
            neutral_count = len(sentiments) - positive_count - negative_count
        else:
            avg_sentiment = None
            positive_count = negative_count = neutral_count = 0

        time_decays = [a['time_decay_score'] for a in c_arts]
        quality_scores = [a['quality_score'] for a in c_arts]

        # Same weighted score formula as keyword version; clusters are always
        # multi-word topics so the 1.5× phrase bonus applies universally
        trending_score = sum(
            td * (q / 100) * 1.5
            for td, q in zip(time_decays, quality_scores)
        )

        avg_time_decay = sum(time_decays) / len(time_decays)
        avg_quality = sum(quality_scores) / len(quality_scores)

        # Top 50 articles by quality — same cap as keyword version
        sample_arts = sorted(c_arts, key=lambda a: a.get('quality_score', 0), reverse=True)[:50]

        trending_topics.append({
            'keyword': extract_cluster_label(c_arts),
            'cluster_id': cluster_id,
            'mention_count': len(c_arts),
            'trending_score': round(trending_score, 3),
            'avg_sentiment': round(avg_sentiment, 4) if avg_sentiment is not None else None,
            'sentiment_article_count': len(sentiments),
            'positive_count': positive_count,
            'negative_count': negative_count,
            'neutral_count': neutral_count,
            'avg_quality': round(avg_quality, 1),
            'avg_time_decay': round(avg_time_decay, 3),
            'is_phrase': True,
            'sample_articles': [
                {
                    'title': a.get('title', ''),
                    'source': a.get('source', ''),
                    'url': a.get('url', ''),
                    'published_at': a.get('published_date', ''),
                    'sentiment': a.get('sentiment_bullish_bearish'),
                    'has_sentiment': a.get('has_meaningful_sentiment', False),
                }
                for a in sample_arts
            ],
        })

    trending_topics.sort(key=lambda x: x['trending_score'], reverse=True)

    # ------------------------------------------------------------------
    # Step 5: Pairwise cosine similarities across ALL clusters
    # ------------------------------------------------------------------
    centroid_map: dict = {}
    for idx, (article, label) in enumerate(zip(filtered, labels)):
        if label == -1:
            continue
        if label not in centroid_map:
            centroid_map[label] = []
        centroid_map[label].append(embeddings_matrix[idx])

    centroids = {cid: np.mean(np.stack(vecs), axis=0)
                 for cid, vecs in centroid_map.items()}

    all_cluster_ids = list(centroids.keys())
    similarities = []
    for i in range(len(all_cluster_ids)):
        for j in range(i + 1, len(all_cluster_ids)):
            a, b = all_cluster_ids[i], all_cluster_ids[j]
            sim = float(np.dot(centroids[a], centroids[b]) /
                        (np.linalg.norm(centroids[a]) * np.linalg.norm(centroids[b]) + 1e-8))
            if sim > 0.30:
                similarities.append({'cluster_a': int(a), 'cluster_b': int(b), 'similarity': round(sim, 3)})

    similarities.sort(key=lambda x: x['similarity'], reverse=True)
    print(f"[embed_and_cluster] {len(similarities)} similarity pairs >0.30 across {len(all_cluster_ids)} clusters")

    # ------------------------------------------------------------------
    # Step 5b: Deterministic dedup — drop the weaker cluster in each
    #           near-duplicate pair (similarity > 0.65) before Layer 3
    # ------------------------------------------------------------------
    DEDUP_THRESHOLD = 0.65
    score_lookup = {t['cluster_id']: t['trending_score'] for t in trending_topics}
    dropped_ids: set = set()

    for pair in similarities:                    # already sorted high → low
        if pair['similarity'] < DEDUP_THRESHOLD:
            break
        cid_a, cid_b = pair['cluster_a'], pair['cluster_b']
        if cid_a in dropped_ids or cid_b in dropped_ids:
            continue                              # one side already eliminated
        # Keep the stronger cluster; drop the weaker
        drop = cid_b if score_lookup.get(cid_a, 0) >= score_lookup.get(cid_b, 0) else cid_a
        dropped_ids.add(drop)

    if dropped_ids:
        trending_topics = [t for t in trending_topics if t['cluster_id'] not in dropped_ids]
        print(f"[embed_and_cluster] Dedup removed {len(dropped_ids)} near-duplicate clusters (sim >{DEDUP_THRESHOLD})")

    # Similarity pairs for Layer 3: only surviving clusters, capped at 100
    surviving_ids = {t['cluster_id'] for t in trending_topics}
    cluster_similarities = [
        p for p in similarities
        if p['cluster_a'] in surviving_ids and p['cluster_b'] in surviving_ids
    ][:100]
    print(f"[embed_and_cluster] {len(cluster_similarities)} similarity pairs after dedup -> Layer 3")

    # ------------------------------------------------------------------
    # Step 6: GPT-4o-mini batch labeling of top-N surviving clusters
    # ------------------------------------------------------------------
    label_targets = trending_topics[:top_n]
    gpt_labels = _gpt_label_clusters(label_targets, client)
    if gpt_labels:
        for t in label_targets:
            gpt_label = gpt_labels.get(t['cluster_id'])
            if gpt_label:
                t['keyword'] = gpt_label

    print(f"[embed_and_cluster] OK: {len(trending_topics)} clusters after dedup -> returning top {top_n}\n")
    return trending_topics[:top_n], cluster_similarities


def generate_report(articles: List[Dict], trending_topics: List[Dict], cluster_similarities: List[Dict] = None) -> Dict:
    """Generate the trending report"""

    # Count FinBERT coverage - separate total from meaningful
    finbert_total = sum(1 for a in articles if a.get('sentiment_finbert') is not None)
    finbert_zero = sum(1 for a in articles
                       if a.get('sentiment_finbert') is not None
                       and float(a.get('sentiment_finbert', 1)) == 0.0)
    finbert_meaningful = finbert_total - finbert_zero

    # Coverage percentages
    finbert_total_pct = (finbert_total / len(articles) * 100) if articles else 0
    finbert_meaningful_pct = (finbert_meaningful / len(articles) * 100) if articles else 0

    # Count sentiment distribution (only from articles with meaningful FinBERT scores)
    articles_with_sentiment = [a for a in articles if a.get('has_meaningful_sentiment', False)]
    bullish = sum(1 for a in articles_with_sentiment if a.get('sentiment_bullish_bearish', 0) > 0.1)
    bearish = sum(1 for a in articles_with_sentiment if a.get('sentiment_bullish_bearish', 0) < -0.1)
    neutral_sentiment = len(articles_with_sentiment) - bullish - bearish
    no_sentiment = len(articles) - len(articles_with_sentiment)

    report = {
        'generated_at': datetime.now(timezone.utc).isoformat(),
        'analysis_window_days': DAYS_BACK,
        'decay_lambda': DECAY_LAMBDA,
        'total_articles': len(articles),
        'filtering_system': 'NLTK + Finance stopwords + Pattern matching',
        'sentiment_system': 'FinBERT transformer (ProsusAI/finbert)',
        'finbert_coverage': {
            'total_scored': finbert_total,
            'zero_scores_excluded': finbert_zero,
            'meaningful_scores': finbert_meaningful,
            'total_coverage_pct': round(finbert_total_pct, 1),
            'meaningful_coverage_pct': round(finbert_meaningful_pct, 1)
        },
        'sentiment_breakdown': {
            'Bullish (>0.1)': bullish,
            'Bearish (<-0.1)': bearish,
            'Neutral (-0.1 to 0.1)': neutral_sentiment,
            'No meaningful sentiment': no_sentiment
        },
        'trending_topics': trending_topics,
        'cluster_similarities': cluster_similarities or [],
    }

    return report


# ============================================================================
# BALANCED KEYWORD SELECTION FOR WORD CLOUD
# ============================================================================

# Minimum keywords per sentiment category for word cloud
MIN_BULLISH = 10
MIN_NEUTRAL = 5
MIN_BEARISH = 10

# Thresholds for sentiment classification
BULLISH_THRESHOLD = 0.05   # >= 0.05 is bullish
BEARISH_THRESHOLD = -0.05  # <= -0.05 is bearish


def normalize_sizes_for_visibility(keywords: List[Dict]) -> List[Dict]:
    """
    Add normalized 'size' field for word cloud visualization while keeping true counts.

    Problem: Bearish keywords might have 100+ mentions while bullish have 10,
    making bullish keywords invisible in the word cloud.

    Solution: Use logarithmic scaling with a minimum floor to compress the range.
    - 'count' stays TRUE (actual mentions)
    - 'size' is normalized for word cloud display (compressed range)

    Args:
        keywords: List of keyword dicts with 'sentiment' and 'count' fields

    Returns:
        Same keywords with 'size' field added for word cloud sizing
    """
    import math

    if not keywords:
        return keywords

    # Get count range
    counts = [k['count'] for k in keywords]
    min_count = min(counts)
    max_count = max(counts)

    # Use log scale to compress the range
    # This makes 10 mentions vs 100 mentions look like 1 vs 2, not 1 vs 10
    # Add 1 to avoid log(0)
    log_min = math.log(min_count + 1)
    log_max = math.log(max_count + 1)
    log_range = log_max - log_min if log_max > log_min else 1

    # Normalize to 30-100 range (minimum 30% size for visibility)
    MIN_SIZE = 30
    MAX_SIZE = 100

    print(f"\nSize normalization for word cloud (TRUE counts preserved):")
    print(f"   Count range: {min_count} - {max_count}")
    print(f"   Using log scale to compress visual range")

    for keyword in keywords:
        count = keyword['count']
        log_count = math.log(count + 1)

        # Normalize to MIN_SIZE - MAX_SIZE range
        if log_range > 0:
            normalized = (log_count - log_min) / log_range
        else:
            normalized = 0.5

        size = int(MIN_SIZE + normalized * (MAX_SIZE - MIN_SIZE))
        keyword['size'] = size

    # Log some examples
    bullish = [k for k in keywords if k.get('sentiment', 0) >= BULLISH_THRESHOLD]
    bearish = [k for k in keywords if k.get('sentiment', 0) <= BEARISH_THRESHOLD]

    if bullish:
        top_bull = max(bullish, key=lambda x: x['count'])
        print(f"   Top bullish: {top_bull['keyword']} count={top_bull['count']} -> size={top_bull['size']}")
    if bearish:
        top_bear = max(bearish, key=lambda x: x['count'])
        print(f"   Top bearish: {top_bear['keyword']} count={top_bear['count']} -> size={top_bear['size']}")

    return keywords


def select_balanced_keywords(trending_topics: List[Dict], total_keywords: int = 50) -> List[Dict]:
    """
    Select keywords ensuring minimum representation of each sentiment category.

    Guarantees at least MIN_BULLISH, MIN_NEUTRAL, MIN_BEARISH keywords in output,
    searching through all trending topics to find them.

    Args:
        trending_topics: Full list of trending topics (sorted by trending score)
        total_keywords: Target number of keywords to return

    Returns:
        Balanced list of keywords with bullish, neutral, and bearish representation
    """
    # Separate topics by sentiment
    bullish = []
    neutral = []
    bearish = []
    no_sentiment = []

    for topic in trending_topics:
        sentiment = topic.get('avg_sentiment')
        if sentiment is None:
            no_sentiment.append(topic)
        elif sentiment >= BULLISH_THRESHOLD:
            bullish.append(topic)
        elif sentiment <= BEARISH_THRESHOLD:
            bearish.append(topic)
        else:
            neutral.append(topic)

    print(f"Sentiment distribution in {len(trending_topics)} topics:")
    print(f"   Bullish (>= +{BULLISH_THRESHOLD}): {len(bullish)}")
    print(f"   Neutral ({BEARISH_THRESHOLD} to +{BULLISH_THRESHOLD}): {len(neutral)}")
    print(f"   Bearish (<= {BEARISH_THRESHOLD}): {len(bearish)}")
    print(f"   No sentiment: {len(no_sentiment)}")

    # Select minimum required from each category
    selected = []
    selected_keywords = set()

    # Take top MIN_BULLISH bullish keywords (by trending score - already sorted)
    for topic in bullish[:MIN_BULLISH]:
        if topic['keyword'] not in selected_keywords:
            selected.append(topic)
            selected_keywords.add(topic['keyword'])
            print(f"   [+] BULLISH: {topic['keyword']} ({topic['avg_sentiment']:+.3f})")

    # Take top MIN_NEUTRAL neutral keywords
    for topic in neutral[:MIN_NEUTRAL]:
        if topic['keyword'] not in selected_keywords:
            selected.append(topic)
            selected_keywords.add(topic['keyword'])
            print(f"   [=] NEUTRAL: {topic['keyword']} ({topic['avg_sentiment']:+.3f})")

    # Take top MIN_BEARISH bearish keywords
    for topic in bearish[:MIN_BEARISH]:
        if topic['keyword'] not in selected_keywords:
            selected.append(topic)
            selected_keywords.add(topic['keyword'])
            print(f"   [-] BEARISH: {topic['keyword']} ({topic['avg_sentiment']:+.3f})")

    # Fill remaining slots with top trending topics (any sentiment)
    remaining_slots = total_keywords - len(selected)
    for topic in trending_topics:
        if remaining_slots <= 0:
            break
        if topic['keyword'] not in selected_keywords:
            selected.append(topic)
            selected_keywords.add(topic['keyword'])
            remaining_slots -= 1

    # Sort final selection by trending score
    selected.sort(key=lambda x: x['trending_score'], reverse=True)

    # Log final distribution
    final_bullish = sum(1 for t in selected if t.get('avg_sentiment') is not None and t['avg_sentiment'] >= BULLISH_THRESHOLD)
    final_neutral = sum(1 for t in selected if t.get('avg_sentiment') is not None and BEARISH_THRESHOLD < t['avg_sentiment'] < BULLISH_THRESHOLD)
    final_bearish = sum(1 for t in selected if t.get('avg_sentiment') is not None and t['avg_sentiment'] <= BEARISH_THRESHOLD)

    print(f"\nFinal word cloud selection ({len(selected)} keywords):")
    print(f"   Bullish: {final_bullish} | Neutral: {final_neutral} | Bearish: {final_bearish}")

    return selected


def save_report_to_s3(report: Dict) -> str:
    """Save report to S3 (dual output: Layer 3 + TopicCloud)"""

    # Archive path
    now = datetime.now()
    archive_key = f"trending_reports/{now.strftime('%Y/%m/%d')}/trending_report_{now.strftime('%H%M%S')}.json"

    # Latest path (for Layer 3)
    latest_key = "trending_reports/latest.json"

    report_json = json.dumps(report, indent=2, default=str)

    # Save archive
    s3_client.put_object(
        Bucket=S3_BUCKET,
        Key=archive_key,
        Body=report_json,
        ContentType='application/json'
    )

    # Save latest
    s3_client.put_object(
        Bucket=S3_BUCKET,
        Key=latest_key,
        Body=report_json,
        ContentType='application/json'
    )

    print(f"OK: Saved to S3:")
    print(f"   Archive: s3://{S3_BUCKET}/{archive_key}")
    print(f"   Latest:  s3://{S3_BUCKET}/{latest_key}")

    # =========================================================================
    # DUAL OUTPUT: TopicCloud keyword-sentiments-finbert.json (NOT used by portal - GPT version is primary)
    # =========================================================================
    # Format expected by portal TopicCloud component
    # Uses balanced selection to ensure minimum bullish/neutral/bearish representation

    print("\n" + "=" * 80)
    print("GENERATING BALANCED WORD CLOUD DATA")
    print("=" * 80)

    # Use balanced selection to ensure sentiment diversity
    balanced_topics = select_balanced_keywords(report['trending_topics'], total_keywords=50)

    # =========================================================================
    # SPORTS FILTER: Remove sports content before building keyword cloud
    # This is a financial portal -- sports content should never appear.
    # Uses word-boundary matching to avoid false positives (e.g. 'heat' in
    # "regulatory heat", 'bulls' in "bull market", 'nets' in "safety nets").
    # =========================================================================
    _TOPICCLOUD_SPORTS_KEYWORDS = [
        'nfl', 'nba', 'mlb', 'nhl', 'ncaa', 'football', 'basketball', 'baseball', 'hockey',
        'free agent', 'free agency', 'nfl trade', 'nfl draft', 'nfl free agency',
        'transfer portal', 'playoff', 'bowl game', 'super bowl', 'world series',
        'quarterback', 'wide receiver', 'running back', 'touchdown', 'home run',
        'franchise tag', 'salary cap', 'draft pick', 'roster move', 'trade deadline',
        'head coach', 'offensive coordinator', 'defensive coordinator',
        'season finale', 'regular season', 'postseason', 'halftime',
        'slam dunk', 'march madness',
        'ufc', 'mma', 'boxing match',
        # NFL teams
        'texans', 'cowboys', 'patriots', 'chiefs', 'steelers', 'ravens',
        'eagles', 'packers', '49ers', 'bengals', 'bills', 'broncos', 'colts',
        'titans', 'falcons', 'saints', 'panthers', 'buccaneers', 'bears',
        'lions', 'vikings', 'seahawks', 'rams', 'chargers', 'raiders',
        'jaguars', 'browns', 'commanders', 'giants', 'jets', 'dolphins',
        'cardinals', 'arizona cardinals',
        # NBA teams
        'lakers', 'celtics', 'knicks', 'warriors', 'heat', 'nets',
        'bucks', 'suns', 'nuggets', 'clippers', 'thunder', 'spurs',
        # MLB teams
        'yankees', 'dodgers', 'mets', 'red sox', 'cubs', 'braves',
        # College
        'michigan state', 'ohio state', 'penn state', 'alabama', 'clemson',
        'college football', 'college basketball',
        # Known athletes who generate sports noise
        'tyreek hill', 'patrick mahomes', 'travis kelce', 'lamar jackson',
        'josh allen', 'logan paul', 'dak prescott',
    ]
    _topiccloud_sports_pattern = re.compile(
        r'\b(' + '|'.join(re.escape(t) for t in _TOPICCLOUD_SPORTS_KEYWORDS) + r')\b',
        re.IGNORECASE
    )

    pre_sports_count = len(balanced_topics)
    sports_filtered = []
    non_sports = []
    for _t in balanced_topics:
        _kw = _t.get('keyword', '').lower()
        if _topiccloud_sports_pattern.search(_kw):
            sports_filtered.append(_kw)
        else:
            non_sports.append(_t)
    balanced_topics = non_sports
    if sports_filtered:
        print(f"BLOCKED: TopicCloud sports filter: removed {len(sports_filtered)} sports keywords: {sports_filtered}")

    # =========================================================================
    # PRE-FILTER: Apply previously learned dynamic stopwords BEFORE GPT validation
    # This ensures keywords flagged in previous runs don't slip through again
    # =========================================================================
    dynamic_stopwords = load_dynamic_stopwords()
    if dynamic_stopwords:
        pre_filter_count = len(balanced_topics)
        balanced_topics = [t for t in balanced_topics if t['keyword'].lower() not in dynamic_stopwords]
        filtered_count = pre_filter_count - len(balanced_topics)
        if filtered_count > 0:
            print(f"SKIP: Pre-filtered {filtered_count} keywords using {len(dynamic_stopwords)} learned stopwords")

    # Build initial keyword list
    keywords_list = [
        {
            'keyword': topic['keyword'],
            'sentiment': topic['avg_sentiment'] if topic['avg_sentiment'] is not None else 0,
            'count': topic['mention_count'],
            'rank': i + 1,
            # FIX: Use actual article distribution counts, not conditional total
            'bullish': topic.get('positive_count', 0),
            'bearish': topic.get('negative_count', 0),
            'neutral': topic.get('neutral_count', 0),
            # Pre-fetched cluster articles — lets keyword-intelligence-generator skip
            # the regex DynamoDB scan (which fails for multi-word cluster labels).
            # Top 10 by quality; fields normalised to KIG's expected schema.
            'articles': [
                {
                    'title':             a.get('title', ''),
                    'source':            a.get('source', ''),
                    'url':               a.get('url', ''),
                    'published':         a.get('published_at', ''),
                    'sentiment_finbert': a.get('sentiment') if a.get('has_sentiment') else None,
                    'summary':           '',
                }
                for a in topic.get('sample_articles', [])[:10]
            ],
        }
        for i, topic in enumerate(balanced_topics)
    ]

    # Apply size normalization for visual balance in word cloud
    # Uses log scale so 10 vs 100 mentions looks like 30% vs 100% size, not 10% vs 100%
    # TRUE counts preserved in 'count', normalized 'size' for display
    keywords_list = normalize_sizes_for_visibility(keywords_list)

    # GPT validation - final pass to catch any junk that slipped through
    # Also learns new stopwords and persists them to S3
    print("\nRunning GPT validation on keywords...")
    keywords_list = gpt_validate_keywords(keywords_list)

    keyword_sentiments = {
        'generated_at': report['generated_at'],
        'days_back': report['analysis_window_days'],
        'total_articles_scanned': report['total_articles'],
        'total_unique_keywords': len(keywords_list),
        'keywords': keywords_list
    }

    keyword_sentiments_json = json.dumps(keyword_sentiments, indent=2, default=str)

    # Write to json/sentiment/ path (canonical portal data path)
    s3_client.put_object(
        Bucket=S3_BUCKET_PORTAL,
        Key='json/sentiment/keyword-sentiments.json',
        Body=keyword_sentiments_json,
        ContentType='application/json'
    )

    print(f"   TopicCloud: s3://{S3_BUCKET_PORTAL}/json/sentiment/keyword-sentiments.json")

    return latest_key


# ============================================================================
# LAMBDA HANDLER
# ============================================================================

def lambda_handler(event, context):
    """
    Lambda handler for trending analysis

    Event parameters (all optional):
        days: Number of days to analyze (default: 7)
        top_n: Number of top topics to return (default: 30)
    """

    print("=" * 80)
    print("NEWS TRENDING ANALYSIS - V2 (PATTERN-BASED FILTERING)")
    print("=" * 80)
    print(f"Time: {datetime.now(timezone.utc).isoformat()}")
    print(f"Stopwords: {len(ALL_STOPWORDS)} words (NLTK + Finance)")
    print()

    # Get parameters from event
    days = event.get('days', DAYS_BACK)
    top_n = event.get('top_n', TOP_N_TOPICS)

    print(f"Parameters: days={days}, top_n={top_n}")
    print()

    try:
        # Step 1: Load articles
        articles = load_articles_from_dynamodb(days)

        if not articles:
            return {
                'statusCode': 200,
                'body': json.dumps({
                    'message': 'No articles found',
                    'articles_analyzed': 0,
                    'trending_topics': 0
                })
            }

        # Step 2: Embed + cluster trending topics (falls back to keyword if hdbscan unavailable)
        trending_topics, cluster_similarities = embed_and_cluster_topics(articles, top_n)

        # Step 3: Generate report
        report = generate_report(articles, trending_topics, cluster_similarities)

        # Step 4: Save to S3
        s3_key = save_report_to_s3(report)

        # Step 5: Kick off keyword intelligence generation immediately
        # The intelligence must be pre-computed for exactly the same keywords
        # that were just decided and written to keyword-sentiments.json.
        # We invoke async (Event) so it runs in parallel without blocking this return.
        try:
            lambda_client = boto3.client('lambda', region_name='us-east-1')
            lambda_client.invoke(
                FunctionName='keyword-intelligence-generator',
                InvocationType='Event',  # async — fire and forget
                Payload=b'{}'
            )
            print("OK: keyword-intelligence-generator invoked (async)")
        except Exception as e:
            # Non-fatal — portal falls back to live computation if cache misses
            print(f"WARN: Could not invoke keyword-intelligence-generator: {e}")

        # Step 6: Chain-invoke Layer 3 GPT curation
        # Layer 3 reads the trending_reports/latest.json we just wrote to S3,
        # curates 10 bullish + 10 bearish topics via GPT, and writes to DynamoDB.
        # Async invocation — Layer 3 will in turn chain-invoke the portal publisher.
        try:
            if not lambda_client:
                lambda_client = boto3.client('lambda', region_name='us-east-1')
            lambda_client.invoke(
                FunctionName='opal-news-layer3-curation',
                InvocationType='Event',  # async — fire and forget
                Payload=b'{}'
            )
            print("OK: opal-news-layer3-curation invoked (async, chained)")
        except Exception as e:
            # Non-fatal — EventBridge schedule is the fallback
            print(f"WARN: Could not invoke opal-news-layer3-curation: {e}")

        print()
        print("=" * 80)
        print("OK: ANALYSIS COMPLETE")
        print("=" * 80)
        print(f"Articles analyzed: {len(articles)}")
        print(f"Trending topics: {len(trending_topics)}")
        print(f"Output: s3://{S3_BUCKET}/{s3_key}")

        return {
            'statusCode': 200,
            'body': json.dumps({
                'message': 'Trending analysis complete',
                'articles_analyzed': len(articles),
                'trending_topics': len(trending_topics),
                's3_key': s3_key,
                'generated_at': report['generated_at']
            })
        }

    except Exception as e:
        print(f"ERROR: {str(e)}")
        import traceback
        traceback.print_exc()

        return {
            'statusCode': 500,
            'body': json.dumps({
                'error': str(e),
                'message': 'Trending analysis failed'
            })
        }


# For local testing
if __name__ == '__main__':
    result = lambda_handler({}, None)
    print(json.dumps(json.loads(result['body']), indent=2))
