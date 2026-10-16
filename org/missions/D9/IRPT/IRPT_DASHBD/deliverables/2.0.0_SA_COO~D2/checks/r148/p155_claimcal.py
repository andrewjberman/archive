"""IRPT_DASHBD round 148, workstream PUBWRITE (issuer 2.0.0_SA_COO~D2, owner of the reporting-publish function) -- DB-b-287, the PUBLISHER and the Cottonwood PUBLISH HANDLER write what series contract 0.3.1 declares
(CTO round-147 analysis, msg 9060 items 1 and 2): the series carries `income_claim` = "absent" exactly when every `income` entry is null (and refuses a series whose income is null on some days and a number on others);
the manifest carries `calendar_source` (pandas_market_calendars or fallback_2010_2027) when the caller names it; the validator grades both against the contract; PUBLISHER_VERSION 0.3.0. The 49 Financial series stays
BYTE-IDENTICAL to the base commit's on a fixture. Python files and tests only; nothing is deployed (the code-update pair is a later act).

  DB-b-287 (~231)   infra/aws/lambda/investor-reporting/reporting-publish/publisher.py + .../reporting-publish-cot/handler.py + tests + a facts record
                    DB155-1-AC1 (the publisher's pure behaviour and the 49 Financial byte identity),
                    DB155-1-AC2 (the Cottonwood handler on a fake S3: income_claim, calendar_source, the guard),
                    DB155-1-AC3 (the new tests, the existing publisher and handler tests, the grant, the facts record)

Usage: python <this file> <repo_root> <criterion_id>      prints "<id> PASS" or "<id> FAIL" last
       python <this file> --selftest                       the pure clauses on synthetic arms
"""
import ast
import copy
import gzip
import importlib.util
import json
import re
import subprocess
import sys
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
D = "org/missions/D9/IRPT/IRPT_DASHBD/deliverables/"
PUB_REL = "infra/aws/lambda/investor-reporting/reporting-publish/publisher.py"
HANDLER_REL = "infra/aws/lambda/investor-reporting/reporting-publish-cot/handler.py"
PUB_TESTS = "infra/aws/lambda/investor-reporting/reporting-publish/tests"
COT_TESTS = "infra/aws/lambda/investor-reporting/reporting-publish-cot/tests"
NEW_TEST = PUB_TESTS + "/test_publisher_claim_calendar.py"
CONTRACT_REL = "org/standards/IRPT_DASHBD_SERIES_CONTRACT.json"
AUTHOR = "0.9.0_WK_IRPT_DASHBD~231"
REC_REL = D + AUTHOR + "/RD_PUBLISHER_CLAIM_CAL_FACTS_R148.json"
ORDER_REL = "org/missions/D9/IRPT/IRPT_DASHBD/task-orders/IRPT_DASHBD.TO-DB-b-287.publisher-income-claim-and-calendar-source.md"
GRANT_PREFIXES = (PUB_TESTS + "/", COT_TESTS + "/", D + AUTHOR + "/", "org/missions/D9/IRPT/IRPT_DASHBD/surprise-channel/investigations/", "org/missions/D9/IRPT/IRPT_DASHBD/task-orders/")
GRANT_FILES = {PUB_REL, HANDLER_REL}
CHANGED_FUNCS = {"build_series", "build_manifest", "validate_against_contract", "PUBLISHER_VERSION"}
CAL_VALUES = ["pandas_market_calendars", "fallback_2010_2027"]
MAX_EXISTING_TEST_LINES = 14
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
    return r.stdout.decode("utf-8", "replace")


def load(path, name):
    spec = importlib.util.spec_from_file_location(name, str(path))
    mod = importlib.util.module_from_spec(spec)
    sys.modules[name] = mod
    spec.loader.exec_module(mod)
    return mod


def p147():
    return load(HERE.parent / "r147" / "p147_publisher.py", "p147_helper")


def p148():
    return load(HERE.parent / "r147" / "p148_cothandler.py", "p148_helper")


def base_commit(root):
    out = git(root, "log", "--diff-filter=A", "--format=%H", "--", ORDER_REL).split()
    need(out, "the order's first commit is not in this history")
    return out[-1]


