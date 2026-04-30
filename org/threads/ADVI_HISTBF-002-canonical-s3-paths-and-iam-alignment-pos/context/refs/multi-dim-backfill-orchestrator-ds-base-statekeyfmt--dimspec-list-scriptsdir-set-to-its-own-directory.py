"""
HISTBF.003 Phase 1 — multi-dim backfill orchestrator

Coordinates per-dim bronze pulls across the full Inflection history window
(2020-05-26 to present) with adaptive rate-limiter coordination and a
global-pause trigger for systemic rate failure (HISTBF.003 §8a).

Dim catalog + run order (ops-convenience; highest-confidence first):
  1. positions_mv  — per-date, per-client (--start/--end)
  2. assets_v2     — per-date, per-client (--start/--end)
  3. transactions  — per-account, inception-to-date (single-shot)
  4. performance   — per-client, inception-to-date (single-shot)

Global-pause trigger (§8a):
  >= 3 dims with last_failure_at within GLOBAL_PAUSE_WINDOW_S seconds
  AND jwt_freshness confirms JWT is fresh
  -> pause all dims for GLOBAL_PAUSE_BACKOFF_S (default 2x rate_limiter STEP_DOWN/STEP_UP ratio)

Date-range dims are broken into --chunk-days windows so the orchestrator
can check JWT freshness + global-pause state between chunks.

Single-shot dims are launched once and run to completion.

Usage:
  python3 run_backfill_orchestrator.py \\
      --start 2020-05-26 --end 2026-04-30 \\
      [--chunk-days 90] \\
      [--dims positions_mv,assets_v2,transactions,performance] \\
      [--cycle-id <uuid>] \\
      [--parallel 2] \\
      [--no-resume]

Author: 0.4.0_DS_ClientPlatform_A
Project: ADVI_HISTBF.003
"""
from __future__ import annotations

import argparse
import datetime as dt
import json
import os
import subprocess
import sys
import threading
import time
import uuid
from concurrent.futures import ThreadPoolExecutor, as_completed
from dataclasses import dataclass, asdict, field
from pathlib import Path
from typing import Optional

import boto3

S3_BUCKET = "opal-data-inf"
STATE_KEY_FMT = "orion/rate_limit_state_{dim_name}.json"
PROGRESS_KEY_FMT = "orion/backfill_progress_{cycle_id}.json"

DEFAULT_CHUNK_DAYS = 90
DEFAULT_PARALLEL = 2
SUBPROCESS_TIMEOUT_S = 14400  # 4 hours per chunk
GLOBAL_PAUSE_WINDOW_S = 120   # 2-minute sliding window for failure detection
GLOBAL_PAUSE_BACKOFF_S = 600  # default 10 min backoff when global-pause fires

# Rate limiter STEP_DOWN default (from rate_limiter.py); used for backoff calculation.
RATE_LIMITER_STEP_DOWN = 0.15
BACKFILL_EARLIEST = "2020-05-26"

# Pull script script names relative to this file's directory.
DATE_RANGE = "date_range"
SINGLE_SHOT = "single_shot"


@dataclass
class DimSpec:
    name: str
    script: str
    mode: str  # DATE_RANGE or SINGLE_SHOT
    extra_args: tuple[str, ...] = ()


BACKFILL_DIMS: list[DimSpec] = [
    DimSpec(
        "positions_mv",
        "pull_inflection_positions_daily.py",
        DATE_RANGE,
        extra_args=("--upload-bronze",),
    ),
    DimSpec(
        "assets_v2",
        "pull_inflection_assets_v2.py",
        DATE_RANGE,
        extra_args=("--upload-bronze",),
    ),
    DimSpec(
        "transactions",
        "pull_inflection_transactions_rest.py",
        SINGLE_SHOT,
        extra_args=("--upload",),
    ),
    DimSpec(
        "performance",
        "pull_inflection_performance_rest.py",
        SINGLE_SHOT,
        extra_args=("--upload",),
    ),
]


@dataclass
class ChunkResult:
    dim: str
    chunk_start: str
    chunk_end: str
    status: str  # "ok" | "fail" | "skip"
    exit_code: int
    elapsed_s: float
    error: str = ""


