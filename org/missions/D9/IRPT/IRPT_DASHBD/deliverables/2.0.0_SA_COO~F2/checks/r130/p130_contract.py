"""IRPT_DASHBD round 130, workstream F-SHIP ~F2 (issuer 2.0.0_SA_COO~F2) -- FWD-5: the TRANSACTION CONTRACT 0.3.0 (Cottonwood served).

  DB-f-1601 (~1601) 0.3.0 follows the CVO's J1 PASS of 0.2.0 (CTO round-129 analysis, msg 9211): Cottonwood is SERVED (its producer lands in the
                    same merge), `source_txn_id` carries a per-row claim and an ALL-PARTITION coverage per firm with its denominator
                    (the worker's own values-free runs of tools/id_coverage.py; the CTO's sample figures are superseded), and the two
                    transforms the producers apply are STATED with a claim each: `custodian` is lower-cased, and an empty or blank
                    symbol or identifier becomes null (text is stripped).  DBF130-1-AC1 (form), AC2 (bindings, reads, coverage)

The checker recomputes: the schema hash; every source from the ground-read records; the fee basis; the mapping words from the ratified
proposal; each 49 Financial code's flow class from the contract's own rule over the CRO table; the Inflection not_observed set from the
live census; and the censuses of the two rule-24 records from the mapping.

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
COTTONWOOD = D + "0.9.0_WK_IRPT_DASHBD~1402/FWD5_WORDS_COTTONWOOD_R128.json"
READS = D + "0.9.0_WK_IRPT_DASHBD~1601/RD_READS_R130.json"
IDCOV = D + "0.9.0_WK_IRPT_DASHBD~1601/RD_ID_COVERAGE_R130.json"
TRANSFER_OUT_PAIR = "Transfer Out | Transfer Out"
CENSUS49 = D + "2.0.0_SA_COO~F2/R124_LIVE_SILVER_CENSUS_49F.json"
CENSUS3 = D + "2.0.0_SA_COO~F2/R128_LIVE_SOURCE_CENSUS_3FIRMS.json"
CRO = "org/tier1_exec/4.0.0_SA_CRO/deliverables/SCHWAB_TRANSACTION_CODE_CLASSIFICATION_20260811.json"
GROUND = {"49financial": D + "0.9.0_WK_IRPT_DASHBD~1401/RD_FWD5_GROUND_49FINANCIAL_R128.json",
          "cottonwood": D + "0.9.0_WK_IRPT_DASHBD~1401/RD_FWD5_GROUND_COTTONWOOD_R128.json",
          "inflection": D + "0.9.0_WK_IRPT_DASHBD~1401/RD_FWD5_GROUND_INFLECTION_R128.json"}
FIRM49 = "49financial"
UNMAPPED = "UNMAPPED"
CLAIMS = ("measured", "inferred", "held", "absent")
FLOW = ("EXTERNAL_IN", "EXTERNAL_OUT", "INCOME", "FEE", "INTERNAL", "CORPORATE_ACTION", "UNRESOLVED")
COLUMNS = ("firm", "account_id", "business_date", "trade_date", "settle_date", "action", "txn_type", "symbol", "asset_name", "units",
           "price", "amount", "fee", "custodian", "flow_class", "source_txn_id", "coverage")
BRIEF14 = COLUMNS[3:]
TYPES = ("string", "date32[day]", "double")
COVERAGE = ("MEASURED", "CODE_NOT_IN_MAPPING", "UNMAPPED_BY_TABLE")
KEYS = ("contract_version", "supersedes", "project", "prd", "authored_by", "authored_under", "table", "grain", "partition", "producer",
        "columns", "sources", "fee_basis", "transforms", "source_txn_id_coverage", "enums", "type_action", "flow_class_rule",
        "source_mapping", "cottonwood_mapping", "unmapped_display", "new_code_reason", "firms_served", "firms_pending",
        "rule24_records", "reads", "schema_hash", "schema_hash_basis", "served", "served_note")
POSTULATES = ("mece", "same_grain", "intent_coherence", "state_coherence")
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
    return hashlib.sha256("\n".join(sorted("%s:%s" % (c["name"], c["type"]) for c in columns)).encode("ascii")).hexdigest()


def column_problems(cols, rec49):
    """The 17 columns in order; the claim of each brief column equals the 49 Financial ground read's claim for that target."""
    if not (isinstance(cols, list) and [c.get("name") if isinstance(c, dict) else None for c in cols] == list(COLUMNS)):
        return ["columns must be exactly, in order: " + ", ".join(COLUMNS)]
    want = {t["target"]: t["claim"] for t in rec49["targets"]}
    pr = []
    for c in cols:
        n = c["name"]
        if c.get("type") not in TYPES or not isinstance(c.get("nullable"), bool):
            pr.append("%s: type or nullable" % n)
        if c.get("claim") not in CLAIMS or not (isinstance(c.get("meaning"), str) and c["meaning"].strip()):
            pr.append("%s: claim or meaning" % n)
        if c.get("claim") == "inferred" and not (isinstance(c.get("method"), str) and c["method"].strip()):
            pr.append("%s: an inferred column needs a method" % n)
        if n in want and c.get("claim") != want[n]:
            pr.append("%s: claim %r differs from the 49 Financial ground read's %r" % (n, c.get("claim"), want[n]))
        if c.get("claim") == "absent" and c.get("nullable") is not True:
            pr.append("%s: an absent column is nullable" % n)
    return pr


