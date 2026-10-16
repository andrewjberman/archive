"""IRPT_DASHBD round 136, workstream F-SHIP ~F2 (issuer 2.0.0_SA_COO~F2) -- FWD-5: the 49 FINANCIAL GOLD HANDLER EMITS THE TRANSACTION DAY (W1).

  DB-f-2201 (~2201) `infra/aws/lambda/investor-reporting/reporting-gold/handler.py` imports `account_transaction` GUARDED (`at49`, `AT49_IMPORT_ERROR`), reads the day's fact_trn
                    partition through `transaction_frame(s3, firm, day)`, and `emit_transactions(s3, firm, days, upload)` runs the producer's `normalize_trn` then
                    `emit_transaction_day` per day, NEVER raising (a failed day is `TRANSACTION_SKIPPED <day> <reason>` and a key of `failed`). The scheduled `run` and `run_backfill`
                    call it LAST (after the filled-report stage) for the days the returns stage wrote, and their results gain `transaction_rows` and `transaction_failed`; the
                    lots-only backfill and the one-day filled event do not call it. The twelve handler tests that fail at the base are PRE-EXISTING and stay as they are.
                    DBF136-1-AC1 (the emission function), DBF136-1-AC2 (the wiring), DBF136-1-AC3 (the tests)

Usage: python <this file> <repo_root> <criterion_id>      prints "<id> PASS" or "<id> FAIL" last
       python <this file> --selftest                        the pure helpers on synthetic arms
"""
import ast
import re
import subprocess
import sys
from pathlib import Path

HANDLER = "infra/aws/lambda/investor-reporting/reporting-gold/handler.py"
TESTS_DIR = "infra/aws/lambda/investor-reporting/reporting-gold/tests"
NEW_TESTS = TESTS_DIR + "/test_transaction_emission.py"
BASE_FAILS = "org/missions/D9/IRPT/IRPT_DASHBD/deliverables/2.0.0_SA_COO~F2/checks/r136/handler_tests_base_failures.txt"
NAME_WORDS = ("guarded", "import", "emit", "skipped", "never", "upload", "dry", "scheduled", "backfill", "failure", "order", "lots")

BEHAVIOUR = r'''
import io, json, sys
from contextlib import redirect_stdout
from unittest import mock
sys.path.insert(0, sys.argv[1])
import pandas as pd
import handler as h

def frame(day, n):
    return pd.DataFrame([{"trade_date": day, "k": i} for i in range(n)])

class At:
    def __init__(self, bad_normalize=(), bad_emit=()):
        self.calls = []
        self.bad_normalize, self.bad_emit = set(bad_normalize), set(bad_emit)
    def normalize_trn(self, fr, firm):
        d = str(fr.iloc[0]["trade_date"])
        if d in self.bad_normalize:
            raise SystemExit("REFUSED: a refused line")
        return [{"d": d}] * len(fr)
    def emit_transaction_day(self, s3, rows, firm, day, *, upload):
        if day in self.bad_emit:
            raise ValueError("boom")
        self.calls.append((day, len(rows), upload))
        return {"rows": len(rows), "landed": upload}

out = {}
sizes = {"2026-10-01": 3, "2026-10-02": 2, "2026-10-05": 4}
with mock.patch.object(h, "transaction_frame", lambda s3, firm, day: frame(day, sizes[day])):
    at = At()
    buf = io.StringIO()
    with mock.patch.object(h, "at49", at), redirect_stdout(buf):
        w, f = h.emit_transactions(None, "49financial", ["2026-10-01", "2026-10-02"], True)
    out["green"] = [w, f, at.calls]
    at = At(bad_normalize={"2026-10-02"})
    buf = io.StringIO()
    with mock.patch.object(h, "at49", at), redirect_stdout(buf):
        w, f = h.emit_transactions(None, "49financial", ["2026-10-01", "2026-10-02", "2026-10-05"], True)
    out["refused_day"] = [w, sorted(f), "TRANSACTION_SKIPPED 2026-10-02" in buf.getvalue(), "SystemExit" in f["2026-10-02"] or "refused" in f["2026-10-02"].lower()]
    at = At(bad_emit={"2026-10-01"})
    buf = io.StringIO()
    with mock.patch.object(h, "at49", at), redirect_stdout(buf):
        w, f = h.emit_transactions(None, "49financial", ["2026-10-01", "2026-10-05"], False)
    out["emit_raises"] = [w, sorted(f), "ValueError" in f["2026-10-01"], at.calls]
    with mock.patch.object(h, "transaction_frame", lambda s3, firm, day: (_ for _ in ()).throw(KeyError("nosuch"))):
        at = At()
        buf = io.StringIO()
        with mock.patch.object(h, "at49", at), redirect_stdout(buf):
            w, f = h.emit_transactions(None, "49financial", ["2026-10-01"], True)
        out["frame_raises"] = [w, sorted(f)]
    buf = io.StringIO()
    with mock.patch.object(h, "at49", None), mock.patch.object(h, "AT49_IMPORT_ERROR", "ImportError: no module named x"), redirect_stdout(buf):
        w, f = h.emit_transactions(None, "49financial", ["2026-10-01", "2026-10-02"], True)
    out["not_importable"] = [w, sorted(f), all("ImportError: no module named x" in v for v in f.values())]
    with mock.patch.object(h, "at49", At()), redirect_stdout(io.StringIO()):
        out["empty_days"] = list(h.emit_transactions(None, "49financial", [], True))
def stages(ev):
    try:
        return h.backfill_stages(ev)
    except SystemExit as e:
        return "REFUSED:" + ("stages" if "stages" in str(e) else "?")
out["stages"] = [stages({}), stages({"stages": ["lots"]}), stages({"stages": ["transaction"]}), stages({"stages": ["transaction", "lots"]}),
                 stages({"stages": ["returns"]}), stages({"stages": []}), stages({"stages": "transaction"})]
print("RESULT " + json.dumps(out, sort_keys=True))
'''


