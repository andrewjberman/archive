"""IRPT_DASHBD round 140, workstream B-49F + contract (issuer 2.0.0_SA_COO~D2, the contract's owner) -- DB-b-273, account_return_daily CONTRACT 0.4.1
(CTO ROUND ANALYSIS B-49F rounds 133-137 @93b8070c65 item 1, and B-IN round 118 ADDENDUM 6 @2a241c37da item 3: terms 2 and 3 of 0.4.0 were not expressible): a row-status column (PRESENT | ABSENT) and a
reason_class enum of eight values, an account_id nullable ONLY when the reason is UNMAPPED_ACCOUNT (then source_account_id is required), Orion rows marked VENDOR_REPORTED in return_basis, the market value
and the flows nullable on an ABSENT row, the rule-24 record and a word-boundary token census. The 19 columns, their types and schema_hash do not move; every 0.3.0 and 0.4.0 writer still validates.
LOCAL: one JSON standard, one new test file, one bounded edit of the 0.4.0 test.

  DB-b-273 (~221)   org/standards/IRPT_DASHBD_ACCOUNT_RETURN_DAILY_CONTRACT.json (0.4.1) + tests/test_account_return_contract_041.py + a bounded edit of test_account_return_contract_040.py + a facts record
                    DB140-1-AC1 (the contract's declarations, pure, and the grant),
                    DB140-1-AC2 (BEHAVIOUR: a reference validator driven ONLY by the contract's declarations accepts the 0.3.0 / 0.4.0 / ABSENT / UNMAPPED rows and rejects the bad ones; the token census recount),
                    DB140-1-AC3 (the worker's tests pass beside the earlier contract-reading tests; the facts record equals the contract)

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
_spec = importlib.util.spec_from_file_location("p137c", str(HERE.parent / "r137" / "p137_contract040.py"))
p137c = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(p137c)

D = "org/missions/D9/IRPT/IRPT_DASHBD/deliverables/"
CONTRACT_REL = p137c.CONTRACT_REL
TEST_REL = "data/assets/scripts/gold/irpt_reporting/tests/test_account_return_contract_041.py"
TEST040_REL = p137c.TEST_REL
EARLIER_TESTS = (p137c.EARLIER_TESTS[0], p137c.EARLIER_TESTS[1], TEST040_REL)
REC_REL = D + "0.9.0_WK_IRPT_DASHBD~221/RD_CONTRACT_041_FACTS_R140.json"
ORDER_REL = "org/missions/D9/IRPT/IRPT_DASHBD/task-orders/IRPT_DASHBD.TO-DB-b-273.account-return-contract-041-row-status-reason-class-and-vendor-reported.md"
AUTHOR = "0.9.0_WK_IRPT_DASHBD~221"
GRANT_FILES = {CONTRACT_REL, TEST_REL, TEST040_REL}
MAX_040_TEST_LINES = 14
GRANT_PREFIXES = (D + "0.9.0_WK_IRPT_DASHBD~221/", "org/missions/D9/IRPT/IRPT_DASHBD/surprise-channel/investigations/", "org/missions/D9/IRPT/IRPT_DASHBD/task-orders/")
FLOW = ("external_flow", "income_received")
CHANGED_COLS = ("account_id", "market_value_eod") + FLOW
BASE_HASH = p137c.BASE_HASH
OPT_HASH_040 = "74fdee3def647fd5c33ab9c07aa14106cbe66dbfe67a8e8608b68278db194154"
OTHER15_SHA = "146f3e0ea187c048416dd6f5236355846b1206bdbf5a17cc612bb2b9e5d534cc"
SOURCE_SHA, CLAIM_SHA = p137c.SOURCE_SHA, "7e76c42e0f065ecba28ce6b9654f0bb23f5c80eb84fd47c72ec9ccd40f2c1827"
SERVED_SHA = p137c.SERVED_SHA
ENUMS_OTHER_SHA = "d0060011b9113b56bd63fbb685b32a5726b032f1cd826c7e94a464953132948f"
R24_OLD_SHA = "b2f6e859fbefb8af0cf476ef4eef0e6e84d871fe7eb14414b02e26065fde8e90"
SUP_OLD_SHA = "08888cbc33115d638f88a91f3e0885bed007211ddc813d256a25e5140e861b91"
ROW_STATUS = ["PRESENT", "ABSENT"]
REASONS = ["NO_GROUP", "GROUP_NO_SERIES", "NO_START_DATE_AT_SOURCE", "SERIES_ENDED_AT_SOURCE", "UNMAPPED_ACCOUNT", "NO_FEED_ROW", "INCOMPLETE_WINDOW", "NO_EOD_VALUE"]
RETURN_BASIS = ["TWR", "NOT_MEASURABLE", "VENDOR_REPORTED"]
OPT_NAMES = ["source", "flow_claim", "source_account_id", "row_status", "reason_class"]
CENSUS_TOKENS = ["PRESENT", "ABSENT"] + REASONS + ["VENDOR_REPORTED", "row_status", "reason_class"]
CENSUS_PATHSPECS = ["data/assets/scripts/gold/irpt_reporting", "org/standards", "infra/aws/lambda/investor-reporting"]
LONG_DIGITS = re.compile(r"\d{8,}")
HEX40 = re.compile(r"[0-9a-f]{40}$")
Fail, need, nes, sha, schema_hash, load_json, git = p137c.Fail, p137c.need, p137c.nes, p137c.sha, p137c.schema_hash, p137c.load_json, p137c.git
R24_OLD_KEYS = ("i_mece_over_a_declared_domain", "ii_same_grain", "iii_intent_coherence", "iv_state_coherence", "token_census", "token_census_method", "token_census_finding", "member_evidence")


def is_int(x):
    return isinstance(x, int) and not isinstance(x, bool)


def own_commits(root):
    base = git(root, "log", "--diff-filter=A", "--format=%H", "--", ORDER_REL).split()
    need(base, "the order's first commit is not in this history")
    out = git(root, "log", "--reverse", "--format=%H", "--author=" + AUTHOR, base[-1] + "..HEAD").split()
    need(out, "no commit by %s since the order was issued" % AUTHOR)
    return out, base[-1]


# ------------------------------------------------------------------------------------------------ the pure clauses
def check_rule24(r):
    need(sha({k: r.get(k) for k in R24_OLD_KEYS}) == R24_OLD_SHA, "the earlier rule24_record keys changed")
    v = r.get("v041")
    need(isinstance(v, dict) and set(v) == {"i_mece_over_a_declared_domain", "ii_same_grain", "iii_intent_coherence", "iv_state_coherence", "token_census", "token_census_finding"},
         "rule24_record.v041 must hold exactly the four postulates, token_census and token_census_finding")
    m = v["i_mece_over_a_declared_domain"]
    need(isinstance(m, dict) and set(m) == {"row_status", "reason_class", "return_basis"}, "v041.i_mece must hold row_status, reason_class and return_basis")
    for col, vals in (("row_status", ROW_STATUS), ("reason_class", REASONS), ("return_basis", ["VENDOR_REPORTED"])):
        t = m[col]
        need(nes(t) and len(t) >= 120 and all(x in t for x in vals), "v041.i_mece.%s must name every value %s and be a real record (120+ characters)" % (col, vals))
    need("denominator" in m["reason_class"] and "precedence" in m["reason_class"].lower(), "v041.i_mece.reason_class must print its denominator and its precedence (by subtraction)")
    for k, words in (("ii_same_grain", ("ACCOUNT-DAY", "row_status")), ("iii_intent_coherence", ("return_method", "return_basis", "VENDOR_REPORTED")), ("iv_state_coherence", ("MEASURED", "VENDOR_REPORTED", "GUARD_NOT_REACHED"))):
        need(nes(v[k]) and len(v[k]) >= 120 and all(w in v[k] for w in words), "v041.%s must be a real record naming %s" % (k, list(words)))
    c = v["token_census"]
    need(isinstance(c, dict) and set(c) == {"commit", "pathspecs", "denominator_files", "claim", "tokens"}, "token_census keys")
    need(HEX40.match(str(c["commit"])) and c["pathspecs"] == CENSUS_PATHSPECS and is_int(c["denominator_files"]) and c["denominator_files"] > 0 and c["claim"] == "measured", "token_census: a full commit, the three pathspecs, a positive denominator, claim measured")
    t = c["tokens"]
    need(isinstance(t, dict) and sorted(t) == sorted(CENSUS_TOKENS), "token_census.tokens must hold exactly %s" % CENSUS_TOKENS)
    for k, x in t.items():
        need(isinstance(x, dict) and set(x) == {"files", "hits", "reading"} and is_int(x["files"]) and is_int(x["hits"]) and x["files"] >= 0 and x["hits"] >= x["files"] and nes(x["reading"]), "token_census.%s: files, hits, reading" % k)
    need(nes(v["token_census_finding"]) and len(v["token_census_finding"]) >= 80, "token_census_finding must say what the census found")
    return True


def check_contract(c):
    need(c.get("contract_version") == "0.4.1", "contract_version is not 0.4.1 (a patch bump)")
    cols = c["columns"]
    need(len(cols) == 19 and schema_hash(cols) == c["schema_hash"] == BASE_HASH, "the 19 columns, their types or the schema_hash moved")
    need(sha([x for x in cols if x["name"] not in CHANGED_COLS]) == OTHER15_SHA, "one of the 15 unchanged columns changed")
    byname = {x["name"]: x for x in cols}
    for n in CHANGED_COLS:
        x = byname[n]
        need(x.get("type") == ("string" if n == "account_id" else "double") and x.get("nullable") is False and nes(x.get("meaning")), "%s must keep its type and nullable false (nullability is conditional)" % n)
    need(byname["account_id"].get("nullable_when") == {"reason_class": "UNMAPPED_ACCOUNT"} and "nullable_when_absent" not in byname["account_id"], "account_id.nullable_when must equal {reason_class: UNMAPPED_ACCOUNT} and nothing else")
    need(byname["market_value_eod"].get("nullable_when_absent") is True and "nullable_when" not in byname["market_value_eod"], "market_value_eod must be nullable only on an ABSENT row (nullable_when_absent true)")
    for n in FLOW:
        need(byname[n].get("nullable_when") == p137c.NULLABLE_WHEN and byname[n].get("nullable_when_absent") is True, "%s keeps the 0.4.0 nullable_when and gains nullable_when_absent true" % n)
    e = c["enums"]
    need(sha({k: v for k, v in e.items() if k not in ("return_basis", "row_status", "reason_class")}) == ENUMS_OTHER_SHA, "an earlier enum changed")
    need(e.get("return_basis") == RETURN_BASIS and e.get("row_status") == ROW_STATUS and e.get("reason_class") == REASONS, "enums: return_basis %s, row_status %s, reason_class %s" % (RETURN_BASIS, ROW_STATUS, REASONS))
    oc = c.get("optional_columns")
    need(isinstance(oc, list) and [o.get("name") for o in oc] == OPT_NAMES, "optional_columns must be exactly %s in order" % OPT_NAMES)
    need(sha(oc[0]) == SOURCE_SHA and sha(oc[1]) == CLAIM_SHA, "the optional columns source and flow_claim changed")
    sa, rs, rc = oc[2], oc[3], oc[4]
    need(sa.get("type") == "int64" and sa.get("nullable") is True and sa.get("required_when") == {"reason_class": "UNMAPPED_ACCOUNT"} and sa.get("since_schema_version") == "1.2" and "Orion" in sa.get("meaning", "") and nes(sa.get("rule")),
         "source_account_id: int64, nullable, required_when {reason_class: UNMAPPED_ACCOUNT}, since 1.2, a meaning naming Orion, a rule")
    need(rs.get("type") == "string" and rs.get("nullable") is True and rs.get("values") == ROW_STATUS and rs.get("since_schema_version") == "1.3" and nes(rs.get("meaning"))
         and "PRESENT" in rs.get("rule", "") and "predates" in rs["rule"], "row_status: string, nullable, values PRESENT/ABSENT, since 1.3, a rule saying a null means a writer that predates the column and reads PRESENT")
    need(rc.get("type") == "string" and rc.get("nullable") is True and rc.get("values") == REASONS and rc.get("since_schema_version") == "1.3" and nes(rc.get("meaning"))
         and "ABSENT" in rc.get("rule", "") and "null" in rc["rule"].lower(), "reason_class: string, nullable, the eight values, since 1.3, a rule saying it is required when the row is ABSENT and null otherwise")
    allcols = cols + [{"name": "source", "type": "string"}, {"name": "flow_claim", "type": "string"}, {"name": "source_account_id", "type": "int64"}, {"name": "row_status", "type": "string"}, {"name": "reason_class", "type": "string"}]
    need(c.get("schema_hash_with_optional") == schema_hash(allcols), "schema_hash_with_optional is not the recomputed hash over the 19 columns plus the five optional columns")
    sup = c.get("supersedes")
    need(isinstance(sup, list) and len(sup) == 4 and sha(sup[:3]) == SUP_OLD_SHA, "supersedes must keep its first three entries (0.1.0, 0.2.0, 0.3.0) byte-identical and add one")
    need(sup[3].get("contract_version") == "0.4.0" and sup[3].get("schema_hash") == BASE_HASH and sup[3].get("schema_hash_with_optional") == OPT_HASH_040 and sup[3].get("changes"), "supersedes[3] must be the 0.4.0 entry with both hashes and its changes")
    need(sha(c.get("served_day_rules")) == SERVED_SHA, "served_day_rules changed")
    need(c.get("source_requires") == {"orion": {"return_basis": "VENDOR_REPORTED"}}, "source_requires must equal {orion: {return_basis: VENDOR_REPORTED}}")
    sr = (c.get("source_rules") or {}).get("orion")
    need(isinstance(sr, dict) and set(sr) == {"flows", "business_date", "account_id", "return_basis"} and all(nes(v) for v in sr.values()), "source_rules.orion must hold exactly flows, business_date, account_id and return_basis, in words")
    need("account_dim" in sr["account_id"] and "UNMAPPED_ACCOUNT" in sr["account_id"] and "source_account_id" in sr["account_id"] and "not a member" in sr["account_id"], "source_rules.orion.account_id must name account_dim's own key form, source_account_id, UNMAPPED_ACCOUNT and 'not a member'")
    need("VENDOR_REPORTED" in sr["return_basis"] and "MEASURED" in sr["return_basis"], "source_rules.orion.return_basis must name VENDOR_REPORTED and say how MEASURED is read with it")
    check_rule24(c.get("rule24_record") or {})
    return True


def row_problems(c, row):
    """A reference validator driven ONLY by the contract's declarations. Returns the list of problems (empty = valid)."""
    out = []
    enums = c["enums"]
    status = row.get("row_status")
    reason = row.get("reason_class")
    if status is not None and status not in enums["row_status"]:
        out.append("row_status outside its values")
    if reason is not None and reason not in enums["reason_class"]:
        out.append("reason_class outside its values")
    if status == "ABSENT" and reason is None:
        out.append("an ABSENT row needs a reason_class")
    if status != "ABSENT" and reason is not None:
        out.append("a PRESENT row carries no reason_class")
    absent = status == "ABSENT"
    for col in c["columns"]:
        if row.get(col["name"]) is None:
            cond = col.get("nullable_when")
            ok = col.get("nullable") is True or (isinstance(cond, dict) and all(row.get(k) == val for k, val in cond.items())) or (col.get("nullable_when_absent") is True and absent)
            if not ok:
                out.append("%s is null" % col["name"])
    for o in c["optional_columns"]:
        req = o.get("required_when")
        if isinstance(req, dict) and all(row.get(k) == val for k, val in req.items()) and row.get(o["name"]) is None:
            out.append("%s is required" % o["name"])
    claim = row.get("flow_claim")
    if not absent:
        nulls = [n for n in FLOW if row.get(n) is None]
        if claim is not None and not nulls:
            out.append("flow_claim without a null flow")
        if claim is not None and claim not in next(o for o in c["optional_columns"] if o["name"] == "flow_claim")["values"]:
            out.append("flow_claim outside its values")
        for src, req in (c.get("source_requires") or {}).items():
            if row.get("source") == src:
                for k, v in req.items():
                    if row.get(k) != v:
                        out.append("a %s row must carry %s %s" % (src, k, v))
    return out


