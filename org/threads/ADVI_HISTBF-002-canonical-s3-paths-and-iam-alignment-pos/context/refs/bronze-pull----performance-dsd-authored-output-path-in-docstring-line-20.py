"""ADVI_INFLEC.HISTBF.006 — Inflection performance (TWR) history bronze pull (REST).

Iterates all Inflection clients and calls the Orion REST performance endpoint,
collecting the full inception-to-date weekly TWR factor time series per client.

    GET https://api.cloud.orionadvisor.com/api/v1/Portfolio/Clients/{clientId}/Performance

Key design facts (from DS~B Phase 0 probe, 20260430T174809Z):
- NO query params needed — single call returns ALL weekly factors from inception
- 365-day window limit was Envision-only; REST endpoint has no server-side cutoff
- Response: {"details": [{"asOfDate": "YYYY-MM-DD", "factor": <float>}], "summaries": [...]}
- Client 449 confirmed: 309 weekly data points, 2020-06-04 to 2026-04-30
- All 309 factors returned in one ~5KB response; no timeout observed
- ~314 clients × 1 call = ~314 total calls (~5 min at 1 req/s)
- New accounts (e.g. opened Nov 2025) may return empty details — log SKIP, 404 = success

HARD LIMIT: do NOT add date window params to this script. Single inception-to-date call only.
5y+ rolling windows time out on this endpoint.

Output: s3://opal-data-inf/bronze/performance/{pull_date}.parquet
  Flat parquet of all weekly TWR factors across all clients. One file per pull date.
  Columns: client_id (int), date (str YYYY-MM-DD), factor (float), pull_date (str).

Usage:
  # Full pull (all clients):
  python3 pull_inflection_performance_rest.py --upload

  # Smoke test (first 10 clients, no upload):
  python3 pull_inflection_performance_rest.py --limit-clients 10 --dry-run

  # With explicit pull date:
  python3 pull_inflection_performance_rest.py --pull-date 2026-04-30 --upload

  # With explicit cycle ID:
  python3 pull_inflection_performance_rest.py --upload --cycle-id <uuid>

Author: 0.4.0_DS_ClientPlatform_D
Project: ADVI_INFLEC.HISTBF.006
Date: 2026-04-30
"""
from __future__ import annotations

import argparse
import datetime as dt
import json
import sys
import time
import uuid
from io import BytesIO
from pathlib import Path

import boto3
import pandas as pd
import requests

# Rate limiter lives in data/orion/scripts/bronze/; add to sys.path for import.
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "scripts" / "bronze"))
from rate_limiter import AdaptiveRateLimiter, CallTelemetry  # noqa: E402

from jwt_freshness import assert_fresh_or_exit  # noqa: E402

sys.stdout.reconfigure(encoding="utf-8")

BASE = "https://api.cloud.orionadvisor.com"
S3_BUCKET = "opal-data-inf"

PERFORMANCE_API_PATH = "/api/v1/Portfolio/Clients/{client_id}/Performance"
HH_REP_MAP_PREFIX = "silver/api_dims/household_rep_mapping/"

REQUEST_TIMEOUT_S = 60
DEFAULT_RETRIES = 3


def _log(msg: str) -> None:
    ts = dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    print(f"[{ts}] {msg}", flush=True)


def _headers(jwt: str) -> dict:
    return {
        "Authorization": f"Session {jwt}",
        "App": "OrionConnect",
        "AppPath": "/portfolio",
        "BrowserSessionId": str(uuid.uuid4()),
        "Origin": BASE,
        "Referer": f"{BASE}/orionconnectapp/",
        "Accept": "application/json, text/plain, */*",
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
            "Chrome/147.0.0.0 Safari/537.36"
        ),
    }


def _load_jwt(s3) -> str:
    meta = json.loads(
        s3.get_object(Bucket=S3_BUCKET, Key="orion/jwt/current.json")["Body"].read()
    )
    jwt = meta.get("jwt", "")
    if not jwt:
        raise RuntimeError("JWT missing from s3://opal-data-inf/orion/jwt/current.json")
    issued = meta.get("issued_at_iso", "?")
    expires = meta.get("expires_at_iso", "?")
    _log(f"jwt loaded: issued={issued} expires={expires} len={len(jwt)}")
    return jwt


