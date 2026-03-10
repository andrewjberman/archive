#!/usr/bin/env python3
"""
SmartX AI Supervisor v2 - Autonomous Pipeline Monitor with Tool Use

This AI supervisor has actual tools it can call to:
1. Check S3 exports and portal data
2. Invoke Lambda functions with retries
3. Execute shell commands for diagnostics
4. Write and execute fix scripts
5. Send alerts and recommendations

Uses OpenAI's function calling for autonomous decision-making.
Large token budget (128k) allows for complex reasoning and self-healing.
"""

import boto3
import json
import os
import sys
import time
import subprocess
from datetime import datetime, timedelta
from typing import Optional, Dict, Any, List
from openai import OpenAI

# =============================================================================
# Configuration
# =============================================================================

CONFIG = {
    'lambda_function': 'opal-smartx-ingestion-pipeline',
    's3_exports_bucket': 'opal-data-smartx-v2',
    's3_portal_bucket': 'opal-data-portal-v2',
    'region': 'us-east-1',
    'max_lambda_retries': 3,
    'expected_portfolios': ['UST', 'ST', 'INT', 'LTC', 'LTA'],
    'openai_model': 'gpt-4o',  # Use GPT-4o for best tool use
    'max_tokens': 4096,
    'log_file': '/var/log/ai-supervisor.log'
}

# =============================================================================
# AWS Clients
# =============================================================================

s3 = boto3.client('s3', region_name=CONFIG['region'])
lambda_client = boto3.client('lambda', region_name=CONFIG['region'])
secrets = boto3.client('secretsmanager', region_name=CONFIG['region'])

# =============================================================================
# Logging
# =============================================================================

def log(message: str, level: str = "INFO"):
    """Log with timestamp to both console and file"""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_line = f"[{timestamp}] [{level}] {message}"
    print(log_line)
    try:
        with open(CONFIG['log_file'], 'a') as f:
            f.write(log_line + '\n')
    except:
        pass

# =============================================================================
# Tool Definitions for OpenAI Function Calling
# =============================================================================

TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "check_s3_exports",
            "description": "Check S3 bucket for today's SmartX export files. Returns list of found portfolios and any missing ones.",
            "parameters": {
                "type": "object",
                "properties": {
                    "date": {
                        "type": "string",
                        "description": "Date to check exports for (YYYY-MM-DD format). Defaults to today."
                    }
                },
                "required": []
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "check_portal_data_freshness",
            "description": "Check when portal JSON files were last updated. Returns age in minutes for each file.",
            "parameters": {
                "type": "object",
                "properties": {
                    "files": {
                        "type": "array",
                        "items": {"type": "string"},
                        "description": "List of files to check. Defaults to main portfolio files."
                    }
                },
                "required": []
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "invoke_lambda",
            "description": "Invoke the SmartX ingestion Lambda function. Returns success status and any error messages.",
            "parameters": {
                "type": "object",
                "properties": {
                    "wait_for_completion": {
                        "type": "boolean",
                        "description": "Whether to wait for Lambda to complete (sync) or return immediately (async)"
                    }
                },
                "required": []
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "run_shell_command",
            "description": "Execute a shell command on the EC2 instance. Use for diagnostics, checking logs, or running scripts.",
            "parameters": {
                "type": "object",
                "properties": {
                    "command": {
                        "type": "string",
                        "description": "The shell command to execute"
                    },
                    "timeout": {
                        "type": "integer",
                        "description": "Timeout in seconds (default 30)"
                    }
                },
                "required": ["command"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "write_and_run_script",
            "description": "Write a Python or Bash script to a file and execute it. Use for creating fix scripts or complex diagnostics.",
            "parameters": {
                "type": "object",
                "properties": {
                    "filename": {
                        "type": "string",
                        "description": "Name of the script file to create (e.g., 'fix_exports.py')"
                    },
                    "content": {
                        "type": "string",
                        "description": "The script content"
                    },
                    "interpreter": {
                        "type": "string",
                        "enum": ["python3", "bash"],
                        "description": "The interpreter to use"
                    }
                },
                "required": ["filename", "content", "interpreter"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "wait_and_retry",
            "description": "Wait for a specified time then retry the previous failed operation.",
            "parameters": {
                "type": "object",
                "properties": {
                    "seconds": {
                        "type": "integer",
                        "description": "Seconds to wait before retrying"
                    },
                    "reason": {
                        "type": "string",
                        "description": "Reason for waiting (for logging)"
                    }
                },
                "required": ["seconds", "reason"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "report_status",
            "description": "Report final status and recommendations. Call this when done with all checks and fixes.",
            "parameters": {
                "type": "object",
                "properties": {
                    "status": {
                        "type": "string",
                        "enum": ["SUCCESS", "PARTIAL_SUCCESS", "FAILURE"],
                        "description": "Overall pipeline status"
                    },
                    "summary": {
                        "type": "string",
                        "description": "Summary of what happened"
                    },
                    "exports_ok": {
                        "type": "boolean",
                        "description": "Whether all 5 exports were found"
                    },
                    "lambda_ok": {
                        "type": "boolean",
                        "description": "Whether Lambda invocation succeeded"
                    },
                    "portal_ok": {
                        "type": "boolean",
                        "description": "Whether portal data was updated"
                    },
                    "recommendations": {
                        "type": "array",
                        "items": {"type": "string"},
                        "description": "List of recommendations for next steps"
                    }
                },
                "required": ["status", "summary"]
            }
        }
    }
]

# =============================================================================
# Tool Implementation Functions
# =============================================================================

def tool_check_s3_exports(date: str = None) -> Dict[str, Any]:
    """Check S3 for today's exports using pagination to find all files"""
    if not date:
        date = datetime.now().strftime("%Y-%m-%d")

    log(f"Checking S3 exports for {date}...")

    try:
        # Use paginator to get ALL objects (fixes MaxKeys=200 bug that missed recent exports)
        paginator = s3.get_paginator('list_objects_v2')
        pages = paginator.paginate(
            Bucket=CONFIG['s3_exports_bucket'],
            Prefix='exports/'
        )

        # Filter to today's files across all pages
        today_files = []
        total_objects = 0
        for page in pages:
            if 'Contents' not in page:
                continue
            total_objects += len(page['Contents'])
            for obj in page['Contents']:
                modified = obj['LastModified'].strftime("%Y-%m-%d")
                if modified == date:
                    today_files.append({
                        'key': obj['Key'],
                        'size': obj['Size'],
                        'modified': obj['LastModified'].isoformat()
                    })

        if total_objects == 0:
            return {'success': False, 'found': [], 'missing': CONFIG['expected_portfolios'], 'error': 'No exports found'}

        # Check for each portfolio
        found = []
        for portfolio in CONFIG['expected_portfolios']:
            for f in today_files:
                if f"/{portfolio}_" in f['key'] or f"_{portfolio}_" in f['key']:
                    found.append(portfolio)
                    break

        missing = list(set(CONFIG['expected_portfolios']) - set(found))

        return {
            'success': len(missing) == 0,
            'date': date,
            'found': found,
            'missing': missing,
            'files_count': len(today_files),
            'total_objects_scanned': total_objects,
            'sample_files': today_files[:5]
        }

    except Exception as e:
        return {'success': False, 'error': str(e)}

def tool_check_portal_data_freshness(files: List[str] = None) -> Dict[str, Any]:
    """Check portal data file timestamps"""
    if not files:
        files = [
            'json/portfolios/aum-metrics.json',
            'json/portfolios/aum-timeseries.json',
            'json/portfolios/account-distribution.json'
        ]

    log(f"Checking portal data freshness...")

    results = {}
    now = datetime.now(tz=None)

    for file_key in files:
        try:
            response = s3.head_object(
                Bucket=CONFIG['s3_portal_bucket'],
                Key=file_key
            )
            last_modified = response['LastModified'].replace(tzinfo=None)
            age_minutes = (now - last_modified).total_seconds() / 60

            results[file_key] = {
                'last_modified': last_modified.isoformat(),
                'age_minutes': round(age_minutes, 1),
                'fresh': age_minutes < 60  # Consider fresh if < 1 hour old
            }
        except Exception as e:
            results[file_key] = {'error': str(e)}

    all_fresh = all(r.get('fresh', False) for r in results.values())

    return {
        'success': all_fresh,
        'files': results,
        'all_fresh': all_fresh
    }

def tool_invoke_lambda(wait_for_completion: bool = True) -> Dict[str, Any]:
    """Invoke the ingestion Lambda"""
    log(f"Invoking Lambda: {CONFIG['lambda_function']}...")

    try:
        invocation_type = 'RequestResponse' if wait_for_completion else 'Event'

        response = lambda_client.invoke(
            FunctionName=CONFIG['lambda_function'],
            InvocationType=invocation_type,
            LogType='Tail'
        )

        status_code = response['StatusCode']

        if wait_for_completion:
            payload = json.loads(response['Payload'].read().decode())

            # Decode logs
            import base64
            log_result = base64.b64decode(response.get('LogResult', '')).decode()

            success = status_code == 200 and not payload.get('errorMessage')

            return {
                'success': success,
                'status_code': status_code,
                'payload': payload,
                'logs_tail': log_result[-1000:] if log_result else None
            }
        else:
            return {
                'success': status_code == 202,
                'status_code': status_code,
                'message': 'Lambda invoked asynchronously'
            }

    except Exception as e:
        return {'success': False, 'error': str(e)}

def tool_run_shell_command(command: str, timeout: int = 30) -> Dict[str, Any]:
    """Execute a shell command"""
    log(f"Running command: {command[:100]}...")

    # Security: Block dangerous commands
    dangerous = ['rm -rf /', 'mkfs', 'dd if=', ':(){', 'chmod -R 777 /']
    for d in dangerous:
        if d in command:
            return {'success': False, 'error': f'Blocked dangerous command pattern: {d}'}

    try:
        result = subprocess.run(
            command,
            shell=True,
            capture_output=True,
            text=True,
            timeout=timeout
        )

        return {
            'success': result.returncode == 0,
            'returncode': result.returncode,
            'stdout': result.stdout[-2000:] if result.stdout else '',
            'stderr': result.stderr[-500:] if result.stderr else ''
        }

    except subprocess.TimeoutExpired:
        return {'success': False, 'error': f'Command timed out after {timeout}s'}
    except Exception as e:
        return {'success': False, 'error': str(e)}

def tool_write_and_run_script(filename: str, content: str, interpreter: str) -> Dict[str, Any]:
    """Write and execute a script"""
    log(f"Writing and running script: {filename}...")

    # Security: Only allow scripts in /tmp
    if not filename.startswith('/tmp/'):
        filename = f'/tmp/{filename}'

    try:
        # Write script
        with open(filename, 'w') as f:
            f.write(content)

        # Make executable
        os.chmod(filename, 0o755)

        # Run script
        result = subprocess.run(
            [interpreter, filename],
            capture_output=True,
            text=True,
            timeout=120
        )

        return {
            'success': result.returncode == 0,
            'filename': filename,
            'returncode': result.returncode,
            'stdout': result.stdout[-2000:] if result.stdout else '',
            'stderr': result.stderr[-500:] if result.stderr else ''
        }

    except Exception as e:
        return {'success': False, 'error': str(e)}

def tool_wait_and_retry(seconds: int, reason: str) -> Dict[str, Any]:
    """Wait before retrying"""
    log(f"Waiting {seconds}s: {reason}")
    time.sleep(seconds)
    return {'success': True, 'waited': seconds, 'reason': reason}

def tool_report_status(status: str, summary: str, **kwargs) -> Dict[str, Any]:
    """Report final status and write summary file"""
    log("=" * 60)
    log(f"FINAL STATUS: {status}")
    log(f"Summary: {summary}")

    if kwargs.get('recommendations'):
        log("Recommendations:")
        for rec in kwargs['recommendations']:
            log(f"  - {rec}")

    log("=" * 60)

    # Write human-readable summary file
    summary_file = '/var/log/smartx-ai-summary.txt'
    try:
        with open(summary_file, 'w') as f:
            f.write("=" * 60 + "\n")
            f.write("SmartX AI Supervisor - Pipeline Summary\n")
            f.write("=" * 60 + "\n\n")
            f.write(f"Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S UTC')}\n")
            f.write(f"Status: {status}\n\n")
            f.write(f"Summary:\n{summary}\n\n")

            if kwargs.get('exports_ok') is not None:
                f.write(f"Exports OK: {'Yes' if kwargs['exports_ok'] else 'No'}\n")
            if kwargs.get('lambda_ok') is not None:
                f.write(f"Lambda OK: {'Yes' if kwargs['lambda_ok'] else 'No'}\n")
            if kwargs.get('portal_ok') is not None:
                f.write(f"Portal Updated: {'Yes' if kwargs['portal_ok'] else 'No'}\n")

            if kwargs.get('recommendations'):
                f.write("\nRecommendations:\n")
                for rec in kwargs['recommendations']:
                    f.write(f"  - {rec}\n")

            f.write("\n" + "=" * 60 + "\n")
            f.write("To check portal data freshness:\n")
            f.write("  aws s3 ls s3://opal-data-portal-v2/json/portfolios/ --human-readable\n")
            f.write("=" * 60 + "\n")

        log(f"Summary written to {summary_file}")
    except Exception as e:
        log(f"Failed to write summary file: {e}", level="WARN")

    return {
        'status': status,
        'summary': summary,
        **kwargs
    }

# Map tool names to functions
TOOL_FUNCTIONS = {
    'check_s3_exports': tool_check_s3_exports,
    'check_portal_data_freshness': tool_check_portal_data_freshness,
    'invoke_lambda': tool_invoke_lambda,
    'run_shell_command': tool_run_shell_command,
    'write_and_run_script': tool_write_and_run_script,
    'wait_and_retry': tool_wait_and_retry,
    'report_status': tool_report_status
}

# =============================================================================
# AI Agent Loop
# =============================================================================

def execute_tool(tool_name: str, arguments: Dict[str, Any]) -> str:
    """Execute a tool and return result as string"""
    if tool_name not in TOOL_FUNCTIONS:
        return json.dumps({'error': f'Unknown tool: {tool_name}'})

    try:
        result = TOOL_FUNCTIONS[tool_name](**arguments)
        return json.dumps(result, indent=2, default=str)
    except Exception as e:
        return json.dumps({'error': str(e)})

def run_ai_agent(client: OpenAI) -> Dict[str, Any]:
    """Run the AI agent loop with tool use"""

    system_prompt = """You are an AI supervisor for the SmartX data pipeline. Your job is to:

1. VERIFY that all 5 portfolio exports (UST, ST, INT, LTC, LTA) exist in S3
2. INVOKE the Lambda function to process exports and update portal
3. VERIFY that portal data was updated
4. DIAGNOSE and FIX any issues you find

You have access to tools that let you:
- Check S3 exports and portal data
- Invoke Lambda functions
- Run shell commands for diagnostics
- Write and execute fix scripts
- Wait and retry failed operations

IMPORTANT GUIDELINES:
- Start by checking S3 exports
- If exports are missing, check the export logs and report the issue
- If exports are OK, invoke the Lambda
- If Lambda fails, try to diagnose why and retry up to 3 times
- If Lambda succeeds, verify portal data was updated
- Always end by calling report_status with your final assessment

Be systematic and thorough. If something fails, try to understand why before giving up.
You have a large token budget - use it to reason through problems carefully."""

    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": f"""The SmartX export pipeline has just completed running Docker containers
for all 5 portfolios. Please verify the pipeline completed successfully:

1. Check that all 5 exports (UST, ST, INT, LTC, LTA) are in S3
2. If exports are OK, invoke the ingestion Lambda to update portal data
3. Verify portal JSON files were updated
4. Report your findings and any issues

Current time: {datetime.now().isoformat()}
Expected exports date: {datetime.now().strftime('%Y-%m-%d')}

Begin your verification now."""}
    ]

    max_iterations = 15
    final_report = None

    for iteration in range(max_iterations):
        log(f"\n--- AI Agent Iteration {iteration + 1}/{max_iterations} ---")

        try:
            response = client.chat.completions.create(
                model=CONFIG['openai_model'],
                messages=messages,
                tools=TOOLS,
                tool_choice="auto",
                max_tokens=CONFIG['max_tokens']
            )

            assistant_message = response.choices[0].message
            messages.append(assistant_message)

            # Check if AI wants to call tools
            if assistant_message.tool_calls:
                for tool_call in assistant_message.tool_calls:
                    tool_name = tool_call.function.name
                    try:
                        arguments = json.loads(tool_call.function.arguments)
                    except:
                        arguments = {}

                    log(f"AI calling tool: {tool_name}")
                    log(f"  Arguments: {json.dumps(arguments)[:200]}")

                    # Execute the tool
                    result = execute_tool(tool_name, arguments)
                    log(f"  Result: {result[:300]}...")

                    # Add tool result to messages
                    messages.append({
                        "role": "tool",
                        "tool_call_id": tool_call.id,
                        "content": result
                    })

                    # Check if this was the final report
                    if tool_name == 'report_status':
                        final_report = json.loads(result)

            # Check if AI is done (no more tool calls and has content)
            if not assistant_message.tool_calls and assistant_message.content:
                log(f"AI message: {assistant_message.content[:500]}")

                # If we have a final report, we're done
                if final_report:
                    break

        except Exception as e:
            log(f"AI agent error: {e}", level="ERROR")
            import traceback
            traceback.print_exc()
            break

    return final_report or {'status': 'ERROR', 'summary': 'AI agent did not complete'}

# =============================================================================
# Main Entry Point
# =============================================================================

def get_openai_key() -> Optional[str]:
    """Fetch OpenAI API key from Secrets Manager"""
    try:
        response = secrets.get_secret_value(SecretId='ai/claude-api-key')
        return response['SecretString']
    except Exception as e:
        log(f"Failed to get OpenAI key: {e}", level="ERROR")
        return None

def main():
    log("=" * 60)
    log("SmartX AI Supervisor v2 - Autonomous Pipeline Monitor")
    log("=" * 60)
    log(f"Model: {CONFIG['openai_model']}")
    log(f"Max tokens: {CONFIG['max_tokens']}")
    log("")

    # Get OpenAI key
    api_key = get_openai_key()
    if not api_key:
        log("FATAL: Could not get OpenAI API key", level="ERROR")
        # Fall back to simple verification
        log("Falling back to simple verification...")
        result = tool_check_s3_exports()
        if result['success']:
            log("Exports OK, invoking Lambda...")
            lambda_result = tool_invoke_lambda()
            if lambda_result['success']:
                log("Lambda succeeded")
                return 0
            else:
                log(f"Lambda failed: {lambda_result}", level="ERROR")
                return 1
        else:
            log(f"Exports verification failed: {result}", level="ERROR")
            return 1

    # Initialize OpenAI client
    client = OpenAI(api_key=api_key)
    log("OpenAI client initialized")

    # Run the AI agent
    log("\nStarting AI agent loop...")
    result = run_ai_agent(client)

    # Determine exit code
    if result.get('status') == 'SUCCESS':
        return 0
    elif result.get('status') == 'PARTIAL_SUCCESS':
        return 0  # Still acceptable
    else:
        return 1

if __name__ == "__main__":
    sys.exit(main())
