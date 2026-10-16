"""IRPT_DASHBD round 147, workstream B-49F + contract (issuer 2.0.0_SA_COO~D2, owner of the reporting-publish function after the CTO's msg 8803) -- DB-b-279, the PUBLISHER's pure functions
for the first Cottonwood series: `build_series` writes the series contract 0.3.0's two unreported-days fields when it is handed the present partition dates and a trading calendar, and writes
the `income` array as the gold column stands (a null stays null, never 0.0); `validate_against_contract` grades the pair, the basis, the window; the 49 Financial path is byte-identical.
LOCAL: one python module and one new test file; no AWS, no deploy.

  DB-b-279 (~226)   infra/aws/lambda/investor-reporting/reporting-publish/publisher.py + tests/test_publisher_unreported.py + a facts record
                    DB147-1-AC1 (the 49 Financial path is BYTE-IDENTICAL to the base commit's, the refusals stand, nothing else in the module changed, version 0.2.0),
                    DB147-1-AC2 (BEHAVIOUR on a synthetic Cottonwood-shaped frame: income null stays null, the unreported list is the calendar minus the present partitions inside (first_data_date, as_of],
                                 the pair and the basis, the validator accepts the good document and rejects eight bad ones),
                    DB147-1-AC3 (the worker's tests, the module's existing tests, the grant, the facts record)

Usage: python <this file> <repo_root> <criterion_id>      prints "<id> PASS" or "<id> FAIL" last
       python <this file> --selftest                       the pure clauses on synthetic arms
"""
import ast
import copy
import datetime as dt
import importlib.util
import inspect
import json
import re
import subprocess
import sys
import tempfile
from pathlib import Path

D = "org/missions/D9/IRPT/IRPT_DASHBD/deliverables/"
BASE = "df2468cbc8fb261d5cdcd241f4a8cfa4e945d111"  # the last commit that changed publisher.py before this order
PUB_REL = "infra/aws/lambda/investor-reporting/reporting-publish/publisher.py"
TESTS_DIR = "infra/aws/lambda/investor-reporting/reporting-publish/tests"
TEST_REL = TESTS_DIR + "/test_publisher_unreported.py"
CAL_REL = "lib/trading_calendar.py"
CONTRACT_REL = "org/standards/IRPT_DASHBD_SERIES_CONTRACT.json"
AUTHOR = "0.9.0_WK_IRPT_DASHBD~226"
REC_REL = D + AUTHOR + "/RD_PUBLISHER_UNREPORTED_FACTS_R147.json"
ORDER_REL = "org/missions/D9/IRPT/IRPT_DASHBD/task-orders/IRPT_DASHBD.TO-DB-b-279.publisher-unreported-days-and-nullable-income.md"
GRANT_FILES = {PUB_REL, TEST_REL}
GRANT_PREFIXES = (D + AUTHOR + "/", "org/missions/D9/IRPT/IRPT_DASHBD/surprise-channel/investigations/", "org/missions/D9/IRPT/IRPT_DASHBD/task-orders/")
CHANGED_FUNCS = {"build_series", "validate_against_contract"}  # every other top-level name of the base keeps its exact source
FIXED = "trading calendar minus present partitions"
KEYS = ("unreported_trading_days", "unreported_trading_days_basis")
LONG_DIGITS = re.compile(r"\d{8,}")


class Fail(Exception):
    pass


def need(cond, msg):
    if not cond:
        raise Fail(msg)


def nes(x):
    return isinstance(x, str) and x.strip() != ""


def git(root, *a):
    r = subprocess.run(["git", "-C", str(root)] + list(a), capture_output=True)
    need(r.returncode == 0, "git %s: %s" % (" ".join(a[:2]), r.stderr.decode("utf-8", "replace").strip()[:200]))
    return r.stdout


def load_module(path, name):
    spec = importlib.util.spec_from_file_location(name, str(path))
    mod = importlib.util.module_from_spec(spec)
    sys.modules[name] = mod
    spec.loader.exec_module(mod)
    return mod


def own_commits(root):
    base = git(root, "log", "--diff-filter=A", "--format=%H", "--", ORDER_REL).decode().split()
    need(base, "the order's first commit is not in this history")
    out = git(root, "log", "--reverse", "--format=%H", "--author=" + AUTHOR, base[-1] + "..HEAD").decode().split()
    need(out, "no commit by %s since the order was issued" % AUTHOR)
    return out


