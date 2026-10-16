"""IRPT_DASHBD round 133 (~F2), cell DB-f-1901 (worker 0.9.0_WK_IRPT_DASHBD~1901): the 0.4.1 generator (round 132, DB-f-1801) changed for the
CTO's final S6 ruling (ADDENDUM 2, msg 9382). Only these change: contract_version 0.4.2, supersedes, authored_by, s6_status, served_note and the
new s6_ruling section.

Generates the FWD-5 transaction contract 0.4.2 and its mapping data file. Adapted from the round-131 generator
(deliverables/0.9.0_WK_IRPT_DASHBD~1701/gen_transaction_contract_0_4_0.py). Round 132 states the CTO's round-131 rulings: one business_date
for all three firms (first_trading_day_on_or_after, lib/trading_calendar.py), the Inflection price on a fund-family line only, the
Reversed offsets with their originals, and the issuer's round-132 censuses as measured claims. Nothing here is typed by hand that a file holds: every
source binding, claim, fee basis, census, coverage figure and read is read from the inputs below. Every source_key is computed BY THIS
SCRIPT calling the module's own normalise_key and pair_key (imported from account_transaction.py), never retyped. Every Inflection
flow class is derived from the inflection_flow_rule table through the taxonomy file's (bucket, nna_direction, account_boundary).

Inputs (read only):
  the three round-128 ground-read records     RD_FWD5_GROUND_{49FINANCIAL,COTTONWOOD,INFLECTION}_R128.json (1401)
  the live census (round 128)                R128_LIVE_SOURCE_CENSUS_3FIRMS.json (2.0.0_SA_COO~F2)
  the live 49 Financial code census          R124_LIVE_SILVER_CENSUS_49F.json (160 codes)
  the Inflection field census (round 131)    R131_INFLECTION_FIELD_CENSUS.json (values-free counts)
  the Inflection fund-family census (round 132) R132_INFLECTION_CENSUS.json (values-free counts; fund_family, reversed)
  the Inflection pairing census (round 132)  R132_INFLECTION_PAIRING_CENSUS.json (S6 pairing; Reversed offset candidates)
  the 49 Financial business_date census (132) R132_F49_BUSINESS_DATE_CENSUS.json (values-free counts)
  the Inflection S6 census v2 (round 133)    R132_INFLECTION_S6_CENSUS_V2.json (values-free counts; the s6_ruling section)
  the ratified proposal                      FWD5_WORDS_PROPOSAL_R124.json (1001)
  the ratified Cottonwood record             FWD5_WORDS_COTTONWOOD_R128.json (1402)
  the CRO table                              SCHWAB_TRANSACTION_CODE_CLASSIFICATION_20260811.json
  the Orion taxonomy                         data/inf/scripts/silver/orion_cashflow_taxonomy.yaml
  the worker's own reads (round 130)         RD_READS_R130.json and RD_ID_COVERAGE_R130.json (1601, unchanged)
  the 0.4.0 contract on trunk                its flow_class_rule (30 pairs, with reasons), read BEFORE it is overwritten

Outputs (written):
  org/standards/IRPT_DASHBD_ACCOUNT_TRANSACTION_CONTRACT.json
  data/assets/scripts/gold/irpt_reporting/transaction_words.json

Run from the worktree root:  python -I <this file>
"""
import hashlib
import importlib.util
import json
import sys
from collections import Counter
from pathlib import Path

import yaml

ROOT = Path(".")
D = "org/missions/D9/IRPT/IRPT_DASHBD/deliverables/"
MINE = D + "0.9.0_WK_IRPT_DASHBD~1801/"
GROUND_D = D + "0.9.0_WK_IRPT_DASHBD~1401/"
PROPOSAL = D + "0.9.0_WK_IRPT_DASHBD~1001/FWD5_WORDS_PROPOSAL_R124.json"
COTTONWOOD_REC = D + "0.9.0_WK_IRPT_DASHBD~1402/FWD5_WORDS_COTTONWOOD_R128.json"
READS = D + "0.9.0_WK_IRPT_DASHBD~1601/RD_READS_R130.json"
IDCOV = D + "0.9.0_WK_IRPT_DASHBD~1601/RD_ID_COVERAGE_R130.json"
CENSUS124 = D + "2.0.0_SA_COO~F2/R124_LIVE_SILVER_CENSUS_49F.json"
CENSUS128 = D + "2.0.0_SA_COO~F2/R128_LIVE_SOURCE_CENSUS_3FIRMS.json"
FIELDS = D + "2.0.0_SA_COO~F2/R131_INFLECTION_FIELD_CENSUS.json"
C132_INF = D + "2.0.0_SA_COO~F2/R132_INFLECTION_CENSUS.json"
C132_PAIR = D + "2.0.0_SA_COO~F2/R132_INFLECTION_PAIRING_CENSUS.json"
C132_F49 = D + "2.0.0_SA_COO~F2/R132_F49_BUSINESS_DATE_CENSUS.json"
CV2 = D + "2.0.0_SA_COO~F2/R132_INFLECTION_S6_CENSUS_V2.json"
ADDENDUM = "org/tier1_exec/1.0.0_SA_CTO/deliverables/CTO_ROUND_ANALYSIS_IRPT_DASHBD_F-SHIP_ROUND_131_20261016.md"
ADDENDUM_PIN = "a5475b2fdd"
CRO ="org/tier1_exec/4.0.0_SA_CRO/deliverables/SCHWAB_TRANSACTION_CODE_CLASSIFICATION_20260811.json"
TAXONOMY = "data/inf/scripts/silver/orion_cashflow_taxonomy.yaml"
MODULE = "data/assets/scripts/gold/irpt_reporting/account_transaction.py"
CONTRACT = "org/standards/IRPT_DASHBD_ACCOUNT_TRANSACTION_CONTRACT.json"
DATA = "data/assets/scripts/gold/irpt_reporting/transaction_words.json"
PRD = "org/missions/D9/IRPT/IRPT_DASHBD/prd/IRPT_DASHBD_PRD.md"
GROUND = {"49financial": GROUND_D + "RD_FWD5_GROUND_49FINANCIAL_R128.json",
          "cottonwood": GROUND_D + "RD_FWD5_GROUND_COTTONWOOD_R128.json",
          "inflection": GROUND_D + "RD_FWD5_GROUND_INFLECTION_R128.json"}

