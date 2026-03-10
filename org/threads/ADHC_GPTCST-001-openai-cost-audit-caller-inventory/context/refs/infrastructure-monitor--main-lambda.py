"""
Opal Infrastructure Monitor

Daily infrastructure health report for Opal Capital AWS infrastructure.

Schedule: 9 AM ET weekdays (EventBridge)
Region: us-east-1 (canonical)

Monitors:
1. Lambda execution health (errors, invocations)
2. SmartX pipeline (EC2 + S3 exports + Lambda processing)
3. OpenAI/AI call success rates
4. AWS costs breakdown
5. AI-powered error analysis for failing Lambdas

Author: AWS Engineer Agent
Created: 2025-12-30
Updated: 2025-12-30 - Added AI error analysis
"""

import json
import boto3
from datetime import datetime, timedelta, timezone
from typing import Dict, List, Any, Optional
import re

# OpenAI for AI analysis
try:
    from openai import OpenAI
    OPENAI_AVAILABLE = True
    print("[AI] OpenAI library loaded successfully")
except ImportError as e:
    OPENAI_AVAILABLE = False
    print(f"[WARN] OpenAI not available - AI analysis disabled: {e}")

# =============================================================================
# AWS CLIENTS - All us-east-1 (canonical region)
# =============================================================================

REGION = 'us-east-1'

cloudwatch = boto3.client('cloudwatch', region_name=REGION)
logs = boto3.client('logs', region_name=REGION)
lambda_client = boto3.client('lambda', region_name=REGION)
s3 = boto3.client('s3', region_name=REGION)
ec2 = boto3.client('ec2', region_name=REGION)
ses = boto3.client('ses', region_name=REGION)
ce = boto3.client('ce', region_name=REGION)
events = boto3.client('events', region_name=REGION)
secretsmanager = boto3.client('secretsmanager', region_name=REGION)

# =============================================================================
# CONFIGURATION
# =============================================================================

EMAIL_RECIPIENT = "andrew@opalinvest.com"
EMAIL_SENDER = "andrew@opalinvest.com"

# SmartX EC2 instance
SMARTX_EC2_INSTANCE_ID = "i-06ebcb27395eb3f49"
SMARTX_S3_BUCKET = "opal-data-smartx-v2"
SMARTX_LAMBDA = "opal-smartx-ingestion-pipeline"

# Report archive location
REPORT_BUCKET = "opal-data-portal-v2"
REPORT_PREFIX = "infrastructure/reports/"

# Lambdas that use OpenAI (for AI tracking)
OPENAI_LAMBDAS = [
    "opal-news-layer3-curation",
    "news-trending-analysis",
    "opal-trending-image-generator",
    "opal-infrastructure-monitor"
]

# AI Error Analysis Configuration
OPENAI_SECRET = "opal/external-apis"
OPENAI_MODEL = "gpt-4o-mini"  # Fast and cost-effective for analysis
MAX_ERROR_LOGS_PER_FUNCTION = 10
MAX_FUNCTIONS_TO_ANALYZE = 5

# System prompt for AI error analysis
ERROR_ANALYSIS_SYSTEM_PROMPT = """You are an AWS infrastructure analyst for Opal Capital, a quantitative investment firm.

Your task is to analyze CloudWatch error logs and provide actionable insights.

## Context
Opal Capital runs several automated pipelines:
- **News Pipeline**: Ingests financial news, scores sentiment with FinBERT, curates trending topics with GPT
- **Portal Data**: Market metrics, fear/greed index, volatility data for investor dashboard
- **SmartX Pipeline**: Portfolio data from SmartX platform (EC2 Docker → S3 → Lambda)
- **FRED Data**: Federal Reserve economic data ingestion

## Analysis Guidelines

1. **Identify Root Cause**: Look for the actual error, not just symptoms
   - Import errors → Missing dependency or wrong handler
   - Timeout → Function too slow or infinite loop
   - Permission denied → IAM role missing policy
   - API errors → External service issue or rate limit

2. **Assess Severity**:
   - CRITICAL: Investor-facing data is stale/broken
   - HIGH: Scheduled automation completely failing
   - MEDIUM: Partial failures or degraded functionality
   - LOW: Cosmetic or non-essential features

3. **Provide Specific Fixes**: Don't be vague
   - Bad: "Check the configuration"
   - Good: "Update Lambda handler from 'lambda_function.handler' to 'main.lambda_handler'"

4. **Consider Patterns**:
   - Same error across multiple functions → Shared dependency issue
   - Errors at specific times → Schedule conflict or resource contention
   - Intermittent errors → Rate limiting or network issues

## Output Format

For each function with errors, provide:

**[Function Name]** - [Severity]
- Root Cause: [One sentence]
- Evidence: [Key log line or pattern]
- Fix: [Specific action to take]
- Impact: [What's affected if not fixed]

End with a SUMMARY section listing priority order for fixes."""

