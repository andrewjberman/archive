"""IRPT_DASHBD round 137, workstream F-SHIP ~F2 (issuer 2.0.0_SA_COO~F2) -- FWD-5: the COTTONWOOD LANDING HANDLER EMITS THE TRANSACTION DAY (cell DB-f-2301).

  Host ruled by the CTO (XA-20261016T224156Z-3c21, msg 10002): `infra/aws/lambda/investor-reporting/account-return-daily/handler.py`, never the filled-report function.
  The handler imports `account_transaction_cottonwood` GUARDED (`atc`, `ATC_IMPORT_ERROR`); `transaction_frame(s3, reader, day)` reads the day's Black Diamond fact_transactions
  partition through the adapter's silver reader; `emit_transactions(s3, reader, days, upload)` runs the producer's `normalize_trn` then `emit_transaction_day` per day and NEVER
  raises (CTO added condition ii: a failed or planted-failing stage leaves the day's returns byte-equal, with a test). The scheduled/day/days path calls it once, AFTER the
  returns days are written, for the written (not held) days; a transaction-only event `{"transaction": {"start", "end"}}` runs the stage alone; the rewrite path never calls it.
  DBF137-2-AC1 (the emission function and the event routes), DBF137-2-AC2 (the wiring and the planted failure), DBF137-2-AC3 (the tests)

Usage: python <this file> <repo_root> <criterion_id>      prints "<id> PASS" or "<id> FAIL" last
       python <this file> --selftest                        the pure helpers on synthetic arms
"""
import ast
import json
import re
import subprocess
import sys
from pathlib import Path

HANDLER = "infra/aws/lambda/investor-reporting/account-return-daily/handler.py"
TESTS_DIR = "infra/aws/lambda/investor-reporting/account-return-daily/tests"
NEW_TESTS = TESTS_DIR + "/test_transaction_emission.py"
NAME_WORDS = ("guarded", "import", "emit", "skipped", "never", "upload", "dry", "held", "planted", "byte", "order", "rewrite", "transaction_only", "floor")

