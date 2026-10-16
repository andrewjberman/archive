"""IRPT_DASHBD round 147, workstream B-49F + contract (issuer 2.0.0_SA_COO~D2) -- DB-b-280, the COTTONWOOD SERIES PUBLISH HANDLER: one Lambda handler that reads the Cottonwood gold
`account_return_daily` partitions from the floor day (2026-07-10), builds each account's series and manifest with the reporting-publish module's pure functions (DB-b-279) and, only when asked
(event upload is exactly True), writes them at the naming builder's platinum `reporting` address. It is new SERVED output when it runs; this cell runs nothing. LOCAL: python files only.

  DB-b-280 (~226)   infra/aws/lambda/investor-reporting/reporting-publish-cot/handler.py + tests/test_handler.py + a facts record
                    DB147-2-AC1 (BEHAVIOUR on a fake S3 holding synthetic gold parquet: the floor, the dry run, the upload keys, the account filter, the upload switch, the contract guard, the summary),
                    DB147-2-AC2 (DISCIPLINE: no typed bucket, firm or key; stdlib + boto3 + pyarrow + the publisher + the naming builder + the calendar only; no account id printed),
                    DB147-2-AC3 (the worker's tests, the grant, the facts record)

Usage: python <this file> <repo_root> <criterion_id>      prints "<id> PASS" or "<id> FAIL" last
       python <this file> --selftest                       the pure clauses on synthetic arms
"""
import ast
import copy
import datetime as dt
import gzip
import importlib.util
import io
import json
import re
import subprocess
import sys
import tempfile
from pathlib import Path

D = "org/missions/D9/IRPT/IRPT_DASHBD/deliverables/"
HANDLER_REL = "infra/aws/lambda/investor-reporting/reporting-publish-cot/handler.py"
TEST_REL = "infra/aws/lambda/investor-reporting/reporting-publish-cot/tests/test_handler.py"
CONTRACT_REL = "org/standards/IRPT_DASHBD_SERIES_CONTRACT.json"
AUTHOR = "0.9.0_WK_IRPT_DASHBD~226"
REC_REL = D + AUTHOR + "/RD_COT_PUBLISH_HANDLER_FACTS_R147.json"
ORDER_REL = "org/missions/D9/IRPT/IRPT_DASHBD/task-orders/IRPT_DASHBD.TO-DB-b-280.cottonwood-series-publish-handler.md"
SIBLING_FILES = {"infra/aws/lambda/investor-reporting/reporting-publish/publisher.py", "infra/aws/lambda/investor-reporting/reporting-publish/tests/test_publisher_unreported.py", "infra/aws/lambda/investor-reporting/reporting-publish-cot/handler.py", "infra/aws/lambda/investor-reporting/reporting-publish-cot/tests/test_handler.py", "infra/aws/lambda/ci/lambda-source-map.json"}  # chain B: the other cells of the same worker on the same branch
SIBLING_PREFIXES = ("infra/aws/terraform/investor-reporting/reporting-publish-iso/", "infra/aws/lambda/investor-reporting/reporting-publish-cot/")
PRIOR_CELL_FILES = SIBLING_FILES
GRANT_FILES = {HANDLER_REL, TEST_REL} | SIBLING_FILES
GRANT_PREFIXES = SIBLING_PREFIXES + (D + AUTHOR + "/", "org/missions/D9/IRPT/IRPT_DASHBD/surprise-channel/investigations/", "org/missions/D9/IRPT/IRPT_DASHBD/task-orders/", "infra/aws/lambda/investor-reporting/reporting-publish-cot/tests/")
FLOOR = "2026-07-10"
FIXED = "trading calendar minus present partitions"
SUMMARY_KEYS = {"ok", "uploaded", "floor", "partitions", "first", "last", "accounts_seen", "accounts_named", "published", "refused", "refusals", "skipped_null_account", "unreported_trading_days", "seconds"}
ALLOWED_IMPORTS = {"__future__", "io", "json", "sys", "time", "datetime", "pathlib", "concurrent", "concurrent.futures", "boto3", "botocore", "pyarrow", "opal_naming", "publisher", "trading_calendar", "logging", "re", "zlib", "os"}
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


