"""IRPT_DASHBD round 148, workstream CONTRACT (issuer 2.0.0_SA_COO~D2) -- DB-b-286, the CLASS PRODUCER'S DATED CLASSIFICATION READ and the SUM-TO-ACCOUNT TEST (CTO msgs 8826/8827/8918: "~D2 adds the sum-to-account
test and the dated classification read (held, as_of) to the existing module; not tied to the swap snapshot"). Three things in `account_class_daily.py` and its tests:
(1) every GetItem the `ClassTable` makes stamps the identifier with the run-day it was read (an injectable clock), and `ClassTable.as_of(identifiers=None)` answers the OLDEST such date over the identifiers (None when none was read);
(2) `emit_class_day(..., classification_as_of=None)` writes `class_source.as_of` and `class_source.claim` = "held" into the day's manifest; the reporting-gold handler passes `ClassTable.as_of()` of the process-wide table;
(3) a NEW test file asserts the sum-to-account ties on synthetic account-days whose account value is given independently, and is KILLED-PROOF: it fails on each of four mutants of `class_contribution`.
The class table contract gains the same two facts in `class_source` (0.1.1). LOCAL: python, a JSON standard and tests; no AWS, no deploy.

  DB-b-286 (~230)   data/assets/scripts/gold/irpt_reporting/account_class_daily.py + infra/aws/lambda/investor-reporting/reporting-gold/handler.py (one call site) + org/standards/IRPT_DASHBD_ACCOUNT_CLASS_DAILY_CONTRACT.json (0.1.1)
                    + data/assets/scripts/gold/irpt_reporting/tests/test_account_class_dated_and_sum.py + a facts record
                    DB154-1-AC1 (BEHAVIOUR of the dating and the manifest, the pure functions byte-identical to the base, the handler passes the date, the contract's two facts),
                    DB154-1-AC2 (MUTATION: the new test file passes on the module and fails on each of four mutants of class_contribution),
                    DB154-1-AC3 (the new tests, the existing class tests, the grant, the facts record)

Usage: python <this file> <repo_root> <criterion_id>      prints "<id> PASS" or "<id> FAIL" last
       python <this file> --selftest                       the pure clauses on synthetic arms
"""
import ast
import copy
import datetime as dt
import importlib.util
import json
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

D = "org/missions/D9/IRPT/IRPT_DASHBD/deliverables/"
MOD_REL = "data/assets/scripts/gold/irpt_reporting/account_class_daily.py"
HANDLER_REL = "infra/aws/lambda/investor-reporting/reporting-gold/handler.py"
CONTRACT_REL = "org/standards/IRPT_DASHBD_ACCOUNT_CLASS_DAILY_CONTRACT.json"
TEST_DIR = "data/assets/scripts/gold/irpt_reporting/tests/"
TEST_REL = TEST_DIR + "test_account_class_dated_and_sum.py"
EXISTING_TEST = TEST_DIR + "test_account_class_daily.py"
AUTHOR = "0.9.0_WK_IRPT_DASHBD~230"
REC_REL = D + AUTHOR + "/RD_CLASS_DATED_FACTS_R148.json"
ORDER_REL = "org/missions/D9/IRPT/IRPT_DASHBD/task-orders/IRPT_DASHBD.TO-DB-b-286.class-producer-dated-read-and-sum-test.md"
GRANT_FILES = {MOD_REL, HANDLER_REL, CONTRACT_REL, TEST_REL}
GRANT_PREFIXES = (D + AUTHOR + "/", "org/missions/D9/IRPT/IRPT_DASHBD/surprise-channel/investigations/", "org/missions/D9/IRPT/IRPT_DASHBD/task-orders/")
UNCHANGED = ("class_contribution", "account_day_rows", "classify_identifier", "positions_by_class", "check_class_rows", "class_values", "holding_identifier", "unclassified_share")
COPY_DIRS = ["data/assets/scripts", "lib", "infra/aws/lambda/v2_portal/_shared", "infra/logic/registry", "org/standards"]
MUTANTS = (
    ("the tie is dropped", "return (total == total and v == v) and abs(total - v) <= tol", "return True"),
    ("the denominator is today's value", "(adj_t.get(cls, 0.0) - adj_p.get(cls, 0.0) - flows.get(cls, 0.0)) / float(v_p)", "(adj_t.get(cls, 0.0) - adj_p.get(cls, 0.0) - flows.get(cls, 0.0)) / float(v_t)"),
    ("the cash class takes no flow residual", "flows[CLASS_CASH] = float(f_t) - sum(flows.values())", "flows[CLASS_CASH] = float(f_t)"),
    ("cash is not made exact", "out[CLASS_CASH] = v - sum(out.values())", "out[CLASS_CASH] = mv.get(CLASS_CASH, 0.0)"),
)
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
    return r.stdout.decode("utf-8", "replace")


