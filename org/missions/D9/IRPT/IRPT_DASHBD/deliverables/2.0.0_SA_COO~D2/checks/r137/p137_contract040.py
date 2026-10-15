"""IRPT_DASHBD round 137, workstream B-49F + contract (issuer 2.0.0_SA_COO~D2, the contract's owner) -- DB-b-270, account_return_daily CONTRACT 0.4.0
(CTO ROUND ANALYSIS IRPT_DASHBD B-IN ROUND 118 ADDENDUM 4 @10e1032651, msg 8546, on 2.0.0_SA_COO~I2 msg 8543): the Scope (Orion) feed carries no external_flow
or income_received, so the two columns become nullable ONLY where source == "orion" and the row says so in a claim column; the 19 columns, their types and schema_hash
do not move, so every 0.3.0 writer still validates. Orion's integer account id is kept in a new optional column. LOCAL: one JSON standard, one test file.

  DB-b-270 (~219)   org/standards/IRPT_DASHBD_ACCOUNT_RETURN_DAILY_CONTRACT.json (0.4.0) + tests/test_account_return_contract_040.py + a facts record
                    DB137-2-AC1 (the contract's declarations, pure),
                    DB137-2-AC2 (BEHAVIOUR: a reference validator driven ONLY by the contract's declarations accepts the 0.3.0 rows and the claimed Orion row and rejects five bad rows),
                    DB137-2-AC3 (the worker's tests pass beside the earlier contract-reading tests; the facts record equals the contract)

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
TEST_REL = "data/assets/scripts/gold/irpt_reporting/tests/test_account_return_contract_040.py"
EARLIER_TESTS = ("data/assets/scripts/gold/irpt_reporting/tests/test_cottonwood_bd_account_return_daily.py",
                 "data/assets/scripts/gold/irpt_reporting/tests/test_cottonwood_report_reader.py")
REC_REL = D + "0.9.0_WK_IRPT_DASHBD~219/RD_CONTRACT_040_FACTS_R137.json"
ORDER_REL = "org/missions/D9/IRPT/IRPT_DASHBD/task-orders/IRPT_DASHBD.TO-DB-b-270.account-return-contract-040-flows-nullable-for-orion-and-source-account-id.md"
AUTHOR = "0.9.0_WK_IRPT_DASHBD~219"
GRANT_FILES = {CONTRACT_REL, TEST_REL, EARLIER_TESTS[0]}
MAX_EARLIER_TEST_LINES = 8
GRANT_PREFIXES = (D + "0.9.0_WK_IRPT_DASHBD~219/", "org/missions/D9/IRPT/IRPT_DASHBD/surprise-channel/investigations/", "org/missions/D9/IRPT/IRPT_DASHBD/task-orders/")
FLOW = ("external_flow", "income_received")
BASE_HASH = "1b25d37ba6cfcf5a7413373ccdca57e306b86614aff94472ca65ca0025484946"
BASE_OPT_HASH = "bc70ee2f2e0b54fd13e3b11fedae943003d4172199a561a4923c3e1a1ad59a27"
OTHER17_SHA = "763754e88fd175785ea53c0dca4e211d3992e3221096c45780c68664c7b41216"
SOURCE_SHA = "d070b67e74d2dd6798ca682174533b6aa1adb8ca9975af09b542da9978f3d2ee"
SERVED_SHA = "f32d74fd684628bf10e2cdabe8086e591cfe31c6c78330d2da83aed619b4ed9d"
CLAIM_REASON = "vendor-reported return, not built from flows"
NULLABLE_WHEN = {"source": "orion", "flow_claim": "absent"}
LONG_DIGITS = re.compile(r"\d{8,}")
DIGIT_OK_KEYS = ("schema_hash", "hash_with_optional", "schema_hash_with_optional", "sha256")


class Fail(Exception):
    pass


def need(cond, msg):
    if not cond:
        raise Fail(msg)


def nes(x):
    return isinstance(x, str) and x.strip() != ""


def sha(x):
    return hashlib.sha256(json.dumps(x, sort_keys=True, separators=(",", ":")).encode()).hexdigest()


def schema_hash(cols):
    return hashlib.sha256("\n".join(sorted("%s:%s" % (c["name"], c["type"]) for c in cols)).encode("utf-8")).hexdigest()


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
    need(c.get("contract_version") == "0.4.0", "contract_version is not 0.4.0 (a minor bump)")
    cols = c["columns"]
    need(len(cols) == 19 and schema_hash(cols) == c["schema_hash"] == BASE_HASH, "the 19 columns, their types or the schema_hash moved")
    need(sha([x for x in cols if x["name"] not in FLOW]) == OTHER17_SHA, "one of the 17 other columns changed")
    flows = [x for x in cols if x["name"] in FLOW]
    need([x["name"] for x in flows] == list(FLOW), "the two flow columns are missing or out of order")
    for x in flows:
        need(x.get("type") == "double" and x.get("nullable") is False, "%s must stay double and nullable false (nullability is conditional, never general)" % x["name"])
        need(x.get("nullable_when") == NULLABLE_WHEN, "%s.nullable_when must equal %s: %s" % (x["name"], NULLABLE_WHEN, x.get("nullable_when")))
        need(nes(x.get("meaning")), "%s lost its meaning" % x["name"])
    oc = c.get("optional_columns")
    need(isinstance(oc, list) and [o.get("name") for o in oc] == ["source", "flow_claim", "source_account_id"], "optional_columns must be exactly source, flow_claim, source_account_id in order")
    need(sha(oc[0]) == SOURCE_SHA, "the optional column `source` changed")
    fc, sa = oc[1], oc[2]
    need(fc.get("type") == "string" and fc.get("nullable") is True and fc.get("values") == ["absent"] and fc.get("reason") == CLAIM_REASON and nes(fc.get("meaning")) and fc.get("since_schema_version") == "1.2",
         "flow_claim: string, nullable, values [absent], reason '%s', since_schema_version 1.2" % CLAIM_REASON)
    rule = (fc.get("rule") or "")
    need(nes(rule) and "orion" in rule and "reject" in rule.lower() and "never" in rule.lower() and "zero" in rule.lower(), "flow_claim.rule must say: required when a flow is null, only for orion, a consumer that needs flows rejects it in words and never treats a null as zero")
    need(sa.get("type") == "int64" and sa.get("nullable") is True and nes(sa.get("meaning")) and "Orion" in sa["meaning"] and sa.get("since_schema_version") == "1.2" and nes(sa.get("rule")),
         "source_account_id: int64, nullable, meaning naming Orion, rule, since_schema_version 1.2")
    allcols = cols + [{"name": "source", "type": "string"}, {"name": "flow_claim", "type": "string"}, {"name": "source_account_id", "type": "int64"}]
    need(c.get("schema_hash_with_optional") == schema_hash(allcols), "schema_hash_with_optional is not the recomputed hash over the 19 columns plus source, flow_claim and source_account_id")
    sup = [x for x in c.get("supersedes", []) if x.get("contract_version") == "0.3.0"]
    need(len(sup) == 1 and sup[0].get("schema_hash") == BASE_HASH and sup[0].get("schema_hash_with_optional") == BASE_OPT_HASH and sup[0].get("changes"), "supersedes must carry the 0.3.0 entry with both hashes and its changes")
    need(sha(c.get("served_day_rules")) == SERVED_SHA, "served_day_rules changed")
    sr = (c.get("source_rules") or {}).get("orion")
    need(isinstance(sr, dict) and set(sr) == {"flows", "business_date", "account_id"} and all(nes(v) for v in sr.values()), "source_rules.orion must hold exactly flows, business_date and account_id, in words")
    need("flow_claim" in sr["flows"], "source_rules.orion.flows must name flow_claim")
    need("compound" in sr["business_date"] and "ABSENT" in sr["business_date"] and "trading" in sr["business_date"], "source_rules.orion.business_date must say calendar factors compound into the next trading day and an ABSENT trading day stays ABSENT")
    need("account_dim" in sr["account_id"] and "UNMAPPED_ACCOUNT" in sr["account_id"] and "source_account_id" in sr["account_id"], "source_rules.orion.account_id must name account_dim, source_account_id and UNMAPPED_ACCOUNT")
    return True


def row_problems(c, row):
    """A reference validator driven ONLY by the contract's declarations. Returns the list of problems (empty = valid)."""
    out = []
    names = set()
    for col in c["columns"]:
        names.add(col["name"])
        v = row.get(col["name"])
        if v is None:
            cond = col.get("nullable_when")
            ok = col.get("nullable") is True or (isinstance(cond, dict) and all(row.get(k) == val for k, val in cond.items()))
            if not ok:
                out.append("%s is null" % col["name"])
    claim = row.get("flow_claim")
    nulls = [n for n in FLOW if row.get(n) is None]
    if claim is not None and claim not in next(o for o in c["optional_columns"] if o["name"] == "flow_claim")["values"]:
        out.append("flow_claim not in its values")
    if claim is not None and not nulls:
        out.append("flow_claim without a null flow")
    return out


