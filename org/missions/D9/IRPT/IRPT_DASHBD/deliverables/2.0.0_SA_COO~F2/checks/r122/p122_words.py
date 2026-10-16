"""IRPT_DASHBD round 122, workstream F-SHIP ~F2 (issuer 2.0.0_SA_COO~F2) -- FWD-5: Opal's action and type words, the rule-24 proposal.

  DB-f-802 (~802) a PROPOSAL record: Opal's closed set of transaction type words (each carrying its action and flow class), the
                  per-firm mapping of EVERY source value in RD_FWD5_FIELDS_R120.json to one Opal type word or to UNMAPPED with a
                  reason, and the taxonomy-law record (four postulates and a word-boundary census) over the measured denominator.
                  DBF122-1-AC1 (the subtraction: every source value mapped exactly once, none invented), AC2 (the law record and hygiene)

The checker computes the subtraction itself from the round-120 record (the denominator), so a source value with no row, a row with
no source value, a duplicate row, or a word used but not defined fails the proposal.

Usage: python <this file> <repo_root> <criterion_id>      prints "<id> PASS" or "<id> FAIL" last
       python <this file> --selftest                        the pure helpers on synthetic arms
"""
import json
import re
import sys
from pathlib import Path

D = "org/missions/D9/IRPT/IRPT_DASHBD/deliverables/"
DENOM = D + "0.9.0_WK_IRPT_DASHBD~701/RD_FWD5_FIELDS_R120.json"
PROP = D + "0.9.0_WK_IRPT_DASHBD~802/FWD5_WORDS_PROPOSAL_R121.json"
CLAIMS = ("measured", "inferred", "held", "absent")
UNMAPPED = "UNMAPPED"
LONG_DIGITS = re.compile(r"\d{8,}")
DIGIT_OK_KEYS = ("sha256", "path", "file", "key", "where", "vintage")
POSTULATES = ("mece", "same_grain", "intent_coherence", "state_coherence")
KEYS = ("as_of", "claim", "postulates", "opal_actions", "opal_types", "mapping", "census", "reads", "files_in_repo",
        "served_values_changed", "pushed", "deployed")
ZERO_READS = {"s3_reads": 0, "s3_writes": 0, "dynamodb_writes": 0, "vendor_calls": 0, "secret_reads": 0}
WORD = re.compile(r"^[A-Za-z][A-Za-z ]{1,40}$")


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


def is_ascii(obj):
    return json.dumps(obj, ensure_ascii=False).isascii()


def denominator(rd):
    """The (firm, field, source_value) triples the round-120 record holds: the population the proposal must cover."""
    out = []
    for f in rd["firms"]:
        for v in f["action_codes"]:
            out.append((f["firm"], "action", v))
        for v in f["type_codes"]:
            out.append((f["firm"], "type", v))
    return out


def mapping_triples(mapping):
    return [(m.get("firm"), m.get("field"), m.get("source_value")) for m in mapping]


def subtraction(rd, prop):
    """Problems of the mapping against the denominator: missing, extra and duplicate triples."""
    pr = []
    den = denominator(rd)
    got = mapping_triples(prop["mapping"])
    missing = [t for t in den if t not in got]
    extra = [t for t in got if t not in den]
    dup = sorted({t for t in got if got.count(t) > 1}, key=repr)
    if missing:
        pr.append("source values with no mapping row: %d (first %r)" % (len(missing), missing[0]))
    if extra:
        pr.append("mapping rows with no source value: %d (first %r)" % (len(extra), extra[0]))
    if dup:
        pr.append("duplicate mapping rows: %d (first %r)" % (len(dup), dup[0]))
    return pr


def word_problems(prop):
    """Every mapped word is defined; UNMAPPED carries a reason; each type word carries a defined action and a flow class."""
    pr = []
    acts = prop["opal_actions"]
    types = prop["opal_types"]
    if not (isinstance(acts, list) and acts and all(isinstance(a, dict) and isinstance(a.get("word"), str)
                                                    and WORD.match(a["word"]) and isinstance(a.get("definition"), str)
                                                    and a["definition"].strip() for a in acts)):
        return ["opal_actions form"]
    act_words = [a["word"] for a in acts]
    if len(set(act_words)) != len(act_words):
        pr.append("opal_actions has a duplicate word")
    ok_types = (isinstance(types, list) and types and all(
        isinstance(t, dict) and isinstance(t.get("word"), str) and WORD.match(t["word"]) and isinstance(t.get("definition"), str)
        and t["definition"].strip() and t.get("action") in act_words and isinstance(t.get("flow_class"), str) and t["flow_class"]
        for t in types))
    if not ok_types:
        return pr + ["opal_types form (each needs word, definition, an action from opal_actions, a flow_class)"]
    type_words = [t["word"] for t in types]
    if len(set(type_words)) != len(type_words):
        pr.append("opal_types has a duplicate word")
    for i, m in enumerate(prop["mapping"]):
        if not (isinstance(m, dict) and m.get("firm") in ("49financial", "cottonwood", "inflection")
                and m.get("field") in ("action", "type") and isinstance(m.get("source_value"), str) and m["source_value"]):
            pr.append("mapping row %d form" % (i + 1))
            continue
        target = m.get("opal_type") if m["field"] == "type" else m.get("opal_action")
        if target == UNMAPPED:
            if not (isinstance(m.get("reason"), str) and m["reason"].strip()):
                pr.append("mapping row %d is UNMAPPED with no reason" % (i + 1))
        elif m["field"] == "type" and target not in type_words:
            pr.append("mapping row %d uses an undefined type word %r" % (i + 1, target))
        elif m["field"] == "action" and target not in act_words:
            pr.append("mapping row %d uses an undefined action word %r" % (i + 1, target))
    return pr