class Fail(Exception):
    pass


def need(cond, msg):
    if not cond:
        raise Fail(msg)


def behaviour_problems(res):
    pr = []
    if res.get("green") != [{"2026-10-01": 3, "2026-10-02": 2}, {}, [["2026-10-01", 3, True], ["2026-10-02", 2, True]]]:
        pr.append("emit_transactions must write each day's normalized rows through emit_transaction_day(upload=...) and return ({day: rows}, {}): %r" % (res.get("green"),))
    rd = res.get("refused_day") or []
    if rd[:2] != [{"2026-10-01": 3, "2026-10-05": 4}, ["2026-10-02"]] or rd[2:] != [True, True]:
        pr.append("a day the producer refuses must be skipped, printed as TRANSACTION_SKIPPED <day> <reason>, and leave the other days written: %r" % (rd,))
    er = res.get("emit_raises") or []
    if er[:3] != [{"2026-10-05": 4}, ["2026-10-01"], True] or er[3:] != [[["2026-10-05", 4, False]]]:
        pr.append("an emit that raises must be caught and recorded for that day only; upload=False must reach the producer: %r" % (er,))
    if res.get("frame_raises") != [{}, ["2026-10-01"]]:
        pr.append("a day whose partition cannot be read must be skipped, never raised: %r" % (res.get("frame_raises"),))
    ni = res.get("not_importable") or []
    if ni != [{}, ["2026-10-01", "2026-10-02"], True]:
        pr.append("when the producer did not import, every day fails with AT49_IMPORT_ERROR's text and nothing raises: %r" % (ni,))
    if res.get("empty_days") != [{}, {}]:
        pr.append("no days must return ({}, {})")
    want = [["returns", "class", "lots"], ["lots"], ["transaction"], "REFUSED:stages", "REFUSED:stages", "REFUSED:stages", "REFUSED:stages"]
    if res.get("stages") != want:
        pr.append("backfill_stages must return the three stages for no key, [lots] and [transaction] for those selections, and refuse by name (the word stages) every other value: %r" % (res.get("stages"),))
    return pr


