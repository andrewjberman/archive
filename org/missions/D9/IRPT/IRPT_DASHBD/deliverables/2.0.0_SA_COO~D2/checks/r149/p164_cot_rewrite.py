"""IRPT_DASHBD round 149, workstream HSRW (issuer 2.0.0_SA_COO~D2) -- DB-b-296, the COTTONWOOD LANDING'S EXPLICIT REWRITE EVENT (CTO ruling on fork e6ef, msg 9264, route (c)): the 65 landed Cottonwood gold days carry the
old history_scope constant and the landing refuses to overwrite a landed day. The handler gains {"rewrite": {"start": "YYYY-MM-DD", "end": "YYYY-MM-DD"}} (optionally with "dry_run"): at most MAX_BACKFILL_DAYS trading days,
ONLY days already landed, never combined with day or days, never before FLOOR_DAY; each named day is derived with the new history_scope rule and its two objects are overwritten (the bucket is versioned: prior versions are kept
and nothing is deleted). The scheduled path and the named-day path keep the no-overwrite guard unchanged. Every refusal comes before any write. LOCAL: python files; nothing runs against AWS.

  DB-b-296 (~239)   adapters/cottonwood_bd_account_return_daily.py (write_day, run_day) + infra/aws/lambda/investor-reporting/account-return-daily/handler.py (landed_days, _run, _rewrite, lambda_handler) + tests + a facts record
                    DB164-1-AC1 (the adapter: write_day and run_day with rewrite),
                    DB164-1-AC2 (the handler event: the rewrite, every refusal, the guard elsewhere),
                    DB164-1-AC3 (the new tests, the gold and landing-handler test directories, the grant, the facts record)

Usage: python <this file> <repo_root> <criterion_id>      prints "<id> PASS" or "<id> FAIL" last
       python <this file> --selftest                       the pure clauses on synthetic arms
"""
import copy
import importlib.util
import io
import re
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
D = "org/missions/D9/IRPT/IRPT_DASHBD/deliverables/"
AUTHOR = "0.9.0_WK_IRPT_DASHBD~239"
REC_REL = D + AUTHOR + "/RD_COT_REWRITE_FACTS_R149.json"
ORDER_REL = "org/missions/D9/IRPT/IRPT_DASHBD/task-orders/IRPT_DASHBD.TO-DB-b-296.cottonwood-landing-explicit-rewrite.md"
GOLD = "data/assets/scripts/gold/irpt_reporting/"
CBD_REL = GOLD + "adapters/cottonwood_bd_account_return_daily.py"
HANDLER_REL = "infra/aws/lambda/investor-reporting/account-return-daily/handler.py"
HANDLER_DIR = "infra/aws/lambda/investor-reporting/account-return-daily"
TEST_REL = GOLD + "tests/test_cottonwood_rewrite.py"
TESTS_DIR = GOLD + "tests"
KNOWN_RED = "test_account_activity_lots.py::test_the_calendar_itself_raises_before_2010_and_the_index_never_asks_it"
GRANT_FILES = {CBD_REL, HANDLER_REL, TEST_REL, GOLD + "tests/test_history_scope_derivation.py"}
GRANT_PREFIXES = (D + AUTHOR + "/", "org/missions/D9/IRPT/IRPT_DASHBD/surprise-channel/investigations/", "org/missions/D9/IRPT/IRPT_DASHBD/task-orders/", HANDLER_DIR + "/tests/")
CLAIM_COL = "history_scope_claim"
LONG_DIGITS = re.compile(r"\d{8,}")


class Fail(Exception):
    pass


def need(cond, msg):
    if not cond:
        raise Fail(msg)


def nes(x):
    return isinstance(x, str) and x.strip() != ""


def git(root, *a):
    r = subprocess.run(["git", "-C", str(root)] + list(a), capture_output=True)
    need(r.returncode == 0, "git %s: %s" % (" ".join(a[:2]), r.stderr.decode("utf-8", "replace").strip()[:200]))
    return r.stdout


