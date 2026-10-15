"""IRPT_DASHBD round 123, workstream B-IN (issuer 2.0.0_SA_COO~I2) -- the Scope feed adapter (cell DB-i-10).

The adapter turns the Scope feed's silver rows (calendar days, daily factor, RETURNED / ABSENT) into rows of
account_return_daily 0.4.0 (org/standards/IRPT_DASHBD_ACCOUNT_RETURN_DAILY_CONTRACT.json): the CTO's round-118 ADDENDUM 4
rules and the contract's source_rules.orion. Every case below is SYNTHETIC: no real account, no client value, no real date.

  DBI123-1-AC1  the golden cases: trading-day compounding, an ABSENT trading day stays ABSENT, leading days skipped, an
                interior gap, UNMAPPED_ACCOUNT, SERIES_ENDED_AT_SOURCE, the EOD value rule, carried_days, the manifest counts.
  DBI123-1-AC2  every output row passes ~D2's contract validator (driven by the contract file's declarations), carries the
                contract's columns exactly, and the adapter refuses a gross-of-fees row and an unsorted calendar.
  DBI123-1-AC3  the worker's own test file runs green under pytest with at least 10 tests, and names a mutant test.

Usage: python -I <this file> <repo_root> <criterion_id>      prints "<id> PASS" or "<id> FAIL" last
       python -I <this file> --selftest [<repo_root>]         the golden expectations against a naive (no compounding) reference
"""
import importlib.util
import math
import re
import subprocess
import sys
from pathlib import Path

ADAPTER_REL = "data/assets/scripts/gold/irpt_reporting/adapters/inflection_scope_feed_adapter.py"
TEST_REL = "data/assets/scripts/gold/irpt_reporting/tests/test_inflection_scope_feed_adapter.py"
CONTRACT_TEST_REL = "data/assets/scripts/gold/irpt_reporting/tests/test_account_return_contract_040.py"
FIRM = "FIRM-SYNTH"
METHOD = 7
TOL = 1e-12


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


# ---- the synthetic world ------------------------------------------------------------------------------------------
# Calendar days (synthetic): Thu 07-02 trading, Fri 07-03 holiday, Sat 07-04, Sun 07-05, Mon 07-06 trading, 07-07, 07-08 trading.
CAL = ["2026-07-02", "2026-07-03", "2026-07-04", "2026-07-05", "2026-07-06", "2026-07-07", "2026-07-08"]
TRADING = ["2026-07-02", "2026-07-06", "2026-07-07", "2026-07-08"]
MAP = {"1001": "ACCT-A", "1002": "ACCT-B", "1003": "ACCT-C", "1004": "ACCT-D", "1006": "ACCT-F", "1007": "ACCT-G"}  # 1005 unmapped

FA = {"2026-07-02": 1.001, "2026-07-03": 1.002, "2026-07-04": 1.0, "2026-07-05": 1.0, "2026-07-06": 1.003, "2026-07-07": 0.995, "2026-07-08": 1.004}


def ret(acct, day, factor, start, end=None):
    return {"day": day, "account_id": acct, "status": "RETURNED", "reason_class": None, "daily_factor": factor,
            "start_market_value": start, "end_market_value": end, "fee_basis": "NET", "calc_gross_of_fees": False, "source": "orion_scope"}


def absent(acct, day, reason):
    return {"day": day, "account_id": acct, "status": "ABSENT", "reason_class": reason, "daily_factor": None,
            "start_market_value": None, "end_market_value": None, "fee_basis": "NET", "calc_gross_of_fees": False, "source": "orion_scope"}