def base_commit(root):
    out = git(root, "log", "--diff-filter=A", "--format=%H", "--", ORDER_REL).split()
    need(out, "the order's first commit is not in this history")
    return out[-1]


def own_commits(root):
    out = git(root, "log", "--reverse", "--format=%H", "--author=" + AUTHOR, base_commit(root) + "..HEAD").split()
    need(out, "no commit by %s since the order was issued" % AUTHOR)
    return out


def segments(src):
    tree = ast.parse(src)
    return {n.name: ast.get_source_segment(src, n) for n in tree.body if isinstance(n, (ast.FunctionDef, ast.ClassDef))}


# ------------------------------------------------------------------------------------------------ the pure clauses
def check_unchanged(base_src, new_src):
    a, b = segments(base_src), segments(new_src)
    for name in UNCHANGED:
        need(name in a and name in b and a[name] == b[name], "the pure function %s changed (it must keep its exact source)" % name)
    return len(UNCHANGED)


def check_handler(src):
    tree = ast.parse(src)
    fn = next((n for n in tree.body if isinstance(n, ast.FunctionDef) and n.name == "emit_classes"), None)
    need(fn is not None, "the handler has no emit_classes")
    calls = [n for n in ast.walk(fn) if isinstance(n, ast.Call) and isinstance(n.func, ast.Attribute) and n.func.attr == "emit_class_day"]
    need(calls, "emit_classes no longer calls emit_class_day")
    for c in calls:
        kw = {k.arg: k.value for k in c.keywords}
        need("classification_as_of" in kw, "an emit_class_day call in emit_classes does not pass classification_as_of")
        seg = ast.get_source_segment(src, kw["classification_as_of"]) or ""
        need("_CLASS_TABLE" in seg and "as_of" in seg and "default_table" not in seg,
             "classification_as_of must come from the ClassTable THIS RUN read through (module global _CLASS_TABLE.as_of()), never default_table(); read %r" % seg[:80])
    cd = next((n for n in tree.body if isinstance(n, ast.FunctionDef) and n.name == "class_days"), None)
    need(cd is not None, "the handler has no class_days")
    need(any(isinstance(n, ast.Global) and "_CLASS_TABLE" in n.names for n in ast.walk(cd)), "class_days must declare `global _CLASS_TABLE`")
    sets = [n for n in ast.walk(cd) if isinstance(n, ast.Assign) and any(isinstance(t, ast.Name) and t.id == "_CLASS_TABLE" for t in n.targets)]
    need(sets, "class_days must assign _CLASS_TABLE the table it passes to compute_classes")
    passes = [k for n in ast.walk(cd) if isinstance(n, ast.Call) and isinstance(n.func, ast.Attribute) and n.func.attr == "compute_classes" for k in n.keywords if k.arg == "table"]
    need(passes and all("ClassTable()" not in (ast.get_source_segment(src, k.value) or "") for k in passes), "compute_classes must receive the SAME table object that _CLASS_TABLE holds, not a fresh ClassTable() expression")
    need(any(isinstance(n, ast.Assign) and any(isinstance(t, ast.Name) and t.id == "_CLASS_TABLE" for t in n.targets) for n in tree.body), "the module must define _CLASS_TABLE at top level (None until class_days runs)")
    return len(calls)


