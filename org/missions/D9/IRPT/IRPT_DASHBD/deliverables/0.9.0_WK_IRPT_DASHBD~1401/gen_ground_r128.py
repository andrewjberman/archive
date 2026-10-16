"""Generate the three FWD-5 ground records (DB-f-1401) from the issuer's live census.

Run from the worktree root: python -I .scratch/gen_r128.py
Reads only the issuer's census record; writes only the three records in the worker's folder.
"""
import json
import sys
from pathlib import Path

ROOT = Path(".").resolve()
D = "org/missions/D9/IRPT/IRPT_DASHBD/deliverables/"
CENSUS_REL = D + "2.0.0_SA_COO~F2/R128_LIVE_SOURCE_CENSUS_3FIRMS.json"
OUT = ROOT / D / "0.9.0_WK_IRPT_DASHBD~1401"
TARGETS = ("trade_date", "settle_date", "action", "txn_type", "symbol", "asset_name", "units", "price", "amount",
           "fee", "custodian", "flow_class", "source_txn_id", "coverage")

# Each row: (target, source, from_columns, claim, method, words, absent)
# absent=True means searched_columns is the firm's full live column list.


def sourced(t, src, claim, words, method=None):
    return (t, src, [], claim, method, words, False)


def computed(t, frm, method, words):
    return (t, None, frm, "inferred", method, words, False)


def absent(t, words):
    return (t, None, [], "absent", None, words, True)


FIRMS = {}

FIRMS["49financial"] = {
    "table_key": "49financial",
    "rows": [
        sourced("trade_date", "trade_date", "measured",
                "The trade_date column of the transaction table, named as the field; the lot source reads it as the closing trade's trade date."),
        sourced("settle_date", "settlmnt_date", "measured",
                "The settlmnt_date column of the transaction table, named as the settlement date. The round-123 absent claim is void: the live schema carries the column."),
        computed("action", ["tran_srcde"],
                 "tran_srcde through source_mapping to the ratified type word, then type_action (the type word to its action word); a code the mapping holds as UNMAPPED or lacks gives a null action.",
                 "No column carries the action word itself. It is the action word of the type word the source code maps to."),
        sourced("txn_type", "tran_srcde", "inferred",
                "The source code column read through the ratified source_mapping (the 49 Financial code to its type word); UNMAPPED when the mapping holds the code as UNMAPPED or lacks it.",
                "tran_srcde through source_mapping (the 49 Financial code to its ratified type word); UNMAPPED when the mapping holds the code as UNMAPPED or lacks it."),
        sourced("symbol", "ticker_symbol", "measured",
                "The ticker_symbol column, named as the security symbol; sources.json trade_identifier_columns names it first."),
        absent("asset_name",
               "Searched every column for a security or issue name: none of the transaction table's columns is named as one. The security is identified by ticker_symbol and cusip (sources.json trade_identifier_columns). transaction_detail_description was considered and rejected: it is free transaction text that the producer carries for same-account type-transfer grammar, not a security name."),
        sourced("units", "quantity", "measured",
                "The quantity column, named as the units; the in-kind valuation reads quantity as the transferred units (sources.json inkind_quantity_column)."),
        sourced("price", "price", "measured",
                "The price column of the transaction table; the in-kind price key reads it (sources.json inkind_price_column)."),
        sourced("amount", "gross_amount", "inferred",
                "gross_amount is the custodian's gross money amount, the money column the adapter declares. The sign is taken from debit_credit on cash rows; net_amount is never read.",
                "gross_amount, the money column the adapter declares (money_column). The sign is taken from debit_credit on cash rows: CREDIT positive, DEBIT negative (direction_map)."),
        computed("fee", ["commission", "exchange_processing_fee", "broker_service_fee", "prime_broker_fee",
                         "trade_away_fee", "redemption_fee", "other_fee", "step_in_fee", "research_fee"],
                 "Per row, the sum of the fee-named columns listed in from_columns and of commission; null when every listed column is null. markupmarkdown is not summed (a price markup, not a fee charge) and exec_brok_comm is not summed (its meaning as a fee is not established from the census or the tracked records).",
                 "The table holds nine fee-named or commission columns, so the fee is a computed total of them. Excluded columns are named in the method with the reason."),
        sourced("custodian", "custdian_id", "inferred",
                "The custdian_id column, read as the custodian identity of the row. The census holds no values, so the value set is not read; the custody entry's registry constant remains the cross-check.",
                "The custodian identity column of the row (custdian_id). Its values are not read by the census; the claim is inferred from the column name."),
        computed("flow_class", ["tran_srcde", "tr_cd", "sb_cd"],
                 "Per the three-part key (tran_srcde, tr_cd, sb_cd) through the classification table's (partition, rule) rows: one class when the key's rows agree, UNRESOLVED when they disagree or the table does not hold the key. The silver-only codes and the two fixed codes are fixed in source_mapping.",
                 "The classification key is the three transaction key columns; the table is keyed on them."),
        sourced("source_txn_id", "cashiering_transaction_identifier", "inferred",
                "The cashiering_transaction_identifier column, read as the per-transaction identifier by its name. schwab_cashiering_unique_id is the other cashiering identifier and is not used. The census holds no values.",
                "The per-transaction cashiering identifier column, read by name; values not read."),
        computed("coverage", ["tran_srcde"],
                 "MEASURED when tran_srcde maps to a type word; CODE_NOT_IN_MAPPING when the mapping lacks the code; UNMAPPED_BY_TABLE when the mapping holds the code as UNMAPPED.",
                 "Coverage is a function of how the source code is covered by the mapping."),
    ],
}

