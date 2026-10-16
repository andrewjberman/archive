"""IRPT_DASHBD round 146, workstream B-49F + contract (issuer 2.0.0_SA_COO~D2, the contract's sole writer) -- DB-b-278, the SERIES contract 0.3.0: the carrier of the unreported-days statement
(PRD ADDENDUM v0.16 item 4, CTO msg 8796): two fields, `unreported_trading_days` (the ISO dates of the window's trading days the source did not report; always present on a series that carries the
statement, `[]` when there are none) and `unreported_trading_days_basis` (the fixed text "trading calendar minus present partitions"), written from the report-build output's statement.
They enter `series.optional`, so every earlier series (every other firm's, written without a statement) still validates; on a series from a source that carries the statement they are a PAIR and are
never omitted. The contract and its first writer (the first Cottonwood series publish, a later cell of the contract's own issuer after the CTO's msg 8803) land in ONE drain. LOCAL: one JSON standard and one new test file.

  DB-b-278 (~225)   org/standards/IRPT_DASHBD_SERIES_CONTRACT.json (0.3.0) + data/assets/scripts/gold/irpt_reporting/tests/test_series_contract_030.py + a facts record
                    DB146-1-AC1 (the contract's declarations, pure, and the grant),
                    DB146-1-AC2 (BEHAVIOUR: a reference validator driven ONLY by the contract's declarations accepts four series and rejects eleven),
                    DB146-1-AC3 (the worker's tests pass beside the publisher's tests and the portal's series-contract test; the facts record equals the contract)

Usage: python <this file> <repo_root> <criterion_id>      prints "<id> PASS" or "<id> FAIL" last
       python <this file> --selftest                       the pure clauses on synthetic arms
"""
import copy
import datetime as dt
import hashlib
import json
import re
import shutil
import subprocess
import sys
from pathlib import Path

D = "org/missions/D9/IRPT/IRPT_DASHBD/deliverables/"
CONTRACT_REL = "org/standards/IRPT_DASHBD_SERIES_CONTRACT.json"
TEST_REL = "data/assets/scripts/gold/irpt_reporting/tests/test_series_contract_030.py"
PUBLISHER_TEST = "infra/aws/lambda/investor-reporting/reporting-publish/tests/test_publisher.py"
PORTAL_TEST = "src/pages/InvestorReporting/__tests__/dsgn-irptv1/iv-e-124.series-contract.test.ts"
REC_REL = D + "0.9.0_WK_IRPT_DASHBD~225/RD_SERIES_CONTRACT_030_FACTS_R146.json"
ORDER_REL = "org/missions/D9/IRPT/IRPT_DASHBD/task-orders/IRPT_DASHBD.TO-DB-b-278.series-contract-030-unreported-trading-days-fields.md"
AUTHOR = "0.9.0_WK_IRPT_DASHBD~225"
GRANT_FILES = {CONTRACT_REL, TEST_REL}
GRANT_PREFIXES = (D + "0.9.0_WK_IRPT_DASHBD~225/", "org/missions/D9/IRPT/IRPT_DASHBD/surprise-channel/investigations/", "org/missions/D9/IRPT/IRPT_DASHBD/task-orders/")
BASE_FILE_SHA = "2f0cb189ad07bef091269d5db9b36ccf23748c836af0fa7b3791f1df2f9764ea"  # the bytes of 0.2.0, the lineage entry this edit appends
SHA = {"required": "89b3ca0d4407d41970dfd3f576f99df590d729df9b107a7e4f5bed4f206d3906", "array_keys": "bc5e84d735776497f55e649d3ee17c4b019874e26fbcf741fd9381172d5976ab",
       "optional": "3db2c3678792570743d1d145ddd0589d175a703dbd652dc3e817c50158ac3b4b", "shape": "f121017b9ffc8be7662ee47cb404dba10670c254fa3b5c068aa107a4837d9513",
       "fields": "e7aba83b3debfe711598df1c54c657cc279723e336ff84acf5be1c35d379199d", "manifest": "d7fd5284ed0eef52b0d07e8cbef468821221b14cc13046297664dcfc928cf8b3",
       "model_windows": "e64a4513caae6ec0ebe349212f11918e704b0163f548dfa5199212328a632dce", "open_changes": "b1b4702a8ba79a8db0e26328f1f0a5c37d4cd7e789f52e406b17233e2fe0579d",
       "files": "9ff0692a5cdb2fb70609460dfd954810ab339c4051e3f5d7e075680a60d0a3d2", "change_rule": "bcc5e64cc95aa71a3d9a4d3ff554fbd95426724195f6a0d76d102feac3b9e2e2",
       "lineage": "1164cf54532032aef6799dbf67d6975a0c3573fbc6e605def89c88900f71388c", "prd_contracts": "7d1ea253a04bb693830f6b29ef814d28daa3d687491a67e43e4a941435186522", "source_table_contract": "6e1ae666a3b12ba3c610d8ebc606a258127c981ac102c62798542a78fa6889ac",
       "writer": "575566759a1ed72c98a7977328bcdbbc6315dab053230711cd33d4996f8ee410", "reader": "b5db6d16abe98c41962016e8aae4d24df9b8a997929e456ea661af52314b348a"}
