"""IRPT_DASHBD round 127, workstream B-IN (issuer 2.0.0_SA_COO~I2) -- the Scope feed module on contract 0.4.2 (cell DB-i-14).

Contract 0.4.2 landed (~D2 merge 6ac152c83a): return_basis is [TWR, NOT_MEASURABLE] (VENDOR_REPORTED is gone and source_requires
is removed; provenance stays in `source`), and the optional column market_value_eod_claim (measured | inferred) is REQUIRED on a
PRESENT Orion row and null on an ABSENT row. Round 125's module writes VENDOR_REPORTED and keeps the claim in the run record: a
0.4.1 Orion row no longer validates. This round flips the module in the same window (CTO msg 8695, 8706): TWR, the claim in the
table, contract_version read from the file (0.4.2), and the W311-S3 test line. Every case is SYNTHETIC.

The checker reads the contract FILE at HEAD for its version, fields, hash and validator (the 0.4.2 test module's row_problems).

  DBI127-1-AC1  the golden through the wrapper: 17 PRESENT rows (TWR, PRESENT, source orion, the claim measured on the window's
                last day and inferred otherwise) and 11 ABSENT rows in the 0.4.1 shape (claim null), the run record
                (contract_version from the file, no claim_placement key, the claim counts, trading_days_unaccounted 0).
  DBI127-1-AC2  the written parquet: its fields and types hash to the contract's schema_hash_with_optional (the claim is a
                declared column), each row passes the 0.4.2 validator, no absent/ file, no AWS or network import, no typed
                contract version, nothing written outside the output directory.
  DBI127-1-AC3  the repairs still hold (edge-day fixtures read 0 unaccounted, five refusals with a count and nothing written,
                the 299-day chain), an account seen only on a dropped day is still counted (W311-S3), and the adapter and
                wrapper tests run green (at least 30 passed) and name a mutant test.

Usage: python -I <this file> <repo_root> <criterion_id>      prints "<id> PASS" or "<id> FAIL" last
       python -I <this file> --selftest [<repo_root>]
"""
import ast
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
TESTS_REL = ("data/assets/scripts/gold/irpt_reporting/tests/test_inflection_scope_feed_adapter.py",
             "data/assets/scripts/gold/irpt_reporting/tests/test_inflection_scope_feed_run.py")
CONTRACT_REL = "org/standards/IRPT_DASHBD_ACCOUNT_RETURN_DAILY_CONTRACT.json"
CONTRACT_TEST_REL = "data/assets/scripts/gold/irpt_reporting/tests/test_account_return_contract_042.py"
FIRM = "FIRM-SYNTH"
METHOD = 7
TOL = 1e-12
CLAIM = "market_value_eod_claim"
FORBIDDEN_IMPORTS = {"boto3", "botocore", "requests", "urllib", "urllib3", "socket", "http", "ftplib", "smtplib"}
TYPE_NAME = {"string": "string", "double": "double", "int64": "int64"}


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


P124 = _load("p124_run", HERE.parent / "r124" / "p124_run.py")
P123 = P124.P123
silver_of, dim_of = P124.silver_of, P124.dim_of


def contract_of(root):
    return json.loads((Path(root) / CONTRACT_REL).read_bytes().decode("utf-8"))


def declared_fields(contract):
    """[(name, type)] of every declared column and optional column, from the contract file."""
    return [(c["name"], c["type"]) for c in contract["columns"]] + [(o["name"], o["type"]) for o in contract["optional_columns"]]


def read_back(out):
    import pyarrow.parquet as pq
    rows, parts = [], {}
    for d in sorted(Path(out).glob("date=*")):
        t = pq.read_table(str(d / "data.parquet"))
        parts[d.name] = (t.schema, t.to_pylist())
        rows.extend(parts[d.name][1])
    return rows, parts


def run_world(mod, rows, dim_ids, out, trading=None, dim=None):
    return mod.run(silver_of(rows), dim if dim is not None else dim_of(dim_ids), trading or P123.TRADING, FIRM, METHOD, str(out))


