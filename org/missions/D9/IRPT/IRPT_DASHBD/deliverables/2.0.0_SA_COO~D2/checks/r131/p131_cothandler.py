"""IRPT_DASHBD round 131, workstream B-49F (issuer 2.0.0_SA_COO~D2) -- DB-b-263, the COTTONWOOD REPORT-BUILD HANDLER (CTO B-CW ROUND-127 ANALYSIS @e86dc1ea32 ruling 2, msg 8348): a
Lambda handler, in its own source directory, that builds the firm's filled report (filled_report_values) for firm cottonwood ONLY, one invocation per owed day with a self-invoke chain.
It reads ONLY the Cottonwood gold tables (account_dim, account_return_daily, holdings_performance_daily/_manifest) and the one served model-series object, writes ONLY Cottonwood's
filled_report_values prefix, never opens a returns partition before the start floor 2026-07-10 (the Commonwealth-era history), and never overwrites a landed day. LOCAL: nothing is
planned, applied, uploaded or deployed; the Terraform root and the source-map entry are the next cell.

  DB-b-263 (~214)   infra/aws/lambda/investor-reporting/reporting-gold-cot/handler.py (+ tests/), a facts record
                    DB131-1-AC1 (static: imports, no other firm, one put, the floor, one Event invoke, the grant),
                    DB131-1-AC2 (the PROBE: the handler staged as it will be packaged, run against a fake S3: every key it touches, the floor, the one put, the skip, the dry run, the refusals, the chain),
                    DB131-1-AC3 (the worker's own tests pass and are not vacuous; the facts record equals the recount)

Usage: python <this file> <repo_root> <criterion_id>      prints "<id> PASS" or "<id> FAIL" last
       python <this file> --selftest                       the pure clauses on synthetic arms
"""
import ast
import json
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

D = "org/missions/D9/IRPT/IRPT_DASHBD/deliverables/"
REC_REL = D + "0.9.0_WK_IRPT_DASHBD~214/RD_COT_REPORT_HANDLER_FACTS_R131.json"
ORDER_REL = "org/missions/D9/IRPT/IRPT_DASHBD/task-orders/IRPT_DASHBD.TO-DB-b-263.cottonwood-report-build-handler-filled-stage-own-function.md"
AUTHOR = "0.9.0_WK_IRPT_DASHBD~214"
HANDLER_REL = "infra/aws/lambda/investor-reporting/reporting-gold-cot/handler.py"
TEST_DIR = "infra/aws/lambda/investor-reporting/reporting-gold-cot/tests/"
GRANT_PREFIXES = ("infra/aws/lambda/investor-reporting/reporting-gold-cot/", D + "0.9.0_WK_IRPT_DASHBD~214/", "org/missions/D9/IRPT/IRPT_DASHBD/surprise-channel/investigations/",
                  "org/missions/D9/IRPT/IRPT_DASHBD/task-orders/")
FLOOR_DAY = "2026-07-10"
# the files the handler is packaged with (paths in the repo = paths in the bundle; the handler itself is the bundle's root)
CLOSURE = ["data/assets/scripts/gold/irpt_reporting/filled_report_values.py", "data/assets/scripts/gold/irpt_reporting/adapters/cottonwood_report_reader.py",
           "data/assets/scripts/gold/irpt_reporting/adapters/model_series_windows.py", "org/standards/IRPT_DASHBD_PERFORMANCE_REPORT_CONTRACT.json", "lib/opal_naming.py", "lib/trading_calendar.py",
           "org/standards/NAMING_SCHEMA.json"] + ["infra/logic/registry/%s.json" % n for n in (
               "systems", "scopes", "tiers", "exemptions", "remediations", "resources", "reporting_policies", "legacy_addresses", "feeds", "platinum_destinations", "firm_pages")]
BUNDLE_MODULES = {"handler", "filled_report_values", "cottonwood_report_reader", "model_series_windows", "opal_naming", "trading_calendar", "opal_naming_rootcheck"}
THIRD_PARTY_OK = {"pyarrow", "boto3", "botocore"}
LONG_DIGITS = re.compile(r"\d{8,}")


class Fail(Exception):
    pass


def need(cond, msg):
    if not cond:
        raise Fail(msg)


def git(root, *a):
    r = subprocess.run(["git", "-C", str(root)] + list(a), capture_output=True)
    return r.stdout.decode("utf-8", "replace"), r.returncode


