"""IRPT_DASHBD round 124, workstream F-SHIP ~F2 (issuer 2.0.0_SA_COO~F2) -- FWD-5: the REVISED words proposal, 49 Financial at tran_srcde grain.

  DB-f-1001 (~1001) the CTO's round-122 analysis (not ratified; the CVO's rule-24 grade holds) orders one record cell: 49 Financial
                    mapped at tran_srcde grain (all 157 codes of the CRO classification table, each to one Opal type word or to
                    UNMAPPED with a reason), state coherence per word, Cottonwood and Inflection carried over unchanged, and the
                    census repeated.                                                     DBF124-1-AC1 (the subtraction and the carry-over), AC2 (the law record)

The checker computes the 49 Financial denominator FROM THE CRO TABLE ITSELF (distinct tran_srcde), the carry-over from the round-122
proposal, and the per-code CRO rules, so a missing code, a changed carried row, a code mapped over disagreeing CRO rules without a
stated reason, or a census that does not match the mapping fails.

Usage: python <this file> <repo_root> <criterion_id>      prints "<id> PASS" or "<id> FAIL" last
       python <this file> --selftest                        the pure helpers on synthetic arms
"""
import json
import re
import sys
from pathlib import Path

D = "org/missions/D9/IRPT/IRPT_DASHBD/deliverables/"
CRO = "org/tier1_exec/4.0.0_SA_CRO/deliverables/SCHWAB_TRANSACTION_CODE_CLASSIFICATION_20260811.json"
OLD = D + "0.9.0_WK_IRPT_DASHBD~802/FWD5_WORDS_PROPOSAL_R121.json"
NEW = D + "0.9.0_WK_IRPT_DASHBD~1001/FWD5_WORDS_PROPOSAL_R124.json"
CLAIMS = ("measured", "inferred", "held", "absent")
UNMAPPED = "UNMAPPED"
LONG_DIGITS = re.compile(r"\d{8,}")
DIGIT_OK_KEYS = ("sha256", "path", "file", "key", "where", "vintage")
POSTULATES = ("mece", "same_grain", "intent_coherence", "state_coherence")
KEYS = ("as_of", "claim", "postulates", "state_coherence_by_word", "unmapped_policy", "cross_firm_statement", "opal_actions",
        "opal_types", "mapping", "census", "reads", "files_in_repo", "served_values_changed", "pushed", "deployed")
ZERO_READS = {"s3_reads": 0, "s3_writes": 0, "dynamodb_writes": 0, "vendor_calls": 0, "secret_reads": 0}
WORD = re.compile(r"^[A-Za-z][A-Za-z ]{1,40}$")
FIRM49 = "49financial"
CARRIED = ("cottonwood", "inflection")


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


def cro_codes(cro_rows):
    """{tran_srcde: sorted list of distinct CRO rules} over the CRO table: the 49 Financial denominator."""
    out = {}
    for r in cro_rows:
        out.setdefault(r["tran_srcde"], set()).add(r["rule"])
    return {k: sorted(v) for k, v in out.items()}


def rows_of(prop, firm):
    return [m for m in prop["mapping"] if isinstance(m, dict) and m.get("firm") == firm]


def target_of(m):
    return m.get("opal_type")


def subtraction_49(codes, prop):
    pr = []
    got = [m.get("source_value") for m in rows_of(prop, FIRM49)]
    bad_field = [m for m in rows_of(prop, FIRM49) if m.get("field") != "tran_srcde"]
    if bad_field:
        pr.append("49financial rows must carry field tran_srcde (%d do not)" % len(bad_field))
    missing = [c for c in codes if c not in got]
    extra = [c for c in got if c not in codes]
    dup = sorted({c for c in got if got.count(c) > 1})
    if missing:
        pr.append("tran_srcde codes with no mapping row: %d (first %r)" % (len(missing), missing[0]))
    if extra:
        pr.append("rows with no CRO code: %d (first %r)" % (len(extra), extra[0]))
    if dup:
        pr.append("duplicate rows: %d (first %r)" % (len(dup), dup[0]))
    return pr


def carry_over(old, new):
    """Cottonwood and Inflection rows must be the round-122 rows, unchanged."""
    pr = []
    for firm in CARRIED:
        a = sorted(json.dumps(m, sort_keys=True) for m in rows_of(old, firm))
        b = sorted(json.dumps(m, sort_keys=True) for m in rows_of(new, firm))
        if a != b:
            pr.append("%s rows differ from the round-122 proposal (%d before, %d now)" % (firm, len(a), len(b)))
    return pr


