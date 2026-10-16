"""IRPT_DASHBD round 135, workstream F-SHIP ~F2 (issuer 2.0.0_SA_COO~F2) -- FWD-5: the TRANSACTION CONTRACT 0.5.1 restates the Inflection counts on the right domain
(CTO msg 9625).

  DB-f-2101 (~2101) Every Orion silver fact_transactions partition is a CUMULATIVE SNAPSHOT of the whole history, so the counts 0.5.0 states "over every partition" (the row
                    filter, the fund-family and price counts, the S6 pairing, the Reversed offsets) were SNAPSHOT-WEIGHTED, about 140 times too large (the ratios held).
                    0.5.1 restates every one of them on the LATEST SNAPSHOT (the issuer's R135 records) and adds `inflection_table_shape`: the cumulative-snapshot
                    fact, its evidence, and the gold run domain (read ONE snapshot, the newest partition for the run day; emit lines by trade date). The S6 release
                    criterion reads N of 96 events. The schema hash is unchanged (19 columns).
                    DBF135-1-AC1 (form, then bindings)

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
FIELDS = D + "2.0.0_SA_COO~F2/R131_INFLECTION_FIELD_CENSUS.json"
C132 = D + "2.0.0_SA_COO~F2/R132_INFLECTION_CENSUS.json"
CPAIR = D + "2.0.0_SA_COO~F2/R132_INFLECTION_PAIRING_CENSUS.json"
CV2 = D + "2.0.0_SA_COO~F2/R132_INFLECTION_S6_CENSUS_V2.json"
SNAP = D + "2.0.0_SA_COO~F2/R135_INFLECTION_SNAPSHOT_CENSUS.json"
LPRICE = D + "2.0.0_SA_COO~F2/R135_INFLECTION_LATEST_PRICE_CENSUS.json"
ADDENDUM = "org/tier1_exec/1.0.0_SA_CTO/deliverables/CTO_ROUND_ANALYSIS_IRPT_DASHBD_F-SHIP_ROUND_131_20261016.md"
ADDENDUM_PIN = "a5475b2fdd"
C49 = D + "2.0.0_SA_COO~F2/R132_F49_BUSINESS_DATE_CENSUS.json"
FUNCTION = "first_trading_day_on_or_after"
TAXONOMY = "data/inf/scripts/silver/orion_cashflow_taxonomy.yaml"
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
           "price", "amount", "fee", "custodian", "flow_class", "source_txn_id", "coverage", "source_action_raw", "business_date_claim")
BRIEF14 = COLUMNS[3:17]
TYPES = ("string", "date32[day]", "double")
COVERAGE = ("MEASURED", "CODE_NOT_IN_MAPPING", "UNMAPPED_BY_TABLE")
KEYS = ("contract_version", "supersedes", "project", "prd", "authored_by", "authored_under", "table", "grain", "partition", "producer",
        "columns", "sources", "fee_basis", "transforms", "source_txn_id_coverage", "enums", "type_action", "flow_class_rule",
        "inflection_flow_rule", "key_normalisation", "source_action_raw_sources", "row_filter", "business_date_rule", "price_rule", "round_132_censuses", "s6_ruling", "inflection_table_shape",
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
    """The 19 columns in order (the 18 of 0.4.x and business_date_claim last); the claim of each brief column equals the 49 Financial ground read's claim for that target."""
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
        if n == "source_action_raw" and not (c.get("nullable") is True and c.get("claim") == "measured" and c.get("type") == "string"):
            pr.append("source_action_raw: a nullable string with the claim measured (the source value exactly as received)")
        if n == "business_date_claim" and not (c.get("nullable") is False and c.get("claim") == "inferred" and c.get("type") == "string"
                                              and isinstance(c.get("method"), str) and "measured" in c["method"] and "inferred" in c["method"]):
            pr.append("business_date_claim: a non-null string, claim inferred, whose method says when the row reads measured and when inferred")
        if n == "business_date" and not (c.get("claim") == "inferred" and isinstance(c.get("method"), str) and "business_date_claim" in c["method"]):
            pr.append("business_date: claim inferred (its weakest row) with a method naming the per-row field business_date_claim")
    return pr


# CTO round-130 ruling (msg 9245): ONE normalisation (strip surrounding whitespace, case kept) used by the mapping's keys and the producer's lookup.
def norm(v):
    return v.strip()


def pair_norm(v):
    return " | ".join(norm(part) for part in v.split(" | ", 1))