def own_commits(root):
    base, _ = git(root, "log", "--diff-filter=A", "--format=%H", "--", ORDER_REL)
    need(base.split(), "the order's first commit is not in this history")
    out, _ = git(root, "log", "--reverse", "--format=%H", "--author=" + AUTHOR, base.split()[-1] + "..HEAD")
    need(out.split(), "no commit by %s since the order was issued" % AUTHOR)
    return out.split()


# ------------------------------------------------------------------------------------------------ the static clauses (pure)
def import_time_names(body):
    out = set()
    for node in body:
        if isinstance(node, ast.Import):
            out |= {a.name.split(".")[0] for a in node.names}
        elif isinstance(node, ast.ImportFrom) and node.level == 0 and node.module:
            out.add(node.module.split(".")[0])
        elif isinstance(node, (ast.If, ast.With)):
            out |= import_time_names(node.body)
            if isinstance(node, ast.If):
                out |= import_time_names(node.orelse)
        elif isinstance(node, ast.Try):
            out |= import_time_names(node.body)
    return out


def check_static(src):
    tree = ast.parse(src)
    std = set(sys.stdlib_module_names)
    mods = import_time_names(tree.body)
    third = {m for m in mods if m not in std and m not in BUNDLE_MODULES and m != "__future__"}
    need(third <= THIRD_PARTY_OK, "import-time third-party imports beyond pyarrow, boto3 and botocore: %s" % sorted(third - THIRD_PARTY_OK))
    low = src.lower()
    for tok in ("49financial", "49f", "schwab", "inflection", "commonwealth_account"):
        need(tok not in low.replace("commonwealth-era", "").replace("commonwealth era", ""), "the handler names another firm's place: %s" % tok)
    calls = [n for n in ast.walk(tree) if isinstance(n, ast.Call)]
    names = [(n.func.attr if isinstance(n.func, ast.Attribute) else getattr(n.func, "id", "")) for n in calls]
    need(names.count("put_object") == 1, "the handler must hold exactly one put_object call, read %d" % names.count("put_object"))
    for bad in ("delete_object", "delete_objects", "copy_object", "upload_file", "upload_fileobj", "put_object_acl", "create_multipart_upload", "update_function_code", "put_bucket_policy"):
        need(bad not in names, "the handler calls %s" % bad)
    need(src.count('InvocationType="Event"') + src.count("InvocationType='Event'") == 1, "exactly one asynchronous self-invoke (InvocationType Event) is allowed")
    consts = {t.targets[0].id: t.value.value for t in tree.body if isinstance(t, ast.Assign) and len(t.targets) == 1 and isinstance(t.targets[0], ast.Name) and isinstance(t.value, ast.Constant)}
    need(consts.get("FLOOR_DAY") == FLOOR_DAY, "FLOOR_DAY must be the string %s" % FLOOR_DAY)
    need("lambda_handler" in {n.name for n in tree.body if isinstance(n, ast.FunctionDef)}, "no lambda_handler")
    return True


def check_grant(changed, extra_ok=()):
    bad = [f for f in changed if not (f.startswith(GRANT_PREFIXES) or f in extra_ok)]
    need(not bad, "the worker's commits touch files outside its grant: %s" % bad[:3])
    need(any(f == HANDLER_REL for f in changed), "the handler was not added")
    return True