def _latest_hh_rep_map_key(s3) -> str:
    paginator = s3.get_paginator("list_objects_v2")
    keys = sorted([
        obj["Key"]
        for page in paginator.paginate(Bucket=S3_BUCKET, Prefix=HH_REP_MAP_PREFIX)
        for obj in page.get("Contents", [])
        if obj["Key"].endswith("/data.parquet")
    ])
    if not keys:
        raise RuntimeError("No silver/api_dims/household_rep_mapping snapshot found.")
    return keys[-1]


def _load_inflection_client_ids(s3) -> list[int]:
    """Load all 313 Inflection household_ids from household_rep_mapping silver.

    Sourcing from household_rep_mapping (not accounts_v2) ensures full coverage:
    - All 294 active Fidelity_Inflection households
    - 9 Fidelity_LH households (~$1.1M AUA) excluded by old accounts_v2 custodian filter
    - Ghost households with historical AUA but $0 current value (404 from API = handled)
    """
    key = _latest_hh_rep_map_key(s3)
    _log(f"Loading client_ids from household_rep_mapping: s3://{S3_BUCKET}/{key}")
    obj = s3.get_object(Bucket=S3_BUCKET, Key=key)
    df = pd.read_parquet(BytesIO(obj["Body"].read()))
    if "household_id" not in df.columns:
        raise RuntimeError(
            f"household_rep_mapping missing 'household_id' column. Got: {list(df.columns)}"
        )
    raw = df["household_id"].dropna().astype(str).str.strip()
    raw = raw[raw != ""]
    cids = sorted({int(x) for x in raw if x.isdigit()})
    _log(f"Inflection client_ids (household_rep_mapping): {len(cids)}")
    return cids


def _s3_key_exists(s3, key: str) -> bool:
    try:
        s3.head_object(Bucket=S3_BUCKET, Key=key)
        return True
    except Exception:
        return False