def transform_problems(tr):
    """The stated transforms: custodian lower-cased; an empty or blank symbol, asset name or identifier becomes null; each an inferred claim."""
    if not (isinstance(tr, list) and tr and all(isinstance(t, dict) for t in tr)):
        return ["transforms must be a non-empty list of objects"]
    pr = []
    by = {t.get("field"): t for t in tr}
    for field, words in (("custodian", ("lower",)), ("symbol", ("empty", "null")), ("source_txn_id", ("empty", "null")),
                         ("asset_name", ("empty", "null"))):
        t = by.get(field)
        if t is None:
            pr.append("transforms must state the rule for %s" % field)
            continue
        if t.get("claim") != "inferred" or not (isinstance(t.get("method"), str) and t["method"].strip()):
            pr.append("transforms %s: claim inferred and a method" % field)
        rule = str(t.get("rule", "")).lower()
        if not all(w in rule for w in words):
            pr.append("transforms %s: the rule must say %s" % (field, " and ".join(words)))
    return pr


def coverage_problems(con, idcov, recs):
    """source_txn_id: a per-row claim, the chosen column, and the ALL-PARTITION coverage the worker's own runs measured, per firm."""
    c = con["source_txn_id_coverage"]
    if not (isinstance(c, dict) and sorted(c.keys()) == sorted(GROUND)):
        return ["source_txn_id_coverage must hold exactly the three firms"]
    pr = []
    for firm in GROUND:
        cov = idcov.get("firms", {}).get(firm) if isinstance(idcov, dict) else None
        if not (isinstance(cov, dict) and cov.get("all_partitions") is True and isinstance(cov.get("rows"), int) and cov["rows"] > 0):
            pr.append("%s: RD_ID_COVERAGE_R130.json must hold the worker's own ALL-partition run (rows above zero)" % firm)
            continue
        chosen = next(t["source"] for t in recs[firm]["targets"] if t["target"] == "source_txn_id")
        want = {"chosen_column": chosen, "rows": cov["rows"], "partitions_read": cov["partitions_read"], "all_partitions": True,
                "columns": cov["columns"]}
        e = c[firm]
        if not isinstance(e, dict) or {k: e.get(k) for k in want} != want:
            pr.append("%s: source_txn_id_coverage must equal the worker's own all-partition run (chosen column %r, rows, partitions, columns)" % (firm, chosen))
        elif not (isinstance(e.get("per_row_claim"), str) and "present" in e["per_row_claim"].lower() and "absent" in e["per_row_claim"].lower()):
            pr.append("%s: per_row_claim must say a row is present where the source column is non-null and absent where it is null" % firm)
    return pr


