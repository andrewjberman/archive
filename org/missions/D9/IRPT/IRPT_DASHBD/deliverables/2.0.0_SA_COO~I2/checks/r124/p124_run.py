"""IRPT_DASHBD round 124, workstream B-IN (issuer 2.0.0_SA_COO~I2) -- the Scope feed RUN wrapper (cell DB-i-11).

The wrapper reads feed silver partitions (pandas frames handed to it), applies the complete-day rule and the duplicate-key
refusal, builds the account map from the dimension frame, calls adapt() (round 123) and writes the contract-0.4.0 table as
local parquet partitions plus an ABSENT-records file and a run record. It writes under one output directory and nowhere
else, and it holds no AWS, network or clock code. Every case below is SYNTHETIC: no real account, no client value.

  DBI124-1-AC1  the wrapper golden: the clean world's rows, partitions, ABSENT records and run record; an incomplete
                calendar day is dropped and counted; a repeated (account, day) key is refused with nothing written.
  DBI124-1-AC2  the written parquet: every partition is date=<business_date> and holds only that date; the contract's 22 columns
                and types hash to its schema_hash_with_optional, beside the one proposed column market_value_eod_claim; each row passes ~D2's validator; no AWS / network
                import; nothing is written outside the output directory.
  DBI124-1-AC3  a 299-calendar-day window (inside the 238-to-365 gap round 122 named): the chained rows equal the product
                of the source's daily factors, to 1e-12, and carried_days sums to the window; the worker's own tests run
                green (at least 8 passed) and name a mutant test.

Usage: python -I <this file> <repo_root> <criterion_id>      prints "<id> PASS" or "<id> FAIL" last
       python -I <this file> --selftest [<repo_root>]
"""
import ast
import datetime
import hashlib
import importlib.util
import json
import re
import subprocess
import sys
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
WRAP_REL = "data/assets/scripts/gold/irpt_reporting/adapters/inflection_scope_feed_run.py"
TEST_REL = "data/assets/scripts/gold/irpt_reporting/tests/test_inflection_scope_feed_run.py"
CONTRACT_TEST_REL = "data/assets/scripts/gold/irpt_reporting/tests/test_account_return_contract_040.py"
FIRM = "FIRM-SYNTH"
METHOD = 7
TOL = 1e-12
FEED_COLS = ["pull_date", "day", "account_id", "household_id", "status", "reason_class", "reason_claim", "reason_cause",
             "daily_factor", "start_market_value", "end_market_value", "fee_basis", "fee_basis_note", "calc_gross_of_fees",
             "source", "data_last_updated"]
EXTRA_COLUMN = "market_value_eod_claim"  # proposed, beside the contract's 22 fields, until 0.4.1 admits it (round-123 analysis item 2)
FORBIDDEN_IMPORTS = {"boto3", "botocore", "requests", "urllib", "urllib3", "socket", "http", "ftplib", "smtplib"}


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


P123 = _load("p123_adapter", HERE.parent / "r123" / "p123_adapter.py")


def silver_of(rows):
    """{ 'date=<day>': DataFrame } from adapter-shaped feed rows (one partition per calendar day)."""
    import pandas as pd
    by_day = {}
    for r in rows:
        full = {c: None for c in FEED_COLS}
        full.update(r)
        full["pull_date"] = r["day"]
        full["household_id"] = "H"
        by_day.setdefault(r["day"], []).append(full)
    return {"date=%s" % d: pd.DataFrame(v, columns=FEED_COLS) for d, v in sorted(by_day.items())}


def dim_of(orion_ids):
    import pandas as pd
    return pd.DataFrame({"account_id": [str(i) for i in orion_ids]})


def read_back(out):
    import pyarrow.parquet as pq
    rows, parts = [], {}
    for d in sorted(Path(out).glob("date=*")):
        t = pq.read_table(str(d / "data.parquet"))
        recs = t.to_pylist()
        parts[d.name] = (t.schema, recs)
        rows.extend(recs)
    return rows, parts


