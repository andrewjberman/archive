"""IRPT_DASHBD round 125, workstream B-49F (issuer 2.0.0_SA_COO~D2) -- DB-b-254, the NO-OVERWRITE GUARD and the START FLOOR of the Cottonwood landing code (CTO analysis @4285776c5c
ruling 1 (a) and (b)): the Cottonwood gold prefix `account_return_daily` holds 3,325 Commonwealth-era partitions (2013-04-03 to 2026-06-22); the merged `write_day` refuses nothing that
exists and the merged `owed_days` would owe five held gap days at every fire (row IRPT_DASHBD-D2-S79, ARMED). LOCAL build with fake clients; nothing is landed or deployed.

  DB-b-254 (~207) adapters/cottonwood_bd_account_return_daily.py: write_day LISTs the exact day partition under the granted prefix first and raises GoldWriteError, with NO put,
                  if either key exists;  account-return-daily/handler.py: FLOOR_DAY = "2026-07-10", owed_days never owes a day before it, and an event naming any day before it raises
                  before any write.                                                          DB125-1-AC1 (the adapter guard, probed), DB125-1-AC2 (the handler floor, probed from the
                                                                                             STAGED closure), DB125-1-AC3 (the facts, the tests, the change is additive)

Round 121's clause that write_day "calls NO other client method" is superseded by the guard's ONE list call (list_objects_v2 under the granted prefix, the one the role already holds).

Usage: python <this file> <repo_root> <criterion_id>      prints "<id> PASS" or "<id> FAIL" last
       python <this file> --selftest [<repo_root>]          the record and probe clauses on synthetic arms
"""
import hashlib
import json
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

D = "org/missions/D9/IRPT/IRPT_DASHBD/deliverables/"
REC_REL = D + "0.9.0_WK_IRPT_DASHBD~207/RD_GUARD_FLOOR_FACTS_R125.json"
ORDER_REL = "org/missions/D9/IRPT/IRPT_DASHBD/task-orders/IRPT_DASHBD.TO-DB-b-254.cottonwood-write-guard-and-start-floor.md"
AUTHOR = "0.9.0_WK_IRPT_DASHBD~207"
ADAPTER_REL = "data/assets/scripts/gold/irpt_reporting/adapters/cottonwood_bd_account_return_daily.py"
ADAPTER_TEST_REL = "data/assets/scripts/gold/irpt_reporting/tests/test_cottonwood_bd_account_return_daily.py"
FN_DIR = "infra/aws/lambda/investor-reporting/account-return-daily/"
HANDLER_REL = FN_DIR + "handler.py"
HANDLER_TEST_REL = FN_DIR + "tests/test_handler.py"
SOURCE_MAP_REL = "infra/aws/lambda/ci/lambda-source-map.json"
ENTRY_KEY = "irpt-cot-account-return-daily-lambda"
FLOOR = "2026-07-10"
BASE_ADAPTER_TESTS = 32
BASE_HANDLER_TESTS = 11
MIN_NEW = 4
CLAIMS = ("measured", "inferred", "held", "absent")
LONG_DIGITS = re.compile(r"\d{8,}")
DIGIT_OK_KEYS = ("sha256", "path", "file", "key", "where", "vintage")
HEX64 = re.compile(r"[0-9a-f]{64}$")


class Fail(Exception):
    pass


def need(cond, msg):
    if not cond:
        raise Fail(msg)


def nes(x):
    return isinstance(x, str) and x.strip() != ""


def is_int(x):
    return isinstance(x, int) and not isinstance(x, bool)


def digit_runs(x, key=""):
    if isinstance(x, dict):
        return [h for k, v in x.items() for h in digit_runs(v, str(k))]
    if isinstance(x, list):
        return [h for v in x for h in digit_runs(v, key)]
    if isinstance(x, str) and key not in DIGIT_OK_KEYS:
        return LONG_DIGITS.findall(x)
    return []