def rule24_problems(rec):
    pr = []
    if not (isinstance(rec, dict) and sorted(rec.keys()) == ["coverage", "flow_class_rule"]):
        return ["rule24_records must hold exactly coverage and flow_class_rule"]
    for name, r in rec.items():
        po = r.get("postulates") if isinstance(r, dict) else None
        if not (isinstance(po, dict) and sorted(po.keys()) == sorted(POSTULATES)
                and all(isinstance(po[k], str) and len(po[k].strip()) >= 40 for k in POSTULATES)):
            pr.append("%s: postulates must be exactly %r, each 40+ characters" % (name, POSTULATES))
        c = r.get("census") if isinstance(r, dict) else None
        if not (isinstance(c, dict) and c.get("method") == "word-boundary" and isinstance(c.get("denominator"), int)
                and isinstance(c.get("per_value"), dict)):
            pr.append("%s: census must carry method word-boundary, an integer denominator and per_value" % name)
    return pr


def form_problems(con, rec49):
    if not isinstance(con, dict) or sorted(con.keys()) != sorted(KEYS):
        return ["contract fields are not exactly " + repr(KEYS)]
    pr = []
    if con["contract_version"] != "0.3.0" or not str(con["supersedes"]).startswith("0.2.0"):
        pr.append("contract_version must be 0.3.0 and supersedes name 0.2.0")
    if con["table"] != "account_transaction" or con["partition"] != "date=YYYY-MM-DD":
        pr.append("table / partition")
    pr += column_problems(con["columns"], rec49)
    if isinstance(con["columns"], list) and all(isinstance(c, dict) and "name" in c and "type" in c for c in con["columns"]):
        if con["schema_hash"] != schema_hash(con["columns"]):
            pr.append("schema_hash is not the sha256 over the sorted name:type lines")
    en = con["enums"]
    if not (isinstance(en, dict) and sorted(en.keys()) == ["action", "coverage", "flow_class", "txn_type"]):
        pr.append("enums must hold exactly txn_type, action, flow_class, coverage")
    elif tuple(en["flow_class"]) != FLOW or tuple(en["coverage"]) != COVERAGE:
        pr.append("enums.flow_class / enums.coverage are not the seven classes / three coverage values in order")
    if con["unmapped_display"] != "Unclassified" or con["new_code_reason"] != "CODE_NOT_IN_MAPPING":
        pr.append("unmapped_display Unclassified and new_code_reason CODE_NOT_IN_MAPPING")
    served, fp = con["firms_served"], con["firms_pending"]
    pending = sorted(x.get("firm") for x in fp if isinstance(x, dict)) if isinstance(fp, list) else []
    if not (isinstance(served, list) and sorted(served) == ["49financial", "cottonwood"] and pending == ["inflection"]):
        pr.append("firms_served must be 49financial and cottonwood and firms_pending inflection (its producer is the next drain)")
    pr += transform_problems(con["transforms"])
    if not (isinstance(fp, list) and all(isinstance(x.get("reason"), str) and x["reason"].strip() for x in fp if isinstance(x, dict))):
        pr.append("every firms_pending entry needs a reason")
    pr += rule24_problems(con["rule24_records"])
    if con["served"] is not False:
        pr.append("served must be false")
    if not json.dumps(con, ensure_ascii=False).isascii():
        pr.append("non-ASCII text")
    return pr