def check_probe(res):
    """res: the child interpreter's JSON result. Every clause is a fact the probe measured."""
    need(res.get("import_ok") is True, "the staged handler does not import: %s" % res.get("import_error"))
    s = res["scenarios"]
    a = s["one_day"]
    need(a["result"].get("rows", 0) > 0 and "failed" not in a["result"], "the one-day event wrote nothing: %s" % a["result"])
    need(a["puts"] == [a["expected_key"]], "the one-day event must make exactly one put, at %s; read %s" % (a["expected_key"], a["puts"]))
    need(a["put_parquet_columns_ok"] is True and a["put_rows"] == a["result"]["rows"], "the put body is not the filled table's parquet with the reported rows")
    need(a["history_touched"] == [], "the handler opened history before the floor: %s" % a["history_touched"][:3])
    need(a["foreign_keys"] == [], "the handler touched keys outside the allowed set: %s" % a["foreign_keys"][:3])
    need(a["model_key_read"] is True, "the served model series was not read through the reader")
    need(a["gets_on_returns"] >= 1, "no returns partition at or after the floor was read")
    sk = s["existing"]
    need(sk["puts"] == [] and sk["result"].get("skipped") == "LANDED", "a landed day must be skipped with no put: %s" % sk)
    dr = s["dry_run"]
    need(dr["puts"] == [] and dr["result"].get("rows", 0) > 0, "a dry run must build rows and put nothing: %s" % dr)
    rf = s["before_floor"]
    need(rf["raised"] is True and rf["calls"] == 0, "a day before the floor must refuse before any call: %s" % rf)
    bad = s["bad_day"]
    need(bad["raised"] is True and bad["calls"] == 0, "a malformed day must refuse before any call: %s" % bad)
    sc = s["scheduled"]
    need(sc["first_day"] == FLOOR_DAY and sc["puts"] == [sc["expected_key"]], "the scheduled path must run the OLDEST owed day (%s) with one put: %s" % (FLOOR_DAY, sc))
    need(len(sc["invokes"]) == 1 and sc["invokes"][0]["InvocationType"] == "Event" and sc["invokes"][0]["FunctionName"] == sc["context_arn"] and sc["invokes"][0]["payload"] == {"day": sc["next_day"]},
         "the chain must be ONE Event self-invoke of the context's own ARN with {day: next}: %s" % sc["invokes"])
    last = s["last_day"]
    need(last["invokes"] == [] and len(last["puts"]) == 1, "the last owed day must put once and chain nothing: %s" % last)
    return True


def check_facts(rec, recount):
    exp = {"reads", "writes", "floor_day", "bundle_members", "events", "words"}
    need(isinstance(rec, dict) and set(rec) == exp, "record keys differ: %s" % (sorted(set(rec) ^ exp) if isinstance(rec, dict) else "?"))
    need(rec["floor_day"] == FLOOR_DAY and rec["bundle_members"] == recount["bundle_members"], "floor_day or bundle_members differ from the recount")
    need(rec["reads"] == recount["reads"] and rec["writes"] == recount["writes"], "reads or writes differ from the probe's measurement: %s %s" % (recount["reads"], recount["writes"]))
    need(rec["events"] == ["day", "dry_run", "scheduled"], "events must list day, dry_run and scheduled")
    need(isinstance(rec["words"], str) and 80 <= len(rec["words"]) <= 1800 and not LONG_DIGITS.findall(rec["words"]), "words must be one paragraph of 80 to 1800 characters with no long digit run")
    return True


