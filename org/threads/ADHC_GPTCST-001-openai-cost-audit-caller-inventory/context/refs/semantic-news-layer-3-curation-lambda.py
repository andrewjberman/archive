"""
Semantic News Layer 3 - GPT Narrative Curation with Embeddings
===============================================================

Takes semantic clusters with embeddings and creates cohesive market narratives.

Key features:
- Uses embeddings to detect semantic relationships between clusters
- Combines related clusters into unified narratives
- Ensures semantic diversity (no redundant topics)
- Creates 5-10 bullish + 5-10 bearish narratives (vs 3+3 in keyword system)
- GPT-4o with full context for high-quality analysis

Author: Systems Architect
Date: 2026-02-12
"""

import json
import os
import boto3
from collections import Counter
from datetime import datetime, timezone
from typing import List, Dict, Tuple
from decimal import Decimal
import logging

# Minimal numpy usage (already in Lambda layer)
try:
    import numpy as np
    NUMPY_AVAILABLE = True
except:
    NUMPY_AVAILABLE = False

# Configure logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)

# AWS clients
s3_client = boto3.client('s3', region_name='us-east-1')
dynamodb = boto3.resource('dynamodb', region_name='us-east-1')

# OpenAI (for GPT-4o) - Updated for openai>=1.0.0
try:
    from openai import OpenAI
    secrets_client = boto3.client('secretsmanager', region_name='us-east-1')
    secret = secrets_client.get_secret_value(SecretId='opal/external-apis')
    api_keys = json.loads(secret['SecretString'])
    openai_client = OpenAI(api_key=api_keys.get('openai_api_key'))
    GPT_ENABLED = True
except Exception as e:
    logger.warning(f"OpenAI not available: {e}")
    GPT_ENABLED = False
    openai_client = None

# Configuration
INPUT_BUCKET = os.environ.get('INPUT_BUCKET', 'opal-data-news-v2')
INPUT_KEY = os.environ.get('INPUT_KEY', 'semantic_clusters/latest.json')
OUTPUT_TABLE = os.environ.get('OUTPUT_TABLE', 'semantic-news-trending-daily')
TOP_N_CLUSTERS = int(os.environ.get('TOP_N_CLUSTERS', '50'))
MIN_NARRATIVES_PER_CATEGORY = int(os.environ.get('MIN_NARRATIVES', '5'))
MAX_NARRATIVES_PER_CATEGORY = int(os.environ.get('MAX_NARRATIVES', '10'))

# Financial keywords for filtering
FINANCIAL_KEYWORDS = [
    'fed', 'federal reserve', 'powell', 'rate', 'inflation', 'cpi', 'ppi',
    'monetary policy', 'interest', 'ecb', 'boe', 'central bank',
    'stock', 'market', 'nasdaq', 'dow', 's&p', 'index', 'rally', 'selloff',
    'bull', 'bear', 'trading', 'investor', 'portfolio', 'equity',
    'gdp', 'economy', 'recession', 'growth', 'unemployment', 'jobs',
    'consumer', 'spending', 'retail', 'housing', 'manufacturing',
    'earnings', 'revenue', 'profit', 'guidance', 'quarter', 'eps',
    'merger', 'acquisition', 'ipo', 'buyout', 'takeover',
    'bitcoin', 'crypto', 'ethereum', 'blockchain', 'defi',
    'oil', 'gold', 'commodity', 'dollar', 'euro', 'currency', 'forex',
    'bank', 'credit', 'loan', 'mortgage', 'debt', 'bond', 'treasury',
    'sec', 'finra', 'regulation', 'policy', 'tariff', 'trade'
]

