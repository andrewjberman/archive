"""IRPT_DASHBD round 147, workstream B-49F + contract (issuer 2.0.0_SA_COO~D2, the contract's sole writer) -- DB-b-282, the SOURCE TABLE contract 0.4.3: `income_received` may be null where the row's
`source` is 'computed from Black Diamond values and flows' (that method separates no income; row IRPT_DASHBD-D2-S104: null on 52,468 of 52,468 Cottonwood floor-era rows). One declared attribute on
one column, `also_nullable_when`, beside the existing `nullable_when`; the 19 columns' hashed fields, both schema hashes, every enum and every other section stay byte-identical. LOCAL: a JSON standard and a test file.

  DB-b-282 (~227)   org/standards/IRPT_DASHBD_ACCOUNT_RETURN_DAILY_CONTRACT.json (0.4.3) + data/assets/scripts/gold/irpt_reporting/tests/test_account_return_contract_043.py + a facts record
                    DB150-1-AC1 (the contract differs from the base ONLY in the allowed places),
                    DB150-1-AC2 (BEHAVIOUR: a reference rule driven only by the declarations accepts five rows and rejects five),
                    DB150-1-AC3 (the new tests, the earlier three contract test files, the grant, the facts record)

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
TEST_REL = TEST_DIR + "test_account_return_contract_043.py"
EARLIER = [TEST_DIR + "test_account_return_contract_040.py", TEST_DIR + "test_account_return_contract_041.py", TEST_DIR + "test_account_return_contract_042.py"]
AUTHOR = "0.9.0_WK_IRPT_DASHBD~227"
REC_REL = D + AUTHOR + "/RD_CONTRACT_043_FACTS_R147.json"
ORDER_REL = "org/missions/D9/IRPT/IRPT_DASHBD/task-orders/IRPT_DASHBD.TO-DB-b-282.source-contract-043-income-null-for-bd-computed.md"
GRANT_FILES = {CONTRACT_REL, TEST_REL} | set(EARLIER)
GRANT_PREFIXES = (D + AUTHOR + "/", "org/missions/D9/IRPT/IRPT_DASHBD/surprise-channel/investigations/", "org/missions/D9/IRPT/IRPT_DASHBD/task-orders/")
BD = "computed from Black Diamond values and flows"
ATTR = "also_nullable_when"
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


def sha(x):
    return hashlib.sha256(json.dumps(x, sort_keys=True, separators=(",", ":")).encode()).hexdigest()


# ------------------------------------------------------------------------------------------------ the pure clauses
def check_diff(base, c):
    """The new contract differs from the base only in: contract_version, supersedes (one entry appended), rule24_record (one key `v043` added), and the income_received column's ATTR."""
    need(base["contract_version"] == "0.4.2", "the base is not 0.4.2: %s" % base["contract_version"])
    need(c.get("contract_version") == "0.4.3", "contract_version is not 0.4.3 (a patch bump)")
    moved = sorted(k for k in set(base) | set(c) if k not in ("contract_version", "supersedes", "rule24_record", "columns") and base.get(k) != c.get(k))
    need(not moved, "sections changed beyond the allowed ones: %s" % moved)
    need(c["schema_hash"] == base["schema_hash"] and c["schema_hash_with_optional"] == base["schema_hash_with_optional"], "a schema hash moved: neither hash may change")
    bc, nc = base["columns"], c["columns"]
    need([x["name"] for x in bc] == [x["name"] for x in nc], "the column list changed")
    for b, n in zip(bc, nc):
        if b["name"] == "income_received":
            need({k: v for k, v in n.items() if k != ATTR} == b, "income_received changed beyond %s" % ATTR)
            need(n.get(ATTR) == [{"source": BD}], "income_received.%s must be exactly [{\"source\": %r}]" % (ATTR, BD))
        else:
            need(b == n, "column %s changed" % b["name"])
    sb, sn = base["supersedes"], c["supersedes"]
    need(isinstance(sn, list) and len(sn) == len(sb) + 1 and sn[:len(sb)] == sb, "supersedes must keep every earlier entry byte-identical and append one")
    e = sn[-1]
    need(e.get("contract_version") == "0.4.2" and e.get("schema_hash") == base["schema_hash"] and e.get("schema_hash_with_optional") == base["schema_hash_with_optional"] and nes(e.get("changes")),
         "the appended entry must be the 0.4.2 one: its version, both hashes (unchanged) and a changes sentence")
    r24b, r24n = base["rule24_record"], c["rule24_record"]
    need({k: v for k, v in r24n.items() if k != "v043"} == r24b and nes(r24n.get("v043")) and BD in r24n["v043"] and "no enum" in r24n["v043"].lower() and "income_received" in r24n["v043"],
         "rule24_record must keep every earlier key and add `v043`: words naming income_received, the source value, and that no enum member is added")
    return True