def load_module(path, name):
    spec = importlib.util.spec_from_file_location(name, str(path))
    mod = importlib.util.module_from_spec(spec)
    sys.modules[name] = mod
    spec.loader.exec_module(mod)
    return mod


def own_commits(root):
    base = git(root, "log", "--diff-filter=A", "--format=%H", "--", ORDER_REL).decode().split()
    need(base, "the order's first commit is not in this history")
    out = git(root, "log", "--reverse", "--format=%H", "--author=" + AUTHOR, base[-1] + "..HEAD").decode().split()
    need(out, "no commit by %s since the order was issued" % AUTHOR)
    return out


# ------------------------------------------------------------------------------------------------ the fake S3 and the fixture
class FakeS3:
    def __init__(self, objects):
        self.objects = dict(objects)
        self.gets, self.puts, self.heads, self.lists = [], {}, [], 0
        self.forbidden = ()

    def get_paginator(self, name):
        need(name == "list_objects_v2", "only list_objects_v2 is paginated")
        outer = self

        class Pg:
            def paginate(self, Bucket, Prefix):
                outer.lists += 1
                yield {"Contents": [{"Key": k, "Size": len(v)} for k, v in sorted(outer.objects.items()) if k.startswith(Prefix)]}
        return Pg()

    def get_object(self, Bucket, Key):
        need(not any(Key.startswith(f) for f in self.forbidden), "the handler read a forbidden key")
        self.gets.append(Key)
        return {"Body": io.BytesIO(self.objects[Key])}

    def put_object(self, Bucket, Key, Body, ContentType=None, **kw):
        need(not kw, "put_object takes Bucket, Key, Body, ContentType only")
        self.puts[Key] = bytes(Body)
        self.objects[Key] = bytes(Body)
        return {}

    def head_object(self, Bucket, Key):
        self.heads.append(Key)
        return {"ContentLength": len(self.objects[Key])}


def trading(tc, a, b):
    return [d.isoformat() for d in tc.trading_days_between(dt.date.fromisoformat(a), dt.date.fromisoformat(b))]


def parquet_bytes(rows, cols):
    import pyarrow as pa
    import pyarrow.parquet as pq
    table = pa.table({c: [r.get(c) for r in rows] for c in cols})
    buf = io.BytesIO()
    pq.write_table(table, buf)
    return buf.getvalue()


def fixture(root, tc, naming):
    """-> (FakeS3, expectations). Gold for the Cottonwood firm: two pre-floor partitions (poisoned), floor-era partitions 2026-07-10 .. 2026-07-24 less 2026-07-15 (no partition), accounts A, B, C and a null id."""
    cols = ["account_id", "business_date", "market_value_eod", "total_return_daily", "return_basis", "day_quality", "external_flow", "income_received", "holdings_price_return", "method_version", "history_scope"]
    firm = naming.lookup("cottonwood")["key"]
    probe = str(naming.address("irpt", firm, "gold", "account_return_daily", "date=2026-07-10", "data.parquet"))
    bucket, key = probe[len("s3://"):].partition("/")[::2]
    prefix = key.rsplit("/date=", 1)[0] + "/"
    present = [d for d in trading(tc, "2026-07-10", "2026-07-24") if d != "2026-07-15"]
    pre = ["2026-07-08", "2026-07-09"]

    def row(acct, d, i, value=100.0):
        first = i == 0
        return {"account_id": acct, "business_date": d, "market_value_eod": value + i, "total_return_daily": None if first else 0.001, "return_basis": "NOT_MEASURABLE" if first else "TWR",
                "day_quality": "NOT_MEASURABLE" if first else "MEASURED", "external_flow": 0.0, "income_received": None, "holdings_price_return": None, "method_version": 3, "history_scope": "PARTIAL_HISTORY"}
    objs, a_rows, b_rows = {}, [], []
    for d in pre:
        objs["%sdate=%s/data.parquet" % (prefix, d)] = parquet_bytes([{"account_id": "A0000000001", "business_date": d, "market_value_eod": None, "total_return_daily": None, "return_basis": "NOT_MEASURABLE",
                                                                      "day_quality": "NOT_MEASURABLE", "external_flow": None, "income_received": None, "holdings_price_return": None, "method_version": 1, "history_scope": "PARTIAL_HISTORY"}], cols)
    b_days = [d for d in present if "2026-07-13" <= d <= "2026-07-22"]
    for d in present:
        rows = [row("A0000000001", d, present.index(d))]
        if d in b_days:
            rows.append(row("B0000000002", d, b_days.index(d), 200.0))
        rows.append(row("C0000000003", d, 1, 0.0) | {"market_value_eod": 0.0})
        if d == "2026-07-10":
            rows.append(row(None, d, 1))
        objs["%sdate=%s/data.parquet" % (prefix, d)] = parquet_bytes(rows, cols)
    exp = {"present": present, "firm": firm, "a_first": present[0], "a_last": present[-1], "b_first": b_days[0], "b_last": b_days[-1], "bucket": bucket,
           "a_unreported": ["2026-07-15"], "b_unreported": ["2026-07-15"], "pre_prefixes": ["%sdate=%s/" % (prefix, d) for d in pre], "accounts": ["A0000000001", "B0000000002", "C0000000003"],
           "global_unreported": ["2026-07-15"]}
    del a_rows, b_rows
    s3 = FakeS3(objs)
    s3.forbidden = tuple(exp["pre_prefixes"])
    return s3, exp