# ------------------------------------------------------------------------------------------------ the probe (child interpreter)
PROBE = r'''
import datetime as dt, io, json, sys
sys.dont_write_bytecode = True
STAGE = sys.argv[1]
sys.path.insert(0, STAGE)
import pyarrow as pa, pyarrow.parquet as pq
res = {"import_ok": False, "scenarios": {}}
try:
    import handler as H
except BaseException as e:
    res["import_error"] = "%s: %s" % (type(e).__name__, str(e)[:300])
    print(json.dumps(res)); sys.exit(0)
res["import_ok"] = True
frv = H.frv if hasattr(H, "frv") else __import__("filled_report_values")
opal_naming = __import__("opal_naming")
FIRM = "cottonwood"
GOLD = opal_naming.address("irpt", FIRM, "gold", "account_return_daily", "date=2000-01-03", "data.parquet")
GB = GOLD[len("s3://"):].split("/", 1)[0]

class Err(Exception):
    def __init__(self, code): self.response = {"Error": {"Code": code}}

class Fake:
    def __init__(self):
        self.store, self.calls, self.puts = {}, [], []
    def _p(self, bucket, key, body): self.store[(bucket, key)] = body
    def get_paginator(self, name):
        fake = self
        class P:
            def paginate(self, Bucket, Prefix, Delimiter=None):
                fake.calls.append(("LIST", Bucket, Prefix))
                keys = sorted(k for (b, k) in fake.store if b == Bucket and k.startswith(Prefix))
                if Delimiter:
                    cps = sorted({Prefix + k[len(Prefix):].split(Delimiter, 1)[0] + Delimiter for k in keys if Delimiter in k[len(Prefix):]})
                    yield {"CommonPrefixes": [{"Prefix": c} for c in cps]}
                else:
                    yield {"Contents": [{"Key": k} for k in keys]}
        return P()
    def list_objects_v2(self, Bucket, Prefix, Delimiter=None, **kw):
        self.calls.append(("LIST", Bucket, Prefix))
        keys = sorted(k for (b, k) in self.store if b == Bucket and k.startswith(Prefix))
        if Delimiter:
            cps = sorted({Prefix + k[len(Prefix):].split(Delimiter, 1)[0] + Delimiter for k in keys if Delimiter in k[len(Prefix):]})
            return {"CommonPrefixes": [{"Prefix": c} for c in cps], "IsTruncated": False}
        return {"Contents": [{"Key": k} for k in keys], "IsTruncated": False}
    def get_object(self, Bucket, Key):
        self.calls.append(("GET", Bucket, Key))
        if (Bucket, Key) not in self.store: raise Err("NoSuchKey")
        return {"Body": io.BytesIO(self.store[(Bucket, Key)]), "VersionId": "v1"}
    def head_object(self, Bucket, Key):
        self.calls.append(("HEAD", Bucket, Key))
        if (Bucket, Key) not in self.store: raise Err("404")
        return {}
    def put_object(self, Bucket, Key, Body, **kw):
        self.calls.append(("PUT", Bucket, Key)); self.puts.append(Key); self.store[(Bucket, Key)] = Body
        return {}

def tbl_bytes(table):
    b = io.BytesIO(); pq.write_table(table, b); return b.getvalue()

def addr(table, day):
    u = opal_naming.address("irpt", FIRM, "gold", table, "date=%s" % day, "data.parquet")
    b, k = u[len("s3://"):].split("/", 1); return b, k

def returns(day, accts):
    n = len(accts)
    return pa.table({"account_id": accts, "business_date": [day] * n, "market_value_eod": [100.0] * n, "external_flow": [0.0] * n, "total_return_daily": [0.001] * n,
                     "day_quality": ["OK"] * n, "guard_state": ["PASS"] * n})

def build_store():
    f = Fake()
    accts = ["A1", "A2", "A3"]
    f._p(*addr("account_dim", "2026-07-13"), tbl_bytes(pa.table({"account_id": accts + ["H1"], "household_id": ["HH1", "HH1", "HH2", "HH9"]})))
    f._p(*addr("account_return_daily", "2026-06-22"), tbl_bytes(returns("2026-06-22", ["OLD1", "OLD2"])))
    f._p(*addr("account_return_daily", "2026-07-10"), tbl_bytes(returns("2026-07-10", accts)))
    f._p(*addr("account_return_daily", "2026-07-13"), tbl_bytes(returns("2026-07-13", accts)))
    f._p("opal-data-portal-v2", "json/benchmarks/model_portfolio_timeseries.json", b"{}")
    return f

def install_stubs():
    real = frv.load_model_module
    def stub_model(repo):
        m = real(repo)
        class M:
            SERVED_BUCKET, SERVED_KEY = m.SERVED_BUCKET, m.SERVED_KEY
            @staticmethod
            def read_served_series(reader):
                reader.get_object(m.SERVED_BUCKET, m.SERVED_KEY)
                return {s: [(dt.date(2026, 7, 13), 0.0)] for s in m.STEMS}, {"source": "stub"}
        return M
    frv.load_model_module = stub_model
    real_bd, real_tr = frv.build_document, frv.to_rows
    frv.build_document = lambda members, ref, as_of, accounts, src, frontiers=None: {"ref": ref, "as_of": as_of, "n": len(accounts)}
    def stub_rows(doc, ref, firm, as_of, cv):
        r = {c: "x" for c in frv.COLUMNS}; r.update(firm=firm, household_ref=ref, as_of=as_of, value_number=None); return [r, dict(r, row_key="k2")]
    frv.to_rows = stub_rows

install_stubs()
class Ctx: invoked_function_arn = "arn:aws:lambda:us-east-1:000000000000:function:probe"

def analyze(f, expected_key=None):
    prefs = [addr(tb, "2000-01-03")[1].split("date=")[0] for tb in ("account_return_daily", "account_dim", "holdings_performance_daily", "holdings_performance_manifest", "filled_report_values")]
    ret_pref = prefs[0]
    served = ("opal-data-portal-v2", "json/benchmarks/model_portfolio_timeseries.json")
    foreign, hist = [], []
    for op, b, k in f.calls:
        if (b, k) == served or (op == "LIST" and b == served[0] and served[1].startswith(k)):
            continue
        if b != GB or not any(k.startswith(p) for p in prefs):
            foreign.append("%s %s/%s" % (op, b, k)); continue
        if op == "GET" and k.startswith(ret_pref) and "date=2026-06" in k:
            hist.append(k)
    return {"foreign_keys": foreign, "history_touched": hist, "gets_on_returns": sum(1 for op, b, k in f.calls if op == "GET" and k.startswith(ret_pref)),
            "model_key_read": any(op == "GET" and (b, k) == served for op, b, k in f.calls)}

S = res["scenarios"]
# one-day event, upload
f = build_store(); out = H.lambda_handler({"day": "2026-07-13"}, None, s3=f)
r = out["result"] if isinstance(out, dict) and "result" in out else out
ek = addr("filled_report_values", "2026-07-13")[1]
a = analyze(f); a.update(result=r, puts=list(f.puts), expected_key=ek)
if f.puts:
    t = pq.read_table(io.BytesIO(f.store[(GB, f.puts[0])])); a["put_rows"] = t.num_rows; a["put_parquet_columns_ok"] = t.schema.names == frv.COLUMNS
else:
    a["put_rows"], a["put_parquet_columns_ok"] = 0, False
S["one_day"] = a
# existing
f = build_store(); f._p(GB, ek, b"landed"); out = H.lambda_handler({"day": "2026-07-13"}, None, s3=f)
S["existing"] = {"result": out["result"] if "result" in out else out, "puts": list(f.puts)}
# dry run
f = build_store(); out = H.lambda_handler({"day": "2026-07-13", "dry_run": True}, None, s3=f)
S["dry_run"] = {"result": out["result"] if "result" in out else out, "puts": list(f.puts)}
# before floor / bad day
for name, ev in (("before_floor", {"day": "2026-06-22"}), ("bad_day", {"day": "2026-13-45"})):
    f = build_store(); raised = False
    try: H.lambda_handler(ev, None, s3=f)
    except (SystemExit, ValueError): raised = True
    S[name] = {"raised": raised, "calls": len(f.calls)}
# scheduled: owed = 2026-07-10 then 2026-07-13; first run + one chain
class Lam:
    def __init__(self): self.invokes = []
    def invoke(self, FunctionName, InvocationType, Payload, **kw): self.invokes.append({"FunctionName": FunctionName, "InvocationType": InvocationType, "payload": json.loads(Payload.decode("utf-8"))}); return {}
f = build_store(); lam = Lam(); out = H.lambda_handler({}, Ctx(), s3=f, lambda_client=lam)
S["scheduled"] = {"first_day": out.get("day"), "puts": list(f.puts), "expected_key": addr("filled_report_values", "2026-07-10")[1], "invokes": lam.invokes, "context_arn": Ctx.invoked_function_arn, "next_day": "2026-07-13"}
# last owed day: nothing to chain
f = build_store(); f._p(*addr("filled_report_values", "2026-07-10"), b"landed"); lam = Lam(); out = H.lambda_handler({"day": "2026-07-13"}, Ctx(), s3=f, lambda_client=lam)
S["last_day"] = {"puts": list(f.puts), "invokes": lam.invokes}
print(json.dumps(res))
'''


