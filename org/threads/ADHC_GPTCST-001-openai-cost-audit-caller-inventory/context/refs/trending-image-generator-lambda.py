"""
Trending Topic Icon Selector Lambda
Uses GPT-4o-mini to intelligently select Phosphor icon names for trending topics

Triggered after Layer 3 GPT curation completes
Selects icons for bullish-1 and bearish-1 topics
"""

import json
import boto3
import os
from datetime import datetime
from openai import OpenAI

# AWS Clients
dynamodb = boto3.resource('dynamodb', region_name='us-east-2')
secrets_client = boto3.client('secretsmanager', region_name='us-east-2')

# Configuration
TRENDING_TABLE = 'opal-news-trending-daily'
OPENAI_SECRET = os.environ.get('OPENAI_SECRET', 'opal/external-apis')
GPT_MODEL = 'gpt-4o-mini'  # Fast and cheap for icon selection

# Available Phosphor icon names (matches frontend ICON_MAP)
AVAILABLE_ICONS = {
    # Tech & Innovation
    'rocket': 'Space, aerospace, innovation, SpaceX, breakthrough tech',
    'laptop': 'Technology, software, digital platforms, tech companies',
    'chip': 'Semiconductors, processors, hardware, chip manufacturing (NVIDIA, AMD, Intel)',
    'robot': 'AI, artificial intelligence, automation, machine learning',
    'database': 'Data, cloud computing, data centers, storage',

    # Finance & Economy
    'bank': 'Federal Reserve, central banks, monetary policy, banking sector',
    'coins': 'Money, assets, wealth, investment, capital, returns',
    'percent': 'Interest rates, yields, bonds, percentages',
    'chart_up': 'Growth, gains, positive momentum, rally, strong performance',
    'chart_down': 'Decline, losses, correction, sell-off, negative performance',
    'currency': 'Currency, dollar, forex, exchange rates',
    'buildings': 'Real estate, commercial property, REITs',
    'briefcase': 'Business, corporate, employment, professional services',

    # Commodities & Energy
    'oil': 'Oil prices, crude, petroleum, energy sector',
    'barrel': 'Oil barrels, OPEC, production, reserves',
    'lightning': 'Energy, power, utilities, electricity, renewables',
    'wheat': 'Agriculture, grains, farming, food prices, commodities',
    'gold': 'Precious metals, gold, safe havens, gold bars',
    'flame': 'Natural gas, heating, energy prices',

    # Global & Geopolitics
    'factory': 'Manufacturing, production, industrial activity, PMI',
    'globe': 'International markets, global trade, geopolitics',
    'warning': 'Risks, concerns, warnings, fears, uncertainty',
    'shield': 'Defense, security, protection, safety',

    # Market Dynamics
    'trend_up': 'Upward trend, bullish momentum, positive direction (generic)',
    'trend_down': 'Downward trend, bearish pressure, negative direction (generic)',
    'scales': 'Balance, weighting, measurement, risk/reward',
    'target': 'Goals, objectives, performance targets, projections',

    # Crypto
    'bitcoin': 'Bitcoin, BTC, cryptocurrency',
    'ethereum': 'Ethereum, ETH, crypto platforms',
    'crypto': 'Cryptocurrency general, digital assets, blockchain',

    # Additional
    'handshake': 'Deals, mergers, acquisitions, partnerships, agreements',
    'chart': 'Market charts, analysis, technical indicators',
    'graph': 'Data visualization, trends, analytics',
    'money': 'Cash, liquidity, monetary flows',
}

SYSTEM_PROMPT = f"""You are an expert at analyzing financial news headlines and selecting appropriate icon names from the Phosphor Icons library.

Given a trending topic headline, select the SINGLE MOST APPROPRIATE icon from this list:

{json.dumps(AVAILABLE_ICONS, indent=2)}

SELECTION RULES:

1. **Focus on the PRIMARY concrete subject** - Not meta-concepts
   - "SpaceX valuation boom" → rocket (space/aerospace is the subject)
   - "Fed signals rate pause" → bank (Federal Reserve/central banking)
   - "Oil prices surge" → oil (commodity is the subject)

2. **Industry over Person**
   - "Musk's ventures ignite growth" → rocket (space industry, not the person)
   - "Powell comments on rates" → bank (Fed policy, not the person)

3. **Specific over Generic**
   - Prefer specific commodity/sector icons (oil, chip, factory) over generic (chart, trend_up)
   - Only use trend_up/trend_down as fallback when no specific match exists

4. **Match the Content not the Tone**
   - Don't choose chart_up just because sentiment is bullish
   - Choose based on WHAT the topic is about, not whether it's positive/negative

EXAMPLES:

Headline: "SpaceX Valuation Boom Reinforces Investor Appetite for Musk Ecosystem Capital"
Analysis: Primary subject is space/aerospace industry
Best icon: "rocket"

Headline: "AI Valuations Come Under Pressure as Policy Backdrop Darkens"
Analysis: Primary subject is AI sector
Best icon: "robot"

Headline: "Oil Prices Surge on OPEC Production Cuts"
Analysis: Primary subject is oil/energy commodity
Best icon: "oil"

Headline: "Federal Reserve Signals Extended Rate Pause Amid Inflation Concerns"
Analysis: Primary subject is Federal Reserve/monetary policy
Best icon: "bank"

Headline: "Semiconductor Exports Decline Sharply"
Analysis: Primary subject is chip/semiconductor industry
Best icon: "chip"

Headline: "Bitcoin Structural and Policy Risks Emerge"
Analysis: Primary subject is Bitcoin/cryptocurrency
Best icon: "bitcoin"

Headline: "Manufacturing PMI Disappoints in Key Markets"
Analysis: Primary subject is manufacturing/industrial activity
Best icon: "factory"

Headline: "Generic Market Rally Continues With No Clear Catalyst"
Analysis: No specific subject, just general market movement
Best icon: "trend_up"

RESPONSE FORMAT:
Return ONLY the icon name (e.g., "rocket", "bank", "oil") with NO explanation or additional text."""


