"""IRPT_DASHBD round 130 (~F2), cell DB-f-1601 (worker 0.9.0_WK_IRPT_DASHBD~1601).

Generates the FWD-5 transaction contract 0.3.0 and its mapping data file. Adapted from the 0.2.0 generator
(deliverables/0.9.0_WK_IRPT_DASHBD~1501/gen_transaction_contract_0_2_0.py). Nothing here is typed by hand: every source binding,
claim, fee basis, census, coverage figure and read is read from the inputs below. The 30-pair flow_class_rule is carried from the
0.2.0 contract on trunk, read BEFORE that file is overwritten.

Inputs (read only):
  the three round-128 ground-read records     RD_FWD5_GROUND_{49FINANCIAL,COTTONWOOD,INFLECTION}_R128.json
  the live census (round 128)                R128_LIVE_SOURCE_CENSUS_3FIRMS.json
  the ratified proposal                      FWD5_WORDS_PROPOSAL_R124.json
  the ratified Cottonwood record             FWD5_WORDS_COTTONWOOD_R128.json (33 type pairs, 87 actions)
  the CRO table                              SCHWAB_TRANSACTION_CODE_CLASSIFICATION_20260811.json
  the live 49 Financial code census          R124_LIVE_SILVER_CENSUS_49F.json (160 codes)
  the worker's own reads (round 130)         RD_READS_R130.json and RD_ID_COVERAGE_R130.json (the two tools' outputs, unchanged)
  the 0.2.0 contract on trunk                its flow_class_rule (30 pairs, with reasons)

Outputs (written):
  org/standards/IRPT_DASHBD_ACCOUNT_TRANSACTION_CONTRACT.json
  data/assets/scripts/gold/irpt_reporting/transaction_words.json

Run from the worktree root:  python -I <this file>
"""
import hashlib
import json
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(".")
D = "org/missions/D9/IRPT/IRPT_DASHBD/deliverables/"
MINE = D + "0.9.0_WK_IRPT_DASHBD~1601/"
GROUND_D = D + "0.9.0_WK_IRPT_DASHBD~1401/"
PROPOSAL = D + "0.9.0_WK_IRPT_DASHBD~1001/FWD5_WORDS_PROPOSAL_R124.json"
COTTONWOOD_REC = D + "0.9.0_WK_IRPT_DASHBD~1402/FWD5_WORDS_COTTONWOOD_R128.json"
READS = MINE + "RD_READS_R130.json"
IDCOV = MINE + "RD_ID_COVERAGE_R130.json"
TRANSFER_OUT_PAIR = "Transfer Out | Transfer Out"
CW_TRANSFER_OUT_RULING = "EXTERNAL_OUT"  # the CTO's round-128 ruling (msg 9175); its class for lines marked None
CW_TRANSFER_OUT_REASON = ("Transfer Out type and sub type. The live read of round 130 finds no null Action in Cottonwood (87 values, none "
                          "missing), so the lines that the round-128 analysis counted as lacking an Action are the lines whose External Flow "
                          "is None. By the CTO's round-128 ruling (msg 9175) the pair's class for lines marked None is EXTERNAL_OUT; no line "
                          "is dropped or left blank.")
CW_ACTION_DERIVATION = ("A Cottonwood line whose vendor Action is null or blank derives its action word from its (Transaction Type, "
                        "Transaction Sub Type) pair through the type table (type_action), the same rule as a 49 Financial code with no action "
                        "field. The live read finds no null Action in Cottonwood, so this is a stated fallback that no observed line uses; the "
                        "Action values that the vendor does carry map through cottonwood_mapping.actions.")
