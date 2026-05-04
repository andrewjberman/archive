#!/usr/bin/env python3
"""
orchestrator.py -- Round-robin agent conversation driver (API-based)

Replaces orchestrator.sh. Uses OpenAI API directly so it can be invoked
from within a Claude Code session via the Bash tool -- no nested claude
CLI processes, no CLAUDECODE env var conflicts.

Usage:
    python org/threads/orchestrator.py --thread <id> [options]

Options:
    --thread <id>       Thread ID to run (required)
    --model <model>     OpenAI model (default: gpt-4o-mini)
    --dry-run           Show what would be invoked without calling API
    --verbose           Print agent responses to stdout as they arrive
    --secret <name>     AWS Secrets Manager secret name (default: openai-api-key)
"""

from __future__ import annotations

import argparse
import io
import json
import os
import re
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import List, Dict, Any, Union

# Force UTF-8 stdout on Windows (persona prompts contain emoji from legacy files)
if sys.stdout.encoding and sys.stdout.encoding.lower() != "utf-8":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

import boto3
from openai import OpenAI

# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------

SCRIPT_DIR = Path(__file__).parent.resolve()
REPO_ROOT = SCRIPT_DIR.parent.parent.resolve()
ORG_DIR = REPO_ROOT / "org"

ROLE_TO_PROMPT = {
    "SA": "systems_architect.md",
    "DE": "dashboard_engineer.md",
    "DT": "devops_technician.md",
    "DS": "data_scientist.md",
    "AE": "aws_engineer.md",
    "RD": "react_designer.md",
}

ROLE_NAMES = {
    "SA": "Systems Architect",
    "DE": "Dashboard Engineer",
    "DT": "DevOps Technician",
    "DS": "Data Scientist",
    "AE": "AWS Engineer",
    "RD": "React Designer",
}

# ---------------------------------------------------------------------------
# Agent resolution
# ---------------------------------------------------------------------------

def resolve_agent(serial: str) -> dict:
    """Map a serial number to its folder paths and role metadata."""
    parts = serial.split(".")
    x = parts[0]
    y = parts[1]
    role_code = parts[2].split("_")[1] if "_" in parts[2] else parts[2]

    z = parts[2].split("_")[0]  # numeric z component before role suffix
    if x != "0":
        tier_folder = "tier1_exec"
    elif z != "0":
        tier_folder = "tier3_junior"
    elif y != "0":
        tier_folder = "tier2_senior"
    else:
        tier_folder = "tier3_junior"

    agent_dir = ORG_DIR / tier_folder / serial

    return {
        "serial": serial,
        "role_code": role_code,
        "role_name": ROLE_NAMES.get(role_code, role_code),
        "agent_dir": agent_dir,
        "prompt_file": agent_dir / "prompt.md",
        "base_prompt_file": ORG_DIR / "ref" / "prompts" / ROLE_TO_PROMPT.get(role_code, ""),
    }

# ---------------------------------------------------------------------------
# Prompt construction
# ---------------------------------------------------------------------------

def build_system_prompt(serial: str) -> str:
    agent = resolve_agent(serial)
    parts = []
    if agent["base_prompt_file"].exists():
        parts.append(agent["base_prompt_file"].read_text(encoding="utf-8"))
    if agent["prompt_file"].exists():
        parts.append(agent["prompt_file"].read_text(encoding="utf-8"))
    return "\n\n".join(parts)


