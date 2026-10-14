"""IRPT_DASHBD round 111 (issuer 2.0.0_SA_COO~D2) -- the 49 Financial HOUSEHOLD DAILY RETURN (CTO ROUND-111 ANALYSIS cell 1 and the round-110 ADDENDUM).

  DB111-1-AC1 (~179)  the new sibling contract, the pure function compute_household_returns, its tests, a private dry run against the real 49 Financial gold
                      and the range tie-out read (HOUSEHOLD_TIEOUT_R111.json).

The checker grades the CONTRACT (columns, schema hash recomputed by its stated basis), the worker's MODULE (imported by path and run on a synthetic arm against
the checker's OWN independent computation, within 1e-12; a mutant of that computation must disagree), the TESTS (they exist and pass) and the FORM and INTERNAL
CONSISTENCY of the tie-out record. It does not re-read the client gold: the record's truth is the reader's and the CTO's. Offline; stdlib only; terminates in seconds.

Usage: python -I <this file> <repo_root> <criterion_id>      prints "<id> PASS" or "<id> FAIL" last
       python -I <this file> --selftest [<repo_root>]          the pure helpers on synthetic arms
"""
import hashlib
import importlib.util
import json
import re
import subprocess
import sys
from pathlib import Path

D = "org/missions/D9/IRPT/IRPT_DASHBD/deliverables/"
CONTRACT_REL = "org/standards/IRPT_DASHBD_HOUSEHOLD_RETURN_DAILY_CONTRACT.json"
MODULE_REL = "data/assets/scripts/gold/irpt_reporting/household_return_daily.py"
TEST_REL = "data/assets/scripts/gold/irpt_reporting/tests/test_household_return_daily.py"
REC_REL = D + "0.9.0_WK_IRPT_DASHBD~179/HOUSEHOLD_TIEOUT_R111.json"
DRIVER_REL = D + "0.9.0_WK_IRPT_DASHBD~179/dry_run_household_return_r111.py"
COLUMNS = [("firm", "string"), ("household_id", "string"), ("business_date", "string"), ("market_value_eod", "double"), ("external_flow", "double"),
           ("total_return_daily", "double"), ("accounts_n", "int64"), ("day_quality", "string"), ("method_version", "int64"), ("schema_version", "string")]
NULLABLE = {"total_return_daily"}
QUALITIES = ["MEASURED", "ACCOUNT_MISSING", "NO_PRIOR_VALUE"]
WINDOWS = ("qtd", "ytd", "last_12_months", "since_inception")
BINS = ("lt_5bp", "5_25bp", "25_100bp", "ge_100bp")
CLAIMS = ("measured", "inferred", "held", "absent")
FOREIGN = ("inflection", "cottonwood", "orion/", "eclipse/", "opal-data-inflection", "opal-data-cottonwood")
WRITE_TOKENS = ("put_object", "upload_file", "upload_fileobj", "copy_object", "delete_object", "delete_objects", "put_item", "delete_item", "update_item", "batch_write_item")
LONG_DIGITS = re.compile(r"\d{8,}")
DIGIT_OK_KEYS = ("sha256", "path", "file", "key", "where", "vintage", "scope_words", "table_sha256")
EPS = 1e-12


class Fail(Exception):
    pass


def need(cond, msg):
    if not cond:
        raise Fail(msg)


def nes(x):
    return isinstance(x, str) and x.strip() != ""


def is_int(x):
    return isinstance(x, int) and not isinstance(x, bool)


def is_num(x):
    return isinstance(x, (int, float)) and not isinstance(x, bool)


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def load(root, rel):
    p = Path(root) / rel
    need(p.is_file(), "no %s" % rel)
    try:
        return json.loads(p.read_bytes().decode("utf-8"))
    except Exception as e:
        raise Fail("%s is not UTF-8 JSON (%s)" % (rel, type(e).__name__))


def schema_hash(cols):
    """sha256 over the sorted 'name:type' lines joined by newline (the account contract's stated basis)."""
    return hashlib.sha256("\n".join(sorted("%s:%s" % (n, t) for n, t in cols)).encode("utf-8")).hexdigest()