def own_commits(root):
    base = git(root, "log", "--diff-filter=A", "--format=%H", "--", ORDER_REL).decode().split()
    need(base, "the order's first commit is not in this history")
    out = git(root, "log", "--reverse", "--format=%H", "--author=" + AUTHOR, base[-1] + "..HEAD").decode().split()
    need(out, "no commit by %s since the order was issued" % AUTHOR)
    return out


def p162():
    spec = importlib.util.spec_from_file_location("p162_helper", str(HERE / "p162_producers_scope.py"))
    mod = importlib.util.module_from_spec(spec)
    sys.modules["p162_helper"] = mod
    spec.loader.exec_module(mod)
    return mod


class LogWriter:
    """put_object and list_objects_v2 only (any delete is an AttributeError); every put is logged in order."""

    def __init__(self):
        self.objs, self.log = {}, []

    def put_object(self, Bucket, Key, Body, **kw):
        self.log.append(Key)
        self.objs[Key] = bytes(Body)
        return {}

    def list_objects_v2(self, Bucket, Prefix, **kw):
        keys = sorted(k for k in self.objs if k.startswith(Prefix))
        if kw.get("Delimiter"):
            parts = sorted({Prefix + k[len(Prefix):].split(kw["Delimiter"], 1)[0] + kw["Delimiter"] for k in keys})
            return {"KeyCount": len(parts), "CommonPrefixes": [{"Prefix": x} for x in parts], "IsTruncated": False}
        return {"KeyCount": len(keys), "Contents": [{"Key": k} for k in keys], "IsTruncated": False}


def raises(fn, kinds, label):
    try:
        fn()
    except BaseException as e:  # noqa: BLE001
        need(isinstance(e, kinds), "%s: raised %s, expected %s" % (label, type(e).__name__, "/".join(k.__name__ for k in kinds)))
        return e
    raise Fail("%s: nothing was raised" % label)


def tables(w):
    import pyarrow.parquet as pq
    out = {}
    for k, v in w.objs.items():
        if k.endswith("data.parquet"):
            out[k.split("date=")[1].split("/")[0]] = pq.read_table(io.BytesIO(v))
    return out


def check_adapter(root):
    h = p162()
    h.paths(root)
    cbd = h.load(root / CBD_REL, "cbd_rewrite_under_check")
    gce = cbd.GoldWriteError
    d1, d2, floor = h.PREV, h.NEXT, h.FLOOR
    # a landed legacy day, then a rewrite of it with the floor day: 21 columns, the same two keys overwritten, nothing else
    w = LogWriter()
    cbd.run_day(h.reader(), w, d1, upload=True)
    before = set(w.objs)
    need(len(before) == 2 and len(tables(w)[d1].schema.names) == 20, "the legacy landing of a day must write the two objects and 20 columns")
    n0 = len(w.log)
    res = cbd.run_day(h.reader(), w, d1, upload=True, floor_day=floor, rewrite=True)
    need(res["held"] is False and res["rows"] == 2, "a rewrite of a landed day must write its two rows")
    need(w.log[n0:] == sorted(before) or sorted(w.log[n0:]) == sorted(before), "the rewrite must put exactly the day's two existing keys, got %s" % w.log[n0:])
    need(set(w.objs) == before, "a rewrite must create no other key")
    t = tables(w)[d1]
    rows = {r["account_id"]: r for r in t.to_pylist()}
    need(t.schema.names[-1] == CLAIM_COL and len(t.schema.names) == 21 and rows[h.X]["history_scope"] == "PARTIAL_HISTORY" and rows[h.Y]["history_scope"] == "FULL", "the rewritten day carries the derived scope and the claim (21 columns)")
    # the guard stays for a plain landing of a landed day
    n1 = len(w.log)
    raises(lambda: cbd.run_day(h.reader(), w, d1, upload=True, floor_day=floor), (gce,), "a plain landing of a landed day")
    need(len(w.log) == n1, "the refused plain landing must write nothing")
    # a rewrite of a day that holds no objects, and a rewrite with no floor partition, are refused before any put
    w2 = LogWriter()
    raises(lambda: cbd.run_day(h.reader(), w2, d1, upload=True, floor_day=floor, rewrite=True), (gce,), "a rewrite of an unlanded day")
    need(not w2.log, "the refused rewrite of an unlanded day must write nothing")
    w3 = LogWriter()
    cbd.run_day(h.reader(), w3, d1, upload=True)
    n3 = len(w3.log)
    raises(lambda: cbd.run_day(h.reader(False), w3, d1, upload=True, floor_day=floor, rewrite=True), (gce,), "a rewrite with no floor partition")
    raises(lambda: cbd.run_day(h.reader(), w3, d1, upload=True, rewrite=True), (gce,), "a rewrite with no floor day")
    need(len(w3.log) == n3, "a rewrite that cannot derive must write nothing")
    # a dry run of a rewrite writes nothing
    n4 = len(w3.log)
    cbd.run_day(h.reader(), w3, d1, upload=False, floor_day=floor, rewrite=True)
    need(len(w3.log) == n4, "upload False must write nothing")
    # write_day itself
    raises(lambda: cbd.write_day(LogWriter(), d2, tables(w)[d1], {"table": cbd.TABLE}, rewrite=True), (gce,), "write_day rewrite on an empty partition")
    return True