def source_problems(con, recs):
    pr = []
    src = con["sources"]
    if not (isinstance(src, dict) and sorted(src.keys()) == sorted(GROUND)):
        return ["sources must hold exactly the three firms"]
    for firm, rec in recs.items():
        got = {s.get("target"): s for s in src[firm]} if isinstance(src[firm], list) else {}
        for t in rec["targets"]:
            want = {"target": t["target"], "source": t["source"], "from_columns": t["from_columns"], "claim": t["claim"],
                    "method": t["method"]}
            g = got.get(t["target"])
            if g is None or {k: g.get(k) for k in want} != want:
                pr.append("%s %s: source entry differs from the ground read" % (firm, t["target"]))
        if sorted(got) != sorted(BRIEF14):
            pr.append("%s: sources must hold exactly the 14 brief targets" % firm)
    fb = con["fee_basis"]
    want_fb = {}
    for firm, rec in recs.items():
        fee = next(t for t in rec["targets"] if t["target"] == "fee")
        want_fb[firm] = fee["from_columns"] if fee["from_columns"] else ([fee["source"]] if fee["source"] else None)
    if not (isinstance(fb, dict) and sorted(fb.keys()) == sorted(GROUND)):
        pr.append("fee_basis must hold exactly the three firms")
    else:
        for firm, cols in want_fb.items():
            e = fb[firm]
            if cols is None:
                if e is not None:
                    pr.append("fee_basis %s must be null (the firm's table has no fee column)" % firm)
            elif not (isinstance(e, dict) and e.get("columns") == cols and isinstance(e.get("rule"), str) and e["rule"].strip()):
                pr.append("fee_basis %s must name exactly the ground read's fee columns %r and state the rule" % (firm, cols))
    return pr


def rule_problems(con):
    got = {}
    for r in con["flow_class_rule"] if isinstance(con["flow_class_rule"], list) else []:
        if isinstance(r, dict):
            got[(r.get("partition"), r.get("rule"))] = (r.get("flow_class"), r.get("reason"))
    if set(got) != set(EXPECTED_RULE):
        return ["flow_class_rule must hold exactly the 30 (partition, rule) pairs"]
    pr = []
    for k, want in EXPECTED_RULE.items():
        if got[k][0] != want or not (isinstance(got[k][1], str) and got[k][1].strip()):
            pr.append("flow_class_rule %r must be %s with a reason" % (k, want))
    return pr


def expected_flow(cro_rows):
    cls = {}
    for r in cro_rows:
        cls.setdefault(r["tran_srcde"], set()).add(EXPECTED_RULE[(r["partition"], r["rule"])])
    return {c: (next(iter(s)) if len(s) == 1 else "UNRESOLVED") for c, s in cls.items()}


def mapping_problems(con, prop, cro_rows, census49, census3):
    pr = []
    types = [t["word"] for t in prop["opal_types"]]
    acts = [a["word"] for a in prop["opal_actions"]]
    en = con["enums"]
    if sorted(en["txn_type"]) != sorted(types) or sorted(en["action"]) != sorted(acts):
        pr.append("enums.txn_type / enums.action are not the ratified proposal's words")
    if con["type_action"] != {t["word"]: t["action"] for t in prop["opal_types"]}:
        pr.append("type_action is not the ratified proposal's table")
    rows = con["source_mapping"]
    if not (isinstance(rows, list) and rows):
        return pr + ["source_mapping is empty"]
    got = {}
    for m in rows:
        key = (m.get("firm"), m.get("source_value"))
        if key in got:
            pr.append("duplicate source_mapping row %r" % (key,))
        got[key] = m
    want = {(m["firm"], m["source_value"]): m["opal_type"] for m in prop["mapping"] if m["firm"] != "cottonwood"}
    if any(k[0] == "cottonwood" for k in got):
        pr.append("Cottonwood rows must not be in the contract: its re-cut words are not ratified")
    if {k: v["opal_type"] for k, v in got.items()} != want:
        pr.append("source_mapping words differ from the ratified proposal for 49 Financial and Inflection (%d rows against %d)"
                  % (len(got), len(want)))
    ef = expected_flow(cro_rows)
    ef.update(SILVER_ONLY_FLOW)
    live_inf = set(census3["firms"]["inflection"]["values"]["transactionDescription"])
    for (firm, code), m in got.items():
        if firm == FIRM49:
            if m.get("flow_class") != ef.get(code):
                pr.append("49financial %r: flow_class %r, the rule gives %r" % (code, m.get("flow_class"), ef.get(code)))
        else:
            if m.get("flow_class") is not None:
                pr.append("%s %r: flow_class must be null until that firm's producer lands" % (firm, code))
            if m.get("not_observed") is not (code not in live_inf):
                pr.append("inflection %r: not_observed must be %r (the live census has %d descriptions)" % (code, code not in live_inf, len(live_inf)))
    for code, cls in FIXED_POINTS.items():
        if got.get((FIRM49, code), {}).get("flow_class") != cls:
            pr.append("%s must be %s" % (code, cls))
    if sum(1 for k in got if k[0] == FIRM49) != len(census49["codes"]):
        pr.append("49financial rows are not the live census's %d codes" % len(census49["codes"]))
    return pr


