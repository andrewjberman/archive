"""OPAL_ASSETS G4 -- per-partner ETF-ownership fold (DRAFT for review).

Author: 0.8.0_AE_CloudComp | 2026-07-13 | STATUS: DRAFT -- routed to 1.0.0_SA_CTO~B
(schema arch-gate) + 0.7.0_AE_CloudOps~A (emitter-structure align) BEFORE any deploy.

WHAT THIS IS: the schema-INDEPENDENT half of the G4 fold. It reads the already-served
Opal-side per-partner ETF-ownership series (opal-data-etfs/daily/{partner}/{date}.json,
COO-ratified canonical held-source) and derives, per Opal ETF, the list of
`held_by_partner` ownership entries the bucket row carries. ZERO sovereign read: it
touches only opal-data-etfs (Opal-side). The upstream bd/RPS read that BUILT the 49F
series is ETFS_SETUP/DS's cadence, not here.

WHAT IS STUBBED (`# SUBJECT-TO-~A-EMITTER`): the exact DynamoDB table/GSI keys + the
item-write (UpdateItem) shape are 0.7.0~A's base emitter's -- this module returns plain
dicts; attach_ownership_to_cohort_items() shows the integration point as a stub.

Design refs: G4 design c509e1c9d, G5 spec e57c02ff4, ~A G6 contract be910e7b7,
CTO-base schema OPAL_ASSETS_P0A_SCHEMA_DESIGN_20260713.md.
"""
from __future__ import annotations

import argparse
import datetime as dt
import json

# cohort_id <-> ticker for the 4 Opal ETFs (verbatim from ~A's G6 contract).
ETF_COHORT_BY_TICKER = {
    "DIVZ": "etf_divz",
    "IDVZ": "etf_idvz",
    "PFOE": "etf_pfoe",
    "PFDE": "etf_pfde",
}
OPAL_ETF_TICKERS = tuple(ETF_COHORT_BY_TICKER)

ETFS_BUCKET = "opal-data-etfs"
ETFS_DAILY_PREFIX = "daily"
# Partners whose per-partner ETF-ownership series we fold (Opal-side, already-served).
# Cottonwood is ONE-WAY (PRD 3e): it folds in, nothing flows back.
FOLD_PARTNERS = ("49financial", "inflection", "cottonwood")

# Staleness threshold (calendar-days, DRAFT) before a held entry reads rolled_forward
# vs fresh. SUBJECT-TO-~A/CTO~B: the trading-day-precise arithmetic + the exact
# threshold live in the G6 checker's calendar (alarms.tf g6_cohort_thresholds); this
# draft uses a calendar-day lag as a stand-in and flags the exact source below.
OWNERSHIP_STALE_THRESHOLD_DAYS = 3


def _source_masters_from_artifact(source_artifact: str) -> list[str]:
    """Derive the source_master LIST (from day 1, CTO~B forward-compat) from the daily
    series' `source_artifact`. 49F RPS = the 08242234 book; inflection (opal-data-inf,
    Eclipse/Orion) + cottonwood are fund/model-level, master-agnostic -> empty list."""
    sa = (source_artifact or "").lower()
    if "schwab/silver/rps" in sa or "08242234" in sa:
        return ["08242234"]
    return []


def _partial_flag(source_masters: list[str]) -> str | None:
    """Interim undercount disclosure. The 49F RPS side is 08242234-ONLY; the 08335338
    CBUGL custody side is NOT represented until G2 (both-masters account-dedup). D1 (PRD
    3c) proved the undercount is real (~22K Opal-ETF position rows live in 08335338).
    Returns None (flag ABSENT) once source_masters carries both -> that absence IS the
    G4-DONE signal (PRD AC4)."""
    if source_masters == ["08242234"]:
        return "08242234-only"
    return None


def _calendar_lag_days(source_as_of: str, bucket_date: str) -> int | None:
    try:
        a = dt.date.fromisoformat(source_as_of)
        b = dt.date.fromisoformat(bucket_date)
    except (TypeError, ValueError):
        return None
    return (b - a).days


def _derive_state(lag_days: int | None) -> str:
    """fresh vs rolled_forward for an ownership entry. `missing` is handled by the
    caller (absent series). SUBJECT-TO-~A: replace lag_days with the G6 checker's
    trading-day staleness so the ownership entry's state agrees with the cohort alarm."""
    if lag_days is None:
        return "missing"
    return "fresh" if lag_days <= OWNERSHIP_STALE_THRESHOLD_DAYS else "rolled_forward"


