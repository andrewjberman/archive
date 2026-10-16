"""IRPT_DASHBD round 148, workstream CONTRACT (issuer 2.0.0_SA_COO~D2, the contract's sole writer) -- DB-b-285, the SERIES contract 0.3.1 (CTO round-146 analysis msg 9057 and round-147 analysis msg 9060):
(1) `income_claim` is carried through to the series: an OPTIONAL string field `income_claim` = "absent" with the fixed reason SOURCE_REPORTS_NO_INCOME, present exactly when every `income` entry is null;
(2) `unreported_trading_days_basis` is marked `const` with a one-line rule-24 note; (3) the manifest gains an OPTIONAL field `calendar_source` (pandas_market_calendars or fallback_2010_2027).
Everything else stays byte-identical. The page's mirror (portal `seriesContract.ts` and the iv-e-124 parity test) is `2.0.0_SA_COO~C2`'s named reader cell: this order does not run or edit it.
LOCAL: a JSON standard, a test file and at most 14 changed lines of the 0.3.0 test file.

  DB-b-285 (~229)   org/standards/IRPT_DASHBD_SERIES_CONTRACT.json (0.3.1) + data/assets/scripts/gold/irpt_reporting/tests/test_series_contract_031.py + a facts record
                    DB153-1-AC1 (the contract differs from the base ONLY in the allowed places),
                    DB153-1-AC2 (BEHAVIOUR: a reference validator driven only by the declarations accepts six and rejects nine),
                    DB153-1-AC3 (the new tests, the 0.3.0 tests and the publisher's tests, the grant, the facts record)

Usage: python <this file> <repo_root> <criterion_id>      prints "<id> PASS" or "<id> FAIL" last
       python <this file> --selftest                       the pure clauses on synthetic arms
"""
import copy
import hashlib
import json
import re
import subprocess
import sys
from pathlib import Path

D = "org/missions/D9/IRPT/IRPT_DASHBD/deliverables/"
CONTRACT_REL = "org/standards/IRPT_DASHBD_SERIES_CONTRACT.json"
TEST_DIR = "data/assets/scripts/gold/irpt_reporting/tests/"
TEST_REL = TEST_DIR + "test_series_contract_031.py"
TEST030 = TEST_DIR + "test_series_contract_030.py"
PUBLISHER_TESTS = "infra/aws/lambda/investor-reporting/reporting-publish/tests"
AUTHOR = "0.9.0_WK_IRPT_DASHBD~229"
REC_REL = D + AUTHOR + "/RD_SERIES_CONTRACT_031_FACTS_R148.json"
ORDER_REL = "org/missions/D9/IRPT/IRPT_DASHBD/task-orders/IRPT_DASHBD.TO-DB-b-285.series-contract-031-income-claim-const-basis-calendar-source.md"
GRANT_FILES = {CONTRACT_REL, TEST_REL, TEST030}
GRANT_PREFIXES = (D + AUTHOR + "/", "org/missions/D9/IRPT/IRPT_DASHBD/surprise-channel/investigations/", "org/missions/D9/IRPT/IRPT_DASHBD/task-orders/")
REASON = "SOURCE_REPORTS_NO_INCOME"
BASIS = "unreported_trading_days_basis"
CAL_VALUES = ["pandas_market_calendars", "fallback_2010_2027"]
MAX_TEST030_LINES = 14
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


def base_commit(root):
    out = git(root, "log", "--diff-filter=A", "--format=%H", "--", ORDER_REL).split()
    need(out, "the order's first commit is not in this history")
    return out[-1]


def own_commits(root):
    out = git(root, "log", "--reverse", "--format=%H", "--author=" + AUTHOR, base_commit(root) + "..HEAD").split()
    need(out, "no commit by %s since the order was issued" % AUTHOR)
    return out


