"""IRPT_DASHBD round 149, workstream HSPUB (issuer 2.0.0_SA_COO~D2) -- DB-b-295, the PUBLISHER writes the history-scope pair (CTO ruling msg 9226): publisher 0.4.0 carries the producer's inference to the series. When the NEWEST gold
row of an account carries history_scope_claim = "inferred" the series carries history_scope_claim = "inferred" and history_scope_basis = "first value day vs source floor" (series contract 0.3.3); a row that carries no claim
(gold written before the derivation) writes NO pair, so a legacy series makes no statement; a claim with any other word is refused. Both publish handlers read the conditional gold column only from a partition that has it.
LOCAL: python files; nothing runs against AWS.

  DB-b-295 (~238)   infra/aws/lambda/investor-reporting/reporting-publish/publisher.py + reporting-publish/handler.py + reporting-publish-cot/handler.py + tests + a facts record
                    DB163-1-AC1 (the publisher: build_series, validate_against_contract, the version),
                    DB163-1-AC2 (both handlers on fake gold: with the claim, without it, and mixed),
                    DB163-1-AC3 (the new tests, the publisher and handler test directories, the forced version-pin edits, the grant, the facts record)

Usage: python <this file> <repo_root> <criterion_id>      prints "<id> PASS" or "<id> FAIL" last
       python <this file> --selftest                       the pure clauses on synthetic arms
"""
import copy
import gzip
import importlib.util
import json
import re
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
D = "org/missions/D9/IRPT/IRPT_DASHBD/deliverables/"
AUTHOR = "0.9.0_WK_IRPT_DASHBD~238"
REC_REL = D + AUTHOR + "/RD_HISTSCOPE_PUBLISHER_FACTS_R149.json"
ORDER_REL = "org/missions/D9/IRPT/IRPT_DASHBD/task-orders/IRPT_DASHBD.TO-DB-b-295.publisher-writes-history-scope-pair.md"
PUBDIR = "infra/aws/lambda/investor-reporting/reporting-publish"
COTDIR = "infra/aws/lambda/investor-reporting/reporting-publish-cot"
PUB_REL, H49_REL, HCOT_REL = PUBDIR + "/publisher.py", PUBDIR + "/handler.py", COTDIR + "/handler.py"
TEST_REL = PUBDIR + "/tests/test_history_scope_pair.py"
CONTRACT_REL = "org/standards/IRPT_DASHBD_SERIES_CONTRACT.json"
PINNED_TESTS = [PUBDIR + "/tests/test_publisher_claim_calendar.py", PUBDIR + "/tests/test_publisher_unreported.py", PUBDIR + "/tests/test_handler_unreported.py", COTDIR + "/tests/test_handler.py"]
GRANT_FILES = {PUB_REL, H49_REL, HCOT_REL, TEST_REL} | set(PINNED_TESTS)
GRANT_PREFIXES = (D + AUTHOR + "/", "org/missions/D9/IRPT/IRPT_DASHBD/surprise-channel/investigations/", "org/missions/D9/IRPT/IRPT_DASHBD/task-orders/")
MAX_PIN_LINES = 20
CLAIM_KEY, BASIS_KEY, CLAIM, BASIS = "history_scope_claim", "history_scope_basis", "inferred", "first value day vs source floor"
VERSION = "0.4.0"
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


def base_commit(root):
    out = git(root, "log", "--diff-filter=A", "--format=%H", "--", ORDER_REL).decode().split()
    need(out, "the order's first commit is not in this history")
    return out[-1]


def own_commits(root):
    out = git(root, "log", "--reverse", "--format=%H", "--author=" + AUTHOR, base_commit(root) + "..HEAD").decode().split()
    need(out, "no commit by %s since the order was issued" % AUTHOR)
    return out


def helper(rel, name):
    spec = importlib.util.spec_from_file_location(name, str(HERE.parent / rel))
    mod = importlib.util.module_from_spec(spec)
    sys.modules[name] = mod
    spec.loader.exec_module(mod)
    return mod