def key_problems(con):
    """key_normalisation is stated; every mapping row carries source_key == the normalised source_value; no two values of one firm and
    field collapse to one key (a collision is a rule-24 finding, printed); source_action_raw has its source column per firm."""
    kn = con["key_normalisation"]
    pr = []
    rule = str(kn.get("rule", "")).lower() if isinstance(kn, dict) else ""
    if not (isinstance(kn, dict) and kn.get("function") == "normalise_key" and kn.get("module") == "account_transaction"
            and "strip" in rule and "case" in rule):
        pr.append("key_normalisation must name function normalise_key in module account_transaction and say strip and case")
    groups = {}
    for m in con["source_mapping"]:
        groups.setdefault((m.get("firm"), "type"), []).append((m.get("source_value"), m.get("source_key"), norm))
    cm = con["cottonwood_mapping"]
    for field, fn in (("type_pairs", pair_norm), ("actions", norm)):
        for m in cm[field]:
            groups.setdefault(("cottonwood", field), []).append((m.get("source_value"), m.get("source_key"), fn))
    for grp, rows in groups.items():
        keys = []
        for sv, sk, fn in rows:
            if not isinstance(sv, str) or sk != fn(sv):
                pr.append("%s %r: source_key %r is not the normalised value" % (grp, sv, sk))
            keys.append(sk)
        if len(set(keys)) != len(keys):
            pr.append("%s: two source values normalise to one key (a finding): %s" % (grp, sorted({k for k in keys if keys.count(k) > 1})[:3]))
    sa = con["source_action_raw_sources"]
    want = {"49financial": "tran_srcde", "cottonwood": "Action", "inflection": "transactionDescription"}
    if not (isinstance(sa, dict) and sorted(sa) == sorted(want) and all(
            isinstance(sa[f], dict) and sa[f].get("column") == c and "received" in str(sa[f].get("rule", "")).lower() for f, c in want.items())):
        pr.append("source_action_raw_sources must name tran_srcde, Action and transactionDescription with a rule saying as received")
    return pr


def row_filter_problems(con, fields):
    """Inflection serves status Complete only (the adapter's own rule); the excluded rows are counted per status from the issuer's census."""
    rf = con["row_filter"]
    st = fields["rows_per_status"]
    want = {"column": "status", "keep": ["Complete"], "rows": fields["rows"], "kept_rows": st["Complete"],
            "excluded_rows_per_status": {k: v for k, v in st.items() if k != "Complete"}, "basis": "latest snapshot " + fields["snapshot"]}
    pr = []
    e = rf.get("inflection") if isinstance(rf, dict) else None
    if not (isinstance(e, dict) and {k: e.get(k) for k in want} == want):
        pr.append("row_filter.inflection must be %r (the issuer's R135 latest-snapshot census)" % want)
    elif not (e.get("unknown_status") == "REFUSED" and isinstance(e.get("reason"), str) and "adapter" in e["reason"].lower()):
        pr.append("row_filter.inflection: unknown_status REFUSED and a reason naming the adapter's rule")
    if not (isinstance(rf, dict) and sorted(rf) == ["inflection"]):
        pr.append("row_filter holds exactly inflection (the other two firms' tables have no status column)")
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


# The issuer's Inflection rule: the Orion taxonomy's (bucket, nna_direction, account_boundary) and, inside Return, the ratified word.
INFL_RETURN_INCOME = ("Capital gain", "Dividend", "Interest")
INFL_RETURN_FEE = ("Fee", "Fee credit", "Management fee", "Trading expense")


def inflection_class(entry, word):
    bucket, nna, boundary = entry["bucket"], entry.get("nna_direction"), entry.get("account_boundary")
    if bucket == "NNA":
        return "EXTERNAL_IN" if nna == "in" else "EXTERNAL_OUT"
    if bucket == "CorporateAction":
        return "CORPORATE_ACTION"
    if boundary == "in":
        return "EXTERNAL_IN"
    if boundary == "out":
        return "EXTERNAL_OUT"
    if bucket == "Internal":
        return "INTERNAL"
    if bucket == "Return":
        if word in INFL_RETURN_INCOME:
            return "INCOME"
        if word in INFL_RETURN_FEE:
            return "FEE"
        return "INTERNAL"
    return "UNRESOLVED"


def inflection_rule_problems(con):
    r = con["inflection_flow_rule"]
    if not (isinstance(r, list) and r and all(isinstance(x, dict) for x in r)):
        return ["inflection_flow_rule must be a non-empty list of {bucket, nna_direction, account_boundary, words, flow_class, reason}"]
    pr = []
    need_keys = {("NNA", "in", None), ("NNA", "out", None), ("CorporateAction", None, None), ("Internal", None, "in"),
                 ("Internal", None, "out"), ("Internal", None, None), ("Return", None, "out"), ("Return", None, None)}
    seen = {(x.get("bucket"), x.get("nna_direction"), x.get("account_boundary")) for x in r}
    if not need_keys <= seen:
        pr.append("inflection_flow_rule must cover the eight (bucket, direction, boundary) combinations of the taxonomy")
    if not all(isinstance(x.get("reason"), str) and x["reason"].strip() and x.get("flow_class") in FLOW for x in r):
        pr.append("every inflection_flow_rule row needs a flow_class from the seven and a reason")
    return pr