def check_handler(root):
    h = p162()
    h.paths(root)
    handler = h.load(root / HANDLER_REL, "landing_rewrite_under_check")
    cbd = sys.modules["cottonwood_bd_account_return_daily"]
    gce = cbd.GoldWriteError
    need(handler.FLOOR_DAY == h.FLOOR and handler.MAX_BACKFILL_DAYS == 25, "FLOOR_DAY and MAX_BACKFILL_DAYS must stay %s and 25" % h.FLOOR)
    w = LogWriter()
    for d in (h.PREV, h.NEXT):
        handler.lambda_handler({"day": d}, None, s3=w, reader=h.reader())
    need(len(w.objs) == 4, "two legacy days must land four objects")
    landed = set(w.objs)
    n0 = len(w.log)
    out = handler.lambda_handler({"rewrite": {"start": h.PREV, "end": h.NEXT}}, None, s3=w, reader=h.reader())
    need(out.get("ok") is True and out.get("days") == [h.PREV, h.NEXT] and out.get("held") == 0, "the rewrite must answer ok, the two days and held 0: %s" % {k: out.get(k) for k in ("ok", "days", "held")})
    need(sorted(w.log[n0:]) == sorted(landed) and set(w.objs) == landed, "the rewrite must put exactly the four existing keys and create no other")
    for d, t in tables(w).items():
        need(t.schema.names[-1] == CLAIM_COL and len(t.schema.names) == 21, "day %s must be rewritten with 21 columns and the claim" % d)
    # every refusal comes before any write
    quiet = []
    cases = [
        ("a day that is not landed", {"rewrite": {"start": h.PREV, "end": "2026-07-15"}}, (ValueError,)),
        ("combined with day", {"rewrite": {"start": h.PREV, "end": h.NEXT}, "day": h.NEXT}, (ValueError,)),
        ("combined with days", {"rewrite": {"start": h.PREV, "end": h.NEXT}, "days": [h.NEXT]}, (ValueError,)),
        ("a spec without end", {"rewrite": {"start": h.PREV}}, (ValueError,)),
        ("a spec with an extra key", {"rewrite": {"start": h.PREV, "end": h.NEXT, "x": 1}}, (ValueError,)),
        ("a spec that is not an object", {"rewrite": "all"}, (ValueError,)),
        ("start after end", {"rewrite": {"start": h.NEXT, "end": h.PREV}}, (ValueError,)),
        ("a start before the floor", {"rewrite": {"start": "2026-07-09", "end": h.NEXT}}, (ValueError,)),
        ("a date that is not ISO", {"rewrite": {"start": "07/13/2026", "end": h.NEXT}}, (ValueError,)),
        ("a range of no trading day", {"rewrite": {"start": "2026-07-11", "end": "2026-07-12"}}, (ValueError,)),
        ("a range over the cap", {"rewrite": {"start": h.FLOOR, "end": "2026-09-30"}}, (SystemExit, ValueError)),
    ]
    n1 = len(w.log)
    for label, ev, kinds in cases:
        raises(lambda ev=ev: handler.lambda_handler(ev, None, s3=w, reader=h.reader()), kinds, label)
        quiet.append(label)
    need(len(w.log) == n1, "no refused rewrite may write anything")
    # the floor and the cap are checked on LANDED days, so only the rule itself can refuse them
    bucket, prefix = cbd.gold_prefix()
    w.objs["%sdate=2026-07-09/data.parquet" % prefix] = b"x"
    raises(lambda: handler.lambda_handler({"rewrite": {"start": "2026-07-09", "end": "2026-07-09"}}, None, s3=w, reader=h.reader()), (ValueError,), "a landed day before the floor")
    del w.objs["%sdate=2026-07-09/data.parquet" % prefix]
    keep = handler.MAX_BACKFILL_DAYS
    handler.MAX_BACKFILL_DAYS = 1
    try:
        raises(lambda: handler.lambda_handler({"rewrite": {"start": h.PREV, "end": h.NEXT}}, None, s3=w, reader=h.reader()), (SystemExit, ValueError), "two landed days over a cap of one")
    finally:
        handler.MAX_BACKFILL_DAYS = keep
    need(len(w.log) == n1, "no refused rewrite may write anything")
    # a dry run writes nothing
    handler.lambda_handler({"rewrite": {"start": h.PREV, "end": h.NEXT}, "dry_run": True}, None, s3=w, reader=h.reader())
    need(len(w.log) == n1, "a dry-run rewrite must write nothing")
    # the guard everywhere else
    raises(lambda: handler.lambda_handler({"day": h.NEXT}, None, s3=w, reader=h.reader()), (gce,), "a named landed day")
    raises(lambda: handler.lambda_handler({"days": [h.PREV]}, None, s3=w, reader=h.reader()), (gce,), "a named landed day in days")
    need(len(w.log) == n1, "the guard must hold on the named-day path")
    return True


