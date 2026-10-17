"""IRPT_DASHBD round 150, workstream CONTRACT (issuer 2.0.0_SA_COO~D2, the contract's sole writer) -- DB-b-335, the SERIES contract 0.4.0: the `class_object` section, the class series object that sits beside
series.json.gz (object `class_series.json.gz`; named to ~F2 and ~S2 in msg 8846; asked for by ~S2 in msg 10638). One new top-level section, one new `files` entry, a lineage entry for the 0.3.3 bytes and the version bump;
`series`, `manifest` and every other section stay byte-identical. The sum test makes the classes sum to the account (PRD C-CLASSES: `class_return_daily` is the class's contribution to the account's daily return).
LOCAL: a JSON standard, one new test file and at most 24 changed lines in four existing test files that pin the 0.3.3 version and the lineage length.

  DB-b-335 (~261)   org/standards/IRPT_DASHBD_SERIES_CONTRACT.json (0.4.0) + data/assets/scripts/gold/irpt_reporting/tests/test_series_contract_040.py + the four pinned test files
                    DB202-1-AC1 (the contract differs from the base ONLY in the allowed places; the class_object section has the declared structure),
                    DB202-1-AC2 (BEHAVIOUR: a reference validator driven only by the class_object declarations accepts four documents and rejects eleven),
                    DB202-1-AC3 (the new tests, the existing contract tests and the publisher's tests, the grant)

Usage: python <this file> <repo_root> <criterion_id>      prints "<id> PASS" or "<id> FAIL" last
       python <this file> --selftest                       the pure clauses on synthetic arms
"""
import copy
import difflib
import hashlib
import json
import re
import subprocess
import sys
from pathlib import Path