FIRMS["cottonwood"] = {
    "table_key": "cottonwood",
    "rows": [
        sourced("trade_date", "Trade Date", "measured",
                "The Trade Date column, named as the field."),
        sourced("settle_date", "Settle Date", "measured",
                "The Settle Date column, named as the field."),
        computed("action", ["Action", "Transaction Type"],
                 "The vendor Action value (87 distinct values) mapped to the Opal action word; where the Action value carries no action word, the action word of the Transaction Type through type_action.",
                 "The vendor Action column has 87 values and is mapped to the Opal action enum."),
        sourced("txn_type", "Transaction Type", "inferred",
                "The Transaction Type column (16 values) read through the ratified source_mapping rows for the type field.",
                "Transaction Type (16 values) through the ratified source_mapping rows for the type field."),
        sourced("symbol", "Symbol", "measured",
                "The Symbol column, named as the security symbol."),
        sourced("asset_name", "Asset Name", "measured",
                "The Asset Name column, named as the security's name."),
        sourced("units", "Units", "measured",
                "The Units column, named as the units."),
        sourced("price", "Price", "measured",
                "The Price column, named as the price."),
        sourced("amount", "Market Value", "inferred",
                "The Market Value column is the transaction's money value column read as the money amount. The census holds no values, so the sign and the transaction-versus-position reading are inferred, not measured.",
                "The transaction money value column. The census holds no values; the reading is inferred from the column name."),
        computed("fee", ["Transaction Fee", "Account Fee"],
                 "Per row, the sum of Transaction Fee and Account Fee; null when both are null.",
                 "The table holds two fee columns, so the fee is a computed total of them."),
        sourced("custodian", "Custodian", "measured",
                "The Custodian column, named as the custodian."),
        computed("flow_class", ["External Flow", "Transaction Type", "Transaction Sub Type"],
                 "Per row: External Flow Contribution maps to EXTERNAL_IN and Withdrawal to EXTERNAL_OUT; a None External Flow takes the class of the (Transaction Type, Transaction Sub Type) pair under the ratified pair rules (the census pairs table, 33 pairs).",
                 "External Flow with the pair; the census pairs table is the basis."),
        sourced("source_txn_id", "TransactionID", "measured",
                "The TransactionID column, named as the per-transaction identifier."),
        computed("coverage", ["Transaction Type", "Transaction Sub Type"],
                 "MEASURED when the (Transaction Type, Transaction Sub Type) pair is in the mapping; CODE_NOT_IN_MAPPING when the mapping lacks the pair; UNMAPPED_BY_TABLE when the mapping holds the pair as UNMAPPED.",
                 "Coverage is a function of how the type pair is covered by the mapping."),
    ],
}

