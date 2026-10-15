"""IRPT_DASHBD round 121, workstream B-49F (issuer 2.0.0_SA_COO~D2) -- DB-b-245, the COTTONWOOD ADAPTER BUILD (CTO analysis @9d4bd6adf3 ruling 4): the Black Diamond account
return adapter of round 119 gains what a landing needs, LOCAL, with fake clients only: the optional `source` column (contract 0.3.0), a write path for one day (data.parquet
and manifest.json at the builder address), a silver presence hold, a packaging-aware import root, and a manifest. Nothing is landed, scheduled, planned or written to AWS.

  DB-b-245 (~199) data/assets/scripts/gold/irpt_reporting/adapters/cottonwood_bd_account_return_daily.py gains, ADDITIVELY and without changing what its 19 tests pin:
                    SOURCE_COLUMN, schema_hash_with_optional(), to_table(rows, with_source=False), GoldWriteError, gold_prefix(), build_manifest(day, table, first_data_date),
                    write_day(s3, day, table, manifest), presence_hold(reader, day), run_day(reader, s3, day, upload=True), _find_root(start).
                                                                                           DB121-4-AC1 (the tests pass, the functions exist),
                                                                                           DB121-4-AC2 (behaviour, probed by this checker with fake clients),
                                                                                           DB121-4-AC3 (the facts record and the change is additive)

Usage: python <this file> <repo_root> <criterion_id>      prints "<id> PASS" or "<id> FAIL" last
       python <this file> --selftest [<repo_root>]          the record clauses on synthetic arms
"""
import ast
import hashlib
import json
import re
import subprocess
import sys
import tempfile
from pathlib import Path

D = "org/missions/D9/IRPT/IRPT_DASHBD/deliverables/"
REC_REL = D + "0.9.0_WK_IRPT_DASHBD~199/RD_CW_BUILD_FACTS_R121.json"
ORDER_REL = "org/missions/D9/IRPT/IRPT_DASHBD/task-orders/IRPT_DASHBD.TO-DB-b-245.cottonwood-adapter-build-source-column-write-path-presence-hold.md"
ADAPTER_REL = "data/assets/scripts/gold/irpt_reporting/adapters/cottonwood_bd_account_return_daily.py"
TEST_REL = "data/assets/scripts/gold/irpt_reporting/tests/test_cottonwood_bd_account_return_daily.py"
CONTRACT_REL = "org/standards/IRPT_DASHBD_ACCOUNT_RETURN_DAILY_CONTRACT.json"
BASE_TESTS = 19
MIN_NEW_TESTS = 8
FUNCS = ("schema_hash_with_optional", "to_table", "gold_prefix", "build_manifest", "write_day", "presence_hold", "run_day", "_find_root")
MANIFEST_KEYS = {"table", "firm", "business_date", "rows", "schema_version", "method_version", "label", "columns", "schema_hash_with_optional", "contract_version",
                 "first_data_date", "thresholds_claim"}
CLAIMS = ("measured", "inferred", "held", "absent")
LONG_DIGITS = re.compile(r"\d{8,}")
DIGIT_OK_KEYS = ("sha256", "path", "file", "key", "where", "vintage", "first_data_date")
HEX64 = re.compile(r"[0-9a-f]{64}$")
ISO = re.compile(r"\d{4}-\d{2}-\d{2}$")


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


def base_commit(root):
    out = git(root, "log", "--diff-filter=A", "--format=%H", "--", ORDER_REL).split()
    need(out, "the order's first commit is not in this history")
    return out[-1]


def numstat(root, base, rel):
    out = git(root, "diff", "--numstat", base, "HEAD", "--", rel).strip().split("\n")[0].split("\t")
    need(len(out) >= 2 and out[0].isdigit() and out[1].isdigit(), "no change recorded for %s" % rel)
    return int(out[0]), int(out[1])


def own_commits(root, author):
    """The commits of this order's worker (author serial), oldest first, since the order was issued: the diff clauses read these commits only, never a whole-repo base..HEAD
    (other seats commit to the same trunk). Round 122 ruling 3."""
    base = base_commit(root)
    out = git(root, "log", "--reverse", "--format=%H", "--author=" + author, base + "..HEAD").split()
    need(out, "no commit by %s since the order was issued" % author)
    return out