def check_grant(changed):
    bad = [f for f in changed if f not in GRANT_FILES and not f.startswith(GRANT_PREFIXES)]
    need(not bad, "the worker's commits touch files outside its grant: %s" % bad[:3])
    need(CBD_REL in changed and HANDLER_REL in changed and TEST_REL in changed, "the adapter, the landing handler and the new test file must all change")
    return True


def check_facts(rec, n_tests):
    exp = {"event", "cap", "landed_days_only", "guard_unchanged", "deletes", "tests", "words"}
    need(isinstance(rec, dict) and set(rec) == exp, "record keys differ: %s" % (sorted(set(rec) ^ exp) if isinstance(rec, dict) else "?"))
    need(rec["event"] == {"rewrite": {"start": "YYYY-MM-DD", "end": "YYYY-MM-DD"}} and rec["cap"] == 25 and rec["landed_days_only"] is True and rec["guard_unchanged"] is True and rec["deletes"] == 0, "event, cap, landed-only, guard or deletes differ")
    need(isinstance(rec["tests"], int) and not isinstance(rec["tests"], bool) and rec["tests"] == n_tests >= 10, "tests must equal the recount, at least 10")
    need(nes(rec["words"]) and 80 <= len(rec["words"]) <= 1800 and not LONG_DIGITS.findall(rec["words"]), "words must be one paragraph of 80 to 1800 characters with no long digit run")
    return True


def run_pytest(root, args):
    r = subprocess.run([sys.executable, "-m", "pytest", "-q", "-p", "no:cacheprovider"] + list(args), cwd=str(root), capture_output=True, text=True, timeout=1500)
    m = re.search(r"(\d+) passed", r.stdout)
    need(r.returncode == 0 and m is not None, "tests failed: %s" % r.stdout[-300:].replace("\n", " | "))
    return int(m.group(1))


