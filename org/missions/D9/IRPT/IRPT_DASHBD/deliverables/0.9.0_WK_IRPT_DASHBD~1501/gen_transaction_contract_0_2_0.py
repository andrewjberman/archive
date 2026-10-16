"""IRPT_DASHBD round 129 (~F2), cell DB-f-1501 (worker 0.9.0_WK_IRPT_DASHBD~1501).

Generates the FWD-5 transaction contract 0.2.0 and its mapping data file. Nothing here is typed by hand: every source binding,
every claim, every fee basis and every census is read from the inputs below.

Inputs (read only):
  the three round-128 ground-read records  RD_FWD5_GROUND_{49FINANCIAL,COTTONWOOD,INFLECTION}_R128.json
  the live census (round 128)               R128_LIVE_SOURCE_CENSUS_3FIRMS.json  (Inflection transactionDescription values)
  the ratified proposal                     FWD5_WORDS_PROPOSAL_R124.json  (21 type words, 8 action words, 224 mapping rows)
  the CRO table                             SCHWAB_TRANSACTION_CODE_CLASSIFICATION_20260811.json  (187 rows)
  the live 49 Financial code census         R124_LIVE_SILVER_CENSUS_49F.json  (160 codes)
  the draft contract 0.1.0 (only its 30-pair flow_class_rule, carried with its reasons, before it is overwritten)

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
GROUND_D = D + "0.9.0_WK_IRPT_DASHBD~1401/"
PROPOSAL = D + "0.9.0_WK_IRPT_DASHBD~1001/FWD5_WORDS_PROPOSAL_R124.json"
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
# For a brief column the claim and the method come from the 49 Financial ground read; the method below is used only where the
# ground read's method does not describe the producer's key (flow_class) or where the column is not a brief target.
COLUMNS = [
    ("firm", "string", False, "inferred",
     "The registry-derived firm scope this row belongs to; never a typed token.",
     "The firm scope of the custody entry the silver partition is read under, taken from the registry."),
    ("account_id", "string", False, "measured",
     "The account key carried by the silver row. It is an identifier and is not reproduced in any report.", None),
    ("business_date", "date32[day]", False, "measured",
     "The silver partition's business date, the date= partition the row is written under.", None),
    ("trade_date", "date32[day]", True, None,
     "The trade_date column of the transaction table, read as the closing trade's trade date (round-128 ground read); null when the row carries none.",
     None),
    ("settle_date", "date32[day]", True, None,
     "The settlement date: the settlmnt_date column of the transaction table (round-128 ground read). The round-123 absent claim is void; "
     "the live schema carries the column. Null when the value is missing or unparsable.", None),
    ("action", "string", True, None,
     "The action word of the row: the txn_type's action through type_action. Null only when the code is not in the mapping.", None),
    ("txn_type", "string", False, None,
     "The ratified type word of the row, or the string UNMAPPED when the mapping holds the code as UNMAPPED or lacks it.", None),
    ("symbol", "string", True, None,
     "The security symbol, the ticker_symbol column; null on a row with no security.", None),
    ("asset_name", "string", True, None,
     "The security's name. The live schema (140 columns) has no name column (round-128 ground read), so the column is null on every row.",
     None),
    ("units", "double", True, None,
     "The quantity column, named as the units (round-128 ground read); null when the row carries none.", None),
    ("price", "double", True, None,
     "The price column (round-128 ground read); null when the row carries none.", None),
    ("amount", "double", False, None,
     "The custodian's gross money amount (gross_amount). On a cash row the sign is taken from debit_credit as account_return_daily takes it: "
     "CREDIT positive, DEBIT negative. On an in-kind row debit_credit is a position side and is not read as a cash sign.", None),
    ("fee", "double", True, None,
     "The stated sum, for 49 Financial, of the columns the contract's fee_basis names (commission, exchange_processing_fee, "
     "broker_service_fee, prime_broker_fee, trade_away_fee, redemption_fee, other_fee, step_in_fee, research_fee). A null column counts as "
     "nothing; a row whose named columns are all null has fee null, never zero.", None),
    ("custodian", "string", False, "inferred",
     "The custodian of the row: the custody entry's constant (sources.json custodian). The round-128 ground read names custdian_id as the "
     "custodian identity column; the constant is what a person reads, and custdian_id is not read onto the row.",
     "The custodian constant of the custody entry the silver partition is read under, set once per entry in the registry."),
    ("flow_class", "string", False, None,
     "The flow class of the row's tran_srcde code: EXTERNAL_IN, EXTERNAL_OUT, INCOME, FEE, INTERNAL, CORPORATE_ACTION or UNRESOLVED.",
     "Per tran_srcde through flow_class_rule over the CRO table's (partition, rule) pairs: one class when the code's CRO rows agree, "
     "UNRESOLVED when they disagree or the table does not hold the code. The silver-only codes and IRAWH and MCE are fixed in source_mapping. "
     "The round-128 ground read names the key (tran_srcde, tr_cd, sb_cd); this contract keys on tran_srcde, the key source_mapping holds."),
    ("source_txn_id", "string", True, None,
     "The per-transaction identifier: the cashiering_transaction_identifier column (round-128 ground read), read by name; null when the "
     "row carries none.", None),
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
FEE_RULE_CW = ("The fee is the stated sum of Transaction Fee and Account Fee per line. A null column counts as nothing. A line whose two "
               "columns are both null has fee null, never zero. No producer exists yet (firms_pending).")

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

SILVER_ONLY_FLOW = {"EXWT": "CORPORATE_ACTION", "RDPC": "CORPORATE_ACTION", "SQDAJ": "UNRESOLVED"}
FIXED_POINTS = {"IRAWH": "EXTERNAL_OUT", "MCE": "EXTERNAL_OUT"}


def ascii_check(obj, label):
    text = json.dumps(obj, ensure_ascii=False)
    if not text.isascii():
        sys.exit("ERROR: non-ASCII text in " + label)


def load(rel):
    return json.loads((ROOT / rel).read_text(encoding="utf-8"))


def schema_hash(columns):
    lines = sorted("%s:%s" % (c["name"], c["type"]) for c in columns)
    return hashlib.sha256("\n".join(lines).encode("ascii")).hexdigest()


def main():
    old = load(CONTRACT)  # the draft 0.1.0: its 30-pair rule is carried with its reasons
    rule_table = [(r["partition"], r["rule"], r["flow_class"], r["reason"]) for r in old["flow_class_rule"]]
    assert len(rule_table) == 30, "the draft's flow_class_rule must hold 30 pairs"
    rule_map = {(p, r): f for p, r, f, _ in rule_table}

    prop = load(PROPOSAL)
    cro = load(CRO)
    cen124 = load(CENSUS124)
    cen128 = load(CENSUS128)
    ground = {f: load(p) for f, p in GROUND.items()}

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

    # The ground reads' per-target claim and method for the brief targets.
    targets = {f: {t["target"]: t for t in ground[f]["targets"]} for f in ground}
    for f in ground:
        assert [t["target"] for t in ground[f]["targets"]] == BRIEF14, "ground order differs in " + f

    # Columns: the claim of each brief column is the 49 Financial ground read's claim for that target.
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
        c = {"name": name, "type": typ, "nullable": nullable, "meaning": meaning, "claim": claim}
        if claim == "inferred":
            assert method, "an inferred column needs a method: " + name
            c["method"] = method
        columns.append(c)
    assert [c["name"] for c in columns] == ["firm", "account_id", "business_date", "trade_date", "settle_date", "action", "txn_type",
                                            "symbol", "asset_name", "units", "price", "amount", "fee", "custodian", "flow_class",
                                            "source_txn_id", "coverage"]

    # Sources: each firm's 14 entries as its ground read has them.
    sources = {}
    for f in (FIRM49, FIRM_CW, FIRM_INF):
        sources[f] = [{"target": t["target"], "source": t["source"], "from_columns": t["from_columns"], "claim": t["claim"],
                       "method": t["method"]} for t in ground[f]["targets"]]

    fee_basis = {}
    for f in (FIRM49, FIRM_CW):
        fee = targets[f]["fee"]
        fee_basis[f] = {"columns": list(fee["from_columns"]),
                        "rule": FEE_RULE_49F if f == FIRM49 else FEE_RULE_CW}
    fee_basis[FIRM_INF] = None
    assert targets[FIRM_INF]["fee"]["from_columns"] == [] and targets[FIRM_INF]["fee"]["source"] is None

    # Mapping rows: 49 Financial and Inflection from the ratified proposal; no Cottonwood row.
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

    contract = {
        "contract_version": "0.2.0",
        "supersedes": "0.1.0 (a draft, never ratified)",
        "project": "IRPT_DASHBD",
        "prd": PRD,
        "authored_by": "0.9.0_WK_IRPT_DASHBD~1501",
        "authored_under": "IRPT_DASHBD.TO-DB-f-1501 (round 129, workstream ~F2, F-SHIP), cell DB-f-1501 of IRPT_DASHBD_DECOMP_R129_F.md, "
                          "following the CTO round-127 analysis for F-SHIP (msg 9162: 0.1.0 is a draft; 0.2.0 names the source column of every "
                          "target per firm, the fee as a stated sum with its basis, and the rule-24 records).",
        "table": "account_transaction",
        "grain": "account x transaction line",
        "partition": "date=YYYY-MM-DD",
        "producer": "data/assets/scripts/gold/irpt_reporting/account_transaction.py",
        "columns": columns,
        "sources": sources,
        "fee_basis": fee_basis,
        "enums": {
            "txn_type": types,
            "action": actions,
            "flow_class": FLOW,
            "coverage": COVERAGE,
        },
        "type_action": type_action,
        "flow_class_rule": [{"partition": p, "rule": r, "flow_class": f, "reason": why} for p, r, f, why in rule_table],
        "source_mapping": source_mapping,
        "unmapped_display": "Unclassified",
        "new_code_reason": "CODE_NOT_IN_MAPPING",
        "firms_served": [FIRM49],
        "firms_pending": [
            {"firm": FIRM_CW,
             "reason": "No producer exists yet. Its ground read is round 128 (RD_FWD5_GROUND_COTTONWOOD_R128.json) and its table fills all 14 "
                       "targets. Its re-cut words (33 type pairs and 87 Action values) are a proposal awaiting ratification, so no Cottonwood "
                       "row is in source_mapping."},
            {"firm": FIRM_INF,
             "reason": "No producer exists yet. Its ground read is round 128: settle_date and fee are absent from its 36 columns. 47 of the 48 "
                       "ratified descriptions are live in the census; the 48th is marked not_observed."},
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
        "schema_hash": schema_hash(columns),
        "schema_hash_basis": SCHEMA_BASIS,
        "served": False,
        "served_note": "Nothing is written. No object of this table exists in any bucket. 0.2.0 supersedes the draft 0.1.0, which was never "
                       "ratified. The release is a never-widen act that waits on this contract, on the producer and on the CVO's judgment at "
                       "L9 (DBF129-1-J1), under a CTO and COO sign-off.",
    }

    data = {
        "contract_version": contract["contract_version"],
        "type_action": contract["type_action"],
        "source_mapping": contract["source_mapping"],
        "fee_basis": contract["fee_basis"],
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


if __name__ == "__main__":
    main()