def grade_golden(mod, root):
    contract = contract_of(root)
    exp_rows, exp_abs = P123.expected()
    name_to_orion = {v: k for k, v in P123.MAP.items()}
    dim_ids = sorted(P123.MAP)  # 1005 is not in the dimension: unmapped
    with tempfile.TemporaryDirectory() as td:
        out = Path(td) / "out"
        rec = run_world(mod, P123.feed(), dim_ids, out)
        rows, parts = read_back(out)
        need(len(rows) == 28, "expected 28 rows (17 PRESENT + 11 ABSENT, 7 accounts x 4 trading days), got %d" % len(rows))
        got = {}
        for r in rows:
            key = (str(r["source_account_id"]), r["business_date"])
            need(key not in got, "duplicate row for %s" % (key,))
            got[key] = r
        present = {k: r for k, r in got.items() if r["row_status"] == "PRESENT"}
        absent = {k: r for k, r in got.items() if r["row_status"] == "ABSENT"}
        need(len(present) + len(absent) == 28, "a row has a row_status outside PRESENT and ABSENT")
        want = {(name_to_orion[a], d): v for (a, d), v in exp_rows.items()}
        need(set(present) == set(want), "PRESENT keys differ: missing %s extra %s" % (sorted(set(want) - set(present)), sorted(set(present) - set(want))))
        for key, (factor, carried, mv) in want.items():
            r = present[key]
            need(abs(r["total_return_daily"] - (factor - 1.0)) <= TOL and r["carried_days"] == carried and abs(r["market_value_eod"] - mv) <= TOL,
                 "PRESENT row %s differs from the golden" % (key,))
            need(r["return_basis"] == "TWR" and r["source"] == "orion" and r["flow_claim"] == "absent" and r["reason_class"] is None,
                 "PRESENT row %s: return_basis / source / flow_claim / reason_class" % (key,))
            need(r["account_id"] == key[0] and r["source_account_id"] == int(key[0]), "PRESENT row %s account ids" % (key,))
        need({k: v["reason_class"] for k, v in absent.items()} == dict(exp_abs), "ABSENT reason classes differ from the golden")
        for key, r in absent.items():
            unmapped = r["reason_class"] == "UNMAPPED_ACCOUNT"
            need((r["account_id"] is None) == unmapped, "ABSENT row %s: account_id must be null exactly when UNMAPPED_ACCOUNT" % (key,))
            need(unmapped or r["account_id"] == key[0], "ABSENT row %s: a mapped ABSENT row carries the dimension account_id" % (key,))
            need(r["source_account_id"] == int(key[0]), "ABSENT row %s: source_account_id" % (key,))
            need(r["market_value_eod"] is None and r["total_return_daily"] is None and r["external_flow"] is None and r["income_received"] is None,
                 "ABSENT row %s carries a value" % (key,))
            need(r["return_basis"] == "NOT_MEASURABLE" and r["day_quality"] == "NOT_MEASURABLE", "ABSENT row %s: return_basis / day_quality" % (key,))
        # the claim: a declared column of the table on 0.4.2; required on PRESENT, null on ABSENT
        need(CLAIM in {n for n, _t in declared_fields(contract)}, "the contract must declare %s (0.4.2)" % CLAIM)
        n_measured = sum(1 for k in present if k[1] == "2026-07-08")
        counts = {"inferred": len(present) - n_measured, "measured": n_measured}
        need(all(r.get(CLAIM) == ("measured" if k[1] == "2026-07-08" else "inferred") for k, r in present.items()), "claim column on PRESENT rows")
        need(all(r.get(CLAIM) is None for r in absent.values()), "an ABSENT row carries a claim")
        need("claim_placement" not in rec, "claim_placement retires: the claim is a declared column")
        need(rec.get("market_value_eod_claim_counts") == counts, "market_value_eod_claim_counts: got %r want %r" % (rec.get("market_value_eod_claim_counts"), counts))
        # the run record
        need(rec.get("contract_version") == contract["contract_version"], "contract_version must be read from the contract file (%s)" % contract["contract_version"])
        for k, v in (("calendar_days_read", 7), ("calendar_days_incomplete", 0), ("incomplete_days", []), ("rows_present", 17), ("rows_absent", 11),
                     ("partitions_written", 4), ("accounts_in_feed", 7), ("accounts_mapped", 6), ("accounts_unmapped", 1), ("trading_days_unaccounted", 0)):
            need(rec.get(k) == v, "run record %s: got %r want %r" % (k, rec.get(k), v))
        want_by = {}
        for reason in exp_abs.values():
            want_by[reason] = want_by.get(reason, 0) + 1
        need(rec.get("absent_by_reason") == want_by, "run record absent_by_reason")
        for gone in ("absent_placement", "proposed_reason_classes"):
            need(gone not in rec, "run record still carries the retired key %s" % gone)
        need("reason_class_status" not in (rec.get("manifest") or {}), "the manifest still carries reason_class_status (the classes are admitted)")
        need(not (out / "absent").exists(), "the absent/ file must retire: ABSENT rows are in the table")
        on_disk = json.loads((out / "run_record.json").read_bytes().decode("ascii"))
        need(on_disk.get("rows_present") == 17 and on_disk.get("contract_version") == contract["contract_version"], "run_record.json differs from the returned record")


