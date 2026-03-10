#!/usr/bin/env python3
"""
Layer 3: GPT-Powered Topic Curation Lambda with Web Research Enrichment
========================================================================

Phase 1: Intelligently curate top 10 bullish + top 10 bearish topics from Layer 2's
trending analysis using GPT-4o.

Phase 2-7: Enrich selected topics with web research, validate claims, and add citations

Input:
- Top 25 trending topics from Layer 2 (S3: trending_reports/latest.json)

Output:
- 20 fully-enriched topic rows in DynamoDB (opal-news-trending-daily)
- Each row includes: GPT headline, analysis, citations, sentiment scores, sources, articles

Author: Andrew Berman
Date: 2025-11-22
"""

import boto3
import json
import os
import re
from datetime import datetime, timedelta
from typing import List, Dict, Optional, Tuple
from decimal import Decimal
import hashlib

# OpenAI SDK
try:
    from openai import OpenAI
except ImportError:
    print("WARNING:  OpenAI SDK not installed. Run: pip install openai")
    OpenAI = None

# Enhanced enrichment module
try:
    import enhanced_enrichment
except ImportError:
    print("WARNING:  enhanced_enrichment module not found")
    enhanced_enrichment = None

# AWS clients - use DATA_REGION for cross-region access (data is in us-east-1)
DATA_REGION = os.environ.get('DATA_REGION', 'us-east-1')
s3_client = boto3.client('s3', region_name=DATA_REGION)
dynamodb = boto3.resource('dynamodb', region_name=DATA_REGION)
secrets_client = boto3.client('secretsmanager', region_name=DATA_REGION)

# Configuration
S3_BUCKET = os.environ.get('S3_BUCKET', 'opal-data-news-av')
SOURCE_TABLE = os.environ.get('SOURCE_TABLE', 'opal-news-articles')
TARGET_TABLE = os.environ.get('TARGET_TABLE', 'opal-news-trending-daily')
OPENAI_SECRET_NAME = os.environ.get('OPENAI_SECRET_NAME', 'openai-api-key')
GPT_MODEL = os.environ.get('GPT_MODEL', 'gpt-4o')
MAX_TOKENS = int(os.environ.get('MAX_TOKENS', '16000'))  # Increased to ensure all 20 topics get full 150-200 word analysis
TEMPERATURE = float(os.environ.get('TEMPERATURE', '0.7'))

# =============================================================================
# TOP 20 KEYWORDS - Portal Word Cloud Integration
# =============================================================================
# These are the keywords displayed in the portal's word cloud.
# Layer 3 should prefer selecting topics that map to these keywords
# so the word cloud has sentiment scores (not zeros).

TOP_20_KEYWORDS = [
    'ai', 'war', 'tech', 'bitcoin', 'crypto', 'trump', 'fed', 'nvidia',
    'china', 'energy', 'jobs', 'euro', 'retail', 'oil', 'inflation',
    'google', 'consumer', 'nasdaq'
]

# Mapping from Layer 2 keywords (verbose) to TOP_20 keywords (normalized)
# This ensures DynamoDB stores keywords that match the portal's expectations
KEYWORD_NORMALIZATION = {
    # AI variants
    'artificial intelligence': 'ai',
    'machine learning': 'ai',
    'generative ai': 'ai',
    'chatgpt': 'ai',
    'openai': 'ai',

    # Fed variants
    'federal reserve': 'fed',
    'rate cut': 'fed',
    'rate hike': 'fed',
    'interest rate': 'fed',
    'fomc': 'fed',
    'powell': 'fed',

    # Jobs variants
    'jobs report': 'jobs',
    'unemployment': 'jobs',
    'unemployment rate': 'jobs',
    'labor market': 'jobs',
    'employment': 'jobs',
    'nonfarm payrolls': 'jobs',

    # Crypto variants
    'bitcoin': 'bitcoin',
    'btc': 'bitcoin',
    'cryptocurrency': 'crypto',
    'coinbase': 'crypto',
    'ethereum': 'crypto',

    # Tech variants
    'technology': 'tech',
    'semiconductor': 'tech',
    'software': 'tech',

    # Energy variants
    'oil prices': 'oil',
    'crude oil': 'oil',
    'opec': 'oil',
    'natural gas': 'energy',
    'renewable': 'energy',

    # Direct mappings (already in TOP_20)
    'nvidia': 'nvidia',
    'trump': 'trump',
    'china': 'china',
    'inflation': 'inflation',
    'google': 'google',
    'nasdaq': 'nasdaq',
    'retail': 'retail',
    'consumer': 'consumer',
    'euro': 'euro',
    'war': 'war',
}


def normalize_keyword(keyword: str) -> str:
    """
    Normalize a keyword to match TOP_20_KEYWORDS for portal integration.

    Args:
        keyword: Original keyword from Layer 2/GPT

    Returns:
        Normalized keyword (from TOP_20) or original if no mapping exists
    """
    keyword_lower = keyword.lower().strip()

    # Check direct mapping (exact match)
    if keyword_lower in KEYWORD_NORMALIZATION:
        return KEYWORD_NORMALIZATION[keyword_lower]

    # Check if already a TOP_20 keyword
    if keyword_lower in TOP_20_KEYWORDS:
        return keyword_lower

    # Check if any KEYWORD_NORMALIZATION phrase appears in the keyword
    # (e.g., "federal reserve policy" contains "federal reserve" -> "fed")
    # Sort by length (longest first) to match most specific phrases
    for phrase in sorted(KEYWORD_NORMALIZATION.keys(), key=len, reverse=True):
        if phrase in keyword_lower:
            return KEYWORD_NORMALIZATION[phrase]

    # Check partial matches using word boundaries
    # (e.g., "nvidia earnings" should map to "nvidia")
    # Use word boundaries to prevent "ai" matching in "retail"
    for top_kw in TOP_20_KEYWORDS:
        pattern = re.compile(rf'\b{re.escape(top_kw)}\b', re.IGNORECASE)
        if pattern.search(keyword_lower):
            return top_kw

    # No normalization found - return original
    return keyword_lower


# =============================================================================
# AWS HELPERS
# =============================================================================

def get_secret(secret_name: str) -> str:
    """Retrieve secret from AWS Secrets Manager"""
    try:
        response = secrets_client.get_secret_value(SecretId=secret_name)
        return response['SecretString']
    except Exception as e:
        print(f"ERROR: Error retrieving secret {secret_name}: {e}")
        raise


def convert_decimals_to_floats(obj):
    """Convert DynamoDB Decimals to Python floats for JSON serialization"""
    if isinstance(obj, list):
        return [convert_decimals_to_floats(i) for i in obj]
    elif isinstance(obj, dict):
        return {k: convert_decimals_to_floats(v) for k, v in obj.items()}
    elif isinstance(obj, Decimal):
        return float(obj)
    else:
        return obj


def convert_floats_to_decimals(obj):
    """Convert Python floats to DynamoDB Decimals"""
    if isinstance(obj, list):
        return [convert_floats_to_decimals(i) for i in obj]
    elif isinstance(obj, dict):
        return {k: convert_floats_to_decimals(v) for k, v in obj.items()}
    elif isinstance(obj, float):
        return Decimal(str(obj))
    else:
        return obj


# =============================================================================
# S3 LOADER
# =============================================================================

def load_latest_trending_report() -> Dict:
    """
    Load the latest trending report from Layer 2

    Returns:
        dict: Trending report with top 25 topics
    """
    try:
        # Load latest trending report
        key = 'trending_reports/latest.json'

        print(f"LOADING: Loading trending report from s3://{S3_BUCKET}/{key}")

        obj = s3_client.get_object(Bucket=S3_BUCKET, Key=key)
        report = json.loads(obj['Body'].read().decode('utf-8'))

        # Convert Decimals to floats
        report = convert_decimals_to_floats(report)

        topics = report.get('trending_topics', [])
        cluster_similarities = report.get('cluster_similarities', [])
        print(f"OK: Loaded {len(topics)} trending topics from Layer 2 "
              f"({len(cluster_similarities)} cluster similarity pairs)\n")

        return report

    except Exception as e:
        print(f"ERROR: Error loading trending report: {e}")
        raise


# =============================================================================
# WEIGHTED COMPOSITE SCORING
# =============================================================================

import math

def calculate_composite_score(topic: Dict, direction: str = 'bullish', max_mentions: int = 200) -> Optional[float]:
    """
    Calculate weighted composite score for GPT ranking.

    Combines three factors:
    1. Article coverage (log-scaled) - more coverage = more significant
    2. Sentiment strength with direction preference
    3. Recency (time decay) - newer news preferred

    Args:
        topic: Topic dict with mention_count, avg_sentiment, avg_time_decay
        direction: 'bullish' or 'bearish' - affects sentiment scoring
        max_mentions: Maximum mention count for normalization

    Returns:
        Composite score 0-1, or None if no FinBERT data

    Weights:
        - articles: 0.30 (coverage matters but diminishing returns)
        - sentiment: 0.45 (strongest signal for financial relevance)
        - recency: 0.25 (prefer recent but not dominant)
    """
    mentions = topic.get('mention_count') or 1  # Handle None explicitly
    finbert = topic.get('avg_sentiment')
    time_decay = topic.get('avg_time_decay') or 0.5  # Handle None explicitly

    # Skip topics with no FinBERT data
    if finbert is None:
        return None

    # 1. Article score: log-scaled, normalized 0-1
    # log(10) ~ 2.3, log(200) ~ 5.3
    # Scale so 10 articles = 0.43, 50 = 0.74, 200 = 1.0
    article_score = math.log(max(mentions, 1) + 1) / math.log(max(max_mentions, 10) + 2)
    article_score = min(article_score, 1.0)  # Cap at 1.0

    # 2. Sentiment score with direction preference
    if direction == 'bullish':
        # Bullish: +1.0 -> 1.0, 0.0 -> 0.5, -1.0 -> 0.0
        sentiment_score = (finbert + 1) / 2
    else:
        # Bearish: -1.0 -> 1.0, 0.0 -> 0.5, +1.0 -> 0.0
        sentiment_score = (1 - finbert) / 2

    # 3. Recency score (already 0-1, higher = more recent)
    recency_score = time_decay

    # Weighted composite
    composite = (
        0.30 * article_score +
        0.45 * sentiment_score +
        0.25 * recency_score
    )

    return composite