def base_row():
    return {"firm": "f", "account_id": "A1", "business_date": "2026-07-13", "market_value_eod": 1.0, "external_flow": 0.0, "income_received": 0.0, "income_return": None, "total_return_daily": 0.01,
            "return_basis": "TWR", "holdings_price_return": None, "holdings_price_return_reason": None, "fee_amount": None, "fee_amount_reason": "FEE_RAIL_UNUSED", "day_quality": "MEASURED",
            "guard_state": "GRADED_AGREED", "history_scope": "FULL", "carried_days": 1, "method_version": 2, "schema_version": "1.1", "source": "computed from Black Diamond values and flows"}


def check_behaviour(c):
    def r(**kw):
        x = base_row()
        x.update(kw)
        return x
    good = (("a 0.3.0 Black Diamond row (flows set, no claim)", r()), ("a 0.3.0 row with a null source and flows set", r(source=None)),
            ("an Orion row with null flows and the claim", r(source="orion", external_flow=None, income_received=None, flow_claim="absent", source_account_id=7)),
            ("an Orion row with flows set and no claim", r(source="orion")))
    bad = (("an Orion row with null flows and NO claim", r(source="orion", external_flow=None, income_received=None)),
           ("a Black Diamond row with null flows and the claim", r(external_flow=None, income_received=None, flow_claim="absent")),
           ("a null-source row with null flows and the claim", r(source=None, external_flow=None, income_received=None, flow_claim="absent")),
           ("an Orion row with flows set and the claim", r(source="orion", flow_claim="absent")),
           ("an Orion row with null flows and a claim outside its values", r(source="orion", external_flow=None, income_received=None, flow_claim="zero")),
           ("an Orion row with a null market value", r(source="orion", market_value_eod=None, flow_claim="absent")))
    for label, row in good:
        p = row_problems(c, row)
        need(not p, "%s must validate: %s" % (label, p))
    for label, row in bad:
        need(row_problems(c, row), "%s must be rejected" % label)
    return len(good), len(bad)