# OpenAI client cache
_openai_client = None

# =============================================================================
# LAMBDA HANDLER
# =============================================================================

def lambda_handler(event, context):
    """Main entry point for infrastructure monitoring."""
    start_time = datetime.now(timezone.utc)
    print(f"[START] Opal Infrastructure Monitor - {start_time.isoformat()}")

    report = {
        "timestamp": start_time.isoformat(),
        "status": "success",
        "sections": {}
    }

    try:
        # 1. Lambda Execution Health
        print("[CHECK] Lambda execution health...")
        report["sections"]["lambda_health"] = check_lambda_health()

        # 2. SmartX Pipeline Status
        print("[CHECK] SmartX pipeline status...")
        report["sections"]["smartx_pipeline"] = check_smartx_pipeline()

        # 3. OpenAI/AI Call Success
        print("[CHECK] OpenAI call success...")
        report["sections"]["ai_tracking"] = check_ai_calls()

        # 4. AWS Costs
        print("[CHECK] AWS costs...")
        report["sections"]["aws_costs"] = get_aws_costs()

        # 5. Security Sweep (from daily 7 AM report)
        print("[CHECK] Security sweep...")
        report["sections"]["security_sweep"] = check_security_sweep()

        # 6. AI Error Analysis (only if there are errors)
        lambda_health = report["sections"].get("lambda_health", {})
        if lambda_health.get('functions_with_errors', 0) > 0:
            print("[AI] Running AI error analysis...")
            report["sections"]["ai_analysis"] = analyze_errors_with_ai(lambda_health)
        else:
            report["sections"]["ai_analysis"] = None

        # 7. Generate and send report
        print("[REPORT] Generating report...")
        email_body = format_report(report)

        print("[EMAIL] Sending report...")
        send_email(email_body, report)

        # 8. Archive report
        archive_report(report, start_time)

    except Exception as e:
        print(f"[ERROR] {str(e)}")
        report["status"] = "error"
        report["error"] = str(e)
        # Still try to send error notification
        try:
            send_error_email(str(e))
        except:
            pass

    duration_ms = int((datetime.now(timezone.utc) - start_time).total_seconds() * 1000)
    print(f"[END] Duration: {duration_ms}ms")

    return {
        "statusCode": 200 if report["status"] == "success" else 500,
        "body": json.dumps(report, default=str)
    }


# =============================================================================
# 1. LAMBDA HEALTH CHECK
# =============================================================================

def check_lambda_health() -> Dict:
    """Check all Lambda functions for errors and invocations in last 24h."""

    # Get all Lambda functions in us-east-1
    functions = []
    paginator = lambda_client.get_paginator('list_functions')
    for page in paginator.paginate():
        functions.extend(page['Functions'])

    print(f"[LAMBDA] Found {len(functions)} functions")

    now = datetime.now(timezone.utc)
    start_time = now - timedelta(hours=24)

    results = []
    total_errors = 0
    total_invocations = 0

    for func in functions:
        func_name = func['FunctionName']

        # Get error count
        errors = get_metric_sum(
            'AWS/Lambda', 'Errors',
            [{'Name': 'FunctionName', 'Value': func_name}],
            start_time, now
        )

        # Get invocation count
        invocations = get_metric_sum(
            'AWS/Lambda', 'Invocations',
            [{'Name': 'FunctionName', 'Value': func_name}],
            start_time, now
        )

        status = "ok"
        if errors > 0:
            status = "error"
        elif invocations == 0:
            status = "idle"

        results.append({
            "function": func_name,
            "errors": errors,
            "invocations": invocations,
            "status": status
        })

        total_errors += errors
        total_invocations += invocations

    # Sort by errors (highest first), then by invocations
    results.sort(key=lambda x: (-x['errors'], -x['invocations']))

    return {
        "total_functions": len(functions),
        "total_errors": total_errors,
        "total_invocations": total_invocations,
        "functions_with_errors": sum(1 for r in results if r['errors'] > 0),
        "idle_functions": sum(1 for r in results if r['status'] == 'idle'),
        "details": results
    }