# ------------------------------------------------------------------------------------------------ AC1: the publisher
def gold_row(d, i, claim=None, with_claim_key=False):
    row = {"business_date": d, "market_value_eod": 100.0 + i, "total_return_daily": None if i == 0 else 0.001, "return_basis": "NOT_MEASURABLE" if i == 0 else "TWR",
           "day_quality": "NOT_MEASURABLE" if i == 0 else "MEASURED", "external_flow": 0.0, "income_received": 0.0, "holdings_price_return": None, "method_version": 3, "history_scope": "FULL"}
    if with_claim_key:
        row[CLAIM_KEY] = claim
    return row


def check_publisher(root, mutate=None):
    pub = load_pub(root)
    if mutate:
        mutate(pub)
    contract = json.loads((Path(root) / CONTRACT_REL).read_bytes().decode("utf-8"))
    need(pub.PUBLISHER_VERSION == VERSION, "PUBLISHER_VERSION must be %s, got %s" % (VERSION, pub.PUBLISHER_VERSION))
    need(tuple(pub.GOLD_CONDITIONAL_COLUMNS) == (CLAIM_KEY,) and CLAIM_KEY not in pub.GOLD_COLUMNS, "GOLD_CONDITIONAL_COLUMNS must be (%s,) and GOLD_COLUMNS must not name it" % CLAIM_KEY)
    days = ["2026-07-06", "2026-07-07", "2026-07-08"]
    derived = [gold_row(d, i, CLAIM, True) for i, d in enumerate(days)]
    s = pub.build_series(derived)
    need(s.get(CLAIM_KEY) == CLAIM and s.get(BASIS_KEY) == BASIS, "a newest row carrying the claim must write the pair (%s = %s, %s = %r)" % (CLAIM_KEY, CLAIM, BASIS_KEY, BASIS))
    gz, _ = pub.series_bytes(s)
    man = pub.build_manifest("A1", "firmx", s, len(gz))
    bad = pub.validate_against_contract(s, man, contract)
    need(not bad, "a series with the pair must validate against the series contract: %s" % bad[:2])
    legacy = [gold_row(d, i) for i, d in enumerate(days)]
    s0 = pub.build_series(legacy)
    need(CLAIM_KEY not in s0 and BASIS_KEY not in s0, "rows without the claim key must write NO pair")
    none_claim = [gold_row(d, i, None, True) for i, d in enumerate(days)]
    s1 = pub.build_series(none_claim)
    need(CLAIM_KEY not in s1 and BASIS_KEY not in s1, "rows whose claim is null must write NO pair")
    older_only = [gold_row(days[0], 0, CLAIM, True), gold_row(days[1], 1, CLAIM, True), gold_row(days[2], 2)]
    s2 = pub.build_series(older_only)
    need(CLAIM_KEY not in s2, "the NEWEST row decides: a claim on older rows only writes no pair")
    newest_only = [gold_row(days[0], 0), gold_row(days[1], 1), gold_row(days[2], 2, CLAIM, True)]
    s3 = pub.build_series(newest_only)
    need(s3.get(CLAIM_KEY) == CLAIM and s3.get(BASIS_KEY) == BASIS, "the NEWEST row decides: a claim on the newest row writes the pair")
    try:
        pub.build_series([gold_row(days[0], 0), gold_row(days[1], 1, "measured", True)])
    except pub.PublishRefused:
        pass
    else:
        raise Fail("a claim with any word but %s must be refused" % CLAIM)
    lone = dict(s)
    lone.pop(BASIS_KEY)
    need(pub.validate_against_contract(lone, man, contract), "a series with a lone claim must fail validation")
    lone2 = dict(s)
    lone2.pop(CLAIM_KEY)
    need(pub.validate_against_contract(lone2, man, contract), "a series with a lone basis must fail validation")
    wrong = dict(s)
    wrong[CLAIM_KEY] = "held"
    need(pub.validate_against_contract(wrong, man, contract), "a series with another claim word must fail validation")
    wrong2 = dict(s)
    wrong2[BASIS_KEY] = "free text"
    need(pub.validate_against_contract(wrong2, man, contract), "a series with a free-text basis must fail validation")
    return True