# Sports terms that are unambiguous in a financial context — safe to check at
# the cluster-keyword level with word-boundary matching.
#
# NOTE: Intentionally excludes ambiguous team names that collide with financial
# vocabulary ('giants' = tech giants, 'bears' = bear market, 'nets' = revenue nets,
# 'heat' = regulatory heat, 'bulls' = bull market, 'rams' = memory).  Those
# collisions are handled by the article-title secondary check below.
import re as _re
_SPORTS_EXCLUSION_TERMS = [
    # Leagues — completely unambiguous
    'nfl', 'nba', 'mlb', 'nhl', 'ncaa',
    # Sports types
    'football', 'basketball', 'baseball', 'hockey',
    # Sports-specific phrases (no financial equivalent)
    'free agency', 'free agent', 'nfl draft', 'nfl trade', 'nfl free agency',
    'quarterback', 'wide receiver', 'running back', 'tight end', 'touchdown',
    'home run', 'franchise tag', 'draft pick', 'roster move', 'trade deadline',
    'head coach', 'offensive coordinator', 'defensive coordinator',
    'regular season', 'postseason', 'halftime', 'march madness',
    'slam dunk', 'super bowl', 'world series', 'transfer portal',
    'bowl game', 'playoff game', 'salary cap',
    # Unambiguous NFL teams
    'texans', 'cowboys', 'patriots', 'chiefs', 'steelers', 'ravens',
    'eagles', 'packers', 'bengals', 'bills', 'colts', 'titans',
    'buccaneers', 'seahawks', 'chargers', 'raiders', 'jaguars',
    'commanders', 'dolphins', 'broncos',
    # Unambiguous NBA teams (exclude 'heat', 'nets', 'bulls', 'bears', 'warriors')
    'lakers', 'celtics', 'knicks', 'bucks', 'suns', 'nuggets', 'clippers',
    'thunder', 'spurs', 'pelicans', 'grizzlies', 'timberwolves',
    # MLB
    'yankees', 'dodgers', 'mets', 'red sox', 'cubs', 'braves',
    # College
    'michigan state', 'ohio state', 'penn state', 'alabama', 'clemson',
    'college football', 'college basketball',
    # Combat sports
    'ufc', 'mma', 'boxing match',
    # Athletes who generate persistent sports noise
    'tyreek hill', 'patrick mahomes', 'travis kelce', 'lamar jackson',
    'josh allen', 'dak prescott', 'logan paul',
]
_SPORTS_PATTERN = _re.compile(
    r'\b(' + '|'.join(_re.escape(t) for t in _SPORTS_EXCLUSION_TERMS) + r')\b',
    _re.IGNORECASE
)


def lambda_handler(event, context):
    """
    Main handler for semantic narrative curation

    Loads semantic clusters, calculates similarities, sends to GPT for narrative creation
    """
    try:
        start_time = datetime.now(timezone.utc)
        logger.info("=== Semantic News Layer 3 Curation Started ===")

        # Phase 1: Load semantic clusters from S3
        logger.info("Phase 1: Loading semantic clusters from S3")
        clusters = load_semantic_clusters()
        logger.info(f"Loaded {len(clusters)} clusters")

        # Phase 2: Filter financial clusters
        logger.info("Phase 2: Filtering financial clusters")
        financial_clusters = filter_financial_clusters(clusters)
        logger.info(f"Financial clusters: {len(financial_clusters)}")

        # Phase 3: Select top N with bullish/bearish balance
        logger.info(f"Phase 3: Selecting top {TOP_N_CLUSTERS} clusters (balanced)")
        selected_clusters = select_balanced_clusters(financial_clusters, TOP_N_CLUSTERS)
        logger.info(f"Selected: {len(selected_clusters)} clusters")

        # Phase 4: Calculate semantic similarity matrix
        logger.info("Phase 4: Calculating cluster semantic similarities")
        similarities = calculate_similarity_matrix(selected_clusters)
        logger.info(f"Calculated {len(similarities)} similarity relationships")

        # Phase 5: Send to GPT for narrative synthesis
        if not GPT_ENABLED:
            logger.error("GPT not available - cannot proceed")
            return {'statusCode': 500, 'body': json.dumps({'error': 'GPT not configured'})}

        logger.info("Phase 5: GPT narrative synthesis")
        narratives = synthesize_narratives_with_gpt(selected_clusters, similarities)
        logger.info(f"Created {len(narratives.get('bullish_narratives', []))} bullish + {len(narratives.get('bearish_narratives', []))} bearish narratives")

        # Phase 5.5: Enrich narratives with real source/article data from clusters
        # GPT only returns 1 top_source and no article urls/dates — override from cluster data
        logger.info("Phase 5.5: Enriching narratives with cluster source/article data")
        narratives = enrich_narratives_from_clusters(narratives, selected_clusters)

        # Phase 6: Save to DynamoDB
        logger.info("Phase 6: Saving narratives to DynamoDB")
        saved_count = save_narratives_to_dynamodb(narratives)
        logger.info(f"Saved {saved_count} narratives")

        duration = (datetime.now(timezone.utc) - start_time).total_seconds()

        logger.info(f"=== Curation Complete in {duration:.1f}s ===")

        return {
            'statusCode': 200,
            'body': json.dumps({
                'message': 'Semantic narrative curation complete',
                'bullish_narratives': len(narratives.get('bullish', [])),
                'bearish_narratives': len(narratives.get('bearish', [])),
                'total_narratives': len(narratives.get('bullish', [])) + len(narratives.get('bearish', [])),
                'duration_seconds': duration
            })
        }

    except Exception as e:
        logger.error(f"ERROR: {e}", exc_info=True)
        return {
            'statusCode': 500,
            'body': json.dumps({'error': str(e), 'message': 'Curation failed'})
        }


