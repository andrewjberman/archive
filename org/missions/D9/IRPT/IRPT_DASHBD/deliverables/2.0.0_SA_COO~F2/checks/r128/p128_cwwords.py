"""IRPT_DASHBD round 128, workstream F-SHIP ~F2 (issuer 2.0.0_SA_COO~F2) -- FWD-5: Cottonwood's words RE-CUT at (Transaction Type, Sub Type) grain.

  DB-f-1402 (~1402) the CTO's round-126 analysis (msg 9133, ruling 2) SUSPENDED Cottonwood's ratified words and ordered them re-cut at the
                    true grain: the type word decided on the (Transaction Type, Transaction Sub Type) pair with its denominator printed from
                    the live data, the action word taken from the vendor's Action column (87 values), flow class per code, and the rule-24
                    record and the token census repeated for Cottonwood only.                         DBF128-2-AC1 (the subtraction), AC2 (the law)

The checker computes both Cottonwood denominators FROM THE LIVE CENSUS RECORD (the issuer's read, since a worker has no AWS access): the
distinct (Transaction Type, Transaction Sub Type) pairs (33) and the distinct Action values (87), and holds the flow class to the rule the
vendor's own External Flow column implies (Contribution is EXTERNAL_IN, Withdrawal is EXTERNAL_OUT, None leaves the pair's own class).

Usage: python <this file> <repo_root> <criterion_id>      prints "<id> PASS" or "<id> FAIL" last
       python <this file> --selftest                        the pure helpers on synthetic arms
"""
import json
import re
import sys
from pathlib import Path

D = "org/missions/D9/IRPT/IRPT_DASHBD/deliverables/"
CENSUS = D + "2.0.0_SA_COO~F2/R128_LIVE_SOURCE_CENSUS_3FIRMS.json"
RATIFIED = D + "0.9.0_WK_IRPT_DASHBD~1001/FWD5_WORDS_PROPOSAL_R124.json"
REC = D + "0.9.0_WK_IRPT_DASHBD~1402/FWD5_WORDS_COTTONWOOD_R128.json"
CLAIMS = ("measured", "inferred", "held", "absent")
UNMAPPED = "UNMAPPED"
LONG_DIGITS = re.compile(r"\d{8,}")
DIGIT_OK_KEYS = ("sha256", "path", "file", "key", "where", "vintage", "rows", "partitions_read", "read_at_utc")
POSTULATES = ("mece", "same_grain", "intent_coherence", "state_coherence")
KEYS = ("as_of", "claim", "postulates", "opal_types_added", "opal_actions_added", "external_flow_rule", "unmapped_display", "mapping",
        "state_coherence_by_word", "state_coherence_by_action", "census", "reads", "files_in_repo", "served_values_changed",
        "pushed", "deployed")
ZERO_READS = {"s3_reads": 0, "s3_writes": 0, "dynamodb_writes": 0, "vendor_calls": 0, "secret_reads": 0}
WORD = re.compile(r"^[A-Za-z][A-Za-z ]{1,40}$")
FLOW_NONE = ("INTERNAL", "INCOME", "FEE", "CORPORATE_ACTION", "UNRESOLVED")
EXTERNAL_FLOW_RULE = {"Contribution": "EXTERNAL_IN", "Withdrawal": "EXTERNAL_OUT"}
SEP = " | "


class Fail(Exception):
    pass


def need(cond, msg):
    if not cond:
        raise Fail(msg)


def load(root, rel):
    p = Path(root) / rel
    need(p.is_file(), "missing file " + rel)
    return json.loads(p.read_text(encoding="utf-8"))


def digits_ok(obj, key=""):
    if isinstance(obj, dict):
        return all(digits_ok(v, k) for k, v in obj.items())
    if isinstance(obj, list):
        return all(digits_ok(v, key) for v in obj)
    if isinstance(obj, str) and LONG_DIGITS.search(obj) and key not in DIGIT_OK_KEYS:
        return False
    return True


