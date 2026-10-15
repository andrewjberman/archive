"""IRPT_DASHBD round 120, workstream B-49F (issuer 2.0.0_SA_COO~D2) -- DB-b-241, the FACTS for the Cottonwood Black Diamond account return adapter's LANDING
PACKET (CTO analysis @5e358b0a8f ruling 5: "the Cottonwood BD adapter lands by its own never-widen pair: ~D2 writes the packet, ~DB2 applies, with a
`*-cot-*` role, builder names and a trading-day frontier").

  DB-b-241 (~195) a READ: what exactly a landing of `adapters/cottonwood_bd_account_return_daily.py` needs: the function (its shape and the precedent it
                  copies), every resource name from the BUILDERS (`lib/opal_naming.py name()` and `address()`), the Cottonwood gold prefix it writes, the
                  IAM it needs (read of the Black Diamond silver grant, write of one Cottonwood gold prefix), the schedule and its input frontier
                  (when the silver lands and when the Commonwealth-free first run can fire), what the adapter itself must change before a landing (the
                  `source` column, a write path), the expected plan, the blast radius and the rollback per key. The issuer writes the packet from it.
                  Nothing is built, changed, applied or written.                                   DB120-5-AC1

The checker RECOMPUTES every builder name and address in the record from `lib/opal_naming.py`, checks that every file path named exists and every line number
is an integer inside its file, and grades the plan and flags.

Usage: python <this file> <repo_root> <criterion_id>      prints "<id> PASS" or "<id> FAIL" last
       python <this file> --selftest [<repo_root>]          the pure helpers and the record clauses on synthetic arms
"""
import json
import re
import sys
from pathlib import Path

D = "org/missions/D9/IRPT/IRPT_DASHBD/deliverables/"
REC_REL = D + "0.9.0_WK_IRPT_DASHBD~195/RD_CW_LANDING_FACTS_R120.json"
ADAPTER_REL = "data/assets/scripts/gold/irpt_reporting/adapters/cottonwood_bd_account_return_daily.py"
CLAIMS = ("measured", "inferred", "held", "absent")
LONG_DIGITS = re.compile(r"\d{8,}")
DIGIT_OK_KEYS = ("sha256", "path", "file", "key", "where", "vintage", "line", "name", "address", "cron")


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


