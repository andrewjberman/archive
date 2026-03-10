"""
Lambda Function: market-update-generator

Purpose: Generate Market Update content using GPT-4
Author: AWS Engineer
Date: 2026-01-21

API Endpoints:
  POST /api/public/market-update/generate - Generate content for all 3 sections
  POST /api/public/market-update/regenerate - Regenerate a specific section
"""

import json
import boto3
import os
from openai import OpenAI

# Initialize AWS clients
secrets_client = boto3.client('secretsmanager')


def lambda_handler(event, context):
    """Main Lambda handler - generates content using GPT-4"""
    try:
        body = json.loads(event.get('body', '{}'))

        # Extract input data
        selected_topics = body.get('selected_topics', {})
        selected_earnings = body.get('selected_earnings', [])
        selected_macro = body.get('selected_macro', [])
        market_metrics = body.get('market_metrics', {})

        # Check if this is a section-specific regeneration
        section = body.get('section')  # 'last_week', 'this_week', or 'portfolio_impact'

        # Get OpenAI API key
        secrets = get_secret('opal/external-apis')
        openai_api_key = secrets.get('openai_api_key')

        if not openai_api_key:
            return error_response(500, 'OpenAI API key not configured')

        # Initialize OpenAI client
        client = OpenAI(api_key=openai_api_key)

        # Generate specific section or all sections
        if section:
            # Regenerate specific section only
            print(f"Regenerating section: {section}")

            if section == 'last_week':
                content = generate_section_1(client, selected_topics, market_metrics)
                return success_response({section: content})
            elif section == 'this_week':
                content = generate_section_2(client, selected_earnings, selected_macro)
                return success_response({section: content})
            elif section == 'portfolio_impact':
                content = generate_section_3(client, selected_topics, market_metrics)
                return success_response({section: content})
            else:
                return error_response(400, f'Invalid section: {section}')
        else:
            # Generate all sections
            print("Generating all sections")

            print("Generating Section 1: What Happened Last Week?")
            last_week = generate_section_1(client, selected_topics, market_metrics)

            print("Generating Section 2: Key Events This Week")
            this_week = generate_section_2(client, selected_earnings, selected_macro)

            print("Generating Section 3: Impact on Client Portfolios")
            portfolio_impact = generate_section_3(client, selected_topics, market_metrics)

            return success_response({
                'last_week': last_week,
                'this_week': this_week,
                'portfolio_impact': portfolio_impact
            })

    except Exception as e:
        print(f"Error generating content: {str(e)}")
        return error_response(500, f'Error generating content: {str(e)}')


