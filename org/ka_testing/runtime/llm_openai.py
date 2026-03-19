"""
OpenAI provider variant of llm.py.

Drop-in replacement with the same public API:
  invoke_llm(), invoke_llm_staged(), get_last_trace()
  scan_signals(), evaluate_transition_predicate(), StagePredicateResult

Uses openai>=1.0.0. Set OPENAI_API_KEY in the environment.
Default model: gpt-4o. Override via DEFAULT_OPENAI_MODEL env var.

The KF gate logic (scan_signals, evaluate_transition_predicate,
_invoke_staged predicate wiring) is identical to llm.py — shared
via re-export from that module. Only the API call layer differs.
"""

from __future__ import annotations

import json
import os
import threading
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any

# ---------------------------------------------------------------------------
# Re-export KF gate functions from llm.py (provider-agnostic pure functions)
# ---------------------------------------------------------------------------
from .llm import (  # noqa: F401
    scan_signals,
    evaluate_transition_predicate,
    StagePredicateResult,
    ExecutionTrace,
    ToolCall,
    get_last_trace as _get_anthropic_trace,
)

DEFAULT_OPENAI_MODEL = os.environ.get("DEFAULT_OPENAI_MODEL", "gpt-4o")

_CONCURRENT_LIMIT = int(os.environ.get("HIERARCHY_CONCURRENT_CALLS", "2"))
_semaphore = threading.Semaphore(_CONCURRENT_LIMIT)
DEFAULT_MAX_ITERATIONS = 20

_last_trace: ExecutionTrace | None = None


def get_last_trace() -> ExecutionTrace | None:
    return _last_trace


def _ensure_api_key():
    if os.environ.get("OPENAI_API_KEY"):
        return
    # Walk up looking for .env
    from pathlib import Path
    search = Path(__file__).resolve().parent
    for _ in range(10):
        env_path = search / ".env"
        if env_path.exists():
            for line in env_path.read_text(encoding="utf-8").splitlines():
                line = line.strip()
                if line and not line.startswith("#") and "=" in line:
                    key, _, value = line.partition("=")
                    os.environ.setdefault(key.strip(), value.strip())
            return
        search = search.parent


def _convert_tools(tools: list[Any]) -> list[dict]:
    """Convert tool definitions to OpenAI function-calling format."""
    converted = []
    for tool in tools:
        if isinstance(tool, dict):
            converted.append({
                "type": "function",
                "function": {
                    "name": tool["name"],
                    "description": tool.get("description", ""),
                    "parameters": tool.get("input_schema", {
                        "type": "object", "properties": {},
                    }),
                },
            })
    return converted


def _execute_tool(name: str, inputs: dict, tools: list[Any]) -> str:
    for tool in tools:
        if isinstance(tool, dict) and tool["name"] == name:
            handler = tool.get("handler")
            if handler and callable(handler):
                try:
                    return handler(**inputs)
                except Exception as e:
                    return f"ERROR: Tool {name} failed: {e}"
    return f"ERROR: Tool {name} not found"


def _call_with_retry(client, *, model, messages, tools=None,
                     max_tokens=8192, max_retries=5):
    import time as _time
    import sys

    kwargs = dict(model=model, messages=messages, max_tokens=max_tokens)
    if tools:
        kwargs["tools"] = tools

    for attempt in range(max_retries):
        try:
            return client.chat.completions.create(**kwargs)
        except Exception as e:
            err = str(e).lower()
            if "rate_limit" in err or "429" in err or "rate limit" in err:
                retry_after = None
                if hasattr(e, "response") and hasattr(e.response, "headers"):
                    retry_after = e.response.headers.get("retry-after")
                    if retry_after:
                        try:
                            retry_after = float(retry_after)
                        except (ValueError, TypeError):
                            retry_after = None
                wait = retry_after if retry_after else min(2 ** attempt * 15, 120)
                print(f"  [RATE LIMIT] Attempt {attempt+1}/{max_retries}, "
                      f"waiting {wait:.0f}s...", file=sys.stderr)
                _time.sleep(wait)
            else:
                raise
    return client.chat.completions.create(**kwargs)


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------

def invoke_llm(
    system: str,
    user: str,
    model: str | None = None,
    tools: list[Any] | None = None,
    max_tokens: int = 8192,
    max_iterations: int | None = None,
) -> str:
    global _last_trace
    try:
        import openai as _openai
    except ImportError:
        raise RuntimeError("openai package not installed.")

    _ensure_api_key()
    model = model or DEFAULT_OPENAI_MODEL

    with _semaphore:
        if tools:
            iterations = max_iterations if max_iterations is not None else DEFAULT_MAX_ITERATIONS
            text, trace = _invoke_with_tools(system, user, model, tools, max_tokens, iterations)
            _last_trace = trace
            return text
        text, trace = _invoke_simple(system, user, model, max_tokens)
        _last_trace = trace
        return text


