"""IRPT_DASHBD round 139, workstream F-SHIP ~F2 (issuer 2.0.0_SA_COO~F2) -- the Cottonwood transaction stage reads the LATE-POSTING WINDOW (cell DB-f-2706).

  The CTO's msgs 10588, 10592, 10597. The Cottonwood fact_transactions silver is a rolling 14-day period pull: a business day's rows repeat across about ten partitions and arrive in the
  partitions D through D+14 trading days. The stage must read that window, keep the rows whose business date is D, dedup on TransactionID, and write a day ONCE, only when its full window
  exists. The handler's API (names are the spec; `tc` is lib/trading_calendar, lag = trading days from D to the partition, counted as the census counts them):
    TX_WINDOW = 14;  window_end_day(day) -> ISO of the D+14th trading day;  window_complete(day, newest_silver) -> bool (lag(day, newest) >= 14);
    newest_writable_day(newest_silver) -> ISO (the trading day 14 trading days before the last trading day on or before newest_silver);
    transaction_owed_days(newest_landed, newest_silver, max_days=MAX_DAYS_PER_FIRE) -> list (nothing before FLOOR_DAY; [newest writable] when nothing landed);
    transaction_frame(s3, reader, day) -> a frame of the DEDUPED rows of business day `day` read from the window partitions only;
    emit_transactions(s3, reader, days, upload) -> (written, failed): an incomplete window or an already landed day is NOT written and is named in `failed`.
  The scheduled fire runs the stage on transaction_owed_days (not on the returns days); day, days and rewrite events never run it; results carry `transaction_window`.

  DBF139-6-AC1  the window primitives and the reader (dedup, window bounds, late row at lag 14 kept, lag 15 excluded, other business days excluded, blank id refused)
  DBF139-6-AC2  owed days and the stage (full window only, once, dry run writes nothing, an already landed day is not rewritten)
  DBF139-6-AC3  the wiring (scheduled fire on its own owed days, day/days/rewrite never run it, the window reported), the function's tests directory green, and the function-map entry
                re-pinned to the edited files (the round-138 bundle criteria DBF138-6-AC1 to AC3 still PASS)

Usage: python <this file> <repo_root> <criterion_id>      prints "<id> PASS" or "<id> FAIL" last
       python <this file> --selftest                        the pure helpers on synthetic arms
"""
import datetime as dt
import importlib.util
import subprocess
import sys
from pathlib import Path

HANDLER = "infra/aws/lambda/investor-reporting/account-return-daily/handler.py"
TESTS = "infra/aws/lambda/investor-reporting/account-return-daily/tests"
D = "2026-08-19"          # a Wednesday; its D+14th trading day is 2026-09-09 (Labor Day 2026-09-07 is a holiday)
END = "2026-09-09"
SPILL = "2026-09-10"       # lag 15
NEWEST_WRITABLE = "2026-08-28"  # the synthetic silver ends 2026-09-18 (a Friday); 14 trading days before it
INCOMPLETE = "2026-09-08"       # its D+14th trading day (2026-09-28) is after the silver's newest partition
LATE_ID = "D011"
IDS = ["D%03d" % i for i in range(1, 11)]


class Fail(Exception):
    pass


def need(cond, msg):
    if not cond:
        raise Fail(msg)


def mmddyyyy(iso):
    y, m, d = iso.split("-")
    return "%s/%s/%s" % (m, d, y)


def load(root):
    sys.path.insert(0, str(Path(root, HANDLER).parent))
    for n in ("handler",):
        sys.modules.pop(n, None)
    spec = importlib.util.spec_from_file_location("handler", str(Path(root, HANDLER)))
    mod = importlib.util.module_from_spec(spec)
    sys.modules["handler"] = mod
    spec.loader.exec_module(mod)
    return mod


def row(pd, atc, tid, trade_iso, portfolio="P1"):
    rec = {c: None for c in atc.SOURCE_COLUMNS + atc._fee_columns(atc.load_words())}
    rec.update({"AccountID": "A0000000001", "Trade Date": mmddyyyy(trade_iso), "Settle Date": mmddyyyy(trade_iso), "Transaction Type": "Trade",
                "Transaction Sub Type": "Buy", "External Flow": "None", "Units": 1.0, "Price": 10.0, "Market Value": 10.0, "Symbol": "ABC",
                "Asset Name": "Abc", "Custodian": "X", "TransactionID": tid, "PortfolioID": portfolio, "Portfolio Name": "Name " + portfolio})
    return rec