def series_key(naming, firm, acct, obj):
    return str(naming.address("irpt", firm, "platinum", "reporting", "account=%s" % acct, obj))[len("s3://"):].partition("/")[2]


# ------------------------------------------------------------------------------------------------ the clauses
def check_behaviour(root, handler=None):
    root = Path(root)
    naming = load_module(root / "lib" / "opal_naming.py", "opal_naming")
    tc = load_module(root / "lib" / "trading_calendar.py", "trading_calendar")
    mod = load_module(handler or (root / HANDLER_REL), "cot_handler")
    for name in ("FIRM", "FLOOR_DAY", "_ROOT", "CONTRACT_REL", "lambda_handler"):
        need(hasattr(mod, name), "the handler must define %s" % name)
    need(mod.FLOOR_DAY == FLOOR, "FLOOR_DAY must be %s" % FLOOR)
    s3, ex = fixture(root, tc, naming)
    need(mod.FIRM == ex["firm"], "FIRM must come from the registry")
    # dry run (no upload key), and the three non-True switches
    for ev in ({}, {"upload": False}, {"upload": "true"}, {"upload": 1}):
        s3.puts.clear()
        out = mod.lambda_handler(dict(ev), None, s3)
        need(not s3.puts, "an event %s must not write" % ev)
        need(out["uploaded"] is False, "uploaded must be false for %s" % ev)
    need(set(out) == SUMMARY_KEYS, "the summary keys differ: %s" % sorted(set(out) ^ SUMMARY_KEYS))
    need(out["partitions"] == len(ex["present"]) and out["first"] == ex["present"][0] and out["last"] == ex["present"][-1] and out["floor"] == FLOOR, "partitions, first, last or floor differ")
    need(out["accounts_seen"] == 3 and out["accounts_named"] == 3 and out["published"] == 2 and out["refused"] == 1 and sum(out["refusals"].values()) == 1 and out["skipped_null_account"] == 1, "the account counts differ: %s" % {k: out[k] for k in ("accounts_seen", "accounts_named", "published", "refused", "skipped_null_account")})
    need(out["unreported_trading_days"] == ex["global_unreported"], "the summary lists the trading days with no partition from the floor: %s" % out["unreported_trading_days"])
    need(all(isinstance(v, int) for v in out["refusals"].values()) and not any(a in " ".join(out["refusals"]) for a in ex["accounts"]), "refusals are reason -> count and name no account")
    need(not any(g.startswith(f) for g in s3.gets for f in ex["pre_prefixes"]), "a pre-floor partition was read")
    # the real upload
    s3.puts.clear()
    out = mod.lambda_handler({"upload": True}, None, s3)
    want = {series_key(naming, ex["firm"], a, o) for a in ("A0000000001", "B0000000002") for o in ("series.json.gz", "manifest.json")}
    need(set(s3.puts) == want, "an upload writes exactly the series and manifest of the two accounts that build, at the builder's address: %s" % sorted(set(s3.puts) ^ want)[:3])
    need(out["uploaded"] is True and out["published"] == 2, "the upload summary")
    for acct, first, last, unrep in (("A0000000001", ex["a_first"], ex["a_last"], ex["a_unreported"]), ("B0000000002", ex["b_first"], ex["b_last"], ex["b_unreported"])):
        gz = s3.puts[series_key(naming, ex["firm"], acct, "series.json.gz")]
        s = json.loads(gzip.decompress(gz).decode("utf-8"))
        need(s["first_data_date"] == first and s["as_of"] == last, "%s window differs" % acct[:1])
        need(s["income"] == [None] * len(s["date"]), "%s income must stay null" % acct[:1])
        need(s["unreported_trading_days"] == unrep and s["unreported_trading_days_basis"] == FIXED, "%s unreported days differ: %s" % (acct[:1], s["unreported_trading_days"]))
        m = json.loads(s3.puts[series_key(naming, ex["firm"], acct, "manifest.json")].decode("utf-8"))
        need(m["firm"] == ex["firm"] and m["account_id"] == acct and m["byte_sizes"]["series.json.gz"] == len(gz) and m["publisher_version"] == "0.2.0", "%s manifest differs" % acct[:1])
    need(len(s3.heads) >= 2, "the handler reads back the stored series size (head_object)")
    # the account filter
    s3.puts.clear()
    out = mod.lambda_handler({"upload": True, "accounts": ["A0000000001"]}, None, s3)
    need(set(s3.puts) == {series_key(naming, ex["firm"], "A0000000001", o) for o in ("series.json.gz", "manifest.json")} and out["accounts_named"] == 1 and out["published"] == 1, "the account filter publishes only the named account")
    # the contract guard: a contract that names no unreported-days field refuses before any S3 call
    tmp = Path(tempfile.mkdtemp(prefix="p148_"))
    (tmp / "org" / "standards").mkdir(parents=True)
    c = json.loads((root / CONTRACT_REL).read_bytes().decode("utf-8"))
    c["series"]["optional"] = [k for k in c["series"]["optional"] if not k.startswith("unreported_")]
    (tmp / "org" / "standards" / "IRPT_DASHBD_SERIES_CONTRACT.json").write_text(json.dumps(c), encoding="utf-8")
    keep, s3b = mod._ROOT, FakeS3({})
    mod._ROOT = tmp
    try:
        try:
            mod.lambda_handler({"upload": True}, None, s3b)
        except SystemExit as e:
            need("REFUSED" in str(e), "the contract refusal reads REFUSED")
        else:
            raise Fail("a contract that names no unreported-days field must refuse")
    finally:
        mod._ROOT = keep
    need(s3b.lists == 0 and not s3b.puts, "the contract guard runs before any S3 call")
    return True


