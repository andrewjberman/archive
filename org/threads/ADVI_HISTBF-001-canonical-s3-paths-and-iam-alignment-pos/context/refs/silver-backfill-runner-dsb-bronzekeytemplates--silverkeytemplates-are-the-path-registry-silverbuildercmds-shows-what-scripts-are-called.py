"""ADVI_HISTBF.004 Phase 2 — Silver backfill for SUPPORTED dims (positions_mv, assets_v2).

Iterates a date range and converts historical bronze parquet partitions to silver for
each date. Bronze existence is checked before each conversion; missing dates are skipped
with a log entry. Already-converted silver partitions are skipped when --resume is set.

NOT rate-limited: silver conversion is local compute + S3 read/write; no ORIAPI calls.

Usage:
  # Backfill positions_mv only:
  python3 run_silver_backfill.py --dims positions_mv --start 2020-05-26 --end 2026-04-30

  # Backfill both SUPPORTED dims:
  python3 run_silver_backfill.py --dims positions_mv assets_v2 --start 2020-05-26 --end 2026-04-30

  # Resume (skip dates already converted):
  python3 run_silver_backfill.py --dims positions_mv --start 2020-05-26 --end 2026-04-30 --resume

  # Dry-run (check bronze existence only; no silver writes):
  python3 run_silver_backfill.py --dims positions_mv --start 2026-04-01 --end 2026-04-30 --dry-run

  # Weekdays only (skip weekends — Orion positions are business-day snapshots):
  python3 run_silver_backfill.py --dims positions_mv --start 2020-05-26 --end 2026-04-30 --weekdays-only

Phase 0 investigation findings (HISTBF.004 §1-3):
  positions_mv: NATIVE — convert_orion_api_to_silver.py --dim positions_mv --snapshot-date DATE
  assets_v2:    NATIVE — convert_assets_v2_to_silver.py --date DATE --upload
  Silver output paths: s3://opal-data-inf/silver/api_dims/{dim}/snapshot_date={date}/data.parquet
    — date-partitioned, non-conflicting with daily outputs.
  Gold dependency: SILVER + GOLD RE-RUN — INF_B_00 must re-run for historical date range after
    silver conversion completes; downstream portal scripts (INF_I_D00, INF_C_04, etc.) scan all
    holdings files and need a single batch re-run at the end of Phase 2.

Author: 0.4.0_DS_ClientPlatform
Project: ADVI_HISTBF.004
Date: 2026-04-30
"""
from __future__ import annotations

import argparse
import datetime
import subprocess
import sys
from pathlib import Path

import boto3
from botocore.exceptions import ClientError

S3_BUCKET = "opal-data-inf"

SCRIPT_DIR = Path(__file__).resolve().parent

# Bronze S3 key templates (Phase 1 outputs from HISTBF.003).
BRONZE_KEY_TEMPLATES: dict[str, str] = {
    "positions_mv": "bronze/positions/{date}.parquet",
    "assets_v2": "bronze/assets/{date}.parquet",
}

# Silver S3 key templates (Phase 2 outputs, written by the builder scripts).
SILVER_KEY_TEMPLATES: dict[str, str] = {
    "positions_mv": "silver/positions_mv/{date}.parquet",
    "assets_v2": "silver/assets_v2/{date}.parquet",
}

# Invocation templates for each dim's silver builder.
# {date} is substituted with YYYY-MM-DD. Scripts are sibling to this file.
SILVER_BUILDER_CMDS: dict[str, list[str]] = {
    "positions_mv": [
        sys.executable,
        str(SCRIPT_DIR / "convert_orion_api_to_silver.py"),
        "--dim", "positions_mv",
        "--snapshot-date", "{date}",
        "--upload",
    ],
    "assets_v2": [
        sys.executable,
        str(SCRIPT_DIR / "convert_assets_v2_to_silver.py"),
        "--date", "{date}",
        "--upload",
    ],
}

SUPPORTED_DIMS = list(BRONZE_KEY_TEMPLATES.keys())


def _log(msg: str) -> None:
    ts = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    print(f"[{ts}] {msg}", flush=True)


def _s3_exists(s3_client, key: str) -> bool:
    try:
        s3_client.head_object(Bucket=S3_BUCKET, Key=key)
        return True
    except ClientError as exc:
        if exc.response["Error"]["Code"] in ("404", "NoSuchKey"):
            return False
        raise


def _date_range(start: datetime.date, end: datetime.date, weekdays_only: bool) -> list[datetime.date]:
    dates = []
    cur = start
    while cur <= end:
        if not weekdays_only or cur.weekday() < 5:
            dates.append(cur)
        cur += datetime.timedelta(days=1)
    return dates