FIRM49 = "49financial"
FIRM_CW = "cottonwood"
FIRM_INF = "inflection"
UNMAPPED = "UNMAPPED"
TRANSFER_OUT_PAIR = "Transfer Out | Transfer Out"
CW_TRANSFER_OUT_RULING = "EXTERNAL_OUT"  # the CTO's round-128 ruling (msg 9175)
CW_TRANSFER_OUT_REASON = ("Transfer Out type and sub type. The live read of round 130 finds no null Action in Cottonwood (87 values, none "
                          "missing), so the lines that the round-128 analysis counted as lacking an Action are the lines whose External Flow "
                          "is None. By the CTO's round-128 ruling (msg 9175) the pair's class for lines marked None is EXTERNAL_OUT; no line "
                          "is dropped or left blank.")
CW_ACTION_DERIVATION = ("A Cottonwood line whose vendor Action is null or blank (after normalising, round 131) derives its action word from "
                        "its (Transaction Type, Transaction Sub Type) pair through the type table (type_action), the same rule as a 49 "
                        "Financial code with no action field. The live read finds no null Action in Cottonwood, so this is a stated "
                        "fallback that no observed line uses; the Action values that the vendor does carry map through "
                        "cottonwood_mapping.actions.")
SILVER_ONLY_FLOW = {"EXWT": "CORPORATE_ACTION", "RDPC": "CORPORATE_ACTION", "SQDAJ": "UNRESOLVED"}
FIXED_POINTS = {"IRAWH": "EXTERNAL_OUT", "MCE": "EXTERNAL_OUT"}
FLOW = ["EXTERNAL_IN", "EXTERNAL_OUT", "INCOME", "FEE", "INTERNAL", "CORPORATE_ACTION", "UNRESOLVED"]
COVERAGE = ["MEASURED", "CODE_NOT_IN_MAPPING", "UNMAPPED_BY_TABLE"]
BRIEF14 = ["trade_date", "settle_date", "action", "txn_type", "symbol", "asset_name", "units", "price", "amount", "fee",
           "custodian", "flow_class", "source_txn_id", "coverage"]
SCHEMA_BASIS = ("sha256 over the sorted 'name:type' lines of columns joined by newline, types as the pyarrow type name the producer's "
                "ARROW_SCHEMA carries (the same method as the account_class_daily and account_return_daily contracts).")
KEY_RULE = ("strip surrounding whitespace and nothing else; case is kept; the mapping's keys and every producer's lookup use this one "
            "function")

