"""IRPT_DASHBD round 132, workstream B-49F (issuer 2.0.0_SA_COO~D2) -- DB-b-264, the VALUE-LEVEL READ of the one landed Cottonwood day 2026-07-10 (CTO ROUND-128 ANALYSIS @cbd0289ecd, msg 8462).
The landing function runs on the layer's pyarrow 14.0.2; the issuer's reference measurement ran on pyarrow 25.0.1, so equality of bytes or of a hash against a 25.0.1 reference proves nothing either
way. The grade reads ONE landed day at the VALUE level against a locally derived reference: the row count, the key set (account_id, business_date) and every float value equal within 1e-12,
every other column exactly equal; and it proves the LANDED file loads under pyarrow 14.0.2 itself (the consumer's pyarrow), by reading it with a 14.0.2 interpreter. READ ONLY: GET and LIST of
the gold and the silver, local files; no write of any kind to AWS.

  the issuer (a LOCAL read, direct act)   the record RD_COT_VALUE_READ_R132.json (a private reference parquet and a private 14.0.2 environment stay outside the repo)
                    DB132-1-AC1 (the record: the comparison's form and verdicts),
                    DB132-1-AC2 (FRESH: the checker re-derives the reference, re-reads the landed file and loads it under the recorded 14.0.2 interpreter; every recorded number equals its own)

Usage: python <this file> <repo_root> <criterion_id>      prints "<id> PASS" or "<id> FAIL" last
       python <this file> --selftest                       the record clauses on synthetic arms
"""
import json
import re
import subprocess
import sys
from pathlib import Path

D = "org/missions/D9/IRPT/IRPT_DASHBD/deliverables/"
REC_REL = D + "2.0.0_SA_COO~D2/RD_COT_VALUE_READ_R132.json"
DAY = "2026-07-10"
TOL = 1e-12
LANDED_PYARROW = "14.0.2"
LONG_DIGITS = re.compile(r"\d{8,}")
DIGIT_OK_KEYS = ("keys_sha256", "venv_python", "created_by", "pyarrow_version")


class Fail(Exception):
    pass


def need(cond, msg):
    if not cond:
        raise Fail(msg)


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


# ------------------------------------------------------------------------------------------------ the record clauses (pure)
def check_record(rec):
    exp = {"day", "landed", "reference", "compare", "loader_read", "words"}
    need(isinstance(rec, dict) and set(rec) == exp, "record keys differ: %s" % (sorted(set(rec) ^ exp) if isinstance(rec, dict) else "?"))
    need(rec["day"] == DAY, "day must be %s" % DAY)
    lan, ref, cmp_, ld = rec["landed"], rec["reference"], rec["compare"], rec["loader_read"]
    need(isinstance(lan, dict) and set(lan) == {"rows", "columns", "keys_sha256", "created_by"} and is_int(lan["rows"]) and lan["rows"] > 0, "landed form")
    need(LANDED_PYARROW in str(lan["created_by"]), "the landed file must be written by pyarrow %s (created_by %s)" % (LANDED_PYARROW, lan["created_by"]))
    need(isinstance(ref, dict) and set(ref) == {"rows", "columns", "keys_sha256", "pyarrow_version"} and is_int(ref["rows"]) and ref["rows"] > 0, "reference form")
    need(str(ref["pyarrow_version"]) != LANDED_PYARROW and re.fullmatch(r"\d+\.\d+\.\d+", str(ref["pyarrow_version"])), "the reference must be derived under a DIFFERENT pyarrow than %s (read %s)" % (LANDED_PYARROW, ref["pyarrow_version"]))
    need(isinstance(cmp_, dict) and set(cmp_) == {"rows_equal", "columns_equal", "key_set_equal", "float_columns", "values_compared", "max_abs_diff", "non_float_mismatches"}, "compare form")
    need(cmp_["rows_equal"] is True and lan["rows"] == ref["rows"], "row counts differ: landed %s reference %s" % (lan["rows"], ref["rows"]))
    need(cmp_["columns_equal"] is True and lan["columns"] == ref["columns"], "columns differ")
    need(cmp_["key_set_equal"] is True and lan["keys_sha256"] == ref["keys_sha256"], "key sets differ")
    need(isinstance(cmp_["float_columns"], list) and cmp_["float_columns"] and is_int(cmp_["values_compared"]) and cmp_["values_compared"] > 0, "no float value was compared")
    need(isinstance(cmp_["max_abs_diff"], (int, float)) and 0 <= cmp_["max_abs_diff"] <= TOL, "max_abs_diff %s exceeds %s" % (cmp_["max_abs_diff"], TOL))
    need(cmp_["non_float_mismatches"] == 0, "non-float columns differ in %s cells" % cmp_["non_float_mismatches"])
    need(isinstance(ld, dict) and set(ld) == {"venv_python", "pyarrow_version", "rows", "keys_sha256"}, "loader_read form")
    need(ld["pyarrow_version"] == LANDED_PYARROW and ld["rows"] == lan["rows"] and ld["keys_sha256"] == lan["keys_sha256"], "the 14.0.2 load differs from the landed file")
    need(isinstance(rec["words"], str) and 80 <= len(rec["words"]) <= 1800, "words must be one paragraph of 80 to 1800 characters")
    need(not digit_runs(rec), "a run of 8 or more digits outside the exempt fields: %s" % digit_runs(rec)[:2])
    return True


