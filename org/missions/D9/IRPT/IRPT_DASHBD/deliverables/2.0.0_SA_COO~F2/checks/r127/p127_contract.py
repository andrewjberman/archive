"""IRPT_DASHBD round 127, workstream F-SHIP ~F2 (issuer 2.0.0_SA_COO~F2) -- FWD-5: the TRANSACTION CONTRACT and its mapping data file.

  DB-f-1301 (~1301) the sole writer's contract `org/standards/IRPT_DASHBD_ACCOUNT_TRANSACTION_CONTRACT.json` (table account_transaction,
                    the 14 brief columns plus the grain columns, claims per column, the ratified enums, the per-code source mapping
                    with each code's flow class) and the same mapping as the producer's data file
                    `data/assets/scripts/gold/irpt_reporting/transaction_words.json`.
                    DBF127-1-AC1 (the contract's form, columns, claims and schema hash), DBF127-1-AC2 (the mapping against the ratified
                    proposal and the CRO table, the flow-class rule, the data file)

The checker recomputes: the schema hash from the columns; the mapping's words from the ratified proposal (round 124); every 49 Financial
code's flow class from the contract's own flow_class_rule applied to the CRO table's (partition, rule) pairs (a code whose rows disagree
is UNRESOLVED); and holds the issuer's rule table, the three silver-only decisions and IRAWH / MCE as fixed points.

Usage: python <this file> <repo_root> <criterion_id>      prints "<id> PASS" or "<id> FAIL" last
       python <this file> --selftest                        the pure helpers on synthetic arms
"""
import hashlib
import json
import sys
from pathlib import Path

D = "org/missions/D9/IRPT/IRPT_DASHBD/deliverables/"
CONTRACT = "org/standards/IRPT_DASHBD_ACCOUNT_TRANSACTION_CONTRACT.json"
DATA = "data/assets/scripts/gold/irpt_reporting/transaction_words.json"
PROPOSAL = D + "0.9.0_WK_IRPT_DASHBD~1001/FWD5_WORDS_PROPOSAL_R124.json"
CENSUS = D + "2.0.0_SA_COO~F2/R124_LIVE_SILVER_CENSUS_49F.json"
CRO = "org/tier1_exec/4.0.0_SA_CRO/deliverables/SCHWAB_TRANSACTION_CODE_CLASSIFICATION_20260811.json"
FIRM49 = "49financial"
UNMAPPED = "UNMAPPED"
CLAIMS = ("measured", "inferred", "held", "absent")
FLOW = ("EXTERNAL_IN", "EXTERNAL_OUT", "INCOME", "FEE", "INTERNAL", "CORPORATE_ACTION", "UNRESOLVED")
COLUMNS = ("firm", "account_id", "business_date", "trade_date", "settle_date", "action", "txn_type", "symbol", "asset_name", "units",
           "price", "amount", "fee", "custodian", "flow_class", "source_txn_id", "coverage")
TYPES = ("string", "date32[day]", "double")
ABSENT_COLUMNS = ("settle_date", "asset_name", "fee", "source_txn_id")
COVERAGE = ("MEASURED", "CODE_NOT_IN_MAPPING", "UNMAPPED_BY_TABLE")
KEYS = ("contract_version", "project", "prd", "authored_by", "authored_under", "table", "grain", "partition", "producer", "columns",
        "enums", "type_action", "flow_class_rule", "source_mapping", "unmapped_display", "new_code_reason", "firms_served",
        "firms_pending", "rule24_record", "schema_hash", "schema_hash_basis", "served", "served_note")