def get_metric_sum(namespace: str, metric_name: str, dimensions: List[Dict],
                   start_time: datetime, end_time: datetime) -> int:
    """Get sum of a CloudWatch metric over time period."""
    try:
        response = cloudwatch.get_metric_statistics(
            Namespace=namespace,
            MetricName=metric_name,
            Dimensions=dimensions,
            StartTime=start_time,
            EndTime=end_time,
            Period=86400,  # 24 hours
            Statistics=['Sum']
        )

        datapoints = response.get('Datapoints', [])
        if datapoints:
            return int(datapoints[0].get('Sum', 0))
        return 0
    except Exception as e:
        print(f"[WARN] Metric error for {metric_name}: {e}")
        return 0


# =============================================================================
# 2. SMARTX PIPELINE CHECK
# =============================================================================

def check_smartx_pipeline() -> Dict:
    """Check SmartX EC2 + S3 exports + Lambda processing."""

    result = {
        "ec2_status": "unknown",
        "latest_export": None,
        "export_age_hours": None,
        "lambda_status": "unknown",
        "status": "unknown"
    }

    # Check EC2 instance status
    try:
        response = ec2.describe_instances(InstanceIds=[SMARTX_EC2_INSTANCE_ID])
        if response['Reservations']:
            instance = response['Reservations'][0]['Instances'][0]
            result["ec2_status"] = instance['State']['Name']
    except Exception as e:
        print(f"[WARN] EC2 check failed: {e}")
        result["ec2_status"] = f"error: {str(e)[:50]}"

    # Check latest S3 export
    try:
        # List exports folder to find latest run
        response = s3.list_objects_v2(
            Bucket=SMARTX_S3_BUCKET,
            Prefix="exports/",
            Delimiter="/"
        )

        if 'CommonPrefixes' in response:
            # Get latest run folder by name (they're timestamped)
            runs = [p['Prefix'] for p in response['CommonPrefixes']]
            runs.sort(reverse=True)

            if runs:
                latest_run = runs[0]
                result["latest_export"] = latest_run.replace("exports/", "").rstrip("/")

                # Check files in latest run
                files_response = s3.list_objects_v2(
                    Bucket=SMARTX_S3_BUCKET,
                    Prefix=latest_run,
                    MaxKeys=10
                )

                if 'Contents' in files_response and files_response['Contents']:
                    # Get most recent file modification time
                    latest_file = max(files_response['Contents'], key=lambda x: x['LastModified'])
                    export_time = latest_file['LastModified']
                    age_hours = (datetime.now(timezone.utc) - export_time.replace(tzinfo=timezone.utc)).total_seconds() / 3600
                    result["export_age_hours"] = round(age_hours, 1)
    except Exception as e:
        print(f"[WARN] S3 export check failed: {e}")

    # Check SmartX Lambda last invocation
    try:
        now = datetime.now(timezone.utc)
        start_time = now - timedelta(hours=24)

        invocations = get_metric_sum(
            'AWS/Lambda', 'Invocations',
            [{'Name': 'FunctionName', 'Value': SMARTX_LAMBDA}],
            start_time, now
        )

        errors = get_metric_sum(
            'AWS/Lambda', 'Errors',
            [{'Name': 'FunctionName', 'Value': SMARTX_LAMBDA}],
            start_time, now
        )

        if errors > 0:
            result["lambda_status"] = f"error ({errors} errors)"
        elif invocations > 0:
            result["lambda_status"] = f"ok ({invocations} runs)"
        else:
            result["lambda_status"] = "idle (no runs in 24h)"
    except Exception as e:
        print(f"[WARN] Lambda check failed: {e}")
        result["lambda_status"] = f"error: {str(e)[:50]}"

    # Overall status
    # SmartX runs Mon-Fri at 5 PM ET only, so need weekend-aware staleness check
    now = datetime.now()
    is_weekday = now.weekday() < 5
    is_weekend = now.weekday() >= 5  # Sat=5, Sun=6
    is_monday_morning = now.weekday() == 0 and now.hour < 18  # Monday before 6 PM

    # Use longer threshold on weekends and Monday morning (Fri 5PM → Mon 5PM = 72h)
    stale_threshold_hours = 72 if (is_weekend or is_monday_morning) else 48

    if "error" in str(result["lambda_status"]).lower():
        result["status"] = "error"
    elif result["export_age_hours"] and result["export_age_hours"] > stale_threshold_hours:
        result["status"] = "stale"
    elif is_weekday and result["ec2_status"] == "stopped" and now.hour >= 17:
        # Only warn if EC2 stopped AFTER expected run time on weekdays
        result["status"] = "warning"
    else:
        result["status"] = "ok"

    return result