def digit_runs(x, key=""):
    out = []
    if isinstance(x, dict):
        for k, v in x.items():
            out += digit_runs(v, k)
    elif isinstance(x, list):
        for v in x:
            out += digit_runs(v, key)
    elif isinstance(x, str) and key not in DIGIT_OK_KEYS and LONG_DIGITS.search(x):
        out.append(key)
    return out


def foreign_hits(src):
    low = src.lower()
    return [t for t in FOREIGN if t in low]


def write_hits(src):
    return [t for t in WRITE_TOKENS if t in src]


# ---------------------------------------------------------------- THE METHOD, independently of the worker's module
def expected(rows, membership, flows=True, missing_as_zero=False):
    """the household daily return: for a household and a date t with previous date p (the previous date the household has any row), S = accounts with a row on BOTH p and t;
    r = (sum V_t over S - sum F_t over S) / (sum V_p over S) - 1. First date: NO_PRIOR_VALUE. An account with a row on p and none on t: ACCOUNT_MISSING, r None.
    An account with a row on t and none on p joins that day (outside S). r None (NO_PRIOR_VALUE) when sum V_p over S <= 0 or S is empty.
    market_value_eod, external_flow and accounts_n are over ALL of the household's accounts with a row on t."""
    by = {}
    for r in rows:
        h = membership.get(r["account_id"])
        if h is None:
            continue
        by.setdefault(h, {}).setdefault(r["business_date"], {})[r["account_id"]] = r
    out = []
    for h in sorted(by):
        dates = sorted(by[h])
        for i, t in enumerate(dates):
            cur = by[h][t]
            v_all = sum(x["market_value_eod"] for x in cur.values())
            f_all = sum(x["external_flow"] for x in cur.values())
            ret, q = None, "NO_PRIOR_VALUE"
            if i > 0:
                prev = by[h][dates[i - 1]]
                missing = [a for a in prev if a not in cur]
                s = [a for a in prev if a in cur]
                if missing and not missing_as_zero:
                    q = "ACCOUNT_MISSING"
                else:
                    vp = sum(prev[a]["market_value_eod"] for a in prev if (a in s or missing_as_zero))
                    vt = sum(cur[a]["market_value_eod"] for a in s)
                    ft = sum(cur[a]["external_flow"] for a in s) if flows else 0.0
                    if s and vp > 0:
                        ret, q = (vt - ft) / vp - 1.0, "MEASURED"
            out.append({"household_id": h, "business_date": t, "market_value_eod": v_all, "external_flow": f_all, "total_return_daily": ret, "accounts_n": len(cur), "day_quality": q})
    return out


def synthetic():
    """one two-account household H1 (A from D1; B joins D3; a deposit into A on D4; B has no row on D5, returns D6) and a one-account household H2 (C)."""
    d = ["2026-01-05", "2026-01-06", "2026-01-07", "2026-01-08", "2026-01-09", "2026-01-12"]
    rows = []

    def add(a, i, v, f=0.0):
        rows.append({"account_id": a, "business_date": d[i], "market_value_eod": v, "external_flow": f})
    for i, v in enumerate([1000.0, 1010.0, 1020.0, 2040.0, 2060.0, 2070.0]):
        add("A", i, v, 1000.0 if i == 3 else 0.0)
    for i, v in ((2, 500.0), (3, 505.0), (5, 520.0)):
        add("B", i, v)
    for i, v in enumerate([300.0, 297.0, 303.0, 306.0, 309.0, 303.0]):
        add("C", i, v, 0.0)
    return rows, {"A": "H1", "B": "H1", "C": "H2"}


def same_rows(a, b):
    """None if equal (keys, order, qualities, sums and returns within 1e-12), else the first difference in words."""
    if len(a) != len(b):
        return "%d rows against %d" % (len(a), len(b))
    for x, y in zip(a, b):
        for k in ("household_id", "business_date", "day_quality", "accounts_n"):
            if x.get(k) != y.get(k):
                return "%s differs at %s %s" % (k, x.get("household_id"), x.get("business_date"))
        for k in ("market_value_eod", "external_flow"):
            if not is_num(x.get(k)) or abs(x[k] - y[k]) > EPS:
                return "%s differs at %s %s" % (k, x.get("household_id"), x.get("business_date"))
        rx, ry = x.get("total_return_daily"), y.get("total_return_daily")
        if (rx is None) != (ry is None) or (rx is not None and (not is_num(rx) or abs(rx - ry) > EPS)):
            return "total_return_daily differs at %s %s" % (x.get("household_id"), x.get("business_date"))
    return None


