"""IRPT_DASHBD round 142, workstream B-49F + contract (issuer 2.0.0_SA_COO~D2, the contract's owner) -- DB-b-275, account_return_daily CONTRACT 0.4.2
(CTO ROUND-124 ANALYSIS B-IN @e5c8b143fe addition 2, msg 8655: "A claim a consumer rejects on has to be a contract field (A VALUE MUST CARRY ITS CLAIM)"): ONE new optional nullable column,
market_value_eod_claim, enum measured | inferred, REQUIRED on every PRESENT Orion row (the Scope feed carries no end value, so the adapter infers it from the next calendar day's start value),
with its rule-24 record and word-boundary token census. The 19 columns, their types, schema_hash, every enum and every earlier optional column do not move; every 0.3.0, 0.4.0 and 0.4.1 writer
still validates. LOCAL: one JSON standard, one new test file, two bounded edits of the earlier contract tests.

  DB-b-275 (~223)   org/standards/IRPT_DASHBD_ACCOUNT_RETURN_DAILY_CONTRACT.json (0.4.2) + tests/test_account_return_contract_042.py + bounded edits of the 0.4.0 and 0.4.1 tests + a facts record
                    DB142-1-AC1 (the contract's declarations, pure, and the grant),
                    DB142-1-AC2 (BEHAVIOUR: a reference validator driven ONLY by the contract's declarations; the token census recount),
                    DB142-1-AC3 (the worker's tests pass beside the earlier contract-reading tests; the facts record equals the contract)

Usage: python <this file> <repo_root> <criterion_id>      prints "<id> PASS" or "<id> FAIL" last
       python <this file> --selftest                       the pure clauses on synthetic arms
"""
import copy
import importlib.util
import re
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
_spec = importlib.util.spec_from_file_location("p140", str(HERE.parent / "r140" / "p140_contract041.py"))
p140 = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(p140)
p137c = p140.p137c

D = p140.D
CONTRACT_REL = p140.CONTRACT_REL
TEST_REL = "data/assets/scripts/gold/irpt_reporting/tests/test_account_return_contract_042.py"
TEST040_REL, TEST041_REL = p140.TEST040_REL, p140.TEST_REL
EARLIER_TESTS = (p140.EARLIER_TESTS[0], p140.EARLIER_TESTS[1], TEST040_REL, TEST041_REL)
REC_REL = D + "0.9.0_WK_IRPT_DASHBD~223/RD_CONTRACT_042_FACTS_R142.json"
ORDER_REL = "org/missions/D9/IRPT/IRPT_DASHBD/task-orders/IRPT_DASHBD.TO-DB-b-275.account-return-contract-042-market-value-eod-claim.md"
AUTHOR = "0.9.0_WK_IRPT_DASHBD~223"
GRANT_FILES = {CONTRACT_REL, TEST_REL, TEST040_REL, TEST041_REL}
MAX_EARLIER_TEST_LINES = 14
MAX_041_TEST_LINES = 120  # Amendment 1: the 0.4.1 test's validator and Orion fixtures move with the new required claim
GRANT_PREFIXES = (D + "0.9.0_WK_IRPT_DASHBD~223/", "org/missions/D9/IRPT/IRPT_DASHBD/surprise-channel/investigations/", "org/missions/D9/IRPT/IRPT_DASHBD/task-orders/")
COLS_SHA = "ae1a77b847a78b30270501595607f13bc092339bee43dc6ca2557169049f222d"
ENUMS_NO_RB_SHA = "e9f68d54c40ffa20bf4a125f7afe4bd553502a9ea5f5257bfcbbd4c7c021b122"
SR3_SHA = "96646019800fe58d528d2436e2d58d36196203896a0155cd6ac0378e74a54c86"
OPT5_SHA = "ba286fca11b0138b84889b4d696f056c99b7778be6049e9bda24fc6c929f108c"
R24_041_SHA = "e21ee29c25e11c905db4dc6b70cea95cbe66dd1cb8a3d37c048d357fb1375df1"
SUP4_SHA = "47d4f47b9f873c14dd5d49a2a47813c8b5fac8efd71fd15bc1da6cc3e74d9b6d"
PROVENANCE_KEYS = ["orion", "computed from Black Diamond values and flows", "computed from custodian holdings"]
OPT_HASH_041 = "6816ef9295d214212be6ccb9ebf386a07cca38e1a4f3a5e56eac3f6c1385fce8"
CLAIM_VALUES = ["measured", "inferred"]
OPT_NAMES = p140.OPT_NAMES + ["market_value_eod_claim"]
CENSUS_TOKENS = ["measured", "inferred", "market_value_eod_claim"]
LONG_DIGITS = re.compile(r"\d{8,}")
Fail, need, nes, sha, schema_hash, load_json, git = p140.Fail, p140.need, p140.nes, p140.sha, p140.schema_hash, p140.load_json, p140.git
is_int = p140.is_int


