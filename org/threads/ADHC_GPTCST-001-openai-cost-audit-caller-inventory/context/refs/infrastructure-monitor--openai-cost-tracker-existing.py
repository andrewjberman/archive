"""
OpenAI Cost Tracker - Real-Time Activity Correlation

Correlates actual CloudWatch Logs OpenAI API call activity with empirical cost data.
Calculates TODAY's cost based on TODAY's actual API calls.

Method:
1. Count OpenAI API calls in CloudWatch Logs (last 24 hours)
2. Apply empirical cost-per-call from historical data
3. Calculate: Today's Cost = Today's API Calls × Avg Cost Per Call

Empirical Data Source: Jan 18 - Feb 17, 2026 (30 days actual usage)
- Total cost: $2.51
- Total API calls: 933
- Cost per call: $0.00269 (blended average)

Author: Systems Architect
Date: 2026-02-17
"""

import boto3
import time
from datetime import datetime, timedelta, timezone
from typing import Dict

# ============================================================================
# EMPIRICAL COST DATA (from Jan 18 - Feb 17, 2026)
# ============================================================================

# Total: $2.51 / 933 API calls = $0.00269 per call (blended average)
COST_PER_API_CALL = 0.002690

# By service (empirical average cost per call)
COST_PER_CALL_BY_SERVICE = {
    'semantic-news-layer3-curation': 0.0110,   # $0.011/call (gpt-4o, 50 clusters)
    'news-trending-analysis': 0.0019,          # $0.002/call (mixed gpt-4o/mini)
    'trending-image-generator': 0.0019,        # $0.002/call (image gen or gpt-4o)
    'market-update-generator': 0.0018,         # $0.002/call (gpt-4o-mini mostly)
    'opal-infrastructure-monitor': 0.0036,     # $0.004/call (mixed analysis)
}

# Fallback daily estimate if CloudWatch fails
FALLBACK_DAILY_ESTIMATE = 0.0823  # $0.08/day (30-day average)

# Lambda functions that use OpenAI
OPENAI_FUNCTIONS = list(COST_PER_CALL_BY_SERVICE.keys())

# ============================================================================
# CloudWatch Log Query Functions
# ============================================================================

def count_openai_calls_today(function_name: str) -> int:
    """
    Count OpenAI API calls for a function today.

    Args:
        function_name: Lambda function name

    Returns:
        Number of API calls detected in last 24 hours
    """

    logs = boto3.client('logs')
    log_group = f'/aws/lambda/{function_name}'

    now = datetime.now(timezone.utc)
    start = now - timedelta(hours=24)

    try:
        # Simple filter for OpenAI API calls
        response = logs.filter_log_events(
            logGroupName=log_group,
            startTime=int(start.timestamp() * 1000),
            endTime=int(now.timestamp() * 1000),
            filterPattern='"api.openai.com"',
            limit=1000
        )

        # Count events
        call_count = len(response.get('events', []))

        # Handle pagination if needed
        while 'nextToken' in response and call_count < 1000:
            response = logs.filter_log_events(
                logGroupName=log_group,
                startTime=int(start.timestamp() * 1000),
                endTime=int(now.timestamp() * 1000),
                filterPattern='"api.openai.com"',
                limit=1000,
                nextToken=response['nextToken']
            )
            call_count += len(response.get('events', []))

        return call_count

    except logs.exceptions.ResourceNotFoundException:
        # Log group doesn't exist (function not invoked recently)
        return 0
    except Exception as e:
        print(f"Warning: Could not query {function_name}: {e}")
        return 0