def feed():
    rows = []
    # A: every day returned; the last day carries end_market_value.
    for i, d in enumerate(CAL):
        rows.append(ret("1001", d, FA[d], 100.0 + i, 999.0 if d == CAL[-1] else None))
    # B: Mon 07-06 is ABSENT (GROUP_NO_SERIES) while the weekend before it is returned; the rest returned.
    for i, d in enumerate(CAL):
        if d == "2026-07-06":
            rows.append(absent("1002", d, "GROUP_NO_SERIES"))
        else:
            rows.append(ret("1002", d, FA[d], 200.0 + i, 888.0 if d == CAL[-1] else None))
    # C: the series starts on Sun 07-05; the days before are ABSENT NO_GROUP (leading).
    for i, d in enumerate(CAL):
        if d < "2026-07-05":
            rows.append(absent("1003", d, "NO_GROUP"))
        else:
            rows.append(ret("1003", d, FA[d], 300.0 + i, 777.0 if d == CAL[-1] else None))
    # D: Sat 07-04 is missing from the feed (an interior gap) while 07-03 and 07-05 are returned.
    for i, d in enumerate(CAL):
        if d != "2026-07-04":
            rows.append(ret("1004", d, FA[d], 400.0 + i, 666.0 if d == CAL[-1] else None))
    # E (1005): unmapped; every day returned.
    for i, d in enumerate(CAL):
        rows.append(ret("1005", d, FA[d], 500.0 + i, 555.0 if d == CAL[-1] else None))
    # F: the series ends after Mon 07-06.
    for i, d in enumerate(CAL):
        if d <= "2026-07-06":
            rows.append(ret("1006", d, FA[d], 600.0 + i))
        else:
            rows.append(absent("1006", d, "SERIES_ENDED_AT_SOURCE"))
    # G: returned every day, but the last day carries no end_market_value (no value to close the day on).
    for i, d in enumerate(CAL):
        rows.append(ret("1007", d, FA[d], 700.0 + i, None))
    return rows


def expected():
    """-> ({(account_id, day): (factor, carried, mv)}, {(orion_id, day): reason}) written by hand from the rules."""
    rows, absents = {}, {}
    # A: eod(t) = start of the next calendar day's row; the last day takes its end_market_value.
    rows[("ACCT-A", "2026-07-02")] = (1.001, 1, 101.0)                       # next row 07-03 start 101.0
    rows[("ACCT-A", "2026-07-06")] = (1.002 * 1.0 * 1.0 * 1.003, 4, 105.0)   # window 07-03..07-06; next row 07-07 start 105.0
    rows[("ACCT-A", "2026-07-07")] = (0.995, 1, 106.0)                       # next row 07-08 start 106.0
    rows[("ACCT-A", "2026-07-08")] = (1.004, 1, 999.0)                       # no next row: end_market_value
    # B: Mon 07-06 stays ABSENT (its own row is absent) although the weekend factors exist; nothing is moved onto it.
    rows[("ACCT-B", "2026-07-02")] = (1.001, 1, 201.0)
    absents[("1002", "2026-07-06")] = "GROUP_NO_SERIES"
    rows[("ACCT-B", "2026-07-07")] = (0.995, 1, 206.0)
    rows[("ACCT-B", "2026-07-08")] = (1.004, 1, 888.0)
    # C: 07-02 own row ABSENT NO_GROUP; Mon 07-06 window 07-03..07-06 with 07-03 and 07-04 before the series start (skipped).
    absents[("1003", "2026-07-02")] = "NO_GROUP"
    rows[("ACCT-C", "2026-07-06")] = (1.0 * 1.003, 2, 305.0)
    rows[("ACCT-C", "2026-07-07")] = (0.995, 1, 306.0)
    rows[("ACCT-C", "2026-07-08")] = (1.004, 1, 777.0)
    # D: Mon 07-06 window has an interior gap (07-04 missing) -> INCOMPLETE_WINDOW.
    rows[("ACCT-D", "2026-07-02")] = (1.001, 1, 401.0)
    absents[("1004", "2026-07-06")] = "INCOMPLETE_WINDOW"
    rows[("ACCT-D", "2026-07-07")] = (0.995, 1, 406.0)
    rows[("ACCT-D", "2026-07-08")] = (1.004, 1, 666.0)
    # E (1005): unmapped -> an absent record for every trading day, no row.
    for d in TRADING:
        absents[("1005", d)] = "UNMAPPED_ACCOUNT"
    # F: ends after 07-06; 07-07 and 07-08 are SERIES_ENDED_AT_SOURCE.
    rows[("ACCT-F", "2026-07-02")] = (1.001, 1, 601.0)
    absents[("1006", "2026-07-06")] = "NO_EOD_VALUE"  # its next row (07-07) is ABSENT and it carries no end value
    absents[("1006", "2026-07-07")] = "SERIES_ENDED_AT_SOURCE"
    absents[("1006", "2026-07-08")] = "SERIES_ENDED_AT_SOURCE"
    # G: the last day has no end_market_value and no next row -> NO_EOD_VALUE.
    rows[("ACCT-G", "2026-07-02")] = (1.001, 1, 701.0)
    rows[("ACCT-G", "2026-07-06")] = (1.002 * 1.0 * 1.0 * 1.003, 4, 705.0)
    rows[("ACCT-G", "2026-07-07")] = (0.995, 1, 706.0)
    absents[("1007", "2026-07-08")] = "NO_EOD_VALUE"
    return rows, absents