def load_pub(root):
    for p in (Path(root) / PUBDIR,):
        if str(p) not in sys.path:
            sys.path.insert(0, str(p))
    sys.modules.pop("publisher", None)
    return helper_load(Path(root) / PUB_REL, "publisher")


def helper_load(path, name):
    spec = importlib.util.spec_from_file_location(name, str(path))
    mod = importlib.util.module_from_spec(spec)
    sys.modules[name] = mod
    spec.loader.exec_module(mod)
    return mod


# ------------------------------------------------------------------------------------------------ AC2: the handlers
COLS = ["account_id", "business_date", "market_value_eod", "total_return_daily", "return_basis", "day_quality", "external_flow", "income_received", "holdings_price_return", "method_version", "history_scope"]


def gold(h, tc, naming, firm, days, claim_days, floor_label):
    """FakeS3 holding gold for `firm` over `days`: accounts A (every day) and B (second day on); the partitions named in claim_days carry the conditional column (A: inferred, B: inferred)."""
    probe = str(naming.address("irpt", firm, "gold", "account_return_daily", "date=2026-07-10", "data.parquet"))
    prefix = probe[len("s3://"):].partition("/")[2].rsplit("/date=", 1)[0] + "/"
    objs = {}
    for i, d in enumerate(days):
        rows = []
        for acct, start in (("A0000000001", 0), ("B0000000002", 1)):
            if i < start:
                continue
            k = i - start
            r = {"account_id": acct, "business_date": d, "market_value_eod": 100.0 + k, "total_return_daily": None if k == 0 else 0.001, "return_basis": "NOT_MEASURABLE" if k == 0 else "TWR",
                 "day_quality": "NOT_MEASURABLE" if k == 0 else "MEASURED", "external_flow": 0.0, "income_received": 0.0, "holdings_price_return": None, "method_version": 3,
                 "history_scope": "PARTIAL_HISTORY" if acct.startswith("A") else "FULL"}
            if d in claim_days:
                r[CLAIM_KEY] = CLAIM
            rows.append(r)
        cols = COLS + ([CLAIM_KEY] if d in claim_days else [])
        objs["%sdate=%s/data.parquet" % (prefix, d)] = h.parquet_bytes(rows, cols)
    return h.FakeS3(objs)


def read_series(h, naming, firm, s3, acct):
    s = json.loads(gzip.decompress(s3.puts[h.series_key(naming, firm, acct, "series.json.gz")]).decode("utf-8"))
    m = json.loads(s3.puts[h.series_key(naming, firm, acct, "manifest.json")].decode("utf-8"))
    return s, m