def check_grant(changed):
    bad = [f for f in changed if f not in GRANT_FILES and not f.startswith(GRANT_PREFIXES)]
    need(not bad, "the worker's commits touch files outside its grant: %s" % bad[:3])
    need(CONTRACT_REL in changed and TEST_REL in changed, "the contract and its test must both change")
    return True


def digit_runs(x, key=""):
    if isinstance(x, dict):
        return [h for k, v in x.items() for h in digit_runs(v, str(k))]
    if isinstance(x, list):
        return [h for v in x for h in digit_runs(v, key)]
    if isinstance(x, str) and key not in DIGIT_OK_KEYS:
        return LONG_DIGITS.findall(x)
    return []


def check_facts(rec, c):
    exp = {"contract_version", "schema_hash", "hash_with_optional", "optional_columns", "nullable_only_for", "words"}
    need(isinstance(rec, dict) and set(rec) == exp, "record keys differ: %s" % (sorted(set(rec) ^ exp) if isinstance(rec, dict) else "?"))
    need(rec["contract_version"] == "0.4.0" and rec["schema_hash"] == c["schema_hash"] and rec["hash_with_optional"] == c["schema_hash_with_optional"], "version or hashes differ from the contract")
    need(rec["optional_columns"] == ["source", "flow_claim", "source_account_id"] and rec["nullable_only_for"] == NULLABLE_WHEN, "optional_columns or nullable_only_for")
    need(nes(rec["words"]) and 80 <= len(rec["words"]) <= 1800 and not digit_runs(rec), "words must be one paragraph of 80 to 1800 characters with no long digit run")
    return True