def own_numstat(root, commits, rel):
    add = dele = 0
    for c in commits:
        for ln in git(root, "show", "--numstat", "--format=", c, "--", rel).strip().splitlines():
            parts = ln.split("	")
            if len(parts) >= 2 and parts[0].isdigit() and parts[1].isdigit():
                add += int(parts[0])
                dele += int(parts[1])
    return add, dele


def own_files(root, commits):
    names = set()
    for c in commits:
        names |= set(git(root, "show", "--name-only", "--format=", c).split())
    return names


# ------------------------------------------------------------------------------------------------ the behaviour probe (runs in a child python)
PROBE = r'''
import io, json, sys, tempfile
from pathlib import Path
root = Path(sys.argv[1])
sys.path.insert(0, str(root / "data/assets/scripts/gold/irpt_reporting/adapters"))
import pyarrow as pa
import pyarrow.parquet as pq
import cottonwood_bd_account_return_daily as ad
out = {}
contract = json.loads((root / "org/standards/IRPT_DASHBD_ACCOUNT_RETURN_DAILY_CONTRACT.json").read_bytes().decode("utf-8"))
out["hash_19"] = ad.schema_hash() == contract["schema_hash"]
out["hash_20"] = ad.schema_hash_with_optional() == contract["schema_hash_with_optional"]
row = {"firm": ad.FIRM, "account_id": "A0000000001", "business_date": "2026-07-14", "market_value_eod": 10.0, "external_flow": 0.0, "income_received": None,
       "income_return": None, "total_return_daily": 0.01, "return_basis": "VENDOR_VALUE", "holdings_price_return": None, "holdings_price_return_reason": None,
       "fee_amount": None, "fee_amount_reason": "x", "day_quality": "MEASURED", "guard_state": "NOT_GRADED", "history_scope": "FULL", "carried_days": 0,
       "method_version": 2, "schema_version": "1.0"}
t19 = ad.to_table([row])
t20 = ad.to_table([row], with_source=True)
out["cols_19"] = len(t19.schema.names)
out["cols_20"] = len(t20.schema.names)
out["source_values"] = sorted(set(t20.column("source").to_pylist())) if "source" in t20.schema.names else None
out["label"] = ad.LABEL


class FakeS3(object):
    def __init__(self):
        self.puts = []

    def put_object(self, Bucket, Key, Body, **kw):
        self.puts.append((Bucket, Key, bytes(Body)))
        return {}


bucket, prefix = ad.gold_prefix()
out["prefix_ok"] = isinstance(bucket, str) and prefix.endswith("/") and "account_return_daily" in prefix
man = ad.build_manifest("2026-07-14", t20, "2026-07-10")
out["manifest_keys"] = sorted(man)
out["manifest_method"] = man.get("method_version")
out["manifest_cols"] = len(man.get("columns", []))
out["manifest_hash"] = man.get("schema_hash_with_optional") == contract["schema_hash_with_optional"]
s3 = FakeS3()
res = ad.write_day(s3, "2026-07-14", t20, man)
out["write_keys"] = sorted(k for _b, k, _x in s3.puts)
out["write_expected"] = sorted([prefix + "date=2026-07-14/data.parquet", prefix + "date=2026-07-14/manifest.json"])
out["write_bucket_ok"] = all(b == bucket for b, _k, _x in s3.puts)
out["write_rows"] = res.get("rows") if isinstance(res, dict) else None
refused = {}
for name, args in (("empty", ("2026-07-14", t20.slice(0, 0), man)), ("bad_day", ("2026-13-45", t20, man)), ("other_table", ("2026-07-14", t20, dict(man, table="other")))):
    s = FakeS3()
    try:
        ad.write_day(s, *args)
        refused[name] = False
    except ad.GoldWriteError:
        refused[name] = len(s.puts) == 0
    except Exception:
        refused[name] = False
out["refused"] = refused
out["err_is_permission"] = issubclass(ad.GoldWriteError, PermissionError)


def alloc(day_vals):
    return pa.table({"AccountID": [a for a, _v in day_vals], "Account Market Value": [v for _a, v in day_vals]})


def trans():
    return pa.table({"AccountID": pa.array([], pa.string()), "Trade Date": pa.array([], pa.string()), "External Flow": pa.array([], pa.string()),
                     "Transaction Type": pa.array([], pa.string()), "Market Value": pa.array([], pa.float64())})


class FakeReader(object):
    def __init__(self, alloc_days, trans_days):
        self.a, self.t = alloc_days, trans_days
        self.reads = 0

    def list_partitions(self, table):
        return sorted((self.a if table == "fact_allocations" else self.t).keys())

    def read_parquet(self, table, day):
        return (self.a if table == "fact_allocations" else self.t)[day]


full = FakeReader({"2026-07-13": alloc([("A0000000001", 100.0), ("A0000000002", 200.0)]), "2026-07-14": alloc([("A0000000001", 101.0), ("A0000000002", 198.0)])},
                  {"2026-07-13": trans(), "2026-07-14": trans()})
out["hold_none"] = ad.presence_hold(full, "2026-07-14") is None
missing_t = FakeReader(full.a, {"2026-07-13": trans()})
h1 = ad.presence_hold(missing_t, "2026-07-14")
out["hold_missing_trans"] = isinstance(h1, str) and h1.startswith("HOLD")
empty_a = FakeReader({"2026-07-13": alloc([("A0000000001", 100.0)]), "2026-07-14": alloc([])}, full.t)
h2 = ad.presence_hold(empty_a, "2026-07-14")
out["hold_empty_alloc"] = isinstance(h2, str) and h2.startswith("HOLD")
s = FakeS3()
r = ad.run_day(missing_t, s, "2026-07-14")
out["run_hold"] = {"held": r.get("held"), "puts": len(s.puts)}
s = FakeS3()
r = ad.run_day(full, s, "2026-07-14")
out["run_ok_held"] = r.get("held")
out["run_ok_puts"] = len(s.puts)
rows_back = None
if s.puts:
    data = [x for _b, k, x in s.puts if k.endswith("data.parquet")]
    mani = [x for _b, k, x in s.puts if k.endswith("manifest.json")]
    if data:
        tb = pq.read_table(io.BytesIO(data[0]))
        rows_back = {"rows": tb.num_rows, "cols": len(tb.schema.names), "dates": sorted(set(tb.column("business_date").to_pylist())), "has_source": "source" in tb.schema.names}
    if mani:
        out["run_manifest"] = sorted(json.loads(mani[0].decode("utf-8")))
out["run_data"] = rows_back
s = FakeS3()
r = ad.run_day(full, s, "2026-07-14", upload=False)
out["run_noupload_puts"] = len(s.puts)
tmp = Path(tempfile.mkdtemp())
(tmp / "lib").mkdir()
(tmp / "lib" / "opal_naming.py").write_text("x = 1\n")
deep = tmp / "a" / "b" / "c"
deep.mkdir(parents=True)
out["find_root"] = str(Path(ad._find_root(deep / "m.py")).resolve()) == str(tmp.resolve())
print("PROBE " + json.dumps(out))
'''