def load(root, rel):
    p = Path(root) / rel
    need(p.is_file(), "no %s" % rel)
    return json.loads(p.read_bytes().decode("utf-8"))


def git(root, *a):
    return subprocess.run(["git", "-C", str(root)] + list(a), capture_output=True, text=True).stdout


def own_commits(root):
    base = git(root, "log", "--diff-filter=A", "--format=%H", "--", ORDER_REL).split()
    need(base, "the order's first commit is not in this history")
    out = git(root, "log", "--reverse", "--format=%H", "--author=" + AUTHOR, base[-1] + "..HEAD").split()
    need(out, "no commit by %s since the order was issued" % AUTHOR)
    return out


def own_numstat(root, commits, rel):
    add = dele = 0
    for c in commits:
        for ln in git(root, "show", "--numstat", "--format=", c, "--", rel).strip().splitlines():
            p = ln.split("\t")
            if len(p) >= 2 and p[0].isdigit() and p[1].isdigit():
                add += int(p[0])
                dele += int(p[1])
    return add, dele


def own_files(root, commits):
    names = set()
    for c in commits:
        names |= set(git(root, "show", "--name-only", "--format=", c).split())
    return names


# ------------------------------------------------------------------------------------------------ the adapter probe (child interpreter)
ADAPTER_PROBE = r'''
import io, json, sys
from pathlib import Path
root = Path(sys.argv[1])
sys.path.insert(0, str(root / "data/assets/scripts/gold/irpt_reporting/adapters"))
import pyarrow as pa
import cottonwood_bd_account_return_daily as ad
out = {}
row = {"firm": ad.FIRM, "account_id": "A0000000001", "business_date": "2026-07-14", "market_value_eod": 10.0, "external_flow": 0.0, "income_received": None,
       "income_return": None, "total_return_daily": 0.01, "return_basis": "VENDOR_VALUE", "holdings_price_return": None, "holdings_price_return_reason": None,
       "fee_amount": None, "fee_amount_reason": "x", "day_quality": "MEASURED", "guard_state": "NOT_GRADED", "history_scope": "FULL", "carried_days": 0,
       "method_version": 2, "schema_version": "1.0"}
t20 = ad.to_table([row], with_source=True)
bucket, prefix = ad.gold_prefix()


class FakeS3(object):
    def __init__(self, existing=()):
        self.existing = set(existing)
        self.puts = []
        self.lists = []

    def put_object(self, Bucket, Key, Body, **kw):
        self.puts.append(Key)
        self.existing.add(Key)
        return {}

    def list_objects_v2(self, **kw):
        self.lists.append(kw)
        pre = kw.get("Prefix", "")
        keys = sorted(k for k in self.existing if k.startswith(pre))
        return {"KeyCount": len(keys), "Contents": [{"Key": k} for k in keys], "IsTruncated": False}


def attempt(existing, day="2026-07-14"):
    man = ad.build_manifest(day, t20, "2026-07-10")
    s = FakeS3(existing)
    try:
        ad.write_day(s, day, t20, man)
        return {"raised": False, "puts": len(s.puts), "lists": s.lists}
    except ad.GoldWriteError:
        return {"raised": True, "puts": len(s.puts), "lists": s.lists}


base = prefix + "date=2026-07-14/"
clean = attempt(())
out["clean"] = {"raised": clean["raised"], "puts": clean["puts"], "list_calls": len(clean["lists"]), "list_prefixes": sorted({x.get("Prefix") for x in clean["lists"]}),
                "list_bucket_ok": all(x.get("Bucket") == bucket for x in clean["lists"])}
out["base"] = base
out["data_exists"] = {k: v for k, v in attempt([base + "data.parquet"]).items() if k != "lists"}
out["manifest_exists"] = {k: v for k, v in attempt([base + "manifest.json"]).items() if k != "lists"}
out["other_day_exists"] = {k: v for k, v in attempt([prefix + "date=2026-07-13/data.parquet"]).items() if k != "lists"}
out["history_day"] = {k: v for k, v in attempt([prefix + "date=2026-06-22/data.parquet"], "2026-06-22").items() if k != "lists"}


class Reader(object):
    reads = 0

    def list_partitions(self, table):
        return ["2026-07-13", "2026-07-14"]

    def read_parquet(self, table, day):
        if table == "fact_allocations":
            return pa.table({"AccountID": ["A0000000001"], "Account Market Value": [100.0 if day == "2026-07-13" else 101.0]})
        return pa.table({"AccountID": pa.array([], pa.string()), "Trade Date": pa.array([], pa.string()), "External Flow": pa.array([], pa.string()),
                         "Transaction Type": pa.array([], pa.string()), "Market Value": pa.array([], pa.float64())})


s = FakeS3([base + "data.parquet"])
try:
    ad.run_day(Reader(), s, "2026-07-14")
    out["run_day_existing"] = {"raised": False, "puts": len(s.puts)}
except ad.GoldWriteError:
    out["run_day_existing"] = {"raised": True, "puts": len(s.puts)}
s = FakeS3(())
r = ad.run_day(Reader(), s, "2026-07-14")
out["run_day_clean"] = {"held": r.get("held"), "puts": len(s.puts)}
s = FakeS3([base + "data.parquet"])
r = ad.run_day(Reader(), s, "2026-07-14", upload=False)
out["run_day_dry"] = {"puts": len(s.puts)}
print("PROBE " + json.dumps(out))
'''