CENSUS124 = D + "2.0.0_SA_COO~F2/R124_LIVE_SILVER_CENSUS_49F.json"
CENSUS128 = D + "2.0.0_SA_COO~F2/R128_LIVE_SOURCE_CENSUS_3FIRMS.json"
CRO = "org/tier1_exec/4.0.0_SA_CRO/deliverables/SCHWAB_TRANSACTION_CODE_CLASSIFICATION_20260811.json"
CONTRACT = "org/standards/IRPT_DASHBD_ACCOUNT_TRANSACTION_CONTRACT.json"
DATA = "data/assets/scripts/gold/irpt_reporting/transaction_words.json"
GROUND = {"49financial": GROUND_D + "RD_FWD5_GROUND_49FINANCIAL_R128.json",
          "cottonwood": GROUND_D + "RD_FWD5_GROUND_COTTONWOOD_R128.json",
          "inflection": GROUND_D + "RD_FWD5_GROUND_INFLECTION_R128.json"}

FIRM49 = "49financial"
FIRM_CW = "cottonwood"
FIRM_INF = "inflection"
UNMAPPED = "UNMAPPED"
FLOW = ["EXTERNAL_IN", "EXTERNAL_OUT", "INCOME", "FEE", "INTERNAL", "CORPORATE_ACTION", "UNRESOLVED"]
COVERAGE = ["MEASURED", "CODE_NOT_IN_MAPPING", "UNMAPPED_BY_TABLE"]
BRIEF14 = ["trade_date", "settle_date", "action", "txn_type", "symbol", "asset_name", "units", "price", "amount", "fee",
           "custodian", "flow_class", "source_txn_id", "coverage"]
SCHEMA_BASIS = ("sha256 over the sorted 'name:type' lines of columns joined by newline, types as the pyarrow type name the producer's "
                "ARROW_SCHEMA carries (the same method as the account_class_daily and account_return_daily contracts).")
PRD = "org/missions/D9/IRPT/IRPT_DASHBD/prd/IRPT_DASHBD_PRD.md"