def base_row():
    r = copy.deepcopy(p137c.base_row())
    r["return_basis"] = "TWR"
    return r


def check_behaviour(c):
    def r(**kw):
        x = base_row()
        x.update(kw)
        return x
    absent_kw = dict(row_status="ABSENT", market_value_eod=None, external_flow=None, income_received=None, total_return_daily=None, return_basis="NOT_MEASURABLE", day_quality="NOT_MEASURABLE",
                     guard_state="GUARD_NOT_REACHED", source="orion")
    orion = dict(source="orion", return_basis="VENDOR_REPORTED", external_flow=None, income_received=None, flow_claim="absent", row_status="PRESENT", source_account_id=7)
    good = [("a 0.3.0 Black Diamond row (no new column)", r()), ("a 0.4.0 Orion row (claim, no new column but VENDOR_REPORTED)", r(source="orion", external_flow=None, income_received=None, flow_claim="absent", source_account_id=7, return_basis="VENDOR_REPORTED")),
            ("an Orion PRESENT row with the status and VENDOR_REPORTED", r(**orion)),
            ("an Orion PRESENT row with flows set", r(source="orion", return_basis="VENDOR_REPORTED", row_status="PRESENT")),
            ("an UNMAPPED_ACCOUNT ABSENT row", r(account_id=None, source_account_id=7, reason_class="UNMAPPED_ACCOUNT", **absent_kw))]
    for rc in REASONS:
        if rc != "UNMAPPED_ACCOUNT":
            good.append(("an ABSENT row, reason %s" % rc, r(reason_class=rc, **absent_kw)))
    bad = [("an ABSENT row with no reason_class", r(**absent_kw)),
           ("a PRESENT row carrying a reason_class", r(row_status="PRESENT", reason_class="NO_GROUP")),
           ("a reason_class outside the enum", r(reason_class="OTHER", **absent_kw)),
           ("a row_status outside the enum", r(row_status="MISSING")),
           ("a null account_id with a reason other than UNMAPPED_ACCOUNT", r(account_id=None, source_account_id=7, reason_class="NO_GROUP", **absent_kw)),
           ("a null account_id, UNMAPPED_ACCOUNT, no source_account_id", r(account_id=None, reason_class="UNMAPPED_ACCOUNT", **absent_kw)),
           ("a null account_id on a PRESENT row", r(account_id=None, source_account_id=7, row_status="PRESENT")),
           ("an Orion PRESENT row labelled TWR", r(source="orion", return_basis="TWR", row_status="PRESENT")),
           ("a PRESENT row with a null market value", r(market_value_eod=None, row_status="PRESENT")),
           ("an Orion PRESENT row with null flows and no claim", r(source="orion", return_basis="VENDOR_REPORTED", external_flow=None, income_received=None, row_status="PRESENT")),
           ("an ABSENT row with another null column (day_quality)", r(reason_class="NO_GROUP", day_quality=None, **{k: v for k, v in absent_kw.items() if k != "day_quality"}))]
    for label, row in good:
        p = row_problems(c, row)
        need(not p, "%s must validate: %s" % (label, p))
    for label, row in bad:
        need(row_problems(c, row), "%s must be rejected" % label)
    return len(good), len(bad)


