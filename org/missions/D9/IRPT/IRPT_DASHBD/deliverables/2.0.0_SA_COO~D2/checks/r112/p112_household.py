"""IRPT_DASHBD round 112 (issuer 2.0.0_SA_COO~D2) -- the household window rule and the household-None cause read (CTO ROUND-112 ANALYSIS cells 1 and 2).

  DB112-1-AC1 (~182)  the SOURCE_BREAK rule for household windows: `household_window_result` in the round-111 module, its tests, the contract's window_rule, a driver over all
                      households and the four windows, and HOUSEHOLD_WINDOWS_R112.json whose class counts the checker RECOMPUTES from the private round-111 table.
  DB112-2-AC1 (~183)  the household-None cause read: RD_HOUSEHOLD_NONE_CAUSE_R112.json (form, internal consistency, and its households_none per window recounted from the same table).

The checker imports the worker's module by path and runs it on a synthetic arm against ITS OWN independent computation (built on round 111's `expected`); a fill-in mutant (a figure over a
gap) must disagree. Offline except the private parquet; stdlib and pyarrow; terminates in seconds.

Usage: python -I <this file> <repo_root> <criterion_id>      prints "<id> PASS" or "<id> FAIL" last
       python -I <this file> --selftest [<repo_root>]          the pure helpers on synthetic arms (and a recount of the private table)
"""
import bisect
import datetime as dt
import importlib.util
import inspect
import json
import re
import subprocess
import sys
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent


def load_path(name, path):
    spec = importlib.util.spec_from_file_location(name, str(path))
    mod = importlib.util.module_from_spec(spec)
    sys.modules[name] = mod
    spec.loader.exec_module(mod)
    return mod


P11 = load_path("p111_household_for_112", HERE.parent / "r111" / "p111_household.py")
Fail = P11.Fail
need, nes, is_int, is_num = P11.need, P11.nes, P11.is_int, P11.is_num
D = P11.D
MODULE_REL, CONTRACT_REL, TEST_REL = P11.MODULE_REL, P11.CONTRACT_REL, P11.TEST_REL
REC1_REL = D + "0.9.0_WK_IRPT_DASHBD~182/HOUSEHOLD_WINDOWS_R112.json"
DRIVER1_REL = D + "0.9.0_WK_IRPT_DASHBD~182/dry_run_household_windows_r112.py"
REC2_REL = D + "0.9.0_WK_IRPT_DASHBD~183/RD_HOUSEHOLD_NONE_CAUSE_R112.json"
TABLE = "C:/dev/_irpt_private_evidence_20261009/IRPT_DASHBD/0.9.0_WK_IRPT_DASHBD~179/household_return_daily.parquet"
WINDOWS = P11.WINDOWS
CLAIMS = P11.CLAIMS
SIG = ["rows", "membership", "household_id", "opening_anchor", "as_of", "table_days"]
W_ACCOUNT = "Account %d of %d has no measured return on %s in this period, so the household return for this period is not shown."
W_NOROW = "The household has no row on %s in this period, so the household return for this period is not shown."
W_INSUF = "This household did not exist at the start of this period."
FORMS = {"source_break_account": "Account <k> of <N> has no measured return on <days> in this period, so the household return for this period is not shown.",
         "source_break_household_no_row": "The household has no row on <days> in this period, so the household return for this period is not shown.",
         "insufficient_history": W_INSUF}
KINDS2 = ("account_closed_before_as_of", "account_null_return", "account_row_missing_inside_life", "household_no_row")
ISO = re.compile(r"\d{4}-\d{2}-\d{2}")
EPS = 1e-9


def days_words(n):
    return "1 day" if n == 1 else "%d days" % n