NEW = ("unreported_trading_days", "unreported_trading_days_basis")
FIXED = "trading calendar minus present partitions"
LONG_DIGITS = re.compile(r"\d{8,}")
ISO = re.compile(r"\d{4}-\d{2}-\d{2}$")


class Fail(Exception):
    pass


def need(cond, msg):
    if not cond:
        raise Fail(msg)


def nes(x):
    return isinstance(x, str) and x.strip() != ""


def sha(x):
    return hashlib.sha256(json.dumps(x, sort_keys=True, separators=(",", ":")).encode()).hexdigest()


def load_json(root, rel):
    p = Path(root) / rel
    need(p.is_file(), "no %s" % rel)
    return json.loads(p.read_bytes().decode("utf-8"))


def git(root, *a):
    r = subprocess.run(["git", "-C", str(root)] + list(a), capture_output=True, text=True)
    need(r.returncode == 0, "git %s: %s" % (" ".join(a[:2]), r.stderr.strip()[:200]))
    return r.stdout


def own_commits(root):
    base = git(root, "log", "--diff-filter=A", "--format=%H", "--", ORDER_REL).split()
    need(base, "the order's first commit is not in this history")
    out = git(root, "log", "--reverse", "--format=%H", "--author=" + AUTHOR, base[-1] + "..HEAD").split()
    need(out, "no commit by %s since the order was issued" % AUTHOR)
    return out