D = "org/missions/D9/IRPT/IRPT_DASHBD/deliverables/"
CONTRACT_REL = "org/standards/IRPT_DASHBD_SERIES_CONTRACT.json"
TEST_DIR = "data/assets/scripts/gold/irpt_reporting/tests/"
TEST_REL = TEST_DIR + "test_series_contract_040.py"
PINNED_TESTS = [TEST_DIR + n for n in ("test_series_contract_030.py", "test_series_contract_031.py", "test_history_scope_claim_contracts.py", "test_income_reason_rename.py")]
PUBLISHER_TESTS = "infra/aws/lambda/investor-reporting/reporting-publish/tests"
AUTHOR = "0.9.0_WK_IRPT_DASHBD~261"
ORDER_REL = "org/missions/D9/IRPT/IRPT_DASHBD/task-orders/IRPT_DASHBD.TO-DB-b-335.series-contract-040-class-object.md"
GRANT_FILES = {CONTRACT_REL, TEST_REL, *PINNED_TESTS}
GRANT_PREFIXES = (D + AUTHOR + "/", "org/missions/D9/IRPT/IRPT_DASHBD/surprise-channel/investigations/", "org/missions/D9/IRPT/IRPT_DASHBD/task-orders/")
MAX_PINNED_LINES = 24
MAX_REMOVED_CONTRACT_LINES = 4
CLASSES = ["fixed_income", "equity", "commodities", "structured", "alternatives", "cash", "unclassified", "other"]
COVERAGE = ["CLASSIFIED", "UNCLASSIFIED_PRESENT", "SOURCE_ABSENT"]
REQUIRED = ["account_id", "firm", "as_of", "method_version", "schema_version", "date", "class_names", "coverage", "market_value_eod", "class_return_daily"]
CO_KEYS = {"version", "file", "shape", "required", "per_day_arrays", "per_class_arrays", "class_names_enum", "coverage_values", "fields", "dated_classification_rule", "sum_test", "absent_means"}
ALLOWED_TOP = ("contract_version", "lineage", "files", "class_object")


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
def check_class_object(co):
    need(isinstance(co, dict) and set(co) == CO_KEYS, "class_object keys differ: %s" % (sorted(set(co) ^ CO_KEYS) if isinstance(co, dict) else "?"))
    need(co["version"] == "0.4.0" and co["file"] == "class_series" and nes(co["shape"]) and "columnar" in co["shape"], "class_object: version 0.4.0, file class_series, a columnar shape sentence")
    need(co["required"] == REQUIRED, "class_object.required must be %s" % REQUIRED)
    need(co["per_day_arrays"] == ["date", "coverage"] and co["per_class_arrays"] == ["market_value_eod", "class_return_daily"], "per_day_arrays and per_class_arrays differ")
    need(co["class_names_enum"] == CLASSES and co["coverage_values"] == COVERAGE, "class_names_enum or coverage_values differ")
    f = co["fields"]
    need(isinstance(f, dict) and set(f) == set(REQUIRED), "class_object.fields must hold exactly the required keys")
    for k, v in f.items():
        need(isinstance(v, dict) and nes(v.get("kind")) and nes(v.get("sentence")) and set(v) <= {"kind", "sentence", "fixed_value"}, "field %s: kind and sentence (and fixed_value only on schema_version)" % k)
    need(f["schema_version"].get("fixed_value") == "class_object-0.4.0" and all("fixed_value" not in f[k] for k in f if k != "schema_version"), "only schema_version carries fixed_value 'class_object-0.4.0'")
    need("SOURCE_ABSENT" in f["coverage"]["sentence"] and "CLASSIFIED" in f["coverage"]["sentence"] and "UNCLASSIFIED_PRESENT" in f["coverage"]["sentence"], "coverage.sentence must explain the three values")
    need("SOURCE_ABSENT" in f["class_return_daily"]["sentence"] and "sum" in f["class_return_daily"]["sentence"] and "never" in f["class_return_daily"]["sentence"].lower(), "class_return_daily.sentence: contribution, sums to the account, null on SOURCE_ABSENT, never filled")
    r = co["dated_classification_rule"]
    need(nes(r) and all(w in r for w in ("in force", "never by today", "unclassified", "SOURCE_ABSENT")), "dated_classification_rule must say: row in force on the day, never today's, unclassified when none, SOURCE_ABSENT when unreadable")
    st = co["sum_test"]
    need(isinstance(st, dict) and set(st) == {"return_tolerance", "value_tolerance_usd", "applies_to", "return_rule", "value_rule"}, "sum_test keys differ")
    need(st["return_tolerance"] == 1e-9 and st["value_tolerance_usd"] == 0.01, "sum_test tolerances must be 1e-9 and 0.01")
    need(nes(st["applies_to"]) and "SOURCE_ABSENT" in st["applies_to"] and "total_return_daily" in st["return_rule"] and nes(st["value_rule"]) and "value" in st["value_rule"], "sum_test rules must name the series' total_return_daily and value and exclude SOURCE_ABSENT")
    need(nes(co["absent_means"]) and "no class view" in co["absent_means"], "absent_means must say 'no class view'")
    return True


def check_diff(base, c, base_sha, base_text=None, new_text=None):
    need(base["contract_version"] == "0.3.3", "the base is not 0.3.3: %s" % base["contract_version"])
    need(c.get("contract_version") == "0.4.0", "contract_version is not 0.4.0")
    moved = sorted(k for k in set(base) | set(c) if k not in ALLOWED_TOP and base.get(k) != c.get(k))
    need(not moved, "sections changed beyond the allowed ones: %s" % moved)
    need("class_object" in c and "class_object" not in base, "the contract must gain class_object")
    lb, ln = base["lineage"], c["lineage"]
    need(isinstance(ln, list) and len(ln) == len(lb) + 1 and ln[:len(lb)] == lb, "lineage must keep every earlier entry byte-identical and append one")
    last = ln[-1]
    need(last.get("contract_version") == "0.3.3" and last.get("sha256") == base_sha and nes(last.get("note")) and set(last) == {"contract_version", "sha256", "note"}, "the appended lineage entry: version 0.3.3, the sha256 of the 0.3.3 file bytes %s, a note" % base_sha[:12])
    fb, fn = base["files"], c["files"]
    need(set(fn) == set(fb) | {"class_series"} and all(fb[k] == fn[k] for k in fb), "files must keep every entry and gain exactly class_series")
    need(nes(fn["class_series"]) and "class_series.json.gz" in fn["class_series"] and "class_object" in fn["class_series"], "files.class_series must name class_series.json.gz and the class_object section")
    check_class_object(c["class_object"])
    if base_text is not None and new_text is not None:
        removed = [ln for ln in difflib.unified_diff(base_text.split("\n"), new_text.split("\n"), lineterm="", n=0) if ln.startswith("-") and not ln.startswith("---")]
        need(len(removed) <= MAX_REMOVED_CONTRACT_LINES, "%d existing lines of the file were removed or reformatted (at most %d: the version line and the files line it must touch)" % (len(removed), MAX_REMOVED_CONTRACT_LINES))
    return True