class Silver(object):
    """A synthetic silver: every calendar day from D to D+30 is a partition. Day D's rows: ids D001..D010 (the first six at lags 0 and 1, all ten from lag 2), a LATE id at lag 14
    (the D+14th trading day), a SPILL id first seen at lag 15, a duplicated line (same id, another portfolio) at lag 2, and rows of other business days in every partition."""

    def __init__(self, h, with_blank=False):
        import pandas as pd
        import pyarrow as pa
        self.h, self.pd, self.pa, self.reads = h, pd, pa, []
        tc = h.tc
        self.days = [(dt.date.fromisoformat(D) + dt.timedelta(days=i)).isoformat() for i in range(0, 31)]
        self.frames = {}
        for p in self.days:
            lag = h.trading_lag(D, p)
            rows = []
            if lag >= 0:
                n = 6 if lag <= 1 else 10
                for tid in IDS[:n]:
                    rows.append(row(pd, h.atc, tid, D))
                if lag == 2:
                    rows.append(row(pd, h.atc, IDS[2], D, portfolio="P2"))
                if lag == 14:
                    rows.append(row(pd, h.atc, LATE_ID, D))
                if lag == 15:
                    rows.append(row(pd, h.atc, "D012", D))
                if with_blank and lag == 5:
                    rows.append(row(pd, h.atc, "", D))
                other = str(tc.trading_days_between(dt.date.fromisoformat(D), dt.date.fromisoformat(D) + dt.timedelta(days=10))[1])[:10]
                rows.append(row(pd, h.atc, "E%s" % p, other))
            self.frames[p] = pd.DataFrame(rows) if rows else None

    def list_partitions(self, table):
        return sorted(self.days)

    def read_parquet(self, table, day):
        self.reads.append(day)
        f = self.frames.get(day)
        return None if f is None else self.pa.Table.from_pandas(f, preserve_index=False)


class FakeS3(object):
    def __init__(self, existing=()):
        self.puts, self.existing = [], list(existing)

    def put_object(self, Bucket, Key, Body, **kw):
        self.puts.append(Key)
        return {}

    def list_objects_v2(self, **kw):
        keys = sorted(k for k in self.existing + self.puts if k.startswith(kw["Prefix"]))
        if kw.get("Delimiter"):
            seen = sorted({kw["Prefix"] + k[len(kw["Prefix"]):].split("/", 1)[0] + "/" for k in keys})
            return {"CommonPrefixes": [{"Prefix": s} for s in seen], "IsTruncated": False, "KeyCount": len(seen)}
        return {"KeyCount": len(keys), "Contents": [{"Key": k} for k in keys], "IsTruncated": False}


def landed_key(h, day):
    uri = h.atc.opal_naming.address("irpt", h.atc.FIRM, "gold", h.atc.TABLE_TRANSACTION, "date=%s" % day)
    bucket, key = h.atc.at.ard._split(uri)
    return key + "/data.parquet"


class Recorder(object):
    """Replaces the producer's writer: the real validation runs (upload=False), the call is recorded."""

    def __init__(self, h):
        self.h, self.calls, self.real = h, [], h.atc.emit_transaction_day

    def __call__(self, s3, rows, firm, day, *, upload):
        res = self.real(s3, rows, firm, day, upload=False)
        self.calls.append((day, len(rows), upload))
        return {"address": res["address"], "rows": len(rows), "landed": bool(upload)}