def contract_030(c):
    """The repo contract with the two unreported-days fields declared (idempotent: the 0.3.0 file already holds them)."""
    c = copy.deepcopy(c)
    opt = c["series"].setdefault("optional", [])
    for k in KEYS:
        if k not in opt:
            opt.append(k)
    f = c["series"].setdefault("fields", {})
    f.setdefault(KEYS[0], {"kind": "scalar list of string", "source": "the report-build output's statement", "sentence": "ISO dates"})
    f.setdefault(KEYS[1], {"kind": "scalar string", "source": "a fixed text", "fixed_value": FIXED, "sentence": "fixed"})
    return c


# ------------------------------------------------------------------------------------------------ fixtures
def gold_row(date, value=100.0, ret=0.001, basis="TWR", quality="MEASURED", flow=0.0, income=0.0, hpr=None, mv=1, scope="PARTIAL_HISTORY", acct="0000000001"):
    return {"account_id": acct, "business_date": date, "market_value_eod": value, "total_return_daily": ret, "return_basis": basis, "day_quality": quality,
            "external_flow": flow, "income_received": income, "holdings_price_return": hpr, "method_version": mv, "history_scope": scope}


def fx49():
    return [gold_row("2026-09-01", 0.0, None, "NOT_MEASURABLE", "NOT_MEASURABLE"), gold_row("2026-09-02", 100.0, None, "NOT_MEASURABLE", "NOT_MEASURABLE"),
            gold_row("2026-09-03", 101.0, 0.01, hpr=0.009, income=1.5), gold_row("2026-09-04", 99.0, -0.02, flow=-1.0, income=0.0),
            gold_row("2026-09-08", 100.5, 0.015, hpr=None, income=0.0), gold_row("2026-09-09", 100.9, 0.004, income=2.25)]


def trading(tc, a, b):
    return [d.isoformat() for d in tc.trading_days_between(dt.date.fromisoformat(a), dt.date.fromisoformat(b))]


def fxcot(tc):
    """The calendar 2026-08-05 .. 2026-08-28 minus the days with no partition (08-05, before the account; 08-19 and 08-24, inside its window; 08-27, after its last row); the account holds a row on every present day 08-10 .. 08-26."""
    allday = trading(tc, "2026-08-05", "2026-08-28")
    missing = {"2026-08-05", "2026-08-19", "2026-08-24", "2026-08-27"}
    present = [d for d in allday if d not in missing]
    rows = [gold_row(d, 1000.0 + i, 0.001 if i else None, "TWR" if i else "NOT_MEASURABLE", "MEASURED" if i else "NOT_MEASURABLE", flow=0.0, income=None)
            for i, d in enumerate(x for x in present if "2026-08-10" <= x <= "2026-08-26")]
    return rows, present


# ------------------------------------------------------------------------------------------------ the clauses
def check_unchanged(base_src, new_src):
    """Every top-level def/class/assignment of the base other than CHANGED_FUNCS keeps its exact source; the new module may only ADD names."""
    tb, tn = ast.parse(base_src), ast.parse(new_src)

    def table(tree, src):
        out = {}
        for node in tree.body:
            if isinstance(node, (ast.FunctionDef, ast.ClassDef)):
                out[node.name] = ast.get_source_segment(src, node)
            elif isinstance(node, ast.Assign) and isinstance(node.targets[0], ast.Name):
                out[node.targets[0].id] = ast.get_source_segment(src, node)
        return out
    a, b = table(tb, base_src), table(tn, new_src)
    missing = [k for k in a if k not in b]
    need(not missing, "the module lost top-level names: %s" % missing[:4])
    changed = [k for k in a if a[k] != b[k] and k not in CHANGED_FUNCS and k != "PUBLISHER_VERSION"]
    need(not changed, "top-level names changed beyond build_series, validate_against_contract and PUBLISHER_VERSION: %s" % changed[:4])
    return len(a), len(b) - len(a)