def grade_written(mod, wrap_path, root):
    contract = contract_of(root)
    cmod = _load("contract_042_tests", Path(root) / CONTRACT_TEST_REL)
    dim_ids = sorted(P123.MAP)
    fields = declared_fields(contract)
    with tempfile.TemporaryDirectory() as td:
        out = Path(td) / "out"
        before = set(Path(td).iterdir())
        run_world(mod, P123.feed(), dim_ids, out)
        need(set(Path(td).iterdir()) == before | {out}, "files written outside the output directory")
        rows, parts = read_back(out)
        need(len(rows) == 28, "expected 28 rows")
        for pname, (schema, recs) in parts.items():
            need(all("date=%s" % r["business_date"] == pname for r in recs), "partition %s holds another date" % pname)
            got = sorted("%s:%s" % (f.name, f.type) for f in schema)
            need(got == sorted("%s:%s" % (n, t) for n, t in fields), "partition %s fields differ from the contract's declared fields: %s" % (pname, sorted(set(got) ^ set("%s:%s" % (n, t) for n, t in fields))))
            need(hashlib.sha256("\n".join(got).encode("utf-8")).hexdigest() == contract["schema_hash_with_optional"], "schema hash of %s differs from schema_hash_with_optional" % pname)
        for r in rows:
            probs = cmod.row_problems(contract, r)
            need(not probs, "contract validator on a %s row: %s" % (r["row_status"], probs))
        need(not (out / "absent").exists(), "an absent/ file was written")
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
    need('"0.4.0"' not in src and '"0.4.1"' not in src, "the contract version is typed in the wrapper; it must be read from the contract file")


def refusal(mod, rows, dim, label, td, silver=None):
    out = Path(td) / ("out_" + label)
    before = sorted(str(p) for p in Path(td).rglob("*"))
    try:
        if silver is None:
            run_world(mod, rows, None, out, dim=dim)
        else:
            mod.run(silver, dim, P123.TRADING, FIRM, METHOD, str(out))
    except ValueError as exc:
        need(re.search(r"\d", str(exc)) is not None, "%s: the refusal must carry a count" % label)
    else:
        raise Fail("%s: not refused" % label)
    need(sorted(str(p) for p in Path(td).rglob("*")) == before, "%s: the refused run wrote files" % label)


