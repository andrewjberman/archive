"""IRPT_DASHBD round 149, workstream COTFIRSTROW (issuer 2.0.0_SA_COO~D2) -- DB-b-303, ONE meaning of history_scope across firms (CTO msg 9480): the Cottonwood adapter calls an account PARTIAL_HISTORY when it has a
ROW on the source floor day (whatever the row's value), as the 49 Financial producer does, not when its floor-day value is positive; the contracts' sentence says so. 31 of 867 floor-day accounts split the two rules.

  DB171-1-AC1  the diff: the adapter changes only inside derive_rows and derive; the three contract fields gain exactly the one clarifying sentence; nothing else of either contract, the handler or any other file moves
  DB171-1-AC2  the behaviour: floor_accounts (a set of accounts with a row on the floor day) decides the scope; zero, negative and unreadable floor rows are PARTIAL, an account absent from the floor partition is FULL, no floor keeps the legacy rows
  DB171-1-AC3  the tests: the three Cottonwood test files pass, floor_values is gone from the adapter and its tests, and the history-scope test file holds first-row tests

Usage: python <this file> <repo_root> <criterion_id>      prints "<id> PASS" or "<id> FAIL" last
       python <this file> --selftest <reference_root>      runs the criteria on a reference tree and on single-fault mutants of its adapter
"""
import importlib.util
import inspect
import json
import re
import subprocess
import sys
from pathlib import Path

BASE = "2cbe7bbcac43013a4fde53c3a73e70f4913827ba"
ADAPTER = "data/assets/scripts/gold/irpt_reporting/adapters/cottonwood_bd_account_return_daily.py"
TESTS = "data/assets/scripts/gold/irpt_reporting/tests/"
T_SCOPE = TESTS + "test_history_scope_derivation.py"
T_REWRITE = TESTS + "test_cottonwood_rewrite.py"
T_ADAPTER = TESTS + "test_cottonwood_bd_account_return_daily.py"
SERIES = "org/standards/IRPT_DASHBD_SERIES_CONTRACT.json"
SOURCE = "org/standards/IRPT_DASHBD_ACCOUNT_RETURN_DAILY_CONTRACT.json"
CLAUSE = " A 'value day' is a day on which the source holds a row for the account, whatever the row's value: a zero, negative or unreadable balance row counts, so an account with a row on the source floor is PARTIAL_HISTORY."
SERIES_PATH = ("series", "fields", "history_scope", "sentence")
SOURCE_PATHS = (("conditional_columns", 1, "rule"), ("rule24_record", "v046"))
FLOOR = "2026-07-10"


class Fail(Exception):
    pass


def need(cond, msg):
    if not cond:
        raise Fail(msg)


def git_show(root, rel):
    r = subprocess.run(["git", "-C", str(root), "show", "%s:%s" % (BASE, rel)], capture_output=True)
    need(r.returncode == 0, "cannot read %s at the base %s" % (rel, BASE[:10]))
    return r.stdout


def rd(root, rel):
    p = Path(root) / rel
    need(p.is_file(), "no %s" % rel)
    return p.read_bytes()


def func_text(text, name):
    m = re.search(r"^def %s\(.*?(?=^def |^class |^# -{20,}|\Z)" % re.escape(name), text, flags=re.S | re.M)
    need(m, "no def %s" % name)
    return m.group(0)


def get_path(doc, path):
    for k in path:
        doc = doc[k]
    return doc


def set_path(doc, path, value):
    for k in path[:-1]:
        doc = doc[k]
    doc[path[-1]] = value