# ---------------------------------------------------------------- THE RULE, independently of the worker's module
def expected_window(rows, membership, hid, anchor, as_of, table_days, fillin=False):
    """the household window result by the rule of the order, built on round 111's own `expected` daily computation (not on the worker's module).
    fillin=True is a CONTROL: it returns a figure over the measured days of a window that holds a gap, which the rule forbids."""
    daily = [x for x in P11.expected(rows, membership) if x["household_id"] == hid]
    by = {x["business_date"]: x for x in daily}
    have = {(r["account_id"], r["business_date"]): r for r in rows if membership.get(r["account_id"]) == hid}
    accts = sorted({a for a, _d in have})
    pos = {a: i + 1 for i, a in enumerate(accts)}
    dates = sorted(by)
    first = dates[0]
    if anchor is not None and first > anchor:
        return {"figure": None, "absent": {"absent": W_INSUF, "kind": "INSUFFICIENT_HISTORY"}, "unmeasured": {}, "days_in_window": 0}
    lo = anchor if anchor is not None else first
    days = [d for d in table_days if lo < d <= as_of]
    unmeasured, norow, prod, mprod = {}, 0, 1.0, 1.0
    for d in days:
        if d not in by:
            norow += 1
            continue
        x = by[d]
        if x["day_quality"] != "MEASURED":
            prev = dates[dates.index(d) - 1]
            named = [a for a in accts if (a, prev) in have and ((a, d) not in have or have[(a, d)].get("total_return_daily") is None)]
            if not named:
                named = [a for a in accts if (a, prev) in have]
            for a in named:
                unmeasured[pos[a]] = unmeasured.get(pos[a], 0) + 1
            continue
        prod *= 1.0 + x["total_return_daily"]
        mprod *= 1.0 + x["total_return_daily"]
    if unmeasured:
        k = min(unmeasured, key=lambda i: (-unmeasured[i], i))
        absent = {"absent": W_ACCOUNT % (k, len(accts), days_words(unmeasured[k])), "kind": "SOURCE_BREAK"}
        fig = 100.0 * (mprod - 1.0) if fillin else None
        return {"figure": fig, "absent": None if fillin else absent, "unmeasured": unmeasured, "days_in_window": len(days)}
    if norow:
        absent = {"absent": W_NOROW % days_words(norow), "kind": "SOURCE_BREAK"}
        fig = 100.0 * (mprod - 1.0) if fillin else None
        return {"figure": fig, "absent": None if fillin else absent, "unmeasured": {}, "days_in_window": len(days)}
    return {"figure": 100.0 * (prod - 1.0), "absent": None, "unmeasured": {}, "days_in_window": len(days)}


def same_result(a, b):
    """None if equal (figure within 1e-9 percent points, absent exactly, unmeasured exactly, days), else the first difference in words."""
    if not isinstance(b, dict) or set(b.keys()) != {"figure", "absent", "unmeasured", "days_in_window"}:
        return "the result keys are not exactly figure, absent, unmeasured, days_in_window"
    fa, fb = a["figure"], b["figure"]
    if (fa is None) != (fb is None) or (fa is not None and (not is_num(fb) or abs(fa - fb) > EPS)):
        return "figure differs (%r against %r)" % (fa, fb)
    if a["absent"] != b["absent"]:
        return "absent differs (%r against %r)" % (a["absent"], b["absent"])
    ub = b["unmeasured"]
    if not isinstance(ub, dict) or {int(k): v for k, v in ub.items()} != a["unmeasured"]:
        return "unmeasured differs (%r against %r)" % (a["unmeasured"], ub)
    if a["days_in_window"] != b["days_in_window"]:
        return "days_in_window differs (%r against %r)" % (a["days_in_window"], b["days_in_window"])
    return None


def synthetic():
    """round 111's arm (H1 two accounts with a missing day, H2 one account with a linked day) plus H3 (a day on which the household has no row) and H4 (two accounts, both
    unmeasured on two days: a tie, and a plural)."""
    rows, mem = P11.synthetic()
    rows = [dict(r) for r in rows]
    mem = dict(mem)
    d = ["2026-01-05", "2026-01-06", "2026-01-07", "2026-01-08", "2026-01-09", "2026-01-12"]
    for i in (0, 1, 3, 4, 5):
        rows.append({"account_id": "E", "business_date": d[i], "market_value_eod": 200.0 + i, "external_flow": 0.0, "total_return_daily": None if i == 0 else 0.001 * i})
    mem["E"] = "H3"
    for a in ("F", "G"):
        for i in range(6):
            r = None if i in (0, 3, 4) else 0.001 * (i + 1)
            rows.append({"account_id": a, "business_date": d[i], "market_value_eod": 100.0, "external_flow": 0.0, "total_return_daily": r})
        mem[a] = "H4"
    return rows, mem, d