def absent_back(out):
    import pyarrow.parquet as pq
    p = Path(out) / "absent" / "data.parquet"
    return pq.read_table(str(p)).to_pylist() if p.is_file() else []


def absent_map(out):
    """{(str(source_account_id), business_date): reason_class}, after checking the 0.4.1 shape of every ABSENT record."""
    got = {}
    for a in absent_back(out):
        need(a.get("row_status") == "ABSENT", "an ABSENT record carries row_status %r" % a.get("row_status"))
        need(a.get("source_account_id") is not None, "an ABSENT record has no source_account_id")
        if a["reason_class"] == "UNMAPPED_ACCOUNT":
            need(a.get("account_id") is None, "an UNMAPPED_ACCOUNT record must have account_id null")
        else:
            need(a.get("account_id") == str(a["source_account_id"]), "a mapped ABSENT record must carry the dimension account_id")
        got[(str(a["source_account_id"]), a["business_date"])] = a["reason_class"]
    return got


def run_world(mod, rows, dim_ids, out, trading=None):
    return mod.run(silver_of(rows), dim_of(dim_ids), trading or P123.TRADING, FIRM, METHOD, str(out))


def grade_golden(mod):
    exp_rows, exp_abs = P123.expected()
    name_to_orion = {v: k for k, v in P123.MAP.items()}
    dim_ids = sorted(P123.MAP)  # 1005 is not in the dimension: unmapped
    with tempfile.TemporaryDirectory() as td:
        out = Path(td) / "out"
        rec = run_world(mod, P123.feed(), dim_ids, out)
        got_rows, parts = read_back(out)
        got = {(r["account_id"], r["business_date"]): r for r in got_rows}
        want = {(name_to_orion[a], d): v for (a, d), v in exp_rows.items()}
        need(set(got) == set(want), "row keys differ: missing %s extra %s" % (sorted(set(want) - set(got)), sorted(set(got) - set(want))))
        for key, (factor, carried, mv) in want.items():
            r = got[key]
            need(abs(r["total_return_daily"] - (factor - 1.0)) <= TOL and r["carried_days"] == carried and abs(r["market_value_eod"] - mv) <= TOL,
                 "row %s differs from the golden" % (key,))
            need(r["source_account_id"] == int(key[0]) and r["source"] == "orion" and r["flow_claim"] == "absent", "row %s source columns" % (key,))
            claim = "measured" if key[1] == "2026-07-08" else "inferred"
            need(r.get("market_value_eod_claim") == claim, "row %s market_value_eod_claim: got %r want %r" % (key, r.get("market_value_eod_claim"), claim))
        need(set(parts) == {"date=%s" % d for (_a, d) in want}, "partition names differ: %s" % sorted(parts))
        ab = absent_map(out)
        need(ab == dict(exp_abs), "ABSENT records differ from the golden")
        need(isinstance(rec, dict), "run() must return the run record dict")
        for k, v in (("calendar_days_read", 7), ("calendar_days_incomplete", 0), ("rows", 17), ("accounts_in_feed", 7), ("accounts_mapped", 6),
                     ("accounts_unmapped", 1), ("partitions_written", 4)):
            need(rec.get(k) == v, "run record %s: got %r want %r" % (k, rec.get(k), v))
        want_by = {}
        for r in exp_abs.values():
            want_by[r] = want_by.get(r, 0) + 1
        need(rec.get("absent_by_reason") == want_by, "run record absent_by_reason")
        need(rec.get("contract_version") == "0.4.0" and rec.get("absent_placement") == "BESIDE_TABLE", "run record must say which contract and where ABSENT sits (0.4.1 has not landed)")
        stat = (rec.get("manifest") or {}).get("reason_class_status")
        need(stat == {"NO_FEED_ROW": "proposed", "INCOMPLETE_WINDOW": "proposed", "NO_EOD_VALUE": "proposed"}, "manifest reason_class_status: got %r" % (stat,))
        proposed = sorted(set(want_by) & {"NO_FEED_ROW", "INCOMPLETE_WINDOW", "NO_EOD_VALUE"})
        need(rec.get("proposed_reason_classes") == proposed, "run record proposed_reason_classes: got %r want %r" % (rec.get("proposed_reason_classes"), proposed))
        on_disk = json.loads((out / "run_record.json").read_bytes().decode("ascii"))
        need(on_disk.get("rows") == 17 and on_disk.get("calendar_days_read") == 7, "run_record.json differs from the returned record")
    # the complete-day rule: one row of one calendar day is ABSENT with no reason class -> the whole day is dropped and counted.
    rows = P123.feed()
    for r in rows:
        if r["account_id"] == "1001" and r["day"] == "2026-07-07":
            r["status"], r["daily_factor"], r["reason_class"] = "ABSENT", None, None
    with tempfile.TemporaryDirectory() as td:
        out = Path(td) / "out"
        rec = run_world(mod, rows, dim_ids, out)
        got_rows, _p = read_back(out)
        need(rec.get("calendar_days_incomplete") == 1 and rec.get("calendar_days_read") == 7, "incomplete day not counted: %r" % rec.get("calendar_days_incomplete"))
        need(not any(r["business_date"] == "2026-07-07" for r in got_rows), "a row was written for the incomplete day")
        ab = absent_map(out)
        need(all(ab.get((a, "2026-07-07")) in ("NO_FEED_ROW", "UNMAPPED_ACCOUNT") for a in ("1001", "1002", "1003", "1004", "1005", "1006", "1007")),
             "the incomplete day must be ABSENT NO_FEED_ROW (or UNMAPPED_ACCOUNT) for every account")
    # a repeated (account, day) key is refused and nothing is written.
    rows = P123.feed()
    rows.append(dict(rows[0]))
    with tempfile.TemporaryDirectory() as td:
        out = Path(td) / "out"
        try:
            run_world(mod, rows, dim_ids, out)
        except ValueError as exc:
            need(re.search(r"\b1\b", str(exc)) is not None, "the refusal must carry the count of repeated keys (1)")
        else:
            raise Fail("a repeated (account, day) key was not refused")
        need(not out.exists() or not any(out.rglob("*.parquet")), "the refused run wrote files")