def invoke_llm_staged(
    system: str,
    user: str,
    stages: list[dict],
    model: str | None = None,
    max_tokens: int = 8192,
    hook_registry: Any = None,
) -> str:
    global _last_trace
    model = model or DEFAULT_OPENAI_MODEL

    with _semaphore:
        text, trace = _invoke_staged(system, user, model, stages, max_tokens, hook_registry)
        _last_trace = trace
        return text


# ---------------------------------------------------------------------------
# Internal
# ---------------------------------------------------------------------------

def _invoke_simple(system: str, user: str, model: str, max_tokens: int) -> tuple[str, ExecutionTrace]:
    try:
        import openai as _openai
    except ImportError:
        raise RuntimeError("openai package not installed.")

    _ensure_api_key()
    client = _openai.OpenAI()
    response = _call_with_retry(
        client, model=model, max_tokens=max_tokens,
        messages=[
            {"role": "system", "content": system},
            {"role": "user", "content": user},
        ],
    )

    usage = response.usage
    trace = ExecutionTrace(
        model=model,
        iterations=1,
        input_tokens=getattr(usage, "prompt_tokens", 0) if usage else 0,
        output_tokens=getattr(usage, "completion_tokens", 0) if usage else 0,
        total_tokens=getattr(usage, "total_tokens", 0) if usage else 0,
        stop_reason=response.choices[0].finish_reason or "",
        timestamp=datetime.now(timezone.utc).isoformat(),
    )

    return response.choices[0].message.content or "", trace


def _invoke_with_tools(
    system: str, user: str, model: str,
    tools: list[Any], max_tokens: int,
    max_iterations: int = 20,
) -> tuple[str, ExecutionTrace]:
    try:
        import openai as _openai
    except ImportError:
        raise RuntimeError("openai package not installed.")

    _ensure_api_key()
    client = _openai.OpenAI()
    oai_tools = _convert_tools(tools)

    messages: list[dict] = [
        {"role": "system", "content": system},
        {"role": "user", "content": user},
    ]
    all_text: list[str] = []
    trace = ExecutionTrace(model=model, timestamp=datetime.now(timezone.utc).isoformat())

    for iteration in range(max_iterations):
        response = _call_with_retry(
            client, model=model, max_tokens=max_tokens,
            messages=messages,
            tools=oai_tools if oai_tools else None,
        )
        choice = response.choices[0]
        msg = choice.message
        finish = choice.finish_reason

        usage = response.usage
        iter_in = getattr(usage, "prompt_tokens", 0) if usage else 0
        iter_out = getattr(usage, "completion_tokens", 0) if usage else 0
        trace.input_tokens += iter_in
        trace.output_tokens += iter_out
        trace.total_tokens += iter_in + iter_out
        trace.tokens_by_iteration.append({
            "iteration": iteration,
            "input_tokens": iter_in,
            "output_tokens": iter_out,
        })
        trace.iterations = iteration + 1
        trace.stop_reason = finish or ""

        # Collect text
        if msg.content:
            all_text.append(msg.content)

        tool_calls = msg.tool_calls or []

        # Add assistant message
        messages.append({"role": "assistant", "content": msg.content, "tool_calls": [
            {"id": tc.id, "type": "function",
             "function": {"name": tc.function.name, "arguments": tc.function.arguments}}
            for tc in tool_calls
        ] if tool_calls else None})

        if finish == "stop" or not tool_calls:
            break

        # Execute tools
        for tc in tool_calls:
            try:
                inputs = json.loads(tc.function.arguments)
            except json.JSONDecodeError:
                inputs = {}
            now = datetime.now(timezone.utc).isoformat()
            result = _execute_tool(tc.function.name, inputs, tools)
            success = not str(result).startswith("ERROR:")
            trace.tool_calls.append(ToolCall(
                iteration=iteration, name=tc.function.name,
                inputs=inputs, output=str(result)[:2000],
                success=success, timestamp=now,
            ))
            messages.append({
                "role": "tool",
                "tool_call_id": tc.id,
                "content": str(result),
            })

    return "\n".join(all_text), trace


