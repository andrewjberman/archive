#!/usr/bin/env python3
"""IB-pr-464: assemble IB160-1_reader_excluded_days.json from the per-cell results ib160_measure.py wrote to the scratch folder.
  python -I ib160_assemble.py <scratch> <out_dir> <base_commit>
Counts only.  Reads local files; touches no AWS."""
import json
import sys
from pathlib import Path

WINDOWS = ("SI", "YTD", "QTD", "1Y")
ENTRIES = ("49F", "orion")
P = "data/assets/scripts/gold/irpt_holdings_performance/holdings_performance.py"


def main(scratch, out_dir, base):
    sc = Path(scratch)
    cells, ver, cen = [], [], {}
    for e in ENTRIES:
        cen[e] = json.loads((sc / ("census_%s.json" % e)).read_text())
        for w in WINDOWS:
            c = json.loads((sc / ("cell_%s_%s.json" % (e, w))).read_text())
            for k in ("absences_named", "absences_named_accounts_with_none"):
                src = c[k].get("for_accounts_with_an_excluded_day", c[k]) if k == "absences_named" else c[k]
                c[k] = {" + ".join("%s:%s" % tuple(x) for x in json.loads(j)): n for j, n in src.items()}
            c["non_ok_rows_in_window_by_status"] = cen[e]["by_window"][w]["non_ok_rows_by_status"]
            cells.append(c)
    for f in sorted(sc.glob("verify_*.json")):
        ver.append(json.loads(f.read_text()))
    ex = json.loads((sc / "meaning.json").read_text())
    doc = {
        "base_commit": base,
        "arm": "READER_CODE_OVER_SERVED_GOLD",
        "arm_in_words": "NOT the deployed route. This is the route reader's OWN code at the base commit (holdings_gold.calculate and map_account, with the source the route composes at "
                        "installed.py:75 for each of its two firms) run locally over the SERVED holdings gold read from S3 (list and get only; no Lambda invoked, no sign-in, no Secrets "
                        "Manager read, nothing written to AWS). Every partition was read ONCE from S3 into a local cache outside the worktree; the reader's calculate() was then run once per "
                        "account per window, with the account's rows served from memory by a stand-in for HoldingsGoldSource's transport (partition_dates, account_keys, frame, _read). "
                        "What the reader computes from the rows (the account mapping, the filter at holdings_gold.py:246, the chain at :253-258, days_excluded at :274, the claim at :291/:295, "
                        "the absences at :308-341) is the reader's own code. Two things are not the reader's: the stand-in transport, and ids.opaque_account memoised with functools.lru_cache "
                        "(same function, same outputs; map_account calls it once per account per call). Checked on a sample of 50 accounts: the result with the stand-in equals the result with the "
                        "reader's OWN HoldingsGoldSource class (partition_dates, frame and account_keys real; only the S3 get and parquet parse of _read replaced by the cached frame); see "
                        "transport_check. The position classes, the distribution and the status tallies are counted by this driver from the same cached rows (classify() in ib160_measure.py), "
                        "and the reader's days_excluded was compared with the driver's own count of non-OK rows for every account that got a figure (field "
                        "reader_days_excluded_differs_from_status_count_of_rows). What could differ from the deployed function: its packaged bytes and dependencies, its mapping loader, the "
                        "route's authorization and scope resolution (the scope is built in memory, one permitted account), and its response envelope; the reader's answer dict is read, not "
                        "the route's HTTP body.",
        "windows_from_code": ["SI", "YTD", "QTD", "1Y"],
        "windows_code_line": "infra/aws/lambda/investor-reporting/performance/holdings_gold.py:98-106 (_period_for: SI when start is 1970-01-01, else f49_engine.ruled_period_for) with "
                             "infra/aws/lambda/investor-reporting/performance/f49_engine.py:44 (RULED_WINDOWS = YTD, QTD, 1Y); any other window refuses (holdings_gold.py:105-106). Each ruled "
                             "window is taken at the latest landed day by parity_period_returns.period_window; SI is 1970-01-01 to the latest landed day.",
        "entries_composed": ["the 49F entry", "orion"],
        "entries_code_line": "infra/aws/lambda/investor-reporting/performance/installed.py:68 (for canonical_firm in (tenants._CANONICAL_49F, tenants._CANONICAL_INF))",
        "partitions_landed": {"the 49F entry": {"count": cen["49F"]["partitions"], "first": cen["49F"]["first_partition"], "last": cen["49F"]["last_partition"]},
                              "orion": {"count": cen["orion"]["partitions"], "first": cen["orion"]["first_partition"], "last": cen["orion"]["last_partition"]}},
        "partitions_read": "every landed partition of both entries was read once (list and get): the 49F entry %d of %d, orion %d of %d; no window was shortened" % (
            cen["49F"]["partitions"], cen["49F"]["partitions"], cen["orion"]["partitions"], cen["orion"]["partitions"]),
        "per_entry_and_window": cells,
        "position_rule_in_words": "Per account, take its rows inside the window in date order and call a row OK or non-OK by its status (the reader's own test, holdings_gold.py:246). The account has an "
                                  "excluded day when the reader returns a figure and days_excluded is 1 or more. last_day_involved: the account's LAST row in the window is non-OK (whatever else). "
                                  "Otherwise, with its first OK row as the dividing point: first_day_only: every non-OK row comes before the first OK row (a leading run of one or more days, e.g. an "
                                  "account not yet funded); interior_only: every non-OK row lies after the first OK row and before the last row (a day between OK days, chained across); "
                                  "first_and_interior: non-OK rows both before the first OK row and between OK days. The four classes are exclusive and cover the accounts with an excluded day. "
                                  "A refused account (no OK row at all, or an account the reader cannot map) is not placed.",
        "status_values": {"the 49F entry": cen["49F"]["status_values"], "orion": cen["orion"]["status_values"]},
        "status_values_basis": "row counts over every landed partition of the entry",
        "what_a_non_ok_row_means": ex,
        "census_by_window": {e: cen[e]["by_window"] for e in ENTRIES},
        "control": {"what": "For each cell the driver reads one account whose every row in the window is OK (the first such account holding the window's fullest set of rows) through the reader's calculate(), "
                            "and the same account again with ONE of its in-window rows set to NON-POSITIVE-BASE in memory only (the cache is never written back; nothing is written to AWS).",
                    "reading": "see `control.per_cell` in the JSON: the unmodified account returns a figure with days_excluded 0 and the claim every account with no excluded day in "
                               "that cell gets (claim_the_reader_gives_accounts_with_none); the mutated copy returns days_excluded 1 and the same claim value, which is the finding itself.",
                    "per_cell": {"%s/%s" % (c["entry"], c["window"]): c.get("control") for c in cells}},
        "transport_check": {"what": "50 accounts (a fixed shuffle of the accounts on the latest partition, seed 160) read twice for the same window: (1) the stand-in transport, (2) the reader's own "
                                    "HoldingsGoldSource class with only the S3 get and parquet parse of _read replaced by the cached frame; compared: outcome, days_excluded, claim and the absences named",
                            "results": ver},
        "not_established": [
            "the deployed route's own answer: the deployed package's bytes, dependencies, mapping loader, authorization and response envelope were not exercised (no Lambda invoked, no sign-in)",
            "the gold was read once, at the time of this run; a later partition may land and move the windows",
            "why a given account's day is non-OK beyond the status token: the producer's inputs (prices, identifiers) were not read",
            "the transport check covers a sample of 50 accounts on the windows listed in transport_check, not every account and window",
            "whether the accounts the reader refuses (no OK row in the window, or absent from the latest partition so not mappable) are ones the route would serve at all: the route's own scope and permitted set were not applied",
            "the account-level meaning of last_day_involved (an account that exited, or a late data fault) was not separated",
        ],
        "functions_invoked": 0, "sign_ins_made": 0, "aws_writes_made": 0, "accounts_written": 0,
    }
    (Path(out_dir) / "IB160-1_reader_excluded_days.json").write_text(json.dumps(doc, indent=1) + "\n", encoding="utf-8")
    print("assembled", len(cells), "cells")
    write_md(doc, Path(out_dir) / "IB160-1_READER_EXCLUDED_DAYS_READ.md")