def cottonwood_problems(con, rec):
    """The contract's Cottonwood section equals the ratified record, except the CTO's round-128 ruling for Transfer Out."""
    cm = con["cottonwood_mapping"]
    if not (isinstance(cm, dict) and sorted(cm.keys()) == ["action_derivation", "actions", "external_flow_rule", "type_pairs"]):
        return ["cottonwood_mapping must hold exactly action_derivation, actions, external_flow_rule, type_pairs"]
    pr = []
    if cm["external_flow_rule"] != rec["external_flow_rule"]:
        pr.append("cottonwood_mapping.external_flow_rule differs from the ratified record")
    if not (isinstance(cm["action_derivation"], str) and "pair" in cm["action_derivation"].lower()):
        pr.append("cottonwood_mapping.action_derivation must say a line with no Action derives its action from the pair (CTO msg 9175)")
    want_t, want_a = {}, {}
    for m in rec["mapping"]:
        if m["field"] == "type_pair":
            want_t[m["source_value"]] = (m["opal_type"], m["flow_class_none"])
        else:
            want_a[m["source_value"]] = m["opal_action"]
    if TRANSFER_OUT_PAIR in want_t:
        want_t[TRANSFER_OUT_PAIR] = (want_t[TRANSFER_OUT_PAIR][0], "EXTERNAL_OUT")
    got_t = {m.get("source_value"): (m.get("opal_type"), m.get("flow_class_none")) for m in cm["type_pairs"]}
    got_a = {m.get("source_value"): m.get("opal_action") for m in cm["actions"]}
    if got_t != want_t or len(cm["type_pairs"]) != len(want_t):
        pr.append("cottonwood_mapping.type_pairs differ from the ratified record (Transfer Out | Transfer Out is EXTERNAL_OUT by the ruling)")
    if got_a != want_a or len(cm["actions"]) != len(want_a):
        pr.append("cottonwood_mapping.actions differ from the ratified record")
    return pr


def reads_problems(con, reads, census3):
    """The contract's `reads` is the worker's own non-null read of each firm; the column lists equal the issuer's census."""
    pr = []
    r = con["reads"]
    if not (isinstance(r, dict) and sorted(r.keys()) == sorted(GROUND)):
        return ["reads must hold exactly the three firms"]
    for firm in GROUND:
        w = reads.get("firms", {}).get(firm) if isinstance(reads, dict) else None
        if not (isinstance(w, dict) and all(isinstance(w.get(k), int) and w[k] > 0 for k in ("partitions_read", "objects_read", "rows"))):
            pr.append("%s: the worker's own read (RD_READS_R129.json) must have partitions_read, objects_read and rows above zero" % firm)
            continue
        if w.get("columns") != census3["firms"][firm]["columns"]:
            pr.append("%s: the worker's own read of the schema differs from the issuer's census" % firm)
        if r[firm] != {k: w[k] for k in ("partitions_read", "objects_read", "rows", "read_at_utc")}:
            pr.append("%s: contract reads must be {partitions_read, objects_read, rows, read_at_utc} of the worker's own read" % firm)
    return pr


