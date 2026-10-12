#!/usr/bin/env python3
"""IB-pr-476: read the eight per-(entry, window) result files ib166_measure.py wrote to the scratch, print the table and write the
numeric part of the record (counts and hashes only).  usage: python -I ib166_assemble.py <scratch> <out_json>"""
import json
import sys
from pathlib import Path

CTO = {"49F": {"SI": 23, "YTD": 19, "QTD": 2, "1Y": 20}, "orion": {"SI": 894, "YTD": 200, "QTD": 7, "1Y": 240}}
scratch, out = Path(sys.argv[1]), Path(sys.argv[2])
cells = {}
for entry in CTO:
    for window in CTO[entry]:
        cells[(entry, window)] = json.loads((scratch / ("cell166_%s_%s.json" % (entry, window))).read_text())
res = {"claim_moves_measured_to_inferred": {}, "rule_fires": {}, "rule_fires_on_accounts_already_inferred_at_base": {},
       "figures_hash_base": {}, "figures_hash_after": {}, "figures_compared_per_cell": {}, "accounts_refused_base_and_after": {},
       "partitions_read": {}, "accounts_with_a_figure": {}, "claim_at_base": {}, "claim_after": {}}
total = 0
for (entry, window), c in cells.items():
    assert c["figures_equal"] is True and c["refusals_differ"] == 0 and c["accounts_inferred_to_measured"] == 0
    assert c["accounts_with_both_new_members"] == c["figures_compared"] == c["accounts_where_the_two_members_sum_to_days_excluded"]
    assert c["accounts_where_value_facts_claim_differs_from_answer_claim"] == 0
    key = "%s/%s" % (entry, window)
    res["claim_moves_measured_to_inferred"].setdefault(entry, {})[window] = c["accounts_whose_claim_moves_measured_to_inferred"]
    res["rule_fires"].setdefault(entry, {})[window] = c["accounts_where_the_new_rule_fires"]
    res["rule_fires_on_accounts_already_inferred_at_base"].setdefault(entry, {})[window] = c["accounts_where_the_new_rule_fires_but_the_base_claim_was_already_inferred"]
    res["figures_hash_base"][key] = c["figures_hash_base"]
    res["figures_hash_after"][key] = c["figures_hash_after"]
    res["figures_compared_per_cell"][key] = c["figures_compared"]
    res["accounts_refused_base_and_after"][key] = [c["accounts_refused_old"], c["accounts_refused_new"]]
    res["partitions_read"][key] = c["partitions_read"]
    res["accounts_with_a_figure"][key] = c["figures_compared"]
    res["claim_at_base"][key] = c["old_claim"]
    res["claim_after"][key] = c["new_claim"]
    total += c["figures_compared"]
res["figures_compared"] = total
res["figures_unchanged"] = all(c["figures_equal"] for c in cells.values())
res["rule_fires_equals_the_ctos_v049_counts"] = res["rule_fires"] == CTO
res["claim_moves_equals_the_ctos_v049_counts"] = res["claim_moves_measured_to_inferred"] == CTO
out.write_text(json.dumps(res, sort_keys=True, indent=1))
print(json.dumps({k: res[k] for k in ("claim_moves_measured_to_inferred", "rule_fires", "rule_fires_on_accounts_already_inferred_at_base",
                                       "figures_compared", "figures_unchanged", "rule_fires_equals_the_ctos_v049_counts",
                                       "claim_moves_equals_the_ctos_v049_counts")}, sort_keys=True, indent=1))