# ------------------------------------------------------------------------------------------------ the pure clauses
def check_diff(base, c, base_sha):
    need(base["contract_version"] == "0.3.0", "the base is not 0.3.0: %s" % base["contract_version"])
    need(c.get("contract_version") == "0.3.1", "contract_version is not 0.3.1 (a patch bump)")
    moved = sorted(k for k in set(base) | set(c) if k not in ("contract_version", "lineage", "series", "manifest", "income_claim_rule") and base.get(k) != c.get(k))
    need(not moved, "sections changed beyond the allowed ones: %s" % moved)
    lb, ln = base["lineage"], c["lineage"]
    need(isinstance(ln, list) and len(ln) == len(lb) + 1 and ln[:len(lb)] == lb, "lineage must keep every earlier entry byte-identical and append one")
    need(ln[-1].get("contract_version") == "0.3.0" and ln[-1].get("sha256") == base_sha and nes(ln[-1].get("note")) and len(ln[-1]) == 3, "the appended lineage entry: version 0.3.0, the sha256 of the 0.3.0 file bytes %s, a note" % base_sha[:12])
    sb, sn = base["series"], c["series"]
    for k in sb:
        if k not in ("optional", "fields"):
            need(sb[k] == sn.get(k), "series.%s changed" % k)
    need(set(sn) == set(sb), "series keys changed")
    need(sn["optional"] == sb["optional"] + ["income_claim"], "series.optional must be the five earlier names then income_claim")
    fb, fn = sb["fields"], sn["fields"]
    need(set(fn) == set(fb) | {"income_claim"}, "series.fields must gain exactly income_claim")
    for k in fb:
        if k != BASIS:
            need(fb[k] == fn[k], "series.fields.%s changed" % k)
    nb = fn[BASIS]
    need({k: v for k, v in nb.items() if k not in ("const", "rule24_note")} == fb[BASIS], "the basis field changed beyond const and rule24_note")
    need(nb.get("const") is True and nes(nb.get("rule24_note")) and "\n" not in nb["rule24_note"] and "one value" in nb["rule24_note"].lower() and "no other state" in nb["rule24_note"].lower(),
         "the basis field must carry const true and a ONE-LINE rule24_note saying one value and no other state")
    ic = fn["income_claim"]
    need(isinstance(ic, dict) and set(ic) == {"kind", "source", "fixed_value", "fixed_reason", "sentence"} and ic["kind"] == "scalar string" and ic["fixed_value"] == "absent" and ic["fixed_reason"] == REASON and nes(ic["source"]) and nes(ic["sentence"]),
         "income_claim: kind 'scalar string', source, fixed_value 'absent', fixed_reason %s, a sentence" % REASON)
    need("income" in ic["sentence"] and "null" in ic["sentence"] and "never" in ic["sentence"].lower() and "zero" in ic["sentence"].lower(), "income_claim.sentence must say: present exactly when every income entry is null, and a null is never read as zero")
    r = c.get("income_claim_rule")
    need(isinstance(r, dict) and set(r) == {"present_when", "value", "reason", "absent_means"} and all(nes(v) for v in r.values()), "income_claim_rule must hold exactly present_when, value, reason and absent_means, in words")
    need("every" in r["present_when"] and "income" in r["present_when"] and "absent" in r["value"] and REASON in r["reason"] and "no statement" in r["absent_means"], "income_claim_rule must say: every income entry null; the value absent; the reason code; no statement when absent")
    mb, mn = base["manifest"], c["manifest"]
    need(set(mn) == set(mb) | {"optional"} and mn["required"] == mb["required"], "manifest must gain exactly an `optional` key and keep `required`")
    need(mn["optional"] == ["calendar_source"], "manifest.optional must be [calendar_source]")
    need(set(mn["fields"]) == set(mb["fields"]) | {"calendar_source"} and all(mb["fields"][k] == mn["fields"][k] for k in mb["fields"]), "manifest.fields must keep every field and gain exactly calendar_source")
    cs = mn["fields"]["calendar_source"]
    need(isinstance(cs, dict) and set(cs) == {"values", "sentence"} and cs["values"] == CAL_VALUES and nes(cs["sentence"]) and "calendar" in cs["sentence"] and "fallback" in cs["sentence"], "manifest.fields.calendar_source: values %s and a sentence on the calendar and the fallback" % CAL_VALUES)
    return True