def run_probe(root):
    with tempfile.TemporaryDirectory() as td:
        pp = Path(td) / "probe.py"
        pp.write_text(PROBE, encoding="utf-8")
        r = subprocess.run([sys.executable, "-I", str(pp), str(root)], capture_output=True, text=True, timeout=200)
    line = [ln for ln in r.stdout.splitlines() if ln.startswith("PROBE ")]
    need(line, "the probe printed no result (rc %s): %s" % (r.returncode, (r.stderr.strip().splitlines() or ["no stderr"])[-1][:300]))
    return json.loads(line[0][len("PROBE "):])


def check_probe(o):
    need(o["hash_19"], "the 19-column schema_hash() no longer equals the contract's schema_hash")
    need(o["hash_20"], "schema_hash_with_optional() differs from the contract's")
    need(o["cols_19"] == 19 and o["cols_20"] == 20, "to_table columns: default %s, with_source %s (want 19 and 20)" % (o["cols_19"], o["cols_20"]))
    need(o["source_values"] == [o["label"]], "the source column must hold the adapter's LABEL on every row, found %s" % o["source_values"])
    need(o["prefix_ok"], "gold_prefix() must return (bucket, key prefix ending in a slash holding account_return_daily)")
    need(set(o["manifest_keys"]) >= MANIFEST_KEYS, "manifest keys missing: %s" % sorted(MANIFEST_KEYS - set(o["manifest_keys"])))
    need(o["manifest_method"] == 2 and o["manifest_cols"] == 20 and o["manifest_hash"], "manifest: method_version, columns or schema_hash_with_optional")
    need(o["write_keys"] == o["write_expected"] and o["write_bucket_ok"], "write_day must put exactly data.parquet and manifest.json under the builder prefix: %s" % o["write_keys"])
    need(o["write_rows"] == 1, "write_day must return {rows: n}")
    need(o["refused"] == {"empty": True, "bad_day": True, "other_table": True} and o["err_is_permission"], "write_day must refuse an empty table, a bad day and another table with GoldWriteError, writing nothing: %s" % o["refused"])
    need(o["hold_none"] and o["hold_missing_trans"] and o["hold_empty_alloc"], "presence_hold: none when both tables hold the day; HOLD when a table lacks it or allocations are empty")
    need(o["run_hold"] == {"held": True, "puts": 0}, "run_day on a held day must write nothing: %s" % o["run_hold"])
    need(o["run_ok_held"] is False and o["run_ok_puts"] == 2, "run_day on a full day must write two objects")
    need(o["run_data"] == {"rows": 2, "cols": 20, "dates": ["2026-07-14"], "has_source": True}, "run_day wrote %s" % o["run_data"])
    need(set(o["run_manifest"]) >= MANIFEST_KEYS, "the written manifest lacks keys")
    need(o["run_noupload_puts"] == 0, "run_day(upload=False) must write nothing")
    need(o["find_root"], "_find_root must walk up to the directory holding lib/opal_naming.py")
    return True