# =============================================================================
# 3. AI/OPENAI CALL TRACKING
# =============================================================================

def check_ai_calls() -> Dict:
    """Check OpenAI call success/failure from CloudWatch logs."""

    results = []
    total_success = 0
    total_failed = 0

    now = datetime.now(timezone.utc)
    start_time = now - timedelta(hours=24)
    start_ms = int(start_time.timestamp() * 1000)

    for func_name in OPENAI_LAMBDAS:
        log_group = f"/aws/lambda/{func_name}"

        func_result = {
            "function": func_name,
            "success": 0,
            "failed": 0,
            "tokens_used": 0
        }

        try:
            # Check if log group exists
            try:
                logs.describe_log_groups(logGroupNamePrefix=log_group, limit=1)
            except:
                continue

            # Search for OpenAI success patterns
            success_patterns = ["Tokens used:", "[OPENAI] Tokens:", "tokens_used"]
            for pattern in success_patterns:
                try:
                    response = logs.filter_log_events(
                        logGroupName=log_group,
                        startTime=start_ms,
                        filterPattern=f'"{pattern}"',
                        limit=100
                    )

                    for event in response.get('events', []):
                        func_result["success"] += 1
                        # Try to extract token count
                        match = re.search(r'(\d{2,6})\s*(tokens|in|out)', event['message'].lower())
                        if match:
                            func_result["tokens_used"] += int(match.group(1))
                except:
                    pass

            # Search for OpenAI error patterns
            error_patterns = ["[OPENAI ERROR]", "OpenAI API error", "openai.error"]
            for pattern in error_patterns:
                try:
                    response = logs.filter_log_events(
                        logGroupName=log_group,
                        startTime=start_ms,
                        filterPattern=f'"{pattern}"',
                        limit=50
                    )
                    func_result["failed"] += len(response.get('events', []))
                except:
                    pass

        except Exception as e:
            print(f"[WARN] AI check for {func_name} failed: {e}")

        if func_result["success"] > 0 or func_result["failed"] > 0:
            results.append(func_result)
            total_success += func_result["success"]
            total_failed += func_result["failed"]

    return {
        "total_success": total_success,
        "total_failed": total_failed,
        "success_rate": round(total_success / (total_success + total_failed) * 100, 1) if (total_success + total_failed) > 0 else 100,
        "details": results
    }


# =============================================================================
# 4. AWS COSTS
# =============================================================================

def get_aws_costs() -> Dict:
    """Get AWS costs for current month."""

    today = datetime.now()
    first_of_month = today.replace(day=1)

    # Cost Explorer needs dates as strings
    start_date = first_of_month.strftime('%Y-%m-%d')
    end_date = today.strftime('%Y-%m-%d')

    result = {
        "period": f"{start_date} to {end_date}",
        "total_mtd": 0,
        "daily_avg": 0,
        "by_service": []
    }

    try:
        response = ce.get_cost_and_usage(
            TimePeriod={
                'Start': start_date,
                'End': end_date
            },
            Granularity='MONTHLY',
            Metrics=['UnblendedCost'],
            GroupBy=[{'Type': 'DIMENSION', 'Key': 'SERVICE'}]
        )

        services = []
        total = 0

        for group in response['ResultsByTime'][0].get('Groups', []):
            service = group['Keys'][0]
            cost = float(group['Metrics']['UnblendedCost']['Amount'])

            if cost > 0.001:  # Only include services with meaningful cost
                services.append({
                    "service": service,
                    "cost": round(cost, 2)
                })
                total += cost

        # Sort by cost descending
        services.sort(key=lambda x: -x['cost'])

        days_elapsed = (today - first_of_month).days + 1

        result["total_mtd"] = round(total, 2)
        result["daily_avg"] = round(total / days_elapsed, 2) if days_elapsed > 0 else 0
        result["by_service"] = services[:10]  # Top 10 services

    except Exception as e:
        print(f"[WARN] Cost check failed: {e}")
        result["error"] = str(e)

    return result