# ------------------------------------------------------------------------------------------------ the pure clauses
def check_contract(c):
    need(c.get("contract_version") == "0.3.0", "contract_version is not 0.3.0 (a minor bump)")
    lin = c.get("lineage")
    need(isinstance(lin, list) and len(lin) == 2 and lin[1].get("contract_version") == "0.2.0" and lin[1].get("sha256") == BASE_FILE_SHA and nes(lin[1].get("note")),
         "lineage must keep its first entry and add the 0.2.0 entry with the sha256 of the 0.2.0 bytes %s" % BASE_FILE_SHA[:12])
    s = c["series"]
    for k in ("required", "array_keys", "shape"):
        need(sha(s[k]) == SHA[k], "series.%s changed" % k)
    need(s["optional"] == ["class_value", "class_weight", "class_names"] + list(NEW), "series.optional must be the three earlier names then %s" % list(NEW))
    f = s["fields"]
    need(isinstance(f, dict) and all(k in f for k in NEW) and sha({k: v for k, v in f.items() if k not in NEW}) == SHA["fields"], "an earlier series field changed, or a new field is missing or another was added")
    u, b = f[NEW[0]], f[NEW[1]]
    need(isinstance(u, dict) and set(u) == {"kind", "source", "sentence"} and u["kind"] == "scalar list of string", "%s: kind 'scalar list of string', source, sentence" % NEW[0])
    need("unreported_days" in u["source"] and "report-build" in u["source"], "%s.source must name the report-build output's statement and its key unreported_days" % NEW[0])
    sent = u["sentence"]
    need(all(w in sent for w in ("ISO", "[]", "never omitted", "strictly increasing", "window", "trading")), "%s.sentence must say: ISO dates, [] when none, never omitted, strictly increasing, the window, trading days" % NEW[0])
    need(isinstance(b, dict) and set(b) == {"kind", "source", "fixed_value", "sentence"} and b["kind"] == "scalar string" and b["fixed_value"] == FIXED and nes(b["source"]) and "fixed" in b["sentence"],
         "%s: kind 'scalar string', source, fixed_value exactly %r, a sentence saying fixed" % (NEW[1], FIXED))
    r = c.get("unreported_days_rule")
    need(isinstance(r, dict) and set(r) == {"present_when", "pair", "empty", "window", "absent_means"} and all(nes(v) for v in r.values()), "unreported_days_rule must hold exactly present_when, pair, empty, window and absent_means, in words")
    need("report-build" in r["present_when"] and "both" in r["pair"] and "neither" in r["pair"] and "[]" in r["empty"] and "first_data_date" in r["window"] and "as_of" in r["window"] and "`date`" in r["window"]
         and "no statement" in r["absent_means"], "unreported_days_rule must name the report-build statement, the pair (both or neither), [], the window (first_data_date, as_of, `date`) and 'no statement'")
    for k in ("manifest", "model_windows", "open_changes", "files", "change_rule", "prd_contracts", "source_table_contract", "writer", "reader"):
        need(sha(c[k]) == SHA[k], "%s changed" % k)
    need(sha([lin[0]]) == SHA["lineage"], "the first lineage entry changed")
    return True


def series_problems(c, series):
    """A reference validator driven ONLY by the contract's declarations (the two new fields and the keys they lean on). Returns the list of problems."""
    out = []
    for k in c["series"]["required"]:
        if k not in series:
            out.append("required key %s is missing" % k)
    has = [k in series for k in NEW]
    if any(has) and not all(has):
        out.append("the two unreported-days fields are a pair: both or neither")
    fixed = c["series"]["fields"][NEW[1]]["fixed_value"]
    if NEW[1] in series and series[NEW[1]] != fixed:
        out.append("the basis must read exactly %r" % fixed)
    if NEW[0] in series:
        v = series[NEW[0]]
        if not isinstance(v, list):
            out.append("unreported_trading_days must be a list ([] when none)")
        else:
            if not all(isinstance(x, str) and ISO.match(x) for x in v):
                out.append("every date must be ISO")
            else:
                if v != sorted(set(v)):
                    out.append("the dates must be strictly increasing")
                first, last, present = series.get("first_data_date"), series.get("as_of"), set(series.get("date", []))
                for x in v:
                    if not (first < x <= last):
                        out.append("%s lies outside the window (after first_data_date, up to as_of)" % x)
                    if x in present:
                        out.append("%s is a present day, not an unreported one" % x)
    return out


def base_series(c):
    s = {}
    for k in c["series"]["required"]:
        s[k] = None
    s.update({"date": ["2026-08-17", "2026-08-18", "2026-08-20", "2026-08-21"], "first_data_date": "2026-08-17", "as_of": "2026-08-21"})
    return s