# Column specs: name, type, nullable, own claim (None = the 49 Financial ground read's claim for the target), meaning, own method.
COLUMNS = [
    ("firm", "string", False, "inferred",
     "The registry-derived firm scope this row belongs to; never a typed token.",
     "The firm scope of the custody entry the silver partition is read under, taken from the registry."),
    ("account_id", "string", False, "measured",
     "The account key carried by the silver row. It is an identifier and is not reproduced in any report.", None),
    ("business_date", "date32[day]", False, "measured",
     "The business date of the row, the date= partition it is written under: the first NYSE trading day on or after the trade date, "
     "computed by first_trading_day_on_or_after in lib/trading_calendar.py (window 14 days) for ALL THREE firms (contract 0.4.1, the CTO's "
     "round-131 ruling). 49 Financial: from its trade_date; the silver business_date column is not the answer. Cottonwood: from its Trade "
     "Date (the adapter's performance day). Inflection: from its transDate, so a Saturday or Sunday transDate rolls to the Monday.",
     None),
    ("trade_date", "date32[day]", True, None,
     "The trade date of the row, the source date as received and never rolled: the trade_date column of the 49 Financial table (round-128 "
     "ground read), the Trade Date of Cottonwood, the transDate of Inflection. A 49 Financial line with no readable trade_date is refused, so "
     "null is not served for that firm.",
     None),
    ("settle_date", "date32[day]", True, None,
     "The settlement date: the settlmnt_date column of the transaction table (round-128 ground read); for Cottonwood the Settle Date column. "
     "Null when the value is missing or unparsable; null on every Inflection row (the table has no settlement column).", None),
    ("action", "string", True, None,
     "The action word of the row: the txn_type's action through type_action. Null only when the code is not in the mapping.", None),
    ("txn_type", "string", False, None,
     "The ratified type word of the row, or the string UNMAPPED when the mapping holds the code as UNMAPPED or lacks it.", None),
    ("symbol", "string", True, None,
     "The security symbol, the ticker_symbol column (49 Financial), the Symbol column (Cottonwood) or the ticker column (Inflection); null on a "
     "row with no security.", None),
    ("asset_name", "string", True, None,
     "The security's name. The 49 Financial live schema (140 columns) has no name column (round-128 ground read), so the column is null on "
     "every 49 Financial row; Cottonwood reads its Asset Name column; Inflection reads productName.", None),
    ("units", "double", True, None,
     "The quantity column, named as the units (round-128 ground read); for Cottonwood the Units column; for Inflection noUnits. Null when the "
     "row carries none.", None),
    ("price", "double", True, None,
     "The price column (round-128 ground read); for Cottonwood the Price column; for Inflection navPrice ONLY on a line whose fundFamilyName "
     "is non-blank, with non-zero noUnits and a positive navPrice (price_rule and sources.inflection); every other Inflection line is null, "
     "with the reason NAV_PRICE_FUND_ONLY, ZERO_UNITS or NAV_NOT_POSITIVE. Null when the row carries none.", None),
    ("amount", "double", False, None,
     "The custodian's money amount. 49 Financial: gross_amount; on a cash row the sign is taken from debit_credit as account_return_daily "
     "takes it (CREDIT positive, DEBIT negative); on an in-kind row debit_credit is a position side and is not read as a cash sign. "
     "Cottonwood: the Market Value, signed by the External Flow word as the adapter does (+abs for Contribution, -abs for Withdrawal) and "
     "as booked otherwise. Inflection: transAmount as booked.", None),
    ("fee", "double", True, None,
     "The stated sum, for each firm, of the columns the contract's fee_basis names (49 Financial: commission, exchange_processing_fee, "
     "broker_service_fee, prime_broker_fee, trade_away_fee, redemption_fee, other_fee, step_in_fee, research_fee; Cottonwood: Transaction Fee "
     "and Account Fee). A null column counts as nothing; a row whose named columns are all null has fee null, never zero. Inflection: null "
     "(no fee column).", None),
    ("custodian", "string", False, "inferred",
     "The custodian of the row, lower-cased: the custody entry's constant (sources.json custodian) for 49 Financial, and Cottonwood's Custodian "
     "column and Inflection's custodianName for those firms. The round-128 ground read names custdian_id as the custodian identity column for "
     "49 Financial; the constant is what a person reads, and custdian_id is not read onto the row.",
     "The custodian constant of the custody entry (49 Financial) or the Custodian or custodianName column (Cottonwood, Inflection), stripped "
     "and lower-cased by the producer; set once per entry in the registry."),
    ("flow_class", "string", False, None,
     "The flow class of the row's code: EXTERNAL_IN, EXTERNAL_OUT, INCOME, FEE, INTERNAL, CORPORATE_ACTION or UNRESOLVED. 49 Financial: the "
     "tran_srcde code's class. Cottonwood: the External Flow word (Contribution EXTERNAL_IN, Withdrawal EXTERNAL_OUT) or the pair's class. "
     "Inflection: the description's class in its source_mapping row, by inflection_flow_rule.",
     "49 Financial: per tran_srcde through flow_class_rule over the CRO table's (partition, rule) pairs: one class when the code's CRO rows "
     "agree, UNRESOLVED when they disagree or the table does not hold the code. The silver-only codes and IRAWH and MCE are fixed in "
     "source_mapping. Cottonwood: cottonwood_mapping (the External Flow rule, then the pair's flow_class_none). Inflection: inflection_flow_rule "
     "applied in the order NNA, CorporateAction, account_boundary in or out, Internal, Return by word. The round-128 ground read names the 49 "
     "Financial key (tran_srcde, tr_cd, sb_cd); this contract keys on tran_srcde, the key source_mapping holds."),
    ("source_txn_id", "string", True, None,
     "The per-transaction identifier of the row, a PER-ROW CLAIM: present where the firm's source column (49 Financial "
     "cashiering_transaction_identifier; Cottonwood TransactionID; Inflection id) is non-null and non-blank, and absent (null) where it is not. "
     "It is never a universal key: source_txn_id_coverage states each firm's coverage over every partition with its denominator.", None),
    ("coverage", "string", False, None,
     "How the row's code is covered by the mapping: MEASURED, CODE_NOT_IN_MAPPING or UNMAPPED_BY_TABLE.",
     "MEASURED when the code maps to a type word; CODE_NOT_IN_MAPPING when the mapping lacks the code; UNMAPPED_BY_TABLE when the mapping "
     "holds the code as UNMAPPED."),
    ("source_action_raw", "string", True, "measured",
     "The source value the type and action were looked up from, exactly as received, unstripped: the 49 Financial tran_srcde code, the "
     "Cottonwood Action, or the Inflection transactionDescription. Null where the source cell is missing. Carried on every row, including a "
     "row the mapping does not hold.", None),
]

