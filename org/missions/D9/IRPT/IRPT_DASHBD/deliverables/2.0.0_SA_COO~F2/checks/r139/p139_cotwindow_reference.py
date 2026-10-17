"""Reference implementation of cell DB-f-2706 (positive control for p139_cotwindow.py ONLY; applied to the trunk handler, graded, then restored with git checkout).
Usage: python p139_cotwindow_reference.py <repo_root>"""
import sys
from pathlib import Path

H = Path(sys.argv[1], "infra/aws/lambda/investor-reporting/account-return-daily/handler.py")
s = H.read_text(encoding="utf-8")


def sub(old, new):
    global s
    if s.count(old) != 1:
        raise SystemExit("reference: anchor not found exactly once: %r" % old[:70])
    s = s.replace(old, new)


start = s.index("def transaction_frame(s3, reader, day):")
end = s.index("def _transaction_only(event, upload, s3, reader):")
s = s[:start] + '''TX_WINDOW = 14  # the late-posting window: a business day's rows arrive in the partitions D through D+14 trading days


def trading_lag(day, partition):
    """Trading days from `day` to `partition` (0 when equal, -1 when the partition is before the day), counted as the census counts them."""
    d, p = tc._to_date(day), tc._to_date(partition)
    if p < d:
        return -1
    return len(tc.trading_days_between(d, p)) - 1


def window_end_day(day):
    d = tc._to_date(day)
    return tc.trading_days_between(d, d + dt.timedelta(days=60))[TX_WINDOW].isoformat()


def window_complete(day, newest_silver):
    return newest_silver is not None and trading_lag(day, newest_silver) >= TX_WINDOW


def newest_writable_day(newest_silver):
    if newest_silver is None:
        return None
    n = tc._to_date(newest_silver)
    return tc.trading_days_between(n - dt.timedelta(days=60), n)[-1 - TX_WINDOW].isoformat()


def transaction_owed_days(newest_landed, newest_silver, max_days=MAX_DAYS_PER_FIRE):
    w = newest_writable_day(newest_silver)
    if w is None or w < FLOOR_DAY:
        return []
    if newest_landed is None:
        return [w]
    start = max(tc._to_date(newest_landed) + dt.timedelta(days=1), tc._to_date(FLOOR_DAY))
    if start > tc._to_date(w):
        return []
    return [d.isoformat() for d in tc.trading_days_between(start, tc._to_date(w))][:max_days]


def _business_day(raw):
    d = atc._day_of(raw)
    if d is None:
        return None
    b = atc.business_date_with_claim(d, window=atc.PERFORMANCE_DAY_WINDOW)[0]
    return None if b is None else str(b)[:10]


def transaction_frame(s3, reader, day):
    """The deduped rows of business day `day` from the partitions D through D+TX_WINDOW trading days (the CTO's msg 10588 rule)."""
    import pandas as pd
    parts = [p for p in reader.list_partitions("fact_transactions") if 0 <= trading_lag(day, p) <= TX_WINDOW]
    frames = []
    for p in sorted(parts):
        tbl = reader.read_parquet("fact_transactions", p)
        if tbl is not None:
            frames.append(tbl.to_pandas())
    if not frames:
        raise SystemExit("REFUSED: no fact_transactions partition in the window of date=%s" % day)
    frame = pd.concat(frames, ignore_index=True)
    ids = frame["TransactionID"]
    blank = ids.isna() | (ids.astype(str).str.strip() == "")
    if blank.any():
        raise SystemExit("REFUSED: %d row(s) with no TransactionID in the window of date=%s" % (int(blank.sum()), day))
    frame = frame.drop_duplicates(subset="TransactionID", keep="first")
    biz = [_business_day(v) for v in frame["Trade Date"]]
    if any(b is None for b in biz):
        raise SystemExit("REFUSED: %d row(s) in the window of date=%s with no placeable Trade Date" % (sum(1 for b in biz if b is None), day))
    return frame[[b == day for b in biz]]


def _landed_transaction_days(s3):
    uri = atc.opal_naming.address("irpt", cbd.FIRM, "gold", atc.TABLE_TRANSACTION, "date=2000-01-01")
    bucket, key = atc.at.ard._split(uri)
    return landed_days(s3, bucket, key.rsplit("date=", 1)[0])


def _window_info(reader):
    silver = reader.list_partitions("fact_transactions")
    newest = silver[-1] if silver else None
    return {"newest_silver": newest, "newest_writable_day": newest_writable_day(newest)}


def emit_transactions(s3, reader, days, upload):
    """Emit the Cottonwood transaction day of each of `days` once, only when its full window exists. NEVER raises; returns (written, failed)."""
    days = sorted(days)
    firm = cbd.FIRM
    written, failed = {}, {}
    if atc is None:
        failed = {d: "account_transaction_cottonwood not importable (%s)" % ATC_IMPORT_ERROR for d in days}
    else:
        try:
            silver = reader.list_partitions("fact_transactions")
            newest = silver[-1] if silver else None
            landed = set(_landed_transaction_days(s3))
        except Exception as exc:  # noqa: BLE001
            failed = {d: "%s: %s" % (type(exc).__name__, str(exc)[:300]) for d in days}
            days = []
        for day in days:
            if not window_complete(day, newest):
                failed[day] = "window incomplete: the newest silver partition %s is before the %d-trading-day window of %s" % (newest, TX_WINDOW, day)
                continue
            if day in landed:
                failed[day] = "already landed: a transaction day is written once"
                continue
            try:
                frame = transaction_frame(s3, reader, day)
                rows = atc.normalize_trn(frame, firm)
                res = atc.emit_transaction_day(s3, rows, firm, day, upload=upload)
            except (Exception, SystemExit) as exc:  # noqa: BLE001
                failed[day] = "%s: %s" % (type(exc).__name__, str(exc)[:300])
                continue
            written[day] = res["rows"]
            print("  %s transaction rows=%d %s" % (day, res["rows"], "LANDED" if res["landed"] else "DRY"))
    for day in sorted(failed):
        print("  TRANSACTION_SKIPPED %s %s" % (day, failed[day]))
    return written, failed


''' + s[end:]
sub('''    return {"ok": True, "transaction": True, "days": days, "transaction_rows": written, "transaction_failed": failed}''',
    '''    return {"ok": True, "transaction": True, "days": days, "transaction_rows": written, "transaction_failed": failed,
            "transaction_window": _window_info(reader)}''')
sub('''    results, held = _run(s3, reader, days, upload)
    written = [d for d in dict.fromkeys(days) if not results[d].get("held")]
    transaction_written, transaction_failed = emit_transactions(s3, reader, written, upload)
    return {"ok": True, "days": days, "results": results, "held": held, "transaction_rows": transaction_written,
            "transaction_failed": transaction_failed}''',
    '''    scheduled = "day" not in event and "days" not in event
    results, held = _run(s3, reader, days, upload)
    transaction_written, transaction_failed, window = {}, {}, None
    if scheduled:
        window = _window_info(reader)
        tx_bucket_days = _landed_transaction_days(s3) if atc is not None else []
        owed = transaction_owed_days(tx_bucket_days[-1] if tx_bucket_days else None, window["newest_silver"])
        print("OWED_TRANSACTION: newest writable %s, days %s" % (window["newest_writable_day"], owed))
        transaction_written, transaction_failed = emit_transactions(s3, reader, owed, upload)
    return {"ok": True, "days": days, "results": results, "held": held, "transaction_rows": transaction_written,
            "transaction_failed": transaction_failed, "transaction_window": window}''')
H.write_text(s, encoding="utf-8", newline="")
print("reference applied")
