"""IRPT_DASHBD round 149, workstream HISTSCOPE (issuer 2.0.0_SA_COO~D2) -- DB-b-294, the PRODUCERS DERIVE history_scope PER ACCOUNT (CTO ruling msg 9226, row D2-S113): an account whose first value day equals the source
floor is PARTIAL_HISTORY, an account first seen after the floor is FULL, and every row of a derived partition carries the conditional column history_scope_claim = "inferred" (source contract 0.4.6). Two
producers write history_scope and are changed here: the 49 Financial producer (data/assets/scripts/gold/irpt_reporting/account_return_daily.py, compute_range + emit_day, floor = the earliest balance partition) and
the Cottonwood Black Diamond adapter (adapters/cottonwood_bd_account_return_daily.py, derive_rows + derive + to_table + run_day, floor day = the landing handler's FLOOR_DAY) with its landing handler. The Inflection
adapters are NOT changed (no series is published from them). A caller that cannot name the floor keeps the old constant and writes NO claim. LOCAL: python files; nothing is run against AWS.

  DB-b-294 (~237)   account_return_daily.py + adapters/cottonwood_bd_account_return_daily.py + infra/aws/lambda/investor-reporting/account-return-daily/handler.py + tests/test_history_scope_derivation.py + a facts record
                    DB162-1-AC1 (the 49 Financial producer: compute_range, table_for, emit_day),
                    DB162-1-AC2 (the Cottonwood adapter and its landing handler),
                    DB162-1-AC3 (the new tests, the whole gold tests directory and the landing handler's tests, the grant, the facts record)

Usage: python <this file> <repo_root> <criterion_id>      prints "<id> PASS" or "<id> FAIL" last
       python <this file> --selftest                       the pure clauses on synthetic arms
"""
import copy
import hashlib
import importlib.util
import io
import json
import re
import subprocess
import sys
from pathlib import Path

D = "org/missions/D9/IRPT/IRPT_DASHBD/deliverables/"
AUTHOR = "0.9.0_WK_IRPT_DASHBD~237"
REC_REL = D + AUTHOR + "/RD_HISTSCOPE_PRODUCERS_FACTS_R149.json"
ORDER_REL = "org/missions/D9/IRPT/IRPT_DASHBD/task-orders/IRPT_DASHBD.TO-DB-b-294.producers-derive-history-scope.md"
GOLD = "data/assets/scripts/gold/irpt_reporting/"
ARD_REL = GOLD + "account_return_daily.py"
CBD_REL = GOLD + "adapters/cottonwood_bd_account_return_daily.py"
HANDLER_REL = "infra/aws/lambda/investor-reporting/account-return-daily/handler.py"
TEST_REL = GOLD + "tests/test_history_scope_derivation.py"
TESTS_DIR = GOLD + "tests"
HANDLER_TESTS = "infra/aws/lambda/investor-reporting/account-return-daily"
CONTRACT_REL = "org/standards/IRPT_DASHBD_ACCOUNT_RETURN_DAILY_CONTRACT.json"
GRANT_FILES = {ARD_REL, CBD_REL, HANDLER_REL, TEST_REL}
GRANT_PREFIXES = (D + AUTHOR + "/", "org/missions/D9/IRPT/IRPT_DASHBD/surprise-channel/investigations/", "org/missions/D9/IRPT/IRPT_DASHBD/task-orders/", HANDLER_TESTS + "/tests/")
KNOWN_RED = "test_account_activity_lots.py::test_the_calendar_itself_raises_before_2010_and_the_index_never_asks_it"
CLAIM_COL, CLAIM = "history_scope_claim", "inferred"
FLOOR = "2026-07-10"
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


def load(path, name):
    spec = importlib.util.spec_from_file_location(name, str(path))
    mod = importlib.util.module_from_spec(spec)
    sys.modules[name] = mod
    spec.loader.exec_module(mod)
    return mod


def paths(root):
    for p in (root / "lib", root / GOLD.rstrip("/"), root / GOLD / "adapters", root):
        if str(p) not in sys.path:
            sys.path.insert(0, str(p))


# ------------------------------------------------------------------------------------------------ the 49 Financial producer
FIRM_BOX = ["firm-unset"]


