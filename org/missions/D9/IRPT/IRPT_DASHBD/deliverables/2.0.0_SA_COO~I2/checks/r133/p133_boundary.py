"""IRPT_DASHBD round 133, workstream B-IN (issuer 2.0.0_SA_COO~I2) -- the boundary measure pairs on the next TRADING day (cell DB-i-20).

CTO round-132 analysis (ruling 1, enrichment E1): run_scope_feed_real.measure_boundary paired day d with d + 1 CALENDAR day, so every
Friday-to-Monday and every holiday-eve boundary was never measured (the feed writes the weekend rows ABSENT when the series has no
point on them). The measure now pairs each landed day with the next TRADING day after it, taken from lib/trading_calendar.py.

The contract this checker grades (the order states it):
  run_scope_feed_real.next_trading_day(day_iso) -> the ISO day of the first trading day strictly after day_iso (lib calendar), or None
  run_scope_feed_real.measure_boundary(silver, next_day=None) -> (pairs, pairs_equal, max_rel_diff_bp); next_day(day_iso) -> ISO day
        or None picks a row's partner; None means next_trading_day. Every other rule is unchanged (a RETURNED row with a non-null
        end_market_value pairs with a RETURNED row of the same account on its partner day with a non-null start_market_value).
  run_real keeps its signature and uses the default.

  DBI133-1-AC1  the behaviour, on partitions written by the FEED'S OWN run() (its fake S3, transport and canned replies, driven in two
                separate runs so a Friday's end value and a Monday's start value both exist): a Friday pairs with the Monday (1 pair,
                the exact basis-point difference), the old calendar rule on the same frames finds 0; a Monday that is not RETURNED is
                not paired; a holiday-eve pairs with the next open day (a calendar double closes a Wednesday); an ordinary Tuesday
                still pairs with the Wednesday; next_trading_day answers the real holiday table (a Saturday, a Friday, the day before
                the observed July holiday, the day before Thanksgiving); run_real counts the Friday-to-Monday pair.
  DBI133-1-AC2  the new tests: >= 3 tests named *boundary*, one on Friday and Monday, one on a holiday, one named *mutant* (the old
                calendar rule must find 0 on the same frames); the boundary tests call measure_boundary and drive the feed's run();
                no hand-built feed frame; the whole file passes with at least 12 tests.

Usage: python -I <this file> <repo_root> <criterion_id>      prints "<id> PASS" or "<id> FAIL" last
       python -I <this file> --selftest [<repo_root>]
"""
import ast
import contextlib
import datetime as dt
import importlib.util
import inspect
import io
import re
import subprocess
import sys
import tempfile
import types
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT_DEFAULT = HERE.parents[8]
D = "org/missions/D9/IRPT/IRPT_DASHBD/deliverables/"
SCRIPT_REL = D + "0.9.0_WK_IRPT_DASHBD~316/run_scope_feed_real.py"
TEST_REL = "data/assets/scripts/gold/irpt_reporting/tests/test_inflection_scope_feed_real_shape.py"
FEED_DIR = "data/inf/manual_api"
ACCOUNTS = (7001, 7002, 7003, 7004, 7005)
RUN_REAL_PARAMS = ["reader", "out_dir", "dim_ids", "trading_days_fn", "firm", "method_version", "max_reads"]
HOLIDAY_DOUBLE = "2026-10-07"   # a calendar double: this Wednesday is a market holiday for the holiday-eve case


class Fail(Exception):
    pass


def need(cond, msg):
    if not cond:
        raise Fail(msg)


def _load(name, path):
    spec = importlib.util.spec_from_file_location(name, str(path))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def load_variant(src, real_path, name="run_scope_feed_real_variant"):
    """Run SOURCE as the module that lives at real_path (so its repository-root lookup binds to the real repository)."""
    mod = types.ModuleType(name)
    mod.__file__ = str(real_path)
    sys.modules[name] = mod
    exec(compile(src, str(real_path), "exec"), mod.__dict__)
    return mod


P131 = _load("p131_feedwriter_for_r133", HERE.parent / "r131" / "p131_feedwriter.py")