def census_problems(con):
    """The two rule-24 censuses equal the counts computed from the mapping."""
    pr = []
    rows49 = [m for m in con["source_mapping"] if m.get("firm") == FIRM49]
    flow = {}
    for m in rows49:
        flow[m.get("flow_class")] = flow.get(m.get("flow_class"), 0) + 1
    cov = {"MEASURED": sum(1 for m in rows49 if m.get("opal_type") != UNMAPPED),
           "UNMAPPED_BY_TABLE": sum(1 for m in rows49 if m.get("opal_type") == UNMAPPED), "CODE_NOT_IN_MAPPING": 0}
    r24 = con["rule24_records"]
    if r24["flow_class_rule"]["census"].get("per_value") != flow or r24["flow_class_rule"]["census"].get("denominator") != len(rows49):
        pr.append("rule24_records.flow_class_rule.census must be the per-class counts of the %d 49 Financial codes" % len(rows49))
    if r24["coverage"]["census"].get("per_value") != cov or r24["coverage"]["census"].get("denominator") != len(rows49):
        pr.append("rule24_records.coverage.census must be %r over the %d codes (CODE_NOT_IN_MAPPING is 0 in the live read)" % (cov, len(rows49)))
    return pr


def data_problems(con, data):
    if not isinstance(data, dict):
        return ["data file form"]
    pr = []
    if data.get("source_mapping") != con["source_mapping"] or data.get("type_action") != con["type_action"]:
        pr.append("transaction_words.json differs from the contract's source_mapping / type_action")
    if data.get("contract_version") != con["contract_version"]:
        pr.append("transaction_words.json contract_version differs")
    return pr


def ac_form(root):
    con = load(root, CONTRACT)
    pr = form_problems(con, load(root, GROUND[FIRM49]))
    need(not pr, "; ".join(pr[:6]))