def compare_recount(rec, fresh):
    """fresh: the checker's own numbers; every recorded number must equal them."""
    for k in ("rows", "columns", "keys_sha256"):
        need(rec["landed"][k] == fresh["landed"][k], "landed %s differs from the checker's re-read" % k)
        need(rec["reference"][k] == fresh["reference"][k], "reference %s differs from the checker's re-derivation" % k)
    c = rec["compare"]
    need(c["values_compared"] == fresh["values_compared"] and c["float_columns"] == fresh["float_columns"], "values_compared or float_columns differ")
    need(abs(c["max_abs_diff"] - fresh["max_abs_diff"]) <= 1e-15 and c["non_float_mismatches"] == fresh["non_float_mismatches"], "max_abs_diff or the non-float mismatches differ")
    need(fresh["max_abs_diff"] <= TOL and fresh["non_float_mismatches"] == 0 and fresh["key_set_equal"] and fresh["rows_equal"], "the checker's own comparison fails")
    ld = fresh["loader"]
    need(ld["pyarrow_version"] == LANDED_PYARROW and ld["rows"] == rec["loader_read"]["rows"] and ld["keys_sha256"] == rec["loader_read"]["keys_sha256"], "the 14.0.2 interpreter's own load differs from the record")
    return True


# ------------------------------------------------------------------------------------------------ the fresh recount
CHILD = r'''
import datetime as dt, hashlib, io, json, sys
root, day, loader_py = sys.argv[1], sys.argv[2], sys.argv[3]
sys.path.insert(0, root + "/lib"); sys.path.insert(0, root + "/data/assets/scripts/gold/irpt_reporting/adapters")
import boto3, pyarrow as pa, pyarrow.parquet as pq, subprocess, tempfile, os
import trading_calendar as tc
import opal_naming
import cottonwood_bd_account_return_daily as cbd
reader = cbd.CottonwoodBlackDiamondSilverReader()
prev = tc.prev_trading_day(dt.date.fromisoformat(day)).isoformat()
rows, _s = cbd.derive(reader, cbd.accounts_in_partition(reader, day), prev, day)
rows = [r for r in rows if r["business_date"] == day]
ref = cbd.to_table(rows, with_source=True)
uri = opal_naming.address("irpt", "cottonwood", "gold", "account_return_daily", "date=" + day, "data.parquet")
b, k = uri[len("s3://"):].split("/", 1)
raw = boto3.client("s3").get_object(Bucket=b, Key=k)["Body"].read()
landed = pq.read_table(io.BytesIO(raw))
created_by = pq.read_metadata(io.BytesIO(raw)).created_by
def keys(t): return sorted("%s|%s" % (a, d) for a, d in zip(t["account_id"].to_pylist(), t["business_date"].to_pylist()))
def sha(t): return hashlib.sha256("\n".join(keys(t)).encode("utf-8")).hexdigest()
def aligned(t):
    idx = sorted(range(t.num_rows), key=lambda i: (t["account_id"][i].as_py(), str(t["business_date"][i].as_py())))
    return t.take(pa.array(idx))
lt, rt = aligned(landed), aligned(ref)
floats = [f.name for f in landed.schema if pa.types.is_floating(f.type)]
maxd, n, nonf = 0.0, 0, 0
if landed.schema.names == ref.schema.names and lt.num_rows == rt.num_rows:
    for name in landed.schema.names:
        a, c = lt[name].to_pylist(), rt[name].to_pylist()
        if name in floats:
            for x, y in zip(a, c):
                if x is None and y is None: continue
                if x is None or y is None: nonf += 1; continue
                n += 1; maxd = max(maxd, abs(x - y))
        else:
            nonf += sum(1 for x, y in zip(a, c) if x != y)
with tempfile.TemporaryDirectory() as td:
    p = os.path.join(td, "landed.parquet"); open(p, "wb").write(raw)
    code = ("import pyarrow as pa, pyarrow.parquet as pq, hashlib, json, sys\n"
            "t = pq.read_table(sys.argv[1])\n"
            "ks = sorted('%s|%s' % (a, d) for a, d in zip(t['account_id'].to_pylist(), t['business_date'].to_pylist()))\n"
            "print(json.dumps({'pyarrow_version': pa.__version__, 'rows': t.num_rows, 'keys_sha256': hashlib.sha256('\\n'.join(ks).encode('utf-8')).hexdigest()}))\n")
    r = subprocess.run([loader_py, "-c", code, p], capture_output=True, text=True)
    loader = json.loads(r.stdout.strip().splitlines()[-1]) if r.returncode == 0 and r.stdout.strip() else {"pyarrow_version": None, "rows": None, "keys_sha256": None, "error": r.stderr[-300:]}
print(json.dumps({"landed": {"rows": landed.num_rows, "columns": landed.schema.names, "keys_sha256": sha(landed), "created_by": created_by},
                  "reference": {"rows": ref.num_rows, "columns": ref.schema.names, "keys_sha256": sha(ref), "pyarrow_version": pa.__version__},
                  "rows_equal": landed.num_rows == ref.num_rows, "key_set_equal": sha(landed) == sha(ref), "float_columns": floats, "values_compared": n,
                  "max_abs_diff": maxd, "non_float_mismatches": nonf, "loader": loader}))
'''