BEHAVIOUR = r'''
import io, json, sys
from contextlib import redirect_stdout
from unittest import mock
sys.path.insert(0, sys.argv[1])
import pandas as pd
import handler as h

DAYS = ["2026-10-13", "2026-10-14", "2026-10-15"]

def frame(day, n):
    return pd.DataFrame([{"Trade Date": day, "k": i} for i in range(n)])

class Atc:
    def __init__(self, bad_normalize=(), bad_emit=()):
        self.calls = []
        self.bad_normalize, self.bad_emit = set(bad_normalize), set(bad_emit)
    def normalize_trn(self, fr, firm):
        d = str(fr.iloc[0]["Trade Date"])
        if d in self.bad_normalize:
            raise SystemExit("REFUSED: a refused line")
        return [{"d": d}] * len(fr)
    def emit_transaction_day(self, s3, rows, firm, day, *, upload):
        if day in self.bad_emit:
            raise ValueError("boom")
        self.calls.append((day, len(rows), upload))
        return {"rows": len(rows), "landed": upload}

sizes = {"2026-10-13": 3, "2026-10-14": 2, "2026-10-15": 4}
out = {}

def quiet():
    return redirect_stdout(io.StringIO())

with mock.patch.object(h, "transaction_frame", lambda s3, reader, day: frame(day, sizes[day])):
    a = Atc()
    with mock.patch.object(h, "atc", a), quiet():
        w, f = h.emit_transactions(None, None, DAYS[:2], True)
    out["green"] = [w, f, a.calls]
    a = Atc(bad_normalize={"2026-10-14"})
    buf = io.StringIO()
    with mock.patch.object(h, "atc", a), redirect_stdout(buf):
        w, f = h.emit_transactions(None, None, DAYS, True)
    out["refused_day"] = [w, sorted(f), "TRANSACTION_SKIPPED 2026-10-14" in buf.getvalue()]
    a = Atc(bad_emit={"2026-10-13"})
    with mock.patch.object(h, "atc", a), quiet():
        w, f = h.emit_transactions(None, None, [DAYS[0], DAYS[2]], False)
    out["emit_raises"] = [w, sorted(f), "ValueError" in f["2026-10-13"], a.calls]
    with mock.patch.object(h, "atc", None), mock.patch.object(h, "ATC_IMPORT_ERROR", "ImportError: x"), quiet():
        w, f = h.emit_transactions(None, None, DAYS[:2], True)
    out["not_importable"] = [w, sorted(f), all("ImportError: x" in v for v in f.values())]
    with mock.patch.object(h, "atc", Atc()), quiet():
        out["empty_days"] = list(h.emit_transactions(None, None, [], True))

    # the transaction-only event: only the stage runs; run_day is never called; upload follows dry_run; the range is validated
    def tx_event(ev):
        a2 = Atc()
        run_day = mock.Mock()
        try:
            with mock.patch.object(h, "atc", a2), mock.patch.object(h.cbd, "run_day", run_day), quiet():
                r = h.lambda_handler(ev, s3=object(), reader=object())
            return [r.get("transaction_rows"), r.get("transaction_failed"), run_day.call_count, [c[2] for c in a2.calls]]
        except (ValueError, SystemExit) as e:
            return "REFUSED:" + type(e).__name__
    out["tx_event"] = tx_event({"transaction": {"start": "2026-10-13", "end": "2026-10-15"}})
    out["tx_event_dry"] = tx_event({"transaction": {"start": "2026-10-14", "end": "2026-10-14"}, "dry_run": True})
    out["tx_before_floor"] = tx_event({"transaction": {"start": "2026-07-01", "end": "2026-07-02"}})
    out["tx_extra_key"] = tx_event({"transaction": {"start": "2026-10-13", "end": "2026-10-15", "x": 1}})
    out["tx_with_day"] = tx_event({"transaction": {"start": "2026-10-13", "end": "2026-10-15"}, "day": "2026-10-15"})
    out["tx_too_long"] = tx_event({"transaction": {"start": "2026-08-03", "end": "2026-10-15"}})
    out["tx_start_after_end"] = tx_event({"transaction": {"start": "2026-10-15", "end": "2026-10-13"}})

    # the scheduled/day path: the stage runs AFTER run_day for the written days only, and a planted failure leaves the returns result byte-equal
    def day_event(ev, atc_obj, held=()):
        order = []
        def run_day(reader, s3, day, **kw):
            order.append(("run_day", day))
            return {"held": True, "reason": "HOLD %s: x" % day} if day in held else {"rows": 5, "day": day}
        real = h.emit_transactions
        def spy(s3, reader, days, upload):
            order.append(("emit", tuple(days), upload))
            return real(s3, reader, days, upload)
        with mock.patch.object(h, "atc", atc_obj), mock.patch.object(h.cbd, "run_day", run_day), mock.patch.object(h, "emit_transactions", spy), quiet():
            r = h.lambda_handler(ev, s3=object(), reader=object())
        return r, order
    good, order = day_event({"days": ["2026-10-14", "2026-10-15"]}, Atc())
    out["day_order"] = [order, good.get("transaction_rows"), good.get("transaction_failed")]
    held_r, held_order = day_event({"days": ["2026-10-14", "2026-10-15"]}, Atc(), held=("2026-10-15",))
    out["held_day"] = [held_order[-1], held_r.get("transaction_rows"), sorted(held_r.get("transaction_failed", {}))]
    planted, _o = day_event({"days": ["2026-10-14", "2026-10-15"]}, Atc(bad_normalize={"2026-10-14", "2026-10-15"}))
    keep = ["ok", "days", "results", "held"]
    out["planted_returns_equal"] = json.dumps({k: good[k] for k in keep}, sort_keys=True) == json.dumps({k: planted[k] for k in keep}, sort_keys=True)
    out["planted_failed"] = sorted(planted.get("transaction_failed", {}))
    # a rewrite event never runs the stage
    called = []
    with mock.patch.object(h, "emit_transactions", lambda *a, **k: called.append(1) or ({}, {})), mock.patch.object(h.cbd, "run_day", mock.Mock(return_value={"rows": 1})), \
            mock.patch.object(h, "landed_days", lambda s3, b, p: ["2026-10-14"]), mock.patch.object(h.cbd, "gold_prefix", lambda: ("b", "p/")), quiet():
        try:
            h.lambda_handler({"rewrite": {"start": "2026-10-14", "end": "2026-10-14"}}, s3=object(), reader=object())
        except Exception as e:
            called.append("raised:" + type(e).__name__)
    out["rewrite_calls"] = [c for c in called if c == 1]
print("RESULT " + json.dumps(out, sort_keys=True))
'''


