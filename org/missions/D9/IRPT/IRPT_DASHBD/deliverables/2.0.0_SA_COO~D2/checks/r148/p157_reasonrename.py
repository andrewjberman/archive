"""IRPT_DASHBD round 149, workstream CONTRACT (issuer 2.0.0_SA_COO~D2, the contracts' sole writer) -- DB-b-289, the RENAME of the income claim's reason (CTO round 147P/148 analysis, msg 9158 item 2, ruling B):
`SOURCE_REPORTS_NO_INCOME` is FALSE (the Cottonwood transaction silver carries non-zero Income on 343,256 of 1,096,830 rows: the SOURCE reports income; it is the Black Diamond-computed RETURN METHOD that does not
separate it), so the reason becomes `RETURN_METHOD_DOES_NOT_SEPARATE_INCOME` "before any series carries it". Two contract edits in ONE order, landed in ONE drain with the writer (DB-b-287): the SOURCE table contract
0.4.4 -> 0.4.5 (the conditional column's reason, meaning and rule) and the SERIES contract 0.3.1 -> 0.3.2 (the income_claim field's fixed_reason, source and sentence, and the claim rule's reason). Nothing else moves; both
schema hashes stay unchanged. LOCAL: two JSON standards, a test file and a few pinned lines in the earlier contract tests.

  DB-b-289 (~233)   org/standards/IRPT_DASHBD_ACCOUNT_RETURN_DAILY_CONTRACT.json (0.4.5) + org/standards/IRPT_DASHBD_SERIES_CONTRACT.json (0.3.2) + tests + a facts record
                    DB157-1-AC1 (each contract differs from its base ONLY in the allowed places),
                    DB157-1-AC2 (the LIVE parts of both say the true thing: the new code, no old code, the words),
                    DB157-1-AC3 (the new tests, the earlier contract tests, the grant, the facts record)

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
SRC_REL = "org/standards/IRPT_DASHBD_ACCOUNT_RETURN_DAILY_CONTRACT.json"
SER_REL = "org/standards/IRPT_DASHBD_SERIES_CONTRACT.json"
TEST_DIR = "data/assets/scripts/gold/irpt_reporting/tests/"
NEW_TEST = TEST_DIR + "test_income_reason_rename.py"
AUTHOR = "0.9.0_WK_IRPT_DASHBD~233"
REC_REL = D + AUTHOR + "/RD_INCOME_REASON_RENAME_FACTS_R149.json"
ORDER_REL = "org/missions/D9/IRPT/IRPT_DASHBD/task-orders/IRPT_DASHBD.TO-DB-b-289.income-reason-rename-both-contracts.md"
EARLIER = [TEST_DIR + "test_account_return_contract_04%d.py" % i for i in range(5)] + [TEST_DIR + "test_series_contract_030.py", TEST_DIR + "test_series_contract_031.py"]
GRANT_FILES = {SRC_REL, SER_REL, NEW_TEST} | set(EARLIER)
GRANT_PREFIXES = (D + AUTHOR + "/", "org/missions/D9/IRPT/IRPT_DASHBD/surprise-channel/investigations/", "org/missions/D9/IRPT/IRPT_DASHBD/task-orders/")
OLD, NEW = "SOURCE_REPORTS_NO_INCOME", "RETURN_METHOD_DOES_NOT_SEPARATE_INCOME"
BD = "computed from Black Diamond values and flows"
MAX_EARLIER_LINES = 28
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


def dumps(x):
    return json.dumps(x, sort_keys=True)


# ------------------------------------------------------------------------------------------------ the pure clauses
def check_source(base, c):
    need(base["contract_version"] == "0.4.4" and c.get("contract_version") == "0.4.5", "source contract: 0.4.4 -> 0.4.5")
    moved = sorted(k for k in set(base) | set(c) if k not in ("contract_version", "supersedes", "rule24_record", "conditional_columns") and base.get(k) != c.get(k))
    need(not moved, "source contract: sections changed beyond the allowed ones (both schema hashes and optional_columns stay byte-identical): %s" % moved)
    bc, nc = base["conditional_columns"], c["conditional_columns"]
    need(len(bc) == 1 and len(nc) == 1 and set(bc[0]) == set(nc[0]), "conditional_columns keeps its one entry and its keys")
    b, n = bc[0], nc[0]
    for k in b:
        if k not in ("reason", "meaning", "rule"):
            need(b[k] == n[k], "conditional_columns[0].%s changed" % k)
    need(n["reason"] == NEW, "the reason must be exactly %s" % NEW)
    for k in ("meaning", "rule"):
        need(nes(n[k]) and OLD not in n[k], "conditional_columns[0].%s must not carry the old code" % k)
    need("return method" in n["meaning"].lower() and "separate" in n["meaning"].lower() and "source" in n["meaning"].lower(), "the meaning must say the return METHOD does not separate income while the source does carry it")
    need(all(w in n["rule"] for w in ("income_received", BD, "optional_columns")) and "never" in n["rule"].lower() and "zero" in n["rule"].lower() and "reject" in n["rule"].lower(), "the rule keeps its clauses")
    sb, sn = base["supersedes"], c["supersedes"]
    need(isinstance(sn, list) and len(sn) == len(sb) + 1 and sn[:len(sb)] == sb, "supersedes must keep every earlier entry byte-identical and append one")
    e = sn[-1]
    need(e.get("contract_version") == "0.4.4" and e.get("schema_hash") == base["schema_hash"] and e.get("schema_hash_with_optional") == base["schema_hash_with_optional"] and nes(e.get("changes")) and NEW in e["changes"], "the appended entry: 0.4.4, both hashes, a changes sentence naming the new code")
    r24b, r24n = base["rule24_record"], c["rule24_record"]
    need({k: x for k, x in r24n.items() if k != "v045"} == r24b and nes(r24n.get("v045")) and NEW in r24n["v045"] and OLD in r24n["v045"] and "343,256" in r24n["v045"] and "one value" in r24n["v045"].lower(),
         "rule24_record keeps every key and adds v045: the rename, why (the 343,256 rows), one value")
    return True


def check_series(base, c, base_sha):
    need(base["contract_version"] == "0.3.1" and c.get("contract_version") == "0.3.2", "series contract: 0.3.1 -> 0.3.2")
    moved = sorted(k for k in set(base) | set(c) if k not in ("contract_version", "lineage", "series", "income_claim_rule") and base.get(k) != c.get(k))
    need(not moved, "series contract: sections changed beyond the allowed ones: %s" % moved)
    lb, ln = base["lineage"], c["lineage"]
    need(isinstance(ln, list) and len(ln) == len(lb) + 1 and ln[:len(lb)] == lb and ln[-1].get("contract_version") == "0.3.1" and ln[-1].get("sha256") == base_sha and nes(ln[-1].get("note")) and len(ln[-1]) == 3,
         "lineage keeps every entry and appends {0.3.1, sha256 of the 0.3.1 bytes, a note}")
    sb, sn = base["series"], c["series"]
    for k in sb:
        if k != "fields":
            need(sb[k] == sn[k], "series.%s changed" % k)
    fb, fn = sb["fields"], sn["fields"]
    need(set(fb) == set(fn) and all(fb[k] == fn[k] for k in fb if k != "income_claim"), "series.fields: only income_claim may change")
    b, n = fb["income_claim"], fn["income_claim"]
    need(set(b) == set(n) and all(b[k] == n[k] for k in b if k not in ("fixed_reason", "source", "sentence")), "income_claim keeps its keys and its kind and fixed_value")
    need(n["fixed_reason"] == NEW, "income_claim.fixed_reason must be exactly %s" % NEW)
    for k in ("source", "sentence"):
        need(nes(n[k]) and OLD not in n[k] and "reports no income" not in n[k], "income_claim.%s must not carry the old code or say the source reports no income" % k)
    need("return method" in n["sentence"].lower() and "separate" in n["sentence"].lower() and "income" in n["sentence"] and "null" in n["sentence"] and "never" in n["sentence"].lower() and "zero" in n["sentence"].lower(),
         "income_claim.sentence must say: every income entry is null, the return method does not separate income, a null is never read as zero")
    rb, rn = base["income_claim_rule"], c["income_claim_rule"]
    need(set(rb) == set(rn) and rb["value"] == rn["value"] and rb["absent_means"] == rn["absent_means"], "income_claim_rule: only `present_when` and `reason` may change")
    need(NEW in rn["reason"] and OLD not in rn["reason"], "income_claim_rule.reason must name the new code and not the old")
    pw = rn["present_when"]
    need(nes(pw) and "every" in pw and "income" in pw and "null" in pw and "reports no income" not in pw and OLD not in pw, "income_claim_rule.present_when must keep `every income entry ... null` and must not say the source reports no income")
    return True


def live_text(c, kind):
    if kind == "src":
        return dumps(c["conditional_columns"])
    return dumps(c["series"]["fields"]["income_claim"]) + dumps(c["income_claim_rule"])


def check_live(src, ser):
    for kind, c in (("src", src), ("ser", ser)):
        t = live_text(c, kind)
        need(NEW in t, "%s: the live parts must name %s" % (kind, NEW))
        need(OLD not in t, "%s: the live parts still carry the old code %s" % (kind, OLD))
        need("reports no income" not in t and "states no income" not in t, "%s: the live parts still say the source reports (or states) no income" % kind)
    return True


def check_grant(changed):
    bad = [f for f in changed if f not in GRANT_FILES and not f.startswith(GRANT_PREFIXES)]
    need(not bad, "the worker's commits touch files outside its grant: %s" % bad[:3])
    need(SRC_REL in changed and SER_REL in changed and NEW_TEST in changed, "both contracts and the new test must change")
    return True


def check_facts(rec, src_sha, ser_sha, n_tests):
    exp = {"source_version", "series_version", "reason", "old_code_in_live_parts", "base_sha256", "tests", "words"}
    need(isinstance(rec, dict) and set(rec) == exp, "record keys differ: %s" % (sorted(set(rec) ^ exp) if isinstance(rec, dict) else "?"))
    need(rec["source_version"] == "0.4.5" and rec["series_version"] == "0.3.2" and rec["reason"] == NEW and rec["old_code_in_live_parts"] == 0, "versions, reason or the old-code count differ")
    need(rec["base_sha256"] == {"source": src_sha, "series": ser_sha}, "base_sha256 must be the sha256 of the two base files {source, series}")
    need(isinstance(rec["tests"], int) and not isinstance(rec["tests"], bool) and rec["tests"] == n_tests and n_tests >= 6, "tests must equal the recount, at least 6")
    need(nes(rec["words"]) and 80 <= len(rec["words"]) <= 1800 and not LONG_DIGITS.findall(rec["words"]), "words must be one paragraph of 80 to 1800 characters with no long digit run")
    return True


def run_pytest(root, files):
    r = subprocess.run([sys.executable, "-m", "pytest", "-q", "-p", "no:cacheprovider"] + list(files), cwd=str(root), capture_output=True, text=True, timeout=900)
    m = re.search(r"(\d+) passed", r.stdout)
    need(r.returncode == 0 and m is not None, "tests failed: %s" % r.stdout[-300:].replace("\n", " | "))
    return int(m.group(1))


def load(root, rel):
    raw = (Path(root) / rel).read_bytes()
    return json.loads(raw.decode("utf-8")), raw


def run(root, cid):
    root = Path(root)
    base = base_commit(root)
    sb_raw, rb_raw = git(root, "show", "%s:%s" % (base, SRC_REL)), git(root, "show", "%s:%s" % (base, SER_REL))
    sb, rb = json.loads(sb_raw.decode("utf-8")), json.loads(rb_raw.decode("utf-8"))
    src, _ = load(root, SRC_REL)
    ser, _ = load(root, SER_REL)
    if cid == "DB157-1-AC1":
        check_source(sb, src)
        check_series(rb, ser, hashlib.sha256(rb_raw).hexdigest())
        print("OK: source contract 0.4.5 and series contract 0.3.2 differ from their bases only in the allowed places (version, one appended history entry, the renamed reason and its words, one rule-24 key); both schema hashes, optional_columns and every other key are byte-identical")
        return True
    if cid == "DB157-1-AC2":
        check_source(sb, src)
        check_series(rb, ser, hashlib.sha256(rb_raw).hexdigest())
        check_live(src, ser)
        print("OK: the live parts of both contracts name %s, carry no %s and do not say the source reports no income; the words say the return method does not separate income" % (NEW, OLD))
        return True
    if cid == "DB157-1-AC3":
        need((root / NEW_TEST).is_file(), "no %s" % NEW_TEST)
        n_new = run_pytest(root, [NEW_TEST])
        need(n_new >= 6, "the new test file holds %d passing tests, at least 6 are owed" % n_new)
        n_old = run_pytest(root, EARLIER)
        edited = 0
        for f in EARLIER:
            for ln in git(root, "diff", "--numstat", base, "HEAD", "--", f).decode().split("\n"):
                p = ln.split("\t")
                if len(p) == 3 and p[0].isdigit() and p[1].isdigit():
                    edited += int(p[0]) + int(p[1])
        need(edited <= MAX_EARLIER_LINES, "the earlier contract tests may change by at most %d lines in all, read %d" % (MAX_EARLIER_LINES, edited))
        changed = set()
        for cm in own_commits(root):
            changed |= set(git(root, "show", "--name-only", "--format=", cm).decode().split())
        check_grant(changed)
        rec = json.loads((root / REC_REL).read_bytes().decode("utf-8"))
        check_facts(rec, hashlib.sha256(sb_raw).hexdigest(), hashlib.sha256(rb_raw).hexdigest(), n_new)
        print("OK: %d new tests and the earlier contract tests' %d pass (%d changed lines, at most %d); %d files changed, all in the grant; the facts record equals the recount" % (n_new, n_old, edited, MAX_EARLIER_LINES, len(changed)))
        return True
    raise Fail("unknown criterion %s" % cid)


def selftest():
    def red(fn, label):
        try:
            fn()
        except Fail:
            return
        raise AssertionError("red arm passed: " + label)
    sbase = {"contract_version": "0.4.4", "schema_hash": "h1", "schema_hash_with_optional": "h2", "supersedes": [{"contract_version": "0.4.3"}], "rule24_record": {"v044": "x"}, "enums": {"a": [1]}, "optional_columns": [],
             "conditional_columns": [{"name": "income_claim", "type": "string", "values": ["absent"], "reason": OLD, "emitted_when": {"source": BD}, "meaning": "the source reports no income", "rule": "old rule"}]}
    sgood = copy.deepcopy(sbase)
    sgood["contract_version"] = "0.4.5"
    cc = sgood["conditional_columns"][0]
    cc["reason"] = NEW
    cc["meaning"] = "the account-day carries no income: the source carries income but the return method (%s) does not separate it" % BD
    cc["rule"] = "Required exactly when income_received is null and the source is '%s'; a row carrying the claim with an income is invalid; a consumer that needs income rejects it and never reads the null as zero; it sits outside optional_columns." % BD
    sgood["supersedes"].append({"contract_version": "0.4.4", "schema_hash": "h1", "schema_hash_with_optional": "h2", "changes": "the reason became %s" % NEW})
    sgood["rule24_record"]["v045"] = "The reason %s (old %s) is renamed: the transaction silver carries income on 343,256 rows; one value, no other state." % (NEW, OLD)
    assert check_source(sbase, sgood)
    sarms = (("version", lambda x: x.update(contract_version="0.4.4")), ("hash", lambda x: x.update(schema_hash="z")), ("section", lambda x: x.update(enums={"a": [2]})),
             ("reason", lambda x: x["conditional_columns"][0].update(reason="OTHER")), ("old in meaning", lambda x: x["conditional_columns"][0].update(meaning="old " + OLD + " return method separate source")),
             ("meaning words", lambda x: x["conditional_columns"][0].update(meaning="no income")), ("rule words", lambda x: x["conditional_columns"][0].update(rule="short")),
             ("other key", lambda x: x["conditional_columns"][0].update(values=["absent", "x"])), ("supersedes", lambda x: x["supersedes"].pop(0)), ("entry", lambda x: x["supersedes"][-1].update(changes="nothing")),
             ("rule24", lambda x: x["rule24_record"].pop("v045")), ("rule24 words", lambda x: x["rule24_record"].update(v045="changed")), ("rule24 earlier", lambda x: x["rule24_record"].update(v044="y")))
    for label, fn in sarms:
        x = copy.deepcopy(sgood)
        fn(x)
        red(lambda: check_source(sbase, x), label)
    rbase = {"contract_version": "0.3.1", "lineage": [{"contract_version": "0.1.0"}], "writer": "w",
             "series": {"required": ["date"], "fields": {"income": {"kind": "n"}, "income_claim": {"kind": "scalar string", "source": "the source reports no income", "fixed_value": "absent", "fixed_reason": OLD, "sentence": "old"}}},
             "income_claim_rule": {"present_when": "every income entry is null (the source reports no income for it)", "value": "absent", "reason": "the fixed code " + OLD, "absent_means": "no statement"}}
    rgood = copy.deepcopy(rbase)
    rgood["contract_version"] = "0.3.2"
    rgood["lineage"].append({"contract_version": "0.3.1", "sha256": "a" * 64, "note": "the 0.3.1 bytes"})
    ic = rgood["series"]["fields"]["income_claim"]
    ic["fixed_reason"] = NEW
    ic["source"] = "the source table contract's income_claim column, carried unchanged"
    ic["sentence"] = "Present exactly when every income entry is null: the return method does not separate income (the source carries it); a null is never read as zero."
    rgood["income_claim_rule"]["reason"] = "the fixed code " + NEW
    rgood["income_claim_rule"]["present_when"] = "every income entry of the series is null (the return method does not separate income)"
    assert check_series(rbase, rgood, "a" * 64)
    rarms = (("version", lambda x: x.update(contract_version="0.3.1")), ("lineage sha", lambda x: x["lineage"][-1].update(sha256="b" * 64)), ("other section", lambda x: x.update(writer="z")),
             ("other field", lambda x: x["series"]["fields"]["income"].update(kind="z")), ("reason", lambda x: x["series"]["fields"]["income_claim"].update(fixed_reason="OTHER")),
             ("value", lambda x: x["series"]["fields"]["income_claim"].update(fixed_value="present")), ("old source words", lambda x: x["series"]["fields"]["income_claim"].update(source="the source reports no income")),
             ("sentence words", lambda x: x["series"]["fields"]["income_claim"].update(sentence="short")), ("rule reason", lambda x: x["income_claim_rule"].update(reason="the fixed code " + OLD)),
             ("rule value", lambda x: x["income_claim_rule"].update(value="present")), ("present_when words", lambda x: x["income_claim_rule"].update(present_when="sometimes")),
             ("present_when old", lambda x: x["income_claim_rule"].update(present_when="every income entry is null (the source reports no income for it)")))
    for label, fn in rarms:
        x = copy.deepcopy(rgood)
        fn(x)
        red(lambda: check_series(rbase, x, "a" * 64), label)
    assert check_live(sgood, rgood)
    leak = copy.deepcopy(rgood)
    leak["series"]["fields"]["income_claim"]["sentence"] += " " + OLD
    red(lambda: check_live(sgood, leak), "old code live")
    assert check_grant({SRC_REL, SER_REL, NEW_TEST, EARLIER[0], D + AUTHOR + "/x.json"})
    red(lambda: check_grant({SRC_REL, SER_REL, NEW_TEST, "lib/x.py"}), "outside grant")
    red(lambda: check_grant({SRC_REL, NEW_TEST}), "one contract")
    rec = {"source_version": "0.4.5", "series_version": "0.3.2", "reason": NEW, "old_code_in_live_parts": 0, "base_sha256": {"source": "a" * 64, "series": "b" * 64}, "tests": 6, "words": "w" * 100}
    assert check_facts(rec, "a" * 64, "b" * 64, 6)
    farms = (("source", lambda r: r.update(source_version="0.4.4")), ("series", lambda r: r.update(series_version="0.3.1")), ("reason", lambda r: r.update(reason="x")), ("old", lambda r: r.update(old_code_in_live_parts=1)),
             ("base", lambda r: r["base_sha256"].update(source="c" * 64)), ("tests", lambda r: r.update(tests=7)), ("extra", lambda r: r.update(z=1)), ("words", lambda r: r.update(words="short")),
             ("digits", lambda r: r.update(words="w" * 100 + " 123456789")))
    for label, fn in farms:
        r2 = copy.deepcopy(rec)
        fn(r2)
        red(lambda: check_facts(r2, "a" * 64, "b" * 64, 6), label)
    print("selftest: source (%d red arms), series (%d), live (1), grant (2) and facts (%d) clauses behave" % (len(sarms), len(rarms), len(farms)))
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