def stage(root, dest):
    dest = Path(dest)
    for rel in CLOSURE:
        src = Path(root) / rel
        need(src.is_file(), "closure member missing: %s" % rel)
        (dest / rel).parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(src, dest / rel)
    shutil.copyfile(Path(root) / HANDLER_REL, dest / "handler.py")


def run_probe(root):
    with tempfile.TemporaryDirectory() as td, tempfile.TemporaryDirectory() as cwd:
        stage(root, td)
        r = subprocess.run([sys.executable, "-I", "-c", PROBE, td], cwd=cwd, capture_output=True, text=True, timeout=300)
        need(r.returncode == 0, "the probe died (rc %s): %s" % (r.returncode, (r.stderr or r.stdout)[-400:].replace("\n", " | ")))
        line = [ln for ln in r.stdout.splitlines() if ln.startswith("{")]
        need(line, "the probe printed no result: %s" % (r.stderr or r.stdout)[-300:])
        return json.loads(line[-1])


def run_tests(root):
    td = Path(root) / TEST_DIR
    need(td.is_dir() and list(td.glob("test_*.py")), "no tests under %s" % TEST_DIR)
    r = subprocess.run([sys.executable, "-m", "pytest", "-q", "-x", str(td), "-p", "no:cacheprovider"], cwd=str(root), capture_output=True, text=True, timeout=600)
    m = re.search(r"(\d+) passed", r.stdout)
    need(r.returncode == 0 and m is not None, "the worker's tests failed: %s" % r.stdout[-300:].replace("\n", " | "))
    texts = " ".join(p.read_text(encoding="utf-8") for p in td.glob("test_*.py")).lower()
    need("cottonwood" in texts and "49financial" not in texts, "the tests must name cottonwood and no other firm")
    return int(m.group(1))


