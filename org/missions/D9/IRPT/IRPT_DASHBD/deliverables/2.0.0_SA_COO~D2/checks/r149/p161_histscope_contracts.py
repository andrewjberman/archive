"""IRPT_DASHBD round 149, workstream PUB49F (issuer 2.0.0_SA_COO~D2, the contracts' sole writer) -- DB-b-293, the HISTORY-SCOPE CLAIM in both contracts (CTO ruling msg 9226, row D2-S113) and the series contract's
unreported-days rule widened to every firm (CTO ruling msg 9224):

  history_scope is DERIVED per account, never a constant: an account whose first value day equals the source floor is PARTIAL_HISTORY (it existed before our data starts), an account first seen after the floor is FULL;
  the derivation is an inference and says so: history_scope_claim = inferred, method "first value day vs source floor". The source table contract 0.4.5 -> 0.4.6 gains the conditional column
  history_scope_claim (outside optional_columns, both schema hashes unchanged); the series contract 0.3.2 -> 0.3.3 gains the optional pair history_scope_claim + history_scope_basis (const text), the rule
  history_scope_rule, and a widened unreported_days_rule (the pair is derived by the publisher from the gold partitions present, for every firm, an explicit [] when none are missing).
  The contract and its writers land in ONE drain (DB-b-292 now; the producer and publisher cells follow). LOCAL: two JSON standards, a test file and a few pinned lines in the earlier contract tests.

  DB-b-293 (~236)   org/standards/IRPT_DASHBD_ACCOUNT_RETURN_DAILY_CONTRACT.json (0.4.6) + org/standards/IRPT_DASHBD_SERIES_CONTRACT.json (0.3.3) + tests + a facts record
                    DB161-1-AC1 (each contract differs from its base ONLY in the allowed places),
                    DB161-1-AC2 (a reference rule driven only by the contracts' declarations accepts and refuses the right rows and series),
                    DB161-1-AC3 (the new tests, the earlier contract tests, the grant, the facts record)

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
NEW_TEST = TEST_DIR + "test_history_scope_claim_contracts.py"
AUTHOR = "0.9.0_WK_IRPT_DASHBD~236"
REC_REL = D + AUTHOR + "/RD_HISTSCOPE_CONTRACTS_FACTS_R149.json"
ORDER_REL = "org/missions/D9/IRPT/IRPT_DASHBD/task-orders/IRPT_DASHBD.TO-DB-b-293.history-scope-claim-contracts-046-033.md"
EARLIER = [TEST_DIR + "test_account_return_contract_04%d.py" % i for i in range(5)] + [TEST_DIR + "test_income_reason_rename.py", TEST_DIR + "test_series_contract_030.py", TEST_DIR + "test_series_contract_031.py"]
GRANT_FILES = {SRC_REL, SER_REL, NEW_TEST} | set(EARLIER)
GRANT_PREFIXES = (D + AUTHOR + "/", "org/missions/D9/IRPT/IRPT_DASHBD/surprise-channel/investigations/", "org/missions/D9/IRPT/IRPT_DASHBD/task-orders/")
METHOD = "first value day vs source floor"
CLAIM = "inferred"
SRC_ENTRY_KEYS = {"name", "type", "nullable", "meaning", "values", "method", "applies_to", "rule", "since_schema_version"}
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


def has_all(text, words):
    low = text.lower()
    missing = [w for w in words if w.lower() not in low]
    return missing


# ------------------------------------------------------------------------------------------------ the pure clauses
def check_source(base, c):
    need(base["contract_version"] == "0.4.5" and c.get("contract_version") == "0.4.6", "source contract: 0.4.5 -> 0.4.6")
    moved = sorted(k for k in set(base) | set(c) if k not in ("contract_version", "supersedes", "rule24_record", "conditional_columns") and base.get(k) != c.get(k))
    need(not moved, "source contract: sections changed beyond the allowed ones (columns, optional_columns, enums and both schema hashes stay byte-identical): %s" % moved)
    bc, nc = base["conditional_columns"], c["conditional_columns"]
    need(isinstance(nc, list) and len(nc) == len(bc) + 1 and nc[:len(bc)] == bc, "conditional_columns keeps every earlier entry byte-identical and appends ONE")
    n = nc[-1]
    need(set(n) == SRC_ENTRY_KEYS, "the new entry's keys differ: %s" % sorted(set(n) ^ SRC_ENTRY_KEYS))
    need(n["name"] == "history_scope_claim" and n["type"] == "string" and n["nullable"] is False and n["values"] == [CLAIM] and n["method"] == METHOD, "name, type, nullable, values or method of the new column")
    for k in ("meaning", "applies_to", "rule", "since_schema_version"):
        need(nes(n[k]), "conditional_columns[-1].%s must be words" % k)
    miss = has_all(n["rule"], ["history_scope", "PARTIAL_HISTORY", "FULL", "first value day", "source floor", "earliest balance partition", "inferred", "optional_columns", "never", "no claim"])
    need(not miss, "the rule must say (missing: %s): the derivation, that the floor is the earliest balance partition, that the column sits outside optional_columns, that a row without it makes no claim" % miss)
    miss = has_all(n["meaning"], ["history_scope", "inferred", "account"])
    need(not miss, "the meaning must say what the claim is about (missing: %s)" % miss)
    sb, sn = base["supersedes"], c["supersedes"]
    need(isinstance(sn, list) and len(sn) == len(sb) + 1 and sn[:len(sb)] == sb, "supersedes must keep every earlier entry byte-identical and append one")
    e = sn[-1]
    need(e.get("contract_version") == "0.4.5" and e.get("schema_hash") == base["schema_hash"] and e.get("schema_hash_with_optional") == base["schema_hash_with_optional"] and nes(e.get("changes")) and "history_scope_claim" in e["changes"],
         "the appended entry: 0.4.5, both unchanged hashes, a changes sentence naming history_scope_claim")
    r24b, r24n = base["rule24_record"], c["rule24_record"]
    need({k: x for k, x in r24n.items() if k != "v046"} == r24b and nes(r24n.get("v046")), "rule24_record keeps every key and adds v046")
    miss = has_all(r24n["v046"], ["history_scope_claim", "inferred", METHOD, "account", "no other state"])
    need(not miss, "v046 must say (missing: %s): the claim, its one value and no other state, the method, the account grain" % miss)
    return True


def check_series(base, c, base_sha):
    need(base["contract_version"] == "0.3.2" and c.get("contract_version") == "0.3.3", "series contract: 0.3.2 -> 0.3.3")
    moved = sorted(k for k in set(base) | set(c) if k not in ("contract_version", "lineage", "series", "unreported_days_rule", "history_scope_rule") and base.get(k) != c.get(k))
    need(not moved, "series contract: sections changed beyond the allowed ones: %s" % moved)
    need("history_scope_rule" in c and "history_scope_rule" not in base, "history_scope_rule must be NEW")
    lb, ln = base["lineage"], c["lineage"]
    need(isinstance(ln, list) and len(ln) == len(lb) + 1 and ln[:len(lb)] == lb and ln[-1].get("contract_version") == "0.3.2" and ln[-1].get("sha256") == base_sha and nes(ln[-1].get("note")) and len(ln[-1]) == 3,
         "lineage keeps every entry and appends {0.3.2, sha256 of the 0.3.2 bytes, a note}")
    sb, sn = base["series"], c["series"]
    for k in sb:
        if k not in ("fields", "optional"):
            need(sb[k] == sn[k], "series.%s changed" % k)
    need(sn["optional"] == sb["optional"] + ["history_scope_claim", "history_scope_basis"], "series.optional keeps its entries and appends history_scope_claim then history_scope_basis")
    fb, fn = sb["fields"], sn["fields"]
    need(set(fn) == set(fb) | {"history_scope_claim", "history_scope_basis"}, "series.fields gains exactly the two new fields")
    for k in fb:
        if k not in ("history_scope", "unreported_trading_days"):
            need(fb[k] == fn[k], "series.fields.%s changed" % k)
    h, u = fn["history_scope"], fn["unreported_trading_days"]
    need(set(h) == set(fb["history_scope"]) and h["kind"] == fb["history_scope"]["kind"] and h["source"] == fb["history_scope"]["source"], "history_scope keeps its keys, kind and source")
    miss = has_all(h["sentence"], ["derived", "account", "PARTIAL_HISTORY", "FULL", "source floor", "never null"])
    need(not miss, "history_scope.sentence must say (missing: %s)" % miss)
    need(set(u) == set(fb["unreported_trading_days"]) and u["kind"] == fb["unreported_trading_days"]["kind"] and u["sentence"] == fb["unreported_trading_days"]["sentence"], "unreported_trading_days keeps its keys, kind and sentence; only `source` may change")
    need(nes(u["source"]) and "gold partitions" in u["source"] and "report-build" in u["source"], "unreported_trading_days.source must name the publisher's derivation from the gold partitions and keep the report-build equality")
    cl, ba = fn["history_scope_claim"], fn["history_scope_basis"]
    need(cl.get("kind") == "scalar string" and cl.get("fixed_value") == CLAIM and nes(cl.get("source")) and nes(cl.get("sentence")) and "history_scope_claim" in cl["source"] and len(cl) == 4,
         "history_scope_claim: kind scalar string, fixed_value inferred, a source naming the source table's column, a sentence")
    need(ba.get("kind") == "scalar string" and ba.get("fixed_value") == METHOD and ba.get("const") is True and nes(ba.get("rule24_note")) and nes(ba.get("sentence")) and ba.get("source") == "a fixed text" and len(ba) == 6,
         "history_scope_basis: a const fixed text %r with a rule24_note and a sentence" % METHOD)
    ub, un = base["unreported_days_rule"], c["unreported_days_rule"]
    need(set(ub) == set(un) and all(ub[k] == un[k] for k in ub if k != "present_when"), "unreported_days_rule: only `present_when` may change")
    pw = un["present_when"]
    miss = has_all(pw, ["every firm", "gold partitions", "[]"])
    need(not miss and "carries neither field" not in pw, "unreported_days_rule.present_when must say it is derived by the publisher from the gold partitions for every firm, [] when none are missing (missing: %s), and must drop the carries-neither clause" % miss)
    r = c["history_scope_rule"]
    need(set(r) == {"present_when", "pair", "value", "basis", "derivation", "absent_means"} and r["value"] == CLAIM and r["basis"] == METHOD, "history_scope_rule: keys, value inferred, basis %r" % METHOD)
    for k in ("present_when", "pair", "derivation", "absent_means"):
        need(nes(r[k]), "history_scope_rule.%s must be words" % k)
    miss = has_all(r["derivation"], ["PARTIAL_HISTORY", "FULL", "first_data_date", "source floor", "earliest"])
    need(not miss, "history_scope_rule.derivation must say (missing: %s)" % miss)
    miss = has_all(r["pair"], ["both", "neither", "lone"])
    need(not miss, "history_scope_rule.pair must say both fields or neither, a lone field invalid (missing: %s)" % miss)
    return True


# the reference rules, driven only by the contracts' declarations
def row_ok(src, row):
    """A source row against the history_scope_claim column's declaration."""
    col = next(x for x in src["conditional_columns"] if x["name"] == "history_scope_claim")
    if "history_scope_claim" not in row:
        return row.get("history_scope") in src["enums"]["history_scope"]
    if row["history_scope_claim"] is None and col["nullable"] is False:
        return False
    return row["history_scope_claim"] in col["values"] and row.get("history_scope") in src["enums"]["history_scope"]