def income_null_ok(c, row):
    """The reference rule, driven ONLY by the declarations: may this row's income_received be null?"""
    col = next(x for x in c["columns"] if x["name"] == "income_received")
    conds = [col.get("nullable_when")] + list(col.get(ATTR) or [])
    return any(isinstance(w, dict) and w and all(row.get(k) == v for k, v in w.items()) for w in conds)


def check_behaviour(c):
    good = [("a BD row with null income", {"source": BD, "flow_claim": None}), ("an Orion row with the flow claim", {"source": "orion", "flow_claim": "absent"}),
            ("a BD row with a flow claim", {"source": BD, "flow_claim": "absent"}), ("a BD row", {"source": BD}), ("a BD row with more keys", {"source": BD, "x": 1, "flow_claim": None})]
    bad = [("a holdings row", {"source": "computed from custodian holdings", "flow_claim": None}), ("an Orion row without the claim", {"source": "orion", "flow_claim": None}),
           ("a row with no source", {"flow_claim": None}), ("a row with a null source", {"source": None}), ("a row with a near-miss source", {"source": BD.upper()})]
    for label, row in good:
        need(income_null_ok(c, row), "%s must allow a null income" % label)
    for label, row in bad:
        need(not income_null_ok(c, row), "%s must NOT allow a null income" % label)
    return len(good), len(bad)


def check_grant(changed):
    bad = [f for f in changed if f not in GRANT_FILES and not f.startswith(GRANT_PREFIXES)]
    need(not bad, "the worker's commits touch files outside its grant: %s" % bad[:3])
    need(CONTRACT_REL in changed and TEST_REL in changed, "the contract and its new test must both change")
    return True


def check_facts(rec, c, base_sha):
    exp = {"contract_version", "base_sha256", "also_nullable_when", "hashes_unchanged", "tests", "words"}
    need(isinstance(rec, dict) and set(rec) == exp, "record keys differ: %s" % (sorted(set(rec) ^ exp) if isinstance(rec, dict) else "?"))
    need(rec["contract_version"] == "0.4.3" and rec["base_sha256"] == base_sha and rec["hashes_unchanged"] is True, "version, base sha256 or the hash claim differ")
    col = next(x for x in c["columns"] if x["name"] == "income_received")
    need(rec["also_nullable_when"] == col.get(ATTR), "also_nullable_when differs from the contract")
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
        for ln in git(root, "diff", "--numstat", base, "HEAD", "--", f).decode().split("\n"):
            parts = ln.split("\t")
            if len(parts) == 3 and parts[0].isdigit() and parts[1].isdigit():
                n += int(parts[0]) + int(parts[1])
    return n


def run(root, cid):
    root = Path(root)
    c = json.loads((root / CONTRACT_REL).read_bytes().decode("utf-8"))
    base = base_commit(root)
    raw = git(root, "show", "%s:%s" % (base, CONTRACT_REL))
    b = json.loads(raw.decode("utf-8"))
    if cid == "DB150-1-AC1":
        check_diff(b, c)
        print("OK: source contract 0.4.3: only contract_version, one supersedes entry, one rule24_record key and income_received.%s differ from the base; both schema hashes and every other column, enum and section are byte-identical" % ATTR)
        return True
    if cid == "DB150-1-AC2":
        check_diff(b, c)
        g, x = check_behaviour(c)
        print("OK: behaviour: a reference rule driven only by the declarations allows a null income on %d rows (BD, Orion with the claim) and refuses it on %d (holdings, Orion without the claim, no source, null source, a near-miss)" % (g, x))
        return True
    if cid == "DB150-1-AC3":
        need((root / TEST_REL).is_file(), "no %s" % TEST_REL)
        n_new = run_pytest(root, [TEST_REL])
        need(n_new >= 8, "the new test file holds %d passing tests, at least 8 are owed" % n_new)
        n_old = run_pytest(root, EARLIER)
        need(earlier_edit_lines(root, base) <= MAX_EARLIER_TEST_LINES, "the earlier contract tests may change by at most %d lines in all" % MAX_EARLIER_TEST_LINES)
        changed = set()
        for cm in own_commits(root):
            changed |= set(git(root, "show", "--name-only", "--format=", cm).decode().split())
        check_grant(changed)
        rec = json.loads((root / REC_REL).read_bytes().decode("utf-8"))
        check_facts(rec, c, hashlib.sha256(raw).hexdigest())
        need(rec["tests"] == n_new, "the record's test count differs from the recount %d" % n_new)
        print("OK: %d new tests and the earlier three files' %d tests pass; %d files changed, all in the grant; the facts record equals the contract" % (n_new, n_old, len(changed)))
        return True
    raise Fail("unknown criterion %s" % cid)