@dataclass
class DimProgress:
    dim: str
    mode: str
    chunks_done: int = 0
    chunks_total: int = 0
    last_chunk_end: str = ""
    status: str = "pending"  # "pending" | "running" | "ok" | "fail"
    error: str = ""


@dataclass
class GlobalPauseCoordinator:
    """Monitors per-dim S3 rate-limiter state files for systemic failure.

    Fires when >= 3 dims show last_failure_at within GLOBAL_PAUSE_WINDOW_S
    AND jwt_freshness reports the JWT is still valid.
    """
    _lock: threading.Lock = field(default_factory=threading.Lock, repr=False)
    _paused: bool = False
    _pause_until: float = 0.0  # monotonic timestamp
    _s3: Optional[object] = field(default=None, repr=False)
    backoff_s: int = GLOBAL_PAUSE_BACKOFF_S

    def _get_s3(self) -> object:
        if self._s3 is None:
            self._s3 = boto3.client("s3", region_name="us-east-1")
        return self._s3

    def check_and_maybe_pause(self, active_dims: list[str]) -> bool:
        """Read S3 state files; trigger global-pause if threshold met.

        Returns True if global-pause was just triggered.
        """
        with self._lock:
            if self._paused and time.monotonic() < self._pause_until:
                return False  # already paused — caller should wait
            self._paused = False

        now_utc = dt.datetime.now(dt.timezone.utc)
        cutoff_utc = now_utc - dt.timedelta(seconds=GLOBAL_PAUSE_WINDOW_S)

        dims_with_recent_failure: list[str] = []
        for dim_name in active_dims:
            key = STATE_KEY_FMT.format(dim_name=dim_name)
            try:
                s3 = self._get_s3()
                body = s3.get_object(Bucket=S3_BUCKET, Key=key)["Body"].read()
                state = json.loads(body)
                raw_ts = state.get("last_failure_at")
                if not raw_ts:
                    continue
                fail_dt = dt.datetime.fromisoformat(raw_ts)
                if fail_dt.tzinfo is None:
                    fail_dt = fail_dt.replace(tzinfo=dt.timezone.utc)
                if fail_dt >= cutoff_utc:
                    dims_with_recent_failure.append(dim_name)
            except Exception:
                pass  # state file unreadable — skip this dim

        if len(dims_with_recent_failure) < 3:
            return False

        # Check JWT freshness before firing global-pause.
        # Import locally to avoid circular path issues on non-EC2 environments.
        try:
            sys.path.insert(0, str(Path(__file__).resolve().parent))
            from jwt_freshness import check_jwt_freshness
            report = check_jwt_freshness(emit_cw=True, script_name="backfill_orchestrator")
            if not report.is_fresh:
                _log(
                    "WARN: global-pause threshold met but JWT is stale — "
                    "likely auth failure, not systemic rate exhaustion; skipping global-pause"
                )
                return False
        except Exception as exc:
            _log(f"WARN: could not check JWT freshness for global-pause evaluation: {exc}")
            return False

        with self._lock:
            self._paused = True
            self._pause_until = time.monotonic() + self.backoff_s
            _log(
                f"GLOBAL-PAUSE FIRED: dims_with_recent_failure={dims_with_recent_failure} "
                f"window={GLOBAL_PAUSE_WINDOW_S}s; pausing all dims for {self.backoff_s}s"
            )
        return True

    def is_paused(self) -> bool:
        with self._lock:
            if self._paused and time.monotonic() >= self._pause_until:
                self._paused = False
                _log("GLOBAL-PAUSE lifted — resuming dim pulls")
            return self._paused

    def wait_if_paused(self, poll_interval_s: int = 30) -> None:
        """Block until global-pause clears, polling at poll_interval_s."""
        while self.is_paused():
            remaining = int(self._pause_until - time.monotonic())
            _log(f"GLOBAL-PAUSE: waiting {max(0, remaining)}s for backoff to expire ...")
            time.sleep(poll_interval_s)


def _log(msg: str) -> None:
    ts = dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    print(f"[{ts}] [orchestrator] {msg}", flush=True)