def table_class(rows, entry, word):
    """The class the contract's own inflection_flow_rule TABLE gives a taxonomy entry: the rows matching (bucket, nna_direction, account_boundary);
    where several match, the row whose `words` list holds the word, else the row whose `words` is the string "other". None when nothing decides."""
    key = (entry["bucket"], entry.get("nna_direction"), entry.get("account_boundary"))
    hit = [r for r in rows if (r.get("bucket"), r.get("nna_direction"), r.get("account_boundary")) == key]
    if len(hit) == 1:
        return hit[0].get("flow_class")
    named = [r for r in hit if isinstance(r.get("words"), list) and word in r["words"]]
    if len(named) == 1:
        return named[0].get("flow_class")
    other = [r for r in hit if r.get("words") == "other"]
    return other[0].get("flow_class") if len(other) == 1 and not named else None


def inflection_flow_problems(con, taxonomy):
    pr = []
    word = {m["source_value"]: m for m in con["source_mapping"] if m.get("firm") == "inflection"}
    for e in taxonomy["types"]:
        m = word.get(e["type_desc"])
        if m is None:
            pr.append("inflection %r: no mapping row" % e["type_desc"])
            continue
        want = inflection_class(e, m.get("opal_type"))
        if m.get("flow_class") != want:
            pr.append("inflection %r: flow_class %r, the rule gives %r" % (e["type_desc"], m.get("flow_class"), want))
        tbl = table_class(con["inflection_flow_rule"], e, m.get("opal_type"))
        if tbl != want:
            pr.append("inflection %r: the contract's inflection_flow_rule table gives %r, the rule gives %r" % (e["type_desc"], tbl, want))
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
    if con["contract_version"] != "0.5.1" or not str(con["supersedes"]).startswith("0.5.0"):
        pr.append("contract_version must be 0.5.1 and supersedes name 0.5.0")
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
    if not (isinstance(served, list) and sorted(served) == sorted(GROUND) and pending == []):
        pr.append("firms_served must be all three firms and firms_pending empty (the Inflection producer lands in this merge)")
    pr += transform_problems(con["transforms"])
    if not isinstance(fp, list):
        pr.append("firms_pending must be a list")
    pr += rule24_problems(con["rule24_records"])
    if con["served"] is not False:
        pr.append("served must be false")
    if not json.dumps(con, ensure_ascii=False).isascii():
        pr.append("non-ASCII text")
    return pr


def price_numbers(fields):
    """(agree, usable) of the issuer's R131 price-source test: rows where noUnits * navPrice equals transAmount within one percent, and the rows
    that carry units and a positive navPrice (Complete rows, every partition)."""
    p = fields["navprice_times_units_vs_amount_by_description"]
    agree = sum(v["agree"] for v in p.values())
    return agree, agree + sum(v["disagree"] for v in p.values())


def price_correction_problems(entry, fields, c132=None):
    """Inflection's price: avgPrice is null on every row (R131); the price is navPrice only on a line with a fund family, units and a positive
    navPrice (R132 census), else null with the reason NAV_PRICE_FUND_ONLY."""
    pr = []
    if fields["null_or_blank_rows_all"]["avgPrice"] != fields["rows"]:
        pr.append("the R131 census no longer finds avgPrice null on every row: the correction's premise changed")
    m = str(entry.get("method") or "")
    if not (entry.get("source") == "navPrice" and entry.get("from_columns") == ["noUnits", "fundFamilyName"] and entry.get("claim") == "inferred"):
        pr.append("inflection price must be source navPrice, from_columns [noUnits, fundFamilyName], claim inferred")
    f = (c132 or {}).get("fund_family") if c132 else None
    needles = ["avgPrice", "null", "NAV_PRICE_FUND_ONLY"]
    if f:
        needles += ["{:,}".format(f["with_fund_family"]), "{:,}".format(f["fund_rows_within_1pct"])]
    for needle in needles:
        if needle not in m:
            pr.append("inflection price method must state %r (the fund-family rule, its census numbers and the avgPrice finding)" % needle)
    return pr