def series_problems(c, series):
    """A reference validator driven ONLY by the contract's declarations (the income / claim rule)."""
    out = []
    claim_field = next(k for k, v in c["series"]["fields"].items() if isinstance(v, dict) and "fixed_reason" in v)
    fixed = c["series"]["fields"][claim_field]["fixed_value"]
    inc = series.get("income")
    all_null = isinstance(inc, list) and len(inc) > 0 and all(x is None for x in inc)
    some_null = isinstance(inc, list) and any(x is None for x in inc)
    has = claim_field in series
    if has and series[claim_field] != fixed:
        out.append("income_claim must read %r" % fixed)
    if has and not all_null:
        out.append("income_claim is present but not every income entry is null")
    if all_null and not has:
        out.append("every income entry is null and the series carries no income_claim: a null with no claim")
    if some_null and not all_null:
        out.append("an income entry is null on a series that has a number: mixed")
    return out


def manifest_problems(c, manifest):
    out = []
    if "calendar_source" in manifest and manifest["calendar_source"] not in c["manifest"]["fields"]["calendar_source"]["values"]:
        out.append("calendar_source outside its values")
    return out


def check_behaviour(c):
    def s(**kw):
        x = {"income": [0.0, 1.5, 0.0]}
        x.update(kw)
        return x
    good = [("numeric income, no claim", s()), ("all-null income with the claim", s(income=[None, None, None], income_claim="absent")), ("a single null-day series with the claim", s(income=[None], income_claim="absent")),
            ("zero income without a claim", s(income=[0.0, 0.0]))]
    bad = [("all-null income, no claim", s(income=[None, None])), ("the claim beside numeric income", s(income_claim="absent")), ("the claim beside mixed income", s(income=[None, 1.0], income_claim="absent")),
           ("mixed income without the claim", s(income=[None, 1.0])), ("a claim of other words", s(income=[None], income_claim="present")), ("a null claim", s(income=[None], income_claim=None))]
    for label, row in good:
        need(not series_problems(c, row), "%s must validate: %s" % (label, series_problems(c, row)))
    for label, row in bad:
        need(series_problems(c, row), "%s must be rejected" % label)
    mg = [("no calendar_source", {}), ("pandas_market_calendars", {"calendar_source": "pandas_market_calendars"}), ("fallback_2010_2027", {"calendar_source": "fallback_2010_2027"})]
    mbad = [("another source", {"calendar_source": "NYSE/hardcoded"}), ("a null source", {"calendar_source": None})]
    for label, m in mg:
        need(not manifest_problems(c, m), "manifest %s must validate" % label)
    for label, m in mbad:
        need(manifest_problems(c, m), "manifest %s must be rejected" % label)
    return len(good) + len(mg), len(bad) + len(mbad)


def check_grant(changed):
    bad = [f for f in changed if f not in GRANT_FILES and not f.startswith(GRANT_PREFIXES)]
    need(not bad, "the worker's commits touch files outside its grant: %s" % bad[:3])
    need(CONTRACT_REL in changed and TEST_REL in changed, "the contract and its new test must both change")
    return True


def check_facts(rec, c, base_sha):
    exp = {"contract_version", "lineage_sha256", "optional", "basis_const", "income_claim", "manifest_optional", "tests", "words"}
    need(isinstance(rec, dict) and set(rec) == exp, "record keys differ: %s" % (sorted(set(rec) ^ exp) if isinstance(rec, dict) else "?"))
    need(rec["contract_version"] == "0.3.1" and rec["lineage_sha256"] == base_sha and rec["optional"] == c["series"]["optional"] and rec["basis_const"] is True, "version, lineage sha256, optional list or the const claim differ")
    need(rec["income_claim"] == {"value": "absent", "reason": REASON} and rec["manifest_optional"] == ["calendar_source"], "income_claim or manifest_optional differ")
    need(isinstance(rec["tests"], int) and not isinstance(rec["tests"], bool) and rec["tests"] >= 10, "tests must be a whole number, at least 10")
    need(nes(rec["words"]) and 80 <= len(rec["words"]) <= 1800 and not LONG_DIGITS.findall(rec["words"]), "words must be one paragraph of 80 to 1800 characters with no long digit run")
    return True


def run_pytest(root, target):
    r = subprocess.run([sys.executable, "-m", "pytest", "-q", "-p", "no:cacheprovider", target] if isinstance(target, str) else [sys.executable, "-m", "pytest", "-q", "-p", "no:cacheprovider"] + list(target),
                       cwd=str(root), capture_output=True, text=True, timeout=900)
    m = re.search(r"(\d+) passed", r.stdout)
    need(r.returncode == 0 and m is not None, "tests failed: %s" % r.stdout[-300:].replace("\n", " | "))
    return int(m.group(1))