# =============================================================================
# FINBERT RANKING-BASED FILTERING
# =============================================================================

# Minimum requirements for a valid topic
MIN_ARTICLE_COUNT = 1  # Must have at least 1 article

# FinBERT direction constraints - STRICT separation
# Bullish pool: ONLY positive sentiment (FinBERT > 0)
# Bearish pool: ONLY negative sentiment (FinBERT < 0)
BULLISH_FINBERT_MIN = 0.0   # Bullish topics must have FinBERT > 0
BEARISH_FINBERT_MAX = 0.0   # Bearish topics must have FinBERT < 0

def prefilter_topics_by_finbert(trending_topics: List[Dict]) -> Dict[str, List[Dict]]:
    """
    Rank topics by weighted composite score combining articles, sentiment, and recency.

    Instead of using fixed thresholds (which can result in empty pools), we:
    1. Filter out SPORTS topics (we don't care about sports at all)
    2. Filter out topics with no FinBERT data (avg_sentiment is None)
    3. Filter out topics with no articles (article_count = 0)
    4. Calculate weighted composite score for each direction
    5. Sort by composite score (higher = better candidate for that direction)

    Composite Score Formula:
        0.30 * log(articles)  +  0.45 * sentiment_direction  +  0.25 * recency

    This ensures we ALWAYS have topics to work with, using intelligent ranking.

    Args:
        trending_topics: Top 25 topics from Layer 2

    Returns:
        dict: {
            'bullish_candidates': [...],    # Sorted by bullish composite score
            'bearish_candidates': [...],    # Sorted by bearish composite score
            'all_valid': [...]              # All valid topics
        }
    """
    # Sports keywords to filter out - WE DON'T CARE ABOUT SPORTS AT ALL
    # NOTE: Use word-boundary matching (\b) to avoid false positives like:
    # 'heat' matching "regulatory heat", 'bulls' matching "bull market",
    # 'nets' matching "safety nets", 'division' matching "financial division"
    sports_keywords = [
        'nfl', 'nba', 'mlb', 'nhl', 'ncaa', 'football', 'basketball', 'baseball', 'hockey',
        'free agent', 'free agency', 'nfl trade', 'nfl draft', 'nfl free agency',
        'transfer portal', 'playoff', 'bowl game', 'super bowl', 'world series',
        'quarterback', 'wide receiver', 'running back', 'touchdown', 'home run',
        'franchise tag', 'salary cap', 'draft pick', 'roster move', 'trade deadline',
        'head coach', 'offensive coordinator', 'defensive coordinator',
        'season finale', 'regular season', 'postseason', 'halftime',
        'slam dunk', 'nba slam', 'march madness',
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
        'tyreek hill', 'logan paul', 'patrick mahomes', 'travis kelce',
        'lamar jackson', 'josh allen', 'dak prescott',
    ]
    # Compile once for efficiency
    sports_pattern = re.compile(
        r'\b(' + '|'.join(re.escape(t) for t in sports_keywords) + r')\b'
    )

    valid_topics = []
    skipped_no_finbert = []
    skipped_no_articles = []
    skipped_sports = []

    for topic in trending_topics:
        finbert = topic.get('avg_sentiment')
        mentions = topic.get('mention_count', 0)
        keyword = topic.get('keyword', 'N/A')
        keyword_lower = keyword.lower()

        # SPORTS FILTER - word-boundary match to avoid false positives
        is_sports = bool(sports_pattern.search(keyword_lower))

        # Also check sample article headlines for sports content
        if not is_sports:
            sample_articles = topic.get('sample_articles', [])
            for article in sample_articles[:3]:  # Check first 3 headlines
                headline = (article.get('title', '') or '').lower()
                if sports_pattern.search(headline):
                    is_sports = True
                    break

        if is_sports:
            skipped_sports.append(keyword)
            print(f"   BLOCKED: SPORTS REJECTED: {keyword} ({mentions} mentions)")
            continue

        # Skip topics with no FinBERT data
        if finbert is None:
            skipped_no_finbert.append(keyword)
            print(f"   SKIP:  SKIP (no FinBERT): {keyword} ({mentions} mentions)")
            continue

        # Skip topics with no articles
        if mentions < MIN_ARTICLE_COUNT:
            skipped_no_articles.append(keyword)
            print(f"   SKIP:  SKIP (no articles): {keyword}")
            continue

        valid_topics.append(topic)

    # Get max mentions for normalization (use `or 1` to handle None values)
    max_mentions = max((t.get('mention_count') or 1 for t in valid_topics), default=100)

    # Calculate composite scores for each topic
    for topic in valid_topics:
        topic['bullish_score'] = calculate_composite_score(topic, 'bullish', max_mentions)
        topic['bearish_score'] = calculate_composite_score(topic, 'bearish', max_mentions)

    # CRITICAL: Filter by FinBERT direction BEFORE sorting - STRICT SEPARATION
    # Bullish pool: ONLY topics with FinBERT > 0 (strictly positive)
    # This ensures GPT can ONLY select from genuinely positive-sentiment topics
    bullish_pool = [t for t in valid_topics if (t.get('avg_sentiment') or 0) > BULLISH_FINBERT_MIN]

    # Bearish pool: ONLY topics with FinBERT < 0 (strictly negative)
    # This ensures GPT can ONLY select from genuinely negative-sentiment topics
    bearish_pool = [t for t in valid_topics if (t.get('avg_sentiment') or 0) < BEARISH_FINBERT_MAX]

    # Sort by composite score within each pool
    bullish_candidates = sorted(
        bullish_pool,
        key=lambda x: x.get('bullish_score', 0) or 0,
        reverse=True
    )

    bearish_candidates = sorted(
        bearish_pool,
        key=lambda x: x.get('bearish_score', 0) or 0,
        reverse=True
    )

    print(f"\n   WARNING:  STRICT DIRECTION CONSTRAINTS:")
    print(f"      Bullish pool (FinBERT > {BULLISH_FINBERT_MIN}): {len(bullish_pool)} topics")
    print(f"      Bearish pool (FinBERT < {BEARISH_FINBERT_MAX}): {len(bearish_pool)} topics")

    # Log all valid topics in ranked order (by bullish score)
    print(f"\n   STAT: Valid topics ranked by COMPOSITE SCORE:")
    print(f"      {'Rank':4} {'Keyword':25} {'Bull':6} {'Bear':6} {'FinBERT':8} {'Articles':8} {'Recency':8}")
    print(f"      {'-'*70}")
    for i, topic in enumerate(bullish_candidates, 1):
        kw = topic.get('keyword', 'N/A')[:24]
        fb = topic.get('avg_sentiment', 0.0)
        bull = topic.get('bullish_score', 0) or 0
        bear = topic.get('bearish_score', 0) or 0
        mentions = topic.get('mention_count', 0)
        decay = topic.get('avg_time_decay', 0.5)
        print(f"      {i:4}. {kw:25} {bull:.3f}  {bear:.3f}  {fb:+.3f}   {mentions:6}   {decay:.2f}")

    print(f"\n   STAT: Pre-filter results:")
    print(f"      Total topics: {len(trending_topics)}")
    print(f"      Valid (have FinBERT + articles): {len(valid_topics)}")
    print(f"      BLOCKED: SPORTS REJECTED: {len(skipped_sports)}")
    print(f"      Skipped (no FinBERT): {len(skipped_no_finbert)}")
    print(f"      Skipped (no articles): {len(skipped_no_articles)}")
    print(f"      Max article count (for normalization): {max_mentions}\n")

    # Log top 5 candidates for each direction
    print(f"   OK: TOP 5 BULLISH candidates (by composite score):")
    for t in bullish_candidates[:5]:
        print(f"      - {t.get('keyword')}: {t.get('bullish_score', 0):.3f} (FinBERT: {t.get('avg_sentiment', 0):+.3f})")
    print(f"   TOP BEARISH: TOP 5 BEARISH candidates (by composite score):")
    for t in bearish_candidates[:5]:
        print(f"      - {t.get('keyword')}: {t.get('bearish_score', 0):.3f} (FinBERT: {t.get('avg_sentiment', 0):+.3f})")

    return {
        'bullish_candidates': bullish_candidates,
        'bearish_candidates': bearish_candidates,
        'all_valid': valid_topics
    }


# =============================================================================
# POST-GPT VALIDATION (Layer 3 Defense)
# =============================================================================

def calculate_word_overlap(headline1: str, headline2: str) -> float:
    """
    Calculate word-for-word overlap between two headlines

    Returns:
        Percentage of words that match (0.0 to 1.0)
    """
    # Normalize both headlines
    words1 = re.sub(r'[^\w\s]', '', headline1.lower()).split()
    words2 = re.sub(r'[^\w\s]', '', headline2.lower()).split()

    if not words1 or not words2:
        return 0.0

    # Count matching words
    matches = sum(1 for w in words1 if w in words2)

    # Calculate overlap as percentage of shorter headline
    shorter_length = min(len(words1), len(words2))
    return matches / shorter_length if shorter_length > 0 else 0.0