# ---------------------------------------------------------------- the contract
def check_contract(root):
    c = load(root, CONTRACT_REL)
    need(c.get("table") == "household_return_daily" and "household" in str(c.get("grain", "")).lower() and "trading day" in str(c.get("grain", "")).lower(), "the contract's table is household_return_daily and its grain names household and trading day")
    cols = c.get("columns")
    need(isinstance(cols, list) and [(x.get("name"), x.get("type")) for x in cols] == COLUMNS, "the contract's columns must be exactly %s" % ", ".join("%s:%s" % x for x in COLUMNS))
    for x in cols:
        need(isinstance(x.get("nullable"), bool) and x["nullable"] == (x["name"] in NULLABLE) and nes(x.get("meaning")), "column %s: nullable must be %s and meaning in words" % (x["name"], x["name"] in NULLABLE))
    need((c.get("enums") or {}).get("day_quality") == QUALITIES, "enums.day_quality must be exactly %s" % QUALITIES)
    need(nes(c.get("schema_hash_basis")) and "sorted" in c["schema_hash_basis"], "schema_hash_basis must state the sorted name:type rule")
    need(c.get("schema_hash") == schema_hash(COLUMNS), "schema_hash must equal the recomputed hash %s" % schema_hash(COLUMNS))
    m = str(c.get("method") or "")
    need("ACCOUNT_MISSING" in m and "NO_PRIOR_VALUE" in m and "external" in m.lower() and "joins" in m.lower(), "the contract's method must state the rule in words (ACCOUNT_MISSING, NO_PRIOR_VALUE, external flows, an account that joins)")
    need(str(c.get("firm_specific_columns", "")).startswith("NONE"), "firm_specific_columns must read NONE: no firm code survives into this table")
    return c


# ---------------------------------------------------------------- the module
def load_module(root):
    p = Path(root) / MODULE_REL
    need(p.is_file(), "no %s" % MODULE_REL)
    src = p.read_text(encoding="utf-8")
    need(not foreign_hits(src) and not write_hits(src) and "boto3" not in src, "the module is a pure function: no other firm's place, no write call, no boto3 (hits %s %s)" % (foreign_hits(src), write_hits(src)))
    spec = importlib.util.spec_from_file_location("household_return_daily_under_check", str(p))
    mod = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = mod
    spec.loader.exec_module(mod)
    return mod


def check_module(root):
    mod = load_module(root)
    need(callable(getattr(mod, "compute_household_returns", None)), "the module must define compute_household_returns(rows, membership)")
    need([tuple(x) for x in getattr(mod, "ARROW_SCHEMA_COLUMNS", [])] == COLUMNS, "the module's ARROW_SCHEMA_COLUMNS must equal the contract's columns (name, type)")
    rows, mem = synthetic()
    got = mod.compute_household_returns(json.loads(json.dumps(rows)), dict(mem))
    diff = same_rows(got, expected(rows, mem))
    need(diff is None, "compute_household_returns disagrees with the checker's own computation on the synthetic week: %s" % diff)
    need(same_rows(got, expected(rows, mem, flows=False)) is not None, "CONTROL: a computation that ignores external flows agrees with the module on the synthetic week (the arm does not exercise the deposit)")
    need(same_rows(got, expected(rows, mem, missing_as_zero=True)) is not None, "CONTROL: a computation that treats a missing account as zero agrees with the module (the arm does not exercise the missing day)")
    by = {(r["household_id"], r["business_date"]): r for r in got}
    own = {}
    for r in rows:
        if r["account_id"] == "C":
            own[r["business_date"]] = r
    ds = sorted(own)
    for a, b in zip(ds, ds[1:]):
        want = (own[b]["market_value_eod"] - own[b]["external_flow"]) / own[a]["market_value_eod"] - 1.0
        need(abs(by[("H2", b)]["total_return_daily"] - want) <= EPS, "a one-account household must equal its account's own daily return")
    q = {(r["household_id"], r["business_date"]): r["day_quality"] for r in got}
    need(q[("H1", "2026-01-09")] == "ACCOUNT_MISSING" and by[("H1", "2026-01-09")]["total_return_daily"] is None, "an account with a row on the previous date and none on the day makes the day ACCOUNT_MISSING and its return None, never zero")
    need(q[("H1", "2026-01-05")] == "NO_PRIOR_VALUE", "a household's first date is NO_PRIOR_VALUE")
    return mod


