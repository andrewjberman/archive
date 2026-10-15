"""IRPT_DASHBD round 120, workstream B-49F (issuer 2.0.0_SA_COO~D2) -- DB-b-240, the account return contract's `source` column
(CTO analysis @5e358b0a8f ruling 4: "the return contract gains a `source` column, a minor bump, values are words such as orion, computed from
Black Diamond values and flows, computed from custodian holdings, so the page can state it").

  DB-b-240 (~194) contract 0.3.0 of the account return table declares an OPTIONAL column `source` (string, nullable, words) with its own schema hash,
                  WITHOUT touching the 19 existing columns or their hash (every table landed so far, and every producer and adapter that
                  checks the 19-column hash, stays valid); a record names every emitter that must add the column at its own landing.
                                                                                       DB120-4-AC1 (the contract), AC2 (the emitters)

Usage: python <this file> <repo_root> <criterion_id>      prints "<id> PASS" or "<id> FAIL" last
       python <this file> --selftest [<repo_root>]          the pure helpers and the clauses on synthetic arms
"""
import hashlib
import json
import re
import subprocess
import sys
from pathlib import Path

D = "org/missions/D9/IRPT/IRPT_DASHBD/deliverables/"
REC_REL = D + "0.9.0_WK_IRPT_DASHBD~194/RD_SOURCE_COLUMN_R120.json"
CONTRACT_REL = "org/standards/IRPT_DASHBD_ACCOUNT_RETURN_DAILY_CONTRACT.json"
BASE_VERSION = "0.2.0"
BASE_HASH = "1b25d37ba6cfcf5a7413373ccdca57e306b86614aff94472ca65ca0025484946"
CLAIMS = ("measured", "inferred", "held", "absent")
LONG_DIGITS = re.compile(r"\d{8,}")
DIGIT_OK_KEYS = ("sha256", "path", "file", "key", "where", "vintage", "schema_hash", "hash_with_optional", "line")
REQUIRED_VALUES = ("orion", "computed from Black Diamond values and flows", "computed from custodian holdings")
EMITTERS = ("data/assets/scripts/gold/irpt_reporting/account_return_daily.py",
            "data/assets/scripts/gold/irpt_reporting/adapters/inflection_account_return_daily.py",
            "data/assets/scripts/gold/irpt_reporting/adapters/cottonwood_bd_account_return_daily.py")


class Fail(Exception):
    pass


def need(cond, msg):
    if not cond:
        raise Fail(msg)


def nes(x):
    return isinstance(x, str) and x.strip() != ""


def is_int(x):
    return isinstance(x, int) and not isinstance(x, bool)


def digit_runs(x, key=""):
    if isinstance(x, dict):
        return [h for k, v in x.items() for h in digit_runs(v, str(k))]
    if isinstance(x, list):
        return [h for v in x for h in digit_runs(v, key)]
    if isinstance(x, str) and key not in DIGIT_OK_KEYS:
        return LONG_DIGITS.findall(x)
    return []


def load_json(root, rel):
    p = Path(root) / rel
    need(p.is_file(), "no %s" % rel)
    return json.loads(p.read_bytes().decode("utf-8"))


def schema_hash(cols):
    return hashlib.sha256("\n".join(sorted("%s:%s" % (c["name"], c["type"]) for c in cols)).encode("utf-8")).hexdigest()


def is_tracked(root, rel):
    return subprocess.run(["git", "-C", str(root), "ls-files", "--error-unmatch", rel], capture_output=True, text=True).returncode == 0


def check_contract(c, columns_sha):
    need(c.get("contract_version") == "0.3.0", "contract_version is not 0.3.0 (a minor bump)")
    cols = c["columns"]
    need(len(cols) == 19 and schema_hash(cols) == c["schema_hash"] == BASE_HASH, "the 19 columns or their schema_hash changed")
    need(hashlib.sha256(json.dumps(cols, sort_keys=True, separators=(",", ":")).encode()).hexdigest() == columns_sha, "a column definition changed")
    oc = c.get("optional_columns")
    need(isinstance(oc, list) and len(oc) == 1 and oc[0].get("name") == "source", "optional_columns must hold exactly the column `source`")
    o = oc[0]
    need(o.get("type") == "string" and o.get("nullable") is True and nes(o.get("meaning")) and nes(o.get("since_schema_version")), "the source column: string, nullable, meaning, since_schema_version")
    vals = o.get("values")
    need(isinstance(vals, list) and all(v in vals for v in REQUIRED_VALUES) and all(nes(v) for v in vals), "the source column's values must include %s" % (REQUIRED_VALUES,))
    need(nes(o.get("rule")) and "absent" in o["rule"].lower(), "the source column's rule must say what an absent source means")
    need(c.get("schema_hash_with_optional") == schema_hash(cols + [{"name": "source", "type": "string"}]), "schema_hash_with_optional is not the recomputed hash over the 19 columns plus source:string")
    sup = [x for x in c.get("supersedes", []) if x.get("contract_version") == BASE_VERSION]
    need(len(sup) == 1 and sup[0].get("schema_hash") == BASE_HASH and any("source" in str(ch) for ch in sup[0].get("changes", [sup[0]])) or len(sup) == 1 and sup[0].get("schema_hash") == BASE_HASH,
         "supersedes must carry the 0.2.0 entry with its schema_hash")
    return True


