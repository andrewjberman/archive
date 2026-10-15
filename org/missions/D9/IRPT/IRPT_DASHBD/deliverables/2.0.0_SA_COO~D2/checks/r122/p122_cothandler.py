"""IRPT_DASHBD round 122, workstream B-49F (issuer 2.0.0_SA_COO~D2) -- DB-b-249, the COTTONWOOD LANDING FUNCTION CODE (CTO analysis @e690365741 ruling 4): a Lambda handler that runs the
round-121 adapter's `run_day` for the Cottonwood account return, its source-map entry and the zip closure it needs, tested LOCAL with fake clients. The Terraform root (function, roles,
DISABLED schedule, builder names) and the pair are the next round; nothing is planned, applied, scheduled or deployed here.

  DB-b-249 (~203) infra/aws/lambda/investor-reporting/account-return-daily/handler.py with lambda_handler(event, context=None, s3=None, reader=None), owed_days(newest_landed, today,
                  max_days=MAX_DAYS_PER_FIRE) and newest_landed_day(s3, bucket, key_prefix); a new entry in infra/aws/lambda/ci/lambda-source-map.json; tests.
                                                                                           DB122-4-AC1 (tests and functions), AC2 (the STAGED closure probe),
                                                                                           AC3 (the facts and the change)

The staged probe (AC2) copies the handler and every `staged_from` member of the new source-map entry to a temporary directory by their `packaged_as` names, with NO repo checkout on the
path, and runs the handler in a child interpreter against fake clients: if a module, a registry file or a schema is missing from the closure, the import or the run fails there.

Usage: python <this file> <repo_root> <criterion_id>      prints "<id> PASS" or "<id> FAIL" last
       python <this file> --selftest [<repo_root>]          the record and probe clauses on synthetic arms
"""
import ast
import hashlib
import json
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

D = "org/missions/D9/IRPT/IRPT_DASHBD/deliverables/"
REC_REL = D + "0.9.0_WK_IRPT_DASHBD~203/RD_CW_HANDLER_FACTS_R122.json"
ORDER_REL = "org/missions/D9/IRPT/IRPT_DASHBD/task-orders/IRPT_DASHBD.TO-DB-b-249.cottonwood-landing-function-code-handler-source-map-closure.md"
AUTHOR = "0.9.0_WK_IRPT_DASHBD~203"
FN_DIR = "infra/aws/lambda/investor-reporting/account-return-daily/"
HANDLER_REL = FN_DIR + "handler.py"
TESTS_REL = FN_DIR + "tests/test_handler.py"
SOURCE_MAP_REL = "infra/aws/lambda/ci/lambda-source-map.json"
ENTRY_KEY = "irpt-cot-account-return-daily-lambda"
ADAPTER_REL = "data/assets/scripts/gold/irpt_reporting/adapters/cottonwood_bd_account_return_daily.py"
FUNCS = ("lambda_handler", "owed_days", "newest_landed_day")
MIN_TESTS = 8
CLAIMS = ("measured", "inferred", "held", "absent")
LONG_DIGITS = re.compile(r"\d{8,}")
DIGIT_OK_KEYS = ("sha256", "path", "file", "key", "where", "vintage", "members", "entry")
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