def run(root, cid):
    root = Path(root)
    c = json.loads((root / CONTRACT_REL).read_bytes().decode("utf-8"))
    base = base_commit(root)
    raw = subprocess.run(["git", "-C", str(root), "show", "%s:%s" % (base, CONTRACT_REL)], capture_output=True).stdout
    b = json.loads(raw.decode("utf-8"))
    bsha = hashlib.sha256(raw).hexdigest()
    if cid == "DB153-1-AC1":
        check_diff(b, c, bsha)
        print("OK: series contract 0.3.1: only the lineage entry, series.optional (+income_claim), the basis field's const and rule-24 note, the income_claim field, the top-level income_claim_rule and manifest.optional (+calendar_source) differ from the base; every other key is byte-identical")
        return True
    if cid == "DB153-1-AC2":
        check_diff(b, c, bsha)
        g, x = check_behaviour(c)
        print("OK: behaviour: a reference validator driven only by the contract accepts %d documents and rejects %d (a null with no claim, the claim beside a number, mixed income, other words, a calendar source outside its values)" % (g, x))
        return True
    if cid == "DB153-1-AC3":
        need((root / TEST_REL).is_file(), "no %s" % TEST_REL)
        n_new = run_pytest(root, TEST_REL)
        need(n_new >= 10, "the new test file holds %d passing tests, at least 10 are owed" % n_new)
        n_030 = run_pytest(root, TEST030)
        n_pub = run_pytest(root, PUBLISHER_TESTS)
        edited = 0
        for ln in git(root, "diff", "--numstat", base, "HEAD", "--", TEST030).split("\n"):
            p = ln.split("\t")
            if len(p) == 3 and p[0].isdigit() and p[1].isdigit():
                edited += int(p[0]) + int(p[1])
        need(edited <= MAX_TEST030_LINES, "the 0.3.0 test file may change by at most %d lines" % MAX_TEST030_LINES)
        changed = set()
        for cm in own_commits(root):
            changed |= set(git(root, "show", "--name-only", "--format=", cm).split())
        check_grant(changed)
        rec = json.loads((root / REC_REL).read_bytes().decode("utf-8"))
        check_facts(rec, c, bsha)
        need(rec["tests"] == n_new, "the record's test count differs from the recount %d" % n_new)
        print("OK: %d new tests, the 0.3.0 file's %d and the publisher's %d tests pass (the portal mirror is the reader cell's and is not run here); %d files changed, all in the grant; the facts record equals the contract" % (n_new, n_030, n_pub, len(changed)))
        return True
    raise Fail("unknown criterion %s" % cid)