def feed_scenario(root, runs):
    """{ 'date=<day>': DataFrame } written by the feed's OWN run() on one fake S3, one feed run per (pull_day, series point days)."""
    import pandas as pd
    root = Path(root)
    sys.path.insert(0, str(root / "lib"))
    sys.path.insert(0, str(root / FEED_DIR))
    import test_scope_feed_daily_factor as T
    s3 = T._fixture_s3()
    for pull, point_days in runs:
        series = [T._point(d, 1.0) for d in point_days] or None
        responses = {5001: T._response([T._group(7001, series=series), T._group(7003, series=None)]), 5002: T._response([])}
        with contextlib.redirect_stdout(io.StringIO()):
            code, _t, _p = T._run(s3, responses, pull_date=pull)
        need(code == 0, "the feed's own run exited %r for pull day %s" % (code, pull))
    out = {}
    for (_bucket, key), body in sorted(s3.objects.items()):
        m = re.search(r"/silver/scope_account_returns/(date=\d{4}-\d{2}-\d{2})/data\.parquet$", "/" + key)
        if m:
            out[m.group(1)] = pd.read_parquet(io.BytesIO(body))
    return out


def cal_plus_one(day):
    return (dt.date.fromisoformat(day) + dt.timedelta(days=1)).isoformat()


def closed_wednesday(day):
    """The next open day after day when HOLIDAY_DOUBLE is closed (weekends are closed)."""
    d = dt.date.fromisoformat(day) + dt.timedelta(days=1)
    while d.weekday() >= 5 or d.isoformat() == HOLIDAY_DOUBLE:
        d += dt.timedelta(days=1)
    return d.isoformat()


def grade_behaviour(root, mod):
    need(hasattr(mod, "next_trading_day"), "the module has no next_trading_day(day_iso)")
    need("next_day" in inspect.signature(mod.measure_boundary).parameters, "measure_boundary takes no next_day argument")
    need(list(inspect.signature(mod.run_real).parameters) == RUN_REAL_PARAMS, "run_real's signature changed: %s" % list(inspect.signature(mod.run_real).parameters))
    fri_mon = feed_scenario(root, [("2026-10-09", ["2026-10-09"]), ("2026-10-12", ["2026-10-12"])])
    need(sorted(fri_mon) == ["date=2026-10-09", "date=2026-10-10", "date=2026-10-11", "date=2026-10-12"], "Friday-Monday partitions: %s" % sorted(fri_mon))
    got = mod.measure_boundary(fri_mon)
    need(got == (1, 0, 1000.0), "Friday-to-Monday: measure_boundary gave %r, want (1, 0, 1000.0)" % (got,))
    old = mod.measure_boundary(fri_mon, next_day=cal_plus_one)
    need(old == (0, 0, None), "the calendar-day rule on the same frames should find 0 pairs, gave %r" % (old,))
    absent_mon = feed_scenario(root, [("2026-10-09", ["2026-10-09"]), ("2026-10-12", [])])
    got = mod.measure_boundary(absent_mon)
    need(got == (0, 0, None), "a Monday that is not RETURNED must not pair: gave %r" % (got,))
    eve = feed_scenario(root, [("2026-10-06", ["2026-10-06"]), ("2026-10-08", ["2026-10-08"])])
    need(sorted(eve) == ["date=2026-10-06", "date=2026-10-07", "date=2026-10-08"], "holiday-eve partitions: %s" % sorted(eve))
    got = mod.measure_boundary(eve, next_day=closed_wednesday)
    need(got == (1, 0, 1000.0), "holiday-eve to the next open day: gave %r, want (1, 0, 1000.0)" % (got,))
    got_old = mod.measure_boundary(eve, next_day=cal_plus_one)
    need(got_old == (0, 0, None), "the calendar rule on the holiday-eve frames should find 0, gave %r" % (got_old,))
    tue_wed = feed_scenario(root, [("2026-10-06", ["2026-10-06"]), ("2026-10-07", ["2026-10-07"])])
    for label, fn in (("default", None), ("calendar rule", cal_plus_one)):
        got = mod.measure_boundary(tue_wed) if fn is None else mod.measure_boundary(tue_wed, next_day=fn)
        need(got == (1, 0, 1000.0), "an ordinary Tuesday-to-Wednesday pair under the %s: gave %r" % (label, got))
    table = (("2026-10-09", "2026-10-12"), ("2026-10-10", "2026-10-12"), ("2026-10-12", "2026-10-13"),
             ("2026-07-02", "2026-07-06"), ("2026-11-25", "2026-11-27"), ("2026-12-24", "2026-12-28"))
    for day, want in table:
        need(mod.next_trading_day(day) == want, "next_trading_day(%s) = %r, want %s" % (day, mod.next_trading_day(day), want))
    with tempfile.TemporaryDirectory() as td:
        rec = mod.run_real(P131.P129.FakeReader({"scope_account_returns": fri_mon}), str(Path(td) / "out"), [str(a) for a in ACCOUNTS],
                           P131.weekdays, "FIRM-SYNTH", 0, 400)
    need(rec.get("status") == "RAN", "run_real status %r on the Friday-Monday partitions" % rec.get("status"))
    need(rec["boundary"]["pairs"] == 1, "run_real boundary.pairs = %r, want 1 (the Friday-to-Monday pair)" % rec["boundary"]["pairs"])