def check_49f(B, N, contract):
    rows = fx49()
    sb, sn = B.build_series(rows), N.build_series(rows)
    need(sb == sn and list(sb) == list(sn), "the 49 Financial series differs from the base commit's")
    need(B.series_bytes(sb) == N.series_bytes(sn), "the 49 Financial series bytes differ from the base commit's")
    mb = B.build_manifest("A", "f", sb, 100, built_at="2026-01-01T00:00:00Z")
    mn = N.build_manifest("A", "f", sn, 100, built_at="2026-01-01T00:00:00Z")
    need({k: v for k, v in mb.items() if k != "publisher_version"} == {k: v for k, v in mn.items() if k != "publisher_version"}, "the manifest differs beyond publisher_version")
    need(B.PUBLISHER_VERSION == "0.1.0" and N.PUBLISHER_VERSION == "0.2.0" and mn["publisher_version"] == "0.2.0", "PUBLISHER_VERSION must be 0.2.0 (base 0.1.0)")
    need(B.validate_against_contract(sb, mb, contract) == [] and N.validate_against_contract(sn, mn, contract) == [], "the 49 Financial documents must validate against the contract at HEAD")
    for label, mut in (("a null market value", lambda r: r.update(market_value_eod=None)), ("a null external flow", lambda r: r.update(external_flow=None)),
                       ("a basis that disagrees with the return", lambda r: r.update(return_basis="NOT_MEASURABLE"))):
        rr = copy.deepcopy(rows)
        mut(rr[3])
        for mod, nm in ((B, "base"), (N, "new")):
            try:
                mod.build_series(rr)
            except mod.PublishRefused:
                continue
            raise Fail("%s: %s no longer refuses" % (label, nm))
    for name in ("build_client_summary", "summary_bytes", "window_return", "validate_filled_report", "publish_filled_report", "report_address", "drawdown_episodes", "series_bytes"):
        need(hasattr(N, name), "the module lost %s" % name)
    return True


def check_cottonwood(N, tc, contract):
    rows, present = fxcot(tc)
    need(len(rows) >= 8, "fixture too small")
    first, last = rows[0]["business_date"], rows[-1]["business_date"]
    want = [d for d in trading(tc, first, last) if d > first and d <= last and d not in present]
    need(want == ["2026-08-19", "2026-08-24"], "fixture arithmetic: %s" % want)
    s = N.build_series(rows, present_dates=present, calendar=tc)
    need(s["unreported_trading_days"] == want, "the unreported list is the calendar over (first_data_date, as_of] minus the present partitions: %s" % s["unreported_trading_days"])
    need(s["unreported_trading_days_basis"] == FIXED, "the basis must read exactly the fixed text")
    need(s["income"] == [None] * len(rows), "income must stay null where the gold row is null, never 0.0")
    need(list(s)[-2:] == list(KEYS) and list(s)[-3] == "drawdown_episodes", "the pair must follow drawdown_episodes")
    need(s["date"] == [r["business_date"] for r in rows] and not any(d in s["date"] for d in want), "date holds the account's rows and no unreported day")
    need("2026-08-05" not in s["unreported_trading_days"] and "2026-08-27" not in s["unreported_trading_days"] and "2026-08-28" not in s["unreported_trading_days"], "a day before first_data_date or after as_of is not listed")
    # none missing -> []
    full = trading(tc, first, last)
    s2 = N.build_series([gold_row(d, 100.0, 0.001, income=None) for d in full], present_dates=full, calendar=tc)
    need(s2["unreported_trading_days"] == [] and s2["unreported_trading_days_basis"] == FIXED, "no unreported day writes [] and the basis, never omits")
    s_first = N.build_series(rows, present_dates=[d for d in present if d != first], calendar=tc)
    need(s_first["unreported_trading_days"] == want, "first_data_date itself is never listed (strictly after it): %s" % s_first["unreported_trading_days"])
    s_last = N.build_series(rows, present_dates=[d for d in present if d != last], calendar=tc)
    need(s_last["unreported_trading_days"] == want + [last], "as_of itself is inside the window (up to and including it): %s" % s_last["unreported_trading_days"])
    s3 = N.build_series(rows)
    need(not any(k in s3 for k in KEYS), "without present_dates the pair is absent")
    try:
        N.build_series(rows, present_dates=present)
    except N.PublishRefused:
        pass
    else:
        raise Fail("present_dates without a calendar must be refused")
    for label, mut in (("a null market value", lambda r: r.update(market_value_eod=None)), ("a null external flow", lambda r: r.update(external_flow=None))):
        rr = copy.deepcopy(rows)
        mut(rr[4])
        try:
            N.build_series(rr, present_dates=present, calendar=tc)
        except N.PublishRefused:
            continue
        raise Fail("%s must still be refused" % label)
    g1, g2 = N.series_bytes(s), N.series_bytes(N.build_series(rows, present_dates=present, calendar=tc))
    need(g1 == g2, "equal input must give equal bytes")
    c = contract_030(contract)
    man = N.build_manifest("A", "f", s, len(g1[0]) if isinstance(g1, tuple) else 1, built_at="2026-01-01T00:00:00Z")
    need(N.validate_against_contract(s, man, c) == [], "the good document must validate: %s" % N.validate_against_contract(s, man, c))
    old = copy.deepcopy(contract)
    old["series"]["optional"] = [k for k in old["series"].get("optional", []) if k not in KEYS]
    need(N.validate_against_contract(s, man, old), "a contract that does not name the pair must reject a series that carries it")
    bad = {
        "the list without the basis": lambda x: x.pop(KEYS[1]),
        "the basis without the list": lambda x: x.pop(KEYS[0]),
        "a basis of other words": lambda x: x.update({KEYS[1]: "calendar"}),
        "a non-ISO date": lambda x: x.update({KEYS[0]: ["19 Aug 2026"]}),
        "a non-ISO date that sorts inside the window": lambda x: x.update({KEYS[0]: ["2026-08-1a"]}),
        "a date before first_data_date": lambda x: x.update({KEYS[0]: ["2026-08-05"]}),
        "a date after as_of": lambda x: x.update({KEYS[0]: ["2026-08-28"]}),
        "a present day": lambda x: x.update({KEYS[0]: [x["date"][2]]}),
        "an unsorted list": lambda x: x.update({KEYS[0]: ["2026-08-24", "2026-08-19"]}),
    }
    for label, fn in bad.items():
        x = copy.deepcopy(s)
        fn(x)
        need(N.validate_against_contract(x, man, c), "%s must be rejected" % label)
    return len(bad)