# The issuer's rule: the CRO table's (partition, rule) pair to the brief's seven flow classes (the 30 pairs of the 2026-08-11 table).
EXPECTED_RULE = {
    ("CONDITIONAL-BY-COUNTERPARTY", "acct-transfer"): "UNRESOLVED", ("CONDITIONAL-BY-COUNTERPARTY", "journals"): "UNRESOLVED",
    ("CONDITIONAL-BY-COUNTERPARTY", "shares-delivered"): "UNRESOLVED", ("EXTERNAL", "checks-classified"): "UNRESOLVED",
    ("EXTERNAL", "returned-deposits"): "UNRESOLVED", ("EXTERNAL-IN", "deposits"): "EXTERNAL_IN",
    ("EXTERNAL-OUT", "ira-withholding"): "EXTERNAL_OUT", ("EXTERNAL-OUT", "schwab-checks-out"): "EXTERNAL_OUT",
    ("EXTERNAL-OUT", "withdrawals"): "EXTERNAL_OUT", ("FEE-ADMIN", "adr-fee"): "FEE", ("FEE-ADMIN", "service-fees"): "FEE",
    ("FEE-MANAGEMENT", "advisor-fee-explicit"): "FEE", ("FEE-MANAGEMENT", "advisory-fee"): "FEE",
    ("FEE-MANAGEMENT-VERIFIED", "advisor-fee-verified"): "FEE", ("INTERNAL", "alt-income"): "INCOME",
    ("INTERNAL", "cash-in-lieu"): "CORPORATE_ACTION", ("INTERNAL", "corp-actions"): "CORPORATE_ACTION",
    ("INTERNAL", "corp-actions-ic"): "CORPORATE_ACTION", ("INTERNAL", "corp-misc"): "CORPORATE_ACTION",
    ("INTERNAL", "dividends"): "INCOME", ("INTERNAL", "foreign-tax"): "INTERNAL", ("INTERNAL", "int-adj-fc"): "INCOME",
    ("INTERNAL", "interest"): "INCOME", ("INTERNAL", "reinvest"): "INTERNAL", ("INTERNAL", "sweeps"): "INTERNAL",
    ("INTERNAL", "trades"): "INTERNAL", ("INTERNAL", "withholding"): "INTERNAL", ("UNRESOLVED", "no-rule"): "UNRESOLVED",
    ("UNRESOLVED-PENDING-SPECIMEN", "lending-misc-ic"): "UNRESOLVED", ("UNRESOLVED-PENDING-SPECIMEN", "misc-adj"): "UNRESOLVED",
}
SILVER_ONLY_FLOW = {"EXWT": "CORPORATE_ACTION", "RDPC": "CORPORATE_ACTION", "SQDAJ": "UNRESOLVED"}
FIXED_POINTS = {"IRAWH": "EXTERNAL_OUT", "MCE": "EXTERNAL_OUT"}


class Fail(Exception):
    pass


def need(cond, msg):
    if not cond:
        raise Fail(msg)


def load(root, rel):
    p = Path(root) / rel
    need(p.is_file(), "missing file " + rel)
    return json.loads(p.read_text(encoding="utf-8"))


def schema_hash(columns):
    lines = sorted("%s:%s" % (c["name"], c["type"]) for c in columns)
    return hashlib.sha256("\n".join(lines).encode("ascii")).hexdigest()


def column_problems(cols):
    if not (isinstance(cols, list) and [c.get("name") if isinstance(c, dict) else None for c in cols] == list(COLUMNS)):
        return ["columns must be exactly, in order: " + ", ".join(COLUMNS)]
    pr = []
    for c in cols:
        n = c["name"]
        if c.get("type") not in TYPES:
            pr.append("%s: type not in %r" % (n, TYPES))
        if not isinstance(c.get("nullable"), bool):
            pr.append("%s: nullable not a boolean" % n)
        if c.get("claim") not in CLAIMS:
            pr.append("%s: claim not in the four-word set" % n)
        if not (isinstance(c.get("meaning"), str) and c["meaning"].strip()):
            pr.append("%s: meaning" % n)
        if c.get("claim") == "inferred" and not (isinstance(c.get("method"), str) and c["method"].strip()):
            pr.append("%s: an inferred column needs a method" % n)
        if n in ABSENT_COLUMNS and not (c.get("claim") == "absent" and c.get("nullable") is True):
            pr.append("%s: must be claim absent and nullable (the round-123 ground read)" % n)
        if n not in ABSENT_COLUMNS and c.get("claim") == "absent":
            pr.append("%s: a column the producer fills is never labelled absent (CTO round-123 ruling 1)" % n)
    return pr