FEE_RULE_49F = ("The fee is the stated sum of the nine listed columns. For each line it is the sum of the non-null values of commission, "
                "exchange_processing_fee, broker_service_fee, prime_broker_fee, trade_away_fee, redemption_fee, other_fee, step_in_fee and "
                "research_fee. A null column counts as nothing. A line whose nine columns are all null has fee null, never zero. "
                "Excluded by the round-128 ground read: markupmarkdown (a price markup, not a fee charge) and exec_brok_comm (its meaning "
                "as a fee is not established from the census or the tracked records).")
FEE_RULE_CW = ("The fee is the stated sum of Transaction Fee and Account Fee per line, read by the Cottonwood producer. A null column counts "
               "as nothing. A line whose two columns are both null has fee null, never zero.")

TRANSFORMS = [
    {"field": "custodian", "firms": [FIRM49, FIRM_CW, FIRM_INF],
     "rule": ("The producer strips the value and LOWER-CASES it: the 49 Financial custody constant, Cottonwood's Custodian column and "
              "Inflection's custodianName, so the word reads the same across firms. A value is lower-cased, never upper-cased or title-cased. "
              "An Inflection line whose custodianName is null or blank is refused."),
     "claim": "inferred",
     "method": ("The strip and lower-case calls in account_transaction.custodian() (49 Financial), in the Cottonwood normaliser's custodian "
                "field and in the Inflection normaliser; asserted by the offline tests of the three modules on made-up custodians.")},
    {"field": "symbol", "firms": [FIRM49, FIRM_CW, FIRM_INF],
     "rule": ("The producer strips the text; an EMPTY or BLANK value becomes NULL, never the empty string. The 49 Financial symbol is "
              "ticker_symbol; the Cottonwood symbol is Symbol; the Inflection symbol is ticker."),
     "claim": "inferred",
     "method": ("The shared text helper of each module (strip, then empty or blank to None); asserted by the offline tests on an empty "
                "and a blank symbol.")},
    {"field": "asset_name", "firms": [FIRM49, FIRM_CW, FIRM_INF],
     "rule": ("The producer strips the text; an EMPTY or BLANK asset name becomes NULL. The 49 Financial column is null on every row "
              "(claim absent: the live schema has no name column); Cottonwood reads its Asset Name column; Inflection reads productName."),
     "claim": "inferred",
     "method": "The same text helper as symbol; the 49 Financial producer sets None by construction, the other two read their column."},
    {"field": "source_txn_id", "firms": [FIRM49, FIRM_CW, FIRM_INF],
     "rule": ("The producer strips the text; an EMPTY or BLANK identifier becomes NULL. So a null source_txn_id is either a source "
              "identifier that was empty or blank, or one the source never carried; source_txn_id_coverage and the source column tell the "
              "two apart. The Inflection identifier is the integral id as a string, and null where id is not integral."),
     "claim": "inferred",
     "method": ("The shared text helper of each module, read from cashiering_transaction_identifier (49 Financial), TransactionID "
                "(Cottonwood) and id (Inflection); asserted by the offline tests on an empty and a missing identifier.")},
]

INFLECTION_FLOW_RULE = [
    {"bucket": "NNA", "nna_direction": "in", "account_boundary": None, "words": None, "flow_class": "EXTERNAL_IN",
     "reason": "New money: an NNA line in the in direction is cash that arrives from outside the firm (a client or employer deposit, a "
               "rollover or a merge from another account)."},
    {"bucket": "NNA", "nna_direction": "out", "account_boundary": None, "words": None, "flow_class": "EXTERNAL_OUT",
     "reason": "New money: an NNA line in the out direction is cash that leaves the firm (a client distribution, a cancelled account, a "
               "transfer out to another account or an external account)."},
    {"bucket": "CorporateAction", "nna_direction": None, "account_boundary": None, "words": None, "flow_class": "CORPORATE_ACTION",
     "reason": "A corporate action (a split, a spin-off, an expiry) changes the holding and moves no money across the account boundary."},
    {"bucket": "Internal", "nna_direction": None, "account_boundary": "in", "words": None, "flow_class": "EXTERNAL_IN",
     "reason": "An internal journal whose account boundary is in: the money comes into this account from another account of the firm, so it "
               "is an external inflow for this account."},
    {"bucket": "Internal", "nna_direction": None, "account_boundary": "out", "words": None, "flow_class": "EXTERNAL_OUT",
     "reason": "An internal journal whose account boundary is out: the money leaves this account for another account of the firm, so it is "
               "an external outflow for this account."},
    {"bucket": "Internal", "nna_direction": None, "account_boundary": None, "words": None, "flow_class": "INTERNAL",
     "reason": "An internal line with no boundary direction (a trade, a sweep, a reinvestment, a corporate-action journal) stays inside the "
               "account."},
    {"bucket": "Return", "nna_direction": None, "account_boundary": "out", "words": None, "flow_class": "EXTERNAL_OUT",
     "reason": "A return-bucket line whose boundary is out is a tax or charge paid to an outside party (federal, state or foreign tax "
               "withheld), so the money leaves the account."},
    {"bucket": "Return", "nna_direction": None, "account_boundary": None,
     "words": ["Capital gain", "Dividend", "Interest"], "flow_class": "INCOME",
     "reason": "A return-bucket line with no boundary whose word is Capital gain, Dividend or Interest is income earned on the holdings and "
               "kept in the account."},
    {"bucket": "Return", "nna_direction": None, "account_boundary": None,
     "words": ["Fee", "Fee credit", "Management fee", "Trading expense"], "flow_class": "FEE",
     "reason": "A return-bucket line with no boundary whose word is Fee, Fee credit, Management fee or Trading expense is a charge or a "
               "credit of a charge taken from the account."},
    {"bucket": "Return", "nna_direction": None, "account_boundary": None, "words": "other", "flow_class": "INTERNAL",
     "reason": "Any other return-bucket line with no boundary (a tax credit, a return of capital, other income) stays inside the account."},
]