def load_semantic_clusters() -> List[Dict]:
    """Load semantic clusters from S3 (Phase 1 output)"""
    response = s3_client.get_object(Bucket=INPUT_BUCKET, Key=INPUT_KEY)
    data = json.loads(response['Body'].read())

    clusters = data.get('clusters', [])

    # Convert centroid and embeddings back to numpy arrays
    for cluster in clusters:
        if 'centroid_embedding' in cluster and cluster['centroid_embedding']:
            cluster['centroid_embedding'] = np.array(cluster['centroid_embedding'])

        for article in cluster.get('articles', []):
            if 'embedding' in article and article['embedding']:
                article['embedding'] = np.array(article['embedding'])

    return clusters


def _is_sports_cluster(cluster: Dict) -> Tuple[bool, str]:
    """
    Return (True, matched_term) if the cluster is sports-related, else (False, '').

    Two-pass check:
    1. Keyword-level: run the sports exclusion pattern against all cluster keywords.
       Uses word-boundary matching to avoid false positives (e.g. 'market' inside
       a keyword won't accidentally match a financial term).
    2. Title-level: if the keyword check passes, spot-check the top 3 article titles
       for the same pattern.  This catches clusters where sports terms appear in
       article text but didn't surface as cluster keywords.
    """
    # Pass 1: cluster keywords
    keywords_text = ' '.join(cluster.get('keywords', [])[:10]).lower()
    m = _SPORTS_PATTERN.search(keywords_text)
    if m:
        return True, m.group(1)

    # Pass 2: sample article titles (top 3 by combined_score)
    top_articles = sorted(
        cluster.get('articles', []),
        key=lambda a: a.get('combined_score', 0),
        reverse=True
    )[:3]
    titles_text = ' '.join(a.get('title', '') for a in top_articles).lower()
    m = _SPORTS_PATTERN.search(titles_text)
    if m:
        return True, m.group(1)

    return False, ''


def filter_financial_clusters(clusters: List[Dict]) -> List[Dict]:
    """
    Filter clusters to only financial/market topics.

    Removes: sports (explicit exclusion first), entertainment, lifestyle, general news
    Keeps: markets, economy, policy, corporate, crypto

    The exclusion-before-inclusion order prevents sports clusters that happen to
    contain financial vocabulary ('market', 'trade', 'contract', 'cap') from
    passing the financial-keyword threshold.
    """
    financial = []

    for cluster in clusters:
        # --- Exclusion gate: sports (runs before financial inclusion check) ---
        is_sports, matched = _is_sports_cluster(cluster)
        if is_sports:
            logger.info(
                f"BLOCKED: sports cluster excluded: "
                f"'{matched}' in {cluster.get('keywords', [])[:5]}"
            )
            continue

        keywords_lower = [kw.lower() for kw in cluster.get('keywords', [])[:10]]

        # --- Inclusion gate: financial relevance ---
        matches = sum(1 for kw in keywords_lower
                     if any(fin_kw in kw for fin_kw in FINANCIAL_KEYWORDS))

        if matches >= 2:
            financial.append(cluster)
        else:
            logger.debug(f"Filtered non-financial cluster: {cluster.get('keywords', [])[:3]}")

    return financial