def run(root, cid):
    root = Path(root)
    src = (root / HANDLER_REL).read_text(encoding="utf-8")
    if cid == "DB131-1-AC1":
        check_static(src)
        cs = own_commits(root)
        changed = set()
        for c in cs:
            changed |= set(git(root, "show", "--name-only", "--format=", c)[0].split())
        check_grant(changed)
        print("OK: static: import-time third party only pyarrow/boto3/botocore, no other firm, one put_object and no delete or copy, one Event self-invoke, FLOOR_DAY %s; %d files changed, all in the grant" % (FLOOR_DAY, len(changed)))
        return True
    if cid == "DB131-1-AC2":
        res = run_probe(root)
        check_probe(res)
        print("OK: probe: one put at the builder address, no key before the floor opened, no foreign key, the model series through the reader, a landed day skipped, a dry run puts nothing, before-floor and malformed days refuse with zero calls, the scheduled path runs the oldest owed day and chains ONE Event self-invoke, the last day chains nothing")
        return True
    if cid == "DB131-1-AC3":
        n = run_tests(root)
        res = run_probe(root)
        check_probe(res)
        a = res["scenarios"]["one_day"]
        recount = {"reads": ["account_dim", "account_return_daily", "model_series"], "writes": ["filled_report_values"], "bundle_members": sorted(CLOSURE)}
        rec = json.loads((root / REC_REL).read_text(encoding="utf-8"))
        check_facts(rec, recount)
        print("OK: %d worker tests pass and name cottonwood only; facts record equals the recount (reads %s, writes %s, %d bundle members)" % (n, recount["reads"], recount["writes"], len(CLOSURE)))
        return a is not None
    raise Fail("unknown criterion %s" % cid)