def detect_and_merge_duplicates(topics: List[Dict], sentiment_label: str) -> List[Dict]:
    """
    Detect and merge duplicate topics based on:
    1. Matching layer2_keyword or original_keyword (KEYWORD DUPLICATES)
    2. 50%+ headline word overlap (HEADLINE DUPLICATES)

    When topics are merged:
    - Keep shorter/clearer headline
    - Combine article lists (deduplicate by URL)
    - Merge sources
    - Merge keywords
    - Average sentiment scores

    Args:
        topics: List of topics from GPT
        sentiment_label: 'bullish' or 'bearish' (for logging)

    Returns:
        Merged list of unique topics
    """
    if not topics:
        return []

    # Track which topics have been merged
    merged_indices = set()
    merged_topics = []

    for i, topic1 in enumerate(topics):
        if i in merged_indices:
            continue  # Already merged into another topic

        headline1 = topic1.get('headline', '').strip()
        keyword1_layer2 = topic1.get('layer2_keyword', '').lower().strip()
        keyword1_original = topic1.get('original_keyword', '').lower().strip()
        merged_into_current = [topic1]

        # Check for duplicates
        for j, topic2 in enumerate(topics[i+1:], start=i+1):
            if j in merged_indices:
                continue

            headline2 = topic2.get('headline', '').strip()
            keyword2_layer2 = topic2.get('layer2_keyword', '').lower().strip()
            keyword2_original = topic2.get('original_keyword', '').lower().strip()

            # CHECK 1: Keyword duplicates (same layer2_keyword or original_keyword)
            is_keyword_duplicate = False
            if keyword1_layer2 and keyword2_layer2 and keyword1_layer2 == keyword2_layer2:
                is_keyword_duplicate = True
                print(f"  MERGE: Merging duplicate {sentiment_label} topics (same layer2_keyword: '{keyword1_layer2}'):")
            elif keyword1_original and keyword2_original and keyword1_original == keyword2_original:
                is_keyword_duplicate = True
                print(f"  MERGE: Merging duplicate {sentiment_label} topics (same original_keyword: '{keyword1_original}'):")

            # CHECK 2: Headline word overlap (50%+)
            overlap = calculate_word_overlap(headline1, headline2)
            is_headline_duplicate = overlap >= 0.5

            if is_keyword_duplicate or is_headline_duplicate:
                if is_headline_duplicate and not is_keyword_duplicate:
                    print(f"  MERGE: Merging duplicate {sentiment_label} topics ({overlap:.0%} headline overlap):")
                print(f"     Topic 1: {headline1[:60]}...")
                print(f"     Topic 2: {headline2[:60]}...")
                merged_into_current.append(topic2)
                merged_indices.add(j)

        # Merge all duplicates into one topic
        if len(merged_into_current) > 1:
            merged_topic = merge_topics(merged_into_current, sentiment_label)
            merged_topics.append(merged_topic)
            print(f"     OK: Merged {len(merged_into_current)} topics into: {merged_topic.get('headline', '')[:60]}...")
        else:
            merged_topics.append(topic1)

    print(f"  STAT: {sentiment_label.capitalize()} topics: {len(topics)} -> {len(merged_topics)} (merged {len(topics) - len(merged_topics)})")
    return merged_topics


def merge_topics(topics: List[Dict], sentiment_label: str) -> Dict:
    """
    Merge multiple duplicate topics into one

    Strategy:
    - Headline: Keep the shortest one (usually clearest)
    - Articles: Combine and deduplicate by URL
    - Sources: Merge unique sources
    - Keywords: Merge (prefer layer2_keyword if available)
    - Sentiment: Average the scores
    - Analysis: Combine the analyses
    """
    # Choose best headline (shortest)
    topics_sorted = sorted(topics, key=lambda t: len(t.get('headline', '')))
    best_topic = topics_sorted[0]

    # Merge articles (deduplicate by URL)
    all_articles = []
    seen_urls = set()
    for topic in topics:
        for article in topic.get('articles', []):
            url = article.get('url', '')
            if url and url not in seen_urls:
                all_articles.append(article)
                seen_urls.add(url)

    # Merge sources
    all_sources = []
    seen_sources = set()
    for topic in topics:
        for source in topic.get('sources', []):
            if source and source not in seen_sources:
                all_sources.append(source)
                seen_sources.add(source)

    # Merge keywords (prefer layer2_keyword, fallback to original_keyword)
    keywords = set()
    for topic in topics:
        if topic.get('layer2_keyword'):
            keywords.add(topic['layer2_keyword'])
        elif topic.get('original_keyword'):
            keywords.add(topic['original_keyword'])

    # Average sentiment scores
    sentiment_scores = [topic.get('sentiment_score', 0) for topic in topics if topic.get('sentiment_score')]
    avg_sentiment = sum(sentiment_scores) / len(sentiment_scores) if sentiment_scores else 0

    # Combine analyses
    analyses = [topic.get('analysis', '') for topic in topics if topic.get('analysis')]
    combined_analysis = ' '.join(analyses) if len(analyses) > 1 else (analyses[0] if analyses else '')

    # Build merged topic
    merged = best_topic.copy()
    merged.update({
        'articles': all_articles,
        'sources': all_sources,
        'article_count': len(all_articles),
        'source_count': len(all_sources),
        'sentiment_score': avg_sentiment,
        'analysis': combined_analysis,
        'merged_keywords': list(keywords),
        'merged_from_count': len(topics)
    })

    return merged


def backfill_from_layer2(
    curated_topics: List[Dict],
    layer2_topics: List[Dict],
    target_count: int,
    sentiment_filter: str,
    gpt_client: OpenAI = None
) -> List[Dict]:
    """
    Backfill topics from Layer 2 to reach target count

    If merging reduced our topic count below target (10), pull additional
    topics from Layer 2 trending data that weren't already selected by GPT.

    Args:
        curated_topics: Topics already selected by GPT (after merging)
        layer2_topics: All trending topics from Layer 2
        target_count: Target number of topics (usually 10)
        sentiment_filter: 'bullish' or 'bearish'

    Returns:
        List with additional topics to reach target_count
    """
    # Sports keywords to filter out - WE DON'T CARE ABOUT SPORTS
    # Word-boundary matching to avoid false positives (see primary filter above)
    sports_keywords = [
        'nfl', 'nba', 'mlb', 'nhl', 'ncaa', 'football', 'basketball', 'baseball', 'hockey',
        'free agent', 'free agency', 'nfl trade', 'nfl draft', 'nfl free agency',
        'transfer portal', 'playoff', 'bowl game', 'super bowl', 'world series',
        'quarterback', 'wide receiver', 'running back', 'touchdown', 'home run',
        'franchise tag', 'salary cap', 'draft pick', 'roster move', 'trade deadline',
        'head coach', 'offensive coordinator', 'defensive coordinator',
        'season finale', 'regular season', 'postseason', 'halftime',
        'slam dunk', 'nba slam', 'march madness',
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
        'tyreek hill', 'logan paul', 'patrick mahomes', 'travis kelce',
        'lamar jackson', 'josh allen', 'dak prescott',
    ]
    sports_pattern = re.compile(
        r'\b(' + '|'.join(re.escape(t) for t in sports_keywords) + r')\b'
    )

    current_count = len(curated_topics)

    if current_count >= target_count:
        return []  # Already at target

    needed = target_count - current_count
    print(f"\nBULLISH: Backfilling {needed} {sentiment_filter} topics from Layer 2...")

    # Get keywords already used by curated topics
    used_keywords = set()
    for topic in curated_topics:
        used_keywords.add(topic.get('layer2_keyword', '').lower())
        used_keywords.add(topic.get('original_keyword', '').lower())
        if 'merged_keywords' in topic:
            used_keywords.update(k.lower() for k in topic['merged_keywords'])

    # Filter Layer 2 topics by sentiment (using avg_sentiment FinBERT score) and exclude already used keywords
    available_topics = []
    for layer2_topic in layer2_topics:
        keyword = layer2_topic.get('keyword', '').lower()
        avg_sentiment = layer2_topic.get('avg_sentiment') or 0.0  # Handle None explicitly

        # SPORTS FILTER - word-boundary match to avoid false positives
        is_sports = bool(sports_pattern.search(keyword))

        # Also check sample article headlines for sports content
        sample_articles = layer2_topic.get('sample_articles', [])
        for article in sample_articles[:3]:  # Check first 3 headlines
            headline = (article.get('title', '') or '').lower()
            if sports_pattern.search(headline):
                is_sports = True
                break

        if is_sports:
            print(f"  BLOCKED: SPORTS REJECTED: {keyword}")
            continue

        # Classify as bullish/bearish based on FinBERT score
        is_bullish = avg_sentiment > 0
        is_bearish = avg_sentiment < 0

        # Skip if wrong sentiment or already used
        if sentiment_filter.lower() == 'bullish' and not is_bullish:
            continue
        if sentiment_filter.lower() == 'bearish' and not is_bearish:
            continue
        if keyword in used_keywords:
            continue

        available_topics.append(layer2_topic)

    # Sort by trend_score (highest first)
    # Use `or 0` to handle None values (get() default only applies if key is missing)
    available_topics.sort(key=lambda t: t.get('trend_score') or 0, reverse=True)

    # Take top N needed topics and return them with real headlines from Layer 2
    backfill_topics = []
    for layer2_topic in available_topics[:needed]:
        keyword = layer2_topic.get('keyword', 'Unknown')
        sample_articles = layer2_topic.get('sample_articles', [])

        # Get the best headline from actual articles (highest quality score)
        if sample_articles:
            # Sort by quality score, take the best
            # Use `or 0` to handle None values
            sorted_articles = sorted(
                sample_articles,
                key=lambda a: a.get('quality_score') or 0,
                reverse=True
            )
            best_headline = sorted_articles[0].get('title', f"{keyword.title()}: Trending market topic")
        else:
            # Fallback if no articles available (shouldn't happen)
            best_headline = f"{keyword.title()}: Trending market topic"

        # Get source count for analysis
        sources = set([a.get('newsapi_source_name') or a.get('source', '') for a in sample_articles if a.get('newsapi_source_name') or a.get('source')])
        source_count = len(sources)

        # Generate GPT analysis for this backfilled topic
        gpt_analysis = {'subtext': '', 'analysis': ''}
        if gpt_client:
            print(f"  GPT: Generating GPT analysis for '{keyword}'...")
            gpt_analysis = generate_single_topic_analysis(
                headline=best_headline,
                keyword=keyword,
                sentiment_direction=sentiment_filter,
                sample_articles=sample_articles,
                client=gpt_client
            )
            if gpt_analysis.get('subtext'):
                print(f"     OK Subtext: {gpt_analysis['subtext'][:50]}...")
        else:
            # Fallback if no GPT client available
            gpt_analysis = {
                'subtext': '',
                'analysis': f"Trending {sentiment_filter} topic with {layer2_topic.get('mention_count', 0)} mentions across {source_count} sources"
            }

        # Create GPT-style wrapper with real headline and GPT analysis
        wrapped_topic = {
            'gpt_topic': {
                'topic_name': keyword.title(),
                'headline': best_headline,  # OK: Real article headline
                'subtext': gpt_analysis.get('subtext', ''),
                'analysis': gpt_analysis.get('analysis', ''),
                'layer2_keyword': keyword,
                'original_keyword': keyword,
                'backfilled': True,
                'confidence_level': 'medium',  # Backfilled topics have medium confidence
                'rationale': f"Selected from Layer 2 trending analysis based on high trend score"
            },
            'layer2_topic': layer2_topic  # Preserve full Layer 2 data
        }
        backfill_topics.append(wrapped_topic)
        print(f"  OK: Backfilled: {keyword} -> \"{best_headline[:60]}...\"")

    return backfill_topics


