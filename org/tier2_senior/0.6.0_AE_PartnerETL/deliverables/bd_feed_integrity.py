#!/usr/bin/env python3
"""
bd_feed_integrity.py -- multi-day BD feed-integrity watch (ADVI_BREAKS, Andrew-direct 2026-07-01).

WHY: after the 2026-06-30/07-01 freeze-class incidents (allocations $0 stub + the txn-06-29
stale-behind-available silver), Andrew wants the BD feeds watched over several days + LOGGED
EXTENSIVELY -- "i dont fully trust them." This is the durable observability that catches the
freeze-class modes AT THE SOURCE, before they reach a bad serve.

WHAT it checks, per BD raw-fed table (transactions/allocations/realized/unrealized), across the
full raw -> silver -> served chain (holdings is EXCLUDED -- it's a gold canonical for BD, not a
raw feed):
  RAW     latest forwardfill_v2/{table}/*.xlsx  -- LastModified, size, max date-in-content
  SILVER  MAX date-in-content across the recent silver/{table} partitions (NOT the last-modified
          partition -- tonight's freeze had partitions named 06-29 whose CONTENT maxed at 06-26)
  SERVED  platinum/firm/header_metrics.json      -- firm data_as_of + total.aua (once, shared)

FLAGS (the freeze-class taxonomy):
  STALE-BEHIND-AVAILABLE  raw max-date > silver max-date  = the txn-06-29 freeze (silver hasn't
                          ingested a fresher raw the merge already has) -- THE headline freeze.
                          Flagged ONLY when BOTH content dates are known (no false-alert on an
                          ambiguous date column).
  STUB                    raw size < STUB_SIZE_FLOOR       = a header-only/T-1 stub (the alloc $0).
  SILVER-STALE / RAW-STALE  no fresh silver / raw in > STALE_HOURS (a feed going dark).
  EMPTY-SILVER            latest silver partition has 0 rows.
  OK                      raw content-date <= silver content-date, fresh, non-stub.

Read-only. Logs the full state to s3://opal-data-bd/diagnostics/feed_integrity/{run_ts}.json
(durable append-only trail Andrew reviews over the days) AND to stdout (extensive). Exit 1 + an
[ALERT] line on ANY anomaly so a scheduler surfaces it.

Usage:  python bd_feed_integrity.py [--no-s3] [--silver-window N]
Owner: 0.6.0_AE_PartnerETL  Project: ADVI_BREAKS (freeze-class observability)
"""
from __future__ import annotations

import argparse
import io
import json
from datetime import datetime, timezone

import boto3
import pandas as pd

S3_BUCKET = "opal-data-bd"
TABLES = ("transactions", "allocations", "realized", "unrealized")  # holdings = gold canonical, not a raw feed
# per-table preferred date column (fallback = any *_date col with the newest max); normalized
# (lower/strip/spaces->underscores) so raw "Trade Date" and silver "trade_date" both match.
DATE_COL_PREF = {
    "transactions": ("trade_date", "as_of_date"),
    "realized":     ("trade_date", "close_date", "as_of_date"),
    "allocations":  ("as_of_date",),
    "unrealized":   ("as_of_date", "open_date"),
}
STUB_SIZE_FLOOR = 50 * 1024
STALE_HOURS = 30
SILVER_WINDOW = 6            # read content-date across the last N silver partitions (by name)
SERVED_KEY = "platinum/firm/header_metrics.json"

s3 = boto3.client("s3")


def _now():
    return datetime.now(timezone.utc)


def _age_h(lm):
    return round((_now() - lm).total_seconds() / 3600.0, 1) if lm else None


def _norm(h):
    return str(h).strip().lower().replace(" ", "_") if h is not None else ""


def _pick_date_col(cols, table):
    norm = {_norm(c): c for c in cols}
    for pref in DATE_COL_PREF.get(table, ()):  # preferred first
        if pref in norm:
            return norm[pref]
    for k, c in norm.items():                  # else any *_date column
        if k.endswith("date") or k == "date":
            return c
    return None


