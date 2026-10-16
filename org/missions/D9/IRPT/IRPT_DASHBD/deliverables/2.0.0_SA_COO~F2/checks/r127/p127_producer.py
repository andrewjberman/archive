"""IRPT_DASHBD round 127, workstream F-SHIP ~F2 (issuer 2.0.0_SA_COO~F2) -- FWD-5: the 49 Financial TRANSACTION PRODUCER.

  DB-f-1302 (~1302) `data/assets/scripts/gold/irpt_reporting/account_transaction.py` and its offline tests: it turns one day of the
                    custody transaction silver (fact_trn columns) into `account_transaction` rows by the contract's mapping, and writes
                    them at the builder address. NOT wired into the reporting-gold handler, never run against S3.
                    DBF127-2-AC1 (the tests: names and a clean pytest run), DBF127-2-AC2 (the producer against the contract: schema
                    hash, mapping, and the behaviour on a mapped code, a table-UNMAPPED code and a code the mapping lacks)

Usage: python <this file> <repo_root> <criterion_id>      prints "<id> PASS" or "<id> FAIL" last
       python <this file> --selftest                        the pure helpers on synthetic arms
"""
import hashlib
import importlib.util
import json
import re
import subprocess
import sys
from pathlib import Path

CONTRACT = "org/standards/IRPT_DASHBD_ACCOUNT_TRANSACTION_CONTRACT.json"
PRODUCER = "data/assets/scripts/gold/irpt_reporting/account_transaction.py"
TEST = "data/assets/scripts/gold/irpt_reporting/tests/test_account_transaction.py"
UNMAPPED = "UNMAPPED"
COLUMNS = ("firm", "account_id", "business_date", "trade_date", "settle_date", "action", "txn_type", "symbol", "asset_name", "units",
           "price", "amount", "fee", "custodian", "flow_class", "source_txn_id", "coverage")
NULL_COLUMNS = ("settle_date", "asset_name", "fee", "source_txn_id")
TITLE_WORDS = ("mapping", "unmapped", "new code", "flow", "action", "absent", "schema", "vocabulary")
TYPE_OF = {"string": "string", "date32[day]": "date32[day]", "double": "double"}


class Fail(Exception):
    pass


def need(cond, msg):
    if not cond:
        raise Fail(msg)


def test_names(text):
    return [m.group(1).replace("_", " ") for m in re.finditer(r"^def (test_\w+)", text, re.M)]


def missing_words(names, words):
    low = " | ".join(names).lower()
    return [w for w in words if w not in low]


def pytest_counts(out):
    passed = re.findall(r"(\d+) passed", out)
    failed = re.findall(r"(\d+) failed", out)
    errors = re.findall(r"(\d+) error", out)
    return (int(passed[-1]) if passed else 0), (int(failed[-1]) if failed else 0), (int(errors[-1]) if errors else 0)


def schema_hash_of(fields):
    return hashlib.sha256("\n".join(sorted("%s:%s" % (n, t) for n, t in fields)).encode("ascii")).hexdigest()


def load_module(root):
    p = Path(root) / PRODUCER
    need(p.is_file(), "missing producer " + PRODUCER)
    spec = importlib.util.spec_from_file_location("account_transaction_under_check", p)
    mod = importlib.util.module_from_spec(spec)
    sys.path.insert(0, str(p.parent))
    spec.loader.exec_module(mod)
    return mod


def ac_tests(root):
    p = Path(root) / TEST
    need(p.is_file(), "missing test file " + TEST)
    mw = missing_words(test_names(p.read_text(encoding="utf-8")), TITLE_WORDS)
    need(not mw, "test names lack " + repr(mw))
    run = subprocess.run([sys.executable, "-m", "pytest", TEST, "-q", "-p", "no:cacheprovider"], cwd=str(root), capture_output=True,
                         text=True, timeout=300)
    passed, failed, errors = pytest_counts((run.stdout or "") + (run.stderr or ""))
    need(run.returncode == 0 and failed == 0 and errors == 0, "pytest rc=%s failed=%s errors=%s" % (run.returncode, failed, errors))
    need(passed >= 14, "only %d tests pass (14 required)" % passed)


def smoke_frame(codes):
    import pandas as pd
    rows = []
    for i, code in enumerate(codes):
        rows.append({"account_id": "0000000001", "business_date": "2026-01-05", "trade_date": "2026-01-05", "tran_srcde": code,
                     "tr_cd": "FC", "sb_cd": "FC", "quantity": 10.0 + i, "price": 2.5, "gross_amount": 25.0 + i,
                     "debit_credit": "C", "ticker_symbol": "TEST%d" % i, "cusip": "000000000"})
    return pd.DataFrame(rows)