def own_commits(root):
    base = git(root, "log", "--diff-filter=A", "--format=%H", "--", ORDER_REL).split()
    need(base, "the order's first commit is not in this history")
    out = git(root, "log", "--reverse", "--format=%H", "--author=" + AUTHOR, base[-1] + "..HEAD").split()
    need(out, "no commit by %s since the order was issued" % AUTHOR)
    return out, base[-1]


# ------------------------------------------------------------------------------------------------ the pure clauses
def check_rule24(r):
    need(sha({k: v for k, v in r.items() if k != "v042"}) == R24_041_SHA, "the earlier rule24_record keys (through v041) changed")
    v = r.get("v042")
    need(isinstance(v, dict) and set(v) == {"i_mece_over_a_declared_domain", "ii_same_grain", "iii_intent_coherence", "iv_state_coherence", "token_census", "token_census_finding"},
         "rule24_record.v042 must hold exactly the four postulates, token_census and token_census_finding")
    m = v["i_mece_over_a_declared_domain"]
    need(isinstance(m, dict) and set(m) == {"market_value_eod_claim", "return_basis"}, "v042.i_mece must hold exactly market_value_eod_claim and return_basis")
    rb = m["return_basis"]
    need(nes(rb) and len(rb) >= 120 and all(x in rb for x in ("VENDOR_REPORTED", "TWR", "NOT_MEASURABLE", "subtraction")), "v042.i_mece.return_basis must show the removal of VENDOR_REPORTED by subtraction from 0.4.1's domain, naming TWR and NOT_MEASURABLE")
    t = m["market_value_eod_claim"]
    need(nes(t) and len(t) >= 120 and all(x in t for x in CLAIM_VALUES) and "denominator" in t, "v042.i_mece.market_value_eod_claim must name both values, print its denominator (the PRESENT Orion rows) and be a real record (120+ characters)")
    for k, words in (("ii_same_grain", ("ACCOUNT-DAY", "market_value_eod")), ("iii_intent_coherence", ("market_value_eod_claim", "flow_claim", "return_basis", "provenance", "source")), ("iv_state_coherence", ("measured", "inferred", "VENDOR_REPORTED"))):
        need(nes(v[k]) and len(v[k]) >= 120 and all(w in v[k] for w in words), "v042.%s must be a real record naming %s" % (k, list(words)))
    c = v["token_census"]
    need(isinstance(c, dict) and set(c) == {"commit", "pathspecs", "denominator_files", "claim", "tokens"}, "token_census keys")
    need(p140.HEX40.match(str(c["commit"])) and c["pathspecs"] == p140.CENSUS_PATHSPECS and is_int(c["denominator_files"]) and c["denominator_files"] > 0 and c["claim"] == "measured", "token_census: a full commit, the three pathspecs, a positive denominator, claim measured")
    tk = c["tokens"]
    need(isinstance(tk, dict) and sorted(tk) == sorted(CENSUS_TOKENS), "token_census.tokens must hold exactly %s" % CENSUS_TOKENS)
    for k, x in tk.items():
        need(isinstance(x, dict) and set(x) == {"files", "hits", "reading"} and is_int(x["files"]) and is_int(x["hits"]) and x["files"] >= 0 and x["hits"] >= x["files"] and nes(x["reading"]), "token_census.%s: files, hits, reading" % k)
    need(nes(v["token_census_finding"]) and len(v["token_census_finding"]) >= 80 and "claim vocabulary" in v["token_census_finding"], "token_census_finding must say what the census found and name the repo's claim vocabulary (measured and inferred are existing words)")
    return True