def check_discipline(src, naming_buckets):
    tree = ast.parse(src)
    mods = set()
    for n in ast.walk(tree):
        if isinstance(n, ast.Import):
            mods |= {a.name for a in n.names}
        elif isinstance(n, ast.ImportFrom) and n.level == 0 and n.module:
            mods.add(n.module)
    bad = sorted(m for m in mods if m.split(".")[0] not in ALLOWED_IMPORTS and m not in ALLOWED_IMPORTS)
    need(not bad, "imports outside stdlib, boto3, pyarrow, the publisher, the naming builder and the calendar: %s" % bad)
    docs = {id(n.value) for n in ast.walk(tree) if isinstance(n, ast.Expr) and isinstance(n.value, ast.Constant)}
    lits = [n for n in ast.walk(tree) if isinstance(n, ast.Constant) and isinstance(n.value, str) and id(n) not in docs]
    for n in lits:
        v = n.value
        need(not (v.startswith("s3://") and v != "s3://"), "a typed s3 uri: %r" % v[:30])
        need(not any(b and b in v for b in naming_buckets), "a typed bucket name: %r" % v[:40])
        need(not re.search(r"irpt/[a-z0-9]+/(gold|platinum)", v), "a typed key prefix: %r" % v[:40])
    # the one firm literal is the argument of lookup(...)
    firm_lits = [n for n in lits if "cottonwood" in n.value.lower()]
    for n in firm_lits:
        parent_ok = any(isinstance(p, ast.Call) and isinstance(p.func, ast.Attribute) and p.func.attr == "lookup" and n in p.args for p in ast.walk(tree))
        need(parent_ok, "the firm token appears outside a lookup() call: %r" % n.value[:40])
    need(re.search(r"\.get\(\s*[\"']upload[\"']\s*\)\s+is\s+True", src) or re.search(r"[\"']upload[\"']\s*\)\s+is\s+True", src), "the upload switch must be tested with `is True`")
    for call in [n for n in ast.walk(tree) if isinstance(n, ast.Call) and isinstance(n.func, ast.Name) and n.func.id == "print"]:
        seg = ast.get_source_segment(src, call) or ""
        for w in re.finditer(r"\b(acct|account_id|accounts|wanted|by_account)\b", seg):
            need(seg[max(0, w.start() - 4):w.start()] == "len(", "print names an account identifier: %s" % seg[:60])
    return len(mods), len(lits)