def get_today_openai_activity() -> Dict:
    """
    Get today's OpenAI activity across all functions.

    Queries CloudWatch Logs for actual API calls, applies empirical cost-per-call.

    Returns:
        Dict with activity and cost estimate
    """

    activity = {}
    total_calls = 0
    total_cost = 0.0

    for function_name in OPENAI_FUNCTIONS:
        call_count = count_openai_calls_today(function_name)

        if call_count > 0:
            # Calculate cost for this function
            cost_per_call = COST_PER_CALL_BY_SERVICE.get(function_name, COST_PER_API_CALL)
            function_cost = call_count * cost_per_call

            activity[function_name] = {
                'api_calls': call_count,
                'estimated_cost': function_cost,
                'cost_per_call': cost_per_call
            }

            total_calls += call_count
            total_cost += function_cost

    # Calculate projection
    now = datetime.now(timezone.utc)
    start_of_day = now.replace(hour=0, minute=0, second=0, microsecond=0)
    hours_elapsed = (now - start_of_day).total_seconds() / 3600

    if hours_elapsed > 0 and total_calls > 0:
        projected_daily = total_cost * (24 / hours_elapsed)
    else:
        projected_daily = FALLBACK_DAILY_ESTIMATE

    return {
        'timestamp': now.isoformat(),
        'hours_elapsed': hours_elapsed,
        'total_api_calls': total_calls,
        'cost_so_far': total_cost,
        'projected_daily_cost': projected_daily,
        'projected_monthly_cost': projected_daily * 30,
        'by_function': activity,
        'has_real_data': total_calls > 0
    }


# ============================================================================
# HTML Generation for Infrastructure Email
# ============================================================================

def get_openai_cost_html() -> str:
    """
    Generate HTML section for infrastructure email based on TODAY's actual activity.

    Queries CloudWatch Logs in real-time and calculates cost from actual API calls.
    """

    estimate = get_today_openai_activity()

    if not estimate['has_real_data']:
        # No activity today, show fallback
        return f"""
<div style="font-family: monospace; background: #f8f9fa; padding: 20px; border-radius: 5px; margin: 20px 0;">
    <h3 style="color: #007bff; margin-top: 0;">💰 OpenAI API Cost Estimate</h3>
    <div style="background: white; padding: 15px; border-radius: 5px;">
        <p><strong>No OpenAI activity detected today</strong></p>
        <p style="color: #6c757d; font-size: 0.9em;">
            Baseline estimate: ${FALLBACK_DAILY_ESTIMATE:.4f}/day (${FALLBACK_DAILY_ESTIMATE * 30:.2f}/month)
        </p>
    </div>
</div>
"""

    # Build function breakdown
    function_rows = ""
    for func, data in sorted(estimate['by_function'].items(), key=lambda x: x[1]['estimated_cost'], reverse=True):
        function_rows += f"""
            <tr style="border-bottom: 1px solid #dee2e6;">
                <td style="padding: 8px; font-size: 0.85em;">{func}</td>
                <td style="padding: 8px; text-align: right;">{data['api_calls']}</td>
                <td style="padding: 8px; text-align: right;">${data['estimated_cost']:.4f}</td>
            </tr>
"""

    hours_elapsed = estimate['hours_elapsed']
    projection_color = "#28a745" if estimate['projected_daily_cost'] < 0.15 else "#ffc107"

    return f"""
<div style="font-family: monospace; background: #f8f9fa; padding: 20px; border-radius: 5px; margin: 20px 0;">
    <h3 style="color: #007bff; margin-top: 0;">💰 OpenAI API Cost (Real-Time Activity)</h3>

    <div style="background: white; padding: 15px; border-radius: 5px; margin-bottom: 15px;">
        <h4 style="margin-top: 0;">Today's Usage ({hours_elapsed:.1f} hours elapsed)</h4>
        <table style="width: 100%; border-collapse: collapse;">
            <tr>
                <td style="padding: 5px;"><strong>API Calls (so far):</strong></td>
                <td style="padding: 5px; text-align: right;">{estimate['total_api_calls']}</td>
            </tr>
            <tr>
                <td style="padding: 5px;"><strong>Cost (so far):</strong></td>
                <td style="padding: 5px; text-align: right;">${estimate['cost_so_far']:.4f}</td>
            </tr>
            <tr style="border-top: 2px solid #dee2e6;">
                <td style="padding: 5px;"><strong>Projected Daily:</strong></td>
                <td style="padding: 5px; text-align: right; font-size: 1.2em; color: {projection_color};">
                    <strong>${estimate['projected_daily_cost']:.4f}</strong>
                </td>
            </tr>
            <tr>
                <td style="padding: 5px;"><strong>Projected Monthly:</strong></td>
                <td style="padding: 5px; text-align: right;">${estimate['projected_monthly_cost']:.2f}</td>
            </tr>
        </table>
    </div>

    <div style="background: white; padding: 15px; border-radius: 5px; margin-bottom: 15px;">
        <h4 style="margin-top: 0;">Activity by Function (Today)</h4>
        <table style="width: 100%; border-collapse: collapse; font-size: 0.9em;">
            <tr style="background: #e9ecef;">
                <th style="padding: 8px; text-align: left;">Function</th>
                <th style="padding: 8px; text-align: right;">Calls</th>
                <th style="padding: 8px; text-align: right;">Est. Cost</th>
            </tr>
{function_rows}
        </table>
    </div>

    <div style="background: #e7f3ff; padding: 12px; border-radius: 5px; border-left: 4px solid #007bff; font-size: 0.9em;">
        <strong>📊 Model:</strong> Real-time CloudWatch activity × empirical cost-per-call<br>
        <strong>🔢 Multiplier:</strong> ${COST_PER_API_CALL:.5f} per call (blended avg from 30-day data)<br>
        <strong>🔄 Updates:</strong> Live - queries CloudWatch Logs for actual API calls<br>
        <strong>📈 Baseline:</strong> ${FALLBACK_DAILY_ESTIMATE:.4f}/day (30-day avg for reference)
    </div>
</div>
"""