def census_recount(root, commit, token):
    r = subprocess.run(["git", "-C", str(root), "grep", "-c", "-w", "-I", "-e", token, commit, "--"] + CENSUS_PATHSPECS, capture_output=True, text=True)
    need(r.returncode in (0, 1), "git grep failed for %s: %s" % (token, r.stderr.strip()[:160]))
    files = hits = 0
    for ln in r.stdout.splitlines():
        files += 1
        hits += int(ln.rsplit(":", 1)[1])
    return files, hits


def check_census(root, c):
    cen = c["rule24_record"]["v041"]["token_census"]
    commit = cen["commit"]
    need(subprocess.run(["git", "-C", str(root), "merge-base", "--is-ancestor", commit, "HEAD"], capture_output=True).returncode == 0, "census commit %s is not an ancestor of HEAD" % commit[:10])
    tree = git(root, "ls-tree", "-r", "--name-only", commit, "--", *CENSUS_PATHSPECS).split("\n")
    n = len([x for x in tree if x])
    need(n == cen["denominator_files"], "census denominator: %d files at %s, the record says %d" % (n, commit[:10], cen["denominator_files"]))
    for tok, x in cen["tokens"].items():
        files, hits = census_recount(root, commit, tok)
        need((files, hits) == (x["files"], x["hits"]), "census %s: recount files %d hits %d, the record says files %d hits %d" % (tok, files, hits, x["files"], x["hits"]))
    return len(cen["tokens"]), n