def ac_binding(root):
    con = json.loads((Path(root) / CONTRACT).read_text(encoding="utf-8"))
    mod = load_module(root)
    fields = [(f.name, str(f.type)) for f in mod.ARROW_SCHEMA]
    need([n for n, _ in fields] == list(COLUMNS), "ARROW_SCHEMA fields are not the contract's columns in order")
    need(schema_hash_of(fields) == con["schema_hash"], "ARROW_SCHEMA hash differs from the contract's schema_hash")
    need(mod.TABLE_TRANSACTION == "account_transaction", "TABLE_TRANSACTION is not account_transaction")
    words = mod.load_words()
    need(words["source_mapping"] == con["source_mapping"] and words["type_action"] == con["type_action"],
         "load_words() differs from the contract's mapping")
    m49 = {m["source_value"]: m for m in con["source_mapping"] if m["firm"] == "49financial"}
    mapped = next(c for c, m in m49.items() if m["opal_type"] != UNMAPPED)
    table_unmapped = next(c for c, m in m49.items() if m["opal_type"] == UNMAPPED)
    unseen = "ZZZZ_NEW_CODE"
    rows = mod.normalize_trn(smoke_frame([mapped, table_unmapped, unseen]), "49financial")
    need(isinstance(rows, list) and len(rows) == 3, "normalize_trn did not return one row per input row")
    for r in rows:
        need(list(r.keys()) == list(COLUMNS), "a row's keys are not the contract's columns in order")
        need(r["firm"] == "49financial" and r["custodian"], "firm or custodian wrong")
        need(all(r[c] is None for c in NULL_COLUMNS), "an absent column carries a value")
    a, b, c = rows
    need(a["txn_type"] == m49[mapped]["opal_type"] and a["flow_class"] == m49[mapped]["flow_class"] and a["coverage"] == "MEASURED"
         and a["action"] == con["type_action"][a["txn_type"]], "the mapped row is wrong")
    need(b["txn_type"] == UNMAPPED and b["coverage"] == "UNMAPPED_BY_TABLE" and b["flow_class"] == m49[table_unmapped]["flow_class"],
         "the table-UNMAPPED row is wrong")
    need(c["txn_type"] == UNMAPPED and c["coverage"] == "CODE_NOT_IN_MAPPING" and c["flow_class"] == "UNRESOLVED"
         and c["action"] is None, "the row for a code the mapping lacks is wrong (it must be counted, never dropped)")
    mod.check_transaction_rows(rows)
    bad = [dict(rows[0], txn_type="Not A Word")]
    try:
        mod.check_transaction_rows(bad)
    except SystemExit:
        return
    raise Fail("check_transaction_rows accepted a word outside the vocabulary")


def selftest():
    bad = 0
    count = 0

    def arm(name, got, want):
        nonlocal bad, count
        count += 1
        if got != want:
            bad += 1
            print("SELFTEST FAIL %s: got %r want %r" % (name, got, want))

    arm("names", test_names("def test_a_b():\n    pass\ndef helper():\n    pass\ndef test_c():\n    pass"), ["test a b", "test c"])
    arm("words-green", missing_words(["x mapping unmapped new code flow action absent schema vocabulary"], TITLE_WORDS), [])
    arm("words-red", missing_words(["only mapping"], TITLE_WORDS), list(TITLE_WORDS[1:]))
    arm("pytest-green", pytest_counts("16 passed in 1.2s"), (16, 0, 0))
    arm("pytest-red", pytest_counts("2 failed, 14 passed in 1s"), (14, 2, 0))
    arm("hash-order", schema_hash_of([("a", "string"), ("b", "double")]) == schema_hash_of([("b", "double"), ("a", "string")]), True)
    arm("columns", len(COLUMNS), 17)
    print("selftest %s" % ("FAIL" if bad else "PASS (%d arms)" % count))
    return 1 if bad else 0


def main(argv):
    if len(argv) == 2 and argv[1] == "--selftest":
        return selftest()
    if len(argv) != 3:
        print(__doc__)
        return 2
    root, ac = argv[1], argv[2]
    table = {"DBF127-2-AC1": ac_tests, "DBF127-2-AC2": ac_binding}
    if ac not in table:
        print("%s FAIL (unknown criterion)" % ac)
        return 1
    try:
        table[ac](root)
    except Fail as e:
        print("reason: %s" % e)
        print("%s FAIL" % ac)
        return 1
    except Exception as e:  # noqa: BLE001
        print("reason: %s: %s" % (type(e).__name__, e))
        print("%s FAIL" % ac)
        return 1
    print("%s PASS" % ac)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