def own_commits(root):
    out = git(root, "log", "--reverse", "--format=%H", "--author=" + AUTHOR, base_commit(root) + "..HEAD").split()
    need(out, "no commit by %s since the order was issued" % AUTHOR)
    return out


def segments(src):
    return {n.name: ast.get_source_segment(src, n) for n in ast.parse(src).body if isinstance(n, (ast.FunctionDef, ast.ClassDef))}


def check_unchanged(base_src, new_src):
    a, b = segments(base_src), segments(new_src)
    kept = 0
    for name in a:
        need(name in b, "the module lost %s" % name)
        if name in CHANGED_FUNCS:
            continue
        need(a[name] == b[name], "the pure function %s changed (it must keep its exact source)" % name)
        kept += 1
    return kept


def frames(tc):
    """(a 49-Financial-shaped frame with numeric income, a Cottonwood-shaped frame with null income, its present dates)."""
    h = p147()
    rows49 = h.fx49()
    rowscot, present = h.fxcot(tc)
    return h, rows49, rowscot, present


def check_publisher(B, N, tc, contract):
    h, rows49, rowscot, present = frames(tc)
    need(N.PUBLISHER_VERSION == "0.3.0", "PUBLISHER_VERSION must be 0.3.0")
    sb, sn = B.build_series(rows49), N.build_series(rows49)
    need(list(sb) == list(sn) and sb == sn and B.series_bytes(sb) == N.series_bytes(sn), "the 49 Financial series must be byte-identical to the base commit's (numeric income writes no claim)")
    mb = B.build_manifest("A", "f", sb, 100, built_at="2026-01-01T00:00:00Z")
    mn = N.build_manifest("A", "f", sn, 100, built_at="2026-01-01T00:00:00Z")
    need({k: v for k, v in mb.items() if k != "publisher_version"} == {k: v for k, v in mn.items() if k != "publisher_version"} and "calendar_source" not in mn, "the 49 Financial manifest differs beyond publisher_version, or carries a calendar_source nobody named")
    s = N.build_series(rowscot, present_dates=present, calendar=tc)
    keys = list(s)
    need(keys[-3:] == ["unreported_trading_days", "unreported_trading_days_basis", "income_claim"], "a Cottonwood series ends with the pair then income_claim: %s" % keys[-4:])
    need(s["income_claim"] == "absent" and all(x is None for x in s["income"]), "all-null income writes income_claim absent and the nulls stay null")
    s_no_pair = N.build_series(rowscot)
    need(s_no_pair["income_claim"] == "absent" and "unreported_trading_days" not in s_no_pair, "the claim does not depend on the unreported pair")
    mixed = copy.deepcopy(rowscot)
    mixed[3]["income_received"] = 1.25
    try:
        N.build_series(mixed, present_dates=present, calendar=tc)
    except N.PublishRefused:
        pass
    else:
        raise Fail("income null on some days and a number on others must be refused")
    m = N.build_manifest("A", "f", s, 100, built_at="2026-01-01T00:00:00Z", calendar_source="fallback_2010_2027")
    need(list(m)[-1] == "calendar_source" and m["calendar_source"] == "fallback_2010_2027" and m["publisher_version"] == "0.3.0", "build_manifest(calendar_source=...) appends calendar_source last")
    need("calendar_source" not in N.build_manifest("A", "f", s, 100, built_at="2026-01-01T00:00:00Z"), "no calendar_source named -> the key is absent")
    for bad in ("NYSE/hardcoded", "", "pandas"):
        try:
            N.build_manifest("A", "f", s, 100, calendar_source=bad)
        except N.PublishRefused:
            continue
        raise Fail("calendar_source %r must be refused" % bad)
    good = N.validate_against_contract(s, m, contract)
    need(good == [], "the Cottonwood document must validate against the repo contract: %s" % good)
    cases = {
        "all-null income without the claim": lambda x, mm: x.pop("income_claim"),
        "the claim beside a number": lambda x, mm: x["income"].__setitem__(0, 1.0),
        "a claim of other words": lambda x, mm: x.update(income_claim="present"),
        "mixed income": lambda x, mm: (x.pop("income_claim"), x["income"].__setitem__(0, 1.0)),
        "a calendar source outside the values": lambda x, mm: mm.update(calendar_source="NYSE/hardcoded"),
        "a null calendar source": lambda x, mm: mm.update(calendar_source=None),
    }
    for label, fn in cases.items():
        x, mm = copy.deepcopy(s), copy.deepcopy(m)
        fn(x, mm)
        need(N.validate_against_contract(x, mm, contract), "%s must be rejected" % label)
    old = copy.deepcopy(contract)
    old["manifest"].pop("optional", None)
    need(N.validate_against_contract(s, m, old), "a contract with no manifest.optional must reject a manifest that carries calendar_source")
    old2 = copy.deepcopy(contract)
    old2["series"]["optional"] = [k for k in old2["series"]["optional"] if k != "income_claim"]
    need(N.validate_against_contract(s, m, old2), "a contract that does not name income_claim must reject a series that carries it")
    return len(cases)