def fresh(root, loader_py):
    r = subprocess.run([sys.executable, "-c", CHILD, str(Path(root).resolve()).replace("\\", "/"), DAY, loader_py], capture_output=True, text=True, timeout=900)
    need(r.returncode == 0, "the re-derivation died (rc %s): %s" % (r.returncode, (r.stderr or r.stdout)[-400:].replace("\n", " | ")))
    return json.loads([ln for ln in r.stdout.splitlines() if ln.startswith("{")][-1])


def run(root, cid):
    root = Path(root)
    rec = json.loads((root / REC_REL).read_text(encoding="utf-8"))
    check_record(rec)
    if cid == "DB132-1-AC1":
        c = rec["compare"]
        print("OK: record: %d rows, key set equal, %d float values over %d columns equal within %g (max diff %g), %d non-float mismatches; the landed file was written by pyarrow %s and loads under %s" %
              (rec["landed"]["rows"], c["values_compared"], len(c["float_columns"]), TOL, c["max_abs_diff"], c["non_float_mismatches"], LANDED_PYARROW, rec["loader_read"]["pyarrow_version"]))
        return True
    if cid == "DB132-1-AC2":
        lp = rec["loader_read"]["venv_python"]
        need(Path(lp).is_file(), "the recorded 14.0.2 interpreter is absent: %s" % lp)
        f = fresh(root, lp)
        compare_recount(rec, {"landed": f["landed"], "reference": f["reference"], "values_compared": f["values_compared"], "float_columns": f["float_columns"], "max_abs_diff": f["max_abs_diff"],
                              "non_float_mismatches": f["non_float_mismatches"], "key_set_equal": f["key_set_equal"], "rows_equal": f["rows_equal"], "loader": f["loader"]})
        print("OK: fresh: the landed file (pyarrow %s) re-read, the reference re-derived under pyarrow %s, %d float values equal within %g (max diff %g), the 14.0.2 interpreter loads %d rows with the same key set" %
              (LANDED_PYARROW, f["reference"]["pyarrow_version"], f["values_compared"], TOL, f["max_abs_diff"], f["loader"]["rows"]))
        return True
    raise Fail("unknown criterion %s" % cid)