# Column specs: name, type, nullable, own claim (None = the 49 Financial ground read's claim for the target), meaning, own method.
# The 17 columns and their types are the 0.2.0 columns (the schema hash does not change); the meanings of three columns say what the
# 0.3.0 producers do (amount for Cottonwood, business_date for Cottonwood, source_txn_id's per-row claim).
COLUMNS = [
    ("firm", "string", False, "inferred",
     "The registry-derived firm scope this row belongs to; never a typed token.",
     "The firm scope of the custody entry the silver partition is read under, taken from the registry."),
    ("account_id", "string", False, "measured",
     "The account key carried by the silver row. It is an identifier and is not reproduced in any report.", None),
    ("business_date", "date32[day]", False, "measured",
     "The business date of the row, the date= partition it is written under. 49 Financial: the silver partition's business date. "
     "Cottonwood: the adapter's performance day, the first NYSE trading day on or after the Trade Date (the adapter's window_day rule).",
     None),
    ("trade_date", "date32[day]", True, None,
     "The trade_date column of the transaction table, read as the closing trade's trade date (round-128 ground read); null when the row carries none.",
     None),
    ("settle_date", "date32[day]", True, None,
     "The settlement date: the settlmnt_date column of the transaction table (round-128 ground read); for Cottonwood the Settle Date column. "
     "Null when the value is missing or unparsable.", None),
    ("action", "string", True, None,
     "The action word of the row: the txn_type's action through type_action. Null only when the code is not in the mapping.", None),
    ("txn_type", "string", False, None,
     "The ratified type word of the row, or the string UNMAPPED when the mapping holds the code as UNMAPPED or lacks it.", None),
    ("symbol", "string", True, None,
     "The security symbol, the ticker_symbol column (49 Financial) or the Symbol column (Cottonwood); null on a row with no security.", None),
    ("asset_name", "string", True, None,
     "The security's name. The 49 Financial live schema (140 columns) has no name column (round-128 ground read), so the column is null on "
     "every 49 Financial row; Cottonwood reads its Asset Name column.", None),
    ("units", "double", True, None,
     "The quantity column, named as the units (round-128 ground read); for Cottonwood the Units column. Null when the row carries none.", None),
    ("price", "double", True, None,
     "The price column (round-128 ground read); for Cottonwood the Price column. Null when the row carries none.", None),
    ("amount", "double", False, None,
     "The custodian's money amount. 49 Financial: gross_amount; on a cash row the sign is taken from debit_credit as account_return_daily "
     "takes it (CREDIT positive, DEBIT negative); on an in-kind row debit_credit is a position side and is not read as a cash sign. "
     "Cottonwood: the Market Value, signed by the External Flow word as the adapter does (+abs for Contribution, -abs for Withdrawal) and "
     "as booked otherwise.", None),
    ("fee", "double", True, None,
     "The stated sum, for each firm, of the columns the contract's fee_basis names (49 Financial: commission, exchange_processing_fee, "
     "broker_service_fee, prime_broker_fee, trade_away_fee, redemption_fee, other_fee, step_in_fee, research_fee; Cottonwood: Transaction Fee "
     "and Account Fee). A null column counts as nothing; a row whose named columns are all null has fee null, never zero.", None),
    ("custodian", "string", False, "inferred",
     "The custodian of the row, lower-cased: the custody entry's constant (sources.json custodian) for 49 Financial, and Cottonwood's Custodian "
     "column for Cottonwood. The round-128 ground read names custdian_id as the custodian identity column for 49 Financial; the constant is "
     "what a person reads, and custdian_id is not read onto the row.",
     "The custodian constant of the custody entry (49 Financial) or the Custodian column (Cottonwood), stripped and lower-cased by the producer; "
     "set once per entry in the registry."),
    ("flow_class", "string", False, None,
     "The flow class of the row's code: EXTERNAL_IN, EXTERNAL_OUT, INCOME, FEE, INTERNAL, CORPORATE_ACTION or UNRESOLVED. 49 Financial: the "
     "tran_srcde code's class. Cottonwood: the External Flow word (Contribution EXTERNAL_IN, Withdrawal EXTERNAL_OUT) or the pair's class.",
     "49 Financial: per tran_srcde through flow_class_rule over the CRO table's (partition, rule) pairs: one class when the code's CRO rows "
     "agree, UNRESOLVED when they disagree or the table does not hold the code. The silver-only codes and IRAWH and MCE are fixed in "
     "source_mapping. Cottonwood: cottonwood_mapping (the External Flow rule, then the pair's flow_class_none). The round-128 ground read "
     "names the 49 Financial key (tran_srcde, tr_cd, sb_cd); this contract keys on tran_srcde, the key source_mapping holds."),
    ("source_txn_id", "string", True, None,
     "The per-transaction identifier of the row, a PER-ROW CLAIM: present where the firm's source column (49 Financial "
     "cashiering_transaction_identifier; Cottonwood TransactionID) is non-null and non-blank, and absent (null) where it is not. It is never a "
     "universal key: source_txn_id_coverage states each firm's coverage over every partition with its denominator.", None),
    ("coverage", "string", False, None,
     "How the row's code is covered by the mapping: MEASURED, CODE_NOT_IN_MAPPING or UNMAPPED_BY_TABLE.",
     "MEASURED when the code maps to a type word; CODE_NOT_IN_MAPPING when the mapping lacks the code; UNMAPPED_BY_TABLE when the mapping "
     "holds the code as UNMAPPED."),
]

FEE_RULE_49F = ("The fee is the stated sum of the nine listed columns. For each line it is the sum of the non-null values of commission, "
                "exchange_processing_fee, broker_service_fee, prime_broker_fee, trade_away_fee, redemption_fee, other_fee, step_in_fee and "
                "research_fee. A null column counts as nothing. A line whose nine columns are all null has fee null, never zero. "
                "Excluded by the round-128 ground read: markupmarkdown (a price markup, not a fee charge) and exec_brok_comm (its meaning "
                "as a fee is not established from the census or the tracked records).")
FEE_RULE_CW = ("The fee is the stated sum of Transaction Fee and Account Fee per line, read by the Cottonwood producer. A null column counts "
               "as nothing. A line whose two columns are both null has fee null, never zero.")