def problems(co, series, obj):
    """A reference validator driven ONLY by the class_object declarations and the series file's arrays."""
    out = []
    missing = set(co["required"]) - set(obj)
    if missing:
        return ["a required key is missing"]
    n = len(obj["date"])
    names = obj["class_names"]
    if len(set(names)) != len(names) or not set(names) <= set(co["class_names_enum"]):
        out.append("class_names repeat or leave the enum")
    for k in co["per_class_arrays"]:
        if set(obj[k]) != set(names) or any(len(v) != n for v in obj[k].values()):
            out.append("%s keys or lengths differ from class_names / date" % k)
    if len(obj["coverage"]) != n or any(x not in co["coverage_values"] for x in obj["coverage"]):
        out.append("coverage length or value")
    if obj["schema_version"] != co["fields"]["schema_version"]["fixed_value"]:
        out.append("schema_version")
    if out:
        return out
    if obj["date"] != sorted(set(obj["date"])):
        out.append("dates not strictly increasing")
    if n and obj["as_of"] != obj["date"][-1]:
        out.append("as_of is not the last date")
    idx = {d: i for i, d in enumerate(series["date"])}
    st = co["sum_test"]
    for i, d in enumerate(obj["date"]):
        if d not in idx:
            out.append("%s is not a series date" % d)
            continue
        rets = [obj["class_return_daily"][k][i] for k in names]
        vals = [obj["market_value_eod"][k][i] for k in names]
        if obj["coverage"][i] == "SOURCE_ABSENT":
            if any(x is not None for x in rets + vals):
                out.append("%s: SOURCE_ABSENT day carries class numbers" % d)
            continue
        tot = series["total_return_daily"][idx[d]]
        if tot is None:
            if any(x is not None for x in rets):
                out.append("%s: class returns on a null total" % d)
        elif any(x is None for x in rets) or abs(sum(rets) - tot) > st["return_tolerance"]:
            out.append("%s: classes do not sum to the account return" % d)
        if any(x is None for x in vals) or abs(sum(vals) - series["value"][idx[d]]) > st["value_tolerance_usd"]:
            out.append("%s: class values do not sum to the account value" % d)
    return out


def sample():
    series = {"date": ["2026-07-01", "2026-07-02", "2026-07-03"], "value": [100.0, 102.0, 103.0], "total_return_daily": [None, 0.02, 0.01]}
    obj = {"account_id": "a", "firm": "f", "as_of": "2026-07-03", "method_version": 1, "schema_version": "class_object-0.4.0", "date": list(series["date"]), "class_names": ["equity", "cash"],
           "coverage": ["CLASSIFIED", "UNCLASSIFIED_PRESENT", "SOURCE_ABSENT"], "market_value_eod": {"equity": [60.0, 62.0, None], "cash": [40.0, 40.0, None]},
           "class_return_daily": {"equity": [None, 0.015, None], "cash": [None, 0.005, None]}}
    return series, obj