# ------------------------------------------------------------------------------------------------ the record clauses (pure)
def check_facts(rec, sha_of, file_exists):
    exp = {"adapter", "tests", "manifest", "packaging", "method_row", "files_changed", "words", "claim", "files_in_repo", "served_values_changed", "pushed", "deployed"}
    need(isinstance(rec, dict) and set(rec) == exp, "record keys differ: %s" % (sorted(set(rec) ^ exp) if isinstance(rec, dict) else "?"))
    need(nes(rec["words"]) and rec["claim"] in CLAIMS, "words or claim")
    a = rec["adapter"]
    need(isinstance(a, dict) and set(a) == {"file", "functions_added", "source_column_values", "hash_with_optional", "words"} and a["file"] == ADAPTER_REL and nes(a["words"])
         and isinstance(a["functions_added"], list) and set(FUNCS) <= set(a["functions_added"]) and isinstance(a["source_column_values"], list) and a["source_column_values"]
         and HEX64.match(str(a["hash_with_optional"])), "adapter block")
    t = rec["tests"]
    need(isinstance(t, dict) and set(t) == {"file", "new_tests", "total"} and t["file"] == TEST_REL and is_int(t["new_tests"]) and t["new_tests"] >= MIN_NEW_TESTS
         and is_int(t["total"]) and t["total"] >= BASE_TESTS + MIN_NEW_TESTS, "tests block")
    m = rec["manifest"]
    need(isinstance(m, dict) and set(m) == {"keys", "first_data_date", "thresholds_claim", "words"} and isinstance(m["keys"], list) and set(m["keys"]) >= MANIFEST_KEYS
         and ISO.match(str(m["first_data_date"])) and m["thresholds_claim"] in CLAIMS and nes(m["words"]), "manifest block")
    p = rec["packaging"]
    need(isinstance(p, dict) and set(p) == {"find_root", "source_map_row_needed", "words"} and p["find_root"] is True and isinstance(p["source_map_row_needed"], bool) and nes(p["words"]),
         "packaging block")
    mr = rec["method_row"]
    need(isinstance(mr, dict) and set(mr) == {"decision", "words"} and mr["decision"] in ("NOT_WRITTEN_BY_THIS_ADAPTER", "WRITTEN_BY_THIS_ADAPTER") and nes(mr["words"]),
         "method_row block (decide whether this adapter writes the dim_return_method row; the one-prefix grant says it does not)")
    fc = rec["files_changed"]
    need(isinstance(fc, list) and {f.get("file") for f in fc} >= {ADAPTER_REL, TEST_REL}, "files_changed must name the adapter and its test file")
    for f in fc:
        need(set(f) == {"file", "sha256", "kind"} and nes(f["kind"]) and file_exists(f["file"]) and HEX64.match(str(f["sha256"])) and sha_of(f["file"]) == f["sha256"],
             "files_changed entry %s: hash or form" % f.get("file"))
        need(f["file"].startswith("data/assets/scripts/gold/irpt_reporting/"), "a changed file outside the grant: %s" % f["file"])
    need(rec["files_in_repo"] is False and rec["served_values_changed"] is False and rec["pushed"] is False and rec["deployed"] is False, "a flag is not false")
    need(not digit_runs(rec), "a run of 8 or more digits outside the exempt fields: %s" % digit_runs(rec)[:2])
    return True