def check_contract(base, c):
    need(base["contract_version"] == "0.1.0" and c.get("contract_version") == "0.1.1", "contract_version must be 0.1.1 over a 0.1.0 base")
    moved = sorted(k for k in set(base) | set(c) if k not in ("contract_version", "class_source") and base.get(k) != c.get(k))
    need(not moved, "sections changed beyond contract_version and class_source: %s" % moved)
    cb, cn = base["class_source"], c["class_source"]
    need(all(cb[k] == cn.get(k) for k in cb), "an earlier class_source key changed")
    extra = set(cn) - set(cb)
    need(extra == {"as_of", "claim"}, "class_source must gain exactly as_of and claim, gained %s" % sorted(extra))
    need(nes(cn["as_of"]) and "oldest" in cn["as_of"] and "GetItem" in cn["as_of"] and "swap" in cn["as_of"].lower(), "class_source.as_of must say: the oldest GetItem date, taken at run time, not the swap snapshot")
    need(cn["claim"] == "held", "class_source.claim must be exactly held")
    return True


class _Table:
    def __init__(self, items):
        self.items = items

    def get_item(self, Key):
        v = self.items.get(Key["ticker"])
        return {"Item": {"ticker": Key["ticker"], "asset_class": v}} if v is not None else {}


class _Client:
    def __init__(self, items):
        self.table = _Table(items)


class _S3:
    def __init__(self):
        self.puts = {}

    def put_object(self, Bucket, Key, Body, **kw):
        self.puts[Key] = bytes(Body)


def load_mod(path, name):
    spec = importlib.util.spec_from_file_location(name, str(path))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def check_behaviour(mod):
    days = iter(["2026-10-14", "2026-10-15", "2026-10-15"])
    t = mod.ClassTable(classifier=_Client({"AAA": "equity", "BBB": "fixed_income"}), clock=lambda: next(days))
    need(t.as_of() is None and t.as_of(["AAA"]) is None, "before any read as_of() must be None")
    t.get("ZZZ")
    t.get("AAA")
    t.get("BBB")
    need(t.as_of() == "2026-10-14", "as_of() must be the OLDEST read date over every identifier read, an absent item included: %s" % t.as_of())
    need(t.as_of(["AAA"]) == "2026-10-15" and t.as_of(["BBB", "ZZZ"]) == "2026-10-14" and t.as_of(["BBB"]) == "2026-10-15", "as_of(identifiers) is the oldest date over those identifiers (an item the table does not hold was read too)")
    need(t.as_of(["NEVER"]) is None, "as_of of an identifier never read is None")
    t.get("ZZZ")
    t.get("AAA")
    need(t.as_of(["ZZZ"]) == "2026-10-14" and t.as_of(["AAA"]) == "2026-10-15" and t.reads == 3, "a cached get never re-stamps and never re-reads")
    default = mod.ClassTable(classifier=_Client({"AAA": "equity"}))
    default.get("AAA")
    need(default.as_of() == dt.datetime.now(dt.timezone.utc).date().isoformat() or default.as_of() == (dt.datetime.now(dt.timezone.utc).date() - dt.timedelta(days=1)).isoformat(), "the default clock is the UTC run-day")
    c = mod.class_contribution(110.0, 100.0, 0.0, {"equity": 70.0, "fixed_income": 40.0}, {"equity": 60.0, "fixed_income": 40.0}, {})
    need(c["coverage"] == mod.COV_MEASURED, "fixture contribution must be measured")
    firm = mod.ard.opal_naming.lookup("cottonwood")["key"]
    rows = mod.account_day_rows(firm, "A0000000001", "2026-10-14", c, c["coverage"])
    saved = mod.ard.sp.stream_to_parquet
    mod.ard.sp.stream_to_parquet = lambda tables, schema, s3, bucket, key: {"rows": 1, "key": key}
    try:
        for given, want in (("2026-10-14", "2026-10-14"), (None, None)):
            s3 = _S3()
            mod.emit_class_day(s3, rows, firm, "2026-10-14", upload=True, classification_as_of=given)
            man = json.loads(next(v for k, v in s3.puts.items() if k.endswith("manifest.json")).decode("utf-8"))
            cs = man["class_source"]
            need(cs.get("as_of") == want and cs.get("claim") == "held", "manifest class_source must carry as_of %r and claim held, read %s" % (want, cs))
            need(cs.get("table") == mod.CLASSIFICATION_TABLE and cs.get("key") == mod.CLASSIFICATION_KEY and cs.get("read") == mod.CLASSIFICATION_READ, "the earlier class_source keys must stay")
        s3 = _S3()
        mod.emit_class_day(s3, rows, firm, "2026-10-14", upload=True)
        need(json.loads(next(v for k, v in s3.puts.items() if k.endswith("manifest.json")).decode("utf-8"))["class_source"]["as_of"] is None, "no classification_as_of -> as_of null, still claim held")
    finally:
        mod.ard.sp.stream_to_parquet = saved
    return True