# =============================================================================
# 5. SECURITY SWEEP
# =============================================================================

def check_security_sweep() -> Dict:
    """Fetch latest security sweep report from S3 (generated at 7 AM daily)."""

    result = {
        "report_date": None,
        "critical_issues": 0,
        "high_issues": 0,
        "medium_issues": 0,
        "low_issues": 0,
        "ai_summary": None,
        "findings": None,
        "status": "ok"
    }

    try:
        today = datetime.now().strftime('%Y-%m-%d')
        bucket = REPORT_BUCKET
        prefix = "security-reports/"

        # 1. Get issue counts from latest_score.json
        try:
            score_obj = s3.get_object(Bucket=bucket, Key=f"{prefix}latest_score.json")
            score_data = json.loads(score_obj['Body'].read())
            result["report_date"] = score_data.get("date")
            result["critical_issues"] = score_data.get("critical", 0)
            result["high_issues"] = score_data.get("high", 0)
            result["medium_issues"] = score_data.get("medium", 0)
            result["low_issues"] = score_data.get("low", 0)
        except Exception as e:
            print(f"[SECURITY] Could not fetch counts: {e}")

        # 2. Get AI summary
        try:
            ai_obj = s3.get_object(Bucket=bucket, Key=f"{prefix}latest_ai_summary.txt")
            result["ai_summary"] = ai_obj['Body'].read().decode('utf-8')
        except Exception as e:
            print(f"[SECURITY] Could not fetch AI summary: {e}")

        # 3. Get raw findings JSON (for any downstream use)
        try:
            findings_obj = s3.get_object(Bucket=bucket, Key=f"{prefix}{today}_findings.json")
            result["findings"] = json.loads(findings_obj['Body'].read())
        except Exception as e:
            print(f"[SECURITY] Could not fetch findings JSON: {e}")

        print(f"[SECURITY] Reports loaded for {today}: Critical={result['critical_issues']}, High={result['high_issues']}")

    except Exception as e:
        print(f"[SECURITY ERROR] Failed to fetch security reports: {e}")
        result["status"] = "error"
        result["error"] = str(e)

    return result


# =============================================================================
# 6. AI ERROR ANALYSIS
# =============================================================================

def get_openai_client() -> Optional[Any]:
    """Get or create OpenAI client with API key from Secrets Manager."""
    global _openai_client

    if not OPENAI_AVAILABLE:
        return None

    if _openai_client is None:
        try:
            secret = secretsmanager.get_secret_value(SecretId=OPENAI_SECRET)
            secret_data = json.loads(secret['SecretString'])
            api_key = secret_data.get('openai_api_key')
            if api_key:
                _openai_client = OpenAI(api_key=api_key)
                print("[AI] OpenAI client initialized")
            else:
                print("[AI] No openai_api_key in secret")
        except Exception as e:
            print(f"[AI ERROR] Failed to get API key: {e}")

    return _openai_client