def check_contract(c):
    need(c.get("contract_version") == "0.4.2", "contract_version is not 0.4.2 (a patch bump)")
    need(sha(c["columns"]) == COLS_SHA and schema_hash(c["columns"]) == c["schema_hash"] == p140.BASE_HASH, "the 19 columns (all of them), their types or the schema_hash moved")
    e = c["enums"]
    need(e.get("market_value_eod_claim") == CLAIM_VALUES and sha({k: v for k, v in e.items() if k not in ("market_value_eod_claim", "return_basis")}) == ENUMS_NO_RB_SHA, "enums: market_value_eod_claim %s and every earlier enum but return_basis byte-identical" % CLAIM_VALUES)
    need(e.get("return_basis") == ["TWR", "NOT_MEASURABLE"], "return_basis must be [TWR, NOT_MEASURABLE]: VENDOR_REPORTED leaves it (the CTO's ruling, msg 8673)")
    oc = c.get("optional_columns")
    need(isinstance(oc, list) and [o.get("name") for o in oc] == OPT_NAMES, "optional_columns must be exactly %s in order" % OPT_NAMES)
    need(sha(oc[:5]) == OPT5_SHA, "the five earlier optional columns changed")
    x = oc[5]
    need(x.get("type") == "string" and x.get("nullable") is True and x.get("values") == CLAIM_VALUES and x.get("since_schema_version") == "1.4" and x.get("required_when") == {"source": "orion"}
         and x.get("required_unless_absent") is True and nes(x.get("meaning")), "market_value_eod_claim: string, nullable, values %s, since 1.4, required_when {source: orion}, required_unless_absent true, a meaning" % CLAIM_VALUES)
    rule = x.get("rule") or ""
    need(nes(rule) and "inferred" in rule and "measured" in rule and "reject" in rule.lower() and "ABSENT" in rule, "market_value_eod_claim.rule must say: required on a PRESENT Orion row, null on an ABSENT row, a consumer that needs a measured value rejects inferred in words")
    allc = c["columns"] + [{"name": "source", "type": "string"}, {"name": "flow_claim", "type": "string"}, {"name": "source_account_id", "type": "int64"}, {"name": "row_status", "type": "string"},
                           {"name": "reason_class", "type": "string"}, {"name": "market_value_eod_claim", "type": "string"}]
    need(c.get("schema_hash_with_optional") == schema_hash(allc), "schema_hash_with_optional is not the recomputed hash over the 19 columns plus the six optional columns")
    sup = c.get("supersedes")
    need(isinstance(sup, list) and len(sup) == 5 and sha(sup[:4]) == SUP4_SHA, "supersedes must keep its first four entries byte-identical and add one")
    need(sup[4].get("contract_version") == "0.4.1" and sup[4].get("schema_hash") == p140.BASE_HASH and sup[4].get("schema_hash_with_optional") == OPT_HASH_041 and sup[4].get("changes"), "supersedes[4] must be the 0.4.1 entry with both hashes and its changes")
    need(sha(c.get("served_day_rules")) == p140.SERVED_SHA, "served_day_rules changed")
    need("source_requires" not in c, "source_requires must be removed: Orion rows carry return_basis TWR and the provenance is read from source")
    pv = c.get("source_provenance")
    need(isinstance(pv, dict) and sorted(pv) == sorted(PROVENANCE_KEYS) and all(nes(v) for v in pv.values()), "source_provenance must map each of the three source values to words: %s" % PROVENANCE_KEYS)
    need("vendor" in pv["orion"].lower() and "computed" in pv["orion"].lower() and "Opal" not in pv["orion"], "source_provenance.orion must say vendor-computed")
    need("Opal" in pv[PROVENANCE_KEYS[1]] and "Opal" in pv[PROVENANCE_KEYS[2]], "the Black Diamond and holdings sources must say Opal-computed")
    sr = (c.get("source_rules") or {}).get("orion")
    need(isinstance(sr, dict) and set(sr) == {"flows", "business_date", "account_id", "return_basis"} and sha({k: sr[k] for k in ("flows", "business_date", "account_id")}) == SR3_SHA, "source_rules.orion keeps flows, business_date and account_id byte-identical and holds return_basis")
    need(nes(sr["return_basis"]) and "TWR" in sr["return_basis"] and "MEASURED" in sr["return_basis"] and "source" in sr["return_basis"] and "VENDOR_REPORTED" not in sr["return_basis"], "source_rules.orion.return_basis must say Orion rows carry TWR, provenance is read from source, and how MEASURED reads; it names no VENDOR_REPORTED")
    check_rule24(c.get("rule24_record") or {})
    return True


