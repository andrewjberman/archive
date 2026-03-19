#!/usr/bin/env python3
"""
Runtime container entry point.

Starts the viz server in a background thread, then runs the requested
phase (alignment, execution, or both).

Usage (from docker run):
  docker run -v /path/to/project:/workspace \
    -e OPENAI_API_KEY=sk-... \
    -e HIERARCHY_LLM_PROVIDER=openai \
    -p 8111:8111 \
    runtime:latest \
    --phase alignment --phase execution --branch CLOUD_test

The user sees:
  - http://localhost:8111 for live dashboard
  - /workspace for code changes (mounted volume)
  - stdout for summary results
"""

import argparse
import http.server
import json
import os
import sys
import threading
import time
from datetime import datetime, timezone
from pathlib import Path

# Runtime is at /opt/runtime/ inside the container
sys.path.insert(0, "/opt")

RESULTS_DIR = Path("/workspace/.runtime/results")
RESULTS_DIR.mkdir(parents=True, exist_ok=True)


# ---------------------------------------------------------------------------
# Viz server (background thread)
# ---------------------------------------------------------------------------

def start_viz_server():
    """Start the telemetry dashboard on port 8111 in a background thread."""
    sys.path.insert(0, "/opt/viz")

    # Import the viz server module
    import importlib.util
    spec = importlib.util.spec_from_file_location("viz_server", "/opt/viz/server.py")
    viz = importlib.util.module_from_spec(spec)

    # Set the events directory before loading
    viz.events_dir = str(RESULTS_DIR)
    viz.jsonl_path = None

    spec.loader.exec_module(viz)

    server = http.server.HTTPServer(("0.0.0.0", 8111), viz.Handler)
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    print("Dashboard: http://localhost:8111", file=sys.stderr)
    return server


# ---------------------------------------------------------------------------
# Event bus initialization
# ---------------------------------------------------------------------------

def init_bus(project_id: str = "runtime"):
    """Initialize the event bus so all LLM calls emit to JSONL + console."""
    from runtime.events import init_event_bus
    return init_event_bus(
        project_id=project_id,
        log_dir=RESULTS_DIR,
        console=True,
    )


# ---------------------------------------------------------------------------
# Phase runners
# ---------------------------------------------------------------------------

def run_alignment(working_dir: str, prd_text: str, worker_config: list[dict], bus):
    """Run alignment phases 1-4. Returns assessment dict."""
    from runtime.alignment import (
        StateRequest,
        invoke_worker_for_state_direct,
        synthesize_alignment,
        assessment_to_dict,
    )
    from runtime.events import NODE_STARTED, NODE_COMPLETED

    bus.emit(NODE_STARTED, node="alignment", detail={"summary": "Alignment phases 1-4"})

    # Phase 1: Mechanical state requests
    state_requests = [
        StateRequest(
            worker_id=w["identity"],
            worker_serial=w["serial"],
            prd_section=prd_text,
            scoped_question="What do you currently produce, what exists, and what is missing relative to this design?",
        )
        for w in worker_config
    ]

    # Phase 2: Worker state collection
    state_reports = []
    for i, req in enumerate(state_requests):
        w = worker_config[i]
        bus.emit(NODE_STARTED, serial=w["serial"], node="worker",
                 detail={"summary": f"State collection: {w['serial']}"})

        report = invoke_worker_for_state_direct(
            system_prompt=w["prompt"],
            state_request=req,
            working_directory=working_dir,
            max_iterations=5,
            max_read_chars=10000,
        )
        state_reports.append(report)

        from runtime.alignment import _get_llm_module
        trace = _get_llm_module().get_last_trace()
        bus.emit(NODE_COMPLETED, serial=w["serial"], node="worker",
                 detail={
                     "input_tokens": trace.input_tokens if trace else 0,
                     "output_tokens": trace.output_tokens if trace else 0,
                     "llm_iterations": trace.iterations if trace else 0,
                 })

    # Phase 3: Coordinator synthesis
    coordinator_prompt = (
        "You are a Coordinator agent. Your job is to sequence and decompose work "
        "across multiple Worker agents. You evaluate interface compatibility, "
        "identify conflicts, and produce dependency graphs. You are pragmatic "
        "and precise. When analyzing Worker state reports, check field-level "
        "compatibility: exact field names, exact types, exact paths."
    )

    bus.emit(NODE_STARTED, node="coordinator", detail={"summary": "Synthesis"})
    assessment = synthesize_alignment(
        state_reports=state_reports,
        prd_section=prd_text,
        coordinator_identity="COORDINATOR",
        coordinator_prompt=coordinator_prompt,
    )
    bus.emit(NODE_COMPLETED, node="coordinator",
             detail={"input_tokens": assessment.token_usage.get("synthesis_input", 0),
                     "output_tokens": assessment.token_usage.get("synthesis_output", 0)})

    return assessment_to_dict(assessment), state_reports, assessment