def fetch_error_logs(func_name: str, hours: int = 24) -> List[str]:
    """Fetch recent error logs from CloudWatch for a Lambda function."""

    log_group = f"/aws/lambda/{func_name}"
    error_logs = []

    now = datetime.now(timezone.utc)
    start_time = now - timedelta(hours=hours)
    start_ms = int(start_time.timestamp() * 1000)

    try:
        # First check if log group exists
        try:
            response = logs.describe_log_groups(logGroupNamePrefix=log_group, limit=1)
            # Check if exact log group exists (not just prefix match)
            log_groups = response.get('logGroups', [])
            if not any(lg.get('logGroupName') == log_group for lg in log_groups):
                return [f"No log group found for {func_name}"]
        except Exception as e:
            return [f"Error checking log group for {func_name}: {str(e)[:100]}"]

        # Search for error patterns
        error_patterns = [
            "ERROR",
            "Error",
            "Exception",
            "Traceback",
            "Task timed out",
            "Runtime.ImportModuleError",
            "INIT_REPORT.*error"
        ]

        for pattern in error_patterns:
            try:
                response = logs.filter_log_events(
                    logGroupName=log_group,
                    startTime=start_ms,
                    filterPattern=pattern,
                    limit=MAX_ERROR_LOGS_PER_FUNCTION
                )

                for event in response.get('events', []):
                    msg = event.get('message', '').strip()
                    if msg and len(msg) > 10:  # Skip tiny messages
                        # Truncate very long messages
                        if len(msg) > 500:
                            msg = msg[:500] + "..."
                        if msg not in error_logs:  # Avoid duplicates
                            error_logs.append(msg)

            except Exception as e:
                print(f"[AI] Log search error for {func_name}: {e}")

        # If no errors found with patterns, get recent logs
        if not error_logs:
            try:
                response = logs.filter_log_events(
                    logGroupName=log_group,
                    startTime=start_ms,
                    limit=5
                )
                for event in response.get('events', []):
                    msg = event.get('message', '').strip()
                    if msg and 'REPORT' not in msg and 'START' not in msg and 'END' not in msg:
                        error_logs.append(msg[:500])
            except:
                pass

    except Exception as e:
        error_logs.append(f"Failed to fetch logs: {str(e)}")

    return error_logs[:MAX_ERROR_LOGS_PER_FUNCTION]


def analyze_errors_with_ai(lambda_health: Dict) -> Optional[str]:
    """Use OpenAI to analyze errors and provide recommendations."""

    client = get_openai_client()
    if not client:
        print("[AI] OpenAI client not available, skipping analysis")
        return None

    # Get functions with errors
    functions_with_errors = [
        f for f in lambda_health.get('details', [])
        if f.get('errors', 0) > 0
    ]

    if not functions_with_errors:
        return "No errors detected - all Lambda functions are healthy."

    # Limit to top N functions by error count
    functions_to_analyze = sorted(
        functions_with_errors,
        key=lambda x: -x['errors']
    )[:MAX_FUNCTIONS_TO_ANALYZE]

    print(f"[AI] Analyzing {len(functions_to_analyze)} functions with errors")

    # Fetch error logs for each function
    error_data = []
    for func in functions_to_analyze:
        func_name = func['function']
        error_count = func['errors']
        invocation_count = func['invocations']

        print(f"[AI] Fetching logs for {func_name}...")
        logs_list = fetch_error_logs(func_name)

        error_data.append({
            "function": func_name,
            "errors": error_count,
            "invocations": invocation_count,
            "error_rate": f"{(error_count/invocation_count*100):.1f}%" if invocation_count > 0 else "N/A",
            "logs": logs_list
        })

    # Build prompt for AI
    prompt = f"""Analyze the following Lambda function errors from the last 24 hours.

Date: {datetime.now().strftime('%Y-%m-%d %H:%M')} ET
Total Functions with Errors: {len(functions_with_errors)}

"""

    for data in error_data:
        prompt += f"""
---
## {data['function']}
- Errors: {data['errors']} / {data['invocations']} invocations ({data['error_rate']} failure rate)

### CloudWatch Logs:
"""
        for i, log in enumerate(data['logs'], 1):
            prompt += f"{i}. {log}\n"

    prompt += """
---

Please analyze these errors and provide your assessment following the format in your instructions."""

    try:
        print(f"[AI] Sending {len(prompt)} chars to OpenAI...")

        response = client.chat.completions.create(
            model=OPENAI_MODEL,
            messages=[
                {"role": "system", "content": ERROR_ANALYSIS_SYSTEM_PROMPT},
                {"role": "user", "content": prompt}
            ],
            max_tokens=1500,
            temperature=0.3
        )

        analysis = response.choices[0].message.content
        usage = response.usage
        print(f"[AI] Analysis complete. Tokens: {usage.prompt_tokens} in, {usage.completion_tokens} out")

        return analysis

    except Exception as e:
        print(f"[AI ERROR] Analysis failed: {e}")
        return f"AI analysis failed: {str(e)}"