def _read_partner_daily(partner: str, bucket_date: str, s3_client) -> list[dict] | None:
    """Latest opal-data-etfs/daily/{partner}/{d}.json with d <= bucket_date. Returns the
    parsed rows (a list of per-ETF ownership records) or None if no partition exists
    (-> the partner's ETF entries land state=missing). Opal-side read only."""
    prefix = f"{ETFS_DAILY_PREFIX}/{partner}/"
    latest_key = None
    latest_ds = None
    paginator = s3_client.get_paginator("list_objects_v2")
    for page in paginator.paginate(Bucket=ETFS_BUCKET, Prefix=prefix):
        for obj in page.get("Contents", []):
            base = obj["Key"].rsplit("/", 1)[-1]
            if not base.endswith(".json"):
                continue
            ds = base[: -len(".json")]
            if len(ds) == len("YYYY-MM-DD") and ds <= bucket_date:
                if latest_ds is None or ds > latest_ds:
                    latest_ds, latest_key = ds, obj["Key"]
    if latest_key is None:
        return None
    raw = s3_client.get_object(Bucket=ETFS_BUCKET, Key=latest_key)["Body"].read()
    rows = json.loads(raw)
    return rows if isinstance(rows, list) else [rows]


def _ownership_entry(row: dict, bucket_date: str, etf_total: float | None) -> dict:
    """One held_by_partner entry from a daily-series row. `as_of` = the row's OWN
    source_as_of (NEVER a cross-partner min -- PRD 3d). ownership_pct needs etf_total
    (the ETF cohort's value, from ~A's ETF row / the mdpf served etf_total_net_assets);
    left None when unavailable, never faked."""
    source_artifact = str(row.get("source_artifact", ""))
    source_masters = _source_masters_from_artifact(source_artifact)
    as_of = str(row.get("source_as_of") or row.get("date") or "")
    held = row.get("ownership_value")
    lag = _calendar_lag_days(as_of, bucket_date)
    ownership_pct = None
    if held is not None and etf_total not in (None, 0):
        ownership_pct = round(float(held) / float(etf_total), 6)
    entry = {
        "partner": row.get("partner"),
        "held_value": None if held is None else round(float(held), 2),
        "account_count": row.get("account_count"),
        "ownership_pct": ownership_pct,
        "source_masters": source_masters,
        "as_of": as_of,
        "state": _derive_state(lag),
        "source_artifact": source_artifact,  # provenance
    }
    flag = _partial_flag(source_masters)
    if flag is not None:
        entry["partial"] = flag
    return entry


def fold_etf_ownership(
    bucket_date: str,
    s3_client=None,
    etf_totals: dict | None = None,
) -> dict:
    """Return {ticker: [held_by_partner entry, ...]} for the 4 Opal ETFs, folded from
    the Opal-side opal-data-etfs/daily series. `etf_totals` (optional) = {ticker:
    etf_total_net_assets} from ~A's ETF cohort rows, for ownership_pct. Pure fold -- no
    DynamoDB write here (see attach_ownership_to_cohort_items)."""
    if s3_client is None:
        import boto3

        s3_client = boto3.client("s3", region_name="us-east-1")
    etf_totals = etf_totals or {}

    out: dict[str, list[dict]] = {t: [] for t in OPAL_ETF_TICKERS}
    for partner in FOLD_PARTNERS:
        rows = _read_partner_daily(partner, bucket_date, s3_client)
        if rows is None:
            continue  # partner series absent -> no entry (cohort-level state=missing upstream)
        for row in rows:
            ticker = str(row.get("etf_ticker", "")).strip().upper()
            if ticker in out:
                out[ticker].append(
                    _ownership_entry(row, bucket_date, etf_totals.get(ticker))
                )
    return out


def attach_ownership_to_cohort_items(cohort_items, ownership_by_ticker):
    """# SUBJECT-TO-~A-EMITTER -- integration stub, NOT the final write.

    ~A's base emitter owns the DynamoDB item shape + the UpdateItem write (PK=cohort,
    SK=bucket_date; first_written_at=if_not_exists(...) + emitted_at=:now per DS note 3).
    This stub shows WHERE the fold attaches: for each ETF cohort item, set the nested
    `ownership` attribute (L of M) to ownership_by_ticker[ticker]. The exact attribute
    name (`ownership` vs `held_by_partner`), the UpdateItem expression, and the item key
    shape are ~A's to finalize -- align before wiring.
    """
    raise NotImplementedError(
        "SUBJECT-TO-~A-EMITTER: attach ownership_by_ticker[ticker] as the ETF cohort "
        "item's nested `ownership` attribute via ~A's UpdateItem write path."
    )


def _main() -> int:
    ap = argparse.ArgumentParser(description="G4 fold dry-run (reads opal-data-etfs; no write)")
    ap.add_argument("--date", required=True, help="bucket_date YYYY-MM-DD")
    args = ap.parse_args()
    folded = fold_etf_ownership(args.date)
    print(json.dumps(folded, indent=2))
    n = sum(len(v) for v in folded.values())
    print(f"OK: {n} ownership entries across {len(folded)} ETFs for {args.date}", flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(_main())