def _list_all(prefix, suffix):
    out, tok = [], None
    while True:
        kw = {"Bucket": S3_BUCKET, "Prefix": prefix}
        if tok:
            kw["ContinuationToken"] = tok
        resp = s3.list_objects_v2(**kw)
        out += [o for o in resp.get("Contents", []) if o["Key"].endswith(suffix)]
        if resp.get("IsTruncated"):
            tok = resp.get("NextContinuationToken")
        else:
            return out


def _raw_latest(table):
    objs = _list_all(f"forwardfill_v2/{table}/", ".xlsx")
    if not objs:
        return None
    latest = max(objs, key=lambda o: o["LastModified"])
    dt, err = _max_date_xlsx(latest["Key"], table)
    return {"file": latest["Key"].split("/")[-1], "lm": latest["LastModified"],
            "size_kb": round(latest["Size"] / 1024, 1), "max_date": dt, "err": err}


def _silver_state(table, window):
    """MAX content-date across the last `window` silver partitions (by name), latest LastModified,
    latest-partition row count. Correct freeze signal: partitions named 06-29 can contain 06-26."""
    objs = _list_all(f"silver/{table}/", ".parquet")
    if not objs:
        return None
    by_name = sorted(objs, key=lambda o: o["Key"])
    recent = by_name[-window:]
    latest_lm = max(o["LastModified"] for o in objs)
    maxd, rows_latest, errs = None, None, []
    for o in recent:
        d, rows, err = _max_date_parquet(o["Key"], table)
        if err:
            errs.append(err)
        if d and (maxd is None or d > maxd):
            maxd = d
        if o is recent[-1]:
            rows_latest = rows
    return {"latest_partition": by_name[-1]["Key"].split("/")[-1], "lm": latest_lm,
            "max_date": maxd, "rows_latest": rows_latest, "err": (errs[0] if errs else None)}


def _max_date_parquet(key, table):
    try:
        df = pd.read_parquet(io.BytesIO(s3.get_object(Bucket=S3_BUCKET, Key=key)["Body"].read()))
    except Exception as e:
        return None, None, f"read-err {e}"
    col = _pick_date_col(df.columns, table)
    if col is None:
        return None, len(df), "no-date-col"
    try:
        return str(pd.to_datetime(df[col]).max().date()), len(df), None
    except Exception as e:
        return None, len(df), f"date-parse-err {e}"


def _max_date_xlsx(key, table):
    try:
        import openpyxl
        wb = openpyxl.load_workbook(io.BytesIO(s3.get_object(Bucket=S3_BUCKET, Key=key)["Body"].read()),
                                    read_only=True, data_only=True)
        ws = wb["Sheet1"] if "Sheet1" in wb.sheetnames else wb.active
        it = ws.iter_rows(values_only=True)
        hdr = next(it)
        col = _pick_date_col(hdr, table)
        if col is None:
            wb.close()
            return None, "no-date-col"
        idx = list(hdr).index(col)
        mx = None
        for r in it:
            if idx < len(r) and r[idx] is not None:
                v = r[idx]
                if isinstance(v, datetime):
                    v = v.date()
                elif not hasattr(v, "year"):
                    try:
                        v = pd.to_datetime(str(v)).date()
                    except Exception:
                        continue
                mx = v if mx is None else max(mx, v)
        wb.close()
        return (str(mx) if mx else None), None
    except Exception as e:
        return None, f"xlsx-err {e}"


def check_table(table):
    raw = _raw_latest(table)
    sil = _silver_state(table, SILVER_WINDOW)
    flags = []
    if raw is None:
        flags.append("RAW-MISSING")
    elif raw["size_kb"] * 1024 < STUB_SIZE_FLOOR:
        flags.append("STUB")
    if raw and _age_h(raw["lm"]) and _age_h(raw["lm"]) > STALE_HOURS:
        flags.append("RAW-STALE")
    if sil is None:
        flags.append("SILVER-MISSING")
    else:
        if _age_h(sil["lm"]) and _age_h(sil["lm"]) > STALE_HOURS:
            flags.append("SILVER-STALE")
        if sil.get("rows_latest") == 0:
            flags.append("EMPTY-SILVER")
    if raw and sil and raw["max_date"] and sil["max_date"] and raw["max_date"] > sil["max_date"]:
        flags.append("STALE-BEHIND-AVAILABLE")
    return {"table": table, "raw": raw, "silver": sil, "flags": flags or ["OK"]}