# =============================================================================
# REPORT FORMATTING
# =============================================================================

def format_report(report: Dict) -> str:
    """Format the report as a readable email."""

    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M ET')

    lines = [
        "OPAL INFRASTRUCTURE REPORT",
        f"{timestamp}",
        "",
        "=" * 60,
        "AUTOMATION HEALTH (Last 24h)",
        "=" * 60,
        ""
    ]

    # Lambda Health
    lambda_data = report["sections"].get("lambda_health", {})
    lines.append(f"LAMBDA FUNCTIONS: {lambda_data.get('total_functions', 0)} total")
    lines.append(f"  Errors: {lambda_data.get('total_errors', 0)}")
    lines.append(f"  Invocations: {lambda_data.get('total_invocations', 0)}")
    lines.append(f"  Functions with errors: {lambda_data.get('functions_with_errors', 0)}")
    lines.append(f"  Idle functions: {lambda_data.get('idle_functions', 0)}")
    lines.append("")

    # Show functions with errors
    if lambda_data.get('functions_with_errors', 0) > 0:
        lines.append("FUNCTIONS WITH ERRORS:")
        for func in lambda_data.get('details', []):
            if func['errors'] > 0:
                lines.append(f"  * {func['function']}: {func['errors']} errors / {func['invocations']} invocations")
        lines.append("")

        # AI Analysis of errors
        ai_analysis = report["sections"].get("ai_analysis")
        if ai_analysis:
            lines.append("=" * 60)
            lines.append("AI ERROR ANALYSIS")
            lines.append("=" * 60)
            lines.append("")
            lines.append(ai_analysis)
            lines.append("")

    # SmartX Pipeline
    smartx = report["sections"].get("smartx_pipeline", {})
    lines.append("SMARTX PIPELINE:")
    lines.append(f"  EC2 Status: {smartx.get('ec2_status', 'unknown')}")
    lines.append(f"  Latest Export: {smartx.get('latest_export', 'unknown')}")
    if smartx.get('export_age_hours'):
        lines.append(f"  Export Age: {smartx.get('export_age_hours')} hours")
    lines.append(f"  Lambda Status: {smartx.get('lambda_status', 'unknown')}")
    lines.append(f"  Overall: {smartx.get('status', 'unknown').upper()}")
    lines.append("")

    # AI Tracking
    lines.append("=" * 60)
    lines.append("AI/OPENAI CALLS (Last 24h)")
    lines.append("=" * 60)
    lines.append("")

    ai_data = report["sections"].get("ai_tracking", {})
    lines.append(f"Success: {ai_data.get('total_success', 0)}")
    lines.append(f"Failed: {ai_data.get('total_failed', 0)}")
    lines.append(f"Success Rate: {ai_data.get('success_rate', 100)}%")

    if ai_data.get('details'):
        lines.append("")
        lines.append("By Function:")
        for func in ai_data['details']:
            lines.append(f"  {func['function']}: {func['success']} ok, {func['failed']} failed")
    lines.append("")

    # AWS Costs
    lines.append("=" * 60)
    lines.append("AWS COSTS (MTD)")
    lines.append("=" * 60)
    lines.append("")

    costs = report["sections"].get("aws_costs", {})
    lines.append(f"Period: {costs.get('period', 'unknown')}")
    lines.append(f"Total MTD: ${costs.get('total_mtd', 0):.2f}")
    lines.append(f"Daily Average: ${costs.get('daily_avg', 0):.2f}")
    lines.append("")

    if costs.get('by_service'):
        lines.append("Top Services:")
        for svc in costs['by_service'][:7]:
            lines.append(f"  {svc['service']}: ${svc['cost']:.2f}")

    lines.append("")

    # Security Sweep
    security = report["sections"].get("security_sweep", {})
    lines.append("=" * 60)
    lines.append("SECURITY (Daily 7 AM Sweep)")
    lines.append("=" * 60)
    lines.append("")

    critical = security.get('critical_issues', 0)
    high = security.get('high_issues', 0)
    medium = security.get('medium_issues', 0)
    low = security.get('low_issues', 0)

    lines.append(f"  CRITICAL: {critical}  |  HIGH: {high}  |  MEDIUM: {medium}  |  LOW: {low}")
    lines.append("")

    # AI summary (replaces score lines)
    if security.get('ai_summary'):
        lines.append("AI SECURITY BRIEFING:")
        lines.append("─" * 60)
        lines.append(security['ai_summary'])
        lines.append("")
    elif critical > 0:
        lines.append(f"WARNING: {critical} CRITICAL issues — review security-reports/ in S3.")
        lines.append("")

    if security.get('report_date'):
        lines.append(f"Full findings: s3://{REPORT_BUCKET}/security-reports/{security['report_date']}_comprehensive_report.txt")
        lines.append("")

    lines.append("=" * 60)
    lines.append("")
    lines.append("This is an automated message from opal-infrastructure-monitor")
    lines.append("Combines: Infrastructure Health + Security Sweep (7 AM)")
    lines.append("Region: us-east-1")

    return "\n".join(lines)