def ac1(root):
    h = load(root)
    for name in ("TX_WINDOW", "trading_lag", "window_end_day", "window_complete", "newest_writable_day", "transaction_frame"):
        need(hasattr(h, name), "the handler must define %s" % name)
    need(h.TX_WINDOW == 14, "TX_WINDOW must be 14")
    need(h.window_end_day(D) == END, "window_end_day(%s) must be %s (got %s)" % (D, END, h.window_end_day(D)))
    need(h.window_complete(D, END) and not h.window_complete(D, "2026-09-08"), "window_complete must turn true exactly at the D+14th trading day's partition")
    need(h.window_complete("2026-08-21", "2026-09-12"), "a Saturday partition after the 14th trading day completes the window")
    need(h.newest_writable_day(END) == D and h.newest_writable_day("2026-09-12") == "2026-08-21",
         "newest_writable_day(%s) must be %s and of 2026-09-12 must be 2026-08-21 (got %s, %s)" % (END, D, h.newest_writable_day(END), h.newest_writable_day("2026-09-12")))
    silver = Silver(h)
    frame = h.transaction_frame(FakeS3(), silver, D)
    ids = sorted(str(v) for v in frame["TransactionID"].tolist())
    need(ids == sorted(IDS + [LATE_ID]), "the frame must hold exactly the %d distinct ids of business day %s (the late id at lag 14 included, the lag 15 id and other days excluded); got %d rows: %s"
         % (len(IDS) + 1, D, len(ids), ids[:14]))
    over = [p for p in silver.reads if not 0 <= h.trading_lag(D, p) <= 14]
    need(not over, "the reader read partitions outside the window: %s" % over[:3])
    need(SPILL not in silver.reads, "the lag 15 partition must not be read")
    try:
        h.transaction_frame(FakeS3(), Silver(h, with_blank=True), D)
        raise Fail("a blank TransactionID in the window must REFUSE")
    except SystemExit as e:
        need("TransactionID" in str(e), "the refusal must name TransactionID: %r" % str(e)[:120])


def ac2(root):
    h = load(root)
    for name in ("transaction_owed_days", "emit_transactions", "newest_writable_day"):
        need(hasattr(h, name), "the handler must define %s" % name)
    need(h.transaction_owed_days(None, END) == [D], "nothing landed: exactly the newest writable day, got %r" % (h.transaction_owed_days(None, END),))
    need(h.transaction_owed_days("2026-08-14", END) == ["2026-08-17", "2026-08-18", D], "owed days after a landed day: %r" % (h.transaction_owed_days("2026-08-14", END),))
    need(h.transaction_owed_days("2026-08-14", END, max_days=2) == ["2026-08-17", "2026-08-18"], "the per-fire cap applies, oldest first")
    need(h.transaction_owed_days(D, END) == [], "nothing is owed when the newest writable day is landed")
    need(h.transaction_owed_days(None, "2026-07-20") == [], "nothing before FLOOR_DAY is owed")
    silver = Silver(h)
    rec = Recorder(h)
    h.atc.emit_transaction_day = rec
    try:
        written, failed = h.emit_transactions(FakeS3(), silver, [D], True)
        need(written == {D: len(IDS) + 1} and not failed, "a full window writes the day once with %d deduped rows: written %r failed %r" % (len(IDS) + 1, written, failed))
        w2, f2 = h.emit_transactions(FakeS3(), silver, [INCOMPLETE], True)
        need(INCOMPLETE in f2 and "window" in f2[INCOMPLETE].lower() and not w2, "an incomplete window is not written and says so: %r" % (f2,))
        w3, f3 = h.emit_transactions(FakeS3(existing=[landed_key(h, D)]), silver, [D], True)
        need(D in f3 and "already" in f3[D].lower() and not w3, "an already landed day is not rewritten and says so: %r" % (f3,))
        before = len(rec.calls)
        w4, f4 = h.emit_transactions(FakeS3(), silver, [D], False)
        need(w4 == {D: len(IDS) + 1} and rec.calls[before][2] is False, "a dry run passes upload False to the producer")
    finally:
        h.atc.emit_transaction_day = rec.real


