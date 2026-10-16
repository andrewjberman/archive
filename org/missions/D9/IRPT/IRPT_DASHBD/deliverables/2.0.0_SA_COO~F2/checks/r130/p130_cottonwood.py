"""IRPT_DASHBD round 130, workstream F-SHIP ~F2 (issuer 2.0.0_SA_COO~F2) -- FWD-5: the COTTONWOOD TRANSACTION PRODUCER.

  DB-f-1601 (~1601) `data/assets/scripts/gold/irpt_reporting/account_transaction_cottonwood.py` and its offline tests: one day of Cottonwood's
                    Black Diamond transaction silver (fact_transactions columns) to `account_transaction` rows by the contract 0.3.0's
                    cottonwood_mapping (the type word on the (Transaction Type, Transaction Sub Type) pair, the action word from the vendor's
                    Action, the flow class from the External Flow column, the fee as the stated sum, the identifier, the stated transforms).
                    Not wired, never run by a test against S3.  The 49 Financial producer gains the stated custodian lower-casing.
                    DBF130-1-AC3 (the tests of both producers and the producer against the contract)

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
CW = "data/assets/scripts/gold/irpt_reporting/account_transaction_cottonwood.py"
CW_TEST = "data/assets/scripts/gold/irpt_reporting/tests/test_account_transaction_cottonwood.py"
F49 = "data/assets/scripts/gold/irpt_reporting/account_transaction.py"
F49_TEST = "data/assets/scripts/gold/irpt_reporting/tests/test_account_transaction.py"
UNMAPPED = "UNMAPPED"
COLUMNS = ("firm", "account_id", "business_date", "trade_date", "settle_date", "action", "txn_type", "symbol", "asset_name", "units",
           "price", "amount", "fee", "custodian", "flow_class", "source_txn_id", "coverage")
TITLE_WORDS = ("pair", "action", "flow", "fee", "settle", "identifier", "custodian", "external", "schema", "unmapped", "new code", "vocabulary")


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
    p = re.findall(r"(\d+) passed", out)
    f = re.findall(r"(\d+) failed", out)
    e = re.findall(r"(\d+) error", out)
    return (int(p[-1]) if p else 0), (int(f[-1]) if f else 0), (int(e[-1]) if e else 0)


def schema_hash_of(fields):
    return hashlib.sha256("\n".join(sorted("%s:%s" % (n, t) for n, t in fields)).encode("ascii")).hexdigest()


def load_module(root, rel, name):
    p = Path(root) / rel
    need(p.is_file(), "missing " + rel)
    spec = importlib.util.spec_from_file_location(name, p)
    mod = importlib.util.module_from_spec(spec)
    sys.path.insert(0, str(p.parent))
    spec.loader.exec_module(mod)
    return mod


def run_pytest(root, rel, minimum):
    run = subprocess.run([sys.executable, "-m", "pytest", rel, "-q", "-p", "no:cacheprovider"], cwd=str(root), capture_output=True,
                         text=True, timeout=400)
    passed, failed, errors = pytest_counts((run.stdout or "") + (run.stderr or ""))
    need(run.returncode == 0 and failed == 0 and errors == 0, "pytest %s rc=%s failed=%s errors=%s" % (rel, run.returncode, failed, errors))
    need(passed >= minimum, "%s: only %d tests pass (%d required)" % (rel, passed, minimum))


def cw_frame(rows):
    import pandas as pd
    return pd.DataFrame(rows)


def base_row(**k):
    row = {"AccountID": "00000000001", "Trade Date": "2026-03-10", "Settle Date": "2026-03-12", "Return Date": "2026-03-10",
           "Transaction Type": "T", "Transaction Sub Type": "S", "Action": "A", "External Flow": "None", "Units": 4.0, "Price": 2.5,
           "Market Value": 10.0, "Transaction Fee": 1.0, "Account Fee": 0.5, "Symbol": "TEST", "Asset Name": "Test Asset",
           "Custodian": "  Some Custodian ", "TransactionID": " TID-1 "}
    row.update(k)
    return row


def ac_all(root):
    con = json.loads((Path(root) / CONTRACT).read_text(encoding="utf-8"))
    names = test_names((Path(root) / CW_TEST).read_text(encoding="utf-8")) if (Path(root) / CW_TEST).is_file() else []
    need(names, "missing test file " + CW_TEST)
    mw = missing_words(names, TITLE_WORDS)
    need(not mw, "Cottonwood test names lack " + repr(mw))
    run_pytest(root, CW_TEST, 20)
    run_pytest(root, F49_TEST, 38)
    mod = load_module(root, CW, "account_transaction_cottonwood_under_check")
    fields = [(f.name, str(f.type)) for f in mod.ARROW_SCHEMA]
    need([n for n, _ in fields] == list(COLUMNS) and schema_hash_of(fields) == con["schema_hash"], "ARROW_SCHEMA is not the contract's (names, order, hash)")
    cm = con["cottonwood_mapping"]
    pairs = {r["source_value"]: r for r in cm["type_pairs"]}
    actions = {r["source_value"]: r for r in cm["actions"]}
    none_pair = next(k for k, r in pairs.items() if r["opal_type"] != UNMAPPED and r["flow_class_none"] is not None)
    t, st = none_pair.split(" | ")
    act = next(k for k, r in actions.items() if r["opal_action"] != UNMAPPED)
    rows = mod.normalize_trn(cw_frame([
        base_row(**{"Transaction Type": t, "Transaction Sub Type": st, "Action": act}),
        base_row(**{"Transaction Type": t, "Transaction Sub Type": st, "Action": act, "External Flow": "Contribution"}),
        base_row(**{"Transaction Type": t, "Transaction Sub Type": st, "Action": act, "External Flow": "Withdrawal"}),
        base_row(**{"Transaction Type": t, "Transaction Sub Type": st, "Action": None, "Symbol": "  ", "TransactionID": ""}),
        base_row(**{"Transaction Type": "ZZ_NEW", "Transaction Sub Type": "ZZ_NEW", "Action": act}),
    ]), "cottonwood")
    need(isinstance(rows, list) and len(rows) == 5, "normalize_trn did not return one row per input row")
    for r in rows:
        need(list(r.keys()) == list(COLUMNS), "a row's keys are not the contract's columns in order")
        need(r["firm"] == "cottonwood" and r["custodian"] == "some custodian", "firm or the lower-cased, stripped custodian is wrong")
        need(str(r["settle_date"]) == "2026-03-12" and r["fee"] == 1.5, "settle_date or the stated fee sum is wrong")
    a, b, c, d, e = rows
    need(a["txn_type"] == pairs[none_pair]["opal_type"] and a["flow_class"] == pairs[none_pair]["flow_class_none"]
         and a["coverage"] == "MEASURED" and a["action"] == actions[act]["opal_action"], "the mapped row is wrong")
    need(a["source_txn_id"] == "TID-1" and a["symbol"] == "TEST", "identifier or symbol not read and stripped")
    need(b["flow_class"] == "EXTERNAL_IN" and c["flow_class"] == "EXTERNAL_OUT", "the External Flow rule is wrong")
    need(d["symbol"] is None and d["source_txn_id"] is None, "an empty symbol or identifier must be null")
    need(d["action"] == con["type_action"][d["txn_type"]], "a line with no Action must derive its action from the pair")
    need(e["txn_type"] == UNMAPPED and e["flow_class"] == "UNRESOLVED" and e["coverage"] == "CODE_NOT_IN_MAPPING" and e["action"] is None,
         "a pair the mapping lacks must read UNMAPPED, UNRESOLVED, CODE_NOT_IN_MAPPING (counted, never dropped)")
    mod.check_transaction_rows(rows)
    try:
        mod.check_transaction_rows([dict(rows[0], txn_type="Not A Word")])
    except SystemExit:
        pass
    else:
        raise Fail("check_transaction_rows accepted a word outside the vocabulary")
    m49 = load_module(root, F49, "account_transaction_49_under_check")
    need(m49.custodian() == m49.custodian().lower(), "the 49 Financial custodian is not lower-cased")


def selftest():
    bad = 0
    count = 0

    def arm(name, got, want):
        nonlocal bad, count
        count += 1
        if got != want:
            bad += 1
            print("SELFTEST FAIL %s: got %r want %r" % (name, got, want))

    arm("names", test_names("def test_a_b():\n    pass\ndef helper():\n    pass"), ["test a b"])
    arm("words-green", missing_words(["pair action flow fee settle identifier custodian external schema unmapped new code vocabulary"], TITLE_WORDS), [])
    arm("words-red", missing_words(["pair"], TITLE_WORDS), list(TITLE_WORDS[1:]))
    arm("pytest", pytest_counts("2 failed, 21 passed in 1s"), (21, 2, 0))
    arm("hash-order", schema_hash_of([("a", "string"), ("b", "double")]) == schema_hash_of([("b", "double"), ("a", "string")]), True)
    arm("columns", len(COLUMNS), 17)
    r = base_row()
    arm("base-row", (r["Custodian"].strip().lower(), r["TransactionID"].strip()), ("some custodian", "TID-1"))
    print("selftest %s" % ("FAIL" if bad else "PASS (%d arms)" % count))
    return 1 if bad else 0


def main(argv):
    if len(argv) == 2 and argv[1] == "--selftest":
        return selftest()
    if len(argv) != 3:
        print(__doc__)
        return 2
    root, ac = argv[1], argv[2]
    if ac != "DBF130-1-AC3":
        print("%s FAIL (unknown criterion)" % ac)
        return 1
    try:
        ac_all(root)
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