# ------------------------------------------------------------------------------------------------ the staged probe (child interpreter)
PROBE = r'''
import datetime as dt, io, json, sys
from pathlib import Path
stage = sys.argv[1]
sys.path.insert(0, stage)
import pyarrow as pa
import handler
out = {"in_stage": str(Path(handler.__file__).resolve()).startswith(str(Path(stage).resolve()))}
out["owed_after"] = handler.owed_days("2026-07-10", dt.date(2026, 7, 15))
out["owed_none"] = handler.owed_days(None, dt.date(2026, 7, 15))
out["owed_closed"] = handler.owed_days("2026-07-10", dt.date(2026, 7, 11))
out["owed_cap"] = len(handler.owed_days("2026-06-01", dt.date(2026, 7, 15)))
out["cap_const"] = handler.MAX_DAYS_PER_FIRE


class FakeS3(object):
    def __init__(self):
        self.puts = []

    def put_object(self, Bucket, Key, Body, **kw):
        self.puts.append(Key)
        return {}

    def list_objects_v2(self, **kw):
        return {"CommonPrefixes": [], "IsTruncated": False}


def alloc(vals):
    return pa.table({"AccountID": [a for a, _v in vals], "Account Market Value": [v for _a, v in vals]})


def trans():
    return pa.table({"AccountID": pa.array([], pa.string()), "Trade Date": pa.array([], pa.string()), "External Flow": pa.array([], pa.string()),
                     "Transaction Type": pa.array([], pa.string()), "Market Value": pa.array([], pa.float64())})


class FakeReader(object):
    def __init__(self, a, t):
        self.a, self.t = a, t
        self.reads = 0

    def list_partitions(self, table):
        return sorted((self.a if table == "fact_allocations" else self.t).keys())

    def read_parquet(self, table, day):
        return (self.a if table == "fact_allocations" else self.t)[day]


A = {"2026-07-13": alloc([("A0000000001", 100.0), ("A0000000002", 200.0)]), "2026-07-14": alloc([("A0000000001", 101.0), ("A0000000002", 198.0)]),
     "2026-07-15": alloc([("A0000000001", 102.0), ("A0000000002", 199.0)])}
T = {"2026-07-13": trans(), "2026-07-14": trans(), "2026-07-15": trans()}
full = FakeReader(A, T)
s = FakeS3()
r = handler.lambda_handler({"day": "2026-07-14"}, None, s3=s, reader=full)
out["full"] = {"ok": r.get("ok"), "puts": len(s.puts), "days": r.get("days")}
s = FakeS3()
r = handler.lambda_handler({"day": "2026-07-14", "dry_run": True}, None, s3=s, reader=full)
out["dry"] = {"ok": r.get("ok"), "puts": len(s.puts)}
s = FakeS3()
held = FakeReader(A, {"2026-07-13": trans()})
r = handler.lambda_handler({"day": "2026-07-14"}, None, s3=s, reader=held)
out["held"] = {"ok": r.get("ok"), "puts": len(s.puts), "held": r.get("held")}
s = FakeS3()
r = handler.lambda_handler({"days": ["2026-07-14", "2026-07-15"]}, None, s3=s, reader=full)
out["two"] = {"puts": len(s.puts), "days": r.get("days")}
s = FakeS3()
try:
    handler.lambda_handler({"day": "2026-13-45"}, None, s3=s, reader=full)
    out["bad"] = {"raised": False, "puts": len(s.puts)}
except BaseException:
    out["bad"] = {"raised": True, "puts": len(s.puts)}
s = FakeS3()
try:
    handler.lambda_handler({"days": ["2026-07-14"] * 30}, None, s3=s, reader=full)
    out["many"] = {"raised": False, "puts": len(s.puts)}
except BaseException:
    out["many"] = {"raised": True, "puts": len(s.puts)}
print("PROBE " + json.dumps(out))
'''


def stage_closure(root, entry, dest):
    root, dest = Path(root), Path(dest)
    src_dir = entry.get("source_dir")
    need(nes(src_dir), "the entry has no source_dir")
    shutil.copy2(root / src_dir / "handler.py", dest / "handler.py")
    members = entry.get("staged_from")
    need(isinstance(members, list) and members, "the entry has no staged_from members")
    for m in members:
        need(isinstance(m, dict) and nes(m.get("repo_path")) and nes(m.get("packaged_as")), "a staged_from member lacks repo_path or packaged_as")
        tgt = dest / m["packaged_as"]
        tgt.parent.mkdir(parents=True, exist_ok=True)
        need((root / m["repo_path"]).is_file(), "staged member missing in the repo: %s" % m["repo_path"])
        shutil.copy2(root / m["repo_path"], tgt)
    return [m["packaged_as"] for m in members]


def run_probe(root, entry):
    with tempfile.TemporaryDirectory() as td:
        stage = Path(td) / "stage"
        stage.mkdir()
        names = stage_closure(root, entry, stage)
        pp = Path(td) / "probe.py"
        pp.write_text(PROBE, encoding="utf-8")
        r = subprocess.run([sys.executable, "-I", str(pp), str(stage)], capture_output=True, text=True, timeout=250, cwd=str(stage))
    line = [ln for ln in r.stdout.splitlines() if ln.startswith("PROBE ")]
    need(line, "the staged probe printed no result (rc %s): %s" % (r.returncode, (r.stderr.strip().splitlines() or ["no stderr"])[-1][:300]))
    return json.loads(line[0][len("PROBE "):]), names