def row_problems(c, row):
    """The 0.4.1 reference validator plus the one new rule, driven ONLY by the contract's declarations."""
    out = list(p140.row_problems(c, row))
    if row.get("return_basis") not in c["enums"]["return_basis"]:
        out.append("return_basis outside its values")
    claim = row.get("market_value_eod_claim")
    o = next(o for o in c["optional_columns"] if o["name"] == "market_value_eod_claim")
    if claim is not None and claim not in o["values"]:
        out.append("market_value_eod_claim outside its values")
    if claim is not None and row.get("market_value_eod") is None:
        out.append("a market_value_eod_claim without a market value")
    return out


def base_row():
    r = copy.deepcopy(p140.base_row())
    r["row_status"] = "PRESENT"
    return r


def check_behaviour(c):
    def r(**kw):
        x = base_row()
        x.update(kw)
        return x
    orion = dict(source="orion", return_basis="TWR", external_flow=None, income_received=None, flow_claim="absent", source_account_id=7)
    absent_kw = dict(row_status="ABSENT", market_value_eod=None, external_flow=None, income_received=None, total_return_daily=None, return_basis="NOT_MEASURABLE", day_quality="NOT_MEASURABLE",
                     guard_state="GUARD_NOT_REACHED", source="orion", reason_class="NO_FEED_ROW")
    good = [("a 0.3.0 Black Diamond row (no claim)", r()), ("a Black Diamond row carrying a measured claim", r(market_value_eod_claim="measured")),
            ("an Orion PRESENT row, claim measured", r(market_value_eod_claim="measured", **orion)), ("an Orion PRESENT row, claim inferred", r(market_value_eod_claim="inferred", **orion)),
            ("an Orion ABSENT row (no value, no claim)", r(**absent_kw)), ("a null-row_status Orion row, claim inferred (a writer that predates row_status)", r(market_value_eod_claim="inferred", row_status=None, **orion))]
    bad = [("an Orion PRESENT row with no claim", r(**orion)), ("an Orion PRESENT row with a claim outside its values", r(market_value_eod_claim="guessed", **orion)),
           ("an ABSENT row carrying a claim (there is no value)", r(market_value_eod_claim="measured", **absent_kw)),
           ("a null-row_status Orion row with no claim", r(row_status=None, **orion)),
           ("an Orion PRESENT row labelled VENDOR_REPORTED (it left the enum)", r(market_value_eod_claim="inferred", **dict(orion, return_basis="VENDOR_REPORTED")))]
    for label, row in good:
        p = row_problems(c, row)
        need(not p, "%s must validate: %s" % (label, p))
    for label, row in bad:
        need(row_problems(c, row), "%s must be rejected" % label)
    return len(good), len(bad)