def check_behaviour(c):
    co = c["class_object"]
    series, obj = sample()

    def with_(fn, s=None):
        o = copy.deepcopy(obj)
        fn(o)
        return (s or series), o
    good = [("a mixed document", (series, obj)),
            ("all days classified", with_(lambda o: o.update(coverage=["CLASSIFIED"] * 3, market_value_eod={"equity": [60.0, 62.0, 63.0], "cash": [40.0, 40.0, 40.0]}, class_return_daily={"equity": [None, 0.015, 0.006], "cash": [None, 0.005, 0.004]}))),
            ("one class only", with_(lambda o: o.update(class_names=["unclassified"], coverage=["CLASSIFIED", "UNCLASSIFIED_PRESENT", "SOURCE_ABSENT"], market_value_eod={"unclassified": [100.0, 102.0, None]}, class_return_daily={"unclassified": [None, 0.02, None]}))),
            ("an empty account window", with_(lambda o: o.update(date=[], as_of="x", coverage=[], market_value_eod={"equity": [], "cash": []}, class_return_daily={"equity": [], "cash": []})))]
    # the empty window has no last date: as_of is unchecked when n == 0
    bad = [("returns do not sum", with_(lambda o: o["class_return_daily"]["cash"].__setitem__(1, 0.009))), ("values do not sum", with_(lambda o: o["market_value_eod"]["cash"].__setitem__(0, 39.0))),
           ("SOURCE_ABSENT carries a number", with_(lambda o: o["market_value_eod"]["cash"].__setitem__(2, 1.0))), ("a class outside the enum", with_(lambda o: o.update(class_names=["equity", "stocks"]))),
           ("a repeated class", with_(lambda o: o.update(class_names=["equity", "equity"]))), ("a coverage outside its values", with_(lambda o: o["coverage"].__setitem__(0, "FULL"))),
           ("a date the series lacks", with_(lambda o: o["date"].__setitem__(2, "2026-07-06"))), ("class returns on a null total", with_(lambda o: o["class_return_daily"]["equity"].__setitem__(0, 0.0))),
           ("a wrong schema_version", with_(lambda o: o.update(schema_version="class_object-0.3"))), ("a short class array", with_(lambda o: o["market_value_eod"]["equity"].pop())),
           ("a required key missing", with_(lambda o: o.pop("coverage")))]
    for label, (s, o) in good:
        need(not problems(co, s, o), "%s must validate: %s" % (label, problems(co, s, o)))
    for label, (s, o) in bad:
        need(problems(co, s, o), "%s must be rejected" % label)
    return len(good), len(bad)


def check_grant(changed):
    bad = [f for f in changed if f not in GRANT_FILES and not f.startswith(GRANT_PREFIXES)]
    need(not bad, "the worker's commits touch files outside its grant: %s" % bad[:3])
    need(CONTRACT_REL in changed and TEST_REL in changed, "the contract and its new test must both change")
    return True


def run_pytest(root, targets):
    r = subprocess.run([sys.executable, "-m", "pytest", "-q", "-p", "no:cacheprovider", "--color=no"] + list(targets), cwd=str(root), capture_output=True, text=True, timeout=900)
    m = re.search(r"(\d+) passed", r.stdout)
    need(r.returncode == 0 and m is not None, "tests failed: %s" % r.stdout[-300:].replace("\n", " | "))
    return int(m.group(1))