def select_balanced_clusters(clusters: List[Dict], target_count: int = 50) -> List[Dict]:
    """
    Select top N clusters ensuring bullish/bearish balance

    Goal: Get enough of each sentiment so GPT can create 5-10 topics per category
    """
    # Separate by sentiment
    bullish = [c for c in clusters if c.get('avg_sentiment', 0) > 0.1]
    bearish = [c for c in clusters if c.get('avg_sentiment', 0) < -0.1]
    neutral = [c for c in clusters if abs(c.get('avg_sentiment', 0)) <= 0.1]

    logger.info(f"  Sentiment distribution: {len(bullish)} bullish, {len(bearish)} bearish, {len(neutral)} neutral")

    # Sort by importance (heavily favor larger clusters)
    def importance_score(c):
        return (c.get('size', 0) ** 2) * abs(c.get('avg_sentiment', 0))

    bullish_sorted = sorted(bullish, key=importance_score, reverse=True)
    bearish_sorted = sorted(bearish, key=importance_score, reverse=True)
    neutral_sorted = sorted(neutral, key=lambda c: c.get('size', 0), reverse=True)

    # Select balanced set
    # Aim for 25 bullish, 25 bearish to ensure GPT has enough options
    selected = []

    # Take top 25 of each (or all if less than 25)
    bullish_count = min(25, len(bullish_sorted))
    bearish_count = min(25, len(bearish_sorted))

    selected.extend(bullish_sorted[:bullish_count])
    selected.extend(bearish_sorted[:bearish_count])

    # Fill remainder with neutrals or more from dominant sentiment
    remaining = target_count - len(selected)
    if remaining > 0:
        # Add neutrals first
        neutral_to_add = min(remaining, len(neutral_sorted))
        selected.extend(neutral_sorted[:neutral_to_add])
        remaining -= neutral_to_add

        # If still need more, take from whichever sentiment has more
        if remaining > 0:
            if len(bullish_sorted) > bullish_count:
                selected.extend(bullish_sorted[bullish_count:bullish_count + remaining])
            elif len(bearish_sorted) > bearish_count:
                selected.extend(bearish_sorted[bearish_count:bearish_count + remaining])

    logger.info(f"  Selected: {len([c for c in selected if c.get('avg_sentiment', 0) > 0.1])} bullish, "
                f"{len([c for c in selected if c.get('avg_sentiment', 0) < -0.1])} bearish clusters")

    return selected[:target_count]


def cosine_similarity_manual(vec_a: List[float], vec_b: List[float]) -> float:
    """
    Calculate cosine similarity between two vectors

    Formula: (A · B) / (||A|| × ||B||)
    For normalized vectors: just A · B (dot product)
    """
    dot_product = sum(a * b for a, b in zip(vec_a, vec_b))
    return dot_product  # Embeddings are already normalized


def calculate_similarity_matrix(clusters: List[Dict]) -> List[Dict]:
    """
    Calculate semantic similarity between all cluster pairs

    Returns list of similarity relationships for GPT context
    """
    # Extract centroids
    centroids = []
    cluster_ids = []

    for cluster in clusters:
        if 'centroid_embedding' in cluster and cluster['centroid_embedding'] is not None:
            centroid = cluster['centroid_embedding']
            # Convert to list if numpy array
            if NUMPY_AVAILABLE and isinstance(centroid, np.ndarray):
                centroid = centroid.tolist()
            centroids.append(centroid)
            cluster_ids.append(cluster['cluster_id'])

    if not centroids:
        logger.warning("No centroids found - returning empty similarities")
        return []

    # Calculate pairwise similarities
    similarities = []

    for i in range(len(cluster_ids)):
        for j in range(i+1, len(cluster_ids)):
            sim_score = cosine_similarity_manual(centroids[i], centroids[j])

            if sim_score > 0.30:  # Only notable relationships
                similarities.append({
                    'cluster_a': int(cluster_ids[i]),
                    'cluster_b': int(cluster_ids[j]),
                    'similarity': round(sim_score, 3),
                    'keywords_a': clusters[i].get('keywords', [])[:3],
                    'keywords_b': clusters[j].get('keywords', [])[:3],
                    'relationship': interpret_similarity(sim_score),
                    'sentiment_a': clusters[i].get('avg_sentiment', 0),
                    'sentiment_b': clusters[j].get('avg_sentiment', 0)
                })

    # Sort by similarity (highest first)
    similarities.sort(key=lambda x: x['similarity'], reverse=True)

    return similarities[:100]  # Top 100 for GPT (most important relationships)