def check_probe(o):
    need(o["in_stage"], "the handler was not imported from the staged directory")
    need(o["owed_after"] == ["2026-07-13", "2026-07-14"], "owed_days after 2026-07-10 on 2026-07-15 must be the trading days through T-1: %s" % o["owed_after"])
    need(o["owed_none"] == ["2026-07-14"], "owed_days with nothing landed must be T-1 only: %s" % o["owed_none"])
    need(o["owed_closed"] == [], "owed_days must be empty when the newest landed day is T-1: %s" % o["owed_closed"])
    need(is_int(o["cap_const"]) and 1 <= o["cap_const"] <= 10 and o["owed_cap"] == o["cap_const"], "owed_days must cap at MAX_DAYS_PER_FIRE (%s), found %s" % (o["cap_const"], o["owed_cap"]))
    need(o["full"]["ok"] is True and o["full"]["puts"] == 2 and o["full"]["days"] == ["2026-07-14"], "a full day must write exactly two objects: %s" % o["full"])
    need(o["dry"]["ok"] is True and o["dry"]["puts"] == 0, "dry_run must write nothing: %s" % o["dry"])
    need(o["held"]["ok"] is True and o["held"]["puts"] == 0 and o["held"]["held"] == 1, "a held day must write nothing and report held 1: %s" % o["held"])
    need(o["two"]["puts"] == 4 and o["two"]["days"] == ["2026-07-14", "2026-07-15"], "two days must write four objects: %s" % o["two"])
    need(o["bad"]["raised"] is True and o["bad"]["puts"] == 0, "a bad day must raise and write nothing: %s" % o["bad"])
    need(o["many"]["raised"] is True and o["many"]["puts"] == 0, "more than 25 days in one event must be refused before any write: %s" % o["many"])
    return True


# ------------------------------------------------------------------------------------------------ the record clauses (pure)
def check_facts(rec, sha_of, file_exists, entry_members):
    exp = {"handler", "closure", "source_map", "tests", "scheduling", "files_changed", "words", "claim", "files_in_repo", "served_values_changed", "pushed", "deployed"}
    need(isinstance(rec, dict) and set(rec) == exp, "record keys differ: %s" % (sorted(set(rec) ^ exp) if isinstance(rec, dict) else "?"))
    need(nes(rec["words"]) and rec["claim"] in CLAIMS, "words or claim")
    h = rec["handler"]
    need(isinstance(h, dict) and set(h) == {"file", "functions", "events", "words"} and h["file"] == HANDLER_REL and set(FUNCS) <= set(h["functions"]) and isinstance(h["events"], list)
         and {"day", "days", "dry_run"} <= set(h["events"]) and nes(h["words"]), "handler block (events must list day, days and dry_run)")
    c = rec["closure"]
    need(isinstance(c, dict) and set(c) == {"members", "staged_probe_ran", "words"} and isinstance(c["members"], list) and c["members"] and c["staged_probe_ran"] is True and nes(c["words"]),
         "closure block")
    need(sorted(c["members"]) == sorted(entry_members), "closure.members differ from the source-map entry's staged_from packaged_as names")
    need(any(m.endswith("cottonwood_bd_account_return_daily.py") for m in c["members"]) and any(m.endswith("lib/opal_naming.py") or m == "lib/opal_naming.py" for m in c["members"]) and
         any(m.endswith("trading_calendar.py") for m in c["members"]), "closure must carry the adapter, opal_naming and trading_calendar")
    sm = rec["source_map"]
    need(isinstance(sm, dict) and set(sm) == {"file", "entry", "pins_null", "words"} and sm["file"] == SOURCE_MAP_REL and sm["entry"] == ENTRY_KEY and sm["pins_null"] is True and nes(sm["words"]),
         "source_map block (pins stay null: the applier writes them)")
    t = rec["tests"]
    need(isinstance(t, dict) and set(t) == {"file", "new_tests"} and t["file"] == TESTS_REL and is_int(t["new_tests"]) and t["new_tests"] >= MIN_TESTS, "tests block")
    sc = rec["scheduling"]
    need(isinstance(sc, dict) and set(sc) == {"max_days_per_fire", "backfill_days_max", "scheduled_rule", "words"} and is_int(sc["max_days_per_fire"]) and 1 <= sc["max_days_per_fire"] <= 10
         and sc["backfill_days_max"] == 25 and nes(sc["scheduled_rule"]) and nes(sc["words"]), "scheduling block")
    fc = rec["files_changed"]
    need(isinstance(fc, list) and {f.get("file") for f in fc} >= {HANDLER_REL, TESTS_REL, SOURCE_MAP_REL}, "files_changed must name the handler, the tests and the source map")
    for f in fc:
        need(set(f) == {"file", "sha256", "kind"} and nes(f["kind"]) and file_exists(f["file"]) and HEX64.match(str(f["sha256"])) and sha_of(f["file"]) == f["sha256"],
             "files_changed entry %s: hash or form" % f.get("file"))
        need(f["file"].startswith(FN_DIR) or f["file"] == SOURCE_MAP_REL, "a changed file outside the grant: %s" % f["file"])
    need(rec["files_in_repo"] is False and rec["served_values_changed"] is False and rec["pushed"] is False and rec["deployed"] is False, "a flag is not false")
    need(not digit_runs(rec), "a run of 8 or more digits outside the exempt fields: %s" % digit_runs(rec)[:2])
    return True