def run_probe(script, root, entry=None):
    with tempfile.TemporaryDirectory() as td:
        pp = Path(td) / "probe.py"
        pp.write_text(script, encoding="utf-8")
        arg, cwd = str(root), None
        if entry is not None:
            stage = Path(td) / "stage"
            stage.mkdir()
            stage_closure(root, entry, stage)
            arg, cwd = str(stage), str(stage)
        r = subprocess.run([sys.executable, "-I", str(pp), arg], capture_output=True, text=True, timeout=250, cwd=cwd)
    line = [ln for ln in r.stdout.splitlines() if ln.startswith("PROBE ")]
    need(line, "the probe printed no result (rc %s): %s" % (r.returncode, (r.stderr.strip().splitlines() or ["no stderr"])[-1][:300]))
    return json.loads(line[0][len("PROBE "):])


def check_adapter_probe(o):
    c = o["clean"]
    need(c["raised"] is False and c["puts"] == 2, "a clean day must write exactly two objects: %s" % c)
    need(c["list_calls"] >= 1, "write_day must LIST before writing")
    need(c["list_prefixes"] == [o["base"]] and c["list_bucket_ok"], "the guard must list exactly the day partition %s in the gold bucket, found %s" % (o["base"], c["list_prefixes"]))
    for k in ("data_exists", "manifest_exists", "history_day"):
        need(o[k] == {"raised": True, "puts": 0}, "%s: write_day must raise GoldWriteError with no put, got %s" % (k, o[k]))
    need(o["other_day_exists"] == {"raised": False, "puts": 2}, "a key of another day must not block: %s" % o["other_day_exists"])
    need(o["run_day_existing"] == {"raised": True, "puts": 0}, "run_day over an existing partition must raise with no put: %s" % o["run_day_existing"])
    need(o["run_day_clean"] == {"held": False, "puts": 2} and o["run_day_dry"] == {"puts": 0}, "run_day clean and dry-run behaviour: %s %s" % (o["run_day_clean"], o["run_day_dry"]))
    return True