def check_grant(changed):
    bad = [f for f in changed if f not in GRANT_FILES and not f.startswith(GRANT_PREFIXES)]
    need(not bad, "the worker's commits touch files outside its grant: %s" % bad[:3])
    need(CONTRACT_REL in changed and TEST_REL in changed, "the contract and its test must both change")
    return True


def check_facts(rec, c):
    exp = {"contract_version", "schema_hash", "hash_with_optional", "optional_columns", "enums", "census_commit", "words"}
    need(isinstance(rec, dict) and set(rec) == exp, "record keys differ: %s" % (sorted(set(rec) ^ exp) if isinstance(rec, dict) else "?"))
    need(rec["contract_version"] == "0.4.1" and rec["schema_hash"] == c["schema_hash"] and rec["hash_with_optional"] == c["schema_hash_with_optional"], "version or hashes differ from the contract")
    need(rec["optional_columns"] == OPT_NAMES and rec["enums"] == {"row_status": ROW_STATUS, "reason_class": REASONS, "return_basis": RETURN_BASIS}, "optional_columns or enums")
    need(rec["census_commit"] == c["rule24_record"]["v041"]["token_census"]["commit"], "census_commit differs from the contract's")
    need(nes(rec["words"]) and 80 <= len(rec["words"]) <= 1800 and not [h for h in LONG_DIGITS.findall(rec["words"])], "words must be one paragraph of 80 to 1800 characters with no long digit run")
    return True