def check_handlers(root, mutate=None):
    root = Path(root)
    h = helper("r147/p148_cothandler.py", "p148_helper")
    p160 = helper("r149/p160_pub49f.py", "p160_helper")
    naming = h.load_module(root / "lib" / "opal_naming.py", "opal_naming")
    tc = h.load_module(root / "lib" / "trading_calendar.py", "trading_calendar")
    contract = json.loads((root / CONTRACT_REL).read_bytes().decode("utf-8"))
    days = h.trading(tc, "2026-07-10", "2026-07-17")
    # ---- the 49 Financial handler
    for p in (root / PUBDIR, root / "lib", root):
        if str(p) not in sys.path:
            sys.path.insert(0, str(p))
    sys.modules.pop("publisher", None)
    mod = h.load_module(root / H49_REL, "f49_handler_295")
    if mutate:
        mutate(sys.modules["publisher"])
    firm = mod.resolve_firm(None)[1]
    for label, claim_days, want_pair in (("every partition carries the claim", set(days), True), ("no partition carries it (legacy gold)", set(), False), ("only the newer partitions carry it (mixed schemas)", set(days[3:]), True)):
        s3 = gold(h, tc, naming, firm, days, claim_days, "49f")
        res = mod.run(accounts=None, upload=True, s3=s3, contract=contract)
        need(len(res) == 2 and all(r["ok"] for r in res), "49F %s: both accounts must publish: %s" % (label, [r.get("error") for r in res if not r["ok"]][:2]))
        for acct in ("A0000000001", "B0000000002"):
            s, m = read_series(h, naming, firm, s3, acct)
            if want_pair:
                need(s.get(CLAIM_KEY) == CLAIM and s.get(BASIS_KEY) == BASIS, "49F %s: %s's series must carry the pair" % (label, acct[:1]))
            else:
                need(CLAIM_KEY not in s and BASIS_KEY not in s, "49F %s: %s's series must carry NO pair" % (label, acct[:1]))
            need(m["publisher_version"] == VERSION, "49F %s: the manifest's publisher_version must be %s" % (label, VERSION))
    # ---- the Cottonwood handler
    sys.modules.pop("publisher", None)
    cot = h.load_module(root / HCOT_REL, "cot_handler_295")
    if mutate:
        mutate(sys.modules["publisher"])
    cfirm = cot.FIRM
    cdays = h.trading(tc, cot.FLOOR_DAY, "2026-07-24")
    for label, claim_days, want_pair in (("every partition carries the claim", set(cdays), True), ("no partition carries it (legacy gold)", set(), False)):
        s3 = gold(h, tc, naming, cfirm, cdays, claim_days, "cot")
        out = cot.lambda_handler({"upload": True}, None, s3)
        need(out["published"] == 2 and out["refused"] == 0, "Cottonwood %s: both accounts must publish, got %s published and %s refused" % (label, out["published"], out["refused"]))
        for acct in ("A0000000001", "B0000000002"):
            s, m = read_series(h, naming, cfirm, s3, acct)
            if want_pair:
                need(s.get(CLAIM_KEY) == CLAIM and s.get(BASIS_KEY) == BASIS, "Cottonwood %s: %s's series must carry the pair" % (label, acct[:1]))
            else:
                need(CLAIM_KEY not in s and BASIS_KEY not in s, "Cottonwood %s: %s's series must carry NO pair" % (label, acct[:1]))
            need(m["publisher_version"] == VERSION, "Cottonwood %s: publisher_version %s" % (label, VERSION))
    del p160
    return True


# ------------------------------------------------------------------------------------------------ grant, facts, tests
def check_grant(changed):
    bad = [f for f in changed if f not in GRANT_FILES and not f.startswith(GRANT_PREFIXES)]
    need(not bad, "the worker's commits touch files outside its grant: %s" % bad[:3])
    need(PUB_REL in changed and H49_REL in changed and HCOT_REL in changed and TEST_REL in changed, "the publisher, both handlers and the new test file must all change")
    return True


def check_facts(rec, n_tests):
    exp = {"publisher_version", "pair", "newest_row_decides", "handlers", "pinned_test_lines", "tests", "words"}
    need(isinstance(rec, dict) and set(rec) == exp, "record keys differ: %s" % (sorted(set(rec) ^ exp) if isinstance(rec, dict) else "?"))
    need(rec["publisher_version"] == VERSION and rec["pair"] == [CLAIM_KEY, BASIS_KEY] and rec["newest_row_decides"] is True and rec["handlers"] == ["reporting-publish", "reporting-publish-cot"], "version, pair, rule or handlers differ")
    need(isinstance(rec["pinned_test_lines"], int) and not isinstance(rec["pinned_test_lines"], bool) and 0 <= rec["pinned_test_lines"] <= MAX_PIN_LINES, "pinned_test_lines: a whole number, at most %d" % MAX_PIN_LINES)
    need(isinstance(rec["tests"], int) and not isinstance(rec["tests"], bool) and rec["tests"] == n_tests >= 10, "tests must equal the recount, at least 10")
    need(nes(rec["words"]) and 80 <= len(rec["words"]) <= 1800 and not LONG_DIGITS.findall(rec["words"]), "words must be one paragraph of 80 to 1800 characters with no long digit run")
    return True


def run_pytest(root, args):
    r = subprocess.run([sys.executable, "-m", "pytest", "-q", "-p", "no:cacheprovider"] + list(args), cwd=str(root), capture_output=True, text=True, timeout=900)
    m = re.search(r"(\d+) passed", r.stdout)
    need(r.returncode == 0 and m is not None, "tests failed: %s" % r.stdout[-300:].replace("\n", " | "))
    return int(m.group(1))