# ------------------------------------------------------------------------------------------------ AC1
def check_diff(root):
    new_a, old_a = rd(root, ADAPTER).decode("utf-8"), git_show(root, ADAPTER).decode("utf-8")
    need("\r" not in new_a, "the adapter must keep LF line endings")
    for fn in ("derive_rows", "derive"):
        old_a = old_a.replace(func_text(old_a, fn), "<<%s>>" % fn)
        new_a = new_a.replace(func_text(new_a, fn), "<<%s>>" % fn)
    need(new_a == old_a, "the adapter differs from the base outside derive_rows and derive")
    cur = rd(root, ADAPTER).decode("utf-8")
    need("floor_values" not in cur, "floor_values must be gone from the adapter (the parameter is floor_accounts)")
    for rel, paths in ((SERIES, (SERIES_PATH,)), (SOURCE, SOURCE_PATHS)):
        new_t, old_t = rd(root, rel).decode("utf-8"), git_show(root, rel).decode("utf-8")
        need("\r" not in new_t, "%s must keep LF line endings" % rel)
        new_j, old_j = json.loads(new_t), json.loads(old_t)
        for path in paths:
            need(get_path(new_j, path) == get_path(old_j, path) + CLAUSE, "%s %s: the field must be the old text plus exactly the clarifying sentence" % (rel.rsplit("/", 1)[-1], "/".join(str(p) for p in path)))
            set_path(new_j, path, get_path(old_j, path))
        need(new_j == old_j, "%s differs from the base in a field other than the clarified sentence(s)" % rel.rsplit("/", 1)[-1])
        changed = [i for i, (a, b) in enumerate(zip(new_t.split("\n"), old_t.split("\n"))) if a != b]
        need(len(new_t.split("\n")) == len(old_t.split("\n")) and len(changed) == len(paths), "%s: exactly %d line(s) change and no line is added or removed, found %d" % (rel.rsplit("/", 1)[-1], len(paths), len(changed)))
    return True


# ------------------------------------------------------------------------------------------------ AC2
def load_adapter(root):
    root = Path(root)
    sys.path[:0] = [str(root / "lib"), str(root / "data/assets/scripts/gold/irpt_reporting/adapters"), str(root)]
    sys.modules.pop("cottonwood_bd_account_return_daily", None)
    spec = importlib.util.spec_from_file_location("cottonwood_bd_account_return_daily", str(root / ADAPTER))
    mod = importlib.util.module_from_spec(spec)
    sys.modules["cottonwood_bd_account_return_daily"] = mod
    spec.loader.exec_module(mod)
    return mod


class FakeReader(object):
    """list_partitions and read_parquet over in-memory tables; the interface the adapter's derive reads through."""
    def __init__(self, alloc, trans):
        self.alloc, self.trans, self.reads = alloc, trans, 0

    def list_partitions(self, table):
        return sorted((self.alloc if table == "fact_allocations" else self.trans).keys())

    def read_parquet(self, table, day):
        import pyarrow as pa
        self.reads += 1
        if table == "fact_allocations":
            rows = self.alloc[day]
            return pa.table({"AccountID": [r[0] for r in rows], "Account Market Value": pa.array([r[1] for r in rows], type=pa.float64())})
        rows = self.trans[day]
        return pa.table({"AccountID": [r[0] for r in rows], "Trade Date": [r[1] for r in rows], "External Flow": [r[2] for r in rows], "Transaction Type": [r[3] for r in rows], "Market Value": pa.array([r[4] for r in rows], type=pa.float64())})