def build_user_prompt(
    thread_dir: Path,
    serial: str,
    turn_number: int,
    now_utc: Union[datetime, None] = None,
) -> List[Dict[str, Any]]:
    """
    Build the user message as a list of content blocks for prompt-caching.

    Returns a list of two content blocks:
      [0] STATIC PREFIX -- identity, instructions, CONTEXT_COMPILED.md, PREVIOUS
          MESSAGES. Marked with cache_control={"type":"ephemeral"} so the
          Anthropic OpenAI-compatible shim caches the prefix. Stable across
          calls for the same (thread, serial, message-history) tuple.
      [1] VARIABLE FOOTER -- turn N / max M / remaining R / timestamp /
          last-turn flag. No cache_control. Wall-clock + per-call counters
          live here so they don't break the prefix hash.

    The `now_utc` param is injected (default: real wall-clock) to make the
    function deterministic in tests.
    """
    thread_json = json.loads((thread_dir / "THREAD.json").read_text())
    turn_json   = json.loads((thread_dir / "TURN.json").read_text())

    topic        = thread_json["topic"]
    max_per      = thread_json["max_turns_per_agent"]
    num_p        = len(thread_json["participants"])
    max_total    = max_per * num_p
    taken        = turn_json["turns_taken"].get(serial, 0)
    remaining    = max_per - taken
    role_name    = resolve_agent(serial)["role_name"]
    ts_dt        = now_utc if now_utc is not None else datetime.now(timezone.utc)
    ts           = ts_dt.strftime("%Y-%m-%dT%H:%M:%SZ")

    # ---- STATIC PREFIX -------------------------------------------------------
    # Everything in this block is a deterministic function of (thread_dir,
    # serial, set-of-message-files-on-disk). NOT a function of turn_number,
    # remaining count, or wall-clock. The prefix's byte-for-byte stability is
    # what enables Anthropic prompt caching to hit on subsequent turns.
    static_lines = [
        "## YOUR TURN -- Thread Protocol",
        "",
        "You are participating in a structured agent conversation thread.",
        "",
        f"**Your identity:** {serial} ({role_name})",
        f"**Thread topic:** {topic}",
        "",
        "### Instructions",
        "",
        "1. Read the CONTEXT section below -- this is your shared briefing material.",
        "2. Read all previous messages in order.",
        "3. Write your response using the required format below.",
        "4. Your entire response will be saved verbatim as the next message file.",
        "5. Set your signal:",
        "   - `continue` -- you have more to discuss or questions remain",
        "   - `converge` -- you believe the conversation has reached resolution",
        "   - `escalate` -- you need human input (explain why in your message body)",
        "",
        "### Required Response Format",
        "",
        "Your response MUST begin with this exact YAML frontmatter block",
        "(replace `continue` with your actual signal, and use the turn number,",
        "agent serial, and timestamp from the YOUR TURN STATE footer at the end",
        "of this prompt):",
        "",
        "```",
        "---",
        "agent: <your serial from footer>",
        "turn: <turn number from footer>",
        "timestamp: <timestamp from footer>",
        "signal: continue",
        "---",
        "```",
        "",
        "Everything after the closing `---` is your message body.",
        "",
        "### Source Priority",
        "",
        "The pre-injected context (session logs, recent commits, deployment tags, task",
        "orders, reference documents) is your primary source of truth. It is factual,",
        "specific, and costs nothing to use. Read it carefully before responding.",
        "",
        "Use file-reading tools ONLY for specific gaps -- an exact value in Terraform,",
        "a precise S3 key pattern in Lambda source code -- that the pre-injected context",
        "does not contain. Do not call tools to re-read information already in context.",
        "If pre-injected context is sufficient, answer directly without any tool calls.",
        "",
        "### Constraints",
        "- Stay in your role. Do not impersonate other agents.",
        "- Be concrete. Name files, functions, S3 paths, resource names, git tags.",
        "- Do not include anything before the opening `---`.",
        "- If the YOUR TURN STATE footer indicates this is your last turn, your",
        "  signal MUST be `converge`.",
    ]

    static_lines += ["", "---", "", "## CONTEXT", ""]

    context_file = thread_dir / "CONTEXT_COMPILED.md"
    if context_file.exists():
        static_lines.append(context_file.read_text(encoding="utf-8"))

    static_lines += ["", "---", "", "## PREVIOUS MESSAGES", ""]

    msg_files = sorted((thread_dir / "messages").glob("*.md"))
    if not msg_files:
        static_lines.append("(No previous messages)")
    else:
        for mf in msg_files:
            static_lines += [f"### Message: {mf.name}", "", mf.read_text(encoding="utf-8"), ""]

    static_text = "\n".join(static_lines)

    # ---- VARIABLE FOOTER -----------------------------------------------------
    # Everything that changes per call goes here. By placing this AFTER the
    # static prefix (and not marking it with cache_control), the cache lookup
    # hashes only the prefix -- this footer is appended on top of a cache hit.
    footer_lines = [
        "",
        "---",
        "",
        "## YOUR TURN STATE",
        "",
        f"- agent: {serial}",
        f"- turn: {turn_number} of max {max_total}",
        f"- turns remaining for you: {remaining}",
        f"- timestamp: {ts}",
    ]
    if remaining <= 1:
        footer_lines.append("- **THIS IS YOUR LAST TURN. Your signal MUST be `converge`.**")

    footer_text = "\n".join(footer_lines)

    return [
        {
            "type": "text",
            "text": static_text,
            "cache_control": {"type": "ephemeral"},
        },
        {
            "type": "text",
            "text": footer_text,
        },
    ]