def run(root, cid):
    root = Path(root)
    new_raw = (root / CONTRACT_REL).read_bytes()
    c = json.loads(new_raw.decode("utf-8"))
    if cid in ("DB202-1-AC1", "DB202-1-AC2"):
        need("class_object" in c, "the contract has no class_object section")  # first, so the base fails on the missing section and not on the order's history
    if cid == "DB202-1-AC3":
        need((root / TEST_REL).is_file(), "no %s" % TEST_REL)
    base = base_commit(root)
    raw = subprocess.run(["git", "-C", str(root), "show", "%s:%s" % (base, CONTRACT_REL)], capture_output=True).stdout
    b = json.loads(raw.decode("utf-8"))
    bsha = hashlib.sha256(raw).hexdigest()
    if cid == "DB202-1-AC1":
        check_diff(b, c, bsha, raw.decode("utf-8"), new_raw.decode("utf-8"))
        print("OK: series contract 0.4.0: only the version, the lineage entry for the 0.3.3 bytes, files.class_series and the new class_object section differ from the base; every other key is byte-identical and at most %d existing lines changed" % MAX_REMOVED_CONTRACT_LINES)
        return True
    if cid == "DB202-1-AC2":
        check_diff(b, c, bsha)
        g, x = check_behaviour(c)
        print("OK: behaviour: a reference validator driven only by class_object accepts %d documents and rejects %d (classes that do not sum, values that do not sum, a number on a SOURCE_ABSENT day, a class outside the enum, a repeat, a coverage outside its values, a date the series lacks, class returns on a null total, a wrong schema version, a short array, a missing key)" % (g, x))
        return True
    if cid == "DB202-1-AC3":
        need((root / TEST_REL).is_file(), "no %s" % TEST_REL)
        n_new = run_pytest(root, [TEST_REL])
        need(n_new >= 10, "the new test file holds %d passing tests, at least 10 are owed" % n_new)
        text = (root / TEST_REL).read_bytes().decode("utf-8")
        need(all(w in text for w in ("class_object", "sum_test", "SOURCE_ABSENT")), "the new test file must exercise class_object, sum_test and SOURCE_ABSENT")
        n_old = run_pytest(root, PINNED_TESTS)
        n_pub = run_pytest(root, [PUBLISHER_TESTS])
        edited = 0
        for ln in git(root, "diff", "--numstat", base, "HEAD", "--", *PINNED_TESTS).split("\n"):
            p = ln.split("\t")
            if len(p) == 3 and p[0].isdigit() and p[1].isdigit():
                edited += int(p[0]) + int(p[1])
        need(edited <= MAX_PINNED_LINES, "the four pinned test files may change by at most %d lines (read %d)" % (MAX_PINNED_LINES, edited))
        rf = subprocess.run([sys.executable, "-m", "ruff", "check", "--target-version", "py39", TEST_REL], cwd=str(root), capture_output=True, text=True)
        need(rf.returncode == 0, "ruff: %s" % rf.stdout[-200:].replace("\n", " | "))
        changed = set()
        for cm in own_commits(root):
            changed |= set(git(root, "show", "--name-only", "--format=", cm).split())
        check_grant(changed)
        print("OK: %d new tests, the %d pinned contract tests and the publisher's %d tests pass (%d lines edited in the pinned files); ruff clean; %d files changed, all in the grant" % (n_new, n_old, n_pub, edited, len(changed)))
        return True
    raise Fail("unknown criterion %s" % cid)


