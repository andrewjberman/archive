"""ADVI_INFLEC.HISTBF.003 — Inflection asset classification bronze pull (backfill-capable).

Iterates a date range x Inflection clientIds, calling Orion's per-client assets endpoint.
Adaptive rate-limiting via AdaptiveRateLimiter (HISTBF.002).

    GET /api/v1/Portfolio/Clients/{clientId}/Assets/{MM-DD-YYYY}?$top=50000&includeCostBasis=false

Returns 100% Morningstar Category coverage via `assetClass` + `productCategory`
(58 columns total). Output is used by silver/api_dims/assets_v2 for asset classification.

Output: one parquet per date at
    bronze/orion-api-v2/{snap_iso}/assets.parquet
        rows = all client asset rows for that date
        cols = 58 native Orion fields (no snapshot_date added here; added by silver builder)

Resume semantics (default ON): if bronze/orion-api-v2/{date}/assets.parquet already exists
in S3, skip that date. Pass --no-resume to re-pull.

Prior version (DIAGFIX.010): single-date only, manual sleep throttle, 296-universe.
This version (HISTBF.003): date-range iteration, AdaptiveRateLimiter + CallTelemetry,
--cycle-id, resume checkpoint, 313-universe via household_rep_mapping.

Usage:
  # Single-date today:
  python3 pull_inflection_assets_v2.py --upload-bronze

  # 30-day backfill (today, today-1, ..., today-29):
  python3 pull_inflection_assets_v2.py --backfill-days 30 --upload-bronze

  # Explicit range (inclusive):
  python3 pull_inflection_assets_v2.py --start 2026-04-01 --end 2026-04-30 --upload-bronze

  # Single-date legacy mode (MM-DD-YYYY format preserved for backward compat):
  python3 pull_inflection_assets_v2.py --date 04-29-2026 --upload-bronze

  # Smoke test (5 clients x 2 dates, no upload):
  python3 pull_inflection_assets_v2.py --backfill-days 2 --limit 5 --dry-run

  # With explicit cycle ID (rate limiter state coordination):
  python3 pull_inflection_assets_v2.py --start 2020-05-26 --end 2026-04-30 \
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

# 58 expected columns from /Settings/Views/AssetDto Standard View.
# Used for schema-validation only; no enforcement (Orion may add fields).
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
    - Ghost households with historical AUA (API returns empty/404 = handled gracefully)
    """
    key = _latest_hh_rep_map_key(s3)
    _log(f"Loading clientIds from household_rep_mapping: s3://{S3_BUCKET}/{key}")
    obj = s3.get_object(Bucket=S3_BUCKET, Key=key)
    df = pd.read_parquet(BytesIO(obj["Body"].read()))
    if "household_id" not in df.columns:
        raise RuntimeError(
            f"household_rep_mapping missing 'household_id' column. Got: {list(df.columns)}"
        )
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
    key = f"bronze/assets/{date_iso}.parquet"
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
) -> list[dict]:
    """One REST call. Returns list of asset dicts (may be empty)."""
    url = f"{BASE}{CLIENT_ASSETS_PATH.format(cid=client_id, date=date_str)}"
    params = {"$top": TOP_N, "includeCostBasis": str(include_cost_basis).lower()}
    last_exc = None

    for attempt in range(1, DEFAULT_RETRIES + 1):
        limiter.throttle()
        with CallTelemetry() as tel:
            try:
                r = requests.get(url, headers=_headers(jwt), params=params,
                                 timeout=REQUEST_TIMEOUT_S)
                tel.set_response(r, record_count=0)
            except requests.exceptions.Timeout as exc:
                tel.set_error(503)
                last_exc = exc
                limiter.observe_call(tel.to_batch_result())
                wait = (2 ** attempt) * 0.5
                _log(f"WARN client {client_id} {date_str}: timeout attempt={attempt} retry in {wait}s")
                time.sleep(wait)
                continue
            except requests.exceptions.RequestException as exc:
                tel.set_error(503)
                last_exc = exc
                limiter.observe_call(tel.to_batch_result())
                wait = (2 ** attempt) * 0.5
                _log(f"WARN client {client_id} {date_str}: exc={exc!s} attempt={attempt} retry in {wait}s")
                time.sleep(wait)
                continue

        if r.status_code == 200:
            try:
                data = r.json()
            except ValueError:
                _log(f"WARN client {client_id} {date_str}: malformed JSON")
                limiter.observe_call(tel.to_batch_result())
                return []
            if not isinstance(data, list):
                _log(f"WARN client {client_id} {date_str}: unexpected shape ({type(data).__name__})")
                limiter.observe_call(tel.to_batch_result())
                return []
            tel._record_count = len(data)  # noqa: SLF001
            limiter.observe_call(tel.to_batch_result())
            return data

        if r.status_code in (429, 500, 502, 503, 504):
            limiter.observe_call(tel.to_batch_result())
            wait = (2 ** attempt) * 0.5
            _log(f"WARN client {client_id} {date_str}: status={r.status_code} attempt={attempt} retry in {wait}s")
            time.sleep(wait)
            continue

        # non-retryable (401, 403, 404, etc.)
        limiter.observe_call(tel.to_batch_result())
        _log(f"FAIL client {client_id} {date_str}: status={r.status_code} body={r.text[:200]}")
        return []

    _log(f"FAIL client {client_id} {date_str}: exhausted retries last_exc={last_exc!s}")
    return []