def check_behaviour(root):
    cbd = load_adapter(root)
    sig = inspect.signature(cbd.derive_rows)
    need("floor_accounts" in sig.parameters and "floor_values" not in sig.parameters, "derive_rows takes floor_accounts and no longer floor_values")
    days = ["2026-07-10", "2026-07-13", "2026-07-14"]
    vals = {"2026-07-10": 0.0, "2026-07-13": 100.0, "2026-07-14": 110.0}
    legacy = cbd.derive_rows("A1", vals, {}, {}, days)
    need(legacy and all(r["history_scope"] == "PARTIAL_HISTORY" and "history_scope_claim" not in r for r in legacy), "no floor: the legacy rows are PARTIAL_HISTORY with no claim")
    on = cbd.derive_rows("A1", vals, {}, {}, days, floor_accounts={"A1", "B2"})
    need(on and all(r["history_scope"] == "PARTIAL_HISTORY" and r["history_scope_claim"] == "inferred" for r in on), "an account with a row on the floor day reads PARTIAL_HISTORY with the claim, even when its floor-day value is zero")
    off = cbd.derive_rows("A1", vals, {}, {}, days, floor_accounts={"B2"})
    need(off and all(r["history_scope"] == "FULL" and r["history_scope_claim"] == "inferred" for r in off), "an account with no row on the floor day reads FULL with the claim")
    empty = cbd.derive_rows("A1", vals, {}, {}, days, floor_accounts=set())
    need(empty and all(r["history_scope"] == "FULL" and r["history_scope_claim"] == "inferred" for r in empty), "an empty floor set is a floor: FULL with the claim, not the legacy rows")
    # derive over a fake reader: positive, zero, negative and unreadable floor rows are PARTIAL; an account absent from the floor partition is FULL
    alloc = {FLOOR: [("PPPPPPPPPP1", 500.0), ("ZZZZZZZZZZ2", 0.0), ("NNNNNNNNNN3", -40.0), ("UUUUUUUUUU4", None)],
             "2026-07-13": [("PPPPPPPPPP1", 510.0), ("ZZZZZZZZZZ2", 20.0), ("NNNNNNNNNN3", 30.0), ("UUUUUUUUUU4", 60.0), ("AAAAAAAAAA5", 70.0)]}
    trans = {"2026-07-13": [("PPPPPPPPPP1", "2026-07-13", "N", "Buy", 1.0)]}
    accounts = {"PPPPPPPPPP1", "ZZZZZZZZZZ2", "NNNNNNNNNN3", "UUUUUUUUUU4", "AAAAAAAAAA5"}
    rows, _ = cbd.derive(FakeReader(alloc, trans), accounts, "2026-07-10", "2026-07-13", floor_day=FLOOR)
    scope = {}
    for r in rows:
        scope.setdefault(r["account_id"], set()).add((r["history_scope"], r.get("history_scope_claim")))
    for a in ("PPPPPPPPPP1", "ZZZZZZZZZZ2", "NNNNNNNNNN3", "UUUUUUUUUU4"):
        need(scope.get(a) == {("PARTIAL_HISTORY", "inferred")}, "%s has a row on the floor day and must read PARTIAL_HISTORY with the claim, read %s" % (a[:1], scope.get(a)))
    need(scope.get("AAAAAAAAAA5") == {("FULL", "inferred")}, "an account absent from the floor partition must read FULL with the claim, read %s" % scope.get("AAAAAAAAAA5"))
    rows2, _ = cbd.derive(FakeReader(alloc, trans), accounts, "2026-07-10", "2026-07-13", floor_day=None)
    need(rows2 and all(r["history_scope"] == "PARTIAL_HISTORY" and "history_scope_claim" not in r for r in rows2), "no floor day: legacy rows, no claim")
    rows3, _ = cbd.derive(FakeReader({k: v for k, v in alloc.items() if k != FLOOR}, trans), accounts, "2026-07-10", "2026-07-13", floor_day=FLOOR)
    need(rows3 and all("history_scope_claim" not in r for r in rows3), "a floor day absent from the listing: legacy rows, no claim")
    return True