def run(root, cid):
    import json
    root = Path(root)
    if cid == "DB164-1-AC1":
        check_adapter(root)
        print("OK: the adapter's run_day with rewrite overwrites exactly a landed day's two keys with the derived 21-column table (no other key, no delete), a plain landing of a landed day is still refused, and a rewrite of an unlanded day, with no floor partition or with no floor day is refused before any put; a dry run writes nothing")
        return True
    if cid == "DB164-1-AC2":
        check_handler(root)
        print("OK: the landing handler's rewrite event overwrites the named landed days (the four existing keys, 21 columns with the claim), refuses before any write a day not landed, a combination with day or days, a malformed spec, start after end, a start before the floor, a non-ISO date, a range of no trading day and a range over the cap, writes nothing on a dry run, and the named-day path keeps the no-overwrite guard")
        return True
    if cid == "DB164-1-AC3":
        need((root / TEST_REL).is_file(), "no %s" % TEST_REL)
        n = run_pytest(root, [TEST_REL])
        n_dir = run_pytest(root, [TESTS_DIR, "--deselect", GOLD + "tests/" + KNOWN_RED])
        n_h = run_pytest(root, [HANDLER_DIR])
        need(n >= 10, "the new test file holds %d passing tests, at least 10 are owed" % n)
        changed = set()
        for cm in own_commits(root):
            changed |= set(git(root, "show", "--name-only", "--format=", cm).decode().split())
        check_grant(changed)
        check_facts(json.loads((root / REC_REL).read_bytes().decode("utf-8")), n)
        print("OK: %d new tests pass; the whole gold tests directory (%d, the one known pre-existing red deselected) and the landing handler's tests (%d) pass; %d files changed, all in the grant; the facts record equals the recount" % (n, n_dir, n_h, len(changed)))
        return True
    raise Fail("unknown criterion %s" % cid)


def selftest():
    def red(fn, label):
        try:
            fn()
        except Fail:
            return
        raise AssertionError("red arm passed: " + label)
    assert check_grant({CBD_REL, HANDLER_REL, TEST_REL, D + AUTHOR + "/x.json", HANDLER_DIR + "/tests/test_x.py"})
    red(lambda: check_grant({CBD_REL, HANDLER_REL}), "no test file")
    red(lambda: check_grant({CBD_REL, HANDLER_REL, TEST_REL, "lib/x.py"}), "outside grant")
    rec = {"event": {"rewrite": {"start": "YYYY-MM-DD", "end": "YYYY-MM-DD"}}, "cap": 25, "landed_days_only": True, "guard_unchanged": True, "deletes": 0, "tests": 10, "words": "w" * 100}
    assert check_facts(rec, 10)
    farms = (("event", lambda r: r.update(event={})), ("cap", lambda r: r.update(cap=50)), ("landed", lambda r: r.update(landed_days_only=False)), ("guard", lambda r: r.update(guard_unchanged=False)),
             ("deletes", lambda r: r.update(deletes=1)), ("tests", lambda r: r.update(tests=11)), ("extra", lambda r: r.update(z=1)), ("words", lambda r: r.update(words="short")),
             ("digits", lambda r: r.update(words="w" * 100 + " 123456789")))
    for label, fn in farms:
        r2 = copy.deepcopy(rec)
        fn(r2)
        red(lambda: check_facts(r2, 10), label)
    print("selftest: grant (2) and facts (%d) clauses behave; the behaviour clauses are exercised against a scratch reference and single-fault mutants by the issuer" % len(farms))
    print("selftest PASS")


if __name__ == "__main__":
    if sys.argv[1:2] == ["--selftest"]:
        selftest()
        sys.exit(0)
    try:
        run(sys.argv[1], sys.argv[2])
        print(sys.argv[2] + " PASS")
    except Exception as e:  # a failed read or clause is a FAIL, not a traceback
        print("FAIL: " + str(e))
        print(sys.argv[2] + " FAIL")
        sys.exit(1)