def domains(cw):
    """({pair source_value: set of External Flow values seen}, [Action values]) from the census's Cottonwood section."""
    pairs = {p["transaction_type"] + SEP + p["transaction_sub_type"]: set(p["external_flow"]) for p in cw["pairs"]}
    return pairs, list(cw["values"]["Action"])


def rows_of(rec, field):
    return [m for m in rec["mapping"] if isinstance(m, dict) and m.get("field") == field]


def subtraction(field, domain, rec):
    got = [m.get("source_value") for m in rows_of(rec, field)]
    pr = []
    missing = [c for c in domain if c not in got]
    extra = [c for c in got if c not in domain]
    dup = sorted({c for c in got if got.count(c) > 1})
    if missing:
        pr.append("%s: values with no mapping row: %d (first %r)" % (field, len(missing), missing[0]))
    if extra:
        pr.append("%s: rows with no live value: %d (first %r)" % (field, len(extra), extra[0]))
    if dup:
        pr.append("%s: duplicate rows: %d (first %r)" % (field, len(dup), dup[0]))
    if any(m.get("firm") != "cottonwood" for m in rows_of(rec, field)):
        pr.append("%s: every row must carry firm cottonwood" % field)
    return pr


def vocab(ratified, rec):
    types = [t["word"] for t in ratified["opal_types"]]
    acts = [a["word"] for a in ratified["opal_actions"]]
    pr = []
    for key, base, label in (("opal_types_added", types, "type"), ("opal_actions_added", acts, "action")):
        added = rec[key]
        if not (isinstance(added, list) and all(isinstance(a, dict) and isinstance(a.get("word"), str) and WORD.match(a["word"])
                                                and isinstance(a.get("definition"), str) and a["definition"].strip() for a in added)):
            pr.append("%s: form (each {word, definition})" % key)
            continue
        words = [a["word"] for a in added]
        if len(set(words)) != len(words) or set(words) & set(base):
            pr.append("%s: a duplicate of itself or of a ratified %s word" % (key, label))
        base.extend(words)
    return types, acts, pr


def row_problems(pairs, types, acts, rec):
    pr = []
    for m in rows_of(rec, "type_pair"):
        key = m.get("source_value")
        w = m.get("opal_type")
        if w != UNMAPPED and w not in types:
            pr.append("pair %r uses an undefined type word %r" % (key, w))
        if w == UNMAPPED and not (isinstance(m.get("reason"), str) and m["reason"].strip()):
            pr.append("pair %r is UNMAPPED with no reason" % key)
        fc = m.get("flow_class_none")
        seen = pairs.get(key)
        if seen is None:
            continue
        if "None" in seen:
            if fc not in FLOW_NONE:
                pr.append("pair %r has External Flow None rows: flow_class_none must be one of %r" % (key, FLOW_NONE))
        elif fc is not None:
            pr.append("pair %r has no External Flow None rows: flow_class_none must be null" % key)
    for m in rows_of(rec, "action"):
        w = m.get("opal_action")
        if w != UNMAPPED and w not in acts:
            pr.append("action %r uses an undefined action word %r" % (m.get("source_value"), w))
        if w == UNMAPPED and not (isinstance(m.get("reason"), str) and m["reason"].strip()):
            pr.append("action %r is UNMAPPED with no reason" % m.get("source_value"))
    return pr


def counts(rec):
    t, a = {}, {}
    for m in rows_of(rec, "type_pair"):
        t[m.get("opal_type")] = t.get(m.get("opal_type"), 0) + 1
    for m in rows_of(rec, "action"):
        a[m.get("opal_action")] = a.get(m.get("opal_action"), 0) + 1
    return t, a


