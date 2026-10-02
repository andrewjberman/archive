"""AMGT-ak-3 -- READ-ONLY rewrite plan for the STORED served reasons that carry a code.

Scans the pool: (1) every M-1 object (`management/v1/<key>/<as_of>.json`), newest per key, whose
`lusha_enrichment.reason` matches the code-shaped pattern; (2) every R-1 peers object
(`peers/v1/<key>/<as_of>.json`), newest per key, whose `csc_columns.absent[i].reason` matches it.
The replacement text is computed BY CALLING THE FIXED PRODUCER CODE
(`enrich.domain_for`, and `csc.build_csc_map` for the peers reasons), never typed here. WRITES NOTHING to the
pool: list and get only. The one output is the plan JSON next to this file.

Run from the worktree root:  PYTHONPATH="$(pwd)" python <this file>"""
import json
import os
import re
import sys

from lib.research.api import scoped_amgt
from lib.research.api.scoped_amgt import pool_reader
from lib.research.management import enrich
from lib.research.peers import csc
from lib.research.posture import fit as posture_fit

CODE = re.compile(r"[a-z]+_[a-z0-9_]+|_Equity|\.json|ABSENT")
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "m1_lusha_reason_plan.json")


def newest_per_key(client, prefix):
    keys = {}
    for page in client.get_paginator("list_objects_v2").paginate(Bucket=pool_reader.POOL_BUCKET, Prefix=prefix):
        for obj in page.get("Contents", []) or []:
            rest = obj["Key"][len(prefix):]
            parts = rest.split("/")
            if len(parts) == 2 and parts[1].endswith(".json"):
                keys.setdefault(parts[0], []).append(obj["Key"])
    return {name: sorted(ks)[-1] for name, ks in keys.items()}


def get(client, key):
    return json.loads(client.get_object(Bucket=pool_reader.POOL_BUCKET, Key=key)["Body"].read().decode("utf-8"))


def main():
    client = scoped_amgt._pool_client()
    entries, unplanned = [], []

    m1 = newest_per_key(client, scoped_amgt.MANAGEMENT_PREFIX)
    for name, key in sorted(m1.items()):
        doc = get(client, key)
        reason = (doc.get("lusha_enrichment") or {}).get("reason")
        if not isinstance(reason, str) or not CODE.search(reason):
            continue
        security_key = doc.get("security_key") or name
        _c, _i, after = enrich.domain_for(security_key, table={"domains": {}}, source_object=None)
        if not after or CODE.search(after) or not reason.startswith("no declared domain for "):
            unplanned.append({"security_key": security_key, "store_key": key, "before": reason})
            continue
        entries.append({"security_key": security_key, "route": "thesis",
                        "json_path": ".management.lusha_enrichment.reason", "store_key": key,
                        "store_field": "lusha_enrichment.reason", "before": reason, "after": after})

    peers = newest_per_key(client, scoped_amgt.PEERS_PREFIX)
    # the fixed producer, called once: the reason each absent column now carries, by column
    fixed = {a["column"]: a["reason"] for a in csc.build_csc_map(
        {"factors": list(posture_fit.load_registry()[0].values())})["absent"]}
    per_key = {}
    for name, key in sorted(peers.items()):
        doc = get(client, key)
        security_key = doc.get("security_key") or name
        for i, item in enumerate((doc.get("csc_columns") or {}).get("absent") or []):
            reason = item.get("reason")
            if not isinstance(reason, str) or not CODE.search(reason):
                continue
            after = fixed.get(item.get("column"))
            if not after or CODE.search(after):
                unplanned.append({"security_key": security_key, "store_key": key, "before": reason})
                continue
            entries.append({"security_key": security_key, "route": "peers",
                            "json_path": ".csc_columns.absent[%d].reason" % i, "store_key": key,
                            "store_field": "csc_columns.absent[%d].reason" % i, "before": reason, "after": after})
            per_key[security_key] = per_key.get(security_key, 0) + 1

    plan = {"denominator": len(m1), "denominator_unit": "M-1 objects scanned (newest per security key)",
            "peers_denominator": len(peers), "peers_denominator_unit": "R-1 peers objects scanned (newest per security key)",
            "peers_entries_per_key": per_key, "entries": entries, "unplanned": unplanned}
    with open(OUT, "w", encoding="utf-8", newline="\n") as handle:
        json.dump(plan, handle, indent=1, ensure_ascii=True)
        handle.write("\n")
    thesis = [e for e in entries if e["route"] == "thesis"]
    print("M-1 scanned %d; thesis entries %d; peers scanned %d; peers entries %d; unplanned %d"
          % (len(m1), len(thesis), len(peers), len(entries) - len(thesis), len(unplanned)))
    print("peers entries per key: %d keys, %s entries each (min %d, max %d)" % (
        len(per_key), sorted(set(per_key.values())), min(per_key.values()), max(per_key.values())))
    return 0


if __name__ == "__main__":
    sys.exit(main())