# ---------------------------------------------------------------------------
# Signal parsing
# ---------------------------------------------------------------------------

def parse_signal(msg_file: Path) -> str:
    content = msg_file.read_text(encoding="utf-8")
    match = re.search(r"^signal:\s*(\w+)", content, re.MULTILINE)
    return match.group(1).strip() if match else "continue"

# ---------------------------------------------------------------------------
# State checks
# ---------------------------------------------------------------------------

def check_convergence(thread_dir: Path) -> bool:
    files = sorted((thread_dir / "messages").glob("*.md"))
    if len(files) < 2:
        return False
    return parse_signal(files[-1]) == "converge" and parse_signal(files[-2]) == "converge"


def check_max_turns(thread_dir: Path) -> bool:
    thread_json = json.loads((thread_dir / "THREAD.json").read_text())
    turn_json   = json.loads((thread_dir / "TURN.json").read_text())
    max_t = thread_json["max_turns_per_agent"]
    return all(
        turn_json["turns_taken"].get(s, 0) >= max_t
        for s in thread_json["participants"]
    )


def compute_next_after(thread_dir: Path, current: str) -> str:
    participants = json.loads((thread_dir / "THREAD.json").read_text())["participants"]
    idx = participants.index(current)
    return participants[(idx + 1) % len(participants)]

# ---------------------------------------------------------------------------
# State mutations
# ---------------------------------------------------------------------------

def advance_turn(thread_dir: Path, current: str, next_agent: str):
    turn_file = thread_dir / "TURN.json"
    turn_json = json.loads(turn_file.read_text())
    turn_json["turn_number"] += 1
    turn_json["next_agent"] = next_agent
    turn_json["turns_taken"][current] = turn_json["turns_taken"].get(current, 0) + 1
    turn_json["last_updated"] = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    turn_file.write_text(json.dumps(turn_json, indent=2), encoding="utf-8")


def set_status(thread_dir: Path, status: str):
    for fname in ("THREAD.json", "TURN.json"):
        f = thread_dir / fname
        data = json.loads(f.read_text())
        data["status"] = status
        f.write_text(json.dumps(data, indent=2), encoding="utf-8")

# ---------------------------------------------------------------------------
# Receipts
# ---------------------------------------------------------------------------

def write_receipts(thread_dir: Path):
    thread_json = json.loads((thread_dir / "THREAD.json").read_text())
    thread_id    = thread_json["id"]
    topic        = thread_json["topic"]
    participants = thread_json["participants"]
    serial_no    = thread_json.get("serial", "")

    msg_files = sorted((thread_dir / "messages").glob("*.md"))
    header_lines = [
        f"# Thread Receipt: {topic}",
        "",
        f"**Thread ID:** {thread_id}",
    ]
    if serial_no:
        header_lines.append(f"**Project Serial:** {serial_no}")
    header_lines += [
        f"**Created by:** {thread_json['created_by']}",
        f"**Created at:** {thread_json['created_at']}",
        f"**Status:** {thread_json['status']}",
        f"**Participants:** {', '.join(participants)}",
        "",
        "---",
        "",
    ]
    header = "\n".join(header_lines)
    body_parts = []
    for mf in msg_files:
        body_parts.append(f"## {mf.name}\n\n{mf.read_text(encoding='utf-8')}\n\n---\n")
    receipt = header + "\n".join(body_parts)

    for serial in participants:
        agent  = resolve_agent(serial)
        others = "+".join(s for s in participants if s != serial)
        # Receipt filename uses full thread_id so project threads sort by code+serial
        dest   = agent["agent_dir"] / "threads" / f"{thread_id}_{others}.md"
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_text(receipt, encoding="utf-8")
        print(f"OK: Receipt -> {dest}")

# ---------------------------------------------------------------------------
# Tool definitions
# ---------------------------------------------------------------------------

TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "read_file",
            "description": (
                "Read the full contents of a file. Path must be relative to the "
                "repository root. Use this to read Lambda source, Terraform files, "
                "endpoint definitions, or any other file in the codebase."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "path": {
                        "type": "string",
                        "description": "File path relative to repo root, e.g. 'infra/aws/terraform/bd-pipeline/eventbridge.tf'",
                    }
                },
                "required": ["path"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "glob_files",
            "description": (
                "Find files matching a glob pattern relative to the repository root. "
                "Use this to discover what files exist in a directory before reading them."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "pattern": {
                        "type": "string",
                        "description": "Glob pattern relative to repo root, e.g. 'infra/aws/terraform/bd-pipeline/*.tf'",
                    }
                },
                "required": ["pattern"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "grep_content",
            "description": (
                "Search for a pattern in a file or directory. Returns matching lines "
                "with file path and line number. Use this to find a specific resource "
                "name, function, or variable across a codebase path."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "pattern": {
                        "type": "string",
                        "description": "String or regex to search for (case-insensitive)",
                    },
                    "path": {
                        "type": "string",
                        "description": "File or directory path relative to repo root",
                    },
                },
                "required": ["pattern", "path"],
            },
        },
    },
]

MAX_TOOL_CALLS_PER_TURN = 5
FILE_SIZE_LIMIT = 50_000  # chars; truncate beyond this


def execute_tool(name: str, args: dict, verbose: bool = False) -> str:
    """Execute a tool call and return the result as a string."""

    def safe_path(raw: str):
        """Resolve and validate a path is within REPO_ROOT."""
        p = (REPO_ROOT / raw).resolve()
        try:
            p.relative_to(REPO_ROOT)
        except ValueError:
            raise PermissionError(f"Path outside repository root: {raw}")
        return p

    if name == "read_file":
        try:
            p = safe_path(args["path"])
        except PermissionError as e:
            return f"ERROR: {e}"
        if not p.exists():
            return f"ERROR: File not found: {args['path']}"
        if not p.is_file():
            return f"ERROR: Not a file: {args['path']}"
        try:
            content = p.read_text(encoding="utf-8", errors="replace")
            if len(content) > FILE_SIZE_LIMIT:
                content = (
                    content[:FILE_SIZE_LIMIT]
                    + f"\n\n[TRUNCATED — file is {len(content):,} chars, showing first {FILE_SIZE_LIMIT:,}]"
                )
            return content
        except Exception as exc:
            return f"ERROR: Could not read file: {exc}"

    elif name == "glob_files":
        try:
            matches = sorted(REPO_ROOT.glob(args["pattern"]))
            files = [
                str(m.relative_to(REPO_ROOT)).replace("\\", "/")
                for m in matches
                if m.is_file()
            ]
            if not files:
                return f"No files found matching: {args['pattern']}"
            return "\n".join(files)
        except Exception as exc:
            return f"ERROR: {exc}"

    elif name == "grep_content":
        try:
            p = safe_path(args["path"])
        except PermissionError as e:
            return f"ERROR: {e}"
        if not p.exists():
            return f"ERROR: Path not found: {args['path']}"

        try:
            pattern = re.compile(args["pattern"], re.IGNORECASE)
        except re.error as exc:
            return f"ERROR: Invalid regex '{args['pattern']}': {exc}"

        files = [p] if p.is_file() else sorted(f for f in p.rglob("*") if f.is_file())[:50]
        results = []
        for f in files:
            try:
                for i, line in enumerate(
                    f.read_text(encoding="utf-8", errors="replace").splitlines(), 1
                ):
                    if pattern.search(line):
                        rel = str(f.relative_to(REPO_ROOT)).replace("\\", "/")
                        results.append(f"{rel}:{i}: {line.rstrip()}")
                        if len(results) >= 100:
                            break
            except Exception:
                continue
            if len(results) >= 100:
                break

        if not results:
            return f"No matches for '{args['pattern']}' in {args['path']}"
        if len(results) == 100:
            results.append("[TRUNCATED — showing first 100 matches]")
        return "\n".join(results)

    else:
        return f"ERROR: Unknown tool '{name}'"


# ---------------------------------------------------------------------------
# OpenAI client
# ---------------------------------------------------------------------------