def run(root, cid):
    root = Path(root)
    if cid == "DB121-4-AC1":
        src = (root / ADAPTER_REL).read_text(encoding="utf-8")
        names = {n.name for n in ast.walk(ast.parse(src)) if isinstance(n, ast.FunctionDef)}
        miss = [f for f in FUNCS if f not in names]
        need(not miss, "the adapter lacks functions: %s" % miss)
        need("class GoldWriteError" in src and "SOURCE_COLUMN" in src, "the adapter lacks GoldWriteError or SOURCE_COLUMN")
        tp = root / TEST_REL
        need(tp.is_file(), "no test file")
        n = len(re.findall(r"^def (test_\w+)", tp.read_text(encoding="utf-8"), re.M))
        need(n >= BASE_TESTS + MIN_NEW_TESTS, "the test file holds %d tests (needs at least %d)" % (n, BASE_TESTS + MIN_NEW_TESTS))
        r = subprocess.run([sys.executable, "-m", "pytest", "-q", "--no-header", "-p", "no:cacheprovider", str(tp)], cwd=str(root), capture_output=True, text=True, timeout=200)
        m = re.search(r"(\d+) passed", r.stdout)
        need(r.returncode == 0 and m and int(m.group(1)) >= BASE_TESTS + MIN_NEW_TESTS and "failed" not in r.stdout,
             "pytest: rc %s, %s" % (r.returncode, (r.stdout.strip().splitlines() or ["no output"])[-1]))
        print("OK: the adapter has the %d new functions, GoldWriteError and SOURCE_COLUMN; %s tests pass (%d earlier, %d new)" % (len(FUNCS), m.group(1), BASE_TESTS, n - BASE_TESTS))
        return True
    if cid == "DB121-4-AC2":
        o = run_probe(root)
        check_probe(o)
        print("OK: probed with fake clients: both hashes equal the contract's, 19 and 20 columns, source = the label, write_day puts exactly two objects under the builder prefix and refuses "
              "an empty table, a bad day and another table, presence_hold holds, run_day writes nothing on a held day and two objects on a full day, _find_root walks up")
        return True
    if cid == "DB121-4-AC3":
        rec = load(root, REC_REL)
        check_facts(rec, lambda rel: hashlib.sha256((root / rel).read_bytes()).hexdigest(), lambda rel: (root / rel).is_file())
        cs = own_commits(root, "0.9.0_WK_IRPT_DASHBD~199")
        add, dele = own_numstat(root, cs, ADAPTER_REL)
        need(add >= 60 and dele <= 12, "the adapter change must be additive: %d added, %d deleted (needs >= 60 and <= 12)" % (add, dele))
        a2, _d2 = own_numstat(root, cs, TEST_REL)
        need(a2 >= 50, "the test file gains %d lines (needs >= 50)" % a2)
        stray = sorted(f for f in own_files(root, cs) if f.startswith(("data/", "infra/", "lib/", "org/standards/")) and f not in (ADAPTER_REL, TEST_REL))
        need(not stray, "this worker's commits changed files outside the adapter and its test: %s" % stray[:3])
        print("OK: facts record valid, files hashed; the adapter gains %d lines and loses %d, its test file gains %d, nothing else under data/, infra/, lib/ or org/standards/ changes" % (add, dele, a2))
        return True
    raise Fail("unknown criterion %s" % cid)


