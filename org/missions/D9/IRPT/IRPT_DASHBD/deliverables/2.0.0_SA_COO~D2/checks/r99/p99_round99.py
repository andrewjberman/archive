"""IRPT_DASHBD round 99 (issuer 2.0.0_SA_COO~D2) -- 1.0.0_SA_CTO~DELL2 msg 7401 (the CVO's row W147-S3: CASH_USD is its own counted pair).

  DB-b-185 (~150, LOCAL)  the gold ETF classifier serves the cash class for the synthetic sweep-cash ticker too, tests updated and a mutant, and the COUNT
                          of served positions and consumers that change; no deploy, no write.                                        DB99-1-AC1

Usage: python <this file> <repo_root> <criterion_id>; prints "<id> PASS" or "<id> FAIL" last.
"""
import hashlib
import json
import re
import subprocess
import sys
from pathlib import Path

PROJ = "org/missions/D9/IRPT/IRPT_DASHBD/"
RECORD = PROJ + "deliverables/0.9.0_WK_IRPT_DASHBD~150/CASH_USD_CASH_CHANGE.json"
CLASSIFIER = "data/black_diamond/scripts/gold/lib/etf_classifier.py"
PIN = "e340e07f4e"
PIN_SHA = "e7385264668e9bf746aeab809c8ff0a869f9091685f86751b1679dfc6ddd81ba"
HEX64 = re.compile(r"[0-9a-f]{64}")
RUN = re.compile(r"\d{8,}")
MAX_CHANGED_LINES = 24

SMOKE = r"""
import sys
sys.path.insert(0, 'data/black_diamond/scripts/gold')
from lib.etf_classifier import ETFClassifier


class Stub:
    def __init__(self, rows):
        self.rows, self.calls = rows, []

    def get_classification(self, t):
        self.calls.append(t)
        return self.rows.get(t)


rows = {'TYPEDCASH': {'asset_class': 'fixed_income', 'sub_asset_class': 'Cash'},
        'BOND': {'asset_class': 'fixed_income', 'sub_asset_class': 'Treasury'},
        'EQ': {'asset_class': 'equity', 'sub_asset_class': 'Large Cap'}}
s = Stub(rows)
c = ETFClassifier(client=s)
out = {
    'cash_usd': c.classify('CASH_USD', 'BD SYNTHETIC CASH'),
    'cash_usd_lower': c.classify('cash_usd', 'x'),
    'cash_usd_identity': str(c.classify_with_identity('CASH_USD', 'BD SYNTHETIC CASH')),
    'typed_cash': c.classify('TYPEDCASH'),
    'bond': c.classify('BOND'),
    'eq': c.classify('EQ'),
    'unknown': c.classify('NOPE'),
    'client_calls_for_cash_usd': [t for t in s.calls if str(t).upper() == 'CASH_USD'],
}
import json
print(json.dumps(out))
"""


class Fail(Exception):
    pass


def need(cond, msg):
    if not cond:
        raise Fail(msg)


def is_int(v):
    return isinstance(v, int) and not isinstance(v, bool) and v >= 0


def long_digit_runs(obj, name=""):
    hits = []
    if isinstance(obj, dict):
        for k, v in obj.items():
            if not str(k).endswith("sha256") and str(k) not in ("commit", "path", "pin", "file"):
                hits += long_digit_runs(v, name + "/" + str(k))
    elif isinstance(obj, list):
        for i, v in enumerate(obj):
            hits += long_digit_runs(v, "%s/%d" % (name, i))
    elif isinstance(obj, str) and RUN.search(obj):
        hits.append(name)
    return hits


