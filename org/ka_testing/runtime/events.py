"""
Event Stream -- real-time visibility into agent activity.

Provides a structured event bus that all runtime components emit to.
Tier 1: writes JSONL to a file + prints to console.
Tier 2: pluggable backends (WebSocket, Kafka, etc.)

Events follow a standard envelope:

    {
        "timestamp": "2026-03-13T14:30:00Z",
        "event_type": "node.started | node.completed | interrupt.fired | ...",
        "project_id": "PRJ-abc123",
        "identity": "APP-EXEC-CHF.APP.1",
        "serial": "CHF.APP.1",
        "archetype": "architect",
        "node": "architect",
        "phase": "design",
        "detail": { ... event-specific payload ... }
    }
"""

from __future__ import annotations

import json
import os
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Callable


# ---------------------------------------------------------------------------
# Event types
# ---------------------------------------------------------------------------

# Node lifecycle
NODE_STARTED = "node.started"
NODE_COMPLETED = "node.completed"
NODE_FAILED = "node.failed"

# Interrupts
INTERRUPT_FIRED = "interrupt.fired"
INTERRUPT_RESUMED = "interrupt.resumed"

# Agent lifecycle
AGENT_ACTIVATED = "agent.activated"
AGENT_DISPATCHED = "agent.dispatched"

# Deliverables
DELIVERABLE_SUBMITTED = "deliverable.submitted"
DELIVERABLE_EVALUATED = "deliverable.evaluated"

# Task orders
TASK_ORDER_CREATED = "task_order.created"
TASK_ORDER_DISPATCHED = "task_order.dispatched"

# Project lifecycle
PROJECT_STARTED = "project.started"
PROJECT_COMPLETED = "project.completed"
PROJECT_FAILED = "project.failed"

# Session logs
SESSION_LOG_WRITTEN = "session_log.written"

# LLM execution (per-iteration telemetry)
LLM_ITERATION = "llm.iteration"
LLM_TOOL_CALL = "llm.tool_call"
LLM_COMPLETE = "llm.complete"

# KF gate v3 — stage transition telemetry (SYS.CORE.KF_GATED_EXEC_IMPL)
KF_TRANSITION = "kf.transition"
KF_TRANSITION_DENIED = "kf.transition_denied"
ARCHETYPE_CONSTRAINT = "kf.archetype_constraint"


# ---------------------------------------------------------------------------
# Event bus
# ---------------------------------------------------------------------------