def validate_gpt_topic_selection(gpt_topic: Dict, original_layer2_topic: Dict) -> Tuple[bool, str]:
    """
    Validate GPT's topic selection against spam patterns
    Run AFTER GPT returns curated topics as final defense layer

    This catches cases where GPT over-justifies spam as financially relevant.

    Args:
        gpt_topic: Topic selected by GPT (with headline, analysis, etc.)
        original_layer2_topic: Original Layer 2 topic data

    Returns:
        (is_valid, rejection_reason)

    Rejection criteria:
    0. SPORTS - Absolute rejection (we don't care about sports at all)
    1. Spam headline patterns ("Complete Guide", "How to", etc.)
    2. Low-quality sources (Shopify, tutorial sites)
    """
    headline = gpt_topic.get('headline', '')
    topic_name = gpt_topic.get('topic_name', '')
    keyword = gpt_topic.get('layer2_keyword', '') or gpt_topic.get('original_keyword', '')
    sources = original_layer2_topic.get('sample_articles', [])

    # Check 0: SPORTS - Absolute rejection (highest priority)
    # Word-boundary matching to avoid false positives (heat=Miami Heat not "regulatory heat",
    # nets=NBA Nets not "safety nets", division=NBA division not "financial division", etc.)
    sports_keywords = [
        'nfl', 'nba', 'mlb', 'nhl', 'ncaa', 'football', 'basketball', 'baseball', 'hockey',
        'free agent', 'free agency', 'nfl trade', 'nfl draft', 'nfl free agency',
        'transfer portal', 'playoff', 'bowl game', 'super bowl', 'world series',
        'quarterback', 'wide receiver', 'running back', 'touchdown', 'home run',
        'franchise tag', 'salary cap', 'draft pick', 'roster move', 'trade deadline',
        'head coach', 'offensive coordinator', 'defensive coordinator',
        'season finale', 'regular season', 'postseason', 'halftime',
        'game score', 'final score', 'slam dunk', 'nba slam', 'march madness',
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
        'tyreek hill', 'logan paul', 'patrick mahomes', 'travis kelce',
        'lamar jackson', 'josh allen', 'dak prescott',
    ]
    sports_pattern = re.compile(
        r'\b(' + '|'.join(re.escape(t) for t in sports_keywords) + r')\b'
    )

    text_to_check = f"{headline} {topic_name} {keyword}".lower()
    if sports_pattern.search(text_to_check):
        matched = sports_pattern.search(text_to_check).group(1)
        return (False, f"SPORTS REJECTED: Contains '{matched}' - we don't care about sports")

    # Check 1: Spam headline patterns
    spam_patterns = [
        r'Complete Guide',
        r'Ultimate Guide',
        r'Definitive Guide',
        r'\d+ Things',
        r'\d+ Ways',
        r'How [Tt]o',
        r'You Won\'?t Believe',
    ]

    for pattern in spam_patterns:
        if re.search(pattern, headline, re.IGNORECASE):
            return (False, f"Spam headline pattern: {pattern}")

    # Check 2: Source quality - check sample article sources
    spam_sources = {'shopify', 'wix', 'squarespace', 'tutorial', 'wikihow', 'medium.com/@'}
    source_names = [
        article.get('source', '').lower()
        for article in sources[:10]  # Check first 10 articles
    ]

    spam_source_count = sum(
        1 for source in source_names
        if any(spam in source for spam in spam_sources)
    )

    # If >30% of sources are spam sources, reject
    if spam_source_count > 0 and spam_source_count / max(len(source_names), 1) > 0.3:
        return (False, f"High spam source ratio: {spam_source_count}/{len(source_names)} articles from spam sources")

    # Check 3 REMOVED (2026-02-24): keyword-in-article-title relevance check.
    # Layer 2 keywords are GPT-generated semantic cluster labels (e.g. "axogen earnings",
    # "japan growth pledge") that rarely appear verbatim in article titles. This check
    # was rejecting 90%+ of valid curated topics. Sports filter (Check 0) and spam
    # filters (Checks 1-2) provide sufficient defense.

    return (True, "Passed validation")


# =============================================================================
# GPT PROMPT BUILDER
# =============================================================================

def build_curation_prompt(trending_topics: List[Dict], prefiltered: Dict[str, List[Dict]] = None, cluster_similarities: List[Dict] = None) -> str:
    """
    Build GPT prompt for intelligent topic curation using pre-filtered pools.

    Args:
        trending_topics: Top 25 topics from Layer 2 (fallback if prefiltered not provided)
        prefiltered: Pre-filtered pools by FinBERT score
        cluster_similarities: Pairwise cosine similarity list from Layer 2 embedding step

    Returns:
        Formatted prompt string
    """

    def format_topic(topic: Dict, idx: int, direction: str = 'bullish') -> str:
        """Format a single topic for the prompt with composite score"""
        keyword = topic.get('keyword', 'N/A')
        mention_count = topic.get('mention_count', 0)
        trending_score = topic.get('trending_score', 0)
        finbert = topic.get('avg_sentiment') or 0.0
        avg_quality = topic.get('avg_quality', 50.0)
        time_decay = topic.get('avg_time_decay', 0.5)  # 1.0 = today, lower = older

        # Get pre-calculated composite score
        if direction == 'bullish':
            composite = topic.get('bullish_score', 0) or 0
        else:
            composite = topic.get('bearish_score', 0) or 0

        # Show top 2 sample articles
        sample_articles = topic.get('sample_articles', [])[:2]
        article_details = ""
        for article in sample_articles:
            title = article.get('title', 'N/A')
            summary = article.get('summary', '')
            art_finbert = article.get('sentiment') or article.get('sentiment_finbert') or 0.0
            source = article.get('source', '')
            pub_date = article.get('published_at', '')[:10] if article.get('published_at') else ''
            article_details += f"     - [{pub_date}] {title} (Source: {source})\n"
            article_details += f"       FinBERT: {art_finbert:+.3f}\n"
            if summary:
                article_details += f"       Summary: {summary[:150]}...\n"

        cluster_id = topic.get('cluster_id')
        cluster_label = f"  CLUSTER_ID={cluster_id}" if cluster_id is not None else ""
        result = f"\n{idx}. LAYER2_KEYWORD=\"{keyword}\"{cluster_label}  STAR: RELEVANCE: {composite:.3f}\n"
        result += f"   Articles: {mention_count} | FinBERT: {finbert:+.3f} | Recency: {time_decay:.2f}\n"
        result += f"   Quality: {avg_quality:.1f} | Trending Score: {trending_score:.2f}\n"
        result += f"   Sample Articles:\n{article_details}"
        return result

    prompt = """You are a senior market analyst at Opal Capital. Your task is to select the TOP 10 BULLISH and TOP 10 BEARISH topics that are FINANCIALLY RELEVANT to portfolio managers.

WARNING:  FINANCIAL RELEVANCE IS MANDATORY
=====================================
SKIP any topic that is NOT relevant to financial markets, investing, or the economy.

Examples to SKIP (ABSOLUTE REJECTION - NO EXCEPTIONS):
- BLOCKED: SPORTS: NFL, NBA, MLB, NHL, NCAA, college football, transfer portal,
  coaching changes, game scores, player trades, playoffs, bowl games,
  Steelers, Patriots, any team names, wide receiver, quarterback, etc.
  WE DO NOT CARE ABOUT SPORTS AT ALL. NEVER SELECT SPORTS TOPICS.
- Entertainment (celebrity gossip, movie/TV news)
- Local news (crime, accidents, human interest)
- Political scandals without direct market impact

Examples to INCLUDE:
- Fed policy, inflation, economic data
- Company earnings, M&A, IPOs
- Crypto/stock market movements
- Trade policy, tariffs, sanctions
- Major corporate news (earnings, layoffs, deals)

STAR: RELEVANCE SCORE EXPLAINED
=============================
Each topic has a pre-calculated RELEVANCE score (0-1) that combines:
- Article coverage (30%) - more articles = more significant
- Sentiment strength (45%) - stronger sentiment = clearer signal
- Recency (25%) - newer news preferred

Higher relevance = better candidate for that pool. Use this to guide your selection,
but you MAY skip high-relevance topics if they are NOT financially relevant.

WARNING:  SELECTION STRATEGY - MAXIMIZE COVERAGE
==========================================
YOU MUST SELECT AS MANY TOPICS AS POSSIBLE (up to 10 per pool).

ONLY skip a topic if it is TRULY:
- Sports (NFL, NBA, etc.) - ABSOLUTE REJECTION
- Entertainment/celebrity news
- Local crime/accidents

DO NOT skip topics just because they seem "generic" or "broad" -
if it has market implications, SELECT IT.

The pools are pre-sorted by relevance. Your job is to:
1. Select UP TO 10 topics from each pool
2. Only reject topics that are genuinely non-financial
3. Most topics in these pools ARE financially relevant - select them!

"""

    # Get sorted pools
    bullish_pool = prefiltered.get('bullish_candidates', []) if prefiltered else []
    bearish_pool = prefiltered.get('bearish_candidates', []) if prefiltered else []

    # Show BULLISH POOL (sorted by bullish composite score)
    if bullish_pool:
        prompt += f"\n{'='*60}\n"
        prompt += f"BULLISH: BULLISH CANDIDATE POOL (sorted by bullish relevance)\n"
        prompt += f"Select TOP 10 financially-relevant topics from this pool\n"
        prompt += f"{'='*60}\n"

        for i, topic in enumerate(bullish_pool, 1):
            prompt += format_topic(topic, i, 'bullish')
    else:
        prompt += "\nWARNING:  NO BULLISH CANDIDATES AVAILABLE\n"

    # Show BEARISH POOL (sorted by bearish composite score)
    if bearish_pool:
        prompt += f"\n\n{'='*60}\n"
        prompt += f"BEARISH: BEARISH CANDIDATE POOL (sorted by bearish relevance)\n"
        prompt += f"Select TOP 10 financially-relevant topics from this pool\n"
        prompt += f"{'='*60}\n"

        for i, topic in enumerate(bearish_pool, 1):
            prompt += format_topic(topic, i, 'bearish')
    else:
        prompt += "\nWARNING:  NO BEARISH CANDIDATES AVAILABLE\n"

    # Add semantic similarity section if available
    if cluster_similarities:
        top_pairs = cluster_similarities[:20]
        # Build a cluster_id -> keyword lookup from the trending topics
        id_to_kw = {t.get('cluster_id'): t.get('keyword', f'cluster_{t.get("cluster_id")}')
                    for t in trending_topics if 'cluster_id' in t}

        prompt += f"\n\n{'='*60}\n"
        prompt += "SEMANTIC: SEMANTIC CLUSTER RELATIONSHIPS (top 20 pairs)\n"
        prompt += "These pairs have high embedding similarity -- they describe related or overlapping stories.\n"
        prompt += f"{'='*60}\n"
        prompt += "cluster_id_a | keyword_a | cluster_id_b | keyword_b | similarity\n"
        prompt += "-" * 70 + "\n"
        for pair in top_pairs:
            cid_a = pair['cluster_a']
            cid_b = pair['cluster_b']
            kw_a = id_to_kw.get(cid_a, f'cluster_{cid_a}')
            kw_b = id_to_kw.get(cid_b, f'cluster_{cid_b}')
            sim = pair['similarity']
            prompt += f"  {cid_a:4d}  \"{kw_a}\"  <->  {cid_b:4d}  \"{kw_b}\"  ->  {sim:.3f}\n"

        prompt += """
WARNING:  DIVERSITY RULE -- USE THIS DATA:
- Pairs with similarity > 0.60 are likely describing the SAME underlying story from different angles.
  Do NOT select both topics from such a pair (e.g., "Fed rate cut" and "Treasury yield drop" in the
  same direction). Pick the stronger one and skip the near-duplicate.
- Pairs with similarity 0.40-0.60 are related but distinct -- you MAY select both if they offer
  meaningfully different angles.
- Reference topics by their cluster_id (shown as CLUSTER_ID in the pools above) to cross-check
  pairs against the candidate lists.
- Goal: maximize topical diversity in your final 10 bullish + 10 bearish selections.
"""

    prompt += """

WARNING:  CRITICAL: LAYER2_KEYWORD MUST BE PRESERVED EXACTLY
Each topic in the input shows LAYER2_KEYWORD="..." - you MUST return this EXACT string
in the "layer2_keyword" field. This is how we link back to the article data.
DO NOT normalize, shorten, or change the layer2_keyword in any way.

OUTPUT FORMAT (JSON) - SIMPLIFIED FOR SPEED:
==========================================
We will generate detailed analysis in a separate step. For now, just select topics
and provide a brief headline. Keep your output CONCISE.

{
  "bullish": [
    {
      "layer2_keyword": "nvidia",
      "original_keyword": "nvidia",
      "headline": "Nvidia Reports Strong Q4 Earnings Beat",
      "rationale": "Strong AI chip demand driving revenue growth"
    }
    // SELECT UP TO 10 bullish topics
  ],
  "bearish": [
    {
      "layer2_keyword": "trump",
      "original_keyword": "trump",
      "headline": "Trump Trade Policy Uncertainty Weighs on Markets",
      "rationale": "Tariff concerns impacting global trade sentiment"
    }
    // SELECT UP TO 10 bearish topics
  ]
}

PORTAL KEYWORD PREFERENCE (for original_keyword):
ai, war, tech, bitcoin, crypto, trump, fed, nvidia, china, energy,
jobs, euro, retail, oil, inflation, google, consumer, nasdaq

CRITICAL:
1. SELECT AS MANY TOPICS AS POSSIBLE - aim for 10 per pool
2. Only reject genuine sports/entertainment - NOT "generic" financial topics
3. Copy layer2_keyword EXACTLY from input
4. Keep headlines factual (from article titles, not predictions)
5. Keep rationale brief (1 sentence)
"""

    return prompt