def mutate(tree_root, name, old, new):
    p = Path(tree_root) / MOD_REL
    s = p.read_text(encoding="utf-8")
    need(s.count(old) == 1, "mutant anchor for %r not found exactly once in the module" % name)
    p.write_text(s.replace(old, new), encoding="utf-8", newline="\n")


def make_tree(root):
    tmp = Path(tempfile.mkdtemp(prefix="p154_"))
    for d in COPY_DIRS:
        shutil.copytree(Path(root) / d, tmp / d, ignore=shutil.ignore_patterns("__pycache__", ".pytest_cache"))
    return tmp


def pytest_in(tree, rel):
    r = subprocess.run([sys.executable, "-m", "pytest", "-q", "-p", "no:cacheprovider", rel], cwd=str(tree), capture_output=True, text=True, timeout=900)
    m = re.search(r"(\d+) passed", r.stdout)
    return r.returncode, int(m.group(1)) if m else 0, r.stdout[-200:].replace("\n", " | ")


def check_mutation(root):
    tree = make_tree(root)
    try:
        rc, n, tail = pytest_in(tree, TEST_REL)
        need(rc == 0 and n >= 6, "the new test file must PASS on the module itself, with at least 6 tests: %s" % tail)
        for name, old, new in MUTANTS:
            t2 = make_tree(root)
            try:
                mutate(t2, name, old, new)
                rc2, _n2, tail2 = pytest_in(t2, TEST_REL)
                need(rc2 != 0, "the new test file does NOT fail on the mutant %r: it does not prove the classes sum to the account" % name)
            finally:
                shutil.rmtree(t2, ignore_errors=True)
        return n
    finally:
        shutil.rmtree(tree, ignore_errors=True)


def check_grant(changed):
    bad = [f for f in changed if f not in GRANT_FILES and not f.startswith(GRANT_PREFIXES)]
    need(not bad, "the worker's commits touch files outside its grant: %s" % bad[:3])
    need(MOD_REL in changed and TEST_REL in changed and CONTRACT_REL in changed and HANDLER_REL in changed, "the module, the handler call site, the contract and the new test must all change")
    return True