def grade_repairs(mod, root):
    dim_ids = sorted(P123.MAP)
    # S1: the first calendar day, then the last, is incomplete; no trading day is left unaccounted and the dropped day is listed.
    for label, bad_day in (("first", "2026-07-02"), ("last", "2026-07-08")):
        rows = P123.feed()
        for r in rows:
            if r["account_id"] == "1001" and r["day"] == bad_day:
                r["status"], r["daily_factor"], r["reason_class"] = "ABSENT", None, None
        with tempfile.TemporaryDirectory() as td:
            out = Path(td) / "out"
            rec = run_world(mod, rows, dim_ids, out)
            got, _p = read_back(out)
            need(len(got) == 28, "%s day incomplete: expected 28 rows (7 accounts x 4 trading days), got %d" % (label, len(got)))
            need(rec.get("trading_days_unaccounted") == 0, "%s day incomplete: trading_days_unaccounted must read 0" % label)
            need(rec.get("incomplete_days") == [bad_day] and rec.get("calendar_days_incomplete") == 1, "%s day incomplete: incomplete_days %r" % (label, rec.get("incomplete_days")))
            need(rec.get("accounts_in_feed") == 7, "%s day incomplete: accounts_in_feed %r" % (label, rec.get("accounts_in_feed")))
            on_day = [r for r in got if r["business_date"] == bad_day]
            need(len(on_day) == 7 and all(r["row_status"] == "ABSENT" for r in on_day), "%s day incomplete: every account must read ABSENT on the dropped trading day" % label)
            need(all(r["reason_class"] in ("NO_FEED_ROW", "UNMAPPED_ACCOUNT") for r in on_day), "%s day incomplete: reason must be NO_FEED_ROW or UNMAPPED_ACCOUNT" % label)
    # W311-S3: an account that appears only on a dropped day is still counted in the run record.
    import pandas as pd
    only = [dict(r) for r in P123.feed() if r["account_id"] != "1007"]
    odd = P123.ret("1007", "2026-07-06", 1.001, 700.0, None)
    odd["status"], odd["daily_factor"], odd["reason_class"] = "ABSENT", None, None
    with tempfile.TemporaryDirectory() as td:
        out = Path(td) / "out"
        rec = run_world(mod, only + [odd], dim_ids, out)
        need(rec.get("accounts_in_feed") == 7 and rec.get("accounts_mapped") == 6, "W311-S3: an account seen only on a dropped day must still be counted: %r" % rec.get("accounts_in_feed"))
    # S4, S5, S6 and the repeated key: refused with a count, nothing written.
    good = dim_of(dim_ids)
    with tempfile.TemporaryDirectory() as td:
        dup = pd.DataFrame({"account_id": dim_ids + [dim_ids[0]]})
        refusal(mod, P123.feed(), dup, "dupdim", td)
        noncanon = pd.DataFrame({"account_id": ["0" + dim_ids[0]] + dim_ids[1:]})
        refusal(mod, P123.feed(), noncanon, "noncanon", td)
        silver = silver_of(P123.feed())
        key = sorted(silver)[0]
        silver[key] = silver[key].copy()
        silver[key].loc[silver[key].index[0], "pull_date"] = "2026-01-01"
        refusal(mod, None, good, "partition", td, silver=silver)
        full = Path(td) / "full"
        full.mkdir()
        (full / "stale.txt").write_bytes(b"x")
        before = sorted(str(p) for p in Path(td).rglob("*"))
        try:
            mod.run(silver_of(P123.feed()), good, P123.TRADING, FIRM, METHOD, str(full))
        except ValueError as exc:
            need(re.search(r"\d", str(exc)) is not None, "non-empty out_dir: the refusal must carry a count")
        else:
            raise Fail("a non-empty output directory was not refused")
        need(sorted(str(p) for p in Path(td).rglob("*")) == before, "the refused non-empty run wrote files")
        rows = P123.feed()
        rows.append(dict(rows[0]))
        refusal(mod, rows, good, "repeat", td)
    # the 299-day chain (round 124) still holds on the new shape
    rows, trading, product = P124.chain_world()
    with tempfile.TemporaryDirectory() as td:
        out = Path(td) / "out"
        rec = mod.run(silver_of(rows), dim_of(["2001"]), trading, FIRM, METHOD, str(out))
        got, _p = read_back(out)
        need(len(got) == len(trading) and all(r["row_status"] == "PRESENT" for r in got), "chain: one PRESENT row per trading day")
        chained = 1.0
        for r in sorted(got, key=lambda x: x["business_date"]):
            chained *= 1.0 + r["total_return_daily"]
        need(abs(chained - product) <= TOL, "chained rows differ from the source product by %.3e" % abs(chained - product))
        need(sum(r["carried_days"] for r in got) == 299, "carried_days must sum to the 299-day window")
        need(rec.get("trading_days_unaccounted") == 0, "chain: trading_days_unaccounted")
    # the tests
    root = Path(root)
    total, mutant = 0, False
    for rel in TESTS_REL:
        tf = root / rel
        need(tf.is_file(), "no test file at %s" % rel)
        mutant = mutant or re.search(r"^def test_\w*mutant\w*\(", tf.read_bytes().decode("ascii"), re.M) is not None
        r = subprocess.run([sys.executable, "-I", "-m", "pytest", "-q", "-p", "no:cacheprovider", str(tf)], cwd=str(root), capture_output=True, text=True, timeout=100)
        tail = (r.stdout or "").strip().splitlines()[-1:] or [""]
        need(r.returncode == 0, "pytest rc %s on %s: %s" % (r.returncode, rel, tail[0]))
        m = re.search(r"(\d+) passed", r.stdout or "")
        need(m is not None, "no pass count for %s" % rel)
        total += int(m.group(1))
    need(mutant, "no test file names a mutant test")
    need(total >= 30, "fewer than 30 passed tests across the adapter and wrapper test files: %d" % total)


def selftest(root):
    s = silver_of(P123.feed())
    need(len(s) == 7, "silver_of drifted")
    exp_rows, exp_abs = P123.expected()
    need(len(exp_rows) + len(exp_abs) == 28, "golden size drifted")
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
        if cid == "DBI127-1-AC1":
            grade_golden(mod, root)
        elif cid == "DBI127-1-AC2":
            grade_written(mod, wp, root)
        elif cid == "DBI127-1-AC3":
            grade_repairs(mod, root)
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