def s6_ruling_problems(con, cv2):
    """The CTO's final S6 ruling (ADDENDUM 2, pin a5475b2fdd): both legs INTERNAL; the numbers are the census v2's; the release criterion is stated."""
    r = con["s6_ruling"]
    pd = cv2["per_description"]
    names = sorted(pd)
    want = {"addendum": ADDENDUM, "addendum_number": 2, "pin": ADDENDUM_PIN, "class": "INTERNAL", "descriptions": names,
            "rows_per_description": {n: pd[n]["rows"] for n in names},
            "legs_with_the_other_legs_key": {n: pd[n]["same_key_as_a_row_of_the_other_description"] for n in names},
            "income_booked_by": "Dividend to Cash"}
    pr = []
    if not (isinstance(r, dict) and {k: r.get(k) for k in want} == want):
        pr.append("s6_ruling must be %r plus reason and release_criterion" % (want,))
        return pr
    rc = str(r.get("release_criterion", ""))
    n = "{:,}".format(pd[names[0]]["rows"])
    if not ("sum to zero" in rc and n in rc and "stops the release" in rc.lower()):
        pr.append("s6_ruling.release_criterion must say per event the two legs' signed amounts sum to zero, printed as N of %s, and that any miss stops the release" % n)
    if not (isinstance(r.get("reason"), str) and "twice" in r["reason"].lower() and "two legs" in r["reason"].lower()):
        pr.append("s6_ruling.reason must say the two descriptions are two legs of one event and that counting a leg as income would count the dividend twice")
    return pr


def rules_problems(con, c132, cpair, c49):
    """business_date_rule, price_rule and round_132_censuses are the issuer's committed census records, stated as measured; the S6 and offset statuses
    are the ones the numbers give."""
    pr = []
    b = con["business_date_rule"]
    rule = str(b.get("rule", "")).lower() if isinstance(b, dict) else ""
    if not (isinstance(b, dict) and b.get("function") == FUNCTION and b.get("module") == "trading_calendar" and b.get("window_days") == 14
            and sorted(b.get("firms", [])) == sorted(GROUND) and "on or after" in rule and "trade date" in rule and "as received" in rule):
        pr.append("business_date_rule must name %s in trading_calendar, window_days 14, the three firms, and say on or after, trade date, as received" % FUNCTION)
    col = next(c for c in con["columns"] if c["name"] == "business_date")
    if FUNCTION not in str(col.get("meaning", "")):
        pr.append("the business_date column's meaning must name %s" % FUNCTION)
    cl = b.get("claims") if isinstance(b, dict) else None
    if not (isinstance(b, dict) and b.get("claim_field") == "business_date_claim" and "first NYSE trading day on or after the trade date" in str(b.get("basis", ""))
            and isinstance(cl, dict) and sorted(cl) == ["inferred", "measured"]
            and "equals" in str(cl.get("measured", "")).lower() and "rolled" in str(cl.get("inferred", "")).lower()):
        pr.append("business_date_rule must carry claim_field business_date_claim, the basis 'first NYSE trading day on or after the trade date', and claims {measured: "
                  "business_date equals trade_date, inferred: rolled forward}")
    f = c132["fund_family"]
    want_counts = {k: f[k] for k in ("unit_bearing_positive_nav_rows", "with_fund_family", "without_fund_family", "fund_rows_within_1pct")}
    p = con["price_rule"].get("inflection") if isinstance(con["price_rule"], dict) else None
    if not (isinstance(p, dict) and p.get("column") == "fundFamilyName" and p.get("reason_code") == "NAV_PRICE_FUND_ONLY" and p.get("else_value") is None
            and p.get("else_claim") == "absent" and sorted(p.get("other_null_reasons", [])) == ["NAV_NOT_POSITIVE", "ZERO_UNITS"]
            and p.get("counts") == want_counts):
        pr.append("price_rule.inflection must be {column fundFamilyName, reason_code NAV_PRICE_FUND_ONLY, else_value null, else_claim absent, "
                  "other_null_reasons [NAV_NOT_POSITIVE, ZERO_UNITS], counts %r}" % (want_counts,))
    L = cpair["latest_snapshot"]
    s6 = L["s6_rows_and_pairing"]
    rows = sum(v["rows"] for v in s6.values())
    paired = sum(v["paired_with_income_class_row"] for v in s6.values())
    share = paired / rows if rows else 0.0
    rev = {"reversed_rows": L["reversed_rows"], "distinct_keys": L["reversed_distinct_keys"], "offset_candidate_rows": L["offset_candidate_rows"],
           "offset_candidate_descriptions": L["offset_candidate_descriptions"]}
    cand = rev["offset_candidate_rows"]
    want = {"basis": "latest snapshot " + L["latest_snapshot"], "fund_family": f, "s6_pairing": s6, "reversed_offsets": rev,
            "f49_business_date": {"partitions_read": c49["partitions_read"], "counts": c49["counts"]},
            "s6_status": "STANDS" if share >= 0.95 else "RULED_INTERNAL",
            "offsets_status": "NONE" if cand == 0 else "EXCLUDED_BY_RULE"}
    rf = con["row_filter"].get("inflection") if isinstance(con["row_filter"], dict) else None
    orule = rf.get("offset_rule") if isinstance(rf, dict) else None
    want_rule = {"key_columns": ["accountId", "ticker", "noUnits", "transAmount"], "negate": "transAmount", "counted_as": "OFFSET_OF_REVERSED", "candidate_rows": cand}
    if not (isinstance(orule, dict) and {k: orule.get(k) for k in want_rule} == want_rule and isinstance(orule.get("reason"), str)
            and "original" in orule["reason"].lower() and "offset" in orule["reason"].lower()):
        pr.append("row_filter.inflection.offset_rule must be %r plus a reason naming the original and its offset (CTO ruling 1)" % (want_rule,))
    got = con["round_132_censuses"]
    if got != want:
        diff = [k for k in want if not isinstance(got, dict) or got.get(k) != want[k]]
        pr.append("round_132_censuses must equal the issuer's R135 latest-snapshot records and the statuses the numbers give (differs: %s; s6 share %.4f, offset candidates %d)"
                  % (diff, share, cand))
    return pr


