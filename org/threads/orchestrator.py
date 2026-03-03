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

import argparse
import io
import json
import os
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

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


def build_user_prompt(thread_dir: Path, serial: str, turn_number: int) -> str:
    thread_json = json.loads((thread_dir / "THREAD.json").read_text())
    turn_json   = json.loads((thread_dir / "TURN.json").read_text())

    topic        = thread_json["topic"]
    max_per      = thread_json["max_turns_per_agent"]
    num_p        = len(thread_json["participants"])
    max_total    = max_per * num_p
    taken        = turn_json["turns_taken"].get(serial, 0)
    remaining    = max_per - taken
    role_name    = resolve_agent(serial)["role_name"]
    ts           = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

    lines = [
        "## YOUR TURN -- Thread Protocol",
        "",
        "You are participating in a structured agent conversation thread.",
        "",
        f"**Your identity:** {serial} ({role_name})",
        f"**Thread topic:** {topic}",
        f"**Turn:** {turn_number} of max {max_total}",
        f"**Your turns remaining:** {remaining}",
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
        "(replace `continue` with your actual signal):",
        "",
        "```",
        "---",
        f"agent: {serial}",
        f"turn: {turn_number}",
        f"timestamp: {ts}",
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
        "Use file-reading tools ONLY for specific gaps — an exact value in Terraform,",
        "a precise S3 key pattern in Lambda source code — that the pre-injected context",
        "does not contain. Do not call tools to re-read information already in context.",
        "If pre-injected context is sufficient, answer directly without any tool calls.",
        "",
        "### Constraints",
        "- Stay in your role. Do not impersonate other agents.",
        "- Be concrete. Name files, functions, S3 paths, resource names, git tags.",
        "- Do not include anything before the opening `---`.",
    ]

    if remaining <= 1:
        lines.append("- **THIS IS YOUR LAST TURN. Your signal MUST be `converge`.**")

    lines += ["", "---", "", "## CONTEXT", ""]

    context_file = thread_dir / "CONTEXT_COMPILED.md"
    if context_file.exists():
        lines.append(context_file.read_text(encoding="utf-8"))

    lines += ["", "---", "", "## PREVIOUS MESSAGES", ""]

    msg_files = sorted((thread_dir / "messages").glob("*.md"))
    if not msg_files:
        lines.append("(No previous messages)")
    else:
        for mf in msg_files:
            lines += [f"### Message: {mf.name}", "", mf.read_text(encoding="utf-8"), ""]

    return "\n".join(lines)

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
    thread_id   = thread_json["id"]
    topic       = thread_json["topic"]
    participants = thread_json["participants"]
    date_prefix = thread_id[:10]
    slug        = thread_id[11:]

    msg_files = sorted((thread_dir / "messages").glob("*.md"))
    header = "\n".join([
        f"# Thread Receipt: {topic}",
        "",
        f"**Thread ID:** {thread_id}",
        f"**Created by:** {thread_json['created_by']}",
        f"**Created at:** {thread_json['created_at']}",
        f"**Status:** {thread_json['status']}",
        f"**Participants:** {', '.join(participants)}",
        "",
        "---",
        "",
    ])
    body_parts = []
    for mf in msg_files:
        body_parts.append(f"## {mf.name}\n\n{mf.read_text(encoding='utf-8')}\n\n---\n")
    receipt = header + "\n".join(body_parts)

    for serial in participants:
        agent  = resolve_agent(serial)
        others = "+".join(s for s in participants if s != serial)
        dest   = agent["agent_dir"] / "threads" / f"{date_prefix}_{others}_{slug}.md"
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

def get_openai_client(secret_name: str) -> OpenAI:
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        sm = boto3.client("secretsmanager", region_name="us-east-1")
        raw = sm.get_secret_value(SecretId=secret_name)["SecretString"]
        # Handle both raw-string and JSON-wrapped secrets
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

# ---------------------------------------------------------------------------
# Tool-aware API call
# ---------------------------------------------------------------------------

def call_with_tools(
    client: OpenAI,
    model: str,
    system_prompt: str,
    user_prompt: str,
    use_tools: bool = True,
    verbose: bool = False,
) -> str:
    """
    Call the OpenAI API with an optional tool-use loop.

    If use_tools is True, the model may call read_file / glob_files /
    grep_content to inspect the codebase before producing its final response.
    The loop runs until the model stops issuing tool calls or the per-turn
    safety limit is reached.

    Returns the final message content as a string.
    """
    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user",   "content": user_prompt},
    ]
    tools_used = 0

    while True:
        kwargs = {"model": model, "messages": messages, "temperature": 0.3}
        if use_tools:
            kwargs["tools"] = TOOLS
            kwargs["tool_choice"] = "auto"

        response = client.chat.completions.create(**kwargs)
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
            final = client.chat.completions.create(
                model=model, messages=messages, temperature=0.3
            )
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

def run_thread(thread_dir: Path, client: OpenAI | None, model: str, dry_run: bool, verbose: bool, no_tools: bool = False):
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

        system_prompt = build_system_prompt(current)
        user_prompt   = build_user_prompt(thread_dir, current, turn_num)

        if dry_run:
            print(f"  DRY RUN -- model: {model}")
            print(f"  System prompt: {len(system_prompt):,} chars")
            print(f"  User prompt:   {len(user_prompt):,} chars")
            print(f"  Output:        {msg_file}")
            if verbose:
                print(f"\n--- SYSTEM (first 500) ---\n{system_prompt[:500]}")
                print(f"\n--- USER (first 1000) ---\n{user_prompt[:1000]}")
            break

        try:
            content = call_with_tools(
                client, model, system_prompt, user_prompt,
                use_tools=(not no_tools), verbose=verbose,
            )
        except Exception as exc:
            print(f"ERROR: OpenAI API call failed for {current}: {exc}")
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
    parser.add_argument("--model",    default="gpt-5.2",          help="OpenAI model (default: gpt-5.2)")
    parser.add_argument("--dry-run",   action="store_true",    help="Show invocation without calling API")
    parser.add_argument("--verbose",   action="store_true",    help="Print agent responses and tool calls to stdout")
    parser.add_argument("--no-tools",  action="store_true",    help="Disable tool use (faster/cheaper; agents cannot read files)")
    parser.add_argument("--secret",    default="openai-api-key", help="AWS Secrets Manager secret name")
    args = parser.parse_args()

    thread_dir = SCRIPT_DIR / args.thread
    if not thread_dir.exists() or not (thread_dir / "THREAD.json").exists():
        print(f"ERROR: Thread not found: {thread_dir}")
        sys.exit(1)

    if args.dry_run:
        client = None
    else:
        print(f"Fetching OpenAI key ({args.secret})...")
        try:
            client = get_openai_client(args.secret)
            print("OK: OpenAI client ready\n")
        except Exception as exc:
            print(f"ERROR: {exc}")
            sys.exit(1)

    run_thread(thread_dir, client, args.model, args.dry_run, args.verbose, args.no_tools)
    print("\nOrchestrator complete.")


if __name__ == "__main__":
    main()