def run_execution(
    working_dir: str,
    task_orders: list[dict],
    branch: str,
    bus,
):
    """Run Phase 5: dependency-ordered Worker execution.

    Each task_order dict has:
      identity, serial, prompt, task_order_text, allowed_paths,
      max_iterations, pre_flight_checks (optional)
    """
    from runtime.alignment import invoke_worker_for_execution, PreFlightCheck
    from runtime.events import NODE_STARTED, NODE_COMPLETED, NODE_FAILED

    results = {}

    for order in task_orders:
        serial = order["serial"]
        bus.emit(NODE_STARTED, serial=serial, node="worker",
                 detail={"summary": order.get("summary", serial)})

        # Convert pre-flight check dicts to PreFlightCheck objects
        pf_checks = None
        if order.get("pre_flight_checks"):
            pf_checks = [
                PreFlightCheck(name=c["name"], command=c["command"],
                               failure_message=c["failure_message"])
                for c in order["pre_flight_checks"]
            ]

        result = invoke_worker_for_execution(
            system_prompt=order["prompt"],
            task_order_text=order["task_order_text"],
            worker_id=order["identity"],
            worker_serial=serial,
            task_order_id=order.get("task_order_id", serial),
            working_directory=working_dir,
            allowed_paths=order.get("allowed_paths"),
            max_iterations=order.get("max_iterations", 25),
            branch=branch,
            pre_flight_checks=pf_checks,
        )

        evt = NODE_COMPLETED if result.success else NODE_FAILED
        bus.emit(evt, serial=serial, node="worker",
                 detail={
                     "input_tokens": result.token_usage.get("input", 0),
                     "output_tokens": result.token_usage.get("output", 0),
                     "llm_iterations": result.iterations,
                     "tool_calls": result.tool_calls,
                     "files_written": result.files_written,
                     "commit_sha": result.commit_sha,
                     "error": result.error,
                 })

        results[serial] = {
            "success": result.success,
            "files_written": result.files_written,
            "commit_sha": result.commit_sha,
            "token_usage": result.token_usage,
            "tool_calls": result.tool_calls,
            "iterations": result.iterations,
            "error": result.error,
            "pre_flight_failures": result.pre_flight_failures,
        }

        # Print summary
        status = "OK" if result.success else "FAIL"
        tok = result.token_usage
        print(
            f"  [{status}] {serial}: "
            f"{tok.get('input',0)}in/{tok.get('output',0)}out "
            f"| {result.iterations} iter, {result.tool_calls} tools "
            f"| commit={result.commit_sha or 'none'}",
            file=sys.stderr,
        )

        # Check if downstream Workers should be skipped
        if not result.success and order.get("blocks"):
            for blocked_serial in order["blocks"]:
                print(f"  SKIP: {blocked_serial} blocked by {serial} failure", file=sys.stderr)
                results[blocked_serial] = {"success": False, "skipped": True,
                                            "reason": f"Blocked by {serial}"}
                # Remove from task_orders so we don't try to run it
                task_orders[:] = [t for t in task_orders if t["serial"] != blocked_serial]

    return results


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(description="Runtime")
    parser.add_argument("--prd", type=str, help="Path to PRD file (relative to /workspace)")
    parser.add_argument("--config", type=str, help="Path to run config JSON (worker roster, task orders)")
    parser.add_argument("--branch", type=str, default="runtime_test", help="Git branch for execution")
    parser.add_argument("--no-viz", action="store_true", help="Skip dashboard server")
    parser.add_argument("--phase", type=str, nargs="+", default=["alignment"],
                        choices=["alignment", "execution", "both"],
                        help="Which phases to run")
    args = parser.parse_args()

    working_dir = "/workspace"

    # Start viz
    if not args.no_viz:
        start_viz_server()
        time.sleep(0.5)  # Let the server bind

    # Init event bus
    bus = init_bus("runtime")
    from runtime.events import PROJECT_STARTED, PROJECT_COMPLETED
    bus.emit(PROJECT_STARTED, detail={"branch": args.branch, "phases": args.phase})

    # Load config if provided
    config = {}
    if args.config:
        config_path = Path(working_dir) / args.config
        if config_path.exists():
            config = json.loads(config_path.read_text(encoding="utf-8"))

    # Load PRD
    prd_text = ""
    if args.prd:
        prd_path = Path(working_dir) / args.prd
        if prd_path.exists():
            prd_text = prd_path.read_text(encoding="utf-8")
        else:
            print(f"ERROR: PRD not found: {prd_path}", file=sys.stderr)
            sys.exit(1)

    phases = args.phase if isinstance(args.phase, list) else [args.phase]
    if "both" in phases:
        phases = ["alignment", "execution"]

    all_results = {"timestamp": datetime.now(timezone.utc).isoformat(), "phases": {}}

    if "alignment" in phases:
        worker_config = config.get("workers", [])
        if not worker_config:
            print("ERROR: No workers in config. Provide --config with a workers array.", file=sys.stderr)
            sys.exit(1)
        if not prd_text:
            print("ERROR: No PRD. Provide --prd path.", file=sys.stderr)
            sys.exit(1)

        assessment_dict, reports, assessment = run_alignment(working_dir, prd_text, worker_config, bus)
        all_results["phases"]["alignment"] = assessment_dict

    if "execution" in phases:
        task_orders = config.get("task_orders", [])
        if not task_orders:
            print("ERROR: No task_orders in config.", file=sys.stderr)
            sys.exit(1)

        exec_results = run_execution(working_dir, task_orders, args.branch, bus)
        all_results["phases"]["execution"] = exec_results

    bus.emit(PROJECT_COMPLETED, detail={
        "total_phases": len(phases),
    })

    # Save results
    ts = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S")
    results_file = RESULTS_DIR / f"run_{ts}.json"
    results_file.write_text(json.dumps(all_results, indent=2, default=str), encoding="utf-8")
    print(f"\nResults: {results_file}", file=sys.stderr)

    # Print summary
    print(json.dumps(all_results, indent=2, default=str))


if __name__ == "__main__":
    main()