def check_facts(rec, N):
    exp = {"publisher_version", "build_series_signature", "basis", "byte_identical_49f", "tests", "words"}
    need(isinstance(rec, dict) and set(rec) == exp, "record keys differ: %s" % (sorted(set(rec) ^ exp) if isinstance(rec, dict) else "?"))
    need(rec["publisher_version"] == "0.2.0" and rec["basis"] == FIXED and rec["byte_identical_49f"] is True, "version, basis or the byte-identity claim differ")
    need(rec["build_series_signature"] == str(inspect.signature(N.build_series)), "build_series_signature differs from the module's")
    t = rec["tests"]
    need(isinstance(t, dict) and set(t) == {"new", "existing"} and all(isinstance(v, int) and not isinstance(v, bool) and v >= 1 for v in t.values()), "tests must be {new, existing} whole numbers")
    need(nes(rec["words"]) and 80 <= len(rec["words"]) <= 1800 and not LONG_DIGITS.findall(rec["words"]), "words must be one paragraph of 80 to 1800 characters with no long digit run")
    return True


def check_grant(changed):
    bad = [f for f in changed if f not in GRANT_FILES and not f.startswith(GRANT_PREFIXES)]
    need(not bad, "the worker's commits touch files outside its grant: %s" % bad[:3])
    need(PUB_REL in changed and TEST_REL in changed, "the publisher and its new test file must both change")
    return True


def run_pytest(root, target, ignore=None):
    cmd = [sys.executable, "-m", "pytest", "-q", "-p", "no:cacheprovider", target]
    if ignore:
        cmd += ["--ignore=" + ignore]
    r = subprocess.run(cmd, cwd=str(root), capture_output=True, text=True, timeout=900)
    m = re.search(r"(\d+) passed", r.stdout)
    need(r.returncode == 0 and m is not None, "tests failed: %s" % r.stdout[-300:].replace("\n", " | "))
    return int(m.group(1))


def modules(root):
    root = Path(root)
    base_src = git(root, "show", BASE + ":" + PUB_REL).decode("utf-8")
    tmp = Path(tempfile.mkdtemp(prefix="p147_"))
    (tmp / "publisher_base.py").write_text(base_src, encoding="utf-8", newline="\n")
    B = load_module(tmp / "publisher_base.py", "publisher_base")
    N = load_module(root / PUB_REL, "publisher_new")
    tc = load_module(root / CAL_REL, "tc_repo")
    contract = json.loads((root / CONTRACT_REL).read_bytes().decode("utf-8"))
    return base_src, B, N, tc, contract