def naive_adapt(feed_rows, account_map, trading_days, firm, method_version, **kw):
    """A reference that does NOT compound (one factor per trading day, its own row only): the golden must reject it."""
    out = {"rows": [], "absent": [], "manifest": {}}
    for r in feed_rows:
        if r["day"] in trading_days and r["status"] == "RETURNED" and r["account_id"] in account_map:
            out["rows"].append({"account_id": account_map[r["account_id"]], "business_date": r["day"],
                                "total_return_daily": r["daily_factor"] - 1.0, "carried_days": 1})
    return out


def grade_golden(mod_adapt):
    res = mod_adapt(feed(), MAP, TRADING, FIRM, METHOD)
    need(isinstance(res, dict) and {"rows", "absent", "manifest"} <= set(res), "adapt must return a dict with rows, absent, manifest")
    exp_rows, exp_abs = expected()
    got = {}
    for r in res["rows"]:
        key = (r["account_id"], r["business_date"])
        need(key not in got, "duplicate row %s" % (key,))
        got[key] = r
    need(set(got) == set(exp_rows), "row keys differ: missing %s extra %s" % (sorted(set(exp_rows) - set(got)), sorted(set(got) - set(exp_rows))))
    for key, (factor, carried, mv) in exp_rows.items():
        r = got[key]
        need(r.get("total_return_daily") is not None and abs(r["total_return_daily"] - (factor - 1.0)) <= TOL,
             "return of %s: got %r want %r" % (key, r.get("total_return_daily"), factor - 1.0))
        need(r.get("carried_days") == carried, "carried_days of %s: got %r want %r" % (key, r.get("carried_days"), carried))
        need(r.get("market_value_eod") is not None and abs(r["market_value_eod"] - mv) <= TOL, "market_value_eod of %s" % (key,))
    ab = {}
    for a in res["absent"]:
        key = (a["account_id"], a["business_date"])
        need(key not in ab, "duplicate absent record %s" % (key,))
        ab[key] = a
    need(set(ab) == set(exp_abs), "absent keys differ: missing %s extra %s" % (sorted(set(exp_abs) - set(ab)), sorted(set(ab) - set(exp_abs))))
    for key, reason in exp_abs.items():
        need(ab[key].get("reason_class") == reason, "reason of %s: got %r want %r" % (key, ab[key].get("reason_class"), reason))
    # no trading day of a mapped account is in both lists, and no unmapped account has a row.
    need(not any(k[0] == "1005" for k in got), "an unmapped account carries a row")
    # the unmapped account's absent records carry no guessed source id.
    need(all(a.get("source_account_id") is None for a in res["absent"] if a["reason_class"] == "UNMAPPED_ACCOUNT"), "an unmapped absent record carries source_account_id")
    m = res["manifest"]
    need(m.get("accounts_in_feed") == 7, "manifest accounts_in_feed")
    need(m.get("accounts_unmapped") == 1 and m.get("accounts_mapped") == 6, "manifest mapped/unmapped counts")
    by = m.get("absent_by_reason") or {}
    want_by = {}
    for r in exp_abs.values():
        want_by[r] = want_by.get(r, 0) + 1
    need(by == want_by, "manifest absent_by_reason: got %r want %r" % (by, want_by))
    need(m.get("rows") == len(exp_rows), "manifest rows")
    # calendar factors folded into a later trading day (days other than the trading day itself) on the rows served.
    folded = sum(c - 1 for (_f, c, _m) in exp_rows.values())
    need(m.get("calendar_days_compounded") == folded, "manifest calendar_days_compounded: got %r want %r" % (m.get("calendar_days_compounded"), folded))
    for k in ("compounding", "market_value_basis", "fee_basis"):
        need(isinstance(m.get(k), str) and len(m[k]) >= 20, "manifest %s must be words (>= 20 chars)" % k)
    need("NET" in m["fee_basis"], "manifest fee_basis must name NET")
    return res