class EventBus:
    """Central event bus for the runtime.

    Subscribers receive every event. Tier 1 ships with two built-in
    subscribers: JSONL file writer and console printer.

    Identity model (from EXP-001-PSCFIX postmortem):
    - run_id: durable across checkpoint resumes (= project_id)
    - invocation_id: increments each time the bus is initialized for
      the same run (tracks resume cycles)
    - seq: monotonically increasing within run_id, continues from
      the existing JSONL file if one exists

    Thread safety: Tier 1 is single-threaded. Tier 2 will need locks.
    """

    def __init__(
        self,
        project_id: str = "",
        log_dir: Path | None = None,
        console: bool = True,
        quiet: bool = False,
    ):
        self.project_id = project_id
        self.run_id = project_id
        self.invocation_id = 1
        self.subscribers: list[Callable[[dict[str, Any]], None]] = []
        self._event_count = 0
        self._jsonl_path: Path | None = None

        # JSONL file subscriber — continue sequencing from existing file
        if log_dir:
            log_dir.mkdir(parents=True, exist_ok=True)
            self._jsonl_path = log_dir / f"{project_id}-events.jsonl"
            if self._jsonl_path.exists():
                # Continue from existing event stream
                self._event_count = self._count_existing_events(self._jsonl_path)
                self.invocation_id = self._count_invocations(self._jsonl_path) + 1
            self.subscribers.append(self._write_jsonl)

            # Telemetry log — human-readable, tail -f from outside Docker
            self._telemetry_path = log_dir / f"{project_id}-telemetry.log"
            self.subscribers.append(self._write_telemetry)

        # Console subscriber — rich format with tokens/iterations
        if console and not quiet:
            self.subscribers.append(self._print_console)

    @staticmethod
    def _count_existing_events(path: Path) -> int:
        """Count events in existing JSONL to continue sequence numbering."""
        try:
            with open(path, "r", encoding="utf-8") as f:
                return sum(1 for line in f if line.strip())
        except Exception:
            return 0

    @staticmethod
    def _count_invocations(path: Path) -> int:
        """Count how many project.started events exist (= prior invocations)."""
        count = 0
        try:
            with open(path, "r", encoding="utf-8") as f:
                for line in f:
                    if line.strip() and '"project.started"' in line:
                        count += 1
        except Exception:
            pass
        return count

    def emit(
        self,
        event_type: str,
        identity: str = "",
        serial: str = "",
        archetype: str = "",
        node: str = "",
        phase: str = "",
        detail: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        """Emit an event to all subscribers.

        Returns the event dict for chaining or inspection.
        """
        self._event_count += 1
        event = {
            "seq": self._event_count,
            "run_id": self.run_id,
            "invocation_id": self.invocation_id,
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "event_type": event_type,
            "project_id": self.project_id,
            "identity": identity,
            "serial": serial,
            "archetype": archetype,
            "node": node,
            "phase": phase,
            "detail": detail or {},
        }

        for sub in self.subscribers:
            try:
                sub(event)
            except Exception:
                pass  # Subscribers must not crash the runtime

        return event

    def subscribe(self, callback: Callable[[dict[str, Any]], None]):
        """Add a subscriber. It will receive all future events."""
        self.subscribers.append(callback)

    @property
    def event_count(self) -> int:
        return self._event_count

    # --- Discovery persistence (ONT.CORE.ARTIFACT v2) ---

    def write_discoveries(self, discoveries: list) -> int:
        """Persist discovery records to upstream.jsonl.

        Discoveries flow upstream (U) as PLK events. They are stored in
        {event_log_dir}/flows/upstream.jsonl for cross-level and cross-project
        retrieval. The Coordinator reads this file during dispatch planning.

        Returns the number of discoveries written.
        """
        if not discoveries or not self._jsonl_path:
            return 0

        flows_dir = self._jsonl_path.parent / "flows"
        flows_dir.mkdir(parents=True, exist_ok=True)
        upstream_path = flows_dir / "upstream.jsonl"

        count = 0
        with open(upstream_path, "a", encoding="utf-8") as f:
            for d in discoveries:
                record = {
                    "type": "discovery",
                    "agent_serial": getattr(d, "agent_serial", ""),
                    "task_order": getattr(d, "task_order_id", ""),
                    "kf_stage": getattr(d, "kf_stage", ""),
                    "scope": getattr(d, "scope", "within_project"),
                    "category": getattr(d, "category", ""),
                    "content": getattr(d, "content", {}),
                    "timestamp": getattr(d, "timestamp", ""),
                    "run_id": self.run_id,
                    "invocation_id": self.invocation_id,
                }
                f.write(json.dumps(record, default=str) + "\n")
                count += 1

        return count

    # --- Built-in subscribers ---

    def _write_jsonl(self, event: dict[str, Any]):
        """Append event as JSON line to the JSONL file."""
        with open(self._jsonl_path, "a", encoding="utf-8") as f:
            f.write(json.dumps(event, default=str) + "\n")

    @staticmethod
    def _format_telemetry_line(event: dict[str, Any], color: bool = False) -> str:
        """Format a single event into a human-readable telemetry line.

        Shows ALL available metrics: tokens, iterations, wall time, stop reason,
        tool calls, spec length, task count, deliverable count, verdicts.
        Used by both console printer and telemetry file writer.
        """
        et = event["event_type"]
        seq = event["seq"]
        serial = event.get("serial", "")
        identity = event.get("identity", "")
        node = event.get("node", "")
        detail = event.get("detail", {})
        ts = event.get("timestamp", "")[11:19]  # HH:MM:SS

        # ANSI codes (only if color=True)
        if color:
            CYAN, GREEN, YELLOW, RED, RESET, DIM, BOLD = (
                "\033[36m", "\033[32m", "\033[33m", "\033[31m",
                "\033[0m", "\033[2m", "\033[1m",
            )
        else:
            CYAN = GREEN = YELLOW = RED = RESET = DIM = BOLD = ""

        # Color by event type
        if "failed" in et:
            c = RED
        elif "completed" in et or "complete" in et:
            c = GREEN
        elif "interrupt" in et:
            c = YELLOW
        elif "iteration" in et or "tool_call" in et:
            c = DIM
        else:
            c = CYAN

        # Agent label (prefer serial, fall back to identity prefix)
        agent = serial or (identity[:25] if identity else node)

        # Build the line
        parts = [f"{c}[{seq:03d}]{RESET} {ts} {c}{et:<22}{RESET} {BOLD}{agent:<16}{RESET}"]

        # Metrics block — show everything available
        metrics = []

        wt = detail.get("wall_time_s")
        if wt is not None:
            metrics.append(f"wall={wt}s")

        in_tok = detail.get("input_tokens")
        out_tok = detail.get("output_tokens")
        if in_tok is not None or out_tok is not None:
            metrics.append(f"tok={in_tok or 0}/{out_tok or 0}")

        total_tok = detail.get("total_tokens")
        if total_tok and not in_tok:
            metrics.append(f"tok={total_tok}")

        stage = detail.get("stage")
        if stage:
            metrics.append(f"stage={stage}")

        iters = detail.get("llm_iterations") or detail.get("iteration")
        if iters is not None:
            metrics.append(f"iter={iters}")

        max_iter = detail.get("max_iterations")
        if max_iter is not None:
            metrics.append(f"max={max_iter}")

        stop = detail.get("stop_reason")
        if stop:
            flag = f"{RED}BUDGET{RESET}" if stop == "tool_use" and iters and max_iter and iters >= max_iter else stop
            metrics.append(f"stop={flag}")

        tc = detail.get("tool_calls")
        if tc is not None:
            fc = detail.get("failed_tool_calls", 0)
            metrics.append(f"tools={tc}" + (f"({fc}err)" if fc else ""))

        spec_len = detail.get("spec_length")
        if spec_len:
            metrics.append(f"spec={spec_len}ch")

        task_count = detail.get("task_count")
        if task_count is not None:
            metrics.append(f"tasks={task_count}")

        dlv = detail.get("deliverable_count")
        if dlv is not None:
            metrics.append(f"dlvs={dlv}")

        verdicts = detail.get("verdicts")
        if verdicts:
            metrics.append(f"verdicts={verdicts}")

        # Tool call details (for llm.tool_call events)
        tool_name = detail.get("tool_name")
        if tool_name:
            tool_path = detail.get("tool_path", "")
            success = detail.get("success", True)
            status = "" if success else f" {RED}FAIL{RESET}"
            metrics.append(f"{tool_name}({tool_path}){status}")

        # Summary (for events without structured metrics)
        summary = detail.get("summary", "")
        if summary and not metrics:
            metrics.append(summary)
        elif summary and "error" in detail:
            metrics.append(summary)

        # Error detail
        error = detail.get("error")
        if error and "summary" not in detail:
            metrics.append(f"{RED}{error[:120]}{RESET}")

        if metrics:
            parts.append(" | ".join(metrics))

        return " ".join(parts)

    def _print_console(self, event: dict[str, Any]):
        """Print a rich telemetry line to stderr with ANSI colors."""
        line = self._format_telemetry_line(event, color=True)
        print(line, file=sys.stderr, flush=True)

    def _write_telemetry(self, event: dict[str, Any]):
        """Write a plain-text telemetry line to the .log file.

        This file is the primary live-visibility mechanism. From outside
        the Docker container: tail -f {project}-telemetry.log
        """
        line = self._format_telemetry_line(event, color=False)
        with open(self._telemetry_path, "a", encoding="utf-8") as f:
            f.write(line + "\n")
            f.flush()


# ---------------------------------------------------------------------------
# Module-level singleton (set per project run)
# ---------------------------------------------------------------------------

_bus: EventBus | None = None


def init_event_bus(
    project_id: str,
    log_dir: Path | None = None,
    console: bool = True,
    quiet: bool = False,
) -> EventBus:
    """Initialize the global event bus for a project run.

    If a bus already exists for the same project_id, returns the
    existing bus (idempotent). This prevents duplicate initialization
    when checkpoint resume cycles re-invoke run_project().

    If the JSONL file already exists, the bus continues from the
    existing sequence number and increments invocation_id.
    """
    global _bus
    if _bus is not None and _bus.project_id == project_id:
        return _bus
    _bus = EventBus(
        project_id=project_id,
        log_dir=log_dir,
        console=console,
        quiet=quiet,
    )
    return _bus


def get_event_bus() -> EventBus | None:
    """Get the current event bus (None if not initialized)."""
    return _bus


def emit(event_type: str, **kwargs) -> dict[str, Any] | None:
    """Convenience: emit on the global bus if it exists."""
    if _bus:
        return _bus.emit(event_type, **kwargs)
    return None