def check_facts(rec, n_tests):
    exp = {"as_of_rule", "claim", "mutants_killed", "tests", "words"}
    need(isinstance(rec, dict) and set(rec) == exp, "record keys differ: %s" % (sorted(set(rec) ^ exp) if isinstance(rec, dict) else "?"))
    need(rec["as_of_rule"] == "oldest GetItem read date over the identifiers used" and rec["claim"] == "held" and rec["mutants_killed"] == len(MUTANTS), "as_of_rule, claim or mutants_killed differ")
    need(rec["tests"] == n_tests and isinstance(rec["tests"], int) and rec["tests"] >= 6, "tests must equal the recount, at least 6")
    need(nes(rec["words"]) and 80 <= len(rec["words"]) <= 1800 and not LONG_DIGITS.findall(rec["words"]), "words must be one paragraph of 80 to 1800 characters with no long digit run")
    return True


def run(root, cid):
    root = Path(root)
    base = base_commit(root)
    if cid == "DB154-1-AC1":
        mod = load_mod(root / MOD_REL, "acd_under_check")
        base_src = git(root, "show", "%s:%s" % (base, MOD_REL))
        n = check_unchanged(base_src, (root / MOD_REL).read_bytes().decode("utf-8"))
        check_behaviour(mod)
        calls = check_handler((root / HANDLER_REL).read_bytes().decode("utf-8"))
        check_contract(json.loads(git(root, "show", "%s:%s" % (base, CONTRACT_REL))), json.loads((root / CONTRACT_REL).read_bytes().decode("utf-8")))
        print("OK: dating: as_of() is the oldest GetItem read date (an injected clock; cached gets never re-stamp; none read -> None); the manifest's class_source carries as_of and claim held; %d pure functions keep their exact source; the handler passes the date at %d call site(s); the class contract 0.1.1 gains exactly as_of and claim" % (n, calls))
        return True
    if cid == "DB154-1-AC2":
        need((root / TEST_REL).is_file(), "no %s" % TEST_REL)
        n = check_mutation(root)
        print("OK: mutation: the new test file passes on the module (%d tests) and FAILS on each of %d mutants of class_contribution (the tie dropped, the wrong denominator, no cash flow residual, cash not exact)" % (n, len(MUTANTS)))
        return True
    if cid == "DB154-1-AC3":
        need((root / TEST_REL).is_file(), "no %s" % TEST_REL)
        rc, n, tail = pytest_in(root, TEST_REL)
        need(rc == 0 and n >= 6, "the new test file must hold at least 6 passing tests: %s" % tail)
        rc2, n2, tail2 = pytest_in(root, EXISTING_TEST)
        need(rc2 == 0, "the existing class tests must pass: %s" % tail2)
        changed = set()
        for cm in own_commits(root):
            changed |= set(git(root, "show", "--name-only", "--format=", cm).split())
        check_grant(changed)
        check_facts(json.loads((root / REC_REL).read_bytes().decode("utf-8")), n)
        print("OK: %d new tests and the existing class file's %d pass; %d files changed, all in the grant; the facts record equals the recount" % (n, n2, len(changed)))
        return True
    raise Fail("unknown criterion %s" % cid)


