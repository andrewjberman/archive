"""OPAL_ASSETS G4 -- build_ownership_rows extension (DROP-IN for ~A's emitter).

Author: 0.8.0_AE_CloudComp | 2026-07-13 | STATUS: PROPOSAL -- pair with 0.7.0~A
(emitter owner) + CTO~B (schema) BEFORE editing the live emitter / safe-apply.

Extends infra/aws/lambda/opal-assets/opal-assets-daily-emitter/lambda_function.py.
Keeps ~A's build_rows() PURE; this is a SIBLING function that does the one extra S3
read (opal-data-etfs/daily), called alongside build_rows in lambda_handler + backfill.

SHAPE DECISION (proposed): per-(ETF, partner) ownership as ADDITIONAL ROWS -- fits the
flat schema + the cohort_history GSI + "map straight in". The 14 BASE cohort rows are
UNCHANGED (DS census-14 invariant intact for the base dimension); ownership rows are an
additive dimension keyed by value_class="etf_ownership_held".

IAM DELTA (add to emitter.tf aws_iam_role_policy.emitter -- the ONLY new grant; write
already covers the table, Rule-22a pre-checked: opal-data-etfs read = implicitDeny today,
mdpf read = allowed positive control):
    { Sid="ReadEtfsOwnershipDaily", Effect="Allow", Action="s3:GetObject",
      Resource="arn:aws:s3:::opal-data-etfs/daily/*" },
    { Sid="ListEtfsOwnershipDaily", Effect="Allow", Action="s3:ListBucket",
      Resource="arn:aws:s3:::opal-data-etfs",
      Condition={ StringLike={ "s3:prefix"=["daily/*"] } } }
"""
from __future__ import annotations

import json

# cohort_id <-> ticker (mirrors ~A's COHORTS etf entries).
_ETF_COHORT_BY_TICKER = {
    "DIVZ": "etf_divz", "IDVZ": "etf_idvz", "PFOE": "etf_pfoe", "PFDE": "etf_pfde",
}
_ETFS_BUCKET = "opal-data-etfs"
# Partners whose per-partner ETF-ownership series we fold. Cottonwood is ONE-WAY
# (PRD 3e). All read Opal-side opal-data-etfs -- ZERO sovereign read.
_FOLD_PARTNERS = ("49financial", "inflection", "cottonwood")


def _etf_totals(body: dict) -> dict:
    """{ticker: etf_total_net_assets} straight off the served body already in build_rows
    -- so ownership_pct needs NO new source read."""
    out = {}
    for e in body.get("etf_decomposition", []) or []:
        t = e.get("ticker")
        if t is not None:
            out[str(t)] = e.get("etf_total_net_assets")
    return out


def _source_masters(source_artifact: str) -> list:
    """LIST from day 1. 49F RPS = the 08242234 book; inflection (opal-data-inf) +
    cottonwood are fund/model-level -> []. At P2 the 49F entry gains 08335338 (value
    change, no schema migration)."""
    sa = (source_artifact or "").lower()
    if "schwab/silver/rps" in sa or "08242234" in sa:
        return ["08242234"]
    return []


def _latest_partner_key(s3, partner: str, run_date: str):
    prefix = "daily/" + partner + "/"
    latest_key, latest_ds = None, None
    token = None
    while True:
        kw = {"Bucket": _ETFS_BUCKET, "Prefix": prefix}
        if token:
            kw["ContinuationToken"] = token
        resp = s3.list_objects_v2(**kw)
        for it in resp.get("Contents", []):
            base = it["Key"].rsplit("/", 1)[-1]
            if not base.endswith(".json"):
                continue
            ds = base[:-len(".json")]
            if len(ds) == len("YYYY-MM-DD") and ds <= run_date:
                if latest_ds is None or ds > latest_ds:
                    latest_ds, latest_key = ds, it["Key"]
        if resp.get("IsTruncated"):
            token = resp.get("NextContinuationToken")
        else:
            break
    return latest_key


def build_ownership_rows(body: dict, run_date: str, s3, trading_days_behind) -> list:
    """Per-(ETF, partner) held-ownership rows from the Opal-side opal-data-etfs/daily
    series. `trading_days_behind` is ~A's function (passed in so the staleness matches
    the base rows + G6 exactly -- no re-derivation). ZERO sovereign read (opal-data-etfs
    only). Returns [] if no partner series is present (never a fake row)."""
    totals = _etf_totals(body)
    gen = body.get("generated_at") or ""
    rows = []
    for partner in _FOLD_PARTNERS:
        key = _latest_partner_key(s3, partner, run_date)
        if key is None:
            continue  # partner series absent -> no ownership row (honest absence)
        recs = json.loads(s3.get_object(Bucket=_ETFS_BUCKET, Key=key)["Body"].read())
        if not isinstance(recs, list):
            recs = [recs]
        for rec in recs:
            ticker = str(rec.get("etf_ticker", "")).strip().upper()
            etf_cohort = _ETF_COHORT_BY_TICKER.get(ticker)
            if etf_cohort is None:
                continue
            as_of = str(rec.get("source_as_of") or rec.get("date") or "")
            held = rec.get("ownership_value")
            masters = _source_masters(str(rec.get("source_artifact", "")))
            staleness = trading_days_behind(as_of, run_date) if as_of else 99
            state = "missing" if not as_of else ("fresh" if staleness == 0 else "rolled_forward")
            etf_total = totals.get(ticker)
            pct = None
            if held is not None and etf_total not in (None, 0):
                pct = round(float(held) / float(etf_total), 6)
            row = {
                "run_date": run_date,
                "cohort_id": etf_cohort + "__held_" + partner,
                "cohort_name": ticker + " held by " + partner,
                "value": None if held is None else round(float(held), 2),
                "as_of": as_of or None,
                "as_of_basis": "etfs_daily_source_as_of",
                "state": state,
                "staleness": staleness,
                "source_masters": masters,
                "value_class": "etf_ownership_held",
                "source_field": "opal-data-etfs/daily/" + partner + "[" + ticker + "].ownership_value",
                "ownership_pct": pct,
                "account_count": rec.get("account_count"),
                "generated_at": gen,
            }
            # Interim undercount disclosure -- absence of this field == G4 DONE (both-masters).
            if masters == ["08242234"]:
                row["partial"] = "08242234-only"
            rows.append(row)
    return rows


# CALL-SITE CHANGES (in ~A's lambda_function.py) -- proposed:
#   lambda_handler():   rows = build_rows(body, run_date) + build_ownership_rows(body, run_date, s3, trading_days_behind)
#   __main__ backfill:  rows = build_rows(body, rd) + build_ownership_rows(body, rd, s3, trading_days_behind)
# (build_rows stays PURE; the S3 read lives only in build_ownership_rows.)