def table_shape_problems(con, snap):
    """inflection_table_shape: the cumulative-snapshot fact, its evidence from the issuer's R135 census, and the gold run domain (CTO msg 9625)."""
    L, A = snap["latest_snapshot"], snap["distinct_and_movement"]
    want = {"kind": "cumulative_snapshot", "snapshots": A["snapshots"], "latest_snapshot": L["latest_snapshot"], "latest_snapshot_rows": L["rows"],
            "distinct_ids_ever_seen": A["distinct_ids_ever_seen"], "ids_in_latest_snapshot": A["ids_in_latest_snapshot"],
            "ids_whose_status_changed_first_to_last": A["ids_whose_status_changed_first_to_last"]}
    t = con["inflection_table_shape"]
    pr = []
    if not (isinstance(t, dict) and {k: t.get(k) for k in want} == want):
        pr.append("inflection_table_shape must be %r plus statement and gold_run_domain" % (want,))
        return pr
    st = str(t.get("statement", "")).lower()
    gd = str(t.get("gold_run_domain", "")).lower()
    if not ("cumulative" in st and "reads" in st and "snapshot-weighted" in st):
        pr.append("inflection_table_shape.statement must say the table is cumulative snapshots and that the reads and earlier counts are snapshot-weighted")
    if not ("newest partition" in gd and "trade date" in gd and "one" in gd and "never" in gd):
        pr.append("inflection_table_shape.gold_run_domain must say the run reads ONE snapshot (the newest partition for the run day), emits lines by trade date, and never treats a partition as that day's transactions")
    return pr

def source_problems(con, recs, fields=None, c132=None):
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
            if fields is not None and firm == "inflection" and t["target"] == "price":
                if g is None:
                    pr.append("inflection price: no source entry")
                else:
                    pr += price_correction_problems(g, fields, c132)
                continue
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
            if m.get("flow_class") not in FLOW:
                pr.append("%s %r: flow_class must be one of the seven (Inflection's producer lands in this merge)" % (firm, code))
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
            pr.append("%s: the worker's own read (RD_READS_R130.json) must have partitions_read, objects_read and rows above zero" % firm)
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
    for k in ("source_mapping", "type_action", "cottonwood_mapping", "fee_basis", "key_normalisation", "row_filter", "business_date_rule", "price_rule"):
        if data.get(k) != con[k]:
            pr.append("transaction_words.json differs from the contract's %s" % k)
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
    need(not form_problems(con, recs[FIRM49]), "the contract's form must pass first")
    snap, lprice, c49 = load(root, SNAP), load(root, LPRICE), load(root, C49)
    L = snap["latest_snapshot"]
    fields_rf = {"rows": L["rows"], "rows_per_status": L["rows_per_status"], "snapshot": L["latest_snapshot"]}
    fields_px = {"rows": lprice["complete_rows"], "null_or_blank_rows_all": {"avgPrice": lprice["null_or_blank_rows_complete"]["avgPrice"]}}
    cv2 = {"per_description": {d: {"rows": v["rows"], "same_key_as_a_row_of_the_other_description": L["s6_keys_in_both"]} for d, v in L["s6_rows_and_pairing"].items()}}
    pr = source_problems(con, recs, fields_px, lprice) + rule_problems(con) + rules_problems(con, lprice, snap, c49) + s6_ruling_problems(con, cv2) + table_shape_problems(con, snap)
    pr += mapping_problems(con, load(root, PROPOSAL), load(root, CRO), load(root, CENSUS49), load(root, CENSUS3))
    pr += census_prob + census_problems(con) + data_problems(con, load(root, DATA))
    pr += inflection_rule_problems(con) + key_problems(con) + row_filter_problems(con, fields_rf)
    import yaml
    pr += inflection_flow_problems(con, yaml.safe_load(Path(root, TAXONOMY).read_text(encoding="utf-8")))
    pr += cottonwood_problems(con, load(root, COTTONWOOD)) + reads_problems(con, load(root, READS), load(root, CENSUS3))
    pr += census_prob
    need(not pr, "; ".join(pr[:6]))