class Fail(Exception):
    pass


def need(cond, msg):
    if not cond:
        raise Fail(msg)


def behaviour_problems(r):
    pr = []
    if r.get("green") != [{"2026-10-13": 3, "2026-10-14": 2}, {}, [["2026-10-13", 3, True], ["2026-10-14", 2, True]]]:
        pr.append("emit_transactions must write each day's rows through emit_transaction_day(upload=...) and return ({day: rows}, {}): %r" % (r.get("green"),))
    if r.get("refused_day") != [{"2026-10-13": 3, "2026-10-15": 4}, ["2026-10-14"], True]:
        pr.append("a day the producer refuses must be skipped, printed as TRANSACTION_SKIPPED <day> <reason>, and leave the others written: %r" % (r.get("refused_day"),))
    if r.get("emit_raises") != [{"2026-10-15": 4}, ["2026-10-13"], True, [["2026-10-15", 4, False]]]:
        pr.append("an emit that raises is caught for that day only and upload=False reaches the producer: %r" % (r.get("emit_raises"),))
    if r.get("not_importable") != [{}, ["2026-10-13", "2026-10-14"], True]:
        pr.append("when the producer did not import every day fails with the import error's text and nothing raises: %r" % (r.get("not_importable"),))
    if r.get("empty_days") != [{}, {}]:
        pr.append("no days return ({}, {})")
    if r.get("tx_event") != [{"2026-10-13": 3, "2026-10-14": 2, "2026-10-15": 4}, {}, 0, [True, True, True]]:
        pr.append("the transaction-only event runs the stage for the trading days of its range and NEVER run_day: %r" % (r.get("tx_event"),))
    if r.get("tx_event_dry") != [{"2026-10-14": 2}, {}, 0, [False]]:
        pr.append("the transaction-only event honours dry_run (upload False): %r" % (r.get("tx_event_dry"),))
    for k, why in (("tx_before_floor", "a range before FLOOR_DAY"), ("tx_extra_key", "a spec with a key beyond start and end"), ("tx_with_day", "an event that also names day"),
                   ("tx_too_long", "more than MAX_BACKFILL_DAYS trading days"), ("tx_start_after_end", "start after end")):
        if not (isinstance(r.get(k), str) and r[k].startswith("REFUSED:")):
            pr.append("the transaction-only event must refuse %s before any call: %r" % (why, r.get(k)))
    return pr