def check_handler_run(root, hmod_path, pub_path, tc_mod):
    """Run the handler on the p148 fixture (a fake S3 of synthetic Cottonwood gold)."""
    h8 = p148()
    root = Path(root)
    naming = h8.load_module(root / "lib" / "opal_naming.py", "opal_naming")
    tc = h8.load_module(root / "lib" / "trading_calendar.py", "trading_calendar")
    sys.path.insert(0, str(Path(pub_path).parent))
    pub = h8.load_module(pub_path, "publisher")
    mod = h8.load_module(hmod_path, "cot_handler_155")
    s3, ex = h8.fixture(root, tc, naming)
    out = mod.lambda_handler({"upload": True}, None, s3)
    need(set(out) == h8.SUMMARY_KEYS, "the summary keys must stay the 14 of DB-b-280: %s" % sorted(set(out) ^ h8.SUMMARY_KEYS))
    for acct in ("A0000000001", "B0000000002"):
        gz = s3.puts[h8.series_key(naming, ex["firm"], acct, "series.json.gz")]
        s = json.loads(gzip.decompress(gz).decode("utf-8"))
        m = json.loads(s3.puts[h8.series_key(naming, ex["firm"], acct, "manifest.json")].decode("utf-8"))
        need(s.get("income_claim") == "absent" and all(x is None for x in s["income"]), "%s: the stored series carries income_claim absent beside null income" % acct[:1])
        need(m.get("calendar_source") in CAL_VALUES and m["publisher_version"] == "0.3.0", "%s: the stored manifest carries calendar_source in its values and publisher 0.3.0: %s" % (acct[:1], m.get("calendar_source")))
        want = "pandas_market_calendars" if tc_mod.calendar_source().startswith("NYSE/pandas_market_calendars") else "fallback_%d_%d" % (tc_mod.FALLBACK_FIRST_YEAR, tc_mod.FALLBACK_LAST_YEAR)
        need(m["calendar_source"] == want, "%s: calendar_source must be the one the calendar answered with (%s)" % (acct[:1], want))
    # the other branch of the mapping: when the package answers, the manifest says so (the calendar is made to answer as the package)
    saved = mod.trading_calendar.calendar_source
    mod.trading_calendar.calendar_source = lambda date=None: "NYSE/pandas_market_calendars"
    try:
        s3p, exp = h8.fixture(root, tc, naming)
        mod.lambda_handler({"upload": True}, None, s3p)
        mp = json.loads(s3p.puts[h8.series_key(naming, exp["firm"], "A0000000001", "manifest.json")].decode("utf-8"))
        need(mp.get("calendar_source") == "pandas_market_calendars", "when the package answers, calendar_source must read pandas_market_calendars: %s" % mp.get("calendar_source"))
    finally:
        mod.trading_calendar.calendar_source = saved
    # the guard: a contract that does not name the new keys refuses before any S3 call
    tmp = Path(tempfile.mkdtemp(prefix="p155_"))
    (tmp / "org" / "standards").mkdir(parents=True)
    base = json.loads((root / CONTRACT_REL).read_bytes().decode("utf-8"))
    variants = []
    a = copy.deepcopy(base)
    a["series"]["optional"] = [k for k in a["series"]["optional"] if k != "income_claim"]
    variants.append(("no income_claim in series.optional", a))
    b = copy.deepcopy(base)
    b["manifest"].pop("optional", None)
    variants.append(("no calendar_source in manifest.optional", b))
    keep = mod._ROOT
    try:
        for label, c in variants:
            (tmp / "org" / "standards" / "IRPT_DASHBD_SERIES_CONTRACT.json").write_text(json.dumps(c), encoding="utf-8")
            mod._ROOT = tmp
            s3b = h8.FakeS3({})
            try:
                mod.lambda_handler({"upload": True}, None, s3b)
            except SystemExit as e:
                need("REFUSED" in str(e), "the guard reads REFUSED")
            else:
                raise Fail("a contract with %s must refuse" % label)
            need(s3b.lists == 0 and not s3b.puts, "the guard runs before any S3 call (%s)" % label)
    finally:
        mod._ROOT = keep
    del pub
    return len(variants)