FIRMS["inflection"] = {
    "table_key": "inflection",
    "rows": [
        sourced("trade_date", "transDate", "inferred",
                "The transDate column, read as the trade date: the feed carries no separate trade-date column, and whether its date equals the trade date is not established by the census.",
                "The transaction date column read as the trade date; equality with the trade date is not established."),
        absent("settle_date",
               "Searched every column for a settlement date: none of the 36 columns is a settle or settlement date. transDate and executionTime are the transaction date columns and neither is a settle date; pull_date is the feed pull date."),
        computed("action", ["transactionDescription"],
                 "transactionDescription (47 values) through the contract's source_mapping rows for the Inflection type field, then the type word's action word through type_action.",
                 "No column carries the action word itself. It is computed from the description through the type mapping."),
        sourced("txn_type", "transactionDescription", "inferred",
                "The transactionDescription column (47 values) read through the contract's source_mapping rows for the Inflection type field. The ratified Orion taxonomy keys on the same description text.",
                "transactionDescription (47 values) through the contract's source_mapping rows for the Inflection type field; the Orion cashflow taxonomy keys on the same text."),
        sourced("symbol", "ticker", "measured",
                "The ticker column, named as the security symbol."),
        sourced("asset_name", "productName", "inferred",
                "The productName column (1675 distinct values, one per product) read as the security or product name. The census shows its distinct count, not its values.",
                "productName read as the product's name; the census shows its distinct count only."),
        sourced("units", "noUnits", "measured",
                "The noUnits column, named as the units."),
        sourced("price", "avgPrice", "inferred",
                "The avgPrice column, read as the average execution price. navPrice is the fund NAV and is not used as the transaction price. The column is a string in the live schema.",
                "avgPrice read as the average execution price; navPrice is the NAV and is not used."),
        sourced("amount", "transAmount", "measured",
                "The transAmount column, named as the transaction amount."),
        absent("fee",
               "Searched every column for a fee amount: no column is named as a fee or charge. The fee descriptions (Management Fee, Trading Expense, Fee Credit and others) are values of transactionDescription, not columns."),
        sourced("custodian", "custodianName", "measured",
                "The custodianName column, named as the custodian."),
        computed("flow_class", ["transactionDescription"],
                 "The description's ratified bucket in the Orion cashflow taxonomy gives the class: NNA as EXTERNAL_IN or EXTERNAL_OUT by the description's direction, Return as INCOME or FEE by the description, Internal as INTERNAL, CorporateAction as CORPORATE_ACTION; a description the taxonomy lacks is UNRESOLVED.",
                 "The taxonomy keys on the description text; the bucket gives the class."),
        sourced("source_txn_id", "id", "inferred",
                "The id column, read as the per-transaction identifier by its name. The census holds no values to confirm uniqueness.",
                "The table row identifier column read as the per-transaction identifier; values not read."),
        computed("coverage", ["transactionDescription"],
                 "MEASURED when the description maps to a type word in the contract's source_mapping; CODE_NOT_IN_MAPPING when the mapping lacks it; UNMAPPED_BY_TABLE when the mapping holds it as UNMAPPED.",
                 "Coverage is a function of how the description is covered by the mapping."),
    ],
}


def build(firm_key, census_firm):
    spec = FIRMS[firm_key]
    cols = census_firm["columns"]
    colset = set(cols)
    targets = []
    for (t, src, frm, claim, method, words, is_abs) in spec["rows"]:
        if is_abs:
            searched = list(cols)
        else:
            searched = None
        if src is not None:
            assert src in colset, (firm_key, t, src)
        for f in frm:
            assert f in colset, (firm_key, t, f)
        targets.append({"target": t, "source": src, "from_columns": frm, "claim": claim,
                        "method": method, "words": words, "searched_columns": searched})
    assert [x["target"] for x in targets] == list(TARGETS), firm_key
    absent_count = sum(1 for x in targets if x["claim"] == "absent")
    computed_count = sum(1 for x in targets if x["source"] is None and x["claim"] == "inferred")
    return {
        "as_of": "2026-10-16",
        "firm": firm_key,
        "source_reads": {"census": CENSUS_REL,
                         "partitions_read": census_firm["partitions_read"],
                         "rows": census_firm["rows"],
                         "column_count": census_firm["column_count"]},
        "targets": targets,
        "absent_count": absent_count,
        "computed_count": computed_count,
        "worker_reads": {"s3_reads": 0, "s3_writes": 0, "dynamodb_writes": 0, "vendor_calls": 0, "secret_reads": 0},
        "files_in_repo": False,
        "served_values_changed": False,
        "pushed": False,
        "deployed": False,
    }


def main():
    census = json.loads((ROOT / CENSUS_REL).read_text(encoding="utf-8"))
    OUT.mkdir(parents=True, exist_ok=True)
    names = {"49financial": "RD_FWD5_GROUND_49FINANCIAL_R128.json",
             "cottonwood": "RD_FWD5_GROUND_COTTONWOOD_R128.json",
             "inflection": "RD_FWD5_GROUND_INFLECTION_R128.json"}
    for firm_key in ("49financial", "cottonwood", "inflection"):
        rec = build(firm_key, census["firms"][firm_key])
        text = json.dumps(rec, indent=2, ensure_ascii=True) + "\n"
        (OUT / names[firm_key]).write_text(text, encoding="ascii")
        print("WROTE", names[firm_key], "absent", rec["absent_count"], "computed", rec["computed_count"])
    return 0


if __name__ == "__main__":
    sys.exit(main())