def wiring_problems(source):
    """AST: `at49`/`AT49_IMPORT_ERROR` defined at module level; `run` and `run_backfill` each call emit_transactions once, after their filled-report stage, and return transaction_rows
    and transaction_failed; the lots-only branch of run_backfill and run_day_event do not call it."""
    pr = []
    tree = ast.parse(source)
    names = {t.id for n in tree.body if isinstance(n, ast.Assign) for t in n.targets if isinstance(t, ast.Name)}
    tried = [n for n in tree.body if isinstance(n, ast.Try)]
    if "at49" not in names and not any(isinstance(s, ast.Assign) and any(getattr(t, "id", "") == "at49" for t in s.targets) for t_ in tried for h in t_.handlers for s in h.body):
        pr.append("at49 (the guarded import's name) is not defined at module level")
    if "import account_transaction as at49" not in source:
        pr.append("the handler must carry `import account_transaction as at49` inside a try/except (the guarded import)")
    if "AT49_IMPORT_ERROR" not in source:
        pr.append("AT49_IMPORT_ERROR is missing")
    funcs = {n.name: n for n in tree.body if isinstance(n, ast.FunctionDef)}
    for need_fn in ("transaction_frame", "emit_transactions"):
        if need_fn not in funcs:
            pr.append("the handler has no %s" % need_fn)
    for name, filled in (("run", ("run_filled_day", "filled_stage", "filled_write")), ("run_backfill", ("filled_write", "filled_stage", "run_filled_day"))):
        fn = funcs.get(name)
        if fn is None:
            pr.append("the handler has no %s" % name)
            continue
        calls = [(c.lineno, c.func.id) for c in ast.walk(fn) if isinstance(c, ast.Call) and isinstance(c.func, ast.Name)]
        tx = [ln for ln, nm in calls if nm == "emit_transactions"]
        fl = [ln for ln, nm in calls if nm in filled]
        want_calls = 2 if name == "run_backfill" else 1
        if len(tx) != want_calls:
            pr.append("%s must call emit_transactions exactly %d time(s) (found %d)%s" % (name, want_calls, len(tx),
                      " (the transaction-only branch and the full path after the filled stage)" if want_calls == 2 else ""))
        elif fl and max(tx) <= max(fl):
            pr.append("%s must call emit_transactions AFTER its filled-report stage (line %d is not after %d)" % (name, max(tx), max(fl)))
        keys = {k.value for d in ast.walk(fn) if isinstance(d, ast.Dict) for k in d.keys if isinstance(k, ast.Constant) and isinstance(k.value, str)}
        for k in ("transaction_rows", "transaction_failed"):
            if k not in keys:
                pr.append("%s must return %s" % (name, k))
    for name in ("run_day_event", "filled_stage", "emit_classes", "emit_lots"):
        fn = funcs.get(name)
        if fn is not None and any(isinstance(c, ast.Call) and isinstance(c.func, ast.Name) and c.func.id == "emit_transactions" for c in ast.walk(fn)):
            pr.append("%s must not call emit_transactions" % name)
    return pr


def test_names(text):
    return re.findall(r"^\s*def (test_\w+)", text, re.M)


def ac1(root):
    hp = Path(root, HANDLER)
    need(hp.is_file(), "missing " + HANDLER)
    run = subprocess.run([sys.executable, "-I", "-c", BEHAVIOUR, str(hp.parent)], capture_output=True, text=True, timeout=300, cwd=str(root))
    line = next((ln for ln in (run.stdout or "").splitlines() if ln.startswith("RESULT ")), None)
    need(line is not None, "the behaviour run failed (rc %s): %s" % (run.returncode, ((run.stderr or "") + (run.stdout or ""))[-400:]))
    import json
    pr = behaviour_problems(json.loads(line[len("RESULT "):]))
    need(not pr, "; ".join(pr))


def ac2(root):
    src = Path(root, HANDLER).read_text(encoding="utf-8")
    pr = wiring_problems(src)
    need(not pr, "; ".join(pr))