def generate_section_1(client, selected_topics, market_metrics):
    """
    Generate 'What Happened Last Week?' bullets.
    Uses past tense, includes specific data points.
    """
    bullish = selected_topics.get('bullish', [])
    bearish = selected_topics.get('bearish', [])

    # Build context
    bullish_context = "\n".join([
        f"- {t.get('headline', 'Unknown')} ({t.get('article_count', 0)} articles)"
        for t in bullish
    ]) or "No major bullish themes"

    bearish_context = "\n".join([
        f"- {t.get('headline', 'Unknown')} ({t.get('article_count', 0)} articles)"
        for t in bearish
    ]) or "No major bearish themes"

    # Extract market metrics safely
    indices = market_metrics.get('indices', {})
    sp500 = indices.get('sp500', {})
    nasdaq = indices.get('nasdaq', {})
    vix = market_metrics.get('volatility', {}).get('vix', {})

    market_context = f"""
S&P 500: {sp500.get('close', 'N/A')} ({sp500.get('week_change_pct', 0):+.1f}% week)
Nasdaq: {nasdaq.get('close', 'N/A')} ({nasdaq.get('week_change_pct', 0):+.1f}% week)
VIX: {vix.get('close', 'N/A')} ({vix.get('change_pct', 0):+.1f}%)
"""

    prompt = f"""You are a professional financial writer for Opal Capital, writing the weekly "Market Update & Commentary" document for clients.

**Section 1: What Happened Last Week?**

Write 3 concise bullets (2-3 sentences each) summarizing last week's market events. Use past tense.

**Trending Topics:**
Bullish themes:
{bullish_context}

Bearish themes:
{bearish_context}

**Market Performance:**
{market_context}

**Style Guidelines:**
- Professional and analytical tone
- Include specific data points (percentages, basis points, index levels)
- 2-3 sentences per bullet
- Avoid hyperbole or emotional language
- Optionally include historical context ("Interesting Fact: Since 1950...")

**Example Bullets:**
- The market notched its best week in 2024 as investors are gaining confidence that the Fed will deliver a September rate cut. The S&P 500 gained 3.9% last week, led by a rally in technology stocks. Interesting Fact: The S&P 500 has averaged 1% returns in August since 2000.

- The health of the consumer remains strong, retail sales beat expectations in July growing at 1% month-over-month. Unemployment claims came in at 227k, lower than the 235k expected. Consumer confidence also beat expectations rising to 103.3 from 100.3.

- Federal Reserve Chair Jay Powell will be speaking at Jackson Hole on Friday. Markets are pricing in a 70% probability of a 25 basis point rate cut in September, with some possibility of a 50 basis point cut if economic data weakens further.

Return only the 3 bullets as a JSON array: ["bullet 1", "bullet 2", "bullet 3"]
Do not include any other text or explanation."""

    try:
        response = client.chat.completions.create(
            model='gpt-4-turbo-preview',
            messages=[
                {'role': 'system', 'content': 'You are a professional financial writer for Opal Capital.'},
                {'role': 'user', 'content': prompt}
            ],
            temperature=0.3,
            max_tokens=1000
        )

        content = response.choices[0].message.content
        print(f"Section 1 raw response: {content}")

        # Parse JSON response
        bullets = json.loads(content)

        # Validate response
        if not isinstance(bullets, list) or len(bullets) != 3:
            raise ValueError("Expected 3 bullets, got different count")

        return bullets

    except Exception as e:
        print(f"Error in section 1: {str(e)}")
        # Return fallback bullets
        return [
            "U.S. equities rallied last week as market sentiment improved.",
            "Economic data showed mixed signals with some positive developments.",
            "Market volatility remained elevated amid ongoing uncertainties."
        ]


def generate_section_2(client, selected_earnings, selected_macro):
    """
    Generate 'Key Events This Week' bullets.
    Uses future tense, highlights upcoming events.
    """
    earnings_context = "\n".join([
        f"- {e.get('ticker', '')} ({e.get('company', '')}) reports {e.get('date', '')} {e.get('time', '')}"
        for e in selected_earnings
    ]) or "No major earnings this week"

    macro_context = "\n".join([
        f"- {m.get('event', '')} on {m.get('date', '')} at {m.get('time', '')} (impact: {m.get('impact', 'unknown')})"
        for m in selected_macro
    ]) or "No major economic releases this week"

    prompt = f"""You are a professional financial writer for Opal Capital, writing the weekly "Market Update & Commentary" document for clients.

**Section 2: Key Events This Week**

Write 3 concise bullets (2-3 sentences each) highlighting the most important upcoming events. Use future tense ("will be released", "focus will be on").

**Upcoming Economic Releases:**
{macro_context}

**Notable Earnings:**
{earnings_context}

**Style Guidelines:**
- Future tense
- Highlight market-relevant events
- Include specific times and dates when possible
- 2-3 sentences per bullet

**Example Bullets:**
- Important economic datapoints released this week include: Jobless Claims (Thursday) and Consumer Sentiment (Friday). All focus will be on the jobs report on Friday, which is expected to show 180k jobs added in August.

- Federal Reserve Chair Jay Powell will be speaking at Jackson Hole on Friday at 10:00 AM ET. His remarks will provide crucial insight into the Fed's thinking on the timing and magnitude of rate cuts.

- Tech earnings season continues with Oracle reporting Monday after close, followed by Salesforce on Wednesday. These cloud software leaders will provide insight into enterprise IT spending trends.

Return only the 3 bullets as a JSON array: ["bullet 1", "bullet 2", "bullet 3"]
Do not include any other text or explanation."""

    try:
        response = client.chat.completions.create(
            model='gpt-4-turbo-preview',
            messages=[
                {'role': 'system', 'content': 'You are a professional financial writer for Opal Capital.'},
                {'role': 'user', 'content': prompt}
            ],
            temperature=0.3,
            max_tokens=1000
        )

        content = response.choices[0].message.content
        print(f"Section 2 raw response: {content}")

        bullets = json.loads(content)

        if not isinstance(bullets, list) or len(bullets) != 3:
            raise ValueError("Expected 3 bullets")

        return bullets

    except Exception as e:
        print(f"Error in section 2: {str(e)}")
        return [
            "Key economic releases this week will provide insight into the current state of the economy.",
            "Major earnings reports are expected from several large-cap companies.",
            "Federal Reserve commentary will be closely watched for policy signals."
        ]