def check_grant(changed):
    bad = [f for f in changed if f not in GRANT_FILES and not f.startswith(GRANT_PREFIXES)]
    need(not bad, "the worker's commits touch files outside its grant: %s" % bad[:3])
    need(PUB_REL in changed and HANDLER_REL in changed and NEW_TEST in changed, "the publisher, the handler and the new test must all change")
    return True


def check_facts(rec, n_new):
    exp = {"publisher_version", "income_claim", "manifest_optional_key", "byte_identical_49f", "tests", "words"}
    need(isinstance(rec, dict) and set(rec) == exp, "record keys differ: %s" % (sorted(set(rec) ^ exp) if isinstance(rec, dict) else "?"))
    need(rec["publisher_version"] == "0.3.0" and rec["income_claim"] == {"value": "absent", "rule": "present exactly when every income entry is null"} and rec["manifest_optional_key"] == "calendar_source" and rec["byte_identical_49f"] is True, "version, claim, manifest key or identity claim differ")
    need(isinstance(rec["tests"], int) and not isinstance(rec["tests"], bool) and rec["tests"] == n_new and n_new >= 10, "tests must equal the recount, at least 10")
    need(nes(rec["words"]) and 80 <= len(rec["words"]) <= 1800 and not LONG_DIGITS.findall(rec["words"]), "words must be one paragraph of 80 to 1800 characters with no long digit run")
    return True


def pytest_run(root, targets):
    r = subprocess.run([sys.executable, "-m", "pytest", "-q", "-p", "no:cacheprovider"] + list(targets), cwd=str(root), capture_output=True, text=True, timeout=900)
    m = re.search(r"(\d+) passed", r.stdout)
    need(r.returncode == 0 and m is not None, "tests failed: %s" % r.stdout[-300:].replace("\n", " | "))
    return int(m.group(1))