def get_openai_key() -> str:
    """Fetch OpenAI API key from Secrets Manager"""
    try:
        response = secrets_client.get_secret_value(SecretId=OPENAI_SECRET)
        secrets = json.loads(response['SecretString'])
        return secrets.get('openai_api_key', '')
    except Exception as e:
        print(f"❌ Error fetching OpenAI key: {str(e)}")
        return ''


def select_icon_with_gpt(client: OpenAI, headline: str, sentiment: str) -> str:
    """
    Use GPT-4o-mini to select the best Phosphor icon for a headline

    Args:
        client: OpenAI client instance
        headline: The trending topic headline
        sentiment: 'bullish' or 'bearish' (for context, but icon should match content not sentiment)

    Returns:
        Icon name (e.g., 'rocket', 'bank', 'oil')
    """
    try:
        response = client.chat.completions.create(
            model=GPT_MODEL,
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": f"Headline: {headline}\nSentiment: {sentiment}\n\nSelect the best icon name:"}
            ],
            temperature=0.1,  # Low temperature for consistent selections
            max_tokens=20
        )

        icon_name = response.choices[0].message.content.strip().lower()

        # Validate icon exists in our list
        if icon_name not in AVAILABLE_ICONS:
            print(f"⚠️  GPT returned invalid icon '{icon_name}', using fallback")
            return 'trend_up' if sentiment == 'bullish' else 'trend_down'

        print(f"✅ Selected '{icon_name}' for: {headline[:60]}...")
        return icon_name

    except Exception as e:
        print(f"❌ Error in GPT icon selection: {str(e)}")
        # Fallback
        return 'trend_up' if sentiment == 'bullish' else 'trend_down'


def get_topic(table, date: str, topic_rank: str):
    """Fetch a topic from DynamoDB"""
    try:
        response = table.get_item(
            Key={
                'date': date,
                'topic_rank': topic_rank
            }
        )
        return response.get('Item')
    except Exception as e:
        print(f"❌ Error fetching {topic_rank}: {str(e)}")
        return None


def update_topic_icon(table, date: str, topic_rank: str, icon_name: str):
    """Update DynamoDB with selected icon name"""
    try:
        table.update_item(
            Key={
                'date': date,
                'topic_rank': topic_rank
            },
            UpdateExpression='SET icon_type = :icon',
            ExpressionAttributeValues={
                ':icon': icon_name
            }
        )
        print(f"✅ Updated {topic_rank} with icon_type='{icon_name}'")
    except Exception as e:
        print(f"❌ Error updating {topic_rank}: {str(e)}")


def lambda_handler(event, context):
    """
    Main handler - selects icons for top bullish and bearish topics

    Event: {"date": "2025-12-17"}
    """
    date = event.get('date', datetime.utcnow().strftime('%Y-%m-%d'))

    print(f"🎨 Icon selection started for {date}")
    print(f"   Using GPT model: {GPT_MODEL}")
    print(f"   Available icons: {len(AVAILABLE_ICONS)}")

    try:
        # Get OpenAI API key
        api_key = get_openai_key()
        if not api_key:
            raise ValueError("OpenAI API key not found")

        client = OpenAI(api_key=api_key)

        # Get DynamoDB table
        table = dynamodb.Table(TRENDING_TABLE)

        # Fetch bullish-1 and bearish-1 topics
        bullish_topic = get_topic(table, date, 'bullish-1')
        bearish_topic = get_topic(table, date, 'bearish-1')

        if not bullish_topic or not bearish_topic:
            raise ValueError(f"Missing topics for {date}")

        # Use 'headline' field (what's displayed in Portal), not 'topic_name'
        bullish_headline = bullish_topic.get('headline', bullish_topic.get('topic_name', 'Unknown Topic'))
        bearish_headline = bearish_topic.get('headline', bearish_topic.get('topic_name', 'Unknown Topic'))

        print(f"\n📊 Topics:")
        print(f"   Bullish: {bullish_headline}")
        print(f"   Bearish: {bearish_headline}")

        # Select icons using GPT
        print(f"\n🤖 Selecting icons with GPT-4o-mini...")
        bullish_icon = select_icon_with_gpt(client, bullish_headline, 'bullish')
        bearish_icon = select_icon_with_gpt(client, bearish_headline, 'bearish')

        # Update DynamoDB
        print(f"\n💾 Updating DynamoDB...")
        update_topic_icon(table, date, 'bullish-1', bullish_icon)
        update_topic_icon(table, date, 'bearish-1', bearish_icon)

        print(f"\n✅ Icon selection complete!")

        return {
            'statusCode': 200,
            'body': json.dumps({
                'message': 'Icon selection completed',
                'date': date,
                'results': {
                    'bullish': {'headline': bullish_headline, 'icon': bullish_icon},
                    'bearish': {'headline': bearish_headline, 'icon': bearish_icon}
                }
            })
        }

    except Exception as e:
        print(f"❌ Error: {str(e)}")
        import traceback
        traceback.print_exc()

        return {
            'statusCode': 500,
            'body': json.dumps({
                'message': 'Icon selection failed',
                'error': str(e),
                'date': date
            })
        }