def ac3(root):
    h = load(root)
    silver = Silver(h)
    rec = Recorder(h)
    h.atc.emit_transaction_day = rec
    calls = {"stage": []}
    real_emit = h.emit_transactions
    h.emit_transactions = lambda s3, reader, days, upload: (calls["stage"].append(list(days)), real_emit(s3, reader, days, upload))[1]
    h._run = lambda s3, reader, days, upload, rewrite=False: ({d: {"held": False} for d in days}, 0)
    h.owed_days = lambda newest, today, max_days=5: ["2026-09-08"]
    h.cbd.gold_prefix = lambda: ("bucket", "returns/")
    try:
        out = h.lambda_handler({}, s3=FakeS3(), reader=silver)
        need(calls["stage"] and calls["stage"][-1] == [NEWEST_WRITABLE], "the scheduled fire must run the stage on transaction_owed_days (%s), not on the returns days: %r" % (NEWEST_WRITABLE, calls["stage"]))
        need(isinstance(out.get("transaction_window"), dict) and out["transaction_window"].get("newest_writable_day") == NEWEST_WRITABLE,
             "the result must report transaction_window with newest_writable_day: %r" % (out.get("transaction_window"),))
        for ev in ({"day": "2026-09-08"}, {"days": ["2026-09-08"]}):
            calls["stage"].clear()
            h.lambda_handler(ev, s3=FakeS3(), reader=silver)
            need(not calls["stage"], "a %s event must not run the transaction stage" % list(ev)[0])
        calls["stage"].clear()
        h._rewrite = lambda event, upload, s3, reader: {"ok": True, "rewrite": True}
        h.lambda_handler({"rewrite": {}}, s3=FakeS3(), reader=silver)
        need(not calls["stage"], "a rewrite event must not run the transaction stage")
        out = h.lambda_handler({"transaction": {"start": D, "end": D}, "dry_run": True}, s3=FakeS3(), reader=silver)
        need(isinstance(out.get("transaction_window"), dict), "the transaction event must report transaction_window")
    finally:
        h.atc.emit_transaction_day = rec.real
    r = subprocess.run([sys.executable, "-m", "pytest", str(Path(root, TESTS)), "-q", "-p", "no:cacheprovider"], capture_output=True, text=True, timeout=900, cwd=str(root))
    tail = (r.stdout or r.stderr or "").strip().splitlines()[-1:] or [""]
    need(r.returncode == 0, "the function's tests directory must be green: %s" % tail[0][:160])
    bundle = str(Path(root, "org/missions/D9/IRPT/IRPT_DASHBD/deliverables/2.0.0_SA_COO~F2/checks/r138/p138_cotbundle.py"))
    for crit in ("DBF138-6-AC1", "DBF138-6-AC2", "DBF138-6-AC3"):
        b = subprocess.run([sys.executable, "-I", bundle, root, crit], capture_output=True, text=True, timeout=900, cwd=root)
        last = ((b.stdout or "").strip().splitlines() or [""])[-1]
        need(last == "%s PASS" % crit, "the function-map entry must still pin the files it packages (%s): %s" % (crit, last[:140]))


def selftest():
    bad = count = 0

    def arm(name, got, want):
        nonlocal bad, count
        count += 1
        if got != want:
            bad += 1
            print("SELFTEST FAIL %s: got %r want %r" % (name, got, want))

    arm("mmddyyyy", mmddyyyy("2026-08-19"), "08/19/2026")
    arm("ids", len(IDS), 10)
    arm("end-after-d", END > D, True)
    arm("spill-after-end", SPILL > END, True)
    s = FakeS3(existing=["a/date=2026-08-19/data.parquet", "a/date=2026-08-20/data.parquet", "b/date=2026-08-21/data.parquet"])
    arm("fake-list", [c["Prefix"] for c in s.list_objects_v2(Prefix="a/", Delimiter="/")["CommonPrefixes"]], ["a/date=2026-08-19/", "a/date=2026-08-20/"])
    print("selftest %s" % ("FAIL" if bad else "PASS (%d arms)" % count))
    return 1 if bad else 0


def main(argv):
    if len(argv) == 2 and argv[1] == "--selftest":
        return selftest()
    if len(argv) != 3 or argv[2] not in ("DBF139-6-AC1", "DBF139-6-AC2", "DBF139-6-AC3"):
        print("usage: p139_cotwindow.py <repo_root> DBF139-6-AC1|AC2|AC3 | --selftest")
        return 2
    root = str(Path(argv[1]).resolve())
    try:
        {"DBF139-6-AC1": ac1, "DBF139-6-AC2": ac2, "DBF139-6-AC3": ac3}[argv[2]](root)
    except Fail as e:
        print("reason: %s" % e)
        print("%s FAIL" % argv[2])
        return 1
    except SystemExit as e:
        print("reason: the code refused: %s" % (str(e)[:200],))
        print("%s FAIL" % argv[2])
        return 1
    except Exception as e:  # noqa: BLE001
        print("reason: %s: %s" % (type(e).__name__, e))
        print("%s FAIL" % argv[2])
        return 1
    print("%s PASS" % argv[2])
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
