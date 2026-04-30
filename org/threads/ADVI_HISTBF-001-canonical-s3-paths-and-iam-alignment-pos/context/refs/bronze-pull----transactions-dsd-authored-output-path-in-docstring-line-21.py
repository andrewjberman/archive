"""ADVI_INFLEC.HISTBF.005 — Inflection transaction history bronze pull (REST).

Iterates all Inflection accounts and calls the Orion REST transactions endpoint
for each, collecting full account-level transaction history from inception.

    GET https://api.cloud.orionadvisor.com/api/v1/Portfolio/Accounts/{accountId}/Transactions

Key design facts (from DS~B Phase 0 probe, 20260430T174809Z):
- NO server-side transTypeId filter — returns ALL types; filter client-side downstream
- NO pagination — full account history returned in one JSON array (3,454 rows tested)
- NO date params for account-level endpoint — returns complete history in one call
- Empty accounts return [] not 404
- ~1,160 total calls (314 clients x ~3.7 avg accounts)

TransTypeId reference (store all; these are the relevant HISTBF types):
  24  = Management Fee (billing)
  110 = Fee Credit (billing reversal)
  8   = Client Contribution (activity / flow in)
  51  = Client Distribution (activity / flow out)

Output: s3://opal-data-inf/bronze/transactions/{pull_date}.parquet
  Flat parquet of all transactions across all accounts. One file per pull date.

Usage:
  # Full pull (all accounts, all history):
  python3 pull_inflection_transactions_rest.py --upload

  # Smoke test (first 5 clients, no upload):
  python3 pull_inflection_transactions_rest.py --limit-clients 5 --dry-run

  # With explicit pull date:
  python3 pull_inflection_transactions_rest.py --pull-date 2026-04-30 --upload

  # With explicit cycle ID for rate limiter state coordination:
  python3 pull_inflection_transactions_rest.py --upload --cycle-id <uuid>

Author: 0.4.0_DS_ClientPlatform_D
Project: ADVI_INFLEC.HISTBF.005
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

# BytesIO retained for accounts_v2 + household_rep_mapping parquet reads below.

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

ACCOUNTS_API_PATH = "/api/v1/Portfolio/Accounts/{account_id}/Transactions"
ACCOUNTS_V2_PREFIX = "silver/api_dims/accounts_v2/"
HH_REP_MAP_PREFIX = "silver/api_dims/household_rep_mapping/"

REQUEST_TIMEOUT_S = 60
DEFAULT_RETRIES = 3

CONFIRMED_FIELDS = {
    "id", "accountId", "clientId", "householdId", "transTypeId",
    "transDate", "transAmount", "noUnits", "navPrice",
    "ticker", "transactionDescription",
}


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


def _latest_accounts_v2_key(s3) -> str:
    paginator = s3.get_paginator("list_objects_v2")
    keys = sorted([
        obj["Key"]
        for page in paginator.paginate(Bucket=S3_BUCKET, Prefix=ACCOUNTS_V2_PREFIX)
        for obj in page.get("Contents", [])
        if obj["Key"].endswith("/data.parquet")
    ])
    if not keys:
        raise RuntimeError("No silver/api_dims/accounts_v2 snapshot found.")
    return keys[-1]


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


def _load_accounts_map(s3) -> tuple[list[int], dict[int, list[int]]]:
    """Return (sorted_client_ids, {client_id: [account_ids]}).

    client_ids: all 313 Inflection households from household_rep_mapping (full categorical
    universe — includes Fidelity_LH households + ghost households with historical AUA).

    account_ids: sourced from accounts_v2 silver (Fidelity_Inflection + Fidelity_LH after
    custodian filter expansion in convert_orion_api_to_silver.py). Ghost households absent
    from accounts_v2 (their accounts do not appear in NewPortfolio) are logged and produce
    zero API calls — their transactions are inaccessible without known account_ids.
    """
    # --- authoritative client universe (313 households) ---
    hh_key = _latest_hh_rep_map_key(s3)
    _log(f"Loading client_ids from household_rep_mapping: s3://{S3_BUCKET}/{hh_key}")
    hh_obj = s3.get_object(Bucket=S3_BUCKET, Key=hh_key)
    hh_df = pd.read_parquet(BytesIO(hh_obj["Body"].read()))
    if "household_id" not in hh_df.columns:
        raise RuntimeError(
            f"household_rep_mapping missing 'household_id' column. Got: {list(hh_df.columns)}"
        )
    hh_raw = hh_df["household_id"].dropna().astype(str).str.strip()
    all_client_ids = sorted({int(x) for x in hh_raw if x.isdigit()})
    _log(f"household_rep_mapping: {len(all_client_ids)} client_ids")

    # --- account_ids from accounts_v2 (includes Fidelity_LH post-silver-fix) ---
    acct_key = _latest_accounts_v2_key(s3)
    _log(f"Loading accounts_v2 from s3://{S3_BUCKET}/{acct_key}")
    acct_obj = s3.get_object(Bucket=S3_BUCKET, Key=acct_key)
    df = pd.read_parquet(BytesIO(acct_obj["Body"].read()))

    if "household_id" not in df.columns or "account_id" not in df.columns:
        raise RuntimeError(
            f"accounts_v2 missing required columns. Got: {list(df.columns)}"
        )

    df = df[df["account_id"].notna() & df["household_id"].notna()].copy()
    df["client_id_int"] = df["household_id"].astype(str).str.strip()
    df["account_id_int"] = df["account_id"].astype(str).str.strip()
    df = df[df["client_id_int"].str.isdigit() & df["account_id_int"].str.isdigit()]
    df["client_id_int"] = df["client_id_int"].astype(int)
    df["account_id_int"] = df["account_id_int"].astype(int)

    accounts_map: dict[int, list[int]] = {}
    for cid, group in df.groupby("client_id_int"):
        accounts_map[int(cid)] = sorted(group["account_id_int"].unique().tolist())

    ghost_hh = [cid for cid in all_client_ids if cid not in accounts_map]
    if ghost_hh:
        _log(
            f"WARN: {len(ghost_hh)} ghost households have no accounts in accounts_v2 "
            f"(absent from NewPortfolio — transactions inaccessible): {ghost_hh}"
        )

    total_accounts = sum(len(v) for v in accounts_map.values())
    _log(
        f"accounts_v2: {len(accounts_map)} clients with accounts, "
        f"{total_accounts} accounts "
        f"(avg {total_accounts / max(len(accounts_map), 1):.1f}/client)"
    )
    return all_client_ids, accounts_map


def _s3_key_exists(s3, key: str) -> bool:
    try:
        s3.head_object(Bucket=S3_BUCKET, Key=key)
        return True
    except Exception:
        return False


def _fetch_account_transactions(
    jwt: str, account_id: int, limiter: AdaptiveRateLimiter
) -> tuple[list[dict], int]:
    """Fetch full transaction history for one account.

    Returns (rows, http_status). Empty account returns ([], 200).
    """
    url = f"{BASE}{ACCOUNTS_API_PATH.format(account_id=account_id)}"
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
                _log(
                    f"WARN account {account_id}: timeout attempt={attempt} "
                    f"exc={exc!s} retry in {wait}s"
                )
                limiter.observe_call(tel.to_batch_result())
                time.sleep(wait)
                continue
            except requests.exceptions.RequestException as exc:
                tel.set_error(503)
                last_status = 503
                wait = (2 ** attempt) * 0.5
                _log(
                    f"WARN account {account_id}: exc={exc!s} "
                    f"attempt={attempt} retry in {wait}s"
                )
                limiter.observe_call(tel.to_batch_result())
                time.sleep(wait)
                continue

        if r.status_code == 200:
            try:
                data = r.json()
            except ValueError:
                _log(f"WARN account {account_id}: malformed JSON response")
                limiter.observe_call(tel.to_batch_result())
                return [], 200
            if not isinstance(data, list):
                _log(
                    f"WARN account {account_id}: unexpected response type "
                    f"{type(data).__name__}"
                )
                limiter.observe_call(tel.to_batch_result())
                return [], 200
            # Update record count for telemetry now that we have it
            tel._record_count = len(data)  # noqa: SLF001
            limiter.observe_call(tel.to_batch_result())
            return data, 200

        if r.status_code == 404:
            # 404 = account has no transactions. Treat as success; return empty list.
            limiter.observe_call(tel.to_batch_result())
            return [], 200

        if r.status_code in (429, 500, 502, 503, 504):
            wait = (2 ** attempt) * 0.5
            _log(
                f"WARN account {account_id}: status={r.status_code} "
                f"attempt={attempt} retry in {wait}s"
            )
            limiter.observe_call(tel.to_batch_result())
            time.sleep(wait)
            continue

        _log(
            f"FAIL account {account_id}: non-retryable status={r.status_code} "
            f"body={r.text[:200]}"
        )
        limiter.observe_call(tel.to_batch_result())
        return [], r.status_code

    _log(f"FAIL account {account_id}: exhausted {DEFAULT_RETRIES} retries")
    return [], last_status


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
        help="Upload flat parquet to s3://opal-data-inf/bronze/transactions/{date}.parquet",
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

    client_ids, accounts_map = _load_accounts_map(s3)
    if args.limit_clients > 0:
        client_ids = client_ids[: args.limit_clients]
        accounts_map = {cid: accounts_map[cid] for cid in client_ids if cid in accounts_map}
        _log(f"limit-clients={args.limit_clients}: pulling {len(client_ids)} clients")

    total_accounts = sum(len(v) for v in accounts_map.values())
    _log(f"Pulling {total_accounts} accounts across {len(client_ids)} clients")

    limiter = AdaptiveRateLimiter(dim_name="transactions")
    limiter.load_state()

    ok_count = 0
    fail_count = 0
    empty_count = 0
    all_rows: list[dict] = []
    account_total = 0
    t_start = time.time()

    for cid in client_ids:
        account_ids_list = accounts_map.get(cid, [])
        for aid in account_ids_list:
            account_total += 1
            if account_total == 1 or account_total % 100 == 0 or account_total == total_accounts:
                elapsed = time.time() - t_start
                _log(f"  [{account_total}/{total_accounts}] client={cid} account={aid} "
                     f"ok={ok_count} fail={fail_count} elapsed={elapsed:.1f}s")

            rows, status = _fetch_account_transactions(jwt, aid, limiter)
            if status == 200:
                if rows:
                    for row in rows:
                        row["pull_date"] = pull_date
                    all_rows.extend(rows)
                    ok_count += 1
                else:
                    empty_count += 1
            else:
                fail_count += 1

    limiter.flush()
    limiter.persist_state()

    elapsed_total = time.time() - t_start
    _log("")
    _log("=== pull_inflection_transactions_rest.py COMPLETE ===")
    _log(f"  accounts={account_total} ok={ok_count} empty={empty_count} fail={fail_count}")
    _log(f"  total_rows={len(all_rows):,} elapsed={elapsed_total:.1f}s "
         f"rate={limiter.current_rps():.3f}rps")

    if not all_rows:
        _log("WARN: no rows collected. Exiting 1.")
        return 1

    if args.dry_run:
        _log("DRY RUN: skipping write.")
        return 0

    df = pd.DataFrame(all_rows)
    fields_missing = CONFIRMED_FIELDS - set(df.columns)
    if fields_missing:
        _log(f"WARN: confirmed fields missing from response: {sorted(fields_missing)}")

    buf = BytesIO()
    df.to_parquet(buf, index=False)
    buf.seek(0)

    local_dir = Path(__file__).resolve().parent / "pulls"
    local_dir.mkdir(parents=True, exist_ok=True)
    local_path = local_dir / f"{pull_date}_inflection_transactions_rest.parquet"
    local_path.write_bytes(buf.getvalue())
    _log(f"Local: {local_path} ({local_path.stat().st_size:,} bytes)")

    if args.upload:
        bronze_key = f"bronze/transactions/{pull_date}.parquet"
        buf.seek(0)
        s3.put_object(
            Bucket=S3_BUCKET, Key=bronze_key, Body=buf.read(),
            ContentType="application/octet-stream", ServerSideEncryption="AES256",
        )
        _log(f"S3: s3://{S3_BUCKET}/{bronze_key} ({len(df):,} rows, {len(df.columns)} cols)")
    else:
        _log("--upload not set; parquet built locally but not uploaded to S3.")

    return 1 if fail_count > 0 else 0


if __name__ == "__main__":
    sys.exit(main())