def run_pytest(root, files):
    r = subprocess.run([sys.executable, "-m", "pytest", "-q", "-p", "no:cacheprovider"] + list(files), cwd=str(root), capture_output=True, text=True, timeout=600)
    m = re.search(r"(\d+) passed", r.stdout)
    need(r.returncode == 0 and m is not None, "tests failed: %s" % r.stdout[-300:].replace("\n", " | "))
    return int(m.group(1))


def run(root, cid):
    root = Path(root)
    if cid == "DB137-2-AC1":
        c = load_json(root, CONTRACT_REL)
        check_contract(c)
        changed = set()
        together = False
        for cm in own_commits(root):
            files = set(git(root, "show", "--name-only", "--format=", cm).split())
            together = together or {CONTRACT_REL, TEST_REL} <= files
            changed |= files
        check_grant(changed)
        base = git(root, "log", "--diff-filter=A", "--format=%H", "--", ORDER_REL).split()[-1]
        stat = git(root, "diff", "--numstat", base, "HEAD", "--", EARLIER_TESTS[0]).split()
        edited = (int(stat[0]) + int(stat[1])) if len(stat) >= 2 else 0
        need(edited <= MAX_EARLIER_TEST_LINES, "the earlier Cottonwood test may change by at most %d lines (its one hash assertion), not %d" % (MAX_EARLIER_TEST_LINES, edited))
        need(together, "the contract and its test must land in ONE commit (the ruling: 0.4.0 lands as one commit with its test)")
        print("OK: contract 0.4.0: the 19 columns and schema_hash are unchanged; the two flow columns are nullable only when %s; optional columns source, flow_claim, source_account_id carry hash %s; %d files changed, all in the grant"
              % (NULLABLE_WHEN, c["schema_hash_with_optional"][:12], len(changed)))
        return True
    if cid == "DB137-2-AC2":
        c = load_json(root, CONTRACT_REL)
        check_contract(c)
        g, b = check_behaviour(c)
        print("OK: behaviour: a validator driven only by the contract accepts %d rows (0.3.0 rows, the claimed Orion row) and rejects %d (no claim, wrong source, claim without a null, claim outside its values, other nulls)" % (g, b))
        return True
    if cid == "DB137-2-AC3":
        c = load_json(root, CONTRACT_REL)
        need((root / TEST_REL).is_file(), "no %s" % TEST_REL)
        n_new = run_pytest(root, [TEST_REL])
        need(n_new >= 6, "the new test file holds %d passing tests, at least 6 are owed" % n_new)
        n_old = run_pytest(root, EARLIER_TESTS)
        check_facts(load_json(root, REC_REL), c)
        print("OK: %d new tests and %d earlier contract-reading tests pass; facts record equals the contract" % (n_new, n_old))
        return True
    raise Fail("unknown criterion %s" % cid)