# =============================================================================
# EMAIL FUNCTIONS
# =============================================================================

def send_email(body: str, report: Dict):
    """Send the infrastructure report via SES."""

    # Determine if there are issues
    lambda_data = report["sections"].get("lambda_health", {})
    smartx = report["sections"].get("smartx_pipeline", {})
    ai_data = report["sections"].get("ai_tracking", {})
    security = report["sections"].get("security_sweep", {})

    has_issues = (
        lambda_data.get('functions_with_errors', 0) > 0 or
        smartx.get('status') in ['error', 'stale'] or
        ai_data.get('total_failed', 0) > 0 or
        security.get('critical_issues', 0) > 0 or
        security.get('high_issues', 0) > 0
    )

    date_str = datetime.now().strftime('%Y-%m-%d')

    # Build subject line with alert indicators
    if security.get('critical_issues', 0) > 0:
        subject = f"[Opal] 🚨 {security['critical_issues']} CRITICAL Security Issues - {date_str}"
    elif has_issues:
        subject = f"[Opal] ⚠️ Infrastructure + Security Report (Action Needed) - {date_str}"
    else:
        subject = f"[Opal] ✅ Infrastructure + Security Report - {date_str}"

    try:
        ses.send_email(
            Source=EMAIL_SENDER,
            Destination={'ToAddresses': [EMAIL_RECIPIENT]},
            Message={
                'Subject': {'Data': subject},
                'Body': {'Text': {'Data': body}}
            }
        )
        print(f"[EMAIL] Sent to {EMAIL_RECIPIENT}")
    except Exception as e:
        print(f"[ERROR] Email failed: {e}")
        raise


def send_error_email(error: str):
    """Send error notification."""

    date_str = datetime.now().strftime('%Y-%m-%d')
    subject = f"[Opal Infrastructure] MONITOR ERROR - {date_str}"
    body = f"""INFRASTRUCTURE MONITOR ERROR

The opal-infrastructure-monitor Lambda encountered an error:

{error}

Please check CloudWatch logs for details.

Timestamp: {datetime.now().isoformat()}
"""

    ses.send_email(
        Source=EMAIL_SENDER,
        Destination={'ToAddresses': [EMAIL_RECIPIENT]},
        Message={
            'Subject': {'Data': subject},
            'Body': {'Text': {'Data': body}}
        }
    )


def archive_report(report: Dict, timestamp: datetime):
    """Save report to S3 for historical reference."""

    key = f"{REPORT_PREFIX}{timestamp.strftime('%Y-%m-%d')}/{timestamp.strftime('%H-%M-%S')}.json"

    try:
        s3.put_object(
            Bucket=REPORT_BUCKET,
            Key=key,
            Body=json.dumps(report, indent=2, default=str),
            ContentType="application/json"
        )
        print(f"[ARCHIVE] Saved to s3://{REPORT_BUCKET}/{key}")
    except Exception as e:
        print(f"[WARN] Archive failed: {e}")


# =============================================================================
# LOCAL TESTING
# =============================================================================

if __name__ == "__main__":
    # For local testing
    result = lambda_handler({}, None)
    print(json.dumps(result, indent=2, default=str))