def ac_all(root):
    """ONE criterion: the contract's form, then its bindings (a single verdict)."""
    ac_form(root)
    ac_bindings(root)


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
    cols[17]["nullable"] = True
    cols[18].update(claim="inferred", method="measured where it equals trade_date; inferred where rolled")
    cols[2].update(claim="inferred", method="the day; the per-row claim is business_date_claim")
    arm("columns-green", column_problems(cols, rec49), [])
    arm("raw-column-must-be-nullable", len(column_problems(cols[:17] + [dict(cols[17], nullable=False)] + cols[18:], rec49)), 1)
    arm("claim-column-must-be-inferred-with-method", len(column_problems(cols[:18] + [dict(cols[18], claim="measured")], rec49)), 1)
    arm("business-date-claim-must-name-the-field", len(column_problems(cols[:2] + [dict(cols[2], method="the day")] + cols[3:], rec49)), 1)
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
    arm("infl-nna-in", inflection_class({"bucket": "NNA", "nna_direction": "in"}, "Deposit"), "EXTERNAL_IN")
    arm("infl-nna-out", inflection_class({"bucket": "NNA", "nna_direction": "out"}, "Withdrawal"), "EXTERNAL_OUT")
    arm("infl-boundary", inflection_class({"bucket": "Internal", "account_boundary": "out"}, "Journal"), "EXTERNAL_OUT")
    arm("infl-internal", inflection_class({"bucket": "Internal"}, "Dividend"), "INTERNAL")
    arm("infl-return-income", inflection_class({"bucket": "Return"}, "Dividend"), "INCOME")
    arm("infl-return-fee", inflection_class({"bucket": "Return"}, "Management fee"), "FEE")
    arm("infl-return-tax", inflection_class({"bucket": "Return"}, "Tax withheld"), "INTERNAL")
    arm("infl-return-tax-out", inflection_class({"bucket": "Return", "account_boundary": "out"}, "Tax withheld"), "EXTERNAL_OUT")
    arm("infl-corp", inflection_class({"bucket": "CorporateAction"}, "Corporate action"), "CORPORATE_ACTION")
    good_tr = [{"field": "custodian", "rule": "lower-cased", "claim": "inferred", "method": "m"},
               {"field": "symbol", "rule": "empty becomes null", "claim": "inferred", "method": "m"},
               {"field": "source_txn_id", "rule": "empty becomes null", "claim": "inferred", "method": "m"},
               {"field": "asset_name", "rule": "empty becomes null", "claim": "inferred", "method": "m"}]
    arm("transforms-green", transform_problems(good_tr), [])
    arm("infl-rule-form", inflection_rule_problems({"inflection_flow_rule": []})[0].startswith("inflection_flow_rule must be"), True)
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
    rows_t = [{"bucket": "Return", "flow_class": "INCOME", "words": ["Dividend"]}, {"bucket": "Return", "flow_class": "FEE", "words": ["Fee"]},
              {"bucket": "Return", "flow_class": "INTERNAL", "words": "other"}, {"bucket": "NNA", "nna_direction": "in", "flow_class": "EXTERNAL_IN"}]
    arm("table-single", table_class(rows_t, {"bucket": "NNA", "nna_direction": "in"}, "Deposit"), "EXTERNAL_IN")
    arm("table-named", table_class(rows_t, {"bucket": "Return"}, "Fee"), "FEE")
    arm("table-other", table_class(rows_t, {"bucket": "Return"}, "Tax withheld"), "INTERNAL")
    arm("table-none", table_class(rows_t, {"bucket": "Internal"}, "Buy"), None)
    pf = {"rows": 10, "null_or_blank_rows_all": {"avgPrice": 10}}
    c132 = {"fund_family": {"unit_bearing_positive_nav_rows": 1207, "with_fund_family": 1207, "without_fund_family": 0, "fund_rows_within_1pct": 1204}}
    good_price = {"source": "navPrice", "from_columns": ["noUnits", "fundFamilyName"], "claim": "inferred",
                  "method": "avgPrice is null on every row; navPrice only on a fund-family line (1,207, 1,204 within one percent); else null with NAV_PRICE_FUND_ONLY"}
    arm("price-green", price_correction_problems(good_price, pf, c132), [])
    arm("price-wrong-source", len(price_correction_problems(dict(good_price, source="avgPrice"), pf, c132)), 1)
    arm("price-method-needs-numbers", len(price_correction_problems(dict(good_price, method="navPrice"), pf, c132)), 5)
    arm("price-premise", len(price_correction_problems(good_price, dict(pf, null_or_blank_rows_all={"avgPrice": 9}), c132)), 1)
    arm("price-from-columns-need-fund-family", len(price_correction_problems(dict(good_price, from_columns=["noUnits"]), pf, c132)), 1)
    cp = {"latest_snapshot": {"latest_snapshot": "2026-10-16", "rows": 10, "rows_per_status": {"Complete": 8, "Rejected": 2},
                              "s6_rows_and_pairing": {"a": {"rows": 100, "paired_with_income_class_row": 96}, "b": {"rows": 100, "paired_with_income_class_row": 96}},
                              "s6_keys_in_both": 100, "reversed_rows": 5, "reversed_distinct_keys": 4, "offset_candidate_rows": 0, "offset_candidate_descriptions": {}},
          "distinct_and_movement": {"snapshots": 2, "distinct_ids_ever_seen": 12, "ids_in_latest_snapshot": 10, "ids_whose_status_changed_first_to_last": 1}}
    c49 = {"partitions_read": 2, "counts": {"rows": 5}}
    col = {"name": "business_date", "meaning": "the day, first_trading_day_on_or_after the trade date", "claim": "inferred", "method": "see business_date_claim"}
    rev_ok = {"reversed_rows": 5, "distinct_keys": 4, "offset_candidate_rows": 0, "offset_candidate_descriptions": {}}
    con_r = {"row_filter": {"inflection": {"offset_rule": {"key_columns": ["accountId", "ticker", "noUnits", "transAmount"], "negate": "transAmount",
                                                          "counted_as": "OFFSET_OF_REVERSED", "candidate_rows": 0,
                                                          "reason": "an original and its offset leave the served set together"}}},
             "business_date_rule": {"function": FUNCTION, "module": "trading_calendar", "window_days": 14, "firms": sorted(GROUND),
                                    "rule": "the first trading day on or after the trade date; trade_date as received",
                                    "claim_field": "business_date_claim", "basis": "first NYSE trading day on or after the trade date",
                                    "claims": {"measured": "business_date equals trade_date", "inferred": "rolled forward by the rule"}},
             "columns": [col],
             "price_rule": {"inflection": {"column": "fundFamilyName", "reason_code": "NAV_PRICE_FUND_ONLY", "else_value": None, "else_claim": "absent",
                                           "other_null_reasons": ["ZERO_UNITS", "NAV_NOT_POSITIVE"],
                                           "counts": {k: c132["fund_family"][k] for k in ("unit_bearing_positive_nav_rows", "with_fund_family",
                                                                                          "without_fund_family", "fund_rows_within_1pct")}}},
             "round_132_censuses": {"basis": "latest snapshot 2026-10-16", "fund_family": c132["fund_family"],
                                    "s6_pairing": cp["latest_snapshot"]["s6_rows_and_pairing"], "reversed_offsets": rev_ok,
                                    "f49_business_date": c49, "s6_status": "STANDS", "offsets_status": "NONE"}}
    arm("rules-green", rules_problems(con_r, c132, cp, c49), [])
    low_l = dict(cp["latest_snapshot"], s6_rows_and_pairing={"a": {"rows": 100, "paired_with_income_class_row": 50}, "b": {"rows": 100, "paired_with_income_class_row": 50}})
    arm("rules-s6-below-95-must-say-ruled-internal", len(rules_problems(con_r, c132, dict(cp, latest_snapshot=low_l), c49)), 1)
    cand_l = dict(cp["latest_snapshot"], offset_candidate_rows=3)
    arm("rules-offsets-must-say-excluded", len(rules_problems(con_r, c132, dict(cp, latest_snapshot=cand_l), c49)) >= 1, True)
    shape_ok = {"kind": "cumulative_snapshot", "snapshots": 2, "latest_snapshot": "2026-10-16", "latest_snapshot_rows": 10, "distinct_ids_ever_seen": 12,
                "ids_in_latest_snapshot": 10, "ids_whose_status_changed_first_to_last": 1,
                "statement": "Every partition is a cumulative snapshot; the reads and the earlier counts over every partition are snapshot-weighted.",
                "gold_run_domain": "ONE snapshot, the newest partition for the run day, lines emitted by trade date; never a partition as that day's transactions."}
    arm("shape-green", table_shape_problems({"inflection_table_shape": shape_ok}, cp), [])
    arm("shape-counts", len(table_shape_problems({"inflection_table_shape": dict(shape_ok, snapshots=3)}, cp)), 1)
    arm("shape-domain", len(table_shape_problems({"inflection_table_shape": dict(shape_ok, gold_run_domain="every partition")}, cp)), 1)
    arm("shape-statement", len(table_shape_problems({"inflection_table_shape": dict(shape_ok, statement="a table")}, cp)), 1)
    cv2 = {"per_description": {"a": {"rows": 100, "same_key_as_a_row_of_the_other_description": 100},
                               "b": {"rows": 100, "same_key_as_a_row_of_the_other_description": 100}}}
    good_r = {"addendum": ADDENDUM, "addendum_number": 2, "pin": ADDENDUM_PIN, "class": "INTERNAL", "descriptions": ["a", "b"],
              "rows_per_description": {"a": 100, "b": 100}, "legs_with_the_other_legs_key": {"a": 100, "b": 100}, "income_booked_by": "Dividend to Cash",
              "release_criterion": "per event the two legs' signed amounts sum to zero, printed as N of 100; any miss stops the release",
              "reason": "two legs of one event; counting a leg as income would count the dividend twice"}
    arm("s6-ruling-green", s6_ruling_problems({"s6_ruling": good_r}, cv2), [])
    arm("s6-ruling-pin", len(s6_ruling_problems({"s6_ruling": dict(good_r, pin="x")}, cv2)), 1)
    arm("s6-ruling-criterion", len(s6_ruling_problems({"s6_ruling": dict(good_r, release_criterion="later")}, cv2)), 1)
    arm("s6-ruling-reason", len(s6_ruling_problems({"s6_ruling": dict(good_r, reason="because")}, cv2)), 1)
    arm("rules-business-date-function", len(rules_problems(dict(con_r, business_date_rule={"function": "x"}), c132, cp, c49)), 2)
    arm("norm-strip-only", (norm("  Buy Money Market "), norm("Buy")), ("Buy Money Market", "Buy"))
    arm("norm-case-kept", norm(" BUY "), "BUY")
    arm("pair-norm", pair_norm("Transfer Out | Transfer Out "), "Transfer Out | Transfer Out")
    kn_ok = {"function": "normalise_key", "module": "account_transaction", "rule": "strip surrounding whitespace; case kept"}
    sa_ok = {"49financial": {"column": "tran_srcde", "rule": "as received"}, "cottonwood": {"column": "Action", "rule": "as received"},
             "inflection": {"column": "transactionDescription", "rule": "as received"}}
    con_k = {"key_normalisation": kn_ok, "source_action_raw_sources": sa_ok,
             "source_mapping": [{"firm": "inflection", "source_value": "A ", "source_key": "A"},
                                {"firm": "inflection", "source_value": "B", "source_key": "B"}],
             "cottonwood_mapping": {"type_pairs": [{"source_value": "T | S ", "source_key": "T | S"}],
                                    "actions": [{"source_value": "Buy ", "source_key": "Buy"}]}}
    arm("keys-green", key_problems(con_k), [])
    arm("keys-wrong-key", len(key_problems(dict(con_k, source_mapping=[{"firm": "inflection", "source_value": "A ", "source_key": "A "}]))), 1)
    clash = dict(con_k, source_mapping=[{"firm": "inflection", "source_value": "A ", "source_key": "A"},
                                        {"firm": "inflection", "source_value": "A", "source_key": "A"}])
    arm("keys-collision-is-a-finding", any("normalise to one key" in x for x in key_problems(clash)), True)
    arm("keys-rule-must-say-case", len(key_problems(dict(con_k, key_normalisation=dict(kn_ok, rule="strip")))), 1)
    fld = {"rows": 10, "rows_per_status": {"Complete": 8, "Rejected": 2}, "snapshot": "2026-10-16"}
    rf_ok = {"inflection": {"column": "status", "keep": ["Complete"], "rows": 10, "kept_rows": 8, "excluded_rows_per_status": {"Rejected": 2},
                            "basis": "latest snapshot 2026-10-16",
                            "unknown_status": "REFUSED", "reason": "the adapter keeps Complete only"}}
    arm("filter-green", row_filter_problems({"row_filter": rf_ok}, fld), [])
    arm("filter-red", len(row_filter_problems({"row_filter": {"inflection": dict(rf_ok["inflection"], kept_rows=9)}}, fld)), 1)
    arm("columns-19", (len(COLUMNS), COLUMNS[-1], len(BRIEF14)), (19, "business_date_claim", 14))
    print("selftest %s" % ("FAIL" if bad else "PASS (%d arms)" % count))
    return 1 if bad else 0


def main(argv):
    if len(argv) == 2 and argv[1] == "--selftest":
        return selftest()
    if len(argv) != 3:
        print(__doc__)
        return 2
    root, ac = argv[1], argv[2]
    table = {"DBF135-1-AC1": ac_all}
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