class Flows:
    def get(self, d):
        return ({}, {}, {}, {}, False)


def ard_run(ard, first_data, bal_days):
    days = ["2026-07-13", "2026-07-14", "2026-07-15"]
    vc = {"2026-07-10": {"A": 100.0}, "2026-07-13": {"A": 101.0, "B": 50.0}, "2026-07-14": {"A": 102.0, "B": 51.0, "C": 70.0}, "2026-07-15": {"A": 103.0, "B": 52.0, "C": 71.0}}
    rows, _notes, _fs = ard.compute_range(None, {"method_version": 2}, FIRM_BOX[0], days, days + ["2026-07-10"], accounts=["A", "B", "C"], thresholds=None, flows=Flows(), value_cache=copy.deepcopy(vc),
                                          holdings_cache={d: {} for d in days}, first_data=first_data, bal_days=bal_days)
    by = {}
    for r in rows:
        by.setdefault(r["account_id"], []).append(r)
    return rows, by


class FakeS3:
    def __init__(self):
        self.puts = {}

    def put_object(self, Bucket, Key, Body, **kw):
        self.puts[Key] = bytes(Body)
        return {}


def check_ard(root):
    paths(root)
    ard = load(root / ARD_REL, "ard_under_check")
    doc = ard.load_declaration()
    FIRM_BOX[0] = ard.firm_scope(ard.source_entry(doc, ard.declared_sources(doc)[0]))
    bal = ["2026-07-10", "2026-07-13", "2026-07-14", "2026-07-15"]
    first = {"A": "2026-07-10", "B": "2026-07-13", "C": "2026-07-14"}
    rows, by = ard_run(ard, dict(first), bal)
    need(set(by) == {"A", "B", "C"}, "the three accounts must produce rows")
    want = {"A": "PARTIAL_HISTORY", "B": "FULL", "C": "FULL"}
    for a, rs in by.items():
        need(all(r["history_scope"] == want[a] for r in rs), "account %s: history_scope must be %s on every row (first value day vs the source floor %s), got %s" % (a, want[a], bal[0], sorted({r["history_scope"] for r in rs})))
        need(all(r.get(CLAIM_COL) == CLAIM for r in rs), "account %s: every row of a derived partition carries %s = %s" % (a, CLAIM_COL, CLAIM))
    # no durable inception, no floor: the old constant and NO claim, on every row
    for label, fd, bd in (("no first_data (window-local inception)", None, bal), ("no bal_days", dict(first), None), ("empty bal_days", dict(first), [])):
        rows2, _ = ard_run(ard, fd, bd)
        need(rows2 and all(r["history_scope"] == "PARTIAL_HISTORY" and CLAIM_COL not in r for r in rows2), "%s: rows must keep PARTIAL_HISTORY and carry NO %s" % (label, CLAIM_COL))
    import pandas as pd
    # table_for: the 19 columns, plus the conditional column only when the frame carries it
    need(hasattr(ard, "table_for"), "account_return_daily.py must define table_for(frame)")
    legacy_rows, _ = ard_run(ard, None, bal)
    clean = lambda rs: pd.DataFrame([{k: v for k, v in r.items() if not k.startswith("_")} for r in rs])  # noqa: E731
    t0 = ard.table_for(clean(legacy_rows))
    need(t0.schema.equals(ard.ARROW_SCHEMA), "a frame without the claim must give exactly the 19-column ARROW_SCHEMA")
    t1 = ard.table_for(clean(rows))
    need(t1.schema.names == list(ard.COLUMNS) + [CLAIM_COL] and str(t1.schema.field(CLAIM_COL).type) == "string" and set(t1[CLAIM_COL].to_pylist()) == {CLAIM}, "a frame with the claim must give the 19 columns then %s (string, every value %s)" % (CLAIM_COL, CLAIM))
    # the schema constants and the contract hash are untouched
    lines = sorted("%s:%s" % (f.name, f.type) for f in ard.ARROW_SCHEMA)
    contract = json.loads((root / CONTRACT_REL).read_bytes().decode("utf-8"))
    need(len(ard.ARROW_SCHEMA) == 19 and hashlib.sha256("\n".join(lines).encode()).hexdigest() == contract["schema_hash"], "ARROW_SCHEMA must stay the 19 columns of the contract's schema_hash")
    # emit_day writes the claim column through the one table builder, with the table's own schema
    rec = []
    ard.sp.stream_to_parquet = lambda tables, schema, s3, bucket, key: (rec.append((schema.names, tables[0].num_rows, key)) or {"etag": "e", "bytes": 1})
    s3 = FakeS3()
    for frame, names in ((clean(rows), list(ard.COLUMNS) + [CLAIM_COL]), (clean(legacy_rows), list(ard.COLUMNS))):
        rec.clear()
        day = "2026-07-15"
        part = frame[frame["business_date"] == day].reset_index(drop=True)
        ard.emit_day(s3, part, FIRM_BOX[0], day, upload=True, thresholds=None, first_data_date=first, src={"method_version": 2})
        need(len(rec) == 1 and rec[0][0] == names, "emit_day must stream the table with columns %s, got %s" % (names[-2:], rec[0][0][-2:] if rec else None))
    # the enum check accepts the derived frame (FULL is a member)
    ard._check_enums(clean(rows))
    return True