def selftest():
    import copy

    def red(fn, label):
        try:
            fn()
        except Fail:
            return
        raise AssertionError("red arm passed: " + label)
    good_src = ('import json\nimport datetime as dt\nimport pyarrow as pa\nimport filled_report_values as frv\nFLOOR_DAY = "2026-07-10"\n'
                'def lambda_handler(event, context=None, s3=None):\n    s3.put_object(Bucket="b", Key="k", Body=b"")\n    lam.invoke(FunctionName="f", InvocationType="Event", Payload=b"")\n')
    assert check_static(good_src)
    red(lambda: check_static(good_src.replace("pyarrow as pa", "pandas as pd")), "third party")
    red(lambda: check_static(good_src + "# 49financial\n"), "other firm")
    red(lambda: check_static(good_src + "def x(s3):\n    s3.put_object(Bucket='b', Key='k', Body=b'')\n"), "two puts")
    red(lambda: check_static(good_src + "def x(s3):\n    s3.delete_object(Bucket='b', Key='k')\n"), "delete")
    red(lambda: check_static(good_src.replace('FLOOR_DAY = "2026-07-10"', 'FLOOR_DAY = "2026-06-01"')), "floor")
    red(lambda: check_static(good_src.replace('InvocationType="Event"', 'InvocationType="RequestResponse"')), "no event invoke")
    red(lambda: check_static(good_src.replace("def lambda_handler", "def other")), "no lambda_handler")
    assert check_grant({HANDLER_REL, TEST_DIR + "test_a.py", D + "0.9.0_WK_IRPT_DASHBD~214/x.json"})
    red(lambda: check_grant({HANDLER_REL, "lib/opal_naming.py"}), "outside grant")
    red(lambda: check_grant({TEST_DIR + "test_a.py"}), "no handler")
    ek = "irpt/cottonwood/gold/filled_report_values/date=2026-07-13/data.parquet"
    ok = {"import_ok": True, "scenarios": {
        "one_day": {"result": {"day": "2026-07-13", "rows": 4}, "puts": [ek], "expected_key": ek, "put_parquet_columns_ok": True, "put_rows": 4, "history_touched": [], "foreign_keys": [], "model_key_read": True, "gets_on_returns": 2},
        "existing": {"result": {"skipped": "LANDED"}, "puts": []}, "dry_run": {"result": {"rows": 4}, "puts": []},
        "before_floor": {"raised": True, "calls": 0}, "bad_day": {"raised": True, "calls": 0},
        "scheduled": {"first_day": FLOOR_DAY, "puts": ["k1"], "expected_key": "k1", "invokes": [{"FunctionName": "a", "InvocationType": "Event", "payload": {"day": "2026-07-13"}}], "context_arn": "a", "next_day": "2026-07-13"},
        "last_day": {"puts": ["k"], "invokes": []}}}
    assert check_probe(copy.deepcopy(ok))
    arms = (("import", lambda r: r.update(import_ok=False)), ("no put", lambda r: r["scenarios"]["one_day"].update(puts=[])), ("two puts", lambda r: r["scenarios"]["one_day"].update(puts=[ek, ek])),
            ("wrong key", lambda r: r["scenarios"]["one_day"].update(puts=["x"])), ("history", lambda r: r["scenarios"]["one_day"].update(history_touched=["k"])),
            ("foreign", lambda r: r["scenarios"]["one_day"].update(foreign_keys=["GET other/x"])), ("model", lambda r: r["scenarios"]["one_day"].update(model_key_read=False)),
            ("no returns read", lambda r: r["scenarios"]["one_day"].update(gets_on_returns=0)), ("columns", lambda r: r["scenarios"]["one_day"].update(put_parquet_columns_ok=False)),
            ("overwrite", lambda r: r["scenarios"]["existing"].update(puts=["k"])), ("not skipped", lambda r: r["scenarios"]["existing"].update(result={"rows": 1})),
            ("dry put", lambda r: r["scenarios"]["dry_run"].update(puts=["k"])), ("floor accepted", lambda r: r["scenarios"]["before_floor"].update(raised=False)),
            ("floor io", lambda r: r["scenarios"]["before_floor"].update(calls=2)), ("bad day io", lambda r: r["scenarios"]["bad_day"].update(calls=1)),
            ("not oldest", lambda r: r["scenarios"]["scheduled"].update(first_day="2026-07-13")), ("no chain", lambda r: r["scenarios"]["scheduled"].update(invokes=[])),
            ("sync chain", lambda r: r["scenarios"]["scheduled"]["invokes"][0].update(InvocationType="RequestResponse")),
            ("other arn", lambda r: r["scenarios"]["scheduled"]["invokes"][0].update(FunctionName="b")), ("wrong next", lambda r: r["scenarios"]["scheduled"]["invokes"][0].update(payload={"day": "2026-07-14"})),
            ("chain at end", lambda r: r["scenarios"]["last_day"].update(invokes=[{}])))
    for label, fn in arms:
        r = copy.deepcopy(ok)
        fn(r)
        red(lambda: check_probe(r), label)
    recount = {"reads": ["account_dim", "account_return_daily", "model_series"], "writes": ["filled_report_values"], "bundle_members": sorted(CLOSURE)}
    rec = {"reads": recount["reads"], "writes": recount["writes"], "floor_day": FLOOR_DAY, "bundle_members": sorted(CLOSURE), "events": ["day", "dry_run", "scheduled"], "words": "w" * 100}
    assert check_facts(rec, recount)
    for label, fn in (("floor", lambda r: r.update(floor_day="2026-01-01")), ("members", lambda r: r.update(bundle_members=["x"])), ("reads", lambda r: r.update(reads=["a"])),
                      ("writes", lambda r: r.update(writes=["x"])), ("events", lambda r: r.update(events=["day"])), ("words", lambda r: r.update(words="short")),
                      ("extra", lambda r: r.update(z=1)), ("digits", lambda r: r.update(words="w" * 100 + " 123456789"))):
        r2 = dict(rec)
        fn(r2)
        red(lambda: check_facts(r2, recount), label)
    print("selftest: static (8 red arms), grant (2), probe (%d red arms) and facts (8 red arms) clauses behave" % len(arms))
    print("selftest PASS")


if __name__ == "__main__":
    if sys.argv[1:2] == ["--selftest"]:
        selftest()
        sys.exit(0)
    try:
        run(sys.argv[1], sys.argv[2])
        print(sys.argv[2] + " PASS")
    except Exception as e:  # a failed read or probe is a FAIL, not a traceback
        print("FAIL: " + str(e))
        print(sys.argv[2] + " FAIL")
        sys.exit(1)