def run(root, cid):
    root = Path(root)
    base = base_commit(root)
    h = p147()
    if cid == "DB155-1-AC1":
        _, B, N, tc, contract = h.modules(root)
        n_kept = check_unchanged(git(root, "show", "%s:%s" % (base, PUB_REL)), (root / PUB_REL).read_bytes().decode("utf-8"))
        n = check_publisher(B, N, tc, contract)
        print("OK: publisher 0.3.0: the 49 Financial series is byte-identical to the base's; an all-null income writes income_claim absent (last, after the pair), a mixed income is refused; build_manifest appends calendar_source (refusing other words); the validator rejects %d bad documents and a contract that does not name the new keys; %d other names keep their exact source" % (n, n_kept))
        return True
    if cid == "DB155-1-AC2":
        _, _, _, tc, _ = h.modules(root)
        n = check_handler_run(root, root / HANDLER_REL, root / PUB_REL, tc)
        print("OK: the Cottonwood handler on a fake S3: both accounts' stored series carry income_claim absent beside null income and both manifests carry calendar_source (the calendar's own answer) and publisher 0.3.0; the 14 summary keys unchanged; %d contracts that omit a new key refuse before any S3 call" % n)
        return True
    if cid == "DB155-1-AC3":
        need((root / NEW_TEST).is_file(), "no %s" % NEW_TEST)
        n_new = pytest_run(root, [NEW_TEST])
        need(n_new >= 10, "the new test file holds %d passing tests, at least 10 are owed" % n_new)
        ignore = [t for t in (PUB_TESTS, COT_TESTS)]
        n_old = 0
        for d in ignore:
            tests = [str(p.relative_to(root)).replace(chr(92), "/") for p in sorted((root / d).glob("test_*.py")) if str(p.relative_to(root)).replace(chr(92), "/") != NEW_TEST]
            n_old += pytest_run(root, tests)
        edited = 0
        for d in ignore:
            for ln in git(root, "diff", "--numstat", base, "HEAD", "--", d).split("\n"):
                p = ln.split("\t")
                if len(p) == 3 and p[0].isdigit() and p[1].isdigit() and p[2] != NEW_TEST:
                    edited += int(p[0]) + int(p[1])
        need(edited <= MAX_EXISTING_TEST_LINES, "the existing publisher and handler tests may change by at most %d lines in all, read %d" % (MAX_EXISTING_TEST_LINES, edited))
        changed = set()
        for cm in own_commits(root):
            changed |= set(git(root, "show", "--name-only", "--format=", cm).split())
        check_grant(changed)
        check_facts(json.loads((root / REC_REL).read_bytes().decode("utf-8")), n_new)
        print("OK: %d new tests and the existing publisher and handler tests' %d pass (%d changed lines in them, at most %d); %d files changed, all in the grant; the facts record equals the recount" % (n_new, n_old, edited, MAX_EXISTING_TEST_LINES, len(changed)))
        return True
    raise Fail("unknown criterion %s" % cid)


def selftest():
    def red(fn, label):
        try:
            fn()
        except Fail:
            return
        raise AssertionError("red arm passed: " + label)
    base = "def build_series():\n    return 1\n\ndef build_manifest():\n    return 2\n\ndef validate_against_contract():\n    return 3\n\ndef drawdown_episodes():\n    return 4\n\nPUBLISHER_VERSION = '0.2.0'\n"
    assert check_unchanged(base, base.replace("return 1", "return 10").replace("return 3", "return 30") + "\ndef extra():\n    return 0\n") == 1
    red(lambda: check_unchanged(base, base.replace("return 4", "return 40")), "a changed neighbour")
    red(lambda: check_unchanged(base, base.replace("def drawdown_episodes", "def other")), "a lost name")
    assert check_grant({PUB_REL, HANDLER_REL, NEW_TEST, COT_TESTS + "/test_handler.py", D + AUTHOR + "/x.json"})
    red(lambda: check_grant({PUB_REL, HANDLER_REL, NEW_TEST, "lib/x.py"}), "outside grant")
    red(lambda: check_grant({PUB_REL, NEW_TEST}), "no handler")
    rec = {"publisher_version": "0.3.0", "income_claim": {"value": "absent", "rule": "present exactly when every income entry is null"}, "manifest_optional_key": "calendar_source", "byte_identical_49f": True, "tests": 12, "words": "w" * 100}
    assert check_facts(rec, 12)
    arms = (("version", lambda r: r.update(publisher_version="0.2.0")), ("claim", lambda r: r["income_claim"].update(value="present")), ("key", lambda r: r.update(manifest_optional_key="x")),
            ("identity", lambda r: r.update(byte_identical_49f=False)), ("tests", lambda r: r.update(tests=11)), ("few", lambda r: r.update(tests=3)), ("extra", lambda r: r.update(z=1)),
            ("words", lambda r: r.update(words="short")), ("digits", lambda r: r.update(words="w" * 100 + " 123456789")))
    for label, fn in arms:
        r2 = copy.deepcopy(rec)
        fn(r2)
        red(lambda: check_facts(r2, 12), label)
    print("selftest: unchanged (2 red arms), grant (2) and facts (%d red arms) clauses behave" % len(arms))
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