def check_tests(root):
    p = Path(root) / TEST_REL
    need(p.is_file(), "no %s" % TEST_REL)
    src = p.read_text(encoding="utf-8")
    need(len(re.findall(r"^\s*def test_", src, re.M)) >= 3, "the test file holds at least 3 tests (a week with a deposit and a missing day, a one-account household, a mutant)")
    g = subprocess.run([sys.executable, "-m", "pytest", "-q", "-p", "no:cacheprovider", str(p)], cwd=str(root), capture_output=True, text=True, timeout=100)
    need(g.returncode == 0, "the tests do not pass: %s" % (g.stdout.strip().splitlines() or ["no output"])[-1][:200])


# ---------------------------------------------------------------- the tie-out record
def check_record(r, root=None):
    need(isinstance(r, dict), "the record is not an object")
    m = r.get("method")
    need(isinstance(m, dict) and nes(m.get("words")) and m.get("claim") in CLAIMS, "method must hold words and a claim")
    need(r.get("tolerance_assumed") is None, "tolerance_assumed must be null: no tolerance is assumed and the CTO rules on the outside-range count")
    hh = r.get("households")
    need(isinstance(hh, dict) and all(is_int(hh.get(k)) and hh[k] >= 1 for k in ("total", "accounts_total", "multi_account")) and hh.get("claim") in CLAIMS, "households must hold total, accounts_total and multi_account (integers) and a claim")
    need(hh["multi_account"] <= hh["total"], "multi_account cannot exceed total households")
    w = r.get("windows")
    need(isinstance(w, dict) and set(w.keys()) == set(WINDOWS), "windows must be keyed exactly %s" % list(WINDOWS))
    for k in WINDOWS:
        x = w[k]
        need(isinstance(x, dict) and x.get("claim") in CLAIMS, "windows.%s must carry a claim" % k)
        for f in ("households_compared", "within_range", "outside_range", "not_comparable"):
            need(is_int(x.get(f)) and x[f] >= 0, "windows.%s.%s must be a non-negative integer" % (k, f))
        need(x["within_range"] + x["outside_range"] == x["households_compared"], "windows.%s: within_range + outside_range must equal households_compared" % k)
        bins = x.get("bins")
        need(isinstance(bins, dict) and set(bins.keys()) == set(BINS) and all(is_int(v) and v >= 0 for v in bins.values()), "windows.%s.bins must hold %s as integers" % (k, list(BINS)))
        need(sum(bins.values()) == x["outside_range"], "windows.%s: the bins must sum to outside_range" % k)
        why = x.get("not_comparable_reasons")
        need(isinstance(why, dict) and all(is_int(v) and v >= 0 for v in why.values()) and sum(why.values()) == x["not_comparable"], "windows.%s.not_comparable_reasons must be counts summing to not_comparable" % k)
        need(x["households_compared"] + x["not_comparable"] <= hh["total"], "windows.%s: compared plus not comparable cannot exceed the households" % k)
    one = r.get("one_account_households")
    need(isinstance(one, dict) and is_int(one.get("compared")) and one["compared"] >= 1 and is_num(one.get("max_abs_gap")) and one.get("claim") in CLAIMS, "one_account_households must hold compared (at least 1), max_abs_gap and a claim")
    need(one["max_abs_gap"] <= 1e-9, "every one-account household must equal its account: max_abs_gap %r exceeds 1e-9" % one["max_abs_gap"])
    dr = r.get("dry_run")
    need(isinstance(dr, dict) and re.fullmatch(r"\d{4}-\d{2}-\d{2}", str(dr.get("first_date"))) and re.fullmatch(r"\d{4}-\d{2}-\d{2}", str(dr.get("last_date"))) and is_int(dr.get("partitions_read")) and dr["partitions_read"] >= 1
         and is_int(dr.get("table_rows")) and dr["table_rows"] >= 1 and re.fullmatch(r"[0-9a-f]{64}", str(dr.get("table_sha256"))) and dr.get("claim") in CLAIMS,
         "dry_run must hold first_date, last_date (ISO), partitions_read, table_rows, table_sha256 and a claim")
    need(dr["first_date"] <= dr["last_date"], "dry_run.first_date is after last_date")
    rd = r.get("reads")
    need(isinstance(rd, dict) and all(rd.get(k) == 0 for k in ("vendor_calls", "s3_writes", "dynamodb_writes", "secret_reads")) and is_int(rd.get("s3_reads")) and rd["s3_reads"] >= 1, "reads: zero writes, vendor calls and secret reads; s3_reads a positive integer")
    need(r.get("files_in_repo") is False and r.get("served_values_changed") is False and r.get("pushed") is False and r.get("deployed") is False, "files_in_repo, served_values_changed, pushed and deployed must be false")
    need(not digit_runs(r), "the record holds a run of 8 or more digits outside a hash, path, file, key, where or vintage field: %s" % digit_runs(r))
    b = r.get("driver")
    need(isinstance(b, dict) and b.get("file") == DRIVER_REL and b.get("tracked") is True and re.fullmatch(r"[0-9a-f]{64}", str(b.get("sha256"))), "driver must hold the tracked dry-run script %s with its sha256" % DRIVER_REL)
    if root is not None:
        p = Path(root) / DRIVER_REL
        need(p.is_file() and sha(p) == b["sha256"], "the driver file must exist and match its recorded sha256")
        src = p.read_text(encoding="utf-8")
        need(not foreign_hits(src) and not write_hits(src), "the driver names no other firm's place and holds no write call (hits %s %s)" % (foreign_hits(src), write_hits(src)))