def run_pytest(root, files):
    r = subprocess.run([sys.executable, "-m", "pytest", "-q", "-p", "no:cacheprovider"] + list(files), cwd=str(root), capture_output=True, text=True, timeout=600)
    m = re.search(r"(\d+) passed", r.stdout)
    need(r.returncode == 0 and m is not None, "tests failed: %s" % r.stdout[-300:].replace("\n", " | "))
    return int(m.group(1))


def run(root, cid):
    root = Path(root)
    c = load_json(root, CONTRACT_REL)
    if cid == "DB140-1-AC1":
        check_contract(c)
        cs, base = own_commits(root)
        changed = set()
        for cm in cs:
            changed |= set(git(root, "show", "--name-only", "--format=", cm).split())
        check_grant(changed)
        stat = git(root, "diff", "--numstat", base, "HEAD", "--", TEST040_REL).split()
        edited = (int(stat[0]) + int(stat[1])) if len(stat) >= 2 else 0
        need(edited <= MAX_040_TEST_LINES, "the 0.4.0 test may change by at most %d lines, not %d" % (MAX_040_TEST_LINES, edited))
        print("OK: contract 0.4.1: the 19 columns and schema_hash unmoved, account_id/market value/flows conditionally nullable, five optional columns (hash %s), %d reason classes, supersedes 0.4.0 and 0.3.0, the rule-24 record; %d files changed, all in the grant" %
              (c["schema_hash_with_optional"][:12], len(REASONS), len(changed)))
        return True
    if cid == "DB140-1-AC2":
        check_contract(c)
        g, b = check_behaviour(c)
        nt, nf = check_census(root, c)
        print("OK: behaviour: a validator driven only by the contract accepts %d rows and rejects %d; the token census recounts %d tokens over %d files at %s" % (g, b, nt, nf, c["rule24_record"]["v041"]["token_census"]["commit"][:10]))
        return True
    if cid == "DB140-1-AC3":
        need((root / TEST_REL).is_file(), "no %s" % TEST_REL)
        n_new = run_pytest(root, [TEST_REL])
        need(n_new >= 12, "the new test file holds %d passing tests, at least 12 are owed" % n_new)
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
    # behaviour on a synthetic contract built around the real column list shape
    cols = []
    for n in [x for x in base_row() if x not in ("source", "flow_claim", "source_account_id", "row_status", "reason_class")]:
        d = {"name": n, "type": "string", "nullable": base_row()[n] is None}
        if n == "account_id":
            d["nullable_when"] = {"reason_class": "UNMAPPED_ACCOUNT"}
        if n == "market_value_eod":
            d["nullable_when_absent"] = True
        if n in FLOW:
            d["nullable_when"] = dict(p137c.NULLABLE_WHEN)
            d["nullable_when_absent"] = True
        cols.append(d)
    c = {"columns": cols, "enums": {"row_status": ROW_STATUS, "reason_class": REASONS, "return_basis": RETURN_BASIS},
         "optional_columns": [{"name": "source"}, {"name": "flow_claim", "values": ["absent"]}, {"name": "source_account_id", "required_when": {"reason_class": "UNMAPPED_ACCOUNT"}}, {"name": "row_status"}, {"name": "reason_class"}],
         "source_requires": {"orion": {"return_basis": "VENDOR_REPORTED"}}}
    for col in c["columns"]:
        if col["name"] in ("source",):
            col["nullable"] = True
    # total_return_daily, income_return etc. already null-tolerant in base; ABSENT rows set several nulls
    for col in c["columns"]:
        if col["name"] in ("total_return_daily",):
            col["nullable"] = True
    g, b = check_behaviour(c)
    assert g == 12 and b == 11, (g, b)
    broken = copy.deepcopy(c)
    broken["columns"][[x["name"] for x in broken["columns"]].index("account_id")].pop("nullable_when")
    red(lambda: check_behaviour(broken), "account_id never nullable: the UNMAPPED row cannot validate")
    nosrc = copy.deepcopy(c)
    nosrc.pop("source_requires")
    red(lambda: check_behaviour(nosrc), "no source_requires: the TWR-labelled Orion row validates")
    noreq = copy.deepcopy(c)
    noreq["optional_columns"][2].pop("required_when")
    red(lambda: check_behaviour(noreq), "no required_when: an UNMAPPED row without source_account_id validates")
    noabs = copy.deepcopy(c)
    noabs["columns"][[x["name"] for x in noabs["columns"]].index("market_value_eod")].pop("nullable_when_absent")
    red(lambda: check_behaviour(noabs), "no nullable_when_absent: the ABSENT row cannot validate")
    assert check_grant({CONTRACT_REL, TEST_REL, TEST040_REL, D + "0.9.0_WK_IRPT_DASHBD~221/x.json"})
    red(lambda: check_grant({CONTRACT_REL, TEST_REL, "lib/x.py"}), "outside grant")
    red(lambda: check_grant({CONTRACT_REL}), "no test")
    r24 = {k: None for k in R24_OLD_KEYS}
    red(lambda: check_rule24(r24), "old rule24 keys changed")
    rec = {"contract_version": "0.4.1", "schema_hash": "a" * 64, "hash_with_optional": "b" * 64, "optional_columns": list(OPT_NAMES),
           "enums": {"row_status": ROW_STATUS, "reason_class": REASONS, "return_basis": RETURN_BASIS}, "census_commit": "c" * 40, "words": "w" * 100}
    cc = {"schema_hash": "a" * 64, "schema_hash_with_optional": "b" * 64, "rule24_record": {"v041": {"token_census": {"commit": "c" * 40}}}}
    assert check_facts(rec, cc)
    arms = (("version", lambda x: x.update(contract_version="0.4.0")), ("hash", lambda x: x.update(schema_hash="d" * 64)), ("optional hash", lambda x: x.update(hash_with_optional="d" * 64)),
            ("columns", lambda x: x.update(optional_columns=["source"])), ("enums", lambda x: x.update(enums={})), ("commit", lambda x: x.update(census_commit="e" * 40)),
            ("words", lambda x: x.update(words="short")), ("extra", lambda x: x.update(z=1)), ("digits", lambda x: x.update(words="w" * 100 + " 123456789")))
    for label, fn in arms:
        r2 = dict(rec)
        fn(r2)
        red(lambda: check_facts(r2, cc), label)
    print("selftest: behaviour (4 red arms, 12 good and 11 bad rows), grant (2), rule24 (1) and facts (%d red arms) clauses behave" % len(arms))
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