# ------------------------------------------------------------------------------------------------ the Cottonwood adapter and landing handler
def pa_mod():
    import pyarrow as pa
    return pa


class FakeReader:
    def __init__(self, alloc, trans):
        self.a, self.t, self.reads = alloc, trans, 0

    def list_partitions(self, table):
        return sorted((self.a if table == "fact_allocations" else self.t).keys())

    def read_parquet(self, table, day):
        self.reads += 1
        return (self.a if table == "fact_allocations" else self.t)[day]


class FakeWriter:
    def __init__(self):
        self.puts = {}

    def put_object(self, Bucket, Key, Body, **kw):
        self.puts[Key] = bytes(Body)
        return {}

    def list_objects_v2(self, Bucket, Prefix, **kw):
        keys = sorted(k for k in self.puts if k.startswith(Prefix))
        return {"KeyCount": len(keys), "Contents": [{"Key": k} for k in keys], "IsTruncated": False}


X, Y = "AB12345678C", "AB87654321D"
NEXT, PREV = "2026-07-14", "2026-07-13"


def reader(with_floor=True):
    pa = pa_mod()
    alloc = lambda pairs: pa.table({"AccountID": [a for a, _v in pairs], "Account Market Value": [v for _a, v in pairs]})  # noqa: E731
    empty = pa.table({"AccountID": pa.array([], pa.string()), "Trade Date": pa.array([], pa.string()), "External Flow": pa.array([], pa.string()),
                      "Transaction Type": pa.array([], pa.string()), "Market Value": pa.array([], pa.float64())})
    a = {PREV: alloc([(X, 101.0), (Y, 50.0)]), NEXT: alloc([(X, 102.0), (Y, 51.0)])}
    if with_floor:
        a[FLOOR] = alloc([(X, 100.0)])
    return FakeReader(a, {FLOOR: empty, PREV: empty, NEXT: empty})


def read_written(w):
    import pyarrow.parquet as pq
    data = [k for k in w.puts if k.endswith("data.parquet")]
    man = [k for k in w.puts if k.endswith("manifest.json")]
    need(len(data) == 1 and len(man) == 1, "run_day must write exactly one data.parquet and one manifest.json, wrote %d and %d" % (len(data), len(man)))
    return pq.read_table(io.BytesIO(w.puts[data[0]])), json.loads(w.puts[man[0]].decode("utf-8"))