# ------------------------------------------------------------------------------------------------ AC3
def check_tests(root):
    root = Path(root)
    scope_t, adapter_t, rewrite_t = (rd(root, f).decode("utf-8") for f in (T_SCOPE, T_ADAPTER, T_REWRITE))
    for name, text in (("test_history_scope_derivation.py", scope_t), ("test_cottonwood_bd_account_return_daily.py", adapter_t), ("test_cottonwood_rewrite.py", rewrite_t)):
        need("floor_values" not in text, "floor_values must be gone from %s" % name)
    base_scope = git_show(root, T_SCOPE).decode("utf-8")
    new_names = set(re.findall(r"^def (test_\w+)\(", scope_t, flags=re.M)) - set(re.findall(r"^def (test_\w+)\(", base_scope, flags=re.M))
    need(len([n for n in new_names if "first_row" in n]) >= 3, "at least three NEW tests in test_history_scope_derivation.py carry first_row in their name (zero, negative/unreadable, absent), found %s" % sorted(new_names))
    r = subprocess.run([sys.executable, "-m", "pytest", "-q", "-x", "-p", "no:cacheprovider", "--color=no", str(root / T_SCOPE), str(root / T_REWRITE), str(root / T_ADAPTER)], capture_output=True, text=True, cwd=str(root))
    need(r.returncode == 0, "pytest failed: %s" % (r.stdout + r.stderr)[-400:].replace("\n", " | "))
    need(re.search(r"\b\d+ passed\b", r.stdout) is not None, "pytest printed no pass count")
    return True


CHECKS = {"DB171-1-AC1": check_diff, "DB171-1-AC2": check_behaviour, "DB171-1-AC3": check_tests}


def selftest(ref_root):
    ref = Path(ref_root)
    for fn in CHECKS.values():
        fn(ref)
    adapter = ref / ADAPTER
    original = adapter.read_bytes()
    txt = original.decode("utf-8")
    n = 0
    anchors = {
        "membership replaced by positivity": ('"PARTIAL_HISTORY" if account_id in floor_accounts else "FULL"', '"PARTIAL_HISTORY" if (account_id in floor_accounts and values.get(days[0], 0) > 0) else "FULL"'),
        "absent account reads PARTIAL": ('"PARTIAL_HISTORY" if account_id in floor_accounts else "FULL"', '"PARTIAL_HISTORY" if True else "FULL"'),
        "claim dropped": ('else "FULL"), True', 'else "FULL"), False'),
    }
    try:
        for label, (a, b) in anchors.items():
            need(a in txt, "selftest: the reference adapter lacks the anchor for '%s'" % label)
            adapter.write_bytes(txt.replace(a, b, 1).encode("utf-8"))
            try:
                check_behaviour(ref)
            except (Fail, AssertionError, Exception):  # noqa: BLE001
                n += 1
                continue
            raise AssertionError("mutant passed: " + label)
        # a diff mutant: a changed line outside derive_rows and derive
        adapter.write_bytes(txt.replace("def to_table(rows, with_source=False):", "def to_table(rows, with_source=False):  # touched", 1).encode("utf-8"))
        try:
            check_diff(ref)
        except Fail:
            n += 1
        else:
            raise AssertionError("diff mutant passed")
    finally:
        adapter.write_bytes(original)
    print("selftest: green on the reference and red on %d single-fault mutants" % n)
    print("selftest PASS")


if __name__ == "__main__":
    if sys.argv[1:2] == ["--selftest"]:
        selftest(sys.argv[2])
        sys.exit(0)
    try:
        CHECKS[sys.argv[2]](sys.argv[1])
        print({"DB171-1-AC1": "OK: the adapter changes only inside derive_rows and derive; the three contract sentences gain exactly the one clarifying sentence and no other byte of either contract, the handler or any other file moves",
               "DB171-1-AC2": "OK: an account with a row on the floor day (positive, zero, negative or unreadable) reads PARTIAL_HISTORY with the claim, an account absent from the floor partition reads FULL with the claim, and no floor keeps the legacy rows without a claim",
               "DB171-1-AC3": "OK: floor_values is gone from the adapter and its tests, the history-scope test file holds the new first-row tests, and the three Cottonwood test files pass"}[sys.argv[2]])
        print(sys.argv[2] + " PASS")
    except Exception as ex:  # a failed read or clause is a FAIL, not a traceback
        print("FAIL: " + str(ex))
        print(sys.argv[2] + " FAIL")
        sys.exit(1)