def run(root, cid):
    root = Path(root)
    if cid == "DB147-1-AC1":
        base_src, B, N, tc, contract = modules(root)
        new_src = (root / PUB_REL).read_bytes().decode("utf-8")
        nb, added = check_unchanged(base_src, new_src)
        check_49f(B, N, contract)
        print("OK: the 49 Financial series is byte-identical to commit %s's, the three refusals stand, %d base names keep their exact source (%d added), PUBLISHER_VERSION 0.2.0" % (BASE[:10], nb, added))
        return True
    if cid == "DB147-1-AC2":
        _, _, N, tc, contract = modules(root)
        n = check_cottonwood(N, tc, contract)
        print("OK: a Cottonwood-shaped frame: income null stays null, the unreported days are the calendar minus the present partitions inside (first_data_date, as_of], the pair follows drawdown_episodes, [] when none, absent without present_dates; the validator accepts the document and rejects %d bad ones and a contract that does not name the pair" % n)
        return True
    if cid == "DB147-1-AC3":
        _, _, N, _, _ = modules(root)
        need((root / TEST_REL).is_file(), "no %s" % TEST_REL)
        n_new = run_pytest(root, TEST_REL)
        need(n_new >= 12, "the new test file holds %d passing tests, at least 12 are owed" % n_new)
        n_old = run_pytest(root, TESTS_DIR, ignore=TEST_REL)
        changed = set()
        for cm in own_commits(root):
            changed |= set(git(root, "show", "--name-only", "--format=", cm).decode().split())
        check_grant(changed)
        rec = json.loads((root / REC_REL).read_bytes().decode("utf-8"))
        check_facts(rec, N)
        need(rec["tests"] == {"new": n_new, "existing": n_old}, "the record's test counts differ from the recount %s" % {"new": n_new, "existing": n_old})
        print("OK: %d new tests and the module's %d existing tests pass; %d files changed, all in the grant; the facts record equals the recount" % (n_new, n_old, len(changed)))
        return True
    raise Fail("unknown criterion %s" % cid)


def selftest():
    def red(fn, label):
        try:
            fn()
        except Fail:
            return
        raise AssertionError("red arm passed: " + label)
    a = "X = 1\n\ndef f():\n    return 1\n\ndef build_series(r):\n    return r\n\ndef validate_against_contract(a):\n    return a\n\nPUBLISHER_VERSION = \"0.1.0\"\n"
    assert check_unchanged(a, a.replace("return r", "return r + 1").replace("0.1.0", "0.2.0") + "\ndef g():\n    return 2\n") == (5, 1)
    red(lambda: check_unchanged(a, a.replace("return 1", "return 2")), "a changed neighbour")
    red(lambda: check_unchanged(a, a.replace("def f", "def h")), "a lost name")
    assert check_grant({PUB_REL, TEST_REL, D + AUTHOR + "/x.json"})
    red(lambda: check_grant({PUB_REL, TEST_REL, "lib/x.py"}), "outside grant")
    red(lambda: check_grant({PUB_REL}), "no test")
    red(lambda: check_grant({TEST_REL}), "no publisher")

    class M:
        @staticmethod
        def build_series(rows, present_dates=None, calendar=None):
            return {}
    rec = {"publisher_version": "0.2.0", "build_series_signature": str(inspect.signature(M.build_series)), "basis": FIXED, "byte_identical_49f": True, "tests": {"new": 12, "existing": 40}, "words": "w" * 100}
    assert check_facts(rec, M)
    arms = (("version", lambda r: r.update(publisher_version="0.1.0")), ("signature", lambda r: r.update(build_series_signature="(rows)")), ("basis", lambda r: r.update(basis="x")),
            ("identity", lambda r: r.update(byte_identical_49f=False)), ("tests", lambda r: r.update(tests={"new": 0, "existing": 1})), ("extra", lambda r: r.update(z=1)),
            ("words", lambda r: r.update(words="short")), ("digits", lambda r: r.update(words="w" * 100 + " 123456789")))
    for label, fn in arms:
        r2 = copy.deepcopy(rec)
        fn(r2)
        red(lambda: check_facts(r2, M), label)
    c = contract_030({"series": {"optional": ["class_value"], "fields": {}}})
    assert c["series"]["optional"] == ["class_value"] + list(KEYS) and c["series"]["fields"][KEYS[1]]["fixed_value"] == FIXED
    assert contract_030(c) == c
    print("selftest: unchanged-names (3), grant (4), facts (%d red arms) and contract-helper clauses behave" % len(arms))
    print("selftest PASS")


if __name__ == "__main__":
    if sys.argv[1:2] == ["--selftest"]:
        selftest()
        sys.exit(0)
    try:
        run(sys.argv[1], sys.argv[2])
        print(sys.argv[2] + " PASS")
    except Exception as e:  # a failed read or clause is a FAIL, not a traceback
        print("FAIL: " + str(e))
        print(sys.argv[2] + " FAIL")
        sys.exit(1)