def get_openai_cost_text() -> str:
    """Text version for plain-text emails."""

    estimate = get_today_openai_activity()

    if not estimate['has_real_data']:
        return f"""
{"="*70}
OPENAI API COST ESTIMATE
{"="*70}
No OpenAI activity detected today.
Baseline estimate: ${FALLBACK_DAILY_ESTIMATE:.4f}/day
{"="*70}
"""

    lines = []
    lines.append("="*70)
    lines.append("OPENAI API COST (TODAY'S ACTIVITY)")
    lines.append("="*70)
    lines.append("")
    lines.append(f"Today's Usage ({estimate['hours_elapsed']:.1f} hours elapsed):")
    lines.append(f"  API Calls:       {estimate['total_api_calls']}")
    lines.append(f"  Cost (so far):   ${estimate['cost_so_far']:.4f}")
    lines.append(f"  Projected Daily: ${estimate['projected_daily_cost']:.4f}")
    lines.append(f"  Projected Monthly: ${estimate['projected_monthly_cost']:.2f}")
    lines.append("")

    if estimate['by_function']:
        lines.append("Activity by Function:")
        for func, data in sorted(estimate['by_function'].items(), key=lambda x: x[1]['estimated_cost'], reverse=True):
            lines.append(f"  {func}: {data['api_calls']} calls → ${data['estimated_cost']:.4f}")

    lines.append("")
    lines.append(f"Model: ${COST_PER_API_CALL:.5f} per call (empirical from 30-day data)")
    lines.append(f"Baseline: ${FALLBACK_DAILY_ESTIMATE:.4f}/day (30-day avg)")
    lines.append("="*70)

    return "\n".join(lines)


# Test
if __name__ == '__main__':
    print("Querying CloudWatch for today's OpenAI activity...\n")
    result = get_today_openai_activity()

    if result['has_real_data']:
        print(f"✅ Found {result['total_api_calls']} API calls today")
        print(f"   Cost so far: ${result['cost_so_far']:.4f}")
        print(f"   Projected daily: ${result['projected_daily_cost']:.4f}")
        print(f"   Projected monthly: ${result['projected_monthly_cost']:.2f}")
        print()
        for func, data in result['by_function'].items():
            print(f"   - {func}: {data['api_calls']} calls")
    else:
        print("ℹ️  No OpenAI activity detected today")

    print("\n" + "="*70)
    print(get_openai_cost_text())