# ------------------------------------------------------------------------------------------------ the handler probe (staged closure)
HANDLER_PROBE = r'''
import datetime as dt, json, sys
from pathlib import Path
stage = sys.argv[1]
sys.path.insert(0, stage)
import pyarrow as pa
import handler
out = {"floor": getattr(handler, "FLOOR_DAY", None), "in_stage": str(Path(handler.__file__).resolve()).startswith(str(Path(stage).resolve()))}
out["owed_gap"] = handler.owed_days("2026-06-22", dt.date(2026, 7, 15))
out["owed_at_floor"] = handler.owed_days("2026-07-10", dt.date(2026, 7, 15))
out["owed_none"] = handler.owed_days(None, dt.date(2026, 7, 15))
out["owed_none_before"] = handler.owed_days(None, dt.date(2026, 7, 8))
out["owed_gap_before"] = handler.owed_days("2026-06-22", dt.date(2026, 7, 9))
out["owed_cap"] = len(handler.owed_days("2026-06-22", dt.date(2026, 9, 15)))
out["cap_const"] = handler.MAX_DAYS_PER_FIRE


class FakeS3(object):
    def __init__(self, existing=()):
        self.existing = set(existing)
        self.puts = []

    def put_object(self, Bucket, Key, Body, **kw):
        self.puts.append(Key)
        self.existing.add(Key)
        return {}

    def list_objects_v2(self, **kw):
        pre = kw.get("Prefix", "")
        if kw.get("Delimiter"):
            days = sorted({k[len(pre):].split("/")[0] for k in self.existing if k.startswith(pre)})
            return {"CommonPrefixes": [{"Prefix": pre + d + "/"} for d in days], "IsTruncated": False}
        keys = sorted(k for k in self.existing if k.startswith(pre))
        return {"KeyCount": len(keys), "Contents": [{"Key": k} for k in keys], "IsTruncated": False}


def alloc(vals):
    return pa.table({"AccountID": [a for a, _v in vals], "Account Market Value": [v for _a, v in vals]})


def trans():
    return pa.table({"AccountID": pa.array([], pa.string()), "Trade Date": pa.array([], pa.string()), "External Flow": pa.array([], pa.string()),
                     "Transaction Type": pa.array([], pa.string()), "Market Value": pa.array([], pa.float64())})


class Reader(object):
    def __init__(self):
        self.reads = 0
        self.days = ["2026-06-29", "2026-06-30", "2026-07-09", "2026-07-10", "2026-07-13", "2026-07-14"]

    def list_partitions(self, table):
        return list(self.days)

    def read_parquet(self, table, day):
        if table == "fact_allocations":
            return alloc([("A0000000001", 100.0), ("A0000000002", 200.0)])
        return trans()


def go(event, existing=()):
    s = FakeS3(existing)
    try:
        r = handler.lambda_handler(event, None, s3=s, reader=Reader())
        return {"raised": False, "puts": len(s.puts), "days": r.get("days")}
    except BaseException:
        return {"raised": True, "puts": len(s.puts), "days": None}


import cottonwood_bd_account_return_daily as cbd
bucket, prefix = cbd.gold_prefix()
out["ok_day"] = go({"day": "2026-07-14"})
out["history_day"] = go({"day": "2026-06-22"}, [prefix + "date=2026-06-22/data.parquet"])
out["gap_day"] = go({"day": "2026-07-09"})
out["below_floor"] = go({"day": "2026-06-30"})
out["mixed_days"] = go({"days": ["2026-07-10", "2026-06-30"]})
out["floor_day"] = go({"day": "2026-07-10"})
out["existing_day"] = go({"day": "2026-07-14"}, [prefix + "date=2026-07-14/data.parquet"])
out["dry_below"] = go({"day": "2026-06-30", "dry_run": True})
print("PROBE " + json.dumps(out))
'''


def stage_closure(root, entry, dest):
    root, dest = Path(root), Path(dest)
    shutil.copy2(root / entry["source_dir"] / "handler.py", dest / "handler.py")
    for m in entry["staged_from"]:
        tgt = dest / m["packaged_as"]
        tgt.parent.mkdir(parents=True, exist_ok=True)
        need((root / m["repo_path"]).is_file(), "staged member missing in the repo: %s" % m["repo_path"])
        shutil.copy2(root / m["repo_path"], tgt)