def grade_tests(root):
    tf = Path(root) / TEST_REL
    need(tf.is_file(), "no test file at %s" % TEST_REL)
    src = tf.read_bytes().decode("ascii")
    need("pull_inflection_scope_account_returns" in src, "the test file never imports the feed module")
    for bad in ("pd.DataFrame([", "pandas.DataFrame([", "DataFrame({\"pull_date\"", "DataFrame({'pull_date'"):
        need(bad not in src, "the test file hand-builds a frame (%s); a feed frame must come from the feed's run()" % bad)
    tree = ast.parse(src)
    funcs = [n for n in tree.body if isinstance(n, ast.FunctionDef) and n.name.startswith("test_")]
    boundary = [f for f in funcs if "boundary" in f.name]
    need(len(boundary) >= 3, "fewer than 3 tests named *boundary* (%d)" % len(boundary))
    names = " ".join(f.name for f in boundary)
    need(re.search(r"friday\w*monday|monday\w*friday", names) is not None, "no boundary test names Friday and Monday")
    need("holiday" in names, "no boundary test names a holiday")
    mutants = [f for f in boundary if "mutant" in f.name]
    need(mutants, "no boundary test named *mutant*")
    text = "\n".join(ast.get_source_segment(src, f) or "" for f in boundary)
    need("measure_boundary(" in text, "the boundary tests never call measure_boundary")
    need("_run(" in text or ".run(" in text, "the boundary tests never drive the feed's run() (directly or through its harness _run)")
    mtext = "\n".join(ast.get_source_segment(src, f) or "" for f in mutants)
    need("next_day=" in mtext and "== 0" in mtext, "the mutant test must pass the calendar rule as next_day= and assert 0 pairs")
    r = subprocess.run([sys.executable, "-I", "-m", "pytest", "-q", "-p", "no:cacheprovider", str(tf)], cwd=str(root), capture_output=True, text=True, timeout=150)
    tail = (r.stdout or "").strip().splitlines()[-1:] or [""]
    need(r.returncode == 0, "pytest rc %s: %s" % (r.returncode, tail[0]))
    m = re.search(r"(\d+) passed", r.stdout or "")
    need(m is not None and int(m.group(1)) >= 12, "fewer than 12 passed tests: %s" % tail[0])


# ---- self-test: a reference module and four mutants for AC1; a reference test file and five mutants for AC2 --------------------
REF_FN = '''
def next_trading_day(day):
    """The first trading day strictly after day (lib/trading_calendar.py), as an ISO day, or None."""
    nxt = tc.first_trading_day_on_or_after(dt.date.fromisoformat(day) + dt.timedelta(days=1))
    return None if nxt is None else nxt.isoformat()


'''


def reference_source(base):
    s = base
    need(s.count("def measure_boundary(silver):") == 1, "base module drifted: measure_boundary header")
    need(s.count("        after = rows.get((account, _next_day(day)))\n") == 1, "base module drifted: the pairing line")
    s = s.replace("def measure_boundary(silver):", REF_FN.lstrip("\n") + "def measure_boundary(silver, next_day=None):")
    s = s.replace("        after = rows.get((account, _next_day(day)))\n",
                  "        partner = (next_day or next_trading_day)(day)\n        after = rows.get((account, partner)) if partner else None\n")
    return s