def interpret_similarity(score: float) -> str:
    """Human-readable similarity interpretation for GPT"""
    if score > 0.80:
        return "Nearly identical - same core story"
    elif score > 0.70:
        return "Highly related - strong overlap"
    elif score > 0.60:
        return "Related - significant connection"
    elif score > 0.50:
        return "Moderately related - connected themes"
    elif score > 0.40:
        return "Loosely related - tangential"
    else:
        return "Distinct - different topics"


def synthesize_narratives_with_gpt(clusters: List[Dict], similarities: List[Dict]) -> Dict:
    """
    Use GPT-4o to synthesize semantic clusters into market narratives

    GPT can combine related clusters into cohesive narratives
    and ensure diversity across selected topics
    """

    # Prepare compact cluster data for GPT
    cluster_summaries = []
    for cluster in clusters:
        # Get top 5 articles by combined_score
        top_articles = sorted(
            cluster.get('articles', []),
            key=lambda a: a.get('combined_score', 0),
            reverse=True
        )[:5]

        cluster_summaries.append({
            'id': cluster['cluster_id'],
            'keywords': cluster.get('keywords', [])[:8],
            'size': cluster.get('size', 0),
            'sentiment': round(cluster.get('avg_sentiment', 0), 3),
            'sentiment_label': cluster.get('sentiment_label', 'Neutral'),
            'top_sources': cluster.get('top_sources', [])[:3],
            'sample_articles': [
                {
                    'title': a.get('title', ''),
                    'source': a.get('source', ''),
                    'relevance': round(a.get('relevance_score', 0), 2),
                    'recency': round(a.get('time_decay_score', 0), 2),
                    'combined': round(a.get('combined_score', 0), 2)
                }
                for a in top_articles
            ]
        })

    # Build GPT prompt
    prompt = f"""You are synthesizing financial news clusters into cohesive market narratives using semantic analysis.

INPUT DATA:
- {len(cluster_summaries)} semantic clusters (top financial topics)
- Semantic similarity matrix showing relationships between clusters
- Each cluster has embeddings showing its semantic position

TASK: Create {MIN_NARRATIVES_PER_CATEGORY}-{MAX_NARRATIVES_PER_CATEGORY} BULLISH and {MIN_NARRATIVES_PER_CATEGORY}-{MAX_NARRATIVES_PER_CATEGORY} BEARISH market narratives

NARRATIVE SYNTHESIS (CRITICAL):
1. A narrative can combine MULTIPLE semantically related clusters
   - If clusters have similarity > 0.60, they likely describe the same story from different angles
   - Example: "Fed cuts" (cluster 42) + "Market rally" (cluster 61, similarity 0.73)
     → Synthesize into ONE narrative: "Fed Pivot Drives Market Rally"
   - This creates richer, more comprehensive topics

2. Narratives must be semantically DIVERSE
   - Final narratives should have similarity < 0.40 to each other
   - Aim for maximum coverage of distinct market themes
   - 5-10 well-differentiated narratives >> 25 redundant picks

3. Use semantic relationships in your analysis
   - "The Fed's dovish pivot (cluster 42) has triggered a market rally (cluster 61, similarity 0.73 - direct market reaction)..."
   - Explain WHY clusters are related based on similarity scores

CLUSTERS (top {len(cluster_summaries)}, balanced bullish/bearish):
{json.dumps(cluster_summaries[:20], indent=2)}
... {len(cluster_summaries) - 20} more clusters

SEMANTIC SIMILARITIES (top 100 relationships):
{json.dumps(similarities[:20], indent=2)}
... {len(similarities) - 20} more relationships

OUTPUT REQUIREMENTS:
For EACH narrative (5-10 bullish, 5-10 bearish):

HEADLINE REQUIREMENTS (CRITICAL):
- Varied, organic language: NO templated phrases like "raises concerns", "boosts confidence", "threatens", "persists"
- Each headline should feel different from the others (diverse structure/voice)
- Examples of GOOD headlines: "Fed's Pause Unleashes Tech Rally", "Oil Hits Year High on Supply Crunch", "Crypto Regulation Pivots Unexpectedly"
- Examples of BAD headlines: "Company X Raises Investor Concerns", "Sector Y Boosts Market Confidence", "Risk Z Threatens Stability"
- Use active verbs (pivots, unleashes, crashes, surges) not passive constructions
- Specific company/sector names where possible
- 10-14 words, punchy and newsworthy

{{
  "narrative_id": "bullish-1" or "bearish-1",
  "headline": "Specific, organic headline with varied structure (NOT templated)",
  "analysis": "200-250 word synthesis explaining:
    - What's happening (combine insights from related clusters)
    - Why it matters for markets
    - How clusters relate (use similarity scores)
    - Specific data points from articles
    - Market implications",
  "source_clusters": [42, 61, 15],  // Which cluster IDs you combined
  "cluster_synthesis_notes": "Combined Fed policy (42) with market reaction (61, sim 0.73) and inflation driver (15, sim 0.52)",
  "total_articles": 45,  // Sum across all source clusters
  "sentiment_score": 0.68,  // Weighted average from source clusters
  "confidence": 0.85,  // How confident in this narrative (0-1)
  "top_sources": ["WSJ", "Bloomberg", "FT"],
  "selected_articles": [...],  // Top 10 articles across all source clusters by combined_score
  "citations": ["[1] WSJ, Feb 13", "[2] Bloomberg, Feb 12", ...]
}}

SELECTION CRITERIA:
1. Importance (larger clusters with stronger sentiment first)
2. Semantic synthesis (combine related clusters, similarity > 0.60)
3. Diversity (final narratives have similarity < 0.40 between them)
4. Balance (similar count of bullish and bearish)
5. Recency (prefer clusters with high time_decay scores)

EXCLUSION CRITERIA (absolute, no exceptions):
- Do NOT select any sports cluster (NFL, NBA, MLB, NHL, NCAA, college sports).
  If a cluster's keywords or articles relate to player trades, free agency,
  salary cap, draft picks, team rosters, or any sports league — skip it entirely.
  This is a financial market intelligence portal, not a sports site.

Respond ONLY with valid JSON (no markdown, no explanations):
{{
  "bullish_narratives": [...5-10 narratives],
  "bearish_narratives": [...5-10 narratives],
  "synthesis_metadata": {{
    "clusters_analyzed": {len(cluster_summaries)},
    "narratives_created": "total count",
    "synthesis_strategy": "brief note on how you combined clusters"
  }}
}}
"""

    # Call GPT-4o (using openai>=1.0.0 API)
    response = openai_client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "You are a financial news analyst synthesizing semantic clusters into market narratives. Create compelling, varied headlines with organic language - avoid templated phrases. Respond only with valid JSON."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.45,
        max_tokens=10000,
        response_format={"type": "json_object"}
    )

    # Log token usage for cost tracking
    input_tokens = response.usage.prompt_tokens
    output_tokens = response.usage.completion_tokens
    total_tokens = response.usage.total_tokens

    # GPT-4o pricing: $2.50 per 1M input tokens, $10.00 per 1M output tokens
    input_cost = (input_tokens / 1_000_000) * 2.50
    output_cost = (output_tokens / 1_000_000) * 10.00
    total_cost = input_cost + output_cost

    logger.info(f"GPT Token Usage: {input_tokens:,} in + {output_tokens:,} out = {total_tokens:,} total")
    logger.info(f"GPT Cost: ${input_cost:.6f} (input) + ${output_cost:.6f} (output) = ${total_cost:.6f} total")

    # Parse response
    narratives_json = response.choices[0].message.content
    logger.info(f"GPT Response (first 500 chars): {narratives_json[:500]}")
    narratives = json.loads(narratives_json)
    logger.info(f"Parsed narratives keys: {narratives.keys()}")

    return narratives