def check_all(root):
    check_contract(root)
    check_module(root)
    check_tests(root)
    r = load(root, REC_REL)
    check_record(r, root)
    w = r["windows"]
    print("OK: contract household_return_daily (%d columns, schema hash recomputed); compute_household_returns equals the checker's own computation on the synthetic week (deposit, missing account, joining account) and the control computations disagree; tests pass; tie-out over %d households: %s; %d one-account households equal their account"
          % (len(COLUMNS), r["households"]["total"], ", ".join("%s %d of %d within range" % (k, w[k]["within_range"], w[k]["households_compared"]) for k in WINDOWS), r["one_account_households"]["compared"]))


# ---------------------------------------------------------------- self-test
def good_record():
    win = {"households_compared": 10, "within_range": 8, "outside_range": 2, "bins": {"lt_5bp": 1, "5_25bp": 1, "25_100bp": 0, "ge_100bp": 0}, "not_comparable": 3,
           "not_comparable_reasons": {"household_return_none": 2, "no_account_complete": 1}, "claim": "measured"}
    return {"method": {"words": "the household daily return chained over days", "claim": "measured"}, "tolerance_assumed": None,
            "households": {"total": 20, "accounts_total": 50, "multi_account": 12, "claim": "measured"}, "windows": {k: json.loads(json.dumps(win)) for k in WINDOWS},
            "one_account_households": {"compared": 8, "max_abs_gap": 0.0, "claim": "measured"},
            "dry_run": {"first_date": "2025-01-02", "last_date": "2026-10-13", "partitions_read": 200, "table_rows": 4000, "table_sha256": "a" * 64, "claim": "measured"},
            "reads": {"vendor_calls": 0, "s3_writes": 0, "dynamodb_writes": 0, "secret_reads": 0, "s3_reads": 205},
            "files_in_repo": False, "served_values_changed": False, "pushed": False, "deployed": False,
            "driver": {"file": DRIVER_REL, "sha256": "b" * 64, "tracked": True}}