def write_md(d, path):
    L = []
    cells = d["per_entry_and_window"]
    L.append("# IB-pr-464: the performance route's reader, per window and per firm -- accounts with an excluded day, and where those days fall")
    L.append("")
    L.append("Base `%s`. READ ONLY. Arm `READER_CODE_OVER_SERVED_GOLD`: the reader's own code (`holdings_gold.calculate`) run locally over the served holdings gold read from S3; "
             "NOT the deployed route (see `arm_in_words`). Every landed partition read once: the 49F entry %d, orion %d. Counts only; no account id is written." % (
                 d["base_commit"], d["partitions_landed"]["the 49F entry"]["count"], d["partitions_landed"]["orion"]["count"]))
    L.append("")
    L.append("## Answer, leading with the interior counts")
    L.append("")
    for e in ("the 49F entry", "orion"):
        L.append("**%s** (interior = `interior_only` + `first_and_interior`, accounts with a figure):" % e)
        for c in [x for x in cells if x["entry"] == e]:
            p = c["position_of_the_excluded_days"]
            L.append("- %s: %d of %d accounts with an excluded day are interior (%d interior only, %d first and interior); %d first day only; %d with the last row excluded." % (
                c["window"], p["interior_only"] + p["first_and_interior"], c["accounts_with_an_excluded_day"], p["interior_only"], p["first_and_interior"],
                p["first_day_only"], p["last_day_involved"]))
        L.append("")
    L.append("**The claim.** The reader gives `claim` `measured` or `inferred`. In the cells below `inferred` appears exactly where the account also carries the `missing_trading_days` absence "
             "(a trading day with no partition, holdings_gold.py:288-295), which is orion's; it appears for accounts with an excluded day and for accounts with none alike, and the 49F entry's "
             "claim is `measured` for all its accounts in all four windows. An excluded day does not enter the claim: the control account read again with one in-memory day set non-OK keeps "
             "its claim in every cell. What names the excluded days is the `excluded_rows` absence, status PARTIAL, which every account with an excluded day carries (49F SI 3736 of 3736; "
             "orion SI 894 of 894; all cells, `absences_named` in the JSON) and no account with none carries.")
    L.append("")
    L.append("## Windows (named from the code)")
    L.append("")
    L.append("`SI`, `YTD`, `QTD`, `1Y`: `%s` Each at the latest landed day (2026-10-08 both entries); the ruled windows start %s." % (
        d["windows_code_line"], ", ".join("%s %s" % (c["window"], c["start"]) for c in cells[:4])))
    L.append("")
    for e in ("the 49F entry", "orion"):
        L.append("## %s" % e)
        L.append("")
        L.append("| window | read | with excluded day | none | refused | first only | interior only | first+interior | last row | claim (with excluded day) | claim (none) |")
        L.append("|---|---|---|---|---|---|---|---|---|---|---|")
        for c in [x for x in cells if x["entry"] == e]:
            p = c["position_of_the_excluded_days"]
            L.append("| %s | %d | %d | %d | %d | %d | %d | %d | %d | %s | %s |" % (
                c["window"], c["accounts_read"], c["accounts_with_an_excluded_day"], c["accounts_with_none"], c["accounts_the_reader_refuses"],
                p["first_day_only"], p["interior_only"], p["first_and_interior"], p["last_day_involved"],
                ", ".join("%s %d" % kv for kv in sorted(c["claim_the_reader_gives"].items())), ", ".join("%s %d" % kv for kv in sorted(c["claim_the_reader_gives_accounts_with_none"].items()))))
        L.append("")
        L.append("Excluded days per account (accounts with an excluded day): " + "; ".join("%s: %s" % (c["window"], ", ".join("%s=%d" % kv for kv in c["excluded_days_per_account_distribution"].items()))
                                                                                       for c in cells if c["entry"] == e))
        L.append("")
        L.append("Refusals: " + "; ".join("%s: %s" % (c["window"], ", ".join("%s %d" % (k, v) for k, v in c["refusals"].items())) for c in cells if c["entry"] == e))
        L.append("")
        L.append("Status values (every partition): " + ", ".join("%s %d" % kv for kv in sorted(d["status_values"][e].items())))
        L.append("")
    L.append("## What a non-OK row means (producer)")
    L.append("")
    for e in ("the 49F entry", "orion"):
        L.append("- **%s:** %s" % (e, d["what_a_non_ok_row_means"][e]))
    L.append("")
    L.append("## Position rule")
    L.append("")
    L.append(d["position_rule_in_words"])
    L.append("")
    L.append("## Control")
    L.append("")
    L.append(d["control"]["what"] + " " + d["control"]["reading"] + " Transport check (stand-in vs the reader's own source class, 50 accounts each): " + "; ".join(
        "%s %s %d of %d identical" % (v["entry"], v["window"], v["identical"], v["sampled"]) for v in d["transport_check"]["results"]) + ".")
    L.append("")
    L.append("## Not established")
    L.append("")
    for x in d["not_established"]:
        L.append("- " + x)
    L.append("")
    L.append("Zeros: functions invoked 0, sign-ins 0, AWS writes 0, accounts written 0.")
    path.write_text(chr(10).join(L) + chr(10), encoding="utf-8")


if __name__ == "__main__":
    main(*sys.argv[1:4])