# ---------------------------------------------------------------- the module
def load_module_at(path, name="household_return_daily_under_check_112"):
    p = Path(path)
    need(p.is_file(), "no %s" % p)
    src = p.read_text(encoding="utf-8")
    need(not P11.foreign_hits(src) and not P11.write_hits(src) and "boto3" not in src, "the module is a pure function: no other firm's place, no write call, no boto3")
    return load_path(name, p), src


def check_function(mod):
    f = getattr(mod, "household_window_result", None)
    need(callable(f), "the module must define household_window_result(rows, membership, household_id, opening_anchor, as_of, table_days)")
    need(list(inspect.signature(f).parameters) == SIG, "household_window_result's parameters must be exactly %s" % SIG)
    rows, mem, d = synthetic()
    td = list(d)

    def run(hid, anchor, as_of):
        return f(json.loads(json.dumps(rows)), dict(mem), hid, anchor, as_of, list(td))
    cases = (("H1", d[0], d[5], "a planted account gap"), ("H1", d[0], d[3], "a window before the gap"), ("H1", "2026-01-04", d[5], "a household that began after the anchor"),
             ("H2", d[0], d[5], "a one-account household with a linked day"), ("H3", d[0], d[3], "a day with no household row"), ("H4", d[0], d[5], "a tie of two accounts over two days"),
             ("H1", None, d[5], "the since-inception window"))
    for hid, anchor, as_of, why in cases:
        want = expected_window(rows, mem, hid, anchor, as_of, td)
        got = run(hid, anchor, as_of)
        diff = same_result(want, got)
        need(diff is None, "household_window_result disagrees with the checker's own computation on %s: %s" % (why, diff))
    gap = run("H1", d[0], d[5])
    need(gap["figure"] is None and gap["absent"] == {"absent": W_ACCOUNT % (2, 2, "1 day"), "kind": "SOURCE_BREAK"}, "a planted account gap must render the words, not a figure: 'Account 2 of 2 has no measured return on 1 day in this period, ...'")
    tie = run("H4", d[0], d[5])
    need(tie["absent"] and tie["absent"]["absent"] == W_ACCOUNT % (1, 2, "2 days") and tie["unmeasured"] == {1: 2, 2: 2}, "a tie names the lowest position and the plural '2 days'")
    nr = run("H3", d[0], d[3])
    need(nr["absent"] and nr["absent"]["absent"] == W_NOROW % "1 day", "a day with no household row reads 'The household has no row on 1 day in this period, ...'")
    ih = run("H1", "2026-01-04", d[5])
    need(ih["figure"] is None and ih["absent"] == {"absent": W_INSUF, "kind": "INSUFFICIENT_HISTORY"}, "a household that began after the anchor reads INSUFFICIENT_HISTORY with its words")
    for hid, anchor, as_of in (("H1", d[0], d[5]), ("H4", d[0], d[5]), ("H3", d[0], d[3])):
        fill = expected_window(rows, mem, hid, anchor, as_of, td, fillin=True)
        need(fill["figure"] is not None, "CONTROL: the fill-in computation returned no figure over a gap (the arm does not exercise it)")
        need(same_result(fill, run(hid, anchor, as_of)) is not None, "CONTROL: the fill-in computation agrees with the module over a gap")
    ok = run("H1", d[0], d[3])
    need(ok["figure"] is not None and ok["absent"] is None, "a window without a gap must return a figure and no absent form")
    own = run("H2", d[0], d[5])
    need(own["absent"] is None and own["figure"] is not None, "a one-account household with a linked day returns a figure")


# ---------------------------------------------------------------- the private round-111 table, recounted
def one_year_before(x):
    try:
        return x.replace(year=x.year - 1)
    except ValueError:
        return x.replace(year=x.year - 1, day=28)


