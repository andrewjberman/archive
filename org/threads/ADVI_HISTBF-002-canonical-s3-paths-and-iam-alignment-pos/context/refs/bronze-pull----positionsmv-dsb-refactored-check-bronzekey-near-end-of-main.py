"""ADVI_INFLEC.HISTBF.003 — Inflection daily positions MV bronze pull (backfill-capable).

Iterates a date range x Inflection clientIds, calling Orion's per-client assets
endpoint at each (clientId, date). Adaptive rate-limiting via AdaptiveRateLimiter
(HISTBF.002) — restarts from prior observed ceiling, not SAFE_FLOOR.

    GET /api/v1/Portfolio/Clients/{clientId}/Assets/{MM-DD-YYYY}?$top=50000&includeCostBasis=false

Output: one parquet per date at
    bronze/orion-api-v2/{snap_iso}/positions.parquet
        rows = sum(per-client asset arrays) for that date
        cols = 58 native Orion fields + snapshot_date partition column

Resume semantics (default ON): if bronze/orion-api-v2/{date}/positions.parquet already
exists in S3, skip that date. Pass --no-resume to re-pull.

Prior version (DIAGFIX.012 Phase 2): manual sleep throttle, no rate limiter.
This version (HISTBF.003): AdaptiveRateLimiter + CallTelemetry + --cycle-id + resume.

Usage:
  # Single-date today:
  python3 pull_inflection_positions_daily.py --upload-bronze

  # 30-day backfill (today, today-1, ..., today-29):
  python3 pull_inflection_positions_daily.py --backfill-days 30 --upload-bronze

  # Explicit range (inclusive):
  python3 pull_inflection_positions_daily.py --start 2026-04-01 --end 2026-04-30 --upload-bronze

  # Smoke (5 clientIds x 2 dates, no upload):
  python3 pull_inflection_positions_daily.py --backfill-days 2 --limit 5 --dry-run

  # With explicit cycle ID (rate limiter state coordination):
  python3 pull_inflection_positions_daily.py --start 2020-05-26 --end 2026-04-30 \
      --upload-bronze --cycle-id <uuid>

Author: 0.4.0_DS_ClientPlatform
Project: ADVI_INFLEC.HISTBF.003
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

# rate_limiter lives in data/orion/scripts/bronze/
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "scripts" / "bronze"))
from rate_limiter import AdaptiveRateLimiter, CallTelemetry  # noqa: E402

from jwt_freshness import assert_fresh_or_exit  # noqa: E402

sys.stdout.reconfigure(encoding="utf-8")

BASE = "https://api.cloud.orionadvisor.com"
S3_BUCKET = "opal-data-inf"

SCRIPT_DIR = Path(__file__).resolve().parent
LOCAL_PULLS_DIR = SCRIPT_DIR / "pulls"

CLIENT_ASSETS_PATH = "/api/v1/Portfolio/Clients/{cid}/Assets/{date}"
HH_REP_MAP_PREFIX = "silver/api_dims/household_rep_mapping/"

TOP_N = 50000
DEFAULT_RETRIES = 3
REQUEST_TIMEOUT_S = 60

EXPECTED_FIELDS = {
    "id", "name", "accountNumber", "ticker", "currentShares", "currentValue",
    "currentPrice", "isManaged", "productCategory", "productCategoryAbbreviation",
    "assetClass", "isCustodialCash", "costBasis", "assetPercentOfAccount",
    "is13FReportable", "accountId", "accountStatusId", "accountType", "isActive",
    "isAdvReportable", "asOfDate", "assetLevelStrategy", "assetLevelStrategyId",
    "createdBy", "createdDate", "custodian", "downloadSymbol", "editedBy",
    "editedDate", "excludeAmount", "excludeAmountType", "isFeeExcluded",
    "excludeFromMargin", "excludePercentOf", "mscsFundAccountNumber", "fundFamily",
    "isGlobalExcluded", "householdName", "clientId", "isDataSharingEntity", "isin",
    "lastReconDate", "managementStyle", "isAdvisorOnly", "modelName", "isOrionVision",
    "productId", "productSubType", "productType", "isRebalance", "registrationId",
    "registrationName", "registrationType", "riskCategory", "secondaryAccountNumber",
    "sleeveType", "status", "isStrategyOverride",
}


def _log(msg: str) -> None:
    ts = dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    print(f"[{ts}] {msg}", flush=True)


def _headers(jwt: str) -> dict:
    return {
        "Authorization": f"Session {jwt}",
        "App": "OrionConnect",
        "AppPath": "/reports/dataqueries/querybuilder",
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
    """All 313 Inflection household_ids from household_rep_mapping (authoritative universe).

    Sourced from household_rep_mapping (not accounts_v2) to include:
    - All 294 active Fidelity_Inflection households
    - 9 Fidelity_LH households excluded by old accounts_v2 custodian filter
    - Ghost households with historical AUA but $0 current value (API returns empty/404)
    """
    key = _latest_hh_rep_map_key(s3)
    _log(f"Loading clientIds from household_rep_mapping: s3://{S3_BUCKET}/{key}")
    obj = s3.get_object(Bucket=S3_BUCKET, Key=key)
    df = pd.read_parquet(BytesIO(obj["Body"].read()))
    if "household_id" not in df.columns:
        raise RuntimeError(f"household_rep_mapping missing 'household_id' column. Got: {list(df.columns)}")
    raw = df["household_id"].dropna().astype(str).str.strip()
    raw = raw[raw != ""]
    cids = sorted({int(x) for x in raw if x.isdigit()})
    _log(f"Inflection households (distinct clientIds): {len(cids)}")
    return cids


def _s3_key_exists(s3, key: str) -> bool:
    try:
        s3.head_object(Bucket=S3_BUCKET, Key=key)
        return True
    except s3.exceptions.ClientError:
        return False
    except Exception:
        return False


def _already_pulled(s3, date_iso: str) -> bool:
    key = f"bronze/positions/{date_iso}.parquet"
    exists = _s3_key_exists(s3, key)
    if exists:
        _log(f"  RESUME: s3://{S3_BUCKET}/{key} exists — skipping date {date_iso}")
    return exists


def _fetch_one_client(
    jwt: str,
    client_id: int,
    date_str: str,
    include_cost_basis: bool,
    limiter: AdaptiveRateLimiter,
) -> tuple[list[dict], dict]:
    """One REST call. Returns (asset_rows, durability_event_dict)."""
    url = f"{BASE}{CLIENT_ASSETS_PATH.format(cid=client_id, date=date_str)}"
    params = {"$top": TOP_N, "includeCostBasis": str(include_cost_basis).lower()}
    durability = {
        "retries": 0, "5xx_count": 0, "429_count": 0, "timeout_count": 0,
        "non_retryable_count": 0, "malformed_count": 0,
        "final_status": None, "final_outcome": "fail",
    }
    last_exc = None

    for attempt in range(1, DEFAULT_RETRIES + 1):
        limiter.throttle()
        with CallTelemetry() as tel:
            try:
                r = requests.get(url, headers=_headers(jwt), params=params,
                                 timeout=REQUEST_TIMEOUT_S)
                tel.set_response(r, record_count=0)
                durability["final_status"] = r.status_code
            except requests.exceptions.Timeout as exc:
                tel.set_error(503)
                last_exc = exc
                durability["timeout_count"] += 1
                durability["retries"] += 1
                limiter.observe_call(tel.to_batch_result())
                wait = (2 ** attempt) * 0.5
                _log(f"WARN client {client_id} {date_str}: timeout attempt={attempt} retry in {wait}s")
                time.sleep(wait)
                continue
            except requests.exceptions.RequestException as exc:
                tel.set_error(503)
                last_exc = exc
                durability["retries"] += 1
                limiter.observe_call(tel.to_batch_result())
                wait = (2 ** attempt) * 0.5
                _log(f"WARN client {client_id} {date_str}: exc={exc!s} attempt={attempt} retry in {wait}s")
                time.sleep(wait)
                continue

        if r.status_code == 200:
            try:
                data = r.json()
            except ValueError:
                durability["malformed_count"] += 1
                _log(f"WARN client {client_id} {date_str}: malformed JSON")
                limiter.observe_call(tel.to_batch_result())
                return [], durability
            if not isinstance(data, list):
                durability["malformed_count"] += 1
                _log(f"WARN client {client_id} {date_str}: unexpected response shape ({type(data).__name__})")
                limiter.observe_call(tel.to_batch_result())
                return [], durability
            tel._record_count = len(data)  # noqa: SLF001
            limiter.observe_call(tel.to_batch_result())
            durability["final_outcome"] = "ok"
            return data, durability

        if r.status_code == 429:
            durability["429_count"] += 1
            durability["retries"] += 1
            limiter.observe_call(tel.to_batch_result())
            wait = (2 ** attempt) * 0.5
            _log(f"WARN client {client_id} {date_str}: 429 attempt={attempt} retry in {wait}s")
            time.sleep(wait)
            continue

        if r.status_code in (500, 502, 503, 504):
            durability["5xx_count"] += 1
            durability["retries"] += 1
            limiter.observe_call(tel.to_batch_result())
            wait = (2 ** attempt) * 0.5
            _log(f"WARN client {client_id} {date_str}: status={r.status_code} attempt={attempt} retry in {wait}s")
            time.sleep(wait)
            continue

        # non-retryable (401, 403, 404, etc.)
        durability["non_retryable_count"] += 1
        limiter.observe_call(tel.to_batch_result())
        _log(f"FAIL client {client_id} {date_str}: status={r.status_code} body={r.text[:200]}")
        return [], durability

    _log(f"FAIL client {client_id} {date_str}: exhausted retries last_exc={last_exc!s}")
    return [], durability


def _resolve_date_range(args) -> list[dt.date]:
    """Return a list of dates (most recent first) per CLI flags."""
    today = dt.datetime.now(dt.timezone.utc).date()

    if args.start and args.end:
        start = dt.datetime.strptime(args.start, "%Y-%m-%d").date()
        end = dt.datetime.strptime(args.end, "%Y-%m-%d").date()
        if start > end:
            raise ValueError(f"--start {start} after --end {end}")
        n = (end - start).days + 1
        return [end - dt.timedelta(days=i) for i in range(n)]

    if args.backfill_days and args.backfill_days > 0:
        return [today - dt.timedelta(days=i) for i in range(args.backfill_days)]

    if args.date:
        d = dt.datetime.strptime(args.date, "%Y-%m-%d").date()
        return [d]

    return [today]


def _summarize_durability(events: list[dict]) -> dict:
    if not events:
        return {}
    total = len(events)
    summary = {
        "total_calls":         total,
        "ok_count":            sum(1 for e in events if e["final_outcome"] == "ok"),
        "fail_count":          sum(1 for e in events if e["final_outcome"] != "ok"),
        "retried_count":       sum(1 for e in events if e["retries"] > 0),
        "total_retries":       sum(e["retries"] for e in events),
        "total_429":           sum(e["429_count"] for e in events),
        "total_5xx":           sum(e["5xx_count"] for e in events),
        "total_timeouts":      sum(e["timeout_count"] for e in events),
        "total_malformed":     sum(e["malformed_count"] for e in events),
        "total_non_retryable": sum(e["non_retryable_count"] for e in events),
    }
    statuses = [e["final_status"] for e in events if e["final_status"] is not None]
    summary["distinct_final_statuses"] = sorted(set(statuses))
    return summary


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--date", default=None,
                        help="Single-date pull, ISO YYYY-MM-DD (default: today UTC).")
    parser.add_argument("--backfill-days", type=int, default=0,
                        help="Pull today, today-1, ..., today-(N-1). Overrides --date.")
    parser.add_argument("--start", default=None,
                        help="Range start, ISO YYYY-MM-DD (use with --end).")
    parser.add_argument("--end", default=None,
                        help="Range end (inclusive), ISO YYYY-MM-DD.")
    parser.add_argument("--limit", type=int, default=0,
                        help="Limit pull to first N clientIds (smoke test). 0 = no limit.")
    parser.add_argument("--upload-bronze", action="store_true",
                        help="Mirror per-date parquet to "
                             "s3://opal-data-inf/bronze/positions/{date}.parquet.")
    parser.add_argument("--dry-run", action="store_true",
                        help="Pull without writing local or S3 outputs (just logs counts).")
    parser.add_argument("--include-cost-basis", action="store_true",
                        help="Set includeCostBasis=true on the API (heavier response).")
    parser.add_argument("--cycle-id", default=None,
                        help="UUID for this pull cycle (rate limiter state coordination). "
                             "Auto-generated if omitted.")
    parser.add_argument("--resume", action="store_true", default=True,
                        help="Skip dates whose S3 bronze parquet already exists (default ON).")
    parser.add_argument("--no-resume", dest="resume", action="store_false",
                        help="Re-pull all dates even if S3 bronze parquet already exists.")
    parser.add_argument("--durability-out", default=None,
                        help="Optional path for durability JSON report.")
    args = parser.parse_args(argv)

    assert_fresh_or_exit(script_name=Path(__file__).name)

    cycle_id = args.cycle_id or str(uuid.uuid4())
    _log(f"cycle_id={cycle_id} resume={args.resume}")

    s3 = boto3.client("s3", region_name="us-east-1")
    jwt = _load_jwt(s3)

    dates = _resolve_date_range(args)
    _log(f"Dates to pull ({len(dates)}): {dates[0].isoformat()} ... {dates[-1].isoformat()}")

    client_ids = _load_inflection_client_ids(s3)
    if args.limit > 0:
        client_ids = client_ids[: args.limit]
        _log(f"Limit applied: pulling first {len(client_ids)} clientIds per date")

    limiter = AdaptiveRateLimiter(dim_name="positions_mv")
    limiter.load_state()

    all_events: list[dict] = []
    per_date_summary: list[dict] = []
    grand_rows = 0
    dates_skipped = 0
    dates_pulled = 0

    LOCAL_PULLS_DIR.mkdir(parents=True, exist_ok=True)

    for d_idx, d in enumerate(dates, start=1):
        snap_iso = d.isoformat()
        date_str = d.strftime("%m-%d-%Y")

        if args.resume and args.upload_bronze and not args.dry_run:
            if _already_pulled(s3, snap_iso):
                dates_skipped += 1
                per_date_summary.append({"date": snap_iso, "rows": 0, "skipped": True})
                continue

        _log(f"--- date {d_idx}/{len(dates)}: API='{date_str}' iso='{snap_iso}' ---")

        rows: list[dict] = []
        date_events: list[dict] = []
        t_start = time.time()

        for i, cid in enumerate(client_ids, start=1):
            if i == 1 or i % 50 == 0 or i == len(client_ids):
                _log(f"  [{snap_iso}] fetching client {cid} ({i}/{len(client_ids)})...")
            assets, dur = _fetch_one_client(jwt, cid, date_str, args.include_cost_basis, limiter)
            dur["client_id"] = cid
            dur["date"] = snap_iso
            date_events.append(dur)
            if assets:
                for row in assets:
                    row["snapshot_date"] = snap_iso
                rows.extend(assets)

        elapsed = time.time() - t_start
        _log(f"  [{snap_iso}] rows={len(rows):,} elapsed={elapsed:.1f}s rate={limiter.current_rps():.3f}rps")
        all_events.extend(date_events)
        grand_rows += len(rows)
        dates_pulled += 1

        if not rows:
            _log(f"  [{snap_iso}] empty pull. Skipping write.")
            per_date_summary.append({"date": snap_iso, "rows": 0, "elapsed_s": elapsed})
            continue

        df = pd.DataFrame(rows)
        if "currentValue" in df.columns:
            mv_total = float(df["currentValue"].fillna(0).sum())
        else:
            mv_total = 0.0
        per_date_summary.append({
            "date": snap_iso, "rows": len(rows),
            "elapsed_s": elapsed, "mv_total": mv_total,
        })

        fields_seen = set(df.columns) - {"snapshot_date"}
        fields_missing = EXPECTED_FIELDS - fields_seen
        fields_new = fields_seen - EXPECTED_FIELDS
        if fields_missing:
            _log(f"  [{snap_iso}] WARN missing fields: {sorted(fields_missing)}")
        if fields_new:
            _log(f"  [{snap_iso}] NOTE new fields: {sorted(fields_new)}")

        if args.dry_run:
            _log(f"  [{snap_iso}] DRY RUN: skipping writes.")
            continue

        local_path = LOCAL_PULLS_DIR / f"{snap_iso}_inflection_positions.parquet"
        df.to_parquet(local_path, index=False)
        _log(f"  [{snap_iso}] Local: {local_path} ({local_path.stat().st_size:,} bytes)")

        if args.upload_bronze:
            bronze_key = f"bronze/positions/{snap_iso}.parquet"
            buf = BytesIO()
            df.to_parquet(buf, index=False)
            buf.seek(0)
            s3.put_object(
                Bucket=S3_BUCKET, Key=bronze_key,
                Body=buf.read(),
                ContentType="application/octet-stream",
                ServerSideEncryption="AES256",
            )
            _log(f"  [{snap_iso}] S3: s3://{S3_BUCKET}/{bronze_key}")

    limiter.flush()
    limiter.persist_state()

    _log(
        f"=== Pull complete: {grand_rows:,} total rows | "
        f"dates_pulled={dates_pulled} dates_skipped={dates_skipped} "
        f"final_rate={limiter.current_rps():.3f}rps ==="
    )
    for s in per_date_summary:
        if s.get("skipped"):
            _log(f"  {s['date']}: SKIPPED (already in S3)")
        elif "mv_total" in s:
            _log(f"  {s['date']}: rows={s['rows']:,} mv=${s['mv_total']:,.0f} elapsed={s['elapsed_s']:.1f}s")
        else:
            _log(f"  {s['date']}: rows={s['rows']:,} elapsed={s.get('elapsed_s', 0):.1f}s")

    durability = _summarize_durability(all_events)
    _log(f"Durability summary: {durability}")

    if args.durability_out:
        out_path = Path(args.durability_out)
        out_path.parent.mkdir(parents=True, exist_ok=True)
        out_path.write_text(json.dumps({
            "summary":    durability,
            "per_date":   per_date_summary,
            "events":     all_events,
        }, indent=2))
        _log(f"Durability report: {out_path}")

    return 0 if grand_rows > 0 or dates_skipped > 0 else 1


if __name__ == "__main__":
    sys.exit(main())