def check_facts(rec, floor_in_landing):
    exp = {"floor_day", "dry_run_default", "upload_switch", "summary_keys", "reads_only_from_floor", "tests", "words"}
    need(isinstance(rec, dict) and set(rec) == exp, "record keys differ: %s" % (sorted(set(rec) ^ exp) if isinstance(rec, dict) else "?"))
    need(rec["floor_day"] == FLOOR == floor_in_landing and rec["dry_run_default"] is True and rec["upload_switch"] == "event upload is exactly True" and rec["reads_only_from_floor"] is True, "floor, dry-run, switch or floor-read claim differ")
    need(sorted(rec["summary_keys"]) == sorted(SUMMARY_KEYS), "summary_keys differ from the handler's summary")
    t = rec["tests"]
    need(isinstance(t, int) and not isinstance(t, bool) and t >= 10, "tests must be a whole number, at least 10")
    need(nes(rec["words"]) and 80 <= len(rec["words"]) <= 1800 and not LONG_DIGITS.findall(rec["words"]), "words must be one paragraph of 80 to 1800 characters with no long digit run")
    return True


def check_grant(changed):
    bad = [f for f in changed if f not in GRANT_FILES and not f.startswith(GRANT_PREFIXES)]
    need(not bad, "the worker's commits touch files outside its grant: %s" % bad[:3])
    need(HANDLER_REL in changed and TEST_REL in changed, "the handler and its test file must both change")
    return True


def landing_floor(root):
    src = (Path(root) / "infra/aws/lambda/investor-reporting/account-return-daily/handler.py").read_bytes().decode("utf-8")
    m = re.search(r'(?m)^FLOOR_DAY\s*=\s*"(\d{4}-\d{2}-\d{2})"', src)
    need(m, "the landing handler's FLOOR_DAY is not readable")
    return m.group(1)


def run_pytest(root, target):
    r = subprocess.run([sys.executable, "-m", "pytest", "-q", "-p", "no:cacheprovider", target], cwd=str(root), capture_output=True, text=True, timeout=900)
    m = re.search(r"(\d+) passed", r.stdout)
    need(r.returncode == 0 and m is not None, "tests failed: %s" % r.stdout[-300:].replace("\n", " | "))
    return int(m.group(1))


def buckets_of(root):
    naming = load_module(Path(root) / "lib" / "opal_naming.py", "opal_naming")
    firm = naming.lookup("cottonwood")["key"]
    probe = str(naming.address("irpt", firm, "gold", "account_return_daily", "date=2026-07-10", "data.parquet"))
    return {probe[len("s3://"):].partition("/")[0]}