def check(root):
    p = root / RECORD
    need(p.is_file(), "no %s" % RECORD)
    r = json.loads(p.read_bytes().decode("utf-8"))

    # the code: tracked, hashes to the stated sha256, differs from the round-96 pin by a handful of lines
    code = r.get("code") or {}
    need(code.get("file") == CLASSIFIER and code.get("tracked") is True and HEX64.fullmatch(str(code.get("sha256") or "")), "code %r" % code)
    need(hashlib.sha256((root / CLASSIFIER).read_bytes()).hexdigest() == code["sha256"], "the classifier on disk does not hash to code.sha256")
    need(code["sha256"] != PIN_SHA, "the classifier equals the round-96 pin: no change was made")
    g = subprocess.run(["git", "-C", str(root), "diff", "--numstat", PIN, "--", CLASSIFIER], capture_output=True, text=True)
    need(g.returncode == 0 and g.stdout.strip(), "git diff against the pin %s read nothing (rc %s)" % (PIN, g.returncode))
    add, dele = g.stdout.split()[:2]
    need(add.isdigit() and dele.isdigit() and 0 < int(add) + int(dele) <= MAX_CHANGED_LINES, "the diff against the pin is %s added and %s deleted lines: one rule changes %d lines at most" % (add, dele, MAX_CHANGED_LINES))
    need(r.get("pin") == PIN, "pin must be %s" % PIN)

    # behaviour, executed here (stub client, no AWS)
    o = subprocess.run([sys.executable, "-I", "-c", SMOKE], cwd=str(root), capture_output=True, text=True)
    need(o.returncode == 0, "the smoke run failed: %s" % o.stderr.strip()[-300:])
    b = json.loads(o.stdout.strip().splitlines()[-1])
    need(b["cash_usd"] == "cash" and b["cash_usd_lower"] == "cash", "classify('CASH_USD') returns %r, want cash" % b["cash_usd"])
    need("cash" in b["cash_usd_identity"] and "fixed_income" not in b["cash_usd_identity"], "classify_with_identity('CASH_USD') returns %r" % b["cash_usd_identity"])
    need(b["typed_cash"] == "cash" and b["bond"] == "fixed_income" and b["eq"] == "equity" and b["unknown"] == "", "the round-96 rule or a verbatim row changed: %r" % b)
    need(b["client_calls_for_cash_usd"] == [], "CASH_USD must still be answered before the table is read")

    # tests and the mutant
    t = r.get("tests") or {}
    need(str(t.get("new_file") or "").strip() and t.get("mutant_failed") is True and is_int(t.get("passed")) and t["passed"] >= 3 and t.get("failed") == 0, "tests %r: a file, a mutant that failed, 3 or more passing, none failing" % t)
    need(isinstance(t.get("updated_files"), list) and t["updated_files"] and all(isinstance(x, str) and x.strip() for x in t["updated_files"]), "tests.updated_files must name every existing test that pinned CASH_USD as fixed_income")
    need(is_int(t.get("suite_passed")) and t["suite_passed"] >= 37 and t.get("suite_failed") == 0, "tests.suite_passed (37 or more) and suite_failed 0 over the classifier test files and the composition and positions tests that name CASH_USD")

    # the count
    ho = r.get("served_holdings") or {}
    need(isinstance(ho.get("stores_read"), list) and ho["stores_read"] and is_int(ho.get("positions_scanned")) and ho["positions_scanned"] > 0 and is_int(ho.get("positions_that_move")) and ho["positions_that_move"] <= ho["positions_scanned"]
         and is_int(ho.get("positions_already_cash")) and is_int(ho.get("accounts_with_a_moving_position")) and isinstance(ho.get("per_firm"), dict) and ho["per_firm"] and sum(ho["per_firm"].values()) == ho["positions_that_move"],
         "served_holdings %r needs stores_read, positions_scanned, positions_that_move, positions_already_cash, per_firm summing to it, and accounts_with_a_moving_position" % ho)
    need(isinstance(r.get("limits"), str) and r["limits"].strip(), "limits must say what the count does not see")

    # who assumes the old class
    cc = r.get("consumers_checked")
    need(isinstance(cc, list) and len(cc) >= 3 and all(isinstance(x, str) and x.strip() for x in cc), "consumers_checked must name 3 or more readers of the class")
    ca = r.get("consumers_assuming_fixed_income")
    need(isinstance(ca, list) and all(isinstance(x, dict) and str(x.get("file") or "").strip() and is_int(x.get("line")) and str(x.get("what") or "").strip() for x in ca), "consumers_assuming_fixed_income must be a list (possibly empty) of {file, line, what}")
    need(isinstance(r.get("other_cash_usd_literals"), list), "other_cash_usd_literals must be a list of {file, line} for every other place the ticker is hard-coded")

    rd = r.get("reads") or {}
    need(rd.get("dynamodb_writes") == 0 and rd.get("s3_writes") == 0 and rd.get("vendor_calls") == 0 and rd.get("secret_reads") == 0, "reads %r" % rd)
    need(r.get("deployed") is False and r.get("pushed") is False and r.get("served_values_changed") is False, "deployed, pushed and served_values_changed must be false")
    hits = long_digit_runs(r)
    need(not hits, "the record holds a run of 8 or more digits at %s" % hits[:3])
    print("OK: CASH_USD serves cash in classify and classify_with_identity (%s added, %s deleted lines against the pin), %d served positions move, %d consumer(s) assume the old class" % (add, dele, ho["positions_that_move"], len(ca)))


def main():
    root = Path(sys.argv[1] if len(sys.argv) > 1 else ".").resolve()
    cid = sys.argv[2] if len(sys.argv) > 2 else ""
    try:
        need(cid == "DB99-1-AC1", "unknown criterion %r" % cid)
        check(root)
    except Fail as e:
        print("FAIL: %s" % e)
        print("%s FAIL" % (cid or "DB99"))
        sys.exit(1)
    print("%s PASS" % cid)


if __name__ == "__main__":
    main()