# =============================================================================
# GPT CURATION
# =============================================================================

def curate_topics_with_gpt(trending_topics: List[Dict], cluster_similarities: List[Dict] = None) -> Dict:
    """
    Use GPT-4o to intelligently curate top 10 bullish + top 10 bearish topics

    Args:
        trending_topics: Top 25 topics from Layer 2
        cluster_similarities: Pairwise cosine similarity list from Layer 2 embedding step

    Returns:
        dict: {
            "bullish": [10 topics with GPT analysis],
            "bearish": [10 topics with GPT analysis]
        }
    """

    print(f"{'='*100}")
    print("GPT-4O TOPIC CURATION")
    print(f"{'='*100}\n")

    # Step 1: Pre-filter topics by FinBERT score
    print("STAT: Pre-filtering topics by FinBERT score...")
    prefiltered = prefilter_topics_by_finbert(trending_topics)

    # Get OpenAI API key
    api_key = get_secret(OPENAI_SECRET_NAME)
    client = OpenAI(api_key=api_key)

    # Build prompt with pre-filtered pools and cluster similarity context
    prompt = build_curation_prompt(trending_topics, prefiltered, cluster_similarities or [])

    print(f"SENDING: Sending {len(trending_topics)} topics to GPT-4o for curation...")
    print(f"   Model: {GPT_MODEL}")
    print(f"   Max tokens: {MAX_TOKENS}")
    print(f"   Temperature: {TEMPERATURE}\n")

    try:
        # Call GPT-4o
        response = client.chat.completions.create(
            model=GPT_MODEL,
            messages=[
                {
                    "role": "system",
                    "content": """You are selecting market topics for a financial news portal.

YOUR GOAL: Select UP TO 10 bullish and UP TO 10 bearish topics from the provided pools.

ONLY REJECT topics that are:
BLOCKED: SPORTS (NFL, NBA, MLB, NHL, NCAA, college football, team names, player trades)
BLOCKED: Entertainment/celebrity news
BLOCKED: Spam/tutorial content ("Complete Guide to...", "How to...")

ALL other topics are FINANCIAL and should be SELECTED.

Topics about stocks, crypto, Fed policy, trade, companies, commodities, economic data,
geopolitics with market impact - SELECT THEM ALL.

IMPORTANT:
- Copy layer2_keyword EXACTLY from input (do not modify it)
- Use actual article headlines, not predictions
- Respond with valid JSON"""
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            max_completion_tokens=MAX_TOKENS,
            temperature=TEMPERATURE,
            response_format={"type": "json_object"}
        )

        # Parse response
        content = response.choices[0].message.content
        curated = json.loads(content)

        # Validate structure
        if 'bullish' not in curated or 'bearish' not in curated:
            raise ValueError("GPT response missing 'bullish' or 'bearish' keys")

        if len(curated['bullish']) != 10 or len(curated['bearish']) != 10:
            print(f"WARNING:  Warning: Expected 10 bullish + 10 bearish, got {len(curated['bullish'])} + {len(curated['bearish'])}")

        print(f"OK: GPT topic selection complete")
        print(f"   Bullish topics selected: {len(curated['bullish'])}")
        print(f"   Bearish topics selected: {len(curated['bearish'])}")
        print(f"   Tokens used: {response.usage.total_tokens}\n")

        # PHASE 2: Generate detailed analysis for each selected topic
        print(f"{'='*60}")
        print("PHASE 2: GENERATING DETAILED ANALYSIS FOR EACH TOPIC")
        print(f"{'='*60}\n")

        # Build lookup for Layer 2 topics by keyword
        layer2_lookup = {t.get('keyword', '').lower(): t for t in trending_topics}

        # Generate analysis for bullish topics
        for i, topic in enumerate(curated['bullish'], 1):
            keyword = topic.get('layer2_keyword', '')
            headline = topic.get('headline', '')
            layer2_topic = layer2_lookup.get(keyword.lower(), {})
            sample_articles = layer2_topic.get('sample_articles', [])

            print(f"BULLISH: Generating analysis for bullish-{i}: {keyword}...")
            analysis_result = generate_single_topic_analysis(
                headline=headline,
                keyword=keyword,
                sentiment_direction='bullish',
                sample_articles=sample_articles,
                client=client
            )
            topic['subtext'] = analysis_result.get('subtext', '')
            topic['analysis'] = analysis_result.get('analysis', '')
            if topic['subtext']:
                print(f"   OK Subtext: {topic['subtext'][:50]}...")

        # Generate analysis for bearish topics
        for i, topic in enumerate(curated['bearish'], 1):
            keyword = topic.get('layer2_keyword', '')
            headline = topic.get('headline', '')
            layer2_topic = layer2_lookup.get(keyword.lower(), {})
            sample_articles = layer2_topic.get('sample_articles', [])

            print(f"BEARISH: Generating analysis for bearish-{i}: {keyword}...")
            analysis_result = generate_single_topic_analysis(
                headline=headline,
                keyword=keyword,
                sentiment_direction='bearish',
                sample_articles=sample_articles,
                client=client
            )
            topic['subtext'] = analysis_result.get('subtext', '')
            topic['analysis'] = analysis_result.get('analysis', '')
            if topic['subtext']:
                print(f"   OK Subtext: {topic['subtext'][:50]}...")

        print(f"\nOK: Analysis generation complete for {len(curated['bullish']) + len(curated['bearish'])} topics\n")

        return curated

    except Exception as e:
        print(f"ERROR: Error calling GPT: {e}")
        raise


def generate_single_topic_analysis(
    headline: str,
    keyword: str,
    sentiment_direction: str,
    sample_articles: List[Dict],
    client: OpenAI
) -> Dict[str, str]:
    """
    Generate subtext and analysis for a single topic using GPT.

    This is called for backfilled topics or topics that didn't get full analysis
    in the main curation call due to token limits.

    Args:
        headline: The topic headline
        keyword: The topic keyword
        sentiment_direction: 'bullish' or 'bearish'
        sample_articles: List of sample articles for context
        client: OpenAI client instance

    Returns:
        dict with 'subtext' and 'analysis' keys
    """
    # Build article context (top 3 articles)
    article_context = ""
    for i, article in enumerate(sample_articles[:3], 1):
        title = article.get('title', 'N/A')
        source = article.get('newsapi_source_name') or article.get('source', 'Unknown')
        summary = article.get('summary', '')[:200] if article.get('summary') else ''
        article_context += f"{i}. [{source}] {title}\n"
        if summary:
            article_context += f"   Summary: {summary}...\n"

    prompt = f"""Generate a brief subtext and analysis for this {sentiment_direction} market topic.

HEADLINE: {headline}
KEYWORD: {keyword}

SAMPLE ARTICLES:
{article_context}

Respond in JSON format:
{{
    "subtext": "Brief 5-10 word tagline summarizing the story",
    "analysis": "150-200 word analysis explaining the {sentiment_direction} market implications. Be specific about affected sectors, potential price movements, and investment considerations."
}}

RULES:
1. subtext should be a brief, punchy tagline (like a newspaper subheadline)
2. analysis should explain WHY this is {sentiment_direction} for markets
3. Only cite facts from the provided articles - no hallucination
4. Focus on actionable market insights for portfolio managers"""

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",  # Use mini for individual calls (faster, cheaper)
            messages=[
                {
                    "role": "system",
                    "content": "You are a senior market analyst writing brief market commentary. Be concise and actionable."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            max_tokens=500,
            temperature=0.7,
            response_format={"type": "json_object"}
        )

        result = json.loads(response.choices[0].message.content)
        return {
            'subtext': result.get('subtext', ''),
            'analysis': result.get('analysis', '')
        }

    except Exception as e:
        print(f"  WARNING:  GPT analysis failed for '{keyword}': {e}")
        return {
            'subtext': '',
            'analysis': f"Trending {sentiment_direction} topic based on {len(sample_articles)} recent articles."
        }


# =============================================================================
# METADATA ENRICHMENT
# =============================================================================

def enrich_topic_with_metadata(
    gpt_topic: Dict,
    original_topic: Dict,
    rank: str,
    date: str
) -> Dict:
    """
    Enrich GPT-curated topic with full metadata from Layer 2

    Args:
        gpt_topic: GPT-generated topic with headline, analysis, etc.
        original_topic: Original topic from Layer 2 with all scores
        rank: Topic rank (e.g., "bullish-1", "bearish-2")
        date: Date string (YYYY-MM-DD)

    Returns:
        dict: Fully enriched topic ready for DynamoDB
    """

    sentiment = original_topic.get('sentiment_all_articles', {})

    # Calculate velocity/momentum (placeholder - would compare to previous day)
    # For now, just mark as "steady" since we don't have historical data yet
    velocity = 1.0
    momentum = "steady"

    # Extract FinBERT score (most important financial sentiment metric)
    # FinBERT is called 'sentiment_score' in individual articles
    finbert_score = 0.0

    # Try to get FinBERT from aggregated data first
    # Layer 2 provides 'avg_sentiment' which is the FinBERT score
    # Note: avg_sentiment can be None for topics with no FinBERT-scored articles
    if original_topic.get('avg_sentiment') is not None:
        finbert_score = original_topic.get('avg_sentiment')
        print(f"  OK Using avg_sentiment from Layer 2: {finbert_score:.4f}")
    elif 'avg_sentiment' in original_topic and original_topic.get('avg_sentiment') is None:
        print(f"  WARNING:  avg_sentiment is None (no FinBERT data for this topic)")
    elif 'avg_finbert_score' in original_topic:
        finbert_score = original_topic.get('avg_finbert_score', 0.0)
    elif 'finbert' in sentiment:
        finbert_score = sentiment.get('finbert', 0.0)
    else:
        # Calculate FinBERT by querying articles with matching keyword
        try:
            keyword = original_topic.get('keyword', '')
            mention_count = original_topic.get('mention_count', 0)

            if keyword and mention_count > 0:
                # Query articles table for this keyword
                articles_table = dynamodb.Table(SOURCE_TABLE)
                response = articles_table.scan(
                    FilterExpression='attribute_exists(#k) AND contains(#k, :val)',
                    ExpressionAttributeNames={'#k': 'keywords_raw'},
                    ExpressionAttributeValues={':val': keyword},
                    ProjectionExpression='sentiment_score,keywords_raw',
                    Limit=200  # Fetch more since we'll filter with word boundaries
                )

                # FIX: Post-filter with word boundaries to avoid false matches
                # e.g., "ai" should NOT match in "retail", "details", etc.
                keyword_pattern = re.compile(r'\b' + re.escape(keyword) + r'\b', re.IGNORECASE)

                finbert_scores = []
                for item in response.get('Items', []):
                    # Verify keyword matches as whole word, not substring
                    keywords_raw = item.get('keywords_raw', '')
                    if not keyword_pattern.search(keywords_raw):
                        continue  # Skip - keyword is substring match only (e.g., "ai" in "retail")

                    fb_score = item.get('sentiment_score')
                    if fb_score is not None:
                        finbert_scores.append(float(Decimal(fb_score) if isinstance(fb_score, Decimal) else fb_score))

                if finbert_scores:
                    finbert_score = sum(finbert_scores) / len(finbert_scores)
                    print(f"  OK Calculated FinBERT from {len(finbert_scores)} articles for '{keyword}': {finbert_score:.4f}")
        except Exception as e:
            print(f"  WARNING:  Could not calculate FinBERT from articles: {e}")

    enriched = {
        # Primary keys
        'date': date,
        'topic_rank': rank,

        # GPT-generated content
        'topic_name': gpt_topic.get('topic_name', ''),
        'headline': gpt_topic.get('headline', ''),
        'subtext': gpt_topic.get('subtext', ''),
        'analysis': gpt_topic.get('analysis', ''),

        # Sentiment scores (FinBERT primary + 6 dimensions from Layer 2)
        'sentiment': {
            'finbert': finbert_score,  # PRIMARY: FinBERT financial sentiment (-1.0 to 1.0)
            'bullish_bearish': sentiment.get('bull_bear', 0.0),
            'confidence_fear': sentiment.get('confidence_fear', 0.0),
            'positive_negative': sentiment.get('positive_negative', 0.0),
            'risk_appetite': sentiment.get('risk_appetite', 0.0),
            'legal_risk': sentiment.get('legal_risk', 0.0),
            'emotional_intensity': sentiment.get('emotional_intensity', 0.0)
        },

        # Momentum & relevance scores
        'trending_score': original_topic.get('trending_score', 0.0),
        'avg_time_decay': original_topic.get('avg_time_decay', 0.0),
        'avg_escalation_score': 0.0,  # TODO: Calculate from escalated articles
        'avg_quality_score': original_topic.get('avg_quality', 50.0),
        'velocity': velocity,
        'momentum': momentum,

        # Article metadata
        'article_count': original_topic.get('mention_count', 0),
        # Use newsapi_source_name (actual publication) if available, fall back to source field
        'source_count': len(set([
            a.get('newsapi_source_name') or a.get('source', '')
            for a in original_topic.get('sample_articles', [])
        ])),
        'sources': list(set([
            a.get('newsapi_source_name') or a.get('source', '')
            for a in original_topic.get('sample_articles', [])
            if (a.get('newsapi_source_name') or a.get('source', ''))  # Filter out empty strings
        ])),

        # Sample articles - preserve all source data including URLs and publication dates
        'top_articles': [
            {
                'headline': a.get('title', ''),  # Portal expects 'headline'
                # Use actual publication name (newsapi_source_name) if available
                'source': a.get('newsapi_source_name') or a.get('source', ''),
                'url': a.get('url', '') or a.get('link', ''),  # Check 'url' first, fall back to 'link' for legacy articles
                'published': a.get('published_at') or a.get('published') or '',  # Try both field names
                'quality_score': float(a.get('quality_score') or 50.0),
                'escalation_score': float(a.get('escalation_score') or 0.0),
                'finbert_score': float(a.get('sentiment') or 0.0)  # Layer 2 uses 'sentiment' field
            }
            for a in original_topic.get('sample_articles', [])[:100]  # Top 100 articles (was 5)
        ],

        # GPT metadata
        'confidence_level': gpt_topic.get('confidence_level', 'medium'),
        'market_implication': gpt_topic.get('market_implication', ''),
        'rationale': gpt_topic.get('rationale', ''),
        'affected_sectors': gpt_topic.get('affected_sectors', []),
        'affected_tickers': gpt_topic.get('affected_tickers', []),

        # Web research enrichment (Phases 2-7)
        'citations': gpt_topic.get('citations', []),
        'initial_analysis': gpt_topic.get('initial_analysis', ''),
        'enhancement_metadata': gpt_topic.get('enhancement_metadata', {}),

        # System metadata
        'created_at': datetime.utcnow().isoformat() + 'Z',
        'layer2_trending_rank': 0,  # TODO: Find original rank in top 25
        'gpt_model': GPT_MODEL,
        # Normalize keyword to match TOP_20 for portal word cloud integration
        'original_keyword': normalize_keyword(
            gpt_topic.get('original_keyword', original_topic.get('keyword', ''))
        ),
        # Keep raw keyword for debugging/audit
        'raw_keyword': gpt_topic.get('original_keyword', original_topic.get('keyword', ''))
    }

    return enriched


# =============================================================================
# DYNAMODB WRITER
# =============================================================================

def check_existing_topics(date: str) -> bool:
    """
    Check if topics already exist for this date

    Args:
        date: Date string (YYYY-MM-DD)

    Returns:
        True if any topics exist for this date, False otherwise
    """
    table = dynamodb.Table(TARGET_TABLE)

    try:
        response = table.scan(
            FilterExpression='#d = :date',
            ExpressionAttributeNames={'#d': 'date'},
            ExpressionAttributeValues={':date': date},
            Limit=1  # Only need to know if ANY exist
        )

        exists = len(response.get('Items', [])) > 0

        if exists:
            print(f"INFO: Found existing topics for {date}")
        else:
            print(f"INFO: No existing topics for {date}")

        return exists

    except Exception as e:
        print(f"WARNING:  Error checking existing topics: {e}")
        return False  # If check fails, proceed with processing


def clear_existing_topics(date: str) -> int:
    """
    Delete all existing topics for this date before writing new ones

    This ensures Lambda is idempotent - running multiple times produces
    the same clean result, not accumulated duplicates.

    Uses blind deletes (trying all possible ranks) to avoid eventual
    consistency issues with DynamoDB scans.

    Args:
        date: Date string (YYYY-MM-DD)

    Returns:
        Number of topics deleted
    """
    table = dynamodb.Table(TARGET_TABLE)

    try:
        # Blind delete all possible topic ranks to avoid scan eventual consistency issues
        # Try bullish-1 through bullish-15 and bearish-1 through bearish-15
        deleted_count = 0

        for sentiment in ['bullish', 'bearish']:
            for i in range(1, 16):  # Try up to 15 to catch any overflow
                rank = f"{sentiment}-{i}"
                try:
                    table.delete_item(
                        Key={
                            'topic_rank': rank,
                            'date': date
                        }
                    )
                    deleted_count += 1
                except table.meta.client.exceptions.ResourceNotFoundException:
                    # Item doesn't exist, that's fine
                    pass
                except Exception as e:
                    # Some other error, but continue trying other ranks
                    if 'ResourceNotFoundException' not in str(e):
                        print(f"  WARNING:  Error deleting {rank}: {e}")

        if deleted_count > 0:
            print(f"DELETE:  Cleared {deleted_count} existing topics for {date}")
        else:
            print(f"DELETE:  No existing topics to clear for {date}")

        return deleted_count

    except Exception as e:
        print(f"ERROR: Error clearing existing topics: {e}")
        raise


def write_to_dynamodb(enriched_topics: List[Dict]) -> None:
    """
    Write enriched topics to DynamoDB table

    Args:
        enriched_topics: List of 6 fully enriched topics
    """

    print(f"{'='*100}")
    print(f"WRITING TO DYNAMODB: {TARGET_TABLE}")
    print(f"{'='*100}\n")

    table = dynamodb.Table(TARGET_TABLE)

    for topic in enriched_topics:
        date = topic['date']
        rank = topic['topic_rank']
        name = topic['topic_name']

        try:
            # Convert floats to Decimals for DynamoDB
            item = convert_floats_to_decimals(topic)

            # Write to table
            table.put_item(Item=item)

            print(f"OK: Wrote {rank}: {name}")

        except Exception as e:
            print(f"ERROR: Error writing {rank} ({name}): {e}")
            raise

    print(f"\nOK: Successfully wrote {len(enriched_topics)} topics to DynamoDB\n")


# =============================================================================
# MAIN LAMBDA HANDLER
# =============================================================================

def lambda_handler(event, context):
    """
    Main Lambda handler for Layer 3 curation

    Event parameters:
        date (optional): Date to process (YYYY-MM-DD), defaults to today
        force_refresh (optional): If true, regenerate even if topics exist. Defaults to false.
    """

    print(f"\n{'='*100}")
    print("LAYER 3: GPT-POWERED TOPIC CURATION")
    print(f"{'='*100}\n")

    # Get date from event or use today
    date = event.get('date', datetime.utcnow().strftime('%Y-%m-%d'))
    force_refresh = event.get('force_refresh', False)

    print(f"DATE: Processing date: {date}")
    print(f"REFRESH: Force refresh: {force_refresh}\n")

    try:
        # OPTION 2: Idempotency Check - Skip if already processed (unless force_refresh=true)
        if not force_refresh:
            if check_existing_topics(date):
                print(f"\nSKIP: Topics already exist for {date}. Skipping processing.")
                print(f"   HINT: To regenerate, invoke with: {{'date': '{date}', 'force_refresh': true}}\n")

                # Still chain-invoke the publisher so portal picks up any pending data
                try:
                    lambda_client = boto3.client('lambda', region_name='us-east-1')
                    lambda_client.invoke(
                        FunctionName='opal-trending-topics-portal-publisher',
                        InvocationType='Event',
                        Payload=b'{}'
                    )
                    print("OK: Portal publisher invoked (data already exists, ensuring publish)")
                except Exception as e:
                    print(f"WARN: Could not invoke portal publisher: {e}")

                return {
                    'statusCode': 200,
                    'body': json.dumps({
                        'message': 'Topics already exist for this date',
                        'date': date,
                        'skipped': True,
                        'hint': 'Use force_refresh=true to regenerate'
                    })
                }

        # OPTION 1: Clear Before Write - Delete existing topics to prevent duplicates
        print(f"\nDELETE:  Clearing any existing topics for {date}...")
        cleared = clear_existing_topics(date)
        if cleared > 0:
            print(f"   Cleared {cleared} topics to ensure clean regeneration\n")

        # Step 1: Load Layer 2 trending report
        trending_report = load_latest_trending_report()
        trending_topics = trending_report.get('trending_topics', [])
        cluster_similarities = trending_report.get('cluster_similarities', [])

        if not trending_topics:
            raise ValueError("No trending topics found in Layer 2 report")

        # Step 2: Curate with GPT (Phase 1)
        curated = curate_topics_with_gpt(trending_topics, cluster_similarities)

        # Step 2.1: Detect and merge duplicate topics (50%+ word overlap)
        print(f"\nCHECKING: Detecting and merging duplicate topics...")
        original_bullish_count = len(curated.get('bullish', []))
        original_bearish_count = len(curated.get('bearish', []))

        curated['bullish'] = detect_and_merge_duplicates(curated.get('bullish', []), 'bullish')
        curated['bearish'] = detect_and_merge_duplicates(curated.get('bearish', []), 'bearish')

        # Step 2.2: Fill in missing analysis for topics that GPT didn't fully process (token limits)
        print("\nFIXING: Checking for topics with missing analysis...")
        try:
            api_key = get_secret(OPENAI_SECRET_NAME)
            analysis_client = OpenAI(api_key=api_key)

            for sentiment_type, topics in [('bullish', curated.get('bullish', [])), ('bearish', curated.get('bearish', []))]:
                for topic in topics:
                    analysis = topic.get('analysis', '')
                    subtext = topic.get('subtext', '')

                    # Check if analysis is missing or too short (less than 50 chars is likely incomplete)
                    needs_analysis = not analysis or len(analysis) < 50
                    needs_subtext = not subtext or len(subtext) < 5

                    if needs_analysis or needs_subtext:
                        keyword = topic.get('layer2_keyword', topic.get('original_keyword', 'Unknown'))
                        headline = topic.get('headline', '')

                        # Find matching Layer 2 topic for article context
                        matching_layer2 = None
                        for l2_topic in trending_topics:
                            if l2_topic.get('keyword', '').lower() == keyword.lower():
                                matching_layer2 = l2_topic
                                break

                        sample_articles = matching_layer2.get('sample_articles', []) if matching_layer2 else []

                        print(f"  GPT: Generating missing analysis for '{keyword}'...")
                        gpt_result = generate_single_topic_analysis(
                            headline=headline,
                            keyword=keyword,
                            sentiment_direction=sentiment_type,
                            sample_articles=sample_articles,
                            client=analysis_client
                        )

                        if needs_subtext and gpt_result.get('subtext'):
                            topic['subtext'] = gpt_result['subtext']
                            print(f"     OK Added subtext: {gpt_result['subtext'][:50]}...")

                        if needs_analysis and gpt_result.get('analysis') and len(gpt_result['analysis']) > 50:
                            topic['analysis'] = gpt_result['analysis']
                            print(f"     OK Added analysis ({len(gpt_result['analysis'])} chars)")

            print("OK: Missing analysis check complete\n")
        except Exception as e:
            print(f"WARNING:  Could not fill missing analysis: {e}\n")

        # Step 2.5: Web Research Enrichment (Phases 2-7) - OPTIONAL
        # Set ENABLE_WEB_ENRICHMENT env var to activate
        enable_enrichment = os.environ.get('ENABLE_WEB_ENRICHMENT', 'false').lower() == 'true'
        if enable_enrichment and enhanced_enrichment:
            print("ENRICHING: Starting web research enrichment (Phases 2-7)...\n")

            # Prepare topics for enrichment
            topics_for_enrichment = []
            for gpt_topic in curated.get('bullish', []) + curated.get('bearish', []):
                topics_for_enrichment.append({
                    'headline': gpt_topic.get('headline', ''),
                    'analysis': gpt_topic.get('analysis', ''),
                    'sentiment': gpt_topic.get('confidence_level', 'medium'),
                    'original_data': gpt_topic
                })

            # Run enrichment (pass date for 30-day filtering)
            try:
                enriched_topics_from_research = enhanced_enrichment.enrich_topics(
                    topics_for_enrichment,
                    search_date=date
                )

                # Merge enrichment results back into curated topics
                for i, enriched in enumerate(enriched_topics_from_research):
                    if i < len(curated['bullish']):
                        curated['bullish'][i].update({
                            'analysis': enriched.get('analysis', curated['bullish'][i].get('analysis', '')),
                            'citations': enriched.get('citations', []),
                            'enhancement_metadata': enriched.get('enhancement_metadata', {})
                        })
                    else:
                        idx = i - len(curated['bullish'])
                        if idx < len(curated['bearish']):
                            curated['bearish'][idx].update({
                                'analysis': enriched.get('analysis', curated['bearish'][idx].get('analysis', '')),
                                'citations': enriched.get('citations', []),
                                'enhancement_metadata': enriched.get('enhancement_metadata', {})
                            })

                print("OK: Web research enrichment complete\n")
            except Exception as e:
                print(f"WARNING:  Web enrichment failed (continuing without enrichment): {e}\n")
        else:
            if not enhanced_enrichment:
                print("WARNING:  enhanced_enrichment module not available (skipping Phases 2-7)\n")
            else:
                print("INFO:  Web enrichment disabled (set ENABLE_WEB_ENRICHMENT=true to enable)\n")

        # Step 3: Enrich with metadata and prepare for DynamoDB
        enriched_topics = []

        # Helper function to find matching Layer 2 topic
        def find_layer2_topic(gpt_topic: Dict, trending_topics: List[Dict]) -> Dict:
            """
            Find the matching Layer 2 topic for a GPT-curated topic.

            Matching priority:
            1. Exact match on layer2_keyword (preferred - should always work)
            2. Exact match on original_keyword (fallback)
            3. Fuzzy match - keyword contains or is contained by Layer 2 keyword
            """
            layer2_keyword = gpt_topic.get('layer2_keyword', '').lower().strip()
            original_keyword = gpt_topic.get('original_keyword', '').lower().strip()

            # Priority 1: Exact match on layer2_keyword
            if layer2_keyword:
                for t in trending_topics:
                    if t.get('keyword', '').lower().strip() == layer2_keyword:
                        print(f"  OK Matched via layer2_keyword: '{layer2_keyword}'")
                        return t

            # Priority 2: Exact match on original_keyword
            if original_keyword:
                for t in trending_topics:
                    if t.get('keyword', '').lower().strip() == original_keyword:
                        print(f"  OK Matched via original_keyword: '{original_keyword}'")
                        return t

            # Priority 3: Fuzzy match - Layer 2 keyword contains GPT keyword or vice versa
            search_terms = [layer2_keyword, original_keyword]
            for search_term in search_terms:
                if not search_term:
                    continue
                for t in trending_topics:
                    t_keyword = t.get('keyword', '').lower().strip()
                    # Check if one contains the other
                    if search_term in t_keyword or t_keyword in search_term:
                        print(f"  WARNING:  Fuzzy matched '{search_term}' -> '{t_keyword}'")
                        return t

            # No match found
            print(f"  ERROR: No match found for layer2_keyword='{layer2_keyword}', original_keyword='{original_keyword}'")
            return {}

        # Process bullish topics
        for i, gpt_topic in enumerate(curated['bullish'], 1):
            print(f"\n  Processing bullish-{i}: {gpt_topic.get('topic_name', 'N/A')}")

            # Find original topic in Layer 2 data
            original_topic = find_layer2_topic(gpt_topic, trending_topics)

            # LAYER 3 DEFENSE: Post-GPT validation
            is_valid, rejection_reason = validate_gpt_topic_selection(gpt_topic, original_topic)
            if not is_valid:
                print(f"  BLOCKED: REJECTED: {rejection_reason}")
                print(f"     Headline: {gpt_topic.get('headline', 'N/A')}")
                continue  # Skip this topic

            enriched = enrich_topic_with_metadata(
                gpt_topic=gpt_topic,
                original_topic=original_topic,
                rank=f"bullish-{i}",
                date=date
            )
            enriched_topics.append(enriched)

        # Process bearish topics
        for i, gpt_topic in enumerate(curated['bearish'], 1):
            print(f"\n  Processing bearish-{i}: {gpt_topic.get('topic_name', 'N/A')}")

            # Find original topic in Layer 2 data
            original_topic = find_layer2_topic(gpt_topic, trending_topics)

            # LAYER 3 DEFENSE: Post-GPT validation
            is_valid, rejection_reason = validate_gpt_topic_selection(gpt_topic, original_topic)
            if not is_valid:
                print(f"  BLOCKED: REJECTED: {rejection_reason}")
                print(f"     Headline: {gpt_topic.get('headline', 'N/A')}")
                continue  # Skip this topic

            enriched = enrich_topic_with_metadata(
                gpt_topic=gpt_topic,
                original_topic=original_topic,
                rank=f"bearish-{i}",
                date=date
            )
            enriched_topics.append(enriched)

        # Step 3.5: Final safety check for duplicates (using word overlap)
        print(f"\nCHECKING: Final safety check for duplicates across all enriched topics...")
        original_count = len(enriched_topics)

        # Apply same merge logic to final enriched topics
        deduplicated_final = []
        merged_indices = set()

        for i, topic1 in enumerate(enriched_topics):
            if i in merged_indices:
                continue

            headline1 = topic1.get('headline', '').strip()
            is_duplicate = False

            # Check against already added topics
            for topic2 in deduplicated_final:
                headline2 = topic2.get('headline', '').strip()
                overlap = calculate_word_overlap(headline1, headline2)

                if overlap >= 0.5:  # 50% overlap
                    print(f"  WARNING:  Skipping duplicate in final check ({overlap:.0%} overlap): {headline1[:60]}...")
                    is_duplicate = True
                    merged_indices.add(i)
                    break

            if not is_duplicate:
                deduplicated_final.append(topic1)

        if len(deduplicated_final) < original_count:
            print(f"   Removed {original_count - len(deduplicated_final)} duplicates in final check")
        else:
            print(f"   No duplicates found in final check")

        enriched_topics = deduplicated_final

        # Step 3.6: Backfill from Layer 2 if needed to reach target count
        TARGET_COUNT = 10

        # Initialize GPT client for backfill analysis
        try:
            api_key = get_secret(OPENAI_SECRET_NAME)
            gpt_client = OpenAI(api_key=api_key)
            print("OK: GPT client initialized for backfill analysis")
        except Exception as e:
            print(f"WARNING:  Could not initialize GPT client for backfill: {e}")
            gpt_client = None

        # Count bullish and bearish topics separately
        bullish_enriched = [t for t in enriched_topics if t.get('topic_rank', '').startswith('bullish')]
        bearish_enriched = [t for t in enriched_topics if t.get('topic_rank', '').startswith('bearish')]

        print(f"\nSTAT: Topic counts after validation:")
        print(f"   Bullish: {len(bullish_enriched)}/{TARGET_COUNT}")
        print(f"   Bearish: {len(bearish_enriched)}/{TARGET_COUNT}")

        # Backfill bullish if needed
        if len(bullish_enriched) < TARGET_COUNT:
            needed = TARGET_COUNT - len(bullish_enriched)
            print(f"\nBULLISH: Backfilling {needed} bullish topics from Layer 2...")
            # Pass ORIGINAL curated list (before validation) so backfill knows which keywords GPT already selected
            backfill_topics = backfill_from_layer2(
                curated_topics=curated['bullish'],  # Original list, not just validated ones
                layer2_topics=trending_topics,
                target_count=TARGET_COUNT,
                sentiment_filter='bullish',
                gpt_client=gpt_client
            )

            # Convert backfilled topics to enriched format
            # Find the highest rank number already used
            existing_ranks = [int(t.get('topic_rank', 'bullish-0').split('-')[1]) for t in bullish_enriched if t.get('topic_rank', '').startswith('bullish-')]
            next_rank = max(existing_ranks) + 1 if existing_ranks else 1

            for wrapped in backfill_topics:
                enriched_backfill = enrich_topic_with_metadata(
                    gpt_topic=wrapped['gpt_topic'],
                    original_topic=wrapped['layer2_topic'],
                    rank=f"bullish-{next_rank}",
                    date=date
                )
                enriched_topics.append(enriched_backfill)
                next_rank += 1

        # Backfill bearish if needed
        if len(bearish_enriched) < TARGET_COUNT:
            needed = TARGET_COUNT - len(bearish_enriched)
            print(f"\nBULLISH: Backfilling {needed} bearish topics from Layer 2...")
            # Pass ORIGINAL curated list (before validation) so backfill knows which keywords GPT already selected
            backfill_topics = backfill_from_layer2(
                curated_topics=curated['bearish'],  # Original list, not just validated ones
                layer2_topics=trending_topics,
                target_count=TARGET_COUNT,
                sentiment_filter='bearish',
                gpt_client=gpt_client
            )

            # Convert backfilled topics to enriched format
            # Find the highest rank number already used
            existing_ranks = [int(t.get('topic_rank', 'bearish-0').split('-')[1]) for t in bearish_enriched if t.get('topic_rank', '').startswith('bearish-')]
            next_rank = max(existing_ranks) + 1 if existing_ranks else 1

            for wrapped in backfill_topics:
                enriched_backfill = enrich_topic_with_metadata(
                    gpt_topic=wrapped['gpt_topic'],
                    original_topic=wrapped['layer2_topic'],
                    rank=f"bearish-{next_rank}",
                    date=date
                )
                enriched_topics.append(enriched_backfill)
                next_rank += 1

        print(f"\nOK: Final counts: {len([t for t in enriched_topics if t.get('topic_rank', '').startswith('bullish')])} bullish, {len([t for t in enriched_topics if t.get('topic_rank', '').startswith('bearish')])} bearish")

        # Step 3.7: Post-backfill duplicate check (backfilled topics might duplicate each other or existing topics)
        print(f"\nCHECKING: Post-backfill duplicate check...")
        pre_check_count = len(enriched_topics)
        final_deduplicated = []
        seen_headlines = {}  # Track headlines we've seen

        for topic in enriched_topics:
            headline = topic.get('headline', '').strip()
            headline_key = ' '.join(re.sub(r'[^\w\s]', '', headline.lower()).split())  # Normalize for comparison

            # Check if this headline is a duplicate (exact match or high overlap)
            is_duplicate = False
            for seen_headline in seen_headlines:
                overlap = calculate_word_overlap(headline, seen_headlines[seen_headline]['headline'])
                if overlap >= 0.5:
                    print(f"  WARNING:  Removing post-backfill duplicate ({overlap:.0%} overlap):")
                    print(f"     Keeping: {seen_headlines[seen_headline]['headline'][:60]}...")
                    print(f"     Removing: {headline[:60]}...")
                    is_duplicate = True
                    break

            if not is_duplicate:
                seen_headlines[headline_key] = {'headline': headline, 'topic': topic}
                final_deduplicated.append(topic)

        if len(final_deduplicated) < pre_check_count:
            print(f"   Removed {pre_check_count - len(final_deduplicated)} post-backfill duplicates")
        else:
            print(f"   No post-backfill duplicates found")

        enriched_topics = final_deduplicated

        # Step 4: Write to DynamoDB
        write_to_dynamodb(enriched_topics)

        # Step 5: Chain-invoke the portal publisher
        # The publisher reads today's topics from DynamoDB and writes to
        # s3://opal-data-portal-v2/json/trending/latest.json for the portal.
        # Invoked synchronously (RequestResponse) so we can confirm success
        # before returning — the publisher runs in <2 seconds.
        try:
            lambda_client = boto3.client('lambda', region_name='us-east-1')
            pub_response = lambda_client.invoke(
                FunctionName='opal-trending-topics-portal-publisher',
                InvocationType='Event',  # async — publisher is fast but don't block Layer 3 return
                Payload=b'{}'
            )
            pub_status = pub_response.get('StatusCode', 0)
            print(f"OK: opal-trending-topics-portal-publisher invoked (status {pub_status})")
        except Exception as e:
            # Non-fatal — EventBridge schedule is the fallback safety net
            print(f"WARN: Could not invoke portal publisher: {e}")

        # Success response
        return {
            'statusCode': 200,
            'body': json.dumps({
                'message': 'Layer 3 curation complete',
                'date': date,
                'topics_written': len(enriched_topics),
                'bullish_count': len(curated['bullish']),
                'bearish_count': len(curated['bearish'])
            })
        }

    except Exception as e:
        print(f"\nERROR: ERROR: {e}\n")
        return {
            'statusCode': 500,
            'body': json.dumps({
                'error': str(e)
            })
        }


# =============================================================================
# LOCAL TESTING
# =============================================================================

if __name__ == "__main__":
    # Test locally
    result = lambda_handler({}, {})
    print(json.dumps(result, indent=2))
