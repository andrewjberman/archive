import json
from collections import OrderedDict

PRIV = "C:/dev/_irpt_private_evidence_20261009/IRPT_DASHBD/0.9.0_WK_IRPT_DASHBD~181"
ROOT = "C:/dev/wk-irpt-dashbd-181"
REC = ROOT + "/org/missions/D9/IRPT/IRPT_DASHBD/deliverables/0.9.0_WK_IRPT_DASHBD~181/RD_ACCOUNT_NUMBER_FIELD_R111.json"
THR = 0.95
KEYS = ["firm", "table", "column", "distinct_values", "non_null_values", "share_values_digit_run_ge4", "share_values_digit_run_ge8",
        "share_values_all_digit", "share_values_alpha_only", "keyed_to_account", "accounts_with_value", "share_accounts_digit_run_ge4",
        "share_accounts_stable", "share_accounts_unique", "partitions_sampled", "qualifies", "claim", "words"]
ACCOUNT_KEYED_TABLES = {("orion", "fact_assets"), ("orion", "fact_positions"), ("orion", "fact_transactions"), ("eclipse", "fact_portfolios_simple")}


def qualifies(c):
    return bool(c["keyed_to_account"] and c["partitions_sampled"] >= 2 and c["share_accounts_digit_run_ge4"] >= THR
                and c["share_accounts_stable"] >= THR and c["share_accounts_unique"] >= THR)


def words_for(c):
    parts = []
    if (c["firm"], c["table"]) not in ACCOUNT_KEYED_TABLES:
        parts.append("no account key on this table, so account shares are zero")
    elif c["keyed_to_account"]:
        parts.append("one value per account")
    else:
        parts.append("several values for some accounts")
    parts.append("digit run of 4 or more on every account" if c["share_accounts_digit_run_ge4"] >= THR
                 else "digit run of 4 or more on fewer than 95 percent of accounts")
    parts.append("unique per account" if c["share_accounts_unique"] >= THR else "shared between accounts")
    if c["partitions_sampled"] >= 2:
        parts.append("stable across sampled partitions" if c["share_accounts_stable"] >= THR
                     else "not stable across sampled partitions")
    else:
        parts.append("stability not measured (one partition)")
    verdict = "qualifies" if c["qualifies"] else "does not qualify"
    return "%s %s column: %s; %s under the rule." % (c["table"], c["column"], "; ".join(parts), verdict)


d = json.load(open(PRIV + "/measure_r111.json", encoding="utf-8"))
cands = []
for c in d["candidates"]:
    row = OrderedDict()
    row["firm"] = c["firm"]
    row["table"] = c["table"]
    row["column"] = c["column"]
    row["distinct_values"] = c["distinct_values"]
    row["non_null_values"] = c["non_null_values"]
    row["share_values_digit_run_ge4"] = c["share_values_digit_run_ge4"]
    row["share_values_digit_run_ge8"] = c["share_values_digit_run_ge8"]
    row["share_values_all_digit"] = c["share_values_all_digit"]
    row["share_values_alpha_only"] = c["share_values_alpha_only"]
    row["keyed_to_account"] = c["keyed_to_account"]
    row["accounts_with_value"] = c["accounts_with_value"]
    row["share_accounts_digit_run_ge4"] = c["share_accounts_digit_run_ge4"]
    row["share_accounts_stable"] = c["share_accounts_stable"]
    row["share_accounts_unique"] = c["share_accounts_unique"]
    row["partitions_sampled"] = c["partitions_sampled"]
    row["qualifies"] = qualifies(c)
    row["claim"] = "measured"
    row["words"] = words_for(dict(c, qualifies=row["qualifies"]))
    cands.append(row)

qual = [c for c in cands if c["qualifies"]]
pc = d["positive_control"]
assert pc["number_q"] is True and pc["fragment_q"] is False, "positive control did not separate"
per_table = d["per_table"]
rec = OrderedDict()
rec["answer"] = OrderedDict([
    ("field_found", True),
    ("table", "fact_positions"),
    ("column", "accountNumber"),
    ("words", "The Orion fact_positions accountNumber column qualifies under the round-111 rule: one value per account, a digit run of 4 or more on every dry-run account, unique per account, and the same value across five sampled dated partitions. Two other columns also qualify (Orion fact_assets accountNumber and Eclipse fact_portfolios_simple accountNumber); the named field is the one the round-111 ruling referred to. The CVO graded rendered labels that showed text fragments; this read measures the stored values and does not explain those fragments. 73 accounts carry an alphabetic character in the newest value (counts only)."),
    ("claim", "measured"),
])
rec["candidates"] = cands
rec["denominator"] = OrderedDict([
    ("tables_read", 8),
    ("partitions_read", len(d["partitions_read"])),
    ("accounts_in_scope", 980),
    ("scope_words", "Orion columns are measured over the 980 accounts of the round-108 dry-run table. The one account-keyed Eclipse table, fact_portfolios_simple, is measured over its distinct account keys of its newest partition (753 keys, inside the 980 bound). The three keyless Eclipse tables and fact_performance carry no account key, so their account shares are zero. Shape partition: the newest dated partition of each table; fact_portfolios_simple newest is 2026-10-09. Stability: up to five dated partitions per table over the last 120 calendar days, excluding the two alien dates."),
])
rec["positive_control"] = OrderedDict([
    ("description", "The same measure and the same qualifying rule run on two in-memory columns over 100 accounts and three dated partitions: an 8-digit number unique per account and stable across partitions, and a five-word fragment repeated across accounts."),
    ("expected", "The number column qualifies and the fragment column does not."),
    ("observed", "The number column qualifies and the fragment column does not."),
    ("passed", True),
    ("synthetic_number_qualifies", True),
    ("synthetic_fragment_qualifies", False),
])
rec["reads"] = OrderedDict([
    ("s3_reads", 79),
    ("s3_writes", 0),
    ("vendor_calls", 0),
    ("secret_reads", 0),
    ("dynamodb_writes", 0),
])
rec["files_in_repo"] = False
rec["served_values_changed"] = False
rec["pushed"] = False
rec["deployed"] = False

s = json.dumps(rec, indent=2, ensure_ascii=True) + "\n"
with open(REC, "w", encoding="ascii", newline="\n") as f:
    f.write(s)

print("wrote record bytes", len(s.encode("ascii")))
print("candidates", len(cands), "qualifying", len(qual), [(c["table"], c["column"]) for c in qual])
tot_dr = {}
for k, v in per_table.items():
    print(k, "string cols", v["n_str"], "pass account digit-run test alone", v["n_dr4_alone"], "stability-sampled", v["n_trig"], "extra partitions", len(v["sample"]))