def get_openai_client(secret_name: str, model: str = "") -> OpenAI:
    # Anthropic path: claude-* models use Anthropic's OpenAI-compatible endpoint
    is_anthropic = model.startswith("claude-")
    env_key = "ANTHROPIC_API_KEY" if is_anthropic else "OPENAI_API_KEY"
    api_key = os.environ.get(env_key) or os.environ.get("OPENAI_API_KEY")
    if not api_key:
        sm = boto3.client("secretsmanager", region_name="us-east-1")
        raw = sm.get_secret_value(SecretId=secret_name)["SecretString"]
        # Handle both raw-string and JSON-wrapped secrets
        try:
            parsed = json.loads(raw)
            api_key = (
                parsed.get("api_key")
                or parsed.get("ANTHROPIC_API_KEY")
                or parsed.get("anthropic_api_key")
                or parsed.get("OPENAI_API_KEY")
                or parsed.get("openai_api_key")
                or raw
            )
        except (json.JSONDecodeError, AttributeError):
            api_key = raw
    if is_anthropic:
        return OpenAI(api_key=api_key, base_url="https://api.anthropic.com/v1")
    return OpenAI(api_key=api_key)

# ---------------------------------------------------------------------------
# Usage telemetry — surfaces prompt-cache hit rate per API call
# ---------------------------------------------------------------------------

def format_usage(usage) -> str:
    """One-line usage line for stdout. Handles OpenAI native and Anthropic
    OpenAI-compat shapes. Anthropic exposes cache READS via
    prompt_tokens_details.cached_tokens; cache CREATION tokens are not always
    in the standard usage object — pulled from model_extra when present."""
    if usage is None:
        return "  [usage] none"
    inp = getattr(usage, "prompt_tokens", 0) or 0
    out = getattr(usage, "completion_tokens", 0) or 0
    cache_read = 0
    cache_create = 0
    details = getattr(usage, "prompt_tokens_details", None)
    if details is not None:
        cache_read = getattr(details, "cached_tokens", 0) or 0
    extra = getattr(usage, "model_extra", None) or {}
    if not cache_read:
        cache_read = extra.get("cache_read_input_tokens", 0) or 0
    cache_create = (
        getattr(usage, "cache_creation_input_tokens", 0)
        or extra.get("cache_creation_input_tokens", 0)
        or 0
    )
    total_input = inp + cache_read + cache_create
    hit_pct = (cache_read / total_input * 100) if total_input else 0.0
    return (
        f"  [usage] input={inp:,} (cache_read={cache_read:,} = {hit_pct:.0f}%, "
        f"cache_create={cache_create:,}) output={out:,}"
    )


# ---------------------------------------------------------------------------
# Tool-aware API call
# ---------------------------------------------------------------------------