def selftest():
    def red(fn, label):
        try:
            fn()
        except Fail:
            return
        raise AssertionError("red arm passed: " + label)
    base_src = "def class_contribution():\n    return 1\n\ndef account_day_rows():\n    return 2\n\ndef classify_identifier():\n    return 3\n\ndef positions_by_class():\n    return 4\n\ndef check_class_rows():\n    return 5\n\ndef class_values():\n    return 6\n\ndef holding_identifier():\n    return 7\n\ndef unclassified_share():\n    return 8\n\ndef emit_class_day():\n    return 9\n"
    assert check_unchanged(base_src, base_src.replace("return 9", "return 90") + "\ndef extra():\n    return 0\n") == len(UNCHANGED)
    for nm in UNCHANGED:
        red(lambda: check_unchanged(base_src, base_src.replace("def %s():\n    return" % nm, "def %s():\n    return 100 +" % nm)), "changed " + nm)
    h = ("_CLASS_TABLE = None\n\n\ndef class_days(s3, firm, days):\n    global _CLASS_TABLE\n    table = acd.ClassTable()\n    _CLASS_TABLE = table\n    return acd.compute_classes(s3, 1, firm, days, table=table)\n\n\ndef emit_classes(s3, firm, days, upload):\n    for day in days:\n        res = acd.emit_class_day(s3, rows[day], firm, day, upload=upload, classification_as_of=(_CLASS_TABLE.as_of() if _CLASS_TABLE is not None else None))\n")
    ARG = ", classification_as_of=(_CLASS_TABLE.as_of() if _CLASS_TABLE is not None else None)"
    EXPR = "(_CLASS_TABLE.as_of() if _CLASS_TABLE is not None else None)"
    assert check_handler(h) == 1
    red(lambda: check_handler(h.replace(ARG, "")), "no kw")
    red(lambda: check_handler(h.replace(EXPR, "acd.default_table().as_of()")), "default_table")
    red(lambda: check_handler(h.replace(EXPR, "'2026-01-01'")), "typed date")
    red(lambda: check_handler(h.replace("    global _CLASS_TABLE" + chr(10), "")), "no global")
    red(lambda: check_handler(h.replace("    _CLASS_TABLE = table" + chr(10), "")), "no assign")
    red(lambda: check_handler(h.replace("table=table)", "table=acd.ClassTable())")), "fresh table passed")
    red(lambda: check_handler(h.replace("_CLASS_TABLE = None" + chr(10) + chr(10) + chr(10), "", 1)), "no module global")
    red(lambda: check_handler("def other():" + chr(10) + "    pass" + chr(10)), "no emit_classes")
    base = {"contract_version": "0.1.0", "class_source": {"table": "t", "key": "k", "read": "GetItem"}, "x": 1}
    good = copy.deepcopy(base)
    good["contract_version"] = "0.1.1"
    good["class_source"].update({"as_of": "the oldest GetItem date over the identifiers used, taken at run time; not the swap snapshot", "claim": "held"})
    assert check_contract(base, good)
    arms = (("version", lambda x: x.update(contract_version="0.1.0")), ("other key", lambda x: x.update(x=2)), ("earlier key", lambda x: x["class_source"].update(read="Scan")),
            ("claim", lambda x: x["class_source"].update(claim="measured")), ("as_of words", lambda x: x["class_source"].update(as_of="a date")), ("extra", lambda x: x["class_source"].update(z=1)),
            ("missing", lambda x: x["class_source"].pop("claim")))
    for label, fn in arms:
        x = copy.deepcopy(good)
        fn(x)
        red(lambda: check_contract(base, x), label)
    assert check_grant({MOD_REL, HANDLER_REL, CONTRACT_REL, TEST_REL, D + AUTHOR + "/x.json"})
    red(lambda: check_grant({MOD_REL, HANDLER_REL, CONTRACT_REL, TEST_REL, "lib/x.py"}), "outside grant")
    red(lambda: check_grant({MOD_REL, CONTRACT_REL, TEST_REL}), "no handler")
    rec = {"as_of_rule": "oldest GetItem read date over the identifiers used", "claim": "held", "mutants_killed": len(MUTANTS), "tests": 7, "words": "w" * 100}
    assert check_facts(rec, 7)
    farms = (("rule", lambda r: r.update(as_of_rule="newest")), ("claim", lambda r: r.update(claim="measured")), ("mutants", lambda r: r.update(mutants_killed=2)), ("tests", lambda r: r.update(tests=9)),
             ("extra", lambda r: r.update(z=1)), ("words", lambda r: r.update(words="short")), ("digits", lambda r: r.update(words="w" * 100 + " 123456789")))
    for label, fn in farms:
        r2 = copy.deepcopy(rec)
        fn(r2)
        red(lambda: check_facts(r2, 7), label)
    print("selftest: unchanged (%d red arms), handler (8), contract (%d), grant (2) and facts (%d) clauses behave" % (len(UNCHANGED), len(arms), len(farms)))
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