def entry_of(root):
    sm = load(root, SOURCE_MAP_REL)
    e = sm.get("functions", {}).get(ENTRY_KEY)
    need(isinstance(e, dict), "the source map has no entry %s" % ENTRY_KEY)
    return e


def run(root, cid):
    root = Path(root)
    if cid == "DB122-4-AC1":
        hp = root / HANDLER_REL
        need(hp.is_file(), "no handler")
        names = {n.name for n in ast.walk(ast.parse(hp.read_text(encoding="utf-8"))) if isinstance(n, ast.FunctionDef)}
        need(set(FUNCS) <= names, "the handler lacks functions: %s" % sorted(set(FUNCS) - names))
        tp = root / TESTS_REL
        need(tp.is_file(), "no test file")
        n = len(re.findall(r"^def (test_\w+)", tp.read_text(encoding="utf-8"), re.M))
        need(n >= MIN_TESTS, "the test file holds %d tests (needs %d)" % (n, MIN_TESTS))
        r = subprocess.run([sys.executable, "-m", "pytest", "-q", "--no-header", "-p", "no:cacheprovider", str(tp)], cwd=str(root), capture_output=True, text=True, timeout=250)
        m = re.search(r"(\d+) passed", r.stdout)
        need(r.returncode == 0 and m and int(m.group(1)) >= MIN_TESTS and "failed" not in r.stdout, "pytest: rc %s, %s" % (r.returncode, (r.stdout.strip().splitlines() or ["no output"])[-1]))
        print("OK: the handler has lambda_handler, owed_days and newest_landed_day; %s tests pass" % m.group(1))
        return True
    if cid == "DB122-4-AC2":
        o, names = run_probe(root, entry_of(root))
        check_probe(o)
        print("OK: staged probe: the handler and %d staged members run with NO repo checkout: owed_days through T-1 and capped, a full day writes two objects, dry_run and a held day write nothing, "
              "two days write four, a bad day and a 30-day event are refused before any write" % len(names))
        return True
    if cid == "DB122-4-AC3":
        rec = load(root, REC_REL)
        members = [m["packaged_as"] for m in entry_of(root).get("staged_from", [])]
        check_facts(rec, lambda rel: hashlib.sha256((root / rel).read_bytes()).hexdigest(), lambda rel: (root / rel).is_file(), members)
        cs = own_commits(root)
        gain, lose = own_numstat(root, cs, SOURCE_MAP_REL)
        need(gain >= 15 and lose == 0, "the source map must only gain lines in the worker's own commits: +%d/-%d (needs gain >= 15, lose 0)" % (gain, lose))
        for m in entry_of(root)["staged_from"]:
            need(m.get("pin") is None and m.get("sha256") is None, "pins and hashes stay null for the applier: %s" % m.get("repo_path"))
        stray = sorted(f for f in own_files(root, cs) if f.startswith(("infra/", "data/", "lib/", "org/standards/")) and not f.startswith(FN_DIR) and f != SOURCE_MAP_REL and (root / f).exists())  # a path the worker moved away no longer exists: not stray (round 122, W203-S5)
        need(not stray, "this worker's commits changed files outside the grant: %s" % stray[:3])
        print("OK: facts record valid, closure members equal the entry's, files hashed; the source map gains %d lines and loses none; pins null; nothing else under infra/, data/, lib/ or org/standards/" % gain)
        return True
    raise Fail("unknown criterion %s" % cid)