def enrich_narratives_from_clusters(narratives: Dict, clusters: List[Dict]) -> Dict:
    """
    Post-GPT enrichment: override top_sources and populate article metadata
    from actual cluster data rather than GPT's output.

    Fixes two issues:
    1. top_sources: GPT echoes a single cluster's source list (always 1 entry).
       We aggregate sources from all articles across all source_clusters so the
       frontend quality filter (requires >= 2 sources) passes correctly.
    2. selected_articles: GPT omits url and published_at. We title-match back to
       original cluster articles to fill those fields in.
    """
    # Build cluster lookup: cluster_id → cluster
    cluster_lookup = {c['cluster_id']: c for c in clusters}

    def enrich_narrative(narrative: Dict) -> None:
        source_cluster_ids = narrative.get('source_clusters', [])

        # Collect all articles from source_clusters once (used for both fixes below)
        all_cluster_articles = []
        all_sources = []
        for cid in source_cluster_ids:
            cluster = cluster_lookup.get(cid)
            if cluster:
                for article in cluster.get('articles', []):
                    all_cluster_articles.append(article)
                    src = article.get('source', '')
                    if src and src.lower() != 'unknown':
                        all_sources.append(src)

        # 1. Aggregate top_sources from all cluster articles (GPT only echoes 1)
        if all_sources:
            narrative['top_sources'] = [s for s, _ in Counter(all_sources).most_common(5)]
            logger.info(f"  Enriched top_sources for '{narrative.get('headline', '')[:50]}': {narrative['top_sources']}")

        # 2. Replace GPT's selected_articles entirely — GPT fabricates titles that
        #    don't match real articles, so title-matching is unreliable. Instead,
        #    take the top N articles from source clusters ranked by combined_score.
        if all_cluster_articles:
            sorted_articles = sorted(
                all_cluster_articles,
                key=lambda a: a.get('combined_score', 0),
                reverse=True
            )
            narrative['selected_articles'] = [
                {
                    'title': a.get('title', ''),
                    'source': a.get('source', ''),
                    'published_at': a.get('published_at', '') or a.get('published_date', '') or a.get('article_date', ''),
                    'url': a.get('url', ''),
                    'sentiment': a.get('sentiment_finbert', 0.0),
                    'combined_score': a.get('combined_score', 0.0),
                }
                for a in sorted_articles[:10]
            ]

    for narrative in narratives.get('bullish_narratives', []):
        enrich_narrative(narrative)
    for narrative in narratives.get('bearish_narratives', []):
        enrich_narrative(narrative)

    return narratives