def _resolve_date_range(args) -> list[dt.date]:
    """Return list of dates (most recent first) per CLI flags."""
    today = dt.datetime.now(dt.timezone.utc).date()

    # --start/--end takes priority
    if args.start and args.end:
        start = dt.datetime.strptime(args.start, "%Y-%m-%d").date()
        end = dt.datetime.strptime(args.end, "%Y-%m-%d").date()
        if start > end:
            raise ValueError(f"--start {start} after --end {end}")
        n = (end - start).days + 1
        return [end - dt.timedelta(days=i) for i in range(n)]

    if args.backfill_days and args.backfill_days > 0:
        return [today - dt.timedelta(days=i) for i in range(args.backfill_days)]

    # Legacy --date MM-DD-YYYY
    if args.date:
        try:
            d = dt.datetime.strptime(args.date, "%m-%d-%Y").date()
        except ValueError:
            d = dt.datetime.strptime(args.date, "%Y-%m-%d").date()
        return [d]

    return [today]


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--date", default=None,
                        help="Single-date pull in MM-DD-YYYY or YYYY-MM-DD (default: today UTC).")
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
                             "s3://opal-data-inf/bronze/assets/{date}.parquet.")
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

    limiter = AdaptiveRateLimiter(dim_name="assets_v2")
    limiter.load_state()

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
        t_start = time.time()

        for i, cid in enumerate(client_ids, start=1):
            if i == 1 or i % 50 == 0 or i == len(client_ids):
                _log(f"  [{snap_iso}] fetching client {cid} ({i}/{len(client_ids)})...")
            assets = _fetch_one_client(jwt, cid, date_str, args.include_cost_basis, limiter)
            if assets:
                rows.extend(assets)

        elapsed = time.time() - t_start
        _log(
            f"  [{snap_iso}] rows={len(rows):,} elapsed={elapsed:.1f}s "
            f"rate={limiter.current_rps():.3f}rps"
        )
        grand_rows += len(rows)
        dates_pulled += 1

        if not rows:
            _log(f"  [{snap_iso}] empty pull. Skipping write.")
            per_date_summary.append({"date": snap_iso, "rows": 0, "elapsed_s": elapsed})
            continue

        df = pd.DataFrame(rows)

        # Coverage diagnostics on assetClass + productCategory
        fields_seen = set(df.columns)
        fields_missing = EXPECTED_FIELDS - fields_seen
        fields_new = fields_seen - EXPECTED_FIELDS
        if fields_missing:
            _log(f"  [{snap_iso}] WARN missing fields: {sorted(fields_missing)}")
        if fields_new:
            _log(f"  [{snap_iso}] NOTE new fields: {sorted(fields_new)}")

        null_ac = df["assetClass"].isna().sum() if "assetClass" in df.columns else len(df)
        null_pc = df["productCategory"].isna().sum() if "productCategory" in df.columns else len(df)
        total_mv = float(df["currentValue"].fillna(0).sum()) if "currentValue" in df.columns else 0.0
        _log(
            f"  [{snap_iso}] assetClass null={null_ac} | "
            f"productCategory null={null_pc} | mv=${total_mv:,.0f}"
        )

        per_date_summary.append({
            "date": snap_iso, "rows": len(rows), "elapsed_s": elapsed, "mv_total": total_mv,
        })

        if args.dry_run:
            _log(f"  [{snap_iso}] DRY RUN: skipping writes.")
            continue

        local_path = LOCAL_PULLS_DIR / f"{snap_iso}_inflection_assets_v2.parquet"
        df.to_parquet(local_path, index=False)
        _log(f"  [{snap_iso}] Local: {local_path} ({local_path.stat().st_size:,} bytes)")

        if args.upload_bronze:
            bronze_key = f"bronze/assets/{snap_iso}.parquet"
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

    return 0 if grand_rows > 0 or dates_skipped > 0 else 1


if __name__ == "__main__":
    sys.exit(main())