def selftest():
    def red(fn, label):
        try:
            fn()
        except Fail:
            return
        raise AssertionError("red arm passed: " + label)
    base = {"contract_version": "0.3.0", "lineage": [{"contract_version": "0.1.0"}], "project": "p", "writer": "w",
            "series": {"required": ["date"], "optional": ["class_value", BASIS], "array_keys": ["date"], "shape": "x",
                       "fields": {"date": {"kind": "a"}, "income": {"kind": "b"}, BASIS: {"kind": "scalar string", "source": "s", "fixed_value": "f", "sentence": "z"}}},
            "manifest": {"required": ["firm"], "fields": {"firm": {"sentence": "f"}}}}
    good = copy.deepcopy(base)
    good["contract_version"] = "0.3.1"
    good["lineage"].append({"contract_version": "0.3.0", "sha256": "a" * 64, "note": "the 0.3.0 bytes"})
    good["series"]["optional"].append("income_claim")
    good["series"]["fields"][BASIS].update({"const": True, "rule24_note": "one value, one intent: how the list was derived; no other state exists."})
    good["series"]["fields"]["income_claim"] = {"kind": "scalar string", "source": "income_claim of the source table", "fixed_value": "absent", "fixed_reason": REASON,
                                                "sentence": "Present exactly when every income entry is null; the source reports no income, and a null is never read as zero."}
    good["income_claim_rule"] = {"present_when": "every income entry is null", "value": "absent", "reason": "the fixed code %s" % REASON, "absent_means": "no statement about income is made"}
    good["manifest"]["optional"] = ["calendar_source"]
    good["manifest"]["fields"]["calendar_source"] = {"values": list(CAL_VALUES), "sentence": "The calendar that answered; fallback means the hardcoded table."}
    assert check_diff(base, good, "a" * 64)
    arms = (("version", lambda x: x.update(contract_version="0.3.0")), ("lineage sha", lambda x: x["lineage"][-1].update(sha256="b" * 64)), ("lineage lost", lambda x: x["lineage"].pop(0)),
            ("other section", lambda x: x.update(writer="z")), ("optional", lambda x: x["series"].update(optional=["class_value", BASIS])), ("optional order", lambda x: x["series"].update(optional=["class_value", "income_claim", BASIS])),
            ("required", lambda x: x["series"].update(required=["date", "z"])), ("earlier field", lambda x: x["series"]["fields"]["income"].update(kind="c")), ("basis fixed value", lambda x: x["series"]["fields"][BASIS].update(fixed_value="g")),
            ("basis const", lambda x: x["series"]["fields"][BASIS].update(const=False)), ("basis note two lines", lambda x: x["series"]["fields"][BASIS].update(rule24_note="one value\nno other state")),
            ("basis note words", lambda x: x["series"]["fields"][BASIS].update(rule24_note="a note")), ("claim value", lambda x: x["series"]["fields"]["income_claim"].update(fixed_value="present")),
            ("claim reason", lambda x: x["series"]["fields"]["income_claim"].update(fixed_reason="OTHER")), ("claim sentence", lambda x: x["series"]["fields"]["income_claim"].update(sentence="short")),
            ("claim extra key", lambda x: x["series"]["fields"]["income_claim"].update(z=1)), ("rule keys", lambda x: x["income_claim_rule"].pop("reason")), ("rule words", lambda x: x["income_claim_rule"].update(present_when="sometimes")),
            ("manifest optional", lambda x: x["manifest"].update(optional=[])), ("manifest required", lambda x: x["manifest"].update(required=["firm", "z"])), ("calendar values", lambda x: x["manifest"]["fields"]["calendar_source"].update(values=["a"])),
            ("calendar sentence", lambda x: x["manifest"]["fields"]["calendar_source"].update(sentence="x")), ("manifest earlier field", lambda x: x["manifest"]["fields"]["firm"].update(sentence="g")))
    for label, fn in arms:
        x = copy.deepcopy(good)
        fn(x)
        red(lambda: check_diff(base, x, "a" * 64), label)
    assert check_behaviour(good) == (7, 8)
    weak = copy.deepcopy(good)
    weak["series"]["fields"]["income_claim"]["fixed_value"] = "other"
    red(lambda: check_behaviour(weak), "a changed fixed value")
    assert check_grant({CONTRACT_REL, TEST_REL, TEST030, D + AUTHOR + "/x.json"})
    red(lambda: check_grant({CONTRACT_REL, TEST_REL, "lib/x.py"}), "outside grant")
    red(lambda: check_grant({CONTRACT_REL}), "no test")
    rec = {"contract_version": "0.3.1", "lineage_sha256": "a" * 64, "optional": good["series"]["optional"], "basis_const": True, "income_claim": {"value": "absent", "reason": REASON}, "manifest_optional": ["calendar_source"], "tests": 10, "words": "w" * 100}
    assert check_facts(rec, good, "a" * 64)
    farms = (("version", lambda r: r.update(contract_version="0.3.0")), ("base", lambda r: r.update(lineage_sha256="b" * 64)), ("optional", lambda r: r.update(optional=[])), ("const", lambda r: r.update(basis_const=False)),
             ("claim", lambda r: r["income_claim"].update(reason="x")), ("manifest", lambda r: r.update(manifest_optional=[])), ("tests", lambda r: r.update(tests=3)), ("extra", lambda r: r.update(z=1)),
             ("words", lambda r: r.update(words="short")), ("digits", lambda r: r.update(words="w" * 100 + " 123456789")))
    for label, fn in farms:
        r2 = copy.deepcopy(rec)
        fn(r2)
        red(lambda: check_facts(r2, good, "a" * 64), label)
    print("selftest: diff (%d red arms), behaviour (2), grant (2) and facts (%d red arms) clauses behave" % (len(arms), len(farms)))
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