def grade_written(mod, wrap_path, contract_mod):
    contract = contract_mod.CONTRACT
    dim_ids = sorted(P123.MAP)
    with tempfile.TemporaryDirectory() as td:
        out = Path(td) / "out"
        before = set(Path(td).iterdir())
        run_world(mod, P123.feed(), dim_ids, out)
        need(set(Path(td).iterdir()) == before | {out}, "files written outside the output directory")
        rows, parts = read_back(out)
        need(len(rows) == 17, "expected 17 rows")
        want_cols = {c["name"] for c in contract["columns"]} | {o["name"] for o in contract["optional_columns"]}
        for pname, (schema, recs) in parts.items():
            need(all("date=%s" % r["business_date"] == pname for r in recs), "partition %s holds another date" % pname)
            need({f.name for f in schema} == want_cols | {EXTRA_COLUMN}, "partition %s columns differ from the contract plus %s" % (pname, EXTRA_COLUMN))
            need(str(schema.field(EXTRA_COLUMN).type) == "string", "%s must be a string" % EXTRA_COLUMN)
            lines = sorted("%s:%s" % (f.name, f.type) for f in schema if f.name != EXTRA_COLUMN)
            need(hashlib.sha256("\n".join(lines).encode("utf-8")).hexdigest() == contract["schema_hash_with_optional"], "schema hash of %s differs from schema_hash_with_optional" % pname)
        for r in rows:
            probs = contract_mod.row_problems(contract, r)
            need(not probs, "contract validator: %s" % probs)
    tree = ast.parse(Path(wrap_path).read_bytes().decode("ascii"))
    names = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            names |= {a.name.split(".")[0] for a in node.names}
        elif isinstance(node, ast.ImportFrom) and node.module:
            names.add(node.module.split(".")[0])
    need(not (names & FORBIDDEN_IMPORTS), "forbidden import(s): %s" % sorted(names & FORBIDDEN_IMPORTS))
    src = Path(wrap_path).read_bytes().decode("ascii")
    need("s3://" not in src and "boto3" not in src, "the wrapper names an s3 address or boto3")