def selftest(root):
    root = Path(root).resolve()
    real = root / SCRIPT_REL
    base = real.read_bytes().decode("ascii")
    try:
        grade_behaviour(root, load_variant(base, real, "rsfr_base"))
        raise Fail("selftest: the BASE module passed AC1")
    except Fail as exc:
        if str(exc).startswith("selftest"):
            raise
        print("selftest BASE (before the fix)        -> FAIL (%s)" % str(exc)[:70])
    except TypeError as exc:
        print("selftest BASE (before the fix)        -> FAIL (TypeError %s)" % str(exc)[:60])
    ref = reference_source(base)
    grade_behaviour(root, load_variant(ref, real, "rsfr_ref"))
    print("selftest REFERENCE                    -> PASS")
    mutants = [
        ("default stays calendar d+1", ref.replace("(next_day or next_trading_day)", "(next_day or _next_day)")),
        ("weekends only, no holidays", ref.replace(
            "    nxt = tc.first_trading_day_on_or_after(dt.date.fromisoformat(day) + dt.timedelta(days=1))\n    return None if nxt is None else nxt.isoformat()\n",
            "    d = dt.date.fromisoformat(day) + dt.timedelta(days=1)\n    while d.weekday() >= 5:\n        d += dt.timedelta(days=1)\n    return d.isoformat()\n")),
        ("partner is the day itself", ref.replace("tc.first_trading_day_on_or_after(dt.date.fromisoformat(day) + dt.timedelta(days=1))",
                                                  "tc.first_trading_day_on_or_after(dt.date.fromisoformat(day))")),
        ("next_day argument ignored", ref.replace("(next_day or next_trading_day)", "next_trading_day")),
    ]
    for label, src in mutants:
        need(src != ref, "selftest: the mutant %r did not change the source" % label)
        try:
            grade_behaviour(root, load_variant(src, real, "rsfr_mut"))
            raise Fail("selftest: the mutant %r PASSED" % label)
        except Fail as exc:
            if str(exc).startswith("selftest"):
                raise
            print("selftest mutant %-26s -> FAIL (%s)" % (label, str(exc)[:60]))
    # AC2 on synthetic test files in a temp root (static checks + a real pytest run)
    good = ('FEED = "pull_inflection_scope_account_returns"\n\n\ndef _run(*a):\n    return 0\n\n\ndef measure_boundary(*a, **k):\n    return 0\n\n\n'
            'def test_boundary_friday_pairs_monday():\n    _run()\n    measure_boundary()\n\n\n'
            'def test_boundary_holiday_eve_pairs_next_open_day():\n    _run()\n    measure_boundary()\n\n\n'
            'def test_boundary_mutant_calendar_rule_finds_none():\n    _run()\n    pairs = measure_boundary(next_day=None)\n    assert pairs == 0\n\n\n')
    good += "".join("def test_filler_%d():\n    assert True\n\n\n" % i for i in range(10))
    cases = [("GOOD", good, False),
             ("no holiday test", good.replace("holiday_eve", "eve"), True),
             ("no mutant test", good.replace("boundary_mutant", "boundary_other"), True),
             ("fewer than 12 tests", good.replace("def test_filler_9", "def helper_filler_9").replace("def test_filler_8", "def helper_filler_8")
                                          .replace("def test_filler_7", "def helper_filler_7").replace("def test_filler_6", "def helper_filler_6"), True),
             ("a failing test", good + "def test_failing():\n    assert False\n", True),
             ("a hand-built feed frame", good + "FRAME = pd.DataFrame([{'a': 1}])\n", True)]
    for label, text, expect_fail in cases:
        with tempfile.TemporaryDirectory() as td:
            tf = Path(td) / TEST_REL
            tf.parent.mkdir(parents=True)
            tf.write_bytes(text.encode("ascii"))
            try:
                grade_tests(td)
                failed, why = False, ""
            except Fail as exc:
                failed, why = True, str(exc)[:60]
        need(failed == expect_fail, "selftest AC2 %s: expected %s" % (label, "FAIL" if expect_fail else "PASS"))
        print("selftest AC2 %-24s -> %s" % (label, ("FAIL (%s)" % why) if failed else "PASS"))
    print("selftest PASS")


def main(argv):
    if len(argv) >= 2 and argv[1] == "--selftest":
        try:
            selftest(argv[2] if len(argv) > 2 else ROOT_DEFAULT)
        except Fail as exc:
            print("REASON: %s" % exc)
            print("selftest FAIL")
            return 1
        return 0
    root, cid = Path(argv[1]).resolve(), argv[2]
    try:
        if cid == "DBI133-1-AC1":
            grade_behaviour(root, load_variant((root / SCRIPT_REL).read_bytes().decode("ascii"), root / SCRIPT_REL, "rsfr_under_test"))
        elif cid == "DBI133-1-AC2":
            grade_tests(root)
        else:
            raise Fail("unknown criterion %s" % cid)
    except Fail as exc:
        print("REASON: %s" % exc)
        print("%s FAIL" % cid)
        return 1
    except Exception as exc:  # a crash is a FAIL with its type named, never a pass
        print("REASON: %s: %s" % (type(exc).__name__, str(exc)[:300]))
        print("%s FAIL" % cid)
        return 1
    print("%s PASS" % cid)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
