"""IRPT_DASHBD round 148, workstream CONTRACT (issuer 2.0.0_SA_COO~D2, the contract's sole writer) -- DB-b-284, the SOURCE TABLE contract 0.4.4 (CTO round-147 analysis, msg 9060 item 1): a row whose
income_received is null because the source reports no income carries a CLAIM, `income_claim` = `absent` with the fixed reason SOURCE_REPORTS_NO_INCOME, so the null can be told apart from a failed read
("a value must carry its claim"). One new entry in a NEW section `conditional_columns` (a column only one SOURCE emits); `optional_columns`, the 19 columns and BOTH schema hashes stay byte-identical, so no pinned reader test moves; row S104 is the owner's.
LOCAL: a JSON standard, a test file and at most 14 changed lines across the earlier four contract tests.

  DB-b-284 (~228)   org/standards/IRPT_DASHBD_ACCOUNT_RETURN_DAILY_CONTRACT.json (0.4.4) + data/assets/scripts/gold/irpt_reporting/tests/test_account_return_contract_044.py + a facts record
                    DB152-1-AC1 (the contract differs from the base ONLY in the allowed places; both hashes unchanged),
                    DB152-1-AC2 (BEHAVIOUR: a reference rule driven only by the declarations accepts five rows and rejects six),
                    DB152-1-AC3 (the new tests, the earlier four contract test files, the grant, the facts record with the token census recounted)

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
CONTRACT_REL = "org/standards/IRPT_DASHBD_ACCOUNT_RETURN_DAILY_CONTRACT.json"
TEST_DIR = "data/assets/scripts/gold/irpt_reporting/tests/"
TEST_REL = TEST_DIR + "test_account_return_contract_044.py"
EARLIER = [TEST_DIR + "test_account_return_contract_04%d.py" % i for i in range(4)]
AUTHOR = "0.9.0_WK_IRPT_DASHBD~228"
REC_REL = D + AUTHOR + "/RD_CONTRACT_044_FACTS_R148.json"
ORDER_REL = "org/missions/D9/IRPT/IRPT_DASHBD/task-orders/IRPT_DASHBD.TO-DB-b-284.source-contract-044-income-claim-absent.md"
GRANT_FILES = {CONTRACT_REL, TEST_REL} | set(EARLIER)
GRANT_PREFIXES = (D + AUTHOR + "/", "org/missions/D9/IRPT/IRPT_DASHBD/surprise-channel/investigations/", "org/missions/D9/IRPT/IRPT_DASHBD/task-orders/")
BD = "computed from Black Diamond values and flows"
REASON = "SOURCE_REPORTS_NO_INCOME"
NEWCOL = "income_claim"
TOKENS = [REASON, NEWCOL]
MAX_EARLIER_TEST_LINES = 14
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
    return r.stdout.decode("utf-8", "replace"), r.returncode


def gitq(root, *a):
    out, rc = git(root, *a)
    need(rc == 0, "git %s failed" % " ".join(a[:2]))
    return out


def base_commit(root):
    out = gitq(root, "log", "--diff-filter=A", "--format=%H", "--", ORDER_REL).split()
    need(out, "the order's first commit is not in this history")
    return out[-1]


def own_commits(root):
    out = gitq(root, "log", "--reverse", "--format=%H", "--author=" + AUTHOR, base_commit(root) + "..HEAD").split()
    need(out, "no commit by %s since the order was issued" % AUTHOR)
    return out


def schema_hash(cols):
    return hashlib.sha256("\n".join(sorted("%s:%s" % (x["name"], x["type"]) for x in cols)).encode("utf-8")).hexdigest()


def census(root, base):
    """The word-boundary census of each token at the base commit: the number of files `git grep -l -w` finds, and the method in words."""
    out = {}
    for t in TOKENS:
        o, rc = git(root, "grep", "-l", "-w", "-e", t, base)
        out[t] = len([ln for ln in o.split("\n") if ln.strip()]) if rc in (0, 1) else None
    return out


# ------------------------------------------------------------------------------------------------ the pure clauses
def check_diff(base, c):
    need(base["contract_version"] == "0.4.3", "the base is not 0.4.3: %s" % base["contract_version"])
    need(c.get("contract_version") == "0.4.4", "contract_version is not 0.4.4 (a patch bump)")
    need("conditional_columns" not in base, "the base already holds conditional_columns")
    moved = sorted(k for k in set(base) | set(c) if k not in ("contract_version", "supersedes", "rule24_record", "conditional_columns") and base.get(k) != c.get(k))
    need(not moved, "sections changed beyond the allowed ones (optional_columns, the 19 columns and both schema hashes must be byte-identical): %s" % moved)
    need(c["schema_hash"] == base["schema_hash"] and schema_hash(c["columns"]) == c["schema_hash"], "schema_hash moved or no longer equals its recomputation over the 19 columns")
    allc = c["columns"] + [{"name": o["name"], "type": o["type"]} for o in c["optional_columns"]]
    need(c["schema_hash_with_optional"] == base["schema_hash_with_optional"] == schema_hash(allc), "schema_hash_with_optional must stay equal to the base's and to its recomputation over the 19 columns plus the SIX optional columns")
    cc = c.get("conditional_columns")
    need(isinstance(cc, list) and len(cc) == 1, "conditional_columns must hold exactly one entry")
    n = cc[0]
    need(set(n) == {"name", "type", "nullable", "meaning", "values", "reason", "emitted_when", "required_when", "rule", "since_schema_version"}, "the conditional column's keys differ: %s" % sorted(n))
    need(n["name"] == NEWCOL and n["type"] == "string" and n["nullable"] is True and n["values"] == ["absent"] and n["reason"] == REASON and nes(n["meaning"]) and nes(n["since_schema_version"]),
         "the new column: name %s, string, nullable, values [absent], reason %s, a meaning and a since_schema_version" % (NEWCOL, REASON))
    need(n["emitted_when"] == {"source": BD} and n["required_when"] == {"source": BD, "income_received": None}, "emitted_when {source: BD} and required_when {source: BD, income_received: null} (the condition as ONE dict of equalities, a JSON null for the null income)")
    rule = n["rule"]
    need(nes(rule) and "income_received" in rule and BD in rule and "never" in rule.lower() and "zero" in rule.lower() and "reject" in rule.lower() and "optional_columns" in rule,
         "income_claim.rule must say: required exactly when income_received is null and the source is the BD-computed one; a row carrying the claim with an income is invalid; a consumer that needs income rejects it; never zero; and why it is not an optional column (it is emitted by one source, so it sits outside the hash basis `optional_columns`)")
    sb, sn = base["supersedes"], c["supersedes"]
    need(isinstance(sn, list) and len(sn) == len(sb) + 1 and sn[:len(sb)] == sb, "supersedes must keep every earlier entry byte-identical and append one")
    e = sn[-1]
    need(e.get("contract_version") == "0.4.3" and e.get("schema_hash") == base["schema_hash"] and e.get("schema_hash_with_optional") == base["schema_hash_with_optional"] and nes(e.get("changes")), "the appended entry must be the 0.4.3 one with its two hashes and a changes sentence")
    r24b, r24n = base["rule24_record"], c["rule24_record"]
    v = r24n.get("v044")
    need({k: x for k, x in r24n.items() if k != "v044"} == r24b and nes(v), "rule24_record must keep every earlier key and add `v044` in words")
    need(NEWCOL in v and REASON in v and "one value" in v.lower() and "no other state" in v.lower() and "income_received" in v, "v044 must name income_claim, the reason code, income_received, say one value and no other state")
    return True


def claim_required(c, row):
    col = next(x for x in c["conditional_columns"] if x["name"] == NEWCOL)
    return all(row.get(k) == v for k, v in col["required_when"].items())


def row_ok(c, row):
    col = next(x for x in c["conditional_columns"] if x["name"] == NEWCOL)
    claim = row.get(NEWCOL)
    if claim is not None and claim not in col["values"]:
        return False
    if claim_required(c, row):
        return claim == "absent"
    return claim is None


def check_behaviour(c):
    good = [("a BD row, no income, the claim", {"source": BD, "income_received": None, NEWCOL: "absent"}), ("a BD row with an income and no claim", {"source": BD, "income_received": 1.5, NEWCOL: None}),
            ("a BD row with income 0.0 and no claim", {"source": BD, "income_received": 0.0}), ("an Orion row with a null income covered by its flow claim", {"source": "orion", "flow_claim": "absent", "income_received": None, NEWCOL: None}),
            ("a holdings row with an income", {"source": "computed from custodian holdings", "income_received": 2.0})]
    bad = [("a BD row, no income, no claim", {"source": BD, "income_received": None, NEWCOL: None}), ("a BD row with an income and the claim", {"source": BD, "income_received": 1.5, NEWCOL: "absent"}),
           ("an Orion row carrying the claim", {"source": "orion", "flow_claim": "absent", "income_received": None, NEWCOL: "absent"}), ("a holdings row carrying the claim", {"source": "computed from custodian holdings", "income_received": None, NEWCOL: "absent"}),
           ("a claim outside its values", {"source": BD, "income_received": None, NEWCOL: "present"}), ("a BD row with income 0.0 and the claim", {"source": BD, "income_received": 0.0, NEWCOL: "absent"})]
    for label, row in good:
        need(row_ok(c, row), "%s must be valid" % label)
    for label, row in bad:
        need(not row_ok(c, row), "%s must be INVALID" % label)
    return len(good), len(bad)


def check_grant(changed):
    bad = [f for f in changed if f not in GRANT_FILES and not f.startswith(GRANT_PREFIXES)]
    need(not bad, "the worker's commits touch files outside its grant: %s" % bad[:3])
    need(CONTRACT_REL in changed and TEST_REL in changed, "the contract and its new test must both change")
    return True


def check_facts(rec, c, base_sha, counts):
    exp = {"contract_version", "base_sha256", "new_column", "hashes", "census", "tests", "words"}
    need(isinstance(rec, dict) and set(rec) == exp, "record keys differ: %s" % (sorted(set(rec) ^ exp) if isinstance(rec, dict) else "?"))
    need(rec["contract_version"] == "0.4.4" and rec["base_sha256"] == base_sha, "version or base sha256 differ")
    need(rec["new_column"] == {"name": NEWCOL, "values": ["absent"], "reason": REASON}, "new_column differs")
    need(rec["hashes"] == {"schema_hash_unchanged": True, "schema_hash_with_optional_unchanged": True}, "hashes block: both hashes unchanged")
    ce = rec["census"]
    need(isinstance(ce, dict) and set(ce) == {"method", "counts"} and nes(ce["method"]) and "git grep -l -w" in ce["method"] and ce["counts"] == counts, "census: the method in words and the counts recounted by the checker %s" % counts)
    need(isinstance(rec["tests"], int) and not isinstance(rec["tests"], bool) and rec["tests"] >= 8, "tests must be a whole number, at least 8")
    need(nes(rec["words"]) and 80 <= len(rec["words"]) <= 1800 and not LONG_DIGITS.findall(rec["words"]), "words must be one paragraph of 80 to 1800 characters with no long digit run")
    return True


def run_pytest(root, files):
    r = subprocess.run([sys.executable, "-m", "pytest", "-q", "-p", "no:cacheprovider"] + list(files), cwd=str(root), capture_output=True, text=True, timeout=900)
    m = re.search(r"(\d+) passed", r.stdout)
    need(r.returncode == 0 and m is not None, "tests failed: %s" % r.stdout[-300:].replace("\n", " | "))
    return int(m.group(1))


def earlier_edit_lines(root, base):
    n = 0
    for f in EARLIER:
        for ln in gitq(root, "diff", "--numstat", base, "HEAD", "--", f).split("\n"):
            parts = ln.split("\t")
            if len(parts) == 3 and parts[0].isdigit() and parts[1].isdigit():
                n += int(parts[0]) + int(parts[1])
    return n


def run(root, cid):
    root = Path(root)
    c = json.loads((root / CONTRACT_REL).read_bytes().decode("utf-8"))
    base = base_commit(root)
    raw = subprocess.run(["git", "-C", str(root), "show", "%s:%s" % (base, CONTRACT_REL)], capture_output=True).stdout
    b = json.loads(raw.decode("utf-8"))
    if cid == "DB152-1-AC1":
        check_diff(b, c)
        print("OK: source contract 0.4.4: only contract_version, one supersedes entry, one rule24_record key, one appended optional column (%s) and the recomputed schema_hash_with_optional differ from the base; schema_hash and every column, enum and section are byte-identical" % NEWCOL)
        return True
    if cid == "DB152-1-AC2":
        check_diff(b, c)
        g, x = check_behaviour(c)
        print("OK: behaviour: a reference rule driven only by the declarations accepts %d rows and refuses %d (a BD null income needs the claim; the claim with an income, on Orion, on holdings or outside its values is invalid)" % (g, x))
        return True
    if cid == "DB152-1-AC3":
        need((root / TEST_REL).is_file(), "no %s" % TEST_REL)
        n_new = run_pytest(root, [TEST_REL])
        need(n_new >= 8, "the new test file holds %d passing tests, at least 8 are owed" % n_new)
        n_old = run_pytest(root, EARLIER)
        need(earlier_edit_lines(root, base) <= MAX_EARLIER_TEST_LINES, "the earlier contract tests may change by at most %d lines in all" % MAX_EARLIER_TEST_LINES)
        changed = set()
        for cm in own_commits(root):
            changed |= set(gitq(root, "show", "--name-only", "--format=", cm).split())
        check_grant(changed)
        rec = json.loads((root / REC_REL).read_bytes().decode("utf-8"))
        check_facts(rec, c, hashlib.sha256(raw).hexdigest(), census(root, base))
        need(rec["tests"] == n_new, "the record's test count differs from the recount %d" % n_new)
        print("OK: %d new tests and the earlier four files' %d tests pass; %d files changed, all in the grant; the facts record equals the contract and the recounted census" % (n_new, n_old, len(changed)))
        return True
    raise Fail("unknown criterion %s" % cid)


def selftest():
    def red(fn, label):
        try:
            fn()
        except Fail:
            return
        raise AssertionError("red arm passed: " + label)
    cols = [{"name": "firm", "type": "string"}, {"name": "income_received", "type": "double", "nullable": False}]
    old_opt = [{"name": "source", "type": "string", "nullable": True}]
    base = {"contract_version": "0.4.3", "schema_hash": schema_hash(cols), "schema_hash_with_optional": schema_hash(cols + old_opt), "supersedes": [{"contract_version": "0.1.0"}], "rule24_record": {"v043": "x"},
            "enums": {"a": [1]}, "columns": cols, "optional_columns": old_opt}
    good = copy.deepcopy(base)
    good["contract_version"] = "0.4.4"
    good["conditional_columns"] = [{"name": NEWCOL, "type": "string", "nullable": True, "meaning": "the claim", "values": ["absent"], "reason": REASON, "emitted_when": {"source": BD},
                                    "required_when": {"source": BD, "income_received": None}, "since_schema_version": "1.5",
                                    "rule": "Required exactly when income_received is null and source is '%s'; a row carrying the claim with an income is invalid; a consumer that needs income rejects it and never treats the null as zero. It sits outside optional_columns because one source emits it." % BD}]
    good["supersedes"].append({"contract_version": "0.4.3", "schema_hash": base["schema_hash"], "schema_hash_with_optional": base["schema_hash_with_optional"], "changes": "income_claim added as a conditional column"})
    good["rule24_record"]["v044"] = "income_claim for income_received: one value (absent), reason %s, no other state." % REASON
    assert check_diff(base, good)
    cc = lambda x: x["conditional_columns"][0]  # noqa: E731
    arms = (("version", lambda x: x.update(contract_version="0.4.3")), ("hash", lambda x: x.update(schema_hash="z")), ("hash_opt moved", lambda x: x.update(schema_hash_with_optional="z")),
            ("enums", lambda x: x["enums"].update(a=[2])), ("column changed", lambda x: x["columns"][0].update(type="int64")), ("optional touched", lambda x: x["optional_columns"][0].update(nullable=False)),
            ("optional appended", lambda x: x["optional_columns"].append({"name": NEWCOL, "type": "string"})), ("two conditional", lambda x: x["conditional_columns"].append({"name": "y"})),
            ("values", lambda x: cc(x).update(values=["absent", "present"])), ("reason", lambda x: cc(x).update(reason="OTHER")), ("emitted_when", lambda x: cc(x).update(emitted_when={"source": "orion"})),
            ("required_when", lambda x: cc(x).update(required_when={"source": BD})), ("required_when orion", lambda x: cc(x).update(required_when={"source": "orion", "income_received": None})),
            ("rule", lambda x: cc(x).update(rule="short")), ("extra key", lambda x: cc(x).update(z=1)), ("supersedes", lambda x: x["supersedes"].pop(0)), ("entry hash", lambda x: x["supersedes"][-1].update(schema_hash="z")),
            ("rule24 missing", lambda x: x["rule24_record"].pop("v044")), ("rule24 words", lambda x: x["rule24_record"].update(v044="changed")), ("rule24 earlier", lambda x: x["rule24_record"].update(v043="y")),
            ("other section", lambda x: x.update(extra=1)))
    for label, fn in arms:
        x = copy.deepcopy(good)
        fn(x)
        red(lambda: check_diff(base, x), label)
    assert check_behaviour(good) == (5, 6)
    nb = copy.deepcopy(good)
    nb["conditional_columns"][0]["required_when"] = {"source": "nothing", "income_received": None}
    red(lambda: check_behaviour(nb), "weakened required_when")
    assert check_grant({CONTRACT_REL, TEST_REL, EARLIER[0], D + AUTHOR + "/x.json"})
    red(lambda: check_grant({CONTRACT_REL, TEST_REL, "lib/x.py"}), "outside grant")
    red(lambda: check_grant({CONTRACT_REL}), "no test")
    counts = {REASON: 3, NEWCOL: 5}
    rec = {"contract_version": "0.4.4", "base_sha256": "a" * 64, "new_column": {"name": NEWCOL, "values": ["absent"], "reason": REASON}, "hashes": {"schema_hash_unchanged": True, "schema_hash_with_optional_unchanged": True},
           "census": {"method": "git grep -l -w <token> at the base commit, files counted", "counts": counts}, "tests": 8, "words": "w" * 100}
    assert check_facts(rec, good, "a" * 64, counts)
    farms = (("version", lambda r: r.update(contract_version="0.4.3")), ("base", lambda r: r.update(base_sha256="b" * 64)), ("column", lambda r: r["new_column"].update(reason="x")), ("hash", lambda r: r["hashes"].update(schema_hash_with_optional_unchanged=False)),
             ("census counts", lambda r: r["census"].update(counts={REASON: 1, NEWCOL: 1})), ("census method", lambda r: r["census"].update(method="by eye")), ("tests", lambda r: r.update(tests=2)),
             ("extra", lambda r: r.update(z=1)), ("words", lambda r: r.update(words="short")), ("digits", lambda r: r.update(words="w" * 100 + " 123456789")))
    for label, fn in farms:
        r2 = copy.deepcopy(rec)
        fn(r2)
        red(lambda: check_facts(r2, good, "a" * 64, counts), label)
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