def check_record(rec, build_name, build_address, line_count):
    """build_name(**args) -> name or raises; build_address(args list) -> address or raises; line_count(rel) -> int or None (missing)."""
    exp = {"firm", "adapter", "landing_shape", "names", "addresses", "iam", "schedule", "adapter_changes", "registry_rows_needed", "expected_plan", "blast_radius",
           "rollback", "words", "claim", "files_in_repo", "served_values_changed", "pushed", "deployed"}
    need(isinstance(rec, dict) and set(rec) == exp, "record keys differ: %s" % (sorted(set(rec) ^ exp) if isinstance(rec, dict) else "?"))
    need(rec["firm"] == "cottonwood" and nes(rec["words"]) and rec["claim"] in CLAIMS, "firm, words or claim")
    ad = rec["adapter"]
    need(isinstance(ad, dict) and set(ad) == {"file", "entry_points", "words"} and ad["file"] == ADAPTER_REL and line_count(ad["file"]) and isinstance(ad["entry_points"], list)
         and len(ad["entry_points"]) >= 1 and nes(ad["words"]), "adapter form")
    for e in ad["entry_points"]:
        need(isinstance(e, dict) and set(e) == {"function", "line"} and nes(e["function"]) and is_int(e["line"]) and 1 <= e["line"] <= line_count(ad["file"]), "an entry point needs a function and a line inside the file")
    ls = rec["landing_shape"]
    need(isinstance(ls, dict) and set(ls) == {"kind", "precedent", "words"} and nes(ls["kind"]) and nes(ls["words"]) and isinstance(ls["precedent"], dict)
         and set(ls["precedent"]) == {"file", "line", "words"} and line_count(ls["precedent"]["file"]) and is_int(ls["precedent"]["line"]) and 1 <= ls["precedent"]["line"] <= line_count(ls["precedent"]["file"])
         and nes(ls["precedent"]["words"]), "landing_shape form: a kind, words and a precedent file and line that exist")
    nms = rec["names"]
    need(isinstance(nms, list) and len(nms) >= 3, "at least three names (the function, its role, its schedule)")
    for n in nms:
        need(isinstance(n, dict) and set(n) == {"purpose", "builder_args", "name"} and nes(n["purpose"]) and isinstance(n["builder_args"], dict) and nes(n["name"]), "a names entry")
        try:
            got = build_name(**n["builder_args"])
        except Exception as e:
            raise Fail("builder REFUSES %s: %s (a refusal is a registry row to add, listed in registry_rows_needed, never a typed name)" % (n["builder_args"], str(e)[:100]))
        need(got == n["name"], "name for %s: record %s, builder %s" % (n["purpose"], n["name"], got))
    ads = rec["addresses"]
    need(isinstance(ads, list) and len(ads) >= 2, "at least two addresses (the table written and the silver or gold read)")
    for a in ads:
        need(isinstance(a, dict) and set(a) == {"purpose", "builder_args", "address"} and nes(a["purpose"]) and isinstance(a["builder_args"], list) and nes(a["address"]), "an addresses entry")
        try:
            got = build_address(a["builder_args"])
        except Exception as e:
            raise Fail("address builder REFUSES %s: %s" % (a["builder_args"], str(e)[:100]))
        need(got == a["address"], "address for %s: record %s, builder %s" % (a["purpose"], a["address"], got))
    iam = rec["iam"]
    need(isinstance(iam, list) and len(iam) >= 2 and all(isinstance(s, dict) and set(s) == {"statement", "actions", "resources", "words"} and nes(s["statement"])
         and isinstance(s["actions"], list) and s["actions"] and isinstance(s["resources"], list) and s["resources"] and nes(s["words"]) for s in iam), "iam statements: at least two, each with actions and resources")
    need(not any(a in ("*", "s3:*") for s in iam for a in s["actions"]), "no wildcard action")
    sc = rec["schedule"]
    need(isinstance(sc, dict) and set(sc) == {"cron", "zone", "inputs", "frontier_rule", "words"} and nes(sc["cron"]) and nes(sc["zone"]) and isinstance(sc["inputs"], list) and sc["inputs"]
         and nes(sc["frontier_rule"]) and "trading" in sc["frontier_rule"].lower() and nes(sc["words"]), "schedule form with a trading-day frontier rule")
    ac = rec["adapter_changes"]
    need(isinstance(ac, list) and len(ac) >= 2 and all(isinstance(x, dict) and set(x) == {"change", "why"} and nes(x["change"]) and nes(x["why"]) for x in ac), "adapter_changes")
    need(any("source" in x["change"].lower() for x in ac), "adapter_changes must include emitting the `source` column")
    need(isinstance(rec["registry_rows_needed"], list) and all(nes(x) for x in rec["registry_rows_needed"]), "registry_rows_needed form")
    ep = rec["expected_plan"]
    need(isinstance(ep, dict) and set(ep) == {"to_add", "to_change", "to_destroy", "resources", "words"} and all(is_int(ep[k]) and ep[k] >= 0 for k in ("to_add", "to_change", "to_destroy"))
         and ep["to_destroy"] == 0 and ep["to_add"] >= 1 and isinstance(ep["resources"], list) and len(ep["resources"]) == ep["to_add"] + ep["to_change"] and nes(ep["words"]),
         "expected_plan: to_destroy 0, at least one add, resources listing every add and change")
    need(nes(rec["blast_radius"]) and nes(rec["rollback"]), "blast_radius and rollback words")
    need(rec["files_in_repo"] is False and rec["served_values_changed"] is False and rec["pushed"] is False and rec["deployed"] is False, "a flag is not false")
    need(not digit_runs(rec), "a run of 8 or more digits outside the exempt fields: %s" % digit_runs(rec)[:2])
    return True


def run(root, cid):
    need(cid == "DB120-5-AC1", "unknown criterion %s" % cid)
    root = Path(root)
    sys.path.insert(0, str(root))
    from lib import opal_naming
    rec = load_json(root, REC_REL)

    def lc(rel):
        p = root / rel
        return len(p.read_text(encoding="utf-8").splitlines()) if p.is_file() else None

    def bname(**kw):
        return opal_naming.name(**kw)

    def baddr(args):
        return opal_naming.address(*args)
    check_record(rec, bname, baddr, lc)
    print("OK: landing facts: %d names and %d addresses recomputed from the builders and equal, the adapter and precedent files and lines exist, the IAM has no wildcard, "
          "the schedule has a trading-day frontier, the plan has no destroy" % (len(rec["names"]), len(rec["addresses"])))
    return True