def _date_chunks(
    start: str, end: str, chunk_days: int
) -> list[tuple[str, str]]:
    """Split [start, end] into non-overlapping chunks of at most chunk_days days."""
    s = dt.date.fromisoformat(start)
    e = dt.date.fromisoformat(end)
    chunks: list[tuple[str, str]] = []
    cur = s
    while cur <= e:
        chunk_end = min(cur + dt.timedelta(days=chunk_days - 1), e)
        chunks.append((cur.isoformat(), chunk_end.isoformat()))
        cur = chunk_end + dt.timedelta(days=1)
    return chunks


def _run_subprocess(
    script: str,
    args: list[str],
    scripts_dir: str,
    cycle_id: str,
    timeout_s: int = SUBPROCESS_TIMEOUT_S,
) -> tuple[int, str]:
    """Launch script as subprocess; return (exit_code, stderr_tail)."""
    cmd = ["python3", script] + args + ["--cycle-id", cycle_id]
    env = os.environ.copy()
    env["PYTHONUNBUFFERED"] = "1"
    try:
        proc = subprocess.run(
            cmd,
            cwd=scripts_dir,
            env=env,
            capture_output=True,
            text=True,
            timeout=timeout_s,
        )
        if proc.stdout:
            # Stream last 2KB of stdout to orchestrator log.
            tail = proc.stdout[-2048:]
            for line in tail.splitlines():
                print(f"  [{script}] {line}", flush=True)
        err_tail = proc.stderr[-500:] if proc.stderr else ""
        return proc.returncode, err_tail
    except subprocess.TimeoutExpired:
        return 1, f"subprocess timeout after {timeout_s}s"
    except Exception as exc:
        return 1, f"{type(exc).__name__}: {exc}"


def _run_date_range_dim(
    spec: DimSpec,
    start: str,
    end: str,
    chunk_days: int,
    cycle_id: str,
    scripts_dir: str,
    resume: bool,
    coordinator: GlobalPauseCoordinator,
    active_dims: list[str],
    progress: DimProgress,
) -> list[ChunkResult]:
    """Iterate date chunks for a DATE_RANGE dim. Returns all chunk results."""
    chunks = _date_chunks(start, end, chunk_days)
    progress.chunks_total = len(chunks)
    progress.status = "running"
    results: list[ChunkResult] = []

    for chunk_start, chunk_end in chunks:
        # Wait if global-pause is active.
        coordinator.wait_if_paused()

        # JWT freshness check before each chunk.
        try:
            sys.path.insert(0, scripts_dir)
            from jwt_freshness import check_jwt_freshness
            report = check_jwt_freshness(emit_cw=True, script_name=spec.name)
            if not report.is_fresh:
                _log(
                    f"FATAL [{spec.name}]: JWT not fresh before chunk "
                    f"{chunk_start}..{chunk_end}: {report.raises_on_stale}"
                )
                results.append(ChunkResult(
                    dim=spec.name,
                    chunk_start=chunk_start,
                    chunk_end=chunk_end,
                    status="fail",
                    exit_code=2,
                    elapsed_s=0.0,
                    error="JWT not fresh; aborting dim",
                ))
                progress.status = "fail"
                return results
        except Exception as exc:
            _log(f"WARN [{spec.name}]: JWT freshness check failed ({exc}); proceeding anyway")

        script_args = list(spec.extra_args) + [
            "--start", chunk_start,
            "--end", chunk_end,
        ]
        if not resume:
            script_args.append("--no-resume")

        _log(f"[{spec.name}] chunk {chunk_start}..{chunk_end} start")
        t0 = time.time()
        exit_code, err_tail = _run_subprocess(
            spec.script, script_args, scripts_dir, cycle_id
        )
        elapsed = time.time() - t0

        if exit_code == 0:
            _log(f"[{spec.name}] chunk {chunk_start}..{chunk_end} OK elapsed={elapsed:.1f}s")
            results.append(ChunkResult(
                dim=spec.name,
                chunk_start=chunk_start,
                chunk_end=chunk_end,
                status="ok",
                exit_code=0,
                elapsed_s=round(elapsed, 1),
            ))
        else:
            _log(
                f"[{spec.name}] chunk {chunk_start}..{chunk_end} FAIL "
                f"exit={exit_code} elapsed={elapsed:.1f}s err={err_tail[:200]}"
            )
            results.append(ChunkResult(
                dim=spec.name,
                chunk_start=chunk_start,
                chunk_end=chunk_end,
                status="fail",
                exit_code=exit_code,
                elapsed_s=round(elapsed, 1),
                error=err_tail[:300],
            ))
            # Non-fatal chunk failure: check global-pause before continuing.
            coordinator.check_and_maybe_pause(active_dims)

        progress.chunks_done += 1
        progress.last_chunk_end = chunk_end

    ok_count = sum(1 for r in results if r.status == "ok")
    fail_count = sum(1 for r in results if r.status == "fail")
    progress.status = "ok" if fail_count == 0 else "fail"
    _log(
        f"[{spec.name}] date-range complete: {ok_count} ok / {fail_count} fail "
        f"total={len(results)} chunks"
    )
    return results