def selftest():
    import copy

    def red(fn, label):
        try:
            fn()
        except Fail:
            return
        raise AssertionError("red arm passed: " + label)
    sha = "ab" * 32
    cols = ["account_id", "business_date", "total_return_daily"]
    good = {"day": DAY, "landed": {"rows": 10, "columns": cols, "keys_sha256": sha, "created_by": "parquet-cpp-arrow version 14.0.2"},
            "reference": {"rows": 10, "columns": cols, "keys_sha256": sha, "pyarrow_version": "25.0.1"},
            "compare": {"rows_equal": True, "columns_equal": True, "key_set_equal": True, "float_columns": ["total_return_daily"], "values_compared": 10, "max_abs_diff": 0.0, "non_float_mismatches": 0},
            "loader_read": {"venv_python": "C:/x/python.exe", "pyarrow_version": "14.0.2", "rows": 10, "keys_sha256": sha}, "words": "w" * 120}
    assert check_record(copy.deepcopy(good))
    arms = (("day", lambda r: r.update(day="2026-07-13")), ("rows", lambda r: r["reference"].update(rows=11)), ("columns", lambda r: r["reference"].update(columns=["x"])),
            ("keys", lambda r: r["reference"].update(keys_sha256="cd" * 32)), ("same pyarrow", lambda r: r["reference"].update(pyarrow_version="14.0.2")),
            ("landed writer", lambda r: r["landed"].update(created_by="parquet-cpp-arrow version 25.0.1")), ("rows flag", lambda r: r["compare"].update(rows_equal=False)),
            ("key flag", lambda r: r["compare"].update(key_set_equal=False)), ("nothing compared", lambda r: r["compare"].update(values_compared=0)),
            ("no float columns", lambda r: r["compare"].update(float_columns=[])), ("diff", lambda r: r["compare"].update(max_abs_diff=1e-9)),
            ("non float", lambda r: r["compare"].update(non_float_mismatches=2)), ("loader version", lambda r: r["loader_read"].update(pyarrow_version="25.0.1")),
            ("loader rows", lambda r: r["loader_read"].update(rows=9)), ("loader keys", lambda r: r["loader_read"].update(keys_sha256="cd" * 32)),
            ("words", lambda r: r.update(words="short")), ("extra key", lambda r: r.update(z=1)), ("digits", lambda r: r.update(words="w" * 100 + " 123456789")))
    for label, fn in arms:
        r = copy.deepcopy(good)
        fn(r)
        red(lambda: check_record(r), label)
    fresh_ok = {"landed": good["landed"], "reference": good["reference"], "values_compared": 10, "float_columns": ["total_return_daily"], "max_abs_diff": 0.0, "non_float_mismatches": 0,
                "key_set_equal": True, "rows_equal": True, "loader": {"pyarrow_version": "14.0.2", "rows": 10, "keys_sha256": sha}}
    assert compare_recount(good, copy.deepcopy(fresh_ok))
    for label, fn in (("landed rows", lambda f: f["landed"].update(rows=11)), ("reference keys", lambda f: f["reference"].update(keys_sha256="cd" * 32)),
                      ("values", lambda f: f.update(values_compared=9)), ("diff", lambda f: f.update(max_abs_diff=1e-9)), ("loader", lambda f: f["loader"].update(rows=9)),
                      ("fresh fails", lambda f: f.update(non_float_mismatches=1))):
        f2 = copy.deepcopy(fresh_ok)
        fn(f2)
        red(lambda: compare_recount(good, f2), label)
    print("selftest: record (%d red arms) and recount (6 red arms) clauses behave" % len(arms))
    print("selftest PASS")


if __name__ == "__main__":
    if sys.argv[1:2] == ["--selftest"]:
        selftest()
        sys.exit(0)
    try:
        run(sys.argv[1], sys.argv[2])
        print(sys.argv[2] + " PASS")
    except Exception as e:  # a failed read or recount is a FAIL, not a traceback
        print("FAIL: " + str(e))
        print(sys.argv[2] + " FAIL")
        sys.exit(1)