def law_problems(cw, rec, pairs, actions):
    pr = []
    po = rec["postulates"]
    if not (isinstance(po, dict) and sorted(po.keys()) == sorted(POSTULATES)
            and all(isinstance(po[k], str) and len(po[k].strip()) >= 40 for k in POSTULATES)):
        pr.append("postulates must be exactly %r, each at least 40 characters" % (POSTULATES,))
    else:
        if "Transaction Sub Type" not in po["mece"] or "Transaction Sub Type" not in po["same_grain"] or "Action" not in po["mece"]:
            pr.append("the mece and same_grain postulates must name the Transaction Sub Type grain, and mece the Action domain")
    if rec["external_flow_rule"] != EXTERNAL_FLOW_RULE:
        pr.append("external_flow_rule must be %r" % EXTERNAL_FLOW_RULE)
    if rec["unmapped_display"] != "Unclassified":
        pr.append("unmapped_display must be Unclassified (CTO round-125 ruling)")
    tcount, acount = counts(rec)
    for key, used in (("state_coherence_by_word", sorted({k for k in tcount} | {UNMAPPED})),
                      ("state_coherence_by_action", sorted({k for k in acount} | {UNMAPPED}))):
        sc = rec[key]
        if not (isinstance(sc, dict) and sorted(sc.keys()) == used and all(isinstance(v, str) and len(v.strip()) >= 20 for v in sc.values())):
            pr.append("%s must have exactly one string (20+ characters) per word used and one for UNMAPPED" % key)
    c = rec["census"]
    if not isinstance(c, dict):
        return pr + ["census form"]
    if c.get("method") != "word-boundary":
        pr.append("census.method is not word-boundary")
    if c.get("denominators") != {"type_pairs": len(pairs), "actions": len(actions)}:
        pr.append("census.denominators must be {type_pairs: %d, actions: %d}" % (len(pairs), len(actions)))
    if c.get("distinct") != {"transaction_type": cw["distinct"]["Transaction Type"], "transaction_sub_type": cw["distinct"]["Transaction Sub Type"],
                             "action": cw["distinct"]["Action"]}:
        pr.append("census.distinct must be the live census's distinct counts of Transaction Type, Sub Type and Action")
    if c.get("per_type_word") != tcount or c.get("per_action_word") != acount:
        pr.append("census.per_type_word / per_action_word do not equal the counts computed from the mapping")
    if c.get("unmapped") != {"type_pairs": tcount.get(UNMAPPED, 0), "actions": acount.get(UNMAPPED, 0)}:
        pr.append("census.unmapped must be the UNMAPPED counts computed from the mapping")
    return pr


def form_problems(rec):
    if not isinstance(rec, dict) or sorted(rec.keys()) != sorted(KEYS):
        return ["top-level fields are not exactly " + repr(KEYS)]
    pr = []
    if not (isinstance(rec["as_of"], str) and re.match(r"\d{4}-\d{2}-\d{2}$", rec["as_of"])):
        pr.append("as_of not an ISO date")
    if rec["claim"] not in CLAIMS:
        pr.append("claim not in the four-word set")
    if rec["reads"] != ZERO_READS:
        pr.append("reads is not the all-zero form (the worker reads no source; the census is the issuer's)")
    for k in ("files_in_repo", "served_values_changed", "pushed", "deployed"):
        if rec[k] is not False:
            pr.append(k + " is not false")
    if not digits_ok(rec):
        pr.append("a run of 8 or more digits outside the exempt fields")
    if not json.dumps(rec, ensure_ascii=False).isascii():
        pr.append("non-ASCII text")
    if not (isinstance(rec["mapping"], list) and rec["mapping"]):
        pr.append("mapping is empty")
    return pr


def prepare(root):
    census = load(root, CENSUS)
    cw = census["firms"]["cottonwood"]
    rec = load(root, REC)
    pr = form_problems(rec)
    need(not pr, "; ".join(pr[:6]))
    pairs, actions = domains(cw)
    return cw, rec, pairs, actions


def ac_subtraction(root):
    cw, rec, pairs, actions = prepare(root)
    types, acts, pr = vocab(load(root, RATIFIED), rec)
    pr += subtraction("type_pair", list(pairs), rec) + subtraction("action", actions, rec) + row_problems(pairs, types, acts, rec)
    need(not pr, "; ".join(pr[:6]))