def row_problems(codes, prop):
    """Word definitions, UNMAPPED reasons, and the per-code CRO rules; a multi-rule code mapped to a word needs a stated reason."""
    pr = []
    type_words = [t.get("word") for t in prop["opal_types"] if isinstance(t, dict)]
    for i, m in enumerate(rows_of(prop, FIRM49)):
        code = m.get("source_value")
        if code not in codes:
            continue
        if m.get("cro_rules") != codes[code]:
            pr.append("row %r: cro_rules is not the CRO table's distinct rules %r" % (code, codes[code]))
        t = target_of(m)
        has_reason = isinstance(m.get("reason"), str) and m["reason"].strip() != ""
        if t == UNMAPPED:
            if not has_reason:
                pr.append("row %r is UNMAPPED with no reason" % code)
        elif t not in type_words:
            pr.append("row %r uses an undefined type word %r" % (code, t))
        elif len(codes[code]) > 1 and not has_reason:
            pr.append("row %r spans %d CRO rules and is mapped to one word with no stated reason" % (code, len(codes[code])))
    return pr


def census_problems(codes, old, prop):
    pr = []
    c = prop["census"]
    if not isinstance(c, dict):
        return ["census form"]
    n49 = len(codes)
    ncw = len(rows_of(prop, "cottonwood"))
    nin = len(rows_of(prop, "inflection"))
    if c.get("method") != "word-boundary":
        pr.append("census.method is not word-boundary")
    if c.get("denominators") != {FIRM49: n49, "cottonwood": ncw, "inflection": nin}:
        pr.append("census.denominators is not {49financial: %d, cottonwood: %d, inflection: %d}" % (n49, ncw, nin))
    if c.get("denominator_total") != n49 + ncw + nin:
        pr.append("census.denominator_total is not %d" % (n49 + ncw + nin))
    if c.get("cro_rows") is None or c.get("cro_distinct_tran_srcde") != n49:
        pr.append("census.cro_distinct_tran_srcde is not %d" % n49)
    counts = {}
    for m in prop["mapping"]:
        if isinstance(m, dict) and m.get("field") in ("type", "tran_srcde"):
            counts[target_of(m)] = counts.get(target_of(m), 0) + 1
    if c.get("per_type_word") != counts:
        pr.append("census.per_type_word does not equal the count computed from the mapping")
    unm = counts.get(UNMAPPED, 0)
    if c.get("unmapped") != unm:
        pr.append("census.unmapped is not the count computed from the mapping (%d)" % unm)
    return pr


def definition_problems(prop):
    pr = []
    acts = prop["opal_actions"]
    types = prop["opal_types"]
    if not (isinstance(acts, list) and acts and all(isinstance(a, dict) and isinstance(a.get("word"), str) and WORD.match(a["word"])
                                                    and isinstance(a.get("definition"), str) and a["definition"].strip() for a in acts)):
        return ["opal_actions form"]
    act_words = [a["word"] for a in acts]
    ok = (isinstance(types, list) and types and all(
        isinstance(t, dict) and isinstance(t.get("word"), str) and WORD.match(t["word"]) and isinstance(t.get("definition"), str)
        and t["definition"].strip() and t.get("action") in act_words and isinstance(t.get("flow_class"), str) and t["flow_class"]
        for t in types))
    if not ok:
        return ["opal_types form (each needs word, definition, an action from opal_actions, a flow_class)"]
    words = [t["word"] for t in types]
    if len(set(words)) != len(words):
        pr.append("opal_types has a duplicate word")
    sc = prop["state_coherence_by_word"]
    if not (isinstance(sc, dict) and sorted(sc.keys()) == sorted(words + [UNMAPPED])
            and all(isinstance(v, str) and len(v.strip()) >= 20 for v in sc.values())):
        pr.append("state_coherence_by_word must have exactly one string (20+ characters) per type word and one for UNMAPPED")
    return pr