def check_record(rec, root_has):
    exp = {"contract_version", "optional_column", "hash_with_optional", "emitters", "words", "claim", "files_in_repo", "served_values_changed", "pushed", "deployed"}
    need(isinstance(rec, dict) and set(rec) == exp, "record keys differ: %s" % (sorted(set(rec) ^ exp) if isinstance(rec, dict) else "?"))
    need(rec["contract_version"] == "0.3.0" and nes(rec["words"]) and rec["claim"] in CLAIMS, "contract_version, words or claim")
    need(isinstance(rec["optional_column"], dict) and rec["optional_column"].get("name") == "source" and rec["optional_column"].get("type") == "string", "optional_column")
    em = rec["emitters"]
    need(isinstance(em, list) and [e.get("file") for e in em] == list(EMITTERS), "emitters must list the producer and the two adapters, in order")
    for e in em:
        need(set(e) == {"file", "kind", "schema_line", "must_add_at_landing", "words"} and is_int(e["schema_line"]) and e["schema_line"] > 0 and e["must_add_at_landing"] is True
             and nes(e["kind"]) and nes(e["words"]), "an emitter entry: %s" % e.get("file"))
        need(root_has(e["file"], e["schema_line"]), "emitter %s: line %s does not mention the schema" % (e["file"], e["schema_line"]))
    need(rec["files_in_repo"] is False and rec["served_values_changed"] is False and rec["pushed"] is False and rec["deployed"] is False, "a flag is not false")
    need(not digit_runs(rec), "a run of 8 or more digits outside the exempt fields: %s" % digit_runs(rec)[:2])
    return True


def run(root, cid):
    root = Path(root)
    if cid == "DB120-4-AC1":
        c = load_json(root, CONTRACT_REL)
        check_contract(c, COLUMNS_SHA)
        print("OK: contract 0.3.0: the 19 columns and their hash are unchanged; the optional column `source` (string, nullable, words) carries its own hash %s; supersedes holds 0.2.0"
              % c["schema_hash_with_optional"][:12])
        return True
    if cid == "DB120-4-AC2":
        rec = load_json(root, REC_REL)
        c = load_json(root, CONTRACT_REL)
        need(rec.get("hash_with_optional") == c.get("schema_hash_with_optional"), "the record's hash_with_optional differs from the contract's")

        def has(rel, line):
            p = root / rel
            if not p.is_file():
                return False
            lines = p.read_text(encoding="utf-8").splitlines()
            return 1 <= line <= len(lines) and re.search(r"schema", lines[line - 1], re.I) is not None
        check_record(rec, has)
        print("OK: the record names the three emitters (the producer and the Inflection and Cottonwood adapters) with a schema line that exists in each, and the hash equals the contract's")
        return True
    raise Fail("unknown criterion %s" % cid)


COLUMNS_SHA = None


def _init_columns_sha():
    global COLUMNS_SHA
    p = Path(__file__).resolve().parent / "p120_srccol.columns.sha256"
    COLUMNS_SHA = p.read_text(encoding="ascii").strip() if p.is_file() else "0" * 64


def selftest(root):
    cols = [{"name": "a", "type": "string"}, {"name": "b", "type": "double"}]
    h = schema_hash(cols)
    need(h == hashlib.sha256(b"a:string\nb:double").hexdigest(), "schema_hash")
    need(schema_hash(cols + [{"name": "source", "type": "string"}]) != h, "the optional hash differs")
    base = {"contract_version": "0.3.0", "schema_hash": BASE_HASH, "columns": [], "optional_columns": [], "supersedes": []}
    try:
        check_contract(base, "0" * 64)
        raise Fail("RED: an empty contract must fail")
    except Fail as e:
        need("RED" not in str(e), str(e))
    emit = [{"file": f, "kind": "k", "schema_line": 10, "must_add_at_landing": True, "words": "w"} for f in EMITTERS]
    rec = {"contract_version": "0.3.0", "optional_column": {"name": "source", "type": "string"}, "hash_with_optional": "ab" * 32, "emitters": emit, "words": "w", "claim": "measured",
           "files_in_repo": False, "served_values_changed": False, "pushed": False, "deployed": False}
    need(check_record(rec, lambda f, line: True), "record GREEN")
    for mut, why in ((lambda r: r["emitters"].pop(), "a missing emitter"), (lambda r: r["emitters"][0].update(schema_line=0), "line 0"),
                     (lambda r: r.update(pushed=True), "push flag"), (lambda r: r.update(words="ids 1234567890"), "digit run"),
                     (lambda r: r.update(contract_version="0.2.1"), "version")):
        r2 = json.loads(json.dumps(rec))
        mut(r2)
        try:
            check_record(r2, lambda f, line: True)
            raise Fail("RED: record clause did not fail: " + why)
        except Fail as e:
            need("RED" not in str(e), str(e))
    try:
        check_record(rec, lambda f, line: False)
        raise Fail("RED: a schema line that does not mention the schema must fail")
    except Fail as e:
        need("RED" not in str(e), str(e))
    print("selftest OK: hash arms, 1 contract red arm, 1 green and 6 red record arms")


if __name__ == "__main__":
    _init_columns_sha()
    try:
        if len(sys.argv) >= 2 and sys.argv[1] == "--selftest":
            selftest(sys.argv[2] if len(sys.argv) > 2 else ".")
            sys.exit(0)
        if len(sys.argv) != 3:
            print("usage: p120_srccol.py <repo_root> <criterion_id>")
            sys.exit(2)
        run(sys.argv[1], sys.argv[2])
        print("%s PASS" % sys.argv[2])
    except Fail as e:
        print("FAIL: %s" % e)
        print("%s FAIL" % (sys.argv[2] if len(sys.argv) > 2 else "?"))
        sys.exit(1)
    except Exception as e:
        print("FAIL: %s: %s" % (type(e).__name__, str(e)[:200]))
        print("%s FAIL" % (sys.argv[2] if len(sys.argv) > 2 else "?"))
        sys.exit(1)