def run_backfill(
    dims: list[str],
    start: datetime.date,
    end: datetime.date,
    resume: bool,
    dry_run: bool,
    weekdays_only: bool,
) -> dict[str, dict[str, int]]:
    """Run silver conversion for each (dim, date) pair in range.

    Returns per-dim counters: {dim: {converted, skipped_bronze_missing,
    skipped_silver_exists, failed}}.
    """
    s3 = boto3.client("s3", region_name="us-east-1")
    dates = _date_range(start, end, weekdays_only)
    _log(f"Date range: {start} to {end} ({len(dates)} dates, weekdays_only={weekdays_only})")
    _log(f"Dims: {dims}  |  resume={resume}  |  dry_run={dry_run}")

    totals: dict[str, dict[str, int]] = {
        dim: {"converted": 0, "skipped_bronze_missing": 0,
              "skipped_silver_exists": 0, "failed": 0}
        for dim in dims
    }

    for date_obj in dates:
        date_iso = date_obj.isoformat()
        for dim in dims:
            bronze_key = BRONZE_KEY_TEMPLATES[dim].format(date=date_iso)
            silver_key = SILVER_KEY_TEMPLATES[dim].format(date=date_iso)
            counters = totals[dim]

            if not _s3_exists(s3, bronze_key):
                _log(f"SKIP  {dim} {date_iso} -- bronze missing: {bronze_key}")
                counters["skipped_bronze_missing"] += 1
                continue

            if resume and _s3_exists(s3, silver_key):
                _log(f"SKIP  {dim} {date_iso} -- silver already exists (--resume)")
                counters["skipped_silver_exists"] += 1
                continue

            if dry_run:
                _log(f"DRY   {dim} {date_iso} -- bronze exists; would convert")
                counters["converted"] += 1
                continue

            cmd = [part.format(date=date_iso) for part in SILVER_BUILDER_CMDS[dim]]
            _log(f"RUN   {dim} {date_iso} -- {' '.join(cmd)}")
            try:
                result = subprocess.run(cmd, capture_output=True, text=True, timeout=300)
                if result.returncode != 0:
                    _log(f"FAIL  {dim} {date_iso} -- exit {result.returncode}")
                    if result.stderr:
                        _log(f"  stderr: {result.stderr.strip()[:400]}")
                    counters["failed"] += 1
                else:
                    _log(f"OK    {dim} {date_iso}")
                    counters["converted"] += 1
            except subprocess.TimeoutExpired:
                _log(f"FAIL  {dim} {date_iso} -- timeout (300s)")
                counters["failed"] += 1
            except Exception as exc:
                _log(f"FAIL  {dim} {date_iso} -- {exc}")
                counters["failed"] += 1

    return totals


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument(
        "--dims", nargs="+", choices=SUPPORTED_DIMS, default=SUPPORTED_DIMS,
        help=f"Dims to backfill (default: all SUPPORTED: {SUPPORTED_DIMS}).",
    )
    p.add_argument(
        "--start", required=True,
        help="Backfill range start date, inclusive (YYYY-MM-DD).",
    )
    p.add_argument(
        "--end", required=True,
        help="Backfill range end date, inclusive (YYYY-MM-DD).",
    )
    p.add_argument(
        "--resume", action="store_true",
        help="Skip dates where silver partition already exists in S3.",
    )
    p.add_argument(
        "--dry-run", action="store_true",
        help="Check bronze existence + log what would run; no silver writes.",
    )
    p.add_argument(
        "--weekdays-only", action="store_true",
        help="Skip weekends (Orion position snapshots are business-day only).",
    )
    args = p.parse_args(argv)

    try:
        start = datetime.date.fromisoformat(args.start)
        end = datetime.date.fromisoformat(args.end)
    except ValueError as exc:
        p.error(f"Invalid date format: {exc}")

    if start > end:
        p.error(f"--start {start} must be <= --end {end}")

    totals = run_backfill(
        dims=args.dims,
        start=start,
        end=end,
        resume=args.resume,
        dry_run=args.dry_run,
        weekdays_only=args.weekdays_only,
    )

    _log("=== SUMMARY ===")
    any_failures = False
    for dim, counters in totals.items():
        _log(
            f"  {dim}: converted={counters['converted']} "
            f"skipped_bronze_missing={counters['skipped_bronze_missing']} "
            f"skipped_silver_exists={counters['skipped_silver_exists']} "
            f"failed={counters['failed']}"
        )
        if counters["failed"] > 0:
            any_failures = True

    if any_failures:
        _log("RESULT: PARTIAL FAILURE -- some dates failed; re-run with --resume to retry.")
        return 1

    _log("RESULT: OK")
    return 0


if __name__ == "__main__":
    sys.exit(main())