def generate_section_3(client, selected_topics, market_metrics):
    """
    Generate 'Impact on Client Portfolios' bullets.
    Uses present tense, discusses portfolio positioning.
    """
    bullish = selected_topics.get('bullish', [])
    bearish = selected_topics.get('bearish', [])
    vix = market_metrics.get('volatility', {}).get('vix', {})

    bullish_themes = ', '.join([t.get('headline', '') for t in bullish]) or "None"
    bearish_themes = ', '.join([t.get('headline', '') for t in bearish]) or "None"

    prompt = f"""You are a professional financial writer for Opal Capital, writing the weekly "Market Update & Commentary" document for clients.

**Section 3: Impact on Client Portfolios**

Write 3 concise bullets (2-3 sentences each) discussing portfolio positioning. Use present tense.

**Current Market Context:**
- Recent bullish factors: {bullish_themes}
- Recent bearish factors: {bearish_themes}
- VIX: {vix.get('close', 'N/A')} ({vix.get('change_pct', 0):+.1f}%)

**Standard Themes to Address:**
1. Fixed income positioning (duration, credit quality, rate sensitivity)
2. Equity diversification (sector tilts, factor exposures, concentration risk)
3. Near-term tactical positioning (volatility management, rebalancing opportunities)

**Style Guidelines:**
- Present tense
- Professional investment advisory tone
- Emphasize risk management and diversification
- Avoid specific portfolio recommendations or performance claims

**Example Bullets:**
- Fixed income portfolios continue to be tilted towards capital preservation, with an emphasis on high-quality corporate bonds and short-to-intermediate duration. Given recent Fed commentary, duration risk is managed conservatively.

- Diversification is key as we are seeing more wild price swings in the market driven by economic data releases. Portfolios maintain exposure across sectors and factors to avoid concentration risk in mega-cap technology.

- Near-term volatility is expected as markets digest upcoming CPI data and Fed commentary. Portfolios are positioned defensively with dry powder available for tactical rebalancing opportunities.

Return only the 3 bullets as a JSON array: ["bullet 1", "bullet 2", "bullet 3"]
Do not include any other text or explanation."""

    try:
        response = client.chat.completions.create(
            model='gpt-4-turbo-preview',
            messages=[
                {'role': 'system', 'content': 'You are a professional financial writer and investment advisor for Opal Capital.'},
                {'role': 'user', 'content': prompt}
            ],
            temperature=0.3,
            max_tokens=1000
        )

        content = response.choices[0].message.content
        print(f"Section 3 raw response: {content}")

        bullets = json.loads(content)

        if not isinstance(bullets, list) or len(bullets) != 3:
            raise ValueError("Expected 3 bullets")

        return bullets

    except Exception as e:
        print(f"Error in section 3: {str(e)}")
        return [
            "Fixed income portfolios remain positioned for a higher-for-longer rate environment.",
            "Equity portfolios maintain diversification across sectors and factors.",
            "Near-term volatility is expected, and portfolios are positioned accordingly."
        ]


# ==================== UTILITY FUNCTIONS ====================

def get_secret(secret_name):
    """Fetch secret from AWS Secrets Manager"""
    try:
        response = secrets_client.get_secret_value(SecretId=secret_name)
        return json.loads(response['SecretString'])
    except Exception as e:
        print(f"Error fetching secret {secret_name}: {str(e)}")
        return {}


def success_response(body):
    """Return success response with CORS headers"""
    return {
        'statusCode': 200,
        'headers': {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': 'POST, OPTIONS',
            'Access-Control-Allow-Headers': 'Content-Type'
        },
        'body': json.dumps(body)
    }


def error_response(status_code, message):
    """Return error response with CORS headers"""
    return {
        'statusCode': status_code,
        'headers': {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': 'POST, OPTIONS',
            'Access-Control-Allow-Headers': 'Content-Type'
        },
        'body': json.dumps({'error': message})
    }