def check_handler_probe(o):
    need(o["in_stage"], "the handler was not imported from the staged directory")
    need(o["floor"] == FLOOR, "FLOOR_DAY must be %s, found %s" % (FLOOR, o["floor"]))
    need(o["owed_gap"] == ["2026-07-10", "2026-07-13", "2026-07-14"], "owed_days after 2026-06-22 on 2026-07-15 must start at the floor: %s" % o["owed_gap"])
    need(o["owed_at_floor"] == ["2026-07-13", "2026-07-14"], "owed_days after 2026-07-10: %s" % o["owed_at_floor"])
    need(o["owed_none"] == ["2026-07-14"] and o["owed_none_before"] == [] and o["owed_gap_before"] == [], "owed_days with nothing landed, or with T-1 before the floor: %s %s %s" %
         (o["owed_none"], o["owed_none_before"], o["owed_gap_before"]))
    need(is_int(o["cap_const"]) and o["owed_cap"] == o["cap_const"], "owed_days must still cap at MAX_DAYS_PER_FIRE")
    need(o["ok_day"] == {"raised": False, "puts": 2, "days": ["2026-07-14"]}, "a day on or after the floor must write two objects: %s" % o["ok_day"])
    need(o["floor_day"] == {"raised": False, "puts": 2, "days": ["2026-07-10"]}, "the floor day itself must be allowed: %s" % o["floor_day"])
    for k in ("history_day", "gap_day", "below_floor", "mixed_days", "dry_below"):
        need(o[k]["raised"] is True and o[k]["puts"] == 0, "%s: an event naming a day before the floor must raise before any write: %s" % (k, o[k]))
    need(o["existing_day"]["raised"] is True and o["existing_day"]["puts"] == 0, "an existing partition must raise with no put: %s" % o["existing_day"])
    return True


# ------------------------------------------------------------------------------------------------ the facts (pure)
def check_facts(rec, sha_of, file_exists):
    exp = {"adapter", "handler", "tests", "superseded_clause", "files_changed", "disarm", "words", "claim", "files_in_repo", "served_values_changed", "pushed", "deployed"}
    need(isinstance(rec, dict) and set(rec) == exp, "record keys differ: %s" % (sorted(set(rec) ^ exp) if isinstance(rec, dict) else "?"))
    need(nes(rec["words"]) and rec["claim"] in CLAIMS, "words or claim")
    a = rec["adapter"]
    need(isinstance(a, dict) and set(a) == {"file", "function", "list_calls_per_write", "list_prefix_form", "words"} and a["file"] == ADAPTER_REL and a["function"] == "write_day"
         and a["list_calls_per_write"] == 1 and nes(a["list_prefix_form"]) and nes(a["words"]), "adapter block")
    h = rec["handler"]
    need(isinstance(h, dict) and set(h) == {"file", "floor_day", "floor_applies_to", "words"} and h["file"] == HANDLER_REL and h["floor_day"] == FLOOR and isinstance(h["floor_applies_to"], list)
         and {"owed_days", "day_event", "days_event"} <= set(h["floor_applies_to"]) and nes(h["words"]), "handler block (floor_applies_to must list owed_days, day_event, days_event)")
    t = rec["tests"]
    need(isinstance(t, dict) and set(t) == {"adapter_file", "adapter_new_tests", "adapter_total", "handler_file", "handler_new_tests", "handler_total"} and t["adapter_file"] == ADAPTER_TEST_REL
         and t["handler_file"] == HANDLER_TEST_REL and is_int(t["adapter_new_tests"]) and t["adapter_new_tests"] >= MIN_NEW and is_int(t["handler_new_tests"]) and t["handler_new_tests"] >= MIN_NEW
         and is_int(t["adapter_total"]) and t["adapter_total"] >= BASE_ADAPTER_TESTS + MIN_NEW and is_int(t["handler_total"]) and t["handler_total"] >= BASE_HANDLER_TESTS + MIN_NEW, "tests block")
    need(nes(rec["superseded_clause"]) and "DB121-4-AC2" in rec["superseded_clause"], "superseded_clause must name DB121-4-AC2")
    fc = rec["files_changed"]
    need(isinstance(fc, list) and {f.get("file") for f in fc} >= {ADAPTER_REL, ADAPTER_TEST_REL, HANDLER_REL, HANDLER_TEST_REL}, "files_changed must name the adapter, the handler and both test files")
    for f in fc:
        need(set(f) == {"file", "sha256", "kind"} and nes(f["kind"]) and file_exists(f["file"]) and HEX64.match(str(f["sha256"])) and sha_of(f["file"]) == f["sha256"], "files_changed entry %s: hash or form" % f.get("file"))
        need(f["file"] in (ADAPTER_REL, ADAPTER_TEST_REL, HANDLER_REL, HANDLER_TEST_REL), "a changed file outside the grant: %s" % f["file"])
    d = rec["disarm"]
    need(isinstance(d, dict) and set(d) == {"row", "words"} and d["row"] == "IRPT_DASHBD-D2-S79" and nes(d["words"]), "disarm block (names row IRPT_DASHBD-D2-S79)")
    need(rec["files_in_repo"] is False and rec["served_values_changed"] is False and rec["pushed"] is False and rec["deployed"] is False, "a flag is not false")
    need(not digit_runs(rec), "a run of 8 or more digits outside the exempt fields: %s" % digit_runs(rec)[:2])
    return True