TRANSFORMS = [
    {"field": "custodian", "firms": [FIRM49, FIRM_CW],
     "rule": ("The producer strips the value and LOWER-CASES it: the 49 Financial custody constant and Cottonwood's Custodian column, so "
              "the word reads the same across firms. A value is lower-cased, never upper-cased or title-cased."),
     "claim": "inferred",
     "method": ("The strip and lower-case calls in account_transaction.custodian() (49 Financial) and in the Cottonwood normaliser's "
                "custodian field; asserted by the offline tests of both modules on made-up custodians.")},
    {"field": "symbol", "firms": [FIRM49, FIRM_CW],
     "rule": ("The producer strips the text; an EMPTY or BLANK value becomes NULL, never the empty string. The 49 Financial symbol is "
              "ticker_symbol; the Cottonwood symbol is Symbol."),
     "claim": "inferred",
     "method": ("The shared text helper of each module (strip, then empty or blank to None); asserted by the offline tests on an empty "
                "and a blank symbol.")},
    {"field": "asset_name", "firms": [FIRM49, FIRM_CW],
     "rule": ("The producer strips the text; an EMPTY or BLANK asset name becomes NULL. The 49 Financial column is null on every row "
              "(claim absent: the live schema has no name column); Cottonwood reads its Asset Name column."),
     "claim": "inferred",
     "method": "The same text helper as symbol; the 49 Financial producer sets None by construction, the Cottonwood producer reads the column."},
    {"field": "source_txn_id", "firms": [FIRM49, FIRM_CW],
     "rule": ("The producer strips the text; an EMPTY or BLANK identifier becomes NULL. So a null source_txn_id is either a source "
              "identifier that was empty or blank, or one the source never carried; source_txn_id_coverage and the source column tell the "
              "two apart."),
     "claim": "inferred",
     "method": ("The shared text helper of each module, read from cashiering_transaction_identifier (49 Financial) and TransactionID "
                "(Cottonwood); asserted by the offline tests on an empty and a missing identifier.")},
]


def ascii_check(obj, label):
    text = json.dumps(obj, ensure_ascii=False)
    if not text.isascii():
        sys.exit("ERROR: non-ASCII text in " + label)


def load(rel):
    return json.loads((ROOT / rel).read_text(encoding="utf-8"))


def schema_hash(columns):
    lines = sorted("%s:%s" % (c["name"], c["type"]) for c in columns)
    return hashlib.sha256("\n".join(lines).encode("ascii")).hexdigest()


def coverage_entry(firm, chosen, cov, parts_text):
    """One firm's source_txn_id coverage: the worker's own all-partition run, copied, with the per-row claim stated from its numbers."""
    assert cov["all_partitions"] is True and cov["rows"] > 0, firm
    col = cov["columns"][chosen]
    rows, nn = cov["rows"], col["non_null"]
    share = 100.0 * nn / rows
    rep, parts_rep = col["rows_in_values_repeated_within_a_partition"], col["partitions_with_a_repeated_value"]
    claim = ("A row's source_txn_id is PRESENT where the source column (%s) is non-null and non-blank, and ABSENT (null) where it is not. "
             "The column is NEVER a universal key: %s of %s rows (%.4f percent) carry a value over all %d partitions. " % (
                 chosen, format(nn, ","), format(rows, ","), share, cov["partitions_read"]))
    claim += parts_text(rep, parts_rep)
    return {"chosen_column": chosen, "per_row_claim": claim, "rows": rows, "partitions_read": cov["partitions_read"],
            "all_partitions": True, "columns": cov["columns"]}