def selftest():
    arms = []

    def ok(name, cond):
        arms.append(name)
        if not cond:
            raise Fail("self-test arm failed: " + name)

    def refuses(name, mutate):
        r = good_record()
        mutate(r)
        try:
            check_record(r)
        except Fail:
            arms.append(name)
            return
        raise Fail("self-test arm failed (accepted): " + name)
    rows, mem = synthetic()
    e = expected(rows, mem)
    by = {(x["household_id"], x["business_date"]): x for x in e}
    ok("first date is NO_PRIOR_VALUE", by[("H1", "2026-01-05")]["day_quality"] == "NO_PRIOR_VALUE" and by[("H1", "2026-01-05")]["total_return_daily"] is None)
    ok("joining account B is outside S on its first day", abs(by[("H1", "2026-01-07")]["total_return_daily"] - (1020.0 / 1010.0 - 1.0)) < EPS and by[("H1", "2026-01-07")]["accounts_n"] == 2)
    ok("the day after a joiner uses both accounts as the base", abs(by[("H1", "2026-01-08")]["total_return_daily"] - ((2040.0 + 505.0 - 1000.0) / (1020.0 + 500.0) - 1.0)) < EPS)
    ok("a missing account makes the day ACCOUNT_MISSING and None", by[("H1", "2026-01-09")]["day_quality"] == "ACCOUNT_MISSING" and by[("H1", "2026-01-09")]["total_return_daily"] is None)
    ok("an account that returns after a gap is outside S on its return day", abs(by[("H1", "2026-01-12")]["total_return_daily"] - (2070.0 / 2060.0 - 1.0)) < EPS)
    ok("a one-account household equals its account", abs(by[("H2", "2026-01-06")]["total_return_daily"] - (297.0 / 300.0 - 1.0)) < EPS)
    ok("the ignore-flows mutant disagrees", same_rows(e, expected(rows, mem, flows=False)) is not None)
    ok("the missing-as-zero mutant disagrees", same_rows(e, expected(rows, mem, missing_as_zero=True)) is not None)
    ok("same_rows is quiet on equal rows", same_rows(e, json.loads(json.dumps(e))) is None)
    ok("schema hash is stable", schema_hash(COLUMNS) == schema_hash(list(reversed(COLUMNS))))
    ok("foreign and write token scans", foreign_hits("x = 'Cottonwood'") == ["cottonwood"] and write_hits("s3.put_object(") == ["put_object"] and foreign_hits("pure") == [])
    check_record(good_record())
    arms.append("a good record passes")
    refuses("bins that do not sum to outside_range", lambda r: r["windows"]["qtd"]["bins"].update({"lt_5bp": 5}))
    refuses("within plus outside not equal to compared", lambda r: r["windows"]["ytd"].update({"within_range": 9}))
    refuses("a one-account household that does not equal its account", lambda r: r["one_account_households"].update({"max_abs_gap": 0.01}))
    refuses("no one-account household compared", lambda r: r["one_account_households"].update({"compared": 0}))
    refuses("a tolerance assumed", lambda r: r.update({"tolerance_assumed": 0.001}))
    refuses("a claim outside the four words", lambda r: r["windows"]["qtd"].update({"claim": "guessed"}))
    refuses("a missing window", lambda r: r["windows"].pop("since_inception"))
    refuses("a write count above zero", lambda r: r["reads"].update({"s3_writes": 1}))
    refuses("a long digit run", lambda r: r["method"].update({"words": "household 12345678901 returned"}))
    refuses("not comparable reasons that do not sum", lambda r: r["windows"]["last_12_months"]["not_comparable_reasons"].update({"x": 5}))
    print("SELFTEST OK: %d arms: %s" % (len(arms), "; ".join(arms)))


CHECKS = {"DB111-1-AC1": check_all}


def main(argv):
    if len(argv) >= 2 and argv[1] == "--selftest":
        selftest()
        return 0
    if len(argv) != 3 or argv[2] not in CHECKS:
        print("usage: p111_household.py <repo_root> <%s>" % "|".join(CHECKS))
        return 2
    root, cid = Path(argv[1]).resolve(), argv[2]
    try:
        CHECKS[cid](root)
    except Fail as e:
        print("FAIL: %s" % e)
        print("%s FAIL" % cid)
        return 1
    except Exception as e:
        print("FAIL: %s: %s" % (type(e).__name__, e))
        print("%s FAIL" % cid)
        return 1
    print("%s PASS" % cid)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