def pair_ok(ser, doc):
    """A series document against the history_scope pair's declaration."""
    rule = ser["history_scope_rule"]
    fields = ser["series"]["fields"]
    has_c, has_b = "history_scope_claim" in doc, "history_scope_basis" in doc
    if has_c != has_b:
        return False
    if not has_c:
        return True
    return doc["history_scope_claim"] == fields["history_scope_claim"]["fixed_value"] == rule["value"] and doc["history_scope_basis"] == fields["history_scope_basis"]["fixed_value"] == rule["basis"]


def check_behaviour(src, ser):
    enum = src["enums"]["history_scope"]
    need(enum == ["FULL", "PARTIAL_HISTORY"], "the history_scope enum must stay FULL | PARTIAL_HISTORY")
    good_rows = [{"history_scope": "PARTIAL_HISTORY", "history_scope_claim": CLAIM}, {"history_scope": "FULL", "history_scope_claim": CLAIM}, {"history_scope": "PARTIAL_HISTORY"}]
    bad_rows = [{"history_scope": "FULL", "history_scope_claim": "measured"}, {"history_scope": "FULL", "history_scope_claim": None}, {"history_scope": "SOMETIMES", "history_scope_claim": CLAIM}, {"history_scope": None, "history_scope_claim": CLAIM}]
    for r in good_rows:
        need(row_ok(src, r), "a legal row was refused: %s" % r)
    for r in bad_rows:
        need(not row_ok(src, r), "an illegal row was accepted: %s" % r)
    good_docs = [{}, {"history_scope_claim": CLAIM, "history_scope_basis": METHOD}]
    bad_docs = [{"history_scope_claim": CLAIM}, {"history_scope_basis": METHOD}, {"history_scope_claim": "held", "history_scope_basis": METHOD}, {"history_scope_claim": CLAIM, "history_scope_basis": "free text"}]
    for d in good_docs:
        need(pair_ok(ser, d), "a legal series was refused: %s" % d)
    for d in bad_docs:
        need(not pair_ok(ser, d), "an illegal series was accepted: %s" % d)
    return True