def _fmt_dt(lm):
    return lm.strftime("%Y-%m-%dT%H:%M:%SZ") if lm else None


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--no-s3", action="store_true")
    ap.add_argument("--silver-window", type=int, default=SILVER_WINDOW)
    args = ap.parse_args(argv)
    ts = _now().strftime("%Y-%m-%dT%H:%M:%SZ")
    print("=" * 82)
    print("BD FEED INTEGRITY WATCH  %s  (ADVI_BREAKS; Andrew multi-day watch)" % ts)
    print("=" * 82)
    try:
        d = json.loads(s3.get_object(Bucket=S3_BUCKET, Key=SERVED_KEY)["Body"].read())
        served = {"data_as_of": d.get("data_as_of"), "total_aua": d.get("total", {}).get("aua"),
                  "account_count": d.get("total", {}).get("account_count")}
    except Exception as e:
        served = {"err": str(e)}
    print("SERVED firm: data_as_of=%s  total.aua=%s  accounts=%s"
          % (served.get("data_as_of"), served.get("total_aua"), served.get("account_count")))
    print("-" * 82)
    rows, alerts = [], []
    for t in TABLES:
        r = check_table(t)
        raw, sil = r["raw"], r["silver"]
        print("[%-13s] flags=%s" % (t, ",".join(r["flags"])))
        print("    RAW    %s" % (("%s  lastmod=%s (%sh)  %.1fMB  max_date=%s%s"
              % (raw["file"], _fmt_dt(raw["lm"]), _age_h(raw["lm"]), raw["size_kb"] / 1024, raw["max_date"],
                 "  [%s]" % raw["err"] if raw.get("err") else "")) if raw else "MISSING"))
        print("    SILVER %s" % (("latest=%s  lastmod=%s (%sh)  rows=%s  max_date(win%d)=%s%s"
              % (sil["latest_partition"], _fmt_dt(sil["lm"]), _age_h(sil["lm"]), sil["rows_latest"],
                 args.silver_window, sil["max_date"], "  [%s]" % sil["err"] if sil.get("err") else "")) if sil else "MISSING"))
        # serialize LastModified for the S3 log
        r_log = dict(r)
        for part in ("raw", "silver"):
            if r_log.get(part):
                r_log[part] = {**r_log[part], "lm": _fmt_dt(r_log[part]["lm"])}
        rows.append(r_log)
        if r["flags"] != ["OK"]:
            alerts.append("%s=%s" % (t, ",".join(r["flags"])))
    print("-" * 82)
    overall = "CLEAN" if not alerts else "ANOMALY"
    if alerts:
        print("[ALERT] freeze-class/feed anomalies: %s" % "; ".join(alerts))
    print("OVERALL: %s" % overall)
    log = {"run_ts": ts, "overall": overall, "served": served, "tables": rows, "alerts": alerts,
           "thresholds": {"stub_size_floor_kb": STUB_SIZE_FLOOR // 1024, "stale_hours": STALE_HOURS,
                          "silver_window": args.silver_window},
           "producer": "bd_feed_integrity.py"}
    if not args.no_s3:
        key = "diagnostics/feed_integrity/%s.json" % ts.replace(":", "").replace("-", "")
        try:
            s3.put_object(Bucket=S3_BUCKET, Key=key, Body=json.dumps(log, indent=2, default=str).encode(),
                          ContentType="application/json")
            print("log -> s3://%s/%s" % (S3_BUCKET, key))
        except Exception as e:
            print("WARN: S3 log write failed: %s" % e)
    return 1 if alerts else 0


if __name__ == "__main__":
    raise SystemExit(main())
