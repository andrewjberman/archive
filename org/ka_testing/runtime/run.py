#!/usr/bin/env python3
"""
Runner script — execute a project through the Tier 1 graph.

Usage:
    python run.py --brief "Build the portfolio dashboard" \
                  --directory "C:/Users/AndrewBerman/Desktop/ajb_workspace/portal"

    python run.py --brief-file project_brief.md \
                  --directory "C:/Users/AndrewBerman/Desktop/ajb_workspace/portal"

Environment:
    ANTHROPIC_API_KEY     Required. Your Anthropic API key.
    CORPOREAL_ROOT        Optional. Defaults to corporeal/ relative detection.
    HIERARCHY_MODEL       Optional. Default model for all nodes.
"""

from __future__ import annotations

import argparse
import os
import sys
from pathlib import Path


def _load_dotenv():
    """Load .env from ajb_workspace root if ANTHROPIC_API_KEY not already set."""
    if os.environ.get("ANTHROPIC_API_KEY"):
        return
    # Walk up from this file to find .env
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


def main():
    _load_dotenv()
    parser = argparse.ArgumentParser(
        description="Run a project through the Hierarchy LangGraph runtime."
    )
    parser.add_argument(
        "--brief",
        type=str,
        help="Project brief (natural language description of what to build).",
    )
    parser.add_argument(
        "--brief-file",
        type=str,
        help="Path to a file containing the project brief.",
    )
    parser.add_argument(
        "--directory",
        type=str,
        required=True,
        help="Working directory for the project (where files are created/modified).",
    )
    parser.add_argument(
        "--project-id",
        type=str,
        default=None,
        help="Unique project ID. Auto-generated if not provided.",
    )
    parser.add_argument(
        "--checkpoint-db",
        type=str,
        default=None,
        help="Path to SQLite database for checkpoint persistence. "
             "If not provided, uses in-memory checkpointer (lost on exit).",
    )
    parser.add_argument(
        "--event-log-dir",
        type=str,
        default=None,
        help="Directory for JSONL event logs. If not provided, uses "
             "system/runtime/event_logs/.",
    )
    parser.add_argument(
        "--macro",
        type=str,
        required=True,
        help="4-char macro code (e.g., MAIN, DSSR). Scopes agent resolution "
             "to the SPAN pair and workers within this macro.",
    )
    parser.add_argument(
        "--auto-approve",
        action="store_true",
        default=False,
        help="Auto-approve all design spec gates. Use when PRINCIPAL has "
             "already reviewed the PRD before delivery (e.g., deliver.sh --chain).",
    )

    args = parser.parse_args()

    # --- Validate ---
    if not args.brief and not args.brief_file:
        parser.error("Provide either --brief or --brief-file")

    if not os.environ.get("ANTHROPIC_API_KEY"):
        print("ERROR: ANTHROPIC_API_KEY environment variable not set.", file=sys.stderr)
        sys.exit(1)

    # --- Load brief ---
    if args.brief_file:
        brief_path = Path(args.brief_file)
        if not brief_path.exists():
            print(f"ERROR: Brief file not found: {args.brief_file}", file=sys.stderr)
            sys.exit(1)
        brief = brief_path.read_text(encoding="utf-8")
    else:
        brief = args.brief

    # --- Validate directory ---
    directory = Path(args.directory)
    if not directory.exists():
        print(f"ERROR: Directory not found: {args.directory}", file=sys.stderr)
        sys.exit(1)

    # --- Set up checkpointer ---
    checkpointer = None
    if args.checkpoint_db:
        try:
            from langgraph.checkpoint.sqlite import SqliteSaver
            import pathlib as _pl
            _pl.Path(args.checkpoint_db).parent.mkdir(parents=True, exist_ok=True)
            _saver = SqliteSaver.from_conn_string(args.checkpoint_db)
            # Newer langgraph returns a context manager; enter it
            if hasattr(_saver, "__enter__"):
                checkpointer = _saver.__enter__()
            else:
                checkpointer = _saver
        except ImportError:
            print("WARN: langgraph sqlite checkpoint not available, using memory.", file=sys.stderr)
        except Exception as e:
            print(f"WARN: sqlite checkpoint failed ({e}), using memory.", file=sys.stderr)

    # --- Run ---
    # Add runtime root to path so package imports work
    # os/ is 2 levels up from runtime/run.py
    os_root = str(Path(__file__).resolve().parent.parent)
    if os_root not in sys.path:
        sys.path.insert(0, os_root)

    from runtime.graph import run_project

    # Build auto-approve policies if flag is set
    policies = []
    if args.auto_approve:
        policies = [
            {
                "authority_type": "design",
                "sub_type": "spec_approval",
                "action": "approve",
                "rationale": "PRINCIPAL pre-approved via --auto-approve (PRD reviewed before delivery)",
            },
        ]

    result = run_project(
        brief=brief,
        working_directory=str(directory.resolve()),
        project_id=args.project_id,
        checkpointer=checkpointer,
        event_log_dir=args.event_log_dir,
        macro=args.macro,
        auto_approve_policies=policies,
    )

    # --- Summary ---
    print("\n--- AUDIT TRAIL ---")
    for entry in result.get("audit_trail", []):
        print(f"  [{entry.timestamp}] {entry.identity} ({entry.archetype}): {entry.action} — {entry.detail}")

    if result.get("error"):
        print(f"\nERROR: {result['error']}")
        sys.exit(1)

    print("\nProject completed successfully.")


if __name__ == "__main__":
    main()