def window_start(name, as_of):
    if name == "qtd":
        return dt.date(as_of.year, 3 * ((as_of.month - 1) // 3) + 1, 1)
    if name == "ytd":
        return dt.date(as_of.year, 1, 1)
    if name == "last_12_months":
        return one_year_before(as_of)
    raise Fail("no start rule for window %s" % name)


def load_table():
    need(Path(TABLE).is_file(), "the private round-111 household table is missing: %s" % TABLE)
    import pyarrow.parquet as pq
    d = pq.read_table(TABLE, columns=["household_id", "business_date", "total_return_daily", "day_quality"]).to_pydict()
    return d


def recount(table=None):
    """per window: households_total, figure, source_break_account, source_break_household_no_row, insufficient_history, from the table alone (window days = the table's own dates)."""
    d = table if table is not None else load_table()
    by, bad = {}, {}
    for h, t, r, q in zip(d["household_id"], d["business_date"], d["total_return_daily"], d["day_quality"]):
        by.setdefault(h, []).append(t)
        if r is None or q != "MEASURED":
            bad.setdefault(h, []).append(t)
    days = sorted(set(d["business_date"]))
    as_of = days[-1]
    a_date = dt.date.fromisoformat(as_of)
    out = {}
    for w in WINDOWS:
        if w == "since_inception":
            anchor = None
        else:
            start = window_start(w, a_date).isoformat()
            before = [x for x in days if x < start]
            anchor = before[-1] if before else "0000-00-00"
        c = {"households_total": len(by), "figure": 0, "source_break_account": 0, "source_break_household_no_row": 0, "insufficient_history": 0}
        for h, hd in by.items():
            hd.sort()
            first = hd[0]
            if anchor is not None and first > anchor:
                c["insufficient_history"] += 1
                continue
            lo = anchor if anchor is not None else first
            n_wd = bisect.bisect_right(days, as_of) - bisect.bisect_right(days, lo)
            n_h = bisect.bisect_right(hd, as_of) - bisect.bisect_right(hd, lo)
            b = sorted(bad.get(h, []))
            n_b = bisect.bisect_right(b, as_of) - bisect.bisect_right(b, lo)
            if n_b > 0:
                c["source_break_account"] += 1
            elif n_h < n_wd:
                c["source_break_household_no_row"] += 1
            else:
                c["figure"] += 1
        out[w] = c
    return as_of, out, d


# ---------------------------------------------------------------- DB112-1-AC1
def check_contract_window_rule(root):
    c = P11.check_contract(root)
    wr = str(c.get("window_rule") or "")
    need("SOURCE_BREAK" in wr and "INSUFFICIENT_HISTORY" in wr and "no imputation" in wr.lower() and "household_window_result" in wr,
         "the contract must carry a `window_rule` text that names SOURCE_BREAK, INSUFFICIENT_HISTORY, 'no imputation' and household_window_result")
    return c


def check_record1(r, root=None, counts=None):
    need(isinstance(r, dict), "the record is not an object")
    need(r.get("as_of") == "2026-10-13", "as_of must be 2026-10-13: the driver reads only the partitions dated on or before it, so its table equals round 111's")
    w = r.get("windows")
    need(isinstance(w, dict) and set(w.keys()) == set(WINDOWS), "windows must be keyed exactly %s" % list(WINDOWS))
    for k in WINDOWS:
        x = w[k]
        need(isinstance(x, dict) and x.get("claim") in CLAIMS, "windows.%s must carry a claim" % k)
        for f in ("households_total", "figure", "source_break", "source_break_account", "source_break_household_no_row", "insufficient_history"):
            need(is_int(x.get(f)) and x[f] >= 0, "windows.%s.%s must be a non-negative integer" % (k, f))
        need(x["source_break"] == x["source_break_account"] + x["source_break_household_no_row"], "windows.%s: source_break must equal the account plus the household_no_row counts" % k)
        need(x["figure"] + x["source_break"] + x["insufficient_history"] == x["households_total"], "windows.%s: figure, source_break and insufficient_history must partition households_total" % k)
    need(r.get("words_forms") == FORMS, "words_forms must equal the three forms of the order exactly (%s)" % json.dumps(FORMS))
    need(r.get("table_matches_round111") is True and r.get("table_rows_differing") == 0, "table_matches_round111 must be true with table_rows_differing 0: the recount of the checker reads round 111's private table")
    rd = r.get("reads")
    need(isinstance(rd, dict) and all(rd.get(k) == 0 for k in ("vendor_calls", "s3_writes", "dynamodb_writes", "secret_reads")) and is_int(rd.get("s3_reads")) and rd["s3_reads"] >= 1, "reads: zero writes, vendor calls and secret reads; s3_reads a positive integer")
    need(r.get("files_in_repo") is False and r.get("served_values_changed") is False and r.get("pushed") is False and r.get("deployed") is False, "files_in_repo, served_values_changed, pushed and deployed must be false")
    need(not P11.digit_runs(r), "the record holds a run of 8 or more digits outside a hash, path, file, key, where or vintage field: %s" % P11.digit_runs(r))
    b = r.get("driver")
    need(isinstance(b, dict) and b.get("file") == DRIVER1_REL and b.get("tracked") is True and re.fullmatch(r"[0-9a-f]{64}", str(b.get("sha256"))), "driver must hold the tracked dry-run script %s with its sha256" % DRIVER1_REL)
    if root is not None:
        p = Path(root) / DRIVER1_REL
        need(p.is_file() and P11.sha(p) == b["sha256"], "the driver file must exist and match its recorded sha256")
        src = p.read_text(encoding="utf-8")
        need(not P11.foreign_hits(src) and not P11.write_hits(src), "the driver names no other firm's place and holds no write call (hits %s %s)" % (P11.foreign_hits(src), P11.write_hits(src)))
    if counts is not None:
        for k in WINDOWS:
            c, x = counts[k], w[k]
            want = {"households_total": c["households_total"], "figure": c["figure"], "source_break_account": c["source_break_account"],
                    "source_break_household_no_row": c["source_break_household_no_row"], "insufficient_history": c["insufficient_history"]}
            got = {f: x[f] for f in want}
            need(got == want, "windows.%s: the class counts must equal the checker's recount of the round-111 table %s (the record says %s)" % (k, want, got))


def check_tests(root):
    p = Path(root) / TEST_REL
    need(p.is_file(), "no %s" % TEST_REL)
    src = p.read_text(encoding="utf-8")
    need(len(re.findall(r"^\s*def test_", src, re.M)) >= 8 and "household_window_result" in src, "the test file holds at least 8 tests and exercises household_window_result (a planted gap, a clean window, a late household, a no-row day, a fill-in mutant)")
    g = subprocess.run([sys.executable, "-m", "pytest", "-q", "-p", "no:cacheprovider", str(p)], cwd=str(root), capture_output=True, text=True, timeout=100)
    need(g.returncode == 0, "the tests do not pass: %s" % (g.stdout.strip().splitlines() or ["no output"])[-1][:200])


def check_all_1(root):
    check_contract_window_rule(root)
    P11.check_module(root)
    mod, _src = load_module_at(Path(root) / MODULE_REL)
    check_function(mod)
    check_tests(root)
    r = P11.load(root, REC1_REL)
    as_of, counts, _d = recount()
    check_record1(r, root, counts)
    w = r["windows"]
    print("OK: window rule in the contract; household_window_result equals the checker's own computation on the synthetic arm (planted gap, tie, no-row day, late household) and the fill-in control disagrees; tests pass; %s"
          % "; ".join("%s: %d figure, %d source_break, %d insufficient_history of %d" % (k, w[k]["figure"], w[k]["source_break"], w[k]["insufficient_history"], w[k]["households_total"]) for k in WINDOWS))


# ---------------------------------------------------------------- DB112-2-AC1
def check_record2(r, counts=None, table=None, root=None):
    need(isinstance(r, dict), "the record is not an object")
    need(r.get("as_of") == "2026-10-13", "as_of must be 2026-10-13")
    w = r.get("windows")
    need(isinstance(w, dict) and set(w.keys()) == set(WINDOWS), "windows must be keyed exactly %s" % list(WINDOWS))
    for k in WINDOWS:
        x = w[k]
        need(isinstance(x, dict) and x.get("claim") in CLAIMS and is_int(x.get("households_none")) and x["households_none"] >= 0, "windows.%s must hold households_none (an integer) and a claim" % k)
        bk = x.get("by_kind")
        need(isinstance(bk, dict) and set(bk.keys()) == set(KINDS2) and all(is_int(v) and v >= 0 for v in bk.values()), "windows.%s.by_kind must hold %s as non-negative integers" % (k, list(KINDS2)))
        need(sum(bk.values()) == x["households_none"], "windows.%s: by_kind must sum to households_none" % k)
        td = x.get("top_dates")
        need(isinstance(td, list) and len(td) <= 10 and all(isinstance(e, dict) and ISO.fullmatch(str(e.get("date"))) and is_int(e.get("households_affected")) and e["households_affected"] >= 1 for e in td), "windows.%s.top_dates must be at most 10 {date ISO, households_affected >= 1}" % k)
        need([e["households_affected"] for e in td] == sorted((e["households_affected"] for e in td), reverse=True), "windows.%s.top_dates must be sorted by households_affected, largest first" % k)
        need(all(e["date"] <= r["as_of"] for e in td), "windows.%s.top_dates: a date after as_of" % k)
    u = r.get("unmeasured_account_days")
    need(isinstance(u, dict) and is_int(u.get("total")) and u["total"] >= 0 and isinstance(u.get("by_day_quality"), dict) and u["by_day_quality"] and all(nes(k) and is_int(v) and v >= 0 for k, v in u["by_day_quality"].items()), "unmeasured_account_days must hold total and by_day_quality (a non-empty object of counts)")
    need(sum(u["by_day_quality"].values()) == u["total"], "unmeasured_account_days.by_day_quality must sum to total (a pair with no row at all is counted under NO_ROW)")
    cs = r.get("cause_by_source")
    need(isinstance(cs, list) and cs and all(isinstance(e, dict) and nes(e.get("cause")) and nes(e.get("producer")) and is_int(e.get("count")) and e["count"] >= 0 and e.get("claim") in CLAIMS for e in cs), "cause_by_source must list at least one {cause, producer, count, claim}")
    if root is not None:
        for e in cs:
            need((Path(root) / e["producer"]).exists(), "cause_by_source.producer %s must be a path that exists at this checkout" % e["producer"])
    dn = r.get("denominator")
    need(isinstance(dn, dict) and all(is_int(dn.get(k)) and dn[k] >= 1 for k in ("households", "accounts", "partitions_read")) and dn["accounts"] >= dn["households"], "denominator must hold households, accounts (at least households) and partitions_read, positive integers")
    pc = r.get("positive_control")
    need(isinstance(pc, dict) and nes(pc.get("description")) and nes(pc.get("expected")) and nes(pc.get("observed")) and pc.get("passed") is True, "positive_control must hold description, expected, observed and passed true")
    rd = r.get("reads")
    need(isinstance(rd, dict) and all(rd.get(k) == 0 for k in ("vendor_calls", "s3_writes", "dynamodb_writes", "secret_reads")) and is_int(rd.get("s3_reads")), "reads: zero writes, vendor calls and secret reads; s3_reads an integer")
    need(r.get("files_in_repo") is False and r.get("served_values_changed") is False and r.get("pushed") is False and r.get("deployed") is False, "files_in_repo, served_values_changed, pushed and deployed must be false")
    need(not P11.digit_runs(r), "the record holds a run of 8 or more digits outside a hash, path, file, key, where or vintage field: %s" % P11.digit_runs(r))
    if counts is not None and table is not None:
        for k in WINDOWS:
            want = counts[k]["source_break_account"] + counts[k]["source_break_household_no_row"]
            need(w[k]["households_none"] == want, "windows.%s.households_none must equal the checker's recount of the source_break households of the round-111 table (%d; the record says %d)" % (k, want, w[k]["households_none"]))
        n_am = sum(1 for q in table["day_quality"] if q == "ACCOUNT_MISSING")
        need(u["total"] >= n_am, "unmeasured_account_days.total (%d) cannot be below the %d ACCOUNT_MISSING household days of the table (each has at least one unmeasured account)" % (u["total"], n_am))
        need(dn["households"] == len(set(table["household_id"])), "denominator.households must equal the %d households of the round-111 table" % len(set(table["household_id"])))


def check_all_2(root):
    r = P11.load(root, REC2_REL)
    as_of, counts, table = recount()
    check_record2(r, counts, table, root)
    w = r["windows"]
    print("OK: the household-None cause read: %s; unmeasured account days %d; %d cause(s) by source; positive control passed"
          % ("; ".join("%s %d households" % (k, w[k]["households_none"]) for k in WINDOWS), r["unmeasured_account_days"]["total"], len(r["cause_by_source"])))


# ---------------------------------------------------------------- self-test
def good_record1():
    win = {"households_total": 20, "figure": 10, "source_break": 6, "source_break_account": 5, "source_break_household_no_row": 1, "insufficient_history": 4, "claim": "measured"}
    return {"as_of": "2026-10-13", "windows": {k: dict(win) for k in WINDOWS}, "words_forms": dict(FORMS), "table_matches_round111": True, "table_rows_differing": 0,
            "reads": {"s3_reads": 580, "s3_writes": 0, "dynamodb_writes": 0, "vendor_calls": 0, "secret_reads": 0},
            "files_in_repo": False, "served_values_changed": False, "pushed": False, "deployed": False, "driver": {"file": DRIVER1_REL, "sha256": "a" * 64, "tracked": True}}


def good_record2():
    win = {"households_none": 6, "by_kind": {"account_closed_before_as_of": 2, "account_null_return": 2, "account_row_missing_inside_life": 1, "household_no_row": 1},
           "top_dates": [{"date": "2026-03-02", "households_affected": 4}, {"date": "2026-02-02", "households_affected": 2}], "claim": "measured"}
    return {"as_of": "2026-10-13", "windows": {k: json.loads(json.dumps(win)) for k in WINDOWS},
            "unmeasured_account_days": {"total": 90, "by_day_quality": {"NO_ROW": 60, "SOURCE_LAG": 30}},
            "cause_by_source": [{"cause": "the account has no row after its last day", "producer": "data/assets/scripts/gold/irpt_reporting/account_return_daily.py", "count": 60, "claim": "measured"}],
            "denominator": {"households": 20, "accounts": 50, "partitions_read": 570}, "positive_control": {"description": "a planted gap", "expected": "found", "observed": "found", "passed": True},
            "reads": {"s3_reads": 580, "s3_writes": 0, "dynamodb_writes": 0, "vendor_calls": 0, "secret_reads": 0},
            "files_in_repo": False, "served_values_changed": False, "pushed": False, "deployed": False}


REFERENCE = '''def household_window_result(rows, membership, household_id, opening_anchor, as_of, table_days):
    return CHECK.expected_window(rows, membership, household_id, opening_anchor, as_of, table_days)
'''


def selftest(root):
    arms = []

    def ok(name, cond):
        arms.append(name)
        if not cond:
            raise Fail("self-test arm failed: " + name)

    def refuses(name, fn, mutate, good):
        r = good()
        mutate(r)
        try:
            fn(r)
        except Fail:
            arms.append(name)
            return
        raise Fail("self-test arm failed (accepted): " + name)
    rows, mem, d = synthetic()
    td = list(d)
    gap = expected_window(rows, mem, "H1", d[0], d[5], td)
    ok("a planted gap gives the words and no figure", gap["figure"] is None and gap["absent"]["absent"] == W_ACCOUNT % (2, 2, "1 day") and gap["unmeasured"] == {2: 1})
    ok("a window before the gap gives a figure", expected_window(rows, mem, "H1", d[0], d[3], td)["figure"] is not None)
    ok("a late household is INSUFFICIENT_HISTORY", expected_window(rows, mem, "H1", "2026-01-04", d[5], td)["absent"]["kind"] == "INSUFFICIENT_HISTORY")
    ok("a tie names the lowest position and the plural", expected_window(rows, mem, "H4", d[0], d[5], td)["absent"]["absent"] == W_ACCOUNT % (1, 2, "2 days"))
    ok("a no-row day gives the household words", expected_window(rows, mem, "H3", d[0], d[3], td)["absent"]["absent"] == W_NOROW % "1 day")
    crets = [r["total_return_daily"] for r in sorted(rows, key=lambda r: r["business_date"]) if r["account_id"] == "C" and r["business_date"] > d[0]]
    prod = 1.0
    for x in crets:
        prod *= 1.0 + x
    ok("a one-account household equals the product of its account's own returns (incl. the linked day)", abs(expected_window(rows, mem, "H2", d[0], d[5], td)["figure"] - 100.0 * (prod - 1.0)) < 1e-9)
    fill = expected_window(rows, mem, "H1", d[0], d[5], td, fillin=True)
    ok("the fill-in control returns a figure over the gap and disagrees", fill["figure"] is not None and same_result(fill, gap) is not None)
    ok("same_result is quiet on equal results", same_result(gap, json.loads(json.dumps({"figure": gap["figure"], "absent": gap["absent"], "unmeasured": {str(k): v for k, v in gap["unmeasured"].items()}, "days_in_window": gap["days_in_window"]}))) is None)
    # the module check on a scratch reference module and on a fill-in mutant
    tmp = Path(tempfile.mkdtemp(prefix="p112_selftest_"))
    here = Path(__file__).resolve()
    ref = tmp / "ref_module.py"
    ref.write_text("import importlib.util, sys\nspec = importlib.util.spec_from_file_location('p112_for_ref', %r)\nCHECK = importlib.util.module_from_spec(spec)\nsys.modules['p112_for_ref'] = CHECK\nspec.loader.exec_module(CHECK)\n" % str(here) + REFERENCE, encoding="utf-8")
    mod, _s = load_module_at(ref, "p112_ref_module")
    check_function(mod)
    arms.append("a reference implementation passes the function checks")
    mut = tmp / "mut_module.py"
    mut.write_text(ref.read_text(encoding="utf-8").replace("return CHECK.expected_window(rows, membership, household_id, opening_anchor, as_of, table_days)", "return CHECK.expected_window(rows, membership, household_id, opening_anchor, as_of, table_days, fillin=True)"), encoding="utf-8")
    mod2, _s2 = load_module_at(mut, "p112_mut_module")
    try:
        check_function(mod2)
    except Fail:
        arms.append("a fill-in mutant is refused")
    else:
        raise Fail("self-test arm failed (accepted): a fill-in mutant")
    check_record1(good_record1())
    arms.append("a good record 1 passes")
    refuses("a record 1 whose classes do not partition", check_record1, lambda r: r["windows"]["qtd"].update({"figure": 11}), good_record1)
    refuses("a record 1 whose source_break is not the sum", check_record1, lambda r: r["windows"]["ytd"].update({"source_break": 7}), good_record1)
    refuses("a record 1 with a changed words form", check_record1, lambda r: r["words_forms"].update({"insufficient_history": "x"}), good_record1)
    refuses("a record 1 whose table differs from round 111", check_record1, lambda r: r.update({"table_rows_differing": 3}), good_record1)
    refuses("a record 1 with the wrong as_of", check_record1, lambda r: r.update({"as_of": "2026-10-14"}), good_record1)
    refuses("a record 1 with a write", check_record1, lambda r: r["reads"].update({"s3_writes": 1}), good_record1)
    refuses("a record 1 with a long digit run", check_record1, lambda r: r.update({"note": "household 12345678901"}), good_record1)
    check_record2(good_record2())
    arms.append("a good record 2 passes")
    refuses("a record 2 whose kinds do not sum", check_record2, lambda r: r["windows"]["qtd"]["by_kind"].update({"household_no_row": 5}), good_record2)
    refuses("a record 2 with unsorted top dates", check_record2, lambda r: r["windows"]["qtd"].update({"top_dates": [{"date": "2026-03-02", "households_affected": 1}, {"date": "2026-02-02", "households_affected": 3}]}), good_record2)
    refuses("a record 2 with a quality breakdown that does not sum", check_record2, lambda r: r["unmeasured_account_days"].update({"total": 91}), good_record2)
    refuses("a record 2 with no cause", check_record2, lambda r: r.update({"cause_by_source": []}), good_record2)
    refuses("a record 2 with a failed positive control", check_record2, lambda r: r["positive_control"].update({"passed": False}), good_record2)
    refuses("a record 2 with a claim outside the four words", check_record2, lambda r: r["windows"]["ytd"].update({"claim": "guessed"}), good_record2)
    if Path(TABLE).is_file():
        as_of, counts, _t = recount()
        ok("the recount partitions the households and reads as_of 2026-10-13", as_of == "2026-10-13" and all(sum(v[f] for f in ("figure", "source_break_account", "source_break_household_no_row", "insufficient_history")) == v["households_total"] for v in counts.values()))
        arms.append("recount: " + "; ".join("%s %d/%d/%d/%d" % (k, counts[k]["figure"], counts[k]["source_break_account"], counts[k]["source_break_household_no_row"], counts[k]["insufficient_history"]) for k in WINDOWS))
    print("SELFTEST OK: %d arms: %s" % (len(arms), "; ".join(arms)))


CHECKS = {"DB112-1-AC1": check_all_1, "DB112-2-AC1": check_all_2}


def main(argv):
    if len(argv) >= 2 and argv[1] == "--selftest":
        selftest(Path(argv[2] if len(argv) > 2 else ".").resolve())
        return 0
    if len(argv) != 3 or argv[2] not in CHECKS:
        print("usage: p112_household.py <repo_root> <%s>" % "|".join(CHECKS))
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