def check_grant(changed):
    bad = [f for f in changed if f not in GRANT_FILES and not f.startswith(GRANT_PREFIXES)]
    need(not bad, "the worker's commits touch files outside its grant: %s" % bad[:3])
    need(SRC_REL in changed and SER_REL in changed and NEW_TEST in changed, "both contracts and the new test must change")
    return True


def check_facts(rec, src_sha, ser_sha, n_tests):
    exp = {"source_version", "series_version", "base_sha256", "hashes", "new_fields", "tests", "words"}
    need(isinstance(rec, dict) and set(rec) == exp, "record keys differ: %s" % (sorted(set(rec) ^ exp) if isinstance(rec, dict) else "?"))
    need(rec["source_version"] == "0.4.6" and rec["series_version"] == "0.3.3", "versions differ")
    need(rec["base_sha256"] == {"source": src_sha, "series": ser_sha}, "base_sha256 must be the sha256 of the two base files {source, series}")
    need(rec["hashes"] == {"schema_hash_unchanged": True, "schema_hash_with_optional_unchanged": True}, "hashes must read both unchanged")
    need(rec["new_fields"] == {"source": ["history_scope_claim"], "series": ["history_scope_claim", "history_scope_basis"]}, "new_fields differ")
    need(isinstance(rec["tests"], int) and not isinstance(rec["tests"], bool) and rec["tests"] == n_tests and n_tests >= 8, "tests must equal the recount, at least 8")
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
    if cid == "DB161-1-AC1":
        check_source(sb, src)
        check_series(rb, ser, hashlib.sha256(rb_raw).hexdigest())
        print("OK: source contract 0.4.6 and series contract 0.3.3 differ from their bases only in the allowed places (version, one appended history entry, the history_scope_claim column and its rule-24 key; the series pair, history_scope_rule, the widened unreported-days rule and the two reworded sentences); both schema hashes, columns, optional_columns and every other key are byte-identical")
        return True
    if cid == "DB161-1-AC2":
        check_source(sb, src)
        check_series(rb, ser, hashlib.sha256(rb_raw).hexdigest())
        check_behaviour(src, ser)
        print("OK: a reference rule driven only by the contracts' declarations accepts the legal rows (a claim beside PARTIAL_HISTORY or FULL, a legacy row without the claim) and the legal series (the pair, or neither) and refuses the illegal ones (a wrong claim value, a null claim, a lone field, a free-text basis)")
        return True
    if cid == "DB161-1-AC3":
        need((root / NEW_TEST).is_file(), "no %s" % NEW_TEST)
        n_new = run_pytest(root, [NEW_TEST])
        need(n_new >= 8, "the new test file holds %d passing tests, at least 8 are owed" % n_new)
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
    income = {"name": "income_claim", "type": "string", "values": ["absent"]}
    sbase = {"contract_version": "0.4.5", "schema_hash": "h1", "schema_hash_with_optional": "h2", "supersedes": [{"contract_version": "0.4.4"}], "rule24_record": {"v045": "x"}, "enums": {"history_scope": ["FULL", "PARTIAL_HISTORY"]},
             "columns": [{"name": "history_scope"}], "optional_columns": [], "conditional_columns": [income]}
    sgood = copy.deepcopy(sbase)
    sgood["contract_version"] = "0.4.6"
    sgood["conditional_columns"].append({"name": "history_scope_claim", "type": "string", "nullable": False, "meaning": "the claim beside history_scope: it is inferred per account, not read",
                                         "values": [CLAIM], "method": METHOD, "applies_to": "every row of a producer that derives history_scope", "since_schema_version": "1.6",
                                         "rule": "history_scope is PARTIAL_HISTORY when the account's first value day equals the source floor (the earliest balance partition the source holds) and FULL when it is after; the claim is inferred and never measured; it sits outside optional_columns; a row without it makes no claim."})
    sgood["supersedes"].append({"contract_version": "0.4.5", "schema_hash": "h1", "schema_hash_with_optional": "h2", "changes": "adds the conditional column history_scope_claim"})
    sgood["rule24_record"]["v046"] = "history_scope_claim has ONE value, inferred, and no other state; it is an ACCOUNT property like history_scope; the method is " + METHOD + "."
    assert check_source(sbase, sgood)
    sarms = (("version", lambda x: x.update(contract_version="0.4.5")), ("hash", lambda x: x.update(schema_hash="z")), ("section", lambda x: x.update(optional_columns=[1])), ("columns", lambda x: x["columns"].append({"name": "q"})),
             ("earlier entry", lambda x: x["conditional_columns"][0].update(values=["x"])), ("two new", lambda x: x["conditional_columns"].append({})), ("name", lambda x: x["conditional_columns"][-1].update(name="q")),
             ("nullable", lambda x: x["conditional_columns"][-1].update(nullable=True)), ("values", lambda x: x["conditional_columns"][-1].update(values=[CLAIM, "held"])), ("method", lambda x: x["conditional_columns"][-1].update(method="other")),
             ("rule words", lambda x: x["conditional_columns"][-1].update(rule="short")), ("meaning words", lambda x: x["conditional_columns"][-1].update(meaning="x")), ("extra key", lambda x: x["conditional_columns"][-1].update(z=1)),
             ("supersedes", lambda x: x["supersedes"].pop(0)), ("entry hash", lambda x: x["supersedes"][-1].update(schema_hash="z")), ("entry words", lambda x: x["supersedes"][-1].update(changes="nothing")),
             ("rule24", lambda x: x["rule24_record"].pop("v046")), ("rule24 words", lambda x: x["rule24_record"].update(v046="changed")), ("rule24 earlier", lambda x: x["rule24_record"].update(v045="y")))
    for label, fn in sarms:
        x = copy.deepcopy(sgood)
        fn(x)
        red(lambda: check_source(sbase, x), label)
    rbase = {"contract_version": "0.3.2", "lineage": [{"contract_version": "0.1.0"}], "writer": "w",
             "series": {"required": ["date"], "optional": ["income_claim"], "shape": "s",
                        "fields": {"history_scope": {"kind": "scalar string", "source": "history_scope", "sentence": "old"}, "unreported_trading_days": {"kind": "scalar list of string", "source": "old", "sentence": "s"}, "income_claim": {"kind": "k"}}},
             "unreported_days_rule": {"present_when": "the series' source carries the report-build statement; a series from a source with no such statement carries neither field", "pair": "p", "absent_means": "a"}}
    rgood = copy.deepcopy(rbase)
    rgood["contract_version"] = "0.3.3"
    rgood["lineage"].append({"contract_version": "0.3.2", "sha256": "a" * 64, "note": "the 0.3.2 bytes"})
    rgood["series"]["optional"] += ["history_scope_claim", "history_scope_basis"]
    f = rgood["series"]["fields"]
    f["history_scope"]["sentence"] = "Derived per account, never null: PARTIAL_HISTORY when first value day equals the source floor, else FULL; never null."
    f["unreported_trading_days"]["source"] = "the publisher's derivation from the gold partitions present, equal to the report-build statement where the source has one"
    f["history_scope_claim"] = {"kind": "scalar string", "source": "the source table contract's history_scope_claim column", "fixed_value": CLAIM, "sentence": "inferred"}
    f["history_scope_basis"] = {"kind": "scalar string", "source": "a fixed text", "fixed_value": METHOD, "const": True, "rule24_note": "one value", "sentence": "fixed text"}
    rgood["unreported_days_rule"]["present_when"] = "for every firm: the publisher derives the pair from the gold partitions present; [] when none are missing"
    rgood["history_scope_rule"] = {"present_when": "the newest gold row carries the claim", "pair": "both fields or neither; a lone field is invalid", "value": CLAIM, "basis": METHOD,
                                   "derivation": "PARTIAL_HISTORY when first_data_date equals the source floor (the earliest balance partition); FULL when it is after", "absent_means": "no statement"}
    assert check_series(rbase, rgood, "a" * 64)
    rarms = (("version", lambda x: x.update(contract_version="0.3.2")), ("lineage sha", lambda x: x["lineage"][-1].update(sha256="b" * 64)), ("other section", lambda x: x.update(writer="z")), ("optional order", lambda x: x["series"]["optional"].reverse()),
             ("missing field", lambda x: x["series"]["fields"].pop("history_scope_basis")), ("other field", lambda x: x["series"]["fields"]["income_claim"].update(kind="z")),
             ("claim value", lambda x: x["series"]["fields"]["history_scope_claim"].update(fixed_value="held")), ("claim keys", lambda x: x["series"]["fields"]["history_scope_claim"].update(z=1)),
             ("basis const", lambda x: x["series"]["fields"]["history_scope_basis"].update(const=False)), ("basis text", lambda x: x["series"]["fields"]["history_scope_basis"].update(fixed_value="other")),
             ("scope sentence", lambda x: x["series"]["fields"]["history_scope"].update(sentence="short")), ("unreported source", lambda x: x["series"]["fields"]["unreported_trading_days"].update(source="old")),
             ("unreported sentence", lambda x: x["series"]["fields"]["unreported_trading_days"].update(sentence="changed")), ("present_when", lambda x: x["unreported_days_rule"].update(present_when="sometimes")),
             ("present_when old", lambda x: x["unreported_days_rule"].update(present_when="for every firm gold partitions [] but carries neither field")), ("unreported pair", lambda x: x["unreported_days_rule"].update(pair="q")),
             ("rule value", lambda x: x["history_scope_rule"].update(value="held")), ("rule basis", lambda x: x["history_scope_rule"].update(basis="x")), ("rule derivation", lambda x: x["history_scope_rule"].update(derivation="words")),
             ("rule pair", lambda x: x["history_scope_rule"].update(pair="x")), ("rule keys", lambda x: x["history_scope_rule"].update(z=1)), ("rule gone", lambda x: x.pop("history_scope_rule")))
    for label, fn in rarms:
        x = copy.deepcopy(rgood)
        fn(x)
        red(lambda: check_series(rbase, x, "a" * 64), label)
    assert check_behaviour(sgood, rgood)
    for label, fn in (("enum", lambda s, r: s["enums"].update(history_scope=["FULL"])), ("claim value drift", lambda s, r: r["series"]["fields"]["history_scope_claim"].update(fixed_value="held")),
                      ("basis drift", lambda s, r: r["history_scope_rule"].update(basis="other"))):
        s2, r2 = copy.deepcopy(sgood), copy.deepcopy(rgood)
        fn(s2, r2)
        red(lambda: check_behaviour(s2, r2), "behaviour: " + label)
    assert check_grant({SRC_REL, SER_REL, NEW_TEST, EARLIER[0], D + AUTHOR + "/x.json"})
    red(lambda: check_grant({SRC_REL, SER_REL, NEW_TEST, "lib/x.py"}), "outside grant")
    red(lambda: check_grant({SRC_REL, NEW_TEST}), "one contract")
    rec = {"source_version": "0.4.6", "series_version": "0.3.3", "base_sha256": {"source": "a" * 64, "series": "b" * 64}, "hashes": {"schema_hash_unchanged": True, "schema_hash_with_optional_unchanged": True},
           "new_fields": {"source": ["history_scope_claim"], "series": ["history_scope_claim", "history_scope_basis"]}, "tests": 8, "words": "w" * 100}
    assert check_facts(rec, "a" * 64, "b" * 64, 8)
    farms = (("source", lambda r: r.update(source_version="0.4.5")), ("series", lambda r: r.update(series_version="0.3.2")), ("base", lambda r: r["base_sha256"].update(source="c" * 64)), ("hashes", lambda r: r["hashes"].update(schema_hash_unchanged=False)),
             ("fields", lambda r: r["new_fields"].update(source=[])), ("tests", lambda r: r.update(tests=9)), ("extra", lambda r: r.update(z=1)), ("words", lambda r: r.update(words="short")), ("digits", lambda r: r.update(words="w" * 100 + " 123456789")))
    for label, fn in farms:
        r2 = copy.deepcopy(rec)
        fn(r2)
        red(lambda: check_facts(r2, "a" * 64, "b" * 64, 8), label)
    print("selftest: source (%d red arms), series (%d), behaviour (3), grant (2) and facts (%d) clauses behave" % (len(sarms), len(rarms), len(farms)))
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