def form_problems(con):
    if not isinstance(con, dict) or sorted(con.keys()) != sorted(KEYS):
        return ["contract fields are not exactly " + repr(KEYS)]
    pr = []
    if con["contract_version"] != "0.1.0" or con["table"] != "account_transaction":
        pr.append("contract_version must be 0.1.0 and table account_transaction")
    if con["partition"] != "date=YYYY-MM-DD":
        pr.append("partition must be date=YYYY-MM-DD")
    pr += column_problems(con["columns"])
    if isinstance(con["columns"], list) and all(isinstance(c, dict) and "name" in c and "type" in c for c in con["columns"]):
        if con["schema_hash"] != schema_hash(con["columns"]):
            pr.append("schema_hash is not the sha256 over the sorted name:type lines")
    en = con["enums"]
    if not (isinstance(en, dict) and sorted(en.keys()) == ["action", "coverage", "flow_class", "txn_type"]):
        pr.append("enums must hold exactly txn_type, action, flow_class, coverage")
    else:
        if tuple(en["flow_class"]) != FLOW:
            pr.append("enums.flow_class must be the brief's seven classes, in this order: " + ", ".join(FLOW))
        if tuple(en["coverage"]) != COVERAGE:
            pr.append("enums.coverage must be " + ", ".join(COVERAGE))
    if con["unmapped_display"] != "Other" or con["new_code_reason"] != "CODE_NOT_IN_MAPPING":
        pr.append("unmapped_display must be Other and new_code_reason CODE_NOT_IN_MAPPING (CTO round-124 ruling)")
    if con["firms_served"] != [FIRM49]:
        pr.append("firms_served must be [49financial]")
    fp = con["firms_pending"]
    if not (isinstance(fp, list) and sorted(x.get("firm") for x in fp if isinstance(x, dict)) == ["cottonwood", "inflection"]
            and all(isinstance(x.get("reason"), str) and x["reason"].strip() for x in fp)):
        pr.append("firms_pending must name cottonwood and inflection, each with a reason")
    if con["served"] is not False:
        pr.append("served must be false")
    if not json.dumps(con, ensure_ascii=False).isascii():
        pr.append("non-ASCII text")
    return pr


def proposal_vocab(prop):
    return ([t["word"] for t in prop["opal_types"]], [a["word"] for a in prop["opal_actions"]],
            {t["word"]: t["action"] for t in prop["opal_types"]})


def rule_problems(con):
    got = {}
    for r in con["flow_class_rule"] if isinstance(con["flow_class_rule"], list) else []:
        if isinstance(r, dict):
            got[(r.get("partition"), r.get("rule"))] = (r.get("flow_class"), r.get("reason"))
    pr = []
    if set(got) != set(EXPECTED_RULE):
        pr.append("flow_class_rule must hold exactly the 30 (partition, rule) pairs of the CRO table (missing %d, extra %d)"
                  % (len(set(EXPECTED_RULE) - set(got)), len(set(got) - set(EXPECTED_RULE))))
        return pr
    for k, want in EXPECTED_RULE.items():
        if got[k][0] != want:
            pr.append("flow_class_rule %r is %r, the issuer's rule says %r" % (k, got[k][0], want))
        if not (isinstance(got[k][1], str) and got[k][1].strip()):
            pr.append("flow_class_rule %r needs a reason" % (k,))
    return pr


def expected_flow(cro_rows):
    """{tran_srcde: flow class} by the issuer's rule: one class when every CRO row of the code agrees, else UNRESOLVED."""
    cls = {}
    for r in cro_rows:
        cls.setdefault(r["tran_srcde"], set()).add(EXPECTED_RULE[(r["partition"], r["rule"])])
    return {c: (next(iter(s)) if len(s) == 1 else "UNRESOLVED") for c, s in cls.items()}