def check_census(root, c):
    cen = c["rule24_record"]["v042"]["token_census"]
    commit = cen["commit"]
    need(subprocess.run(["git", "-C", str(root), "merge-base", "--is-ancestor", commit, "HEAD"], capture_output=True).returncode == 0, "census commit %s is not an ancestor of HEAD" % commit[:10])
    tree = git(root, "ls-tree", "-r", "--name-only", commit, "--", *p140.CENSUS_PATHSPECS).split("\n")
    n = len([x for x in tree if x])
    need(n == cen["denominator_files"], "census denominator: %d files at %s, the record says %d" % (n, commit[:10], cen["denominator_files"]))
    for tok, x in cen["tokens"].items():
        files, hits = p140.census_recount(root, commit, tok)
        need((files, hits) == (x["files"], x["hits"]), "census %s: recount files %d hits %d, the record says files %d hits %d" % (tok, files, hits, x["files"], x["hits"]))
    return len(cen["tokens"]), n


def check_grant(changed):
    bad = [f for f in changed if f not in GRANT_FILES and not f.startswith(GRANT_PREFIXES)]
    need(not bad, "the worker's commits touch files outside its grant: %s" % bad[:3])
    need(CONTRACT_REL in changed and TEST_REL in changed, "the contract and its test must both change")
    return True


def check_facts(rec, c):
    exp = {"contract_version", "schema_hash", "hash_with_optional", "optional_columns", "enum", "census_commit", "words"}
    need(isinstance(rec, dict) and set(rec) == exp, "record keys differ: %s" % (sorted(set(rec) ^ exp) if isinstance(rec, dict) else "?"))
    need(rec["contract_version"] == "0.4.2" and rec["schema_hash"] == c["schema_hash"] and rec["hash_with_optional"] == c["schema_hash_with_optional"], "version or hashes differ from the contract")
    need(rec["optional_columns"] == OPT_NAMES and rec["enum"] == {"market_value_eod_claim": CLAIM_VALUES}, "optional_columns or enum")
    need(rec["census_commit"] == c["rule24_record"]["v042"]["token_census"]["commit"], "census_commit differs from the contract's")
    need(nes(rec["words"]) and 80 <= len(rec["words"]) <= 1800 and not LONG_DIGITS.findall(rec["words"]), "words must be one paragraph of 80 to 1800 characters with no long digit run")
    return True