def count_tests(path):
    return len(re.findall(r"^\s*def (test_\w+)", Path(path).read_text(encoding="utf-8"), re.M))


def run(root, cid):
    root = Path(root)
    if cid == "DB125-1-AC1":
        o = run_probe(ADAPTER_PROBE, root)
        check_adapter_probe(o)
        n = count_tests(root / ADAPTER_TEST_REL)
        need(n >= BASE_ADAPTER_TESTS + MIN_NEW, "the adapter test file holds %d tests (needs %d)" % (n, BASE_ADAPTER_TESTS + MIN_NEW))
        r = subprocess.run([sys.executable, "-m", "pytest", "-q", "--no-header", "-p", "no:cacheprovider", str(root / ADAPTER_TEST_REL)], cwd=str(root), capture_output=True, text=True, timeout=250)
        m = re.search(r"(\d+) passed", r.stdout)
        need(r.returncode == 0 and m and int(m.group(1)) >= BASE_ADAPTER_TESTS + MIN_NEW and "failed" not in r.stdout, "adapter pytest: rc %s, %s" % (r.returncode, (r.stdout.strip().splitlines() or ["no output"])[-1]))
        print("OK: write_day LISTs the day partition (one call, the exact prefix) and raises GoldWriteError with no put when either key exists, including a 2026-06-22 history day; "
              "another day's key does not block; run_day over an existing partition raises with no put; %s adapter tests pass" % m.group(1))
        return True
    if cid == "DB125-1-AC2":
        entry = load(root, SOURCE_MAP_REL)["functions"][ENTRY_KEY]
        o = run_probe(HANDLER_PROBE, root, entry)
        check_handler_probe(o)
        n = count_tests(root / HANDLER_TEST_REL)
        need(n >= BASE_HANDLER_TESTS + MIN_NEW, "the handler test file holds %d tests (needs %d)" % (n, BASE_HANDLER_TESTS + MIN_NEW))
        r = subprocess.run([sys.executable, "-m", "pytest", "-q", "--no-header", "-p", "no:cacheprovider", str(root / HANDLER_TEST_REL)], cwd=str(root), capture_output=True, text=True, timeout=250)
        m = re.search(r"(\d+) passed", r.stdout)
        need(r.returncode == 0 and m and int(m.group(1)) >= BASE_HANDLER_TESTS + MIN_NEW and "failed" not in r.stdout, "handler pytest: rc %s, %s" % (r.returncode, (r.stdout.strip().splitlines() or ["no output"])[-1]))
        print("OK: staged probe: FLOOR_DAY %s; owed_days after 2026-06-22 starts at the floor and skips the gap, owes nothing while T-1 is before it; an event naming a day before the floor "
              "(including 2026-06-22) raises before any write; the floor day and later days write; an existing partition raises with no put; %s handler tests pass" % (FLOOR, m.group(1)))
        return True
    if cid == "DB125-1-AC3":
        rec = load(root, REC_REL)
        check_facts(rec, lambda rel: hashlib.sha256((root / rel).read_bytes()).hexdigest(), lambda rel: (root / rel).is_file())
        cs = own_commits(root)
        a_add, a_del = own_numstat(root, cs, ADAPTER_REL)
        h_add, h_del = own_numstat(root, cs, HANDLER_REL)
        need(a_add >= 8 and a_del <= 8, "the adapter change must be additive: +%d/-%d (needs gain >= 8, lose <= 8)" % (a_add, a_del))
        need(h_add >= 10 and h_del <= 12, "the handler change must be additive: +%d/-%d (needs gain >= 10, lose <= 12)" % (h_add, h_del))
        stray = sorted(f for f in own_files(root, cs) if f.startswith(("infra/", "data/", "lib/", "org/standards/")) and f not in (ADAPTER_REL, ADAPTER_TEST_REL, HANDLER_REL, HANDLER_TEST_REL))
        need(not stray, "this worker's commits changed files outside the grant: %s" % stray[:3])
        print("OK: facts valid, files hashed; adapter +%d/-%d, handler +%d/-%d in the worker's own commits; the source map and every other file untouched" % (a_add, a_del, h_add, h_del))
        return True
    raise Fail("unknown criterion %s" % cid)