def main():
    old = load(CONTRACT)  # the 0.2.0 contract on trunk: its 30-pair rule is carried with its reasons, before it is overwritten
    rule_table = [(r["partition"], r["rule"], r["flow_class"], r["reason"]) for r in old["flow_class_rule"]]
    assert len(rule_table) == 30, "the 0.2.0 flow_class_rule must hold 30 pairs"
    rule_map = {(p, r): f for p, r, f, _ in rule_table}

    prop = load(PROPOSAL)
    cro = load(CRO)
    cen124 = load(CENSUS124)
    cen128 = load(CENSUS128)
    ground = {f: load(p) for f, p in GROUND.items()}
    cw = load(COTTONWOOD_REC)
    reads_doc = load(READS)
    idcov_doc = load(IDCOV)

    missing = sorted({(r["partition"], r["rule"]) for r in cro} - set(rule_map))
    if missing:
        sys.exit("ERROR: CRO pairs outside the 30-pair table: %r" % (missing,))

    per_code = {}
    for r in cro:
        per_code.setdefault(r["tran_srcde"], set()).add(rule_map[(r["partition"], r["rule"])])
    code_flow = {c: (next(iter(s)) if len(s) == 1 else "UNRESOLVED") for c, s in per_code.items()}

    types = [t["word"] for t in prop["opal_types"]]
    actions = [a["word"] for a in prop["opal_actions"]]
    type_action = {t["word"]: t["action"] for t in prop["opal_types"]}
    assert len(types) == 21 and len(actions) == 8

    live_inf = set(cen128["firms"][FIRM_INF]["values"]["transactionDescription"])
    live49 = set(cen124["codes"])
    assert len(live49) == 160 and len(live_inf) == 47, (len(live49), len(live_inf))
    assert set(cen124["silver_only_codes"]) == set(SILVER_ONLY_FLOW)

    targets = {f: {t["target"]: t for t in ground[f]["targets"]} for f in ground}
    for f in ground:
        assert [t["target"] for t in ground[f]["targets"]] == BRIEF14, "ground order differs in " + f

    columns = []
    for name, typ, nullable, own_claim, meaning, own_method in COLUMNS:
        if name in BRIEF14:
            t = targets[FIRM49][name]
            claim = t["claim"]
            method = t["method"] if claim == "inferred" else None
            if name == "flow_class":
                method = own_method
        else:
            claim = own_claim
            method = own_method if claim == "inferred" else None
        if name == "custodian":
            claim, method = "inferred", own_method
        c = {"name": name, "type": typ, "nullable": nullable, "meaning": meaning, "claim": claim}
        if claim == "inferred":
            assert method, "an inferred column needs a method: " + name
            c["method"] = method
        columns.append(c)
    assert [c["name"] for c in columns] == ["firm", "account_id", "business_date", "trade_date", "settle_date", "action", "txn_type",
                                            "symbol", "asset_name", "units", "price", "amount", "fee", "custodian", "flow_class",
                                            "source_txn_id", "coverage"]
    assert schema_hash(columns) == old["schema_hash"], "the schema hash must not change in 0.3.0"

    sources = {}
    for f in (FIRM49, FIRM_CW, FIRM_INF):
        sources[f] = [{"target": t["target"], "source": t["source"], "from_columns": t["from_columns"], "claim": t["claim"],
                       "method": t["method"]} for t in ground[f]["targets"]]

    fee_basis = {FIRM49: {"columns": list(targets[FIRM49]["fee"]["from_columns"]), "rule": FEE_RULE_49F},
                 FIRM_CW: {"columns": list(targets[FIRM_CW]["fee"]["from_columns"]), "rule": FEE_RULE_CW},
                 FIRM_INF: None}
    assert targets[FIRM_INF]["fee"]["from_columns"] == [] and targets[FIRM_INF]["fee"]["source"] is None

    source_mapping = []
    seen = set()
    for m in prop["mapping"]:
        firm, src = m["firm"], m["source_value"]
        if (firm, src) in seen:
            sys.exit("ERROR: duplicate proposal row %r" % ((firm, src),))
        seen.add((firm, src))
        if firm == FIRM_CW:
            continue
        reason = m.get("reason") if (m["opal_type"] == UNMAPPED or (firm == FIRM49 and src in SILVER_ONLY_FLOW)) else None
        if firm == FIRM49:
            if src in SILVER_ONLY_FLOW:
                flow = SILVER_ONLY_FLOW[src]
            elif src in FIXED_POINTS:
                flow = FIXED_POINTS[src]
            else:
                if src not in code_flow:
                    sys.exit("ERROR: live code %r is not in the CRO table and not a fixed or silver-only code" % src)
                flow = code_flow[src]
            row = {"firm": firm, "field": m["field"], "source_value": src, "opal_type": m["opal_type"], "flow_class": flow,
                   "reason": reason}
        else:
            row = {"firm": firm, "field": m["field"], "source_value": src, "opal_type": m["opal_type"], "flow_class": None,
                   "reason": reason, "not_observed": src not in live_inf}
        source_mapping.append(row)

    rows49 = [r for r in source_mapping if r["firm"] == FIRM49]
    rows_inf = [r for r in source_mapping if r["firm"] == FIRM_INF]
    assert len(rows49) == 160 and set(r["source_value"] for r in rows49) == live49
    assert len(rows_inf) == 48
    for code in FIXED_POINTS:
        assert any(r["firm"] == FIRM49 and r["source_value"] == code for r in rows49)
    assert not any(r["firm"] == FIRM_CW for r in source_mapping)

    flow_counts = Counter(r["flow_class"] for r in rows49)
    cov_counts = {"MEASURED": sum(1 for r in rows49 if r["opal_type"] != UNMAPPED),
                  "UNMAPPED_BY_TABLE": sum(1 for r in rows49 if r["opal_type"] == UNMAPPED),
                  "CODE_NOT_IN_MAPPING": 0}
    not_observed = sorted(r["source_value"] for r in rows_inf if r["not_observed"])

    cw_type_pairs = [{"source_value": m["source_value"], "opal_type": m["opal_type"],
                      "flow_class_none": (CW_TRANSFER_OUT_RULING if m["source_value"] == TRANSFER_OUT_PAIR else m["flow_class_none"]),
                      "reason": (CW_TRANSFER_OUT_REASON if m["source_value"] == TRANSFER_OUT_PAIR else m["reason"])}
                     for m in cw["mapping"] if m["field"] == "type_pair"]
    cw_actions = [{"source_value": m["source_value"], "opal_action": m["opal_action"], "reason": m["reason"]}
                  for m in cw["mapping"] if m["field"] == "action"]
    assert len(cw_type_pairs) == 33 and len(cw_actions) == 87, (len(cw_type_pairs), len(cw_actions))
    assert [m for m in cw_type_pairs if m["source_value"] == TRANSFER_OUT_PAIR][0]["opal_type"] == "Transfer out"
    cottonwood_mapping = {"external_flow_rule": cw["external_flow_rule"], "action_derivation": CW_ACTION_DERIVATION,
                          "type_pairs": cw_type_pairs, "actions": cw_actions}

    reads = {f: {k: reads_doc["firms"][f][k] for k in ("partitions_read", "objects_read", "rows", "read_at_utc")} for f in GROUND}
    assert all(reads[f]["rows"] > 0 and reads[f]["objects_read"] > 0 for f in GROUND)

    def parts49(rep, parts_rep):
        return ("%s rows of the present ones share their value with another row of the same partition (%d partitions), so the "
                "identifier is not unique within every partition." % (format(rep, ","), parts_rep))

    def parts_cw(rep, parts_rep):
        return ("%s rows of the present ones share their value with another row of the same partition (%d partitions), so "
                "TransactionID is not unique within every partition and is not a universal key." % (format(rep, ","), parts_rep))

    def parts_inf(rep, parts_rep):
        return ("No present row shares its value with another row of the same partition; the Inflection producer is pending "
                "(firms_pending), so this is the coverage read only.")

    fi = idcov_doc["firms"]
    chosen = {f: next(t["source"] for t in ground[f]["targets"] if t["target"] == "source_txn_id") for f in GROUND}
    assert chosen == {FIRM49: "cashiering_transaction_identifier", FIRM_CW: "TransactionID", FIRM_INF: "id"}, chosen
    coverage = {
        FIRM49: coverage_entry(FIRM49, chosen[FIRM49], fi[FIRM49], parts49),
        FIRM_CW: coverage_entry(FIRM_CW, chosen[FIRM_CW], fi[FIRM_CW], parts_cw),
        FIRM_INF: coverage_entry(FIRM_INF, chosen[FIRM_INF], fi[FIRM_INF], parts_inf),
    }

    contract = {
        "contract_version": "0.3.0",
        "supersedes": "0.2.0 (graded: the CVO's J1 PASS 20 of 20 by natural key)",
        "project": "IRPT_DASHBD",
        "prd": PRD,
        "authored_by": "0.9.0_WK_IRPT_DASHBD~1601",
        "authored_under": "IRPT_DASHBD.TO-DB-f-1601 (round 130, workstream ~F2, F-SHIP), cell DB-f-1601 of IRPT_DASHBD_DECOMP_R130_F.md, "
                          "following the CTO round-129 analysis for F-SHIP (msg 9211: source_txn_id's per-row claim with all-partition "
                          "coverage per firm; the custodian and empty-to-null transforms stated; the Cottonwood producer) and the CTO's "
                          "ruling msg 9192 item 4.",
        "table": "account_transaction",
        "grain": "account x transaction line",
        "partition": "date=YYYY-MM-DD",
        "producer": "data/assets/scripts/gold/irpt_reporting/account_transaction.py",
        "columns": columns,
        "sources": sources,
        "fee_basis": fee_basis,
        "transforms": TRANSFORMS,
        "source_txn_id_coverage": coverage,
        "enums": {
            "txn_type": types,
            "action": actions,
            "flow_class": FLOW,
            "coverage": COVERAGE,
        },
        "type_action": type_action,
        "flow_class_rule": [{"partition": p, "rule": r, "flow_class": f, "reason": why} for p, r, f, why in rule_table],
        "source_mapping": source_mapping,
        "cottonwood_mapping": cottonwood_mapping,
        "unmapped_display": "Unclassified",
        "new_code_reason": "CODE_NOT_IN_MAPPING",
        "firms_served": [FIRM49, FIRM_CW],
        "firms_pending": [
            {"firm": FIRM_INF,
             "reason": "No producer exists yet; the Inflection producer is the next drain (round 131), because it touches this contract "
                       "again. Its ground read is round 128: settle_date and fee are absent from its 36 columns. 47 of the 48 ratified "
                       "descriptions are live in the census; the 48th is marked not_observed. Its source_txn_id is the id column, read "
                       "over every partition in round 130."},
        ],
        "rule24_records": {
            "coverage": {
                "postulates": POSTULATES["coverage"],
                "census": {"method": "word-boundary", "denominator": len(rows49), "per_value": cov_counts},
            },
            "flow_class_rule": {
                "postulates": POSTULATES["flow_class_rule"],
                "census": {"method": "word-boundary", "denominator": len(rows49), "per_value": dict(flow_counts)},
            },
        },
        "reads": reads,
        "schema_hash": schema_hash(columns),
        "schema_hash_basis": SCHEMA_BASIS,
        "served": False,
        "served_note": ("Nothing is written. No object of this table exists in any bucket. 0.3.0 supersedes 0.2.0, which the CVO's J1 "
                        "passed 20 of 20 by natural key. Cottonwood's producer is account_transaction_cottonwood.py and is not wired; "
                        "the release is a never-widen act that waits on the producers, on the CVO's judgment at L9 (DBF130-1-J1), and on "
                        "a CTO and COO sign-off."),
    }

    data = {
        "contract_version": contract["contract_version"],
        "type_action": contract["type_action"],
        "source_mapping": contract["source_mapping"],
        "fee_basis": contract["fee_basis"],
        "cottonwood_mapping": contract["cottonwood_mapping"],
    }

    ascii_check(contract, CONTRACT)
    ascii_check(data, DATA)
    (ROOT / CONTRACT).write_text(json.dumps(contract, indent=2, ensure_ascii=True) + "\n", encoding="utf-8", newline="\n")
    (ROOT / DATA).write_text(json.dumps(data, indent=2, ensure_ascii=True) + "\n", encoding="utf-8", newline="\n")

    print("49 Financial codes by flow class (denominator %d):" % len(rows49))
    for f in FLOW:
        print("  %s %d" % (f, flow_counts.get(f, 0)))
    print("coverage per_value (denominator %d): %s" % (len(rows49), json.dumps(cov_counts, sort_keys=True)))
    print("inflection descriptions not_observed (%d): %s" % (len(not_observed), json.dumps(not_observed)))
    print("schema_hash %s" % contract["schema_hash"])
    print("wrote %s" % CONTRACT)
    print("wrote %s" % DATA)


