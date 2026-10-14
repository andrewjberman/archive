"""plant_gen.py -- the ISSUER's reference implementation of the gen_harvest_rows.py interface, used ONLY to plant the PASS arm of
c12.AC1-AC3 at the cut (standing battery clause 1): proof that the checks pass on a correct row set and fail on a mutated one.
It is not given to the worker and writes nothing under the repo's catalog_entries.

  python plant_gen.py --g1 FILE --out DIR --deployed-tools FILE [--existing DIR]
"""
import argparse
import json
import os
import re
import sys

import yaml

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import g1lib  # noqa: E402


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--g1", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--deployed-tools", required=True)
    ap.add_argument("--existing", default=None)
    a = ap.parse_args()
    text = open(a.g1, encoding="utf-8").read()
    contracts = {}
    for b in re.findall(r"```json\n(.*?)\n```", text, re.S):
        d = json.loads(b)
        if isinstance(d, dict) and "contract_id" in d:
            contracts[d["s3_prefix"]] = d
    old = {}
    if a.existing:
        import glob
        for fp in glob.glob(os.path.join(a.existing, "harvest_*.yaml")):
            r0 = yaml.safe_load(open(fp, encoding="utf-8"))
            if "prefix_key" in r0:
                sys.path.insert(0, os.path.join(os.getcwd(), "lib"))
                import opal_naming
                r0["prefix"] = opal_naming.legacy_address(r0["prefix_key"])[len("s3://"):].partition("/")[2]
            old[r0["prefix"]] = r0
    deployed = set(json.load(open(a.deployed_tools, encoding="utf-8")))
    os.makedirs(a.out, exist_ok=True)
    for p, c in contracts.items():
        derived = c["freshness"]["derived_from"]
        pn, pc = c["producer"].get("name"), c["producer"].get("claim")
        if pn:
            producer = ("inferred: " if pc == "inferred" else "") + pn
        else:
            producer = "NOT TRACED -- G1 read no producer for this table (absent)"
        rt = g1lib.expected_read_tool(c, deployed)
        o = old.get(p) or {}
        row = {
            "bucket": c["bucket"],
            "business_meaning": o.get("business_meaning") or "%s %s table `%s` of %s (%s): %s. Opal-internal research data, served to Opal principals only."
                                % (c["layer"].capitalize(), c["format"], c["table"], c["bucket"], p, c["grain"]),
            "example_questions": list(o.get("example_questions") or []) + [q for q in c["common_queries"] if q not in (o.get("example_questions") or [])]
            or ["Where is the %s %s table of the harvest bucket?" % (c["table"], c["layer"])],
            "grain": c["grain"],
            "freshness_field": "NONE -- " + derived,
            "firm_scope_rule": "opal-internal-only",
            "never_sum_rules": (list(c["never_sum_rules"]) + [x for x in (o.get("never_sum_rules") if isinstance(o.get("never_sum_rules"), list) else []) if x not in c["never_sum_rules"]])
            or "NONE -- G1 states no never-sum rule for this table",
            "producer": producer,
            "read_tool": rt,
            "gap_owner": None if rt else "NFRA_OPLGTW",
            "table": c["table"], "layer": c["layer"], "format": c["format"],
            "contract": {"id": c["contract_id"], "size": c["size"], "keys": c["securities"], "freshness": c["freshness"],
                         "partition": c["partition"], "producer": c["producer"]},
            "nl_tags": c["nl_tags"],
            "retired": p in g1lib.RETIRE_REQUIRED,
        }
        lk = g1lib.legacy_key(p)
        if lk:
            row["prefix_key"] = lk
        else:
            row["prefix"] = p
        if row["retired"]:
            row["retired_reason"] = "superseded by gold article_security_mention (G1 section 2 item 4)"
        with open(os.path.join(a.out, "harvest_%s.yaml" % g1lib.slug(p)), "w", encoding="utf-8", newline="\n") as f:
            yaml.safe_dump(row, f, sort_keys=False, allow_unicode=True)
    print("wrote %d rows to %s" % (len(contracts), a.out))
    return 0


if __name__ == "__main__":
    sys.exit(main())