def check_behaviour(c):
    def mk(**kw):
        x = base_series(c)
        x.update(kw)
        return x
    good = [("an earlier series (neither field)", mk()), ("a series with [] and the basis", mk(unreported_trading_days=[], unreported_trading_days_basis=FIXED)),
            ("a series with one unreported day", mk(unreported_trading_days=["2026-08-19"], unreported_trading_days_basis=FIXED)),
            ("a series with two unreported days", mk(date=["2026-08-17", "2026-08-21"], unreported_trading_days=["2026-08-18", "2026-08-20"], unreported_trading_days_basis=FIXED))]
    bad = [("the list without the basis", mk(unreported_trading_days=["2026-08-19"])), ("the basis without the list", mk(unreported_trading_days_basis=FIXED)),
           ("a basis of other words", mk(unreported_trading_days=[], unreported_trading_days_basis="calendar")), ("a null list", mk(unreported_trading_days=None, unreported_trading_days_basis=FIXED)),
           ("a non-ISO date", mk(unreported_trading_days=["19 Aug 2026"], unreported_trading_days_basis=FIXED)),
           ("a date before first_data_date", mk(unreported_trading_days=["2026-08-14"], unreported_trading_days_basis=FIXED)),
           ("a date after as_of", mk(unreported_trading_days=["2026-08-24"], unreported_trading_days_basis=FIXED)),
           ("a date that is a present day", mk(unreported_trading_days=["2026-08-18"], unreported_trading_days_basis=FIXED)),
           ("a duplicated date", mk(date=["2026-08-17", "2026-08-21"], unreported_trading_days=["2026-08-19", "2026-08-19"], unreported_trading_days_basis=FIXED)),
           ("an unsorted list", mk(date=["2026-08-17", "2026-08-21"], unreported_trading_days=["2026-08-20", "2026-08-18"], unreported_trading_days_basis=FIXED)),
           ("a string for the list", mk(unreported_trading_days="2026-08-19", unreported_trading_days_basis=FIXED))]
    for label, row in good:
        p = series_problems(c, row)
        need(not p, "%s must validate: %s" % (label, p))
    for label, row in bad:
        need(series_problems(c, row), "%s must be rejected" % label)
    return len(good), len(bad)


def check_grant(changed):
    bad = [f for f in changed if f not in GRANT_FILES and not f.startswith(GRANT_PREFIXES)]
    need(not bad, "the worker's commits touch files outside its grant: %s" % bad[:3])
    need(CONTRACT_REL in changed and TEST_REL in changed, "the contract and its test must both change")
    return True


def check_facts(rec, c):
    exp = {"contract_version", "lineage_sha256", "optional", "fixed_value", "words"}
    need(isinstance(rec, dict) and set(rec) == exp, "record keys differ: %s" % (sorted(set(rec) ^ exp) if isinstance(rec, dict) else "?"))
    need(rec["contract_version"] == "0.3.0" and rec["lineage_sha256"] == BASE_FILE_SHA and rec["optional"] == c["series"]["optional"] and rec["fixed_value"] == FIXED, "version, lineage sha256, optional list or fixed value differ from the contract")
    need(nes(rec["words"]) and 80 <= len(rec["words"]) <= 1800 and not LONG_DIGITS.findall(rec["words"]), "words must be one paragraph of 80 to 1800 characters with no long digit run")
    return True


def run_pytest(root, files):
    r = subprocess.run([sys.executable, "-m", "pytest", "-q", "-p", "no:cacheprovider"] + list(files), cwd=str(root), capture_output=True, text=True, timeout=600)
    m = re.search(r"(\d+) passed", r.stdout)
    need(r.returncode == 0 and m is not None, "tests failed: %s" % r.stdout[-300:].replace("\n", " | "))
    return int(m.group(1))


def run_portal_test(root):
    portal = Path(root) / "portal"
    need((portal / PORTAL_TEST).is_file(), "the portal's series-contract test %s is missing" % PORTAL_TEST)
    b = shutil.which("bun")
    need(b, "bun is not on PATH")
    r = subprocess.run([b, "test", PORTAL_TEST], cwd=str(portal), capture_output=True, text=True, timeout=300)
    need(r.returncode == 0, "the portal's series-contract test failed against the new contract: %s" % (r.stdout + r.stderr)[-300:].replace("\n", " | "))