ROW_FILTER_REASON = ("Inflection's status column has six values. The Inflection adapter (adapters/inflection_account_return_daily.py, "
                     "STATUS_COMPLETE) keeps Complete rows only, and so does this table: a Complete line is a transaction that happened. The "
                     "five other statuses (Inactive, Pending, Pending Corporate Action, Rejected, Reversed) are not transactions that happened; "
                     "they are counted per status in excluded_rows_per_status and never served. A status outside the six is refused. No other "
                     "firm has a status column.")
OFFSET_REASON = ("An original and its offset leave the served set together. A Reversed line is out as Reversed (its own status, already "
                 "counted in excluded_rows_per_status). A Complete line whose (accountId, ticker, noUnits, negated transAmount) equals the key of a "
                 "Reversed line is the offset of that original and is counted OFFSET_OF_REVERSED. The CALLER supplies the Reversed keys "
                 "(reversed_keys_of) to split_complete; the producer neither reads the table nor stores a set. The round-132 pairing census "
                 "counts the candidates below (CTO round-131 ruling 1: the Reversed offsets leave the served set with their originals).")
BUSINESS_DATE_RULE = {
    "function": "first_trading_day_on_or_after", "module": "trading_calendar", "window_days": 14,
    "firms": ["49financial", "cottonwood", "inflection"],
    "rule": ("business_date is the first NYSE trading day on or after the trade date, for all three firms: the day returned by "
             "first_trading_day_on_or_after (lib/trading_calendar.py) for the firm's trade date within 14 days. 49 Financial reads its "
             "trade_date; Cottonwood its Trade Date; Inflection its transDate. trade_date is the source date as received and is never rolled. "
             "A line whose trade date has no trading day within 14 days, or none readable, is refused and counted. Each writer refuses a row "
             "whose business_date is not the date= partition it is written under (CTO round-131 ruling (c))."),
}
KEY_NORMALISATION = {"function": "normalise_key", "module": "account_transaction", "rule": KEY_RULE}
SOURCE_ACTION_RAW_SOURCES = {
    "49financial": {"column": "tran_srcde", "rule": ("The code exactly as received, unstripped: the value the 49 Financial lookup is "
                                                   "made from, carried on every row (null where the cell is missing).")},
    "cottonwood": {"column": "Action", "rule": ("The Action exactly as received from the vendor, unstripped, carried on every row (null "
                                               "where the cell is missing); the lookup normalises it by the one key function.")},
    "inflection": {"column": "transactionDescription", "rule": ("The transactionDescription exactly as received, unstripped, carried on "
                                                              "every row (null where the cell is missing); the lookup normalises it by the "
                                                              "one key function.")},
}

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


def ascii_check(obj, label):
    text = json.dumps(obj, ensure_ascii=False)
    if not text.isascii():
        sys.exit("ERROR: non-ASCII text in " + label)


def load(rel):
    return json.loads((ROOT / rel).read_text(encoding="utf-8"))


def schema_hash(columns):
    lines = sorted("%s:%s" % (c["name"], c["type"]) for c in columns)
    return hashlib.sha256("\n".join(lines).encode("ascii")).hexdigest()


