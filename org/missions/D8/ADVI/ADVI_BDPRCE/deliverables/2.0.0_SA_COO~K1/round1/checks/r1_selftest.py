"""Self-test of r1_checks.py: one GOOD fixture per grader (must pass) and one MUTANT per rule (must fail). ASCII only.
Prints `R1 SELFTEST: OK <n> arms` on success.
"""
import copy
import json
import os
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
CHK = os.path.join(HERE, "r1_checks.py")

GOOD = {
    "writers": {
        "order": "BP-a-1", "read_at": "2026-10-13T13:00:00Z", "claim": "measured", "object_versions_read": 12,
        "calls": ["aws s3api list-object-versions --bucket opal-data-bd --prefix silver/prices/canonical_prices.parquet"],
        "writers": [
            {"writer_id": "lambda:bd-price-update", "bucket": "opal-data-bd", "object_key": "silver/prices/canonical_prices.parquet",
             "evidence": "x", "rule_copy": "bd_price_update.py:327", "claim": "measured"},
            {"writer_id": "lambda:bd-price-update", "bucket": "opal-data-bd", "object_key": "silver/prices/2026-10-12.parquet",
             "evidence": "x", "rule_copy": "bd_price_update.py:327", "claim": "inferred"}],
        "unidentified": [],
    },
    "gap": {
        "order": "BP-a-3", "claim": "measured", "served_rows": 10, "window": "2026-09-16..2026-10-13",
        "bound_statement": "1 of 10 unexplained",
        "classes": {"EQUAL": 6, "EXPLAINED_BY_VERSION_AT_WRITE": 2, "EXPLAINED_BY_MULTIDAY_WINDOW": 1,
                    "EXPLAINED_OTHER": 0, "UNEXPLAINED": 1, "NOT_RECOMPUTABLE": 0},
        "calls": ["aws s3api get-object --bucket opal-data-bd --key silver/transactions/2026-10-12.parquet"],
    },
    "trace": {"asset_name": "A", "date": "2026-10-12", "served_price": 1.5, "price_source": "transaction_observed",
              "rule": "median(|market_value|/|units|) over the day's rows", "trade_ids": ["t1", "t2"],
              "recomputed_price": 1.5, "match": True},
    "thread": {"served_object_key": "k", "as_of_date": "2026-10-12", "account_ref": "0123456789ab", "asset_name": "A",
               "ticker": None, "served_price": 1.5, "price_source": "transaction_observed", "rule": "R",
               "trade_ids": ["t1"], "recomputed_price": 1.5, "recompute_equals_served": True,
               "instrument": "p", "claim": "measured"},
}


def mutant(kind, why, edit):
    rec = copy.deepcopy(GOOD[kind])
    edit(rec)
    return (kind, why, rec)


MUTANTS = [
    mutant("writers", "write verb", lambda r: r["calls"].append("aws s3api put-object --bucket b --key k")),
    mutant("writers", "no denominator", lambda r: r.update(object_versions_read=0)),
    mutant("writers", "no canonical row", lambda r: r.update(writers=r["writers"][1:])),
    mutant("gap", "sum mismatch", lambda r: r["classes"].update(EQUAL=7)),
    mutant("gap", "class set open", lambda r: r["classes"].pop("UNEXPLAINED")),
    mutant("gap", "no bound", lambda r: r.update(bound_statement="")),
    mutant("trace", "txn with no ids", lambda r: r.update(trade_ids=[])),
    mutant("thread", "raw account id", lambda r: r.update(account_id="123")),
    mutant("thread", "tickered holding", lambda r: r.update(ticker="IQLT")),
    mutant("thread", "no trades", lambda r: r.update(trade_ids=[])),
]


def run(kind, rec):
    with tempfile.TemporaryDirectory() as d:
        p = os.path.join(d, "r.json")
        with open(p, "w", encoding="utf-8") as fh:
            json.dump(rec, fh)
        r = subprocess.run([sys.executable, CHK, kind, "--file", p], capture_output=True, text=True)
        return r.returncode, r.stdout.strip().splitlines()[-1] if r.stdout.strip() else ""


def main():
    arms = 0
    for kind, rec in GOOD.items():
        rc, line = run(kind, rec)
        if rc != 0 or "record ok" not in line:
            print("R1 SELFTEST: FAIL good arm %s -> %s" % (kind, line))
            return 1
        arms += 1
    for kind, why, rec in MUTANTS:
        rc, line = run(kind, rec)
        if rc == 0 or "record FAIL" not in line:
            print("R1 SELFTEST: FAIL mutant arm %s/%s was admitted -> %s" % (kind, why, line))
            return 1
        arms += 1
    print("R1 SELFTEST: OK %d arms" % arms)
    return 0


if __name__ == "__main__":
    sys.exit(main())