def mapping_problems(con, prop, cro_rows, census):
    pr = []
    types, acts, type_action = proposal_vocab(prop)
    en = con["enums"]
    if sorted(en["txn_type"]) != sorted(types) or sorted(en["action"]) != sorted(acts):
        pr.append("enums.txn_type / enums.action are not the ratified proposal's words")
    ta = con["type_action"]
    if ta != type_action:
        pr.append("type_action is not the ratified proposal's type-to-action table")
    rows = con["source_mapping"]
    if not (isinstance(rows, list) and rows):
        return pr + ["source_mapping is empty"]
    want = {(m["firm"], m["source_value"]): m["opal_type"] for m in prop["mapping"]}
    got = {}
    for m in rows:
        key = (m.get("firm"), m.get("source_value"))
        if key in got:
            pr.append("duplicate source_mapping row %r" % (key,))
        got[key] = m
    if {k: v["opal_type"] for k, v in got.items()} != want:
        pr.append("source_mapping words differ from the ratified proposal (%d rows against %d)" % (len(got), len(want)))
    ef = expected_flow(cro_rows)
    ef.update(SILVER_ONLY_FLOW)
    for (firm, code), m in got.items():
        if firm == FIRM49:
            if m.get("flow_class") != ef.get(code):
                pr.append("49financial %r: flow_class %r, the rule gives %r" % (code, m.get("flow_class"), ef.get(code)))
        elif m.get("flow_class") is not None:
            pr.append("%s %r: flow_class must be null until that firm's producer lands" % (firm, code))
    for code, want_class in FIXED_POINTS.items():
        if got.get((FIRM49, code), {}).get("flow_class") != want_class:
            pr.append("%s must be %s (CTO round-124 ruling)" % (code, want_class))
    live = set(census["codes"])
    n49 = sum(1 for k in got if k[0] == FIRM49)
    if n49 != len(live):
        pr.append("49financial rows are %d, the live census has %d codes" % (n49, len(live)))
    return pr


def data_problems(con, data):
    pr = []
    if not isinstance(data, dict):
        return ["data file form"]
    if data.get("source_mapping") != con["source_mapping"] or data.get("type_action") != con["type_action"]:
        pr.append("transaction_words.json source_mapping / type_action differ from the contract's")
    if data.get("contract_version") != con["contract_version"]:
        pr.append("transaction_words.json contract_version differs")
    return pr


def ac_form(root):
    con = load(root, CONTRACT)
    pr = form_problems(con)
    need(not pr, "; ".join(pr[:6]))


def ac_mapping(root):
    con = load(root, CONTRACT)
    need(not form_problems(con), "the contract's form must pass DBF127-1-AC1 first")
    pr = rule_problems(con) + mapping_problems(con, load(root, PROPOSAL), load(root, CRO), load(root, CENSUS))
    pr += data_problems(con, load(root, DATA))
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

    arm("rule-pairs", len(EXPECTED_RULE), 30)
    arm("flow-values", sorted(set(EXPECTED_RULE.values()) - set(FLOW)), [])
    cro = [{"tran_srcde": "A", "partition": "INTERNAL", "rule": "dividends"},
           {"tran_srcde": "B", "partition": "INTERNAL", "rule": "dividends"},
           {"tran_srcde": "B", "partition": "EXTERNAL-IN", "rule": "deposits"}]
    arm("expected-flow", expected_flow(cro), {"A": "INCOME", "B": "UNRESOLVED"})
    cols = [{"name": n, "type": "string"} for n in COLUMNS]
    arm("hash", schema_hash(cols) == schema_hash(list(reversed(cols))), True)
    arm("columns-red", column_problems([{"name": "x"}])[0].startswith("columns must be"), True)
    ok = [{"name": n, "type": "string", "nullable": n in ABSENT_COLUMNS, "meaning": "m",
           "claim": "absent" if n in ABSENT_COLUMNS else "measured"} for n in COLUMNS]
    arm("columns-green", column_problems(ok), [])
    bad_abs = [dict(c) for c in ok]
    bad_abs[0]["claim"] = "absent"
    arm("filled-never-absent", len(column_problems(bad_abs)), 1)
    no_method = [dict(c) for c in ok]
    no_method[1]["claim"] = "inferred"
    arm("inferred-needs-method", len(column_problems(no_method)), 1)
    arm("fixed-points", sorted(FIXED_POINTS), ["IRAWH", "MCE"])
    arm("form-red", form_problems({"a": 1})[0].startswith("contract fields"), True)
    print("selftest %s" % ("FAIL" if bad else "PASS (%d arms)" % count))
    return 1 if bad else 0


def main(argv):
    if len(argv) == 2 and argv[1] == "--selftest":
        return selftest()
    if len(argv) != 3:
        print(__doc__)
        return 2
    root, ac = argv[1], argv[2]
    table = {"DBF127-1-AC1": ac_form, "DBF127-1-AC2": ac_mapping}
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
