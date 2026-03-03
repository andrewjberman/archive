#!/usr/bin/env python3
"""
test-model.py -- Verify a model works with the chat completions endpoint.

Usage:
    python org/threads/test-model.py
    python org/threads/test-model.py --model gpt-5.2
    python org/threads/test-model.py --model gpt-4o
"""

import argparse
import json
import os
import sys
from pathlib import Path

import boto3
from openai import OpenAI


def get_client(secret_name: str) -> OpenAI:
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        print(f"Fetching key from Secrets Manager ({secret_name})...")
        sm = boto3.client("secretsmanager", region_name="us-east-1")
        raw = sm.get_secret_value(SecretId=secret_name)["SecretString"]
        try:
            parsed = json.loads(raw)
            api_key = (
                parsed.get("api_key")
                or parsed.get("OPENAI_API_KEY")
                or parsed.get("openai_api_key")
                or raw
            )
        except (json.JSONDecodeError, AttributeError):
            api_key = raw
    return OpenAI(api_key=api_key)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--model",  default="gpt-5.2",          help="Model to test")
    parser.add_argument("--secret", default="openai-api-key",   help="AWS Secrets Manager secret name")
    args = parser.parse_args()

    print(f"Testing model: {args.model}")
    print(f"Endpoint:      chat.completions.create")
    print()

    try:
        client = get_client(args.secret)
    except Exception as e:
        print(f"FAIL: Could not create OpenAI client: {e}")
        sys.exit(1)

    try:
        # Test 1: basic call
        response = client.chat.completions.create(
            model=args.model,
            messages=[{"role": "user", "content": "Reply with exactly: OK"}],
            max_completion_tokens=10,
        )
        content = response.choices[0].message.content.strip()
        print(f"OK: Basic call: {repr(content)}")

        # Test 2: temperature parameter (orchestrator uses temperature=0.3)
        try:
            r2 = client.chat.completions.create(
                model=args.model,
                messages=[{"role": "user", "content": "Reply with exactly: OK"}],
                temperature=0.3,
            )
            print(f"OK: temperature=0.3 supported")
        except Exception as e:
            print(f"WARN: temperature not supported: {e}")
            print(f"     Orchestrator will need to drop temperature for this model.")

        response = response  # keep for usage print below
        content = response.choices[0].message.content.strip()
        print(f"OK: Model responded: {repr(content)}")
        print(f"    Usage: {response.usage}")
    except Exception as e:
        print(f"FAIL: {type(e).__name__}: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