def run(root, cid):
    root = Path(root)
    if cid == "DB163-1-AC1":
        check_publisher(root)
        print("OK: publisher %s writes history_scope_claim = inferred and history_scope_basis (the fixed text) when the NEWEST gold row carries the claim, writes no pair for legacy or null-claim rows or a claim on older rows only, refuses any other claim word, and validates the pair against series contract 0.3.3 (a lone field, another word or a free-text basis fail)" % VERSION)
        return True
    if cid == "DB163-1-AC2":
        check_handlers(root)
        print("OK: both publish handlers read the conditional gold column only from a partition that has it: with the claim in every partition (or only the newer ones) the series carry the pair, with legacy gold none, and every manifest says publisher %s" % VERSION)
        return True
    if cid == "DB163-1-AC3":
        need((root / TEST_REL).is_file(), "no %s" % TEST_REL)
        n = run_pytest(root, [TEST_REL])
        n_p = run_pytest(root, [PUBDIR + "/tests", COTDIR])
        need(n >= 10, "the new test file holds %d passing tests, at least 10 are owed" % n)
        edited = 0
        for cm in own_commits(root):
            for f in PINNED_TESTS:
                for ln in git(root, "show", "--numstat", "--format=", cm, "--", f).decode().split("\n"):
                    p = ln.split("\t")
                    if len(p) == 3 and p[0].isdigit() and p[1].isdigit():
                        edited += int(p[0]) + int(p[1])
        need(edited <= MAX_PIN_LINES, "the earlier tests may change by at most %d lines (the version pins), read %d" % (MAX_PIN_LINES, edited))
        changed = set()
        for cm in own_commits(root):
            changed |= set(git(root, "show", "--name-only", "--format=", cm).decode().split())
        check_grant(changed)
        rec = json.loads((root / REC_REL).read_bytes().decode("utf-8"))
        check_facts(rec, n)
        need(rec["pinned_test_lines"] == edited, "pinned_test_lines must equal the recount %d" % edited)
        print("OK: %d new tests pass; the publisher and handler test directories pass (%d tests) with %d forced pin lines (at most %d); %d files changed, all in the grant; the facts record equals the recount" % (n, n_p, edited, MAX_PIN_LINES, len(changed)))
        return True
    raise Fail("unknown criterion %s" % cid)


def selftest():
    def red(fn, label):
        try:
            fn()
        except Fail:
            return
        raise AssertionError("red arm passed: " + label)
    assert check_grant({PUB_REL, H49_REL, HCOT_REL, TEST_REL, PINNED_TESTS[0], D + AUTHOR + "/x.json"})
    red(lambda: check_grant({PUB_REL, H49_REL, TEST_REL}), "no cot handler")
    red(lambda: check_grant({PUB_REL, H49_REL, HCOT_REL, TEST_REL, "lib/x.py"}), "outside grant")
    rec = {"publisher_version": VERSION, "pair": [CLAIM_KEY, BASIS_KEY], "newest_row_decides": True, "handlers": ["reporting-publish", "reporting-publish-cot"], "pinned_test_lines": 6, "tests": 10, "words": "w" * 100}
    assert check_facts(rec, 10)
    farms = (("version", lambda r: r.update(publisher_version="0.3.0")), ("pair", lambda r: r.update(pair=[CLAIM_KEY])), ("rule", lambda r: r.update(newest_row_decides=False)), ("handlers", lambda r: r.update(handlers=["x"])),
             ("pin lines", lambda r: r.update(pinned_test_lines=99)), ("tests", lambda r: r.update(tests=11)), ("extra", lambda r: r.update(z=1)), ("words", lambda r: r.update(words="short")),
             ("digits", lambda r: r.update(words="w" * 100 + " 123456789")))
    for label, fn in farms:
        r2 = copy.deepcopy(rec)
        fn(r2)
        red(lambda: check_facts(r2, 10), label)
    print("selftest: grant (2) and facts (%d) clauses behave; the behaviour clauses are exercised against a scratch reference and single-fault mutants by the issuer" % len(farms))
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