def ac_law(root):
    cw, rec, pairs, actions = prepare(root)
    pr = law_problems(cw, rec, pairs, actions)
    need(not pr, "; ".join(pr[:6]))


def selftest():
    bad = 0
    count = 0

    def arm(name, got, want):
        nonlocal bad, count
        count += 1
        if got != want:
            bad += 1
            print("SELFTEST FAIL %s: got %r want %r" % (name, got, want))

    cw = {"pairs": [{"transaction_type": "Buy", "transaction_sub_type": "Buy", "external_flow": {"None": 3, "Contribution": 1}},
                    {"transaction_type": "Cash", "transaction_sub_type": "Deposit", "external_flow": {"Contribution": 5}}],
          "values": {"Action": {"Buy": 4, "Cash Deposit": 5}}}
    pairs, actions = domains(cw)
    arm("domains", (sorted(pairs), actions, sorted(pairs["Buy | Buy"])), (["Buy | Buy", "Cash | Deposit"], ["Buy", "Cash Deposit"], ["Contribution", "None"]))
    rec = {"mapping": [
        {"firm": "cottonwood", "field": "type_pair", "source_value": "Buy | Buy", "opal_type": "Buy", "flow_class_none": "INTERNAL"},
        {"firm": "cottonwood", "field": "type_pair", "source_value": "Cash | Deposit", "opal_type": "Deposit", "flow_class_none": None},
        {"firm": "cottonwood", "field": "action", "source_value": "Buy", "opal_action": "Trade"},
        {"firm": "cottonwood", "field": "action", "source_value": "Cash Deposit", "opal_action": UNMAPPED, "reason": "x"}]}
    arm("sub-green", subtraction("type_pair", list(pairs), rec) + subtraction("action", actions, rec), [])
    arm("rows-green", row_problems(pairs, ["Buy", "Deposit"], ["Trade"], rec), [])
    arm("sub-missing", len(subtraction("action", actions, {"mapping": rec["mapping"][:3]})), 1)
    arm("sub-dup", len(subtraction("action", actions, {"mapping": rec["mapping"] + rec["mapping"][2:3]})), 1)
    arm("flow-none-needed", len(row_problems(pairs, ["Buy", "Deposit"], ["Trade"],
                                             {"mapping": [dict(rec["mapping"][0], flow_class_none=None)] + rec["mapping"][1:]})), 1)
    arm("flow-none-forbidden", len(row_problems(pairs, ["Buy", "Deposit"], ["Trade"],
                                                {"mapping": [rec["mapping"][0], dict(rec["mapping"][1], flow_class_none="INTERNAL")] + rec["mapping"][2:]})), 1)
    arm("undefined-word", len(row_problems(pairs, ["Deposit"], ["Trade"], rec)), 1)
    arm("counts", counts(rec), ({"Buy": 1, "Deposit": 1}, {"Trade": 1, UNMAPPED: 1}))
    arm("digits-red", digits_ok({"words": "id 12345678901"}), False)
    arm("form-red", form_problems({"as_of": "x"})[0].startswith("top-level"), True)
    print("selftest %s" % ("FAIL" if bad else "PASS (%d arms)" % count))
    return 1 if bad else 0


def main(argv):
    if len(argv) == 2 and argv[1] == "--selftest":
        return selftest()
    if len(argv) != 3:
        print(__doc__)
        return 2
    root, ac = argv[1], argv[2]
    table = {"DBF128-2-AC1": ac_subtraction, "DBF128-2-AC2": ac_law}
    if ac not in table:
        print("%s FAIL (unknown criterion)" % ac)
        return 1
    try:
        table[ac](root)
    except Fail as e:
        print("reason: %s" % e)
        print("%s FAIL" % ac)
        return 1
    except Exception as e:  # noqa: BLE001
        print("reason: %s: %s" % (type(e).__name__, e))
        print("%s FAIL" % ac)
        return 1
    print("%s PASS" % ac)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