def wiring_problems(r):
    pr = []
    d = r.get("day_order") or [None, None, None]
    want_order = [["run_day", "2026-10-14"], ["run_day", "2026-10-15"], ["emit", ["2026-10-14", "2026-10-15"], True]]
    if d[0] != want_order:
        pr.append("the day/days path must run every run_day FIRST and then emit_transactions ONCE for the written days: %r" % (d[0],))
    if d[1] != {"2026-10-14": 2, "2026-10-15": 4} or d[2] != {}:
        pr.append("the day/days path must return transaction_rows and transaction_failed: %r" % (d[1:],))
    h = r.get("held_day") or [None, None, None]
    if not (h[0] == ["emit", ["2026-10-14"], True] and h[1] == {"2026-10-14": 2} and h[2] == []):
        pr.append("a HELD day is not a written day: the stage runs for the written days only: %r" % (h,))
    if r.get("planted_returns_equal") is not True:
        pr.append("a planted stage failure must leave the returns result (ok, days, results, held) byte-equal to the clean run")
    if r.get("planted_failed") != ["2026-10-14", "2026-10-15"]:
        pr.append("the planted failure must be recorded per day in transaction_failed: %r" % (r.get("planted_failed"),))
    if r.get("rewrite_calls") != []:
        pr.append("the rewrite path must never run the transaction stage")
    return pr


def source_problems(source):
    pr = []
    if "import account_transaction_cottonwood as atc" not in source or "ATC_IMPORT_ERROR" not in source:
        pr.append("the handler must carry `import account_transaction_cottonwood as atc` in a try/except that sets ATC_IMPORT_ERROR (the guarded import)")
    tree = ast.parse(source)
    funcs = {n.name: n for n in tree.body if isinstance(n, ast.FunctionDef)}
    for need_fn in ("transaction_frame", "emit_transactions"):
        if need_fn not in funcs:
            pr.append("the handler has no %s" % need_fn)
    for name in ("_run", "_rewrite"):
        fn = funcs.get(name)
        if fn is not None and any(isinstance(c, ast.Call) and isinstance(c.func, ast.Name) and c.func.id == "emit_transactions" for c in ast.walk(fn)):
            pr.append("%s must not call emit_transactions (the returns write and the rewrite stay as they are)" % name)
    return pr


def test_names(text):
    return re.findall(r"^\s*def (test_\w+)", text, re.M)


def run_behaviour(root):
    hp = Path(root, HANDLER)
    need(hp.is_file(), "missing " + HANDLER)
    run = subprocess.run([sys.executable, "-I", "-c", BEHAVIOUR, str(hp.parent)], capture_output=True, text=True, timeout=300, cwd=str(root))
    line = next((ln for ln in (run.stdout or "").splitlines() if ln.startswith("RESULT ")), None)
    need(line is not None, "the behaviour run failed (rc %s): %s" % (run.returncode, ((run.stderr or "") + (run.stdout or ""))[-400:]))
    return json.loads(line[len("RESULT "):])


def ac1(root):
    pr = source_problems(Path(root, HANDLER).read_text(encoding="utf-8")) if Path(root, HANDLER).is_file() else []
    r = run_behaviour(root)
    pr += behaviour_problems(r)
    need(not pr, "; ".join(pr))


def ac2(root):
    r = run_behaviour(root)
    pr = wiring_problems(r)
    need(not pr, "; ".join(pr))


def ac3(root):
    tp = Path(root, NEW_TESTS)
    need(tp.is_file(), "missing " + NEW_TESTS)
    names = test_names(tp.read_text(encoding="utf-8"))
    need(len(names) >= 14, "the new test file must hold at least 14 tests (found %d)" % len(names))
    low = " | ".join(names).lower()
    for w in NAME_WORDS:
        need(w in low, "the new test names lack %r" % w)
    run = subprocess.run([sys.executable, "-m", "pytest", TESTS_DIR, "-q", "-p", "no:cacheprovider", "--color=no", "-rf"], cwd=str(root), capture_output=True, text=True, timeout=900)
    need(run.returncode == 0, "the tests directory must pass (the base passes all 16): %s" % (run.stdout or "")[-300:])
    need("passed" in (run.stdout or ""), "pytest printed no passed count")