def form_problems(prop):
    if not isinstance(prop, dict) or sorted(prop.keys()) != sorted(KEYS):
        return ["top-level fields are not exactly " + repr(KEYS)]
    pr = []
    if not (isinstance(prop["as_of"], str) and re.match(r"\d{4}-\d{2}-\d{2}$", prop["as_of"])):
        pr.append("as_of not an ISO date")
    if prop["claim"] not in CLAIMS:
        pr.append("claim not in the four-word set")
    po = prop["postulates"]
    if not (isinstance(po, dict) and sorted(po.keys()) == sorted(POSTULATES)
            and all(isinstance(po[k], str) and len(po[k].strip()) >= 40 for k in POSTULATES)):
        pr.append("postulates must be exactly %r, each at least 40 characters" % (POSTULATES,))
    elif "tran_srcde" not in po["mece"] or "tran_srcde" not in po["same_grain"]:
        pr.append("the mece and same_grain postulates must name the tran_srcde domain")
    if prop["unmapped_policy"] not in ("shown", "excluded", "counted"):
        pr.append("unmapped_policy must be one of shown, excluded, counted")
    if not (isinstance(prop["cross_firm_statement"], str) and "another firm" in prop["cross_firm_statement"].lower()):
        pr.append("cross_firm_statement must say what remapping a code does to another firm's rows (the words 'another firm')")
    if prop["reads"] != ZERO_READS:
        pr.append("reads block is not the all-zero form")
    for k in ("files_in_repo", "served_values_changed", "pushed", "deployed"):
        if prop[k] is not False:
            pr.append(k + " is not false")
    if not digits_ok(prop):
        pr.append("a run of 8 or more digits outside the exempt fields")
    if not json.dumps(prop, ensure_ascii=False).isascii():
        pr.append("non-ASCII text")
    if not (isinstance(prop["mapping"], list) and prop["mapping"]):
        pr.append("mapping is empty")
    return pr


def ac_subtraction(root):
    codes = cro_codes(load(root, CRO))
    old, new = load(root, OLD), load(root, NEW)
    pr = form_problems(new)
    need(not pr, "; ".join(pr[:6]))
    pr = subtraction_49(codes, new) + carry_over(old, new) + row_problems(codes, new)
    need(not pr, "; ".join(pr[:6]))


def ac_law(root):
    codes = cro_codes(load(root, CRO))
    old, new = load(root, OLD), load(root, NEW)
    pr = form_problems(new) + definition_problems(new) + census_problems(codes, old, new)
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

    cro = [{"tran_srcde": "A", "rule": "r1"}, {"tran_srcde": "A", "rule": "r2"}, {"tran_srcde": "B", "rule": "r1"}]
    codes = cro_codes(cro)
    arm("codes", codes, {"A": ["r1", "r2"], "B": ["r1"]})
    row = lambda c, t, **k: dict({"firm": FIRM49, "field": "tran_srcde", "source_value": c, "opal_type": t,  # noqa: E731
                                  "cro_rules": codes.get(c)}, **k)
    prop = {"mapping": [row("A", "Fee", reason="rules disagree; fee wins"), row("B", UNMAPPED, reason="no meaning")],
            "opal_types": [{"word": "Fee"}]}
    arm("sub-green", subtraction_49(codes, prop), [])
    arm("rows-green", row_problems(codes, prop), [])
    arm("sub-missing", len(subtraction_49(codes, {"mapping": prop["mapping"][:1]})), 1)
    arm("sub-dup", len(subtraction_49(codes, {"mapping": prop["mapping"] + prop["mapping"][:1]})), 1)
    multi_noreason = {"mapping": [row("A", "Fee"), row("B", UNMAPPED, reason="x")], "opal_types": [{"word": "Fee"}]}
    arm("multi-rule-needs-reason", len(row_problems(codes, multi_noreason)), 1)
    wrong_rules = {"mapping": [dict(row("B", UNMAPPED, reason="x"), cro_rules=["zz"])], "opal_types": []}
    arm("cro-rules-checked", len(row_problems(codes, wrong_rules)), 1)
    old = {"mapping": [{"firm": "cottonwood", "source_value": "Buy"}, {"firm": "inflection", "source_value": "X"}]}
    arm("carry-green", carry_over(old, old), [])
    arm("carry-red", len(carry_over(old, {"mapping": [{"firm": "cottonwood", "source_value": "Sale"}, old["mapping"][1]]})), 1)
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
    table = {"DBF124-1-AC1": ac_subtraction, "DBF124-1-AC2": ac_law}
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