def run(root, cid):
    root = Path(root)
    c = load_json(root, CONTRACT_REL)
    if cid == "DB146-1-AC1":
        check_contract(c)
        changed = set()
        for cm in own_commits(root):
            changed |= set(git(root, "show", "--name-only", "--format=", cm).split())
        check_grant(changed)
        print("OK: series contract 0.3.0: the sections and the 16 earlier fields are byte-identical; series.optional gains %s; the lineage appends the 0.2.0 bytes; the rule is in words; %d files changed, all in the grant" % (list(NEW), len(changed)))
        return True
    if cid == "DB146-1-AC2":
        check_contract(c)
        g, b = check_behaviour(c)
        print("OK: behaviour: a validator driven only by the contract accepts %d series (an earlier one, [] with the basis, one and two unreported days) and rejects %d (a lone field, wrong basis, null, non-ISO, outside the window, a present day, duplicate, unsorted, a string)" % (g, b))
        return True
    if cid == "DB146-1-AC3":
        need((root / TEST_REL).is_file(), "no %s" % TEST_REL)
        n_new = run_pytest(root, [TEST_REL])
        need(n_new >= 10, "the new test file holds %d passing tests, at least 10 are owed" % n_new)
        n_pub = run_pytest(root, [PUBLISHER_TEST])
        run_portal_test(root)
        check_facts(load_json(root, REC_REL), c)
        print("OK: %d new tests, the publisher's %d tests and the portal's series-contract test pass against the new contract; facts record equals the contract" % (n_new, n_pub))
        return True
    raise Fail("unknown criterion %s" % cid)


def selftest():
    def red(fn, label):
        try:
            fn()
        except Fail:
            return
        raise AssertionError("red arm passed: " + label)
    c = {"series": {"required": ["date", "first_data_date", "as_of", "value"], "fields": {NEW[1]: {"fixed_value": FIXED}}}}
    g, b = check_behaviour(c)
    assert (g, b) == (4, 11), (g, b)
    c2 = copy.deepcopy(c)
    c2["series"]["fields"][NEW[1]]["fixed_value"] = "other"
    red(lambda: check_behaviour(c2), "a different fixed value rejects the packet's basis")
    assert check_grant({CONTRACT_REL, TEST_REL, D + "0.9.0_WK_IRPT_DASHBD~225/x.json"})
    red(lambda: check_grant({CONTRACT_REL, TEST_REL, "lib/x.py"}), "outside grant")
    red(lambda: check_grant({CONTRACT_REL}), "no test")
    red(lambda: check_grant({TEST_REL}), "no contract")
    rec = {"contract_version": "0.3.0", "lineage_sha256": BASE_FILE_SHA, "optional": ["class_value", "class_weight", "class_names"] + list(NEW), "fixed_value": FIXED, "words": "w" * 100}
    cc = {"series": {"optional": list(rec["optional"])}}
    assert check_facts(rec, cc)
    arms = (("version", lambda r: r.update(contract_version="0.2.0")), ("lineage", lambda r: r.update(lineage_sha256="0" * 64)), ("optional", lambda r: r.update(optional=[])), ("fixed", lambda r: r.update(fixed_value="x")),
            ("words", lambda r: r.update(words="short")), ("extra", lambda r: r.update(z=1)), ("digits", lambda r: r.update(words="w" * 100 + " 123456789")))
    for label, fn in arms:
        r2 = dict(rec)
        fn(r2)
        red(lambda: check_facts(r2, cc), label)
    d = dt.date(2026, 8, 19)
    assert d.isoformat() == "2026-08-19"
    print("selftest: behaviour (1 red arm, 4 good and 11 bad series), grant (3) and facts (%d red arms) clauses behave" % len(arms))
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