def _invoke_staged(
    system: str, user: str, model: str,
    stages: list[dict], max_tokens: int,
    hook_registry: Any = None,
) -> tuple[str, ExecutionTrace]:
    """OpenAI staged tool loop — mirrors llm.py _invoke_staged with KF gate v3."""
    try:
        import openai as _openai
    except ImportError:
        raise RuntimeError("openai package not installed.")

    _ensure_api_key()
    client = _openai.OpenAI()

    messages: list[dict] = [
        {"role": "system", "content": system},
        {"role": "user", "content": user},
    ]
    all_text: list[str] = []
    global_iteration = 0
    all_tool_history: list[dict] = []

    trace = ExecutionTrace(model=model, timestamp=datetime.now(timezone.utc).isoformat())

    for stage_idx, stage in enumerate(stages):
        stage_name = stage.get("name", "?")
        stage_tools = stage.get("tools", [])
        stage_budget = stage.get("budget", 0)
        transition_msg = stage.get("transition_msg", "")
        stage_deliverables = stage.get("deliverables", [])
        stage_working_dir = stage.get("working_dir", ".")
        predicate_enabled = stage.get("predicate_enabled", True)
        current_sub_stage = stage_name

        if stage_budget <= 0:
            continue

        # --- Context windowing at stage boundaries ---
        if stage_idx > 0 and len(messages) > 5:
            prior_reasoning = []
            for msg in messages[2:]:  # Skip system + user
                if msg.get("role") == "assistant":
                    content = msg.get("content")
                    if isinstance(content, str) and content.strip():
                        prior_reasoning.append(content)

            summary = "\n\n".join(prior_reasoning[-3:])
            messages = [
                messages[0],  # system prompt
                messages[1],  # original user prompt
                {"role": "assistant", "content": f"[Prior stages completed. Key findings:]\n{summary[:4000]}"},
                {"role": "user", "content": "Continue with the next stage."},
            ]

        oai_tools = _convert_tools(stage_tools)

        if transition_msg:
            messages.append({"role": "user", "content": transition_msg})

        for stage_iter in range(stage_budget):
            response = _call_with_retry(
                client, model=model, max_tokens=max_tokens,
                messages=messages,
                tools=oai_tools if oai_tools else None,
            )
            choice = response.choices[0]
            msg = choice.message
            finish = choice.finish_reason

            usage = response.usage
            iter_in = getattr(usage, "prompt_tokens", 0) if usage else 0
            iter_out = getattr(usage, "completion_tokens", 0) if usage else 0
            trace.input_tokens += iter_in
            trace.output_tokens += iter_out
            trace.total_tokens += iter_in + iter_out
            trace.tokens_by_iteration.append({
                "iteration": global_iteration,
                "stage": stage_name,
                "input_tokens": iter_in,
                "output_tokens": iter_out,
            })
            global_iteration += 1
            trace.iterations = global_iteration
            trace.stop_reason = finish or ""

            if msg.content:
                all_text.append(msg.content)

            tool_calls = msg.tool_calls or []

            # Build assistant message
            messages.append({"role": "assistant", "content": msg.content, "tool_calls": [
                {"id": tc.id, "type": "function",
                 "function": {"name": tc.function.name, "arguments": tc.function.arguments}}
                for tc in tool_calls
            ] if tool_calls else None})

            # Scan text for KF signals
            iter_text = msg.content or ""
            signals = scan_signals(iter_text)

            # Track Pe→In sub-stage transition
            if (signals.get("transition") == ("Pe", "In")
                    and current_sub_stage == "Pe"
                    and stage_name == "Pe"):
                current_sub_stage = "In"

            if finish == "stop" or not tool_calls:
                # COMPLETE signal
                if signals.get("complete"):
                    break

                # ARCHETYPE_CONSTRAINT
                constraint = signals.get("constraint")
                if constraint:
                    messages.append({"role": "user", "content": (
                        f"Constraint noted. Required tool: {constraint['required']}. "
                        f"Request type: {constraint['request']}. Continue with available tools."
                    )})
                    continue

                # Predicate check
                if not predicate_enabled:
                    break

                from .llm import evaluate_transition_predicate
                pred = evaluate_transition_predicate(
                    from_stage=current_sub_stage,
                    tool_call_history=all_tool_history,
                    deliverable_paths=stage_deliverables,
                    working_dir=stage_working_dir,
                )
                if not pred.satisfied:
                    messages.append({"role": "user", "content": (
                        f"TRANSITION DENIED: {pred.reason}\n"
                        f"Continue in {current_sub_stage} stage."
                    )})
                    continue

                break

            # Execute tools
            for tc in tool_calls:
                try:
                    inputs = json.loads(tc.function.arguments)
                except json.JSONDecodeError:
                    inputs = {}
                now = datetime.now(timezone.utc).isoformat()
                result = _execute_tool(tc.function.name, inputs, stage_tools)
                success = not str(result).startswith("ERROR:")
                trace.tool_calls.append(ToolCall(
                    iteration=global_iteration - 1,
                    name=tc.function.name,
                    inputs=inputs, output=str(result)[:2000],
                    success=success, timestamp=now,
                ))
                all_tool_history.append({
                    "name": tc.function.name,
                    "stage": current_sub_stage,
                    "success": success,
                })
                messages.append({
                    "role": "tool",
                    "tool_call_id": tc.id,
                    "content": str(result),
                })

    return "\n".join(all_text), trace