def float_to_decimal(obj):
    """Convert floats to Decimal for DynamoDB compatibility"""
    if isinstance(obj, float):
        return Decimal(str(obj))
    elif isinstance(obj, dict):
        return {k: float_to_decimal(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [float_to_decimal(item) for item in obj]
    return obj


def save_narratives_to_dynamodb(narratives: Dict) -> int:
    """
    Save narratives to DynamoDB table

    Schema matches existing trending-daily table for compatibility
    """
    table = dynamodb.Table(OUTPUT_TABLE)
    date_str = datetime.now(timezone.utc).strftime('%Y-%m-%d')

    saved_count = 0

    # Save bullish narratives
    for i, narrative in enumerate(narratives.get('bullish_narratives', []), 1):
        item = {
            'date': date_str,
            'topic_rank': f'bullish-{i}',
            'headline': narrative.get('headline', ''),
            'analysis': narrative.get('analysis', ''),
            'source_clusters': narrative.get('source_clusters', []),
            'cluster_synthesis': narrative.get('cluster_synthesis_notes', ''),
            'article_count': narrative.get('total_articles', 0),
            'sentiment_score': Decimal(str(narrative.get('sentiment_score', 0))),
            'confidence': Decimal(str(narrative.get('confidence', 0.5))),
            'top_sources': narrative.get('top_sources', []),
            'selected_articles': narrative.get('selected_articles', [])[:100],  # Limit to 100
            'citations': narrative.get('citations', []),
            'generated_at': datetime.now(timezone.utc).isoformat(),
            'curation_method': 'semantic_synthesis'
        }

        # Convert any remaining floats in nested structures
        item = float_to_decimal(item)

        table.put_item(Item=item)
        saved_count += 1

    # Save bearish narratives
    for i, narrative in enumerate(narratives.get('bearish_narratives', []), 1):
        item = {
            'date': date_str,
            'topic_rank': f'bearish-{i}',
            'headline': narrative.get('headline', ''),
            'analysis': narrative.get('analysis', ''),
            'source_clusters': narrative.get('source_clusters', []),
            'cluster_synthesis': narrative.get('cluster_synthesis_notes', ''),
            'article_count': narrative.get('total_articles', 0),
            'sentiment_score': Decimal(str(narrative.get('sentiment_score', 0))),
            'confidence': Decimal(str(narrative.get('confidence', 0.5))),
            'top_sources': narrative.get('top_sources', []),
            'selected_articles': narrative.get('selected_articles', [])[:100],
            'citations': narrative.get('citations', []),
            'generated_at': datetime.now(timezone.utc).isoformat(),
            'curation_method': 'semantic_synthesis'
        }

        # Convert any remaining floats in nested structures
        item = float_to_decimal(item)

        table.put_item(Item=item)
        saved_count += 1

    return saved_count