def selftest():
    def red(fn, label):
        try:
            fn()
        except Fail:
            return
        raise AssertionError("red arm passed: " + label)
    # behaviour and grant and facts on a synthetic contract (the 17-column and hash clauses are exercised against the real file by the scratch reference)
    c = {"columns": [{"name": "firm", "type": "string", "nullable": False}, {"name": "market_value_eod", "type": "double", "nullable": False},
                     {"name": "external_flow", "type": "double", "nullable": False, "nullable_when": dict(NULLABLE_WHEN)},
                     {"name": "income_received", "type": "double", "nullable": False, "nullable_when": dict(NULLABLE_WHEN)}],
         "optional_columns": [{"name": "source", "values": []}, {"name": "flow_claim", "values": ["absent"]}, {"name": "source_account_id"}]}
    assert row_problems(c, {"firm": "f", "market_value_eod": 1.0, "external_flow": 0.0, "income_received": 0.0}) == []
    assert row_problems(c, {"firm": "f", "market_value_eod": 1.0, "source": "orion", "flow_claim": "absent", "external_flow": None, "income_received": None}) == []
    assert row_problems(c, {"firm": "f", "market_value_eod": 1.0, "source": "orion", "external_flow": None, "income_received": None}) != []
    assert row_problems(c, {"firm": "f", "market_value_eod": 1.0, "source": "x", "flow_claim": "absent", "external_flow": None, "income_received": None}) != []
    assert row_problems(c, {"firm": "f", "market_value_eod": 1.0, "source": "orion", "flow_claim": "absent", "external_flow": 1.0, "income_received": 1.0}) != []
    c2 = copy.deepcopy(c)
    c2["columns"][2]["nullable"] = True
    # a contract that is nullable everywhere would accept the Black Diamond row with null flows: the behaviour check must see that
    full = copy.deepcopy(c)
    full["columns"][2].pop("nullable_when")
    full["columns"][3].pop("nullable_when")
    red(lambda: check_behaviour_on(full), "flows never nullable: the Orion row cannot validate")
    unconditional = copy.deepcopy(c)
    unconditional["columns"][2]["nullable"] = True
    unconditional["columns"][3]["nullable"] = True
    red(lambda: check_behaviour_on(unconditional), "flows nullable everywhere: the Black Diamond null row validates")
    assert check_grant({CONTRACT_REL, TEST_REL, D + "0.9.0_WK_IRPT_DASHBD~219/x.json"})
    red(lambda: check_grant({CONTRACT_REL, TEST_REL, "lib/x.py"}), "outside grant")
    red(lambda: check_grant({CONTRACT_REL}), "no test")
    red(lambda: check_grant({TEST_REL}), "no contract")
    rec = {"contract_version": "0.4.0", "schema_hash": "a" * 64, "hash_with_optional": "b" * 64, "optional_columns": ["source", "flow_claim", "source_account_id"], "nullable_only_for": dict(NULLABLE_WHEN), "words": "w" * 100}
    cc = {"schema_hash": "a" * 64, "schema_hash_with_optional": "b" * 64}
    assert check_facts(rec, cc)
    arms = (("version", lambda r: r.update(contract_version="0.3.0")), ("hash", lambda r: r.update(schema_hash="c" * 64)), ("optional hash", lambda r: r.update(hash_with_optional="c" * 64)),
            ("columns", lambda r: r.update(optional_columns=["source"])), ("nullable_only_for", lambda r: r.update(nullable_only_for={"source": "orion"})),
            ("words", lambda r: r.update(words="short")), ("extra", lambda r: r.update(z=1)), ("digits", lambda r: r.update(words="w" * 100 + " 123456789")))
    for label, fn in arms:
        r2 = dict(rec)
        fn(r2)
        red(lambda: check_facts(r2, cc), label)
    print("selftest: behaviour (2 red arms), grant (3), facts (%d red arms) clauses behave" % len(arms))
    print("selftest PASS")


def check_behaviour_on(c):
    """Selftest shim: check_behaviour needs the 19-column rows; build a synthetic full contract around the two flow columns."""
    full = {"columns": [{"name": k, "type": "string", "nullable": k not in base_row() or base_row()[k] is None} for k in base_row() if k not in FLOW + ("flow_claim",)]
            + [x for x in c["columns"] if x["name"] in FLOW], "optional_columns": c["optional_columns"]}
    for col in full["columns"]:
        if col["name"] in ("source",):
            col["nullable"] = True
    return check_behaviour(full)


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