def selftest(root):
    def good():
        return {"firm": "cottonwood", "adapter": {"file": ADAPTER_REL, "entry_points": [{"function": "derive", "line": 10}], "words": "w"},
                "landing_shape": {"kind": "lambda", "precedent": {"file": "p.py", "line": 5, "words": "w"}, "words": "w"},
                "names": [{"purpose": p, "builder_args": {"system": "irpt", "scope": "cottonwood", "function": "f", "kind": k}, "name": "irpt-cot-f-" + k} for p, k in
                          (("function", "lambda"), ("role", "role"), ("schedule", "schedule"))],
                "addresses": [{"purpose": "table", "builder_args": ["irpt", "cottonwood", "gold", "t", "date=D"], "address": "s3://b/k"},
                              {"purpose": "silver", "builder_args": ["x"], "address": "s3://b/s"}],
                "iam": [{"statement": "ReadSilver", "actions": ["s3:GetObject"], "resources": ["arn:x"], "words": "w"},
                        {"statement": "WriteGold", "actions": ["s3:PutObject"], "resources": ["arn:y"], "words": "w"}],
                "schedule": {"cron": "cron(0 8 ? * MON-FRI *)", "zone": "America/New_York", "inputs": ["silver"], "frontier_rule": "the trading-day frontier T-1", "words": "w"},
                "adapter_changes": [{"change": "emit the source column", "why": "w"}, {"change": "a write path", "why": "w"}], "registry_rows_needed": [],
                "expected_plan": {"to_add": 2, "to_change": 0, "to_destroy": 0, "resources": ["a", "b"], "words": "w"}, "blast_radius": "w", "rollback": "w", "words": "w", "claim": "measured",
                "files_in_repo": False, "served_values_changed": False, "pushed": False, "deployed": False}

    def bname(**kw):
        return "irpt-cot-f-" + kw["kind"]

    def baddr(args):
        if args == ["x"]:
            return "s3://b/s"
        return "s3://b/k"

    def grade(rec, bn=bname, ba=baddr, lc=lambda rel: 100):
        try:
            return check_record(rec, bn, ba, lc)
        except Fail:
            return False
    need(grade(good()) is True, "GREEN arm failed")
    for mut, why in ((lambda r: r["names"][0].update(name="typed-name"), "a name that is not builder output"),
                     (lambda r: r["addresses"][0].update(address="s3://other/k"), "an address that differs"),
                     (lambda r: r["iam"][0]["actions"].append("s3:*"), "a wildcard action"), (lambda r: r["expected_plan"].update(to_destroy=1), "a destroy"),
                     (lambda r: r["expected_plan"].update(resources=["a"]), "resources that do not list every change"),
                     (lambda r: r["schedule"].update(frontier_rule="every day"), "no trading-day frontier"),
                     (lambda r: r["adapter_changes"].pop(0), "no source column change"), (lambda r: r["adapter"]["entry_points"][0].update(line=500), "a line outside the file"),
                     (lambda r: r.update(words="ids 1234567890"), "a digit run"), (lambda r: r.update(pushed=True), "a push flag"),
                     (lambda r: r["names"].pop(), "fewer than three names")):
        r = json.loads(json.dumps(good()))
        mut(r)
        need(grade(r) is False, "RED: " + why)

    def refuse(**kw):
        raise ValueError("refused token")
    need(grade(good(), bn=refuse) is False, "RED: a builder refusal must fail")
    need(grade(good(), lc=lambda rel: None) is False, "RED: a missing file must fail")
    print("selftest OK: 1 green and 13 red landing arms")


if __name__ == "__main__":
    try:
        if len(sys.argv) >= 2 and sys.argv[1] == "--selftest":
            selftest(sys.argv[2] if len(sys.argv) > 2 else ".")
            sys.exit(0)
        if len(sys.argv) != 3:
            print("usage: p120_landing.py <repo_root> <criterion_id>")
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
