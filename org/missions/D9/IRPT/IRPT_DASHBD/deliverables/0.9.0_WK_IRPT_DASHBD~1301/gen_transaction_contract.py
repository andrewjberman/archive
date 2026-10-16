"""IRPT_DASHBD round 127 (~F2), cell DB-f-1301 (worker 0.9.0_WK_IRPT_DASHBD~1301).

Generates the FWD-5 transaction contract and its mapping data file from the ratified inputs. Nothing here is typed by hand.

Inputs (read only):
  the ratified proposal  FWD5_WORDS_PROPOSAL_R124.json  (21 type words, 8 action words, 224 mapping rows)
  the CRO table          SCHWAB_TRANSACTION_CODE_CLASSIFICATION_20260811.json  (187 rows: tran_srcde, partition, rule)
  the live census        R124_LIVE_SILVER_CENSUS_49F.json  (160 live 49 Financial codes, 3 silver-only codes)

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
PROPOSAL = D + "0.9.0_WK_IRPT_DASHBD~1001/FWD5_WORDS_PROPOSAL_R124.json"
CENSUS = D + "2.0.0_SA_COO~F2/R124_LIVE_SILVER_CENSUS_49F.json"
CRO = "org/tier1_exec/4.0.0_SA_CRO/deliverables/SCHWAB_TRANSACTION_CODE_CLASSIFICATION_20260811.json"
CONTRACT = "org/standards/IRPT_DASHBD_ACCOUNT_TRANSACTION_CONTRACT.json"
DATA = "data/assets/scripts/gold/irpt_reporting/transaction_words.json"

FIRM49 = "49financial"
FLOW = ["EXTERNAL_IN", "EXTERNAL_OUT", "INCOME", "FEE", "INTERNAL", "CORPORATE_ACTION", "UNRESOLVED"]
COVERAGE = ["MEASURED", "CODE_NOT_IN_MAPPING", "UNMAPPED_BY_TABLE"]

# The issuer's 30-pair rule table, copied from the order (partition, rule, flow_class, reason).
RULE_TABLE = [
    ("CONDITIONAL-BY-COUNTERPARTY", "acct-transfer", "UNRESOLVED",
     "An account transfer is internal only when its counterparty leg is matched, and the line does not carry the counterparty."),
    ("CONDITIONAL-BY-COUNTERPARTY", "journals", "UNRESOLVED",
     "A journal is internal or external by its counterparty, which the line does not carry."),
    ("CONDITIONAL-BY-COUNTERPARTY", "shares-delivered", "UNRESOLVED",
     "A share delivery is internal when its other leg sits in a sister account, and the line does not state which."),
    ("EXTERNAL", "checks-classified", "UNRESOLVED",
     "A classified check's direction is not stated by the rule, so it cannot be classed until a specimen is read."),
    ("EXTERNAL", "returned-deposits", "UNRESOLVED",
     "A returned deposit reverses a deposit whose direction the rule does not state, so the table does not settle its class."),
    ("EXTERNAL-IN", "deposits", "EXTERNAL_IN",
     "The partition is money entering the account from outside the firm."),
    ("EXTERNAL-OUT", "ira-withholding", "EXTERNAL_OUT",
     "The partition is money leaving the account to outside it, and an IRA withholding is paid out of the account."),
    ("EXTERNAL-OUT", "schwab-checks-out", "EXTERNAL_OUT",
     "A check paid out of the account leaves the account to a payee outside it."),
    ("EXTERNAL-OUT", "withdrawals", "EXTERNAL_OUT",
     "A withdrawal moves cash or securities from the account to outside the firm."),
    ("FEE-ADMIN", "adr-fee", "FEE",
     "An administrative fee charged to the account is a fee whatever its label."),
    ("FEE-ADMIN", "service-fees", "FEE",
     "A service fee charged to the account is a fee."),
    ("FEE-MANAGEMENT", "advisor-fee-explicit", "FEE",
     "An explicit advisor fee debited from the account is a management fee, which is a fee."),
    ("FEE-MANAGEMENT", "advisory-fee", "FEE",
     "An advisory fee debited from the account is a fee."),
    ("FEE-MANAGEMENT-VERIFIED", "advisor-fee-verified", "FEE",
     "A verified advisor fee is a fee against the fee record."),
    ("INTERNAL", "alt-income", "INCOME",
     "Alternative income is income earned inside the account, read from the INTERNAL partition, which the return engine treats as inside the account."),
    ("INTERNAL", "cash-in-lieu", "CORPORATE_ACTION",
     "A cash-in-lieu payment for a fractional share is a corporate action inside the account, read from the INTERNAL partition."),
    ("INTERNAL", "corp-actions", "CORPORATE_ACTION",
     "A corporate action on a holding is an event inside the account, read from the INTERNAL partition."),
    ("INTERNAL", "corp-actions-ic", "CORPORATE_ACTION",
     "A corporate action on an in-kind position is an event inside the account, read from the INTERNAL partition."),
    ("INTERNAL", "corp-misc", "CORPORATE_ACTION",
     "A miscellaneous corporate action is an event inside the account, read from the INTERNAL partition."),
    ("INTERNAL", "dividends", "INCOME",
     "A dividend is income earned by the account, read from the INTERNAL partition."),
    ("INTERNAL", "foreign-tax", "INTERNAL",
     "A foreign tax withheld on income is taken inside the account, so it stays an INTERNAL movement."),
    ("INTERNAL", "int-adj-fc", "INCOME",
     "An interest adjustment is income inside the account, read from the INTERNAL partition."),
    ("INTERNAL", "interest", "INCOME",
     "Interest is income earned by the account, read from the INTERNAL partition."),
    ("INTERNAL", "reinvest", "INTERNAL",
     "A reinvestment moves income back into the account, an INTERNAL movement."),
    ("INTERNAL", "sweeps", "INTERNAL",
     "A sweep moves cash between the account's own holdings, an INTERNAL movement."),
    ("INTERNAL", "trades", "INTERNAL",
     "A trade moves value between cash and a position inside the account, an INTERNAL movement."),
    ("INTERNAL", "withholding", "INTERNAL",
     "A withholding taken inside the account is an INTERNAL movement."),
    ("UNRESOLVED", "no-rule", "UNRESOLVED",
     "The table holds no rule for the line, so its class is the table's own unresolved state."),
    ("UNRESOLVED-PENDING-SPECIMEN", "lending-misc-ic", "UNRESOLVED",
     "A lending or miscellaneous in-kind line cannot be classed until a specimen shows its direction."),
    ("UNRESOLVED-PENDING-SPECIMEN", "misc-adj", "UNRESOLVED",
     "A miscellaneous adjustment's cash direction is not stated by the table, so it stays UNRESOLVED until a specimen is read."),
]

# The three silver-only codes and the two fixed in-kind codes, decided by the issuer (the order's step 5).
SILVER_ONLY_FLOW = {"EXWT": "CORPORATE_ACTION", "RDPC": "CORPORATE_ACTION", "SQDAJ": "UNRESOLVED"}
FIXED_POINTS = {"IRAWH": "EXTERNAL_OUT", "MCE": "EXTERNAL_OUT"}

COLUMNS = [
    # name, type, nullable, claim, meaning, method (inferred only)
    ("firm", "string", False, "inferred",
     "The registry-derived firm scope this row belongs to; never a typed token.",
     "The firm scope of the custody entry the silver partition is read under, taken from the registry."),
    ("account_id", "string", False, "measured",
     "The account key carried by the silver row. It is an identifier and is not reproduced in any report.", None),
    ("business_date", "date32[day]", False, "measured",
     "The silver partition's business date, the date= partition the row is written under.", None),
    ("trade_date", "date32[day]", True, "measured",
     "The trade_date column of fact_trn, which the lot source reads; null when the silver row carries none.", None),
    ("settle_date", "date32[day]", True, "absent",
     "The settlement date. No silver column supplies it (round-123 ground read), so the column is null.", None),
    ("action", "string", True, "inferred",
     "The action word of the row: the txn_type's action through type_action. Null only when the code is not in the mapping.",
     "From txn_type through type_action (the type word to its action word)."),
    ("txn_type", "string", False, "inferred",
     "The ratified type word of the row, or the string UNMAPPED when the mapping holds the code as UNMAPPED or lacks it.",
     "From tran_srcde through source_mapping (the 49 Financial code to its ratified type word); UNMAPPED when the mapping holds the code as UNMAPPED or lacks it."),
    ("symbol", "string", True, "measured",
     "The security symbol, the ticker_symbol column; null on a row with no security.", None),
    ("asset_name", "string", True, "absent",
     "The security's name. No silver column supplies it, so the column is null.", None),
    ("units", "double", True, "measured",
     "The quantity column (quantity); null when the row carries none.", None),
    ("price", "double", True, "measured",
     "The price column; null when the row carries none.", None),
    ("amount", "double", False, "measured",
     "The custodian's gross money amount (gross_amount). On a cash row the sign is taken from debit_credit as account_return_daily.py takes it: CREDIT positive, DEBIT negative. On an in-kind row debit_credit is a position side and is not read as a cash sign.", None),
    ("fee", "double", True, "absent",
     "The fee column. The fee rail is unused by design, so no silver column supplies it and the column is null.", None),
    ("custodian", "string", False, "inferred",
     "The custodian of the row, the constant of the custody entry.",
     "The custodian constant of the custody entry the silver partition is read under, set once per entry in the registry."),
    ("flow_class", "string", False, "inferred",
     "The flow class of the row's tran_srcde: EXTERNAL_IN, EXTERNAL_OUT, INCOME, FEE, INTERNAL, CORPORATE_ACTION or UNRESOLVED.",
     "Per tran_srcde through flow_class_rule over the CRO table's (partition, rule) pairs: one class when the code's CRO rows agree, UNRESOLVED when they disagree or the table does not hold the code. The silver-only codes and IRAWH and MCE are fixed in source_mapping."),
    ("source_txn_id", "string", True, "absent",
     "A per-transaction identifier. None is read: order_number is an order-level id and is not used, so the column is null.", None),
    ("coverage", "string", False, "inferred",
     "How the row's code is covered by the mapping: MEASURED, CODE_NOT_IN_MAPPING or UNMAPPED_BY_TABLE.",
     "MEASURED when the code maps to a type word; CODE_NOT_IN_MAPPING when the mapping lacks the code; UNMAPPED_BY_TABLE when the mapping holds the code as UNMAPPED."),
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


def main():
    prop = load(PROPOSAL)
    cro = load(CRO)
    census = load(CENSUS)

    rule_map = {(p, r): f for p, r, f, _ in RULE_TABLE}
    assert len(rule_map) == 30, "rule table must hold 30 pairs"

    # Every CRO (partition, rule) pair must be one of the 30 pairs.
    missing = sorted({(r["partition"], r["rule"]) for r in cro} - set(rule_map))
    if missing:
        sys.exit("ERROR: CRO pairs outside the 30-pair table: %r" % (missing,))

    # Per-code flow class by the rule: one class when every CRO row of the code agrees, else UNRESOLVED.
    per_code = {}
    for r in cro:
        per_code.setdefault(r["tran_srcde"], set()).add(rule_map[(r["partition"], r["rule"])])
    code_flow = {c: (next(iter(s)) if len(s) == 1 else "UNRESOLVED") for c, s in per_code.items()}
    disagree = sorted(c for c, s in per_code.items() if len(s) > 1)

    types = [t["word"] for t in prop["opal_types"]]
    actions = [a["word"] for a in prop["opal_actions"]]
    type_action = {t["word"]: t["action"] for t in prop["opal_types"]}
    assert len(types) == 21 and len(actions) == 8

    silver_only = set(census["silver_only_codes"])
    assert silver_only == set(SILVER_ONLY_FLOW), "silver-only codes differ from the three decided in the order"

    source_mapping = []
    seen = set()
    for m in prop["mapping"]:
        firm, src = m["firm"], m["source_value"]
        assert (firm, src) not in seen, "duplicate proposal row %r" % ((firm, src),)
        seen.add((firm, src))
        if firm == FIRM49:
            assert m["field"] == "tran_srcde"
            if src in SILVER_ONLY_FLOW:
                flow = SILVER_ONLY_FLOW[src]
            elif src in FIXED_POINTS:
                flow = FIXED_POINTS[src]
            else:
                flow = code_flow[src]
            # The 49 Financial rows are the live codes; a live code the CRO table holds is computed by the rule.
        else:
            flow = None
        reason = m.get("reason") if (m["opal_type"] == "UNMAPPED" or (firm == FIRM49 and src in silver_only)) else None
        source_mapping.append({
            "firm": firm,
            "field": m["field"],
            "source_value": src,
            "opal_type": m["opal_type"],
            "flow_class": flow,
            "reason": reason,
        })

    n49 = sum(1 for r in source_mapping if r["firm"] == FIRM49)
    assert n49 == len(census["codes"]) == 160, "49 Financial rows must number the 160 live codes"
    for code in FIXED_POINTS:
        assert any(r["firm"] == FIRM49 and r["source_value"] == code for r in source_mapping)

    columns = []
    for name, typ, nullable, claim, meaning, method in COLUMNS:
        c = {"name": name, "type": typ, "nullable": nullable, "meaning": meaning, "claim": claim}
        if claim == "inferred":
            assert method
            c["method"] = method
        columns.append(c)
    assert [c["name"] for c in columns] == [
        "firm", "account_id", "business_date", "trade_date", "settle_date", "action", "txn_type", "symbol", "asset_name",
        "units", "price", "amount", "fee", "custodian", "flow_class", "source_txn_id", "coverage"]

    contract = {
        "contract_version": "0.1.0",
        "project": "IRPT_DASHBD",
        "prd": "org/missions/D9/IRPT/IRPT_DASHBD/prd/IRPT_DASHBD_PRD.md",
        "authored_by": "0.9.0_WK_IRPT_DASHBD~1301",
        "authored_under": "IRPT_DASHBD.TO-DB-f-1301 (round 127, workstream ~F2, F-SHIP), cell DB-f-1301 of IRPT_DASHBD_DECOMP_R127_F.md, "
                          "following the CTO round-124 analysis for F-SHIP (msg 9097) and the round-123 analysis (msg 9064, ruling 1).",
        "table": "account_transaction",
        "grain": "account x transaction line",
        "partition": "date=YYYY-MM-DD",
        "producer": "data/assets/scripts/gold/irpt_reporting/account_transaction.py",
        "columns": columns,
        "enums": {
            "txn_type": types,
            "action": actions,
            "flow_class": FLOW,
            "coverage": COVERAGE,
        },
        "type_action": type_action,
        "flow_class_rule": [{"partition": p, "rule": r, "flow_class": f, "reason": why} for p, r, f, why in RULE_TABLE],
        "source_mapping": source_mapping,
        "unmapped_display": "Unclassified",
        "new_code_reason": "CODE_NOT_IN_MAPPING",
        "firms_served": [FIRM49],
        "firms_pending": [
            {"firm": "cottonwood",
             "reason": "No producer exists yet. Its ground read is round 126. Its 16 mapping rows are carried with a null flow_class."},
            {"firm": "inflection",
             "reason": "No producer exists yet. Its ground read is round 126. Its 48 mapping rows are carried with a null flow_class."},
        ],
        "rule24_record": {
            "ratified_words": "The ratified proposal " + PROPOSAL + " gives 21 type words with their actions, 8 action words and 224 mapping rows; "
                              "its postulates are MECE, same grain, intent coherence and state coherence.",
            "cvo_grades": "The CVO's grades are not read by this worker: the CVO deliverables are not materialized in this worktree. "
                          "The order cites them through the CTO round-124 analysis.",
            "cto_ratification": "1.0.0_SA_CTO~DELL2 message 9097 ratified the FWD-5 words: flow class per code from the CRO classification table; "
                                "UNMAPPED shown as Other with its count; a code not in the mapping reads CODE_NOT_IN_MAPPING and is counted, never dropped.",
            "analysis_path": "org/tier1_exec/1.0.0_SA_CTO/deliverables/CTO_ROUND_ANALYSIS_IRPT_DASHBD_F-SHIP_ROUND_124_20261016.md",
            "round_123_ruling": "Message 9064, ruling 1: a field the producer computes carries inferred and a method, never absent.",
        },
        "schema_hash": schema_hash(columns),
        "schema_hash_basis": "sha256 over the sorted 'name:type' lines of columns joined by newline, types as the pyarrow type name the producer's "
                             "ARROW_SCHEMA carries (the same method as the account_class_daily and account_return_daily contracts).",
        "served": False,
        "served_note": "Nothing is written. No object of this table exists in any bucket. The release is a never-widen act that waits on this "
                       "contract and on the producer (DB-f-1302), under a CTO and COO sign-off.",
    }

    data = {
        "contract_version": contract["contract_version"],
        "type_action": contract["type_action"],
        "source_mapping": contract["source_mapping"],
    }

    ascii_check(contract, CONTRACT)
    ascii_check(data, DATA)

    (ROOT / CONTRACT).write_text(json.dumps(contract, indent=2, ensure_ascii=True) + "\n", encoding="utf-8", newline="\n")
    (ROOT / DATA).write_text(json.dumps(data, indent=2, ensure_ascii=True) + "\n", encoding="utf-8", newline="\n")

    # Summary for the report (counts only).
    cls = Counter(r["flow_class"] for r in source_mapping if r["firm"] == FIRM49)
    print("49 Financial codes by flow class:")
    for f in FLOW:
        print("  %s %d" % (f, cls.get(f, 0)))
    print("49 Financial total %d" % sum(cls.values()))
    print("codes UNRESOLVED because CRO rows disagree: %s" % ", ".join(
        c for c in disagree if any(r["source_value"] == c and r["firm"] == FIRM49 for r in source_mapping)))
    print("schema_hash %s" % contract["schema_hash"])
    print("wrote %s" % CONTRACT)
    print("wrote %s" % DATA)


if __name__ == "__main__":
    main()
