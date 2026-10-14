"""plant_gen14.py -- the ISSUER's reference implementation of the gen_silver_rows.py interface, used ONLY to plant the PASS arm of
c14.AC1-AC3 and the loader checks at the cut (standing battery clause 1). Not given to the worker; writes nothing under the repo.

  python plant_gen14.py --g2 F --g5 F --g6 F --out DIR --deployed-tools FILE
"""
import argparse
import json
import os
import sys

import yaml

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import glib  # noqa: E402


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--g2", required=True)
    ap.add_argument("--g4", required=True)
    ap.add_argument("--g5", required=True)
    ap.add_argument("--g6", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--deployed-tools", required=True)
    a = ap.parse_args()
    deployed = set(json.load(open(a.deployed_tools, encoding="utf-8")))
    os.makedirs(a.out, exist_ok=True)
    n = 0
    for path in (a.g2, a.g4, a.g5, a.g6):
        for c in glib.parse(open(path, encoding="utf-8").read()):
            if not glib.in_scope(c):
                continue
            rt = glib.expected_read_tool(c, deployed)
            fr = glib.firm_rule(c)
            pn, pc = (c["producer"] or {}).get("name"), str((c["producer"] or {}).get("claim") or "")
            if pn:
                producer = ("inferred: " if "inferred" in pc else "") + pn
            else:
                producer = "NOT TRACED -- the contract names no producer (absent)"
            pk = c["partition"].get("keys") or []
            rule = c["size"].get("row_count_rule")
            row = {
                "bucket": c["bucket"],
                "prefix": c["s3_prefix"],
                "business_meaning": ("%s %s table `%s` in %s (%s): %s. %s" % (
                    c["layer"].capitalize(), c["format"], c["table"], c["bucket"], c["s3_prefix"], c["grain"],
                    "Client data forked by firm, account last-4 and platform; Opal-internal principals only until a data grant names the firm."
                    if fr == "firm-scoped" else "Opal-internal data.")) + "".join(" %s." % w for w in glib.marks(c) if w) + (" " + glib.LIVE49F if glib.is_49f_bd(c) else ""),
                "example_questions": list(c["common_queries"]) or ["Where is the %s %s table?" % (c["table"], c["layer"])],
                "grain": c["grain"],
                "freshness_field": ("FIELD:" + pk[0]) if pk else "NONE -- " + str(c["freshness"].get("basis")),
                "firm_scope_rule": fr,
                "never_sum_rules": [rule] if rule else "NONE -- the contract states no row-count rule for this table",
                "producer": producer,
                "tools": [rt] if rt else [],
                "read_tool": rt,
                "gap_owner": None if rt else "NFRA_OPLGTW",
                "table": c["table"], "layer": c["layer"], "format": c["format"],
                "contract": {"id": c["contract_id"], "size": c["size"], "freshness": c["freshness"],
                             "partition": c["partition"], "producer": c["producer"]},
                "fork_keys": c["fork_keys"],
                "nl_tags": c["nl_tags"],
                "retired": c["contract_id"] in glib.DO_NOT_SERVE,
                "open_items": c["open_items"],
            }
            if row["retired"]:
                row["retired_reason"] = "do-not-serve: " + str(c.get("routing") or "")
            with open(os.path.join(a.out, glib.entity(c["contract_id"]) + ".yaml"), "w", encoding="utf-8", newline="\n") as f:
                yaml.safe_dump(row, f, sort_keys=False, allow_unicode=True)
            n += 1
    print("wrote %d rows to %s" % (n, a.out))
    return 0


if __name__ == "__main__":
    sys.exit(main())