def selftest():
    import copy
    good_probe = {"in_stage": True, "owed_after": ["2026-07-13", "2026-07-14"], "owed_none": ["2026-07-14"], "owed_closed": [], "owed_cap": 5, "cap_const": 5,
                  "full": {"ok": True, "puts": 2, "days": ["2026-07-14"]}, "dry": {"ok": True, "puts": 0}, "held": {"ok": True, "puts": 0, "held": 1},
                  "two": {"puts": 4, "days": ["2026-07-14", "2026-07-15"]}, "bad": {"raised": True, "puts": 0}, "many": {"raised": True, "puts": 0}}
    assert check_probe(copy.deepcopy(good_probe))
    for key, val in (("in_stage", False), ("owed_after", ["2026-07-14"]), ("owed_none", []), ("owed_cap", 9), ("full", {"ok": True, "puts": 1, "days": ["2026-07-14"]}),
                     ("dry", {"ok": True, "puts": 2}), ("held", {"ok": True, "puts": 0, "held": 0}), ("two", {"puts": 2, "days": ["x"]}), ("bad", {"raised": False, "puts": 0}),
                     ("many", {"raised": True, "puts": 2})):
        o = copy.deepcopy(good_probe)
        o[key] = val
        try:
            check_probe(o)
            raise AssertionError("red probe arm %s passed" % key)
        except Fail:
            pass
    members = ["data/assets/scripts/gold/irpt_reporting/adapters/cottonwood_bd_account_return_daily.py", "lib/opal_naming.py", "lib/trading_calendar.py"]
    fc = [{"file": f, "sha256": "ab" * 32, "kind": "k"} for f in (HANDLER_REL, TESTS_REL, SOURCE_MAP_REL)]
    good = {"handler": {"file": HANDLER_REL, "functions": list(FUNCS), "events": ["day", "days", "dry_run"], "words": "w"},
            "closure": {"members": list(members), "staged_probe_ran": True, "words": "w"}, "source_map": {"file": SOURCE_MAP_REL, "entry": ENTRY_KEY, "pins_null": True, "words": "w"},
            "tests": {"file": TESTS_REL, "new_tests": 9}, "scheduling": {"max_days_per_fire": 5, "backfill_days_max": 25, "scheduled_rule": "r", "words": "w"},
            "files_changed": fc, "words": "w", "claim": "inferred", "files_in_repo": False, "served_values_changed": False, "pushed": False, "deployed": False}

    def grade(r, mem=members, sha="ab" * 32):
        try:
            return check_facts(r, lambda rel: sha, lambda rel: True, mem)
        except Fail:
            return False
    assert grade(copy.deepcopy(good)) is True
    for f in (lambda r: r["handler"].update(events=["day"]), lambda r: r["closure"].update(staged_probe_ran=False), lambda r: r["closure"].update(members=["x"]),
              lambda r: r["source_map"].update(pins_null=False), lambda r: r["tests"].update(new_tests=2), lambda r: r["scheduling"].update(backfill_days_max=50),
              lambda r: r.update(deployed=True), lambda r: r["files_changed"].append({"file": "infra/x.tf", "sha256": "ab" * 32, "kind": "k"}), lambda r: r.update(words="id 1234567890")):
        r = copy.deepcopy(good)
        f(r)
        assert grade(r) is False
    assert grade(copy.deepcopy(good), mem=members[:2]) is False
    print("selftest: ten probe arms and ten facts arms behave")


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