def check_cbd(root):
    paths(root)
    cbd = load(root / CBD_REL, "cbd_under_check")
    contract = json.loads((root / CONTRACT_REL).read_bytes().decode("utf-8"))
    need(cbd.schema_hash() == contract["schema_hash"] and len(cbd.ARROW_SCHEMA) == 19 and len(cbd.SCHEMA_WITH_SOURCE) == 20, "the adapter's schema constants and hash must be untouched (19 columns, 20 with the source label)")
    h0 = next(s for s in contract["supersedes"] if s["contract_version"] == "0.3.0")["schema_hash_with_optional"]
    need(cbd.schema_hash_with_optional() == h0, "schema_hash_with_optional() must stay the 0.3.0 value")
    # derived: floor day given and present
    w = FakeWriter()
    res = cbd.run_day(reader(), w, NEXT, upload=True, floor_day=FLOOR)
    need(res["held"] is False and res["rows"] == 2, "run_day with a floor day must write the day's two rows")
    t, man = read_written(w)
    names = t.schema.names
    need(len(names) == 21 and names[19] == "source" and names[20] == CLAIM_COL, "a derived day's table must be the 19 columns, source, then %s (21 columns), got %d ending %s" % (CLAIM_COL, len(names), names[-2:]))
    got = {r["account_id"]: r for r in t.to_pylist()}
    need(got[X]["history_scope"] == "PARTIAL_HISTORY" and got[Y]["history_scope"] == "FULL" and all(r[CLAIM_COL] == CLAIM for r in got.values()),
         "the account with a value on the floor day is PARTIAL_HISTORY, the one first seen after it FULL, both carry the claim")
    need(man["columns"] == names and man["schema_hash_with_optional"] == h0, "the manifest lists the table's columns and keeps the 0.3.0 schema_hash_with_optional")
    # legacy: no floor day, floor partition absent
    for label, rd, kw in (("no floor day", reader(), {}), ("floor partition absent", reader(False), {"floor_day": FLOOR})):
        w2 = FakeWriter()
        cbd.run_day(rd, w2, NEXT, upload=True, **kw)
        t2, _ = read_written(w2)
        need(len(t2.schema.names) == 20 and CLAIM_COL not in t2.schema.names and {r["history_scope"] for r in t2.to_pylist()} == {"PARTIAL_HISTORY"}, "%s: the old 20-column table with PARTIAL_HISTORY and NO claim" % label)
    # the landing handler passes its FLOOR_DAY: a day landed through lambda_handler carries the derived scope
    handler = load(root / HANDLER_REL, "landing_handler_under_check")
    need(handler.FLOOR_DAY == FLOOR, "the landing handler's FLOOR_DAY must stay %s" % FLOOR)
    w3 = FakeWriter()
    handler.lambda_handler({"day": NEXT}, None, s3=w3, reader=reader())
    t3, _ = read_written(w3)
    g3 = {r["account_id"]: r for r in t3.to_pylist()}
    need(t3.schema.names[-1] == CLAIM_COL and g3[X]["history_scope"] == "PARTIAL_HISTORY" and g3[Y]["history_scope"] == "FULL", "a day landed through the handler carries the derived history_scope and the claim")
    return True


# ------------------------------------------------------------------------------------------------ grant, facts, tests
def check_grant(changed):
    bad = [f for f in changed if f not in GRANT_FILES and not f.startswith(GRANT_PREFIXES)]
    need(not bad, "the worker's commits touch files outside its grant: %s" % bad[:3])
    need(ARD_REL in changed and CBD_REL in changed and HANDLER_REL in changed and TEST_REL in changed, "both producers, the landing handler and the new test file must all change")
    return True


def check_facts(rec, n_tests):
    exp = {"claim_column", "claim_value", "method", "producers", "legacy_without_floor", "tests", "words"}
    need(isinstance(rec, dict) and set(rec) == exp, "record keys differ: %s" % (sorted(set(rec) ^ exp) if isinstance(rec, dict) else "?"))
    need(rec["claim_column"] == CLAIM_COL and rec["claim_value"] == CLAIM and rec["method"] == "first value day vs source floor", "claim column, value or method differ")
    need(rec["producers"] == ["account_return_daily.py", "cottonwood_bd_account_return_daily.py"] and rec["legacy_without_floor"] is True, "producers or the legacy statement differ")
    need(isinstance(rec["tests"], int) and not isinstance(rec["tests"], bool) and rec["tests"] == n_tests >= 10, "tests must equal the recount, at least 10")
    need(nes(rec["words"]) and 80 <= len(rec["words"]) <= 1800 and not LONG_DIGITS.findall(rec["words"]), "words must be one paragraph of 80 to 1800 characters with no long digit run")
    return True