def selftest():
    bad = 0
    count = 0

    def arm(name, got, want):
        nonlocal bad, count
        count += 1
        if got != want:
            bad += 1
            print("SELFTEST FAIL %s: got %r want %r" % (name, got, want))

    green = {"green": [{"2026-10-13": 3, "2026-10-14": 2}, {}, [["2026-10-13", 3, True], ["2026-10-14", 2, True]]],
             "refused_day": [{"2026-10-13": 3, "2026-10-15": 4}, ["2026-10-14"], True],
             "emit_raises": [{"2026-10-15": 4}, ["2026-10-13"], True, [["2026-10-15", 4, False]]],
             "not_importable": [{}, ["2026-10-13", "2026-10-14"], True], "empty_days": [{}, {}],
             "tx_event": [{"2026-10-13": 3, "2026-10-14": 2, "2026-10-15": 4}, {}, 0, [True, True, True]], "tx_event_dry": [{"2026-10-14": 2}, {}, 0, [False]],
             "tx_before_floor": "REFUSED:ValueError", "tx_extra_key": "REFUSED:ValueError", "tx_with_day": "REFUSED:ValueError", "tx_too_long": "REFUSED:SystemExit",
             "tx_start_after_end": "REFUSED:ValueError",
             "day_order": [[["run_day", "2026-10-14"], ["run_day", "2026-10-15"], ["emit", ["2026-10-14", "2026-10-15"], True]], {"2026-10-14": 2, "2026-10-15": 4}, {}],
             "held_day": [["emit", ["2026-10-14"], True], {"2026-10-14": 2}, []], "planted_returns_equal": True, "planted_failed": ["2026-10-14", "2026-10-15"], "rewrite_calls": []}
    arm("behaviour-green", behaviour_problems(green), [])
    arm("wiring-green", wiring_problems(green), [])
    arm("behaviour-red", len(behaviour_problems(dict(green, empty_days=[{"x": 1}, {}]))), 1)
    arm("wiring-planted-red", len(wiring_problems(dict(green, planted_returns_equal=False))), 1)
    arm("wiring-held-red", len(wiring_problems(dict(green, held_day=[["emit", ["2026-10-14", "2026-10-15"], True], {}, []]))), 1)
    arm("wiring-order-red", len(wiring_problems(dict(green, day_order=[[["emit", ["2026-10-14"], True]], {}, {}]))) >= 1, True)
    arm("source-green", source_problems("try:\n    import account_transaction_cottonwood as atc\n    ATC_IMPORT_ERROR = None\nexcept Exception:\n    atc = None\n"
                                        "def transaction_frame(a, b, c):\n    pass\ndef emit_transactions(a, b, c, d):\n    pass\n"), [])
    arm("source-run-calls-emit-red", len(source_problems("import account_transaction_cottonwood as atc\nATC_IMPORT_ERROR = 1\ndef transaction_frame(a,b,c):\n    pass\n"
                                                         "def emit_transactions(a,b,c,d):\n    pass\ndef _run():\n    emit_transactions(1,2,3,4)\n")), 1)
    arm("test-names", test_names("def test_a():\n    pass\n"), ["test_a"])
    print("selftest %s" % ("FAIL" if bad else "PASS (%d arms)" % count))
    return 1 if bad else 0


def main(argv):
    if len(argv) == 2 and argv[1] == "--selftest":
        return selftest()
    if len(argv) != 3:
        print(__doc__)
        return 2
    root, ac = argv[1], argv[2]
    table = {"DBF137-2-AC1": ac1, "DBF137-2-AC2": ac2, "DBF137-2-AC3": ac3}
    if ac not in table:
        print("%s FAIL (unknown criterion)" % ac)
        return 1
    try:
        table[ac](root)
    except Fail as e:
        print("reason: %s" % e)
        print("%s FAIL" % ac)
        return 1
    except Exception as e:  # noqa: BLE001
        print("reason: %s: %s" % (type(e).__name__, e))
        print("%s FAIL" % ac)
        return 1
    print("%s PASS" % ac)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