def chain_world():
    """A single account, 299 calendar days from a Monday: every weekday trades, the window ends on a Friday."""
    start = datetime.date(2026, 1, 5)  # a Monday (synthetic)
    days = [start + datetime.timedelta(days=i) for i in range(299)]
    need(days[0].weekday() == 0 and days[-1].weekday() == 4, "fixture must run Monday to Friday")
    need(238 <= len(days) <= 365, "fixture window must sit inside 238 to 365 days")
    rows, product, v = [], 1.0, 1000.0
    for i, d in enumerate(days):
        f = 1.0 + (((i * 7) % 11) - 5) * 0.0004
        rows.append(P123.ret("2001", d.isoformat(), f, v, None))
        product *= f
        v *= f
    rows[-1]["end_market_value"] = v
    trading = [d.isoformat() for d in days if d.weekday() < 5]
    return rows, trading, product


def grade_chain(mod, root):
    rows, trading, product = chain_world()
    with tempfile.TemporaryDirectory() as td:
        out = Path(td) / "out"
        rec = mod.run(silver_of(rows), dim_of(["2001"]), trading, FIRM, METHOD, str(out))
        got, _p = read_back(out)
        need(len(got) == len(trading), "expected one row per trading day (%d), got %d" % (len(trading), len(got)))
        chained = 1.0
        for r in sorted(got, key=lambda x: x["business_date"]):
            chained *= 1.0 + r["total_return_daily"]
        need(abs(chained - product) <= TOL, "chained rows differ from the source product by %.3e" % abs(chained - product))
        need(sum(r["carried_days"] for r in got) == 299, "carried_days must sum to the 299-day window")
        need(rec.get("rows") == len(trading), "run record rows")
    tf = root / TEST_REL
    need(tf.is_file(), "no test file at %s" % TEST_REL)
    src = tf.read_bytes().decode("ascii")
    need(re.search(r"^def test_\w*mutant\w*\(", src, re.M) is not None, "the test file names no mutant test")
    r = subprocess.run([sys.executable, "-I", "-m", "pytest", "-q", "-p", "no:cacheprovider", str(tf)], cwd=str(root), capture_output=True, text=True, timeout=100)
    tail = (r.stdout or "").strip().splitlines()[-1:] or [""]
    need(r.returncode == 0, "pytest rc %s: %s" % (r.returncode, tail[0]))
    m = re.search(r"(\d+) passed", r.stdout or "")
    need(m is not None and int(m.group(1)) >= 8, "fewer than 8 passed tests: %s" % tail[0])


def selftest(root):
    rows, trading, product = chain_world()
    need(len(rows) == 299 and len(trading) == 215, "chain fixture drifted: %d days %d trading" % (len(rows), len(trading)))
    s = silver_of(P123.feed())
    need(len(s) == 7 and all(list(df.columns) == FEED_COLS for df in s.values()), "silver_of drifted")
    print("selftest PASS")


def main(argv):
    if len(argv) >= 2 and argv[1] == "--selftest":
        selftest(Path(argv[2]) if len(argv) > 2 else Path("."))
        return 0
    root, cid = Path(argv[1]).resolve(), argv[2]
    try:
        wp = root / WRAP_REL
        need(wp.is_file(), "no wrapper at %s" % WRAP_REL)
        mod = _load("scope_feed_run_under_test", wp)
        need(hasattr(mod, "run"), "the wrapper has no run()")
        if cid == "DBI124-1-AC1":
            grade_golden(mod)
        elif cid == "DBI124-1-AC2":
            grade_written(mod, wp, _load("contract_040_tests", root / CONTRACT_TEST_REL))
        elif cid == "DBI124-1-AC3":
            grade_chain(mod, root)
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