def _run_single_shot_dim(
    spec: DimSpec,
    cycle_id: str,
    scripts_dir: str,
    resume: bool,
    coordinator: GlobalPauseCoordinator,
    active_dims: list[str],
    progress: DimProgress,
) -> list[ChunkResult]:
    """Run a SINGLE_SHOT dim once. Returns a single-element chunk result list."""
    coordinator.wait_if_paused()
    progress.status = "running"
    progress.chunks_total = 1

    script_args = list(spec.extra_args)
    if not resume:
        script_args.append("--no-resume")

    _log(f"[{spec.name}] single-shot start")
    t0 = time.time()
    exit_code, err_tail = _run_subprocess(
        spec.script, script_args, scripts_dir, cycle_id
    )
    elapsed = time.time() - t0

    if exit_code == 0:
        _log(f"[{spec.name}] single-shot OK elapsed={elapsed:.1f}s")
        progress.status = "ok"
        progress.chunks_done = 1
        return [ChunkResult(
            dim=spec.name,
            chunk_start="inception",
            chunk_end="current",
            status="ok",
            exit_code=0,
            elapsed_s=round(elapsed, 1),
        )]
    else:
        _log(
            f"[{spec.name}] single-shot FAIL exit={exit_code} "
            f"elapsed={elapsed:.1f}s err={err_tail[:200]}"
        )
        progress.status = "fail"
        progress.error = err_tail[:300]
        progress.chunks_done = 1
        coordinator.check_and_maybe_pause(active_dims)
        return [ChunkResult(
            dim=spec.name,
            chunk_start="inception",
            chunk_end="current",
            status="fail",
            exit_code=exit_code,
            elapsed_s=round(elapsed, 1),
            error=err_tail[:300],
        )]