def counts_by_word(prop):
    c = {}
    for m in prop["mapping"]:
        if m.get("field") == "type":
            c[m.get("opal_type")] = c.get(m.get("opal_type"), 0) + 1
    return c


def census_problems(rd, prop):
    pr = []
    c = prop["census"]
    if not isinstance(c, dict):
        return ["census form"]
    den = denominator(rd)
    if c.get("denominator_total") != len(den):
        pr.append("census.denominator_total is not the round-120 population (%d)" % len(den))
    if c.get("method") != "word-boundary":
        pr.append("census.method is not word-boundary")
    flow = rd["brief_flow_classes"]["count"]
    if c.get("brief_flow_classes") != flow:
        pr.append("census.brief_flow_classes is not the round-120 count (%d)" % flow)
    if c.get("per_type_word") != counts_by_word(prop):
        pr.append("census.per_type_word does not equal the count computed from the mapping")
    unm = sum(1 for m in prop["mapping"] if (m.get("opal_type") == UNMAPPED or m.get("opal_action") == UNMAPPED))
    if c.get("unmapped") != unm:
        pr.append("census.unmapped is not the count computed from the mapping (%d)" % unm)
    return pr


def form_problems(prop):
    pr = []
    if not isinstance(prop, dict) or sorted(prop.keys()) != sorted(KEYS):
        return ["top-level fields are not exactly " + repr(KEYS)]
    if not (isinstance(prop["as_of"], str) and re.match(r"\d{4}-\d{2}-\d{2}$", prop["as_of"])):
        pr.append("as_of not an ISO date")
    if prop["claim"] not in CLAIMS:
        pr.append("claim not in the four-word set")
    po = prop["postulates"]
    if not (isinstance(po, dict) and sorted(po.keys()) == sorted(POSTULATES)
            and all(isinstance(po[k], str) and len(po[k].strip()) >= 40 for k in POSTULATES)):
        pr.append("postulates must be exactly %r, each at least 40 characters" % (POSTULATES,))
    if prop["reads"] != ZERO_READS:
        pr.append("reads block is not the all-zero form")
    for k in ("files_in_repo", "served_values_changed", "pushed", "deployed"):
        if prop[k] is not False:
            pr.append(k + " is not false")
    if not digits_ok(prop):
        pr.append("a run of 8 or more digits outside the exempt fields")
    if not is_ascii(prop):
        pr.append("non-ASCII text")
    if not (isinstance(prop["mapping"], list) and prop["mapping"]):
        pr.append("mapping is empty")
    return pr


def ac_subtraction(root):
    rd, prop = load(root, DENOM), load(root, PROP)
    pr = form_problems(prop)
    need(not pr, "; ".join(pr))
    pr = subtraction(rd, prop) + word_problems(prop)
    need(not pr, "; ".join(pr[:6]))


def ac_law(root):
    rd, prop = load(root, DENOM), load(root, PROP)
    pr = form_problems(prop) + census_problems(rd, prop)
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

    rd = {"firms": [{"firm": "49financial", "action_codes": ["TR"], "type_codes": ["DV", "WD"]},
                    {"firm": "cottonwood", "action_codes": [], "type_codes": ["Buy"]}],
          "brief_flow_classes": {"count": 2}}
    good = {"mapping": [
        {"firm": "49financial", "field": "action", "source_value": "TR", "opal_action": "Trade"},
        {"firm": "49financial", "field": "type", "source_value": "DV", "opal_type": "Dividend"},
        {"firm": "49financial", "field": "type", "source_value": "WD", "opal_type": UNMAPPED, "reason": "marker only"},
        {"firm": "cottonwood", "field": "type", "source_value": "Buy", "opal_type": "Buy"}],
        "opal_actions": [{"word": "Trade", "definition": "a buy or a sell"}],
        "opal_types": [{"word": "Dividend", "definition": "income paid", "action": "Trade", "flow_class": "INCOME"},
                       {"word": "Buy", "definition": "a purchase", "action": "Trade", "flow_class": "TRADE"}],
        "census": {"denominator_total": 4, "method": "word-boundary", "brief_flow_classes": 2,
                   "per_type_word": {"Dividend": 1, UNMAPPED: 1, "Buy": 1}, "unmapped": 1}}
    arm("denominator", len(denominator(rd)), 4)
    arm("subtraction-green", subtraction(rd, good), [])
    arm("words-green", word_problems(good), [])
    arm("census-green", census_problems(rd, good), [])
    short = dict(good, mapping=good["mapping"][1:])
    arm("subtraction-missing", len(subtraction(rd, short)), 1)
    dup = dict(good, mapping=good["mapping"] + [good["mapping"][0]])
    arm("subtraction-dup", len(subtraction(rd, dup)), 1)
    undefined = dict(good, mapping=[dict(good["mapping"][0])] + [dict(good["mapping"][1], opal_type="Nope")] + good["mapping"][2:])
    arm("word-undefined", len(word_problems(undefined)), 1)
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
    table = {"DBF122-1-AC1": ac_subtraction, "DBF122-1-AC2": ac_law}
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