def run(root, cid):
    root = Path(root)
    need((root / HANDLER_REL).is_file(), "no %s" % HANDLER_REL)
    if cid == "DB147-2-AC1":
        check_behaviour(root)
        print("OK: a fake S3 holding synthetic Cottonwood gold: the two pre-floor partitions are never read; no event but upload=True writes; an upload writes exactly the series and manifest of the two accounts that build, at the builder's address; income stays null; the unreported day is listed; the account filter, the contract guard and the summary hold")
        return True
    if cid == "DB147-2-AC2":
        n_imp, n_lit = check_discipline((root / HANDLER_REL).read_bytes().decode("utf-8"), buckets_of(root))
        print("OK: %d imports, all stdlib, boto3, pyarrow, the publisher, the naming builder or the calendar; %d string literals, none a bucket, an s3 uri or a key prefix; the firm token only inside lookup(); upload tested with `is True`; no print names an account" % (n_imp, n_lit))
        return True
    if cid == "DB147-2-AC3":
        need((root / TEST_REL).is_file(), "no %s" % TEST_REL)
        n = run_pytest(root, TEST_REL)
        need(n >= 10, "the test file holds %d passing tests, at least 10 are owed" % n)
        changed = set()
        for cm in own_commits(root):
            changed |= set(git(root, "show", "--name-only", "--format=", cm).decode().split())
        check_grant(changed)
        rec = json.loads((root / REC_REL).read_bytes().decode("utf-8"))
        check_facts(rec, landing_floor(root))
        need(rec["tests"] == n, "the record's test count differs from the recount %d" % n)
        print("OK: %d tests pass; %d files changed, all in the grant; the facts record equals the handler and the landing function's floor" % (n, len(changed)))
        return True
    raise Fail("unknown criterion %s" % cid)


def selftest():
    def red(fn, label):
        try:
            fn()
        except Fail:
            return
        raise AssertionError("red arm passed: " + label)
    good = 'import json\nimport boto3\nimport publisher\nimport opal_naming\nFIRM = opal_naming.lookup("cottonwood")["key"]\n\n\ndef h(event, acct):\n    up = event.get("upload") is True\n    print(len(acct))\n    return up\n'
    assert check_discipline(good, {"opal-data-x"}) == (4, 3)
    arms = (("import", good + "import requests\n"), ("bucket", good + 'B = "opal-data-x"\n'), ("uri", good + 'U = "s3://b/k"\n'), ("prefix", good + 'P = "irpt/abc/gold/t"\n'),
            ("firm outside lookup", good + 'F = "cottonwood"\n'), ("switch", good.replace(" is True", " == True")), ("print", good.replace("len(acct)", "acct")), ("print wanted", good + "def g(wanted):\n    print(wanted)\n"))
    for label, src in arms:
        red(lambda: check_discipline(src, {"opal-data-x"}), label)
    assert check_grant({HANDLER_REL, TEST_REL, D + AUTHOR + "/x.json", sorted(PRIOR_CELL_FILES)[0]})
    red(lambda: check_grant({HANDLER_REL, TEST_REL, "lib/x.py"}), "outside grant")
    red(lambda: check_grant({HANDLER_REL}), "no test")
    rec = {"floor_day": FLOOR, "dry_run_default": True, "upload_switch": "event upload is exactly True", "summary_keys": sorted(SUMMARY_KEYS), "reads_only_from_floor": True, "tests": 10, "words": "w" * 100}
    assert check_facts(rec, FLOOR)
    farms = (("floor", lambda r: r.update(floor_day="2026-07-09")), ("dry", lambda r: r.update(dry_run_default=False)), ("switch", lambda r: r.update(upload_switch="x")), ("keys", lambda r: r.update(summary_keys=["ok"])),
             ("tests", lambda r: r.update(tests=3)), ("extra", lambda r: r.update(z=1)), ("words", lambda r: r.update(words="short")), ("digits", lambda r: r.update(words="w" * 100 + " 123456789")))
    for label, fn in farms:
        r2 = copy.deepcopy(rec)
        fn(r2)
        red(lambda: check_facts(r2, FLOOR), label)
    red(lambda: check_facts(rec, "2026-07-11"), "landing floor differs")
    print("selftest: discipline (%d red arms), grant (3) and facts (%d red arms) clauses behave" % (len(arms), len(farms) + 1))
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