def _write_progress(
    s3_client: object,
    cycle_id: str,
    dim_progress: dict[str, DimProgress],
    chunk_results: list[ChunkResult],
) -> None:
    key = PROGRESS_KEY_FMT.format(cycle_id=cycle_id)
    body = {
        "cycle_id": cycle_id,
        "updated_at": dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "dims": {name: asdict(p) for name, p in dim_progress.items()},
        "chunk_results": [asdict(r) for r in chunk_results],
    }
    try:
        s3_client.put_object(
            Bucket=S3_BUCKET,
            Key=key,
            Body=json.dumps(body, indent=2),
            ContentType="application/json",
        )
        _log(f"progress written to s3://{S3_BUCKET}/{key}")
    except Exception as exc:
        _log(f"WARN: progress write failed ({exc})")


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--start", default=BACKFILL_EARLIEST,
                   help=f"Start date YYYY-MM-DD (default: {BACKFILL_EARLIEST})")
    p.add_argument("--end", default=None,
                   help="End date YYYY-MM-DD (default: today UTC)")
    p.add_argument("--chunk-days", type=int, default=DEFAULT_CHUNK_DAYS,
                   help=f"Days per chunk for date-range dims (default: {DEFAULT_CHUNK_DAYS})")
    p.add_argument("--dims", default=None,
                   help="Comma-separated subset of dim names (default: all)")
    p.add_argument("--cycle-id", default=None,
                   help="UUID for this backfill cycle (auto-generated if omitted)")
    p.add_argument("--parallel", type=int, default=DEFAULT_PARALLEL,
                   help=f"Max concurrent dim threads (default: {DEFAULT_PARALLEL})")
    p.add_argument("--repo-dir", default=None,
                   help="Repo root; default: 3 levels up from this script")
    p.add_argument("--resume", action="store_true", default=True,
                   help="Skip dates/accounts already present in S3 (default ON)")
    p.add_argument("--no-resume", dest="resume", action="store_false",
                   help="Re-pull all dates/accounts")
    p.add_argument("--global-pause-backoff", type=int, default=GLOBAL_PAUSE_BACKOFF_S,
                   help=f"Seconds to pause all dims on global-pause trigger (default: {GLOBAL_PAUSE_BACKOFF_S})")
    args = p.parse_args()

    cycle_id = args.cycle_id or str(uuid.uuid4())
    end_date = args.end or dt.datetime.utcnow().strftime("%Y-%m-%d")

    # Scripts directory = directory containing this file.
    scripts_dir = str(Path(__file__).resolve().parent)
    if args.repo_dir:
        scripts_dir = args.repo_dir

    selected_dim_names = set(args.dims.split(",")) if args.dims else None
    dims: list[DimSpec] = [
        d for d in BACKFILL_DIMS
        if (selected_dim_names is None or d.name in selected_dim_names)
    ]
    active_dim_names = [d.name for d in dims]

    coordinator = GlobalPauseCoordinator(backoff_s=args.global_pause_backoff)

    dim_progress = {
        d.name: DimProgress(dim=d.name, mode=d.mode) for d in dims
    }
    all_chunk_results: list[ChunkResult] = []
    results_lock = threading.Lock()

    _log(
        f"HISTBF.003 backfill start: cycle_id={cycle_id} "
        f"dims={active_dim_names} start={args.start} end={end_date} "
        f"chunk_days={args.chunk_days} parallel={args.parallel} resume={args.resume}"
    )

    s3_client = boto3.client("s3", region_name="us-east-1")
    _write_progress(s3_client, cycle_id, dim_progress, all_chunk_results)

    def run_dim(spec: DimSpec) -> list[ChunkResult]:
        if spec.mode == DATE_RANGE:
            return _run_date_range_dim(
                spec,
                start=args.start,
                end=end_date,
                chunk_days=args.chunk_days,
                cycle_id=cycle_id,
                scripts_dir=scripts_dir,
                resume=args.resume,
                coordinator=coordinator,
                active_dims=active_dim_names,
                progress=dim_progress[spec.name],
            )
        else:
            return _run_single_shot_dim(
                spec,
                cycle_id=cycle_id,
                scripts_dir=scripts_dir,
                resume=args.resume,
                coordinator=coordinator,
                active_dims=active_dim_names,
                progress=dim_progress[spec.name],
            )

    with ThreadPoolExecutor(max_workers=args.parallel) as pool:
        future_to_spec = {pool.submit(run_dim, spec): spec for spec in dims}
        for fut in as_completed(future_to_spec):
            spec = future_to_spec[fut]
            try:
                chunk_results = fut.result()
            except Exception as exc:
                _log(f"FATAL [{spec.name}]: future raised: {type(exc).__name__}: {exc}")
                chunk_results = [ChunkResult(
                    dim=spec.name,
                    chunk_start="?",
                    chunk_end="?",
                    status="fail",
                    exit_code=1,
                    elapsed_s=0.0,
                    error=f"future exception: {exc}",
                )]
                dim_progress[spec.name].status = "fail"
                dim_progress[spec.name].error = str(exc)[:300]

            with results_lock:
                all_chunk_results.extend(chunk_results)

            _write_progress(s3_client, cycle_id, dim_progress, all_chunk_results)

    # Final summary.
    ok_dims = [name for name, p in dim_progress.items() if p.status == "ok"]
    fail_dims = [name for name, p in dim_progress.items() if p.status == "fail"]
    overall = "SUCCESS" if not fail_dims else "FAILURE"

    _log(
        f"HISTBF.003 backfill {overall}: "
        f"ok={ok_dims} fail={fail_dims} cycle_id={cycle_id}"
    )
    _write_progress(s3_client, cycle_id, dim_progress, all_chunk_results)

    return 0 if not fail_dims else 1


if __name__ == "__main__":
    sys.exit(main())