def selftest(root):
    good_probe = {"hash_19": True, "hash_20": True, "cols_19": 19, "cols_20": 20, "source_values": ["L"], "label": "L", "prefix_ok": True, "manifest_keys": sorted(MANIFEST_KEYS),
                  "manifest_method": 2, "manifest_cols": 20, "manifest_hash": True, "write_keys": ["a", "b"], "write_expected": ["a", "b"], "write_bucket_ok": True, "write_rows": 1,
                  "refused": {"empty": True, "bad_day": True, "other_table": True}, "err_is_permission": True, "hold_none": True, "hold_missing_trans": True, "hold_empty_alloc": True,
                  "run_hold": {"held": True, "puts": 0}, "run_ok_held": False, "run_ok_puts": 2, "run_data": {"rows": 2, "cols": 20, "dates": ["2026-07-14"], "has_source": True},
                  "run_manifest": sorted(MANIFEST_KEYS), "run_noupload_puts": 0, "find_root": True}
    need(check_probe(dict(good_probe)) is True, "GREEN probe arm failed")
    for key, val in (("hash_19", False), ("cols_20", 19), ("source_values", ["x"]), ("write_keys", ["a"]), ("refused", {"empty": True, "bad_day": False, "other_table": True}),
                     ("hold_missing_trans", False), ("run_hold", {"held": True, "puts": 1}), ("run_ok_puts", 1), ("run_noupload_puts", 2), ("find_root", False), ("manifest_method", 1)):
        o = dict(good_probe)
        o[key] = val
        try:
            check_probe(o)
            raise AssertionError("RED probe arm %s passed" % key)
        except Fail:
            pass
    fc = [{"file": f, "sha256": "ab" * 32, "kind": "k"} for f in (ADAPTER_REL, TEST_REL)]

    def good():
        return {"adapter": {"file": ADAPTER_REL, "functions_added": list(FUNCS), "source_column_values": ["L"], "hash_with_optional": "ab" * 32, "words": "w"},
                "tests": {"file": TEST_REL, "new_tests": 9, "total": 28}, "manifest": {"keys": sorted(MANIFEST_KEYS), "first_data_date": "2026-07-10", "thresholds_claim": "absent", "words": "w"},
                "packaging": {"find_root": True, "source_map_row_needed": True, "words": "w"}, "method_row": {"decision": "NOT_WRITTEN_BY_THIS_ADAPTER", "words": "w"},
                "files_changed": json.loads(json.dumps(fc)), "words": "w", "claim": "measured", "files_in_repo": False, "served_values_changed": False, "pushed": False, "deployed": False}

    def grade(rec, sha="ab" * 32):
        try:
            return check_facts(rec, lambda rel: sha, lambda rel: True)
        except Fail:
            return False
    need(grade(good()) is True, "GREEN facts arm failed")
    for mut, why in ((lambda r: r["tests"].update(new_tests=2), "too few tests"), (lambda r: r["manifest"].update(keys=["table"]), "manifest keys missing"),
                     (lambda r: r["method_row"].update(decision="maybe"), "an unnamed decision"), (lambda r: r.update(deployed=True), "a deploy flag"),
                     (lambda r: r["files_changed"].append({"file": "infra/x.tf", "sha256": "ab" * 32, "kind": "k"}), "a file outside the grant"),
                     (lambda r: r["adapter"].update(functions_added=["run_day"]), "functions missing"), (lambda r: r.update(words="ids 1234567890"), "a digit run")):
        r = json.loads(json.dumps(good()))
        mut(r)
        need(grade(r) is False, "RED: " + why)
    need(grade(good(), sha="cd" * 32) is False, "RED: a hash that differs from the bytes")
    print("selftest OK: 1 green and 11 red probe arms, 1 green and 8 red facts arms")


if __name__ == "__main__":
    try:
        if len(sys.argv) >= 2 and sys.argv[1] == "--selftest":
            selftest(sys.argv[2] if len(sys.argv) > 2 else ".")
            print("selftest PASS")
            sys.exit(0)
        run(sys.argv[1], sys.argv[2])
        print("%s PASS" % sys.argv[2])
    except Fail as e:
        print("FAIL: %s" % e)
        print("%s FAIL" % (sys.argv[2] if len(sys.argv) > 2 else "?"))
        sys.exit(1)
    except Exception as e:
        print("FAIL: %s: %s" % (type(e).__name__, str(e)[:200]))
        print("%s FAIL" % (sys.argv[2] if len(sys.argv) > 2 else "?"))
        sys.exit(1)