def run(root, cid):
    root = Path(root)
    c = load_json(root, CONTRACT_REL)
    if cid == "DB142-1-AC1":
        check_contract(c)
        cs, base = own_commits(root)
        changed = set()
        for cm in cs:
            changed |= set(git(root, "show", "--name-only", "--format=", cm).split())
        check_grant(changed)
        for rel in (TEST040_REL, TEST041_REL):
            stat = git(root, "diff", "--numstat", base, "HEAD", "--", rel).split()
            edited = (int(stat[0]) + int(stat[1])) if len(stat) >= 2 else 0
            bound = MAX_041_TEST_LINES if rel == TEST041_REL else MAX_EARLIER_TEST_LINES
            need(edited <= bound, "%s may change by at most %d lines, not %d" % (rel.rsplit("/", 1)[-1], bound, edited))
        print("OK: contract 0.4.2: the 19 columns, schema_hash, every enum and the five earlier optional columns unmoved; one new optional column market_value_eod_claim (measured | inferred) required on a PRESENT Orion row, hash %s; supersedes 0.4.1; the rule-24 record; %d files changed, all in the grant" %
              (c["schema_hash_with_optional"][:12], len(changed)))
        return True
    if cid == "DB142-1-AC2":
        check_contract(c)
        g, b = check_behaviour(c)
        nt, nf = check_census(root, c)
        print("OK: behaviour: a validator driven only by the contract accepts %d rows and rejects %d; the token census recounts %d tokens over %d files at %s" % (g, b, nt, nf, c["rule24_record"]["v042"]["token_census"]["commit"][:10]))
        return True
    if cid == "DB142-1-AC3":
        need((root / TEST_REL).is_file(), "no %s" % TEST_REL)
        n_new = p140.run_pytest(root, [TEST_REL])
        need(n_new >= 8, "the new test file holds %d passing tests, at least 8 are owed" % n_new)
        n_old = p140.run_pytest(root, EARLIER_TESTS)
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
    cols = [{"name": n, "type": "string", "nullable": base_row()[n] is None} for n in base_row() if n not in ("source", "flow_claim", "source_account_id", "row_status", "reason_class", "market_value_eod_claim")]
    for col in cols:
        if col["name"] in ("source", "total_return_daily"):
            col["nullable"] = True
        if col["name"] == "account_id":
            col["nullable_when"] = {"reason_class": "UNMAPPED_ACCOUNT"}
        if col["name"] == "market_value_eod":
            col["nullable_when_absent"] = True
        if col["name"] in p140.FLOW:
            col["nullable_when"] = dict(p137c.NULLABLE_WHEN)
            col["nullable_when_absent"] = True
    c = {"columns": cols, "enums": {"row_status": p140.ROW_STATUS, "reason_class": p140.REASONS, "return_basis": ["TWR", "NOT_MEASURABLE"], "market_value_eod_claim": CLAIM_VALUES},
         "optional_columns": [{"name": "source"}, {"name": "flow_claim", "values": ["absent"]}, {"name": "source_account_id", "required_when": {"reason_class": "UNMAPPED_ACCOUNT"}}, {"name": "row_status"},
                              {"name": "reason_class"}, {"name": "market_value_eod_claim", "values": CLAIM_VALUES, "required_when": {"source": "orion"}, "required_unless_absent": True}]}
    g, b = check_behaviour(c)
    assert (g, b) == (6, 5), (g, b)
    noreq = copy.deepcopy(c)
    noreq["optional_columns"][5].pop("required_when")
    red(lambda: check_behaviour(noreq), "no required_when: an Orion row with no claim validates")
    nounless = copy.deepcopy(c)
    nounless["optional_columns"][5].pop("required_unless_absent")
    red(lambda: check_behaviour(nounless), "no required_unless_absent: an ABSENT Orion row demands a claim")
    novals = copy.deepcopy(c)
    novals["optional_columns"][5]["values"] = ["measured", "inferred", "guessed"]
    red(lambda: check_behaviour(novals), "a widened enum accepts 'guessed'")
    assert check_grant({CONTRACT_REL, TEST_REL, TEST040_REL, TEST041_REL, D + "0.9.0_WK_IRPT_DASHBD~223/x.json"})
    red(lambda: check_grant({CONTRACT_REL, TEST_REL, "lib/x.py"}), "outside grant")
    red(lambda: check_grant({CONTRACT_REL}), "no test")
    red(lambda: check_rule24({"x": 1}), "earlier rule24 keys changed")
    rec = {"contract_version": "0.4.2", "schema_hash": "a" * 64, "hash_with_optional": "b" * 64, "optional_columns": list(OPT_NAMES), "enum": {"market_value_eod_claim": CLAIM_VALUES}, "census_commit": "c" * 40, "words": "w" * 100}
    cc = {"schema_hash": "a" * 64, "schema_hash_with_optional": "b" * 64, "rule24_record": {"v042": {"token_census": {"commit": "c" * 40}}}}
    assert check_facts(rec, cc)
    arms = (("version", lambda x: x.update(contract_version="0.4.1")), ("hash", lambda x: x.update(schema_hash="d" * 64)), ("optional hash", lambda x: x.update(hash_with_optional="d" * 64)),
            ("columns", lambda x: x.update(optional_columns=["source"])), ("enum", lambda x: x.update(enum={})), ("commit", lambda x: x.update(census_commit="e" * 40)),
            ("words", lambda x: x.update(words="short")), ("extra", lambda x: x.update(z=1)), ("digits", lambda x: x.update(words="w" * 100 + " 123456789")))
    for label, fn in arms:
        r2 = dict(rec)
        fn(r2)
        red(lambda: check_facts(r2, cc), label)
    print("selftest: behaviour (3 red arms, 6 good and 5 bad rows), grant (2), rule24 (1) and facts (%d red arms) clauses behave" % len(arms))
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