def call_with_tools(
    client: OpenAI,
    model: str,
    system_prompt: str,
    user_prompt: Union[str, List[Dict[str, Any]]],
    use_tools: bool = True,
    verbose: bool = False,
) -> str:
    """
    Call the OpenAI API with an optional tool-use loop.

    If use_tools is True, the model may call read_file / glob_files /
    grep_content to inspect the codebase before producing its final response.
    The loop runs until the model stops issuing tool calls or the per-turn
    safety limit is reached.

    `user_prompt` may be either a plain string (legacy) or a list of content
    blocks (preferred -- enables Anthropic prompt caching when blocks carry
    cache_control). The system prompt is wrapped in a single text block with
    cache_control={"type":"ephemeral"} so the per-agent system prompt is
    cached across turns. OpenAI ignores cache_control fields harmlessly and
    applies its own automatic prefix caching server-side.

    Returns the final message content as a string.
    """
    # Wrap system prompt in a content array with a cache breakpoint. Even
    # though OpenAI doesn't use the cache_control hint, it accepts the array
    # form, so this keeps the message shape uniform across providers.
    system_blocks = [
        {
            "type": "text",
            "text": system_prompt,
            "cache_control": {"type": "ephemeral"},
        }
    ]
    # Accept either a string (back-compat) or a pre-built list of blocks.
    if isinstance(user_prompt, str):
        user_content: Union[str, List[Dict[str, Any]]] = user_prompt
    else:
        user_content = user_prompt

    messages = [
        {"role": "system", "content": system_blocks},
        {"role": "user",   "content": user_content},
    ]
    tools_used = 0

    while True:
        kwargs = {"model": model, "messages": messages, "temperature": 0.3}
        if use_tools:
            kwargs["tools"] = TOOLS
            kwargs["tool_choice"] = "auto"

        try:
            response = client.chat.completions.create(**kwargs)
        except Exception as e:
            # Newer models (claude-opus-4-7 deprecated; gpt-5.5 only-supports-default)
            # reject the temperature parameter. Fall back to no-temperature rather
            # than fail the thread.
            if "temperature" in str(e):
                kwargs.pop("temperature", None)
                response = client.chat.completions.create(**kwargs)
            else:
                raise
        print(format_usage(getattr(response, "usage", None)))
        msg = response.choices[0].message

        # No tool calls — model is done
        if not msg.tool_calls:
            return msg.content or ""

        # Safety limit: force a final answer without tools
        if tools_used >= MAX_TOOL_CALLS_PER_TURN:
            print(f"  WARN: tool call limit ({MAX_TOOL_CALLS_PER_TURN}) reached, forcing finish")
            messages.append({"role": "assistant", "content": msg.content or "", "tool_calls": []})
            messages.append({
                "role": "user",
                "content": (
                    "You have reached the tool call limit for this turn. "
                    "Write your final response now using only what you have already read."
                ),
            })
            try:
                final = client.chat.completions.create(
                    model=model, messages=messages, temperature=0.3
                )
            except Exception as e:
                if "temperature" in str(e):
                    final = client.chat.completions.create(
                        model=model, messages=messages
                    )
                else:
                    raise
            print(format_usage(getattr(final, "usage", None)))
            return final.choices[0].message.content or ""

        # Append the assistant message that contains tool calls
        messages.append({
            "role": "assistant",
            "content": msg.content,
            "tool_calls": [
                {
                    "id": tc.id,
                    "type": "function",
                    "function": {"name": tc.function.name, "arguments": tc.function.arguments},
                }
                for tc in msg.tool_calls
            ],
        })

        # Execute each tool call and append results
        for tc in msg.tool_calls:
            name = tc.function.name
            args = json.loads(tc.function.arguments)
            if verbose:
                print(f"  [tool] {name}({args})")
            result = execute_tool(name, args, verbose=verbose)
            tools_used += 1
            messages.append({
                "role": "tool",
                "tool_call_id": tc.id,
                "content": result,
            })


# ---------------------------------------------------------------------------
# Main run loop
# ---------------------------------------------------------------------------