def selftest():
    def red(fn, label):
        try:
            fn()
        except Fail:
            return
        raise AssertionError("red arm passed: " + label)
    base = {"contract_version": "0.4.2", "schema_hash": "h1", "schema_hash_with_optional": "h2", "supersedes": [{"contract_version": "0.1.0"}], "rule24_record": {"v042": "x"}, "enums": {"a": [1]},
            "columns": [{"name": "firm", "type": "string"}, {"name": "income_received", "type": "double", "nullable": False, "nullable_when": {"source": "orion", "flow_claim": "absent"}}]}
    good = copy.deepcopy(base)
    good["contract_version"] = "0.4.3"
    good["supersedes"].append({"contract_version": "0.4.2", "schema_hash": "h1", "schema_hash_with_optional": "h2", "changes": "income may be null for BD"})
    good["rule24_record"]["v043"] = "income_received gains a source " + BD + "; no enum member is added"
    good["columns"][1][ATTR] = [{"source": BD}]
    assert check_diff(base, good)
    arms = (("version", lambda x: x.update(contract_version="0.4.2")), ("hash", lambda x: x.update(schema_hash="z")), ("enums", lambda x: x["enums"].update(a=[2])), ("other column", lambda x: x["columns"][0].update(type="int64")),
            ("attr value", lambda x: x["columns"][1].update({ATTR: [{"source": "orion"}]})), ("attr missing", lambda x: x["columns"][1].pop(ATTR)), ("income changed", lambda x: x["columns"][1].update(nullable=True)),
            ("supersedes", lambda x: x["supersedes"].pop(0)), ("entry hash", lambda x: x["supersedes"][-1].update(schema_hash="z")), ("rule24", lambda x: x["rule24_record"].pop("v043")),
            ("rule24 words", lambda x: x["rule24_record"].update(v043="changed")), ("rule24 earlier", lambda x: x["rule24_record"].update(v042="y")))
    for label, fn in arms:
        x = copy.deepcopy(good)
        fn(x)
        red(lambda: check_diff(base, x), label)
    assert check_behaviour(good) == (5, 5)
    nb = copy.deepcopy(good)
    nb["columns"][1].pop(ATTR)
    red(lambda: check_behaviour(nb), "no attribute")
    assert check_grant({CONTRACT_REL, TEST_REL, EARLIER[0], D + AUTHOR + "/x.json"})
    red(lambda: check_grant({CONTRACT_REL, TEST_REL, "lib/x.py"}), "outside grant")
    red(lambda: check_grant({CONTRACT_REL}), "no test")
    rec = {"contract_version": "0.4.3", "base_sha256": "a" * 64, "also_nullable_when": [{"source": BD}], "hashes_unchanged": True, "tests": 8, "words": "w" * 100}
    assert check_facts(rec, good, "a" * 64)
    farms = (("version", lambda r: r.update(contract_version="0.4.2")), ("base", lambda r: r.update(base_sha256="b" * 64)), ("attr", lambda r: r.update(also_nullable_when=[])), ("hashes", lambda r: r.update(hashes_unchanged=False)),
             ("tests", lambda r: r.update(tests=2)), ("extra", lambda r: r.update(z=1)), ("words", lambda r: r.update(words="short")), ("digits", lambda r: r.update(words="w" * 100 + " 123456789")))
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