def grade_contract(mod, res, contract_mod):
    contract = contract_mod.CONTRACT
    cols = [c["name"] for c in contract["columns"]]
    opts = [o["name"] for o in contract["optional_columns"]]
    for r in res["rows"]:
        need(set(r) == set(cols) | set(opts), "row keys differ from the contract's columns + optional columns: %s" % sorted(set(r) ^ (set(cols) | set(opts))))
        probs = contract_mod.row_problems(contract, r)
        need(not probs, "contract validator: %s" % probs)
        need(r["firm"] == FIRM and r["method_version"] == METHOD and r["source"] == "orion" and r["flow_claim"] == "absent", "firm/method/source/claim")
        need(r["external_flow"] is None and r["income_received"] is None, "an Orion row carries no flow")
        need(isinstance(r["source_account_id"], int) and not isinstance(r["source_account_id"], bool), "source_account_id must be an int")
        need(r["return_basis"] == "TWR" and r["day_quality"] in contract["enums"]["day_quality"] and r["guard_state"] in contract["enums"]["guard_state"], "enum members")
        need(r["history_scope"] in contract["enums"]["history_scope"] and r["fee_amount_reason"] in contract["enums"]["fee_amount_reason"], "enum members")
        need(isinstance(r["total_return_daily"], float) and not math.isnan(r["total_return_daily"]), "total_return_daily must be a float")
    by_acct = {}
    for r in res["rows"]:
        by_acct.setdefault(r["account_id"], set()).add(r["source_account_id"])
    need(by_acct.get("ACCT-A") == {1001} and by_acct.get("ACCT-G") == {1007}, "source_account_id must equal the Orion id of the mapped account")
    # the validator is live: a null flow without its claim is refused, and a claim beside both flows is refused.
    bad = dict(res["rows"][0], flow_claim=None)
    need(contract_mod.row_problems(contract, bad), "the contract validator accepted an Orion row with a null flow and no claim")
    bad2 = dict(res["rows"][0], external_flow=1.0, income_received=1.0)
    need(contract_mod.row_problems(contract, bad2), "the contract validator accepted a claim beside both flows")
    # refusals
    gross = feed()
    gross[0] = dict(gross[0], calc_gross_of_fees=True)
    try:
        mod.adapt(gross, MAP, TRADING, FIRM, METHOD)
    except ValueError:
        pass
    else:
        raise Fail("the adapter accepted a gross-of-fees row")
    try:
        mod.adapt(feed(), MAP, list(reversed(TRADING)), FIRM, METHOD)
    except ValueError:
        pass
    else:
        raise Fail("the adapter accepted an unsorted trading calendar")


def grade_tests(root):
    tf = root / TEST_REL
    need(tf.is_file(), "no test file at %s" % TEST_REL)
    src = tf.read_bytes().decode("ascii")
    need(re.search(r"^def test_\w*mutant\w*\(", src, re.M) is not None, "the test file names no mutant test (def test_*mutant*)")
    r = subprocess.run([sys.executable, "-I", "-m", "pytest", "-q", "-p", "no:cacheprovider", str(tf)], cwd=str(root), capture_output=True, text=True, timeout=100)
    tail = (r.stdout or "").strip().splitlines()[-1:] or [""]
    need(r.returncode == 0, "pytest rc %s: %s" % (r.returncode, tail[0]))
    m = re.search(r"(\d+) passed", r.stdout or "")
    need(m is not None and int(m.group(1)) >= 10, "fewer than 10 passed tests: %s" % tail[0])


def selftest(root):
    exp_rows, _a = expected()
    need(len(exp_rows) == 17, "golden row count drifted: %d" % len(exp_rows))
    try:
        grade_golden(naive_adapt)
    except Fail:
        print("selftest: the naive (no compounding) reference FAILS the golden: as expected")
    else:
        raise Fail("the naive reference passed the golden")
    print("selftest PASS")


def main(argv):
    if len(argv) >= 2 and argv[1] == "--selftest":
        selftest(Path(argv[2]) if len(argv) > 2 else Path("."))
        return 0
    root, cid = Path(argv[1]).resolve(), argv[2]
    try:
        ap = root / ADAPTER_REL
        need(ap.is_file(), "no adapter at %s" % ADAPTER_REL)
        mod = _load("scope_feed_adapter_under_test", ap)
        need(hasattr(mod, "adapt"), "the adapter has no adapt()")
        if cid == "DBI123-1-AC1":
            grade_golden(mod.adapt)
        elif cid == "DBI123-1-AC2":
            res = grade_golden(mod.adapt)
            grade_contract(mod, res, _load("contract_040_tests", root / CONTRACT_TEST_REL))
        elif cid == "DBI123-1-AC3":
            grade_tests(root)
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