def load_module():
    """The module under contract, loaded from its own path: its normalise_key and pair_key are the only key functions used here."""
    spec = importlib.util.spec_from_file_location("account_transaction_for_contract_0_4_0", ROOT / MODULE)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def table_class(rows, entry, word):
    """The class the inflection_flow_rule TABLE gives a taxonomy entry: the rows matching (bucket, nna_direction, account_boundary); where
    several match, the row whose words list holds the word, else the row whose words is the string 'other'. None when nothing decides."""
    key = (entry["bucket"], entry.get("nna_direction"), entry.get("account_boundary"))
    hit = [r for r in rows if (r["bucket"], r["nna_direction"], r["account_boundary"]) == key]
    if len(hit) == 1:
        return hit[0]["flow_class"]
    named = [r for r in hit if isinstance(r["words"], list) and word in r["words"]]
    if len(named) == 1:
        return named[0]["flow_class"]
    other = [r for r in hit if r["words"] == "other"]
    return other[0]["flow_class"] if len(other) == 1 and not named else None


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
    old = load(CONTRACT)  # the 0.4.0 contract on trunk: its 30-pair rule is carried with its reasons, before it is overwritten
    assert old["contract_version"] in ("0.4.0", "0.4.1", "0.4.2"), "the generator reads the trunk contract (0.4.1, or 0.4.2 on a re-run) before overwriting it"
    rule_table = [(r["partition"], r["rule"], r["flow_class"], r["reason"]) for r in old["flow_class_rule"]]
    assert len(rule_table) == 30, "the flow_class_rule must hold 30 pairs"
    rule_map = {(p, r): f for p, r, f, _ in rule_table}

    mod = load_module()
    prop = load(PROPOSAL)
    cro = load(CRO)
    cen124 = load(CENSUS124)
    cen128 = load(CENSUS128)
    fields = load(FIELDS)
    c132 = load(C132_INF)
    cpair = load(C132_PAIR)
    c49 = load(C132_F49)
    ground = {f: load(p) for f, p in GROUND.items()}
    cw = load(COTTONWOOD_REC)
    reads_doc = load(READS)
    idcov_doc = load(IDCOV)
    taxonomy = yaml.safe_load((ROOT / TAXONOMY).read_text(encoding="utf-8"))

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
                                            "source_txn_id", "coverage", "source_action_raw"]
    assert len(columns) == 18

    sources = {}
    for f in (FIRM49, FIRM_CW, FIRM_INF):
        sources[f] = [{"target": t["target"], "source": t["source"], "from_columns": t["from_columns"], "claim": t["claim"],
                       "method": t["method"]} for t in ground[f]["targets"]]
    price_entries = [e for e in sources[FIRM_INF] if e["target"] == "price"]
    assert len(price_entries) == 1 and price_entries[0]["source"] == "avgPrice", "the round-128 price entry is the one to correct"
    agree = sum(v["agree"] for v in fields["navprice_times_units_vs_amount_by_description"].values())
    usable = agree + sum(v["disagree"] for v in fields["navprice_times_units_vs_amount_by_description"].values())
    assert fields["null_or_blank_rows_all"]["avgPrice"] == fields["rows"] == 218054352
    fund = c132["fund_family"]
    assert fund["with_fund_family"] + fund["without_fund_family"] == fund["unit_bearing_positive_nav_rows"]
    price_entries[0].update({
        "source": "navPrice", "from_columns": ["noUnits", "fundFamilyName"], "claim": "inferred",
        "method": ("The price is navPrice ONLY on a line that carries a fund family: the fundFamilyName is non-blank, noUnits is non-zero and "
                   "navPrice is positive. Every other line serves null, never zero, with the reason NAV_PRICE_FUND_ONLY (units non-zero, "
                   "navPrice positive, no fund family), ZERO_UNITS (no units) or NAV_NOT_POSITIVE (units non-zero, navPrice not positive). The "
                   "round-128 ground read named avgPrice for this target and read no value; the round-131 census (values-free, "
                   "R131_INFLECTION_FIELD_CENSUS.json) finds avgPrice null or blank on every one of {rows:,} rows, so the producer never reads it. "
                   "The round-132 census (values-free, R132_INFLECTION_CENSUS.json) finds {upr:,} unit-bearing rows with a positive navPrice, of "
                   "which {wff:,} carry a fund family and {wof:,} do not; navPrice times noUnits equals transAmount within one percent on "
                   "{fw1:,} of the {wff:,} fund-family lines, so navPrice is the unit price the amount is booked at.").format(
                       rows=fields["rows"], upr=fund["unit_bearing_positive_nav_rows"], wff=fund["with_fund_family"],
                       wof=fund["without_fund_family"], fw1=fund["fund_rows_within_1pct"])})

    fee_basis = {FIRM49: {"columns": list(targets[FIRM49]["fee"]["from_columns"]), "rule": FEE_RULE_49F},
                 FIRM_CW: {"columns": list(targets[FIRM_CW]["fee"]["from_columns"]), "rule": FEE_RULE_CW},
                 FIRM_INF: None}
    assert targets[FIRM_INF]["fee"]["from_columns"] == [] and targets[FIRM_INF]["fee"]["source"] is None

    # the Inflection flow class: derived from the table, for each taxonomy entry through its description's word
    word_of = {}
    for m in prop["mapping"]:
        if m["firm"] == FIRM_INF:
            word_of[m["source_value"]] = m["opal_type"]
    tax_by_desc = {e["type_desc"]: e for e in taxonomy["types"]}
    assert set(tax_by_desc) == set(word_of) and len(tax_by_desc) == 48, "the taxonomy and the ratified Inflection rows differ"

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
            row = {"firm": firm, "field": m["field"], "source_value": src, "source_key": normalise_or_fail(mod, src),
                   "opal_type": m["opal_type"], "flow_class": flow, "reason": reason}
        else:
            entry = tax_by_desc[src]
            flow = table_class(INFLECTION_FLOW_RULE, entry, m["opal_type"])
            if flow is None or flow not in FLOW:
                sys.exit("ERROR: no inflection_flow_rule class for %r" % src)
            row = {"firm": firm, "field": m["field"], "source_value": src, "source_key": normalise_or_fail(mod, src),
                   "opal_type": m["opal_type"], "flow_class": flow, "reason": reason, "not_observed": src not in live_inf}
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

    cw_type_pairs = [{"source_value": m["source_value"], "source_key": pair_key_of(mod, m["source_value"]), "opal_type": m["opal_type"],
                      "flow_class_none": (CW_TRANSFER_OUT_RULING if m["source_value"] == TRANSFER_OUT_PAIR else m["flow_class_none"]),
                      "reason": (CW_TRANSFER_OUT_REASON if m["source_value"] == TRANSFER_OUT_PAIR else m["reason"])}
                     for m in cw["mapping"] if m["field"] == "type_pair"]
    cw_actions = [{"source_value": m["source_value"], "source_key": normalise_or_fail(mod, m["source_value"]),
                   "opal_action": m["opal_action"], "reason": m["reason"]}
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
        if rep == 0 and parts_rep == 0:
            return ("No present row shares its value with another row of the same partition, on the round-130 read over every partition, "
                    "so the id column is unique within each partition on that read.")
        return ("%s rows of the present ones share their value with another row of the same partition (%d partitions), so the id column is "
                "not unique within every partition." % (format(rep, ","), parts_rep))

    fi = idcov_doc["firms"]
    chosen = {f: next(t["source"] for t in ground[f]["targets"] if t["target"] == "source_txn_id") for f in GROUND}
    assert chosen == {FIRM49: "cashiering_transaction_identifier", FIRM_CW: "TransactionID", FIRM_INF: "id"}, chosen
    coverage = {
        FIRM49: coverage_entry(FIRM49, chosen[FIRM49], fi[FIRM49], parts49),
        FIRM_CW: coverage_entry(FIRM_CW, chosen[FIRM_CW], fi[FIRM_CW], parts_cw),
        FIRM_INF: coverage_entry(FIRM_INF, chosen[FIRM_INF], fi[FIRM_INF], parts_inf),
    }

    row_filter = {FIRM_INF: {
        "column": "status", "keep": ["Complete"], "rows": fields["rows"], "kept_rows": fields["rows_per_status"]["Complete"],
        "excluded_rows_per_status": {k: v for k, v in fields["rows_per_status"].items() if k != "Complete"},
        "unknown_status": "REFUSED", "reason": ROW_FILTER_REASON}}
    row_filter[FIRM_INF]["offset_rule"] = {
        "key_columns": ["accountId", "ticker", "noUnits", "transAmount"], "negate": "transAmount", "counted_as": "OFFSET_OF_REVERSED",
        "candidate_rows": cpair["reversed"]["offset_candidate_rows"],
        "distinct_keys_with_a_candidate": cpair["reversed"]["distinct_keys_with_a_candidate"], "reason": OFFSET_REASON}

    # the round-132 censuses, copied as measured records; the statuses are what the numbers give (the checker's rule, stated here).
    s6 = cpair["s6_pairing"]
    s6_rows = sum(v["rows"] for v in s6.values())
    s6_paired = sum(v["paired_in_any_partition"] for v in s6.values())
    s6_share = s6_paired / s6_rows
    round_132 = {
        "fund_family": c132["fund_family"],
        "s6_pairing": s6,
        "reversed_offsets": cpair["reversed"],
        "f49_business_date": {"partitions_read": c49["partitions_read"], "counts": c49["counts"]},
        "s6_status": "STANDS" if s6_share >= 0.95 else "RULED_INTERNAL",
        "offsets_status": "NONE" if cpair["reversed"]["offset_candidate_rows"] == 0 else "EXCLUDED_BY_RULE",
    }
    price_rule = {"inflection": {
        "column": "fundFamilyName", "reason_code": "NAV_PRICE_FUND_ONLY", "else_value": None, "else_claim": "absent",
        "other_null_reasons": ["ZERO_UNITS", "NAV_NOT_POSITIVE"],
        "counts": {k: c132["fund_family"][k] for k in ("unit_bearing_positive_nav_rows", "with_fund_family", "without_fund_family",
                                                       "fund_rows_within_1pct")}}}

    # the CTO's final S6 ruling (ADDENDUM 2 to the round-131 analysis, pin a5475b2fdd, msg 9382): the names and counts are the census v2's.
    cv2 = load(CV2)
    pd = cv2["per_description"]
    names = sorted(pd)
    assert len(names) == 2 and all(pd[n]["rows"] == pd[names[0]]["rows"] for n in names), "the S6 census must hold two equal descriptions"
    s6_ruling = {
        "addendum": ADDENDUM,
        "addendum_number": 2,
        "pin": ADDENDUM_PIN,
        "class": "INTERNAL",
        "descriptions": names,
        "rows_per_description": {n: pd[n]["rows"] for n in names},
        "legs_with_the_other_legs_key": {n: pd[n]["same_key_as_a_row_of_the_other_description"] for n in names},
        "income_booked_by": "Dividend to Cash",
        "reason": ("The two descriptions are two legs of one event: every row of each has a row of the other with the same account, day and "
                   "absolute amount (census v2). Counting a leg as income would count the dividend twice, because the income is booked by "
                   "Dividend to Cash (INCOME)."),
        "release_criterion": ("Per event the two legs' signed amounts sum to zero, printed as N of {n}; any miss stops the release.").format(
            n="{:,}".format(pd[names[0]]["rows"])),
    }

    contract = {
        "contract_version": "0.4.2",
        "supersedes": ("0.4.1 (the round-132 contract, whose round_132_censuses.s6_status read REOPENED_FOR_CTO: the CTO's final S6 ruling "
                       "(ADDENDUM 2, pin a5475b2fdd) makes both legs of the Dividend Paid from Cash / Income Paid event INTERNAL and the status "
                       "RULED_INTERNAL, recorded in s6_ruling; the rest of 0.4.1 stands)"),
        "project": "IRPT_DASHBD",
        "prd": PRD,
        "authored_by": "0.9.0_WK_IRPT_DASHBD~1901",
        "authored_under": ("IRPT_DASHBD.TO-DB-f-1801 (round 132, workstream ~F2, F-SHIP), cell DB-f-1801 of IRPT_DASHBD_DECOMP_R132_F.md, "
                           "following the CTO round-131 analysis for F-SHIP (msg 9342: rulings (b) the fund-only price, (c) one business_date "
                           "by the function in lib/trading_calendar.py, (1) the Reversed offsets with their originals, (5) contract, producers "
                           "and mirror in one merge) and the round-132 issuer's censuses."),
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
        "inflection_flow_rule": INFLECTION_FLOW_RULE,
        "key_normalisation": KEY_NORMALISATION,
        "source_action_raw_sources": SOURCE_ACTION_RAW_SOURCES,
        "row_filter": row_filter,
        "source_mapping": source_mapping,
        "cottonwood_mapping": cottonwood_mapping,
        "unmapped_display": "Unclassified",
        "new_code_reason": "CODE_NOT_IN_MAPPING",
        "firms_served": [FIRM49, FIRM_CW, FIRM_INF],
        "firms_pending": [],
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
        "served_note": ("Nothing is written. No object of this table exists in any bucket. 0.4.1 supersedes 0.4.0 on the CTO round-131 rulings "
                        "(round 132, DB-f-1801): one business_date for all three firms by first_trading_day_on_or_after; the Inflection price "
                        "on a fund-family line only (NAV_PRICE_FUND_ONLY); the Reversed offsets counted with their originals. The round-132 "
                        "censuses are stated as measured claims with the statuses the numbers give (round_132_censuses). The release is a "
                        "never-widen act that waits on the CVO's judgment at L9 (DBF132-1-J1 and J2) and on a CTO and COO sign-off. "
                        "0.4.2 records the CTO's final S6 ruling (ADDENDUM 2 to the round-131 analysis, pin a5475b2fdd): both legs of the "
                        "Dividend Paid from Cash / Income Paid event stay INTERNAL, so round_132_censuses.s6_status reads RULED_INTERNAL."),
        "business_date_rule": BUSINESS_DATE_RULE,
        "price_rule": price_rule,
        "round_132_censuses": round_132,
        "s6_ruling": s6_ruling,
    }

    data = {
        "contract_version": contract["contract_version"],
        "type_action": contract["type_action"],
        "source_mapping": contract["source_mapping"],
        "fee_basis": contract["fee_basis"],
        "cottonwood_mapping": contract["cottonwood_mapping"],
        "key_normalisation": contract["key_normalisation"],
        "row_filter": contract["row_filter"],
        "business_date_rule": contract["business_date_rule"],
        "price_rule": contract["price_rule"],
    }

    ascii_check(contract, CONTRACT)
    ascii_check(data, DATA)
    (ROOT / CONTRACT).write_text(json.dumps(contract, indent=2, ensure_ascii=True) + "\n", encoding="utf-8", newline="\n")
    (ROOT / DATA).write_text(json.dumps(data, indent=2, ensure_ascii=True) + "\n", encoding="utf-8", newline="\n")

    print("49 Financial codes by flow class (denominator %d):" % len(rows49))
    for f in FLOW:
        print("  %s %d" % (f, flow_counts.get(f, 0)))
    print("coverage per_value (denominator %d): %s" % (len(rows49), json.dumps(cov_counts, sort_keys=True)))
    print("inflection flow_class per description (denominator %d): %s" % (
        len(rows_inf), json.dumps(dict(Counter(r["flow_class"] for r in rows_inf)), sort_keys=True)))
    print("inflection descriptions not_observed (%d): %s" % (len(not_observed), json.dumps(not_observed)))
    print("inflection price agreement: %s of %s unit-bearing rows" % ("{:,}".format(agree), "{:,}".format(usable)))
    print("s6 pairing share %.6f (%d of %d rows): s6_status %s" % (s6_share, s6_paired, s6_rows, round_132["s6_status"]))
    print("reversed offset candidate rows %d (distinct keys %d): offsets_status %s" % (
        cpair["reversed"]["offset_candidate_rows"], cpair["reversed"]["distinct_keys_with_a_candidate"], round_132["offsets_status"]))
    print("schema_hash %s" % contract["schema_hash"])
    print("wrote %s" % CONTRACT)
    print("wrote %s" % DATA)


def normalise_or_fail(mod, value):
    """The one key function of the module under contract, applied to one single-valued source value (never retyped here)."""
    key = mod.normalise_key(value)
    if key is None:
        sys.exit("ERROR: a source value normalises to None: %r" % (value,))
    return key


def pair_key_of(mod, value):
    """The module's pair_key of a Cottonwood type-pair source value (split on ' | ', each part normalised by the one function)."""
    parts = value.split(" | ", 1)
    if len(parts) != 2:
        sys.exit("ERROR: a type pair does not split on ' | ': %r" % (value,))
    return mod.pair_key(parts[0], parts[1])


if __name__ == "__main__":
    main()