SILVER_ONLY_FLOW = {"EXWT": "CORPORATE_ACTION", "RDPC": "CORPORATE_ACTION", "SQDAJ": "UNRESOLVED"}
FIXED_POINTS = {"IRAWH": "EXTERNAL_OUT", "MCE": "EXTERNAL_OUT"}
POSTULATES = {
    "coverage": {
        "mece": "Declared domain: the 160 live 49 Financial codes of the round-124 census, each in exactly one state. MEASURED is a code the "
                "mapping holds as a type word, UNMAPPED_BY_TABLE a code it holds as UNMAPPED, and CODE_NOT_IN_MAPPING a code the mapping lacks. "
                "Subtracting the mapped and the UNMAPPED codes from the 160 leaves none, so CODE_NOT_IN_MAPPING is 0 in the live read and the "
                "per_value counts sum to the denominator.",
        "same_grain": "Grain: one value per transaction line, read from the line's tran_srcde code through source_mapping and computed at row "
                      "build. It is the grain of txn_type and flow_class; it is never an account, a day or a firm total. A code the mapping lacks "
                      "is a line-level value, and the line is counted, never dropped.",
        "intent_coherence": "One intent: say whether the line's code has a ratified reading, so a reader knows whether the txn_type and action "
                            "on the row are the ratified word or the Unclassified display. Each of the three values answers that one question. "
                            "The money direction of a line is a different intent and belongs to flow_class, so coverage never carries it.",
        "state_coherence": "Which values one remedy does NOT move: ratifying an UNMAPPED code as a word moves only that code's rows from "
                           "UNMAPPED_BY_TABLE to MEASURED; a new code in a later read moves only its own rows to CODE_NOT_IN_MAPPING until the "
                           "mapping holds it. Neither remedy moves flow_class, which the CRO table gives per code, nor any other code's coverage.",
    },
    "flow_class_rule": {
        "mece": "Declared domain: the 30 (partition, rule) pairs of the CRO classification table (187 rows, 157 distinct codes). Every pair the "
                "table holds is one of the 30 and the checker finds none outside them, so the subtraction leaves no uncovered pair. Each pair "
                "takes one of the seven classes, and a code whose rows disagree takes UNRESOLVED, so every code has exactly one class.",
        "same_grain": "Grain: one class per tran_srcde code, derived from that code's (partition, rule) rows in the CRO table and carried by each "
                      "line of the code. The rule reads table rows, not account, day or amount values, so a line of the same code always "
                      "carries the same class.",
        "intent_coherence": "One intent: does money cross the account boundary. EXTERNAL_IN and EXTERNAL_OUT say yes, by direction. INTERNAL, "
                            "INCOME and CORPORATE_ACTION say the money stays inside the account. FEE says a charge is taken from the account. "
                            "UNRESOLVED says the table does not settle the question. Every pair is classed by that one question and by nothing else.",
        "state_coherence": "Which values one remedy does NOT move: a specimen that settles one UNRESOLVED pair moves only that pair and the codes "
                           "whose only row it is; it moves no EXTERNAL_IN or EXTERNAL_OUT pair. The silver-only codes and the two fixed codes are "
                           "set in source_mapping and move no pair of the table, so the 30-pair rule is unchanged by them.",
    },
}


if __name__ == "__main__":
    main()