def run_pytest(root, args):
    r = subprocess.run([sys.executable, "-m", "pytest", "-q", "-p", "no:cacheprovider"] + list(args), cwd=str(root), capture_output=True, text=True, timeout=1500)
    m = re.search(r"(\d+) passed", r.stdout)
    need(r.returncode == 0 and m is not None, "tests failed: %s" % r.stdout[-300:].replace("\n", " | "))
    return int(m.group(1))


def run(root, cid):
    root = Path(root)
    if cid == "DB162-1-AC1":
        check_ard(root)
        print("OK: the 49 Financial producer derives history_scope per account against the source floor (the earliest balance partition): the floor-start account is PARTIAL_HISTORY, the ones first seen after it FULL, every row carries history_scope_claim = inferred; with no durable inception or no floor the old constant and NO claim; table_for and emit_day write the 19 columns plus the claim only when the frame has it, and the 19-column schema and its contract hash are untouched")
        return True
    if cid == "DB162-1-AC2":
        check_cbd(root)
        print("OK: the Cottonwood adapter derives history_scope from the floor-day partition (a value on the floor day is PARTIAL_HISTORY, none is FULL) and writes 19 columns, source, then the claim; with no floor day or no floor partition the old 20-column table and NO claim; its constants and 0.3.0 hash are untouched; a day landed through the handler carries the derived scope")
        return True
    if cid == "DB162-1-AC3":
        need((root / TEST_REL).is_file(), "no %s" % TEST_REL)
        n = run_pytest(root, [TEST_REL])
        n_dir = run_pytest(root, [TESTS_DIR, "--deselect", GOLD + "tests/" + KNOWN_RED])
        n_h = run_pytest(root, [HANDLER_TESTS]) if (root / HANDLER_TESTS / "tests").is_dir() else 0
        need(n >= 10, "the new test file holds %d passing tests, at least 10 are owed" % n)
        changed = set()
        for cm in own_commits(root):
            changed |= set(git(root, "show", "--name-only", "--format=", cm).decode().split())
        check_grant(changed)
        check_facts(json.loads((root / REC_REL).read_bytes().decode("utf-8")), n)
        print("OK: %d new tests pass; the whole gold tests directory passes (%d tests, the one known pre-existing red deselected) and the landing handler's tests (%d); %d files changed, all in the grant; the facts record equals the recount" % (n, n_dir, n_h, len(changed)))
        return True
    raise Fail("unknown criterion %s" % cid)


def selftest():
    def red(fn, label):
        try:
            fn()
        except Fail:
            return
        raise AssertionError("red arm passed: " + label)
    assert check_grant({ARD_REL, CBD_REL, HANDLER_REL, TEST_REL, D + AUTHOR + "/x.json", HANDLER_TESTS + "/tests/test_x.py"})
    red(lambda: check_grant({ARD_REL, CBD_REL, HANDLER_REL}), "no test file")
    red(lambda: check_grant({ARD_REL, CBD_REL, HANDLER_REL, TEST_REL, "lib/x.py"}), "outside grant")
    red(lambda: check_grant({ARD_REL, CBD_REL, TEST_REL}), "no handler")
    rec = {"claim_column": CLAIM_COL, "claim_value": CLAIM, "method": "first value day vs source floor", "producers": ["account_return_daily.py", "cottonwood_bd_account_return_daily.py"],
           "legacy_without_floor": True, "tests": 10, "words": "w" * 100}
    assert check_facts(rec, 10)
    farms = (("column", lambda r: r.update(claim_column="x")), ("value", lambda r: r.update(claim_value="held")), ("method", lambda r: r.update(method="x")), ("producers", lambda r: r.update(producers=["a"])),
             ("legacy", lambda r: r.update(legacy_without_floor=False)), ("tests", lambda r: r.update(tests=11)), ("extra", lambda r: r.update(z=1)), ("words", lambda r: r.update(words="short")),
             ("digits", lambda r: r.update(words="w" * 100 + " 123456789")))
    for label, fn in farms:
        r2 = copy.deepcopy(rec)
        fn(r2)
        red(lambda: check_facts(r2, 10), label)
    red(lambda: check_facts(rec, 9), "tests below the recount")
    print("selftest: grant (3) and facts (%d) clauses behave; the behaviour clauses are exercised against a scratch reference and single-fault mutants by the issuer" % (len(farms) + 1))
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