def _fetch_client_performance(
    jwt: str, client_id: int, limiter: AdaptiveRateLimiter
) -> tuple[dict | None, int]:
    """Fetch full inception-to-date performance for one client.

    Returns (raw_payload, http_status).
    raw_payload: full Orion JSON dict ({"details": [...], "summaries": [...]}).
                 None on hard failure; {} on 404/empty.
    """
    url = f"{BASE}{PERFORMANCE_API_PATH.format(client_id=client_id)}"
    last_status = 0

    for attempt in range(1, DEFAULT_RETRIES + 1):
        limiter.throttle()
        with CallTelemetry() as tel:
            try:
                r = requests.get(url, headers=_headers(jwt), timeout=REQUEST_TIMEOUT_S)
                tel.set_response(r, record_count=0)
                last_status = r.status_code
            except requests.exceptions.Timeout as exc:
                tel.set_error(503)
                last_status = 503
                wait = (2 ** attempt) * 0.5
                _log(f"WARN client {client_id}: timeout attempt={attempt} exc={exc!s} retry in {wait}s")
                limiter.observe_call(tel.to_batch_result())
                time.sleep(wait)
                continue
            except requests.exceptions.RequestException as exc:
                tel.set_error(503)
                last_status = 503
                wait = (2 ** attempt) * 0.5
                _log(f"WARN client {client_id}: exc={exc!s} attempt={attempt} retry in {wait}s")
                limiter.observe_call(tel.to_batch_result())
                time.sleep(wait)
                continue

        if r.status_code == 200:
            try:
                payload = r.json()
            except ValueError:
                _log(f"WARN client {client_id}: malformed JSON response")
                limiter.observe_call(tel.to_batch_result())
                return {}, 200
            n_details = len(payload.get("details", [])) if isinstance(payload, dict) else 0
            if n_details == 0:
                _log(f"INFO client {client_id}: empty performance details (new/zero-history client)")
            tel._record_count = n_details  # noqa: SLF001
            limiter.observe_call(tel.to_batch_result())
            return payload if isinstance(payload, dict) else {}, 200

        if r.status_code == 404:
            _log(f"INFO client {client_id}: 404 (no performance history — SKIP)")
            limiter.observe_call(tel.to_batch_result())
            return {}, 200

        if r.status_code in (429, 500, 502, 503, 504):
            wait = (2 ** attempt) * 0.5
            _log(f"WARN client {client_id}: status={r.status_code} attempt={attempt} retry in {wait}s")
            limiter.observe_call(tel.to_batch_result())
            time.sleep(wait)
            continue

        _log(f"FAIL client {client_id}: non-retryable status={r.status_code} body={r.text[:200]}")
        limiter.observe_call(tel.to_batch_result())
        return None, r.status_code

    _log(f"FAIL client {client_id}: exhausted {DEFAULT_RETRIES} retries")
    return None, last_status


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--cycle-id", default=None,
        help="UUID for this pull cycle (rate limiter state coordination). "
             "Auto-generated if omitted.",
    )
    parser.add_argument(
        "--limit-clients", type=int, default=0,
        help="Limit to first N clients (smoke test). 0 = no limit.",
    )
    parser.add_argument(
        "--pull-date", default=None,
        help="S3 partition date for output (default: today UTC, YYYY-MM-DD).",
    )
    parser.add_argument(
        "--upload", action="store_true",
        help="Upload flat parquet to s3://opal-data-inf/bronze/performance/{date}.parquet",
    )
    parser.add_argument(
        "--dry-run", action="store_true",
        help="Fetch and log without writing to S3.",
    )
    args = parser.parse_args(argv)

    assert_fresh_or_exit(script_name=Path(__file__).name)

    pull_date = args.pull_date or dt.datetime.now(dt.timezone.utc).date().isoformat()
    cycle_id = args.cycle_id or str(uuid.uuid4())
    _log(f"pull_date={pull_date} cycle_id={cycle_id} upload={args.upload} dry_run={args.dry_run}")

    s3 = boto3.client("s3", region_name="us-east-1")
    jwt = _load_jwt(s3)

    client_ids = _load_inflection_client_ids(s3)
    if args.limit_clients > 0:
        client_ids = client_ids[: args.limit_clients]
        _log(f"limit-clients={args.limit_clients}: pulling {len(client_ids)} clients")

    _log(f"Pulling performance for {len(client_ids)} clients")

    limiter = AdaptiveRateLimiter(dim_name="performance")
    limiter.load_state()

    ok_count = 0
    empty_count = 0
    fail_count = 0
    all_detail_rows: list[dict] = []
    t_start = time.time()

    for i, cid in enumerate(client_ids, start=1):
        if i == 1 or i % 50 == 0 or i == len(client_ids):
            elapsed = time.time() - t_start
            _log(f"  [{i}/{len(client_ids)}] client={cid} "
                 f"ok={ok_count} fail={fail_count} elapsed={elapsed:.1f}s")

        payload, status = _fetch_client_performance(jwt, cid, limiter)
        if status == 200:
            details = payload.get("details", []) if payload else []
            if details:
                for d in details:
                    date_val = d.get("asOfDate") or d.get("date")
                    factor = d.get("factor")
                    if date_val is not None and factor is not None:
                        all_detail_rows.append({
                            "client_id": cid,
                            "date": date_val,
                            "factor": factor,
                            "pull_date": pull_date,
                        })
                ok_count += 1
            else:
                empty_count += 1
        else:
            fail_count += 1

    limiter.flush()
    limiter.persist_state()

    elapsed_total = time.time() - t_start
    avg_weeks = len(all_detail_rows) / max(ok_count, 1)
    _log("")
    _log("=== pull_inflection_performance_rest.py COMPLETE ===")
    _log(f"  clients={len(client_ids)} ok={ok_count} empty={empty_count} fail={fail_count}")
    _log(f"  total_weekly_rows={len(all_detail_rows):,} avg_weeks/client={avg_weeks:.1f} "
         f"elapsed={elapsed_total:.1f}s rate={limiter.current_rps():.3f}rps")

    if not all_detail_rows:
        _log("WARN: no detail rows collected. Exiting 1.")
        return 1

    if args.dry_run:
        _log("DRY RUN: skipping write.")
        return 0

    df = pd.DataFrame(all_detail_rows)

    buf = BytesIO()
    df.to_parquet(buf, index=False)
    buf.seek(0)

    local_dir = Path(__file__).resolve().parent / "pulls"
    local_dir.mkdir(parents=True, exist_ok=True)
    local_path = local_dir / f"{pull_date}_inflection_performance_rest.parquet"
    local_path.write_bytes(buf.getvalue())
    _log(f"Local: {local_path} ({local_path.stat().st_size:,} bytes)")

    if args.upload:
        bronze_key = f"bronze/performance/{pull_date}.parquet"
        buf.seek(0)
        s3.put_object(
            Bucket=S3_BUCKET, Key=bronze_key, Body=buf.read(),
            ContentType="application/octet-stream", ServerSideEncryption="AES256",
        )
        _log(f"S3: s3://{S3_BUCKET}/{bronze_key} ({len(df):,} rows)")
    else:
        _log("--upload not set; parquet built locally but not uploaded to S3.")

    return 1 if fail_count > 0 else 0


if __name__ == "__main__":
    sys.exit(main())