def ac3(root):
    tp = Path(root, NEW_TESTS)
    need(tp.is_file(), "missing " + NEW_TESTS)
    names = test_names(tp.read_text(encoding="utf-8"))
    need(len(names) >= 14, "the new test file must hold at least 14 tests (found %d)" % len(names))
    low = " | ".join(names).lower()
    for w in NAME_WORDS:
        need(w in low, "the new test names lack %r" % w)
    base = {ln.strip() for ln in Path(root, BASE_FAILS).read_text(encoding="utf-8").splitlines() if ln.strip()}
    run = subprocess.run([sys.executable, "-m", "pytest", TESTS_DIR, "-q", "-p", "no:cacheprovider", "--color=no", "-rf"], cwd=str(root), capture_output=True, text=True, timeout=900)
    failed = {re.sub(r" - .*", "", ln[len("FAILED "):]).strip() for ln in (run.stdout or "").splitlines() if ln.startswith("FAILED ")}
    new = sorted(failed - base)
    need(not new, "tests that passed at the base now fail (or the new file fails): %s" % "; ".join(new[:4]))
    need("passed" in (run.stdout or ""), "pytest printed no passed count: %s" % (run.stdout or "")[-200:])


def selftest():
    bad = 0
    count = 0

    def arm(name, got, want):
        nonlocal bad, count
        count += 1
        if got != want:
            bad += 1
            print("SELFTEST FAIL %s: got %r want %r" % (name, got, want))

    green = {"stages": [["returns", "class", "lots"], ["lots"], ["transaction"], "REFUSED:stages", "REFUSED:stages", "REFUSED:stages", "REFUSED:stages"],
             "green": [{"2026-10-01": 3, "2026-10-02": 2}, {}, [["2026-10-01", 3, True], ["2026-10-02", 2, True]]],
             "refused_day": [{"2026-10-01": 3, "2026-10-05": 4}, ["2026-10-02"], True, True],
             "emit_raises": [{"2026-10-05": 4}, ["2026-10-01"], True, [["2026-10-05", 4, False]]],
             "frame_raises": [{}, ["2026-10-01"]], "not_importable": [{}, ["2026-10-01", "2026-10-02"], True], "empty_days": [{}, {}]}
    arm("behaviour-green", behaviour_problems(green), [])
    arm("behaviour-red", len(behaviour_problems(dict(green, empty_days=[{"x": 1}, {}]))), 1)
    arm("stages-red", len(behaviour_problems(dict(green, stages=[["returns", "class", "lots"], ["lots"], ["lots"]] + ["x"] * 4))), 1)
    src = ("try:\n    import account_transaction as at49\n    AT49_IMPORT_ERROR = None\nexcept Exception as _e:\n    at49 = None\n    AT49_IMPORT_ERROR = str(_e)\n"
           "def transaction_frame(s3, firm, day):\n    return None\n"
           "def emit_transactions(s3, firm, days, upload):\n    return {}, {}\n"
           "def run(s3):\n    filled_stage()\n    a, b = emit_transactions(s3, 1, [], True)\n    return {'transaction_rows': a, 'transaction_failed': b}\n"
           "def run_backfill(s3):\n    c, d = emit_transactions(s3, 1, [], True)\n    filled_write()\n    a, b = emit_transactions(s3, 1, [], True)\n    return {'transaction_rows': a, 'transaction_failed': b}\n")
    arm("wiring-green", wiring_problems(src), [])
    arm("wiring-before-filled", len(wiring_problems(src.replace("filled_stage()\n    a, b = emit_transactions(s3, 1, [], True)", "a, b = emit_transactions(s3, 1, [], True)\n    filled_stage()"))), 1)
    arm("wiring-missing-keys", len(wiring_problems(src.replace("'transaction_failed': b", "'x': b"))) >= 1, True)
    arm("test-names", test_names("def test_a_b():\n    pass\n    def test_c():\n        pass\n"), ["test_a_b", "test_c"])
    print("selftest %s" % ("FAIL" if bad else "PASS (%d arms)" % count))
    return 1 if bad else 0


def main(argv):
    if len(argv) == 2 and argv[1] == "--selftest":
        return selftest()
    if len(argv) != 3:
        print(__doc__)
        return 2
    root, ac = argv[1], argv[2]
    table = {"DBF136-1-AC1": ac1, "DBF136-1-AC2": ac2, "DBF136-1-AC3": ac3}
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