def ac_bindings(root):
    con = load(root, CONTRACT)
    recs = {f: load(root, p) for f, p in GROUND.items()}
    census_prob = coverage_problems(con, load(root, IDCOV), recs)
    need(not form_problems(con, recs[FIRM49]), "the contract's form must pass DBF130-1-AC1 first")
    pr = source_problems(con, recs) + rule_problems(con)
    pr += mapping_problems(con, load(root, PROPOSAL), load(root, CRO), load(root, CENSUS49), load(root, CENSUS3))
    pr += census_problems(con) + data_problems(con, load(root, DATA))
    pr += cottonwood_problems(con, load(root, COTTONWOOD)) + reads_problems(con, load(root, READS), load(root, CENSUS3))
    pr += census_prob
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
    cro = [{"tran_srcde": "A", "partition": "INTERNAL", "rule": "dividends"}]
    arm("expected-flow", expected_flow(cro), {"A": "INCOME"})
    rec49 = {"targets": [{"target": n, "claim": "measured"} for n in BRIEF14]}
    cols = [{"name": n, "type": "string", "nullable": False, "meaning": "m", "claim": "measured"} for n in COLUMNS]
    arm("columns-green", column_problems(cols, rec49), [])
    drift = [dict(c) for c in cols]
    drift[4]["claim"] = "absent"
    arm("claim-must-match-ground", len(column_problems(drift, rec49)) >= 1, True)
    arm("hash-order", schema_hash(cols) == schema_hash(list(reversed(cols))), True)
    po = {k: "x" * 41 for k in POSTULATES}
    good24 = {n: {"postulates": po, "census": {"method": "word-boundary", "denominator": 1, "per_value": {}}} for n in ("coverage", "flow_class_rule")}
    arm("rule24-green", rule24_problems(good24), [])
    arm("rule24-red", len(rule24_problems({"coverage": good24["coverage"]})), 1)
    arm("fee-basis-form", source_problems({"sources": {"x": []}, "fee_basis": {}}, {}), ["sources must hold exactly the three firms"])
    arm("form-red", form_problems({"a": 1}, rec49)[0].startswith("contract fields"), True)
    good_tr = [{"field": "custodian", "rule": "lower-cased", "claim": "inferred", "method": "m"},
               {"field": "symbol", "rule": "empty becomes null", "claim": "inferred", "method": "m"},
               {"field": "source_txn_id", "rule": "empty becomes null", "claim": "inferred", "method": "m"},
               {"field": "asset_name", "rule": "empty becomes null", "claim": "inferred", "method": "m"}]
    arm("transforms-green", transform_problems(good_tr), [])
    arm("transforms-missing", len(transform_problems(good_tr[:3])), 1)
    arm("transforms-word", len(transform_problems([dict(good_tr[0], rule="as written")] + good_tr[1:])), 1)
    recs3 = {f: {"targets": [{"target": "source_txn_id", "source": "c"}]} for f in GROUND}
    cov = {"all_partitions": True, "rows": 5, "partitions_read": 2, "columns": {"c": {"non_null": 5}}}
    con_c = {"source_txn_id_coverage": {f: {"chosen_column": "c", "rows": 5, "partitions_read": 2, "all_partitions": True,
                                            "columns": {"c": {"non_null": 5}}, "per_row_claim": "present where non-null, absent where null"}
                                        for f in GROUND}}
    arm("coverage-green", coverage_problems(con_c, {"firms": {f: cov for f in GROUND}}, recs3), [])
    arm("coverage-needs-all-partitions", len(coverage_problems(con_c, {"firms": {f: dict(cov, all_partitions=False) for f in GROUND}}, recs3)), 3)
    rec_cw = {"external_flow_rule": {"x": "y"}, "mapping": [
        {"field": "type_pair", "source_value": TRANSFER_OUT_PAIR, "opal_type": "Transfer out", "flow_class_none": "UNRESOLVED"},
        {"field": "action", "source_value": "Buy", "opal_action": "Trade"}]}
    con_cw = {"cottonwood_mapping": {"action_derivation": "from the pair", "external_flow_rule": {"x": "y"},
                                     "type_pairs": [{"source_value": TRANSFER_OUT_PAIR, "opal_type": "Transfer out", "flow_class_none": "EXTERNAL_OUT"}],
                                     "actions": [{"source_value": "Buy", "opal_action": "Trade"}]}}
    arm("cottonwood-ruling-green", cottonwood_problems(con_cw, rec_cw), [])
    old = {"cottonwood_mapping": dict(con_cw["cottonwood_mapping"], type_pairs=[{"source_value": TRANSFER_OUT_PAIR, "opal_type": "Transfer out",
                                                                                 "flow_class_none": "UNRESOLVED"}])}
    arm("cottonwood-ruling-red", len(cottonwood_problems(old, rec_cw)), 1)
    c3 = {"firms": {f: {"columns": ["a"]} for f in GROUND}}
    ok = {f: {"partitions_read": 1, "objects_read": 1, "rows": 2, "columns": ["a"], "read_at_utc": "t"} for f in GROUND}
    con_r = {"reads": {f: {k: ok[f][k] for k in ("partitions_read", "objects_read", "rows", "read_at_utc")} for f in GROUND}}
    arm("reads-green", reads_problems(con_r, {"firms": ok}, c3), [])
    zero = {f: dict(ok[f], rows=0) for f in GROUND}
    arm("reads-must-be-nonzero", len(reads_problems(con_r, {"firms": zero}, c3)), 3)
    arm("fixed-points", sorted(FIXED_POINTS), ["IRAWH", "MCE"])
    print("selftest %s" % ("FAIL" if bad else "PASS (%d arms)" % count))
    return 1 if bad else 0


def main(argv):
    if len(argv) == 2 and argv[1] == "--selftest":
        return selftest()
    if len(argv) != 3:
        print(__doc__)
        return 2
    root, ac = argv[1], argv[2]
    table = {"DBF130-1-AC1": ac_form, "DBF130-1-AC2": ac_bindings}
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