def run_thread(thread_dir: Path, clients: dict, model: str, participant_models: dict, dry_run: bool, verbose: bool, no_tools: bool = False):
    thread_json = json.loads((thread_dir / "THREAD.json").read_text())
    thread_id   = thread_json["id"]

    if thread_json.get("status") != "active":
        print(f"SKIP: Thread '{thread_id}' is not active (status: {thread_json['status']})")
        return

    print(f"\n{'=' * 40}")
    print(f"THREAD: {thread_id}")
    print(f"{'=' * 40}\n")

    while True:
        turn_json = json.loads((thread_dir / "TURN.json").read_text())

        if turn_json.get("status") != "active":
            print(f"HALT: Turn status is '{turn_json['status']}'")
            break

        if check_max_turns(thread_dir):
            print("COMPLETE: All agents have exhausted their max turns")
            set_status(thread_dir, "complete")
            write_receipts(thread_dir)
            break

        if check_convergence(thread_dir):
            print("COMPLETE: Consecutive converge signals detected")
            set_status(thread_dir, "complete")
            write_receipts(thread_dir)
            break

        current  = turn_json["next_agent"]
        turn_num = turn_json["turn_number"]
        msg_file = thread_dir / "messages" / f"{turn_num:03d}.md"

        thread_json = json.loads((thread_dir / "THREAD.json").read_text())
        max_per = thread_json["max_turns_per_agent"]
        taken   = turn_json["turns_taken"].get(current, 0)

        if taken >= max_per:
            print(f"SKIP: {current} exhausted turns ({taken}/{max_per})")
            nxt = compute_next_after(thread_dir, current)
            turn_json["next_agent"] = nxt
            (thread_dir / "TURN.json").write_text(json.dumps(turn_json, indent=2))
            continue

        print(f"TURN {turn_num}: {current}")

        # Resolve per-agent model: participant_models override > thread-level participant_models > default model
        thread_pm = thread_json.get("participant_models", {})
        agent_model = participant_models.get(current) or thread_pm.get(current) or model
        # Route to the right client based on provider
        if agent_model.startswith("claude-"):
            agent_client = clients.get("anthropic")
        else:
            agent_client = clients.get("openai")
        if agent_client is None and not dry_run:
            print(f"ERROR: No API client available for model '{agent_model}' (agent {current})")
            set_status(thread_dir, "blocked")
            break

        system_prompt = build_system_prompt(current)
        user_blocks   = build_user_prompt(thread_dir, current, turn_num)

        if dry_run:
            user_total_chars = sum(len(b["text"]) for b in user_blocks)
            print(f"  DRY RUN -- model: {agent_model} (agent: {current})")
            print(f"  System prompt: {len(system_prompt):,} chars (1 block, cache_control=ephemeral)")
            print(f"  User prompt:   {user_total_chars:,} chars across {len(user_blocks)} block(s)")
            for i, b in enumerate(user_blocks):
                cc = b.get("cache_control")
                cc_str = f"cache_control={cc}" if cc else "no cache_control"
                print(f"    block[{i}]: {len(b['text']):,} chars; {cc_str}")
            print(f"  Output:        {msg_file}")
            if verbose:
                print(f"\n--- SYSTEM (first 500) ---\n{system_prompt[:500]}")
                if user_blocks:
                    print(f"\n--- USER block[0] (first 1000) ---\n{user_blocks[0]['text'][:1000]}")
                if len(user_blocks) > 1:
                    print(f"\n--- USER block[{len(user_blocks)-1}] (full footer) ---\n{user_blocks[-1]['text']}")
            break

        try:
            content = call_with_tools(
                agent_client, agent_model, system_prompt, user_blocks,
                use_tools=(not no_tools), verbose=verbose,
            )
        except Exception as exc:
            print(f"ERROR: API call failed for {current} (model={agent_model}): {exc}")
            set_status(thread_dir, "blocked")
            break

        if verbose:
            print(f"\n--- {current} ---\n{content}\n--- end ---\n")

        msg_file.write_text(content, encoding="utf-8")

        signal = parse_signal(msg_file)
        print(f"  Signal: {signal}")

        if signal == "escalate":
            print(f"ESCALATE: {current} requests human input")
            set_status(thread_dir, "needs_human")
            break

        nxt = compute_next_after(thread_dir, current)
        advance_turn(thread_dir, current, nxt)
        print(f"  Next: {nxt} (turn {turn_num + 1})\n")

# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(description="Run an agent thread via OpenAI API")
    parser.add_argument("--thread",   required=True,          help="Thread ID to run")
    parser.add_argument("--model",    default="gpt-5.2",       help="Default model for all agents (default: gpt-5.2)")
    parser.add_argument("--dry-run",   action="store_true",    help="Show invocation without calling API")
    parser.add_argument("--dry-run-build", default="",         help="Build prompts for the named agent serial and emit JSON-serialized block structure to stdout. Bypasses active-status check. For inspecting cache_control placement in any thread state.")
    parser.add_argument("--verbose",   action="store_true",    help="Print agent responses and tool calls to stdout")
    parser.add_argument("--no-tools",  action="store_true",    help="Disable tool use (faster/cheaper; agents cannot read files)")
    parser.add_argument("--secret",    default="openai-api-key", help="AWS Secrets Manager secret name (default/OpenAI)")
    parser.add_argument("--anthropic-secret", default="anthropic-api-key", help="AWS Secrets Manager secret name for Anthropic API key")
    parser.add_argument("--openai-secret",    default="openai-api-key",    help="AWS Secrets Manager secret name for OpenAI API key")
    parser.add_argument(
        "--participant-models",
        default="",
        help=(
            'JSON map of agent serial to model string, e.g. '
            '\'{"1.1.0_SA_CTO":"claude-opus-4-7","3.1.0_SA_CVO":"gpt-5.5","2.1.0_SA_COO":"claude-sonnet-4-6"}\'. '
            'Overrides --model for named agents. Persisted to THREAD.json participant_models.'
        ),
    )
    args = parser.parse_args()

    thread_dir = SCRIPT_DIR / args.thread
    if not thread_dir.exists() or not (thread_dir / "THREAD.json").exists():
        print(f"ERROR: Thread not found: {thread_dir}")
        sys.exit(1)

    # Parse participant-models override
    participant_models: dict = {}
    if args.participant_models:
        try:
            participant_models = json.loads(args.participant_models)
        except json.JSONDecodeError as exc:
            print(f"ERROR: --participant-models is not valid JSON: {exc}")
            sys.exit(1)

    # Persist participant_models into THREAD.json if provided
    if participant_models:
        thread_json = json.loads((thread_dir / "THREAD.json").read_text())
        thread_json["participant_models"] = participant_models
        (thread_dir / "THREAD.json").write_text(json.dumps(thread_json, indent=2))
        print(f"OK: Persisted participant_models to THREAD.json: {participant_models}")

    # --dry-run-build: print prompt block structure for one agent and exit.
    # Useful for verifying cache_control placement on threads in any status
    # (including 'complete') without burning tokens or running the loop.
    if args.dry_run_build:
        target = args.dry_run_build
        turn_json = json.loads((thread_dir / "TURN.json").read_text())
        # Use the recorded turn_number if the thread is mid-flight; otherwise
        # synthesize a representative turn (the next one this agent would take).
        turn_number = turn_json.get("turn_number", 1)
        system_prompt = build_system_prompt(target)
        # Pin the timestamp to a fixed value so two back-to-back invocations
        # produce byte-identical static prefixes (the determinism check).
        fixed_ts = datetime(2026, 1, 1, 0, 0, 0, tzinfo=timezone.utc)
        user_blocks = build_user_prompt(thread_dir, target, turn_number, now_utc=fixed_ts)
        out = {
            "thread_id": args.thread,
            "agent": target,
            "turn_number": turn_number,
            "system": [
                {
                    "type": "text",
                    "text_len": len(system_prompt),
                    "text_head": system_prompt[:200],
                    "cache_control": {"type": "ephemeral"},
                }
            ],
            "user": [
                {
                    "type": b["type"],
                    "text_len": len(b["text"]),
                    "text_head": b["text"][:200],
                    "text_tail": b["text"][-200:],
                    "cache_control": b.get("cache_control"),
                }
                for b in user_blocks
            ],
        }
        print(json.dumps(out, indent=2))
        # Determinism sanity check: rebuild and compare prefix bytes.
        user_blocks_2 = build_user_prompt(thread_dir, target, turn_number, now_utc=fixed_ts)
        prefix_match = user_blocks[0]["text"] == user_blocks_2[0]["text"]
        print(f"\n# DETERMINISM: static-prefix byte-equal across two builds = {prefix_match}")
        # Also confirm wall-clock variation does not affect the prefix.
        later_ts = datetime(2099, 12, 31, 23, 59, 59, tzinfo=timezone.utc)
        user_blocks_3 = build_user_prompt(thread_dir, target, turn_number, now_utc=later_ts)
        prefix_independent_of_clock = user_blocks[0]["text"] == user_blocks_3[0]["text"]
        footer_changed_with_clock   = user_blocks[1]["text"] != user_blocks_3[1]["text"]
        print(f"# DETERMINISM: static-prefix is wall-clock-independent      = {prefix_independent_of_clock}")
        print(f"# DETERMINISM: footer DOES vary with wall-clock             = {footer_changed_with_clock}")
        return

    # Collect all models needed (default + per-agent overrides)
    all_models = list(participant_models.values()) + [args.model]
    needs_anthropic = any(m.startswith("claude-") for m in all_models)
    needs_openai    = any(not m.startswith("claude-") for m in all_models)

    clients: dict = {}

    if args.dry_run:
        pass  # No clients needed for dry run
    else:
        if needs_anthropic:
            secret = args.anthropic_secret
            print(f"Fetching Anthropic key ({secret})...")
            try:
                clients["anthropic"] = get_openai_client(secret, model="claude-sonnet-4-6")
                print("OK: Anthropic client ready")
            except Exception as exc:
                print(f"ERROR: Anthropic client failed: {exc}")
                sys.exit(1)
        if needs_openai:
            secret = args.openai_secret or args.secret
            print(f"Fetching OpenAI key ({secret})...")
            try:
                clients["openai"] = get_openai_client(secret, model="gpt-4o")
                print("OK: OpenAI client ready")
            except Exception as exc:
                print(f"ERROR: OpenAI client failed: {exc}")
                sys.exit(1)
        print()

    run_thread(thread_dir, clients, args.model, participant_models, args.dry_run, args.verbose, args.no_tools)
    print("\nOrchestrator complete.")


if __name__ == "__main__":
    main()