def selftest():
    def red(fn, label):
        try:
            fn()
        except Fail:
            return
        raise AssertionError("red arm passed: " + label)
    fields = {k: {"kind": "k", "sentence": "s"} for k in REQUIRED}
    fields["schema_version"]["fixed_value"] = "class_object-0.4.0"
    fields["coverage"]["sentence"] = "CLASSIFIED, UNCLASSIFIED_PRESENT, SOURCE_ABSENT"
    fields["class_return_daily"]["sentence"] = "the contribution; the classes sum to the account; null on SOURCE_ABSENT; never filled"
    co = {"version": "0.4.0", "file": "class_series", "shape": "columnar: x", "required": list(REQUIRED), "per_day_arrays": ["date", "coverage"], "per_class_arrays": ["market_value_eod", "class_return_daily"],
          "class_names_enum": list(CLASSES), "coverage_values": list(COVERAGE), "fields": fields,
          "dated_classification_rule": "the row in force on the day, never by today's row; unclassified when none; SOURCE_ABSENT when unreadable",
          "sum_test": {"return_tolerance": 1e-9, "value_tolerance_usd": 0.01, "applies_to": "every day whose coverage is not SOURCE_ABSENT", "return_rule": "equals the series total_return_daily", "value_rule": "equals the series value"},
          "absent_means": "no class view: the page says so"}
    base = {"contract_version": "0.3.3", "lineage": [{"contract_version": "0.1.0"}], "project": "p", "writer": "w", "files": {"series": "s", "manifest": "m"}, "series": {"x": 1}, "manifest": {"y": 2}}
    good = copy.deepcopy(base)
    good["contract_version"] = "0.4.0"
    good["lineage"].append({"contract_version": "0.3.3", "sha256": "a" * 64, "note": "the 0.3.3 bytes"})
    good["files"]["class_series"] = "class_series.json.gz -- the class_object section"
    good["class_object"] = co
    assert check_diff(base, good, "a" * 64)
    arms = (("version", lambda x: x.update(contract_version="0.3.3")), ("lineage sha", lambda x: x["lineage"][-1].update(sha256="b" * 64)), ("lineage lost", lambda x: x["lineage"].pop(0)), ("lineage extra key", lambda x: x["lineage"][-1].update(z=1)),
            ("other section", lambda x: x.update(writer="z")), ("series touched", lambda x: x["series"].update(x=2)), ("manifest touched", lambda x: x["manifest"].update(y=3)), ("files lost", lambda x: x["files"].pop("series")),
            ("files no class_series", lambda x: x["files"].pop("class_series")), ("files words", lambda x: x["files"].update(class_series="something")), ("no class_object", lambda x: x.pop("class_object")),
            ("co key missing", lambda x: x["class_object"].pop("sum_test")), ("co extra key", lambda x: x["class_object"].update(z=1)), ("co version", lambda x: x["class_object"].update(version="0.3.0")),
            ("co required", lambda x: x["class_object"].update(required=REQUIRED[:-1])), ("co enum", lambda x: x["class_object"].update(class_names_enum=CLASSES[:-1])), ("co coverage", lambda x: x["class_object"].update(coverage_values=COVERAGE[:2])),
            ("co per-class", lambda x: x["class_object"].update(per_class_arrays=["market_value_eod"])), ("field missing", lambda x: x["class_object"]["fields"].pop("firm")), ("field no sentence", lambda x: x["class_object"]["fields"]["firm"].pop("sentence")),
            ("fixed value", lambda x: x["class_object"]["fields"]["schema_version"].update(fixed_value="v")), ("fixed value elsewhere", lambda x: x["class_object"]["fields"]["firm"].update(fixed_value="v")),
            ("coverage sentence", lambda x: x["class_object"]["fields"]["coverage"].update(sentence="short")), ("return sentence", lambda x: x["class_object"]["fields"]["class_return_daily"].update(sentence="the contribution")),
            ("dated rule", lambda x: x["class_object"].update(dated_classification_rule="by today's row")), ("sum keys", lambda x: x["class_object"]["sum_test"].pop("value_rule")), ("return tolerance", lambda x: x["class_object"]["sum_test"].update(return_tolerance=1e-3)),
            ("value tolerance", lambda x: x["class_object"]["sum_test"].update(value_tolerance_usd=1.0)), ("applies_to", lambda x: x["class_object"]["sum_test"].update(applies_to="every day")), ("absent_means", lambda x: x["class_object"].update(absent_means="nothing")))
    for label, fn in arms:
        x = copy.deepcopy(good)
        fn(x)
        red(lambda: check_diff(base, x, "a" * 64), label)
    old = "\n".join(["a", "b", "c", "d"])
    assert check_diff(base, good, "a" * 64, old, "\n".join(["a", "B", "c", "d", "e"]))
    red(lambda: check_diff(base, good, "a" * 64, "a\nb\nc\nd\ne\nf", "w\nx\ny\nz\nq\nr"), "six lines reformatted")
    assert check_behaviour(good) == (4, 11)
    weak = copy.deepcopy(good)
    weak["class_object"]["sum_test"]["return_tolerance"] = 10.0
    red(lambda: check_behaviour(weak), "a loosened tolerance")
    assert check_grant({CONTRACT_REL, TEST_REL, PINNED_TESTS[0], D + AUTHOR + "/x.json"})
    red(lambda: check_grant({CONTRACT_REL, TEST_REL, "lib/x.py"}), "outside grant")
    red(lambda: check_grant({CONTRACT_REL}), "no test")
    print("selftest: diff (%d red arms plus the text clause), behaviour (2) and grant (2) clauses behave" % len(arms))
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