def selftest():
    import copy
    base = "gold/prefix/date=2026-07-14/"
    ok = {"clean": {"raised": False, "puts": 2, "list_calls": 1, "list_prefixes": [base], "list_bucket_ok": True}, "base": base, "data_exists": {"raised": True, "puts": 0},
          "manifest_exists": {"raised": True, "puts": 0}, "other_day_exists": {"raised": False, "puts": 2}, "history_day": {"raised": True, "puts": 0},
          "run_day_existing": {"raised": True, "puts": 0}, "run_day_clean": {"held": False, "puts": 2}, "run_day_dry": {"puts": 0}}
    assert check_adapter_probe(copy.deepcopy(ok))
    for key, val in (("clean", {"raised": False, "puts": 2, "list_calls": 0, "list_prefixes": [], "list_bucket_ok": True}), ("data_exists", {"raised": False, "puts": 2}),
                     ("manifest_exists", {"raised": True, "puts": 1}), ("other_day_exists", {"raised": True, "puts": 0}), ("history_day", {"raised": False, "puts": 2}),
                     ("run_day_existing", {"raised": True, "puts": 2}), ("run_day_dry", {"puts": 1}),
                     ("clean", {"raised": False, "puts": 2, "list_calls": 1, "list_prefixes": ["other/"], "list_bucket_ok": True})):
        o = copy.deepcopy(ok)
        o[key] = val
        try:
            check_adapter_probe(o)
            raise AssertionError("red adapter arm %s passed" % key)
        except Fail:
            pass
    hok = {"floor": FLOOR, "in_stage": True, "owed_gap": ["2026-07-10", "2026-07-13", "2026-07-14"], "owed_at_floor": ["2026-07-13", "2026-07-14"], "owed_none": ["2026-07-14"],
           "owed_none_before": [], "owed_gap_before": [], "owed_cap": 5, "cap_const": 5, "ok_day": {"raised": False, "puts": 2, "days": ["2026-07-14"]},
           "floor_day": {"raised": False, "puts": 2, "days": ["2026-07-10"]}, "history_day": {"raised": True, "puts": 0, "days": None}, "gap_day": {"raised": True, "puts": 0, "days": None},
           "below_floor": {"raised": True, "puts": 0, "days": None}, "mixed_days": {"raised": True, "puts": 0, "days": None}, "dry_below": {"raised": True, "puts": 0, "days": None},
           "existing_day": {"raised": True, "puts": 0, "days": None}}
    assert check_handler_probe(copy.deepcopy(hok))
    for key, val in (("floor", "2026-06-23"), ("owed_gap", ["2026-06-23", "2026-06-24"]), ("owed_none_before", ["2026-07-07"]), ("floor_day", {"raised": True, "puts": 0, "days": None}),
                     ("mixed_days", {"raised": True, "puts": 2, "days": None}), ("history_day", {"raised": False, "puts": 2, "days": ["2026-06-22"]}),
                     ("existing_day", {"raised": False, "puts": 2, "days": ["2026-07-14"]}), ("in_stage", False), ("owed_cap", 9)):
        o = copy.deepcopy(hok)
        o[key] = val
        try:
            check_handler_probe(o)
            raise AssertionError("red handler arm %s passed" % key)
        except Fail:
            pass
    fc = [{"file": f, "sha256": "ab" * 32, "kind": "k"} for f in (ADAPTER_REL, ADAPTER_TEST_REL, HANDLER_REL, HANDLER_TEST_REL)]
    good = {"adapter": {"file": ADAPTER_REL, "function": "write_day", "list_calls_per_write": 1, "list_prefix_form": "gold prefix + date=<day>/", "words": "w"},
            "handler": {"file": HANDLER_REL, "floor_day": FLOOR, "floor_applies_to": ["owed_days", "day_event", "days_event"], "words": "w"},
            "tests": {"adapter_file": ADAPTER_TEST_REL, "adapter_new_tests": 5, "adapter_total": 37, "handler_file": HANDLER_TEST_REL, "handler_new_tests": 5, "handler_total": 16},
            "superseded_clause": "DB121-4-AC2 'calls NO other client method' is superseded by the one list call", "files_changed": fc,
            "disarm": {"row": "IRPT_DASHBD-D2-S79", "words": "w"}, "words": "w", "claim": "measured", "files_in_repo": False, "served_values_changed": False, "pushed": False, "deployed": False}

    def grade(r, sha="ab" * 32):
        try:
            return check_facts(r, lambda rel: sha, lambda rel: True)
        except Fail:
            return False
    assert grade(copy.deepcopy(good)) is True
    for f in (lambda r: r["adapter"].update(list_calls_per_write=2), lambda r: r["handler"].update(floor_day="2026-06-23"), lambda r: r["handler"]["floor_applies_to"].pop(),
              lambda r: r["tests"].update(adapter_new_tests=1), lambda r: r.update(superseded_clause="none"), lambda r: r["disarm"].update(row="x"), lambda r: r.update(pushed=True),
              lambda r: r["files_changed"].append({"file": SOURCE_MAP_REL, "sha256": "ab" * 32, "kind": "k"}), lambda r: r.update(words="id 1234567890")):
        r = copy.deepcopy(good)
        f(r)
        assert grade(r) is False
    assert grade(copy.deepcopy(good), sha="cd" * 32) is False
    print("selftest: nine adapter arms, ten handler arms and ten facts arms behave")


if __name__ == "__main__":
    try:
        if len(sys.argv) >= 2 and sys.argv[1] == "--selftest":
            selftest()
            print("selftest PASS")
            sys.exit(0)
        run(sys.argv[1], sys.argv[2])
        print("%s PASS" % sys.argv[2])
    except Fail as e:
        print("FAIL: %s" % e)
        print("%s FAIL" % (sys.argv[2] if len(sys.argv) > 2 else "?"))
        sys.exit(1)
